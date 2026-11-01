# -*- coding: utf-8 -*-
"""PINTOR del kit «terror CRT» (`terror_crt.py`, `terror_pc.py`; docs/estilo_terror_crt.md). Es el pintor `pix` de `mods_ia_fusion`
con `P(w, h)` (búfer de cualquier tamaño: la pantalla de la tele/monitor es un `P(1216, 912)`), `ww/INI/FIN` (anclas a la voz;
leen `timeline.json` del video EN CURSO, el cwd), `acabado` y `Clip` (extractos de `clips/*.mp4`). Promovido a nucleo el 13-oct-2026.

Kit «tecno» VERTICAL (1080x1920): motion graphics dibujados por código sobre fondo oscuro con neón, circuitos y datos.

Pintor `P` a resolución completa (texto nítido), con pila de transformaciones (`cam`, `grupo`) y recorte (`clip`); todo se
mezcla con máscaras uint8 solo en el recuadro que se toca. El brillo de neón NO se pinta en cada forma: lo da `acabado`
(bloom global + viñeta + líneas de barrido + aberración cromática + glitch/temblor en los golpes).

    p = P(); fondo_tecno(p, t)
    with p.cam(1.08, 540, 900):          # zoom alrededor de un punto
        p.rrect(100, 300, 980, 900, 30, PANEL, borde=CIAN)
        p.texto("MEMORIA", 540, 360, 64, AMAR, "black")
    img = acabado(p.im, t, golpe=0.4)

Anclas a la voz por PALABRA:  ww("puente", 3, "memoria")  ->  segundo en que se dice (KeyError si no está).
"""
import contextlib
import functools
import json
import math
import os
import re

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from motor import H, W

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}

# ------------------------------------------------------------------ paleta
FONDO0 = (0.016, 0.020, 0.050)
FONDO1 = (0.050, 0.030, 0.110)
PANEL = (0.035, 0.045, 0.095)
PANEL2 = (0.060, 0.075, 0.150)
CIAN = (0.10, 0.92, 1.00)
MAGENTA = (1.00, 0.20, 0.62)
AMAR = (1.00, 0.84, 0.16)
VERDE = (0.32, 1.00, 0.46)
ROJO = (1.00, 0.24, 0.26)
BLANCO = (0.96, 0.97, 1.00)
GRIS = (0.46, 0.52, 0.66)
GRIS2 = (0.22, 0.26, 0.38)
NARANJA = (1.00, 0.56, 0.14)
LILA = (0.70, 0.60, 1.00)
NEGRO = (0.0, 0.0, 0.0)

_DIRS = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]
FUENTES = dict(black="Poppins-Black.ttf", xbold="Poppins-ExtraBold.ttf", bold="Poppins-Bold.ttf", semi="Poppins-SemiBold.ttf",
               med="Poppins-Medium.ttf", ital="Poppins-BlackItalic.ttf", mono="consolab.ttf", mono_r="consola.ttf")


# ------------------------------------------------------------------ tiempo y curvas
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def pr(t, a, b):
    return clamp((t - a) / max(b - a, 1e-6))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def e_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def e_in(x):
    x = clamp(x)
    return x ** 3


