<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** API error with HTTP status and response details. */
class ApiException extends DocGenException
{
    public function __construct(
        public readonly int $statusCode,
        string $message,
        public readonly ?string $responseBody = null,
    ) {
        parent::__construct($message, $statusCode);
    }
}
