# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Egipto en 5 minutos» (v2, 11-oct-2026), con RELIEVE REAL.

Copia del kit v2 de `historia_espana` adaptada a una sola rejilla en proyección de MERCATOR:
  - "eg": del Egeo y Cirenaica a Mesopotamia y del mar Negro a Etiopía (lon 18..50, lat 42..8), 60 px por grado.
    Bajo el guache: relieve y batimetría NOAA ETOPO1 (1', datos/relieve_eg_etopo1.nc, descargado de coastwatch.pfeg.noaa.gov/erddap,
    dataset etopo180), el VALLE VERDE del Nilo (franja fértil + Delta + El Fayum) y ríos reales de Natural Earth (el Nilo con sus brazos de
    Rosetta y Damieta, Nilo Azul y Blanco, Atbara, Éufrates, Tigris, Jordán). Los lagos son agua; el lago Nasser es una capa que se llena en 1970.
Los campos se calculan una vez (`python mapa.py`) y se guardan en datos/campos_eg.npz (int16, 1/8 de px).
Unidades: los campos se proyectan a pantalla en PÍXELES DE PANTALLA (S * zoom nativo), así los bordes y sombras miden lo mismo a cualquier zoom.
Fuentes: Natural Earth 50 m (tierra, países, ríos, lagos; dominio público), NOAA ETOPO1 (dominio público).
Los territorios históricos son aproximados (atlas de Baines y Málek, Cambridge Ancient History, mapas de la Encyclopaedia Britannica).
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
F_NC = os.path.join(AQUI, "datos", "relieve_eg_etopo1.nc")
DATOS = os.path.join(AQUI, "datos")
ESC_I16 = 8.0                        # los campos se guardan en int16 con 1/8 px de resolución


# ------------------------------------------------------------------ proyección de Mercator
def ymerc(lat):
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.asarray(lat, float)) / 2)))


def inv_ymerc(y):
    return np.degrees(2 * np.arctan(np.exp(np.radians(np.asarray(y, float)))) - np.pi / 2)


def U(lon):
    """Longitud «desenvuelta» (aquí no hace falta: la rejilla no cruza el antimeridiano)."""
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


REJ = {"eg": Rej("eg", 18.0, 50.0, 42.0, 8.0, 60.0)}
PXDEG_REF = REJ["eg"].pxdeg          # zoom de la cámara = px de pantalla por px de la rejilla (z = 1: 60 px por grado)

# ------------------------------------------------------------------ paleta de guache (desierto cálido, mar turquesa apagado)
MAR = (170, 206, 212)
MAR_HONDO = (128, 172, 196)
MAR_CL = (204, 228, 224)
TIERRA = (238, 222, 184)
TIERRA_ALTA = (206, 178, 136)
TIERRA_CUMBRE = (236, 230, 216)
RIO = (90, 150, 196)
VALLE = (138, 178, 104)
AGUA_LAGO = (150, 196, 214)
COL = {
    "alto": (232, 226, 210), "bajo": (200, 70, 58), "egipto": (226, 170, 62), "reino_antiguo": (226, 170, 62), "caos": (190, 150, 100),
    "reino_medio": (78, 150, 130), "tebas": (70, 140, 150), "hicsos": (150, 92, 150), "reino_nuevo": (204, 74, 58), "hititas": (110, 120, 170),
    "aton": (240, 196, 72), "ramses": (196, 68, 56), "kush": (120, 86, 66), "asiria": (130, 112, 96), "persia": (110, 96, 170),
    "macedonia": (232, 170, 70), "alejandro": (226, 150, 60), "ptolemaico": (70, 120, 186), "roma": (186, 52, 46), "bizancio": (140, 90, 150),
    "califato": (70, 140, 96), "fatimi": (96, 160, 110), "ayubi": (214, 160, 60), "cruzados": (232, 232, 222), "mameluco": (200, 120, 60),
    "mongoles": (110, 104, 92), "otomano": (180, 56, 66), "francia": (74, 108, 180), "mehmet": (206, 96, 64), "britanico": (190, 72, 80),
    "egipto_mod": (204, 64, 56), "sudan": (196, 170, 120),
}
COL_CELDAS = [(214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
              (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110)]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat)
