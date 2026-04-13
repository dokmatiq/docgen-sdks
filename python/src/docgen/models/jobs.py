"""Async job types."""

from __future__ import annotations

from dataclasses import dataclass

from docgen.models.enums import JobStatus, OutputFormat


@dataclass
class JobInfo:
    """Status information for an async generation job.

    Args:
        job_id: Unique job identifier.
        status: Current job status.
        output_format: Requested output format.
        submit_time: Job submission timestamp (ISO format).
        completion_time: Job completion timestamp (ISO format).
        error: Error message if the job failed.
        file_size_bytes: Size of the generated document in bytes.
    """

    job_id: str
    status: JobStatus = JobStatus.PENDING
    output_format: OutputFormat | None = None
    submit_time: str | None = None
    completion_time: str | None = None
    error: str | None = None
    file_size_bytes: int | None = None


@dataclass
class WebhookPayload:
    """Payload sent via webhook on async job completion.

    Args:
        job_id: Job identifier.
        status: Final job status.
        download_url: URL to download the result.
        file_size_bytes: Size of the generated document.
        duration_ms: Processing duration in milliseconds.
        error: Error message if the job failed.
    """

    job_id: str
    status: JobStatus
    download_url: str | None = None
    file_size_bytes: int | None = None
    duration_ms: int | None = None
    error: str | None = None
