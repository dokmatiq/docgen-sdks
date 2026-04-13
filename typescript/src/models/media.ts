import type { BarcodeFormat, ColumnFormat, TextAlignment } from "./enums.js";

/** Embedded image data for a document bookmark. */
export interface ImageData {
  bookmarkName: string;
  base64: string;
  width?: number;
  height?: number;
  altText?: string;
}

/** QR code data for a document bookmark. */
export interface QrCodeData {
  bookmarkName: string;
  content: string;
  width?: number;
  height?: number;
  errorCorrectionLevel?: string;
}

/** Barcode data for a document bookmark. */
export interface BarcodeData {
  bookmarkName: string;
  content: string;
  format?: BarcodeFormat;
  width?: number;
  height?: number;
}

/** Column definition for table data. */
export interface ColumnDef {
  header: string;
  width?: number;
  alignment?: TextAlignment;
  format?: ColumnFormat;
}

/** Table styling options. */
export interface TableStyle {
  borderColor?: string;
  headerBackground?: string;
  headerTextColor?: string;
  alternateRowBackground?: string;
  fontSize?: number;
}

/** Table data with columns, rows, and optional styling. */
export interface TableData {
  columns: ColumnDef[];
  rows: string[][];
  style?: TableStyle;
}
