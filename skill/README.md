# DocGen Claude Code Skill

A Claude Code skill that provides document generation capabilities via the DocGen MCP server.

## Setup

1. Install the MCP server:

```bash
pip install dokmatiq-docgen-mcp
```

2. Add the MCP server to Claude Code:

```bash
claude mcp add docgen -- docgen-mcp
```

3. Set your API key:

```bash
export DOCGEN_API_KEY=dk_live_xxx
```

4. Add the skill to your project:

Copy `SKILL.md` into your project's `.claude/skills/` directory, or reference it from your `CLAUDE.md`.

## What it enables

With this skill active, Claude Code can:

- Generate PDFs from HTML or Markdown
- Use document templates with field replacement
- Create ZUGFeRD-compliant e-invoices
- Validate, parse, and transform XRechnung XML
- Merge, split, and manipulate PDFs
- Fill PDF forms
- Digitally sign documents
- Preview PDF pages as images
- Generate styled Excel workbooks from JSON, CSV, or templates
- Convert between Excel, CSV, and JSON formats
- Extract structured data from receipt and invoice images (AI-powered)
- Map receipts to SKR03/04 accounts with DATEV-compatible export

## License

MIT