def e_back(x, c=1.9):
    x = clamp(x)
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def pop(t, t0, dur=0.36):
    """Entrada con rebote: 0 antes de t0, se pasa un poco y se asienta en 1."""
    if t <= t0:
        return 0.0
    u = (t - t0) / dur
    return 1.0 if u >= 2.2 else 1 - math.exp(-5.5 * u) * math.cos(8.5 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def mix(c0, c1, u):
    return tuple(lerp(a, b, u) for a, b in zip(c0, c1))


def rnd(i, k=0):
    """Azar determinista 0..1 a partir de enteros."""
    x = math.sin(i * 127.1 + k * 311.7) * 43758.5453
    return x - math.floor(x)


def golpe(t, t0, dur=0.35):
    """Envolvente de impacto: 1 en t0 y cae a 0."""
    return 0.0 if t < t0 else max(0.0, 1 - (t - t0) / dur) ** 2


# ------------------------------------------------------------------ anclas a la voz
def _norm(s):
    s = s.lower()
    for a, b in zip("áéíóúü", "aeiouu"):
        s = s.replace(a, b)
    return re.sub(r"[^a-zñ0-9]", "", s)


def ww(esc, frase, palabra, n=0, fin=False):
    obj = [_norm(x) for x in palabra.split()]
    ws = ESC[esc]["frases"][frase]["words"]
    nw = [_norm(x["w"]) for x in ws]
    hits = [ws[i + len(obj) - 1]["e"] if fin else ws[i]["s"]
            for i in range(len(ws) - len(obj) + 1) if all(nw[i + j].startswith(obj[j]) for j in range(len(obj)))]
    if len(hits) <= n:
        raise KeyError(f"[{esc}:{frase}] palabra no encontrada: '{palabra}' en {[x['w'] for x in ws]}")
    return hits[n]


def INI(esc, frase=0):
    return ESC[esc]["frases"][frase]["t0"]


def FIN(esc, frase=-1):
    return ESC[esc]["frases"][frase]["t1"]


# ------------------------------------------------------------------ pintor
@functools.lru_cache(maxsize=64)
def _fuente(fnt, px):
    nombre = FUENTES.get(fnt, fnt)
    for d in _DIRS:
        ruta = os.path.join(d, nombre)
        if os.path.exists(ruta):
            return ImageFont.truetype(ruta, px)
    raise FileNotFoundError(nombre)


@functools.lru_cache(maxsize=700)
def _sprite(txt, px, fnt, esp):
    f = _fuente(fnt, px)
    if esp:
        anchos = [f.getlength(c) for c in txt]
        w = int(sum(anchos) + esp * px * (len(txt) - 1)) + 8
        asc, desc = f.getmetrics()
        im = Image.new("L", (w, asc + desc + 8), 0)
        d = ImageDraw.Draw(im)
        x = 4.0
        for c, a in zip(txt, anchos):
            d.text((x, 4), c, font=f, fill=255)
            x += a + esp * px
        return np.asarray(im)
    bb = f.getbbox(txt)
    asc, desc = f.getmetrics()
    im = Image.new("L", (bb[2] - bb[0] + 8, asc + desc + 8), 0)
    ImageDraw.Draw(im).text((4 - bb[0], 4), txt, font=f, fill=255)
    return np.asarray(im)


def ancho_texto(txt, px, fnt="black", esp=0.0):
    return _sprite(txt, max(6, int(round(px))), fnt, esp).shape[1] - 8


@functools.lru_cache(maxsize=16)
def _rejilla(w, h):
    return np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))


