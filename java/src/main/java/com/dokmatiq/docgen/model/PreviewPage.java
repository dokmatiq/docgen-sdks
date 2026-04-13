package com.dokmatiq.docgen.model;

/** A single rendered page preview. */
public record PreviewPage(
        int page,
        String imageBase64,
        int width,
        int height
) {}
