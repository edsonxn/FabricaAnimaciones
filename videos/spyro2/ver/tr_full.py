import sys, io
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cuda", compute_type="float16")
seg, info = m.transcribe("mxp_audio.m4a", language="en", vad_filter=True, beam_size=3, condition_on_previous_text=False)
with open("tr_full.txt","w",encoding="utf-8") as o:
    for s in seg:
        o.write(f"[{s.start:8.1f} - {s.end:8.1f}] {s.text.strip()}\n"); o.flush()
print("FIN")
