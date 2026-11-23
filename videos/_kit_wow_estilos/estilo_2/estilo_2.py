# -*- coding: utf-8 -*-
"""
ESTILO 2 · RELIQUIA DE ORO Y PIEDRA — propuesta de kit visual para Crónicas de Warcraft (22-nov-2026).

Todo por código (numpy + PIL + opencv, cuadro a cuadro) y original: piedra oscura tallada con ruido fractal y bisel por
mapa de distancias, molduras de oro con relieve iluminado desde arriba a la izquierda, gemas de talla brillante dibujadas
faceta a faceta y engastadas con garras, runas inventadas (no son de Blizzard) y polvo dorado.

Piezas reutilizables (para pasarlas al kit si se elige el estilo):
    mapa_ruta(mapa, zona, puntos, ruta=(i, j), foto=..., rotulo_final=..., t0=...)   mapa enmarcado + cámara + ruta de runas
    ficha(titulo, iconos, etiqueta='×15', valor=15, t0=...)                          tablilla de piedra con engastes y contador
    tarjeta(foto, linea1, linea2, sub, t0=...)                                         relicario de arco con gema clave
    rotulo(texto, sello='5', t0=...)                                                   rótulo inferior con sello de oro
Cada una devuelve un objeto con .dibujar(lienzo, t) (lienzo = np.float32 HxWx3, 0-255; t en segundos absolutos).

Uso:
    python estilo_2.py                 render completo (video + hoja.jpg)
    python estilo_2.py --cuadros 5 9.6 cuadros sueltos a _tmp/ (pruebas rápidas, sin video)
    python estilo_2.py --hoja          solo rehace hoja.jpg desde el mp4
"""
import os
import sys
import math
import functools
import subprocess

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

cv2.setNumThreads(1)

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = r'C:\FabricaAnimaciones\videos\wow_errores_60'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
SALIDA = os.path.join(AQUI, 'estilo_2_oro_piedra.mp4')
W, H, FPS, DUR = 1920, 1080, 30, 30.0
NOMBRE = 'ESTILO 2 · RELIQUIA DE ORO Y PIEDRA'

F_GRAB = r'C:\Windows\Fonts\CASTELAR.TTF'      # mayúsculas grabadas (no tiene «·»: se dibuja un rombo de oro)
F_SERIF = r'C:\Windows\Fonts\constanb.ttf'     # Constantia negrita
F_SERIF_I = r'C:\Windows\Fonts\constanz.ttf'   # Constantia negrita cursiva

GEMA = dict(rojo=(206, 26, 44), ambar=(236, 160, 22), azul=(36, 100, 230), verde=(34, 190, 70),
            violeta=(140, 60, 215), blanco=(220, 232, 250))
PIEDRA = (50, 48, 56)
LUZ = np.array([-0.55, -0.65, 0.52], np.float32)
LUZ /= np.linalg.norm(LUZ)
SS = 4  # supermuestreo de máscaras