CIUDADES = {
    # Egipto
    "alejandria": (29.92, 31.20), "rosetta": (30.42, 31.40), "damieta": (31.81, 31.42), "port_said": (32.30, 31.26), "pelusio": (32.57, 31.04),
    "menfis": (31.25, 29.85), "guiza": (31.13, 29.98), "saqqara": (31.22, 29.87), "cairo": (31.24, 30.04), "heliopolis": (31.31, 30.13),
    "avaris": (31.82, 30.79), "tanis": (31.88, 30.98), "sais": (30.77, 30.97), "bubastis": (31.51, 30.57), "fayum": (30.84, 29.31),
    "heracleopolis": (30.94, 29.08), "hermopolis": (30.80, 27.78), "amarna": (30.90, 27.65), "abidos": (31.92, 26.18), "tebas": (32.64, 25.70),
    "karnak": (32.66, 25.72), "valle_reyes": (32.60, 25.74), "deir_bahari": (32.61, 25.74), "nejen": (32.78, 25.10), "edfu": (32.87, 24.98),
    "asuan": (32.89, 24.09), "file": (32.88, 24.02), "presa": (32.88, 23.97), "abu_simbel": (31.63, 22.34), "buhen": (31.33, 21.92),
    "kerma": (30.40, 19.60), "napata": (31.83, 18.54), "meroe": (33.75, 16.94), "jartum": (32.53, 15.59), "siwa": (25.52, 29.20),
    "suez": (32.55, 29.97), "ismailia": (32.27, 30.60), "abukir": (30.07, 31.32), "sinai": (33.97, 28.54), "mersa_gawasis": (34.25, 26.55),
    "el_alamein": (28.95, 30.83), "fustat": (31.23, 30.01), "ciudadela": (31.26, 30.03),
    # Levante, Anatolia, Mesopotamia, Arabia, Grecia
    "kadesh": (36.51, 34.56), "megido": (35.18, 32.58), "jerusalen": (35.23, 31.78), "biblos": (35.65, 34.12), "ugarit": (35.78, 35.60),
    "carquemis": (38.01, 36.83), "alepo": (37.16, 36.20), "damasco": (36.29, 33.51), "tiro": (35.20, 33.27), "gaza": (34.45, 31.50),
    "hattusa": (34.62, 40.02), "ninive": (43.15, 36.36), "asur": (43.26, 35.46), "babilonia": (44.42, 32.54), "susa": (48.25, 32.19),
    "bagdad": (44.36, 33.31), "ain_yalut": (35.36, 32.55), "acre": (35.08, 32.93), "meca": (39.83, 21.42), "medina": (39.61, 24.47),
    "estambul": (28.98, 41.01), "pela": (22.52, 40.76), "atenas": (23.73, 37.98), "accio": (20.73, 38.95), "rodas": (28.22, 36.43),
    "chipre": (33.2, 35.1), "creta": (24.9, 35.2), "cirene": (21.86, 32.82), "punt": (39.4, 15.4), "adulis": (39.65, 15.27),
    "trebisonda": (39.72, 41.0), "antioquia": (36.16, 36.20), "tripoli_l": (35.84, 34.44),
}
RUTAS = {
    "nilo_arriba": [(31.2, 30.1), (31.3, 29.2), (30.85, 28.1), (31.3, 27.1), (31.9, 26.3), (32.6, 25.7), (32.9, 24.1)],
    "punt": [(32.66, 25.72), (33.4, 26.1), (34.25, 26.55), (35.2, 25.4), (36.3, 23.5), (37.6, 20.6), (38.8, 17.6), (39.6, 15.6)],
    "punt_vuelta": [(39.6, 15.6), (38.6, 18.2), (37.2, 21.5), (35.9, 24.2), (34.8, 26.0), (34.25, 26.55)],
    "tutmosis": [(31.88, 30.98), (32.57, 31.04), (34.45, 31.50), (35.18, 32.58), (35.6, 33.6), (36.3, 34.6), (37.16, 36.20), (38.01, 36.83)],
    "kadesh_eg": [(31.88, 30.98), (32.57, 31.04), (34.45, 31.50), (35.18, 32.58), (35.75, 33.7), (36.4, 34.45)],
    "kadesh_hit": [(34.62, 40.02), (35.6, 38.4), (36.4, 37.0), (37.16, 36.20), (36.8, 35.3), (36.55, 34.7)],
    "hicsos": [(36.29, 33.51), (35.18, 32.58), (34.45, 31.50), (32.57, 31.04), (31.82, 30.79)],
    "hicsos_fuera": [(31.82, 30.79), (32.57, 31.04), (34.45, 31.50), (35.18, 32.58)],
    "pueblos_mar": [(26.0, 37.5), (28.5, 35.8), (31.0, 33.5), (31.5, 31.8), (31.4, 31.3)],
    "nubios": [(31.83, 18.54), (31.4, 20.5), (31.3, 22.2), (32.0, 23.4), (32.9, 24.1), (32.6, 25.7)],
    "asirios": [(43.15, 36.36), (40.0, 36.0), (37.16, 36.20), (35.18, 32.58), (34.45, 31.50), (32.57, 31.04), (31.25, 29.85)],
    "persas": [(48.25, 32.19), (44.42, 32.54), (40.5, 34.5), (37.16, 36.20), (35.9, 34.6), (35.18, 32.58), (34.45, 31.50), (32.57, 31.04), (31.25, 29.85)],
    "alejandro": [(22.52, 40.76), (26.0, 40.2), (29.5, 39.0), (33.0, 37.5), (36.16, 36.20), (35.5, 34.0), (35.20, 33.27), (34.45, 31.50),
                  (32.57, 31.04), (31.25, 29.85)],
    "siwa": [(29.92, 31.20), (28.0, 31.1), (27.2, 30.6), (25.52, 29.20)],
    "cesar": [(18.0, 37.6), (22.0, 35.8), (26.0, 33.6), (29.92, 31.20)],
    "antonio": [(26.5, 36.6), (31.0, 34.6), (35.9, 34.1)],
    "accio_eg": [(29.92, 31.20), (25.0, 33.8), (21.8, 37.0), (20.9, 38.8)],
    "octavio": [(18.0, 39.4), (19.6, 39.2), (20.5, 38.95)],
    "arabes": [(39.61, 24.47), (38.4, 26.6), (36.2, 29.6), (35.0, 30.5), (34.45, 31.50), (32.57, 31.04), (31.23, 30.01)],
    "cruzados": [(18.0, 38.0), (24.0, 36.6), (30.0, 34.8), (35.08, 32.93)],
    "mongoles": [(48.0, 36.5), (44.36, 33.31), (40.5, 35.4), (37.16, 36.20), (36.29, 33.51), (35.36, 32.55)],
    "napoleon": [(18.0, 36.6), (22.0, 34.6), (26.0, 32.6), (29.92, 31.20), (30.6, 30.6), (31.13, 30.05)],
    "rosetta_paris": [(30.42, 31.40), (25.0, 34.0), (18.0, 37.6)],
    "suez": [(32.30, 31.26), (32.32, 31.0), (32.27, 30.60), (32.35, 30.35), (32.45, 30.15), (32.55, 29.97)],
    "ruta_india": [(18.0, 36.0), (26.0, 33.6), (32.30, 31.40), (32.55, 29.97), (33.6, 27.9), (35.4, 25.8), (37.6, 21.8), (40.0, 17.4),
                   (42.6, 13.3), (43.5, 12.4), (46.0, 11.9), (50.0, 12.6)],
    "ruta_africa": [(18.0, 36.0), (18.0, 30.0), (18.0, 20.0), (18.0, 8.0)],
}
# semillas de fracturas (lon, lat)
CELDAS_SEMILLAS = {
    "diadocos": [(30.5, 27.5), (43.0, 33.5), (33.0, 38.6), (22.6, 40.2)],
    "nomos": [(31.88, 30.98), (30.77, 30.97), (31.51, 30.57), (30.3, 31.1), (31.25, 29.85), (30.94, 29.08), (30.80, 27.78), (31.2, 27.1),
              (31.92, 26.18), (32.64, 25.70), (32.87, 24.98), (32.89, 24.09)],
    "tercer": [(31.88, 30.98), (30.77, 30.97), (31.51, 30.57), (31.25, 29.85), (30.94, 29.08), (30.80, 27.78), (31.92, 26.18),
               (32.64, 25.70), (32.89, 24.09)],
}
CELDAS_PAISES = {}

