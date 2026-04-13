"""Quick start examples for the DocGen Python SDK."""

from pathlib import Path

from docgen import (
    DocGen,
    ColumnDef,
    ContentArea,
    DocumentPart,
    InvoiceBuilder,
    InvoiceUnit,
    OutputFormat,
    PageOrientation,
    PageSettings,
    QrCodeData,
    TableData,
    TextAlignment,
    WatermarkConfig,
)


def simple_html_to_pdf():
    """Convert HTML to PDF in one line."""
    dg = DocGen(api_key="dk_live_xxx")
    pdf = dg.html_to_pdf("<h1>Hello World</h1><p>Generated with DocGen.</p>")
    Path("hello.pdf").write_bytes(pdf)
    print(f"Generated hello.pdf ({len(pdf)} bytes)")


def markdown_to_pdf():
    """Convert Markdown to PDF."""
    dg = DocGen(api_key="dk_live_xxx")
    pdf = dg.markdown_to_pdf("""
# Project Report

## Summary

This report was **automatically generated** using the DocGen SDK.

### Key Findings

- Finding 1: Performance improved by 25%
- Finding 2: Error rate reduced to 0.1%
- Finding 3: User satisfaction up to 4.8/5

> The results exceeded all expectations.
""")
    Path("report.pdf").write_bytes(pdf)


def builder_with_template():
    """Use the fluent builder with a template."""
    with DocGen(api_key="dk_live_xxx") as dg:
        pdf = (dg.document()
            .html("<h1>Rechnung {{invoice_nr}}</h1><p>{{body}}</p>")
            .template("invoice-template.odt")
            .field("invoice_nr", "RE-2026-042")
            .field("date", "12.04.2026")
            .field("body", "Vielen Dank für Ihren Auftrag.")
            .watermark("ENTWURF")
            .as_pdf()
            .generate())
        Path("invoice.pdf").write_bytes(pdf)


def builder_with_table_and_qr():
    """Builder with table data and QR code."""
    with DocGen(api_key="dk_live_xxx") as dg:
        pdf = (dg.document()
            .html("<h1>Bestellung</h1>")
            .template("order-template.odt")
            .table("items", TableData(
                columns=[
                    ColumnDef("Position", width=15, alignment=TextAlignment.CENTER),
                    ColumnDef("Artikel", width=80),
                    ColumnDef("Menge", width=20, alignment=TextAlignment.RIGHT),
                    ColumnDef("Preis", width=25, alignment=TextAlignment.RIGHT),
                ],
                rows=[
                    ["1", "Widget Pro", "10", "99,90 €"],
                    ["2", "Gadget Plus", "5", "149,50 €"],
                    ["3", "Tool Basic", "20", "29,80 €"],
                ],
            ))
            .qr_code("payment_qr", "BCD\n002\n1\nSCT\nCOBADEFFXXX\nACME GmbH\nDE89370400440532013000\nEUR279.20\n\n\nBestellung 2026-042")
            .as_pdf()
            .generate())
        Path("order.pdf").write_bytes(pdf)


def invoice_with_zugferd():
    """Generate an invoice with embedded ZUGFeRD data."""
    with DocGen(api_key="dk_live_xxx") as dg:
        # Build structured invoice data
        invoice = (dg.invoice()
            .number("RE-2026-042")
            .date("2026-04-12")
            .seller(
                name="ACME GmbH",
                street="Musterstraße 1",
                zip="10115",
                city="Berlin",
                country="DE",
                vat_id="DE123456789",
                email="rechnung@acme.de",
            )
            .buyer(
                name="Kunde AG",
                street="Kundenweg 5",
                zip="20095",
                city="Hamburg",
                country="DE",
                vat_id="DE987654321",
            )
            .item("Beratungsleistung", quantity=8, unit=InvoiceUnit.HOUR, unit_price=120.0)
            .item("Reisekosten (pauschal)", unit_price=250.0)
            .bank(iban="DE89370400440532013000", bic="COBADEFFXXX", holder="ACME GmbH")
            .payment_terms("Zahlbar innerhalb 14 Tagen ohne Abzug")
            .due_date("2026-04-26")
            .build())

        # Generate invoice PDF with embedded ZUGFeRD XML
        pdf = (dg.document()
            .html("<h1>Rechnung RE-2026-042</h1>")
            .template("invoice-template.odt")
            .field("invoice_nr", "RE-2026-042")
            .field("date", "12.04.2026")
            .invoice(invoice)
            .as_pdf()
            .generate())
        Path("zugferd-invoice.pdf").write_bytes(pdf)


def compose_multi_part():
    """Compose a multi-part document."""
    with DocGen(api_key="dk_live_xxx") as dg:
        pdf = (dg.compose()
            .part(DocumentPart(
                html_content="<h1>Deckblatt</h1><p>Jahresbericht 2025</p>",
                page_settings=PageSettings(orientation=PageOrientation.PORTRAIT),
            ))
            .part(DocumentPart(
                html_content="<h1>Kapitel 1: Einleitung</h1><p>...</p>",
                template_name="report-template.odt",
            ))
            .part(DocumentPart(
                html_content="<h1>Kapitel 2: Ergebnisse</h1><p>...</p>",
                template_name="report-template.odt",
            ))
            .watermark("VERTRAULICH")
            .as_pdf()
            .generate())
        Path("jahresbericht.pdf").write_bytes(pdf)


def pdf_operations():
    """Common PDF operations."""
    with DocGen(api_key="dk_live_xxx") as dg:
        # Merge PDFs
        merged = dg.merge_pdfs([
            Path("part1.pdf"),
            Path("part2.pdf"),
            Path("appendix.pdf"),
        ])
        Path("merged.pdf").write_bytes(merged)

        # Extract text
        text = dg.pdf_tools.extract_text(Path("document.pdf"))
        print(f"Extracted text: {text[:200]}...")

        # Get page count
        pages = dg.preview.page_count(Path("document.pdf"))
        print(f"Document has {pages} pages")

        # Fill a PDF form
        filled = dg.fill_form(
            Path("form.pdf"),
            fields={"name": "Max Mustermann", "date": "12.04.2026"},
            flatten=True,
        )
        Path("filled-form.pdf").write_bytes(filled)


def content_areas_example():
    """Place content at absolute positions on the PDF."""
    with DocGen(api_key="dk_live_xxx") as dg:
        pdf = (dg.document()
            .html("<h1>Dokument mit positioniertem Inhalt</h1><p>Haupttext...</p>")
            .content_area(ContentArea(
                x=150, y=10, width=50,
                text="**Dokument-ID:** DOC-2026-042",
                font_size=8, color="#666666",
                pages="all",
            ))
            .content_area(ContentArea(
                x=10, y=280, width=190,
                text="ACME GmbH · Musterstraße 1 · 10115 Berlin · www.acme.de",
                font_size=7, color="#999999",
                alignment=TextAlignment.CENTER,
                pages="all",
            ))
            .as_pdf()
            .generate())
        Path("positioned.pdf").write_bytes(pdf)


if __name__ == "__main__":
    simple_html_to_pdf()
