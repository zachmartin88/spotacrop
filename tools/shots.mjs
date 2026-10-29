// App Store screenshots (6.9", 1320×2868) from the web build, driven through headless Chrome (muted, no installs needed).
//   node tools/shots.mjs [base url]      (default http://localhost:5179/)  -> store/screenshots-6.9/N.jpg
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const BASE = process.argv[2] || 'http://localhost:5179/';
const OUT = path.join(ROOT, 'store/screenshots-6.9');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const prof = fs.mkdtempSync('/tmp/sac-shots-');
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`, '--mute-audio',
  '--no-first-run', '--hide-scrollbars', '--window-size=440,956', 'about:blank'], { stdio: 'ignore' });

let ws, id = 0;
const pending = new Map();
function send(method, params = {}) {
  return new Promise((res, rej) => {
    const i = ++id;
    pending.set(i, { res, rej });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
}
async function js(expr) {
  const r = await send('Runtime.evaluate', { expression: `(async () => { ${expr} })()`, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result.value;
}

// An iPhone status bar and home indicator, so the shots look like the app on a phone.
const CHROME_JS = `
  document.documentElement.style.setProperty('--safe-top', '62px');
  document.documentElement.style.setProperty('--safe-bottom', '30px');
  if (!document.getElementById('shotCss')) { const st = document.createElement('style'); st.id = 'shotCss'; st.textContent = '.leaflet-tractors-pane{display:none}'; document.head.appendChild(st); }
  if (!document.getElementById('fakeStatus')) {
    const s = document.createElement('div');
    s.id = 'fakeStatus';
    s.style.cssText = 'position:fixed;left:0;right:0;top:0;height:54px;z-index:99999;display:flex;align-items:center;justify-content:space-between;padding:6px 34px 0 52px;color:#fff;font:600 17px -apple-system,system-ui;pointer-events:none;text-shadow:0 1px 2px rgba(0,0,0,.4)';
    s.innerHTML = '<span>9:41</span><span style="display:flex;gap:7px;align-items:center">'
      + '<svg width="19" height="12" viewBox="0 0 19 12"><rect x="0" y="8" width="3" height="4" rx="1" fill="#fff"/><rect x="5" y="5.5" width="3" height="6.5" rx="1" fill="#fff"/><rect x="10" y="3" width="3" height="9" rx="1" fill="#fff"/><rect x="15" y="0" width="3" height="12" rx="1" fill="#fff"/></svg>'
      + '<svg width="17" height="12" viewBox="0 0 17 12"><path d="M8.5 2.5c2.4 0 4.6.9 6.2 2.4l1.2-1.2C13.9 1.8 11.3.8 8.5.8S3.1 1.8 1.1 3.7l1.2 1.2C3.9 3.4 6.1 2.5 8.5 2.5zm0 3.4c1.5 0 2.8.5 3.8 1.4l1.2-1.2c-1.3-1.2-3.1-1.9-5-1.9s-3.7.7-5 1.9l1.2 1.2c1-.9 2.3-1.4 3.8-1.4zm0 3.4c.6 0 1.1.2 1.5.6L8.5 11.4 7 9.9c.4-.4.9-.6 1.5-.6z" fill="#fff"/></svg>'
      + '<svg width="27" height="13" viewBox="0 0 27 13"><rect x=".5" y=".5" width="23" height="12" rx="3.5" stroke="#fff" stroke-opacity=".5" fill="none"/><rect x="2" y="2" width="20" height="9" rx="2" fill="#fff"/><rect x="24.5" y="4.5" width="1.5" height="4" rx=".7" fill="#fff" fill-opacity=".5"/></svg></span>';
    document.body.appendChild(s);
    const h = document.createElement('div');
    h.style.cssText = 'position:fixed;left:50%;bottom:8px;width:140px;height:5px;margin-left:-70px;border-radius:3px;background:rgba(255,255,255,.75);z-index:99999;pointer-events:none';
    document.body.appendChild(h);
  }
  dispatchEvent(new Event('resize'));
