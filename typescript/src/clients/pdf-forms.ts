import type { Transport } from "../transport.js";
import type { PdfFormField } from "../models/forms.js";
import { toBase64, type FileInput } from "../files.js";

/** Client for PDF form inspection and filling. */
export class PdfFormsClient {
  constructor(private readonly transport: Transport) {}

  /** Inspect form fields in a PDF. */
  async inspectFields(file: FileInput): Promise<PdfFormField[]> {
    const base64 = toBase64(file);
    return this.transport.requestJson<PdfFormField[]>(
      "POST",
      "/api/pdf-forms/inspect",
      { pdfBase64: base64 },
    );
  }

  /** Fill form fields in a PDF. */
  async fill(
    file: FileInput,
    fields: Record<string, string>,
    flatten = false,
  ): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/pdf-forms/fill", {
      pdfBase64: base64,
      fields,
      flatten,
    });
  }
}
