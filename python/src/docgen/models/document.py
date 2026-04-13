"""Core document request types."""

from __future__ import annotations

from dataclasses import dataclass, field

from docgen.models.content import ContentArea, StationeryConfig, WatermarkConfig
from docgen.models.enums import OutputFormat
from docgen.models.invoice import InvoiceData
from docgen.models.markdown import MarkdownStyles
from docgen.models.media import BarcodeData, ImageData, QrCodeData, TableData
from docgen.models.page import PageSettings


@dataclass
class DocumentRequest:
    """Request to generate a single document.

    At least one of html_content or markdown_content should be provided,
    or a template_name/template_base64 with fields.

    Args:
        html_content: HTML content to render.
        markdown_content: Markdown content to render.
        output_format: Target format (PDF, DOCX, ODT).
        template_name: Name of a pre-uploaded template.
        template_base64: Base64-encoded template file.
        template_filename: Filename hint for inline template (to detect format).
        fields: Template field replacements (key → value).
        bookmarks: HTML content to insert at named bookmarks.
        markdown_bookmarks: Markdown content to insert at named bookmarks.
        images: Images to insert at named bookmarks.
        qr_codes: QR codes to generate at named bookmarks.
        barcodes: Barcodes to generate at named bookmarks.
        tables: Tables to insert at named bookmarks.
        page_settings: Page layout configuration.
        markdown_styles: Custom Markdown → LibreOffice style mapping.
        watermark: Watermark config or simple string for diagonal text overlay.
        stationery: PDF stationery/letterhead background.
        content_areas: Absolutely positioned content on PDF pages.
        invoice: Invoice data for ZUGFeRD embedding.
        password: Password to encrypt the output PDF.
        callback_url: Webhook URL for async job completion notification.
        callback_secret: HMAC secret for webhook signature verification.
    """

    html_content: str | None = None
    markdown_content: str | None = None
    output_format: OutputFormat = OutputFormat.PDF
    template_name: str | None = None
    template_base64: str | None = None
    template_filename: str | None = None
    fields: dict[str, str] | None = None
    bookmarks: dict[str, str] | None = None
    markdown_bookmarks: dict[str, str] | None = None
    images: dict[str, ImageData] | None = None
    qr_codes: dict[str, QrCodeData] | None = None
    barcodes: dict[str, BarcodeData] | None = None
    tables: dict[str, TableData] | None = None
    page_settings: PageSettings | None = None
    markdown_styles: MarkdownStyles | None = None
    watermark: WatermarkConfig | str | None = None
    stationery: StationeryConfig | None = None
    content_areas: list[ContentArea] | None = None
    invoice: InvoiceData | None = None
    password: str | None = None
    callback_url: str | None = None
    callback_secret: str | None = None


@dataclass
class DocumentPart:
    """A single part in a composed multi-part document.

    Args:
        html_content: HTML content for this part.
        markdown_content: Markdown content for this part.
        template_name: Template to use for this part.
        template_base64: Inline template for this part.
        template_filename: Filename hint for inline template.
        fields: Field replacements for this part.
        bookmarks: Bookmark HTML content for this part.
        markdown_bookmarks: Bookmark Markdown content for this part.
        images: Images for this part.
        qr_codes: QR codes for this part.
        barcodes: Barcodes for this part.
        tables: Tables for this part.
        page_settings: Page settings for this part.
        markdown_styles: Markdown style mapping for this part.
    """

    html_content: str | None = None
    markdown_content: str | None = None
    template_name: str | None = None
    template_base64: str | None = None
    template_filename: str | None = None
    fields: dict[str, str] | None = None
    bookmarks: dict[str, str] | None = None
    markdown_bookmarks: dict[str, str] | None = None
    images: dict[str, ImageData] | None = None
    qr_codes: dict[str, QrCodeData] | None = None
    barcodes: dict[str, BarcodeData] | None = None
    tables: dict[str, TableData] | None = None
    page_settings: PageSettings | None = None
    markdown_styles: MarkdownStyles | None = None


@dataclass
class ComposeRequest:
    """Request to compose multiple document parts into a single document.

    Args:
        parts: List of document parts to combine.
        output_format: Target format for the combined document.
        watermark: Watermark applied to the combined output.
        stationery: Stationery applied to the combined output.
        content_areas: Content areas on the combined output.
        invoice: Invoice data for ZUGFeRD embedding.
        password: Password for the combined output.
        callback_url: Webhook URL for async job completion.
        callback_secret: HMAC secret for webhook signature.
    """

    parts: list[DocumentPart] = field(default_factory=list)
    output_format: OutputFormat = OutputFormat.PDF
    watermark: WatermarkConfig | str | None = None
    stationery: StationeryConfig | None = None
    content_areas: list[ContentArea] | None = None
    invoice: InvoiceData | None = None
    password: str | None = None
    callback_url: str | None = None
    callback_secret: str | None = None
