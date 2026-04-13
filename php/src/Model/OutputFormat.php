<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Model;

/** Output document format. */
enum OutputFormat: string
{
    case PDF = 'PDF';
    case DOCX = 'DOCX';
    case ODT = 'ODT';
}
