package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Embedded image data for a document bookmark. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ImageData(
        String bookmarkName,
        String base64,
        Integer width,
        Integer height,
        String altText
) {}
