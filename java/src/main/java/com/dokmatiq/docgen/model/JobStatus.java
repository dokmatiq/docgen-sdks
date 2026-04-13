package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonValue;

/** Async job status. */
public enum JobStatus {
    PENDING("PENDING"), PROCESSING("PROCESSING"),
    COMPLETED("COMPLETED"), FAILED("FAILED");

    private final String value;

    JobStatus(String value) { this.value = value; }

    @JsonValue
    public String getValue() { return value; }
}
