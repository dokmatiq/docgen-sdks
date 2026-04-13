import { type DocGenConfig, resolveConfig } from "./config.js";
import { Transport } from "./transport.js";
import { DocumentsClient } from "./clients/documents.js";
import { TemplatesClient } from "./clients/templates.js";
import { FontsClient } from "./clients/fonts.js";
import { PdfFormsClient } from "./clients/pdf-forms.js";
import { SignaturesClient } from "./clients/signatures.js";
import { PdfToolsClient } from "./clients/pdf-tools.js";
import { PreviewClient } from "./clients/preview.js";
import { ZugferdClient } from "./clients/zugferd.js";
import { XRechnungClient } from "./clients/xrechnung.js";
import { ExcelClient } from "./clients/excel.js";
import { DocumentBuilder } from "./builders/document-builder.js";
import { ComposeBuilder } from "./builders/compose-builder.js";
import { InvoiceBuilder } from "./builders/invoice-builder.js";
import type { FileInput } from "./files.js";

/**
 * Main DocGen SDK client.
 *
 * @example
 * ```ts
 * const dg = new DocGen({ apiKey: 'dk_live_xxx' });
 *
 * // One-liner
 * const pdf = await dg.htmlToPdf('<h1>Hello World</h1>');
 *
 * // Builder
 * const invoice = await dg.document()
 *   .html('<h1>Rechnung</h1>')
 *   .template('invoice.odt')
 *   .field('nr', '2026-001')
 *   .asPdf()
 *   .generate();
 * ```
 */
export class DocGen {
  private readonly transport: Transport;

  /** Document generation and async jobs. */
  readonly documents: DocumentsClient;
  /** Template management. */
  readonly templates: TemplatesClient;
  /** Font management. */
  readonly fonts: FontsClient;
  /** PDF form inspection and filling. */
  readonly pdfForms: PdfFormsClient;
  /** Digital signature operations. */
  readonly signatures: SignaturesClient;
  /** PDF manipulation tools. */
  readonly pdfTools: PdfToolsClient;
  /** PDF page preview rendering. */
  readonly preview: PreviewClient;
  /** ZUGFeRD/Factur-X operations. */
  readonly zugferd: ZugferdClient;
  /** XRechnung operations. */
  readonly xrechnung: XRechnungClient;
  /** Excel workbook generation and conversion. */
  readonly excel: ExcelClient;

  constructor(config: DocGenConfig) {
    const resolved = resolveConfig(config);
    this.transport = new Transport(resolved);

    this.documents = new DocumentsClient(this.transport);
    this.templates = new TemplatesClient(this.transport);
    this.fonts = new FontsClient(this.transport);
    this.pdfForms = new PdfFormsClient(this.transport);
    this.signatures = new SignaturesClient(this.transport);
    this.pdfTools = new PdfToolsClient(this.transport);
    this.preview = new PreviewClient(this.transport);
    this.zugferd = new ZugferdClient(this.transport);
    this.xrechnung = new XRechnungClient(this.transport);
    this.excel = new ExcelClient(this.transport);
  }

  // ── Builder entry points ──────────────────────────────────────────

  /** Create a DocumentBuilder for fluent document construction. */
  document(): DocumentBuilder {
    return new DocumentBuilder()._setClient(this.documents);
  }

  /** Create a ComposeBuilder for multi-part document composition. */
  compose(): ComposeBuilder {
    return new ComposeBuilder()._setClient(this.documents);
  }

  /** Create an InvoiceBuilder for structured invoice data. */
  invoice(): InvoiceBuilder {
    return new InvoiceBuilder();
  }

  // ── Convenience methods ───────────────────────────────────────────

  /** Convert HTML to PDF in one call. */
  async htmlToPdf(html: string): Promise<Buffer> {
    return this.documents.generate({
      htmlContent: html,
      outputFormat: "PDF",
    });
  }

  /** Convert Markdown to PDF in one call. */
  async markdownToPdf(markdown: string): Promise<Buffer> {
    return this.documents.generate({
      markdownContent: markdown,
      outputFormat: "PDF",
    });
  }

  /** Merge multiple PDF files into one. */
  async mergePdfs(files: FileInput[]): Promise<Buffer> {
    return this.pdfTools.merge(files);
  }

  /** Sign a PDF with a certificate. */
  async signPdf(
    file: FileInput,
    certificateName: string,
    certificatePassword: string,
  ): Promise<Buffer> {
    return this.signatures.sign(file, certificateName, certificatePassword);
  }

  /** Fill form fields in a PDF. */
  async fillForm(
    file: FileInput,
    fields: Record<string, string>,
    flatten = false,
  ): Promise<Buffer> {
    return this.pdfForms.fill(file, fields, flatten);
  }
}
