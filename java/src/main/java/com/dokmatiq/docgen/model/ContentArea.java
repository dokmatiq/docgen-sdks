package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Absolutely positioned content area on the PDF page. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ContentArea(
        double x,
        double y,
        double width,
        String text,
        String html,
        String imageBase64,
        Double fontSize,
        String fontFamily,
        String color,
        TextAlignment alignment,
        String pages
) {
    public static Builder builder(double x, double y, double width) {
        return new Builder(x, y, width);
    }

    public static class Builder {
        private final double x, y, width;
        private String text, html, imageBase64, fontFamily, color, pages;
        private Double fontSize;
        private TextAlignment alignment;

        Builder(double x, double y, double width) {
            this.x = x; this.y = y; this.width = width;
        }

        public Builder text(String text) { this.text = text; return this; }
        public Builder html(String html) { this.html = html; return this; }
        public Builder imageBase64(String base64) { this.imageBase64 = base64; return this; }
        public Builder fontSize(double fontSize) { this.fontSize = fontSize; return this; }
        public Builder fontFamily(String fontFamily) { this.fontFamily = fontFamily; return this; }
        public Builder color(String color) { this.color = color; return this; }
        public Builder alignment(TextAlignment alignment) { this.alignment = alignment; return this; }
        public Builder pages(String pages) { this.pages = pages; return this; }

        public ContentArea build() {
            return new ContentArea(x, y, width, text, html, imageBase64,
                    fontSize, fontFamily, color, alignment, pages);
        }
    }
}
