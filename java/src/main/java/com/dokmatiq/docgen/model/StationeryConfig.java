package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Stationery (letterhead) PDF background configuration. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record StationeryConfig(
        String pdfBase64,
        String firstPagePdfBase64
) {}
