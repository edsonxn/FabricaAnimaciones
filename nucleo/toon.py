# -*- coding: utf-8 -*-
"""Kit del estilo CARTOON 90s (referencia: «Coraje el perro cobarde», Cartoon Network): tinta gruesa de grosor variable que
«hierve» a 12 dibujos/s, rellenos planos de celda con sombra de 2 tonos desfasados de la línea, fondos pintados y luz
dramática. TODO se redibuja en cada cuadro desde cero: los personajes no son recortes que se deslizan, son formas
elásticas (curvas que se estiran, se aplastan y se doblan) cuyo contorno se vuelve a trazar con la pluma.

    h = Toon()                           # una por proceso
    h.nuevo(t, fondo)                    # fondo: float32 HxWx3 ya pintado (o None = negro)
    h.forma(P, color, sombra=..., w=9)   # relleno + sombra de celda + contorno de tinta de la forma cerrada P
    h.trazo(P, w=8)                      # trazo abierto con puntas afinadas
    img = h.final(t)                     # float32 [0,1] con luz, grano y viñeta

Piezas: `Toon` (lienzo, tinta, rellenos, cámara/capas con paralaje, luces), `Pista` (animación por claves con
anticipación/rebote/muelle), `muelle` (oscilación amortiguada tras un golpe), `rebote`, geometría de formas elásticas
(`blob`, `tubo`, `bezier2`, `suave`) y efectos (`lineas_velocidad`, `gota`, `estrella`, `polvo`).
Conceptos y por qué es así: docs/estilo_cartoon90.md.
"""
import math
import os

import cv2
import numpy as np

from motor import (FPS, H, W, catmull, clamp01, e_back, e_in, e_inout, e_out, hash_arr, lerp, mat_r, mat_s, mat_t,
                   prog, remuestrear, ruido1, smooth)

FPS_DIB = 12                      # dibujos por segundo: la tinta se vuelve a trazar a este ritmo (el movimiento va a todos los cuadros)
TINTA = (24, 18, 26)
LUZ_DIR = np.array([-0.62, -0.78])  # de dónde viene la luz (arriba-izquierda): la sombra de celda cae al lado opuesto

try:                              # kernels numba (FAB_SIN_NUMBA=1 los apaga y usa numpy)
    if os.environ.get("FAB_SIN_NUMBA"):
        raise ImportError
    from numba import njit, prange

    @njit(parallel=True, cache=True, fastmath=True)
    def _k_over(canvas, mask, x0, y0, c0, c1, gy0, gy1, alfa, tex, tx, ty, tamp):
        """canvas[roi] = mezcla(canvas, color, mask*alfa); color = degradado vertical c0->c1 entre gy0 y gy1 (en px de pantalla)
        modulado por la textura `tex` (ruido de pintura, ±tamp)."""
        h, w = mask.shape
        th, tw = tex.shape
        k255 = np.float32(1.0 / 255.0)
        dgy = np.float32(1.0) / max(np.float32(1.0), gy1 - gy0)
        for y in prange(h):
            yy = y0 + y
            g = (yy - gy0) * dgy
            if g < 0.0:
                g = 0.0
            elif g > 1.0:
                g = 1.0
            ty_ = (yy + ty) % th
            for x in range(w):
                m = mask[y, x]
                if m == 0:
                    continue
                a = m * k255 * alfa
                tv = np.float32(1.0) + tamp * tex[ty_, (x0 + x + tx) % tw]
                for c in range(3):
                    col = (c0[c] + (c1[c] - c0[c]) * g) * tv
                    canvas[yy, x0 + x, c] += (col - canvas[yy, x0 + x, c]) * a
except Exception:
    _k_over = None


# ================================================================ texturas fijas (pintura)
def _crear_tex():
    r = np.random.default_rng(7)
    fino = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 1.1)
    medio = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 6, W // 6)).astype(np.float32), (0, 0), 2.2), (W, H),
                       interpolation=cv2.INTER_CUBIC)
    t = 0.35 * fino / (fino.std() + 1e-9) + 0.9 * medio / (medio.std() + 1e-9)
    return (t / (t.std() + 1e-9)).astype(np.float32)


TEX = _crear_tex()
_GRANOS = None


def _banco_grano():
    global _GRANOS
    if _GRANOS is None:
        r = np.random.default_rng(99)
        _GRANOS = [cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8) for _ in range(6)]
        _GRANOS = [g / g.std() for g in _GRANOS]
    return _GRANOS


