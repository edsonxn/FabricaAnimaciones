# -*- coding: utf-8 -*-
"""Prepara los datos geográficos del mapa con relieve (kz_mapa.py). Se corre UNA vez: `python kz_mapa_datos.py`.

Fuentes (todas de dominio público):
  - Relieve y batimetría: NOAA NCEI ETOPO1 (1 minuto de arco), ventana lat 14-33.5, lon -119 a -84.5
    (descargado de coastwatch.pfeg.noaa.gov/erddap, dataset etopo180 -> videos/independencia_mx/datos/relieve_mx_etopo1.nc).
  - Países, costas y lagos: Natural Earth 50 m (naturalearthdata.com; videos/historia_china/datos/ne_50m_admin_0_countries.geojson
    y videos/independencia_mx/datos/ne_50m_lakes.geojson).
Salida en nucleo/datos/: relieve_mx.npz (altitud int16 + ríos calculados del relieve), paises.json (polígonos), lagos.json.
Los ríos se calculan con el relieve real (llenado de depresiones + acumulación de flujo D8), no se dibujan a mano."""
import json
import os
import sys

import numpy as np
from numba import njit

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SAL = os.path.join(AQUI, "datos")
NC = os.path.join(RAIZ, "videos", "independencia_mx", "datos", "relieve_mx_etopo1.nc")
PAISES = os.path.join(RAIZ, "videos", "historia_china", "datos", "ne_50m_admin_0_countries.geojson")
LAGOS = os.path.join(RAIZ, "videos", "independencia_mx", "datos", "ne_50m_lakes.geojson")

LAT0, LON0, PASO = 14.0, -119.0, 1.0 / 60.0


# ------------------------------------------------------------------ ríos desde el relieve
@njit(cache=True)
def _heap_push(hk, hv, n, k, v):
    i = n
    hk[i] = k
    hv[i] = v
    while i > 0:
        p = (i - 1) // 2
        if hk[p] <= hk[i]:
            break
        hk[p], hk[i] = hk[i], hk[p]
        hv[p], hv[i] = hv[i], hv[p]
        i = p
    return n + 1


@njit(cache=True)
def _heap_pop(hk, hv, n):
    k0, v0 = hk[0], hv[0]
    n -= 1
    hk[0], hv[0] = hk[n], hv[n]
    i = 0
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and hk[l] < hk[m]:
            m = l
        if r < n and hk[r] < hk[m]:
            m = r
        if m == i:
            break
        hk[m], hk[i] = hk[i], hk[m]
        hv[m], hv[i] = hv[i], hv[m]
        i = m
    return k0, v0, n


@njit(cache=True)
def priority_flood(dem, mar):
    """Barnes 2014 (Priority-Flood + epsilon). mar: celdas que son salida (mar). Devuelve (relieve llenado, padre, orden de extracción).
    padre[c] = celda a la que desagua c (-1 en las salidas)."""
    h, w = dem.shape
    N = h * w
    fill = dem.copy()
    padre = np.full(N, -2, np.int32)
    orden = np.empty(N, np.int32)
    hk = np.empty(N + 8, np.float32)
    hv = np.empty(N + 8, np.int32)
    n = 0
    for i in range(h):
        for j in range(w):
            c = i * w + j
            if mar[i, j] or i == 0 or j == 0 or i == h - 1 or j == w - 1:
                padre[c] = -1
                n = _heap_push(hk, hv, n, fill[i, j], c)
    dx = np.array([1, -1, 0, 0, 1, 1, -1, -1])
    dy = np.array([0, 0, 1, -1, 1, -1, 1, -1])
    k = 0
    eps = np.float32(1e-3)
    while n > 0:
        e, c, n = _heap_pop(hk, hv, n)
        orden[k] = c
        k += 1
        ci, cj = c // w, c % w
        for d in range(8):
            ni, nj = ci + dy[d], cj + dx[d]
            if ni < 0 or nj < 0 or ni >= h or nj >= w:
                continue
            m = ni * w + nj
            if padre[m] != -2:
                continue
            padre[m] = c
            if fill[ni, nj] <= e:
                fill[ni, nj] = e + eps
            n = _heap_push(hk, hv, n, fill[ni, nj], m)
    return fill, padre, orden


@njit(cache=True)
def acumular(padre, orden):
    acc = np.ones(padre.shape[0], np.float32)
    for k in range(orden.shape[0] - 1, -1, -1):
        c = orden[k]
        p = padre[c]
        if p >= 0:
            acc[p] += acc[c]
    return acc


