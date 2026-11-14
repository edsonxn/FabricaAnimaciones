# -*- coding: utf-8 -*-
"""SFX sintetizados del video 2 de Amaya (Español), anclados a las mismas palabras que la animación (importa las anclas de cada
plano_*.py). Reutiliza los bloques de sonidos_amaya.py / sonidos_base.py y añade lo que la voz nombra aquí: PALMADAS (es-cue-la),
el BIP de reversa del camión, RONQUIDOS («papá ronca») y el sartén/hot cake."""
import math

import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bip, boing, bp, destello, env, hp, lp, norm, osc, pop, retumbo, ruido, signo, whoosh)
from sonidos_base import bajon, ficha, papel_, tachon, tic_tac, tramo
from sonidos_amaya import acierto, corazon_s, fanfarria, risita


def palmada(seed=0):
    d = 0.18
    x = bp(ruido(d, seed), 700, 5000) * env(d, 0.0008, 0.035)
    x += bp(ruido(d, seed + 1), 1500, 3000) * env(d, 0.004, 0.05) * 0.5
    return norm(x, 0.8)


def bip_reversa(dur=3.0, seed=0):
    """Pitido de camión en reversa: tono de 1 kHz, 0,4 s encendido / 0,4 s apagado."""
    x = np.zeros(int(dur * SR))
    for k in range(int(dur / 0.8) + 1):
        d = 0.4
        b = (osc(1000, d) + 0.3 * osc(3000, d)) * env(d, 0.01, 0.35)
        i = int(k * 0.8 * SR)
        n = min(len(b), len(x) - i)
        if n > 0:
            x[i:i + n] += b[:n]
    return norm(lp(x, 6000), 0.45)


def ronquido(seed=0, dur=1.6):
    """Ronquido: ruido grave modulado por un zumbido de ~35 Hz que sube y baja (inhalación)."""
    t = _t(dur)
    amp = np.sin(np.pi * t / dur) ** 1.5
    x = lp(ruido(dur, seed), 500, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 34 * t)) * amp
    x += osc(barrido(70, 95, dur), dur) * amp * 0.25
    return norm(x, 0.6)


def ladrido(seed=0):
    """«¡Guau!»: ráfaga con formantes y tono que cae (perro mediano)."""
    d = 0.32
    f = barrido(520, 300, d)
    x = sum(osc(f * m, d) / m for m in (1, 2, 3, 4)) * env(d, 0.008, 0.12)
    x = bp(x + bp(ruido(d, seed), 400, 2500) * env(d, 0.004, 0.06) * 0.6, 250, 3200)
    return norm(x, 0.7)


def chisporroteo(dur=1.5, seed=0):
    x = hp(ruido(dur, seed), 2500) * 0.25
    rg = _rng(seed + 3)
    for k in range(int(dur * 25)):
        c = bp(ruido(0.008, seed + 10 + k), 2500, 8000) * env(0.008, 0.0005, 0.004)
        i = int(rg.uniform(0, dur - 0.02) * SR)
        x[i:i + len(c)] += c * rg.uniform(0.3, 1.0)
    return norm(x * env(dur, 0.1, dur * 0.4), 0.35)


