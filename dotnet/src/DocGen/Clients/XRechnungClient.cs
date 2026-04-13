using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for XRechnung operations.
/// </summary>
public sealed class XRechnungClient
{
    private readonly Transport _transport;

    internal XRechnungClient(Transport transport) => _transport = transport;

    /// <summary>Generate XRechnung XML from invoice data.</summary>
    public string Generate(InvoiceData invoiceData, XRechnungFormat? format = null)
    {
        var body = new Dictionary<string, object?> { ["invoiceData"] = invoiceData };
        if (format is not null) body["format"] = format;
        var result = _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post,
            "/api/xrechnung/generate", body);
        return result.TryGetValue("xml", out var xml) ? xml?.ToString() ?? "" : "";
    }

    /// <summary>Parse XRechnung XML into structured data.</summary>
    public InvoiceData Parse(string xml)
        => _transport.RequestJson<InvoiceData>(HttpMethod.Post, "/api/xrechnung/parse", new { xml });

    /// <summary>Validate XRechnung XML.</summary>
    public Dictionary<string, object> Validate(string xml)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post, "/api/xrechnung/validate", new { xml });

    /// <summary>Transform between XRechnung formats.</summary>
    public string Transform(string xml, XRechnungFormat targetFormat)
    {
        var result = _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post,
            "/api/xrechnung/transform", new { xml, targetFormat });
        return result.TryGetValue("xml", out var x) ? x?.ToString() ?? "" : "";
    }

    /// <summary>Detect if XML is XRechnung.</summary>
    public Dictionary<string, object> Detect(string xml)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post, "/api/xrechnung/detect", new { xml });

    /// <summary>Extract invoice data using AI.</summary>
    public ExtractionResult ExtractAI(string xml)
        => _transport.RequestJson<ExtractionResult>(HttpMethod.Post, "/api/xrechnung/extract-ai", new { xml });
}