# ───────────────────────────── easing ─────────────────────────────
def cl(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def pr(t, t0, t1):
    return cl((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)


def eo(x):
    return 1 - (1 - x) ** 3


def eio(x):
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def eback(x, s=1.70158):
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def ebounce(x):
    n1, d1 = 7.5625, 2.75
    if x < 1 / d1:
        return n1 * x * x
    if x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + .75
    if x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + .9375
    x -= 2.625 / d1
    return n1 * x * x + .984375


def lerp(a, b, x):
    return a + (b - a) * x


@functools.lru_cache(None)
def fuente(ruta, tam):
    return ImageFont.truetype(ruta, tam)


# ───────────────────────────── sprites ─────────────────────────────
class Spr:
    """Sprite premultiplicado: p = rgb*alfa (float32, 0-255), a = alfa (0-1). pad = margen de sombra."""

    def __init__(self, p, a, pad=0, ancla=(.5, .5)):
        self.p = np.ascontiguousarray(p, np.float32)
        self.a = np.ascontiguousarray(a, np.float32)
        self.pad = pad
        self.ancla = ancla
        self._cache = {}

    @classmethod
    def rgba(cls, rgb, a, **kw):
        a = np.clip(a, 0, 1).astype(np.float32)
        return cls(np.asarray(rgb, np.float32) * a[..., None], a, **kw)

    @classmethod
    def pil(cls, im):
        arr = np.asarray(im.convert('RGBA')).astype(np.float32)
        return cls.rgba(arr[..., :3], arr[..., 3] / 255)

    @property
    def w(self):
        return self.a.shape[1]

    @property
    def h(self):
        return self.a.shape[0]

    def escala(self, s):
        if abs(s - 1) < 2e-3:
            return self
        k = round(s, 3)
        if k in self._cache:
            return self._cache[k]
        nw, nh = max(1, int(round(self.w * s))), max(1, int(round(self.h * s)))
        q = cv2.resize(np.dstack([self.p, self.a]), (nw, nh),
                       interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
        r = Spr(q[..., :3], q[..., 3], self.pad * s, self.ancla)
        if self.w * self.h < 160000 and len(self._cache) < 80:
            self._cache[k] = r
        return r

    def rotar(self, grados):
        d = int(math.ceil(math.hypot(self.w, self.h))) + 2
        M = cv2.getRotationMatrix2D((self.w / 2, self.h / 2), grados, 1.0)
        M[0, 2] += (d - self.w) / 2
        M[1, 2] += (d - self.h) / 2
        q = cv2.warpAffine(np.dstack([self.p, self.a]), M, (d, d), flags=cv2.INTER_LINEAR)
        return Spr(q[..., :3], q[..., 3])

    def cols(self, f0, f1):
        c0 = int(self.w * cl(f0))
        c1 = max(c0 + 1, int(self.w * cl(f1)))
        r = Spr.__new__(Spr)
        r.p, r.a, r.pad, r.ancla, r._cache = self.p[:, c0:c1], self.a[:, c0:c1], 0, (0, 0), {}
        return r, c0


def pegar(lz, sp, x, y, alfa=1.0, s=1.0, ancla=None, modo='n'):
    """Compone sp sobre lz (float HxWx3) con su punto `ancla` (fracción del sprite) en (x, y). modo 'n' normal, 'a' aditivo."""
    if alfa <= 0.003 or s <= 0.01:
        return
    if s != 1:
        sp = sp.escala(s)
    ax, ay = ancla if ancla is not None else sp.ancla
    h, w = sp.a.shape
    x0 = int(round(x - ax * w))
    y0 = int(round(y - ay * h))
    X0, Y0 = max(0, x0), max(0, y0)
    X1, Y1 = min(lz.shape[1], x0 + w), min(lz.shape[0], y0 + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    p = sp.p[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    reg = lz[Y0:Y1, X0:X1]
    if modo == 'n':
        a = sp.a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
        reg *= (1 - a * alfa)[..., None]
    reg += p * alfa


def pegar_spr(dst, src, x, y, ancla=(.5, .5)):
    """Compone un sprite dentro de otro (actualiza también el alfa)."""
    h, w = src.a.shape
    x0, y0 = int(round(x - ancla[0] * w)), int(round(y - ancla[1] * h))
    X0, Y0 = max(0, x0), max(0, y0)
    X1, Y1 = min(dst.w, x0 + w), min(dst.h, y0 + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    a = src.a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    dst.p[Y0:Y1, X0:X1] = dst.p[Y0:Y1, X0:X1] * (1 - a[..., None]) + src.p[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    dst.a[Y0:Y1, X0:X1] = dst.a[Y0:Y1, X0:X1] * (1 - a) + a


def barrido(sp, pos, ancho=.10, fuerza=.85):
    """Destello que cruza el sprite en diagonal (pos 0-1), solo donde hay oro/texto."""
    h, w = sp.a.shape
    u = (np.arange(w, dtype=np.float32)[None, :] + np.arange(h, dtype=np.float32)[:, None] * .45) / (w + h * .45)
    b = np.exp(-((u - pos) / ancho) ** 2) * fuerza
    return Spr(sp.p + (b * sp.a)[..., None] * np.array([255, 244, 210], np.float32), sp.a, sp.pad, sp.ancla)


# ───────────────────────────── materiales ─────────────────────────────
def ruido(h, w, seed, octavas=5, base=3):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octavas):
        nx = base * 2 ** o
        ny = max(2, int(round(nx * h / max(w, 1))))
        g = rng.random((ny + 1, nx + 1)).astype(np.float32)
        acc += cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC) * amp
        tot += amp
        amp *= .5
    acc /= tot
    acc -= acc.min()
    return acc / max(1e-6, acc.max())


def piedra(h, w, seed=0, base=PIEDRA, oscura=1.0):
    """Piedra oscura: ruido fractal + vetas finas + grano + leve calidez."""
    n = ruido(h, w, seed, 6, 3)
    n2 = ruido(h, w, seed + 7, 5, 5)
    vena = np.exp(-((n2 - .5) / .016) ** 2)
    g = np.random.default_rng(seed + 3).random((h, w)).astype(np.float32)
    v = (.80 + .8 * (n - .5) - .3 * vena + .1 * (g - .5)) * oscura
    tib = ruido(h, w, seed + 11, 3, 2)[..., None]
    col = np.array(base, np.float32) * (1 - .3 * tib) + np.array((66, 56, 46), np.float32) * .3 * tib
    return col * v[..., None]


def relieve(cob, ancho, perfil='redondo', altura=1.0):
    """Sombreado 0-1 de una forma en relieve (luz arriba-izquierda) a partir de su cobertura."""
    m = (cob > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    x = np.clip(d / max(ancho, .5), 0, 1)
    hgt = np.sqrt(np.clip(1 - (1 - x) ** 2, 0, 1)) if perfil == 'redondo' else x
    hgt = cv2.GaussianBlur(hgt * ancho * altura, (0, 0), .9)
    gy, gx = np.gradient(hgt)
    n = np.sqrt(gx * gx + gy * gy + 1)
    return np.clip((-gx * LUZ[0] - gy * LUZ[1] + LUZ[2]) / n, 0, 1)


_ORO_T = [0, .2, .42, .6, .76, .9, 1]
_ORO_C = np.array([(30, 16, 4), (88, 50, 12), (166, 112, 34), (220, 166, 66), (248, 210, 122),
                   (255, 238, 186), (255, 254, 236)], np.float32)


def oro(sh):
    return np.stack([np.interp(sh, _ORO_T, _ORO_C[:, c]) for c in range(3)], -1).astype(np.float32)


def mascara(w, h, dibujar):
    im = Image.new('L', (int(w) * SS, int(h) * SS), 0)
    dibujar(ImageDraw.Draw(im), SS)
    return np.asarray(im.resize((int(w), int(h)), Image.BOX)).astype(np.float32) / 255


def forma(tipo, w, h, ins, radio=0):
    def f(d, k):
        i = ins * k
        x1, y1 = w * k - 1 - i, h * k - 1 - i
        if x1 <= i or y1 <= i:
            return
        if tipo == 'rect':
            d.rounded_rectangle([i, i, x1, y1], radius=max(0.0, radio - ins) * k, fill=255)
        elif tipo == 'arco':
            R = w / 2.0
            d.ellipse([i, i, x1, 2 * R * k - 1 - i], fill=255)
            d.rounded_rectangle([i, R * k, x1, y1], radius=max(0.0, radio - ins) * k, fill=255)
        elif tipo == 'circulo':
            d.ellipse([i, i, x1, y1], fill=255)
        elif tipo == 'rombo':
            e = ins * k * 1.4142
            d.polygon([(w * k / 2, e), (w * k - e, h * k / 2), (w * k / 2, h * k - e), (e, h * k / 2)], fill=255)
    return f


def oro_de(cob, ancho, grano_seed=None):
    g = oro(relieve(cob, ancho))
    if grano_seed is not None:
        n = ruido(cob.shape[0], cob.shape[1], grano_seed, 4, 9)
        g *= (.92 + .16 * n)[..., None]
    return g


def con_sombra(sp, sombra=12, fuerza=.7, solo_fuera=None):
    """Añade margen y sombra proyectada (abajo-derecha) a un sprite."""
    pad = int(sombra * 2)
    h, w = sp.h, sp.w
    P = np.zeros((h + 2 * pad, w + 2 * pad, 3), np.float32)
    A = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
    P[pad:pad + h, pad:pad + w] = sp.p
    A[pad:pad + h, pad:pad + w] = sp.a
    base = A.copy() if solo_fuera is None else np.pad(solo_fuera, pad)
    M = np.float32([[1, 0, sombra * .45], [0, 1, sombra * .8]])
    s = cv2.warpAffine(cv2.GaussianBlur(base, (0, 0), sombra * .55), M, (base.shape[1], base.shape[0])) * fuerza
    if solo_fuera is not None:
        s *= (1 - base)
    A = A + s * (1 - A)
    return Spr(P, A, pad, sp.ancla)


# ───────────────────────────── marcos ─────────────────────────────
def placa_oro(tam, seed=0):
    """Rombo de oro (asiento de gema en las esquinas)."""
    cob = mascara(tam, tam, forma('rombo', tam, tam, 0))
    cob2 = mascara(tam, tam, forma('rombo', tam, tam, tam * .16))
    g = oro_de(cob, tam * .12, seed)
    filo = np.clip(cob - cob2, 0, 1)
    inner = oro(relieve(cob2, tam * .05)) * .78
    rgb = g * filo[..., None] + inner * cob2[..., None]
    return Spr.rgba(rgb, cob)


def marco(w, h, borde=40, radio=16, tipo='rect', interior='piedra', seed=1, inlay=True, oscuro=.58,
          sombra=14, adornos=False, base=PIEDRA):
    """Marco tallado: moldura de oro · banda de piedra biselada (con hilo de oro) · moldura interior · fondo.
    interior='piedra' (tablilla) o 'hueco' (ventana transparente con sombra interior para meter mapa/foto)."""
    w, h = int(w), int(h)
    g1 = max(3.0, borde * .2)
    b = borde * .56
    g2 = max(2.5, borde * .2)

    def M(ins):
        return mascara(w, h, forma(tipo, w, h, ins, radio))

    c0, c1, c2, c3 = M(0), M(g1), M(g1 + b), M(g1 + b + g2)
    anillo_o = np.clip(c0 - c1, 0, 1)
    banda = np.clip(c1 - c2, 0, 1)
    anillo_i = np.clip(c2 - c3, 0, 1)
    st = piedra(h, w, seed, base)
    sh_b = relieve(banda, min(6.0, b / 3), 'chaflan')
    rgb = (oro_de(anillo_o, g1 / 2, seed + 5) * anillo_o[..., None]
           + st * (1 + 1.3 * (sh_b - LUZ[2]))[..., None] * banda[..., None]
           + oro_de(anillo_i, g2 / 2, seed + 6) * anillo_i[..., None])
    if inlay and b > 8:
        la, lb = M(g1 + b * .5 - 1.3), M(g1 + b * .5 + 1.3)
        lin = np.clip(la - lb, 0, 1)
        rgb = rgb * (1 - lin[..., None]) + oro(relieve(lin, 1.3)) * lin[..., None]
    a = c0.copy()
    m3 = (c3 > .5).astype(np.uint8)
    if interior == 'piedra':
        st2 = piedra(h, w, seed + 21, base, oscura=oscuro)
        rec = 1 - 1.15 * (relieve(c3, 12, 'chaflan') - LUZ[2])
        d = cv2.distanceTransform(m3, cv2.DIST_L2, 5)
        ao = np.clip(d / 24, 0, 1) * .4 + .6
        rgb = rgb + st2 * (rec * ao)[..., None] * c3[..., None]
        gi = borde * .45 + 4
        if gi * 2 + 20 < min(w, h) - 2 * (g1 + b + g2) and borde >= 14:
            ga, gb = M(g1 + b + g2 + gi), M(g1 + b + g2 + gi + 2.2)
            surco = np.clip(ga - gb, 0, 1)
            luz = np.clip(np.roll(np.roll(surco, 2, 0), 2, 1) - surco, 0, 1)
            rgb = rgb * (1 - .7 * surco[..., None]) + np.array((150, 118, 64), np.float32) * (.55 * luz * (1 - surco))[..., None]
    else:
        a = np.clip(c0 - c3, 0, 1)
        d = cv2.distanceTransform(m3, cv2.DIST_L2, 5)
        ms = m3 & np.roll(np.roll(m3, 9, 0), 9, 1)
        d2 = cv2.distanceTransform(ms, cv2.DIST_L2, 5)
        som = np.maximum((1 - np.clip(d / 22, 0, 1)) ** 2 * .55, (1 - np.clip(d2 / 30, 0, 1)) ** 2 * .8)
        a = a + som * c3
    sp = Spr.rgba(np.clip(rgb, 0, 255), np.clip(a, 0, 1))
    if adornos:
        pt = int(borde * 1.75)
        pl = placa_oro(pt, seed + 9)
        q = borde * .5
        esq = [(q, q), (w - q, q), (q, h - q), (w - q, h - q)] if tipo == 'rect' else [(q, h - q), (w - q, h - q)]
        for x, y in esq:
            pegar_spr(sp, pl, x, y)
    sp.interior = (g1 + b + g2)
    if sombra:
        r = con_sombra(sp, sombra, .72, solo_fuera=c0)
        r.interior = sp.interior
        return r
    return sp


# ───────────────────────────── gemas y brillos ─────────────────────────────
@functools.lru_cache(None)
def gema(d, color, seed=0, punta=0.0, bisel=.17, garras=6, apagada=False):
    """Gema de talla brillante vista desde arriba, engastada en bisel de oro con garras.
    punta>0 añade un colgante de oro terminado en pico (marcador de mapa); el ancla queda en el pico."""
    col = np.array(color, np.float32) * (.32 if apagada else 1.0)
    R = d / 2.0
    bw = d * bisel
    pad = int(math.ceil(bw + 7))
    Wd = int(math.ceil(d + 2 * pad))
    c = Wd / 2.0
    ro = R + bw
    L = d * punta
    Hd = int(math.ceil(Wd + L + 4)) if punta else Wd
    k = SS
    rng = np.random.default_rng(seed)

    def tono(b):
        v = col * b if b <= 1 else col + (255 - col) * min(1.0, (b - 1) * 1.7)
        if apagada:
            v = col * min(b, 1.3)
        return tuple(int(x) for x in np.clip(v, 0, 255))

    im = Image.new('RGB', (Wd * k, Hd * k), (0, 0, 0))
    dr = ImageDraw.Draw(im, 'RGBA')
    a0 = -math.pi / 2 + math.pi / 8
    T = [(c + .5 * R * math.cos(a0 + j * math.pi / 4), c + .5 * R * math.sin(a0 + j * math.pi / 4)) for j in range(8)]
    G = [(c + R * 1.03 * math.cos(a0 + i * math.pi / 8), c + R * 1.03 * math.sin(a0 + i * math.pi / 8)) for i in range(16)]
    thL = math.atan2(-1, -1)

    def P(pts):
        return [(x * k, y * k) for x, y in pts]

    for j in range(8):
        a, b2 = T[j], T[(j + 1) % 8]
        g0, g1, g2 = G[2 * j], G[2 * j + 1], G[(2 * j + 2) % 16]
        for tri, base, off in (((a, b2, g1), .74, 0), ((a, g0, g1), .5, .38), ((b2, g1, g2), .5, -.38)):
            cx = sum(p[0] for p in tri) / 3 - c
            cy = sum(p[1] for p in tri) / 3 - c
            cv = math.cos(math.atan2(cy, cx) - thL + off)
            bri = base + .45 * cv + .55 * max(0.0, -cv) ** 8 + rng.uniform(-.09, .09)
            dr.polygon(P(tri), fill=tono(bri))
    dr.polygon(P(T), fill=tono(.86))
    ew = max(1, int(round(k * d / 46)))
    edge = tono(.38)
    for j in range(8):
        a, b2 = T[j], T[(j + 1) % 8]
        for q in ((a, b2), (a, G[2 * j]), (a, G[2 * j + 1]), (b2, G[2 * j + 1])):
            dr.line(P(q), fill=edge, width=ew)
    if not apagada:
        dr.polygon(P([(c - .40 * R, c - .06 * R), (c - .06 * R, c - .40 * R), (c + .06 * R, c - .30 * R),
                      (c - .30 * R, c + .06 * R)]), fill=(255, 255, 255, 105))
        rr = .085 * R
        dr.ellipse(P([(c - .58 * R - rr, c - .5 * R - rr), (c - .58 * R + rr, c - .5 * R + rr)]), fill=(255, 255, 255, 220))
    gem_rgb = np.asarray(im.resize((Wd, Hd), Image.BOX)).astype(np.float32)
    gem_cov = mascara(Wd, Hd, lambda dd, kk: dd.ellipse([(c - R) * kk, (c - R) * kk, (c + R) * kk, (c + R) * kk], fill=255))

    def m_oro(dd, kk):
        dd.ellipse([(c - ro) * kk, (c - ro) * kk, (c + ro) * kk, (c + ro) * kk], fill=255)
        if punta:
            dd.polygon([((c - ro * .66) * kk, (c + ro * .5) * kk), ((c + ro * .66) * kk, (c + ro * .5) * kk),
                        (c * kk, (c + ro + L) * kk)], fill=255)
        ri = R * .95
        dd.ellipse([(c - ri) * kk, (c - ri) * kk, (c + ri) * kk, (c + ri) * kk], fill=0)

    gcov = mascara(Wd, Hd, m_oro)
    gold = oro(relieve(gcov, bw * .55))
    if apagada:
        gold *= .62

    p = gem_rgb * gem_cov[..., None]
    a = gem_cov.copy()
    p = p * (1 - gcov[..., None]) + gold * gcov[..., None]
    a = a * (1 - gcov) + gcov
    if garras:
        def m_g(dd, kk):
            for i in range(garras):
                an = -math.pi / 2 + (i + .5) * 2 * math.pi / garras
                px, py = c + R * .97 * math.cos(an), c + R * .97 * math.sin(an)
                r2 = bw * .6
                dd.ellipse([(px - r2) * kk, (py - r2) * kk, (px + r2) * kk, (py + r2) * kk], fill=255)
        pc = mascara(Wd, Hd, m_g)
        pg = oro(relieve(pc, bw * .5)) * (.62 if apagada else 1)
        p = p * (1 - pc[..., None]) + pg * pc[..., None]
        a = a * (1 - pc) + pc
    s = cv2.warpAffine(cv2.GaussianBlur(a, (0, 0), max(1.2, d * .05)), np.float32([[1, 0, 2], [0, 1, 3]]), (Wd, Hd)) * .6
    a2 = a + s * (1 - a)
    ancla = (.5, (c + ro + L) / Hd) if punta else (.5, .5)
    sp = Spr(p, a2, 0, ancla)
    sp.centro = (c, c)   # centro de la piedra dentro del sprite
    return sp


@functools.lru_cache(None)
def destello(r=80, color=(255, 236, 190)):
    """Estrella de 4 puntas + halo (para sumar)."""
    y, x = np.mgrid[-r:r + 1, -r:r + 1].astype(np.float32)
    rr = np.sqrt(x * x + y * y) / r
    th = r * .022 + .8
    I = (np.exp(-(rr / .09) ** 2) + np.exp(-(rr / .32) ** 2) * .32
         + np.exp(-(y / th) ** 2) * np.clip(1 - np.abs(x) / r, 0, 1) ** 2.2
         + np.exp(-(x / th) ** 2) * np.clip(1 - np.abs(y) / r, 0, 1) ** 2.2)
    u, v = (x + y) / 1.4142, (x - y) / 1.4142
    I += .35 * (np.exp(-(v / th) ** 2) * np.clip(1 - np.abs(u) / (r * .55), 0, 1) ** 2
                + np.exp(-(u / th) ** 2) * np.clip(1 - np.abs(v) / (r * .55), 0, 1) ** 2)
    I = np.clip(I, 0, 1.6)
    return Spr(I[..., None] * np.array(color, np.float32), np.clip(I, 0, 1))


@functools.lru_cache(None)
def halo(r=40, color=(255, 196, 96), dureza=2.0):
    y, x = np.mgrid[-r:r + 1, -r:r + 1].astype(np.float32)
    I = np.exp(-((np.sqrt(x * x + y * y) / r) * dureza) ** 2)
    return Spr(I[..., None] * np.array(color, np.float32), I)


@functools.lru_cache(None)
def anillo_luz(r=100, color=(255, 214, 130)):
    q = int(r * 1.15)
    y, x = np.mgrid[-q:q + 1, -q:q + 1].astype(np.float32)
    rr = np.sqrt(x * x + y * y) / r
    I = np.exp(-((rr - 1) / .045) ** 2) + .35 * np.exp(-((rr - .93) / .1) ** 2)
    return Spr(I[..., None] * np.array(color, np.float32), np.clip(I, 0, 1))


def flash(lz, t, t_imp, x, y, tam=1.0, dur=.55):
    tau = t - t_imp
    if 0 <= tau <= dur:
        e = tau / dur
        pegar(lz, destello(), x, y, (1 - e) ** 2 * 1.1, s=tam * (.5 + .9 * eo(e)), modo='a')


def onda(lz, t, t0, x, y, rmax=160, dur=.6):
    tau = t - t0
    if 0 <= tau <= dur:
        e = tau / dur
        pegar(lz, anillo_luz(), x, y, (1 - e) ** 2 * .9, s=max(.05, rmax / 100 * eo(e)), modo='a')


def chispa_periodica(lz, t, x, y, fase=0.0, periodo=2.8, tam=.32):
    v = math.sin(2 * math.pi * (t / periodo + fase))
    if v > .9:
        pegar(lz, destello(), x, y, ((v - .9) / .1) ** 1.5 * .9, s=tam, modo='a')


def estallido(lz, t, t0, x, y, n=26, seed=0, vel=(150, 440), vida=1.1, alfa=1.0):
    tau = t - t0
    if tau < 0 or tau > vida * 1.4:
        return
    rng = np.random.default_rng(seed)
    for _ in range(n):
        an = rng.uniform(0, 2 * math.pi)
        v = rng.uniform(*vel)
        L = vida * rng.uniform(.55, 1.3)
        r = int(rng.uniform(2, 5))
        if tau > L:
            continue
        dist = v * (1 - math.exp(-3.2 * tau)) / 3.2
        px = x + math.cos(an) * dist
        py = y + math.sin(an) * dist * .8 + 70 * tau * tau
        pegar(lz, halo(r * 2, (255, 214, 120), 1.6), px, py, (1 - tau / L) ** 1.4 * alfa, modo='a')


class Polvo:
    """Polvo dorado que flota y titila (sin estado: depende solo de t)."""

    def __init__(self, n=70, seed=3, zona=(0, 0, W, H), vel=(10, 34), tam=(2, 6)):
        rng = np.random.default_rng(seed)
        self.zona = zona
        x0, y0, x1, y1 = zona
        self.ps = [(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*vel), rng.uniform(8, 30),
                    rng.uniform(.2, .7), rng.uniform(0, 6.28), rng.uniform(.6, 2.2), rng.uniform(0, 6.28),
                    int(rng.uniform(*tam)), rng.uniform(.35, 1.0)) for _ in range(n)]

    def dibujar(self, lz, t, alfa=1.0):
        if alfa <= 0:
            return
        x0, y0, x1, y1 = self.zona
        for (px, py, v, sw, ws, ph, wt, ph2, r, ba) in self.ps:
            x = px + sw * math.sin(ws * t + ph)
            y = (py - v * t - y0) % (y1 - y0) + y0
            tw = .2 + .8 * max(0.0, math.sin(wt * t + ph2)) ** 2
            pegar(lz, halo(r, (255, 206, 110), 1.7), x, y, alfa * tw * ba * .8, modo='a')


# ───────────────────────────── texto ─────────────────────────────
def _mascara_texto(txt, f, tam):
    """Máscara L del texto; los «·» se sustituyen por un rombo (Castellar no trae el punto medio)."""
    partes = txt.split('·')
    sep_w = int(tam * 1.15)
    asc, desc = f.getmetrics()
    anchos = [f.getlength(p.strip()) if p.strip() else 0 for p in partes]
    total = int(sum(anchos) + sep_w * (len(partes) - 1)) + 4
    hh = asc + desc
    im = Image.new('L', (max(total, 1), hh), 0)
    d = ImageDraw.Draw(im)
    x = 0
    caps = f.getbbox('H')
    ymid = (caps[1] + caps[3]) / 2
    for i, p in enumerate(partes):
        if p.strip():
            d.text((x, 0), p.strip(), font=f, fill=255)
        x += anchos[i]
        if i < len(partes) - 1:
            cx = x + sep_w / 2
            rr = tam * .13
            d.polygon([(cx, ymid - rr), (cx + rr, ymid), (cx, ymid + rr), (cx - rr, ymid)], fill=255)
            x += sep_w
    arr = np.asarray(im)
    ys, xs = np.nonzero(arr > 8)
    if len(xs) == 0:
        return np.zeros((2, 2), np.float32)
    return arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32) / 255


@functools.lru_cache(None)
def texto(txt, tam, ruta=F_GRAB, estilo='oro', contorno=3, sombra=4, ancla=(.5, .5)):
    """Texto grabado: 'oro' (relieve metálico) o 'marfil'. Contorno oscuro y sombra; ancla = fracción del sprite."""
    f = fuente(ruta, tam)
    m0 = _mascara_texto(txt, f, tam)
    pad = contorno + sombra * 2 + 4
    m = np.pad(m0, pad)
    h, w = m.shape
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    if estilo == 'oro':
        sh = relieve(m, max(1.4, tam * .045))
        col = oro(np.clip(sh * (1.18 - .38 * yy), 0, 1))
    else:
        col = np.ones((h, w, 3), np.float32) * np.array((240, 228, 204), np.float32) * (1.04 - .14 * yy)[..., None]
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * contorno + 1, 2 * contorno + 1))
    mo = cv2.GaussianBlur(cv2.dilate(m, ker), (0, 0), .7)
    ms = cv2.warpAffine(cv2.GaussianBlur(mo, (0, 0), 1 + tam * .05), np.float32([[1, 0, sombra * .6], [0, 1, sombra]]), (w, h)) * .8
    a = ms
    p = np.zeros((h, w, 3), np.float32)
    p = p * (1 - mo)[..., None] + np.array((26, 15, 6), np.float32) * mo[..., None]
    a = mo + a * (1 - mo)
    p = p * (1 - m)[..., None] + col * m[..., None]
    a = m + a * (1 - m)
    return Spr(p, a, pad, ancla)


def placa(txt, tam=30, ruta=F_GRAB, estilo='oro', borde=12, padx=None, gemas=None, seed=4, oscuro=.5):
    """Placa de piedra con filo de oro y texto grabado; gemas = color de los dos remaches."""
    tx = texto(txt, tam, ruta, estilo, 3, 3)
    padx = padx if padx is not None else int(tam * .9) + (int(tam * .7) if gemas else 0)
    w = tx.w - 2 * tx.pad + 2 * padx + 2 * borde
    h = int(tam * 1.25) + 2 * borde + 10
    pl = marco(w, h, borde=borde, radio=borde * .7, interior='piedra', seed=seed, inlay=False, oscuro=oscuro, sombra=8)
    cx, cy = pl.w / 2, pl.h / 2
    pegar_spr(pl, tx, cx, cy + 1)
    if gemas:
        g = gema(int(tam * .5), tuple(gemas), seed=seed, garras=4)
        off = w / 2 - borde - tam * .55
        pegar_spr(pl, g, cx - off, cy)
        pegar_spr(pl, g, cx + off, cy)
    return pl


def engaste(d, ancho=10, seed=0, oscuro=.35):
    """Hueco circular tallado en la piedra con aro de oro (asiento de un ícono)."""
    S = int(d + 4)
    c0 = mascara(S, S, forma('circulo', S, S, 2))
    c1 = mascara(S, S, forma('circulo', S, S, 2 + ancho))
    aro = np.clip(c0 - c1, 0, 1)
    st = piedra(S, S, seed, oscura=oscuro)
    rec = 1 - 1.2 * (relieve(c1, d * .12, 'chaflan') - LUZ[2])
    rgb = oro_de(aro, ancho / 2, seed + 1) * aro[..., None] + st * rec[..., None] * c1[..., None]
    return Spr.rgba(rgb, c0)


def icono_redondo(ruta, d):
    im = Image.open(ruta).convert('RGB').resize((d, d), Image.LANCZOS)
    cob = mascara(d, d, forma('circulo', d, d, 0))
    rgb = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:d, 0:d].astype(np.float32)
    r = np.sqrt((xx - d / 2) ** 2 + (yy - d / 2) ** 2) / (d / 2)
    rgb *= (1 - .45 * np.clip(r - .6, 0, 1) / .4)[..., None]
    return Spr.rgba(rgb, cob)


def foto_enmarcada(ruta, w, h, borde=16, seed=8, tipo='rect'):
    fr = marco(w, h, borde=borde, radio=borde * .6, tipo=tipo, interior='hueco', seed=seed, inlay=borde > 14, sombra=10)
    iw, ih = int(w - 2 * borde + 6), int(h - 2 * borde + 6)
    im = Image.open(ruta).convert('RGB')
    s = max(iw / im.width, ih / im.height)
    im = im.resize((int(math.ceil(im.width * s)), int(math.ceil(im.height * s))), Image.LANCZOS)
    x0, y0 = (im.width - iw) // 2, (im.height - ih) // 2
    ph = np.asarray(im.crop((x0, y0, x0 + iw, y0 + ih))).astype(np.float32)
    lum = ph @ np.array([.299, .587, .114], np.float32)
    ph = (lum[..., None] + (ph - lum[..., None]) * .9) * np.array([1.04, 1.0, .9], np.float32)
    base = Spr(np.zeros((fr.h, fr.w, 3)), np.zeros((fr.h, fr.w)))
    pegar_spr(base, Spr.rgba(ph, np.ones((ih, iw))), fr.w / 2, fr.h / 2)
    pegar_spr(base, fr, fr.w / 2, fr.h / 2)
    base.pad = fr.pad
    return base


def regla_oro(w, seed=0, gema_color=None):
    """Filete de oro horizontal con rombo central."""
    h = 26
    def dib(d, k):
        d.rectangle([0, (h / 2 - 1.6) * k, w * k, (h / 2 + 1.6) * k], fill=255)
        c = w / 2
        d.polygon([((c - 16) * k, h / 2 * k), (c * k, 2 * k), ((c + 16) * k, h / 2 * k), (c * k, (h - 2) * k)], fill=255)
        for s in (-1, 1):
            cx = c + s * (w / 2 - 6)
            d.polygon([((cx - 6) * k, h / 2 * k), (cx * k, (h / 2 - 6) * k), ((cx + 6) * k, h / 2 * k), (cx * k, (h / 2 + 6) * k)], fill=255)
    cob = mascara(w, h, dib)
    sp = Spr.rgba(oro_de(cob, 2.2, seed), cob)
    sp = con_sombra(sp, 3, .8)
    if gema_color:
        pegar_spr(sp, gema(14, tuple(gema_color), garras=0, bisel=.12), sp.w / 2, sp.h / 2)
    return sp


# ───────────────────────────── runas y cadena ─────────────────────────────
_TRAZOS = [((0, -.9), (.62, -.45)), ((0, -.45), (.62, -.9)), ((0, -.9), (-.62, -.45)), ((0, .05), (.62, .55)),
           ((0, .05), (-.62, .55)), ((0, -.35), (.62, .15)), ((0, -.35), (-.62, .15)), ((-.55, -.1), (.55, -.1)),
           ((.62, -.45), (0, .1)), ((-.62, -.45), (0, .1)), ((0, .9), (.55, .5)), ((0, .9), (-.55, .5))]


def glifo(seed, tam):
    rng = np.random.default_rng(seed + 101)
    sel = rng.choice(len(_TRAZOS), 2 + int(rng.integers(0, 2)), replace=False)
    lw = tam * .1

    def dib(d, k):
        def P(x, y):
            return ((tam / 2 + x * tam * .36) * k, (tam / 2 + y * tam * .42) * k)
        for a, b in [((0, -.92), (0, .92))] + [_TRAZOS[i] for i in sel]:
            d.line([P(*a), P(*b)], fill=255, width=int(lw * k))
            for q in (a, b):
                x, y = P(*q)
                d.ellipse([x - lw * k / 2, y - lw * k / 2, x + lw * k / 2, y + lw * k / 2], fill=255)
    return mascara(tam, tam, dib)


def runa(seed, D=44):
    """Devuelve (base apagada, glifo encendido, resplandor). Base = rombo de piedra con filo de oro y glifo grabado."""
    base = marco(D, D, borde=7, tipo='rombo', interior='piedra', seed=seed + 40, inlay=False, oscuro=.55, sombra=4)
    gt = int(D * .5)
    g = glifo(seed, gt)
    # grabado: hendidura oscura con borde claro abajo-derecha
    sh = relieve(g, 1.6)
    eng = np.stack([np.full_like(g, 18), np.full_like(g, 14), np.full_like(g, 10)], -1) + (1 - sh)[..., None] * np.array((70, 56, 30), np.float32)
    pegar_spr(base, Spr.rgba(eng, g * .95), base.w / 2, base.h / 2)
    lit = Spr.rgba(oro(np.clip(relieve(g, 1.6) * 1.2 + .3, 0, 1)), g)
    gl = cv2.GaussianBlur(np.pad(g, 18), (0, 0), 6.0) * 2.4
    glow = Spr(gl[..., None] * np.array((255, 190, 80), np.float32), np.clip(gl, 0, 1))
    return base, lit, glow


@functools.lru_cache(None)
def eslabon(tipo, ang):
    """Eslabón de cadena de oro: 'a' anilla vista de frente, 'b' de canto. ang en grados (dirección de la ruta)."""
    w, h = (27, 16) if tipo == 'a' else (27, 8)

    def dib(d, k):
        if tipo == 'a':
            d.ellipse([1 * k, 1 * k, (w - 1) * k, (h - 1) * k], fill=255)
            d.ellipse([6.5 * k, 5.2 * k, (w - 6.5) * k, (h - 5.2) * k], fill=0)
        else:
            d.rounded_rectangle([1 * k, 1 * k, (w - 1) * k, (h - 1) * k], radius=2 * k, fill=255)
    cob = mascara(w, h, dib)
    sp = Spr.rgba(oro(relieve(cob, 2.6)), cob)
    sp = con_sombra(sp, 2, .85)
    return sp.rotar(-ang)


def bezier(p0, c1, c2, p1, n=500):
    t = np.linspace(0, 1, n)[:, None]
    pts = (1 - t) ** 3 * np.array(p0) + 3 * (1 - t) ** 2 * t * np.array(c1) + 3 * (1 - t) * t ** 2 * np.array(c2) + t ** 3 * np.array(p1)
    seg = np.sqrt((np.diff(pts, axis=0) ** 2).sum(1))
    s = np.concatenate([[0], np.cumsum(seg)])
    return pts, s / s[-1]


def en_ruta(pts, s, f):
    i = int(np.clip(np.searchsorted(s, f), 1, len(s) - 1))
    q = (f - s[i - 1]) / max(1e-9, s[i] - s[i - 1])
    p = pts[i - 1] + (pts[i] - pts[i - 1]) * q
    dx, dy = pts[i] - pts[i - 1]
    return p[0], p[1], math.degrees(math.atan2(dy, dx))


# ───────────────────────────── fondos ─────────────────────────────
def _vineta(w, h, borde=.4, pot=2.2):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2) / 1.414
    return (1 - (1 - borde) * np.clip(r, 0, 1) ** pot).astype(np.float32)