`;

async function shot(n) {
  await js(CHROME_JS);
  await sleep(600);
  const { data } = await send('Page.captureScreenshot', { format: 'jpeg', quality: 92, captureBeyondViewport: false });
  fs.writeFileSync(path.join(OUT, `${n}.jpg`), Buffer.from(data, 'base64'));
  console.log('shot', n);
}
async function load(q = '?sim') {
  await send('Page.navigate', { url: BASE + q });
  await sleep(4500);
}
const tapAt = (x, y) => js(`const el = document.elementFromPoint(${x}, ${y}); const o = {bubbles:true, clientX:${x}, clientY:${y}, view:window};
  for (const t of ['pointerdown','mousedown','pointerup','mouseup','click']) el.dispatchEvent(new (t.startsWith('pointer') ? PointerEvent : MouseEvent)(t, o)); return el.className;`);

try {
  let tabs;
  for (let i = 0; i < 40 && !tabs; i++) { await sleep(250); tabs = await fetch(`http://127.0.0.1:${PORT}/json`).then((r) => r.json()).catch(() => null); }
  const page = tabs.find((t) => t.type === 'page');
  ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((r) => { ws.onopen = r; });
  ws.onmessage = (m) => { const d = JSON.parse(m.data); const p = pending.get(d.id); if (p) { pending.delete(d.id); d.error ? p.rej(new Error(d.error.message)) : p.res(d.result); } };
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 440, height: 956, deviceScaleFactor: 3, mobile: true });
  await send('Emulation.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
  await send('Emulation.setGeolocationOverride', { latitude: 42.05, longitude: -93.75, accuracy: 10 });
  await send('Browser.grantPermissions', { permissions: ['geolocation'] }).catch(() => {});

  // First visit: skip the walkthrough, download Earl, voice on.
  await load('');
  await js(`localStorage.setItem('fs.onboarded','1'); localStorage.setItem('fs.voice','1'); localStorage.setItem('fs.talkWho', JSON.stringify('earl'));
    const vp = await import('/voicepack.js'); await vp.install('earl'); await vp.install('dot'); return 'ok';`);

  // 4. The U.S. map with the farm belts (start screen card hidden)
  await load('?sim');
  await js(`document.getElementById('welcome').hidden = true; document.body.classList.remove('welcoming'); return 1;`);
  await sleep(1500);
  await shot(4);

  // 1. Driving, with Earl calling the crops
  await load('?sim');
  await js(`document.getElementById('startBtn').click(); return 1;`);
  await sleep(26000);   // let the simulated drive reach mixed fields
  await shot(1);

  // 6. The drive recap
  await sleep(90000);
  await js(`document.getElementById('dbEnd').click(); return 1;`);
  await sleep(2500);
  await shot(6);

  // 3. A tapped field: history and harvest progress
  await js(`document.querySelector('[aria-label=Close], .sheet .close')?.click(); return 1;`);
  await sleep(800);
  await tapAt(70, 300);
  await sleep(6000);
  await shot(3);

  // 2. The voice cast
  await js(`document.querySelector('[aria-label=Close], .sheet .close')?.click(); return 1;`);
  await sleep(600);
  await js(`document.getElementById('menuBtn').click(); await new Promise(r => setTimeout(r, 600)); document.querySelector('[data-act=voice]').click(); return 1;`);
  await sleep(2500);
  await shot(2);

  // 5. Road-trip bingo
  await js(`document.getElementById('menuBtn').click(); await new Promise(r => setTimeout(r, 600)); document.querySelector('[data-act=bingo]').click(); return 1;`);
  await sleep(2500);
  await shot(5);
} catch (e) {
  console.error(e);
} finally {
  chrome.kill();
  fs.rmSync(prof, { recursive: true, force: true });
}
