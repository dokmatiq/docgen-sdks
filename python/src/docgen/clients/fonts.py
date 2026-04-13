"""Fonts sub-client: upload, list, delete custom fonts."""

from __future__ import annotations

from docgen._files import FileInput, to_bytes, detect_filename
from docgen._transport import Transport


class FontsClient:
    """Client for custom font management."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def upload(self, source: FileInput, filename: str | None = None) -> dict:
        """Upload a custom font (.ttf, .otf).

        Args:
            source: Font file (path, bytes, or base64).
            filename: Override filename.

        Returns:
            API response with upload confirmation.
        """
        name = filename or detect_filename(source) or "font.ttf"
        data = to_bytes(source)
        content_type = "font/ttf" if name.endswith(".ttf") else "font/otf"
        return self._transport.upload(
            "/api/fonts",
            files={"file": (name, data, content_type)},
        )

    def list(self) -> list[str]:
        """List available font family names."""
        return self._transport.request_list("GET", "/api/fonts")

    def delete(self, filename: str) -> None:
        """Delete an uploaded font.

        Args:
            filename: Font filename to delete.
        """
        self._transport.delete(f"/api/fonts/{filename}")
