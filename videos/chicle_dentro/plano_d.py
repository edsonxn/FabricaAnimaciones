# -*- coding: utf-8 -*-
"""ESTÓMAGO: la bolita cae al lago de jugo gástrico («¿7 AÑOS?») → regla de pH con el limón → pepsina (pac-man) que
corta proteínas → el estómago revuelve: el pan y el bistec se deshacen, el chicle NO (la pepsina rebota: «¡BOING!») →
capa de MOCO brillante + recuadro seco/mojado → reloj «cada 1½-2 h» → la ESCOBA (onda que barre) se lleva al chicle
hacia la salida (píloro)."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, ww
from fondos_chicle import estomago
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, BLANCO, burbuja, destello, exclama, kuri
from piezas_chicle import (MOCO, ROJO, bistec, calendario, chicle, enzima, escoba, limon, pan, proteina)

T_INI = T0("estomago")
E = "estomago"
tMito, tSiete, tVeamos = ww(E, 0, "mito"), ww(E, 0, "siete"), ww(E, 0, "veamos")
tBolsa, tJugo, tAcido, tLimon = ww(E, 1, "bolsa"), ww(E, 1, "jugo"), ww(E, 1, "clorhidrico"), ww(E, 1, "limon")
tEnzimas, tPepsina, tCortan, tPedacitos = ww(E, 2, "enzimas"), ww(E, 2, "pepsina"), ww(E, 2, "cortan"), ww(E, 2, "pedacitos")
tAprieta, tHoras, tPan, tBistec = ww(E, 3, "aprieta"), ww(E, 3, "horas"), ww(E, 3, "pan"), ww(E, 3, "bistec")
tYel, tNada, tRomper, tIgual = ww(E, 4, "chicle"), ww(E, 4, "nada"), ww(E, 4, "romper"), ww(E, 4, "igualito")
tPega, tMoco, tSecas = ww(E, 5, "pega"), ww(E, 5, "moco"), ww(E, 5, "secas")
tLimpieza, tHora, tOnda, tBarre = ww(E, 6, "limpieza"), ww(E, 6, "hora"), ww(E, 6, "onda"), ww(E, 6, "barre")
tComplejo, tEscoba, tLleva = ww(E, 7, "complejo"), ww(E, 7, "escoba"), ww(E, 7, "lleva")

GX, GY = 900, 770                     # la bolita flotando en el jugo
PX, PY = 1790, 470                    # salida (píloro)


def _gum(t):
    cae = e_out(pr(t, T_INI, T_INI + 1.2))
    x = lerp(300, GX, cae)
    y = lerp(80, GY, e_in(pr(t, T_INI, T_INI + 1.2)))
    y += 8 * math.sin(t * 2.2)
    v = suave(pr(t, tBarre - 0.6, tLleva + 0.6))                           # la onda la arrastra a la salida
    x, y = lerp(x, PX, v), lerp(y, PY, v)
    return x, y, 1 - 0.6 * pr(t, tLleva + 0.2, tLleva + 0.8)


def reloj(im, x, y, r, t, seed=9700, vel=6.0):
    forma(im, elipse(x, y, r, r), BLANCO, t, seed, tinta=4)
    for k in range(12):
        a = k * math.pi / 6
        linea(im, [(x + 0.8 * r * math.cos(a), y + 0.8 * r * math.sin(a)), (x + 0.92 * r * math.cos(a), y + 0.92 * r * math.sin(a))],
              2.4, seed=seed + 1 + k, t=t, punta=False)
    a = t * vel
    linea(im, [(x, y), (x + 0.75 * r * math.sin(a), y - 0.75 * r * math.cos(a))], 5, seed=seed + 20, t=t)
    linea(im, [(x, y), (x + 0.5 * r * math.sin(a / 12), y - 0.5 * r * math.cos(a / 12))], 7, seed=seed + 21, t=t)


def cuadro_crudo(t):
    im = estomago()
    # revuelve: olas en el jugo
    rev = pr(t, tAprieta - 0.3, tAprieta + 0.3) * (1 - pr(t, tYel, tYel + 0.5))
    for k in range(6):
        x = (k * 340 + t * 90) % (W + 300) - 150
        linea(im, curva([(x - 120, 770), (x, 750 - 30 * rev), (x + 120, 770)], 6), 5, col=rgb("eef08a"), seed=9600 + k, t=t,
              alfa=0.6, punta=False)
    for k in range(5):
        burbuja(im, 200 + k * 360 + 30 * math.sin(t + k), 900 - ((t * 60 + k * 70) % 160), 9 + k % 3, t, seed=9610 + k)
    # moco brillante en las paredes
    if t > tMoco - 0.4:
        a = pr(t, tMoco - 0.4, tMoco + 0.3)
        for k in range(3):
            lavado(im, curva([(-40, 60 + k * 230), (600, 30 + k * 230), (1200, 80 + k * 230), (W + 40, 40 + k * 230),
                              (W + 40, 120 + k * 230), (1200, 150 + k * 230), (600, 110 + k * 230), (-40, 130 + k * 230)], 6, True),
                   MOCO, 0.5 * a, 9620 + k)
            linea(im, curva([(100, 70 + k * 230), (700, 50 + k * 230), (1300, 90 + k * 230)], 6), 4, col=BLANCO,
                  seed=9625 + k, t=t, alfa=0.6 * a, punta=False)
        if t < tLimpieza:
            rotulo(im, "MOCO RESBALOSO", 960, 330, 72, rgb("8aa62a"), t, seed=9630, esc=e_back(pr(t, tMoco - 0.2, tMoco + 0.1)))
    # pan y bistec que se deshacen
    if tAprieta - 0.5 < t < tNada + 0.6:
        e = e_back(pr(t, tAprieta - 0.5, tAprieta - 0.2))
        pan(im, 380, 760, 2.3 * e + 0.01, t, deshace=pr(t, tPan, tPan + 1.0))
        bistec(im, 1450, 765, 2.3 * e + 0.01, t, deshace=pr(t, tBistec, tBistec + 1.0))
        if tPan < t < tBistec + 1.0:
            rotulo(im, "SE DESHACE", 380, 540, 64, BLANCO, t, seed=9640, esc=e_back(pr(t, tPan, tPan + 0.2)))
        if t > tBistec:
            rotulo(im, "SE DESHACE", 1450, 540, 64, BLANCO, t, seed=9641, esc=e_back(pr(t, tBistec, tBistec + 0.2)))
    # pepsina y proteínas
    if tEnzimas - 0.3 < t < tAprieta:
        e = e_back(pr(t, tEnzimas - 0.3, tEnzimas))
        corte = 3 if t > tCortan else None
        proteina(im, 1380, 520, 2.5 * e + 0.01, t, corte=corte, sep=pr(t, tCortan, tPedacitos))
        abre = 0.5 + 0.5 * math.sin(t * 12)
        enzima(im, lerp(1800, 1380, e_out(pr(t, tPepsina, tCortan))), 400, 3.4 * e + 0.01, t, abre=abre)
        rotulo(im, "PEPSINA", 1640, 200, 84, rgb("4f86c6"), t, seed=9650, esc=e_back(pr(t, tPepsina - 0.2, tPepsina + 0.1)))
        rotulo(im, "PROTEÍNAS", 1380, 640, 60, BLANCO, t, seed=9651, esc=e)
    # regla de pH
    if tAcido - 0.4 < t < tEnzimas:
        e = e_back(pr(t, tAcido - 0.4, tAcido))
        x0, y0 = 300, 330
        cols = ["e35d4a", "ef7b3c", "f2bf35", "e8d34a", "c8d94a", "8fd18a", "5ab88a", "4fb3b0", "4f86c6", "6a5ad1"]
        for k in range(10):
            forma(im, rrect(x0 + k * 90 * e, y0, 86 * e + 1, 90 * e + 1, 8), rgb(cols[k]), t, 9660 + k, tinta=2.4)
        rotulo(im, "ÁCIDO", x0, y0 + 95, 56, ROJO, t, seed=9671, esc=e)
        rotulo(im, "ÁCIDO CLORHÍDRICO", 1280, 130, 84, AMARILLO, t, seed=9672, esc=e)
        if t > tLimon - 0.3:
            el = e_back(pr(t, tLimon - 0.3, tLimon))
            limon(im, x0 + 140, y0 - 150, 1.5 * el + 0.01, t)
            forma(im, np.array([(x0 + 100, y0 - 60), (x0 + 150, y0 - 60), (x0 + 125, y0 - 45)], np.float32), TINTA, t, 9673, tinta=0)
            rotulo(im, "LIMÓN", x0 + 330, y0 - 150, 56, AMARILLO, t, seed=9675, esc=el)
        rotulo(im, "TU ESTÓMAGO", x0 + 40, y0 + 160, 52, BLANCO, t, seed=9674, esc=e)
    # reloj de «horas» y de «cada hora y media o dos»
    if tHoras - 0.3 < t < tPan:
        reloj(im, 1690, 260, 140 * e_back(pr(t, tHoras - 0.3, tHoras)) + 1, t, vel=10)
    if tHora - 0.4 < t < tBarre + 0.5:
        e = e_back(pr(t, tHora - 0.4, tHora)) * (1 - pr(t, tBarre, tBarre + 0.5))
        reloj(im, 1560, 280, 150 * e + 1, t, seed=9710, vel=4)
        rotulo(im, "CADA 1½ - 2 HORAS", 1560, 500, 64, AMARILLO, t, seed=9720, esc=e)
    if tLimpieza - 0.3 < t < tHora:
        el = e_back(pr(t, tLimpieza - 0.3, tLimpieza))
        escoba(im, 1500, 470, 1.9 * el + 0.01, t, rot=0.25 * math.sin(t * 5))
        for k in range(5):
            burbuja(im, 1380 + k * 60 + 20 * math.sin(t * 2 + k), 640 - ((t * 80 + k * 50) % 260), (14 + 4 * (k % 3)) * el + 1, t,
                    seed=9722 + k)
        rotulo(im, "SERVICIO DE LIMPIEZA", 960, 150, 84, AMARILLO, t, seed=9721, rot=-0.03,
               esc=e_back(pr(t, tLimpieza - 0.3, tLimpieza)))
    # la onda que barre (la escoba)
    if t > tOnda - 0.3:
        v = pr(t, tOnda - 0.3, tLleva + 1.2)
        xw = lerp(-300, W + 200, v)
        forma(im, curva([(xw - 260, H + 40), (xw - 200, 400), (xw - 60, 120), (xw + 20, 400), (xw + 60, H + 40)], 7, True),
              rgb("c0566a"), t, 9730, tinta=5, alfa=0.85, luz=(BLANCO, -20, 0, 0.25))
        if t > tEscoba - 0.3:
            escoba(im, xw - 40, 520, 1.6 * e_back(pr(t, tEscoba - 0.3, tEscoba)), t, rot=0.5 + 0.2 * math.sin(t * 8))
    if tComplejo - 0.3 < t < tEscoba + 0.2:
        forma(im, rrect(960, 150, 980, 110, 20), rgb("fbf3df"), t, 9740, tinta=4)
        rotulo(im, "COMPLEJO MOTOR MIGRATORIO", 960, 150, 56, rgb("2f4f86"), t, seed=9741, tinta=False,
               esc=e_back(pr(t, tComplejo - 0.3, tComplejo)))
    if t > tEscoba:
        rotulo(im, "= LA ESCOBA", 960, 150, 90, AMARILLO, t, seed=9742, esc=e_back(pr(t, tEscoba, tEscoba + 0.2)))
    # la bolita y Kuri
    gx, gy, gs = _gum(t)
    pica = pr(t, tRomper - 0.1, tRomper + 0.6)
    if 0 < pica < 1:                                                       # la pepsina intenta morderla y rebota
        enzima(im, gx + lerp(300, 130, math.sin(pica * math.pi)), gy - 60, 2.4, t, abre=0.5 + 0.5 * math.sin(t * 14))
        if pica > 0.5:
            rotulo(im, "¡BOING!", gx + 380, gy - 230, 80, BLANCO, t, seed=9750)
    cara = "normal" if t < tNada else ("feliz" if t < tBarre else "susto")
    chicle(im, gx, gy, 115 * gs, t, seed=9760, cara=cara)
    kuri(im, gx - 15 * gs, gy - 200 * gs, 1.45 * gs, t, cara="susto" if t < T_INI + 1.2 or t > tBarre else "normal", aura=False)
    if tNada + 0.3 < t < tPega:                                                  # ni el ácido ni las enzimas
        tA, tZ = ww(E, 4, "acido"), ww(E, 4, "enzimas")
        for k, (txt, x, tt, col) in enumerate([("ÁCIDO", 420, tA, AMARILLO), ("ENZIMAS", 1500, tZ, rgb("4f86c6"))]):
            if t > tt - 0.2:
                e = e_back(pr(t, tt - 0.2, tt + 0.1))
                rotulo(im, txt, x, 380, 84, col, t, seed=9810 + k, esc=e)
                marca_x(im, x, 380, 1.6 * e_back(pr(t, tRomper - 0.1, tRomper + 0.2)), t, seed=9812 + k)
        for k in range(6):                                                     # gotas de ácido que rebotan
            ph = (t * 0.9 + k / 6) % 1
            dx = (k - 2.5) * 70
            yy = 520 + 300 * ph if ph < 0.6 else 700 - 400 * (ph - 0.6)
            forma(im, elipse(gx + dx * (1 + ph), yy - 30, 12, 16), rgb("e8f04a"), t, 9820 + k, tinta=2, alfa=0.9)
    if tPega - 0.2 < t < tMoco - 0.2:
        rotulo(im, "¿SE PEGA?", 960, 170, 110, AMARILLO, t, seed=9830, rot=-0.04, esc=e_back(pr(t, tPega - 0.2, tPega + 0.1)))
        pregunta_ = e_back(pr(t, tPega, tPega + 0.3))
        rotulo(im, "?", gx + 200, gy - 300, 120, BLANCO, t, seed=9831, esc=pregunta_)
    if tNada - 0.2 < t < tPega:
        rotulo(im, "NADA", gx, gy - 430, 130, AMARILLO, t, seed=9770, esc=e_back(pr(t, tNada - 0.2, tNada + 0.1)))
        if t > tIgual - 0.2:
            destello(im, gx + 130, gy - 80, 1.6 * e_back(pr(t, tIgual - 0.2, tIgual)), t)
    if T_INI + 0.8 < t < tBolsa:
        calendario(im, 1500, 360, 1.7 * e_back(pr(t, tSiete - 0.3, tSiete)), t, "¿AÑOS?", "7")
        rotulo(im, "EL ESTÓMAGO", 520, 170, 96, AMARILLO, t, seed=9799, rot=-0.04, esc=e_back(pr(t, T_INI + 0.8, T_INI + 1.2)))
        if t > tVeamos - 0.2:
            exclama(im, gx + 180, gy - 380, e_back(pr(t, tVeamos - 0.2, tVeamos)), t)
    if tBolsa - 0.3 < t < tAcido - 0.3:                                         # bolsa de músculo y jugo gástrico
        e = e_back(pr(t, tBolsa - 0.3, tBolsa))
        rotulo(im, "BOLSA DE MÚSCULO", 520, 240, 70, BLANCO, t, seed=9800, esc=e)
        linea(im, [(520, 290), (560, 420)], 5 * e + 1, seed=9801, t=t)
        if t > tJugo - 0.3:
            ej = e_back(pr(t, tJugo - 0.3, tJugo))
            rotulo(im, "JUGO GÁSTRICO", 1450, 560, 70, AMARILLO, t, seed=9802, esc=ej)
            linea(im, [(1450, 610), (1400, 800)], 5 * ej + 1, seed=9803, t=t)
    # recuadro: seco vs mojado
    if tSecas - 1.0 < t < tLimpieza - 0.2:
        e = e_back(pr(t, tSecas - 1.0, tSecas - 0.7)) * (1 - pr(t, tLimpieza - 0.6, tLimpieza - 0.2))
        for k, (x, txt, col) in enumerate([(560, "SECO", rgb("c9a25a")), (1360, "MOJADO", rgb("8cc8ee"))]):
            forma(im, rrect(x, 520, 420 * e + 1, 300 * e + 1, 20), rgb("fbf3df"), t, 9780 + k, tinta=4)
            forma(im, rrect(x, 580, 340 * e + 1, 60 * e + 1, 8), col, t, 9782 + k, tinta=3)
            if k == 0:
                chicle(im, x, 545, 40 * e + 1, t, seed=9784)
                palomita(im, x + 130 * e, 430, 0.6 * e, t, seed=9785)
                rotulo(im, "SE PEGA", x, 700, 44, TINTA, t, seed=9786, tinta=False, esc=e)
            else:
                chicle(im, x - 60 + 120 * ((t * 0.8) % 1), 545, 40 * e + 1, t, seed=9787)
                marca_x(im, x + 130 * e, 430, 0.5 * e, t, seed=9788)
                rotulo(im, "SE RESBALA", x, 700, 44, TINTA, t, seed=9789, tinta=False, esc=e)
            rotulo(im, txt, x, 420, 56, col * 0.7, t, seed=9790 + k, esc=e)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
