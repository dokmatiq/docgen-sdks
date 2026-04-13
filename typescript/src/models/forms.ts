/** A form field detected in a PDF. */
export interface PdfFormField {
  name: string;
  type: string;
  value?: string;
  options?: string[];
  required?: boolean;
  readOnly?: boolean;
}

/** Request to fill PDF form fields. */
export interface PdfFormFillRequest {
  pdfBase64: string;
  fields: Record<string, string>;
  flatten?: boolean;
}
