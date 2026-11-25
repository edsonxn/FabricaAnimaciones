# -*- coding: utf-8 -*-
"""Transcribe la voz del reel (palabras con tiempo) -> fuente/palabras.json"""
import json, subprocess
from pathlib import Path
from faster_whisper import WhisperModel

AQUI = Path(__file__).parent
SRC = AQUI / "fuente" / "orig.mp4"
wav = AQUI / "fuente" / "voz.wav"
if not wav.exists():
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-ac", "1", "-ar", "16000", str(wav)], check=True)
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True, vad_filter=False)
pal, frases = [], []
for s in segs:
    frases.append(dict(t0=round(s.start, 2), t1=round(s.end, 2), texto=s.text.strip()))
    for w in s.words:
        pal.append(dict(t0=round(w.start, 2), t1=round(w.end, 2), w=w.word.strip()))
(AQUI / "fuente" / "palabras.json").write_text(json.dumps(dict(frases=frases, palabras=pal), ensure_ascii=False, indent=1), encoding="utf-8")
with open(AQUI / "fuente" / "frases.txt", "w", encoding="utf-8") as f:
    for fr in frases:
        f.write(f"{fr['t0']:6.2f}-{fr['t1']:6.2f}  {fr['texto']}\n")
print(len(frases), "frases")