def _viñeta(k=0.55, p=2.2):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.4142
    return (1 - k * np.clip(d, 0, 1) ** p).astype(np.float32)


_VIN = {}


# ================================================================ animación: pistas, muelles, rebotes
def _ease(u, tipo):
    u = 0.0 if u < 0 else 1.0 if u > 1 else u
    if tipo == "l":
        return u
    if tipo == "i":
        return u ** 2.2
    if tipo == "o":
        return 1 - (1 - u) ** 2.2
    if tipo == "io":
        return smooth(u)
    if tipo == "b":                       # se pasa y vuelve (anticipación al revés)
        return e_back(u, 1.9)
    if tipo == "B":
        return e_back(u, 3.4)
    if tipo == "a":                       # anticipación: primero retrocede un poco y luego sale disparado
        return u * u * (3.2 * u - 2.2) if u < 1 else 1.0
    if tipo == "m":                       # muelle: llega, se pasa y se asienta oscilando
        return 1.0 if u >= 1 else 1 - math.exp(-7.0 * u) * math.cos(2 * math.pi * 1.6 * u)
    if tipo == "M":
        return 1.0 if u >= 1 else 1 - math.exp(-5.0 * u) * math.cos(2 * math.pi * 2.4 * u)
    if tipo == "h":                       # escalón: se queda donde estaba hasta la clave y salta (poses «a golpe»)
        return 1.0 if u >= 1 else 0.0
    return u


class Pista:
    """Curva de animación por claves [(t, valor), (t, valor, 'tipo'), ...]. El tipo describe CÓMO se llega a esa clave desde la
    anterior: l lineal · i entra lento · o sale rápido y frena · io suave · b se pasa y vuelve · B se pasa mucho · a anticipa
    (retrocede y dispara) · m / M muelle · h escalón. Valores escalares o tuplas (se interpolan componente a componente).
    Antes de la primera clave y después de la última se mantiene el valor."""

    def __init__(self, claves, defecto=None):
        cl = []
        for k in claves:
            cl.append((float(k[0]), np.asarray(k[1], float) if np.ndim(k[1]) else float(k[1]), k[2] if len(k) > 2 else "io"))
        cl.sort(key=lambda c: c[0])
        self.cl = cl
        self.ts = [c[0] for c in cl]

    def __call__(self, t):
        cl = self.cl
        if t <= cl[0][0]:
            return cl[0][1]
        if t >= cl[-1][0]:
            return cl[-1][1]
        lo, hi = 0, len(cl) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if cl[mid][0] <= t:
                lo = mid
            else:
                hi = mid
        a, b = cl[lo], cl[hi]
        u = (t - a[0]) / max(1e-9, b[0] - a[0])
        return a[1] + (b[1] - a[1]) * _ease(u, b[2])


def muelle(t, golpes, f=3.2, z=0.16):
    """Oscilación amortiguada tras cada golpe (t0, amplitud): sirve para orejas, barriga, gelatina, aplastamientos al caer.
    Es función pura de t (no hay simulación), así que cualquier tramo se puede renderizar suelto."""
    v = 0.0
    for t0, amp in golpes:
        d = t - t0
        if d > 0:
            v += amp * math.exp(-z * 2 * math.pi * f * d) * math.sin(2 * math.pi * f * d)
    return v


def pulso(t, t0, dur, amp=1.0):
    """Campana de 0 a amp y de vuelta a 0 entre t0 y t0+dur."""
    if t <= t0 or t >= t0 + dur:
        return 0.0
    return amp * math.sin(math.pi * (t - t0) / dur) ** 2


def rebote(u):
    """(altura 0..1, aplastamiento) de un salto con rebotes decrecientes; u en 0..1 (cae al inicio, termina quieto)."""
    u = clamp01(u)
    tramos = [(0.0, 0.42, 1.0), (0.42, 0.68, 0.34), (0.68, 0.84, 0.12), (0.84, 0.94, 0.04)]
    for a, b, alt in tramos:
        if a <= u < b:
            k = (u - a) / (b - a)
            hh = alt * (1 - (2 * k - 1) ** 2) if a > 0 else alt * (1 - k * k)
            sq = 0.0
            if k > 0.86:
                sq = 0.30 * alt * (k - 0.86) / 0.14
            if k < 0.10 and a > 0:
                sq = 0.30 * alt * (0.10 - k) / 0.10
            return hh, sq
    return 0.0, 0.0


