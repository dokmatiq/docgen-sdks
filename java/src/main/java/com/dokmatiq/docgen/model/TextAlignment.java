package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Text alignment. */
public enum TextAlignment {
    LEFT("LEFT"), CENTER("CENTER"), RIGHT("RIGHT");

    private final String value;

    TextAlignment(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
