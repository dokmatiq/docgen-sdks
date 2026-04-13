namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 409 – resource conflict.
/// </summary>
public class ConflictException : ApiException
{
    public ConflictException(string message) : base(409, message) { }
}
