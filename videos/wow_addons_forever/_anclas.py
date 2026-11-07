# -*- coding: utf-8 -*-
"""Comprueba TODAS las anclas de efectos.py contra la transcripción (timeline.json) y sugiere la grafía real."""
import importlib.util, json, os, re, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
from secuencia_fx import _norm
tl = json.load(open("timeline.json", encoding="utf-8"))
pal = [_norm(w["w"]) for e in tl["escenas"] for fr in e["frases"] for w in fr["words"]]
pal = [p for p in pal if p]
crudo = [w["w"] for e in tl["escenas"] for fr in e["frases"] for w in fr["words"]]
s = importlib.util.spec_from_file_location("efx", "efectos.py"); E = importlib.util.module_from_spec(s); s.loader.exec_module(E)
def anclas(d):
    for k in ("en", "de", "a"):
        if k in d: yield d[k]
    for m in d.get("marcas", []): yield m
def txt(x):
    return x[0] if isinstance(x, (tuple, list)) else x
malas = set()
for d in list(E.FX) + list(E.APOYOS) + list(E.ROTULOS) + list(E.PISTAS):
    for a in anclas(d):
        a = txt(a)
        if not isinstance(a, str) or a.startswith("scene-"):
            continue
        m = re.fullmatch(r"(.*?)(?:#(\d+))?(\|fin)?", a, re.S)
        ag = [w for w in (_norm(w) for w in m.group(1).split()) if w]
        n = sum(1 for i in range(len(pal) - len(ag) + 1) if pal[i:i + len(ag)] == ag)
        if n < int(m.group(2) or 1):
            malas.add(m.group(1))
for a in sorted(malas):
    ag = [w for w in (_norm(w) for w in a.split()) if w]
    best = max(range(len(pal)), key=lambda i: sum(1 for j in range(len(ag)) if i + j < len(pal) and pal[i + j] == ag[j]))
    print(f"✗ «{a}»  →  {' '.join(crudo[best:best + len(ag) + 2])}")
print(len(malas), "anclas sin encontrar")
