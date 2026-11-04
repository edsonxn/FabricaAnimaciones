# -*- coding: utf-8 -*-
"""SFX sintetizados del Short de las arenas movedizas (bloques de sfx_proc.py) y sus pistas, ancladas a las mismas
palabras que la animación (importa las anclas de plano_a/b/c)."""
import math

import numpy as np

from sfx_proc import (SR, _rng, _t, barrido, bp, burbuja, destello, env, glup, hp, lp, norm, osc, pop, rafaga_burbujas,
                      ruido, whoosh)


def olas(dur, seed=0):
    """Rompientes suaves: ruido rosado que sube y baja cada ~5 s + siseo de espuma."""
    t = _t(dur)
    n = ruido(dur, seed)
    cuerpo = lp(n, 700, 2)
    espuma = bp(n, 2500, 8000)
    ciclo = np.clip(np.sin(2 * np.pi * t / 5.3 + seed) * 0.5 + 0.5, 0, 1) ** 2
    ciclo2 = np.clip(np.sin(2 * np.pi * t / 3.7 + 1.3 + seed) * 0.5 + 0.5, 0, 1) ** 3
    x = cuerpo * (0.25 + 0.6 * ciclo) + espuma * (0.08 + 0.3 * ciclo2)
    return norm(x, 0.4)


def gaviota(seed=0):
    """Graznido: dos «kiau» con tono que cae y armónicos ásperos."""
    out = np.zeros(int(0.9 * SR))
    r = _rng(seed)
    for k in range(2):
        d = r.uniform(0.22, 0.3)
        f = barrido(r.uniform(1500, 1750), r.uniform(900, 1050), d)
        x = (osc(f, d, "saw") * 0.4 + osc(f * 2, d) * 0.3) * env(d, 0.02, d * 0.5)
        x = bp(x, 700, 4000)
        i = int(k * 0.34 * SR)
        out[i:i + len(x)] += x * (1 - 0.3 * k)
    return norm(out, 0.5)


def paso_arena(seed=0):
    """Pisada en arena seca: crujido corto de granos."""
    d = 0.12
    x = bp(ruido(d, seed), 900, 5000) * env(d, 0.004, 0.03)
    return norm(x, 0.35)


def succion(seed=0, dur=1.1):
    """«Shluuurp»: barro que se traga algo (ruido grave con resonancia que baja + gorgoteo)."""
    t = _t(dur)
    n = ruido(dur, seed)
    out = np.zeros_like(n)
    for k in range(10):
        a, b = int(k * len(n) / 10), int((k + 1) * len(n) / 10)
        fc = 900 * (160 / 900) ** (k / 9)
        out[a:b] = bp(n, fc * 0.6, fc * 1.5, 2)[a:b]
    out *= np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.7
    r = _rng(seed)
    for k in range(6):
        b_ = burbuja(seed + 40 + k, r.uniform(1.6, 2.4)) * 0.6
        i = int(r.uniform(0.1, dur - 0.2) * SR)
        out[i:i + len(b_)] += b_
    return norm(lp(out, 2200), 0.8)


def salpicon(seed=0):
    d = 0.5
    x = bp(ruido(d, seed), 400, 3500) * env(d, 0.004, 0.09)
    x += osc(barrido(220, 90, d), d) * env(d, 0.003, 0.05) * 0.5
    return norm(x, 0.6)


def proyector(dur, seed=0):
    """Proyector de cine: traqueteo a 24 fps + zumbido del motor."""
    t = _t(dur)
    clic = np.zeros_like(t)
    per = int(SR / 24)
    k_ = lp(ruido(0.006, seed), 4000) * np.linspace(1, 0, int(0.006 * SR))
    for i in range(0, len(t) - len(k_), per):
        clic[i:i + len(k_)] += k_ * (0.7 + 0.3 * math.sin(i * 0.001))
    zum = osc(120, dur) * 0.08 + osc(240, dur) * 0.04
    return norm(clic * 0.9 + zum, 0.35)


