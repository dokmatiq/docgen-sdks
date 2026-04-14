using Dokmatiq.DocGen.Internal;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for AI-powered receipt and ticket data extraction.
/// Requires AI processing consent in portal settings (GDPR).
/// </summary>
public sealed class ReceiptsClient
{
    private readonly Transport _transport;

    internal ReceiptsClient(Transport transport) => _transport = transport;

    /// <summary>Extract structured data from a receipt image or PDF.</summary>
    public Dictionary<string, object?> Extract(byte[] fileBytes, string fileName)
        => _transport.Upload<Dictionary<string, object?>>("/api/receipts/extract", "file", fileBytes, fileName);

    /// <summary>Submit receipt for async extraction with optional webhook callback.</summary>
    public Dictionary<string, object?> ExtractAsync(byte[] fileBytes, string fileName,
        string? callbackUrl = null, string? callbackSecret = null)
    {
        var extra = new Dictionary<string, string>();
        if (callbackUrl != null) extra["callbackUrl"] = callbackUrl;
        if (callbackSecret != null) extra["callbackSecret"] = callbackSecret;
        return _transport.Upload<Dictionary<string, object?>>("/api/receipts/extract-async", "file", fileBytes, fileName,
            extra.Count > 0 ? extra : null);
    }

    /// <summary>Extract receipt and generate expense report document.</summary>
    public Dictionary<string, object?> ToDocument(byte[] fileBytes, string fileName,
        string format = "PDF", string title = "Spesenbeleg")
    {
        var extra = new Dictionary<string, string> { ["format"] = format, ["title"] = title };
        return _transport.Upload<Dictionary<string, object?>>("/api/receipts/to-document", "file", fileBytes, fileName, extra);
    }

    /// <summary>Export receipt data as CSV (DATEV-compatible).</summary>
    public byte[] ExportCsv(List<Dictionary<string, object?>> receipts)
        => _transport.RequestBytes(HttpMethod.Post, "/api/receipts/export/csv", receipts);

    /// <summary>Export receipt data as XLSX.</summary>
    public byte[] ExportXlsx(List<Dictionary<string, object?>> receipts)
        => _transport.RequestBytes(HttpMethod.Post, "/api/receipts/export/xlsx", receipts);

    /// <summary>Get async job status.</summary>
    public Dictionary<string, object?> GetJob(string jobId)
        => _transport.RequestJson<Dictionary<string, object?>>(HttpMethod.Get, $"/api/receipts/jobs/{jobId}");

    /// <summary>Get async job extraction result.</summary>
    public Dictionary<string, object?> GetJobResult(string jobId)
        => _transport.RequestJson<Dictionary<string, object?>>(HttpMethod.Get, $"/api/receipts/jobs/{jobId}/result");

    /// <summary>List all async receipt jobs.</summary>
    public List<Dictionary<string, object?>> ListJobs()
        => _transport.RequestList<Dictionary<string, object?>>(HttpMethod.Get, "/api/receipts/jobs");
}
