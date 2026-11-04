# -*- coding: utf-8 -*-
"""Personajes y utilería del Short de las arenas movedizas (kit acuarela.py; Kuri e iconos vienen de personajes.py).
    explorador(...)   chibi de frente con salacot, camisa caqui, mochila y botas; camina, patalea, se echa atrás
    arena_frente(...) la superficie de la arena movediza tapando lo que está debajo (borde ondulado, ondas, grumos)
    corte_arena(...)  vista en CORTE: el pozo de arena con granos, transparente para ver las piernas («rayos X»)
    coche, balanza, reloj, sol, palmera, gaviota, ola, heroe_cine (el galán de los sesenta), flotador, tache
"""
import math

import numpy as np

from acuarela import (TINTA, H, W, brillo, cinta, clamp, curva, elipse, forma, lavado, linea, lerp, mancha_pts, rgb,
                      rrect, tr)
from personajes import BLANCO, PIEL, ROSA, _ojos

PELO = rgb("6b4630")
CAMISA = rgb("d8b56c")
CAMISA_OSC = rgb("a8843f")
SHORT = rgb("7d6a45")
BOTA = rgb("7a4a2a")
MOCHILA = rgb("d9603b")
SALACOT = rgb("e9dcb2")
CINTA_S = rgb("6d7f4a")
ARENA = rgb("d9b77c")
ARENA_HUM = rgb("a98653")
ARENA_OSC = rgb("7c5f37")
AGUA = rgb("3f8fb0")


# ------------------------------------------------------------ explorador
def _boca(im, T, tipo, t, seed, a_):
    if tipo == "sonrisa":
        linea(im, T(curva([(-14, -84), (0, -76), (14, -84)], 6)), 3.6 * a_, seed=seed, t=t)
    elif tipo == "o":
        forma(im, T(elipse(0, -78, 8, 10)), rgb("6a2b2b"), t, seed, tinta=3 * a_)
    elif tipo == "grito":
        forma(im, T(curva([(-16, -88), (16, -88), (12, -68), (0, -62), (-12, -68)], 6, True)), rgb("6a2b2b"), t, seed,
              tinta=3.2 * a_)
        forma(im, T(elipse(0, -68, 8, 4)), ROSA, t, seed + 1, tinta=0)
    elif tipo == "apretada":
        forma(im, T(rrect(0, -80, 30, 12, 5)), BLANCO, t, seed, tinta=3 * a_)
        linea(im, T([(-14, -80), (14, -80)]), 2 * a_, seed=seed + 1, t=t)
    elif tipo == "triste":
        linea(im, T(curva([(-12, -76), (0, -84), (12, -76)], 6)), 3.4 * a_, seed=seed, t=t)
    else:                                                   # plana
        linea(im, T([(-10, -80), (10, -80)]), 3.4 * a_, seed=seed, t=t)


