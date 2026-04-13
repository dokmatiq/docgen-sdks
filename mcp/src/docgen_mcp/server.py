"""DocGen MCP Server – exposes DocGen API capabilities as MCP tools.

Configure via environment variables:
    DOCGEN_API_KEY  – API key for the DocGen service (required)
    DOCGEN_BASE_URL – Base URL override (default: https://api.dokmatiq.com)
"""

from __future__ import annotations

import base64
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# Lazy-init the DocGen client on first tool call
_client = None

logger = logging.getLogger("docgen-mcp")

mcp = FastMCP("DocGen")


def _get_client():
    """Lazy-initialise the DocGen client."""
    global _client
    if _client is None:
        # Import here so the module can be imported without the SDK installed
        # (useful for schema introspection)
        from docgen import DocGen

        api_key = os.environ.get("DOCGEN_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "DOCGEN_API_KEY environment variable is required. "
                "Set it to your DocGen API key before starting the server."
            )
        base_url = os.environ.get("DOCGEN_BASE_URL")
        kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        _client = DocGen(**kwargs)
    return _client


# ─── Document Generation ─────────────────────────────────────────────


@mcp.tool()
def generate_pdf_from_html(html: str) -> str:
    """Generate a PDF from HTML content.

    Args:
        html: HTML content to convert to PDF.

    Returns:
        Base64-encoded PDF bytes.
    """
    dg = _get_client()
    pdf = dg.html_to_pdf(html)
    return base64.b64encode(pdf).decode()


@mcp.tool()
def generate_pdf_from_markdown(markdown: str) -> str:
    """Generate a PDF from Markdown content.

    Args:
        markdown: Markdown content to convert to PDF.

    Returns:
        Base64-encoded PDF bytes.
    """
    dg = _get_client()
    pdf = dg.markdown_to_pdf(markdown)
    return base64.b64encode(pdf).decode()


@mcp.tool()
def generate_document(
    html_content: str | None = None,
    markdown_content: str | None = None,
    template_name: str | None = None,
    fields: dict[str, str] | None = None,
    watermark: str | None = None,
    output_format: str = "PDF",
) -> str:
    """Generate a document with optional template, fields, and watermark.

    Args:
        html_content: HTML content for the document body.
        markdown_content: Markdown content (alternative to HTML).
        template_name: Name of a pre-uploaded template (ODT/DOCX).
        fields: Template field replacements (key-value pairs).
        watermark: Diagonal watermark text overlay.
        output_format: Output format – PDF, DOCX, or ODT (default: PDF).

    Returns:
        Base64-encoded document bytes.
    """
    dg = _get_client()
    from docgen.models import OutputFormat

    builder = dg.document()
    if html_content:
        builder.html(html_content)
    if markdown_content:
        builder.markdown(markdown_content)
    if template_name:
        builder.template(template_name)
    if fields:
        builder.fields(fields)
    if watermark:
        builder.watermark(watermark)
    builder.output_format(OutputFormat(output_format))

    result = builder.generate()
    return base64.b64encode(result).decode()


@mcp.tool()
def compose_document(
    parts: list[dict[str, Any]],
    watermark: str | None = None,
    output_format: str = "PDF",
) -> str:
    """Compose a multi-part document from several sections.

    Each part is a dict with: htmlContent, markdownContent, templateName, fields.

    Args:
        parts: List of document parts. Each part can have htmlContent, markdownContent, templateName, fields.
        watermark: Optional diagonal watermark text overlay.
        output_format: Output format – PDF, DOCX, or ODT (default: PDF).

    Returns:
        Base64-encoded document bytes.
    """
    dg = _get_client()
    from docgen.models import DocumentPart, OutputFormat

    builder = dg.compose()
    for p in parts:
        builder.part(DocumentPart(
            html_content=p.get("htmlContent"),
            markdown_content=p.get("markdownContent"),
            template_name=p.get("templateName"),
            fields=p.get("fields"),
        ))
    if watermark:
        builder.watermark(watermark)
    builder.output_format(OutputFormat(output_format))

    result = builder.generate()
    return base64.b64encode(result).decode()


# ─── E-Invoicing ─────────────────────────────────────────────────────


