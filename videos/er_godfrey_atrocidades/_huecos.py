# -*- coding: utf-8 -*-
"""Huecos sin pegatina/MG/pantalla > LIM s, FX de < 2 s y FX que pasan del final (regla del 3-nov-2026: ningún tramo de > ~4 s
con el clip solo, salvo que suene un audio nombrado). Además, densidad por minuto y MG por tipo.
    python _huecos.py [LIM]          (desde la carpeta del video; carga efectos.py con los kits reales, como fx --seco)
"""
import collections
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(1, os.path.join(AQUI, "..", "..", "nucleo"))
import secuencia_fx as SF

LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
capa = SF.cargar()
tot = capa.total
iv = sorted((d["de"], d["a"], d.get("nombre", "?")) for d in capa.fx)
audio = [(d["de"], d["a"]) for d in capa.pistas if d.get("voz")]
t, huecos = 0.6, []
for de, a, n in iv:
    if de - t > LIM:
        if not any(p0 <= t + .5 and p1 >= de - .5 for p0, p1 in audio):
            huecos.append((t, de))
    t = max(t, a)
if tot - 1 - t > LIM:
    huecos.append((t, tot))
print(f"{len(capa.fx)} FX · {tot:.1f} s · {len(capa.fx) / (tot / 60):.1f} FX/min")
print(f"HUECOS > {LIM} s:", len(huecos))
for h in huecos:
    print(f"  {h[0]:7.1f}-{h[1]:7.1f}  ({h[1] - h[0]:.1f} s)  {capa.beat_en(h[0] + .01)['id']}")
cortos = [(de, a, n) for de, a, n in iv if a - de < 2.0]
print("FX < 2 s:", len(cortos))
for c in cortos:
    print(f"  {c[0]:7.1f}-{c[1]:7.1f}  {c[2]}")
largos = [(de, a, n) for de, a, n in iv if a - de > 30]
print("FX > 30 s:", len(largos))
for c in largos:
    print(f"  {c[0]:7.1f}-{c[1]:7.1f}  {c[2]}")
fuera = [d.get("nombre") for d in capa.fx for m in d.get("_marcas", []) if m < -.05 or m > d["a"] - d["de"] + .05]
print("marcas fuera del tramo:", len(fuera), sorted(set(fuera)))
tipos = collections.Counter(n.split()[0] + (" " + n.split()[1] if n.startswith("MG ") else "") for _, _, n in iv)
for k, v in sorted(tipos.items(), key=lambda x: -x[1]):
    print(f"  {v:3d}  {k}")
