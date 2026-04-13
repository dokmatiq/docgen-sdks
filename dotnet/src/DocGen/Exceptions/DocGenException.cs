namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Base exception for all DocGen SDK errors.
/// </summary>
public class DocGenException : Exception
{
    public DocGenException(string message) : base(message) { }
    public DocGenException(string message, Exception innerException) : base(message, innerException) { }
}