@mcp.tool()
def create_invoice(
    invoice_number: str,
    invoice_date: str,
    seller_name: str,
    seller_street: str,
    seller_zip: str,
    seller_city: str,
    buyer_name: str,
    buyer_street: str,
    buyer_zip: str,
    buyer_city: str,
    items: list[dict[str, Any]],
    iban: str | None = None,
    bic: str | None = None,
    payment_terms: str | None = None,
    due_date: str | None = None,
    seller_vat_id: str | None = None,
    seller_country: str = "DE",
    buyer_country: str = "DE",
    buyer_vat_id: str | None = None,
    currency: str = "EUR",
    template_name: str | None = None,
    html_content: str | None = None,
) -> str:
    """Create a ZUGFeRD-compliant invoice PDF with structured e-invoicing data.

    Each item in the items list should have: description, unitPrice, and optionally
    quantity, unit (C62=piece, HUR=hour, DAY=day, KGM=kg), vatRate.

    Args:
        invoice_number: Unique invoice number (e.g. "RE-2026-001").
        invoice_date: Invoice date in ISO format (e.g. "2026-04-12").
        seller_name: Seller company name.
        seller_street: Seller street address.
        seller_zip: Seller postal code.
        seller_city: Seller city.
        buyer_name: Buyer company name.
        buyer_street: Buyer street address.
        buyer_zip: Buyer postal code.
        buyer_city: Buyer city.
        items: Line items – each with description, unitPrice, and optionally quantity, unit, vatRate.
        iban: Payment IBAN.
        bic: Payment BIC/SWIFT code.
        payment_terms: Payment terms text.
        due_date: Payment due date (ISO format).
        seller_vat_id: Seller VAT ID.
        seller_country: Seller country code (default: DE).
        buyer_country: Buyer country code (default: DE).
        buyer_vat_id: Buyer VAT ID.
        currency: Currency code (default: EUR).
        template_name: Template name for the invoice layout.
        html_content: HTML content for the invoice body.

    Returns:
        Base64-encoded PDF with embedded ZUGFeRD XML.
    """
    dg = _get_client()
    from docgen.models import InvoiceUnit

    inv = dg.invoice()
    inv.number(invoice_number).date(invoice_date)
    inv.seller(
        name=seller_name, street=seller_street, zip=seller_zip,
        city=seller_city, country=seller_country, vat_id=seller_vat_id,
    )
    inv.buyer(
        name=buyer_name, street=buyer_street, zip=buyer_zip,
        city=buyer_city, country=buyer_country, vat_id=buyer_vat_id,
    )

    for item in items:
        unit = item.get("unit", "C62")
        inv.item(
            description=item["description"],
            quantity=float(item.get("quantity", 1)),
            unit=InvoiceUnit(unit),
            unit_price=float(item["unitPrice"]),
            vat_rate=float(item.get("vatRate", 19.0)),
        )

    if iban:
        inv.bank(iban=iban, bic=bic)
    if payment_terms:
        inv.payment_terms(payment_terms)
    if due_date:
        inv.due_date(due_date)
    inv.currency(currency)

    invoice_data = inv.build()

    doc = dg.document()
    if html_content:
        doc.html(html_content)
    else:
        doc.html(f"<h1>Rechnung {invoice_number}</h1>")
    if template_name:
        doc.template(template_name)
    doc.invoice(invoice_data)
    doc.as_pdf()

    result = doc.generate()
    return base64.b64encode(result).decode()


# ─── PDF Tools ───────────────────────────────────────────────────────


@mcp.tool()
def merge_pdfs(pdfs_base64: list[str]) -> str:
    """Merge multiple PDFs into a single PDF.

    Args:
        pdfs_base64: List of base64-encoded PDF files to merge.

    Returns:
        Base64-encoded merged PDF.
    """
    dg = _get_client()
    files = [base64.b64decode(p) for p in pdfs_base64]
    merged = dg.merge_pdfs(files)
    return base64.b64encode(merged).decode()


@mcp.tool()
def extract_text_from_pdf(pdf_base64: str) -> str:
    """Extract all text content from a PDF.

    Args:
        pdf_base64: Base64-encoded PDF file.

    Returns:
        Extracted text content.
    """
    dg = _get_client()
    return dg.pdf_tools.extract_text(base64.b64decode(pdf_base64))


