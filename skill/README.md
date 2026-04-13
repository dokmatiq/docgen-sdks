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
- Merge, split, and manipulate PDFs
- Fill PDF forms
- Digitally sign documents
- Preview PDF pages as images

## License

MIT
