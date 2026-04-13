package com.dokmatiq.docgen.internal;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;

/** File handling utilities. */
public final class FileUtils {
    private FileUtils() {}

    /** Convert a file path or byte array to base64. */
    public static String toBase64(byte[] data) {
        return Base64.getEncoder().encodeToString(data);
    }

    /** Read a file and encode as base64. */
    public static String toBase64(Path path) {
        try {
            return Base64.getEncoder().encodeToString(Files.readAllBytes(path));
        } catch (IOException e) {
            throw new RuntimeException("Failed to read file: " + path, e);
        }
    }

    /** Read a file into a byte array. */
    public static byte[] readBytes(Path path) {
        try {
            return Files.readAllBytes(path);
        } catch (IOException e) {
            throw new RuntimeException("Failed to read file: " + path, e);
        }
    }

    /** Detect filename from a path. */
    public static String detectFilename(Path path) {
        return path.getFileName().toString();
    }
}
