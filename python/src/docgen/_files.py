"""File handling utilities for transparent path/bytes/base64 conversion."""

from __future__ import annotations

import base64
from pathlib import Path


FileInput = bytes | Path | str
"""Flexible file input type.

- ``bytes``: Raw file data.
- ``Path``: File path on disk (will be read automatically).
- ``str``: Either a file path or a base64-encoded string.
"""


def to_base64(source: FileInput) -> str:
    """Convert a file input to a base64-encoded string.

    Args:
        source: File path, raw bytes, or base64 string.

    Returns:
        Base64-encoded string of the file content.
    """
    if isinstance(source, bytes):
        return base64.b64encode(source).decode("ascii")

    if isinstance(source, Path):
        return base64.b64encode(source.read_bytes()).decode("ascii")

    # String: could be a file path or already base64
    path = Path(source)
    if path.exists() and path.is_file():
        return base64.b64encode(path.read_bytes()).decode("ascii")

    # Assume it's already base64
    return source


def to_bytes(source: FileInput) -> bytes:
    """Convert a file input to raw bytes.

    Args:
        source: File path, raw bytes, or base64 string.

    Returns:
        Raw bytes of the file content.
    """
    if isinstance(source, bytes):
        return source

    if isinstance(source, Path):
        return source.read_bytes()

    path = Path(source)
    if path.exists() and path.is_file():
        return path.read_bytes()

    # Assume base64
    return base64.b64decode(source)


def detect_filename(source: FileInput) -> str | None:
    """Extract filename from a file input, if available."""
    if isinstance(source, Path):
        return source.name
    if isinstance(source, str):
        path = Path(source)
        if path.exists() and path.is_file():
            return path.name
    return None
