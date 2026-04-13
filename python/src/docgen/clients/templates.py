"""Templates sub-client: upload, list, delete LibreOffice templates."""

from __future__ import annotations

from docgen._files import FileInput, to_bytes, detect_filename
from docgen._transport import Transport


class TemplatesClient:
    """Client for template management."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def upload(self, source: FileInput, filename: str | None = None) -> dict:
        """Upload a LibreOffice template (.odt, .ott, .docx).

        Args:
            source: Template file (path, bytes, or base64).
            filename: Override filename (auto-detected from path if not provided).

        Returns:
            API response with upload confirmation.
        """
        name = filename or detect_filename(source) or "template.odt"
        data = to_bytes(source)
        content_type = "application/vnd.oasis.opendocument.text"
        if name.endswith(".docx"):
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        return self._transport.upload(
            "/api/templates",
            files={"file": (name, data, content_type)},
        )

    def list(self) -> list[str]:
        """List all uploaded template names."""
        return self._transport.request_list("GET", "/api/templates")

    def delete(self, template_name: str) -> None:
        """Delete an uploaded template.

        Args:
            template_name: Name of the template to delete.
        """
        self._transport.delete(f"/api/templates/{template_name}")
