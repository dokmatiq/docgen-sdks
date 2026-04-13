namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 500 – internal server error.
/// </summary>
public class ServerException : ApiException
{
    public ServerException(string message, string? responseBody)
        : base(500, message, responseBody) { }
}
