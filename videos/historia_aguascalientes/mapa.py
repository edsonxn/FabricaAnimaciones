# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Aguascalientes» (kit v2.1 de historia_jalisco), con RELIEVE REAL SRTM15+.

Una sola rejilla en proyección de MERCATOR, con la llave "mx" para no tocar el kit:
  - "mx": de Zacatecas a Lagos de Moreno y de Jerez/Juchipila a San Luis Potosí (lon -104.2.. -100.1, lat 23.05.. 20.85;
    ancha para que con z 0,74 quepa casi toda en 16:9), 640 px por grado (el estado de Aguascalientes llena la pantalla con
    z ≈ 1,8; la capital de cerca con z 5-8).
    Bajo el guache: sombreado con AWS Terrain Tiles (Terrarium z10 ≈ 140 m, datos/relieve_ags_terrarium_z10.npz); ríos y presa
    con SRTM15+ (15", datos/relieve_ags_srtm15.nc, ERDDAP srtm15plus); valles verdes (San Pedro y Calvillo),
    Presa Calles inundada sobre el propio relieve y red de ríos calculada del relieve (D8). Estados de Natural Earth 10 m.
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
F_NC = os.path.join(AQUI, "datos", "relieve_ags_srtm15.nc")   # ERDDAP srtm15plus, z[(20.6):(23.3)][(-104.5):(-99.8)]
F_FINO = os.path.join(AQUI, "datos", "relieve_ags_terrarium_z10.npz")  # AWS Terrain Tiles (Terrarium z10 ≈ 140 m), solo para el sombreado
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


REJ = {"mx": Rej("mx", -104.20, -100.10, 23.05, 20.85, 640.0)}   # llave "mx" para no tocar el kit; es Aguascalientes y su entorno
PXDEG_REF = REJ["mx"].pxdeg

# ------------------------------------------------------------------ paleta de guache (papel cálido, sierra ocre, valle verde, presas azules)
MAR = (168, 204, 212)
MAR_HONDO = (124, 168, 194)
MAR_CL = (204, 228, 224)
TIERRA = (236, 220, 184)
TIERRA_ALTA = (202, 174, 132)
TIERRA_CUMBRE = (236, 230, 216)
RIO = (88, 148, 196)
VALLE = (144, 180, 110)
AGUA_LAGO = (128, 184, 212)
# el altiplano entero está a 1 800-2 000 m: la escala de color del relieve empieza en ALT_BASE (cañones = tierra baja, valle = medio,
# Sierra Fría y Laurel = ocre alto, cumbres > ~2 600 m casi blancas). En Jalisco era 0..2 600 m.
ALT_BASE, ALT_RANGO = 1500.0, 1500.0

COL = {
    # estados (Aguascalientes protagonista, vecinos más apagados)
    "aguascalientes": (204, 92, 66),
    "edo_zacatecas": (214, 168, 80),
    "edo_jalisco": (110, 150, 96),
    "edo_san_luis_potosi": (150, 96, 150),
    "edo_guanajuato": (98, 134, 184),
    "resto_mx": (196, 168, 120),
    "mexico_mod": (78, 148, 96),
    # pueblos chichimecas y vecinos
    "chichimecas": (196, 120, 62),
    "guachichiles": (226, 170, 60),
    "guamares": (150, 96, 150),
    "zacatecos": (176, 132, 80),
    "caxcanes": (198, 104, 58),
    "tecuexes": (110, 150, 96),
    # colonia y siglo XIX
    "nueva_galicia": (214, 156, 58),
    "nueva_espana": (196, 168, 120),
    "zacatecas_dep": (190, 140, 70),
    "territorio": (204, 72, 58),
    "estado_libre": (204, 72, 58),
    "insurgentes": (74, 146, 98),
    "realistas": (78, 112, 174),
    "federacion": (98, 150, 104),
    "liberales": (74, 138, 104),
    "conservadores": (150, 94, 158),
    # siglo XX
    "porfiriato": (196, 146, 68),
    "revolucion": (198, 70, 60),
    "cristeros": (198, 70, 60),
    "metro": (210, 110, 70),
    "valle": VALLE,
    "presa_calles": AGUA_LAGO,
}
COL_ESTADOS = {
    "Aguascalientes": (204, 92, 66), "Zacatecas": (214, 168, 80), "Jalisco": (110, 150, 96), "San Luis Potosí": (150, 96, 150),
    "Guanajuato": (98, 134, 184),
}
COL_CELDAS = [
    (214, 120, 64), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60),
    (140, 120, 190), (180, 160, 90), (110, 170, 170), (206, 98, 120), (150, 176, 84), (92, 120, 160), (226, 150, 110),
]

