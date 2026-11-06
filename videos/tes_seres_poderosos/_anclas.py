# -*- coding: utf-8 -*-
"""Anclas que casan > 1 vez o 0 veces (lección dwemer). python _anclas.py"""
import json, os, re, sys
sys.path.insert(0, os.path.join("..", "..", "nucleo"))
from secuencia_fx import _norm
import importlib.util
tl = json.load(open("timeline.json", encoding="utf-8"))
pal = [_norm(w["w"]) for e in tl["escenas"] for fr in e["frases"] for w in fr["words"]]
pal = [p for p in pal if p]
spec = importlib.util.spec_from_file_location("ef", "efectos.py"); ef = importlib.util.module_from_spec(spec); spec.loader.exec_module(ef)
def cuenta(s):
    s = re.sub(r"(#\d+)?(\|fin)?$", "", s)
    a = [w for w in (_norm(w) for w in s.split()) if w]
    return sum(1 for i in range(len(pal) - len(a) + 1) if pal[i:i + len(a)] == a)
def anclas(d):
    for k in ("en", "de", "a"):
        v = d.get(k)
        if isinstance(v, (tuple, list)): v = v[0]
        if isinstance(v, str) and not v.startswith("scene-"): yield k, v
    for m in d.get("marcas", []):
        if isinstance(m, (tuple, list)): m = m[0]
        if isinstance(m, str): yield "marca", m
n = 0
for i, d in enumerate(list(ef.FX) + list(getattr(ef, "PISTAS", []))):
    for k, v in anclas(d):
        c = cuenta(v)
        if c != 1 and "#" not in v:
            n += 1; print(f"{i:4d} {d.get('nombre', d.get('sfx', d.get('tipo')))[:30]:30s} {k:5s} x{c}  «{v}»")
print(n, "anclas a revisar")
