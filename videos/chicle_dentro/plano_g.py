# -*- coding: utf-8 -*-
"""CIERRE: ¿de dónde salió? («7 AÑOS» con signos, NADIE LO SABE) → los papás que regañan («¡SE TE QUEDA 7 AÑOS!») y una
fila de niños de varias épocas frente a la bolita gris gigante → de vuelta al parque: la niña tranquila, el estómago con
escoba → la mesa con chicles pegados (X) y el basurero (✓) → Kuri y el botón SUSCRÍBETE + la olla del próximo viaje."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, desborde, ww
from fondos_chicle import papel, patio
from iconos_ia import marca_x, palomita, personita
from personajes import AMARILLO, BLANCO, corazon, destello, kuri, pregunta
from utileria import vapor
from personajes_ia import globo, nina
from piezas_chicle import GRIS, ROJO, basurero, calendario, chicle, escoba

T_INI = T0("cierre")
C = "cierre"
tSalio, tNadie = ww(C, 0, "salio"), ww(C, 0, "nadie")
tPapas, tNinos, tFunciono, tGeneraciones, tGris = (ww(C, 1, "papas"), ww(C, 1, "ninos"), ww(C, 1, "funciono"),
                                                    ww(C, 1, "generaciones"), ww(C, 1, "gris"))
tSabes, tTranquilo, tEscoba, tCuerpo = ww(C, 2, "sabes"), ww(C, 2, "tranquilo"), ww(C, 2, "escoba"), ww(C, 2, "cuerpo")
tBasura, tMesa = ww(C, 3, "basura"), ww(C, 3, "mesa")
tViajando, tSuscribete, tProximo, tCocinando = (ww(C, 4, "viajando"), ww(C, 4, "suscribete"), ww(C, 4, "proximo"),
                                                ww(C, 4, "cocinando"))
T_PARQUE = tSabes - 0.5


def mito(t):
    im = papel("sepia")
    if t < tPapas:
        calendario(im, 960, 480, 1.6 * e_back(pr(t, T_INI, T_INI + 0.4)), t, "AÑOS", "7")
        for k in range(3):
            pregunta(im, 600 + k * 360, 220 + 40 * (k % 2), e_back(pr(t, tSalio + 0.15 * k, tSalio + 0.25 + 0.15 * k)), t, seed=1011 + k)
        en = e_back(pr(t, T_INI + 0.2, T_INI + 0.6))
        nina(im, 320, 620 + 4 * math.sin(t * 2), 1.35 * en + 0.01, t, cara="normal", boca="duda", mira=0.7)
        kuri(im, 1620, 600 + 14 * math.sin(t * 1.5), 1.7 * en + 0.01, t, cara="normal" if t < tNadie else "susto",
             brazos=(1.6, 1.6) if t > tNadie else (0.5, 0.5))
        if t > tNadie - 0.2:
            rotulo(im, "NADIE LO SABE", 960, 860, 110, rgb("8a5a34"), t, seed=10500, esc=e_back(pr(t, tNadie - 0.2, tNadie + 0.1)))
        return im
    # los papás que regañan
    if t < tFunciono:
        e = e_back(pr(t, tPapas - 0.2, tPapas + 0.2))
        personita(im, 520, 470, 5.0 * e + 0.01, t, seed=2, col=rgb("6aa84f"))
        cara_p(im, 520, 470, 5.0 * e + 0.01, t, 2, "enojo")
        personita(im, 780, 450, 5.4 * e + 0.01, t, seed=4, col=rgb("9b6ad1"))
        cara_p(im, 780, 450, 5.4 * e + 0.01, t, 4, "enojo")
        globo(im, 650, 170, 700, 150, "", t, px=46, n=60 * pr(t, tPapas, tPapas + 0.8), lineas=["¡SE TE QUEDA", "SIETE AÑOS!"],
              cola=(-1, 1), alfa=e)
        if t > tNinos - 0.3:
            sn = 3.4 * e_back(pr(t, tNinos - 0.3, tNinos)) + 0.01
            personita(im, 1350, 640, sn, t, seed=5, col=rgb("e35d4a"))
            cara_p(im, 1350, 640, sn, t, 5, "susto")
            chicle(im, 1500, 560, 40, t, seed=10510, dientes=False)
            marca_x(im, 1500, 560, 0.5 * e_back(pr(t, tNinos + 0.3, tNinos + 0.5)), t, seed=10511)
        return im
    # generaciones frente a la bolita gris gigante
    e = e_back(pr(t, tFunciono - 0.2, tFunciono + 0.2))
    chicle(im, 960, 330, 220 * e + 1, t, seed=10520, col=GRIS * 0.9, cara="normal")
    lavado(im, elipse(960, 600, 300, 50), rgb("6a5a4a"), 0.3, 10521)
    n = int(7 * e_out(pr(t, tGeneraciones - 0.3, tGeneraciones + 1.0)))
    for k in range(n):
        x = 240 + k * 240
        personita(im, x, 760, 3.2, t, seed=10 + k)
        cara_p(im, x, 760, 3.2, t, 10 + k, "susto")
        rotulo(im, ["1950", "1960", "1970", "1980", "1990", "2000", "2010"][k], x, 990, 40, rgb("8a5a34"), t, seed=10530 + k,
               tinta=False)
        brillo(im, x + 60, 640, 14, BLANCO, 0)
    if t > tGris - 0.2:
        rotulo(im, "¡FUNCIONÓ!", 960, 100, 90, ROJO, t, seed=10540, esc=e_back(pr(t, tGris - 0.2, tGris + 0.1)))
    return im


def cara_p(im, x, y, s, t, seed, cara="normal"):
    """Ojos y boca para la personita de iconos_ia (cabeza de radio 24·s en (x, y))."""
    if s < 0.3:
        return
    dy = 3 * s * math.sin(t * 5 + seed)
    for d in (-1, 1):
        forma(im, elipse(x + d * 8 * s, y + 3 * s + dy, 2.0 * s, 2.8 * s), TINTA, t, 10800 + seed * 3 + d, tinta=0)
        if cara == "enojo":
            linea(im, [(x + d * 4 * s, y - 2 * s + dy), (x + d * 13 * s, y - 5 * s + dy)], 0.9 * s, seed=10820 + seed * 3 + d,
                  t=t, punta=False)
    if cara == "enojo":
        forma(im, elipse(x, y + 13 * s + dy, 5 * s, 3.5 * s), rgb("8a3a3a"), t, 10840 + seed, tinta=0.6 * s)
    elif cara == "susto":
        forma(im, elipse(x, y + 13 * s + dy, 3 * s, 4 * s), rgb("8a3a3a"), t, 10840 + seed, tinta=0.6 * s)
    else:
        linea(im, curva([(x - 5 * s, y + 11 * s + dy), (x, y + 14 * s + dy), (x + 5 * s, y + 11 * s + dy)], 4), 0.8 * s,
              seed=10840 + seed, t=t, punta=False)


def parque(t):
    im = patio()
    if t < tBasura - 0.4:                                                 # Kuri acompaña desde el principio
        kuri(im, 1720, 330 + 15 * math.sin(t * 1.6), 1.5, t, cara="feliz", brazos=(0.5, 1.6 + 0.4 * math.sin(t * 6)))
    nina(im, 560, 600, 1.6, t, cara="feliz" if t < tBasura else "normal", boca="sonrisa",
         brazos=(0.3, 0.3) if t < tBasura - 0.3 or t > tMesa + 0.5 else (0.3, 1.9), codos=(0.4, 0.4))
    if tTranquilo - 0.3 < t < tBasura - 0.4:
        rotulo(im, "TRANQUILO", 560, 160, 90, AMARILLO, t, seed=10600, esc=e_back(pr(t, tTranquilo - 0.3, tTranquilo)))
    if tEscoba - 0.5 < t < tBasura - 0.4:                                 # estómago con escoba
        e = e_back(pr(t, tEscoba - 0.5, tEscoba - 0.2))
        cx, cy = 1250, 520
        forma(im, curva([(cx - 120 * e, cy - 140 * e), (cx + 60 * e, cy - 150 * e), (cx + 160 * e, cy - 20 * e), (cx + 120 * e, cy + 120 * e),
                         (cx - 40 * e, cy + 140 * e), (cx - 150 * e, cy + 20 * e)], 7, True), rgb("e48c8c"), t, 10610, tinta=5,
              luz=(BLANCO, -20, -20, 0.25))
        forma(im, elipse(cx - 40 * e, cy - 30 * e, 10 * e + 1, 13 * e + 1), TINTA, t, 10611, tinta=0)
        forma(im, elipse(cx + 40 * e, cy - 30 * e, 10 * e + 1, 13 * e + 1), TINTA, t, 10612, tinta=0)
        linea(im, curva([(cx - 30 * e, cy + 20 * e), (cx, cy + 40 * e), (cx + 30 * e, cy + 20 * e)], 4), 5, seed=10613, t=t)
        escoba(im, cx + 230 * e, cy, 1.1 * e, t, rot=0.4 + 0.25 * math.sin(t * 7))
        if t > tCuerpo - 0.2:
            destello(im, cx + 150, cy - 200, 1.2 * e_back(pr(t, tCuerpo - 0.2, tCuerpo + 0.1)), t)
    if t > tBasura - 0.5 and t < tViajando - 0.3:                          # basurero ✓ y mesa con chicles ✗
        e = e_back(pr(t, tBasura - 0.5, tBasura - 0.2))
        basurero(im, 1000, 760, 1.2 * e + 0.01, t)
        v = pr(t, tBasura - 0.2, tBasura + 0.5)
        if v < 1:
            chicle(im, lerp(700, 1000, v), lerp(330, 620, v) - 200 * math.sin(v * math.pi), 24, t, seed=10620)
        palomita(im, 1000, 520, 0.9 * e_back(pr(t, tBasura + 0.4, tBasura + 0.6)), t, seed=10621)
        if t > tMesa - 0.4:
            e2 = e_back(pr(t, tMesa - 0.4, tMesa))
            forma(im, rrect(1520, 560, 520 * e2 + 2, 40 * e2 + 2, 8), rgb("a86e3c"), t, 10630, tinta=4)
            for d in (-1, 1):
                forma(im, rrect(1520 + d * 220 * e2, 780, 30 * e2 + 1, 400 * e2 + 1, 6), rgb("8a5a34"), t, 10631 + d, tinta=3.6)
            for k in range(5):
                chicle(im, 1360 + k * 80, 600 + 6 * (k % 2), 22 * e2 + 1, t, seed=10640 + k,
                       col=[rgb("f39bc0"), GRIS, rgb("8fd18a")][k % 3], dientes=False)
            marca_x(im, 1520, 760, 1.2 * e_back(pr(t, tMesa + 0.1, tMesa + 0.3)), t, seed=10650)
    if t > tViajando - 0.3:                                               # Kuri y suscríbete
        e = e_back(pr(t, tViajando - 0.3, tViajando))
        kuri(im, 1250, 450 + 15 * math.sin(t * 1.6), 2.4 * e + 0.01, t, cara="feliz", brazos=(0.5, 1.7 if t > tSuscribete else 0.5))
        if t > tSuscribete - 0.3:
            e2 = e_back(pr(t, tSuscribete - 0.3, tSuscribete))
            aprieta = 0.9 if (t - tSuscribete) % 1.6 < 0.2 else 1.0
            forma(im, rrect(1250, 820, 520 * e2 * aprieta + 2, 120 * e2 * aprieta + 2, 30), rgb("e35d4a"), t, 10700, tinta=4.4,
                  luz=(BLANCO, 0, -14, 0.3))
            rotulo(im, "SUSCRÍBETE", 1250, 820, 70, BLANCO, t, seed=10701, esc=e2 * aprieta, tinta=False)
        if t > tProximo - 0.3:                                            # la olla del próximo viaje
            e3 = e_back(pr(t, tProximo - 0.3, tProximo))
            ox, oy = 1700, 330
            forma(im, curva([(ox - 120 * e3, oy - 60 * e3), (ox + 120 * e3, oy - 60 * e3), (ox + 100 * e3, oy + 80 * e3), (ox - 100 * e3, oy + 80 * e3)],
                            4, True), rgb("4b4b55"), t, 10710, tinta=4)
            forma(im, elipse(ox, oy - 64 * e3, 130 * e3 + 1, 22 * e3 + 1), rgb("6a6a74"), t, 10711, tinta=3)
            vapor(im, ox, oy - 110, e3, t, seed=10712)
            rotulo(im, "PRÓXIMO VIAJE", ox, oy + 160, 52, AMARILLO, t, seed=10713, esc=e3)
            pregunta(im, ox + 140, oy - 170, e3, t, seed=1019)
    return im


def cuadro_crudo(t):
    if t < T_PARQUE:
        return mito(t)
    if t < T_PARQUE + 0.8:
        return desborde(mito(t), parque(t), pr(t, T_PARQUE, T_PARQUE + 0.8), W / 2, H / 2)
    return parque(t)


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
