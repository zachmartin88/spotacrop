// What the voice says, and when. Turns driving events into lines for the chosen character
// (or a rotating cast), paced by the Chattiness setting so it's fun without being a lot.
import * as pack from './voicepack.js';

const lget = (k, d) => { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } };
const lput = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* full */ } };

export const talk = {
  who: lget('fs.talkWho', 'earl'),          // a character id, or 'mix-drive' / 'mix-line'
  chatty: lget('fs.chatty', 'normal'),      // 'crops' | 'normal' | 'chatty'
  set(k, v) { this[k] = v; lput({ who: 'fs.talkWho', chatty: 'fs.chatty' }[k], v); },
};
export const CHATTY = [
  { id: 'crops', name: 'Just crops', emoji: '🌾', blurb: 'Only the crops, nothing extra' },
  { id: 'normal', name: 'Normal', emoji: '🙂', blurb: 'Crops, plus states, finds and the odd fact' },
  { id: 'chatty', name: 'Chatty', emoji: '🗣️', blurb: 'Jokes, facts and banter on quiet stretches' },
];
export const MIXES = [
  { id: 'mix-drive', name: 'New voice each drive', emoji: '🎲', blurb: 'A surprise guest every trip' },
  { id: 'mix-line', name: 'Take turns', emoji: '🎭', blurb: 'The whole cast passes the mic' },
];

// ---------- who's talking ----------
let installedIds = [];
export async function refreshInstalled() {
  const all = await pack.cast();
  installedIds = [];
  for (const c of all) if (await pack.installed(c.id)) installedIds.push(c.id);
  return installedIds;
}
let driveVoice = null;
export function newDrive() {
  driveVoice = installedIds.length ? installedIds[Math.floor(Math.random() * installedIds.length)] : null;
}
let lastTurn = null;
function speaker() {
  if (talk.who === 'mix-drive') return driveVoice || installedIds[0] || null;
  if (talk.who === 'mix-line') {
    const pool = installedIds.filter((id) => id !== lastTurn);
    lastTurn = (pool.length ? pool : installedIds)[Math.floor(Math.random() * (pool.length || installedIds.length))] || null;
    return lastTurn;
  }
  return installedIds.includes(talk.who) ? talk.who : null;
}
/** True when a recorded voice is ready (otherwise the app falls back to the phone's voice). */
export const ready = () => !!(talk.who.startsWith('mix') ? installedIds.length : installedIds.includes(talk.who));

function line(keys, kind = 'event') {
  const id = speaker();
  return id ? pack.say(id, keys, { kind }) : false;
}

// ---------- land that isn't a crop ----------
const SPOT = new Map([
  ...[121, 122, 123, 124].map((c) => [c, 'town']), [111, 'water'], ...[141, 142, 143].map((c) => [c, 'woods']),
  [190, 'wetland'], [195, 'wetland'], [176, 'pasture'], [171, 'pasture'], [61, 'fallow'], [152, 'scrub'], [131, 'scrub'],
]);

// ---------- pacing ----------
const last = {};            // kind -> time it was last said
const since = (k) => Date.now() - (last[k] || 0);
const mark = (k) => { last[k] = Date.now(); };
const GAP = { normal: { extra: 7 * 60e3, spot: 4 * 60e3, flavor: 3 * 60e3 }, chatty: { extra: 3 * 60e3, spot: 2 * 60e3, flavor: 90e3 } };
const gap = (k) => (GAP[talk.chatty] || GAP.normal)[k];

// ---------- events from the app ----------
const sideKey = { left: 'left', right: 'right', here: 'around', point: 'around' };
const streak = {};          // side -> { code, since }

