package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.Map;

/** Request to fill PDF form fields. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PdfFormFillRequest(
        String pdfBase64,
        Map<String, String> fields,
        Boolean flatten
) {}
