# Round 3 samples: natural base voices (Orpheus) for references, 11 characters, A/B takes scored for liveliness.
#   ~/spotacrop-voices/.venv/bin/python tools/voice/gen_samples3.py ~/spotacrop-voices/samples3 [chars...]
import subprocess, sys, json, re, numpy as np, torch, soundfile as sf, librosa
from pathlib import Path
from cast import CAST
from qa import check
import orpheus

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SR = 24000
DEV = 'mps' if torch.backends.mps.is_available() else 'cpu'

LINES = {
    'earl': [
        "Well, I'll be. [chuckle] Corn on your left, far as the eye can see. Y'all ain't never seen corn like that.",
        "Soybeans off to the right. Corn last year, beans this year. That's just good farming, is what that is.",
        "Welcome to Nebraska, partner. The Cornhusker State. Now, I reckon you can guess what they grow.",
        "Still corn. [sigh] Yep. I'd act surprised, but I'd be lying to ya.",
        "Whoa, whoa, whoa. Christmas trees? Out here? Well, I'll be darned. Ain't that something.",
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
        "Hey! Did you know one acre of corn has about twenty-five million kernels? That's a lot of cousins!",
    ],
    'sam': [
        "Corn on your left.",
        "Soybeans on your right. This field was corn last year.",
        "Welcome to Nebraska. Mostly corn and soybeans ahead.",
        "Iowa's corn harvest is about halfway done.",
        "Coming up: about ten miles of wheat.",
    ],
    'nigel': [
        "And here... on the left... the corn. Magnificent. Standing perfectly still, as corn so often does.",
        "On the right, a herd of soybeans. Watch closely. They are... doing absolutely nothing.",
        "We have now entered the Corn Belt. Few have returned to tell of its... corn.",
        "Remarkable. A Christmas tree farm. So rarely glimpsed in the wild.",
        "Still corn. The corn, it seems, has no natural predators.",
    ],
    'brody': [
        "Duuude. Corn on the left. Totally gnarly, bro.",
        "Whoa, soybeans on the right. That's, like, so chill.",
        "We're in the Corn Belt, dude. Endless corn. Like an endless summer, but... corn.",
        "Pumpkins! Radical! Pumpkin spice, bro! Pumpkin spice!",
        "Still corn, man. Just riding the corn wave. [laugh] Cowabunga.",
    ],
    'hank': [
        "Corn on the left! Look at that form! Textbook!",
        "Soybeans on the right! You call that a crop? Yes! Yes I do! Great hustle!",
        "We are in the Corn Belt! No crying in the Corn Belt! Let's go, let's go!",
        "A hundred miles! Hit the showers! Just kidding, keep driving!",
        "Still corn! Dig deep! Corn doesn't quit, and neither do you!",
    ],
    'rye': [
        "Corn. On the left. Tall, golden... and hiding something.",
        "Soybeans on the right. Quiet types. [sigh] Too quiet.",
        "The Corn Belt. A place where every field has a secret. And the secret... is corn.",
        "Christmas trees? Out here? Something doesn't add up. That's a rare one, kid.",
        "Still corn. It was always corn. I should've known.",
    ],
    'delphine': [
        "Corn! On the left! [gasp] I simply cannot believe it!",
        "Soybeans... on the right. After everything we've been through? How dare they be so lovely.",
        "The Corn Belt. [sigh] At last, darling. At last.",
        "Pumpkins! [gasp] Oh, it's all too much! I need to sit down. I am sitting down.",
        "Still corn. It's always corn. Story of my life, darling.",
    ],
}

