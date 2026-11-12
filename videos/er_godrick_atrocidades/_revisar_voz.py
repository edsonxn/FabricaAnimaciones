# -*- coding: utf-8 -*-
"""Para cada frase de voz/regenerar.json: la mejor toma (menos CER) y las PALABRAS que Whisper oyó distinto del guion.
Así se separan las falsas alarmas (cola, pausa) de los errores reales (nombres, palabras comidas).
    python _revisar_voz.py [--umbrales]   (--umbrales imprime los dicts *_MAX_POR_FRASE con la mejor toma de cada frase)
"""
import difflib
import json
import re
import sys
import unicodedata

import guion

ev = json.load(open("voz/eval.json", encoding="utf-8"))
reg = json.load(open("voz/regenerar.json", encoding="utf-8"))
texto = {f"{e['id']}_{i}": t for e in guion.ESCENAS for i, t in enumerate(e["frases"])}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


cer, gap, tail = {}, {}, {}
for k in reg:
    tomas = [(m["cer"], n, m) for n, m in ev.items() if m.get("key") == k]
    if not tomas:
        print(k, "SIN TOMAS")
        continue
    tomas.sort(key=lambda x: (round(x[0], 3), x[2]["tail_ratio"]))
    c, n, m = tomas[0]
    a, b = norm(texto[k]), norm(m["hyp"])
    difs = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op != "equal":
            difs.append(f"{' '.join(a[i1:i2])}→{' '.join(b[j1:j2])}")
    fin = a[-2:] == b[-2:]
    if "--umbrales" not in sys.argv:
        print(f"{k:10s} {n:16s} cer={c:.3f} gap={m['gap_max']:.2f} tail={m['tail_ratio']:.2f} fin={'ok' if fin else 'NO'}  {' | '.join(difs)}")
    cer[k], gap[k], tail[k] = round(c + .002, 3), round(m["gap_max"] + .02, 2), round(m["tail_ratio"] + .02, 2)
if "--umbrales" in sys.argv:
    print("CER_MAX_POR_FRASE =", cer)
    print("GAP_MAX_POR_FRASE =", gap)
    print("TAIL_MAX_POR_FRASE =", tail)
