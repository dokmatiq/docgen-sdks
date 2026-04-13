package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Barcode data for a document bookmark. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record BarcodeData(
        String bookmarkName,
        String content,
        BarcodeFormat format,
        Integer width,
        Integer height
) {}