def drama(seed=0):
    """«¡Tan-tan-taaan!» de película vieja: tres acordes de metales con trémolo."""
    out = np.zeros(int(2.0 * SR))
    for k, (raiz, d) in enumerate(((196, 0.22), (185, 0.22), (165, 1.2))):
        x = np.zeros(int(d * SR))
        for m in (1, 1.19, 1.5, 2):
            x += osc(raiz * m, d, "saw") / m
        x = lp(x, 2200) * env(d, 0.01, d * 0.6) * (1 + 0.25 * np.sin(2 * np.pi * 7 * _t(d)))
        i = int(k * 0.28 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.6)


def sello(seed=0):
    """Golpe de sello de goma: thump grave + palmada."""
    d = 0.4
    x = osc(barrido(140, 55, d), d) * env(d, 0.002, 0.07)
    x += bp(ruido(d, seed), 800, 4000) * env(d, 0.001, 0.02) * 0.7
    return norm(x, 0.85)


def rasgado(seed=0, dur=0.6):
    """Papel/película que se rasga: ruido granulado con chasquidos."""
    n = ruido(dur, seed)
    g = (_rng(seed + 1).random(len(n)) > 0.985).astype(float)
    x = bp(n, 1500, 7000) * (0.3 + 0.7 * lp(g, 200, 1) * 40) * env(dur, 0.01, dur * 0.4)
    return norm(x, 0.5)


def crujido_madera(seed=0, dur=0.7):
    """Balanza que se inclina: madera que cruje (pulsos irregulares filtrados)."""
    t = _t(dur)
    r = _rng(seed)
    x = np.zeros_like(t)
    i = 0
    while i < len(t) - 400:
        p = bp(ruido(0.008, seed + i), 300, 2500) * np.linspace(1, 0, int(0.008 * SR))
        x[i:i + len(p)] += p * r.uniform(0.4, 1)
        i += int(r.uniform(0.006, 0.03) * SR)
    return norm(x * np.sin(np.pi * t / dur), 0.45)


def clonc(seed=0):
    """Platillo que toca fondo: metal hueco."""
    d = 0.8
    x = sum(osc(f, d) * env(d, 0.001, 0.25 / (1 + j)) / (1 + j) for j, f in enumerate((410, 1090, 1730, 2480)))
    return norm(x, 0.6)


def granos(dur, seed=0):
    """Granos de arena que se aprietan: crujido denso que crece."""
    t = _t(dur)
    r = _rng(seed)
    x = np.zeros_like(t)
    for k in range(int(dur * 180)):
        i = int(r.uniform(0, dur - 0.01) * SR)
        p = bp(ruido(0.004, seed + k), 1500, 7000) * np.linspace(1, 0, int(0.004 * SR))
        x[i:i + len(p)] += p * r.uniform(0.2, 1) * (0.3 + 0.7 * i / len(t))
    return norm(x, 0.45)


def cemento(seed=0):
    """Fraguado: golpe sordo de piedra + crujido."""
    d = 0.6
    x = osc(barrido(90, 45, d), d) * env(d, 0.002, 0.12)
    x += lp(ruido(d, seed), 1200) * env(d, 0.002, 0.05) * 0.8
    return norm(x, 0.85)


def esfuerzo_cuerda(seed=0, dur=1.0):
    """Cuerda que se tensa: chirrido de fibras (fricción modulada)."""
    t = _t(dur)
    f = 180 + 60 * np.sin(2 * np.pi * 3 * t)
    x = osc(f, dur, "saw") * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 11 * t)))
    x = bp(x, 400, 2500) * np.sin(np.pi * t / dur) ** 0.5
    return norm(x, 0.4)


def bocina(seed=0):
    """Bocina de cochecito: «mec-mec»."""
    out = np.zeros(int(0.6 * SR))
    for k in range(2):
        d = 0.16
        x = (osc(415, d, "cuad") + osc(523, d, "cuad")) * env(d, 0.005, None)
        x = bp(x, 300, 3000)
        i = int(k * 0.22 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.55)


def tictac(dur, seed=0, vel=8.0):
    """Reloj acelerado: tic-tac cada vez más rápido."""
    x = np.zeros(int(dur * SR))
    tt, k = 0.0, 0
    while tt < dur - 0.05:
        d = 0.03
        c = bp(ruido(d, seed + k), 2500 if k % 2 else 1800, 8000) * env(d, 0.001, 0.006)
        i = int(tt * SR)
        x[i:i + len(c)] += c
        tt += 1 / (2 + vel * tt / dur * 3)
        k += 1
    return norm(x, 0.45)


