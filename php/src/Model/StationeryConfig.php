<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Stationery (letterhead) PDF background configuration. */
final class StationeryConfig
{
    public function __construct(
        public readonly string $pdfBase64,
        public readonly ?string $firstPagePdfBase64 = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
