package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Header/footer configuration with left/center/right sections. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record HeaderFooterConfig(
        String left,
        String center,
        String right,
        Double fontSize,
        String fontFamily,
        String color
) {
    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private String left, center, right, fontFamily, color;
        private Double fontSize;

        public Builder left(String left) { this.left = left; return this; }
        public Builder center(String center) { this.center = center; return this; }
        public Builder right(String right) { this.right = right; return this; }
        public Builder fontSize(double fontSize) { this.fontSize = fontSize; return this; }
        public Builder fontFamily(String fontFamily) { this.fontFamily = fontFamily; return this; }
        public Builder color(String color) { this.color = color; return this; }

        public HeaderFooterConfig build() {
            return new HeaderFooterConfig(left, center, right, fontSize, fontFamily, color);
        }
    }
}
