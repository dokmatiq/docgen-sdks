"""AI invoice extraction types."""

from __future__ import annotations

from dataclasses import dataclass, field

from docgen.models.invoice import InvoiceData


@dataclass
class ExtractionResult:
    """Result of AI-powered invoice data extraction.

    Args:
        invoice_data: Extracted structured invoice data (if successful).
        missing_fields: Fields that could not be extracted.
        uncertain_fields: Fields extracted with low confidence.
        ai_extraction_used: Whether AI was used for extraction.
        raw_pdf_text: Raw text extracted from the PDF.
        error: Error message if extraction failed.
    """

    invoice_data: InvoiceData | None = None
    missing_fields: list[str] = field(default_factory=list)
    uncertain_fields: list[str] = field(default_factory=list)
    ai_extraction_used: bool = False
    raw_pdf_text: str | None = None
    error: str | None = None
