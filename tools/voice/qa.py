# Listen back to recorded lines with Whisper and flag any that don't say what the script says.
# Used by gen_lines.py; also runnable on a folder:  qa.py <clips.json>
import re, sys, json
from difflib import SequenceMatcher

_model = None
def model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel('small.en', device='cpu', compute_type='int8')
    return _model

NUM = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
       'ten': '10', 'twenty': '20', 'fifty': '50', 'hundred': '100'}

def words(s):
    s = re.sub(r'\[[a-z ]+\]', ' ', s.lower())          # acting tags aren't spoken
    s = s.replace("'", '').replace('’', '').replace('-', ' ')
    w = re.findall(r'[a-z0-9]+', s)
    return [NUM.get(x, x) for x in w]

def transcribe(path):
    segs, _ = model().transcribe(str(path), language='en', beam_size=3, vad_filter=False)
    return ' '.join(s.text for s in segs).strip()

def score(expected, heard):
    """0..1 similarity of the word sequences."""
    a, b = words(expected), words(heard)
    if not a: return 1.0
    return SequenceMatcher(None, a, b).ratio()

def check(path, expected, need=0.8):
    heard = transcribe(path)
    s = score(expected, heard)
    return s >= need, round(s, 2), heard

if __name__ == '__main__':
    for item in json.load(open(sys.argv[1])):
        ok, s, heard = check(item['path'], item['text'])
        print('OK ' if ok else 'BAD', s, '|', item['text'], '|', heard)
