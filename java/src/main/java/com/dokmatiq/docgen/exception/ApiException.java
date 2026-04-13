package com.dokmatiq.docgen.exception;

/** API error with HTTP status and response details. */
public class ApiException extends DocGenException {
    private final int statusCode;
    private final String responseBody;

    public ApiException(int statusCode, String message, String responseBody) {
        super(message);
        this.statusCode = statusCode;
        this.responseBody = responseBody;
    }

    public int statusCode() { return statusCode; }
    public String responseBody() { return responseBody; }
}
