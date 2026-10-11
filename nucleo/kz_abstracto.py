# -*- coding: utf-8 -*-
"""Conceptos abstractos del estilo Kurzgesagt (referencia: «This Woman Cured Her Cancer…»): ideas que no se pueden filmar se dibujan con formas,
color, partículas y texto, no con ilustraciones literales.

  titulo_textura(lz, texto, x, y, px, t, ...)   tipografía gigante rellena con un patrón animado (como «VIRO THERAPY»).
  petalos(lz, t, t0, origen, ...)               ráfaga de pétalos/partículas que sale de un punto (algo que se fragmenta, florece o se disuelve).
  corriente(lz, t, ...)                          partículas que siguen una trayectoria curva (ejércitos, flujo de gente, migración como «batalla de células»).
  halo_punto(lz, x, y, r, t, ...)                punto oscuro con halo de color que late (el «tumor» de la referencia: un concepto, no un dibujo).
  barrido(lz, t, t0, dur, color, ...)            ola de color que cruza la pantalla (transición/tratamiento «quimioterapia»).
  grano(img, t)                                  grano fino 2-3 % sobre todo el cuadro.
  medallon_tiempo(lz, x, y, r, t, ...)           círculo con borde y línea de tiempo con hitos (semanas/años) debajo.
  contador_atras(...)                            año que retrocede girando como un tragamonedas (tiempo que se rebobina).
"""
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

import plano as P
from motor import W, H, SS, fuente, elipse, circulo, rect_red, catmull, h01, prog, smooth, e_back, e_out, e_inout, ruido1


# ---------------------------------------------------------------------------------------------------- tipografía con textura
_CACHE_TXT = {}


def _mascara_texto(texto, px, nombre="geo_x"):
    clave = (texto, px, nombre)
    if clave not in _CACHE_TXT:
        f = fuente(nombre, int(px * SS))
        im = Image.new("L", (10, 10))
        d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = d.textbbox((0, 0), texto, font=f)
        pad = int(px * SS * 0.10)
        w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
        im = Image.new("L", (w, h), 0)
        ImageDraw.Draw(im).text((pad - x0, pad - y0), texto, font=f, fill=255)
        _CACHE_TXT[clave] = np.asarray(im)
    return _CACHE_TXT[clave]


