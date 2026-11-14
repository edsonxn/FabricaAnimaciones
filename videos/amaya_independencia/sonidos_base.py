# -*- coding: utf-8 -*-
"""SFX sintetizados del video del chicle (bloques de sfx_proc.py) anclados a las mismas palabras que la animación
(importa las anclas de cada plano_*.py). Sonidos nuevos de este video: bomba que se infla, masticar, tripas, ácido que
chisporrotea, apretón de músculo, escoba, bacterias, monedas, pájaros y grillos, olla que hierve."""
import math

import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bip, boing, bp, burbuja, destello, env, glup, hp, latido, lp, norm, osc, pop,
                      ruido, signo, trago, whoosh)


def tramo(x, fade=0.5):
    n = int(fade * SR)
    x = x.copy()
    x[:n] *= np.linspace(0, 1, n)
    x[-n:] *= np.linspace(1, 0, n)
    return x


# ------------------------------------------------------------ camas
def parque(dur, seed=0):
    """Aire libre: viento suave + pájaros (gorjeos con barrido) de vez en cuando."""
    x = lp(ruido(dur, seed), 500, 2) * 0.35
    rg = _rng(seed + 1)
    for k in range(int(dur * 0.8)):
        d = rg.uniform(0.08, 0.16)
        f0 = rg.uniform(2600, 4200)
        p = osc(1, d) * 0
        for j in range(rg.integers(2, 5)):
            c = np.sin(2 * np.pi * np.cumsum(barrido(f0, f0 * rg.uniform(0.7, 1.4), d)) / SR) * env(d, 0.005, d * 0.8)
            i = int((rg.uniform(0, dur - 1) + j * d * 1.3) * SR)
            x[i:i + len(c)] += c * 0.12
    return norm(x, 0.35)


def selva(dur, seed=0):
    """Selva: grillos (pulsos agudos) + pájaros graves + rumor de hojas."""
    t = _t(dur)
    x = bp(ruido(dur, seed), 300, 1600) * 0.25
    gr = osc(4300, dur) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 28 * t))) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.7 * t)) ** 4
    x += gr * 0.06
    rg = _rng(seed + 3)
    for k in range(int(dur * 0.5)):
        d = 0.35
        f = rg.uniform(700, 1300)
        c = np.sin(2 * np.pi * np.cumsum(barrido(f, f * 1.5, d)) / SR) * env(d, 0.02, 0.3)
        i = int(rg.uniform(0, dur - 0.5) * SR)
        x[i:i + len(c)] += c * 0.12
    return norm(x, 0.35)


def cuerpo(dur, seed=0, f=48):
    """Por dentro del cuerpo: rumor grave líquido + latido lejano + gorgoteos."""
    t = _t(dur)
    x = lp(ruido(dur, seed), 180, 2) * 0.6 + osc(f, dur) * 0.15 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * t))
    lt = latido(seed)
    for k in range(int(dur / 0.9)):
        i = int(k * 0.9 * SR)
        x[i:i + len(lt)] += lt[:max(0, len(x) - i)] * 0.25
    rg = _rng(seed + 5)
    for k in range(int(dur * 0.6)):
        g = tripas(seed + 10 + k, dur=rg.uniform(0.3, 0.7))
        i = int(rg.uniform(0, dur - 1) * SR)
        x[i:i + len(g)] += g * 0.25
    return norm(x, 0.35)


# ------------------------------------------------------------ eventos
def inflar(dur=1.6, seed=0):
    """Bomba de chicle que se infla: soplido filtrado que sube de tono."""
    t = _t(dur)
    f = 300 + 900 * (t / dur) ** 1.5
    x = ruido(dur, seed) * 0.6
    out = np.zeros_like(x)
    for k in range(0, len(x), 2048):
        out[k:k + 2048] = bp(x[k:k + 2048], f[k] * 0.8, f[k] * 1.4)
    return norm(out * env(dur, 0.2, dur * 0.2), 0.5)


