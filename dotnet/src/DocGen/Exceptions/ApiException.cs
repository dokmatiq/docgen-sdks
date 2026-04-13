namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown when the DocGen API returns an error HTTP status.
/// </summary>
public class ApiException : DocGenException
{
    /// <summary>HTTP status code.</summary>
    public int StatusCode { get; }

    /// <summary>Raw response body.</summary>
    public string? ResponseBody { get; }

    public ApiException(int statusCode, string message, string? responseBody = null)
        : base(message)
    {
        StatusCode = statusCode;
        ResponseBody = responseBody;
    }
}
