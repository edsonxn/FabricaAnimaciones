# -*- coding: utf-8 -*-
"""Motor doodle: lienzo supersampleado con capas, trazos temblorosos (boil),
rellenos, texto, sprites y composición con borde tipo sticker."""
import math
import os
from contextlib import contextmanager
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import estilos

try:                    # formato del video: guion.py -> FORMATO = "vertical" (1080x1920) o "horizontal" (1920x1080)
    import guion as _g
    VERTICAL = getattr(_g, "FORMATO", "horizontal") == "vertical"
except Exception:
    VERTICAL = False
W, H = (1080, 1920) if VERTICAL else (1920, 1080)
SS = int(os.environ.get("FAB_SS", "2"))        # supersampling del lienzo vectorial (FAB_SS=1: borrador rápido, solo vista previa)
FPS = int(os.environ.get("FAB_FPS", "30"))     # un video puede pedir 60 fps con `FPS = 60` en guion.py (fab.py lo pasa en FAB_FPS)
BOIL_FPS = 10          # las líneas "hierven" a 10 fps, como animación a mano

FUENTES = {
    "snap": "C:/Windows/Fonts/SNAP____.TTF",     # groovy años 60
    "black": "C:/Windows/Fonts/seguibl.ttf",     # subtítulos
    "print": "C:/Windows/Fonts/segoeprb.ttf",    # anotaciones a mano
    "semi": "C:/Windows/Fonts/seguisb.ttf",
    "show": "C:/Windows/Fonts/SHOWG.TTF",
    # sans geométrica limpia (estilo Kurzgesagt); si falta Poppins se usa Bahnschrift
    "geo": "~/AppData/Local/Microsoft/Windows/Fonts/Poppins-Bold.ttf|C:/Windows/Fonts/bahnschrift.ttf",
    "geo_n": "~/AppData/Local/Microsoft/Windows/Fonts/Poppins-SemiBold.ttf|C:/Windows/Fonts/bahnschrift.ttf",
    # rotulación estilo Vox: grotesca gruesa + serif para pies de mapa
    "vox_x": "~/AppData/Local/Microsoft/Windows/Fonts/Montserrat-Black.ttf|C:/Windows/Fonts/seguibl.ttf",
    "vox_b": "~/AppData/Local/Microsoft/Windows/Fonts/Montserrat-ExtraBold.ttf|C:/Windows/Fonts/seguibl.ttf",
    "vox_s": "~/AppData/Local/Microsoft/Windows/Fonts/Montserrat-SemiBold.ttf|C:/Windows/Fonts/seguisb.ttf",
    "vox_serif": "~/AppData/Local/Microsoft/Windows/Fonts/Baskervville-BoldItalic.ttf|C:/Windows/Fonts/georgiaz.ttf",
    "geo_x": "~/AppData/Local/Microsoft/Windows/Fonts/Poppins-ExtraBold.ttf|C:/Windows/Fonts/seguibl.ttf",
}

NEGRO = (20, 16, 24)
BLANCO = (255, 252, 244)
OCRE = (178, 64, 34)
OCRE_CLARO = (214, 120, 60)
PIEL = (241, 190, 140)
PIEL_N = (214, 160, 112)


# ---------------------------------------------------------------- easing
def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def prog(t, a, b):
    if b <= a:
        return 1.0 if t >= a else 0.0
    return clamp01((t - a) / (b - a))


def lerp(a, b, u):
    return a + (b - a) * u


def smooth(x):
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def e_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def e_in(x):
    x = clamp01(x)
    return x ** 3


def e_inout(x):
    x = clamp01(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def e_back(x, s=1.9):
    x = clamp01(x) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def e_elastic(x):
    x = clamp01(x)
    if x in (0.0, 1.0):
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * 2 * math.pi / 3) + 1


def campana(t, a, b):
    """0 fuera de [a,b], sube y baja suave dentro."""
    if t <= a or t >= b:
        return 0.0
    return math.sin(math.pi * (t - a) / (b - a))


# ---------------------------------------------------------------- ruido determinista
_M32 = np.uint64(0xFFFFFFFF)


