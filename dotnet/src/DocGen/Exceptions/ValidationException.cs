namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 400 with field-level validation errors.
/// </summary>
public class ValidationException : ApiException
{
    /// <summary>Per-field validation errors.</summary>
    public IReadOnlyDictionary<string, string>? FieldErrors { get; }

    /// <summary>Optional hint for fixing the error.</summary>
    public string? Hint { get; }

    public ValidationException(string message, string? responseBody,
        IReadOnlyDictionary<string, string>? fieldErrors, string? hint)
        : base(400, message, responseBody)
    {
        FieldErrors = fieldErrors;
        Hint = hint;
    }
}
