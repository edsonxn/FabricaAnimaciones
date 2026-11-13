# -*- coding: utf-8 -*-
"""Kit «LÍNEA 3D» (13-nov-2026): 3D de alambre en LÍNEAS BLANCAS SOBRE NEGRO, estética de transmisión de lanzamiento.
Todo se proyecta con una cámara en perspectiva real; nada es un dibujo plano. Monocromo (blanco y grises), brillo suave.

    from linea3d import Cam, L3, geo, globo, cuerpo_revolucion, ...
    cam = Cam(pos, mira, arriba)                 # unidades libres (el mundo de los cohetes va en km, centro de la Tierra = 0)
    lz = L3(cam)
    globo(lz, (0,0,0), R_T)                      # rejilla + costas reales + limbo, con cara oculta
    lz.linea(P, op=0.8, w=1.2)                   # polilínea 3D (N,3); op por vértice permitido; guion=k para trazos
    lz.texto("MECO", x, y, 28, "SemiBold Condensed", esp=0.12)
    img = lz.final(t)                            # float32 HxWx3 0..1 (brillo, viñeta, grano)

Piezas: `Cam` (perspectiva, recorte cercano), `L3` (lienzo 2x supermuestreo, niveles de opacidad, rellenos negros para
ocultar lo de atrás, texto Bahnschrift = letra tipo DIN), `globo` (rejilla lat/lon, costas mundiales unidas con shapely y
cacheadas, limbo exacto de la esfera), `cuerpo_revolucion` (silueta de un cuerpo de revolución vista desde la cámara + anillos
con mitad trasera tenue: el «plano técnico» de un cohete), `chorro` (pluma de partículas en trazos), `rejilla_suelo`,
`circulo3d`, `etiqueta3d` (rótulo con guía hacia un punto 3D), `curva_suave` (interpolación de tablas).
Ejemplo: videos/cohete_crs30/ · doc: docs/estilo_linea3d.md
"""
import functools
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from motor import H, W

SS = 2                                   # supermuestreo del lienzo
R_T = 6371.0                             # radio terrestre (km)
DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
FUENTE = "C:/Windows/Fonts/bahnschrift.ttf"
TINTE = np.array([0.95, 0.97, 1.0], np.float32)     # blanco apenas frío


# ------------------------------------------------------------------ utilidades
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def pr(t, a, b):
    return clamp((t - a) / max(b - a, 1e-9))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def e_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def e_inout(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def lerp(a, b, u):
    return a + (b - a) * u


def nrm(v):
    v = np.asarray(v, np.float64)
    return v / max(np.linalg.norm(v), 1e-12)


def rnd(i, k=0):
    x = math.sin(i * 127.1 + k * 311.7) * 43758.5453
    return x - math.floor(x)


def rot_eje(eje, ang):
    """Matriz de rotación de `ang` rad alrededor de `eje` (Rodrigues)."""
    k = nrm(eje)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K


def base_de(eje, ref=(0, 0, 1)):
    """Dos vectores perpendiculares a `eje` (para dibujar círculos)."""
    a = nrm(eje)
    r = np.asarray(ref, np.float64)
    if abs(a @ nrm(r)) > 0.95:
        r = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    u = nrm(np.cross(a, r))
    return u, np.cross(a, u)


def curva_suave(tabla, paso=0.5, suav=6):
    """Tabla [(x, y0, y1...)] -> función x -> (y0, y1...) con interpolación lineal densa + suavizado gaussiano."""
    tab = np.asarray(tabla, np.float64)
    xs = np.arange(tab[0, 0], tab[-1, 0] + paso, paso)
    ys = np.stack([np.interp(xs, tab[:, 0], tab[:, j]) for j in range(1, tab.shape[1])], 1)
    if suav > 0:
        k = np.exp(-0.5 * (np.arange(-3 * suav, 3 * suav + 1) / suav) ** 2)
        k /= k.sum()
        pad = np.pad(ys, ((3 * suav, 3 * suav), (0, 0)), mode="edge")
        ys = np.stack([np.convolve(pad[:, j], k, mode="valid") for j in range(ys.shape[1])], 1)

    def f(x):
        x = np.asarray(x, np.float64)
        return np.stack([np.interp(x, xs, ys[:, j]) for j in range(ys.shape[1])], -1)
    return f


# ------------------------------------------------------------------ geografía
def latlon_xyz(lat, lon, r=R_T):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([r * np.cos(la) * np.cos(lo), r * np.cos(la) * np.sin(lo), r * np.sin(la)], -1)


def enu(lat, lon):
    """Base local (este, norte, arriba) en un punto de la Tierra."""
    la, lo = math.radians(lat), math.radians(lon)
    e = np.array([-math.sin(lo), math.cos(lo), 0.0])
    n = np.array([-math.sin(la) * math.cos(lo), -math.sin(la) * math.sin(lo), math.cos(la)])
    u = np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)])
    return e, n, u


