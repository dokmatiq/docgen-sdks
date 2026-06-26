# Dokmatiq DocGen — Codex & Claude Code Plugin

> **Moved.** This plugin now lives at [github.com/dokmatiq/claude-plugins](https://github.com/dokmatiq/claude-plugins). Install with:
> ```
> /plugin marketplace add dokmatiq/claude-plugins
> /plugin install docgen@dokmatiq
> ```
> The copy in this folder is kept for backward compatibility and will be removed in a future release.

Install the Dokmatiq DocGen MCP server (40 tools) plus a triggering `dokmatiq-docgen` skill that tells Codex, Claude Code, and other MCP-enabled assistants when to use it.

Use this when you want an AI assistant to create PDFs, invoices, e-invoices, ZUGFeRD/XRechnung files, Excel workbooks, receipt exports, or documents on company letterhead (Briefpapier/Firmenpapier).

## What's inside

- **MCP server** auto-configured: 40 tools covering PDF generation, e-invoicing (ZUGFeRD/XRechnung), Excel workbooks, digital signatures, PDF operations, AI-powered receipt recognition
- **Skill** with detailed trigger description so the assistant reaches for these tools when relevant — without you having to spell it out each time

## Prerequisites

1. **Python 3.11+** with the MCP server installable:
   ```bash
   python3.11 -m pip install --user dokmatiq-docgen-mcp
   ```
2. **Dokmatiq API key** from https://developer.dokmatiq.com
3. **`DOCGEN_API_KEY` environment variable** set in your shell:
   ```bash
   export DOCGEN_API_KEY="dk_live_xxxxxxxxxxxxx"
   ```

## Install in Claude Code

```bash
/plugin marketplace add dokmatiq/claude-plugins
/plugin install docgen@dokmatiq
```

After install, restart Claude Code. The MCP server is auto-configured via the bundled `.mcp.json`, and the skill triggers on relevant prompts.

The bundled `.mcp.json` does not include an `env` block. JSON MCP config files do not perform shell-style `${DOCGEN_API_KEY}` expansion consistently across clients, so the server reads the real `DOCGEN_API_KEY` from the environment of the host process.

### Legacy install from this repository

This repository still contains a backwards-compatible plugin copy:

```bash
claude plugin install dokmatiq/docgen-sdks@plugin
```

### Codex skill install from GitHub

Codex users can install the skill directly from this repository:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo dokmatiq/docgen-sdks \
  --path plugin/skills/dokmatiq-docgen
```

Then configure an MCP server named `docgen` that runs `docgen-mcp` and receives `DOCGEN_API_KEY` in its environment. If `docgen-mcp` was installed into `~/.local/bin`, either add that directory to `PATH` or use the absolute command path in the MCP config.

## Verify

In Claude Code:

```
/mcp
```

Should list `docgen` as connected with 40 tools.

Then try:

```
Generate a PDF from this Markdown: # Hello world
```

The skill should fire and Claude should call `generate_pdf_from_markdown`.

## Without the plugin

If you don't use Claude Code (e.g. Claude Desktop, Cursor, Continue, Cline, Hermes), you can still use the MCP server directly — see https://github.com/dokmatiq/docgen-sdks/tree/main/mcp for setup instructions per client.

## License

MIT
