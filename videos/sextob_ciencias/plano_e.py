# -*- coding: utf-8 -*-
"""DEFENSA: el sistema inmunitario.
intro: SISTEMA INMUNITARIO = INMUNOLÓGICO = DE DEFENSA, con la foto real de su cuaderno y un escudo que late.
invasores: un niño grande con escudo; llegan BACTERIAS, HONGOS, VIRUS y SUSTANCIAS EXTRAÑAS (frasco con calavera) y rebotan.
castillo: TU CUERPO = UN CASTILLO; 1.ª BARRERA = LAS MURALLAS: PIEL · VELLOS · SUDOR · LÁGRIMAS · MOCO (cada una con su dibujo);
un virus choca contra la muralla y rebota; el MOCO sale con capa roja de héroe.
innata: INMUNIDAD INNATA = NACES CON ELLA, con un bebé envuelto que ya trae su escudito."""
import math

import numpy as np

from acuarela import H, W, TINTA, brillo, curva, e_out, elipse, forma, lavado, linea, mancha_pts, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from comun_ci import cartel, titulo
from fondos_amaya import papel
from iconos_ia import palomita
from personajes import AMARILLO, destello, exclama, gota
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, cara_p, chispas, entra, gente, letrero, papa, tarjeta
from piezas_es import ROSA_M, polaroid
from piezas_fj import base, montanas
from piezas_ci import MOCO, PIEL, ROSA, _ojos, bacteria, castillo, hongo, virus
from utileria import calavera

T_INI = T0("defensa")
D = "defensa"
tUlt, tSist, tInmuno, tDef = ww(D, 0, "ultimo"), ww(D, 0, "sistema"), ww(D, 0, "inmunologico"), ww(D, 0, "defensa")
T_INV = ww(D, 1, "es") - 0.3
tDefiende, tInvas, tBact, tHong, tVir, tSust = (ww(D, 1, "defiende"), ww(D, 1, "invasores"), ww(D, 1, "bacterias"),
                                                ww(D, 1, "hongos"), ww(D, 1, "virus"), ww(D, 1, "sustancias"))
T_CAS = ww(D, 2, "imaginen") - 0.3
tCast, tPrim, tMur = ww(D, 2, "castillo"), ww(D, 2, "primera"), ww(D, 2, "murallas")
MUROS = [("PIEL", ww(D, 2, "piel")), ("VELLOS", ww(D, 2, "vellos")), ("SUDOR", ww(D, 2, "sudor")),
         ("LÁGRIMAS", ww(D, 2, "lagrimas")), ("MOCO", ww(D, 2, "mucosa"))]
tMoco, tMoco2, tHeroe = ww(D, 2, "moco"), ww(D, 2, "moco", 1), ww(D, 2, "heroe")
T_INN = ww(D, 3, "a") - 0.3
tLlama, tInnata, tInnata2, tNaces = ww(D, 3, "inmunidad"), ww(D, 3, "innata"), ww(D, 3, "innata", 1), ww(D, 3, "naces")


def escudo(im, x, y, s, t, seed, col=AZUL, cruz=True):
    pts = curva([(x - 90 * s, y - 100 * s), (x, y - 125 * s), (x + 90 * s, y - 100 * s), (x + 80 * s, y + 20 * s), (x, y + 120 * s),
                 (x - 80 * s, y + 20 * s)], 8, True)
    forma(im, np.array(pts, np.float32), col, t, seed, tinta=5 * s, luz=(rgb("ffffff"), -30 * s, -40 * s, 0.35))
    if cruz:
        forma(im, rrect(x, y - 5 * s, 36 * s, 130 * s, 6 * s), CREMA, t, seed + 1, tinta=0)
        forma(im, rrect(x, y - 15 * s, 110 * s, 34 * s, 6 * s), CREMA, t, seed + 2, tinta=0)


def frasco(im, x, y, s, t, seed):
    """Sustancia extraña: frasco morado con calavera."""
    forma(im, rrect(x, y - 95 * s, 44 * s, 40 * s, 6 * s), GRIS, t, seed, tinta=3 * s)
    forma(im, mancha_pts(x, y, 80 * s, seed + 1, 0.05), rgb("9a6ad0"), t, seed + 2, tinta=4 * s, luz=(rgb("ffffff"), -25 * s, -25 * s, 0.4))
    calavera(im, x, y + 5 * s, 0.55 * s, t, seed=seed + 3)


