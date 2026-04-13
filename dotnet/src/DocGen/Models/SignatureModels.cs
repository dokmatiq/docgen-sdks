using System.Text.Json.Serialization;

namespace Dokmatiq.DocGen.Models;

/// <summary>
/// Configuration for visible signature placement.
/// </summary>
public class VisibleSignatureConfig
{
    [JsonPropertyName("page")] public int Page { get; set; } = 1;
    [JsonPropertyName("x")] public double X { get; set; } = 10;
    [JsonPropertyName("y")] public double Y { get; set; } = 10;
    [JsonPropertyName("width")] public double Width { get; set; } = 200;
    [JsonPropertyName("height")] public double Height { get; set; } = 50;
    [JsonPropertyName("text")] public string? Text { get; set; }
    [JsonPropertyName("fontSize")] public double? FontSize { get; set; }
    [JsonPropertyName("imageBase64")] public string? ImageBase64 { get; set; }
    [JsonPropertyName("contact")] public string? Contact { get; set; }
}

/// <summary>
/// Result of PDF signature verification.
/// </summary>
public class SignatureVerifyResult
{
    [JsonPropertyName("signed")] public bool Signed { get; set; }
    [JsonPropertyName("signatureCount")] public int SignatureCount { get; set; }
    [JsonPropertyName("allValid")] public bool AllValid { get; set; }
    [JsonPropertyName("signatures")] public List<SignatureDetail>? Signatures { get; set; }
}

public class SignatureDetail
{
    [JsonPropertyName("signerName")] public string? SignerName { get; set; }
    [JsonPropertyName("signDate")] public string? SignDate { get; set; }
    [JsonPropertyName("valid")] public bool Valid { get; set; }
    [JsonPropertyName("reason")] public string? Reason { get; set; }
    [JsonPropertyName("location")] public string? Location { get; set; }
}

/// <summary>
/// PDF form field information.
/// </summary>
public class PdfFormField
{
    [JsonPropertyName("name")] public string Name { get; set; } = "";
    [JsonPropertyName("type")] public string Type { get; set; } = "";
    [JsonPropertyName("value")] public string? Value { get; set; }
    [JsonPropertyName("options")] public List<string>? Options { get; set; }
    [JsonPropertyName("required")] public bool? Required { get; set; }
    [JsonPropertyName("readOnly")] public bool? ReadOnly { get; set; }
}

/// <summary>
/// Multi-page preview result.
/// </summary>
public class PreviewResponse
{
    [JsonPropertyName("pages")] public List<PreviewPage>? Pages { get; set; }
    [JsonPropertyName("totalPages")] public int TotalPages { get; set; }
}

public class PreviewPage
{
    [JsonPropertyName("page")] public int Page { get; set; }
    [JsonPropertyName("imageBase64")] public string ImageBase64 { get; set; } = "";
}

/// <summary>
/// AI-powered invoice extraction result.
/// </summary>
public class ExtractionResult
{
    [JsonPropertyName("invoiceNumber")] public string? InvoiceNumber { get; set; }
    [JsonPropertyName("invoiceDate")] public string? InvoiceDate { get; set; }
    [JsonPropertyName("sellerName")] public string? SellerName { get; set; }
    [JsonPropertyName("buyerName")] public string? BuyerName { get; set; }
    [JsonPropertyName("totalAmount")] public double? TotalAmount { get; set; }
    [JsonPropertyName("currency")] public string? Currency { get; set; }
    [JsonPropertyName("confidence")] public double? Confidence { get; set; }
    [JsonPropertyName("rawData")] public Dictionary<string, object>? RawData { get; set; }
}
