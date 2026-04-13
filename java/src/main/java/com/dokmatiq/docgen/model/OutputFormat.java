package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Output document format. */
public enum OutputFormat {
    PDF("PDF"),
    DOCX("DOCX"),
    ODT("ODT");

    private final String value;

    OutputFormat(String value) {
        this.value = value;
    }

    @JsonValue
    public String getValue() {
        return value;
    }
}