def masticar(n=4, seed=0):
    """Masticar chicle: chasquidos húmedos (ruido corto filtrado + pop grave)."""
    d = 0.22
    out = np.zeros(int(n * d * SR) + SR // 4, np.float32)
    for k in range(n):
        c = bp(ruido(0.07, seed + k), 600, 2400) * env(0.07, 0.002, 0.05) * 0.7
        p_ = pop(seed + k, 300, 160, 0.08)[:len(c)]
        c[:len(p_)] += p_ * 0.4
        i = int(k * d * SR)
        out[i:i + len(c)] += c
    return norm(out, 0.5)


def tripas(seed=0, dur=0.6):
    """Gorgoteo de tripas: burbujas graves en serie con un barrido."""
    t = _t(dur)
    f = 90 + 60 * np.sin(2 * np.pi * (3 + seed % 3) * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 11 * t) ** 2)
    x += lp(ruido(dur, seed), 400) * 0.4
    return norm(x * env(dur, 0.05, dur * 0.6), 0.5)


def acido(dur=1.4, seed=0):
    """Chisporroteo de ácido: crepitar agudo de impulsos aleatorios."""
    x = np.zeros(int(dur * SR), np.float32)
    rg = _rng(seed)
    for k in range(int(dur * 120)):
        i = int(rg.uniform(0, dur - 0.01) * SR)
        c = hp(ruido(0.004, seed + k), 3000) * rg.uniform(0.2, 1)
        x[i:i + len(c)] += c
    return norm(x * env(dur, 0.1, 0.4), 0.45)


def apreton(seed=0, dur=0.7):
    """Apretón de músculo (peristalsis): squish grave que baja."""
    x = np.sin(2 * np.pi * np.cumsum(barrido(220, 70, dur)) / SR) * 0.5 + lp(ruido(dur, seed), 600) * 0.5
    return norm(x * env(dur, 0.08, dur * 0.7), 0.5)


def barrer(dur=1.2, seed=0):
    """Escobazo: ráfaga de ruido de cerdas (pasa de grave a agudo) + whoosh."""
    x = bp(ruido(dur, seed), 1200, 6000) * env(dur, 0.25, 0.6)
    return norm(x + whoosh(dur, seed + 1, 200, 1800)[:len(x)] * 0.5, 0.55)


def bacterias(dur=2.0, seed=0):
    """Multitud de bacterias: chirridos agudos tipo cuchicheo."""
    x = np.zeros(int(dur * SR), np.float32)
    rg = _rng(seed)
    for k in range(int(dur * 9)):
        d = rg.uniform(0.05, 0.12)
        f = rg.uniform(900, 2200)
        c = osc(f, d, "tri") * env(d, 0.005, d * 0.7) * (1 + 0.4 * osc(37, d))
        i = int(rg.uniform(0, dur - 0.15) * SR)
        x[i:i + len(c)] += c * 0.25
    return norm(x, 0.4)


def moneda_clink(seed=0):
    d = 0.6
    x = sum(osc(f, d) * env(d, 0.001, 0.5 / (1 + j)) * (0.6 / (1 + j)) for j, f in enumerate((2100, 3350, 5200, 6100)))
    return norm(x, 0.5)


def olla(dur=2.0, seed=0):
    """Olla que hierve: burbujas grandes y vapor."""
    x = hp(ruido(dur, seed), 2000) * 0.15
    rg = _rng(seed + 1)
    for k in range(int(dur * 8)):
        b = burbuja(seed + k, rg.uniform(0.6, 1.6))
        i = int(rg.uniform(0, dur - 0.2) * SR)
        x[i:i + len(b)] += b[:max(0, len(x) - i)] * 0.4
    return norm(x * env(dur, 0.2, 0.5), 0.45)


def tachon(seed=0):
    d = 0.32
    x = bp(ruido(d, seed), 1500, 5000) * env(d, 0.01, 0.25)
    p = pop(seed, 500, 200, 0.12)
    x[:len(p)] += p[:len(x)] * 0.3
    return norm(x, 0.5)


