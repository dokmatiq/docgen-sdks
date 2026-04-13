<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** QR code data for a document bookmark. */
final class QrCodeData
{
    public function __construct(
        public readonly string $bookmarkName,
        public readonly string $content,
        public readonly ?int $width = null,
        public readonly ?int $height = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
