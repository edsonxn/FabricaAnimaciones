# -*- coding: utf-8 -*-
"""Motor isométrico para el estilo Kurzgesagt (dioramas de pueblos, fuertes, ciudades), sobre el Lienzo (polígonos planos, sin contornos).

Proyección isométrica de 30° (la de los dioramas de Kurzgesagt):  sx = (x - y) * cos30,  sy = (x + y) * sin30 - z   (unidades de mundo = px a zoom 1).
  +x baja a la derecha, +y baja a la izquierda, +z sube. La cámara `Iso(cx, cy, cz, z)` pone el punto de mundo (cx, cy, cz) en el centro de la pantalla.
Luz desde la izquierda: la cara +y (inferior izquierda) es la iluminada, la +x (inferior derecha) la sombreada, la de arriba la más clara.
Todo se dibuja por «mundo» ordenado por profundidad (algoritmo del pintor): `Mundo.add(x0, y0, x1, y1, h, fn)`; `Mundo.dibujar(lz, iso)`.
"""
import math

import cv2
import numpy as np

from motor import W, H, circulo, elipse, rect_red, catmull, h01
import plano as P

C30 = math.cos(math.radians(30.0))
S30 = 0.5

# luz global de la escena (se cambia con luz(...)): multiplicador RGB y mezcla hacia un color (p. ej. violeta de noche)
_LUZ = dict(mul=(1.0, 1.0, 1.0), mix=None, k=0.0)


def luz(mul=(1.0, 1.0, 1.0), mix=None, k=0.0):
    _LUZ.update(mul=mul, mix=mix, k=k)


def tint(c):
    """Color de la escena bajo la luz actual."""
    m, mx, k = _LUZ["mul"], _LUZ["mix"], _LUZ["k"]
    c = tuple(min(255, int(v * mm)) for v, mm in zip(c[:3], m))
    if mx is not None and k > 0:
        c = tuple(int(v + (w - v) * k) for v, w in zip(c, mx))
    return c


def tonos(c):
    """(arriba, izquierda iluminada, derecha en sombra) de un color base."""
    return (P.aclarar(c, 0.16), tuple(c[:3]), P.oscurecer(c, 0.30))


class Iso:
    """Cámara isométrica. z = px por unidad de mundo."""

    def __init__(self, cx=0.0, cy=0.0, cz=0.0, z=1.0, sx0=W / 2, sy0=H / 2):
        self.cx, self.cy, self.cz, self.z, self.sx0, self.sy0 = cx, cy, cz, z, sx0, sy0
        self._ox = (cx - cy) * C30
        self._oy = (cx + cy) * S30 - cz

    def P(self, x, y, z=0.0):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        z = np.asarray(z, float)
        return self.sx0 + ((x - y) * C30 - self._ox) * self.z, self.sy0 + ((x + y) * S30 - z - self._oy) * self.z

    def pts(self, p3):
        a = np.asarray(p3, float)
        sx, sy = self.P(a[:, 0], a[:, 1], a[:, 2])
        return np.stack([sx, sy], 1)

    def visible(self, x0, y0, x1, y1, h=0.0, margen=140.0):
        """¿Su caja de mundo toca la pantalla?"""
        c = np.array([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0), (x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)], float)
        s = self.pts(c)
        return not (s[:, 0].max() < -margen or s[:, 0].min() > W + margen or s[:, 1].max() < -margen or s[:, 1].min() > H + margen)

    def inv_suelo(self, sx, sy):
        """Punto del suelo (z=0) bajo el píxel (sx, sy)."""
        u = ((sx - self.sx0) / self.z + self._ox) / C30          # = x - y
        v = ((sy - self.sy0) / self.z + self._oy) / S30          # = x + y
        return (u + v) / 2, (v - u) / 2


# ------------------------------------------------------------------------------------------------ suelo
def suelo(lz, iso, pts_xy, color, z=0.0, alfa=1.0):
    a = np.asarray(pts_xy, float)
    lz.relleno(iso.pts(np.column_stack([a[:, 0], a[:, 1], np.full(len(a), z)])), tint(color), alfa=alfa)


def suelo_rect(lz, iso, x, y, w, d, color, z=0.0, alfa=1.0):
    suelo(lz, iso, [(x, y), (x + w, y), (x + w, y + d), (x, y + d)], color, z, alfa)


