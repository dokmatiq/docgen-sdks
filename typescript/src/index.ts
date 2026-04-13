// Client
export { DocGen } from "./client.js";

// Config
export type { DocGenConfig, RetryPolicy } from "./config.js";

// Builders
export { DocumentBuilder } from "./builders/document-builder.js";
export { ComposeBuilder } from "./builders/compose-builder.js";
export { InvoiceBuilder } from "./builders/invoice-builder.js";

// Errors
export {
  DocGenError,
  ApiError,
  ValidationError,
  AuthenticationError,
  NotFoundError,
  ConflictError,
  RateLimitError,
  ServerError,
  ServiceUnavailableError,
  TimeoutError,
} from "./errors.js";

// Enums
export {
  OutputFormat,
  PaperSize,
  PageOrientation,
  TextAlignment,
  BarcodeFormat,
  JobStatus,
  XRechnungFormat,
  ColumnFormat,
  ZugferdProfile,
  InvoiceUnit,
} from "./models/enums.js";

// Models (re-export all types)
export type {
  ImageData,
  QrCodeData,
  BarcodeData,
  ColumnDef,
  TableStyle,
  TableData,
} from "./models/media.js";

export type {
  WatermarkConfig,
  StationeryConfig,
  ContentArea,
} from "./models/content.js";

export type { HeaderFooterConfig, PageSettings } from "./models/page.js";

export type {
  Party,
  InvoiceItem,
  BankAccount,
  InvoiceData,
} from "./models/invoice.js";

export type {
  MarkdownStyles,
  DocumentRequest,
  DocumentPart,
  ComposeRequest,
} from "./models/document.js";

export type {
  VisibleSignatureConfig,
  SignatureRequest,
  SignatureDetail,
  SignatureVerifyResult,
} from "./models/signature.js";

export type { PdfFormField, PdfFormFillRequest } from "./models/forms.js";

export type { PreviewPage, PreviewResponse } from "./models/preview.js";

export type { JobInfo, WebhookPayload } from "./models/jobs.js";

export type { ExtractionResult } from "./models/extraction.js";

// File utilities
export type { FileInput } from "./files.js";

// Webhooks
export { verifyWebhook } from "./webhooks.js";

// Sub-clients (for advanced usage / typing)
export { DocumentsClient } from "./clients/documents.js";
export { TemplatesClient } from "./clients/templates.js";
export { FontsClient } from "./clients/fonts.js";
export { PdfFormsClient } from "./clients/pdf-forms.js";
export { SignaturesClient } from "./clients/signatures.js";
export { PdfToolsClient } from "./clients/pdf-tools.js";
export { PreviewClient } from "./clients/preview.js";
export { ZugferdClient } from "./clients/zugferd.js";
export { XRechnungClient } from "./clients/xrechnung.js";