# ------------------------------------------------------------------ polígonos (lon, lat): se recortan con la tierra
DELTA = [(31.30, 29.95), (30.85, 30.25), (30.25, 30.65), (29.70, 30.95), (29.40, 31.30), (29.50, 31.70), (32.80, 31.70), (32.62, 31.10),
         (32.20, 30.60), (31.70, 30.25)]
FAYUM = [(30.35, 29.25), (30.55, 29.55), (30.95, 29.55), (31.15, 29.30), (30.95, 29.05), (30.55, 29.05)]
SINAI = [(32.35, 31.70), (34.30, 31.70), (34.95, 29.50), (34.40, 27.70), (33.80, 27.50), (32.90, 29.10), (32.35, 30.05)]
LEV_N = [(33.6, 31.0), (33.9, 31.9), (34.4, 32.9), (34.9, 34.0), (35.4, 35.2), (35.5, 36.0), (35.9, 36.7), (36.6, 37.1), (37.6, 37.2), (38.4, 37.1),
         (38.7, 36.4), (38.2, 35.6), (37.4, 34.8), (36.9, 33.8), (36.7, 32.8), (36.4, 31.8), (35.9, 30.7), (35.2, 29.7), (34.95, 29.45), (34.6, 29.6),
         (34.2, 30.4), (33.9, 30.9)]
