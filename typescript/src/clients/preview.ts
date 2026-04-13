import type { Transport } from "../transport.js";
import type { PreviewResponse } from "../models/preview.js";
import { toBase64, type FileInput } from "../files.js";

/** Client for PDF page preview rendering. */
export class PreviewClient {
  constructor(private readonly transport: Transport) {}

  /** Render a single page as a PNG image. */
  async previewPage(
    file: FileInput,
    page = 1,
    dpi = 150,
  ): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/preview/page", {
      pdfBase64: base64,
      page,
      dpi,
    });
  }

  /** Render multiple pages as preview images. */
  async previewPages(
    file: FileInput,
    pages?: number[],
    dpi = 150,
  ): Promise<PreviewResponse> {
    const base64 = toBase64(file);
    return this.transport.requestJson<PreviewResponse>(
      "POST",
      "/api/preview/pages",
      { pdfBase64: base64, pages, dpi },
    );
  }

  /** Get the total page count of a PDF. */
  async pageCount(file: FileInput): Promise<number> {
    const base64 = toBase64(file);
    const result = await this.transport.requestJson<{ pageCount: number }>(
      "POST",
      "/api/preview/page-count",
      { pdfBase64: base64 },
    );
    return result.pageCount;
  }
}
