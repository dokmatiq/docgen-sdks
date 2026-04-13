<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use Dokmatiq\DocGen\DocGen;
use Dokmatiq\DocGen\Model\BankAccount;
use Dokmatiq\DocGen\Model\InvoiceItem;
use Dokmatiq\DocGen\Model\InvoiceUnit;
use Dokmatiq\DocGen\Model\Party;
use Dokmatiq\DocGen\Model\WatermarkConfig;

$dg = new DocGen(getenv('DOCGEN_API_KEY') ?: 'your-api-key');

// ── 1. Simple HTML to PDF ───────────────────────────────────────

$pdf = $dg->htmlToPdf('<h1>Hello, World!</h1><p>Generated with DocGen PHP SDK.</p>');
file_put_contents('hello.pdf', $pdf);
echo "1. Created hello.pdf\n";

// ── 2. Markdown to PDF ──────────────────────────────────────────

$pdf = $dg->markdownToPdf("# Report\n\n- Item A\n- Item B\n- Item C");
file_put_contents('report.pdf', $pdf);
echo "2. Created report.pdf\n";

// ── 3. Fluent builder with fields + watermark ───────────────────

$pdf = $dg->document()
    ->html('<h1>Rechnung {{nr}}</h1><p>Datum: {{datum}}</p>')
    ->field('nr', 'RE-2026-001')
    ->field('datum', '12.04.2026')
    ->watermark('ENTWURF')
    ->asPdf()
    ->generate();
file_put_contents('invoice-draft.pdf', $pdf);
echo "3. Created invoice-draft.pdf\n";

// ── 4. Template with fields ─────────────────────────────────────

// Upload a template first
// $dg->templates->upload('templates/invoice.odt');

$pdf = $dg->document()
    ->template('invoice.odt')
    ->fields([
        'company' => 'ACME GmbH',
        'address' => 'Musterstr. 1, 10115 Berlin',
        'total'   => '1.234,56 €',
    ])
    ->asPdf()
    ->generate();
file_put_contents('from-template.pdf', $pdf);
echo "4. Created from-template.pdf\n";

// ── 5. Watermark with custom styling ────────────────────────────

$pdf = $dg->document()
    ->html('<h1>Confidential Document</h1>')
    ->watermark(new WatermarkConfig(
        text: 'CONFIDENTIAL',
        fontSize: 60,
        opacity: 0.15,
        color: '#FF0000',
    ))
    ->asPdf()
    ->generate();
file_put_contents('confidential.pdf', $pdf);
echo "5. Created confidential.pdf\n";

// ── 6. ZUGFeRD invoice with builder ─────────────────────────────

$invoiceData = $dg->invoice()
    ->number('RE-2026-001')
    ->date('2026-04-12')
    ->seller(new Party('ACME GmbH', 'Musterstr. 1', '10115', 'Berlin'))
    ->buyer(new Party('Kunde AG', 'Kundenweg 5', '20095', 'Hamburg'))
    ->item(new InvoiceItem('Beratung', 120.0, quantity: 8, unit: InvoiceUnit::HOUR))
    ->item(new InvoiceItem('Reisekosten', 350.0))
    ->bank(new BankAccount('DE89370400440532013000'))
    ->paymentTerms('Zahlbar innerhalb 14 Tagen')
    ->build();

$invoicePdf = $dg->document()
    ->html('<h1>Rechnung RE-2026-001</h1>')
    ->invoice($invoiceData)
    ->asPdf()
    ->generate();
file_put_contents('zugferd-invoice.pdf', $invoicePdf);
echo "6. Created zugferd-invoice.pdf\n";

// ── 7. Merge PDFs ───────────────────────────────────────────────

$merged = $dg->mergePdfs(['hello.pdf', 'report.pdf']);
file_put_contents('merged.pdf', $merged);
echo "7. Created merged.pdf\n";

echo "\nDone! All examples completed successfully.\n";
