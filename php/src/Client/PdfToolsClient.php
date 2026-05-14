<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;

/** Client for PDF utility operations. */
final class PdfToolsClient
{
    public function __construct(private readonly Transport $transport) {}

    /**
     * Merge multiple PDFs into one.
     *
     * @param string[] $pdfPathsOrBase64 Array of file paths or base64 strings
     */
    public function merge(array $pdfPathsOrBase64): string
    {
        $pdfs = array_map(fn (string $p) => FileUtils::toBase64($p), $pdfPathsOrBase64);
        return $this->transport->requestBytes('POST', '/api/pdf/merge', ['pdfs' => $pdfs]);
    }

    /**
     * Split a PDF by page ranges.
     *
     * @param string[] $ranges e.g. ["1-3", "4-6"]
     * @return string[] Array of base64-encoded PDFs
     */
    public function split(string $pdfPathOrBase64, array $ranges): array
    {
        $data = $this->transport->requestJson('POST', '/api/pdf/split', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'ranges' => $ranges,
        ]);
        return $data['parts'] ?? [];
    }

    /** Extract text from a PDF. */
    public function extractText(string $pdfPathOrBase64): string
    {
        $data = $this->transport->requestJson('POST', '/api/pdf-tools/extract-text', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
        return $data['text'] ?? '';
    }

    /** Get or set PDF metadata. */
    public function metadata(string $pdfPathOrBase64, ?array $metadata = null): array
    {
        $body = ['pdfBase64' => FileUtils::toBase64($pdfPathOrBase64)];
        if ($metadata !== null) {
            $body['metadata'] = $metadata;
        }
        return $this->transport->requestJson('POST', '/api/pdf/metadata', $body);
    }

    /** Convert a PDF to PDF/A. */
    public function toPdfA(string $pdfPathOrBase64): string
    {
        return $this->transport->requestBytes('POST', '/api/pdf/to-pdfa', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
    }

    /** Rotate PDF pages. */
    public function rotate(string $pdfPathOrBase64, int $degrees, ?string $pages = null): string
    {
        $body = [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'degrees' => $degrees,
        ];
        if ($pages !== null) $body['pages'] = $pages;

        return $this->transport->requestBytes('POST', '/api/pdf/rotate', $body);
    }
}