# ------------------------------------------------------------ intro
def intro(t):
    im = cache("e_int", lambda: papel("frio")).copy()
    titulo(im, "ÚLTIMO TEMA (Y EL MÁS LARGO)", t, tUlt, 25000, col=MORADO, x=640, y=100, px=56)
    if t > tSist - 0.3:
        polaroid(im, "inmune1", 1480, 330, entra(t, tSist - 0.3), t, rot=0.05, seed=25005, alto=290)
    late = 1 + 0.05 * math.sin(t * 5) * (t > tDef)
    e = entra(t, tUlt + 0.2)
    if e > 0.01:
        escudo(im, 260, 520, 1.1 * e * late, t, 25010)
    nombres = [("SISTEMA INMUNITARIO", tSist, ROJO), ("SISTEMA INMUNOLÓGICO", tInmuno, AZUL), ("SISTEMA DE DEFENSA", tDef, VERDE)]
    for k, (txt, tk, col) in enumerate(nombres):
        if t > tk - 0.3:
            letrero(im, txt, 700, 340 + 170 * k, 52, t, col=col, txt=CREMA, seed=25020 + k * 5, esc=entra(t, tk - 0.3),
                    rot=(k % 2 - 0.5) * 0.04)
        if k and t > tk - 0.3:
            rotulo(im, "=", 700, 255 + 170 * k, 64, TINTA, t, seed=25040 + k, tinta=False, esc=entra(t, tk - 0.3))
    if t > tDef - 0.2:
        rotulo(im, "¡3 NOMBRES, 1 SISTEMA!", 700, 900, 54, MORADO, t, seed=25050, esc=entra(t, tDef + 0.5))
    chispas(im, 260, 520, 170, t, tDef, seed=25060, col=AMARILLO)
    return im


# ------------------------------------------------------------ invasores
INV = [("BACTERIAS", -1.0), ("HONGOS", -1.0), ("VIRUS", 1.0), ("SUSTANCIAS EXTRAÑAS", 1.0)]


def invasores(t):
    im = cache("e_inv", lambda: papel("calido")).copy()
    titulo(im, "DEFIENDE AL CUERPO DE INVASORES", t, tDefiende, 25100, col=ROJO, x=700, y=100, px=60)
    cx, cy = 760, 600
    gente(im, cx, cy + 40, 5.0, t, seed=25110, cara="normal")
    if t > tDefiende - 0.2:
        escudo(im, cx + 150, cy + 60, 0.75 * entra(t, tDefiende - 0.2), t, 25115)
    puestos = [(260, 330, tBact), (300, 760, tHong), (1260, 330, tVir), (1250, 650, tSust)]
    for k, ((x, y, tk), (txt, lado)) in enumerate(zip(puestos, INV)):
        if t <= tk - 0.4:
            continue
        u = pr(t, tk - 0.4, tk + 0.3)
        # llega volando desde afuera, choca con el escudo invisible y rebota un poco
        rb = 22 * math.sin(max(0.0, t - tk - 0.3) * 4) * math.exp(-max(0.0, t - tk - 0.3) * 0.8)
        dx = (1 - e_out(u)) * 400 * (-1 if x < cx else 1)
        X, Y = x + dx + rb * (-1 if x < cx else 1), y + 6 * math.sin(t * 3 + k)
        if k == 0:
            bacteria(im, X, Y, 1.25, t, seed=25120)
        elif k == 1:
            hongo(im, X, Y, 1.15, t, seed=25130)
        elif k == 2:
            virus(im, X, Y, 1.4, t, seed=25140)
        else:
            frasco(im, X, Y, 1.3, t, 25150)
        rotulo(im, txt, x, y + (150 if k != 1 else 170), 44 if k < 3 else 38, ROJO, t, seed=25160 + k, esc=entra(t, tk - 0.2))
    if t > tInvas - 0.3:
        letrero(im, "INVASORES", cx, 960, 50, t, col=ROJO, txt=CREMA, seed=25170, esc=entra(t, tInvas - 0.3), rot=0.03)
    return im


# ------------------------------------------------------------ castillo
def _fondo_cast():
    im = papel("calido")
    lavado(im, rrect(W / 2, 260, W, 520, 0), rgb("bfe0f0"), 0.5, 25201)
    montanas(im, 0, seed=25202, y0=820)
    lavado(im, rrect(W / 2, 1000, W, 220, 0), rgb("8fc06a"), 0.55, 25203)
    return im


