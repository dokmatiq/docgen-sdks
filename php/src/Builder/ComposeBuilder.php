<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Builder;

use Dokmatiq\DocGen\Client\DocumentsClient;
use Dokmatiq\DocGen\Model\ComposeRequest;
use Dokmatiq\DocGen\Model\ContentArea;
use Dokmatiq\DocGen\Model\DocumentPart;
use Dokmatiq\DocGen\Model\InvoiceData;
use Dokmatiq\DocGen\Model\OutputFormat;
use Dokmatiq\DocGen\Model\StationeryConfig;
use Dokmatiq\DocGen\Model\WatermarkConfig;

/** Fluent builder for multi-part document composition. */
final class ComposeBuilder
{
    /** @var DocumentPart[] */
    private array $parts = [];
    private string|WatermarkConfig|null $watermark = null;
    private ?StationeryConfig $stationery = null;
    /** @var ContentArea[] */
    private array $contentAreas = [];
    private ?InvoiceData $invoiceData = null;
    private ?string $password = null;
    private ?OutputFormat $outputFormat = null;

    public function __construct(private readonly DocumentsClient $client) {}

    public function part(DocumentPart $part): self { $this->parts[] = $part; return $this; }

    public function htmlPart(string $html): self
    {
        $this->parts[] = new DocumentPart(htmlContent: $html);
        return $this;
    }

    public function markdownPart(string $md): self
    {
        $this->parts[] = new DocumentPart(markdownContent: $md);
        return $this;
    }

    public function watermark(string|WatermarkConfig $watermark): self { $this->watermark = $watermark; return $this; }
    public function stationery(StationeryConfig $stationery): self { $this->stationery = $stationery; return $this; }
    public function contentArea(ContentArea $area): self { $this->contentAreas[] = $area; return $this; }
    public function invoice(InvoiceData $data): self { $this->invoiceData = $data; return $this; }
    public function password(string $pw): self { $this->password = $pw; return $this; }
    public function asPdf(): self { $this->outputFormat = OutputFormat::PDF; return $this; }
    public function asDocx(): self { $this->outputFormat = OutputFormat::DOCX; return $this; }

    /** Build the ComposeRequest without sending it. */
    public function build(): ComposeRequest
    {
        return new ComposeRequest(
            parts: $this->parts,
            watermark: $this->watermark,
            stationery: $this->stationery,
            contentAreas: $this->contentAreas ?: null,
            invoiceData: $this->invoiceData,
            password: $this->password,
            outputFormat: $this->outputFormat,
        );
    }

    /** Compose the document. Returns raw bytes. */
    public function generate(): string
    {
        return $this->client->compose($this->build());
    }
}
