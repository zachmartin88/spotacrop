# Round 2 samples: more personality. For each character:
#   1. Kokoro stock voice reads the reference text (neutral).
#   2. Original Chatterbox re-performs it with high exaggeration -> a hammier reference.
#   3. Lines are made two ways from that reference: A = Turbo (fast, [laugh] tags), B = original Chatterbox
#      with the exaggeration dial. Both are scored for expressiveness (pitch range, loudness swing)
#      and checked with Whisper; the livelier passing take wins.
#   ~/spotacrop-voices/.venv/bin/python tools/voice/gen_samples2.py ~/spotacrop-voices/samples2 [chars...]
import subprocess, sys, json, re, numpy as np, torch, soundfile as sf, librosa
from pathlib import Path
from cast import CAST
from qa import check

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SR = 24000
DEV = 'mps' if torch.backends.mps.is_available() else 'cpu'

# exaggeration / cfg for the dramatic reference and for method B. Lower cfg = slower, more deliberate.
ACT = {
    'earl':   {'exag': 0.85, 'cfg': 0.3, 'tempo': 0.94},
    'dot':    {'exag': 0.95, 'cfg': 0.35, 'tempo': 0.96},
    'buck':   {'exag': 1.35, 'cfg': 0.45, 'tempo': 1.0},
    'penny':  {'exag': 1.25, 'cfg': 0.45, 'tempo': 1.0},
    'kernel': {'exag': 1.3, 'cfg': 0.45, 'tempo': 1.0},
}
REF_TEXT = {
    'earl': "Well now... I been farming this ground for forty-some years. Heh. Corn, beans, little hay for the cows. "
            "Ain't nothing fancy. But I'll tell ya what... there's no prettier sight in this whole world than a field of corn at sunset. Mm-hm.",
    'dot': "Oh, honey! Come here, come here, sit down! I just made a pie. Rhubarb! Your favorite! Oh, I'm so happy you're here. "
           "Now tell me everything. Did you see the sunflowers? Oh, I just love, love, love the sunflowers this time of year!",
    'buck': "Ladies and gentlemen! Boys and girls! Welcome... to the biggest! Show! In the whole entire county! Are you ready?! "
            "I can't hear you! Let's make some noise for our next rider, coming out of chute number three! Yeehaw!",
    'penny': "Oh my gosh, okay, okay, okay, I have the best joke ever, you are going to love this so much. "
             "Why did the tomato blush? Because it saw the salad dressing! Ha! Get it?! I'm hilarious! I know! I know!",
    'kernel': "Hi hi hi! I'm Kernel! Are we going on a road trip?! Can I sit in the front?! Ooh, ooh, look, a tractor! "
              "I love tractors so, so much! Are we there yet? Just kidding! But... are we?",
}
LINES = {
    'earl': [
        "Well now... [chuckle] would ya look at that. Corn on your left. Far as the eye can see, and then some.",
        "Soybeans off to the right. Corn last year, beans this year. Mm. That's good farming, right there.",
        "Welcome to Nebraska, partner. The Cornhusker State. [chuckle] Now... guess what they grow.",
        "Still corn. [sigh] Yep. I'd act surprised... but I'd be lying.",
        "Whoa, whoa, whoa. Christmas trees? Out here? Well, I'll be darned. That's a rare one.",
    ],
    'dot': [
        "Oh, sweetie! Look, look, corn on your left! [laugh] Isn't that just lovely?",
        "Soybeans on the right, dear. You know, your grandpa used to grow those. Oh, he loved his beans.",
        "Welcome to Iowa, honey! Now, did you remember to pack a sweater? It gets chilly!",
        "Oh my gourd, pumpkins! [laugh] Get it? Oh, I just crack myself up.",
        "Corn again? Well... it's good for you, so I won't complain. Much.",
    ],
    'buck': [
        "And on the left... it's corn! Corn, corn, corn! The crowd goes wild!",
        "Ladies and gentlemen, coming in hot on the right... it's soybeans! What a comeback!",
        "Ohhh, folks! We have officially entered... the Corn Belt! Hold on to your hats!",
        "A hundred miles of corn today! A hundred miles! What a performance! Let's hear it!",
        "Wait, wait, wait! Is that... a Christmas tree farm? You do not see that every day, folks!",
    ],
    'penny': [
        "Corn on your left! A-maize-ing, right? [laugh] Okay, okay, I'll stop. No I won't!",
        "Soybeans on the right! Bean there, done that! Ha! I'm so good at this.",
        "Ooh! Ooh! New crop card! Lettuce celebrate! Get it? Lettuce? Let us? Okay.",
        "Oh my gourd, pumpkins! Pumpkins! This is literally the best day ever!",
        "Still corn! Sorry, I know, I know, that's a little corny. [laugh]",
    ],
    'kernel': [
        "Whoa whoa whoa! Corn on the left! That's my family! Hi, Grandma! Hi, Uncle Cob!",
        "Soybeans on the right! They're my buddies! Hi, buddies!",
        "Ooh, ooh, ooh! New crop card! Sunflowers! I love sunflowers so much!",
        "Are we there yet? Are we there yet? [laugh] Just kidding! More corn!",
        "Hey! Hey! Did you know one acre of corn has about twenty-five million kernels? That's a lot of cousins!",
    ],
}

