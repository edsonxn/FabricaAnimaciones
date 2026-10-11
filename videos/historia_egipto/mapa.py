# -*- coding: utf-8 -*-
"""Mapa pintado a guache para «La historia de Egipto en 5 minutos».

Campos de distancia con signo (SDF, negativo = dentro) sobre una rejilla lon/lat («campo»).
Cada cuadro se proyecta a pantalla con la cámara (`Cam`) y se pinta con pincel de guache
y textura de papel antiguo (papiro).
"""
import json
import math
import os

import cv2
import numpy as np

import boceto as B
from motor import H, W, clamp01, lerp, prog

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS_ROMA = os.path.join(AQUI, "..", "historia_roma", "datos")
DATOS_MEX = os.path.join(AQUI, "..", "independencia_mx", "datos")
DATOS_MOCT = os.path.join(AQUI, "..", "tesoro_moctezuma", "datos")

# ------------------------------------------------------------------ proyección rectangular
# Coordenadas que encuadran el valle del Nilo, el Delta, el Sinaí, el Mar Rojo y el Mediterráneo
LON0, LON1, LAT0, LAT1 = 21.0, 40.0, 39.0, 17.0
PXLAT = 40.0
KX = math.cos(math.radians(27.5))
FW = int((LON1 - LON0) * KX * PXLAT)
FH = int((LAT0 - LAT1) * PXLAT)


def proj(lon, lat):
    """lon/lat -> píxeles del campo (admite escalares o arreglos)."""
    return (np.asarray(lon, float) - LON0) * KX * PXLAT, (LAT0 - np.asarray(lat, float)) * PXLAT


def proj_pts(P):
    P = np.asarray(P, float)
    x, y = proj(P[:, 0], P[:, 1])
    return np.stack([x, y], 1)


# ------------------------------------------------------------------ paleta de guache egipcia
MAR = (182, 214, 222)          # Mar Mediterráneo y Mar Rojo en acuarela turquesa suave
MAR_CL = (204, 230, 234)
TIERRA = (234, 218, 185)       # Desierto líbico y arábigo (arena dorada de guache)
TIERRA_OSC = (212, 192, 155)
NILO_VERDE = (112, 168, 108)   # La franja fértil del Nilo (Kemet / la Tierra Negra)
NILO_AGUA = (118, 172, 215)    # El cauce azul del río Nilo

COL = {
    "predinastico": (205, 150, 95),
    "antiguo": (232, 184, 62),      # Oro de las pirámides
    "medio": (98, 162, 142),        # Turquesa
    "hicsos": (188, 96, 78),        # Terracota invasora
    "nuevo": (196, 64, 52),         # Rojo imperial guerrero
    "amarna": (236, 198, 68),       # Oro de Atón
    "ramses": (185, 52, 48),
    "tardio": (148, 112, 152),
    "ptolomeo": (68, 128, 178),     # Azul alejandrino
    "romano": (178, 48, 48),        # Púrpura romana
    "islam": (68, 148, 108),        # Verde islámico
    "mameluco": (196, 132, 52),
    "moderno": (58, 112, 172),
}

# ------------------------------------------------------------------ geometrías de épocas y regiones (lon, lat)
# El Delta triangular de Egipto (siguiendo la costa mediterránea)
POLI_DELTA = [
    (31.24, 29.95),  # Vértice de Menfis / Saqqara / El Cairo
    (29.75, 31.15),  # Alejandría / oeste
    (30.15, 31.35),
    (30.55, 31.52),  # Desembocadura de Rosetta
    (31.00, 31.60),  # Costa norte central del Delta
    (31.45, 31.60),
    (31.85, 31.55),  # Desembocadura de Damietta
    (32.35, 31.25),  # Pelusio / Port Said
    (31.24, 29.95),
]


# Imperio del Reino Nuevo (llega hasta Siria/Éufrates y Nubia)
POLI_REINO_NUEVO = [
    (28.5, 19.5), (33.5, 19.5), (35.5, 23.0), (36.0, 28.0), (37.5, 33.5), (38.0, 36.5),
    (35.5, 36.5), (33.5, 32.5), (31.5, 31.6), (29.5, 31.5), (28.5, 29.0), (28.5, 19.5)
]

# Imperio Ptolemaico (Egipto + Cirenaica + Chipre + sur del Levante)
POLI_PTOLEMAICO = [
    (24.0, 32.5), (35.0, 33.5), (36.0, 31.0), (34.0, 27.0), (33.5, 22.0), (28.0, 22.0), (24.0, 29.0)
]

