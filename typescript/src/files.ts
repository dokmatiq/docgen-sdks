import { readFileSync } from "node:fs";
import { basename } from "node:path";

/** Flexible file input: Buffer, Uint8Array, or file path string. */
export type FileInput = Buffer | Uint8Array | string;

/** Convert a FileInput to a base64-encoded string. */
export function toBase64(input: FileInput): string {
  if (typeof input === "string") {
    return Buffer.from(readFileSync(input)).toString("base64");
  }
  return Buffer.from(input).toString("base64");
}

/** Convert a FileInput to a Buffer. */
export function toBuffer(input: FileInput): Buffer {
  if (typeof input === "string") {
    return Buffer.from(readFileSync(input));
  }
  return Buffer.from(input);
}

/** Detect a filename from the input. */
export function detectFilename(input: FileInput, fallback: string): string {
  if (typeof input === "string") {
    return basename(input);
  }
  return fallback;
}
