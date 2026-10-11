# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Roma en 5 minutos».

Campos de distancia con signo (SDF, negativo = dentro) rasterizados sobre una rejilla
lon/lat del Mediterráneo y Europa. Cada cuadro se interpolan los campos de dos épocas,
se proyectan con la cámara (`Cam`) y se pintan con textura de guache.
"""
import json
import math
import os

import cv2
import numpy as np

import boceto as B
from motor import H, W, clamp01, lerp, prog

AQUI = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ proyección (Mediterráneo, Europa y Oriente Próximo)
LON0, LON1, LAT0, LAT1 = -28.0, 68.0, 68.0, 16.0
PXLAT = 26.0
KX = math.cos(math.radians(42.0))
FW = int((LON1 - LON0) * KX * PXLAT)
FH = int((LAT0 - LAT1) * PXLAT)


def proj(lon, lat):
    """lon/lat -> píxeles del campo."""
    return (np.asarray(lon, float) - LON0) * KX * PXLAT, (LAT0 - np.asarray(lat, float)) * PXLAT


def proj_pts(P):
    P = np.asarray(P, float)
    x, y = proj(P[:, 0], P[:, 1])
    return np.stack([x, y], 1)


# ------------------------------------------------------------------ paleta de guache
MAR = (186, 214, 216)
MAR_CL = (206, 228, 226)
TIERRA = (234, 222, 192)
TIERRA_OSC = (214, 198, 160)

COL = {
    "lacio": (210, 110, 80), "italia": (196, 75, 65), "cartago": (110, 140, 180),
    "punicas": (205, 70, 60), "mediterraneo": (190, 65, 55), "cesar": (180, 55, 50),
    "imperio": (175, 45, 45), "maxima": (170, 40, 40), "occidente": (160, 60, 80),
    "oriente": (80, 120, 160), "barbaros": (120, 140, 110),
}

COL_CELDAS = [
    (196, 75, 65), (110, 140, 180), (120, 160, 100), (220, 160, 60),
    (150, 90, 130), (80, 130, 150), (190, 110, 50), (130, 110, 170),
]

# ------------------------------------------------------------------ geometrías de las épocas (lon, lat)
POLI = {
    # 1. Lacio: orígenes en las 7 colinas
    "lacio": [
        (11.8, 41.3), (12.0, 42.5), (13.2, 42.5), (13.5, 41.5), (12.5, 41.2)
    ],
    # 2. Italia: península itálica unificada
    "italia": [
        (6.5, 44.0), (7.0, 46.0), (12.0, 46.8), (14.0, 46.0), (16.0, 42.0),
        (19.0, 40.0), (18.5, 39.0), (16.5, 37.5), (14.5, 36.0), (12.0, 36.5),
        (11.5, 38.5), (9.0, 44.0)
    ],
    # 3. Cartago (África del norte)
    "cartago": [
        (6.0, 37.5), (12.5, 37.5), (15.5, 33.0), (15.0, 31.0), (9.0, 31.5),
        (6.0, 35.0)
    ],
    # 4. Fin de las Guerras Púnicas: Italia + Sicilia + Cerdeña + costa este de Hispania
    "punicas": [
        (-7.0, 35.5), (-7.0, 38.0), (-3.0, 40.5), (0.0, 42.5), (3.5, 43.0),
        (7.0, 44.0), (9.0, 44.5), (14.0, 46.5), (16.5, 41.2), (19.0, 40.0),
        (16.5, 37.5), (14.5, 36.0), (12.0, 36.5), (8.0, 38.5), (8.0, 42.5),
        (-2.0, 37.0), (-6.0, 35.5)
    ],
    # 5. Mare Nostrum: todo el anillo del Mediterráneo
    "mediterraneo": [
        (-15.0, 32.0), (-15.0, 45.0), (0.0, 43.5), (5.0, 44.5), (10.0, 46.5),
        (18.0, 45.5), (25.0, 42.0), (29.5, 42.0), (36.0, 41.0), (37.0, 36.0),
        (36.5, 31.0), (32.5, 30.5), (31.0, 29.5), (28.0, 30.5), (24.0, 31.5),
        (20.0, 30.5), (16.0, 30.5), (13.0, 31.5), (10.5, 32.5), (8.5, 34.5),
        (5.0, 34.8), (0.0, 34.2), (-5.0, 33.5), (-9.5, 30.5), (-15.0, 30.5)
    ],
    # 6. Conquista de las Galias (Julio César)
    "cesar": [
        (-15.0, 32.0), (-15.0, 49.5), (-5.0, 50.0), (2.0, 51.5), (4.1, 52.0),
        (7.6, 50.4), (8.3, 49.5), (8.2, 48.0), (10.0, 46.5), (18.0, 45.5),
        (25.0, 42.0), (29.5, 42.0), (36.0, 41.0), (37.0, 36.0), (36.5, 31.0),
        (32.5, 30.5), (31.0, 29.5), (28.0, 30.5), (24.0, 31.5), (20.0, 30.5),
        (16.0, 30.5), (13.0, 31.5), (10.5, 32.5), (8.5, 34.5), (5.0, 34.8),
        (0.0, 34.2), (-5.0, 33.5), (-9.5, 30.5), (-15.0, 30.5)
    ],
    # 7. Pax Romana (Augusto: frontera en Rin y Danubio, Egipto entero)
    "imperio": [
        (-15.0, 32.0), (-15.0, 49.5), (-5.0, 50.0), (2.0, 51.5), (4.1, 52.0),
        (7.6, 50.4), (8.3, 49.5), (8.2, 48.0), (10.5, 48.7), (12.1, 49.0),
        (14.0, 48.5), (16.4, 48.2), (19.0, 47.5), (20.5, 44.8), (22.5, 44.6),
        (28.0, 45.2), (29.6, 45.3), (38.0, 42.0), (41.5, 41.5), (42.0, 40.5),
        (40.8, 38.5), (39.2, 37.0), (37.5, 35.8), (36.5, 33.5), (35.5, 31.5),
        (35.0, 29.0), (33.5, 28.0), (32.0, 27.0), (30.0, 27.0), (27.0, 29.5),
        (24.0, 31.5), (20.0, 30.5), (16.0, 30.5), (13.0, 31.5), (10.5, 32.5),
        (8.5, 34.5), (5.0, 34.8), (0.0, 34.2), (-5.0, 33.5), (-9.5, 30.5),
        (-15.0, 30.5)
    ],
    # 8. Máxima extensión (Trajano 117 d.C.: Britania, Dacia, Armenia, Mesopotamia y Arabia)
    "maxima": [
        (-15.0, 32.0), (-15.0, 55.5), (-3.5, 55.5), (0.0, 55.5), (1.5, 53.0),
        (4.1, 52.0), (7.6, 50.4), (8.3, 49.5), (8.2, 48.0), (10.5, 48.7),
        (12.1, 49.0), (14.0, 48.5), (16.4, 48.2), (19.0, 47.5), (20.5, 44.8),
        (22.5, 44.6), (21.5, 46.5), (23.5, 47.8), (26.0, 47.8), (27.5, 46.5),
        (28.5, 45.5), (29.6, 45.3), (38.0, 42.0), (41.5, 42.0), (44.5, 40.5),
        (46.0, 39.0), (45.5, 36.5), (46.5, 34.0), (48.0, 31.5), (48.5, 30.0),
        (47.0, 30.5), (45.0, 31.8), (42.5, 33.5), (39.5, 34.8), (37.5, 33.0),
        (36.5, 31.0), (35.5, 29.0), (33.5, 28.0), (32.0, 27.0), (30.0, 27.0),
        (27.0, 29.5), (24.0, 31.5), (20.0, 30.5), (16.0, 30.5), (13.0, 31.5),
        (10.5, 32.5), (8.5, 34.5), (5.0, 34.8), (0.0, 34.2), (-5.0, 33.5),
        (-9.5, 30.5), (-15.0, 30.5)
    ],
    # 9. Imperio Romano de Occidente (395 d.C.)
    "occidente": [
        (-15.0, 32.0), (-15.0, 55.5), (-3.5, 55.5), (0.0, 55.5), (1.5, 53.0),
        (4.1, 52.0), (7.6, 50.4), (8.3, 49.5), (8.2, 48.0), (10.5, 48.7),
        (12.1, 49.0), (14.0, 48.5), (16.4, 48.2), (19.0, 45.0), (19.0, 42.0),
        (16.5, 38.0), (12.0, 37.0), (11.5, 31.5), (8.5, 34.5), (5.0, 34.8),
        (0.0, 34.2), (-5.0, 33.5), (-9.5, 30.5), (-15.0, 30.5)
    ],
    # 10. Imperio Romano de Oriente / Bizancio (395 d.C.)
    "oriente": [
        (19.0, 45.0), (20.5, 44.8), (22.5, 44.6), (28.0, 45.2), (29.6, 45.3),
        (38.0, 42.0), (41.5, 41.5), (42.0, 40.5), (40.8, 38.5), (39.2, 37.0),
        (37.5, 35.8), (36.5, 33.5), (35.5, 31.5), (35.0, 29.0), (33.5, 28.0),
        (32.0, 27.0), (30.0, 27.0), (27.0, 29.5), (24.0, 31.5), (20.0, 30.5),
        (18.5, 30.5), (18.5, 32.5), (20.0, 35.0), (19.0, 38.0), (19.0, 42.0)
    ],
}

# Semillas para Voronoi (división territorial y caudillos/bárbaros)
CELDAS = {
    "barbaros": [
        (-3.0, 40.0), (2.0, 46.5), (12.0, 43.0), (22.0, 40.0),
        (32.0, 39.0), (30.0, 29.0), (8.0, 34.0)
    ],
    "division": [
        (4.0, 44.0), (12.5, 42.0), (24.0, 39.0), (33.0, 35.0)
    ],
}

# ------------------------------------------------------------------ geografía y referencias
RIO_TIBER = [(12.0, 43.8), (12.3, 43.2), (12.5, 42.5), (12.49, 41.9), (12.25, 41.74)]
RIO_RIN = [(9.5, 47.5), (7.6, 48.5), (8.3, 49.5), (7.6, 50.4), (6.9, 51.2), (5.5, 51.9), (4.1, 52.0)]
RIO_DANUBIO = [(8.2, 48.0), (12.1, 49.0), (16.4, 48.2), (19.0, 47.5), (20.5, 44.8), (22.5, 44.6), (28.0, 45.2), (29.6, 45.3)]
RIO_NILO = [(31.2, 30.0), (31.3, 29.0), (32.0, 27.0), (32.6, 25.7), (32.9, 24.1)]
VIA_APIA = [(12.49, 41.90), (13.0, 41.5), (13.7, 41.3), (14.25, 40.85), (15.0, 41.1), (16.8, 40.8), (17.9, 40.6)]

CIUDADES = {
    "roma": (12.49, 41.90), "cartago": (10.32, 36.85), "atenas": (23.73, 37.98),
    "alejandria": (29.92, 31.20), "constantinopla": (28.98, 41.01), "antioquia": (36.16, 36.20),
    "londres": (-0.12, 51.51), "tarraco": (1.25, 41.12), "lutecia": (2.35, 48.85),
    "siracusa": (15.28, 37.07), "ravena": (12.20, 44.42),
}

# ------------------------------------------------------------------ rasterización de campos
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
    """Campo de distancia con signo (negativo dentro) de una máscara uint8."""
    b = (m > 127).astype(np.uint8)
    din = cv2.distanceTransform(b, cv2.DIST_L2, 5)
    dout = cv2.distanceTransform(1 - b, cv2.DIST_L2, 5)
    s = (dout - din).astype(np.float32)
    return cv2.GaussianBlur(s, (0, 0), 1.6)


_TIERRA_M = None
CAMPOS = {}
GEOMS = {}
_CEL = {}


def cargar():
    global _TIERRA_M
    if _TIERRA_M is not None:
        return
    land_path = os.path.join(AQUI, "datos", "ne_50m_land.json")
    if not os.path.exists(land_path):
        land_path = os.path.join(AQUI, "..", "tesoro_moctezuma", "datos", "ne_50m_land.json")
    land = json.load(open(land_path, encoding="utf-8"))
    _TIERRA_M = _mascara_geom([f["geometry"] for f in land["features"]])
    CAMPOS["tierra"] = _sdf(_TIERRA_M)

    for k, pts in POLI.items():
        m = np.zeros((FH, FW), np.uint8)
        cv2.fillPoly(m, [np.rint(proj_pts(pts) * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
        CAMPOS[k] = _sdf(cv2.bitwise_and(m, _TIERRA_M))


def celdas(nombre):
    """Mapa de celdas de Voronoi."""
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


# ------------------------------------------------------------------ cámara
class Cam:
    def __init__(self, lon=12.5, lat=42.0, z=1.3, rot=0.0):
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


# ------------------------------------------------------------------ texturas y pintura guache
def _texturas():
    r = np.random.default_rng(7)
    lento = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 12, W // 12)).astype(np.float32), (0, 0), 3), (W, H), interpolation=cv2.INTER_CUBIC)
    trazos = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=16, sigmaY=5.0)
    lento = lento / (lento.std() + 1e-6)
    trazos = trazos / (trazos.std() + 1e-6)
    pincel = (0.020 * lento + 0.007 * trazos).astype(np.float32)
    grano = (B.PAPEL_F / (np.array(B.PAPEL, np.float32) / 255.0)).astype(np.float32)
    ruido = []
    for k in range(3):
        n = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 6, W // 6)).astype(np.float32), (0, 0), 1.6), (W, H), interpolation=cv2.INTER_CUBIC)
        ruido.append((n / (n.std() + 1e-6)).astype(np.float32))
    return pincel, grano, ruido


PINCEL, GRANO, RUIDO = _texturas()
_BASE_MAR = None


def fondo_base():
    """Mar pintado a guache sobre el papel."""
    global _BASE_MAR
    if _BASE_MAR is None:
        img = np.empty((H, W, 3), np.float32)
        img[:] = np.array(MAR, np.float32) / 255.0
        img *= (1 + PINCEL * 1.3)[..., None]
        _BASE_MAR = img * GRANO
    return _BASE_MAR.copy()


from numba import njit, prange  # noqa: E402


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
    return (max(0, ys.min() * 8 - margen), min(H, ys.max() * 8 + 8 + margen),
            max(0, xs.min() * 8 - margen), min(W, xs.max() * 8 + 8 + margen))


def pintar(img, S, color, alfa=1.0, fase=0, borde=1.0, sombra=0.24, ruido=1.0):
    """Pinta la forma de campo S con `color` a guache sobre `img`."""
    r = _roi(S)
    if r is None:
        return
    col = (np.array(color, np.float32) / 255.0)
    _pintar_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, col, np.float32(alfa), np.float32(sombra),
               np.float32(borde), np.float32(1.5 * ruido), r[0], r[1], r[2], r[3])


def pintar_tierra(img, cam, fase=0):
    """Tierra firme con oleaje claro en la costa."""
    S = cam.proyectar(CAMPOS["tierra"])
    _halo_nb(img, S, np.array(MAR_CL, np.float32) / 255.0, np.float32(0.6), np.float32(34.0), 0, H, 0, W)
    pintar(img, S, TIERRA, 1.0, fase, sombra=0.16)
    return S


def pintar_campo(img, cam, S_campo, color, alfa=1.0, fase=0):
    S = cam.proyectar(S_campo)
    pintar(img, S, color, alfa, fase)
    return S


def mezcla_campos(a, b, k):
    """Interpola dos campos de distancia."""
    k = float(min(1.0, max(0.0, k)))
    if k <= 0:
        return CAMPOS[a]
    if k >= 1:
        return CAMPOS[b]
    return CAMPOS[a] * (1.0 - k) + CAMPOS[b] * k
