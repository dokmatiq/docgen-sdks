<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Diagonal watermark overlay configuration. */
final class WatermarkConfig
{
    public function __construct(
        public readonly string $text,
        public readonly ?float $fontSize = null,
        public readonly ?float $opacity = null,
        public readonly ?string $color = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
