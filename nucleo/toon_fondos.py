# -*- coding: utf-8 -*-
"""Fondos PINTADOS del estilo cartoon90 (nucleo/toon.py): lienzo float32 con polígonos de bordes rugosos, pinceladas direccionales,
degradados, brillos aditivos, sombras y luz derramada, perspectiva con `warpPerspective` (pasillos, suelos). Se pintan UNA vez por
proceso (cache) en un lienzo más grande que la pantalla para poder mover la cámara; lo animado va encima con tinta (Toon).

    p = Pintor(1350, 2400)
    p.degradado([(0, (10, 12, 40)), (1, (90, 120, 130))])
    p.poli(P, (30, 26, 60), rug=3, blur=1.5)
    p.pinceladas(P, (60, 50, 110), ang=0, n=400, largo=120)
    p.glow(x, y, r, (255, 230, 150), 0.8)
    img = p.rgba() / p.rgb()
Los colores son 0-255. Detalle y receta: docs/estilo_cartoon90.md.
"""
import math

import cv2
import numpy as np

_NZ = {}


def ruido_suave(h, w, escala, seed=1):
    """Ruido de valor 2D suave con media 0 y desviación ~1 (cache por tamaño)."""
    k = (h, w, escala, seed)
    if k not in _NZ:
        r = np.random.default_rng(seed)
        sh, sw = max(2, int(h / escala) + 2), max(2, int(w / escala) + 2)
        a = r.normal(0, 1, (sh, sw)).astype(np.float32)
        a = cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)
        a = (a - a.mean()) / (a.std() + 1e-9)
        if len(_NZ) > 24:
            _NZ.clear()
        _NZ[k] = a.astype(np.float32)
    return _NZ[k]


def fbm(h, w, escala=120, octavas=4, seed=1, gain=0.5):
    out = np.zeros((h, w), np.float32)
    amp = 1.0
    tot = 0.0
    for o in range(octavas):
        out += amp * ruido_suave(h, w, max(2, escala / (2 ** o)), seed + o * 13)
        tot += amp
        amp *= gain
    return out / tot


def textura_pincel(h, w, ang=0.0, largo=40, seed=3):
    """Ruido alargado en la dirección `ang` (grados): el grano de una pincelada seca."""
    r = np.random.default_rng(seed)
    a = r.normal(0, 1, (h, w)).astype(np.float32)
    k = np.zeros((largo, largo), np.float32)
    c = largo // 2
    d = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
    for s in np.linspace(-c, c, largo * 2):
        x, y = int(round(c + d[0] * s)), int(round(c + d[1] * s))
        if 0 <= x < largo and 0 <= y < largo:
            k[y, x] = 1
    k /= k.sum()
    a = cv2.filter2D(a, -1, k)
    return (a - a.mean()) / (a.std() + 1e-9)


def col(c):
    return np.asarray(c, np.float32) / 255.0