def suelo_curvo(lz, iso, pts_xy, color, z=0.0, alfa=1.0, n=10):
    """Polígono de suelo con bordes suaves (Catmull-Rom cerrado)."""
    q = np.array(catmull(np.asarray(pts_xy, float), n, True), float)
    suelo(lz, iso, q, color, z, alfa)


def camino(lz, iso, pts_xy, ancho, color, borde=None, z=0.0, alfa=1.0, n=10):
    """Camino de ancho constante a lo largo de una polilínea (suavizada), con borde más oscuro opcional."""
    p = np.array(catmull(np.asarray(pts_xy, float), n, False), float) if len(pts_xy) > 2 else np.asarray(pts_xy, float)
    d = np.gradient(p, axis=0)
    d /= np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-6)[:, None]
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    for w, col in (((ancho + 6) if borde else None, borde), (ancho, color)):
        if w is None:
            continue
        a, b = p + nrm * w / 2, p - nrm * w / 2
        suelo(lz, iso, np.vstack([a, b[::-1]]), col, z, alfa)


def cuadricula(lz, iso, x0, y0, x1, y1, paso, color=(255, 255, 255), alfa=0.08, ancho=1.2, z=0.0):
    """Líneas de la rejilla isométrica (baldosas) muy tenues sobre el suelo."""
    sx0, sy0 = iso.P(x0, y0)
    for gx in np.arange(x0, x1 + 1e-6, paso):
        lz.trazo(iso.pts([(gx, y0, z), (gx, y1, z)]), color, ancho, afinar=False, temblor=0.0, capa=None) if False else None
    # (se dibujan como polígonos finos para que respeten el alfa)
    g = []
    for gx in np.arange(x0, x1 + 1e-6, paso):
        g.append(iso.pts([(gx, y0, z), (gx, y1, z)]))
    for gy in np.arange(y0, y1 + 1e-6, paso):
        g.append(iso.pts([(x0, gy, z), (x1, gy, z)]))
    for seg in g:
        _linea(lz, seg, color, ancho * max(0.6, iso.z), alfa)


def _linea(lz, seg, color, ancho, alfa=1.0):
    (xa, ya), (xb, yb) = seg
    d = np.array([xb - xa, yb - ya])
    L = float(np.hypot(*d))
    if L < 1e-6:
        return
    n = np.array([-d[1], d[0]]) / L * ancho / 2
    lz.relleno(np.array([[xa, ya] + n, [xb, yb] + n, [xb, yb] - n, [xa, ya] - n]), color, alfa=alfa)


# ------------------------------------------------------------------------------------------------ sombras
def sombra_suelo(lz, iso, x, y, w, d, h, k=0.55, alfa=0.20, dx=1.0, dy=0.28):
    """Sombra proyectada sobre el suelo (cae hacia +x, la luz viene de la izquierda)."""
    L = h * k
    pts = [(x, y), (x + w, y), (x + w + L * dx, y + L * dy), (x + w + L * dx, y + d + L * dy), (x + w, y + d), (x, y + d), (x + L * dx, y + L * dy), (x + L * dx, y + d + L * dy)]
    q = iso.pts([(a, b, 0.0) for a, b in pts]).astype(np.float32)
    hull = cv2.convexHull(q).reshape(-1, 2)
    lz.relleno(hull, (30, 24, 70), alfa=alfa)


def sombra_elipse(lz, iso, x, y, rx, ry, alfa=0.22):
    th = np.linspace(0, 2 * math.pi, 18, endpoint=False)
    lz.relleno(iso.pts(np.column_stack([x + rx * np.cos(th), y + ry * np.sin(th), np.zeros(18)])), (30, 24, 70), alfa=alfa)


