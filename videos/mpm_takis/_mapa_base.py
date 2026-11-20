# -*- coding: utf-8 -*-
"""Mapas base REALES (Natural Earth 50 m, países) para mg_mapa tema «planta», proyección Mercator.
Salida: mapas/<slug>.jpg + mapas/<slug>.json (bbox) · ll(slug, lat, lon) → (x, y) en fracción de la imagen.
    python _mapa_base.py            genera norteamerica y atlantico
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
NE = r"C:\FabricaAnimaciones\videos\historia_china\datos\ne_50m_admin_0_countries.geojson"
LAGOS = r"C:\FabricaAnimaciones\videos\independencia_mx\datos\ne_50m_lakes.geojson"
MAPAS = {
    # slug: (lon0, lon1, lat0, lat1, ancho, alto, etiquetas)
    "norteamerica": (-121.0, -86.0, 13.5, 37.5, 2400, 1350,
                     [("MÉXICO", 23.6, -102.5, 64), ("ESTADOS UNIDOS", 35.6, -100.0, 54), ("OCÉANO PACÍFICO", 20.0, -114.5, 34),
                      ("GOLFO DE MÉXICO", 25.2, -90.5, 34)]),
    "atlantico": (-125.0, 12.0, 8.0, 62.0, 2400, 1350,
                  [("MÉXICO", 23.0, -102.5, 46), ("ESTADOS UNIDOS", 39.5, -99.0, 46), ("REINO UNIDO", 55.8, -7.5, 30),
                   ("OCÉANO ATLÁNTICO", 33.0, -45.0, 40)]),
}


def _y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def ll(slug, lat, lon):
    lon0, lon1, lat0, lat1 = MAPAS[slug][:4]
    x = (lon - lon0) / (lon1 - lon0)
    y = 1 - (_y(lat) - _y(lat0)) / (_y(lat1) - _y(lat0))
    return round(x, 4), round(y, 4)


def _anillos(geom):
    t = geom["type"]
    polys = geom["coordinates"] if t == "MultiPolygon" else [geom["coordinates"]]
    for p in polys:
        for k, anillo in enumerate(p):
            yield k, anillo


def generar(slug):
    lon0, lon1, lat0, lat1, W, H, etiquetas = MAPAS[slug]
    def px(lon, lat):
        x, y = ll(slug, lat, lon)
        return x * W, y * H
    im = Image.new("RGB", (W, H), (9, 20, 32))
    d = ImageDraw.Draw(im, "RGBA")
    for lon in range(int(lon0) // 5 * 5, int(lon1) + 5, 5):          # rejilla de plano cada 5°
        x, _ = px(lon, lat0)
        d.line((x, 0, x, H), fill=(40, 84, 116, 90 if lon % 10 else 150), width=1)
    for lat in range(int(lat0) // 5 * 5, int(lat1) + 5, 5):
        _, y = px(lon0, lat)
        d.line((0, y, W, y), fill=(40, 84, 116, 90 if lat % 10 else 150), width=1)
    gj = json.load(open(NE, encoding="utf-8"))
    tierra = Image.new("L", (W, H), 0)
    dt = ImageDraw.Draw(tierra)
    resalta = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(resalta)
    bordes = []
    for f in gj["features"]:
        nombre = f["properties"].get("ADMIN") or f["properties"].get("admin") or ""
        for k, anillo in _anillos(f["geometry"]):
            pts = [px(lo, la) for lo, la in anillo]
            if k == 0:
                dt.polygon(pts, fill=255)
                if nombre in ("Mexico",):
                    dr.polygon(pts, fill=255)
            else:
                dt.polygon(pts, fill=0)
            bordes.append(pts)
    if os.path.exists(LAGOS):
        for f in json.load(open(LAGOS, encoding="utf-8"))["features"]:
            for k, anillo in _anillos(f["geometry"]):
                if k == 0:
                    dt.polygon([px(lo, la) for lo, la in anillo], fill=0)
    # halo de costa
    halo = tierra.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10))
    im.paste((60, 150, 200), (0, 0), halo.point(lambda v: int(v * .25)))
    im.paste((44, 50, 56), (0, 0), tierra)
    im.paste((62, 64, 62), (0, 0), resalta)
    d = ImageDraw.Draw(im, "RGBA")
    for pts in bordes:
        if len(pts) > 2:
            d.line(pts + [pts[0]], fill=(150, 160, 168, 150), width=2)
    f = lambda t: ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", t)
    for txt, la, lo, t in etiquetas:
        x, y = px(lo, la)
        fo = f(t)
        try:
            fo.set_variation_by_name("Light Condensed")
        except Exception:
            pass
        agua = txt.startswith(("OCÉANO", "GOLFO"))
        d.text((x, y), txt, font=fo, anchor="mm", fill=(120, 200, 240, 150) if agua else (200, 204, 208, 120))
    im.save(os.path.join(AQUI, "mapas", slug + ".jpg"), quality=92)
    json.dump(dict(lon=[lon0, lon1], lat=[lat0, lat1], proyeccion="mercator", tam=[W, H], fuente="Natural Earth 50 m"),
              open(os.path.join(AQUI, "mapas", slug + ".json"), "w"))
    print("ok", slug)


if __name__ == "__main__":
    os.makedirs(os.path.join(AQUI, "mapas"), exist_ok=True)
    for s in (sys.argv[1:] or MAPAS):
        generar(s)
