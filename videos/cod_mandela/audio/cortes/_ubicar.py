# -*- coding: utf-8 -*-
"""Ubica con Whisper (palabras con tiempo) las frases que la voz anuncia y que se tienen que OÍR (regla 31-oct-2026).
    python _ubicar.py            imprime cada palabra con su segundo dentro de cada ventana
"""
import subprocess

import numpy as np
from faster_whisper import WhisperModel

SR = 16000
# id: (desde, hasta) segundos de la ventana a transcribir
VENTANAS = {
    "mv88YFoq2rc": (46, 62),     # Shepherd: «Good. That's one less loose end.»
    "ijssTVhflBc": (80, 100),    # MacMillan: «I think I saw his arm fly off.»
    "YzK11dTXbrQ": (40, 56),     # interrogador: «The numbers, Mason. What do they mean?»
    "KEWwsYGC0HY": (170, 420),   # Foley: gritos de «Ramirez!»
    "NRIkSSmXJMk": (0, 31),      # jingle de Juggernog
    "bH1lHCirCGI": (28, 48),     # tráiler MW2019: «Bravo Six, going dark.»
}


def leer(id_, a, b):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", id_ + ".wav", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)


wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
for id_, (a, b) in VENTANAS.items():
    segs, _ = wm.transcribe(leer(id_, a, b), language="en", word_timestamps=True, vad_filter=False)
    print(f"== {id_}")
    for s in segs:
        print("   " + " ".join(f"{w.word.strip()}@{a + w.start:.2f}" for w in s.words))
