"""Client for Excel workbook generation and conversion."""

from __future__ import annotations

from typing import Any

from docgen._transport import Transport


class ExcelClient:
    """Client for Excel workbook operations."""

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    # ── Generate from JSON structure ─────────────────────────────────

    def generate(self, request: dict[str, Any]) -> bytes:
        """Generate an Excel workbook from a structured JSON definition.

        Returns raw XLSX bytes.
        """
        return self._t.request_bytes("POST", "/api/excel/generate", json=request)

    # ── CSV ↔ XLSX ───────────────────────────────────────────────────

    def from_csv(
        self,
        csv_content: str,
        *,
        delimiter: str = ",",
        has_header: bool = True,
        sheet_name: str | None = None,
    ) -> bytes:
        """Convert CSV content to an Excel workbook. Returns XLSX bytes."""
        body: dict[str, Any] = {
            "csvContent": csv_content,
            "delimiter": delimiter,
            "hasHeader": has_header,
        }
        if sheet_name:
            body["sheetName"] = sheet_name
        return self._t.request_bytes("POST", "/api/excel/from-csv", json=body)

    def to_csv(
        self,
        excel_base64: str,
        *,
        sheet_index: int = 0,
        delimiter: str = ",",
    ) -> str:
        """Convert an Excel sheet to CSV text."""
        body = {
            "excelBase64": excel_base64,
            "sheetIndex": sheet_index,
            "delimiter": delimiter,
        }
        raw = self._t.request_bytes("POST", "/api/excel/to-csv", json=body)
        return raw.decode("utf-8")

    # ── XLSX → JSON ──────────────────────────────────────────────────

    def to_json(
        self,
        excel_base64: str,
        *,
        sheet_index: int = 0,
        has_header: bool = True,
    ) -> dict[str, Any]:
        """Convert an Excel sheet to structured JSON."""
        body = {
            "excelBase64": excel_base64,
            "sheetIndex": sheet_index,
            "hasHeader": has_header,
        }
        return self._t.request_json("POST", "/api/excel/to-json", json=body)

    # ── Fill template ────────────────────────────────────────────────

    def fill_template(
        self,
        template_base64: str,
        *,
        values: dict[str, Any] | None = None,
        tables: dict[str, list[list[Any]]] | None = None,
        recalculate: bool = True,
        password: str | None = None,
    ) -> bytes:
        """Fill an Excel template with data. Returns XLSX bytes."""
        body: dict[str, Any] = {
            "templateBase64": template_base64,
            "recalculate": recalculate,
        }
        if values:
            body["values"] = values
        if tables:
            body["tables"] = tables
        if password:
            body["password"] = password
        return self._t.request_bytes("POST", "/api/excel/fill-template", json=body)

    # ── Inspect ──────────────────────────────────────────────────────

    def inspect(self, excel_base64: str) -> dict[str, Any]:
        """Inspect an Excel workbook and return metadata."""
        return self._t.request_json("POST", "/api/excel/inspect", json={
            "excelBase64": excel_base64,
        })