# ------------------------------------------------------------------------------------------------ cajas
class Caja:
    """Prisma rectangular alineado a los ejes: esquina (x, y) mínima, tamaño (w, d, h), base a altura z0."""

    def __init__(self, x, y, w, d, h, z0=0.0):
        self.x, self.y, self.w, self.d, self.h, self.z0 = x, y, w, d, h, z0

    def punto(self, cara, a, b):
        """Punto 3D de la cara 'y' (izquierda, plano y+d, a a lo largo de +x) o 'x' (derecha, plano x+w, a a lo largo de +y), b = altura sobre la base."""
        if cara == "y":
            return (self.x + a, self.y + self.d, self.z0 + b)
        if cara == "yi":                       # pared interior del fondo (plano y mínimo; a a lo largo de +x): se ve desde dentro
            return (self.x + a, self.y, self.z0 + b)
        if cara == "xi":                       # pared interior del fondo (plano x mínimo; a a lo largo de +y)
            return (self.x, self.y + a, self.z0 + b)
        return (self.x + self.w, self.y + a, self.z0 + b)

    def rect(self, cara, a0, a1, b0, b1):
        return [self.punto(cara, a0, b0), self.punto(cara, a1, b0), self.punto(cara, a1, b1), self.punto(cara, a0, b1)]


def caja(lz, iso, x, y, w, d, h, color, z0=0.0, t3=None, alfa=1.0):
    """Dibuja un prisma con 3 caras. Devuelve la Caja (para colocar ventanas, puertas y techos)."""
    c = Caja(x, y, w, d, h, z0)
    top, izq, der = t3 or tonos(color)
    X1, Y1, Z1 = x + w, y + d, z0 + h
    lz.relleno(iso.pts([(X1, y, z0), (X1, Y1, z0), (X1, Y1, Z1), (X1, y, Z1)]), tint(der), alfa=alfa)
    lz.relleno(iso.pts([(x, Y1, z0), (X1, Y1, z0), (X1, Y1, Z1), (x, Y1, Z1)]), tint(izq), alfa=alfa)
    lz.relleno(iso.pts([(x, y, Z1), (X1, y, Z1), (X1, Y1, Z1), (x, Y1, Z1)]), tint(top), alfa=alfa)
    return c


def cara_rect(lz, iso, c, cara, a0, a1, b0, b1, color, alfa=1.0, tono=True):
    """Rectángulo pegado a una cara de la caja (ventana, puerta, franja). Si tono, se oscurece en la cara derecha."""
    col = P.oscurecer(color, 0.22) if (tono and cara in ("x", "xi")) else color
    lz.relleno(iso.pts(c.rect(cara, a0, a1, b0, b1)), tint(col), alfa=alfa)


def cara_arco(lz, iso, c, cara, a0, a1, b0, b1, color, alfa=1.0, n=10):
    """Vano con arco de medio punto (puerta, ventana, portal) en una cara."""
    ra = (a1 - a0) / 2
    pts = [c.punto(cara, a0, b0), c.punto(cara, a1, b0)]
    for k in range(n + 1):
        th = math.pi * k / n
        pts.append(c.punto(cara, a0 + ra + ra * math.cos(th), b1 - ra + ra * math.sin(th) * 1.0))
    col = P.oscurecer(color, 0.22) if cara == "x" else color
    lz.relleno(iso.pts(pts), tint(col), alfa=alfa)


def hilera_ventanas(lz, iso, c, cara, n, b0, alto, ancho, margen_a=0.1, color=(86, 58, 96), marco=None, rejas=False, postigo=None):
    """n ventanas iguales repartidas a lo largo de la cara."""
    L = c.w if cara == "y" else c.d
    paso = (L * (1 - 2 * margen_a)) / n
    for i in range(n):
        a0 = L * margen_a + paso * i + (paso - ancho) / 2
        if marco is not None:
            cara_rect(lz, iso, c, cara, a0 - ancho * 0.12, a0 + ancho * 1.12, b0 - alto * 0.08, b0 + alto * 1.10, marco)
        cara_rect(lz, iso, c, cara, a0, a0 + ancho, b0, b0 + alto, color)
        if rejas:
            for k in range(1, 3):
                cara_rect(lz, iso, c, cara, a0 + ancho * k / 3 - ancho * 0.03, a0 + ancho * k / 3 + ancho * 0.03, b0, b0 + alto, P.aclarar(color, 0.35), tono=False)
        if postigo is not None:
            cara_rect(lz, iso, c, cara, a0 - ancho * 0.34, a0 - ancho * 0.12, b0, b0 + alto, postigo)
            cara_rect(lz, iso, c, cara, a0 + ancho * 1.12, a0 + ancho * 1.34, b0, b0 + alto, postigo)


