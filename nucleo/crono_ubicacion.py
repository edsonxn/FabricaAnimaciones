# -*- coding: utf-8 -*-
"""Ubicación en México para los mapas de Cronopapel (22-oct-2026; formato elegido por el usuario entre las muestras de
`videos/_muestras_mapa_cronopapel/`): «que se note en qué parte de México estamos».

Tres piezas, todas alineadas con la cámara del kit (`mapa.Cam`: px de pantalla por grado = z · M.PXDEG_REF, Mercator):
  · APERTURA (muestra 4): México entero en guache (32 estados, relieve ETOPO1, mares, CDMX), el estado protagonista en rojo
    con chincheta y su nombre; la cámara hace zoom hasta el encuadre del estado y el mapa fino del video entra fundido.
  · ESTADO (muestra 6): sobre el mapa fino, fronteras estatales a lápiz, vecinos con velo de color y su nombre DENTRO de su
    territorio, el protagonista teñido y con contorno de tinta, minimapa de México en tarjeta de papel (recuadro rojo = lo que se
    ve), cartela «NOMBRE · dónde queda» y escala en km.
  · REGIÓN (muestra 5): mapa escolar con todos los estados de colores y sus nombres, para cuando la historia cruza varios estados.

Uso en un video del kit (escenas.py ya lo trae; se activa con `UBICACION` en guion.py):
    UB = crono_ubicacion.Ubicacion(M, prota="MX-AGU", subtitulo="centro-norte de México")
    UB.apertura(0.0, 6.5)                     # en la coreografía: México quieto ~2 s y zoom hasta la clave de cámara de t1
    UB.estado(6.5, 14.0)                      # fronteras + vecinos + tarjeta + cartela + escala
    UB.region(80.0, 88.0)                     # mapa de región con todos los estados
  y en escenas.py: `st = UB.camara(t, st)` antes de `M.Cam(*st)` y `img = UB.componer(img, cam, t)` al final de `fondo`.
Datos: `nucleo/datos/mx_ubicacion.npz` (lo crea `python nucleo/crono_ubicacion.py`, de Natural Earth 10 m + ETOPO1).
Doc: docs/estilo_boceto_guache_mapa.md § «Ubicación en México».
"""
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from motor import H, W

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
F_DATOS = os.path.join(AQUI, "datos", "mx_ubicacion.npz")
FUENTE = "C:/Windows/Fonts/Inkfree.ttf"

TINTA = (62, 52, 46)
PAPEL = (240, 230, 208)
ROJO = (206, 74, 50)
MAR = (168, 204, 212)
MAR_HONDO = (124, 168, 194)
MAR_CL = (204, 228, 224)
TXT_EDO = (92, 80, 70)
TXT_MAR = (80, 92, 104)
PALETA = [(232, 206, 150), (196, 214, 164), (234, 190, 166), (198, 208, 224), (220, 204, 226), (238, 224, 176)]

NOMBRES = {
    "MX-AGU": "AGUASCALIENTES", "MX-BCN": "BAJA CALIFORNIA", "MX-BCS": "BAJA CALIFORNIA SUR", "MX-CAM": "CAMPECHE",
    "MX-CHP": "CHIAPAS", "MX-CHH": "CHIHUAHUA", "MX-COA": "COAHUILA", "MX-COL": "COLIMA", "MX-DIF": "CIUDAD DE MÉXICO",
    "MX-DUR": "DURANGO", "MX-GUA": "GUANAJUATO", "MX-GRO": "GUERRERO", "MX-HID": "HIDALGO", "MX-JAL": "JALISCO",
    "MX-MEX": "ESTADO DE MÉXICO", "MX-MIC": "MICHOACÁN", "MX-MOR": "MORELOS", "MX-NAY": "NAYARIT", "MX-NLE": "NUEVO LEÓN",
    "MX-OAX": "OAXACA", "MX-PUE": "PUEBLA", "MX-QUE": "QUERÉTARO", "MX-ROO": "QUINTANA ROO", "MX-SLP": "SAN LUIS POTOSÍ",
    "MX-SIN": "SINALOA", "MX-SON": "SONORA", "MX-TAB": "TABASCO", "MX-TAM": "TAMAULIPAS", "MX-TLA": "TLAXCALA",
    "MX-VER": "VERACRUZ", "MX-YUC": "YUCATÁN", "MX-ZAC": "ZACATECAS",
}
CORTOS = {"MX-DIF": "CDMX", "MX-MEX": "EDO. MÉX.", "MX-TLA": "TLAX.", "MX-MOR": "MOR.", "MX-AGU": "AGS."}
MARES = (("OCÉANO PACÍFICO", -110.5, 16.6), ("GOLFO DE MÉXICO", -91.0, 25.4), ("ESTADOS UNIDOS", -101.5, 31.2))


def c01(c):
    return np.float32(c) / 255.0


def ymerc(lat):
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.asarray(lat, float)) / 2)))


def inv_ymerc(y):
    return np.degrees(2 * np.arctan(np.exp(np.radians(np.asarray(y, float)))) - np.pi / 2)


