"""ZUGFeRD sub-client: embed, extract, validate e-invoices."""

from __future__ import annotations

from typing import Any

from docgen._files import FileInput, to_base64
from docgen._serialization import from_dict, to_dict
from docgen._transport import Transport
from docgen.models.enums import ZugferdProfile
from docgen.models.invoice import InvoiceData


class ZugferdClient:
    """Client for ZUGFeRD/Factur-X e-invoice operations."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def embed(
        self,
        pdf: FileInput,
        invoice: InvoiceData,
        *,
        profile: ZugferdProfile = ZugferdProfile.EN16931,
    ) -> bytes:
        """Embed ZUGFeRD/Factur-X invoice data into a PDF.

        The PDF will be converted to PDF/A-3 and the invoice XML attached.

        Args:
            pdf: PDF to embed the invoice into.
            invoice: Structured invoice data.
            profile: ZUGFeRD profile level.

        Returns:
            PDF bytes with embedded invoice.
        """
        payload: dict[str, Any] = {
            "pdfBase64": to_base64(pdf),
            "invoice": to_dict(invoice),
            "profile": profile.value,
        }
        return self._transport.request_bytes(
            "POST", "/api/zugferd/embed/base64", json=payload
        )

    def extract(self, pdf: FileInput) -> InvoiceData:
        """Extract structured invoice data from a ZUGFeRD/Factur-X PDF.

        Args:
            pdf: ZUGFeRD PDF to extract from.

        Returns:
            Extracted invoice data.
        """
        data = self._transport.request_json(
            "POST", "/api/zugferd/extract/base64",
            json={"pdfBase64": to_base64(pdf)},
        )
        return from_dict(InvoiceData, data)

    def validate(self, pdf: FileInput) -> dict[str, Any]:
        """Validate a ZUGFeRD/Factur-X PDF.

        Args:
            pdf: PDF to validate.

        Returns:
            Validation result with valid flag and any errors.
        """
        return self._transport.request_json(
            "POST", "/api/zugferd/validate/base64",
            json={"pdfBase64": to_base64(pdf)},
        )