def moco_heroe(im, x, y, s, t, seed):
    """El moco con capa roja de héroe que ondea y un brazo arriba."""
    ond = math.sin(t * 6)
    capa = [(x - 40 * s, y - 50 * s), (x + 40 * s, y - 50 * s), (x + 120 * s + 20 * s * ond, y + 90 * s), (x - 20 * s, y + 110 * s + 10 * s * ond)]
    forma(im, np.array(curva(capa, 6, True), np.float32), ROJO, t, seed, tinta=4 * s)
    forma(im, mancha_pts(x, y + 10 * s, 80 * s, seed + 1, 0.12), MOCO, t, seed + 2, tinta=4.5 * s,
          luz=(rgb("ffffff"), -25 * s, -25 * s, 0.55))
    _ojos(im, x, y, s * 0.9, t, seed + 3, "feliz")
    linea(im, [(x - 70 * s, y + 10 * s), (x - 110 * s, y - 70 * s + 8 * s * ond)], 9 * s, MOCO, seed=seed + 4, t=t)
    forma(im, elipse(x - 112 * s, y - 78 * s, 14 * s, 14 * s), MOCO, t, seed + 5, tinta=2.5 * s)
    forma(im, rrect(x, y + 50 * s, 40 * s, 30 * s, 6 * s), AMARILLO, t, seed + 6, tinta=2 * s)
    rotulo(im, "M", x, y + 52 * s, 26 * s, ROJO, t, seed=seed + 7, tinta=False)


def _icono_muro(im, k, x, y, t, seed):
    if k == 0:          # piel: mano
        forma(im, elipse(x, y + 8, 30, 26), PIEL, t, seed, tinta=3)
        for j in range(4):
            forma(im, rrect(x - 21 + 14 * j, y - 24, 11, 34, 5), PIEL, t, seed + 1 + j, tinta=2.5)
    elif k == 1:        # vellos
        forma(im, rrect(x, y + 14, 80, 22, 8), PIEL, t, seed, tinta=3)
        for j in range(6):
            linea(im, [(x - 32 + 13 * j, y + 4), (x - 30 + 13 * j + 6 * math.sin(t * 3 + j), y - 32)], 3, rgb("5a3a2a"), seed=seed + 1 + j, t=t)
    elif k == 2:        # sudor
        for j in range(3):
            gota(im, x - 22 + 22 * j, y - 6 + 10 * math.sin(t * 4 + j), 0.5, t, seed=seed + j)
    elif k == 3:        # lágrimas: ojito que llora
        forma(im, elipse(x, y - 8, 30, 18), CREMA, t, seed, tinta=3)
        forma(im, elipse(x, y - 8, 10, 12), TINTA, t, seed + 1, tinta=0)
        gota(im, x + 14, y + 24 + 8 * ((t * 1.5) % 1), 0.4, t, seed=seed + 2)
    else:               # moco
        forma(im, mancha_pts(x, y, 26, seed, 0.2), MOCO, t, seed + 1, tinta=3)


def castillo_t(t):
    im = cache("e_cas", _fondo_cast).copy()
    titulo(im, "TU CUERPO = UN CASTILLO", t, tCast, 25200, col=MORADO, x=760, y=90, px=66)
    s = 0.95 * (0.85 + 0.15 * e_out(pr(t, T_CAS, T_CAS + 0.8)))
    castillo(im, 760, 940, s, t, seed=25210)
    if t > tPrim - 0.3:
        letrero(im, "1.ª BARRERA: LAS MURALLAS", 760, 190, 46, t, col=AMARILLO, seed=25220, esc=entra(t, tPrim - 0.3), rot=-0.02)
    if t > tMur - 0.2:
        brillo(im, 760 - 285 * s, 720, 220, rgb("fff3a0"), 0.35 * pr(t, tMur - 0.2, tMur + 0.4))
        brillo(im, 760 + 285 * s, 720, 220, rgb("fff3a0"), 0.35 * pr(t, tMur - 0.2, tMur + 0.4))
    # virus que cae sobre la muralla central y rebota, cada 2.4 s
    if t > tMur:
        c = ((t - tMur) % 2.4) / 2.4
        yw = 940 - 360 * s - 60
        if c < 0.45:
            u = c / 0.45
            X, Y = 1060 - 160 * u, 420 + (yw - 420) * u * u
        else:
            u = (c - 0.45) / 0.55
            X, Y = 900 + 180 * u, yw - 260 * math.sin(u * math.pi * 0.8)
        virus(im, X, Y, 0.6, t, seed=25230, cara="susto" if c > 0.45 else "enojo")
        if 0.42 < c < 0.62:
            destello(im, 900, yw + 30, 1.1, t, seed=25235)
            rotulo(im, "¡BOING!", 980, yw - 90, 44, ROJO, t, seed=25236, rot=0.1)
    pos = [(230, 330), (230, 520), (230, 710), (1290, 330), (1290, 520)]
    for k, ((txt, tk), (x, y)) in enumerate(zip(MUROS, pos)):
        if t <= tk - 0.3:
            continue
        e = entra(t, tk - 0.3)
        tarjeta(im, x, y, 330 * e, 130 * e, t, CREMA, 25240 + k * 7, rot=(k % 2 - 0.5) * 0.04)
        if e > 0.6:
            _icono_muro(im, k, x - 100, y, t, 25250 + k * 10)
        rotulo(im, txt, x + 45, y + 4, (38 if len(txt) > 6 else 44) * e + 1, VERDE if k == 4 else TINTA, t, seed=25241 + k * 7,
               tinta=False)
    if t > tMoco2 - 0.3:
        e = entra(t, tMoco2 - 0.3)
        moco_heroe(im, 1290, 760 - 20 * abs(math.sin(t * 3)), 1.3 * e, t, 25300)
        if t > tHeroe - 0.3:
            rotulo(im, "¡EL MOCO ES UN HÉROE!", 1060, 960, 50, VERDE, t, seed=25310, esc=entra(t, tHeroe - 0.3), rot=-0.03)
            chispas(im, 1290, 760, 160, t, tHeroe, seed=25315, col=AMARILLO)
    return im