def rios(alt, lat0=LAT0, lon0=LON0, umbral=260):
    h, w = alt.shape
    dem = alt.astype(np.float32)
    mar = alt <= 0
    fill, padre, orden = priority_flood(dem, mar)
    acc = acumular(padre, orden)
    marf = mar.reshape(-1)
    es_rio = (acc >= umbral) & (~marf)
    # fuentes: celdas de río sin afluente de río
    tiene_aflu = np.zeros(h * w, bool)
    idx = np.nonzero(es_rio)[0]
    p = padre[idx]
    ok = p >= 0
    tiene_aflu[p[ok]] = True
    fuentes = idx[~tiene_aflu[idx]]
    usado = np.zeros(h * w, bool)
    lineas = []
    for s in fuentes:
        c = int(s)
        pts = []
        while True:
            pts.append((c, float(acc[c])))
            ya = usado[c]
            usado[c] = True
            p = int(padre[c])
            if ya or p < 0 or marf[p]:
                if p >= 0 and (not ya):
                    pts.append((p, float(acc[p])))
                break
            c = p
        if len(pts) >= 5:
            lineas.append(pts)
    salida = []
    for pts in lineas:
        ci = np.array([c for c, _ in pts])
        ii, jj = ci // w, ci % w
        lat = lat0 + ii * PASO
        lon = lon0 + jj * PASO
        a = np.array([v for _, v in pts], np.float32)
        salida.append(np.stack([lon, lat, a], 1).astype(np.float32))
    return salida, acc.reshape(h, w)


# ------------------------------------------------------------------ geojson
def _anillos(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    return geom["coordinates"]


def simplificar(p, tol):
    import cv2
    q = np.asarray(p, np.float32).reshape(-1, 1, 2)
    r = cv2.approxPolyDP(q, tol, False).reshape(-1, 2)
    return r if len(r) >= 3 else np.asarray(p, np.float32)


def paises():
    """Todos los países con alguna parte entre lon -135..50 y lat -58..75 (América, Europa y el norte de África). México y los vecinos cercanos conservan el detalle completo;
    el resto se simplifica a ~0,02° para que el archivo no crezca."""
    import cv2
    g = json.load(open(PAISES, encoding="utf-8"))
    detalle = {"Mexico", "United States of America", "Guatemala", "Belize", "Honduras", "El Salvador", "Nicaragua", "Cuba", "Spain", "Costa Rica", "Panama", "Jamaica", "Haiti", "Dominican Republic", "Bahamas"}
    out = {}
    for ft in g["features"]:
        nom = ft["properties"].get("NAME") or ft["properties"].get("ADMIN")
        polys = []
        for poly in _anillos(ft["geometry"]):
            ext = np.array(poly[0], np.float32)
            if len(ext) < 4:
                continue
            if not (ext[:, 0].max() > -135 and ext[:, 0].min() < 50 and ext[:, 1].max() > -58 and ext[:, 1].min() < 75):
                continue
            if nom not in detalle:
                ext = simplificar(ext, 0.02)
            polys.append(ext.tolist())
        if polys:
            out[nom] = polys
    return out


def lagos():
    g = json.load(open(LAGOS, encoding="utf-8"))
    out = []
    for ft in g["features"]:
        for poly in _anillos(ft["geometry"]):
            a = np.array(poly[0], np.float32)
            if ((a[:, 0] > -118) & (a[:, 0] < -86) & (a[:, 1] > 14) & (a[:, 1] < 33)).any():
                out.append(dict(nombre=ft["properties"].get("name"), pts=a.tolist()))
    return out


VENTANAS = {
    "mx": os.path.join(RAIZ, "videos", "independencia_mx", "datos", "relieve_mx_etopo1.nc"),
    "eu": os.path.join(RAIZ, "videos", "independencia_mx", "datos", "relieve_eu_etopo1.nc"),
}


def ventana(nombre):
    """Lee un .nc de NOAA ETOPO1 (altitud en m), calcula los ríos y guarda nucleo/datos/relieve_<nombre>.npz."""
    from scipy.io import netcdf_file
    f = netcdf_file(VENTANAS[nombre], "r", mmap=False)
    alt = f.variables["altitude"][:].astype(np.int16).copy()
    lat = f.variables["latitude"][:].copy()
    lon = f.variables["longitude"][:].copy()
    lat0, lon0 = float(lat[0]), float(lon[0])
    print(nombre, "relieve", alt.shape, alt.min(), alt.max(), "lat0", lat0, "lon0", lon0)
    rs, acc = rios(alt, lat0, lon0)
    print("  ríos:", len(rs), "tramos")
    pts = np.concatenate(rs)
    cortes = np.cumsum([0] + [len(r) for r in rs]).astype(np.int32)
    np.savez_compressed(os.path.join(SAL, f"relieve_{nombre}.npz"), alt=alt, lat0=lat0, lon0=lon0, paso=PASO, rios_pts=pts, rios_cortes=cortes, acc=np.log1p(acc).astype(np.float16))


def main():
    os.makedirs(SAL, exist_ok=True)
    for nombre in VENTANAS:
        if os.path.isfile(VENTANAS[nombre]):
            ventana(nombre)
    json.dump(paises(), open(os.path.join(SAL, "paises.json"), "w"), separators=(",", ":"))
    json.dump(lagos(), open(os.path.join(SAL, "lagos.json"), "w"), separators=(",", ":"))
    for n in sorted(os.listdir(SAL)):
        print(n, os.path.getsize(os.path.join(SAL, n)) // 1024, "KB")


if __name__ == "__main__":
    main()
