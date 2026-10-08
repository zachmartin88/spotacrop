# Orpheus TTS (Canopy Labs, Apache-2.0; built on Llama 3.2) running locally through llama.cpp on Metal,
# decoded with SNAC (MIT). Natural voices with built-in <laugh> <chuckle> <sigh> <gasp> <groan> <yawn> tags.
# Voices: tara, leah, jess, mia, zoe (female) · leo, dan, zac (male).
import glob, os, numpy as np, torch

GGUF = glob.glob(os.path.expanduser('~/.cache/huggingface/hub/models--lex-au--Orpheus-3b-FT-Q8_0.gguf/snapshots/*/Orpheus-3b-FT-Q8_0.gguf'))[0]
SR = 24000
START, EOT, END_HUMAN, START_SPEECH, END_SPEECH, AUDIO0 = 128259, 128009, 128260, 128257, 128258, 128266

_llm = _snac = None
def _load():
    global _llm, _snac
    if _llm is None:
        from llama_cpp import Llama
        _llm = Llama(model_path=GGUF, n_ctx=4096, n_gpu_layers=-1, verbose=False)
        from snac import SNAC
        _snac = SNAC.from_pretrained('hubertsiuzdak/snac_24khz').eval()

def speak(text, voice='tara', temperature=0.6, top_p=0.95, repeat_penalty=1.1, max_tokens=1600):
    """Returns float32 mono audio at 24 kHz, or None if the model produced nothing usable."""
    _load()
    ids = [START] + _llm.tokenize(f'{voice}: {text}'.encode(), add_bos=True, special=False) + [EOT, END_HUMAN]
    out = []
    for tok in _llm.generate(ids, temp=temperature, top_p=top_p, repeat_penalty=repeat_penalty, reset=True):
        if tok == END_SPEECH or tok == EOT or len(out) >= max_tokens:
            break
        out.append(tok)
    if START_SPEECH in out:
        out = out[len(out) - out[::-1].index(START_SPEECH):]
    codes = [t - AUDIO0 for t in out if t >= AUDIO0]
    codes = codes[: len(codes) // 7 * 7]
    if not codes:
        return None
    l1, l2, l3 = [], [], []
    for i in range(len(codes) // 7):
        c = codes[7 * i: 7 * i + 7]
        l1.append(c[0])
        l2.append(c[1] - 4096)
        l3.append(c[2] - 2 * 4096)
        l3.append(c[3] - 3 * 4096)
        l2.append(c[4] - 4 * 4096)
        l3.append(c[5] - 5 * 4096)
        l3.append(c[6] - 6 * 4096)
    if min(l1 + l2 + l3) < 0 or max(l1 + l2 + l3) > 4095:
        return None   # garbled frame layout; caller retries
    with torch.inference_mode():
        audio = _snac.decode([torch.tensor(l, dtype=torch.long).unsqueeze(0) for l in (l1, l2, l3)])
    return audio.squeeze().numpy().astype(np.float32)

if __name__ == '__main__':
    import sys, time, soundfile as sf
    out = sys.argv[1]
    for v in ['tara', 'leah', 'jess', 'mia', 'zoe', 'leo', 'dan', 'zac']:
        t = time.time()
        a = speak("Well now <chuckle>, would you look at that. Corn on your left, as far as the eye can see!", v)
        sf.write(f'{out}/orpheus_{v}.wav', a, SR)
        print(v, round(time.time() - t, 1), 's for', round(len(a) / SR, 1), 's', flush=True)
