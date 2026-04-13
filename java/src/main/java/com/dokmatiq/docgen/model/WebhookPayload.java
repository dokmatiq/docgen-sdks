package com.dokmatiq.docgen.model;

/** Webhook payload sent when an async job completes. */
public record WebhookPayload(
        String jobId,
        String status,
        String completedAt,
        String errorMessage
) {}
