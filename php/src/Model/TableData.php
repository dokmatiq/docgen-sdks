<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Table data with columns, rows, and optional styling. */
final class TableData
{
    /**
     * @param ColumnDef[] $columns
     * @param string[][] $rows
     */
    public function __construct(
        public readonly array $columns,
        public readonly array $rows,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'columns' => array_map(fn (ColumnDef $c) => $c->toArray(), $this->columns),
            'rows' => $this->rows,
        ];
    }
}
