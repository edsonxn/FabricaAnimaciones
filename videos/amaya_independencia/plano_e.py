# -*- coding: utf-8 -*-
"""ETAPA 1 · INICIO (1810-1811, Hidalgo): Hidalgo y su ejército del pueblo (palos, machetes, hondas) → la Alhóndiga de
Granaditas y el Pípila con la losa en la espalda y la antorcha; la puerta arde → el camino: Monte de las Cruces ✓, Ciudad de
México (se dan la vuelta), Puente de Calderón ✗ → 1811: capturado y fusilado → la cadena de la esclavitud se rompe."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave,
                      terminar)
from comun import T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import marca_x, palomita, estrella
from personajes import AMARILLO, destello, exclama
from utileria import flecha
from kit_amaya import (AZUL, CAFE, CREMA, DORADO, GRIS, ROJO, VERDE, cache, cam, chispas, entra, gente, letrero, papa, tarjeta)

T_INI = T0("inicio")
C = "inicio"
tUno, tHid, tMil, tEjer, tGente, tPalos, tMach, tHond = (ww(C, 0, "uno"), ww(C, 0, "hidalgo"), ww(C, 0, "mil"), ww(C, 0, "ejercito"),
                                                         ww(C, 0, "gente"), ww(C, 0, "palos"), ww(C, 0, "machetes"),
                                                         ww(C, 0, "hondas"))
tGto, tAlh, tMinero, tPip, tLosa, tFuego, tPuerta = (ww(C, 1, "guanajuato"), ww(C, 1, "alhondiga"), ww(C, 1, "minero"),
                                                     ww(C, 1, "pipila"), ww(C, 1, "losa"), ww(C, 1, "fuego"), ww(C, 1, "puerta"))
tGanaron, tMonte, tEntraron, tCiudad, tPerd, tCald = (ww(C, 2, "ganaron"), ww(C, 2, "monte"), ww(C, 2, "entraron"),
                                                      ww(C, 2, "ciudad"), ww(C, 2, "perdieron"), ww(C, 2, "calderon"))
tMil11, tCapt, tFus, tAntes, tDecr, tEscl = (ww(C, 3, "mil"), ww(C, 3, "capturaron"), ww(C, 3, "fusilaron"), ww(C, 3, "antes"),
                                             ww(C, 3, "decretar"), ww(C, 3, "esclavitud"))
T_ALH = tGto - 0.5
T_RUTA = tGanaron - 0.5
T_FIN = tMil11 - 0.5
COL = rgb("f6a6a0")


def cabecera(im, t):
    forma(im, rrect(330, 70, 560, 90, 20), COL, t, 13000, tinta=4)
    rotulo(im, "1 · INICIO · 1810-1811", 330, 74, 46, TINTA, t, seed=13001, tinta=False)


def ejercito(t):
    im = cache("e_ej", lambda: papel("calido")).copy()
    _manchas(im, rgb("f2c9a0"), 0, 1)
    forma(im, np.array([(0, 820), (W, 800), (W, H), (0, H)], np.float32), rgb("d9c08e"), 0, 13010, tinta=0)
    cabecera(im, t)
    cam(im, "hidalgo", 420, 450, 0.95 * entra(t, tHid - 0.3), t, "MIGUEL HIDALGO", seed=50)
    if t > tGente - 0.4:
        for k in range(8):
            u = entra(t, tGente - 0.4 + 0.08 * k)
            x, y = 740 + 105 * k, 780 + 40 * (k % 2)
            gente(im, x, y, 2.4 * u + 0.01, t, seed=80 + k, cara="grito")
            arma = k % 3
            tt = [tPalos, tMach, tHond][arma]
            if t > tt - 0.2:
                ea = entra(t, tt - 0.2)
                bx, by = x + 52, y - 10
                if arma == 0:
                    linea(im, [(bx, by + 60), (bx + 20 * ea, by - 110 * ea)], 9, CAFE, seed=13020 + k, t=t)
                elif arma == 1:
                    forma(im, np.array([(bx, by + 30), (bx + 10, by + 30), (bx + 30 * ea, by - 90 * ea), (bx + 8 * ea, by - 80 * ea)], np.float32),
                          rgb("c8ccd4"), t, 13030 + k, tinta=2.5)
                else:
                    a = t * 12 + k
                    linea(im, [(bx, by + 20), (bx + 40 * math.cos(a) * ea, by - 40 + 40 * math.sin(a) * ea)], 3, CAFE, seed=13040 + k, t=t)
                    forma(im, elipse(bx + 40 * math.cos(a) * ea, by - 40 + 40 * math.sin(a) * ea, 9, 9), GRIS, t, 13045 + k, tinta=2)
    for k, (tt, txt) in enumerate(((tPalos, "PALOS"), (tMach, "MACHETES"), (tHond, "HONDAS"))):
        if t > tt - 0.2:
            letrero(im, txt, 1000 + 330 * k, 380, 50, t, col=CREMA, seed=13050 + k * 5, esc=entra(t, tt - 0.2), rot=(k - 1) * 0.05)
    if tUno - 0.3 < t < tGente - 0.3:
        e1 = entra(t, tUno - 0.3)
        rotulo(im, "1", 1150, 420, 300, COL, t, seed=13061, esc=e1)
        rotulo(im, "INICIO", 1150, 680, 140, ROJO, t, seed=13062, esc=entra(t, tUno + 0.5))
        letrero(im, "1810 – 1811", 1150, 840, 60, t, col=CREMA, seed=13063, esc=entra(t, tMil - 0.2))
    if t > tGente - 0.3:
        rotulo(im, "GENTE DEL PUEBLO", 1250, 230, 70, ROJO, t, seed=13060, esc=entra(t, tGente - 0.3))
    return im


def fuego(im, x, y, s, t, seed=13100):
    for k in range(5):
        a = t * 9 + k * 1.7
        h = (120 + 40 * math.sin(a)) * s
        dx = (k - 2) * 34 * s
        forma(im, curva([(x + dx - 30 * s, y), (x + dx, y - h), (x + dx + 30 * s, y)], 6, True),
              rgb("f08a2a") if k % 2 else rgb("f6c64a"), t, seed + k, tinta=2.5)
    brillo(im, x, y - 60 * s, 260 * s, rgb("ffb060"), 0.5)


def alhondiga(t):
    def f():
        im = papel("sepia")
        forma(im, np.array([(0, 860), (W, 850), (W, H), (0, H)], np.float32), rgb("cbb58a"), 0, 13110, tinta=0)
        forma(im, rrect(1150, 560, 1000, 560, 10), rgb("d8c39a"), 0, 13111, tinta=6, sombra=(rgb("b09a70"), 30, 0, 0.5))
        for r in range(4):
            for c in range(7):
                forma(im, rrect(720 + c * 145, 340 + r * 120, 110, 70, 6), rgb("c9b088"), 0, 13120 + r * 7 + c, tinta=2)
        forma(im, rrect(1150, 280, 1040, 40, 6), rgb("b89a6a"), 0, 13150, tinta=4)
        return im
    im = cache("e_alh", f).copy()
    cabecera(im, t)
    letrero(im, "ALHÓNDIGA DE GRANADITAS", 1150, 190, 52, t, col=CREMA, seed=13160, esc=entra(t, tAlh - 0.2))
    letrero(im, "GUANAJUATO", 330, 190, 44, t, col=AMARILLO, seed=13165, esc=entra(t, tGto - 0.2))
    arde = pr(t, tFuego - 0.2, tFuego + 0.4)
    forma(im, rrect(1150, 740, 220, 230, 30), rgb("5a3a22") if arde < 1 else rgb("3a2a1a"), t, 13170, tinta=4)    # puerta
    if arde > 0:
        fuego(im, 1150, 850, 1.3 * arde, t)
    # el Pípila: camina con la losa en la espalda y la antorcha
    if t > tMinero - 0.4:
        u = e_out(pr(t, tMinero - 0.4, tFuego - 0.2))
        x = 260 + (960 - 260) * u
        y = 760 + 8 * abs(math.sin(t * 8)) * (u < 1)
        if t > tLosa - 0.3:
            forma(im, rrect(x - 75, y + 20, 190, 170, 10, -0.2), rgb("9a9aa2"), t, 13180, tinta=4, sombra=(rgb("6a6a72"), 20, 10, 0.5))
        gente(im, x, y, 3.2, t, seed=91, cara="enojo", col=rgb("6a8a4a"))
        linea(im, [(x + 70, y + 60), (x + 120, y - 50)], 9, CAFE, seed=13185, t=t)
        fuego(im, x + 122, y - 50, 0.35, t, seed=13190)
        if t > tPip - 0.2:
            letrero(im, "EL PÍPILA", x, y - 160, 50, t, col=AMARILLO, seed=13195, esc=entra(t, tPip - 0.2))
    return im


def ruta(t):
    im = cache("e_ruta", lambda: papel("frio")).copy()
    cabecera(im, t)
    pts = [(280, 640), (820, 520), (1340, 640)]
    linea(im, curva([(140, 700), (280, 640), (550, 560), (820, 520), (1080, 560), (1340, 640), (1500, 700)], 12), 8, rgb("8a7a5a"),
          seed=13200, t=t, alfa=0.5)
    nombres = [("MONTE DE LAS CRUCES", tMonte, VERDE), ("CIUDAD DE MÉXICO", tCiudad, AZUL), ("PUENTE DE CALDERÓN", tCald, ROJO)]
    for k, ((x, y), (nom, tk, col)) in enumerate(zip(pts, nombres)):
        e = entra(t, tk - 0.4)
        forma(im, elipse(x, y, 70 * e + 1, 70 * e + 1), col, t, 13210 + k, tinta=4)
        if e > 0.2:
            letrero(im, nom, x, y + 150, 44, t, col=CREMA, seed=13215 + k * 5, esc=e)
    if t > tMonte + 0.3:
        palomita(im, 280, 630, 1.4 * entra(t, tMonte + 0.3), t, seed=13230, col=CREMA)
        rotulo(im, "¡GANARON!", 280, 400, 64, VERDE, t, seed=13231, esc=entra(t, tMonte + 0.3))
    # el ejército (bandera) avanza hacia la ciudad y se da la vuelta; luego va a Calderón
    if t > tEntraron - 0.4:
        u = pr(t, tEntraron - 0.4, tEntraron + 0.6)
        v = pr(t, tEntraron + 0.7, tPerd)
        x = 280 + 440 * math.sin(math.pi * u) * (1 - v) + (1060 * e_out(v))
        y = 620 - 100 * math.sin(math.pi * u) * (1 - v) + 40 * v
        linea(im, [(x, y), (x, y - 120)], 6, CAFE, seed=13240, t=t)
        forma(im, np.array([(x, y - 120), (x + 80, y - 100), (x, y - 70)], np.float32), ROJO, t, 13241, tinta=3)
        if 0.3 < u and v < 0.1:
            rotulo(im, "NO ENTRARON", 820, 360, 60, AZUL, t, seed=13245, esc=entra(t, tEntraron + 0.1))
    if t > tCald:
        marca_x(im, 1340, 640, 1.5 * entra(t, tCald), t, seed=13250, col=CREMA)
        rotulo(im, "PERDIERON", 1340, 420, 64, ROJO, t, seed=13251, esc=entra(t, tCald))
    return im


def cadena(im, x, y, t, rompe, seed=13300):
    for k in range(-4, 5):
        if k == 0:
            continue
        lado = -1 if k < 0 else 1
        dx = lado * 160 * e_out(rompe)
        dy = 60 * e_in(rompe) * abs(k) / 4
        cx = x + k * 95 + dx
        cy = y + dy
        rot = lado * 0.4 * rompe if k % 2 else 0
        linea(im, np.array([(cx + 60 * math.cos(a) * (1 if k % 2 else 0.6), cy + 30 * math.sin(a) * (1 if k % 2 == 0 else 0.6))
                            for a in np.linspace(0, 2 * math.pi, 30)]), 14, rgb("6a6a74"), seed=seed + k, t=t, cerrado=True, punta=False)


def final(t):
    im = cache("e_fin", lambda: papel("rosa")).copy()
    cabecera(im, t)
    gris = 1 - 0.0 * pr(t, tCapt, tCapt + 1)
    cam(im, "hidalgo", 400, 480, 0.8, t, "1811", seed=51)
    if t > tCapt - 0.3:
        letrero(im, "CAPTURADO", 1000, 300, 72, t, col=CREMA, seed=13400, esc=entra(t, tCapt - 0.3), rot=-0.04)
    if t > tFus - 0.3:
        letrero(im, "Y FUSILADO", 1000, 440, 72, t, col=CREMA, txt=ROJO, seed=13405, esc=entra(t, tFus - 0.3), rot=0.03)
    if t > tAntes - 0.4:
        e = entra(t, tAntes - 0.4)
        rompe = pr(t, tEscl - 0.1, tEscl + 0.5)
        cadena(im, 1020, 720, t, rompe)
        if rompe > 0:
            chispas(im, 1020, 720, 220, t, tEscl, seed=13410, col=AMARILLO)
            rotulo(im, "¡FIN DE LA ESCLAVITUD!", 960, 920, 76, VERDE, t, seed=13420, esc=entra(t, tEscl))
        if t > tDecr - 0.3:
            letrero(im, "DECRETO", 1400, 600, 46, t, col=AMARILLO, seed=13430, esc=entra(t, tDecr - 0.3), rot=0.06)
    return im


TRAMOS = [(T_INI, ejercito), (T_ALH, alhondiga), (T_RUTA, ruta), (T_FIN, final)]


def _base(t):
    from comun import desborde
    i = max(k for k, (t0, _) in enumerate(TRAMOS) if t >= t0 or k == 0)
    t0, f = TRAMOS[i]
    if i > 0 and t < t0 + 0.6:
        return desborde(TRAMOS[i - 1][1](t), f(t), pr(t, t0, t0 + 0.6), W / 2, H / 2)
    return f(t)


def cuadro_crudo(t):
    im = _base(t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
