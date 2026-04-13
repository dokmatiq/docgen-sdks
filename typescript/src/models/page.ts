import type { PageOrientation, PaperSize } from "./enums.js";

/** Header/footer configuration with left/center/right sections. */
export interface HeaderFooterConfig {
  left?: string;
  center?: string;
  right?: string;
  fontSize?: number;
  fontFamily?: string;
  color?: string;
}

/** Page layout and margin settings. */
export interface PageSettings {
  paperSize?: PaperSize;
  orientation?: PageOrientation;
  marginTop?: number;
  marginBottom?: number;
  marginLeft?: number;
  marginRight?: number;
  header?: HeaderFooterConfig;
  footer?: HeaderFooterConfig;
  firstPageHeader?: HeaderFooterConfig;
  firstPageFooter?: HeaderFooterConfig;
  evenPageHeader?: HeaderFooterConfig;
  evenPageFooter?: HeaderFooterConfig;
}
