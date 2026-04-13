<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 409 – Conflict (e.g. resource already exists). */
class ConflictException extends ApiException
{
    public function __construct(string $message = 'Resource conflict', ?string $responseBody = null)
    {
        parent::__construct(409, $message, $responseBody);
    }
}