def plaf(seed=0):
    d = 0.3
    return norm(lp(ruido(d, seed), 900, 2) * env(d, 0.002, 0.08) + osc(140, d) * env(d, 0.002, 0.06) * 0.6, 0.7)


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

    for k, esc in enumerate(("silabas", "clasif", "preg1", "reglas", "preg2", "adverbios", "preg3", "autobio", "anecdota", "carta",
                             "preg4", "repaso", "cierre")):
        a(T0(esc) - 0.1, whoosh(0.8, 300 + k, 250, 1800), 0.35)
    # gancho
    a(A.tHola - 0.1, ficha(1, 880), 0.5)
    for k in range(4):
        a(A.tFotos - 0.1 + 0.22 * k, whoosh(0.4, 2 + k, 600, 2600), 0.35, -0.5 + 0.3 * k)
        a(A.tFotos + 0.35 + 0.22 * k, pop(6 + k, 900, 500, 0.08), 0.45, -0.5 + 0.3 * k)
    a(A.tEsp - 0.2, fanfarria(10, 523.25), 0.35)
    for k, tk in enumerate(A.tTema):
        a(tk - 0.15, pop(11 + k, 600 + 70 * k, 400), 0.45, -0.4 + 0.16 * k)
    a(A.tCort, boing(18, 500, 250, 0.3), 0.45)
    a(A.tSale1 - 0.1, pop(19, 800, 500), 0.5)
    a(A.tPausa - 0.5, ficha(20, 660), 0.5)
    a(A.tArr - 0.2, fanfarria(21, 587.33), 0.4)
    # sílabas: aplausos de verdad en es-cue-la
    for k, tk in enumerate((B.tEs, B.tCue, B.tLa)):
        a(tk - 0.02, palmada(30 + k), 0.8, -0.1 + 0.1 * k)
    a(B.tTonica - 0.2, destello(34), 0.45)
    a(B.tPa - 0.1, boing(35, 500, 900, 0.25), 0.45, 0.4)
    a(B.tUlt - 0.2, whoosh(0.6, 36, 2500, 500), 0.35)
    for c, tc in enumerate(B.T_COL):
        a(tc - 0.35, papel_(40 + c), 0.4, -0.4 + 0.4 * c)
        for k, (_, _, tk) in enumerate(B.PALABRAS[c]):
            a(tk + 0.1, pop(44 + c * 4 + k, 750 + 80 * k, 450, 0.08), 0.35, -0.4 + 0.4 * c)
    for k in range(3):
        a(B.tAmaya + 0.3 + 0.15 * k, corazon_s(60 + k), 0.3, -0.3 + 0.3 * k)
    a(B.tDru - 0.05, ficha(64, 990), 0.5)
    a(B.tSolita - 0.2, risita(65), 0.4, 0.4)
    a(B.tReversa - 0.3, bip_reversa(B.tEs4 + 0.6 - B.tReversa + 0.3, 66), 0.5, 0.2)
    # pregunta 1 / reglas
    a(C.tP1 - 0.2, ficha(70, 520), 0.55)
    a(C.tMus - 0.2, signo(71), 0.45)
    cuenta3(C.tFinP1 + 0.15, C.T_R1 + 0.1, 72)
    a(C.tEsdR - 0.1, acierto(77), 0.6)
    a(C.tRayita, whoosh(0.4, 78, 1500, 4000), 0.4)
    a(C.tCam, acierto(79), 0.4, -0.4)
    a(C.tCal, bajon(80), 0.4, -0.4)
    for k, tk in enumerate((C.tArb, C.tFac, C.tCes)):
        a(tk + 0.1, pop(81 + k, 800, 500, 0.08), 0.4, 0.4)
    a(C.tCama, bajon(84), 0.35, 0.4)
    a(C.tHerm - 0.1, boing(85, 300, 500, 0.3), 0.45)
    for k, tk in enumerate(C.tSiem):
        a(tk - 0.05, plaf(86 + k), 0.5, -0.4 + 0.4 * k)
    a(C.tMama - 0.1, tic_tac(1.6, 90), 0.35)
    a(C.tSueter - 0.1, bajon(89), 0.4)
    a(C.tTodas - 0.2, destello(91), 0.4)
    # trampa
    a(D.tP2 - 0.2, ficha(95, 520), 0.55)
    a(D.tOjo - 0.2, boing(96, 900, 400, 0.35), 0.5)
    cuenta3(D.tFinP2 + 0.15, D.T_R2 + 0.1, 97)
    a(D.tGrave - 0.1, acierto(102), 0.6)
    a(D.tEsdr + 0.2, tachon(103), 0.6)
    a(D.tCorr - 0.3, papel_(104), 0.4)
    a(D.tTres + 1.2, bajon(105), 0.35, 0.3)
    # adverbios
    a(E.tVerbo + 0.2, whoosh(0.6, 110, 1800, 500), 0.4, 0.4)
    for k, tk in enumerate(E.tQs):
        a(tk - 0.15, pop(111 + k), 0.4, -0.45 + 0.3 * k)
    for k, (_, _, _, t1) in enumerate(E.EJ):
        a(t1 - 0.2, ficha(116 + k, 700 + 90 * k), 0.4)
    for k, (_, _, _, _, _, tt) in enumerate(E.TIPOS):
        a(tt - 0.2, acierto(121 + k), 0.3, -0.45 + 0.3 * k)
    a(E.OPI[0][3] - 0.2, acierto(126), 0.35, -0.4)
    a(E.OPI[1][3] - 0.2, bajon(127), 0.35)
    a(E.OPI[2][3] - 0.2, signo(128), 0.35, 0.4)
    a(E.tCerebro - 0.2, tachon(129), 0.5, 0.4)
    for k in range(3):                                       # «el perro ladra»: se oyen los ladridos
        a(E.tRonca + 0.1 + 0.9 * k, ladrido(130 + k), 0.6, -0.3)
    for k in range(2):
        a(E.tSiempre + 0.3 + 0.9 * k, ladrido(133 + k), 0.6, -0.3)
    cuenta3(E.tFinP3 + 0.15, E.T_R3 + 0.1, 133)
    a(E.tAyer - 0.1, acierto(138), 0.6)
    # autobiografía / anécdota
    for k, tk in enumerate((F.tA, F.tB, F.tG)):
        a(tk - 0.1, pop(140 + k, 600 + 120 * k, 400), 0.45, -0.4 + 0.4 * k)
    a(F.tYo - 0.2, boing(143, 400, 800, 0.3), 0.45, -0.4)
    a(F.tCuad - 0.3, papel_(144), 0.4, 0.3)
    a(F.tPeli - 0.4, tramo(chisporroteo(2.0, 145), 0.3), 0.15)          # proyector
    a(F.tClip - 0.2, pop(146), 0.45)
    for k, (_, tk) in enumerate(F.PREGS):
        a(tk - 0.1, ficha(147 + k, 700 + 70 * k), 0.4)
    a(F.tDom - 0.4, tramo(chisporroteo(2.2, 153), 0.4), 0.4, -0.3)    # hot cake en el sartén
    a(F.tHot - 0.2, whoosh(0.7, 154, 400, 2500), 0.5, -0.2)
    a(F.tPeg - 0.1, plaf(155), 0.7, -0.1)
    for k in range(4):
        a(F.tRisa - 0.4 + 0.25 * k, risita(156 + k), 0.4, 0.2 + 0.1 * k)
    a(F.tCinco2 - 0.2, acierto(160), 0.5)
    # carta
    for k, (_, tk) in enumerate(G.PARTES):
        a(tk - 0.15, papel_(165 + k), 0.4, 0.3)
    for k, (_, tk) in enumerate(G.FRASE):
        a(tk - 0.1, pop(171 + k, 500 + 90 * k, 350, 0.1), 0.45, -0.4 + 0.2 * k)
    a(G.tP4 - 0.2, ficha(177, 520), 0.55)
    cuenta3(G.tFinP4 + 0.15, G.T_R4 + 0.1, 178)
    for k, tk in enumerate(G.R_PARTES):
        a(tk - 0.1, pop(183 + k, 800, 500, 0.08), 0.35, 0.3)
    a(G.tMuy - 0.2, fanfarria(189, 659.25), 0.45)
    # repaso y cierre
    for k, tk in enumerate((Hh.tAg, Hh.tGr, Hh.tEs, Hh.tAdv, Hh.tAuto, Hh.tAnec, Hh.tCarta)):
        a(tk - 0.2, pop(190 + k), 0.4, -0.4 + 0.13 * k)
    a(Hh.tHoy - 0.2, acierto(200), 0.4, -0.4)
    a(Hh.tSopa - 0.2, acierto(201), 0.4, 0.2)
    a(Hh.tPuedes - 0.2, fanfarria(202, 523.25), 0.4)
    for k in range(5):
        a(Hh.tQuiero + 0.4 * k, corazon_s(203 + k), 0.3, -0.5 + 0.25 * k)
    a(Hh.tExito - 0.2, destello(210), 0.5)
    return [e for e in ev if 0 <= e[0] < TOTAL]
