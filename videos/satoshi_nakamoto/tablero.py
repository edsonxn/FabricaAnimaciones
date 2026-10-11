# -*- coding: utf-8 -*-
"""TABLERO DE DETECTIVE VIVO (estilo documental de Edsonxn, 3-oct-2026).

Un corcho infinito visto por una cámara 3D que NUNCA se detiene (trayectoria Hermite por fotogramas clave + deriva de mano, látigos con
desenfoque de movimiento, inclinación de perspectiva). Sobre el corcho:
  - Pieza(...)   : láminas (polaroid, ficha, nota adhesiva, recorte, documento, foto real) que entran volando, caen con sombra, se clavan
                   con chincheta y pueden ser «portales»: una escena dibujada que vive DENTRO de la foto y llena la pantalla al entrar.
  - Hilo(...)    : lana tensada entre chinchetas (caída en catenaria, vaivén al tenderse, se puede CORTAR y las mitades caen colgando).
  - Flecha/Circulo/Tache (rotulador sobre el corcho o sobre un papel), Punteada (línea de datos con paquetes que viajan),
    Cinta (cinta adhesiva entre dos papeles), Cadena (bloques enlazados), Etiqueta colgada del hilo, Sello sobre papel.
  - Lupa (aumento real con distorsión), polvo/bokeh en primer plano, cuerdas desenfocadas cerca de la cámara (profundidad).
Coordenadas: mundo en «px de tablero» (zoom 1 = 1 px de pantalla); z = altura sobre el corcho (negativa = hacia la cámara).
Todo se registra en listas globales (PIEZAS, HILOS, MARCAS...) y `render_tablero(lz, t)` dibuja el cuadro.
"""
import functools
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import docu as D
from motor import H, W

AQUI = os.path.dirname(os.path.abspath(__file__))
TIPOS = dict(
    maquina=os.path.join(AQUI, "tipos", "SpecialElite-Regular.ttf"),
    courier=os.path.join(AQUI, "tipos", "CourierPrime-Regular.ttf"),
    courier_b=os.path.join(AQUI, "tipos", "CourierPrime-Bold.ttf"),
    marcador=os.path.join(AQUI, "tipos", "PermanentMarker-Regular.ttf"),
    mano=os.path.join(AQUI, "tipos", "Caveat[wght].ttf"),
    oswald=os.path.join(AQUI, "tipos", "Oswald[wght].ttf"),
)
F_FOCAL = 1500.0


