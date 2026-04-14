# Dokmatiq DocGen MCP Server

MCP (Model Context Protocol) server that exposes the [Dokmatiq DocGen](https://dokmatiq.com) document generation API as tools for AI assistants like Claude.

## Setup

### Prerequisites

- Python 3.10+
- DocGen API key

### Installation

```bash
pip install dokmatiq-docgen-mcp
```

Or install from source:

```bash
cd mcp
pip install -e .
```

### Configuration

Set your API key as an environment variable:

```bash
export DOCGEN_API_KEY=dk_live_xxx
```

Optionally override the base URL:

```bash
export DOCGEN_BASE_URL=https://custom.api.endpoint.com
```

## Usage with Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "docgen": {
      "command": "docgen-mcp",
      "env": {
        "DOCGEN_API_KEY": "dk_live_xxx"
      }
    }
  }
}
```

Or using `uvx`:

```json
{
  "mcpServers": {
    "docgen": {
      "command": "uvx",
      "args": ["dokmatiq-docgen-mcp"],
      "env": {
        "DOCGEN_API_KEY": "dk_live_xxx"
      }
    }
  }
}
```

## Usage with Claude Code

```bash
claude mcp add docgen -- docgen-mcp
```

Set the API key in your environment or `.env` file.

## Available Tools

### Document Generation

| Tool | Description |
|------|-------------|
| `generate_pdf_from_html` | Convert HTML to PDF |
| `generate_pdf_from_markdown` | Convert Markdown to PDF |
| `generate_document` | Generate with template, fields, watermark, output format |
| `compose_document` | Compose multi-part document from sections |
| `create_invoice` | Create ZUGFeRD-compliant invoice PDF |

### PDF Tools

| Tool | Description |
|------|-------------|
| `merge_pdfs` | Merge multiple PDFs into one |
| `extract_text_from_pdf` | Extract all text content |
| `get_pdf_metadata` | Get title, author, page count |
| `convert_to_pdfa` | Convert to PDF/A archival format |
| `rotate_pdf` | Rotate pages |

### PDF Forms

| Tool | Description |
|------|-------------|
| `inspect_pdf_form` | List form fields with types and values |
| `fill_pdf_form` | Fill form fields |

### Digital Signatures

| Tool | Description |
|------|-------------|
| `sign_pdf` | Digitally sign with PKCS#12 certificate |
| `verify_pdf_signatures` | Verify existing signatures |
| `list_certificates` | List uploaded certificates |

### Templates & Fonts

| Tool | Description |
|------|-------------|
| `list_templates` | List uploaded templates |
| `upload_template` | Upload ODT/DOCX template |
| `delete_template` | Delete a template |
| `list_fonts` | List uploaded fonts |

### Preview

| Tool | Description |
|------|-------------|
| `preview_pdf_page` | Render page as PNG image |
| `get_pdf_page_count` | Get total page count |

### E-Invoicing

| Tool | Description |
|------|-------------|
| `validate_zugferd` | Validate ZUGFeRD compliance |
| `extract_zugferd` | Extract invoice data from ZUGFeRD PDF |
| `validate_xrechnung` | Validate XRechnung XML |
| `parse_xrechnung` | Parse XRechnung into structured data |
| `detect_xrechnung` | Detect XRechnung format |

### Receipt Recognition (AI-Powered)

| Tool | Description |
|------|-------------|
| `extract_receipt` | Extract structured data from receipt image (vendor, totals, VAT, line items, SKR03/04 account) |
| `extract_receipt_async` | Submit receipt for async extraction with optional webhook |
| `get_receipt_job` | Check async extraction job status |
| `get_receipt_job_result` | Get extraction result of completed job |
| `list_receipt_jobs` | List all async receipt jobs |
| `receipt_to_document` | Extract receipt and generate expense report (PDF/DOCX/ODT) |
| `export_receipts_csv` | Export receipts as DATEV-compatible CSV |
| `export_receipts_xlsx` | Export receipts as Excel workbook |

## Example Prompts

Once connected, you can ask Claude:

- "Generate a PDF from this HTML: `<h1>Hello World</h1>`"
- "Create an invoice for ACME GmbH to Kunde AG for 8 hours of consulting at 120€/hour"
- "Merge these two PDFs together"
- "Extract the text from this PDF"
- "Fill the form fields name=Max and date=12.04.2026 in this PDF"
- "Extract the data from this receipt image -- I need vendor, total, and VAT breakdown"
- "Analyze these receipts and export them as a DATEV CSV"
- "Turn this receipt photo into an expense report PDF"

## License

MIT
