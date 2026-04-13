<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 500 – Internal server error. */
class ServerException extends ApiException
{
    public function __construct(string $message = 'Internal server error', ?string $responseBody = null)
    {
        parent::__construct(500, $message, $responseBody);
    }
}
