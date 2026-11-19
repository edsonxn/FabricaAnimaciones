# -*- coding: utf-8 -*-
"""Baja teselas de OpenTopoMap (CC-BY-SA, © OpenStreetMap) y arma dos bases: sierra (z13, Juchipila – Sierra de Morones)
y region (z8, Juchipila – sur de Durango). mapas/<nombre>.png + mapas/<nombre>_meta.json."""
import json, math, os, time
import requests
from PIL import Image

AQ = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "FabricaMapas/1.0 (mapa para un video local)"}
ZONAS = {"sierra": (13, 21.27, 21.46, -103.33, -103.06), "region": (9, 19.9, 24.3, -106.4, -101.4)}


def tile(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n


for nombre, (Z, LAT0, LAT1, LON0, LON1) in ZONAS.items():
    x0, y0 = tile(LAT1, LON0, Z)
    x1, y1 = tile(LAT0, LON1, Z)
    tx0, ty0, tx1, ty1 = int(x0), int(y0), int(x1), int(y1)
    os.makedirs(os.path.join(AQ, "mapas", "_teselas"), exist_ok=True)
    im = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
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
    im.save(os.path.join(AQ, "mapas", nombre + ".png"))
    json.dump(dict(z=Z, tx0=tx0, ty0=ty0), open(os.path.join(AQ, "mapas", nombre + "_meta.json"), "w"))
    print(nombre, im.size)