def explorador(im, x, y, s, t, rot=0.0, cara="normal", boca="sonrisa", brazos=(0.3, 0.3), codos=(0.4, 0.4), anda=0.0,
               vel=7.0, piernas=None, rodillas=(0.0, 0.0), sx=1.0, seed=100, sombrero=0.0, barro=0.0, bota_izq=True):
    """Explorador chibi de frente. (x, y) = centro del torso. anda 0..1 = amplitud del paso; piernas=(a0, a1) fija el ángulo
    de cada cadera (rad desde la vertical, + hacia fuera); sombrero = cuánto se le levanta el salacot del susto;
    barro 0..1 = manchas de arena mojada en piernas y camisa; bota_izq=False = se le quedó la bota en la arena.
    Devuelve dict con 'manos', 'pies' y 'cabeza' en pantalla (para cuerdas, iconos y burbujas)."""
    def T(p):
        return tr(np.asarray(p, np.float32), x, y, s, rot, sx)

    a_ = s
    # mochila detrás
    forma(im, T(rrect(0, -8, 118, 112, 30)), MOCHILA, t, seed + 1, tinta=4.2 * a_, sombra=(rgb("9a3a22"), 10, 0, 0.55))
    forma(im, T(rrect(-46, 22, 30, 44, 10)), rgb("b34a2c"), t, seed + 2, tinta=3.2 * a_)
    forma(im, T(rrect(0, -70, 76, 22, 10)), rgb("8b9a5a"), t, seed + 3, tinta=3.2 * a_)          # saco de dormir
    # piernas
    pies = []
    for i, d in enumerate((-1, 1)):
        if piernas is None:
            ang = d * 0.08 + anda * 0.45 * math.sin(t * vel + i * math.pi)
        else:
            ang = piernas[i] * d
        hip = np.array([d * 22, 46], np.float32)
        rod = hip + 36 * np.array([math.sin(ang), math.cos(ang)])
        a2 = ang + rodillas[i] * d
        pie = rod + 34 * np.array([math.sin(a2), math.cos(a2)])
        forma(im, T(cinta([hip, rod, pie], 26, 22)), PIEL, t, seed + 10 + i, tinta=4 * a_, sombra=(rgb("d9967a"), 6 * d, 0, 0.4))
        if barro > 0:
            lavado(im, T(cinta([rod, pie], 22, 22)), ARENA_HUM, 0.75 * barro, seed + 14 + i)
        if bota_izq or i == 1:
            bota = np.array([(-16, -12), (16, -12), (18, 6), (30, 14), (30, 24), (-18, 24)], np.float32)
            bota[:, 0] *= d
            forma(im, T(bota + pie), BOTA, t, seed + 12 + i, tinta=4 * a_, luz=(BLANCO, -4, 6, 0.15))
        else:
            forma(im, T(elipse(pie[0], pie[1] + 6, 14, 12)), rgb("f3efe6"), t, seed + 16, tinta=3.4 * a_)        # calcetín
        pies.append(T([pie])[0])
    forma(im, T(curva([(-48, 20), (48, 20), (50, 60), (6, 64), (0, 52), (-6, 64), (-50, 60)], 6, True)), SHORT, t, seed + 18,
          tinta=4.2 * a_)
    # torso
    torso = curva([(-46, -54), (46, -54), (52, 6), (46, 34), (-46, 34), (-52, 6)], 8, True)
    forma(im, T(torso), CAMISA, t, seed + 20, tinta=4.6 * a_, sombra=(CAMISA_OSC, 14, 0, 0.55), luz=(BLANCO, -12, 10, 0.14))
    forma(im, T(curva([(-16, -54), (0, -34), (16, -54)], 4, True)), PIEL, t, seed + 21, tinta=2.8 * a_)          # cuello
    for d in (-1, 1):
        forma(im, T(rrect(d * 24, -12, 24, 20, 4)), CAMISA_OSC, t, seed + 22 + d, tinta=2.6 * a_)                # bolsillos
    linea(im, T(curva([(-40, -50), (-30, -10), (-36, 30)], 5)), 6 * a_, col=rgb("6b3a24"), seed=seed + 25, t=t, punta=False)
    linea(im, T(curva([(40, -50), (30, -10), (36, 30)], 5)), 6 * a_, col=rgb("6b3a24"), seed=seed + 26, t=t, punta=False)
    forma(im, T(rrect(0, 30, 98, 12, 5)), rgb("5a3b22"), t, seed + 27, tinta=2.6 * a_)
    if barro > 0:
        lavado(im, T(mancha_pts(14, 18, 26, seed + 28, 0.35)), ARENA_HUM, 0.6 * barro, seed + 28)
    # brazos
    manos = []
    for i, d in enumerate((-1, 1)):
        hom = np.array([d * 42, -40], np.float32)
        a1 = brazos[i] * d
        codo = hom + 38 * np.array([math.sin(a1), math.cos(a1)])
        a2 = a1 + codos[i] * d
        mano = codo + 34 * np.array([math.sin(a2), math.cos(a2)])
        forma(im, T(cinta([hom, codo], 26, 22)), CAMISA, t, seed + 30 + i, tinta=4 * a_)
        forma(im, T(cinta([codo, mano], 20, 18)), PIEL, t, seed + 32 + i, tinta=3.8 * a_)
        forma(im, T(elipse(mano[0], mano[1], 14, 14)), PIEL, t, seed + 34 + i, tinta=3.6 * a_)
        manos.append(T([mano])[0])
    # cabeza
    forma(im, T(elipse(0, -118, 72, 66)), PIEL, t, seed + 40, tinta=4.8 * a_, sombra=(rgb("d9967a"), 12, -2, 0.45))
    for d in (-1, 1):
        forma(im, T(elipse(d * 72, -112, 12, 16)), PIEL, t, seed + 41 + d, tinta=3.6 * a_)                       # orejas
    forma(im, T(curva([(-70, -132), (-56, -150), (-20, -158), (24, -158), (58, -150), (72, -130), (40, -142), (0, -146),
                       (-40, -142)], 6, True)), PELO, t, seed + 44, tinta=3.6 * a_)
    _ojos(im, cara, list(T([(-27, -112), (27, -112)])), 0, s * 1.15, t, seed + 50, sx)
    for d in (-1, 1):                                                                                           # cejas
        lev = 10 if cara in ("susto", "abiertos") else 0
        linea(im, T(curva([(d * 40, -134 - lev), (d * 27, -140 - lev), (d * 14, -136 - lev)], 4)), 3.6 * a_, seed=seed + 55 + d, t=t)
    lavado(im, T(elipse(-46, -90, 13, 8)), ROSA, 0.5, seed + 58)
    lavado(im, T(elipse(46, -90, 13, 8)), ROSA, 0.5, seed + 59)
    _boca(im, T, boca, t, seed + 60, a_)
    # salacot (se levanta del susto)
    sy = -sombrero * 46
    forma(im, T(elipse(0, -160 + sy, 108, 26)), SALACOT, t, seed + 70, tinta=4.2 * a_, sombra=(rgb("c7b37f"), 0, -6, 0.5))
    forma(im, T(curva([(-70, -164), (-60, -212), (-24, -238), (24, -238), (60, -212), (70, -164)], 7, True) + [0, sy]),
          SALACOT, t, seed + 71, tinta=4.4 * a_, sombra=(rgb("c7b37f"), 16, 0, 0.5), luz=(BLANCO, -14, 10, 0.25))
    forma(im, T(np.array([(-70, -176), (70, -176), (68, -162), (-68, -162)], np.float32) + [0, sy]), CINTA_S, t, seed + 72,
          tinta=2.8 * a_)
    forma(im, T(elipse(0, -240 + sy, 9, 7)), CINTA_S, t, seed + 73, tinta=2.4 * a_)
    return dict(manos=manos, pies=pies, cabeza=T([(0, -120)])[0], sombrero=T([(0, -230 + sy)])[0])


