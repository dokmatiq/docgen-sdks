import { writeFileSync } from "node:fs";
import { DocGen } from "../src/index.js";

const dg = new DocGen({ apiKey: "dk_live_xxx" });

async function main() {
  // Parallel generation
  const [pdfA, pdfB, pdfC] = await Promise.all([
    dg.htmlToPdf("<h1>Document A</h1>"),
    dg.htmlToPdf("<h1>Document B</h1>"),
    dg.markdownToPdf("# Document C\n\nGenerated in parallel."),
  ]);

  writeFileSync("parallel-1.pdf", pdfA);
  writeFileSync("parallel-2.pdf", pdfB);
  writeFileSync("parallel-3.pdf", pdfC);
  console.log("Generated 3 documents in parallel");
}

main().catch(console.error);