def marea(dur, seed=0):
    """La marea que sube: oleaje que crece + rumor grave."""
    t = _t(dur)
    x = olas(dur, seed) * (0.4 + 0.9 * t / dur)
    x += lp(ruido(dur, seed + 5), 160, 3) * (t / dur) * 0.6
    return norm(x, 0.6)


def alarma_kuri(seed=0):
    out = np.zeros(int(0.9 * SR))
    for k in range(3):
        d = 0.12
        x = osc(1760 if k % 2 == 0 else 1320, d, "tri") * env(d, 0.003, None)
        i = int(k * 0.15 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.4)


def tachon(seed=0):
    """Dos trazos de rotulador."""
    out = np.zeros(int(0.6 * SR))
    for k in range(2):
        d = 0.18
        x = bp(ruido(d, seed + k), 1200, 6000) * np.sin(np.pi * _t(d) / d)
        i = int(k * 0.22 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.5)


def chirrido_flotador(seed=0):
    """Flotador de plástico: «cuic» de goma."""
    d = 0.25
    x = osc(barrido(700, 1100, d), d, "saw") * env(d, 0.01, None) * (0.6 + 0.4 * np.sin(2 * np.pi * 40 * _t(d)))
    return norm(bp(x, 500, 4000), 0.4)


def chapoteo(seed=0, dur=1.8):
    """Agua que se cuela entre los granos: borboteo suave."""
    out = rafaga_burbujas(14, seed, dur) * 0.6
    out[:int(dur * SR)] += bp(ruido(dur, seed), 300, 1500) * 0.15
    return norm(out, 0.5)


def plop(seed=0):
    """«¡PLOP!»: el pie sale (corcho + succión corta)."""
    a = pop(seed, 700, 260, 0.18)
    b = succion(seed + 3, 0.35) * 0.6
    out = np.zeros(int(0.5 * SR))
    out[:len(b)] += b
    i = int(0.25 * SR)
    out[i:i + len(a)] += a
    return norm(out, 0.8)


def campana_final(seed=0):
    """Acorde de cierre en celesta: arpegio mayor."""
    out = np.zeros(int(2.0 * SR))
    for k, f in enumerate((784, 988, 1175, 1568)):
        d = 1.6 - 0.1 * k
        x = osc(f, d) * env(d, 0.003, 0.5) + osc(f * 2, d) * env(d, 0.003, 0.2) * 0.3
        i = int(k * 0.09 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.5)


def tramo(x, fade=0.4):
    """Fundido de entrada y salida para camas largas."""
    n = len(x)
    f = int(fade * SR)
    e = np.ones(n)
    e[:f] = np.linspace(0, 1, f)
    e[-f:] = np.linspace(1, 0, f)
    return x * e


