<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;

/** Client for PDF preview operations. */
final class PreviewClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Preview a single page as PNG. Returns raw image bytes. */
    public function previewPage(string $pdfPathOrBase64, int $page = 1, int $dpi = 150): string
    {
        return $this->transport->requestBytes('POST', '/api/preview/page', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'page' => $page,
            'dpi' => $dpi,
        ]);
    }

    /**
     * Preview multiple pages as base64-encoded PNGs.
     *
     * @return array<int, array{page: int, imageBase64: string}>
     */
    public function previewPages(string $pdfPathOrBase64, ?int $maxPages = null, int $dpi = 150): array
    {
        $body = [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'dpi' => $dpi,
        ];
        if ($maxPages !== null) $body['maxPages'] = $maxPages;

        $data = $this->transport->requestJson('POST', '/api/preview/pages', $body);
        return $data['pages'] ?? [];
    }

    /** Get the page count of a PDF. */
    public function pageCount(string $pdfPathOrBase64): int
    {
        $data = $this->transport->requestJson('POST', '/api/preview/page-count', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
        return (int) ($data['pageCount'] ?? 0);
    }
}
