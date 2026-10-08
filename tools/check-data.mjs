// Monthly check (run by .github/workflows/refresh-data.yml): has USDA published a newer crop map
// than the one data/*.json was built from? Prints a summary and sets `changed=true|false` for the
// workflow. Also reports whether USDA has published a newer national field-boundary (CSB) edition.
import fs from 'node:fs';
import { discoverLayers } from '../data.js';

const meta = JSON.parse(fs.readFileSync(new URL('../data/meta.json', import.meta.url), 'utf8'));
const layers = await discoverLayers();
const now = { live: layers.live?.layer ?? null, annual: layers.years[0] ?? null };
const changed = now.live !== meta.live || now.annual !== meta.annual;

// The app uses USDA's 2022 national field outlines. Flag when a newer national edition (2023+) appears.
let csb = false, csbName = null;
try {
  const r = await fetch('https://pdi.scinet.usda.gov/hosting/rest/services/Hosted?f=json', { signal: AbortSignal.timeout(30000) });
  const names = (await r.json()).services.map((s) => s.name).filter((n) => /Crop_Sequence_Bound/i.test(n));
  csbName = names.find((n) => +(n.match(/(\d{4})$/)?.[1] || 0) > 2022) || null;
  csb = !!csbName;
} catch { /* service unreachable this month */ }

const lines = [
  `Built from: live ${meta.live ?? '—'}, annual ${meta.annual ?? '—'} (built ${meta.built})`,
  `Available now: live ${now.live ?? '—'}, annual ${now.annual ?? '—'}`,
  changed ? '➡️ New crop map available: rebuilding data.' : '✅ Data is up to date.',
  csb ? `🟢 USDA published a newer national field-outline edition: ${csbName}.` : '✅ Field outlines: using USDA 2022 (no newer national edition yet).',
];
console.log(lines.join('\n'));
if (process.env.GITHUB_OUTPUT) fs.appendFileSync(process.env.GITHUB_OUTPUT, `changed=${changed}\ncsb=${csb}\n`);
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, lines.map((l) => `- ${l}`).join('\n') + '\n');
