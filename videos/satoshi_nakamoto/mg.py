# -*- coding: utf-8 -*-
"""Motion graphics dibujados (siluetas, objetos, ambientes) para el documental. TODO es procedural: nada de metraje reciclado.

Se pinta a media resolución (960x540) sobre un lienzo float32 y se escala al final: es 4x más rápido y el filtro de película (`docu_fx.cine`)
ya suaviza y da grano, así que no se nota. Las coordenadas que recibe cada función son SIEMPRE las del cuadro final (1920x1080).

    p = P()                          # lienzo vacío
    p.fondo((0.02, .03, .07), (0.10, .12, .20))
    persona(p, 900, 900, 420, pose_caminar(t * 2.0), COL_SIL)
    p.fin(lz)                        # escala a 1920x1080 y lo copia en `lz`
"""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

import docu as D
from motor import H, W

K = 0.5
HW, HH = int(W * K), int(H * K)

# paleta del documental: noche azul, luz cálida, rojo de tinta
SIL = (0.012, 0.016, 0.026)           # silueta
SIL2 = (0.030, 0.040, 0.060)          # silueta lejana
AZUL = (0.10, 0.20, 0.34)
AZUL_OSC = (0.025, 0.045, 0.085)
TEAL = (0.10, 0.36, 0.42)
CALIDO = (1.00, 0.72, 0.36)
LUZ = (1.00, 0.93, 0.78)
ROJO = (0.86, 0.10, 0.10)
CREMA = (0.93, 0.90, 0.82)
AMAR = (0.95, 0.88, 0.20)
GRIS = (0.45, 0.47, 0.52)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = clamp(x)
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2


def lerp(a, b, u):
    return a + (b - a) * u


def mix(c0, c1, u):
    return tuple(lerp(a, b, u) for a, b in zip(c0, c1))


def pr(t, a, b):
    return clamp((t - a) / max(b - a, 1e-6))


@functools.lru_cache(maxsize=8)
def _grid_roi(w, h):
    return np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))


