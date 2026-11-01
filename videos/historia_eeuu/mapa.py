# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Estados Unidos en 6 minutos» (kit v2.1), con RELIEVE REAL NOAA ETOPO1.

Una sola rejilla en proyección de MERCATOR:
  - "us": del Pacífico al Atlántico y del sur de Canadá a Cuba (lon -127.. -63, lat 51.. 22.5), 44 px por grado.
    Bajo el guache: relieve y batimetría NOAA ETOPO1 (1', datos/relieve_us_etopo1.nc), bosque oriental y del noroeste en verde
    frente a las Grandes Llanuras y el oeste árido, Grandes Lagos y ríos reales de Natural Earth (Misisipi, Misuri, Ohio, Bravo, Colorado, Columbia…).
    Estados reales (datos/us_states.json) para las trece colonias, la Confederación y la fractura en estados (`celdas("estados")`).
Los campos se calculan una vez (`python mapa.py`) y se guardan en datos/campos_us.npz (int16, 1/8 de px).
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
F_NC = os.path.join(AQUI, "datos", "relieve_us_etopo1.nc")
F_EST = os.path.join(AQUI, "datos", "us_states.json")
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


REJ = {"us": Rej("us", -127.0, -63.0, 51.0, 22.5, 44.0)}
PXDEG_REF = REJ["us"].pxdeg

# ------------------------------------------------------------------ paleta de guache (papel cálido, Rocosas ocres, bosque oriental verde, mar turquesa)
MAR = (168, 204, 212)
MAR_HONDO = (124, 168, 194)
MAR_CL = (204, 228, 224)
TIERRA = (236, 220, 184)
TIERRA_ALTA = (202, 174, 132)
TIERRA_CUMBRE = (236, 230, 216)
RIO = (88, 148, 196)
VALLE = (150, 182, 116)
AGUA_LAGO = (128, 184, 212)

COL = {
    "nativos": (176, 124, 78),
    "cahokia": (198, 118, 62),
    "pueblo": (212, 150, 84),
    "iroquesa": (92, 142, 104),
    "espana": (226, 168, 58),
    "inglaterra": (196, 70, 62),
    "francia": (82, 112, 176),
    "colonias": (196, 70, 62),
    "eeuu": (78, 112, 174),
    "luisiana": (228, 150, 92),
    "mexico": (78, 148, 96),
    "texas": (212, 132, 64),
    "perdido": (236, 176, 82),
    "oregon": (150, 110, 170),
    "cherokee": (178, 112, 76),
    "territorio_indio": (196, 146, 92),
    "union": (70, 100, 172),
    "confederacion": (166, 156, 142),
    "fronterizos": (112, 146, 196),
    "canada": (200, 98, 92),
    "urss": (196, 60, 54),
    "eeuu_hoy": (78, 112, 174),
}
COL_CELDAS = [
    (214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
    (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110),
]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat)
CIUDADES = {
    # pueblos originarios
    "white_sands": (-106.30, 32.80), "cahokia": (-90.06, 38.66), "mesa_verde": (-108.49, 37.18), "chaco": (-107.96, 36.06),
    "onondaga": (-76.15, 43.05),
    # colonias y revolución
    "san_agustin": (-81.31, 29.89), "jamestown": (-76.78, 37.21), "point_comfort": (-76.30, 37.00), "plymouth": (-70.66, 41.96),
    "boston": (-71.06, 42.36), "nueva_york": (-74.00, 40.71), "filadelfia": (-75.17, 39.95), "lexington": (-71.23, 42.45),
    "saratoga": (-73.64, 43.00), "yorktown": (-76.51, 37.24), "charleston": (-79.93, 32.78), "pensacola": (-87.22, 30.42),
    "mobile": (-88.04, 30.69), "nueva_orleans": (-90.07, 29.95), "quebec": (-71.21, 46.81), "montreal": (-73.57, 45.50),
    "washington": (-77.04, 38.90),
    # oeste
    "san_luis": (-90.20, 38.63), "kansas_city": (-94.58, 39.10), "fort_mandan": (-101.27, 47.30), "astoria": (-123.83, 46.19),
    "new_echota": (-84.92, 34.54), "tahlequah": (-94.97, 35.91), "santa_fe": (-105.94, 35.69), "san_antonio": (-98.49, 29.42),
    "alamo": (-98.49, 29.42), "houston": (-95.37, 29.76), "san_diego": (-117.16, 32.72), "los_angeles": (-118.24, 34.05),
    "san_francisco": (-122.42, 37.77), "coloma": (-120.89, 38.80), "sacramento": (-121.49, 38.58), "salt_lake": (-111.89, 40.76),
    # guerra civil
    "fort_sumter": (-79.87, 32.75), "richmond": (-77.44, 37.54), "gettysburg": (-77.23, 39.83), "appomattox": (-78.80, 37.38),
    "atlanta": (-84.39, 33.75), "savannah": (-81.10, 32.08), "vicksburg": (-90.88, 32.35),
    # industria y siglo XX
    "promontory": (-112.55, 41.62), "omaha": (-95.93, 41.26), "chicago": (-87.63, 41.88), "pittsburgh": (-80.00, 40.44),
    "detroit": (-83.05, 42.33), "cleveland": (-81.69, 41.50), "menlo_park": (-74.33, 40.56), "ellis_island": (-74.04, 40.70),
    "kitty_hawk": (-75.67, 36.02), "la_habana": (-82.37, 23.11), "montgomery": (-86.30, 32.38), "cabo_canaveral": (-80.60, 28.40),
    "silicon_valley": (-122.03, 37.37), "seattle": (-122.33, 47.61), "miami": (-80.19, 25.76), "dallas": (-96.80, 32.78),
    "denver": (-104.99, 39.74), "phoenix": (-112.07, 33.45), "las_vegas": (-115.14, 36.17), "minneapolis": (-93.27, 44.98),
    "mexico_frontera": (-106.48, 31.74),
}

RUTAS = {
    "poblamiento": [(-126.6, 50.6), (-124.2, 46.5), (-121.0, 40.0), (-117.0, 35.0), (-111.0, 33.2), (-106.3, 32.8)],
    "espanoles_florida": [(-82.37, 23.11), (-80.6, 25.6), (-80.4, 27.6), (-81.31, 29.89)],
    "ingleses_jamestown": [(-63.4, 35.0), (-70.0, 36.4), (-76.0, 37.1), (-76.78, 37.21)],
    "esclavos": [(-63.4, 31.5), (-70.0, 34.0), (-75.0, 36.6), (-76.30, 37.00)],
    "mayflower": [(-63.4, 43.0), (-67.0, 42.4), (-69.8, 41.9), (-70.66, 41.96)],
    "barcos_te": [(-63.4, 41.6), (-67.5, 42.0), (-70.6, 42.3), (-71.06, 42.36)],
    "washington_sur": [(-74.00, 40.71), (-75.17, 39.95), (-77.04, 38.90), (-76.51, 37.24)],
    "flota_francia": [(-63.4, 36.4), (-70.0, 36.8), (-75.6, 37.0), (-76.2, 37.15)],
    "galvez": [(-90.07, 29.95), (-89.0, 30.3), (-88.04, 30.69), (-87.22, 30.42)],
    "lewis_clark": [(-90.20, 38.63), (-94.58, 39.10), (-95.93, 41.26), (-98.0, 43.0), (-100.6, 46.0), (-101.27, 47.30),
                    (-104.0, 48.0), (-110.6, 47.5), (-114.0, 46.9), (-116.9, 46.4), (-120.0, 45.7), (-123.83, 46.19)],
    "sendero_lagrimas": [(-84.92, 34.54), (-86.8, 36.2), (-88.5, 37.1), (-90.5, 37.3), (-92.4, 36.5), (-94.97, 35.91)],
    "kearny": [(-94.58, 39.10), (-100.0, 37.8), (-105.94, 35.69), (-110.5, 33.0), (-114.6, 32.7), (-117.16, 32.72)],
    "taylor_sur": [(-97.4, 27.8), (-97.5, 25.9), (-99.0, 25.0)],
    "fiebre_oro": [(-90.20, 38.63), (-95.93, 41.26), (-100.8, 41.1), (-104.8, 41.1), (-111.9, 41.2), (-117.0, 40.5), (-120.89, 38.80)],
    "oro_mar": [(-63.4, 30.0), (-72.0, 27.0), (-79.5, 24.0)],
    "sherman": [(-84.39, 33.75), (-83.2, 33.0), (-82.0, 32.6), (-81.10, 32.08)],
    "union_gettysburg": [(-77.04, 38.90), (-77.4, 39.4), (-77.23, 39.83)],
    "lee_gettysburg": [(-77.44, 37.54), (-78.2, 38.6), (-77.9, 39.5), (-77.23, 39.83)],
    "union_pacific": [(-95.93, 41.26), (-100.8, 41.1), (-104.8, 41.1), (-108.0, 41.6), (-111.0, 41.3), (-112.55, 41.62)],
    "central_pacific": [(-121.49, 38.58), (-119.8, 39.5), (-117.7, 40.9), (-115.0, 40.8), (-112.55, 41.62)],
    "ferro_este": [(-74.00, 40.71), (-80.00, 40.44), (-87.63, 41.88), (-95.93, 41.26)],
    "inmigrantes": [(-63.4, 39.6), (-68.0, 40.2), (-72.5, 40.5), (-74.04, 40.70)],
    "flota_1898": [(-80.19, 25.76), (-81.0, 24.4), (-82.37, 23.11)],
    "tropas_europa": [(-74.00, 40.71), (-69.0, 40.5), (-63.4, 41.0)],
    "pacifico_oeste": [(-122.42, 37.77), (-125.0, 35.0), (-126.8, 31.0)],
    "misiles_cuba": [(-82.37, 23.11), (-80.8, 25.2)],
}

CELDAS_SEMILLAS = {
    "naciones_nativas": [(-122.5, 46.0), (-119.5, 37.5), (-111.0, 35.0), (-108.0, 41.5), (-101.0, 45.5), (-98.0, 35.5),
                         (-90.5, 38.0), (-86.0, 33.0), (-79.0, 36.5), (-75.5, 43.0), (-70.0, 44.5), (-92.0, 46.5),
                         (-113.5, 45.5), (-103.0, 31.5), (-95.0, 30.5)],
}
CELDAS_PAISES = {}

# ------------------------------------------------------------------ polígonos históricos (lon, lat)
BOSQUE_ESTE = [
    (-96.6, 49.0), (-67.0, 47.6), (-66.8, 44.6), (-70.2, 41.2), (-75.8, 35.0), (-80.4, 25.0), (-82.2, 26.8), (-83.0, 29.2),
    (-90.0, 28.9), (-94.2, 29.4), (-97.4, 27.8), (-97.0, 29.6), (-98.3, 31.0), (-97.2, 32.6), (-98.0, 34.2),
    (-96.4, 35.6), (-97.3, 37.2), (-95.9, 38.6), (-96.6, 40.2), (-95.4, 41.8), (-96.3, 43.4), (-95.6, 45.0),
    (-96.8, 46.6), (-95.8, 47.8),
]
BOSQUE_NOROESTE = [
    (-124.8, 49.2), (-120.8, 49.2), (-121.4, 45.5), (-121.8, 41.8), (-123.0, 38.5), (-124.4, 40.2),
]
CAHOKIA_ZONA = [
    (-92.5, 40.5), (-87.0, 40.0), (-84.0, 36.5), (-81.5, 33.5), (-84.0, 30.6), (-91.0, 30.6), (-94.5, 33.5), (-95.0, 37.5),
]
PUEBLO_ZONA = [
    (-112.5, 38.8), (-106.5, 38.5), (-104.8, 35.5), (-106.5, 33.0), (-110.5, 33.5), (-113.0, 36.0),
]
IROQUESA = [
    (-80.0, 43.3), (-79.2, 44.0), (-75.6, 44.9), (-73.6, 43.6), (-73.8, 42.0), (-76.5, 41.9), (-79.8, 42.0),
]
FLORIDA_1565 = [
    (-87.6, 31.0), (-81.5, 31.2), (-80.0, 25.0), (-82.5, 24.4), (-87.6, 30.2),
]
FLORIDA_1783 = [
    (-91.6, 31.0), (-81.5, 30.75), (-80.0, 25.0), (-82.5, 24.4), (-89.6, 29.0), (-91.6, 30.0),
]
NUEVA_FRANCIA_SUR = [
    (-114.0, 49.0), (-95.0, 49.0), (-89.0, 48.0), (-82.0, 46.0), (-80.0, 42.0), (-80.0, 40.0), (-81.2, 37.0),
    (-84.0, 34.6), (-88.0, 30.3), (-94.0, 29.6), (-95.0, 33.5), (-100.0, 37.5), (-104.0, 38.5), (-106.0, 41.0),
    (-111.0, 44.5), (-114.0, 47.5),
]
NUEVA_FRANCIA_NORTE = [
    (-95.0, 51.2), (-62.8, 51.2), (-62.8, 45.4), (-67.2, 45.2), (-71.0, 45.0), (-75.0, 45.0), (-79.5, 43.5),
    (-83.0, 45.5), (-89.0, 48.0), (-95.0, 49.0),
]
EEUU_1783 = [
    (-95.2, 49.0), (-89.6, 48.0), (-84.0, 46.5), (-82.4, 43.0), (-79.0, 43.2), (-75.0, 45.0), (-71.5, 45.0), (-70.0, 46.5),
    (-67.8, 47.1), (-67.0, 44.8), (-65.5, 43.5), (-70.0, 40.0), (-76.0, 34.0), (-81.5, 30.7), (-84.9, 31.0), (-91.6, 31.0),
    (-91.2, 32.5), (-90.2, 35.0), (-89.2, 37.0), (-91.2, 40.0), (-91.0, 43.0), (-92.5, 46.5), (-95.2, 48.0),
]
LUISIANA_1803 = [
    (-114.0, 49.0), (-95.2, 49.0), (-95.2, 48.0), (-91.5, 47.3), (-89.6, 45.0), (-91.2, 43.0), (-91.4, 40.5),
    (-89.4, 37.0), (-90.4, 35.0), (-91.2, 31.0), (-89.6, 28.9), (-94.0, 29.6), (-94.0, 33.5), (-100.0, 36.5),
    (-103.0, 36.5), (-105.0, 38.5), (-106.5, 40.5), (-108.0, 42.0), (-111.0, 44.5), (-113.5, 47.0),
]
OREGON_1846 = [
    (-124.9, 49.0), (-114.0, 49.0), (-113.5, 47.0), (-111.0, 44.5), (-108.0, 42.0), (-124.9, 42.0),
]
NORTE_NOVOHISPANO = [
    (-124.6, 42.0), (-108.0, 42.0), (-106.5, 40.5), (-105.0, 38.5), (-103.0, 36.5), (-100.0, 36.5),
    (-94.0, 33.5), (-93.6, 29.5), (-97.0, 25.8), (-105.0, 25.0), (-117.2, 32.4), (-124.6, 38.0),
]
TEXAS_1836 = [
    (-103.5, 36.5), (-100.0, 36.5), (-94.0, 33.6), (-93.8, 29.6), (-97.1, 25.9),
    (-99.2, 26.5), (-101.5, 29.5), (-103.5, 32.0),
]
PERDIDO_1848 = [
    (-124.6, 42.0), (-108.0, 42.0), (-106.5, 40.5), (-105.0, 38.5), (-103.0, 36.5), (-103.0, 32.0),
    (-104.8, 30.6), (-106.5, 31.8), (-109.0, 31.3), (-114.8, 32.5), (-117.2, 32.5), (-124.6, 38.0),
]
CHEROKEE_TIERRAS = [
    (-86.5, 35.5), (-84.0, 35.8), (-82.8, 35.4), (-83.2, 34.6), (-84.5, 33.8), (-86.3, 34.0),
]

# estados reales (christa_pike/mapas/us_states.json, ∩ costa de Natural Earth)
TRECE = ("Massachusetts", "Maine", "New Hampshire", "Vermont", "Rhode Island", "Connecticut", "New York", "New Jersey",
         "Pennsylvania", "Delaware", "Maryland", "Virginia", "North Carolina", "South Carolina", "Georgia")
CONFEDERADOS = ("South Carolina", "Mississippi", "Florida", "Alabama", "Georgia", "Louisiana", "Texas", "Virginia",
                "Arkansas", "North Carolina", "Tennessee")
FRONTERIZOS = ("Maryland", "Delaware", "Kentucky", "Missouri", "West Virginia")
ALGODON = ("South Carolina", "Mississippi", "Alabama", "Georgia", "Louisiana")
LAGOS_SI = ("Lake Superior", "Lake Michigan", "Lake Huron", "Lake Erie", "Lake Ontario", "Great Salt Lake", "Lake Okeechobee",
            "Lake of the Woods", "Lake Winnipeg", "Lake Champlain")

# Ríos principales suplementarios (por si Natural Earth los corta)
RIOS_EXTRA = []


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
    "Mississippi": 9.6, "Missouri": 9.3, "Ohio": 9.2, "Rio Grande": 9.2, "Colorado": 9.1, "Columbia": 9.1, "Snake": 8.6,
    "Arkansas": 8.6, "Red": 8.3, "Tennessee": 8.5, "Platte": 8.2, "North Platte": 8.0, "Yellowstone": 8.2, "Hudson": 8.4,
    "St. Lawrence": 9.2, "Saint Lawrence": 9.2, "Sacramento": 8.2, "San Joaquin": 8.0, "Brazos": 8.0, "Gila": 8.0,
    "Susquehanna": 8.0, "Potomac": 8.1, "Savannah": 7.9, "Illinois": 7.9, "Wabash": 7.9, "Cumberland": 7.9,
}


