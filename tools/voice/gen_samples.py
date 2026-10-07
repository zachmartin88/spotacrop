# Make a short sample reel for each character, to judge the voices before recording everything.
#   ~/spotacrop-voices/.venv/bin/python tools/voice/gen_samples.py ~/spotacrop-voices/samples
import subprocess, sys, os, torch, soundfile as sf
from pathlib import Path
from cast import CAST

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SR = 24000

SAMPLES = {
    'earl': [
        "Well now [chuckle], would ya look at that. Corn on your left, far as the eye can see.",
        "Soybeans off to the right. Corn last year, beans this year. That's good farming.",
        "Welcome to Nebraska, partner. The Cornhusker State. Guess what they grow.",
        "Still corn. [sigh] I'd act surprised, but I'd be lyin'.",
        "Ooh, Christmas trees! Don't see many of those out here. That's a rare one.",
    ],
    'dot': [
        "Oh, sweetie, look! Corn on your left. [laugh] Isn't that lovely?",
        "Soybeans on the right, dear. Your grandpa used to grow those, you know.",
        "Welcome to Iowa, honey! Did you remember to pack a sweater?",
        "Oh my gourd, pumpkins! [laugh] Get it? Oh, I crack myself up.",
        "Corn again. Well, it's good for you, so I won't complain.",
    ],
    'buck': [
        "And on the left... it's corn! The crowd goes wild!",
        "Coming in hot on the right, it's soybeans, folks!",
        "Ladies and gentlemen, we have officially entered... the Corn Belt!",
        "A hundred miles of corn today! What a performance!",
        "Oh! A Christmas tree farm! You do not see that every day, folks!",
    ],
    'penny': [
        "Corn on your left! A-maize-ing, right? [laugh]",
        "Soybeans on the right! Bean there, done that!",
        "Lettuce celebrate, it's a brand new crop card!",
        "Oh my gourd, pumpkins! This is the best day ever!",
        "Still corn! Sorry, I know, that's a little corny.",
    ],
    'kernel': [
        "Whoa! Corn on the left! That's my family!",
        "Soybeans on the right! They're my buddies.",
        "Ooh ooh, a new crop card! Sunflowers! I love sunflowers!",
        "Are we there yet? [laugh] Just kidding. More corn!",
        "Hey, did you know one acre of corn has about twenty-five million kernels? That's a lot of cousins!",
    ],
    'sam': [
        "Corn on your left.",
        "Soybeans on your right. This field was corn last year.",
        "Welcome to Nebraska. Mostly corn and soybeans ahead.",
        "Iowa's corn harvest is about halfway done.",
        "Coming up: about ten miles of wheat.",
    ],
}

def ff(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def polish(src, dst):
    """Trim silence at both ends and even out the loudness."""
    ff('-i', str(src), '-af',
       'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,'
       'areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,'
       'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(SR), str(dst))

from kokoro import KPipeline
kp = KPipeline(lang_code='a')
def kokoro(text, voice, speed, path):
    parts = [torch.as_tensor(a) for _, _, a in kp(text, voice=voice, speed=speed)]
    sf.write(str(path), torch.cat(parts).numpy(), SR)

turbo = None
only = sys.argv[2:] or list(CAST)
for key in only:
    c = CAST[key]
    d = OUT / key; d.mkdir(exist_ok=True)
    if c['engine'] == 'turbo':
        ref_raw, ref = d / 'ref_raw.wav', d / 'ref.wav'
        kokoro(c['ref_text'], c['kokoro'], c['speed'], ref_raw)
        p = c['pitch']
        # Pitch via resample (changes speed too), then put the tempo back.
        ff('-i', str(ref_raw), '-af', f'asetrate={int(SR * p)},aresample={SR},atempo={1 / p:.4f}', str(ref))
        if turbo is None:
            from chatterbox.tts_turbo import ChatterboxTurboTTS
            turbo = ChatterboxTurboTTS.from_pretrained(device='mps' if torch.backends.mps.is_available() else 'cpu')
        turbo.prepare_conditionals(str(ref))
    clips = []
    for i, line in enumerate(SAMPLES[key]):
        raw, out = d / f'{i}_raw.wav', d / f'{i}.wav'
        if c['engine'] == 'turbo':
            wav = turbo.generate(line)
            sf.write(str(raw), wav.squeeze(0).cpu().numpy(), turbo.sr)
        else:
            kokoro(line.replace('[chuckle]', '').replace('[laugh]', '').replace('[sigh]', ''), c['kokoro'], c['speed'], raw)
        polish(raw, out)
        clips.append(out)
        print(key, i, 'done', flush=True)
    # One reel per character: the name, then each line with a short pause.
    lst = d / 'list.txt'
    gap = d / 'gap.wav'
    ff('-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.7', str(gap))
    lst.write_text(''.join(f"file '{p}'\nfile '{gap}'\n" for p in clips))
    ff('-f', 'concat', '-safe', '0', '-i', str(lst), '-c:a', 'aac', '-b:a', '96k', str(OUT / f"{c['emoji']} {c['name']} - {c['blurb']}.m4a"))
    print(key, 'reel ok', flush=True)
