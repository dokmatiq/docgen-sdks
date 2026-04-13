import type { Transport } from "../transport.js";
import { toBuffer, detectFilename, type FileInput } from "../files.js";

interface TemplateInfo {
  name: string;
  size?: number;
  uploadedAt?: string;
}

/** Client for template management endpoints. */
export class TemplatesClient {
  constructor(private readonly transport: Transport) {}

  /** Upload a template file (ODT/DOCX). */
  async upload(file: FileInput, name?: string): Promise<TemplateInfo> {
    const buffer = toBuffer(file);
    const fileName = name ?? detectFilename(file, "template.odt");
    return this.transport.upload<TemplateInfo>(
      "/api/templates",
      "file",
      buffer,
      fileName,
    );
  }

  /** List all uploaded templates. */
  async list(): Promise<TemplateInfo[]> {
    return this.transport.requestList<TemplateInfo>("GET", "/api/templates");
  }

  /** Delete a template by name. */
  async delete(name: string): Promise<void> {
    return this.transport.delete(`/api/templates/${encodeURIComponent(name)}`);
  }
}
