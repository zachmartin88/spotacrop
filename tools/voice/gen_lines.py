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
        for l in mine:
            l['id'] = hashlib.sha1(f"{refsig}|{l['text']}".encode()).hexdigest()[:12]
            if not (d / f"{l['id']}.m4a").exists():
                todo.append(l)
        print(f'{ch}: {len(mine)} lines, {len(todo)} to record', flush=True)
        failed, t0 = [], time.time()
        for n, l in enumerate(todo, 1):
            ok = False
            for attempt in range(3):
                if attempt < 2:
                    w, sr = tb.generate(l['text'], temperature=0.85 if attempt == 0 else 0.7), tb.sr
                else:   # last try: the slower dramatic model, which garbles less
                    if cb is None:
                        cb = ChatterboxTTS.from_pretrained(device=DEV)
                    cb.prepare_conditionals(str(ref), exaggeration=c.get('exag', 0.8))
                    w, sr = cb.generate(spoken(l['text']), exaggeration=c.get('exag', 0.8), cfg_weight=0.4), cb.sr
                raw = d / 'tmp.wav'
                sf.write(str(raw), w.squeeze(0).cpu().numpy(), sr)
                out = d / f"{l['id']}.m4a"
                polish_to_m4a(raw, out)
                ok, score, heard = check(out, spoken(l['text']), need=0.8)
                if ok:
                    break
                out.unlink(missing_ok=True)
            if not ok:
                failed.append({**l, 'heard': heard, 'score': score})
            if n % 25 == 0 or n == len(todo):
                rate = (time.time() - t0) / n
                print(f'  {ch} {n}/{len(todo)}  {rate:.1f}s/line  ~{(len(todo) - n) * rate / 60:.0f} min left  failed {len(failed)}', flush=True)
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
