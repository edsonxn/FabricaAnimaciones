# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Japón en 5 minutos».

Campos de distancia con signo (SDF, negativo = dentro) rasterizados una vez por proceso sobre una rejilla lon/lat («campo»).
Cada cuadro se interpolan los campos de dos épocas (el territorio crece, se parte y se reúne), se proyectan a pantalla con la
cámara (`Cam`) y se pintan con pincel de guache. Después la escena dibuja encima tinta y crayón (boceto).
"""
import json
import math
import os

import cv2
import numpy as np

import boceto as B
from motor import H, W, clamp01, lerp, prog

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS_IRAN = os.path.join(AQUI, "..", "historia_iran", "datos")

# ------------------------------------------------------------------ proyección (rectangular con coseno de latitud medio)
LON0, LON1, LAT0, LAT1 = 117.0, 152.0, 49.0, 22.0
PXLAT = 34.0                                  # píxeles de campo por grado de latitud
KX = math.cos(math.radians(35.0))
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
    "jomon": (122, 160, 104), "yayoi": (238, 178, 64), "yamato": (196, 84, 84), "heian": (150, 100, 160), "shogun": (70, 144, 146),
    "sengoku": (214, 130, 70), "tokugawa": (58, 130, 186), "meiji": (206, 98, 72), "imperio": (196, 60, 60), "ocupado": (170, 136, 170),
    "japon": (92, 150, 110), "corea": (238, 178, 64), "mongol": (96, 134, 184), "rusia": (190, 104, 92),
}
COL_CELDAS = [(206, 98, 72), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
              (140, 120, 190), (180, 160, 90), (110, 170, 170)]


# ------------------------------------------------------------------ geometrías de épocas (lon, lat); se recortan con Japón/tierra
POLI = {
    "yayoi": [(129.0, 32.6), (132.4, 32.6), (132.4, 33.97), (129.0, 33.97)],
    "yamato": [(129.0, 30.5), (129.0, 33.97), (131.8, 34.6), (132.4, 35.6), (136.6, 36.0), (137.0, 33.0), (132.6, 30.5)],
    "yamato_exp": [(129.0, 30.0), (129.0, 34.0), (131.0, 35.8), (136.0, 37.3), (138.4, 36.4), (138.2, 33.0), (132.6, 30.0)],
    "heian": [(129.0, 30.0), (129.0, 34.0), (131.0, 36.0), (136.0, 38.0), (138.4, 39.4), (141.4, 39.0), (141.4, 35.0), (140.8, 34.2), (137.0, 33.0),
              (133.0, 30.0)],
    "kanto": [(138.6, 34.5), (138.6, 37.0), (141.2, 37.0), (141.2, 34.5)],
    "honshu_sur": [(129.0, 30.0), (129.0, 34.0), (131.0, 36.0), (136.0, 38.0), (139.0, 41.3), (142.3, 41.3), (142.3, 35.0), (137.0, 33.0), (133.0, 30.0)],
    "sin_hokkaido": [(128.5, 29.0), (128.5, 38.0), (133.0, 38.0), (139.0, 41.3), (142.5, 41.3), (142.5, 29.0)],
    "hokkaido": [(139.0, 41.35), (139.0, 46.5), (146.5, 46.5), (146.5, 41.35)],
    "manchuria": [(119.0, 41.5), (119.0, 49.0), (135.0, 49.0), (135.0, 43.0), (131.0, 42.6), (126.5, 41.3), (124.3, 39.8)],
    "karafuto": [(141.0, 46.0), (141.0, 49.0), (144.5, 49.0), (144.5, 46.0)],
    "kyushu": [(129.0, 30.0), (129.0, 33.97), (132.3, 33.97), (132.3, 30.0)],
    "kinai": [(134.4, 34.0), (134.4, 35.7), (136.6, 35.7), (136.6, 34.0)],
}
# semillas de los estados en que se parte el país (lon, lat)
CELDAS = {
    "sengoku": [(130.6, 32.6), (133.0, 34.2), (135.3, 34.9), (137.0, 35.2), (139.0, 36.0), (140.4, 38.2), (132.4, 35.1), (141.0, 40.6)],
    "clanes": [(131.0, 33.0), (133.5, 34.4), (135.5, 35.2), (138.5, 35.5), (140.5, 37.5), (140.6, 35.8)],
}

# ------------------------------------------------------------------ datos geográficos de apoyo
RUTA_MONGOL = [(128.6, 35.1), (129.2, 34.45), (129.9, 33.85), (130.35, 33.62)]
RUTA_PERRY = [(151.0, 29.5), (146.0, 32.0), (141.5, 34.2), (139.9, 35.05), (139.72, 35.25)]
RUTA_PORTUGUESES = [(122.0, 24.5), (126.0, 27.0), (129.0, 29.8), (131.0, 30.55)]
RUTA_PACIFICO = [(141.5, 34.5), (146.0, 31.5), (151.5, 28.0)]
RUTA_COREA = [(127.0, 37.5), (129.5, 35.5), (131.3, 34.2), (135.0, 34.6)]
RUTA_SEKIGAHARA = [(139.69, 35.69), (138.0, 35.4), (136.46, 35.36)]
CIUDADES = {
    "kioto": (135.77, 35.01), "nara": (135.80, 34.68), "osaka": (135.50, 34.69), "tokio": (139.69, 35.69), "edo": (139.69, 35.69),
    "kamakura": (139.55, 35.32), "hakata": (130.40, 33.60), "nagasaki": (129.87, 32.75), "hiroshima": (132.46, 34.39), "yokohama": (139.64, 35.44),
    "sekigahara": (136.46, 35.36), "tanegashima": (131.0, 30.6), "seul": (126.98, 37.56), "mukden": (123.4, 41.8), "pearl": (152.0, 28.0),
    "sakai": (135.49, 34.56), "nagoya": (136.9, 35.18), "azuchi": (136.14, 35.15), "honnoji": (135.76, 35.01), "sapporo": (141.35, 43.06),
    "dejima": (129.87, 32.75), "kagoshima": (130.56, 31.6), "shimonoseki": (130.94, 33.95), "busan": (129.04, 35.18), "taipei": (121.56, 25.04),
    "yamato": (135.8, 34.5), "kanto": (139.7, 36.0), "uraga": (139.72, 35.25), "fuji": (138.73, 35.36), "hokkaido": (142.8, 43.3),
    "tsushima": (129.3, 34.45), "pekin": (116.4, 39.9), "manchuria": (125.0, 44.0),
}


# ------------------------------------------------------------------ rasterización de los campos
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
    paises = json.load(open(os.path.join(DATOS_IRAN, "ne_50m_admin_0_countries.geojson"), encoding="utf-8"))
    for clave, nombres in (("japon", ("Japan",)), ("corea_sur", ("South Korea",)), ("corea_nor", ("North Korea",)), ("taiwan", ("Taiwan",))):
        g = [f["geometry"] for f in paises["features"] if f["properties"]["NAME"] in nombres]
        GEOMS[clave] = g
        CAMPOS[clave] = _sdf(_mascara_geom(g))
    m_jp = _mascara_geom(GEOMS["japon"])
    m_corea = cv2.bitwise_or(_mascara_geom(GEOMS["corea_sur"]), _mascara_geom(GEOMS["corea_nor"]))
    CAMPOS["corea"] = _sdf(m_corea)
    # regiones de Japón = polígono ∧ país; territorios del imperio = polígono ∧ tierra
    for k, pts in POLI.items():
        m = np.zeros((FH, FW), np.uint8)
        cv2.fillPoly(m, [np.rint(proj_pts(pts) * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
        base = _TIERRA_M if k in ("manchuria", "karafuto") else m_jp
        CAMPOS[k] = _sdf(cv2.bitwise_and(m, base))
    # el imperio japonés de 1942: Japón + Corea + Taiwán + Manchuria + Karafuto
    imp = m_jp.copy()
    for k in ("corea_sur", "corea_nor", "taiwan"):
        imp = cv2.bitwise_or(imp, _mascara_geom(GEOMS[k]))
    for k in ("manchuria", "karafuto"):
        m = np.zeros((FH, FW), np.uint8)
        cv2.fillPoly(m, [np.rint(proj_pts(POLI[k]) * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
        imp = cv2.bitwise_or(imp, cv2.bitwise_and(m, _TIERRA_M))
    CAMPOS["imperio"] = _sdf(imp)
    CAMPOS["meiji"] = CAMPOS["japon"]
    CAMPOS["tokugawa"] = CAMPOS["sin_hokkaido"]


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
