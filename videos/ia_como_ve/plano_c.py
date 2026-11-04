# -*- coding: utf-8 -*-
"""GATO 1959: Hubel y Wiesel (retratos reales en camafeo) → un gato chibi mira una pantalla donde gira una barra de luz; la
neurona solo «dispara» (picos en el registro + destellos) con UNA inclinación → la figura real de su artículo → pirámide
líneas → esquinas → formas → el gato armado por pisos → medalla «NOBEL 1981» → los ingenieros: «¿y si lo hacemos con números?»."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, mancha_pts, pr, rgb,
                      rotulo, rrect, suave, terminar)
from comun import FIN, INI, T0, T1, desborde, ww
from fondos_ia import papel
from personajes import AMARILLO, BLANCO, OJO_K, destello, exclama, kuri, pregunta
from personajes_ia import NARANJA, camafeo, gato, nina, pegar, retrato

E = "gato"
T_INI = T0(E)
tPista, tCient, tMidieron = ww(E, 0, "pista"), ww(E, 0, "cientificos"), ww(E, 0, "midieron")
tGato0 = ww(E, 0, "gato")
tRaro, tCada, tLinea, tCierta = ww(E, 1, "rarisimo"), ww(E, 1, "cada"), ww(E, 1, "linea"), ww(E, 1, "inclinacion")
tUnas, tEsquinas, tFormas = ww(E, 2, "unas"), ww(E, 2, "esquinas"), ww(E, 2, "formas")
tGolpe, tPisos, tComplejo, tNobel = ww(E, 3, "golpe"), ww(E, 3, "pisos"), ww(E, 3, "complejo"), ww(E, 3, "nobel")
tIng, tNumeros = ww(E, 4, "ingenieros"), ww(E, 4, "numeros")
T_FIN = T1(E)
ANG_BUENO = math.radians(45)


def _barra(t):
    """Ángulo de la barra de luz: gira; desde «inclinación» se queda en el ángulo bueno."""
    if t > tCierta - 0.3:
        return ANG_BUENO
    return ANG_BUENO + 1.4 * math.sin((t - tLinea) * 1.6) if t > tLinea else math.pi / 2


def _disparo(ang):
    return math.exp(-((ang - ANG_BUENO) / 0.22) ** 2)


def cerebro(im, cx, cy, s, t, luces=(), seed=8500, alfa=1.0):
    """Cerebro de acuarela (vista lateral): lóbulo rosa con circunvoluciones de tinta, cerebelo y tronco; `luces` = [(u, v, f)]
    en coordenadas relativas (-1..1) que brillan como zonas activas."""
    if s <= 0.02:
        return
    forma(im, rrect(cx + 50 * s, cy + 150 * s, 40 * s, 90 * s, 16 * s, -0.35), rgb("e7a7bd"), t, seed + 1, tinta=3.5 * s, alfa=alfa)
    forma(im, elipse(cx + 125 * s, cy + 105 * s, 78 * s, 50 * s, -0.2), rgb("d98aa8"), t, seed, tinta=3.5 * s, alfa=alfa)
    forma(im, mancha_pts(cx - 20 * s, cy - 10 * s, 210 * s, seed + 2, irreg=0.07, ry=140 * s), rgb("f0b3c6"), t, seed + 3, tinta=5 * s,
          alfa=alfa, sombra=(rgb("c47c98"), 0, 18 * s, 0.45), luz=(BLANCO, -30 * s, -30 * s, 0.35))
    r = np.random.default_rng(seed)
    for k in range(17):                                         # circunvoluciones
        x0, y0 = cx - 20 * s + r.uniform(-160, 160) * s, cy + r.uniform(-100, 75) * s
        a = r.uniform(0, math.pi)
        pts = [(x0 + (j - 2) * 22 * s * math.cos(a) + 12 * s * math.sin(j * 1.7 + k),
                y0 + (j - 2) * 22 * s * math.sin(a) + 12 * s * math.cos(j * 1.9 + k)) for j in range(5)]
        linea(im, curva(pts, 5), 4 * s, col=rgb("a85a7a"), seed=seed + 10 + k, t=t, alfa=0.8 * alfa)
    linea(im, curva([(cx - 200 * s, cy + 10 * s), (cx - 60 * s, cy + 40 * s), (cx + 120 * s, cy + 30 * s)], 6), 5 * s,
          col=rgb("a85a7a"), seed=seed + 30, t=t, alfa=0.9 * alfa)
    for (u, v, f) in luces:
        if f > 0.02:
            brillo(im, cx - 20 * s + u * 170 * s, cy + v * 110 * s, 70 * s, AMARILLO, 0.75 * f)


def laboratorio(t):
    im = papel("calido")
    ec = e_back(pr(t, tPista - 0.2, tPista + 0.3)) * (1 - pr(t, tCient - 0.5, tCient - 0.1))
    if ec > 0.02:
        cerebro(im, 470, 560, 1.35 * ec, t, luces=[(0.85, 0.15, 0.5 + 0.5 * math.sin(t * 4))])
        rotulo(im, "UN CEREBRO DE VERDAD", 470, 860, 52, rgb("b8443a"), t, seed=8021, esc=ec)
    # retratos reales (camafeos)
    for k, (n, nom) in enumerate((("hubel", "DAVID HUBEL"), ("wiesel", "TORSTEN WIESEL"))):
        e = e_back(pr(t, tCient - 0.1 + 0.3 * k, tCient + 0.25 + 0.3 * k)) * (1 - pr(t, tRaro - 0.3, tRaro))
        camafeo(im, retrato(n, 220, 280, sepia=True), 200 + 330 * k, 330, 0.95 * e, t, nombre=nom, seed=8000 + 10 * k)
    if t > tPista - 0.2:
        rotulo(im, "1959", 365, 130, 90, rgb("b8443a"), t, seed=8020, esc=e_back(pr(t, tPista + 0.8, tPista + 1.1)),
               alfa=1 - pr(t, tRaro - 0.3, tRaro))
    # la pantalla con la barra de luz y el gato que la mira
    sx, sy = 1300, 380
    forma(im, rrect(sx, sy, 700, 470, 18), rgb("1d2430"), t, 8030, tinta=5)
    ang = _barra(t)
    if t > tMidieron - 0.4:
        d = np.array([math.cos(ang), -math.sin(ang)]) * 170
        n = np.array([math.sin(ang), math.cos(ang)]) * 16
        c = np.array([sx, sy])
        poly = np.array([c - d - n, c + d - n, c + d + n, c - d + n], np.float32)
        forma(im, poly, rgb("fff2b8"), t, 8031, tinta=0)
        brillo(im, sx, sy, 160, rgb("fff2b8"), 0.25)
    gato(im, sx - 80, 860, 1.25, t, pose="despierto", seed=8100, sx=-1)
    # la neurona y su registro
    f = _disparo(ang) if t > tCada else 0.0
    nx, ny = 430, 560 if t > tRaro else 1400
    if t > tRaro - 0.4:
        nyy = lerp(1300, 520, e_out(pr(t, tRaro - 0.4, tRaro + 0.2)))
        for k in range(6):                                     # dendritas
            a = math.pi * (0.75 + 0.5 * k / 5)
            linea(im, curva([(nx, nyy), (nx + 110 * math.cos(a), nyy - 110 * math.sin(a)),
                             (nx + 170 * math.cos(a + 0.2), nyy - 170 * math.sin(a + 0.2))], 6), 8, col=rgb("d77fa1"), seed=8200 + k, t=t)
        linea(im, curva([(nx, nyy), (nx + 160, nyy + 40), (nx + 330, nyy + 10)], 6), 10, col=rgb("d77fa1"), seed=8210, t=t)
        forma(im, elipse(nx, nyy, 62, 56), rgb("e9a0bd"), t, 8211, tinta=4.6, sombra=(rgb("b8668a"), 10, 0, 0.5))
        brillo(im, nx, nyy, 90 + 60 * f, AMARILLO, 0.55 * f)
        # registro: picos a la derecha de la neurona
        forma(im, rrect(470, 880, 620, 190, 14), rgb("fbf3df"), t, 8219, tinta=4)
        rotulo(im, "LO QUE «DICE» LA NEURONA", 470, 815, 30, TINTA, t, seed=8218, tinta=False)
        linea(im, curva([(nx + 330, nyy + 10), (nx + 380, nyy + 200), (nx + 280, 860)], 6), 4, col=rgb("d77fa1"), seed=8217, t=t,
              alfa=0.7, punta=False)
        rx0, ry_ = 230, 920
        pts = []
        for i in range(120):
            x = rx0 + i * 4
            tt = t - (120 - i) * 0.012
            fa = _disparo(_barra(tt)) if tt > tCada else 0
            pico = 1.0 if ((int(tt * 40) * 7919) % 100) < 85 * fa and (int(tt * 40) % 2 == 0) else 0
            pts.append((x, ry_ - 70 * pico))
        linea(im, pts, 3, seed=8220, t=t, punta=False)
        if f > 0.6 and t > tCierta:
            for k in range(3):
                destello(im, nx + 90 * math.cos(k * 2.1 + t), nyy - 90 + 30 * math.sin(k * 2.1 + t), 0.6, t, seed=1032 + k)
            rotulo(im, "¡TIC TIC TIC!", nx, nyy - 220, 54, AMARILLO, t, seed=8230, esc=e_back(pr(t, tCierta, tCierta + 0.2)))
    # la figura REAL de su artículo
    if t > tCierta + 0.3:
        e = e_back(pr(t, tCierta + 0.3, tCierta + 0.6))
        pegar(im, retrato("hubel_wiesel_registro", 290, 390), 1760, 790, 0.62 * e, 0.06, t=t, seed=8240)
        rotulo(im, "SU REGISTRO (1959)", 1760, 965, 30, TINTA, t, seed=8241, tinta=False, esc=e)
    return im


def piramide(t):
    im = papel("calido")
    pisos = [("LÍNEAS", tUnas), ("ESQUINAS", tEsquinas), ("FORMAS", tFormas), ("GATO", tPisos + 0.4)]
    base_y, alto = 950, 200
    # a la derecha, el cerebro del gato: cada piso enciende una zona más adelante (de la nuca hacia la frente)
    cerebro(im, 1640, 640, 1.05, t, luces=[(0.9 - 0.45 * k, -0.1 + 0.15 * (k % 2), e_out(pr(t, ti, ti + 0.4)))
                                           for k, (_, ti) in enumerate(pisos)])
    rotulo(im, "CEREBRO DEL GATO", 1620, 870, 40, rgb("b8443a"), t, seed=8301)
    for k, (nom, ti) in enumerate(pisos):
        e = e_back(pr(t, ti - 0.15, ti + 0.2))
        if e <= 0.02:
            continue
        y = base_y - k * alto
        w = 1120 - 220 * k
        cx = 820
        forma(im, rrect(cx, y, w * e, alto - 24, 20), rgb(["dff0f2", "cfe8ea", "bfdfe2", "fbe2b8"][k]), t, 8300 + k, tinta=4)
        rotulo(im, nom, cx - w / 2 + 110, y, 40, TINTA, t, seed=8310 + k, tinta=False, esc=e)
        # contenido de cada piso
        for j in range(4 - k):
            px = cx - w / 2 + 300 + j * (w - 380) / max(1, 3 - k)
            if k == 0:
                a = j * 0.8
                linea(im, [(px - 40 * math.cos(a), y + 40 * math.sin(a)), (px + 40 * math.cos(a), y - 40 * math.sin(a))], 7,
                      seed=8320 + j, t=t)
            elif k == 1:
                linea(im, [(px - 40, y - 30), (px - 40, y + 30), (px + 30, y + 30)], 7, seed=8330 + j, t=t, punta=False)
            elif k == 2:
                if j == 0:
                    linea(im, elipse(px, y, 40, 40), 7, seed=8340, t=t, cerrado=True, punta=False)
                else:
                    linea(im, [(px - 40, y + 32), (px, y - 38), (px + 40, y + 32), (px - 40, y + 32)], 7, seed=8341 + j, t=t,
                          punta=False)
            elif k == 3:
                gato(im, cx + 40, y + 20, 0.5, t, pose="despierto", seed=8350)
        if k > 0 and e > 0.5:                                  # hilos que suben de piso a piso
            for j in range(3):
                linea(im, [(cx - 200 + 200 * j, y + alto / 2 - 4), (cx - 150 + 150 * j, y + alto / 2 - 30)], 3,
                      col=rgb("d77fa1"), seed=8360 + k * 3 + j, t=t, alfa=0.7, punta=False)
    if t > tGolpe - 0.2:
        e = e_back(pr(t, tGolpe - 0.2, tGolpe + 0.1)) * (1 - pr(t, tPisos - 0.2, tPisos))
        rotulo(im, "¿DE GOLPE? NO", 820, 150, 72, rgb("e35d4a"), t, seed=8370, esc=e, rot=0.05)
    if t > tComplejo - 0.1:
        flecha_y = lerp(base_y, base_y - 3 * alto, e_out(pr(t, tComplejo - 0.1, tComplejo + 0.5)))
        linea(im, [(150, base_y - 20), (150, flecha_y)], 12, col=rgb("3f78c8"), seed=8380, t=t)
        rotulo(im, "SIMPLE", 150, base_y + 70, 38, rgb("3f78c8"), t, seed=8381)
        rotulo(im, "COMPLEJO", 160, base_y - 3 * alto - 70, 38, rgb("3f78c8"), t, seed=8382, esc=pr(t, tComplejo, tComplejo + 0.3))
    if t > tNobel - 0.2:                                       # medalla
        e = e_back(pr(t, tNobel - 0.2, tNobel + 0.2))
        mx, my = 1640, 330
        for k in range(2):
            linea(im, [(mx - 30 + 60 * k, my - 230 * e), (mx, my - 80 * e)], 18, col=rgb(["3f78c8", "e35d4a"][k]), seed=8390 + k, t=t)
        forma(im, elipse(mx, my, 100 * e, 100 * e), rgb("e9b949"), t, 8392, tinta=5, luz=(BLANCO, -14, 16, 0.4))
        rotulo(im, "NOBEL", mx, my - 16, int(36 * e) + 2, rgb("8a5a14"), t, seed=8393, tinta=False)
        rotulo(im, "1981", mx, my + 26, int(32 * e) + 2, rgb("8a5a14"), t, seed=8394, tinta=False)
        destello(im, mx + 110, my - 90, 0.9 * e, t, seed=1035)
    return im


def ingenieros(t):
    im = papel("frio")
    p = nina(im, 600, 640, 1.5, t, cara="normal", boca="abierta" if t > tNumeros else "sonrisa", brazos=(0.4, 2.3),
             codos=(0.3, 0.6), mira=1.0)
    kuri(im, 1420, 560, 2.2, t, cara="feliz" if t > tNumeros else "normal")
    e = e_back(pr(t, tIng, tIng + 0.3))
    # bombilla de idea sobre la niña
    bx, by = p["cabeza"][0], p["cabeza"][1] - 260
    forma(im, elipse(bx, by, 60 * e, 66 * e), rgb("fff2b8"), t, 8400, tinta=4)
    forma(im, rrect(bx, by + 76 * e, 50 * e, 30 * e, 6), rgb("9a9a9a"), t, 8401, tinta=3)
    brillo(im, bx, by, 130, AMARILLO, 0.5 * e)
    if t > tNumeros - 0.4:
        u = e_out(pr(t, tNumeros - 0.4, T_FIN))
        rotulo(im, "¿Y SI LO HACEMOS CON NÚMEROS?", W / 2, 140, 74, AMARILLO, t, seed=8410, esc=e_back(pr(t, tNumeros - 0.3, tNumeros)))
        for k in range(18):                                    # números que giran y forman una neurona
            a = k / 18 * 2 * math.pi + t
            r = lerp(260, 70, u)
            x, y = 1010 + r * math.cos(a), 600 + r * 0.8 * math.sin(a)
            rotulo(im, str((k * 37) % 10), x, y, 44, rgb("3f78c8"), t, seed=8420 + k, tinta=False, alfa=1 - 0.6 * u)
        if u > 0.6:                                            # los números se vuelven una neurona
            e2 = e_back(pr(u, 0.6, 1.0))
            forma(im, elipse(1010, 600, 46 * e2, 42 * e2), rgb("e9a0bd"), t, 8440, tinta=4)
            brillo(im, 1010, 600, 110, AMARILLO, 0.5 * e2)
    return im


TRAMOS = [(laboratorio, T_INI), (piramide, tUnas - 0.4), (ingenieros, tIng - 0.4)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * 0.7, H * 0.4)
        else:
            import plano_b
            im = desborde(plano_b.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.3, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
