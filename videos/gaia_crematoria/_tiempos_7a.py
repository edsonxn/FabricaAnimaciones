# -*- coding: utf-8 -*-
"""Lista tiempos de prueba del acto 1 (fotos reales y mapas): python _tiempos_7a.py [t_max]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import escenas as E
tmax = float(sys.argv[1]) if len(sys.argv) > 1 else 798
for s in E.TOMAS:
    if s["t0"] >= tmax:
        break
    nom = f"{s['esc']}_{s['n']}"
    if "mapa" in s:
        print(f"MAPA {nom} {s['t0']:.1f}-{s['t1']:.1f} marcas={[round(m,1) for m in s['marcas']]}")
    for r in s.get("real", []):
        cuando = r[1]
        ti = E.tk(*cuando) if isinstance(cuando, tuple) else s["t0"] + (0.4 if cuando is None else cuando)
        print(f"REAL {nom} {r[0]} t={ti+1.5:.1f}")