LEV_S = [(33.6, 31.0), (33.9, 31.9), (34.4, 32.9), (34.9, 34.0), (35.3, 34.65), (35.9, 34.62), (36.5, 34.3), (36.8, 33.6), (36.6, 32.6),
         (36.3, 31.7), (35.8, 30.6), (35.2, 29.7), (34.95, 29.45), (34.6, 29.6), (34.2, 30.4), (33.9, 30.9)]
HICSOS_AS = [(32.3, 31.4), (34.2, 31.7), (34.9, 32.8), (35.6, 33.0), (35.7, 32.0), (35.3, 31.0), (34.4, 30.5), (32.6, 30.6)]
HITITAS = [(28.5, 40.9), (31.5, 41.3), (35.0, 41.9), (38.5, 41.0), (40.5, 40.0), (40.5, 38.5), (39.2, 37.5), (38.7, 36.6), (38.4, 35.9), (37.6, 35.1),
           (36.7, 34.62), (35.95, 34.66), (35.4, 34.9), (35.4, 35.4), (35.6, 36.1), (34.6, 36.4), (33.0, 36.0), (31.0, 36.6), (29.3, 36.4), (28.0, 37.0),
           (27.0, 38.0), (26.5, 39.4), (26.8, 40.4)]
KUSH_SUR = [(32.3, 15.0), (36.2, 15.4), (35.8, 18.0), (34.0, 18.8), (32.3, 17.2)]
ASIRIA = [(35.5, 37.4), (38.0, 38.2), (41.5, 38.2), (44.5, 37.6), (46.2, 36.5), (46.8, 35.0), (47.8, 32.5), (48.2, 30.6), (47.6, 29.9), (46.5, 30.6),
          (44.8, 31.0), (43.0, 32.4), (40.5, 33.6), (38.4, 33.6), (37.2, 32.2), (36.2, 30.6), (35.2, 29.6), (34.95, 29.45), (34.4, 29.8), (33.9, 30.9),
          (33.6, 31.0), (33.9, 31.9), (34.4, 32.9), (34.9, 34.0), (35.4, 35.2), (35.5, 36.0), (35.9, 36.7)]
PERSIA = [(26.2, 39.6), (26.6, 40.4), (29.0, 41.0), (29.2, 42.2), (50.2, 42.2), (50.2, 30.0), (48.6, 29.9), (47.8, 29.3), (46.5, 29.1), (44.5, 29.4),
          (42.5, 30.5), (40.0, 31.6), (38.0, 31.0), (37.0, 30.0), (36.0, 29.2), (34.95, 29.35), (34.4, 28.0), (33.8, 27.7), (33.1, 28.9), (32.6, 29.9),
          (32.35, 30.05), (32.35, 31.4), (30.0, 32.5), (28.0, 35.5), (26.0, 36.5), (25.6, 38.4)]
