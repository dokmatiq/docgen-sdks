package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** XRechnung XML format. */
public enum XRechnungFormat {
    CII("CII"), UBL("UBL");

    private final String value;

    XRechnungFormat(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
