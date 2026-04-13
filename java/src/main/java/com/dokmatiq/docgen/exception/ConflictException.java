package com.dokmatiq.docgen.exception;

/** 409 – Resource conflict. */
public class ConflictException extends ApiException {
    public ConflictException(String message) {
        super(409, message, null);
    }
}
