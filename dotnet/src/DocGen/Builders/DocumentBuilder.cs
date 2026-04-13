using Dokmatiq.DocGen.Clients;
using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Builders;

/// <summary>
/// Fluent builder for constructing and executing document generation requests.
/// <code>
/// byte[] pdf = dg.Document()
///     .Html("&lt;h1&gt;Invoice {{nr}}&lt;/h1&gt;")
///     .Template("invoice.odt")
///     .Field("nr", "2026-001")
///     .Watermark("DRAFT")
///     .AsPdf()
///     .Generate();
/// </code>
/// </summary>
public sealed class DocumentBuilder
{
    private DocumentsClient? _client;
    private readonly DocumentRequest _request = new();

    internal DocumentBuilder SetClient(DocumentsClient client) { _client = client; return this; }

    public DocumentBuilder Html(string content) { _request.HtmlContent = content; return this; }
    public DocumentBuilder Markdown(string content) { _request.MarkdownContent = content; return this; }
    public DocumentBuilder Template(string name) { _request.TemplateName = name; return this; }

    public DocumentBuilder TemplateFile(string filePath)
    {
        _request.TemplateBase64 = FileUtils.ToBase64(filePath);
        return this;
    }

    public DocumentBuilder Field(string name, string value)
    {
        _request.Fields ??= new();
        _request.Fields[name] = value;
        return this;
    }

    public DocumentBuilder Fields(Dictionary<string, string> values)
    {
        _request.Fields ??= new();
        foreach (var (k, v) in values) _request.Fields[k] = v;
        return this;
    }

    public DocumentBuilder Bookmark(string name, string html)
    {
        _request.Bookmarks ??= new();
        _request.Bookmarks[name] = html;
        return this;
    }

    public DocumentBuilder MarkdownBookmark(string name, string md)
    {
        _request.MarkdownBookmarks ??= new();
        _request.MarkdownBookmarks[name] = md;
        return this;
    }

    public DocumentBuilder Image(string bookmarkName, string filePath, int? width = null, int? height = null)
    {
        _request.Images ??= new();
        _request.Images.Add(new ImageData(bookmarkName, FileUtils.ToBase64(filePath), width, height));
        return this;
    }

    public DocumentBuilder QrCode(string bookmarkName, string content, int? width = null, int? height = null)
    {
        _request.QrCodes ??= new();
        _request.QrCodes.Add(new QrCodeData(bookmarkName, content, width, height));
        return this;
    }

    public DocumentBuilder Barcode(string bookmarkName, string content, BarcodeFormat format,
        int? width = null, int? height = null)
    {
        _request.Barcodes ??= new();
        _request.Barcodes.Add(new BarcodeData(bookmarkName, content, format, width, height));
        return this;
    }

    public DocumentBuilder Table(string name, TableData data)
    {
        _request.Tables ??= new();
        _request.Tables[name] = data;
        return this;
    }

    public DocumentBuilder PageSettings(PageSettings settings) { _request.PageSettings = settings; return this; }

    public DocumentBuilder Watermark(string text) { _request.Watermark = text; return this; }
    public DocumentBuilder Watermark(WatermarkConfig config) { _request.Watermark = config; return this; }

    public DocumentBuilder Stationery(string filePath)
    {
        _request.Stationery = new StationeryConfig(FileUtils.ToBase64(filePath));
        return this;
    }

    public DocumentBuilder Stationery(string filePath, string firstPageFilePath)
    {
        _request.Stationery = new StationeryConfig(FileUtils.ToBase64(filePath), FileUtils.ToBase64(firstPageFilePath));
        return this;
    }

    public DocumentBuilder ContentArea(ContentArea area)
    {
        _request.ContentAreas ??= new();
        _request.ContentAreas.Add(area);
        return this;
    }

    public DocumentBuilder Invoice(InvoiceData data) { _request.InvoiceData = data; return this; }
    public DocumentBuilder Password(string pwd) { _request.Password = pwd; return this; }
    public DocumentBuilder OutputFormat(OutputFormat format) { _request.OutputFormat = format; return this; }
    public DocumentBuilder AsPdf() { _request.OutputFormat = Models.OutputFormat.PDF; return this; }
    public DocumentBuilder AsDocx() { _request.OutputFormat = Models.OutputFormat.DOCX; return this; }
    public DocumentBuilder AsOdt() { _request.OutputFormat = Models.OutputFormat.ODT; return this; }

    public DocumentBuilder Callback(string url, string? secret = null)
    {
        _request.CallbackUrl = url;
        _request.CallbackSecret = secret;
        return this;
    }

    public DocumentBuilder MarkdownStyles(Dictionary<string, string> styles)
    {
        _request.MarkdownStyles = styles;
        return this;
    }

    /// <summary>Build the DocumentRequest without executing.</summary>
    public DocumentRequest Build() => _request;

    /// <summary>Generate the document (requires attached client via dg.Document()).</summary>
    public byte[] Generate()
    {
        if (_client is null)
            throw new InvalidOperationException(
                "No client attached. Use dg.Document() or pass the request to dg.Documents.Generate().");
        return _client.Generate(_request);
    }

    /// <summary>Generate the document asynchronously.</summary>
    public Task<byte[]> GenerateAsync()
    {
        if (_client is null)
            throw new InvalidOperationException("No client attached. Use dg.Document().");
        return _client.GenerateAsync(_request);
    }
}
