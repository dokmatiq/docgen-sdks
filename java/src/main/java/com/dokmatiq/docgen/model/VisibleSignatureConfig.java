package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Visible signature placement configuration. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record VisibleSignatureConfig(
        Integer page,
        Double x,
        Double y,
        Double width,
        Double height,
        String text,
        Double fontSize,
        String imageBase64,
        String contact
) {
    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Integer page = 1;
        private Double x = 10.0, y = 10.0, width = 200.0, height = 50.0;
        private String text, imageBase64, contact;
        private Double fontSize;

        public Builder page(int page) { this.page = page; return this; }
        public Builder x(double x) { this.x = x; return this; }
        public Builder y(double y) { this.y = y; return this; }
        public Builder width(double width) { this.width = width; return this; }
        public Builder height(double height) { this.height = height; return this; }
        public Builder text(String text) { this.text = text; return this; }
        public Builder fontSize(double fontSize) { this.fontSize = fontSize; return this; }
        public Builder imageBase64(String imageBase64) { this.imageBase64 = imageBase64; return this; }
        public Builder contact(String contact) { this.contact = contact; return this; }

        public VisibleSignatureConfig build() {
            return new VisibleSignatureConfig(page, x, y, width, height, text, fontSize, imageBase64, contact);
        }
    }
}