# ------------------------------------------------------------ innata
def bebe(im, x, y, s, t, seed):
    """Bebé envuelto en su cobijita, con chupón."""
    forma(im, mancha_pts(x, y + 70 * s, 110 * s, seed, 0.06, ry=150 * s), rgb("a9d4f2"), t, seed + 1, tinta=4.5 * s)
    for k in range(3):
        linea(im, [(x - 90 * s, y + (40 + 50 * k) * s), (x + 90 * s, y + (60 + 50 * k) * s)], 3 * s, rgb("7fb0d8"), seed=seed + 2 + k, t=t,
              alfa=0.6)
    forma(im, elipse(x, y - 70 * s, 78 * s, 74 * s), PIEL, t, seed + 6, tinta=4.5 * s, luz=(rgb("ffffff"), -20 * s, -20 * s, 0.35))
    lavado(im, elipse(x - 40 * s, y - 50 * s, 16 * s, 10 * s), ROSA, 0.6, seed + 7)
    lavado(im, elipse(x + 40 * s, y - 50 * s, 16 * s, 10 * s), ROSA, 0.6, seed + 8)
    linea(im, curva([(x - 6 * s, y - 145 * s), (x + 10 * s, y - 165 * s), (x + 2 * s, y - 180 * s)], 5), 4 * s, rgb("5a3a2a"),
          seed=seed + 9, t=t)
    cara_p(im, x, y - 75 * s, 2.0 * s, t, seed + 10, cara="normal")
    forma(im, elipse(x, y - 35 * s, 16 * s, 12 * s), AMARILLO, t, seed + 11, tinta=2.5 * s)


def innata(t):
    im = cache("e_inn", lambda: papel("rosa")).copy()
    if t > tLlama - 0.3:
        letrero(im, "INMUNIDAD INNATA", 700, 140, 70, t, col=ROJO, txt=CREMA, seed=25400, esc=entra(t, tLlama - 0.3), rot=-0.03)
    rotulo(im, "= 1.ª BARRERA", 700, 260, 46, MORADO, t, seed=25405, esc=entra(t, T_INN + 0.3))
    e = entra(t, T_INN)
    bebe(im, 520, 620, 1.3 * e + 0.01, t, 25410)
    if t > tNaces - 0.6:
        escudo(im, 760, 690, 0.7 * entra(t, tNaces - 0.6), t, 25420)
        palomita(im, 760, 540, 0.6 * entra(t, tNaces), t, seed=25425, col=VERDE)
    if t > tInnata2 - 0.3:
        e2 = entra(t, tInnata2 - 0.3)
        tarjeta(im, 1120, 520, 560 * e2, 240 * e2, t, CREMA, 25430, rot=0.03)
        rotulo(im, "INNATA =", 1120, 470, 54 * e2 + 1, ROJO, t, seed=25431, tinta=False, rot=0.03)
        if t > tNaces - 0.3:
            rotulo(im, "NACES CON ELLA", 1120, 560, 54 * entra(t, tNaces - 0.3) + 1, VERDE, t, seed=25432, tinta=False, rot=0.03)
    chispas(im, 520, 600, 220, t, tNaces + 0.3, seed=25440, col=AMARILLO)
    return im


TRAMOS = [(T_INI, intro), (T_INV, invasores), (T_CAS, castillo_t), (T_INN, innata)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
