using Dokmatiq.DocGen.Internal;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for font management endpoints.
/// </summary>
public sealed class FontsClient
{
    private readonly Transport _transport;

    internal FontsClient(Transport transport) => _transport = transport;

    /// <summary>Upload a font file (TTF/OTF).</summary>
    public Dictionary<string, object> Upload(string filePath)
        => _transport.Upload<Dictionary<string, object>>("/api/fonts", "file",
            FileUtils.ReadBytes(filePath), FileUtils.DetectFilename(filePath));

    /// <summary>Upload a font from bytes.</summary>
    public Dictionary<string, object> Upload(byte[] data, string fileName)
        => _transport.Upload<Dictionary<string, object>>("/api/fonts", "file", data, fileName);

    /// <summary>List all uploaded fonts.</summary>
    public List<Dictionary<string, object>> List()
        => _transport.RequestList<Dictionary<string, object>>(HttpMethod.Get, "/api/fonts");

    /// <summary>Delete a font by name.</summary>
    public void Delete(string name) => _transport.Delete($"/api/fonts/{name}");
}
