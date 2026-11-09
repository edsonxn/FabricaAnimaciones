import os
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cuda", compute_type="float16")
for f in ["spoken1", "miaddon1", "spoken3", "miaddon3"]:
    segs, _ = m.transcribe(os.path.join(r"E:\videos grabados", f + ".mp4"), language="es", word_timestamps=True)
    ws = [w for s in segs for w in s.words if w.start < 14]
    print(f, " ".join(f"{w.word.strip()}[{w.start:.1f}-{w.end:.1f}]" for w in ws))
