package com.dokmatiq.docgen.internal;

import com.dokmatiq.docgen.DocGenConfig;
import com.dokmatiq.docgen.exception.*;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/** HTTP transport layer with retry and error mapping. */
public class Transport implements AutoCloseable {
    private static final Set<Integer> RETRYABLE = Set.of(429, 500, 502, 503, 504);

    private final DocGenConfig config;
    private final HttpClient httpClient;

    public Transport(DocGenConfig config) {
        this.config = config;
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(config.timeout())
                .build();
    }

    /** Make a JSON request and return parsed response. */
    public <T> T requestJson(String method, String path, Object body, Class<T> responseType) {
        var response = execute(method, path, body != null ? JsonMapper.toJson(body) : null, "application/json");
        return JsonMapper.fromJson(response, responseType);
    }

    /** Make a JSON request and return a list. */
    public <T> java.util.List<T> requestList(String method, String path, Class<T> elementType) {
        var response = execute(method, path, null, null);
        return JsonMapper.fromJsonList(response, elementType);
    }

    /** Make a JSON request and return raw bytes. */
    public byte[] requestBytes(String method, String path, Object body) {
        var jsonBody = body != null ? JsonMapper.toJson(body) : null;
        return executeRawBytes(method, path,
                jsonBody != null ? jsonBody.getBytes(java.nio.charset.StandardCharsets.UTF_8) : null,
                "application/json");
    }

    /** Upload a file via multipart. */
    public <T> T upload(String path, String fieldName, byte[] fileBytes,
                        String fileName, Map<String, String> extraFields, Class<T> responseType) {
        String boundary = "----DocGenBoundary" + UUID.randomUUID().toString().replace("-", "");
        var sb = new StringBuilder();

        sb.append("--").append(boundary).append("\r\n");
        sb.append("Content-Disposition: form-data; name=\"").append(fieldName)
                .append("\"; filename=\"").append(fileName).append("\"\r\n");
        sb.append("Content-Type: application/octet-stream\r\n\r\n");

        var prefix = sb.toString().getBytes(StandardCharsets.UTF_8);
        var suffix = new StringBuilder();

        if (extraFields != null) {
            for (var entry : extraFields.entrySet()) {
                suffix.append("\r\n--").append(boundary).append("\r\n");
                suffix.append("Content-Disposition: form-data; name=\"")
                        .append(entry.getKey()).append("\"\r\n\r\n");
                suffix.append(entry.getValue());
            }
        }
        suffix.append("\r\n--").append(boundary).append("--\r\n");
        var suffixBytes = suffix.toString().getBytes(StandardCharsets.UTF_8);

        var fullBody = new byte[prefix.length + fileBytes.length + suffixBytes.length];
        System.arraycopy(prefix, 0, fullBody, 0, prefix.length);
        System.arraycopy(fileBytes, 0, fullBody, prefix.length, fileBytes.length);
        System.arraycopy(suffixBytes, 0, fullBody, prefix.length + fileBytes.length, suffixBytes.length);

        var response = executeRaw("POST", path, fullBody, "multipart/form-data; boundary=" + boundary);
        return JsonMapper.fromJson(response, responseType);
    }

    /** Upload bytes and return binary response. */
    public byte[] uploadBytes(String path, String fieldName, byte[] fileBytes,
                              String fileName, Map<String, String> extraFields) {
        String boundary = "----DocGenBoundary" + UUID.randomUUID().toString().replace("-", "");
        var sb = new StringBuilder();

        sb.append("--").append(boundary).append("\r\n");
        sb.append("Content-Disposition: form-data; name=\"").append(fieldName)
                .append("\"; filename=\"").append(fileName).append("\"\r\n");
        sb.append("Content-Type: application/octet-stream\r\n\r\n");

        var prefix = sb.toString().getBytes(StandardCharsets.UTF_8);
        var suffix = new StringBuilder();

        if (extraFields != null) {
            for (var entry : extraFields.entrySet()) {
                suffix.append("\r\n--").append(boundary).append("\r\n");
                suffix.append("Content-Disposition: form-data; name=\"")
                        .append(entry.getKey()).append("\"\r\n\r\n");
                suffix.append(entry.getValue());
            }
        }
        suffix.append("\r\n--").append(boundary).append("--\r\n");
        var suffixBytes = suffix.toString().getBytes(StandardCharsets.UTF_8);

        var fullBody = new byte[prefix.length + fileBytes.length + suffixBytes.length];
        System.arraycopy(prefix, 0, fullBody, 0, prefix.length);
        System.arraycopy(fileBytes, 0, fullBody, prefix.length, fileBytes.length);
        System.arraycopy(suffixBytes, 0, fullBody, prefix.length + fileBytes.length, suffixBytes.length);

        return executeRawBytes("POST", path, fullBody, "multipart/form-data; boundary=" + boundary);
    }

