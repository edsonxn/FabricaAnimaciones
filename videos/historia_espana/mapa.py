# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de España en 5 minutos», con RELIEVE REAL y dos rejillas.

Campos de distancia con signo (SDF, negativo = dentro) sobre rejillas en proyección de MERCATOR (conforme: la península y Sudamérica
conservan su forma y las dos rejillas casan entre sí al fundirse):
  - "eu": península, Europa occidental y el norte de África (lon -20..23, lat 56..30.5), 46 px por grado ecuatorial (≈60 px por grado
    a la latitud de España). Bajo el guache: relieve y batimetría NOAA ETOPO1 (1') y ríos calculados del propio relieve (nucleo/datos/relieve_eu.npz).
  - "am": del Pacífico occidental a Iberia, pasando por América (lon 100E → 22E, envuelta; lat 56..-57), 11 px por grado, ríos de Natural Earth.
`usar(nombre)` activa una rejilla: las variables y funciones del módulo pasan a ser las de esa rejilla (core.py y reg.py no cambian).
Los campos se calculan una vez (`python mapa.py`) y se guardan en datos/campos_<rejilla>.npz (int16, 1/8 de px).
Unidades: los campos se proyectan a pantalla en PÍXELES DE PANTALLA (S * zoom nativo), así los bordes y sombras miden lo mismo a cualquier zoom.
Fuentes: Natural Earth 50 m (tierra, países, ríos; dominio público), NOAA ETOPO1 (dominio público).
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
F_REL = os.path.join(RAIZ, "nucleo", "datos", "relieve_eu.npz")
DATOS = os.path.join(AQUI, "datos")
ESC_I16 = 8.0                        # los campos se guardan en int16 con 1/8 px de resolución


# ------------------------------------------------------------------ proyección de Mercator
def ymerc(lat):
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.asarray(lat, float)) / 2)))


def inv_ymerc(y):
    return np.degrees(2 * np.arctan(np.exp(np.radians(np.asarray(y, float)))) - np.pi / 2)


def U(lon):
    """Longitud «desenvuelta» (100..420): la cámara interpola aquí, así va de Iberia a Filipinas cruzando América y el Pacífico."""
    lon = np.asarray(lon, float)
    return np.where(lon < 60, lon + 360, lon)


def desU(u):
    return ((np.asarray(u, float) + 180.0) % 360.0) - 180.0


class Rej:
    def __init__(self, nombre, lon0, lon1, lat0, lat1, pxdeg, envuelve):
        self.nombre, self.lon0, self.lon1, self.lat0, self.lat1 = nombre, lon0, lon1, lat0, lat1
        self.pxdeg, self.envuelve = pxdeg, envuelve
        self.Y0 = float(ymerc(lat0))
        self.FW = int(round((lon1 - lon0) * pxdeg))
        self.FH = int(round((self.Y0 - float(ymerc(lat1))) * pxdeg))
        self.campos = {}
        self.aux = None              # (FH, FW, 3) float32: luz del relieve, altitud 0..1, profundidad 0..1
        self.rios = []               # [(P lon/lat, peso)]
        self.celdas_def = {}
        self._cel = {}

    def nat(self, lon):
        lon = np.asarray(lon, float)
        return np.where(lon < 60, lon + 360, lon) if self.envuelve else lon

    def proj(self, lon, lat):
        return (self.nat(lon) - self.lon0) * self.pxdeg, (self.Y0 - ymerc(lat)) * self.pxdeg

    def proj_pts(self, P):
        P = np.asarray(P, float)
        x, y = self.proj(P[:, 0], P[:, 1])
        return np.stack([x, y], 1)

    def inv(self, x, y):
        """px del campo -> (lon nativa, lat)."""
        return self.lon0 + np.asarray(x, float) / self.pxdeg, inv_ymerc(self.Y0 - np.asarray(y, float) / self.pxdeg)


REJ = {
    "eu": Rej("eu", -20.0, 23.0, 56.0, 30.5, 46.0, False),
    "am": Rej("am", 100.0, 382.0, 56.0, -57.0, 11.0, True),
}
PXDEG_REF = REJ["eu"].pxdeg          # el zoom de la cámara se expresa siempre en píxeles de pantalla por píxel de la rejilla "eu"

# ------------------------------------------------------------------ paleta de guache (apagada y cálida)
MAR = (176, 208, 214)
MAR_HONDO = (150, 186, 204)
MAR_CL = (206, 228, 226)
TIERRA = (236, 224, 194)
TIERRA_ALTA = (214, 194, 156)
TIERRA_CUMBRE = (236, 232, 222)
RIO = (122, 170, 196)
COL = {
    "iberos": (214, 140, 80), "celtas": (122, 150, 104), "fenicios": (150, 92, 150), "cartago": (176, 112, 160), "roma": (198, 70, 62),
    "visigodos": (196, 150, 64), "andalus": (86, 150, 112), "omeyas": (110, 160, 120), "asturias": (120, 110, 168), "leon": (138, 96, 160),
    "castilla": (150, 80, 150), "navarra": (196, 76, 76), "aragon": (232, 180, 60), "cataluna": (226, 150, 64), "portugal": (78, 156, 150),
    "granada": (70, 140, 100), "espana": (206, 70, 58), "imperio": (210, 86, 60), "austrias": (204, 84, 60), "borbon": (70, 110, 180),
    "francia": (84, 120, 190), "gb": (190, 72, 80), "eeuu": (96, 128, 176), "republica": (150, 90, 160), "nacional": (98, 104, 92),
    "franco": (138, 132, 118), "democracia": (214, 84, 64), "hispano": (232, 160, 60), "independiente": (120, 170, 120), "taifas": (86, 150, 112),
}
COL_CELDAS = [(214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
              (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110)]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat)
