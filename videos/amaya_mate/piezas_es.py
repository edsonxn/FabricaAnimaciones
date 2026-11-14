# -*- coding: utf-8 -*-
"""Piezas pintadas del video 2 de Amaya (ESPAÑOL): fotos reales de SU cuaderno como polaroid, sílabas en fichas con la tónica
encerrada como en su cuaderno, manos que aplauden, camión de reversa, sopa de letras L·S·A·D·F, la carta que se arma por partes,
película contra clip, hot cake pegado en el techo, flecha de «pregúntale al verbo»."""
import math
import os

import cv2
import numpy as np

from acuarela import (H, W, TINTA, curva, e_back, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave)
from comun import cache
from kit_amaya import AMAR, AZUL, CAFE, CREMA, DORADO, GRIS, MORADO, ROJO, VERDE, entra, letrero, tarjeta
import personajes_ia as PI

AQUI = os.path.dirname(os.path.abspath(__file__))
ROSA_M = rgb("e8559a")          # el plumón rosa de su cuaderno
TURQ = rgb("2fb5a0")            # el plumón turquesa
PIEL = rgb("f4cfae")
PIEL_O = rgb("d9a77f")


def hoja(nombre, alto=None):
    """Foto real del cuaderno (propios/cuaderno/<nombre>.jpg) como float RGB 0..1, opcionalmente reescalada a `alto`."""
    def f():
        im = cv2.imread(os.path.join(AQUI, "propios", "cuaderno", nombre + ".jpg"))
        if alto:
            im = cv2.resize(im, (int(im.shape[1] * alto / im.shape[0]), alto), interpolation=cv2.INTER_AREA)
        return im[..., ::-1].astype(np.float32) / 255
    return cache(("hoja", nombre, alto), f)


def polaroid(im, nombre, x, y, esc, t, rot=0.0, seed=0, alto=None, alfa=1.0, cinta=True):
    """La foto de su cuaderno pegada con cinta adhesiva."""
    if esc <= 0.02:
        return
    caja = PI.pegar(im, hoja(nombre, alto), x, y, esc, rot, alfa=alfa, marco=16, t=t, seed=seed)
    if cinta and caja is not None:
        y0 = caja[:, 1].min()
        forma(im, rrect(x, y0 + 4 * esc, 130 * esc, 38 * esc, 4, rot - 0.06), rgb("f3e7b0"), t, seed + 9, tinta=0, alfa=0.75 * alfa)


# ------------------------------------------------------------ sílabas
def ficha(im, txt, x, y, px, t, col=CREMA, seed=0, esc=1.0, fuerte=0.0, txt_col=TINTA, rot=0.0):
    """Una sílaba en su ficha. fuerte (0..1) = la tónica: crece, se vuelve roja y la encierra un círculo de plumón rosa."""
    if esc <= 0.02:
        return
    s = esc * (1 + 0.28 * fuerte)
    w = (len(txt) * px * 0.62 + px * 0.9) * s
    h = px * 1.45 * s
    yy = y - 22 * fuerte
    tarjeta(im, x, yy, w, h, t, col if fuerte < 0.5 else rgb("fde0dc"), seed, rot=rot)
    rotulo(im, txt, x, yy + 3 * s, px * s, ROJO if fuerte > 0.5 else txt_col, t, seed=seed + 3, tinta=False, rot=rot)
    if fuerte > 0.02:
        n = max(3, int(64 * min(1, fuerte * 1.4)))
        a = np.linspace(-0.4, -0.4 + 2 * math.pi * 1.05 * min(1, fuerte * 1.4), n)
        linea(im, np.stack([x + (w * 0.62) * np.cos(a), yy + (h * 0.72) * np.sin(a)], 1), 6 * s, ROSA_M, seed=seed + 5, t=t,
              punta=False)