# ------------------------------------------------------------------------------------------------ techos
def techo_dos_aguas(lz, iso, c, eje, hr, color, vuelo=4.0, gablete=None, tejas=True, grosor=2.2):
    """Techo a dos aguas sobre la caja c. eje = 'x' (cumbrera paralela a x) o 'y'. hr = altura de la cumbrera sobre el borde. gablete = color del hastial."""
    x, y, w, d, z = c.x - vuelo, c.y - vuelo, c.w + 2 * vuelo, c.d + 2 * vuelo, c.z0 + c.h
    claro, medio, oscuro = P.aclarar(color, 0.10), color, P.oscurecer(color, 0.28)
    if eje == "x":
        ym = y + d / 2
        R0, R1 = (x, ym, z + hr), (x + w, ym, z + hr)
        # faldón trasero (normal -y), hastial derecho, faldón delantero (normal +y)
        lz.relleno(iso.pts([(x, y, z), (x + w, y, z), R1, R0]), tint(oscuro))
        gb = gablete or (P.oscurecer(c_wall(c), 0.30) if False else (200, 190, 190))
        lz.relleno(iso.pts([(c.x + c.w, c.y, z), (c.x + c.w, c.y + c.d, z), (c.x + c.w, ym, z + hr * (c.d / d))]), tint(gb))
        lz.relleno(iso.pts([(x, y + d, z), (x + w, y + d, z), R1, R0]), tint(claro))
        # grosor del borde (fascia)
        lz.relleno(iso.pts([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z - grosor), (x, y + d, z - grosor)]), tint(oscuro))
        lz.relleno(iso.pts([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z - grosor), (x + w, y, z - grosor)]), tint(P.oscurecer(color, 0.45)))
        if tejas:
            for k in range(1, 5):
                f = k / 5
                q = iso.pts([(x, y + d - (d / 2) * f, z + hr * f), (x + w, y + d - (d / 2) * f, z + hr * f)])
                _linea(lz, q, tint(P.oscurecer(claro, 0.16)), max(1.0, 1.4 * iso.z), 0.55)
    else:
        xm = x + w / 2
        R0, R1 = (xm, y, z + hr), (xm, y + d, z + hr)
        lz.relleno(iso.pts([(x, y, z), (x, y + d, z), R1, R0]), tint(claro))
        gb = gablete or (200, 190, 190)
        lz.relleno(iso.pts([(c.x, c.y + c.d, z), (c.x + c.w, c.y + c.d, z), (xm, c.y + c.d, z + hr * (c.w / w))]), tint(gb))
        lz.relleno(iso.pts([(x + w, y, z), (x + w, y + d, z), R1, R0]), tint(oscuro))
        lz.relleno(iso.pts([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z - grosor), (x + w, y, z - grosor)]), tint(P.oscurecer(color, 0.45)))
        lz.relleno(iso.pts([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z - grosor), (x, y + d, z - grosor)]), tint(oscuro))
        if tejas:
            for k in range(1, 5):
                f = k / 5
                q = iso.pts([(x + w - (w / 2) * f, y, z + hr * f), (x + w - (w / 2) * f, y + d, z + hr * f)])
                _linea(lz, q, tint(P.oscurecer(oscuro, 0.10)), max(1.0, 1.4 * iso.z), 0.55)


def c_wall(c):
    return (230, 220, 210)


def techo_plano(lz, iso, c, color, borde=3.0, alto=2.5):
    """Azotea con pretil: aro bajo en el borde y fondo ligeramente más oscuro."""
    z = c.z0 + c.h
    caja(lz, iso, c.x, c.y, c.w, c.d, alto, color, z0=z)
    lz.relleno(iso.pts([(c.x + borde, c.y + borde, z + alto), (c.x + c.w - borde, c.y + borde, z + alto), (c.x + c.w - borde, c.y + c.d - borde, z + alto),
                        (c.x + borde, c.y + c.d - borde, z + alto)]), tint(P.oscurecer(color, 0.18)))


def techo_piramide(lz, iso, c, h, color, vuelo=2.0):
    """Techo piramidal (torres, kioscos)."""
    x, y, w, d, z = c.x - vuelo, c.y - vuelo, c.w + 2 * vuelo, c.d + 2 * vuelo, c.z0 + c.h
    apex = (x + w / 2, y + d / 2, z + h)
    lz.relleno(iso.pts([(x + w, y, z), (x + w, y + d, z), apex]), tint(P.oscurecer(color, 0.30)))
    lz.relleno(iso.pts([(x, y + d, z), (x + w, y + d, z), apex]), tint(color))


