# Can Bark (Suno, MIT) sing our lines? Several takes per lyric and voice, scored for
# (a) lyrics heard correctly (Whisper) and (b) how "sung" it is: share of voiced audio holding a steady note.
#   ~/spotacrop-voices/.venv/bin/python tools/voice/sing_bark.py ~/spotacrop-voices/sing
import sys, json, numpy as np, torch, soundfile as sf, librosa
from pathlib import Path
from qa import check

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
LYRICS = [
    "♪ Corn on the left, corn on the right, corn as far as the eye can see ♪",
    "♪ Soybeans, soybeans, growing in a row ♪",
    "♪ We're rolling through the Corn Belt, yee haw ♪",
]
VOICES = ['v2/en_speaker_6', 'v2/en_speaker_9']
TAKES = 2

def sunginess(path):
    y, sr = librosa.load(str(path), sr=16000)
    f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=700, sr=sr, frame_length=1024, hop_length=160)
    st = 12 * np.log2(np.where(voiced, f0, np.nan) / 100)
    win, steady, total = 10, 0, 0   # 100 ms windows
    for i in range(0, len(st) - win, win):
        w = st[i:i + win]
        if np.sum(~np.isnan(w)) >= win * 0.8:
            total += 1
            if np.nanstd(w) < 0.35: steady += 1
    return round(steady / total, 2) if total else 0.0

from transformers import AutoProcessor, BarkModel
dev = 'cpu'   # Bark hits an MPS dtype bug in generate()
proc = AutoProcessor.from_pretrained('suno/bark')
model = BarkModel.from_pretrained('suno/bark').to(dev)
sr = model.generation_config.sample_rate
results = []
for v in VOICES:
    for li, lyric in enumerate(LYRICS):
        for t in range(TAKES):
            inputs = proc(lyric, voice_preset=v).to(dev)
            with torch.inference_mode():
                audio = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()
            p = OUT / f"{v.split('/')[-1]}_{li}_{t}.wav"
            sf.write(str(p), audio, sr)
            ok, score, heard = check(p, lyric.replace('♪', ''), need=0.6)
            s = sunginess(p)
            results.append({'file': p.name, 'voice': v, 'lyric': li, 'words': score, 'sung': s, 'heard': heard})
            print(p.name, 'words', score, 'sung', s, '|', heard, flush=True)
json.dump(results, open(OUT / 'bark.json', 'w'), indent=1)