# ------------------------------------------------------------ arena
def arena_frente(im, y_sup, t, seed=0, x0=-40, x1=W + 40, onda=6.0, col=ARENA_HUM, alto=None, cuerpo=None, ondas_r=0.0):
    """Tapa todo lo que queda por debajo de y_sup con arena movediza mojada (borde ondulado que respira).
    cuerpo = x del cuerpo hundido: ahí la arena hace un cuello y anillos (ondas_r = radio de las ondas que se abren)."""
    alto = H + 60 if alto is None else alto
    xs = np.linspace(x0, x1, 40)
    ys = y_sup + onda * np.sin(xs / 90 + t * 1.6 + seed) + 3 * np.sin(xs / 31 - t * 2.2)
    if cuerpo is not None:
        ys = ys - 14 * np.exp(-((xs - cuerpo) / 80) ** 2)
    top = np.stack([xs, ys], 1)
    if alto < H:                                             # charco: labio delantero en media elipse (perspectiva)
        cx_, rx_ = (x0 + x1) / 2, (x1 - x0) / 2
        a = np.linspace(0, math.pi, 30)
        fondo = np.stack([cx_ + rx_ * np.cos(a), y_sup + (alto - y_sup) * np.sin(a)], 1)
        pol = np.concatenate([top, fondo]).astype(np.float32)
    else:
        pol = np.concatenate([top, [(x1, alto), (x0, alto)]]).astype(np.float32)
    forma(im, pol, col, t, seed + 1, tinta=4.0, sombra=(ARENA_OSC, 0, -30, 0.35), luz=(rgb("f3dcaa"), 0, 24, 0.3), amp=1.0)
    rg = np.random.default_rng(seed + 7)
    for k in range(26):                                      # grumos y brillos de agua
        gx, gy = rg.uniform(x0, x1), y_sup + rg.uniform(20, 700)
        if gy < alto - 10:
            lavado(im, elipse(gx, gy, rg.uniform(10, 34), rg.uniform(5, 12)), ARENA_OSC if k % 3 else rgb("f0d9a6"), 0.35,
                   seed + 20 + k)
    if cuerpo is not None and ondas_r > 0:
        for j in range(3):
            r = (ondas_r + j * 70) % 260 + 60
            a = 1 - (r - 60) / 260
            linea(im, elipse(cuerpo, y_sup + 6, r, r * 0.22), 3.5, col=ARENA_OSC, seed=seed + 40 + j, t=t, cerrado=True,
                  alfa=0.6 * a, punta=False)