MACEDONIA = [(20.4, 41.9), (24.5, 42.0), (24.8, 40.9), (23.8, 40.2), (22.6, 39.9), (21.3, 40.0), (20.6, 40.5)]
TRACIA = [(24.5, 42.2), (29.2, 42.2), (29.0, 41.0), (26.6, 40.4), (26.2, 40.6), (24.8, 40.9)]
CIRENAICA = [(19.6, 29.6), (25.1, 29.6), (25.1, 33.4), (19.6, 33.4)]
ROMA_OR = [(18.0, 42.2), (41.5, 42.2), (41.5, 40.6), (39.8, 39.6), (38.8, 38.2), (38.3, 37.0), (38.4, 36.3), (39.2, 35.6), (38.6, 34.6), (37.6, 33.4),
           (37.0, 32.0), (36.6, 30.8), (36.0, 29.6), (35.3, 28.0), (34.6, 27.8), (34.2, 26.8), (35.4, 25.0), (36.0, 23.2), (24.9, 23.2), (24.9, 29.5),
           (18.0, 29.5)]
CALIFATO_N = [(50.2, 41.5), (45.0, 41.0), (42.0, 39.5), (39.5, 38.5), (37.5, 37.6), (36.2, 37.0), (35.6, 36.8), (34.5, 36.6), (33.6, 31.0),
              (32.35, 31.6), (32.35, 30.05), (32.6, 29.9), (33.1, 28.9), (33.8, 27.7), (35.0, 26.5), (36.3, 24.5), (37.3, 23.0), (38.6, 20.0),
              (40.4, 17.0), (42.0, 14.0), (43.4, 12.6), (44.5, 11.5), (50.2, 11.5)]
HEJAZ = [(34.9, 29.4), (36.4, 29.5), (38.4, 26.5), (40.6, 23.5), (41.6, 20.5), (42.0, 18.4), (40.0, 18.0), (37.0, 23.0), (35.0, 26.5), (34.6, 28.0)]
SIRIA = [(33.6, 31.0), (33.9, 31.9), (34.4, 32.9), (34.9, 34.0), (35.4, 35.2), (35.5, 36.0), (35.9, 36.7), (36.6, 37.1), (38.0, 37.6), (40.0, 37.4),
         (42.0, 37.1), (42.2, 36.0), (40.8, 35.0), (39.2, 34.6), (38.0, 33.4), (37.4, 32.0), (36.5, 30.5), (35.6, 29.6), (34.95, 29.45), (34.6, 29.6),
         (34.2, 30.4), (33.9, 30.9)]
FATIMI_LEV = [(33.6, 31.0), (33.9, 31.9), (34.4, 32.9), (34.9, 34.0), (35.5, 34.7), (36.6, 34.6), (37.2, 33.6), (36.9, 32.4), (36.4, 31.0),
              (35.6, 29.6), (34.95, 29.45), (34.6, 29.6), (34.2, 30.4), (33.9, 30.9)]
CRUZADOS = [(34.55, 32.0), (35.25, 32.0), (35.55, 32.85), (35.75, 33.40), (36.15, 34.0), (36.35, 34.90), (36.3, 35.40), (36.7, 35.90),
            (37.0, 36.30), (36.8, 36.85), (35.90, 36.70), (35.70, 35.80), (35.50, 34.50), (35.00, 33.30), (34.60, 32.40)]
MONGOLES = [(31.0, 41.2), (36.0, 41.9), (42.0, 41.5), (50.2, 42.2), (50.2, 29.8), (48.0, 29.9), (47.0, 29.5), (45.5, 30.7), (43.5, 32.3), (42.0, 34.2),
            (40.6, 35.2), (39.0, 36.4), (38.2, 37.2), (36.6, 37.3), (35.6, 36.9), (34.5, 36.6), (32.5, 36.2), (30.8, 36.6), (30.6, 39.0)]
OTOMANO = [(18.6, 42.2), (42.0, 42.2), (43.6, 40.8), (44.2, 39.5), (44.6, 37.4), (45.6, 35.6), (46.4, 33.4), (47.6, 31.4), (48.6, 29.9),
           (47.2, 29.2), (45.0, 29.4), (42.0, 30.6), (39.0, 31.4), (37.2, 29.8), (36.2, 29.0), (34.95, 29.35), (34.6, 28.0), (33.8, 27.7),
           (33.1, 28.9), (32.6, 29.9), (32.35, 30.05), (32.35, 31.4), (25.1, 31.4), (25.1, 29.6), (18.6, 29.6)]