class P:
    """Pintor a media resolución. Todo se mezcla con máscaras uint8 en recuadros pequeños (solo se toca lo que se dibuja)."""

    def __init__(self):
        self.im = np.zeros((HH, HW, 3), np.float32)

    # ---------------------------------------------------------------- base
    def fondo(self, top, bot=None, y0=0.0, y1=1.0):
        bot = top if bot is None else bot
        ys = np.clip((np.arange(HH, dtype=np.float32) / HH - y0) / max(y1 - y0, 1e-6), 0, 1)[:, None, None]
        self.im[:] = np.float32(top) * (1 - ys) + np.float32(bot) * ys

    def _blend(self, m, rx, ry, color, op=1.0, aditivo=False):
        h, w = m.shape
        reg = self.im[ry:ry + h, rx:rx + w]
        a = m.astype(np.float32) * (op / 255.0)
        if isinstance(color, np.ndarray):
            col = color
        else:
            col = np.float32(color)
        if aditivo:
            reg += a[..., None] * col
        else:
            reg *= (1 - a)[..., None]
            reg += a[..., None] * col

    def _bb(self, pts, pad=3):
        a = np.asarray(pts, np.float32) * K
        x0, y0 = np.floor(a.min(0)).astype(int) - pad
        x1, y1 = np.ceil(a.max(0)).astype(int) + pad
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(HW, x1), min(HH, y1)
        if x1 <= x0 or y1 <= y0:
            return None
        return x0, y0, x1, y1

    def _fx(self, pts, rx, ry):
        return np.round((np.asarray(pts, np.float32) * K - (rx, ry)) * 16).astype(np.int32)

    # ---------------------------------------------------------------- formas
    def poly(self, pts, color, op=1.0, grad=None):
        """Polígono relleno. `grad` = (color_arriba, color_abajo) sustituye a `color` con degradado vertical dentro del recuadro."""
        bb = self._bb(pts)
        if bb is None or op <= 0.003:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(m, [self._fx(pts, x0, y0)], 255, cv2.LINE_AA, shift=4)
        if grad is not None:
            t = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
            color = np.float32(grad[0]) * (1 - t) + np.float32(grad[1]) * t
            color = np.broadcast_to(color, (y1 - y0, x1 - x0, 3))
        self._blend(m, x0, y0, color, op)

    def circ(self, x, y, r, color, op=1.0, grad=None):
        self.elip(x, y, r, r, 0, color, op, grad)

    def elip(self, x, y, rx, ry, ang=0.0, color=SIL, op=1.0, grad=None, a0=0, a1=360):
        m_ = max(rx, ry)
        bb = self._bb([(x - m_, y - m_), (x + m_, y + m_)])
        if bb is None or op <= 0.003:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        c = np.array([x * K - x0, y * K - y0]) * 16
        cv2.ellipse(m, (int(c[0]), int(c[1])), (max(1, int(rx * K * 16)), max(1, int(ry * K * 16))), ang, a0, a1, 255, -1, cv2.LINE_AA, shift=4)
        if grad is not None:
            t = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
            color = np.broadcast_to(np.float32(grad[0]) * (1 - t) + np.float32(grad[1]) * t, (y1 - y0, x1 - x0, 3))
        self._blend(m, x0, y0, color, op)

    def linea(self, p0, p1, w, color=SIL, op=1.0, caps=True):
        self.polilinea([p0, p1], w, color, op, caps=caps)

    def polilinea(self, pts, w, color=SIL, op=1.0, cerrado=False, caps=True):
        bb = self._bb(pts, pad=int(w * K) + 3)
        if bb is None or op <= 0.003:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        f = self._fx(pts, x0, y0)
        cv2.polylines(m, [f], cerrado, 255, max(1, int(round(w * K))), cv2.LINE_AA, shift=4)
        if caps:
            for q in f[[0, -1]] if not cerrado else []:
                cv2.circle(m, (int(q[0]), int(q[1])), int(w * K * 8), 255, -1, cv2.LINE_AA, shift=4)
        self._blend(m, x0, y0, color, op)

    def rect(self, x0, y0, x1, y1, color=SIL, op=1.0, grad=None):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, op, grad)

    def rrect(self, x0, y0, x1, y1, r, color=SIL, op=1.0):
        r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        pts = []
        for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
            for k in range(7):
                an = math.radians(a + 90 * k / 6)
                pts.append((cx + r * math.cos(an), cy + r * math.sin(an)))
        self.poly(pts, color, op)

    def glow(self, x, y, r, color=LUZ, amt=1.0):
        """Resplandor aditivo (caída suave)."""
        bb = self._bb([(x - r, y - r), (x + r, y + r)], pad=0)
        if bb is None or amt <= 0.003:
            return
        x0, y0, x1, y1 = bb
        gx, gy = _grid_roi(x1 - x0, y1 - y0)
        d = np.sqrt((gx + x0 - x * K) ** 2 + (gy + y0 - y * K) ** 2) / max(r * K, 1)
        a = np.clip(1 - d, 0, 1) ** 2.2
        reg = self.im[y0:y1, x0:x1]
        reg += (a * amt)[..., None] * np.float32(color)

    def haz(self, x, y, ang, largo, abertura, color=LUZ, amt=0.6):
        """Cono de luz desde (x, y) hacia `ang` (grados, 0 = derecha, 90 = abajo)."""
        a0, a1 = math.radians(ang - abertura / 2), math.radians(ang + abertura / 2)
        pts = [(x, y), (x + largo * math.cos(a0), y + largo * math.sin(a0)), (x + largo * math.cos(a1), y + largo * math.sin(a1))]
        bb = self._bb(pts, pad=1)
        if bb is None or amt <= 0.003:
            return
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(m, [self._fx(pts, x0, y0)], 255, cv2.LINE_AA, shift=4)
        gx, gy = _grid_roi(x1 - x0, y1 - y0)
        d = np.sqrt((gx + x0 - x * K) ** 2 + (gy + y0 - y * K) ** 2) / max(largo * K, 1)
        fall = np.clip(1 - d, 0, 1) ** 1.3
        m = (m.astype(np.float32) * fall).astype(np.uint8)
        self._blend(m, x0, y0, color, amt, aditivo=True)

    def texto(self, txt, x, y, px, color=CREMA, fnt="serif", op=1.0, anchor="mm", stroke=0):
        sp = _texto_sprite(txt, int(px * K), fnt, stroke)
        w, h = sp.shape[1], sp.shape[0]
        ax = {"l": 0, "m": 0.5, "r": 1.0}[anchor[0]]
        ay = {"t": 0, "m": 0.5, "b": 1.0}[anchor[1]]
        rx, ry = int(round(x * K - w * ax)), int(round(y * K - h * ay))
        x0, y0 = max(0, rx), max(0, ry)
        x1, y1 = min(HW, rx + w), min(HH, ry + h)
        if x1 <= x0 or y1 <= y0:
            return
        self._blend(sp[y0 - ry:y1 - ry, x0 - rx:x1 - rx], x0, y0, color, op)

    def fin(self, lz):
        lz[:] = cv2.resize(np.clip(self.im, 0, 1), (W, H), interpolation=cv2.INTER_CUBIC)