def ficha(seed=0, f=880):
    d = 0.12
    return norm(osc(f, d, "tri") * env(d, 0.002, 0.1) + osc(f * 2, d) * env(d, 0.002, 0.05) * 0.3, 0.45)


def caja_registradora(seed=0):
    """«Ding» antiguo para la caja de 1870: campanita + traqueteo."""
    d = 1.0
    x = osc(1760, d) * env(d, 0.002, 0.9) * 0.5 + osc(2637, d) * env(d, 0.002, 0.6) * 0.3
    x[:int(0.12 * SR)] += bp(ruido(0.12, seed), 800, 3000) * 0.4
    return norm(x, 0.5)


# ------------------------------------------------------------ pistas
def pistas():
    import plano_a as A, plano_b as B, plano_c as C, plano_d as D, plano_e as E, plano_f as F, plano_g as G
    from comun import TOTAL
    ev = []

    def a(t, x, v=0.6, pan=0.0):
        ev.append((t, x, v, pan))

    # camas
    a(0, tramo(parque(A.T_MAPA + 0.8, 1)), 0.35)
    a(B.T_SELVA, tramo(selva(B.T_SEPIA - B.T_SELVA + 0.8, 2)), 0.4)
    a(C.T_INI, tramo(cuerpo(F.T_INI - C.T_INI + 0.8, 3)), 0.32)
    a(G.T_PARQUE, tramo(parque(TOTAL - G.T_PARQUE, 4)), 0.3)
    # gancho
    a(0.4, inflar(A.tTragas - 0.7, 10), 0.5)
    a(A.tTragas - 0.25, pop(11, 900, 300, 0.2), 0.9)
    a(A.tTragas + 0.05, glup(12), 0.9)
    a(A.tEstomago - 0.3, ficha(13, 660), 0.6, 0.3)
    a(A.tSiete - 0.1, boing(14), 0.6, 0.5)
    for k in range(6):
        a(A.tCreces + k * (A.tPrimaria - A.tCreces) / 6, ficha(20 + k, 1000 + 60 * k), 0.4, 0.5)
    a(A.tCumples - 0.2, destello(30), 0.5, -0.5)
    a(A.tPrimaria - 0.2, pop(31), 0.5)
    a(A.tCierto - 0.2, signo(32), 0.6)
    a(A.T_MAPA, whoosh(0.9, 33), 0.6)
    a(A.tBoca - 0.2, barrido_cinta(A.tSale - A.tBoca + 0.4, 34), 0.35)
    a(A.tSi - 0.1, boing(35, 500, 300, 0.4), 0.6)
    # origen
    a(B.T_INI + 0.3, bp(ruido(0.5, 40), 1500, 6000) * env(0.5, 0.01, 0.4), 0.4)
    a(B.tComida + 0.35, tachon(41), 0.6, 0.4)
    a(B.T_SELVA, whoosh(0.9, 42), 0.5)
    for k in range(5):
        a(B.tCortas - 0.1 + k * 0.2, tachon(43 + k), 0.35, 0.5)
    a(B.tSavia, burbuja(48, 0.8), 0.5, 0.5)
    a(B.tChico - 0.2, ficha(49, 740), 0.5, -0.4)
    a(B.tMayas, masticar(6, 50), 0.6, -0.4)
    a(B.tChicle2 - 0.2, pop(51), 0.6)
    a(B.T_SEPIA, whoosh(0.9, 52), 0.5)
    a(B.tSanta - 0.3, ficha(53, 520), 0.5)
    a(B.tHule - 0.2, boing(54, 200, 120, 0.3), 0.6, 0.5)
    a(B.tAdams - 0.3, ficha(55, 620), 0.5, 0.5)
    a(B.tFracaso - 1.2, olla(1.2, 56), 0.4)
    a(B.tFracaso - 0.1, bajon(57), 0.6)
    a(B.tMastica - 0.3, masticar(5, 58), 0.6, -0.5)
    a(B.tNacio - 0.4, caja_registradora(59), 0.6)
    a(B.T_HOY, whoosh(0.9, 60), 0.5)
    a(B.tHoy + 0.4, tachon(61), 0.5, -0.6)
    a(B.tLlanta - 0.3, boing(62, 180, 110, 0.3), 0.5, -0.5)
    a(B.tPega - 0.3, pop(63, 700, 350), 0.5, 0.5)
    a(B.tAzucar - 0.2, destello(64), 0.4)
    a(B.tGris - 0.2, apreton(65, 0.5), 0.4)
    a(B.tTragaste - 0.3, glup(66), 0.6)
    # bajada
    a(C.T_INI, whoosh(0.9, 70), 0.5)
    a(C.tLengua - 0.2, apreton(71, 0.9), 0.6)
    a(C.tEpi, pop(72, 400, 250, 0.15), 0.6, 0.3)
    a(C.tPulmones - 0.2, tachon(73), 0.5, 0.4)
    a(C.tCae - 0.3, trago(74), 0.7)
    for k in range(5):
        a(C.tOndas - 0.2 + k * 0.9, apreton(75 + k), 0.5)
    a(C.tPasta, apreton(80, 0.6), 0.4, 0.5)
    a(C.tCabeza - 0.3, boing(81), 0.5, 0.5)
    a(C.tEstom, glup(82), 0.6)
    # estómago
    a(D.T_INI + 0.8, burbuja(90, 0.5), 0.9)
    a(D.tSiete - 0.3, ficha(91), 0.5, 0.5)
    a(D.tAcido - 0.4, acido(1.6, 92), 0.5)
    a(D.tLimon - 0.3, pop(93), 0.5, -0.5)
    a(D.tPepsina - 0.1, masticar(4, 94), 0.5, 0.5)
    a(D.tCortan, tachon(95), 0.4, 0.4)
    a(D.tAprieta - 0.3, tripas(96, 1.2), 0.7)
    a(D.tPan, acido(1.0, 97), 0.4, -0.5)
    a(D.tBistec, acido(1.0, 98), 0.4, 0.5)
    a(D.tNada - 0.2, bip(99, 1320, 0.07, True), 0.5)
    a(D.tRomper + 0.2, boing(100, 400, 800, 0.3), 0.7, 0.3)
    a(D.tIgual - 0.2, destello(101), 0.5)
    a(D.tMoco - 0.3, burbuja(102, 0.4), 0.5)
    a(D.tSecas - 0.9, ficha(103), 0.4)
    a(D.tHora - 0.3, tic_tac(1.5, 104), 0.4, 0.5)
    a(D.tOnda - 0.3, barrer(1.8, 105), 0.7)
    a(D.tEscoba - 0.3, barrer(1.2, 106), 0.7)
    a(D.tLleva, trago(107), 0.6, 0.6)
    # intestinos
    a(E.T_INI, whoosh(0.8, 110), 0.4)
    a(E.tSeis - 0.3, barrido_cinta(1.5, 111), 0.4)
    a(E.T_TUNEL, whoosh(0.9, 112), 0.5)
    a(E.tBilis - 0.3, burbuja(113), 0.5, -0.4)
    a(E.tPancreas - 0.3, burbuja(114, 1.3), 0.5, 0.4)
    for k, tt in enumerate((E.tAzucar, E.tGrasas, E.tProt)):
        a(tt + 0.3, pop(115 + k, 600, 300, 0.12), 0.4, -0.5 + 0.5 * k)
    a(E.tNada - 0.2, bip(118), 0.4)
    for k in range(6):
        a(E.tAvanza + k * (E.tMetro + 1.0 - E.tAvanza) / 6, ficha(120 + k, 700 + 80 * k), 0.35, 0.6)
    a(E.T_GRUESO, whoosh(0.9, 127), 0.5)
    a(E.tBacterias - 0.3, bacterias(E.tJunta - E.tBacterias + 0.5, 128), 0.45)
    a(E.tTampoco + 0.4, boing(129, 600, 300, 0.3), 0.6)
    a(E.tJunta - 0.2, apreton(130, 1.0), 0.5)
    a(E.tAgua - 0.2, burbuja(131, 0.6), 0.5)
    a(E.T_FINAL, whoosh(0.9, 132), 0.5)
    a(E.tAdios - 0.3, glup(133), 0.6)
    a(E.tAdios, destello(134), 0.5, 0.5)
    a(E.tNo7, tachon(135), 0.6, 0.3)
    # peligro
    a(F.tUno - 0.3, pop(140), 0.5, -0.4)
    a(F.tExc - 0.3, signo(141), 0.6, 0.4)
    a(F.tAnio - 0.3, papel_(142), 0.5)
    a(F.tHosp - 0.3, ficha(143, 540), 0.5, 0.6)
    for k in range(5):
        a(F.tCinco - 0.3 + k * 0.35, masticar(1, 144 + k), 0.4, -0.3)
    a(F.tEstr - 0.2, tripas(150, 0.8), 0.6)
    a(F.tTanta, apreton(151, 1.0), 0.5)
    a(F.tBezoar - 0.3, bajon(152), 0.6)
    a(F.T_RX, whoosh(0.9, 153), 0.5)
    for k in range(4):
        a(F.tMonedas - 0.4 + k * 0.12, moneda_clink(154 + k), 0.45, 0.1 * k)
    a(F.tLeccion - 0.2, ficha(160), 0.5)
    a(F.tAcc - 0.3, pop(161), 0.4, -0.5)
    a(F.tAhi - 0.2, tachon(162), 0.6, 0.5)
    # cierre
    a(G.T_INI, whoosh(0.8, 170), 0.4)
    a(G.tSalio, signo(171), 0.5)
    a(G.tPapas, bip(172, 900, 0.1, True), 0.4)
    a(G.tGeneraciones - 0.3, olla(0.1, 173) * 0, 0.0)
    a(G.tGris - 0.2, boing(174), 0.5)
    a(G.T_PARQUE, whoosh(0.9, 175), 0.5)
    a(G.tEscoba - 0.4, barrer(1.0, 176), 0.5, 0.4)
    a(G.tBasura, whoosh(0.5, 177, 600, 2000), 0.4)
    a(G.tBasura + 0.5, pop(178, 300, 150, 0.15), 0.6, 0.1)
    a(G.tMesa + 0.1, tachon(179), 0.5, 0.6)
    a(G.tSuscribete - 0.3, ficha(180, 1046), 0.6)
    a(G.tProximo - 0.3, olla(2.5, 181), 0.4, 0.7)
    return ev


