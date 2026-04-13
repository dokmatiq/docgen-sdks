package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.InvoiceData;

import java.nio.file.Path;
import java.util.Map;

/** Client for ZUGFeRD/Factur-X operations. */
public class ZugferdClient {
    private final Transport transport;

    public ZugferdClient(Transport transport) {
        this.transport = transport;
    }

    /** Embed ZUGFeRD XML into a PDF. */
    public byte[] embed(Path file, InvoiceData invoiceData) {
        return transport.requestBytes("POST", "/api/zugferd/embed",
                Map.of("pdfBase64", FileUtils.toBase64(file), "invoiceData", invoiceData));
    }

    /** Embed ZUGFeRD XML from bytes. */
    public byte[] embed(byte[] data, InvoiceData invoiceData) {
        return transport.requestBytes("POST", "/api/zugferd/embed",
                Map.of("pdfBase64", FileUtils.toBase64(data), "invoiceData", invoiceData));
    }

    /** Extract ZUGFeRD XML from a PDF. */
    public InvoiceData extract(Path file) {
        return transport.requestJson("POST", "/api/zugferd/extract",
                Map.of("pdfBase64", FileUtils.toBase64(file)), InvoiceData.class);
    }

    /** Validate a ZUGFeRD PDF. */
    public Map<?, ?> validate(Path file) {
        return transport.requestJson("POST", "/api/zugferd/validate",
                Map.of("pdfBase64", FileUtils.toBase64(file)), Map.class);
    }
}
