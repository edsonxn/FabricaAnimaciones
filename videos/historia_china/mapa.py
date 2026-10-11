# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de China en 3 minutos».

Todo son campos de distancia con signo (SDF, negativo = dentro) rasterizados una vez por proceso sobre una rejilla
lon/lat («campo»). Cada cuadro se interpolan los campos de dos épocas (el imperio crece, se encoge, se reparte), se
proyectan a pantalla con la cámara (`Cam`) y se pintan con pincel de guache: relleno plano con grano, borde más denso y
media luna de sombra hacia abajo-derecha. Después la escena dibuja encima tinta y crayón (boceto).
"""
import json
import math
import os

import cv2
import numpy as np

import boceto as B
from motor import H, W, clamp01, lerp, prog

AQUI = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ proyección (rectangular con coseno de latitud medio)
LON0, LON1, LAT0, LAT1 = 58.0, 152.0, 62.0, -2.0
PXLAT = 26.0                                  # píxeles de campo por grado de latitud
KX = math.cos(math.radians(33.0))
FW = int((LON1 - LON0) * KX * PXLAT)
FH = int((LAT0 - LAT1) * PXLAT)


def proj(lon, lat):
    """lon/lat -> píxeles del campo (puede recibir arreglos)."""
    return (np.asarray(lon, float) - LON0) * KX * PXLAT, (LAT0 - np.asarray(lat, float)) * PXLAT


def proj_pts(P):
    P = np.asarray(P, float)
    x, y = proj(P[:, 0], P[:, 1])
    return np.stack([x, y], 1)


# ------------------------------------------------------------------ paleta de guache (apagada y cálida)
MAR = (186, 214, 216)
MAR_CL = (206, 228, 226)
TIERRA = (234, 222, 192)
TIERRA_OSC = (214, 198, 160)
COL = {
    "shang": (205, 150, 70), "zhou": (122, 160, 104), "estados": (196, 120, 92), "qin": (142, 74, 66),
    "han": (206, 98, 72), "tres": (196, 98, 82), "tang": (238, 178, 64), "song": (126, 168, 138),
    "yuan": (96, 134, 184), "ming": (196, 62, 62), "qing": (70, 144, 146), "rep": (170, 136, 170), "prc": (206, 70, 58),
}
COL_CELDAS = [(206, 98, 72), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
              (140, 120, 190), (180, 160, 90), (110, 170, 170)]


# ------------------------------------------------------------------ geometrías de las épocas (lon, lat). El lado del mar es
# generoso porque cada época se recorta con la tierra firme.
POLI = {
    "shang": [(109, 35), (110, 38), (113.5, 39.8), (117.5, 39.6), (121, 38.5), (123, 37), (121.5, 34.5), (119, 32.5), (113, 32), (110, 33)],
    "zhou": [(104.5, 35.5), (105, 38), (109, 40.5), (113, 41), (117, 41.5), (121, 41), (123.5, 39), (123.5, 37), (122.5, 34), (122.5, 30.5),
             (121.5, 28), (119.6, 27.5), (118, 26), (115, 25), (112, 27), (109, 29.5), (107, 31.5), (105, 33.5)],
    "estados": [(101, 32), (101, 36), (104, 38.5), (108, 41.5), (113, 42), (118, 42.5), (122, 42), (124, 40), (123.5, 37), (122.5, 34),
                (122.5, 30.5), (121.5, 28), (119.6, 26), (116.5, 24.5), (111, 24.5), (107, 25), (104, 27), (102, 28.5), (101, 30)],
    "qin": [(101, 33), (100.5, 36), (104, 38.5), (107, 41), (112, 42), (117, 42.5), (121, 42), (124, 40.3), (123.5, 37), (122.5, 34),
            (122.5, 30.5), (121.5, 28), (119.6, 26), (119.6, 23.5), (117, 22), (113, 21), (109.5, 20.5), (107, 21.5), (105.5, 23),
            (104.5, 26), (102.5, 27.5), (101, 29.5)],
    "han": [(94, 41), (98, 42.5), (104, 42.5), (108, 42), (113, 42.5), (118, 42.5), (122, 43.5), (125, 42.8), (126.8, 40), (125.5, 37.8),
            (123.5, 36), (122.5, 34), (122.5, 30.5), (121.5, 28), (119.6, 26), (119.6, 23.5), (117, 22), (113, 20.5), (109.5, 19.3),
            (106, 19.3), (105, 21.8), (103, 22), (100.5, 21.8), (98.5, 24), (98, 27), (100, 29), (100, 32), (98.5, 34.5), (98, 37.5), (94, 38.5)],
    "tres": [(98, 36.5), (102, 38), (106, 40), (110, 41.5), (115, 41.5), (119, 41), (122.5, 40.2), (123, 38), (122.5, 34), (122.5, 30.5),
             (121.5, 28), (119.6, 26), (119.6, 23.5), (117, 22), (113, 20.5), (109.5, 19.3), (106, 20.5), (105.5, 22.5), (103, 22.5),
             (101, 24), (98.5, 25.5), (100, 29), (100, 32), (99, 34.5)],
    "tang": [(72.5, 39.5), (71, 41.5), (74, 43.5), (79, 44.5), (84, 46.5), (90, 46), (96, 44), (104, 42.5), (110.5, 43.5), (116, 47),
             (121, 47.5), (123, 45), (124.5, 42), (124.5, 40.2), (124, 37), (123.5, 33), (122.5, 28.5), (121, 26.5), (119.6, 25.5),
             (119.6, 23.5), (117, 22), (113, 20.5), (109.5, 19.3), (106, 20), (105, 22.5), (101, 22.5), (98.5, 24), (98.2, 27), (99.5, 29.5),
             (101.5, 31), (102.5, 33.5), (102, 35.5), (101, 37), (96, 37.3), (90, 37.7), (84, 36.8), (78, 37.5), (75.5, 38.8)],
    "song": [(103, 30), (104.5, 33.5), (104, 35), (106, 36.5), (106, 38), (110, 37.5), (113, 39.3), (116, 39.3), (118, 38.5), (120, 37.8),
             (123, 37), (122.5, 34), (122.5, 30.5), (121.5, 28), (119.6, 26), (119.6, 23.5), (117, 22), (113, 20.8), (109.5, 19.3),
             (108, 21.3), (106.5, 21.8), (105.5, 23.5), (105.2, 26), (104, 28)],
    "yuan": [(74.5, 38.5), (73, 41), (77, 44.5), (81, 46), (85, 48.5), (88, 50), (93, 51.5), (99, 51.8), (104, 50.5), (108, 50),
             (113, 50.3), (118, 49.8), (121, 53), (126, 53.5), (131, 51), (134.5, 48.5), (135.5, 43.5), (130.3, 42.5), (128, 41.8),
             (125, 40.8), (124.3, 39.8), (124, 37), (123.5, 33), (122.5, 28.5), (121, 26.5), (119.6, 25.5), (119.6, 23.5), (117, 22),
             (113, 20.5), (109.5, 19.3), (106.5, 21.3), (105.5, 22.8), (103, 22.5), (101, 21.5), (98.5, 23), (97.8, 25), (98.5, 27.5),
             (96.5, 28.3), (93, 27.3), (89, 27.5), (85, 27.7), (81, 30), (79, 32.5), (78, 35), (76.5, 36.5), (75.5, 38.2)],
    "ming": [(98, 39.8), (100.5, 39.5), (103.5, 38.8), (106.5, 38.8), (109, 39.5), (112, 40.5), (113.5, 41.5), (116, 42), (118, 41.5),
             (121, 41.5), (124.5, 41.2), (124.3, 39.8), (124, 37), (123.5, 33), (122.5, 28.5), (121, 26.5), (119.6, 25.5), (119.6, 23.5),
             (117, 22), (113, 20.5), (109.5, 19.3), (108, 21.3), (106.5, 22.6), (105, 23.3), (103, 22.5), (101.5, 22.3), (99.5, 22.3),
             (98.5, 24.5), (98.5, 27.5), (99.5, 29.5), (101.5, 31), (102.5, 33.5), (103.5, 35.3), (101, 36.8), (99, 38.3)],
    "qing": [(74, 39), (73.8, 41.5), (78, 43.5), (80.2, 45), (83, 47.3), (87, 49.2), (91, 50.5), (96, 50.5), (98.5, 52), (104, 51),
             (108, 49.8), (116, 49.8), (119.5, 52.7), (122, 54.5), (127, 55), (135, 55), (141, 54), (142.5, 48), (140.5, 45), (135, 42.8),
             (131, 42.5), (130.3, 42.3), (128, 41.6), (125, 40.7), (124.2, 39.8), (124, 37), (123.5, 33), (122.5, 28.5), (122.6, 26),
             (122.4, 21.8), (119.6, 21.8), (117, 22), (113, 20.5), (109.5, 19.3), (108, 21.3), (106.5, 22.6), (105, 23.3), (103, 22.5),
             (101.5, 21.5), (100, 21.5), (98.5, 24), (97.5, 28.3), (96, 28.5), (93, 27.3), (89.5, 27.5), (85, 27.8), (81, 30), (79, 32.5),
             (78, 35), (76.5, 36.5), (75, 37.5)],
}
# semillas de los estados que se reparten el imperio (lon, lat)
CELDAS = {
    "estados": [(106.5, 34.8), (112.3, 38.4), (117.5, 40.3), (118.8, 36.5), (114.8, 35.0), (111.8, 33.6), (114, 30.0)],
    "tres": [(113.5, 37.5), (104, 29.5), (116.5, 28.5)],
    "caudillos": [(117, 39.5), (125, 44), (112.5, 37.5), (103, 36), (86, 43), (88, 31), (104.5, 30.5), (102.5, 25), (113, 23.5), (119.5, 31),
                  (112, 28)],
}

# ------------------------------------------------------------------ datos geográficos de apoyo
RIO_AMARILLO = [(96.5, 34.5), (98.5, 34.6), (100.5, 35.3), (102.3, 34.3), (103.5, 36), (104.6, 36.8), (106.6, 38.3), (108.2, 40.8), (110.3, 40.6),
                (111.5, 39.6), (111, 37), (110.5, 35.3), (112.5, 34.8), (114.3, 34.9), (116.6, 36.4), (118.2, 37.4), (119, 37.8)]
RIO_AZUL = [(91.5, 33.3), (94.5, 32.5), (97.2, 31.2), (99.4, 28.5), (101, 27.3), (102.8, 28), (104.6, 28.8), (106.5, 29.6), (108.6, 30.8),
            (111.3, 30.7), (113.3, 30.4), (114.4, 30.4), (116, 29.8), (117.3, 30.6), (119.4, 32.1), (121.7, 31.7)]
MURALLA_MING = [(98.2, 39.8), (100, 39.2), (102.8, 38.4), (105.8, 38.4), (108, 38.3), (110.5, 39.4), (112.7, 40.2), (114.6, 40.6), (116.1, 40.3),
                (117.8, 40.6), (119.8, 40.1)]
MURALLA_QIN = [(103.2, 35.6), (105, 38.5), (108.5, 41), (111.7, 41.6), (114, 41.4), (117, 41.8), (120, 41.7), (123, 41.3), (124.5, 40.6)]
GRAN_CANAL = [(120.2, 30.3), (120.6, 31.3), (119.4, 32.4), (119, 33.5), (117.2, 34.3), (116.6, 35.4), (116.3, 37), (117.2, 39.1), (116.4, 39.9)]
RUTA_SEDA = [(108.9, 34.3), (103.8, 36.1), (98.5, 39.7), (94.7, 40.1), (89, 42), (84, 41.6), (80, 40), (75.9, 39.5), (72, 39.6), (67, 39.6), (61, 38.5)]
RUTA_ZHENG = [(118.8, 32), (122.2, 30.4), (121, 26), (117, 22.5), (111, 15), (107, 9), (103.5, 3.5), (100, 4.5), (95, 6), (90, 7), (84, 8), (79, 8.5), (75, 11),
              (68, 12), (60, 10)]
CIUDADES = {
    "anyang": (114.3, 36.1), "chang'an": (108.9, 34.3), "luoyang": (112.4, 34.6), "nanjing": (118.8, 32.0), "pekin": (116.4, 39.9),
    "hangzhou": (120.2, 30.3), "cantón": (113.3, 23.1), "hongkong": (114.2, 22.3), "shanghai": (121.5, 31.2), "xianyang": (108.7, 34.4),
    "lintzu": (118.3, 36.8), "chengdu": (104.1, 30.7), "kaifeng": (114.3, 34.8), "wuhan": (114.3, 30.6), "lhasa": (91.1, 29.7),
    "karakorum": (102.8, 47.2), "dadu": (116.4, 39.9), "yangzhou": (119.4, 32.4), "guangzhou": (113.3, 23.1), "tokio": (139.7, 35.7),
}


# ------------------------------------------------------------------ rasterización de los campos
def _anillos(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    return geom["coordinates"]


def _mascara_geom(geoms):
    m = np.zeros((FH, FW), np.uint8)
    for g in geoms:
        for poly in _anillos(g):
            I = [np.rint(proj_pts(r) * 4).astype(np.int32).reshape(-1, 1, 2) for r in poly]
            cv2.fillPoly(m, I, 255, cv2.LINE_8, 2)
    return m


def _sdf(m):
    """Campo de distancia con signo (negativo dentro) de una máscara uint8, suavizado."""
    b = (m > 127).astype(np.uint8)
    din = cv2.distanceTransform(b, cv2.DIST_L2, 5)
    dout = cv2.distanceTransform(1 - b, cv2.DIST_L2, 5)
    s = (dout - din).astype(np.float32)
    return cv2.GaussianBlur(s, (0, 0), 1.6)


_TIERRA_M = None
CAMPOS = {}
GEOMS = {}


def cargar():
    global _TIERRA_M
    if _TIERRA_M is not None:
        return
    land = json.load(open(os.path.join(AQUI, "..", "tesoro_moctezuma", "datos", "ne_50m_land.json"), encoding="utf-8"))
    _TIERRA_M = _mascara_geom([f["geometry"] for f in land["features"]])
    CAMPOS["tierra"] = _sdf(_TIERRA_M)
    paises = json.load(open(os.path.join(AQUI, "datos", "ne_50m_admin_0_countries.geojson"), encoding="utf-8"))
    chn = [f["geometry"] for f in paises["features"] if f["properties"]["NAME"] in ("China", "Hong Kong", "Macao")]
    GEOMS["prc"] = chn
    mp = _mascara_geom(chn)
    CAMPOS["prc"] = _sdf(mp)
    for k, pts in POLI.items():
        m = np.zeros((FH, FW), np.uint8)
        cv2.fillPoly(m, [np.rint(proj_pts(pts) * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
        CAMPOS[k] = _sdf(cv2.bitwise_and(m, _TIERRA_M))
    CAMPOS["tres"] = CAMPOS["tres"]
    # los «caudillos» usan la forma actual
    CAMPOS["rep"] = CAMPOS["prc"]


def celdas(nombre):
    """Mapa de celdas de Voronoi (índice del estado más cercano) y distancia al borde entre celdas, en el campo."""
    if nombre in _CEL:
        return _CEL[nombre]
    seeds = proj_pts(CELDAS[nombre])
    ys, xs = np.mgrid[0:FH:2, 0:FW:2].astype(np.float32)
    d = np.stack([np.hypot(xs - sx, ys - sy) for sx, sy in seeds], 0)
    idx = np.argmin(d, 0).astype(np.uint8)
    ds = np.sort(d, 0)
    borde = ((ds[1] - ds[0]) * 0.5).astype(np.float32) if len(seeds) > 1 else np.full(d.shape[1:], 999, np.float32)
    idx = cv2.resize(idx, (FW, FH), interpolation=cv2.INTER_NEAREST)
    borde = cv2.resize(borde, (FW, FH), interpolation=cv2.INTER_LINEAR)
    _CEL[nombre] = (idx, borde)
    return _CEL[nombre]


_CEL = {}


# ------------------------------------------------------------------ cámara
class Cam:
    """Cámara sobre el campo: centro (lon, lat), zoom (pantalla/campo), giro (rad)."""

    def __init__(self, lon=105.0, lat=36.0, z=1.3, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.lon, self.lat, self.z, self.rot = lon, lat, z, rot
        cx, cy = proj(lon, lat)
        c, s = math.cos(rot) * z, math.sin(rot) * z
        self.M = np.float32([[c, -s, W / 2 - (c * cx - s * cy)], [s, c, H / 2 - (s * cx + c * cy)]])

    def pant(self, lon, lat):
        x, y = proj(lon, lat)
        M = self.M
        return M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]

    def pant_pts(self, P):
        P = np.asarray(P, float)
        x, y = proj(P[:, 0], P[:, 1])
        M = self.M
        return np.stack([M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]], 1)

    def proyectar(self, campo, relleno=200.0):
        return cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)

    @property
    def escala(self):
        return self.z


# ------------------------------------------------------------------ pincel de guache
def _texturas():
    r = np.random.default_rng(7)
    lento = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 12, W // 12)).astype(np.float32), (0, 0), 3), (W, H), interpolation=cv2.INTER_CUBIC)
    trazos = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=16, sigmaY=5.0)
    lento = lento / (lento.std() + 1e-6)
    trazos = trazos / (trazos.std() + 1e-6)
    pincel = (0.020 * lento + 0.007 * trazos).astype(np.float32)
    grano = (B.PAPEL_F / (np.array(B.PAPEL, np.float32) / 255.0)).astype(np.float32)        # grano del papel (~1 ± 0,02)
    # 3 fases de ruido para el temblor del borde (hervor a 12 cuadros/s)
    ruido = []
    for k in range(3):
        n = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 6, W // 6)).astype(np.float32), (0, 0), 1.6), (W, H), interpolation=cv2.INTER_CUBIC)
        ruido.append((n / (n.std() + 1e-6)).astype(np.float32))
    return pincel, grano, ruido


PINCEL, GRANO, RUIDO = _texturas()


_BASE_MAR = None


def fondo_base():
    """Mar pintado a guache sobre el papel (imagen float32 HxWx3, copia nueva en cada llamada)."""
    global _BASE_MAR
    if _BASE_MAR is None:
        img = np.empty((H, W, 3), np.float32)
        img[:] = np.array(MAR, np.float32) / 255.0
        img *= (1 + PINCEL * 1.3)[..., None]
        _BASE_MAR = img * GRANO
    return _BASE_MAR.copy()


from numba import njit, prange            # noqa: E402


@njit(parallel=True, fastmath=True, cache=True)
def _pintar_nb(img, S, nz, pincel, grano, col, alfa, sombra, borde, amp, y0, y1, x0, x1):
    h, w = S.shape
    for y in prange(y0, y1):
        for x in range(x0, x1):
            s = S[y, x] + amp * nz[y, x]
            if s > 2.0:
                continue
            a = 0.5 - s * 0.7692
            if a <= 0.0:
                continue
            if a > 1.0:
                a = 1.0
            a *= alfa
            d = -s * (1.0 / 26.0)
            if d < 0.0:
                d = 0.0
            if d > 1.0:
                d = 1.0
            lum = 1.0 - 0.07 * (1.0 - d) * borde
            if d < 1.0:
                xm = x - 1 if x > 0 else 0
                xp = x + 1 if x < w - 1 else w - 1
                ym = y - 1 if y > 0 else 0
                yp = y + 1 if y < h - 1 else h - 1
                gx = S[y, xp] - S[y, xm]
                gy = S[yp, x] - S[ym, x]
                nr = np.sqrt(gx * gx + gy * gy) + 1e-6
                sh = (gx * 0.55 + gy * 0.83) / nr
                band = (1.0 - d) * (1.0 - d)
                if sh > 0.0:
                    lum -= sombra * sh * band
                else:
                    lum -= 0.10 * sh * band
            k = lum * (1.0 + 1.2 * pincel[y, x])
            for c in range(3):
                pig = col[c] * k * grano[y, x, c]
                img[y, x, c] = img[y, x, c] * (1.0 - a) + pig * a


@njit(parallel=True, fastmath=True, cache=True)
def _halo_nb(img, S, col, fuerza, ancho, y0, y1, x0, x1):
    for y in prange(y0, y1):
        for x in range(x0, x1):
            s = S[y, x]
            if s <= 0.0 or s >= ancho:
                continue
            t = 1.0 - s / ancho
            hh = t * t * fuerza
            for c in range(3):
                img[y, x, c] = img[y, x, c] * (1.0 - hh) + col[c] * hh


def _roi(S, margen=24):
    m = S[::8, ::8] < 3.0
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        return None
    return (max(0, ys.min() * 8 - margen), min(H, ys.max() * 8 + 8 + margen), max(0, xs.min() * 8 - margen), min(W, xs.max() * 8 + 8 + margen))


def pintar(img, S, color, alfa=1.0, fase=0, borde=1.0, sombra=0.24, ruido=1.0):
    """Pinta la forma de campo S (pantalla, negativo dentro) con `color` (0-255) a guache sobre `img` (float32 0-1)."""
    r = _roi(S)
    if r is None:
        return
    col = (np.array(color, np.float32) / 255.0)
    _pintar_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, col, np.float32(alfa), np.float32(sombra), np.float32(borde),
               np.float32(1.5 * ruido), r[0], r[1], r[2], r[3])


def pintar_tierra(img, cam, fase=0):
    """Tierra firme: arena con orilla clara en el mar (ola de acuarela) y media luna de sombra."""
    S = cam.proyectar(CAMPOS["tierra"])
    # halo claro en el agua junto a la costa (S > 0 = mar)
    _halo_nb(img, S, np.array(MAR_CL, np.float32) / 255.0, np.float32(0.6), np.float32(34.0), 0, H, 0, W)
    pintar(img, S, TIERRA, 1.0, fase, sombra=0.16)
    return S


def pintar_campo(img, cam, S_campo, color, alfa=1.0, fase=0):
    S = cam.proyectar(S_campo)
    pintar(img, S, color, alfa, fase)
    return S


def mezcla_campos(a, b, k):
    """Interpola dos campos de distancia: el imperio crece o se encoge sin saltos."""
    k = float(min(1.0, max(0.0, k)))
    if k <= 0:
        return CAMPOS[a]
    if k >= 1:
        return CAMPOS[b]
    return cv2.addWeighted(CAMPOS[a], 1 - k, CAMPOS[b], k, 0)
