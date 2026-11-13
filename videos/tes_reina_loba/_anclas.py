# -*- coding: utf-8 -*-
"""Anclas ambiguas de efectos.py: las que la voz dice VARIAS veces y cuya 1.ª vez cae lejos de donde va el FX
(comparado con el FX anterior en el orden del archivo). Imprime la sugerencia «#N».
    python _anclas.py        (desde la carpeta del video)
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
_norm = lambda w: re.sub(r"[\W_]+", "", w.lower())
tl = json.load(open("timeline.json", encoding="utf-8"))
pal = [(_norm(w["w"]), w["s"], w["e"]) for e in tl["escenas"] for fr in e["frases"] for w in fr["words"]]
pal = [p for p in pal if p[0]]


def veces(txt):
    m = re.fullmatch(r"(.*?)(?:#(\d+))?(\|fin)?", txt, re.S)
    ag = [w for w in (_norm(w) for w in m.group(1).split()) if w]
    out = [pal[i][1] for i in range(len(pal) - len(ag) + 1) if all(pal[i + j][0] == ag[j] for j in range(len(ag)))]
    return out, int(m.group(2) or 0)


def anclas(d):
    for k in ("en", "de", "a"):
        if k in d:
            x = d[k]
            yield k, x[0] if isinstance(x, (tuple, list)) else x
    for m in d.get("marcas", []):
        yield "marca", m[0] if isinstance(m, (tuple, list)) else m


from PIL import Image as _I  # noqa: E402
_open = _I.open
_I.open = lambda f, *a, **k: _open(f if not isinstance(f, str) or os.path.exists(f) else os.path.join(AQUI, "pegatinas", "soledad.png"), *a, **k)
import efectos  # noqa: E402

prev = 0.0
malas = 0
for n, d in enumerate(efectos.FX):
    ts = []
    for k, x in anclas(d):
        if not isinstance(x, str) or x.startswith("scene-"):
            continue
        occ, fij = veces(x)
        if not occ:
            print(f"FX{n} {d.get('nombre', '')}: NO SE DICE «{x}»")
            malas += 1
            continue
        if fij:
            ts.append(occ[fij - 1])
            continue
        if len(occ) > 1:
            # la vez más cercana DESPUÉS del FX anterior (con 20 s de tolerancia hacia atrás)
            mejor = min(range(len(occ)), key=lambda i: abs(occ[i] - prev) if occ[i] >= prev - 20 else 1e9)
            if mejor != 0:
                print(f"FX{n} {d.get('nombre', '')[:40]} [{k}] «{x}» → usar #{mejor + 1} ({occ[0]:.0f}s → {occ[mejor]:.0f}s)")
                malas += 1
            ts.append(occ[mejor])
        else:
            ts.append(occ[0])
    if ts and d.get("tipo") != "placa":
        prev = max(prev, min(ts)) if min(ts) >= prev - 60 else prev
print(malas, "anclas a revisar")
