// Shared helpers for the screenshot tools. Nothing here is imported by the product.
import { chromium } from 'playwright-core';

export const arg = (name, fallback) => {
  const i = process.argv.indexOf(name);
  return i > 0 ? process.argv[i + 1] : fallback;
};

export async function launch() {
  // CHROMIUM_PATH points at a Chromium/Chrome binary. Without it Playwright's own download is used
  // (`npx playwright-core install chromium`).
  return chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox'] });
}

/** Encodes a PNG buffer as WebP with the browser's own encoder, so no image library is needed. */
export async function makeWebpEncoder(context) {
  const page = await context.newPage();
  await page.setContent('<canvas id="c"></canvas>');
  return async (png, quality = 0.9) => {
    const b64 = await page.evaluate(async ([data, q]) => {
      const img = new Image();
      img.src = 'data:image/png;base64,' + data;
      await img.decode();
      const c = document.getElementById('c');
      c.width = img.width;
      c.height = img.height;
      c.getContext('2d').drawImage(img, 0, 0);
      return c.toDataURL('image/webp', q).split(',')[1];
    }, [png.toString('base64'), quality]);
    return Buffer.from(b64, 'base64');
  };
}
