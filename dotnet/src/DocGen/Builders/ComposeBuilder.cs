using Dokmatiq.DocGen.Clients;
using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Builders;

/// <summary>
/// Fluent builder for multi-part document composition.
/// <code>
/// byte[] pdf = dg.Compose()
///     .Part(new DocumentPart("&lt;h1&gt;Cover&lt;/h1&gt;"))
///     .Part(new DocumentPart("&lt;h1&gt;Chapter 1&lt;/h1&gt;", "report.odt"))
///     .Watermark("CONFIDENTIAL")
///     .AsPdf()
///     .Generate();
/// </code>
/// </summary>
public sealed class ComposeBuilder
{
    private DocumentsClient? _client;
    private readonly ComposeRequest _request = new();

    internal ComposeBuilder SetClient(DocumentsClient client) { _client = client; return this; }

    public ComposeBuilder Part(DocumentPart part) { _request.Parts.Add(part); return this; }

    public ComposeBuilder Watermark(string text) { _request.Watermark = text; return this; }
    public ComposeBuilder Watermark(WatermarkConfig config) { _request.Watermark = config; return this; }

    public ComposeBuilder Stationery(string filePath)
    {
        _request.Stationery = new StationeryConfig(FileUtils.ToBase64(filePath));
        return this;
    }

    public ComposeBuilder ContentArea(ContentArea area)
    {
        _request.ContentAreas ??= new();
        _request.ContentAreas.Add(area);
        return this;
    }

    public ComposeBuilder Invoice(InvoiceData data) { _request.InvoiceData = data; return this; }
    public ComposeBuilder Password(string pwd) { _request.Password = pwd; return this; }
    public ComposeBuilder OutputFormat(OutputFormat format) { _request.OutputFormat = format; return this; }
    public ComposeBuilder AsPdf() { _request.OutputFormat = Models.OutputFormat.PDF; return this; }
    public ComposeBuilder AsDocx() { _request.OutputFormat = Models.OutputFormat.DOCX; return this; }

    public ComposeBuilder Callback(string url, string? secret = null)
    {
        _request.CallbackUrl = url;
        _request.CallbackSecret = secret;
        return this;
    }

    /// <summary>Build the ComposeRequest without executing.</summary>
    public ComposeRequest Build() => _request;

    /// <summary>Generate the composed document (requires attached client).</summary>
    public byte[] Generate()
    {
        if (_client is null)
            throw new InvalidOperationException(
                "No client attached. Use dg.Compose() or pass the request to dg.Documents.Compose().");
        return _client.Compose(_request);
    }

    /// <summary>Generate the composed document asynchronously.</summary>
    public Task<byte[]> GenerateAsync()
    {
        if (_client is null)
            throw new InvalidOperationException("No client attached. Use dg.Compose().");
        return _client.ComposeAsync(_request);
    }
}
