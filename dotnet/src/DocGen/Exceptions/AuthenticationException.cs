namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 401 – invalid or missing API key.
/// </summary>
public class AuthenticationException : ApiException
{
    public AuthenticationException(string message) : base(401, message) { }
}
