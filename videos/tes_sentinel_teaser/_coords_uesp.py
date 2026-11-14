# -*- coding: utf-8 -*-
"""Coordenadas REALES de lugares de Skyrim (base de datos del mapa de UESP, gamemap.uesp.net) convertidas a fracciones (x, y) del
mapa de papel mapas/skyrim.jpg. Calibra con las ciudades (leídas en skyrim_rejilla.jpg) por mínimos cuadrados (afín).
    python _coords_uesp.py        imprime cada lugar con su (x, y) en el mapa y el error de calibración"""
import json
import sys
import time
import urllib.parse
import urllib.request

import numpy as np

UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones; coords)"}
sys.stdout.reconfigure(encoding="utf-8")
_cache = {}

# ciudades leídas en mapas/skyrim_rejilla.jpg (centro del escudo de la ciudad)
CIUDADES = {"Solitude": (.33, .20), "Markarth": (.105, .49), "Whiterun": (.545, .49), "Windhelm": (.78, .42),
            "Riften": (.89, .78), "Falkreath": (.43, .77), "Winterhold": (.73, .20), "Dawnstar": (.56, .21), "Morthal": (.42, .31)}

LUGARES = ["Avanchnzel", "Alftand", "Sarethi Farm", "Dead Men's Respite", "Swindler's Den", "Rorikstead", "Forsaken Cave",
           "Throat of the World", "Northwatch Keep", "Red Eagle Redoubt", "Sundered Towers", "Rebel's Cairn", "Ysgramor's Tomb",
           "Wolfskull Cave", "Statue to Meridia", "Kilkreath Ruins", "Last Vigil", "Septimus Signus's Outpost", "Darkfall Cave",
           "Ivarstead", "Froki's Shack", "Folgunthur", "Saarthal", "Geirmund's Hall", "Reachwater Rock", "Dragon Bridge",
           "Graywinter Watch", "Mzinchaleft", "Raldbthar"]


def buscar(nombre):
    if nombre in _cache:
        return _cache[nombre]
    u = "https://gamemap.uesp.net/sr/db/gamemap.php?" + urllib.parse.urlencode(dict(action="search", db="sr", search=nombre))
    for _ in range(3):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
            break
        except Exception:
            time.sleep(3)
    else:
        return None
    locs = [l for l in r.get("locations", []) if l.get("worldId") == 1 and l["name"].lower() == nombre.lower()]
    locs = locs or [l for l in r.get("locations", []) if l.get("worldId") == 1]
    if not locs:
        return None
    l = min(locs, key=lambda l: l.get("displayLevel", 99))          # el marcador del mapa del mundo (nivel más bajo)
    _cache[nombre] = (l["x"], l["y"], l["name"])
    return _cache[nombre]


def main():
    A, B = [], []
    for c, (fx, fy) in CIUDADES.items():
        g = buscar(c)
        if g:
            A.append([g[0], g[1], 1])
            B.append([fx, fy])
    A, B = np.array(A, float), np.array(B, float)
    M, *_ = np.linalg.lstsq(A, B, rcond=None)
    err = np.abs(A @ M - B).max()
    print(f"calibración con {len(A)} ciudades · error máx {err:.3f}")
    for n in LUGARES:
        g = buscar(n)
        if not g:
            print(f"  {n:28} —")
            continue
        x, y = np.array([g[0], g[1], 1.0]) @ M
        print(f"  {n:28} ({x:.3f}, {y:.3f})   [{g[2]}]")


if __name__ == "__main__":
    main()