class P:
    def __init__(self, w=None, h=None):
        self.W, self.H = w or W, h or H
        self.im = np.zeros((self.H, self.W, 3), np.float32)
        self.s, self.ox, self.oy = 1.0, 0.0, 0.0
        self.rec = (0, 0, self.W, self.H)

    # ---------------------------------------------------------------- transformaciones
    @contextlib.contextmanager
    def grupo(self, x=0.0, y=0.0, s=1.0):
        """Todo lo que se dibuje dentro queda escalado `s` con su origen en (x, y)."""
        ant = (self.s, self.ox, self.oy)
        self.ox, self.oy, self.s = self.ox + x * self.s, self.oy + y * self.s, self.s * s
        try:
            yield
        finally:
            self.s, self.ox, self.oy = ant

    def cam(self, z=1.0, cx=None, cy=None, dx=0.0, dy=0.0):
        """Cámara: zoom `z` alrededor de (cx, cy), que queda en el centro de la pantalla (más dx, dy)."""
        cx = self.W / 2 if cx is None else cx
        cy = self.H / 2 if cy is None else cy
        return self.grupo(self.W / 2 + dx - cx * z, self.H / 2 + dy - cy * z, z)

    def pivote(self, x, y, s):
        """Escala `s` alrededor de (x, y) (para entradas con rebote)."""
        return self.grupo(x - x * s, y - y * s, s)

    @contextlib.contextmanager
    def clip(self, x0, y0, x1, y1):
        ant = self.rec
        a = self._t([(x0, y0), (x1, y1)])
        self.rec = (max(ant[0], int(a[0, 0])), max(ant[1], int(a[0, 1])), min(ant[2], int(a[1, 0])), min(ant[3], int(a[1, 1])))
        try:
            yield
        finally:
            self.rec = ant

    def _t(self, pts):
        return np.asarray(pts, np.float32) * self.s + (self.ox, self.oy)

    def _bb(self, a, pad=3):
        x0, y0 = np.floor(a.min(0)).astype(int) - pad
        x1, y1 = np.ceil(a.max(0)).astype(int) + pad
        x0, y0, x1, y1 = max(self.rec[0], x0), max(self.rec[1], y0), min(self.rec[2], x1), min(self.rec[3], y1)
        if x1 <= x0 or y1 <= y0:
            return None
        return x0, y0, x1, y1

    def _blend(self, m, x0, y0, color, op=1.0, aditivo=False):
        h, w = m.shape
        reg = self.im[y0:y0 + h, x0:x0 + w]
        a = (m.astype(np.float32) * (op / 255.0))[..., None]
        col = color if isinstance(color, np.ndarray) else np.float32(color)
        if aditivo:
            reg += a * col
        else:
            reg *= 1 - a
            reg += a * col

    # ---------------------------------------------------------------- formas
    def fondo(self, top, bot):
        ys = (np.arange(self.H, dtype=np.float32) / self.H)[:, None, None]
        self.im[:] = np.float32(top) * (1 - ys) + np.float32(bot) * ys

    def poly(self, pts, color, op=1.0, grad=None, aditivo=False):
        if op <= 0.004:
            return
        a = self._t(pts)
        bb = self._bb(a)
        if bb is None:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(m, [np.round((a - (x0, y0)) * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
        if grad is not None:
            ya, yb = a[:, 1].min(), a[:, 1].max()
            u = np.clip((np.arange(y0, y1, dtype=np.float32) - ya) / max(yb - ya, 1), 0, 1)[:, None, None]
            color = np.broadcast_to(np.float32(grad[0]) * (1 - u) + np.float32(grad[1]) * u, (y1 - y0, x1 - x0, 3))
        self._blend(m, x0, y0, color, op, aditivo)

    def rect(self, x0, y0, x1, y1, color, op=1.0, grad=None, aditivo=False):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, op, grad, aditivo)

    @staticmethod
    def _pts_rr(x0, y0, x1, y1, r):
        r = max(0.0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))
        pts = []
        for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
            for k in range(7):
                an = math.radians(a + 90 * k / 6)
                pts.append((cx + r * math.cos(an), cy + r * math.sin(an)))
        return pts

    def rrect(self, x0, y0, x1, y1, r, color=None, op=1.0, borde=None, w=4, op_b=None, grad=None):
        pts = self._pts_rr(x0, y0, x1, y1, r)
        if color is not None or grad is not None:
            self.poly(pts, color, op, grad)
        if borde is not None:
            self.polilinea(pts, w, borde, op if op_b is None else op_b, cerrado=True)

    def elip(self, x, y, rx, ry, color, op=1.0, ang=0.0, a0=0, a1=360, w=0, aditivo=False):
        """Elipse rellena (w=0) o arco de grosor w."""
        if op <= 0.004:
            return
        m_ = max(rx, ry) + w
        a = self._t([(x - m_, y - m_), (x + m_, y + m_)])
        bb = self._bb(a)
        if bb is None:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        c = (self._t([(x, y)])[0] - (x0, y0)) * 16
        ejes = (max(1, int(rx * self.s * 16)), max(1, int(ry * self.s * 16)))
        cv2.ellipse(m, (int(c[0]), int(c[1])), ejes, ang, a0, a1, 255, -1 if w <= 0 else max(1, int(round(w * self.s))), cv2.LINE_AA, shift=4)
        self._blend(m, x0, y0, color, op, aditivo)

    def circ(self, x, y, r, color, op=1.0, w=0, aditivo=False):
        self.elip(x, y, r, r, color, op, w=w, aditivo=aditivo)

    def polilinea(self, pts, w, color, op=1.0, cerrado=False, aditivo=False):
        if op <= 0.004 or len(pts) < 2:
            return
        a = self._t(pts)
        g = max(1, int(round(w * self.s)))
        bb = self._bb(a, pad=g + 3)
        if bb is None:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.polylines(m, [np.round((a - (x0, y0)) * 16).astype(np.int32)], cerrado, 255, g, cv2.LINE_AA, shift=4)
        self._blend(m, x0, y0, color, op, aditivo)

    def linea(self, p0, p1, w, color, op=1.0, aditivo=False):
        self.polilinea([p0, p1], w, color, op, aditivo=aditivo)

    def glow(self, x, y, r, color, amt=1.0, pot=2.2):
        """Resplandor aditivo de caída suave."""
        if amt <= 0.004:
            return
        a = self._t([(x - r, y - r), (x + r, y + r)])
        bb = self._bb(a, pad=0)
        if bb is None:
            return
        x0, y0, x1, y1 = bb
        gx, gy = _rejilla(x1 - x0, y1 - y0)
        c = self._t([(x, y)])[0]
        d = np.sqrt((gx + (x0 - c[0])) ** 2 + (gy + (y0 - c[1])) ** 2) / max(r * self.s, 1)
        self.im[y0:y1, x0:x1] += (np.clip(1 - d, 0, 1) ** pot * amt)[..., None] * np.float32(color)

    def texto(self, txt, x, y, px, color=BLANCO, fnt="black", op=1.0, anchor="mm", esp=0.0, sombra=0.0, aditivo=False):
        """Texto nítido. anchor: l/m/r + t/m/b. `sombra` > 0 = respaldo negro difuso para leerse sobre cualquier fondo."""
        if op <= 0.004 or not txt:
            return
        sp = _sprite(txt, max(6, int(round(px * self.s))), fnt, esp)
        h, w = sp.shape
        c = self._t([(x, y)])[0]
        rx = int(round(c[0] - w * {"l": 0, "m": 0.5, "r": 1.0}[anchor[0]]))
        ry = int(round(c[1] - h * {"t": 0, "m": 0.5, "b": 1.0}[anchor[1]]))
        if sombra > 0:
            pad = int(px * self.s * 0.35) + 4
            sx0, sy0 = max(self.rec[0], rx - pad), max(self.rec[1], ry - pad)
            sx1, sy1 = min(self.rec[2], rx + w + pad), min(self.rec[3], ry + h + pad)
            if sx1 > sx0 and sy1 > sy0:
                m = np.zeros((sy1 - sy0, sx1 - sx0), np.uint8)
                ix0, iy0 = max(rx, sx0), max(ry, sy0)
                ix1, iy1 = min(rx + w, sx1), min(ry + h, sy1)
                if ix1 > ix0 and iy1 > iy0:
                    m[iy0 - sy0:iy1 - sy0, ix0 - sx0:ix1 - sx0] = sp[iy0 - ry:iy1 - ry, ix0 - rx:ix1 - rx]
                    k = pad | 1
                    m = cv2.GaussianBlur(cv2.dilate(m, np.ones((5, 5), np.uint8)), (k, k), 0)
                    self._blend(m, sx0, sy0, NEGRO, min(1.0, sombra * op))
        x0, y0 = max(self.rec[0], rx), max(self.rec[1], ry)
        x1, y1 = min(self.rec[2], rx + w), min(self.rec[3], ry + h)
        if x1 <= x0 or y1 <= y0:
            return
        self._blend(sp[y0 - ry:y1 - ry, x0 - rx:x1 - rx], x0, y0, color, op, aditivo)

    def imagen(self, rgb, x0, y0, x1, y1, op=1.0, r=0.0, brillo=1.0):
        """Pega una imagen uint8 RGB cubriendo el rectángulo (recorta lo que sobre), con esquinas redondeadas `r`."""
        if op <= 0.004:
            return
        a = self._t([(x0, y0), (x1, y1)])
        ax0, ay0, ax1, ay1 = a[0, 0], a[0, 1], a[1, 0], a[1, 1]
        bb = self._bb(a, pad=0)
        if bb is None:
            return
        bx0, by0, bx1, by1 = bb
        ih, iw = rgb.shape[:2]
        k = max((ax1 - ax0) / iw, (ay1 - ay0) / ih)
        M = np.float32([[k, 0, (ax0 + ax1) / 2 - iw * k / 2 - bx0], [0, k, (ay0 + ay1) / 2 - ih * k / 2 - by0]])
        reg = cv2.warpAffine(rgb, M, (bx1 - bx0, by1 - by0), flags=cv2.INTER_AREA if k < 0.7 else cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE).astype(np.float32) * (brillo / 255.0)
        m = np.zeros((by1 - by0, bx1 - bx0), np.uint8)
        pts = (np.float32(self._pts_rr(x0, y0, x1, y1, r)) * self.s + (self.ox - bx0, self.oy - by0))
        cv2.fillPoly(m, [np.round(pts * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
        self._blend(m, bx0, by0, reg, op)


# ------------------------------------------------------------------ fondo y acabado
@functools.lru_cache(maxsize=1)
def _vineta():
    gx, gy = _rejilla(W, H)
    d = np.sqrt(((gx - W / 2) / (W * 0.78)) ** 2 + ((gy - H / 2) / (H * 0.66)) ** 2)
    return (1 - 0.55 * np.clip(d - 0.35, 0, 1) ** 1.6)[..., None].astype(np.float32)


@functools.lru_cache(maxsize=1)
def _barrido():
    y = np.arange(H, dtype=np.float32)
    return (1 - 0.055 * (0.5 + 0.5 * np.sin(y * math.pi / 1.5)))[:, None, None].astype(np.float32)


def fondo_tecno(p, t, tono=CIAN, tono2=MAGENTA, fuerza=1.0):
    """Fondo vivo: degradado, dos nebulosas de color a la deriva, rejilla que avanza y motas de luz en tres planos."""
    p.fondo(FONDO0, FONDO1)
    p.glow(W * (0.25 + 0.12 * math.sin(t * 0.21)), H * (0.22 + 0.06 * math.cos(t * 0.17)), 900, tono, 0.085 * fuerza, 1.6)
    p.glow(W * (0.80 + 0.10 * math.cos(t * 0.19)), H * (0.78 + 0.07 * math.sin(t * 0.23)), 980, tono2, 0.075 * fuerza, 1.6)
    paso = 120
    dx, dy = (t * 14) % paso, (t * 22) % paso
    xs = np.arange(int(dx), W, paso)
    ys = np.arange(int(dy), H, paso)
    p.im[:, xs] += 0.020
    p.im[ys, :] += 0.020
    for i in range(46):                               # motas: plano lejano (lentas, pequeñas) a cercano (rápidas, grandes)
        z = 0.35 + 0.65 * rnd(i, 3)
        x = (rnd(i, 1) * W + t * 9 * z * (1 if i % 2 else -1)) % W
        y = (rnd(i, 2) * H - t * (16 + 46 * z)) % H
        tw = 0.55 + 0.45 * math.sin(t * (1.2 + 2 * rnd(i, 5)) + i)
        p.glow(x, y, 5 + 20 * z, tono if i % 3 else tono2, 0.20 * z * tw, 1.8)


def acabado(im, t, golpe=0.0, glitch=0.0, flash=0.0, bloom=1.0):
    """Bloom + aberración cromática + líneas de barrido + viñeta. `golpe` = temblor de cámara; `glitch` = bandas corridas."""
    ch = cv2.resize(im, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    luz = np.clip(ch - 0.50, 0, None)
    b = cv2.GaussianBlur(luz, (0, 0), 5) * 0.75 + cv2.GaussianBlur(luz, (0, 0), 20) * 0.75
    im = im + cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR) * bloom
    ca = int(round(2 + 10 * glitch + 6 * golpe))
    if ca:
        im[..., 0] = np.roll(im[..., 0], ca, axis=1)
        im[..., 2] = np.roll(im[..., 2], -ca, axis=1)
    if glitch > 0.02:
        rng = np.random.default_rng(int(t * 30) * 7 + 1)
        for _ in range(int(3 + 9 * glitch)):
            y0 = int(rng.integers(0, H - 20))
            h = int(rng.integers(8, 90))
            im[y0:y0 + h] = np.roll(im[y0:y0 + h], int(rng.integers(-1, 2) * (20 + 120 * glitch) * rng.random()), axis=1)
    if golpe > 0.01:
        k = int(t * 30)
        dx, dy = int((rnd(k, 1) - 0.5) * 46 * golpe), int((rnd(k, 2) - 0.5) * 46 * golpe)
        M = np.float32([[1 + 0.03 * golpe, 0, dx - W * 0.015 * golpe], [0, 1 + 0.03 * golpe, dy - H * 0.015 * golpe]])
        im = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    im = im * _barrido() * _vineta()
    if flash > 0.003:
        im = im + flash
    return np.clip(im, 0, 1).astype(np.float32)


# ------------------------------------------------------------------ extractos de video real
class Clip:
    _abiertos = {}

    def __init__(self, ruta):
        self.cap = cv2.VideoCapture(ruta)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.n = max(1, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.pos, self.ult = -2, None

    @classmethod
    def cuadro(cls, nombre, seg):
        if nombre not in cls._abiertos:
            cls._abiertos[nombre] = Clip(os.path.join("clips", nombre + ".mp4"))
        c = cls._abiertos[nombre]
        idx = int(min(c.n - 1, max(0, round(seg * c.fps))))
        if idx == c.pos and c.ult is not None:
            return c.ult
        if not (c.pos < idx <= c.pos + 12):            # salto: buscar; si es poco, leer hacia delante (más rápido y exacto)
            c.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            c.pos = idx - 1
        f = None
        while c.pos < idx:
            ok, f = c.cap.read()
            c.pos += 1
            if not ok:
                break
        if f is not None:
            c.ult = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        return c.ult if c.ult is not None else np.zeros((720, 1280, 3), np.uint8)
