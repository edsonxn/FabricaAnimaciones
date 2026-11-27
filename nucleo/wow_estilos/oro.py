# -*- coding: utf-8 -*-
"""ESTILO «oro» (reliquia de oro y piedra) del kit de Crónicas de Warcraft — motor. API: nucleo/mg_wow_estilos.py.
Adaptado de videos/_kit_wow_estilos/estilo_2/estilo_2.py (22-nov-2026): piedra oscura tallada, molduras de oro con relieve,
gemas de talla brillante engastadas (marcadores), ruta = cadena de oro con runas inventadas que se encienden, destellos y
polvo dorado; letras grabadas Castellar / Constantia. Todo original (no es la interfaz de Blizzard).
Las piezas devuelven fn(dt, dur, marcas) -> BGRA (lienzo local con alfa; el mapa, cuadro entero opaco)."""
import functools
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import comun as C

W, H = 1920, 1080
F_GRAB = r'C:\Windows\Fonts\CASTELAR.TTF'      # mayúsculas grabadas (no tiene «·»: se dibuja un rombo de oro)
F_SERIF = r'C:\Windows\Fonts\constanb.ttf'     # Constantia negrita
F_SERIF_I = r'C:\Windows\Fonts\constanz.ttf'   # Constantia negrita cursiva
GEMA = dict(rojo=(206, 26, 44), ambar=(236, 160, 22), azul=(36, 100, 230), verde=(34, 190, 70),
            violeta=(140, 60, 215), blanco=(220, 232, 250))
PIEDRA = (50, 48, 56)
LUZ = np.array([-0.55, -0.65, 0.52], np.float32)
LUZ /= np.linalg.norm(LUZ)
SS = 4  # supermuestreo de máscaras
FPS = 30


# ----------------------------------------------------------------------------- utilidades (copiadas de la demo)
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
    if lz.shape[2] == 4:                       # lienzo con alfa (kit: canal 3 = alfa en 0-255)
        if modo == 'n':
            a = sp.a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0] * alfa
            reg *= (1 - a)[..., None]
            reg[..., :3] += p * alfa
            reg[..., 3] += a * 255
        else:
            q = p * alfa
            reg[..., :3] += q
            reg[..., 3] = np.minimum(255, reg[..., 3] + q.max(-1))
        return
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
          sombra=14, adornos=False, base=PIEDRA, surco=True):
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
        if surco and gi * 2 + 20 < min(w, h) - 2 * (g1 + b + g2) and borde >= 14:
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
    # sin surco (25-nov-2026): en placas bajas el surco tallado quedaba pegado al texto y se leía «[TEXTO_CON_GUION]»
    pl = marco(w, h, borde=borde, radio=borde * .7, interior='piedra', seed=seed, inlay=False, oscuro=oscuro, sombra=8,
               surco=False)
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
    im = (ruta if isinstance(ruta, Image.Image) else Image.open(ruta)).convert('RGB')
    s = max(iw / im.width, ih / im.height)
    im = im.resize((int(math.ceil(im.width * s)), int(math.ceil(im.height * s))), Image.LANCZOS)
    # recorte desde arriba (regla del usuario 25-nov-2026: en las tarjetas de personaje SIEMPRE se le ve la cara)
    x0, y0 = (im.width - iw) // 2, int((im.height - ih) * .15)
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
def ei(x):
    return x ** 3


# ============================================================================= piezas del kit (generalizadas)
VIG = _vineta(W, H, .32, 1.8)
COLORES = [GEMA['azul'], GEMA['ambar'], GEMA['verde'], GEMA['violeta']]
FONDO_FOTO = (26, 22, 28)


def _lienzo(w, h):
    return np.zeros((int(h), int(w), 4), np.float32)


def _salida(lz):
    return C.bgra_premul(lz / 255.0)


def _cabe(txt, tam, ancho, minimo=18, **kw):
    """texto() que se achica hasta caber en `ancho` (sin contar el margen de sombra)."""
    s = texto(txt, tam, **kw)
    while s.w - 2 * s.pad > ancho and tam > minimo:
        tam -= 2
        s = texto(txt, tam, **kw)
    return s


