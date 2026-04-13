using System.Text.Json.Serialization;

namespace Dokmatiq.DocGen.Models;

/// <summary>
/// Async generation job information.
/// </summary>
public class JobInfo
{
    [JsonPropertyName("jobId")] public string JobId { get; set; } = "";
    [JsonPropertyName("status")] public JobStatus Status { get; set; }
    [JsonPropertyName("createdAt")] public string? CreatedAt { get; set; }
    [JsonPropertyName("completedAt")] public string? CompletedAt { get; set; }
    [JsonPropertyName("errorMessage")] public string? ErrorMessage { get; set; }
}

/// <summary>
/// Webhook callback payload.
/// </summary>
public class WebhookPayload
{
    [JsonPropertyName("jobId")] public string JobId { get; set; } = "";
    [JsonPropertyName("status")] public string Status { get; set; } = "";
    [JsonPropertyName("completedAt")] public string? CompletedAt { get; set; }
    [JsonPropertyName("errorMessage")] public string? ErrorMessage { get; set; }
}
