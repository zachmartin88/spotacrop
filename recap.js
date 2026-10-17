// End-of-drive keepsakes: a recap card (image) and a short voice clip (video: the character's line with
// a caption), both sent through the phone's share sheet.
import { prettyName } from './data.js';
import { cropColor, cropEmoji } from './palette.js';
import { isNative, Filesystem, Share } from './native.js';

const FONT = 'Inter, -apple-system, "Segoe UI", Roboto, sans-serif';
const SITE = 'zachmartin88.github.io/spotacrop';
const GOLD = '#e8c170', INK = '#0f1218';

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
}
function backdrop(ctx, W, H) {
  ctx.fillStyle = INK; ctx.fillRect(0, 0, W, H);
  const g = ctx.createRadialGradient(W * 0.8, -H * 0.05, 0, W * 0.8, -H * 0.05, H * 0.9);
  g.addColorStop(0, 'rgba(232,193,112,.30)'); g.addColorStop(1, 'rgba(232,193,112,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
}
// Wrap text into lines that fit maxW.
function wrap(ctx, text, maxW) {
  const out = [];
  let cur = '';
  for (const w of text.split(/\s+/)) {
    const t = cur ? `${cur} ${w}` : w;
    if (ctx.measureText(t).width > maxW && cur) { out.push(cur); cur = w; } else cur = t;
  }
  if (cur) out.push(cur);
  return out;
}

/**
 * The drive at a glance. d: { miles, farmPct, top: [{code, mi}], cards: [code], states: [name], who: {emoji, name} | null, when: Date }
 */
export async function recapCard(d) {
  await document.fonts?.ready;
  const W = 1080, H = 1350, cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d');
  backdrop(ctx, W, H);
  ctx.textBaseline = 'alphabetic';
  ctx.font = `800 40px ${FONT}`; ctx.fillStyle = GOLD; ctx.fillText('Spot-a-Crop', 80, 120);
  ctx.font = `900 92px ${FONT}`; ctx.fillStyle = '#fff'; ctx.fillText('My drive', 80, 232);
  ctx.font = `600 38px ${FONT}`; ctx.fillStyle = 'rgba(255,255,255,.7)';
  ctx.fillText(d.when.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' }), 80, 292);

  // Big numbers
  const stat = (x, big, small) => {
    ctx.font = `900 120px ${FONT}`; ctx.fillStyle = '#fff'; ctx.fillText(big, x, 450);
    ctx.font = `700 34px ${FONT}`; ctx.fillStyle = 'rgba(255,255,255,.65)'; ctx.fillText(small, x, 500);
  };
  stat(80, d.miles, 'miles');
  stat(440, `${d.farmPct}%`, 'farmland');
  stat(800, String(d.top.length), d.top.length === 1 ? 'crop' : 'crops');

  // Top crops
  ctx.font = `800 34px ${FONT}`; ctx.fillStyle = GOLD; ctx.fillText('MOST SEEN', 80, 600);
  const max = d.top[0]?.mi || 1;
  d.top.slice(0, 5).forEach((r, i) => {
    const y = 640 + i * 96;
    ctx.font = `64px ${FONT}`; ctx.fillStyle = '#fff'; ctx.fillText(cropEmoji(r.code), 80, y + 62);
    ctx.font = `800 40px ${FONT}`; ctx.fillStyle = '#fff'; ctx.fillText(prettyName(r.code), 170, y + 40);
    ctx.fillStyle = 'rgba(255,255,255,.1)'; roundRect(ctx, 170, y + 56, 700, 16, 8); ctx.fill();
    ctx.fillStyle = cropColor(r.code); roundRect(ctx, 170, y + 56, Math.max(16, 700 * r.mi / max), 16, 8); ctx.fill();
    ctx.font = `700 34px ${FONT}`; ctx.fillStyle = 'rgba(255,255,255,.75)'; ctx.textAlign = 'right';
    ctx.fillText(`${r.mi < 10 ? r.mi.toFixed(1) : Math.round(r.mi)} mi`, W - 80, y + 72); ctx.textAlign = 'left';
    ctx.fillStyle = GOLD;
  });

  // New cards and states
  let y = 640 + Math.min(5, d.top.length) * 96 + 50;
  const extras = [];
  if (d.cards.length) extras.push(`🃏 ${d.cards.length} new ${d.cards.length === 1 ? 'card' : 'cards'}  ${d.cards.slice(0, 8).map(cropEmoji).join(' ')}`);
  if (d.states.length > 1) extras.push(`🗺️ ${d.states.join(' → ')}`);
  ctx.font = `700 36px ${FONT}`; ctx.fillStyle = '#fff';
  for (const e of extras) for (const l of wrap(ctx, e, W - 160)) { if (y < H - 170) { ctx.fillText(l, 80, y); y += 52; } }

  ctx.font = `700 32px ${FONT}`; ctx.fillStyle = 'rgba(255,255,255,.85)';
  ctx.fillText(d.who ? `Crops called by ${d.who.emoji} ${d.who.name}` : 'Crops called out as you drive', 80, H - 84);
  ctx.font = `600 28px ${FONT}`; ctx.fillStyle = GOLD; ctx.fillText(SITE, 80, H - 42);
  return cv;
}

// ---------- voice clip video ----------

/** Can this browser record a canvas plus audio into a video? */
export function canMakeClip() {
  return typeof MediaRecorder !== 'undefined' && !!HTMLCanvasElement.prototype.captureStream && pickMime() != null;
}
function pickMime() {
  if (typeof MediaRecorder === 'undefined') return null;
  for (const m of ['video/mp4;codecs=avc1,mp4a.40.2', 'video/mp4', 'video/webm;codecs=vp9,opus', 'video/webm']) {
    if (MediaRecorder.isTypeSupported?.(m)) return m;
  }
  return null;
}

/**
 * A 9:16 video of one line: the character, the caption appearing as it's spoken, and a little sound meter.
 * c: { bytes: ArrayBuffer (the m4a line), caption, who: {emoji, name, blurb}, crop: code | null }. Resolves to a Blob.
 */
export async function clipVideo(c) {
  await document.fonts?.ready;
  const W = 720, H = 1280, cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d');
  const ac = new (window.AudioContext || window.webkitAudioContext)();
  if (ac.state === 'suspended') await ac.resume().catch(() => {});
  const audio = await ac.decodeAudioData(c.bytes.slice(0));
  const dest = ac.createMediaStreamDestination(), an = ac.createAnalyser();
  an.fftSize = 256;
  const src = ac.createBufferSource();
  src.buffer = audio;
  src.connect(an); an.connect(dest); an.connect(ac.destination);   // you hear it while it records
  const stream = new MediaStream([...cv.captureStream(30).getVideoTracks(), ...dest.stream.getAudioTracks()]);
  const mime = pickMime();
  const rec = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 2_500_000, audioBitsPerSecond: 96_000 });
  const chunks = [];
  rec.ondataavailable = (e) => e.data.size && chunks.push(e.data);
  const done = new Promise((r) => { rec.onstop = r; });

  const LEAD = 0.5, TAIL = 1.2, total = LEAD + audio.duration + TAIL;
  const words = (c.caption || '').split(/\s+/).filter(Boolean);
  const levels = new Uint8Array(an.frequencyBinCount);
  let t0 = null, started = false, raf = 0;
  const draw = (now) => {
    t0 ??= now;
    const t = (now - t0) / 1000;
    if (!started && t >= LEAD) { started = true; src.start(); }
    an.getByteFrequencyData(levels);
    const lvl = started && t < LEAD + audio.duration ? levels.slice(2, 40).reduce((a, b) => a + b, 0) / (38 * 255) : 0;
    backdrop(ctx, W, H);
    ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
    ctx.font = `800 30px ${FONT}`; ctx.fillStyle = GOLD; ctx.fillText('Spot-a-Crop', W / 2, 110);
    // The character, bobbing with their voice
    const s = 1 + lvl * 0.25;
    ctx.save(); ctx.translate(W / 2, 430); ctx.scale(s, s);
    ctx.beginPath(); ctx.arc(0, 0, 150, 0, Math.PI * 2); ctx.fillStyle = 'rgba(232,193,112,.14)'; ctx.fill();
    ctx.lineWidth = 4; ctx.strokeStyle = 'rgba(232,193,112,.6)'; ctx.stroke();
    ctx.font = `170px ${FONT}`; ctx.textBaseline = 'middle'; ctx.fillStyle = '#fff'; ctx.fillText(c.who.emoji, 0, 8);
    ctx.restore();
    ctx.textBaseline = 'alphabetic';
    ctx.font = `900 50px ${FONT}`; ctx.fillStyle = '#fff'; ctx.fillText(c.who.name, W / 2, 660);
    ctx.font = `600 30px ${FONT}`; ctx.fillStyle = 'rgba(255,255,255,.6)'; ctx.fillText(c.who.blurb || '', W / 2, 706);
    // Caption: words appear as they're spoken (spread evenly over the line)
    const shown = started ? Math.min(words.length, Math.ceil(words.length * Math.min(1, (t - LEAD) / Math.max(0.5, audio.duration * 0.92)))) : 0;
    ctx.font = `800 46px ${FONT}`;
    const lines = wrap(ctx, words.join(' '), W - 120);
    let n = 0;
    lines.forEach((l, i) => {
      const lw = l.split(' ');
      const vis = lw.slice(0, Math.max(0, shown - n)).join(' ');
      n += lw.length;
      const y = 820 + i * 62;
      ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.fillText(l, W / 2, y);
      if (vis) {
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'left';
        ctx.fillText(vis, W / 2 - ctx.measureText(l).width / 2, y);
        ctx.textAlign = 'center';
      }
    });
    // Sound meter
    const bars = 24, bw = 12, gap = 8, x0 = W / 2 - (bars * (bw + gap) - gap) / 2;
    for (let i = 0; i < bars; i++) {
      const v = started ? levels[3 + i * 2] / 255 : 0, h = 8 + v * 70;
      ctx.fillStyle = 'rgba(232,193,112,.85)'; roundRect(ctx, x0 + i * (bw + gap), 1110 - h / 2, bw, h, 6); ctx.fill();
    }
    if (c.crop != null) {
      ctx.font = `600 28px ${FONT}`; ctx.fillStyle = 'rgba(255,255,255,.7)';
      ctx.fillText(`${cropEmoji(c.crop)} ${prettyName(c.crop)}`, W / 2, 1200);
    }
    if (t < total) raf = requestAnimationFrame(draw);
    else rec.stop();
  };
  rec.start(250);
  raf = requestAnimationFrame(draw);
  await done;
  cancelAnimationFrame(raf);
  stream.getTracks().forEach((tr) => tr.stop());
  ac.close().catch(() => {});
  return new Blob(chunks, { type: (mime || 'video/mp4').split(';')[0] });
}

/** Share a file (image or video) through the phone's share sheet, or download it on desktop. */
export async function shareBlob(blob, { filename, title, text }) {
  const full = `${text} https://${SITE}/`;
  if (isNative) {
    const data = await new Promise((r) => { const f = new FileReader(); f.onload = () => r(String(f.result).split(',')[1]); f.readAsDataURL(blob); });
    const { uri } = await Filesystem.writeFile({ path: filename, data, directory: 'CACHE' });
    try { await Share.share({ title, text: full, files: [uri], dialogTitle: title }); return 'shared'; } catch { return 'cancelled'; }
  }
  const file = new File([blob], filename, { type: blob.type });
  const data = { files: [file], title, text: full };
  if (navigator.canShare?.(data)) {
    try { await navigator.share(data); return 'shared'; } catch (e) { if (e.name === 'AbortError') return 'cancelled'; }
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  return 'downloaded';
}
export const canvasBlob = (cv) => new Promise((r) => cv.toBlob(r, 'image/png'));
