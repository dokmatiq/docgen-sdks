"""PDF form types."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PdfFormField:
    """A field found in a PDF AcroForm.

    Args:
        name: Field name.
        type: Field type (TEXT, CHECKBOX, RADIO, DROPDOWN, LISTBOX, SIGNATURE, BUTTON).
        value: Current field value.
        required: Whether the field is required.
        read_only: Whether the field is read-only.
        max_length: Maximum character length (for text fields).
        options: Available options (for dropdown/listbox/radio).
    """

    name: str
    type: str
    value: str | None = None
    required: bool = False
    read_only: bool = False
    max_length: int | None = None
    options: list[str] | None = None


@dataclass
class PdfFormFillRequest:
    """Request to fill PDF form fields.

    Args:
        pdf_base64: Base64-encoded PDF with form fields.
        fields: Field values to fill (name → value).
        flatten: Whether to flatten the form after filling (makes fields non-editable).
        password: Optional password for the filled PDF.
    """

    pdf_base64: str
    fields: dict[str, str] = field(default_factory=dict)
    flatten: bool = False
    password: str | None = None
