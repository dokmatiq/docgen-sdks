package com.dokmatiq.docgen.exception;

/** 500 – Internal server error. */
public class ServerException extends ApiException {
    public ServerException(String message, String responseBody) {
        super(500, message, responseBody);
    }
}