def cilindro(lz, iso, x, y, r, h, color, z0=0.0, tapa=True, n=20, t3=None):
    """Cilindro vertical de radio r (en unidades de mundo): franjas iluminada / media / sombreada."""
    top, izq, der = t3 or tonos(color)
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    # elipse de la base y de la tapa
    def aro(z):
        return iso.pts(np.column_stack([x + r * np.cos(th), y + r * np.sin(th), np.full(n, z)]))
    b, t = aro(z0), aro(z0 + h)
    cx, cy = iso.P(x, y, z0)
    ax = r * C30 * math.sqrt(2) * iso.z
    lz.relleno(b, tint(der))
    # cuerpo: rectángulo entre tangentes verticales
    cyt = iso.P(x, y, z0 + h)[1]
    lz.relleno(np.array([[cx - ax, cy], [cx + ax, cy], [cx + ax, cyt], [cx - ax, cyt]]), tint(izq))
    lz.relleno(np.array([[cx + ax * 0.15, cy], [cx + ax, cy], [cx + ax, cyt], [cx + ax * 0.15, cyt]]), tint(der))
    lz.relleno(np.array([[cx - ax * 0.62, cy], [cx - ax * 0.30, cy], [cx - ax * 0.30, cyt], [cx - ax * 0.62, cyt]]), tint(P.aclarar(izq, 0.10)))
    if tapa:
        lz.relleno(t, tint(top))


def cono(lz, iso, x, y, r, h, color, z0=0.0, n=18):
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    b = iso.pts(np.column_stack([x + r * np.cos(th), y + r * np.sin(th), np.full(n, z0)]))
    cx, cy = iso.P(x, y, z0)
    ax = r * C30 * math.sqrt(2) * iso.z
    ay = iso.P(x, y, z0 + h)[1]
    lz.relleno(b, tint(P.oscurecer(color, 0.30)))
    lz.relleno(np.array([[cx - ax, cy], [cx + ax, cy], [cx, ay]]), tint(P.oscurecer(color, 0.30)))
    lz.relleno(np.array([[cx - ax, cy], [cx + ax * 0.1, cy], [cx, ay]]), tint(color))


def cupula(lz, iso, x, y, r, color, z0=0.0, n=24, linterna=True):
    """Cúpula semiesférica con degradado por franjas."""
    cx, cy = iso.P(x, y, z0)
    ax = r * C30 * math.sqrt(2) * iso.z
    ay = r * 1.15 * iso.z
    th = np.linspace(math.pi, 2 * math.pi, n)
    cont = np.column_stack([cx + ax * np.cos(th), cy + ax * np.sin(th) * (ay / ax)])
    lz.relleno(cont, tint(P.oscurecer(color, 0.28)))
    for f, col in ((0.74, color), (0.46, P.aclarar(color, 0.10))):
        lz.relleno(np.column_stack([cx - ax * 0.15 + (ax * f) * np.cos(th) * 0.95, cy + ax * f * np.sin(th) * (ay / ax)]), tint(col))
    if linterna:
        lz.relleno(circulo(cx, cy - ay - 3 * iso.z, 3.2 * iso.z, 10), tint(P.aclarar(color, 0.5)))


def cruz(lz, iso, x, y, z, s=1.0, color=(250, 244, 230)):
    sx, sy = iso.P(x, y, z)
    k = iso.z * s
    lz.relleno(rect_red(sx - 1.6 * k, sy - 14 * k, 3.2 * k, 14 * k, 1), tint(color))
    lz.relleno(rect_red(sx - 5.5 * k, sy - 10.5 * k, 11 * k, 3.0 * k, 1), tint(color))


