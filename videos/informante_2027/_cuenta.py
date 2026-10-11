# -*- coding: utf-8 -*-
"""Cuenta palabras y caracteres del guion (sin corchetes) y estima la duración a 2,5 palabras/s + pausas."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion as G

tot_p = tot_c = n = 0
aire = 0.0
for e in G.ESCENAS:
    p = c = 0
    for f in e["frases"]:
        limpio = re.sub(r"\[[^\]]*\]\s*", "", f)
        p += len(limpio.split()); c += len(f)
    n += len(e["frases"])
    aire += e.get("pre", 0) + e.get("post", 0) + G.GAP * (len(e["frases"]) - 1)
    print(f"{e['id']:12s} frases={len(e['frases'])} palabras={p:4d} ~{p / 2.5:5.1f}s")
    tot_p += p; tot_c += c
voz = tot_p / 2.5
print(f"TOTAL escenas={len(G.ESCENAS)} frases={n} palabras={tot_p} caracteres={tot_c} voz~{voz:.0f}s aire~{aire:.0f}s total~{(voz + aire) / 60:.1f} min")
print(f"creditos eleven_v4 ~{tot_c * 0.11:.0f}")
