<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\Transport;

/** Client for template management. */
final class TemplatesClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Upload a template file. */
    public function upload(string $filePath): array
    {
        $response = $this->transport->uploadMultipart('POST', '/api/templates/upload', $filePath);
        return json_decode($response, true) ?: [];
    }

    /** List all uploaded templates. */
    public function list(): array
    {
        return $this->transport->requestJson('GET', '/api/templates');
    }

    /** Delete a template by name. */
    public function delete(string $name): void
    {
        $this->transport->requestJson('DELETE', "/api/templates/{$name}");
    }
}
