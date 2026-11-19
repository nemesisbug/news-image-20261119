// "The World Today" — 19 November 2026 front page.
// The program is deterministic and offline: it copies the entry image
// that this repository holds into the output directory make.fun reads.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(import.meta.dirname, "entry.png");
const dst = join(outDir, "entry.png");

const bytes = readFileSync(src);
if (bytes[0] !== 0x89 || bytes[1] !== 0x50 || bytes[2] !== 0x4e || bytes[3] !== 0x47) {
  throw new Error("entry.png is not a PNG file");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
const written = readFileSync(dst);
if (!written.equals(bytes)) {
  throw new Error("entry.png copy differs from source");
}
console.log(`wrote ${dst} (${written.length} bytes)`);
