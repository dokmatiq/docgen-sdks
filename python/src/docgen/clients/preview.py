"""Preview sub-client: render PDF pages as images."""

from __future__ import annotations

from docgen._files import FileInput, to_base64
from docgen._serialization import from_dict
from docgen._transport import Transport
from docgen.models.preview import PreviewPage, PreviewResponse


class PreviewClient:
    """Client for PDF preview rendering."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def preview_page(
        self,
        pdf: FileInput,
        *,
        page: int = 1,
        dpi: int = 150,
        format: str = "png",
    ) -> bytes:
        """Render a single PDF page as an image.

        Args:
            pdf: PDF to preview.
            page: Page number (1-based).
            dpi: Render resolution.
            format: Image format ("png" or "jpeg").

        Returns:
            Raw image bytes (PNG or JPEG).
        """
        return self._transport.request_bytes(
            "POST", "/api/preview/base64",
            json={
                "pdfBase64": to_base64(pdf),
                "page": page,
                "dpi": dpi,
                "format": format,
            },
        )

    def preview_pages(
        self,
        pdf: FileInput,
        *,
        dpi: int = 150,
        format: str = "png",
    ) -> PreviewResponse:
        """Render all pages of a PDF as images.

        Args:
            pdf: PDF to preview.
            dpi: Render resolution.
            format: Image format ("png" or "jpeg").

        Returns:
            Preview response with base64-encoded page images.
        """
        data = self._transport.request_json(
            "POST", "/api/preview/pages/base64",
            json={
                "pdfBase64": to_base64(pdf),
                "dpi": dpi,
                "format": format,
            },
        )
        return from_dict(PreviewResponse, data)

    def page_count(self, pdf: FileInput) -> int:
        """Count the number of pages in a PDF.

        Args:
            pdf: PDF to count pages of.

        Returns:
            Number of pages.
        """
        data = self._transport.request_json(
            "POST", "/api/preview/page-count",
            json={"pdfBase64": to_base64(pdf)},
        )
        return data.get("pageCount", 0)
