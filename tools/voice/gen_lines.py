# Record every line for the chosen characters, check each one with Whisper (re-recording failures),
# and package each character into voice/<id>/pack.bin + index.json for the app.
#   ~/spotacrop-voices/.venv/bin/python tools/voice/gen_lines.py earl dot ...
# Re-runs are incremental: a line is only recorded if its text (or the character's reference) changed.
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
import soundfile as sf, torch
from cast import CAST
from lines import build
from qa import check

WORK = Path(os.path.expanduser('~/spotacrop-voices/lines'))
REFS = Path(os.path.expanduser('~/spotacrop-voices/refs'))
SITE = Path(__file__).resolve().parents[2] / 'voice'
SR = 24000
DEV = 'mps' if torch.backends.mps.is_available() else 'cpu'

def ff(*a):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)

def spoken(s):
    return re.sub(r'[\[<][a-z ]+[\]>]', '', s)

def polish_to_m4a(src, dst):
    ff('-i', str(src), '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,'
       'areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.15,areverse,'
       'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '24000', '-ac', '1', '-c:a', 'aac', '-b:a', '48k', '-movflags', '+faststart', str(dst))

def main(chars):
    from chatterbox.tts import ChatterboxTTS
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    tb = ChatterboxTurboTTS.from_pretrained(device=DEV)
    cb = None
    all_lines = build(chars)
    for ch in chars:
        c = CAST[ch]
        ref = REFS / f'{ch}.wav'
        if not ref.exists():
            sys.exit(f'no reference for {ch}: put the approved sample reference at {ref}')
        refsig = hashlib.sha1(ref.read_bytes()).hexdigest()[:8]
        d = WORK / ch; d.mkdir(parents=True, exist_ok=True)
        tb.prepare_conditionals(str(ref))
        mine = [l for l in all_lines if l['char'] == ch]
        todo = []
        seen = set()
        for l in mine:
            l['id'] = hashlib.sha1(f"{refsig}|{l['text']}".encode()).hexdigest()[:12]
            # The same text can appear under two moments; record it once (both keys share the clip).
            if l['id'] not in seen and not (d / f"{l['id']}.m4a").exists():
                todo.append(l)
            seen.add(l['id'])
        print(f'{ch}: {len(mine)} lines, {len(todo)} to record', flush=True)
        failed, t0 = [], time.time()
        # Record and check in parallel: Whisper checks one line (on the CPU) while the next records (on the GPU).
        from concurrent.futures import ThreadPoolExecutor
        pool, pending = ThreadPoolExecutor(max_workers=1), []   # one Whisper at a time (model load isn't thread-safe)
        def finish(job):
            l, tmp, out, attempt = job['l'], job['tmp'], job['out'], job['attempt']
            ok, score, heard = job['fut'].result()
            if ok:
                if tmp.exists(): tmp.rename(out)
                return None
            tmp.unlink(missing_ok=True)
            return {**l, 'heard': heard, 'score': score, 'attempt': attempt}
        def record(l, attempt):
            if attempt < 2:
                w, sr = tb.generate(l['text'], temperature=0.85 if attempt == 0 else 0.7), tb.sr
            else:   # last try: the slower dramatic model, which garbles less
                nonlocal_cb[0] = nonlocal_cb[0] or ChatterboxTTS.from_pretrained(device=DEV)
                m = nonlocal_cb[0]
                m.prepare_conditionals(str(ref), exaggeration=c.get('exag', 0.8))
                w, sr = m.generate(spoken(l['text']), exaggeration=c.get('exag', 0.8), cfg_weight=0.4), m.sr
            raw = d / f"raw_{l['id']}.wav"
            sf.write(str(raw), w.squeeze(0).cpu().numpy(), sr)
            tmp = d / f"tmp_{l['id']}.m4a"
            polish_to_m4a(raw, tmp); raw.unlink(missing_ok=True)
            return {'l': l, 'tmp': tmp, 'out': d / f"{l['id']}.m4a", 'attempt': attempt,
                    'fut': pool.submit(check, tmp, spoken(l['text']), 0.8)}
        nonlocal_cb = [cb]
        queue = [(l, 0) for l in todo]
        done = 0
        while queue or pending:
            if queue:
                l, attempt = queue.pop(0)
                pending.append(record(l, attempt))
            while pending and (pending[0]['fut'].done() or not queue):
                bad = finish(pending.pop(0))
                if bad is None:
                    done += 1
                elif bad['attempt'] < 2:
                    if bad['attempt'] == 1:
                        tb.prepare_conditionals(str(ref))
                    queue.append((bad, bad['attempt'] + 1))
                else:
                    failed.append(bad); done += 1
                if done and done % 25 == 0:
                    rate = (time.time() - t0) / done
                    print(f'  {ch} {done}/{len(todo)}  {rate:.1f}s/line  ~{(len(todo) - done) * rate / 60:.0f} min left  failed {len(failed)}', flush=True)
        cb = nonlocal_cb[0]
        print(f'  {ch} done: {len(todo) - len(failed)} recorded, {len(failed)} failed after 3 tries, {(time.time() - t0) / 60:.0f} min', flush=True)
        json.dump(failed, open(d / 'failed.json', 'w'), indent=1)
        pack(ch, mine, d)

def pack(ch, mine, d):
    out = SITE / ch; out.mkdir(parents=True, exist_ok=True)
    keys, blob = {}, bytearray()
    for l in mine:
        f = d / f"{l['id']}.m4a"
        if not f.exists():
            continue
        b = f.read_bytes()
        keys.setdefault(l['key'], []).append([len(blob), len(b)])
        blob += b
    version = hashlib.sha1(bytes(blob)).hexdigest()[:10]
    (out / 'pack.bin').write_bytes(bytes(blob))
    json.dump({'id': ch, 'version': version, 'bytes': len(blob), 'keys': keys}, open(out / 'index.json', 'w'), separators=(',', ':'))
    c = CAST[ch]
    castf = SITE / 'cast.json'
    cast = json.load(open(castf)) if castf.exists() else {'cast': []}
    cast['cast'] = [x for x in cast['cast'] if x['id'] != ch] + [{
        'id': ch, 'name': c['name'], 'emoji': c['emoji'], 'blurb': c['blurb'], 'version': version,
        'mb': round(len(blob) / 1e6, 1), 'lines': sum(len(v) for v in keys.values()),
    }]
    order = list(CAST)
    cast['cast'].sort(key=lambda x: order.index(x['id']) if x['id'] in order else 99)
    json.dump(cast, open(castf, 'w'), indent=1, ensure_ascii=False)
    print(f'{ch}: packed {len(blob) / 1e6:.1f} MB, {sum(len(v) for v in keys.values())} lines, {len(keys)} moments', flush=True)

if __name__ == '__main__':
    main(sys.argv[1:] or list(CAST))
