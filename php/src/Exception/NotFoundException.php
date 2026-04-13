<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 404 – Resource not found. */
class NotFoundException extends ApiException
{
    public function __construct(string $message = 'Resource not found', ?string $responseBody = null)
    {
        parent::__construct(404, $message, $responseBody);
    }
}
