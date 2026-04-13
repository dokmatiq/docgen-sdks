<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Webhook;

use Dokmatiq\DocGen\Model\WebhookPayload;

/** HMAC-SHA256 webhook signature verification. */
final class WebhookVerifier
{
    public function __construct(private readonly string $secret) {}

    /** Verify the webhook signature and return the parsed payload. */
    public function verify(string $body, string $signature): WebhookPayload
    {
        $expected = hash_hmac('sha256', $body, $this->secret);

        if (!hash_equals($expected, $signature)) {
            throw new \RuntimeException('Invalid webhook signature');
        }

        $data = json_decode($body, true, 512, JSON_THROW_ON_ERROR);
        return WebhookPayload::fromArray($data);
    }

    /** Check if a signature is valid without throwing. */
    public function isValid(string $body, string $signature): bool
    {
        $expected = hash_hmac('sha256', $body, $this->secret);
        return hash_equals($expected, $signature);
    }
}
