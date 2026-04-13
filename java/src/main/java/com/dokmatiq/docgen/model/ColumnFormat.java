package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Column number format. */
public enum ColumnFormat {
    TEXT("TEXT"), NUMBER("NUMBER"), CURRENCY("CURRENCY"), PERCENTAGE("PERCENTAGE");

    private final String value;

    ColumnFormat(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
