<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 401 – Invalid or missing API key. */
class AuthenticationException extends ApiException
{
    public function __construct(string $message = 'Invalid or missing API key', ?string $responseBody = null)
    {
        parent::__construct(401, $message, $responseBody);
    }
}
