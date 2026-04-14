using Dokmatiq.DocGen.Builders;
using Dokmatiq.DocGen.Clients;
using Dokmatiq.DocGen.Internal;

namespace Dokmatiq.DocGen;

/// <summary>
/// Main DocGen SDK client.
/// <code>
/// using var dg = new DocGenClient("dk_live_xxx");
///
/// // One-liner
/// byte[] pdf = dg.HtmlToPdf("&lt;h1&gt;Hello World&lt;/h1&gt;");
///
/// // Fluent builder
/// byte[] invoice = dg.Document()
///     .Html("&lt;h1&gt;Rechnung&lt;/h1&gt;")
///     .Template("invoice.odt")
///     .Field("nr", "2026-001")
///     .AsPdf()
///     .Generate();
/// </code>
/// </summary>
public sealed class DocGenClient : IDisposable
{
    private readonly Transport _transport;

    /// <summary>Document generation and async jobs.</summary>
    public DocumentsClient Documents { get; }

    /// <summary>Template management (upload, list, delete).</summary>
    public TemplatesClient Templates { get; }

    /// <summary>Font management (upload, list, delete).</summary>
    public FontsClient Fonts { get; }

    /// <summary>PDF form inspection and filling.</summary>
    public PdfFormsClient PdfForms { get; }

    /// <summary>Digital signature operations.</summary>
    public SignaturesClient Signatures { get; }

    /// <summary>PDF manipulation tools (merge, split, rotate, etc.).</summary>
    public PdfToolsClient PdfTools { get; }

    /// <summary>PDF page preview rendering.</summary>
    public PreviewClient Preview { get; }

    /// <summary>ZUGFeRD/Factur-X operations.</summary>
    public ZugferdClient Zugferd { get; }

    /// <summary>XRechnung operations.</summary>
    public XRechnungClient XRechnung { get; }

    /// <summary>Excel workbook generation and conversion.</summary>
    public ExcelClient Excel { get; }

    /// <summary>AI-powered receipt and ticket data extraction.</summary>
    public ReceiptsClient Receipts { get; }

    /// <summary>
    /// Create a new DocGen client with full configuration.
    /// </summary>
    public DocGenClient(DocGenConfig config)
    {
        _transport = new Transport(config);
        Documents = new DocumentsClient(_transport);
        Templates = new TemplatesClient(_transport);
        Fonts = new FontsClient(_transport);
        PdfForms = new PdfFormsClient(_transport);
        Signatures = new SignaturesClient(_transport);
        PdfTools = new PdfToolsClient(_transport);
        Preview = new PreviewClient(_transport);
        Zugferd = new ZugferdClient(_transport);
        XRechnung = new XRechnungClient(_transport);
        Excel = new ExcelClient(_transport);
        Receipts = new ReceiptsClient(_transport);
    }

    /// <summary>
    /// Create a new DocGen client with just an API key.
    /// </summary>
    public DocGenClient(string apiKey) : this(new DocGenConfig(apiKey)) { }

    // ── Builder entry points ────────────────────────────────────────

    /// <summary>Create a DocumentBuilder for fluent document construction.</summary>
    public DocumentBuilder Document() => new DocumentBuilder().SetClient(Documents);

    /// <summary>Create a ComposeBuilder for multi-part composition.</summary>
    public ComposeBuilder Compose() => new ComposeBuilder().SetClient(Documents);

    /// <summary>Create an InvoiceBuilder for structured invoice data.</summary>
    public InvoiceBuilder Invoice() => new();

    // ── Convenience methods ─────────────────────────────────────────

    /// <summary>Convert HTML to PDF in one call.</summary>
    public byte[] HtmlToPdf(string html) => Document().Html(html).AsPdf().Generate();

    /// <summary>Convert Markdown to PDF in one call.</summary>
    public byte[] MarkdownToPdf(string markdown) => Document().Markdown(markdown).AsPdf().Generate();

    /// <summary>Merge multiple PDF files into one.</summary>
    public byte[] MergePdfs(IEnumerable<string> filePaths) => PdfTools.Merge(filePaths);

    /// <summary>Merge PDF byte arrays.</summary>
    public byte[] MergePdfs(params byte[][] pdfs) => PdfTools.Merge(pdfs);

    /// <summary>Sign a PDF with a certificate.</summary>
    public byte[] SignPdf(string filePath, string certificateName, string certificatePassword)
        => Signatures.Sign(filePath, certificateName, certificatePassword);

    /// <summary>Fill form fields in a PDF.</summary>
    public byte[] FillForm(string filePath, Dictionary<string, string> fields, bool flatten = false)
        => PdfForms.Fill(filePath, fields, flatten);

    /// <summary>Fill form fields from bytes.</summary>
    public byte[] FillForm(byte[] data, Dictionary<string, string> fields, bool flatten = false)
        => PdfForms.Fill(data, fields, flatten);

    public void Dispose() => _transport.Dispose();
}
