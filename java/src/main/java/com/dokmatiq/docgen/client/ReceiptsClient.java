package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.Transport;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Client for AI-powered receipt and ticket data extraction. */
public final class ReceiptsClient {

    private final Transport transport;

    public ReceiptsClient(Transport transport) {
        this.transport = transport;
    }

    /** Extract structured data from a receipt image or PDF. Requires AI consent. */
    @SuppressWarnings("unchecked")
    public Map<String, Object> extract(byte[] fileBytes, String fileName) {
        return transport.upload("/api/receipts/extract", "file", fileBytes, fileName, null, Map.class);
    }

    /** Submit receipt for async extraction with optional webhook. */
    @SuppressWarnings("unchecked")
    public Map<String, Object> extractAsync(byte[] fileBytes, String fileName,
                                            String callbackUrl, String callbackSecret) {
        var extra = new HashMap<String, String>();
        if (callbackUrl != null) extra.put("callbackUrl", callbackUrl);
        if (callbackSecret != null) extra.put("callbackSecret", callbackSecret);
        return transport.upload("/api/receipts/extract-async", "file", fileBytes, fileName,
                extra.isEmpty() ? null : extra, Map.class);
    }

    /** Extract receipt and generate expense report document. */
    @SuppressWarnings("unchecked")
    public Map<String, Object> toDocument(byte[] fileBytes, String fileName,
                                          String format, String title) {
        var extra = new HashMap<String, String>();
        if (format != null) extra.put("format", format);
        if (title != null) extra.put("title", title);
        return transport.upload("/api/receipts/to-document", "file", fileBytes, fileName,
                extra.isEmpty() ? null : extra, Map.class);
    }

    /** Export receipt data as CSV (DATEV-compatible). */
    public byte[] exportCsv(List<Map<String, Object>> receipts) {
        return transport.requestBytes("POST", "/api/receipts/export/csv", receipts);
    }

    /** Export receipt data as Excel (XLSX). */
    public byte[] exportXlsx(List<Map<String, Object>> receipts) {
        return transport.requestBytes("POST", "/api/receipts/export/xlsx", receipts);
    }

    /** Get async job status. */
    @SuppressWarnings("unchecked")
    public Map<String, Object> getJob(String jobId) {
        return transport.requestJson("GET", "/api/receipts/jobs/" + jobId, null, Map.class);
    }

    /** Get async job extraction result. */
    @SuppressWarnings("unchecked")
    public Map<String, Object> getJobResult(String jobId) {
        return transport.requestJson("GET", "/api/receipts/jobs/" + jobId + "/result", null, Map.class);
    }

    /** List all async receipt jobs. */
    @SuppressWarnings({"unchecked", "rawtypes"})
    public List<Map<String, Object>> listJobs() {
        List raw = transport.requestList("GET", "/api/receipts/jobs", Map.class);
        return (List<Map<String, Object>>) (List) raw;
    }
}
