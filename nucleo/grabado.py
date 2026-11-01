# -*- coding: utf-8 -*-
"""Kit «GRABADO DE PESTE» (docs/estilo_grabado_peste.md; creado el 14-oct-2026 para `wow_tres_noches`).

Grabado en cobre / xilografía ANIMADA al estilo de la danza macabra (Holbein, Durero, hojas volantes de la peste): tinta casi
negra sobre papel hueso. La luz es papel sin tinta; la sombra es TRAMA de líneas (paralelas, cruzadas, que siguen el contorno,
anillos o rayos), nunca un degradado. Un solo color de acento por acto en una «plancha» aparte (multiplica, con mal registro y
densidad irregular, como una estampa iluminada a mano). Las líneas HIERVEN (`HERVOR` veces por segundo cambian un poco): nada
está quieto aunque la cámara no se mueva.

    g = G(t)                                       # lienzo de papel (W x H) en el segundo t
    cielo(g, t, 640)                               # cielo de noche: líneas horizontales, estrellas talladas
    with g.cam(1.05, 960, 540):
        g.figura(pts, tono=0.2, tono2=0.7, luz=0)  # papel + trama (luz a la izquierda) + contorno de buril
        g.acento(pts, SANGRE)                      # plancha de color
        esqueleto(g, 900, 980, 1.0, pose_danza(t), t)
    img = acabado(g)                               # papel envejecido, mal registro, grano, viñeta de vela

Pintor `G` = `terror_pix.P` (transformaciones `cam/grupo/pivote/clip`, `poly`, `texto`...) más:
  trama(pts, tono, tono2, luz, ang, per, modo, cruz, borde)   sombra de líneas (modo lineal · contorno · anillos · rayos)
  papel(pts) · figura(pts, tono, ...) · trazo(pts, w, w1, ...) (línea de buril: ancho variable, punta afilada, tiembla)
  macizo(pts) (tinta sólida) · acento(pts, color) · acento_luz(x, y, r, color) (plancha de color)
Las coordenadas son las del lienzo (1920x1080) o las del `grupo` activo; la trama vive en el objeto (si la cámara se acerca,
las líneas engordan como en una lámina vista de cerca), con un periodo mínimo de 3 px en pantalla.

RENDIMIENTO (16-oct-2026; docs/estilo_grabado_peste.md § «Rendimiento»): `g = fondo(t, clave, etapas)` pinta el fondo lejano
(y lo cercano con la cámara quieta) una vez por tick de HERVOR y lo copia; `sprite(...)` estampa figuras de multitud y
vegetación desde pocas variantes cacheadas (`esqueleto_baila`, `lapida` ya lo usan). `CACHE = False` = todo desde cero.
"""
import contextlib
import functools
import math

import cv2
import numpy as np

from motor import FPS, H, W, bezier, catmull  # noqa: F401
from terror_pix import (ESC, FIN, FUENTES, INI, TL, TOTAL, Clip, P, _rejilla, ancho_texto, clamp, e_back, e_in,  # noqa: F401
                        e_out, golpe, lerp, mix, pop, pr, rnd, smooth, ww)

FUENTES.update(gotica="OLDENGL.TTF", gara="GARA.TTF", gara_b="GARABD.TTF", gara_i="GARAIT.TTF", grab="ENGR.TTF",
               capital="CASTELAR.TTF")

# ------------------------------------------------------------------ paleta
PAPEL = (0.925, 0.872, 0.770)        # hueso
PAPEL_FRIO = (0.860, 0.875, 0.860)   # papel del acto helado
TINTA = (0.070, 0.056, 0.050)        # negro de imprenta (un poco cálido)
SEPIA = (0.330, 0.220, 0.150)        # tinta diluida (textos secundarios)
SANGRE = (0.700, 0.080, 0.060)       # acentos (plancha de color)
PLAGA = (0.470, 0.620, 0.120)
HIELO = (0.600, 0.770, 0.930)
ORO = (0.840, 0.640, 0.240)
ESPECTRO = (0.700, 0.880, 0.960)

HERVOR = 8                           # veces por segundo que los CONTORNOS tiemblan (dibujo «en dos» y «en tres»)
HIERVE_TRAMA = False                 # la trama de relleno NO hierve: en superficies grandes y con cámara en movimiento
                                     # marea (el usuario, 14-oct-2026); las líneas quedan pegadas a cada objeto


def hervor(t):
    return int(math.floor(t * HERVOR + 1e-6))


# ------------------------------------------------------------------ geometría
def _remuestrear(Pt, paso, cerrado=False):
    Pt = np.asarray(Pt, np.float32)
    if cerrado:
        Pt = np.vstack([Pt, Pt[:1]])
    d = np.sqrt(((Pt[1:] - Pt[:-1]) ** 2).sum(1))
    s = np.concatenate([[0.0], np.cumsum(d)]).astype(np.float32)
    L = float(s[-1])
    if L < 1e-6:
        return Pt[:1], np.zeros(1, np.float32), 0.0
    n = max(3, int(L / max(paso, 1e-3)) + 1)
    ss = np.linspace(0.0, L, n, dtype=np.float32)
    R = np.stack([np.interp(ss, s, Pt[:, 0]), np.interp(ss, s, Pt[:, 1])], 1).astype(np.float32)
    if cerrado:
        R, ss = R[:-1], ss[:-1]
    return R, ss, L


def _normales(R, cerrado=False):
    if cerrado:
        T = np.roll(R, -1, 0) - np.roll(R, 1, 0)
    else:
        T = np.gradient(R, axis=0)
    n = np.stack([-T[:, 1], T[:, 0]], 1)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-6)


def _todos(pts):
    """Todos los puntos (Nx2) de un polígono o de una lista de polígonos."""
    if isinstance(pts, (list, tuple)) and len(pts) and np.asarray(pts[0], dtype=object).ndim == 2:
        return np.vstack([np.asarray(p, np.float32) for p in pts])
    return np.asarray(pts, np.float32)


def inflar(pts, d):
    """Polígono agrandado `d` unidades hacia fuera (contorno por «inflado» de uniones de piezas)."""
    a = np.asarray(pts, np.float32)
    c = a.mean(0)
    R, ss, _ = _remuestrear(a, max(2.0, d), True)
    n = _normales(R, True)
    sg = np.sign(((R - c) * n).sum(1)).mean() or 1.0
    return R + n * (d * (1.0 if sg > 0 else -1.0))


def tr(pts, x=0.0, y=0.0, s=1.0, ang=0.0, sx=1.0):
    """Puntos locales -> escena: espejo (sx = -1), escala, giro (radianes) y traslado."""
    a = np.asarray(pts, np.float32) * np.float32((sx * s, s))
    c, si = math.cos(ang), math.sin(ang)
    return np.stack([a[:, 0] * c - a[:, 1] * si + x, a[:, 0] * si + a[:, 1] * c + y], 1)


def circ_pts(x, y, r, n=40, ry=None):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([x + r * np.cos(a), y + (ry or r) * np.sin(a)], 1).astype(np.float32)


def capsula(a, b, r, n=9):
    """Contorno de una cápsula (hueso, rama) de a a b con radio r."""
    a, b = np.float32(a), np.float32(b)
    d = b - a
    ang = math.atan2(d[1], d[0])
    t1 = np.linspace(ang - np.pi / 2, ang + np.pi / 2, n)
    t0 = np.linspace(ang + np.pi / 2, ang + 3 * np.pi / 2, n)
    p1 = np.stack([b[0] + r * np.cos(t1), b[1] + r * np.sin(t1)], 1)
    p0 = np.stack([a[0] + r * np.cos(t0), a[1] + r * np.sin(t0)], 1)
    return np.vstack([p1, p0]).astype(np.float32)


def silueta_ruido(pts, amp, sem=0, paso=8.0, ond=(17.0, 6.3)):
    """Borde áspero: desplaza el contorno por su normal con ruido periódico (manchas, sangre, niebla)."""
    R, ss, _ = _remuestrear(pts, paso, True)
    n = _normales(R, True)
    off = amp * (0.6 * np.sin(ss / ond[0] + sem * 1.7) + 0.4 * np.sin(ss / ond[1] + sem * 3.1))
    return R + n * off[:, None]


# ------------------------------------------------------------------ trama (el corazón del estilo)
def _lineas(u, per_px, ancho):
    """Cobertura (0..1) de una familia de líneas: `u` en periodos, `ancho` = fracción del periodo con tinta."""
    f = u - np.floor(u)
    d = np.minimum(f, 1.0 - f) * per_px
    hw = ancho * (0.5 * per_px)
    return np.clip(hw + 0.5 - d, 0.0, 1.0) * np.clip(2.0 * hw, 0.0, 1.0)


def tramado(T, X, Y, s=1.0, ang=45.0, per=7.0, modo="lineal", cruz=True, k=0, dist=None, centro=None, n=140, vibra=1.0):
    """Tono (0 papel .. 1 tinta) -> cobertura de tinta con líneas de buril.
    ang = dirección de las líneas en grados (0 = horizontales). modo: lineal · contorno (siguen el borde; necesita `dist`)
    · anillos (concéntricas a `centro`) · rayos (desde `centro`, `n` rayos). cruz=False: una sola familia que engorda
    hasta casi cerrarse (grabado a la fibra / cielo de noche); cruz=True: se cruzan 2-3 familias según el tono."""
    per_px = max(per * s, 3.0)
    q = per_px / s
    a = math.radians(ang + 90.0)
    ca, sa = math.cos(a), math.sin(a)
    v = Y * ca - X * sa
    kk = k if HIERVE_TRAMA else 0
    ph1, ph2 = rnd(kk, 11) * 6.2832, rnd(kk, 12) * 6.2832
    vib = vibra * (0.06 * np.sin(v / (10.0 * q) + ph1) + 0.028 * np.sin(v / (2.7 * q) + ph2))
    pp = per_px
    if modo == "contorno" and dist is not None:
        u = dist / q
    elif modo == "anillos" and centro is not None:
        u = np.sqrt((X - centro[0]) ** 2 + (Y - centro[1]) ** 2) / q
    elif modo == "rayos" and centro is not None:
        dx, dy = X - centro[0], Y - centro[1]
        u = np.arctan2(dy, dx) * np.float32(n / 6.2832)
        pp = np.maximum(np.sqrt(dx * dx + dy * dy) * (s * 6.2832 / n), 1.6)
        vib = vib * 0.4
    else:
        u = (X * ca + Y * sa) / q
    u = u + vib
    T = np.clip(T, 0.0, 1.0)
    if not cruz:
        return np.maximum(_lineas(u, pp, T * 0.94), np.clip((T - 0.95) / 0.05, 0.0, 1.0))
    # la 1.ª familia carga casi todo el tono; las cruzadas son más finas y de otro periodo (sin «malla» mecánica)
    c = _lineas(u, pp, np.clip(T / 0.62, 0.0, 1.0) * 0.62)
    tmax = float(np.max(T))
    if tmax > 0.48:
        a2 = a + math.radians(74)
        u2 = (X * math.cos(a2) + Y * math.sin(a2)) / (q * 1.22) - vib
        c = 1.0 - (1.0 - c) * (1.0 - _lineas(u2, per_px * 1.22, np.clip((T - 0.48) / 0.40, 0.0, 1.0) * 0.30))
    if tmax > 0.78:
        a3 = a - math.radians(38)
        u3 = (X * math.cos(a3) + Y * math.sin(a3)) / (q * 0.9) + vib
        c = 1.0 - (1.0 - c) * (1.0 - _lineas(u3, per_px * 0.9, np.clip((T - 0.78) / 0.18, 0.0, 1.0) * 0.45))
    return np.maximum(c, np.clip((T - 0.95) / 0.05, 0.0, 1.0))


