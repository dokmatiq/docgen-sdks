import type { Transport } from "../transport.js";
import { toBase64, type FileInput } from "../files.js";

interface PdfMetadata {
  title?: string;
  author?: string;
  subject?: string;
  keywords?: string;
  creator?: string;
  producer?: string;
  pageCount?: number;
}

/** Client for PDF manipulation tools. */
export class PdfToolsClient {
  constructor(private readonly transport: Transport) {}

  /** Merge multiple PDFs into one. */
  async merge(files: FileInput[]): Promise<Buffer> {
    const pdfs = files.map((f) => toBase64(f));
    return this.transport.requestBytes("POST", "/api/pdf-tools/merge", {
      pdfs,
    });
  }

  /** Split a PDF by page ranges. */
  async split(
    file: FileInput,
    ranges: string[],
  ): Promise<Buffer[]> {
    const base64 = toBase64(file);
    return this.transport.requestJson<Buffer[]>(
      "POST",
      "/api/pdf-tools/split",
      { pdfBase64: base64, ranges },
    );
  }

  /** Extract text content from a PDF. */
  async extractText(file: FileInput): Promise<string> {
    const base64 = toBase64(file);
    const result = await this.transport.requestJson<{ text: string }>(
      "POST",
      "/api/pdf-tools/extract-text",
      { pdfBase64: base64 },
    );
    return result.text;
  }

  /** Get PDF metadata. */
  async getMetadata(file: FileInput): Promise<PdfMetadata> {
    const base64 = toBase64(file);
    return this.transport.requestJson<PdfMetadata>(
      "POST",
      "/api/pdf-tools/metadata",
      { pdfBase64: base64 },
    );
  }

  /** Set PDF metadata. */
  async setMetadata(
    file: FileInput,
    metadata: Omit<PdfMetadata, "pageCount">,
  ): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/pdf-tools/metadata/set", {
      pdfBase64: base64,
      ...metadata,
    });
  }

  /** Convert a PDF to PDF/A format. */
  async toPdfA(file: FileInput): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/pdf-tools/pdfa", {
      pdfBase64: base64,
    });
  }

  /** Rotate pages in a PDF. */
  async rotate(
    file: FileInput,
    angle: number,
    pages?: string,
  ): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/pdf-tools/rotate", {
      pdfBase64: base64,
      angle,
      pages,
    });
  }
}
