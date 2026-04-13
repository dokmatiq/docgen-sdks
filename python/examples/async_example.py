"""Async usage examples for the DocGen Python SDK."""

import asyncio
from pathlib import Path

from docgen import AsyncDocGen


async def main():
    """Generate documents asynchronously."""
    async with AsyncDocGen(api_key="dk_live_xxx") as dg:
        # Simple async generation
        pdf = await dg.html_to_pdf("<h1>Async Hello</h1>")
        Path("async-hello.pdf").write_bytes(pdf)

        # Parallel generation
        results = await asyncio.gather(
            dg.html_to_pdf("<h1>Document A</h1>"),
            dg.html_to_pdf("<h1>Document B</h1>"),
            dg.markdown_to_pdf("# Document C\n\nGenerated in parallel."),
        )
        for i, result in enumerate(results):
            Path(f"parallel-{i + 1}.pdf").write_bytes(result)

        print(f"Generated {len(results) + 1} documents")


if __name__ == "__main__":
    asyncio.run(main())
