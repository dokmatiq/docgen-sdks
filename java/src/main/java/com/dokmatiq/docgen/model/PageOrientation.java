package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Page orientation. */
public enum PageOrientation {
    PORTRAIT("PORTRAIT"), LANDSCAPE("LANDSCAPE");

    private final String value;

    PageOrientation(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