# ------------------------------------------------------------------ pintor
class G(P):
    """Lienzo de papel con plancha de tinta (`im`) y plancha de color (`ac`, multiplica; la corre `acabado`)."""

    def __init__(self, t, w=None, h=None, papel=PAPEL, alfa=False, k=None):
        """`alfa=True`: lienzo TRANSPARENTE (color premultiplicado + canal `alfa`) para capas que luego se desenfocan,
        se componen o se pegan en perspectiva (`capa`, `estampar`, `grabado_3d`). `k`: fija el hervor (texturas cacheadas)."""
        super().__init__(w, h)
        self.fondo_papel = papel
        self.alfa = np.zeros((self.H, self.W), np.float32) if alfa else None
        if not alfa:
            self.im[:] = np.float32(papel)
        self.ac = np.ones((self.H, self.W, 3), np.float32)
        self.t = t
        self.k = hervor(t) if k is None else k

    def _blend(self, m, x0, y0, color, op=1.0, aditivo=False):
        super()._blend(m, x0, y0, color, op, aditivo)
        if self.alfa is not None and not aditivo:
            h, w = m.shape
            a = m.astype(np.float32) * (op / 255.0)
            r = self.alfa[y0:y0 + h, x0:x0 + w]
            r *= 1.0 - a
            r += a

    # ---------------------------------------------------------------- utilidades
    def _mascara(self, pts):
        """Máscara de un polígono, o de la UNIÓN de varios (lista de arrays Nx2)."""
        if isinstance(pts, (list, tuple)) and len(pts) and np.asarray(pts[0], dtype=object).ndim == 2:
            pols = [self._t(p) for p in pts]
        else:
            pols = [self._t(pts)]
        bb = self._bb(np.vstack(pols))
        if bb is None:
            return None, None
        x0, y0, x1, y1 = bb
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        for a in pols:
            cv2.fillPoly(m, [np.round((a - (x0, y0)) * 16).astype(np.int32)], 255, cv2.LINE_AA, shift=4)
        return m, bb

    def _obj(self, x0, y0, x1, y1):
        gx, gy = _rejilla(x1 - x0, y1 - y0)
        return (gx + (x0 - self.ox)) / self.s, (gy + (y0 - self.oy)) / self.s

    @staticmethod
    def _tono(tono, tono2, luz, X, Y, pts):
        if callable(tono):
            return np.asarray(tono(X, Y), np.float32)
        if tono2 is None:
            return np.full(X.shape, tono, np.float32)
        a = _todos(pts)
        cx, cy = a.mean(0)
        ext = max(float(np.ptp(a[:, 0])), float(np.ptp(a[:, 1])), 1.0) / 2
        r = math.radians(luz)
        d = ((X - cx) * math.cos(r) + (Y - cy) * math.sin(r)) / ext
        return tono + (tono2 - tono) * np.clip(0.5 + 0.5 * d, 0.0, 1.0)

    # ---------------------------------------------------------------- planchas
    def trama(self, pts, tono=0.5, tono2=None, luz=0.0, ang=45.0, per=7.0, modo="lineal", cruz=True, borde=0.0, rb=30.0,
              centro=None, n=140, op=1.0, color=TINTA, mascara=None, vibra=1.0):
        """Sombra de líneas dentro del polígono. `tono2` + `luz`: degradado de tono de `tono` (lado de la luz) a `tono2`
        en la dirección `luz` (grados; 0 = la luz viene de la izquierda). `borde`: oscurece cerca del contorno (volumen)."""
        if op <= 0.004:
            return
        m, bb = self._mascara(pts) if mascara is None else mascara
        if m is None:
            return
        x0, y0, x1, y1 = bb
        X, Y = self._obj(*bb)
        T = self._tono(tono, tono2, luz, X, Y, pts)
        dist = None
        if modo == "contorno" or borde > 0:
            dist = cv2.distanceTransform((m > 100).astype(np.uint8), cv2.DIST_L2, 5) / self.s
        if borde > 0:
            T = T + borde * (1.0 - np.clip(dist / rb, 0.0, 1.0)) ** 1.5
        if float(np.max(T)) < 0.01:
            return
        cov = tramado(T, X, Y, self.s, ang, per, modo, cruz, self.k, dist, centro, n, vibra)
        self._blend(m.astype(np.float32) * cov, x0, y0, color, op)

    def papel(self, pts, op=1.0, color=None):
        """Tapa con papel (y limpia la plancha de color): lo que se dibuje encima queda delante."""
        m, bb = self._mascara(pts)
        if m is None or op <= 0.004:
            return None, None
        x0, y0, x1, y1 = bb
        self._blend(m, x0, y0, color or self.fondo_papel, op)
        a = m.astype(np.float32)[..., None] * (op / 255.0)
        r = self.ac[y0:y1, x0:x1]
        r += (1.0 - r) * a
        return m, bb

    def figura(self, pts, tono=0.0, contorno=2.4, op=1.0, papel=True, **kw):
        """Papel + trama + contorno de buril: la forma estándar de dibujar un objeto que tapa lo de atrás."""
        mb = self.papel(pts, op) if papel else self._mascara(pts)
        if mb[0] is None:
            return
        if callable(tono) or tono > 0 or kw.get("tono2"):
            self.trama(pts, tono, op=op, mascara=mb, **kw)
        if contorno:
            self.trazo(pts, contorno, op=op, cerrado=True, afilado=0.0)

    def figura_union(self, piezas, tono=0.0, contorno=2.4, op=1.0, **kw):
        """Como `figura`, pero de la UNIÓN de varias piezas (nube de bucles, hueso con cabezas): un solo contorno
        exterior por inflado (tinta debajo, papel encima) y una trama continua sobre todo."""
        if contorno:
            for pz in piezas:
                self.macizo(inflar(pz, contorno), op)
        mb = self.papel(list(piezas), op)
        if mb[0] is None:
            return
        if callable(tono) or tono > 0 or kw.get("tono2"):
            self.trama(list(piezas), tono, op=op, mascara=mb, **kw)

    def macizo(self, pts, op=1.0, color=TINTA):
        if isinstance(pts, (list, tuple)) and len(pts) and np.asarray(pts[0], dtype=object).ndim == 2:
            m, bb = self._mascara(pts)
            if m is not None:
                self._blend(m, bb[0], bb[1], color, op)
            return
        self.poly(pts, color, op)

    def trazo(self, pts, w=3.0, w1=None, color=TINTA, op=1.0, cerrado=False, afilado=0.6, temblor=1.0, sem=0, var=0.22,
              anchos=None):
        """Línea de buril: ancho que respira, puntas afiladas y un temblor que cambia `HERVOR` veces por segundo.
        `w1`: ancho al final (rama que adelgaza); `anchos`: un ancho por punto (líneas en perspectiva). Anchos en unidades
        del grupo actual (mínimo ~0,8 px en pantalla)."""
        if op <= 0.004 or len(pts) < 2:
            return
        s = max(self.s, 1e-3)
        R, ss, L = _remuestrear(pts, 5.0 / s, cerrado)
        if len(R) < 2 or L <= 0:
            return
        k = self.k
        ph = [rnd(k + 31 * sem, j) * 6.2832 for j in range(3)]
        n = _normales(R, cerrado)
        off = temblor * (0.40 * np.sin(ss * s / 29.0 + ph[0]) + 0.20 * np.sin(ss * s / 10.0 + ph[1])) / s
        if anchos is not None:
            P0 = np.asarray(pts, np.float32)
            s0 = np.concatenate([[0.0], np.cumsum(np.sqrt(((P0[1:] - P0[:-1]) ** 2).sum(1)))])
            wi = np.interp(ss, s0, np.asarray(anchos, np.float32)).astype(np.float32)
        elif w1 is None:
            wi = np.full(len(R), float(w), np.float32)
        else:
            wi = (w + (w1 - w) * ss / L).astype(np.float32)
        wi = wi * (1.0 + var * np.sin(ss * s / 23.0 + ph[2]))
        if not cerrado and afilado > 0:
            e = np.minimum(ss, L - ss) * s
            wi = wi * ((1.0 - afilado) + afilado * np.clip(e / max(3.0 * float(np.max(wi)) * s, 6.0), 0.0, 1.0) ** 0.6)
        wi = np.maximum(wi, 0.8 / s)
        C = R + n * off[:, None]
        izq = C + n * (wi[:, None] / 2)
        der = C - n * (wi[:, None] / 2)
        if cerrado:
            pol = np.vstack([izq, izq[:1], der[:1], der[::-1]])
        else:
            pol = np.vstack([izq, der[::-1]])
        self.poly(pol, color, op)

    def acento(self, pts, color=SANGRE, op=0.85, aspero=1.0, sem=0):
        """Plancha de color (multiplica): manchas de acuarela/estarcido con borde áspero."""
        if op <= 0.004:
            return
        R = silueta_ruido(pts, 3.0 * aspero / max(self.s, 0.2), sem, 9.0 / max(self.s, 0.2)) if aspero else pts
        m, bb = self._mascara(R)
        if m is None:
            return
        x0, y0, x1, y1 = bb
        a = m.astype(np.float32)[..., None] * (op / 255.0)
        r = self.ac[y0:y1, x0:x1]
        r *= 1.0 - a * (1.0 - np.float32(color))

    def acento_luz(self, x, y, r, color=ESPECTRO, amt=0.6, pot=1.6):
        """Mancha de color redonda y difusa en la plancha de color (aura, niebla de sangre)."""
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
        f = (np.clip(1 - d, 0, 1) ** pot * amt)[..., None]
        reg = self.ac[y0:y1, x0:x1]
        reg *= 1.0 - f * (1.0 - np.float32(color))


# ------------------------------------------------------------------ capas (profundidad de campo, bruma)
@contextlib.contextmanager
def capa(g, desenfoque=0.0, bruma=0.0, color_bruma=None, op=1.0):
    """Dibuja en una capa TRANSPARENTE con la cámara actual y la compone al salir: `desenfoque` = sigma en px (profundidad
    de campo: primer plano o fondo fuera de foco), `bruma` 0..1 (se funde hacia `color_bruma`, por defecto el papel:
    lejanía), `op`.      with capa(g, desenfoque=7) as c:  GR.lapida(c, ...)"""
    c = G(g.t, g.W, g.H, g.fondo_papel, alfa=True, k=g.k)
    c.s, c.ox, c.oy, c.rec = g.s, g.ox, g.oy, g.rec
    yield c
    componer(g, c, desenfoque, bruma, color_bruma, op)


