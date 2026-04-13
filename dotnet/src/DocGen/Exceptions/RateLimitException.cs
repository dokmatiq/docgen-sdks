namespace Dokmatiq.DocGen.Exceptions;

/// <summary>
/// Exception thrown on HTTP 429 – rate limit exceeded.
/// </summary>
public class RateLimitException : ApiException
{
    /// <summary>Seconds until the next request is allowed.</summary>
    public double? RetryAfter { get; }

    /// <summary>Total rate limit.</summary>
    public int? Limit { get; }

    /// <summary>Remaining requests in the current window.</summary>
    public int? Remaining { get; }

    public RateLimitException(string message, double? retryAfter, int? limit, int? remaining)
        : base(429, message)
    {
        RetryAfter = retryAfter;
        Limit = limit;
        Remaining = remaining;
    }
}
