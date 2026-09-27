// Exporta o pin do Instagram para MP4 em loop (1080x1080, 30 fps, sem áudio).
// Uso: node render.mjs [link-do-qr] [saida.mp4]   (precisa de playwright e ffmpeg)
import { chromium } from "playwright";
import { mkdtempSync, rmSync, existsSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";

const qr = process.argv[2] || "https://www.instagram.com/obrunookamoto";
const here = dirname(fileURLToPath(import.meta.url));
const out = process.argv[3] || join(here, "pin-instagram-bruno.mp4");
const FPS = 30;
const ffmpeg = process.env.FFMPEG || "ffmpeg";
const work = mkdtempSync(join(tmpdir(), "pin-"));

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });
// Se o gerador de QR estiver instalado localmente, serve ele no lugar do CDN (render offline).
try {
  const lib = createRequire(import.meta.url).resolve("qrcode-generator/qrcode.js");
  await page.route("**/qrcode-generator/**", (r) => r.fulfill({ body: readFileSync(lib), contentType: "text/javascript" }));
} catch {}
await page.goto(`file://${join(here, "index.html")}?export&qr=${encodeURIComponent(qr)}`);
await page.waitForFunction(() => window.__pin && window.__pin.ready());

const frames = Math.round((await page.evaluate(() => window.__pin.T)) * FPS);
for (let f = 0; f < frames; f++) {
  await page.evaluate((t) => window.__pin.render(t), f / FPS);
  await page.screenshot({ path: join(work, `f${String(f).padStart(4, "0")}.png`) });
}
await browser.close();

execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", join(work, "f%04d.png"),
  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "slow", "-tune", "animation",
  "-movflags", "+faststart", "-an", out]);
rmSync(work, { recursive: true, force: true });
console.log("ok:", out, "| QR:", qr);
