# -*- coding: utf-8 -*-
"""Pista de voz sola (sin música ni ambiente) para VISTAS PREVIAS: cada toma de voz/final en su t0 del timeline.
Uso: python _voz_previa.py [t_ini t_fin] -> audio/voz_previa.wav (el MASTER usa `mezcla`, no esto)."""
import json
import sys

import numpy as np
import soundfile as sf

t = json.load(open("timeline.json", encoding="utf-8"))
a, b = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else (0.0, t["total"])
SR = 48000
pista = np.zeros(int((b - a) * SR) + SR, dtype=np.float32)
for e in t["escenas"]:
    for f in e["frases"]:
        if f["t1"] < a or f["t0"] > b:
            continue
        x, sr = sf.read(f"voz/final/{f['key']}.wav", dtype="float32", always_2d=True)
        x = x.mean(axis=1)
        if sr != SR:
            x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x).astype(np.float32)
        # la toma arranca con su propio silencio inicial: se alinea por su primera palabra (t0) con un margen fijo
        i = int((f["t0"] - a) * SR)
        if i < 0:
            x, i = x[-i:], 0
        n = min(len(x), len(pista) - i)
        pista[i:i + n] += x[:n]
pista /= max(1.0, float(np.abs(pista).max()) / 0.9)
sf.write("audio/voz_previa.wav", pista[: int((b - a) * SR)], SR)
print(f"audio/voz_previa.wav  {a:.0f}-{b:.0f} s")
