using System.Net;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Dokmatiq.DocGen.Exceptions;

namespace Dokmatiq.DocGen.Internal;

/// <summary>
/// HTTP transport layer with retry logic and error mapping.
/// </summary>
internal sealed class Transport : IDisposable
{
    private static readonly HashSet<int> RetryableCodes = new() { 429, 500, 502, 503, 504 };

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        PropertyNameCaseInsensitive = true,
        Converters = { new JsonStringEnumConverter() }
    };

    private readonly DocGenConfig _config;
    private readonly HttpClient _http;

    public Transport(DocGenConfig config)
    {
        _config = config;
        _http = new HttpClient { Timeout = config.Timeout };
    }

    /// <summary>Make a JSON request and deserialize the response.</summary>
    public async Task<T> RequestJsonAsync<T>(HttpMethod method, string path, object? body = null)
    {
        var bytes = await ExecuteAsync(method, path, SerializeBody(body), "application/json");
        return JsonSerializer.Deserialize<T>(bytes, JsonOptions)!;
    }

    /// <summary>Make a JSON request and return raw bytes.</summary>
    public async Task<byte[]> RequestBytesAsync(HttpMethod method, string path, object? body = null)
    {
        return await ExecuteAsync(method, path, SerializeBody(body), "application/json");
    }

    /// <summary>Make a JSON request and return a list.</summary>
    public async Task<List<T>> RequestListAsync<T>(HttpMethod method, string path)
    {
        var bytes = await ExecuteAsync(method, path, null, null);
        return JsonSerializer.Deserialize<List<T>>(bytes, JsonOptions) ?? new List<T>();
    }

    /// <summary>Upload a file via multipart/form-data and return deserialized response.</summary>
    public async Task<T> UploadAsync<T>(string path, string fieldName, byte[] fileBytes,
        string fileName, Dictionary<string, string>? extraFields = null)
    {
        var (body, contentType) = BuildMultipart(fieldName, fileBytes, fileName, extraFields);
        var bytes = await ExecuteAsync(HttpMethod.Post, path, body, contentType);
        return JsonSerializer.Deserialize<T>(bytes, JsonOptions)!;
    }

    /// <summary>Upload a file and return raw bytes.</summary>
    public async Task<byte[]> UploadBytesAsync(string path, string fieldName, byte[] fileBytes,
        string fileName, Dictionary<string, string>? extraFields = null)
    {
        var (body, contentType) = BuildMultipart(fieldName, fileBytes, fileName, extraFields);
        return await ExecuteAsync(HttpMethod.Post, path, body, contentType);
    }

    /// <summary>Send a DELETE request.</summary>
    public async Task DeleteAsync(string path)
    {
        await ExecuteAsync(HttpMethod.Delete, path, null, null);
    }

    // ── Synchronous wrappers ────────────────────────────────────────

    public T RequestJson<T>(HttpMethod method, string path, object? body = null)
        => RequestJsonAsync<T>(method, path, body).GetAwaiter().GetResult();

    public byte[] RequestBytes(HttpMethod method, string path, object? body = null)
        => RequestBytesAsync(method, path, body).GetAwaiter().GetResult();

    public List<T> RequestList<T>(HttpMethod method, string path)
        => RequestListAsync<T>(method, path).GetAwaiter().GetResult();

    public T Upload<T>(string path, string fieldName, byte[] fileBytes,
        string fileName, Dictionary<string, string>? extraFields = null)
        => UploadAsync<T>(path, fieldName, fileBytes, fileName, extraFields).GetAwaiter().GetResult();

    public byte[] UploadBytes(string path, string fieldName, byte[] fileBytes,
        string fileName, Dictionary<string, string>? extraFields = null)
        => UploadBytesAsync(path, fieldName, fileBytes, fileName, extraFields).GetAwaiter().GetResult();

    public void Delete(string path) => DeleteAsync(path).GetAwaiter().GetResult();

    // ── Private ─────────────────────────────────────────────────────

    private async Task<byte[]> ExecuteAsync(HttpMethod method, string path,
        byte[]? body, string? contentType)
    {
        var retry = _config.Retry;
        Exception? lastError = null;

        for (int attempt = 0; attempt <= retry.MaxRetries; attempt++)
        {
            try
            {
                using var request = new HttpRequestMessage(method, _config.BaseUrl + path);
                request.Headers.Add("X-API-Key", _config.ApiKey);

                if (_config.ValidateMode is not null)
                    request.Headers.Add("X-Validate-Mode", _config.ValidateMode);

                if (body is not null)
                {
                    request.Content = new ByteArrayContent(body);
                    if (contentType is not null)
                        request.Content.Headers.ContentType = MediaTypeHeaderValue.Parse(contentType);
                }

                using var response = await _http.SendAsync(request);
                var status = (int)response.StatusCode;

                if (status >= 200 && status < 300)
                    return await response.Content.ReadAsByteArrayAsync();

                if (RetryableCodes.Contains(status) && attempt < retry.MaxRetries)
                {
                    var delay = CalculateDelay(retry, attempt);

                    if (status == 429 && response.Headers.RetryAfter?.Delta is { } retryDelta)
                        delay = TimeSpan.FromMilliseconds(Math.Max(delay.TotalMilliseconds, retryDelta.TotalMilliseconds));

                    await Task.Delay(delay);
                    continue;
                }

                ThrowForStatus(status, response);
            }
            catch (ApiException) { throw; }
            catch (TaskCanceledException ex) when (ex.InnerException is TimeoutException)
            {
                throw new DocGenException("Request timed out", ex);
            }
            catch (HttpRequestException ex)
            {
                lastError = ex;
                if (attempt < retry.MaxRetries)
                {
                    await Task.Delay(CalculateDelay(retry, attempt));
                    continue;
                }
            }
        }

        throw new DocGenException("Request failed after all retries", lastError ?? new Exception("Unknown error"));
    }

    private static TimeSpan CalculateDelay(RetryPolicy retry, int attempt)
    {
        var delayMs = retry.InitialDelay.TotalMilliseconds * Math.Pow(retry.BackoffMultiplier, attempt);
        delayMs = Math.Min(delayMs, retry.MaxDelay.TotalMilliseconds);
        return TimeSpan.FromMilliseconds(delayMs);
    }

    private static void ThrowForStatus(int status, HttpResponseMessage response)
    {
        var body = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
        string message;

        try
        {
            using var doc = JsonDocument.Parse(body);
            var root = doc.RootElement;
            message = root.TryGetProperty("message", out var msg) ? msg.GetString() ?? $"HTTP {status}"
                    : root.TryGetProperty("error", out var err) ? err.GetString() ?? $"HTTP {status}"
                    : $"HTTP {status}";
        }
        catch
        {
            message = $"HTTP {status}";
        }

        switch (status)
        {
            case 400:
                Dictionary<string, string>? fieldErrors = null;
                string? hint = null;
                try
                {
                    using var doc = JsonDocument.Parse(body);
                    if (doc.RootElement.TryGetProperty("fieldErrors", out var fe))
                        fieldErrors = JsonSerializer.Deserialize<Dictionary<string, string>>(fe.GetRawText());
                    if (doc.RootElement.TryGetProperty("hint", out var h))
                        hint = h.GetString();
                }
                catch { /* ignore parse errors */ }
                throw new ValidationException(message, body, fieldErrors, hint);

            case 401:
                throw new AuthenticationException(message);

            case 404:
                throw new NotFoundException(message);

            case 409:
                throw new ConflictException(message);

            case 429:
                double? retryAfter = null;
                int? limit = null, remaining = null;
                if (response.Headers.RetryAfter?.Delta is { } d)
                    retryAfter = d.TotalSeconds;
                if (response.Headers.TryGetValues("X-RateLimit-Limit", out var lv))
                    limit = int.TryParse(lv.FirstOrDefault(), out var li) ? li : null;
                if (response.Headers.TryGetValues("X-RateLimit-Remaining", out var rv))
                    remaining = int.TryParse(rv.FirstOrDefault(), out var ri) ? ri : null;
                throw new RateLimitException(message, retryAfter, limit, remaining);

            case 500:
                throw new ServerException(message, body);

            case 503:
                throw new ServiceUnavailableException(message, body);

            default:
                throw new ApiException(status, message, body);
        }
    }

    private static byte[]? SerializeBody(object? body)
    {
        if (body is null) return null;
        return JsonSerializer.SerializeToUtf8Bytes(body, JsonOptions);
    }

    private static (byte[] body, string contentType) BuildMultipart(
        string fieldName, byte[] fileBytes, string fileName, Dictionary<string, string>? extraFields)
    {
        var boundary = "----DocGenBoundary" + Guid.NewGuid().ToString("N");
        using var ms = new MemoryStream();
        using var writer = new StreamWriter(ms, Encoding.UTF8, leaveOpen: true) { NewLine = "\r\n" };

        writer.Write($"--{boundary}\r\n");
        writer.Write($"Content-Disposition: form-data; name=\"{fieldName}\"; filename=\"{fileName}\"\r\n");
        writer.Write("Content-Type: application/octet-stream\r\n\r\n");
        writer.Flush();
        ms.Write(fileBytes, 0, fileBytes.Length);

        if (extraFields is not null)
        {
            foreach (var (key, value) in extraFields)
            {
                writer.Write($"\r\n--{boundary}\r\n");
                writer.Write($"Content-Disposition: form-data; name=\"{key}\"\r\n\r\n");
                writer.Write(value);
            }
        }

        writer.Write($"\r\n--{boundary}--\r\n");
        writer.Flush();

        return (ms.ToArray(), $"multipart/form-data; boundary={boundary}");
    }

    public void Dispose() => _http.Dispose();
}