# ------------------------------------------------------------------ geografía de apoyo (lon, lat); «aprox.» = sitio histórico sin coordenada fiable
CIUDADES = {
    # capital y sus barrios
    "aguascalientes": (-102.2916, 21.8818), "plaza_patria": (-102.2960, 21.8818), "san_marcos": (-102.3044, 21.8778),
    "encino": (-102.2915, 21.8763), "estacion": (-102.2790, 21.8865), "ojocaliente": (-102.2715, 21.8795),
    "cerro_muerto": (-102.4292, 21.8667),            # cumbre en SRTM15+ (2 380 m), al poniente del centro
    # resto del estado
    "el_ocote": (-102.5600, 21.7650),                 # aprox. (≈ 31 km al SO, junto a la raya con Jalisco; cerro Los Tecuanes)
    "real_asientos": (-102.0897, 22.2386), "calvillo": (-102.7186, 21.8467), "san_jose_gracia": (-102.4194, 22.1464),
    "presa_calles": (-102.4450, 22.1500), "cristo_roto": (-102.4330, 22.1400), "rincon_romos": (-102.3214, 22.2333),
    "pabellon_hidalgo": (-102.3380, 22.1850), "pabellon_arteaga": (-102.2764, 22.1494), "jesus_maria": (-102.3436, 21.9614),
    "san_francisco_romo": (-102.2717, 22.0756), "tepezala": (-102.1700, 22.2244), "cosio": (-102.3000, 22.3667),
    "el_llano": (-101.9667, 21.9167),
    "cienega_grande": (-102.0200, 22.1942),           # localidad actual (Asientos); el presidio de c. 1570-80 estaba por ahí (aprox.)
    "bocas_gallardo": (-102.2700, 21.7200),           # aprox.: presidio en el sur de Ags, sobre el Camino Real
    "palmillas": (-102.3000, 22.4100),                # aprox.: presidio, sobre el Camino Real hacia Zacatecas
    # vecinos
    "zacatecas": (-102.5832, 22.7709), "guadalupe_zac": (-102.5200, 22.7470), "jerez": (-102.9900, 22.6500),
    "lagos_moreno": (-101.9292, 21.3564), "encarnacion": (-102.2400, 21.5200), "teocaltiche": (-102.5700, 21.4300),
    "juchipila": (-103.1200, 21.4100), "ojuelos": (-101.5900, 21.8600), "san_luis_potosi": (-100.9760, 22.1500),
    "leon": (-101.6800, 21.1200), "silao": (-101.4300, 20.9400), "san_juan_lagos": (-102.3300, 21.2500),
    # fuera de la caja: punto en el borde, en la dirección real desde la capital (para flechas); la posición real va en *_real
    "guadalajara": (-103.1800, 20.9000), "guadalajara_real": (-103.3500, 20.6700),
    "ciudad_mexico": (-100.9600, 20.8900), "ciudad_mexico_real": (-99.1330, 19.4330),
    "queretaro": (-100.7700, 20.8900), "queretaro_real": (-100.3900, 20.5900),
}