def lag(f, t, retraso, n=3):
    """Valor de la función f(t) «arrastrado»: promedio de f en t - retraso*(0..1). Da acción superpuesta (la cola, las orejas y las
    cejas llegan después que la cabeza) sin simular nada."""
    if n <= 1:
        return f(t - retraso)
    return sum(f(t - retraso * k / (n - 1)) for k in range(n)) / n


def tiembla(t, amp, f=24.0, sem=0):
    """Temblor de miedo: vibra de un cuadro al siguiente (par/impar) con una variación irregular."""
    k = int(math.floor(t * FPS))
    s = 1.0 if k % 2 == 0 else -1.0
    j = 0.55 + 0.45 * float(ruido1(np.array([k * 0.37]), 100 + sem, 0)[0])
    j2 = 0.55 + 0.45 * float(ruido1(np.array([k * 0.41]), 200 + sem, 0)[0])
    return amp * s * j, amp * 0.55 * (-s if k % 4 < 2 else s) * j2


def vel(f, t, h=1.0 / 60):
    """Derivada numérica de una pista (velocidad)."""
    return (np.asarray(f(t + h)) - np.asarray(f(t - h))) / (2 * h)


# ================================================================ geometría de formas elásticas
def suave(P, n=10, cerrado=True):
    return catmull(np.asarray(P, float), n, cerrado)


def blob(cx, cy, rx, ry, rad=None, rot=0.0, n=14, sub=8):
    """Contorno cerrado orgánico: elipse cuyo radio se modula con `rad` (lista de factores, p. ej. [1, 1.1, .95, ...]) y que se
    suaviza con Catmull-Rom. Es la base de cabezas, cuerpos y monstruos (la deformación son solo estos números)."""
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    r = np.ones(n) if rad is None else np.interp(np.arange(n), np.linspace(0, n, len(rad), endpoint=False), np.asarray(rad, float),
                                                 period=n)
    x, y = rx * r * np.cos(a), ry * r * np.sin(a)
    c, s = math.cos(rot), math.sin(rot)
    P = np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)
    return catmull(P, sub, True)


def elipse_(cx, cy, rx, ry, rot=0.0, n=40):
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    x, y = rx * np.cos(a), ry * np.sin(a)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)


def bezier2(p0, p1, p2, n=24):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = (np.asarray(p, float) for p in (p0, p1, p2))
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2


