# -*- coding: utf-8 -*-
"""SFX sintetizados del video de Amaya (bloques de sfx_proc.py + sonidos_base.py) anclados a las mismas palabras que la
animación (importa las anclas de cada plano_*.py). Sonidos nuevos: campana de Dolores, fuego, cañonazos del sitio, cadena que se
rompe, tambor de marcha, fanfarria, tictac de la cuenta regresiva, grillos de la noche."""
import math

import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bip, boing, bp, destello, env, hp, lp, norm, osc, pop, retumbo, ruido, signo, whoosh)
from sonidos_base import bajon, ficha, moneda_clink, papel_, tachon, tic_tac, tramo


# ------------------------------------------------------------ sonidos nuevos
def campana(seed=0, f=392.0, dur=3.0):
    """Campana de iglesia: parciales inarmónicos (hum, prime, tierce, quint, nominal) con batido lento."""
    x = np.zeros(int(dur * SR))
    for m, a, dk in ((0.5, 0.5, 1.2), (1.0, 1.0, 0.9), (1.19, 0.6, 0.7), (1.5, 0.45, 0.6), (2.0, 0.55, 0.5), (2.74, 0.25, 0.3)):
        x += osc(f * m * (1 + 0.002 * math.sin(m)), dur) * env(dur, 0.003, dk) * a * (1 + 0.15 * np.sin(2 * np.pi * 1.3 * _t(dur)))
    x[:int(0.02 * SR)] += bp(ruido(0.02, seed), 800, 4000) * 0.5
    return norm(x, 0.6)


def fuego(dur=2.0, seed=0):
    x = lp(ruido(dur, seed), 900, 2) * 0.4
    rg = _rng(seed + 1)
    for k in range(int(dur * 14)):
        c = bp(ruido(0.012, seed + 10 + k), 1500, 7000) * env(0.012, 0.0005, 0.006)
        i = int(rg.uniform(0, dur - 0.05) * SR)
        x[i:i + len(c)] += c * rg.uniform(0.3, 1.0)
    return norm(x * env(dur, 0.15, dur * 0.5), 0.45)


def canon(seed=0):
    d = 1.2
    x = lp(ruido(d, seed), 160, 3) * env(d, 0.002, 0.35) + osc(barrido(70, 35, d), d) * env(d, 0.002, 0.25) * 0.6
    return norm(x, 0.8)


def cadena(seed=0):
    """Cadena que se rompe: chasquido metálico + eslabones que caen."""
    out = np.zeros(int(1.2 * SR))
    rg = _rng(seed)
    for k in range(6):
        d = 0.35
        x = sum(osc(f * rg.uniform(0.9, 1.1), d) * env(d, 0.001, 0.12 / (1 + j)) / (1 + j) for j, f in enumerate((900, 1530, 2380)))
        i = int((0 if k == 0 else 0.15 + 0.12 * k + rg.uniform(0, 0.05)) * SR)
        out[i:i + len(x)] += x * (1.0 if k == 0 else 0.4)
    return norm(out, 0.55)


def tambor(dur=2.0, seed=0, bpm=120):
    """Redoblante de marcha: golpes a tiempo con un redoble corto cada compás."""
    x = np.zeros(int(dur * SR))
    paso = 60 / bpm
    for k in range(int(dur / paso)):
        for j in ((0,) if k % 4 else (0, 0.06, 0.12)):
            d = 0.12
            g = bp(ruido(d, seed + k * 3 + int(j * 100)), 180, 5000) * env(d, 0.001, 0.05) + osc(190, d) * env(d, 0.001, 0.04) * 0.5
            i = int((k * paso + j) * SR)
            x[i:i + len(g)] += g * (1.0 if j == 0 else 0.6)
    return norm(x, 0.5)


