<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Configuration for a visible signature on a PDF. */
final class VisibleSignatureConfig
{
    public function __construct(
        public readonly int $page = 1,
        public readonly float $x = 10,
        public readonly float $y = 10,
        public readonly float $width = 200,
        public readonly float $height = 50,
        public readonly ?string $label = null,
        public readonly ?string $imageBase64 = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
