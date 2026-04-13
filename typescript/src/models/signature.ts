/** Visible signature placement configuration. */
export interface VisibleSignatureConfig {
  page?: number;
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  text?: string;
  fontSize?: number;
  imageBase64?: string;
  contact?: string;
}

/** Request to digitally sign a PDF. */
export interface SignatureRequest {
  pdfBase64: string;
  certificateName: string;
  certificatePassword: string;
  reason?: string;
  location?: string;
  visibleSignature?: VisibleSignatureConfig;
}

/** Details of a single signature in a signed PDF. */
export interface SignatureDetail {
  signer?: string;
  signingTime?: string;
  valid: boolean;
  reason?: string;
  location?: string;
}

/** Result of PDF signature verification. */
export interface SignatureVerifyResult {
  signed: boolean;
  signatureCount: number;
  allValid: boolean;
  signatures?: SignatureDetail[];
}