class Pintor:
    def __init__(self, w, h, base=(0, 0, 0), seed=1):
        self.w, self.h = w, h
        self.c = np.empty((h, w, 3), np.float32)
        self.c[:] = col(base)
        self.A = np.zeros((h, w), np.float32)      # alfa acumulado (c es color premultiplicado)
        self.seed = seed
        self.o = np.zeros(2)                    # origen del lienzo en coordenadas del mundo: todo se pinta en coordenadas del mundo
        self.rng = np.random.default_rng(seed)
        self.tp = textura_pincel(h, w, 0, 36, seed + 5)         # grano horizontal
        self.tv = textura_pincel(h, w, 90, 36, seed + 6)        # grano vertical

    # ---------------------------------------------------------- bajo nivel
    def _roi(self, P, m=6):
        x0 = int(max(0, math.floor(P[:, 0].min()) - m))
        y0 = int(max(0, math.floor(P[:, 1].min()) - m))
        x1 = int(min(self.w, math.ceil(P[:, 0].max()) + m + 1))
        y1 = int(min(self.h, math.ceil(P[:, 1].max()) + m + 1))
        return x0, y0, x1, y1

    def mascara(self, P, blur=1.2, rug=0.0, esc_rug=14.0, m=None):
        P = np.asarray(P, float) + self.o
        mm = m if m is not None else int(blur * 4 + rug * 14 + 6)
        x0, y0, x1, y1 = self._roi(P, mm)
        if x1 <= x0 or y1 <= y0:
            return None
        mk = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(mk, [np.rint((P - (x0, y0)) * 16).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_AA, 4)
        a = mk.astype(np.float32) / 255.0
        if rug > 0:
            # borde rugoso: se perturba solo en la franja de transición (nunca aparecen islas lejos del borde)
            ab = cv2.GaussianBlur(a, (0, 0), 1.5 + rug * 3.0)
            n = ruido_suave(y1 - y0, x1 - x0, esc_rug, self.seed + 31 + (x0 * 7 + y0 * 3) % 97)
            edge = 4 * ab * (1 - ab)
            a = np.clip((ab - 0.5 + n * 0.20 * rug * edge) * 3.0 + 0.5, 0, 1)
            a = cv2.GaussianBlur(a, (0, 0), max(0.7, blur * 0.6))
        elif blur > 0.1:
            a = cv2.GaussianBlur(a, (0, 0), blur)
        return a, x0, y0

    def _mezclar(self, a, x0, y0, color, alfa=1.0, tex=0.05, grad=None, luz=None):
        h, w = a.shape
        roi = self.c[y0:y0 + h, x0:x0 + w]
        if grad is not None:                                   # (color2, y0, y1) degradado vertical en px del lienzo
            c2 = col(grad[0])
            gy = np.clip((np.arange(y0, y0 + h, dtype=np.float32) - (grad[1] + self.o[1])) / max(1.0, grad[2] - grad[1]), 0, 1)[:, None, None]
            cc = col(color) + (c2 - col(color)) * gy
        else:
            cc = col(color)
        if tex > 0:
            tt = (0.55 * self.tp[y0:y0 + h, x0:x0 + w] + 0.45 * self.tv[y0:y0 + h, x0:x0 + w])[..., None]
            cc = cc * (1 + tex * tt)
        roi += (cc - roi) * (a * alfa)[..., None]
        Ar = self.A[y0:y0 + h, x0:x0 + w]
        Ar += (1 - Ar) * (a * alfa)

    # ---------------------------------------------------------- pintura
    def degradado(self, stops, y0=0, y1=None, tex=0.03):
        y1 = self.h if y1 is None else y1
        ys = np.arange(self.h, dtype=np.float32)
        u = np.clip((ys - y0) / max(1.0, y1 - y0), 0, 1)
        ps = [s[0] for s in stops]
        cs = np.array([col(s[1]) for s in stops], np.float32)
        out = np.stack([np.interp(u, ps, cs[:, k]) for k in range(3)], 1)
        self.c[:] = out[:, None, :]
        self.A[:] = 1.0
        if tex > 0:
            self.c *= 1 + tex * (0.6 * fbm(self.h, self.w, 90, 3, self.seed + 2) + 0.4 * self.tp)[..., None]

    def poli(self, P, color, alfa=1.0, blur=1.0, rug=1.0, tex=0.06, grad=None):
        r = self.mascara(P, blur, rug)
        if r is None:
            return None
        a, x0, y0 = r
        self._mezclar(a, x0, y0, color, alfa, tex, grad)
        return a, x0, y0

    def rect(self, x, y, w, h, color, **kw):
        return self.poli(np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], float), color, **kw)

    def elipse(self, cx, cy, rx, ry, color, rot=0.0, n=60, **kw):
        a = np.linspace(0, 2 * math.pi, n, endpoint=False)
        x, y = rx * np.cos(a), ry * np.sin(a)
        c, s = math.cos(rot), math.sin(rot)
        return self.poli(np.stack([cx + x * c - y * s, cy + x * s + y * c], 1), color, **kw)

    def pinceladas(self, P, color, ang=0.0, n=300, largo=100, ancho=5.0, alfa=0.22, var=0.12, rug=0.0):
        """Pinceladas translúcidas (líneas gruesas) dentro del polígono P: da la mano de pintura a una superficie plana."""
        P = np.asarray(P, float)
        r = self.mascara(P, 0.8, 0.0)
        if r is None:
            return
        a, x0, y0 = r
        h, w = a.shape
        capa = np.zeros((h, w), np.uint8)
        rng = np.random.default_rng(self.seed + int(P.sum()) % 10007)
        d = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
        for _ in range(n):
            cx, cy = rng.uniform(0, w), rng.uniform(0, h)
            ln = largo * rng.uniform(0.5, 1.3)
            aa = math.radians(ang + rng.normal(0, 6))
            dd = np.array([math.cos(aa), math.sin(aa)])
            p0 = (cx - dd[0] * ln / 2, cy - dd[1] * ln / 2)
            p1 = (cx + dd[0] * ln / 2, cy + dd[1] * ln / 2)
            cv2.line(capa, (int(p0[0] * 4), int(p0[1] * 4)), (int(p1[0] * 4), int(p1[1] * 4)), int(rng.uniform(120, 255)),
                     max(1, int(ancho * rng.uniform(0.5, 1.4))), cv2.LINE_AA, 2)
        capa = cv2.GaussianBlur(capa.astype(np.float32) / 255.0, (0, 0), 1.2) * a
        cc = col(color) * (1 + var * (rng.uniform(-1, 1)))
        roi = self.c[y0:y0 + h, x0:x0 + w]
        roi += (cc - roi) * (capa * alfa)[..., None]
        Ar = self.A[y0:y0 + h, x0:x0 + w]
        Ar += (1 - Ar) * (capa * alfa)

    def glow(self, x, y, r, color, k=1.0, ry=None, pot=2.0):
        """Resplandor aditivo (luna, ventana, farol)."""
        ry = r if ry is None else ry
        x, y = x + self.o[0], y + self.o[1]
        x0, y0 = int(max(0, x - r * 1.05)), int(max(0, y - ry * 1.05))
        x1, y1 = int(min(self.w, x + r * 1.05)), int(min(self.h, y + ry * 1.05))
        if x1 <= x0 or y1 <= y0:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt(((xx - x) / r) ** 2 + ((yy - y) / ry) ** 2)
        a = np.clip(1 - d, 0, 1) ** pot * k
        self.c[y0:y1, x0:x1] += a[..., None] * col(color)
        Ar = self.A[y0:y1, x0:x1]
        Ar += (1 - Ar) * np.clip((a[..., None] * col(color)).max(-1), 0, 1)

    def luz_poli(self, P, color, k=0.5, blur=18.0):
        """Luz derramada (aditiva) con la forma de P y borde difuso: la ventana sobre el suelo."""
        r = self.mascara(P, blur, 0.0, m=int(blur * 3 + 6))
        if r is None:
            return
        a, x0, y0 = r
        h, w = a.shape
        self.c[y0:y0 + h, x0:x0 + w] += (a * k)[..., None] * col(color)
        Ar = self.A[y0:y0 + h, x0:x0 + w]
        Ar += (1 - Ar) * np.clip(((a * k)[..., None] * col(color)).max(-1), 0, 1)

    def sombra_poli(self, P, k=0.5, blur=14.0, color=(10, 8, 30)):
        r = self.mascara(P, blur, 0.0, m=int(blur * 3 + 6))
        if r is None:
            return
        a, x0, y0 = r
        h, w = a.shape
        roi = self.c[y0:y0 + h, x0:x0 + w]
        roi += (col(color) - roi) * (a * k)[..., None]
        Ar = self.A[y0:y0 + h, x0:x0 + w]
        Ar += (1 - Ar) * (a * k)

    def manchas(self, x0, y0, x1, y1, color, n=30, rmin=20, rmax=120, alfa=0.12):
        """Manchas de humedad / desgaste (círculos muy suaves)."""
        for _ in range(n):
            cx, cy = self.rng.uniform(x0, x1), self.rng.uniform(y0, y1)
            self.glow_mult(cx, cy, self.rng.uniform(rmin, rmax), color, alfa * self.rng.uniform(0.5, 1.0))

    def glow_mult(self, x, y, r, color, k):
        x, y = x + self.o[0], y + self.o[1]
        x0, y0 = int(max(0, x - r)), int(max(0, y - r))
        x1, y1 = int(min(self.w, x + r)), int(min(self.h, y + r))
        if x1 <= x0 or y1 <= y0:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r
        a = np.clip(1 - d, 0, 1) ** 1.5 * k
        roi = self.c[y0:y1, x0:x1]
        roi += (col(color) - roi) * a[..., None]
        Ar = self.A[y0:y1, x0:x1]
        Ar += (1 - Ar) * a

    def textura(self, k=0.04, escala=70):
        self.c *= 1 + k * fbm(self.h, self.w, escala, 4, self.seed + 9)[..., None]

    def viñeta(self, k=0.5, p=2.0, cx=None, cy=None):
        cx = self.w / 2 if cx is None else cx + self.o[0]
        cy = self.h / 2 if cy is None else cy + self.o[1]
        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        d = np.sqrt(((xx - cx) / (self.w * 0.62)) ** 2 + ((yy - cy) / (self.h * 0.62)) ** 2)
        self.c *= (1 - k * np.clip(d, 0, 1.3) ** p)[..., None]

    def rgb(self):
        return np.clip(self.c, 0, 1).astype(np.float32)

    def rgba_auto(self):
        """Capa con el alfa acumulado de lo pintado (rgb premultiplicado)."""
        a = np.clip(self.A, 0, 1)
        c = np.minimum(np.clip(self.c, 0, 1), a[..., None])
        return np.dstack([c, a]).astype(np.float32)

    def rgba(self, alfa):
        """Capa con transparencia (alfa HxW 0..1): rgb premultiplicado."""
        a = np.clip(alfa, 0, 1).astype(np.float32)
        c = np.clip(self.c, 0, 1) * a[..., None]
        return np.dstack([c, a]).astype(np.float32)


# ---------------------------------------------------------------- perspectiva
def plano_persp(textura, dst, tam_out):
    """Pega una textura plana HxWx3 sobre el cuadrilátero dst (4 puntos: sup-izq, sup-der, inf-der, inf-izq) de un lienzo de tam_out
    (w, h). Devuelve (imagen, máscara). Pasillos, suelos de baldosas, paredes inclinadas."""
    h, w = textura.shape[:2]
    src = np.float32([(0, 0), (w, 0), (w, h), (0, h)])
    M = cv2.getPerspectiveTransform(src, np.float32(dst))
    img = cv2.warpPerspective(textura, M, tam_out, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    mk = cv2.warpPerspective(np.ones((h, w), np.float32), M, tam_out, flags=cv2.INTER_LINEAR)
    return img, mk


def desenfoque(rgba, sigma):
    return cv2.GaussianBlur(rgba, (0, 0), sigma)
