<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Internal;

use BackedEnum;

/** Recursive serialization of model objects to API-compatible arrays. */
final class Serializer
{
    /**
     * Convert an object to a JSON-serializable array, omitting null values.
     *
     * @return array<string, mixed>
     */
    public static function toArray(object $obj): array
    {
        $result = [];
        foreach (get_object_vars($obj) as $key => $value) {
            if ($value === null) {
                continue;
            }
            $result[$key] = self::serializeValue($value);
        }
        return $result;
    }

    private static function serializeValue(mixed $value): mixed
    {
        if ($value instanceof BackedEnum) {
            return $value->value;
        }
        if (is_object($value) && method_exists($value, 'toArray')) {
            return $value->toArray();
        }
        if (is_object($value)) {
            return self::toArray($value);
        }
        if (is_array($value)) {
            return array_map(fn ($v) => self::serializeValue($v), $value);
        }
        return $value;
    }

    /**
     * Convert a JSON string to an associative array.
     *
     * @return array<string, mixed>
     */
    public static function fromJson(string $json): array
    {
        $data = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
        return is_array($data) ? $data : [];
    }

    /** Convert an array to a JSON string, omitting null values. */
    public static function toJson(mixed $data): string
    {
        if (is_object($data)) {
            $data = self::toArray($data);
        }
        return json_encode($data, JSON_THROW_ON_ERROR | JSON_UNESCAPED_UNICODE);
    }
}
