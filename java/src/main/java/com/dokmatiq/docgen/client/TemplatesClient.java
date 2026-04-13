package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

/** Client for template management endpoints. */
public class TemplatesClient {
    private final Transport transport;

    public TemplatesClient(Transport transport) {
        this.transport = transport;
    }

    /** Upload a template file (ODT/DOCX). */
    public Map<?, ?> upload(Path file) {
        return transport.upload("/api/templates", "file",
                FileUtils.readBytes(file), FileUtils.detectFilename(file), null, Map.class);
    }

    /** Upload a template from bytes. */
    public Map<?, ?> upload(byte[] data, String fileName) {
        return transport.upload("/api/templates", "file", data, fileName, null, Map.class);
    }

    /** List all uploaded templates. */
    public List<Map> list() {
        return transport.requestList("GET", "/api/templates", Map.class);
    }

    /** Delete a template by name. */
    public void delete(String name) {
        transport.delete("/api/templates/" + name);
    }
}
