"""XRechnung sub-client: generate, parse, validate, transform, detect, AI extract."""

from __future__ import annotations

from typing import Any

from docgen._files import FileInput, to_base64, to_bytes, detect_filename
from docgen._serialization import from_dict, to_dict
from docgen._transport import Transport
from docgen.models.enums import XRechnungFormat
from docgen.models.extraction import ExtractionResult
from docgen.models.invoice import InvoiceData


class XRechnungClient:
    """Client for XRechnung (EN 16931) e-invoice operations."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def generate(
        self,
        invoice: InvoiceData,
        *,
        format: XRechnungFormat = XRechnungFormat.CII,
    ) -> bytes:
        """Generate XRechnung XML from structured invoice data.

        Args:
            invoice: Invoice data (buyer_reference is required for XRechnung).
            format: XML format (CII or UBL).

        Returns:
            XRechnung XML bytes.
        """
        payload: dict[str, Any] = {
            "invoiceData": to_dict(invoice),
            "format": format.value,
        }
        return self._transport.request_bytes(
            "POST", "/api/xrechnung/generate", json=payload
        )

    def parse(self, xml: FileInput) -> InvoiceData:
        """Parse an XRechnung XML into structured invoice data.

        Args:
            xml: XRechnung XML file.

        Returns:
            Parsed invoice data.
        """
        name = detect_filename(xml) or "invoice.xml"
        data_bytes = to_bytes(xml)
        result = self._transport.upload(
            "/api/xrechnung/parse",
            files={"file": (name, data_bytes, "application/xml")},
        )
        return from_dict(InvoiceData, result)

    def validate(self, xml: FileInput) -> dict[str, Any]:
        """Validate an XRechnung XML against EN 16931.

        Args:
            xml: XRechnung XML file.

        Returns:
            Validation result with valid flag and any errors.
        """
        name = detect_filename(xml) or "invoice.xml"
        data_bytes = to_bytes(xml)
        return self._transport.upload(
            "/api/xrechnung/validate",
            files={"file": (name, data_bytes, "application/xml")},
        )

    def transform(
        self,
        xml: FileInput,
        *,
        target_format: XRechnungFormat,
    ) -> bytes:
        """Transform XRechnung between CII and UBL formats.

        Args:
            xml: Source XRechnung XML.
            target_format: Target format (CII or UBL).

        Returns:
            Transformed XML bytes.
        """
        name = detect_filename(xml) or "invoice.xml"
        data_bytes = to_bytes(xml)
        return self._transport.upload_bytes(
            "/api/xrechnung/transform",
            files={"file": (name, data_bytes, "application/xml")},
            data={"targetFormat": target_format.value},
        )

    def detect(self, xml: FileInput) -> XRechnungFormat:
        """Detect the format (CII or UBL) of an XRechnung XML.

        Args:
            xml: XRechnung XML file.

        Returns:
            Detected format.
        """
        name = detect_filename(xml) or "invoice.xml"
        data_bytes = to_bytes(xml)
        result = self._transport.upload(
            "/api/xrechnung/detect",
            files={"file": (name, data_bytes, "application/xml")},
        )
        return XRechnungFormat(result.get("format", "CII"))

    def extract_ai(self, source: FileInput) -> ExtractionResult:
        """Extract invoice data from a PDF or image using AI.

        Uses Claude AI to extract structured invoice data from
        unstructured documents (scanned invoices, images, etc.).

        Args:
            source: PDF or image file to extract from.

        Returns:
            Extraction result with invoice data and confidence info.
        """
        name = detect_filename(source) or "document.pdf"
        data_bytes = to_bytes(source)
        content_type = "application/pdf" if name.endswith(".pdf") else "image/png"
        result = self._transport.upload(
            "/api/xrechnung/extract",
            files={"file": (name, data_bytes, content_type)},
        )
        return from_dict(ExtractionResult, result)
