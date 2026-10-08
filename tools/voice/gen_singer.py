# Sample reel for the singing character: Turbo speaks each line in Cole's voice, then songify.py sings it.
#   ~/spotacrop-voices/.venv/bin/python tools/voice/gen_singer.py ~/spotacrop-voices/sing
import sys, re, subprocess, torch, soundfile as sf
from pathlib import Path
from cast import CAST
from songify import songify

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SR = 24000
LINES = [
    "Corn on the left, corn on the right, corn as far as the eye can see!",
    "Soybeans, soybeans, growing in a row!",
    "We're rolling through the Corn Belt! Yee haw!",
    "Oh my gourd, it's pumpkins, pumpkins everywhere!",
    "Still corn, still corn, it's always, always corn!",
]
def ff(*a): subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)
c = CAST['cole']; d = OUT / 'cole'; d.mkdir(exist_ok=True)
from kokoro import KPipeline
kp = KPipeline(lang_code='a')
parts = [torch.as_tensor(x) for _, _, x in kp(c['ref'], voice=c['voice'], speed=c['speed'])]
sf.write(str(d / 'ref_raw.wav'), torch.cat(parts).numpy(), SR)
from chatterbox.tts import ChatterboxTTS
from chatterbox.tts_turbo import ChatterboxTurboTTS
dev = 'mps' if torch.backends.mps.is_available() else 'cpu'
cb = ChatterboxTTS.from_pretrained(device=dev)
cb.prepare_conditionals(str(d / 'ref_raw.wav'), exaggeration=c['exag'])
w = cb.generate(c['ref'], exaggeration=c['exag'], cfg_weight=0.4)
sf.write(str(d / 'ref.wav'), w.squeeze(0).cpu().numpy(), cb.sr)
tb = ChatterboxTurboTTS.from_pretrained(device=dev)
tb.prepare_conditionals(str(d / 'ref.wav'))
outs = []
for i, line in enumerate(LINES):
    w = tb.generate(line, temperature=0.7)
    sf.write(str(d / f'{i}_spoken.wav'), w.squeeze(0).cpu().numpy(), tb.sr)
    songify(d / f'{i}_spoken.wav', d / f'{i}_sung.wav', tune=i, low=True, seed=i)
    outs.append(d / f'{i}_sung.wav'); print('cole', i, 'sung', flush=True)
gap = d / 'gap.wav'; ff('-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.6', str(gap))
(d / 'list.txt').write_text(''.join(f"file '{p}'\nfile '{gap}'\n" for p in outs))
ff('-f', 'concat', '-safe', '0', '-i', str(d / 'list.txt'), '-af', 'loudnorm=I=-16:TP=-1.5', '-c:a', 'aac', '-b:a', '128k', str(OUT / '🎸 Cole - Auto-Tune singer.m4a'))
print('cole reel ok', flush=True)
