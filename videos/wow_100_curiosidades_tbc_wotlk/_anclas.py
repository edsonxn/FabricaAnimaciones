# -*- coding: utf-8 -*-
"""Comprueba las anclas de Rasganorte: cada FX/apoyo desde «mapa rasganorte» con su segundo y la curiosidad de la voz en
ese momento; marca «<<» si salta hacia atrás (el ancla encontró la frase en otra curiosidad: la voz busca la PRIMERA vez)."""
import json
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.getcwd(), r"C:\FabricaAnimaciones\nucleo"]
import secuencia_fx as F  # noqa: E402
import efectos as E  # noqa: E402

c = F.cargar()
tl = json.load(open("timeline.json", encoding="utf-8"))
tramos = [(e["frases"][0]["words"][0]["s"], e["id"]) for e in tl["escenas"] if e["frases"] and e["frases"][0]["words"]]


def cur(t):
    return next((i for s, i in reversed(tramos) if s <= t + 1e-3), "?")


def de(d):
    return c.ancla(d["en"] if "en" in d else d["de"])


i0 = next(k for k, d in enumerate(E.FX) if d.get("nombre") == "mapa rasganorte")
filas = [(de(d), d.get("nombre", d["tipo"])) for d in E.FX[i0:]]
k0 = next(k for k, a in enumerate(E.APOYOS) if c.ancla(a["en"]) >= filas[0][0] - 1)
filas += [(c.ancla(a["en"]), "tarjeta " + a["tarjeta"]["titulo"]) for a in E.APOYOS[k0:]]
prev = 0
for k, (t, n) in enumerate(filas):
    if k == len(E.FX) - i0:
        prev = 0
        print("---- APOYOS")
    print(f"{t:7.1f} {cur(t):7s} {n}" + ("   <<" if t < prev - .5 else ""))
    prev = t
