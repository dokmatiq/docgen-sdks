import type { DocumentsClient } from "../clients/documents.js";
import type {
  ContentArea,
  StationeryConfig,
  WatermarkConfig,
} from "../models/content.js";
import type {
  DocumentRequest,
  MarkdownStyles,
} from "../models/document.js";
import type { OutputFormat, BarcodeFormat } from "../models/enums.js";
import type { InvoiceData } from "../models/invoice.js";
import type {
  BarcodeData,
  ImageData,
  QrCodeData,
  TableData,
} from "../models/media.js";
import type { PageSettings } from "../models/page.js";
import { toBase64, type FileInput } from "../files.js";

/**
 * Fluent builder for constructing and executing document generation requests.
 *
 * @example
 * ```ts
 * const pdf = await dg.document()
 *   .html('<h1>Invoice {{nr}}</h1>')
 *   .template('invoice.odt')
 *   .field('nr', '2026-001')
 *   .watermark('DRAFT')
 *   .asPdf()
 *   .generate();
 * ```
 */
export class DocumentBuilder {
  private readonly request: DocumentRequest = {};
  private client?: DocumentsClient;

  /** @internal Attach a client for direct generation. */
  _setClient(client: DocumentsClient): this {
    this.client = client;
    return this;
  }

  /** Set the HTML content. */
  html(content: string): this {
    this.request.htmlContent = content;
    return this;
  }

  /** Set the Markdown content. */
  markdown(content: string): this {
    this.request.markdownContent = content;
    return this;
  }

  /** Set the template by name (must be pre-uploaded). */
  template(name: string): this {
    this.request.templateName = name;
    return this;
  }

  /** Set the template from a file (uploaded inline as base64). */
  templateFile(file: FileInput): this {
    this.request.templateBase64 = toBase64(file);
    return this;
  }

  /** Set a single template field. */
  field(name: string, value: string): this {
    this.request.fields ??= {};
    this.request.fields[name] = value;
    return this;
  }

  /** Set multiple template fields at once. */
  fields(values: Record<string, string>): this {
    this.request.fields = { ...this.request.fields, ...values };
    return this;
  }

  /** Set a bookmark replacement. */
  bookmark(name: string, html: string): this {
    this.request.bookmarks ??= {};
    this.request.bookmarks[name] = html;
    return this;
  }

  /** Set a markdown bookmark replacement. */
  markdownBookmark(name: string, markdown: string): this {
    this.request.markdownBookmarks ??= {};
    this.request.markdownBookmarks[name] = markdown;
    return this;
  }

  /** Add an image at a bookmark. */
  image(bookmarkName: string, file: FileInput, options?: Omit<ImageData, "bookmarkName" | "base64">): this {
    this.request.images ??= [];
    this.request.images.push({
      bookmarkName,
      base64: toBase64(file),
      ...options,
    });
    return this;
  }

  /** Add a QR code at a bookmark. */
  qrCode(bookmarkName: string, content: string, options?: Omit<QrCodeData, "bookmarkName" | "content">): this {
    this.request.qrCodes ??= [];
    this.request.qrCodes.push({ bookmarkName, content, ...options });
    return this;
  }

  /** Add a barcode at a bookmark. */
  barcode(
    bookmarkName: string,
    content: string,
    format?: BarcodeFormat,
    options?: Omit<BarcodeData, "bookmarkName" | "content" | "format">,
  ): this {
    this.request.barcodes ??= [];
    this.request.barcodes.push({
      bookmarkName,
      content,
      format,
      ...options,
    });
    return this;
  }

  /** Add table data at a named position. */
  table(name: string, data: TableData): this {
    this.request.tables ??= {};
    this.request.tables[name] = data;
    return this;
  }

  /** Set page layout settings. */
  pageSettings(settings: PageSettings): this {
    this.request.pageSettings = settings;
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

  /** Attach structured invoice data (ZUGFeRD/XRechnung). */
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

  /** Shorthand: set output to ODT. */
  asOdt(): this {
    this.request.outputFormat = "ODT";
    return this;
  }

  /** Set the async callback URL. */
  callback(url: string, secret?: string): this {
    this.request.callbackUrl = url;
    if (secret) {
      this.request.callbackSecret = secret;
    }
    return this;
  }

  /** Set Markdown rendering style overrides. */
  markdownStyles(styles: MarkdownStyles): this {
    this.request.markdownStyles = styles;
    return this;
  }

  /** Build the DocumentRequest object without executing. */
  build(): DocumentRequest {
    return { ...this.request };
  }

  /** Generate the document (requires attached client). */
  async generate(): Promise<Buffer> {
    if (!this.client) {
      throw new Error(
        "No client attached. Use dg.document() or pass the request to dg.documents.generate().",
      );
    }
    return this.client.generate(this.build());
  }
}
