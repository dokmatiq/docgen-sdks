"""Page settings and header/footer configuration."""

from __future__ import annotations

from dataclasses import dataclass

from docgen.models.enums import PageOrientation, PaperSize


@dataclass
class HeaderFooterConfig:
    """Header or footer configuration with page-specific control.

    Supports placeholders: {{PAGE}}, {{PAGES}}, {{DATE}}, {{TIME}},
    {{DATETIME}}, {{FILENAME}}.

    Args:
        left: Left-aligned text.
        center: Center-aligned text.
        right: Right-aligned text.
        height: Header/footer height in mm.
        spacing: Spacing between header/footer and body in mm.
        font_name: Font family name.
        font_size: Font size in points.
        color: Text color as hex string.
    """

    left: str | None = None
    center: str | None = None
    right: str | None = None
    height: float | None = None
    spacing: float | None = None
    font_name: str | None = None
    font_size: float | None = None
    color: str | None = None


@dataclass
class PageSettings:
    """Page layout settings for document generation.

    Args:
        orientation: Page orientation (PORTRAIT or LANDSCAPE).
        paper_size: Paper size (A4, A3, A5, LETTER, LEGAL).
        margin_top: Top margin in mm.
        margin_bottom: Bottom margin in mm.
        margin_left: Left margin in mm.
        margin_right: Right margin in mm.
        header_left: Simple left-aligned header text.
        header_center: Simple center-aligned header text.
        header_right: Simple right-aligned header text.
        footer_left: Simple left-aligned footer text.
        footer_center: Simple center-aligned footer text.
        footer_right: Simple right-aligned footer text.
        header: Advanced header config (overrides simple header_* fields).
        footer: Advanced footer config (overrides simple footer_* fields).
        header_first_page: Header config for first page only.
        footer_first_page: Footer config for first page only.
        header_even_pages: Header config for even pages.
        footer_even_pages: Footer config for even pages.
        header_footer_font_name: Default font for all headers/footers.
        header_footer_font_size: Default font size for all headers/footers.
        header_footer_color: Default color for all headers/footers.
    """

    orientation: PageOrientation | None = None
    paper_size: PaperSize | None = None
    margin_top: float | None = None
    margin_bottom: float | None = None
    margin_left: float | None = None
    margin_right: float | None = None
    header_left: str | None = None
    header_center: str | None = None
    header_right: str | None = None
    footer_left: str | None = None
    footer_center: str | None = None
    footer_right: str | None = None
    header: HeaderFooterConfig | None = None
    footer: HeaderFooterConfig | None = None
    header_first_page: HeaderFooterConfig | None = None
    footer_first_page: HeaderFooterConfig | None = None
    header_even_pages: HeaderFooterConfig | None = None
    footer_even_pages: HeaderFooterConfig | None = None
    header_footer_font_name: str | None = None
    header_footer_font_size: float | None = None
    header_footer_color: str | None = None
