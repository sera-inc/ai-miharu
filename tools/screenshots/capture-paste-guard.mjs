#!/usr/bin/env node
// Records the REAL paste guard (extension/src/guard.js, unmodified) on the demo page:
// warn -> "それでも貼り付ける", then block mode. Writes paste-guard-demo.webm and three stills.
//
//   node capture-paste-guard.mjs [--out ./out]
//
//   GUARD_DEMO_URL  default http://127.0.0.1:8090/demo/   (the extension-demo service of demo/)
//   CHROMIUM_PATH   optional Chromium/Chrome binary
//
// guard.js ignores synthetic events (event.isTrusted), so the text is put on the clipboard and pasted with
// Ctrl+V. The strings are fictitious or taken from the vendors' documentation.
import fs from 'node:fs';
import path from 'node:path';
import { arg, launch, makeWebpEncoder } from './lib.mjs';

const base = process.env.GUARD_DEMO_URL || 'http://127.0.0.1:8090/demo/';
const out = arg('--out', './out');
fs.mkdirSync(out, { recursive: true });

async function paste(page, text) {
  await page.evaluate(() => document.getElementById('prompt').focus());
  await page.evaluate((t) => navigator.clipboard.writeText(t), text);
  await page.keyboard.press('Control+V');
}

const browser = await launch();
const permissions = ['clipboard-read', 'clipboard-write'];

// 1. The recording (1280x720, about 15 seconds).
const recorded = await browser.newContext({ viewport: { width: 1280, height: 720 }, locale: 'ja-JP', permissions, recordVideo: { dir: out, size: { width: 1280, height: 720 } } });
const page = await recorded.newPage();
await page.goto(base + '?mode=warn', { waitUntil: 'networkidle' });
await page.waitForTimeout(900);
await page.click('#prompt');
await page.keyboard.type('次のログを要約してください: ', { delay: 55 });
await page.waitForTimeout(500);
await paste(page, 'AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE');
await page.waitForTimeout(2600);
await page.click('button:has-text("それでも貼り付ける")');
await page.waitForTimeout(2000);
await page.goto(base + '?mode=block', { waitUntil: 'networkidle' });
await page.waitForTimeout(700);
await page.click('#prompt');
await page.keyboard.type('請求先のカード番号: ', { delay: 55 });
await page.waitForTimeout(400);
await paste(page, '4111 1111 1111 1111');
await page.waitForTimeout(3200);
const video = page.video();
await recorded.close();
fs.renameSync(await video.path(), path.join(out, 'paste-guard-demo.webm'));

// 2. Stills at 1.5x.
const stills = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5, locale: 'ja-JP', permissions });
const sp = await stills.newPage();
const toWebp = await makeWebpEncoder(stills);
const save = async (name) => {
  const png = await sp.screenshot();
  fs.writeFileSync(path.join(out, name + '.png'), png);
  fs.writeFileSync(path.join(out, name + '.webp'), await toWebp(png));
};
await sp.goto(base + '?mode=warn', { waitUntil: 'networkidle' });
await sp.click('#prompt');
await sp.keyboard.type('次のログを要約してください: ');
await paste(sp, 'AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE');
await sp.waitForTimeout(700);
await save('paste-guard-warn');
await sp.click('button:has-text("それでも貼り付ける")');
await sp.waitForTimeout(900);
await save('paste-guard-report');
await sp.goto(base + '?mode=block', { waitUntil: 'networkidle' });
await sp.click('#prompt');
await sp.keyboard.type('請求先のカード番号: ');
await paste(sp, '4111 1111 1111 1111');
await sp.waitForTimeout(700);
await save('paste-guard-block');
await browser.close();
console.log('wrote', fs.readdirSync(out).join(', '));
