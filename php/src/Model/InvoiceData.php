<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Structured invoice data for ZUGFeRD/Factur-X and XRechnung. */
final class InvoiceData
{
    /**
     * @param InvoiceItem[] $items
     */
    public function __construct(
        public readonly string $invoiceNumber,
        public readonly string $invoiceDate,
        public readonly Party $seller,
        public readonly Party $buyer,
        public readonly array $items = [],
        public readonly string $currency = 'EUR',
        public readonly ?BankAccount $bankAccount = null,
        public readonly ?string $paymentTerms = null,
        public readonly ?string $dueDate = null,
        public readonly ?string $note = null,
        public readonly ?string $buyerReference = null,
        public readonly string $invoiceTypeCode = '380',
        public readonly ZugferdProfile $profile = ZugferdProfile::EN16931,
        public readonly ?XRechnungFormat $xrechnungFormat = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
