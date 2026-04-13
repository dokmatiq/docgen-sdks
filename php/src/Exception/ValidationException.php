<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 400 – Validation error with field-level details. */
class ValidationException extends ApiException
{
    /**
     * @param array<string, string>|null $fieldErrors
     */
    public function __construct(
        string $message,
        ?string $responseBody = null,
        public readonly ?array $fieldErrors = null,
        public readonly ?string $hint = null,
    ) {
        parent::__construct(400, $message, $responseBody);
    }
}
