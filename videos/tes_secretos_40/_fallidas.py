# -*- coding: utf-8 -*-
"""Lista las frases de voz/regenerar.json con su mejor toma (CER, pausa, cola) y lo que oyó Whisper."""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
e = json.load(open(os.path.join(AQUI, "voz", "eval.json"), encoding="utf-8"))
r = json.load(open(os.path.join(AQUI, "voz", "regenerar.json"), encoding="utf-8"))
sys.stdout.reconfigure(encoding="utf-8")
for k in r:
    ts = sorted([v for v in e.values() if v["key"] == k], key=lambda v: v["cer"])
    b = ts[0]
    print(f"{k:9} cer={b['cer']:.3f} gap={b['gap_max']:.2f} tail={b['tail_ratio']:.2f} dur={b['dur']:.1f} | {b['hyp'][:170]}")