class Sitio:
    """Marco local en un punto: km este/norte/altura -> mundo (con la curvatura de la Tierra)."""

    def __init__(self, lat, lon):
        self.lat, self.lon = lat, lon
        self.E, self.N, self.U = enu(lat, lon)
        self.P = self.U * R_T

    def a_mundo(self, e, n, h=0.0):
        e, n, h = np.broadcast_arrays(np.asarray(e, np.float64), np.asarray(n, np.float64), np.asarray(h, np.float64))
        v = self.P + e[..., None] * self.E + n[..., None] * self.N
        return v / np.linalg.norm(v, axis=-1, keepdims=True) * (R_T + h[..., None])

    def latlon_a_en(self, lat, lon):
        """lat/lon -> (km este, km norte) en el plano local (aprox. válida a < 300 km)."""
        p = latlon_xyz(np.asarray(lat), np.asarray(lon)) - self.P
        return p @ self.E, p @ self.N

    def gran_circulo(self, azimut_deg, s_km, h_km):
        """Punto a `s_km` sobre el gran círculo que sale del sitio con ese azimut, a `h_km` de altura."""
        a = math.radians(azimut_deg)
        d = math.sin(a) * self.E + math.cos(a) * self.N
        s = np.asarray(s_km, np.float64)[..., None] / R_T
        h = np.asarray(h_km, np.float64)[..., None]
        return (np.cos(s) * self.U + np.sin(s) * d) * (R_T + h)


@functools.lru_cache(maxsize=2)
def costas_mundo(tol=0.08):
    """Costas del mundo (contornos de la tierra unida, shapely) como lista de arrays de vectores unitarios. Caché npz."""
    ruta = os.path.join(DATOS, f"costas_mundo_{tol}.npz")
    if not os.path.exists(ruta):
        from shapely.geometry import Polygon
        from shapely.ops import unary_union
        polys = []
        for v in json.load(open(os.path.join(DATOS, "paises.json"), encoding="utf-8")).values():
            for p in v:
                if len(p) >= 4:
                    g = Polygon(p).buffer(0)
                    if not g.is_empty:
                        polys.append(g)
        u = unary_union(polys).simplify(tol)
        anillos = []
        for g in getattr(u, "geoms", [u]):
            for r in [g.exterior] + list(g.interiors):
                c = np.asarray(r.coords)
                if len(c) >= 8:
                    anillos.append(c)
        np.savez_compressed(ruta, *anillos)
    z = np.load(ruta)
    return [latlon_xyz(z[k][:, 1], z[k][:, 0], 1.0) for k in z.files]


# ------------------------------------------------------------------ cámara
class Cam:
    def __init__(self, pos, mira, arriba=(0, 0, 1), fov=40.0, cerca=1e-4, centro=None):
        self.pos = np.asarray(pos, np.float64)
        self.cx, self.cy = centro if centro is not None else (W / 2, H / 2)
        f = nrm(np.asarray(mira, np.float64) - self.pos)
        r = nrm(np.cross(f, arriba))
        u = np.cross(r, f)
        self.R = np.stack([r, u, f])
        self.f = (H / 2) / math.tan(math.radians(fov) / 2)
        self.cerca = cerca
        self.dir = f

    def proy(self, P):
        """(N,3) -> x, y (px a 1x), z (profundidad). z <= cerca = detrás de la cámara."""
        Q = (np.asarray(P, np.float64) - self.pos) @ self.R.T
        z = Q[..., 2]
        zz = np.where(z > self.cerca, z, np.nan)
        x = self.cx + self.f * Q[..., 0] / zz
        y = self.cy - self.f * Q[..., 1] / zz
        return x, y, z

    def px(self, P):
        x, y, _ = self.proy(np.asarray(P, np.float64)[None])
        return float(x[0]), float(y[0])

    def escala(self, P):
        """Píxeles por unidad de mundo a la distancia de P."""
        _, _, z = self.proy(np.asarray(P, np.float64)[None])
        return self.f / max(float(z[0]), 1e-9)


