# Dokmatiq DocGen SDKs

[![CI TypeScript](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-typescript.yml/badge.svg)](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-typescript.yml)
[![CI Python](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-python.yml/badge.svg)](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-python.yml)
[![CI Java](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-java.yml/badge.svg)](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-java.yml)
[![CI .NET](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-dotnet.yml/badge.svg)](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-dotnet.yml)
[![CI PHP](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-php.yml/badge.svg)](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-php.yml)

Official SDKs for the [Dokmatiq DocGen API](https://developer.dokmatiq.com) -- document generation, e-invoicing, Excel workbooks, receipt recognition, and PDF tools in a single API.

Dokmatiq DocGen also includes an MCP server and AI assistant skill for Codex and Claude Code to create PDFs, invoices, e-invoices, ZUGFeRD/XRechnung documents, and documents on company letterhead (Briefpapier/Firmenpapier).

## SDKs

| Language | Package | Install |
|----------|---------|---------|
| **TypeScript** | [`@dokmatiq/docgen`](typescript/) | `npm install @dokmatiq/docgen` |
| **Python** | [`dokmatiq-docgen`](python/) | `pip install dokmatiq-docgen` |
| **Java** | [`com.dokmatiq:docgen-sdk`](java/) | Maven / Gradle |
| **PHP** | [`dokmatiq/docgen-sdk`](php/) | `composer require dokmatiq/docgen-sdk` |
| **C# / .NET** | [`Dokmatiq.DocGen`](dotnet/) | `dotnet add package Dokmatiq.DocGen` |

Also included: [MCP Server](mcp/) for AI assistants (any MCP client — Claude Desktop, Cursor, Continue, Cline, …) and a [Codex / Claude Code plugin and skill](plugin/) (MCP setup plus a triggering `dokmatiq-docgen` skill).

## AI Assistant Install

Use the Dokmatiq DocGen MCP server with Codex, Claude Code, Claude Desktop, Cursor, Continue, Cline, Hermes, or any other MCP-capable client.

### Codex Skill

Install the skill from this repo path:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo dokmatiq/docgen-sdks \
  --path plugin/skills/dokmatiq-docgen
```

Then install and configure the MCP server:

```bash
python3.11 -m pip install --user dokmatiq-docgen-mcp
export DOCGEN_API_KEY="dk_live_xxxxxxxxxxxxx"
```

If `docgen-mcp` is installed into `~/.local/bin`, make sure that directory is on your `PATH`, or configure your MCP client with the absolute command path.

### Claude Code Plugin

```bash
/plugin marketplace add dokmatiq/claude-plugins
/plugin install docgen@dokmatiq
```

The legacy plugin copy in this repository is kept under [`plugin/`](plugin/) for backwards compatibility.

---

## Features

All SDKs provide the same capabilities with idiomatic APIs:

### Document Generation
HTML, Markdown, and ODT templates to PDF, DOCX, or ODT -- with field substitution, images, QR codes, tables, watermarks, and stationery overlays.

### E-Invoicing (ZUGFeRD / XRechnung)
Embed and extract structured invoice data in PDF invoices (EN16931). Generate, parse, validate, and transform XRechnung XML (CII and UBL).

### Excel Workbooks
Create styled XLSX from JSON with formulas, freeze panes, auto-filters, and cell styling. Convert between XLSX, CSV, and JSON. Fill Excel templates.

### Receipt Recognition (AI-Powered)
Extract structured data from receipt and invoice images:

- **Vendor, date, totals** (gross / net / VAT per rate)
- **Line items** with quantity, unit price, and total
- **SKR03/04 account mapping** for German bookkeeping
- **Multi-currency support** with exchange rates
- **DATEV-compatible CSV export**
- **Confidence score** for extraction quality
- **Async processing** for large batches

```typescript
const result = await dg.receipts.extract("receipt.jpg");
// { vendor, date, total: { gross, net, vat }, skr03Account, lineItems, confidence, ... }

const csv = await dg.receipts.exportDatev([result]);
```

### PDF Operations
Merge, split, rotate, extract text, read/write metadata, convert to PDF/A.

### Digital Signatures
Sign PDFs with PKCS#12 certificates. Verify existing signatures.

### PDF Forms
Inspect and fill PDF form fields programmatically.

### Preview
Render PDF pages as PNG images for thumbnails and previews.

### Async Processing
Submit long-running jobs with polling or webhook callbacks.

---

## Quick Start

```bash
# 1. Get an API key at https://developer.dokmatiq.com
# 2. Install your SDK of choice

npm install @dokmatiq/docgen          # TypeScript
pip install dokmatiq-docgen           # Python
composer require dokmatiq/docgen-sdk  # PHP
dotnet add package Dokmatiq.DocGen    # .NET
# Maven: com.dokmatiq:docgen-sdk     # Java
```

```typescript
import { DocGen } from "@dokmatiq/docgen";

const dg = new DocGen({ apiKey: "your-api-key" });

// Generate a PDF
const pdf = await dg.htmlToPdf("<h1>Hello World</h1>");

// Build a complex document
const doc = await dg.document()
  .html("<h1>Invoice {{nr}}</h1>")
  .field("nr", "RE-2026-001")
  .watermark("DRAFT")
  .asPdf()
  .generate();

// Extract receipt data
const receipt = await dg.receipts.extract("receipt.jpg");

// Create an Excel workbook
const xlsx = await dg.excel.generate({
  sheets: [{ name: "Report", columns: [...], rows: [...] }]
});
```

---

## Documentation

- [Developer Portal](https://developer.dokmatiq.com) -- Sign up, API keys, usage dashboard
- [API Reference](https://docs.dokmatiq.com) -- Full REST API docs
- [Website](https://dokmatiq.com) -- Product overview

Each SDK has its own detailed README with full examples:
[TypeScript](typescript/) | [Python](python/) | [Java](java/) | [PHP](php/) | [.NET](dotnet/)

---

## License

[MIT](LICENSE) -- Copyright 2026 Dokmatiq
