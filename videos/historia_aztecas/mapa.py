# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «Toda la historia de los AZTECAS» (kit v2.1 de historia_jalisco / historia_aguascalientes), RELIEVE REAL.

DOS rejillas Mercator (misma proyección y mismos lon/lat, así que la cámara es una sola):
  - "mx" (la del kit, la que manda): del Bajío y Michoacán al Soconusco y del Golfo al Pacífico (lon -103.0..-91.8,
    lat 22.0..14.3), 300 px por grado → cabe el imperio entero de 1519 (z ≈ 0,57), el centro de México se ve con z 1,4-2,5 y la
    cuenca de México entera con z ≈ 6. Bajo el guache: AWS Terrain Tiles (Terrarium z9 ≈ 300 m, con batimetría).
  - "cuenca" (solo para el FONDO y los campos de la isla): el Valle de México con sus volcanes (lon -99.45..-98.45, lat 19.95..18.95)
    a 2000 px por grado con Terrarium z12 (≈ 38 m). `pintar_base` la funde encima de "mx" cuando la cámara se acerca (z > 1,7):
    el lago, la isla y los cerros quedan nítidos hasta z ≈ 40-80 (la isla de cerca).
Los lagos de 1519 (Texcoco, Xochimilco, Chalco, Xaltocan, Zumpango) son AGUA en las dos rejillas aunque hoy sean ciudad; la isla
de Tenochtitlan-Tlatelolco es tierra. Fuentes y método: `_mapa_notas.md` y `datos/fuentes/`.
Los campos se calculan una vez (`python mapa.py`, ~1 min) y se guardan en datos/campos_mx.npz (int16, 1/8 de px).

Campos de la rejilla "cuenca" (isla_1519, isla_1325, islote_1325, islote_tlatelolco, agua_isla_1325, lagos_cuenca): tienen OTRO tamaño
que los de "mx"; `Cam.proyectar` los reconoce por su forma. Un `Territorio` solo puede fundir campos de la MISMA rejilla.
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
DATOS = os.path.join(AQUI, "datos")
F_LAND = os.path.join(DATOS, "ne_10m_land.geojson")
F_PAISES = os.path.join(DATOS, "estados_mx.geojson")
F_RIOS = os.path.join(DATOS, "ne_10m_rivers_lake_centerlines.geojson")
F_LAGOS = os.path.join(DATOS, "ne_10m_lakes.geojson")
F_FINO = os.path.join(DATOS, "relieve_azt_terrarium_z9.npz")         # AWS Terrain Tiles, Terrarium z9 (con batimetría)
F_FINO_C = os.path.join(DATOS, "relieve_valle_terrarium_z12.npz")    # Terrarium z12 de la cuenca de México
F_TERR = os.path.join(DATOS, "aztecas_territorios.geojson")          # imperio por etapas, enclaves, purépecha, tepanecas...
F_CUENCA = os.path.join(DATOS, "aztecas_cuenca.geojson")             # lagos 1519, isla de Tenochtitlan-Tlatelolco, islotes
F_LINEAS = os.path.join(DATOS, "aztecas_lineas.json")                # calzadas, albarradón, ríos de la cuenca, rótulos de los lagos
ESC_I16 = 8.0                        # los campos se guardan en int16 con 1/8 px de resolución
ESC_AUX = 8000.0                     # el relieve (luz, altitud, profundidad) se guarda en int16 × 8000


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
        self.aux = None              # (FH, FW, 3) int16 (× ESC_AUX): luz del relieve, altitud 0..1, profundidad 0..1
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


REJ = {"mx": Rej("mx", -103.00, -91.80, 22.00, 14.30, 300.0)}          # llave "mx" para no tocar el kit
REJ_CUENCA = Rej("cuenca", -99.45, -98.45, 19.95, 18.95, 2000.0)          # valle de México con lagos, isla y volcanes
PXDEG_REF = REJ["mx"].pxdeg

# ------------------------------------------------------------------ paleta de guache
MAR = (168, 204, 212)
MAR_HONDO = (124, 168, 194)
MAR_CL = (204, 228, 224)
TIERRA = (236, 220, 184)
TIERRA_ALTA = (202, 174, 132)
TIERRA_CUMBRE = (240, 236, 226)
RIO = (88, 148, 196)
VALLE = (144, 180, 110)
AGUA_LAGO = (150, 198, 214)
CALZADA = (214, 190, 140)
TINTA_MAPA = (70, 60, 52)
# altitud → color: costas y Tierra Caliente claras, altiplano (2 200 m) ocre medio, sierras ocre, volcanes (> 4 000 m) nevados
ALT_E = (0.0, 2200.0, 3600.0, 4300.0, 5000.0)
ALT_V = (0.0, 0.30, 0.62, 0.80, 0.97)
PROF_LAGO = 0.06                     # agua de los lagos: clara y poco honda

