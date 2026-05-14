using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for ZUGFeRD/Factur-X operations.
/// </summary>
public sealed class ZugferdClient
{
    private readonly Transport _transport;

    internal ZugferdClient(Transport transport) => _transport = transport;

    /// <summary>Embed ZUGFeRD XML into a PDF file.</summary>
    public byte[] Embed(string filePath, InvoiceData invoiceData)
        => _transport.RequestBytes(HttpMethod.Post, "/api/zugferd/embed/base64",
            new { pdfBase64 = FileUtils.ToBase64(filePath), invoice = invoiceData });

    /// <summary>Embed ZUGFeRD XML from bytes.</summary>
    public byte[] Embed(byte[] data, InvoiceData invoiceData)
        => _transport.RequestBytes(HttpMethod.Post, "/api/zugferd/embed/base64",
            new { pdfBase64 = FileUtils.ToBase64(data), invoice = invoiceData });

    /// <summary>Extract ZUGFeRD XML from a PDF.</summary>
    public InvoiceData Extract(string filePath)
        => _transport.RequestJson<InvoiceData>(HttpMethod.Post, "/api/zugferd/extract/base64",
            new { pdfBase64 = FileUtils.ToBase64(filePath) });

    /// <summary>Validate a ZUGFeRD PDF.</summary>
    public Dictionary<string, object> Validate(string filePath)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post, "/api/zugferd/validate/base64",
            new { pdfBase64 = FileUtils.ToBase64(filePath) });
}
