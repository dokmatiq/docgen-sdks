<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Single line item on an invoice. */
final class InvoiceItem
{
    public function __construct(
        public readonly string $description,
        public readonly float $quantity = 1.0,
        public readonly InvoiceUnit $unit = InvoiceUnit::PIECE,
        public readonly float $unitPrice = 0.0,
        public readonly float $vatRate = 19.0,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
