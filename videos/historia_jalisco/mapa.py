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
F_LAND = os.path.join(AQUI, "datos", "ne_10m_land.geojson")
F_PAISES = os.path.join(AQUI, "datos", "estados_mx.geojson")
F_RIOS = os.path.join(AQUI, "datos", "ne_10m_rivers_lake_centerlines.geojson")
F_LAGOS = os.path.join(AQUI, "datos", "ne_10m_lakes.geojson")
F_NC = os.path.join(AQUI, "datos", "relieve_jal_etopo1.nc")
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


REJ = {"mx": Rej("mx", -108.5, -98.5, 25.0, 17.0, 260.0)}   # llave "mx" para no tocar el kit; es Jalisco y su entorno
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
    "jalisco": (204, 92, 66),
    "teuchitlan": (196, 120, 62),
    "tumbas": (176, 132, 80),
    "caxcanes": (198, 104, 58),
    "tecuexes": (110, 150, 96),
    "cocas": (86, 140, 160),
    "wixarika": (226, 170, 60),
    "purepecha": (150, 96, 150),
    "guzman": (176, 52, 48),
    "nueva_galicia": (214, 156, 58),
    "nueva_espana": (196, 168, 120),
    "mixton": (204, 70, 52),
    "insurgentes": (74, 146, 98),
    "realistas": (78, 112, 174),
    "estado_libre": (204, 72, 58),
    "federacion": (98, 150, 104),
    "liberales": (74, 138, 104),
    "conservadores": (150, 94, 158),
    "porfiriato": (196, 146, 68),
    "cristeros": (198, 70, 60),
    "metro": (210, 110, 70),
    "mexico_mod": (78, 148, 96),
}
COL_ESTADOS = {
    "Jalisco": (204, 92, 66), "Nayarit": (96, 150, 120), "Zacatecas": (214, 168, 80), "Aguascalientes": (176, 120, 160),
    "Guanajuato": (98, 134, 184), "Michoacán": (150, 176, 84), "Colima": (230, 150, 110), "Durango": (180, 160, 90),
    "Sinaloa": (110, 170, 170), "San Luis Potosí": (206, 98, 120), "Querétaro": (122, 160, 104), "Hidalgo": (226, 150, 110),
    "México": (140, 120, 190), "Distrito Federal": (200, 120, 60), "Guerrero": (92, 120, 160), "Morelos": (238, 178, 64),
}
COL_CELDAS = [
    (214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
    (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110),
]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat)
CIUDADES = {
    "guadalajara": (-103.35, 20.67), "zapopan": (-103.39, 20.72), "tonala": (-103.23, 20.62), "tlaquepaque": (-103.31, 20.64),
    "atemajac": (-103.36, 20.70), "tlacotan": (-103.25, 20.87), "nochistlan": (-102.84, 21.36), "juchipila": (-103.12, 21.41),
    "mixton": (-103.03, 21.47), "teocaltiche": (-102.57, 21.43), "tlaltenango": (-103.30, 21.78),
    "tequila": (-103.84, 20.88), "volcan_tequila": (-103.85, 20.79), "teuchitlan": (-103.85, 20.68), "guachimontones": (-103.84, 20.695),
    "cocula": (-103.82, 20.37), "chapala": (-103.19, 20.29), "ocotlan": (-102.77, 20.35), "sayula": (-103.60, 19.88),
    "zapotlan": (-103.46, 19.70), "autlan": (-104.36, 19.77), "puerto_vallarta": (-105.23, 20.62), "tepatitlan": (-102.76, 20.82),
    "arandas": (-102.35, 20.70), "san_juan_lagos": (-102.33, 21.25), "lagos_moreno": (-101.93, 21.36), "zapotlanejo": (-103.07, 20.62),
    "puente_calderon": (-103.00, 20.60), "colotlan": (-103.27, 22.11), "mezquitic": (-103.72, 21.90), "huejuquilla": (-103.90, 22.62),
    "compostela": (-104.90, 21.24), "tepic": (-104.89, 21.50), "colima": (-103.72, 19.24), "zacatecas": (-102.57, 22.77),
    "aguascalientes": (-102.29, 21.88), "guanajuato": (-101.26, 21.02), "irapuato": (-101.35, 20.68), "la_piedad": (-102.03, 20.35),
    "morelia": (-101.19, 19.70), "tzintzuntzan": (-101.58, 19.63), "cdmx": (-99.13, 19.43), "queretaro": (-100.39, 20.59),
    "culiacan": (-107.39, 24.80), "dolores": (-100.93, 21.16), "estadio": (-103.46, 20.68),
}

