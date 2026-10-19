// First-launch walkthrough: three quick swipeable screens, skippable, replayable from the menu.
import { KERNEL_SVG, fx } from './fun.js';

const KEY = 'fs.onboarded';
export const onboarded = () => { try { return localStorage.getItem(KEY) === '1'; } catch { return true; } };
const done = () => { try { localStorage.setItem(KEY, '1'); } catch { /* fine */ } };

const tile = (bg, e) => `<i style="background:${bg}">${e}</i>`;
const STEPS = [
  {
    art: `<div class="ob-kernel">${KERNEL_SVG}</div><div class="ob-patch">${[
      ['#ffc928', '🌽'], ['#22c55e', '🫘'], ['#fb7a24', '🌾'], ['#ffc928', '🌽'], ['#a78bfa', '🌿'], ['#22c55e', '🫘'],
    ].map(([b, e]) => tile(b, e)).join('')}</div>`,
    title: 'Hi! I’m Kernel 🌽',
    text: 'See what’s growing in any field in the lower 48, from <b>this season’s satellite map</b>.',
  },
  {
    art: `<div class="ob-strip"><div><small>◂ LEFT</small><b><i style="background:#ffc928">🌽</i>Corn</b><em>LIVE</em></div><div><small>RIGHT ▸</small><b><i style="background:#22c55e">🫘</i>Soybeans</b><em>LIVE</em></div></div>
      <div class="ob-cast">${[['🤠', 'Earl'], ['👵', 'Dot'], ['📣', 'Buck'], ['🌽', 'Kernel'], ['🎩', 'Nigel']].map(([e, n], i) => `<span style="--i:${i}"><i>${e}</i>${n}</span>`).join('')}</div>`,
    title: 'Drive and listen',
    text: 'Tap <b>Start driving</b>. A co-pilot calls out the crops, so your eyes stay on the road.',
  },
  {
    art: `<div class="ob-cards">${[['#ffc928', '🌽'], ['#38bdf8', '🍚'], ['#d946ef', '🍇']].map(([b, e], i) => `<i style="background:${b};--r:${(i - 1) * 9}deg">${e}</i>`).join('')}</div>
      <div class="ob-games"><span>🃏 Cards</span><span>🎯 Bingo</span><span>🏅 Badges</span></div>`,
    title: 'Tap, collect, share',
    text: '<b>Tap any field</b> for its story, and collect a card for every crop you pass.',
    last: true,
  },
];

export function showOnboarding({ onDone } = {}) {
  let i = 0;
  const el = document.createElement('div');
  el.className = 'onboard';
  el.innerHTML = `<div class="ob-card-wrap" role="dialog" aria-label="How Spot-a-Crop works">
      <button class="ob-skip">Skip</button>
      <div class="ob-stage"></div>
      <div class="ob-dots">${STEPS.map(() => '<i></i>').join('')}</div>
      <div class="ob-nav"><button class="ghost ob-back">Back</button><button class="primary ob-next">Next</button></div>
    </div>`;
  document.body.appendChild(el);
  const stage = el.querySelector('.ob-stage'), next = el.querySelector('.ob-next'), back = el.querySelector('.ob-back');

  function render(dir = 1) {
    const s = STEPS[i];
    stage.innerHTML = `<div class="ob-step ${dir > 0 ? 'in-right' : 'in-left'}"><div class="ob-art">${s.art}</div><h2>${s.title}</h2><p>${s.text}</p></div>`;
    el.querySelectorAll('.ob-dots i').forEach((d, k) => d.classList.toggle('on', k === i));
    back.style.visibility = i ? 'visible' : 'hidden';
    next.textContent = s.last ? 'Let’s go! 🚜' : 'Next';
  }
  function close() {
    done();
    el.classList.add('out');
    setTimeout(() => el.remove(), 300);
    onDone?.();
  }
  next.addEventListener('click', () => { fx('flip'); if (STEPS[i].last) close(); else { i++; render(1); } });
  back.addEventListener('click', () => { if (i) { i--; render(-1); } });
  el.querySelector('.ob-skip').addEventListener('click', close);
  // Swipe left/right.
  let x0 = null;
  stage.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', (e) => {
    if (x0 == null) return;
    const dx = e.changedTouches[0].clientX - x0;
    x0 = null;
    if (dx < -50 && !STEPS[i].last) { i++; render(1); } else if (dx > 50 && i) { i--; render(-1); }
  });
  document.addEventListener('keydown', function key(e) {
    if (!el.isConnected) return document.removeEventListener('keydown', key);
    if (e.key === 'ArrowRight') next.click(); else if (e.key === 'ArrowLeft') back.click(); else if (e.key === 'Escape') close();
  });
  render();
}
