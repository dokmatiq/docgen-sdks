"""HTTP transport layer with auth, retry, and error mapping."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx

from docgen.config import DocGenConfig, RetryPolicy
from docgen.exceptions import (
    AuthenticationError,
    ConflictError,
    DocGenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ServiceUnavailableError,
    ValidationError,
)


class Transport:
    """Synchronous HTTP transport for the DocGen API."""

    def __init__(self, config: DocGenConfig) -> None:
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"X-API-Key": self._config.api_key}
        if self._config.validate_mode:
            headers["X-DocGen-Validate"] = self._config.validate_mode
        return headers

    def request_json(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a JSON request and return the parsed JSON response."""
        response = self._request_with_retry(method, path, json=json, params=params)
        _raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()  # type: ignore[no-any-return]

    def request_bytes(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        """Send a JSON request and return the raw response bytes (for documents)."""
        response = self._request_with_retry(method, path, json=json, params=params)
        _raise_for_status(response)
        return response.content

    def upload(
        self,
        path: str,
        *,
        files: dict[str, tuple[str, bytes, str]],
        data: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a multipart upload request."""
        response = self._client.post(path, files=files, data=data or {})
        _raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()  # type: ignore[no-any-return]

    def upload_bytes(
        self,
        path: str,
        *,
        files: dict[str, tuple[str, bytes, str]],
        data: dict[str, str] | None = None,
    ) -> bytes:
        """Send a multipart upload and return raw bytes."""
        response = self._client.post(path, files=files, data=data or {})
        _raise_for_status(response)
        return response.content

    def request_list(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> list[Any]:
        """Send a request and return the parsed JSON list response."""
        response = self._request_with_retry(method, path, params=params)
        _raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return []
        return response.json()  # type: ignore[no-any-return]

    def delete(self, path: str) -> None:
        """Send a DELETE request."""
        response = self._client.delete(path)
        _raise_for_status(response)

    def _request_with_retry(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        retry = self._config.retry
        last_exc: Exception | None = None

        for attempt in range(retry.max_retries + 1):
            try:
                response = self._client.request(method, path, **kwargs)
                if response.status_code not in retry.retry_on_status or attempt == retry.max_retries:
                    return response

                # 429 with Retry-After
                if response.status_code == 429:
                    wait = _parse_retry_after(response)
                    if wait:
                        time.sleep(wait)
                        continue

                time.sleep(_backoff_delay(retry, attempt))

            except httpx.TimeoutException as exc:
                last_exc = exc
                if not retry.retry_on_timeout or attempt == retry.max_retries:
                    raise DocGenError(f"Request timed out: {exc}") from exc
                time.sleep(_backoff_delay(retry, attempt))

        raise DocGenError("Max retries exceeded") from last_exc

    def close(self) -> None:
        self._client.close()


class AsyncTransport:
    """Asynchronous HTTP transport for the DocGen API."""

    def __init__(self, config: DocGenConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"X-API-Key": self._config.api_key}
        if self._config.validate_mode:
            headers["X-DocGen-Validate"] = self._config.validate_mode
        return headers

    async def request_json(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = await self._request_with_retry(method, path, json=json, params=params)
        _raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()  # type: ignore[no-any-return]

    async def request_bytes(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> bytes:
        response = await self._request_with_retry(method, path, json=json, params=params)
        _raise_for_status(response)
        return response.content

    async def upload(
        self,
        path: str,
        *,
        files: dict[str, tuple[str, bytes, str]],
        data: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        response = await self._client.post(path, files=files, data=data or {})
        _raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()  # type: ignore[no-any-return]

    async def upload_bytes(
        self,
        path: str,
        *,
        files: dict[str, tuple[str, bytes, str]],
        data: dict[str, str] | None = None,
    ) -> bytes:
        response = await self._client.post(path, files=files, data=data or {})
        _raise_for_status(response)
        return response.content

    async def request_list(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> list[Any]:
        response = await self._request_with_retry(method, path, params=params)
        _raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return []
        return response.json()  # type: ignore[no-any-return]

    async def delete(self, path: str) -> None:
        response = await self._client.delete(path)
        _raise_for_status(response)

    async def _request_with_retry(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        retry = self._config.retry
        last_exc: Exception | None = None

        for attempt in range(retry.max_retries + 1):
            try:
                response = await self._client.request(method, path, **kwargs)
                if response.status_code not in retry.retry_on_status or attempt == retry.max_retries:
                    return response

                if response.status_code == 429:
                    wait = _parse_retry_after(response)
                    if wait:
                        await asyncio.sleep(wait)
                        continue

                await asyncio.sleep(_backoff_delay(retry, attempt))

            except httpx.TimeoutException as exc:
                last_exc = exc
                if not retry.retry_on_timeout or attempt == retry.max_retries:
                    raise DocGenError(f"Request timed out: {exc}") from exc
                await asyncio.sleep(_backoff_delay(retry, attempt))

        raise DocGenError("Max retries exceeded") from last_exc

    async def close(self) -> None:
        await self._client.aclose()


def _raise_for_status(response: httpx.Response) -> None:
    """Map HTTP error responses to typed SDK exceptions."""
    if response.is_success:
        return

    body: dict[str, Any] | None = None
    message = response.reason_phrase or "Unknown error"
    try:
        body = response.json()
        message = body.get("error", body.get("message", message))
    except Exception:
        pass

    status = response.status_code
    if status == 400:
        raise ValidationError(message, body=body)
    if status == 401:
        raise AuthenticationError(message, body=body)
    if status == 404:
        raise NotFoundError(message, body=body)
    if status == 409:
        raise ConflictError(message, body=body)
    if status == 429:
        raise RateLimitError(
            message,
            body=body,
            retry_after=_parse_retry_after(response),
            limit=_int_header(response, "X-RateLimit-Limit"),
            remaining=_int_header(response, "X-RateLimit-Remaining"),
        )
    if status == 503:
        raise ServiceUnavailableError(message, body=body)
    if status >= 500:
        raise ServerError(message, body=body)

    raise DocGenError(message, status_code=status, body=body)


def _parse_retry_after(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After")
    if value:
        try:
            return float(value)
        except ValueError:
            pass
    return None


def _int_header(response: httpx.Response, name: str) -> int | None:
    value = response.headers.get(name)
    if value:
        try:
            return int(value)
        except ValueError:
            pass
    return None


def _backoff_delay(retry: RetryPolicy, attempt: int) -> float:
    delay = retry.initial_delay * (retry.backoff_multiplier ** attempt)
    return min(delay, retry.max_delay)