MAMELUCO_N = [(33.6, 31.0), (33.9, 31.9), (34.4, 32.9), (34.9, 34.0), (35.4, 35.2), (35.5, 36.0), (35.9, 36.7), (36.6, 37.3), (37.8, 37.4),
              (38.6, 36.9), (39.4, 36.0), (39.4, 35.0), (38.4, 33.6), (37.4, 32.0), (36.5, 30.5), (35.6, 29.6), (34.95, 29.45), (34.6, 29.6),
              (34.2, 30.4), (33.9, 30.9)]
NILO_CORTE = 31.30           # latitud del vértice del Delta (al norte, el Delta lo pone el polígono)


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


_PAISES = None
_RIOS = None
RIOS_SI = {"Nile": 9.4, "Rosetta Branch": 9.0, "Damietta Branch": 9.0, "El Bahr el Abyad": 9.0, "Bahr el Jebel": 8.6, "El Bahr el Azraq": 8.4,
           "Abay": 8.0, "Atbara": 7.6, "Setit": 7.0, "Euphrates": 8.6, "Al Furat": 8.6, "Firat": 8.6, "Tigris": 8.4, "Dicle": 8.4,
           "Shatt al Arab": 8.0, "Jordan": 7.6}


def _paises(nombres):
    return [f["geometry"] for f in _PAISES["features"] if f["properties"]["NAME"] in nombres]


def _lineas_rio(nombres):
    """Polilíneas (lon, lat) de los ríos de Natural Earth con esos nombres (río + tramo que cruza lagos)."""
    out = []
    for f in _RIOS["features"]:
        if f["properties"].get("name") not in nombres:
            continue
        g = f["geometry"]
        for c in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            if len(c) >= 2:
                out.append(np.asarray(c, float))
    return out


def _corredor(rej, lat_min, lat_max, ancho, brazos=False):
    """Franja de `ancho` grados centrada en el Nilo, entre dos latitudes (máscara de la rejilla)."""
    m = np.zeros((rej.FH, rej.FW), np.uint8)
    nombres = ("Nile", "Rosetta Branch", "Damietta Branch") if brazos else ("Nile",)
    for P in _lineas_rio(nombres):
        Q = rej.proj_pts(P)
        cv2.polylines(m, [np.rint(Q * 4).astype(np.int32).reshape(-1, 1, 2)], False, 255, max(1, int(ancho * rej.pxdeg)), cv2.LINE_8, 2)
    y0 = int((rej.Y0 - ymerc(lat_max)) * rej.pxdeg)
    y1 = int((rej.Y0 - ymerc(lat_min)) * rej.pxdeg)
    caja = np.zeros_like(m)
    caja[max(0, y0):max(0, y1), :] = 255
    return cv2.bitwise_and(m, caja)