def palabra(im, sils, x, y, px, t, tonica=-1, t_ap=-9.0, t_ton=1e9, seed=0, col=CREMA, gap=None, paso=0.12, etiquetas=None,
            t_eti=1e9):
    """Fila de fichas («es - cue - la») que entran una a una desde t_ap; la tónica se enciende en t_ton.
    etiquetas = textos bajo cada ficha (p. ej. ANTEPENÚLTIMA/PENÚLTIMA/ÚLTIMA), que aparecen de derecha a izquierda desde t_eti.
    Devuelve las x de cada ficha."""
    ws = [(len(s_) * px * 0.62 + px * 0.9) for s_ in sils]
    gap = px * 0.7 if gap is None else gap
    tot = sum(ws) + gap * (len(sils) - 1)
    xs, cx = [], x - tot / 2
    for w_ in ws:
        xs.append(cx + w_ / 2)
        cx += w_ + gap
    for k, (s_, xk) in enumerate(zip(sils, xs)):
        e = entra(t, t_ap[k] if isinstance(t_ap, (list, tuple)) else t_ap + paso * k)
        f = suave(pr(t, t_ton - 0.1, t_ton + 0.3)) if k == tonica else 0.0
        if k > 0 and e > 0.5:
            linea(im, [(xk - ws[k] / 2 - gap * 0.7, y), (xk - ws[k] / 2 - gap * 0.3, y)], 5, seed=seed + 40 + k, t=t)
        ficha(im, s_, xk, y, px, t, col, seed + 7 * k, esc=e, fuerte=f)
    if etiquetas:
        n = len(sils)
        for j, et in enumerate(etiquetas):
            k = n - len(etiquetas) + j
            ee = entra(t, t_eti + 0.35 * (len(etiquetas) - 1 - j))
            if ee > 0.02:
                linea(im, [(xs[k], y + px * 1.1), (xs[k], y + px * 1.1 + 40 * ee)], 4, GRIS, seed=seed + 60 + j, t=t)
                rotulo(im, et, xs[k], y + px * 1.1 + 78, 40 * ee + 1, MORADO, t, seed=seed + 70 + j, tinta=False)
    return xs


def mano(im, x, y, s, t, lado, seed=0):
    """Mano abierta en acuarela (palma + 4 dedos + pulgar), vista de canto; lado = -1 izquierda, +1 derecha."""
    forma(im, elipse(x, y, 46 * s, 62 * s, 0.12 * lado), PIEL, t, seed, tinta=3.5 * s)
    for k in range(4):
        forma(im, elipse(x + (-24 + 16 * k) * s, y - 70 * s - 6 * s * (1 - abs(k - 1.5) / 1.5), 9 * s, 24 * s), PIEL, t,
              seed + 1 + k, tinta=3 * s)
    forma(im, elipse(x - lado * 48 * s, y - 6 * s, 13 * s, 26 * s, -0.7 * lado), PIEL, t, seed + 6, tinta=3 * s)
    lavado(im, elipse(x + lado * 14 * s, y + 18 * s, 28 * s, 30 * s), PIEL_O, 0.35, seed + 7)


def aplauso(im, x, y, s, t, golpes, seed=0):
    """Dos manos que se juntan en cada instante de `golpes`, con rayitas de impacto."""
    d = min([abs(t - g) for g in golpes] + [9])
    junta = math.exp(-(d / 0.11) ** 2)
    sep = (120 - 85 * junta) * s
    mano(im, x - sep / 2 - 30 * s, y, s, t, -1, seed)
    mano(im, x + sep / 2 + 30 * s, y, s, t, 1, seed + 20)
    if junta > 0.4:
        for k in range(6):
            a = -math.pi / 2 + (k - 2.5) * 0.45
            r0, r1 = 120 * s, (150 + 50 * junta) * s
            linea(im, [(x + r0 * math.cos(a), y - 30 * s + r0 * math.sin(a)), (x + r1 * math.cos(a), y - 30 * s + r1 * math.sin(a))],
                  6 * s, AMAR, seed=seed + 40 + k, t=t)


