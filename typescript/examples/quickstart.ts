import { writeFileSync } from "node:fs";
import {
  DocGen,
  InvoiceUnit,
  TextAlignment,
  type ColumnDef,
  type TableData,
} from "../src/index.js";

const dg = new DocGen({ apiKey: "dk_live_xxx" });

// ── Simple HTML to PDF ──────────────────────────────────────────────

async function simpleHtmlToPdf() {
  const pdf = await dg.htmlToPdf("<h1>Hello World</h1><p>Generated with DocGen.</p>");
  writeFileSync("hello.pdf", pdf);
  console.log(`Generated hello.pdf (${pdf.length} bytes)`);
}

// ── Markdown to PDF ─────────────────────────────────────────────────

async function markdownToPdf() {
  const pdf = await dg.markdownToPdf(`
# Project Report

## Summary

This report was **automatically generated** using the DocGen SDK.

### Key Findings

- Finding 1: Performance improved by 25%
- Finding 2: Error rate reduced to 0.1%
- Finding 3: User satisfaction up to 4.8/5
`);
  writeFileSync("report.pdf", pdf);
}

// ── Builder with Template ───────────────────────────────────────────

async function builderWithTemplate() {
  const pdf = await dg
    .document()
    .html("<h1>Rechnung {{invoice_nr}}</h1><p>{{body}}</p>")
    .template("invoice-template.odt")
    .field("invoice_nr", "RE-2026-042")
    .field("date", "12.04.2026")
    .field("body", "Vielen Dank für Ihren Auftrag.")
    .watermark("ENTWURF")
    .asPdf()
    .generate();
  writeFileSync("invoice.pdf", pdf);
}

// ── Builder with Table and QR Code ──────────────────────────────────

async function builderWithTableAndQr() {
  const columns: ColumnDef[] = [
    { header: "Position", width: 15, alignment: TextAlignment.CENTER },
    { header: "Artikel", width: 80 },
    { header: "Menge", width: 20, alignment: TextAlignment.RIGHT },
    { header: "Preis", width: 25, alignment: TextAlignment.RIGHT },
  ];

  const table: TableData = {
    columns,
    rows: [
      ["1", "Widget Pro", "10", "99,90 €"],
      ["2", "Gadget Plus", "5", "149,50 €"],
      ["3", "Tool Basic", "20", "29,80 €"],
    ],
  };

  const pdf = await dg
    .document()
    .html("<h1>Bestellung</h1>")
    .template("order-template.odt")
    .table("items", table)
    .qrCode("payment_qr", "BCD\n002\n1\nSCT\nCOBADEFFXXX\nACME GmbH\nDE89370400440532013000\nEUR279.20")
    .asPdf()
    .generate();
  writeFileSync("order.pdf", pdf);
}

// ── Invoice with ZUGFeRD ────────────────────────────────────────────

async function invoiceWithZugferd() {
  const invoice = dg
    .invoice()
    .number("RE-2026-042")
    .date("2026-04-12")
    .seller({
      name: "ACME GmbH",
      street: "Musterstraße 1",
      zip: "10115",
      city: "Berlin",
      country: "DE",
      vatId: "DE123456789",
    })
    .buyer({
      name: "Kunde AG",
      street: "Kundenweg 5",
      zip: "20095",
      city: "Hamburg",
      country: "DE",
    })
    .item({ description: "Beratungsleistung", quantity: 8, unit: InvoiceUnit.HOUR, unitPrice: 120.0 })
    .item({ description: "Reisekosten (pauschal)", unitPrice: 250.0 })
    .bank({ iban: "DE89370400440532013000", bic: "COBADEFFXXX", accountHolder: "ACME GmbH" })
    .paymentTerms("Zahlbar innerhalb 14 Tagen ohne Abzug")
    .dueDate("2026-04-26")
    .build();

  const pdf = await dg
    .document()
    .html("<h1>Rechnung RE-2026-042</h1>")
    .template("invoice-template.odt")
    .field("invoice_nr", "RE-2026-042")
    .field("date", "12.04.2026")
    .invoice(invoice)
    .asPdf()
    .generate();
  writeFileSync("zugferd-invoice.pdf", pdf);
}

// ── Multi-Part Compose ──────────────────────────────────────────────

async function composeMultiPart() {
  const pdf = await dg
    .compose()
    .part({ htmlContent: "<h1>Deckblatt</h1><p>Jahresbericht 2025</p>" })
    .part({ htmlContent: "<h1>Kapitel 1</h1><p>...</p>", templateName: "report-template.odt" })
    .part({ htmlContent: "<h1>Kapitel 2</h1><p>...</p>", templateName: "report-template.odt" })
    .watermark("VERTRAULICH")
    .asPdf()
    .generate();
  writeFileSync("jahresbericht.pdf", pdf);
}

// ── PDF Operations ──────────────────────────────────────────────────

async function pdfOperations() {
  // Merge PDFs
  const merged = await dg.mergePdfs(["part1.pdf", "part2.pdf", "appendix.pdf"]);
  writeFileSync("merged.pdf", merged);

  // Extract text
  const text = await dg.pdfTools.extractText("document.pdf");
  console.log(`Extracted text: ${text.slice(0, 200)}...`);

  // Fill form
  const filled = await dg.fillForm("form.pdf", {
    name: "Max Mustermann",
    date: "12.04.2026",
  }, true);
  writeFileSync("filled-form.pdf", filled);
}

// ── Run ─────────────────────────────────────────────────────────────

simpleHtmlToPdf().catch(console.error);
