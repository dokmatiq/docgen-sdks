# DocGen .NET SDK

Official .NET SDK for the [DocGen](https://dokmatiq.com) document generation platform.

[![NuGet](https://img.shields.io/nuget/v/Dokmatiq.DocGen)](https://www.nuget.org/packages/Dokmatiq.DocGen)
[![.NET 8+](https://img.shields.io/badge/.NET-8.0%2B-blue)](https://dotnet.microsoft.com)

## Installation

```bash
dotnet add package Dokmatiq.DocGen
```

## Quick Start

```csharp
using Dokmatiq.DocGen;

using var dg = new DocGenClient("dk_live_YOUR_API_KEY");

// One-liner: HTML → PDF
byte[] pdf = dg.HtmlToPdf("<h1>Hello World</h1>");
File.WriteAllBytes("hello.pdf", pdf);
```

## Features

| Feature | Description |
|---------|-------------|
| **Document Generation** | HTML, Markdown, templates → PDF, DOCX, ODT |
| **Multi-Part Composition** | Combine multiple document parts into one |
| **Excel Workbooks** | Generate XLSX with styling, formulas, charts |
| **PDF Tools** | Merge, split, rotate, extract text, PDF/A |
| **Digital Signatures** | Sign and verify PDFs with PKCS#12 certificates |
| **PDF Forms** | Inspect and fill form fields |
| **ZUGFeRD / Factur-X** | Embed/extract e-invoice data in PDFs |
| **XRechnung** | Generate, parse, validate German e-invoices |
| **Templates** | Upload and manage ODT/DOCX templates |
| **Fonts** | Upload custom fonts (TTF/OTF) |
| **Webhooks** | Secure HMAC-SHA256 signature verification |

## Fluent Document Builder

```csharp
byte[] pdf = dg.Document()
    .Html("<h1>Invoice {{nr}}</h1>")
    .Template("invoice.odt")
    .Field("nr", "RE-2026-001")
    .Field("customer", "ACME GmbH")
    .Image("logo", "logo.png")
    .QrCode("payment_qr", "https://pay.example.com/inv/2026-001")
    .Watermark("DRAFT")
    .AsPdf()
    .Generate();
```

## E-Invoicing (ZUGFeRD / XRechnung)

```csharp
var invoice = dg.Invoice()
    .Number("RE-2026-001")
    .Date("2026-04-13")
    .Seller(Party.Builder("ACME GmbH")
        .Street("Musterstr. 1").Zip("10115").City("Berlin")
        .VatId("DE123456789").Build())
    .Buyer(Party.Builder("Kunde AG")
        .Street("Kundenweg 5").Zip("20095").City("Hamburg").Build())
    .Item(InvoiceItem.Builder("Consulting", 150.0)
        .Quantity(8).Unit(InvoiceUnit.HOUR).Build())
    .Bank(new BankAccount("DE89370400440532013000"))
    .Build();

// Embed ZUGFeRD data into PDF
byte[] zugferd = dg.Zugferd.Embed("invoice.pdf", invoice);

// Generate XRechnung XML
string xml = dg.XRechnung.Generate(invoice);
```

## Excel Workbooks

```csharp
var request = new Dictionary<string, object>
{
    ["sheets"] = new[]
    {
        new Dictionary<string, object>
        {
            ["name"] = "Sales",
            ["columns"] = new[]
            {
                new { header = "Month", width = 15 },
                new { header = "Revenue", width = 12, format = "#,##0.00 €" }
            },
            ["rows"] = new[]
            {
                new { values = new object[] { "January", 42500.0 } },
                new { values = new object[] { "February", 38900.0 } }
            }
        }
    }
};
byte[] xlsx = dg.Excel.Generate(request);

// CSV → Excel
byte[] fromCsv = dg.Excel.FromCsv(csvContent);

// Excel → JSON
var data = dg.Excel.ToJson(excelBase64);
```

## PDF Tools

```csharp
// Merge PDFs
byte[] merged = dg.MergePdfs(new[] { "part1.pdf", "part2.pdf" });

// Extract text
string text = dg.PdfTools.ExtractText("document.pdf");

// Convert to PDF/A
byte[] pdfA = dg.PdfTools.ToPdfA("document.pdf");

// Digital signature
byte[] signed = dg.SignPdf("contract.pdf", "my-cert", "cert-password");
```

## Multi-Part Composition

```csharp
byte[] report = dg.Compose()
    .Part(new DocumentPart("<h1>Cover</h1>"))
    .Part(new DocumentPart("<h1>Chapter 1</h1>", "report.odt"))
    .Watermark("CONFIDENTIAL")
    .AsPdf()
    .Generate();
```

## Async Generation

```csharp
// Submit job
var job = dg.Documents.SubmitAsync(request);
Console.WriteLine($"Job ID: {job.JobId}");

// Poll until done
byte[] result = dg.Documents.WaitForJob(job.JobId);

// Or with custom timeout
byte[] result2 = dg.Documents.WaitForJob(job.JobId,
    pollInterval: TimeSpan.FromSeconds(5),
    timeout: TimeSpan.FromMinutes(5));
```

## Webhook Verification

```csharp
using Dokmatiq.DocGen.Webhook;

// In your ASP.NET endpoint
[HttpPost("/webhooks/docgen")]
public IActionResult HandleWebhook(
    [FromBody] string body,
    [FromHeader(Name = "X-DocGen-Signature")] string signature)
{
    var payload = WebhookVerifier.Verify(body, signature, "your-secret");
    Console.WriteLine($"Job {payload.JobId} → {payload.Status}");
    return Ok();
}
```

## Configuration

```csharp
var config = new DocGenConfig("dk_live_xxx")
{
    BaseUrl = "https://api.dokmatiq.com",
    Timeout = TimeSpan.FromSeconds(120),
    ValidateMode = "strict",
    Retry = new RetryPolicy
    {
        MaxRetries = 5,
        InitialDelay = TimeSpan.FromSeconds(1),
        BackoffMultiplier = 2.0,
        MaxDelay = TimeSpan.FromSeconds(60)
    }
};

using var dg = new DocGenClient(config);
```

## Error Handling

```csharp
using Dokmatiq.DocGen.Exceptions;

try
{
    byte[] pdf = dg.HtmlToPdf("<h1>Test</h1>");
}
catch (ValidationException ex)
{
    Console.WriteLine($"Validation: {ex.Message}");
    foreach (var (field, error) in ex.FieldErrors ?? new())
        Console.WriteLine($"  {field}: {error}");
    if (ex.Hint is not null) Console.WriteLine($"Hint: {ex.Hint}");
}
catch (RateLimitException ex)
{
    Console.WriteLine($"Rate limited. Retry after {ex.RetryAfter}s");
}
catch (AuthenticationException)
{
    Console.WriteLine("Invalid API key");
}
catch (DocGenException ex)
{
    Console.WriteLine($"DocGen error: {ex.Message}");
}
```

## Requirements

- .NET 8.0 or later
- API key from [developer.dokmatiq.com](https://developer.dokmatiq.com)

## License

MIT - see [LICENSE](../LICENSE)
