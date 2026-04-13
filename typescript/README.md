# Dokmatiq DocGen TypeScript SDK

TypeScript/Node.js SDK for the [Dokmatiq DocGen](https://dokmatiq.com) document generation API. Generate PDF, DOCX, and ODT documents from HTML/Markdown with templates, e-invoicing (ZUGFeRD/XRechnung), digital signatures, and more.

## Installation

```bash
npm install @dokmatiq/docgen
```

## Quick Start

```typescript
import { DocGen } from '@dokmatiq/docgen';

const dg = new DocGen({ apiKey: 'dk_live_xxx' });

// One-liner: HTML to PDF
const pdf = await dg.htmlToPdf('<h1>Hello World</h1>');

// Markdown to PDF
const report = await dg.markdownToPdf('# Report\n\n**Summary**: ...');
```

## Builder Pattern

For complex documents, use the fluent builder:

```typescript
import { DocGen, TextAlignment, type ColumnDef, type TableData } from '@dokmatiq/docgen';

const dg = new DocGen({ apiKey: 'dk_live_xxx' });

const pdf = await dg.document()
  .html('<h1>Rechnung {{nr}}</h1>')
  .template('invoice.odt')
  .field('nr', 'RE-2026-001')
  .field('datum', '12.04.2026')
  .table('positionen', {
    columns: [
      { header: 'Artikel', width: 80 },
      { header: 'Preis', width: 30, alignment: TextAlignment.RIGHT },
    ],
    rows: [['Widget', '9.99 €'], ['Gadget', '24.99 €']],
  })
  .qrCode('payment', 'BCD\n002\n1\nSCT\n...')
  .watermark('ENTWURF')
  .asPdf()
  .generate();
```

## E-Invoicing (ZUGFeRD / XRechnung)

```typescript
import { DocGen, InvoiceUnit } from '@dokmatiq/docgen';

const dg = new DocGen({ apiKey: 'dk_live_xxx' });

const invoice = dg.invoice()
  .number('RE-2026-001')
  .date('2026-04-12')
  .seller({ name: 'ACME GmbH', street: 'Musterstr. 1', zip: '10115', city: 'Berlin', vatId: 'DE123456789' })
  .buyer({ name: 'Kunde AG', street: 'Kundenweg 5', zip: '20095', city: 'Hamburg' })
  .item({ description: 'Beratung', quantity: 8, unit: InvoiceUnit.HOUR, unitPrice: 120.0 })
  .item({ description: 'Reisekosten', unitPrice: 250.0 })
  .bank({ iban: 'DE89370400440532013000', bic: 'COBADEFFXXX', accountHolder: 'ACME GmbH' })
  .paymentTerms('Zahlbar innerhalb 14 Tagen')
  .build();

const pdf = await dg.document()
  .html('<h1>Rechnung RE-2026-001</h1>')
  .template('invoice.odt')
  .invoice(invoice)
  .asPdf()
  .generate();
```

## PDF Operations

```typescript
import { DocGen } from '@dokmatiq/docgen';

const dg = new DocGen({ apiKey: 'dk_live_xxx' });

// Merge PDFs
const merged = await dg.mergePdfs(['part1.pdf', 'part2.pdf']);

// Fill form fields
const filled = await dg.fillForm('form.pdf', { name: 'Max', date: '12.04.2026' });

// Sign PDF
const signed = await dg.signPdf('doc.pdf', 'my-cert.p12', 'password123');

// Extract text
const text = await dg.pdfTools.extractText('document.pdf');

// Preview page as image
const png = await dg.preview.previewPage('document.pdf', 1, 300);
```

## Parallel Generation

```typescript
const [pdfA, pdfB] = await Promise.all([
  dg.htmlToPdf('<h1>Doc A</h1>'),
  dg.htmlToPdf('<h1>Doc B</h1>'),
]);
```

## Async Jobs

```typescript
const job = await dg.documents.generateAsync(request);
const pdf = await dg.documents.waitForJob(job.jobId, 2000, 120_000);
```

## Configuration

```typescript
import { DocGen } from '@dokmatiq/docgen';

const dg = new DocGen({
  apiKey: 'dk_live_xxx',
  baseUrl: 'https://api.dokmatiq.com',
  timeout: 60_000,
  retry: {
    maxRetries: 5,
    initialDelay: 1000,
    backoffMultiplier: 2.0,
  },
  validateMode: 'strict',  // 'strict' | 'warn' | undefined
});
```

## Error Handling

```typescript
import { DocGen, ValidationError, RateLimitError, AuthenticationError } from '@dokmatiq/docgen';

try {
  const pdf = await dg.htmlToPdf('<h1>Hello</h1>');
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.log('Invalid API key');
  } else if (error instanceof ValidationError) {
    console.log(`Validation failed: ${error.message}`);
    console.log(`Field errors:`, error.fieldErrors);
    console.log(`Hint: ${error.hint}`);
  } else if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after ${error.retryAfter}s`);
  }
}
```

## Webhook Verification

```typescript
import { verifyWebhook } from '@dokmatiq/docgen';

// In your webhook handler:
const payload = verifyWebhook(req.body, req.headers['x-docgen-signature'], secret);
console.log(`Job ${payload.jobId} completed: ${payload.status}`);
```

## Sub-Clients

| Client | Access | Description |
|--------|--------|-------------|
| `dg.documents` | Document generation, compose, async jobs |
| `dg.templates` | Template upload, list, delete |
| `dg.fonts` | Font upload, list, delete |
| `dg.pdfForms` | Form field inspection and filling |
| `dg.signatures` | Certificate management, sign, verify |
| `dg.pdfTools` | Merge, split, metadata, PDF/A, rotate |
| `dg.preview` | Page rendering as images |
| `dg.zugferd` | ZUGFeRD embed, extract, validate |
| `dg.xrechnung` | XRechnung generate, parse, validate, transform |

## Requirements

- Node.js 18+
- TypeScript 5.0+ (for type definitions)

## License

MIT
