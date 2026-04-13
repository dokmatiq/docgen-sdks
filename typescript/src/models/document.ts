import type { OutputFormat } from "./enums.js";
import type { ContentArea, StationeryConfig, WatermarkConfig } from "./content.js";
import type { InvoiceData } from "./invoice.js";
import type { BarcodeData, ImageData, QrCodeData, TableData } from "./media.js";
import type { PageSettings } from "./page.js";

/** Markdown rendering style overrides. */
export interface MarkdownStyles {
  [key: string]: string;
}

/** Main document generation request. */
export interface DocumentRequest {
  htmlContent?: string;
  markdownContent?: string;
  templateName?: string;
  templateBase64?: string;
  fields?: Record<string, string>;
  bookmarks?: Record<string, string>;
  markdownBookmarks?: Record<string, string>;
  images?: ImageData[];
  qrCodes?: QrCodeData[];
  barcodes?: BarcodeData[];
  tables?: Record<string, TableData>;
  pageSettings?: PageSettings;
  watermark?: string | WatermarkConfig;
  stationery?: StationeryConfig;
  contentAreas?: ContentArea[];
  invoiceData?: InvoiceData;
  password?: string;
  outputFormat?: OutputFormat;
  callbackUrl?: string;
  callbackSecret?: string;
  markdownStyles?: MarkdownStyles;
}

/** A single part in a multi-part composed document. */
export interface DocumentPart {
  htmlContent?: string;
  markdownContent?: string;
  templateName?: string;
  templateBase64?: string;
  fields?: Record<string, string>;
  bookmarks?: Record<string, string>;
  images?: ImageData[];
  qrCodes?: QrCodeData[];
  barcodes?: BarcodeData[];
  tables?: Record<string, TableData>;
  pageSettings?: PageSettings;
}

/** Multi-part document composition request. */
export interface ComposeRequest {
  parts: DocumentPart[];
  watermark?: string | WatermarkConfig;
  stationery?: StationeryConfig;
  contentAreas?: ContentArea[];
  invoiceData?: InvoiceData;
  password?: string;
  outputFormat?: OutputFormat;
  callbackUrl?: string;
  callbackSecret?: string;
}
