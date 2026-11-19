# -*- coding: utf-8 -*-
"""Lista TODAS las anclas de efectos.py que la voz no dice (fx --seco se para en la primera).
    python _anclas_check.py
"""
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import secuencia_fx as SF

tl = json.load(open("timeline.json", encoding="utf-8"))
pal = [SF._norm(w["w"]) for e in tl["escenas"] for fr in e["frases"] for w in fr["words"]]
pal = [p for p in pal if p]
sp = importlib.util.spec_from_file_location("fxv", "efectos.py")
m = importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)


def ok(x):
    if isinstance(x, (int, float)):
        return True
    if isinstance(x, (tuple, list)):
        return ok(x[0])
    if re.fullmatch(r"scene-\d{3,}(:fin)?", x):
        return True
    mm = re.fullmatch(r"(.*?)(?:#(\d+))?(\|fin)?", x, re.S)
    ag = [w for w in (SF._norm(w) for w in mm.group(1).split()) if w]
    vez, visto = int(mm.group(2) or 1), 0
    for i in range(len(pal) - len(ag) + 1):
        if pal[i:i + len(ag)] == ag:
            visto += 1
            if visto == vez:
                return True
    return False


malas = []
for lista in ("FX", "PISTAS", "ROTULOS"):
    for d in getattr(m, lista, []):
        for k in ("en", "de", "a"):
            if k in d and not ok(d[k]):
                malas.append((lista, d.get("nombre", ""), k, d[k]))
        for x in d.get("marcas", []):
            if not ok(x):
                malas.append((lista, d.get("nombre", ""), "marca", x))
for x in malas:
    print(*x, sep=" | ")
print(len(malas), "anclas malas")
