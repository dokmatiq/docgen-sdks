using Dokmatiq.DocGen.Models;

namespace Dokmatiq.DocGen.Builders;

/// <summary>
/// Fluent builder for structured invoice data (ZUGFeRD/XRechnung).
/// <code>
/// var invoice = dg.Invoice()
///     .Number("RE-2026-001")
///     .Date("2026-04-13")
///     .Seller(Party.Builder("ACME GmbH").Street("Musterstr. 1").Zip("10115").City("Berlin").Build())
///     .Buyer(Party.Builder("Kunde AG").Street("Kundenweg 5").Zip("20095").City("Hamburg").Build())
///     .Item(InvoiceItem.Builder("Beratung", 120.0).Quantity(8).Unit(InvoiceUnit.HOUR).Build())
///     .Bank(new BankAccount("DE89370400440532013000"))
///     .Build();
/// </code>
/// </summary>
public sealed class InvoiceBuilder
{
    private readonly InvoiceData _data = new();

    public InvoiceBuilder Number(string number) { _data.InvoiceNumber = number; return this; }
    public InvoiceBuilder Date(string date) { _data.InvoiceDate = date; return this; }
    public InvoiceBuilder Seller(Party seller) { _data.Seller = seller; return this; }
    public InvoiceBuilder Buyer(Party buyer) { _data.Buyer = buyer; return this; }

    public InvoiceBuilder Item(InvoiceItem item) { _data.Items.Add(item); return this; }

    public InvoiceBuilder Item(string description, double unitPrice)
    {
        _data.Items.Add(new InvoiceItem(description, unitPrice));
        return this;
    }

    public InvoiceBuilder Currency(string code) { _data.Currency = code; return this; }
    public InvoiceBuilder Bank(BankAccount account) { _data.BankAccount = account; return this; }
    public InvoiceBuilder PaymentTerms(string terms) { _data.PaymentTerms = terms; return this; }
    public InvoiceBuilder DueDate(string dueDate) { _data.DueDate = dueDate; return this; }
    public InvoiceBuilder Note(string note) { _data.Note = note; return this; }
    public InvoiceBuilder BuyerReference(string reference) { _data.BuyerReference = reference; return this; }
    public InvoiceBuilder TypeCode(string code) { _data.InvoiceTypeCode = code; return this; }
    public InvoiceBuilder Profile(ZugferdProfile profile) { _data.Profile = profile; return this; }
    public InvoiceBuilder XRechnung(XRechnungFormat format) { _data.XRechnungFormat = format; return this; }
    public InvoiceBuilder XRechnung() { _data.XRechnungFormat = Models.XRechnungFormat.CII; return this; }

    /// <summary>Build the InvoiceData object.</summary>
    public InvoiceData Build()
    {
        if (string.IsNullOrEmpty(_data.InvoiceNumber))
            throw new InvalidOperationException("Invoice number is required");
        if (string.IsNullOrEmpty(_data.InvoiceDate))
            throw new InvalidOperationException("Invoice date is required");
        if (_data.Seller is null)
            throw new InvalidOperationException("Seller is required");
        if (_data.Buyer is null)
            throw new InvalidOperationException("Buyer is required");

        return _data;
    }
}
