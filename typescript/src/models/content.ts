import type { TextAlignment } from "./enums.js";

/** Diagonal watermark overlay configuration. */
export interface WatermarkConfig {
  text: string;
  fontSize?: number;
  opacity?: number;
  color?: string;
}

/** Stationery (letterhead) PDF background configuration. */
export interface StationeryConfig {
  pdfBase64: string;
  firstPagePdfBase64?: string;
}

/** Absolutely positioned content area on the PDF page. */
export interface ContentArea {
  x: number;
  y: number;
  width: number;
  text?: string;
  html?: string;
  imageBase64?: string;
  fontSize?: number;
  fontFamily?: string;
  color?: string;
  alignment?: TextAlignment;
  pages?: string;
}
