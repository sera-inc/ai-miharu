#!/usr/bin/env node
// Renders the PNG / ICO exports of the Sera AI Governance symbol from the SVG sources
// in assets/brand/. The SVG files are the source of truth; nothing here draws the mark.
//
//   node tools/brand-render.cjs [--chromium /path/to/chrome] [--playwright /path/to/node_modules]
//
// Needs a headless Chromium and playwright-core. They are not dependencies of the product,
// so pass their locations (or have them resolvable). Outputs are written next to the sources.
const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const arg = (name, dflt) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const req = createRequire(path.resolve(arg('--playwright', process.cwd())) + '/');
const { chromium } = req('playwright-core');
const brand = path.join(__dirname, '..', 'assets', 'brand');
const staticDir = path.join(__dirname, '..', 'portal', 'app', 'static');

// A Windows icon holding PNG images (supported since Vista).
function ico(pngs) {
  const head = Buffer.alloc(6); head.writeUInt16LE(0, 0); head.writeUInt16LE(1, 2); head.writeUInt16LE(pngs.length, 4);
  let offset = 6 + 16 * pngs.length;
  const dir = pngs.map(({ size, data }) => {
    const e = Buffer.alloc(16);
    e.writeUInt8(size >= 256 ? 0 : size, 0); e.writeUInt8(size >= 256 ? 0 : size, 1);
    e.writeUInt16LE(1, 4); e.writeUInt16LE(32, 6); e.writeUInt32LE(data.length, 8); e.writeUInt32LE(offset, 12);
    offset += data.length; return e;
  });
  return Buffer.concat([head, ...dir, ...pngs.map(p => p.data)]);
}

(async () => {
  const browser = await chromium.launch({ executablePath: arg('--chromium'), args: ['--no-sandbox'] });
  const svg = f => 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(brand, f)).toString('base64');
  const color = svg('sera-ai-governance-symbol.svg'), white = svg('sera-ai-governance-symbol-white.svg');
  async function shot(html, w, h, transparent = true, scale = 1) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    const page = await ctx.newPage();
    await page.setContent(`<style>html,body{margin:0;background:transparent}img{display:block}</style>${html}`);
    await page.waitForFunction(() => [...document.images].every(i => i.complete));
    const buf = await page.screenshot({ omitBackground: transparent, clip: { x: 0, y: 0, width: w, height: h } });
    await ctx.close(); return buf;
  }
  const mark = (src, size) => `<img src="${src}" width="${size}" height="${size}">`;
  const write = (file, buf) => { fs.writeFileSync(file, buf); fs.chmodSync(file, 0o644); console.log('wrote', path.relative(process.cwd(), file), buf.length); };

  const png512 = await shot(mark(color, 512), 512, 512);
  write(path.join(brand, 'sera-ai-governance-symbol-512.png'), png512);
  write(path.join(staticDir, 'sera-ai-governance-symbol.png'), png512);
  write(path.join(staticDir, 'logo.png'), png512);           // /logo.png: the old upstream logo is gone

  // Apple touch icon: opaque, mark centred with margin (iOS rounds the corners itself).
  const apple = await shot(`<div style="width:180px;height:180px;background:#fff;display:flex;align-items:center;justify-content:center">${mark(color, 140)}</div>`, 180, 180, false);
  write(path.join(staticDir, 'apple-touch-icon.png'), apple);

  const sizes = [16, 32, 48];
  const pngs = [];
  for (const size of sizes) pngs.push({ size, data: await shot(mark(color, size), size, size, true, 1) });
  write(path.join(staticDir, 'favicon.ico'), ico(pngs));

  // Lockups for READMEs (light and dark surfaces). Text is rendered here, so viewers need no font.
  const lockup = (src, ink) => `<div style="width:1200px;height:300px;display:flex;align-items:center;gap:36px;padding:0 24px;box-sizing:border-box;font-family:'Noto Sans JP','Noto Sans CJK JP','Hiragino Sans','Yu Gothic',sans-serif">
    ${mark(src, 220)}<div style="color:${ink};line-height:1.15"><div style="font-size:92px;font-weight:800;letter-spacing:.01em">世良AIガバナンス</div>
    <div style="font-size:34px;font-weight:500;opacity:.8;margin-top:10px">組織で使われている AI を、端末・アカウント・費用まで見える化</div></div></div>`;
  write(path.join(brand, 'sera-ai-governance-lockup-light.png'), await shot(lockup(color, '#1a1a1a'), 1200, 300));
  write(path.join(brand, 'sera-ai-governance-lockup-dark.png'), await shot(lockup(white, '#ffffff'), 1200, 300));
  await browser.close();
})();