/** The crops beside the road changed. items: [{side, code}] for sides whose crop just changed. */
export function cropsChanged(items, isAg) {
  const now = Date.now();
  for (const it of items) streak[it.side] = { code: it.code, since: now };
  const crops = items.filter((it) => isAg(it.code) && !SPOT.has(it.code));
  const spots = items.filter((it) => SPOT.has(it.code));
  if (crops.length === 2 && crops[0].code === crops[1].code) {
    line([`crop:${crops[0].code}:both`], 'crop');
  } else if (crops.length) {
    line(crops.map((it) => `crop:${it.code}:${sideKey[it.side] || 'around'}`), 'crop');
  } else if (spots.length && talk.chatty !== 'crops' && since('spot') > gap('spot')) {
    if (line([`spot:${SPOT.get(spots[0].code)}`], 'extra')) mark('spot');
  }
  // Now and then, a little color about the crop we just met.
  if (crops.length && talk.chatty !== 'crops' && since('flavor') > gap('flavor') && Math.random() < 0.35) {
    setTimeout(() => { if (line([`flavor:${crops[0].code}`], 'extra')) mark('flavor'); }, 2500);
  }
}

/** Called every few seconds while driving with the current sides: long same-crop stretches get a quip. */
export function tick(sides) {
  if (talk.chatty === 'crops') return;
  const stretch = talk.chatty === 'chatty' ? 5 * 60e3 : 9 * 60e3;
  for (const [side, s] of Object.entries(sides)) {
    const st = streak[side];
    if (!st || st.code !== s.code) { streak[side] = { code: s.code, since: Date.now() }; continue; }
    if (Date.now() - st.since > stretch && since('streak') > stretch) {
      mark('streak'); st.since = Date.now();
      return line([`streak:${s.code}`], 'extra') || line(['streak'], 'extra');
    }
  }
  // Quiet stretch: a fact, a joke or some banter.
  if (pack.quietFor() > 90e3 && since('extra') > gap('extra')) {
    const code = sides.left?.code ?? sides.here?.code;
    const pool = talk.chatty === 'chatty' ? [`fact:${code}`, 'fact', 'joke', 'banter', 'banter'] : [`fact:${code}`, 'fact'];
    const k = pool[Math.floor(Math.random() * pool.length)];
    if (line([k], 'extra') || line(['fact'], 'extra')) mark('extra');
  }
}

// Each state's farm belt, said right after the welcome when you cross into a different belt.
const BELT_OF = { IA: 'corn', IL: 'corn', IN: 'corn', OH: 'corn', NE: 'corn', KS: 'wheat', OK: 'wheat', ND: 'spring', MT: 'spring',
  TX: 'cotton', MS: 'cotton', AL: 'cotton', GA: 'cotton', AR: 'rice', LA: 'rice', CA: 'fruit', FL: 'citrus', ID: 'potato', WA: 'palouse', MN: 'beets' };
const welcomed = lget('fs.welcomed', {});   // state -> day last welcomed (once a day per state)
let lastState = null;
export function enteredState(st) {
  if (!st || st === lastState) return;
  const prev = lastState;
  lastState = st;
  if (prev == null || talk.chatty === 'crops') return;   // no welcome for where the drive starts
  const day = new Date().toDateString();
  if (welcomed[st] === day) return;
  welcomed[st] = day; lput('fs.welcomed', welcomed);
  const keys = [`state:${st}`];
  if (BELT_OF[st] && BELT_OF[st] !== BELT_OF[prev]) keys.push(`belt:${BELT_OF[st]}`);
  line(keys);
}

export const driveStarted = () => {
  newDrive(); lastState = null;
  const h = new Date().getHours();
  line([h < 5 || h >= 21 ? 'start:night' : h < 12 ? 'start:morning' : h < 17 ? 'start:afternoon' : 'start:evening']);
};
export const driveEnded = (topCode) => line(topCode != null ? ['end', `recap:${topCode}`] : ['end']);
export const voiceOn = () => line(['hello']);
export const newCard = (code, rare) => line(rare ? ['rare', 'card', `name:${code}`] : ['card', `name:${code}`]);
export const badge = () => line(['badge']);
export const bingo = (full) => line([full ? 'bingo' : 'bingo:square'], full ? 'event' : 'extra');
export const milestone = (miles) => line([`miles:${miles}`]);
export const gps = (ok) => line([ok ? 'gps:back' : 'gps:lost'], 'extra');
export const preview = (id, keys) => pack.say(id, keys, { kind: 'event' });
export const hush = () => pack.hush();
