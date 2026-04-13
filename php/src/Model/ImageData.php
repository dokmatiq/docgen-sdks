<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Embedded image data for a document bookmark. */
final class ImageData
{
    public function __construct(
        public readonly string $bookmarkName,
        public readonly string $base64,
        public readonly ?int $width = null,
        public readonly ?int $height = null,
        public readonly ?string $altText = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
