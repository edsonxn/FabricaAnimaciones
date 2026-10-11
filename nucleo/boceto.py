# -*- coding: utf-8 -*-
"""Kit del estilo BOCETO: papel crema, tinta que "hierve", crayón desfasado y letra manuscrita.

Cada elemento es una lista de operaciones (`Dib`): trazos de tinta (`T`) y rellenos de crayón (`R`). Cada cuadro se
redibuja desde cero: la pluma recorre el contorno (progreso `u` 0..1 = "dibujar"; `u` decreciente = "borrar" en orden
inverso) y el crayón rellena en zigzag, ligeramente fuera de línea, como un niño coloreando. La tinta tiembla en
3 fases a 12 cuadros/s (`fase(t)`), como animación a mano.

    hoja = Hoja()                       # una por proceso
    hoja.limpiar()
    NUBE.dibujar(hoja, x, y, s, u=prog(t, t0, t0 + 1.5), fase=fase(t))
    hoja.texto_palabra(...)             # letra manuscrita que se escribe
    img = hoja.componer()               # float32 HxWx3 en [0,1]

Coordenadas locales (x derecha, y abajo) transformadas por (x, y, s, rot, flip). Helpers de geometría: circ, elip,
curva, ondas, union_circulos, mano_poli. Paleta de crayón abajo.
"""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from motor import H, W, catmull, clamp01, e_inout, lerp, prog, ruido1

# ------------------------------------------------------------------ paleta
TINTA = (30, 27, 33)
PAPEL = (247, 244, 235)
AZUL = (84, 150, 216)
AZUL_CL = (176, 212, 240)
AZUL_OSC = (52, 96, 170)
ROJO = (226, 84, 62)
NARANJA = (242, 152, 60)
AMARILLO = (250, 206, 72)
VERDE = (104, 172, 96)
VERDE_OSC = (58, 124, 86)
ROSA = (238, 144, 154)
MARRON = (168, 114, 80)
GRIS = (156, 158, 170)
GRIS_CL = (206, 208, 216)
HIELO = (216, 236, 250)
PIEL = (242, 192, 152)
BLANCO = (255, 253, 248)

FASES = 3
FPS_BOIL = 12


def fase(t):
    """Fase del temblor de la tinta (0..2), a 12 cuadros por segundo."""
    return int(math.floor(t * FPS_BOIL + 1e-6)) % FASES


# ------------------------------------------------------------------ texturas fijas (papel y crayón)
def _norm(a):
    a = a - a.mean()
    return a / (a.std() + 1e-9)