def bezier3(p0, p1, p2, p3, n=30):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = (np.asarray(p, float) for p in (p0, p1, p2, p3))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def eje_curvo(a, b, curva=0.0, n=24):
    """Eje de un brazo/pierna de goma: de a a b con una panza lateral `curva` (px, positiva = a la derecha del sentido a->b)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    L = float(np.hypot(*d)) + 1e-9
    nrm = np.array([d[1], -d[0]]) / L
    return bezier2(a, (a + b) / 2 + nrm * curva, b, n)


def tubo(eje, w0, w1=None, wmed=None, extremo=True, n_cap=7):
    """Silueta cerrada de un tubo de grosor variable alrededor de `eje` (polilínea): w0 en el inicio, w1 al final y wmed
    (opcional) en medio. Terminan en punta redondeada. Brazos, piernas, cola, tentáculos."""
    eje = np.asarray(eje, float)
    n = len(eje)
    u = np.linspace(0, 1, n)
    w1 = w0 if w1 is None else w1
    w = w0 + (w1 - w0) * u
    if wmed is not None:
        w = w + (wmed - 0.5 * (w0 + w1)) * 4 * u * (1 - u)
    d = np.gradient(eje, axis=0)
    L = np.hypot(d[:, 0], d[:, 1]) + 1e-9
    nr = np.stack([d[:, 1] / L, -d[:, 0] / L], 1)
    izq = eje + nr * (w / 2)[:, None]
    der = eje - nr * (w / 2)[:, None]
    capf = None
    if extremo:
        ang = np.linspace(0, math.pi, n_cap)[1:-1]
        t1 = np.array([d[-1, 0], d[-1, 1]]) / L[-1]
        n1 = nr[-1]
        capf = np.array([eje[-1] + n1 * (w[-1] / 2) * math.cos(a_) + t1 * (w[-1] / 2) * math.sin(a_) for a_ in ang])
        t0 = -np.array([d[0, 0], d[0, 1]]) / L[0]
        n0 = nr[0]
        capi = np.array([eje[0] - n0 * (w[0] / 2) * math.cos(a_) + t0 * (w[0] / 2) * math.sin(a_) for a_ in ang])
        return np.vstack([izq, capf, der[::-1], capi])
    return np.vstack([izq, der[::-1]])


def espinas(P, nivel, amp=26.0, per=5, sem=0):
    """Pelo erizado: empuja hacia afuera puntos alternos del contorno (cerrado, ya remuestreado). nivel 0..1."""
    if nivel <= 0.001:
        return P
    c = P.mean(0)
    n = len(P)
    k = np.arange(n)
    ph = (k % per) / per
    tri = 1 - np.abs(2 * ph - 1)
    r = np.stack([ruido1(k * 0.9, 300 + sem, 0) * 0.35 + 1.0], 1)[:, 0]
    d = P - c
    dn = d / (np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9)
    return P + dn * (nivel * amp * tri * r)[:, None]


def ondular(P, amp, f, fase, cerrado=True):
    """Ondula el contorno hacia la normal (gelatina, banderas, fantasmas)."""
    n = len(P)
    d = np.roll(P, -1, 0) - np.roll(P, 1, 0)
    L = np.hypot(d[:, 0], d[:, 1]) + 1e-9
    nr = np.stack([d[:, 1] / L, -d[:, 0] / L], 1)
    s = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return P + nr * (amp * np.sin(f * s + fase))[:, None]


def _area(P):
    return 0.5 * float(np.dot(P[:, 0], np.roll(P[:, 1], -1)) - np.dot(P[:, 1], np.roll(P[:, 0], -1)))


def _normales(P, cerrado):
    if cerrado:
        d = np.roll(P, -1, 0) - np.roll(P, 1, 0)
    else:
        d = np.gradient(P, axis=0)
    L = np.hypot(d[:, 0], d[:, 1]) + 1e-9
    nr = np.stack([d[:, 1] / L, -d[:, 0] / L], 1)
    if cerrado and _area(P) < 0:
        nr = -nr
    return nr


def _remu(P, paso, cerrado):
    return remuestrear(np.asarray(P, float), paso, cerrado)


# ================================================================ el lienzo de dibujo
class Toon:
    """Lienzo float32 HxWx3 con tinta, relleno de celda, sombra, cámara con capas y luces. Una por proceso."""

    def __init__(self):
        self.img = np.zeros((H, W, 3), np.float32)
        self.M = np.eye(3)
        self.zoom = 1.0
        self.dib = 0
        self.tinte = np.array([1.0, 1.0, 1.0], np.float32)
        self.luces = []
        self.ambiente = np.array([1.0, 1.0, 1.0], np.float32)
        self.t = 0.0
        self._cam = (1.0, W / 2, H / 2, 0.0)
        self.silueta = None                   # (color, alfa): todo se dibuja como mancha plana (sombra proyectada); sin tinta ni sombra de celda

    # ---------------------------------------------------------- cuadro / cámara / capas
    def nuevo(self, t, fondo=None, tinte=(1, 1, 1)):
        self.t = t
        self.dib = int(math.floor(t * FPS_DIB + 1e-6))
        if fondo is None:
            self.img[:] = 0
        else:
            self.img[:] = fondo
        self.tinte = np.array(tinte, np.float32)
        self.luces = []
        self.ambiente = np.array([1.0, 1.0, 1.0], np.float32)
        self.camara(1.0, W / 2, H / 2, 0.0)

    def camara(self, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0):
        """Mira al punto (cx, cy) del mundo con zoom y giro (Dutch angle). Todo lo que se dibuje después pasa por esta cámara."""
        self._cam = (zoom, cx, cy, rot)
        self.M = mat_t(W / 2, H / 2) @ mat_r(rot) @ mat_s(zoom) @ mat_t(-cx, -cy)
        self.zoom = zoom

    def matriz_capa(self, prof):
        """Matriz de la cámara para una capa a profundidad prof (0 = infinito, no se mueve; 1 = el plano de los personajes;
        >1 = primer plano, se mueve más)."""
        zoom, cx, cy, rot = self._cam
        z = 1 + (zoom - 1) * prof
        cxd = W / 2 + (cx - W / 2) * prof
        cyd = H / 2 + (cy - H / 2) * prof
        return mat_t(W / 2, H / 2) @ mat_r(rot * min(1.0, prof)) @ mat_s(z) @ mat_t(-cxd, -cyd)

    def capa(self, prof):
        """Con `with h.capa(0.6):` lo dibujado va con el paralaje de esa profundidad."""
        h = self

        class _C:
            def __enter__(s):
                s.M0, s.z0 = h.M, h.zoom
                h.M = h.matriz_capa(prof)
                h.zoom = 1 + (h._cam[0] - 1) * prof

            def __exit__(s, *a):
                h.M, h.zoom = s.M0, s.z0
        return _C()

    def tf(self, P):
        P = np.asarray(P, float)
        M = self.M
        return P @ M[:2, :2].T + M[:2, 2]

    def pegar_capa(self, rgba, ox, oy, prof=1.0):
        """Pega una imagen float32 HxWx4 (rgb premultiplicado + alfa) cuya esquina sup-izq está en (ox, oy) del mundo."""
        if rgba.shape[2] == 3:                      # capa opaca (fondo): se pega sin transparencia
            return self.pegar_fondo(rgba, ox, oy, prof)
        M = self.matriz_capa(prof) @ mat_t(ox, oy)
        out = cv2.warpAffine(rgba, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        a = out[..., 3:4]
        self.img *= (1 - a)
        self.img += out[..., :3]

    def pegar_fondo(self, rgb, ox, oy, prof=0.0):
        """Fondo opaco HxWx3 (o más grande que la pantalla) con paralaje."""
        M = self.matriz_capa(prof) @ mat_t(ox, oy)
        self.img[:] = cv2.warpAffine(rgb, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    # ---------------------------------------------------------- máscaras y rellenos
    @staticmethod
    def _roi(P, m=3):
        x0 = int(max(0, math.floor(P[:, 0].min()) - m))
        y0 = int(max(0, math.floor(P[:, 1].min()) - m))
        x1 = int(min(W, math.ceil(P[:, 0].max()) + m + 1))
        y1 = int(min(H, math.ceil(P[:, 1].max()) + m + 1))
        return x0, y0, x1, y1

    def mascara(self, polis, m=3, roi=None):
        """Máscara uint8 antialias de uno o varios polígonos (pantalla). Devuelve (mask, x0, y0) o None si queda fuera."""
        polis = [np.asarray(p, float) for p in polis]
        allp = np.vstack(polis)
        x0, y0, x1, y1 = roi or self._roi(allp, m)
        if x1 - x0 < 1 or y1 - y0 < 1:
            return None
        mk = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(mk, [np.rint((p - (x0, y0)) * 16).astype(np.int32).reshape(-1, 1, 2) for p in polis], 255, cv2.LINE_AA, 4)
        return mk, x0, y0

    def _pintar(self, mk, x0, y0, c0, c1=None, grad=None, alfa=1.0, tex=0.03, tdesp=(0, 0)):
        if self.silueta is not None:
            c0, c1, grad, tex = self.silueta[0], None, None, 0.0
            alfa = alfa * self.silueta[1]
        c0 = np.asarray(c0, np.float32) / 255.0 * (self.tinte if self.silueta is None else 1.0)
        c1 = c0 if c1 is None else np.asarray(c1, np.float32) / 255.0 * self.tinte
        gy0, gy1 = grad if grad else (0.0, 1.0)
        if _k_over is not None:
            _k_over(self.img, mk, x0, y0, c0.astype(np.float32), c1.astype(np.float32), np.float32(gy0), np.float32(gy1),
                    np.float32(alfa), TEX, int(tdesp[0]), int(tdesp[1]), np.float32(tex))
        else:
            h, w = mk.shape
            a = mk.astype(np.float32) * (alfa / 255.0)
            yy = np.arange(y0, y0 + h, dtype=np.float32)[:, None]
            g = np.clip((yy - gy0) / max(1.0, gy1 - gy0), 0, 1)[..., None]
            col = c0 + (c1 - c0) * g
            tv = 1 + tex * TEX[y0:y0 + h, x0:x0 + w][..., None]
            roi = self.img[y0:y0 + h, x0:x0 + w]
            roi += (col * tv - roi) * a[..., None]

    def relleno(self, P, color, grad=None, alfa=1.0, tex=0.012, off=(0, 0), clip=None):
        """Rellena el polígono P (pantalla) con un color plano o degradado vertical grad=(color2, y0, y1). `clip`: máscara
        (mask, x0, y0) con la que se intersecta (ojos, dientes)."""
        P = np.asarray(P, float) + off
        r = self.mascara([P])
        if r is None:
            return None
        mk, x0, y0 = r
        if clip is not None:
            mk = self._intersecar(mk, x0, y0, clip)
            if mk is None:
                return None
        if grad is None:
            self._pintar(mk, x0, y0, color, alfa=alfa, tex=tex)
        else:
            self._pintar(mk, x0, y0, color, c1=grad[0], grad=(grad[1], grad[2]), alfa=alfa, tex=tex)
        return mk, x0, y0

    @staticmethod
    def _intersecar(mk, x0, y0, clip):
        cm, cx0, cy0 = clip
        ax0, ay0 = max(x0, cx0), max(y0, cy0)
        ax1, ay1 = min(x0 + mk.shape[1], cx0 + cm.shape[1]), min(y0 + mk.shape[0], cy0 + cm.shape[0])
        if ax1 <= ax0 or ay1 <= ay0:
            return None
        out = np.zeros_like(mk)
        out[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0] = cv2.bitwise_and(mk[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0],
                                                                    cm[ay0 - cy0:ay1 - cy0, ax0 - cx0:ax1 - cx0])
        return out

    def sombra_celda(self, mk, x0, y0, color, d=(16, 20), alfa=0.55, clip=None):
        """Sombra de celda de 2 tonos: la parte del relleno que no cubre su copia desplazada hacia la luz (media luna del lado opuesto)."""
        if self.silueta is not None:
            return None
        dx, dy = int(round(d[0])), int(round(d[1]))
        m = 3 + max(abs(dx), abs(dy))
        h, w = mk.shape
        big = np.zeros((h + 2 * m, w + 2 * m), np.uint8)
        big[m:m + h, m:m + w] = mk
        M = np.float32([[1, 0, -dx], [0, 1, -dy]])
        sh = cv2.warpAffine(big, M, (w + 2 * m, h + 2 * m), flags=cv2.INTER_LINEAR)
        banda = cv2.subtract(big, sh)[m:m + h, m:m + w]
        banda = cv2.GaussianBlur(banda, (0, 0), 1.0)
        banda = cv2.bitwise_and(banda, mk)
        self._pintar(banda, x0, y0, color, alfa=alfa, tex=0.02)
        return banda

    # ---------------------------------------------------------- tinta
    def _jit(self, P, amp, sem, cerrado=True):
        """Tiembla el contorno entre un dibujo y otro (la línea se vuelve a trazar a mano): senoidales periódicas con fase por dibujo."""
        n = len(P)
        if amp <= 0 or n < 6:
            return P
        s = np.linspace(0, 2 * math.pi, n, endpoint=False) if cerrado else np.linspace(0, 2 * math.pi, n)
        rng = np.random.default_rng((self.dib * 7919 + sem * 104729) & 0x7FFFFFFF)
        dx = np.zeros(n)
        dy = np.zeros(n)
        for k, a_ in zip((2, 3, 5, 7), (1.0, 0.8, 0.5, 0.35)):
            ph = rng.uniform(0, 2 * math.pi, 2)
            dx += a_ * np.sin(k * s + ph[0])
            dy += a_ * np.sin(k * s + ph[1])
        return P + amp * 0.62 * np.stack([dx, dy], 1)

    def anillo(self, P, w, sem=0, color=TINTA, alfa=1.0, peso_luz=0.5, ruido=0.26, jit=2.4, sketch=0.0):
        """Contorno cerrado de tinta de grosor variable (más grueso en el lado de la sombra, con ondas de presión)."""
        if self.silueta is not None:
            return
        P = np.asarray(P, float)
        Q = _remu(P, 4.0, True)[:-1]
        if len(Q) < 6:
            return
        Q = self._jit(Q, jit * self.zoom, sem)
        nr = _normales(Q, True)
        n = len(Q)
        s = np.linspace(0, 1, n, endpoint=False)
        ph = (self.dib * 0.173 + sem * 0.37)
        f = 1 + peso_luz * (nr @ (-LUZ_DIR)) * 0.8 + ruido * np.sin(2 * math.pi * (3 * s) + ph * 6 + sem) \
            + ruido * 0.6 * np.sin(2 * math.pi * (7 * s) + ph * 11)
        ww = np.clip(w * self.zoom * f, 1.0, None)
        outer = Q + nr * (ww / 2)[:, None]
        inner = Q - nr * (ww / 2)[:, None]
        r = self.mascara([outer, inner], m=int(ww.max()) + 3)
        if r is None:
            return
        mk, x0, y0 = r
        self._pintar(mk, x0, y0, color, alfa=alfa, tex=0.0)
        if sketch > 0 and n > 30:
            # segundo trazo flojo y fino que se sale un poco de la línea (entintado a mano alzada): 2 arcos por dibujo
            rng = np.random.default_rng((self.dib * 4099 + sem * 7727) & 0x7FFFFFFF)
            for _ in range(2):
                i0 = int(rng.uniform(0, n))
                ln = int(n * rng.uniform(0.14, 0.26))
                idx = (np.arange(ln) + i0) % n
                off = rng.uniform(2.0, 4.5) * self.zoom * (1 if rng.uniform() < 0.8 else -1)
                A = Q[idx] + nr[idx] * off
                self.trazo(A, max(2.2, w * 0.30), sem + 500, color=color, alfa=alfa * 0.9 * sketch, taper=(0.35, 0.45), jit=1.2, tf=False)

    def trazo(self, P, w=8.0, sem=0, color=TINTA, alfa=1.0, taper=(0.5, 0.5), ruido=0.18, jit=1.2, tf=True):
        """Trazo abierto de pluma con las puntas afinadas. P en coordenadas del mundo (pasa por la cámara) salvo tf=False."""
        if self.silueta is not None:
            return
        P = self.tf(P) if tf else np.asarray(P, float)
        if len(P) < 2:
            return
        Q = _remu(P, 3.5, False)
        if len(Q) < 3:
            return
        L = float(np.hypot(*np.diff(Q, axis=0).T).sum())
        if L < 2:
            return
        Q = self._jit(Q, jit * self.zoom, sem, False)
        nr = _normales(Q, False)
        n = len(Q)
        s = np.linspace(0, 1, n)
        f = 1 + ruido * np.sin(2 * math.pi * 2 * s + self.dib * 1.3 + sem)
        a, b = taper
        ex = np.minimum(np.clip(s * L / max(2.0, a * L), 0, 1), np.clip((1 - s) * L / max(2.0, b * L), 0, 1))
        ww = np.clip(w * self.zoom * f * (0.18 + 0.82 * np.sqrt(ex)), 0.8, None)
        izq = Q + nr * (ww / 2)[:, None]
        der = Q - nr * (ww / 2)[:, None]
        poly = np.vstack([izq, der[::-1]])
        r = self.mascara([poly], m=int(ww.max()) + 3)
        if r is None:
            return
        mk, x0, y0 = r
        self._pintar(mk, x0, y0, color, alfa=alfa, tex=0.0)

    def forma(self, P, color, sombra=None, w=9.0, sem=0, grad=None, linea=True, d_sombra=(16, 20), alfa=1.0, jit=2.4, off=None,
              clip=None, color_linea=TINTA, brillo=None, tex=0.012, w_luz=0.5, sketch=0.0):
        """Forma de celda completa: relleno (desfasado un poco de la línea, como pintada a mano), sombra de 2 tonos y contorno de
        tinta. P cerrada en coordenadas del mundo (pasa por la cámara). Devuelve la máscara del relleno."""
        Pw = self.tf(P)
        Pj = self._jit(_remu(Pw, 4.0, True)[:-1] if len(Pw) > 8 else Pw, jit * self.zoom, sem)
        o = off if off is not None else (1.8 * math.sin(self.dib * 2.1 + sem), 1.8 * math.cos(self.dib * 1.7 + sem * 2))
        r = self.relleno(Pj, color, grad=grad, alfa=alfa, tex=tex, off=o, clip=clip)
        if r is not None and sombra is not None:
            mk, x0, y0 = r
            self.sombra_celda(mk, x0, y0, sombra, d=(d_sombra[0] * self.zoom, d_sombra[1] * self.zoom), clip=clip)
        if brillo is not None and r is not None:
            mk, x0, y0 = r
            self.sombra_celda(mk, x0, y0, brillo, d=(-d_sombra[0] * 0.5 * self.zoom, -d_sombra[1] * 0.5 * self.zoom), alfa=0.5)
        if linea and w > 0:
            self.anillo(Pj, w, sem, color=color_linea, peso_luz=w_luz, jit=0.0, sketch=sketch)
        return r

    def disco(self, x, y, r, color, sem=0, w=0.0):
        P = elipse_(x, y, r, r, n=18)
        return self.forma(P, color, None, w=w, sem=sem, jit=0.4, tex=0.0)

    # ---------------------------------------------------------- luz y acabado
    def luz_radial(self, x, y, r, color, k=1.0, mundo=True):
        if mundo:
            x, y = self.tf(np.array([[x, y]]))[0]
            r *= self.zoom
        self.luces.append(("r", x, y, r, np.asarray(color, np.float32), k))

    def luz_cono(self, x, y, ang, abre, largo, color, k=1.0, suave=0.28, mundo=True):
        """Cono de luz (linterna): origen, dirección (rad), semiapertura (rad), largo (px)."""
        if mundo:
            x, y = self.tf(np.array([[x, y]]))[0]
            largo *= self.zoom
            ang += self._cam[3]
        self.luces.append(("c", x, y, ang, abre, largo, np.asarray(color, np.float32), k, suave))

    def mapa_luz(self):
        sh, sw = H // 3, W // 3
        yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
        xx *= 3
        yy *= 3
        L = np.empty((sh, sw, 3), np.float32)
        L[:] = self.ambiente
        for lz in self.luces:
            if lz[0] == "r":
                _, x, y, r, col, k = lz
                d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / max(1.0, r)
                a = np.clip(1 - d, 0, 1) ** 2 * k
                L += a[..., None] * col
            else:
                _, x, y, ang, abre, largo, col, k, suave = lz
                dx, dy = xx - x, yy - y
                d = np.sqrt(dx * dx + dy * dy) + 1e-3
                cosang = (dx * math.cos(ang) + dy * math.sin(ang)) / d
                th = np.arccos(np.clip(cosang, -1, 1))
                lat = np.clip((abre - th) / (abre * suave + 1e-4), 0, 1)
                lat = lat * lat * (3 - 2 * lat)
                lon = np.clip(1 - d / largo, 0, 1) ** 0.8 * np.clip(d / 170.0, 0, 1)      # sin deslumbrar junto a la lente
                a = lat * lon * k
                L += a[..., None] * col
        return cv2.resize(L, (W, H), interpolation=cv2.INTER_LINEAR)

    def final(self, t, grano=0.045, vin=0.5, luz=True, bloom=0.0):
        img = self.img
        if luz and (self.luces or not np.allclose(self.ambiente, 1.0)):
            img *= self.mapa_luz()
        if bloom > 0:
            br = np.clip(img - 0.62, 0, None)
            g = cv2.GaussianBlur(cv2.resize(br, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 7)
            img += cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR) * bloom
        if grano > 0:
            g = _banco_grano()[int(t * 24) % 6]
            img *= (1 + grano * g)[..., None]
        if vin > 0:
            v = _VIN.get(vin)
            if v is None:
                v = _VIN[vin] = _viñeta(vin)
            img *= v[..., None]
        np.clip(img, 0, 1, out=img)
        return img


# ================================================================ efectos de cartoon
def lineas_velocidad(h, cx, cy, dx, dy, n=9, largo=240, w=7, sem=0, sep=44):
    """Rayas de velocidad detrás de algo que se mueve en (dx, dy)."""
    L = math.hypot(dx, dy) + 1e-9
    ux, uy = -dx / L, -dy / L
    nx, ny = -uy, ux
    rng = np.random.default_rng(sem + h.dib * 31)
    for i in range(n):
        o = (i - (n - 1) / 2) * sep + rng.uniform(-12, 12)
        l0 = rng.uniform(0.5, 1.0) * largo
        off = rng.uniform(40, 120)
        a = np.array([cx + nx * o + ux * off, cy + ny * o + uy * off])
        b = a + np.array([ux, uy]) * l0
        h.trazo(np.array([a, b]), w, sem + i, taper=(0.1, 0.9), jit=0.8)


def gota(cx, cy, r, ang=0.0):
    """Gota de sudor (lágrima): contorno cerrado, punta hacia arriba (ang=0)."""
    u = np.linspace(0, 2 * math.pi, 28, endpoint=False)
    x = r * np.sin(u) * (1 - 0.0)
    y = -r * np.cos(u)
    y = np.where(y < 0, y * 1.9, y)
    x = np.where(y < 0, x * (1 + y / (r * 1.9)) * 1.0, x)
    c, s = math.cos(ang), math.sin(ang)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)


def estrella(cx, cy, r1, r2, puntas=5, rot=-math.pi / 2):
    a = rot + np.arange(puntas * 2) * math.pi / puntas
    r = np.where(np.arange(puntas * 2) % 2 == 0, r1, r2)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def pol_rad(cx, cy, radios, a0=0.0):
    """Polígono radial con los radios dados (explosiones, gritos, nubes de polvo con picos)."""
    n = len(radios)
    a = a0 + np.arange(n) * 2 * math.pi / n
    r = np.asarray(radios, float)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)
