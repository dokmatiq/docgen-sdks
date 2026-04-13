package com.dokmatiq.docgen.builder;

import com.dokmatiq.docgen.client.DocumentsClient;
import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.model.*;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Fluent builder for multi-part document composition.
 *
 * <pre>{@code
 * byte[] pdf = dg.compose()
 *     .part(new DocumentPart("<h1>Cover</h1>"))
 *     .part(new DocumentPart("<h1>Chapter 1</h1>", "report.odt"))
 *     .watermark("CONFIDENTIAL")
 *     .asPdf()
 *     .generate();
 * }</pre>
 */
public class ComposeBuilder {
    private DocumentsClient client;
    private final List<DocumentPart> parts = new ArrayList<>();
    private Object watermark;
    private StationeryConfig stationery;
    private List<ContentArea> contentAreas;
    private InvoiceData invoiceData;
    private String password;
    private OutputFormat outputFormat;
    private String callbackUrl;
    private String callbackSecret;

    /** @internal */
    public ComposeBuilder setClient(DocumentsClient client) {
        this.client = client;
        return this;
    }

    public ComposeBuilder part(DocumentPart part) { parts.add(part); return this; }

    public ComposeBuilder watermark(String text) { this.watermark = text; return this; }
    public ComposeBuilder watermark(WatermarkConfig config) { this.watermark = config; return this; }

    public ComposeBuilder stationery(Path file) {
        this.stationery = new StationeryConfig(FileUtils.toBase64(file), null);
        return this;
    }

    public ComposeBuilder contentArea(ContentArea area) {
        if (contentAreas == null) contentAreas = new ArrayList<>();
        contentAreas.add(area);
        return this;
    }

    public ComposeBuilder invoice(InvoiceData data) { this.invoiceData = data; return this; }
    public ComposeBuilder password(String pwd) { this.password = pwd; return this; }
    public ComposeBuilder outputFormat(OutputFormat format) { this.outputFormat = format; return this; }
    public ComposeBuilder asPdf() { this.outputFormat = OutputFormat.PDF; return this; }
    public ComposeBuilder asDocx() { this.outputFormat = OutputFormat.DOCX; return this; }

    public ComposeBuilder callback(String url, String secret) {
        this.callbackUrl = url;
        this.callbackSecret = secret;
        return this;
    }

    /** Build the ComposeRequest without executing. */
    public ComposeRequest build() {
        return new ComposeRequest(List.copyOf(parts), watermark, stationery, contentAreas,
                invoiceData, password, outputFormat, callbackUrl, callbackSecret);
    }

    /** Generate the composed document (requires attached client). */
    public byte[] generate() {
        if (client == null) {
            throw new IllegalStateException(
                    "No client attached. Use dg.compose() or pass the request to dg.documents().compose().");
        }
        return client.compose(build());
    }
}
