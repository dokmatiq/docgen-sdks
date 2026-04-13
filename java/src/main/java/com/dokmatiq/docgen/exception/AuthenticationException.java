package com.dokmatiq.docgen.exception;

/** 401 – Invalid or missing API key. */
public class AuthenticationException extends ApiException {
    public AuthenticationException(String message) {
        super(401, message, null);
    }
}
