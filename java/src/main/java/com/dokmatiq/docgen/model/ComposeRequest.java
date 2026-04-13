package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;

/** Multi-part document composition request. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ComposeRequest(
        List<DocumentPart> parts,
        Object watermark,
        StationeryConfig stationery,
        List<ContentArea> contentAreas,
        InvoiceData invoiceData,
        String password,
        OutputFormat outputFormat,
        String callbackUrl,
        String callbackSecret
) {}