def _foto_img(fuente_img, w=400, h=400):
    """PIL RGB para enmarcar: los íconos de objeto, enteros y centrados sobre piedra oscura; las fotos, tal cual."""
    im = C.rgba(fuente_img)
    if C.es_icono(fuente_img):
        bg = Image.new('RGBA', (w, h), FONDO_FOTO + (255,))
        e = min(w, h) * .80 / max(im.size)
        ic = im.resize((max(2, int(im.width * e)), max(2, int(im.height * e))), Image.LANCZOS)
        bg.alpha_composite(ic, ((w - ic.width) // 2, (h - ic.height) // 2))
        return bg.convert('RGB')
    bg = Image.new('RGBA', im.size, FONDO_FOTO + (255,))
    bg.alpha_composite(im)
    return bg.convert('RGB')


def _en_fila(a, b, gap=-6):
    """Dos sprites lado a lado (a a la izquierda), centrados en vertical."""
    w = a.w + b.w + gap
    h = max(a.h, b.h)
    out = Spr(np.zeros((h, w, 3), np.float32), np.zeros((h, w), np.float32))
    pegar_spr(out, b, a.w + gap + b.w / 2, h / 2)
    pegar_spr(out, a, a.w / 2, h / 2)
    return out


def _apilar(sprs, gap=-10):
    """Apila sprites (centrados) en uno solo."""
    sprs = [s for s in sprs if s is not None]
    w = max(s.w for s in sprs)
    h = sum(s.h for s in sprs) + gap * (len(sprs) - 1)
    out = Spr(np.zeros((h, w, 3), np.float32), np.zeros((h, w), np.float32))
    y = 0
    for s in sprs:
        pegar_spr(out, s, w / 2, y + s.h / 2)
        y += s.h + gap
    return out


# ----------------------------------------------------------------------------- FICHA (tablilla de piedra con engastes)
class Ficha:
    """Tablilla de piedra con molduras de oro: título grabado que se revela, íconos que caen en sus engastes (marca k)
    con destello, onda y chispas, su etiqueta, y el contador que corre en su cartucho y estalla al total."""

    def __init__(self, titulo, iconos, etiquetas, valores, total=None, colores=None, seed=31):
        n = len(iconos)
        self.n = n
        self.valores = list(valores)
        self.final = total if total is not None else sum(valores)
        self.colores = colores or [GEMA['rojo'], GEMA['ambar'], GEMA['azul'], GEMA['verde']]
        w_base = 190 + 235 * (n - 1) + 245 + 290 + 70
        ts = 50
        self.tit = texto(titulo, ts)
        while self.tit.w - 2 * self.tit.pad > max(w_base, 1720) - 230 and ts > 28:
            ts -= 2
            self.tit = texto(titulo, ts)
        w = int(max(w_base, min(1720, self.tit.w - 2 * self.tit.pad + 230)))
        h = 560
        self.w, self.h = w, h
        off = (w - w_base) / 2
        tab = marco(w, h, borde=40, radio=18, interior='piedra', seed=seed, adornos=True, oscuro=.56, sombra=20)
        P = tab.pad
        pegar_spr(tab, regla_oro(int(w * .72), seed, GEMA['rojo']), P + w / 2, P + 158)
        self.d_eng = 178
        self.xs = [off + 190 + i * 235 for i in range(n)]
        self.y_eng = 300
        for i, x in enumerate(self.xs):
            pegar_spr(tab, engaste(self.d_eng, 11, seed + i), P + x, P + self.y_eng)
        cx0 = self.xs[-1] + 245
        cx1 = cx0 + 290
        self.cx_num = (cx0 + cx1) / 2 + 40
        self.x_igual = cx0 + 10
        self.cw_num = int(cx1 - cx0 - 50)
        car = marco(self.cw_num, 200, borde=14, radio=12, interior='piedra', seed=seed + 9, inlay=False, oscuro=.38, sombra=0)
        pegar_spr(tab, car, P + self.cx_num, P + self.y_eng)
        self.tab = tab
        self.iconos = [icono_redondo_img(r, self.d_eng - 28) for r in iconos]
        self.etqs = [_cabe(e, 46, 220, 26) if e else None for e in etiquetas]
        self.igual = texto('=', 110)
        self.esq = [(20, 20), (w - 20, 20), (20, h - 20), (w - 20, h - 20)]
        self.CW, self.CH = tab.w + 380, tab.h + 340
        self.centro = (self.CW / 2, self.CH / 2)

    def _num(self, v):
        s = texto(str(int(v)), 150)
        return s, min(1.0, (self.cw_num - 36) / max(1, s.w - 2 * s.pad))

    def dibujar(self, lz, t, dur, t_iconos):
        T0 = 0.0
        e_in = pr(t, T0 + .05, T0 + .8)
        if e_in <= 0:
            return
        t_salida = dur - .7
        e_out = pr(t, t_salida, t_salida + .6)
        if e_out >= 1:
            return
        a = eo(e_in) * (1 - e_out)
        dy = 90 * (1 - eo(e_in)) + 70 * eio(e_out)
        sc = lerp(.93, 1, eo(e_in)) * lerp(1, .95, eio(e_out))
        cx, cy = self.centro[0], self.centro[1] + dy
        x0, y0 = cx - self.w / 2 * sc, cy - self.h / 2 * sc

        def L(x, y):
            return x0 + x * sc, y0 + y * sc
        pegar(lz, self.tab, cx, cy, a, s=sc)
        estallido(lz, t, T0 + .75, cx, y0 + self.h * sc, 30, seed=7, vel=(120, 420), vida=.8, alfa=.8)
        for i, (ex, ey) in enumerate(self.esq):
            ti = t_iconos[i] if i < self.n else T0 + 1
            X, Y = L(ex, ey)
            lit = pr(t, ti + .3, ti + .5)
            col = tuple(self.colores[i % len(self.colores)])
            pegar(lz, gema(28, col, seed=40 + i, apagada=True), X, Y, a)
            if lit > 0:
                pegar(lz, halo(30, col, 1.8), X, Y, lit * a * .7, modo='a')
                pegar(lz, gema(28, col, seed=40 + i), X, Y, lit * a)
                flash(lz, t, ti + .35, X, Y, .7)
        r = pr(t, T0 + .6, T0 + 1.3)
        if r > 0:
            sp, c0 = self.tit.cols(0, eio(r))
            tx, ty = L(self.w / 2, 98)
            tw = self.tit.w * sc
            if T0 + 1.7 < t < T0 + 2.7:
                sp, c0 = barrido(self.tit, pr(t, T0 + 1.7, T0 + 2.7) * 1.3 - .15).cols(0, 1)
            pegar(lz, sp, tx - tw / 2 + c0 * sc, ty - self.tit.h * sc / 2, a, s=sc, ancla=(0, 0))
            if r < 1:
                pegar(lz, destello(), tx - tw / 2 + self.tit.w * eio(r) * sc, ty, .8, s=.45, modo='a')
        cuenta = 0.0
        for i, ti in enumerate(t_iconos):
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
            if e2 > 0 and self.etqs[i] is not None:
                ex, ey = L(self.xs[i], 445)
                pegar(lz, self.etqs[i], ex, ey + 18 * (1 - eo(e2)), e2 * a, s=sc)
            cuenta += self.valores[i] * eo(pr(t, ti + .35, ti + .8))
        cuenta *= self.final / max(1e-6, sum(self.valores))
        t3 = min(1.5, max(.9, t_iconos[0] - .2))
        e3 = pr(t, t3, t3 + .4)
        if e3 > 0:
            X, Y = L(self.x_igual, self.y_eng)
            pegar(lz, self.igual, X, Y, e3 * a, s=sc)
            NX, NY = L(self.cx_num, self.y_eng + 4)
            tfin = t_iconos[-1] + .8
            pulso = 1 + .16 * math.exp(-((t - tfin) / .12) ** 2) if t > tfin - .3 else 1
            num, k = self._num(round(cuenta))
            if tfin + .2 < t < tfin + 1.2:
                num = barrido(num, pr(t, tfin + .2, tfin + 1.2) * 1.3 - .15)
            pegar(lz, num, NX, NY, e3 * a, s=sc * pulso * k)
            if t > tfin - .05:
                pegar(lz, halo(110, (255, 190, 80), 2.2), NX, NY, .45 * math.exp(-((t - tfin) / .5) ** 2) * a, modo='a')
            flash(lz, t, tfin, NX, NY, 1.4, .7)
            onda(lz, t, tfin, NX, NY, 230, .7)
            estallido(lz, t, tfin, NX, NY, 34, seed=77, vel=(160, 460), vida=1.2)

    def fn(self):
        def fn(dt, dur, marcas):
            ti = C.tiempos(marcas, self.n, ini=1.6, paso=.9, minimo=.9)[:self.n]
            lz = _lienzo(self.CW, self.CH)
            self.dibujar(lz, dt, dur, ti)
            return _salida(lz)
        return fn


def icono_redondo_img(fuente_img, d):
    im = C.rgba(fuente_img)
    bg = Image.new('RGBA', im.size, FONDO_FOTO + (255,))
    bg.alpha_composite(im)
    im = bg.convert('RGB').resize((d, d), Image.LANCZOS)
    cob = mascara(d, d, forma('circulo', d, d, 0))
    rgb = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:d, 0:d].astype(np.float32)
    r = np.sqrt((xx - d / 2) ** 2 + (yy - d / 2) ** 2) / (d / 2)
    rgb *= (1 - .45 * np.clip(r - .6, 0, 1) / .4)[..., None]
    return Spr.rgba(rgb, cob)


# ----------------------------------------------------------------------------- TARJETA (relicario de arco)
class Tarjeta:
    """Relicario de arco en piedra y oro: rayos y gema clave que se engasta con destello, foto enmarcada que sale de la
    sombra, título grabado (dos líneas si lleva «:»), subtítulo en cursiva y gemas de elemento que se encienden por turnos."""
    MX, MY = 170, 120

    def __init__(self, foto, titulo, sub=None, elementos=None, gema_clave=GEMA['rojo'], seed=61):
        if ':' in titulo:
            a_, b_ = titulo.split(':', 1)
            l1, l2 = a_.strip() + ':', b_.strip()
        else:
            l1, l2 = None, titulo
        w = 600
        self.l1 = _cabe(l1, 32, w - 90, 20, estilo='marfil', contorno=3, sombra=3) if l1 else None
        self.l2 = _cabe(l2, 74, w - 100, 30)
        self.subs = []
        if sub:
            s1 = _cabe(sub, 31, w - 80, 24, ruta=F_SERIF_I, estilo='marfil', contorno=3, sombra=3)
            if s1.w - 2 * s1.pad <= w - 80:
                self.subs = [s1]
            else:
                f = fuente(F_SERIF_I, 27)
                self.subs = [texto(l, 27, F_SERIF_I, 'marfil', 3, 3) for l in C.partir(sub, w - 90, f.getlength)[:2]]
        extra = 36 * max(0, len(self.subs) - 1)
        self.elementos = [GEMA['rojo'], GEMA['azul'], GEMA['verde'], GEMA['ambar']] if elementos is None else list(elementos)
        h = 860 + extra if self.elementos else 800 + extra
        self.w, self.h = w, h
        card = marco(w, h, borde=40, radio=16, tipo='arco', interior='piedra', seed=seed, adornos=True, oscuro=.55, sombra=22)
        P = card.pad
        self.kc = (w / 2, 150)

        def ray(d, k):
            for i in range(9):
                an = math.radians(-180 + i * 22.5)
                L0, L1 = 62, 95 + 45 * abs(math.cos(an))
                xa, ya = self.kc[0] + L0 * math.cos(an), self.kc[1] + L0 * math.sin(an)
                xb, yb = self.kc[0] + L1 * math.cos(an), self.kc[1] + L1 * math.sin(an)
                nx, ny = -math.sin(an), math.cos(an)
                d.polygon([((xa + nx * 5.5) * k, (ya + ny * 5.5) * k), ((xa - nx * 5.5) * k, (ya - ny * 5.5) * k), (xb * k, yb * k)], fill=255)
        rc = mascara(w, h, ray)
        pegar_spr(card, con_sombra(Spr.rgba(oro_de(rc, 2.5, seed), rc), 3, .8), P + w / 2, P + h / 2)
        pegar_spr(card, engaste(112, 9, seed + 3, oscuro=.3), P + self.kc[0], P + self.kc[1])
        pegar_spr(card, foto_enmarcada(_foto_img(foto, 444, 236), 480, 272, borde=18, seed=seed + 4), P + w / 2, P + 236 + 136)
        pegar_spr(card, regla_oro(400, seed, GEMA['rojo']), P + w / 2, P + 668)
        self.y_l1, self.y_l2 = (562, 616) if self.l1 is not None else (0, 590)
        self.y_sub = [712 + 36 * i for i in range(len(self.subs))]
        self.xg = [w / 2 + (i - (len(self.elementos) - 1) / 2) * 96 for i in range(len(self.elementos))]
        self.yg = 772 + extra
        for x in self.xg:
            pegar_spr(card, engaste(58, 6, seed + 11, oscuro=.3), P + x, P + self.yg)
        self.card = card
        self.gclave = gema(84, tuple(gema_clave), seed=9, garras=6)
        self.CW, self.CH = card.w + 2 * self.MX, card.h + 2 * self.MY

    def dibujar(self, lz, t, dur):
        T0 = -.25
        e = pr(t, T0 + .3, T0 + 1.0)
        if e <= 0:
            return
        t_salida = dur - .7
        eo_ = pr(t, t_salida, t_salida + .8)
        if eo_ >= 1:
            return
        dx = 140 * (1 - eo(e)) + 160 * eio(eo_)
        a = pr(e, 0, .35) * (1 - pr(eo_, .4, 1))
        X0, Y0 = self.MX + self.card.pad + dx, self.MY + self.card.pad

        def L(x, y):
            return X0 + x, Y0 + y
        pegar(lz, self.card, X0 - self.card.pad, Y0 - self.card.pad, a, ancla=(0, 0))
        kx, ky = L(*self.kc)
        tk = T0 + 1.15
        if t >= tk:
            x = pr(t, tk, tk + .35)
            pegar(lz, halo(70, (255, 80, 70), 1.8), kx, ky, .35 * x * a, modo='a')
            pegar(lz, self.gclave, kx, ky, x * a, s=lerp(1.6, 1, eo(x)))
            flash(lz, t, tk + .28, kx, ky, 1.2)
            onda(lz, t, tk + .28, kx, ky, 160, .6)
            chispa_periodica(lz, t, kx - 18, ky - 18, fase=.4, periodo=2.6, tam=.4)
        flash(lz, t, t_salida, kx, ky, 1.3, .6)
        e2 = pr(t, T0 + 1.0, T0 + 1.6)
        if e2 < 1:
            fx, fy = L(self.w / 2, 236 + 136)
            reg_h, reg_w = 272 - 36, 480 - 36
            x0, y0 = int(fx - reg_w / 2), int(fy - reg_h / 2)
            x0c, x1c = max(0, x0), min(lz.shape[1], x0 + reg_w)
            if x1c > x0c:
                lz[y0:y0 + reg_h, x0c:x1c, :3] *= (1 - .85 * (1 - eo(e2)))
        textos = [(self.l1, self.y_l1, T0 + 1.5), (self.l2, self.y_l2, T0 + 1.7)] + \
                 [(s, y, T0 + 2.1 + .2 * i) for i, (s, y) in enumerate(zip(self.subs, self.y_sub))]
        for sp, ty, ts in textos:
            if sp is None:
                continue
            x = pr(t, ts, ts + .5)
            if x > 0:
                q = sp
                if sp is self.l2 and T0 + 2.3 < t < T0 + 3.3:
                    q = barrido(sp, pr(t, T0 + 2.3, T0 + 3.3) * 1.3 - .15)
                tx, tyy = L(self.w / 2, ty + 16 * (1 - eo(x)))
                pegar(lz, q, tx, tyy, x * a)
        tg = T0 + 2.4
        ng = len(self.xg)
        for i, xg in enumerate(self.xg):
            gx, gy = L(xg, self.yg)
            col = tuple(self.elementos[i])
            ap = pr(t, tg + i * .12, tg + i * .12 + .3)
            if ap <= 0:
                continue
            pegar(lz, gema(40, col, seed=70 + i, apagada=True, garras=4), gx, gy, ap * a)
            if t > tg + .6:
                k = int((t - tg - .6) / .6) % ng
                fase = ((t - tg - .6) / .6) % 1
                if k == i:
                    v = math.sin(math.pi * fase)
                    pegar(lz, halo(44, col, 1.6), gx, gy, .8 * v * a, modo='a')
                    pegar(lz, gema(40, col, seed=70 + i, garras=4), gx, gy, min(1, v * 1.6) * a)

    def fn(self):
        def fn(dt, dur, marcas):
            lz = _lienzo(self.CW, self.CH)
            self.dibujar(lz, dt, dur)
            return _salida(lz)
        return fn


# ----------------------------------------------------------------------------- RÓTULO (barra de piedra con sello de oro)
class Rotulo:
    """Medallón de oro con su cifra que se estampa (o gema, sin cifra) y barra de piedra que se despliega con el texto."""

    def __init__(self, texto_, sello_txt=None, seed=91):
        self.txt = _cabe(texto_, 52, 1300, 30, ruta=F_SERIF, estilo='oro', contorno=3, sombra=4)
        ancho = int(self.txt.w - 2 * self.txt.pad + 112 + 64)
        self.ancho = ancho
        self.barra = marco(ancho, 112, borde=18, radio=14, interior='piedra', seed=seed, inlay=True, oscuro=.48, sombra=12)
        self.sello = sello(170, str(sello_txt)[:3]) if sello_txt else con_sombra(gema(96, GEMA['rojo'], seed=3), 8, .7)
        self.CW, self.CH = 200 + ancho + 80, 440
        self.pos = (200, 220)

    def dibujar(self, lz, t, dur):
        ts = .05
        x0, y0 = self.pos
        t_salida = dur - .7
        so = pr(t, t_salida, t_salida + .5)
        so2 = pr(t, t_salida + .4, t_salida + .8)
        if so2 >= 1:
            return
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
                pegar(lz, tsp, x0 + 112 - q.pad + c1, y0 - q.h / 2 + 2, 1, ancla=(0, 0))
        x = pr(t, ts, ts + .4)
        s = lerp(2.3, 1, eo(x) ** 1.5) * lerp(1, .2, ei(so2))
        pegar(lz, self.sello, x0, y0, pr(x, 0, .5) * (1 - so2), s=s)
        ti = ts + .4
        flash(lz, t, ti, x0, y0, 1.3, .6)
        onda(lz, t, ti, x0, y0, 190, .6)
        estallido(lz, t, ti, x0, y0, 30, seed=91, vel=(150, 420), vida=1.0)
        flash(lz, t, t_salida + .45, x0, y0, 1.0, .5)
        if t > ti + .8 and so2 == 0:
            chispa_periodica(lz, t, x0 - 40, y0 - 44, fase=.75, periodo=2.9, tam=.35)

    def fn(self):
        def fn(dt, dur, marcas):
            lz = _lienzo(self.CW, self.CH)
            self.dibujar(lz, dt, dur)
            return _salida(lz)
        return fn


# ----------------------------------------------------------------------------- PEGATINA (relicario de oro)
class Pegatina:
    """Foto en relicario de oro y piedra (arco si es retrato, círculo si es ícono de objeto, rectángulo con esquinas de
    oro si es paisaje), gema en la clave, placa con el nombre; entra con rebote y destello, flota y suelta chispas."""

    def __init__(self, fuente_img, titulo=None, tam=380, seed=0):
        im = C.rgba(fuente_img)
        ar = im.width / im.height
        if C.es_icono(fuente_img):
            tipo, w = 'circulo', int(min(tam, 300))
            h = w
        elif ar < .9:
            tipo, w = 'arco', int(tam * .8)
            h = int(w * 1.32)
        else:
            tipo, w = 'rect', int(tam)
            h = int(tam / min(max(ar, 1.25), 1.8))
        borde = 22
        fr = marco(w, h, borde=borde, radio=borde * .6, tipo=tipo, interior='hueco', seed=seed + 3, inlay=True, sombra=12,
                   adornos=(tipo == 'rect'))
        foto = _foto_img(fuente_img, w, h)
        s = max(w / foto.width, h / foto.height)
        foto = foto.resize((max(w, int(math.ceil(foto.width * s))), max(h, int(math.ceil(foto.height * s)))), Image.LANCZOS)
        x0 = (foto.width - w) // 2
        y0 = int((foto.height - h) * .15) if tipo != 'arco' else int((foto.height - h) * .2)   # cara (25-nov-2026)
        ph = np.asarray(foto.crop((x0, y0, x0 + w, y0 + h))).astype(np.float32)
        lum = ph @ np.array([.299, .587, .114], np.float32)
        ph = (lum[..., None] + (ph - lum[..., None]) * .92) * np.array([1.04, 1.0, .92], np.float32)
        cob = mascara(w, h, forma(tipo, w, h, borde * .7, borde * .6))
        base = Spr(np.zeros((fr.h, fr.w, 3), np.float32), np.zeros((fr.h, fr.w), np.float32))
        pegar_spr(base, Spr.rgba(np.clip(ph, 0, 255), cob), fr.w / 2, fr.h / 2)
        pegar_spr(base, fr, fr.w / 2, fr.h / 2)
        base.pad = fr.pad
        self.cuadro = base
        self.gema = gema(30, GEMA['rojo'], seed=seed + 5, garras=4)
        self.gy = fr.pad + (borde * .5 if tipo != 'circulo' else borde * .45)
        self.placa = None
        if titulo:
            ts = 26
            pl = placa(titulo, ts, borde=12, seed=seed + 7)
            while pl.w - 2 * pl.pad > max(w * 1.35, 360) and ts > 16:
                ts -= 2
                pl = placa(titulo, ts, borde=12, seed=seed + 7)
            self.placa = pl
        pw = self.placa.w if self.placa is not None else 0
        ph_ = self.placa.h - 2 * self.placa.pad if self.placa is not None else 0
        self.CW = int(max(base.w, pw) + 160)
        self.CH = int(base.h + ph_ + 150)
        self.fc = (self.CW / 2, 70 + base.h / 2)
        self.py = 70 + base.h - base.pad + ph_ / 2 - 6
        self.polvo = Polvo(14, seed + 9, (40, 40, self.CW - 40, self.CH - 40), tam=(2, 4))

    def dibujar(self, lz, t, dur):
        e = pr(t, 0, .5)
        if e <= 0:
            return
        so = pr(t, dur - .45, dur)
        a = pr(e, 0, .3) * (1 - so)
        s = lerp(.6, 1, eback(e)) * lerp(1, .85, eio(so))
        fx, fy = self.fc[0], self.fc[1] + 5 * math.sin(t * 1.4)
        sp = self.cuadro
        if .6 < t < 1.6:
            sp = barrido(sp, pr(t, .6, 1.6) * 1.3 - .15, fuerza=.5)
        pegar(lz, sp, fx, fy, a, s=s)
        gx, gy = fx, fy + (self.gy - self.cuadro.h / 2) * s
        pegar(lz, self.gema, gx, gy, a, s=s)
        flash(lz, t, .4, gx, gy, .8)
        onda(lz, t, .4, fx, fy, 140, .5)
        if t > 1.0:
            chispa_periodica(lz, t, gx - 8, gy - 8, fase=.3, periodo=2.7, tam=.3)
        if self.placa is not None:
            ep = pr(t, .45, .9)
            if ep > 0:
                pegar(lz, self.placa, self.CW / 2, self.py + 26 * (1 - eo(ep)), ep * (1 - so), s=lerp(.8, 1, eback(ep)))
        self.polvo.dibujar(lz, t, .7 * a)

    def fn(self):
        def fn(dt, dur, marcas):
            lz = _lienzo(self.CW, self.CH)
            self.dibujar(lz, dt, dur)
            return _salida(lz)
        return fn


# ----------------------------------------------------------------------------- MAPA (cuadro entero)
class Mapa:
    """Mapa enmarcado en piedra y oro con gemas en las esquinas, placa con la zona, una gema-marcador por paso que cae
    con rebote en su marca (destello, onda, chispas), cadena de oro con runas que se encienden del paso anterior al nuevo,
    placa con el nombre (y subrótulo) y la foto enmarcada de lo que se nombra. Cámara: encuadra los pasos vistos."""

    def __init__(self, mapa, puntos, titulo=None, sub=None, zmin=1.0, zmax=1.6, objeto=None, rect=(30, 52, 1890, 1050),
                 borde=44, seed=2):
        img = cv2.imread(mapa)[..., ::-1].astype(np.float32)
        lum = img @ np.array([.299, .587, .114], np.float32)
        img = lum[..., None] + (img - lum[..., None]) * .8
        img = (img - 128) * 1.08 + 128
        img *= np.array([1.05, .98, .84], np.float32)
        img = img + .6 * (img - cv2.GaussianBlur(img, (0, 0), 1.3))
        self.mapa = np.clip(img, 0, 255).astype(np.float32)
        self.mh, self.mw = self.mapa.shape[:2]
        self.zmin, self.zmax = zmin, zmax
        self.rect = rect
        x0, y0, x1, y1 = rect
        self.win = (x0 + borde, y0 + borde, x1 - borde, y1 - borde)
        self.ww, self.wh = self.win[2] - self.win[0], self.win[3] - self.win[1]
        self.vig = _vineta(self.ww, self.wh, .5, 2.0)[..., None]
        self.marco = marco(x1 - x0, y1 - y0, borde=borde, radio=20, interior='hueco', seed=seed, adornos=True, sombra=16)
        self.fondo = piedra(H, W, seed + 50, oscura=.55) * VIG[..., None]
        self.esquinas = [(x0 + borde / 2, y0 + borde / 2), (x1 - borde / 2, y0 + borde / 2),
                         (x0 + borde / 2, y1 - borde / 2), (x1 - borde / 2, y1 - borde / 2)]
        self.col_esq = [GEMA['rojo'], GEMA['ambar'], GEMA['azul'], GEMA['verde']]
        fijas = []
        self.titulo = None
        if titulo:
            ts = 46
            self.titulo = placa(titulo, ts, borde=20, gemas=GEMA['ambar'], seed=seed + 3)
            while self.titulo.w > 1300 and ts > 28:
                ts -= 4
                self.titulo = placa(titulo, ts, borde=20, gemas=GEMA['ambar'], seed=seed + 3)
            tw = self.titulo.w - 2 * self.titulo.pad
            fijas.append((W / 2 - tw / 2, self.win[1] - 40, W / 2 + tw / 2, self.win[1] + 50))
        self.sub = texto(sub, 28, F_SERIF_I, 'marfil', 3, 3) if sub else None
        if self.sub is not None:
            fijas.append((W / 2 - self.sub.w / 2, self.win[1] + 46, W / 2 + self.sub.w / 2, self.win[1] + 46 + self.sub.h))
        n = len(puntos)
        self.n = n
        ult = n - 1 if n > 1 else -1
        self.P = [(p[0] / 100 * self.mw, p[1] / 100 * self.mh) for p in puntos]
        self.pts = []
        for i, p in enumerate(puntos):
            d = 54 if i == ult else 40
            col = GEMA['rojo'] if i == ult else COLORES[i % len(COLORES)]
            g = gema(d, tuple(col), seed=i, punta=.8)
            nom = placa(p[2], 28 if i == ult else 24, borde=14, seed=7 + i) if len(p) > 2 and p[2] else None
            sb = texto(p[3], 24, F_SERIF_I, 'marfil', 3, 3) if len(p) > 3 and p[3] else None
            rot = _apilar([nom, sb]) if (nom is not None or sb is not None) else None
            f_ico = p[4] if len(p) > 4 and p[4] else None
            if rot is not None and f_ico is not None:     # ícono fijo junto al nombre (regla del usuario, 25-nov-2026)
                ico = foto_enmarcada(_foto_img(f_ico, 104, 104), 104, 104, borde=9, seed=31 + i)
                rot = _en_fila(ico, rot)
            self.pts.append(dict(d=d, gem=g, rot=rot, hc=g.ancla[1] * g.h - g.centro[1]))
        fotos = [p[4] if len(p) > 4 and p[4] else None for p in puntos]
        if objeto and n and fotos[-1] is None:
            fotos[-1] = "ico:" + objeto
        self.fotos = []
        for i, f in enumerate(fotos):
            if f is None:
                self.fotos.append(None)
                continue
            fw, fh = (400, 244) if i == ult else (290, 178)
            self.fotos.append(foto_enmarcada(_foto_img(f, fw, fh), fw, fh, borde=16 if i == ult else 13, seed=8 + i))
        self.foto_gema = gema(26, GEMA['rojo'], seed=5, garras=4)
        # cadenas: un tramo por paso nuevo
        s_fin = C.camara(self.P, list(range(n)), self.mw, self.mh, self.ww, self.wh, zmin, zmax)[2]
        self.tramos = []
        for k in range(1, n):
            p0, p1 = np.array(self.P[k - 1]), np.array(self.P[k])
            dv = p1 - p0
            Ld = max(np.linalg.norm(dv), 1e-6)
            perp = np.array([-dv[1], dv[0]]) / Ld * (.16 if k % 2 else -.16) * Ld
            pts, sp = bezier(p0, p0 + dv / 3 + perp, p0 + 2 * dv / 3 + perp, p1)
            Lm = float(np.sum(np.sqrt((np.diff(pts, axis=0) ** 2).sum(1))))
            Lpx = Lm * s_fin
            f_ini = (self.pts[k - 1]['d'] * .2) / max(Lpx, 1)
            f_fin = 1 - (self.pts[k]['d'] * .2) / max(Lpx, 1)
            ne = max(4, int((f_fin - f_ini) * Lpx / 17))
            esl = []
            for i in range(ne + 1):
                f = lerp(f_ini, f_fin, i / ne)
                esl.append((f, eslabon('a' if i % 2 == 0 else 'b', round(en_ruta(pts, sp, f)[2]))))
            nr = max(2, int(Lpx / 190))
            runas = [(lerp(.22, .84, i / (nr - 1)),) + runa(seed * 10 + 7 * k + i, 46) for i in range(nr)]
            self.tramos.append((pts, sp, esl, runas))
        lim = (self.win[0] + 10, self.win[1] + 10, self.win[2] - 10, self.win[3] - 10)
        self.lim = lim
        tam_rot = [(q['rot'].w, q['rot'].h) if q['rot'] is not None else None for q in self.pts]
        tam_foto = [(f.w - 2 * f.pad + 20, f.h - 2 * f.pad + 20) if f is not None else None for f in self.fotos]
        self.lado_rot, self.lado_foto = C.colocador(self.P, None, self.mw, self.mh, self.ww, self.wh, zmin, zmax, self.win[0],
                                                    self.win[1], fijas, tam_rot, tam_foto, lambda j: self.pts[j]['d'] * .9,
                                                    lambda j: self.pts[j]['d'] * .55 + 4, lambda j: self.pts[j]['d'] + 40, lim)
        self.polvo = Polvo(60, seed + 1, self.win)

    def _pant(self, p, cx, cy, s):
        return self.win[0] + self.ww / 2 + (p[0] - cx) * s, self.win[1] + self.wh / 2 + (p[1] - cy) * s

    def _marcador(self, lz, t, i, X, Y, dur=.55):
        q = self.pts[i]
        t1 = q['t']
        x = pr(t, t1, t1 + dur)
        off = -170 * (1 - ebounce(x))
        hc = q['hc']
        pegar(lz, halo(26, (0, 0, 0), 1.6), X, Y, .5 * x, modo='n')
        pegar(lz, q['gem'], X, Y + off, pr(x, 0, .15))
        ti = t1 + dur * .364
        flash(lz, t, ti, X, Y - hc, 1.0)
        onda(lz, t, ti, X, Y, 120, .55)
        estallido(lz, t, ti, X, Y - hc * .5, 18, seed=int(t1 * 10) + i, vel=(90, 260), vida=.9)
        if t > ti + .6:
            chispa_periodica(lz, t, X - q['d'] * .2, Y - hc - q['d'] * .2, fase=t1 * .37, tam=.28)

    def cuadro(self, t, dur, tk):
        lz = self.fondo.copy()
        cx, cy, s, vistos = C.camara_en(self.P, tk, t, dur, self.mw, self.mh, self.ww, self.wh, self.zmin, self.zmax)
        pant = lambda p: self._pant(p, cx, cy, s)
        M = np.float32([[s, 0, self.ww / 2 - cx * s], [0, s, self.wh / 2 - cy * s]])
        win = cv2.warpAffine(self.mapa, M, (self.ww, self.wh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        win *= self.vig
        am = eo(pr(t, .3, 1.2))
        x0, y0, x1, y1 = self.win
        lz[y0:y1, x0:x1] = lz[y0:y1, x0:x1] * (1 - am) + win * am
        e = eo(pr(t, 0, .9))
        mx, my = (self.rect[0] + self.rect[2]) / 2, (self.rect[1] + self.rect[3]) / 2
        pegar(lz, self.marco, mx, my, e, s=lerp(1.035, 1, e))
        for i, (ex, ey) in enumerate(self.esquinas):
            te = .6 + i * .16
            if t >= te:
                x = pr(t, te, te + .3)
                pegar(lz, gema(30, tuple(self.col_esq[i]), seed=20 + i), ex, ey, x, s=lerp(1.7, 1, eo(x)))
                flash(lz, t, te + .22, ex, ey, .7)
                chispa_periodica(lz, t, ex - 5, ey - 5, fase=i * .23, periodo=3.3, tam=.25)
        for k, (pts, sp_, esl, runas) in enumerate(self.tramos, 1):
            prog = eio(pr(t, tk[k], tk[k] + 1.4))
            if prog <= 0:
                continue
            for f, spr in esl:
                if prog >= f:
                    X, Y = pant(en_ruta(pts, sp_, f)[:2])
                    pop = cl((prog - f) / .035)
                    pegar(lz, spr, X, Y, pop, s=lerp(1.6, 1, eo(pop)))
            for f, base, lit, glow in runas:
                if prog >= f:
                    X, Y = pant(en_ruta(pts, sp_, f)[:2])
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
                X, Y = pant(en_ruta(pts, sp_, prog)[:2])
                pegar(lz, halo(30), X, Y, .9, modo='a')
                pegar(lz, destello(), X, Y, .75, s=.4, modo='a')
        n = self.n
        for i in vistos:
            self.pts[i]['t'] = tk[i]
            X, Y = pant(self.P[i])
            self._marcador(lz, t, i, X, Y)
        for i in vistos:
            q = self.pts[i]
            if q['rot'] is None:
                continue
            ep = pr(t, tk[i] + .45, tk[i] + .85)
            if ep <= 0:
                continue
            a = ep
            if i != n - 1 and i + 2 < n and t > tk[i + 2]:
                a *= 1 - eo((t - tk[i + 2]) / .4)
            if a <= 0:
                continue
            X, Y = pant(self.P[i])
            r = q['rot']
            rx, ry = C.caja_en(X, Y, r.w, r.h, q['d'] * .55 + 4, self.lado_rot.get(i, 0), self.lim)
            pegar(lz, r, rx + r.w / 2, ry + r.h / 2, a, s=lerp(.7, 1, eback(ep)))
        for i in sorted(vistos, reverse=True):
            ft = self.fotos[i]
            if ft is None:
                continue
            e = pr(t, tk[i] + .6, tk[i] + 1.2)
            if e <= 0:
                continue
            a = pr(e, 0, .4)
            if i + 1 < n and t > tk[i + 1]:
                a *= 1 - eo((t - tk[i + 1]) / .35)
            if a <= 0:
                continue
            X, Y = pant(self.P[i])
            fw, fh = ft.w - 2 * ft.pad + 20, ft.h - 2 * ft.pad + 20
            rx, ry = C.caja_en(X, Y, fw, fh, self.pts[i]['d'] + 40, self.lado_foto.get(i, 0), self.lim)
            fx, fy = rx + fw / 2, ry + fh / 2
            pegar(lz, ft, fx, fy, a, s=lerp(.55, 1, eback(e)))
            if e >= 1:
                gx, gy = fx, fy - (ft.h - 2 * ft.pad) / 2 + 1
                pegar(lz, self.foto_gema, gx, gy, a)
                flash(lz, t, tk[i] + 1.25, gx, gy, .6)
        if self.titulo is not None and t >= .8:
            e = pr(t, .8, 1.5)
            ty = lerp(-70, self.win[1], eback(e))
            sp = self.titulo
            if 1.7 < t < 2.7:
                sp = barrido(sp, lerp(-.15, 1.15, pr(t, 1.7, 2.7)))
            pegar(lz, sp, W / 2, ty, pr(e, 0, .3))
            if e >= 1:
                chispa_periodica(lz, t, W / 2 - (sp.w / 2 - sp.pad) + 46, self.win[1] - 4, fase=.1, periodo=3.1, tam=.3)
        if self.sub is not None:
            e = pr(t, 1.3, 1.8)
            if e > 0:
                pegar(lz, self.sub, W / 2, self.win[1] + 46 + self.sub.h / 2 + 10 * (1 - eo(e)), e)
        self.polvo.dibujar(lz, t, pr(t, .5, 1.5))
        return lz

    def fn(self):
        def fn(dt, dur, marcas):
            tk = C.tiempos(marcas, self.n, ini=1.3, paso=2.2, minimo=1.0)
            return C.bgra_opaco(self.cuadro(dt, dur, tk) / 255.0)
        return fn
