using System.Text.Json.Serialization;

namespace Dokmatiq.DocGen.Models;

public class ImageData
{
    [JsonPropertyName("bookmarkName")] public string BookmarkName { get; set; } = "";
    [JsonPropertyName("base64")] public string Base64 { get; set; } = "";
    [JsonPropertyName("width")] public int? Width { get; set; }
    [JsonPropertyName("height")] public int? Height { get; set; }
    [JsonPropertyName("altText")] public string? AltText { get; set; }

    public ImageData() { }
    public ImageData(string bookmarkName, string base64, int? width = null, int? height = null, string? altText = null)
    {
        BookmarkName = bookmarkName; Base64 = base64; Width = width; Height = height; AltText = altText;
    }
}

public class QrCodeData
{
    [JsonPropertyName("bookmarkName")] public string BookmarkName { get; set; } = "";
    [JsonPropertyName("content")] public string Content { get; set; } = "";
    [JsonPropertyName("width")] public int? Width { get; set; }
    [JsonPropertyName("height")] public int? Height { get; set; }
    [JsonPropertyName("errorCorrectionLevel")] public string? ErrorCorrectionLevel { get; set; }

    public QrCodeData() { }
    public QrCodeData(string bookmarkName, string content, int? width = null, int? height = null, string? ecl = null)
    {
        BookmarkName = bookmarkName; Content = content; Width = width; Height = height; ErrorCorrectionLevel = ecl;
    }
}

public class BarcodeData
{
    [JsonPropertyName("bookmarkName")] public string BookmarkName { get; set; } = "";
    [JsonPropertyName("content")] public string Content { get; set; } = "";
    [JsonPropertyName("format")] public BarcodeFormat? Format { get; set; }
    [JsonPropertyName("width")] public int? Width { get; set; }
    [JsonPropertyName("height")] public int? Height { get; set; }

    public BarcodeData() { }
    public BarcodeData(string bookmarkName, string content, BarcodeFormat? format = null, int? width = null, int? height = null)
    {
        BookmarkName = bookmarkName; Content = content; Format = format; Width = width; Height = height;
    }
}

public class TableData
{
    [JsonPropertyName("columns")] public List<ColumnDef>? Columns { get; set; }
    [JsonPropertyName("rows")] public List<List<string>>? Rows { get; set; }
    [JsonPropertyName("style")] public TableStyle? Style { get; set; }

    public TableData() { }
    public TableData(List<ColumnDef> columns, List<List<string>> rows)
    {
        Columns = columns; Rows = rows;
    }
}

public class ColumnDef
{
    [JsonPropertyName("header")] public string Header { get; set; } = "";
    [JsonPropertyName("width")] public string? Width { get; set; }
    [JsonPropertyName("alignment")] public TextAlignment? Alignment { get; set; }
    [JsonPropertyName("format")] public string? Format { get; set; }
}

public class TableStyle
{
    [JsonPropertyName("headerBackground")] public string? HeaderBackground { get; set; }
    [JsonPropertyName("headerColor")] public string? HeaderColor { get; set; }
    [JsonPropertyName("borderColor")] public string? BorderColor { get; set; }
    [JsonPropertyName("alternateRowBackground")] public string? AlternateRowBackground { get; set; }
}

public class PageSettings
{
    [JsonPropertyName("paperSize")] public PaperSize? PaperSize { get; set; }
    [JsonPropertyName("orientation")] public PageOrientation? Orientation { get; set; }
    [JsonPropertyName("marginTop")] public double? MarginTop { get; set; }
    [JsonPropertyName("marginBottom")] public double? MarginBottom { get; set; }
    [JsonPropertyName("marginLeft")] public double? MarginLeft { get; set; }
    [JsonPropertyName("marginRight")] public double? MarginRight { get; set; }
    [JsonPropertyName("header")] public HeaderFooterConfig? Header { get; set; }
    [JsonPropertyName("footer")] public HeaderFooterConfig? Footer { get; set; }
}

public class HeaderFooterConfig
{
    [JsonPropertyName("left")] public string? Left { get; set; }
    [JsonPropertyName("center")] public string? Center { get; set; }
    [JsonPropertyName("right")] public string? Right { get; set; }
}

public class ContentArea
{
    [JsonPropertyName("x")] public double X { get; set; }
    [JsonPropertyName("y")] public double Y { get; set; }
    [JsonPropertyName("width")] public double Width { get; set; }
    [JsonPropertyName("text")] public string? Text { get; set; }
    [JsonPropertyName("html")] public string? Html { get; set; }
    [JsonPropertyName("imageBase64")] public string? ImageBase64 { get; set; }
    [JsonPropertyName("fontSize")] public double? FontSize { get; set; }
    [JsonPropertyName("fontFamily")] public string? FontFamily { get; set; }
    [JsonPropertyName("color")] public string? Color { get; set; }
    [JsonPropertyName("alignment")] public TextAlignment? Alignment { get; set; }
    [JsonPropertyName("pages")] public string? Pages { get; set; }
}

public class StationeryConfig
{
    [JsonPropertyName("pdfBase64")] public string PdfBase64 { get; set; } = "";
    [JsonPropertyName("firstPagePdfBase64")] public string? FirstPagePdfBase64 { get; set; }

    public StationeryConfig() { }
    public StationeryConfig(string pdfBase64, string? firstPagePdfBase64 = null)
    {
        PdfBase64 = pdfBase64; FirstPagePdfBase64 = firstPagePdfBase64;
    }
}

public class WatermarkConfig
{
    [JsonPropertyName("text")] public string Text { get; set; } = "";
    [JsonPropertyName("fontSize")] public double? FontSize { get; set; }
    [JsonPropertyName("opacity")] public double? Opacity { get; set; }
    [JsonPropertyName("color")] public string? Color { get; set; }

    public WatermarkConfig() { }
    public WatermarkConfig(string text) { Text = text; }
}
