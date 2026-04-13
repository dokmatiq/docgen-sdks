using System.Text.Json.Serialization;

namespace Dokmatiq.DocGen.Models;

/// <summary>
/// Request for multi-part document composition.
/// </summary>
public class ComposeRequest
{
    [JsonPropertyName("parts")]
    public List<DocumentPart> Parts { get; set; } = new();

    [JsonPropertyName("watermark")]
    public object? Watermark { get; set; }

    [JsonPropertyName("stationery")]
    public StationeryConfig? Stationery { get; set; }

    [JsonPropertyName("contentAreas")]
    public List<ContentArea>? ContentAreas { get; set; }

    [JsonPropertyName("invoiceData")]
    public InvoiceData? InvoiceData { get; set; }

    [JsonPropertyName("password")]
    public string? Password { get; set; }

    [JsonPropertyName("outputFormat")]
    public OutputFormat? OutputFormat { get; set; }

    [JsonPropertyName("callbackUrl")]
    public string? CallbackUrl { get; set; }

    [JsonPropertyName("callbackSecret")]
    public string? CallbackSecret { get; set; }
}

/// <summary>
/// A single part in a composed document.
/// </summary>
public class DocumentPart
{
    [JsonPropertyName("htmlContent")]
    public string? HtmlContent { get; set; }

    [JsonPropertyName("markdownContent")]
    public string? MarkdownContent { get; set; }

    [JsonPropertyName("templateName")]
    public string? TemplateName { get; set; }

    [JsonPropertyName("templateBase64")]
    public string? TemplateBase64 { get; set; }

    [JsonPropertyName("fields")]
    public Dictionary<string, string>? Fields { get; set; }

    [JsonPropertyName("bookmarks")]
    public Dictionary<string, string>? Bookmarks { get; set; }

    [JsonPropertyName("images")]
    public List<ImageData>? Images { get; set; }

    [JsonPropertyName("qrCodes")]
    public List<QrCodeData>? QrCodes { get; set; }

    [JsonPropertyName("barcodes")]
    public List<BarcodeData>? Barcodes { get; set; }

    [JsonPropertyName("tables")]
    public Dictionary<string, TableData>? Tables { get; set; }

    [JsonPropertyName("pageSettings")]
    public PageSettings? PageSettings { get; set; }

    public DocumentPart() { }

    public DocumentPart(string htmlContent)
    {
        HtmlContent = htmlContent;
    }

    public DocumentPart(string htmlContent, string templateName)
    {
        HtmlContent = htmlContent;
        TemplateName = templateName;
    }
}
