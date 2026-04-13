package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Column definition for table data. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ColumnDef(
        String header,
        Integer width,
        TextAlignment alignment,
        ColumnFormat format
) {
    public ColumnDef(String header, int width) {
        this(header, width, null, null);
    }

    public ColumnDef(String header, int width, TextAlignment alignment) {
        this(header, width, alignment, null);
    }
}