COL = {
    # mexicas y Triple Alianza (rojo almagre que se oscurece con los años)
    "imperio": (196, 74, 52),
    "triple_alianza": (196, 74, 52),
    "imperio_1428": (204, 96, 60), "imperio_1440": (200, 86, 56), "imperio_1469": (196, 74, 52),
    "imperio_1481": (190, 68, 50), "imperio_1486": (188, 66, 50), "imperio_1502": (182, 60, 48), "imperio_1519": (176, 56, 46),
    "mexicas": (196, 74, 52),
    "isla": (214, 186, 128), "isla_1325": (214, 186, 128), "isla_1519": (214, 186, 128), "islote_1325": (214, 186, 128),
    "islote_tlatelolco": (200, 170, 118),
    # vecinos y rivales
    "tepanecas": (98, 120, 176),
    "acolhuas": (214, 164, 64),
    "tlaxcala": (92, 150, 98),
    "purepecha": (148, 96, 150),
    "teotitlan": (150, 140, 110),
    "yopitzinco": (150, 140, 110),
    "independientes": (150, 140, 110),
    # conquista y hoy
    "espanoles": (70, 96, 150),
    "nueva_espana": (196, 168, 120),
    "mexico_mod": (78, 148, 96),
    "edo_cdmx": (204, 92, 66),
    "metro": (210, 110, 70),
    # agua y paisaje
    "lagos_1519": AGUA_LAGO, "lagos_cuenca": AGUA_LAGO, "agua_isla_1325": AGUA_LAGO,
    "valle": VALLE,
}
COL_CELDAS = [
    (214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
    (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110),
]

# ------------------------------------------------------------------ lugares (lon, lat) DE FUENTE (ver _mapa_notas.md); * = aproximado
CIUDADES = {
    # isla y cuenca de México
    "tenochtitlan": (-99.13139, 19.43500),            # Templo Mayor (Wikipedia)
    "ciudad_mexico": (-99.13139, 19.43500),           # = Tenochtitlan (el Zócalo está a 150 m)
    "templo_mayor": (-99.13139, 19.43500),
    "tlatelolco": (-99.13750, 19.45108),              # zona arqueológica (Wikipedia «México-Tlatelolco»)
    "chapultepec": (-99.18167, 19.42056),             # cerro (castillo; Wikipedia)
    "azcapotzalco": (-99.18766, 19.48731),
    "tlacopan": (-99.18570, 19.45590),                # Tacuba (Wikipedia)
    "texcoco": (-98.88293, 19.51194),
    "culhuacan": (-99.10783, 19.33954),               # pueblo de Culhuacán (Wikipedia)
    "tizapan": (-99.20220, 19.33707),                 # * Tizapán (San Ángel, OSM); la identificación con el Tizapan mexica es tradicional
    "iztapalapa": (-99.09663, 19.35900),              # barrio de San Lucas, centro del pueblo (OSM)
    "mexicaltzingo": (-99.11982, 19.35707),           # (OSM)
    "xoloc": (-99.15087, 19.36469),                   # * bifurcación de las calzadas de Iztapalapa y Coyoacán (mapa de Sémhur)
    "coyoacan": (-99.16222, 19.35000),
    "xochimilco": (-99.09822, 19.24758),
    "chalco": (-98.89750, 19.26472),
    "tlahuac": (-99.00468, 19.26909),                 # Cuitláhuac, isla (OSM San Pedro Tláhuac)
    "ayotzingo": (-98.92912, 19.20808),               # (OSM)
    "xaltocan": (-99.05026, 19.72003),                # isla (OSM San Miguel Xaltocan)
    "zumpango": (-99.10073, 19.79729),
    "citlaltepec": (-99.14451, 19.81088),             # San Juan Zitlaltepec (OSM)
    "cuautitlan": (-99.16663, 19.70552),
    "tepotzotlan": (-99.22307, 19.71734),
    "los_remedios": (-99.25151, 19.47229),            # Otoncalpulco, santuario de los Remedios (OSM)
    "tepeyac": (-99.11578, 19.48683),                 # cerro (Wikipedia)
    "tenayuca": (-99.16852, 19.53252),
    "atzacoalco": (-99.09515, 19.50044),              # arranque norte del albarradón (OSM)
    "ecatepec": (-99.04916, 19.59907),
    "chimalhuacan": (-98.94170, 19.41840),            # * (centro del municipio, Wikipedia)
    "coatlinchan": (-98.87222, 19.44889),
    "huexotla": (-98.87268, 19.47855),
    "acolman": (-98.91095, 19.63895),
    "teotihuacan": (-98.84389, 19.69250),
    "otumba": (-98.75472, 19.69694),
    "tula": (-99.34114, 20.06347),                    # Tollan-Xicocotitlan (Wikipedia)
    "amecameca": (-98.76963, 19.12560),
    "tlalmanalco": (-98.73232, 19.20661),
    "popocatepetl": (-98.62343, 19.02339),            # cumbre (Wikipedia)
    "iztaccihuatl": (-98.64183, 19.17799),
    "paso_cortes": (-98.64694, 19.08670),
    # centro de México y ruta de Cortés
    "tlaxcala": (-98.23615, 19.31514),                # Tlaxcala de Xicohténcatl (Wikipedia)
    "tizatlan": (-98.24740, 19.31630),                # señorío de Xicohténcatl (OSM)
    "cholula": (-98.30194, 19.05750),                 # Gran Pirámide (Wikipedia)
    "huexotzinco": (-98.40639, 19.16194),             # Huejotzingo (Wikipedia)
    "hueyotlipan": (-98.33014, 19.47959),             # * (centro del municipio, OSM)
    "huamantla": (-97.91457, 19.32333),               # * cerca de Tecoac (OSM)
    "ixtacamaxtitlan": (-97.82581, 19.59813),         # * (centro del municipio, OSM)
    "zautla": (-97.67151, 19.71392),                  # * (centro del municipio, OSM)
    "perote": (-97.26853, 19.51086),                  # *
    "xico": (-97.07076, 19.44578),                    # * (OSM)
    "xalapa": (-96.91589, 19.53124),                  # Xalapa-Enríquez (Wikipedia)
    "cempoala": (-96.40889, 19.44500),                # zona arqueológica (Wikipedia)
    "quiahuiztlan": (-96.41492, 19.66967),
    "villa_rica": (-96.39750, 19.67639),              # Villa Rica de la Veracruz, Actopan (OSM): la primera Villa Rica, 1519
    "veracruz": (-96.15333, 19.19028),                # puerto (San Juan de Ulúa enfrente)
    "tepeaca": (-97.90250, 18.96810),                 # Tepeyacac (OSM)
    "tehuacan": (-97.39783, 18.46580),
    # imperio y vecinos
    "tzintzuntzan": (-101.57889, 19.62833),           # capital purépecha (Wikipedia)
    "cuauhnahuac": (-99.23417, 18.91861),             # Cuernavaca (Wikipedia)
    "malinalco": (-99.49472, 18.94833),
    "toluca": (-99.65690, 19.29250),
    "xilotepec": (-99.53750, 19.95320),
    "huaxtepec": (-98.97200, 18.91060),               # Oaxtepec (OSM)
    "oaxaca": (-96.72528, 17.06056),                  # Huaxyacac = Oaxaca de Juárez (Wikipedia)
    "coyolapan": (-96.77980, 16.99630),               # Cuilápam (OSM)
    "tochtepec": (-96.11830, 18.08170),               # Tuxtepec, centro de los pochteca (OSM)
    "tochpan": (-97.42590, 20.95800),                 # Tuxpan (OSM)
    "cuetlaxtlan": (-96.35100, 18.85770),             # Cotaxtla (OSM)
    "tlachco": (-99.60530, 18.55650),                 # Taxco (OSM)
    "tlapan": (-98.58550, 17.52710),                  # Tlapa (OSM)
    "teotitlan": (-97.08730, 18.11930),               # Teotitlán (OSM)
    "metztitlan": (-98.82910, 20.56470),              # * (centro del municipio, OSM)
    "tututepec": (-97.62330, 16.07110),               # * (OSM)
    "acapulco": (-99.89400, 16.86800),
    "tehuantepec": (-95.24000, 16.32000),             # *
    "soconusco": (-92.72639, 15.31559),               # * Xoconochco (Wikipedia «Soconusco»: la región)
    # flecha de la migración: Aztlán es mítico → un punto en el borde norte, al noroeste de Tula
    "aztlan_flecha": (-100.70, 21.90),                # * (borde de la rejilla, no es un sitio)
}

LAGOS_ROT = {}        # rótulos de los lagos (lon, lat) del mapa de Sémhur: se llenan al cargar datos/aztecas_lineas.json
LINEAS = {}           # calzadas, albarradón y ríos de la cuenca [(lon, lat)...] (idem)


def _c_(*ks):
    return [CIUDADES[k] for k in ks]


def _lineas():
    if not LINEAS and os.path.exists(F_LINEAS):
        d = json.load(open(F_LINEAS, encoding="utf-8"))
        LINEAS.update({k: [tuple(p) for p in v] for k, v in d["lineas"].items()})
        LINEAS["rios_cuenca"] = d["rios_cuenca"]
        LAGOS_ROT.update({k: tuple(v) for k, v in d["rotulos"].items()})
    return LINEAS


_lineas()
_L = LINEAS


def _cal(k, inv=False):
    P = list(_L.get(k, []))
    return P[::-1] if inv else P


RUTAS_COMPLETAS = {
    # migración (s. XII-1325): del borde norte (Aztlán, mítico) a Tula, Tenayuca, Azcapotzalco, Chapultepec, Culhuacán, Tizapán y la isla
    "migracion": _c_("aztlan_flecha", "tula", "tenayuca", "azcapotzalco", "chapultepec", "culhuacan", "tizapan") + [
        (-99.17, 19.37), CIUDADES["tenochtitlan"]],
    # Cortés, de la costa a Tenochtitlan (ago.-nov. 1519): Villa Rica → Cempoala → Xalapa → Xico → paso del Cofre de Perote → Zautla →
    # Ixtacamaxtitlan → Tecoac → Tlaxcala → Cholula → paso entre los volcanes → Amecameca → Ayotzingo → Cuitláhuac → Iztapalapa →
    # calzada (Mexicaltzingo, Xoloc) → Tenochtitlan
    "cortes_ida": _c_("villa_rica", "cempoala", "xalapa", "xico", "perote", "zautla", "ixtacamaxtitlan", "huamantla", "tlaxcala",
                      "cholula", "paso_cortes", "amecameca", "ayotzingo", "tlahuac", "iztapalapa") + _cal("calzada_iztapalapa", True)[1:],
    # Noche Triste (30 jun.-1 jul. 1520) y retirada a Tlaxcala: calzada de Tlacopan → Los Remedios → Cuautitlán → Tepotzotlán →
    # Citlaltepec → Zumpango → (por el norte de los lagos) → Teotihuacan → Otumba (7 jul.) → Hueyotlipan → Tlaxcala
    "noche_triste": _cal("calzada_tlacopan") + _c_("los_remedios", "cuautitlan", "tepotzotlan", "citlaltepec", "zumpango") + [
        (-98.98, 19.80), (-98.90, 19.73)] + _c_("teotihuacan", "otumba", "hueyotlipan", "tlaxcala"),
    # pochteca: de Tenochtitlan por Chalco, Cholula, Tepeaca y Tehuacán a Tochtepec (Tuxtepec) y de ahí al Soconusco por Tehuantepec
    "comercio_pochteca": _c_("tenochtitlan", "iztapalapa", "chalco", "amecameca", "cholula", "tepeaca", "tehuacan", "tochtepec",
                             "tehuantepec", "soconusco"),
}
RUTAS_FIJAS = {}


def _recortar(pts, rej, paso=0.01):
    """Recorta una ruta a la caja de la rejilla: se queda con el tramo continuo más largo dentro (puntos originales + extremos)."""
    P = np.asarray(pts, float)
    m = 0.02

    def dentro(q):
        return rej.lon0 + m < q[0] < rej.lon1 - m and rej.lat1 + m < q[1] < rej.lat0 - m

    tramos, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.hypot(*(b - a)) / paso))
        for k in range(n + 1):
            q = a + (b - a) * k / n
            if dentro(q):
                if k == n:
                    cur.append(("o", tuple(b)))
                elif not cur:
                    cur.append(("c", tuple(q)))
            elif cur:
                cur.append(("c", tuple(a + (b - a) * (k - 1) / n)))
                tramos.append(cur)
                cur = []
                break
    if cur:
        tramos.append(cur)
    T = max(tramos, key=len)
    return [(round(float(p[0]), 5), round(float(p[1]), 5)) for _, p in T]


