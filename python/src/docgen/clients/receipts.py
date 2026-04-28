"""Client for AI-powered receipt and ticket data extraction."""

from __future__ import annotations

from typing import Any

from docgen._transport import Transport


class ReceiptsClient:
    """Client for receipt extraction, export, and async processing.

    Requires AI processing consent in portal settings (GDPR).
    """

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    # ── Extraction ───────────────────────────────────────────────────

    def extract(self, file_bytes: bytes, file_name: str, content_type: str = "image/jpeg") -> dict[str, Any]:
        """Extract structured data from a receipt image or PDF."""
        return self._t.upload("/api/receipts/extract",
            files={"file": (file_name, file_bytes, content_type)})

    def extract_batch(self, files: list[tuple[str, bytes, str]]) -> dict[str, Any]:
        """Extract data from multiple receipts sequentially.

        Args:
            files: List of (filename, bytes, content_type) tuples.
        """
        results = []
        success_count = 0
        for i, (name, data, ct) in enumerate(files):
            try:
                result = self.extract(data, name, ct)
                results.append({"index": i, "filename": name, "success": True, "result": result})
                success_count += 1
            except Exception as e:
                results.append({"index": i, "filename": name, "success": False, "error": str(e)})
        return {
            "totalFiles": len(files),
            "successCount": success_count,
            "failureCount": len(files) - success_count,
            "results": results,
        }

    # ── Async extraction ─────────────────────────────────────────────

    def extract_async(
        self,
        file_bytes: bytes,
        file_name: str,
        content_type: str = "image/jpeg",
        *,
        callback_url: str | None = None,
        callback_secret: str | None = None,
    ) -> dict[str, Any]:
        """Submit receipt for async extraction with optional webhook callback."""
        data: dict[str, str] = {}
        if callback_url:
            data["callbackUrl"] = callback_url
        if callback_secret:
            data["callbackSecret"] = callback_secret
        return self._t.upload("/api/receipts/extract-async",
            files={"file": (file_name, file_bytes, content_type)},
            data=data)

    # ── Document generation ──────────────────────────────────────────

    def to_document(
        self,
        file_bytes: bytes,
        file_name: str,
        content_type: str = "image/jpeg",
        *,
        format: str = "PDF",
        template_name: str | None = None,
        title: str = "Spesenbeleg",
    ) -> dict[str, Any]:
        """Extract receipt and generate expense report document."""
        data: dict[str, str] = {"format": format, "title": title}
        if template_name:
            data["templateName"] = template_name
        return self._t.upload("/api/receipts/to-document",
            files={"file": (file_name, file_bytes, content_type)},
            data=data)

    # ── Export ────────────────────────────────────────────────────────

    def export_csv(self, receipts: list[dict[str, Any]]) -> bytes:
        """Export receipt data as CSV (DATEV-compatible)."""
        return self._t.request_bytes("POST", "/api/receipts/export/csv", json=receipts)

    def export_xlsx(self, receipts: list[dict[str, Any]]) -> bytes:
        """Export receipt data as Excel (XLSX)."""
        return self._t.request_bytes("POST", "/api/receipts/export/xlsx", json=receipts)

    # ── Async jobs ───────────────────────────────────────────────────

    def get_job(self, job_id: str) -> dict[str, Any]:
        """Get async job status."""
        return self._t.request_json("GET", f"/api/receipts/jobs/{job_id}")

    def get_job_result(self, job_id: str) -> dict[str, Any]:
        """Get async job extraction result."""
        return self._t.request_json("GET", f"/api/receipts/jobs/{job_id}/result")

    def list_jobs(self) -> list[dict[str, Any]]:
        """List all async receipt jobs."""
        return self._t.request_list("GET", "/api/receipts/jobs")
