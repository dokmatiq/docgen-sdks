using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for PDF page preview rendering.
/// </summary>
public sealed class PreviewClient
{
    private readonly Transport _transport;

    internal PreviewClient(Transport transport) => _transport = transport;

    /// <summary>Render a single page as a PNG image.</summary>
    public byte[] PreviewPage(string filePath, int page = 1, int dpi = 150)
        => _transport.RequestBytes(HttpMethod.Post, "/api/preview/page",
            new { pdfBase64 = FileUtils.ToBase64(filePath), page, dpi });

    /// <summary>Render a single page from bytes.</summary>
    public byte[] PreviewPage(byte[] data, int page = 1, int dpi = 150)
        => _transport.RequestBytes(HttpMethod.Post, "/api/preview/page",
            new { pdfBase64 = FileUtils.ToBase64(data), page, dpi });

    /// <summary>Render multiple pages.</summary>
    public PreviewResponse PreviewPages(string filePath, List<int>? pages = null, int dpi = 150)
    {
        var body = new Dictionary<string, object> { ["pdfBase64"] = FileUtils.ToBase64(filePath), ["dpi"] = dpi };
        if (pages is not null) body["pages"] = pages;
        return _transport.RequestJson<PreviewResponse>(HttpMethod.Post, "/api/preview/pages", body);
    }

    /// <summary>Get total page count.</summary>
    public int PageCount(string filePath)
    {
        var result = _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post,
            "/api/preview/page-count", new { pdfBase64 = FileUtils.ToBase64(filePath) });
        return result.TryGetValue("pageCount", out var pc) && pc is System.Text.Json.JsonElement el
            ? el.GetInt32() : 0;
    }
}
