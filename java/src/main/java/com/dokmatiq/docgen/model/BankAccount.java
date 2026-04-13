package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Bank account details for payment. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record BankAccount(
        String iban,
        String bic,
        String accountHolder
) {
    public BankAccount(String iban) {
        this(iban, null, null);
    }
}
