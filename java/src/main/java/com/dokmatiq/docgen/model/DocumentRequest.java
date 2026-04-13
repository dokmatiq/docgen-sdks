package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import java.util.Map;

/** Main document generation request. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record DocumentRequest(
        String htmlContent,
        String markdownContent,
        String templateName,
        String templateBase64,
        Map<String, String> fields,
        Map<String, String> bookmarks,
        Map<String, String> markdownBookmarks,
        List<ImageData> images,
        List<QrCodeData> qrCodes,
        List<BarcodeData> barcodes,
        Map<String, TableData> tables,
        PageSettings pageSettings,
        Object watermark,
        StationeryConfig stationery,
        List<ContentArea> contentAreas,
        InvoiceData invoiceData,
        String password,
        OutputFormat outputFormat,
        String callbackUrl,
        String callbackSecret,
        Map<String, String> markdownStyles
) {}
