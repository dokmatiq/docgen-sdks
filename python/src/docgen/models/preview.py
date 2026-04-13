"""PDF preview types."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PreviewPage:
    """A single rendered page from a PDF preview.

    Args:
        page_number: 1-based page number.
        image_base64: Base64-encoded page image (PNG or JPEG).
        width: Rendered image width in pixels.
        height: Rendered image height in pixels.
    """

    page_number: int
    image_base64: str
    width: int
    height: int


@dataclass
class PreviewResponse:
    """Multi-page PDF preview result.

    Args:
        page_count: Total number of pages in the PDF.
        format: Image format ("png" or "jpeg").
        dpi: Render resolution in DPI.
        pages: Rendered page images.
    """

    page_count: int = 0
    format: str = "png"
    dpi: int = 150
    pages: list[PreviewPage] = field(default_factory=list)