_GRANOS = {}


def corte_arena(im, y_sup, t, seed=0, aprieta=0.0, agua=0.0, cx=W / 2, piernas_y=(0, 0), r_aflojar=0.0):
    """Vista en corte: capas de arena bajo y_sup con granos. aprieta 0..1: los granos se juntan y oscurecen alrededor de
    las piernas (cx, piernas_y=(y0, y1)); agua 0..1: hilos azules que entran y aflojan (r_aflojar = radio afectado)."""
    forma(im, np.array([(-40, y_sup), (W + 40, y_sup), (W + 40, H + 40), (-40, H + 40)], np.float32), ARENA, t, seed,
          tinta=4.5, sombra=(ARENA_OSC, 0, -60, 0.3), amp=0.8, alfa=0.55)
    for k, (yy, c) in enumerate(((y_sup + 260, ARENA_HUM), (y_sup + 620, ARENA_OSC), (y_sup + 980, rgb("8c6a3e")))):
        xs = np.linspace(-40, W + 40, 30)
        pol = np.concatenate([np.stack([xs, yy + 22 * np.sin(xs / 140 + k)], 1), [(W + 40, H + 40), (-40, H + 40)]])
        lavado(im, pol.astype(np.float32), c, 0.28, seed + 10 + k)
    if seed not in _GRANOS:
        rg = np.random.default_rng(seed + 99)
        _GRANOS[seed] = np.stack([rg.uniform(0, W, 900), rg.uniform(0, 1, 900), rg.uniform(4, 10, 900)], 1)
    g = _GRANOS[seed]
    y0, y1 = piernas_y
    for (gx, gu, gr) in g[::3]:
        gy = y_sup + 30 + gu * (H - y_sup)
        dx = gx - cx
        cerca = math.exp(-(dx / 170) ** 2) * (1 if y0 - 60 < gy < y1 + 120 else 0.3)
        px = gx - dx * 0.35 * aprieta * cerca
        col = ARENA_OSC * (1 - 0.35 * aprieta * cerca)
        if agua > 0 and math.hypot(dx, gy - (y0 + y1) / 2) < r_aflojar:
            px = gx + dx * 0.25 * agua
            col = col * (1 - 0.4 * agua) + AGUA * 0.4 * agua
        lavado(im, elipse(px, gy, gr, gr * 0.8), col, 0.55, int(gx) % 97)


def hilos_agua(im, cx, y0, y1, u, t, seed=0):
    """Hilos de agua que bajan serpenteando hasta las piernas (u 0..1 = cuánto han bajado)."""
    for k in range(6):
        x = cx + (k - 2.5) * 70
        n = 12
        yy = np.linspace(y0, y0 + (y1 - y0) * u, n)
        pts = np.stack([x + 18 * np.sin(yy / 50 + k + t * 2), yy], 1)
        if u > 0.02:
            linea(im, pts, 15, col=AGUA, seed=seed + k, t=t, alfa=0.85)


