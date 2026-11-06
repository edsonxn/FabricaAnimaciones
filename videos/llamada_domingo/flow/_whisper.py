# Whisper a clips: python flow/_whisper.py archivo1.mp4 ... -> texto por archivo (vad) en flow/_whisper.json
import sys, json, os
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cuda", compute_type="float16")
out = json.load(open("flow/_whisper.json", encoding="utf-8")) if os.path.exists("flow/_whisper.json") else {}
for f in sys.argv[1:]:
    segs, info = m.transcribe(f, language="es", vad_filter=True)
    t = [(round(s.start, 2), round(s.end, 2), s.text.strip()) for s in segs]
    out[os.path.basename(f)] = t
    print(os.path.basename(f), "|", " / ".join(f"{a}-{b} {x}" for a, b, x in t), flush=True)
json.dump(out, open("flow/_whisper.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