# ------------------------------------------------------------ cosas
def camion(im, x, y, s, t, seed=0, bip=0.0):
    """Camión de volteo visto de lado (mira a la derecha y va de reversa hacia la izquierda); bip (0..1) = «¡BIP!» que late."""
    forma(im, rrect(x - 60 * s, y - 70 * s, 260 * s, 120 * s, 14 * s), rgb("f2b23c"), t, seed, tinta=4 * s)
    forma(im, rrect(x + 125 * s, y - 55 * s, 110 * s, 150 * s, 18 * s), rgb("e35d4a"), t, seed + 1, tinta=4 * s)
    forma(im, rrect(x + 140 * s, y - 80 * s, 60 * s, 50 * s, 8 * s), rgb("cfe8f3"), t, seed + 2, tinta=3 * s)
    forma(im, rrect(x + 20 * s, y + 10 * s, 380 * s, 34 * s, 8 * s), rgb("5a5a62"), t, seed + 3, tinta=3 * s)
    gira = -t * 5
    for k, xr in enumerate((-120, 20, 150)):
        forma(im, elipse(x + xr * s, y + 40 * s, 36 * s, 36 * s), rgb("2f2f36"), t, seed + 5 + k, tinta=3 * s)
        forma(im, elipse(x + xr * s, y + 40 * s, 14 * s, 14 * s), GRIS, t, seed + 9 + k, tinta=2 * s)
        linea(im, [(x + xr * s, y + 40 * s), (x + xr * s + 14 * s * math.cos(gira + k), y + 40 * s + 14 * s * math.sin(gira + k))],
              3 * s, seed=seed + 12 + k, t=t)
    if bip > 0.02:
        late = 1 + 0.12 * abs(math.sin(t * 9))
        rotulo(im, "¡BIP!", x - 250 * s, y - 170 * s, 70 * s * late * bip, ROJO, t, seed=seed + 20, rot=-0.15)
        rotulo(im, "¡BIP!", x - 60 * s, y - 230 * s, 56 * s * late * bip, ROJO, t, seed=seed + 21, rot=0.1)


def sopa(im, x, y, s, t, letras="LSADF", sale=1.0, seed=0, vapor_=True):
    """Plato hondo de sopa (caldo naranja) del que suben las letras L, S, A, D, F (sale 0..1 = cuántas han subido)."""
    forma(im, elipse(x, y + 70 * s, 260 * s, 40 * s), rgb("e9e2d4"), t, seed, tinta=3 * s)
    forma(im, np.array([(x - 250 * s, y - 10 * s), (x + 250 * s, y - 10 * s), (x + 190 * s, y + 90 * s), (x - 190 * s, y + 90 * s)],
                       np.float32), rgb("4f8fc8"), t, seed + 1, tinta=4 * s, luz=(rgb("ffffff"), -30, -10, 0.25))
    forma(im, elipse(x, y - 10 * s, 250 * s, 46 * s), rgb("4f8fc8"), t, seed + 2, tinta=4 * s)
    forma(im, elipse(x, y - 8 * s, 222 * s, 36 * s), rgb("f2a13c"), t, seed + 3, tinta=2 * s)
    for k in range(9):
        forma(im, elipse(x - 170 * s + 42 * k * s, y - 8 * s + 10 * s * math.sin(k * 2.1), 8 * s, 5 * s), rgb("fbe7b0"), t,
              seed + 30 + k, tinta=0)
    if vapor_:
        from utileria import vapor
        vapor(im, x, y - 60 * s, 1.2 * s, t, n=3, seed=seed + 50)
    for k, c in enumerate(letras):
        u = clamp01(sale * len(letras) - k)
        if u <= 0:
            continue
        yy = y - 10 * s - 200 * s * e_out(u) + 8 * math.sin(t * 3 + k)
        xx = x + (k - (len(letras) - 1) / 2) * 105 * s
        rotulo(im, c, xx, yy, 92 * s * (0.4 + 0.6 * u), rgb("f2a13c"), t, seed=seed + 60 + k)


def clamp01(v):
    return max(0.0, min(1.0, v))


def tira(im, x, y, w, h, t, n=6, seed=0, col=None, avanza=True):
    """Tira de película con perforaciones y cuadritos de colores que corren (toda la película = toda la vida)."""
    col = rgb("33302e") if col is None else col
    forma(im, rrect(x, y, w, h, 10), col, t, seed, tinta=4)
    off = (t * 60) % (w / n) if avanza else 0
    cols = [rgb("f6a6a0"), rgb("b8c7e8"), rgb("a8d8b0"), rgb("f4d38a"), rgb("d8b8e8"), rgb("f7c59f")]
    for k in range(n + 1):
        cx = x - w / 2 + (k + 0.5) * w / n - off
        if x - w / 2 + 20 < cx < x + w / 2 - 20:
            forma(im, rrect(cx, y, w / n - 26, h * 0.62, 6), cols[k % 6], t, seed + 1 + k, tinta=2.5)
    for k in range(int(w / 38)):
        px_ = x - w / 2 + 19 + k * 38
        for yy in (y - h / 2 + 12, y + h / 2 - 12):
            forma(im, rrect(px_, yy, 16, 11, 3), CREMA, t, seed + 20 + k, tinta=0)


