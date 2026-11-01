# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de México en 5 minutos» (kit v2.1), con RELIEVE REAL NOAA ETOPO1.

Una sola rejilla en proyección de MERCATOR:
  - "mx": de Alta California al Caribe y de Oregón/Colorado a Costa Rica (lon -125.. -75, lat 42.5.. 8.5), 52 px por grado.
    Bajo el guache: relieve y batimetría NOAA ETOPO1 (1', datos/relieve_mx_etopo1.nc), cinturón verde mesoamericano (selvas y valles
    fértiles del centro y sur frente al norte árido) y ríos reales de Natural Earth + ríos principales de México (Bravo, Colorado,
    Gila, Lerma-Santiago, Balsas, Pánuco, Papaloapan, Grijalva, Usumacinta).
Los campos se calculan una vez (`python mapa.py`) y se guardan en datos/campos_mx.npz (int16, 1/8 de px).
"""
import json
import math
import os

import cv2
import numpy as np

import boceto as B
from motor import H, W, clamp01, lerp, prog

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(AQUI)
RAIZ = os.path.dirname(VIDEOS)
F_LAND = os.path.join(VIDEOS, "historia_roma", "datos", "ne_50m_land.json")
F_PAISES = os.path.join(VIDEOS, "historia_iran", "datos", "ne_50m_admin_0_countries.geojson")
F_RIOS = os.path.join(VIDEOS, "independencia_mx", "datos", "ne_50m_rivers_lake_centerlines.geojson")
F_LAGOS = os.path.join(VIDEOS, "independencia_mx", "datos", "ne_50m_lakes.geojson")
F_NC = os.path.join(AQUI, "datos", "relieve_mx_etopo1.nc")
DATOS = os.path.join(AQUI, "datos")
ESC_I16 = 8.0                        # los campos se guardan en int16 con 1/8 px de resolución


# ------------------------------------------------------------------ proyección de Mercator
def ymerc(lat):
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.asarray(lat, float)) / 2)))


def inv_ymerc(y):
    return np.degrees(2 * np.arctan(np.exp(np.radians(np.asarray(y, float)))) - np.pi / 2)


def U(lon):
    return np.asarray(lon, float)


def desU(u):
    return np.asarray(u, float)


class Rej:
    def __init__(self, nombre, lon0, lon1, lat0, lat1, pxdeg, envuelve=False):
        self.nombre, self.lon0, self.lon1, self.lat0, self.lat1 = nombre, lon0, lon1, lat0, lat1
        self.pxdeg, self.envuelve = pxdeg, envuelve
        self.Y0 = float(ymerc(lat0))
        self.FW = int(round((lon1 - lon0) * pxdeg))
        self.FH = int(round((self.Y0 - float(ymerc(lat1))) * pxdeg))
        self.campos = {}
        self.aux = None              # (FH, FW, 3) float32: luz del relieve, altitud 0..1, profundidad 0..1
        self.rios = []
        self._cel = {}

    def nat(self, lon):
        return np.asarray(lon, float)

    def proj(self, lon, lat):
        return (np.asarray(lon, float) - self.lon0) * self.pxdeg, (self.Y0 - ymerc(lat)) * self.pxdeg

    def proj_pts(self, P):
        P = np.asarray(P, float)
        x, y = self.proj(P[:, 0], P[:, 1])
        return np.stack([x, y], 1)

    def inv(self, x, y):
        return self.lon0 + np.asarray(x, float) / self.pxdeg, inv_ymerc(self.Y0 - np.asarray(y, float) / self.pxdeg)


REJ = {"mx": Rej("mx", -125.0, -75.0, 42.5, 8.5, 52.0)}
PXDEG_REF = REJ["mx"].pxdeg

# ------------------------------------------------------------------ paleta de guache (papel cálido, sierra ocre, selva jade, mar turquesa)
MAR = (168, 204, 212)
MAR_HONDO = (124, 168, 194)
MAR_CL = (204, 228, 224)
TIERRA = (236, 220, 184)
TIERRA_ALTA = (202, 174, 132)
TIERRA_CUMBRE = (236, 230, 216)
RIO = (88, 148, 196)
VALLE = (144, 180, 110)
AGUA_LAGO = (128, 184, 212)

COL = {
    "olmeca": (72, 152, 126),
    "zapoteca": (198, 118, 62),
    "teotihuacan": (208, 76, 58),
    "maya": (68, 148, 108),
    "tolteca": (186, 134, 64),
    "mexica": (204, 66, 54),
    "tlaxcala": (236, 184, 62),
    "conquista": (188, 56, 52),
    "nueva_espana": (218, 158, 58),
    "insurgentes": (74, 146, 98),
    "morelos": (92, 156, 108),
    "imperio_iturbide": (82, 142, 96),
    "mexico_1824": (86, 148, 98),
    "texas": (212, 132, 64),
    "eeuu": (78, 112, 174),
    "perdido": (132, 148, 178),
    "mexico_mod": (78, 148, 96),
    "reforma_lib": (74, 138, 104),
    "imperio_max": (150, 94, 158),
    "porfiriato": (196, 146, 68),
    "rev_norte": (206, 112, 58),
    "rev_sur": (82, 152, 96),
    "constitucion": (204, 72, 58),
    "cardenas": (76, 144, 98),
}
COL_CELDAS = [
    (214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
    (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110),
]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat)
CIUDADES = {
    # Centro y Valle de México
    "tenochtitlan": (-99.13, 19.43), "cdmx": (-99.13, 19.43), "texcoco": (-98.88, 19.51), "tlatelolco": (-99.14, 19.45),
    "teotihuacan": (-98.84, 19.69), "tula": (-99.34, 20.05), "tlaxcala": (-98.24, 19.32), "cholula": (-98.30, 19.06),
    "puebla": (-98.20, 19.04), "cuernavaca": (-99.23, 18.92), "anenehuilco": (-98.99, 18.78), "cuautla": (-98.95, 18.81),
    "toluca": (-99.66, 19.29),
    # Golfo, Oaxaca y Sureste / Área Maya
    "veracruz": (-96.13, 19.18), "zempoala": (-96.40, 19.45), "san_lorenzo": (-94.76, 17.75), "la_venta": (-94.04, 18.10),
    "monte_alban": (-96.77, 17.04), "oaxaca": (-96.72, 17.06), "guelatao": (-96.49, 17.31), "tehuacan": (-97.39, 18.46),
    "palenque": (-92.05, 17.48), "calakmul": (-89.81, 18.10), "tikal": (-89.62, 17.22), "chichen_itza": (-88.57, 20.68),
    "uxmal": (-89.77, 20.36), "merida": (-89.62, 20.97), "campeche": (-90.53, 19.84), "cozumel": (-86.95, 20.51),
    # Sur y Pacífico
    "acapulco": (-99.89, 16.86), "chilpancingo": (-99.50, 17.55), "iguala": (-99.54, 18.34), "apatzingan": (-102.35, 19.09),
    "morelia": (-101.19, 19.70), "valladolid": (-101.19, 19.70), "tzintzuntzan": (-101.58, 19.63),
    # Bajío y Occidente
    "queretaro": (-100.39, 20.59), "dolores": (-100.93, 21.16), "guanajuato": (-101.26, 21.02), "san_miguel": (-100.74, 20.91),
    "celaya": (-100.81, 20.52), "guadalajara": (-103.35, 20.67), "san_blas": (-105.28, 21.54), "colima": (-103.72, 19.24),
    "zacatecas": (-102.57, 22.77), "aguascalientes": (-102.29, 21.88), "san_luis": (-100.98, 22.15), "tampico": (-97.86, 22.25),
    "poza_rica": (-97.46, 20.53),
    # Norte y frontera histórica
    "monterrey": (-100.31, 25.67), "saltillo": (-101.00, 25.42), "torreon": (-103.41, 25.54), "durango": (-104.65, 24.02),
    "chihuahua": (-106.09, 28.63), "parral": (-105.66, 26.93), "ciudad_juarez": (-106.48, 31.74), "paso_norte": (-106.48, 31.74),
    "hermosillo": (-110.96, 29.07), "cananea": (-110.29, 30.98), "tijuana": (-117.04, 32.51), "la_paz": (-110.31, 24.14),
    # Territorios del norte y vecinos
    "san_antonio": (-98.49, 29.42), "alamo": (-98.49, 29.42), "houston": (-95.37, 29.76), "santa_fe": (-105.94, 35.69),
    "san_francisco": (-122.42, 37.77), "los_angeles": (-118.24, 34.05), "san_diego": (-117.16, 32.72),
    "la_habana": (-82.37, 23.11), "guatemala": (-90.51, 14.63),
}

RUTAS = {
    "migracion_mexica": [(-105.2, 21.8), (-103.3, 20.7), (-101.2, 20.1), (-99.34, 20.05), (-99.13, 19.43)],
    "cortes_mar": [(-82.37, 23.11), (-86.95, 20.51), (-90.53, 19.84), (-92.8, 18.6), (-96.13, 19.18)],
    "cortes_tierra": [(-96.13, 19.18), (-96.40, 19.45), (-97.4, 19.4), (-98.24, 19.32), (-98.30, 19.06), (-99.13, 19.43)],
    "camino_plata": [(-99.13, 19.43), (-100.39, 20.59), (-101.26, 21.02), (-102.57, 22.77), (-104.65, 24.02), (-106.09, 28.63), (-105.94, 35.69)],
    "galeon_manila": [(-124.5, 19.0), (-116.0, 17.8), (-108.0, 17.0), (-99.89, 16.86)],
    "ruta_veracruz": [(-96.13, 19.18), (-93.0, 21.0), (-88.0, 23.2), (-82.37, 23.11), (-76.0, 25.0)],
    "hidalgo": [(-100.93, 21.16), (-100.74, 20.91), (-101.26, 21.02), (-101.19, 19.70), (-99.4, 19.3), (-103.35, 20.67)],
    "morelos": [(-101.19, 19.70), (-99.89, 16.86), (-99.50, 17.55), (-98.95, 18.81), (-96.72, 17.06)],
    "trigarante": [(-99.54, 18.34), (-100.39, 20.59), (-98.20, 19.04), (-99.13, 19.43)],
    "eeuu_norte": [(-97.5, 28.5), (-100.31, 25.67), (-101.00, 25.42)],
    "eeuu_ oeste": [(-104.0, 37.0), (-105.94, 35.69), (-112.0, 33.5), (-117.16, 32.72)],
    "eeuu_scott": [(-93.0, 23.5), (-96.13, 19.18), (-98.20, 19.04), (-99.13, 19.43)],
    "francia_inv": [(-92.0, 20.5), (-96.13, 19.18), (-98.20, 19.04), (-99.13, 19.43)],
    "juarez_norte": [(-99.13, 19.43), (-100.98, 22.15), (-101.00, 25.42), (-106.09, 28.63), (-106.48, 31.74)],
    "juarez_regreso": [(-106.48, 31.74), (-106.09, 28.63), (-102.57, 22.77), (-100.39, 20.59), (-99.13, 19.43)],
    "ferrocarril_norte": [(-99.13, 19.43), (-100.39, 20.59), (-102.29, 21.88), (-102.57, 22.77), (-103.41, 25.54), (-106.09, 28.63), (-106.48, 31.74)],
    "ferrocarril_golfo": [(-99.13, 19.43), (-98.20, 19.04), (-96.13, 19.18)],
    "villa_sur": [(-106.48, 31.74), (-106.09, 28.63), (-103.41, 25.54), (-102.57, 22.77), (-100.39, 20.59), (-99.13, 19.43)],
    "zapata_norte": [(-98.95, 18.81), (-99.23, 18.92), (-99.13, 19.43)],
}

CELDAS_SEMILLAS = {
    "clasico_colapso": [(-98.84, 19.69), (-96.77, 17.04), (-92.05, 17.48), (-89.81, 18.10), (-88.57, 20.68), (-96.40, 19.45)],
    "caudillos_xix": [(-99.13, 19.43), (-103.35, 20.67), (-96.13, 19.18), (-96.72, 17.06), (-89.62, 20.97), (-100.31, 25.67), (-106.09, 28.63)],
    "facciones_rev": [(-106.09, 28.63), (-98.95, 18.81), (-100.31, 25.67), (-109.5, 27.5), (-96.13, 19.18)],
}
CELDAS_PAISES = {}

# ------------------------------------------------------------------ polígonos históricos (lon, lat)
VALLE_VERDE = [
    (-105.5, 21.6), (-102.0, 21.4), (-99.8, 21.2), (-97.5, 22.2), (-95.8, 19.0), (-94.0, 18.6),
    (-90.6, 20.0), (-89.5, 21.6), (-86.7, 21.6), (-86.8, 18.0), (-88.0, 15.0), (-83.0, 10.0),
    (-85.5, 9.5), (-92.2, 14.5), (-95.2, 16.0), (-99.9, 16.7), (-103.8, 18.6), (-105.6, 20.4),
]
LAGO_TEXCOCO = [
    (-99.22, 19.68), (-98.92, 19.68), (-98.86, 19.48), (-98.92, 19.24), (-99.16, 19.24), (-99.24, 19.46),
]
OLMECA = [
    (-96.2, 18.9), (-94.8, 18.7), (-93.0, 18.5), (-92.6, 17.5), (-94.2, 17.1), (-95.8, 17.5),
]
ZAPOTECA = [
    (-98.1, 18.1), (-95.8, 17.9), (-94.8, 16.4), (-96.5, 15.6), (-98.2, 16.2),
]
TEOTIHUACAN_ZONA = [
    (-101.2, 20.9), (-97.2, 20.8), (-96.6, 18.6), (-98.6, 18.0), (-100.8, 18.6),
]
MAYA_ZONA = [
    (-93.2, 18.6), (-90.6, 20.0), (-89.6, 21.6), (-86.7, 21.6), (-86.8, 18.0), (-88.0, 15.2),
    (-87.6, 13.8), (-90.8, 13.8), (-92.8, 15.2), (-93.6, 17.0),
]
TOLTECA = [
    (-102.2, 21.8), (-97.6, 21.6), (-97.4, 19.2), (-100.8, 19.0), (-102.4, 20.0),
]
MEXICA = [
    (-100.8, 20.8), (-97.3, 21.2), (-95.8, 18.8), (-94.8, 17.8), (-95.0, 16.0), (-92.2, 14.6),
    (-93.8, 15.8), (-96.8, 15.7), (-99.9, 16.7), (-101.4, 17.8), (-100.8, 19.4),
]
TLAXCALA_POLI = [
    (-98.48, 19.68), (-97.72, 19.66), (-97.70, 19.12), (-98.46, 19.10),
]
CONQUISTA_1521 = [
    (-100.4, 20.4), (-96.0, 19.8), (-95.8, 18.4), (-98.4, 18.0), (-100.4, 18.8),
]
NORTE_NOVOHISPANO = [
    (-124.6, 42.0), (-109.0, 42.0), (-106.0, 39.0), (-103.0, 37.0), (-100.0, 36.5),
    (-94.0, 33.5), (-93.6, 29.5), (-97.0, 25.8), (-105.0, 25.0), (-117.2, 32.4), (-124.6, 38.0),
]
TEXAS_1836 = [
    (-103.5, 36.5), (-100.0, 36.5), (-94.0, 33.6), (-93.8, 29.6), (-97.1, 25.9),
    (-99.2, 26.5), (-101.5, 29.5), (-103.5, 32.0),
]
PERDIDO_1848 = [
    (-124.6, 42.0), (-109.0, 42.0), (-106.0, 39.0), (-103.0, 37.0), (-100.0, 36.5),
    (-94.0, 33.6), (-93.8, 29.6), (-97.1, 25.9), (-99.8, 27.5), (-103.0, 29.0),
    (-104.8, 30.6), (-106.5, 31.8), (-109.0, 31.3), (-114.8, 32.5), (-117.2, 32.5), (-124.6, 38.0),
]
INSURGENTES_1810 = [
    (-105.2, 22.2), (-100.0, 22.4), (-99.0, 19.4), (-101.5, 19.0), (-104.8, 20.0),
]
MORELOS_SUR = [
    (-102.6, 19.6), (-97.8, 19.2), (-95.8, 17.6), (-96.2, 15.6), (-100.2, 16.6), (-102.4, 18.0),
]
IMPERIO_MAX = [
    (-104.0, 22.4), (-97.5, 22.4), (-95.8, 18.8), (-96.4, 16.6), (-100.5, 18.2), (-103.8, 20.2),
]
REV_NORTE = [
    (-109.2, 31.8), (-101.0, 29.5), (-100.5, 24.5), (-102.5, 22.2), (-105.8, 23.2), (-108.5, 27.5),
]
REV_SUR = [
    (-100.4, 19.3), (-97.8, 19.2), (-97.6, 17.4), (-99.8, 17.2),
]

# Ríos principales suplementarios de México para garantizar trazos continuos y visibles
RIOS_EXTRA = [
    ([(-106.48, 31.74), (-104.5, 29.5), (-103.0, 29.0), (-101.4, 29.8), (-99.5, 27.5), (-97.15, 25.95)], 9.3),  # Río Bravo
    ([(-114.6, 36.0), (-114.5, 34.5), (-114.7, 32.7), (-114.8, 31.8)], 9.0),                                      # Río Colorado
    ([(-99.6, 19.3), (-100.8, 20.1), (-102.7, 20.3), (-103.3, 20.8), (-105.3, 21.6)], 8.9),                       # Lerma - Grande de Santiago
    ([(-98.2, 19.1), (-98.6, 18.0), (-100.2, 17.9), (-101.8, 18.3), (-102.2, 17.95)], 8.8),                       # Río Balsas
    ([(-99.2, 20.2), (-98.8, 21.2), (-98.3, 22.0), (-97.85, 22.25)], 8.6),                                        # Río Pánuco
    ([(-96.8, 17.6), (-96.2, 18.2), (-95.7, 18.6)], 8.6),                                                         # Río Papaloapan
    ([(-92.0, 15.6), (-93.1, 16.8), (-93.5, 17.8), (-92.9, 18.0), (-92.7, 18.6)], 8.9),                           # Río Grijalva
    ([(-90.5, 16.0), (-91.4, 17.2), (-92.5, 18.4)], 9.0),                                                         # Río Usumacinta
]


# ------------------------------------------------------------------ rasterización
def _anillos(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    return geom["coordinates"]


def _mask_geoms(rej, geoms):
    m = np.zeros((rej.FH, rej.FW), np.uint8)
    for g in geoms:
        for poly in _anillos(g):
            I = []
            for r in poly:
                P = np.asarray(r, float)
                x = (P[:, 0] - rej.lon0) * rej.pxdeg
                if x.max() < -50 or x.min() > rej.FW + 50:
                    continue
                y = (rej.Y0 - ymerc(np.clip(P[:, 1], -85, 85))) * rej.pxdeg
                I.append(np.rint(np.stack([x, y], 1) * 4).astype(np.int32).reshape(-1, 1, 2))
            if I:
                cv2.fillPoly(m, I, 255, cv2.LINE_8, 2)
    return m


def _mano(pts, paso=0.04, amp=0.10):
    P = np.asarray(pts, float)
    P = np.vstack([P, P[:1]])
    out = []
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / paso))
        for k in range(n):
            out.append(a + (b - a) * k / n)
    Q = np.array(out)
    lo, la = Q[:, 0], Q[:, 1]
    dx = (np.sin(lo * 2.3 + la * 1.7 + 0.4) * 0.6 + np.sin(lo * 5.1 - la * 4.3 + 1.9) * 0.3 + np.sin(lo * 11.0 + la * 9.0) * 0.12)
    dy = (np.sin(la * 2.1 - lo * 1.9 + 2.2) * 0.6 + np.sin(la * 4.7 + lo * 5.3 + 0.7) * 0.3 + np.sin(la * 10.0 - lo * 12.0) * 0.12)
    return np.stack([lo + amp * dx, la + amp * dy], 1)


def _mask_poli(rej, pts, mano=True):
    m = np.zeros((rej.FH, rej.FW), np.uint8)
    P = rej.proj_pts(_mano(pts) if mano else pts)
    cv2.fillPoly(m, [np.rint(P * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
    return m


def _sdf(m):
    b = (m > 127).astype(np.uint8)
    if b.max() == 0:
        return np.full(m.shape, 4000.0, np.float32)
    din = cv2.distanceTransform(b, cv2.DIST_L2, 5)
    dout = cv2.distanceTransform(1 - b, cv2.DIST_L2, 5)
    return cv2.GaussianBlur((dout - din).astype(np.float32), (0, 0), 1.3)


def _i16(s):
    return np.clip(np.rint(s * ESC_I16), -32000, 32000).astype(np.int16)


_PAISES = None
_RIOS = None
RIOS_SI = {
    "Rio Grande": 9.4, "Colorado": 9.0, "Gila": 8.2, "Brazos": 8.0, "Mississippi": 9.2,
    "Pánuco": 8.6, "Río Grande de Santiago": 8.8, "Usumacinta": 9.0, "Chixoy": 8.2, "Coco": 8.0, "Verde": 8.0,
}


def _paises(nombres):
    return [f["geometry"] for f in _PAISES["features"] if f["properties"]["NAME"] in nombres]


def _construir(rej):
    """Calcula todos los campos de la rejilla (se hace una vez y se guarda en datos/campos_mx.npz)."""
    global _PAISES, _RIOS
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    _RIOS = json.load(open(F_RIOS, encoding="utf-8"))
    lagos = json.load(open(F_LAGOS, encoding="utf-8"))
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    perm = [f["geometry"] for f in lagos["features"] if f["properties"].get("name") in
            ("Lake Chapala", "Lago de Chapala", "Lake Nicaragua", "Lake Managua", "Great Salt Lake")]
    m_lagos = _mask_geoms(rej, perm)
    tierra = cv2.bitwise_and(tierra0, cv2.bitwise_not(m_lagos))
    M = {"tierra": tierra}

    def P(pts, base=tierra, mano=True):
        return cv2.bitwise_and(_mask_poli(rej, pts, mano), base)

    def U_(*ms):
        out = ms[0].copy()
        for m in ms[1:]:
            out = cv2.bitwise_or(out, m)
        return out

    def menos(a, *bs):
        out = a.copy()
        for b in bs:
            out = cv2.bitwise_and(out, cv2.bitwise_not(b))
        return out

    def paises(*n):
        return cv2.bitwise_and(_mask_geoms(rej, _paises(n)), tierra)

    mx = paises("Mexico")
    eeuu = paises("United States of America")
    centroam = paises("Guatemala", "Belize", "Honduras", "El Salvador", "Nicaragua", "Costa Rica")
    cuba = paises("Cuba")

    M["valle"] = P(VALLE_VERDE)
    M["lago_texcoco"] = _mask_poli(rej, LAGO_TEXCOCO, mano=False)
    M["olmeca"] = P(OLMECA, mx)
    M["zapoteca"] = P(ZAPOTECA, mx)
    M["teotihuacan"] = P(TEOTIHUACAN_ZONA, mx)
    M["maya"] = P(MAYA_ZONA)
    M["tolteca"] = P(TOLTECA, mx)
    tlax = P(TLAXCALA_POLI, mx, mano=False)
    M["tlaxcala"] = tlax
    M["mexica"] = menos(P(MEXICA, mx), tlax)
    M["conquista_1521"] = P(CONQUISTA_1521, mx)

    norte_nh = cv2.bitwise_and(_mask_poli(rej, NORTE_NOVOHISPANO, mano=True), eeuu)
    M["nueva_espana"] = U_(mx, norte_nh, centroam, cuba)
    M["insurgentes_1810"] = P(INSURGENTES_1810, mx)
    M["morelos_sur"] = P(MORELOS_SUR, mx)
    M["imperio_iturbide"] = U_(mx, norte_nh, centroam)
    M["mexico_1824"] = U_(mx, norte_nh)

    texas = cv2.bitwise_and(_mask_poli(rej, TEXAS_1836, mano=True), eeuu)
    perdido = cv2.bitwise_and(_mask_poli(rej, PERDIDO_1848, mano=True), eeuu)
    M["texas_1836"] = texas
    M["mexico_1836"] = menos(M["mexico_1824"], texas)
    M["perdido_1848"] = perdido
    M["eeuu_1846"] = menos(eeuu, menos(perdido, texas))
    M["eeuu_mod"] = eeuu
    M["mexico_mod"] = mx

    M["imperio_max"] = P(IMPERIO_MAX, mx)
    M["republica_juarez"] = menos(mx, M["imperio_max"])
    M["rev_norte"] = P(REV_NORTE, mx)
    M["rev_sur"] = P(REV_SUR, mx)

    campos = {k: _i16(_sdf(v)) for k, v in M.items()}
    aux = _relieve(rej, tierra)
    rios = _rios(rej)
    return campos, {}, aux, rios


def _relieve(rej, tierra):
    """(FH, FW, 3): luz del sombreado (-1..1), altitud 0..1 (tierra) y profundidad 0..1 (mar), del relieve ETOPO1."""
    from scipy.io import netcdf_file
    f = netcdf_file(F_NC, "r", mmap=False)
    alt = f.variables["altitude"][:].astype(np.float32).copy()
    lat_ = f.variables["latitude"][:].copy()
    lon_ = f.variables["longitude"][:].copy()
    lat0, lon0, paso = float(lat_[0]), float(lon_[0]), float(lat_[1] - lat_[0])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float32)
    lon, lat = rej.inv(xs, ys)
    mi = ((lat - lat0) / paso).astype(np.float32)
    mj = ((lon - lon0) / paso).astype(np.float32)
    e = cv2.remap(alt, mj, mi, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    es = cv2.GaussianBlur(e, (0, 0), 1.2)
    gx = cv2.Sobel(es, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(es, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    px_m = 111320.0 / (rej.pxdeg * (1.0 / np.cos(np.radians(lat))))
    k = 9.0 / px_m
    luz = np.clip(k * (gx * 0.70 + gy * 0.70), -1.0, 1.0)
    luz = np.where(tierra > 127, luz, 0.0).astype(np.float32)
    alt01 = np.clip(e / 2600.0, 0, 1)
    prof = np.clip(-e / 1800.0, 0, 1).astype(np.float32)
    return np.stack([luz, alt01.astype(np.float32), prof], -1).astype(np.float32)


def _rios(rej):
    out = []
    for f in _RIOS["features"]:
        n = f["properties"].get("name")
        if n not in RIOS_SI:
            continue
        g = f["geometry"]
        for c in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            P = np.asarray(c, float)
            if len(P) < 2:
                continue
            out.append((P, RIOS_SI[n]))
    for pts, peso in RIOS_EXTRA:
        out.append((np.asarray(pts, float), peso))
    return out


def preparar(nombres=("mx",)):
    os.makedirs(DATOS, exist_ok=True)
    for n in nombres:
        rej = REJ[n]
        campos, cel, aux, rios = _construir(rej)
        datos = {f"c_{k}": v for k, v in campos.items()}
        datos["aux"] = aux.astype(np.float16)
        datos["rios_pts"] = np.concatenate([r[0] for r in rios]).astype(np.float32)
        datos["rios_cortes"] = np.cumsum([0] + [len(r[0]) for r in rios]).astype(np.int64)
        datos["rios_peso"] = np.array([r[1] for r in rios], np.float32)
        np.savez_compressed(os.path.join(DATOS, f"campos_{n}.npz"), **datos)
        print(n, rej.FW, "x", rej.FH, "campos:", len(campos), "ríos:", len(rios), flush=True)


def _cargar_rej(rej):
    if rej.campos:
        return
    d = np.load(os.path.join(DATOS, f"campos_{rej.nombre}.npz"))
    for k in d.files:
        if k.startswith("c_"):
            rej.campos[k[2:]] = d[k]
    rej.aux = d["aux"].astype(np.float32) if "aux" in d.files else None
    pts, cortes, peso = d["rios_pts"].astype(np.float64), d["rios_cortes"], d["rios_peso"]
    rej.rios = [(pts[a:b], float(p)) for a, b, p in zip(cortes[:-1], cortes[1:], peso)]
    rej.r_pts = pts
    rej.r_cortes = cortes
    rej.r_peso = peso


ACT = None
CAMPOS = {}
CELDAS = {}
LON0 = LON1 = LAT0 = LAT1 = 0.0
FW = FH = 0


def usar(nombre="mx"):
    global ACT, CAMPOS, CELDAS, LON0, LON1, LAT0, LAT1, FW, FH
    rej = REJ["mx"]
    _cargar_rej(rej)
    ACT = rej
    CAMPOS = rej.campos
    CELDAS = dict(CELDAS_SEMILLAS)
    LON0, LON1, LAT0, LAT1, FW, FH = rej.lon0, rej.lon1, rej.lat0, rej.lat1, rej.FW, rej.FH


def cargar():
    _cargar_rej(REJ["mx"])
    if ACT is None:
        usar("mx")


def proj(lon, lat):
    return ACT.proj(lon, lat)


def proj_pts(P):
    return ACT.proj_pts(P)


def celdas(nombre):
    rej = ACT
    if nombre in rej._cel:
        return rej._cel[nombre]
    seeds = rej.proj_pts(CELDAS_SEMILLAS[nombre])
    ys, xs = np.mgrid[0:rej.FH:2, 0:rej.FW:2].astype(np.float32)
    d = np.stack([np.hypot(xs - sx, ys - sy) for sx, sy in seeds], 0)
    idx = np.argmin(d, 0).astype(np.uint8)
    ds = np.sort(d, 0)
    borde = ((ds[1] - ds[0]) * 0.5).astype(np.float32)
    idx = cv2.resize(idx, (rej.FW, rej.FH), interpolation=cv2.INTER_NEAREST)
    borde = cv2.resize(borde, (rej.FW, rej.FH), interpolation=cv2.INTER_LINEAR)
    rej._cel[nombre] = (idx, borde)
    return rej._cel[nombre]


# ------------------------------------------------------------------ cámara
class Cam:
    """Cámara: centro (lon, lat), zoom z (px de pantalla por px de la rejilla), giro (rad)."""

    def __init__(self, lon=-100.0, lat=21.5, z=2.2, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.rej = ACT if ACT is not None else REJ["mx"]
        self.lon, self.lat, self.z, self.rot = lon, lat, z, rot
        self.zn = z * PXDEG_REF / self.rej.pxdeg
        cx, cy = self.rej.proj(lon, lat)
        c, s = math.cos(rot) * self.zn, math.sin(rot) * self.zn
        self.M = np.float32([[c, -s, W / 2 - (c * cx - s * cy)], [s, c, H / 2 - (s * cx + c * cy)]])

    def pant(self, lon, lat):
        x, y = self.rej.proj(lon, lat)
        M = self.M
        return float(M[0, 0] * x + M[0, 1] * y + M[0, 2]), float(M[1, 0] * x + M[1, 1] * y + M[1, 2])

    def pant_pts(self, P):
        P = np.asarray(P, float)
        x, y = self.rej.proj(P[:, 0], P[:, 1])
        M = self.M
        return np.stack([M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]], 1)

    def proyectar(self, campo, relleno=4000.0):
        if campo.dtype == np.int16:
            r = cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=int(min(relleno * ESC_I16, 32000)))
            return r.astype(np.float32) * np.float32(self.zn / ESC_I16)
        r = cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)
        return r * np.float32(self.zn)

    def proyectar_crudo(self, img, relleno=0.0, interp=cv2.INTER_LINEAR):
        return cv2.warpAffine(img, self.M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)

    @property
    def escala(self):
        return self.z

    def limites(self):
        hw = W / 2 / (self.zn * self.rej.pxdeg)
        y = float(ymerc(self.lat))
        hh = H / 2 / (self.zn * self.rej.pxdeg)
        return self.lon - hw, self.lon + hw, float(inv_ymerc(y - hh)), float(inv_ymerc(y + hh))


# ------------------------------------------------------------------ pincel de guache
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
_CERO = np.zeros((H, W), np.float32)

from numba import njit, prange            # noqa: E402


@njit(parallel=True, fastmath=True, cache=True)
def _pintar_nb(img, S, nz, pincel, grano, col, alfa, sombra, borde, amp, luz, kluz, y0, y1, x0, x1):
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
            d = -s * (1.0 / 70.0)
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
            k = lum * (1.0 + 1.2 * pincel[y, x]) * (1.0 + kluz * luz[y, x])
            for c in range(3):
                pig = col[c] * k * grano[y, x, c]
                img[y, x, c] = img[y, x, c] * (1.0 - a) + pig * a


@njit(parallel=True, fastmath=True, cache=True)
def _tierra_nb(img, S, nz, pincel, grano, aux, c_baja, c_alta, c_cumbre, c_mar, c_hondo, c_orilla, amp, y0, y1, x0, x1):
    h, w = S.shape
    for y in prange(y0, y1):
        for x in range(x0, x1):
            s = S[y, x] + amp * nz[y, x]
            luz = aux[y, x, 0]
            alt = aux[y, x, 1]
            pr = aux[y, x, 2]
            pc = 1.0 + 1.3 * pincel[y, x]
            if s > -2.0:
                u = pr ** 0.6
                o = 0.0
                if s < 46.0 and s > 0.0:
                    t = 1.0 - s / 46.0
                    o = t * t * 0.55
                for c in range(3):
                    m = c_mar[c] * (1.0 - u) + c_hondo[c] * u
                    m = m * (1.0 - o) + c_orilla[c] * o
                    img[y, x, c] = m * pc * grano[y, x, c]
            if s > 2.0:
                continue
            a = 0.5 - s * 0.7692
            if a <= 0.0:
                continue
            if a > 1.0:
                a = 1.0
            d = -s * (1.0 / 60.0)
            if d < 0.0:
                d = 0.0
            if d > 1.0:
                d = 1.0
            lum = 1.0 - 0.06 * (1.0 - d)
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
                    lum -= 0.13 * sh * band
                else:
                    lum -= 0.08 * sh * band
            lum *= (1.0 + 0.40 * luz) * (1.0 + 1.2 * pincel[y, x])
            ac = alt * 1.6
            if ac > 1.0:
                ac = 1.0
            sn = (alt - 0.72) * 4.0
            if sn < 0.0:
                sn = 0.0
            if sn > 1.0:
                sn = 1.0
            for c in range(3):
                col = c_baja[c] * (1.0 - ac) + c_alta[c] * ac
                col = col * (1.0 - sn) + c_cumbre[c] * sn
                pig = col * lum * grano[y, x, c]
                img[y, x, c] = img[y, x, c] * (1.0 - a) + pig * a


def _roi(S, margen=24):
    m = S[::8, ::8] < 3.0
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        return None
    return (max(0, ys.min() * 8 - margen), min(H, ys.max() * 8 + 8 + margen), max(0, xs.min() * 8 - margen), min(W, xs.max() * 8 + 8 + margen))


def _c(col):
    return np.array(col, np.float32) / 255.0


def pintar(img, S, color, alfa=1.0, fase=0, borde=1.0, sombra=0.24, ruido=1.0, luz=None, kluz=0.34):
    r = _roi(S)
    if r is None:
        return
    _pintar_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, _c(color), np.float32(alfa), np.float32(sombra), np.float32(borde),
               np.float32(4.0 * ruido), _CERO if luz is None else luz, np.float32(kluz if luz is not None else 0.0), r[0], r[1], r[2], r[3])


class Base:
    pass


def pintar_base(cam, fase=0):
    """Fondo: mar con profundidad, tierra con relieve de las Sierras Madres y el cinturón verde mesoamericano."""
    rej = cam.rej
    img = np.empty((H, W, 3), np.float32)
    S = cam.proyectar(rej.campos["tierra"])
    aux = cam.proyectar_crudo(rej.aux, 0.0)
    _tierra_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, aux, _c(TIERRA), _c(TIERRA_ALTA), _c(TIERRA_CUMBRE), _c(MAR_CL), _c(MAR_HONDO), _c((214, 234, 230)),
               np.float32(3.0), 0, H, 0, W)
    b = Base()
    b.S, b.luz = S, aux[..., 0].copy()
    Sv = cam.proyectar(rej.campos["valle"])
    pintar(img, Sv, VALLE, 0.72, fase, borde=0.35, sombra=0.08, ruido=0.6, luz=b.luz, kluz=0.28)
    return img, b


def pintar_rios(img, cam, base, t=0.0, alfa=0.92, minimo=None):
    """Ríos (pincelada azul) sobre tierra y territorios; grosor según el peso del río y el zoom."""
    rej = cam.rej
    if minimo is None:
        minimo = float(np.interp(math.log(max(cam.z, 0.05)), [math.log(1.0), math.log(3.0)], [8.3, 6.8]))
    Q = cam.pant_pts(rej.r_pts)
    Q16 = np.rint(Q * 16).astype(np.int32)
    capas = [[], [], []]
    for (a, b, p) in zip(rej.r_cortes[:-1], rej.r_cortes[1:], rej.r_peso):
        if p < minimo:
            continue
        seg = Q16[a:b]
        if len(seg) < 2 or seg[:, 0].max() < -320 or seg[:, 0].min() > (W + 20) * 16 or seg[:, 1].max() < -320 or seg[:, 1].min() > (H + 20) * 16:
            continue
        f = p - minimo
        capas[0 if f < 0.7 else (1 if f < 1.6 else 2)].append(seg)
    m = np.zeros((H, W), np.uint8)
    esc = max(0.7, min(2.6, cam.z / 2.2)) ** 0.65
    for g, L in enumerate(capas):
        if L:
            cv2.polylines(m, L, False, 255, max(1, int(round((2.2 + 1.9 * g) * esc))), cv2.LINE_AA, 4)
    tierra = (base.S < -1.0).astype(np.uint8) * 255
    m = cv2.multiply(m, tierra, scale=1 / 255.0)
    ys, xs = np.nonzero(m)
    if len(ys):
        a = (m[ys, xs].astype(np.float32) / 255.0)[:, None] * alfa
        col = _c(RIO) * (1 + 1.2 * PINCEL[ys, xs])[:, None] * GRANO[ys, xs]
        img[ys, xs] = img[ys, xs] * (1 - a) + col * a


_ROT = {}


def _mascara_rot(t, px, rot):
    k = (t, px, rot)
    if k not in _ROT:
        m = B.mascara_texto(t, px)
        if rot:
            h_, w_ = m.shape
            d = int(math.hypot(w_, h_)) + 4
            big = np.zeros((d, d), np.uint8)
            big[(d - h_) // 2:(d - h_) // 2 + h_, (d - w_) // 2:(d - w_) // 2 + w_] = m
            Mr = cv2.getRotationMatrix2D((d / 2, d / 2), math.degrees(rot), 1.0)
            m = cv2.warpAffine(big, Mr, (d, d))
            ys, xs = np.nonzero(m > 8)
            m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        _ROT[k] = m
    return _ROT[k]


def rotulo_mapa(img, txt, cam, lon, lat, px=40, alfa=0.42, color=(70, 96, 120), espaciado=True, rot=0.0):
    x, y = cam.pant(lon, lat)
    t = " ".join(txt) if espaciado else txt
    px = int(max(18, min(84, px * (cam.zn / 2.6) ** 0.45)))
    m = _mascara_rot(t, px, round(rot, 3))
    h_, w_ = m.shape
    x0, y0 = int(x - w_ / 2), int(y - h_ / 2)
    fuera = max(0.0, 30 - x0, x0 + w_ - (W - 30), 125 - y0, y0 + h_ - (H - 30))
    alfa *= max(0.0, 1.0 - fuera / 24.0)
    if alfa <= 0.01:
        return
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w_), min(H, y0 + h_)
    if xb <= xa or yb <= ya:
        return
    a = (m[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32) / 255.0)[..., None] * alfa
    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - a) + _c(color) * a


def mezcla_campos(a, b, k):
    k = float(min(1.0, max(0.0, k)))
    if k <= 0:
        return CAMPOS[a]
    if k >= 1:
        return CAMPOS[b]
    return cv2.addWeighted(CAMPOS[a], 1 - k, CAMPOS[b], k, 0)


if __name__ == "__main__":
    preparar()
