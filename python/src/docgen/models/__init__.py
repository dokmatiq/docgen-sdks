"""DocGen SDK model types."""

from docgen.models.enums import (
    BarcodeFormat,
    ColumnFormat,
    InvoiceUnit,
    JobStatus,
    OutputFormat,
    PageOrientation,
    PaperSize,
    TextAlignment,
    XRechnungFormat,
    ZugferdProfile,
)
from docgen.models.media import BarcodeData, ColumnDef, ImageData, QrCodeData, TableData, TableStyle
from docgen.models.content import ContentArea, StationeryConfig, WatermarkConfig
from docgen.models.page import HeaderFooterConfig, PageSettings
from docgen.models.invoice import BankAccount, InvoiceData, InvoiceItem, Party
from docgen.models.document import ComposeRequest, DocumentPart, DocumentRequest
from docgen.models.signature import SignatureDetail, SignatureRequest, SignatureVerifyResult, VisibleSignatureConfig
from docgen.models.forms import PdfFormField, PdfFormFillRequest
from docgen.models.preview import PreviewPage, PreviewResponse
from docgen.models.jobs import JobInfo, WebhookPayload
from docgen.models.extraction import ExtractionResult
from docgen.models.markdown import MarkdownStyles

__all__ = [
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
    # Media
    "BarcodeData",
    "ColumnDef",
    "ImageData",
    "QrCodeData",
    "TableData",
    "TableStyle",
    # Content
    "ContentArea",
    "StationeryConfig",
    "WatermarkConfig",
    # Page
    "HeaderFooterConfig",
    "PageSettings",
    # Invoice
    "BankAccount",
    "InvoiceData",
    "InvoiceItem",
    "Party",
    # Document
    "ComposeRequest",
    "DocumentPart",
    "DocumentRequest",
    # Signature
    "SignatureDetail",
    "SignatureRequest",
    "SignatureVerifyResult",
    "VisibleSignatureConfig",
    # Forms
    "PdfFormField",
    "PdfFormFillRequest",
    # Preview
    "PreviewPage",
    "PreviewResponse",
    # Jobs
    "JobInfo",
    "WebhookPayload",
    # Extraction
    "ExtractionResult",
    # Markdown
    "MarkdownStyles",
]
