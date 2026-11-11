# -*- coding: utf-8 -*-
"""pausas reales de una frase (señal) frente a sus palabras: python …/pausas_frase.py frase [frase …]"""
import json
import os
import sys

import numpy as np
import soundfile as sf

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D)
from espaciar_voz import envolvente  # noqa: E402

pal = json.load(open(os.path.join(D, "voz", "palabras.json"), encoding="utf-8"))
for key in sys.argv[1:]:
    x, sr = sf.read(os.path.join(D, "voz", "final_orig", key + ".wav"), always_2d=True)
    env, hop, um = envolvente(x, sr)
    b = env < um
    tr, k = [], 0
    while k < len(b):
        if b[k]:
            f = k
            while f + 1 < len(b) and b[f + 1]:
                f += 1
            if (f - k + 1) * hop >= .05:
                tr.append((round(k * hop, 2), round((f + 1) * hop, 2)))
            k = f + 1
        else:
            k += 1
    p = pal[key]
    w = p.get("espaciado", p)["words"]
    print(key, f"dur {len(x) / sr:.2f} · umbral {um:.0f} dB · suelo {np.percentile(env, 5):.0f} dB · p90 {np.percentile(env, 90):.0f}")
    print("  pausas:", tr)
    print("  palabras:", " ".join(f"{q['w']}@{q['s']:.2f}-{q['e']:.2f}" for q in w))