RUTAS_COMPLETAS = {        # trazado real; RUTAS = estas mismas recortadas a la caja
    # Camino Real de Tierra Adentro: México → Querétaro → Celaya → Irapuato → Silao → León → Lagos → Ags → Zacatecas
    "camino_plata": [(-99.133, 19.433), (-99.70, 19.80), (-100.39, 20.59), (-100.82, 20.52), (-101.35, 20.68), (-101.43, 20.94),
                     (-101.68, 21.12), (-101.93, 21.36), (-102.10, 21.47), (-102.24, 21.52), (-102.27, 21.63), (-102.29, 21.88),
                     (-102.31, 22.03), (-102.33, 22.18), (-102.32, 22.23), (-102.30, 22.37), (-102.38, 22.52), (-102.52, 22.75),
                     (-102.583, 22.771)],
    # Ferrocarril Central Mexicano (1884): mismo corredor, más recto; estación de Ags al oriente del centro
    "tren": [(-99.133, 19.433), (-100.39, 20.59), (-101.35, 20.68), (-101.43, 20.94), (-101.68, 21.12), (-101.93, 21.36),
             (-102.24, 21.52), (-102.27, 21.70), (-102.279, 21.8865), (-102.29, 22.03), (-102.276, 22.149), (-102.32, 22.233),
             (-102.30, 22.367), (-102.42, 22.58), (-102.52, 22.747), (-102.583, 22.771)],
}
RUTAS_FIJAS = {
    # ruta para visitar: Plaza de la Patria → Calvillo → San José de Gracia (Presa Calles) → Pabellón de Hidalgo → Real de Asientos
    "ruta_turista": [(-102.2960, 21.8818), (-102.40, 21.875), (-102.53, 21.865), (-102.7186, 21.8467), (-102.66, 21.95), (-102.56, 22.04),
                     (-102.4194, 22.1464), (-102.338, 22.185), (-102.22, 22.22), (-102.0897, 22.2386)],
    # la capital y sus barrios (para un paseo de cerca)
    "paseo_capital": [(-102.2715, 21.8795), (-102.2790, 21.8865), (-102.2960, 21.8818), (-102.2915, 21.8763), (-102.3044, 21.8778)],
    # Santa Anna llega de Zacatecas (1835)
    "santa_anna": [(-102.583, 22.771), (-102.52, 22.75), (-102.38, 22.52), (-102.30, 22.37), (-102.32, 22.23), (-102.31, 22.03),
                   (-102.2916, 21.8818)],
}

CELDAS_SEMILLAS = {
    # cabeceras de los 11 municipios (para partir el estado en municipios con `fractura`)
    "municipios": [(-102.2916, 21.8818), (-102.0897, 22.2386), (-102.7186, 21.8467), (-102.3000, 22.3667), (-102.3436, 21.9614),
                   (-102.2764, 22.1494), (-102.3214, 22.2333), (-102.4194, 22.1464), (-102.1700, 22.2244), (-101.9667, 21.9167),
                   (-102.2717, 22.0756)],
    "pueblos": [(-102.60, 22.60), (-101.60, 22.50), (-102.90, 21.80), (-101.50, 21.40), (-102.40, 21.30), (-102.25, 21.95)],
}
CELDAS_PAISES = {}

# ------------------------------------------------------------------ polígonos históricos (lon, lat), aproximados (el contorno se tiembla a mano)
# valles fértiles: dentro de estos contornos holgados, el verde va donde el relieve es fondo de valle (`_valle_dem`)
VALLE_VERDE = [  # valle del río San Pedro (de Cosío a la capital y al sur, hasta Encarnación)
    (-102.42, 22.42), (-102.20, 22.42), (-102.14, 22.10), (-102.14, 21.80), (-102.16, 21.50), (-102.36, 21.48), (-102.42, 21.85),
    (-102.46, 22.10),
]
VALLE_CALVILLO = [(-102.86, 21.95), (-102.60, 21.96), (-102.57, 21.80), (-102.70, 21.73), (-102.86, 21.76)]   # guayaba
VALLE_REL, VALLE_PEND = 45.0, 0.06         # m sobre el fondo local (radio ≈ 4 km) y pendiente máxima
GUACHICHILES = [(-102.25, 23.10), (-100.00, 23.10), (-100.00, 21.80), (-101.55, 21.90), (-101.95, 22.05), (-102.15, 22.30),
                (-102.25, 22.60)]