def componer(g, c, desenfoque=0.0, bruma=0.0, color_bruma=None, op=1.0, dx=0, dy=0):
    """Compone la capa transparente `c` sobre `g` (mismo tamaño) con desenfoque, bruma y opacidad."""
    ys, xs = np.nonzero(c.alfa > 0.002)
    if len(ys) == 0 or op <= 0.004:
        return
    pad = int(3 * desenfoque) + 2
    y0, y1 = max(0, ys.min() - pad), min(c.H, ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(c.W, xs.max() + pad + 1)
    im, A, ac = c.im[y0:y1, x0:x1], c.alfa[y0:y1, x0:x1], c.ac[y0:y1, x0:x1]
    if bruma > 0:
        im = im * (1 - bruma) + np.float32(color_bruma or g.fondo_papel) * (bruma * A)[..., None]
    if desenfoque > 0.3:
        im = cv2.GaussianBlur(im, (0, 0), desenfoque)
        A = cv2.GaussianBlur(A, (0, 0), desenfoque)
        ac = 1.0 - cv2.GaussianBlur(1.0 - ac, (0, 0), desenfoque)
    A = A * op
    gy0, gy1, gx0, gx1 = y0 + dy, y1 + dy, x0 + dx, x1 + dx
    if gx0 < 0 or gy0 < 0 or gx1 > g.W or gy1 > g.H:
        return
    reg = g.im[gy0:gy1, gx0:gx1]
    reg *= 1.0 - A[..., None]
    reg += im * op
    rac = g.ac[gy0:gy1, gx0:gx1]
    rac *= 1.0 - A[..., None]
    rac += ac * A[..., None]
    if g.alfa is not None:
        ra = g.alfa[gy0:gy1, gx0:gx1]
        ra *= 1.0 - A
        ra += A


# ------------------------------------------------------------------ cachés de rendimiento (16-oct-2026)
# Un cuadro se dibujaba entero desde cero (~3 s a 1080p) aunque la trama no hierva y los contornos cambien solo HERVOR
# veces por segundo. Dos cachés (docs/estilo_grabado_peste.md § «Rendimiento»):
#   fondo(t, clave, etapas)    el FONDO LEJANO (cielo, colinas, muros...) se dibuja una vez por tick de HERVOR y se copia
#   sprite(g, clave, x, y, s, dibujar, caja)   figuras de multitud y vegetación ESTAMPADAS desde pocas variantes cacheadas
CACHE = True                    # False: todo se dibuja como antes (comparar / depurar)
SPRITE_CICLO = 3                # los sprites hierven «en tres»: 3 dibujos de contorno que se repiten (no uno por tick)
SPRITE_PASO = 1.04              # escalones de escala del sprite (4 %); se reescala al tamaño exacto al estamparlo
SPRITE_MAX_MB = 300             # memoria máxima de sprites por proceso (uint8; se tiran los más viejos)
FONDO_TOL = 1.5                 # px: si el fondo se movería más que esto dentro del tick, se dibuja en vivo (hasta ahí la
                                # luna o la colina avanzan a saltos de tick, como el hervor; lo cercano usa G3.firma_cerca,
                                # que escala su firma para tolerar solo ~0,75 px: los pies no resbalan)
_SPRITES = {}
_SPRITES_MB = [0.0]
_FONDOS = {}
ESTAD = {"sprite_hit": 0, "sprite_miss": 0, "fondo_hit": 0, "fondo_miss": 0, "fondo_vivo": 0}


def t_tick(t):
    """Inicio del tick de HERVOR del segundo t (lo cacheado se dibuja SIEMPRE en este instante: determinista)."""
    return hervor(t) / float(HERVOR)


def fondo(t, clave, etapas, papel=PAPEL):
    """Lienzo G(t) con el fondo YA DIBUJADO. `etapas` = [(dibujar(g, tt), firma(tt)), ...] en orden de pintado (lo primero
    que se pinta en el cuadro). La firma es una tupla de px de pantalla de los que depende la etapa (horizonte, x de la
    luna, paralaje, cámara...): si ninguno cambia FONDO_TOL px o más dentro del tick, la etapa se reutiliza. Se cachea el
    PREFIJO de etapas que cumplen: se pintan en el instante del tick (t_tick) una vez y se copian en los cuadros
    siguientes; las demás (cámara que se mueve rápido) se pintan en vivo en t, encima. Con cámara quieta, todas cuestan una
    copia de memoria. OJO: la imagen cacheada NO se corre para seguir al horizonte: las rayas del cielo están fijas en
    pantalla y correrlas las haría temblar a 8 Hz (probado el 16-oct-2026)."""
    g = G(t, papel=papel)
    if not CACHE:
        for dib, _ in etapas:
            dib(g, t)
        return g
    tt = t_tick(t)
    n = 0
    for _, firma in etapas:
        if firma is not None:
            a, b = firma(tt), firma(t)
            if max((abs(float(x) - float(y)) for x, y in zip(a, b)), default=0.0) >= FONDO_TOL:
                break
        n += 1
    if n:
        key = (clave, g.k, n)
        if key in _FONDOS:
            im, ac = _FONDOS[key]
            g.im[:] = im
            if ac is not None:
                g.ac[:] = ac
            ESTAD["fondo_hit"] += 1
        else:
            g.t = tt
            for dib, _ in etapas[:n]:
                dib(g, tt)
            g.t = t
            if len(_FONDOS) >= 2:                          # el del tick anterior y este (cada uno ~25-50 MB)
                _FONDOS.pop(next(iter(_FONDOS)))
            _FONDOS[key] = (g.im.copy(), None if float(g.ac.min()) > 0.9999 else g.ac.copy())
            ESTAD["fondo_miss"] += 1
    for dib, _ in etapas[n:]:
        dib(g, t)
        ESTAD["fondo_vivo"] += 1
    return g


def sprite(g, clave, x, y, s, dibujar, caja, op=1.0):
    """Estampa en `g` una figura CACHEADA con su punto de suelo en (x, y) y escala s (coordenadas del grupo actual).
    dibujar(c, ax, ay, s_) la dibuja sobre el lienzo transparente c (punto de suelo en (ax, ay), escala s_). `clave` = todo
    lo que cambia el dibujo (tipo, pose CUANTIZADA, tono, op...); la escala (escalones de SPRITE_PASO) y el hervor
    (g.k % SPRITE_CICLO) se añaden aquí. `caja` = (x0, y0, x1, y1) de la figura en unidades locales con s=1, con margen.
    Solo para figuras que no tocan la plancha de color fuera de su silueta y no leen lo de debajo. Lo que cae fuera del
    cuadro no se dibuja; lo grande y medio cortado por el borde se dibuja en vivo (sale más barato)."""
    if s <= 1e-4 or op <= 0.004:
        return
    if not CACHE:
        dibujar(g, x, y, s)
        return
    (sx, sy), ss = g._t([(x, y)])[0], s * g.s
    x0, y0, x1, y1 = caja
    bx0, by0, bx1, by1 = sx + x0 * ss, sy + y0 * ss, sx + x1 * ss, sy + y1 * ss
    vis = max(0.0, min(bx1, g.rec[2]) - max(bx0, g.rec[0])) * max(0.0, min(by1, g.rec[3]) - max(by0, g.rec[1]))
    area = (bx1 - bx0) * (by1 - by0)
    if vis <= 0:
        return
    if vis < 0.6 * area and area > 60000 or area > 2600 * 2000:
        dibujar(g, x, y, s)
        return
    ns = int(round(math.log(ss) / math.log(SPRITE_PASO)))
    kk = g.k % SPRITE_CICLO
    key = (clave, ns, kk)
    spr = _SPRITES.get(key)
    if spr is None:
        sb = SPRITE_PASO ** ns
        w, h = int(math.ceil((x1 - x0) * sb)) + 8, int(math.ceil((y1 - y0) * sb)) + 8
        c = G(g.t, w, h, g.fondo_papel, alfa=True, k=kk)
        ax, ay = -x0 * sb + 4, -y0 * sb + 4
        dibujar(c, ax, ay, sb)
        filas, cols = np.nonzero((c.alfa > 0.002).any(1))[0], np.nonzero((c.alfa > 0.002).any(0))[0]
        if len(filas) == 0:
            spr = (None,)
        else:
            a0, a1, b0, b1 = filas[0], filas[-1] + 1, cols[0], cols[-1] + 1
            rgba = np.dstack([c.im[a0:a1, b0:b1], c.alfa[a0:a1, b0:b1]])
            rgba = np.clip(rgba * 255.0 + 0.5, 0, 255).astype(np.uint8)
            ac = c.ac[a0:a1, b0:b1]
            ac = None if float(ac.min()) > 0.998 else np.clip(ac * 255.0 + 0.5, 0, 255).astype(np.uint8)
            spr = (rgba, ac, ax - b0, ay - a0, sb)
            _SPRITES_MB[0] += (rgba.nbytes + (0 if ac is None else ac.nbytes)) / 1e6
        _SPRITES[key] = spr
        while _SPRITES_MB[0] > SPRITE_MAX_MB and len(_SPRITES) > 1:
            viejo = _SPRITES.pop(next(iter(_SPRITES)))
            if viejo[0] is not None:
                _SPRITES_MB[0] -= (viejo[0].nbytes + (0 if viejo[1] is None else viejo[1].nbytes)) / 1e6
        ESTAD["sprite_miss"] += 1
    else:
        ESTAD["sprite_hit"] += 1
    if spr[0] is None:
        return
    rgba, ac, ax, ay, sb = spr
    r = ss / sb
    h, w = rgba.shape[:2]
    X0, Y0 = int(math.floor(sx - r * ax)) - 1, int(math.floor(sy - r * ay)) - 1
    X1, Y1 = X0 + int(math.ceil(r * w)) + 3, Y0 + int(math.ceil(r * h)) + 3
    cx0, cy0, cx1, cy1 = max(X0, g.rec[0]), max(Y0, g.rec[1]), min(X1, g.rec[2]), min(Y1, g.rec[3])
    if cx1 - cx0 < 1 or cy1 - cy0 < 1:
        return
    M = np.float32([[r, 0, sx - r * ax - cx0], [0, r, sy - r * ay - cy0]])
    sz = (cx1 - cx0, cy1 - cy0)
    q = cv2.warpAffine(rgba, M, sz, flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0)).astype(np.float32)
    q *= np.float32(op / 255.0)
    imw, A3 = q[..., :3], q[..., 3:]
    reg = g.im[cy0:cy1, cx0:cx1]
    reg *= 1.0 - A3
    reg += imw
    rac = g.ac[cy0:cy1, cx0:cx1]
    if ac is None:                                         # sin plancha de color: el papel de la figura la limpia
        rac += (1.0 - rac) * A3
    else:
        acw = cv2.warpAffine(ac, M, sz, flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255)).astype(np.float32)
        rac *= 1.0 - A3
        rac += acw * (A3 / 255.0)
    if g.alfa is not None:
        ra = g.alfa[cy0:cy1, cx0:cx1]
        ra *= 1.0 - A3[..., 0]
        ra += A3[..., 0]


def fase_cuant(fase, pasos):
    """Fase (radianes) cuantizada a `pasos` por vuelta: (índice 0..pasos-1, fase cuantizada). Para poses de sprites."""
    i = int(round(fase / 6.283185307 * pasos)) % pasos
    return i, i * 6.283185307 / pasos


# ------------------------------------------------------------------ papel y acabado
@functools.lru_cache(maxsize=4)
def _octava(cel, sem):
    rng = np.random.default_rng(9000 + cel * 7 + sem)
    peq = rng.random((H // cel + 3, W // cel + 3)).astype(np.float32)
    return cv2.resize(peq, (W, H), interpolation=cv2.INTER_CUBIC)


@functools.lru_cache(maxsize=1)
def _textura_papel():
    """Papel de trapo envejecido: moteado, fibras, manchas de óxido y bordes amarillentos (multiplica)."""
    rng = np.random.default_rng(1505)
    n = 0.42 * _octava(260, 0) + 0.28 * _octava(80, 0) + 0.18 * _octava(22, 0) + 0.12 * _octava(5, 0)
    n = (n - n.mean()) / (n.std() + 1e-6)
    tex = 1.0 + 0.032 * n
    fib = np.zeros((H, W), np.float32)
    for _ in range(2600):
        x, y = rng.random() * W, rng.random() * H
        a = rng.random() * math.pi
        L = 5 + rng.random() ** 2 * 36
        cv2.line(fib, (int(x), int(y)), (int(x + L * math.cos(a)), int(y + L * math.sin(a))), float(rng.random() * 2 - 1), 1,
                 cv2.LINE_AA)
    tex += 0.05 * cv2.GaussianBlur(fib, (0, 0), 0.7)
    rgb = np.repeat(tex[..., None], 3, 2).astype(np.float32)
    for _ in range(34):                                       # manchas de óxido (foxing)
        cx, cy = rng.random() * W, rng.random() * H
        r = 3 + rng.random() ** 3 * 60
        R = int(r * 3) + 2
        x0, y0, x1, y1 = max(0, int(cx - R)), max(0, int(cy - R)), min(W, int(cx + R)), min(H, int(cy + R))
        if x1 <= x0 or y1 <= y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) - cx, np.arange(y0, y1) - cy)
        f = np.exp(-(gx ** 2 + gy ** 2) / (2 * r * r)).astype(np.float32) * (0.03 + 0.09 * rng.random())
        rgb[y0:y1, x0:x1] -= f[..., None] * np.float32((0.22, 0.50, 0.95))
    gx, gy = _rejilla(W, H)
    d = np.minimum(np.minimum(gx, W - 1 - gx) / W, np.minimum(gy, H - 1 - gy) / H)
    ed = np.clip(1 - d / 0.075, 0, 1) ** 2 * (0.75 + 0.5 * (_octava(80, 1) - 0.5))
    rgb -= ed[..., None] * np.float32((0.16, 0.27, 0.42))
    return np.clip(rgb, 0.55, 1.15).astype(np.float32)


