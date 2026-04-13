"""Webhook signature verification utility."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any

from docgen._serialization import from_dict
from docgen.exceptions import DocGenError
from docgen.models.jobs import WebhookPayload


def verify_webhook(
    body: bytes | str,
    signature: str,
    secret: str,
) -> WebhookPayload:
    """Verify a DocGen webhook signature and parse the payload.

    The DocGen API signs webhook payloads with HMAC-SHA256 using the
    callback_secret provided in the original generation request.

    Args:
        body: Raw request body (bytes or string).
        signature: Value of the X-DocGen-Signature header.
        secret: The callback_secret used when creating the job.

    Returns:
        Parsed webhook payload.

    Raises:
        DocGenError: If the signature is invalid.
    """
    if isinstance(body, str):
        body = body.encode("utf-8")

    expected = hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise DocGenError("Invalid webhook signature")

    import json
    data = json.loads(body)
    return from_dict(WebhookPayload, data)
