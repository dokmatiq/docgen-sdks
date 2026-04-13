package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.JsonMapper;
import com.dokmatiq.docgen.internal.Transport;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Client for Excel workbook generation and conversion. */
public final class ExcelClient {

    private final Transport transport;

    public ExcelClient(Transport transport) {
        this.transport = transport;
    }

    /** Generate an Excel workbook from a structured JSON definition. Returns XLSX bytes. */
    public byte[] generate(Map<String, Object> request) {
        return transport.requestBytes("POST", "/api/excel/generate", request);
    }

    /** Convert CSV content to an Excel workbook. Returns XLSX bytes. */
    public byte[] fromCsv(String csvContent) {
        return fromCsv(csvContent, ",", true, null);
    }

    /** Convert CSV content to an Excel workbook. Returns XLSX bytes. */
    public byte[] fromCsv(String csvContent, String delimiter, boolean hasHeader, String sheetName) {
        var body = new HashMap<String, Object>();
        body.put("csvContent", csvContent);
        body.put("delimiter", delimiter);
        body.put("hasHeader", hasHeader);
        if (sheetName != null) body.put("sheetName", sheetName);
        return transport.requestBytes("POST", "/api/excel/from-csv", body);
    }

    /** Convert an Excel sheet to CSV text. */
    public String toCsv(String excelBase64) {
        return toCsv(excelBase64, 0, ",");
    }

    /** Convert an Excel sheet to CSV text. */
    public String toCsv(String excelBase64, int sheetIndex, String delimiter) {
        var body = Map.of(
                "excelBase64", (Object) excelBase64,
                "sheetIndex", sheetIndex,
                "delimiter", delimiter
        );
        byte[] bytes = transport.requestBytes("POST", "/api/excel/to-csv", body);
        return new String(bytes, java.nio.charset.StandardCharsets.UTF_8);
    }

    /** Convert an Excel sheet to structured JSON. */
    public Map<String, Object> toJson(String excelBase64) {
        return toJson(excelBase64, 0, true);
    }

    /** Convert an Excel sheet to structured JSON. */
    @SuppressWarnings("unchecked")
    public Map<String, Object> toJson(String excelBase64, int sheetIndex, boolean hasHeader) {
        var body = Map.of(
                "excelBase64", (Object) excelBase64,
                "sheetIndex", sheetIndex,
                "hasHeader", hasHeader
        );
        return transport.requestJson("POST", "/api/excel/to-json", body);
    }

    /** Fill an Excel template with data. Returns XLSX bytes. */
    public byte[] fillTemplate(String templateBase64, Map<String, Object> values) {
        return fillTemplate(templateBase64, values, null, true, null);
    }

    /** Fill an Excel template with data. Returns XLSX bytes. */
    public byte[] fillTemplate(String templateBase64, Map<String, Object> values,
                               Map<String, List<List<Object>>> tables,
                               boolean recalculate, String password) {
        var body = new HashMap<String, Object>();
        body.put("templateBase64", templateBase64);
        body.put("recalculate", recalculate);
        if (values != null) body.put("values", values);
        if (tables != null) body.put("tables", tables);
        if (password != null) body.put("password", password);
        return transport.requestBytes("POST", "/api/excel/fill-template", body);
    }

    /** Inspect an Excel workbook and return metadata. */
    public Map<String, Object> inspect(String excelBase64) {
        return transport.requestJson("POST", "/api/excel/inspect",
                Map.of("excelBase64", excelBase64));
    }
}
