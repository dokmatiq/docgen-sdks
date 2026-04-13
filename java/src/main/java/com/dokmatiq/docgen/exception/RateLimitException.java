package com.dokmatiq.docgen.exception;

/** 429 – Rate limit exceeded. */
public class RateLimitException extends ApiException {
    private final Double retryAfter;
    private final Integer limit;
    private final Integer remaining;

    public RateLimitException(String message, Double retryAfter, Integer limit, Integer remaining) {
        super(429, message, null);
        this.retryAfter = retryAfter;
        this.limit = limit;
        this.remaining = remaining;
    }

    public Double retryAfter() { return retryAfter; }
    public Integer limit() { return limit; }
    public Integer remaining() { return remaining; }
}
