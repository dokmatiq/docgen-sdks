import type {
  InvoiceData,
  InvoiceItem,
  Party,
  BankAccount,
} from "../models/invoice.js";
import type {
  XRechnungFormat,
  ZugferdProfile,
} from "../models/enums.js";

/**
 * Fluent builder for structured invoice data (ZUGFeRD/XRechnung).
 *
 * @example
 * ```ts
 * const invoice = dg.invoice()
 *   .number('RE-2026-001')
 *   .date('2026-04-12')
 *   .seller({ name: 'ACME GmbH', street: 'Musterstr. 1', zip: '10115', city: 'Berlin' })
 *   .buyer({ name: 'Kunde AG', street: 'Kundenweg 5', zip: '20095', city: 'Hamburg' })
 *   .item({ description: 'Beratung', quantity: 8, unit: InvoiceUnit.HOUR, unitPrice: 120 })
 *   .bank({ iban: 'DE89370400440532013000' })
 *   .build();
 * ```
 */
export class InvoiceBuilder {
  private _number = "";
  private _date = "";
  private _seller?: Party;
  private _buyer?: Party;
  private _items: InvoiceItem[] = [];
  private _currency = "EUR";
  private _bankAccount?: BankAccount;
  private _paymentTerms?: string;
  private _dueDate?: string;
  private _note?: string;
  private _buyerReference?: string;
  private _typeCode = "380";
  private _profile?: ZugferdProfile;
  private _xrechnungFormat?: XRechnungFormat;

  /** Set the invoice number. */
  number(invoiceNumber: string): this {
    this._number = invoiceNumber;
    return this;
  }

  /** Set the invoice date (ISO format, e.g. '2026-04-12'). */
  date(invoiceDate: string): this {
    this._date = invoiceDate;
    return this;
  }

  /** Set the seller party. */
  seller(party: Party): this {
    this._seller = party;
    return this;
  }

  /** Set the buyer party. */
  buyer(party: Party): this {
    this._buyer = party;
    return this;
  }

  /** Add a line item. */
  item(lineItem: InvoiceItem): this {
    this._items.push(lineItem);
    return this;
  }

  /** Set the currency (default: EUR). */
  currency(code: string): this {
    this._currency = code;
    return this;
  }

  /** Set the bank account for payment. */
  bank(account: BankAccount): this {
    this._bankAccount = account;
    return this;
  }

  /** Set payment terms description. */
  paymentTerms(terms: string): this {
    this._paymentTerms = terms;
    return this;
  }

  /** Set payment due date (ISO format). */
  dueDate(date: string): this {
    this._dueDate = date;
    return this;
  }

  /** Set a free-text note. */
  note(text: string): this {
    this._note = text;
    return this;
  }

  /** Set the buyer reference / Leitweg-ID. */
  buyerReference(ref: string): this {
    this._buyerReference = ref;
    return this;
  }

  /** Set the invoice type code (default: '380'). */
  typeCode(code: string): this {
    this._typeCode = code;
    return this;
  }

  /** Set the ZUGFeRD profile level. */
  profile(profile: ZugferdProfile): this {
    this._profile = profile;
    return this;
  }

  /** Enable XRechnung format. */
  xrechnung(format?: XRechnungFormat): this {
    this._xrechnungFormat = format ?? "CII";
    return this;
  }

  /** Build the InvoiceData object. */
  build(): InvoiceData {
    if (!this._number) throw new Error("Invoice number is required");
    if (!this._date) throw new Error("Invoice date is required");
    if (!this._seller) throw new Error("Seller is required");
    if (!this._buyer) throw new Error("Buyer is required");

    return {
      number: this._number,
      date: this._date,
      seller: this._seller,
      buyer: this._buyer,
      items: [...this._items],
      currency: this._currency,
      bankAccount: this._bankAccount,
      paymentTerms: this._paymentTerms,
      dueDate: this._dueDate,
      note: this._note,
      buyerReference: this._buyerReference,
      invoiceTypeCode: this._typeCode,
      profile: this._profile,
      xrechnungFormat: this._xrechnungFormat,
    };
  }
}
