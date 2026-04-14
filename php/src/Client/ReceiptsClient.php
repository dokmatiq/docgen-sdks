<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\Transport;

/** Client for AI-powered receipt and ticket data extraction. */
final class ReceiptsClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Extract structured data from a receipt image or PDF. Requires AI consent. */
    public function extract(string $filePath): array
    {
        $raw = $this->transport->uploadMultipart('POST', '/api/receipts/extract', $filePath, 'file');
        return json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    }

    /** Submit receipt for async extraction with optional webhook. */
    public function extractAsync(string $filePath, ?string $callbackUrl = null, ?string $callbackSecret = null): array
    {
        $fields = [];
        if ($callbackUrl !== null) $fields['callbackUrl'] = $callbackUrl;
        if ($callbackSecret !== null) $fields['callbackSecret'] = $callbackSecret;
        $raw = $this->transport->uploadMultipart('POST', '/api/receipts/extract-async', $filePath, 'file', $fields);
        return json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    }

    /** Extract receipt and generate expense report document. */
    public function toDocument(string $filePath, string $format = 'PDF', string $title = 'Spesenbeleg'): array
    {
        $fields = ['format' => $format, 'title' => $title];
        $raw = $this->transport->uploadMultipart('POST', '/api/receipts/to-document', $filePath, 'file', $fields);
        return json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    }

    /** Export receipt data as CSV (DATEV-compatible). Returns raw CSV bytes. */
    public function exportCsv(array $receipts): string
    {
        return $this->transport->requestBytes('POST', '/api/receipts/export/csv', $receipts);
    }

    /** Export receipt data as XLSX. Returns raw XLSX bytes. */
    public function exportXlsx(array $receipts): string
    {
        return $this->transport->requestBytes('POST', '/api/receipts/export/xlsx', $receipts);
    }

    /** Get async job status. */
    public function getJob(string $jobId): array
    {
        return $this->transport->requestJson('GET', "/api/receipts/jobs/{$jobId}");
    }

    /** Get async job extraction result. */
    public function getJobResult(string $jobId): array
    {
        return $this->transport->requestJson('GET', "/api/receipts/jobs/{$jobId}/result");
    }

    /** List all async receipt jobs. */
    public function listJobs(): array
    {
        return $this->transport->requestJson('GET', '/api/receipts/jobs');
    }
}
