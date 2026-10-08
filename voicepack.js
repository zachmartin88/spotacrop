// The recorded voice cast. Each character is one "pack": index.json (which lines exist for which
// moment) + pack.bin (all the recorded lines, back to back). A pack is downloaded once and kept on
// the phone. Lines are played one at a time, never repeating a line until its siblings have played.
import { isNative } from './native.js';

// Registered by the app itself (ios/App/App/AppViewController.swift), so it's reached through
// Capacitor.Plugins rather than registerPlugin, and looked up when first used.
const clipPlayer = () => globalThis.Capacitor?.Plugins?.ClipPlayer;
// The website serves the packs; the app fetches them from the website too.
const BASE = globalThis.SPOTACROP_VOICE_BASE || (isNative ? 'https://zachmartin88.github.io/spotacrop/voice/' : 'voice/');   // override for local testing

const lget = (k, d) => { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } };
const lput = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* full */ } };

// ---------- the cast list ----------
let castP = null;
/** [{id, name, emoji, blurb, mb, version}] from voice/cast.json. */
export function cast() {
  castP ||= fetch(`${BASE}cast.json`, { cache: 'no-cache' }).then((r) => r.json()).then((j) => j.cast).catch(() => { castP = null; return []; });
  return castP;
}

// ---------- storage (IndexedDB, works on the website and in the app) ----------
const DB = 'spotacrop-voice';
function db() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore('packs');
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}
async function idb(mode, fn) {
  const d = await db();
  return new Promise((res, rej) => {
    const tx = d.transaction('packs', mode), q = fn(tx.objectStore('packs'));
    tx.oncomplete = () => res(q?.result);
    tx.onerror = () => rej(tx.error);
  });
}

const packs = {};   // id -> { index, buf }
/** Is this character's pack on the phone (any version)? */
export async function installed(id) {
  if (packs[id]) return true;
  const p = await idb('readonly', (s) => s.get(id)).catch(() => null);
  if (p) { packs[id] = p; return true; }
  return false;
}
export async function installedVersion(id) {
  return (await installed(id)) ? packs[id].index.version : null;
}

/** Download (or update) a character's pack. onProgress(0..1). */
export async function install(id, onProgress = () => {}) {
  const idx = await (await fetch(`${BASE}${id}/index.json`, { cache: 'no-cache' })).json();
  const r = await fetch(`${BASE}${id}/pack.bin?v=${idx.version}`);
  if (!r.ok) throw new Error(`download failed (${r.status})`);
  const total = idx.bytes || +r.headers.get('content-length') || 0;
  const reader = r.body.getReader(), chunks = [];
  let got = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value); got += value.length;
    if (total) onProgress(Math.min(1, got / total));
  }
  const buf = new Uint8Array(got);
  let o = 0;
  for (const c of chunks) { buf.set(c, o); o += c.length; }
  const pack = { index: idx, buf: buf.buffer };
  await idb('readwrite', (s) => s.put(pack, id));
  packs[id] = pack;
  onProgress(1);
  return pack;
}
export async function uninstall(id) {
  delete packs[id];
  await idb('readwrite', (s) => s.delete(id)).catch(() => {});
}

// ---------- picking a line without repeats ----------
// For each character+moment we remember the order we're working through; a fresh shuffle starts
// only when every line for that moment has played, and never starts with the line just heard.
const bags = lget('fs.vbags', {});
let bagsDirty = false;
function pickIndex(id, key, n) {
  const k = `${id}|${key}`;
  let b = bags[k];
  if (!b || b.n !== n || !b.q.length) {
    const q = [...Array(n).keys()].sort(() => Math.random() - 0.5);
    if (b?.last != null && q[0] === b.last && n > 1) q.push(q.shift());
    b = bags[k] = { n, q, last: b?.last ?? null };
  }
  const i = b.q.shift();
  b.last = i;
  if (!bagsDirty) { bagsDirty = true; setTimeout(() => { bagsDirty = false; lput('fs.vbags', bags); }, 2000); }
  return i;
}

/** Does this character have a line for this moment? */
export function hasLine(id, key) { return !!packs[id]?.index.keys[key]?.length; }

function clip(id, key) {
  const p = packs[id], list = p?.index.keys[key];
  if (!list?.length) return null;
  const [off, len] = list[pickIndex(id, key, list.length)];
  return p.buf.slice(off, off + len);
}

// ---------- playing ----------
let ctx = null, webSrc = null;
function b64(buf) {
  let s = '';
  const u = new Uint8Array(buf);
  for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
  return btoa(s);
}
async function playBuf(buf, volume = 1) {
  if (isNative) {
    const r = await clipPlayer().play({ data: b64(buf), volume }).catch(() => ({ completed: false }));
    return r.completed;
  }
  ctx ||= new (window.AudioContext || window.webkitAudioContext)();
  if (ctx.state === 'suspended') await ctx.resume().catch(() => {});
  const audio = await ctx.decodeAudioData(buf.slice(0));
  return new Promise((res) => {
    const src = ctx.createBufferSource(), g = ctx.createGain();
    g.gain.value = volume;
    src.buffer = audio; src.connect(g).connect(ctx.destination);
    src.onended = () => { if (webSrc === src) webSrc = null; res(true); };
    webSrc = src; src.start();
  });
}

// One line at a time. Crop calls are "now or never": if something else is talking and a newer
// crop call comes in, the old queued one is dropped. Extras (facts, jokes) only play when it's quiet.
const queue = [];
let busy = false, lastEnd = 0;
export const isTalking = () => busy;
export const quietFor = () => (busy ? 0 : Date.now() - lastEnd);

/**
 * say(id, [key, key2, ...], { kind }) plays one line for each key in order (e.g. ['card', 'name:6']).
 * kind: 'crop' (replaces queued crop calls), 'event' (queued), 'extra' (skipped unless quiet).
 * Returns false if the character has no line for the first key.
 */
export function say(id, keys, { kind = 'event', volume = 1 } = {}) {
  keys = [].concat(keys).filter((k) => hasLine(id, k));
  if (!keys.length) return false;
  if (kind === 'extra' && (busy || queue.length)) return false;
  if (kind === 'crop') for (let i = queue.length - 1; i >= 0; i--) if (queue[i].kind === 'crop') queue.splice(i, 1);
  queue.push({ id, keys, kind, volume, at: Date.now() });
  pump();
  return true;
}
async function pump() {
  if (busy) return;
  const job = queue.shift();
  if (!job) return;
  if (Date.now() - job.at > (job.kind === 'crop' ? 8000 : 20000)) return pump();   // stale
  busy = true;
  try {
    for (const k of job.keys) {
      const buf = clip(job.id, k);
      if (buf) await playBuf(buf, job.volume);
    }
  } catch { /* a bad clip shouldn't stop the show */ }
  busy = false; lastEnd = Date.now();
  setTimeout(pump, 350);   // a breath between lines
}
export function hush() {
  queue.length = 0;
  if (isNative) clipPlayer()?.stop().catch(() => {});
  else try { webSrc?.stop(); } catch { /* not playing */ }
}
