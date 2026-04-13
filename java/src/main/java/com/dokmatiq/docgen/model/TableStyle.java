package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Table styling options. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record TableStyle(
        String borderColor,
        String headerBackground,
        String headerTextColor,
        String alternateRowBackground,
        Double fontSize
) {}
