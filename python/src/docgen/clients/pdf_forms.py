"""PDF Forms sub-client: inspect and fill form fields."""

from __future__ import annotations

from typing import Any

from docgen._files import FileInput, to_base64
from docgen._serialization import from_dict, to_dict
from docgen._transport import Transport
from docgen.models.forms import PdfFormField, PdfFormFillRequest


class PdfFormsClient:
    """Client for PDF AcroForm operations."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def inspect_fields(self, pdf: FileInput) -> list[PdfFormField]:
        """Inspect form fields in a PDF.

        Args:
            pdf: PDF file (path, bytes, or base64).

        Returns:
            List of form fields found in the PDF.
        """
        data = self._transport.request_json(
            "POST", "/api/pdf-forms/fields/base64",
            json={"pdfBase64": to_base64(pdf)},
        )
        # API returns a list directly
        if isinstance(data, list):
            return [from_dict(PdfFormField, item) for item in data]
        return [from_dict(PdfFormField, item) for item in data.get("fields", [])]

    def fill(
        self,
        pdf: FileInput,
        fields: dict[str, str],
        *,
        flatten: bool = False,
        password: str | None = None,
    ) -> bytes:
        """Fill form fields in a PDF.

        Args:
            pdf: PDF file with form fields.
            fields: Field values to fill (name → value).
            flatten: Make fields non-editable after filling.
            password: Optional password for the output PDF.

        Returns:
            Filled PDF bytes.
        """
        request = PdfFormFillRequest(
            pdf_base64=to_base64(pdf),
            fields=fields,
            flatten=flatten,
            password=password,
        )
        return self._transport.request_bytes(
            "POST", "/api/pdf-forms/fill", json=to_dict(request)
        )