GUAMARES = [(-101.95, 21.95), (-101.55, 21.85), (-100.00, 21.75), (-100.00, 20.80), (-101.50, 20.80), (-101.85, 21.20), (-102.05, 21.55)]
ZACATECOS = [(-104.30, 23.10), (-102.30, 23.10), (-102.30, 22.60), (-102.55, 22.35), (-103.00, 22.35), (-104.30, 22.45)]
CAXCANES = [(-103.80, 22.45), (-103.00, 22.35), (-102.70, 22.05), (-102.55, 21.70), (-102.45, 21.35), (-102.95, 21.10),
            (-103.80, 21.15)]
TECUEXES = [(-102.95, 21.10), (-102.45, 21.35), (-102.10, 21.32), (-101.90, 21.05), (-101.95, 20.80), (-103.60, 20.80)]
METRO = [(-102.36, 21.95), (-102.29, 21.97), (-102.23, 21.94), (-102.22, 21.87), (-102.24, 21.81), (-102.30, 21.79),
         (-102.35, 21.82), (-102.37, 21.88)]
INSURGENTES = [(-102.70, 22.40), (-102.00, 22.40), (-101.60, 21.40), (-102.40, 21.10), (-103.00, 21.60)]

# Ríos: Natural Earth 10 m solo trae el Santiago, lejos de aquí → la red de ríos sale del propio relieve SRTM15+ (`_rios_dem`:
# relleno de depresiones + D8 + acumulación; San Pedro-Verde, Juchipila, Calvillo, Santiago-Pabellón, Encarnación...).
RIOS_EXTRA = []
RIO_SUMIDERO, RIO_SUM_AREA = 10.0, 400   # depresión de ≥ 10 m y ≥ 400 celdas (≈ 80 km²) = cuenca cerrada (las chicas son ruido)
RIO_A0 = 260                 # celdas de 15" (≈ 0,2 km² c/u) que drenan a un punto para que haya río (≈ 50 km²)
# Presa Calles (1927-28): Natural Earth no la trae → se inunda el relieve hasta un nivel que deja ≈ PRESA_CELDAS celdas de 15"
PRESA_SEMILLA, PRESA_CELDAS, PRESA_CAJA = (-102.445, 22.152), 75, (-102.54, -102.39, 22.09, 22.21)


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
    return [(round(float(p[0]), 4), round(float(p[1]), 4)) for _, p in T]


RUTAS = {k: _recortar(v, REJ["mx"]) for k, v in RUTAS_COMPLETAS.items()}
RUTAS.update(RUTAS_FIJAS)


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
    Q = np.asarray(pts, float)
    ext = float(max(np.ptp(Q[:, 0]), np.ptp(Q[:, 1])))
    amp = min(0.10, max(0.006, 0.05 * ext))         # el temblor a mano, proporcional al tamaño (la mancha urbana no se deforma)
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


_PAISES = None
_RIOS = None
RIOS_SI = {}                 # Natural Earth no trae ríos útiles en esta caja (ver _rios_dem); se deja el mecanismo por subcadena
ESTADOS = ("Aguascalientes", "Zacatecas", "Jalisco", "San Luis Potosí", "Guanajuato")


def _nombre(f):
    n = f["properties"].get("name") or ""
    return n.encode("latin-1", "ignore").decode("utf-8", "ignore") if "Ã" in n else n


def _clave(n):
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", n) if unicodedata.category(c) != "Mn")
    return s.lower().replace(" ", "_")


def _estados(nombres):
    ks = {_clave(n) for n in nombres}
    return [f["geometry"] for f in _PAISES["features"] if _clave(_nombre(f)) in ks]


# ------------------------------------------------------------------ relieve SRTM15+ (rejilla del DEM → rejilla del mapa)
_DEM = None


def _dem():
    """(z, lat, lon) del relieve, lat y lon crecientes."""
    global _DEM
    if _DEM is None:
        from scipy.io import netcdf_file
        f = netcdf_file(F_NC, "r", mmap=False)
        var = "z" if "z" in f.variables else "altitude"
        z = f.variables[var][:].astype(np.float32).copy()
        lat_ = f.variables["latitude"][:].astype(np.float64).copy()
        lon_ = f.variables["longitude"][:].astype(np.float64).copy()
        if lat_[0] > lat_[-1]:
            z, lat_ = z[::-1].copy(), lat_[::-1].copy()
        _DEM = (z, lat_, lon_)
    return _DEM


