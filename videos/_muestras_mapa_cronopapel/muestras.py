# Muestras de mapa para Cronopapel (22-oct-2026): «que se note en qué parte de México estamos».
# Mismo lugar (Aguascalientes) en varias versiones, para que el usuario elija.
# uso (desde esta carpeta):
#   PYTHONPATH="<esta carpeta>;C:\FabricaAnimaciones\videos\historia_aguascalientes;C:\FabricaAnimaciones\nucleo" python muestras.py
#   vertical: anteponer "<esta carpeta>\vert" al PYTHONPATH (trae un guion.py con FORMATO = "vertical") y pasar --vertical
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import mapa as M
from motor import H, W

AQUI = os.path.dirname(os.path.abspath(__file__))
SAL = os.path.join(AQUI, "salida")
os.makedirs(SAL, exist_ok=True)
F_EDOS = os.path.join(RAIZ := os.path.dirname(os.path.dirname(AQUI)), "videos", "historia_aguascalientes", "datos", "estados_mx.geojson")
F_ETOPO = os.path.join(RAIZ, "videos", "historia_mexico", "datos", "relieve_mx_etopo1.nc")
F_LAND = os.path.join(RAIZ, "videos", "historia_aguascalientes", "datos", "ne_10m_land.geojson")
FUENTE = "C:/Windows/Fonts/Inkfree.ttf"
FUENTE_B = "C:/Windows/Fonts/georgiab.ttf"
PROTA = "MX-AGU"
VECINOS = {"MX-ZAC": "ZACATECAS", "MX-JAL": "JALISCO", "MX-SLP": "SAN LUIS POTOSÍ", "MX-GUA": "GUANAJUATO"}
TINTA = (62, 52, 46)
PAPEL = (240, 230, 208)
ROJO = (206, 74, 50)


def c01(c):
    return np.float32(c) / 255.0


# ------------------------------------------------------------------ datos
def _anillos(g):
    if g["type"] == "Polygon":
        return [g["coordinates"][0]]
    return [p[0] for p in g["coordinates"]]


EDOS = {}
for f in json.load(open(F_EDOS, encoding="utf8"))["features"]:
    k = f["properties"].get("iso_3166_2") or f["properties"].get("adm1_code")
    EDOS.setdefault(k, []).extend(np.array(a, float) for a in _anillos(f["geometry"]))
TIERRA_MUNDO = []
for f in json.load(open(F_LAND, encoding="utf8"))["features"]:
    for a in _anillos(f["geometry"]):
        a = np.array(a, float)
        if a[:, 0].max() > -125 and a[:, 0].min() < -75 and a[:, 1].max() > 5 and a[:, 1].min() < 40:
            TIERRA_MUNDO.append(a)


def _etopo():
    from scipy.io import netcdf_file
    f = netcdf_file(F_ETOPO, "r", mmap=False)
    z = f.variables["altitude"][:].astype(np.float32).copy()
    la = f.variables["latitude"][:].astype(np.float64).copy()
    lo = f.variables["longitude"][:].astype(np.float64).copy()
    if la[0] > la[-1]:
        z, la = z[::-1].copy(), la[::-1].copy()
    return z, la, lo


ETOPO = _etopo()


def ymerc(lat):
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))


def inv_ymerc(y):
    return np.degrees(2 * np.arctan(np.exp(np.radians(y))) - np.pi / 2)


# ------------------------------------------------------------------ mapa propio de México entero (ETOPO1 + estados)
class Merc:
    def __init__(self, lon, lat, k, w, h):
        self.lon, self.lat, self.k, self.w, self.h = lon, lat, k, w, h
        self.y0 = ymerc(lat)

    @staticmethod
    def ajustar(lon0, lon1, lat0, lat1, w, h, margen=0.06):
        k = min(w * (1 - 2 * margen) / (lon1 - lon0), h * (1 - 2 * margen) / (ymerc(lat1) - ymerc(lat0)))
        return Merc((lon0 + lon1) / 2, float(inv_ymerc((ymerc(lat0) + ymerc(lat1)) / 2)), k, w, h)

    def pts(self, P):
        P = np.asarray(P, float)
        return np.stack([self.w / 2 + (P[:, 0] - self.lon) * self.k, self.h / 2 - (ymerc(P[:, 1]) - self.y0) * self.k], 1)

    def pt(self, lon, lat):
        return self.pts([[lon, lat]])[0]

    def rejilla(self):
        x = np.arange(self.w, dtype=np.float64)
        y = np.arange(self.h, dtype=np.float64)
        lon = self.lon + (x - self.w / 2) / self.k
        lat = inv_ymerc(self.y0 - (y - self.h / 2) / self.k)
        return lon, lat


