package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.PreviewResponse;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Client for PDF page preview rendering. */
public class PreviewClient {
    private final Transport transport;

    public PreviewClient(Transport transport) {
        this.transport = transport;
    }

    /** Render a single page as a PNG image. */
    public byte[] previewPage(Path file, int page, int dpi) {
        return transport.requestBytes("POST", "/api/preview/page",
                Map.of("pdfBase64", FileUtils.toBase64(file), "page", page, "dpi", dpi));
    }

    /** Render a single page with default DPI (150). */
    public byte[] previewPage(Path file, int page) {
        return previewPage(file, page, 150);
    }

    /** Render a single page (page 1, default DPI). */
    public byte[] previewPage(Path file) {
        return previewPage(file, 1, 150);
    }

    /** Render multiple pages. */
    public PreviewResponse previewPages(Path file, List<Integer> pages, int dpi) {
        var body = new HashMap<String, Object>();
        body.put("pdfBase64", FileUtils.toBase64(file));
        if (pages != null) body.put("pages", pages);
        body.put("dpi", dpi);
        return transport.requestJson("POST", "/api/preview/pages", body, PreviewResponse.class);
    }

    /** Get total page count. */
    public int pageCount(Path file) {
        var result = transport.requestJson("POST", "/api/preview/page-count",
                Map.of("pdfBase64", FileUtils.toBase64(file)), Map.class);
        return ((Number) result.get("pageCount")).intValue();
    }
}
