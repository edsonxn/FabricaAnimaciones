# -*- coding: utf-8 -*-
"""Baja las teselas de OpenTopoMap (CC-BY-SA, © OpenStreetMap) de la zona Jesús María – Moyahua – Juchipila – Apozol y arma
mapas/canon_base.png + mapas/canon_meta.json (bbox en mercator para convertir lat/lon a píxeles). Ruta: OSRM sobre OSM (_ruta.json)."""
import json, math, os, time, io
import requests
from PIL import Image

AQ = os.path.dirname(os.path.abspath(__file__))
Z = 13
LAT0, LAT1, LON0, LON1 = 21.04, 21.50, -103.29, -102.99
UA = {"User-Agent": "FabricaMapas/1.0 (mapa de ruta para un video local)"}


def tile(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


x0, y0 = tile(LAT1, LON0, Z)
x1, y1 = tile(LAT0, LON1, Z)
tx0, ty0, tx1, ty1 = int(x0), int(y0), int(x1), int(y1)
os.makedirs(os.path.join(AQ, "mapas", "_teselas"), exist_ok=True)
W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
im = Image.new("RGB", (W, H))
for tx in range(tx0, tx1 + 1):
    for ty in range(ty0, ty1 + 1):
        p = os.path.join(AQ, "mapas", "_teselas", f"{Z}_{tx}_{ty}.png")
        if not os.path.exists(p):
            for s in "abc":
                r = requests.get(f"https://{s}.tile.opentopomap.org/{Z}/{tx}/{ty}.png", headers=UA, timeout=30)
                if r.ok:
                    open(p, "wb").write(r.content)
                    break
            time.sleep(0.3)
        im.paste(Image.open(p).convert("RGB"), ((tx - tx0) * 256, (ty - ty0) * 256))
im.save(os.path.join(AQ, "mapas", "canon_base.png"))
json.dump(dict(z=Z, tx0=tx0, ty0=ty0, W=W, H=H), open(os.path.join(AQ, "mapas", "canon_meta.json"), "w"))
print("mapa", W, H, "teselas", (tx1 - tx0 + 1) * (ty1 - ty0 + 1))