RUTAS = {k: _recortar(v, REJ["mx"]) for k, v in RUTAS_COMPLETAS.items() if len(v) > 1}
for _k in ("calzada_tepeyac", "calzada_tlacopan", "calzada_iztapalapa", "calzada_coyoacan", "albarradon", "calzada_tlahuac_n",
           "calzada_tlahuac_s"):
    if _L.get(_k):
        RUTAS[_k] = list(_L[_k])
RUTAS.update(RUTAS_FIJAS)

CELDAS_SEMILLAS = {
    # las tres cabeceras de la Triple Alianza (para partir la cuenca/el imperio en tres con `fractura`)
    "triple_alianza": _c_("tenochtitlan", "texcoco", "tlacopan"),
    # altepetl de la cuenca (ciudades-estado)
    "cuenca": _c_("tenochtitlan", "tlatelolco", "texcoco", "tlacopan", "azcapotzalco", "coyoacan", "xochimilco", "chalco", "culhuacan",
                  "iztapalapa", "xaltocan", "cuautitlan", "tenayuca", "huexotla", "coatlinchan", "chimalhuacan", "acolman", "tlahuac"),
    # cabeceras de provincias tributarias de 1519 (21 de las 38; mapa de Sémhur / Atlas del México prehispánico)
    "provincias": _c_("tenochtitlan", "tochpan", "tochtepec", "cuetlaxtlan", "tlachco", "tlapan", "tepeaca", "coyolapan", "toluca",
                      "xilotepec", "cuauhnahuac", "malinalco", "huaxtepec", "soconusco") + [
        (-97.6792, 17.2694), (-97.2544, 17.7166), (-97.1567, 20.0221), (-97.5057, 19.8386), (-98.6714, 20.3409), (-96.9655, 19.1456),
        (-99.4563, 18.1244)],   # Tlachquiauhco, Coixtlahuacan, Tlapacoyan, Tlatlauhquitepec, Atotonilco, Cuauhtochco, Tepecoacuilco
}
CELDAS_PAISES = {}

