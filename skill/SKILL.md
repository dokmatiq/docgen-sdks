# DocGen – Document Generation Skill

Generate professional PDF, DOCX, and ODT documents from HTML/Markdown with templates, tables, QR codes, e-invoicing (ZUGFeRD/XRechnung), digital signatures, and more.

## Prerequisites

This skill requires the DocGen MCP server to be connected. Add it to your Claude Code configuration:

```bash
claude mcp add docgen -- docgen-mcp
```

Set the `DOCGEN_API_KEY` environment variable with your API key.

## Capabilities

### Document Generation

**Simple conversion:**
- `generate_pdf_from_html` – Convert HTML to PDF
- `generate_pdf_from_markdown` – Convert Markdown to PDF

**Advanced generation:**
- `generate_document` – Generate with template, field replacements, watermark, and output format selection
- `compose_document` – Compose a multi-part document from multiple sections (cover page, chapters, appendix)

### E-Invoicing (ZUGFeRD / XRechnung)

- `create_invoice` – Create a complete, ZUGFeRD-compliant invoice PDF with structured e-invoicing data embedded. Supports seller/buyer parties, line items with units (hours, pieces, kg, etc.), bank details, payment terms, and VAT calculation.

### PDF Tools

- `merge_pdfs` – Merge multiple PDFs into a single file
- `extract_text_from_pdf` – Extract all text content from a PDF
- `get_pdf_metadata` – Get title, author, page count, and other metadata
- `convert_to_pdfa` – Convert to PDF/A archival format
- `rotate_pdf` – Rotate pages by 90°, 180°, or 270°

### PDF Forms

- `inspect_pdf_form` – List all form fields with their types, values, and options
- `fill_pdf_form` – Fill form fields and optionally flatten (lock) them

### Digital Signatures

- `sign_pdf` – Digitally sign a PDF with a PKCS#12 certificate
- `verify_pdf_signatures` – Check if a PDF is signed and validate all signatures
- `list_certificates` – List available signing certificates

### Templates & Fonts

- `list_templates` – List all uploaded document templates
- `upload_template` – Upload an ODT/DOCX template for use in generation
- `delete_template` – Remove a template
- `list_fonts` – List uploaded custom fonts

### Preview

- `preview_pdf_page` – Render a PDF page as a PNG image
- `get_pdf_page_count` – Get total number of pages

### E-Invoice Validation

- `validate_zugferd` – Validate ZUGFeRD/Factur-X PDF compliance
- `extract_zugferd` – Extract structured invoice data from a ZUGFeRD PDF
- `validate_xrechnung` – Validate XRechnung XML
- `parse_xrechnung` – Parse XRechnung XML into structured data
- `detect_xrechnung` – Detect if XML is an XRechnung and identify format

## Usage Patterns

### Quick document generation

"Generate a PDF from this HTML: `<h1>Project Report</h1><p>Summary of findings...</p>`"

### Invoice creation

"Create an invoice from ACME GmbH (Musterstr. 1, 10115 Berlin, VAT DE123456789) to Kunde AG (Kundenweg 5, 20095 Hamburg) for:
- 8 hours consulting at 120€/hour
- Travel expenses 250€ flat
Payment to IBAN DE89370400440532013000, due in 14 days."

### Document with template

"Generate a document using the 'report.odt' template with fields: title=Quarterly Report, author=Max Mustermann, date=12.04.2026, and add a DRAFT watermark."

### Multi-part composition

"Create a multi-part document with a cover page, two chapters using the 'report-template.odt' template, and a CONFIDENTIAL watermark."

### PDF operations

"Merge part1.pdf and part2.pdf into one document."
"Extract all text from this PDF."
"Fill the form fields name=Max Mustermann and date=12.04.2026 in this PDF form."

## Notes

- All file inputs/outputs use base64 encoding for binary data
- Templates must be uploaded before they can be referenced by name
- Invoices automatically embed ZUGFeRD XML for e-invoicing compliance
- Digital signatures require pre-uploaded PKCS#12 certificates
- Unit codes follow UN/ECE Recommendation 20: C62=piece, HUR=hour, DAY=day, KGM=kg
