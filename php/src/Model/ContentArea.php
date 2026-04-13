<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Absolutely positioned content area on the PDF page. */
final class ContentArea
{
    public function __construct(
        public readonly float $x,
        public readonly float $y,
        public readonly float $width,
        public readonly ?string $text = null,
        public readonly ?string $html = null,
        public readonly ?string $imageBase64 = null,
        public readonly ?float $fontSize = null,
        public readonly ?string $fontFamily = null,
        public readonly ?string $color = null,
        public readonly ?TextAlignment $alignment = null,
        public readonly ?string $pages = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
