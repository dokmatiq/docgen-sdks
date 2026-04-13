import type { RetryPolicy } from "./config.js";
import {
  ApiError,
  AuthenticationError,
  ConflictError,
  NotFoundError,
  RateLimitError,
  ServerError,
  ServiceUnavailableError,
  TimeoutError,
  ValidationError,
} from "./errors.js";

const RETRYABLE_STATUS_CODES = new Set([429, 500, 502, 503, 504]);

interface TransportConfig {
  baseUrl: string;
  apiKey: string;
  timeout: number;
  retry: Required<RetryPolicy>;
  validateMode?: "strict" | "warn";
}

/** HTTP transport layer with retry and error mapping. */
export class Transport {
  private readonly config: TransportConfig;

  constructor(config: TransportConfig) {
    this.config = config;
  }

  /** Make a JSON API request and return parsed response. */
  async requestJson<T>(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<T> {
    const response = await this.request(method, path, {
      headers: { "Content-Type": "application/json" },
      body: body != null ? JSON.stringify(body) : undefined,
    });
    return (await response.json()) as T;
  }

  /** Make an API request and return raw bytes. */
  async requestBytes(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<Buffer> {
    const response = await this.request(method, path, {
      headers: { "Content-Type": "application/json" },
      body: body != null ? JSON.stringify(body) : undefined,
    });
    const arrayBuffer = await response.arrayBuffer();
    return Buffer.from(arrayBuffer);
  }

  /** Upload a file via multipart form data. */
  async upload<T>(
    path: string,
    fieldName: string,
    fileBuffer: Buffer,
    fileName: string,
    extraFields?: Record<string, string>,
  ): Promise<T> {
    const formData = new FormData();
    formData.append(
      fieldName,
      new Blob([new Uint8Array(fileBuffer)]),
      fileName,
    );
    if (extraFields) {
      for (const [key, value] of Object.entries(extraFields)) {
        formData.append(key, value);
      }
    }
    const response = await this.request("POST", path, { body: formData });
    return (await response.json()) as T;
  }

  /** Upload raw bytes and return binary response. */
  async uploadBytes(
    path: string,
    fieldName: string,
    fileBuffer: Buffer,
    fileName: string,
    extraFields?: Record<string, string>,
  ): Promise<Buffer> {
    const formData = new FormData();
    formData.append(
      fieldName,
      new Blob([new Uint8Array(fileBuffer)]),
      fileName,
    );
    if (extraFields) {
      for (const [key, value] of Object.entries(extraFields)) {
        formData.append(key, value);
      }
    }
    const response = await this.request("POST", path, { body: formData });
    const arrayBuffer = await response.arrayBuffer();
    return Buffer.from(arrayBuffer);
  }

  /** Send a DELETE request. */
  async delete(path: string): Promise<void> {
    await this.request("DELETE", path);
  }

  /** Make a JSON request and return an array. */
  async requestList<T>(method: string, path: string): Promise<T[]> {
    const response = await this.request(method, path);
    return (await response.json()) as T[];
  }

  private async request(
    method: string,
    path: string,
    options?: { headers?: Record<string, string>; body?: string | FormData },
  ): Promise<Response> {
    const url = `${this.config.baseUrl}${path}`;
    const headers: Record<string, string> = {
      "X-API-Key": this.config.apiKey,
      ...options?.headers,
    };
    if (this.config.validateMode) {
      headers["X-Validate-Mode"] = this.config.validateMode;
    }

    const { maxRetries, initialDelay, backoffMultiplier, maxDelay } =
      this.config.retry;
    let lastError: Error | undefined;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(
          () => controller.abort(),
          this.config.timeout,
        );

        const response = await fetch(url, {
          method,
          headers,
          body: options?.body,
          signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (response.ok) {
          return response;
        }

        // Check if retryable
        if (
          RETRYABLE_STATUS_CODES.has(response.status) &&
          attempt < maxRetries
        ) {
          let delay = initialDelay * Math.pow(backoffMultiplier, attempt);
          delay = Math.min(delay, maxDelay);

          // Respect Retry-After header on 429
          if (response.status === 429) {
            const retryAfter = response.headers.get("Retry-After");
            if (retryAfter) {
              const retryMs = parseFloat(retryAfter) * 1000;
              if (!isNaN(retryMs)) {
                delay = Math.max(delay, retryMs);
              }
            }
          }

          await sleep(delay);
          continue;
        }

        // Non-retryable or retries exhausted — throw mapped error
        await throwForStatus(response);
      } catch (error: unknown) {
        if (error instanceof ApiError) {
          throw error;
        }
        if (
          error instanceof Error &&
          error.name === "AbortError"
        ) {
          lastError = new TimeoutError(
            `Request timed out after ${this.config.timeout}ms`,
          );
          if (attempt < maxRetries) {
            const delay = Math.min(
              initialDelay * Math.pow(backoffMultiplier, attempt),
              maxDelay,
            );
            await sleep(delay);
            continue;
          }
          throw lastError;
        }
        lastError = error instanceof Error ? error : new Error(String(error));
        if (attempt < maxRetries) {
          const delay = Math.min(
            initialDelay * Math.pow(backoffMultiplier, attempt),
            maxDelay,
          );
          await sleep(delay);
          continue;
        }
      }
    }

    throw lastError ?? new Error("Request failed after all retries");
  }
}

async function throwForStatus(response: Response): Promise<never> {
  const body = await response.text();
  let parsed: Record<string, unknown> | undefined;
  try {
    parsed = JSON.parse(body);
  } catch {
    // not JSON
  }

  const message =
    (parsed?.["message"] as string) ??
    (parsed?.["error"] as string) ??
    `HTTP ${response.status}`;

  switch (response.status) {
    case 400: {
      const fieldErrors = parsed?.["fieldErrors"] as
        | Record<string, string>
        | undefined;
      const hint = parsed?.["hint"] as string | undefined;
      throw new ValidationError(message, body, fieldErrors, hint);
    }
    case 401:
      throw new AuthenticationError(message);
    case 404:
      throw new NotFoundError(message);
    case 409:
      throw new ConflictError(message);
    case 429: {
      const retryAfter = response.headers.get("Retry-After");
      const limit = response.headers.get("X-RateLimit-Limit");
      const remaining = response.headers.get("X-RateLimit-Remaining");
      throw new RateLimitError(
        message,
        retryAfter ? parseFloat(retryAfter) : undefined,
        limit ? parseInt(limit, 10) : undefined,
        remaining ? parseInt(remaining, 10) : undefined,
      );
    }
    case 500:
      throw new ServerError(message, body);
    case 503:
      throw new ServiceUnavailableError(message, body);
    default:
      throw new ApiError(response.status, message, body);
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
