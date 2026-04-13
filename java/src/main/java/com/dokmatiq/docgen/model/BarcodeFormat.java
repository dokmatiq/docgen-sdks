package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Barcode formats. */
public enum BarcodeFormat {
    CODE_128("CODE_128"), CODE_39("CODE_39"),
    EAN_13("EAN_13"), EAN_8("EAN_8"), UPC_A("UPC_A"),
    QR_CODE("QR_CODE"), DATA_MATRIX("DATA_MATRIX"), PDF_417("PDF_417");

    private final String value;

    BarcodeFormat(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
