import type { Transport } from "../transport.js";
import type {
  SignatureVerifyResult,
  VisibleSignatureConfig,
} from "../models/signature.js";
import { toBase64, toBuffer, detectFilename, type FileInput } from "../files.js";

interface CertificateInfo {
  name: string;
  subject?: string;
  issuer?: string;
  validFrom?: string;
  validTo?: string;
}

/** Client for digital signature operations. */
export class SignaturesClient {
  constructor(private readonly transport: Transport) {}

  /** Upload a PKCS#12 certificate. */
  async uploadCertificate(
    file: FileInput,
    password: string,
    name?: string,
  ): Promise<CertificateInfo> {
    const buffer = toBuffer(file);
    const fileName = name ?? detectFilename(file, "certificate.p12");
    return this.transport.upload<CertificateInfo>(
      "/api/signatures/certificates",
      "file",
      buffer,
      fileName,
      { password },
    );
  }

  /** List uploaded certificates. */
  async listCertificates(): Promise<CertificateInfo[]> {
    return this.transport.requestList<CertificateInfo>(
      "GET",
      "/api/signatures/certificates",
    );
  }

  /** Delete a certificate by name. */
  async deleteCertificate(name: string): Promise<void> {
    return this.transport.delete(
      `/api/signatures/certificates/${encodeURIComponent(name)}`,
    );
  }

  /** Get certificate details. */
  async certificateInfo(name: string): Promise<CertificateInfo> {
    return this.transport.requestJson<CertificateInfo>(
      "GET",
      `/api/signatures/certificates/${encodeURIComponent(name)}`,
    );
  }

  /** Digitally sign a PDF. */
  async sign(
    file: FileInput,
    certificateName: string,
    certificatePassword: string,
    options?: {
      reason?: string;
      location?: string;
      visibleSignature?: VisibleSignatureConfig;
    },
  ): Promise<Buffer> {
    const base64 = toBase64(file);
    return this.transport.requestBytes("POST", "/api/signatures/sign", {
      pdfBase64: base64,
      certificateName,
      certificatePassword,
      ...options,
    });
  }

  /** Verify signatures in a PDF. */
  async verify(file: FileInput): Promise<SignatureVerifyResult> {
    const base64 = toBase64(file);
    return this.transport.requestJson<SignatureVerifyResult>(
      "POST",
      "/api/signatures/verify",
      { pdfBase64: base64 },
    );
  }
}
