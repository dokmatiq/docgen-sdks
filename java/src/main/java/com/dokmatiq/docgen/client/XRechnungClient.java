package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.ExtractionResult;
import com.dokmatiq.docgen.model.InvoiceData;
import com.dokmatiq.docgen.model.XRechnungFormat;

import java.util.HashMap;
import java.util.Map;

/** Client for XRechnung operations. */
public class XRechnungClient {
    private final Transport transport;

    public XRechnungClient(Transport transport) {
        this.transport = transport;
    }

    /** Generate XRechnung XML from invoice data. */
    public String generate(InvoiceData invoiceData, XRechnungFormat format) {
        var body = new HashMap<String, Object>();
        body.put("invoiceData", invoiceData);
        if (format != null) body.put("format", format);
        var result = transport.requestJson("POST", "/api/xrechnung/generate", body, Map.class);
        return String.valueOf(result.get("xml"));
    }

    /** Generate XRechnung XML (default format). */
    public String generate(InvoiceData invoiceData) {
        return generate(invoiceData, null);
    }

    /** Parse XRechnung XML into structured data. */
    public InvoiceData parse(String xml) {
        return transport.requestJson("POST", "/api/xrechnung/parse",
                Map.of("xml", xml), InvoiceData.class);
    }

    /** Validate XRechnung XML. */
    public Map<?, ?> validate(String xml) {
        return transport.requestJson("POST", "/api/xrechnung/validate",
                Map.of("xml", xml), Map.class);
    }

    /** Transform between XRechnung formats. */
    public String transform(String xml, XRechnungFormat targetFormat) {
        var result = transport.requestJson("POST", "/api/xrechnung/transform",
                Map.of("xml", xml, "targetFormat", targetFormat), Map.class);
        return String.valueOf(result.get("xml"));
    }

    /** Detect if XML is XRechnung. */
    public Map<?, ?> detect(String xml) {
        return transport.requestJson("POST", "/api/xrechnung/detect",
                Map.of("xml", xml), Map.class);
    }

    /** Extract invoice data using AI. */
    public ExtractionResult extractAI(String xml) {
        return transport.requestJson("POST", "/api/xrechnung/extract-ai",
                Map.of("xml", xml), ExtractionResult.class);
    }
}
