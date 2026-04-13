package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Single line item on an invoice. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record InvoiceItem(
        String description,
        Double quantity,
        InvoiceUnit unit,
        double unitPrice,
        Double vatRate
) {
    public InvoiceItem(String description, double unitPrice) {
        this(description, 1.0, InvoiceUnit.PIECE, unitPrice, 19.0);
    }

    public static Builder builder(String description, double unitPrice) {
        return new Builder(description, unitPrice);
    }

    public static class Builder {
        private final String description;
        private final double unitPrice;
        private double quantity = 1.0;
        private InvoiceUnit unit = InvoiceUnit.PIECE;
        private double vatRate = 19.0;

        Builder(String description, double unitPrice) {
            this.description = description;
            this.unitPrice = unitPrice;
        }

        public Builder quantity(double quantity) { this.quantity = quantity; return this; }
        public Builder unit(InvoiceUnit unit) { this.unit = unit; return this; }
        public Builder vatRate(double vatRate) { this.vatRate = vatRate; return this; }

        public InvoiceItem build() {
            return new InvoiceItem(description, quantity, unit, unitPrice, vatRate);
        }
    }
}
