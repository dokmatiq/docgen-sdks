package com.dokmatiq.docgen;

import com.dokmatiq.docgen.builder.ComposeBuilder;
import com.dokmatiq.docgen.builder.DocumentBuilder;
import com.dokmatiq.docgen.builder.InvoiceBuilder;
import com.dokmatiq.docgen.client.*;
import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.OutputFormat;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Main DocGen SDK client.
 *
 * <pre>{@code
 * try (var dg = new DocGen(DocGenConfig.builder("dk_live_xxx").build())) {
 *     // One-liner
 *     byte[] pdf = dg.htmlToPdf("<h1>Hello World</h1>");
 *
 *     // Builder
 *     byte[] invoice = dg.document()
 *         .html("<h1>Rechnung</h1>")
 *         .template("invoice.odt")
 *         .field("nr", "2026-001")
 *         .asPdf()
 *         .generate();
 * }
 * }</pre>
 */
public class DocGen implements AutoCloseable {
    private final Transport transport;

    private final DocumentsClient documents;
    private final TemplatesClient templates;
    private final FontsClient fonts;
    private final PdfFormsClient pdfForms;
    private final SignaturesClient signatures;
    private final PdfToolsClient pdfTools;
    private final PreviewClient preview;
    private final ZugferdClient zugferd;
    private final XRechnungClient xrechnung;
    private final ExcelClient excel;
    private final ReceiptsClient receipts;

    public DocGen(DocGenConfig config) {
        this.transport = new Transport(config);
        this.documents = new DocumentsClient(transport);
        this.templates = new TemplatesClient(transport);
        this.fonts = new FontsClient(transport);
        this.pdfForms = new PdfFormsClient(transport);
        this.signatures = new SignaturesClient(transport);
        this.pdfTools = new PdfToolsClient(transport);
        this.preview = new PreviewClient(transport);
        this.zugferd = new ZugferdClient(transport);
        this.xrechnung = new XRechnungClient(transport);
        this.excel = new ExcelClient(transport);
        this.receipts = new ReceiptsClient(transport);
    }

    /** Convenience: create with just an API key. */
    public DocGen(String apiKey) {
        this(DocGenConfig.builder(apiKey).build());
    }

    // ── Sub-clients ─────────────────────────────────────────────────

    public DocumentsClient documents() { return documents; }
    public TemplatesClient templates() { return templates; }
    public FontsClient fonts() { return fonts; }
    public PdfFormsClient pdfForms() { return pdfForms; }
    public SignaturesClient signatures() { return signatures; }
    public PdfToolsClient pdfTools() { return pdfTools; }
    public PreviewClient preview() { return preview; }
    public ZugferdClient zugferd() { return zugferd; }
    public XRechnungClient xrechnung() { return xrechnung; }
    public ExcelClient excel() { return excel; }
    public ReceiptsClient receipts() { return receipts; }

    // ── Builder entry points ────────────────────────────────────────

    /** Create a DocumentBuilder for fluent document construction. */
    public DocumentBuilder document() {
        return new DocumentBuilder().setClient(documents);
    }

    /** Create a ComposeBuilder for multi-part composition. */
    public ComposeBuilder compose() {
        return new ComposeBuilder().setClient(documents);
    }

    /** Create an InvoiceBuilder for structured invoice data. */
    public InvoiceBuilder invoice() {
        return new InvoiceBuilder();
    }

    // ── Convenience methods ─────────────────────────────────────────

    /** Convert HTML to PDF in one call. */
    public byte[] htmlToPdf(String html) {
        return document().html(html).asPdf().generate();
    }

    /** Convert Markdown to PDF in one call. */
    public byte[] markdownToPdf(String markdown) {
        return document().markdown(markdown).asPdf().generate();
    }

    /** Merge multiple PDF files into one. */
    public byte[] mergePdfs(List<Path> files) {
        return pdfTools.merge(files);
    }

    /** Sign a PDF with a certificate. */
    public byte[] signPdf(Path file, String certificateName, String certificatePassword) {
        return signatures.sign(file, certificateName, certificatePassword);
    }

    /** Fill form fields in a PDF. */
    public byte[] fillForm(Path file, Map<String, String> fields) {
        return pdfForms.fill(file, fields, false);
    }

    /** Fill form fields in a PDF with flatten option. */
    public byte[] fillForm(Path file, Map<String, String> fields, boolean flatten) {
        return pdfForms.fill(file, fields, flatten);
    }

    @Override
    public void close() {
        transport.close();
    }
}
