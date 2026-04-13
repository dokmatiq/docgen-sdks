package com.dokmatiq.docgen.builder;

import com.dokmatiq.docgen.model.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Fluent builder for structured invoice data (ZUGFeRD/XRechnung).
 *
 * <pre>{@code
 * InvoiceData invoice = dg.invoice()
 *     .number("RE-2026-001")
 *     .date("2026-04-12")
 *     .seller(Party.builder("ACME GmbH").street("Musterstr. 1").zip("10115").city("Berlin").build())
 *     .buyer(Party.builder("Kunde AG").street("Kundenweg 5").zip("20095").city("Hamburg").build())
 *     .item(InvoiceItem.builder("Beratung", 120.0).quantity(8).unit(InvoiceUnit.HOUR).build())
 *     .bank(new BankAccount("DE89370400440532013000"))
 *     .build();
 * }</pre>
 */
public class InvoiceBuilder {
    private String number;
    private String date;
    private Party seller;
    private Party buyer;
    private final List<InvoiceItem> items = new ArrayList<>();
    private String currency = "EUR";
    private BankAccount bankAccount;
    private String paymentTerms;
    private String dueDate;
    private String note;
    private String buyerReference;
    private String typeCode = "380";
    private ZugferdProfile profile = ZugferdProfile.EN16931;
    private XRechnungFormat xrechnungFormat;

    public InvoiceBuilder number(String number) { this.number = number; return this; }
    public InvoiceBuilder date(String date) { this.date = date; return this; }
    public InvoiceBuilder seller(Party seller) { this.seller = seller; return this; }
    public InvoiceBuilder buyer(Party buyer) { this.buyer = buyer; return this; }

    public InvoiceBuilder item(InvoiceItem item) { items.add(item); return this; }

    public InvoiceBuilder item(String description, double unitPrice) {
        items.add(new InvoiceItem(description, unitPrice));
        return this;
    }

    public InvoiceBuilder currency(String code) { this.currency = code; return this; }
    public InvoiceBuilder bank(BankAccount account) { this.bankAccount = account; return this; }
    public InvoiceBuilder paymentTerms(String terms) { this.paymentTerms = terms; return this; }
    public InvoiceBuilder dueDate(String dueDate) { this.dueDate = dueDate; return this; }
    public InvoiceBuilder note(String note) { this.note = note; return this; }
    public InvoiceBuilder buyerReference(String ref) { this.buyerReference = ref; return this; }
    public InvoiceBuilder typeCode(String code) { this.typeCode = code; return this; }
    public InvoiceBuilder profile(ZugferdProfile profile) { this.profile = profile; return this; }
    public InvoiceBuilder xrechnung(XRechnungFormat format) { this.xrechnungFormat = format; return this; }
    public InvoiceBuilder xrechnung() { this.xrechnungFormat = XRechnungFormat.CII; return this; }

    /** Build the InvoiceData object. */
    public InvoiceData build() {
        Objects.requireNonNull(number, "Invoice number is required");
        Objects.requireNonNull(date, "Invoice date is required");
        Objects.requireNonNull(seller, "Seller is required");
        Objects.requireNonNull(buyer, "Buyer is required");

        return new InvoiceData(
                number, date, seller, buyer, List.copyOf(items),
                currency, bankAccount, paymentTerms, dueDate, note,
                buyerReference, typeCode, profile, xrechnungFormat
        );
    }
}