# ------------------------------------------------------------ utilería
def coche(im, x, y, s, t, col=None, seed=2100, rot=0.0, cara=True):
    """Cochecito chibi de perfil (centro de la carrocería)."""
    col = rgb("d8463a") if col is None else col

    def T(p):
        return tr(np.asarray(p, np.float32), x, y, s, rot)
    forma(im, T(curva([(-150, 30), (-150, -10), (-90, -24), (-50, -80), (50, -80), (100, -24), (150, -14), (152, 30)], 7, True)),
          col, t, seed, tinta=5 * s, sombra=(col * 0.6, 0, -16, 0.6), luz=(BLANCO, -10, 12, 0.22))
    forma(im, T(curva([(-40, -70), (-4, -70), (-4, -28), (-74, -28)], 3, True)), rgb("bfe7f3"), t, seed + 1, tinta=3.2 * s)
    forma(im, T(curva([(8, -70), (44, -70), (84, -28), (8, -28)], 3, True)), rgb("bfe7f3"), t, seed + 2, tinta=3.2 * s)
    for d in (-1, 1):
        forma(im, T(elipse(d * 88, 30, 34, 34)), rgb("2b2a2e"), t, seed + 3 + d, tinta=4 * s)
        forma(im, T(elipse(d * 88, 30, 14, 14)), rgb("c9cdd3"), t, seed + 6 + d, tinta=2.4 * s)
    forma(im, T(elipse(140, -4, 10, 8)), rgb("ffe28a"), t, seed + 9, tinta=2.4 * s)
    if cara:
        for d in (-1, 1):
            forma(im, T(elipse(-30 + d * 14, 4, 6, 8)), TINTA, t, seed + 10 + d, tinta=0)
        linea(im, T(curva([(-44, 18), (-30, 26), (-16, 18)], 5)), 3 * s, seed=seed + 13, t=t)


def balanza(im, x, y, s, t, incl, seed=2200):
    """Balanza de platillos: incl > 0 baja el platillo derecho. Devuelve los centros de los platillos."""
    forma(im, tr(np.array([(-70, 260), (70, 260), (24, 220), (-24, 220)], np.float32), x, y, s), rgb("8a6a44"), t, seed,
          tinta=4 * s)
    forma(im, tr(rrect(0, 100, 22, 250, 8), x, y, s), rgb("a07f52"), t, seed + 1, tinta=4 * s)
    ex = np.array([math.cos(incl), math.sin(incl)]) * 330 * s
    c = np.array([x, y - 20 * s])
    linea(im, [c - ex, c + ex], 14 * s, col=rgb("6b4e2f"), seed=seed + 2, t=t, punta=False)
    forma(im, elipse(c[0], c[1], 18 * s, 18 * s), rgb("d9b25c"), t, seed + 3, tinta=3 * s)
    plat = []
    for k, e in enumerate((-ex, ex)):
        p = c + e
        q = p + np.array([0, 190 * s])
        for d in (-1, 1):
            linea(im, [p, q + np.array([d * 110 * s, 0])], 3 * s, seed=seed + 4 + 2 * k + d, t=t)
        forma(im, curva([(q[0] - 130 * s, q[1]), (q[0], q[1] + 40 * s), (q[0] + 130 * s, q[1])], 6, True), rgb("d9b25c"), t,
              seed + 8 + k, tinta=3.6 * s)
        plat.append(q)
    return plat


def cubeta(im, x, y, s, t, seed=2300):
    """Cubeta llena de arena movediza (pesa el doble)."""
    forma(im, tr(np.array([(-80, -90), (80, -90), (62, 90), (-62, 90)], np.float32), x, y, s), rgb("4f8fc0"), t, seed,
          tinta=4.6 * s, sombra=(rgb("2f5f86"), 14, 0, 0.5))
    forma(im, tr(elipse(0, -90, 80, 20), x, y, s), ARENA_HUM, t, seed + 1, tinta=3.6 * s)
    linea(im, tr(curva([(-78, -92), (-40, -170), (40, -170), (78, -92)], 6), x, y, s), 5 * s, seed=seed + 2, t=t, punta=False)


def reloj(im, x, y, r, t, horas, seed=2400):
    """Reloj de pared pintado; horas = cuánto ha girado la aguja corta (gira rápido para el «horas…»)."""
    forma(im, elipse(x, y, r, r), BLANCO, t, seed, tinta=6, sombra=(rgb("c9c2b0"), 10, -6, 0.5))
    for k in range(12):
        a = k / 12 * 2 * math.pi
        linea(im, [(x + 0.78 * r * math.sin(a), y - 0.78 * r * math.cos(a)), (x + 0.9 * r * math.sin(a), y - 0.9 * r * math.cos(a))],
              4, seed=seed + 1 + k, t=t, punta=False)
    a1 = horas / 12 * 2 * math.pi
    a2 = horas * 2 * math.pi
    linea(im, [(x, y), (x + 0.5 * r * math.sin(a1), y - 0.5 * r * math.cos(a1))], 9, seed=seed + 20, t=t)
    linea(im, [(x, y), (x + 0.75 * r * math.sin(a2), y - 0.75 * r * math.cos(a2))], 6, col=rgb("c8473a"), seed=seed + 21, t=t)
    forma(im, elipse(x, y, 9, 9), TINTA, t, seed + 22, tinta=0)


