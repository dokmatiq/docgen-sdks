package com.dokmatiq.docgen.exception;

import java.util.Map;

/** 400 – Validation error with field-level details. */
public class ValidationException extends ApiException {
    private final Map<String, String> fieldErrors;
    private final String hint;

    public ValidationException(String message, String responseBody,
                               Map<String, String> fieldErrors, String hint) {
        super(400, message, responseBody);
        this.fieldErrors = fieldErrors;
        this.hint = hint;
    }

    public Map<String, String> fieldErrors() { return fieldErrors; }
    public String hint() { return hint; }
}
