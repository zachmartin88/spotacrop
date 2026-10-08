# "Songify": turn a spoken line into a sung one, Auto-Tune style, with a banjo underneath.
# Words are timed with Whisper, each word is stretched onto a beat and its pitch snapped to a note
# (with vibrato and little slides between notes), then re-synthesized with the WORLD vocoder.
import numpy as np, pyworld as pw, soundfile as sf, librosa

SR = 24000
# G major pentatonic, around a comfortable singing range (Hz). Lower set for deep voices.
SCALE_HI = [196.0, 220.0, 246.9, 293.7, 329.6, 392.0, 440.0]
SCALE_LO = [98.0, 110.0, 123.5, 146.8, 164.8, 196.0, 220.0]
# Melodies as scale steps (0..6); the last note gets held. Picked by word count.
TUNES = [
    [2, 2, 3, 4, 4, 3, 2, 1, 2, 0],
    [0, 2, 4, 4, 5, 4, 2, 3, 2, 0],
    [4, 4, 3, 2, 3, 4, 4, 4, 3, 3, 4, 3, 2],
    [0, 0, 2, 4, 2, 0, 1, 2, 1, 0],
]

_wm = None
def words(path):
    global _wm
    if _wm is None:
        from faster_whisper import WhisperModel
        _wm = WhisperModel('small.en', device='cpu', compute_type='int8')
    segs, _ = _wm.transcribe(str(path), language='en', word_timestamps=True)
    return [(w.start, w.end, w.word.strip()) for s in segs for w in s.words]

def pluck(freq, dur, sr=SR, decay=0.993, vol=0.18):
    n = max(2, int(sr / freq)); out = np.zeros(int(sr * dur), np.float32)
    ring = np.random.uniform(-1, 1, n).astype(np.float32); j = 0
    for i in range(len(out)):
        k = (j + 1) % n; v = ring[j]; out[i] = v; ring[j] = decay * 0.5 * (v + ring[k]); j = k
    return out * vol

def songify(src, dst, tune=0, beat=0.36, low=False, seed=0):
    rng = np.random.default_rng(seed)
    x, sr = sf.read(str(src))
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = librosa.resample(x, orig_sr=sr, target_sr=SR)
    x = x.astype(np.float64)
    ws = words(src)
    if not ws: raise ValueError('no words heard')
    scale = SCALE_LO if low else SCALE_HI
    melody = TUNES[tune % len(TUNES)]
    period = 5.0  # ms
    f0, t = pw.harvest(x, SR, frame_period=period)
    sp = pw.cheaptrick(x, f0, t, SR); ap = pw.d4c(x, f0, t, SR)
    fr = lambda s: int(round(s * 1000 / period))
    out_f0, out_sp, out_ap, notes = [], [], [], []
    for i, (a, b, w) in enumerate(ws):
        last = i == len(ws) - 1
        lo, hi = fr(a), max(fr(b), fr(a) + 2)
        seg = slice(lo, min(hi, len(f0)))
        n_src = seg.stop - seg.start
        if n_src <= 1: continue
        target = beat * (2.2 if last else (1.0 if len(w) > 3 else 0.7))
        n_out = max(2, fr(target))
        idx = np.linspace(seg.start, seg.stop - 1, n_out).round().astype(int)
        note = scale[melody[min(i, len(melody) - 1)] if i < len(melody) - 1 else melody[-1]]
        if last: note = scale[0] if melody[-1] == 0 else scale[melody[-1]]
        tt = np.arange(n_out) * period / 1000
        vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * tt) * np.clip(tt / 0.2, 0, 1)     # vibrato fades in
        glide = np.ones(n_out)
        if notes:   # quick slide from the previous note
            k = min(n_out, fr(0.05)); glide[:k] = np.linspace(notes[-1] / note, 1, k)
        nf0 = note * vib * glide * (f0[idx] > 0)
        out_f0.append(nf0); out_sp.append(sp[idx]); out_ap.append(ap[idx]); notes.append(note)
        gap = fr(0.04 if not last else 0.0)   # tiny breath between words
        if gap:
            out_f0.append(np.zeros(gap)); out_sp.append(np.repeat(sp[idx[-1:]], gap, 0)); out_ap.append(np.repeat(np.ones_like(ap[idx[-1:]]), gap, 0))
    F0 = np.concatenate(out_f0); SP = np.ascontiguousarray(np.concatenate(out_sp)); AP = np.ascontiguousarray(np.concatenate(out_ap))
    y = pw.synthesize(F0, SP, AP, SR, frame_period=period)
    # Banjo: a plucked note on each beat, following the melody's root, plus a final chord.
    dur = len(y) / SR
    band = np.zeros(len(y) + SR, np.float32)
    beats = int(dur / beat) + 1
    roots = [scale[0] / 2, scale[3] / 2, scale[4] / 2, scale[0] / 2]
    for k in range(beats):
        f = roots[(k // 4) % len(roots)] * (1 if k % 2 == 0 else 1.5)
        p = pluck(f, beat * 2, vol=0.10 if k % 2 else 0.14)
        s = int(k * beat * SR); band[s:s + len(p)] += p[: len(band) - s]
    for f in (scale[0], scale[2], scale[4]):
        p = pluck(f, 1.2, vol=0.09); s = max(0, len(y) - int(0.3 * SR)); band[s:s + len(p)] += p[: len(band) - s]
    mix = np.zeros(len(band), np.float32); mix[:len(y)] += (y / (np.abs(y).max() + 1e-9) * 0.8).astype(np.float32)
    mix += band
    mix /= np.abs(mix).max() + 1e-9
    sf.write(str(dst), mix * 0.9, SR)
    return dst

if __name__ == '__main__':
    import sys
    songify(sys.argv[1], sys.argv[2], tune=int(sys.argv[3]) if len(sys.argv) > 3 else 0)
