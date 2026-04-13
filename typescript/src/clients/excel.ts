import { Transport } from '../transport.js';

/** Client for Excel workbook generation and conversion. */
export class ExcelClient {
  constructor(private readonly transport: Transport) {}

  /** Generate an Excel workbook from a structured JSON definition. Returns XLSX bytes. */
  async generate(request: ExcelRequest): Promise<Buffer> {
    return this.transport.requestBytes('POST', '/api/excel/generate', request);
  }

  /** Convert CSV content to an Excel workbook. Returns XLSX bytes. */
  async fromCsv(csvContent: string, options?: {
    delimiter?: string;
    hasHeader?: boolean;
    sheetName?: string;
  }): Promise<Buffer> {
    return this.transport.requestBytes('POST', '/api/excel/from-csv', {
      csvContent,
      delimiter: options?.delimiter ?? ',',
      hasHeader: options?.hasHeader ?? true,
      sheetName: options?.sheetName,
    });
  }

  /** Convert an Excel sheet to CSV text. */
  async toCsv(excelBase64: string, options?: {
    sheetIndex?: number;
    delimiter?: string;
  }): Promise<string> {
    const res = await this.transport.requestJson('POST', '/api/excel/to-csv', {
      excelBase64,
      sheetIndex: options?.sheetIndex ?? 0,
      delimiter: options?.delimiter ?? ',',
    });
    return typeof res === 'string' ? res : JSON.stringify(res);
  }

  /** Convert an Excel sheet to structured JSON. */
  async toJson(excelBase64: string, options?: {
    sheetIndex?: number;
    hasHeader?: boolean;
  }): Promise<ExcelJsonResult> {
    return this.transport.requestJson('POST', '/api/excel/to-json', {
      excelBase64,
      sheetIndex: options?.sheetIndex ?? 0,
      hasHeader: options?.hasHeader ?? true,
    }) as Promise<ExcelJsonResult>;
  }

  /** Fill an Excel template with data. Returns XLSX bytes. */
  async fillTemplate(templateBase64: string, options?: {
    values?: Record<string, unknown>;
    tables?: Record<string, unknown[][]>;
    recalculate?: boolean;
    password?: string;
  }): Promise<Buffer> {
    return this.transport.requestBytes('POST', '/api/excel/fill-template', {
      templateBase64,
      values: options?.values,
      tables: options?.tables,
      recalculate: options?.recalculate ?? true,
      password: options?.password,
    });
  }

  /** Inspect an Excel workbook and return metadata. */
  async inspect(excelBase64: string): Promise<ExcelInspectResult> {
    return this.transport.requestJson('POST', '/api/excel/inspect', {
      excelBase64,
    }) as Promise<ExcelInspectResult>;
  }
}

// ── Types ─────────────────────────────────────────────────────────

export interface ExcelRequest {
  sheets: SheetDefinition[];
  properties?: Record<string, string>;
  password?: string;
}

export interface SheetDefinition {
  name?: string;
  columns?: ExcelColumnDef[];
  rows?: ExcelRow[];
  cells?: ExcelCell[];
  formulas?: ExcelFormula[];
  mergedRegions?: string[];
  namedRanges?: ExcelNamedRange[];
  headerFooter?: ExcelHeaderFooter;
  printArea?: string;
  freezePane?: { row: number; col: number };
  headerStyle?: ExcelCellStyle;
  dataStyle?: ExcelCellStyle;
  defaultColumnWidth?: number;
  defaultRowHeight?: number;
  autoSizeColumns?: boolean;
  autoFilter?: boolean;
  pageOrientation?: 'PORTRAIT' | 'LANDSCAPE';
  fitToPage?: boolean;
  protectionPassword?: string;
}

export interface ExcelColumnDef {
  index?: number;
  header?: string;
  width?: number;
  format?: string;
  align?: 'LEFT' | 'CENTER' | 'RIGHT';
  headerStyle?: ExcelCellStyle;
  dataStyle?: ExcelCellStyle;
}

export interface ExcelRow {
  index?: number;
  values?: unknown[];
  cells?: ExcelCell[];
  height?: number;
  style?: ExcelCellStyle;
}

export interface ExcelCell {
  ref?: string;
  column?: number;
  value?: unknown;
  type?: 'STRING' | 'NUMERIC' | 'BOOLEAN' | 'DATE' | 'FORMULA' | 'BLANK';
  formula?: string;
  format?: string;
  style?: ExcelCellStyle;
  comment?: string;
  hyperlink?: string;
}

export interface ExcelFormula {
  cell: string;
  formula: string;
  label?: string;
  format?: string;
  style?: ExcelCellStyle;
}

export interface ExcelNamedRange {
  name: string;
  range: string;
}

export interface ExcelHeaderFooter {
  header?: string;
  footer?: string;
  headerLeft?: string;
  headerCenter?: string;
  headerRight?: string;
  footerLeft?: string;
  footerCenter?: string;
  footerRight?: string;
}

export interface ExcelCellStyle {
  fontName?: string;
  fontSize?: number;
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
  strikethrough?: boolean;
  fontColor?: string;
  backgroundColor?: string;
  fillPattern?: string;
  horizontalAlignment?: 'LEFT' | 'CENTER' | 'RIGHT' | 'JUSTIFY' | 'FILL';
  verticalAlignment?: 'TOP' | 'CENTER' | 'BOTTOM' | 'JUSTIFY';
  wrapText?: boolean;
  rotation?: number;
  indent?: number;
  borderStyle?: 'NONE' | 'THIN' | 'MEDIUM' | 'THICK' | 'DOUBLE' | 'DOTTED' | 'DASHED';
  borderColor?: string;
  numberFormat?: string;
}

export interface ExcelJsonResult {
  sheetName: string;
  totalRows: number;
  headers?: string[];
  data: Record<string, unknown>[];
}

export interface ExcelInspectResult {
  sheetCount: number;
  sheets: Array<{
    index: number;
    name: string;
    rows: number;
    columns?: number;
  }>;
  namedRanges?: Array<{
    name: string;
    range: string;
  }>;
}
