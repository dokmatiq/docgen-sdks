package com.dokmatiq.docgen.model;

import java.util.List;

/** Response from a multi-page preview request. */
public record PreviewResponse(
        List<PreviewPage> pages,
        int totalPages
) {}
