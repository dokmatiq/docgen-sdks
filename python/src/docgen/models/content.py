"""Content positioning types: content areas, watermark, stationery."""

from __future__ import annotations

from dataclasses import dataclass

from docgen.models.enums import BarcodeFormat, TextAlignment


@dataclass
class WatermarkConfig:
    """Diagonal watermark overlay on all pages.

    Args:
        text: Watermark text.
        font_size: Font size in points (default: 72).
        opacity: Opacity from 0.0 (transparent) to 1.0 (opaque). Default: 0.3.
        color: Text color as hex string (e.g. "#FF0000"). Default: gray.
    """

    text: str
    font_size: float = 72.0
    opacity: float = 0.3
    color: str | None = None


@dataclass
class StationeryConfig:
    """PDF stationery (letterhead) overlay applied as background.

    Args:
        pdf: Base64-encoded PDF used as background for all pages.
        first_page_pdf: Optional separate Base64-encoded PDF for page 1 only.
    """

    pdf: str
    first_page_pdf: str | None = None


@dataclass
class ContentArea:
    """Absolutely positioned content on a PDF page.

    Allows placing text, images, or barcodes at exact coordinates.

    Args:
        x: Horizontal position in mm from left edge.
        y: Vertical position in mm from top edge.
        width: Area width in mm.
        height: Area height in mm (optional, for clipping).
        text: Text content. Supports inline markup: **bold**, *italic*.
        font_name: Font family name.
        font_size: Font size in points.
        font_base64: Base64-encoded font file (.ttf/.otf) for inline use.
        color: Text color as hex string.
        alignment: Text alignment within the area.
        image_base64: Base64-encoded image to place in this area.
        image_width: Image width in mm.
        image_height: Image height in mm.
        barcode_content: Barcode data string.
        barcode_format: Barcode format type.
        barcode_width: Barcode width in mm.
        barcode_height: Barcode height in mm.
        pages: Page filter expression. Examples: "1", "2+", "2-4", "all".
    """

    x: float
    y: float
    width: float | None = None
    height: float | None = None
    text: str | None = None
    font_name: str | None = None
    font_size: float | None = None
    font_base64: str | None = None
    color: str | None = None
    alignment: TextAlignment | None = None
    image_base64: str | None = None
    image_width: float | None = None
    image_height: float | None = None
    barcode_content: str | None = None
    barcode_format: BarcodeFormat | None = None
    barcode_width: float | None = None
    barcode_height: float | None = None
    pages: str = "all"
