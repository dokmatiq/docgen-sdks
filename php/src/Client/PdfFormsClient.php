<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;

/** Client for PDF form operations. */
final class PdfFormsClient
{
    public function __construct(private readonly Transport $transport) {}

    /**
     * Inspect form fields in a PDF.
     *
     * @return array<int, array<string, mixed>>
     */
    public function inspectFields(string $pdfPathOrBase64): array
    {
        $data = $this->transport->requestJson('POST', '/api/pdf-forms/inspect', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
        return $data['fields'] ?? $data;
    }

    /**
     * Fill form fields in a PDF.
     *
     * @param array<string, string> $fields
     */
    public function fillForm(string $pdfPathOrBase64, array $fields, bool $flatten = true): string
    {
        return $this->transport->requestBytes('POST', '/api/pdf-forms/fill', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'fields' => $fields,
            'flatten' => $flatten,
        ]);
    }
}
