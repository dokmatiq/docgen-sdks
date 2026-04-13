/** Output document format. */
export const OutputFormat = {
  PDF: "PDF",
  DOCX: "DOCX",
  ODT: "ODT",
} as const;
export type OutputFormat = (typeof OutputFormat)[keyof typeof OutputFormat];

/** Standard paper sizes. */
export const PaperSize = {
  A4: "A4",
  A3: "A3",
  A5: "A5",
  LETTER: "LETTER",
  LEGAL: "LEGAL",
} as const;
export type PaperSize = (typeof PaperSize)[keyof typeof PaperSize];

/** Page orientation. */
export const PageOrientation = {
  PORTRAIT: "PORTRAIT",
  LANDSCAPE: "LANDSCAPE",
} as const;
export type PageOrientation =
  (typeof PageOrientation)[keyof typeof PageOrientation];

/** Text alignment. */
export const TextAlignment = {
  LEFT: "LEFT",
  CENTER: "CENTER",
  RIGHT: "RIGHT",
} as const;
export type TextAlignment =
  (typeof TextAlignment)[keyof typeof TextAlignment];

/** Barcode formats. */
export const BarcodeFormat = {
  CODE_128: "CODE_128",
  CODE_39: "CODE_39",
  EAN_13: "EAN_13",
  EAN_8: "EAN_8",
  UPC_A: "UPC_A",
  QR_CODE: "QR_CODE",
  DATA_MATRIX: "DATA_MATRIX",
  PDF_417: "PDF_417",
} as const;
export type BarcodeFormat =
  (typeof BarcodeFormat)[keyof typeof BarcodeFormat];

/** Async job status. */
export const JobStatus = {
  PENDING: "PENDING",
  PROCESSING: "PROCESSING",
  COMPLETED: "COMPLETED",
  FAILED: "FAILED",
} as const;
export type JobStatus = (typeof JobStatus)[keyof typeof JobStatus];

/** XRechnung XML format. */
export const XRechnungFormat = {
  CII: "CII",
  UBL: "UBL",
} as const;
export type XRechnungFormat =
  (typeof XRechnungFormat)[keyof typeof XRechnungFormat];

/** Column number format. */
export const ColumnFormat = {
  TEXT: "TEXT",
  NUMBER: "NUMBER",
  CURRENCY: "CURRENCY",
  PERCENTAGE: "PERCENTAGE",
} as const;
export type ColumnFormat = (typeof ColumnFormat)[keyof typeof ColumnFormat];

/** ZUGFeRD profile level. */
export const ZugferdProfile = {
  MINIMUM: "MINIMUM",
  BASIC_WL: "BASIC_WL",
  BASIC: "BASIC",
  EN16931: "EN16931",
  EXTENDED: "EXTENDED",
  XRECHNUNG: "XRECHNUNG",
} as const;
export type ZugferdProfile =
  (typeof ZugferdProfile)[keyof typeof ZugferdProfile];

/** Invoice unit codes (UN/ECE Recommendation 20). */
export const InvoiceUnit = {
  PIECE: "C62",
  HOUR: "HUR",
  DAY: "DAY",
  KILOGRAM: "KGM",
  METER: "MTR",
  LITER: "LTR",
  SQUARE_METER: "MTK",
  CUBIC_METER: "MTQ",
  SET: "SET",
  PACKAGE: "PK",
} as const;
export type InvoiceUnit = (typeof InvoiceUnit)[keyof typeof InvoiceUnit];
