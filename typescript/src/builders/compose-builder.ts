import type { DocumentsClient } from "../clients/documents.js";
import type {
  ContentArea,
  StationeryConfig,
  WatermarkConfig,
} from "../models/content.js";
import type { ComposeRequest, DocumentPart } from "../models/document.js";
import type { OutputFormat } from "../models/enums.js";
import type { InvoiceData } from "../models/invoice.js";
import { toBase64, type FileInput } from "../files.js";

/**
 * Fluent builder for multi-part document composition.
 *
 * @example
 * ```ts
 * const pdf = await dg.compose()
 *   .part({ htmlContent: '<h1>Cover</h1>' })
 *   .part({ htmlContent: '<h1>Chapter 1</h1>', templateName: 'report.odt' })
 *   .watermark('CONFIDENTIAL')
 *   .asPdf()
 *   .generate();
 * ```
 */
export class ComposeBuilder {
  private readonly request: ComposeRequest = { parts: [] };
  private client?: DocumentsClient;

  /** @internal Attach a client for direct generation. */
  _setClient(client: DocumentsClient): this {
    this.client = client;
    return this;
  }

  /** Add a document part. */
  part(p: DocumentPart): this {
    this.request.parts.push(p);
    return this;
  }

  /** Add a diagonal watermark overlay. */
  watermark(text: string, options?: Omit<WatermarkConfig, "text">): this {
    if (options) {
      this.request.watermark = { text, ...options };
    } else {
      this.request.watermark = text;
    }
    return this;
  }

  /** Set stationery (letterhead) PDF background. */
  stationery(file: FileInput, firstPageFile?: FileInput): this {
    const config: StationeryConfig = { pdfBase64: toBase64(file) };
    if (firstPageFile) {
      config.firstPagePdfBase64 = toBase64(firstPageFile);
    }
    this.request.stationery = config;
    return this;
  }

  /** Add an absolutely positioned content area. */
  contentArea(area: ContentArea): this {
    this.request.contentAreas ??= [];
    this.request.contentAreas.push(area);
    return this;
  }

  /** Attach structured invoice data. */
  invoice(data: InvoiceData): this {
    this.request.invoiceData = data;
    return this;
  }

  /** Set a password for the output document. */
  password(pwd: string): this {
    this.request.password = pwd;
    return this;
  }

  /** Set the output format. */
  outputFormat(format: OutputFormat): this {
    this.request.outputFormat = format;
    return this;
  }

  /** Shorthand: set output to PDF. */
  asPdf(): this {
    this.request.outputFormat = "PDF";
    return this;
  }

  /** Shorthand: set output to DOCX. */
  asDocx(): this {
    this.request.outputFormat = "DOCX";
    return this;
  }

  /** Build the ComposeRequest without executing. */
  build(): ComposeRequest {
    return { ...this.request, parts: [...this.request.parts] };
  }

  /** Generate the composed document (requires attached client). */
  async generate(): Promise<Buffer> {
    if (!this.client) {
      throw new Error(
        "No client attached. Use dg.compose() or pass the request to dg.documents.compose().",
      );
    }
    return this.client.compose(this.build());
  }
}