# valles fértiles (contornos holgados; el verde va donde el relieve es fondo de valle, `_valle_dem`)
VALLES = [
    [(-99.36, 19.98), (-98.72, 19.98), (-98.66, 19.55), (-98.78, 19.18), (-99.02, 19.10), (-99.28, 19.18), (-99.34, 19.45)],   # cuenca
    [(-98.60, 19.60), (-97.70, 19.60), (-97.50, 19.05), (-97.90, 18.75), (-98.50, 18.85)],                                    # Puebla-Tlaxcala
    [(-99.90, 19.60), (-99.42, 19.60), (-99.42, 19.02), (-99.85, 19.02)],                                                     # Toluca
    [(-99.40, 19.00), (-98.70, 19.00), (-98.70, 18.50), (-99.40, 18.50)],                                                     # Morelos
    [(-97.00, 17.30), (-96.40, 17.30), (-96.40, 16.75), (-97.00, 16.75)],                                                     # Oaxaca
    [(-101.95, 20.10), (-100.75, 20.10), (-100.75, 19.35), (-101.95, 19.35)],                                                 # Pátzcuaro-Cuitzeo
    [(-97.60, 20.60), (-96.10, 19.30), (-95.40, 18.50), (-95.10, 18.00), (-96.20, 17.70), (-96.80, 18.60), (-97.40, 19.60)],  # llanura del Golfo
]
VALLE_REL, VALLE_PEND = 70.0, 0.05         # m sobre el fondo local y pendiente máxima
RIOS_PESO = {"Balsas": 9.4, "Lerma": 9.2, "Papaloapan": 9.2, "Moctezuma": 8.9, "Atoyac": 8.6, "Grijalva": 9.2, "Usumacinta": 9.3,
             "Coatzacoalcos": 9.0, "Santiago": 9.0, "Pánuco": 9.0, "Verde": 8.4, "Tula": 8.3}