@functools.lru_cache(maxsize=1)
def _mancha_color():
    """Densidad irregular de la plancha de color (0,72..1): acuarela dada a mano."""
    n = 0.6 * _octava(60, 3) + 0.4 * _octava(14, 3)
    return (0.72 + 0.28 * np.clip((n - 0.25) / 0.5, 0, 1)).astype(np.float32)


@functools.lru_cache(maxsize=1)
def _granos():
    rng = np.random.default_rng(77)
    return [cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.7) for _ in range(3)]


@functools.lru_cache(maxsize=1)
def _motas():
    """Motas de papel que asoman en la tinta sólida (la tinta nunca cubre parejo)."""
    rng = np.random.default_rng(78)
    out = []
    for _ in range(3):
        n = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 1.3)
        out.append(np.clip((n - 0.55) / 0.35, 0, 1).astype(np.float32))
    return out


@functools.lru_cache(maxsize=1)
def _vineta():
    gx, gy = _rejilla(W, H)
    d = np.sqrt(((gx - W / 2) / (W * 0.60)) ** 2 + ((gy - H * 0.46) / (H * 0.62)) ** 2)
    return (1 - 0.62 * np.clip(d - 0.42, 0, 1) ** 1.35).astype(np.float32)


def acabado(g, golpe=0.0, flash=0.0, vineta=1.0, registro=(3, -2), grano=0.6, oscuro=0.0, negativo=0.0, vaiven=0.0):
    """Estampa terminada: plancha de color corrida (mal registro) y dispareja, tinta con motas, sangrado leve, papel
    envejecido, grano, viñeta de vela que parpadea, vaivén de la hoja. `golpe` = sacudida (sustos); `negativo` 0..1 invierte
    la estampa (solo en golpes de 1-2 cuadros); `oscuro` apaga la luz de la vela."""
    t, k = g.t, g.k
    ac = g.ac
    if registro and (registro[0] or registro[1]):
        ac = np.roll(ac, (registro[1], registro[0]), axis=(0, 1))
    ac = 1.0 - (1.0 - ac) * _mancha_color()[..., None]
    im = g.im * ac
    lum = im.mean(2)
    neg = np.clip((0.24 - lum) / 0.16, 0, 1)
    im += (neg * _motas()[0] * 0.13)[..., None] * np.float32(g.fondo_papel)
    im = cv2.GaussianBlur(im, (0, 0), 0.55)
    im *= _textura_papel()
    im += (_granos()[k % 3] * (0.020 * grano))[..., None]
    fl = 1.0 + 0.018 * math.sin(t * 7.3) + 0.011 * math.sin(t * 17.9 + 1.3) - oscuro
    im *= ((1.0 - vineta * (1.0 - _vineta())) * fl)[..., None]
    dx = vaiven * 0.6 * math.sin(k * 1.73)
    dy = vaiven * 0.5 * math.sin(k * 2.31 + 1.0)
    z = 1.0
    if golpe > 0.01:
        kk = int(t * FPS)
        dx += (rnd(kk, 1) - 0.5) * 46 * golpe
        dy += (rnd(kk, 2) - 0.5) * 46 * golpe
        z = 1 + 0.035 * golpe
    if abs(dx) + abs(dy) > 0.05 or z != 1.0:
        M = np.float32([[z, 0, dx - W * (z - 1) / 2], [0, z, dy - H * (z - 1) / 2]])
        im = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if negativo > 0.003:
        im = im * (1 - negativo) + (np.float32(PAPEL) - im + np.float32(TINTA)) * negativo
    if flash > 0.003:
        im = im + flash
    return np.clip(im, 0, 1).astype(np.float32)


# ------------------------------------------------------------------ cielo, luna, nubes, tierra
def cielo(g, t, y1, tono_alto=0.93, tono_bajo=0.60, per=6.5, estrellas=46, sem=0, x0=-60, x1=W + 60, y0=-60):
    """Cielo de noche grabado: líneas horizontales que engordan hacia arriba y estrellas talladas que titilan."""
    g.trama([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], tono_alto, tono2=tono_bajo, luz=90, ang=0, per=per, cruz=False)
    for i in range(estrellas):
        x = x0 + rnd(i, 1 + sem) * (x1 - x0)
        y = y0 + rnd(i, 2 + sem) ** 1.6 * (y1 - y0) * 0.85
        tw = 0.55 + 0.45 * math.sin(t * (0.8 + 2.2 * rnd(i, 3)) + i * 1.7)
        r = 1.2 + 2.6 * rnd(i, 4) ** 3
        g.circ(x, y, r, g.fondo_papel, 0.9 * tw)
        if r > 2.5:
            L = r * (3.2 + 1.2 * tw)
            g.trazo([(x - L, y), (x + L, y)], 1.3, color=g.fondo_papel, op=0.85 * tw, afilado=1.0, temblor=0.3)
            g.trazo([(x, y - L), (x, y + L)], 1.3, color=g.fondo_papel, op=0.85 * tw, afilado=1.0, temblor=0.3)


def luna(g, x, y, r, t, halo=2.5, tono_cielo=0.80, per=6.5):
    """Luna grabada: el cielo se aclara a su alrededor (misma trama del cielo, sin costura), disco con sombra en anillos,
    cráteres y dos anillos de halo tallados."""
    g.papel(circ_pts(x, y, r * halo, 72))
    g.trama(circ_pts(x, y, r * halo, 72), lambda X, Y: np.clip(
        tono_cielo * (np.sqrt((X - x) ** 2 + (Y - y) ** 2) / (r * halo)) ** 1.4, 0, 1), ang=0, per=per, cruz=False)
    for i, (f, op) in enumerate(((1.28, 0.55), (1.62, 0.35))):
        g.trazo(circ_pts(x, y, r * f + 2 * math.sin(t * 0.7 + i), 90), 1.4, color=g.fondo_papel, op=op, cerrado=True)
    disco = circ_pts(x, y, r, 72)
    g.figura(disco, 0.0, contorno=2.2, tono2=0.42, luz=35, modo="anillos", centro=(x - r * 0.35, y - r * 0.3), per=5.5,
             cruz=False)
    for i in range(6):
        cx = x + (rnd(i, 21) - 0.5) * r * 1.2
        cy = y + (rnd(i, 22) - 0.5) * r * 1.2
        if (cx - x) ** 2 + (cy - y) ** 2 < (r * 0.75) ** 2:
            rr = r * (0.06 + 0.12 * rnd(i, 23))
            g.trazo(circ_pts(cx, cy, rr, 18), 1.2, op=0.55, cerrado=True)


def nube(g, x, y, ancho, t, tono=0.22, tono2=0.62, sem=0, vel=6.0, alto=None):
    """Nube de lámina antigua: base plana, lomo de bucles, trama horizontal (luz de arriba) y rizos en la base."""
    x = x + t * vel
    alto = alto or ancho * 0.34
    nb = max(3, int(ancho / 75))
    piezas = [circ_pts(x, y - alto * 0.16, ancho * 0.5, 44, alto * 0.26)]
    bucles = []
    for i in range(nb):
        u = (i + 0.5) / nb
        bx = x - ancho * 0.40 + ancho * 0.80 * u
        r = ancho / nb * (0.56 + 0.30 * rnd(i, sem + 40))
        hy = alto * (0.22 + 0.50 * math.sin(math.pi * u)) * (0.8 + 0.2 * rnd(i, sem + 41))
        bucles.append((bx, y - hy, r))
        piezas.append(circ_pts(bx, y - hy, r, 30))
    g.figura_union(piezas, tono, contorno=2.2, tono2=tono2, luz=90, ang=0, per=6.5, cruz=False)
    for i, (bx, by, r) in enumerate(bucles[1:]):
        a = np.radians(np.linspace(150, 232, 9))
        g.trazo(np.stack([bx + r * np.cos(a), by + r * np.sin(a)], 1), 1.7, op=0.8, sem=i)


def colina(g, perfil, tono=0.45, tono2=0.8, ang=-8, per=6.0, contorno=2.6, fondo=H + 80, cruz=True, luz=90):
    """Masa de tierra bajo un perfil [(x, y), ...] (de izquierda a derecha): papel, trama y un solo contorno arriba."""
    perfil = np.float32(perfil)
    pol = np.vstack([perfil, [(perfil[-1, 0], fondo), (perfil[0, 0], fondo)]])
    g.papel(pol)
    g.trama(pol, tono, tono2=tono2, luz=luz, ang=ang, per=per, cruz=cruz)
    if contorno:
        g.trazo(perfil, contorno, afilado=0.0)


def perfil_colina(x0, x1, y, amp, sem=0, n=24, ondas=2.0):
    xs = np.linspace(x0, x1, n)
    u = (xs - x0) / max(x1 - x0, 1)
    ys = y - amp * (0.55 * np.sin(u * math.pi * ondas + sem) + 0.3 * np.sin(u * math.pi * ondas * 2.7 + sem * 2.1)
                    + 0.15 * np.sin(u * math.pi * ondas * 6.1 + sem * 0.7))
    return catmull(np.stack([xs, ys], 1), 6)


def pasto(g, x, y, s, t, n=7, sem=0, op=1.0, color=TINTA):
    """Mata de hierba seca que se mece con el viento."""
    for i in range(n):
        a = math.radians(-90 + (i - (n - 1) / 2) * (100 / max(n - 1, 1)) + 10 * (rnd(i, sem) - 0.5))
        L = s * (16 + 22 * rnd(i, sem + 1))
        sw = s * 5 * math.sin(t * 1.4 + x * 0.013 + i * 0.6)
        p0 = (x + (i - n / 2) * s * 1.6, y)
        p2 = (p0[0] + L * math.cos(a) + sw, p0[1] + L * math.sin(a))
        p1 = ((p0[0] + p2[0]) / 2 - sw * 0.3, (p0[1] + p2[1]) / 2)
        g.trazo(np.float32([p0, p1, p2]), 1.9 * s, op=op, color=color, afilado=0.9, temblor=0.4)


def niebla(g, y0, y1, t, op=0.55, vel=18.0, n=9, sem=0, x0=-200, x1=W + 200):
    """Bancos de niebla: trazos largos de papel (tallados) que se arrastran sobre lo de atrás."""
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 0.5) / n + 6 * math.sin(t * 0.5 + i)
        L = 260 + 380 * rnd(i, sem + 50)
        x = x0 + ((rnd(i, sem + 51) * (x1 - x0) + t * vel * (0.6 + 0.8 * rnd(i, sem + 52))) % (x1 - x0))
        xs = np.linspace(x - L / 2, x + L / 2, 14)
        ys = y + 7 * np.sin(xs * 0.011 + t * 0.8 + i)
        g.trazo(np.stack([xs, ys], 1), 3 + 7 * rnd(i, sem + 53), color=g.fondo_papel, op=op * (0.5 + 0.5 * rnd(i, sem + 54)),
                afilado=1.0, temblor=0.6)


