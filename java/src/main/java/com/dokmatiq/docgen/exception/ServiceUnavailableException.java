package com.dokmatiq.docgen.exception;

/** 503 – Service temporarily unavailable. */
public class ServiceUnavailableException extends ApiException {
    public ServiceUnavailableException(String message, String responseBody) {
        super(503, message, responseBody);
    }
}
