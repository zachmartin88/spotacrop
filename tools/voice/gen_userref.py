# Sample reels from a person's own reference recording (no stock base voice): 5 lines, best of two takes each.
#   gen_userref.py <out dir> <char>=<ref.wav> ...
import sys, re, subprocess, numpy as np, torch, soundfile as sf
from pathlib import Path
from qa import check

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
DEV = 'mps' if torch.backends.mps.is_available() else 'cpu'
LINES = {
    'cornbeard': ["Arr, corn off the port bow! That's your left, matey!", "Soybeans to starboard! Starboard be right, landlubber.",
                  "Ahoy, Iowa! The Hawkeye State! Iowa grows more corn than any other state. Arr!", "A rare treasure! Rarer than gold doubloons!",
                  "Still corn! A whole ocean of it! [laugh]"],
    'earl': ["Well, I'll be. [chuckle] Corn on your left, far as the eye can see.", "Soybeans off to the right. Corn last year, beans this year. That's just good farmin'.",
             "Well, welcome to Nebraska, partner. The Cornhusker State. Now, I reckon you can guess what they grow.",
             "Still corn. [sigh] Yep. I'd act surprised, but I'd be lyin' to ya.", "Whoa, whoa. Christmas trees? Out here? Well, I'll be darned."],
    'auntie': ["Ooh, look at that corn on the left, darlin'! Tall and proud!", "Soybeans on the right! Mm-hmm, nice and green.",
               "Sugarcane! [laugh] Just like back home, darlin'!", "Welcome to Georgia, sweetheart! They grow peanuts here, you know.",
               "Slow down, nah! The corn not goin' anywhere!"],
}
def spoken(s): return re.sub(r'\[[a-z ]+\]', '', s)
def ff(*a): subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)
def polish(src, dst):
    ff('-i', str(src), '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,'
       'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '24000', str(dst))
def lively(p):
    import librosa
    y, sr = librosa.load(str(p), sr=16000)
    f0, v, _ = librosa.pyin(y, fmin=70, fmax=600, sr=sr); f0 = f0[v & ~np.isnan(f0)]
    return float(np.std(12 * np.log2(f0 / np.median(f0)))) if len(f0) > 10 else 0.0

import os
MODEL = os.environ.get('MODEL', 'turbo')
if MODEL == 'turbo':
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    tb = ChatterboxTurboTTS.from_pretrained(device=DEV)
else:   # the original Chatterbox: slower, more faithful to the reference, with an exaggeration dial
    from chatterbox.tts import ChatterboxTTS
    tb = ChatterboxTTS.from_pretrained(device=DEV)
EXAG = float(os.environ.get('EXAG', '0.6'))
for arg in sys.argv[2:]:
    ch, ref = arg.split('=')
    d = OUT / ch; d.mkdir(exist_ok=True)
    tb.prepare_conditionals(ref) if MODEL == 'turbo' else tb.prepare_conditionals(ref, exaggeration=EXAG)
    picks = []
    for i, line in enumerate(LINES[ch]):
        best = None
        for k, temp in enumerate((0.8, 0.9)):
            w = tb.generate(line, temperature=temp) if MODEL == 'turbo' else tb.generate(spoken(line), exaggeration=EXAG, cfg_weight=0.35 + 0.15 * k, temperature=temp)
            raw = d / f'{i}_{k}_raw.wav'; sf.write(str(raw), w.squeeze(0).cpu().numpy(), tb.sr)
            out = d / f'{i}_{k}.wav'; polish(raw, out)
            ok, sc, heard = check(out, spoken(line), 0.75)
            score = (ok, lively(out))
            print(ch, i, k, ok, sc, '|', heard, flush=True)
            if best is None or score > best[0]: best = (score, out)
        picks.append(best[1])
    gap = d / 'gap.wav'
    ff('-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.7', str(gap))
    (d / 'list.txt').write_text(''.join(f"file '{p}'\nfile '{gap}'\n" for p in picks))
    ff('-f', 'concat', '-safe', '0', '-i', str(d / 'list.txt'), '-c:a', 'aac', '-b:a', '96k', str(OUT / f'{ch}-your-voice{"" if MODEL == "turbo" else "-v2"}.m4a'))
    print(ch, 'reel ok', flush=True)