@mcp.tool()
def get_pdf_metadata(pdf_base64: str) -> str:
    """Get metadata (title, author, page count, etc.) from a PDF.

    Args:
        pdf_base64: Base64-encoded PDF file.

    Returns:
        JSON string with metadata fields.
    """
    dg = _get_client()
    metadata = dg.pdf_tools.get_metadata(base64.b64decode(pdf_base64))
    from docgen._serialization import to_dict
    return json.dumps(to_dict(metadata))


@mcp.tool()
def convert_to_pdfa(pdf_base64: str) -> str:
    """Convert a PDF to PDF/A archival format.

    Args:
        pdf_base64: Base64-encoded PDF file.

    Returns:
        Base64-encoded PDF/A file.
    """
    dg = _get_client()
    result = dg.pdf_tools.to_pdfa(base64.b64decode(pdf_base64))
    return base64.b64encode(result).decode()


@mcp.tool()
def rotate_pdf(pdf_base64: str, angle: int, pages: str | None = None) -> str:
    """Rotate pages in a PDF.

    Args:
        pdf_base64: Base64-encoded PDF file.
        angle: Rotation angle in degrees (90, 180, 270).
        pages: Page range to rotate (e.g. "1-3", "all"). Default: all pages.

    Returns:
        Base64-encoded rotated PDF.
    """
    dg = _get_client()
    result = dg.pdf_tools.rotate(base64.b64decode(pdf_base64), angle, pages)
    return base64.b64encode(result).decode()


# ─── PDF Forms ───────────────────────────────────────────────────────


@mcp.tool()
def inspect_pdf_form(pdf_base64: str) -> str:
    """Inspect form fields in a PDF and return their names, types, and current values.

    Args:
        pdf_base64: Base64-encoded PDF file with form fields.

    Returns:
        JSON array of form field definitions.
    """
    dg = _get_client()
    fields = dg.pdf_forms.inspect_fields(base64.b64decode(pdf_base64))
    from docgen._serialization import to_dict
    return json.dumps([to_dict(f) for f in fields])


@mcp.tool()
def fill_pdf_form(
    pdf_base64: str,
    fields: dict[str, str],
    flatten: bool = False,
) -> str:
    """Fill form fields in a PDF.

    Args:
        pdf_base64: Base64-encoded PDF file with form fields.
        fields: Field name-value pairs to fill.
        flatten: Whether to flatten the form (make fields non-editable).

    Returns:
        Base64-encoded filled PDF.
    """
    dg = _get_client()
    result = dg.fill_form(base64.b64decode(pdf_base64), fields, flatten)
    return base64.b64encode(result).decode()


# ─── Digital Signatures ──────────────────────────────────────────────


@mcp.tool()
def sign_pdf(
    pdf_base64: str,
    certificate_name: str,
    certificate_password: str,
    reason: str | None = None,
    location: str | None = None,
) -> str:
    """Digitally sign a PDF with a PKCS#12 certificate.

    Args:
        pdf_base64: Base64-encoded PDF to sign.
        certificate_name: Name of a pre-uploaded certificate.
        certificate_password: Password for the certificate.
        reason: Reason for signing.
        location: Location of signing.

    Returns:
        Base64-encoded signed PDF.
    """
    dg = _get_client()
    result = dg.signatures.sign(
        base64.b64decode(pdf_base64),
        certificate_name, certificate_password,
        reason=reason, location=location,
    )
    return base64.b64encode(result).decode()


@mcp.tool()
def verify_pdf_signatures(pdf_base64: str) -> str:
    """Verify digital signatures in a PDF.

    Args:
        pdf_base64: Base64-encoded signed PDF.

    Returns:
        JSON with verification results (signed, signatureCount, allValid, signatures).
    """
    dg = _get_client()
    result = dg.signatures.verify(base64.b64decode(pdf_base64))
    from docgen._serialization import to_dict
    return json.dumps(to_dict(result))


@mcp.tool()
def list_certificates() -> str:
    """List all uploaded signing certificates.

    Returns:
        JSON array of certificate info objects.
    """
    dg = _get_client()
    certs = dg.signatures.list_certificates()
    return json.dumps(certs)


# ─── Templates & Fonts ───────────────────────────────────────────────


@mcp.tool()
def list_templates() -> str:
    """List all uploaded document templates.

    Returns:
        JSON array of template info objects.
    """
    dg = _get_client()
    templates = dg.templates.list()
    return json.dumps(templates)


