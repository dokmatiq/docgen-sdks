package com.dokmatiq.docgen.exception;

/** 404 – Resource not found. */
public class NotFoundException extends ApiException {
    public NotFoundException(String message) {
        super(404, message, null);
    }
}
