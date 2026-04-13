<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

enum PaperSize: string
{
    case A4 = 'A4';
    case A3 = 'A3';
    case A5 = 'A5';
    case LETTER = 'LETTER';
    case LEGAL = 'LEGAL';
}