    /** Send a DELETE request. */
    public void delete(String path) {
        execute("DELETE", path, null, null);
    }

    private String execute(String method, String path, String jsonBody, String contentType) {
        return new String(executeRawBytes(method, path,
                jsonBody != null ? jsonBody.getBytes(StandardCharsets.UTF_8) : null,
                contentType), StandardCharsets.UTF_8);
    }

    private String executeRaw(String method, String path, byte[] body, String contentType) {
        return new String(executeRawBytes(method, path, body, contentType), StandardCharsets.UTF_8);
    }

    private byte[] executeRawBytes(String method, String path, byte[] body, String contentType) {
        var retry = config.retry();
        Exception lastError = null;

        for (int attempt = 0; attempt <= retry.maxRetries(); attempt++) {
            try {
                var reqBuilder = HttpRequest.newBuilder()
                        .uri(URI.create(config.baseUrl() + path))
                        .timeout(config.timeout())
                        .header("X-API-Key", config.apiKey());

                if (config.validateMode() != null) {
                    reqBuilder.header("X-Validate-Mode", config.validateMode());
                }
                if (contentType != null) {
                    reqBuilder.header("Content-Type", contentType);
                }

                if (body != null) {
                    reqBuilder.method(method, HttpRequest.BodyPublishers.ofByteArray(body));
                } else {
                    reqBuilder.method(method, HttpRequest.BodyPublishers.noBody());
                }

                var response = httpClient.send(reqBuilder.build(),
                        HttpResponse.BodyHandlers.ofByteArray());

                int status = response.statusCode();

                if (status >= 200 && status < 300) {
                    return response.body();
                }

                if (RETRYABLE.contains(status) && attempt < retry.maxRetries()) {
                    long delay = (long) (retry.initialDelay().toMillis()
                            * Math.pow(retry.backoffMultiplier(), attempt));
                    delay = Math.min(delay, retry.maxDelay().toMillis());

                    if (status == 429) {
                        var retryAfter = response.headers().firstValue("Retry-After");
                        if (retryAfter.isPresent()) {
                            try {
                                delay = Math.max(delay, (long) (Double.parseDouble(retryAfter.get()) * 1000));
                            } catch (NumberFormatException ignored) {}
                        }
                    }

                    Thread.sleep(delay);
                    continue;
                }

                throwForStatus(status, response);
            } catch (ApiException e) {
                throw e;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new DocGenException("Request interrupted", e);
            } catch (IOException e) {
                lastError = e;
                if (attempt < retry.maxRetries()) {
                    try {
                        long delay = (long) (retry.initialDelay().toMillis()
                                * Math.pow(retry.backoffMultiplier(), attempt));
                        delay = Math.min(delay, retry.maxDelay().toMillis());
                        Thread.sleep(delay);
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        throw new DocGenException("Request interrupted", ie);
                    }
                    continue;
                }
            }
        }

        throw new DocGenException("Request failed after all retries",
                lastError != null ? lastError : new RuntimeException("Unknown error"));
    }

    private void throwForStatus(int status, HttpResponse<byte[]> response) {
        String body = new String(response.body(), StandardCharsets.UTF_8);
        var parsed = JsonMapper.toMap(body);
        String message = parsed.containsKey("message")
                ? String.valueOf(parsed.get("message"))
                : parsed.containsKey("error")
                ? String.valueOf(parsed.get("error"))
                : "HTTP " + status;

        switch (status) {
            case 400 -> {
                @SuppressWarnings("unchecked")
                var fieldErrors = parsed.containsKey("fieldErrors")
                        ? (Map<String, String>) parsed.get("fieldErrors") : null;
                var hint = parsed.containsKey("hint") ? String.valueOf(parsed.get("hint")) : null;
                throw new ValidationException(message, body, fieldErrors, hint);
            }
            case 401 -> throw new AuthenticationException(message);
            case 404 -> throw new NotFoundException(message);
            case 409 -> throw new ConflictException(message);
            case 429 -> {
                var retryAfter = response.headers().firstValue("Retry-After")
                        .map(Double::parseDouble).orElse(null);
                var limit = response.headers().firstValue("X-RateLimit-Limit")
                        .map(Integer::parseInt).orElse(null);
                var remaining = response.headers().firstValue("X-RateLimit-Remaining")
                        .map(Integer::parseInt).orElse(null);
                throw new RateLimitException(message, retryAfter, limit, remaining);
            }
            case 500 -> throw new ServerException(message, body);
            case 503 -> throw new ServiceUnavailableException(message, body);
            default -> throw new ApiException(status, message, body);
        }
    }

    @Override
    public void close() {
        // HttpClient doesn't require explicit close in Java 17
    }
}
