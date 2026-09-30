# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Irán en 5 minutos».

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
LON0, LON1, LAT0, LAT1 = 18.0, 82.0, 52.0, 8.0
PXLAT = 26.0                                  # píxeles de campo por grado de latitud
KX = math.cos(math.radians(30.0))
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
    "meseta": (206, 176, 128), "elam": (196, 120, 92), "medos": (122, 160, 104), "persis": (238, 178, 64), "aquemenida": (150, 100, 160),
    "alejandro": (196, 84, 84), "diadocos": (196, 84, 84), "partos": (214, 130, 70), "sasanidas": (70, 144, 146), "califato": (96, 150, 100),
    "mongol": (96, 134, 184), "safavidas": (58, 130, 186), "qayar": (190, 104, 92), "iran": (92, 150, 110), "pahlavi": (170, 136, 170),
}
COL_CELDAS = [(206, 98, 72), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
              (140, 120, 190), (180, 160, 90), (110, 170, 170)]


# ------------------------------------------------------------------ geometrías de las épocas (lon, lat). El lado del mar es
# generoso porque cada época se recorta con la tierra firme.
POLI = {
    "elam": [(46.5, 34), (47, 31), (48, 29), (50.5, 28.6), (52, 29.6), (51.8, 32), (50, 33.6), (48, 34.3)],
    "medos": [(44, 35), (44.3, 37.3), (46, 38.8), (49, 38.6), (52.5, 38.3), (56, 37.4), (56.5, 35), (54, 33.6), (50.5, 33), (48, 33.2), (45.5, 33.6)],
    "persis": [(50, 27.5), (49.8, 30.2), (51.8, 31.8), (54.6, 31.8), (57, 29.6), (57.2, 27), (54, 26.8)],
    "lidia": [(26, 36.3), (26, 40.6), (30, 41.2), (36, 41.2), (38.5, 39), (38.5, 36.6), (33, 36.3)],
    # Medos + Persis unidos
    "medo_persa": [(44, 35), (44.3, 37.3), (46, 38.8), (49, 38.6), (52.5, 38.3), (56, 37.4), (57.2, 34), (58, 29), (57.2, 26.6), (54, 26.4), (50.5, 27),
                   (49, 29), (47.5, 31), (45.5, 33.6)],
    # Imperio de Ciro: medos + persas + Lidia + Babilonia + Asia central
    "ciro": [(26, 37.5), (26.5, 40.5), (31, 41.5), (37, 41.3), (41, 41), (45, 40), (48, 40.5), (52, 39.3), (56, 39), (60, 38.2), (65, 39.8), (69, 40),
             (70, 37), (68, 34), (66, 30), (63, 26), (58, 25), (56, 26.5), (52, 27.5), (49.5, 29), (48, 29), (47, 29), (44, 29.8), (40, 30.8),
             (37, 31.5), (35.5, 32.5), (35.5, 35.5), (36.2, 36.5), (34, 36.3), (30, 36.4), (27.5, 36.6)],
    # Imperio de Darío: de Egipto al Indo
    "dario": [(20.5, 32.8), (24.5, 32.5), (28, 31.3), (32, 31.3), (34.3, 31.3), (35.2, 33), (35.8, 35), (36.4, 36.5), (33, 36.3), (30, 36.5),
              (27.5, 36.8), (26.5, 38.5), (26, 40.2), (24, 40.8), (22.5, 41.2), (26, 42), (31, 42), (37, 41.5), (41, 41.5), (45, 42), (48, 41.5),
              (51, 41), (53, 42), (55.5, 43), (58, 44.5), (61, 44.5), (64, 43), (68, 42.5), (72, 42.5), (74.5, 40.5), (75, 37), (74, 34), (74.5, 31),
              (73, 27.5), (71, 24), (68, 23.5), (66, 25), (62, 25), (58, 25), (56.5, 26.3), (54, 26.7), (51, 27.3), (49, 29), (48, 29.5),
              (44.5, 29), (42, 28.5), (39, 28.5), (36, 29), (34.5, 27.5), (34, 24.5), (32.5, 22.3), (25, 22), (24.8, 29), (24.5, 31.3), (22, 32.2)],
    # Imperio de Alejandro: Grecia, Egipto, Persia y el Punjab
    "alejandro": [(20, 32.6), (24.5, 32.5), (28, 31.3), (32, 31.3), (34.3, 31.3), (35.2, 33), (35.8, 35), (36.4, 36.5), (33, 36.3), (30, 36.5),
                  (27.5, 36.8), (26.5, 38), (22, 36.3), (20.5, 38), (19.6, 41), (20, 42.5), (23, 43), (26, 42), (31, 42), (37, 41.5), (41, 41.5),
                  (45, 42), (48, 41.5), (51, 41), (53, 42), (55.5, 43), (58, 44.5), (61, 44.5), (64, 43), (68, 42.5), (72, 42.5), (75, 40.5), (76, 37),
                  (75.5, 34), (76.5, 31.5), (75, 28), (72, 24), (68, 23.5), (66, 25), (62, 25), (58, 25), (56.5, 26.3), (54, 26.7), (51, 27.3),
                  (49, 29), (48, 29.5), (44.5, 29), (42, 28.5), (39, 28.5), (36, 29), (34.5, 27.5), (34, 24.5), (32.5, 22.3), (25, 22), (24.8, 29)],
    "partos": [(38, 35), (38, 37.3), (41, 38), (44, 40), (48, 40), (52, 38.5), (56, 38.5), (60, 38), (63, 39), (66, 38.5), (68, 37), (68, 33),
               (67, 29), (66, 25), (62, 25), (58, 25.5), (56, 26.5), (52, 27.5), (49, 29), (47.5, 30), (44, 29), (42, 30.5), (40, 33)],
    "sasanidas": [(38, 34), (38, 37), (40, 38), (42, 40), (44, 41.5), (48, 42), (50, 41), (52, 39.5), (55, 39), (58, 38), (62, 38.3), (66, 38),
                  (69, 38.3), (70, 36), (70, 32), (68, 28), (66, 25), (62, 24.5), (58, 23.5), (56, 24.5), (53, 24), (51, 24.5), (48, 26.5), (47, 29.5),
                  (44, 28.5), (41, 30), (39, 32)],
    "califato": [(17, 32), (24, 33), (30, 31.8), (34, 33), (36, 36.6), (33, 36.4), (29, 36.6), (34, 37.2), (38, 37.4), (42, 38), (44, 39.6), (48, 39.8),
                 (54, 38.6), (60, 37.8), (66, 37.6), (70, 36), (70, 30), (67, 24.5), (62, 24.5), (57, 24), (59, 22), (56, 17), (52, 14.5), (45, 12.5),
                 (43, 12.3), (42, 13.5), (38, 18), (34, 22), (25, 22), (17, 22)],
    "mongol": [(50, 34), (50, 40), (54, 44), (60, 47), (70, 52), (82, 52), (82, 34), (72, 28), (66, 30), (60, 32), (54, 33)],
    "ilkanato": [(44, 29.5), (42, 32), (40, 35), (37.5, 37.5), (40, 40), (44, 41.5), (48, 41.5), (52, 39.5), (56, 39), (61, 38.3), (66, 38), (70, 36),
                 (69, 32), (66, 28), (63, 25), (58, 24.5), (54, 26), (50, 28), (48, 28.5)],
    "safavidas": [(42, 37), (43, 40), (44.5, 41.7), (48, 42), (50, 40.5), (53, 39.5), (56, 38.5), (61, 37.5), (64, 35), (66, 32.5), (66, 29), (62, 25),
                  (57, 25), (54, 26.5), (50.5, 27.5), (49, 30), (46, 31.5), (44, 33), (42, 35)],
}
# semillas de los estados en que se parte un territorio (lon, lat)
CELDAS = {
    "gancho": [(30.5, 27.5), (32, 39), (43.5, 33), (53, 33.5), (64, 38.5), (70, 29), (51.5, 28)],
    "diadocos": [(22.5, 40.3), (30, 27), (37.5, 35.5), (50, 34.5), (67, 38), (73, 31)],
    "cierre": [(47.5, 35.5), (53.5, 36.5), (58, 35), (45.5, 31), (52, 29.5), (56, 28), (60, 31)],
}

