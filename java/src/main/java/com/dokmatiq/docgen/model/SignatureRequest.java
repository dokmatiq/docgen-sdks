package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Request to digitally sign a PDF. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record SignatureRequest(
        String pdfBase64,
        String certificateName,
        String certificatePassword,
        String reason,
        String location,
        VisibleSignatureConfig visibleSignature
) {}