def hash_arr(a, b=0, c=0):
    a = np.asarray(np.floor(a) + 4_000_000, dtype=np.int64).astype(np.uint64)
    b = np.asarray(np.floor(b) + 4_000_000, dtype=np.int64).astype(np.uint64)
    c = np.asarray(np.floor(c) + 4_000_000, dtype=np.int64).astype(np.uint64)
    x = (a * np.uint64(73856093)) ^ (b * np.uint64(19349663)) ^ (c * np.uint64(83492791))
    x &= _M32
    x ^= x >> np.uint64(13)
    x = (x * np.uint64(0x5BD1E995)) & _M32
    x ^= x >> np.uint64(15)
    return (x & np.uint64(0xFFFFFF)).astype(np.float64) / 16777216.0


def h01(a, b=0, c=0):
    return float(hash_arr(np.array([a]), np.array([b]), np.array([c]))[0])


def ruido1(x, seed=0, canal=0):
    """Ruido de valor 1D suave en [-1,1]."""
    x = np.asarray(x, dtype=np.float64)
    i = np.floor(x)
    f = x - i
    u = f * f * (3 - 2 * f)
    a = hash_arr(i, seed, canal) * 2 - 1
    b = hash_arr(i + 1, seed, canal) * 2 - 1
    return a + (b - a) * u


def r1(x, seed=0, canal=0):
    return float(ruido1(np.array([x]), seed, canal)[0])


# ---------------------------------------------------------------- geometría
def remuestrear(P, paso, cerrado):
    if cerrado:
        P = np.vstack([P, P[:1]])
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    L = d[-1]
    if L < 1e-6:
        return P
    n = max(3, int(L / paso) + 1)
    s = np.linspace(0, L, n)
    return np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], 1)


def circulo(cx, cy, r, n=64, a0=0.0):
    a = a0 + np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def elipse(cx, cy, rx, ry, rot=0.0, n=64):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x, y = rx * np.cos(a), ry * np.sin(a)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + c * x - s * y, cy + s * x + c * y], 1)


def arco(cx, cy, r, a0, a1, n=32, ry=None):
    a = np.linspace(a0, a1, n)
    return np.stack([cx + r * np.cos(a), cy + (ry or r) * np.sin(a)], 1)


def blob(cx, cy, r, seed=0, irr=0.18, n=72, lob=5):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    k = a / (2 * np.pi) * lob
    rr = r * (1 + irr * ruido1(k, seed, 3) + irr * 0.5 * ruido1(k * 2.3, seed, 5))
    # cerrar el ruido de forma periódica: mezcla con el inicio
    w = np.clip((a - 1.5 * np.pi) / (0.5 * np.pi), 0, 1)
    r0 = r * (1 + irr * ruido1(np.zeros(1), seed, 3) + irr * 0.5 * ruido1(np.zeros(1), seed, 5))
    rr = rr * (1 - w) + r0 * w
    return np.stack([cx + rr * np.cos(a), cy + rr * np.sin(a)], 1)


def estrella(cx, cy, r1_, r2_, puntas=5, rot=-np.pi / 2):
    a = rot + np.arange(puntas * 2) * np.pi / puntas
    r = np.where(np.arange(puntas * 2) % 2 == 0, r1_, r2_)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def corazon(cx, cy, s, n=80):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    return np.stack([cx + x * s / 16, cy + y * s / 16], 1)


def rect_red(x, y, w, h, r, n=10):
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -np.pi / 2), (x + w - r, y + h - r, 0),
                       (x + r, y + h - r, np.pi / 2), (x + r, y + r, np.pi)):
        a = np.linspace(a0, a0 + np.pi / 2, n)
        pts.append(np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1))
    return np.vstack(pts)


def bezier(p0, p1, p2, p3, n=40):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def catmull(P, n=12, cerrado=False):
    P = np.asarray(P, dtype=np.float64)
    if cerrado:
        P = np.vstack([P[-1:], P, P[:2]])
    else:
        P = np.vstack([P[:1], P, P[-1:]])
    out = []
    t = np.linspace(0, 1, n, endpoint=False)[:, None]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    if not cerrado:
        out.append(P[-2][None])
    return np.vstack(out)


def espiral(cx, cy, r0, r1_, vueltas, n=200, a0=0.0):
    a = np.linspace(0, vueltas * 2 * np.pi, n)
    r = np.linspace(r0, r1_, n)
    return np.stack([cx + r * np.cos(a + a0), cy + r * np.sin(a + a0)], 1)


def mat_t(x, y):
    return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], dtype=np.float64)


def mat_r(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float64)


def mat_s(sx, sy=None):
    return np.array([[sx, 0, 0], [0, sx if sy is None else sy, 0], [0, 0, 1]], dtype=np.float64)


