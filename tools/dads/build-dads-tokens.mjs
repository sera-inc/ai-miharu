#!/usr/bin/env node
/**
 * Builds the DADS Layer 1 token bridge that the portal serves by default.
 *
 * Source: @digital-go-jp/tailwind-theme-plugin (Digital Agency, MIT License),
 * pinned to an exact version in package.json / package-lock.json. Nothing is
 * copied from any private repository.
 *
 *   npm ci && npm run build     regenerate portal/app/static/dads/
 *   npm ci && npm run check     fail if the committed files differ (CI, review)
 *
 * The output is a machine-generated bridge: every DADS value is copied
 * verbatim under a `--dads-` prefix, and nothing is added or edited by hand.
 * Spacing and breakpoints are not variables in the plugin's CSS, so they are
 * completed from the DADS Foundation definitions (spacing, layout), the same
 * constants the design system's own bridge uses.
 */
import { mkdirSync, readFileSync, writeFileSync, existsSync, chmodSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, '..', '..', 'portal', 'app', 'static', 'dads');
const pluginDir = join(here, 'node_modules', '@digital-go-jp', 'tailwind-theme-plugin');
if (!existsSync(join(pluginDir, 'dist', 'v4.css'))) {
  console.error('The DADS plugin is not installed. Run `npm ci` in tools/dads first.');
  process.exit(2);
}
const pkg = JSON.parse(readFileSync(join(pluginDir, 'package.json'), 'utf8'));
const css = readFileSync(join(pluginDir, 'dist', 'v4.css'), 'utf8');

// 1. Variables declared in the plugin's @theme block, under a --dads- prefix.
const theme = css.match(/@theme\s*\{([\s\S]*?)\n\}/);
if (!theme) throw new Error('@theme block not found in dist/v4.css');
const vars = [...theme[1].matchAll(/--([a-z0-9-]+)\s*:\s*([^;]+);/g)]
  .map((m) => `  --dads-${m[1]}: ${m[2].trim()};`);

// 2. The plugin's text-* utilities, as variables and as classes.
const textVars = [];
const textClasses = [];
for (const m of css.matchAll(/@utility (text-[a-z0-9-]+[A-Z]?[a-z0-9-]*)\s*\{([\s\S]*?)\n\}/gi)) {
  const name = m[1].replace(/^text-/, '');
  const prop = (re) => m[2].match(re)?.[1]?.trim();
  const size = prop(/font-size\s*:\s*([^;]+);/);
  if (!size) continue; // list markers and other non-text utilities
  const weight = prop(/font-weight\s*:\s*([^;]+);/) ?? '400';
  const leading = prop(/line-height\s*:\s*([^;]+);/) ?? 'normal';
  const tracking = prop(/letter-spacing\s*:\s*([^;]+);/) ?? '0';
  textVars.push(
    `  --dads-text-${name}-size: ${size};`,
    `  --dads-text-${name}-weight: ${weight};`,
    `  --dads-text-${name}-leading: ${leading};`,
    `  --dads-text-${name}-tracking: ${tracking};`,
  );
  textClasses.push(
    `.dads-text-${name} {`,
    `  font-size: var(--dads-text-${name}-size);`,
    `  font-weight: var(--dads-text-${name}-weight);`,
    `  line-height: var(--dads-text-${name}-leading);`,
    `  letter-spacing: var(--dads-text-${name}-tracking);`,
    `}`,
  );
}

// 3. Spacing (8px base unit) and layout breakpoints from DADS Foundation.
const spacing = {
  0: '0', '05': '0.25rem', 1: '0.5rem', 2: '1rem', 3: '1.5rem',
  4: '2rem', 5: '2.5rem', 6: '3rem', 8: '4rem', 10: '5rem',
};
const breakpoints = {
  '1col-max': '767px', '12col-sm': '928px', '12col-md': '1024px',
  '12col-lg': '1280px', '12col-xl': '1440px', '12col-xxl': '1920px',
};
const extra = [
  ...Object.entries(spacing).map(([k, v]) => `  --dads-spacing-${k}: ${v};`),
  ...Object.entries(breakpoints).map(([k, v]) => `  --dads-breakpoint-${k}: ${v};`),
];

const dads = `/*
 * dads.css - DADS Layer 1 token bridge (generated; do not edit by hand)
 * Source: @digital-go-jp/tailwind-theme-plugin v${pkg.version} (dist/v4.css), MIT License.
 * Regenerate: cd tools/dads && npm ci && npm run build
 *
 * Attribution: this file was machine-converted from the design tokens of the
 * Digital Agency Design System (DADS), https://design.digital.go.jp/dads/
 * The Digital Agency is not affiliated with this product and does not endorse it.
 * Spacing and breakpoints are completed from the DADS Foundation definitions.
 * The full licence text is in licenses/dads-tailwind-theme-plugin-MIT.txt.
 */
:root {
${vars.join('\n')}

  /* --- text styles (from the plugin's text-* utilities) --- */
${textVars.join('\n')}

  /* --- spacing (DADS Foundation: 8px base scale) --- */
  /* --- breakpoints (DADS Foundation: layout) --- */
${extra.join('\n')}
}

/* --- text style classes (from the plugin's text-* utilities) --- */
${textClasses.join('\n')}
`;

const index = `/*
 * index.css - entry point for the bundled DADS Layer 1 tokens.
 * The portal links this file. When an organisation mounts its own complete
 * token directory (DADS_CSS_DIR), that directory's index.css is served instead.
 */
@import "./dads.css";
`;

const files = { 'dads.css': dads, 'index.css': index };
if (process.argv.includes('--check')) {
  let drift = false;
  for (const [name, text] of Object.entries(files)) {
    const path = join(outDir, name);
    if (!existsSync(path) || readFileSync(path, 'utf8') !== text) {
      console.error(`DRIFT: ${path} differs from what plugin v${pkg.version} generates`);
      drift = true;
    }
  }
  if (drift) process.exit(1);
  console.log(`dads tokens are current (plugin v${pkg.version}, ${vars.length} variables, ${textVars.length / 4} text styles)`);
} else {
  mkdirSync(outDir, { recursive: true });
  // Explicit modes: the portal runs as a non-root user, and a restrictive
  // umask on the machine that generates these must not leak into the image.
  chmodSync(outDir, 0o755);
  for (const [name, text] of Object.entries(files)) {
    writeFileSync(join(outDir, name), text);
    chmodSync(join(outDir, name), 0o644);
  }
  console.log(`generated ${outDir} (plugin v${pkg.version}, ${vars.length} variables, ${textVars.length / 4} text styles)`);
}
