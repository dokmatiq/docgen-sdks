package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import java.util.Map;

/** A single part in a multi-part composed document. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record DocumentPart(
        String htmlContent,
        String markdownContent,
        String templateName,
        String templateBase64,
        Map<String, String> fields,
        Map<String, String> bookmarks,
        List<ImageData> images,
        List<QrCodeData> qrCodes,
        List<BarcodeData> barcodes,
        Map<String, TableData> tables,
        PageSettings pageSettings
) {
    public DocumentPart(String htmlContent) {
        this(htmlContent, null, null, null, null, null, null, null, null, null, null);
    }

    public DocumentPart(String htmlContent, String templateName) {
        this(htmlContent, null, templateName, null, null, null, null, null, null, null, null);
    }
}