# ------------------------------------------------------------------ utilería de cementerio
def lapida(g, x, y, s, forma="arco", inclin=0.0, texto="", tono=0.22, tono2=0.62, sem=0, grieta=True):
    """Lápida con canto (volumen), trama de luz lateral, marco tallado, grieta y musgo. (x, y) = base al centro.
    No depende del tiempo: se ESTAMPA desde un sprite cacheado (`sprite`) salvo las de primer plano."""
    if not CACHE or 160 * s * g.s > 700:
        return _lapida(g, x, y, s, forma, inclin, texto, tono, tono2, sem, grieta)
    sprite(g, ("lapida", forma, round(inclin, 1), texto, round(tono, 2), round(tono2, 2), sem, grieta), x, y, s,
           lambda c, ax, ay, s_: _lapida(c, ax, ay, s_, forma, inclin, texto, tono, tono2, sem, grieta),
           (-110, -170, 110, 40))


def _lapida(g, x, y, s, forma="arco", inclin=0.0, texto="", tono=0.22, tono2=0.62, sem=0, grieta=True):
    a = math.radians(inclin)
    if forma == "cruz":
        loc = [(-0.09, 0), (0.09, 0), (0.09, -0.62), (0.32, -0.62), (0.32, -0.78), (0.09, -0.78), (0.09, -1.05),
               (-0.09, -1.05), (-0.09, -0.78), (-0.32, -0.78), (-0.32, -0.62), (-0.09, -0.62)]
    elif forma == "plana":
        loc = [(-0.34, 0), (0.34, 0), (0.34, -0.72), (0.26, -0.8), (-0.26, -0.8), (-0.34, -0.72)]
    else:
        arc = [(0.3 * math.cos(u), -0.72 + 0.3 * math.sin(u)) for u in np.linspace(0, -math.pi, 16)]
        loc = [(-0.3, 0), (0.3, 0)] + arc + [(-0.3, 0)]
    loc = np.float32(loc)
    canto = tr(loc + np.float32((0.07, -0.03)), x, y, s * 120, a)
    g.figura(canto, 0.78, contorno=2.0, ang=80, per=5.5, cruz=False)
    cara = tr(loc, x, y, s * 120, a)
    g.figura(cara, tono, tono2=tono2, luz=0, ang=70, per=6.0, borde=0.25, rb=10 * s, contorno=2.6)
    if forma != "cruz":
        g.trazo(tr(loc * 0.82 + np.float32((0, -0.05)), x, y, s * 120, a), 1.3, cerrado=True, op=0.75)
    if texto and abs(inclin) < 4:
        g.texto(texto, x, y - s * 120 * 0.5, max(10, int(s * 24)), TINTA, "grab", 0.85)
    if grieta:
        pts = [(0.05 + 0.1 * rnd(sem, 1), -0.75), (0.0, -0.55), (0.09, -0.42), (0.02, -0.25)]
        g.trazo(tr(np.float32(pts), x, y, s * 120, a), 1.4, op=0.85)
    g.trama(tr(np.float32([(-0.36, 0.02), (0.38, 0.02), (0.32, -0.1), (0.1, -0.16), (-0.2, -0.12)]), x, y, s * 120, a),
            0.85, ang=-30, per=4.0, cruz=False)


def reja(g, x0, x1, y, alto, t, paso=34.0, s=1.0, op=1.0):
    """Reja de cementerio: barrotes con punta de lanza, dos travesaños; tinta sólida con brillo tallado."""
    for yy in (y - alto * 0.18, y - alto * 0.78):
        g.macizo([(x0, yy - 3 * s), (x1, yy - 3 * s), (x1, yy + 3 * s), (x0, yy + 3 * s)], op)
    xs = np.arange(x0, x1 + 1, paso * s)
    for i, xx in enumerate(xs):
        top = y - alto - (8 * s if i % 2 else 0)
        g.macizo([(xx - 2.6 * s, y), (xx + 2.6 * s, y), (xx + 2.6 * s, top), (xx - 2.6 * s, top)], op)
        g.macizo([(xx - 7 * s, top + 2 * s), (xx, top - 16 * s), (xx + 7 * s, top + 2 * s), (xx, top - 2 * s)], op)
        g.trazo([(xx - 0.8 * s, y - 4), (xx - 0.8 * s, top + 6 * s)], 1.0 * s, color=g.fondo_papel, op=0.35 * op, afilado=1)


def _rama(g, x, y, ang, L, w, prof, t, sem, maxp, tallado):
    sw = 0.035 * math.sin(t * 0.9 + sem + prof * 1.3) * prof
    a = ang + sw
    x2, y2 = x + L * math.cos(a), y + L * math.sin(a)
    dob = (rnd(sem, prof * 7 + 1) - 0.5) * 0.5 * L
    mx, my = (x + x2) / 2 - math.sin(a) * dob * 0.3, (y + y2) / 2 + math.cos(a) * dob * 0.3
    pts = catmull(np.float32([(x, y), (mx, my), (x2, y2)]), 5)
    g.trazo(pts, w, w1=w * 0.62, afilado=0.0 if prof < maxp else 0.8, var=0.1)
    if tallado and prof <= 1 and w > 6:
        off = np.float32((-math.sin(a), math.cos(a))) * w * 0.18
        g.trazo(pts[: int(len(pts) * 0.8)] + off, max(1.0, w * 0.10), color=g.fondo_papel, op=0.55, afilado=1.0)
    if prof >= maxp:
        return
    nh = 2 + (1 if rnd(sem, prof * 5 + 3) > 0.55 else 0)
    for j in range(nh):
        da = (j - (nh - 1) / 2) * (0.55 + 0.25 * rnd(sem + j, prof)) + (rnd(sem + j, prof + 9) - 0.5) * 0.3
        _rama(g, x2, y2, a + da, L * (0.62 + 0.18 * rnd(sem + j, prof + 2)), w * 0.6, prof + 1, t, sem * 3 + j + 1, maxp,
              tallado)


def arbol_seco(g, x, y, s, t, sem=0, prof=5, ang=-90.0, tallado=True):
    """Árbol muerto de silueta (tinta sólida) con ramas que se mecen y brillo tallado en el tronco."""
    with g.grupo(x, y, s):
        g.macizo([(-26, 4), (26, 4), (12, -10), (-12, -10)])
        _rama(g, 0, 0, math.radians(ang), 150, 30, 0, t, sem, prof, tallado)


def craneo(g, x, y, r, t, ang=0.0, mand=0.0, tono=0.0, tono2=0.42, ojos=0.0, op=1.0):
    """Calavera de frente: cráneo con trama de volumen, cuencas de tinta, nariz, dientes y mandíbula que se abre (`mand`
    0..1). `ojos` > 0 = brasas pálidas en las cuencas."""
    def T(p):
        return tr(np.float32(p), x, y, r, ang)
    cr = catmull(np.float32([(0, -1.05), (0.62, -0.92), (0.92, -0.45), (0.88, 0.02), (0.72, 0.32), (0.62, 0.56),
                             (0.40, 0.62), (0.30, 0.78), (-0.30, 0.78), (-0.40, 0.62), (-0.62, 0.56), (-0.72, 0.32),
                             (-0.88, 0.02), (-0.92, -0.45), (-0.62, -0.92)]), 5, cerrado=True)
    m = clamp(mand)
    jaw = np.float32([(-0.60, 0.48), (-0.56, 0.86), (-0.34, 1.12), (0.34, 1.12), (0.56, 0.86), (0.60, 0.48), (0.44, 0.62),
                      (0.32, 0.86), (-0.32, 0.86), (-0.44, 0.62)]) + np.float32((0, 0.28 * m))
    if m > 0.02:
        g.macizo(T([(-0.34, 0.74), (0.34, 0.74), (0.34, 0.92 + 0.28 * m), (-0.34, 0.92 + 0.28 * m)]), op)
    g.figura(T(catmull(jaw, 4, cerrado=True)), tono, contorno=max(1.4, r * 0.05), op=op, tono2=tono2, luz=0,
             ang=60, per=4.5, modo="contorno", borde=0.2, rb=r * 0.1)
    g.figura(T(cr), tono, contorno=max(1.6, r * 0.06), op=op, tono2=tono2, luz=40, ang=55, per=4.8, modo="contorno",
             borde=0.25, rb=r * 0.14)
    for sx in (-1, 1):
        g.macizo(T(circ_pts(sx * 0.36, 0.10, 0.25, 24, 0.21)), op)
        g.trama(T(circ_pts(sx * 0.70, -0.05, 0.16, 16, 0.26)), 0.55, ang=80, per=4.0, cruz=False, op=op)
        if ojos > 0:
            g.circ(*T([(sx * 0.36, 0.12)])[0], r * 0.06, g.fondo_papel, op * ojos)
        g.trazo(T([(sx * 0.62, 0.40), (sx * 0.42, 0.40), (sx * 0.24, 0.30)]), max(1.0, r * 0.03), op=0.8 * op)
    g.macizo(T([(0, 0.27), (0.11, 0.50), (0, 0.56), (-0.11, 0.50)]), op)
    for dz in (0.0, 0.28 * m):
        yy0, yy1 = (0.66, 0.80) if dz == 0 else (0.86 + dz, 0.98 + dz)
        g.figura(T([(-0.30, yy0), (0.30, yy0), (0.30, yy1), (-0.30, yy1)]), 0.0, contorno=max(1.0, r * 0.03), op=op)
        for i in range(1, 6):
            xx = -0.30 + 0.6 * i / 6
            g.trazo(T([(xx, yy0), (xx, yy1)]), max(0.9, r * 0.025), op=op, afilado=0.0)
    g.trazo(T([(-0.05, -1.02), (0.02, -0.85), (-0.04, -0.7), (0.03, -0.55)]), max(0.8, r * 0.02), op=0.7 * op)


# ------------------------------------------------------------------ danza macabra
def _piezas_hueso(a, b, r):
    a, b = np.float32(a), np.float32(b)
    d = b - a
    L = float(np.hypot(*d)) + 1e-6
    nrm = np.float32((-d[1], d[0])) / L
    piezas = [capsula(a, b, r * 0.55)]
    for c in (a, b):
        for sg in (-1, 1):
            piezas.append(circ_pts(*(c + nrm * sg * r * 0.42), r * 0.62, 16))
    return piezas, d, nrm


def huesos(g, lista, op=1.0, tono=0.0, w=None):
    """Huesos unidos [(a, b, r), ...] (brazo, pierna): PRIMERO la tinta inflada de todos, LUEGO el papel y la trama; así las
    articulaciones salen limpias, sin manchas negras."""
    datos = [(r, *_piezas_hueso(a, b, r)) for a, b, r in lista]
    for r, piezas, _, _ in datos:
        ww = w if w is not None else max(1.6, r * 0.30)
        for pz in piezas:
            g.macizo(inflar(pz, ww), op)
    for r, piezas, d, nrm in datos:
        for pz in piezas:
            g.papel(pz, op)
        g.trama(piezas[0], tono, tono2=tono + 0.45, luz=math.degrees(math.atan2(nrm[1], nrm[0])),
                ang=math.degrees(math.atan2(d[1], d[0])), per=4.2, modo="contorno", borde=0.3, rb=r * 0.35, op=op)


def _hueso(g, a, b, r, op=1.0, tono=0.0, w=None):
    """Hueso largo suelto: diáfisis con trama a lo largo y dos cabezas (epífisis)."""
    huesos(g, [(a, b, r)], op, tono, w)


