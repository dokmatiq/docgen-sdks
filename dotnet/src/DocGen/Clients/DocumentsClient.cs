using Dokmatiq.DocGen.Exceptions;
using Dokmatiq.DocGen.Internal;
using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Clients;

/// <summary>
/// Client for document generation endpoints.
/// </summary>
public sealed class DocumentsClient
{
    private readonly Transport _transport;

    internal DocumentsClient(Transport transport) => _transport = transport;

    /// <summary>Generate a document synchronously.</summary>
    public byte[] Generate(DocumentRequest request)
        => _transport.RequestBytes(HttpMethod.Post, "/api/documents/generate", request);

    /// <summary>Generate a document synchronously (async).</summary>
    public Task<byte[]> GenerateAsync(DocumentRequest request)
        => _transport.RequestBytesAsync(HttpMethod.Post, "/api/documents/generate", request);

    /// <summary>Compose a multi-part document.</summary>
    public byte[] Compose(ComposeRequest request)
        => _transport.RequestBytes(HttpMethod.Post, "/api/documents/compose", request);

    /// <summary>Compose a multi-part document (async).</summary>
    public Task<byte[]> ComposeAsync(ComposeRequest request)
        => _transport.RequestBytesAsync(HttpMethod.Post, "/api/documents/compose", request);

    /// <summary>Submit an async generation job.</summary>
    public JobInfo SubmitAsync(DocumentRequest request)
        => _transport.RequestJson<JobInfo>(HttpMethod.Post, "/api/documents/generate/async", request);

    /// <summary>Get status of an async job.</summary>
    public JobInfo GetJob(string jobId)
        => _transport.RequestJson<JobInfo>(HttpMethod.Get, $"/api/jobs/{jobId}");

    /// <summary>Download the result of a completed async job.</summary>
    public byte[] DownloadJob(string jobId)
        => _transport.RequestBytes(HttpMethod.Get, $"/api/jobs/{jobId}/download");

    /// <summary>List recent async jobs.</summary>
    public List<JobInfo> ListJobs()
        => _transport.RequestList<JobInfo>(HttpMethod.Get, "/api/jobs");

    /// <summary>Poll an async job until completion.</summary>
    public byte[] WaitForJob(string jobId, TimeSpan? pollInterval = null, TimeSpan? timeout = null)
    {
        var interval = pollInterval ?? TimeSpan.FromSeconds(2);
        var deadline = DateTimeOffset.UtcNow + (timeout ?? TimeSpan.FromSeconds(120));

        while (DateTimeOffset.UtcNow < deadline)
        {
            var job = GetJob(jobId);

            if (job.Status == JobStatus.COMPLETED)
                return DownloadJob(jobId);

            if (job.Status == JobStatus.FAILED)
                throw new DocGenException($"Job {jobId} failed: {job.ErrorMessage ?? "unknown error"}");

            var remaining = deadline - DateTimeOffset.UtcNow;
            if (remaining <= TimeSpan.Zero) break;

            Thread.Sleep(interval < remaining ? interval : remaining);
        }

        throw new DocGenException($"Job {jobId} did not complete within timeout");
    }
}
