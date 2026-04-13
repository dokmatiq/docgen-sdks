"""Fluent builder for ComposeRequest."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from docgen._files import FileInput, to_base64
from docgen.models.content import ContentArea, StationeryConfig, WatermarkConfig
from docgen.models.document import ComposeRequest, DocumentPart
from docgen.models.enums import OutputFormat
from docgen.models.invoice import InvoiceData

if TYPE_CHECKING:
    from docgen.clients.documents import DocumentsClient


class ComposeBuilder:
    """Fluent builder for composing multiple document parts.

    Usage::

        pdf = (dg.compose()
            .part(DocumentPart(html_content="<h1>Part 1</h1>"))
            .part(DocumentPart(html_content="<h1>Part 2</h1>", template_name="report.odt"))
            .watermark("CONFIDENTIAL")
            .as_pdf()
            .generate())
    """

    def __init__(self, client: DocumentsClient | None = None) -> None:
        self._client = client
        self._request = ComposeRequest()

    def part(self, part: DocumentPart) -> Self:
        """Add a document part to the composition."""
        self._request.parts.append(part)
        return self

    def watermark(self, text: str, **kwargs: float | str | None) -> Self:
        """Add a watermark to the combined output."""
        if kwargs:
            self._request.watermark = WatermarkConfig(text=text, **kwargs)  # type: ignore[arg-type]
        else:
            self._request.watermark = text
        return self

    def stationery(self, pdf: FileInput, first_page: FileInput | None = None) -> Self:
        """Set PDF stationery for the combined output."""
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

    def invoice(self, data: InvoiceData) -> Self:
        """Attach invoice data for ZUGFeRD embedding."""
        self._request.invoice = data
        return self

    def password(self, pw: str) -> Self:
        """Encrypt the output PDF."""
        self._request.password = pw
        return self

    def output_format(self, fmt: OutputFormat) -> Self:
        """Set the output format."""
        self._request.output_format = fmt
        return self

    def as_pdf(self) -> Self:
        self._request.output_format = OutputFormat.PDF
        return self

    def as_docx(self) -> Self:
        self._request.output_format = OutputFormat.DOCX
        return self

    def as_odt(self) -> Self:
        self._request.output_format = OutputFormat.ODT
        return self

    def build(self) -> ComposeRequest:
        """Build the ComposeRequest without sending it."""
        return self._request

    def generate(self) -> bytes:
        """Build and immediately send the compose request."""
        if self._client is None:
            raise RuntimeError(
                "Cannot call generate() without a client. "
                "Use dg.compose().part(...).generate()."
            )
        return self._client.compose(self._request)
