<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** A single part in a multi-part composed document. */
final class DocumentPart
{
    /**
     * @param array<string, string>|null $fields
     */
    public function __construct(
        public readonly ?string $htmlContent = null,
        public readonly ?string $markdownContent = null,
        public readonly ?string $templateName = null,
        public readonly ?array $fields = null,
        public readonly ?PageSettings $pageSettings = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
