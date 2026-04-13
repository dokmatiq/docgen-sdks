package com.dokmatiq.docgen.exception;

/** Base exception for all DocGen SDK errors. */
public class DocGenException extends RuntimeException {
    public DocGenException(String message) {
        super(message);
    }

    public DocGenException(String message, Throwable cause) {
        super(message, cause);
    }
}
