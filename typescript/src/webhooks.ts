import { createHmac, timingSafeEqual } from "node:crypto";
import { DocGenError } from "./errors.js";
import type { WebhookPayload } from "./models/jobs.js";

/**
 * Verify a DocGen webhook signature and parse the payload.
 *
 * @param body - Raw request body (string or Buffer).
 * @param signature - Value of the X-DocGen-Signature header.
 * @param secret - The callback_secret used when creating the job.
 * @returns Parsed webhook payload.
 * @throws DocGenError if the signature is invalid.
 */
export function verifyWebhook(
  body: string | Buffer,
  signature: string,
  secret: string,
): WebhookPayload {
  const bodyBuffer = typeof body === "string" ? Buffer.from(body, "utf-8") : body;

  const expected = createHmac("sha256", secret)
    .update(bodyBuffer)
    .digest("hex");

  const sigBuffer = Buffer.from(signature, "utf-8");
  const expectedBuffer = Buffer.from(expected, "utf-8");

  if (
    sigBuffer.length !== expectedBuffer.length ||
    !timingSafeEqual(sigBuffer, expectedBuffer)
  ) {
    throw new DocGenError("Invalid webhook signature");
  }

  return JSON.parse(bodyBuffer.toString("utf-8")) as WebhookPayload;
}
