<?php

declare(strict_types=1);

namespace Dokmatiq\DocGen\Client;

use Dokmatiq\DocGen\Internal\FileUtils;
use Dokmatiq\DocGen\Internal\Transport;
use Dokmatiq\DocGen\Model\SignatureRequest;
use Dokmatiq\DocGen\Model\VisibleSignatureConfig;

/** Client for PDF digital signature operations. */
final class SignaturesClient
{
    public function __construct(private readonly Transport $transport) {}

    /** Upload a signing certificate (PKCS#12). */
    public function uploadCert(string $filePath, string $password, ?string $alias = null): array
    {
        $fields = ['password' => $password];
        if ($alias !== null) {
            $fields['alias'] = $alias;
        }
        $response = $this->transport->uploadMultipart('POST', '/api/signatures/certificates', $filePath, 'file', $fields);
        return json_decode($response, true) ?: [];
    }

    /** List uploaded certificates. */
    public function listCerts(): array
    {
        return $this->transport->requestJson('GET', '/api/signatures/certificates');
    }

    /** Delete a certificate by alias. */
    public function deleteCert(string $alias): void
    {
        $this->transport->requestJson('DELETE', "/api/signatures/certificates/{$alias}");
    }

    /** Sign a PDF. */
    public function sign(string $pdfPathOrBase64, string $certAlias, ?string $reason = null, ?string $location = null, ?VisibleSignatureConfig $visible = null): string
    {
        $body = [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
            'certificateAlias' => $certAlias,
        ];
        if ($reason !== null) $body['reason'] = $reason;
        if ($location !== null) $body['location'] = $location;
        if ($visible !== null) $body['visibleSignature'] = $visible;

        return $this->transport->requestBytes('POST', '/api/signatures/sign', $body);
    }

    /** Verify signatures on a PDF. */
    public function verify(string $pdfPathOrBase64): array
    {
        return $this->transport->requestJson('POST', '/api/signatures/verify', [
            'pdfBase64' => FileUtils::toBase64($pdfPathOrBase64),
        ]);
    }
}
