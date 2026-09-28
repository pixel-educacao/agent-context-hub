// Exporta o vídeo "empresa agêntica" para MP4 (1920x1080, 30 fps, com áudio).
// Uso: node render.mjs [saida.mp4]   (precisa de playwright e ffmpeg)
import { chromium } from "playwright";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.argv[2] || join(here, "empresa-agentica.mp4");
const FPS = 30;
const ffmpeg = process.env.FFMPEG || "ffmpeg";
const work = mkdtempSync(join(tmpdir(), "agentica-"));

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`file://${join(here, "index.html")}?export`);
await page.waitForFunction(() => window.__film && window.__film.ready());

const frames = Math.round((await page.evaluate(() => window.__film.T)) * FPS);
for (let f = 0; f < frames; f++) {
  await page.evaluate((t) => window.__film.render(t), f / FPS);
  await page.screenshot({ path: join(work, `f${String(f).padStart(5, "0")}.png`) });
}
writeFileSync(join(work, "audio.wav"), Buffer.from(await page.evaluate(() => window.__film.wav()), "base64"));
await browser.close();

execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", join(work, "f%05d.png"),
  "-i", join(work, "audio.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow",
  "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]);
rmSync(work, { recursive: true, force: true });
console.log("ok:", out);