def pistas():
    import plano_a as A
    import plano_b as B
    import plano_c as C
    from comun import TOTAL
    P = []

    def ev(t, x, v=1.0, pan=0.0):
        P.append((t, x, v, pan))

    # camas: olas en la playa, proyector en el cine, rumor bajo en los cortes
    ev(0.0, tramo(olas(A.T_CINE + 0.5, 1)), 0.55)
    ev(A.T_CINE, tramo(proyector(A.T_BAL - A.T_CINE + 0.4, 2)), 0.45)
    ev(A.T_CORTE, tramo(lp(ruido(B.T_PLAYA - A.T_CORTE, 3), 200, 3) * 0.3), 0.6)
    ev(B.T_PLAYA, tramo(olas(B.tSube - B.T_PLAYA, 4)), 0.5)
    ev(B.tSube - 0.3, tramo(marea(B.T1(B.MA) - B.tSube + 0.9, 5), 0.3), 0.8)
    ev(C.T_INI, tramo(olas(C.T_CORTE - C.T_INI + 0.5, 6)), 0.5)
    ev(C.T_SALE, tramo(olas(TOTAL - C.T_SALE, 7), 1.0), 0.45)
    for k, tg in enumerate((1.2, 37.0, 50.5, 66.0)):
        ev(tg, gaviota(10 + k), 0.35, pan=0.6 - 0.4 * k)
    # gancho
    for k in range(5):
        ev(0.6 + k * 0.45, paso_arena(20 + k), 0.6, pan=-0.1 + 0.05 * (k % 2))
    ev(A.tSuelo - 0.05, succion(30, 1.3), 1.0)
    ev(A.tTraga, salpicon(31), 0.8)
    ev(A.tSuelo, pop(32, 1400, 900, 0.1), 0.5, pan=0.4)           # «!» de Kuri
    ev(A.tTraga + 0.05, pop(33, 1200, 700, 0.12), 0.45, pan=-0.3)
    ev(A.tArenas - 0.05, whoosh(0.35, 34, 400, 3000), 0.6)
    ev(A.tMoved - 0.05, whoosh(0.35, 35, 500, 3500), 0.6)
    # el cine
    for k in range(35):
        if k % 3 == 0:
            ev(A.tUna + k * 0.035, pop(40 + k, 1100 + 20 * k, 600, 0.07), 0.25, pan=(k % 5 - 2) * 0.2)
    ev(A.tPelis + 0.3, destello(41), 0.5)
    ev(A.tSiempre - 0.3, drama(42), 0.55)
    ev(A.tHund, succion(43, 1.6), 0.6)
    ev(A.tCabeza + 0.1, glup(44), 0.6)
    ev(A.tMint - 0.05, sello(45), 1.0)
    ev(A.T_BAL - 0.1, rasgado(46), 0.6)
    # balanza
    ev(A.tArena2 - 0.1, pop(47, 600, 300, 0.15), 0.5, pan=0.4)
    ev(A.tPesa, crujido_madera(48), 0.7)
    ev(A.tDoble + 0.2, clonc(49), 0.6, pan=0.4)
    # corte: hundirse y flotar
    ev(A.tHundes - 0.1, succion(50, 1.4), 0.7)
    ev(A.tFlotas - 0.1, destello(51), 0.5)
    ev(A.tFlotas, chirrido_flotador(52), 0.3)
    # trampa
    ev(B.tPataleas - 0.1, tramo(rafaga_burbujas(10, 53, 1.5), 0.1), 0.5)
    ev(B.tPataleas + 0.4, tramo(granos(B.tCemento - B.tPataleas, 54), 0.2), 0.8)
    ev(B.tCemento - 0.1, cemento(55), 1.0)
    ev(B.tTiron - 0.15, esfuerzo_cuerda(56, 1.3), 0.8, pan=0.3)
    ev(B.tLevantar - 0.2, pop(57, 900, 500, 0.12), 0.4, pan=-0.4)
    ev(B.tCoche, bocina(58), 0.6, pan=-0.4)
    # marea
    ev(B.tQuedarte - 0.2, tictac(B.tSube - B.tQuedarte + 0.2, 59), 0.6, pan=-0.5)
    ev(B.tSube + 0.2, alarma_kuri(60), 0.5, pan=0.4)
    ev(B.tMarea - 0.1, whoosh(0.4, 61, 300, 2500), 0.6)
    # cierre
    ev(C.tNo - 0.05, tachon(62), 0.7)
    ev(C.tEchate, whoosh(0.8, 63, 200, 1200), 0.4)
    ev(C.tFlotaras - 0.2, pop(64, 800, 1400, 0.12), 0.4, pan=-0.4)
    ev(C.tFlotaras + 0.2, chirrido_flotador(65), 0.4, pan=-0.4)
    ev(C.tMueve, tramo(lp(ruido(C.T_SALE - C.tMueve, 66), 220, 3) * 0.3), 0.6)
    ev(C.tEntre - 0.2, chapoteo(67, 1.8), 0.8)
    ev(C.tPoco, succion(68, 1.6), 0.5)
    ev(C.tSuelta - 0.1, plop(69), 1.0)
    ev(C.T_SENTADO + 0.2, destello(70), 0.35)
    ev(C.tMint + 0.35, glup(71), 0.6, pan=0.3)
    ev(C.tNoP - 0.1, pop(72, 1000, 1500, 0.1), 0.4)
    ev(C.tPanico - 0.1, campana_final(73), 0.6)
    ev(C.tPanico + 1.0, rafaga_burbujas(6, 74, 1.2), 0.4, pan=0.3)
    return P