RIO_CUENCA_PESO = 7.0                       # ríos que bajan a los lagos (mapa de Sémhur): se ven de z ≈ 2,7 en adelante


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
                if len(P) < 3:
                    continue
                x = (P[:, 0] - rej.lon0) * rej.pxdeg
                if x.max() < -50 or x.min() > rej.FW + 50:
                    continue
                y = (rej.Y0 - ymerc(np.clip(P[:, 1], -85, 85))) * rej.pxdeg
                if y.max() < -50 or y.min() > rej.FH + 50:
                    continue
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
    Q = np.asarray(pts, float)
    ext = float(max(np.ptp(Q[:, 0]), np.ptp(Q[:, 1])))
    amp = min(0.10, max(0.006, 0.05 * ext))
    P = rej.proj_pts(_mano(pts, paso=amp * 0.4, amp=amp) if mano else pts)
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


def _clave(n):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", n) if unicodedata.category(c) != "Mn")
    return s.lower().replace(" ", "_")


# ------------------------------------------------------------------ relieve (Terrarium, Web Mercator) → rejilla del mapa
def _alt_fina(rej, f=None):
    d = np.load(f or F_FINO)
    n = 256.0 * 2 ** int(d["zoom"])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float64)
    lon = rej.lon0 + xs / rej.pxdeg
    ym = np.radians(rej.Y0 - ys / rej.pxdeg)
    mx = ((lon + 180.0) / 360.0 * n - 256.0 * int(d["x0"])).astype(np.float32)
    my = ((1.0 - ym / math.pi) / 2.0 * n - 256.0 * int(d["y0"])).astype(np.float32)
    return cv2.remap(d["z"].astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def _valle_dem(rej, e):
    """Fondos de valle (0/255): poca altura sobre el fondo local y poca pendiente, con bordes suaves."""
    e = cv2.GaussianBlur(e, (0, 0), 1.5)
    r = 30
    fondo = cv2.GaussianBlur(cv2.erode(e, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))), (0, 0), 8)
    px_m = 111320.0 * math.cos(math.radians(19.0)) / rej.pxdeg
    pend = np.hypot(cv2.Sobel(e, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(e, cv2.CV_32F, 0, 1, ksize=3)) / 8.0 / px_m
    v = ((e - fondo) < VALLE_REL) & (pend < VALLE_PEND) & (e > 0)
    v = cv2.morphologyEx(v.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    v = cv2.morphologyEx(v, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    return ((cv2.GaussianBlur(v.astype(np.float32), (0, 0), 2.0)) > 127).astype(np.uint8) * 255


def _relieve(rej, tierra, lagos, e):
    """(FH, FW, 3) int16 × ESC_AUX: luz del sombreado (-1..1), altitud 0..1 (tierra) y profundidad 0..1 (agua)."""
    es = cv2.GaussianBlur(e, (0, 0), 1.0)
    gx = cv2.Sobel(es, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(es, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    ys = np.arange(rej.FH, dtype=np.float32)
    _, lat = rej.inv(np.zeros_like(ys), ys)
    px_m = (111320.0 * np.cos(np.radians(lat)) / rej.pxdeg).astype(np.float32)[:, None]
    k = (9.0 if rej.pxdeg < 1000 else 5.0) / px_m           # de cerca (cuenca) el sombreado se suaviza: si no, cada barranco grita
    luz = np.clip(k * (gx * 0.70 + gy * 0.70), -1.0, 1.0)
    luz = np.where(tierra > 127, luz, 0.0).astype(np.float32)
    alt01 = np.interp(e, ALT_E, ALT_V).astype(np.float32)
    prof = np.clip(-e / 3500.0, 0, 1) * 0.85 + 0.15
    prof = np.where(lagos > 127, PROF_LAGO, prof)
    prof = np.where(tierra > 127, 0.0, prof).astype(np.float32)
    A = np.stack([luz, alt01, prof], -1)
    return np.clip(np.rint(A * ESC_AUX), -32000, 32000).astype(np.int16)


def _rios(rej, lineas):
    out = []
    R = json.load(open(F_RIOS, encoding="utf-8"))
    for f in R["features"]:
        n = f["properties"].get("name") or ""
        pk = [v for k, v in RIOS_PESO.items() if k in n]
        if not pk:
            continue
        g = f["geometry"]
        for c in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            P = np.asarray(c, float)
            if len(P) < 2 or P[:, 0].max() < rej.lon0 - 1 or P[:, 0].min() > rej.lon1 + 1 or P[:, 1].max() < rej.lat1 - 1 or P[:, 1].min() > rej.lat0 + 1:
                continue
            out.append((P, pk[0]))
    for P in lineas.get("rios_cuenca", []):
        out.append((np.asarray(P, float), RIO_CUENCA_PESO))
    return out


def _feats(f):
    if not os.path.exists(f):
        return {}
    d = json.load(open(f, encoding="utf-8"))
    return {x["properties"]["clave"]: x["geometry"] for x in d["features"]}


def _construir(rej):
    """Campos de la rejilla "mx" (se hace una vez y se guarda en datos/campos_mx.npz)."""
    land = json.load(open(F_LAND, encoding="utf-8"))
    edos = json.load(open(F_PAISES, encoding="utf-8"))
    lagos_ne = [f["geometry"] for f in json.load(open(F_LAGOS, encoding="utf-8"))["features"] if f["properties"].get("featurecla") == "Lake"]
    TE, CU = _feats(F_TERR), _feats(F_CUENCA)
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    lagos = cv2.bitwise_or(_mask_geoms(rej, lagos_ne), _mask_geoms(rej, [CU["lagos_1519"]]) if "lagos_1519" in CU else 0 * tierra0)
    tierra = cv2.bitwise_and(tierra0, cv2.bitwise_not(lagos))
    M = {"tierra": tierra, "lagos_1519": _mask_geoms(rej, [CU["lagos_1519"]]) if "lagos_1519" in CU else 0 * tierra0}

    def P(pts, mano=True):
        return cv2.bitwise_and(_mask_poli(rej, pts, mano), tierra)

    def G(*claves):
        return cv2.bitwise_and(_mask_geoms(rej, [TE[c] for c in claves if c in TE]), tierra)

    e = _alt_fina(rej)
    v = np.zeros_like(tierra)
    for pol in VALLES:
        v = cv2.bitwise_or(v, P(pol))
    M["valle"] = cv2.bitwise_and(v, _valle_dem(rej, e))
    todos = [f["geometry"] for f in edos["features"]]
    M["mexico_mod"] = cv2.bitwise_and(_mask_geoms(rej, todos), tierra)
    M["edo_cdmx"] = cv2.bitwise_and(_mask_geoms(rej, [f["geometry"] for f in edos["features"]
                                                      if f["properties"].get("iso_3166_2") == "MX-DIF"]), tierra)
    for k in ("imperio_1428", "imperio_1440", "imperio_1469", "imperio_1481", "imperio_1486", "imperio_1502", "imperio_1519",
              "tepanecas", "acolhuas", "tlaxcala", "teotitlan", "yopitzinco", "purepecha"):
        if k in TE:
            M[k] = G(k)
    campos = {k: _i16(_sdf(x)) for k, x in M.items()}
    aux = _relieve(rej, tierra, lagos, e)
    rios = _rios(rej, _lineas())
    return campos, aux, rios


def _construir_cuenca(rej):
    """Rejilla fina de la cuenca: tierra (con los lagos de 1519 como agua), relieve Terrarium z12 y los campos de la isla."""
    land = json.load(open(F_LAND, encoding="utf-8"))
    CU = _feats(F_CUENCA)
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    lagos = _mask_geoms(rej, [CU["lagos_1519"]])
    tierra = cv2.bitwise_and(tierra0, cv2.bitwise_not(lagos))
    e = _alt_fina(rej, F_FINO_C)
    aux = _relieve(rej, tierra, lagos, e)
    M = {"tierra": tierra, "lagos_cuenca": lagos}
    for k in ("isla_1519", "isla_1325", "islote_1325", "islote_tlatelolco"):
        if k in CU:
            M[k] = _mask_geoms(rej, [CU[k]])
    if "isla_1519" in M:      # agua que tapa lo que la isla todavía no era en 1325 (capa de agua que se encoge hasta 1519)
        M["agua_isla_1325"] = cv2.bitwise_and(M["isla_1519"], cv2.bitwise_not(cv2.bitwise_or(M.get("islote_1325", 0 * lagos),
                                                                                               M.get("islote_tlatelolco", 0 * lagos))))
    campos = {k: _i16(_sdf(x)) for k, x in M.items()}
    return campos, aux


def preparar():
    os.makedirs(DATOS, exist_ok=True)
    rej = REJ["mx"]
    campos, aux, rios = _construir(rej)
    datos = {f"c_{k}": v for k, v in campos.items()}
    datos["aux"] = aux
    datos["rios_pts"] = np.concatenate([r[0] for r in rios]).astype(np.float32)
    datos["rios_cortes"] = np.cumsum([0] + [len(r[0]) for r in rios]).astype(np.int64)
    datos["rios_peso"] = np.array([r[1] for r in rios], np.float32)
    cc, auxc = _construir_cuenca(REJ_CUENCA)
    for k, v in cc.items():
        datos[f"v_{k}"] = v
    datos["aux_v"] = auxc
    np.savez_compressed(os.path.join(DATOS, "campos_mx.npz"), **datos)
    print("mx", rej.FW, "x", rej.FH, "campos:", len(campos), "ríos:", len(rios), "| cuenca", REJ_CUENCA.FW, "x", REJ_CUENCA.FH,
          "campos:", len(cc), flush=True)


ALIAS = {"territorio": "imperio_1519", "mexicas": "imperio_1519", "triple_alianza": "imperio_1428", "imperio": "imperio_1519",
         "isla": "isla_1519", "lagos": "lagos_1519"}


def _cargar_rej(rej):
    if rej.campos:
        return
    d = np.load(os.path.join(DATOS, "campos_mx.npz"))
    rc = REJ_CUENCA
    for k in d.files:
        if k.startswith("c_"):
            rej.campos[k[2:]] = d[k]
        elif k.startswith("v_"):
            rc.campos[k[2:]] = d[k]
    rej.aux = d["aux"]
    rc.aux = d["aux_v"] if "aux_v" in d.files else None
    pts, cortes, peso = d["rios_pts"].astype(np.float64), d["rios_cortes"], d["rios_peso"]
    rej.rios = [(pts[a:b], float(p)) for a, b, p in zip(cortes[:-1], cortes[1:], peso)]
    rej.r_pts = pts
    rej.r_cortes = cortes
    rej.r_peso = peso
    for k, v in rc.campos.items():              # los campos de la isla viven en la rejilla fina (Cam.proyectar los reconoce)
        if k != "tierra":
            rej.campos.setdefault(k, v)
    for a, b in ALIAS.items():
        if b not in rej.campos and b == "imperio_1428":      # sin el mapa tepaneca aún no hay 1428: la Triple Alianza = 1440
            b = "imperio_1440"
        if b in rej.campos:
            rej.campos.setdefault(a, rej.campos[b])


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
    """(índice de celda uint8, media distancia al borde) en la rejilla "mx" (Voronoi de las semillas). Sin apilar n mapas de distancia."""
    rej = ACT
    if nombre in rej._cel:
        return rej._cel[nombre]
    seeds = rej.proj_pts(CELDAS_SEMILLAS[nombre])
    ys, xs = np.mgrid[0:rej.FH:2, 0:rej.FW:2].astype(np.float32)
    d1 = np.full(xs.shape, 1e9, np.float32)
    d2 = np.full(xs.shape, 1e9, np.float32)
    idx = np.zeros(xs.shape, np.uint8)
    for i, (sx, sy) in enumerate(seeds):
        d = np.hypot(xs - sx, ys - sy)
        m1 = d < d1
        d2 = np.where(m1, d1, np.minimum(d2, d))
        idx[m1] = i
        d1 = np.where(m1, d, d1)
    borde = ((d2 - d1) * 0.5).astype(np.float32)
    idx = cv2.resize(idx, (rej.FW, rej.FH), interpolation=cv2.INTER_NEAREST)
    borde = cv2.resize(borde, (rej.FW, rej.FH), interpolation=cv2.INTER_LINEAR)
    rej._cel[nombre] = (idx, borde)
    return rej._cel[nombre]


# ------------------------------------------------------------------ cámara
class Cam:
    """Cámara: centro (lon, lat), zoom z (px de pantalla por px de la rejilla "mx"), giro (rad)."""

    def __init__(self, lon=-99.13, lat=19.43, z=1.7, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.rej = ACT if ACT is not None else REJ["mx"]
        self.lon, self.lat, self.z, self.rot = lon, lat, z, rot
        self.zn = z * PXDEG_REF / self.rej.pxdeg
        cx, cy = self.rej.proj(lon, lat)
        c, s = math.cos(rot) * self.zn, math.sin(rot) * self.zn
        self.M = np.float32([[c, -s, W / 2 - (c * cx - s * cy)], [s, c, H / 2 - (s * cx + c * cy)]])
        # misma cámara para la rejilla fina de la cuenca (px de la cuenca → px de "mx" → pantalla)
        rc, r = REJ_CUENCA, self.rej
        k = r.pxdeg / rc.pxdeg
        A = np.array([[k, 0, (rc.lon0 - r.lon0) * r.pxdeg], [0, k, (r.Y0 - rc.Y0) * r.pxdeg], [0, 0, 1]], np.float64)
        self.Mc = (np.vstack([self.M.astype(np.float64), [0, 0, 1]]) @ A)[:2].astype(np.float32)
        self.znc = self.zn * k

    def pant(self, lon, lat):
        x, y = self.rej.proj(lon, lat)
        M = self.M
        return float(M[0, 0] * x + M[0, 1] * y + M[0, 2]), float(M[1, 0] * x + M[1, 1] * y + M[1, 2])

    def pant_pts(self, P):
        P = np.asarray(P, float)
        x, y = self.rej.proj(P[:, 0], P[:, 1])
        M = self.M
        return np.stack([M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2]], 1)

    def _matriz(self, campo):
        if campo.shape[:2] == (REJ_CUENCA.FH, REJ_CUENCA.FW) and campo.shape[:2] != (self.rej.FH, self.rej.FW):
            return self.Mc, self.znc
        return self.M, self.zn

    def proyectar(self, campo, relleno=4000.0):
        M, zn = self._matriz(campo)
        if campo.dtype == np.int16:
            r = cv2.warpAffine(campo, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=int(min(relleno * ESC_I16, 32000)))
            return r.astype(np.float32) * np.float32(zn / ESC_I16)
        r = cv2.warpAffine(campo, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)
        return r * np.float32(zn)

    def proyectar_crudo(self, img, relleno=0.0, interp=cv2.INTER_LINEAR):
        M, _ = self._matriz(img)
        r = cv2.warpAffine(img, M, (W, H), flags=interp, borderMode=cv2.BORDER_REPLICATE)
        if r.dtype == np.int16:
            return r.astype(np.float32) * np.float32(1.0 / ESC_AUX)
        return r

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
                u = pr ** 0.6 if pr > 1e-4 else 0.0     # fastmath: 0 ** 0,6 daba NaN (puntos negros en la orilla)
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


def peso_cuenca(cam):
    """(H, W) 0..1: dónde y cuánto manda la rejilla fina de la cuenca (None si no se ve o la cámara está lejos)."""
    rc = REJ_CUENCA
    if rc.aux is None or "tierra" not in rc.campos:
        return None
    kz = clamp01((cam.znc - 0.24) / 0.22)          # px de pantalla por px de la cuenca: < 0,24 sería submuestrear (z < 1,6)
    if kz <= 0:
        return None
    m4 = 4
    P = np.array([[0, 0], [rc.FW, 0], [rc.FW, rc.FH], [0, rc.FH]], np.float64)
    P = (np.c_[P, np.ones(4)] @ cam.Mc.astype(np.float64).T) / m4
    if P[:, 0].max() < 0 or P[:, 0].min() > W / m4 or P[:, 1].max() < 0 or P[:, 1].min() > H / m4:
        return None
    m = np.zeros((H // m4, W // m4), np.float32)
    cv2.fillConvexPoly(m, np.rint(P).astype(np.int32), 1.0, cv2.LINE_AA)
    pl = max(2, int(min(18, 0.03 * rc.FW * cam.znc / m4)))      # fundido: 3 % del ancho de la cuenca, como mucho 72 px
    m = cv2.erode(m, np.ones((2 * pl + 1, 2 * pl + 1), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), pl * 0.6)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR) * np.float32(kz)


def pintar_base(cam, fase=0):
    """Fondo: mar con profundidad, tierra con relieve y valles verdes; los lagos de 1519 como agua clara.
    De cerca, la cuenca de México sale de su rejilla fina (2000 px/°) fundida con la general."""
    rej = cam.rej
    img = np.empty((H, W, 3), np.float32)
    S = cam.proyectar(rej.campos["tierra"])
    aux = cam.proyectar_crudo(rej.aux)
    wc = peso_cuenca(cam)
    if wc is not None:
        rc = REJ_CUENCA
        Sc = cam.proyectar(rc.campos["tierra"])
        auxc = cam.proyectar_crudo(rc.aux)
        S = S + (Sc - S) * wc
        aux = aux + (auxc - aux) * wc[..., None]
    _tierra_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, aux, _c(TIERRA), _c(TIERRA_ALTA), _c(TIERRA_CUMBRE), _c(MAR_CL), _c(MAR_HONDO), _c((214, 234, 230)),
               np.float32(3.0), 0, H, 0, W)
    b = Base()
    b.S, b.luz = S, np.ascontiguousarray(aux[..., 0])
    b.cuenca = wc
    Sv = cam.proyectar(rej.campos["valle"])
    av = 0.62 * clamp01(1.0 - (cam.z - 10.0) / 20.0)       # el verde de valle es de la rejilla general: de muy cerca se retira
    if av > 0.01:
        pintar(img, Sv, VALLE, av, fase, borde=0.35, sombra=0.08, ruido=0.6, luz=b.luz, kluz=0.28)
    return img, b


def pintar_rios(img, cam, base, t=0.0, alfa=0.92, minimo=None):
    """Ríos (pincelada azul) sobre tierra y territorios; grosor según el peso del río y el zoom."""
    rej = cam.rej
    if minimo is None:
        minimo = float(np.interp(math.log(max(cam.z, 0.05)), [math.log(1.0), math.log(3.0)], [8.3, 6.8]))
    Q = cam.pant_pts(rej.r_pts)
    Q16 = np.rint(np.clip(Q, -30000, 30000) * 16).astype(np.int32)
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


def pintar_calzadas(img, cam, claves=("calzada_tepeyac", "calzada_tlacopan", "calzada_iztapalapa", "calzada_coyoacan"), alfa=1.0,
                    u=1.0, ancho_m=12.0, albarradon=True):
    """Calzadas (bandas de tierra clara con borde de tinta) y albarradón de Nezahualcóyotl (línea de estacas) sobre el lago.
    u = 0..1: cuánto de cada calzada está hecho (para verlas crecer). Para usar en un `R.fondo` o en una escena de la isla."""
    if alfa <= 0.01:
        return
    px_m = cam.zn * cam.rej.pxdeg / 111320.0 * 1.06                 # px de pantalla por metro (≈ a 19,4° N)
    w = max(2.0, min(14.0, ancho_m * px_m))
    m = np.zeros((H, W), np.uint8)
    t = np.zeros((H, W), np.uint8)
    for k in claves:
        P = np.asarray(LINEAS.get(k, []), float)
        if len(P) < 2:
            continue
        if u < 1.0:
            d = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
            L = d[-1] * clamp01(u)
            j = int(np.searchsorted(d, L))
            if j <= 0:
                continue
            q = P[j - 1] + (P[min(j, len(P) - 1)] - P[j - 1]) * ((L - d[j - 1]) / max(1e-9, d[min(j, len(P) - 1)] - d[j - 1]))
            P = np.vstack([P[:j], q])
        Q = np.rint(cam.pant_pts(P) * 16).astype(np.int32)
        cv2.polylines(t, [Q], False, 255, int(round(w + 3)), cv2.LINE_AA, 4)
        cv2.polylines(m, [Q], False, 255, int(round(w)), cv2.LINE_AA, 4)
    for mm, col, k in ((t, TINTA_MAPA, 0.85), (m, CALZADA, 1.0)):
        ys, xs = np.nonzero(mm)
        if len(ys):
            a = (mm[ys, xs].astype(np.float32) / 255.0)[:, None] * alfa * k
            c = _c(col) * (1 + 1.2 * PINCEL[ys, xs])[:, None] * GRANO[ys, xs]
            img[ys, xs] = img[ys, xs] * (1 - a) + c * a
    if albarradon and LINEAS.get("albarradon"):
        P = np.asarray(LINEAS["albarradon"], float)
        Q = cam.pant_pts(P)
        d = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(Q, axis=0).T))])
        paso = max(5.0, 2.2 * w)
        for s in np.arange(0, d[-1], paso):
            j = min(len(Q) - 2, int(np.searchsorted(d, s) - 1))
            j = max(0, j)
            q = Q[j] + (Q[j + 1] - Q[j]) * ((s - d[j]) / max(1e-9, d[j + 1] - d[j]))
            if -10 < q[0] < W + 10 and -10 < q[1] < H + 10:
                cv2.circle(img, (int(q[0]), int(q[1])), max(1, int(w * 0.45)), tuple(float(v) for v in _c(TINTA_MAPA)), -1, cv2.LINE_AA)


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