def pose_danza(t, fase=0.0, vel=1.0, brio=1.0):
    """Ciclo de baile de la danza macabra (brazos al aire, una pierna que se levanta). Ángulos en radianes."""
    a = t * 6.2832 * 0.55 * vel + fase
    sa, s2 = math.sin(a), math.sin(2 * a)
    return dict(tr=0.13 * sa * brio, cab=0.22 * math.sin(a + 1.2) * brio, hi=1.7 + 0.7 * sa * brio,
                ci=0.5 + 0.6 * s2 * brio, hd=0.6 + 1.0 * math.sin(a + math.pi) * brio, cd=0.9 + 0.5 * math.sin(2 * a + 1) * brio,
                pi=0.18 + 0.32 * max(0.0, sa) * brio, ri=-0.05 - 0.55 * max(0.0, sa) * brio,
                pd=0.12 + 0.3 * max(0.0, -sa) * brio, rd=-0.05 - 0.5 * max(0.0, -sa) * brio,
                salto=10 * abs(sa) * brio, mand=0.25 + 0.35 * max(0.0, math.sin(3 * a)))


POSE_QUIETO = dict(tr=0.0, cab=0.0, hi=0.12, ci=0.05, hd=0.12, cd=0.05, pi=0.06, ri=0.0, pd=0.06, rd=0.0, salto=0.0, mand=0.0)


def esqueleto(g, x, y, s, pose, t, op=1.0, tono=0.10, ojos=0.0, suelo=True):
    """Esqueleto de frente (danza macabra), ~400 de alto con s=1. (x, y) = punto del suelo bajo los pies; con `suelo=True`
    el pie más bajo toca y (nada flota) salvo `pose['salto']`. Pose: tr (torso), cab, hi/ci y hd/cd (hombro/codo izq./der.,
    0 = colgando), pi/ri y pd/rd (cadera/rodilla), salto, mand (mandíbula)."""
    p = dict(POSE_QUIETO)
    p.update(pose)
    jx = (rnd(g.k, 61) - 0.5) * 0.8                    # hervor de la figura entera
    rot = lambda v, a: (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))  # noqa: E731
    add = lambda a, b: (a[0] + b[0], a[1] + b[1])  # noqa: E731
    Pv = (0.0, 0.0)
    N = add(Pv, rot((0, -128), p["tr"]))
    Hd = add(N, rot((0, -44), p["tr"] + p["cab"]))
    j = {}
    for lado, sg, kh, kc in (("i", -1, "hi", "ci"), ("d", 1, "hd", "cd")):
        sh = add(N, rot((sg * 44, 10), p["tr"]))
        e = add(sh, rot((sg * 70 * math.sin(p[kh]), 70 * math.cos(p[kh])), p["tr"]))
        a2 = p[kh] + p[kc]
        dv = rot((sg * math.sin(a2), math.cos(a2)), p["tr"])
        w_ = add(e, (64 * dv[0], 64 * dv[1]))
        j["sh" + lado], j["e" + lado], j["w" + lado], j["a" + lado] = sh, e, w_, dv
    for lado, sg, kp, kr in (("i", -1, "pi", "ri"), ("d", 1, "pd", "rd")):
        hp = add(Pv, rot((sg * 22, 8), p["tr"] * 0.3))
        kn = add(hp, (sg * 94 * math.sin(p[kp]), 94 * math.cos(p[kp])))
        a2 = p[kp] + p[kr] * -1
        an = add(kn, (sg * 92 * math.sin(a2), 92 * math.cos(a2)))
        j["h" + lado], j["k" + lado], j["n" + lado] = hp, kn, an
    pie = max(j["ni"][1], j["nd"][1]) + 10
    oy = (-pie if suelo else 0.0) - p["salto"]
    with g.grupo(x + jx * s, y + oy * s, s):
        def brazo(l, sg):
            wx, wy = j["w" + l]
            dirx, diry = j["a" + l]
            for f in range(4):                                      # dedos ANTES: la muñeca los tapa limpia
                fa = math.atan2(diry, dirx) + (f - 1.5) * 0.28
                tip = (wx + 26 * math.cos(fa), wy + 26 * math.sin(fa))
                g.trazo([(wx, wy), tip], 6.5, color=TINTA, op=op, afilado=0.3, temblor=0.3)
                g.trazo([(wx, wy), tip], 3.0, color=g.fondo_papel, op=op, afilado=0.6, temblor=0.3)
            huesos(g, [(j["sh" + l], j["e" + l], 13), (j["e" + l], j["w" + l], 11)], op, tono)

        def pierna(l, sg):
            ax, ay = j["n" + l]
            g.figura([(ax - 8, ay - 6), (ax + sg * 34, ay + 4), (ax + sg * 36, ay + 12), (ax - 6, ay + 10)], 0.15,
                     contorno=2.0, op=op, ang=0, per=4.0, cruz=False)
            huesos(g, [(j["h" + l], j["k" + l], 15), (j["k" + l], j["n" + l], 13)], op, tono)
        brazo("i", -1)
        pierna("i", -1)
        # columna lumbar y pelvis
        for i in range(6):
            u = i / 5
            c = (lerp(N[0], Pv[0], 0.62 + 0.38 * u), lerp(N[1], Pv[1], 0.62 + 0.38 * u) - 6)
            g.figura(circ_pts(c[0], c[1], 7.5, 14, 6), 0.1, contorno=2.0, op=op, ang=0, per=4.0, cruz=False)
        pel = tr(np.float32([(-42, -16), (-32, -32), (-12, -24), (0, -14), (12, -24), (32, -32), (42, -16), (36, 6),
                             (16, 20), (6, 24), (-6, 24), (-16, 20), (-36, 6)]), Pv[0], Pv[1], 1.0, p["tr"] * 0.3)
        g.figura(catmull(pel, 4, cerrado=True), tono, tono2=0.5, luz=90, contorno=2.4, op=op, ang=30, per=4.2,
                 modo="contorno", borde=0.3, rb=6)
        for sg in (-1, 1):
            g.macizo(tr(circ_pts(sg * 16, 10, 7, 16, 6), Pv[0], Pv[1], 1.0, p["tr"] * 0.3), op)
        # caja torácica
        with g.grupo(N[0], N[1], 1.0):
            a = p["tr"]
            for i in range(6):
                yy = 14 + i * 12.5
                for sg in (-1, 1):
                    ancho = 40 - abs(i - 2) * 2.2
                    rib = [(sg * 5, yy), (sg * ancho * 0.75, yy - 4), (sg * ancho, yy + 9), (sg * ancho * 0.8, yy + 20),
                           (sg * 9, yy + 16)]
                    rib = tr(catmull(np.float32(rib), 5), 0, 0, 1.0, a)
                    g.trazo(rib, 8.0, color=TINTA, op=op, afilado=0.2, temblor=0.4)
                    g.trazo(rib, 4.2, color=g.fondo_papel, op=op, afilado=0.5, temblor=0.4)
            g.figura(capsula(*tr(np.float32([(0, 12), (0, 70)]), 0, 0, 1, a), 5.5), 0.1, contorno=2.0, op=op,
                     ang=0, per=4.0, cruz=False)
            for sg in (-1, 1):
                cl = tr(np.float32([(sg * 4, 6), (sg * 24, 2), (sg * 44, 10)]), 0, 0, 1, a)
                g.trazo(cl, 7.5, op=op, afilado=0.2)
                g.trazo(cl, 3.5, color=g.fondo_papel, op=op, afilado=0.5)
        # cuello
        g.trazo([N, Hd], 9, op=op, afilado=0.0)
        g.trazo([N, Hd], 4, color=g.fondo_papel, op=op, afilado=0.0)
        brazo("d", 1)
        pierna("d", 1)
        craneo(g, Hd[0], Hd[1] - 4, 31, t, p["tr"] + p["cab"], p["mand"], ojos=ojos, op=op)


def esqueleto_baila(g, x, y, s, t, fase=0.0, vel=1.0, brio=1.0, op=1.0, tono=0.10, ojos=0.0, poses=16):
    """esqueleto(g, x, y, s, pose_danza(t, fase, vel, brio), t, ...) ESTAMPADO (`sprite`): el ciclo de baile se cuantiza a
    `poses` dibujos y todos los bailarines comparten los sprites (la fase solo elige el dibujo). Lo grande, en vivo."""
    if not CACHE or 430 * s * g.s > 640:
        return esqueleto(g, x, y, s, pose_danza(t, fase, vel, brio), t, op, tono, ojos)
    i, h = fase_cuant(t * 6.2832 * 0.55 * vel + fase, poses)
    pose = pose_danza(0.0, h, vel, brio)
    sprite(g, ("esqueleto", i, poses, round(brio, 2), round(op, 2), round(tono, 2), round(ojos, 2)), x, y, s,
           lambda c, ax, ay, s_: esqueleto(c, ax, ay, s_, pose, t, op, tono, ojos), (-260, -560, 260, 40))


# ------------------------------------------------------------------ espectros y alas
def fantasma(g, x, y, s, t, fase=0.0, op=1.0, dirx=1, tono=0.05, estela=True, color_estela=None):
    """Alma en pena: sudario con capucha, brazo que se estira, cola que ondea; trama que sigue el contorno (se ve hueco),
    rostro de tinta con dos brasas y jirones de estela. ~240 de alto con s=1; flota (sube y baja)."""
    y = y + 8 * s * math.sin(t * 1.6 + fase)
    w = [9 * math.sin(t * 2.3 + fase + i * 0.9) for i in range(7)]
    br = 5 * math.sin(t * 1.9 + fase)

    def T(p):
        return tr(np.float32(p), x, y, s, 0.0, dirx)
    # brazo de atrás (más oscuro), cuerpo, brazo de delante: los dos brazos tendidos al frente, a la altura del pecho
    lejos = [(30, -70), (70, -50 + br), (92, -34 + br), (94, -24 + br), (76, -28 + br), (40, -48)]
    g.figura(T(catmull(np.float32(lejos), 4, cerrado=True)), 0.45, contorno=2.0, op=op, ang=20, per=4.6, cruz=False)
    loc = [(0, -158), (30, -150), (46, -126), (46, -98), (40, -82), (46, -40), (40, 4), (30, 46), (10, 86 + w[1]),
           (-22, 112 + w[2]), (-62, 126 + w[3]), (-108, 112 + w[4]), (-80, 96 + w[5]), (-52, 72 + w[6]), (-44, 24),
           (-48, -32), (-50, -86), (-44, -128), (-26, -152)]
    pol = T(catmull(np.float32(loc), 5, cerrado=True))
    g.figura(pol, tono, contorno=2.4, op=op, ang=70, per=5.5, modo="contorno", borde=0.45, rb=24, cruz=True)
    cerca = [(16, -80), (60, -52 + br), (86, -36 + br), (96, -24 + br), (80, -18 + br), (58, -30 + br), (20, -50)]
    g.figura(T(catmull(np.float32(cerca), 4, cerrado=True)), 0.12, contorno=2.0, op=op, ang=20, per=4.6, borde=0.3, rb=8)
    for f in range(3):                                         # dedos huesudos que cuelgan
        fx = 86 + f * 5
        g.trazo(T([(fx, -22 + br), (fx + 3, -4 + br + 3 * math.sin(t * 3 + f))]), 1.8, op=op, afilado=0.8)
    # capucha: hueco negro con dos brasas
    g.macizo(T(catmull(np.float32([(4, -138), (28, -134), (36, -112), (30, -92), (12, -88), (-2, -104)]), 4, cerrado=True)), op)
    for ex in (14, 27):
        g.circ(*T([(ex, -114)])[0], 2.6 * s, g.fondo_papel, op * (0.7 + 0.3 * math.sin(t * 5 + ex)))
    for i, pl in enumerate(([(-6, -80), (-10, -20), (-4, 40), (-22, 90)], [(22, -30), (16, 20), (8, 64)],
                            [(-30, -70), (-32, 0), (-44, 64), (-70, 104)])):
        g.trazo(T(catmull(np.float32(pl), 5)), 1.6, op=0.8 * op, sem=i + 3)
    if estela:
        col = color_estela or TINTA
        for i in range(3):
            xs = np.linspace(-100, -180 - 30 * i, 8)
            ys = 112 + i * 9 + 10 * np.sin(xs * 0.05 + t * 2.4 + i + fase)
            g.trazo(T(np.stack([xs, ys], 1)), 2.2 - 0.4 * i, color=col, op=0.6 * op, afilado=1.0)


