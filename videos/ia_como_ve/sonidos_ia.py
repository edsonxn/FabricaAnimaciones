# -*- coding: utf-8 -*-
"""SFX sintetizados del video «¿Cómo VE una IA?» (bloques de sfx_proc.py) y sus pistas, ancladas a las mismas palabras que la
animación (importa las anclas de cada plano_*.py). Cada plano nuevo añade su bloque en `pistas()`."""
import importlib
import math

import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bip, bp, burbuja, destello, env, hp, lp, norm, osc, pop, ruido, signo, whoosh)


# ------------------------------------------------------------ camas
def cuarto(dur, seed=0):
    """Tono de cuarto: rumor grave + un reloj de pared lejano (tic cada segundo)."""
    t = _t(dur)
    x = lp(ruido(dur, seed), 260, 2) * 0.5
    for k in range(int(dur)):
        d = 0.025
        c = bp(ruido(d, seed + 10 + k), 2600 if k % 2 else 2000, 7000) * env(d, 0.001, 0.005)
        i = int((k + 0.3) * SR)
        x[i:i + len(c)] += c * 0.35
    return norm(x * (0.85 + 0.15 * np.sin(2 * np.pi * t / 7)), 0.3)


def maquina(dur, seed=0, f=55):
    """Por dentro de la cabeza de Kuri: zumbido eléctrico suave con un latido de datos y destellos de alta frecuencia."""
    t = _t(dur)
    x = osc(f, dur) * 0.35 + osc(f * 2, dur) * 0.18 + osc(f * 3.01, dur) * 0.06
    x *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.6 * t) ** 2
    x += bp(ruido(dur, seed), 3000, 9000) * 0.04 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t + seed))
    r = _rng(seed)
    for k in range(int(dur * 1.5)):
        d = 0.05
        b = osc(r.uniform(2400, 4200), d, "tri") * env(d, 0.002, 0.015)
        i = int(r.uniform(0, max(0.01, dur - d)) * SR)
        x[i:i + len(b)] += b * 0.12
    return norm(lp(x, 6000), 0.35)


