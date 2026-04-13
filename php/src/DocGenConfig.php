<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen;

/** SDK configuration. */
final class DocGenConfig
{
    public function __construct(
        public readonly string $apiKey,
        public readonly string $baseUrl = 'https://api.dokmatiq.com',
        public readonly int $timeout = 120,
        public readonly int $maxRetries = 3,
        public readonly float $retryDelay = 0.5,
        public readonly float $retryMultiplier = 2.0,
        public readonly float $retryMaxDelay = 30.0,
    ) {}
}
