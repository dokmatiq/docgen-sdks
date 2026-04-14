"""Main DocGen client with sync and async variants."""

from __future__ import annotations

from typing import Any

from docgen._files import FileInput, to_base64
from docgen._transport import AsyncTransport, Transport
from docgen.builders.compose_builder import ComposeBuilder
from docgen.builders.document_builder import DocumentBuilder
from docgen.builders.invoice_builder import InvoiceBuilder
from docgen.clients.documents import DocumentsClient
from docgen.clients.fonts import FontsClient
from docgen.clients.pdf_forms import PdfFormsClient
from docgen.clients.pdf_tools import PdfToolsClient
from docgen.clients.preview import PreviewClient
from docgen.clients.signatures import SignaturesClient
from docgen.clients.templates import TemplatesClient
from docgen.clients.excel import ExcelClient
from docgen.clients.receipts import ReceiptsClient
from docgen.clients.xrechnung import XRechnungClient
from docgen.clients.zugferd import ZugferdClient
from docgen.config import DocGenConfig, RetryPolicy
from docgen.models.document import DocumentRequest
from docgen.models.enums import OutputFormat


class DocGen:
    """Main DocGen SDK client (synchronous).

    Provides access to all DocGen API capabilities via sub-clients
    and convenience methods for common operations.

    Usage::

        from docgen import DocGen

        dg = DocGen(api_key="dk_live_xxx")
        pdf = dg.html_to_pdf("<h1>Hello World</h1>")

        # Or with builder
        pdf = (dg.document()
            .html("<h1>Invoice</h1>")
            .template("invoice.odt")
            .field("nr", "2026-001")
            .as_pdf()
            .generate())

        # Context manager for automatic cleanup
        with DocGen(api_key="dk_live_xxx") as dg:
            pdf = dg.html_to_pdf("<h1>Hello</h1>")
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "http://localhost:8080",
        timeout: float = 30.0,
        retry: RetryPolicy | None = None,
        validate_mode: str | None = None,
        config: DocGenConfig | None = None,
    ) -> None:
        if config is not None:
            self._config = config
        else:
            self._config = DocGenConfig(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                retry=retry or RetryPolicy(),
                validate_mode=validate_mode,
            )
        self._transport = Transport(self._config)

        # Initialize sub-clients
        self._documents = DocumentsClient(self._transport)
        self._templates = TemplatesClient(self._transport)
        self._fonts = FontsClient(self._transport)
        self._pdf_forms = PdfFormsClient(self._transport)
        self._signatures = SignaturesClient(self._transport)
        self._pdf_tools = PdfToolsClient(self._transport)
        self._preview = PreviewClient(self._transport)
        self._zugferd = ZugferdClient(self._transport)
        self._xrechnung = XRechnungClient(self._transport)
        self._excel = ExcelClient(self._transport)
        self._receipts = ReceiptsClient(self._transport)

    # --- Sub-Clients ---

    @property
    def documents(self) -> DocumentsClient:
        """Document generation and async job management."""
        return self._documents

    @property
    def templates(self) -> TemplatesClient:
        """Template upload, listing, and deletion."""
        return self._templates

    @property
    def fonts(self) -> FontsClient:
        """Custom font management."""
        return self._fonts

    @property
    def pdf_forms(self) -> PdfFormsClient:
        """PDF AcroForm inspection and filling."""
        return self._pdf_forms

    @property
    def signatures(self) -> SignaturesClient:
        """PDF digital signatures and certificate management."""
        return self._signatures

    @property
    def pdf_tools(self) -> PdfToolsClient:
        """PDF merge, split, metadata, PDF/A, rotation."""
        return self._pdf_tools

    @property
    def preview(self) -> PreviewClient:
        """PDF page rendering as images."""
        return self._preview

    @property
    def zugferd(self) -> ZugferdClient:
        """ZUGFeRD/Factur-X e-invoice operations."""
        return self._zugferd

    @property
    def xrechnung(self) -> XRechnungClient:
        """XRechnung e-invoice operations."""
        return self._xrechnung

    @property
    def excel(self) -> ExcelClient:
        """Excel workbook generation and conversion."""
        return self._excel

    @property
    def receipts(self) -> ReceiptsClient:
        """AI-powered receipt and ticket data extraction."""
        return self._receipts

    # --- Builder Entry Points ---

    def document(self) -> DocumentBuilder:
        """Start building a document generation request.

        Returns:
            Fluent builder with .generate() support.
        """
        return DocumentBuilder(client=self._documents)

    def compose(self) -> ComposeBuilder:
        """Start building a multi-part document composition.

        Returns:
            Fluent builder with .generate() support.
        """
        return ComposeBuilder(client=self._documents)

    def invoice(self) -> InvoiceBuilder:
        """Start building structured invoice data.

        Returns:
            Fluent builder with .build() to create InvoiceData.
        """
        return InvoiceBuilder()

    # --- Convenience Methods ---

    def html_to_pdf(self, html: str, **kwargs: Any) -> bytes:
        """Convert HTML to PDF in one call.

        Args:
            html: HTML content to render.
            **kwargs: Additional DocumentRequest fields.

        Returns:
            PDF bytes.
        """
        request = DocumentRequest(
            html_content=html,
            output_format=OutputFormat.PDF,
            **kwargs,
        )
        return self._documents.generate(request)

    def markdown_to_pdf(self, md: str, **kwargs: Any) -> bytes:
        """Convert Markdown to PDF in one call.

        Args:
            md: Markdown content to render.
            **kwargs: Additional DocumentRequest fields.

        Returns:
            PDF bytes.
        """
        request = DocumentRequest(
            markdown_content=md,
            output_format=OutputFormat.PDF,
            **kwargs,
        )
        return self._documents.generate(request)

    def merge_pdfs(self, files: list[FileInput]) -> bytes:
        """Merge multiple PDF files into one.

        Args:
            files: List of PDF files (paths, bytes, or base64).

        Returns:
            Merged PDF bytes.
        """
        return self._pdf_tools.merge(files)

    def sign_pdf(
        self,
        pdf: FileInput,
        certificate_name: str,
        certificate_password: str,
        **kwargs: Any,
    ) -> bytes:
        """Sign a PDF with a digital certificate.

        Args:
            pdf: PDF to sign.
            certificate_name: Pre-uploaded certificate name.
            certificate_password: Certificate password.
            **kwargs: Additional SignatureRequest fields (reason, location, etc.).

        Returns:
            Signed PDF bytes.
        """
        return self._signatures.sign(
            pdf, certificate_name, certificate_password, **kwargs
        )

    def fill_form(
        self,
        pdf: FileInput,
        fields: dict[str, str],
        **kwargs: Any,
    ) -> bytes:
        """Fill PDF form fields.

        Args:
            pdf: PDF with form fields.
            fields: Field values (name → value).
            **kwargs: Additional options (flatten, password).

        Returns:
            Filled PDF bytes.
        """
        return self._pdf_forms.fill(pdf, fields, **kwargs)

    # --- Context Manager ---

    def __enter__(self) -> DocGen:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._transport.close()


class AsyncDocGen:
    """Async variant of the DocGen SDK client.

    Usage::

        async with AsyncDocGen(api_key="dk_live_xxx") as dg:
            pdf = await dg.html_to_pdf("<h1>Hello</h1>")
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "http://localhost:8080",
        timeout: float = 30.0,
        retry: RetryPolicy | None = None,
        validate_mode: str | None = None,
        config: DocGenConfig | None = None,
    ) -> None:
        if config is not None:
            self._config = config
        else:
            self._config = DocGenConfig(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                retry=retry or RetryPolicy(),
                validate_mode=validate_mode,
            )
        self._transport = AsyncTransport(self._config)

    # Async convenience methods

    async def html_to_pdf(self, html: str, **kwargs: Any) -> bytes:
        """Convert HTML to PDF asynchronously."""
        from docgen._serialization import to_dict
        request = DocumentRequest(
            html_content=html,
            output_format=OutputFormat.PDF,
            **kwargs,
        )
        return await self._transport.request_bytes(
            "POST", "/api/documents/generate", json=to_dict(request)
        )

    async def markdown_to_pdf(self, md: str, **kwargs: Any) -> bytes:
        """Convert Markdown to PDF asynchronously."""
        from docgen._serialization import to_dict
        request = DocumentRequest(
            markdown_content=md,
            output_format=OutputFormat.PDF,
            **kwargs,
        )
        return await self._transport.request_bytes(
            "POST", "/api/documents/generate", json=to_dict(request)
        )

    async def merge_pdfs(self, files: list[FileInput]) -> bytes:
        """Merge multiple PDFs asynchronously."""
        pdfs = [to_base64(f) for f in files]
        return await self._transport.request_bytes(
            "POST", "/api/pdf-tools/merge/base64",
            json={"pdfs": pdfs},
        )

    # --- Context Manager ---

    async def __aenter__(self) -> AsyncDocGen:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the async HTTP client."""
        await self._transport.close()