# ---------------------------------------------------------------- texto
@lru_cache(maxsize=64)
def fuente(nombre, px):
    import os
    rutas = [os.path.expanduser(r) for r in FUENTES[nombre].split("|")]
    ruta = next((r for r in rutas if os.path.exists(r)), rutas[-1])
    return ImageFont.truetype(ruta, int(px))


@lru_cache(maxsize=3000)
def sprite_texto(texto, nombre, px, color, borde, borde_px):
    """RGBA premultiplicado uint8 con texto relleno + contorno (px ya en espacio destino)."""
    f = fuente(nombre, px)
    x0, y0, x1, y1 = f.getbbox(texto, stroke_width=borde_px)
    pad = 4
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    org = (pad - x0, pad - y0)
    ms = Image.new("L", (w, h), 0)
    ImageDraw.Draw(ms).text(org, texto, font=f, fill=255, stroke_width=borde_px, stroke_fill=255)
    mf = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mf).text(org, texto, font=f, fill=255)
    ms = np.asarray(ms, np.float32)[..., None] / 255
    mf = np.asarray(mf, np.float32)[..., None] / 255
    if borde is None or borde_px == 0:
        ms = mf
    cf = np.array(color, np.float32)
    cb = np.array(borde if borde is not None else color, np.float32)
    rgb = cf * mf + cb * np.clip(ms - mf, 0, 1)
    a = np.clip(ms + mf - ms * mf, 0, 1) * 255
    return np.concatenate([rgb, a], -1).round().astype(np.uint8)


def ancho_texto(texto, nombre, px):
    return fuente(nombre, int(px)).getlength(texto)