def _poly(mask, rings, proj, val=255):
    P = [np.rint(proj(r) * 8).astype(np.int32) for r in rings if len(r) > 2]
    cv2.fillPoly(mask, P, val, cv2.LINE_AA, 3)
    return mask


def _ruido(h, w, semilla, escalas=((6, .5), (40, .3), (160, .2))):
    rng = np.random.default_rng(semilla)
    out = np.zeros((h, w), np.float32)
    for s, p in escalas:
        r = rng.random((h // s + 2, w // s + 2)).astype(np.float32)
        out += p * cv2.resize(r, (w, h), interpolation=cv2.INTER_CUBIC)
    return out - out.mean()


def _colores_estados(ids, masks):
    """Coloreado voraz para que dos vecinos no compartan color."""
    pal = [(232, 206, 150), (196, 214, 164), (234, 190, 166), (198, 208, 224), (220, 204, 226), (238, 224, 176)]
    ker = np.ones((7, 7), np.uint8)
    dil = {k: cv2.dilate((masks[k] > 128).astype(np.uint8), ker) for k in ids}
    col = {}
    for k in sorted(ids, key=lambda k: -int(dil[k].sum())):
        usados = {col[o] for o in col if (dil[k] & dil[o]).any()}
        col[k] = next(i for i in range(len(pal)) if i not in usados) if len(usados) < len(pal) else 0
    return {k: pal[i] for k, i in col.items()}


def pintar_mexico(mc, prota=PROTA, resaltar=True, rotular=0, suave=False):
    """Mapa de México entero en guache: relieve ETOPO1, estados en colores de papel, el protagonista en rojo."""
    w, h = mc.w, mc.h
    lon, lat = mc.rejilla()
    z, la, lo = ETOPO
    mx = ((lon - lo[0]) / (lo[1] - lo[0])).astype(np.float32)
    my = ((lat - la[0]) / (la[1] - la[0])).astype(np.float32)
    alt = cv2.remap(z, np.tile(mx, (h, 1)), np.tile(my[:, None], (1, w)), cv2.INTER_LINEAR)
    # sombreado (luz del noroeste), escala vertical según km por px
    kmpx = 111.32 / mc.k
    gy, gx = np.gradient(cv2.GaussianBlur(alt, (0, 0), 1.0))
    gx, gy = gx / (kmpx * 1000), gy / (kmpx * 1000)
    ex = 6.0 + 18.0 * min(1.0, kmpx / 3.0)
    nx, ny = -gx * ex, -gy * ex
    lx, ly, lz = -0.6, -0.6, 0.53
    sh = (nx * lx + ny * ly + lz) / np.sqrt(nx * nx + ny * ny + 1)
    sh = np.clip(sh / lz, 0.35, 1.25).astype(np.float32)
    tierra = np.zeros((h, w), np.uint8)
    _poly(tierra, TIERRA_MUNDO, mc.pts)
    tierra = np.maximum(tierra, ((alt > 0) * 255).astype(np.uint8) * (cv2.dilate(tierra, np.ones((9, 9), np.uint8)) > 0))
    masks = {k: _poly(np.zeros((h, w), np.uint8), r, mc.pts) for k, r in EDOS.items()}
    mexico = np.zeros((h, w), np.uint8)
    for m in masks.values():
        mexico = np.maximum(mexico, m)
    # mar
    prof = np.clip(-alt / 4000.0, 0, 1)[..., None]
    img = c01(M.MAR) * (1 - prof) + c01(M.MAR_HONDO) * prof
    dist = cv2.distanceTransform(255 - tierra, cv2.DIST_L2, 5)
    orilla = np.exp(-dist / (6 + 0.004 * w))[..., None]
    img = img * (1 - 0.6 * orilla) + c01(M.MAR_CL) * 0.6 * orilla
    # tierra extranjera: papel apagado
    ft = (tierra.astype(np.float32) / 255)[..., None]
    fuera = c01((222, 214, 196)) * (0.80 + 0.22 * sh[..., None])
    img = img * (1 - ft) + fuera * ft
    # estados de México
    cols = _colores_estados(list(masks), masks)
    for k, m in masks.items():
        a = (m.astype(np.float32) / 255)[..., None]
        c = ROJO if (k == prota and resaltar) else cols[k]
        if suave and k != prota:
            c = tuple(int(0.55 * v + 0.45 * p) for v, p in zip(c, PAPEL))
        img = img * (1 - a) + (c01(c) * (0.72 + 0.32 * sh[..., None])) * a
    # grano de papel / pincel
    n = _ruido(h, w, 7)
    img *= (1 + 0.10 * n)[..., None]
    # fronteras estatales: blancas con un trazo de lápiz encima
    ids = np.zeros((h, w), np.int32)
    for i, (k, m) in enumerate(masks.items(), 1):
        ids[m > 127] = i
    borde = (cv2.morphologyEx(ids.astype(np.float32), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0) & (ids > 0)
    b = cv2.GaussianBlur(borde.astype(np.float32), (0, 0), 0.8)
    b = np.clip(b * 2.2, 0, 1)[..., None]
    img = img * (1 - 0.75 * b) + c01((250, 246, 236)) * 0.75 * b
    # costa de México con tinta
    costa = cv2.morphologyEx(mexico, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32) / 255
    img = img * (1 - 0.55 * costa[..., None]) + c01(TINTA) * 0.55 * costa[..., None]
    if resaltar:
        mp = masks[prota]
        ext = cv2.morphologyEx(mp, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)).astype(np.float32) / 255
        img = img * (1 - 0.9 * ext[..., None]) + c01(TINTA) * 0.9 * ext[..., None]
    return np.clip(img, 0, 1).astype(np.float32), masks


# ------------------------------------------------------------------ texto a mano
_F = {}


def _fuente(px, f=FUENTE):
    if (px, f) not in _F:
        _F[(px, f)] = ImageFont.truetype(f, px)
    return _F[(px, f)]


def texto(img, txt, x, y, px, color=TINTA, alfa=0.9, halo=0.75, espaciado=False, centro=True, f=FUENTE, ancla_y=0.5):
    t = " ".join(txt) if espaciado else txt
    fu = _fuente(px, f)
    bb = fu.getbbox(t)
    pad = max(6, px // 5)
    w_, h_ = bb[2] + 2 * pad, int(px * 1.45) + 2 * pad
    im = Image.new("L", (w_, h_), 0)
    ImageDraw.Draw(im).text((pad, pad), t, font=fu, fill=255, stroke_width=1 if px < 60 else 2, stroke_fill=255)
    m = np.asarray(im, np.float32) / 255
    x0 = int(x - (bb[2] / 2 if centro else 0)) - pad
    y0 = int(y - (bb[1] + bb[3]) * ancla_y) - pad
    capas = []
    if halo:
        mh = cv2.dilate(m, np.ones((max(3, px // 7),) * 2, np.uint8))
        mh = cv2.GaussianBlur(mh, (0, 0), max(1.5, px / 16))
        capas.append((np.clip(mh * 1.4, 0, 1), c01(PAPEL), halo))
    capas.append((m, c01(color), alfa))
    for mm, col, al in capas:
        _pegar(img, mm, x0, y0, col, al)
    return x0, y0, w_, h_


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


def pin(img, x, y, r=22, color=ROJO):
    """Chincheta: gota roja con sombra y brillo."""
    h, w = img.shape[:2]
    m = np.zeros((h, w), np.uint8)
    cv2.circle(m, (int(x), int(y - 2.2 * r)), r, 255, -1, cv2.LINE_AA)
    cv2.fillConvexPoly(m, np.int32([[x - r * 0.82, y - 1.75 * r], [x + r * 0.82, y - 1.75 * r], [x, y]]), 255, cv2.LINE_AA)
    mf = m.astype(np.float32) / 255
    sombra_bajo(img, mf, 6, 7, 5, 0.45)
    img[:] = img * (1 - mf[..., None]) + c01(color) * mf[..., None]
    borde = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)[..., None] / 255
    img[:] = img * (1 - 0.8 * borde) + c01(TINTA) * 0.8 * borde
    cv2.circle(img, (int(x), int(y - 2.2 * r)), max(3, r // 3), (0.98, 0.95, 0.9), -1, cv2.LINE_AA)


def anillo(img, x, y, r, grosor=4, color=ROJO, alfa=0.85):
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.circle(m, (int(x), int(y)), int(r), 255, grosor, cv2.LINE_AA)
    a = m.astype(np.float32)[..., None] / 255 * alfa
    img[:] = img * (1 - a) + c01(color) * a


# ------------------------------------------------------------------ tarjeta de ubicación (minimapa en papel)
def tarjeta_mexico(w=540, h=380, vista=None, titulo="MÉXICO"):
    """Minimapa de México en una tarjeta de papel con cinta. vista = 4 esquinas (lon, lat) del encuadre actual."""
    pw, ph = w - 36, h - 74
    mc = Merc.ajustar(-117.5, -86.5, 14.3, 32.8, pw, ph, 0.02)
    mapa, masks = pintar_mexico(mc, suave=True)
    card = np.ones((h, w, 3), np.float32) * c01((246, 239, 222))
    card *= (1 + 0.05 * _ruido(h, w, 3))[..., None]
    card[18:18 + ph, 18:18 + pw] = mapa
    cv2.rectangle(card, (18, 18), (18 + pw - 1, 18 + ph - 1), c01(TINTA).tolist(), 2, cv2.LINE_AA)
    if vista is not None:
        P = np.rint(mc.pts(vista) + 18).astype(np.int32)
        cv2.polylines(card, [P], True, c01((250, 246, 236)).tolist(), 5, cv2.LINE_AA)
        cv2.polylines(card, [P], True, c01(ROJO).tolist(), 2, cv2.LINE_AA)
    cx, cy = np.argwhere(masks[PROTA] > 128).mean(0)[::-1] + 18
    anillo(card, cx, cy, 22, 3)
    texto(card, titulo, w // 2, h - 30, 34, halo=0, espaciado=True)
    return card


def pegar_tarjeta(img, card, x, y, ang=-3.0, cinta=True):
    h, w = card.shape[:2]
    d = int(math.hypot(w, h)) + 20
    big = np.zeros((d, d, 3), np.float32)
    msk = np.zeros((d, d), np.float32)
    ox, oy = (d - w) // 2, (d - h) // 2
    big[oy:oy + h, ox:ox + w] = card
    msk[oy:oy + h, ox:ox + w] = 1
    R = cv2.getRotationMatrix2D((d / 2, d / 2), ang, 1.0)
    big = cv2.warpAffine(big, R, (d, d), flags=cv2.INTER_LINEAR)
    msk = cv2.warpAffine(msk, R, (d, d), flags=cv2.INTER_LINEAR)
    x0, y0 = int(x - d / 2), int(y - d / 2)
    full = np.zeros(img.shape[:2], np.float32)
    H_, W_ = img.shape[:2]
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W_, x0 + d), min(H_, y0 + d)
    full[ya:yb, xa:xb] = msk[ya - y0:yb - y0, xa - x0:xb - x0]
    sombra_bajo(img, full, 10, 14, 10, 0.42)
    a = full[ya:yb, xa:xb, None]
    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - a) + big[ya - y0:yb - y0, xa - x0:xb - x0] * a
    if cinta:
        for sx in (-1, 1):
            cx_, cy_ = x + sx * w * 0.36, y - h * 0.5 + sx * 4
            t = cv2.boxPoints(((cx_, cy_), (120, 34), -sx * 28 + ang))
            m = np.zeros(img.shape[:2], np.uint8)
            cv2.fillConvexPoly(m, np.int32(t), 255, cv2.LINE_AA)
            a = m.astype(np.float32)[..., None] / 255 * 0.62
            img[:] = img * (1 - a) + c01((236, 226, 186)) * a


# ------------------------------------------------------------------ mapa regional (el kit actual de Aguascalientes)
def base_actual(cam, color_prota=0.0):
    img, base = M.pintar_base(cam, 0)
    if color_prota:
        M.pintar(img, cam.proyectar(M.CAMPOS["aguascalientes"]), M.COL["aguascalientes"], color_prota, 0, luz=base.luz)
    M.pintar_rios(img, cam, base)
    return img, base


def masks_pantalla(cam):
    return {k: _poly(np.zeros((H, W), np.uint8), r, cam.pant_pts) for k, r in EDOS.items()}


def lavar(img, mask, k=0.55, gris=0.7):
    """Aclara y desatura lo que NO es protagonista (papel lavado)."""
    a = (mask.astype(np.float32) / 255)[..., None] * k
    g = img.mean(2, keepdims=True)
    des = img * (1 - gris) + g * gris
    des = des * 0.55 + c01(PAPEL) * 0.45
    img[:] = img * (1 - a) + des * a


def tintes(img, masks, alfa=0.2):
    """Cada estado vecino con un velo de color propio (como el mapa escolar), muy suave para no tapar el relieve."""
    pal = {"MX-ZAC": (196, 214, 164), "MX-JAL": (232, 206, 150), "MX-SLP": (234, 190, 166), "MX-GUA": (198, 208, 224),
           "MX-NAY": (220, 204, 226), "MX-DUR": (234, 190, 166), "MX-MIC": (196, 214, 164), "MX-QUE": (220, 204, 226)}
    for k, c in pal.items():
        if k in masks:
            m = cv2.GaussianBlur(masks[k].astype(np.float32) / 255, (0, 0), 1.2)[..., None] * alfa
            img[:] = img * (1 - m) + img * c01(c) * 1.25 * m


def fronteras_lapiz(img, masks, prota=PROTA, grosor=3, alfa=0.85, prota_grosor=6, semilla=11):
    """Fronteras estatales con halo de papel y trazo de lápiz con grano; el protagonista con tinta gruesa."""
    ids = np.zeros((H, W), np.int32)
    for i, (k, m) in enumerate(masks.items(), 1):
        ids[m > 127] = i
    borde = (cv2.morphologyEx(ids.astype(np.float32), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0).astype(np.uint8)
    if grosor > 1:
        borde = cv2.dilate(borde, np.ones((grosor, grosor), np.uint8))
    halo = cv2.GaussianBlur(cv2.dilate(borde, np.ones((7, 7), np.uint8)).astype(np.float32), (0, 0), 2.5)
    img[:] = img * (1 - 0.55 * halo[..., None]) + c01((250, 245, 232)) * 0.55 * halo[..., None]
    lapiz = cv2.GaussianBlur(borde.astype(np.float32), (0, 0), 0.7)
    grano = np.clip(0.7 + 2.0 * _ruido(H, W, semilla, ((2, .6), (9, .4))), 0.25, 1.0)
    a = (lapiz * grano * alfa)[..., None]
    img[:] = img * (1 - a) + c01(TINTA) * a
    if prota:
        mp = masks[prota]
        e = cv2.morphologyEx(mp, cv2.MORPH_GRADIENT, np.ones((prota_grosor, prota_grosor), np.uint8)).astype(np.float32) / 255
        hb = cv2.GaussianBlur(cv2.dilate(e, np.ones((9, 9), np.uint8)), (0, 0), 3)
        img[:] = img * (1 - 0.7 * hb[..., None]) + c01((252, 248, 238)) * 0.7 * hb[..., None]
        a = (cv2.GaussianBlur(e, (0, 0), 0.8) * np.clip(0.85 + grano * 0.3, 0, 1) * 0.92)[..., None]
        img[:] = img * (1 - a) + c01(TINTA) * a


def polo(mask, excluir=None, margen=(150, 130)):
    """Punto más adentro de la parte VISIBLE de una máscara (para rotular sin salirse ni chocar). -> (x, y, holgura)"""
    h, w = mask.shape
    m = (mask > 127).astype(np.uint8)
    mx, my = margen
    m[:my], m[h - my:], m[:, :mx], m[:, w - mx:] = 0, 0, 0, 0
    if excluir is not None:
        m[excluir > 0] = 0
    if not m.any():
        return None
    s = 4
    d = cv2.distanceTransform(cv2.resize(m, (w // s, h // s), interpolation=cv2.INTER_NEAREST), cv2.DIST_L2, 5)
    y, x = np.unravel_index(int(d.argmax()), d.shape)
    return x * s + s // 2, y * s + s // 2, float(d.max() * s)


def cabe(mask, w_, h_, excluir=None, margen=40):
    """Centro donde un rótulo de w_×h_ cabe ENTERO dentro de la máscara (y fuera de lo excluido). -> (x, y) o None"""
    s = 4
    m = (mask > 127).astype(np.uint8)
    if excluir is not None:
        m[excluir > 0] = 0
    m[:margen], m[-margen:], m[:, :margen], m[:, -margen:] = 0, 0, 0, 0
    m = cv2.resize(m, (m.shape[1] // s, m.shape[0] // s), interpolation=cv2.INTER_NEAREST)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (max(1, int(w_ / s)), max(1, int(h_ / s))))
    e = cv2.erode(m, k)
    if not e.any():
        return None
    d = cv2.distanceTransform(e, cv2.DIST_L2, 3)
    y, x = np.unravel_index(int(d.argmax()), d.shape)
    return x * s + s // 2, y * s + s // 2


def rotulos_vecinos(img, cam, px=46, alfa=0.72, masks=None, excluir=None, cuales=VECINOS):
    """Nombre de cada estado vecino DENTRO de su territorio visible; si no cabe, más chico; si tampoco, se omite."""
    masks = masks if masks is not None else masks_pantalla(cam)
    ex = cv2.dilate(masks[PROTA], np.ones((41, 41), np.uint8))
    if excluir is not None:
        ex = np.maximum(ex, excluir)
    for k, n in cuales.items():
        if k not in masks:
            continue
        for p, esp in ((px, True), (int(px * 0.8), True), (int(px * 0.8), False), (int(px * 0.65), False)):
            t = " ".join(n) if esp else n
            w_, h_ = _fuente(p).getlength(t) + 30, p * 1.1
            q = cabe(masks[k], w_, h_, ex)
            if q:
                texto(img, n, q[0], q[1], p, color=(92, 80, 70), alfa=alfa, halo=0.6, espaciado=esp)
                ex = np.maximum(ex, caja(q[0] - w_ / 2, q[1] - h_, q[0] + w_ / 2, q[1] + h_))
                break


def caja(x0, y0, x1, y1):
    m = np.zeros((H, W), np.uint8)
    cv2.rectangle(m, (int(x0), int(y0)), (int(x1), int(y1)), 255, -1)
    return m


def escala(img, cam, x, y, km=50):
    x1, _ = cam.pant(-102.3, 21.9)
    x2, _ = cam.pant(-102.3 + km / (111.32 * math.cos(math.radians(21.9))), 21.9)
    L = int(abs(x2 - x1))
    for i in range(4):
        c = TINTA if i % 2 == 0 else (250, 246, 236)
        cv2.rectangle(img, (x + i * L // 4, y), (x + (i + 1) * L // 4, y + 10), c01(c).tolist(), -1)
    cv2.rectangle(img, (x, y), (x + L, y + 10), c01(TINTA).tolist(), 2, cv2.LINE_AA)
    texto(img, f"{km} km", x + L // 2, y + 34, 26, halo=0.5)


def rosa(img, x, y, r=46):
    P = np.float32([[0, -1], [0.22, 0], [0, 1], [-0.22, 0]]) * r
    Q = np.float32([[-1, 0], [0, 0.22], [1, 0], [0, -0.22]]) * r * 0.6
    for poly, c in ((Q, (150, 132, 110)), (P, TINTA)):
        cv2.fillConvexPoly(img, np.int32(poly + [x, y]), c01(c).tolist(), cv2.LINE_AA)
    cv2.fillConvexPoly(img, np.int32(np.float32([[0, -1], [0.22, 0], [0, 0]]) * r + [x, y]), c01(ROJO).tolist(), cv2.LINE_AA)
    cv2.circle(img, (int(x), int(y)), int(r * 1.05), c01(TINTA).tolist(), 2, cv2.LINE_AA)
    texto(img, "N", x, y - r - 22, 30, halo=0.6)


def cartela(img, linea1, linea2, x, y):
    """Etiqueta de lugar tipo recorte de papel: nombre grande + dónde queda en México."""
    f1, f2 = _fuente(58), _fuente(30)
    w_ = int(max(f1.getlength(linea1), f2.getlength(linea2))) + 70
    h_ = 128
    m = np.zeros((H, W), np.uint8)
    pts = np.int32([[x, y + 4], [x + w_, y], [x + w_ - 6, y + h_], [x + 5, y + h_ + 3]])
    cv2.fillConvexPoly(m, pts, 255, cv2.LINE_AA)
    mf = m.astype(np.float32) / 255
    sombra_bajo(img, mf, 8, 10, 7, 0.4)
    papel = c01((248, 241, 224)) * (1 + 0.05 * _ruido(H, W, 21))[..., None]
    img[:] = img * (1 - mf[..., None]) + papel * mf[..., None]
    cv2.line(img, (x + 22, y + 74), (x + w_ - 26, y + 72), c01(ROJO).tolist(), 3, cv2.LINE_AA)
    texto(img, linea1, x + 32, y + 42, 58, halo=0, centro=False)
    texto(img, linea2, x + 34, y + 100, 30, color=(110, 92, 78), halo=0, centro=False)


def esquinas(cam):
    lo0, la0 = -102.30 - (W / 2) / (cam.z * M.PXDEG_REF), 0
    pts = []
    for sx, sy in ((0, 0), (W, 0), (W, H), (0, H)):
        lon = cam.lon + (sx - W / 2) / (cam.z * M.PXDEG_REF)
        yc = ymerc(cam.lat) - (sy - H / 2) / (cam.z * M.PXDEG_REF)
        pts.append((lon, float(inv_ymerc(yc))))
    return pts


# ------------------------------------------------------------------ las muestras
def guardar(nombre, img):
    out = (np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(SAL, nombre + ".jpg"), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return out


def muestras_horizontales():
    M.cargar()
    M.usar("mx")
    LON, LAT = -102.33, 22.0
    res = []

    # 0 · HOY: el mapa tal como sale en el video
    cam = M.Cam(LON, LAT, 1.8)
    img, _ = base_actual(cam)
    res.append(("0_hoy", guardar("0_hoy", img)))

    # 1 · FRONTERAS A LÁPIZ + vecinos rotulados (encuadre un poco más abierto)
    cam = M.Cam(LON, 22.0, 1.0)
    img, _ = base_actual(cam, 0.55)
    ms = masks_pantalla(cam)
    fuera = 255 - ms[PROTA]
    lavar(img, fuera, 0.45, 0.5)
    tintes(img, ms, 0.35)
    fronteras_lapiz(img, ms)
    rotulos_vecinos(img, cam)
    x, y = cam.pant(-102.33, 22.02)
    texto(img, "AGUASCALIENTES", x, y, 64, color=TINTA, alfa=0.95, halo=0.85, espaciado=False)
    res.append(("1_fronteras", guardar("1_fronteras", img)))

    # 2 · MINIMAPA DE UBICACIÓN en una tarjeta (mapa de hoy + la tarjeta)
    cam = M.Cam(LON, LAT, 1.8)
    img, _ = base_actual(cam)
    card = tarjeta_mexico(500, 350, vista=esquinas(cam))
    pegar_tarjeta(img, card, 300, 820, -3.5)
    res.append(("2_minimapa", guardar("2_minimapa", img)))

    # 3 · RECORTE DE PAPEL: el estado levantado sobre los vecinos lavados
    cam = M.Cam(LON, 22.0, 1.15)
    img0, _ = base_actual(cam, 0.85)
    ms = masks_pantalla(cam)
    mp = ms[PROTA].astype(np.float32) / 255
    img = img0.copy()
    lavar(img, 255 - ms[PROTA], 0.85, 0.85)
    fronteras_lapiz(img, ms, prota=None, grosor=1, alfa=0.45)
    rotulos_vecinos(img, cam, 42, 0.6)
    dx, dy = -8, -12
    mlev = np.roll(np.roll(mp, dy, 0), dx, 1)
    pieza = np.roll(np.roll(img0, dy, 0), dx, 1)
    canto = np.clip(cv2.dilate(mlev, np.ones((13, 13), np.uint8)) - mlev, 0, 1)
    full = np.clip(mlev + canto, 0, 1)
    sombra_bajo(img, full, 18, 24, 14, 0.5)
    img = img * (1 - canto[..., None]) + c01((252, 248, 240)) * canto[..., None]
    img = img * (1 - mlev[..., None]) + pieza * mlev[..., None]
    x, y = cam.pant(-102.33, 22.02)
    texto(img, "AGUASCALIENTES", x + dx, y + dy, 64, halo=0.85)
    res.append(("3_recorte", guardar("3_recorte", img)))

    # 4 · APERTURA: México entero, el estado en rojo con chincheta
    mc = Merc.ajustar(-117.6, -86.4, 14.2, 32.9, W, H, 0.03)
    img, masks = pintar_mexico(mc)
    cy, cx = np.argwhere(masks[PROTA] > 128).mean(0)
    for r, a in ((60, 0.55), (95, 0.3)):
        anillo(img, cx, cy, r, 4, alfa=a)
    pin(img, cx, cy, 20)
    tx, ty = mc.pt(-111.2, 19.6)
    texto(img, "AGUASCALIENTES", tx, ty, 60, halo=0.85)
    cv2.line(img, (int(tx + 120), int(ty - 34)), (int(cx - 40), int(cy - 12)), c01(TINTA).tolist(), 3, cv2.LINE_AA)
    for n, (lo_, la_), px in (("ESTADOS UNIDOS", (-101.5, 31.2), 40), ("OCÉANO PACÍFICO", (-111.0, 17.6), 42),
                              ("GOLFO DE MÉXICO", (-91.0, 25.4), 42), ("M É X I C O", (-100.9, 26.9), 70)):
        x, y = mc.pt(lo_, la_)
        texto(img, n, x, y, px, color=(80, 92, 104) if px < 60 else TINTA, alfa=0.7 if px < 60 else 0.85,
              espaciado=px < 60, halo=0.5)
    x, y = mc.pt(-99.13, 19.43)
    cv2.circle(img, (int(x), int(y)), 9, c01(TINTA).tolist(), -1, cv2.LINE_AA)
    texto(img, "CDMX", x + 16, y + 6, 30, centro=False, halo=0.7)
    rosa(img, W - 150, H - 170)
    res.append(("4_mexico", guardar("4_mexico", img)))

    # 5 · REGIÓN con TODOS los estados de colores (división política clara)
    mc = Merc.ajustar(-106.2, -97.8, 18.6, 24.6, W, H, 0.0)
    img, masks = pintar_mexico(mc)
    yy, xx = np.argwhere(masks[PROTA] > 128).mean(0)
    ex = caja(xx - 260, yy - 150, xx + 260, yy - 50)
    ex = np.maximum(ex, cv2.dilate(masks[PROTA], np.ones((41, 41), np.uint8)))
    for k, n in list(VECINOS.items()) + [("MX-NAY", "NAYARIT"), ("MX-DUR", "DURANGO"), ("MX-MIC", "MICHOACÁN"),
                                          ("MX-QUE", "QUERÉTARO"), ("MX-COL", "COLIMA"), ("MX-HID", "HIDALGO"), ("MX-SIN", "SINALOA")]:
        if k not in masks:
            continue
        p = polo(masks[k], ex, (110, 90))
        if p and p[2] > 34:
            x, y, _ = p
            texto(img, n, x, y, 38, color=(82, 70, 62), alfa=0.78, espaciado=True, halo=0.55)
            ex = np.maximum(ex, caja(x - 200, y - 30, x + 200, y + 30))
    texto(img, "AGUASCALIENTES", xx, yy - 100, 56, halo=0.9)
    cv2.line(img, (int(xx), int(yy - 66)), (int(xx), int(yy - 22)), c01(TINTA).tolist(), 3, cv2.LINE_AA)
    x, y = mc.pt(-103.35, 20.67)
    cv2.circle(img, (int(x), int(y)), 9, c01(TINTA).tolist(), -1, cv2.LINE_AA)
    texto(img, "Guadalajara", x + 16, y + 8, 30, centro=False, halo=0.7)
    rosa(img, W - 140, 170)
    res.append(("5_region_estados", guardar("5_region_estados", img)))

    # 6 · COMBINADA (la que recomiendo): mapa de hoy + fronteras a lápiz + vecinos + minimapa + cartela + escala
    cam = M.Cam(LON, 22.0, 1.25)
    img, _ = base_actual(cam, 0.45)
    ms = masks_pantalla(cam)
    lavar(img, 255 - ms[PROTA], 0.30, 0.35)
    tintes(img, ms, 0.3)
    fronteras_lapiz(img, ms)
    rotulos_vecinos(img, cam, 44, 0.75, ms, np.maximum(caja(0, 0, 700, 230), caja(1380, 620, W, H)))
    card = tarjeta_mexico(420, 300, vista=esquinas(cam))
    pegar_tarjeta(img, card, 1640, 830, 3.0)
    cartela(img, "AGUASCALIENTES", "centro-norte de México", 60, 70)
    escala(img, cam, 70, 990, 50)
    res.append(("6_combinada", guardar("6_combinada", img)))
    return res


def hoja(res, nombre, cols=2, titulos=None):
    tiles = []
    for k, (n, im) in enumerate(res):
        t = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
        cv2.rectangle(t, (0, 486), (520, 540), (34, 30, 28), -1)
        cv2.putText(t, titulos[k] if titulos else n, (14, 524), cv2.FONT_HERSHEY_DUPLEX, 1.0, (240, 236, 226), 2, cv2.LINE_AA)
        tiles.append(t)
    while len(tiles) % cols:
        tiles.append(np.full_like(tiles[0], 30))
    filas = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    cv2.imwrite(os.path.join(SAL, nombre), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 88])


def muestra_vertical():
    M.cargar()
    M.usar("mx")
    cam = M.Cam(-102.33, 21.95, 1.45)
    img, _ = base_actual(cam, 0.45)
    ms = masks_pantalla(cam)
    lavar(img, 255 - ms[PROTA], 0.30, 0.35)
    tintes(img, ms, 0.3)
    fronteras_lapiz(img, ms)
    rotulos_vecinos(img, cam, 44, 0.75, ms, np.maximum(caja(0, 150, W, 420), caja(0, 1200, W, H)))
    card = tarjeta_mexico(460, 330, vista=esquinas(cam))
    pegar_tarjeta(img, card, 300, 1430, -3.0)
    cartela(img, "AGUASCALIENTES", "centro-norte de México", 50, 230)
    escala(img, cam, 640, 1500, 25)
    guardar("7_vertical_combinada", img)


if __name__ == "__main__":
    if "--vertical" in sys.argv:
        muestra_vertical()
    else:
        r = muestras_horizontales()
        hoja(r, "HOJA_muestras.jpg", 2, ["0 HOY", "1 FRONTERAS A LAPIZ", "2 MINIMAPA", "3 RECORTE DE PAPEL",
                                         "4 MEXICO ENTERO (apertura)", "5 REGION CON ESTADOS", "6 COMBINADA"])
    print("ok", SAL)
