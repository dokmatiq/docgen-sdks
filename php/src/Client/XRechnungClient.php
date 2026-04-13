<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\Transport;
use Dokmatiq\DocGen\Model\InvoiceData;
use Dokmatiq\DocGen\Model\XRechnungFormat;

/** Client for XRechnung operations. */
final class XRechnungClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Generate XRechnung XML from invoice data. */
    public function generate(InvoiceData $invoiceData, ?XRechnungFormat $format = null): string
    {
        $body = ['invoiceData' => $invoiceData];
        if ($format !== null) $body['format'] = $format;

        $data = $this->transport->requestJson('POST', '/api/xrechnung/generate', $body);
        return $data['xml'] ?? '';
    }

    /** Parse XRechnung XML into structured data. */
    public function parse(string $xml): array
    {
        return $this->transport->requestJson('POST', '/api/xrechnung/parse', ['xml' => $xml]);
    }

    /** Validate XRechnung XML. */
    public function validate(string $xml): array
    {
        return $this->transport->requestJson('POST', '/api/xrechnung/validate', ['xml' => $xml]);
    }

    /** Transform between XRechnung formats (CII ↔ UBL). */
    public function transform(string $xml, XRechnungFormat $targetFormat): string
    {
        $data = $this->transport->requestJson('POST', '/api/xrechnung/transform', [
            'xml' => $xml,
            'targetFormat' => $targetFormat,
        ]);
        return $data['xml'] ?? '';
    }

    /** Detect if XML is XRechnung. */
    public function detect(string $xml): array
    {
        return $this->transport->requestJson('POST', '/api/xrechnung/detect', ['xml' => $xml]);
    }

    /** Extract invoice data using AI. */
    public function extractAI(string $xml): array
    {
        return $this->transport->requestJson('POST', '/api/xrechnung/extract-ai', ['xml' => $xml]);
    }
}
