package com.dokmatiq.docgen.model;

import java.util.List;

/** Result of PDF signature verification. */
public record SignatureVerifyResult(
        boolean signed,
        int signatureCount,
        boolean allValid,
        List<SignatureDetail> signatures
) {}
