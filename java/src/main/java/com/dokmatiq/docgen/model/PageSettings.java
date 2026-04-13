package com.dokmatiq.docgen.model;

import com.fasterxml.jackson.annotation.JsonInclude;

/** Page layout and margin settings. */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record PageSettings(
        PaperSize paperSize,
        PageOrientation orientation,
        Double marginTop,
        Double marginBottom,
        Double marginLeft,
        Double marginRight,
        HeaderFooterConfig header,
        HeaderFooterConfig footer,
        HeaderFooterConfig firstPageHeader,
        HeaderFooterConfig firstPageFooter,
        HeaderFooterConfig evenPageHeader,
        HeaderFooterConfig evenPageFooter
) {
    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private PaperSize paperSize;
        private PageOrientation orientation;
        private Double marginTop, marginBottom, marginLeft, marginRight;
        private HeaderFooterConfig header, footer;
        private HeaderFooterConfig firstPageHeader, firstPageFooter;
        private HeaderFooterConfig evenPageHeader, evenPageFooter;

        public Builder paperSize(PaperSize paperSize) { this.paperSize = paperSize; return this; }
        public Builder orientation(PageOrientation orientation) { this.orientation = orientation; return this; }
        public Builder marginTop(double v) { this.marginTop = v; return this; }
        public Builder marginBottom(double v) { this.marginBottom = v; return this; }
        public Builder marginLeft(double v) { this.marginLeft = v; return this; }
        public Builder marginRight(double v) { this.marginRight = v; return this; }
        public Builder header(HeaderFooterConfig header) { this.header = header; return this; }
        public Builder footer(HeaderFooterConfig footer) { this.footer = footer; return this; }
        public Builder firstPageHeader(HeaderFooterConfig h) { this.firstPageHeader = h; return this; }
        public Builder firstPageFooter(HeaderFooterConfig f) { this.firstPageFooter = f; return this; }
        public Builder evenPageHeader(HeaderFooterConfig h) { this.evenPageHeader = h; return this; }
        public Builder evenPageFooter(HeaderFooterConfig f) { this.evenPageFooter = f; return this; }

        public PageSettings build() {
            return new PageSettings(paperSize, orientation, marginTop, marginBottom,
                    marginLeft, marginRight, header, footer, firstPageHeader,
                    firstPageFooter, evenPageHeader, evenPageFooter);
        }
    }
}
