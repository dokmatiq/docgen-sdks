# DocGen PHP SDK

Official PHP SDK for the [Dokmatiq DocGen](https://dokmatiq.com) document generation API.

## Requirements

- PHP 8.1+
- ext-curl
- ext-json

## Installation

```bash
composer require dokmatiq/docgen-sdk
```

## Quick Start

```php
use Dokmatiq\DocGen\DocGen;

$dg = new DocGen('your-api-key');

// HTML to PDF
$pdf = $dg->htmlToPdf('<h1>Hello, World!</h1>');
file_put_contents('hello.pdf', $pdf);

// Markdown to PDF
$pdf = $dg->markdownToPdf('# Report\n\nGenerated with DocGen.');
file_put_contents('report.pdf', $pdf);
```

## Fluent Builder API

```php
use Dokmatiq\DocGen\Model\WatermarkConfig;

$pdf = $dg->document()
    ->html('<h1>Rechnung {{nr}}</h1>')
    ->template('invoice.odt')
    ->field('nr', 'RE-2026-001')
    ->field('datum', '12.04.2026')
    ->watermark('ENTWURF')
    ->asPdf()
    ->generate();
```

### With images, QR codes, and tables

```php
use Dokmatiq\DocGen\Model\ColumnDef;
use Dokmatiq\DocGen\Model\TableData;

$pdf = $dg->document()
    ->html('<h1>Order {{nr}}</h1>')
    ->field('nr', 'B-001')
    ->image('logo', 'logo.png', width: 200)
    ->qrCode('payment', 'BCD\n002\n1\nSCT\n...', size: 150)
    ->table('items', new TableData(
        columns: [new ColumnDef('Artikel', 80), new ColumnDef('Preis', 30)],
        rows: [['Widget', '9.99'], ['Gadget', '24.99']],
    ))
    ->asPdf()
    ->generate();
```

### Watermark with styling

```php
$pdf = $dg->document()
    ->html('<h1>Draft</h1>')
    ->watermark(new WatermarkConfig(
        text: 'CONFIDENTIAL',
        fontSize: 60,
        opacity: 0.15,
        color: '#FF0000',
    ))
    ->asPdf()
    ->generate();
```

## Sub-Clients

All API endpoints are accessible through typed sub-clients:

```php
// Templates
$dg->templates->upload('invoice.odt');
$dg->templates->list();
$dg->templates->delete('invoice.odt');

// Fonts
$dg->fonts->upload('custom-font.ttf');

// PDF Forms
$fields = $dg->pdfForms->inspectFields('form.pdf');
$filled = $dg->pdfForms->fillForm('form.pdf', ['name' => 'John Doe']);

// Digital Signatures
$dg->signatures->uploadCert('cert.p12', 'password', 'my-cert');
$signed = $dg->signatures->sign('document.pdf', 'my-cert', reason: 'Approved');
$result = $dg->signatures->verify('signed.pdf');

// PDF Tools
$merged = $dg->pdfTools->merge(['a.pdf', 'b.pdf']);
$parts  = $dg->pdfTools->split('document.pdf', ['1-3', '4-6']);
$text   = $dg->pdfTools->extractText('document.pdf');
$pdfa   = $dg->pdfTools->toPdfA('document.pdf');

// Preview
$png   = $dg->preview->previewPage('document.pdf', page: 1, dpi: 300);
$pages = $dg->preview->previewPages('document.pdf', maxPages: 5);
$count = $dg->preview->pageCount('document.pdf');

// ZUGFeRD
$zugferd  = $dg->zugferd->embed('invoice.pdf', $invoiceData);
$extracted = $dg->zugferd->extract('zugferd.pdf');
$valid    = $dg->zugferd->validate('zugferd.pdf');

// XRechnung
$xml = $dg->xrechnung->generate($invoiceData);
$parsed = $dg->xrechnung->parse($xml);
$valid  = $dg->xrechnung->validate($xml);
```

## Invoice Builder (ZUGFeRD / XRechnung)

```php
use Dokmatiq\DocGen\Model\BankAccount;
use Dokmatiq\DocGen\Model\InvoiceItem;
use Dokmatiq\DocGen\Model\InvoiceUnit;
use Dokmatiq\DocGen\Model\Party;

$invoice = $dg->invoice()
    ->number('RE-2026-001')
    ->date('2026-04-12')
    ->seller(new Party('ACME GmbH', 'Musterstr. 1', '10115', 'Berlin'))
    ->buyer(new Party('Kunde AG', 'Kundenweg 5', '20095', 'Hamburg'))
    ->item(new InvoiceItem('Beratung', 120.0, quantity: 8, unit: InvoiceUnit::HOUR))
    ->item(new InvoiceItem('Reisekosten', 350.0))
    ->bank(new BankAccount('DE89370400440532013000'))
    ->paymentTerms('Zahlbar innerhalb 14 Tagen')
    ->build();

// Embed in PDF
$zugferdPdf = $dg->zugferd->embed('invoice.pdf', $invoice);

// Or generate XRechnung XML
$xml = $dg->xrechnung->generate($invoice);
```

## Multi-Part Documents (Compose)

```php
$pdf = $dg->compose()
    ->htmlPart('<h1>Cover Page</h1>')
    ->htmlPart('<h2>Chapter 1</h2><p>Content...</p>')
    ->markdownPart('## Chapter 2\n\nMore content...')
    ->watermark('DRAFT')
    ->asPdf()
    ->generate();
```

## Async Generation

```php
$job = $dg->document()
    ->html('<h1>Large Report</h1>')
    ->asPdf()
    ->generateAsync();

echo "Job started: {$job->jobId}\n";

// Poll until complete
$pdf = $dg->documents->waitForJob($job->jobId, pollInterval: 2.0, timeout: 300.0);
file_put_contents('report.pdf', $pdf);
```

## Webhook Verification

```php
use Dokmatiq\DocGen\Webhook\WebhookVerifier;

$verifier = new WebhookVerifier('your-webhook-secret');

// In your webhook handler:
$body = file_get_contents('php://input');
$signature = $_SERVER['HTTP_X_DOCGEN_SIGNATURE'] ?? '';

$payload = $verifier->verify($body, $signature);
echo "Job {$payload->jobId} completed with status: {$payload->status}\n";
```

## Error Handling

```php
use Dokmatiq\DocGen\Exception\ValidationException;
use Dokmatiq\DocGen\Exception\AuthenticationException;
use Dokmatiq\DocGen\Exception\RateLimitException;

try {
    $pdf = $dg->htmlToPdf('<h1>Test</h1>');
} catch (ValidationException $e) {
    echo "Validation: {$e->getMessage()}\n";
    print_r($e->fieldErrors);     // Field-level errors
    echo $e->hint . "\n";         // Suggestion
} catch (AuthenticationException $e) {
    echo "Auth failed: {$e->getMessage()}\n";
} catch (RateLimitException $e) {
    echo "Rate limited. Retry after: {$e->retryAfter}s\n";
}
```

## Configuration

```php
$dg = new DocGen(
    apiKey: 'your-api-key',
    baseUrl: 'https://api.dokmatiq.com',  // Custom base URL
    timeout: 120,                          // Request timeout in seconds
    maxRetries: 3,                         // Max retry attempts
);
```

## File Input

All methods that accept PDF/file input support both file paths and raw bytes:

```php
// File path
$text = $dg->pdfTools->extractText('/path/to/document.pdf');

// Raw bytes (e.g. from upload)
$text = $dg->pdfTools->extractText($uploadedFileContent);
```

## License

See [LICENSE](../LICENSE) for details.
