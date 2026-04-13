import type { Transport } from "../transport.js";
import { toBuffer, detectFilename, type FileInput } from "../files.js";

interface FontInfo {
  name: string;
  family?: string;
  size?: number;
  uploadedAt?: string;
}

/** Client for font management endpoints. */
export class FontsClient {
  constructor(private readonly transport: Transport) {}

  /** Upload a font file (TTF/OTF). */
  async upload(file: FileInput, name?: string): Promise<FontInfo> {
    const buffer = toBuffer(file);
    const fileName = name ?? detectFilename(file, "font.ttf");
    return this.transport.upload<FontInfo>(
      "/api/fonts",
      "file",
      buffer,
      fileName,
    );
  }

  /** List all uploaded fonts. */
  async list(): Promise<FontInfo[]> {
    return this.transport.requestList<FontInfo>("GET", "/api/fonts");
  }

  /** Delete a font by name. */
  async delete(name: string): Promise<void> {
    return this.transport.delete(`/api/fonts/${encodeURIComponent(name)}`);
  }
}
