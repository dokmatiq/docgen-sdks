"""Media types: images, QR codes, barcodes, tables."""

from __future__ import annotations

from dataclasses import dataclass, field

from docgen.models.enums import BarcodeFormat, ColumnFormat, TextAlignment


@dataclass
class ImageData:
    """Image to insert at a bookmark position.

    Args:
        base64: Base64-encoded image data (PNG, JPG, WEBP, GIF).
        width: Image width in millimeters.
        height: Image height in millimeters.
    """

    base64: str
    width: float
    height: float


@dataclass
class QrCodeData:
    """QR code to generate and insert at a bookmark position.

    Args:
        content: QR code content (URL, text, EPC/GiroCode string, etc.).
        size: QR code size in millimeters (width = height).
    """

    content: str
    size: float = 40.0


@dataclass
class BarcodeData:
    """Barcode to generate and insert at a bookmark position.

    Args:
        content: Barcode data string.
        format: Barcode format (CODE128, EAN13, etc.).
        width: Barcode width in millimeters.
        height: Barcode height in millimeters.
        show_text: Whether to display the barcode value as text below.
    """

    content: str
    format: BarcodeFormat = BarcodeFormat.CODE128
    width: float = 60.0
    height: float = 30.0
    show_text: bool = True


@dataclass
class ColumnDef:
    """Table column definition.

    Args:
        header: Column header text.
        width: Column width in millimeters.
        alignment: Text alignment within the column.
        format: Data format (text, number, currency).
        style_name: Optional LibreOffice style name for the column.
    """

    header: str
    width: float = 40.0
    alignment: TextAlignment = TextAlignment.LEFT
    format: ColumnFormat = ColumnFormat.TEXT
    style_name: str | None = None


@dataclass
class TableStyle:
    """Inline styling for table rendering.

    Args:
        header_background: Header row background color (hex, e.g. "#003366").
        border_color: Table border color (hex).
        alternating_row_color: Alternating row background color (hex).
        header_font_size: Header font size in points.
        body_font_size: Body font size in points.
    """

    header_background: str | None = None
    border_color: str | None = None
    alternating_row_color: str | None = None
    header_font_size: float | None = None
    body_font_size: float | None = None


@dataclass
class TableData:
    """Table to insert at a bookmark position.

    Args:
        columns: Column definitions.
        rows: Row data as list of lists (each inner list = one row).
        style: Inline styling options.
        template_style: Named LibreOffice table style (e.g. "Box List Blue").
    """

    columns: list[ColumnDef]
    rows: list[list[str]] = field(default_factory=list)
    style: TableStyle | None = None
    template_style: str | None = None
