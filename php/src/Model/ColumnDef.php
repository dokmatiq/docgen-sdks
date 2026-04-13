<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Column definition for table data. */
final class ColumnDef
{
    public function __construct(
        public readonly string $header,
        public readonly ?int $width = null,
        public readonly ?TextAlignment $alignment = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