def _construir(rej):
    """Calcula todos los campos de la rejilla (lento: se hace una vez y se guarda)."""
    global _PAISES, _RIOS
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    _RIOS = json.load(open(F_RIOS, encoding="utf-8"))
    lagos = json.load(open(F_LAGOS, encoding="utf-8"))
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    perm = [f["geometry"] for f in lagos["features"] if f["properties"].get("name") in
            ("Lake Tana", "Dead Sea", "Sea of Galilee", "Lake Van", "Lake Tuz", "Lake Urmia", "Lake Sevan", "Lake Assal")]
    nasser = [f["geometry"] for f in lagos["features"] if f["properties"].get("name") == "Lake Nasser"]
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

    def lat_entre(m, la0, la1):
        y0 = int((rej.Y0 - ymerc(la1)) * rej.pxdeg)
        y1 = int((rej.Y0 - ymerc(la0)) * rej.pxdeg)
        c = np.zeros_like(m)
        c[max(0, y0):max(0, y1), :] = 255
        return cv2.bitwise_and(m, c)

    def cor(la0, la1, ancho):
        return cv2.bitwise_and(_corredor(rej, la0, la1, ancho), tierra)

    delta = P(DELTA)
    fayum = P(FAYUM, mano=False)
    # el valle verde: franja estrecha a lo largo del Nilo (y de sus brazos), el Delta y El Fayum
    valle = cv2.bitwise_and(U_(_corredor(rej, 14.5, 31.0, 0.19, brazos=True), delta, fayum), tierra)
    valle = cv2.morphologyEx(valle, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    M["valle"] = valle
    M["nasser"] = _mask_geoms(rej, nasser)
    egipto = paises("Egypt")
    sudan = paises("Sudan")
    sinai = P(SINAI, egipto)
    M["egipto_mod"] = egipto
    M["sudan"] = sudan
    M["egipto_sudan"] = U_(egipto, sudan)
    # el Egipto faraónico: franja del valle (± 0,5°) + el Delta + El Fayum
    nucleo = U_(cor(24.0, NILO_CORTE, 1.0), delta, fayum)
    M["alto"] = U_(cor(24.0, 29.62, 1.0), fayum)
    M["bajo"] = menos(U_(delta, cor(29.62, NILO_CORTE, 1.0)), M["alto"])
    M["reino_antiguo"] = nucleo
    M["tebas_sur"] = cor(24.0, 27.4, 1.0)
    M["norte_caos"] = menos(nucleo, M["tebas_sur"])
    M["reino_medio"] = U_(nucleo, cor(21.5, 24.1, 0.9))
    M["hicsos"] = U_(delta, cor(27.4, NILO_CORTE, 1.0), fayum, P(HICSOS_AS), cv2.bitwise_and(sinai, P([(32.3, 31.7), (34.4, 31.7), (34.4, 30.6), (32.3, 30.6)], mano=False)))
    nubia_nr = cor(18.3, 24.1, 1.0)
    M["reino_nuevo"] = U_(nucleo, nubia_nr, sinai, P(LEV_N))
    M["imp_1350"] = U_(nucleo, nubia_nr, sinai, P(LEV_S))
    M["ramses"] = M["imp_1350"]
    M["hititas"] = P(HITITAS)
    M["kush"] = U_(cor(15.2, 22.0, 1.3), P(KUSH_SUR))
    M["kush_egipto"] = U_(M["kush"], nucleo, cor(22.0, 24.1, 1.0))
    M["asiria"] = U_(P(ASIRIA), nucleo, sinai)
    egn = lat_entre(egipto, 22.0, 32.0)
    cire = cv2.bitwise_and(P(CIRENAICA), paises("Libya"))
    M["persia"] = U_(P(PERSIA), egn)
    grecia = U_(lat_entre(paises("Greece"), 35.5, 42.5), P(MACEDONIA))
    M["macedonia"] = P(MACEDONIA)
    M["alejandro"] = U_(M["persia"], grecia, P(TRACIA), cire)
    chipre = paises("Cyprus", "N. Cyprus")
    M["ptolemaico"] = U_(egn, cire, chipre, P(LEV_S))
    M["roma"] = menos(P(ROMA_OR), paises("Italy", "Iran", "Iraq", "Saudi Arabia", "Sudan"))
    M["egipto_romano"] = lat_entre(egipto, 23.2, 32.0)
    M["roma_rep"] = menos(M["roma"], egipto, P([(32.3, 31.8), (35.0, 31.8), (35.0, 27.5), (32.3, 27.5)], mano=False))      # Roma en el 50 a. C. (sin Egipto ni el Sinaí)
    M["califato"] = U_(menos(P(CALIFATO_N), paises("Eritrea", "Ethiopia", "Djibouti", "Somaliland", "Somalia", "Sudan", "Egypt")), egipto, cire)
    M["bizancio"] = menos(M["roma"], M["califato"], egipto, cire, paises("Libya"))         # lo que le queda a Bizancio tras las conquistas árabes
    hejaz = P(HEJAZ)
    M["fatimi"] = U_(egipto, cire, P(FATIMI_LEV), hejaz)
    cruz = P(CRUZADOS)
    M["cruzados"] = cruz
    M["ayubi"] = U_(egipto, hejaz, paises("Yemen"), menos(P(SIRIA), cruz))
    M["mameluco"] = U_(egipto, hejaz, P(MAMELUCO_N), cv2.bitwise_and(cire, P([(23.0, 29.0), (25.2, 29.0), (25.2, 33.5), (23.0, 33.5)], mano=False)))
    M["mongoles"] = menos(P(MONGOLES), M["mameluco"])
    M["otomano"] = U_(menos(P(OTOMANO), paises("Italy", "Iran", "Russia", "Georgia", "Azerbaijan", "Armenia")), egipto, hejaz, paises("Yemen"),
                      cor(20.5, 22.1, 1.0))
    M["francia"] = nucleo.copy()                     # la ocupación francesa (1798-1801): el Delta y el valle
    M["mehmet"] = U_(egipto, lat_entre(sudan, 12.0, 23.0))
    M["britanico"] = egipto.copy()
    M["anglo_sudan"] = U_(egipto, sudan)
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
    px_m = 111320.0 / (rej.pxdeg * (1.0 / np.cos(np.radians(lat))))           # metros por px de la rejilla (Mercator)
    k = 9.0 / px_m
    luz = np.clip(k * (gx * 0.70 + gy * 0.70), -1.0, 1.0)                     # ladera hacia el noroeste (iluminada) > 0
    luz = np.where(tierra > 127, luz, 0.0).astype(np.float32)
    alt01 = np.clip(e / 2200.0, 0, 1)
    prof = np.clip(-e / 1400.0, 0, 1).astype(np.float32)
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
    return out


def preparar(nombres=("eg",)):
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


# ------------------------------------------------------------------ rejilla activa (compatibilidad con core.py / reg.py)
ACT = None
CAMPOS = {}
CELDAS = {}
LON0 = LON1 = LAT0 = LAT1 = 0.0
FW = FH = 0


def usar(nombre="eg"):
    global ACT, CAMPOS, CELDAS, LON0, LON1, LAT0, LAT1, FW, FH
    rej = REJ["eg"]
    _cargar_rej(rej)
    ACT = rej
    CAMPOS = rej.campos
    CELDAS = dict(CELDAS_SEMILLAS)
    LON0, LON1, LAT0, LAT1, FW, FH = rej.lon0, rej.lon1, rej.lat0, rej.lat1, rej.FW, rej.FH


def cargar():
    _cargar_rej(REJ["eg"])
    if ACT is None:
        usar("eg")


def proj(lon, lat):
    return ACT.proj(lon, lat)


def proj_pts(P):
    return ACT.proj_pts(P)


def celdas(nombre):
    """(índice de celda, distancia a la frontera entre celdas) en la rejilla activa. Semillas -> Voronoi."""
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

    def __init__(self, lon=31.0, lat=27.0, z=2.5, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.rej = ACT if ACT is not None else REJ["eg"]
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
        """Campo de la rejilla -> pantalla, en px de pantalla (int16 -> float32)."""
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
    """Fondo: mar con profundidad, tierra con relieve y el valle verde del Nilo. Devuelve (img, base) con base.S (tierra) y base.luz."""
    rej = cam.rej
    img = np.empty((H, W, 3), np.float32)
    S = cam.proyectar(rej.campos["tierra"])
    aux = cam.proyectar_crudo(rej.aux, 0.0)
    _tierra_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, aux, _c(TIERRA), _c(TIERRA_ALTA), _c(TIERRA_CUMBRE), _c(MAR_CL), _c(MAR_HONDO), _c((214, 234, 230)),
               np.float32(3.0), 0, H, 0, W)
    b = Base()
    b.S, b.luz = S, aux[..., 0].copy()
    Sv = cam.proyectar(rej.campos["valle"])
    pintar(img, Sv, VALLE, 0.92, fase, borde=0.4, sombra=0.10, ruido=0.6, luz=b.luz, kluz=0.2)
    return img, b


def pintar_valle(img, cam, base, fase=0, alfa=0.55):
    """El valle verde otra vez, encima de los territorios (translúcido): la franja fértil se ve bajo cualquier reino."""
    Sv = cam.proyectar(cam.rej.campos["valle"])
    pintar(img, Sv, VALLE, alfa, fase, borde=0.3, sombra=0.06, ruido=0.6)


def pintar_rios(img, cam, base, t=0.0, alfa=0.92, minimo=None, nasser=0.0):
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
    """Máscara del texto girada SIN recortar (el lienzo crece hasta la diagonal)."""
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
    """Nombre de mar, desierto o región pintado en el propio mapa (debajo de todo, se mueve con la cámara)."""
    x, y = cam.pant(lon, lat)
    t = " ".join(txt) if espaciado else txt
    px = int(max(18, min(84, px * (cam.zn / 2.6) ** 0.45)))
    m = _mascara_rot(t, px, round(rot, 3))
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
    preparar()
