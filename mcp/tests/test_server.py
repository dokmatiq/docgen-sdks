"""Smoke tests for the published MCP server entry point and tool interface."""

import base64
import shutil
import tempfile
import unittest
from unittest.mock import patch

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

from docgen_mcp import server


class MCPServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_entrypoint_starts_and_lists_tools(self) -> None:
        command = shutil.which("docgen-mcp")
        self.assertIsNotNone(command, "install the project before running MCP tests")

        params = StdioServerParameters(
            command=command,
            env={"DOCGEN_API_KEY": ""},
        )
        with tempfile.TemporaryFile(mode="w+") as errlog:
            async with Client(
                stdio_client(params, errlog=errlog),
                raise_exceptions=False,
            ) as client:
                result = await client.list_tools()

                self.assertEqual(40, len(result.tools))
                self.assertIn("generate_pdf_from_html", {tool.name for tool in result.tools})

                # A tool call without credentials must be handled by the server,
                # not terminate the stdio process or attempt a network request.
                call_result = await client.call_tool(
                    "generate_pdf_from_html",
                    {"html": "<h1>Smoke test</h1>"},
                )
                self.assertTrue(call_result.is_error)
                self.assertIn("generate_pdf_from_html", call_result.content[0].text)

    async def test_client_can_call_a_tool_without_live_api(self) -> None:
        class FakeDocGen:
            @staticmethod
            def html_to_pdf(html: str) -> bytes:
                return b"pdf-bytes:" + html.encode()

        html = "<h1>Smoke test</h1>"
        with patch.object(server, "_get_client", return_value=FakeDocGen()):
            async with Client(server.mcp) as client:
                result = await client.call_tool("generate_pdf_from_html", {"html": html})

        self.assertFalse(result.is_error)
        self.assertEqual(
            base64.b64encode(b"pdf-bytes:" + html.encode()).decode(),
            result.content[0].text,
        )


if __name__ == "__main__":
    unittest.main()
