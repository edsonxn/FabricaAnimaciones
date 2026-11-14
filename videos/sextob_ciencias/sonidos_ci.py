# -*- coding: utf-8 -*-
"""SFX sintetizados del video 3 de sexto B (Ciencias), anclados a las mismas palabras que la animación (importa las anclas de cada
plano_*.py). Reutiliza los bloques de sfx_proc / sonidos_base / sonidos_amaya y añade lo de este guion: el SISEO del gas que se
escapa del tanque, el globo que se infla, el «¡ZAS!» del émbolo que regresa, el «¡BOING!» del virus contra la muralla, el ÑAM del
macrófago, el SILBATO y el «¡GOL!» de la cancha (partido de práctica y autogol)."""
import math

import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bip, boing, bp, destello, env, hp, lp, norm, osc, pop, retumbo, ruido, signo, whoosh)
from sonidos_base import bajon, ficha, inflar, masticar, papel_, tachon, tic_tac, tramo
from sonidos_amaya import acierto, corazon_s, fanfarria, risita


def siseo(dur=2.0, seed=0):
    """Gas que se escapa de la válvula: ruido agudo con un poco de silbido."""
    x = bp(ruido(dur, seed), 3000, 9000) + 0.15 * osc(barrido(4200, 3600, dur), dur)
    return norm(x * env(dur, 0.06, dur * 0.5), 0.45)


def zas(seed=0):
    """Émbolo que regresa de golpe: barrido rápido + golpecito seco."""
    d = 0.35
    x = bp(ruido(d, seed), 800, 6000) * env(d, 0.003, 0.08) * osc(barrido(300, 1800, d), d, "tri")
    g = lp(ruido(0.08, seed + 1), 1500) * env(0.08, 0.001, 0.02) * 0.9
    x[-len(g):] += g
    return norm(np.concatenate([x[:int(0.3 * SR)], np.zeros(int(0.05 * SR))]), 0.75)


def silbato(seed=0, dur=0.55):
    """Silbato de árbitro: tono de ~2,9 kHz con trino (la bolita adentro)."""
    t = _t(dur)
    f = 2900 + 120 * np.sign(np.sin(2 * np.pi * 28 * t))
    x = osc(f, dur) * (0.75 + 0.25 * np.sin(2 * np.pi * 28 * t)) + 0.2 * bp(ruido(dur, seed), 2500, 4000)
    return norm(x * env(dur, 0.01, None), 0.5)


def gol(dur=2.2, seed=0):
    """Gritito de «¡gol!» de la tribuna: ruido de voces que sube y baja + un tono festivo."""
    t = _t(dur)
    cuerpo = bp(ruido(dur, seed), 300, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.3 * t))
    x = cuerpo * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.7
    tono = osc(barrido(520, 880, 0.5), 0.5, "tri") * env(0.5, 0.01, 0.2)
    x[:len(tono)] += 0.3 * tono
    return norm(x, 0.5)


