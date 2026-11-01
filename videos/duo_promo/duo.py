# -*- coding: utf-8 -*-
"""Kit «Dúo» VERTICAL (1080x1920): la interfaz de la app Dúo (E:/CalendarioPareja, modo oscuro) dibujada por código.

Pintor `P` (primitivas tomadas del kit de mods_ia_fusion/pix.py) + lo propio de Dúo:
  - degradado horizontal de la marca (`hg=(xa, xb[, paradas, fase])` en poly/rrect/elip/texto),
  - sombras suaves de tarjeta (`sombra`), emojis de color (`emoji`, Segoe UI Emoji), trazos parciales (palomita que se dibuja),
  - componentes en px CSS de la app (dibujar dentro de `p.grupo(x, y, k)`): tarjeta, pill, tag, avatar, barra de XP, anillos de
    la semana, tarjeta de misión, calendario, botón, toast, teléfono, logo de dos círculos, confeti (`burst`), orbes de XP.
  - fondo vivo: base #17121C + tres manchas difusas (coral, violeta, rosa) a la deriva + motas/corazones flotando (dos planos).

Anclas a la voz por PALABRA:  ww("barra", 1, "llena")  ->  segundo en que se dice (KeyError si no está).
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

AQUI = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}


# ------------------------------------------------------------------ paleta (CSS de la app, modo oscuro)
def hexa(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


BG = hexa("17121C")
CARD = hexa("221B29")
LINE = hexa("32283B")
INK = hexa("F6EEF7")
MUT = hexa("A99BB0")
A = hexa("FF5E7E")          # --a  rosa coral
B = hexa("8B5CF6")          # --b  violeta
O = hexa("FF8A5B")          # inicio del degradado
GOLD = hexa("FFB648")
OK = hexa("22C58B")
FIRE = hexa("F0692F")
AV_A = hexa("FF7A6B")       # avatar de Ana (coral) — y círculo izquierdo del logo
AV_L = hexa("9B6BFF")       # avatar de Leo (violeta) — y círculo derecho del logo
CUERPO = hexa("0C090F")     # cuerpo del teléfono
BLANCO = (1.0, 1.0, 1.0)
NEGRO = (0.0, 0.0, 0.0)
GRAD = ((0.0, O), (0.45, A), (1.0, B))
GRAD_ORO = ((0.0, GOLD), (0.35, O), (0.7, hexa("FFD36B")), (1.0, GOLD))


def mix(c0, c1, u):
    return tuple(a + (b - a) * u for a, b in zip(c0, c1))


def sobre(c, base, a):
    """Color `c` con opacidad `a` sobre `base` (los rgba(...) del CSS)."""
    return mix(base, c, a)


def screen(c0, c1):
    return tuple(1 - (1 - a) * (1 - b) for a, b in zip(c0, c1))


LOGO_MEZCLA = screen(AV_A, AV_L)

_FUENTES_DIR = os.path.join(AQUI, "fuentes")
FUENTES = dict(x="PJS-ExtraBold.ttf", b="PJS-Bold.ttf", s="PJS-SemiBold.ttf", m="PJS-Medium.ttf")
EMOJI_TTF = "C:/Windows/Fonts/seguiemj.ttf"


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


def e_io(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def e_back(x, c=1.7):
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


def rnd(i, k=0):
    """Azar determinista 0..1 a partir de enteros."""
    x = math.sin(i * 127.1 + k * 311.7) * 43758.5453
    return x - math.floor(x)


def golpe(t, t0, dur=0.35):
    return 0.0 if t < t0 else max(0.0, 1 - (t - t0) / dur) ** 2


def kf(t, claves, ease=e_io):
    """Interpola entre claves [(t0, v0), (t1, v1), ...] (v número o tupla) con suavizado entre cada par."""
    if t <= claves[0][0]:
        return claves[0][1]
    for (ta, va), (tb, vb) in zip(claves, claves[1:]):
        if t <= tb:
            u = ease(pr(t, ta, tb))
            if isinstance(va, tuple):
                return tuple(lerp(a, b, u) for a, b in zip(va, vb))
            return lerp(va, vb, u)
    return claves[-1][1]


def squish(t, t0):
    """El rebote «squish» de la tarjeta al completarse (escala)."""
    if t < t0 or t > t0 + 0.55:
        return 1.0
    u = (t - t0) / 0.55
    return kf(u, [(0, 1.0), (0.3, 0.96), (0.65, 1.025), (1.0, 1.0)], smooth)


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


def T0(esc):
    return ESC[esc]["t0"]


# ------------------------------------------------------------------ fuentes, texto y emojis
@functools.lru_cache(maxsize=64)
def _fuente(fnt, px):
    return ImageFont.truetype(os.path.join(_FUENTES_DIR, FUENTES.get(fnt, fnt)), px)


@functools.lru_cache(maxsize=900)
def _sprite(txt, px, fnt, esp):
    f = _fuente(fnt, px)
    asc, desc = f.getmetrics()
    if esp:
        anchos = [f.getlength(c) for c in txt]
        w = int(sum(anchos) + esp * px * (len(txt) - 1)) + 8
        im = Image.new("L", (w, asc + desc + 8), 0)
        d = ImageDraw.Draw(im)
        x = 4.0
        for c, a in zip(txt, anchos):
            d.text((x, 4), c, font=f, fill=255)
            x += a + esp * px
        return np.asarray(im)
    bb = f.getbbox(txt)
    im = Image.new("L", (bb[2] - bb[0] + 8, asc + desc + 8), 0)
    ImageDraw.Draw(im).text((4 - bb[0], 4), txt, font=f, fill=255)
    return np.asarray(im)


def ancho_texto(txt, px, fnt="b", esp=0.0):
    return _fuente(fnt, max(6, int(round(px)))).getlength(txt) + esp * px * max(0, len(txt) - 1)


def envolver(txt, px, fnt, ancho):
    """Parte `txt` en líneas que quepan en `ancho` (mismas unidades que px)."""
    lineas, cur = [], ""
    for pal in txt.split():
        prueba = (cur + " " + pal).strip()
        if cur and ancho_texto(prueba, px * 4, fnt) / 4 > ancho:
            lineas.append(cur)
            cur = pal
        else:
            cur = prueba
    if cur:
        lineas.append(cur)
    return lineas


@functools.lru_cache(maxsize=300)
def _emoji(ch, px):
    """Emoji de color RGBA float32 (premultiplicado) de alto ~px."""
    f = ImageFont.truetype(EMOJI_TTF, 109)
    im = Image.new("RGBA", (190, 150), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20, 10), ch, font=f, embedded_color=True)
    bb = im.getbbox()
    if bb is None:
        return np.zeros((2, 2, 4), np.float32)
    im = im.crop(bb)
    k = px / 109.0
    im = im.resize((max(2, int(round(im.width * k))), max(2, int(round(im.height * k)))), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    a[..., :3] *= a[..., 3:4]
    return a


@functools.lru_cache(maxsize=16)
def _rejilla(w, h):
    return np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))


def _paradas(stops, u):
    """Colores (N,3) de un degradado con paradas [(pos, color), ...] evaluado en u (N,)."""
    ps = np.float32([s[0] for s in stops])
    cs = np.float32([s[1] for s in stops])
    return np.stack([np.interp(u, ps, cs[:, c]) for c in range(3)], -1).astype(np.float32)


def trazo(pts, u):
    """Los primeros `u` (0..1) de una polilínea, por longitud (para palomitas y trazos que se dibujan)."""
    pts = [tuple(p) for p in pts]
    if u >= 1:
        return pts
    segs = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(segs) * clamp(u)
    out = [pts[0]]
    for (a, b), s in zip(zip(pts, pts[1:]), segs):
        if total <= 0:
            break
        k = min(1.0, total / max(s, 1e-6))
        out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
        total -= s
    return out


# ------------------------------------------------------------------ pintor
class P:
    def __init__(self):
        self.im = np.zeros((H, W, 3), np.float32)
        self.s, self.ox, self.oy = 1.0, 0.0, 0.0
        self.rec = (0, 0, W, H)

    @contextlib.contextmanager
    def grupo(self, x=0.0, y=0.0, s=1.0):
        """Todo lo que se dibuje dentro queda escalado `s` con su origen en (x, y)."""
        ant = (self.s, self.ox, self.oy)
        self.ox, self.oy, self.s = self.ox + x * self.s, self.oy + y * self.s, self.s * s
        try:
            yield
        finally:
            self.s, self.ox, self.oy = ant

    def cam(self, z=1.0, cx=W / 2, cy=H / 2, dx=0.0, dy=0.0):
        """Cámara: zoom `z` alrededor de (cx, cy), que queda en el centro de la pantalla (más dx, dy)."""
        return self.grupo(W / 2 + dx - cx * z, H / 2 + dy - cy * z, z)

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

    def _color(self, color, hg, x0, y0, x1, y1):
        """Color sólido, o el degradado horizontal `hg=(xa, xb[, paradas[, fase]])` evaluado en el recuadro."""
        if hg is None:
            return color
        xa, xb = hg[0], hg[1]
        stops = hg[2] if len(hg) > 2 and hg[2] is not None else GRAD
        ta = self._t([(xa, 0), (xb, 0)])[:, 0]
        u = (np.arange(x0, x1, dtype=np.float32) - ta[0]) / max(float(ta[1] - ta[0]), 1.0)
        if len(hg) > 3 and hg[3] is not None:              # degradado que corre (background-position animado), en espejo
            v = (u * 0.5 + hg[3]) % 2.0
            u = np.where(v > 1, 2 - v, v)
        cols = _paradas(stops, np.clip(u, 0, 1))
        return np.broadcast_to(cols[None], (y1 - y0, x1 - x0, 3))

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
    def fondo(self, color):
        self.im[:] = np.float32(color)

    def poly(self, pts, color=None, op=1.0, hg=None, aditivo=False):
        if op <= 0.004:
            return
        a = self._t(pts)
        bb = self._bb(a)
        if bb is None:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(m, [np.round((a - (x0, y0)) * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
        self._blend(m, x0, y0, self._color(color, hg, x0, y0, x1, y1), op, aditivo)

    def rect(self, x0, y0, x1, y1, color=None, op=1.0, hg=None, aditivo=False):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, op, hg, aditivo)

    @staticmethod
    def _pts_rr(x0, y0, x1, y1, r):
        r = max(0.0, min(r, (x1 - x0) / 2, (y1 - y0) / 2))
        pts = []
        for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
            for k in range(9):
                an = math.radians(a + 90 * k / 8)
                pts.append((cx + r * math.cos(an), cy + r * math.sin(an)))
        return pts

    def rrect(self, x0, y0, x1, y1, r, color=None, op=1.0, borde=None, w=2, op_b=None, hg=None, dash=None):
        pts = self._pts_rr(x0, y0, x1, y1, r)
        if color is not None or hg is not None:
            self.poly(pts, color, op, hg)
        if borde is not None:
            self.polilinea(pts, w, borde, op if op_b is None else op_b, cerrado=True)

    def elip(self, x, y, rx, ry, color=None, op=1.0, ang=0.0, a0=0, a1=360, w=0, aditivo=False, hg=None):
        """Elipse rellena (w=0; con a0/a1 = sector) o arco de grosor w."""
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
        cv2.ellipse(m, (int(c[0]), int(c[1])), ejes, ang, a0, a1, 255, -1 if w <= 0 else max(1, int(round(w * self.s))),
                    cv2.LINE_AA, shift=4)
        self._blend(m, x0, y0, self._color(color, hg, x0, y0, x1, y1), op, aditivo)

    def circ(self, x, y, r, color=None, op=1.0, w=0, aditivo=False, hg=None):
        self.elip(x, y, r, r, color, op, w=w, aditivo=aditivo, hg=hg)

    def polilinea(self, pts, w, color, op=1.0, cerrado=False, aditivo=False, hg=None):
        if op <= 0.004 or len(pts) < 2:
            return
        a = self._t(pts)
        g = max(1, int(round(w * self.s)))
        bb = self._bb(a, pad=g + 3)
        if bb is None:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        q = np.round((a - (x0, y0)) * 16).astype(np.int32)
        cv2.polylines(m, [q], cerrado, 255, g, cv2.LINE_AA, shift=4)
        if g >= 3:                                      # puntas redondas (stroke-linecap: round)
            for e in ((q[0], q[-1]) if not cerrado else ()):
                cv2.circle(m, (int(e[0]), int(e[1])), int(g * 8), 255, -1, cv2.LINE_AA, shift=4)
        self._blend(m, x0, y0, self._color(color, hg, x0, y0, x1, y1), op, aditivo)

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

    def sombra(self, x0, y0, x1, y1, r, blur=26, op=0.55, dy=10, color=NEGRO):
        """Sombra suave de tarjeta (box-shadow 0 dy blur): rectángulo redondeado difuminado."""
        if op <= 0.004:
            return
        pad = blur * 2.2
        a = self._t([(x0 - pad, y0 - pad + dy), (x1 + pad, y1 + pad + dy)])
        bb = self._bb(a, pad=0)
        if bb is None:
            return
        bx0, by0, bx1, by1 = bb
        m = np.zeros((by1 - by0, bx1 - bx0), np.uint8)
        pts = (np.float32(self._pts_rr(x0, y0 + dy, x1, y1 + dy, r)) * self.s + (self.ox - bx0, self.oy - by0))
        cv2.fillPoly(m, [np.round(pts * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
        sg = max(1.0, blur * self.s * 0.5)
        if m.shape[0] * m.shape[1] > 250000:              # sombras grandes: difuminar a 1/4 (igual de suaves, más rápido)
            ch = cv2.resize(m, (max(1, m.shape[1] // 4), max(1, m.shape[0] // 4)), interpolation=cv2.INTER_AREA)
            ch = cv2.GaussianBlur(ch, (0, 0), max(0.6, sg / 4))
            m = cv2.resize(ch, (m.shape[1], m.shape[0]), interpolation=cv2.INTER_LINEAR)
        else:
            m = cv2.GaussianBlur(m, (0, 0), sg)
        self._blend(m, bx0, by0, color, op)

    def texto(self, txt, x, y, px, color=INK, fnt="b", op=1.0, anchor="mm", esp=0.0, hg=None, aditivo=False):
        """Texto nítido. anchor: l/m/r + t/m/b (b = línea base aproximada al pie de la caja)."""
        if op <= 0.004 or not txt:
            return
        sp = _sprite(txt, max(6, int(round(px * self.s))), fnt, esp)
        h, w = sp.shape
        c = self._t([(x, y)])[0]
        rx = int(round(c[0] - w * {"l": 0, "m": 0.5, "r": 1.0}[anchor[0]]))
        ry = int(round(c[1] - h * {"t": 0, "m": 0.5, "b": 1.0}[anchor[1]]))
        x0, y0 = max(self.rec[0], rx), max(self.rec[1], ry)
        x1, y1 = min(self.rec[2], rx + w), min(self.rec[3], ry + h)
        if x1 <= x0 or y1 <= y0:
            return
        col = color
        if hg is not None:
            col = self._color(color, hg, x0, y0, x1, y1)
        self._blend(sp[y0 - ry:y1 - ry, x0 - rx:x1 - rx], x0, y0, col, op, aditivo)

    def parrafo(self, lineas, x, y, px, lh, color=INK, fnt="s", op=1.0, anchor="l"):
        for i, ln in enumerate(lineas):
            self.texto(ln, x, y + i * lh, px, color, fnt, op, anchor + "t")

    def emoji(self, ch, x, y, px, op=1.0):
        """Emoji de color centrado en (x, y), de alto ~px."""
        if op <= 0.004:
            return
        e = _emoji(ch, max(4, int(round(px * self.s))))
        h, w = e.shape[:2]
        c = self._t([(x, y)])[0]
        rx, ry = int(round(c[0] - w / 2)), int(round(c[1] - h / 2))
        x0, y0 = max(self.rec[0], rx), max(self.rec[1], ry)
        x1, y1 = min(self.rec[2], rx + w), min(self.rec[3], ry + h)
        if x1 <= x0 or y1 <= y0:
            return
        sub = e[y0 - ry:y1 - ry, x0 - rx:x1 - rx]
        reg = self.im[y0:y1, x0:x1]
        reg *= 1 - sub[..., 3:4] * op
        reg += sub[..., :3] * op

    def oscurecer(self, op):
        """Velo de pantalla completa (el `.over` de la app: rgba(20,10,25,.72))."""
        if op > 0.003:
            self.im *= 1 - op
            self.im += np.float32(hexa("140A19")) * op


# ------------------------------------------------------------------ fondo vivo (como `.bg` de la app)
_CH = (W // 4, H // 4)


@functools.lru_cache(maxsize=1)
def _rej_chica():
    gx, gy = np.meshgrid(np.arange(_CH[0], dtype=np.float32) * 4, np.arange(_CH[1], dtype=np.float32) * 4)
    return gx, gy


def _manchas(t, dx=0.0, dy=0.0, fuerza=1.0, calida=0.0):
    """Las tres manchas difusas de la app a 1/4 de resolución (son suaves), ya escaladas a pantalla completa."""
    gx, gy = _rej_chica()
    vm = max(W, H) / 100.0                                  # 1 vmax en px
    im = np.empty((_CH[1], _CH[0], 3), np.float32)
    im[:] = np.float32(BG)
    manchas = (                                              # (centro x, centro y, radio, color, opacidad, periodo, fase)
        (10 * vm, 5 * vm, 30 * vm, O, 0.30 + 0.06 * calida, 11.0, 0.0),
        (W - 5 * vm, H - 2 * vm, 30 * vm, B, 0.30, 14.0, 2.0),
        (0.45 * W + 17.5 * vm, 0.35 * H + 17.5 * vm, 17.5 * vm, A, 0.18 + 0.08 * calida, 17.0, 4.0),
    )
    for k, (cx, cy, r, col, opa, per, fa) in enumerate(manchas):
        u = 0.5 - 0.5 * math.cos(2 * math.pi * (t + fa) / per)           # «drift» alternate
        x = cx + 8 * vm * u + dx * (0.6 + 0.2 * k)
        y = cy + 6 * vm * u * (1 if k != 1 else -1) + dy * (0.6 + 0.2 * k)
        rr = r * (1 + 0.15 * u)
        d2 = ((gx - x) ** 2 + (gy - y) ** 2) / (rr * rr)
        a = np.exp(-d2 * 1.6) * opa * fuerza
        im += a[..., None] * (np.float32(col) - im)
    return cv2.resize(im, (W, H), interpolation=cv2.INTER_LINEAR)


def _corazon(cx, cy, r, n=28):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * r / 17, cy + y * r / 17))
    return pts


def fondo_duo(p, t, dx=0.0, dy=0.0, fuerza=1.0, motas=1.0, calida=0.0):
    """Plano lejano (manchas) + plano medio (orbes dorados, corazones y destellos que suben despacio, con paralaje)."""
    p.im[:] = _manchas(t, dx * 0.15, dy * 0.15, fuerza, calida)
    if motas <= 0:
        return
    for i in range(30):
        z = 0.3 + 0.7 * rnd(i, 3)                            # 0.3 lejos .. 1 cerca
        x = (rnd(i, 1) * (W + 200) - 100 + dx * 0.35 * z + 14 * math.sin(t * 0.5 + i)) % (W + 200) - 100
        y = (rnd(i, 2) * (H + 300) - t * (14 + 40 * z) + dy * 0.35 * z) % (H + 300) - 150
        tw = 0.6 + 0.4 * math.sin(t * (1.1 + 1.7 * rnd(i, 5)) + i)
        tipo = i % 3
        if tipo == 0:                                        # orbe dorado (el `.orb` de la app)
            p.glow(x, y, 10 + 22 * z, GOLD, 0.30 * z * tw * motas, 1.7)
            p.circ(x, y, 2 + 3 * z, (1, 0.93, 0.8), 0.55 * z * tw * motas)
        elif tipo == 1:                                      # corazoncito
            col = (A, B, O)[i % 3]
            p.poly(_corazon(x, y, 7 + 12 * z), col, 0.22 * z * tw * motas)
        else:                                                # destello de 4 puntas
            r = 6 + 12 * z
            q = r * 0.22
            p.poly([(x, y - r), (x + q, y - q), (x + r, y), (x + q, y + q), (x, y + r), (x - q, y + q), (x - r, y), (x - q, y - q)],
                   (1, 0.95, 0.98), 0.30 * z * tw * motas)


@functools.lru_cache(maxsize=1)
def _vineta():
    gx, gy = _rejilla(W, H)
    d = np.sqrt(((gx - W / 2) / (W * 0.80)) ** 2 + ((gy - H / 2) / (H * 0.70)) ** 2)
    return (1 - 0.40 * np.clip(d - 0.40, 0, 1) ** 1.5)[..., None].astype(np.float32)


def acabado(im, t, flash=0.0, bloom=1.0, sacudida=0.0):
    """Brillo suave en lo luminoso (los box-shadow de color de la app) + viñeta leve. Limpio: sin grano ni barrido."""
    ch = cv2.resize(im, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    luz = np.clip(ch - 0.62, 0, None)
    b = cv2.GaussianBlur(luz, (0, 0), 6) * 0.45 + cv2.GaussianBlur(luz, (0, 0), 22) * 0.45
    im = im + cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR) * bloom
    if sacudida > 0.01:
        k = int(t * 30)
        dx, dy = (rnd(k, 1) - 0.5) * 24 * sacudida, (rnd(k, 2) - 0.5) * 24 * sacudida
        M = np.float32([[1 + 0.015 * sacudida, 0, dx - W * 0.0075 * sacudida], [0, 1 + 0.015 * sacudida, dy - H * 0.0075 * sacudida]])
        im = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    im = im * _vineta()
    if flash > 0.003:
        im = im + flash
    return np.clip(im, 0, 1).astype(np.float32)


# ------------------------------------------------------------------ componentes de la app (px CSS; dibujar dentro de p.grupo)
def tarjeta(p, x0, y0, x1, y1, r=22, op=1.0, sombra=True, borde=LINE, color=CARD):
    if sombra:
        p.sombra(x0, y0, x1, y1, r, blur=30, op=0.6 * op, dy=10)
    p.rrect(x0, y0, x1, y1, r, color, op, borde=borde, w=1.5, op_b=op)


def pill(p, txt, x, y, color, fondo, px=12, op=1.0, anchor="l", emo=None, fnt="x"):
    """Pastilla (`.pill`): devuelve su ancho. (x, y) = borde izquierdo (o derecho/centro según anchor), centro vertical."""
    ancho = ancho_texto(txt, px, fnt) + (px * 1.35 if emo else 0) + 20
    x0 = x if anchor == "l" else (x - ancho if anchor == "r" else x - ancho / 2)
    h = px + 10
    p.rrect(x0, y - h / 2, x0 + ancho, y + h / 2, h / 2, fondo, op)
    tx = x0 + 10
    if emo:
        p.emoji(emo, tx + px * 0.55, y, px * 1.05, op)
        tx += px * 1.35
    p.texto(txt, tx, y + px * 0.04, px, color, fnt, op, "lm")
    return ancho


def tag(p, txt, x, y, color=MUT, fondo=LINE, px=11, op=1.0, chk=False):
    """`.tag` de la tarjeta de misión (chk = con palomita «✓» dibujada): devuelve su ancho."""
    ancho = ancho_texto(txt, px, "b") + 16 + (13 if chk else 0)
    p.rrect(x, y - 9.5, x + ancho, y + 9.5, 8, fondo, op)
    if chk:
        palomita(p, x + 13, y + 0.5, 7, 1.0, op, w=1.8, color=color)
    p.texto(txt, x + 8 + (13 if chk else 0), y + 0.5, px, color, "b", op, "lm")
    return ancho


def avatar(p, x, y, letra, color, r=19, op=1.0, borde=BG, w=2.5):
    if borde is not None:
        p.circ(x, y, r + w, borde, op)
    p.circ(x, y, r, color, op)
    if letra:
        p.texto(letra, x, y + r * 0.04, r * 0.8, BLANCO, "x", op)


def palomita(p, x, y, r, u, op=1.0, w=3.5, color=BLANCO):
    """La palomita de `.chk svg` (path M5 12.5l4.5 4.5L19 7 en un viewBox de 24) dibujándose hasta `u`."""
    if u <= 0:
        return
    k = r * 0.9 / 12
    pts = [(x + (5 - 12) * k, y + (12.5 - 12) * k), (x + (9.5 - 12) * k, y + (17 - 12) * k), (x + (19 - 12) * k, y + (7 - 12) * k)]
    p.polilinea(trazo(pts, u), w, color, op)


def check(p, x, y, t, t_on, op=1.0, r=22):
    """`.chk` 44px: anillo gris; al completarse se llena del degradado (pop) y se dibuja la palomita."""
    if t < t_on:
        p.circ(x, y, r - 1.25, LINE, op, w=2.5)
        return
    s = 0.6 + 0.4 * pop(t, t_on, 0.30) if t < t_on + 0.6 else 1.0
    with p.pivote(x, y, s):
        p.sombra(x - r, y - r, x + r, y + r, r, blur=16, op=0.55 * op, dy=6, color=A)
        p.circ(x, y, r, op=op, hg=(x - r, x + r))
    palomita(p, x, y, r, e_out(pr(t, t_on + 0.1, t_on + 0.45)), op)


def corazon_btn(p, x, y, t, t_on, op=1.0, r=22):
    """`.heart`: anillo gris con ♥; al darle «me encantó» se llena del degradado con pop."""
    if t < t_on:
        p.circ(x, y, r - 1.25, LINE, op, w=2.5)
        p.poly(_corazon(x, y + 1, 9), MUT, op)
        return
    s = 0.6 + 0.4 * pop(t, t_on, 0.30) if t < t_on + 0.6 else 1.0
    with p.pivote(x, y, s):
        p.sombra(x - r, y - r, x + r, y + r, r, blur=16, op=0.55 * op, dy=6, color=A)
        p.circ(x, y, r, op=op, hg=(x - r, x + r))
        p.poly(_corazon(x, y + 1, 10), BLANCO, op)


MISIONES = {    # textos reales de la app (index.html)
    "tie1": ("⏳", "Cenen juntos sin pantallas: celulares lejos de la mesa.", "duo"),
    "afe2": ("💝", "Dense un abrazo de 20 segundos completos. Cuéntenlos.", "duo"),
    "div2": ("🎲", "Bailen una canción completa en la sala.", "duo"),
    "afe1": ("💝", "Deja una notita cariñosa donde tu pareja la encuentre.", "solo"),
    "equ1": ("🤝", "Haz una tarea de la casa que normalmente le toca a tu pareja.", "solo"),
    "afe20": ("💝", "Prepárale una bebida caliente o una bolsa térmica sin que te la pida.", "solo"),
    "com8": ("💬", "Agradécele algo concreto que hizo por ti esta semana.", "solo"),
}


def mision(p, x0, y0, mid, t, t_check=None, op=1.0, t_like=None, hecha_por=None, ancho=364):
    """Tarjeta `.m` (devuelve su alto). t_check = cuándo se marca; hecha_por = versión `.got` (con botón de corazón)."""
    emo, txt, tipo = MISIONES[mid]
    x1 = x0 + ancho
    lineas = envolver(txt, 15, "s", ancho - 28 - 46 - 14 - 44 - 14)
    alto = 14 + max(46, len(lineas) * 21 + 8 + 19) + 14
    hecho = t_check is not None and t >= t_check
    s = squish(t, t_check) if t_check is not None else 1.0
    with p.pivote(x0 + ancho / 2, y0 + alto / 2, s):
        tarjeta(p, x0, y0, x1, y0 + alto, 20, op, sombra=hecha_por is None)
        if t_check is not None and t_check <= t <= t_check + 0.8:          # barrido dorado (`.m.pop:after`)
            u = (t - t_check) / 0.8
            cx = x0 + (-0.5 + 1.7 * u) * ancho
            with p.clip(x0, y0, x1, y0 + alto):
                p.poly([(cx - 70, y0 + alto), (cx + 20, y0), (cx + 120, y0), (cx + 30, y0 + alto)], GOLD, 0.26 * op * math.sin(math.pi * u))
        p.rrect(x0 + 14, y0 + alto / 2 - 23, x0 + 60, y0 + alto / 2 + 23, 14, sobre(B, CARD, 0.10), op)
        p.emoji(emo, x0 + 37, y0 + alto / 2, 22, op)
        tx = x0 + 74
        ty = y0 + alto / 2 - (len(lineas) * 21 + 8 + 19) / 2
        col_txt = mix(INK, MUT, smooth(pr(t, t_check + 0.2, t_check + 0.6))) if hecho and hecha_por is None else INK
        p.parrafo(lineas, tx, ty - 1, 15, 21, col_txt, "s", op)
        if hecho and hecha_por is None:                          # tachado (text-decoration: line-through)
            u = e_out(pr(t, t_check + 0.15, t_check + 0.55))
            for i, ln in enumerate(lineas):
                wl = ancho_texto(ln, 15, "s")
                yy = ty + i * 21 + 11
                p.linea((tx, yy), (tx + wl * u, yy), 1.5, MUT, 0.6 * op)
        yt = ty + len(lineas) * 21 + 8 + 9.5
        if hecha_por is not None:
            wx = tag(p, f"Hecha por {hecha_por}", tx, yt, OK, sobre(OK, CARD, 0.14), op=op, chk=True)
            if t_like is not None and t >= t_like:
                tag(p, "+5 XP", tx + wx + 6, yt, hexa("C9821A"), sobre(GOLD, CARD, 0.2), op=op * smooth(pr(t, t_like, t_like + 0.2)))
            corazon_btn(p, x1 - 36, y0 + alto / 2, t, t_like if t_like is not None else 1e9, op)
        else:
            wx = tag(p, "Juntos · tú propones" if tipo == "duo" else "Para tu pareja", tx, yt, op=op)
            tag(p, f"+{25 if tipo == 'duo' else 15} XP", tx + wx + 6, yt, hexa("C9821A"), sobre(GOLD, CARD, 0.2), op=op)
            check(p, x1 - 36, y0 + alto / 2, t, t_check if t_check is not None else 1e9, op)
    return alto


def barra_xp(p, x0, y0, x1, frac, t, op=1.0, llena=0.0, h=26):
    """`.xp`: canal gris, relleno con el degradado que corre + brillo que pasa + marcas cada 10 %; dorada al llenarse."""
    r = h / 2
    p.rrect(x0, y0, x1, y0 + h, r, LINE, op)
    p.rrect(x0, y0 + 1, x1, y0 + 4, 2, NEGRO, 0.10 * op)                 # inset shadow
    fx = x0 + (x1 - x0) * clamp(frac)
    if fx - x0 > 2:
        p.sombra(x0, y0, fx, y0 + h, r, blur=18, op=0.55 * op * (1 - llena), dy=0, color=A)
        if llena > 0:
            p.sombra(x0, y0, fx, y0 + h, r, blur=24, op=0.8 * op * llena, dy=0, color=GOLD)
        fase = (t / 4.0) % 2.0
        p.rrect(x0, y0, max(fx, x0 + h), y0 + h, r, op=op, hg=(x0, x1, GRAD, fase))
        if llena > 0:
            p.rrect(x0, y0, max(fx, x0 + h), y0 + h, r, op=op * llena, hg=(x0, x1, GRAD_ORO, fase))
        sx = x0 - 60 + ((t % 2.6) / 2.6) * (fx - x0 + 120)                 # `.xpfill:after` (shine)
        with p.clip(x0, y0, fx, y0 + h):
            for k in range(6):
                p.rect(sx + k * 10, y0, sx + k * 10 + 10, y0 + h, BLANCO, 0.10 * math.sin(math.pi * (k + 0.5) / 6) * op)
    for k in range(1, 10):                                                 # `.ticks`
        xx = x0 + (x1 - x0) * k / 10
        p.rect(xx - 0.75, y0, xx + 0.75, y0 + h, BLANCO, 0.13 * op)


def anillo_dia(p, x, y, frac, letra, op=1.0, hoy=False, futuro=False, lleno_t=None, t=0.0):
    """`.wd i`: anillo con avance cónico (var(--a)) y letra debajo; al 100 % se llena del degradado con ✓."""
    o = op * (0.45 if futuro else 1.0)
    if hoy:
        p.circ(x, y, 19, A, o, w=2)
    if frac >= 1:
        s = 0.6 + 0.4 * pop(t, lleno_t, 0.3) if lleno_t is not None and t < lleno_t + 0.6 else 1.0
        with p.pivote(x, y, s):
            p.circ(x, y, 15, op=o, hg=(x - 15, x + 15))
            palomita(p, x, y, 13, 1.0, o, w=2.6)
    else:
        p.circ(x, y, 15, LINE, o)
        if frac > 0:
            p.elip(x, y, 15, 15, A, o, a0=-90, a1=-90 + 360 * frac)
        p.circ(x, y, 11, CARD, o)
    p.texto(letra, x, y + 28, 11, INK if hoy else MUT, "b", o)


def tarjeta_xp(p, x0, y0, t, xp, nivel=3, racha=4, dias=(), por=(0, 0), op=1.0, llena=0.0, ancho=364, nombres=("Ana", "Leo"),
               hoy=2, lleno_t=None, nivel_pop=None):
    """La tarjeta grande de la semana (home): pills, número, barra, mensaje, aportes de cada quien y los 7 días."""
    x1 = x0 + ancho
    alto = 232
    tarjeta(p, x0, y0, x1, y0 + alto, 22, op)
    s = 1.0 + 0.25 * golpe(t, nivel_pop, 0.5) if nivel_pop is not None else 1.0
    wn = ancho_texto(f"Nivel {nivel}", 12, "x") + 20
    with p.pivote(x0 + 18 + wn / 2, y0 + 32, s):
        w1 = pill(p, f"Nivel {nivel}", x0 + 18, y0 + 32, B if llena < 1 else GOLD, sobre(B, CARD, 0.14), op=op)
    pill(p, f"{racha} días", x0 + 18 + w1 + 8, y0 + 32, FIRE, sobre(O, CARD, 0.16), op=op, emo="🔥")
    xr = x1 - 18
    p.texto(f" / 450 XP", xr, y0 + 33, 13, MUT, "s", op, "rm")
    wv = ancho_texto(" / 450 XP", 13, "s")
    p.texto(str(int(round(xp))), xr - wv, y0 + 31, 20, INK if llena < 1 else GOLD, "x", op, "rm")
    barra_xp(p, x0 + 18, y0 + 58, x1 - 18, xp / 450.0, t, op, llena)
    if llena >= 1 or xp >= 449.5:
        p.emoji("🏆", x0 + 28, y0 + 104, 14, op)
        extra = int(round(xp - 450))
        msg = f"¡Meta cumplida! Llevan +{extra} XP extra esta semana." if extra > 0 else "¡Meta cumplida! Subieron de nivel."
        p.texto(msg, x0 + 40, y0 + 104, 13, INK, "s", op, "lm")
    else:
        quedan = 7 - hoy
        cola = "último día" if quedan <= 1 else f"quedan {quedan} días"
        p.texto(f"Faltan {int(round(450 - xp))} XP para llenar la barra · {cola}.", x0 + 20, y0 + 104, 13, MUT, "m", op, "lm")
    cy = y0 + 132
    avatar(p, x0 + 28, cy, "", AV_A, 10, op, None)
    p.texto(f"{nombres[0]} {int(round(por[0]))} XP", x0 + 44, cy + 0.5, 12, MUT, "b", op, "lm")
    xb = x0 + 44 + ancho_texto(f"{nombres[0]} {int(round(por[0]))} XP", 12, "b") + 22
    avatar(p, xb, cy, "", AV_L, 10, op, None)
    p.texto(f"{nombres[1]} {int(round(por[1]))} XP", xb + 16, cy + 0.5, 12, MUT, "b", op, "lm")
    p.rect(x0 + 18, y0 + 150, x1 - 18, y0 + 151.5, LINE, op)
    for i, l in enumerate("LMXJVSD"):
        xx = x0 + 18 + 15 + i * (ancho - 36 - 30) / 6
        f = dias[i] if i < len(dias) else 0.0
        lt = lleno_t[i] if isinstance(lleno_t, (list, tuple)) and i < len(lleno_t) else None
        anillo_dia(p, xx, y0 + 182, f, l, op, hoy=i == hoy, futuro=i > hoy, lleno_t=lt, t=t)
    return alto, (x0 + 18, y0 + 58, x1 - 18, y0 + 84), (x0 + 28, cy), (xb, cy)


def encabezado(p, nombre, sub, t, op=1.0, otro="L", c_yo=AV_A, c_otro=AV_L, ancho=400):
    p.texto(sub, 18, 62, 13, MUT, "s", op, "lm")
    p.texto(f"Hola, {nombre}", 18, 92, 26, INK, "x", op, "lm")
    avatar(p, ancho - 18 - 19 - 28, 80, nombre[0], c_yo, 19, op)
    avatar(p, ancho - 18 - 19, 80, otro, c_otro, 19, op)


def h2(p, txt, y, op=1.0, small=None, ancho=400):
    p.texto(txt, 22, y, 15, INK, "b", op, "lm")
    if small:
        p.texto(small, ancho - 22, y + 1, 12, MUT, "s", op, "rm")


def pestanas(p, activa, t, op=1.0, ancho=400, alto=860, t_cambio=None, de=None):
    """Barra inferior `.tabs` (Misiones · Ciclo · Nosotros · 💬). `activa` puede deslizarse de `de` a `activa` desde t_cambio."""
    nombres = ["Misiones", "Ciclo", "Nosotros", "💬"]
    pads = [15, 15, 15, 14]
    ws = [ancho_texto(n, 14, "b") + 2 * pd if n != "💬" else 46 for n, pd in zip(nombres, pads)]
    tot = sum(ws) + 4 * 3 + 12
    x0 = ancho / 2 - tot / 2
    y0 = alto - 14 - 54
    p.sombra(x0, y0, x0 + tot, y0 + 54, 24, blur=30, op=0.6 * op, dy=10)
    p.rrect(x0, y0, x0 + tot, y0 + 54, 24, sobre(CARD, BG, 0.85), op, borde=LINE, w=1.5)
    xs = []
    x = x0 + 6
    for w_ in ws:
        xs.append((x, x + w_))
        x += w_ + 4
    ia = nombres.index(activa)
    if t_cambio is not None and de is not None and t < t_cambio + 0.35:
        u = e_out(pr(t, t_cambio, t_cambio + 0.35))
        ib = nombres.index(de)
        ax0, ax1 = lerp(xs[ib][0], xs[ia][0], u), lerp(xs[ib][1], xs[ia][1], u)
    else:
        ax0, ax1 = xs[ia]
    p.rrect(ax0, y0 + 6, ax1, y0 + 48, 18, op=op, hg=(ax0, ax1))
    for (a, b_), n in zip(xs, nombres):
        if n == "💬":
            p.emoji(n, (a + b_) / 2, y0 + 27, 16, op)
            continue
        dentro = ax0 - 2 <= (a + b_) / 2 <= ax1 + 2
        p.texto(n, (a + b_) / 2, y0 + 27, 14, BLANCO if dentro else MUT, "b", op)


def calendario(p, x0, y0, t, op=1.0, ancho=364, hoy=13, periodo=(12, 13), estimado=(14, 15, 16), fertil=range(22, 28), ovu=27,
               pulso=None):
    """Tarjeta del calendario del ciclo (octubre de 2026: empieza en jueves)."""
    x1 = x0 + ancho
    alto = 352
    tarjeta(p, x0, y0, x1, y0 + alto, 22, op)
    p.rrect(x0 + 18, y0 + 16, x0 + 54, y0 + 52, 12, None, op, borde=LINE, w=1.5)
    p.texto("←", x0 + 36, y0 + 34, 16, INK, "b", op)
    p.rrect(x1 - 54, y0 + 16, x1 - 18, y0 + 52, 12, None, op, borde=LINE, w=1.5)
    p.texto("→", x1 - 36, y0 + 34, 16, INK, "b", op)
    p.texto("Octubre de 2026", (x0 + x1) / 2, y0 + 34, 16, INK, "x", op)
    cw = (ancho - 36) / 7
    for i, l in enumerate("LMXJVSD"):
        p.texto(l, x0 + 18 + cw * (i + 0.5), y0 + 72, 11, MUT, "b", op)
    off = 3                                                    # 1-oct-2026 es jueves
    for d in range(1, 32):
        k = d - 1 + off
        cx = x0 + 18 + cw * (k % 7 + 0.5)
        cy = y0 + 104 + (k // 7) * (cw * 0.98)
        r = cw / 2 - 3
        col_txt = MUT if d > hoy else INK
        fnt = "s"
        if d in fertil:
            p.circ(cx, cy, r, sobre(B, CARD, 0.35 if d == ovu else 0.14), op)
            fnt = "x" if d == ovu else "s"
        if d in periodo:
            s = 1.0 + (0.12 * math.sin((t - pulso) * 7) * math.exp(-(t - pulso) * 1.2) if pulso is not None and t > pulso else 0.0)
            with p.pivote(cx, cy, s):
                p.circ(cx, cy, r, A, op)
            col_txt, fnt = BLANCO, "x"
            p.circ(cx, cy + r - 6, 2.5, BLANCO, op)
        elif d in estimado:
            n = 16
            for j in range(n):                                  # borde punteado (`.pred`)
                if j % 2 == 0:
                    a0 = 360 * j / n
                    p.elip(cx, cy, r - 1, r - 1, A, op, a0=a0, a1=a0 + 360 / n, w=2)
        if d == hoy:
            p.circ(cx, cy, r + 3.5, INK, op, w=2)
        p.texto(str(d), cx, cy, 14, col_txt, fnt, op)
    ly = y0 + alto - 22
    lx = x0 + 20
    for etq, col, tipo in (("Periodo", A, 0), ("Estimado", A, 1), ("Ventana fértil", sobre(B, CARD, 0.35), 0)):
        if tipo:
            p.circ(lx + 5, ly, 4.5, A, op, w=1.6)
        else:
            p.circ(lx + 5, ly, 5, col, op)
        p.texto(etq, lx + 15, ly + 0.5, 11, MUT, "s", op, "lm")
        lx += 15 + ancho_texto(etq, 11, "s") + 16
    return alto


def boton(p, txt, x0, y0, x1, h=54, op=1.0, px=16, emo=None):
    """`.btn` con el degradado de la marca y su sombra de color."""
    p.sombra(x0, y0, x1, y0 + h, 16, blur=24, op=0.7 * op, dy=10, color=A)
    p.rrect(x0, y0, x1, y0 + h, 16, op=op, hg=(x0, x1))
    if emo:
        wt = ancho_texto(txt, px, "b")
        p.emoji(emo, (x0 + x1) / 2 - wt / 2 - px * 0.2, y0 + h / 2, px * 1.1, op)
        p.texto(txt, (x0 + x1) / 2 + px * 0.6, y0 + h / 2 + 0.5, px, BLANCO, "b", op)
    else:
        p.texto(txt, (x0 + x1) / 2, y0 + h / 2 + 0.5, px, BLANCO, "b", op)


def toast(p, txt, cx, y, op=1.0, px=14, emo=None):
    """`.toast` (modo oscuro: fondo claro var(--ink), texto oscuro)."""
    wt = ancho_texto(txt, px, "s") + (px * 1.5 if emo else 0)
    x0, x1 = cx - wt / 2 - 18, cx + wt / 2 + 18
    h = px + 26
    p.sombra(x0, y, x1, y + h, 16, blur=26, op=0.6 * op, dy=10)
    p.rrect(x0, y, x1, y + h, 16, INK, op)
    tx = x0 + 18
    p.texto(txt, tx, y + h / 2 + 0.5, px, BG, "s", op, "lm")
    if emo:
        p.emoji(emo, x1 - 18 - px * 0.6, y + h / 2, px * 1.1, op)


def logo(p, cx, cy, r, t, op=1.0, sep=None, respira=True):
    """Logo: dos círculos (coral y violeta) que se mezclan en «screen» (modo oscuro) y respiran (duoL/duoR)."""
    d = r * 0.88 if sep is None else sep
    if respira:
        d -= r * 0.11 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 3.2))
    xa, xb = cx - d / 2, cx + d / 2
    p.circ(xa, cy, r, AV_A, op)
    p.circ(xb, cy, r, AV_L, op)
    if d < 2 * r:                                            # intersección (lente) con el color «screen»
        a = math.acos(clamp(d / (2 * r), -1, 1))
        n = 40
        pts = [(xa + r * math.cos(-a + 2 * a * k / n), cy + r * math.sin(-a + 2 * a * k / n)) for k in range(n + 1)]
        pts += [(xb + r * math.cos(math.pi - a + 2 * a * k / n), cy + r * math.sin(math.pi - a + 2 * a * k / n)) for k in range(n + 1)]
        p.poly(pts, LOGO_MEZCLA, op)


def burst(p, x, y, t, t0, n=36, fuerza=1.0, semilla=0, dur=1.6, escala=1.0):
    """Confeti de la app (`burst`: 5 colores, cuadritos y círculos que giran, con gravedad y freno)."""
    if t < t0 or t > t0 + dur:
        return
    tau = t - t0
    cols = (O, A, B, GOLD, OK)
    for i in range(n):
        a = rnd(i, semilla + 1) * 2 * math.pi
        v = (0.4 + rnd(i, semilla + 2)) * 900 * fuerza * escala
        vx, vy = math.cos(a) * v, math.sin(a) * v - 420 * fuerza * escala
        fr = (1 - math.exp(-2.2 * tau)) / 2.2
        px_ = x + vx * fr
        py_ = y + vy * fr + 0.5 * 1500 * escala * tau * tau * 0.6
        life = 1 - tau / dur
        r = (5 + rnd(i, semilla + 3) * 7) * escala
        col = cols[i % 5]
        if rnd(i, semilla + 4) < 0.5:
            ang = rnd(i, semilla + 5) * 6 + tau * (4 + 6 * rnd(i, semilla + 6))
            ca, sa = math.cos(ang), math.sin(ang)
            pts = [(px_ + ca * dx - sa * dy, py_ + sa * dx + ca * dy) for dx, dy in ((-r, -r * 0.6), (r, -r * 0.6), (r, r * 0.6), (-r, r * 0.6))]
            p.poly(pts, col, clamp(life * 1.4))
        else:
            p.circ(px_, py_, r * 0.7, col, clamp(life * 1.4))


def orbe(p, x, y, op=1.0, r=12):
    """`.orb`: bolita de luz dorada (blanco al centro)."""
    p.glow(x, y, r * 2.6, GOLD, 0.9 * op, 1.6)
    p.circ(x, y, r * 0.55, (1.0, 0.95, 0.85), op)


def vuelo(t, t0, dur, a, b, curva=-160):
    """Posición de algo que vuela de a a b en arco (u 0..1 con e_io). None si no está en vuelo."""
    if t < t0 or t > t0 + dur:
        return None
    u = e_io((t - t0) / dur)
    x = lerp(a[0], b[0], u)
    y = lerp(a[1], b[1], u) + curva * math.sin(math.pi * u)
    return x, y, u


def float_xp(p, txt, x, y, t, t0, px=20, op=1.0):
    """`.floatxp`: +N XP dorado que sube y se desvanece (1,1 s)."""
    if t < t0 or t > t0 + 1.25:
        return
    u = (t - t0) / 1.25
    if u < 0.2:
        a, dy, s = u / 0.2, -14 * u / 0.2, 0.6 + 0.55 * u / 0.2
    else:
        k = (u - 0.2) / 0.8
        a, dy, s = 1 - k, -14 - 76 * k, 1.15 - 0.15 * k
    p.texto(txt, x + 2, y + dy + 3, px * s, NEGRO, "x", a * 0.35 * op)
    p.texto(txt, x, y + dy, px * s, GOLD, "x", a * op)


# ------------------------------------------------------------------ teléfono
TEL_W, TEL_H = 400, 860            # pantalla en px CSS


def telefono(p, cx, cy, k, t, contenido, op=1.0, hora="9:41"):
    """Teléfono centrado en (cx, cy) con su pantalla a escala k; `contenido(p, t)` dibuja la app en px CSS (0..400 x 0..860)."""
    x0, y0 = cx - TEL_W * k / 2, cy - TEL_H * k / 2
    with p.grupo(x0, y0, k):
        p.sombra(-14, -14, TEL_W + 14, TEL_H + 14, 64, blur=50, op=0.75 * op, dy=26)
        p.rrect(-14, -14, TEL_W + 14, TEL_H + 14, 64, CUERPO, op, borde=hexa("3A3042"), w=2.5)
        p.rrect(-11, -11, TEL_W + 11, TEL_H + 11, 61, None, op, borde=hexa("1E1824"), w=2)
        p.rrect(0, 0, TEL_W, TEL_H, 52, BG, op)
        with p.clip(0, 0, TEL_W, TEL_H):
            ant = p.im.copy() if op < 1 else None
            contenido(p, t)
            if ant is not None:
                p.im[:] = ant + (p.im - ant) * op
        _esquinas(p, 0, 0, TEL_W, TEL_H, 52, CUERPO, op)
        p.rrect(150, 11, 250, 41, 15, NEGRO, op)                 # isla
        p.texto(hora, 52, 27, 15, INK, "b", op)
        p.rrect(336, 20, 360, 32, 4, None, op, borde=INK, w=1.5)  # batería
        p.rrect(338.5, 22.5, 354, 29.5, 2, INK, op)
        for i in range(4):
            p.rect(306 + i * 5, 31 - (i + 1) * 2.6, 309 + i * 5, 31, INK, op)


def _esquinas(p, x0, y0, x1, y1, r, color, op=1.0):
    """Tapa lo que el contenido dibuje fuera de las esquinas redondeadas de la pantalla."""
    for cx, cy, sx, sy in ((x0 + r, y0 + r, -1, -1), (x1 - r, y0 + r, 1, -1), (x1 - r, y1 - r, 1, 1), (x0 + r, y1 - r, -1, 1)):
        ah = 0.0 if sx > 0 else math.pi
        av = math.pi / 2 if sy > 0 else -math.pi / 2
        d = (av - ah + math.pi) % (2 * math.pi) - math.pi          # barrido corto de 90 grados
        e = r + 3
        pts = [(cx + sx * e, cy)]
        pts += [(cx + r * math.cos(ah + d * k / 12), cy + r * math.sin(ah + d * k / 12)) for k in range(13)]
        pts += [(cx, cy + sy * e), (cx + sx * e, cy + sy * e)]
        p.poly(pts, color, op)


def fondo_app(p, t, ancho=TEL_W, alto=TEL_H):
    """El `.bg` de la app dentro de la pantalla del teléfono (manchas más chicas)."""
    p.rect(0, 0, ancho, alto, BG)
    vm = 8.6
    u = 0.5 - 0.5 * math.cos(2 * math.pi * t / 9)
    p.glow(40 + 30 * u, 30 + 20 * u, 300, sobre(O, BG, 0.5), 0.28, 1.3)
    p.glow(ancho - 20 - 20 * u, alto - 30, 360, sobre(B, BG, 0.5), 0.30, 1.3)
    p.glow(0.6 * ancho, 0.5 * alto, 180, sobre(A, BG, 0.5), 0.10, 1.3)
