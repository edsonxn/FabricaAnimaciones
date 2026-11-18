# -*- coding: utf-8 -*-
"""cada voz/final/<k>.wav debe durar lo que dice palabras.json y llevar exactamente los silencios de ESPACIOS_VOZ (nada duplicado)"""
import json
import os
import sys

import soundfile as sf

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D)
from guion import ESPACIOS_VOZ  # noqa: E402

pal = json.load(open(os.path.join(D, "voz", "palabras.json"), encoding="utf-8"))
malos = 0
for k, p in pal.items():
    d = sf.info(os.path.join(D, "voz", "final", k + ".wav")).duration
    if abs(d - p["dur"]) > .1:
        malos += 1
        print("NO CUADRA", k, round(d, 2), p["dur"])
for k, spec in ESPACIOS_VOZ.items():
    o = sf.info(os.path.join(D, "voz", "final_orig", k + ".wav")).duration
    d = sf.info(os.path.join(D, "voz", "final", k + ".wav")).duration
    if abs(d - o - sum(q[2] for q in spec)) > .1:
        malos += 1
        print("SILENCIOS MAL", k, round(d - o, 2), sum(q[2] for q in spec))
print(len(pal), "frases,", len(ESPACIOS_VOZ), "espaciadas,", malos, "problemas")
sys.exit(1 if malos else 0)
