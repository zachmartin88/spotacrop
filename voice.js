// Who reads the crops out loud, how fast, and in what style.
// The phone's own voices are used (iPhone ships fun ones like Grandpa, Bahh and Superstar).
import { isNative, TextToSpeech } from './native.js';
import { prettyName } from './data.js';
import { cropPun } from './puns.js';

const get = (k, d) => { try { const v = localStorage.getItem(k); return v == null ? d : v; } catch { return d; } };
const put = (k, v) => { try { localStorage.setItem(k, v); } catch { /* private mode */ } };

export const prefs = {
  uri: get('fs.voiceUri', ''),            // '' = the phone's default English voice
  rate: +get('fs.voiceRate', '1') || 1,
  style: get('fs.voiceStyle', 'friendly'),
  set(k, v) { this[k] = v; put({ uri: 'fs.voiceUri', rate: 'fs.voiceRate', style: 'fs.voiceStyle' }[k], String(v)); },
};

export const STYLES = [
  { id: 'facts', emoji: '📋', name: 'Just the facts', sample: 'Left: corn. Right: soybeans.' },
  { id: 'friendly', emoji: '😊', name: 'Friendly', sample: 'Corn on your left, soybeans on your right.' },
  { id: 'farmer', emoji: '🤠', name: 'Farmer', sample: 'Well howdy! That there\'s corn on your left.' },
  { id: 'pun', emoji: '🤪', name: 'Pun-dit', sample: 'Corn on your left. Ear-resistible!' },
  { id: 'hype', emoji: '📣', name: 'Announcer', sample: 'And on the left… it\'s CORN!' },
];
export const RATES = [{ v: 0.85, name: 'Easy' }, { v: 1, name: 'Normal' }, { v: 1.15, name: 'Quick' }];

// Friendly names for the phone's voices. Anything not listed shows under its own name.
const CAST = {
  Grandpa: ['farm', '👴', 'Porch-swing storyteller'], Grandma: ['farm', '👵', 'Pie-baking sweetheart'],
  Bahh: ['farm', '🐑', 'An actual sheep. Sort of.'], Fred: ['farm', '🤖', 'Old-school tractor robot'],
  Junior: ['farm', '🧒', 'Farm kid on a road trip'], Ralph: ['farm', '🧔', 'Deep-voiced farmhand'],
  Superstar: ['silly', '🌟', 'Sings it'], Jester: ['silly', '🤡', 'Can\'t stop laughing'],
  Whisper: ['silly', '🤫', 'Secret crops'], Bubbles: ['silly', '🫧', 'Underwater edition'],
  Boing: ['silly', '🪀', 'Very bouncy'], Wobble: ['silly', '〰️', 'Wobbly'], Zarvox: ['silly', '👽', 'Visiting alien'],
  Trinoids: ['silly', '🛸', 'More aliens'], 'Bad News': ['silly', '🎻', 'Dramatic'], 'Good News': ['silly', '🎉', 'Thrilled'],
  Bells: ['silly', '🔔', 'Rings it'], Cellos: ['silly', '🎻', 'Cello-brates'], Organ: ['silly', '🎹', 'Church organ'],
  Albert: ['silly', '🎙️', 'Gravelly'], Kathy: ['farm', '👩‍🌾', 'Classic 90s computer'],
  Samantha: ['regular', '🇺🇸', 'American'], Daniel: ['regular', '🇬🇧', 'British'], Karen: ['regular', '🇦🇺', 'Aussie'],
  Moira: ['regular', '🇮🇪', 'Irish'], Tessa: ['regular', '🇿🇦', 'South African'], Rishi: ['regular', '🇮🇳', 'Indian'],
};

