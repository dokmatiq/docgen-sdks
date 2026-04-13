using Dokmatiq.DocGen;
using Dokmatiq.DocGen.Builders;
using Dokmatiq.DocGen.Models;
using Dokmatiq.DocGen.Webhook;

// ── 1. One-liner: HTML to PDF ──────────────────────────────────────

using var dg = new DocGenClient("dk_live_YOUR_API_KEY");

byte[] simplePdf = dg.HtmlToPdf("<h1>Hello from .NET!</h1><p>Generated with DocGen.</p>");
File.WriteAllBytes("hello.pdf", simplePdf);

// ── 2. Fluent builder with template ────────────────────────────────

byte[] invoice = dg.Document()
    .Html("<h1>Rechnung {{nr}}</h1><p>Kunde: {{kunde}}</p>")
    .Template("invoice.odt")
    .Field("nr", "RE-2026-042")
    .Field("kunde", "ACME GmbH")
    .Watermark("ENTWURF")
    .AsPdf()
    .Generate();
File.WriteAllBytes("invoice.pdf", invoice);

// ── 3. Multi-part composition ──────────────────────────────────────

byte[] report = dg.Compose()
    .Part(new DocumentPart("<h1>Cover Page</h1>"))
    .Part(new DocumentPart("<h1>Chapter 1</h1><p>Content here...</p>"))
    .Part(new DocumentPart("<h1>Chapter 2</h1><p>More content...</p>"))
    .AsPdf()
    .Generate();
File.WriteAllBytes("report.pdf", report);

// ── 4. ZUGFeRD e-invoice ───────────────────────────────────────────

var invoiceData = dg.Invoice()
    .Number("RE-2026-042")
    .Date("2026-04-13")
    .Seller(Party.Builder("ACME GmbH")
        .Street("Musterstr. 1").Zip("10115").City("Berlin")
        .VatId("DE123456789").Build())
    .Buyer(Party.Builder("Kunde AG")
        .Street("Kundenweg 5").Zip("20095").City("Hamburg").Build())
    .Item(InvoiceItem.Builder("Softwareentwicklung", 150.0)
        .Quantity(40).Unit(InvoiceUnit.HOUR).VatRate(19.0).Build())
    .Item("Hosting (monatlich)", 49.99)
    .Bank(new BankAccount("DE89370400440532013000"))
    .DueDate("2026-05-13")
    .Build();

byte[] zugferdPdf = dg.Zugferd.Embed("invoice.pdf", invoiceData);
File.WriteAllBytes("zugferd-invoice.pdf", zugferdPdf);

// ── 5. PDF tools ───────────────────────────────────────────────────

byte[] merged = dg.MergePdfs(new[] { "part1.pdf", "part2.pdf" });
string text = dg.PdfTools.ExtractText("document.pdf");
byte[] pdfA = dg.PdfTools.ToPdfA("document.pdf");

// ── 6. Excel generation ────────────────────────────────────────────

var excelRequest = new Dictionary<string, object>
{
    ["sheets"] = new[]
    {
        new Dictionary<string, object>
        {
            ["name"] = "Umsätze",
            ["columns"] = new[]
            {
                new { header = "Monat", width = 15 },
                new { header = "Umsatz", width = 12, format = "#,##0.00 €" },
                new { header = "Gewinn", width = 12, format = "#,##0.00 €" }
            },
            ["rows"] = new[]
            {
                new { values = new object[] { "Januar", 42500.0, 8500.0 } },
                new { values = new object[] { "Februar", 38900.0, 7200.0 } },
                new { values = new object[] { "März", 51200.0, 11800.0 } }
            }
        }
    }
};
byte[] xlsx = dg.Excel.Generate(excelRequest);
File.WriteAllBytes("report.xlsx", xlsx);

// ── 7. Webhook verification ────────────────────────────────────────

// In your ASP.NET endpoint:
// var payload = WebhookVerifier.Verify(requestBody, signatureHeader, "your-secret");
// Console.WriteLine($"Job {payload.JobId} → {payload.Status}");

Console.WriteLine("All examples completed!");