@mcp.tool()
def upload_template(template_base64: str, filename: str) -> str:
    """Upload a document template (ODT or DOCX).

    Args:
        template_base64: Base64-encoded template file.
        filename: Filename for the template (e.g. "invoice.odt").

    Returns:
        JSON with upload result.
    """
    dg = _get_client()
    result = dg.templates.upload(base64.b64decode(template_base64), filename)
    return json.dumps(result)


@mcp.tool()
def delete_template(name: str) -> str:
    """Delete a template by name.

    Args:
        name: Name of the template to delete.

    Returns:
        Confirmation message.
    """
    dg = _get_client()
    dg.templates.delete(name)
    return f"Template '{name}' deleted."


@mcp.tool()
def list_fonts() -> str:
    """List all uploaded custom fonts.

    Returns:
        JSON array of font info objects.
    """
    dg = _get_client()
    fonts = dg.fonts.list()
    return json.dumps(fonts)


# ─── Preview ─────────────────────────────────────────────────────────


@mcp.tool()
def preview_pdf_page(
    pdf_base64: str,
    page: int = 1,
    dpi: int = 150,
) -> str:
    """Render a PDF page as a PNG image preview.

    Args:
        pdf_base64: Base64-encoded PDF file.
        page: Page number (1-based, default: 1).
        dpi: Resolution in DPI (default: 150).

    Returns:
        Base64-encoded PNG image.
    """
    dg = _get_client()
    png = dg.preview.preview_page(base64.b64decode(pdf_base64), page, dpi)
    return base64.b64encode(png).decode()


@mcp.tool()
def get_pdf_page_count(pdf_base64: str) -> int:
    """Get the total number of pages in a PDF.

    Args:
        pdf_base64: Base64-encoded PDF file.

    Returns:
        Page count.
    """
    dg = _get_client()
    return dg.preview.page_count(base64.b64decode(pdf_base64))


# ─── ZUGFeRD ─────────────────────────────────────────────────────────


@mcp.tool()
def validate_zugferd(pdf_base64: str) -> str:
    """Validate a ZUGFeRD/Factur-X PDF for compliance.

    Args:
        pdf_base64: Base64-encoded PDF with embedded ZUGFeRD data.

    Returns:
        JSON validation result (valid, profile, errors, warnings).
    """
    dg = _get_client()
    result = dg.zugferd.validate(base64.b64decode(pdf_base64))
    from docgen._serialization import to_dict
    return json.dumps(to_dict(result))


@mcp.tool()
def extract_zugferd(pdf_base64: str) -> str:
    """Extract structured invoice data from a ZUGFeRD/Factur-X PDF.

    Args:
        pdf_base64: Base64-encoded ZUGFeRD PDF.

    Returns:
        JSON with extracted invoice data.
    """
    dg = _get_client()
    result = dg.zugferd.extract(base64.b64decode(pdf_base64))
    from docgen._serialization import to_dict
    return json.dumps(to_dict(result))


# ─── XRechnung ───────────────────────────────────────────────────────


@mcp.tool()
def validate_xrechnung(xml: str) -> str:
    """Validate XRechnung XML for compliance.

    Args:
        xml: XRechnung XML content.

    Returns:
        JSON validation result (valid, format, errors, warnings).
    """
    dg = _get_client()
    result = dg.xrechnung.validate(xml)
    from docgen._serialization import to_dict
    return json.dumps(to_dict(result))


@mcp.tool()
def parse_xrechnung(xml: str) -> str:
    """Parse XRechnung XML into structured invoice data.

    Args:
        xml: XRechnung XML content.

    Returns:
        JSON with parsed invoice data.
    """
    dg = _get_client()
    result = dg.xrechnung.parse(xml)
    from docgen._serialization import to_dict
    return json.dumps(to_dict(result))


@mcp.tool()
def detect_xrechnung(xml: str) -> str:
    """Detect if an XML document is an XRechnung and identify its format.

    Args:
        xml: XML content to analyze.

    Returns:
        JSON with detection result (detected, format, version).
    """
    dg = _get_client()
    result = dg.xrechnung.detect(xml)
    from docgen._serialization import to_dict
    return json.dumps(to_dict(result))


# ─── Excel ──────────────────────────────────────────────────────────


