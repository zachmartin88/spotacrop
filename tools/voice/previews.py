# A few seconds of each character (their hello, then a corn call), shipped inside the app and the website,
# so people can hear the whole cast before downloading anyone.  Writes previews/<id>.m4a + previews/index.json.
import json, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VOICE, OUT = ROOT / 'voice', ROOT / 'previews'

def ff(*a):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)

def main():
    OUT.mkdir(exist_ok=True)
    cast = json.load(open(VOICE / 'cast.json'))['cast']
    idx_path = OUT / 'index.json'
    have = json.load(open(idx_path)) if idx_path.exists() else {}
    for c in cast:
        ch = c['id']
        if have.get(ch) == c['version'] and (OUT / f'{ch}.m4a').exists():
            continue
        index = json.load(open(VOICE / ch / 'index.json'))
        blob = (VOICE / ch / 'pack.bin').read_bytes()
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            parts = []
            for key in ('hello', 'crop:1:left'):
                if index['keys'].get(key):
                    off, n = index['keys'][key][0]
                    m = t / f'{len(parts)}.m4a'
                    m.write_bytes(blob[off:off + n])
                    p = t / f'{len(parts)}.wav'
                    ff('-i', str(m), '-ar', '24000', '-ac', '1', str(p))
                    parts.append(p)
            ff('-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.35', str(t / 'gap.wav'))
            seq = []
            for p in parts:
                seq += [p, t / 'gap.wav']
            (t / 'list.txt').write_text(''.join(f"file '{p}'\n" for p in seq[:-1]))
            ff('-f', 'concat', '-safe', '0', '-i', str(t / 'list.txt'), '-c:a', 'aac_at', '-b:a', '32k', '-ac', '1', '-ar', '24000',
               '-movflags', '+faststart', str(OUT / f'{ch}.m4a'))
        have[ch] = c['version']
        print(ch, 'preview', (OUT / f'{ch}.m4a').stat().st_size // 1024, 'KB')
    json.dump(have, open(idx_path, 'w'), indent=1)

if __name__ == '__main__':
    main()
