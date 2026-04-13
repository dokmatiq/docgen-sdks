package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** QR code data for a document bookmark. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record QrCodeData(
        String bookmarkName,
        String content,
        Integer width,
        Integer height,
        String errorCorrectionLevel
) {}
