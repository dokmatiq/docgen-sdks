"""Documents sub-client: generate, compose, async jobs."""

from __future__ import annotations

import time
from typing import Any

from docgen._serialization import from_dict, to_dict
from docgen._transport import Transport
from docgen.exceptions import DocGenError
from docgen.models.document import ComposeRequest, DocumentRequest
from docgen.models.enums import JobStatus
from docgen.models.jobs import JobInfo


class DocumentsClient:
    """Client for document generation and async job management."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def generate(self, request: DocumentRequest) -> bytes:
        """Generate a document synchronously.

        Args:
            request: Document generation request.

        Returns:
            Raw document bytes (PDF, DOCX, or ODT).
        """
        return self._transport.request_bytes(
            "POST", "/api/documents/generate", json=to_dict(request)
        )

    def compose(self, request: ComposeRequest) -> bytes:
        """Compose multiple document parts into a single document.

        Args:
            request: Compose request with parts and global settings.

        Returns:
            Raw document bytes.
        """
        return self._transport.request_bytes(
            "POST", "/api/documents/compose", json=to_dict(request)
        )

    def generate_async(self, request: DocumentRequest) -> JobInfo:
        """Submit an async document generation job.

        Args:
            request: Document generation request.

        Returns:
            Job info with job_id for status polling.
        """
        data = self._transport.request_json(
            "POST", "/api/documents/generate-async", json=to_dict(request)
        )
        return from_dict(JobInfo, data)

    def get_job(self, job_id: str) -> JobInfo:
        """Get the status of an async job.

        Args:
            job_id: Job identifier returned by generate_async.
        """
        data = self._transport.request_json("GET", f"/api/documents/jobs/{job_id}")
        return from_dict(JobInfo, data)

    def download_job(self, job_id: str) -> bytes:
        """Download the result of a completed async job.

        Args:
            job_id: Job identifier.

        Returns:
            Raw document bytes.

        Raises:
            ConflictError: If the job is not yet completed.
        """
        return self._transport.request_bytes("GET", f"/api/documents/jobs/{job_id}/download")

    def list_jobs(self) -> list[JobInfo]:
        """List all async jobs."""
        data = self._transport.request_list("GET", "/api/documents/jobs")
        return [from_dict(JobInfo, item) for item in data]

    def wait_for_job(
        self,
        job_id: str,
        *,
        poll_interval: float = 2.0,
        timeout: float = 120.0,
    ) -> bytes:
        """Poll an async job until completion and return the result.

        Args:
            job_id: Job identifier.
            poll_interval: Seconds between status checks.
            timeout: Maximum seconds to wait.

        Returns:
            Raw document bytes.

        Raises:
            DocGenError: If the job fails.
            TimeoutError: If the timeout is exceeded.
        """
        start = time.monotonic()
        while True:
            job = self.get_job(job_id)

            if job.status == JobStatus.COMPLETED:
                return self.download_job(job_id)

            if job.status == JobStatus.FAILED:
                raise DocGenError(f"Job {job_id} failed: {job.error}")

            elapsed = time.monotonic() - start
            if elapsed + poll_interval > timeout:
                raise DocGenError(f"Job {job_id} timed out after {timeout}s")

            time.sleep(poll_interval)