let cache = null;
/** English voices on this phone: [{uri, name, lang, group, emoji, blurb, index}]. */
export async function listVoices() {
  if (cache) return cache;
  let raw = [];
  if (isNative) raw = (await TextToSpeech.getSupportedVoices().catch(() => ({ voices: [] }))).voices || [];
  else if ('speechSynthesis' in window) {
    raw = speechSynthesis.getVoices();
    if (!raw.length) {   // Chrome and Safari fill the list a moment after load
      await new Promise((r) => { speechSynthesis.addEventListener('voiceschanged', r, { once: true }); setTimeout(r, 1500); });
      raw = speechSynthesis.getVoices();
    }
  }
  const seen = new Set(), out = [];
  raw.forEach((v, index) => {
    if (!/^en[-_]/i.test(v.lang)) return;
    const name = String(v.name).replace(/\s*\((Enhanced|Premium|English.*)\)\s*/gi, '').trim();
    // One entry per name: the US one if there is one, else the first.
    const key = name.toLowerCase();
    const isUS = /en[-_]US/i.test(v.lang);
    const prev = out.find((o) => o.key === key);
    if (prev && !(isUS && !/en[-_]US/i.test(prev.lang))) return;
    if (prev) out.splice(out.indexOf(prev), 1);
    seen.add(key);
    const [group, emoji, blurb] = CAST[name] || ['regular', '🗣️', v.lang.replace('_', '-')];
    out.push({ key, uri: v.voiceURI, name, lang: v.lang, group, emoji, blurb, index });
  });
  const order = { farm: 0, regular: 1, silly: 2 };
  out.sort((a, b) => order[a.group] - order[b.group] || a.name.localeCompare(b.name));
  cache = out;
  return out;
}

/** Say something in the chosen voice. Returns when it's handed to the speech engine. */
export async function say(text, { rate = prefs.rate, uri = prefs.uri } = {}) {
  if (isNative) {
    let voice;
    if (uri) voice = (await listVoices()).find((v) => v.uri === uri)?.index;
    TextToSpeech.stop().catch(() => {});
    return TextToSpeech.speak({ text, lang: 'en-US', rate, pitch: 1, volume: 1, category: 'playback', ...(voice != null ? { voice } : {}) }).catch(() => {});
  }
  if (!('speechSynthesis' in window)) return;
  const u = new SpeechSynthesisUtterance(text);
  u.rate = rate * 1.02;
  if (uri) u.voice = speechSynthesis.getVoices().find((v) => v.voiceURI === uri) || null;
  speechSynthesis.cancel();
  speechSynthesis.speak(u);
}

export function stop() {
  if (isNative) TextToSpeech.stop().catch(() => {});
  else if ('speechSynthesis' in window) speechSynthesis.cancel();
}

const pick = (a) => a[Math.floor(Math.random() * a.length)];
const SIDE_WORD = { left: 'left', right: 'right' };

/**
 * What to say for the sides that just changed.
 * items: [{ side: 'left'|'right'|'here'|'point', code, probably }]
 */
export function phrase(items, style = prefs.style) {
  const lines = items.map(({ side, code, probably }) => {
    const crop = prettyName(code).toLowerCase();
    const where = SIDE_WORD[side];
    const maybe = probably ? 'probably ' : '';
    switch (style) {
      case 'facts':
        return `${where ? where[0].toUpperCase() + where.slice(1) : 'Around you'}: ${maybe}${crop}.`;
      case 'farmer':
        return where
          ? pick([`Well I'll be, ${maybe}${crop} on your ${where}.`, `That there's ${maybe}${crop} off to the ${where}.`, `Lookee yonder, ${maybe}${crop} on the ${where}.`])
          : pick([`${crop} all around ya, partner.`, `We're knee-deep in ${crop} now.`]);
      case 'pun':
        return `${where ? `${maybe}${crop} on your ${where}.` : `${crop} all around you.`} ${cropPun(code)}`;
      case 'hype':
        return where
          ? pick([`And on the ${where}… it's ${crop.toUpperCase()}!`, `Coming in hot on the ${where}: ${crop}!`, `Ladies and gentlemen, ${crop}, on your ${where}!`])
          : `We are SURROUNDED by ${crop}, folks!`;
      default:
        return where ? `${maybe}${crop} on your ${where}.` : `${maybe}${crop} all around you.`;
    }
  });
  // Each side's line starts with a capital ("probably corn…" → "Probably corn…").
  return lines.map((l) => l.charAt(0).toUpperCase() + l.slice(1)).join(' ');
}

/** The line said when voice is switched on. */
export function hello(style = prefs.style) {
  return {
    facts: 'Voice on.',
    friendly: 'Voice on. I\'ll name the crops as we go.',
    farmer: 'Howdy! I\'ll holler out the crops as we go.',
    pun: 'Voice on. Lettuce begin!',
    hype: 'Ladies and gentlemen, it\'s crop time!',
  }[style] || 'Voice on.';
}

/** A two-sided sample in the current style, for previews. */
export const sample = (style = prefs.style) => phrase([{ side: 'left', code: 1 }, { side: 'right', code: 5 }], style);
