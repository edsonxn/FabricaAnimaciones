# -*- coding: utf-8 -*-
"""Comprueba que cada ancla de efectos.py existe en el guion (y cuántas veces), sin cargar los kits (stubs).
Avisa si un ancla cae > 40 palabras ANTES que la anterior (lección de Radahn) y de las ambiguas sin #n.
    python _anclas.py
"""
import importlib
import re
import sys
import types
import unicodedata

for m in ("mg_er", "mg_tes", "peg_estilos", "mg_wow", "mg_mapa"):
    st = types.ModuleType(m)
    st.__getattr__ = lambda n: (lambda *a, **k: (lambda *x, **y: None))
    sys.modules[m] = st
sys.modules["peg_estilos"].pos_silueta = lambda fn, lado="izq": (.2, .6)

G = importlib.import_module("guion")
E = importlib.import_module("efectos")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ ]+", " ", s.replace("ñ", "n")).split()


palabras = []
for esc in G.ESCENAS:
    for f in esc["frases"]:
        palabras += norm(f)


def posiciones(txt):
    w = norm(txt)
    n = len(w)
    return [i for i in range(len(palabras) - n + 1) if palabras[i:i + n] == w]


def ancla(a):
    if isinstance(a, (int, float)) or a is None:
        return None
    if isinstance(a, tuple):
        a = a[0]
    if not isinstance(a, str) or a.startswith("scene-"):
        return None
    a = a.split("|")[0]
    k = 1
    if "#" in a:
        a, k = a.split("#")
        k = int(k)
    return a, k


malas, prev = 0, -1
for i, fx in enumerate(E.FX):
    nombre = fx.get("nombre", "?")
    for campo in ("en", "de", "a"):
        r = ancla(fx.get(campo))
        if not r:
            continue
        p = posiciones(r[0])
        if len(p) < r[1]:
            print(f"NO ESTÁ  [{nombre}] {campo}: «{r[0]}» #{r[1]}")
            malas += 1
            continue
        pos = p[r[1] - 1]
        if len(p) > 1 and r[1] == 1:
            print(f"  ambigua ({len(p)}×) [{nombre}] {campo}: «{r[0]}»")
        if campo in ("en", "de"):
            if pos < prev - 40:
                print(f"  ATRÁS {prev - pos} palabras [{nombre}] «{r[0]}»")
            prev = pos
    rd, ra = ancla(fx.get("de")), ancla(fx.get("a"))
    pd = posiciones(rd[0])[rd[1] - 1] if rd and len(posiciones(rd[0])) >= rd[1] else None
    pa = posiciones(ra[0])[ra[1] - 1] + len(norm(ra[0])) if ra and len(posiciones(ra[0])) >= ra[1] else None
    for m in fx.get("marcas") or []:
        r = ancla(m)
        if not r:
            continue
        p = posiciones(r[0])
        if len(p) < r[1]:
            print(f"NO ESTÁ  [{nombre}] marca: «{r[0]}»")
            malas += 1
        elif pd is not None and pa is not None and not (pd - 8 <= p[r[1] - 1] <= pa + 8):
            k = next((i + 1 for i, q in enumerate(p) if pd - 8 <= q <= pa + 8), None)
            print(f"FUERA    [{nombre}] marca «{r[0]}» → usa «{r[0]}#{k}»")
            malas += 1
print(f"{len(E.FX)} FX · {malas} anclas que no están")
