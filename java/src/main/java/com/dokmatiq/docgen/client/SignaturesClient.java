package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.SignatureVerifyResult;
import com.dokmatiq.docgen.model.VisibleSignatureConfig;

import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Client for digital signature operations. */
public class SignaturesClient {
    private final Transport transport;

    public SignaturesClient(Transport transport) {
        this.transport = transport;
    }

    /** Upload a PKCS#12 certificate. */
    public Map<?, ?> uploadCertificate(Path file, String password) {
        return transport.upload("/api/signatures/certificates", "file",
                FileUtils.readBytes(file), FileUtils.detectFilename(file),
                Map.of("password", password), Map.class);
    }

    /** List uploaded certificates. */
    public List<Map> listCertificates() {
        return transport.requestList("GET", "/api/signatures/certificates", Map.class);
    }

    /** Delete a certificate by name. */
    public void deleteCertificate(String name) {
        transport.delete("/api/signatures/certificates/" + name);
    }

    /** Get certificate details. */
    public Map<?, ?> certificateInfo(String name) {
        return transport.requestJson("GET", "/api/signatures/certificates/" + name, null, Map.class);
    }

    /** Digitally sign a PDF. */
    public byte[] sign(Path file, String certificateName, String certificatePassword) {
        return sign(file, certificateName, certificatePassword, null, null, null);
    }

    /** Digitally sign a PDF with options. */
    public byte[] sign(Path file, String certificateName, String certificatePassword,
                       String reason, String location, VisibleSignatureConfig visibleSignature) {
        var body = new HashMap<String, Object>();
        body.put("pdfBase64", FileUtils.toBase64(file));
        body.put("certificateName", certificateName);
        body.put("certificatePassword", certificatePassword);
        if (reason != null) body.put("reason", reason);
        if (location != null) body.put("location", location);
        if (visibleSignature != null) body.put("visibleSignature", visibleSignature);
        return transport.requestBytes("POST", "/api/signatures/sign", body);
    }

    /** Sign a PDF from bytes. */
    public byte[] sign(byte[] data, String certificateName, String certificatePassword) {
        return transport.requestBytes("POST", "/api/signatures/sign",
                Map.of("pdfBase64", FileUtils.toBase64(data),
                        "certificateName", certificateName,
                        "certificatePassword", certificatePassword));
    }

    /** Verify signatures in a PDF. */
    public SignatureVerifyResult verify(Path file) {
        return transport.requestJson("POST", "/api/signatures/verify",
                Map.of("pdfBase64", FileUtils.toBase64(file)), SignatureVerifyResult.class);
    }

    /** Verify signatures from bytes. */
    public SignatureVerifyResult verify(byte[] data) {
        return transport.requestJson("POST", "/api/signatures/verify",
                Map.of("pdfBase64", FileUtils.toBase64(data)), SignatureVerifyResult.class);
    }
}
