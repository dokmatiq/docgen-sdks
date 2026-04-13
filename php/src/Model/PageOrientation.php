<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

enum PageOrientation: string
{
    case PORTRAIT = 'PORTRAIT';
    case LANDSCAPE = 'LANDSCAPE';
}
