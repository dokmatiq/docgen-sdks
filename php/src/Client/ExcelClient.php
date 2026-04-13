<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;

/** Client for Excel workbook generation and conversion. */
final class ExcelClient
{
    public function __construct(private readonly Transport $transport) {}

    /**
     * Generate an Excel workbook from a structured JSON definition.
     * Returns raw XLSX bytes.
     */
    public function generate(array $request): string
    {
        return $this->transport->requestBytes('POST', '/api/excel/generate', $request);
    }

    /** Convert CSV content to an Excel workbook. Returns XLSX bytes. */
    public function fromCsv(
        string $csvContent,
        string $delimiter = ',',
        bool $hasHeader = true,
        ?string $sheetName = null,
    ): string {
        $body = [
            'csvContent' => $csvContent,
            'delimiter' => $delimiter,
            'hasHeader' => $hasHeader,
        ];
        if ($sheetName !== null) $body['sheetName'] = $sheetName;

        return $this->transport->requestBytes('POST', '/api/excel/from-csv', $body);
    }

    /** Convert an Excel sheet to CSV text. */
    public function toCsv(string $excelBase64, int $sheetIndex = 0, string $delimiter = ','): string
    {
        return $this->transport->requestBytes('POST', '/api/excel/to-csv', [
            'excelBase64' => $excelBase64,
            'sheetIndex' => $sheetIndex,
            'delimiter' => $delimiter,
        ]);
    }

    /** Convert an Excel sheet to structured JSON. */
    public function toJson(string $excelBase64, int $sheetIndex = 0, bool $hasHeader = true): array
    {
        return $this->transport->requestJson('POST', '/api/excel/to-json', [
            'excelBase64' => $excelBase64,
            'sheetIndex' => $sheetIndex,
            'hasHeader' => $hasHeader,
        ]);
    }

    /**
     * Fill an Excel template with data. Returns XLSX bytes.
     *
     * @param array<string, mixed>|null $values Cell values (key = cell ref or named range)
     * @param array<string, list<list<mixed>>>|null $tables Table data at named ranges
     */
    public function fillTemplate(
        string $templateBase64,
        ?array $values = null,
        ?array $tables = null,
        bool $recalculate = true,
        ?string $password = null,
    ): string {
        $body = [
            'templateBase64' => $templateBase64,
            'recalculate' => $recalculate,
        ];
        if ($values !== null) $body['values'] = $values;
        if ($tables !== null) $body['tables'] = $tables;
        if ($password !== null) $body['password'] = $password;

        return $this->transport->requestBytes('POST', '/api/excel/fill-template', $body);
    }

    /** Inspect an Excel workbook and return metadata. */
    public function inspect(string $excelBase64): array
    {
        return $this->transport->requestJson('POST', '/api/excel/inspect', [
            'excelBase64' => $excelBase64,
        ]);
    }
}