def sorpresa(seed=0):
    """«¿Eh?» cómico: tono que sube."""
    d = 0.35
    return norm(osc(barrido(260, 620, d), d, "tri") * env(d, 0.01, 0.15), 0.5)


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

    for k, esc in enumerate(("materia", "gas", "jeringa", "preg1", "resp1", "atmosfera", "aire", "preg2", "resp2", "defensa",
                             "leucocitos", "linfocitos", "preg3", "resp3", "vacunas", "autoinmune", "preg4", "resp4", "repaso",
                             "cierre")):
        a(T0(esc) - 0.1, whoosh(0.8, 300 + k, 250, 1800), 0.35)
    # gancho
    a(A.tHola - 0.1, ficha(1, 880), 0.5)
    a(A.tBata - 0.1, destello(2), 0.45)
    for k in range(4):
        a(A.tFotos - 0.1 + 0.22 * k, whoosh(0.4, 3 + k, 600, 2600), 0.35, -0.5 + 0.3 * k)
        a(A.tFotos + 0.35 + 0.22 * k, pop(8 + k, 900, 500, 0.08), 0.45, -0.5 + 0.3 * k)
    for k, tk in enumerate(A.tTema):
        a(tk - 0.15, pop(12 + k, 600 + 70 * k, 400), 0.45, -0.4 + 0.16 * k)
    a(A.tEjer - 0.1, tramo(retumbo(1.0, 17), 0.3), 0.35)
    a(A.tPausa - 0.5, ficha(18, 660), 0.5)
    a(A.tArr - 0.2, fanfarria(19, 587.33), 0.4)
    # materia / gas
    a(B.tOcupa - 0.1, pop(20, 700, 450), 0.45, -0.3)
    a(B.tMasa - 0.1, retumbo(0.6, 21), 0.4, 0.3)
    for k, tk in enumerate((B.tBanca, B.tAgua, B.tUst)):
        a(tk - 0.1, pop(22 + k, 800 + 60 * k, 500, 0.08), 0.4, -0.4 + 0.4 * k)
    a(B.tQ1 + 0.4, acierto(25), 0.35, -0.3)
    a(B.tQ2 + 0.4, acierto(26), 0.35, 0.3)
    a(B.tInfla - 0.2, inflar(1.6, 27), 0.5)
    a(B.tPesa + 0.2, boing(28, 300, 220, 0.4), 0.35)
    a(B.tDesinf - 0.1, bajon(29), 0.3)
    for k, tk in enumerate((B.tSol, B.tLiq, B.tGaseo)):
        a(tk - 0.1, pop(30 + k, 650 + 120 * k, 420), 0.45, -0.4 + 0.4 * k)
    a(B.tPied - 0.1, retumbo(0.5, 33), 0.4, -0.3)
    a(B.tVaso - 0.1, ficha(34, 1320), 0.35)
    a(B.tTanque - 0.2, ficha(35, 440), 0.35)
    a(B.tEscapan - 0.3, siseo(2.2, 36), 0.6, 0.2)                       # el gas se escapa: se oye
    # jeringa
    a(C.tExp - 0.2, signo(40), 0.4)
    a(C.tDedo - 0.1, pop(41, 500, 300, 0.12), 0.45, -0.3)
    a(C.tCuesta, tramo(lp(ruido(1.6, 42), 400) * 0.6, 0.3), 0.3)
    a(C.tYa - 0.2, bajon(43), 0.35)
    a(C.tReg - 0.1, zas(44), 0.75)
    a(C.tDuele - 0.1, boing(45, 900, 400, 0.3), 0.5, -0.4)
    a(C.tSoltar - 0.05, zas(46), 0.6)
    for k in range(5):
        a(C.tApri + 0.2 * k, pop(47 + k, 1200 - 80 * k, 700, 0.06), 0.3, -0.4 + 0.2 * k)
    a(C.tEmpuj - 0.1, boing(52, 260, 520, 0.3), 0.45)
    a(C.tP1 - 0.2, ficha(53, 520), 0.55)
    cuenta3(C.tFinP1 + 0.15, C.T_R1 + 0.1, 54)
    a(C.tOcupan - 0.1, acierto(59), 0.6)
    a(C.tEso - 0.2, fanfarria(60, 659.25), 0.35)
    # atmósfera / aire
    a(D.tCapa - 0.2, whoosh(1.0, 61, 200, 1200), 0.35)
    a(D.tGrav - 0.2, retumbo(0.8, 62), 0.35)
    a(D.tCobija - 0.2, destello(63), 0.4)
    for k, tk in enumerate((D.tClima, D.tMov, D.tAireA)):
        a(tk - 0.15, papel_(64 + k), 0.4, -0.4 + 0.4 * k)
    for k, (_, _, _, t_num, t_nom) in enumerate(D.FILAS):
        a(t_num - 0.1, tramo(tic_tac(0.8, 68 + k), 0.2), 0.25)
        a(t_nom - 0.1, pop(72 + k, 700 + 90 * k, 450, 0.08), 0.4)
    a(D.tSalon - 0.2, signo(76), 0.4)
    a(D.tP2 - 0.2, ficha(77, 520), 0.55)
    a(D.tOjo - 0.2, boing(78, 900, 400, 0.35), 0.5)
    cuenta3(D.tFinP2 + 0.15, D.T_R2 + 0.1, 79)
    a(D.tNitR - 0.1, acierto(84), 0.6)
    a(D.tOxi2 + 0.2, tachon(85), 0.55)
    # defensa
    a(E.tSist - 0.2, destello(90), 0.4)
    for k, tk in enumerate((E.tBact, E.tHong, E.tVir, E.tSust)):
        a(tk - 0.3, whoosh(0.5, 91 + k, 1800, 400), 0.35, -0.5 if k < 2 else 0.5)
        a(tk + 0.3, boing(95 + k, 400, 250, 0.25), 0.3, -0.5 if k < 2 else 0.5)
    a(E.tCast - 0.2, fanfarria(99, 392.0), 0.3)
    for k in range(4):                                                  # el virus rebota en la muralla (cada 2,4 s)
        a(E.tMur + 2.4 * k + 0.45 * 2.4, boing(100 + k, 700, 320, 0.3), 0.35, 0.1)
    for k, (_, tk) in enumerate(E.MUROS):
        a(tk - 0.1, pop(105 + k, 650 + 80 * k, 420), 0.4, -0.4 if k < 3 else 0.4)
    a(E.tHeroe - 0.2, fanfarria(110, 523.25), 0.45, 0.3)
    a(E.tNaces - 0.2, corazon_s(111), 0.4)
    # leucocitos
    a(F.tBrinca - 0.5, whoosh(1.0, 120, 400, 2200), 0.45)
    a(F.tBrinca + 0.5, boing(121, 300, 600, 0.3), 0.4)
    for k in range(3):
        a(F.tSalen + 0.25 * k, retumbo(0.3, 122 + k), 0.4, -0.3 + 0.3 * k)
    a(F.tBlanco - 0.1, whoosh(0.6, 125, 2500, 600), 0.35, 0.3)
    for k, tk in enumerate((F.tGatos, F.tMonos, F.tLeones)):
        a(tk - 0.1, destello(126 + k), 0.4, -0.45 + 0.45 * k)
    for k in range(6):                                                   # enzimas
        a(F.tSueltan + 0.18 * k, pop(130 + k, 1400, 900, 0.05), 0.3, 0.1 * k)
    a(F.tEnz + 0.6, sorpresa(136), 0.4, 0.4)
    a(F.tCrecen - 0.2, inflar(0.8, 137), 0.4)
    a(F.tComen - 0.1, masticar(3, 138), 0.6)
    a(F.tComen + 0.2, risita(139), 0.3)
    a(F.tListos - 0.2, ficha(140, 1180), 0.4)
    a(F.tDestr + 0.1, pop(141, 400, 150, 0.3), 0.6)
    a(F.tDestr + 0.2, destello(142), 0.4)
    for k in range(5):
        a(F.tFabr + 0.25 * k, pop(143 + k, 900 + 60 * k, 600, 0.06), 0.3, 0.1 * k)
    a(F.tMem - 0.3, papel_(148), 0.4, 0.4)
    a(F.tQue - 0.2, signo(149), 0.4)
    for k, tk in enumerate((F.tTox, F.tBac, F.tVir, F.tPed)):
        a(tk - 0.15, pop(150 + k, 600 + 80 * k, 400), 0.4, -0.45 + 0.3 * k)
    a(F.tAjeno - 0.1, acierto(155), 0.45)
    for k in range(6):
        a(F.tPega - 0.5 + 0.12 * k + 0.6, pop(156 + k, 1100, 700, 0.05), 0.35, -0.5 + 0.2 * k)
    a(F.tCalco - 0.2, papel_(162), 0.5)
    a(F.tDestr2 - 0.05, pop(163, 500, 120, 0.35), 0.7)
    a(F.tDestr2, destello(164), 0.5)
    a(F.tCuerpo - 0.2, acierto(165), 0.35)
    # preg3 / resp3
    a(G.tP3 - 0.2, ficha(170, 520), 0.55)
    cuenta3(G.tFinP3 + 0.15, G.T_R3 + 0.1, 171)
    a(G.tLeuR - 0.1, acierto(176), 0.6)
    for k, tk in enumerate(G.R3_TR):
        a(tk - 0.1, destello(177 + k), 0.35, -0.45 + 0.45 * k)
    a(G.tMuyBien - 0.2, fanfarria(180, 587.33), 0.4)
    # vacunas
    a(G.tActivar - 0.1, destello(181), 0.45)
    a(G.tMem - 0.3, papel_(182), 0.35, 0.4)
    a(G.tDebil - 0.3, bajon(183), 0.3, -0.3)
    a(G.tPartido - 0.3, silbato(184), 0.55)
    a(G.tFlojito + 0.2, pop(185, 300, 200, 0.12), 0.5)                 # patada
    a(G.tFlojito + 0.8, gol(2.0, 186), 0.5)
    a(G.tLlega - 0.3, retumbo(1.0, 187), 0.45, 0.4)
    a(G.tSabe - 0.1, pop(188, 300, 200, 0.12), 0.5)
    a(G.tSabe + 0.5, gol(2.2, 189), 0.55)
    a(G.tSabe + 0.5, silbato(190, 0.4), 0.4)
    # autoinmune
    a(G.tConf - 0.2, sorpresa(191), 0.45)
    for k in range(3):
        a(G.tAtaca + 0.2 + 0.25 * k, pop(192 + k, 500, 250, 0.1), 0.45, 0.3 + 0.1 * k)
    a(G.tUno - 0.2, ficha(195, 880), 0.4)
    a(G.tAutobio - 0.5, papel_(196), 0.4, 0.4)
    a(G.tAutogol - 0.5, pop(197, 300, 200, 0.12), 0.5)
    a(G.tAutogol, bajon(198), 0.5)
    a(G.tAutogol + 0.1, tachon(199), 0.45, -0.5)
    for k, tk in enumerate((G.tComan, G.tHagan, G.tDuerman)):
        a(tk - 0.3, acierto(200 + k), 0.3, -0.4 + 0.4 * k)
    a(G.tP4 - 0.2, ficha(203, 520), 0.55)
    cuenta3(G.tFinP4 + 0.15, G.T_R4 + 0.1, 204)
    a(G.tDebR - 0.1, acierto(209), 0.6)
    a(G.tEso - 0.2, fanfarria(210, 659.25), 0.4)
    # repaso y cierre
    for c, (_, _, tc, items) in enumerate(Hh.COLS):
        a(tc - 0.3, papel_(220 + c), 0.4, -0.4 + 0.4 * c)
        for k, (_, tk) in enumerate(items):
            a(tk - 0.2, pop(225 + c * 6 + k, 700 + 60 * k, 450, 0.08), 0.3, -0.4 + 0.4 * c)
    a(Hh.tLogro - 0.2, fanfarria(250, 523.25), 0.5)
    for k in range(6):
        a(Hh.tTodo - 0.3 + 0.15 * k, pop(251 + k, 900, 500, 0.06), 0.3, -0.5 + 0.2 * k)
    a(Hh.tGanas - 0.3, fanfarria(260, 587.33), 0.4)
    for k in range(5):
        a(Hh.tMucho + 0.4 * k, corazon_s(261 + k), 0.3, -0.5 + 0.25 * k)
    a(Hh.tSextoB - 0.2, destello(270), 0.5)
    return [e for e in ev if 0 <= e[0] < TOTAL]
