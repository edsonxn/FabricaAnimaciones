# tr.py <archivo> [offset_s]  -> imprime segmentos con tiempo
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from faster_whisper import WhisperModel
f = sys.argv[1]; off = float(sys.argv[2]) if len(sys.argv)>2 else 0
try:
    m = WhisperModel("small", device="cuda", compute_type="float16")
except Exception as e:
    m = WhisperModel("small", device="cpu", compute_type="int8")
seg, info = m.transcribe(f, language="en", word_timestamps=False, vad_filter=False, beam_size=5)
for s in seg:
    print(f"[{s.start+off:8.1f} - {s.end+off:8.1f}] {s.text.strip()}")
