/** Base error for all DocGen SDK errors. */
export class DocGenError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DocGenError";
  }
}

/** API error with HTTP status and response details. */
export class ApiError extends DocGenError {
  readonly statusCode: number;
  readonly responseBody?: string;

  constructor(statusCode: number, message: string, responseBody?: string) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
    this.responseBody = responseBody;
  }
}

/** 400 – Validation error with field-level details. */
export class ValidationError extends ApiError {
  readonly fieldErrors?: Record<string, string>;
  readonly hint?: string;

  constructor(
    message: string,
    responseBody?: string,
    fieldErrors?: Record<string, string>,
    hint?: string,
  ) {
    super(400, message, responseBody);
    this.name = "ValidationError";
    this.fieldErrors = fieldErrors;
    this.hint = hint;
  }
}

/** 401 – Invalid or missing API key. */
export class AuthenticationError extends ApiError {
  constructor(message = "Invalid or missing API key") {
    super(401, message);
    this.name = "AuthenticationError";
  }
}

/** 404 – Requested resource not found. */
export class NotFoundError extends ApiError {
  constructor(message = "Resource not found") {
    super(404, message);
    this.name = "NotFoundError";
  }
}

/** 409 – Resource conflict. */
export class ConflictError extends ApiError {
  constructor(message = "Resource conflict") {
    super(409, message);
    this.name = "ConflictError";
  }
}

/** 429 – Rate limit exceeded. */
export class RateLimitError extends ApiError {
  readonly retryAfter?: number;
  readonly limit?: number;
  readonly remaining?: number;

  constructor(
    message = "Rate limit exceeded",
    retryAfter?: number,
    limit?: number,
    remaining?: number,
  ) {
    super(429, message);
    this.name = "RateLimitError";
    this.retryAfter = retryAfter;
    this.limit = limit;
    this.remaining = remaining;
  }
}

/** 500 – Internal server error. */
export class ServerError extends ApiError {
  constructor(message = "Internal server error", responseBody?: string) {
    super(500, message, responseBody);
    this.name = "ServerError";
  }
}

/** 503 – Service temporarily unavailable. */
export class ServiceUnavailableError extends ApiError {
  constructor(
    message = "Service temporarily unavailable",
    responseBody?: string,
  ) {
    super(503, message, responseBody);
    this.name = "ServiceUnavailableError";
  }
}

/** Request timed out. */
export class TimeoutError extends DocGenError {
  constructor(message = "Request timed out") {
    super(message);
    this.name = "TimeoutError";
  }
}