@mcp.tool()
def generate_excel(request: dict) -> str:
    """Generate an Excel workbook (.xlsx) from a structured JSON definition.

    The request dict should contain:
        sheets: List of sheet definitions, each with:
            name: Sheet tab name
            columns: Column definitions (header, width, format, align)
            rows: Data rows (list of dicts with 'values' or 'cells')
            formulas: List of formula definitions (cell, formula, label)
            headerFooter: Print header/footer configuration
            printArea: Print area in A1 notation
            freezePane: {row, col} for frozen panes
            headerStyle/dataStyle: Cell styling definitions
            autoSizeColumns, autoFilter, pageOrientation, fitToPage
        properties: Document properties (title, author, subject)
        password: Workbook protection password

    Args:
        request: Structured JSON definition of the Excel workbook.

    Returns:
        Base64-encoded XLSX file.
    """
    dg = _get_client()
    xlsx = dg.excel.generate(request)
    return base64.b64encode(xlsx).decode()


@mcp.tool()
def csv_to_excel(
    csv_content: str,
    delimiter: str = ",",
    has_header: bool = True,
    sheet_name: str | None = None,
) -> str:
    """Convert CSV content into a styled Excel workbook.

    Auto-formats with header styling, auto-filter, frozen header row, and auto-sized columns.

    Args:
        csv_content: Raw CSV text content.
        delimiter: CSV delimiter (default: comma).
        has_header: Whether the first row is a header (default: true).
        sheet_name: Name for the sheet tab (default: "Data").

    Returns:
        Base64-encoded XLSX file.
    """
    dg = _get_client()
    xlsx = dg.excel.from_csv(csv_content, delimiter=delimiter, has_header=has_header, sheet_name=sheet_name)
    return base64.b64encode(xlsx).decode()


@mcp.tool()
def excel_to_csv(
    excel_base64: str,
    sheet_index: int = 0,
    delimiter: str = ",",
) -> str:
    """Extract data from an Excel sheet and return it as CSV text.

    Args:
        excel_base64: Base64-encoded Excel file.
        sheet_index: Sheet index to extract (0-based, default: 0).
        delimiter: CSV delimiter (default: comma).

    Returns:
        CSV text content.
    """
    dg = _get_client()
    return dg.excel.to_csv(excel_base64, sheet_index=sheet_index, delimiter=delimiter)


@mcp.tool()
def excel_to_json(
    excel_base64: str,
    sheet_index: int = 0,
    has_header: bool = True,
) -> str:
    """Extract data from an Excel sheet and return structured JSON.

    Returns headers (if present) and typed data rows.

    Args:
        excel_base64: Base64-encoded Excel file.
        sheet_index: Sheet index to extract (0-based, default: 0).
        has_header: Whether the first row is a header (default: true).

    Returns:
        JSON with sheetName, totalRows, headers, and data array.
    """
    dg = _get_client()
    result = dg.excel.to_json(excel_base64, sheet_index=sheet_index, has_header=has_header)
    return json.dumps(result)


@mcp.tool()
def fill_excel_template(
    template_base64: str,
    values: dict[str, Any] | None = None,
    tables: dict[str, list[list[Any]]] | None = None,
    recalculate: bool = True,
) -> str:
    """Fill an Excel template with data at named cells and ranges.

    Args:
        template_base64: Base64-encoded Excel template file.
        values: Cell values to set (key = cell ref like 'Sheet1!A1' or named range, value = content).
        tables: Table data to insert at named ranges (key = range name, value = row arrays).
        recalculate: Recalculate formulas after filling (default: true).

    Returns:
        Base64-encoded filled XLSX file.
    """
    dg = _get_client()
    xlsx = dg.excel.fill_template(
        template_base64, values=values, tables=tables, recalculate=recalculate
    )
    return base64.b64encode(xlsx).decode()


@mcp.tool()
def inspect_excel(excel_base64: str) -> str:
    """Inspect an Excel workbook and return metadata.

    Returns sheet names, row/column counts, and named ranges.

    Args:
        excel_base64: Base64-encoded Excel file.

    Returns:
        JSON with sheetCount, sheets array, and namedRanges.
    """
    dg = _get_client()
    result = dg.excel.inspect(excel_base64)
    return json.dumps(result)


# ─── Server Entry Point ──────────────────────────────────────────────


def main():
    """Run the DocGen MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
