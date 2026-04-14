<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen;

use Dokmatiq\DocGen\Builder\ComposeBuilder;
use Dokmatiq\DocGen\Builder\DocumentBuilder;
use Dokmatiq\DocGen\Builder\InvoiceBuilder;
use Dokmatiq\DocGen\Client\DocumentsClient;
use Dokmatiq\DocGen\Client\FontsClient;
use Dokmatiq\DocGen\Client\PdfFormsClient;
use Dokmatiq\DocGen\Client\PdfToolsClient;
use Dokmatiq\DocGen\Client\PreviewClient;
use Dokmatiq\DocGen\Client\SignaturesClient;
use Dokmatiq\DocGen\Client\TemplatesClient;
use Dokmatiq\DocGen\Client\ExcelClient;
use Dokmatiq\DocGen\Client\ReceiptsClient;
use Dokmatiq\DocGen\Client\XRechnungClient;
use Dokmatiq\DocGen\Client\ZugferdClient;
use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;
use Dokmatiq\DocGen\Model\DocumentRequest;
use Dokmatiq\DocGen\Model\OutputFormat;

/**
 * DocGen PHP SDK – main client.
 *
 * Usage:
 *   $dg = new DocGen('your-api-key');
 *
 *   // Fluent builder
 *   $pdf = $dg->document()
 *       ->html('<h1>Hello {{name}}</h1>')
 *       ->field('name', 'World')
 *       ->asPdf()
 *       ->generate();
 *
 *   // Convenience
 *   $pdf = $dg->htmlToPdf('<h1>Hello</h1>');
 *
 *   // Sub-clients
 *   $dg->templates()->upload('invoice.odt');
 *   $dg->pdfTools()->merge(['a.pdf', 'b.pdf']);
 */
final class DocGen
{
    private readonly Transport $transport;

    public readonly DocumentsClient $documents;
    public readonly TemplatesClient $templates;
    public readonly FontsClient $fonts;
    public readonly PdfFormsClient $pdfForms;
    public readonly SignaturesClient $signatures;
    public readonly PdfToolsClient $pdfTools;
    public readonly PreviewClient $preview;
    public readonly ZugferdClient $zugferd;
    public readonly XRechnungClient $xrechnung;
    public readonly ExcelClient $excel;
    public readonly ReceiptsClient $receipts;

    public function __construct(
        string $apiKey,
        string $baseUrl = 'https://api.dokmatiq.com',
        int $timeout = 120,
        int $maxRetries = 3,
    ) {
        $config = new DocGenConfig($apiKey, $baseUrl, $timeout, $maxRetries);
        $this->transport = new Transport($config);

        $this->documents  = new DocumentsClient($this->transport);
        $this->templates  = new TemplatesClient($this->transport);
        $this->fonts      = new FontsClient($this->transport);
        $this->pdfForms   = new PdfFormsClient($this->transport);
        $this->signatures = new SignaturesClient($this->transport);
        $this->pdfTools   = new PdfToolsClient($this->transport);
        $this->preview    = new PreviewClient($this->transport);
        $this->zugferd    = new ZugferdClient($this->transport);
        $this->xrechnung  = new XRechnungClient($this->transport);
        $this->excel      = new ExcelClient($this->transport);
        $this->receipts   = new ReceiptsClient($this->transport);
    }

    /** Alternative constructor from config object. */
    public static function fromConfig(DocGenConfig $config): self
    {
        $instance = new self($config->apiKey, $config->baseUrl, $config->timeout, $config->maxRetries);
        return $instance;
    }

    // ── Fluent Builders ─────────────────────────────────────────────

    /** Start building a document request. */
    public function document(): DocumentBuilder
    {
        return new DocumentBuilder($this->documents);
    }

    /** Start building a compose (multi-part) request. */
    public function compose(): ComposeBuilder
    {
        return new ComposeBuilder($this->documents);
    }

    /** Start building invoice data. */
    public function invoice(): InvoiceBuilder
    {
        return new InvoiceBuilder();
    }

    // ── Convenience Methods ─────────────────────────────────────────

    /** Convert HTML to PDF. */
    public function htmlToPdf(string $html): string
    {
        return $this->document()->html($html)->asPdf()->generate();
    }

    /** Convert Markdown to PDF. */
    public function markdownToPdf(string $markdown): string
    {
        return $this->document()->markdown($markdown)->asPdf()->generate();
    }

    /**
     * Merge multiple PDFs.
     *
     * @param string[] $pdfPaths
     */
    public function mergePdfs(array $pdfPaths): string
    {
        return $this->pdfTools->merge($pdfPaths);
    }

    /** Sign a PDF with a certificate. */
    public function signPdf(string $pdfPath, string $certAlias, ?string $reason = null): string
    {
        return $this->signatures->sign($pdfPath, $certAlias, $reason);
    }
}
