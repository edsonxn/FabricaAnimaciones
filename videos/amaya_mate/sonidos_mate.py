# -*- coding: utf-8 -*-
"""SFX sintetizados del video 3 de Amaya (Matemáticas), anclados a las mismas palabras que la animación (importa las anclas de
cada plano_*.py). Reutiliza los bloques de sonidos_amaya.py / sonidos_base.py y añade lo propio de este guion: pasitos del
monito que camina en el plano y «boing» al subir, el lápiz del compás que traza el arco, el cuchillo que parte la pizza, los que
mastican la pizza, el ronquido del eje «acostado» y el aleteo de la mariposa."""
import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bip, boing, bp, destello, env, hp, lp, norm, osc, pop, retumbo, ruido, signo, whoosh)
from sonidos_base import bajon, ficha, masticar, moneda_clink, papel_, tachon, tic_tac, tramo
from sonidos_amaya import acierto, corazon_s, fanfarria, risita


def paso(seed=0):
    d = 0.09
    return norm(lp(ruido(d, seed), 1200, 2) * env(d, 0.001, 0.03) + osc(180, d) * env(d, 0.001, 0.025) * 0.4, 0.55)


def lapiz(dur=0.8, seed=0):
    """Grafito que raspa el papel mientras traza un arco."""
    t = _t(dur)
    x = bp(ruido(dur, seed), 2500, 7000) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    return norm(x * env(dur, 0.05, dur * 0.6), 0.35)


def corte(seed=0):
    """Cuchillo que parte la pizza: raspón corto con crujido."""
    d = 0.22
    x = bp(ruido(d, seed), 1500, 6000) * env(d, 0.004, 0.08) + osc(barrido(900, 500, d), d) * env(d, 0.002, 0.05) * 0.2
    return norm(x, 0.5)


def ronquido(seed=0, dur=1.4):
    t = _t(dur)
    amp = np.sin(np.pi * t / dur) ** 1.5
    x = lp(ruido(dur, seed), 500, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 34 * t)) * amp
    x += osc(barrido(70, 95, dur), dur) * amp * 0.25
    return norm(x, 0.5)


def aleteo(dur=1.0, seed=0):
    """Alas de mariposa: soplos suaves a ~9 por segundo."""
    t = _t(dur)
    x = lp(ruido(dur, seed), 1400, 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) ** 2
    return norm(x * env(dur, 0.1, dur * 0.6), 0.35)


