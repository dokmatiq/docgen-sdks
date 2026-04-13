/** A single rendered page preview. */
export interface PreviewPage {
  page: number;
  imageBase64: string;
  width: number;
  height: number;
}

/** Response from a multi-page preview request. */
export interface PreviewResponse {
  pages: PreviewPage[];
  totalPages: number;
}