@functools.lru_cache(maxsize=256)
def _texto_sprite(txt, px, fnt, stroke):
    f = D.fuente(fnt, max(8, px))
    bb = f.getbbox(txt, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 6, bb[3] - bb[1] + 6
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((3 - bb[0], 3 - bb[1]), txt, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    return np.asarray(im)


# ====================================================================== ambiente
@functools.lru_cache(maxsize=16)
def _ruido(seed, w=HW * 2, h=HH, sig=40):
    rng = np.random.default_rng(seed)
    r = rng.random((h // 4, w // 4)).astype(np.float32)
    n = r.shape[1]
    r = cv2.GaussianBlur(np.tile(r, (1, 3)), (0, 0), sig / 4)[:, n:2 * n]       # horizontal sin costura
    r = cv2.resize(r, (w, h), interpolation=cv2.INTER_CUBIC)
    r = (r - r.min()) / max(r.max() - r.min(), 1e-6)
    return r


def niebla(p, t, y, alto, color=(0.5, 0.58, 0.7), op=0.5, vel=14.0, seed=1, sig=60):
    """Banda de niebla que se desplaza (ruido suave recorriendo el cuadro)."""
    n = _ruido(seed, sig=sig)
    off = int((t * vel * K) % (HW * 2 - HW))
    ys0, ys1 = int(max(0, (y - alto / 2) * K)), int(min(HH, (y + alto / 2) * K))
    if ys1 <= ys0:
        return
    reg = n[ys0:ys1, off:off + HW]
    v = np.linspace(-1, 1, ys1 - ys0, dtype=np.float32)[:, None]
    a = np.clip((reg - 0.35) * 2.2, 0, 1) * (1 - v ** 2) * op
    dst = p.im[ys0:ys1]
    dst *= (1 - a)[..., None]
    dst += a[..., None] * np.float32(color)


def estrellas(p, t, n=120, seed=3, y_max=0.6, brillo=0.9):
    rng = np.random.default_rng(seed)
    xs, ys, ph, rr = rng.random(n), rng.random(n) * y_max, rng.random(n) * 6.28, rng.random(n) * 1.6 + 0.6
    for i in range(n):
        b = brillo * (0.45 + 0.55 * math.sin(t * (0.8 + rr[i] * 0.6) + ph[i]))
        if b > 0.05:
            p.circ(xs[i] * W, ys[i] * H, rr[i] * 1.8, (0.9, 0.93, 1.0), b)


def luna(p, x, y, r, color=(0.93, 0.95, 1.0), halo=1.0):
    p.glow(x, y, r * 5.0, (0.28, 0.34, 0.5), 0.9 * halo)
    p.glow(x, y, r * 2.2, (0.55, 0.62, 0.78), 0.6 * halo)
    p.circ(x, y, r, color)
    p.circ(x - r * 0.28, y - r * 0.1, r * 0.22, (0.82, 0.85, 0.92), 0.5)
    p.circ(x + r * 0.30, y + r * 0.28, r * 0.15, (0.82, 0.85, 0.92), 0.5)


def lluvia(p, t, op=0.35, n=90, ang=12, largo=70, vel=2400, color=(0.7, 0.78, 0.9), seed=5):
    rng = np.random.default_rng(seed)
    xs, ys, ls = rng.random(n), rng.random(n), rng.random(n) * 0.6 + 0.7
    dx = math.tan(math.radians(ang))
    for i in range(n):
        y = ((ys[i] * H + t * vel * ls[i]) % (H + 200)) - 100
        x = (xs[i] * (W + 400) - 200 + dx * (y)) % (W + 200)
        p.linea((x, y), (x + dx * largo * ls[i], y + largo * ls[i]), 2, color, op * ls[i], caps=False)


def polvo(p, t, n=50, seed=7, op=0.5, color=LUZ, vel=18):
    rng = np.random.default_rng(seed)
    xs, ys, vx, vy, rr, ph = rng.random(n), rng.random(n), rng.random(n) - 0.5, rng.random(n) * -0.5 - 0.15, rng.random(n) * 3 + 1.5, rng.random(n) * 6
    for i in range(n):
        x = (xs[i] * W + vx[i] * vel * t * 3) % W
        y = (ys[i] * H + vy[i] * vel * t * 3) % H
        b = op * (0.4 + 0.6 * math.sin(t * 1.3 + ph[i]) ** 2)
        p.circ(x, y, rr[i], color, b)


def colinas(p, base_y, amp, color, off=0.0, seed=1, escala=1.0, op=1.0, relleno_hasta=None):
    """Cresta de montañas/colinas (suma de senos) rellena hacia abajo; `off` desplaza en x (paralaje)."""
    rng = np.random.default_rng(seed)
    f = rng.random(4) * 0.0035 + np.array([0.0012, 0.0028, 0.0061, 0.011]) * escala
    ph = rng.random(4) * 6.28
    a = np.array([1.0, 0.55, 0.28, 0.12]) * amp
    xs = np.arange(-40, W + 41, 20)
    ys = base_y - sum(a[i] * (0.5 + 0.5 * np.sin(f[i] * (xs + off) + ph[i])) for i in range(4))
    pts = [(x, y) for x, y in zip(xs, ys)] + [(W + 40, relleno_hasta or H + 40), (-40, relleno_hasta or H + 40)]
    p.poly(pts, color, op)


def pino(p, x, y, h, color=SIL, ancho=0.34):
    w = h * ancho
    p.poly([(x, y - h), (x - w * 0.34, y - h * 0.62), (x + w * 0.34, y - h * 0.62)], color)
    p.poly([(x, y - h * 0.82), (x - w * 0.5, y - h * 0.38), (x + w * 0.5, y - h * 0.38)], color)
    p.poly([(x, y - h * 0.55), (x - w * 0.66, y - h * 0.06), (x + w * 0.66, y - h * 0.06)], color)
    p.rect(x - h * 0.018, y - h * 0.08, x + h * 0.018, y, color)


def arbol_pelado(p, x, y, h, color=SIL, seed=1, nivel=5):
    """Árbol sin hojas (ramas recursivas), para bosque de invierno."""
    rng = np.random.default_rng(seed)

    def rama(x0, y0, ang, largo, grosor, n):
        x1, y1 = x0 + largo * math.cos(ang), y0 - largo * math.sin(ang)
        p.linea((x0, y0), (x1, y1), grosor, color)
        if n <= 0 or largo < 14:
            return
        for da in (-0.5 + rng.random() * 0.25, 0.45 - rng.random() * 0.25):
            rama(x1, y1, ang + da, largo * (0.68 + rng.random() * 0.1), max(2, grosor * 0.66), n - 1)
    rama(x, y, math.pi / 2, h * 0.3, h * 0.04, nivel)


def bosque(p, y, h, color, off=0.0, seed=1, n=22, pelados=False):
    rng = np.random.default_rng(seed)
    xs = (np.arange(n) / n * (W + 400) + rng.random(n) * 80 - 200 - off) % (W + 400) - 200
    for i in range(n):
        hh = h * (0.7 + rng.random() * 0.5)
        if pelados:
            arbol_pelado(p, xs[i], y, hh, color, seed=int(seed * 31 + i), nivel=4)
        else:
            pino(p, xs[i], y, hh, color)


def ciudad(p, t, y, color, off=0.0, seed=2, ventanas=True, h_max=420, ancho_med=110, luz=(1.0, 0.85, 0.5)):
    """Skyline de rascacielos con ventanas que parpadean."""
    rng = np.random.default_rng(seed)
    x = -200 - (off % 400)
    while x < W + 100:
        w = ancho_med * (0.6 + rng.random() * 0.9)
        h = h_max * (0.25 + rng.random() ** 1.6 * 0.75)
        p.rect(x, y - h, x + w, y + 10, color)
        if rng.random() < 0.3:
            p.rect(x + w * 0.45, y - h - 40, x + w * 0.55, y - h, color)
        if ventanas:
            cols, filas = int(w // 22), int(h // 30)
            for c in range(cols):
                for r in range(filas):
                    if rng.random() < 0.22:
                        b = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * rng.random() * 1.2 + rng.random() * 9))
                        p.rect(x + 8 + c * 22, y - h + 12 + r * 30, x + 8 + c * 22 + 11, y - h + 12 + r * 30 + 15, luz, b * 0.85)
        x += w + rng.random() * 14


def suelo(p, y, color_top, color_bot=None, h=None):
    p.rect(-10, y, W + 10, (H + 10) if h is None else y + h, color_top, grad=(color_top, color_bot or color_top))


def vineta_p(p, fuerza=0.6):
    """Oscurece bordes en el propio lienzo (además del filtro de película)."""
    key = ("v", round(fuerza, 2))
    if key not in _VIN:
        gx, gy = _grid_roi(HW, HH)
        r = np.sqrt(((gx - HW / 2) / (HW / 2)) ** 2 + ((gy - HH / 2) / (HH / 2)) ** 2)
        _VIN[key] = (1 - fuerza * np.clip(r - 0.35, 0, None) ** 1.6).clip(0.15, 1).astype(np.float32)[..., None]
    p.im *= _VIN[key]


_VIN = {}


# ====================================================================== personas (siluetas con esqueleto)
def _fk(pose, h):
    """Esqueleto: devuelve posiciones (en px, y hacia ARRIBA con origen en el suelo bajo la cadera) de cada articulación. Ángulos desde la vertical, + hacia delante."""
    th, sh, ua, fa, hd, rc = 0.245, 0.245, 0.165, 0.150, 0.075, 0.062
    lean = pose.get("lean", 0.0)
    (hl, kl), (hr, kr) = pose.get("ll", (0, 0)), pose.get("lr", (0, 0))

    def pierna(hip, flex):
        a1 = hip
        a2 = hip - flex
        kx, ky = th * math.sin(a1), -th * math.cos(a1)
        ax, ay = kx + sh * math.sin(a2), ky - sh * math.cos(a2)
        return (kx, ky), (ax, ay)
    kl_, al_ = pierna(hl, kl)
    kr_, ar_ = pierna(hr, kr)
    low = min(al_[1], ar_[1]) - 0.025 * pose.get("pie", 1)
    pel = (0.0, -low + pose.get("drop", 0.0))       # cadera sobre el suelo
    tx, ty = 0.30 * math.sin(lean), 0.30 * math.cos(lean)
    cu = (pel[0] + tx, pel[1] + ty)                # base del cuello
    sho = cu

    def brazo(a1, flex):
        ex, ey = sho[0] + ua * math.sin(a1), sho[1] - ua * math.cos(a1)
        wx, wy = ex + fa * math.sin(a1 + flex), ey - fa * math.cos(a1 + flex)
        return (ex, ey), (wx, wy)
    bl, br = pose.get("bl", (0.05, 0.2)), pose.get("br", (-0.05, 0.2))
    el_, wl_ = brazo(*bl)
    er_, wr_ = brazo(*br)
    hdc = (cu[0] + 0.05 * math.sin(lean + pose.get("head", 0.0)), cu[1] + 0.05 + hd)
    S = lambda q: (q[0] * h, q[1] * h)
    j = dict(pel=S(pel), cu=S(cu), hd=S(hdc), rc=rc * h,
             kl=S((pel[0] + kl_[0], pel[1] + kl_[1])), al=S((pel[0] + al_[0], pel[1] + al_[1])),
             kr=S((pel[0] + kr_[0], pel[1] + kr_[1])), ar=S((pel[0] + ar_[0], pel[1] + ar_[1])),
             el=S(el_), wl=S(wl_), er=S(er_), wr=S(wr_))
    return j


def capsula(p, a, b, r0, r1, color, alpha=1.0):
    """Segmento cónico redondeado entre a (radio r0) y b (radio r1)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p.poly([(a[0] + nx * r0, a[1] + ny * r0), (b[0] + nx * r1, b[1] + ny * r1), (b[0] - nx * r1, b[1] - ny * r1), (a[0] - nx * r0, a[1] - ny * r0)], color, alpha)
    p.circ(a[0], a[1], r0, color, alpha)
    p.circ(b[0], b[1], r1, color, alpha)


def persona(p, x, y, h, pose, color=SIL, facing=1, ropa="pantalon", pelo="corto", sombrero=False, bolso=False, alpha=1.0, objeto=None, mujer=None):
    """Silueta humana con esqueleto. (x, y) = pies; h = altura en px; facing = ±1."""
    j = _fk(pose, h)
    f = facing
    mujer = (ropa == "vestido" or pelo in ("largo", "moño")) if mujer is None else mujer

    def Q(q):
        return (x + f * q[0], y - q[1])
    pel, cu = Q(j["pel"]), Q(j["cu"])
    # piernas cónicas + zapatos
    for k in ("l", "r"):
        kn, an = Q(j["k" + k]), Q(j["a" + k])
        capsula(p, pel, kn, h * 0.047, h * 0.036, color, alpha)
        capsula(p, kn, an, h * 0.036, h * 0.025, color, alpha)
        p.poly([(an[0] - f * h * 0.015, an[1] - h * 0.012), (an[0] + f * h * 0.075, an[1] + h * 0.012), (an[0] + f * h * 0.075, an[1] + h * 0.030), (an[0] - f * h * 0.03, an[1] + h * 0.030)], color, alpha)
    # torso (hombros anchos, cintura, cadera)
    sw = h * (0.078 if mujer else 0.098)
    wa = h * (0.050 if mujer else 0.070)
    hw = h * (0.074 if mujer else 0.066)
    mid = ((cu[0] + pel[0]) / 2, (cu[1] + pel[1]) / 2)
    if ropa == "vestido":
        p.poly([(cu[0] - sw, cu[1] + h * 0.012), (cu[0] + sw, cu[1] + h * 0.012), (mid[0] + wa, mid[1]), (pel[0] + hw * 1.4, pel[1] + h * 0.02),
                (pel[0] + h * 0.17, pel[1] + h * 0.27), (pel[0] - h * 0.17, pel[1] + h * 0.27), (pel[0] - hw * 1.4, pel[1] + h * 0.02), (mid[0] - wa, mid[1])], color, alpha)
    else:
        p.poly([(cu[0] - sw, cu[1] + h * 0.012), (cu[0] + sw, cu[1] + h * 0.012), (mid[0] + wa, mid[1]), (pel[0] + hw, pel[1] - h * 0.02), (pel[0] - hw, pel[1] - h * 0.02), (mid[0] - wa, mid[1])], color, alpha)
        if ropa == "chaqueta":
            p.poly([(pel[0] - hw * 1.25, pel[1] + h * 0.06), (pel[0] + hw * 1.25, pel[1] + h * 0.06), (pel[0] + hw * 1.15, pel[1] - h * 0.09), (pel[0] - hw * 1.15, pel[1] - h * 0.09)], color, alpha)
    # brazos
    for k in ("l", "r"):
        e_, w_ = Q(j["e" + k]), Q(j["w" + k])
        capsula(p, (cu[0] + (-1 if k == "l" else 1) * f * sw * 0.55 * 0, cu[1] - h * 0.012), e_, h * 0.034, h * 0.027, color, alpha)
        capsula(p, e_, w_, h * 0.027, h * 0.021, color, alpha)
        p.circ(w_[0], w_[1], h * 0.026, color, alpha)
    # cuello y cabeza
    hd = Q(j["hd"])
    capsula(p, cu, (hd[0], hd[1] + j["rc"] * 0.4), h * 0.026, h * 0.022, color, alpha)
    p.elip(hd[0], hd[1], j["rc"] * 0.92, j["rc"] * 1.08, 0, color, alpha)
    if pelo == "largo":
        p.poly([(hd[0] - f * j["rc"] * 0.1, hd[1] - j["rc"] * 1.15), (hd[0] - f * j["rc"] * 1.25, hd[1] - j["rc"] * 0.5),
                (hd[0] - f * j["rc"] * 1.9, hd[1] + j["rc"] * 2.8), (hd[0] - f * j["rc"] * 0.4, hd[1] + j["rc"] * 2.3), (hd[0] + f * j["rc"] * 0.5, hd[1] + j["rc"] * 0.2)], color, alpha)
    elif pelo == "moño":
        p.circ(hd[0] - f * j["rc"] * 0.75, hd[1] - j["rc"] * 1.0, j["rc"] * 0.46, color, alpha)
    elif pelo == "afro":
        p.circ(hd[0], hd[1] - j["rc"] * 0.3, j["rc"] * 1.35, color, alpha)
    if sombrero:
        p.poly([(hd[0] - j["rc"] * 1.7, hd[1] - j["rc"] * 0.6), (hd[0] + j["rc"] * 1.7, hd[1] - j["rc"] * 0.6), (hd[0] + j["rc"] * 0.9, hd[1] - j["rc"] * 1.15),
                (hd[0] - j["rc"] * 0.9, hd[1] - j["rc"] * 1.15)], color, alpha)
    if bolso:
        w_ = Q(j["wl"])
        p.rect(w_[0] - h * 0.045, w_[1], w_[0] + h * 0.045, w_[1] + h * 0.10, color, alpha)
    if objeto:
        objeto(p, Q(j["wr"]), Q(j["wl"]), f)
    return j


def pose_caminar(ph, amp=0.55, brazos=0.45, lean=0.06, rebote=0.012):
    s = math.sin(ph)
    c = math.cos(ph)
    return dict(ll=(amp * s, max(0, -0.9 * c + 0.2) * 0.7), lr=(-amp * s, max(0, 0.9 * c + 0.2) * 0.7),
                bl=(-brazos * s * 0.8, 0.25 + 0.15 * c), br=(brazos * s * 0.8, 0.25 - 0.15 * c), lean=lean, head=0.0, drop=rebote * abs(c))


def pose_estar(t=0.0, lean=0.0):
    r = 0.012 * math.sin(t * 1.8)
    return dict(ll=(0.04, 0), lr=(-0.04, 0), bl=(0.05 + r, 0.12), br=(-0.04 - r, 0.12), lean=lean, head=0.0)


def pose_sentado(t=0.0, lean=0.08):
    return dict(ll=(1.35, 1.35), lr=(1.30, 1.30), bl=(0.55, 1.0), br=(0.50, 1.05), lean=lean, head=0.1 * math.sin(t))


def pose_escribir(t=0.0):
    return dict(ll=(1.35, 1.35), lr=(1.30, 1.30), bl=(0.9, 0.7 + 0.1 * math.sin(t * 7)), br=(0.8, 0.9 + 0.1 * math.sin(t * 7 + 1)), lean=0.2, head=0.35)


def pose_manos_cara(t=0.0):
    return dict(ll=(1.35, 1.35), lr=(1.30, 1.30), bl=(0.45, 2.2), br=(0.35, 2.3), lean=0.3 + 0.01 * math.sin(t * 1.5), head=0.5)


def pose_cartel(t=0.0, ph=0.0):
    b = 0.06 * math.sin(t * 5 + ph)
    return dict(ll=(0.04, 0), lr=(-0.04, 0), bl=(2.7 + b, 0.2), br=(2.6 - b, 0.2), lean=0.0, head=-0.1)


def pose_señalar(u=1.0):
    return dict(ll=(0.1, 0), lr=(-0.1, 0), bl=(0.1, 0.1), br=(1.45 * u, 0.1), lean=0.1, head=0.0)


def pose_brazos_arriba(t=0.0):
    b = 0.08 * math.sin(t * 6)
    return dict(ll=(0.2, 0.1), lr=(-0.2, 0.1), bl=(2.5 + b, 0.5), br=(2.4 - b, 0.5), lean=-0.05, head=-0.2)


def pose_correr(ph):
    return pose_caminar(ph, amp=0.9, brazos=0.9, lean=0.22, rebote=0.03)


def multitud(p, n, x0, x1, y, h, color, t, seed=1, pose=None, sway=1.0, h_var=0.18, objeto=None, ropas=None):
    """Fila de siluetas de pie con balanceo y alturas variadas."""
    rng = np.random.default_rng(seed)
    xs = np.linspace(x0, x1, n) + (rng.random(n) - 0.5) * (x1 - x0) / n * 0.6
    for i in range(n):
        hh = h * (1 - h_var / 2 + rng.random() * h_var)
        ps = pose(t, i) if pose else pose_estar(t * sway + rng.random() * 6, lean=0.02 * math.sin(t + i))
        persona(p, xs[i], y + (rng.random() - 0.5) * 24, hh, ps, color, facing=1 if rng.random() < 0.5 else -1,
                ropa=("vestido" if rng.random() < 0.3 else "pantalon") if ropas is None else ropas, pelo="largo" if rng.random() < 0.35 else "corto",
                objeto=objeto)


def silueta_sentada_vista_trasera(p, x, y, h, color=SIL):
    """Persona vista de espaldas en un banco (cabeza + hombros): público, testigos."""
    p.rrect(x - h * 0.30, y - h * 0.55, x + h * 0.30, y + h * 0.5, h * 0.2, color)
    p.circ(x, y - h * 0.72, h * 0.22, color)


def acostada(p, x, y, largo, color=SIL, t=0.0, brazo=1.0, resp=1.0, mover=0.0, sabana=None):
    """Figura tendida de lado (vista lateral) sobre una camilla; (x, y) = centro del cuerpo. brazo: 0..1 extendido hacia el espectador."""
    L = largo
    r = math.sin(t * 1.6) * 0.010 * resp
    # torso + cadera
    p.rrect(x - L * 0.30, y - L * 0.07 - L * r, x + L * 0.14, y + L * 0.07, L * 0.06, color)
    p.rrect(x + L * 0.10, y - L * 0.055, x + L * 0.30, y + L * 0.06, L * 0.05, color)
    # piernas (una se mueve si mover > 0)
    kk = math.sin(t * 3.0) * 0.05 * mover
    p.polilinea([(x + L * 0.28, y + L * 0.01), (x + L * 0.48, y - L * 0.015 + L * kk), (x + L * 0.66, y + L * 0.015)], L * 0.06, color)
    p.polilinea([(x + L * 0.28, y + L * 0.04), (x + L * 0.50, y + L * 0.03), (x + L * 0.67, y + L * 0.035)], L * 0.055, color)
    # cabeza
    p.circ(x - L * 0.40, y - L * 0.02, L * 0.062, color)
    p.linea((x - L * 0.34, y - L * 0.02), (x - L * 0.28, y - L * 0.01), L * 0.04, color)
    # brazo hacia el espectador (se dobla en el codo)
    sx, sy = x - L * 0.22, y + L * 0.02
    ex, ey = sx + L * 0.10, sy + L * 0.09 * brazo
    wx, wy = ex + L * 0.13, ey + L * 0.045 * brazo - L * 0.01 * math.sin(t * 2.6) * mover
    p.polilinea([(sx, sy), (ex, ey), (wx, wy)], L * 0.035, color)
    p.circ(wx, wy, L * 0.022, color)
    return (ex, ey), (wx, wy)


# ====================================================================== composición con zoom de cámara sobre el lienzo
def zoom_p(p, z=1.0, cx=0.5, cy=0.5):
    """Acerca el lienzo ya pintado (cámara). z>1 acerca."""
    if abs(z - 1.0) < 1e-3:
        return
    M = np.array([[z, 0, HW * cx * (1 - z)], [0, z, HH * cy * (1 - z)]], np.float32)
    p.im[:] = cv2.warpAffine(p.im, M, (HW, HH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
