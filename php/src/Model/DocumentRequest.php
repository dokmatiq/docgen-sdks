<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Main document generation request. */
final class DocumentRequest
{
    /**
     * @param array<string, string>|null $fields
     * @param array<string, string>|null $bookmarks
     * @param ImageData[]|null $images
     * @param QrCodeData[]|null $qrCodes
     * @param array<string, TableData>|null $tables
     * @param ContentArea[]|null $contentAreas
     */
    public function __construct(
        public readonly ?string $htmlContent = null,
        public readonly ?string $markdownContent = null,
        public readonly ?string $templateName = null,
        public readonly ?string $templateBase64 = null,
        public readonly ?array $fields = null,
        public readonly ?array $bookmarks = null,
        public readonly ?array $images = null,
        public readonly ?array $qrCodes = null,
        public readonly ?array $tables = null,
        public readonly ?PageSettings $pageSettings = null,
        public readonly string|WatermarkConfig|null $watermark = null,
        public readonly ?StationeryConfig $stationery = null,
        public readonly ?array $contentAreas = null,
        public readonly ?InvoiceData $invoiceData = null,
        public readonly ?string $password = null,
        public readonly ?OutputFormat $outputFormat = null,
        public readonly ?string $callbackUrl = null,
        public readonly ?string $callbackSecret = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
