package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.Map;

/** Result of AI-powered invoice data extraction. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ExtractionResult(
        String invoiceNumber,
        String invoiceDate,
        String sellerName,
        String buyerName,
        Double totalAmount,
        String currency,
        Double confidence,
        Map<String, Object> rawData
) {}
