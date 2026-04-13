namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 503 – service temporarily unavailable.
/// </summary>
public class ServiceUnavailableException : ApiException
{
    public ServiceUnavailableException(string message, string? responseBody)
        : base(503, message, responseBody) { }
}
