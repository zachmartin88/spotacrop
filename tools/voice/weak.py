# Find recorded lines that passed the Whisper check but still sound off: long dead air in the middle,
# an ending that's cut off, or a pace that's far too slow or too fast for the words.
#   weak.py [chars...]            report
#   weak.py --delete [chars...]   also delete them, so the next gen_lines.py run re-records them
import hashlib, json, os, re, sys
from pathlib import Path
import numpy as np

WORK = Path(os.path.expanduser('~/spotacrop-voices/lines'))
REFS = Path(os.path.expanduser('~/spotacrop-voices/refs'))

def _load(path):
    import librosa
    return librosa.load(str(path), sr=16000)

def defects(path, text):
    """[] if the clip sounds fine, else a list of short reasons."""
    import librosa
    y, sr = _load(path)
    if len(y) < sr * 0.3:
        return ['too short']
    dur = len(y) / sr
    out = []
    # Dead air: gaps between voiced stretches (pauses for "..." are fine up to about a second).
    spans = librosa.effects.split(y, top_db=38, frame_length=1024, hop_length=256)
    gaps = [(b0 - a1) / sr for (_, a1), (b0, _) in zip(spans[:-1], spans[1:])]
    allowed = 1.5 if ('...' in text or '[' in text or '?' in text.rstrip()[:-1]) else 0.95
    if gaps and max(gaps) > allowed:
        out.append(f'gap {max(gaps):.1f}s')
    # Cut off: the last 60 ms is still as loud as the speech itself.
    rms = librosa.feature.rms(y=y, frame_length=512, hop_length=128)[0]
    speech = np.median(rms[rms > np.max(rms) * 0.1]) if np.any(rms > np.max(rms) * 0.1) else 0
    tail = rms[-max(1, int(0.06 * sr / 128)):].mean()
    if speech and tail > speech * 0.7:
        out.append('cut off')
    # Pace: words per second, given how many words the line has.
    n = len(re.findall(r"[A-Za-z0-9']+", re.sub(r'\[[a-z ]+\]', '', text)))
    tags = len(re.findall(r'\[[a-z ]+\]', text))
    talk = max(0.3, dur - 0.6 * tags)
    wps = n / talk
    if n >= 3 and wps < 1.1:
        out.append(f'dragging {wps:.1f} w/s')
    if n >= 3 and wps > 5.8:
        out.append(f'rushed {wps:.1f} w/s')
    return out

if __name__ == '__main__':
    args = sys.argv[1:]
    delete = '--delete' in args
    chars = [a for a in args if not a.startswith('--')]
    sys.path.insert(0, str(Path(__file__).parent))
    from lines import build
    from cast import CAST
    lines = build(chars or list(CAST))
    report = {}
    for ch in chars or list(CAST):
        ref = REFS / f'{ch}.wav'
        if not ref.exists():
            continue
        sig = hashlib.sha1(ref.read_bytes()).hexdigest()[:8]
        seen, bad = set(), []
        for l in lines:
            if l['char'] != ch:
                continue
            i = hashlib.sha1(f"{sig}|{l['text']}".encode()).hexdigest()[:12]
            f = WORK / ch / f'{i}.m4a'
            if i in seen or not f.exists():
                continue
            seen.add(i)
            why = defects(f, l['text'])
            if why:
                bad.append({'key': l['key'], 'text': l['text'], 'why': why, 'file': str(f)})
                if delete:
                    f.unlink()
                    (WORK / ch / f'{i}.best').unlink(missing_ok=True)
        report[ch] = bad
        print(f'{ch}: {len(bad)} weak of {len(seen)}', flush=True)
        for b in bad[:6]:
            print('   ', b['why'], '|', b['text'])
    json.dump(report, open(WORK / 'weak.json', 'w'), indent=1)
