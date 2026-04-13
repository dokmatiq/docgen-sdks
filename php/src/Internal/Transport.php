<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Internal;

use Dokmatiq\DocGen\DocGenConfig;
use Dokmatiq\DocGen\Exception\ApiException;
use Dokmatiq\DocGen\Exception\AuthenticationException;
use Dokmatiq\DocGen\Exception\ConflictException;
use Dokmatiq\DocGen\Exception\NotFoundException;
use Dokmatiq\DocGen\Exception\RateLimitException;
use Dokmatiq\DocGen\Exception\ServerException;
use Dokmatiq\DocGen\Exception\ServiceUnavailableException;
use Dokmatiq\DocGen\Exception\ValidationException;

/** cURL-based HTTP transport with retry and error mapping. */
final class Transport
{
    private const RETRYABLE = [429, 500, 502, 503, 504];

    public function __construct(private readonly DocGenConfig $config) {}

    // ── JSON request → decoded array ────────────────────────────────

    /** @return array<string, mixed> */
    public function requestJson(string $method, string $path, mixed $body = null): array
    {
        $response = $this->doRequest($method, $path, $body);
        $decoded = json_decode($response, true);
        return is_array($decoded) ? $decoded : [];
    }

    // ── Binary request → raw bytes ──────────────────────────────────

    public function requestBytes(string $method, string $path, mixed $body = null): string
    {
        return $this->doRequest($method, $path, $body, expectBinary: true);
    }

    // ── Multipart upload ────────────────────────────────────────────

    /**
     * @param array<string, string> $fields
     */
    public function uploadMultipart(string $method, string $path, string $filePath, string $fileField = 'file', array $fields = []): string
    {
        $url = $this->url($path);

        $postFields = $fields;
        $postFields[$fileField] = new \CURLFile($filePath);

        $attempt = 0;
        while (true) {
            $ch = curl_init($url);
            curl_setopt_array($ch, [
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_CUSTOMREQUEST => $method,
                CURLOPT_HTTPHEADER => [
                    'X-API-Key: ' . $this->config->apiKey,
                    'Accept: application/json',
                ],
                CURLOPT_POSTFIELDS => $postFields,
                CURLOPT_TIMEOUT => $this->config->timeout,
            ]);

            $responseBody = curl_exec($ch);
            $statusCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $curlError = curl_error($ch);
            curl_close($ch);

            if ($responseBody === false) {
                throw new ApiException(0, 'cURL error: ' . $curlError);
            }

            if ($statusCode >= 200 && $statusCode < 300) {
                return (string) $responseBody;
            }

            if ($this->shouldRetry($statusCode, $attempt)) {
                $this->waitBeforeRetry($attempt);
                $attempt++;
                continue;
            }

            $this->throwForStatus($statusCode, (string) $responseBody);
        }
    }

    // ── Core request ────────────────────────────────────────────────

    private function doRequest(string $method, string $path, mixed $body = null, bool $expectBinary = false): string
    {
        $url = $this->url($path);
        $attempt = 0;

        while (true) {
            $ch = curl_init($url);
            $headers = [
                'X-API-Key: ' . $this->config->apiKey,
                'Accept: ' . ($expectBinary ? 'application/octet-stream' : 'application/json'),
            ];

            $options = [
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_CUSTOMREQUEST => $method,
                CURLOPT_HTTPHEADER => $headers,
                CURLOPT_TIMEOUT => $this->config->timeout,
            ];

            if ($body !== null) {
                $json = json_encode(Serializer::toArray($body), JSON_THROW_ON_ERROR);
                $options[CURLOPT_POSTFIELDS] = $json;
                $options[CURLOPT_HTTPHEADER][] = 'Content-Type: application/json';
            }

            curl_setopt_array($ch, $options);

            $rawHeaders = '';
            curl_setopt($ch, CURLOPT_HEADERFUNCTION, function ($ch, string $header) use (&$rawHeaders): int {
                $rawHeaders .= $header;
                return strlen($header);
            });

            $responseBody = curl_exec($ch);
            $statusCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $curlError = curl_error($ch);
            curl_close($ch);

            if ($responseBody === false) {
                throw new ApiException(0, 'cURL error: ' . $curlError);
            }

            if ($statusCode >= 200 && $statusCode < 300) {
                return (string) $responseBody;
            }

            if ($this->shouldRetry($statusCode, $attempt)) {
                $retryAfter = $this->parseRetryAfter($rawHeaders);
                $this->waitBeforeRetry($attempt, $retryAfter);
                $attempt++;
                continue;
            }

            $this->throwForStatus($statusCode, (string) $responseBody);
        }
    }

    // ── Helpers ─────────────────────────────────────────────────────

    private function url(string $path): string
    {
        return rtrim($this->config->baseUrl, '/') . '/' . ltrim($path, '/');
    }

    private function shouldRetry(int $status, int $attempt): bool
    {
        return $attempt < $this->config->maxRetries && in_array($status, self::RETRYABLE, true);
    }

    private function waitBeforeRetry(int $attempt, ?float $retryAfter = null): void
    {
        if ($retryAfter !== null) {
            $delay = $retryAfter;
        } else {
            $delay = min(
                $this->config->retryDelay * ($this->config->retryMultiplier ** $attempt),
                $this->config->retryMaxDelay,
            );
        }
        usleep((int) ($delay * 1_000_000));
    }

    private function parseRetryAfter(string $headers): ?float
    {
        if (preg_match('/Retry-After:\s*(\d+)/i', $headers, $m)) {
            return (float) $m[1];
        }
        return null;
    }

    /** @return never */
    private function throwForStatus(int $status, string $body): void
    {
        $data = json_decode($body, true);
        $message = $data['message'] ?? $data['error'] ?? "HTTP $status";

        throw match ($status) {
            400 => new ValidationException(
                $message,
                $body,
                $data['fieldErrors'] ?? null,
                $data['hint'] ?? null,
            ),
            401 => new AuthenticationException($message, $body),
            404 => new NotFoundException($message, $body),
            409 => new ConflictException($message, $body),
            429 => new RateLimitException($message, $body, $data['retryAfter'] ?? null),
            500 => new ServerException($message, $body),
            503 => new ServiceUnavailableException($message, $body),
            default => new ApiException($status, $message, $body),
        };
    }
}
