<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Page layout and margin settings. */
final class PageSettings
{
    public function __construct(
        public readonly ?PaperSize $paperSize = null,
        public readonly ?PageOrientation $orientation = null,
        public readonly ?float $marginTop = null,
        public readonly ?float $marginBottom = null,
        public readonly ?float $marginLeft = null,
        public readonly ?float $marginRight = null,
        public readonly ?HeaderFooterConfig $header = null,
        public readonly ?HeaderFooterConfig $footer = null,
        public readonly ?HeaderFooterConfig $firstPageHeader = null,
        public readonly ?HeaderFooterConfig $firstPageFooter = null,
        public readonly ?HeaderFooterConfig $evenPageHeader = null,
        public readonly ?HeaderFooterConfig $evenPageFooter = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
