/** Retry policy configuration. */
export interface RetryPolicy {
  /** Maximum number of retries (default: 3). */
  maxRetries?: number;
  /** Initial delay in milliseconds before the first retry (default: 500). */
  initialDelay?: number;
  /** Backoff multiplier between retries (default: 2.0). */
  backoffMultiplier?: number;
  /** Maximum delay in milliseconds (default: 30000). */
  maxDelay?: number;
}

/** DocGen client configuration. */
export interface DocGenConfig {
  /** API key for authentication (required). */
  apiKey: string;
  /** Base URL of the DocGen API (default: "https://api.dokmatiq.com"). */
  baseUrl?: string;
  /** Request timeout in milliseconds (default: 60000). */
  timeout?: number;
  /** Retry policy for failed requests. */
  retry?: RetryPolicy;
  /** Validation mode: "strict" rejects, "warn" logs, undefined skips. */
  validateMode?: "strict" | "warn";
}

const DEFAULT_BASE_URL = "https://api.dokmatiq.com";
const DEFAULT_TIMEOUT = 60_000;
const DEFAULT_RETRY: Required<RetryPolicy> = {
  maxRetries: 3,
  initialDelay: 500,
  backoffMultiplier: 2.0,
  maxDelay: 30_000,
};

/** Resolve config with defaults applied. */
export function resolveConfig(config: DocGenConfig): {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  retry: Required<RetryPolicy>;
  validateMode?: "strict" | "warn";
} {
  return {
    apiKey: config.apiKey,
    baseUrl: config.baseUrl ?? DEFAULT_BASE_URL,
    timeout: config.timeout ?? DEFAULT_TIMEOUT,
    retry: { ...DEFAULT_RETRY, ...config.retry },
    validateMode: config.validateMode,
  };
}
