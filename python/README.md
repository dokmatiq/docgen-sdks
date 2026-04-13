# Dokmatiq DocGen Python SDK

Python SDK for the [Dokmatiq DocGen](https://dokmatiq.com) document generation API. Generate PDF, DOCX, and ODT documents from HTML/Markdown with templates, e-invoicing (ZUGFeRD/XRechnung), digital signatures, and more.

## Installation

```bash
pip install dokmatiq-docgen
```

## Quick Start

```python
from docgen import DocGen

dg = DocGen(api_key="dk_live_xxx")

# One-liner: HTML to PDF
pdf = dg.html_to_pdf("<h1>Hello World</h1>")

# Markdown to PDF
pdf = dg.markdown_to_pdf("# Report\n\n**Summary**: ...")
```

## Builder Pattern

For complex documents, use the fluent builder:

```python
from docgen import DocGen, ColumnDef, TableData, TextAlignment

with DocGen(api_key="dk_live_xxx") as dg:
    pdf = (dg.document()
        .html("<h1>Rechnung {{nr}}</h1>")
        .template("invoice.odt")
        .field("nr", "RE-2026-001")
        .field("datum", "12.04.2026")
        .table("positionen", TableData(
            columns=[
                ColumnDef("Artikel", width=80),
                ColumnDef("Preis", width=30, alignment=TextAlignment.RIGHT),
            ],
            rows=[["Widget", "9.99 €"], ["Gadget", "24.99 €"]],
        ))
        .qr_code("payment", "BCD\n002\n1\nSCT\n...")
        .watermark("ENTWURF")
        .as_pdf()
        .generate())
```

## E-Invoicing (ZUGFeRD / XRechnung)

```python
from docgen import DocGen, InvoiceUnit

with DocGen(api_key="dk_live_xxx") as dg:
    invoice = (dg.invoice()
        .number("RE-2026-001")
        .date("2026-04-12")
        .seller(name="ACME GmbH", street="Musterstr. 1", zip="10115", city="Berlin", vat_id="DE123456789")
        .buyer(name="Kunde AG", street="Kundenweg 5", zip="20095", city="Hamburg")
        .item("Beratung", quantity=8, unit=InvoiceUnit.HOUR, unit_price=120.0)
        .item("Reisekosten", unit_price=250.0)
        .bank(iban="DE89370400440532013000", bic="COBADEFFXXX", holder="ACME GmbH")
        .payment_terms("Zahlbar innerhalb 14 Tagen")
        .build())

    pdf = (dg.document()
        .html("<h1>Rechnung RE-2026-001</h1>")
        .template("invoice.odt")
        .invoice(invoice)
        .as_pdf()
        .generate())
```

## PDF Operations

```python
from pathlib import Path
from docgen import DocGen

with DocGen(api_key="dk_live_xxx") as dg:
    # Merge PDFs
    merged = dg.merge_pdfs([Path("part1.pdf"), Path("part2.pdf")])

    # Fill form fields
    filled = dg.fill_form(Path("form.pdf"), {"name": "Max", "date": "12.04.2026"})

    # Sign PDF
    signed = dg.sign_pdf(Path("doc.pdf"), "my-cert.p12", "password123")

    # Extract text
    text = dg.pdf_tools.extract_text(Path("document.pdf"))

    # Preview page as image
    png = dg.preview.preview_page(Path("document.pdf"), page=1, dpi=300)
```

## Async Support

```python
import asyncio
from docgen import AsyncDocGen

async def main():
    async with AsyncDocGen(api_key="dk_live_xxx") as dg:
        # Parallel generation
        pdfs = await asyncio.gather(
            dg.html_to_pdf("<h1>Doc A</h1>"),
            dg.html_to_pdf("<h1>Doc B</h1>"),
        )

asyncio.run(main())
```

## Async Jobs

```python
with DocGen(api_key="dk_live_xxx") as dg:
    # Submit async job
    job = dg.documents.generate_async(request)

    # Poll until complete (with timeout)
    pdf = dg.documents.wait_for_job(job.job_id, poll_interval=2.0, timeout=120.0)
```

## Configuration

```python
from docgen import DocGen, RetryPolicy

dg = DocGen(
    api_key="dk_live_xxx",
    base_url="https://api.dokmatiq.com",
    timeout=60.0,
    retry=RetryPolicy(
        max_retries=5,
        initial_delay=1.0,
        backoff_multiplier=2.0,
    ),
    validate_mode="strict",  # "strict" | "warn" | None
)
```

## Error Handling

```python
from docgen import DocGen, ValidationError, RateLimitError, AuthenticationError

try:
    pdf = dg.html_to_pdf("<h1>Hello</h1>")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Validation failed: {e}")
    print(f"Field errors: {e.field_errors}")
    print(f"Hint: {e.hint}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
```

## Webhook Verification

```python
from docgen import verify_webhook

# In your webhook handler:
payload = verify_webhook(request.body, request.headers["X-DocGen-Signature"], secret)
print(f"Job {payload.job_id} completed: {payload.status}")
```

## Sub-Clients

| Client | Access | Description |
|--------|--------|-------------|
| `dg.documents` | Document generation, compose, async jobs |
| `dg.templates` | Template upload, list, delete |
| `dg.fonts` | Font upload, list, delete |
| `dg.pdf_forms` | Form field inspection and filling |
| `dg.signatures` | Certificate management, sign, verify |
| `dg.pdf_tools` | Merge, split, metadata, PDF/A, rotate |
| `dg.preview` | Page rendering as images |
| `dg.zugferd` | ZUGFeRD embed, extract, validate |
| `dg.xrechnung` | XRechnung generate, parse, validate, transform |

## Requirements

- Python 3.10+
- httpx >= 0.27

## License

MIT
