import type { Transport } from "../transport.js";
import type { InvoiceData } from "../models/invoice.js";
import type { ExtractionResult } from "../models/extraction.js";
import type { XRechnungFormat } from "../models/enums.js";

interface XRechnungValidationResult {
  valid: boolean;
  format?: string;
  errors?: string[];
  warnings?: string[];
}

interface XRechnungDetectionResult {
  detected: boolean;
  format?: string;
  version?: string;
}

/** Client for XRechnung operations. */
export class XRechnungClient {
  constructor(private readonly transport: Transport) {}

  /** Generate XRechnung XML from invoice data. */
  async generate(
    invoiceData: InvoiceData,
    format?: XRechnungFormat,
  ): Promise<string> {
    const result = await this.transport.requestJson<{ xml: string }>(
      "POST",
      "/api/xrechnung/generate",
      { invoiceData, format },
    );
    return result.xml;
  }

  /** Parse XRechnung XML into structured invoice data. */
  async parse(xml: string): Promise<InvoiceData> {
    return this.transport.requestJson<InvoiceData>(
      "POST",
      "/api/xrechnung/parse",
      { xml },
    );
  }

  /** Validate XRechnung XML. */
  async validate(xml: string): Promise<XRechnungValidationResult> {
    return this.transport.requestJson<XRechnungValidationResult>(
      "POST",
      "/api/xrechnung/validate",
      { xml },
    );
  }

  /** Transform between XRechnung formats (CII ↔ UBL). */
  async transform(
    xml: string,
    targetFormat: XRechnungFormat,
  ): Promise<string> {
    const result = await this.transport.requestJson<{ xml: string }>(
      "POST",
      "/api/xrechnung/transform",
      { xml, targetFormat },
    );
    return result.xml;
  }

  /** Detect if an XML document is an XRechnung. */
  async detect(xml: string): Promise<XRechnungDetectionResult> {
    return this.transport.requestJson<XRechnungDetectionResult>(
      "POST",
      "/api/xrechnung/detect",
      { xml },
    );
  }

  /** Extract invoice data using AI. */
  async extractAI(xml: string): Promise<ExtractionResult> {
    return this.transport.requestJson<ExtractionResult>(
      "POST",
      "/api/xrechnung/extract-ai",
      { xml },
    );
  }
}
