<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Bank account details for payment. */
final class BankAccount
{
    public function __construct(
        public readonly string $iban,
        public readonly ?string $bic = null,
        public readonly ?string $accountHolder = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
