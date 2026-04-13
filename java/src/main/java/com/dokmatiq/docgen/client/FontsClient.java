package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.internal.FileUtils;
import com.dokmatiq.docgen.internal.Transport;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

/** Client for font management endpoints. */
public class FontsClient {
    private final Transport transport;

    public FontsClient(Transport transport) {
        this.transport = transport;
    }

    /** Upload a font file (TTF/OTF). */
    public Map<?, ?> upload(Path file) {
        return transport.upload("/api/fonts", "file",
                FileUtils.readBytes(file), FileUtils.detectFilename(file), null, Map.class);
    }

    /** Upload a font from bytes. */
    public Map<?, ?> upload(byte[] data, String fileName) {
        return transport.upload("/api/fonts", "file", data, fileName, null, Map.class);
    }

    /** List all uploaded fonts. */
    public List<Map> list() {
        return transport.requestList("GET", "/api/fonts", Map.class);
    }

    /** Delete a font by name. */
    public void delete(String name) {
        transport.delete("/api/fonts/" + name);
    }
}
