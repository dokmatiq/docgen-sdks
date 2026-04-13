"""Fluent builder for InvoiceData."""

from __future__ import annotations

from typing import Self

from docgen.models.enums import InvoiceUnit, XRechnungFormat, ZugferdProfile
from docgen.models.invoice import BankAccount, InvoiceData, InvoiceItem, Party


class InvoiceBuilder:
    """Fluent builder for constructing structured invoice data.

    Usage::

        invoice = (InvoiceBuilder()
            .number("RE-2026-001")
            .date("2026-04-12")
            .seller(name="ACME GmbH", street="Musterstr. 1", zip="12345", city="Berlin", vat_id="DE123456789")
            .buyer(name="Kunde AG", street="Kundenweg 5", zip="54321", city="Hamburg")
            .item("Beratung", quantity=8, unit=InvoiceUnit.HOUR, unit_price=120.0)
            .item("Reisekosten", unit_price=250.0)
            .bank(iban="DE89370400440532013000", bic="COBADEFFXXX", holder="ACME GmbH")
            .payment_terms("Zahlbar innerhalb 14 Tagen")
            .build())
    """

    def __init__(self) -> None:
        self._number: str = ""
        self._date: str = ""
        self._seller: Party | None = None
        self._buyer: Party | None = None
        self._items: list[InvoiceItem] = []
        self._currency: str = "EUR"
        self._bank_account: BankAccount | None = None
        self._payment_terms: str | None = None
        self._due_date: str | None = None
        self._note: str | None = None
        self._buyer_reference: str | None = None
        self._type_code: str = "380"
        self._profile: ZugferdProfile = ZugferdProfile.EN16931
        self._xrechnung_format: XRechnungFormat | None = None

    def number(self, invoice_number: str) -> Self:
        """Set the invoice number."""
        self._number = invoice_number
        return self

    def date(self, invoice_date: str) -> Self:
        """Set the invoice date (ISO format, e.g. '2026-04-12')."""
        self._date = invoice_date
        return self

    def seller(
        self,
        name: str,
        street: str | None = None,
        zip: str | None = None,
        city: str | None = None,
        country: str = "DE",
        vat_id: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> Self:
        """Set the seller party."""
        self._seller = Party(
            name=name, street=street, zip=zip, city=city,
            country=country, vat_id=vat_id, email=email, phone=phone,
        )
        return self

    def buyer(
        self,
        name: str,
        street: str | None = None,
        zip: str | None = None,
        city: str | None = None,
        country: str = "DE",
        vat_id: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> Self:
        """Set the buyer party."""
        self._buyer = Party(
            name=name, street=street, zip=zip, city=city,
            country=country, vat_id=vat_id, email=email, phone=phone,
        )
        return self

    def item(
        self,
        description: str,
        quantity: float = 1.0,
        unit: InvoiceUnit = InvoiceUnit.PIECE,
        unit_price: float = 0.0,
        vat_rate: float = 19.0,
    ) -> Self:
        """Add a line item to the invoice."""
        self._items.append(InvoiceItem(
            description=description, quantity=quantity, unit=unit,
            unit_price=unit_price, vat_rate=vat_rate,
        ))
        return self

    def bank(
        self,
        iban: str,
        bic: str | None = None,
        holder: str | None = None,
    ) -> Self:
        """Set the payment bank account."""
        self._bank_account = BankAccount(iban=iban, bic=bic, account_holder=holder)
        return self

    def currency(self, code: str) -> Self:
        """Set the currency (default: EUR)."""
        self._currency = code
        return self

    def payment_terms(self, terms: str) -> Self:
        """Set payment terms description."""
        self._payment_terms = terms
        return self

    def due_date(self, date: str) -> Self:
        """Set payment due date (ISO format)."""
        self._due_date = date
        return self

    def note(self, text: str) -> Self:
        """Set a free-text note."""
        self._note = text
        return self

    def buyer_reference(self, ref: str) -> Self:
        """Set the buyer reference / Leitweg-ID (required for XRechnung)."""
        self._buyer_reference = ref
        return self

    def type_code(self, code: str) -> Self:
        """Set the invoice type code (default: '380' = commercial invoice)."""
        self._type_code = code
        return self

    def profile(self, profile: ZugferdProfile) -> Self:
        """Set the ZUGFeRD profile level."""
        self._profile = profile
        return self

    def xrechnung(self, format: XRechnungFormat = XRechnungFormat.CII) -> Self:
        """Enable XRechnung format."""
        self._xrechnung_format = format
        return self

    def build(self) -> InvoiceData:
        """Build the InvoiceData object."""
        if not self._number:
            raise ValueError("Invoice number is required")
        if not self._date:
            raise ValueError("Invoice date is required")
        if self._seller is None:
            raise ValueError("Seller is required")
        if self._buyer is None:
            raise ValueError("Buyer is required")

        return InvoiceData(
            invoice_number=self._number,
            invoice_date=self._date,
            seller=self._seller,
            buyer=self._buyer,
            items=self._items,
            currency=self._currency,
            bank_account=self._bank_account,
            payment_terms=self._payment_terms,
            due_date=self._due_date,
            note=self._note,
            buyer_reference=self._buyer_reference,
            invoice_type_code=self._type_code,
            profile=self._profile,
            xrechnung_format=self._xrechnung_format,
        )
