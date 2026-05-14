<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\Transport;
use Dokmatiq\DocGen\Model\ComposeRequest;
use Dokmatiq\DocGen\Model\DocumentRequest;
use Dokmatiq\DocGen\Model\JobInfo;

/** Client for document generation endpoints. */
final class DocumentsClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Generate a document and return raw PDF/DOCX bytes. */
    public function generate(DocumentRequest $request): string
    {
        return $this->transport->requestBytes('POST', '/api/documents/generate', $request);
    }

    /** Compose a multi-part document. */
    public function compose(ComposeRequest $request): string
    {
        return $this->transport->requestBytes('POST', '/api/documents/compose', $request);
    }

    /** Start async document generation. Returns job info. */
    public function generateAsync(DocumentRequest $request): JobInfo
    {
        $data = $this->transport->requestJson('POST', '/api/documents/generate-async', $request);
        return JobInfo::fromArray($data);
    }

    /** Get job status. */
    public function getJob(string $jobId): JobInfo
    {
        $data = $this->transport->requestJson('GET', "/api/documents/jobs/{$jobId}");
        return JobInfo::fromArray($data);
    }

    /** Download completed job result. */
    public function downloadJob(string $jobId): string
    {
        return $this->transport->requestBytes('GET', "/api/documents/jobs/{$jobId}/download");
    }

    /**
     * Poll until job completes, then return bytes.
     *
     * @param float $pollInterval Seconds between polls (default 2)
     * @param float $timeout Max seconds to wait (default 300)
     */
    public function waitForJob(string $jobId, float $pollInterval = 2.0, float $timeout = 300.0): string
    {
        $start = microtime(true);
        while (true) {
            $job = $this->getJob($jobId);
            if ($job->status === 'COMPLETED') {
                return $this->downloadJob($jobId);
            }
            if ($job->status === 'FAILED') {
                throw new \RuntimeException("Job {$jobId} failed: " . ($job->errorMessage ?? 'unknown error'));
            }
            if (microtime(true) - $start > $timeout) {
                throw new \RuntimeException("Job {$jobId} timed out after {$timeout}s");
            }
            usleep((int) ($pollInterval * 1_000_000));
        }
    }
}
