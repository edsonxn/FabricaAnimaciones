# -*- coding: utf-8 -*-
"""SFX sintetizados de los planos g-k (ImageNet, parches, palabras, trucos, cierre), anclados a sus mismas palabras."""
import numpy as np

from sfx_proc import SR, _rng, _t, barrido, bip, bp, destello, env, lp, norm, osc, pop, ruido, signo, whoosh
from sonidos_ia import (_plano, carta, cascada, cuarto, error, ficha, lupa, maquina, nubecita, procesa, sello, tachon, tecleo,
                        tramo)
from sonidos_ia_cf import bloque, clic_perilla, clics_continuos, ding, fanfarria, golpe


def murmullo(dur, seed=0):
    """Multitud a lo lejos: muchas «voces» de ruido formante que suben y bajan."""
    t = _t(dur)
    x = np.zeros_like(t)
    r = _rng(seed)
    for k in range(6):
        f = r.uniform(350, 900)
        x += bp(ruido(dur, seed + k), f, f * 1.6) * (0.5 + 0.5 * np.sin(2 * np.pi * r.uniform(0.3, 0.9) * t + k))
    return norm(lp(x, 2500), 0.35)


def ventiladores(dur, seed=0):
    t = _t(dur)
    x = lp(ruido(dur, seed), 900, 2) * (0.8 + 0.2 * np.sin(2 * np.pi * 47 * t)) + osc(94, dur) * 0.08
    return norm(tramo(x, 0.3), 0.35)


def aplastar(seed=0):
    d = 0.7
    x = osc(barrido(160, 40, d), d) * env(d, 0.002, 0.18) + lp(ruido(d, seed), 1500) * env(d, 0.001, 0.06)
    x += osc(barrido(600, 200, d), d, "saw") * env(d, 0.005, 0.1) * 0.2
    return norm(x, 0.85)


def sube_grafica(dur, seed=0):
    """La línea de la gráfica que se dibuja: rotulador con tono que baja (el error baja)."""
    t = _t(dur)
    x = bp(ruido(dur, seed), 1500, 6000) * 0.5 + osc(barrido(900, 300, dur), dur, "tri") * 0.25
    return norm(x * np.sin(np.pi * t / dur) ** 0.5, 0.35)


def clac(seed=0):
    """Pieza de rompecabezas que encaja."""
    d = 0.08
    x = bp(ruido(d, seed), 1500, 6000) * env(d, 0.0005, 0.01) + osc(900, d) * env(d, 0.001, 0.012) * 0.4
    return norm(x, 0.45)


def hilo(seed=0, f0=600, f1=1400):
    d = 0.5
    x = osc(barrido(f0, f1, d), d) * env(d, 0.02, 0.2) * 0.6 + osc(barrido(f0 * 1.5, f1 * 1.5, d), d) * env(d, 0.02, 0.1) * 0.2
    return norm(x, 0.35)


def iman(seed=0, sube=True):
    d = 0.6
    x = osc(barrido(220, 880, d) if sube else barrido(880, 160, d), d, "tri") * env(d, 0.03, 0.25)
    return norm(lp(x, 3000), 0.4)


def estrellas(dur, seed=0):
    """Cielo del mapa: campanitas suaves al azar."""
    x = np.zeros(int(dur * SR) + SR)
    r = _rng(seed)
    for k in range(int(dur * 2.5)):
        f = r.choice([1568, 1760, 2093, 2349, 2637])
        d = 0.9
        b = osc(f, d) * env(d, 0.003, 0.3) * r.uniform(0.2, 0.6)
        i = int(r.uniform(0, dur) * SR)
        x[i:i + len(b)] += b
    return norm(tramo(x[:int(dur * SR)], 0.5), 0.3)


def viento_nieve(dur, seed=0):
    t = _t(dur)
    x = bp(ruido(dur, seed), 300, 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t) ** 2)
    return norm(tramo(x, 0.5), 0.35)


