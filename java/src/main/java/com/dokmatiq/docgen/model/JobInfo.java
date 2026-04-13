package com.dokmatiq.docgen.model;

/** Information about an async generation job. */
public record JobInfo(
        String jobId,
        JobStatus status,
        String createdAt,
        String completedAt,
        String errorMessage
) {}
