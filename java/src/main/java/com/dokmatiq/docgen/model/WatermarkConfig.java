package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Diagonal watermark overlay configuration. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record WatermarkConfig(
        String text,
        Double fontSize,
        Double opacity,
        String color
) {
    public WatermarkConfig(String text) {
        this(text, null, null, null);
    }
}
