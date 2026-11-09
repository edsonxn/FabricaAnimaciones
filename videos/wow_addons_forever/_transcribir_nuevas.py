# -*- coding: utf-8 -*-
"""Transcribe las grabaciones nuevas del 8-nov (Spoken vs el add-on propio) con tiempos, para elegir tramos de >= 5 s."""
import json
import os
from faster_whisper import WhisperModel

D = r"E:\videos grabados"
F = ["2026-11-08 20-48-41", "spoken1", "spoken2", "spoken3", "miaddon1", "miaddon3", "miaddon4", "miaddon5"]
m = WhisperModel("small", device="cuda", compute_type="float16")
out = {}
for f in F:
    segs, _ = m.transcribe(os.path.join(D, f + ".mp4"), language="es", vad_filter=True)
    out[f] = [(round(s.start, 1), round(s.end, 1), s.text.strip()) for s in segs]
    print(f"== {f}")
    for a, b, t in out[f]:
        print(f"  {a:5.1f}-{b:5.1f} {t}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_nuevas_whisper.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
