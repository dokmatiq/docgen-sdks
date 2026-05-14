import type { Transport } from "../transport.js";
import type { InvoiceData } from "../models/invoice.js";
import { toBase64, type FileInput } from "../files.js";

interface ZugferdValidationResult {
  valid: boolean;
  profile?: string;
  errors?: string[];
  warnings?: string[];
}

/** Client for ZUGFeRD/Factur-X operations. */
export class ZugferdClient {
  constructor(private readonly transport: Transport) {}

  /** Embed ZUGFeRD XML into a PDF. */
  async embed(
    file: FileInput,
    invoiceData: InvoiceData,
  ): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/zugferd/embed/base64", {
      pdfBase64: base64,
      invoice: invoiceData,
    });
  }

  /** Extract ZUGFeRD XML from a PDF. */
  async extract(file: FileInput): Promise<InvoiceData> {
    const base64 = toBase64(file);
    return this.transport.requestJson<InvoiceData>(
      "POST",
      "/api/zugferd/extract/base64",
      { pdfBase64: base64 },
    );
  }

  /** Validate a ZUGFeRD PDF. */
  async validate(file: FileInput): Promise<ZugferdValidationResult> {
    const base64 = toBase64(file);
    return this.transport.requestJson<ZugferdValidationResult>(
      "POST",
      "/api/zugferd/validate/base64",
      { pdfBase64: base64 },
    );
  }
}
