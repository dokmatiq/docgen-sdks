"""Enumerations for the DocGen SDK."""

from __future__ import annotations

from enum import Enum


class OutputFormat(str, Enum):
    """Document output format."""

    PDF = "PDF"
    DOCX = "DOCX"
    ODT = "ODT"


class PaperSize(str, Enum):
    """Paper size for page settings."""

    A4 = "A4"
    A3 = "A3"
    A5 = "A5"
    LETTER = "LETTER"
    LEGAL = "LEGAL"


class PageOrientation(str, Enum):
    """Page orientation."""

    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"


class TextAlignment(str, Enum):
    """Text alignment for content areas and table columns."""

    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class BarcodeFormat(str, Enum):
    """Barcode format types."""

    CODE128 = "CODE128"
    CODE39 = "CODE39"
    EAN13 = "EAN13"
    EAN8 = "EAN8"
    UPC_A = "UPC_A"
    ITF = "ITF"
    CODABAR = "CODABAR"


class JobStatus(str, Enum):
    """Async job status."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class XRechnungFormat(str, Enum):
    """XRechnung XML format."""

    CII = "CII"
    UBL = "UBL"


class ColumnFormat(str, Enum):
    """Table column data format."""

    TEXT = "text"
    NUMBER = "number"
    CURRENCY = "currency"


class ZugferdProfile(str, Enum):
    """ZUGFeRD/Factur-X profile level."""

    MINIMUM = "MINIMUM"
    BASICWL = "BASICWL"
    BASIC = "BASIC"
    EN16931 = "EN16931"
    EXTENDED = "EXTENDED"
    XRECHNUNG = "XRECHNUNG"


class InvoiceUnit(str, Enum):
    """Unit codes for invoice items (UN/CEFACT)."""

    HOUR = "HUR"
    PIECE = "C62"
    KILOGRAM = "KGM"
    METER = "MTR"
    LITER = "LTR"
    DAY = "DAY"