def _pluma(g, base, ang, L, ancho, tono, op, k):
    ca, sa = math.cos(ang), math.sin(ang)
    nx, ny = -sa, ca
    loc = [(0, -0.35), (0.25, -0.5), (0.6, -0.48), (0.92, -0.22), (1.0, 0.0), (0.9, 0.22), (0.55, 0.5), (0.2, 0.48),
           (0, 0.3)]
    pts = np.float32([(base[0] + ca * L * u + nx * ancho * v, base[1] + sa * L * u + ny * ancho * v) for u, v in loc])
    pts = catmull(pts, 4, cerrado=True)
    g.figura(pts, tono, contorno=1.6, op=op, tono2=tono + 0.4, luz=math.degrees(ang), ang=math.degrees(ang) + 35, per=4.2,
             cruz=False)
    g.trazo([base, (base[0] + ca * L * 0.88, base[1] + sa * L * 0.88)], 1.5, op=op, afilado=0.6, temblor=0.3)


def ala(g, x, y, s, t, lado=1, apertura=1.0, tono=0.10, op=1.0, n=20):
    """Ala de plumas grabada (ángel, cuervo grande): borde de ataque, remeras largas en abanico, dos filas de coberteras.
    (x, y) = hombro; lado 1 = hacia la derecha. Respira (`apertura` + oscilación)."""
    ap = apertura + 0.04 * math.sin(t * 1.1)
    k = g.k
    borde = np.float32([(0, 0), (70, -70 * ap - 10), (150, -118 * ap - 10), (240, -150 * ap), (318, -150 * ap + 6)])
    E = catmull(borde, 8)
    R, ss, L = _remuestrear(E, 4.0)
    with g.grupo(x, y, s):
        def punto(u):
            return R[min(len(R) - 1, int(u * (len(R) - 1)))]

        def a_(deg):
            return math.radians(deg if lado > 0 else 180 - deg)

        def P_(p):
            return (p[0] * lado, p[1])
        for i in reversed(range(n)):
            u = i / (n - 1)
            b = P_(punto(0.06 + 0.94 * u))
            deg = lerp(96, 18, u ** 0.9) + 3 * math.sin(t * 2.0 + i * 0.4)
            Lf = lerp(130, 238, u ** 0.8)
            _pluma(g, b, a_(deg), Lf, lerp(24, 30, u), tono + 0.10 * (1 - u), op, k)
        for fila, (Lc, nc, dt) in enumerate(((92, 15, 0.06), (52, 13, 0.0))):
            for i in reversed(range(nc)):
                u = i / (nc - 1)
                b = P_(punto(0.02 + 0.92 * u))
                deg = lerp(100, 30, u) + 2 * math.sin(t * 2.0 + i * 0.6 + fila)
                _pluma(g, b, a_(deg), Lc * lerp(1.0, 0.8, u), 18 - 4 * fila, tono + dt, op, k)
        g.trazo(np.float32([P_(p) for p in E]), 5.0, op=op, afilado=0.4)


def llama(g, x, y, s, t, sem=0, op=1.0, color=ORO, acento=0.75):
    """Llama de vela/antorcha: papel con lenguas de tinta, parpadea; mancha de color en la plancha de acento."""
    f = [math.sin(t * (8 + i) + sem * 1.7 + i) for i in range(4)]
    loc = [(0, 0), (12, -8), (16, -24), (10 + 3 * f[0], -42), (4 + 4 * f[1], -66 - 6 * f[2]), (-2, -44), (-8 + 3 * f[3], -52),
           (-14, -28), (-12, -8)]
    pts = tr(catmull(np.float32(loc), 4, cerrado=True), x, y, s)
    g.figura(pts, 0.0, contorno=1.8, op=op)
    g.trazo(tr(np.float32([(-2, -6), (3, -20), (1 + 2 * f[1], -38)]), x, y, s), 1.4, op=0.8 * op)
    if acento:
        g.acento(pts, color, acento * op, aspero=0.5, sem=sem)


def cuervo(g, x, y, s, t, fase=0.0, dirx=1, op=1.0):
    """Cuervo en vuelo: silueta de tinta, alas que baten, brillo tallado en las plumas."""
    b = math.sin(t * 7.5 + fase)
    with g.grupo(x, y, s):
        for sg in (-1, 1):
            tip = (sg * 64, -30 * b - 8)
            mid = (sg * 30, -14 * b - 4)
            ala_ = [(sg * 6, -4), mid, tip, (sg * 50, -18 * b + 6), (sg * 40, -10 * b + 10), (sg * 26, -4 * b + 8),
                    (sg * 8, 6)]
            g.macizo(np.float32(ala_), op)
            g.trazo([(sg * 10, -1), mid, (sg * 48, -22 * b)], 1.0, color=g.fondo_papel, op=0.45 * op, afilado=1)
        g.macizo(circ_pts(0, 0, 13, 20, 7), op)
        g.macizo(circ_pts(dirx * 14, -3, 6.5, 14), op)
        g.macizo([(dirx * 19, -5), (dirx * 29, -2), (dirx * 19, 0)], op)
        g.macizo([(-dirx * 10, -2), (-dirx * 24, 4), (-dirx * 22, 8), (-dirx * 9, 5)], op)


# ------------------------------------------------------------------ cartelas, marcos, rótulos
def cartela(g, x, y, ancho, texto, t, px=46, fnt="gotica", alto=None, op=1.0, color=TINTA, ondea=1.0):
    """Filacteria (cinta con texto) de las láminas antiguas: banda que ondea, pliegues y colas cortadas en V."""
    alto = alto or px * 1.45
    hw, hh = ancho / 2, alto / 2
    o = [ondea * 5 * math.sin(t * 1.3 + i) for i in range(4)]
    for sg in (-1, 1):
        ex = x + sg * hw
        cola = [(ex - sg * 10, y - hh + 14 + o[0]), (ex + sg * 70, y - hh + 22 + o[1]), (ex + sg * 52, y + 4 + o[2]),
                (ex + sg * 74, y + hh + 16 + o[3]), (ex - sg * 10, y + hh + 10 + o[3])]
        g.figura(np.float32(cola), 0.55, contorno=2.0, op=op, ang=60 * sg, per=4.5, cruz=False)
        g.figura(np.float32([(ex - sg * 2, y - hh + o[0]), (ex - sg * 2, y + hh + o[3]), (ex - sg * 14, y + hh + 12 + o[3]),
                             (ex - sg * 14, y - hh + 14 + o[0])]), 0.85, contorno=1.6, op=op, ang=0, per=4.0, cruz=False)
    xs = np.linspace(x - hw, x + hw, 16)
    top = np.stack([xs, y - hh + 4 * np.sin((xs - x) / ancho * 3.0 + t * 1.3) * ondea], 1)
    bot = np.stack([xs[::-1], y + hh + 4 * np.sin((xs[::-1] - x) / ancho * 3.0 + t * 1.3) * ondea], 1)
    banda = np.vstack([top, bot])
    g.figura(banda, lambda X, Y: np.clip((np.abs(X - x) / hw - 0.72) / 0.28, 0, 1) * 0.5, contorno=2.4, op=op, ang=80,
             per=4.5, cruz=False)
    if texto:
        g.texto(texto, x, y + px * 0.04, px, color, fnt, op)


def marco(g, x0, y0, x1, y1, t, banda=22, esquinas=True, op=1.0, tono=0.6):
    """Marco de lámina: filete grueso, banda tramada, filete fino y medallones de calavera en las esquinas."""
    ext = [(x0 - banda, y0 - banda), (x1 + banda, y0 - banda), (x1 + banda, y1 + banda), (x0 - banda, y1 + banda)]
    hueco = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    # banda: cuatro tiras (para no tapar el hueco)
    tiras = [[ext[0], ext[1], (x1, y0), (x0, y0)], [ext[1], ext[2], (x1, y1), (x1, y0)],
             [ext[2], ext[3], (x0, y1), (x1, y1)], [ext[3], ext[0], (x0, y0), (x0, y1)]]
    for i, tira in enumerate(tiras):
        g.papel(tira, op)
        g.trama(tira, tono, ang=45 if i % 2 == 0 else -45, per=4.5, cruz=False, op=op)
    g.trazo(ext, 4.5, cerrado=True, op=op, afilado=0.0)
    g.trazo(hueco, 2.0, cerrado=True, op=op, afilado=0.0)
    ins = banda * 0.45
    g.trazo([(x0 - ins, y0 - ins), (x1 + ins, y0 - ins), (x1 + ins, y1 + ins), (x0 - ins, y1 + ins)], 1.3, cerrado=True,
            color=g.fondo_papel, op=0.8 * op, afilado=0.0)
    if esquinas:
        for (cx, cy) in ((x0 - banda / 2, y0 - banda / 2), (x1 + banda / 2, y0 - banda / 2), (x1 + banda / 2, y1 + banda / 2),
                         (x0 - banda / 2, y1 + banda / 2)):
            g.figura(circ_pts(cx, cy, banda * 1.35, 30), 0.0, contorno=2.6, op=op)
            g.trazo(circ_pts(cx, cy, banda * 1.1, 30), 1.2, cerrado=True, op=op * 0.8)
            craneo(g, cx, cy - banda * 0.12, banda * 0.66, t, 0.0, 0.0, tono=0.1, op=op)


def rotulo(g, txt, x, y, px, t, t0, t1=None, fnt="gotica", color=TINTA, anchor="mm", sombra=0.0, esp=0.0):
    """Rótulo de énfasis que se ESTAMPA (entra grande y se asienta, como un sello) y se desvanece en `t1`."""
    if t < t0 or (t1 is not None and t > t1 + 0.4):
        return
    k = pop(t, t0, 0.28)
    sc = lerp(1.22, 1.0, min(1.0, k)) if k < 1 else k
    opa = pr(t, t0, t0 + 0.07) * (1 - (pr(t, t1, t1 + 0.4) if t1 is not None else 0))
    with g.pivote(x, y, sc):
        g.texto(txt, x, y, px, color, fnt, opa, anchor, esp, sombra)


