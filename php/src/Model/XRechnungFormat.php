<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

enum XRechnungFormat: string
{
    case CII = 'CII';
    case UBL = 'UBL';
}
