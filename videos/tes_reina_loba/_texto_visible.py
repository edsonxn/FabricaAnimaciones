# -*- coding: utf-8 -*-
"""V3: segundos con texto quemado (previews/texto_clips.json) que NO tapa ninguna pantalla de Flow.  python _texto_visible.py"""
import json, os, sys
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo"); sys.path.insert(0, os.getcwd())
import secuencia_fx as SF
c = SF.cargar()
P = [(d["de"] + .3, d["a"] - .3) for d in c.fx if d["tipo"] == "pantalla"]
T = json.load(open("previews/texto_clips.json", encoding="utf-8"))
for sid, fr in sorted(T.items()):
    b = c.por_id[sid]
    vis = [(s, t) for s, t in fr if not any(p0 <= b["t0"] + s + .5 <= p1 for p0, p1 in P)]
    if len(vis) >= 2:
        print(f"{sid} {b['t0']:7.1f} {len(vis):2d}s | " + " / ".join(vis[len(vis)//2][1])[:110])
