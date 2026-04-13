using System.Text;
using Dokmatiq.DocGen.Internal;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for Excel workbook generation and conversion.
/// </summary>
public sealed class ExcelClient
{
    private readonly Transport _transport;

    internal ExcelClient(Transport transport) => _transport = transport;

    /// <summary>Generate an Excel workbook from a structured JSON definition. Returns XLSX bytes.</summary>
    public byte[] Generate(Dictionary<string, object> request)
        => _transport.RequestBytes(HttpMethod.Post, "/api/excel/generate", request);

    /// <summary>Convert CSV content to an Excel workbook.</summary>
    public byte[] FromCsv(string csvContent, string delimiter = ",", bool hasHeader = true, string? sheetName = null)
    {
        var body = new Dictionary<string, object?>
        {
            ["csvContent"] = csvContent,
            ["delimiter"] = delimiter,
            ["hasHeader"] = hasHeader,
            ["sheetName"] = sheetName
        };
        return _transport.RequestBytes(HttpMethod.Post, "/api/excel/from-csv", body);
    }

    /// <summary>Convert an Excel sheet to CSV text.</summary>
    public string ToCsv(string excelBase64, int sheetIndex = 0, string delimiter = ",")
    {
        var bytes = _transport.RequestBytes(HttpMethod.Post, "/api/excel/to-csv",
            new { excelBase64, sheetIndex, delimiter });
        return Encoding.UTF8.GetString(bytes);
    }

    /// <summary>Convert an Excel sheet to structured JSON.</summary>
    public Dictionary<string, object> ToJson(string excelBase64, int sheetIndex = 0, bool hasHeader = true)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post, "/api/excel/to-json",
            new { excelBase64, sheetIndex, hasHeader });

    /// <summary>Fill an Excel template with data. Returns XLSX bytes.</summary>
    public byte[] FillTemplate(string templateBase64, Dictionary<string, object>? values = null,
        Dictionary<string, List<List<object>>>? tables = null, bool recalculate = true, string? password = null)
    {
        var body = new Dictionary<string, object?>
        {
            ["templateBase64"] = templateBase64,
            ["recalculate"] = recalculate,
            ["values"] = values,
            ["tables"] = tables,
            ["password"] = password
        };
        return _transport.RequestBytes(HttpMethod.Post, "/api/excel/fill-template", body);
    }

    /// <summary>Inspect an Excel workbook and return metadata.</summary>
    public Dictionary<string, object> Inspect(string excelBase64)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Post, "/api/excel/inspect",
            new { excelBase64 });
}
