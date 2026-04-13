package com.dokmatiq.docgen.builder;

import com.dokmatiq.docgen.client.DocumentsClient;
import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.model.*;

import java.nio.file.Path;
import java.util.*;

/**
 * Fluent builder for constructing and executing document generation requests.
 *
 * <pre>{@code
 * byte[] pdf = dg.document()
 *     .html("<h1>Invoice {{nr}}</h1>")
 *     .template("invoice.odt")
 *     .field("nr", "2026-001")
 *     .watermark("DRAFT")
 *     .asPdf()
 *     .generate();
 * }</pre>
 */
public class DocumentBuilder {
    private DocumentsClient client;

    private String htmlContent;
    private String markdownContent;
    private String templateName;
    private String templateBase64;
    private Map<String, String> fields;
    private Map<String, String> bookmarks;
    private Map<String, String> markdownBookmarks;
    private List<ImageData> images;
    private List<QrCodeData> qrCodes;
    private List<BarcodeData> barcodes;
    private Map<String, TableData> tables;
    private PageSettings pageSettings;
    private Object watermark;
    private StationeryConfig stationery;
    private List<ContentArea> contentAreas;
    private InvoiceData invoiceData;
    private String password;
    private OutputFormat outputFormat;
    private String callbackUrl;
    private String callbackSecret;
    private Map<String, String> markdownStyles;

    /** @internal */
    public DocumentBuilder setClient(DocumentsClient client) {
        this.client = client;
        return this;
    }

    public DocumentBuilder html(String content) { this.htmlContent = content; return this; }
    public DocumentBuilder markdown(String content) { this.markdownContent = content; return this; }
    public DocumentBuilder template(String name) { this.templateName = name; return this; }

    public DocumentBuilder templateFile(Path file) {
        this.templateBase64 = FileUtils.toBase64(file);
        return this;
    }

    public DocumentBuilder field(String name, String value) {
        if (fields == null) fields = new LinkedHashMap<>();
        fields.put(name, value);
        return this;
    }

    public DocumentBuilder fields(Map<String, String> values) {
        if (fields == null) fields = new LinkedHashMap<>();
        fields.putAll(values);
        return this;
    }

    public DocumentBuilder bookmark(String name, String html) {
        if (bookmarks == null) bookmarks = new LinkedHashMap<>();
        bookmarks.put(name, html);
        return this;
    }

    public DocumentBuilder markdownBookmark(String name, String md) {
        if (markdownBookmarks == null) markdownBookmarks = new LinkedHashMap<>();
        markdownBookmarks.put(name, md);
        return this;
    }

    public DocumentBuilder image(String bookmarkName, Path file) {
        if (images == null) images = new ArrayList<>();
        images.add(new ImageData(bookmarkName, FileUtils.toBase64(file), null, null, null));
        return this;
    }

    public DocumentBuilder image(String bookmarkName, Path file, int width, int height) {
        if (images == null) images = new ArrayList<>();
        images.add(new ImageData(bookmarkName, FileUtils.toBase64(file), width, height, null));
        return this;
    }

    public DocumentBuilder qrCode(String bookmarkName, String content) {
        if (qrCodes == null) qrCodes = new ArrayList<>();
        qrCodes.add(new QrCodeData(bookmarkName, content, null, null, null));
        return this;
    }

    public DocumentBuilder barcode(String bookmarkName, String content, BarcodeFormat format) {
        if (barcodes == null) barcodes = new ArrayList<>();
        barcodes.add(new BarcodeData(bookmarkName, content, format, null, null));
        return this;
    }

    public DocumentBuilder table(String name, TableData data) {
        if (tables == null) tables = new LinkedHashMap<>();
        tables.put(name, data);
        return this;
    }

    public DocumentBuilder pageSettings(PageSettings settings) { this.pageSettings = settings; return this; }

    public DocumentBuilder watermark(String text) {
        this.watermark = text;
        return this;
    }

    public DocumentBuilder watermark(WatermarkConfig config) {
        this.watermark = config;
        return this;
    }

    public DocumentBuilder stationery(Path file) {
        this.stationery = new StationeryConfig(FileUtils.toBase64(file), null);
        return this;
    }

    public DocumentBuilder stationery(Path file, Path firstPage) {
        this.stationery = new StationeryConfig(FileUtils.toBase64(file), FileUtils.toBase64(firstPage));
        return this;
    }

    public DocumentBuilder contentArea(ContentArea area) {
        if (contentAreas == null) contentAreas = new ArrayList<>();
        contentAreas.add(area);
        return this;
    }

    public DocumentBuilder invoice(InvoiceData data) { this.invoiceData = data; return this; }
    public DocumentBuilder password(String pwd) { this.password = pwd; return this; }
    public DocumentBuilder outputFormat(OutputFormat format) { this.outputFormat = format; return this; }
    public DocumentBuilder asPdf() { this.outputFormat = OutputFormat.PDF; return this; }
    public DocumentBuilder asDocx() { this.outputFormat = OutputFormat.DOCX; return this; }
    public DocumentBuilder asOdt() { this.outputFormat = OutputFormat.ODT; return this; }

    public DocumentBuilder callback(String url, String secret) {
        this.callbackUrl = url;
        this.callbackSecret = secret;
        return this;
    }

    public DocumentBuilder markdownStyles(Map<String, String> styles) {
        this.markdownStyles = styles;
        return this;
    }

    /** Build the DocumentRequest without executing. */
    public DocumentRequest build() {
        return new DocumentRequest(
                htmlContent, markdownContent, templateName, templateBase64,
                fields, bookmarks, markdownBookmarks, images, qrCodes, barcodes,
                tables, pageSettings, watermark, stationery, contentAreas,
                invoiceData, password, outputFormat, callbackUrl, callbackSecret,
                markdownStyles
        );
    }

    /** Generate the document (requires attached client). */
    public byte[] generate() {
        if (client == null) {
            throw new IllegalStateException(
                    "No client attached. Use dg.document() or pass the request to dg.documents().generate().");
        }
        return client.generate(build());
    }
}