CIUDADES = {
    "madrid": (-3.70, 40.42), "toledo": (-4.02, 39.86), "cordoba": (-4.78, 37.88), "sevilla": (-5.98, 37.39), "granada": (-3.60, 37.18),
    "cadiz": (-6.29, 36.53), "barcelona": (2.17, 41.39), "valencia": (-0.38, 39.47), "zaragoza": (-0.88, 41.65), "cartagena": (-0.98, 37.60),
    "merida": (-6.34, 38.92), "segovia": (-4.12, 40.95), "numancia": (-2.44, 41.81), "italica": (-6.04, 37.44), "covadonga": (-5.05, 43.31),
    "atapuerca": (-3.52, 42.35), "altamira": (-4.12, 43.38), "palos": (-6.89, 37.23), "gibraltar": (-5.35, 36.14), "guernica": (-2.68, 43.32),
    "lisboa": (-9.14, 38.72), "roma": (12.50, 41.90), "cartago": (10.32, 36.85), "paris": (2.35, 48.86), "bruselas": (4.35, 50.85),
    "milan": (9.19, 45.46), "napoles": (14.27, 40.85), "lepanto": (21.83, 38.39), "londres": (-0.13, 51.51), "ampurias": (3.11, 42.13),
    "malaga": (-4.42, 36.72), "tanger": (-5.81, 35.77), "ceuta": (-5.32, 35.89), "guadalete": (-5.95, 36.65), "navas": (-3.58, 38.28),
    "burgos": (-3.70, 42.34), "leon": (-5.57, 42.60), "oviedo": (-5.84, 43.36), "pamplona": (-1.64, 42.81), "tarragona": (1.25, 41.12),
    "salamanca": (-5.66, 40.97), "valladolid": (-4.72, 41.65), "bayona": (-1.47, 43.49), "consuegra": (-3.61, 39.46), "benidorm": (-0.13, 38.54),
    "sanmillan": (-2.86, 42.33), "badajoz": (-6.97, 38.88), "alhambra": (-3.59, 37.18), "elche": (-0.70, 38.27), "baleares": (2.9, 39.6), "almeria": (-2.46, 36.84),
    # América, Pacífico
    "guanahani": (-74.5, 24.05), "santo_domingo": (-69.9, 18.47), "habana": (-82.36, 23.13), "tenochtitlan": (-99.13, 19.43), "veracruz": (-96.13, 19.19),
    "acapulco": (-99.88, 16.85), "cuzco": (-71.97, -13.53), "lima": (-77.04, -12.05), "potosi": (-65.75, -19.58), "zacatecas": (-102.57, 22.77),
    "panama": (-79.52, 8.98), "portobelo": (-79.65, 9.55), "cartagena_ind": (-75.51, 10.39), "manila": (120.98, 14.6), "buenos_aires": (-58.38, -34.6),
    "bogota": (-74.07, 4.71), "caracas": (-66.9, 10.48), "santiago": (-70.65, -33.45), "quito": (-78.47, -0.18), "mexico": (-99.13, 19.43),
    "san_juan": (-66.1, 18.47), "canarias": (-15.4, 28.1), "cajamarca": (-78.5, -7.16), "arica": (-70.3, -18.48), "callao": (-77.15, -12.05),
    "washington": (-77.04, 38.9), "malabo": (8.78, 3.75),
}
RUTAS = {
    "fenicios": [(24.0, 35.0), (16.0, 36.4), (10.6, 37.3), (4.0, 37.2), (-2.0, 36.5), (-5.6, 36.0), (-6.25, 36.5)],
    "griegos": [(22.0, 37.6), (15.6, 38.2), (12.0, 39.5), (8.8, 41.4), (6.2, 42.6), (3.2, 42.15)],
    "anibal": [(-0.98, 37.60), (-0.38, 39.47), (0.9, 40.9), (2.17, 41.5), (2.9, 42.4), (3.3, 43.1), (4.6, 43.7), (6.0, 44.6), (6.9, 45.1),
               (7.7, 45.0), (9.2, 44.9), (11.0, 44.0), (12.0, 42.8), (12.5, 41.9)],
    "roma_desembarco": [(12.3, 41.6), (9.0, 41.8), (5.5, 42.0), (3.1, 42.1)],
    "via_augusta": [(-6.29, 36.53), (-5.98, 37.39), (-4.78, 37.88), (-3.8, 38.0), (-2.6, 38.5), (-1.3, 38.9), (-0.38, 39.47), (0.0, 40.0),
                    (0.5, 40.7), (1.25, 41.12), (2.17, 41.39), (2.8, 42.0), (3.0, 42.45)],
    "via_plata": [(-5.98, 37.39), (-6.34, 38.92), (-6.2, 39.6), (-6.0, 40.4), (-5.66, 40.97), (-5.8, 41.5), (-6.06, 42.46)],
    "tariq": [(-5.32, 35.89), (-5.37, 36.05), (-5.35, 36.14)],
    "conquista_711": [(-5.35, 36.14), (-5.85, 36.6), (-5.3, 37.3), (-4.78, 37.88), (-4.3, 38.9), (-4.02, 39.86)],
    "colon": [(-6.89, 37.23), (-8.6, 35.0), (-13.0, 30.5), (-17.2, 28.1), (-30.0, 27.0), (-50.0, 26.2), (-65.0, 25.0), (-74.5, 24.05)],
    "cortes": [(-96.13, 19.19), (-97.3, 19.4), (-98.2, 19.3), (-99.13, 19.43)],
    "pizarro": [(-79.5, 8.9), (-80.5, 3.5), (-80.6, -2.5), (-80.6, -5.1), (-78.5, -7.16), (-76.5, -11.0), (-71.97, -13.53)],
    "flota_mx": [(-102.57, 22.77), (-99.13, 19.43), (-96.13, 19.19), (-90.0, 22.0), (-84.0, 23.6), (-82.36, 23.13), (-79.0, 26.0),
                 (-70.0, 32.0), (-50.0, 36.5), (-28.0, 38.0), (-12.0, 37.0), (-6.4, 36.8), (-5.98, 37.39)],
    "flota_peru": [(-65.75, -19.58), (-70.3, -18.48), (-74.0, -15.0), (-77.15, -12.05), (-80.0, -4.0), (-80.5, 2.0), (-79.52, 8.98),
                   (-79.65, 9.55), (-78.0, 11.5), (-75.51, 10.39), (-78.0, 16.0), (-82.36, 23.13)],
    "galeon_manila": [(-99.88, 16.85), (-110.0, 14.5), (-130.0, 13.0), (-160.0, 13.0), (175.0, 13.5), (145.0, 13.4), (128.0, 13.0), (124.0, 12.6),
                      (120.98, 14.6)],
    "tornaviaje": [(120.98, 14.6), (125.0, 18.0), (140.0, 34.0), (160.0, 40.0), (-170.0, 41.0), (-140.0, 38.0), (-120.0, 30.0), (-110.0, 22.0),
                   (-99.88, 16.85)],
    "armada": [(-6.0, 47.4), (-4.6, 49.1), (-2.0, 49.8), (0.5, 50.25), (1.6, 50.8), (2.0, 51.4)],
    "lepanto": [(15.6, 38.2), (18.5, 38.6), (20.8, 38.3), (21.4, 38.3)],
    "borbon": [(2.35, 48.86), (0.7, 46.6), (-0.6, 44.84), (-1.47, 43.49), (-2.7, 42.85), (-3.70, 42.34), (-3.70, 40.42)],
    "napoleon": [(2.35, 48.86), (0.7, 46.6), (-0.6, 44.84), (-1.47, 43.49), (-2.7, 42.85), (-3.70, 42.34), (-3.70, 40.42)],
    "eeuu_cuba": [(-77.04, 38.9), (-79.5, 32.0), (-80.6, 26.0), (-82.36, 23.13)],
    "eeuu_filipinas": [(-122.4, 37.8), (-140.0, 30.0), (-160.0, 21.3), (175.0, 18.0), (145.0, 14.5), (125.0, 14.4), (120.98, 14.6)],
}
# semillas de los reinos de taifas (1031) (lon, lat): Badajoz, Toledo, Zaragoza, Sevilla, Córdoba, Granada, Málaga, Almería, Denia, Valencia, Murcia, Lérida, Albarracín
CELDAS_SEMILLAS = {
    "taifas": [(-6.97, 38.88), (-4.02, 39.86), (-0.88, 41.65), (-5.98, 37.39), (-4.78, 37.88), (-3.60, 37.18), (-4.42, 36.72), (-2.46, 36.84),
               (0.10, 38.84), (-0.38, 39.47), (-1.13, 37.98), (0.62, 41.61), (-1.44, 40.41), (-8.0, 37.1), (-2.2, 40.0)],
}
# fractura por FRONTERAS REALES: celda = país de Natural Earth (rejilla "am")
CELDAS_PAISES = {
    "independencias": ["Mexico", "Guatemala", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama", "Colombia", "Venezuela", "Ecuador",
                       "Peru", "Bolivia", "Chile", "Argentina", "Paraguay", "Uruguay", "Dominican Rep.", "Cuba", "Puerto Rico", "Philippines", "Spain"],
}
QUEDAN_1825 = ("Cuba", "Puerto Rico", "Philippines", "Spain")

