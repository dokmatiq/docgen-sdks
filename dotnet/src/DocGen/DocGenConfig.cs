namespace Dokmatiq.DocGen;

/// <summary>
/// Configuration for the DocGen client.
/// </summary>
public sealed class DocGenConfig
{
    /// <summary>API key (required). Starts with "dk_live_" or "dk_test_".</summary>
    public string ApiKey { get; }

    /// <summary>Base URL of the DocGen API. Default: https://api.dokmatiq.com</summary>
    public string BaseUrl { get; init; } = "https://api.dokmatiq.com";

    /// <summary>Request timeout. Default: 60 seconds.</summary>
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(60);

    /// <summary>Retry policy for transient failures.</summary>
    public RetryPolicy Retry { get; init; } = RetryPolicy.Default;

    /// <summary>Validation mode: "strict" or "warn". Null for default behavior.</summary>
    public string? ValidateMode { get; init; }

    public DocGenConfig(string apiKey)
    {
        ApiKey = apiKey ?? throw new ArgumentNullException(nameof(apiKey));
    }
}

/// <summary>
/// Retry policy for transient HTTP errors (429, 500, 502, 503, 504).
/// </summary>
public sealed class RetryPolicy
{
    /// <summary>Maximum number of retries. Default: 3.</summary>
    public int MaxRetries { get; init; } = 3;

    /// <summary>Initial delay before first retry. Default: 500ms.</summary>
    public TimeSpan InitialDelay { get; init; } = TimeSpan.FromMilliseconds(500);

    /// <summary>Backoff multiplier. Default: 2.0.</summary>
    public double BackoffMultiplier { get; init; } = 2.0;

    /// <summary>Maximum delay between retries. Default: 30 seconds.</summary>
    public TimeSpan MaxDelay { get; init; } = TimeSpan.FromSeconds(30);

    /// <summary>Default retry policy.</summary>
    public static RetryPolicy Default => new();
}
