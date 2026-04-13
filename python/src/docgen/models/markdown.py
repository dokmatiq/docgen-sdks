"""Markdown style mapping."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MarkdownStyles:
    """Custom mapping of Markdown elements to LibreOffice style names.

    Each field maps a Markdown element type to a named style in the
    LibreOffice template. Leave None to use default styles.

    Args:
        heading1: Style name for # headings.
        heading2: Style name for ## headings.
        heading3: Style name for ### headings.
        heading4: Style name for #### headings.
        paragraph: Style name for body paragraphs.
        list_bullet: Style name for unordered list items.
        list_number: Style name for ordered list items.
        code_block: Style name for fenced code blocks.
        block_quote: Style name for blockquotes.
    """

    heading1: str | None = None
    heading2: str | None = None
    heading3: str | None = None
    heading4: str | None = None
    paragraph: str | None = None
    list_bullet: str | None = None
    list_number: str | None = None
    code_block: str | None = None
    block_quote: str | None = None