# ------------------------------------------------------------------ polígonos de las épocas (lon, lat): se recortan con la península/tierra
POLI = {
    "iberos": [(3.6, 43.5), (2.0, 42.6), (1.0, 42.3), (0.0, 41.9), (-0.9, 41.6), (-1.5, 41.0), (-1.8, 40.0), (-2.3, 39.0), (-3.2, 38.6), (-4.5, 38.3),
               (-6.0, 38.0), (-7.0, 37.6), (-7.5, 37.0), (-7.6, 35.5), (4.5, 35.5), (4.5, 43.5)],
    "cartago_hisp": [(-7.6, 36.5), (-7.5, 37.3), (-6.5, 38.0), (-5.0, 38.4), (-3.6, 38.9), (-2.0, 39.6), (-0.9, 40.4), (0.6, 40.9), (1.5, 40.5),
                     (1.5, 38.5), (-1.0, 35.8), (-7.6, 35.5)],
    "cartago_afr": [(8.4, 37.4), (11.3, 37.4), (11.3, 35.5), (10.6, 34.0), (12.0, 32.8), (8.0, 34.0), (8.2, 36.5)],
    "hispania_197": [(3.6, 42.6), (1.5, 42.5), (0.0, 41.9), (-1.0, 41.6), (-1.8, 40.8), (-2.6, 39.5), (-3.8, 38.7), (-5.2, 38.3), (-6.5, 37.9),
                     (-7.5, 37.3), (-7.6, 35.5), (4.6, 35.5), (4.6, 42.6)],
    "norte_133": [(-10.5, 41.1), (-7.0, 41.4), (-5.5, 41.8), (-4.2, 42.1), (-3.0, 42.6), (-1.9, 42.8), (-1.2, 43.0), (-0.5, 43.3), (-0.5, 44.5), (-10.5, 44.5)],
    "septimania": [(1.7, 42.45), (3.2, 42.45), (4.8, 43.4), (4.6, 44.0), (3.3, 44.0), (2.0, 43.6), (1.7, 42.9)],
    "andalus_711": [(-6.6, 35.8), (-6.6, 37.2), (-4.6, 37.3), (-4.4, 35.8)],
    "asturias_722": [(-7.4, 44.0), (-7.08, 43.5), (-7.0, 43.12), (-6.85, 42.86), (-6.4, 42.96), (-5.9, 43.0), (-5.4, 43.03), (-4.95, 43.06),
                     (-4.5, 43.0), (-4.1, 42.97), (-3.8, 43.06), (-3.55, 43.16), (-3.38, 43.3), (-3.3, 44.0)],
    "vasconia": [(-3.3, 44.0), (-3.2, 43.0), (-1.8, 42.7), (-0.8, 42.75), (-0.6, 44.0)],
    "leon_1000": [(-10.0, 44.5), (-10.0, 41.0), (-7.0, 41.1), (-6.0, 41.4), (-5.0, 41.6), (-4.0, 41.55), (-3.3, 41.6), (-2.7, 41.9), (-2.7, 42.4),
                  (-3.0, 42.9), (-3.1, 44.0)],
    "navarra_1000": [(-3.1, 44.0), (-3.0, 42.9), (-2.7, 42.4), (-2.0, 42.15), (-1.0, 42.25), (0.3, 42.3), (0.4, 43.5), (-1.5, 44.0)],
    "cataluna_1000": [(0.4, 43.5), (0.3, 42.3), (0.9, 41.9), (1.4, 41.6), (1.9, 41.3), (3.6, 41.3), (3.6, 43.5)],
    "castilla_1100": [(-10.0, 44.5), (-10.0, 40.15), (-8.6, 40.15), (-7.5, 40.1), (-6.6, 40.0), (-5.6, 39.95), (-4.8, 39.85), (-4.0, 39.75), (-3.3, 39.85),
                      (-2.6, 40.1), (-2.2, 40.6), (-2.0, 41.1), (-2.0, 42.0), (-2.4, 42.6), (-3.1, 44.0)],
    "aragon_1100": [(-3.1, 44.0), (-2.4, 42.6), (-2.0, 42.15), (-1.0, 42.25), (-0.3, 42.05), (0.3, 42.0), (0.4, 43.5), (-1.5, 44.0)],
    "cataluna_1100": [(0.4, 43.5), (0.3, 42.0), (0.8, 41.8), (1.3, 41.4), (1.6, 41.2), (3.6, 41.2), (3.6, 43.5)],
    "aragon_1250": [(-1.0, 43.5), (-1.0, 42.85), (-1.15, 42.4), (-1.65, 41.95), (-1.95, 41.5), (-1.85, 41.0), (-1.75, 40.45), (-1.5, 40.1), (-1.3, 39.6),
                    (-1.1, 39.0), (-0.95, 38.65), (-0.2, 38.55), (0.5, 38.35), (4.6, 38.35), (4.6, 43.5)],
    "navarra_1250": [(-2.5, 43.5), (-2.45, 42.6), (-2.0, 42.05), (-1.65, 41.95), (-1.15, 42.4), (-1.0, 42.85), (-1.0, 43.5)],
    "granada": [(-5.65, 35.8), (-5.65, 36.0), (-5.6, 36.45), (-5.3, 36.85), (-4.95, 37.15), (-4.4, 37.45), (-3.9, 37.6), (-3.3, 37.8), (-2.7, 37.75),
                (-2.2, 37.65), (-1.75, 37.5), (-1.5, 37.2), (-1.5, 35.8)],
    "cadiz_libre": [(-6.45, 36.35), (-6.45, 36.65), (-6.05, 36.65), (-6.05, 36.35)],
    "franco_comte": [(5.3, 46.25), (5.3, 47.9), (6.4, 48.0), (7.1, 47.5), (6.5, 46.4)],
    "milan": [(8.5, 44.75), (8.4, 45.9), (9.3, 46.4), (10.5, 46.2), (10.6, 45.0), (9.5, 44.7)],
    "napoles": [(13.0, 41.9), (14.0, 42.2), (14.8, 41.95), (16.2, 41.9), (18.6, 40.3), (18.6, 37.8), (15.5, 37.8), (13.0, 41.1)],
    "sicilia": [(12.0, 36.5), (12.0, 38.4), (15.8, 38.4), (15.8, 36.5)],
    "cerdena": [(8.0, 38.8), (8.0, 41.3), (10.0, 41.3), (10.0, 38.8)],
    # Guerra Civil: zona sublevada en julio de 1936 y la República partida en dos (abril de 1938)
    "nac36_norte": [(-10.0, 44.5), (-10.0, 39.25), (-6.4, 39.25), (-5.8, 39.4), (-5.4, 39.95), (-4.8, 40.25), (-4.3, 40.6), (-3.9, 40.85), (-3.2, 41.1),
                    (-2.3, 41.0), (-1.6, 40.4), (-1.0, 40.4), (-0.9, 41.1), (-0.6, 41.7), (-0.3, 42.2), (-0.2, 42.8), (-0.8, 42.95), (-1.4, 43.3),
                    (-2.0, 43.05), (-2.9, 42.95), (-3.2, 42.9), (-3.6, 43.0), (-4.2, 42.95), (-4.9, 43.05), (-6.0, 42.9), (-6.9, 43.0), (-7.05, 43.8),
                    (-7.1, 44.5)],
    "nac36_sur": [(-7.6, 35.9), (-7.6, 37.6), (-6.5, 37.9), (-5.5, 37.95), (-4.8, 37.95), (-5.0, 37.3), (-5.3, 36.85), (-5.5, 36.4), (-5.45, 35.9)],
    "nac36_baleares": [(1.0, 38.5), (1.0, 40.2), (3.6, 40.2), (3.6, 38.5)],
    "rep38_centro": [(-3.9, 40.75), (-3.0, 40.95), (-2.2, 40.95), (-1.6, 40.5), (-1.0, 40.2), (-0.4, 39.85), (0.6, 39.85), (0.6, 36.4), (-2.5, 36.55),
                     (-3.4, 36.7), (-3.7, 37.0), (-3.75, 37.6), (-4.1, 38.0), (-4.9, 38.2), (-5.4, 38.6), (-5.6, 39.0), (-4.8, 39.4), (-4.3, 39.8),
                     (-4.0, 40.2), (-4.1, 40.45)],
    "rep38_cat": [(3.6, 43.0), (0.7, 42.9), (0.6, 42.0), (0.65, 41.6), (0.5, 41.2), (0.6, 40.8), (1.0, 40.55), (3.6, 40.55)],
    "menorca": [(3.75, 39.75), (3.75, 40.15), (4.4, 40.15), (4.4, 39.75)],
    # América
    "nueva_espana_norte": [(-124.6, 42.0), (-106.0, 42.0), (-106.0, 38.5), (-100.0, 37.5), (-100.0, 34.5), (-94.0, 33.6), (-94.0, 31.9), (-93.8, 29.7),
                           (-95.0, 26.0), (-125.0, 26.0)],
    "mexico_1525": [(-106.0, 22.6), (-97.0, 22.6), (-86.0, 22.6), (-86.0, 14.0), (-106.0, 14.0)],
    "mexico_1550": [(-110.0, 25.0), (-96.0, 25.0), (-86.0, 25.0), (-86.0, 14.0), (-110.0, 14.0)],
    "chile_1550": [(-80.0, -17.0), (-66.0, -17.0), (-66.0, -38.0), (-80.0, -38.0)],
    "argentina_1600": [(-75.0, -21.0), (-53.0, -21.0), (-53.0, -38.5), (-75.0, -38.5)],
}


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
                for sh in ((0.0, 360.0) if rej.envuelve else (0.0,)):
                    x = (P[:, 0] + sh - rej.lon0) * rej.pxdeg
                    if x.max() < -50 or x.min() > rej.FW + 50:
                        continue
                    y = (rej.Y0 - ymerc(np.clip(P[:, 1], -85, 85))) * rej.pxdeg
                    I.append(np.rint(np.stack([x, y], 1) * 4).astype(np.int32).reshape(-1, 1, 2))
            if I:
                cv2.fillPoly(m, I, 255, cv2.LINE_8, 2)
    return m


