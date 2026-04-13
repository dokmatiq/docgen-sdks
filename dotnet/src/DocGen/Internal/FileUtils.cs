namespace Dokmatiq.DocGen.Internal;

/// <summary>
/// Internal file handling utilities.
/// </summary>
internal static class FileUtils
{
    public static string ToBase64(byte[] data) => Convert.ToBase64String(data);

    public static string ToBase64(string filePath) => Convert.ToBase64String(File.ReadAllBytes(filePath));

    public static byte[] ReadBytes(string filePath) => File.ReadAllBytes(filePath);

    public static string DetectFilename(string filePath) => Path.GetFileName(filePath);
}
