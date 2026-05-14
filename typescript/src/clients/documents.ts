import type { Transport } from "../transport.js";
import type {
  ComposeRequest,
  DocumentRequest,
} from "../models/document.js";
import type { JobInfo } from "../models/jobs.js";
import { TimeoutError } from "../errors.js";

/** Client for document generation endpoints. */
export class DocumentsClient {
  constructor(private readonly transport: Transport) {}

  /** Generate a document synchronously. */
  async generate(request: DocumentRequest): Promise<Buffer> {
    return this.transport.requestBytes("POST", "/api/documents/generate", request);
  }

  /** Compose a multi-part document. */
  async compose(request: ComposeRequest): Promise<Buffer> {
    return this.transport.requestBytes("POST", "/api/documents/compose", request);
  }

  /** Submit an async generation job. */
  async generateAsync(request: DocumentRequest): Promise<JobInfo> {
    return this.transport.requestJson<JobInfo>(
      "POST",
      "/api/documents/generate-async",
      request,
    );
  }

  /** Get status of an async job. */
  async getJob(jobId: string): Promise<JobInfo> {
    return this.transport.requestJson<JobInfo>("GET", `/api/documents/jobs/${jobId}`);
  }

  /** Download the result of a completed async job. */
  async downloadJob(jobId: string): Promise<Buffer> {
    return this.transport.requestBytes("GET", `/api/documents/jobs/${jobId}/download`);
  }

  /** List recent async jobs. */
  async listJobs(): Promise<JobInfo[]> {
    return this.transport.requestList<JobInfo>("GET", "/api/documents/jobs");
  }

  /**
   * Poll an async job until completion.
   * @param jobId - Job ID to poll.
   * @param pollInterval - Interval in ms between polls (default: 2000).
   * @param timeout - Maximum wait time in ms (default: 120000).
   */
  async waitForJob(
    jobId: string,
    pollInterval = 2000,
    timeout = 120_000,
  ): Promise<Buffer> {
    const deadline = Date.now() + timeout;

    while (Date.now() < deadline) {
      const job = await this.getJob(jobId);

      if (job.status === "COMPLETED") {
        return this.downloadJob(jobId);
      }

      if (job.status === "FAILED") {
        throw new Error(
          `Job ${jobId} failed: ${job.errorMessage ?? "unknown error"}`,
        );
      }

      const remaining = deadline - Date.now();
      if (remaining <= 0) break;
      await new Promise((r) => setTimeout(r, Math.min(pollInterval, remaining)));
    }

    throw new TimeoutError(`Job ${jobId} did not complete within ${timeout}ms`);
  }
}
