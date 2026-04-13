package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/** Client for PDF manipulation tools. */
public class PdfToolsClient {
    private final Transport transport;

    public PdfToolsClient(Transport transport) {
        this.transport = transport;
    }

    /** Merge multiple PDFs into one. */
    public byte[] merge(List<Path> files) {
        var pdfs = files.stream().map(FileUtils::toBase64).collect(Collectors.toList());
        return transport.requestBytes("POST", "/api/pdf-tools/merge", Map.of("pdfs", pdfs));
    }

    /** Merge PDFs from byte arrays. */
    public byte[] merge(byte[]... pdfs) {
        var encoded = java.util.Arrays.stream(pdfs).map(FileUtils::toBase64).collect(Collectors.toList());
        return transport.requestBytes("POST", "/api/pdf-tools/merge", Map.of("pdfs", encoded));
    }

    /** Extract text content from a PDF. */
    public String extractText(Path file) {
        var result = transport.requestJson("POST", "/api/pdf-tools/extract-text",
                Map.of("pdfBase64", FileUtils.toBase64(file)), Map.class);
        return String.valueOf(result.get("text"));
    }

    /** Extract text from bytes. */
    public String extractText(byte[] data) {
        var result = transport.requestJson("POST", "/api/pdf-tools/extract-text",
                Map.of("pdfBase64", FileUtils.toBase64(data)), Map.class);
        return String.valueOf(result.get("text"));
    }

    /** Get PDF metadata. */
    public Map<?, ?> getMetadata(Path file) {
        return transport.requestJson("POST", "/api/pdf-tools/metadata",
                Map.of("pdfBase64", FileUtils.toBase64(file)), Map.class);
    }

    /** Set PDF metadata. */
    public byte[] setMetadata(Path file, Map<String, String> metadata) {
        var body = new HashMap<String, Object>();
        body.put("pdfBase64", FileUtils.toBase64(file));
        body.putAll(metadata);
        return transport.requestBytes("POST", "/api/pdf-tools/metadata/set", body);
    }

    /** Convert to PDF/A. */
    public byte[] toPdfA(Path file) {
        return transport.requestBytes("POST", "/api/pdf-tools/pdfa",
                Map.of("pdfBase64", FileUtils.toBase64(file)));
    }

    /** Convert bytes to PDF/A. */
    public byte[] toPdfA(byte[] data) {
        return transport.requestBytes("POST", "/api/pdf-tools/pdfa",
                Map.of("pdfBase64", FileUtils.toBase64(data)));
    }

    /** Rotate pages in a PDF. */
    public byte[] rotate(Path file, int angle) {
        return transport.requestBytes("POST", "/api/pdf-tools/rotate",
                Map.of("pdfBase64", FileUtils.toBase64(file), "angle", angle));
    }

    /** Rotate specific pages. */
    public byte[] rotate(Path file, int angle, String pages) {
        var body = new HashMap<String, Object>();
        body.put("pdfBase64", FileUtils.toBase64(file));
        body.put("angle", angle);
        body.put("pages", pages);
        return transport.requestBytes("POST", "/api/pdf-tools/rotate", body);
    }
}
