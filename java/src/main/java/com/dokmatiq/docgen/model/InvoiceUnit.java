package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Invoice unit codes (UN/ECE Recommendation 20). */
public enum InvoiceUnit {
    PIECE("C62"), HOUR("HUR"), DAY("DAY"),
    KILOGRAM("KGM"), METER("MTR"), LITER("LTR"),
    SQUARE_METER("MTK"), CUBIC_METER("MTQ"),
    SET("SET"), PACKAGE("PK");

    private final String value;

    InvoiceUnit(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