def fanfarria(seed=0, base=523.25):
    """Fanfarria corta de trompeta (arpegio mayor que sube y se queda en la tónica alta)."""
    notas = ((1.0, 0.12), (1.26, 0.12), (1.5, 0.12), (2.0, 0.55))
    out = np.zeros(int(1.2 * SR))
    i = 0
    for m, d in notas:
        f = base * m
        x = (osc(f, d, "tri") + 0.5 * osc(f * 2, d, "tri") + 0.25 * osc(f * 3, d)) * env(d, 0.01, d * 0.8)
        x *= 1 + 0.03 * np.sin(2 * np.pi * 6 * _t(d))
        out[i:i + len(x)] += x
        i += int(d * 0.9 * SR)
    return norm(lp(out, 4500), 0.5)


def acierto(seed=0):
    """«¡Eso!»: dos notas brillantes que suben + destello."""
    out = np.zeros(int(1.6 * SR))
    for k, f in enumerate((880, 1318.5)):
        d = 0.25
        x = (osc(f, d, "tri") + 0.3 * osc(f * 2, d)) * env(d, 0.003, 0.18)
        i = int(k * 0.11 * SR)
        out[i:i + len(x)] += x
    dz = destello(seed)
    out[:len(dz)] += dz * 0.6
    return norm(out, 0.55)


def grillos(dur, seed=0):
    t = _t(dur)
    gr = osc(4600, dur) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 30 * t))) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.9 * t)) ** 6
    x = gr * 0.12 + lp(ruido(dur, seed), 400) * 0.15
    return norm(x, 0.3)


def risita(seed=0):
    """«riu»: boing chiquito agudo, como risa bajita."""
    return boing(seed, 700, 1100, 0.16)


def corazon_s(seed=0):
    return pop(seed, 600, 900, 0.14)


