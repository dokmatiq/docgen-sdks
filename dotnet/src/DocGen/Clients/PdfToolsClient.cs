using Dokmatiq.DocGen.Internal;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for PDF manipulation tools.
/// </summary>
public sealed class PdfToolsClient
{
    private readonly Transport _transport;

    internal PdfToolsClient(Transport transport) => _transport = transport;

    /// <summary>Merge multiple PDF files into one.</summary>
    public byte[] Merge(IEnumerable<string> filePaths)
    {
        var pdfs = filePaths.Select(FileUtils.ToBase64).ToList();
        return _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/merge", new { pdfs });
    }

    /// <summary>Merge PDFs from byte arrays.</summary>
    public byte[] Merge(params byte[][] pdfs)
    {
        var encoded = pdfs.Select(FileUtils.ToBase64).ToList();
        return _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/merge", new { pdfs = encoded });
    }

    /// <summary>Split a PDF by page ranges.</summary>
    public byte[] Split(string filePath, string pages)
        => _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/split",
            new { pdfBase64 = FileUtils.ToBase64(filePath), pages });

    /// <summary>Extract text from a PDF.</summary>
    public string ExtractText(string filePath)
    {
        var result = _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post,
            "/api/pdf-tools/extract-text", new { pdfBase64 = FileUtils.ToBase64(filePath) });
        return result.TryGetValue("text", out var text) ? text?.ToString() ?? "" : "";
    }

    /// <summary>Extract text from bytes.</summary>
    public string ExtractText(byte[] data)
    {
        var result = _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post,
            "/api/pdf-tools/extract-text", new { pdfBase64 = FileUtils.ToBase64(data) });
        return result.TryGetValue("text", out var text) ? text?.ToString() ?? "" : "";
    }

    /// <summary>Get PDF metadata.</summary>
    public Dictionary<string, object> GetMetadata(string filePath)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post,
            "/api/pdf-tools/metadata", new { pdfBase64 = FileUtils.ToBase64(filePath) });

    /// <summary>Set PDF metadata.</summary>
    public byte[] SetMetadata(string filePath, Dictionary<string, string> metadata)
    {
        var body = new Dictionary<string, object> { ["pdfBase64"] = FileUtils.ToBase64(filePath) };
        foreach (var (key, value) in metadata) body[key] = value;
        return _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/metadata/set", body);
    }

    /// <summary>Convert to PDF/A.</summary>
    public byte[] ToPdfA(string filePath)
        => _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/pdfa",
            new { pdfBase64 = FileUtils.ToBase64(filePath) });

    /// <summary>Convert bytes to PDF/A.</summary>
    public byte[] ToPdfA(byte[] data)
        => _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/pdfa",
            new { pdfBase64 = FileUtils.ToBase64(data) });

    /// <summary>Rotate pages in a PDF.</summary>
    public byte[] Rotate(string filePath, int angle, string? pages = null)
    {
        var body = new Dictionary<string, object>
        {
            ["pdfBase64"] = FileUtils.ToBase64(filePath),
            ["angle"] = angle
        };
        if (pages is not null) body["pages"] = pages;
        return _transport.RequestBytes(HttpMethod.Post, "/api/pdf-tools/rotate", body);
    }
}
