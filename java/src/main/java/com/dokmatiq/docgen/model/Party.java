package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Invoice party (seller or buyer). */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record Party(
        String name,
        String street,
        String zip,
        String city,
        String country,
        String vatId,
        String email,
        String phone
) {
    public static Builder builder(String name) { return new Builder(name); }

    public static class Builder {
        private final String name;
        private String street, zip, city, country = "DE", vatId, email, phone;

        Builder(String name) { this.name = name; }

        public Builder street(String street) { this.street = street; return this; }
        public Builder zip(String zip) { this.zip = zip; return this; }
        public Builder city(String city) { this.city = city; return this; }
        public Builder country(String country) { this.country = country; return this; }
        public Builder vatId(String vatId) { this.vatId = vatId; return this; }
        public Builder email(String email) { this.email = email; return this; }
        public Builder phone(String phone) { this.phone = phone; return this; }

        public Party build() {
            return new Party(name, street, zip, city, country, vatId, email, phone);
        }
    }
}