def barrido_cinta(dur=1.5, seed=0):
    """Rastro de la bolita en el mapa / cinta métrica que se desenrolla: tiza suave."""
    x = bp(ruido(dur, seed), 2000, 6000) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * _t(dur)))
    return norm(x * env(dur, 0.05, 0.3), 0.3)


def bajon(seed=0):
    """«Wah-wah» de fracaso: dos notas que bajan."""
    out = []
    for f0, f1 in ((392, 370), (330, 262)):
        d = 0.35
        out.append(osc(1, d) * 0 + np.sin(2 * np.pi * np.cumsum(barrido(f0, f1, d)) / SR) * env(d, 0.02, 0.3))
    return norm(np.concatenate(out), 0.45)


def tic_tac(dur=1.5, seed=0):
    x = np.zeros(int(dur * SR), np.float32)
    for k in range(int(dur * 4)):
        c = bp(ruido(0.02, seed + k), 2500 if k % 2 else 1800, 7000) * env(0.02, 0.001, 0.015)
        i = int(k * 0.25 * SR)
        x[i:i + len(c)] += c
    return norm(x, 0.4)


def papel_(seed=0):
    d = 0.5
    return norm(bp(ruido(d, seed), 1000, 7000) * env(d, 0.05, 0.4) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * _t(d))), 0.4)
