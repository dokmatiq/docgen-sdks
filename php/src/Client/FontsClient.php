<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\Transport;

/** Client for font management. */
final class FontsClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Upload a font file. */
    public function upload(string $filePath): array
    {
        $response = $this->transport->uploadMultipart('POST', '/api/fonts/upload', $filePath);
        return json_decode($response, true) ?: [];
    }

    /** List all uploaded fonts. */
    public function list(): array
    {
        return $this->transport->requestJson('GET', '/api/fonts');
    }

    /** Delete a font by name. */
    public function delete(string $name): void
    {
        $this->transport->requestJson('DELETE', "/api/fonts/{$name}");
    }
}
