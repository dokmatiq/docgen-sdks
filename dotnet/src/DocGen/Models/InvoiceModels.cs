using System.Text.Json.Serialization;

namespace Dokmatiq.DocGen.Models;

/// <summary>
/// Structured invoice data for ZUGFeRD/XRechnung.
/// </summary>
public class InvoiceData
{
    [JsonPropertyName("invoiceNumber")]
    public string InvoiceNumber { get; set; } = "";

    [JsonPropertyName("invoiceDate")]
    public string InvoiceDate { get; set; } = "";

    [JsonPropertyName("seller")]
    public Party? Seller { get; set; }

    [JsonPropertyName("buyer")]
    public Party? Buyer { get; set; }

    [JsonPropertyName("items")]
    public List<InvoiceItem> Items { get; set; } = new();

    [JsonPropertyName("currency")]
    public string Currency { get; set; } = "EUR";

    [JsonPropertyName("bankAccount")]
    public BankAccount? BankAccount { get; set; }

    [JsonPropertyName("paymentTerms")]
    public string? PaymentTerms { get; set; }

    [JsonPropertyName("dueDate")]
    public string? DueDate { get; set; }

    [JsonPropertyName("note")]
    public string? Note { get; set; }

    [JsonPropertyName("buyerReference")]
    public string? BuyerReference { get; set; }

    [JsonPropertyName("invoiceTypeCode")]
    public string InvoiceTypeCode { get; set; } = "380";

    [JsonPropertyName("profile")]
    public ZugferdProfile Profile { get; set; } = ZugferdProfile.EN16931;

    [JsonPropertyName("xrechnungFormat")]
    public XRechnungFormat? XRechnungFormat { get; set; }
}

/// <summary>
/// Invoice party (seller or buyer).
/// </summary>
public class Party
{
    [JsonPropertyName("name")]
    public string Name { get; set; } = "";

    [JsonPropertyName("street")]
    public string? Street { get; set; }

    [JsonPropertyName("zip")]
    public string? Zip { get; set; }

    [JsonPropertyName("city")]
    public string? City { get; set; }

    [JsonPropertyName("country")]
    public string Country { get; set; } = "DE";

    [JsonPropertyName("vatId")]
    public string? VatId { get; set; }

    [JsonPropertyName("email")]
    public string? Email { get; set; }

    [JsonPropertyName("phone")]
    public string? Phone { get; set; }

    public Party() { }

    public Party(string name) { Name = name; }

    /// <summary>Create a builder for a Party.</summary>
    public static PartyBuilder Builder(string name) => new(name);
}

public class PartyBuilder
{
    private readonly Party _party;

    internal PartyBuilder(string name) { _party = new Party(name); }

    public PartyBuilder Street(string street) { _party.Street = street; return this; }
    public PartyBuilder Zip(string zip) { _party.Zip = zip; return this; }
    public PartyBuilder City(string city) { _party.City = city; return this; }
    public PartyBuilder Country(string country) { _party.Country = country; return this; }
    public PartyBuilder VatId(string vatId) { _party.VatId = vatId; return this; }
    public PartyBuilder Email(string email) { _party.Email = email; return this; }
    public PartyBuilder Phone(string phone) { _party.Phone = phone; return this; }

    public Party Build() => _party;
}

/// <summary>
/// A single line item on an invoice.
/// </summary>
public class InvoiceItem
{
    [JsonPropertyName("description")]
    public string Description { get; set; } = "";

    [JsonPropertyName("quantity")]
    public double Quantity { get; set; } = 1.0;

    [JsonPropertyName("unit")]
    public InvoiceUnit Unit { get; set; } = InvoiceUnit.PIECE;

    [JsonPropertyName("unitPrice")]
    public double UnitPrice { get; set; }

    [JsonPropertyName("vatRate")]
    public double VatRate { get; set; } = 19.0;

    public InvoiceItem() { }

    public InvoiceItem(string description, double unitPrice)
    {
        Description = description;
        UnitPrice = unitPrice;
    }

    /// <summary>Create a builder for an InvoiceItem.</summary>
    public static InvoiceItemBuilder Builder(string description, double unitPrice) => new(description, unitPrice);
}

public class InvoiceItemBuilder
{
    private readonly InvoiceItem _item;

    internal InvoiceItemBuilder(string description, double unitPrice)
    {
        _item = new InvoiceItem(description, unitPrice);
    }

    public InvoiceItemBuilder Quantity(double quantity) { _item.Quantity = quantity; return this; }
    public InvoiceItemBuilder Unit(InvoiceUnit unit) { _item.Unit = unit; return this; }
    public InvoiceItemBuilder VatRate(double vatRate) { _item.VatRate = vatRate; return this; }

    public InvoiceItem Build() => _item;
}

/// <summary>
/// Bank account for payment.
/// </summary>
public class BankAccount
{
    [JsonPropertyName("iban")]
    public string Iban { get; set; } = "";

    [JsonPropertyName("bic")]
    public string? Bic { get; set; }

    [JsonPropertyName("accountHolder")]
    public string? AccountHolder { get; set; }

    public BankAccount() { }

    public BankAccount(string iban) { Iban = iban; }

    public BankAccount(string iban, string? bic, string? accountHolder)
    {
        Iban = iban;
        Bic = bic;
        AccountHolder = accountHolder;
    }
}
