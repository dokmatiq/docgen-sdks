<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

/** Invoice unit codes (UN/ECE Recommendation 20). */
enum InvoiceUnit: string
{
    case PIECE = 'C62';
    case HOUR = 'HUR';
    case DAY = 'DAY';
    case KILOGRAM = 'KGM';
    case METER = 'MTR';
    case LITER = 'LTR';
    case SQUARE_METER = 'MTK';
    case CUBIC_METER = 'MTQ';
    case SET = 'SET';
    case PACKAGE = 'PK';
}
