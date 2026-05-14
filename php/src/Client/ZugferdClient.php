<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;
use Dokmatiq\DocGen\Model\InvoiceData;

/** Client for ZUGFeRD operations. */
final class ZugferdClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Embed ZUGFeRD XML into a PDF. */
    public function embed(string $pdfPathOrBase64, InvoiceData $invoiceData): string
    {
        return $this->transport->requestBytes('POST', '/api/zugferd/embed/base64', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'invoice' => $invoiceData,
        ]);
    }

    /** Extract ZUGFeRD data from a PDF. */
    public function extract(string $pdfPathOrBase64): array
    {
        return $this->transport->requestJson('POST', '/api/zugferd/extract/base64', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
    }

    /** Validate ZUGFeRD compliance. */
    public function validate(string $pdfPathOrBase64): array
    {
        return $this->transport->requestJson('POST', '/api/zugferd/validate/base64', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
    }
}
