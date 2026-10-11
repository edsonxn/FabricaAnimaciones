# -*- coding: utf-8 -*-
"""Mapa de relieve REAL del sureste de EE. UU. (teselas de elevación AWS Terrain / Mapzen Terrarium, dominio público: SRTM/NED/ETOPO)
con sombreado calculado aquí, límites estatales (Census, dominio público) y ciudades en su coordenada.
Salida: mapas/relieve_sureste.png (+ mapas/meta.json con la proyección para ubicar puntos)."""
import io, json, math, os, sys
import numpy as np, requests, cv2
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "mapas")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "FabricaAnimaciones/1.0 (jairedson5@gmail.com)"}
Z = 8
LON0, LON1, LAT0, LAT1 = -91.5, -77.0, 32.2, 40.2     # sureste: de Arkansas/Misisipi a Virginia


def tile_xy(lon, lat, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def main():
    x0, y1 = tile_xy(LON0, LAT0, Z)
    x1, y0 = tile_xy(LON1, LAT1, Z)
    tx0, tx1, ty0, ty1 = int(x0), int(x1), int(y0), int(y1)
    W = (tx1 - tx0 + 1) * 256
    H = (ty1 - ty0 + 1) * 256
    dem = np.zeros((H, W), np.float32)
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            u = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{tx}/{ty}.png"
            r = requests.get(u, headers=UA, timeout=60)
            im = np.asarray(Image.open(io.BytesIO(r.content)).convert("RGB")).astype(np.float32)
            dem[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = im[..., 0] * 256 + im[..., 1] + im[..., 2] / 256 - 32768
    # recorte al bbox pedido
    px = lambda lon, lat: ((tile_xy(lon, lat, Z)[0] - tx0) * 256, (tile_xy(lon, lat, Z)[1] - ty0) * 256)
    a, b = px(LON0, LAT1)
    c, d = px(LON1, LAT0)
    dem = dem[int(b):int(d), int(a):int(c)]
    h, w = dem.shape
    # sombreado (luz NO) con exageración vertical
    ps = 1.0  # tamaño de píxel relativo
    mpp = 40075016.0 * math.cos(math.radians((LAT0 + LAT1) / 2)) / (256 * 2 ** Z)
    gy, gx = np.gradient(cv2.GaussianBlur(dem, (0, 0), 1.2), mpp)
    ex = 5.0
    slope = np.arctan(ex * np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    az, alt = math.radians(315), math.radians(42)
    sh = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    sh = np.clip(sh, 0, 1)
    land = dem > 1.0
    # gradación hipsométrica suave (verde-ocre-gris) multiplicada por el sombreado
    e = np.clip(dem, 0, 1900) / 1900.0
    col = np.zeros((h, w, 3), np.float32)
    stops = [(0.00, (0.42, 0.52, 0.38)), (0.12, (0.58, 0.62, 0.42)), (0.35, (0.68, 0.62, 0.45)), (0.7, (0.62, 0.52, 0.42)), (1.0, (0.85, 0.82, 0.78))]
    for k in range(3):
        col[..., k] = np.interp(e, [s[0] for s in stops], [s[1][k] for s in stops])
    img = col * (0.35 + 0.85 * sh[..., None])
    sea = np.array([0.10, 0.16, 0.22], np.float32)
    img[~land] = sea
    img = np.clip(img, 0, 1)
    out = (img * 255).astype(np.uint8)
    meta = dict(w=w, h=h, lon0=LON0, lon1=LON1, lat0=LAT0, lat1=LAT1, z=Z, x_off=float(a), y_off=float(b), tx0=tx0, ty0=ty0)
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"))
    Image.fromarray(out).save(os.path.join(OUT, "relieve_sureste_base.png"))
    print("base", w, h)


if __name__ == "__main__":
    main()
