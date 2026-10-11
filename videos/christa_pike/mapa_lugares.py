# -*- coding: utf-8 -*-
"""Compone mapas/mapa_sureste.png: relieve real + límites estatales (Natural Earth) + proyección para ubicar ciudades.
Importable: `proyecta(lon, lat) -> (x, y)` en píxeles del mapa (2640x1808)."""
import json, math, os
import numpy as np, cv2
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
META = json.load(open(os.path.join(AQUI, "mapas", "meta.json")))


def proyecta(lon, lat):
    n = 2 ** META["z"]
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return (x - META["tx0"]) * 256 - META["x_off"], (y - META["ty0"]) * 256 - META["y_off"]


CIUDADES = {   # nombre: (lon, lat)
    "Beckley": (-81.188, 37.778), "Swannanoa": (-82.400, 35.598), "Knoxville": (-83.921, 35.961), "Nashville": (-86.781, 36.163),
}


def componer():
    base = Image.open(os.path.join(AQUI, "mapas", "relieve_sureste_base.png")).convert("RGB")
    g = np.asarray(base).astype(np.float32)
    lum = g @ np.array([0.30, 0.59, 0.11], np.float32)
    g = lum[..., None] + (g - lum[..., None]) * 0.35           # desaturado, serio
    g = np.clip(g * 0.92, 0, 255).astype(np.uint8)
    im = Image.fromarray(g)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    gj = json.load(open(os.path.join(AQUI, "mapas", "ne_admin1.geojson"), encoding="utf-8"))
    for ft in gj["features"]:
        p = ft["properties"]
        if p.get("adm0_a3") != "USA" and p.get("iso_a2") != "US":
            continue
        nom = p.get("name")
        geom = ft["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        tn = nom == "Tennessee"
        for poly in polys:
            for ring in poly:
                pts = [proyecta(lo, la) for lo, la in ring]
                if all(-200 < x < im.size[0] + 200 and -200 < y < im.size[1] + 200 for x, y in pts[::8]) or any(0 <= x < im.size[0] and 0 <= y < im.size[1] for x, y in pts[::8]):
                    d.line(pts + [pts[0]], fill=(255, 205, 80, 235) if tn else (255, 255, 255, 120), width=7 if tn else 3, joint="curve")
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    im.save(os.path.join(AQUI, "mapas", "mapa_sureste.png"))
    return im


if __name__ == "__main__":
    im = componer()
    print(im.size, {k: tuple(round(v) for v in proyecta(*c)) for k, c in CIUDADES.items()})
    im.resize((im.size[0] // 3, im.size[1] // 3)).save(os.path.join(AQUI, "previews", "mapa_sureste_vista.jpg"))
