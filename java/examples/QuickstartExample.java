import com.dokmatiq.docgen.DocGen;
import com.dokmatiq.docgen.DocGenConfig;
import com.dokmatiq.docgen.builder.InvoiceBuilder;
import com.dokmatiq.docgen.model.*;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/**
 * Quick start examples for the DocGen Java SDK.
 */
public class QuickstartExample {

    public static void main(String[] args) throws Exception {
        simpleHtmlToPdf();
    }

    static void simpleHtmlToPdf() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            byte[] pdf = dg.htmlToPdf("<h1>Hello World</h1><p>Generated with DocGen.</p>");
            Files.write(Path.of("hello.pdf"), pdf);
            System.out.println("Generated hello.pdf (" + pdf.length + " bytes)");
        }
    }

    static void markdownToPdf() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            byte[] pdf = dg.markdownToPdf("""
                # Project Report

                ## Summary

                This report was **automatically generated** using the DocGen SDK.

                ### Key Findings

                - Performance improved by 25%
                - Error rate reduced to 0.1%
                - User satisfaction up to 4.8/5
                """);
            Files.write(Path.of("report.pdf"), pdf);
        }
    }

    static void builderWithTemplate() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            byte[] pdf = dg.document()
                    .html("<h1>Rechnung {{invoice_nr}}</h1><p>{{body}}</p>")
                    .template("invoice-template.odt")
                    .field("invoice_nr", "RE-2026-042")
                    .field("date", "12.04.2026")
                    .field("body", "Vielen Dank für Ihren Auftrag.")
                    .watermark("ENTWURF")
                    .asPdf()
                    .generate();
            Files.write(Path.of("invoice.pdf"), pdf);
        }
    }

    static void builderWithTableAndQr() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            var table = new TableData(
                    List.of(
                            new ColumnDef("Position", 15, TextAlignment.CENTER),
                            new ColumnDef("Artikel", 80),
                            new ColumnDef("Menge", 20, TextAlignment.RIGHT),
                            new ColumnDef("Preis", 25, TextAlignment.RIGHT)
                    ),
                    List.of(
                            List.of("1", "Widget Pro", "10", "99,90 €"),
                            List.of("2", "Gadget Plus", "5", "149,50 €"),
                            List.of("3", "Tool Basic", "20", "29,80 €")
                    )
            );

            byte[] pdf = dg.document()
                    .html("<h1>Bestellung</h1>")
                    .template("order-template.odt")
                    .table("items", table)
                    .qrCode("payment_qr", "BCD\n002\n1\nSCT\nCOBADEFFXXX\nACME GmbH\nDE89370400440532013000\nEUR279.20")
                    .asPdf()
                    .generate();
            Files.write(Path.of("order.pdf"), pdf);
        }
    }

    static void invoiceWithZugferd() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            InvoiceData invoice = dg.invoice()
                    .number("RE-2026-042")
                    .date("2026-04-12")
                    .seller(Party.builder("ACME GmbH")
                            .street("Musterstraße 1").zip("10115").city("Berlin")
                            .country("DE").vatId("DE123456789").build())
                    .buyer(Party.builder("Kunde AG")
                            .street("Kundenweg 5").zip("20095").city("Hamburg")
                            .country("DE").build())
                    .item(InvoiceItem.builder("Beratungsleistung", 120.0)
                            .quantity(8).unit(InvoiceUnit.HOUR).build())
                    .item("Reisekosten (pauschal)", 250.0)
                    .bank(new BankAccount("DE89370400440532013000", "COBADEFFXXX", "ACME GmbH"))
                    .paymentTerms("Zahlbar innerhalb 14 Tagen ohne Abzug")
                    .dueDate("2026-04-26")
                    .build();

            byte[] pdf = dg.document()
                    .html("<h1>Rechnung RE-2026-042</h1>")
                    .template("invoice-template.odt")
                    .field("invoice_nr", "RE-2026-042")
                    .invoice(invoice)
                    .asPdf()
                    .generate();
            Files.write(Path.of("zugferd-invoice.pdf"), pdf);
        }
    }

    static void composeMultiPart() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            byte[] pdf = dg.compose()
                    .part(new DocumentPart("<h1>Deckblatt</h1><p>Jahresbericht 2025</p>"))
                    .part(new DocumentPart("<h1>Kapitel 1</h1><p>...</p>", "report-template.odt"))
                    .part(new DocumentPart("<h1>Kapitel 2</h1><p>...</p>", "report-template.odt"))
                    .watermark("VERTRAULICH")
                    .asPdf()
                    .generate();
            Files.write(Path.of("jahresbericht.pdf"), pdf);
        }
    }

    static void pdfOperations() throws Exception {
        try (var dg = new DocGen("dk_live_xxx")) {
            // Merge
            byte[] merged = dg.mergePdfs(List.of(
                    Path.of("part1.pdf"), Path.of("part2.pdf")));
            Files.write(Path.of("merged.pdf"), merged);

            // Extract text
            String text = dg.pdfTools().extractText(Path.of("document.pdf"));
            System.out.println("Extracted: " + text.substring(0, Math.min(200, text.length())));

            // Fill form
            byte[] filled = dg.fillForm(Path.of("form.pdf"),
                    java.util.Map.of("name", "Max Mustermann", "date", "12.04.2026"), true);
            Files.write(Path.of("filled-form.pdf"), filled);
        }
    }
}
