package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** ZUGFeRD profile level. */
public enum ZugferdProfile {
    MINIMUM("MINIMUM"), BASIC_WL("BASIC_WL"), BASIC("BASIC"),
    EN16931("EN16931"), EXTENDED("EXTENDED"), XRECHNUNG("XRECHNUNG");

    private final String value;

    ZugferdProfile(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