def cam_orbita(centro, dist, az, el, arriba=(0, 0, 1), fov=40.0, base=None):
    """Cámara que mira `centro` desde (azimut, elevación) en grados, en la base local `base` = (e, n, u) o ejes del mundo."""
    e, n, u = base if base is not None else (np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0]))
    a, b = math.radians(az), math.radians(el)
    d = math.cos(b) * (math.sin(a) * e + math.cos(a) * n) + math.sin(b) * u
    return Cam(np.asarray(centro) + d * dist, centro, u if base is not None else arriba, fov, cerca=dist * 1e-4)


def cam_mezcla(c0, c1, u):
    """Interpola dos cámaras (posición, mira y fov) para transiciones de plano."""
    u = clamp(u)
    pos = c0.pos + (c1.pos - c0.pos) * u
    mira = pos + nrm(c0.dir + (c1.dir - c0.dir) * u)
    arr = nrm(c0.R[1] + (c1.R[1] - c0.R[1]) * u)
    fov0 = math.degrees(2 * math.atan((H / 2) / c0.f))
    fov1 = math.degrees(2 * math.atan((H / 2) / c1.f))
    return Cam(pos, mira, arr, lerp(fov0, fov1, u), cerca=min(c0.cerca, c1.cerca))


# ------------------------------------------------------------------ texto
@functools.lru_cache(maxsize=96)
def _fuente(peso, px):
    f = ImageFont.truetype(FUENTE, int(px))
    try:
        f.set_variation_by_name(peso)
    except Exception:
        pass
    return f


@functools.lru_cache(maxsize=512)
def _sprite(txt, px, peso, esp):
    f = _fuente(peso, px)
    sep = esp * px
    anchos = [f.getlength(c) for c in txt]
    ancho = int(sum(anchos) + sep * max(0, len(txt) - 1) + px * 0.4) + 2
    alto = int(px * 1.45)
    im = Image.new("L", (ancho, alto), 0)
    d = ImageDraw.Draw(im)
    x = px * 0.2
    for c, a in zip(txt, anchos):
        d.text((x, px * 0.18), c, fill=255, font=f)
        x += a + sep
    a = np.asarray(im)
    cols = np.where(a.max(0) > 0)[0]
    if len(cols):
        a = a[:, max(0, cols[0] - 1):cols[-1] + 2]
    return a


def ancho_texto(txt, px, peso="SemiBold Condensed", esp=0.0):
    return _sprite(txt, int(px * SS), peso, esp).shape[1] / SS