def ff(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def polish(src, dst, tempo=1.0):
    t = f'atempo={tempo},' if abs(tempo - 1) > 0.01 else ''
    ff('-i', str(src), '-af', f'{t}silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,'
       'areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,'
       'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(SR), str(dst))

def liveliness(path):
    """Pitch range (semitones, std of voiced F0) and loudness swing (dB std). Flat voices score low."""
    y, sr = librosa.load(str(path), sr=16000)
    f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=600, sr=sr)
    f0 = f0[voiced & ~np.isnan(f0)]
    pitch = float(np.std(12 * np.log2(f0 / np.median(f0)))) if len(f0) > 10 else 0.0
    rms = librosa.feature.rms(y=y)[0]
    loud = float(np.std(20 * np.log10(rms[rms > 1e-4] + 1e-9)))
    return round(pitch, 2), round(loud, 2)

def no_tags(s):
    s = s.replace('[laugh]', 'Ha ha!').replace('[chuckle]', 'Heh.').replace('[sigh]', 'Hmm.')
    return re.sub(r'\[[a-z ]+\]', '', s)

from kokoro import KPipeline
kp = KPipeline(lang_code='a')
from chatterbox.tts import ChatterboxTTS
from chatterbox.tts_turbo import ChatterboxTurboTTS
cb = ChatterboxTTS.from_pretrained(device=DEV)
tb = ChatterboxTurboTTS.from_pretrained(device=DEV)

report = {}
for key in (sys.argv[2:] or list(ACT)):
    c, a = CAST[key], ACT[key]
    d = OUT / key; d.mkdir(exist_ok=True)
    # 1. neutral stock read, pitched for the character
    raw = d / 'ref_kokoro_raw.wav'
    parts = [torch.as_tensor(x) for _, _, x in kp(REF_TEXT[key].replace('...', ','), voice=c['kokoro'], speed=c['speed'])]
    sf.write(str(raw), torch.cat(parts).numpy(), SR)
    neutral = d / 'ref_kokoro.wav'
    p = c['pitch']
    ff('-i', str(raw), '-af', f'asetrate={int(SR * p)},aresample={SR},atempo={1 / p:.4f}', str(neutral))
    # 2. hammed-up reference
    cb.prepare_conditionals(str(neutral), exaggeration=a['exag'])
    wav = cb.generate(no_tags(REF_TEXT[key]), exaggeration=a['exag'], cfg_weight=a['cfg'])
    hammy = d / 'ref_hammy.wav'
    sf.write(str(hammy), wav.squeeze(0).cpu().numpy(), cb.sr)
    print(key, 'ref', liveliness(neutral), '->', liveliness(hammy), flush=True)
    # 3. lines, two ways
    tb.prepare_conditionals(str(hammy))
    cb.prepare_conditionals(str(hammy), exaggeration=a['exag'])
    picks, rows = [], []
    for i, line in enumerate(LINES[key]):
        takes = {}
        w = tb.generate(line, temperature=0.9)
        sf.write(str(d / f'{i}_A_raw.wav'), w.squeeze(0).cpu().numpy(), tb.sr)
        polish(d / f'{i}_A_raw.wav', d / f'{i}_A.wav', a['tempo'])
        w = cb.generate(no_tags(line), exaggeration=a['exag'], cfg_weight=a['cfg'])
        sf.write(str(d / f'{i}_B_raw.wav'), w.squeeze(0).cpu().numpy(), cb.sr)
        polish(d / f'{i}_B_raw.wav', d / f'{i}_B.wav', a['tempo'])
        for m in 'AB':
            ok, s, heard = check(d / f'{i}_{m}.wav', line if m == 'A' else no_tags(line), need=0.75)
            pr, ld = liveliness(d / f'{i}_{m}.wav')
            takes[m] = {'ok': ok, 'score': s, 'pitch': pr, 'loud': ld, 'heard': heard}
        good = [m for m in 'AB' if takes[m]['ok']] or ['A', 'B']
        best = max(good, key=lambda m: takes[m]['pitch'] + 0.5 * takes[m]['loud'])
        picks.append(d / f'{i}_{best}.wav')
        rows.append({'line': line, 'pick': best, **{m: takes[m] for m in 'AB'}})
        print(key, i, 'A', takes['A']['pitch'], takes['A']['ok'], '| B', takes['B']['pitch'], takes['B']['ok'], '-> ', best, flush=True)
    report[key] = rows
    gap = d / 'gap.wav'
    ff('-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.7', str(gap))
    (d / 'list.txt').write_text(''.join(f"file '{p}'\nfile '{gap}'\n" for p in picks))
    ff('-f', 'concat', '-safe', '0', '-i', str(d / 'list.txt'), '-c:a', 'aac', '-b:a', '96k', str(OUT / f"{c['emoji']} {c['name']} v2 - more intensity.m4a"))
    print(key, 'reel ok', flush=True)
    json.dump(report, open(OUT / 'report.json', 'w'), indent=1)
