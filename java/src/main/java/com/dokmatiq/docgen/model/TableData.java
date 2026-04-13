package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;

/** Table data with columns, rows, and optional styling. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record TableData(
        List<ColumnDef> columns,
        List<List<String>> rows,
        TableStyle style
) {
    public TableData(List<ColumnDef> columns, List<List<String>> rows) {
        this(columns, rows, null);
    }
}
