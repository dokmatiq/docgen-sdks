package com.dokmatiq.docgen.model;

import java.util.List;

/** A form field detected in a PDF. */
public record PdfFormField(
        String name,
        String type,
        String value,
        List<String> options,
        Boolean required,
        Boolean readOnly
) {}