def sol(im, x, y, r, t, col=None, seed=2500, cara=None):
    col = rgb("ffd65a") if col is None else col
    brillo(im, x, y, r * 2.4, col, 0.35)
    for k in range(10):
        a = k / 10 * 2 * math.pi + t * 0.3
        linea(im, [(x + 1.2 * r * math.cos(a), y + 1.2 * r * math.sin(a)), (x + 1.55 * r * math.cos(a), y + 1.55 * r * math.sin(a))],
              7, col=col * 0.9, seed=seed + k, t=t)
    forma(im, elipse(x, y, r, r), col, t, seed + 20, tinta=4.5, luz=(BLANCO, -r * 0.2, r * 0.25, 0.3))
    if cara == "sudor":
        for d in (-1, 1):
            forma(im, elipse(x + d * r * 0.3, y - r * 0.1, r * 0.08, r * 0.12), TINTA, t, seed + 30 + d, tinta=0)
        linea(im, curva([(x - r * 0.25, y + r * 0.35), (x, y + r * 0.25), (x + r * 0.25, y + r * 0.35)], 5), 4, seed=seed + 33, t=t)


def palmera(im, x, y, s, t, seed=2600):
    tronco = cinta(curva([(x, y), (x + 30 * s, y - 260 * s), (x + 90 * s, y - 520 * s)], 8), 46 * s, 26 * s)
    forma(im, tronco, rgb("9b7448"), t, seed, tinta=4 * s, sombra=(rgb("6e4f2e"), 10, 0, 0.5))
    cx, cy = x + 90 * s, y - 520 * s
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.62 + 0.06 * math.sin(t * 1.4 + k)
        p1 = (cx + 150 * s * math.cos(a), cy + 150 * s * math.sin(a) * 0.6 - 30 * s)
        p2 = (cx + 270 * s * math.cos(a), cy + 120 * s * abs(math.cos(a)) + 30 * s)
        hoja = cinta(curva([(cx, cy), p1, p2], 8), 52 * s, 6 * s)
        forma(im, hoja, rgb("5f9a4a") * (0.9 + 0.08 * (k % 2)), t, seed + 1 + k, tinta=3.4 * s)
    for d in (-1, 0, 1):
        forma(im, elipse(cx + d * 26 * s, cy + 22 * s, 18 * s, 18 * s), rgb("6b4a2a"), t, seed + 10 + d, tinta=3 * s)


def gaviota(im, x, y, s, t, seed=2700):
    a = 0.5 * math.sin(t * 7 + seed)
    for d in (-1, 1):
        linea(im, curva([(x, y), (x + d * 40 * s, y - (20 + 30 * a) * s), (x + d * 80 * s, y - 6 * s + 20 * a * s)], 5),
              6 * s, seed=seed + d, t=t)


def ola(im, y, t, col, alfa=0.7, seed=2800, amp=18.0, x0=-40, x1=W + 40, espuma=True, y0=-40):
    """Lengua de agua desde arriba hasta y (borde con espuma)."""
    xs = np.linspace(x0, x1, 36)
    ys = y + amp * np.sin(xs / 120 + t * 1.8 + seed) + 6 * np.sin(xs / 37 - t * 3)
    pol = np.concatenate([[(x0, y0), (x1, y0)], np.stack([xs, ys], 1)[::-1]]).astype(np.float32)
    lavado(im, pol, col, alfa, seed, humedo=14)
    if espuma:
        linea(im, np.stack([xs, ys], 1), 9, col=BLANCO, seed=seed + 1, t=t, alfa=0.85, punta=False)