# ------------------------------------------------------------------ datos geográficos de apoyo
CAMINO_REAL = [(26.0, 38.5), (29.5, 38.9), (33.0, 39.6), (36.0, 39.3), (38.5, 38.4), (41.0, 37.5), (43.15, 36.3), (44.4, 35.5), (45.8, 34.5),
               (47.2, 33.0), (48.25, 32.2)]
RUTA_ALEJANDRO = [(24.0, 40.5), (26.4, 40.1), (32.0, 38.0), (36.6, 36.8), (43.4, 36.6), (44.4, 32.5), (48.2, 32.2), (52.9, 29.9), (56.0, 36.0),
                  (62.0, 36.0), (67.0, 36.7), (72.0, 34.0)]
RUTA_ARABE = [(39.8, 21.4), (42.0, 27.0), (44.4, 32.0), (44.6, 33.1), (48.4, 34.2), (54.0, 35.5), (62.2, 37.6)]
RUTA_MONGOL = [(80.0, 45.0), (72.0, 41.0), (67.0, 39.6), (62.0, 37.6), (58.8, 36.2), (52.0, 36.0), (48.0, 35.0), (44.36, 33.3)]
RUTA_NADER = [(59.6, 36.3), (63.0, 34.6), (65.7, 31.6), (68.0, 33.0), (69.2, 34.5), (72.0, 33.8), (75.0, 31.6), (77.2, 28.6)]
RUTA_PETROLEO = [(49.3, 32.0), (48.3, 30.3), (50.5, 28.0), (55.0, 26.0)]
CIUDADES = {
    "susa": (48.25, 32.19), "persepolis": (52.89, 29.93), "pasargada": (53.17, 30.2), "ecbatana": (48.5, 34.8), "babilonia": (44.42, 32.54),
    "sardes": (26.0, 38.5), "ctesifonte": (44.58, 33.09), "isfahan": (51.67, 32.65), "teheran": (51.39, 35.69), "mashhad": (59.6, 36.3),
    "bagdad": (44.36, 33.31), "delhi": (77.2, 28.6), "samarcanda": (66.96, 39.65), "tabriz": (46.3, 38.08), "nishapur": (58.8, 36.2),
    "mecca": (39.8, 21.4), "ninive": (43.15, 36.36), "atenas": (23.7, 37.98), "carras": (39.03, 36.87), "alejandria": (29.9, 31.2),
    "gaugamela": (43.4, 36.6), "maraton": (23.96, 38.15), "masyed": (49.3, 32.0), "tesifonte": (44.58, 33.09), "egipto": (31.2, 30.0),
    "indo": (72.0, 30.0), "persia": (53.0, 30.5), "cairo": (31.2, 30.0), "moscu": (37.6, 55.0), "londres": (-0.1, 51.5),
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
    for clave, nombres in (("iran", ("Iran",)), ("irak", ("Iraq",))):
        g = [f["geometry"] for f in paises["features"] if f["properties"]["NAME"] in nombres]
        GEOMS[clave] = g
        CAMPOS[clave] = _sdf(_mascara_geom(g))
    # la meseta iraní es el país actual un poco ensanchado (pintada en color tierra)
    CAMPOS["meseta"] = CAMPOS["iran"]
    for k, pts in POLI.items():
        m = np.zeros((FH, FW), np.uint8)
        cv2.fillPoly(m, [np.rint(proj_pts(pts) * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
        CAMPOS[k] = _sdf(cv2.bitwise_and(m, _TIERRA_M))
    CAMPOS["qayar"] = CAMPOS["iran"]
    CAMPOS["pahlavi"] = CAMPOS["iran"]


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