def salpicadura(g, x, y, r, sem=0, color=None, op=1.0, gotas=14, crece=1.0):
    """Mancha con gotas (tinta, o sangre/peste si `color`: va a la plancha de color)."""
    if crece <= 0.01:
        return
    rr = r * crece
    a = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    rad = np.ones_like(a)
    for i, f in enumerate((2, 3, 5, 7, 11, 13)):
        rad += (0.20 if f < 5 else 0.09) * rnd(sem, 90 + i) * np.sin(f * a + rnd(sem, 97 + i) * 6.2832)
    el, rot = 0.65 + 0.5 * rnd(sem, 99), rnd(sem, 98) * 3.1416
    px_, py_ = rr * rad * np.cos(a), rr * rad * np.sin(a) * el
    pts = np.stack([x + px_ * math.cos(rot) - py_ * math.sin(rot), y + px_ * math.sin(rot) + py_ * math.cos(rot)], 1)
    piezas = [pts]
    for i in range(int(2 + 3 * rnd(sem, 88))):                  # regueros: chorros que se afinan con una gota al final
        an = rnd(i, sem + 60) * 6.2832
        L = rr * (1.4 + 1.8 * rnd(i, sem + 61))
        ca, sa = math.cos(an), math.sin(an)
        w0 = rr * (0.22 + 0.15 * rnd(i, sem + 62))
        piezas.append(np.float32([(x - sa * w0, y + ca * w0), (x + ca * L, y + sa * L), (x + sa * w0, y - ca * w0)]))
        piezas.append(circ_pts(x + ca * L, y + sa * L, rr * 0.11, 12))
    for i in range(gotas):
        an = rnd(i, sem + 70) * 6.2832
        d = rr * (1.2 + 1.8 * rnd(i, sem + 71))
        rg = rr * (0.04 + 0.12 * rnd(i, sem + 72) ** 1.5)
        piezas.append(tr(circ_pts(0, 0, 1.0, 12, 0.6 + 0.4 * rnd(i, sem + 73)), x + d * math.cos(an), y + d * math.sin(an), rg,
                         an))
    for pz in piezas:
        if color is None:
            g.macizo(pz, op)
        else:
            g.acento(pz, color, op, aspero=0.0)


# ------------------------------------------------------------------ recuerdos: video real pasado a tinta
_NIVELES = {}


def _niveles(nombre):
    """Niveles fijos por clip (percentiles de 6 cuadros repartidos): el brillo no bombea cuadro a cuadro."""
    if nombre not in _NIVELES:
        Clip.cuadro(nombre, 0.0)
        c = Clip._abiertos[nombre]
        vals = []
        for idx in np.linspace(0, c.n - 1, 6).astype(int):
            c.cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
            ok, f = c.cap.read()
            if ok:
                vals.append(cv2.cvtColor(cv2.resize(f, (320, 180)), cv2.COLOR_BGR2GRAY).ravel())
        c.pos, c.ult = -2, None
        v = np.concatenate(vals).astype(np.float32) / 255.0 if vals else np.float32([0, 1])
        _NIVELES[nombre] = (float(np.percentile(v, 2)), float(np.percentile(v, 99)))
    return _NIVELES[nombre]


@functools.lru_cache(maxsize=2)
def _ruido_borde(sem):
    rng = np.random.default_rng(500 + sem)
    peq = rng.random((70, 120)).astype(np.float32)
    peq = cv2.GaussianBlur(peq, (0, 0), 1.6)
    return (peq - peq.min()) / (np.ptp(peq) + 1e-6)


def grabar_imagen(rgb, w, h, lo=0.0, hi=1.0, tinta=1.0, per=4.6, ang=30.0, k=0, gamma=0.9, contornos=0.8):
    """Imagen real (uint8 RGB) -> estampa w x h (float32 RGB): duotono sepia (`tinta` = 0) a grabado de líneas con contornos
    de buril (`tinta` = 1). `tinta` puede ser un mapa h x w (más grabado hacia los bordes, por ejemplo)."""
    ih, iw = rgb.shape[:2]
    kz = max(w / iw, h / ih)
    nw, nh = int(math.ceil(iw * kz)), int(math.ceil(ih * kz))
    im = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA if kz < 1 else cv2.INTER_LINEAR)
    ox, oy = (nw - w) // 2, (nh - h) // 2
    im = im[oy:oy + h, ox:ox + w]
    gr = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    lum = np.clip((gr - lo) / max(hi - lo, 1e-3), 0, 1) ** gamma
    if kz > 1.3:                                               # fuente vieja de baja resolución: realce antes de grabar
        lum = np.clip(lum + 0.9 * (lum - cv2.GaussianBlur(lum, (0, 0), 1.2 * kz)), 0, 1)
    peq = cv2.resize(lum, (max(8, w // 2), max(8, h // 2)), interpolation=cv2.INTER_AREA)
    peq = cv2.bilateralFilter(peq, 5, 0.10, 3)
    n = 5.0                                                    # regiones tonales nítidas, como en una lámina
    q = np.floor(peq * n) / n
    f = peq * n - np.floor(peq * n)
    q = q + np.clip((f - 0.7) / 0.3, 0, 1) ** 2 / n
    peq = 0.45 * peq + 0.55 * q
    lis = cv2.resize(peq, (w, h), interpolation=cv2.INTER_LINEAR)
    duo = np.float32(TINTA) + (np.float32(PAPEL) - np.float32(TINTA)) * lis[..., None]
    gx, gy = _rejilla(w, h)
    cov = tramado(1.0 - lis * 1.08, gx, gy, 1.0, ang, per, "lineal", True, k)
    sx = cv2.Sobel(peq, cv2.CV_32F, 1, 0, ksize=3)
    sy = cv2.Sobel(peq, cv2.CV_32F, 0, 1, ksize=3)
    e = cv2.resize(np.clip((np.sqrt(sx * sx + sy * sy) - 0.12) * 3.0, 0, 1), (w, h), interpolation=cv2.INTER_LINEAR)
    cov = np.maximum(cov, e * contornos)
    gra = np.float32(PAPEL) * (1 - cov[..., None]) + np.float32(TINTA) * cov[..., None]
    ti = np.asarray(tinta, np.float32)
    if ti.ndim == 2:
        ti = ti[..., None]
    return duo * (1 - ti) + gra * ti


def recuerdo(g, nombre, seg, x0, y0, x1, y1, t, tinta=0.35, come=1.0, banda=22, texto=None, px=40, sem=0, op=1.0,
             z=1.0, cx=0.5, cy=0.5, tono_marco=0.6):
    """Un RECUERDO: extracto real (clips/<nombre>.mp4, segundo `seg`) dentro de un marco grabado, pasado a tinta (duotono
    sepia al centro, grabado de líneas hacia los bordes) y con la tinta COMIÉNDOSE los bordes (mancha viva, `come` 0..1).
    `z`, `cx`, `cy`: encuadre dentro del clip (zoom y centro en fracciones). `texto`: cartela encima del marco."""
    a = g._t([(x0, y0), (x1, y1)])
    sx0, sy0, sx1, sy1 = int(round(a[0, 0])), int(round(a[0, 1])), int(round(a[1, 0])), int(round(a[1, 1]))
    bx0, by0, bx1, by1 = max(0, sx0), max(0, sy0), min(g.W, sx1), min(g.H, sy1)
    if bx1 - bx0 < 8 or by1 - by0 < 8 or op <= 0.004:
        return
    w, h = sx1 - sx0, sy1 - sy0
    rgb = Clip.cuadro(nombre, seg)
    if z > 1.0001:
        ih, iw = rgb.shape[:2]
        cw, ch = iw / z, ih / z
        ccx = clamp(cx * iw, cw / 2, iw - cw / 2)
        ccy = clamp(cy * ih, ch / 2, ih - ch / 2)
        rgb = rgb[int(ccy - ch / 2):int(ccy + ch / 2), int(ccx - cw / 2):int(ccx + cw / 2)]
    lo, hi = _niveles(nombre)
    gx, gy = _rejilla(w, h)
    db = np.minimum(np.minimum(gx, w - 1 - gx), np.minimum(gy, h - 1 - gy))
    nb = cv2.resize(_ruido_borde(sem), (w, h), interpolation=cv2.INTER_LINEAR)
    nb2 = np.roll(nb, int(t * 9) % max(w, 1), axis=1) * 0.5 + np.roll(nb, int(t * 5) % max(h, 1), axis=0) * 0.5
    mapa = np.clip(tinta + (1 - tinta) * (1 - np.clip(db / (0.22 * min(w, h)), 0, 1)) ** 1.3, 0, 1)
    est = grabar_imagen(rgb, w, h, lo, hi, mapa, per=4.6, ang=30, k=g.k)
    lim = come * (0.05 * min(w, h)) * (0.35 + 1.3 * nb2)
    tin = np.clip((lim - db) / 3.0 + 0.5, 0, 1)[..., None]
    est = est * (1 - tin) + np.float32(TINTA) * tin
    ex0, ey0 = bx0 - sx0, by0 - sy0
    reg = g.im[by0:by1, bx0:bx1]
    sub = est[ey0:ey0 + (by1 - by0), ex0:ex0 + (bx1 - bx0)]
    reg *= 1 - op
    reg += sub * op
    acr = g.ac[by0:by1, bx0:bx1]
    acr += (1 - acr) * op
    if g.alfa is not None:
        ar = g.alfa[by0:by1, bx0:bx1]
        ar += (1 - ar) * op
    marco(g, x0, y0, x1, y1, t, banda=banda, op=op, tono=tono_marco)
    if texto:
        cartela(g, (x0 + x1) / 2, y0 - banda - px * 0.2, min(x1 - x0, ancho_texto(texto, px, "gotica") + 140), texto, t,
                px=px, op=op)


# ------------------------------------------------------------------ chat del juego (se corrompe)
_GLIFOS = "†‡§¶#%&*~"


def chat(g, x, y, lineas, t, corr=0.0, ancho=760, px=26, op=1.0, sem=0, color_canal=SANGRE, vel=45.0):
    """Ventana de chat grabada: pergamino con filete, líneas que se escriben solas (`(canal, autor, texto, t_aparece)`)
    y CORRUPCIÓN (`corr` 0..1): letras que se vuelven glifos y gotas de tinta que escurren."""
    vis = [ln for ln in lineas if t >= ln[3]]
    if not vis:
        return
    paso = px * 1.42
    alto = paso * len(vis) + px * 1.2
    caja = [(x, y - alto), (x + ancho, y - alto), (x + ancho, y), (x, y)]
    g.figura(np.float32(caja), 0.16, contorno=2.6, op=op, ang=0, per=5.0, cruz=False)
    g.trazo(np.float32([(x + 7, y - alto + 7), (x + ancho - 7, y - alto + 7), (x + ancho - 7, y - 7), (x + 7, y - 7)]), 1.2,
            cerrado=True, op=0.7 * op, afilado=0.0)
    for i, (canal, autor, texto, t0) in enumerate(vis):
        yy = y - alto + px * 0.95 + paso * (i + 0.5)
        tag = f"[{canal}] "
        quien = f"{autor}: " if autor else ""
        cuerpo = texto[:int(max(0.0, t - t0) * vel)]
        if corr > 0:
            cuerpo = "".join(_GLIFOS[int(rnd(j + 13 * i, sem + g.k % 3) * len(_GLIFOS))]
                             if (c != " " and rnd(j + 7 * i, sem) < corr * 0.55) else c for j, c in enumerate(cuerpo))
        xt = x + 22
        g.texto(tag, xt, yy, px, color_canal, "gara_b", op, "lm")
        xt += ancho_texto(tag, px, "gara_b")
        if quien:
            g.texto(quien, xt, yy, px, TINTA, "gara_b", op, "lm")
            xt += ancho_texto(quien, px, "gara_b")
        g.texto(cuerpo, xt, yy, px, TINTA, "gara_i", op, "lm")
        if corr > 0.05:
            wtx = ancho_texto(cuerpo, px, "gara_i") if cuerpo else 0
            for d in range(int(2 + 6 * corr)):
                if rnd(d + 5 * i, sem + 90) < corr:
                    gx_ = xt + rnd(d + 5 * i, sem + 91) * max(wtx, 10)
                    L = px * (0.4 + 2.2 * corr * rnd(d + 5 * i, sem + 92)) * (0.85 + 0.15 * math.sin(t * 2 + d))
                    g.trazo([(gx_, yy + px * 0.25), (gx_ + 1, yy + px * 0.25 + L)], 2.6, op=op, afilado=0.3, w1=1.6)
                    g.circ(gx_ + 1, yy + px * 0.25 + L, 2.8, TINTA, op)