def _crear_texturas():
    r = np.random.default_rng(11)
    fino = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.9)
    lento = cv2.resize(cv2.GaussianBlur(r.normal(0, 1, (H // 10, W // 10)).astype(np.float32), (0, 0), 5),
                       (W, H), interpolation=cv2.INTER_CUBIC)
    papel = np.empty((H, W, 3), np.float32)
    papel[:] = PAPEL
    papel *= (1 + 0.010 * _norm(fino) + 0.011 * _norm(lento))[..., None]
    n = r.random((H, W), dtype=np.float32)
    k = np.eye(17, dtype=np.float32) / 17
    diag = _norm(cv2.filter2D(n, -1, k))
    pt = _norm(cv2.GaussianBlur(n, (0, 0), 0.7))
    t = 0.7 * diag + 0.3 * pt
    lo, hi = np.percentile(t, [6, 94])
    tex = 0.62 + 0.38 * np.clip((t - lo) / (hi - lo), 0, 1)
    return np.clip(papel / 255, 0, 1).astype(np.float32), tex.astype(np.float32)


PAPEL_F, TEX = _crear_texturas()


def _crear_parches():
    """Campo suave con valores ~uniformes en [0,1]: umbralizarlo da manchas irregulares que crecen (disolver crayón)."""
    r = np.random.default_rng(23)
    g = cv2.GaussianBlur(r.normal(0, 1, (H // 14, W // 14)).astype(np.float32), (0, 0), 1.6)
    rank = np.argsort(np.argsort(g.ravel())).reshape(g.shape).astype(np.float32) / g.size
    return cv2.resize(rank, (W, H), interpolation=cv2.INTER_CUBIC)


PARCHES = _crear_parches()
_INK = np.array(TINTA, np.float32) / 255

try:                                    # composición fusionada (numba); FAB_SIN_NUMBA=1 fuerza la versión numpy
    if os.environ.get("FAB_SIN_NUMBA"):
        raise ImportError
    from numba import njit, prange

    @njit(parallel=True, cache=True, fastmath=True)
    def _comp_numba(papel, cal, tex, cray, tinta, ink, hay, out):
        h, w = tinta.shape
        c255 = np.float32(1.0 / 255.0)
        for y in prange(h):
            for x in range(w):
                k = tinta[y, x] * c255
                a = np.float32(0.0)
                if hay:
                    a = cal[y, x] * c255 * tex[y, x]
                if k == 0.0 and a == 0.0:
                    out[y, x, 0] = papel[y, x, 0]
                    out[y, x, 1] = papel[y, x, 1]
                    out[y, x, 2] = papel[y, x, 2]
                    continue
                for c in range(3):
                    v = papel[y, x, c]
                    if a != 0.0:
                        v *= 1.0 - a * (1.0 - cray[y, x, c] * c255)
                    v *= 1.0 - k * (1.0 - ink[c])
                    out[y, x, c] = v
except Exception:
    _comp_numba = None


# ------------------------------------------------------------------ geometría
def circ(cx, cy, r, a0=0.0, vuelta=1.05, n=48, ry=None):
    a = a0 + np.linspace(0, 2 * math.pi * vuelta, n)
    return np.stack([cx + r * np.cos(a), cy + (ry or r) * np.sin(a)], 1)


def elip(cx, cy, rx, ry, rot=0.0, vuelta=1.05, n=48):
    a = np.linspace(0, 2 * math.pi * vuelta, n)
    x, y = rx * np.cos(a), ry * np.sin(a)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)


def arco_(cx, cy, r, a0, a1, n=24, ry=None):
    a = np.linspace(math.radians(a0), math.radians(a1), n)
    return np.stack([cx + r * np.cos(a), cy + (ry or r) * np.sin(a)], 1)


def curva(P, n=10, cerrado=False):
    return catmull(np.asarray(P, float), n, cerrado)


def linea(*P):
    return np.asarray(P, float)


def ondas(x0, x1, y, amp, lam, ph=0.0, n=None):
    n = n or max(8, int(abs(x1 - x0) / 10))
    x = np.linspace(x0, x1, n)
    return np.stack([x, y + amp * np.sin((x - x0) / lam * 2 * math.pi + ph)], 1)


def mano_poli(P, amp=3.0, seed=0, paso=26.0):
    """Sub-divide los lados de un polígono y los tuerce un poco, como trazado a mano alzada."""
    P = np.asarray(P, float)
    out = []
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        n = max(1, int(np.hypot(*(b - a)) / paso))
        for k in range(n):
            q = a + (b - a) * k / n
            out.append(q + amp * np.array([ruido1(np.array([len(out) * 0.7]), seed, 0)[0],
                                           ruido1(np.array([len(out) * 0.7]), seed, 1)[0]]))
    out.append(P[-1])
    return np.array(out)


def union_circulos(circulos, base_y, centro=(0.0, 0.0), n=90):
    """Contorno de la unión de círculos (cx, cy, r) recortado por la línea y = base_y (nubes)."""
    pts = []
    for i, c in enumerate(circulos):
        cx, cy, r = c[:3]
        a = np.linspace(0, 2 * math.pi, n, endpoint=False)
        x, y = cx + r * np.cos(a), cy + r * np.sin(a)
        ok = y <= (c[3] if len(c) > 3 else base_y)         # 4.º valor opcional: y máxima del arco de ese círculo
        for j, (qx, qy, qr) in enumerate(c_ for c_ in [cc[:3] for cc in circulos]):
            if j != i:
                ok &= np.hypot(x - qx, y - qy) > qr + 0.5
        pts += list(zip(x[ok], y[ok]))
    pts = np.array(pts)
    ang = np.arctan2(pts[:, 1] - centro[1], pts[:, 0] - centro[0])
    return pts[np.argsort(ang)], ang


GIRO_SOL = 0.5                   # rad/s de giro de los soles (el video lo ajusta a vueltas enteras)
OMEGA = 2 * math.pi / 1.85       # frecuencia base de la "vida" (el video la ajusta a un número entero de ciclos: bucle exacto)


def vivir(P, cx, cy, tv, ph, amp, resp):
    """Deformación continua de la forma: ondulación suave del contorno + respiración (ninguna forma queda quieta).
    Todas las frecuencias son múltiplos enteros de OMEGA, así el movimiento es periódico."""
    w = OMEGA
    x, y = P[:, 0], P[:, 1]
    dx = amp * (np.sin(y / 57.0 + 2 * w * tv + ph) + 0.5 * np.sin(x / 83.0 - 3 * w * tv + 2 * ph))
    dy = amp * (np.sin(x / 61.0 + 3 * w * tv + 1.7 * ph) + 0.5 * np.sin(y / 79.0 - 2 * w * tv + ph))
    r = 1 + resp * math.sin(w * tv + ph)
    return np.stack([cx + (x - cx) * r + dx, cy + (y - cy) * r + dy], 1)


def transformar(P, x, y, s=1.0, rot=0.0, flip=False, sq=0.0):
    """Escala, gira y traslada. sq > 0 aplasta (más ancho y bajo), sq < 0 estira (rebote y caída)."""
    Q = np.asarray(P, float) * (s * (1 + sq) * (-1 if flip else 1), s * (1 - sq))
    if rot:
        c, sn = math.cos(rot), math.sin(rot)
        Q = np.stack([Q[:, 0] * c - Q[:, 1] * sn, Q[:, 0] * sn + Q[:, 1] * c], 1)
    return Q + (x, y)


def _remuestrear(P, paso):
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    L = float(d[-1])
    if L < 1e-6:
        return P[:1], 0.0
    n = max(2, int(L / paso) + 1)
    s = np.linspace(0, L, n)
    return np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], 1), L


# ------------------------------------------------------------------ la hoja (un cuadro)
class Hoja:
    def __init__(self):
        self.tinta = np.zeros((H, W), np.uint8)
        self.cray = np.zeros((H, W, 3), np.uint8)
        self.cal = np.zeros((H, W), np.uint8)
        self.hay_cray = False
        self.fondo = None                    # imagen float32 (H,W,3) pintada a guache que sustituye al papel liso (mapas)
        self.peg = np.zeros((H, W), np.uint8)  # siluetas de las "pegatinas" (recortes de papel bajo los dibujos)
        self.hay_peg = False

    def limpiar(self):
        self.tinta.fill(0)
        self.cal.fill(0)
        self.hay_cray = False
        self.fondo = None
        if self.hay_peg:
            self.peg.fill(0)
            self.hay_peg = False

    # ---- pegatinas: recorte de papel con borde blanco y sombra, para que los dibujos se lean sobre el mapa pintado
    def silueta(self, P, cerrado_relleno=True, ancho=0):
        """Añade una silueta (polígono relleno o trazo de `ancho` px) a la máscara de pegatinas."""
        P = np.asarray(P, float)
        I = np.rint(P * 4).astype(np.int32).reshape(-1, 1, 2)
        if cerrado_relleno:
            cv2.fillPoly(self.peg, [I], 255, cv2.LINE_8, 2)
        else:
            cv2.polylines(self.peg, [I], False, 255, max(1, int(ancho)), cv2.LINE_8, 2)
        self.hay_peg = True

    def peg_mascara(self, m, x, y, cols=None):
        """Añade a las pegatinas la silueta de una máscara uint8 (letras recortadas en papel, sellos)."""
        h, w = m.shape
        if cols is not None:
            w = max(0, min(w, int(cols)))
        if w <= 0:
            return
        x, y = int(round(x)), int(round(y))
        xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
        if xb <= xa or yb <= ya:
            return
        np.maximum(self.peg[ya:yb, xa:xb], m[ya - y:yb - y, xa - x:xb - x], out=self.peg[ya:yb, xa:xb])
        self.hay_peg = True

    def sello(self, m, x, y, color, alfa=235, desgaste=0.0, semilla=0):
        """Estampa una máscara como tinta de color en la capa de crayón (sellos rojos), con el desgaste típico."""
        h, w = m.shape
        x, y = int(round(x)), int(round(y))
        xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
        if xb <= xa or yb <= ya:
            return
        src = m[ya - y:yb - y, xa - x:xb - x]
        if desgaste > 0:
            src = (src.astype(np.float32) * (PARCHES[ya:yb, xa:xb] > desgaste * 0.5)).astype(np.uint8)
        sel = src > 0
        self.cray[ya:yb, xa:xb][sel] = color
        np.maximum(self.cal[ya:yb, xa:xb], (src.astype(np.uint16) * alfa // 255).astype(np.uint8), out=self.cal[ya:yb, xa:xb])
        self.hay_cray = True

    def _aplicar_pegatinas(self, base, borde=11):
        ys, xs = np.nonzero(self.peg[::4, ::4])
        if len(ys) == 0:
            return base
        m = 40
        y0, y1 = max(0, ys.min() * 4 - m), min(H, ys.max() * 4 + m)
        x0, x1 = max(0, xs.min() * 4 - m), min(W, xs.max() * 4 + m)
        roi = self.peg[y0:y1, x0:x1]
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * borde + 1, 2 * borde + 1))
        a = cv2.GaussianBlur(cv2.dilate(roi, k), (0, 0), 1.3).astype(np.float32) * (1 / 255.0)
        sh = cv2.warpAffine(a, np.float32([[1, 0, 7], [0, 1, 10]]), (x1 - x0, y1 - y0))
        sh = cv2.GaussianBlur(sh, (0, 0), 6.0) * 0.30
        sh = np.clip(sh - a * 0.30, 0, 1)
        if base is PAPEL_F:
            base = base.copy()
        b = base[y0:y1, x0:x1]
        b *= (1 - sh)[..., None]
        b[:] = b * (1 - a)[..., None] + PAPEL_F[y0:y1, x0:x1] * 1.012 * a[..., None]
        return base

    # ---- tinta
    def trazo(self, P, ancho=5.0, seed=0, fase_=0, frac=1.0, amp=1.7, v=255, cerrado=False):
        """Trazo de pluma sobre la polilínea P (pantalla). `frac` = fracción ya dibujada (la punta avanza)."""
        if frac <= 0.002 or len(P) < 2:
            return
        Q, L = _remuestrear(np.asarray(P, float), 6.0)
        if L < 1.5 or len(Q) < 2:
            return
        s = np.linspace(0, L, len(Q))
        if frac < 1.0:
            Lc = L * frac
            k = int(np.searchsorted(s, Lc))
            if k >= len(Q):
                k = len(Q) - 1
            if k < 1:
                return
            f = (Lc - s[k - 1]) / max(1e-6, s[k] - s[k - 1])
            punta = Q[k - 1] + (Q[k] - Q[k - 1]) * f
            Q = np.vstack([Q[:k], punta])
            s = np.append(s[:k], Lc)
            L = Lc
        # temblor: lento (mano) + por fase (hervor)
        x = s / 42.0 + fase_ * 9.17
        Q = Q + amp * np.stack([ruido1(x, seed, 0), ruido1(x, seed, 1)], 1)
        Q = Q + 1.1 * np.stack([ruido1(s / 85.0, seed + 91, 0), ruido1(s / 85.0, seed + 91, 1)], 1)
        w = ancho * (0.86 + 0.22 * ruido1(s / 55.0, seed + 5, 2))
        w = w * np.minimum(1.0, np.minimum(0.55 + s / 16.0, 0.55 + (L - s) / 16.0))
        wi = np.maximum(1, np.rint(w).astype(int))
        I = np.rint(Q * 16).astype(np.int32)
        i = 0
        n = len(Q)
        while i < n - 1:
            j = i + 1
            while j < n - 1 and wi[j] == wi[i]:
                j += 1
            cv2.polylines(self.tinta, [I[i:j + 1].reshape(-1, 1, 2)], False, int(v), int(wi[i]), cv2.LINE_AA, 4)
            i = j

    def punto(self, x, y, r, seed=0, fase_=0, v=255):
        """Punto de tinta (ojos)."""
        cv2.circle(self.tinta, (int(round((x + 0.7 * ruido1(np.array([fase_ * 3.1]), seed, 0)[0]) * 16)),
                                int(round((y + 0.7 * ruido1(np.array([fase_ * 3.1]), seed, 1)[0]) * 16))),
                   int(round(r * 16)), int(v), -1, cv2.LINE_AA, 4)

    # ---- crayón
    def relleno(self, poly, color, seed=0, fase_=0, frac=1.0, sp=11.0, ang=-55.0, off=(6.0, -5.0), alfa=228,
                disolver=0.0, inv=False):
        if frac <= 0.002:
            return
        poly = np.asarray(poly, float)
        x0 = int(max(0, math.floor(poly[:, 0].min() + min(off[0], 0) - sp)))
        y0 = int(max(0, math.floor(poly[:, 1].min() + min(off[1], 0) - sp)))
        x1 = int(min(W, math.ceil(poly[:, 0].max() + max(off[0], 0) + sp)))
        y1 = int(min(H, math.ceil(poly[:, 1].max() + max(off[1], 0) + sp)))
        if x1 - x0 < 3 or y1 - y0 < 3:
            return
        w, h = x1 - x0, y1 - y0
        j = 1.4 * np.array([ruido1(np.array([fase_ * 2.3]), seed, 0)[0], ruido1(np.array([fase_ * 2.3]), seed, 1)[0]])
        Pm = poly + np.array(off) + j - (x0, y0)
        mask = np.zeros((h, w), np.uint8)
        cv2.fillPoly(mask, [np.rint(Pm * 16).astype(np.int32).reshape(-1, 1, 2)], 255, cv2.LINE_AA, 4)
        # zigzag de coloreado
        a = math.radians(ang)
        d = np.array([math.cos(a), math.sin(a)])
        nrm = np.array([-d[1], d[0]])
        c = np.array([w / 2, h / 2])
        R = math.hypot(w, h) / 2 + sp
        K = int(2 * R / sp) + 1
        k = np.arange(K)
        o = (k * sp - R)[:, None] * nrm
        jit = 0.5 * sp * np.stack([ruido1(k * 0.9, seed + 3, 0), ruido1(k * 0.9, seed + 4, 0)], 1)[:, :1] * d
        pa = c + o - d * (R + jit)
        pb = c + o + d * (R - jit)
        par = (k % 2 == 0)[:, None]
        p1 = np.where(par, pa, pb)
        p2 = np.where(par, pb, pa)
        Z = np.stack([p1, p2], 1).reshape(-1, 2)
        if inv:
            Z = Z[::-1]                      # el coloreado empieza por el otro lado (p. ej. de abajo hacia arriba)
        if frac < 1.0:
            seg = np.hypot(*np.diff(Z, axis=0).T)
            cum = np.concatenate([[0.0], np.cumsum(seg)])
            Lc = cum[-1] * frac
            m = int(np.searchsorted(cum, Lc))
            m = max(2, min(m, len(Z)))
            Zc = Z[:m].copy()
            if m < len(Z):
                f = (Lc - cum[m - 1]) / max(1e-6, cum[m] - cum[m - 1])
                Zc = np.vstack([Z[:m], Z[m - 1] + (Z[m] - Z[m - 1]) * f])
            Z = Zc
        tmp = np.zeros((h, w), np.uint8)
        cv2.polylines(tmp, [np.rint(Z * 4).astype(np.int32).reshape(-1, 1, 2)], False, 255,
                      max(2, int(sp * 0.86)), cv2.LINE_AA, 2)
        m_ = cv2.bitwise_and(tmp, mask)
        if disolver > 0:                     # el crayón se deshace en manchas
            m_ = m_ * (PARCHES[y0:y1, x0:x1] > disolver)
        sel = m_ > 0
        self.cray[y0:y1, x0:x1][sel] = color
        np.maximum(self.cal[y0:y1, x0:x1], (m_.astype(np.uint16) * alfa // 255).astype(np.uint8),
                   out=self.cal[y0:y1, x0:x1])
        self.hay_cray = True

    # ---- letra manuscrita (sprites de PIL)
    def pegar_mascara(self, m, x, y, cols=None, v=255):
        """Pega una máscara uint8 (h,w) en tinta con esquina (x,y); `cols` = columnas visibles (escritura)."""
        h, w = m.shape
        if cols is not None:
            w = max(0, min(w, int(cols)))
        if w <= 0:
            return
        x, y = int(round(x)), int(round(y))
        xa, ya = max(0, x), max(0, y)
        xb, yb = min(W, x + w), min(H, y + h)
        if xb <= xa or yb <= ya:
            return
        src = m[ya - y:yb - y, xa - x:xb - x]
        if v < 255:
            src = (src.astype(np.uint16) * v // 255).astype(np.uint8)
        np.maximum(self.tinta[ya:yb, xa:xb], src, out=self.tinta[ya:yb, xa:xb])

    def componer(self):
        """Papel + crayón + tinta -> imagen float32 [0,1]. Un solo paso fusionado con numba (multihilo) si está
        disponible; si no, la versión numpy de siempre."""
        base = PAPEL_F if self.fondo is None else self.fondo
        if self.hay_peg:
            base = self._aplicar_pegatinas(base)
        if _comp_numba is None:
            return self._componer_numpy(base)
        out = np.empty_like(PAPEL_F)
        _comp_numba(np.ascontiguousarray(base, dtype=np.float32), self.cal, TEX, self.cray, self.tinta, _INK, self.hay_cray, out)
        return out

    def _componer_numpy(self, base=None):
        img = (PAPEL_F if base is None else base).copy()
        if self.hay_cray:
            a = self.cal.astype(np.float32) * (1 / 255.0) * TEX
            cr = self.cray.astype(np.float32) * (1 / 255.0)
            img *= 1 - a[..., None] * (1 - cr)
        k = self.tinta.astype(np.float32) * (1 / 255.0)
        img *= 1 - k[..., None] * (1 - _INK)
        return img


# ------------------------------------------------------------------ dibujos (listas de operaciones)
def T(P, w=5.0, peso=None, v=255):
    """Trazo de tinta."""
    return ("t", np.asarray(P, float), w, peso, v)


def R(P, color, peso=None, sp=11.0, ang=-55.0, off=(6.0, -5.0)):
    """Relleno de crayón del polígono P."""
    return ("r", np.asarray(P, float), color, peso, sp, ang, off)


class Dib:
    def __init__(self, ops):
        self.ops = ops
        costes = []
        for op in ops:
            if op[0] == "t":
                L = float(np.hypot(*np.diff(op[1], axis=0).T).sum())
                c = op[3] if op[3] is not None else 0.05 + L / 1100.0
            else:
                P = op[1]
                area = 0.5 * abs(np.dot(P[:, 0], np.roll(P[:, 1], 1)) - np.dot(P[:, 1], np.roll(P[:, 0], 1)))
                c = op[3] if op[3] is not None else 0.10 + 0.0007 * math.sqrt(area + 1)
            costes.append(c)
        self.c0 = np.concatenate([[0.0], np.cumsum(costes)])
        self.costes = costes
        self.total = float(self.c0[-1])

    def dibujar(self, hoja, x, y, s=1.0, rot=0.0, flip=False, u=1.0, fase_=0, semilla=0, ancho=1.0, sq=0.0, lapiz=0.0,
                tv=None, vida=1.0, peg=False):
        """u = progreso de dibujo (0..1); lapiz 0..1 = intensidad del boceto de lápiz gris previo (los contornos
        aparecen enteros, flojos y temblorosos, antes de que la tinta y el crayón los cierren).
        peg=True: el dibujo lleva pegatina (recorte de papel con sombra) cuando se pinta sobre un fondo de guache."""
        ph = (semilla * 0.7311) % (2 * math.pi)
        amp, resp = 3.4 * vida * min(1.5, s ** 0.5), 0.03 * vida

        def tf(Pl):
            P = transformar(Pl, x, y, s, rot, flip, sq)
            return P if tv is None else vivir(P, x, y, tv, ph, amp, resp)
        if lapiz > 0.01:
            for k, op in enumerate(self.ops):
                if op[0] == "t":
                    hoja.trazo(tf(op[1]), 2.4, semilla + k * 7 + 3, fase_, 1.0, amp=2.6,
                               v=int(125 * lapiz))
        if u <= 0.001:
            return
        pos = min(1.0, u) * self.total
        for k, op in enumerate(self.ops):
            fr = (pos - self.c0[k]) / self.costes[k]
            if fr <= 0:
                break
            fr = min(1.0, fr)
            P = tf(op[1])
            sd = semilla + k * 7
            if peg:
                if op[0] == "r" or float(np.hypot(*(P[0] - P[-1]))) < 0.08 * (np.ptp(P[:, 0]) + np.ptp(P[:, 1]) + 1):
                    hoja.silueta(P)
                else:
                    hoja.silueta(P, False, op[2] * 1.6 * max(0.6, min(1.25, s ** 0.5)))
            if op[0] == "t":
                hoja.trazo(P, op[2] * ancho * max(0.6, min(1.25, s ** 0.5)), sd, fase_, fr, v=op[4])
            else:
                hoja.relleno(P, op[2], sd, fase_, fr, op[4] * max(0.7, min(1.3, s)), op[5], op[6])


# ------------------------------------------------------------------ texto manuscrito
_FUENTE = "C:/Windows/Fonts/Inkfree.ttf"


@lru_cache(maxsize=64)
def _fuente(px):
    return ImageFont.truetype(_FUENTE, px)


@lru_cache(maxsize=512)
def mascara_texto(txt, px=64):
    f = _fuente(px)
    bb = f.getbbox(txt)
    w, h = bb[2] + 10, int(px * 1.5)
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((4, 2), txt, font=f, fill=255, stroke_width=1 if px < 120 else 2, stroke_fill=255)
    return np.asarray(im, np.uint8)


def ancho_texto(txt, px=64):
    return _fuente(px).getlength(txt)


# ------------------------------------------------------------------ transformación de un objeto en otro
def remuestrear_n(P, n):
    P = np.asarray(P, float)
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    s_ = np.linspace(0, d[-1], n)
    return np.stack([np.interp(s_, d, P[:, 0]), np.interp(s_, d, P[:, 1])], 1)


def _alinear(a, b):
    """Gira/invierte el arranque de b para que se parezca lo más posible a a (evita que el contorno se retuerza)."""
    n = len(a)
    mejor, arg = 1e18, (0, False)
    for rev in (False, True):
        bb = b[::-1] if rev else b
        for sh in range(0, n, 3):
            c = float(((np.roll(bb, sh, axis=0) - a) ** 2).sum())
            if c < mejor:
                mejor, arg = c, (sh, rev)
    bb = b[::-1] if arg[1] else b
    return np.roll(bb, arg[0], axis=0)


def _partes(dib):
    return [op for op in dib.ops if op[0] == "t"], [op for op in dib.ops if op[0] == "r"]


def morfosis(hoja, A, pa, B, pb, k, fase_=0, semilla=0, tv=None, vida=1.0):
    """Dibuja el cuadro k (0..1) de la transformación del Dib A en el Dib B.
    pa, pb: dict(x, y, s, rot, flip, sq) con la posición de cada uno en pantalla (pueden ser distintas)."""
    tA, rA = _partes(A)
    tB, rB = _partes(B)
    km = e_inout(prog(k, 0.10, 0.72))
    onda = math.sin(math.pi * km)                       # el contorno "se re-traza" a mano: más temblor a mitad de camino
    ph = (semilla * 0.7311) % (2 * math.pi)

    def tf(P, p):
        Q = transformar(P, p["x"], p["y"], p["s"], p.get("rot", 0.0), p.get("flip", False), p.get("sq", 0.0))
        return Q if tv is None else vivir(Q, p["x"], p["y"], tv, ph, 3.4 * vida, 0.03 * vida)

    # 1) contornos emparejados: A se deforma en B
    for i in range(max(len(tA), len(tB))):
        if i < len(tA) and i < len(tB):
            a = remuestrear_n(tf(tA[i][1], pa), 90)
            b = _alinear(a, remuestrear_n(tf(tB[i][1], pb), 90))
            P = (1 - km) * a + km * b
            hoja.trazo(P, lerp(tA[i][2], tB[i][2], km), semilla + i * 7, fase_, 1.0, amp=1.7 + 2.6 * onda)
        elif i < len(tA):                               # sobra en A: se borra rápido
            fr = 1 - prog(k, 0.0, 0.35)
            if fr > 0:
                hoja.trazo(tf(tA[i][1], pa), tA[i][2], semilla + i * 7, fase_, fr)
        else:                                           # solo en B: se dibuja (asa, detalles)
            fr = prog(k, 0.35, 0.85)
            if fr > 0:
                hoja.trazo(tf(tB[i][1], pb), tB[i][2], semilla + i * 7, fase_, fr)
    # 2) crayón de A: se disuelve en manchas
    dA = prog(k, 0.0, 0.22)
    if dA < 1:
        for j, op in enumerate(rA):
            hoja.relleno(tf(op[1], pa), op[2], semilla + 100 + j, fase_, 1.0, op[4], op[5], op[6], disolver=max(dA, 0.001))
    # 3) crayón de B: sube desde abajo, en manchas
    fB = prog(k, 0.62, 1.0)
    if fB > 0:
        for j, op in enumerate(rB):
            hoja.relleno(tf(op[1], pb), op[2], semilla + 200 + j, fase_, fB, op[4], op[5], op[6], inv=fB < 1.0)
    # 4) garabatos de lápiz gris dentro de la forma que se está haciendo
    inten = prog(k, 0.12, 0.45) * (1 - prog(k, 0.6, 0.9))
    if inten > 0 and tB:
        allp = np.vstack([tf(o[1], pb) for o in tB])
        cx, cy = allp.mean(0)
        rx, ry = np.ptp(allp[:, 0]) / 2, np.ptp(allp[:, 1]) / 2
        rng = np.random.default_rng(semilla + 5)
        for j in range(12):
            x0 = cx + rng.uniform(-0.75, 0.75) * rx
            y0 = cy + rng.uniform(-0.45, 0.8) * ry
            ln = rng.uniform(0.25, 0.6) * ry
            an = math.radians(-62 + rng.uniform(-18, 18))
            hoja.trazo(np.array([(x0, y0), (x0 + ln * math.cos(an), y0 + ln * math.sin(an))]), 2.4, semilla + 300 + j, fase_, 1.0,
                       amp=1.5, v=int(130 * inten))