def tramo(x, fade=0.4):
    n = len(x)
    f = min(int(fade * SR), n // 2)
    e = np.ones(n)
    e[:f] = np.linspace(0, 1, f)
    e[n - f:] = np.linspace(1, 0, f)
    return x * e


# ------------------------------------------------------------ golpes
def tecleo(dur, seed=0, vel=14.0):
    """Teclas de máquina de escribir/teclado: clics irregulares (el globo de Kuri que se escribe)."""
    x = np.zeros(int(dur * SR) + SR // 4)
    r = _rng(seed)
    tt, k = 0.0, 0
    while tt < dur:
        d = 0.03
        c = bp(ruido(d, seed + k), r.uniform(1800, 2600), 8000) * env(d, 0.0008, 0.006)
        c += osc(r.uniform(180, 240), d) * env(d, 0.001, 0.01) * 0.4
        i = int(tt * SR)
        x[i:i + len(c)] += c * r.uniform(0.6, 1)
        tt += r.uniform(0.6, 1.4) / vel
        k += 1
    return norm(x, 0.4)


def carta(seed=0):
    """Una tarjeta que gira en la mano: «fffp» de papel + golpecito."""
    d = 0.32
    x = bp(ruido(d, seed), 1500, 7000) * np.sin(np.pi * np.clip(_t(d) / d, 0, 1)) ** 2
    p = pop(seed + 1, 500, 300, 0.08)
    x[:len(p)] += p * 0.4
    return norm(x, 0.45)


def procesa(seed=0):
    """Kuri «piensa»: tres bips ascendentes cortísimos de computadora."""
    out = np.zeros(int(0.4 * SR))
    for k, f in enumerate((1568, 1976, 2349)):
        d = 0.045
        b = osc(f, d, "cuad") * env(d, 0.002, None)
        i = int(k * 0.07 * SR)
        out[i:i + len(b)] += lp(b, 5000)
    return norm(out, 0.35)


def lupa(seed=0):
    """Lupa que aparece: «tuiing» de vidrio (sinusoide que sube con brillo)."""
    d = 0.6
    x = osc(barrido(900, 2200, d), d) * env(d, 0.005, 0.2) + osc(barrido(1800, 4400, d), d) * env(d, 0.005, 0.08) * 0.3
    return norm(x, 0.4)


def nubecita(seed=0):
    """Nube triste: «wah» que cae."""
    d = 0.7
    f = barrido(520, 300, d)
    x = (osc(f, d, "saw") * 0.5 + osc(f * 1.5, d) * 0.3) * env(d, 0.03, 0.35)
    return norm(lp(x, 1800), 0.4)


def zoom_in(dur=1.2, seed=0):
    """Zambullida a la pantalla: whoosh que acelera + barrido tonal que sube."""
    t = _t(dur)
    w = whoosh(dur, seed, 200, 4000)
    s = osc(barrido(120, 900, dur), dur, "tri") * (t / dur) ** 2 * 0.4
    x = np.zeros(max(len(w), len(s)))
    x[:len(w)] += w
    x[:len(s)] += s
    return norm(x, 0.7)


def chispa(seed=0, f=None):
    """Una neurona que se enciende: chispazo eléctrico corto + tono."""
    r = _rng(seed)
    d = 0.18
    f = f or r.uniform(1100, 2200)
    x = hp(ruido(d, seed), 3000) * env(d, 0.0005, 0.02) * 0.6
    x += osc(f, d, "tri") * env(d, 0.002, 0.06) * 0.6
    return norm(x, 0.4)


def ristra_chispas(n, dur, seed=0):
    out = np.zeros(int(dur * SR) + SR // 2)
    r = _rng(seed)
    for k in range(n):
        c = chispa(seed + 1 + k)
        i = int(dur * (k / max(1, n - 1)) ** 1.3 * SR * r.uniform(0.9, 1.0))
        out[i:i + len(c)] += c * r.uniform(0.4, 1)
    return norm(out, 0.5)


def cuadricula(seed=0):
    """La rejilla de píxeles aparece: cascada de clics digitales afinados."""
    out = np.zeros(int(0.8 * SR))
    for k in range(12):
        d = 0.03
        b = osc(800 + 90 * k, d, "cuad") * env(d, 0.001, 0.01)
        i = int(k * 0.045 * SR)
        out[i:i + len(b)] += lp(b, 6000) * (0.5 + 0.5 * k / 11)
    return norm(out, 0.35)


def ficha(seed=0, f=880):
    """Un número que salta a su casilla: «plic» de marimba (sinusoide con armónico de madera)."""
    d = 0.35
    x = osc(f, d) * env(d, 0.002, 0.09) + osc(f * 3.9, d) * env(d, 0.001, 0.02) * 0.4
    return norm(x, 0.4)


def contador(dur, seed=0):
    """Números que corren: tictic digital que acelera (cuenta de 12 millones)."""
    x = np.zeros(int(dur * SR) + SR // 4)
    tt, k = 0.0, 0
    while tt < dur:
        d = 0.012
        b = osc(2600 + 400 * (k % 3), d, "cuad") * env(d, 0.0005, 0.003)
        i = int(tt * SR)
        x[i:i + len(b)] += lp(b, 7000)
        tt += 1 / (10 + 40 * tt / dur)
        k += 1
    return norm(x, 0.3)


def cascada(dur, seed=0):
    """Lluvia de números: muchos «plic» agudos y suaves, como granizo digital."""
    x = np.zeros(int(dur * SR) + SR // 4)
    r = _rng(seed)
    for k in range(int(dur * 26)):
        d = 0.025
        b = osc(r.uniform(1500, 3800), d) * env(d, 0.0005, 0.006)
        i = int(r.uniform(0, dur) * SR)
        x[i:i + len(b)] += b * r.uniform(0.2, 0.8)
    return norm(tramo(x, 0.3), 0.35)


def interruptor(seed=0):
    """Se apaga la luz: clic de apagador + caída grave."""
    d = 0.5
    x = bp(ruido(d, seed), 1200, 6000) * env(d, 0.0005, 0.008)
    x += osc(barrido(300, 70, d), d) * env(d, 0.005, 0.15) * 0.5
    return norm(x, 0.5)


def error(seed=0):
    """Zumbido de error: dos notas ásperas que bajan («bu-buuu»)."""
    out = np.zeros(int(0.8 * SR))
    for k, (f, d) in enumerate(((220, 0.16), (165, 0.4))):
        x = (osc(f, d, "cuad") * 0.5 + osc(f * 1.01, d, "saw") * 0.4) * env(d, 0.005, None)
        i = int(k * 0.2 * SR)
        out[i:i + len(x)] += lp(x, 2200)
    return norm(out, 0.45)


def tachon(seed=0):
    """Dos trazos de rotulador (el tache)."""
    out = np.zeros(int(0.6 * SR))
    for k in range(2):
        d = 0.18
        x = bp(ruido(d, seed + k), 1200, 6000) * np.sin(np.pi * _t(d) / d)
        i = int(k * 0.22 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.5)


def tiza(dur=0.9, seed=0):
    """Rotulador que escribe una regla en el pizarrón: fricción con pausas."""
    t = _t(dur)
    n = bp(ruido(dur, seed), 1800, 7000)
    golpes = (np.sin(2 * np.pi * 5.5 * t) > -0.2).astype(float)
    return norm(n * lp(golpes, 30, 1) * np.sin(np.pi * t / dur) ** 0.4, 0.4)


def sello(seed=0):
    d = 0.4
    x = osc(barrido(140, 55, d), d) * env(d, 0.002, 0.07)
    x += bp(ruido(d, seed), 800, 4000) * env(d, 0.001, 0.02) * 0.7
    return norm(x, 0.85)


def ronroneo(dur=1.6, seed=0):
    """El gato ronronea: pulsos graves de ~25 Hz sobre ruido filtrado."""
    t = _t(dur)
    am = (0.5 + 0.5 * np.sin(2 * np.pi * 24 * t)) ** 3
    x = lp(ruido(dur, seed), 400, 2) * am * (0.6 + 0.4 * np.sin(2 * np.pi * 0.6 * t) ** 2)
    return norm(tramo(x, 0.3), 0.4)


# ------------------------------------------------------------ pistas por plano
def _plano(n):
    try:
        return importlib.import_module(n)
    except ImportError:
        return None


def pistas():
    A, B = _plano("plano_a"), _plano("plano_b")
    from comun import TOTAL
    P = []

    def ev(t, x, v=1.0, pan=0.0):
        if t < TOTAL:
            P.append((t, x, v, pan))

    # ---------------- gancho (cuarto de la niña → dentro de Kuri)
    ev(0.0, tramo(cuarto(A.tCabeza + 0.6, 1)), 0.6)
    ev(A.tFoto - 0.55, carta(2), 0.6, pan=-0.3)
    ev(A.tMenos - 0.1, procesa(3), 0.5, pan=0.35)
    ev(A.tUnGato, tecleo(A.tTeclado - A.tUnGato, 4), 0.55, pan=0.35)
    ev(A.tUnGato + 0.3, ronroneo(1.8, 5), 0.35, pan=-0.3)
    for k, ti in enumerate((A.tDibujo, A.tRadio, A.tMeme)):
        ev(ti - 0.15, carta(10 + k), 0.6, pan=-0.3)
        ev(ti + 0.25, tecleo(0.6, 13 + k, 18), 0.4, pan=0.35)
        ev(ti + 0.85, destello(16 + k), 0.4, pan=0.4)
    ev(A.tOjos - 0.2, lupa(20), 0.55, pan=0.3)
    ev(A.tOjos + 0.1, cascada(1.0, 21), 0.35, pan=0.3)
    ev(A.tNunca - 0.1, nubecita(22), 0.4, pan=0.3)
    ev(A.tNi, signo(23), 0.4, pan=0.35)
    ev(A.tVer, signo(24), 0.35, pan=-0.3)
    ev(A.tComo - 0.1, pop(25, 700, 1300, 0.14), 0.5)
    ev(A.tCabeza - 0.5, zoom_in(1.2, 26), 0.75)
    ev(A.tCabeza + 0.2, tramo(maquina(B.T_INI - A.tCabeza + 0.6, 27), 0.6), 0.6)
    ev(A.tNeurona - 0.3, ristra_chispas(9, A.T_FIN - A.tNeurona + 0.3, 28), 0.5)

    # ---------------- píxeles
    ev(B.T_INI, tramo(maquina(B.T_FIN - B.T_INI, 30, f=49), 1.0), 0.35)
    ev(B.tAcercas - 0.2, whoosh(0.8, 31, 300, 2500), 0.55)
    ev(B.tCuadritos - 0.3, cuadricula(32), 0.55)
    ev(B.tPixeles - 0.1, pop(33, 900, 1500, 0.12), 0.5)
    ev(B.tCada - 0.1, whoosh(0.4, 34, 600, 3000), 0.4, pan=0.3)
    for k, (ti, f) in enumerate(((B.tRojo, 659), (B.tVerde, 784), (B.tAzul, 988))):
        ev(ti - 0.1, ficha(35 + k, f), 0.55, pan=0.4)
    ev(B.tCero - 0.1, ficha(38, 523), 0.4, pan=0.2)
    ev(B.tDosc - 0.1, ficha(39, 1319), 0.4, pan=0.5)
    ev(B.tDoce - 0.5, contador(B.tTreinta - B.tDoce + 0.5, 40), 0.4, pan=0.3)
    ev(B.tDoce - 0.05, sello(41), 0.55, pan=0.3)
    ev(B.tO, pop(42, 800, 500, 0.1), 0.45, pan=0.3)
    ev(B.tTreinta - 0.1, sello(43), 0.8, pan=0.3)
    ev(B.tTreinta + 0.2, cascada(B.tPara - B.tTreinta, 44), 0.45)
    ev(B.tTabla - 0.3, whoosh(1.0, 45, 200, 1800), 0.5)
    ev(B.tTabla, cascada(1.2, 46), 0.35, pan=-0.2)
    ev(B.tNada - 0.1, pop(47, 1000, 600, 0.12), 0.5, pan=0.5)
    ev(B.tMueve - 0.2, ronroneo(0.9, 48), 0.3, pan=-0.3)
    ev(B.tLuz - 0.2, interruptor(49), 0.7)
    ev(B.tCambian, cascada(1.0, 50), 0.4, pan=0.3)
    ev(B.tCambian, bip(51, 660, 0.08), 0.35, pan=0.3)
    ev(B.tMismo - 0.1, destello(52), 0.5)
    ev(B.tSi - 0.15, tiza(1.0, 53), 0.5, pan=0.2)
    ev(B.tTriang - 0.1, tiza(0.5, 54), 0.4, pan=0.4)
    for k in range(2):
        ev(B.tExplicas - 0.6 + 0.25 * k, carta(55 + k), 0.45, pan=-0.1 + 0.3 * k)
    ev(B.tOreja - 0.2, signo(57), 0.45, pan=0.4)
    ev(B.tNoFunc - 0.1, tachon(58), 0.7)
    ev(B.tNoFunc + 0.15, error(59), 0.5)
    from sonidos_ia_cf import bloque_cf
    bloque_cf(ev)
    from sonidos_ia_gk import bloque_gk
    bloque_gk(ev)
    return P