def _paises(nombres):
    return [f["geometry"] for f in _PAISES["features"] if f["properties"]["NAME"] in nombres]


def _construir(rej):
    """Calcula todos los campos de la rejilla (se hace una vez y se guarda en datos/campos_us.npz)."""
    global _PAISES, _RIOS
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    _RIOS = json.load(open(F_RIOS, encoding="utf-8"))
    lagos = json.load(open(F_LAGOS, encoding="utf-8"))
    est = json.load(open(F_EST, encoding="utf-8"))
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    perm = [f["geometry"] for f in lagos["features"] if f["properties"].get("name") in LAGOS_SI]
    print("lagos:", sorted({f["properties"].get("name") for f in lagos["features"] if f["properties"].get("name") in LAGOS_SI}))
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

    def estados(*n):
        g = [f["geometry"] for f in est["features"] if f["properties"]["name"] in n]
        assert len(g) == len(n), (n, len(g))
        return cv2.bitwise_and(_mask_geoms(rej, g), eeuu)

    eeuu = paises("United States of America")
    mx = paises("Mexico")
    canada = paises("Canada")
    cuba = paises("Cuba")
    M["eeuu_mod"], M["mexico_mod"], M["canada"], M["cuba"] = eeuu, mx, canada, cuba

    M["valle"] = U_(P(BOSQUE_ESTE), P(BOSQUE_NOROESTE))
    M["cahokia"] = P(CAHOKIA_ZONA, eeuu)
    M["pueblo"] = P(PUEBLO_ZONA, eeuu)
    M["iroquesa"] = P(IROQUESA)
    M["florida_1565"] = P(FLORIDA_1565, eeuu)
    M["florida_1783"] = P(FLORIDA_1783, eeuu)
    trece = estados(*TRECE)
    M["trece"] = trece
    nf = U_(P(NUEVA_FRANCIA_SUR), P(NUEVA_FRANCIA_NORTE))
    M["nueva_francia"] = menos(nf, trece)
    norte_nh = cv2.bitwise_and(_mask_poli(rej, NORTE_NOVOHISPANO, mano=True), eeuu)
    M["nueva_espana"] = U_(norte_nh, M["florida_1565"], mx, cuba)
    M["espana_1783"] = U_(menos(P(LUISIANA_1803, eeuu), trece), norte_nh, M["florida_1783"], mx, cuba)
    e1783 = menos(P(EEUU_1783, eeuu), M["florida_1783"])
    M["eeuu_1783"] = e1783
    luis = menos(P(LUISIANA_1803, eeuu), e1783, norte_nh)
    M["luisiana_1803"] = luis
    M["eeuu_1803"] = U_(e1783, luis)
    M["eeuu_1819"] = U_(M["eeuu_1803"], M["florida_1783"])
    texas = cv2.bitwise_and(_mask_poli(rej, TEXAS_1836, mano=True), eeuu)
    perdido = cv2.bitwise_and(_mask_poli(rej, PERDIDO_1848, mano=True), eeuu)
    M["texas_1836"] = texas
    M["mexico_1824"] = U_(mx, norte_nh)
    M["mexico_1836"] = menos(M["mexico_1824"], texas)
    M["perdido_1848"] = menos(perdido, texas)
    M["oregon_1846"] = menos(P(OREGON_1846, eeuu), norte_nh)
    M["eeuu_1845"] = U_(M["eeuu_1819"], texas)
    M["eeuu_1846"] = menos(eeuu, M["perdido_1848"])
    M["cherokee"] = P(CHEROKEE_TIERRAS, eeuu)
    M["territorio_indio"] = estados("Oklahoma")
    conf = estados(*CONFEDERADOS)
    M["confederacion"] = conf
    M["fronterizos"] = estados(*FRONTERIZOS)
    M["union"] = menos(eeuu, conf)
    M["algodon"] = estados(*ALGODON)
    M["norte_industrial"] = estados("Massachusetts", "New York", "Pennsylvania", "New Jersey", "Connecticut", "Rhode Island",
                                    "Ohio", "Illinois", "Michigan", "Indiana", "New Hampshire", "Vermont", "Maine")

    # fractura por estados reales (índice 1..48 por estado contiguo; 0 = fuera)
    idx = np.zeros((rej.FH, rej.FW), np.uint8)
    nombres = sorted(f["properties"]["name"] for f in est["features"]
                     if f["properties"]["name"] not in ("Alaska", "Hawaii", "Puerto Rico", "District of Columbia"))
    for k, n in enumerate(nombres, 1):
        idx[estados(n) > 127] = k
    idx[eeuu <= 127] = 0

    campos = {k: _i16(_sdf(v)) for k, v in M.items()}
    aux = _relieve(rej, tierra)
    rios = _rios(rej)
    return campos, {"est_idx": idx}, aux, rios


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