# ------------------------------------------------------------------------------------------------ mundo (orden por profundidad)
class Mundo:
    """Lista de objetos con su huella en el mundo; se dibujan de atrás hacia delante. `fijos` persisten; `dinamicos` se vacían cada cuadro."""

    def __init__(self):
        self.fijos = []
        self.dinamicos = []

    def add(self, x0, y0, x1, y1, h, fn, fijo=True, clave=None):
        k = (x0 + x1) / 2 + (y0 + y1) / 2 if clave is None else clave
        (self.fijos if fijo else self.dinamicos).append((k, x0, y0, x1, y1, h, fn))

    def nuevo_cuadro(self):
        self.dinamicos = []

    topo = False                     # True: orden por geometría (ver _orden_topologico) en vez de solo por la clave del centro

    def dibujar(self, lz, iso):
        todo = [o for o in self.fijos + self.dinamicos if iso.visible(o[1], o[2], o[3], o[4], o[5])]
        todo = _orden_topologico(todo, iso) if self.topo else sorted(todo, key=lambda o: o[0])
        for k, x0, y0, x1, y1, h, fn in todo:
            fn(lz, iso)


def _orden_topologico(objs, iso, eps=0.5, pad=12.0):
    """Orden de dibujo de atrás hacia delante por GEOMETRÍA: i va antes que j si su caja queda enteramente a menor x o a menor y (y las proyecciones en pantalla se tocan).
    Corrige lo que la clave del centro no puede (casas largas con gente delante, barcos junto a muelles, árboles grandes). Entre cajas sin relación manda la clave."""
    import heapq
    n = len(objs)
    if n < 2:
        return objs
    a = np.array([(o[1], o[2], o[3], o[4], o[5]) for o in objs], float)
    x0, y0, x1, y1, h = a.T
    key = np.array([o[0] for o in objs], float)
    zs = np.stack([np.zeros(n), h], 1)
    sx = np.empty((n, 2, 4)); sy = np.empty((n, 2, 4))
    for zi in range(2):
        for ci, (cx, cy) in enumerate(((x0, y0), (x1, y0), (x1, y1), (x0, y1))):
            px, py = iso.P(cx, cy, zs[:, zi])
            sx[:, zi, ci], sy[:, zi, ci] = px, py
    bx0, bx1 = sx.min((1, 2)) - pad, sx.max((1, 2)) + pad
    by0, by1 = sy.min((1, 2)) - pad, sy.max((1, 2)) + pad
    solapa = (bx0[:, None] < bx1[None, :]) & (bx1[:, None] > bx0[None, :]) & (by0[:, None] < by1[None, :]) & (by1[:, None] > by0[None, :])
    sepx = x1[:, None] <= x0[None, :] + eps                       # i está a menor x que j
    sepy = y1[:, None] <= y0[None, :] + eps
    atras = (sepx | sepy) & ~(sepx.T | sepy.T) & solapa           # i detrás de j (y no lo contrario)
    np.fill_diagonal(atras, False)
    indeg = atras.sum(0)
    suc = [np.nonzero(atras[i])[0] for i in range(n)]
    hp = [(key[i], i) for i in range(n) if indeg[i] == 0]
    heapq.heapify(hp)
    hecho = np.zeros(n, bool)
    sal = []
    while len(sal) < n:
        if not hp:                                                   # ciclo: se rompe por la clave
            i = min((j for j in range(n) if not hecho[j]), key=lambda j: key[j])
            indeg[i] = 0
        else:
            _, i = heapq.heappop(hp)
            if hecho[i]:
                continue
        hecho[i] = True
        sal.append(objs[i])
        for j in suc[i]:
            indeg[j] -= 1
            if indeg[j] == 0 and not hecho[j]:
                heapq.heappush(hp, (key[j], j))
    return sal


