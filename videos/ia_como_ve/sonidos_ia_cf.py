# -*- coding: utf-8 -*-
"""SFX sintetizados de los planos c-f (gato 1959, neurona y filtros, capas, aprender), anclados a sus mismas palabras."""
import numpy as np

from sfx_proc import SR, _rng, _t, barrido, bip, bp, burbuja, destello, env, hp, lp, norm, osc, pop, ruido, signo, whoosh
from sonidos_ia import (_plano, carta, cascada, cuadricula, error, ficha, interruptor, lupa, maquina, nubecita, procesa, sello,
                        tachon, tramo)


def crepitar(dur, seed=0):
    """Película vieja: chasquidos sueltos sobre siseo suave (el laboratorio de 1959)."""
    x = hp(ruido(dur, seed), 2000) * 0.05
    r = _rng(seed)
    for k in range(int(dur * 9)):
        d = 0.004
        c = ruido(d, seed + k) * np.linspace(1, 0, int(d * SR))
        i = int(r.uniform(0, dur - d) * SR)
        x[i:i + len(c)] += c * r.uniform(0.2, 1)
    return norm(lp(x, 7000), 0.25)


def disparos(dur, tasa, seed=0):
    """Una neurona en el altavoz del laboratorio: «tic-tic-tic» secos (potenciales de acción) a `tasa` por segundo."""
    x = np.zeros(int(dur * SR) + SR // 8)
    r = _rng(seed)
    tt = 0.0
    while tt < dur and tasa > 0:
        d = 0.006
        c = hp(ruido(d, seed + int(tt * 1000)), 1500) * env(d, 0.0003, 0.0015)
        i = int(tt * SR)
        x[i:i + len(c)] += c
        tt += r.exponential(1 / tasa)
    return norm(x, 0.5)


def clic_perilla(seed=0, n=4):
    """Perilla que gira: trinquete de clics finos."""
    out = np.zeros(int((0.05 * n + 0.1) * SR))
    for k in range(n):
        d = 0.012
        c = bp(ruido(d, seed + k), 2500, 9000) * env(d, 0.0005, 0.003)
        i = int(k * 0.05 * SR)
        out[i:i + len(c)] += c
    return norm(out, 0.35)


def ding(seed=0, f=1318):
    d = 1.4
    x = osc(f, d) * env(d, 0.002, 0.45) + osc(f * 2.76, d) * env(d, 0.002, 0.12) * 0.4 + osc(f * 5.4, d) * env(d, 0.001, 0.04) * 0.2
    return norm(x, 0.45)


def bloque(seed=0, f=520):
    """Bloque de madera: un piso que se pone."""
    d = 0.25
    x = osc(f, d) * env(d, 0.001, 0.04) + bp(ruido(d, seed), 600, 3000) * env(d, 0.0005, 0.01) * 0.5
    return norm(x, 0.5)


def caida(seed=0, dur=0.9):
    """Algo que baja: tono que cae con whoosh (la bola del error)."""
    x = osc(barrido(900, 160, dur), dur, "tri") * env(dur, 0.02, dur * 0.5) * 0.5
    w = whoosh(dur, seed, 1800, 300)
    n = min(len(x), len(w))
    x[:n] += w[:n] * 0.6
    return norm(x, 0.5)


def golpe(seed=0):
    d = 0.4
    x = osc(barrido(120, 50, d), d) * env(d, 0.002, 0.08) + lp(ruido(d, seed), 900) * env(d, 0.001, 0.03) * 0.6
    return norm(x, 0.7)


def gotas(n, dur, seed=0):
    out = np.zeros(int(dur * SR) + SR // 2)
    r = _rng(seed)
    for k in range(n):
        b = burbuja(seed + k, r.uniform(0.6, 1.0))
        i = int(r.uniform(0, dur) * SR)
        out[i:i + len(b)] += b[:len(out) - i] * r.uniform(0.3, 0.8)
    return norm(out, 0.5)


def fanfarria(seed=0):
    out = np.zeros(int(1.6 * SR))
    for k, f in enumerate((523, 659, 784, 1046)):
        d = 1.2 - 0.15 * k
        x = (osc(f, d, "saw") * 0.4 + osc(f * 2, d) * 0.2) * env(d, 0.01, d * 0.6)
        i = int(k * 0.1 * SR)
        out[i:i + len(x)] += lp(x, 3500)
    return norm(out, 0.5)


def barrido_sube(seed=0):
    d = 0.6
    x = osc(barrido(300, 1200, d), d, "tri") * env(d, 0.02, 0.3)
    return norm(lp(x, 4000), 0.35)


def rasgueo_barrido(dur, seed=0):
    """La lupa que barre: rasgueo suave fila a fila (ruido que sube y baja 12 veces)."""
    t = _t(dur)
    x = bp(ruido(dur, seed), 1200, 5000) * (0.4 + 0.6 * np.abs(np.sin(np.pi * 12 * t / dur)))
    return norm(x, 0.35)


def clics_continuos(dur, seed=0, tasa=18):
    x = np.zeros(int(dur * SR) + SR // 8)
    r = _rng(seed)
    tt = 0.0
    while tt < dur:
        d = 0.01
        c = bp(ruido(d, seed + int(tt * 997)), 2200, 8000) * env(d, 0.0005, 0.002)
        i = int(tt * SR)
        x[i:i + len(c)] += c * r.uniform(0.3, 1)
        tt += r.exponential(1 / tasa)
    return norm(x, 0.35)


def bloque_cf(ev):
    C, D, E, F = (_plano(n) for n in ("plano_c", "plano_d", "plano_e", "plano_f"))
    if C:
        ev(C.T_INI, tramo(crepitar(C.tUnas - C.T_INI, 80)), 0.5)
        ev(C.tPista - 0.2, pop(81, 600, 900, 0.14), 0.4, pan=-0.4)
        ev(C.tCient - 0.1, carta(82), 0.4, pan=-0.5)
        ev(C.tCient + 0.2, carta(83), 0.4, pan=-0.3)
        ev(C.tMidieron - 0.4, interruptor(84), 0.4, pan=0.4)
        ev(C.tCada, disparos(C.tLinea - C.tCada, 1.5, 85), 0.6, pan=-0.3)          # casi callada
        ev(C.tLinea, disparos(C.tCierta - C.tLinea - 0.3, 5, 86), 0.6, pan=-0.3)    # suena a ratos al pasar la barra
        ev(C.tCierta - 0.3, disparos(C.tUnas - C.tCierta, 38, 87), 0.75, pan=-0.3)  # ¡tic tic tic!
        for k, ti in enumerate((C.tUnas, C.tEsquinas, C.tFormas, C.tPisos + 0.4)):
            ev(ti - 0.15, bloque(88 + k, 440 + 110 * k), 0.6)
        ev(C.tGolpe - 0.2, error(92), 0.35, pan=0.3)
        ev(C.tComplejo - 0.1, whoosh(0.6, 93, 300, 2500), 0.4, pan=-0.6)
        ev(C.tNobel - 0.2, fanfarria(94), 0.45, pan=0.5)
        ev(C.tIng, ding(95, 1568), 0.5, pan=-0.3)
        ev(C.tNumeros - 0.4, cascada(1.5, 96), 0.35)
    if D:
        ev(D.T_INI, tramo(maquina(D.tImagina - D.T_INI, 100, f=52), 0.6), 0.25)
        ev(D.tCalc - 0.15, lupa(101), 0.45, pan=-0.1)
        for k in range(3):
            ev(D.tRecibe + 0.2 * k, pop(102 + k, 900, 600, 0.1), 0.4, pan=-0.6)
            ev(D.tMultip - 0.1 + 0.15 * k, pop(105 + k, 700, 1000, 0.1), 0.35, pan=-0.3)
            ev(D.tPerilla + 0.25 * k, clic_perilla(108 + k), 0.6, pan=-0.3)
        ev(D.tSuma - 0.1, cascada(0.9, 111), 0.3)
        ev(D.tNivel, barrido_sube(112), 0.4, pan=0.5)
        ev(D.tEnciende - 0.1, ding(113), 0.65, pan=0.3)
        ev(D.tTodo - 0.2, destello(114), 0.4)
        ev(D.tImagina - 0.2, carta(115), 0.45)
        ev(D.tCuadrito - 0.1, cuadricula(116), 0.5, pan=-0.4)
        ev(D.tClaro - 0.2, clic_perilla(117, 6), 0.5, pan=0.1)
        ev(D.tOscuro - 0.2, clic_perilla(118, 3), 0.5, pan=0.2)
        ev(D.tBorde - 0.1, ding(119, 1760), 0.55, pan=0.5)
        ev(D.tDetector - 0.1, pop(120, 800, 1400, 0.14), 0.4)
        ev(D.tPasas - 0.1, tramo(rasgueo_barrido(D.tMapa + 0.8 - D.tPasas, 121), 0.2), 0.4)
        for k, ti in enumerate((D.tFiltro, D.tAcost, D.tDiag, D.tColor)):
            ev(ti - 0.15, carta(122 + k), 0.5, pan=-0.4 + 0.27 * k)
        ev(D.tIdea - 0.3, bloque(127, 660), 0.4)
        ev(D.tLeCun - 0.1, pop(128, 600, 1000, 0.14), 0.45, pan=-0.5)
        ev(D.tEscritos - 0.3, carta(129), 0.5, pan=0.2)
        for k in range(5):
            ev(D.tEscritos + 0.3 + 0.12 * k, bip(130 + k, 1320 + 80 * k, 0.04), 0.3, pan=0.2)
        ev(D.tCheques - 0.3, carta(136), 0.5, pan=0.3)
        ev(D.tCheques + 0.3, sello(137), 0.6, pan=0.4)
    if E:
        ev(E.T_INI, tramo(maquina(E.T_FIN - E.T_INI, 140, f=58), 1.0), 0.3)
        for k in range(4):
            ev(E.T_INI + 0.7 + 0.45 * k, golpe(141 + k), 0.4)
        ev(E.tTorre - 0.4, whoosh(1.2, 146, 150, 1500), 0.5)
        for k, ti in enumerate(E.T_PISO):
            ev(ti - 0.2, bloque(147 + k, 392 + 98 * k), 0.6, pan=-0.3)
            ev(ti - 0.3, lupa(151 + k), 0.3, pan=0.5)
        ev(E.tCientos - 0.2, cascada(1.4, 155), 0.35, pan=0.5)
        for k, ti in enumerate((E.tEsq, E.tCurv, E.tRay, E.tOjo, E.tOreja, E.tNariz, E.tBig, E.tCara, E.tRueda, E.tLetrero)):
            ev(ti - 0.15, ficha(156 + k, 523 * 2 ** ((k % 5) / 6)), 0.45, pan=0.5)
        ev(E.tMapas - 0.3, whoosh(0.8, 167, 400, 2000), 0.35, pan=-0.3)
        ev(E.tInv - 0.2, lupa(168), 0.45, pan=0.5)
        for k, ti in enumerate(E.tV):
            ev(ti - 0.2, bloque(169 + k, 523 + 131 * k), 0.5, pan=-0.2)
        ev(E.tNadie - 0.3, carta(173), 0.5, pan=-0.4)
        ev(E.tProg + 0.1, tachon(174), 0.6, pan=-0.4)
        ev(E.tSola - 0.2, destello(175), 0.55, pan=0.3)
        ev(E.tSola, ding(176, 1568), 0.4, pan=0.3)
        ev(E.tComo - 0.15, signo(177), 0.5)
    if F:
        ev(F.T_INI, tramo(maquina(F.T_FIN - F.T_INI, 180, f=50), 1.0), 0.25)
        ev(F.tPerillas - 0.3, tramo(clics_continuos(F.tEnsenas - F.tPerillas, 181), 0.3), 0.4)
        ev(F.tNada - 0.2, nubecita(182), 0.4, pan=-0.5)
        ev(F.tEnsenas - 0.2, carta(183), 0.5, pan=-0.3)
        ev(F.tTost - 0.4, procesa(184), 0.45, pan=0.4)
        ev(F.tMal - 0.1, error(185), 0.6, pan=0.3)
        ev(F.tMal - 0.05, tachon(186), 0.5, pan=0.4)
        ev(F.tMide - 0.2, barrido_sube(187), 0.4, pan=0.5)
        ev(F.tError - 0.3, pop(188, 400, 800, 0.15), 0.5)
        ev(F.tAtras - 0.2, caida(189, F.tCada + 0.5 - F.tAtras), 0.6)
        for k in range(4):
            ev(F.tCada + 0.2 * (3 - k), clic_perilla(190 + k), 0.55, pan=0.3)
        ev(F.tFrio - 0.1, ding(195, 2093), 0.4, pan=-0.5)
        ev(F.tCaliente - 0.1, whoosh(0.5, 196, 200, 1200), 0.45, pan=0.5)
        ev(F.tMillones - 0.2, tramo(clics_continuos(2.0, 197, 40), 0.3), 0.4)
        ev(F.tPerro - 0.4, procesa(198), 0.4, pan=0.4)
        ev(F.tMenosMal - 0.1, nubecita(199), 0.3, pan=0.4)
        ev(F.tGiran, clic_perilla(200, 6), 0.5, pan=-0.5)
        ev(F.tOtra2 + 0.6, clic_perilla(201, 6), 0.5, pan=-0.5)
        ev(F.tGato - 0.4, procesa(202), 0.4, pan=0.4)
        ev(F.tCasi - 0.1, destello(203), 0.5, pan=0.4)
        for k in range(10):
            ev(F.tRepite + 0.4 * k, whoosh(0.3, 204 + k, 800, 3500), 0.25, pan=-0.6 + 0.1 * k)
        ev(F.tSolitas - 0.5, clic_perilla(215, 8), 0.5, pan=0.4)
        for k, ti in enumerate(F.tDet):
            ev(ti - 0.15, ding(216 + k, 1046 + 262 * k), 0.4, pan=0.4)
        ev(F.tRetro - 0.1, fanfarria(220), 0.35)
        ev(F.tCulpa - 0.1, gotas(30, 1.6, 221), 0.55)
        ev(F.tProblema - 0.1, nubecita(222), 0.35, pan=-0.5)
        for k in range(12):
            ev(F.tProblema + 0.3 * k, carta(223 + k), 0.25, pan=-0.3 + 0.05 * k)
        ev(F.tAbsurda - 0.1, golpe(236), 0.6)
