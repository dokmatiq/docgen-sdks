<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Multi-part document composition request. */
final class ComposeRequest
{
    /**
     * @param DocumentPart[] $parts
     * @param ContentArea[]|null $contentAreas
     */
    public function __construct(
        public readonly array $parts,
        public readonly string|WatermarkConfig|null $watermark = null,
        public readonly ?StationeryConfig $stationery = null,
        public readonly ?array $contentAreas = null,
        public readonly ?InvoiceData $invoiceData = null,
        public readonly ?string $password = null,
        public readonly ?OutputFormat $outputFormat = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
