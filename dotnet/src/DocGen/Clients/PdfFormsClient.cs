using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for PDF form inspection and filling.
/// </summary>
public sealed class PdfFormsClient
{
    private readonly Transport _transport;

    internal PdfFormsClient(Transport transport) => _transport = transport;

    /// <summary>Inspect form fields in a PDF file.</summary>
    public List<PdfFormField> InspectFields(string filePath)
        => _transport.RequestJson<List<PdfFormField>>(HttpMethod.Post, "/api/pdf-forms/inspect",
            new { pdfBase64 = FileUtils.ToBase64(filePath) });

    /// <summary>Inspect form fields from bytes.</summary>
    public List<PdfFormField> InspectFields(byte[] data)
        => _transport.RequestJson<List<PdfFormField>>(HttpMethod.Post, "/api/pdf-forms/inspect",
            new { pdfBase64 = FileUtils.ToBase64(data) });

    /// <summary>Fill form fields in a PDF.</summary>
    public byte[] Fill(string filePath, Dictionary<string, string> fields, bool flatten = false)
        => _transport.RequestBytes(HttpMethod.Post, "/api/pdf-forms/fill",
            new { pdfBase64 = FileUtils.ToBase64(filePath), fields, flatten });

    /// <summary>Fill form fields from bytes.</summary>
    public byte[] Fill(byte[] data, Dictionary<string, string> fields, bool flatten = false)
        => _transport.RequestBytes(HttpMethod.Post, "/api/pdf-forms/fill",
            new { pdfBase64 = FileUtils.ToBase64(data), fields, flatten });
}