# ------------------------------------------------------------------ ciudades y sitios históricos (lon, lat)
CIUDADES = {
    "menfis": (31.25, 29.85),
    "guiza": (31.13, 29.98),
    "el_cairo": (31.24, 30.05),
    "saqqara": (31.22, 29.87),
    "tebas": (32.64, 25.68),
    "karnak": (32.66, 25.72),
    "amarna": (30.90, 27.64),
    "asuan": (32.89, 24.09),
    "abu_simbel": (31.62, 22.34),
    "alejandria": (29.92, 31.20),
    "rosetta": (30.42, 31.40),
    "damietta": (31.81, 31.42),
    "suez": (32.55, 29.97),
    "sinai": (33.80, 29.50),
    "kadesh": (36.52, 34.56),
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
NILO_LINEAS = []


def cargar():
    global _TIERRA_M, NILO_LINEAS
    if _TIERRA_M is not None:
        return

    # 1. Cargar máscara de tierra continental
    land_file = os.path.join(DATOS_MOCT, "ne_50m_land.json")
    if not os.path.exists(land_file):
        land_file = os.path.join(DATOS_ROMA, "ne_50m_land.json")
    land = json.load(open(land_file, encoding="utf-8"))
    _TIERRA_M = _mascara_geom([f["geometry"] for f in land["features"]])
    CAMPOS["tierra"] = _sdf(_TIERRA_M)

    # 2. Cargar el curso del río Nilo desde GeoJSON
    rivers_file = os.path.join(DATOS_MEX, "ne_50m_rivers_lake_centerlines.geojson")
    if os.path.exists(rivers_file):
        rivers = json.load(open(rivers_file, encoding="utf-8"))
        for f in rivers["features"]:
            name = str(f["properties"].get("name", ""))
            if "Nile" in name:
                geom = f["geometry"]
                if geom["type"] == "MultiLineString":
                    for line in geom["coordinates"]:
                        pts = [(pt[0], pt[1]) for pt in line if 21.0 <= pt[1] <= 32.5 and 28.0 <= pt[0] <= 34.0]
                        if pts:
                            NILO_LINEAS.append(pts)

    # Añadir las ramas del Delta (Rosetta y Damietta) desde El Cairo
    cairo_pt = (31.23, 30.10)
    rosetta_pt = (30.42, 31.45)
    damietta_pt = (31.81, 31.52)
    NILO_LINEAS.append([cairo_pt, (30.8, 30.7), rosetta_pt])
    NILO_LINEAS.append([cairo_pt, (31.5, 30.8), damietta_pt])

    # 3. Rasterizar el corredor fértil del Nilo (Kemet)
    m_nilo_corredor = np.zeros((FH, FW), np.uint8)
    # Dibujar la cinta del Nilo con grosor fértil (~18 píxeles de ancho)
    for seg in NILO_LINEAS:
        pts_px = np.rint(proj_pts(seg) * 4).astype(np.int32).reshape(-1, 1, 2)
        cv2.polylines(m_nilo_corredor, [pts_px], False, 255, 18, cv2.LINE_8, 2)

    # Rellenar el Delta fértil
    pts_delta = np.rint(proj_pts(POLI_DELTA) * 4).astype(np.int32).reshape(-1, 1, 2)
    cv2.fillPoly(m_nilo_corredor, [pts_delta], 255, cv2.LINE_8, 2)

    # El corredor fértil solo existe sobre tierra firme
    m_nilo_corredor = cv2.bitwise_and(m_nilo_corredor, _TIERRA_M)
    CAMPOS["nilo_corredor"] = _sdf(m_nilo_corredor)

    # 4. Rasterizar el cauce de agua del Nilo (más fino)
    m_nilo_rio = np.zeros((FH, FW), np.uint8)
    for seg in NILO_LINEAS:
        pts_px = np.rint(proj_pts(seg) * 4).astype(np.int32).reshape(-1, 1, 2)
        cv2.polylines(m_nilo_rio, [pts_px], False, 255, 5, cv2.LINE_8, 2)
    m_nilo_rio = cv2.bitwise_and(m_nilo_rio, _TIERRA_M)
    CAMPOS["nilo_rio"] = _sdf(m_nilo_rio)

    # 5. Geometrías históricas
    # Delta del Nilo
    m_delta = np.zeros((FH, FW), np.uint8)
    pts_delta = np.rint(proj_pts(POLI_DELTA) * 4).astype(np.int32).reshape(-1, 1, 2)
    cv2.fillPoly(m_delta, [pts_delta], 255, cv2.LINE_8, 2)
    m_delta = cv2.bitwise_and(m_delta, _TIERRA_M)
    CAMPOS["delta"] = _sdf(m_delta)

    # Alto Egipto: sigue con fidelidad el curso del río Nilo desde Asuán (~23.8°N) hasta Menfis (~30.15°N)
    m_alto = np.zeros((FH, FW), np.uint8)
    for seg in NILO_LINEAS:
        pts = [p for p in seg if 23.8 <= p[1] <= 30.2]
        if len(pts) > 1:
            pts_px = np.rint(proj_pts(pts) * 4).astype(np.int32).reshape(-1, 1, 2)
            cv2.polylines(m_alto, [pts_px], False, 255, 32, cv2.LINE_8, 2)
            for p in pts:
                px, py = proj(p[0], p[1])
                cv2.circle(m_alto, (int(round(px)), int(round(py))), 16, 255, -1)
    m_alto = cv2.bitwise_and(m_alto, _TIERRA_M)
    CAMPOS["alto_egipto"] = _sdf(m_alto)

    # Egipto unificado = Alto Egipto + Delta del Nilo (cubriendo todo el valle y delta sin desfasarse)
    m_unificado = cv2.bitwise_or(m_alto, m_delta)
    CAMPOS["unificado"] = _sdf(m_unificado)

    # Grandes imperios expansivos
    for k, pts in [("reino_nuevo", POLI_REINO_NUEVO),
                   ("ptolomeo", POLI_PTOLEMAICO)]:
        m = np.zeros((FH, FW), np.uint8)
        cv2.fillPoly(m, [np.rint(proj_pts(pts) * 4).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_8, 2)
        CAMPOS[k] = _sdf(cv2.bitwise_and(m, _TIERRA_M))


# ------------------------------------------------------------------ cámara
class Cam:
    """Cámara sobre el campo de Egipto: centro (lon, lat), zoom (pantalla/campo), giro (rad)."""

    def __init__(self, lon=31.2, lat=27.5, z=1.4, rot=0.0):
        self.fijar(lon, lat, z, rot)

    def fijar(self, lon, lat, z, rot=0.0):
        self.lon, self.lat, self.z, self.rot = lon, lat, z, rot
        cx, cy = proj(lon, lat)
        c, s = math.cos(rot) * z, math.sin(rot) * z
        self.M = np.float32([
            [c, -s, W / 2 - (c * cx - s * cy)],
            [s,  c, H / 2 - (s * cx + c * cy)]
        ])

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
        return cv2.warpAffine(campo, self.M, (W, H), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_CONSTANT, borderValue=relleno)

    @property
    def escala(self):
        return self.z


# ------------------------------------------------------------------ pincel de guache
def _texturas():
    r = np.random.default_rng(42)
    lento = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 12, W // 12)).astype(np.float32), (0, 0), 3),
                       (W, H), interpolation=cv2.INTER_CUBIC)
    trazos = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=16, sigmaY=5.0)
    lento = lento / (lento.std() + 1e-6)
    trazos = trazos / (trazos.std() + 1e-6)
    pincel = (0.020 * lento + 0.007 * trazos).astype(np.float32)
    grano = (B.PAPEL_F / (np.array(B.PAPEL, np.float32) / 255.0)).astype(np.float32)
    ruido = []
    for k in range(3):
        n = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 6, W // 6)).astype(np.float32), (0, 0), 1.6),
                       (W, H), interpolation=cv2.INTER_CUBIC)
        ruido.append((n / (n.std() + 1e-6)).astype(np.float32))
    return pincel, grano, ruido