@functools.lru_cache(maxsize=256)
def fnt(nombre, px):
    ruta = TIPOS.get(nombre) or D.FUENTES.get(nombre, nombre)
    return ImageFont.truetype(ruta, int(px))


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def sm(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def e_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def e_back(x, s=1.7):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def pr(t, a, b):
    return clamp((t - a) / max(b - a, 1e-6))


def lerp(a, b, u):
    return a + (b - a) * u


# =====================================================================================================================  CÁMARA
class Camara:
    """Fotogramas clave (t, x, y, z, rz, rx, ry, modo). z = zoom sobre el corcho; rz = giro en el plano; rx/ry = inclinación (grados).
    modo del tramo que EMPIEZA en esa clave: 'fluido' (Hermite, nunca se para), 'latigo' (barrido rápido con desenfoque), 'suave' (frena)."""

    def __init__(self):
        self.K = []

    def clave(self, t, x, y, z=1.0, rz=0.0, rx=0.0, ry=0.0, modo="fluido"):
        self.K.append(dict(t=float(t), v=np.array([x, y, math.log(z), rz, rx, ry], np.float64), modo=modo))
        self.K.sort(key=lambda k: k["t"])
        self._tan = None

    def _tangentes(self):
        K = self.K
        n = len(K)
        tg = []
        for i in range(n):
            parar = K[i]["modo"] in ("latigo", "suave") or (i > 0 and K[i - 1]["modo"] in ("latigo", "suave"))
            if parar or i == 0 or i == n - 1:
                tg.append(np.zeros(6))
            else:
                dt = K[i + 1]["t"] - K[i - 1]["t"]
                tg.append((K[i + 1]["v"] - K[i - 1]["v"]) / max(dt, 1e-6))
        self._tan = tg

    def base(self, t):
        """Pose interpolada sin deriva de mano: (x, y, z, rz, rx, ry)."""
        v = self._interp(t)
        return v[0], v[1], math.exp(v[2]), v[3], v[4], v[5]

    def estado(self, t):
        x, y, lz, rz, rx, ry = self._interp(t)
        return self._deriva(t, x, y, lz, rz, rx, ry)

    def _interp(self, t):
        K = self.K
        if self._tan is None:
            self._tangentes()
        if t <= K[0]["t"]:
            v = K[0]["v"].copy()
        elif t >= K[-1]["t"]:
            v = K[-1]["v"].copy()
        else:
            i = max(j for j in range(len(K)) if K[j]["t"] <= t)
            a, b = K[i], K[i + 1]
            dt = b["t"] - a["t"]
            u = (t - a["t"]) / dt
            if a["modo"] == "latigo":
                u = _quint(u)
                v = a["v"] + (b["v"] - a["v"]) * u
            else:
                h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
                v = h00 * a["v"] + h10 * dt * self._tan[i] + h01 * b["v"] + h11 * dt * self._tan[i + 1]
        return v

    def _deriva(self, t, x, y, lz, rz, rx, ry):
        z = math.exp(lz)
        # deriva de cámara en mano (siempre viva) + respiración de zoom
        x += (7.0 * math.sin(0.83 * t) + 3.0 * math.sin(2.1 * t + 1.3)) / z
        y += (5.0 * math.sin(0.61 * t + 2.0) + 2.5 * math.sin(1.7 * t)) / z
        rz += 0.25 * math.sin(0.37 * t + 0.5)
        rx += 0.6 * math.sin(0.29 * t + 1.1)
        ry += 0.8 * math.sin(0.23 * t + 2.3)
        z *= 1.0 + 0.012 * math.sin(0.45 * t)
        z *= SACUDIDA.zoom(t)
        sx, sy = SACUDIDA.desp(t)
        return x + sx / z, y + sy / z, z, rz, rx, ry


def _quint(u):
    u = clamp(u)
    return 16 * u ** 5 if u < 0.5 else 1 - (-2 * u + 2) ** 5 / 2


class _Sacudida:
    """Pequeños golpes de cámara cuando algo se clava o se sella."""

    def __init__(self):
        self.ev = []

    def add(self, t, amp=6.0):
        self.ev.append((t, amp))

    def desp(self, t):
        x = y = 0.0
        for t0, a in self.ev:
            e = t - t0
            if 0 <= e < 0.6:
                k = a * math.exp(-e * 9)
                x += k * math.sin(e * 55)
                y += k * math.cos(e * 47) * 0.7
        return x, y

    def zoom(self, t):
        z = 1.0
        for t0, a in self.ev:
            e = t - t0
            if 0 <= e < 0.5:
                z *= 1.0 + 0.004 * a * math.exp(-e * 10)
        return z


SACUDIDA = _Sacudida()
CAM = Camara()


class Vista:
    """Proyección de un instante: mundo (x, y, z) -> pantalla."""

    def __init__(self, t):
        x, y, z, rz, rx, ry = CAM.estado(t)
        self.t, self.z, self.cx, self.cy = t, z, x, y
        f = F_FOCAL
        Dd = f / z
        a, b, c = math.radians(rx), math.radians(ry), math.radians(rz)
        Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
        Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
        Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
        R = Rz @ Rx @ Ry                     # cámara -> mundo
        self.Rt = R.T
        self.C = np.array([x, y, 0.0]) + R @ np.array([0, 0, -Dd])
        self.K = np.array([[f, 0, W / 2], [0, f, H / 2], [0, 0, 1.0]])
        self.Dd = Dd

    def proy(self, P):
        """P: (N,3) -> (N,2) pantalla y profundidad (N,)."""
        P = np.asarray(P, np.float64).reshape(-1, 3)
        pc = (P - self.C) @ self.Rt.T
        zc = pc[:, 2]
        zs = np.maximum(zc, 1e-3)
        u = F_FOCAL * pc[:, 0] / zs + W / 2
        v = F_FOCAL * pc[:, 1] / zs + H / 2
        return np.stack([u, v], 1), zc

    def plano(self, z0=0.0):
        """Homografía plano z=z0 (x, y) -> pantalla."""
        Rt = self.Rt
        M = np.column_stack([Rt[:, 0], Rt[:, 1], Rt @ (np.array([0, 0, z0]) - self.C)])
        return self.K @ M

    def escala(self, z0=0.0):
        """px de pantalla por unidad de mundo (aprox., en el centro) a la altura z0."""
        return F_FOCAL / max(self.Dd + z0, 1.0)


# =====================================================================================================================  CORCHO
def _ruido_periodico(n, sigma, rng):
    a = rng.standard_normal((n, n)).astype(np.float32)
    F = np.fft.fft2(a)
    fx = np.fft.fftfreq(n)[:, None]
    fy = np.fft.fftfreq(n)[None, :]
    g = np.exp(-(fx ** 2 + fy ** 2) * (2 * math.pi * sigma) ** 2 / 2)
    r = np.real(np.fft.ifft2(F * g)).astype(np.float32)
    r -= r.mean()
    return r / (r.std() + 1e-6)


@functools.lru_cache(maxsize=1)
def corcho_mip():
    """Textura de corcho periódica (1024²) con gránulos, motas y agujeros de chinchetas viejas; y sus reducciones."""
    n = 1024
    rng = np.random.default_rng(11)
    base = 0.55 * _ruido_periodico(n, 1.2, rng) + 0.35 * _ruido_periodico(n, 3.0, rng) + 0.30 * _ruido_periodico(n, 14, rng) \
        + 0.22 * _ruido_periodico(n, 60, rng)
    gr = _ruido_periodico(n, 0.7, rng)
    col_a = np.array([0.50, 0.35, 0.21], np.float32)
    col_b = np.array([0.33, 0.22, 0.12], np.float32)
    u = np.clip(0.5 + 0.22 * base, 0, 1)[..., None]
    img = col_b * (1 - u) + col_a * u
    img *= (1.0 + 0.10 * np.clip(gr, -2, 2))[..., None]
    # motas oscuras y claras (corcho aglomerado)
    for k, (col, nn, rr) in enumerate((((0.16, 0.10, 0.05), 2600, (1, 3)), ((0.70, 0.55, 0.36), 1800, (1, 2)), ((0.24, 0.16, 0.08), 500, (3, 6)))):
        m = np.zeros((n, n), np.float32)
        for _ in range(nn):
            x, y = rng.integers(0, n, 2)
            r = int(rng.integers(rr[0], rr[1] + 1))
            for dx in (-n, 0, n):
                for dy in (-n, 0, n):
                    cv2.ellipse(m, (int(x + dx), int(y + dy)), (r, max(1, int(r * rng.uniform(0.5, 1.0)))), float(rng.uniform(0, 180)), 0, 360, 1.0, -1, cv2.LINE_AA)
        m = np.clip(m, 0, 1)[..., None] * 0.55
        img = img * (1 - m) + np.float32(col) * m
    # agujeros de chinchetas viejas
    m = np.zeros((n, n), np.float32)
    for _ in range(140):
        x, y = rng.integers(0, n, 2)
        cv2.circle(m, (int(x), int(y)), 2, 1.0, -1, cv2.LINE_AA)
    img *= (1 - 0.6 * m[..., None])
    img = np.clip(img, 0, 1)
    mips = [img]
    for _ in range(4):
        mips.append(cv2.resize(mips[-1], (mips[-1].shape[1] // 2, mips[-1].shape[0] // 2), interpolation=cv2.INTER_AREA))
    return mips


def dibujar_corcho(lz, V):
    mips = corcho_mip()
    esc = V.escala(0)
    k = 0
    while k < len(mips) - 1 and esc < 0.70 / (2 ** k):
        k += 1
    s = 1.0 / (2 ** k)
    M = V.plano(0) @ np.diag([1 / s, 1 / s, 1.0])
    cv2.warpPerspective(mips[k], M, (W, H), dst=lz, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


# =====================================================================================================================  LÁMINAS
class Lam:
    """Lámina RGBA premultiplicada + sombra difusa (para pegar en 3D)."""

    def __init__(self, rgba, sr=10):
        rgba = np.asarray(rgba)
        rgba = rgba.astype(np.float32) / 255.0 if rgba.dtype == np.uint8 else rgba.astype(np.float32)
        self.h, self.w = rgba.shape[:2]
        a = rgba[..., 3]
        # se guarda en 8 bits (premultiplicado): 4x menos memoria por proceso de render; se pasa a float al mezclar
        self.a = _u8(a)
        self.pm = _u8(rgba[..., :3] * a[..., None])
        self.sr = sr
        self.pad = int(sr * 3)
        self.sh = _u8(cv2.GaussianBlur(np.pad(a.astype(np.float32), self.pad), (0, 0), sr)) if sr > 0 else None
        self._mip = {}

    def nivel(self, esc):
        """Versión reducida si la lámina se ve muy pequeña (evita parpadeo)."""
        k = 0
        while esc < 0.5 / (2 ** k) and min(self.w, self.h) / (2 ** (k + 1)) > 8 and k < 4:
            k += 1
        if k == 0:
            return self.pm, self.a, 1.0
        if k not in self._mip:
            f = 1 / 2 ** k
            sz = (max(2, int(self.w * f)), max(2, int(self.h * f)))
            self._mip[k] = (cv2.resize(self.pm, sz, interpolation=cv2.INTER_AREA), cv2.resize(self.a, sz, interpolation=cv2.INTER_AREA))
        pm, a = self._mip[k]
        return pm, a, pm.shape[1] / self.w


def _u8(x):
    return np.ascontiguousarray(np.clip(np.asarray(x, np.float32) * 255.0 + 0.5, 0, 255).astype(np.uint8))


def _f(x):
    return x.astype(np.float32) * np.float32(1 / 255.0) if x.dtype == np.uint8 else x


def _mezclar(lz, pm, a, M, op):
    h, w = a.shape
    c = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    d = cv2.perspectiveTransform(c, M).reshape(-1, 2)
    x0, y0 = d.min(0)
    x1, y1 = d.max(0)
    ix0, iy0 = int(max(math.floor(x0), 0)), int(max(math.floor(y0), 0))
    ix1, iy1 = int(min(math.ceil(x1), W)), int(min(math.ceil(y1), H))
    if ix1 <= ix0 or iy1 <= iy0 or (x1 - x0) > 40000 or (y1 - y0) > 40000:
        return
    T = np.array([[1, 0, -ix0], [0, 1, -iy0], [0, 0, 1]], np.float64)
    sz = (ix1 - ix0, iy1 - iy0)
    aw = _f(cv2.warpPerspective(a, T @ M, sz, flags=cv2.INTER_LINEAR, borderValue=0))
    if pm is None:
        D.mezclar_pm(lz, np.zeros(aw.shape + (3,), np.float32), aw, ix0, iy0, op)
        return
    pw = _f(cv2.warpPerspective(pm, T @ M, sz, flags=cv2.INTER_LINEAR, borderValue=0))
    D.mezclar_pm(lz, pw, aw, ix0, iy0, op)


def esquinas3d(w, h, x, y, z=0.0, s=1.0, rz=0.0, tx=0.0, ty=0.0):
    """Esquinas (4,3) de una lámina w×h centrada en (x, y, z), escala s, giro rz en el plano y bisagras tx (eje x) / ty (eje y)."""
    hw, hh = w * s / 2, h * s / 2
    P = np.array([[-hw, -hh, 0], [hw, -hh, 0], [hw, hh, 0], [-hw, hh, 0]], np.float64)
    a, b, c = math.radians(tx), math.radians(ty), math.radians(rz)
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return P @ (Rz @ Rx @ Ry).T + np.array([x, y, z])


LUZ = np.array([0.55, 0.85])          # dirección de la sombra sobre el corcho (luz arriba-izquierda)


def pegar3d(lz, V, L, x, y, z=-1.0, s=1.0, rz=0.0, tx=0.0, ty=0.0, op=1.0, sombra=1.0):
    """Pega la lámina L en el mundo; su sombra cae sobre el corcho desplazada según la altura."""
    if op <= 0.003:
        return None
    E = esquinas3d(L.w, L.h, x, y, z, s, rz, tx, ty)
    q, zc = V.proy(E)
    if (zc < 5).any():
        return None
    if q[:, 0].max() < -50 or q[:, 0].min() > W + 50 or q[:, 1].max() < -50 or q[:, 1].min() > H + 50:
        return q
    esc = math.sqrt(abs(np.cross(q[1] - q[0], q[3] - q[0]))) / math.sqrt(L.w * L.h + 1e-6)
    if sombra > 0 and L.sh is not None:
        alt = max(-z, 0.0)
        off = LUZ * (6.0 + alt * 0.35)
        Es = E.copy()
        Es[:, :2] += off
        Es[:, 2] = 0.0
        qs, _ = V.proy(Es)
        p = L.pad
        src = np.float32([[p, p], [p + L.w, p], [p + L.w, p + L.h], [p, p + L.h]])
        Ms = cv2.getPerspectiveTransform(src, np.float32(qs))
        so = sombra * op * (0.55 if alt < 30 else 0.55 * 30 / alt + 0.1)
        _mezclar(lz, None, L.sh, Ms, so)
    pm, a, f = L.nivel(esc)
    src = np.float32([[0, 0], [L.w * f, 0], [L.w * f, L.h * f], [0, L.h * f]])
    M = cv2.getPerspectiveTransform(src, np.float32(q))
    _mezclar(lz, pm, a, M, op)
    return q


# =====================================================================================================================  FABRICAR LÁMINAS
def _papel(w, h, color=(0.95, 0.93, 0.86), seed=0, envejecer=0.25, borde=0.0):
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((h // 4 + 2, w // 4 + 2)).astype(np.float32)
    n = cv2.resize(cv2.GaussianBlur(n, (0, 0), 3), (w, h), interpolation=cv2.INTER_CUBIC)
    f = rng.standard_normal((h, w)).astype(np.float32) * 0.012
    img = np.ones((h, w, 3), np.float32) * np.float32(color)
    img *= (1 + 0.025 * n + f)[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - envejecer * 0.25 * np.clip(r - 0.6, 0, 1))[..., None]
    img[..., 2] *= 1 - envejecer * 0.08 * np.clip(r, 0, 1.4)
    a = np.ones((h, w), np.float32)
    if borde > 0:            # borde rasgado/irregular
        m = np.zeros((h, w), np.uint8)
        pts = []
        for i in range(0, w, 6):
            pts.append((i, int(borde * rng.random())))
        for j in range(0, h, 6):
            pts.append((w - 1 - int(borde * rng.random()), j))
        for i in range(w, 0, -6):
            pts.append((i, h - 1 - int(borde * rng.random())))
        for j in range(h, 0, -6):
            pts.append((int(borde * rng.random()), j))
        cv2.fillPoly(m, [np.array(pts, np.int32)], 255, cv2.LINE_AA)
        a = m.astype(np.float32) / 255.0
    return np.clip(img, 0, 1), a


def _texto_en(im_pil, xy, txt, fuente, px, color, ancho=None, interlinea=1.18, anchor="la", rot=0):
    d = ImageDraw.Draw(im_pil)
    f = fnt(fuente, px)
    lineas = []
    if ancho:
        for par in txt.split("\n"):
            pal = par.split(" ")
            cur = ""
            for p in pal:
                prueba = (cur + " " + p).strip()
                if f.getlength(prueba) > ancho and cur:
                    lineas.append(cur)
                    cur = p
                else:
                    cur = prueba
            lineas.append(cur)
    else:
        lineas = txt.split("\n")
    x, y = xy
    for ln in lineas:
        d.text((x, y), ln, font=f, fill=tuple(int(c * 255) for c in color) + (255,), anchor=anchor)
        y += px * interlinea
    return y


def _a_rgba(img, a):
    return np.dstack([img, a]).astype(np.float32)


@functools.lru_cache(maxsize=64)
def ficha(txt, ancho=520, alto=330, titulo=None, seed=1, color=(0.96, 0.95, 0.90), px=34, fuente="maquina", tinta=(0.10, 0.09, 0.10),
          rayada=True, sello=None):
    """Ficha bibliográfica (index card) con texto a máquina."""
    img, a = _papel(ancho, alto, color, seed, 0.3)
    pil = Image.fromarray((img * 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    if rayada:
        for yy in range(int(alto * 0.30), alto - 10, 34):
            d.line([(14, yy), (ancho - 14, yy)], fill=(150, 170, 205), width=2)
        d.line([(14, int(alto * 0.22)), (ancho - 14, int(alto * 0.22))], fill=(205, 90, 90), width=2)
    y = 26
    if titulo:
        y = _texto_en(pil, (28, 20), titulo, "courier_b", px * 0.95, (0.55, 0.06, 0.06), ancho - 56)
        y = max(y, alto * 0.22 + 14)
    if rayada:                      # la escritura se apoya en los renglones (cada 34 px desde el 30 % del alto)
        r0 = int(alto * 0.30)
        k = max(0, int(math.ceil((y + px * 0.85 - r0) / 34.0)))
        _texto_en(pil, (28, r0 + 34 * k - px * 0.92), txt, fuente, px, tinta, ancho - 56, 34.0 / px)
    else:
        _texto_en(pil, (28, y + 4), txt, fuente, px, tinta, ancho - 56, 1.2)
    img = np.asarray(pil, np.float32) / 255.0
    return Lam(_a_rgba(img, a), sr=8)


@functools.lru_cache(maxsize=64)
def nota(txt, lado=300, color=(0.98, 0.86, 0.25), px=46, seed=2, fuente="mano", tinta=(0.08, 0.08, 0.12)):
    """Nota adhesiva con letra a mano (rizo de sombra abajo)."""
    img, a = _papel(lado, lado, color, seed, 0.15)
    yy = np.linspace(0, 1, lado, dtype=np.float32)[:, None, None]
    img *= 1 - 0.10 * yy ** 3
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    f = fnt(fuente, px)
    lineas = []
    for par in txt.split("\n"):
        cur = ""
        for p in par.split(" "):
            pr_ = (cur + " " + p).strip()
            if f.getlength(pr_) > lado - 36 and cur:
                lineas.append(cur)
                cur = p
            else:
                cur = pr_
        lineas.append(cur)
    hh = len(lineas) * px * 1.05
    y = (lado - hh) / 2
    for ln in lineas:
        d.text((lado / 2, y), ln, font=f, fill=tuple(int(c * 255) for c in tinta), anchor="ma")
        y += px * 1.05
    img = np.asarray(pil, np.float32) / 255.0
    return Lam(_a_rgba(img, a), sr=7)


def cargar_img(nombre, lado=1400):
    return D.cargar(D.ruta_img(nombre), lado)


@functools.lru_cache(maxsize=64)
def polaroid(nombre=None, ancho=460, asp=1.0, foco=(0.5, 0.5), leyenda=None, seed=3, gris=False, ventana=False, px=40, zoom=1.0):
    """Polaroid con foto real (o ventana transparente para un portal) y leyenda a rotulador.
    Devuelve (Lam, rect_ventana) con rect en px de la lámina (x0, y0, x1, y1)."""
    b = int(ancho * 0.06)
    pie = int(ancho * 0.22)
    fw = ancho - 2 * b
    fh = int(fw / asp)
    h = b + fh + pie
    img, a = _papel(ancho, h, (0.95, 0.94, 0.90), seed, 0.35)
    if nombre is not None and not ventana:
        im = cargar_img(nombre, 1600)
        ih, iw = im.shape[:2]
        k = max(fw / iw, fh / ih) * zoom
        rs = cv2.resize(im, (max(fw, int(iw * k) + 1), max(fh, int(ih * k) + 1)), interpolation=cv2.INTER_AREA)
        ox = int(clamp(foco[0] * rs.shape[1] - fw / 2, 0, rs.shape[1] - fw))
        oy = int(clamp(foco[1] * rs.shape[0] - fh / 2, 0, rs.shape[0] - fh))
        foto = rs[oy:oy + fh, ox:ox + fw].astype(np.float32) / 255.0
        if gris:
            g = foto.mean(2, keepdims=True)
            foto = np.repeat(g, 3, 2) * np.float32([1.0, 0.97, 0.92])
        foto = np.clip((foto - 0.5) * 1.05 + 0.5, 0, 1) * 0.96
        img[b:b + fh, b:b + fw] = foto
    elif ventana:
        a[b:b + fh, b:b + fw] = 0.0
    else:
        img[b:b + fh, b:b + fw] = 0.06
    if leyenda:
        pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
        d = ImageDraw.Draw(pil)
        f = fnt("marcador", px)
        while f.getlength(leyenda) > ancho - 30 and px > 16:
            px -= 2
            f = fnt("marcador", px)
        d.text((ancho / 2, b + fh + pie * 0.52), leyenda, font=f, fill=(25, 22, 30), anchor="mm")
        img = np.asarray(pil, np.float32) / 255.0
        if ventana:
            img[b:b + fh, b:b + fw] = 0.0
    return Lam(_a_rgba(img, a), sr=10), (b, b, b + fw, b + fh)


@functools.lru_cache(maxsize=32)
def silueta_card(nombre, sub="SIN FOTO LIBRE", ancho=460, seed=5):
    """Polaroid de sospechoso sin foto libre: silueta gris con signo de interrogación (no se inventa un rostro)."""
    b = int(ancho * 0.06)
    pie = int(ancho * 0.22)
    fw = ancho - 2 * b
    fh = fw
    h = b + fh + pie
    img, a = _papel(ancho, h, (0.95, 0.94, 0.90), seed, 0.35)
    ph = np.ones((fh, fw, 3), np.float32) * np.float32([0.20, 0.21, 0.24])
    yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32)
    ph *= (1 - 0.35 * np.sqrt(((xx - fw / 2) / fw) ** 2 + ((yy - fh * 0.3) / fh) ** 2))[..., None]
    m = np.zeros((fh, fw), np.uint8)
    cv2.ellipse(m, (fw // 2, int(fh * 0.40)), (int(fw * 0.17), int(fh * 0.21)), 0, 0, 360, 255, -1, cv2.LINE_AA)
    cv2.ellipse(m, (fw // 2, int(fh * 1.02)), (int(fw * 0.40), int(fh * 0.38)), 0, 180, 360, 255, -1, cv2.LINE_AA)
    cv2.rectangle(m, (int(fw * 0.42), int(fh * 0.55)), (int(fw * 0.58), int(fh * 0.68)), 255, -1)
    ms = m.astype(np.float32)[..., None] / 255
    ph = ph * (1 - ms) + ms * np.float32([0.07, 0.075, 0.085])
    pil_ph = Image.fromarray((np.clip(ph, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(pil_ph)
    d.text((fw // 2, int(fh * 0.40)), "?", font=fnt("serif", int(fh * 0.30)), fill=(200, 40, 40), anchor="mm")
    d.text((fw // 2, int(fh * 0.92)), sub, font=fnt("courier_b", int(fw * 0.055)), fill=(170, 170, 175), anchor="mm")
    img[b:b + fh, b:b + fw] = np.asarray(pil_ph, np.float32) / 255
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    px = 40
    f = fnt("marcador", px)
    while f.getlength(nombre) > ancho - 30 and px > 16:
        px -= 2
        f = fnt("marcador", px)
    d.text((ancho / 2, b + fh + pie * 0.52), nombre, font=f, fill=(25, 22, 30), anchor="mm")
    return Lam(_a_rgba(np.asarray(pil, np.float32) / 255, a), sr=10)


@functools.lru_cache(maxsize=32)
def hoja_img(nombre, alto=900, recorte=None, borde=0.0, seed=4, tono=1.0):
    """Documento / recorte real (escaneo de Commons) como papel."""
    im = cargar_img(nombre, 2400).astype(np.float32) / 255.0
    if recorte:
        h0, w0 = im.shape[:2]
        x0, y0, x1, y1 = recorte
        im = im[int(y0 * h0):int(y1 * h0), int(x0 * w0):int(x1 * w0)]
    k = alto / im.shape[0]
    im = cv2.resize(im, (max(2, int(im.shape[1] * k)), alto), interpolation=cv2.INTER_AREA)
    pap, a = _papel(im.shape[1], im.shape[0], (1, 1, 1), seed, 0.3, borde)
    img = np.clip(im * pap * tono, 0, 1)
    return Lam(_a_rgba(img, a), sr=10)


@functools.lru_cache(maxsize=32)
def lam_texto(txt, fuente="marcador", px=80, color=(0.92, 0.10, 0.10), rot_libre=0):
    """Texto suelto (rotulador sobre el corcho o un papel)."""
    f = fnt(fuente, px)
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20
    pil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(pil).text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=tuple(int(c * 255) for c in color) + (235,))
    return Lam(np.asarray(pil, np.float32) / 255.0, sr=0)


@functools.lru_cache(maxsize=32)
def sello_lam(txt, px=70, color=(0.78, 0.08, 0.08)):
    sp = D._estampa_sprite(txt, px, tuple(color))
    rgba = np.dstack([np.clip(sp.pm / np.maximum(sp.a[..., None], 1e-4), 0, 1), sp.a]).astype(np.float32)
    return Lam(rgba, sr=0)


@functools.lru_cache(maxsize=8)
def chincheta_lam(color, r=13):
    d = r * 4
    yy, xx = np.mgrid[0:d, 0:d].astype(np.float32)
    rr = np.hypot(xx - d / 2, yy - d / 2)
    a = np.clip(r - rr + 0.5, 0, 1)
    sh = np.clip(1 - np.hypot((xx - d * 0.40) / (r * 0.55), (yy - d * 0.38) / (r * 0.55)), 0, 1)
    col = np.float32(color)[None, None, :] * (0.50 + 0.50 * np.clip(1 - rr / r, 0, 1)[..., None] ** 0.6)
    col = col + sh[..., None] ** 2 * 0.75
    borde = np.clip(1 - np.abs(rr - r * 0.86) / 1.6, 0, 1)[..., None]
    col = col * (1 - 0.35 * borde)
    return Lam(np.dstack([np.clip(col, 0, 1), a]).astype(np.float32), sr=3)


# =====================================================================================================================  PIEZAS
PIEZAS = []


class Pieza:
    """Una lámina en el tablero.
    entrada: 'cae' (llega volando desde la cámara, gira y se asienta), 'desliza' (entra rasante desde un lado), 'aparece' (fundido), None (ya estaba).
    chinchetas: lista de (dx, dy, color) en px de la lámina relativos al centro (escalados); clavadas al asentarse.
    portal: fn(t) -> imagen float32 (h, w, 3) que se dibuja dentro de la ventana (polaroid con ventana=True).
    t_fuera: la pieza sale (se arranca) desde ese tiempo. luz: brillo (1 = normal)."""

    def __init__(self, L, x, y, rot=0.0, s=1.0, t_in=0.0, entrada="cae", desde=None, dur=0.75, chinchetas=((0, None, (0.82, 0.10, 0.10)),),
                 z=-2.0, portal=None, ventana=None, t_fuera=None, sonido=True, capa=1, flota=True, op=1.0, teaser=None):
        self.L, self.x, self.y, self.rot, self.s = L, x, y, rot, s
        self.t_in, self.entrada, self.dur, self.z = t_in, entrada, dur, z
        self.desde = desde
        self.ch = []
        for c in chinchetas:
            dx, dy, col = c
            if dy is None:
                dy = -L.h * 0.5 + 22
            self.ch.append((dx, dy, col))
        self.portal, self.ventana, self.t_fuera, self.capa, self.flota, self.op = portal, ventana, t_fuera, capa, flota, op
        self.teaser = teaser
        self.marcas = []           # (fn(lz, V, t, pieza)) dibujos sobre la pieza
        self.fase = (hash((x, y)) % 1000) / 160.0
        PIEZAS.append(self)
        if sonido and entrada and t_in > 0.05:
            from kit import snd
            snd(t_in + dur * 0.92, "pin", 0.55)
            snd(t_in, "papel", 0.30)
            SACUDIDA.add(t_in + dur * 0.92, 3.0)

    # punto del mundo de un anclaje local (px de lámina relativos al centro)
    def punto(self, dx, dy, t=None):
        c, s_ = math.cos(math.radians(self.rot)), math.sin(math.radians(self.rot))
        return (self.x + (dx * c - dy * s_) * self.s, self.y + (dx * s_ + dy * c) * self.s)

    def pin(self, i=0):
        dx, dy, _ = self.ch[i]
        return self.punto(dx, dy)

    def visible(self, t):
        if self.teaser and self.teaser[0] <= t < self.teaser[1]:
            return True
        return t >= self.t_in and (self.t_fuera is None or t < self.t_fuera + 0.8)

    def pose(self, t):
        """(x, y, z, s, rz, tx, ty, op)"""
        x, y, z, s, rz, tx, ty, op = self.x, self.y, self.z, self.s, self.rot, 0.0, 0.0, self.op
        if self.teaser and self.teaser[0] <= t < self.teaser[1]:
            return x, y, z, s, rz, tx, ty, op
        e = t - self.t_in
        if self.entrada == "cae" and e < self.dur:
            u = e_out(pr(e, 0, self.dur))
            dx, dy = self.desde if self.desde else (-260, -180)
            x, y = x + dx * (1 - u), y + dy * (1 - u)
            z = lerp(-650.0, self.z, u)
            rz = rz + 24 * (1 - u)
            tx, ty = 26 * (1 - u), -18 * (1 - u)
            op *= sm(pr(e, 0, 0.12))
        elif self.entrada == "desliza" and e < self.dur:
            u = e_out(pr(e, 0, self.dur))
            dx, dy = self.desde if self.desde else (-900, 0)
            x, y = x + dx * (1 - u), y + dy * (1 - u)
            z = lerp(-60.0, self.z, u)
            rz = rz - 10 * (1 - u)
            op *= sm(pr(e, 0, 0.15))
        elif self.entrada == "aparece":
            op *= sm(pr(e, 0, self.dur))
        # asentamiento con rebote + respiración (aire de la habitación)
        if self.entrada and e >= self.dur:
            k = e - self.dur
            rz += 2.2 * math.exp(-k * 5) * math.sin(k * 18)
            z += -6.0 * math.exp(-k * 7) * abs(math.sin(k * 14))
        if self.flota:
            tx += 0.9 * math.sin(0.7 * t + self.fase)
            ty += 0.7 * math.sin(0.53 * t + 2 * self.fase)
        if self.t_fuera is not None and t >= self.t_fuera:
            u = sm(pr(t, self.t_fuera, self.t_fuera + 0.8))
            z = lerp(z, -700, u)
            rz += 30 * u
            op *= 1 - u
        return x, y, z, s, rz, tx, ty, op

    def dibujar(self, lz, V, t):
        x, y, z, s, rz, tx, ty, op = self.pose(t)
        if op <= 0.003:
            return
        if self.portal is not None and self.ventana is not None:
            self._portal(lz, V, t, x, y, z, s, rz, tx, ty, op)
        q = pegar3d(lz, V, self.L, x, y, z, s, rz, tx, ty, op)
        for m in self.marcas:
            m(lz, V, t, self)
        # chinchetas: se clavan al asentarse
        t_c = self.t_in + self.dur * 0.9 if self.entrada else -1
        if (self.teaser and self.teaser[0] <= t < self.teaser[1]) or t >= t_c:
            u = 1.0 if (self.teaser and self.teaser[0] <= t < self.teaser[1]) else e_back(pr(t, t_c, t_c + 0.18))
            for dx, dy, col in self.ch:
                if col is None:
                    continue
                px_, py_ = self.punto(dx, dy)
                L = chincheta_lam(tuple(col))
                pegar3d(lz, V, L, px_, py_, z - 7 - 40 * (1 - u), 1.0 + 0.6 * (1 - u), 0, 0, 0, op * sm(pr(u, 0, 0.3)), 1.0)

    def esquinas_ventana(self, t):
        x, y, z, s, rz, tx, ty, op = self.pose(t)
        x0, y0, x1, y1 = self.ventana
        cx, cy = (x0 + x1) / 2 - self.L.w / 2, (y0 + y1) / 2 - self.L.h / 2
        E = esquinas3d(x1 - x0, y1 - y0, 0, 0, 0, 1.0, 0, 0, 0)
        E[:, 0] += cx
        E[:, 1] += cy
        a, b, c = math.radians(tx), math.radians(ty), math.radians(rz)
        Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
        Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
        Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
        return (E * s) @ (Rz @ Rx @ Ry).T + np.array([x, y, z])

    def _portal(self, lz, V, t, x, y, z, s, rz, tx, ty, op):
        E = self.esquinas_ventana(t)
        q, zc = V.proy(E)
        if (zc < 5).any():
            return
        if q[:, 0].max() < 0 or q[:, 0].min() > W or q[:, 1].max() < 0 or q[:, 1].min() > H:
            return
        img = self.portal(t)
        h, w = img.shape[:2]
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(q))
        _mezclar(lz, img * 1.0, np.ones((h, w), np.float32), M, op)

    def llena_pantalla(self, t, V):
        """True si la ventana del portal cubre toda la pantalla (no hace falta dibujar el tablero)."""
        if self.portal is None or self.ventana is None or not self.visible(t):
            return False
        q, zc = V.proy(self.esquinas_ventana(t))
        if (zc < 5).any():
            return False
        poly = q.astype(np.float32).reshape(-1, 1, 2)
        for px_, py_ in ((0, 0), (W, 0), (W, H), (0, H)):
            if cv2.pointPolygonTest(poly, (float(px_), float(py_)), True) < 2:
                return False
        return True


# =====================================================================================================================  HILOS Y CONECTORES
HILOS = []
LANA = dict(rojo=(0.80, 0.07, 0.07), amarillo=(0.95, 0.78, 0.12), azul=(0.12, 0.42, 0.85), blanco=(0.93, 0.92, 0.88),
            verde=(0.15, 0.70, 0.35), negro=(0.05, 0.05, 0.06))


def _poli_mask(pts, grosor, x0, y0, w, h):
    m = np.zeros((h, w), np.uint8)
    q = np.round((np.asarray(pts, np.float32) - [x0, y0]) * 16).astype(np.int32)
    cv2.polylines(m, [q], False, 255, max(1, int(round(grosor))), cv2.LINE_AA, shift=4)
    return m.astype(np.float32) / 255.0


def trazo(lz, pts, color, grosor, op=1.0, sombra_pts=None, sombra_op=0.45, sombra_sig=None, textura=False, guion=None):
    """Polilínea en pantalla con sombra (otra polilínea) y textura de lana opcional."""
    pts = np.asarray(pts, np.float32)
    if len(pts) < 2 or op <= 0.003:
        return
    todo = pts if sombra_pts is None else np.vstack([pts, sombra_pts])
    g = grosor * 3 + 16
    x0, y0 = np.floor(todo.min(0) - g).astype(int)
    x1, y1 = np.ceil(todo.max(0) + g).astype(int)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0:
        return
    w, h = x1 - x0, y1 - y0
    if sombra_pts is not None:
        sm_ = _poli_mask(sombra_pts, grosor, x0, y0, w, h)
        sm_ = cv2.GaussianBlur(sm_, (0, 0), sombra_sig or max(1.0, grosor * 0.9))
        D.mezclar_pm(lz, np.zeros(sm_.shape + (3,), np.float32), sm_ * sombra_op, x0, y0, op)
    m = _poli_mask(pts, grosor, x0, y0, w, h)
    if guion:                                  # línea a trazos (marcador punteado)
        L_, H_ = guion
        seg = np.cumsum(np.r_[0, np.hypot(*np.diff(pts, axis=0).T)])
        mm = np.zeros_like(m)
        for i in range(len(pts) - 1):
            if (seg[i] % (L_ + H_)) < L_:
                mm = np.maximum(mm, _poli_mask(pts[i:i + 2], grosor, x0, y0, w, h))
        m = mm
    col = np.float32(color)
    pm = m[..., None] * col
    D.mezclar_pm(lz, pm, m, x0, y0, op)
    if textura and grosor >= 2.2:                # brillos torcidos de la lana
        luz = _poli_mask(pts + np.float32([-grosor * 0.18, -grosor * 0.18]), max(1.0, grosor * 0.35), x0, y0, w, h)
        seg = np.cumsum(np.r_[0, np.hypot(*np.diff(pts, axis=0).T)])
        per = max(6.0, grosor * 2.6)
        mask = np.zeros_like(luz)
        for i in range(len(pts) - 1):
            if (seg[i] % per) < per * 0.5:
                mask = np.maximum(mask, _poli_mask(pts[i:i + 2], max(1.0, grosor * 0.35), x0 - 0, y0 - 0, w, h))
        luz = luz * mask
        cl = np.clip(col * 1.6 + 0.12, 0, 1)
        D.mezclar_pm(lz, luz[..., None] * cl, luz * 0.55, x0, y0, op)


class Hilo:
    """Lana entre dos puntos del mundo (o dos piezas: se usa su chincheta). Se tiende de a -> b desde t0 en `dur` s.
    corte: tiempo en que se corta (las dos mitades caen colgando de sus chinchetas). etiqueta: Lam colgada en el centro."""

    def __init__(self, a, b, t0, dur=0.9, color="rojo", grosor=3.2, holgura=0.035, corte=None, etiqueta=None, z=-8.0, sonido=True,
                 t_fuera=None, teaser=None):
        self.a, self.b, self.t0, self.dur = a, b, t0, dur
        self.col = LANA.get(color, color) if isinstance(color, str) else color
        self.grosor, self.holgura, self.corte, self.etiqueta, self.z = grosor, holgura, corte, etiqueta, z
        self.t_fuera, self.teaser = t_fuera, teaser
        HILOS.append(self)
        if sonido and t0 > 0.05:
            from kit import snd
            snd(t0, "whoosh", 0.18, dur=min(0.6, dur))
            if corte:
                snd(corte, "zap", 0.35)

    def _p(self, e):
        return e.pin() if isinstance(e, Pieza) else e

    def dibujar(self, lz, V, t):
        en_teaser = self.teaser and self.teaser[0] <= t < self.teaser[1]
        if not en_teaser and (t < self.t0 or (self.t_fuera is not None and t > self.t_fuera + 0.6)):
            return
        op = 1.0
        if self.t_fuera is not None and t > self.t_fuera and not en_teaser:
            op = 1 - sm(pr(t, self.t_fuera, self.t_fuera + 0.6))
        (ax, ay), (bx, by) = self._p(self.a), self._p(self.b)
        u = 1.0 if en_teaser else e_out(pr(t, self.t0, self.t0 + self.dur))
        dist = math.hypot(bx - ax, by - ay)
        n = max(12, min(70, int(dist / 40)))
        e_ = t - (self.t0 + self.dur)
        vaiven = 0.0 if en_teaser else (math.exp(-e_ * 3.0) * math.sin(e_ * 11) * 0.5 if e_ > 0 else 0.0)
        sag = self.holgura * dist * (1 + vaiven) + 2.0 * math.sin(0.8 * t + ax * 0.01)
        if self.corte is not None and t >= self.corte and not en_teaser:
            # dos mitades que caen colgando de cada extremo
            k = t - self.corte
            caida = 1 - math.exp(-k * 4.0)
            mitad = dist * 0.5
            for (px_, py_), (qx, qy) in (((ax, ay), (bx, by)), ((bx, by), (ax, ay))):
                ang0 = math.atan2(qy - py_, qx - px_)
                ang = lerp(ang0, math.pi / 2 + 0.25 * math.sin(k * 3.0) * math.exp(-k * 1.2), caida)
                ss = np.linspace(0, 1, 20)
                P = []
                for s_ in ss:
                    a_ = lerp(ang0, ang, s_ ** 0.7)
                    P.append((px_ + math.cos(a_) * mitad * s_, py_ + math.sin(a_) * mitad * s_ + sag * 0.3 * s_ * (1 - caida), self.z * (1 - s_ * 0.3)))
                self._dibujar_pts(lz, V, np.array(P), op)
            return
        ss = np.linspace(0, u, n)
        P = np.stack([ax + (bx - ax) * ss, ay + (by - ay) * ss + 4 * sag * ss * (1 - ss) * (1 if u >= 1 else 0.6),
                      np.full(n, self.z) - 10 * np.sin(np.pi * ss) * (1 - u)], 1)
        self._dibujar_pts(lz, V, P, op)
        if self.etiqueta is not None and u >= 1:
            mx, my = (ax + bx) / 2, (ay + by) / 2 + sag
            ang = math.degrees(math.atan2(by - ay, bx - ax)) * 0.25
            ue = e_back(pr(t, self.t0 + self.dur, self.t0 + self.dur + 0.35)) if not en_teaser else 1.0
            pegar3d(lz, V, self.etiqueta, mx, my + self.etiqueta.h * 0.5 * ue, self.z - 4, ue, ang + 3 * math.sin(1.3 * t), 0, 0, op)

    def _dibujar_pts(self, lz, V, P, op):
        q, zc = V.proy(P)
        if (zc < 5).any():
            return
        Ps = P.copy()
        Ps[:, :2] += LUZ * (8.0 - P[:, 2:3] * 0.35)
        Ps[:, 2] = 0
        qs, _ = V.proy(Ps)
        g = max(1.2, self.grosor * V.escala(self.z))
        trazo(lz, q, self.col, g, op, qs, 0.45, textura=True)


class Marca:
    """Dibujo a rotulador sobre el plano del corcho (o sobre un papel a altura z): flecha, círculo, tache, subrayado, texto.
    pts: lista de (x, y) del mundo; se dibuja progresivamente de t0 a t0+dur."""

    def __init__(self, pts, t0, dur=0.6, color=(0.86, 0.08, 0.08), grosor=7.0, z=-1.5, punta=False, t_fuera=None, sonido=True, op=0.92,
                 guion=None, teaser=None):
        self.P = np.asarray(pts, np.float64)
        self.t0, self.dur, self.col, self.grosor, self.z, self.punta, self.t_fuera, self.op = t0, dur, color, grosor, z, punta, t_fuera, op
        self.guion, self.teaser = guion, teaser
        MARCAS.append(self)
        if sonido and t0 > 0.05:
            from kit import snd
            snd(t0, "garabato", 0.32)

    def dibujar(self, lz, V, t):
        en_t = self.teaser and self.teaser[0] <= t < self.teaser[1]
        if not en_t and (t < self.t0 or (self.t_fuera is not None and t > self.t_fuera + 0.5)):
            return
        u = 1.0 if en_t else sm(pr(t, self.t0, self.t0 + self.dur))
        op = self.op * (1 - (sm(pr(t, self.t_fuera, self.t_fuera + 0.5)) if (self.t_fuera is not None and not en_t) else 0))
        seg = np.cumsum(np.r_[0, np.hypot(*np.diff(self.P, axis=0).T)])
        Ltot = seg[-1]
        lim = Ltot * u
        P = [self.P[0]]
        for i in range(1, len(self.P)):
            if seg[i] <= lim:
                P.append(self.P[i])
            else:
                f = (lim - seg[i - 1]) / max(seg[i] - seg[i - 1], 1e-6)
                P.append(self.P[i - 1] + (self.P[i] - self.P[i - 1]) * f)
                break
        P = np.asarray(P)
        if len(P) < 2:
            return
        P3 = np.column_stack([P, np.full(len(P), self.z)])
        q, zc = V.proy(P3)
        if (zc < 5).any():
            return
        g = max(1.5, self.grosor * V.escala(self.z))
        trazo(lz, q, self.col, g, op, guion=self.guion)
        if self.punta and u > 0.97 and len(P) >= 2:
            a = P[-1]
            d = P[-1] - P[-2]
            d = d / (np.linalg.norm(d) + 1e-6)
            nrm = np.array([-d[1], d[0]])
            L_ = self.grosor * 4.5
            for sg in (1, -1):
                b = a - d * L_ + nrm * L_ * 0.6 * sg
                qq, _ = V.proy(np.array([[*a, self.z], [*b, self.z]]))
                trazo(lz, qq, self.col, g, op)


MARCAS = []


def circulo_pts(cx, cy, rx, ry, vueltas=1.08, n=60, seed=0, rot=-20):
    rng = np.random.default_rng(seed)
    a0 = math.radians(rot)
    out = []
    for i in range(n + 1):
        a = a0 + 2 * math.pi * vueltas * i / n
        j = 1 + 0.03 * math.sin(i * 0.7 + seed) + 0.02 * rng.standard_normal()
        out.append((cx + rx * j * math.cos(a), cy + ry * j * math.sin(a)))
    return out


def flecha_pts(a, b, curva=0.18, n=26, seed=0):
    (ax, ay), (bx, by) = a, b
    mx, my = (ax + bx) / 2, (ay + by) / 2
    dx, dy = bx - ax, by - ay
    cx, cy = mx - dy * curva, my + dx * curva
    out = []
    rng = np.random.default_rng(seed)
    for i in range(n + 1):
        s = i / n
        x = (1 - s) ** 2 * ax + 2 * (1 - s) * s * cx + s ** 2 * bx
        y = (1 - s) ** 2 * ay + 2 * (1 - s) * s * cy + s ** 2 * by
        out.append((x + rng.normal(0, 1.2), y + rng.normal(0, 1.2)))
    return out


class Punteada:
    """Línea de datos (correo, transacción) entre dos puntos del mundo: trazo discontinuo claro + paquetes luminosos que viajan."""

    def __init__(self, a, b, t0, t1=None, color=(0.95, 0.92, 0.70), curva=0.12, z=-3.0, paquetes=3, vel=0.45, dur=0.8, grosor=3.0):
        self.a, self.b, self.t0, self.t1, self.col, self.curva, self.z = a, b, t0, t1, color, curva, z
        self.paq, self.vel, self.dur, self.grosor = paquetes, vel, dur, grosor
        CONECTORES.append(self)

    def _p(self, e):
        return e.pin() if isinstance(e, Pieza) else e

    def dibujar(self, lz, V, t):
        if t < self.t0 or (self.t1 is not None and t > self.t1 + 0.5):
            return
        op = 1 - (sm(pr(t, self.t1, self.t1 + 0.5)) if self.t1 is not None else 0)
        u = e_out(pr(t, self.t0, self.t0 + self.dur))
        P = np.array(flecha_pts(self._p(self.a), self._p(self.b), self.curva, 40, 3))
        k = max(2, int(len(P) * u))
        P3 = np.column_stack([P[:k], np.full(k, self.z)])
        q, zc = V.proy(P3)
        if (zc < 5).any():
            return
        g = max(1.2, self.grosor * V.escala(self.z))
        trazo(lz, q, self.col, g, op * 0.85, guion=(14, 10))
        if u >= 1:
            for j in range(self.paq):
                s = ((t - self.t0) * self.vel + j / self.paq) % 1.0
                i = s * (len(P) - 1)
                i0 = int(i)
                p = P[i0] + (P[min(i0 + 1, len(P) - 1)] - P[i0]) * (i - i0)
                qq, _ = V.proy(np.array([[*p, self.z - 2]]))
                r = max(3.0, 9 * V.escala(self.z))
                x0, y0 = int(qq[0, 0] - r * 4), int(qq[0, 1] - r * 4)
                sz = int(r * 8)
                if x0 + sz < 0 or y0 + sz < 0 or x0 > W or y0 > H:
                    continue
                yy, xx = np.mgrid[0:sz, 0:sz].astype(np.float32)
                gl = np.exp(-((xx - sz / 2) ** 2 + (yy - sz / 2) ** 2) / (2 * r * r)) * op
                xs0, ys0 = max(x0, 0), max(y0, 0)
                xs1, ys1 = min(x0 + sz, W), min(y0 + sz, H)
                gl = gl[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
                lz[ys0:ys1, xs0:xs1] += gl[..., None] * np.float32([1.0, 0.85, 0.45]) * 0.9


CONECTORES = []


class Cinta:
    """Tira de cinta adhesiva semitransparente sobre el borde de un papel (o uniendo dos papeles)."""

    def __init__(self, x, y, rot, t0, largo=150, ancho=46, z=-3.5):
        self.x, self.y, self.rot, self.t0, self.z = x, y, rot, t0, z
        self.L = _cinta_lam(int(largo), int(ancho), int(abs(x * 7 + y) % 97))
        CONECTORES.append(self)

    def dibujar(self, lz, V, t):
        if t < self.t0:
            return
        u = e_out(pr(t, self.t0, self.t0 + 0.25))
        pegar3d(lz, V, self.L, self.x, self.y, self.z, lerp(1.25, 1.0, u), self.rot, 0, 0, u * 0.92, 0.25)


@functools.lru_cache(maxsize=16)
def _cinta_lam(largo, ancho, seed):
    rng = np.random.default_rng(seed)
    img = np.ones((ancho, largo, 3), np.float32) * np.float32([0.93, 0.89, 0.74])
    n = cv2.GaussianBlur(rng.standard_normal((ancho, largo)).astype(np.float32), (0, 0), 2)
    img *= (1 + 0.04 * n)[..., None]
    a = np.full((ancho, largo), 0.62, np.float32)
    for x in range(0, ancho):           # bordes dentados en los extremos
        j0 = int(rng.integers(0, 6))
        j1 = int(rng.integers(0, 6))
        a[x, :j0] = 0
        a[x, largo - j1:] = 0
    return Lam(_a_rgba(img, a), sr=0)


# =====================================================================================================================  AMBIENTE
def luz_lampara(lz, V, t, fx=None):
    """Pozo de luz cálida de una lámpara que sigue a la cámara con retraso + penumbra fría en los bordes."""
    lx, ly = V.cx - 260.0 / V.z, V.cy - 160.0 / V.z
    q, _ = V.proy(np.array([[lx, ly, 0.0]]))
    cx, cy = q[0]
    r = 1150 * (0.75 + 0.25 * min(V.z, 2.0))
    s = 4
    ys = (np.arange(H // s, dtype=np.float32) * s - cy) / r
    xs = (np.arange(W // s, dtype=np.float32) * s - cx) / r
    d2 = ys[:, None] ** 2 + xs[None, :] ** 2
    m = 0.36 + 0.82 * np.exp(-d2 * 1.15)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    if fx is not None:
        m *= fx
    lz *= m[..., None]
    lz *= np.float32([1.04, 0.98, 0.90])


_POLVO = None


def polvo_frente(lz, V, t, n=34, op=0.5):
    """Motas de polvo desenfocadas cerca de la cámara (parallax fuerte con el movimiento)."""
    global _POLVO
    if _POLVO is None:
        rng = np.random.default_rng(21)
        _POLVO = rng.random((n, 4))
    for i in range(n):
        a, b, c, d = _POLVO[i]
        prof = 0.15 + 0.55 * c            # fracción de la distancia de cámara
        x = (a * 2600 - 1300 + 30 * math.sin(t * 0.3 + i))
        y = (b * 1600 - 800 + 25 * t * (0.2 + d) * 3) % 1600 - 800
        P = np.array([[V.cx + x / V.z, V.cy + y / V.z, -V.Dd * prof]])
        q, zc = V.proy(P)
        if zc[0] < 5:
            continue
        qx, qy = q[0]
        if qx < -80 or qx > W + 80 or qy < -80 or qy > H + 80:
            continue
        r = 2.5 + 16 * (1 - prof)
        sz = int(r * 4) + 2
        yy, xx = np.mgrid[0:sz, 0:sz].astype(np.float32)
        gl = np.exp(-((xx - sz / 2) ** 2 + (yy - sz / 2) ** 2) / (2 * (r * 0.6) ** 2)) * op * (0.25 + 0.75 * d)
        x0, y0 = int(qx - sz / 2), int(qy - sz / 2)
        xs0, ys0, xs1, ys1 = max(x0, 0), max(y0, 0), min(x0 + sz, W), min(y0 + sz, H)
        if xs1 <= xs0 or ys1 <= ys0:
            continue
        gl = gl[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
        lz[ys0:ys1, xs0:xs1] += gl[..., None] * np.float32([1.0, 0.9, 0.7]) * 0.35


def desenfoque_movimiento(lz, V0, V1):
    """Desenfoque direccional si la cámara se mueve rápido (látigos)."""
    c = np.array([[V1.cx, V1.cy, 0.0]])
    q0, _ = V0.proy(c)
    q1, _ = V1.proy(c)
    dx, dy = q1[0] - q0[0]
    zr = abs(math.log(max(V1.z, 1e-3) / max(V0.z, 1e-3)))
    v = math.hypot(dx, dy)
    if v < 12 and zr < 0.02:
        return lz
    if v >= 12:
        L_ = int(min(90, v * 0.9)) | 1
        k = np.zeros((L_, L_), np.float32)
        cv2.line(k, (0, L_ // 2), (L_ - 1, L_ // 2), 1.0, 1)
        Mr = cv2.getRotationMatrix2D((L_ / 2 - 0.5, L_ / 2 - 0.5), math.degrees(math.atan2(dy, dx)), 1.0)
        k = cv2.warpAffine(k, Mr, (L_, L_))
        k /= k.sum() + 1e-6
        s = 2
        peq = cv2.resize(lz, (W // s, H // s), interpolation=cv2.INTER_AREA)
        k2 = cv2.resize(k, (max(3, L_ // s) | 1, max(3, L_ // s) | 1), interpolation=cv2.INTER_AREA)
        k2 /= k2.sum() + 1e-6
        b = cv2.filter2D(peq, -1, k2, borderType=cv2.BORDER_REFLECT)
        b = cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR)
        mix = clamp((v - 12) / 40.0)
        lz = lz * (1 - mix) + b * mix
    if zr >= 0.02:                      # zoom rápido: desenfoque radial barato
        mix = clamp((zr - 0.02) / 0.08) * 0.8
        acc = lz.copy()
        for f in (1.012, 1.024, 1.036):
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, f)
            acc += cv2.warpAffine(lz, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        lz = lz * (1 - mix) + acc / 4 * mix
    return lz.astype(np.float32)


# =====================================================================================================================  CUADRO
FONDO_EXTRA = []          # fn(lz, V, t) por debajo de las piezas (p. ej. papeles de fondo)
FRENTE = []               # fn(lz, V, t) por encima de todo (cuerdas desenfocadas, manos...)
LUZ_FX = []               # fn(t) -> factor de luz global (apagones, linterna)


def render_tablero(lz, t, dt=1 / 30):
    V = Vista(t)
    portal = None
    for p in PIEZAS:
        if p.portal is not None and p.visible(t) and p.llena_pantalla(t, V):
            portal = p
            break
    if portal is not None:
        x, y, z, s, rz, tx, ty, op = portal.pose(t)
        portal._portal(lz, V, t, x, y, z, s, rz, tx, ty, 1.0)
    else:
        dibujar_corcho(lz, V)
        for f in FONDO_EXTRA:
            f(lz, V, t)
        for capa in (0, 1, 2):
            for p in PIEZAS:
                if p.capa == capa and p.visible(t):
                    p.dibujar(lz, V, t)
            if capa == 1:
                for m in MARCAS:
                    m.dibujar(lz, V, t)
                for c in CONECTORES:
                    c.dibujar(lz, V, t)
                for h in HILOS:
                    h.dibujar(lz, V, t)
        fx = 1.0
        for f in LUZ_FX:
            fx = fx * f(t)
        luz_lampara(lz, V, t, None)
        if fx != 1.0:
            lz *= fx
    for f in FRENTE:
        f(lz, V, t)
    polvo_frente(lz, V, t)
    out = desenfoque_movimiento(lz, Vista(t - dt), V)
    if out is not lz:
        lz[:] = out
    return V


# =====================================================================================================================  EXTRAS
def oscura(L, k=0.72):
    """Copia oscurecida de una lámina (papeles de fondo que no compiten con las pistas)."""
    N = object.__new__(Lam)
    N.__dict__.update(L.__dict__)
    N.pm = (L.pm.astype(np.float32) * k + 0.5).astype(np.uint8)
    N._mip = {}
    return N


def centro_ventana(pz):
    x0, y0, x1, y1 = pz.ventana
    return pz.punto((x0 + x1) / 2 - pz.L.w / 2, (y0 + y1) / 2 - pz.L.h / 2)


def zoom_lleno(pz, margen=1.05):
    x0, y0, x1, y1 = pz.ventana
    return max(W / ((x1 - x0) * pz.s), H / ((y1 - y0) * pz.s)) * margen


class Lupa:
    """Lupa que se desliza sobre el tablero con AUMENTO REAL de lo que hay debajo (aro metálico, mango, reflejo).
    camino: [(t, x, y)] en el mundo; r = radio en px de pantalla; aum = aumento."""

    def __init__(self, camino, r=230, aum=1.9, t_in=None, t_out=None):
        self.cam = camino
        self.r, self.aum = r, aum
        self.t_in = camino[0][0] if t_in is None else t_in
        self.t_out = camino[-1][0] if t_out is None else t_out
        FRENTE.append(self.dibujar)

    def _pos(self, t):
        c = self.cam
        if t <= c[0][0]:
            return c[0][1:]
        for (ta, xa, ya), (tb, xb, yb) in zip(c, c[1:]):
            if t <= tb:
                u = sm((t - ta) / max(tb - ta, 1e-6))
                return xa + (xb - xa) * u, ya + (yb - ya) * u
        return c[-1][1:]

    def dibujar(self, lz, V, t):
        if t < self.t_in - 0.4 or t > self.t_out + 0.4:
            return
        op = sm(pr(t, self.t_in - 0.4, self.t_in)) * (1 - sm(pr(t, self.t_out, self.t_out + 0.4)))
        x, y = self._pos(t)
        q, _ = V.proy(np.array([[x, y, -40.0]]))
        cx, cy = q[0]
        cx += (1 - op) * 600
        cy += (1 - op) * 300
        r = self.r
        x0, y0, x1, y1 = int(cx - r - 40), int(cy - r - 40), int(cx + r + 40), int(cy + r + 40)
        if x1 < 0 or y1 < 0 or x0 > W or y0 > H:
            return
        # sombra de la lupa sobre el tablero
        sh = np.zeros((H, W), np.float32)
        cv2.circle(sh, (int(cx + 40), int(cy + 55)), int(r * 1.04), 1.0, -1, cv2.LINE_AA)
        sh = cv2.GaussianBlur(sh[max(y0, 0):min(y1 + 120, H), max(x0, 0):min(x1 + 120, W)], (0, 0), 18)
        lz[max(y0, 0):min(y1 + 120, H), max(x0, 0):min(x1 + 120, W)] *= (1 - 0.45 * op * sh)[..., None]
        # aumento: remapeo radial con leve distorsión de barril
        gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dx, dy = gx - cx, gy - cy
        d = np.sqrt(dx * dx + dy * dy) / r
        k = 1.0 / self.aum * (1 + 0.18 * d * d)
        mx, my = (cx + dx * k).astype(np.float32), (cy + dy * k).astype(np.float32)
        src = cv2.remap(lz, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        m = np.clip((1.0 - d) * r / 2.0, 0, 1) * op
        ys0, xs0 = max(y0, 0), max(x0, 0)
        ys1, xs1 = min(y1, H), min(x1, W)
        sub = (slice(ys0 - y0, ys1 - y0), slice(xs0 - x0, xs1 - x0))
        reg = lz[ys0:ys1, xs0:xs1]
        mm = m[sub][..., None]
        reflejo = np.clip(1 - np.hypot(dx + r * 0.35, dy + r * 0.40) / (r * 0.55), 0, 1)[sub][..., None] ** 2 * 0.18
        reg[:] = reg * (1 - mm) + (src[sub] * 1.06 + reflejo) * mm
        # aro y mango
        aro = np.clip(1 - np.abs(d - 1.0) * r / 9.0, 0, 1)[sub] * op
        col = np.float32([0.62, 0.60, 0.55]) * (0.75 + 0.35 * np.clip(-dy[sub] / r, -1, 1))[..., None]
        reg[:] = reg * (1 - aro[..., None]) + col * aro[..., None]
        ang = math.radians(40)
        a = (cx + r * 1.02 * math.cos(ang), cy + r * 1.02 * math.sin(ang))
        b = (cx + r * 2.1 * math.cos(ang), cy + r * 2.1 * math.sin(ang))
        trazo(lz, np.array([a, b]), (0.20, 0.13, 0.08), r * 0.20, op, np.array([(a[0] + 30, a[1] + 45), (b[0] + 30, b[1] + 45)]), 0.4)


class Linterna:
    """Oscuridad con un haz de linterna (círculo cálido) que sigue un camino en PANTALLA [(t, x, y, r)] entre t0 y t1."""

    def __init__(self, camino, t0, t1, amb=0.10, fundido=0.6):
        self.cam, self.t0, self.t1, self.amb, self.fun = camino, t0, t1, amb, fundido
        FRENTE.insert(0, self.dibujar)

    def _pos(self, t):
        c = self.cam
        if t <= c[0][0]:
            return c[0][1:]
        for a, b in zip(c, c[1:]):
            if t <= b[0]:
                u = sm((t - a[0]) / max(b[0] - a[0], 1e-6))
                return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
        return c[-1][1:]

    def dibujar(self, lz, V, t):
        if t < self.t0 or t > self.t1 + self.fun:
            return
        f = 1 - sm(pr(t, self.t1, self.t1 + self.fun))
        x, y, r = self._pos(t)
        parp = 1.0 - 0.25 * (math.sin(t * 37) > 0.97)
        s = 4
        ys = (np.arange(H // s, dtype=np.float32) * s - y) / r
        xs = (np.arange(W // s, dtype=np.float32) * s - x) / r
        d2 = ys[:, None] ** 2 + xs[None, :] ** 2
        m = self.amb + (1.25 - self.amb) * np.exp(-d2 ** 1.6 * 1.4) * parp
        m = cv2.resize(m.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
        m = 1 - f * (1 - m)
        lz *= m[..., None]
