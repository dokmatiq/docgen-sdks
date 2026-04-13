namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 404 – resource not found.
/// </summary>
public class NotFoundException : ApiException
{
    public NotFoundException(string message) : base(404, message) { }
}