def _mano(pts, paso=0.04, amp=0.10):
    """Frontera "natural": subdivide el polígono y lo desplaza con un campo de ruido que depende solo de (lon, lat),
    así dos polígonos que comparten un lado siguen encajando."""
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
    """Campo de distancia con signo (negativo dentro) de una máscara uint8, suavizado (px de la rejilla)."""
    b = (m > 127).astype(np.uint8)
    if b.max() == 0:
        return np.full(m.shape, 4000.0, np.float32)
    din = cv2.distanceTransform(b, cv2.DIST_L2, 5)
    dout = cv2.distanceTransform(1 - b, cv2.DIST_L2, 5)
    return cv2.GaussianBlur((dout - din).astype(np.float32), (0, 0), 1.3)


def _i16(s):
    return np.clip(np.rint(s * ESC_I16), -32000, 32000).astype(np.int16)


def _paises(nombres):
    return [f["geometry"] for f in _PAISES["features"] if f["properties"]["NAME"] in nombres]


_PAISES = None


def _construir(rej):
    """Calcula todos los campos de la rejilla (lento: se hace una vez y se guarda)."""
    global _PAISES
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    M = {}
    tierra = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    M["tierra"] = tierra

    def P(nombre, base):
        return cv2.bitwise_and(_mask_poli(rej, POLI[nombre]), base)

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

    espana = _mask_geoms(rej, _paises(("Spain",)))
    portugal = _mask_geoms(rej, _paises(("Portugal",)))
    andorra = _mask_geoms(rej, _paises(("Andorra",)))
    caja_pen = _mask_poli(rej, [(-10.0, 35.95), (-10.0, 44.2), (4.6, 44.2), (4.6, 35.95)], mano=False)
    pen = cv2.bitwise_and(U_(espana, portugal, andorra), caja_pen)
    M["espana"] = espana
    M["peninsula"] = pen
    M["portugal"] = cv2.bitwise_and(portugal, caja_pen)
    if rej.nombre == "eu":
        M["iberos"] = P("iberos", pen)
        M["celtas"] = menos(pen, M["iberos"])
        M["cartago"] = U_(P("cartago_hisp", pen), P("cartago_afr", tierra))
        italia = _mask_geoms(rej, _paises(("Italy",)))
        M["roma_italia"] = cv2.bitwise_and(italia, _mask_poli(rej, [(6.0, 36.0), (6.0, 44.4), (19.0, 44.4), (19.0, 36.0)]))
        M["hispania_197"] = U_(P("hispania_197", pen), M["roma_italia"])
        M["hispania_133"] = U_(menos(pen, P("norte_133", pen)), M["roma_italia"])
        M["hispania_19"] = U_(pen, M["roma_italia"])
        M["visigodos"] = U_(pen, P("septimania", tierra))
        magreb = cv2.bitwise_and(_mask_geoms(rej, _paises(("Morocco", "Algeria", "Tunisia", "Libya", "W. Sahara"))),
                                 _mask_poli(rej, [(-12, 30.6), (-12, 37.6), (16, 37.6), (16, 30.6)], mano=False))
        M["omeyas_afr"] = magreb
        M["andalus_711"] = U_(P("andalus_711", pen), magreb)
        M["asturias_722"] = P("asturias_722", pen)
        M["andalus_718"] = U_(menos(pen, M["asturias_722"], P("vasconia", pen)), magreb)
        M["leon_1000"] = P("leon_1000", pen)
        M["navarra_1000"] = P("navarra_1000", pen)
        M["cataluna_1000"] = P("cataluna_1000", tierra)
        M["andalus_1000"] = menos(pen, M["leon_1000"], M["navarra_1000"], M["cataluna_1000"])
        M["castilla_1100"] = P("castilla_1100", pen)
        M["aragon_1100"] = P("aragon_1100", pen)
        M["cataluna_1100"] = P("cataluna_1100", tierra)
        M["andalus_1100"] = menos(pen, M["castilla_1100"], M["aragon_1100"], M["cataluna_1100"])
        M["portugal_1250"] = M["portugal"]
        M["aragon_1250"] = P("aragon_1250", pen)
        M["navarra_1250"] = P("navarra_1250", pen)
        M["granada"] = P("granada", pen)
        M["castilla_1250"] = menos(pen, M["portugal"], M["aragon_1250"], M["navarra_1250"], M["granada"])
        M["castilla_1492"] = U_(M["castilla_1250"], M["granada"])
        M["espana_1492"] = U_(M["castilla_1492"], M["aragon_1250"])
        M["espana_1512"] = U_(M["espana_1492"], M["navarra_1250"])
        posesiones = U_(_mask_geoms(rej, _paises(("Netherlands", "Belgium", "Luxembourg"))), P("franco_comte", tierra), P("milan", tierra),
                        P("napoles", italia), P("sicilia", italia), P("cerdena", italia))
        M["posesiones"] = posesiones
        M["austrias"] = U_(M["espana_1512"], posesiones)
        M["francia"] = _mask_geoms(rej, _paises(("France",)))
        M["ocupada_1810"] = U_(menos(M["espana"], P("cadiz_libre", tierra)), M["francia"])
        M["espana_peq"] = M["espana"]
        M["nac36"] = cv2.bitwise_and(U_(P("nac36_norte", tierra), P("nac36_sur", tierra), P("nac36_baleares", tierra)), espana)
        M["rep36"] = menos(espana, M["nac36"])
        rep38 = cv2.bitwise_and(U_(P("rep38_centro", tierra), P("rep38_cat", tierra), P("menorca", tierra)), espana)
        M["rep38"] = rep38
        M["nac38"] = menos(espana, rep38)
        M["ue"] = U_(_mask_geoms(rej, _paises(("France", "Germany", "Italy", "Belgium", "Netherlands", "Luxembourg", "Denmark", "Ireland",
                                                  "United Kingdom", "Greece", "Portugal"))))
    else:
        def paises(*n):
            return _mask_geoms(rej, _paises(n))
        islas = paises("Cuba", "Dominican Rep.", "Haiti", "Puerto Rico", "Jamaica")
        centro = paises("Guatemala", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama", "Belize")
        mex = paises("Mexico")
        sur_1550 = paises("Colombia", "Venezuela", "Ecuador", "Peru", "Bolivia", "Paraguay")
        chile = paises("Chile")
        arg_uru = paises("Argentina", "Uruguay")
        usa = paises("United States of America")
        filip = paises("Philippines")
        M["am_1500"] = U_(pen, islas)
        M["am_1525"] = U_(M["am_1500"], P("mexico_1525", mex), centro)
        M["am_1550"] = U_(M["am_1525"], P("mexico_1550", mex), sur_1550, P("chile_1550", chile))
        italia = paises("Italy")
        posesiones = U_(paises("Netherlands", "Belgium", "Luxembourg"), P("franco_comte", tierra), P("milan", tierra), P("napoles", italia),
                        P("sicilia", italia), P("cerdena", italia))
        M["posesiones"] = posesiones
        M["am_1600"] = U_(M["am_1550"], mex, P("chile_1550", chile), P("argentina_1600", arg_uru), filip, posesiones)
        M["am_1810"] = U_(M["am_1550"], mex, chile, arg_uru, filip, P("nueva_espana_norte", usa))
        M["am_1825"] = U_(pen, paises("Cuba", "Puerto Rico"), filip)
        M["am_1898"] = pen.copy()
        M["usa"] = usa
        M["usa_1898"] = U_(usa, paises("Puerto Rico"), filip)
        M["hispanohablantes"] = U_(espana, mex, centro, paises("Cuba", "Dominican Rep.", "Puerto Rico"), sur_1550, chile, arg_uru, paises("Eq. Guinea"))
        M["filipinas"] = filip
        M["peninsula_am"] = pen
    campos = {k: _i16(_sdf(v)) for k, v in M.items()}
    # celdas por fronteras reales (índice del país más cercano y distancia a la frontera con el vecino)
    cel = {}
    for nombre, lista in CELDAS_PAISES.items():
        if rej.nombre != "am":
            continue
        ds = np.stack([_sdf(_mask_geoms(rej, _paises((n,)))) for n in lista], 0)
        idx = np.argmin(ds, 0).astype(np.uint8)
        dd = np.sort(ds, 0)
        borde = np.clip((dd[1] - dd[0]) * 0.5, 0, 3000).astype(np.float32)
        cel[nombre] = (idx, borde)
    # relieve, altitud y profundidad (solo "eu")
    aux = _relieve(rej, tierra) if rej.nombre == "eu" else None
    rios = _rios_eu(rej) if rej.nombre == "eu" else _rios_ne(rej)
    return campos, cel, aux, rios


def _relieve(rej, tierra):
    """(FH, FW, 3): luz del sombreado (-1..1), altitud 0..1 (tierra) y profundidad 0..1 (mar), del relieve ETOPO1 de nucleo/datos."""
    d = np.load(F_REL)
    alt = d["alt"].astype(np.float32)
    lat0, lon0, paso = float(d["lat0"]), float(d["lon0"]), float(d["paso"])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float32)
    lon, lat = rej.inv(xs, ys)
    mi = ((lat - lat0) / paso).astype(np.float32)
    mj = ((lon - lon0) / paso).astype(np.float32)
    e = cv2.remap(alt, mj, mi, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=-99999.0)
    h, w = alt.shape
    dentro = np.minimum(np.minimum(mi, h - 1 - mi), np.minimum(mj, w - 1 - mj)) / 60.0     # grados hasta el borde de la ventana de datos
    wv = np.clip(dentro / 0.8, 0, 1).astype(np.float32)
    wv = wv * wv * (3 - 2 * wv)
    wv[e < -90000] = 0.0
    e[e < -90000] = 0.0
    es = cv2.GaussianBlur(e, (0, 0), 1.2)
    gx = cv2.Sobel(es, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(es, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    px_m = 111320.0 / (rej.pxdeg * (1.0 / np.cos(np.radians(lat))))           # metros por px de la rejilla (Mercator)
    k = 8.0 / px_m
    luz = np.clip(k * (gx * 0.70 + gy * 0.70), -1.0, 1.0) * wv              # ladera hacia el noroeste (iluminada) > 0
    luz = np.where(tierra > 127, luz, 0.0).astype(np.float32)
    alt01 = np.clip(e / 2200.0, 0, 1) * wv
    prof = np.clip(-e / 1400.0, 0, 1)
    prof = (prof * wv + 1.0 * (1 - wv)).astype(np.float32)
    return np.stack([luz, alt01.astype(np.float32), prof], -1).astype(np.float32)


def _rios_eu(rej):
    d = np.load(F_REL)
    rp = d["rios_pts"]
    cortes = d["rios_cortes"].astype(np.int64)
    ln = np.log1p(rp[:, 2])
    out = []
    for a, b in zip(cortes[:-1], cortes[1:]):
        l = ln[a:b]
        if l[-1] < 6.0:
            continue
        ini = int(np.argmax(l >= 6.0))
        P = rp[a + ini:b, :2].astype(np.float64)
        if len(P) < 3:
            continue
        out.append((_suavizar_linea(P, 2.0), float(l[-1])))
    return out


def _suavizar_linea(P, sig):
    """Suaviza una polilínea (los ríos del relieve van en escalera de 1')."""
    if len(P) < 5:
        return P
    k = int(3 * sig)
    ex = np.vstack([np.repeat(P[:1], k, 0), P, np.repeat(P[-1:], k, 0)])
    w = np.exp(-0.5 * (np.arange(-k, k + 1) / sig) ** 2)
    w /= w.sum()
    Q = np.stack([np.convolve(ex[:, 0], w, "valid"), np.convolve(ex[:, 1], w, "valid")], 1)
    Q[0], Q[-1] = P[0], P[-1]
    return Q


def _rios_ne(rej):
    d = json.load(open(F_RIOS, encoding="utf-8"))
    out = []
    for f in d["features"]:
        if f["properties"].get("scalerank", 9) > 5:
            continue
        g = f["geometry"]
        lineas = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for c in lineas:
            P = np.asarray(c, float)
            if len(P) < 2:
                continue
            x, _ = rej.proj(P[:, 0], P[:, 1])
            if x.max() < 0 or x.min() > rej.FW:
                continue
            out.append((P, 8.6 - 0.5 * f["properties"].get("scalerank", 5)))
    return out


def preparar(nombres=("eu", "am")):
    os.makedirs(DATOS, exist_ok=True)
    for n in nombres:
        rej = REJ[n]
        campos, cel, aux, rios = _construir(rej)
        datos = {f"c_{k}": v for k, v in campos.items()}
        for k, (idx, borde) in cel.items():
            datos[f"i_{k}"] = idx
            datos[f"b_{k}"] = borde.astype(np.float16)
        if aux is not None:
            datos["aux"] = aux.astype(np.float16)
        datos["rios_pts"] = np.concatenate([r[0] for r in rios]).astype(np.float32)
        datos["rios_cortes"] = np.cumsum([0] + [len(r[0]) for r in rios]).astype(np.int64)
        datos["rios_peso"] = np.array([r[1] for r in rios], np.float32)
        np.savez_compressed(os.path.join(DATOS, f"campos_{n}.npz"), **datos)
        print(n, rej.FW, "x", rej.FH, "campos:", len(campos), "ríos:", len(rios), flush=True)


def _cortar_costura(rej, pts, cortes, peso):
    """Un río que cruza la costura de longitud de una rejilla envuelta (60° E en "am") se proyecta con un salto de 360°: una raya recta
    de lado a lado del mundo (se veía sobre España, a 42,2° N). Se parte en dos justo en la costura."""
    nat = rej.nat(pts[:, 0])
    salto = np.nonzero(np.abs(np.diff(nat)) > 180.0)[0] + 1
    salto = np.setdiff1d(salto, cortes)
    if not len(salto):
        return pts, cortes, peso
    nuevos = np.union1d(cortes, salto)
    dueno = np.searchsorted(cortes, nuevos[:-1], side="right") - 1
    return pts, nuevos.astype(cortes.dtype), peso[dueno]


def _cargar_rej(rej):
    if rej.campos:
        return
    d = np.load(os.path.join(DATOS, f"campos_{rej.nombre}.npz"))
    for k in d.files:
        if k.startswith("c_"):
            rej.campos[k[2:]] = d[k]
        elif k.startswith("i_"):
            n = k[2:]
            rej._cel[n] = (d[k], d["b_" + n].astype(np.float32))
    rej.aux = d["aux"].astype(np.float32) if "aux" in d.files else None
    pts, cortes, peso = d["rios_pts"].astype(np.float64), d["rios_cortes"], d["rios_peso"]
    if rej.envuelve:
        pts, cortes, peso = _cortar_costura(rej, pts, cortes, peso)
    rej.rios = [(pts[a:b], float(p)) for a, b, p in zip(cortes[:-1], cortes[1:], peso)]
    rej.r_pts = pts
    rej.r_cortes = cortes
    rej.r_peso = peso


# ------------------------------------------------------------------ rejilla activa (compatibilidad con core.py / reg.py)
ACT = None
CAMPOS = {}
CELDAS = {}
LON0 = LON1 = LAT0 = LAT1 = 0.0
FW = FH = 0
PXLAT = 1.0
KX = 1.0


def usar(nombre):
    global ACT, CAMPOS, CELDAS, LON0, LON1, LAT0, LAT1, FW, FH
    rej = REJ[nombre]
    _cargar_rej(rej)
    ACT = rej
    CAMPOS = rej.campos
    CELDAS = {**{k: v for k, v in CELDAS_SEMILLAS.items()}, **{k: v for k, v in CELDAS_PAISES.items()}}
    LON0, LON1, LAT0, LAT1, FW, FH = rej.lon0, rej.lon1, rej.lat0, rej.lat1, rej.FW, rej.FH


def cargar():
    for n in REJ:
        _cargar_rej(REJ[n])
    if ACT is None:
        usar("eu")


def proj(lon, lat):
    return ACT.proj(lon, lat)


def proj_pts(P):
    return ACT.proj_pts(P)


def celdas(nombre):
    """(índice de celda, distancia a la frontera entre celdas) en la rejilla activa. Semillas -> Voronoi; países -> fronteras reales."""
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
    """Cámara: centro (lon, lat), zoom z (px de pantalla por px de la rejilla "eu"), giro (rad). Usa la rejilla activa al fijarse."""

    def __init__(self, lon=-3.7, lat=40.0, z=3.0, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.rej = ACT if ACT is not None else REJ["eu"]
        self.lon, self.lat, self.z, self.rot = lon, lat, z, rot
        self.zn = z * PXDEG_REF / self.rej.pxdeg                 # zoom nativo de la rejilla
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
        """Campo de la rejilla -> pantalla, en px de pantalla (int16 -> float32)."""
        if campo.dtype == np.int16:
            r = cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=int(min(relleno * ESC_I16, 32000)))
            return r.astype(np.float32) * np.float32(self.zn / ESC_I16)
        r = cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)
        return r * np.float32(self.zn)

    def proyectar_crudo(self, img, relleno=0.0, interp=cv2.INTER_LINEAR):
        return cv2.warpAffine(img, self.M, (W, H), flags=interp, borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)

    @property
    def escala(self):
        return self.z

    def limites(self):
        """(lon_min, lon_max, lat_min, lat_max) aproximados de lo que se ve (lon nativa de la rejilla)."""
        hw = W / 2 / (self.zn * self.rej.pxdeg)
        cx = float(self.rej.nat(self.lon))
        y = float(ymerc(self.lat))
        hh = H / 2 / (self.zn * self.rej.pxdeg)
        return cx - hw, cx + hw, float(inv_ymerc(y - hh)), float(inv_ymerc(y + hh))


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
    """Guache plano: S en px de pantalla (negativo dentro). Borde suave de ~1,3 px, media luna de sombra de ~70 px."""
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
    """Mar (con profundidad y orilla clara) y tierra (color por altitud, sombreado del relieve, media luna de sombra en la costa)."""
    h, w = S.shape
    for y in prange(y0, y1):
        for x in range(x0, x1):
            s = S[y, x] + amp * nz[y, x]
            luz = aux[y, x, 0]
            alt = aux[y, x, 1]
            pr = aux[y, x, 2]
            pc = 1.0 + 1.3 * pincel[y, x]
            # mar
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
            lum *= (1.0 + 0.36 * luz) * (1.0 + 1.2 * pincel[y, x])
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
    """Pinta la forma S (pantalla, px, negativo dentro) con `color` (0-255) a guache sobre `img` (float32 0-1); `luz` = relieve proyectado."""
    r = _roi(S)
    if r is None:
        return
    _pintar_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, _c(color), np.float32(alfa), np.float32(sombra), np.float32(borde),
               np.float32(4.0 * ruido), _CERO if luz is None else luz, np.float32(kluz if luz is not None else 0.0), r[0], r[1], r[2], r[3])


