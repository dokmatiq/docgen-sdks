import type { JobStatus } from "./enums.js";

/** Information about an async generation job. */
export interface JobInfo {
  jobId: string;
  status: JobStatus;
  createdAt?: string;
  completedAt?: string;
  errorMessage?: string;
}

/** Webhook payload sent when an async job completes. */
export interface WebhookPayload {
  jobId: string;
  status: string;
  completedAt?: string;
  errorMessage?: string;
}
