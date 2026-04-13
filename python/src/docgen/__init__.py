"""Dokmatiq DocGen Python SDK.

Generate PDF, DOCX, and ODT documents from HTML/Markdown content
with templates, e-invoicing (ZUGFeRD/XRechnung), digital signatures, and more.

Quick start::

    from docgen import DocGen

    dg = DocGen(api_key="dk_live_xxx")
    pdf = dg.html_to_pdf("<h1>Hello World</h1>")

Builder pattern::

    pdf = (dg.document()
        .html("<h1>Invoice {{nr}}</h1>")
        .template("invoice.odt")
        .field("nr", "2026-001")
        .watermark("DRAFT")
        .as_pdf()
        .generate())
"""

from docgen.client import AsyncDocGen, DocGen
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
from docgen.models import (
    BankAccount,
    BarcodeData,
    BarcodeFormat,
    ColumnDef,
    ColumnFormat,
    ComposeRequest,
    ContentArea,
    DocumentPart,
    DocumentRequest,
    ExtractionResult,
    HeaderFooterConfig,
    ImageData,
    InvoiceData,
    InvoiceItem,
    InvoiceUnit,
    JobInfo,
    JobStatus,
    MarkdownStyles,
    OutputFormat,
    PageOrientation,
    PageSettings,
    PaperSize,
    Party,
    PdfFormField,
    PdfFormFillRequest,
    PreviewPage,
    PreviewResponse,
    QrCodeData,
    SignatureRequest,
    SignatureVerifyResult,
    StationeryConfig,
    TableData,
    TableStyle,
    TextAlignment,
    VisibleSignatureConfig,
    WatermarkConfig,
    WebhookPayload,
    XRechnungFormat,
    ZugferdProfile,
)
from docgen.builders import ComposeBuilder, DocumentBuilder, InvoiceBuilder
from docgen.webhooks import verify_webhook

__version__ = "0.1.0"

__all__ = [
    # Client
    "AsyncDocGen",
    "DocGen",
    # Config
    "DocGenConfig",
    "RetryPolicy",
    # Builders
    "ComposeBuilder",
    "DocumentBuilder",
    "InvoiceBuilder",
    # Exceptions
    "AuthenticationError",
    "ConflictError",
    "DocGenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ServiceUnavailableError",
    "ValidationError",
    # Enums
    "BarcodeFormat",
    "ColumnFormat",
    "InvoiceUnit",
    "JobStatus",
    "OutputFormat",
    "PageOrientation",
    "PaperSize",
    "TextAlignment",
    "XRechnungFormat",
    "ZugferdProfile",
    # Models
    "BankAccount",
    "BarcodeData",
    "ColumnDef",
    "ComposeRequest",
    "ContentArea",
    "DocumentPart",
    "DocumentRequest",
    "ExtractionResult",
    "HeaderFooterConfig",
    "ImageData",
    "InvoiceData",
    "InvoiceItem",
    "JobInfo",
    "MarkdownStyles",
    "PageSettings",
    "Party",
    "PdfFormField",
    "PdfFormFillRequest",
    "PreviewPage",
    "PreviewResponse",
    "QrCodeData",
    "SignatureRequest",
    "SignatureVerifyResult",
    "StationeryConfig",
    "TableData",
    "TableStyle",
    "VisibleSignatureConfig",
    "WatermarkConfig",
    "WebhookPayload",
    # Webhooks
    "verify_webhook",
]