PINCEL, GRANO, RUIDO = _texturas()

_BASE_MAR = None


def fondo_base():
    """Fondo de mar/agua en acuarela sobre papel de papiro (float32 HxWx3)."""
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
    """Pinta la forma S (negativo dentro) con `color` a guache sobre `img`."""
    r = _roi(S)
    if r is None:
        return
    col = (np.array(color, np.float32) / 255.0)
    _pintar_nb(img, S, RUIDO[fase % 3], PINCEL, GRANO, col, np.float32(alfa), np.float32(sombra),
               np.float32(borde), np.float32(1.5 * ruido), r[0], r[1], r[2], r[3])


def pintar_tierra(img, cam, fase=0):
    """Pinta la tierra firme (desierto) con su orilla de ola de acuarela en el mar."""
    S = cam.proyectar(CAMPOS["tierra"])
    _halo_nb(img, S, np.array(MAR_CL, np.float32) / 255.0, np.float32(0.6), np.float32(34.0), 0, H, 0, W)
    pintar(img, S, TIERRA, 1.0, fase, sombra=0.16)
    return S


def pintar_nilo(img, cam, fase=0):
    """Pinta el corredor fértil verde (Kemet) y el río Nilo azul."""
    if "nilo_corredor" in CAMPOS:
        S_corredor = cam.proyectar(CAMPOS["nilo_corredor"])
        pintar(img, S_corredor, NILO_VERDE, 0.85, fase, sombra=0.12)
    if "nilo_rio" in CAMPOS:
        S_rio = cam.proyectar(CAMPOS["nilo_rio"])
        pintar(img, S_rio, NILO_AGUA, 0.95, fase, sombra=0.08)


def pintar_campo(img, cam, S_campo, color, alfa=1.0, fase=0):
    S = cam.proyectar(S_campo)
    pintar(img, S, color, alfa, fase)
    return S


def mezcla_campos(a, b, k):
    """Interpola dos campos de distancia para transición fluida de fronteras."""
    k = float(min(1.0, max(0.0, k)))
    if k <= 0:
        return CAMPOS[a]
    if k >= 1:
        return CAMPOS[b]
    return cv2.addWeighted(CAMPOS[a], 1 - k, CAMPOS[b], k, 0)
