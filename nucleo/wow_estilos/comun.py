# -*- coding: utf-8 -*-
"""Piezas comunes de los motores de estilo: tiempos con las marcas de la voz, cámara que encuadra los puntos vistos de un
mapa, colocación de rótulos/fotos sin choques (lado fijo, regla del 11-nov-2026), carga de imágenes («ico:» = ícono de
Wowhead) y salida BGRA para el motor (nucleo/secuencia_fx.py: fn(dt, dur, marcas) -> BGRA)."""
import math
import os

import numpy as np
from PIL import Image

W, H = 1920, 1080


def cl(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else float(x)


def seg(t, a, b):
    return cl((t - a) / (b - a)) if b > a else float(t >= a)


def eo(u):
    u = cl(u)
    return 1 - (1 - u) ** 3


def eio(u):
    u = cl(u)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def mk(marcas, i, defecto):
    return marcas[i] if i < len(marcas) else defecto


def tiempos(marcas, n, ini=1.0, paso=2.2, minimo=0.0):
    """Segundo de cada paso (n + 1 valores: el extra es la marca de remate); nunca antes de `minimo` ni desordenados."""
    out, prev = [], minimo
    for i in range(n + 1):
        v = max(mk(marcas, i, ini + i * paso), minimo)
        v = max(v, prev)
        out.append(v)
        prev = v
    return out


def rgba(fuente_img, tam=None):
    """PIL RGBA de una ruta local o de «ico:<ícono de Wowhead>» (mg_wow.icono). tam = lado máximo opcional."""
    s = str(fuente_img)
    if s.startswith("ico:"):
        import mg_wow
        im = mg_wow.icono(s[4:], tam or 256).convert("RGBA")
    else:
        if not os.path.exists(s):
            raise SystemExit(f"mg_wow_estilos: falta la imagen {s}")
        im = Image.open(s).convert("RGBA")
    return im


def es_icono(fuente_img):
    """Íconos de objeto (o_*.png de 56 px, «ico:»): se muestran enteros y sin recorte de cara."""
    s = str(fuente_img)
    return s.startswith("ico:") or os.path.basename(s).startswith("o_")


def bgra_premul(c):
    """Lienzo premultiplicado float (h, w, 4) en 0..1 -> BGRA uint8 recto para el motor."""
    a = np.clip(c[..., 3:4], 0, 1)
    rgb = np.clip(c[..., :3] / np.maximum(a, 1e-4), 0, 1)
    out = np.empty(c.shape[:2] + (4,), np.uint8)
    out[..., 0] = (rgb[..., 2] * 255 + .5).astype(np.uint8)
    out[..., 1] = (rgb[..., 1] * 255 + .5).astype(np.uint8)
    out[..., 2] = (rgb[..., 0] * 255 + .5).astype(np.uint8)
    out[..., 3] = (a[..., 0] * 255 + .5).astype(np.uint8)
    return out


def bgra_opaco(rgb01):
    """Cuadro RGB float 0..1 a cuadro entero BGRA opaco (mapas: FX `pantalla`)."""
    f = (np.clip(rgb01, 0, 1) * 255 + .5).astype(np.uint8)
    return np.dstack([f[..., 2], f[..., 1], f[..., 0], np.full(f.shape[:2], 255, np.uint8)])


VACIO = np.zeros((2, 2, 4), np.uint8)


# ------------------------------------------------------------------ cámara de mapa (como mg_wow.ruta)
def camara(P, vistos, bw, bh, vw, vh, zmin=1.0, zmax=1.6):
    """(cx, cy, s): centro en px del mapa y escala (px de pantalla por px de mapa) que encuadra los pasos vistos
    dentro de una ventana vw x vh sin salirse del mapa."""
    s_min = max(vw / bw, vh / bh)
    if not vistos:
        s, cx, cy = s_min * zmin, bw / 2, bh / 2
    else:
        xs, ys = [P[i][0] for i in vistos], [P[i][1] for i in vistos]
        mw, mh = (max(xs) - min(xs)) + bw * .30, (max(ys) - min(ys)) + bh * .34
        s = max(s_min * zmin, min(s_min * zmax, vw / mw, vh / mh))
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    hw, hh = vw / s / 2, vh / s / 2
    return min(max(cx, hw), bw - hw), min(max(cy, hh), bh - hh), s


def camara_en(P, tk, dt, dur, bw, bh, vw, vh, zmin, zmax, mover=1.1, empuje=.03):
    vistos = [i for i in range(len(P)) if dt >= tk[i]]
    cam = camara(P, vistos, bw, bh, vw, vh, zmin, zmax)
    if vistos:
        u = eio((dt - tk[vistos[-1]]) / mover)
        cam = tuple(a + (b - a) * u for a, b in zip(camara(P, vistos[:-1], bw, bh, vw, vh, zmin, zmax), cam))
    cx, cy, s = cam
    return cx, cy, s * (1 + empuje * dt / max(dur, 1)), vistos


# ------------------------------------------------------------------ colocación sin choques
def choque(caja, ocup):
    return sum(max(0, min(caja[2], o[2]) - max(caja[0], o[0])) * max(0, min(caja[3], o[3]) - max(caja[1], o[1])) for o in ocup)


def encajar(x, y, w, h, lim):
    x0, y0, x1, y1 = lim
    return min(max(x, x0), x1 - w), min(max(y, y0), y1 - h)


def cands_alrededor(x, y, w, h, off):
    """Esquinas superiores izquierdas candidatas: derecha, izquierda, abajo, arriba y las 4 diagonales."""
    return [(x + off, y - h / 2), (x - off - w, y - h / 2), (x - w / 2, y + off), (x - w / 2, y - off - h),
            (x + off, y - h - 10), (x - off - w, y - h - 10), (x + off, y + 10), (x - off - w, y + 10)]


def mejor_lado(cands, w, h, lim, ocup, fuera=None):
    """Índice del candidato con menos choque (tras encajarlo en `lim`); `fuera` penaliza lo que se encaja lejos."""
    mejor = None
    for k, (rx, ry) in enumerate(cands):
        ex, ey = encajar(rx, ry, w, h, lim)
        c = choque((ex, ey, ex + w, ey + h), ocup) + (60 if fuera is None else fuera) * (abs(ex - rx) + abs(ey - ry))
        if mejor is None or c < mejor[0]:
            mejor = (c, k)
        if c == 0:
            break
    return mejor[1]


def partir(texto, ancho, medir):
    """Parte un texto en líneas que quepan en `ancho` según medir(cadena) -> px."""
    pal, lineas, act = texto.split(), [], ""
    for p in pal:
        prueba = (act + " " + p).strip()
        if act and medir(prueba) > ancho:
            lineas.append(act)
            act = p
        else:
            act = prueba
    if act:
        lineas.append(act)
    return lineas or [""]


def colocador(P, tk, bw, bh, vw, vh, zmin, zmax, ox, oy, cajas_fijas, tam_rot, tam_foto, r_pin, off_rot, off_foto, lim):
    """Elige UNA vez el lado de cada rótulo y de cada foto, con la cámara ya asentada en su paso (lado fijo, 11-nov).
    tam_rot[i] / tam_foto[i] = (w, h) o None; devuelve (lados_rot, lados_foto)."""
    lr, lf = {}, {}
    for i in range(len(P)):
        cx, cy, s = camara(P, list(range(i + 1)), bw, bh, vw, vh, zmin, zmax)

        def pt(p):
            return ox + vw / 2 + s * (p[0] - cx), oy + vh / 2 + s * (p[1] - cy)
        ocup = list(cajas_fijas) + [(x - r_pin(j), y - r_pin(j), x + r_pin(j), y + r_pin(j))
                                    for j in range(i + 1) for x, y in [pt(P[j])]]
        for j in range(1, i + 1):                      # el trazo de la ruta tampoco se tapa
            (ax, ay), (bx, by) = pt(P[j - 1]), pt(P[j])
            for u in np.linspace(.15, .85, 8):
                x, y = ax + (bx - ax) * u, ay + (by - ay) * u
                ocup.append((x - 22, y - 22, x + 22, y + 22))
        for j in sorted(range(i + 1), key=lambda j: -j):
            if tam_rot[j] is None:
                continue
            x, y = pt(P[j])
            w, h = tam_rot[j]
            cands = cands_alrededor(x, y, w, h, off_rot(j))[:4]
            if j not in lr:
                lr[j] = mejor_lado(cands, w, h, lim, ocup)
            rx, ry = encajar(*cands[lr[j]], w, h, lim)
            ocup.append((rx, ry, rx + w, ry + h))
        if tam_foto[i] is not None:
            x, y = pt(P[i])
            w, h = tam_foto[i]
            lf[i] = mejor_lado(cands_alrededor(x, y, w, h, off_foto(i)), w, h, lim, ocup)
    return lr, lf


def caja_en(x, y, w, h, off, lado, lim, solo4=False):
    c = cands_alrededor(x, y, w, h, off)
    rx, ry = encajar(*c[lado], w, h, lim)
    return rx, ry


def hash_semilla(*cosas):
    import hashlib
    return int(hashlib.md5("|".join(map(str, cosas)).encode("utf-8")).hexdigest()[:6], 16)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
