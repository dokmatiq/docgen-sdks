/** Result of AI-powered invoice data extraction. */
export interface ExtractionResult {
  invoiceNumber?: string;
  invoiceDate?: string;
  sellerName?: string;
  buyerName?: string;
  totalAmount?: number;
  currency?: string;
  confidence?: number;
  rawData?: Record<string, unknown>;
}
