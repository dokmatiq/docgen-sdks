"""DocGen API sub-clients."""

from docgen.clients.documents import DocumentsClient
from docgen.clients.templates import TemplatesClient
from docgen.clients.fonts import FontsClient
from docgen.clients.pdf_forms import PdfFormsClient
from docgen.clients.signatures import SignaturesClient
from docgen.clients.pdf_tools import PdfToolsClient
from docgen.clients.preview import PreviewClient
from docgen.clients.zugferd import ZugferdClient
from docgen.clients.excel import ExcelClient
from docgen.clients.xrechnung import XRechnungClient

__all__ = [
    "DocumentsClient",
    "ExcelClient",
    "FontsClient",
    "PdfFormsClient",
    "PdfToolsClient",
    "PreviewClient",
    "SignaturesClient",
    "TemplatesClient",
    "XRechnungClient",
    "ZugferdClient",
]
