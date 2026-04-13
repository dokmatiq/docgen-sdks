package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.PdfFormField;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

/** Client for PDF form inspection and filling. */
public class PdfFormsClient {
    private final Transport transport;

    public PdfFormsClient(Transport transport) {
        this.transport = transport;
    }

    /** Inspect form fields in a PDF. */
    public List<PdfFormField> inspectFields(Path file) {
        var base64 = FileUtils.toBase64(file);
        return transport.requestList("POST", "/api/pdf-forms/inspect",
                PdfFormField.class);
    }

    /** Inspect form fields from bytes. */
    public List<PdfFormField> inspectFields(byte[] data) {
        var base64 = FileUtils.toBase64(data);
        return transport.requestList("POST", "/api/pdf-forms/inspect",
                PdfFormField.class);
    }

    /** Fill form fields in a PDF. */
    public byte[] fill(Path file, Map<String, String> fields, boolean flatten) {
        var base64 = FileUtils.toBase64(file);
        return transport.requestBytes("POST", "/api/pdf-forms/fill",
                Map.of("pdfBase64", base64, "fields", fields, "flatten", flatten));
    }

    /** Fill form fields from bytes. */
    public byte[] fill(byte[] data, Map<String, String> fields, boolean flatten) {
        var base64 = FileUtils.toBase64(data);
        return transport.requestBytes("POST", "/api/pdf-forms/fill",
                Map.of("pdfBase64", base64, "fields", fields, "flatten", flatten));
    }

    /** Fill form fields (without flattening). */
    public byte[] fill(Path file, Map<String, String> fields) {
        return fill(file, fields, false);
    }
}
