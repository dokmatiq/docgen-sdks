# Dokmatiq DocGen Java SDK

[![CI](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-java.yml/badge.svg)](https://github.com/dokmatiq/docgen-sdks/actions/workflows/ci-java.yml)

Java SDK for the [Dokmatiq DocGen](https://dokmatiq.com) document generation API. Generate PDF, DOCX, and ODT documents from HTML/Markdown with templates, e-invoicing (ZUGFeRD/XRechnung), digital signatures, and more.

## Installation

### Maven

```xml
<dependency>
    <groupId>com.dokmatiq</groupId>
    <artifactId>docgen-sdk</artifactId>
    <version>0.1.0</version>
</dependency>
```

### Gradle

```groovy
implementation 'com.dokmatiq:docgen-sdk:0.1.0'
```

## Quick Start

```java
try (var dg = new DocGen("dk_live_xxx")) {
    // One-liner: HTML to PDF
    byte[] pdf = dg.htmlToPdf("<h1>Hello World</h1>");

    // Markdown to PDF
    byte[] report = dg.markdownToPdf("# Report\n\n**Summary**: ...");
}
```

## Builder Pattern

For complex documents, use the fluent builder:

```java
try (var dg = new DocGen("dk_live_xxx")) {
    byte[] pdf = dg.document()
        .html("<h1>Rechnung {{nr}}</h1>")
        .template("invoice.odt")
        .field("nr", "RE-2026-001")
        .field("datum", "12.04.2026")
        .table("positionen", new TableData(
            List.of(
                new ColumnDef("Artikel", 80),
                new ColumnDef("Preis", 30, TextAlignment.RIGHT)
            ),
            List.of(
                List.of("Widget", "9.99 €"),
                List.of("Gadget", "24.99 €")
            )
        ))
        .qrCode("payment", "BCD\n002\n1\nSCT\n...")
        .watermark("ENTWURF")
        .asPdf()
        .generate();
}
```

## E-Invoicing (ZUGFeRD / XRechnung)

```java
try (var dg = new DocGen("dk_live_xxx")) {
    InvoiceData invoice = dg.invoice()
        .number("RE-2026-001")
        .date("2026-04-12")
        .seller(Party.builder("ACME GmbH")
            .street("Musterstr. 1").zip("10115").city("Berlin")
            .vatId("DE123456789").build())
        .buyer(Party.builder("Kunde AG")
            .street("Kundenweg 5").zip("20095").city("Hamburg").build())
        .item(InvoiceItem.builder("Beratung", 120.0)
            .quantity(8).unit(InvoiceUnit.HOUR).build())
        .item("Reisekosten", 250.0)
        .bank(new BankAccount("DE89370400440532013000", "COBADEFFXXX", "ACME GmbH"))
        .paymentTerms("Zahlbar innerhalb 14 Tagen")
        .build();

    byte[] pdf = dg.document()
        .html("<h1>Rechnung RE-2026-001</h1>")
        .template("invoice.odt")
        .invoice(invoice)
        .asPdf()
        .generate();
}
```

## PDF Operations

```java
try (var dg = new DocGen("dk_live_xxx")) {
    // Merge PDFs
    byte[] merged = dg.mergePdfs(List.of(Path.of("part1.pdf"), Path.of("part2.pdf")));

    // Fill form fields
    byte[] filled = dg.fillForm(Path.of("form.pdf"),
        Map.of("name", "Max", "date", "12.04.2026"), true);

    // Sign PDF
    byte[] signed = dg.signPdf(Path.of("doc.pdf"), "my-cert.p12", "password123");

    // Extract text
    String text = dg.pdfTools().extractText(Path.of("document.pdf"));

    // Preview page as image
    byte[] png = dg.preview().previewPage(Path.of("document.pdf"), 1, 300);
}
```

## Async Jobs

```java
try (var dg = new DocGen("dk_live_xxx")) {
    JobInfo job = dg.documents().generateAsync(request);
    byte[] pdf = dg.documents().waitForJob(job.jobId(), 2000, 120_000);
}
```

## Configuration

```java
var config = DocGenConfig.builder("dk_live_xxx")
    .baseUrl("https://api.dokmatiq.com")
    .timeout(Duration.ofSeconds(60))
    .retry(new DocGenConfig.RetryPolicy(5, Duration.ofSeconds(1), 2.0, Duration.ofSeconds(30)))
    .validateMode("strict")  // "strict" | "warn" | null
    .build();

try (var dg = new DocGen(config)) {
    // ...
}
```

## Error Handling

```java
import com.dokmatiq.docgen.exception.*;

try {
    byte[] pdf = dg.htmlToPdf("<h1>Hello</h1>");
} catch (AuthenticationException e) {
    System.out.println("Invalid API key");
} catch (ValidationException e) {
    System.out.println("Validation failed: " + e.getMessage());
    System.out.println("Field errors: " + e.fieldErrors());
    System.out.println("Hint: " + e.hint());
} catch (RateLimitException e) {
    System.out.println("Rate limited. Retry after " + e.retryAfter() + "s");
}
```

## Webhook Verification

```java
import com.dokmatiq.docgen.webhook.WebhookVerifier;

WebhookPayload payload = WebhookVerifier.verify(requestBody, signatureHeader, secret);
System.out.println("Job " + payload.jobId() + " completed: " + payload.status());
```

## Excel Workbooks

```java
try (var dg = new DocGen("dk_live_xxx")) {
    // Generate XLSX from structured data
    byte[] xlsx = dg.excel().generate(Map.of(
        "sheets", List.of(Map.of(
            "name", "Sales",
            "columns", List.of(
                Map.of("header", "Month", "width", 15),
                Map.of("header", "Revenue", "width", 12, "format", "#,##0.00 €")
            ),
            "rows", List.of(
                Map.of("values", List.of("January", 42500.0)),
                Map.of("values", List.of("February", 38900.0))
            )
        ))
    ));

    // CSV → XLSX
    byte[] fromCsv = dg.excel().fromCsv(csvContent);

    // XLSX → JSON
    Map<String, Object> data = dg.excel().toJson(excelBase64);
}
```

## Receipt Recognition (AI)

Extract structured data from receipts, tickets, and invoices using AI vision:

```java
try (var dg = new DocGen("dk_live_xxx")) {
    // Extract data from a receipt image
    byte[] imageBytes = Files.readAllBytes(Path.of("kassenbeleg.jpg"));
    Map<String, Object> result = dg.receipts().extract(imageBytes, "kassenbeleg.jpg");

    Map<String, Object> data = (Map<String, Object>) result.get("receiptData");
    System.out.println(data.get("totalAmount"));   // 42.50
    System.out.println(data.get("receiptType"));    // "cash_receipt"
    System.out.println(data.get("skr03Account"));   // "4650"

    // Export as DATEV-compatible CSV
    byte[] csv = dg.receipts().exportCsv(List.of(data));

    // Async extraction with webhook
    Map<String, Object> job = dg.receipts().extractAsync(imageBytes, "beleg.jpg",
        "https://my-app.com/webhooks/receipts", "my-secret");
}
```

> **Note:** Requires AI processing consent in the [Developer Portal](https://developer.dokmatiq.com) settings (GDPR).

## Sub-Clients

| Client | Access | Description |
|--------|--------|-------------|
| `dg.documents()` | Document generation, compose, async jobs |
| `dg.templates()` | Template upload, list, delete |
| `dg.fonts()` | Font upload, list, delete |
| `dg.pdfForms()` | Form field inspection and filling |
| `dg.signatures()` | Certificate management, sign, verify |
| `dg.pdfTools()` | Merge, split, metadata, PDF/A, rotate |
| `dg.preview()` | Page rendering as images |
| `dg.zugferd()` | ZUGFeRD embed, extract, validate |
| `dg.xrechnung()` | XRechnung generate, parse, validate, transform |
| `dg.excel()` | Excel workbook generation and conversion |
| `dg.receipts()` | AI-powered receipt/ticket extraction and export |

## Requirements

- Java 17+
- Jackson 2.18+

## License

MIT
