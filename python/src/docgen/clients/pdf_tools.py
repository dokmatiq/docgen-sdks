"""PDF Tools sub-client: merge, split, metadata, PDF/A, rotate."""

from __future__ import annotations

from typing import Any

from docgen._files import FileInput, to_base64, to_bytes, detect_filename
from docgen._transport import Transport


class PdfToolsClient:
    """Client for PDF manipulation operations."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def merge(self, files: list[FileInput]) -> bytes:
        """Merge multiple PDFs into one.

        Args:
            files: List of PDF files to merge (in order).

        Returns:
            Merged PDF bytes.
        """
        pdfs = [to_base64(f) for f in files]
        return self._transport.request_bytes(
            "POST", "/api/pdf-tools/merge/base64",
            json={"pdfs": pdfs},
        )

    def split(self, pdf: FileInput) -> list[bytes]:
        """Split a PDF into individual pages.

        Args:
            pdf: PDF to split.

        Returns:
            List of single-page PDF bytes.
        """
        name = detect_filename(pdf) or "document.pdf"
        data = to_bytes(pdf)
        # Split returns a zip file containing individual pages
        return [self._transport.upload_bytes(
            "/api/pdf-tools/split",
            files={"file": (name, data, "application/pdf")},
        )]

    def extract_text(self, pdf: FileInput) -> str:
        """Extract text from a PDF.

        Args:
            pdf: PDF to extract text from.

        Returns:
            Extracted text content.
        """
        name = detect_filename(pdf) or "document.pdf"
        data = to_bytes(pdf)
        result = self._transport.upload(
            "/api/pdf-tools/extract",
            files={"file": (name, data, "application/pdf")},
        )
        return str(result.get("text", ""))

    def get_metadata(self, pdf: FileInput) -> dict[str, Any]:
        """Get PDF metadata (title, author, subject, etc.).

        Args:
            pdf: PDF to read metadata from.

        Returns:
            Dict of metadata fields.
        """
        name = detect_filename(pdf) or "document.pdf"
        data = to_bytes(pdf)
        return self._transport.upload(
            "/api/pdf-tools/metadata",
            files={"file": (name, data, "application/pdf")},
        )

    def set_metadata(
        self,
        pdf: FileInput,
        *,
        title: str | None = None,
        author: str | None = None,
        subject: str | None = None,
        keywords: str | None = None,
        creator: str | None = None,
        producer: str | None = None,
    ) -> bytes:
        """Set PDF metadata.

        Args:
            pdf: PDF to modify.
            title: Document title.
            author: Document author.
            subject: Document subject.
            keywords: Document keywords.
            creator: Creator application name.
            producer: Producer application name.

        Returns:
            Modified PDF bytes.
        """
        payload: dict[str, Any] = {"pdfBase64": to_base64(pdf)}
        metadata: dict[str, str] = {}
        if title is not None:
            metadata["title"] = title
        if author is not None:
            metadata["author"] = author
        if subject is not None:
            metadata["subject"] = subject
        if keywords is not None:
            metadata["keywords"] = keywords
        if creator is not None:
            metadata["creator"] = creator
        if producer is not None:
            metadata["producer"] = producer
        payload["metadata"] = metadata

        return self._transport.request_bytes(
            "POST", "/api/pdf-tools/metadata/set/base64", json=payload
        )

    def to_pdfa(self, pdf: FileInput) -> bytes:
        """Convert a PDF to PDF/A format for archival.

        Args:
            pdf: PDF to convert.

        Returns:
            PDF/A bytes.
        """
        return self._transport.request_bytes(
            "POST", "/api/pdf-tools/pdfa/base64",
            json={"pdfBase64": to_base64(pdf)},
        )

    def rotate(self, pdf: FileInput, degrees: int, pages: str = "all") -> bytes:
        """Rotate PDF pages.

        Args:
            pdf: PDF to rotate.
            degrees: Rotation angle (90, 180, 270).
            pages: Page filter ("all", "1", "2-4", etc.).

        Returns:
            Rotated PDF bytes.
        """
        name = detect_filename(pdf) or "document.pdf"
        data = to_bytes(pdf)
        return self._transport.upload_bytes(
            "/api/pdf-tools/rotate",
            files={"file": (name, data, "application/pdf")},
            data={"degrees": str(degrees), "pages": pages},
        )
