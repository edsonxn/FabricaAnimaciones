# -*- coding: utf-8 -*-
"""Huecos sin MG/pegatina/pantalla > 4 s, a partir de `fx --seco` (guardado en _fxseco.log). 3-nov-2026."""
import re
iv = []
for ln in open("_fxseco.log", encoding="utf-8", errors="ignore"):
    m = re.match(r"\s*([\d.]+)-\s*([\d.]+)\s+scene-\d+\s+FX\s+(mg|pantalla)", ln)
    if m:
        iv.append((float(m.group(1)), float(m.group(2))))
iv.sort()
fin, huecos = 0.0, []
for a, b in iv:
    if a - fin > 4.0:
        huecos.append((fin, a))
    fin = max(fin, b)
if 1644 - fin > 4:
    huecos.append((fin, 1644))
print(len(iv), "gráficos ·", round(len(iv) / 27.4, 1), "por min ·", len(huecos), "huecos > 4 s,", round(sum(b - a for a, b in huecos)), "s")
for a, b in huecos:
    print(f"  {a:7.1f} - {b:7.1f}  ({b - a:4.1f} s)")
