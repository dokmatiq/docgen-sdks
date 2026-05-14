import type { InvoiceUnit, XRechnungFormat, ZugferdProfile } from "./enums.js";

/** Invoice party (seller or buyer). */
export interface Party {
  name: string;
  street?: string;
  zip?: string;
  city?: string;
  country?: string;
  vatId?: string;
  email?: string;
  phone?: string;
}

/** Single line item on an invoice. */
export interface InvoiceItem {
  description: string;
  quantity?: number;
  unit?: InvoiceUnit;
  unitPrice: number;
  vatRate?: number;
}

/** Bank account details for payment. */
export interface BankAccount {
  iban: string;
  bic?: string;
  accountHolder?: string;
}

/** Structured invoice data for ZUGFeRD/Factur-X and XRechnung. */
export interface InvoiceData {
  number: string;
  date: string;
  seller: Party;
  buyer: Party;
  items: InvoiceItem[];
  currency?: string;
  bankAccount?: BankAccount;
  paymentTerms?: string;
  dueDate?: string;
  note?: string;
  buyerReference?: string;
  invoiceTypeCode?: string;
  profile?: ZugferdProfile;
  xrechnungFormat?: XRechnungFormat;
  /** @deprecated Use number. Accepted by the API for compatibility. */
  invoiceNumber?: string;
  /** @deprecated Use date. Accepted by the API for compatibility. */
  invoiceDate?: string;
  /** @deprecated Use date. Accepted by the API for compatibility. */
  issueDate?: string;
  /** @deprecated Use bankAccount. Accepted by the API for compatibility. */
  bankDetails?: BankAccount;
}
