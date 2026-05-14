# Dokmatiq DocGen — Claude Code Plugin

> **Moved.** This plugin now lives at [github.com/dokmatiq/claude-plugins](https://github.com/dokmatiq/claude-plugins). Install with:
> ```
> /plugin marketplace add dokmatiq/claude-plugins
> /plugin install docgen@dokmatiq
> ```
> The copy in this folder is kept for backward compatibility and will be removed in a future release.

One-step install of the Dokmatiq DocGen MCP server (40 tools) plus a triggering skill that tells Claude Code when to use them.

## What's inside

- **MCP server** auto-configured: 40 tools covering PDF generation, e-invoicing (ZUGFeRD/XRechnung), Excel workbooks, digital signatures, PDF operations, AI-powered receipt recognition
- **Skill** with detailed trigger description so Claude reaches for these tools when relevant — without you having to spell it out each time

## Prerequisites

1. **Python 3.11+** with the MCP server installable:
   ```bash
   pip install dokmatiq-docgen-mcp
   ```
2. **Dokmatiq API key** from https://developer.dokmatiq.com
3. **`DOCGEN_API_KEY` environment variable** set in your shell:
   ```bash
   export DOCGEN_API_KEY="dk_live_xxxxxxxxxxxxx"
   ```

## Install

```bash
claude plugin install dokmatiq/docgen-sdks@plugin
```

After install, restart Claude Code. The MCP server is auto-configured via the bundled `.mcp.json`, and the skill triggers on relevant prompts.

The bundled `.mcp.json` does not include an `env` block. JSON MCP config files do not perform shell-style `${DOCGEN_API_KEY}` expansion consistently across clients, so the server reads the real `DOCGEN_API_KEY` from the environment of the host process.

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
