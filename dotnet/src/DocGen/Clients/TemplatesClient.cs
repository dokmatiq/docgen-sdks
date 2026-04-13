using Dokmatiq.DocGen.Internal;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for template management endpoints.
/// </summary>
public sealed class TemplatesClient
{
    private readonly Transport _transport;

    internal TemplatesClient(Transport transport) => _transport = transport;

    /// <summary>Upload a template file (ODT/DOCX).</summary>
    public Dictionary<string, object> Upload(string filePath)
        => _transport.Upload<Dictionary<string, object>>("/api/templates", "file",
            FileUtils.ReadBytes(filePath), FileUtils.DetectFilename(filePath));

    /// <summary>Upload a template from bytes.</summary>
    public Dictionary<string, object> Upload(byte[] data, string fileName)
        => _transport.Upload<Dictionary<string, object>>("/api/templates", "file", data, fileName);

    /// <summary>List all uploaded templates.</summary>
    public List<Dictionary<string, object>> List()
        => _transport.RequestList<Dictionary<string, object>>(HttpMethod.Get, "/api/templates");

    /// <summary>Delete a template by name.</summary>
    public void Delete(string name) => _transport.Delete($"/api/templates/{name}");
}
