#!/usr/bin/env node
// Captures the portal screens used by the README and the landing page from a RUNNING DEMO
// (demo/, sample data). Do not point it at a real deployment: it signs in and opens every screen.
//
//   node capture-portal.mjs [--out ./out] [--scale 1.5] [--only overview,tools]
//
//   PORTAL_URL       default http://127.0.0.1:8091
//   PORTAL_USER      default admin               (the demo's public sign-in)
//   PORTAL_PASSWORD  default admin-demo-portal   (demo only)
//   CHROMIUM_PATH    optional Chromium/Chrome binary
//
// For repeatable output, start from a fresh demo (`docker compose down -v && docker compose up -d --build`
// in demo/): the period and compact-view choices are saved per account, so an earlier session that changed
// them changes the capture. The script ends the first-run tour if it appears.
import fs from 'node:fs';
import path from 'node:path';
import { arg, launch, makeWebpEncoder } from './lib.mjs';

const base = process.env.PORTAL_URL || 'http://127.0.0.1:8091';
const out = arg('--out', './out');
const scale = Number(arg('--scale', '1.5'));
const only = arg('--only', '').split(',').filter(Boolean);
fs.mkdirSync(out, { recursive: true });

const shots = [
  { id: 'overview', hash: 'overview' },
  { id: 'tools', hash: 'tools' },
  { id: 'people', hash: 'people' },
  { id: 'devices', hash: 'devices' },
  { id: 'personal', hash: 'personal' },
  { id: 'mcp', hash: 'mcp' },
  { id: 'register', hash: 'register' },
  { id: 'registry', hash: 'registry', prepare: async (p) => { await p.click('summary:has-text("製品に同梱のツール定義")'); await p.waitForTimeout(600); } },
  { id: 'paste', hash: 'paste' },
  { id: 'iso', hash: 'iso' },
  { id: 'budget', hash: 'budget', prepare: async (p) => { const b = await p.$('text=詳細を見る'); if (b) { await b.click(); await p.waitForTimeout(700); } } },
  { id: 'agentic', hash: 'agentic' },
  { id: 'setup', hash: 'setup' },
  { id: 'coverage', hash: 'coverage' },
  { id: 'fleet', hash: 'fleet' },
  { id: 'tokens', hash: 'tokens' },
  { id: 'settings', hash: 'settings' },
  { id: 'dashboard', hash: 'dashboard', wait: 6000 },
  { id: 'diagnostics', hash: 'diagnostics' },
  { id: 'wizard', hash: 'wizard' },
];

const browser = await launch();
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: scale, locale: 'ja-JP' });
const page = await context.newPage();
await page.goto(base + '/', { waitUntil: 'networkidle' });
await page.fill('#li-user', process.env.PORTAL_USER || 'admin');
await page.fill('#li-pass', process.env.PORTAL_PASSWORD || 'admin-demo-portal');
await page.click('[data-act="do-login"]');
await page.waitForTimeout(2500);
await page.evaluate(() => { location.hash = '#overview'; });
try {
  await page.waitForSelector('[data-tour-act="skip"]', { timeout: 9000 });
  await page.click('[data-tour-act="skip"]');
  await page.waitForTimeout(900);
  const close = await page.$('#tourdlg[open] [data-act="tour-notice-close"]');
  if (close) await close.click();
} catch { /* the tour does not show twice for an account */ }

const toWebp = await makeWebpEncoder(context);
const manifest = {};
for (const shot of shots) {
  if (only.length && !only.includes(shot.id)) continue;
  await page.evaluate((h) => { location.hash = '#' + h; }, shot.hash);
  await page.waitForTimeout(shot.wait || 2600);
  try { await page.waitForLoadState('networkidle', { timeout: 8000 }); } catch { /* keep going */ }
  if (shot.prepare) await shot.prepare(page);
  await page.mouse.move(700, 880); // keep the pointer off hover states
  const png = await page.screenshot();
  const webp = await toWebp(png);
  fs.writeFileSync(path.join(out, shot.id + '.png'), png);
  fs.writeFileSync(path.join(out, shot.id + '.webp'), webp);
  manifest[shot.id] = { webp: webp.length, png: png.length };
  console.log(shot.id.padEnd(12), 'webp', String(webp.length).padStart(7), 'png', String(png.length).padStart(8));
}
fs.writeFileSync(path.join(out, 'manifest.json'), JSON.stringify(manifest, null, 2));
await browser.close();