# ------------------------------------------------------------------ lienzo
class L3:
    NIVELES = 24

    def __init__(self, cam):
        self.cam = cam
        self.b = np.zeros((H * SS, W * SS), np.uint8)

    # -- 3D
    def _seg(self, P, op, guion=None, cerrada=False):
        x, y, z = self.cam.proy(P)
        if cerrada:
            x, y, z = np.append(x, x[:1]), np.append(y, y[:1]), np.append(z, z[:1])
            if np.ndim(op):
                op = np.append(op, op[:1])
        ok = np.isfinite(x) & np.isfinite(y) & (np.abs(x) < W * 6) & (np.abs(y) < H * 6)
        opv = np.broadcast_to(np.asarray(op, np.float64), x.shape)
        a = np.minimum(opv[:-1], opv[1:]) * (ok[:-1] & ok[1:])
        if guion:
            a = a * (((np.arange(len(a)) // guion) % 2) == 0)
        p = np.stack([x, y], -1)
        return p[:-1], p[1:], a

    def _dibujar_segs(self, p0, p1, a, w):
        if len(a) == 0:
            return
        lv = np.clip(np.round(a * self.NIVELES), 0, self.NIVELES).astype(int)
        th = max(1, int(round(w * SS)))
        S = SS * 16                                  # coordenadas en subpíxel (shift=4)
        q0 = np.round(np.clip(np.nan_to_num(p0), -2e4, 2e4) * S).astype(np.int32)
        q1 = np.round(np.clip(np.nan_to_num(p1), -2e4, 2e4) * S).astype(np.int32)
        for k in np.unique(lv):
            if k <= 0:
                continue
            m = lv == k
            segs = np.stack([q0[m], q1[m]], 1)
            cv2.polylines(self.b, list(segs), False, int(255 * k / self.NIVELES), th, cv2.LINE_AA, shift=4)

    def linea(self, P, op=1.0, w=1.0, guion=None, cerrada=False):
        P = np.asarray(P, np.float64)
        if len(P) < 2:
            return
        p0, p1, a = self._seg(P, op, guion, cerrada)
        self._dibujar_segs(p0, p1, a, w)

    def lineas(self, lista, op=1.0, w=1.0):
        """Varias polilíneas de un golpe (misma opacidad base; op puede ser lista de arrays por vértice)."""
        P0, P1, A = [], [], []
        for i, P in enumerate(lista):
            if len(P) < 2:
                continue
            o = op[i] if isinstance(op, (list, tuple)) else op
            p0, p1, a = self._seg(np.asarray(P, np.float64), o)
            P0.append(p0), P1.append(p1), A.append(a)
        if A:
            self._dibujar_segs(np.concatenate(P0), np.concatenate(P1), np.concatenate(A), w)

    def puntos(self, P, r=2.0, op=1.0):
        x, y, z = self.cam.proy(np.atleast_2d(P))
        opv = np.broadcast_to(np.asarray(op, np.float64), x.shape)
        for xi, yi, oi in zip(x, y, opv):
            if np.isfinite(xi) and oi > 0.01 and -50 < xi < W + 50 and -50 < yi < H + 50:
                cv2.circle(self.b, (int(xi * SS * 16), int(yi * SS * 16)), max(1, int(r * SS * 16)), int(255 * clamp(oi)),
                           -1, cv2.LINE_AA, shift=4)

    def relleno(self, P, val=0.0):
        """Rellena el polígono proyectado (por defecto NEGRO: tapa lo que hay detrás)."""
        x, y, z = self.cam.proy(np.asarray(P, np.float64))
        if not np.all(np.isfinite(x)):
            return
        pts = np.round(np.stack([x, y], -1) * SS * 16).astype(np.int32)
        cv2.fillPoly(self.b, [pts], int(255 * val), cv2.LINE_AA, shift=4)

    # -- 2D (coordenadas de pantalla a 1x)
    def l2(self, pts, op=1.0, w=1.0, cerrada=False):
        pts = np.round(np.asarray(pts, np.float64) * SS * 16).astype(np.int32)
        cv2.polylines(self.b, [pts], cerrada, int(255 * clamp(op)), max(1, int(round(w * SS))), cv2.LINE_AA, shift=4)

    def c2(self, x, y, r, op=1.0, w=1.0, lleno=False):
        cv2.circle(self.b, (int(x * SS * 16), int(y * SS * 16)), max(1, int(r * SS * 16)), int(255 * clamp(op)),
                   -1 if lleno else max(1, int(round(w * SS))), cv2.LINE_AA, shift=4)

    def r2(self, x0, y0, x1, y1, val=0.0):
        cv2.rectangle(self.b, (int(x0 * SS), int(y0 * SS)), (int(x1 * SS), int(y1 * SS)), int(255 * val), -1)

    def texto(self, txt, x, y, px, peso="SemiBold Condensed", op=1.0, anchor="lm", esp=0.0, fondo=False):
        if op <= 0.01 or not txt:
            return
        s = _sprite(txt, int(px * SS), peso, esp)
        h, w = s.shape
        X, Y = x * SS, y * SS
        X -= {"l": 0, "m": w / 2, "r": w}[anchor[0]]
        Y -= {"t": 0, "m": h / 2, "b": h}[anchor[1]]
        X, Y = int(round(X)), int(round(Y))
        x0, y0, x1, y1 = max(0, X), max(0, Y), min(self.b.shape[1], X + w), min(self.b.shape[0], Y + h)
        if x1 <= x0 or y1 <= y0:
            return
        sub = s[y0 - Y:y1 - Y, x0 - X:x1 - X].astype(np.float32) * clamp(op)
        dst = self.b[y0:y1, x0:x1]
        if fondo:                                     # recuadro negro detrás (legible sobre líneas)
            dst[:] = 0
        np.maximum(dst, sub.astype(np.uint8), out=dst)

    # -- acabado
    def final(self, t=0.0, brillo=1.0, grano=0.018):
        a = cv2.resize(self.b, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        p = cv2.resize(a, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        g = cv2.GaussianBlur(p, (0, 0), 2.2) * 0.55 + cv2.GaussianBlur(p, (0, 0), 9.0) * 0.45
        g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
        img = a + g * 0.9 * brillo
        img = 1.0 - np.exp(-img * 1.15)               # curva suave: el blanco puro no se quema
        img = img / (1.0 - math.exp(-1.15))
        img *= _vineta()
        if grano:
            rng = np.random.default_rng(int(t * 30) + 7)
            img += (rng.random((H // 2, W // 2), np.float32) - 0.5)[np.arange(H) // 2][:, np.arange(W) // 2] * grano
        img = np.clip(img, 0, 1)
        return img[..., None] * TINTE[None, None, :]


@functools.lru_cache(maxsize=1)
def _vineta():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return (1.0 - 0.28 * np.clip(d - 0.55, 0, 1) ** 1.6).astype(np.float32)


# ------------------------------------------------------------------ primitivas 3D
def circulo3d(c, eje, r, n=96, a0=0.0, a1=2 * math.pi, ref=(0, 0, 1)):
    u, v = base_de(eje, ref)
    a = np.linspace(a0, a1, n)
    return np.asarray(c)[None] + r * (np.cos(a)[:, None] * u[None] + np.sin(a)[:, None] * v[None])


def globo(lz, C, R, op=1.0, paso=15, costas=True, op_rej=0.22, op_costa=0.75, rellenar=True, w=1.0, limbo=0.9, tol=None):
    """Esfera de alambre con cara oculta: rejilla lat/lon, costas reales y limbo exacto."""
    C = np.asarray(C, np.float64)
    cam = lz.cam
    v = cam.pos - C
    d = np.linalg.norm(v)
    if d <= R * 1.0001:
        return
    vn = v / d
    hor = R / d                                    # coseno del ángulo del horizonte visto desde la cámara

    def vis(U):                                    # U: vectores unitarios (N,3)
        k = U @ vn
        return np.clip((k - hor) / 0.06, 0, 1) ** 1.2

    cl = C + vn * (R * hor)                        # círculo del limbo
    rl = R * math.sqrt(max(0.0, 1 - hor * hor))
    anillo = circulo3d(cl, vn, rl, 240)
    if rellenar:
        lz.relleno(anillo, 0.0)
    lineas, ops = [], []
    for lat in range(-90 + paso, 90, paso):
        U = latlon_xyz(np.full(181, lat), np.linspace(-180, 180, 181), 1.0)
        lineas.append(C + U * R), ops.append(vis(U) * op * op_rej)
    for lon in range(-180, 180, paso):
        U = latlon_xyz(np.linspace(-88, 88, 121), np.full(121, lon), 1.0)
        lineas.append(C + U * R), ops.append(vis(U) * op * op_rej)
    lz.lineas(lineas, ops, w=w * 0.8)
    if costas:
        if tol is None:                            # costa fina cuando la cámara está cerca
            tol = 0.01 if d - R < 3000 else 0.08
        cs = costas_mundo(tol)
        lz.lineas([C + U * R for U in cs], [vis(U) * op * op_costa for U in cs], w=w)
    if limbo:
        lz.linea(anillo, op * limbo, w=w * 1.4)


def cuerpo_revolucion(lz, base, eje, perfil, anillos=None, op=1.0, w=1.2, gen=8, rot=0.0, rellenar=True, op_atras=0.28,
                      ref=(0, 0, 1)):
    """Plano técnico de un cuerpo de revolución: perfil [(z, r), ...] a lo largo de `eje` desde `base`.
    Dibuja la SILUETA vista desde la cámara (dos generatrices), los anillos en z de `anillos` (mitad trasera tenue)
    y `gen` generatrices finas que giran con `rot` (dan volumen). Rellena de negro para tapar lo de atrás."""
    cam = lz.cam
    base = np.asarray(base, np.float64)
    a = nrm(eje)
    perfil = np.asarray(perfil, np.float64)
    u0, v0 = base_de(a, ref)
    izq, der = [], []
    for z, r in perfil:
        c = base + a * z
        vc = cam.pos - c
        vp = vc - a * (vc @ a)
        if np.linalg.norm(vp) < 1e-9:
            s = u0
        else:
            s = nrm(np.cross(a, vp))
        izq.append(c + s * r), der.append(c - s * r)
    izq, der = np.array(izq), np.array(der)
    if rellenar:
        lz.relleno(np.concatenate([izq, der[::-1]]), 0.0)
        for z, r in (perfil[0], perfil[-1]):          # tapas (elipses) también tapan
            if r > 0:
                lz.relleno(circulo3d(base + a * z, a, r, 48, ref=ref), 0.0)
    # anillos
    zs = anillos if anillos is not None else [z for z, r in perfil]
    for z in zs:
        r = float(np.interp(z, perfil[:, 0], perfil[:, 1]))
        if r <= 0:
            continue
        c = base + a * z
        P = circulo3d(c, a, r, 64, ref=ref)
        vc = nrm(cam.pos - c)
        fr = ((P - c) @ vc) > -1e-9
        opv = np.where(fr, op, op * op_atras)
        lz.linea(P, opv, w * 0.8, cerrada=True)
    # generatrices finas (solo cara visible)
    if gen:
        for k in range(gen):
            ang = rot + 2 * math.pi * k / gen
            d = math.cos(ang) * u0 + math.sin(ang) * v0
            P = np.array([base + a * z + d * r for z, r in perfil])
            frente = np.array([(cam.pos - p) @ d for p in P]) > 0
            lz.linea(P, np.where(frente, op * 0.22, 0.0), w * 0.7)
    lz.linea(izq, op, w)
    lz.linea(der, op, w)


def rejilla_suelo(lz, centro, e, n, tam, paso, op=0.25, w=0.8, desv=None):
    """Rejilla de suelo (plano e-n) que se desvanece hacia el borde."""
    c = np.asarray(centro, np.float64)
    k = np.arange(-tam, tam + 1e-9, paso)
    lineas, ops = [], []
    s = np.linspace(-tam, tam, 60)
    for x in k:
        P = c + x * e + s[:, None] * n
        lineas.append(P), ops.append(op * np.clip(1 - np.hypot(x, s) / tam, 0, 1) ** 1.5)
        P = c + s[:, None] * e + x * n
        lineas.append(P), ops.append(op * np.clip(1 - np.hypot(s, x) / tam, 0, 1) ** 1.5)
    lz.lineas(lineas, ops, w)


def chorro(lz, salida, dir_, largo, ancho, t, n=70, op=1.0, semilla=0, w=1.0, abre=1.6):
    """Pluma de motor en trazos: partículas que salen de `salida` en `dir_` y se abren (cono) y desvanecen."""
    salida = np.asarray(salida, np.float64)
    d = nrm(dir_)
    u, v = base_de(d)
    for i in range(n):
        f = (rnd(i, semilla) + t * (1.6 + 0.8 * rnd(i, semilla + 3))) % 1.0
        ang = rnd(i, semilla + 1) * 2 * math.pi
        rr = ancho * (0.25 + abre * f) * math.sqrt(rnd(i, semilla + 2))
        p = salida + d * (largo * f) + (math.cos(ang) * u + math.sin(ang) * v) * rr
        q = p + d * largo * (0.05 + 0.08 * rnd(i, semilla + 4))
        o = op * (1 - f) ** 1.3 * (0.5 + 0.5 * rnd(i, semilla + 5))
        lz.linea(np.array([p, q]), o, w)
    # núcleo
    lz.linea(np.array([salida, salida + d * largo * 0.35]), op * 0.9, w * 1.6)


def etiqueta3d(lz, P, txt, sub=None, dx=60, dy=-50, op=1.0, px=26, lado=None):
    """Rótulo con guía: punto en P, línea quebrada y texto (y subtexto) en pantalla."""
    if op <= 0.01:
        return None
    x, y = lz.cam.px(P)
    if not (np.isfinite(x) and -200 < x < W + 200):
        return None
    lado = lado or (1 if dx >= 0 else -1)
    x1, y1 = x + dx * 0.55, y + dy
    x2 = x1 + 40 * lado
    lz.c2(x, y, 4, op, lleno=True)
    lz.c2(x, y, 9, op * 0.6, w=1)
    lz.l2([(x, y), (x1, y1), (x2, y1)], op * 0.8, 1.0)
    an = "lb" if lado > 0 else "rb"
    lz.texto(txt, x2 + 8 * lado, y1 + px * 0.42, px, "SemiBold Condensed", op, an, esp=0.1)
    if sub:
        lz.texto(sub, x2 + 8 * lado, y1 + px * 0.42 + px * 0.95, int(px * 0.72), "Light Condensed", op * 0.85, an, esp=0.12)
    return x, y