def _a_rejilla(rej, arr, interp=cv2.INTER_LINEAR):
    """Lleva un arreglo en la rejilla del DEM a la rejilla del mapa (Mercator)."""
    _, lat_, lon_ = _dem()
    paso = float(lat_[1] - lat_[0])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float32)
    lon, lat = rej.inv(xs, ys)
    mi = ((lat - lat_[0]) / paso).astype(np.float32)
    mj = ((lon - lon_[0]) / float(lon_[1] - lon_[0])).astype(np.float32)
    return cv2.remap(arr.astype(np.float32), mj, mi, interp, borderMode=cv2.BORDER_REPLICATE)


def _alt_fina(rej):
    """Altitud en la rejilla del mapa desde el mosaico Terrarium z10 (Web Mercator, ≈ 140 m); si no está, la de SRTM15+."""
    if not os.path.exists(F_FINO):
        return _a_rejilla(rej, _dem()[0])
    d = np.load(F_FINO)
    n = 256.0 * 2 ** int(d["zoom"])
    ys, xs = np.mgrid[0:rej.FH, 0:rej.FW].astype(np.float64)
    lon = rej.lon0 + xs / rej.pxdeg
    ym = np.radians(rej.Y0 - ys / rej.pxdeg)                     # Mercator en radianes (rej usa grados)
    mx = ((lon + 180.0) / 360.0 * n - 256.0 * int(d["x0"])).astype(np.float32)
    my = ((1.0 - ym / math.pi) / 2.0 * n - 256.0 * int(d["y0"])).astype(np.float32)
    return cv2.remap(d["z"].astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def _presa_dem():
    """Máscara (rejilla del DEM, 0/1) de la Presa Calles: inunda desde la semilla hasta tener ≈ PRESA_CELDAS celdas."""
    z, lat_, lon_ = _dem()
    a, b, c, d = PRESA_CAJA
    i0, i1 = np.searchsorted(lat_, c), np.searchsorted(lat_, d)
    j0, j1 = np.searchsorted(lon_, a), np.searchsorted(lon_, b)
    sub = z[i0:i1, j0:j1]
    si, sj = np.searchsorted(lat_, PRESA_SEMILLA[1]) - i0, np.searchsorted(lon_, PRESA_SEMILLA[0]) - j0
    best = None
    for nivel in np.arange(sub[si, sj], sub[si, sj] + 80, 1.0):
        n, lab = cv2.connectedComponents((sub <= nivel).astype(np.uint8), connectivity=4)
        comp = lab == lab[si, sj]
        if comp.sum() >= PRESA_CELDAS:
            best = comp
            break
        best = comp
    m = np.zeros(z.shape, np.float32)
    m[i0:i1, j0:j1] = best
    return m


def _valle_dem(rej):
    """Fondos de valle (0/255): poca altura sobre el fondo local y poca pendiente, con bordes suaves."""
    e = cv2.GaussianBlur(_alt_fina(rej), (0, 0), 2.0)
    r = 25
    fondo = cv2.GaussianBlur(cv2.erode(e, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))), (0, 0), 8)
    px_m = 111320.0 * math.cos(math.radians(22.0)) / rej.pxdeg
    pend = np.hypot(cv2.Sobel(e, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(e, cv2.CV_32F, 0, 1, ksize=3)) / 8.0 / px_m
    v = ((e - fondo) < VALLE_REL) & (pend < VALLE_PEND)
    v = cv2.morphologyEx(v.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    v = cv2.morphologyEx(v, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return ((cv2.GaussianBlur(v.astype(np.float32), (0, 0), 3.0)) > 127).astype(np.uint8) * 255


def _rios_dem():
    """Red de ríos a partir del relieve: relleno de depresiones (priority-flood), D8 y acumulación de flujo.
    Devuelve [(puntos lon/lat, peso)]; el peso (6,9..9,6) crece con el log del área que drena."""
    import heapq
    z, lat_, lon_ = _dem()
    ny, nx = z.shape
    f = z.astype(np.float64).copy()
    hecho = np.zeros((ny, nx), bool)
    heap = []
    for i in range(ny):
        for j in (0, nx - 1):
            heap.append((f[i, j], i, j))
            hecho[i, j] = True
    for j in range(1, nx - 1):
        for i in (0, ny - 1):
            heap.append((f[i, j], i, j))
            hecho[i, j] = True
    heapq.heapify(heap)
    vec = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while heap:
        e, i, j = heapq.heappop(heap)
        for di, dj in vec:
            a, b = i + di, j + dj
            if 0 <= a < ny and 0 <= b < nx and not hecho[a, b]:
                hecho[a, b] = True
                if f[a, b] <= e:
                    f[a, b] = e + 1e-3
                heapq.heappush(heap, (f[a, b], a, b))
    cx = math.cos(math.radians(float(lat_.mean())))
    P = np.pad(f, 1, mode="edge")
    best = np.zeros((ny, nx))
    dirn = np.full((ny, nx), -1, np.int64)
    for k, (di, dj) in enumerate(vec):
        dist = math.hypot(di, dj * cx)
        s = (f - P[1 + di:1 + di + ny, 1 + dj:1 + dj + nx]) / dist
        m = s > best
        best[m] = s[m]
        dirn[m] = k
    ii, jj = np.mgrid[0:ny, 0:nx]
    off_i = np.array([v[0] for v in vec])
    off_j = np.array([v[1] for v in vec])
    di_ = np.where(dirn >= 0, off_i[np.maximum(dirn, 0)], 0)
    dj_ = np.where(dirn >= 0, off_j[np.maximum(dirn, 0)], 0)
    abajo = np.where(dirn >= 0, (ii + di_) * nx + (jj + dj_), -1).ravel()
    borde = np.zeros((ny, nx), bool)
    borde[0, :] = borde[-1, :] = borde[:, 0] = borde[:, -1] = True
    abajo[borde.ravel()] = -1
    # cuencas cerradas (llanos de Ojuelos, altiplano potosino): una depresión rellenada más de RIO_SUMIDERO m es un sumidero; si no,
    # el relleno inventa ríos rectos que cruzan los llanos hasta el borde
    n, lab, st, _ = cv2.connectedComponentsWithStats(((f - z) > 1.0).astype(np.uint8), connectivity=8)
    hondo = np.zeros(n)
    np.maximum.at(hondo, lab.ravel(), (f - z).ravel())
    grande = (st[:, cv2.CC_STAT_AREA] >= RIO_SUM_AREA) & (hondo >= RIO_SUMIDERO)
    grande[0] = False
    sumidero = grande[lab].ravel()
    abajo[sumidero] = -1
    orden = np.argsort(-f.ravel(), kind="stable")
    acc = np.ones(ny * nx)
    for k in orden:
        d = abajo[k]
        if d >= 0:
            acc[d] += acc[k]
    canal = (acc >= RIO_A0) & ~sumidero
    arriba = np.zeros(ny * nx, np.int32)
    src = np.nonzero(canal & (abajo >= 0))[0]
    np.add.at(arriba, abajo[src][canal[abajo[src]]], 1)
    cabezas = np.nonzero(canal & (arriba == 0))[0]
    visto = np.zeros(ny * nx, bool)
    out = []

    def peso(a):
        return np.clip(6.9 + 1.4 * np.log10(a / RIO_A0), 6.9, 9.6)

    for h in cabezas[np.argsort(-acc[cabezas])]:
        cam = []
        k = h
        while k >= 0 and canal[k]:
            cam.append(k)
            if visto[k]:
                break
            visto[k] = True
            k = abajo[k]
        if len(cam) < 3:
            continue
        cam = np.array(cam)
        lon = lon_[cam % nx]
        lat = lat_[cam // nx]
        L = np.stack([lon, lat], 1)
        if len(L) > 5:                                   # suaviza el zigzag del D8 (extremos fijos: siguen unidos al río mayor)
            K = np.ones(5) / 5
            Ls = L.copy()
            Ls[2:-2, 0] = np.convolve(L[:, 0], K, "valid")
            Ls[2:-2, 1] = np.convolve(L[:, 1], K, "valid")
            L = Ls
        pk = np.round(peso(acc[cam]) * 4) / 4
        a = 0
        for b in range(1, len(L) + 1):
            if b == len(L) or pk[b] != pk[a]:
                seg = L[a:min(b + 1, len(L))]
                if len(seg) >= 2:
                    out.append((seg, float(pk[a])))
                a = b
    return out


def _construir(rej):
    """Calcula todos los campos de la rejilla de Aguascalientes (se hace una vez y se guarda en datos/campos_mx.npz)."""
    global _PAISES, _RIOS
    land = json.load(open(F_LAND, encoding="utf-8"))
    _PAISES = json.load(open(F_PAISES, encoding="utf-8"))
    _RIOS = json.load(open(F_RIOS, encoding="utf-8"))
    tierra0 = _mask_geoms(rej, [f["geometry"] for f in land["features"]])
    presa = (cv2.GaussianBlur(_a_rejilla(rej, _presa_dem()), (0, 0), 1.5) > 0.5).astype(np.uint8) * 255
    tierra = cv2.bitwise_and(tierra0, cv2.bitwise_not(presa))
    M = {"tierra": tierra, "presa_calles": presa}

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
    ags = edos("Aguascalientes")
    M["aguascalientes"] = ags
    M["mexico_mod"] = mx
    for n in ESTADOS[1:]:
        M["edo_" + _clave(n)] = edos(n)
    M["resto_mx"] = menos(mx, edos(*ESTADOS))
    M["valle"] = cv2.bitwise_and(U_(P(VALLE_VERDE), P(VALLE_CALVILLO)), _valle_dem(rej))
    M["metro"] = P(METRO)
    for k, pol in (("guachichiles", GUACHICHILES), ("guamares", GUAMARES), ("zacatecos", ZACATECOS), ("caxcanes", CAXCANES),
                   ("tecuexes", TECUEXES), ("insurgentes", INSURGENTES)):
        M[k] = P(pol)
    M["chichimecas"] = U_(M["guachichiles"], M["guamares"], M["zacatecos"], M["caxcanes"], M["tecuexes"])
    ng = U_(ags, edos("Zacatecas", "Jalisco"))
    M["nueva_galicia"] = ng
    M["nueva_espana"] = menos(mx, ng)
    M["zacatecas_dep"] = U_(ags, edos("Zacatecas"))           # 1835 y 1848-1857: Aguascalientes como parte de Zacatecas
    M["territorio"] = ags                                       # alias para la separación de 1835 (mismo contorno)
    M["edo_aguascalientes"] = ags                               # alias con el nombre que usaba el kit de Jalisco
    campos = {k: _i16(_sdf(v)) for k, v in M.items()}
    aux = _relieve(rej, tierra)
    rios = _rios(rej)
    return campos, {}, aux, rios


def _relieve(rej, tierra):
    """(FH, FW, 3): luz del sombreado (-1..1), altitud 0..1 (tierra) y profundidad 0..1 (agua), del relieve Terrarium z10."""
    e = _alt_fina(rej)
    es = cv2.GaussianBlur(e, (0, 0), 1.0)
    gx = cv2.Sobel(es, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(es, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    ys = np.arange(rej.FH, dtype=np.float32)
    _, lat = rej.inv(np.zeros_like(ys), ys)
    px_m = (111320.0 * np.cos(np.radians(lat)) / rej.pxdeg).astype(np.float32)[:, None]
    k = 9.0 / px_m
    luz = np.clip(k * (gx * 0.70 + gy * 0.70), -1.0, 1.0)
    luz = np.where(tierra > 127, luz, 0.0).astype(np.float32)
    alt01 = np.clip((e - ALT_BASE) / ALT_RANGO, 0, 1)
    prof = np.where(tierra > 127, 0.0, 0.35).astype(np.float32)        # las presas: agua clara, poco honda
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
    out += _rios_dem()
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

    def __init__(self, lon=-102.30, lat=21.95, z=1.8, rot=0.0):
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