RUTAS = {
    "guzman": [(-101.19, 19.70), (-102.40, 20.20), (-103.23, 20.62), (-103.84, 20.88), (-104.89, 21.50), (-105.80, 22.60), (-107.39, 24.80)],
    "gdl_mudanzas": [(-102.84, 21.36), (-103.23, 20.62), (-103.25, 20.87), (-103.35, 20.67)],
    "mendoza": [(-99.13, 19.43), (-100.39, 20.59), (-101.26, 21.02), (-102.40, 21.20), (-102.84, 21.36), (-103.12, 21.41), (-103.03, 21.47)],
    "alvarado": [(-103.25, 20.87), (-103.05, 21.10), (-102.84, 21.36)],
    "caxcanes_ataque": [(-103.06, 21.33), (-103.15, 21.15), (-103.25, 20.87)],
    "camino_plata": [(-103.35, 20.67), (-102.90, 21.30), (-102.29, 21.88), (-102.57, 22.77)],
    "torres": [(-103.65, 20.15), (-103.55, 20.40), (-103.35, 20.67)],
    "hidalgo": [(-101.19, 19.70), (-102.00, 20.10), (-102.77, 20.35), (-103.35, 20.67)],
    "hidalgo_sale": [(-103.35, 20.67), (-103.07, 20.62), (-103.00, 20.60)],
    "calleja": [(-101.26, 21.02), (-101.93, 21.36), (-102.76, 20.82), (-103.00, 20.60)],
    "tren": [(-101.35, 20.68), (-102.03, 20.35), (-102.77, 20.35), (-103.35, 20.67)],
    "cristeros": [(-102.33, 21.25), (-102.76, 20.82), (-102.35, 20.70), (-101.93, 21.36)],
}

CELDAS_SEMILLAS = {
    "pueblos": [(-103.10, 21.60), (-102.80, 20.95), (-103.35, 20.40), (-104.10, 22.10), (-103.90, 20.70), (-103.50, 19.80)],
}
CELDAS_PAISES = {}

# ------------------------------------------------------------------ polígonos históricos (lon, lat), aproximados
VALLE_VERDE = [  # riberas fértiles: valle de Atemajac, Tequila, Chapala y la costa
    (-104.2, 20.95), (-103.2, 20.95), (-102.6, 20.45), (-102.6, 20.15), (-103.5, 20.10), (-104.0, 20.35),
]
TEUCHITLAN = [(-104.25, 20.95), (-103.55, 21.0), (-103.35, 20.55), (-103.75, 20.35), (-104.2, 20.5)]
TUMBAS = [(-105.3, 22.0), (-103.6, 21.8), (-102.9, 20.6), (-103.3, 19.2), (-104.4, 18.9), (-105.2, 20.2)]
CAXCANES = [(-104.0, 22.3), (-102.9, 22.4), (-102.3, 21.6), (-102.6, 21.1), (-103.4, 21.0), (-103.9, 21.5)]
TECUEXES = [(-103.4, 21.0), (-102.6, 21.1), (-102.2, 20.9), (-102.5, 20.55), (-103.2, 20.55)]
COCAS = [(-103.8, 20.62), (-103.2, 20.58), (-102.6, 20.4), (-102.8, 20.05), (-103.5, 20.0), (-103.9, 20.25)]
WIXARIKA = [(-104.6, 22.9), (-103.7, 22.9), (-103.5, 22.2), (-103.9, 21.6), (-104.5, 21.8)]
SALINAS = [(-103.75, 20.05), (-103.3, 20.0), (-103.2, 19.55), (-103.6, 19.45), (-103.85, 19.75)]
GUZMAN = [(-101.6, 19.9), (-102.6, 20.6), (-103.6, 21.0), (-104.8, 21.8), (-106.2, 23.4), (-107.6, 24.9), (-106.4, 25.0),
          (-105.2, 22.6), (-104.0, 21.2), (-103.4, 20.3), (-102.0, 19.8)]
