import { Transport } from '../transport.js';

/** Client for AI-powered receipt and ticket data extraction. */
export class ReceiptsClient {
  constructor(private readonly transport: Transport) {}

  /** Extract structured data from a receipt image or PDF. Requires AI processing consent in portal settings. */
  async extract(file: Buffer, fileName: string): Promise<ReceiptExtractionResult> {
    return this.transport.upload<ReceiptExtractionResult>('/api/receipts/extract', 'file', file, fileName);
  }

  /** Extract data from multiple receipts sequentially. Convenience wrapper around extract(). */
  async extractBatch(files: Array<{ buffer: Buffer; name: string }>): Promise<BatchExtractionResult> {
    const results: BatchItemResult[] = [];
    let successCount = 0;
    for (let i = 0; i < files.length; i++) {
      try {
        const result = await this.extract(files[i].buffer, files[i].name);
        results.push({ index: i, filename: files[i].name, success: true, result });
        successCount++;
      } catch (e) {
        results.push({ index: i, filename: files[i].name, success: false, error: String(e) });
      }
    }
    return {
      totalFiles: files.length,
      successCount,
      failureCount: files.length - successCount,
      results,
    };
  }

  /** Submit receipt for async extraction with optional webhook callback. */
  async extractAsync(file: Buffer, fileName: string, options?: {
    callbackUrl?: string;
    callbackSecret?: string;
  }): Promise<ReceiptJob> {
    const extraFields: Record<string, string> = {};
    if (options?.callbackUrl) extraFields.callbackUrl = options.callbackUrl;
    if (options?.callbackSecret) extraFields.callbackSecret = options.callbackSecret;
    return this.transport.upload<ReceiptJob>('/api/receipts/extract-async', 'file', file, fileName, extraFields);
  }

  /** Extract receipt and generate an expense report document. */
  async toDocument(file: Buffer, fileName: string, options?: {
    format?: string;
    templateName?: string;
    title?: string;
  }): Promise<ReceiptToDocumentResult> {
    const extraFields: Record<string, string> = {};
    if (options?.format) extraFields.format = options.format;
    if (options?.templateName) extraFields.templateName = options.templateName;
    if (options?.title) extraFields.title = options.title;
    return this.transport.upload<ReceiptToDocumentResult>('/api/receipts/to-document', 'file', file, fileName, extraFields);
  }

  /** Export receipt data as CSV (DATEV-compatible). */
  async exportCsv(receipts: ReceiptData[]): Promise<Buffer> {
    return this.transport.requestBytes('POST', '/api/receipts/export/csv', receipts);
  }

  /** Export receipt data as Excel (XLSX). */
  async exportXlsx(receipts: ReceiptData[]): Promise<Buffer> {
    return this.transport.requestBytes('POST', '/api/receipts/export/xlsx', receipts);
  }

  /** Get async job status. */
  async getJob(jobId: string): Promise<ReceiptJob> {
    return this.transport.requestJson<ReceiptJob>('GET', `/api/receipts/jobs/${jobId}`);
  }

  /** Get async job result. */
  async getJobResult(jobId: string): Promise<ReceiptExtractionResult> {
    return this.transport.requestJson<ReceiptExtractionResult>('GET', `/api/receipts/jobs/${jobId}/result`);
  }

  /** List all async jobs. */
  async listJobs(): Promise<ReceiptJob[]> {
    return this.transport.requestJson<ReceiptJob[]>('GET', '/api/receipts/jobs');
  }
}

// -- Types -------------------------------------------------------------------

export interface VatBreakdown {
  rate: number;
  netAmount: number;
  vatAmount: number;
  grossAmount: number;
}

export interface LineItem {
  description: string;
  quantity?: number;
  unitPrice?: number;
  totalPrice?: number;
  vatRate?: number;
}

export interface ReceiptData {
  receiptType?: string;
  issuer?: string;
  date?: string;
  time?: string;
  totalAmount?: number;
  netAmount?: number;
  currency?: string;
  vatBreakdown?: VatBreakdown[];
  items?: LineItem[];
  paymentMethod?: string;
  referenceNumber?: string;
  tipAmount?: number;
  taxNumber?: string;
  vatId?: string;
  issuerAddress?: string;
  language?: string;
  country?: string;
  skr03Account?: string;
  skr03Description?: string;
  skr04Account?: string;
  skr04Description?: string;
  expenseCategory?: string;
  metadata?: Record<string, unknown>;
}

export interface ReceiptExtractionResult {
  receiptData: ReceiptData;
  missingFields?: string[];
  uncertainFields?: string[];
  warnings?: string[];
  qualityHints?: string[];
  inputType?: string;
  aiExtractionUsed?: boolean;
  confidence?: number;
  message?: string;
}

export interface BatchItemResult {
  index: number;
  filename: string;
  success: boolean;
  result?: ReceiptExtractionResult;
  error?: string;
}

export interface BatchExtractionResult {
  totalFiles: number;
  successCount: number;
  failureCount: number;
  results: BatchItemResult[];
}

export interface ReceiptJob {
  jobId: string;
  status: string;
  filename?: string;
  result?: ReceiptExtractionResult;
  error?: string;
  createdAt?: string;
  completedAt?: string;
  durationMs?: number;
}

export interface ReceiptToDocumentResult {
  extraction: ReceiptExtractionResult;
  generatedHtml?: string;
  suggestedFilename?: string;
}