class Base:
    """Lo que la cámara ve de la rejilla en este cuadro: tierra (S), relieve proyectado (aux)."""
    pass


def pintar_base(cam, fase=0):
    """Fondo: papel, mar con profundidad, tierra con relieve. Devuelve (img, base) con base.S (tierra) y base.luz (sombreado)."""
    rej = cam.rej
    img = np.empty((H, W, 3), np.float32)
    S = cam.proyectar(rej.campos["tierra"])
    if rej.aux is not None:
        aux = cam.proyectar_crudo(rej.aux, 0.0)
    else:
        aux = np.zeros((H, W, 3), np.float32)
        aux[..., 2] = 0.55
    _tierra_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, aux, _c(TIERRA), _c(TIERRA_ALTA), _c(TIERRA_CUMBRE), _c(MAR_CL), _c(MAR_HONDO), _c((214, 234, 230)),
               np.float32(3.0), 0, H, 0, W)
    b = Base()
    b.S, b.luz = S, aux[..., 0].copy()
    return img, b


def pintar_rios(img, cam, base, t=0.0, alfa=0.9, minimo=None):
    """Ríos (pincelada azul fina) sobre tierra y territorios; grosor según caudal y zoom."""
    rej = cam.rej
    if not rej.rios:
        return
    if minimo is None:
        minimo = float(np.interp(math.log(max(cam.z, 0.05)), [math.log(0.6), math.log(2.3), math.log(6.0)], [10.6, 9.3, 7.6])) if rej.nombre == "eu" else \
            float(np.interp(math.log(max(cam.z, 0.05)), [math.log(0.3), math.log(1.5)], [6.8, 5.6]))
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
        capas[0 if f < 0.7 else (1 if f < 1.4 else 2)].append(seg)
    m = np.zeros((H, W), np.uint8)
    esc = max(0.7, min(2.2, cam.z / 2.6)) ** 0.6
    for g, L in enumerate(capas):
        if L:
            cv2.polylines(m, L, False, 255, max(1, int(round((2.0 + 1.6 * g) * esc))), cv2.LINE_AA, 4)
    tierra = (base.S < -1.0).astype(np.uint8) * 255
    m = cv2.multiply(m, tierra, scale=1 / 255.0)
    ys, xs = np.nonzero(m)
    if len(ys):
        a = (m[ys, xs].astype(np.float32) / 255.0)[:, None] * alfa
        col = _c(RIO) * (1 + 1.2 * PINCEL[ys, xs])[:, None] * GRANO[ys, xs]
        img[ys, xs] = img[ys, xs] * (1 - a) + col * a


def rotulo_mapa(img, txt, cam, lon, lat, px=40, alfa=0.42, color=(70, 96, 120), espaciado=True, rot=0.0):
    """Nombre de mar u océano pintado en el propio mapa (debajo de todo, se mueve con la cámara)."""
    x, y = cam.pant(lon, lat)
    t = " ".join(txt) if espaciado else txt
    zref = 2.3 if cam.rej.nombre == "eu" else 0.9
    px = int(max(18, min(90, px * (cam.zn / zref) ** 0.45)))
    m = B.mascara_texto(t, px)
    if rot:
        h_, w_ = m.shape
        Mr = cv2.getRotationMatrix2D((w_ / 2, h_ / 2), math.degrees(rot), 1.0)
        m = cv2.warpAffine(m, Mr, (w_, h_))
    h_, w_ = m.shape
    x0, y0 = int(x - w_ / 2), int(y - h_ / 2)
    fuera = max(0.0, 30 - x0, x0 + w_ - (W - 30), 125 - y0, y0 + h_ - (H - 30))         # arriba queda libre para el contador y los sellos
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
    import sys
    preparar(tuple(sys.argv[1:]) or ("eu", "am"))
