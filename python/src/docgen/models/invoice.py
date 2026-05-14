"""Invoice data types for ZUGFeRD and XRechnung."""

from __future__ import annotations

from dataclasses import dataclass, field

from docgen.models.enums import InvoiceUnit, XRechnungFormat, ZugferdProfile


@dataclass
class Party:
    """Invoice party (seller or buyer).

    Args:
        name: Company or person name.
        street: Street address.
        zip: Postal code.
        city: City name.
        country: ISO 3166-1 alpha-2 country code (e.g. "DE").
        vat_id: VAT identification number.
        email: Email address.
        phone: Phone number.
    """

    name: str
    street: str | None = None
    zip: str | None = None
    city: str | None = None
    country: str = "DE"
    vat_id: str | None = None
    email: str | None = None
    phone: str | None = None


@dataclass
class InvoiceItem:
    """Single line item on an invoice.

    Args:
        description: Item description.
        quantity: Number of units.
        unit: Unit code (HUR=hour, C62=piece, KGM=kg, etc.).
        unit_price: Price per unit (net, before VAT).
        vat_rate: VAT rate as percentage (e.g. 19.0 for 19%).
    """

    description: str
    quantity: float = 1.0
    unit: InvoiceUnit = InvoiceUnit.PIECE
    unit_price: float = 0.0
    vat_rate: float = 19.0


@dataclass
class BankAccount:
    """Bank account details for payment.

    Args:
        iban: International Bank Account Number.
        bic: Bank Identifier Code (SWIFT).
        account_holder: Name of the account holder.
    """

    iban: str
    bic: str | None = None
    account_holder: str | None = None


@dataclass
class InvoiceData:
    """Structured invoice data for ZUGFeRD/Factur-X and XRechnung.

    Args:
        invoice_number: Unique invoice number.
        invoice_date: Invoice date (ISO format, e.g. "2026-04-12").
        seller: Seller party information.
        buyer: Buyer party information.
        items: Line items.
        currency: ISO 4217 currency code (default: "EUR").
        bank_account: Payment bank account details.
        payment_terms: Payment terms description.
        due_date: Payment due date (ISO format).
        note: Free-text note on the invoice.
        buyer_reference: Buyer reference / Leitweg-ID (required for XRechnung).
        invoice_type_code: UN/CEFACT type code (default: "380" = commercial invoice).
        profile: ZUGFeRD profile level.
        xrechnung_format: XRechnung XML format (CII or UBL).
    """

    invoice_number: str = field(metadata={"json_name": "number", "aliases": ("invoiceNumber",)})
    invoice_date: str = field(metadata={"json_name": "date", "aliases": ("invoiceDate", "issueDate")})
    seller: Party
    buyer: Party
    items: list[InvoiceItem] = field(default_factory=list)
    currency: str = "EUR"
    bank_account: BankAccount | None = field(default=None, metadata={"json_name": "bankAccount", "aliases": ("bankDetails",)})
    payment_terms: str | None = None
    due_date: str | None = None
    note: str | None = None
    buyer_reference: str | None = None
    invoice_type_code: str = "380"
    profile: ZugferdProfile = ZugferdProfile.EN16931
    xrechnung_format: XRechnungFormat | None = None
