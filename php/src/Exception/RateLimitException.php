<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 429 – Rate limit exceeded. */
class RateLimitException extends ApiException
{
    public function __construct(
        string $message = 'Rate limit exceeded',
        ?string $responseBody = null,
        public readonly ?int $retryAfter = null,
    ) {
        parent::__construct(429, $message, $responseBody);
    }
}