def heroe_cine(im, x, y, s, t, seed=2900, mano=0.0):
    """El galán de las películas viejas (sombrero de ala, bigote, traje); (x, y) = cabeza; mano 0..1 = el brazo que asoma."""
    forma(im, tr(curva([(-80, 60), (80, 60), (96, 300), (-96, 300)], 5, True), x, y, s), rgb("6a5a4a"), t, seed + 20, tinta=4.6 * s)
    forma(im, tr(curva([(-22, 60), (22, 60), (0, 140)], 3, True), x, y, s), BLANCO, t, seed + 21, tinta=3 * s)
    forma(im, tr(curva([(-8, 70), (8, 70), (4, 130), (-4, 130)], 3, True), x, y, s), rgb("8a2a2a"), t, seed + 22, tinta=2 * s)
    forma(im, tr(elipse(0, 0, 70, 66), x, y, s), rgb("e8d8c0"), t, seed, tinta=4.6 * s)
    forma(im, tr(elipse(0, -50, 116, 20), x, y, s), rgb("3a3330"), t, seed + 1, tinta=4 * s)
    forma(im, tr(curva([(-62, -52), (-54, -104), (54, -104), (62, -52)], 6, True), x, y, s), rgb("3a3330"), t, seed + 2, tinta=4 * s)
    for d in (-1, 1):
        forma(im, tr(elipse(d * 24, 4, 12, 13), x, y, s), BLANCO, t, seed + 3 + d, tinta=2.6 * s)
        forma(im, tr(elipse(d * 24, 6, 5, 6), x, y, s), TINTA, t, seed + 6 + d, tinta=0)
    forma(im, tr(curva([(-26, 30), (0, 24), (26, 30), (0, 36)], 4, True), x, y, s), rgb("3a3330"), t, seed + 9, tinta=2 * s)
    forma(im, tr(elipse(0, 50, 14, 10), x, y, s), rgb("5a2b2b"), t, seed + 10, tinta=2.6 * s)
    if mano > 0:
        mx, my = x + 150 * s, y - 40 * s - 120 * s * mano
        forma(im, cinta([(mx, y + 120 * s), (mx, my)], 30 * s, 26 * s), rgb("e8d8c0"), t, seed + 11, tinta=4 * s)
        forma(im, elipse(mx, my - 10 * s, 24 * s, 28 * s), rgb("e8d8c0"), t, seed + 12, tinta=4 * s)


def flotador(im, x, y, s, t, seed=3000):
    """Flotador de alberca a rayas."""
    forma(im, elipse(x, y, 120 * s, 46 * s), rgb("f7f2e6"), t, seed, tinta=4.5 * s, sombra=(rgb("c9c2b0"), 0, -10, 0.5))
    for k in range(4):
        a0 = k / 4 * 2 * math.pi + 0.3
        pts = [(x + 120 * s * math.cos(a0 + j * 0.25), y + 46 * s * math.sin(a0 + j * 0.25)) for j in range(4)]
        pts += [(x + 72 * s * math.cos(a0 + j * 0.25), y + 22 * s * math.sin(a0 + j * 0.25)) for j in range(3, -1, -1)]
        lavado(im, np.array(pts, np.float32), rgb("e8584a"), 0.85, seed + 1 + k)
    forma(im, elipse(x, y - 2 * s, 66 * s, 20 * s), AGUA, t, seed + 9, tinta=3.2 * s)


def tache(im, x, y, r, t, u=1.0, seed=3100):
    """Tache rojo pintado (dos trazos que se dibujan con u)."""
    rojo = rgb("d8463a")
    a = clamp(u * 2)
    b = clamp(u * 2 - 1)
    if a > 0:
        linea(im, [(x - r, y - r), (x - r + 2 * r * a, y - r + 2 * r * a)], r * 0.28, col=rojo, seed=seed, t=t)
    if b > 0:
        linea(im, [(x + r, y - r), (x + r - 2 * r * b, y - r + 2 * r * b)], r * 0.28, col=rojo, seed=seed + 1, t=t)


def cuerda(im, p0, p1, t, tension=1.0, seed=3200):
    """Cuerda de p0 a p1; con poca tensión cuelga."""
    p0, p1 = np.asarray(p0, np.float32), np.asarray(p1, np.float32)
    m = (p0 + p1) / 2 + np.array([0, 80 * (1 - tension)])
    linea(im, curva([tuple(p0), tuple(m), tuple(p1)], 10), 11, col=rgb("b8925a"), seed=seed, t=t, punta=False)