VIG = _vineta(W, H, .32, 1.8)
_U = ((np.arange(W, dtype=np.float32)[None, :] + .5 * np.arange(H, dtype=np.float32)[:, None]) / (W + .5 * H)).astype(np.float32)


class Clip:
    def __init__(self, ruta, inicio=0.0):
        self.ruta, self.inicio = ruta, int(round(inicio * FPS))
        self._abrir(self.inicio)

    def _abrir(self, pos):
        self.cap = cv2.VideoCapture(self.ruta)
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if pos:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        self.idx, self.ult = pos - 1, None

    def cuadro(self, i):
        obj = min(self.inicio + max(0, int(i)), self.n - 1)
        if obj < self.idx or (self.ult is None and obj > self.idx + 1 and obj - self.idx > 90):
            self._abrir(obj)
        while self.idx < obj:
            ok, fr = self.cap.read()
            if not ok:
                break
            self.idx += 1
            self.ult = fr
        return self.ult


def gradar(fr, zoom=1.07, oscuro=.54, satur=.6):
    """Gameplay tratado: recorte leve (quita bordes de interfaz), menos color, tono de oro viejo, viñeta."""
    h, w = fr.shape[:2]
    cw, ch = int(w / zoom), int(h / zoom)
    x0, y0 = (w - cw) // 2, (h - ch) // 2
    f = cv2.resize(fr[y0:y0 + ch, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LINEAR)
    f = cv2.GaussianBlur(f, (0, 0), 1.6)[..., ::-1].astype(np.float32)
    lum = f @ np.array([.299, .587, .114], np.float32)
    f = lum[..., None] + (f - lum[..., None]) * satur
    f *= np.array([1.08, .97, .78], np.float32) * oscuro
    f *= VIG[..., None]
    return f


def transicion(A, B, x):
    """Barrido de luz dorada en diagonal: detrás de la franja ya está la escena nueva."""
    pos = lerp(-.12, 1.12, eio(x))
    e = np.clip((pos - _U) / .05 + .5, 0, 1)[..., None]
    out = A * (1 - e) + B * e
    banda = np.exp(-((_U - pos) / .03) ** 2) * (math.sin(math.pi * x) * 190)
    out += banda[..., None] * np.array([1.0, .82, .5], np.float32)
    return out


# ───────────────────────────── 1 · MAPA CON RUTA ─────────────────────────────
class MapaRuta:
    def __init__(self, mapa, zona, puntos, ruta=(0, 1), foto=None, rotulo_final='', t0=0.0,
                 rect=(30, 52, 1890, 1050), borde=44, vista_ini=None, vista_fin=None, empuje=.06,
                 ctrl=((0, -70), (-10, 70)), tiempos=None, colores_esquina=None, seed=2):
        """puntos: [dict(xy=(%x, %y), nombre, color, d, lado='izq'|'der'|'abajo', t, tam)] (t relativo a t0).
        ruta=(i, j): de puntos[i] a puntos[j]; el destino lleva `foto` y `rotulo_final`."""
        self.t0 = t0
        T = dict(marco=(0, .9), mapa=(.3, 1.2), esquinas=.7, titulo=1.1, zoom=(1.8, 4.6), ruta=(5.8, 8.4),
                 final=8.35, foto=8.9, rotulo=9.3, fin=11.3)
        T.update(tiempos or {})
        self.T = T
        img = cv2.imread(mapa)[..., ::-1].astype(np.float32)
        lum = img @ np.array([.299, .587, .114], np.float32)
        img = lum[..., None] + (img - lum[..., None]) * .8
        img = (img - 128) * 1.08 + 128
        img *= np.array([1.05, .98, .84], np.float32)
        img = img + .6 * (img - cv2.GaussianBlur(img, (0, 0), 1.3))
        self.mapa = np.clip(img, 0, 255).astype(np.float32)
        self.mh, self.mw = self.mapa.shape[:2]
        self.rect = rect
        x0, y0, x1, y1 = rect
        self.win = (x0 + borde, y0 + borde, x1 - borde, y1 - borde)
        self.ww, self.wh = self.win[2] - self.win[0], self.win[3] - self.win[1]
        self.vig = _vineta(self.ww, self.wh, .5, 2.0)[..., None]
        self.marco = marco(x1 - x0, y1 - y0, borde=borde, radio=20, interior='hueco', seed=seed, adornos=True, sombra=16)
        self.fondo = piedra(H, W, seed + 50, oscura=.55) * VIG[..., None]
        self.esquinas = [(x0 + borde / 2, y0 + borde / 2), (x1 - borde / 2, y0 + borde / 2),
                         (x0 + borde / 2, y1 - borde / 2), (x1 - borde / 2, y1 - borde / 2)]
        self.col_esq = colores_esquina or [GEMA['rojo'], GEMA['ambar'], GEMA['azul'], GEMA['verde']]
        self.titulo = placa(zona, 46, borde=20, gemas=GEMA['ambar'], seed=seed + 3)
        self.puntos = []
        for p in puntos:
            q = dict(lado='izq', d=40, tam=28, color=GEMA['azul'])
            q.update(p)
            q['px'] = (q['xy'][0] / 100 * self.mw, q['xy'][1] / 100 * self.mh)
            q['gem'] = gema(q['d'], tuple(q['color']), seed=len(self.puntos), punta=.8)
            q['placa'] = placa(q['nombre'], q['tam'], seed=7 + len(self.puntos)) if q.get('nombre') else None
            self.puntos.append(q)
        a, b = self.puntos[ruta[0]], self.puntos[ruta[1]]
        self.dest = b
        p0, p1 = np.array(a['px']), np.array(b['px'])
        self.pts, self.s = bezier(p0, p0 + ctrl[0], p1 + ctrl[1], p1)
        self.foto = foto_enmarcada(foto, 430, 262, borde=16) if foto else None
        self.rot_final = placa(rotulo_final, 30, seed=19, gemas=GEMA['rojo']) if rotulo_final else None
        self.foto_gema = gema(26, GEMA['rojo'], seed=5, garras=4)
        # cámara
        ar = self.wh / self.ww
        self.v0 = vista_ini or (self.mw / 2, min(self.mw * ar / 2, self.mh / 2), self.mw)
        if vista_fin is None:
            xs = [p['px'][0] for p in self.puntos]
            ys = [p['px'][1] for p in self.puntos]
            vista_fin = ((min(xs) + max(xs)) / 2 + 30, (min(ys) + max(ys)) / 2 - 10, 820)
        self.v1 = vista_fin
        self.empuje = empuje
        # cadena: eslabones cada ~6.5 px de mapa, runas cada ~32
        L = float(np.sum(np.sqrt((np.diff(self.pts, axis=0) ** 2).sum(1))))
        self.f_ini, self.f_fin = 0.0, 1 - 5 / L
        self.eslabones = []
        n = int((self.f_fin - self.f_ini) * L / 8.2)
        for i in range(n + 1):
            f = lerp(self.f_ini, self.f_fin, i / n)
            _, _, an = en_ruta(self.pts, self.s, f)
            self.eslabones.append((f, eslabon('a' if i % 2 == 0 else 'b', round(an))))
        nr = 5
        self.runas = []
        for i in range(nr):
            f = lerp(.22, .86, i / (nr - 1))
            self.runas.append((f,) + runa(seed * 10 + i, 52))
        self.polvo = Polvo(60, seed + 1, (self.win[0], self.win[1], self.win[2], self.win[3]))

    def camara(self, t):
        z = eio(pr(t, *self.T['zoom']))
        cx = lerp(self.v0[0], self.v1[0], z)
        cy = lerp(self.v0[1], self.v1[1], z)
        cw = math.exp(lerp(math.log(self.v0[2]), math.log(self.v1[2]), z))
        cw *= 1 - self.empuje * pr(t, self.T['zoom'][1], self.T['fin'])
        return cx, cy, cw

    def a_pantalla(self, cam, x, y):
        cx, cy, cw = cam
        s = self.ww / cw
        ch = cw * self.wh / self.ww
        return self.win[0] + (x - (cx - cw / 2)) * s, self.win[1] + (y - (cy - ch / 2)) * s

    def _marcador(self, lz, t, q, cam, dur=.55):
        t1 = q['t']
        if t < t1:
            return None
        X, Y = self.a_pantalla(cam, *q['px'])
        x = pr(t, t1, t1 + dur)
        off = -170 * (1 - ebounce(x))
        g = q['gem']
        hc = (g.ancla[1] * g.h - g.centro[1])  # pico → centro de la gema
        pegar(lz, halo(26, (0, 0, 0), 1.6), X, Y, .5 * x, s=1.0, modo='n')
        pegar(lz, g, X, Y + off, pr(x, 0, .15))
        ti = t1 + dur * .364
        flash(lz, t, ti, X, Y - hc, 1.0)
        onda(lz, t, ti, X, Y, 120, .55)
        estallido(lz, t, ti, X, Y - hc * .5, 18, seed=int(t1 * 10), vel=(90, 260), vida=.9)
        if t > ti + .6:
            chispa_periodica(lz, t, X - q['d'] * .2, Y - hc - q['d'] * .2, fase=t1 * .37, tam=.28)
        if q['placa'] is not None:
            e = pr(t, t1 + .45, t1 + .85)
            if e > 0:
                pl = q['placa']
                pw = pl.w - 2 * pl.pad
                s = lerp(.7, 1, eback(e))
                if q['lado'] == 'izq':
                    pegar(lz, pl, X - 30 - pw / 2 * s, Y - hc, e, s=s)
                elif q['lado'] == 'der':
                    pegar(lz, pl, X + 30 + pw / 2 * s, Y - hc, e, s=s)
                else:
                    pegar(lz, pl, X, Y + 34, e, s=s)
        return X, Y, hc

    def dibujar(self, lz, t):
        t = t - self.t0
        T = self.T
        lz[:] = self.fondo
        cam = self.camara(t)
        cx, cy, cw = cam
        s = self.ww / cw
        ch = cw * self.wh / self.ww
        M = np.float32([[s, 0, -(cx - cw / 2) * s], [0, s, -(cy - ch / 2) * s]])
        win = cv2.warpAffine(self.mapa, M, (self.ww, self.wh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        win *= self.vig
        am = eo(pr(t, *T['mapa']))
        x0, y0, x1, y1 = self.win
        reg = lz[y0:y1, x0:x1]
        lz[y0:y1, x0:x1] = reg * (1 - am) + win * am
        # marco
        e = eo(pr(t, *T['marco']))
        mx, my = (self.rect[0] + self.rect[2]) / 2, (self.rect[1] + self.rect[3]) / 2
        pegar(lz, self.marco, mx, my, e, s=lerp(1.035, 1, e))
        for i, (ex, ey) in enumerate(self.esquinas):
            te = T['esquinas'] + i * .18
            if t >= te:
                x = pr(t, te, te + .3)
                pegar(lz, gema(30, tuple(self.col_esq[i]), seed=20 + i), ex, ey, x, s=lerp(1.7, 1, eo(x)))
                flash(lz, t, te + .22, ex, ey, .7)
                chispa_periodica(lz, t, ex - 5, ey - 5, fase=i * .23, periodo=3.3, tam=.25)
        # ruta: cadena de oro + runas que se encienden
        prog = eio(pr(t, *T['ruta']))
        if prog > 0:
            for f, sp in self.eslabones:
                if prog >= f:
                    X, Y = self.a_pantalla(cam, *en_ruta(self.pts, self.s, f)[:2])
                    pop = cl((prog - f) / .035)
                    pegar(lz, sp, X, Y, pop, s=lerp(1.6, 1, eo(pop)))
            for f, base, lit, glow in self.runas:
                if prog >= f:
                    X, Y = self.a_pantalla(cam, *en_ruta(self.pts, self.s, f)[:2])
                    ap = cl((prog - f) / .05)
                    pegar(lz, base, X, Y, ap, s=lerp(.3, 1, eback(ap)))
                    li = cl((prog - f) / .09)
                    pul = .55 + .3 * math.sin(2 * math.pi * (t * .8) - f * 9)
                    pegar(lz, halo(34, (255, 170, 60), 1.8), X, Y, li * pul * .55, modo='a')
                    pegar(lz, glow, X, Y, li * pul * 1.3, modo='a')
                    pegar(lz, lit, X, Y, li)
                    fl = math.exp(-((prog - f - .035) / .03) ** 2)
                    if fl > .02:
                        pegar(lz, destello(), X, Y, fl, s=.55, modo='a')
            if prog < 1:
                X, Y = self.a_pantalla(cam, *en_ruta(self.pts, self.s, prog)[:2])
                pegar(lz, halo(30), X, Y, .9, modo='a')
                pegar(lz, destello(), X, Y, .75, s=.4, modo='a')
        # marcadores
        dest = None
        for q in self.puntos:
            r = self._marcador(lz, t, q, cam)
            if q is self.dest:
                dest = r
        # foto + rótulo del destino
        if dest is not None and self.foto is not None:
            X, Y, hc = dest
            e = pr(t, T['foto'], T['foto'] + .6)
            if e > 0:
                fw = self.foto.w - 2 * self.foto.pad
                fx = X + 90 + fw / 2
                fy = Y - hc + 45
                sc = lerp(.55, 1, eback(e))
                pegar(lz, self.foto, fx, fy, pr(e, 0, .4), s=sc)
                if e >= 1:
                    gx, gy = fx, fy - (self.foto.h - 2 * self.foto.pad) / 2 + 1
                    pegar(lz, self.foto_gema, gx, gy)
                    flash(lz, t, T['foto'] + .65, gx, gy, .6)
                    chispa_periodica(lz, t, gx - 4, gy - 4, fase=.6, tam=.25)
                if self.rot_final is not None:
                    e2 = pr(t, T['rotulo'], T['rotulo'] + .5)
                    if e2 > 0:
                        rw = self.rot_final.w - 2 * self.rot_final.pad
                        fh = self.foto.h - 2 * self.foto.pad
                        rx, ry = X + 90 + rw / 2, fy + fh / 2 + 52
                        pegar(lz, barrido(self.rot_final, lerp(-.2, 1.2, pr(t, T['rotulo'] + .5, T['rotulo'] + 1.4)))
                              if T['rotulo'] + .5 < t < T['rotulo'] + 1.4 else self.rot_final,
                              rx, ry + 20 * (1 - eo(e2)), e2)
        # título de zona
        if t >= T['titulo']:
            e = pr(t, T['titulo'], T['titulo'] + .7)
            ty = lerp(-70, self.win[1], eback(e))
            sp = self.titulo
            ts = T['titulo'] + .9
            if ts < t < ts + 1.0:
                sp = barrido(sp, lerp(-.15, 1.15, pr(t, ts, ts + 1.0)))
            pegar(lz, sp, W / 2, ty, pr(e, 0, .3))
            if e >= 1:
                chispa_periodica(lz, t, W / 2 - (sp.w / 2 - sp.pad) + 46, self.win[1] - 4, fase=.1, periodo=3.1, tam=.3)
        self.polvo.dibujar(lz, t, pr(t, .5, 1.5))


def mapa_ruta(*a, **kw):
    return MapaRuta(*a, **kw)


# ───────────────────────────── 2 · FICHA ─────────────────────────────
class Ficha:
    def __init__(self, titulo, iconos, etiqueta='×15', valor=15, total=None, t0=11.0, centro=(960, 560),
                 tam=(1500, 560), t_iconos=None, t_salida=None, colores=None, seed=31):
        self.t0, self.centro = t0, centro
        self.n = len(iconos)
        self.valor = valor
        self.total = total if total is not None else valor * self.n
        self.t_iconos = t_iconos or [t0 + 1.8 + i * .9 for i in range(self.n)]
        self.t_salida = t_salida if t_salida is not None else t0 + 9.25
        w, h = tam
        self.w, self.h = w, h
        self.colores = colores or [GEMA['rojo'], GEMA['ambar'], GEMA['azul'], GEMA['verde']]
        tab = marco(w, h, borde=40, radio=18, interior='piedra', seed=seed, adornos=True, oscuro=.56, sombra=20)
        P = tab.pad
        # título (ajustado al ancho)
        ts = 50
        while True:
            self.tit = texto(titulo, ts)
            if self.tit.w - 2 * self.tit.pad <= w - 230 or ts < 30:
                break
            ts -= 2
        pegar_spr(tab, regla_oro(int(w * .72), seed, GEMA['rojo']), P + w / 2, P + 158)
        # engastes
        self.d_eng = 178
        self.xs = [190 + i * 235 for i in range(self.n)]
        self.y_eng = 300
        for i, x in enumerate(self.xs):
            pegar_spr(tab, engaste(self.d_eng, 11, seed + i), P + x, P + self.y_eng)
        # cartucho del contador
        cx0, cx1 = self.xs[-1] + 245, w - 70
        self.cx_num = (cx0 + cx1) / 2 + 40
        self.x_igual = cx0 + 10
        cw_, chh = int(cx1 - cx0 - 50), 200
        car = marco(cw_, chh, borde=14, radio=12, interior='piedra', seed=seed + 9, inlay=False, oscuro=.38, sombra=0)
        pegar_spr(tab, car, P + self.cx_num, P + self.y_eng)
        self.tab = tab
        self.iconos = [icono_redondo(r, self.d_eng - 28) for r in iconos]
        self.etq = texto(etiqueta, 46)
        self.igual = texto('=', 110)
        self.polvo_burst = None
        self.esq = [(40 / 2, 40 / 2), (w - 20, 20), (20, h - 20), (w - 20, h - 20)]

    def _num(self, v):
        return texto(str(int(v)), 150)

    def dibujar(self, lz, t):
        T0 = self.t0
        e_in = pr(t, T0 + .25, T0 + 1.0)
        if e_in <= 0:
            return
        e_out = pr(t, self.t_salida, self.t_salida + .6)
        if e_out >= 1:
            return
        a = eo(e_in) * (1 - e_out)
        dy = 90 * (1 - eo(e_in)) + 70 * eio(e_out)
        sc = lerp(.93, 1, eo(e_in)) * lerp(1, .95, eio(e_out))
        cx, cy = self.centro[0], self.centro[1] + dy
        x0, y0 = cx - self.w / 2 * sc, cy - self.h / 2 * sc

        def L(x, y):  # coordenadas locales → pantalla
            return x0 + x * sc, y0 + y * sc
        pegar(lz, self.tab, cx, cy, a, s=sc)
        estallido(lz, t, T0 + .95, cx, y0 + self.h * sc, 30, seed=7, vel=(120, 520), vida=.8, alfa=.8)
        # esquinas: gema por cristal
        for i, (ex, ey) in enumerate(self.esq):
            ti = self.t_iconos[i] if i < self.n else T0 + 1
            X, Y = L(ex, ey)
            lit = pr(t, ti + .3, ti + .5)
            pegar(lz, gema(28, tuple(self.colores[i % 4]), seed=40 + i, apagada=True), X, Y, a)
            if lit > 0:
                pegar(lz, halo(30, tuple(self.colores[i % 4]), 1.8), X, Y, lit * a * .7, modo='a')
                pegar(lz, gema(28, tuple(self.colores[i % 4]), seed=40 + i), X, Y, lit * a)
                flash(lz, t, ti + .35, X, Y, .7)
        # título con revelado de izquierda a derecha
        r = pr(t, T0 + .9, T0 + 1.6)
        if r > 0:
            sp, c0 = self.tit.cols(0, eio(r))
            tx, ty = L(self.w / 2, 98)
            tw = self.tit.w * sc
            if t > T0 + 2.0 and t < T0 + 3.0:
                sp, c0 = barrido(self.tit, pr(t, T0 + 2.0, T0 + 3.0) * 1.3 - .15).cols(0, 1)
            pegar(lz, sp, tx - tw / 2 + c0 * sc, ty - self.tit.h * sc / 2, a, s=sc, ancla=(0, 0))
            if r < 1:
                pegar(lz, destello(), tx - tw / 2 + self.tit.w * eio(r) * sc, ty, .8, s=.45, modo='a')
        # cristales
        cuenta = 0.0
        for i, ti in enumerate(self.t_iconos):
            if t < ti:
                continue
            x = pr(t, ti, ti + .45)
            X, Y = L(self.xs[i], self.y_eng)
            pegar(lz, self.iconos[i], X, Y - 60 * (1 - eo(x)), pr(x, 0, .3) * a, s=sc * lerp(1.5, 1, eo(x)))
            flash(lz, t, ti + .35, X, Y, 1.0)
            onda(lz, t, ti + .35, X, Y, 140, .5)
            estallido(lz, t, ti + .35, X, Y, 16, seed=50 + i, vel=(100, 300), vida=.8)
            if t > ti + 1.2:
                chispa_periodica(lz, t, X - 30, Y - 34, fase=i * .27, periodo=3.0, tam=.3)
            e2 = pr(t, ti + .4, ti + .75)
            if e2 > 0:
                ex, ey = L(self.xs[i], 445)
                pegar(lz, self.etq, ex, ey + 18 * (1 - eo(e2)), e2 * a, s=sc)
            cuenta += self.valor * eo(pr(t, ti + .35, ti + .8))
        # contador
        e3 = pr(t, T0 + 1.5, T0 + 1.9)
        if e3 > 0:
            X, Y = L(self.x_igual, self.y_eng)
            pegar(lz, self.igual, X, Y, e3 * a, s=sc)
            NX, NY = L(self.cx_num, self.y_eng + 4)
            tfin = self.t_iconos[-1] + .8
            pulso = 1 + .16 * math.exp(-((t - tfin) / .12) ** 2) if t > tfin - .3 else 1
            num = self._num(round(cuenta))
            if t > tfin + .2 and t < tfin + 1.2:
                num = barrido(num, pr(t, tfin + .2, tfin + 1.2) * 1.3 - .15)
            pegar(lz, num, NX, NY, e3 * a, s=sc * pulso)
            if t > tfin - .05:
                pegar(lz, halo(110, (255, 190, 80), 2.2), NX, NY, .45 * math.exp(-((t - tfin) / .5) ** 2) * a, modo='a')
            flash(lz, t, tfin, NX, NY, 1.4, .7)
            onda(lz, t, tfin, NX, NY, 230, .7)
            estallido(lz, t, tfin, NX, NY, 34, seed=77, vel=(160, 520), vida=1.2)


def ficha(*a, **kw):
    return Ficha(*a, **kw)


# ───────────────────────────── 3 · TARJETA (relicario) ─────────────────────────────
class Tarjeta:
    def __init__(self, foto, linea1, linea2, sub, t0=21.0, rect=(1240, 120, 600, 860), t_salida=None,
                 elementos=None, gema_clave=GEMA['rojo'], seed=61):
        self.t0 = t0
        self.x, self.y, self.w, self.h = rect
        self.t_salida = t_salida if t_salida is not None else t0 + 7.5
        self.elementos = elementos or [GEMA['rojo'], GEMA['azul'], GEMA['verde'], GEMA['ambar']]
        w, h = self.w, self.h
        card = marco(w, h, borde=40, radio=16, tipo='arco', interior='piedra', seed=seed, adornos=True, oscuro=.55, sombra=22)
        P = card.pad
        # rayos de oro en el tímpano
        self.kc = (w / 2, 150)

        def ray(d, k):
            for i in range(9):
                an = math.radians(-180 + i * 22.5)
                L0 = 62
                L1 = 95 + 45 * abs(math.cos(an))
                xa, ya = self.kc[0] + L0 * math.cos(an), self.kc[1] + L0 * math.sin(an)
                xb, yb = self.kc[0] + L1 * math.cos(an), self.kc[1] + L1 * math.sin(an)
                nx, ny = -math.sin(an), math.cos(an)
                wa = 5.5
                d.polygon([((xa + nx * wa) * k, (ya + ny * wa) * k), ((xa - nx * wa) * k, (ya - ny * wa) * k), (xb * k, yb * k)], fill=255)
        rc = mascara(w, h, ray)
        pegar_spr(card, con_sombra(Spr.rgba(oro_de(rc, 2.5, seed), rc), 3, .8), P + w / 2, P + h / 2)
        # anillo de la gema clave
        pegar_spr(card, engaste(112, 9, seed + 3, oscuro=.3), P + self.kc[0], P + self.kc[1])
        self.foto = foto_enmarcada(foto, 480, 272, borde=18, seed=seed + 4)
        pegar_spr(card, self.foto, P + w / 2, P + 236 + 136)
        pegar_spr(card, regla_oro(400, seed, GEMA['rojo']), P + w / 2, P + 668)
        self.xg = [w / 2 + (i - 1.5) * 96 for i in range(4)]
        self.yg = 772
        for x in self.xg:
            pegar_spr(card, engaste(58, 6, seed + 11, oscuro=.3), P + x, P + self.yg)
        self.card = card
        self.l1 = texto(linea1, 32, estilo='marfil', contorno=3, sombra=3)
        self.l2 = texto(linea2, 74)
        self.sub = texto(sub, 31, F_SERIF_I, 'marfil', 3, 3)
        self.gclave = gema(84, tuple(gema_clave), seed=9, garras=6)

    def dibujar(self, lz, t):
        T0 = self.t0
        e = pr(t, T0 + .3, T0 + 1.2)
        if e <= 0:
            return
        eo_ = pr(t, self.t_salida, self.t_salida + .8)
        if eo_ >= 1:
            return
        dx = 760 * (1 - eo(e)) + 800 * eio(eo_)
        a = pr(e, 0, .35) * (1 - pr(eo_, .6, 1))
        X0, Y0 = self.x + dx, self.y

        def L(x, y):
            return X0 + x, Y0 + y
        pegar(lz, self.card, X0 - self.card.pad, Y0 - self.card.pad, a, ancla=(0, 0))
        # gema clave
        kx, ky = L(*self.kc)
        tk = T0 + 1.15
        if t >= tk:
            x = pr(t, tk, tk + .35)
            pegar(lz, halo(70, (255, 80, 70), 1.8), kx, ky, .35 * x * a, modo='a')
            pegar(lz, self.gclave, kx, ky, x * a, s=lerp(1.6, 1, eo(x)))
            flash(lz, t, tk + .28, kx, ky, 1.2)
            onda(lz, t, tk + .28, kx, ky, 180, .6)
            chispa_periodica(lz, t, kx - 18, ky - 18, fase=.4, periodo=2.6, tam=.4)
        flash(lz, t, self.t_salida, kx, ky, 1.3, .6)
        # foto: aparece desde oscuro con un barrido
        e2 = pr(t, T0 + 1.0, T0 + 1.6)
        if e2 < 1:
            fx, fy = L(self.w / 2, 236 + 136)
            reg_h, reg_w = 272 - 36, 480 - 36
            x0, y0 = int(fx - reg_w / 2), int(fy - reg_h / 2)
            x0c, x1c = max(0, x0), min(W, x0 + reg_w)
            if x1c > x0c:
                lz[y0:y0 + reg_h, x0c:x1c] *= (1 - .85 * (1 - eo(e2)))
        # textos
        for sp, ty, ts in ((self.l1, 562, T0 + 1.5), (self.l2, 616, T0 + 1.7), (self.sub, 712, T0 + 2.1)):
            x = pr(t, ts, ts + .5)
            if x > 0:
                q = sp
                if sp is self.l2 and T0 + 2.3 < t < T0 + 3.3:
                    q = barrido(sp, pr(t, T0 + 2.3, T0 + 3.3) * 1.3 - .15)
                tx, tyy = L(self.w / 2, ty + 16 * (1 - eo(x)))
                pegar(lz, q, tx, tyy, x * a)
        # gemas de elemento: se encienden por turnos (cada 25 %)
        tg = T0 + 2.4
        for i, xg in enumerate(self.xg):
            gx, gy = L(xg, self.yg)
            col = tuple(self.elementos[i])
            ap = pr(t, tg + i * .12, tg + i * .12 + .3)
            if ap <= 0:
                continue
            pegar(lz, gema(40, col, seed=70 + i, apagada=True, garras=4), gx, gy, ap * a)
            if t > tg + .6:
                k = int((t - tg - .6) / .6) % 4
                fase = ((t - tg - .6) / .6) % 1
                if k == i:
                    v = math.sin(math.pi * fase)
                    pegar(lz, halo(44, col, 1.6), gx, gy, .8 * v * a, modo='a')
                    pegar(lz, gema(40, col, seed=70 + i, garras=4), gx, gy, min(1, v * 1.6) * a)
                    if fase < .3:
                        flash(lz, t, t - fase * .6, gx, gy, .45)


def tarjeta(*a, **kw):
    return Tarjeta(*a, **kw)


# ───────────────────────────── 3b · RÓTULO INFERIOR + SELLO ─────────────────────────────
def sello(d=170, txt='5', seed=81):
    """Medallón de oro: aro con perlas, campo rebajado y cifra en relieve."""
    S = int(d)
    c0 = mascara(S, S, forma('circulo', S, S, 0))
    c1 = mascara(S, S, forma('circulo', S, S, d * .1))
    c2 = mascara(S, S, forma('circulo', S, S, d * .19))
    aro = np.clip(c0 - c1, 0, 1)
    perl = np.clip(c1 - c2, 0, 1)
    rgb = oro_de(aro, d * .05, seed) * aro[..., None]
    # perlas
    def dib(dd, k):
        rr = d * .5 - d * .145
        for i in range(20):
            an = i * 2 * math.pi / 20
            x, y = S / 2 + rr * math.cos(an), S / 2 + rr * math.sin(an)
            q = d * .026
            dd.ellipse([(x - q) * k, (y - q) * k, (x + q) * k, (y + q) * k], fill=255)
    pc = mascara(S, S, dib)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rr = np.sqrt((xx - S / 2) ** 2 + (yy - S / 2) ** 2)
    rec = -(relieve(c1, d * .06, 'chaflan') - LUZ[2]) * .9          # rebajado: luz invertida en el borde
    guil = .05 * np.sin(rr * 1.1) + .04 * np.sin(np.arctan2(yy - S / 2, xx - S / 2) * 24)   # guilloché
    campo = oro(np.clip(.44 + rec + guil - .1 * (rr / (S / 2)), 0, 1))
    rgb = rgb + campo * c1[..., None]
    rgb = rgb * (1 - pc[..., None]) + oro(relieve(pc, d * .02)) * pc[..., None]
    sp = Spr.rgba(rgb, c0)
    num = texto(txt, int(d * .52), contorno=3, sombra=3)
    pegar_spr(sp, num, S / 2, S / 2 + d * .02)
    return con_sombra(sp, 10, .75)


class Rotulo:
    def __init__(self, texto_, sello_txt='5', t0=21.0, pos=(215, 905), ancho=900, t_salida=None, seed=91):
        self.t0, self.pos, self.ancho = t0, pos, ancho
        self.t_salida = t_salida if t_salida is not None else t0 + 7.3
        self.barra = marco(ancho, 112, borde=18, radio=14, interior='piedra', seed=seed, inlay=True, oscuro=.48, sombra=12)
        self.txt = texto(texto_, 52, F_SERIF, 'oro', 3, 4)
        self.sello = sello(170, sello_txt)

    def dibujar(self, lz, t):
        T0 = self.t0
        ts = T0 + 2.6
        if t < ts:
            return
        x0, y0 = self.pos
        so = pr(t, self.t_salida, self.t_salida + .5)    # barra se recoge
        so2 = pr(t, self.t_salida + .4, self.t_salida + .8)  # sello se va
        if so2 >= 1:
            return
        # barra (se despliega desde el sello hacia la derecha)
        r = eio(pr(t, ts + .4, ts + 1.0)) * (1 - eio(so))
        if r > 0:
            b = self.barra
            sp, c0 = b.cols(0, (b.pad + 40 + (b.w - 2 * b.pad - 40) * r) / b.w)
            pegar(lz, sp, x0 - b.pad, y0 - b.h / 2, 1, ancla=(0, 0))
            rt = pr(t, ts + .8, ts + 1.4) * (1 - pr(so, 0, .4))
            if rt > 0:
                q = self.txt
                if ts + 2.0 < t < ts + 3.0:
                    q = barrido(q, pr(t, ts + 2.0, ts + 3.0) * 1.3 - .15)
                tsp, c1 = q.cols(0, eio(rt))
                tx = x0 + 112
                pegar(lz, tsp, tx - q.pad + c1, y0 - q.h / 2 + 2, 1, ancla=(0, 0))
        # sello que se estampa
        x = pr(t, ts, ts + .4)
        s = lerp(2.3, 1, eo(x) ** 1.5) * lerp(1, .2, ei(so2))
        a = pr(x, 0, .5) * (1 - so2)
        pegar(lz, self.sello, x0, y0, a, s=s)
        ti = ts + .4
        flash(lz, t, ti, x0, y0, 1.3, .6)
        onda(lz, t, ti, x0, y0, 210, .6)
        estallido(lz, t, ti, x0, y0, 30, seed=91, vel=(150, 480), vida=1.0)
        flash(lz, t, self.t_salida + .45, x0, y0, 1.0, .5)
        if t > ti + .8 and so2 == 0:
            chispa_periodica(lz, t, x0 - 40, y0 - 44, fase=.75, periodo=2.9, tam=.35)


def ei(x):
    return x ** 3


def rotulo(*a, **kw):
    return Rotulo(*a, **kw)


# ───────────────────────────── montaje del video de muestra ─────────────────────────────
class Video:
    def __init__(self):
        S = SRC
        self.esc1 = mapa_ruta(
            os.path.join(S, 'mapas', 'ungoro_norte.jpg'), 'CRÁTER DE UN’GORO',
            [dict(xy=(43.6, 23.0), nombre='REFUGIO DE LOS MARISCALES', color=GEMA['azul'], d=40, lado='izq', t=4.4, tam=28),
             dict(xy=(45.2, 22.8), nombre='GRYFE · VUELO', color=GEMA['ambar'], d=24, lado='der', t=5.15, tam=20),
             dict(xy=(47.3, 10.8), nombre=None, color=GEMA['rojo'], d=54, lado='der', t=8.35)],
            ruta=(0, 2), foto=os.path.join(S, 'pegatinas', 'bancal_creador.png'),
            rotulo_final='BANCAL DEL CREADOR · 58-60', t0=0.0,
            vista_fin=(790, 228, 780), ctrl=((-6, -70), (-50, 55)))
        self.ficha = ficha('N.º 15 · SIN LOS 60 CRISTALES',
                           [os.path.join(S, 'pegatinas', f'o_cristal_{c}.png') for c in ('rojo', 'amarillo', 'azul', 'verde')],
                           '×15', 15, 60, t0=11.0, t_iconos=[12.8, 13.7, 14.6, 15.5], t_salida=20.2)
        self.tarj = tarjeta(os.path.join(S, 'pegatinas', 'bancal_creador.png'), 'JEFA FINAL:', 'NANAYA',
                            'cambia de elemento cada 25 %', t0=21.0, t_salida=28.5)
        self.rot = rotulo('Sin cristales: solo 5 jefes', '5', t0=21.0, t_salida=28.2)
        self.c89 = Clip(os.path.join(S, 'medios', 'scene-089.mp4'), .3)
        self.c91 = Clip(os.path.join(S, 'medios', 'scene-091.mp4'), .2)
        self.c93 = Clip(os.path.join(S, 'medios', 'scene-093.mp4'), .3)
        self.polvo = Polvo(80, 9)
        self.marca = texto(NOMBRE, 22, contorno=2, sombra=2, ancla=(0, 0))

    def escena1(self, t):
        lz = np.empty((H, W, 3), np.float32)
        self.esc1.dibujar(lz, t)
        return lz

    def escena2(self, t):
        L = t - 10.7
        A = gradar(self.c89.cuadro(L * FPS))
        if L > 5.0:
            B = gradar(self.c91.cuadro((L - 5.0) * FPS))
            x = eio(pr(L, 5.0, 5.6))
            A = A * (1 - x) + B * x
        self.polvo.dibujar(A, t)
        self.ficha.dibujar(A, t)
        return A

    def escena3(self, t):
        L = t - 20.7
        A = gradar(self.c93.cuadro(L * FPS), oscuro=.74)
        self.polvo.dibujar(A, t)
        self.tarj.dibujar(A, t)
        self.rot.dibujar(A, t)
        return A

    def cuadro(self, t):
        if t < 10.7:
            lz = self.escena1(t)
        elif t < 11.3:
            lz = transicion(self.escena1(t), self.escena2(t), pr(t, 10.7, 11.3))
        elif t < 20.7:
            lz = self.escena2(t)
        elif t < 21.3:
            lz = transicion(self.escena2(t), self.escena3(t), pr(t, 20.7, 21.3))
        else:
            lz = self.escena3(t)
        f = pr(t, 29.25, 29.97)
        if f > 0:
            lz *= 1 - eio(f)
        pegar(lz, self.marca, 34, 14, .82)
        return np.clip(lz, 0, 255).astype(np.uint8)


def render():
    v = Video()
    wav = os.path.join(SRC, 'audio', 'wow', 'nlXOcybLHxc.wav')
    # «−18 dB»: la pista está a −21,6 LUFS en estos 30 s; +3,6 dB la deja en −18 LUFS (pico −3,9 dBFS).
    af = 'volume=3.6dB,afade=t=in:st=0:d=1.5,afade=t=out:st=27.3:d=2.7'
    cmd = [FFMPEG, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-t', str(DUR), '-i', wav, '-filter_complex', f'[1:a]{af}[a]', '-map', '0:v', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-threads', '3',
           '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), '-movflags', '+faststart', SALIDA]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    import time
    t0 = time.time()
    for i in range(n):
        p.stdin.write(v.cuadro(i / FPS).tobytes())
        if i % 60 == 0:
            print(f'  cuadro {i}/{n}  {time.time() - t0:.0f} s', flush=True)
    p.stdin.close()
    p.wait()
    print('listo', SALIDA, f'{time.time() - t0:.0f} s')


def hoja():
    tmp = os.path.join(AQUI, '_tmp')
    os.makedirs(tmp, exist_ok=True)
    ims = []
    for k in range(12):
        t = 1.25 + 2.5 * k
        out = os.path.join(tmp, f'h{k:02d}.jpg')
        subprocess.run([FFMPEG, '-y', '-v', 'error', '-ss', f'{t:.3f}', '-i', SALIDA, '-frames:v', '1', '-vf', 'scale=640:360', out], check=True)
        im = Image.open(out).convert('RGB')
        ImageDraw.Draw(im).text((8, 336), f'{t:.2f} s', fill=(255, 255, 255), font=fuente(F_SERIF, 18))
        ims.append(im)
    sheet = Image.new('RGB', (640 * 4, 360 * 3))
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % 4) * 640, (k // 4) * 360))
    sheet.save(os.path.join(AQUI, 'hoja.jpg'), quality=88)
    print('hoja', os.path.join(AQUI, 'hoja.jpg'))


if __name__ == '__main__':
    if '--cuadros' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--cuadros') + 1:]]
        v = Video()
        tmp = os.path.join(AQUI, '_tmp')
        os.makedirs(tmp, exist_ok=True)
        for t in ts:
            Image.fromarray(v.cuadro(t)).save(os.path.join(tmp, f'c_{t:05.2f}.jpg'), quality=90)
            print('cuadro', t)
    elif '--hoja' in sys.argv:
        hoja()
    else:
        render()
        hoja()
