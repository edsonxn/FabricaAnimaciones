# -*- coding: utf-8 -*-
"""Baja el relieve REAL para el mapa de Tequisquiapan (datos abiertos, sin claves):
  - AWS Terrain Tiles (Terrarium z10 ≈ 143 m a 20,5° N) → datos/relieve_qro_terrarium_z10.npz (z float32, zoom, x0, y0)
  - SRTM15+ (15", ERDDAP coastwatch `srtm15plus`) → datos/relieve_qro_srtm15.nc (ríos D8 y presas)
uso: python _bajar_relieve.py [--z 10]
"""
import math
import os
import sys
import urllib.request

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
LON0, LON1, LAT0, LAT1 = -101.15, -98.75, 22.55, 18.95      # caja del mapa (-101.05..-98.85, 22.45..19.05) + margen
Z = int(sys.argv[sys.argv.index("--z") + 1]) if "--z" in sys.argv else 10


def tile(lon, lat, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return int(x), int(y)


def terrarium():
    x0, y0 = tile(LON0, LAT0, Z)
    x1, y1 = tile(LON1, LAT1, Z)
    mos = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
    cache = os.path.join(DATOS, f"_teselas_z{Z}")
    os.makedirs(cache, exist_ok=True)
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            f = os.path.join(cache, f"{tx}_{ty}.png")
            if not os.path.exists(f):
                u = f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{tx}/{ty}.png"
                urllib.request.urlretrieve(u, f)
            im = cv2.imread(f, cv2.IMREAD_COLOR)[..., ::-1].astype(np.float32)
            e = im[..., 0] * 256.0 + im[..., 1] + im[..., 2] / 256.0 - 32768.0
            mos[(ty - y0) * 256:(ty - y0 + 1) * 256, (tx - x0) * 256:(tx - x0 + 1) * 256] = e
    out = os.path.join(DATOS, f"relieve_qro_terrarium_z{Z}.npz")
    np.savez_compressed(out, z=mos, zoom=Z, x0=x0, y0=y0)
    print("terrarium", mos.shape, "min/max", float(mos.min()), float(mos.max()), "->", out)


def srtm15():
    out = os.path.join(DATOS, "relieve_qro_srtm15.nc")
    if os.path.exists(out):
        print("ya está", out)
        return
    u = (f"https://coastwatch.pfeg.noaa.gov/erddap/griddap/srtm15plus.nc?z[({LAT1}):1:({LAT0})][({LON0}):1:({LON1})]")
    urllib.request.urlretrieve(u, out)
    print("srtm15 ->", out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    terrarium()
    srtm15()