def suave(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ datos (una vez: python nucleo/crono_ubicacion.py)
def _anillos(g):
    if g["type"] == "Polygon":
        return [g["coordinates"][0]]
    return [p[0] for p in g["coordinates"]]


def preparar(src_edos=None, src_land=None, src_etopo=None, tol=0.0015):
    """Empaqueta estados (simplificados), tierra cercana, relieve ETOPO1 de México, colores y vecindades en un npz."""
    from scipy.io import netcdf_file
    src_edos = src_edos or os.path.join(RAIZ, "videos", "historia_aguascalientes", "datos", "estados_mx.geojson")
    src_land = src_land or os.path.join(RAIZ, "videos", "historia_aguascalientes", "datos", "ne_10m_land.geojson")
    src_etopo = src_etopo or os.path.join(RAIZ, "videos", "historia_mexico", "datos", "relieve_mx_etopo1.nc")

    def simpl(a):
        a = np.asarray(a, np.float64)
        if len(a) < 8:
            return a.astype(np.float32)
        s = cv2.approxPolyDP((a * 1e4).astype(np.int32).reshape(-1, 1, 2), tol * 1e4, True).reshape(-1, 2) / 1e4
        return (s if len(s) >= 3 else a).astype(np.float32)

    codigos, e_pts, e_cortes, e_dueno = [], [], [0], []
    for f in json.load(open(src_edos, encoding="utf8"))["features"]:
        k = f["properties"].get("iso_3166_2")
        if k not in NOMBRES:
            continue
        if k not in codigos:
            codigos.append(k)
        for a in _anillos(f["geometry"]):
            s = simpl(a)
            e_pts.append(s)
            e_cortes.append(e_cortes[-1] + len(s))
            e_dueno.append(codigos.index(k))
    t_pts, t_cortes = [], [0]
    for f in json.load(open(src_land, encoding="utf8"))["features"]:
        for a in _anillos(f["geometry"]):
            a = np.asarray(a, float)
            if a[:, 0].max() > -130 and a[:, 0].min() < -70 and a[:, 1].max() > 5 and a[:, 1].min() < 40:
                a = np.clip(a, [-140, -5], [-60, 60])
                s = simpl(a)
                t_pts.append(s)
                t_cortes.append(t_cortes[-1] + len(s))
    nc = netcdf_file(src_etopo, "r", mmap=False)
    z = nc.variables["altitude"][:].astype(np.float32).copy()
    la = nc.variables["latitude"][:].astype(np.float64).copy()
    lo = nc.variables["longitude"][:].astype(np.float64).copy()
    if la[0] > la[-1]:
        z, la = z[::-1].copy(), la[::-1].copy()
    i0, i1 = np.searchsorted(la, 9.0), np.searchsorted(la, 36.0)
    j0, j1 = np.searchsorted(lo, -124.0), np.searchsorted(lo, -78.0)
    alt = np.clip(z[i0:i1, j0:j1], -32000, 32000).astype(np.int16)
    # vecindades y colores (coloreado voraz: dos vecinos nunca del mismo color)
    paso = 0.02
    rw, rh = int(46 / paso), int(27 / paso)
    ids = np.zeros((rh, rw), np.int32)
    for (a, b), d in zip(zip(e_cortes[:-1], e_cortes[1:]), e_dueno):
        P = np.concatenate(e_pts)[a:b]
        Q = np.stack([(P[:, 0] + 124) / paso, (36 - P[:, 1]) / paso], 1)
        cv2.fillPoly(ids, [np.rint(Q).astype(np.int32)], d + 1)
    n = len(codigos)
    vec = np.zeros((n, n), np.uint8)
    ker = np.ones((5, 5), np.uint8)
    dil = [cv2.dilate((ids == i + 1).astype(np.uint8), ker) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (dil[i] & dil[j]).any():
                vec[i, j] = vec[j, i] = 1
    col = {}
    for i in sorted(range(n), key=lambda i: -int(dil[i].sum())):
        usados = {col[j] for j in col if vec[i, j]}
        col[i] = next((c for c in range(len(PALETA)) if c not in usados), 0)
    np.savez_compressed(F_DATOS, codigos=np.array(codigos), e_pts=np.concatenate(e_pts), e_cortes=np.int32(e_cortes),
                        e_dueno=np.int32(e_dueno), t_pts=np.concatenate(t_pts), t_cortes=np.int32(t_cortes), alt=alt,
                        alt_lat0=la[i0], alt_lon0=lo[j0], alt_paso=float(la[1] - la[0]), vecinos=vec,
                        colores=np.int32([col[i] for i in range(n)]))
    print(f"ok {F_DATOS}: {n} estados, {len(t_cortes) - 1} anillos de tierra, relieve {alt.shape}")


class _Datos:
    def __init__(self):
        if not os.path.exists(F_DATOS):
            preparar()
        d = np.load(F_DATOS)
        self.codigos = [str(c) for c in d["codigos"]]
        P, C = d["e_pts"].astype(np.float64), d["e_cortes"]
        self.edos = {k: [] for k in self.codigos}
        for (a, b), i in zip(zip(C[:-1], C[1:]), d["e_dueno"]):
            self.edos[self.codigos[i]].append(P[a:b])
        self.caja = {k: (min(r[:, 0].min() for r in v), max(r[:, 0].max() for r in v),
                         min(r[:, 1].min() for r in v), max(r[:, 1].max() for r in v)) for k, v in self.edos.items()}
        P, C = d["t_pts"].astype(np.float64), d["t_cortes"]
        self.tierra = [P[a:b] for a, b in zip(C[:-1], C[1:])]
        self.t_caja = [(r[:, 0].min(), r[:, 0].max(), r[:, 1].min(), r[:, 1].max()) for r in self.tierra]
        self.alt = d["alt"].astype(np.float32)
        self.alt_lat0, self.alt_lon0, self.alt_paso = float(d["alt_lat0"]), float(d["alt_lon0"]), float(d["alt_paso"])
        v = d["vecinos"]
        self.vecinos = {k: [self.codigos[j] for j in np.nonzero(v[i])[0]] for i, k in enumerate(self.codigos)}
        self.color = {k: PALETA[int(c)] for k, c in zip(self.codigos, d["colores"])}


_D = None


def datos():
    global _D
    if _D is None:
        _D = _Datos()
    return _D


# ------------------------------------------------------------------ vista Mercator alineada con mapa.Cam
class Vista:
    """(lon, lat) al centro, k px por grado, giro rot (mismo sentido que mapa.Cam)."""

    def __init__(self, lon, lat, k, rot=0.0, w=W, h=H):
        self.lon, self.lat, self.k, self.rot, self.w, self.h = lon, lat, k, rot, w, h
        self.y0 = float(ymerc(lat))
        self.c, self.s = math.cos(rot), math.sin(rot)

    @staticmethod
    def de_cam(cam, pxdeg):
        return Vista(cam.lon, cam.lat, cam.z * pxdeg, cam.rot)

    @staticmethod
    def ajustar(lon0, lon1, lat0, lat1, w=W, h=H, margen=0.04):
        k = min(w * (1 - 2 * margen) / (lon1 - lon0), h * (1 - 2 * margen) / float(ymerc(lat1) - ymerc(lat0)))
        return Vista((lon0 + lon1) / 2, float(inv_ymerc((ymerc(lat0) + ymerc(lat1)) / 2)), k, 0.0, w, h)

    def pts(self, P):
        P = np.asarray(P, float)
        x = (P[:, 0] - self.lon) * self.k
        y = (self.y0 - ymerc(P[:, 1])) * self.k
        return np.stack([self.c * x - self.s * y + self.w / 2, self.s * x + self.c * y + self.h / 2], 1)

    def pt(self, lon, lat):
        return self.pts([[lon, lat]])[0]

    def inv(self, x, y):
        dx, dy = np.asarray(x, float) - self.w / 2, np.asarray(y, float) - self.h / 2
        px, py = self.c * dx + self.s * dy, -self.s * dx + self.c * dy
        return self.lon + px / self.k, inv_ymerc(self.y0 - py / self.k)

    def limites(self):
        lo, la = self.inv(np.float64([0, self.w, self.w, 0]), np.float64([0, 0, self.h, self.h]))
        return lo.min(), lo.max(), la.min(), la.max()


def _ve(caja, lim, m=0.3):
    return not (caja[1] < lim[0] - m or caja[0] > lim[1] + m or caja[3] < lim[2] - m or caja[2] > lim[3] + m)


def _poly(mask, rings, proj, val=255):
    P = [np.rint(proj(r) * 8).astype(np.int32) for r in rings if len(r) > 2]
    if P:
        cv2.fillPoly(mask, P, val, cv2.LINE_AA, 3)
    return mask


def mascaras(v, cuales=None):
    """Máscaras uint8 de pantalla de los estados visibles (o de `cuales`)."""
    D = datos()
    lim = v.limites()
    out = {}
    for k in (cuales or D.codigos):
        if _ve(D.caja[k], lim):
            out[k] = _poly(np.zeros((v.h, v.w), np.uint8), D.edos[k], v.pts)
    return out


_RUIDO = {}


def ruido(h, w, semilla, escalas=((6, .5), (40, .3), (160, .2))):
    key = (h, w, semilla, escalas)
    if key not in _RUIDO:
        rng = np.random.default_rng(semilla)
        out = np.zeros((h, w), np.float32)
        for s, p in escalas:
            r = rng.random((h // s + 2, w // s + 2)).astype(np.float32)
            out += p * cv2.resize(r, (w, h), interpolation=cv2.INTER_CUBIC)
        _RUIDO[key] = out - out.mean()
    return _RUIDO[key]


# ------------------------------------------------------------------ México en guache (apertura, región, minimapa)
def _lonlat(v):
    """lon, lat de cada píxel (separable si la vista no gira: mucho más barato)."""
    if abs(v.rot) < 1e-4:
        lon, _ = v.inv(np.arange(v.w, dtype=np.float64), np.zeros(v.w))
        _, lat = v.inv(np.full(v.h, v.w / 2.0), np.arange(v.h, dtype=np.float64))
        return (np.broadcast_to(lon[None, :].astype(np.float32), (v.h, v.w)),
                np.broadcast_to(lat[:, None].astype(np.float32), (v.h, v.w)))
    xs, ys = np.meshgrid(np.arange(v.w, dtype=np.float64), np.arange(v.h, dtype=np.float64))
    lon, lat = v.inv(xs, ys)
    return lon.astype(np.float32), lat.astype(np.float32)


def pintar_mexico(v, prota=None, suave_=False, relieve=1.0):
    """Mapa de México: mar con profundidad, tierra extranjera apagada, estados de colores (vecinos nunca iguales), relieve,
    fronteras blancas, costa a tinta; `prota` en rojo con contorno grueso. -> (img float HxWx3, máscaras)"""
    D = datos()
    w, h = v.w, v.h
    lon, lat = _lonlat(v)
    mx = np.ascontiguousarray((lon - np.float32(D.alt_lon0)) / np.float32(D.alt_paso))
    my = np.ascontiguousarray((lat - np.float32(D.alt_lat0)) / np.float32(D.alt_paso))
    alt = cv2.remap(D.alt, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=-3000)
    kmpx = 111.32 / v.k
    ex = np.float32((6.0 + 18.0 * min(1.0, kmpx / 3.0)) * relieve / (kmpx * 1000))
    ab = cv2.GaussianBlur(alt, (0, 0), 1.0)
    gx = cv2.Sobel(ab, cv2.CV_32F, 1, 0, ksize=1, scale=0.5) * -ex
    gy = cv2.Sobel(ab, cv2.CV_32F, 0, 1, ksize=1, scale=0.5) * -ex
    sh = (gx * np.float32(-0.6) + gy * np.float32(-0.6) + np.float32(0.53)) / np.sqrt(gx * gx + gy * gy + np.float32(1))
    sh = np.clip(sh * np.float32(1 / 0.53), 0.35, 1.25)
    lim = v.limites()
    tierra = np.zeros((h, w), np.uint8)
    _poly(tierra, [r for r, c in zip(D.tierra, D.t_caja) if _ve(c, lim)], v.pts)
    ms = mascaras(v)
    mexico = np.zeros((h, w), np.uint8)
    for m in ms.values():
        cv2.max(mexico, m, mexico)
    cv2.max(tierra, mexico, tierra)
    prof = np.clip(alt * np.float32(-1 / 4000.0), 0, 1)[..., None]
    img = c01(MAR) + (c01(MAR_HONDO) - c01(MAR)) * prof
    dist = cv2.distanceTransform(255 - tierra, cv2.DIST_L2, 5)
    orilla = np.exp(dist * np.float32(-1 / (6 + 0.004 * w))) * np.float32(0.6)
    img += (c01(MAR_CL) - img) * orilla[..., None]
    ft = tierra.astype(np.float32) * np.float32(1 / 255)
    luz = (np.float32(0.80) + np.float32(0.22) * sh)[..., None]
    img += (c01((222, 214, 196)) * luz - img) * ft[..., None]
    # estados: un color por estado, solo dentro de su recuadro
    luz = (np.float32(0.72) + np.float32(0.32) * sh)[..., None]
    ids = np.zeros((h, w), np.uint8)
    for i, (k, m) in enumerate(ms.items(), 1):
        x0, y0, bw, bh = cv2.boundingRect(m)
        if bw == 0:
            continue
        x1, y1 = x0 + bw, y0 + bh
        c = ROJO if k == prota else D.color[k]
        if suave_ and k != prota:
            c = tuple(int(0.55 * x + 0.45 * q) for x, q in zip(c, PAPEL))
        a = m[y0:y1, x0:x1].astype(np.float32) * np.float32(1 / 255)
        r = img[y0:y1, x0:x1]
        r += (c01(c) * luz[y0:y1, x0:x1] - r) * a[..., None]
        ids[y0:y1, x0:x1][m[y0:y1, x0:x1] > 127] = i
    img *= (np.float32(1) + np.float32(0.10) * ruido(h, w, 7))[..., None]
    borde = cv2.morphologyEx(ids, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    borde = ((borde > 0) & (ids > 0)).astype(np.float32)
    b = np.clip(cv2.GaussianBlur(borde, (0, 0), 0.8) * np.float32(2.2 * 0.75), 0, 0.75)
    img += (c01((250, 246, 236)) - img) * b[..., None]
    costa = cv2.morphologyEx(mexico, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32) * np.float32(0.55 / 255)
    img += (c01(TINTA) - img) * costa[..., None]
    if prota in ms:
        e = cv2.morphologyEx(ms[prota], cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)).astype(np.float32) * np.float32(0.9 / 255)
        img += (c01(TINTA) - img) * e[..., None]
    return np.clip(img, 0, 1, out=img), ms


# ------------------------------------------------------------------ texto a mano, chincheta, rosa, escala
_F = {}


def fuente(px):
    if px not in _F:
        _F[px] = ImageFont.truetype(FUENTE, px)
    return _F[px]


def ancho(txt, px, espaciado=False):
    return fuente(px).getlength(" ".join(txt) if espaciado else txt)


def texto(img, txt, x, y, px, color=TINTA, alfa=0.9, halo=0.75, espaciado=False, centro=True, borde=0):
    """Rótulo a mano con halo de papel. borde > 0: se desvanece si se acerca a menos de `borde` px del canto (nunca cortado)."""
    if alfa <= 0.01:
        return
    t = " ".join(txt) if espaciado else txt
    fu = fuente(px)
    bb = fu.getbbox(t)
    if borde:
        h_, w_ = img.shape[:2]
        x0_ = x - (bb[2] / 2 if centro else 0)
        fuera = max(0.0, borde - x0_, x0_ + bb[2] - (w_ - borde), borde - (y - px * 0.6), (y + px * 0.6) - (h_ - borde))
        alfa *= max(0.0, 1.0 - fuera / 28.0)
        if alfa <= 0.01:
            return
    pad = max(6, px // 5)
    im = Image.new("L", (bb[2] + 2 * pad, int(px * 1.45) + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad, pad), t, font=fu, fill=255, stroke_width=1 if px < 60 else 2, stroke_fill=255)
    m = np.asarray(im, np.float32) / 255
    x0 = int(x - (bb[2] / 2 if centro else 0)) - pad
    y0 = int(y - (bb[1] + bb[3]) * 0.5) - pad
    if halo:
        mh = cv2.GaussianBlur(cv2.dilate(m, np.ones((max(3, px // 7),) * 2, np.uint8)), (0, 0), max(1.5, px / 16))
        _pegar(img, np.clip(mh * 1.4, 0, 1), x0, y0, c01(PAPEL), halo * alfa)
    _pegar(img, m, x0, y0, c01(color), alfa)


def _pegar(img, mm, x0, y0, col, al):
    h, w = img.shape[:2]
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(w, x0 + mm.shape[1]), min(h, y0 + mm.shape[0])
    if xb <= xa or yb <= ya:
        return
    a = mm[ya - y0:yb - y0, xa - x0:xb - x0][..., None] * al
    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - a) + col * a


def sombra_bajo(img, mask, dx=14, dy=18, sigma=12, k=0.38):
    s = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), sigma)
    s = np.roll(np.roll(s, dy, 0), dx, 1)
    img *= (1 - k * s)[..., None]


def _roi(img, x0, y0, x1, y1):
    """Recorte (vista, desplazamiento) de img a un recuadro dentro de la pantalla, o None."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(w, int(x1)), min(h, int(y1))
    if x1 <= x0 or y1 <= y0:
        return None
    return img[y0:y1, x0:x1], x0, y0


def pin(img, x, y, r=22, alfa=1.0, color=ROJO):
    """Chincheta roja con sombra y brillo (dibujada solo en su recuadro)."""
    if alfa <= 0.01:
        return
    q = _roi(img, x - 2 * r, y - 4 * r, x + 2 * r + 20, y + r + 20)
    if q is None:
        return
    sub, ox, oy = q
    x, y = x - ox, y - oy
    m = np.zeros(sub.shape[:2], np.uint8)
    cv2.circle(m, (int(x), int(y - 2.2 * r)), int(r), 255, -1, cv2.LINE_AA)
    cv2.fillConvexPoly(m, np.int32([[x - r * 0.82, y - 1.75 * r], [x + r * 0.82, y - 1.75 * r], [x, y]]), 255, cv2.LINE_AA)
    mf = m.astype(np.float32) / 255 * alfa
    sombra_bajo(sub, mf, 6, 7, 5, 0.45)
    sub[:] = sub * (1 - mf[..., None]) + c01(color) * mf[..., None]
    b = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)[..., None] / 255 * alfa
    sub[:] = sub * (1 - 0.8 * b) + c01(TINTA) * 0.8 * b
    m2 = np.zeros(sub.shape[:2], np.uint8)
    cv2.circle(m2, (int(x), int(y - 2.2 * r)), max(3, int(r) // 3), 255, -1, cv2.LINE_AA)
    a = m2.astype(np.float32)[..., None] / 255 * alfa
    sub[:] = sub * (1 - a) + c01((250, 242, 230)) * a


def punto(img, x, y, r=9, color=TINTA, alfa=1.0):
    """Punto de ciudad que se funde con su nombre."""
    anillo(img, x, y, r / 2, int(r), color, alfa)


def anillo(img, x, y, r, grosor=4, color=ROJO, alfa=0.85):
    if alfa <= 0.01 or r <= 1:
        return
    q = _roi(img, x - r - grosor - 2, y - r - grosor - 2, x + r + grosor + 3, y + r + grosor + 3)
    if q is None:
        return
    sub, ox, oy = q
    m = np.zeros(sub.shape[:2], np.uint8)
    cv2.circle(m, (int(x - ox), int(y - oy)), int(r), 255, grosor, cv2.LINE_AA)
    a = m.astype(np.float32)[..., None] / 255 * alfa
    sub[:] = sub * (1 - a) + c01(color) * a


def linea(img, p0, p1, grosor=3, color=TINTA, alfa=1.0):
    if alfa <= 0.01:
        return
    q = _roi(img, min(p0[0], p1[0]) - grosor - 2, min(p0[1], p1[1]) - grosor - 2,
             max(p0[0], p1[0]) + grosor + 3, max(p0[1], p1[1]) + grosor + 3)
    if q is None:
        return
    sub, ox, oy = q
    m = np.zeros(sub.shape[:2], np.uint8)
    cv2.line(m, (int(p0[0] - ox), int(p0[1] - oy)), (int(p1[0] - ox), int(p1[1] - oy)), 255, grosor, cv2.LINE_AA)
    a = m.astype(np.float32)[..., None] / 255 * alfa
    sub[:] = sub * (1 - a) + c01(color) * a


def rosa(img, x, y, r=46, alfa=1.0):
    if alfa <= 0.01:
        return
    capa = img.copy()
    P = np.float32([[0, -1], [0.22, 0], [0, 1], [-0.22, 0]]) * r
    Q = np.float32([[-1, 0], [0, 0.22], [1, 0], [0, -0.22]]) * r * 0.6
    for poly, c in ((Q, (150, 132, 110)), (P, TINTA)):
        cv2.fillConvexPoly(capa, np.int32(poly + [x, y]), c01(c).tolist(), cv2.LINE_AA)
    cv2.fillConvexPoly(capa, np.int32(np.float32([[0, -1], [0.22, 0], [0, 0]]) * r + [x, y]), c01(ROJO).tolist(), cv2.LINE_AA)
    cv2.circle(capa, (int(x), int(y)), int(r * 1.05), c01(TINTA).tolist(), 2, cv2.LINE_AA)
    img[:] = img * (1 - alfa) + capa * alfa
    texto(img, "N", x, y - r - 22, 30, halo=0.6, alfa=alfa)


def escala(img, v, x, y, km=None, alfa=1.0):
    """Barra de escala de papel y tinta; elige 10/25/50/100/250/500 km para que mida ~250-450 px."""
    kmpx = 111.32 * math.cos(math.radians(v.lat)) / v.k
    if km is None:
        km = min((10, 25, 50, 100, 250, 500), key=lambda c: abs(c / kmpx - 340))
    L = int(km / kmpx)
    capa = img.copy()
    for i in range(4):
        c = TINTA if i % 2 == 0 else (250, 246, 236)
        cv2.rectangle(capa, (x + i * L // 4, y), (x + (i + 1) * L // 4, y + 10), c01(c).tolist(), -1)
    cv2.rectangle(capa, (x, y), (x + L, y + 10), c01(TINTA).tolist(), 2, cv2.LINE_AA)
    img[:] = img * (1 - alfa) + capa * alfa
    texto(img, f"{km} km", x + L // 2, y + 34, 26, halo=0.5, alfa=alfa)


# ------------------------------------------------------------------ capa ESTADO sobre el mapa fino
def lavar(img, mask, k=0.30, gris=0.35):
    a = (mask.astype(np.float32) / 255)[..., None] * k
    g = img.mean(2, keepdims=True)
    des = (img * (1 - gris) + g * gris) * 0.55 + c01(PAPEL) * 0.45
    img[:] = img * (1 - a) + des * a


def tintes(img, ms, prota, alfa=0.3):
    """Velo de color propio en cada estado vecino (multiplica; solo dentro del recuadro de cada uno)."""
    D = datos()
    for k, m in ms.items():
        if k == prota:
            continue
        x0, y0, bw, bh = cv2.boundingRect(m)
        if bw == 0:
            continue
        a = m[y0:y0 + bh, x0:x0 + bw].astype(np.float32) * np.float32(alfa / 255)
        r = img[y0:y0 + bh, x0:x0 + bw]
        r *= np.float32(1) + (c01(D.color[k]) * np.float32(1.25) - np.float32(1)) * a[..., None]


def tenir(img, m, color=(222, 120, 84), alfa=0.5):
    """Tiñe el estado protagonista conservando el relieve (guache transparente)."""
    a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 1.5)[..., None] * alfa
    lum = img.mean(2, keepdims=True)
    img[:] = img * (1 - a) + c01(color) * (0.45 + 0.75 * lum) * a


def fronteras_lapiz(img, ms, prota=None, grosor=3, alfa=0.85, prota_grosor=6, semilla=11):
    h, w = img.shape[:2]
    ids = np.zeros((h, w), np.int32)
    for i, m in enumerate(ms.values(), 1):
        ids[m > 127] = i
    borde = (cv2.morphologyEx(ids.astype(np.float32), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8)
    if grosor > 1:
        borde = cv2.dilate(borde, np.ones((grosor, grosor), np.uint8))
    halo = cv2.GaussianBlur(cv2.dilate(borde, np.ones((7, 7), np.uint8)).astype(np.float32), (0, 0), 2.5)[..., None] * alfa
    img[:] = img * (1 - 0.55 * halo) + c01((250, 245, 232)) * 0.55 * halo
    grano = np.clip(0.7 + 2.0 * ruido(h, w, semilla, ((2, .6), (9, .4))), 0.25, 1.0)
    a = (cv2.GaussianBlur(borde.astype(np.float32), (0, 0), 0.7) * grano * alfa)[..., None]
    img[:] = img * (1 - a) + c01(TINTA) * a
    if prota in ms:
        e = cv2.morphologyEx(ms[prota], cv2.MORPH_GRADIENT, np.ones((prota_grosor, prota_grosor), np.uint8)).astype(np.float32) / 255
        hb = cv2.GaussianBlur(cv2.dilate(e, np.ones((9, 9), np.uint8)), (0, 0), 3)[..., None] * alfa
        img[:] = img * (1 - 0.7 * hb) + c01((252, 248, 238)) * 0.7 * hb
        a = (cv2.GaussianBlur(e, (0, 0), 0.8) * np.clip(0.85 + grano * 0.3, 0, 1) * 0.92 * alfa)[..., None]
        img[:] = img * (1 - a) + c01(TINTA) * a


def caja(x0, y0, x1, y1, w=W, h=H):
    m = np.zeros((h, w), np.uint8)
    cv2.rectangle(m, (int(x0), int(y0)), (int(x1), int(y1)), 255, -1)
    return m


def cabe(mask, w_, h_, excluir=None, margen=40, cerca=None):
    """Centro donde un rótulo w_×h_ cabe ENTERO en la máscara (fuera de lo excluido); el más holgado, o el más cercano a `cerca`."""
    s = 4
    m = (mask > 127).astype(np.uint8)
    if excluir is not None:
        m[excluir > 0] = 0
    m[:margen], m[-margen:], m[:, :margen], m[:, -margen:] = 0, 0, 0, 0
    m = cv2.resize(m, (m.shape[1] // s, m.shape[0] // s), interpolation=cv2.INTER_NEAREST)
    e = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_RECT, (max(1, int(w_ / s)), max(1, int(h_ / s)))))
    if not e.any():
        return None
    if cerca is not None:
        ys, xs = np.nonzero(e)
        i = int(np.argmin((xs * s - cerca[0]) ** 2 + (ys * s - cerca[1]) ** 2))
        return xs[i] * s + s // 2, ys[i] * s + s // 2
    d = cv2.distanceTransform(e, cv2.DIST_L2, 3)
    y, x = np.unravel_index(int(d.argmax()), d.shape)
    return x * s + s // 2, y * s + s // 2


def colocar_rotulos(v, ms, cuales, px, excluir):
    """Coloca nombres de estado DENTRO de su territorio visible (más chico si no cabe; si tampoco, se omite).
    -> [(nombre, lon, lat, px, espaciado)] en coordenadas geográficas (así se mueven con el mapa sin saltar)."""
    out = []
    ex = excluir.copy()
    for k in cuales:
        if k not in ms:
            continue
        n = NOMBRES[k]
        for p, esp, t in ((px, True, n), (int(px * 0.8), True, n), (int(px * 0.8), False, n), (int(px * 0.65), False, n),
                          (int(px * 0.65), False, CORTOS.get(k, n))):
            w_, h_ = ancho(t, p, esp) + 30, p * 1.1
            q = cabe(ms[k], w_, h_, ex)
            if q:
                lo, la = v.inv(q[0], q[1])
                out.append((t, float(lo), float(la), p, esp))
                ex = np.maximum(ex, caja(q[0] - w_ / 2, q[1] - h_, q[0] + w_ / 2, q[1] + h_, v.w, v.h))
                break
    return out


def cartela(img, linea1, linea2, x, y, alfa=1.0):
    if alfa <= 0.01:
        return
    w_ = int(max(ancho(linea1, 58), ancho(linea2, 30))) + 70
    h_ = 128
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.fillConvexPoly(m, np.int32([[x, y + 4], [x + w_, y], [x + w_ - 6, y + h_], [x + 5, y + h_ + 3]]), 255, cv2.LINE_AA)
    mf = m.astype(np.float32) / 255 * alfa
    sombra_bajo(img, mf, 8, 10, 7, 0.4)
    papel = c01((248, 241, 224)) * (1 + 0.05 * ruido(img.shape[0], img.shape[1], 21))[..., None]
    img[:] = img * (1 - mf[..., None]) + papel * mf[..., None]
    linea(img, (x + 22, y + 74), (x + w_ - 26, y + 72), 3, ROJO, alfa)
    texto(img, linea1, x + 32, y + 42, 58, halo=0, centro=False, alfa=alfa)
    texto(img, linea2, x + 34, y + 100, 30, color=(110, 92, 78), halo=0, centro=False, alfa=alfa)


# ------------------------------------------------------------------ tarjeta con el minimapa
class Tarjeta:
    """Minimapa de México en papel con cinta; el recuadro rojo es lo que ve la cámara."""

    def __init__(self, prota, w=420, h=300, titulo="MÉXICO"):
        self.w, self.h, self.prota = w, h, prota
        pw, ph = w - 36, h - 74
        self.v = Vista.ajustar(-117.5, -86.5, 14.3, 32.8, pw, ph, 0.02)
        mapa, ms = pintar_mexico(self.v, prota=prota, suave_=True)
        card = np.ones((h, w, 3), np.float32) * c01((246, 239, 222))
        card *= (1 + 0.05 * ruido(h, w, 3))[..., None]
        card[18:18 + ph, 18:18 + pw] = mapa
        cv2.rectangle(card, (18, 18), (18 + pw - 1, 18 + ph - 1), c01(TINTA).tolist(), 2, cv2.LINE_AA)
        texto(card, titulo, w // 2, h - 30, 34, halo=0, espaciado=True)
        self.card = card
        cy, cx = np.argwhere(ms[prota] > 128).mean(0)
        self.cx, self.cy = cx + 18, cy + 18

    def pegar(self, img, x, y, vista_cam=None, ang=-3.0, alfa=1.0):
        if alfa <= 0.01:
            return
        card = self.card.copy()
        if vista_cam is not None:
            lo, la = vista_cam.inv(np.float64([0, W, W, 0]), np.float64([0, 0, H, H]))
            P = np.rint(self.v.pts(np.stack([lo, la], 1)) + 18).astype(np.int32)
            if (P.max(0) - P.min(0)).max() < 14:          # recuadro diminuto: un anillo que lo señale
                anillo(card, self.cx, self.cy, 20, 3)
            cv2.polylines(card, [P], True, c01((250, 246, 236)).tolist(), 5, cv2.LINE_AA)
            cv2.polylines(card, [P], True, c01(ROJO).tolist(), 2, cv2.LINE_AA)
        h, w = card.shape[:2]
        d = int(math.hypot(w, h)) + 20
        big = np.zeros((d, d, 3), np.float32)
        msk = np.zeros((d, d), np.float32)
        ox, oy = (d - w) // 2, (d - h) // 2
        big[oy:oy + h, ox:ox + w] = card
        msk[oy:oy + h, ox:ox + w] = 1
        R = cv2.getRotationMatrix2D((d / 2, d / 2), ang, 1.0)
        big = cv2.warpAffine(big, R, (d, d), flags=cv2.INTER_LINEAR)
        msk = cv2.warpAffine(msk, R, (d, d), flags=cv2.INTER_LINEAR) * alfa
        x0, y0 = int(x - d / 2), int(y - d / 2)
        Hh, Ww = img.shape[:2]
        full = np.zeros((Hh, Ww), np.float32)
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(Ww, x0 + d), min(Hh, y0 + d)
        full[ya:yb, xa:xb] = msk[ya - y0:yb - y0, xa - x0:xb - x0]
        sombra_bajo(img, full, 10, 14, 10, 0.42)
        a = full[ya:yb, xa:xb, None]
        img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - a) + big[ya - y0:yb - y0, xa - x0:xb - x0] * a
        for sx in (-1, 1):
            t = cv2.boxPoints(((x + sx * w * 0.36, y - h * 0.5 + sx * 4), (110, 32), -sx * 28 + ang))
            m = np.zeros((Hh, Ww), np.uint8)
            cv2.fillConvexPoly(m, np.int32(t), 255, cv2.LINE_AA)
            a = m.astype(np.float32)[..., None] / 255 * 0.62 * alfa
            img[:] = img * (1 - a) + c01((236, 226, 186)) * a


# ------------------------------------------------------------------ línea de tiempo: apertura, estado, región
class Ubicacion:
    """Une las tres piezas con la cámara y el fondo de un video del kit.
    `M` = el módulo mapa.py del video (para PXDEG_REF y la caja de la rejilla activa)."""

    def __init__(self, M, prota, subtitulo="", nombre=None, vecinos=None, vertical=None):
        self.M, self.prota = M, prota
        self.nombre = nombre or NOMBRES[prota]
        self.subtitulo = subtitulo
        self.vecinos = vecinos if vecinos is not None else datos().vecinos[prota]
        self.vertical = (H > W) if vertical is None else vertical
        self.ap, self.ed, self.rg = [], [], []
        self._tarjeta = None
        self._rot = {}
        self._cache = None
        self.cam_fn = None        # f(t) -> (lon, lat, z, rot) de la coreografía (escenas.py lo pone: CAM.estado)

    # ---- registro (desde la coreografía)
    def apertura(self, t0, t1, quieto=2.0, fundido=0.8, estado=6.0, **k_estado):
        """México entero de t0 a t0+quieto; zoom hasta la cámara de la coreografía en t1 (lo previo a t0 se funde desde negro).
        Al llegar sigue la capa ESTADO `estado` s (0 = sin ella); k_estado = opciones de estado() (tarjeta=False...)."""
        self.ap.append(dict(t0=t0, t1=t1, quieto=quieto, fundido=fundido))
        if estado:
            self.estado(t1 - 0.5, t1 + estado, **k_estado)

    def estado(self, t0, t1, fronteras=True, tarjeta=True, cartela=True, escala=True, vecinos=True, fundido=0.6):
        self.ed.append(dict(t0=t0, t1=t1, fronteras=fronteras, tarjeta=tarjeta, cartela=cartela, escala=escala,
                            vecinos=vecinos, fundido=fundido))

    def region(self, t0, t1, fundido=0.7, extra=()):
        """Mapa escolar de estados sobre la cámara actual (convén aflojar el zoom a z ≈ 0,3-0,45 para ver 6-10 estados).
        extra = [(texto, lon, lat)] puntos con nombre (ciudades)."""
        self.rg.append(dict(t0=t0, t1=t1, fundido=fundido, extra=list(extra)))

    def cajas_ocupadas(self):
        """(t0, t1, caja, etiqueta) de la cartela y la tarjeta, para el control de choques (_qa_choques.py)."""
        out = []
        for e in self.ed:
            if e["cartela"]:
                out.append((e["t0"], e["t1"], self._caja_cartela(), "ubicación: cartela"))
            if e["tarjeta"]:
                x, y, w, h = self._pos_tarjeta()
                out.append((e["t0"], e["t1"], (x - w / 2, y - h / 2, x + w / 2, y + h / 2), "ubicación: minimapa"))
        return out

    # ---- geometría de pantalla (16:9 y vertical; el año va arriba a la izquierda y los sellos arriba a la derecha)
    def _pos_tarjeta(self):
        return (310, 1450, 460, 330) if self.vertical else (290, 860, 420, 300)

    def _pos_cartela(self):
        return (50, 300) if self.vertical else (40, 118)

    def _caja_cartela(self):
        x, y = self._pos_cartela()
        return (x, y, x + max(ancho(self.nombre, 58), ancho(self.subtitulo, 30)) + 80, y + 140)

    def _pos_escala(self):
        return (640, 1520) if self.vertical else (560, 1010)

    # ---- pesos en el tiempo
    @staticmethod
    def _ventana(t, e, fi=None, fo=None):
        fi = e.get("fundido", 0.6) if fi is None else fi
        fo = fi if fo is None else fo
        if t < e["t0"] or t > e["t1"]:
            return 0.0
        return min(suave((t - e["t0"]) / max(1e-3, fi)), suave((e["t1"] - t) / max(1e-3, fo)))

    def _ap(self, t):
        for e in self.ap:
            if e["t0"] - e["fundido"] <= t <= e["t1"]:
                return e
        return None

    # ---- cámara: durante la apertura sale de México entero y llega a la cámara de la coreografía
    def _cam_mexico(self):
        v = Vista.ajustar(-117.6, -86.4, 14.2, 32.9, W, H, 0.03) if not self.vertical else Vista.ajustar(-108.5, -96.0, 14.2, 32.9, W, H, 0.02)
        return v.lon, v.lat, v.k / self.M.PXDEG_REF

    def camara(self, t, st):
        e = self._ap(t)
        if e is None:
            return st
        lon0, lat0, z0 = self._cam_mexico()
        ta = e["t0"] + e["quieto"]
        if t <= ta:
            return (lon0, lat0, z0 * (1 + 0.012 * (t - e["t0"])), 0.0)
        st1 = self.cam_fn(e["t1"]) if self.cam_fn else st
        u = (t - ta) / max(1e-3, e["t1"] - ta)
        uz = suave(u) ** 1.0
        z = math.exp((1 - uz) * math.log(z0 * (1 + 0.012 * e["quieto"])) + uz * math.log(st1[2]))
        # el centro llega antes que el zoom (si no, el estado se sale del cuadro a media apertura)
        up = suave(min(1.0, u * 1.6))
        y = (1 - up) * float(ymerc(lat0)) + up * float(ymerc(st1[1]))
        return ((1 - up) * lon0 + up * st1[0], float(inv_ymerc(y)), z, up * (st1[3] if len(st1) > 3 else 0.0))

    # ---- fondo
    def _peso_fino(self, t, cam):
        """Cuánto manda el mapa fino del video (0 = México en guache)."""
        e = self._ap(t)
        if e is None:
            return 1.0
        if t < e["t0"] + e["quieto"]:
            return 0.0
        st1 = self.cam_fn(e["t1"]) if self.cam_fn else (cam.lon, cam.lat, cam.z)
        r = math.log(cam.z / st1[2])              # 0 al llegar; negativo antes
        return suave((r + 1.05) / 0.85)            # entra del todo cuando faltan ~e^0,2 de zoom

    def _mascara_rejilla(self, cam):
        rej = self.M.ACT if self.M.ACT is not None else self.M.REJ["mx"]
        v = Vista.de_cam(cam, self.M.PXDEG_REF)
        P = v.pts([[rej.lon0, rej.lat0], [rej.lon1, rej.lat0], [rej.lon1, rej.lat1], [rej.lon0, rej.lat1]])
        m = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(m, np.rint(P).astype(np.int32), 255, cv2.LINE_AA)
        m = cv2.erode(m, np.ones((41, 41), np.uint8))
        return cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 14)

    def _vref(self, t):
        """Vista de la cámara de la coreografía en t (para colocar rótulos UNA vez donde la cámara se asienta)."""
        st = self.cam_fn(t)
        return Vista(st[0], st[1], st[2] * self.M.PXDEG_REF, st[3] if len(st) > 3 else 0.0)

    @staticmethod
    def _cerca(v, vref, tol=0.35):
        """1 con el zoom de referencia; se apaga si la cámara se aleja o se acerca mucho (rótulos fuera de escala)."""
        return suave(1.0 - abs(math.log(v.k / vref.k)) / tol)

    def _zoom_region(self, v, r):
        """El mapa de región solo entra cuando la cámara ya se alejó (de cerca el relieve ETOPO1 se pixela)."""
        if not self.cam_fn:
            return 1.0
        return suave(1.0 - max(0.0, math.log(v.k / self._vref(min(r["t1"], r["t0"] + r.get("ref", 2.5))).k)) / 0.9)

    def _mexico(self, v, suave_=False):
        key = (round(v.lon, 4), round(v.lat, 4), round(v.k, 2), round(v.rot, 4), suave_)
        if self._cache is None or self._cache[0] != key:
            self._cache = (key, pintar_mexico(v, prota=self.prota, suave_=suave_))
        img, ms = self._cache[1]
        return img.copy(), ms

    def componer(self, img, cam, t):
        """Llamar al final de escenas.fondo: devuelve el fondo con la ubicación (apertura / estado / región) encima."""
        if not (self.ap or self.ed or self.rg):
            return img
        v = Vista.de_cam(cam, self.M.PXDEG_REF)
        e = self._ap(t)
        wr = max([self._ventana(t, r) * self._zoom_region(v, r) for r in self.rg] + [0.0])
        pf = self._peso_fino(t, cam)
        if e is not None or wr > 0:
            fino = self._mascara_rejilla(cam) * pf * (1 - wr)
            if fino.min() < 0.999:
                mx, ms = self._mexico(v)
                a = fino[..., None]
                img = mx * (1 - a) + img * a
                if e is not None:
                    self._sobre_apertura(img, v, ms, t, e, pf)
                if wr > 0:
                    self._sobre_region(img, v, ms, t, wr)
        zoom = pf if (e is not None and t > e["t0"] + e["quieto"]) else 0.0
        for ed in self.ed:
            w_ = self._ventana(t, ed)
            if zoom and e["t0"] <= ed["t0"] <= e["t1"] + 0.01:      # la capa del estado entra con el mapa fino durante el zoom
                wm = max(w_, zoom)
            else:
                wm = w_
            if wm > 0:
                self._sobre_estado(img, v, cam, t, ed, wm * (1 - wr), w_ * (1 - wr))
        if e is not None and t < e["t0"]:
            img *= suave((t - (e["t0"] - e["fundido"])) / e["fundido"])     # entra desde negro si es lo primero
        return img

    def _sobre_apertura(self, img, v, ms, t, e, pf):
        a = 1.0 - suave((t - (e["t0"] + e["quieto"])) / 1.2)             # los rótulos de país se van al empezar el zoom
        if a > 0.01:
            for n, lo, la in MARES:
                x, y = v.pt(lo, la)
                texto(img, n, x, y, 40, color=TXT_MAR, alfa=0.7 * a, espaciado=True, halo=0.5)
            x, y = v.pt(-100.9, 26.9)
            texto(img, "MÉXICO", x, y, 70, alfa=0.85 * a, espaciado=True, halo=0.5)
            x, y = v.pt(-99.13, 19.43)
            if self.prota != "MX-DIF":
                punto(img, x, y, 9, alfa=a)
                texto(img, "CDMX", x + 16, y + 6, 30, centro=False, halo=0.7, alfa=a)
            rosa(img, W - 150, H - 170, alfa=a)
        if self.prota in ms:
            cy, cx = np.argwhere(ms[self.prota] > 128).mean(0)
            b = 1.0 - suave((pf - 0.15) / 0.5)
            u = (t - e["t0"])
            ent = suave((u - 0.3) / 0.6)
            for r, al in ((60, 0.55), (95, 0.3)):
                anillo(img, cx, cy, r * (0.6 + 0.4 * ent), 4, alfa=al * b * ent)
            pin(img, cx, cy, 20, alfa=b * suave((u - 0.2) / 0.4))
            bt = ent * (1.0 - suave((t - (e["t0"] + e["quieto"])) / 0.7))   # el nombre se despide al empezar el zoom
            if bt > 0.01:
                if "_ap_txt" not in e:          # sitio del nombre (respecto a la chincheta): lo libre más cercano, fuera de los demás rótulos
                    libre = 255 - cv2.dilate(sum((m > 0).astype(np.uint8) for m in ms.values()) * 255, np.ones((15, 15), np.uint8))
                    for n, lo, la in MARES + (("MÉXICO", -100.9, 26.9),):
                        x, y = v.pt(lo, la)
                        w2 = ancho(n, 70 if n == "MÉXICO" else 40, True) / 2 + 30
                        libre[max(0, int(y - 50)):max(0, int(y + 50)), max(0, int(x - w2)):max(0, int(x + w2))] = 0
                    libre[H - 300:, W - 300:] = 0                          # rosa de los vientos
                    w_ = ancho(self.nombre, 60) + 40
                    q = cabe(libre.astype(np.uint8), w_, 80, None, 60, cerca=(cx, cy + 160))
                    e["_ap_txt"] = (q[0] - cx, q[1] - cy) if q else (0, -150)
                tx, ty = cx + e["_ap_txt"][0], cy + e["_ap_txt"][1]
                texto(img, self.nombre, tx, ty, 60, halo=0.85, alfa=bt)
                dx, dy = cx - tx, cy - ty
                n = math.hypot(dx, dy) or 1
                linea(img, (tx + dx / n * 60, ty + dy / n * 40), (cx - dx / n * 30, cy - dy / n * 30), 3, TINTA, bt)

    def _sobre_region(self, img, v, ms, t, wr):
        r = next(x for x in self.rg if self._ventana(t, x) > 0)
        vref = self._vref(min(r["t1"], r["t0"] + r.get("ref", 2.5))) if self.cam_fn else v
        cerca = self._cerca(v, vref)
        if "_pos" not in r:
            v_, ms = vref, mascaras(vref)
            ex = cv2.dilate(ms.get(self.prota, np.zeros((H, W), np.uint8)), np.ones((41, 41), np.uint8))
            if self.prota in ms:
                yx = np.argwhere(ms[self.prota] > 128)
                cx, top = yx[:, 1].mean(), yx[:, 0].min()
                r["_prota"] = v_.inv(cx, top)                       # nombre ENCIMA del estado, con una rayita hasta su borde
                w_ = ancho(self.nombre, 56)
                ex = np.maximum(ex, caja(cx - w_ / 2 - 30, top - 110, cx + w_ / 2 + 30, top))
            ex = np.maximum(ex, caja(0, 0, 520, 130))      # año
            ex = np.maximum(ex, caja(W - 640, 0, W, 130))  # sellos
            yr = 250 if not self.vertical else 420
            ex = np.maximum(ex, caja(W - 270, yr - 120, W, yr + 90))   # rosa de los vientos
            for n, lo, la in r["extra"]:                                # ciudades con nombre
                x, y = v_.pt(lo, la)
                ex = np.maximum(ex, caja(x - 20, y - 26, x + ancho(n, 30) + 30, y + 30))
            orden = [k for k in ms if k != self.prota]
            orden.sort(key=lambda k: -int((ms[k] > 127).sum()))
            r["_pos"] = colocar_rotulos(v_, ms, orden, 38, ex)
        for n, lo, la, px, esp in r["_pos"]:
            x, y = v.pt(lo, la)
            texto(img, n, x, y, px, color=(82, 70, 62), alfa=0.78 * wr * cerca, espaciado=esp, halo=0.55, borde=30)
        if "_prota" in r:
            x, y = v.pt(*r["_prota"])
            texto(img, self.nombre, x, y - 72, 56, halo=0.9, alfa=wr * cerca)
            linea(img, (x, y - 40), (x, y + 10), 3, TINTA, wr * cerca)
        for n, lo, la in r["extra"]:
            x, y = v.pt(lo, la)
            punto(img, x, y, 9, alfa=wr * cerca)
            texto(img, n, x + 16, y + 8, 30, centro=False, halo=0.7, alfa=wr * cerca)
        rosa(img, W - 140, 250 if not self.vertical else 420, alfa=wr)

    def _sobre_estado(self, img, v, cam, t, ed, w_, wf=None):
        """w_ = peso de la capa del mapa (tinte, fronteras, vecinos); wf = peso del mobiliario (cartela, tarjeta, escala)."""
        wf = w_ if wf is None else wf
        ms = mascaras(v)
        base = img.copy()
        if self.prota in ms:
            lavar(img, 255 - ms[self.prota])
            tenir(img, ms[self.prota])
        if ed["fronteras"]:
            tintes(img, ms, self.prota)
            fronteras_lapiz(img, ms, self.prota)
        if w_ < 0.999:
            img[:] = base * (1 - w_) + img * w_
        if ed["vecinos"]:
            vref = self._vref(ed["t0"] + 0.5 + ed["fundido"]) if self.cam_fn else v
            if "_pos" not in ed:
                ms = mascaras(vref)
                ex = cv2.dilate(ms.get(self.prota, np.zeros((H, W), np.uint8)), np.ones((41, 41), np.uint8))
                x0, y0, x1, y1 = self._caja_cartela()
                ex = np.maximum(ex, caja(0, 0, x1 + 20, y1 + 20))
                xt, yt, wt, ht = self._pos_tarjeta()
                ex = np.maximum(ex, caja(xt - wt / 2 - 40, yt - ht / 2 - 60, xt + wt / 2 + 40, H))
                ex = np.maximum(ex, caja(W - 640, 0, W, 130))
                otros = sorted((k for k in ms if k != self.prota and k not in self.vecinos), key=lambda k: -int((ms[k] > 127).sum()))
                ed["_pos"] = colocar_rotulos(vref, ms, [k for k in self.vecinos if k in ms] + otros, 44, ex)
            for n, lo, la, px, esp in ed["_pos"]:
                x, y = v.pt(lo, la)
                texto(img, n, x, y, px, color=TXT_EDO, alfa=0.75 * w_ * self._cerca(v, vref, 0.6), halo=0.6, espaciado=esp, borde=30)
        w_ = wf
        if w_ <= 0.01:
            return
        if ed["cartela"]:
            x, y = self._pos_cartela()
            cartela(img, self.nombre, self.subtitulo, x, y, w_)
        if ed["tarjeta"]:
            if self._tarjeta is None:
                xt, yt, wt, ht = self._pos_tarjeta()
                self._tarjeta = Tarjeta(self.prota, wt, ht)
            xt, yt, _, _ = self._pos_tarjeta()
            self._tarjeta.pegar(img, xt, yt, v, -3.0, w_)
        if ed["escala"]:
            x, y = self._pos_escala()
            escala(img, v, x, y, alfa=w_)


if __name__ == "__main__":
    preparar()
