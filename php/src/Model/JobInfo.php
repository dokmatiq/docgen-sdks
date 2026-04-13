<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

/** Information about an async generation job. */
final class JobInfo
{
    public function __construct(
        public readonly string $jobId,
        public readonly JobStatus $status,
        public readonly ?string $createdAt = null,
        public readonly ?string $completedAt = null,
        public readonly ?string $errorMessage = null,
    ) {}

    /** @param array<string, mixed> $data */
    public static function fromArray(array $data): self
    {
        return new self(
            jobId: $data['jobId'],
            status: JobStatus::from($data['status']),
            createdAt: $data['createdAt'] ?? null,
            completedAt: $data['completedAt'] ?? null,
            errorMessage: $data['errorMessage'] ?? null,
        );
    }
}
