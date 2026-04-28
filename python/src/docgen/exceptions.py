"""SDK exception types mapped to API HTTP errors."""

from __future__ import annotations

from typing import Any


class DocGenError(Exception):
    """Base exception for all DocGen SDK errors."""

    def __init__(self, message: str, status_code: int | None = None, body: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class ValidationError(DocGenError):
    """400 - Request validation failed.

    Attributes:
        field_errors: List of field-level error details from the API.
        hint: Suggested correction (e.g. "did you mean 'templateName'?").
    """

    def __init__(self, message: str, body: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=400, body=body)
        self.field_errors: list[dict[str, Any]] = (body or {}).get("fieldErrors", [])
        self.hint: str | None = (body or {}).get("hint")


class AuthenticationError(DocGenError):
    """401 - Invalid or missing API key."""

    def __init__(self, message: str = "Invalid or missing API key", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=401, body=body)


class NotFoundError(DocGenError):
    """404 - Resource not found (template, job, certificate)."""

    def __init__(self, message: str = "Resource not found", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=404, body=body)


class ConflictError(DocGenError):
    """409 - Conflict (e.g. async job not yet ready for download)."""

    def __init__(self, message: str = "Resource conflict", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=409, body=body)


class RateLimitError(DocGenError):
    """429 - Rate limit exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying.
        limit: Configured rate limit (requests per minute).
        remaining: Remaining requests in the current window.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        body: dict[str, Any] | None = None,
        retry_after: float | None = None,
        limit: int | None = None,
        remaining: int | None = None,
    ) -> None:
        super().__init__(message, status_code=429, body=body)
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining


class ServerError(DocGenError):
    """500 - Internal server error."""

    def __init__(self, message: str = "Internal server error", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=500, body=body)


class ServiceUnavailableError(DocGenError):
    """503 - Service unavailable (e.g. LibreOffice pool exhausted)."""

    def __init__(self, message: str = "Service unavailable", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=503, body=body)


class TimeoutError(DocGenError):
    """Request or job polling timed out."""

    def __init__(self, message: str = "Request timed out") -> None:
        super().__init__(message)