def _patron_flores(w, h, paleta, seed=3, n=None):
    """Patrón de pétalos, puntos y brotes sobre un fondo plano (para rellenar tipografía)."""
    rng = np.random.RandomState(seed)
    img = np.zeros((h, w, 3), np.uint8)
    img[:] = paleta[0]
    n = n or max(40, (w * h) // 2600)
    for i in range(n):
        cx, cy = rng.randint(0, w), rng.randint(0, h)
        r = rng.randint(int(h * 0.05), int(h * 0.16))
        col = paleta[1 + rng.randint(0, len(paleta) - 1)]
        tipo = rng.randint(0, 3)
        for dx in (-w, 0, w):                                      # que el patrón sea continuo al desplazarlo
            if tipo == 0:                                          # flor de cinco pétalos
                for k in range(5):
                    a = rng.rand() * 0 + k * 2 * math.pi / 5 + i
                    cv2.ellipse(img, (cx + dx + int(math.cos(a) * r * 0.9), cy + int(math.sin(a) * r * 0.9)), (int(r * 0.7), int(r * 0.42)), math.degrees(a), 0, 360, col, -1, cv2.LINE_AA)
                cv2.circle(img, (cx + dx, cy), int(r * 0.45), paleta[0], -1, cv2.LINE_AA)
            elif tipo == 1:                                        # gota/pétalo
                cv2.ellipse(img, (cx + dx, cy), (int(r * 1.1), int(r * 0.55)), rng.rand() * 180, 0, 360, col, -1, cv2.LINE_AA)
            else:                                                  # punto
                cv2.circle(img, (cx + dx, cy), int(r * 0.5), col, -1, cv2.LINE_AA)
    return img


def titulo_textura(lz, texto, x, y, px, t, paleta=((108, 40, 150), (255, 150, 44), (255, 204, 70), (236, 70, 140), (90, 210, 190)), k=1.0, alfa=1.0, seed=3,
                   vel=22.0, sombra=(14, 6, 40), ancla=(0.5, 0.5), capa=2, nombre="geo_x"):
    """Texto grande relleno con un patrón de flores que se desliza lentamente. (x, y) = centro; px = alto de letra."""
    if alfa <= 0.005:
        return
    m = _mascara_texto(texto, px, nombre)
    h, w = m.shape
    clave = ("pat", texto, px, paleta, seed)
    if clave not in _CACHE_TXT:
        _CACHE_TXT[clave] = _patron_flores(w, h, paleta, seed)
    pat = _CACHE_TXT[clave]
    off = int((t * vel * SS) % w)
    pat = np.roll(pat, off, axis=1)
    a = m.astype(np.float32) / 255.0
    rgba = np.dstack([(pat.astype(np.float32) * a[..., None]), m.astype(np.float32)]).round().astype(np.uint8)
    if sombra is not None:                                          # sombra suave desplazada (sin contorno)
        sh = cv2.GaussianBlur(m, (0, 0), px * SS * 0.05)
        sh = np.dstack([np.zeros_like(sh), np.zeros_like(sh), np.zeros_like(sh), (sh * 0.45).astype(np.uint8)])
        lz.pegar(sh, x + px * 0.05, y + px * 0.08, k=k / SS, ancla=ancla, alfa=alfa, capa=capa)
    lz.pegar(rgba, x, y, k=k / SS, ancla=ancla, alfa=alfa, capa=capa)


# ---------------------------------------------------------------------------------------------------- partículas
def _petalo_pts(cx, cy, L, W_, ang):
    u = np.linspace(0, 1, 9)
    lado = W_ * np.sin(math.pi * u) ** 0.8
    ca, sa = math.cos(ang), math.sin(ang)
    P1 = [(cx + ca * L * v - sa * w_, cy + sa * L * v + ca * w_) for v, w_ in zip(u, lado)]
    P2 = [(cx + ca * L * v + sa * w_, cy + sa * L * v - ca * w_) for v, w_ in zip(u[::-1], lado[::-1])]
    return np.array(P1 + P2)


def petalos(lz, t, t0, origen, n=24, dur=2.6, color=((255, 150, 44), (255, 204, 70), (236, 70, 140)), vel=(160, 420), g=-80.0, spread=(-math.pi, 0.0), tam=(10, 22), seed=1, capa=2, alfa=1.0, viento=40.0):
    """Ráfaga de pétalos desde `origen` (px). Todo es función de t. spread = rango de ángulos de salida (rad, 0 = derecha, -pi/2 = arriba)."""
    u = t - t0
    if u < 0 or u > dur:
        return
    ox, oy = origen
    for i in range(n):
        a = spread[0] + (spread[1] - spread[0]) * h01(seed, i, 1)
        v = vel[0] + (vel[1] - vel[0]) * h01(seed, i, 2)
        frena = 1 - 0.35 * u / dur
        dx = math.cos(a) * v * u * frena + viento * u * u * (h01(seed, i, 5) - 0.3)
        dy = math.sin(a) * v * u * frena + 70.0 * u * u * (0.5 + h01(seed, i, 6))      # al final caen un poco (aire)
        L = (tam[0] + (tam[1] - tam[0]) * h01(seed, i, 3)) * (1 - 0.3 * u / dur)
        ang = h01(seed, i, 4) * 6.28 + u * (2.0 + 4.0 * h01(seed, i, 7)) * (1 if i % 2 else -1)
        fade = min(1.0, u / 0.12) * (1 - smooth(prog(u, dur * 0.55, dur)))
        col = color[i % len(color)]
        lz.relleno(_petalo_pts(ox + dx, oy + dy, L, L * 0.42, ang), col, alfa=fade * alfa, capa=capa)
        lz.relleno(_petalo_pts(ox + dx, oy + dy, L * 0.9, L * 0.16, ang), P.aclarar(col, 0.3), alfa=fade * alfa * 0.8, capa=capa)


def corriente(lz, t, trayecto, n=40, ancho=26.0, vel=0.22, color=((255, 120, 90), (255, 200, 90)), r=(4.0, 8.0), seed=1, capa=1, alfa=1.0, estela=0.0):
    """n partículas que avanzan por la curva `trayecto` (puntos en px; se suaviza con Catmull-Rom). Cada una con su desfase y su carril (ancho en px)."""
    Q = catmull(np.asarray(trayecto, float), 12, False)
    seg = np.hypot(*np.diff(Q, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    nQ = len(Q)
    for i in range(n):
        u = (t * vel * (0.85 + 0.3 * h01(seed, i, 1)) + h01(seed, i, 2)) % 1.0
        k = min(nQ - 2, int(u * (nQ - 1)))
        f = u * (nQ - 1) - k
        p = Q[k] * (1 - f) + Q[k + 1] * f
        tan = Q[k + 1] - Q[k]
        tan = tan / (np.hypot(*tan) + 1e-6)
        nor = np.array([-tan[1], tan[0]])
        lane = (h01(seed, i, 3) - 0.5) * 2 * ancho + 3.0 * math.sin(t * 3 + i)
        pos = p + nor * lane
        rr = r[0] + (r[1] - r[0]) * h01(seed, i, 4)
        c = color[i % len(color)]
        a = alfa * min(1.0, u / 0.06) * min(1.0, (1 - u) / 0.06)
        if estela > 0:
            for j in range(3):
                lz.relleno(circulo(pos[0] - tan[0] * rr * 2.2 * (j + 1), pos[1] - tan[1] * rr * 2.2 * (j + 1), rr * (1 - 0.22 * (j + 1)), 10), c, alfa=a * 0.35 / (j + 1), capa=capa)
        lz.relleno(circulo(pos[0], pos[1], rr, 12), c, alfa=a, capa=capa)


def halo_punto(lz, x, y, r, t, color=(60, 220, 210), nucleo=(10, 4, 20), latido=0.12, capa=2, alfa=1.0, seed=0):
    """Punto oscuro con halo de color que late: el concepto «algo ahí dentro» sin dibujar el objeto."""
    p = 1 + latido * math.sin(t * 3.0 + seed)
    lz.halo(x, y, r * 2.6 * p, color, alfa=0.55 * alfa, dureza=1.2, capa=capa)
    lz.relleno(circulo(x, y, r * 1.35 * p, 28), color, alfa=0.9 * alfa, capa=capa)
    lz.relleno(circulo(x, y, r * p, 28), nucleo, alfa=alfa, capa=capa)


def barrido(lz, t, t0, dur=0.9, color=(255, 255, 255), ang=0.0, alfa=0.9, ancho=0.45, capa=2):
    """Ola de color que cruza la pantalla con borde ondulado (sin dejar nada detrás salvo la luz del frente)."""
    u = prog(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return
    ca, sa = math.cos(ang), math.sin(ang)
    L = abs(W * ca) + abs(H * sa)
    pos = -ancho * L + (L * (1 + ancho)) * e_inout(u)
    n = 30
    s = np.linspace(-0.7 * math.hypot(W, H), 0.7 * math.hypot(W, H), n)
    cx, cy = W / 2, H / 2
    for k, (off, a_) in enumerate(((0.0, 1.0), (-ancho * L * 0.5, 0.5), (-ancho * L, 0.25))):
        borde = [(cx + ca * (pos + off - L / 2 + 25 * math.sin(si * 0.013 + t * 6 + k)) - sa * si, cy + sa * (pos + off - L / 2 + 25 * math.sin(si * 0.013 + t * 6 + k)) + ca * si) for si in s]
        atras = [(cx + ca * (-L) - sa * si, cy + sa * (-L) + ca * si) for si in s[::-1]]
        lz.relleno(np.array(borde + atras), color, alfa=alfa * a_ * 0.5, capa=capa)


def grano(img, t, fuerza=0.025):
    """Grano fino sobre el cuadro (img float32 HxWx3 en [0,1])."""
    rng = np.random.RandomState(int(t * 12) % 97)
    g = rng.randn(H // 2, W // 2).astype(np.float32)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_NEAREST)
    return img * (1 + fuerza * g[..., None])


def contador_atras(lz, x, y, valor, px=120, color=(255, 255, 255), k=1.0, alfa=1.0, fuente_="geo_x"):
    """Cifra grande centrada (entero) con sombra suave; el que llama anima `valor` (p. ej. 2026 -> 1541 con e_inout)."""
    if alfa <= 0.01:
        return
    lz.texto(str(int(valor)), x + 3, y + 5, px, fuente_, color=(20, 8, 50), borde=None, k=k, alfa=0.35 * alfa, capa=2, temblor=0.0)
    lz.texto(str(int(valor)), x, y, px, fuente_, color=color, borde=None, k=k, alfa=alfa, capa=2, temblor=0.0)


def medallon_tiempo(lz, x, y, r, t, hitos, actual=0.0, color_borde=(255, 200, 70), ancho=900, y_linea=None, alfa=1.0):
    """Línea de tiempo horizontal con hitos [(etiqueta, ...)] y un medallón circular que se desliza al hito `actual` (fracción 0..n-1)."""
    y_linea = y if y_linea is None else y_linea
    n = len(hitos)
    xs = [x - ancho / 2 + ancho * i / max(1, n - 1) for i in range(n)]
    lz.relleno(rect_red(xs[0] - 20, y_linea + r + 40, ancho + 40, 6, 3), (255, 255, 255), alfa=0.35 * alfa, capa=2)
    for i, (xi, h) in enumerate(zip(xs, hitos)):
        a = float(np.clip(1 - abs(actual - i), 0.35, 1.0))
        lz.relleno(rect_red(xi - 2, y_linea + r + 26, 4, 36, 2), (255, 255, 255), alfa=0.6 * a * alfa, capa=2)
        P.rotulo(lz, xi, y_linea + r + 96, str(h), px=34, alfa=a * alfa)
    cx = np.interp(actual, range(n), xs)
    lz.halo(cx, y_linea, r * 1.7, color_borde, alfa=0.35 * alfa, capa=2)
    return float(cx), float(y_linea)
