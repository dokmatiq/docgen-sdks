<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

enum ZugferdProfile: string
{
    case MINIMUM = 'MINIMUM';
    case BASIC_WL = 'BASIC_WL';
    case BASIC = 'BASIC';
    case EN16931 = 'EN16931';
    case EXTENDED = 'EXTENDED';
    case XRECHNUNG = 'XRECHNUNG';
}