# ---------------------------------------------------------------- lienzo
class Lienzo:
    """Capas: 0 = pared/fondo dibujado, 1 = stickers (borde blanco + sombra), 2 = encima."""

    NCAPAS = 3

    def __init__(self):
        self.capas = [np.zeros((H * SS, W * SS, 4), np.uint8) for _ in range(self.NCAPAS)]
        self.sucia = [True] * self.NCAPAS
        self.M = np.eye(3)
        self.pila = []
        self.c = 1
        self.wob = 2.0
        self.boil = 0
        self.t = 0.0
        self.recortes = []   # polígonos de recorte activos (px SS, punto fijo x16)

    def nuevo(self, t, wob=2.0):
        for i, c in enumerate(self.capas):
            if self.sucia[i]:
                c[:] = 0
                self.sucia[i] = False
        self.M = np.eye(3)
        self.pila = []
        self.recortes = []
        self.c = 1
        self.t = t
        self.boil = int(math.floor(t * BOIL_FPS + 1e-6))
        self.wob = wob
        self.dif = []                  # etiquetas sin cola diferidas (se dibujan al final del cuadro, ya sabiendo dónde quedó todo lo demás)
        self.zonas_rot = []            # rectángulos de rótulos ya dibujados en este cuadro (para que las etiquetas sin cola no se encimen)
        self.ocupado = []              # huecos ya usados por íconos de ciudad en este cuadro (evita que se amontonen en el mapa)

    # ---- transformaciones
    def push(self):
        self.pila.append(self.M.copy())

    def pop(self):
        self.M = self.pila.pop()

    @contextmanager
    def grupo(self, x=0.0, y=0.0, s=1.0, rot=0.0, sy=None):
        self.push()
        self.M = self.M @ mat_t(x, y) @ mat_r(rot) @ mat_s(s, sy)
        try:
            yield self
        finally:
            self.pop()

    @contextmanager
    def capa(self, i):
        prev = self.c
        self.c = i
        try:
            yield self
        finally:
            self.c = prev

    @contextmanager
    def recorte(self, pts):
        """Todo lo que se dibuje dentro queda recortado a la forma `pts` (coords locales). Se pueden anidar."""
        self.recortes.append(np.round(self.a_px(pts) * SS * 16).astype(np.int32))
        try:
            yield self
        finally:
            self.recortes.pop()

    def _caja_recorte(self, x0, y0, x1, y1):
        """Intersecta una caja (px SS) con el lienzo y con los recortes activos."""
        x0, y0 = max(0, int(x0)), max(0, int(y0))
        x1, y1 = min(W * SS, int(x1)), min(H * SS, int(y1))
        for Q in self.recortes:
            qx0, qy0 = Q.min(0) // 16 - 2
            qx1, qy1 = Q.max(0) // 16 + 3
            x0, y0, x1, y1 = max(x0, qx0), max(y0, qy0), min(x1, qx1), min(y1, qy1)
        return x0, y0, x1, y1

    def _mascara_recorte(self, x0, y0, x1, y1):
        m = None
        for Q in self.recortes:
            mk = np.zeros((y1 - y0, x1 - x0), np.uint8)
            cv2.fillPoly(mk, [Q - np.array([x0 * 16, y0 * 16], np.int32)], 255, cv2.LINE_AA, 4)
            m = mk if m is None else (m.astype(np.uint16) * mk // 255).astype(np.uint8)
        return m

    def _dibujar_en(self, buf, caja, fn, alfa=1.0):
        """Dibuja fn(tmp, off) en un búfer temporal del tamaño de `caja`, aplica recortes y alfa, y compone."""
        x0, y0, x1, y1 = self._caja_recorte(*caja)
        if x1 <= x0 or y1 <= y0:
            return
        tmp = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
        fn(tmp, np.array([x0 * 16, y0 * 16], np.int32))
        m = self._mascara_recorte(x0, y0, x1, y1)
        if m is not None:
            a = cv2.multiply(tmp, cv2.merge([m, m, m, m]), scale=1 / 255.0)
            tmp = a
        self._componer_bloques(buf, tmp, x0, y0, alfa)

    def _componer_bloques(self, buf, tmp, x0, y0, alfa=1.0, T=256):
        """Compone regiones grandes por bloques de TxT, saltando los bloques totalmente transparentes."""
        h, w = tmp.shape[:2]
        if h * w < 600_000:
            self._componer(buf, tmp, x0, y0, alfa)
            return
        a = tmp[..., 3]
        ny, nx = -(-h // T), -(-w // T)
        pad = np.zeros((ny * T, nx * T), np.uint8)
        pad[:h, :w] = a
        ocupado = pad.reshape(ny, T, nx, T).max(axis=(1, 3)) > 0
        for by, bx in zip(*np.nonzero(ocupado)):
            ya, xa = by * T, bx * T
            self._componer(buf, tmp[ya:ya + T, xa:xa + T], x0 + xa, y0 + ya, alfa)

    def escala(self):
        return math.sqrt(abs(np.linalg.det(self.M[:2, :2])))

    def a_px(self, pts):
        P = np.asarray(pts, dtype=np.float64)
        return P @ self.M[:2, :2].T + self.M[:2, 2]

    def _buf(self, capa):
        i = self.c if capa is None else capa
        self.sucia[i] = True
        return self.capas[i]

    def _temblor(self, P, seed, amp):
        if amp <= 0 or len(P) < 2:
            return P
        seg = np.hypot(*np.diff(P, axis=0).T)
        d = np.concatenate([[0.0], np.cumsum(seg)])
        k = d / 90.0 + h01(seed, 11) * 50
        b = self.boil
        dx = ruido1(k, seed * 7 + b * 131, 1) + 0.35 * ruido1(k * 3.1, seed * 7 + b * 131, 2)
        dy = ruido1(k, seed * 7 + b * 131, 3) + 0.35 * ruido1(k * 3.1, seed * 7 + b * 131, 4)
        return P + amp * np.stack([dx, dy], 1)

    @staticmethod
    def _col(color, alfa=255):
        c = estilizar(tuple(int(v) for v in color[:3]))
        a = int(color[3]) if len(color) == 4 else int(alfa)
        return (c[0], c[1], c[2], a)

    # ---- primitivas
    def trazo(self, pts, color=NEGRO, ancho=6.0, cerrado=False, seed=0, temblor=1.0,
              afinar=True, capa=None, paso=5.0):
        if estilos.ACTUAL.get("sin_contorno") and tuple(int(v) for v in color[:3]) == NEGRO:
            return
        P = remuestrear(self.a_px(pts), paso, cerrado)
        P = self._temblor(P, seed, self.wob * temblor)
        w = ancho * self.escala()
        if w <= 0.05:
            return
        buf = self._buf(capa)
        col = self._col(color)
        Q = np.round(P * SS * 16).astype(np.int32)
        n = len(Q)

        def dibuja(dst, off):
            Qo = Q - off
            if not afinar or cerrado or n < 10:
                cv2.polylines(dst, [Qo], cerrado, col, max(1, int(round(w * SS))), cv2.LINE_AA, 4)
                return
            chunks = int(min(12, max(4, n // 6)))
            edges = np.linspace(0, n - 1, chunks + 1).astype(int)
            for i in range(chunks):
                a, b = edges[i], edges[i + 1]
                u = (a + b) / 2 / (n - 1)
                f = 0.42 + 0.58 * math.sin(math.pi * u) ** 0.45
                cv2.polylines(dst, [Qo[a:b + 1]], False, col, max(1, int(round(w * f * SS))), cv2.LINE_AA, 4)

        if not self.recortes:
            dibuja(buf, np.zeros(2, np.int32))
            return
        m = w * SS + 4
        self._dibujar_en(buf, (Q[:, 0].min() / 16 - m, Q[:, 1].min() / 16 - m,
                               Q[:, 0].max() / 16 + m, Q[:, 1].max() / 16 + m), dibuja)

    def relleno(self, pts, color, seed=0, temblor=1.0, capa=None, alfa=1.0):
        P = remuestrear(self.a_px(pts), 5.0, True)
        P = self._temblor(P, seed, self.wob * temblor)
        Q = np.round(P * SS * 16).astype(np.int32)
        buf = self._buf(capa)
        col = self._col(color)
        if alfa >= 0.999 and not self.recortes:
            cv2.fillPoly(buf, [Q], col, cv2.LINE_AA, 4)
            return
        self._dibujar_en(buf, (Q[:, 0].min() // 16 - 2, Q[:, 1].min() // 16 - 2,
                               Q[:, 0].max() // 16 + 3, Q[:, 1].max() // 16 + 3),
                         lambda dst, off: cv2.fillPoly(dst, [Q - off], col, cv2.LINE_AA, 4), alfa)

    def degradado(self, pts, c0, c1, p0, p1, capa=None, alfa=1.0, curva=1.0):
        """Relleno con degradado lineal: color c0 en el punto p0 y c1 en p1 (coords locales)."""
        P = remuestrear(self.a_px(pts), 5.0, True)
        Q = np.round(P * SS * 16).astype(np.int32)
        a, b = self.a_px([p0, p1]) * SS
        d = b - a
        dd = float(d @ d) + 1e-9
        ca = np.array(self._col(c0)[:3], np.float32)
        cb = np.array(self._col(c1)[:3], np.float32)

        def dibuja(dst, off):
            h, w = dst.shape[:2]
            ox, oy = off / 16
            m = np.zeros((h, w), np.uint8)
            cv2.fillPoly(m, [Q - off], 255, cv2.LINE_AA, 4)
            ux = ((np.arange(w, dtype=np.float32) + ox - a[0]) * d[0] / dd)[None, :]
            uy = ((np.arange(h, dtype=np.float32) + oy - a[1]) * d[1] / dd)[:, None]
            u = np.clip(ux + uy, 0, 1)
            if curva != 1.0:
                u = u ** curva
            mf = m.astype(np.float32)[..., None] / 255
            rgb = (ca + (cb - ca) * u[..., None]) * mf
            dst[:] = np.concatenate([rgb, mf * 255], -1).round().astype(np.uint8)

        self._dibujar_en(self._buf(capa), (Q[:, 0].min() // 16 - 2, Q[:, 1].min() // 16 - 2,
                                           Q[:, 0].max() // 16 + 3, Q[:, 1].max() // 16 + 3), dibuja, alfa)

    def halo(self, x, y, r, color, alfa=1.0, dureza=1.6, capa=None, r0=0.0):
        """Resplandor radial suave (glow) centrado en (x, y), radio r (local). Opaco hasta r0*r, se desvanece
        hasta r. Se calcula a 1/4 de resolución (es suave) y se escala."""
        if alfa <= 0.003 or r <= 0:
            return
        c = self.a_px([[x, y]])[0] * SS
        R = r * self.escala() * SS
        col = np.array(self._col(color)[:3], np.float32)

        def dibuja(dst, off):
            h, w = dst.shape[:2]
            f = 4
            hs, ws = max(2, h // f + 1), max(2, w // f + 1)
            ox, oy = off / 16
            xs = (np.arange(ws, dtype=np.float32) * f + ox - c[0])[None, :]
            ys = (np.arange(hs, dtype=np.float32) * f + oy - c[1])[:, None]
            dist = np.sqrt(xs * xs + ys * ys) / R
            aa = np.clip((1 - dist) / max(1e-3, 1 - r0), 0, 1) ** dureza
            rellenar_suave(dst, aa, f, col)

        self._dibujar_en(self._buf(capa), (c[0] - R - 2, c[1] - R - 2, c[0] + R + 3, c[1] + R + 3), dibuja, alfa)

    def forma(self, pts, relleno=None, borde=NEGRO, ancho=6.0, seed=0, temblor=1.0, capa=None):
        if relleno is not None:
            self.relleno(pts, relleno, seed, temblor, capa)
        if borde is not None and ancho > 0:
            self.trazo(pts, borde, ancho, cerrado=True, seed=seed, temblor=temblor, capa=capa)

    def puntos(self, pts, radio, color, capa=None):
        """Muchos círculos rellenos (sin temblor): partículas, spray, estrellas."""
        P = self.a_px(pts)
        r = np.broadcast_to(np.asarray(radio, dtype=np.float64) * self.escala(), (len(P),))
        buf = self._buf(capa)
        col = self._col(color)
        Q = np.round(P * SS * 16).astype(np.int32)
        R = np.maximum(1, np.round(r * SS * 16)).astype(np.int32)
        if len(Q) == 0:
            return

        def dibuja(dst, off):
            for (x, y), rr in zip(Q - off, R):
                cv2.circle(dst, (int(x), int(y)), int(rr), col, -1, cv2.LINE_AA, 4)

        if not self.recortes:
            dibuja(buf, np.zeros(2, np.int32))
            return
        m = R.max() / 16 + 2
        self._dibujar_en(buf, (Q[:, 0].min() / 16 - m, Q[:, 1].min() / 16 - m,
                               Q[:, 0].max() / 16 + m, Q[:, 1].max() / 16 + m), dibuja)

    # ---- sprites
    @staticmethod
    def _componer(buf, spr, x0, y0, alfa=1.0):
        """'Over' premultiplicado: dst = spr + dst * (1 - alfa_spr), con OpenCV en enteros."""
        h, w = spr.shape[:2]
        dst = buf[y0:y0 + h, x0:x0 + w]
        if spr.dtype != np.uint8 or alfa < 0.999:
            spr = cv2.convertScaleAbs(spr, alpha=float(min(1.0, alfa)))
        inv = 255 - spr[..., 3]
        dst[:] = cv2.add(cv2.multiply(dst, cv2.merge([inv, inv, inv, inv]), scale=1 / 255.0), spr)

    def pegar(self, spr, x, y, k=1.0, rot=0.0, ancla=(0.5, 0.5), alfa=1.0, capa=None):
        """spr en píxeles SS; k = escala local."""
        if alfa <= 0.003:
            return
        h, w = spr.shape[:2]
        A = mat_s(SS) @ self.M @ mat_t(x, y) @ mat_r(rot) @ mat_s(k) @ mat_t(-ancla[0] * w, -ancla[1] * h)
        cs = np.array([[0, 0, 1], [w, 0, 1], [w, h, 1], [0, h, 1]], np.float64) @ A.T
        x0 = int(max(0, math.floor(cs[:, 0].min()) - 1))
        y0 = int(max(0, math.floor(cs[:, 1].min()) - 1))
        x1 = int(min(W * SS, math.ceil(cs[:, 0].max()) + 2))
        y1 = int(min(H * SS, math.ceil(cs[:, 1].max()) + 2))
        if x1 <= x0 or y1 <= y0:
            return
        A2 = mat_t(-x0, -y0) @ A
        # reducciones fuertes: pre-reducir para no generar aliasing
        esc = math.sqrt(abs(np.linalg.det(A2[:2, :2])))
        src = spr
        if esc < 0.6:
            f = max(esc * 1.3, 1.0 / max(w, h))
            src = cv2.resize(spr, (max(1, int(w * f)), max(1, int(h * f))), interpolation=cv2.INTER_AREA)
            A2 = A2 @ mat_s(w / src.shape[1], h / src.shape[0])
        warp = cv2.warpAffine(src, A2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        if self.recortes:
            m = self._mascara_recorte(x0, y0, x1, y1)
            warp = warp.astype(np.float32) * (m[..., None].astype(np.float32) / 255.0)
        self._componer(self._buf(capa), warp, x0, y0, alfa)

    def texto(self, s, x, y, px, fuente_="snap", color=BLANCO, borde=NEGRO, borde_px=None,
              k=1.0, rot=0.0, ancla=(0.5, 0.5), alfa=1.0, capa=None, temblor=1.0, seed=0):
        eff = px * k * self.escala()
        if eff < 2:
            return
        if estilos.ACTUAL["relleno"] == "oscuro" and tuple(color[:3]) == NEGRO:
            color = (235, 235, 245)      # texto oscuro sobre rellenos oscurecidos: aclararlo
        q = 2 ** (round(math.log2(eff) * 16) / 16)            # pasos de ~4%
        bp = borde_px if borde_px is not None else max(2.0, px * 0.085)
        bpq = int(round(bp * k * self.escala() * SS)) if borde is not None else 0
        spr = sprite_texto(s, fuente_, int(round(q * SS)), tuple(color),
                           tuple(borde) if borde is not None else None, bpq)
        kk = (px * k) / (q * SS)
        if temblor > 0 and not estilos.ACTUAL.get("texto_fijo"):
            rot += 0.012 * temblor * r1(self.boil * 0.9, seed, 7)
            x += 1.2 * temblor * r1(self.boil * 0.9, seed, 8)
            y += 1.2 * temblor * r1(self.boil * 0.9, seed, 9)
        self.pegar(spr, x, y, kk, rot, ancla, alfa, capa)

    # ---- salida
    def resolver(self):
        out = []
        for i, c in enumerate(self.capas):
            if self.sucia[i]:
                out.append(cv2.resize(c, (W, H), interpolation=cv2.INTER_AREA))
            else:
                out.append(None)
        return out


def rellenar_suave(dst, aa, f, col):
    """Llena dst (RGBA premultiplicado uint8) con un alfa suave calculado a 1/f de resolución (aa en [0,1])."""
    h, w = dst.shape[:2]
    a8 = np.clip(aa * 255 + 0.5, 0, 255).astype(np.uint8)
    A = cv2.resize(a8, (a8.shape[1] * f, a8.shape[0] * f), interpolation=cv2.INTER_LINEAR)[:h, :w]
    ch = [cv2.convertScaleAbs(A, alpha=float(c) / 255.0) for c in col[:3]]
    dst[:] = cv2.merge(ch + [A])


# ---------------------------------------------------------------- estilo
def estilizar(c):
    """Color RGB -> color según el estilo activo (la tinta NEGRO se sustituye; rellenos se transforman)."""
    E = estilos.ACTUAL
    if E["tinta"] is not None and c == NEGRO:
        return E["tinta"]
    return estilos.transformar_relleno(c) if E["relleno"] else c


_TEX_CACHE = {}


def textura_trazo(boil, fuerza):
    """Máscara multiplicativa (H,W,1) que 'rompe' los trazos como tiza/lápiz; cambia a 10 fps."""
    k = boil % 3
    if k not in _TEX_CACHE:
        rng = np.random.default_rng(900 + k)
        n = rng.normal(0, 1, (H, W)).astype(np.float32)
        n = cv2.GaussianBlur(n, (0, 0), 0.8) + 0.6 * cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 3.0, sigmaY=0.6)
        n = (n - n.min()) / (n.max() - n.min())
        _TEX_CACHE[k] = np.clip((n - 0.42) / 0.3, 0, 1)[..., None]
    return 1.0 - fuerza * _TEX_CACHE[k]


_K_CACHE = {}


def _kernel(d):
    if d not in _K_CACHE:
        _K_CACHE[d] = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d, d))
    return _K_CACHE[d]


# ---------------------------------------------------------------- composición
def componer(fondo, capas, sticker=None, sombra=None, borde_col=None, estilo=True, boil=0):
    """fondo float32 HxWx3 en [0,1]; capas uint8 premultiplicadas (o None).
    estilo=True aplica el estilo activo (sticker, sombra, textura de tiza, brillo neón);
    estilo=False es para la capa de interfaz (subtítulos), que no debe estilizarse."""
    E = estilos.ACTUAL if estilo else None
    if sticker is None:
        sticker = E["sticker"] if E else False
    if sombra is None:
        sombra = E["sombra"] if E else 0.0
    if borde_col is None:
        bc = (E["borde_sticker"] if E else None) or (255, 251, 242)
        borde_col = tuple(v / 255 for v in bc)
    tex = E["textura_trazo"] if E else 0.0
    neon = E["brillo_neon"] if E else 0.0
    kernel = _kernel(E["grosor_sticker"] if E else 13)
    img = fondo
    c0, c1, c2 = capas
    T = textura_trazo(boil, tex) if tex > 0 else None
    # «over» de cada capa con numba (fusiona astype + /255 + mezcla: ~3x menos tiempo, mismo resultado). `propio` = img ya
    # es un arreglo nuestro y se puede escribir encima (el fondo puede venir de una caché y no se toca).
    rapido = _sobre_nb is not None and T is None and img.dtype == np.float32 and img.shape == (H, W, 3)
    propio = False
    if c0 is not None:
        if rapido:
            img, propio = _sobre(img, c0, propio), True
        else:
            c = c0.astype(np.float32) / 255
            if T is not None:
                c = c * T
            img = c[..., :3] + img * (1 - c[..., 3:4])
    if c1 is not None and rapido and not (sticker or sombra > 0 or neon > 0):
        img, propio = _sobre(img, c1, propio), True
    elif c1 is not None:
        m = c1[..., 3]
        c = c1.astype(np.float32) / 255
        if T is not None:
            c = c * T
        if sticker or sombra > 0:
            if sticker:
                dil = cv2.dilate(m, kernel)
                dil = cv2.GaussianBlur(dil, (3, 3), 0).astype(np.float32) / 255
            else:
                dil = m.astype(np.float32) / 255
            if sombra > 0:
                sh = cv2.GaussianBlur(dil, (0, 0), 7)
                sh = cv2.warpAffine(sh, np.float32([[1, 0, 9], [0, 1, 12]]), (W, H))
                img = img * (1 - sombra * sh[..., None])
            if sticker:
                img = img * (1 - dil[..., None]) + np.array(borde_col, np.float32) * dil[..., None]
        img = c[..., :3] + img * (1 - c[..., 3:4])
        if neon > 0:
            # brillo solo de lo saturado y luminoso (contornos de neón), no de textos/rellenos claros
            rgb = np.ascontiguousarray(c[..., :3])
            mx, mn = rgb.max(-1, keepdims=True), rgb.min(-1, keepdims=True)
            sat = np.clip((mx - mn) / (mx + 1e-4), 0, 1)
            fuente = rgb * (sat ** 2) * np.clip(mx * 1.3 - 0.3, 0, 1)
            glow = cv2.GaussianBlur(fuente, (0, 0), 8) * 0.9 + cv2.GaussianBlur(fuente, (0, 0), 2.5) * 0.35
            img = img + neon * glow
        propio = True
    if c2 is not None:
        if rapido and img.dtype == np.float32:
            img = _sobre(img, c2, propio)
        else:
            c = c2.astype(np.float32) / 255
            img = c[..., :3] + img * (1 - c[..., 3:4])
    return img


def _a_uint8_numpy(img):
    return np.clip(img * 255 + 0.5, 0, 255).astype(np.uint8)


try:                                    # conversión float [0,1] -> uint8 en un solo paso multihilo (FAB_SIN_NUMBA=1 la apaga)
    if os.environ.get("FAB_SIN_NUMBA"):
        raise ImportError
    from numba import njit as _njit, prange as _prange

    @_njit(parallel=True, cache=True)
    def _a8(x, out):
        c255, medio = np.float32(255.0), np.float32(0.5)
        for i in _prange(x.shape[0]):
            v = x[i] * c255 + medio
            out[i] = 0 if v < 0 else (255 if v > 255 else np.uint8(v))
except Exception:
    _a8 = None

try:                                    # «over» de una capa uint8 premultiplicada sobre una imagen float32 (componer)
    if os.environ.get("FAB_SIN_NUMBA"):
        raise ImportError
    from numba import njit as _njit, prange as _prange

    @_njit(parallel=True, cache=True)
    def _sobre_nb(img, cap, out):
        k = np.float32(255.0)
        uno = np.float32(1.0)
        for y in _prange(img.shape[0]):
            for x in range(img.shape[1]):
                a = cap[y, x, 3]
                if a == 0:
                    for ch in range(3):
                        out[y, x, ch] = img[y, x, ch] * uno
                else:
                    inv = uno - np.float32(a) / k
                    for ch in range(3):
                        out[y, x, ch] = np.float32(cap[y, x, ch]) / k + img[y, x, ch] * inv
except Exception:
    _sobre_nb = None


def _sobre(img, cap, en_sitio):
    """cap (uint8 HxWx4 premultiplicada) 'over' img (float32 HxWx3). en_sitio=True escribe sobre img."""
    out = img if en_sitio else np.empty((H, W, 3), np.float32)
    _sobre_nb(img, cap, out)
    return out


def a_uint8(img):
    if _a8 is not None and img.dtype == np.float32 and img.flags.c_contiguous:
        out = np.empty(img.shape, np.uint8)
        _a8(img.reshape(-1), out.reshape(-1))
        return out
    return _a_uint8_numpy(img)
