using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for digital signature operations.
/// </summary>
public sealed class SignaturesClient
{
    private readonly Transport _transport;

    internal SignaturesClient(Transport transport) => _transport = transport;

    /// <summary>Upload a PKCS#12 certificate.</summary>
    public Dictionary<string, object> UploadCertificate(string filePath, string password)
        => _transport.Upload<Dictionary<string, object>>("/api/signatures/certificates", "file",
            FileUtils.ReadBytes(filePath), FileUtils.DetectFilename(filePath),
            new Dictionary<string, string> { ["password"] = password });

    /// <summary>List uploaded certificates.</summary>
    public List<Dictionary<string, object>> ListCertificates()
        => _transport.RequestList<Dictionary<string, object>>(HttpMethod.Get, "/api/signatures/certificates");

    /// <summary>Delete a certificate by name.</summary>
    public void DeleteCertificate(string name)
        => _transport.Delete($"/api/signatures/certificates/{name}");

    /// <summary>Get certificate details.</summary>
    public Dictionary<string, object> CertificateInfo(string name)
        => _transport.RequestJson<Dictionary<string, object>>(HttpMethod.Get, $"/api/signatures/certificates/{name}");

    /// <summary>Digitally sign a PDF.</summary>
    public byte[] Sign(string filePath, string certificateName, string certificatePassword,
        string? reason = null, string? location = null, VisibleSignatureConfig? visibleSignature = null)
    {
        var body = new Dictionary<string, object?>
        {
            ["pdfBase64"] = FileUtils.ToBase64(filePath),
            ["certificateName"] = certificateName,
            ["certificatePassword"] = certificatePassword,
            ["reason"] = reason,
            ["location"] = location,
            ["visibleSignature"] = visibleSignature
        };
        return _transport.RequestBytes(HttpMethod.Post, "/api/signatures/sign", body);
    }

    /// <summary>Sign a PDF from bytes.</summary>
    public byte[] Sign(byte[] data, string certificateName, string certificatePassword)
        => _transport.RequestBytes(HttpMethod.Post, "/api/signatures/sign",
            new { pdfBase64 = FileUtils.ToBase64(data), certificateName, certificatePassword });

    /// <summary>Verify signatures in a PDF file.</summary>
    public SignatureVerifyResult Verify(string filePath)
        => _transport.RequestJson<SignatureVerifyResult>(HttpMethod.Post, "/api/signatures/verify",
            new { pdfBase64 = FileUtils.ToBase64(filePath) });

    /// <summary>Verify signatures from bytes.</summary>
    public SignatureVerifyResult Verify(byte[] data)
        => _transport.RequestJson<SignatureVerifyResult>(HttpMethod.Post, "/api/signatures/verify",
            new { pdfBase64 = FileUtils.ToBase64(data) });
}
