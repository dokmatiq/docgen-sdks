<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Internal;

/** File reading and base64 encoding utilities. */
final class FileUtils
{
    /** Convert file path or raw bytes to base64. */
    public static function toBase64(string $input): string
    {
        if (is_file($input)) {
            return base64_encode(file_get_contents($input));
        }
        // Already base64?
        if (base64_decode($input, true) !== false && base64_encode(base64_decode($input, true)) === $input) {
            return $input;
        }
        // Raw bytes
        return base64_encode($input);
    }

    /** Read file contents from path or return raw bytes as-is. */
    public static function readBytes(string $input): string
    {
        if (is_file($input)) {
            return file_get_contents($input);
        }
        return $input;
    }

    /** Detect filename from a file path, or return a default. */
    public static function detectFilename(string $input, string $default = 'file'): string
    {
        if (is_file($input)) {
            return basename($input);
        }
        return $default;
    }
}