ALTOS = [(-103.1, 21.2), (-102.3, 21.95), (-101.55, 21.75), (-101.6, 21.1), (-102.2, 20.5), (-102.9, 20.55)]
METRO = [(-103.50, 20.76), (-103.42, 20.80), (-103.30, 20.79), (-103.21, 20.74), (-103.17, 20.66), (-103.20, 20.58), (-103.30, 20.55),
         (-103.42, 20.56), (-103.50, 20.61), (-103.54, 20.69)]
INSURGENTES = [(-104.2, 21.1), (-102.6, 21.3), (-101.4, 20.6), (-102.4, 19.7), (-103.8, 19.8)]

# Ríos de apoyo (Natural Earth 10 m ya trae el Santiago y el Lerma; esto asegura el trazo en el lago de Chapala)
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
RIOS_SI = {"Grande de Santiago": 9.3, "Lerma": 9.1, "Verde": 8.6, "Purificaci": 8.4, "Atengo": 8.4, "San Pedro": 8.4,
           "Balsas": 8.6, "Moctezuma": 8.3, "nuco": 8.3}
ESTADOS = ("Jalisco", "Nayarit", "Zacatecas", "Aguascalientes", "Guanajuato", "Michoacán", "Colima")


def _nombre(f):
    n = f["properties"].get("name") or ""
    return n.encode("latin-1", "ignore").decode("utf-8", "ignore") if "Ã" in n else n


def _estados(nombres):
    return [f["geometry"] for f in _PAISES["features"] if _nombre(f) in nombres]


def _construir(rej):
    """Calcula todos los campos de la rejilla de Jalisco (se hace una vez y se guarda en datos/campos_mx.npz)."""
    global _PAISES, _RIOS
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    _RIOS = json.load(open(F_RIOS, encoding="utf-8"))
    lagos = json.load(open(F_LAGOS, encoding="utf-8"))
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    perm = [f["geometry"] for f in lagos["features"] if (f["properties"].get("name") or "") in ("Lago de Chapala",)]
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

    def edos(*n):
        return cv2.bitwise_and(_mask_geoms(rej, _estados(n)), tierra)

    todos = sorted({_nombre(f) for f in _PAISES["features"]} - {""})
    mx = edos(*todos)
    jal = edos("Jalisco")
    M["jalisco"] = jal
    M["mexico_mod"] = mx
    for n in ESTADOS[1:]:
        M["edo_" + n.lower().replace("á", "a")] = edos(n)
    M["resto_mx"] = menos(mx, edos(*ESTADOS))
    M["valle"] = P(VALLE_VERDE)
    M["teuchitlan"] = P(TEUCHITLAN)
    M["tumbas"] = P(TUMBAS)
    M["caxcanes"] = P(CAXCANES)
    M["tecuexes"] = P(TECUEXES)
    M["cocas"] = P(COCAS)
    M["wixarika"] = P(WIXARIKA)
    M["salinas"] = P(SALINAS)
    M["purepecha"] = edos("Michoacán")
    M["guzman"] = P(GUZMAN)
    ng = U_(jal, edos("Nayarit", "Aguascalientes", "Zacatecas"))
    M["nueva_galicia"] = ng
    M["nueva_espana"] = menos(mx, ng)
    M["insurgentes"] = P(INSURGENTES)
    M["altos"] = P(ALTOS)
    M["metro"] = P(METRO)
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
        n = f["properties"].get("name") or ""
        pk = [v for k, v in RIOS_SI.items() if k in n]
        if not pk:
            continue
        g = f["geometry"]
        for c in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            P = np.asarray(c, float)
            if len(P) < 2:
                continue
            out.append((P, pk[0]))
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