def hotcake(im, x, y, s, t, seed=0, rot=0.0):
    forma(im, elipse(x, y, 120 * s, 34 * s, rot), rgb("d9973f"), t, seed, tinta=3.5 * s, luz=(rgb("fbd38a"), -20, -10, 0.5))
    lavado(im, elipse(x + 10 * s, y - 6 * s, 70 * s, 14 * s, rot), rgb("f6d07a"), 0.6, seed + 1)


def sarten(im, x, y, s, t, seed=0, rot=0.0):
    forma(im, elipse(x, y, 150 * s, 42 * s, rot), rgb("3a3a40"), t, seed, tinta=4 * s)
    c, sn = math.cos(rot), math.sin(rot)
    forma(im, np.array([(x + 140 * s * c, y + 140 * s * sn - 12 * s), (x + 330 * s * c, y + 330 * s * sn - 12 * s),
                        (x + 330 * s * c, y + 330 * s * sn + 12 * s), (x + 140 * s * c, y + 140 * s * sn + 12 * s)], np.float32),
          rgb("6a4a34"), t, seed + 1, tinta=3 * s)


def carta(im, x, y, s, t, partes, seed=0, rot=0.0):
    """Hoja de carta que se arma por partes; partes = [u_lugar, u_saludo, u_asunto, u_despedida, u_firma] (0..1)."""
    tarjeta(im, x, y, 620 * s, 820 * s, t, rgb("fffaf0"), seed, rot=rot)
    for k in range(13):
        yy = y - 330 * s + k * 55 * s
        linea(im, [(x - 280 * s, yy + 22 * s), (x + 280 * s, yy + 22 * s)], 1.6, rgb("b8c7e8"), seed=seed + 1 + k, t=t, punta=False,
              alfa=0.6)
    u = partes
    if u[0] > 0.02:
        rotulo(im, "Juchipila, 7 de nov. de 2026", x + 70 * s, y - 330 * s, 25 * s * entra_u(u[0]) + 1, AZUL, t, seed=seed + 20,
               tinta=False, fuente="segoeprb.ttf")
    if u[1] > 0.02:
        rotulo(im, "Querido sexto B:", x - 140 * s, y - 230 * s, 40 * s * entra_u(u[1]) + 1, ROJO, t, seed=seed + 21, tinta=False,
               fuente="segoeprb.ttf")
    if u[2] > 0.02:
        n = 5
        for k in range(n):
            v = clamp01(u[2] * n * 1.2 - k)
            if v > 0:
                ww_ = (480 if k < n - 1 else 300) * s * v
                linea(im, [(x - 250 * s, y - 140 * s + k * 55 * s), (x - 250 * s + ww_, y - 140 * s + k * 55 * s)], 5 * s, GRIS,
                      seed=seed + 30 + k, t=t)
    if u[3] > 0.02:
        rotulo(im, "Con cariño,", x + 90 * s, y + 200 * s, 38 * s * entra_u(u[3]) + 1, VERDE, t, seed=seed + 22, tinta=False,
               fuente="segoeprb.ttf")
    if u[4] > 0.02:
        n = max(2, int(40 * u[4]))
        a = np.linspace(0, 1, 40)[:n]
        pts = np.stack([x - 20 * s + 260 * s * a, y + 300 * s + 18 * s * np.sin(a * 18) - 10 * s * a], 1)
        linea(im, pts, 4 * s, TINTA, seed=seed + 40, t=t)
        if u[4] > 0.6:
            rotulo(im, "Profe Tilde", x + 110 * s, y + 345 * s, 34 * s, TINTA, t, seed=seed + 41, tinta=False, fuente="segoeprb.ttf")


def entra_u(u):
    return e_back(clamp01(u))


def gis_txt(im, texto, x, y, px, t, t0, col, seed, vel=0.05, **kw):
    """Texto que se escribe letra a letra desde t0."""
    n = int(len(texto) * clamp01((t - t0) / (0.25 + vel * len(texto))))
    if n > 0:
        rotulo(im, texto[:n], x - (len(texto) - n) * px * 0.28, y, px, col, t, seed=seed, **kw)