# ------------------------------------------------------------ pistas
def pistas():
    import plano_a as A, plano_b as B, plano_c as C, plano_d as D, plano_e as E
    import plano_f as F, plano_g as G, plano_h as Hh, plano_i as I, plano_j as J
    from comun import TOTAL, T0
    ev = []

    def a(t, x, v=0.6, pan=0.0):
        ev.append((t, x, v, pan))

    def cuenta3(t0, t1, seed):
        for k in range(3):
            a(t0 + k * (t1 - t0) / 3, ficha(seed + k, 990 - 110 * k), 0.55)
        a(t0, tic_tac(t1 - t0, seed + 5), 0.35)

    # paso de un plano a otro: whoosh suave de acuarela
    for k, esc in enumerate(("causas", "grito", "truco", "inicio", "organizacion", "resistencia", "consumacion", "repaso",
                             "cierre")):
        a(T0(esc) - 0.1, whoosh(0.8, 300 + k, 250, 1800), 0.35)
    # gancho
    a(A.tHola - 0.1, ficha(1, 880), 0.5)
    a(A.tExamen - 0.2, signo(2), 0.5, 0.3)
    a(A.tCinco - 0.1, pop(3), 0.5)
    a(A.tRobot - 0.1, bip(4), 0.5, -0.3)
    a(A.tChistes, boing(5), 0.5, 0.3)
    a(A.tPausa - 0.1, ficha(6, 660), 0.5)
    a(A.tSale - 0.1, pop(7, 800, 500), 0.5)
    a(A.tArranc - 0.2, fanfarria(8, 523.25), 0.4)
    # causas
    a(B.tPorque - 0.1, signo(10), 0.5)
    a(B.tRey - 0.2, fanfarria(11, 392), 0.3, 0.4)
    a(B.tPiramide - 0.2, papel_(12), 0.4)
    for k, tk in enumerate((B.tPenins, B.tCriollos, B.tMestizos)):
        a(tk - 0.1, ficha(13 + k, 880 - 140 * k), 0.45, -0.3 + 0.3 * k)
    a(B.tMega - 0.1, bajon(16), 0.45)
    a(B.tIdeas - 0.2, destello(17), 0.4)
    a(B.tNapo - 0.2, tambor(1.8, 18, 140), 0.4, 0.3)
    a(B.tTrono, boing(19, 400, 200, 0.35), 0.5)
    a(B.tTruco - 0.2, destello(20), 0.4)
    for k, tk in enumerate((B.tInj, B.tIde, B.tNap)):
        a(tk - 0.1, pop(21 + k, 800 + 100 * k, 400), 0.5)
    # grito
    a(C.tQro - 0.2, papel_(30), 0.35)
    for k, tk in enumerate((C.tAll, C.tAld, C.tHid, C.tJos)):
        a(tk - 0.1, ficha(31 + k, 700 + 80 * k), 0.4, -0.4 + 0.25 * k)
    a(C.tDesc - 0.2, boing(36, 500, 250, 0.4), 0.55)
    a(C.tAvisar - 0.1, whoosh(0.6, 37, 600, 3000), 0.4)
    a(C.tCampana - 0.1, campana(38), 0.55)
    a(C.tCampana + 1.2, campana(39, 392 * 1.003), 0.35)
    a(C.tGrito - 0.2, fanfarria(40, 440), 0.4)
    a(C.tZorro - 0.1, boing(41), 0.45, 0.4)
    a(C.tPreg - 0.2, ficha(42, 520), 0.6)
    a(C.tQue, signo(43), 0.5)
    cuenta3(C.tFinP + 0.15, C.T_RESP + 0.1, 44)
    a(C.tR16 - 0.1, acierto(48), 0.6)
    # truco HMGI
    a(D.tTruco - 0.2, destello(50), 0.4)
    for k in range(4):
        a(D.tEt[k] - 0.2, pop(51 + k), 0.4, -0.45 + 0.3 * k)
        a(D.tFrase[k] - 0.1, ficha(56 + k, 660 + 110 * k), 0.4, -0.45 + 0.3 * k)
        a(D.tDice[k] - 0.05, boing(61 + k, 420 + 80 * k, 700 + 80 * k, 0.2), 0.45, -0.45 + 0.3 * k)
    a(D.tRep - 0.1, bip(66), 0.45, 0.5)
    # inicio
    a(E.tGente - 0.3, tambor(2.4, 70, 150), 0.35)
    a(E.tPip - 0.2, ficha(71, 740), 0.45)
    a(E.tFuego - 0.3, tramo(fuego(2.5, 72), 0.3), 0.5)
    a(E.tMonte, acierto(73), 0.45, -0.4)
    a(E.tCald, bajon(74), 0.45, 0.4)
    a(E.tFus - 0.1, canon(75), 0.35)
    a(E.tEscl - 0.1, cadena(76), 0.6)
    # organización
    a(F.tAlumno, whoosh(0.5, 80, 800, 2500), 0.35)
    a(F.tDolia - 0.1, boing(81, 600, 300, 0.3), 0.45, -0.5)
    a(F.tEjer - 0.3, tambor(2.6, 82, 132), 0.4, -0.3)
    for k in range(3):
        a(F.tAguanto + 0.2 + 0.7 * k, canon(83 + k), 0.3, 0.3)
    a(F.tSent - 0.4, papel_(86), 0.45)
    for k, tk in enumerate((F.tLibres, F.tEscl, F.tCastas)):
        a(tk - 0.1, ficha(87 + k, 880 + 110 * k), 0.45)
    a(F.tApatz - 0.1, destello(90), 0.45, 0.4)
    a(F.tSiervo - 0.2, destello(91), 0.4)
    a(F.tFus - 0.1, canon(92), 0.3)
    for k in range(5):
        a(F.tDinero - 0.1 + 0.15 * k + 1.0, moneda_clink(93 + k), 0.35, 0.3)
    a(F.tInfo - 0.4, whoosh(0.7, 98, 500, 2500), 0.4)
    a(F.tEspia - 0.2, tachon(99), 0.55)
    # resistencia
    a(G.tEsc - 0.1, whoosh(0.4, 100, 1200, 400), 0.4)
    a(G.tAtac - 0.2, boing(101, 300, 700, 0.3), 0.5, -0.3)
    a(G.tEscon - 0.1, whoosh(0.4, 102, 1500, 300), 0.45, 0.3)
    a(G.tUlt - 0.4, tic_tac(2.2, 103), 0.4, 0.4)
    a(G.tVac - 0.1, bajon(104), 0.35)
    a(G.tPrim - 0.2, fanfarria(105, 523.25), 0.45)
    # consumación
    a(Hh.tRealista - 0.2, ficha(110, 440), 0.5, -0.4)
    a(Hh.tCambio - 0.1, whoosh(0.9, 111, 300, 2600), 0.5)
    a(Hh.tAbrazo - 0.2, destello(112), 0.45)
    for k in range(3):
        a(Hh.tAbrazo + 0.4 * k, corazon_s(113 + k), 0.35, 0.2)
    for k, tk in enumerate((Hh.tRel, Hh.tInd, Hh.tUni)):
        a(tk - 0.15, pop(116 + k, 700 + 150 * k, 400), 0.5, -0.4 + 0.4 * k)
    a(Hh.tTrig - 0.2, tambor(1.5, 119, 120), 0.35)
    a(Hh.tBand - 0.2, papel_(120), 0.35)
    for k, tk in enumerate((Hh.tBl, Hh.tVe, Hh.tRo)):
        a(tk - 0.1, ficha(121 + k, 660 + 110 * k), 0.45, -0.4 + 0.4 * k)
    for k in range(3):
        a(Hh.tRiu - 0.2 + 0.28 * k, risita(124 + k), 0.5, -0.3 + 0.3 * k)
    a(Hh.tTrat - 0.2, papel_(128), 0.4)
    a(Hh.t27 - 0.2, ficha(129, 880), 0.5, 0.4)
    a(Hh.tEntro - 0.6, tambor(2.8, 130, 120), 0.45)
    a(Hh.tCiudad + 0.4, fanfarria(131, 523.25), 0.45)
    a(Hh.tCumple - 0.2, destello(132), 0.45, -0.3)
    a(Hh.tPais - 0.1, pop(133, 500, 900, 0.2), 0.55, 0.2)
    a(Hh.tPais + 0.1, fanfarria(134, 587.33), 0.45)
    # repaso y preguntas
    a(I.tRep - 0.2, bip(140), 0.45)
    a(I.t16 - 0.2, ficha(141, 660), 0.5, -0.4)
    a(I.t27 - 0.2, ficha(142, 880), 0.5, 0.4)
    a(I.tDos - 0.2, whoosh(0.5, 143, 900, 2400), 0.35)
    a(I.tPatrio - 0.3, fanfarria(144, 523.25), 0.4)
    a(I.tP2 - 0.2, ficha(145, 520), 0.6)
    a(I.tEtapas - 0.2, signo(146), 0.5)
    cuenta3(I.tFinP2 + 0.15, I.T_R2 + 0.1, 147)
    for k in range(4):
        a(I.tR2[k] - 0.15, papel_(151 + k), 0.35, -0.45 + 0.3 * k)
        a(I.tLid[k] - 0.1, ficha(155 + k, 660 + 110 * k), 0.45, -0.45 + 0.3 * k)
    a(I.tLid[3] + 0.4, acierto(160), 0.55)
    a(I.tP3 - 0.2, ficha(161, 520), 0.6)
    a(I.tQuien3 - 0.1, signo(162), 0.5)
    cuenta3(I.tFinP3 + 0.15, I.T_R3 + 0.1, 163)
    a(I.tJos - 0.1, acierto(167), 0.55, -0.4)
    for k, tk in enumerate((I.tRel, I.tInd, I.tUni)):
        a(tk - 0.15, pop(168 + k, 700 + 150 * k, 400), 0.45, 0.2 + 0.2 * k)
    a(I.tBien - 0.2, fanfarria(171, 659.25), 0.45)
    # cierre
    a(J.tLista - 0.2, acierto(180), 0.5)
    a(J.T_NOCHE, tramo(grillos(J.T_ANIMO - J.T_NOCHE + 0.5, 181), 0.4), 0.35)
    a(J.tQueda - 0.2, destello(182), 0.4)
    a(J.tPuedes - 0.2, fanfarria(183, 523.25), 0.4)
    for k in range(5):
        a(J.tQuiero + 0.5 * k, corazon_s(184 + k), 0.3, -0.5 + 0.25 * k)
    a(J.tExito - 0.2, destello(190), 0.5)
    return [e for e in ev if 0 <= e[0] < TOTAL]
