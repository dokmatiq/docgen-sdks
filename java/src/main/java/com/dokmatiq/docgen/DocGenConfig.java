package com.dokmatiq.docgen;

import java.time.Duration;
import java.util.Objects;

/** DocGen client configuration. */
public final class DocGenConfig {
    private final String apiKey;
    private final String baseUrl;
    private final Duration timeout;
    private final RetryPolicy retry;
    private final String validateMode;

    private DocGenConfig(Builder builder) {
        this.apiKey = Objects.requireNonNull(builder.apiKey, "apiKey is required");
        this.baseUrl = builder.baseUrl != null ? builder.baseUrl : "https://api.dokmatiq.com";
        this.timeout = builder.timeout != null ? builder.timeout : Duration.ofSeconds(60);
        this.retry = builder.retry != null ? builder.retry : RetryPolicy.defaultPolicy();
        this.validateMode = builder.validateMode;
    }

    public static Builder builder(String apiKey) { return new Builder(apiKey); }

    public String apiKey() { return apiKey; }
    public String baseUrl() { return baseUrl; }
    public Duration timeout() { return timeout; }
    public RetryPolicy retry() { return retry; }
    public String validateMode() { return validateMode; }

    /** Retry policy configuration. */
    public record RetryPolicy(
            int maxRetries,
            Duration initialDelay,
            double backoffMultiplier,
            Duration maxDelay
    ) {
        public static RetryPolicy defaultPolicy() {
            return new RetryPolicy(3, Duration.ofMillis(500), 2.0, Duration.ofSeconds(30));
        }
    }

    public static class Builder {
        private final String apiKey;
        private String baseUrl;
        private Duration timeout;
        private RetryPolicy retry;
        private String validateMode;

        Builder(String apiKey) { this.apiKey = apiKey; }

        public Builder baseUrl(String baseUrl) { this.baseUrl = baseUrl; return this; }
        public Builder timeout(Duration timeout) { this.timeout = timeout; return this; }
        public Builder retry(RetryPolicy retry) { this.retry = retry; return this; }
        public Builder validateMode(String mode) { this.validateMode = mode; return this; }

        public DocGenConfig build() { return new DocGenConfig(this); }
    }
}
