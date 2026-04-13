"""Signatures sub-client: certificates, sign, verify."""

from __future__ import annotations

from typing import Any

from docgen._files import FileInput, to_base64, to_bytes, detect_filename
from docgen._serialization import from_dict, to_dict
from docgen._transport import Transport
from docgen.models.signature import (
    SignatureRequest,
    SignatureVerifyResult,
    VisibleSignatureConfig,
)


class SignaturesClient:
    """Client for PDF digital signature operations."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    # --- Certificate Management ---

    def upload_certificate(self, source: FileInput, filename: str | None = None) -> dict:
        """Upload a PKCS#12 certificate (.p12, .pfx).

        Args:
            source: Certificate file.
            filename: Override filename.
        """
        name = filename or detect_filename(source) or "certificate.p12"
        data = to_bytes(source)
        return self._transport.upload(
            "/api/signatures/certificates",
            files={"file": (name, data, "application/x-pkcs12")},
        )

    def list_certificates(self) -> list[str]:
        """List uploaded certificate names."""
        return self._transport.request_list("GET", "/api/signatures/certificates")

    def delete_certificate(self, filename: str) -> None:
        """Delete an uploaded certificate."""
        self._transport.delete(f"/api/signatures/certificates/{filename}")

    def certificate_info(self, source: FileInput, password: str) -> dict:
        """Get information about a PKCS#12 certificate.

        Args:
            source: Certificate file.
            password: Certificate password.
        """
        name = detect_filename(source) or "certificate.p12"
        data = to_bytes(source)
        return self._transport.upload(
            "/api/signatures/certificates/info",
            files={"file": (name, data, "application/x-pkcs12")},
            data={"password": password},
        )

    # --- Signing ---

    def sign(
        self,
        pdf: FileInput,
        certificate_name: str,
        certificate_password: str,
        *,
        reason: str | None = None,
        location: str | None = None,
        visible_signature: VisibleSignatureConfig | None = None,
    ) -> bytes:
        """Digitally sign a PDF.

        Args:
            pdf: PDF to sign.
            certificate_name: Name of a pre-uploaded certificate.
            certificate_password: Certificate password.
            reason: Reason for signing.
            location: Location of signing.
            visible_signature: Optional visible signature configuration.

        Returns:
            Signed PDF bytes.
        """
        request = SignatureRequest(
            pdf_base64=to_base64(pdf),
            certificate_name=certificate_name,
            certificate_password=certificate_password,
            reason=reason,
            location=location,
            visible_signature=visible_signature,
        )
        return self._transport.request_bytes(
            "POST", "/api/signatures/sign", json=to_dict(request)
        )

    # --- Verification ---

    def verify(self, pdf: FileInput) -> SignatureVerifyResult:
        """Verify signatures in a PDF.

        Args:
            pdf: PDF to verify.

        Returns:
            Verification result with signature details.
        """
        data = self._transport.request_json(
            "POST", "/api/signatures/verify/base64",
            json={"pdfBase64": to_base64(pdf)},
        )
        return from_dict(SignatureVerifyResult, data)