# ------------------------------------------------------------------------------------------------ isla flotante y habitación en corte
def isla(lz, iso, x0, y0, x1, y1, color_top=(120, 188, 96), esp=34.0, c_tierra=(150, 100, 70), c_roca=(122, 104, 148), sombra=True, t=0.0, seed=0):
    """Losa de terreno flotante (diorama) con tierra y roca debajo y sombra lejana. Dibujar ANTES de los objetos del suelo y después del fondo."""
    if sombra:
        c = iso.P((x0 + x1) / 2 + 30, (y0 + y1) / 2 + 30, -esp - 80)
        lz.halo(c[0], c[1], max(x1 - x0, y1 - y0) * 0.95 * iso.z, (10, 8, 40), alfa=0.35, capa=0)
    bob = 2.2 * math.sin(t * 1.1 + seed)
    # cara derecha (x = x1) y cara izquierda (y = y1) con estratos
    for plano in ("x", "y"):
        L = (y1 - y0) if plano == "x" else (x1 - x0)
        for (za, zb, col) in ((0, -6, P.aclarar(color_top, -0.0)), (-6, -esp * 0.45, c_tierra), (-esp * 0.45, -esp, c_roca)):
            if plano == "x":
                pts = [(x1, y0, za), (x1, y1, za), (x1, y1, zb), (x1, y0, zb)]
            else:
                pts = [(x0, y1, za), (x1, y1, za), (x1, y1, zb), (x0, y1, zb)]
            c = tint(P.oscurecer(col, 0.30) if plano == "x" else col)
            lz.relleno(iso.pts([(a, b, z + bob) for a, b, z in pts]), c)
        # estalactitas de roca
        n = max(3, int(L / 26))
        for i in range(n):
            u = (i + 0.5) / n
            lo = esp * (0.5 + 0.9 * h01(seed + (1 if plano == "x" else 2), i))
            w_ = (L / n) * 0.5
            if plano == "x":
                a = [(x1, y0 + u * L - w_, -esp), (x1, y0 + u * L + w_, -esp), (x1, y0 + u * L, -lo)]
            else:
                a = [(x0 + u * L - w_, y1, -esp), (x0 + u * L + w_, y1, -esp), (x0 + u * L, y1, -lo)]
            lz.relleno(iso.pts([(p, q, r + bob) for p, q, r in a]), tint(P.oscurecer(c_roca, 0.30) if plano == "x" else c_roca))
    lz.relleno(iso.pts([(x0, y0, bob), (x1, y0, bob), (x1, y1, bob), (x0, y1, bob)]), tint(color_top))


def habitacion(lz, iso, x, y, w, d, h, piso=(176, 120, 86), pared_a=(250, 232, 196), pared_b=None, friso=(150, 100, 80), espesor=4.0):
    """Habitación en corte (casa de muñecas): suelo y dos paredes de fondo (planos x e y mínimos) vistas desde dentro. Devuelve la Caja para colocar ventanas y cuadros."""
    pared_b = pared_b or P.oscurecer(pared_a, 0.0)
    c = Caja(x, y, w, d, h, 0.0)
    # suelo con grosor
    caja(lz, iso, x - espesor, y - espesor, w + espesor, d + espesor, espesor, P.oscurecer(piso, 0.25), z0=-espesor)
    lz.relleno(iso.pts([(x, y, 0), (x + w, y, 0), (x + w, y + d, 0), (x, y + d, 0)]), tint(piso))
    # entablado
    n = int(d / 9)
    for i in range(1, n):
        lz.relleno(iso.pts([(x, y + i * d / n - 0.4, 0), (x + w, y + i * d / n - 0.4, 0), (x + w, y + i * d / n + 0.4, 0), (x, y + i * d / n + 0.4, 0)]), tint(P.oscurecer(piso, 0.16)), alfa=0.6)
    # paredes: plano y = y (cara 'yi', ilumina) y plano x = x (cara 'xi', sombra)
    lz.relleno(iso.pts(c.rect("yi", 0, w, 0, h)), tint(pared_a))
    lz.relleno(iso.pts(c.rect("xi", 0, d, 0, h)), tint(P.oscurecer(pared_b, 0.22)))
    # zócalo/friso y moldura superior
    for cara, L in (("yi", w), ("xi", d)):
        cara_rect(lz, iso, c, cara, 0, L, 0, 9, friso)
        cara_rect(lz, iso, c, cara, 0, L, h - 4, h, P.aclarar(pared_a, 0.2))
    # grosor del borde superior de las paredes
    lz.relleno(iso.pts([(x - espesor, y - espesor, h), (x + w, y - espesor, h), (x + w, y, h), (x - espesor, y, h)]), tint(P.aclarar(pared_a, 0.12)))
    lz.relleno(iso.pts([(x - espesor, y - espesor, h), (x, y - espesor, h), (x, y + d, h), (x - espesor, y + d, h)]), tint(P.aclarar(pared_a, 0.05)))
    lz.relleno(iso.pts([(x - espesor, y - espesor, 0), (x + w, y - espesor, 0), (x + w, y - espesor, h), (x - espesor, y - espesor, h)]), tint(P.oscurecer(pared_a, 0.35)), alfa=0.0)
    return c
