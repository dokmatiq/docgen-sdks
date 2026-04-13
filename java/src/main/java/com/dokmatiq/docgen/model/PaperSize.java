package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Standard paper sizes. */
public enum PaperSize {
    A4("A4"), A3("A3"), A5("A5"), LETTER("LETTER"), LEGAL("LEGAL");

    private final String value;

    PaperSize(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
