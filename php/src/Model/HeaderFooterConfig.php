<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

/** Header/footer configuration with left/center/right sections. */
final class HeaderFooterConfig
{
    public function __construct(
        public readonly ?string $left = null,
        public readonly ?string $center = null,
        public readonly ?string $right = null,
        public readonly ?float $fontSize = null,
        public readonly ?string $fontFamily = null,
        public readonly ?string $color = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return array_filter(get_object_vars($this), fn ($v) => $v !== null);
    }
}
