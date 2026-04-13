"""Fluent builder for DocumentRequest."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Self

from docgen._files import FileInput, to_base64, detect_filename
from docgen.models.content import ContentArea, StationeryConfig, WatermarkConfig
from docgen.models.document import DocumentRequest
from docgen.models.enums import BarcodeFormat, OutputFormat
from docgen.models.invoice import InvoiceData
from docgen.models.markdown import MarkdownStyles
from docgen.models.media import BarcodeData, ImageData, QrCodeData, TableData
from docgen.models.page import PageSettings

if TYPE_CHECKING:
    from docgen.clients.documents import DocumentsClient


class DocumentBuilder:
    """Fluent builder for constructing and executing document generation requests.

    Usage::

        pdf = (dg.document()
            .html("<h1>Hello</h1>")
            .template("invoice.odt")
            .field("company", "ACME")
            .as_pdf()
            .generate())
    """

    def __init__(self, client: DocumentsClient | None = None) -> None:
        self._client = client
        self._request = DocumentRequest()

    # --- Content ---

    def html(self, content: str) -> Self:
        """Set HTML content for the document."""
        self._request.html_content = content
        return self

    def markdown(self, content: str) -> Self:
        """Set Markdown content for the document."""
        self._request.markdown_content = content
        return self

    # --- Template ---

    def template(self, name: str) -> Self:
        """Use a pre-uploaded template by name."""
        self._request.template_name = name
        return self

    def template_file(self, path: FileInput) -> Self:
        """Use an inline template from a file path or bytes."""
        self._request.template_base64 = to_base64(path)
        filename = detect_filename(path)
        if filename:
            self._request.template_filename = filename
        return self

    # --- Fields & Bookmarks ---

    def field(self, key: str, value: str) -> Self:
        """Set a single template field value."""
        if self._request.fields is None:
            self._request.fields = {}
        self._request.fields[key] = value
        return self

    def fields(self, **kwargs: str) -> Self:
        """Set multiple template field values."""
        if self._request.fields is None:
            self._request.fields = {}
        self._request.fields.update(kwargs)
        return self

    def bookmark(self, name: str, html: str) -> Self:
        """Insert HTML content at a named bookmark."""
        if self._request.bookmarks is None:
            self._request.bookmarks = {}
        self._request.bookmarks[name] = html
        return self

    def markdown_bookmark(self, name: str, md: str) -> Self:
        """Insert Markdown content at a named bookmark."""
        if self._request.markdown_bookmarks is None:
            self._request.markdown_bookmarks = {}
        self._request.markdown_bookmarks[name] = md
        return self

    # --- Media ---

    def image(self, bookmark: str, source: ImageData | FileInput, width: float = 50, height: float = 50) -> Self:
        """Insert an image at a named bookmark.

        Args:
            bookmark: Bookmark name in the template.
            source: ImageData object, file path, bytes, or base64 string.
            width: Image width in mm (used when source is not ImageData).
            height: Image height in mm (used when source is not ImageData).
        """
        if self._request.images is None:
            self._request.images = {}
        if isinstance(source, ImageData):
            self._request.images[bookmark] = source
        else:
            self._request.images[bookmark] = ImageData(
                base64=to_base64(source), width=width, height=height
            )
        return self

    def qr_code(self, bookmark: str, content: str, size: float = 40) -> Self:
        """Generate a QR code at a named bookmark."""
        if self._request.qr_codes is None:
            self._request.qr_codes = {}
        self._request.qr_codes[bookmark] = QrCodeData(content=content, size=size)
        return self

    def barcode(
        self,
        bookmark: str,
        content: str,
        format: BarcodeFormat = BarcodeFormat.CODE128,
        width: float = 60,
        height: float = 30,
        show_text: bool = True,
    ) -> Self:
        """Generate a barcode at a named bookmark."""
        if self._request.barcodes is None:
            self._request.barcodes = {}
        self._request.barcodes[bookmark] = BarcodeData(
            content=content, format=format, width=width, height=height, show_text=show_text
        )
        return self

    def table(self, bookmark: str, data: TableData) -> Self:
        """Insert a table at a named bookmark."""
        if self._request.tables is None:
            self._request.tables = {}
        self._request.tables[bookmark] = data
        return self

    # --- Page & Layout ---

    def page_settings(self, settings: PageSettings) -> Self:
        """Set page layout (orientation, paper size, margins, headers/footers)."""
        self._request.page_settings = settings
        return self

    def markdown_styles(self, styles: MarkdownStyles) -> Self:
        """Set custom Markdown → LibreOffice style mapping."""
        self._request.markdown_styles = styles
        return self

    def watermark(self, text: str, **kwargs: float | str | None) -> Self:
        """Add a diagonal watermark overlay.

        Args:
            text: Watermark text.
            **kwargs: Optional WatermarkConfig fields (font_size, opacity, color).
        """
        if kwargs:
            self._request.watermark = WatermarkConfig(text=text, **kwargs)  # type: ignore[arg-type]
        else:
            self._request.watermark = text
        return self

    def stationery(self, pdf: FileInput, first_page: FileInput | None = None) -> Self:
        """Set a PDF stationery (letterhead) background.

        Args:
            pdf: PDF file for all pages.
            first_page: Optional separate PDF for page 1 only.
        """
        config = StationeryConfig(pdf=to_base64(pdf))
        if first_page is not None:
            config.first_page_pdf = to_base64(first_page)
        self._request.stationery = config
        return self

    def content_area(self, area: ContentArea) -> Self:
        """Add an absolutely positioned content area."""
        if self._request.content_areas is None:
            self._request.content_areas = []
        self._request.content_areas.append(area)
        return self

    # --- Invoice ---

    def invoice(self, data: InvoiceData) -> Self:
        """Attach invoice data for ZUGFeRD embedding."""
        self._request.invoice = data
        return self

    # --- Security ---

    def password(self, pw: str) -> Self:
        """Encrypt the output PDF with a password."""
        self._request.password = pw
        return self

    # --- Output Format ---

    def output_format(self, fmt: OutputFormat) -> Self:
        """Set the output format."""
        self._request.output_format = fmt
        return self

    def as_pdf(self) -> Self:
        """Set output format to PDF."""
        self._request.output_format = OutputFormat.PDF
        return self

    def as_docx(self) -> Self:
        """Set output format to DOCX."""
        self._request.output_format = OutputFormat.DOCX
        return self

    def as_odt(self) -> Self:
        """Set output format to ODT."""
        self._request.output_format = OutputFormat.ODT
        return self

    # --- Async ---

    def callback(self, url: str, secret: str | None = None) -> Self:
        """Set webhook callback for async generation."""
        self._request.callback_url = url
        if secret:
            self._request.callback_secret = secret
        return self

    # --- Build & Execute ---

    def build(self) -> DocumentRequest:
        """Build the DocumentRequest without sending it."""
        return self._request

    def generate(self) -> bytes:
        """Build and immediately send the generation request.

        Returns:
            Raw document bytes (PDF, DOCX, or ODT).

        Raises:
            RuntimeError: If no client is attached (use via ``dg.document()``).
        """
        if self._client is None:
            raise RuntimeError(
                "Cannot call generate() without a client. "
                "Use dg.document().html(...).generate() or build the request with .build() "
                "and pass it to client.documents.generate()."
            )
        return self._client.generate(self._request)
