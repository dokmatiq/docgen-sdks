"""Digital signature types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VisibleSignatureConfig:
    """Configuration for a visible signature on a PDF page.

    Args:
        page: Page number for the signature (1-based).
        x: X position in mm from left edge.
        y: Y position in mm from top edge.
        width: Signature area width in mm.
        height: Signature area height in mm.
        text: Text to display in the signature area.
        font_size: Font size for the signature text.
        image_base64: Base64-encoded signature image.
        contact: Contact information in the signature.
    """

    page: int = 1
    x: float = 10.0
    y: float = 10.0
    width: float = 200.0
    height: float = 50.0
    text: str | None = None
    font_size: float | None = None
    image_base64: str | None = None
    contact: str | None = None


@dataclass
class SignatureRequest:
    """Request to digitally sign a PDF.

    Args:
        pdf_base64: Base64-encoded PDF to sign.
        certificate_name: Name of a pre-uploaded PKCS#12 certificate.
        certificate_password: Password for the certificate.
        reason: Reason for signing.
        location: Location of signing.
        visible_signature: Visible signature configuration.
    """

    pdf_base64: str
    certificate_name: str
    certificate_password: str
    reason: str | None = None
    location: str | None = None
    visible_signature: VisibleSignatureConfig | None = None


@dataclass
class SignatureDetail:
    """Details of a single signature in a signed PDF.

    Args:
        signer: Signer common name.
        signing_time: Signing timestamp (ISO format).
        valid: Whether this signature is valid.
        reason: Stated reason for signing.
        location: Stated signing location.
    """

    signer: str | None = None
    signing_time: str | None = None
    valid: bool = False
    reason: str | None = None
    location: str | None = None


@dataclass
class SignatureVerifyResult:
    """Result of PDF signature verification.

    Args:
        signed: Whether the PDF contains any signatures.
        signature_count: Number of signatures found.
        all_valid: Whether all signatures are valid.
        signatures: Individual signature details.
    """

    signed: bool = False
    signature_count: int = 0
    all_valid: bool = False
    signatures: list[SignatureDetail] | None = None
