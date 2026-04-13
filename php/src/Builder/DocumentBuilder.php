<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Builder;

use Dokmatiq\DocGen\Client\DocumentsClient;
use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Model\ContentArea;
use Dokmatiq\DocGen\Model\DocumentRequest;
use Dokmatiq\DocGen\Model\ImageData;
use Dokmatiq\DocGen\Model\InvoiceData;
use Dokmatiq\DocGen\Model\OutputFormat;
use Dokmatiq\DocGen\Model\PageSettings;
use Dokmatiq\DocGen\Model\QrCodeData;
use Dokmatiq\DocGen\Model\StationeryConfig;
use Dokmatiq\DocGen\Model\TableData;
use Dokmatiq\DocGen\Model\WatermarkConfig;

/**
 * Fluent builder for document generation.
 *
 * Usage:
 *   $pdf = $dg->document()
 *       ->html('<h1>Hello {{name}}</h1>')
 *       ->field('name', 'World')
 *       ->watermark('DRAFT')
 *       ->asPdf()
 *       ->generate();
 */
final class DocumentBuilder
{
    private ?string $htmlContent = null;
    private ?string $markdownContent = null;
    private ?string $templateName = null;
    private ?string $templateBase64 = null;
    /** @var array<string, string> */
    private array $fields = [];
    /** @var array<string, string> */
    private array $bookmarks = [];
    /** @var ImageData[] */
    private array $images = [];
    /** @var QrCodeData[] */
    private array $qrCodes = [];
    /** @var array<string, TableData> */
    private array $tables = [];
    private ?PageSettings $pageSettings = null;
    private string|WatermarkConfig|null $watermark = null;
    private ?StationeryConfig $stationery = null;
    /** @var ContentArea[] */
    private array $contentAreas = [];
    private ?InvoiceData $invoiceData = null;
    private ?string $password = null;
    private ?OutputFormat $outputFormat = null;
    private ?string $callbackUrl = null;
    private ?string $callbackSecret = null;

    public function __construct(private readonly DocumentsClient $client) {}

    public function html(string $html): self { $this->htmlContent = $html; return $this; }
    public function markdown(string $md): self { $this->markdownContent = $md; return $this; }
    public function template(string $name): self { $this->templateName = $name; return $this; }

    public function templateFile(string $path): self
    {
        $this->templateBase64 = FileUtils::toBase64($path);
        return $this;
    }

    public function field(string $key, string $value): self { $this->fields[$key] = $value; return $this; }

    /** @param array<string, string> $fields */
    public function fields(array $fields): self { $this->fields = array_merge($this->fields, $fields); return $this; }

    public function bookmark(string $key, string $value): self { $this->bookmarks[$key] = $value; return $this; }
    public function image(string $bookmarkName, string $pathOrBase64, ?int $width = null, ?int $height = null): self
    {
        $this->images[] = new ImageData($bookmarkName, FileUtils::toBase64($pathOrBase64), $width, $height);
        return $this;
    }

    public function qrCode(string $bookmarkName, string $content, ?int $size = null): self
    {
        $this->qrCodes[] = new QrCodeData($bookmarkName, $content, $size);
        return $this;
    }

    public function table(string $bookmarkName, TableData $table): self
    {
        $this->tables[$bookmarkName] = $table;
        return $this;
    }

    public function pageSettings(PageSettings $settings): self { $this->pageSettings = $settings; return $this; }
    public function watermark(string|WatermarkConfig $watermark): self { $this->watermark = $watermark; return $this; }
    public function stationery(StationeryConfig $stationery): self { $this->stationery = $stationery; return $this; }
    public function contentArea(ContentArea $area): self { $this->contentAreas[] = $area; return $this; }
    public function invoice(InvoiceData $data): self { $this->invoiceData = $data; return $this; }
    public function password(string $pw): self { $this->password = $pw; return $this; }
    public function asPdf(): self { $this->outputFormat = OutputFormat::PDF; return $this; }
    public function asDocx(): self { $this->outputFormat = OutputFormat::DOCX; return $this; }
    public function outputFormat(OutputFormat $format): self { $this->outputFormat = $format; return $this; }
    public function callback(string $url, ?string $secret = null): self
    {
        $this->callbackUrl = $url;
        $this->callbackSecret = $secret;
        return $this;
    }

    /** Build the DocumentRequest without sending it. */
    public function build(): DocumentRequest
    {
        return new DocumentRequest(
            htmlContent: $this->htmlContent,
            markdownContent: $this->markdownContent,
            templateName: $this->templateName,
            templateBase64: $this->templateBase64,
            fields: $this->fields ?: null,
            bookmarks: $this->bookmarks ?: null,
            images: $this->images ?: null,
            qrCodes: $this->qrCodes ?: null,
            tables: $this->tables ?: null,
            pageSettings: $this->pageSettings,
            watermark: $this->watermark,
            stationery: $this->stationery,
            contentAreas: $this->contentAreas ?: null,
            invoiceData: $this->invoiceData,
            password: $this->password,
            outputFormat: $this->outputFormat,
            callbackUrl: $this->callbackUrl,
            callbackSecret: $this->callbackSecret,
        );
    }

    /** Generate the document synchronously. Returns raw bytes. */
    public function generate(): string
    {
        return $this->client->generate($this->build());
    }

    /** Generate asynchronously. Returns a JobInfo. */
    public function generateAsync(): \Dokmatiq\DocGen\Model\JobInfo
    {
        return $this->client->generateAsync($this->build());
    }
}
