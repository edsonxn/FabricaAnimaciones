# -*- coding: utf-8 -*-
"""Transcribe la voz del reel base (palabras con tiempo) → fuente/palabras.json + hoja de cuadros."""
import json, subprocess, sys
from pathlib import Path
from faster_whisper import WhisperModel

AQUI = Path(__file__).parent
SRC = AQUI / "fuente" / "fugu.mp4"
wav = AQUI / "fuente" / "voz.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-ac", "1", "-ar", "16000", str(wav)], check=True)
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True, vad_filter=False)
pal, frases = [], []
for s in segs:
    frases.append(dict(t0=round(s.start, 2), t1=round(s.end, 2), texto=s.text.strip()))
    for w in s.words:
        pal.append(dict(t0=round(w.start, 2), t1=round(w.end, 2), w=w.word.strip()))
(AQUI / "fuente" / "palabras.json").write_text(json.dumps(dict(frases=frases, palabras=pal), ensure_ascii=False, indent=1), encoding="utf-8")
for f in frases:
    print(f"{f['t0']:6.2f}-{f['t1']:6.2f}  {f['texto']}")
# hoja de cuadros 4x3 cada ~4 s
prev = AQUI / "previews"; prev.mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-vf", "fps=1/4,scale=270:480,tile=6x2", "-frames:v", "1", str(prev / "fuente_hoja.jpg")], check=True)
