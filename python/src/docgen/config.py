"""SDK configuration."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RetryPolicy:
    """Retry configuration for failed requests.

    Args:
        max_retries: Maximum number of retry attempts.
        initial_delay: Initial delay in seconds before first retry.
        max_delay: Maximum delay in seconds between retries.
        backoff_multiplier: Multiplier for exponential backoff.
        retry_on_status: HTTP status codes that trigger a retry.
        retry_on_timeout: Whether to retry on request timeouts.
    """

    max_retries: int = 3
    initial_delay: float = 0.5
    max_delay: float = 30.0
    backoff_multiplier: float = 2.0
    retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504)
    retry_on_timeout: bool = True


@dataclass
class DocGenConfig:
    """Configuration for the DocGen client.

    Args:
        api_key: API key for authentication (X-API-Key header).
        base_url: Base URL of the DocGen API (default: http://localhost:8080).
        timeout: Request timeout in seconds (default: 30).
        retry: Retry policy for transient failures.
        validate_mode: Validation mode sent via X-DocGen-Validate header.
            "strict" returns 400 on unknown fields,
            "warn" logs warnings but succeeds.
            None sends no validation header.
    """

    api_key: str
    base_url: str = "http://localhost:8080"
    timeout: float = 30.0
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    validate_mode: str | None = None
