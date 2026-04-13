package com.dokmatiq.docgen.model;

/** Details of a single signature in a signed PDF. */
public record SignatureDetail(
        String signer,
        String signingTime,
        boolean valid,
        String reason,
        String location
) {}
