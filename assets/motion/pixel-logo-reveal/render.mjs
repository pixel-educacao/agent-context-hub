// Exporta a animação para MP4 (1920x1080, 30 fps, com áudio).
// Uso: node render.mjs [light|dark]   (precisa de playwright e ffmpeg)
import { chromium } from "playwright";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const theme = process.argv[2] || "light";
const FPS = 30;
const here = dirname(fileURLToPath(import.meta.url));
const ffmpeg = process.env.FFMPEG || "ffmpeg";
const work = mkdtempSync(join(tmpdir(), "pixel-reveal-"));

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`file://${join(here, "index.html")}?export&theme=${theme}`);
await page.waitForFunction(() => window.__pixel);
await page.evaluate(() => document.fonts.ready);

const frames = Math.round((await page.evaluate(() => window.__pixel.DURATION)) * FPS);
for (let f = 0; f < frames; f++) {
  await page.evaluate((t) => window.__pixel.render(t), f / FPS);
  await page.screenshot({ path: join(work, `f${String(f).padStart(4, "0")}.png`) });
}
writeFileSync(join(work, "audio.wav"), Buffer.from(await page.evaluate(() => window.__pixel.wav()), "base64"));
await browser.close();

const out = join(here, `pixel-logo-reveal-${theme}.mp4`);
execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", join(work, "f%04d.png"),
  "-i", join(work, "audio.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "slow",
  "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]);
rmSync(work, { recursive: true, force: true });
console.log("ok:", out);
