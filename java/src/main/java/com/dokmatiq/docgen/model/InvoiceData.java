package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

/** Structured invoice data for ZUGFeRD/Factur-X and XRechnung. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record InvoiceData(
        @JsonProperty("number")
        String invoiceNumber,
        @JsonProperty("date")
        String invoiceDate,
        Party seller,
        Party buyer,
        List<InvoiceItem> items,
        String currency,
        BankAccount bankAccount,
        String paymentTerms,
        String dueDate,
        String note,
        String buyerReference,
        String invoiceTypeCode,
        ZugferdProfile profile,
        XRechnungFormat xrechnungFormat
) {}
