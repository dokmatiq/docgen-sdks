<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Exception;

/** 503 – Service unavailable (e.g. LibreOffice pool exhausted). */
class ServiceUnavailableException extends ApiException
{
    public function __construct(string $message = 'Service unavailable', ?string $responseBody = null)
    {
        parent::__construct(503, $message, $responseBody);
    }
}
