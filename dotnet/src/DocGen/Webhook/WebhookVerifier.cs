using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Dokmatiq.DocGen.Exceptions;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Webhook;

/// <summary>
/// Utility for verifying DocGen webhook signatures (HMAC-SHA256).
/// <code>
/// var payload = WebhookVerifier.Verify(requestBody, signatureHeader, secret);
/// Console.WriteLine($"Job {payload.JobId} status: {payload.Status}");
/// </code>
/// </summary>
public static class WebhookVerifier
{
    /// <summary>
    /// Verify a DocGen webhook signature and parse the payload.
    /// </summary>
    /// <param name="body">Raw request body string.</param>
    /// <param name="signature">Value of the X-DocGen-Signature header.</param>
    /// <param name="secret">The callback secret used when creating the job.</param>
    /// <returns>Parsed webhook payload.</returns>
    /// <exception cref="DocGenException">Thrown if the signature is invalid.</exception>
    public static WebhookPayload Verify(string body, string signature, string secret)
        => Verify(Encoding.UTF8.GetBytes(body), signature, secret);

    /// <summary>
    /// Verify a DocGen webhook signature and parse the payload.
    /// </summary>
    public static WebhookPayload Verify(byte[] body, string signature, string secret)
    {
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
        var hash = hmac.ComputeHash(body);
        var expected = Convert.ToHexString(hash).ToLowerInvariant();

        if (!CryptographicOperations.FixedTimeEquals(
                Encoding.UTF8.GetBytes(expected),
                Encoding.UTF8.GetBytes(signature)))
        {
            throw new DocGenException("Invalid webhook signature");
        }

        return JsonSerializer.Deserialize<WebhookPayload>(body,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
            ?? throw new DocGenException("Failed to parse webhook payload");
    }
}
