# -*- coding: utf-8 -*-
"""28-48,3 s · TRAMPA: en corte, cuanto más patalea más se juntan los granos → «¡COMO CEMENTO!» → en la playa Kuri tira de
una cuerda atada al pie = levantar un coche (burbuja) · MAREA: la arena no es lo peligroso: pasan las horas (reloj, sol que
baja, tarde) y la marea sube hasta el pecho."""
import math

import numpy as np

from acuarela import (H, W, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import FIN, INI, T1, desborde, ww
from fondos_arena import Y_MAR, playa
from personajes import AMARILLO, BLANCO, exclama, gota, kuri, nube_lluvia
from personajes_arena import ARENA_HUM, AGUA, arena_frente, coche, cuerda, explorador, gaviota, ola, palmera, reloj, sol
import plano_a as A

TR, MA = "trampa", "marea"
T_INI = T1("mito")
tProblema, tSuelta, tPataleas = ww(TR, 0, "problema"), ww(TR, 0, "suelta"), ww(TR, 0, "pataleas")
tAprieta, tCemento = ww(TR, 0, "aprieta"), ww(TR, 0, "cemento")
tSacar, tTiron, tLevantar, tCoche = ww(TR, 1, "sacar"), ww(TR, 1, "tiron"), ww(TR, 1, "levantar"), ww(TR, 1, "coche")
tPelig, tArena, tQuedarte, tHoras = ww(MA, 0, "peligroso"), ww(MA, 0, "arena"), ww(MA, 0, "quedarte"), ww(MA, 0, "horas")
tSube, tMarea = ww(MA, 0, "sube"), ww(MA, 0, "marea")
T_PLAYA = INI(TR, 1) - 0.4
GRIS = rgb("9a9a94")
EX, BY = 540, A.Y_SUP - 54            # hundido hasta la cintura en la vista de playa


# ------------------------------------------------------------ la trampa en corte
def trampa_corte(t):
    pat = pr(t, tPataleas - 0.1, tPataleas + 0.3) * (1 - pr(t, tCemento, tCemento + 0.3))
    apr = suave(pr(t, tPataleas + 0.4, tCemento))
    cara = "apretados" if t < tPataleas else ("susto" if t < tCemento else "triste")
    boca = "apretada" if t < tPataleas else ("grito" if t < tCemento else "triste")
    bra = (2.6 + 0.15 * math.sin(t * 9), 2.6 + 0.15 * math.cos(t * 9)) if t < tPataleas else (1.5 + 0.5 * math.sin(t * 11), 1.5 + 0.5 * math.cos(t * 11))
    im, p, by = A.corte(t, aprieta=apr, patada=pat, extra=dict(cara=cara, boca=boca, brazos=bra))
    if t > tAprieta - 0.3:                              # flechas de los granos que se cierran
        e = pr(t, tAprieta - 0.3, tAprieta + 0.4) * (1 - pr(t, tCemento + 0.4, tCemento + 0.8))
        for d in (-1, 1):
            for k in range(2):
                y = by + 110 + k * 90
                x0 = 540 + d * 330
                linea(im, [(x0, y), (x0 - d * 130 * e, y)], 14, col=rgb("7c5f37"), seed=6000 + k + 3 * d, t=t)
                linea(im, [(x0 - d * 130 * e + d * 30, y - 24), (x0 - d * 130 * e, y), (x0 - d * 130 * e + d * 30, y + 24)], 10,
                      col=rgb("7c5f37"), seed=6010 + k + 3 * d, t=t)
    if t > tCemento - 0.15:                             # cemento alrededor de las piernas
        e = e_out(pr(t, tCemento - 0.15, tCemento + 0.35))
        bloque = rrect(540, by + 150, 330, 260, 30)
        forma(im, bloque, GRIS, t, 6100, tinta=5, alfa=0.85 * e, sombra=(rgb("6b6b66"), 16, 0, 0.5))
        for k in range(4):                              # grietas
            x = 420 + k * 80
            linea(im, [(x, by + 40), (x + 18, by + 110), (x - 6, by + 170)], 3, seed=6110 + k, t=t, alfa=0.7 * e)
        rotulo(im, "¡COMO CEMENTO!", 540, 330, 120, AMARILLO, t, seed=51, rot=-0.05, esc=e_back(pr(t, tCemento - 0.15, tCemento + 0.15)))
    kx, ky = A._kuri_flota(im, t, x=860, y=640, cara="susto" if t > tPataleas else "normal",
                           brazos=(1.4, 1.4) if t > tPataleas else (0.5, 0.5))
    if t > tSuelta - 0.1 and t < tPataleas:
        exclama(im, kx, ky - 170, 1.1 * e_back(pr(t, tSuelta - 0.1, tSuelta + 0.2)), t)
    return terminar(im, t)


# ------------------------------------------------------------ en la playa: el tirón, las horas y la marea
def playa_atrapado(t):
    tarde = suave(pr(t, tQuedarte, tSube + 0.6))
    im = playa(tarde)
    if t > tPelig - 1:                                  # el sol baja y se pone
        u = suave(pr(t, tQuedarte - 0.2, tSube + 0.4))
        sx, sy = lerp(820, 640, u), lerp(230, Y_MAR - 20, u)
        sol(im, sx, sy, 70, t, col=rgb("ffd65a") * (1 - u) + rgb("f2884a") * u, cara="sudor" if u > 0.3 else None)
        im[Y_MAR - 4:] = im[Y_MAR - 4:]
    for k in range(2):
        gaviota(im, (300 + 120 * t + k * 420) % (W + 200) - 100, 300 + 80 * k, 0.8, t, seed=2750 + k)
    palmera(im, 70, 1180, 1.25, t)
    lavado(im, elipse(EX, A.Y_SUP + 60, 420, 150), ARENA_HUM, 0.8, 77, humedo=16)
    tira = pr(t, tTiron - 0.15, tTiron + 0.1) * (1 - pr(t, tPelig - 0.6, tPelig - 0.2))
    tira_y = -26 * e_out(tira) + 8 * math.sin(t * 30) * tira
    cansado = t > tHoras
    susto = t > tSube
    cara = "apretados" if 0.2 < tira else ("susto" if susto else ("triste" if cansado else "normal"))
    boca = "grito" if 0.2 < tira and t < tLevantar else ("o" if susto else ("triste" if cansado else "plana"))
    bra = (1.3 + 0.2 * math.sin(t * 9), 1.3 + 0.2 * math.cos(t * 9)) if susto else (0.9, 0.9)
    um = suave(pr(t, tSube - 0.3, T1(MA) + 0.3))        # la marea: detrás cubre la playa entera...
    if um > 0:
        ola(im, lerp(860, H + 60, um), t, rgb("4a7fa8"), alfa=0.62, y0=Y_MAR, seed=2800)
    p = explorador(im, EX, BY + 4 * math.sin(t * 2), A.S_EX, t, cara=cara, boca=boca, brazos=bra, codos=(0.6, 0.6))
    arena_frente(im, A.Y_SUP, t, seed=3, x0=EX - 430, x1=EX + 430, onda=5, alto=A.Y_SUP + 210, cuerpo=EX)
    if um > 0.25:                                       # ...y delante le sube hasta el pecho
        top = lerp(A.Y_SUP + 40, BY - 60, suave(pr(um, 0.25, 1)))
        xs = np.linspace(-40, W + 40, 36)
        ys = top + 14 * np.sin(xs / 100 + t * 2.2) + 5 * np.sin(xs / 33 - t * 3)
        pol = np.concatenate([np.stack([xs, ys], 1), [(W + 40, H + 60), (-40, H + 60)]]).astype(np.float32)
        lavado(im, pol, rgb("4a7fa8"), 0.55, 2810, humedo=14)
        linea(im, np.stack([xs, ys], 1), 8, col=BLANCO, seed=2811, t=t, alfa=0.85, punta=False)
    # Kuri con la cuerda atada al pie (entra con «sacar», tira con «tirón», la suelta con «peligroso»)
    con_cuerda = tSacar - 0.4 < t < tPelig - 0.2
    kx, ky = 820 + 10 * math.sin(t * 1.3), 900 + 16 * math.sin(t * 1.9) + tira_y * 3
    if con_cuerda:
        cuerda(im, (kx - 30, ky + 30), (EX + 90, A.Y_SUP + 30), t, tension=0.4 + 0.6 * tira)
    kc = "apretados" if tira > 0.2 else ("susto" if susto else "normal")
    kuri(im, kx, ky, 1.1, t, cara=kc, brazos=(-0.6, -0.6) if con_cuerda else ((1.5, 1.5) if susto else (0.5, 0.5)))
    if tira > 0.2:
        for k in range(3):
            gota(im, kx + 70 + 12 * k, ky - 70 + 26 * k, 0.9, t, seed=1060 + k)
    if t > tLevantar - 0.2 and t < tPelig + 0.2:       # burbuja: levantar un coche
        e = e_back(pr(t, tLevantar - 0.2, tLevantar + 0.15)) * (1 - e_in(pr(t, tPelig - 0.3, tPelig + 0.2)))
        if e > 0.02:
            bx, by_, r = 330, 480, 250 * e
            for k, (dx, dy, rr) in enumerate(((150, 230, 22), (200, 290, 14))):
                forma(im, elipse(bx + dx * e, by_ + dy * e, rr * e, rr * e), BLANCO, t, 6200 + k, tinta=3)
            forma(im, elipse(bx, by_, r, r * 0.9), BLANCO, t, 6210, tinta=5, sombra=(rgb("d9d2bf"), 10, -8, 0.5))
            sube = 40 * math.sin(t * 3) * 0.3 - 60 * e_out(pr(t, tCoche, tCoche + 0.8))
            linea(im, [(bx, by_ - r * 0.85), (bx, by_ - 20 * e + sube)], 6 * e, col=rgb("b8925a"), seed=6220, t=t, punta=False)
            coche(im, bx, by_ + 70 * e + sube, 0.95 * e, t, rot=0.05 * math.sin(t * 4))
            rotulo(im, "= 1 COCHE", bx, by_ + r + 70, 100, AMARILLO, t, seed=52, esc=e)
    # las horas: reloj que gira
    if t > tQuedarte - 0.3 and t < tSube + 0.4:
        e = e_back(pr(t, tQuedarte - 0.3, tQuedarte)) * (1 - e_in(pr(t, tSube, tSube + 0.4)))
        reloj(im, 220, 420, 120 * e + 1, t, 8 * suave(pr(t, tQuedarte, tSube)))
        if e > 0.5:
            rotulo(im, "HORAS", 220, 600, 90, BLANCO, t, seed=53, esc=e)
    # la marea sube hasta el pecho
    if t > tSube - 0.3:
        if um > 0.3:
            exclama(im, kx, ky - 170, 1.2 * e_back(pr(t, tSube + 0.2, tSube + 0.5)), t)
        if t > tMarea - 0.1:
            rotulo(im, "¡LA MAREA!", 540, 330, 150, AMARILLO, t, seed=54, rot=-0.06, esc=e_back(pr(t, tMarea - 0.1, tMarea + 0.2)))
    if cansado and not susto:
        nube_lluvia(im, p["cabeza"][0] - 10, p["cabeza"][1] - 330, 0.8, t)
    return terminar(im, t)


def cuadro(t):
    if t < T_PLAYA:
        return trampa_corte(t)
    if t < T_PLAYA + 0.6:
        return desborde(trampa_corte(t), playa_atrapado(t), pr(t, T_PLAYA, T_PLAYA + 0.6), cx=540, cy=A.Y_SUP)
    return playa_atrapado(t)
