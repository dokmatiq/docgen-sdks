<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

/** Result of AI-based data extraction. */
final class ExtractionResult
{
    public function __construct(
        public readonly ?InvoiceData $invoiceData = null,
        public readonly ?float $confidence = null,
        public readonly ?string $rawText = null,
    ) {}

    /** @param array<string, mixed> $data */
    public static function fromArray(array $data): self
    {
        return new self(
            invoiceData: isset($data['invoiceData']) ? new InvoiceData(
                number: $data['invoiceData']['number'] ?? '',
                date: $data['invoiceData']['date'] ?? '',
                seller: new Party(
                    name: $data['invoiceData']['seller']['name'] ?? '',
                    street: $data['invoiceData']['seller']['street'] ?? null,
                    zip: $data['invoiceData']['seller']['zip'] ?? null,
                    city: $data['invoiceData']['seller']['city'] ?? null,
                ),
                buyer: new Party(
                    name: $data['invoiceData']['buyer']['name'] ?? '',
                    street: $data['invoiceData']['buyer']['street'] ?? null,
                    zip: $data['invoiceData']['buyer']['zip'] ?? null,
                    city: $data['invoiceData']['buyer']['city'] ?? null,
                ),
            ) : null,
            confidence: $data['confidence'] ?? null,
            rawText: $data['rawText'] ?? null,
        );
    }
}
