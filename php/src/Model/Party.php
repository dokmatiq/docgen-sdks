<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

use Dokmatiq\DocGen\Internal\Serializer;

/** Invoice party (seller or buyer). */
final class Party
{
    public function __construct(
        public readonly string $name,
        public readonly ?string $street = null,
        public readonly ?string $zip = null,
        public readonly ?string $city = null,
        public readonly string $country = 'DE',
        public readonly ?string $vatId = null,
        public readonly ?string $email = null,
        public readonly ?string $phone = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return Serializer::toArray($this);
    }
}