def estatica(dur, seed=0):
    x = bp(ruido(dur, seed), 2000, 9000) * (0.6 + 0.4 * (_rng(seed).random(int(dur * SR)) > 0.5))
    return norm(tramo(x, 0.05), 0.35)


def boton(seed=0):
    out = np.zeros(int(0.9 * SR))
    a = pop(seed, 500, 900, 0.1)
    out[:len(a)] += a
    for k, f in enumerate((1046, 1568)):
        d = 0.5
        b = osc(f, d) * env(d, 0.003, 0.18)
        i = int((0.15 + 0.12 * k) * SR)
        out[i:i + len(b)] += b * 0.6
    return norm(out, 0.5)


def acorde_final(seed=0):
    out = np.zeros(int(2.4 * SR))
    for k, f in enumerate((523, 659, 784, 1046, 1318)):
        d = 2.0 - 0.1 * k
        x = osc(f, d) * env(d, 0.004, 0.7) + osc(f * 2, d) * env(d, 0.003, 0.25) * 0.3
        i = int(k * 0.08 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.5)


def bloque_gk(ev):
    G, Hh, I, J, K = (_plano(n) for n in ("plano_g", "plano_h", "plano_i", "plano_j", "plano_k"))
    if G:
        ev(G.tNueve - 0.2, pop(300, 600, 900, 0.14), 0.4, pan=-0.5)
        ev(G.tNueve + 0.2, carta(301), 0.45, pan=-0.5)
        for k in range(12):
            ev(G.tFei + 0.6 + 0.3 * k, carta(302 + k), 0.25, pan=-0.1 + 0.06 * k)
        ev(G.tImageNet - 0.15, fanfarria(315), 0.35, pan=0.3)
        ev(G.tCatorce - 0.1, sello(316), 0.6, pan=-0.5)
        for k in range(12):
            ev(G.tEtiq - 0.2 + 0.08 * k, tecleo(0.15, 317 + k, 25), 0.25, pan=0.3)
        ev(G.tContrato - 0.2, tramo(murmullo(G.tConcurso - G.tContrato, 330)), 0.45)
        ev(G.tCuarenta - 0.1, sello(331), 0.55, pan=-0.4)
        ev(G.tCiento - 0.1, sello(332), 0.55, pan=0.4)
        for k, ti in enumerate((G.tGato, G.tVolcan, G.tTost)):
            ev(ti - 0.3, pop(333 + k, 800 + 100 * k, 1200, 0.1), 0.45, pan=-0.5 + 0.5 * k)
        ev(G.tConcurso - 0.3, destello(337), 0.5)
        ev(G.tConcurso - 0.2, fanfarria(338), 0.4)
        ev(G.tPrograma - 0.2, procesa(339), 0.4)
        ev(G.tDoce - 0.2, pop(340, 600, 900, 0.14), 0.4, pan=-0.6)
        ev(G.tDoce, tramo(maquina(G.tQuince - G.tDoce, 341, f=60), 0.5), 0.3)
        for k in range(8):
            ev(G.tDoce - 0.1 + 0.4 * k, bloque(342 + k, 330 + 40 * k), 0.4, pan=-0.6 + 0.1 * k)
        ev(G.tTarjetas - 0.3, tramo(ventiladores(G.tQuince - G.tTarjetas, 351), 0.3), 0.4, pan=0.5)
        ev(G.tSesenta - 0.2, clics_continuos(1.6, 352, 45), 0.45)
        ev(G.tQuince - 0.4, whoosh(0.6, 353, 200, 1500), 0.4, pan=-0.3)
        ev(G.tVeinti - 0.4, whoosh(0.6, 354, 200, 1500), 0.4, pan=0.3)
        ev(G.tAplasto - 0.2, aplastar(355), 0.8, pan=0.3)
        ev(G.tAplasto + 0.3, destello(356), 0.4, pan=0.3)
        ev(G.tCambio - 0.3, tramo(sube_grafica(G.tPersona + 0.3 - G.tCambio, 357), 0.3), 0.4)
        ev(G.tPersona - 0.2, ding(358, 1568), 0.55, pan=0.4)
        ev(G.tPersona - 0.1, destello(359), 0.5, pan=0.4)
    if Hh:
        ev(Hh.T_INI, tramo(cuarto(Hh.tCortan - Hh.T_INI, 400)), 0.4)
        ev(Hh.tDescriben - 0.6, tecleo(Hh.tPaso - Hh.tDescriben + 0.6, 401, 16), 0.45, pan=0.1)
        ev(Hh.tPaso - 0.2, pop(402, 700, 1200, 0.14), 0.4, pan=0.4)
        for k in range(14):
            ev(Hh.tCortan + 0.12 * k, clac(403 + k), 0.4, pan=-0.5 + 0.07 * k)
        ev(Hh.tDieci - 0.2, sello(420), 0.4, pan=0.5)
        ev(Hh.tLista - 0.3, whoosh(0.5, 421, 400, 2500), 0.45, pan=0.5)
        ev(Hh.tLista + 0.2, cascada(0.8, 422), 0.3, pan=0.5)
        for k, ti in enumerate((Hh.tPelo, Hh.tTecla, Hh.tOreja)):
            ev(ti - 0.2, ficha(423 + k, 784 + 196 * k), 0.45, pan=-0.2)
        ev(Hh.tPelo, clac(426), 0.5, pan=-0.1)
        ev(Hh.tAtencion - 0.2, ding(427, 1046), 0.45, pan=0.4)
        ev(Hh.tMira - 0.2, tramo(estrellas(2.0, 428), 0.3), 0.4)
        ev(Hh.tQuien - 0.3, procesa(429), 0.35, pan=0.4)
        for k, ti in enumerate((Hh.tOreja4, Hh.tBigote)):
            ev(ti - 0.2, hilo(430 + k), 0.5, pan=0.1)
        ev(Hh.tSomos - 0.2, destello(432), 0.5, pan=0.4)
        ev(Hh.tGato5 - 0.3, hilo(433, 400, 1000), 0.5, pan=-0.2)
        ev(Hh.tEscena - 0.2, ding(434, 1318), 0.45)
        ev(Hh.tTitulo - 0.3, carta(435), 0.5)
        ev(Hh.tVale - 0.2, destello(436), 0.45)
    if I:
        ev(I.T_INI, tramo(maquina(I.tVeintiuno - I.T_INI, 500, f=55), 0.5), 0.3)
        ev(I.tNumeros - 0.2, whoosh(0.6, 501, 300, 2000), 0.45)
        ev(I.tPalabras - 0.2, pop(502, 700, 1200, 0.14), 0.45, pan=0.4)
        ev(I.tVeintiuno - 0.2, pop(503, 600, 900, 0.14), 0.4, pan=-0.5)
        ev(I.tVeintiuno, tramo(cascada(I.tAcercar - I.tVeintiuno, 504), 0.5), 0.25)
        ev(I.tCuatro - 0.2, sello(505), 0.5)
        ev(I.tAcercar, iman(506, True), 0.5, pan=-0.3)
        ev(I.tAlejarla, iman(507, False), 0.5, pan=0.3)
        ev(I.tMapa - 0.5, tramo(estrellas(I.tDibujo - I.tMapa, 508), 1.0), 0.45)
        for k, ti in enumerate((I.tGato, I.tGatoP, I.tPerro, I.tVolcan)):
            ev(ti - 0.3, pop(509 + k, 900 + 150 * k, 1300, 0.12), 0.4, pan=-0.4 + 0.3 * k)
        ev(I.tVolcan + 0.3, whoosh(1.0, 513, 1500, 300), 0.4, pan=0.5)
        ev(I.tTraductor - 0.3, maquina(2.5, 514, f=70), 0.35)
        for k in range(6):
            ev(I.tTraductor + 0.3 * k + 1.0, ding(515 + k, 1568 + 100 * k), 0.25, pan=0.4)
        ev(I.tLee - 0.3, tecleo(1.2, 521, 18), 0.4)
        for k in range(5):
            ev(I.tContesta - 0.2 + 0.55 * k, pop(522 + k, 1000 + 80 * k, 1400, 0.08), 0.4, pan=-0.4 + 0.2 * k)
        for k, ti in enumerate((I.tDibujo, I.tRadio, I.tMeme)):
            ev(ti - 0.3, carta(527 + k), 0.5, pan=-0.5 + 0.5 * k)
        for k in range(5):
            ev(I.tMiles - 0.2 + 0.15 * k, carta(530 + k), 0.3)
    if J:
        ev(J.tOjo + 0.3, lupa(600), 0.45, pan=0.4)
        ev(J.tPatrones - 0.2, ficha(601, 880), 0.4, pan=0.4)
        ev(J.tEquiv - 0.2, nubecita(602), 0.35)
        ev(J.tExper, tramo(viento_nieve(J.tPanda - J.tExper, 603)), 0.35)
        for k in range(4):
            ev(J.tExper + 0.6 + 0.5 * k, carta(604 + k), 0.4, pan=-0.6)
        ev(J.tHusky + 0.6, carta(608), 0.5, pan=0.4)
        ev(J.tNieve - 0.4, procesa(609), 0.4, pan=0.4)
        ev(J.tNieve, error(610), 0.45, pan=0.4)
        ev(J.tAnimal - 0.2, tachon(611), 0.5, pan=0.4)
        ev(J.tManchitas - 0.3, estatica(0.6, 612), 0.4)
        ev(J.tJuro - 0.2, procesa(613), 0.4, pan=0.4)
        ev(J.tNoventa, sello(614), 0.6, pan=0.4)
        ev(J.tGibon - 0.2, signo(615), 0.4)
        ev(J.tCient - 0.3, tramo(maquina(J.T_FIN - J.tCient + 0.5, 616, f=58), 0.5), 0.3)
        ev(J.tCient, lupa(617), 0.45, pan=0.4)
        ev(J.tVerdad - 0.3, signo(618), 0.45)
    if K:
        ev(K.T_INI, tramo(cuarto(K.tPix - K.T_INI, 700)), 0.45)
        ev(K.tViaje - 0.3, destello(701), 0.4)
        ev(K.tPix - 0.4, whoosh(1.0, 702, 200, 2500), 0.5)
        ev(K.tPix, tramo(maquina(K.tNoVio - K.tPix, 703, f=55), 0.5), 0.3)
        for k, ti in enumerate((K.tPix, K.tFiltros, K.tPisos, K.tPerillas, K.tMapa)):
            ev(ti - 0.3, ding(704 + k, 1046 * 2 ** (k * 2 / 12)), 0.4, pan=-0.6 + 0.3 * k)
        ev(K.tPerillas, clic_perilla(710, 6), 0.4, pan=0.3)
        ev(K.tMapa, tramo(estrellas(3.0, 711), 0.4), 0.35, pan=0.5)
        ev(K.tPatron - 0.3, tramo(cascada(1.3, 712), 0.3), 0.35)
        ev(K.tLlamo - 0.6, carta(713), 0.5, pan=0.4)
        ev(K.tLlamo - 0.1, ding(714, 1318), 0.45, pan=0.4)
        ev(K.tCabeza - 0.6, whoosh(1.0, 715, 300, 2500), 0.45)
        ev(K.tSuscribete + 0.4, boton(716), 0.6, pan=0.3)
        ev(K.tPisosK - 0.4, golpe(717), 0.4)
        for k in range(6):
            ev(K.tPisosK + 0.3 * k, bloque(718 + k, 392 + 65 * k), 0.4, pan=-0.3)
        ev(K.tPisosK + 1.2, acorde_final(724), 0.55)
