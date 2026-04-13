<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

enum BarcodeFormat: string
{
    case CODE_128 = 'CODE_128';
    case CODE_39 = 'CODE_39';
    case EAN_13 = 'EAN_13';
    case EAN_8 = 'EAN_8';
    case UPC_A = 'UPC_A';
    case QR_CODE = 'QR_CODE';
    case DATA_MATRIX = 'DATA_MATRIX';
    case PDF_417 = 'PDF_417';
}