def preparar(nombres=("us",)):
    os.makedirs(DATOS, exist_ok=True)
    for n in nombres:
        rej = REJ[n]
        campos, cel, aux, rios = _construir(rej)
        datos = {f"c_{k}": v for k, v in campos.items()}
        datos["aux"] = aux.astype(np.float16)
        datos["rios_pts"] = np.concatenate([r[0] for r in rios]).astype(np.float32)
        datos["rios_cortes"] = np.cumsum([0] + [len(r[0]) for r in rios]).astype(np.int64)
        datos["rios_peso"] = np.array([r[1] for r in rios], np.float32)
        for k, v in cel.items():
            datos[k] = v
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
    rej.est_idx = d["est_idx"] if "est_idx" in d.files else None
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


def usar(nombre="us"):
    global ACT, CAMPOS, CELDAS, LON0, LON1, LAT0, LAT1, FW, FH
    rej = REJ["us"]
    _cargar_rej(rej)
    ACT = rej
    CAMPOS = rej.campos
    CELDAS = dict(CELDAS_SEMILLAS)
    LON0, LON1, LAT0, LAT1, FW, FH = rej.lon0, rej.lon1, rej.lat0, rej.lat1, rej.FW, rej.FH


def cargar():
    _cargar_rej(REJ["us"])
    if ACT is None:
        usar("us")


def proj(lon, lat):
    return ACT.proj(lon, lat)


def proj_pts(P):
    return ACT.proj_pts(P)


def celdas(nombre):
    rej = ACT
    if nombre in rej._cel:
        return rej._cel[nombre]
    if nombre == "estados":
        idx = rej.est_idx
        cambio = np.zeros(idx.shape, np.uint8)
        cambio[:, 1:] |= (idx[:, 1:] != idx[:, :-1])
        cambio[1:, :] |= (idx[1:, :] != idx[:-1, :])
        borde = cv2.distanceTransform((1 - cambio).astype(np.uint8), cv2.DIST_L2, 5).astype(np.float32)
        rej._cel[nombre] = (idx, borde)
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

    def __init__(self, lon=-96.0, lat=38.0, z=2.2, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.rej = ACT if ACT is not None else REJ["us"]
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
    """Fondo: mar con profundidad, tierra con relieve (Rocosas, Apalaches) y el bosque oriental y del noroeste."""
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