def pistas():
    import plano_a as A, plano_b as B, plano_c as C, plano_d as D, plano_e as E, plano_f as F, plano_g as G, plano_h as Hh
    from comun import TOTAL, T0
    ev = []

    def a(t, x, v=0.6, pan=0.0):
        ev.append((t, x, v, pan))

    def cuenta3(t0, t1, seed):
        for k in range(3):
            a(t0 + k * (t1 - t0) / 3, ficha(seed + k, 990 - 110 * k), 0.55)
        a(t0, tic_tac(t1 - t0, seed + 5), 0.35)

    def camina(t0, t1, ts0, ts1, seed, pan=-0.4):
        n = max(2, int((t1 - t0) / 0.18))
        for k in range(n):
            a(t0 + k * (t1 - t0) / n, paso(seed + k), 0.4, pan)
        a(ts0, boing(seed + 20, 300, 700, max(0.25, ts1 - ts0)), 0.4, pan)

    for k, esc in enumerate(("decimales", "preg1", "resp1", "numeros", "preg2", "resp2", "triangulos", "preg3", "resp3", "plano",
                             "preg4", "resp4", "fracciones", "preg5", "resp5", "repaso", "cierre")):
        a(T0(esc) - 0.1, whoosh(0.8, 300 + k, 250, 1800), 0.32)
    # gancho
    a(A.tHola - 0.1, ficha(1, 880), 0.5)
    for k in range(4):
        a(A.tFotos - 0.1 + 0.22 * k, whoosh(0.4, 2 + k, 600, 2600), 0.3, -0.5 + 0.3 * k)
        a(A.tFotos + 0.35 + 0.22 * k, pop(6 + k, 900, 500, 0.08), 0.42, -0.5 + 0.3 * k)
    for k, tk in enumerate(A.tTema):
        a(tk - 0.15, pop(11 + k, 600 + 70 * k, 400), 0.45, -0.4 + 0.16 * k)
    a(A.tPizza - 0.1, boing(18, 500, 250, 0.3), 0.45)
    a(A.tPausa - 0.4, ficha(20, 660), 0.5)
    a(A.tArr - 0.2, fanfarria(21, 587.33), 0.4)
    # decimales
    a(B.tPunto - 0.1, destello(30), 0.45)
    for k, tk in enumerate(B.tLug):
        a(tk - 0.15, pop(31 + k, 650 + 90 * k, 420), 0.42, -0.3 + 0.3 * k)
    for k, tk in enumerate(B.tFila):
        a(tk - 0.2, ficha(34 + k, 700 + 100 * k), 0.4, -0.3)
    for k, tk in enumerate(B.tOcho):
        a(tk - 0.3, pop(37 + k, 700 + 250 * k, 500 + 200 * k, 0.1), 0.42, 0.3)
    for k, tk in enumerate(B.tL):
        a(tk - 0.1, pop(40 + k, 800, 500, 0.08), 0.35, -0.3 + 0.2 * k)
    a(B.tCentav - 0.2, moneda_clink(44), 0.5, -0.4)
    a(B.tCien - 0.1, moneda_clink(45), 0.35)
    a(B.tCinc - 0.2, pop(46), 0.42, 0.4)
    # pregunta 1
    a(B.tP1 - 0.2, ficha(50, 520), 0.55)
    a(B.tNum1 - 0.2, signo(51), 0.45)
    cuenta3(B.tFinP1 + 0.15, B.T_R1 + 0.1, 52)
    a(B.tR[0] - 0.1, acierto(57), 0.6)
    a(B.tAunq, boing(58, 400, 800, 0.3), 0.42)
    a(B.tEso - 0.2, acierto(59), 0.4)
    # números grandes
    a(C.tMiedo - 0.2, bajon(60), 0.4)
    a(C.tTruco - 0.2, destello(61), 0.4)
    for k in range(2):
        a(C.tEmp + 0.6 * k, pop(62 + k, 1000, 600, 0.07), 0.45, 0.3 - 0.3 * k)
    a(C.tDer - 0.3, whoosh(0.8, 64, 2400, 500), 0.35, 0.3)
    a(C.tMiles - 0.3, ficha(65, 760), 0.42)
    a(C.tMillones - 0.3, ficha(66, 880), 0.42)
    a(C.tCada - 0.3, papel_(67), 0.35)
    for k, tk in enumerate(C.tG2):
        a(tk - 0.15, pop(68 + k, 700 + 100 * k, 450), 0.4, -0.4 + 0.4 * k)
    a(C.tCero - 0.2, signo(72), 0.4)
    a(C.tEscrito - 0.4, papel_(73), 0.45)
    # trampa 7,735,923
    a(D.tP2 - 0.2, ficha(80, 520), 0.55)
    a(D.tOjo - 0.2, boing(81, 900, 400, 0.35), 0.5)
    for k, tk in enumerate(D.tGr):
        a(tk - 0.2, ficha(82 + k, 700 + 90 * k), 0.42, -0.3 + 0.3 * k)
    cuenta3(D.tFinP2 + 0.15, D.T_R2 + 0.1, 85)
    a(D.tL[0] - 0.1, acierto(90), 0.6)
    for k, tk in enumerate((D.tMll, D.tMil, D.tSol)):
        a(tk - 0.2, pop(91 + k, 800, 500, 0.08), 0.4, -0.4 + 0.4 * k)
    a(D.tCuad - 0.3, papel_(94), 0.4)
    a(D.tDos - 0.2, tachon(95), 0.6, 0.3)
    a(D.tDice - 0.3, papel_(96), 0.45, 0.3)
    a(D.tCinco - 0.2, destello(97), 0.4)
    a(D.tCorr - 0.3, boing(98, 400, 900, 0.3), 0.4)
    for k in range(3):
        a(D.tGrup + 0.8 * k, pop(99 + k, 600 + 120 * k, 400, 0.1), 0.38, 0.1 + 0.15 * k)
    a(D.tEscr - 0.2, acierto(103), 0.45)
    # triángulos
    for k in range(3):
        a(E.tSig + 0.25 * k + 0.2, pop(110 + k, 700 + 80 * k, 450), 0.42, -0.4 + 0.4 * k)
    a(E.tNo - 0.2, signo(113), 0.4)
    a(E.tIg1 - 0.2, ficha(114, 880), 0.45, -0.4)
    for k in range(3):
        a(E.tEquipo - 0.2 + 0.18 * k, pop(115 + k, 900, 600, 0.08), 0.42, 0.1 + 0.15 * k)
    a(E.tUnif - 0.3, acierto(118), 0.35, 0.3)
    a(E.tDos - 0.2, ficha(119, 780), 0.45, -0.4)
    for k in range(2):
        a(E.tTen - 0.2 + 0.2 * k, pop(120 + k, 700, 500), 0.42, 0.1 + 0.2 * k)
    a(E.tChan - 0.3, boing(122, 250, 160, 0.35), 0.5, 0.45)
    a(E.tTres3 - 0.2, ficha(123, 680), 0.45, -0.4)
    for k in range(4):
        a(E.tEscal - 0.2 + 0.12 * k, pop(124 + k, 500 + 160 * k, 400 + 120 * k, 0.08), 0.42, 0.2 + 0.08 * k)
    a(E.tComp - 0.3, ficha(130, 1500), 0.35, 0.3)
    a(E.tAbre - 0.3, lapiz(0.8, 131), 0.5, 0.2)
    a(E.tArco - 0.2, lapiz(0.8, 132), 0.6, 0.0)
    a(E.tCada + 0.1, lapiz(0.8, 133), 0.6, 0.4)
    a(E.tCruz - 0.2, destello(134), 0.5, 0.2)
    a(E.tAsi - 0.2, lapiz(0.8, 135), 0.45, 0.2)
    a(E.tIg4 - 0.3, acierto(136), 0.4)
    a(E.tP3 - 0.2, ficha(140, 520), 0.55)
    for k, tk in enumerate((E.tC1, E.tC2, E.tT3)):
        a(tk - 0.2, pop(141 + k, 800, 500, 0.08), 0.38, -0.3)
    cuenta3(E.tFinP3 + 0.15, E.T_R3 + 0.1, 144)
    a(E.tIsoR - 0.1, acierto(150), 0.6)
    a(E.tTenR - 0.3, pop(151, 700, 500), 0.4, 0.3)
    # plano cartesiano
    a(F.tCuad - 0.3, papel_(160), 0.4, 0.3)
    a(F.tHoja - 0.2, whoosh(1.2, 161, 400, 2000), 0.3, -0.3)
    for k in range(4):
        a(F.tPuntos - 0.3 + 0.12 * k, pop(162 + k, 900 + 60 * k, 600, 0.07), 0.38, -0.4 + 0.2 * k)
    a(F.tEjes - 0.3, whoosh(0.7, 166, 500, 2600), 0.4, -0.3)
    a(F.tAcost - 0.1, tramo(ronquido(167), 0.3), 0.4, 0.3)
    a(F.tParado - 0.3, boing(168, 300, 800, 0.3), 0.45, 0.3)
    a(F.tParen - 0.4, pop(169, 600, 400), 0.4, 0.3)
    for k in range(5):
        a(F.tAbc - 0.3 + 0.06 * k, ficha(170 + k, 600 + 80 * k), 0.3, 0.3)
    a(F.tTruco - 0.2, destello(176), 0.4)
    camina(F.tCam1 - 0.1, F.tCam1 + 0.5, F.tSub4 - 0.1, F.tSub4 + 0.5, 177)
    a(F.tAhi - 0.2, acierto(200), 0.4, -0.4)
    camina(F.tCam9 - 0.1, F.tCam9 + 0.7, F.tSub4b - 0.1, F.tSub4b + 0.5, 201, pan=0.0)
    a(F.tVolt + 0.4, boing(225, 700, 300, 0.4), 0.35, -0.2)
    a(F.tCaes, bajon(226), 0.45, -0.2)
    a(F.tOrden - 0.3, destello(227), 0.4)
    a(F.tP4 - 0.2, ficha(230, 520), 0.55)
    a(F.tCoord - 0.3, signo(231), 0.45, -0.3)
    cuenta3(F.tFinP4 + 0.15, F.T_R4 + 0.1, 232)
    a(F.tTres - 0.1, acierto(238), 0.6)
    camina(F.tCam3 - 0.1, F.tCam3 + 0.5, F.tSub2 - 0.1, F.tSub2 + 0.5, 239)
    a(F.tBien - 0.2, fanfarria(260, 659.25), 0.4)
    # fracciones
    a(G.tCuad - 0.3, papel_(270), 0.4, 0.3)
    a(G.tPizza - 0.3, pop(271, 500, 300, 0.15), 0.5, -0.4)
    a(G.tEntero - 0.2, destello(272), 0.35, -0.4)
    a(G.tAna - 0.2, pop(273, 900, 600), 0.42, 0.1)
    a(G.tLuis - 0.2, pop(274, 700, 450), 0.42, 0.35)
    a(G.tCuartos - 0.3, pop(275, 800, 500), 0.4, -0.4)
    a(G.tTercios - 0.3, pop(276, 650, 420), 0.4, 0.1)
    a(G.tNoSe - 0.2, bajon(277), 0.45, 0.4)
    a(G.tDoce - 0.2, destello(278), 0.4, 0.2)
    for k in range(6):
        a(G.tAhora - 0.2 + k * (G.tDoceReb + 0.6 - G.tAhora) / 6, corte(279 + k), 0.45, -0.4)
    for k in range(3):
        a(G.tTres3 - 0.3 + 0.2 * k, pop(290 + k, 900, 650, 0.07), 0.35, -0.3)
    for k in range(4):
        a(G.tCuatro3 - 0.3 + 0.2 * k, pop(293 + k, 700, 500, 0.07), 0.35, -0.3)
    a(G.tSiete - 0.3, acierto(298), 0.45, 0.3)
    a(G.tMenos - 0.3, ficha(299, 760), 0.4, 0.3)
    a(G.tQuedaron - 0.4, masticar(6, 300), 0.5, -0.3)
    a(G.tCinco - 0.2, acierto(301), 0.4, 0.3)
    for k in range(6):
        a(G.tTarde - 0.6 + 0.12 * k, paso(302 + k), 0.4, 0.6 - 0.1 * k)
    a(G.tTarde + 0.3, bajon(309), 0.4, 0.2)
    a(G.tMari - 0.3, aleteo(1.2, 310), 0.5, -0.2)
    a(G.tUnoC - 0.2, whoosh(0.6, 311, 600, 2400), 0.38, -0.3)
    a(G.tUnoC2 - 0.2, whoosh(0.6, 312, 600, 2400), 0.38, 0.3)
    a(G.tCincoMas - 0.2, pop(313, 800, 500), 0.4)
    a(G.tAbajo - 0.2, pop(314, 600, 400), 0.4)
    a(G.tRes - 0.2, acierto(315), 0.5)
    # pregunta 5 / respuesta 5
    a(Hh.tP5 - 0.2, ficha(320, 520), 0.55)
    a(Hh.tMedio - 0.3, pop(321, 800, 500), 0.4, -0.4)
    a(Hh.tTercio - 0.3, pop(322, 700, 450), 0.4, 0.1)
    a(Hh.tCuanto - 0.2, signo(323), 0.45, 0.3)
    cuenta3(Hh.tFinP5 + 0.15, Hh.T_R5 + 0.1, 324)
    a(Hh.tCinco - 0.1, acierto(330), 0.6, 0.3)
    a(Hh.tMari - 0.3, aleteo(1.1, 331), 0.45, -0.2)
    a(Hh.tC1 - 0.2, whoosh(0.6, 332, 600, 2400), 0.35, -0.3)
    a(Hh.tC2 - 0.2, whoosh(0.6, 333, 600, 2400), 0.35, 0.3)
    a(Hh.tSuma - 0.2, pop(334, 800, 500), 0.4)
    a(Hh.tAbajo - 0.2, pop(335, 600, 400), 0.4)
    a(Hh.tBien - 0.2, fanfarria(336, 587.33), 0.45)
    # repaso y cierre
    for k, tk in enumerate((Hh.tDec, Hh.tNum, Hh.tTri, Hh.tPlano, Hh.tFra)):
        a(tk - 0.25, papel_(340 + k), 0.4, -0.4 + 0.2 * k)
    for k, tk in enumerate((Hh.tEqui, Hh.tIso, Hh.tEsc)):
        a(tk - 0.2, pop(345 + k, 700 + 100 * k, 450, 0.08), 0.35, -0.4)
    a(Hh.tNivel - 0.3, fanfarria(350, 523.25), 0.45)
    for k in range(5):
        a(Hh.tCuad - 0.2 + 0.12 * k, pop(351 + k, 900 + 60 * k, 650, 0.07), 0.35, -0.5 + 0.2 * k)
    a(Hh.tDormir - 0.6, destello(357), 0.3, -0.3)
    a(Hh.tPueden - 0.2, fanfarria(358, 659.25), 0.4)
    for k in range(5):
        a(Hh.tPueden + 0.4 + 0.3 * k, corazon_s(360 + k), 0.3, -0.5 + 0.25 * k)
    a(Hh.tExito - 0.2, destello(366), 0.5)
    return [e for e in ev if 0 <= e[0] < TOTAL]