def ff(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def polish(src, dst):
    ff('-i', str(src), '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,'
       'areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,'
       'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(SR), str(dst))

def pitch(src, dst, p):
    if abs(p - 1) < 0.005:
        ff('-i', str(src), str(dst)); return
    ff('-i', str(src), '-af', f'asetrate={int(SR * p)},aresample={SR},atempo={1 / p:.4f}', str(dst))

def liveliness(path):
    y, sr = librosa.load(str(path), sr=16000)
    f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=600, sr=sr)
    f0 = f0[voiced & ~np.isnan(f0)]
    pr = float(np.std(12 * np.log2(f0 / np.median(f0)))) if len(f0) > 10 else 0.0
    rms = librosa.feature.rms(y=y)[0]
    return round(pr, 2), round(float(np.std(20 * np.log10(rms[rms > 1e-4] + 1e-9))), 2)

def spoken(s):   # what Whisper should hear
    return re.sub(r'[\[<][a-z ]+[\]>]', '', s)

from kokoro import KPipeline
kp = KPipeline(lang_code='a')
kpb = KPipeline(lang_code='b')   # British English
from chatterbox.tts import ChatterboxTTS
from chatterbox.tts_turbo import ChatterboxTurboTTS
cb = ChatterboxTTS.from_pretrained(device=DEV)
tb = ChatterboxTurboTTS.from_pretrained(device=DEV)

report = {}
for key in (sys.argv[2:] or list(CAST)):
    c = CAST[key]
    d = OUT / key; d.mkdir(exist_ok=True)
    raw = d / 'ref_raw.wav'
    if c['base'] == 'orpheus':
        for attempt in range(3):   # Orpheus occasionally returns nothing usable
            a = orpheus.speak(c['ref'], c['voice'], temperature=0.7)
            if a is not None and len(a) > SR * 5: break
        sf.write(str(raw), a, SR)
    else:
        pipe = kpb if c['voice'].startswith('b') else kp
        parts = [torch.as_tensor(x) for _, _, x in pipe(re.sub(r'<[a-z]+>', '', c['ref']), voice=c['voice'], speed=c.get('speed', 1))]
        sf.write(str(raw), torch.cat(parts).numpy(), SR)
    ref = d / 'ref.wav'
    pitch(raw, ref, c.get('pitch', 1))
    if c['base'] == 'kokoro':   # ham it up first
        cb.prepare_conditionals(str(ref), exaggeration=c['exag'])
        w = cb.generate(spoken(c['ref']), exaggeration=c['exag'], cfg_weight=0.4)
        ref = d / 'ref_hammy.wav'
        sf.write(str(ref), w.squeeze(0).cpu().numpy(), cb.sr)
    print(key, 'ref', liveliness(ref), flush=True)
    tb.prepare_conditionals(str(ref))
    exag = c.get('exag', 0.8)
    cb.prepare_conditionals(str(ref), exaggeration=exag)
    picks, rows = [], []
    for i, line in enumerate(LINES[key]):
        takes = {}
        w = tb.generate(line, temperature=0.85)
        sf.write(str(d / f'{i}_A_raw.wav'), w.squeeze(0).cpu().numpy(), tb.sr); polish(d / f'{i}_A_raw.wav', d / f'{i}_A.wav')
        w = cb.generate(spoken(line), exaggeration=exag, cfg_weight=0.4)
        sf.write(str(d / f'{i}_B_raw.wav'), w.squeeze(0).cpu().numpy(), cb.sr); polish(d / f'{i}_B_raw.wav', d / f'{i}_B.wav')
        for m in 'AB':
            ok, s, heard = check(d / f'{i}_{m}.wav', spoken(line), need=0.75)
            pr, ld = liveliness(d / f'{i}_{m}.wav')
            takes[m] = {'ok': ok, 'score': s, 'pitch': pr, 'loud': ld, 'heard': heard}
        good = [m for m in 'AB' if takes[m]['ok']] or ['A', 'B']
        best = max(good, key=lambda m: takes[m]['pitch'] + 0.5 * takes[m]['loud'])
        picks.append(d / f'{i}_{best}.wav')
        rows.append({'line': line, 'pick': best, **takes})
        print(key, i, 'A', takes['A']['pitch'], takes['A']['ok'], '| B', takes['B']['pitch'], takes['B']['ok'], '->', best, flush=True)
    report[key] = rows
    gap = d / 'gap.wav'
    ff('-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.7', str(gap))
    (d / 'list.txt').write_text(''.join(f"file '{p}'\nfile '{gap}'\n" for p in picks))
    ff('-f', 'concat', '-safe', '0', '-i', str(d / 'list.txt'), '-c:a', 'aac', '-b:a', '96k', str(OUT / f"{c['emoji']} {c['name']} - {c['blurb']}.m4a"))
    print(key, 'reel ok', flush=True)
    json.dump(report, open(OUT / f'report_{key}.json', 'w'), indent=1)
