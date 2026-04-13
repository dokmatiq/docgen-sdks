<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

/** Webhook payload sent when an async job completes. */
final class WebhookPayload
{
    public function __construct(
        public readonly string $jobId,
        public readonly string $status,
        public readonly ?string $completedAt = null,
        public readonly ?string $errorMessage = null,
    ) {}

    /** @param array<string, mixed> $data */
    public static function fromArray(array $data): self
    {
        return new self(
            jobId: $data['jobId'],
            status: $data['status'],
            completedAt: $data['completedAt'] ?? null,
            errorMessage: $data['errorMessage'] ?? null,
        );
    }
}
