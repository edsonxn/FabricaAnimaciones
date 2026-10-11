# -*- coding: utf-8 -*-
"""Efectos de sonido del estilo NOIR (videos/ia_noir): todo sintetizado. Ambientes estéreo (lluvia, multitud, cafetería, autopista,
zumbidos), mecánica (máquina de escribir, tambor de revólver, servos, pinza, engranajes, imprenta, aplanadora), papel y golpes
(sello, periódico, fichas, dardo) y atmósferas (grave inquietante, sombra que crece, subida, teremín). Se importan al final de sfx.py.
Los de duración variable aceptan dur=…; los cortos, tono=…"""
import math

import numpy as np

from sinte import SR, bp, butter_hp, butter_lp, hp, lp, mtof, ruido, saturar, sierra


def _t(d):
    return np.arange(int(max(0.01, d) * SR)) / SR


def _nrm(x, pico=0.9):
    return x / (np.abs(x).max() + 1e-9) * pico


def _env(d, caida, ataque=0.002):
    t = _t(d)
    return np.minimum(1, t / ataque) * np.exp(-t / caida)


def _fade(x, ent=0.3, sal=0.5):
    n = x.shape[-1]
    e = np.ones(n)
    a, b = min(n // 2, int(ent * SR)), min(n // 2, int(sal * SR))
    if a:
        e[:a] = np.linspace(0, 1, a)
    if b:
        e[n - b:] = np.linspace(1, 0, b)
    return x * e


def _st(l, r):
    return np.stack([l, r])


def _granos(d, n, f_fn, seed, largo=0.004, amp=1.0):
    """Lluvia de impulsos filtrados (gotas, teclas, chisporroteo)."""
    out = np.zeros(int(d * SR))
    r = np.random.default_rng(seed)
    L = int(largo * SR)
    t = np.arange(L) / SR
    for _ in range(int(n)):
        i = int(r.uniform(0, max(1, len(out) - L)))
        f = f_fn(r)
        g = np.sin(2 * np.pi * f * t) * np.exp(-t / (largo / 4)) * r.uniform(0.3, 1.0) * amp
        out[i:i + L] += g
    return out


def _ajusta(x, n):
    return x[:n] if len(x) >= n else np.pad(x, (0, n - len(x)))


def _mete(x, y, i, k=1.0):
    """Suma y en x desde la muestra i (recortando en el borde)."""
    if i >= len(x):
        return
    n = min(len(y), len(x) - i)
    x[i:i + n] += y[:n] * k


def _golpe(f0, f1, d, caida, ruido_k=0.4, seed=0, fc=2500):
    t = _t(d)
    f = f1 + (f0 - f1) * np.exp(-t * 30)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / caida)
    x += butter_lp(ruido(len(t), seed), fc, 2) * np.exp(-t / (caida * 0.3)) * ruido_k
    return x


# ================================================================== ambientes
def s_lluvia_amb(dur=10.0, **k):
    n = int(dur * SR)
    l = butter_lp(butter_hp(ruido(n, 1), 300, 2), 7000, 2)
    r = butter_lp(butter_hp(ruido(n, 2), 300, 2), 7000, 2)
    gotas_l = _granos(dur, dur * 90, lambda q: q.uniform(1500, 5000), 3, 0.006)
    gotas_r = _granos(dur, dur * 90, lambda q: q.uniform(1500, 5000), 4, 0.006)
    mod = 1 + 0.15 * np.sin(2 * np.pi * 0.13 * np.arange(n) / SR)
    rum = butter_lp(ruido(n, 5), 180, 2) * 1.5
    return _nrm(_fade(_st(l * mod * 0.5 + gotas_l * 0.25 + rum, r * mod * 0.5 + gotas_r * 0.25 + rum), 1.0, 1.0), 0.8)


def s_lluvia_lejana(dur=8.0, **k):
    x = s_lluvia_amb(dur)
    return _nrm(np.stack([butter_lp(x[0], 1800, 2), butter_lp(x[1], 1800, 2)]), 0.6)


def s_gotas_vidrio(dur=3.0, **k):
    x = _granos(dur, dur * 14, lambda q: q.uniform(900, 2600), 11, 0.03)
    return _nrm(_fade(x, 0.1, 0.5), 0.7)


def s_trueno_lejano(dur=4.0, **k):
    t = _t(dur)
    x = butter_lp(ruido(len(t), 21), 220, 2) * (np.exp(-t * 1.2) * (1 + 0.6 * np.sin(2 * np.pi * 3 * t) ** 2))
    return _nrm(x)


def s_multitud(dur=6.0, **k):
    n = int(dur * SR)
    voces = np.zeros(n)
    r = np.random.default_rng(31)
    t = np.arange(n) / SR
    for v in range(14):                                   # murmullo: ruido en formantes que se abren y cierran
        f1 = r.uniform(400, 900)
        f2 = r.uniform(1100, 2200)
        sil = (np.sin(2 * np.pi * r.uniform(2.5, 5.0) * t + r.uniform(0, 6)) > -0.2).astype(float)
        sil = butter_lp(sil, 12, 1)
        x = bp(ruido(n, 40 + v), f1, 4) + 0.6 * bp(ruido(n, 60 + v), f2, 5)
        voces += x * sil * r.uniform(0.5, 1.0)
    pasos = _granos(dur, dur * 6, lambda q: q.uniform(120, 260), 33, 0.04)
    l = voces + pasos * 0.5 + s_lluvia_amb(dur)[0] * 0.4
    return _nrm(_fade(_st(l, np.roll(l, 3000)), 0.4, 0.6), 0.8)


def s_cafeteria_amb(dur=8.0, **k):
    x = s_multitud(dur) * 0.5
    t = _t(dur)
    hum = (np.sin(2 * np.pi * 60 * t) * 0.3 + np.sin(2 * np.pi * 120 * t) * 0.15)
    cl = _granos(dur, dur * 1.5, lambda q: q.uniform(2500, 4200), 41, 0.12, 0.6)
    return _nrm(_fade(x + (hum * 0.15 + cl)[None, :], 0.3, 0.5), 0.7)


def s_pajaros_ciudad(dur=8.0, **k):
    out = np.zeros(int(dur * SR))
    r = np.random.default_rng(51)
    for _ in range(int(dur * 1.5)):
        i = int(r.uniform(0, max(1, len(out) - SR // 3)))
        d = r.uniform(0.06, 0.18)
        t = _t(d)
        f = r.uniform(2800, 4200) * (1 + 0.3 * np.sin(2 * np.pi * r.uniform(15, 30) * t))
        out[i:i + len(t)] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) * 0.5
    return _nrm(_fade(out, 1.0, 1.0), 0.5)


def s_autopista(dur=5.0, **k):
    n = int(dur * SR)
    t = np.arange(n) / SR
    base = butter_lp(ruido(n, 61), 500, 2) * 0.8
    pas = np.zeros(n)
    for j, c in enumerate(np.arange(0.4, dur, 1.1)):
        g = np.exp(-((t - c) / 0.45) ** 2)
        pas += butter_lp(ruido(n, 62 + j), 900, 2) * g
    return _nrm(_fade(_st(base + pas, base + np.roll(pas, 4000)), 0.5, 0.6), 0.7)


def s_auto_pasa(dur=2.5, **k):
    t = _t(dur)
    c = dur * 0.45
    g = np.exp(-((t - c) / (dur * 0.22)) ** 2)
    f = 90 * (1 + 0.12 * np.tanh((c - t) * 4))                   # efecto Doppler
    motor = saturar(sierra(f) * 0.6, 2.0)
    agua = butter_hp(ruido(len(t), 71), 1500, 2) * 0.8
    x = (motor * 0.6 + agua) * g
    pan = np.clip((t - c) / (dur * 0.4), -1, 1)
    return _nrm(_st(x * (1 - pan) / 2 + x * 0.3, x * (1 + pan) / 2 + x * 0.3), 0.85)


def s_motores_carrera(dur=4.0, **k):
    t = _t(dur)
    x = np.zeros(len(t))
    for j, f0 in enumerate((70, 84, 96)):
        f = f0 * (1 + 0.25 * t / dur) * (1 + 0.04 * np.sin(2 * np.pi * (5 + j) * t))
        x += saturar(sierra(f) * 0.7, 2.5) * (0.8 - 0.15 * j)
    x = butter_lp(x, 2500, 2) + butter_hp(ruido(len(t), 81), 2000, 2) * 0.25
    return _nrm(_fade(_st(x, np.roll(x, 900)), 0.2, 0.4), 0.85)


def s_motor_acelera(dur=3.0, **k):
    t = _t(dur)
    f = 60 + 200 * (t / dur) ** 1.4
    x = butter_lp(saturar(sierra(f) * 0.8, 3.0), 3000, 2)
    return _nrm(_fade(x, 0.1, 0.3), 0.85)


def s_zumbido_lampara(dur=8.0, **k):
    t = _t(dur)
    x = np.sin(2 * np.pi * 60 * t) * 0.5 + np.sin(2 * np.pi * 120 * t) * 0.35 + np.sin(2 * np.pi * 180 * t) * 0.15
    x += butter_hp(ruido(len(t), 91), 4000, 2) * 0.03 * (1 + np.sin(2 * np.pi * 0.7 * t))
    return _nrm(_fade(x, 0.5, 0.8), 0.5)


def s_zumbido_servidores(dur=4.0, **k):
    t = _t(dur)
    x = butter_lp(ruido(len(t), 101), 900, 2) * 0.6 + np.sin(2 * np.pi * 240 * t) * 0.1 + np.sin(2 * np.pi * 3100 * t) * 0.02
    return _nrm(_fade(x, 0.3, 0.3), 0.6)


def s_zumbido_foco(dur=3.0, **k):
    t = _t(dur)
    x = np.sin(2 * np.pi * 120 * t) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t)) + butter_hp(ruido(len(t), 111), 5000, 2) * 0.05
    return _nrm(_fade(x, 0.2, 0.4), 0.5)


def s_datos(dur=3.0, **k):
    t = _t(dur)
    bits = (np.sin(2 * np.pi * 37 * t) > 0) * np.sin(2 * np.pi * 1800 * t) * 0.3
    x = bits + _granos(dur, dur * 60, lambda q: q.choice([1200, 1800, 2400, 3600]), 121, 0.02, 0.5)
    return _nrm(_fade(butter_lp(x, 6000, 2), 0.1, 0.2), 0.6)


def s_telar(dur=3.0, **k):
    x = np.zeros(int(dur * SR))
    for j, c in enumerate(np.arange(0, dur, 0.25)):
        i = int(c * SR)
        y = _golpe(400, 200, 0.12, 0.03, 0.6, 130 + j, 3000)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.6)


def s_imprenta(dur=6.0, **k):
    x = np.zeros(int(dur * SR))
    for j, c in enumerate(np.arange(0, dur, 0.32)):
        i = int(c * SR)
        _mete(x, _golpe(180, 70, 0.3, 0.08, 0.9, 140 + j, 1800), i)
        _mete(x, _golpe(1200, 800, 0.08, 0.02, 0.4, 160 + j, 6000), i, 0.4)
    t = _t(dur)
    x += butter_lp(ruido(len(t), 141), 600, 2) * 0.3
    return _nrm(_fade(x, 0.2, 0.4), 0.85)


def s_obra(dur=5.0, **k):
    x = np.zeros(int(dur * SR))
    r = np.random.default_rng(151)
    for j in range(int(dur * 3)):
        i = int(r.uniform(0, len(x) - SR // 2))
        f = r.uniform(400, 1500)
        t = _t(0.6)
        y = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t * 8) * r.uniform(0.3, 1.0)
        _mete(x, y, i)
    t = _t(dur)
    x += _ajusta(butter_lp(ruido(len(t), 152), 300, 2) * 0.4 + saturar(np.sin(2 * np.pi * np.cumsum(55 + 3 * np.sin(2 * np.pi * 0.3 * t)) / SR) * 0.3, 2) * 0.2, len(x))
    return _nrm(_fade(x, 0.4, 0.5), 0.8)


def s_aplanadora(dur=6.0, **k):
    t = _t(dur)
    puf = (np.sin(2 * np.pi * 2.2 * t) > 0.6).astype(float)
    puf = butter_lp(puf, 30, 1)
    x = butter_lp(ruido(len(t), 161), 700, 2) * puf * 1.2 + saturar(sierra(42) * 0.6, 2) * 0.4
    x += butter_lp(ruido(len(t), 162), 120, 2) * 0.8                 # el rodillo aplastando
    return _nrm(_fade(x, 0.3, 0.5), 0.85)


def s_hormigas(dur=2.0, **k):
    x = _granos(dur, dur * 400, lambda q: q.uniform(4000, 8000), 171, 0.002, 0.4)
    return _nrm(_fade(x, 0.1, 0.3), 0.4)


def s_engranajes(dur=5.0, **k):
    x = np.zeros(int(dur * SR))
    c, j = 0.0, 0
    while c < dur:
        i = int(c * SR)
        y = _golpe(2400, 1800, 0.05, 0.012, 0.3, 180 + j, 8000)
        x[i:i + len(y)] += y[:len(x) - i]
        c += 0.18 * (1 - 0.8 * c / dur)                            # se acelera
        j += 1
    t = _t(dur)
    x += saturar(sierra(40 + 40 * t / dur) * 0.3, 2) * 0.3
    return _nrm(_fade(x, 0.2, 0.3), 0.8)


def s_reloj_pared(dur=6.0, **k):
    x = np.zeros(int(dur * SR))
    for j, c in enumerate(np.arange(0, dur, 0.5)):
        i = int(c * SR)
        y = _golpe(1800 if j % 2 else 1500, 1200, 0.07, 0.015, 0.4, 190 + j, 7000)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.5)


def s_caja_musica(dur=6.0, **k):
    """Caja de música desafinada (una melodía de cuna que se va frenando)."""
    notas = [72, 76, 79, 76, 74, 71, 72, 67, 69, 72, 76, 74]
    x = np.zeros(int(dur * SR))
    c = 0.0
    j = 0
    while c < dur - 0.3:
        f = mtof(notas[j % len(notas)]) * (1 - 0.01 * j)
        t = _t(1.2)
        y = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 3.01 * t)) * np.exp(-t * 3.5)
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
        c += 0.34 * (1 + 0.6 * c / dur)
        j += 1
    return _nrm(_fade(x, 0.05, 0.6), 0.6)


def s_teremin(dur=1.6, **k):
    t = _t(dur)
    f = 600 + 250 * np.sin(2 * np.pi * 0.7 * t) + 15 * np.sin(2 * np.pi * 6 * t)
    return _nrm(_fade(np.sin(2 * np.pi * np.cumsum(f) / SR), 0.2, 0.4), 0.6)


# ================================================================== máquina de escribir y papel
def s_tecla(tono=1.0, **k):
    d = 0.09
    t = _t(d)
    clack = butter_hp(ruido(len(t), int(tono * 1000) % 97), 1800, 2) * np.exp(-t * 120)
    body = np.sin(2 * np.pi * 900 * tono * t) * np.exp(-t * 80) * 0.6 + np.sin(2 * np.pi * 220 * t) * np.exp(-t * 50) * 0.5
    return _nrm(clack + body, 0.8)


def s_tecleo_rapido(dur=1.0, **k):
    x = np.zeros(int(dur * SR))
    r = np.random.default_rng(201)
    c = 0.0
    while c < dur - 0.1:
        y = s_tecla(r.uniform(0.9, 1.15))
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i] * r.uniform(0.6, 1.0)
        c += r.uniform(0.045, 0.11)
    return _nrm(x, 0.8)


def s_carro_maquina(**k):
    d = 0.7
    t = _t(d)
    ding = np.sin(2 * np.pi * 2900 * t) * np.exp(-t * 6) * 0.6
    ras = butter_hp(ruido(len(t), 211), 1200, 2) * np.clip(1 - np.abs(t - 0.35) / 0.25, 0, 1) * 0.5
    return _nrm(ding + ras, 0.8)


def s_papel_viento(dur=3.0, **k):
    t = _t(dur)
    x = bp(ruido(len(t), 221), 2500, 1.5) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 3.3 * t))) + butter_lp(ruido(len(t), 222), 400, 2) * 0.8
    return _nrm(_fade(x, 0.4, 0.4), 0.7)


def s_papel_atrapa(**k):
    d = 0.3
    t = _t(d)
    return _nrm(bp(ruido(len(t), 231), 3000, 1) * np.exp(-t * 20) + bp(ruido(len(t), 232), 900, 2) * np.exp(-t * 30), 0.8)


def s_papel_arranca(**k):
    d = 0.8
    t = _t(d)
    x = bp(ruido(len(t), 241), 3500, 0.8) * (np.random.default_rng(1).random(len(t)) > 0.3) * np.clip(1 - t / d, 0, 1)
    return _nrm(x, 0.85)


def s_paginas(dur=3.0, **k):
    x = np.zeros(int(dur * SR))
    for j, c in enumerate(np.arange(0, dur - 0.2, 0.09)):
        y = s_papel_atrapa() * 0.6
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.7)


def s_sobre_desliza(dur=0.8, **k):
    t = _t(dur)
    return _nrm(_fade(bp(ruido(len(t), 251), 2000, 1) * 0.8 + butter_lp(ruido(len(t), 252), 300, 2), 0.05, 0.3), 0.7)


def s_fotos(**k):
    x = np.zeros(int(0.8 * SR))
    for j in range(3):
        y = s_papel_atrapa() * 0.7
        i = int(j * 0.15 * SR)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.7)


def s_periodico_gira(**k):
    d = 1.0
    t = _t(d)
    x = bp(ruido(len(t), 261), 1500 + 1500 * t, 1.2) * np.sin(np.pi * t / d) ** 2
    golpe = _golpe(160, 60, d, 0.08, 0.6, 262)
    golpe[: int(0.85 * SR)] = 0
    return _nrm(x + np.roll(golpe, 0) * 0.0 + np.pad(_golpe(160, 60, 0.15, 0.06, 0.7, 263), (int(0.85 * SR), 0))[:len(t)], 0.85)


def s_periodico_golpe(**k):
    d = 0.5
    return _nrm(_golpe(140, 50, d, 0.1, 1.0, 271, 2500), 0.95)


def s_tachon(**k):
    d = 0.45
    t = _t(d)
    return _nrm(bp(ruido(len(t), 281), 1800, 2) * np.sin(np.pi * t / d), 0.75)


def s_pluma(**k):
    d = 0.35
    t = _t(d)
    return _nrm(bp(ruido(len(t), 291), 4500, 3) * np.sin(np.pi * t / d) * (1 + 0.5 * np.sin(2 * np.pi * 18 * t)), 0.5)


def s_lapiz(dur=1.4, **k):
    t = _t(dur)
    x = bp(ruido(len(t), 301), 3500, 2) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 4 * t)))
    return _nrm(_fade(x, 0.05, 0.2), 0.55)


def s_sello_golpe(**k):
    d = 0.6
    t = _t(d)
    x = _golpe(130, 55, d, 0.12, 1.0, 311, 2200) + butter_hp(ruido(len(t), 312), 2500, 2) * np.exp(-t * 60) * 0.5
    return _nrm(saturar(x, 1.4), 0.95)


def s_chincheta(**k):
    return _nrm(_golpe(2600, 1800, 0.12, 0.02, 0.3, 321, 8000), 0.6)


def s_hilo_tenso(**k):
    d = 0.5
    t = _t(d)
    f = 300 + 500 * t
    return _nrm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * 0.7 + bp(ruido(len(t), 331), 2000, 3) * np.exp(-t * 10) * 0.3, 0.5)


# ================================================================== mecánica y armas
def s_tambor_gira(dur=1.5, **k):
    x = np.zeros(int(dur * SR))
    c, j = 0.0, 0
    while c < dur:
        y = _golpe(3200, 2400, 0.04, 0.008, 0.5, 340 + j, 9000)
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
        c += 0.03 + 0.25 * (c / dur) ** 2                       # frena
        j += 1
    return _nrm(x, 0.8)


def s_tambor_click(**k):
    d = 0.5
    t = _t(d)
    x = _ajusta(_golpe(2200, 1500, 0.08, 0.015, 0.6, 351, 9000), len(t)) + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 8) * 0.5
    return _nrm(x, 0.95)


def s_revolver_desliza(dur=1.2, **k):
    t = _t(dur)
    x = bp(ruido(len(t), 361), 900, 1.5) * np.clip(1 - t / dur, 0, 1) * 0.8 + _golpe(800, 500, dur, 0.05, 0.2, 362) * 0.4
    return _nrm(x, 0.7)


def s_servo(dur=1.2, **k):
    t = _t(dur)
    f = 900 + 300 * np.sin(np.pi * t / dur)
    x = sierra(f) * 0.25 + np.sin(2 * np.pi * f * 0.5 * t) * 0.4
    return _nrm(_fade(butter_lp(x, 3000, 2) * (0.7 + 0.3 * np.sin(2 * np.pi * 30 * t)), 0.05, 0.15), 0.6)


def s_pinza(**k):
    d = 0.4
    t = _t(d)
    x = _golpe(1500, 900, d, 0.05, 0.4, 371, 6000) + np.sin(2 * np.pi * 3400 * t) * np.exp(-t * 25) * 0.3
    return _nrm(x, 0.9)


def s_taza(**k):
    d = 0.6
    t = _t(d)
    return _nrm(np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 9) + np.sin(2 * np.pi * 3700 * t) * np.exp(-t * 14) * 0.5 +
                _golpe(400, 200, d, 0.03, 0.3, 381) * 0.5, 0.7)


def s_cafe_sirve(dur=2.0, **k):
    t = _t(dur)
    f = 600 + 900 * t / dur                                      # la taza se llena: sube el tono
    x = bp(ruido(len(t), 391), 1, 1) * 0 + bp(ruido(len(t), 392), 1200, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * f * t / 50))
    return _nrm(_fade(x, 0.1, 0.3), 0.6)


def s_desenchufa(**k):
    d = 0.4
    t = _t(d)
    x = _golpe(500, 300, d, 0.06, 0.6, 401, 3000) + butter_hp(ruido(len(t), 402), 5000, 2) * np.exp(-t * 80) * 0.6
    return _nrm(x, 0.9)


def s_enchufa(**k):
    return s_desenchufa() * 0.9


def s_interruptor(**k):
    d = 0.35
    return _nrm(_golpe(1800, 600, d, 0.03, 0.8, 411, 7000), 0.95)


def s_linterna_click(**k):
    return _nrm(_golpe(2600, 1600, 0.12, 0.012, 0.5, 421, 9000), 0.8)


def s_alarma_leds(dur=1.8, **k):
    t = _t(dur)
    x = np.sin(2 * np.pi * 1200 * t) * (np.sin(2 * np.pi * 10 * t) > 0)
    return _nrm(_fade(x * 0.5, 0.02, 0.2), 0.5)


def s_camara_zoom(**k):
    d = 0.8
    t = _t(d)
    return _nrm(_fade(np.sin(2 * np.pi * np.cumsum(380 + 120 * t) / SR) * 0.3, 0.05, 0.2), 0.5)


def s_lampara_chisporrotea(dur=1.2, **k):
    x = _granos(dur, dur * 80, lambda q: q.uniform(2000, 6000), 431, 0.004, 1.0)
    t = _t(dur)
    x += np.sin(2 * np.pi * 120 * t) * 0.3 * (np.sin(2 * np.pi * 14 * t) > 0.3)
    return _nrm(x, 0.7)


def s_electricidad(dur=1.4, **k):
    t = _t(dur)
    x = saturar(np.sin(2 * np.pi * 60 * t) * 3 * (1 + np.sin(2 * np.pi * 7 * t)), 3) * 0.4
    x += _granos(dur, dur * 120, lambda q: q.uniform(3000, 8000), 441, 0.003, 1.0)
    return _nrm(_fade(x, 0.02, 0.3), 0.8)


def s_perillas(dur=2.6, **k):
    x = np.zeros(int(dur * SR))
    r = np.random.default_rng(451)
    c = 0.0
    while c < dur:
        y = _golpe(r.uniform(2000, 4000), 1500, 0.05, 0.008, 0.4, int(c * 1000), 9000) * r.uniform(0.3, 1.0)
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
        c += r.uniform(0.01, 0.06) * (1.5 - c / dur)
    return _nrm(x, 0.6)


def s_pieza_ajedrez(**k):
    return _nrm(_golpe(700, 400, 0.3, 0.05, 0.6, 461, 4000), 0.85)


def s_ficha(**k):
    d = 0.25
    t = _t(d)
    return _nrm(np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 30) + _golpe(1200, 700, d, 0.02, 0.5, 471, 7000), 0.8)


def s_fichas_mezcla(dur=1.8, **k):
    x = np.zeros(int(dur * SR))
    r = np.random.default_rng(481)
    for _ in range(int(dur * 18)):
        y = s_ficha() * r.uniform(0.2, 0.8)
        i = int(r.uniform(0, len(x) - len(y)))
        x[i:i + len(y)] += y
    return _nrm(x, 0.8)


def s_fichas_empuja(dur=1.2, **k):
    t = _t(dur)
    return _nrm(bp(ruido(len(t), 491), 1800, 1.5) * np.clip(1 - t / dur, 0, 1) + s_fichas_mezcla(dur)[: len(t)] * 0.5, 0.8)


def s_caja_registradora(**k):
    d = 1.4
    t = _t(d)
    x = _golpe(900, 500, d, 0.05, 0.8, 501, 5000)
    ding = np.sin(2 * np.pi * 2600 * t) * np.exp(-np.maximum(t - 0.25, 0) * 5) * (t > 0.25)
    return _nrm(x + ding * 0.8 + s_fichas_mezcla(d)[: len(t)] * 0.3, 0.9)


def s_dados(**k):
    x = np.zeros(int(1.4 * SR))
    for j, c in enumerate((0.0, 0.18, 0.31, 0.42, 0.5, 0.57)):
        y = _golpe(1500, 900, 0.08, 0.015, 0.6, 510 + j, 8000) * (1 - j * 0.12)
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.8)


def s_dardo(**k):
    d = 0.6
    t = _t(d)
    zum = bp(ruido(len(t), 521), 3000, 3) * np.clip(1 - t / 0.25, 0, 1) * 0.6
    golpe = np.pad(_golpe(600, 300, 0.35, 0.05, 0.8, 522, 4000), (int(0.25 * SR), 0))[:len(t)]
    return _nrm(zum + golpe, 0.9)


def s_lupa(**k):
    return _nrm(_fade(np.sin(2 * np.pi * np.cumsum(np.linspace(900, 1800, int(0.4 * SR))) / SR) * 0.4, 0.05, 0.2), 0.4)


def s_brujula(dur=2.4, **k):
    t = _t(dur)
    x = np.sin(2 * np.pi * (500 + 80 * np.sin(2 * np.pi * 1.3 * t)) * t) * 0.2 + _granos(dur, dur * 8, lambda q: 2400, 531, 0.02, 0.4)
    return _nrm(_fade(x, 0.1, 0.3), 0.5)


def s_oro_brillo(**k):
    d = 1.2
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (3 + j)) for j, f in enumerate((2093, 2637, 3136, 4186)))
    return _nrm(x * (1 + 0.3 * np.sin(2 * np.pi * 12 * t)), 0.6)


def s_corona_cae(**k):
    x = np.zeros(int(1.6 * SR))
    for j, c in enumerate((0.0, 0.3, 0.5, 0.64, 0.74)):
        t = _t(0.6)
        y = (np.sin(2 * np.pi * 1700 * t) + 0.6 * np.sin(2 * np.pi * 4300 * t)) * np.exp(-t * 9) * (1 - 0.15 * j)
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.7)


def s_apreton(**k):
    d = 0.4
    t = _t(d)
    return _nrm(bp(ruido(len(t), 541), 800, 1) * np.exp(-t * 14) + _golpe(160, 90, d, 0.05, 0.3, 542) * 0.6, 0.7)


def s_cerilla(**k):
    d = 1.6
    t = _t(d)
    ras = bp(ruido(len(t), 551), 3000, 1.2) * np.exp(-t * 18)
    llama = butter_lp(ruido(len(t), 552), 900, 2) * np.clip((t - 0.1) * 6, 0, 1) * np.exp(-t * 0.8) * 0.7
    return _nrm(ras + llama, 0.85)


def s_apagado_vela(**k):
    d = 0.8
    t = _t(d)
    return _nrm(butter_lp(ruido(len(t), 561), 600, 2) * np.sin(np.pi * np.minimum(t / 0.5, 1)) * np.exp(-t * 2), 0.6)


def s_colilla(**k):
    d = 0.5
    t = _t(d)
    return _nrm(bp(ruido(len(t), 571), 2400, 2) * np.sin(np.pi * t / d) * 0.6, 0.5)


def s_chisporroteo(**k):
    d = 1.0
    t = _t(d)
    x = butter_hp(ruido(len(t), 581), 3000, 2) * np.exp(-t * 4) + _granos(d, 40, lambda q: q.uniform(3000, 7000), 582, 0.004, 0.8)
    return _nrm(x, 0.7)


def s_calada(dur=1.4, **k):
    t = _t(dur)
    x = bp(ruido(len(t), 591), 1600, 1) * np.sin(np.pi * t / dur) * 0.7 + _granos(dur, dur * 60, lambda q: q.uniform(3000, 6000), 592,
                                                                                   0.003, 0.5)
    return _nrm(x, 0.6)


def s_exhala(dur=1.6, **k):
    t = _t(dur)
    return _nrm(bp(ruido(len(t), 601), 900, 0.8) * np.sin(np.pi * t / dur) ** 1.5, 0.6)


def s_puerta(**k):
    d = 1.4
    t = _t(d)
    chirr = np.sin(2 * np.pi * np.cumsum(400 + 200 * np.sin(2 * np.pi * 3 * t)) / SR) * np.exp(-t * 1.5) * 0.3
    x = chirr.copy()
    _mete(x, _golpe(120, 60, 0.4, 0.1, 0.8, 611), int(0.9 * SR))
    return _nrm(x, 0.7)


def s_paso_madera(**k):
    return _nrm(_golpe(200, 90, 0.25, 0.04, 0.8, 621, 2500), 0.7)


def s_paso_firme(**k):
    return _nrm(_golpe(160, 70, 0.3, 0.05, 0.9, 631, 2200), 0.8)


def s_pasos_mojados(dur=3.0, **k):
    x = np.zeros(int(dur * SR))
    for j, c in enumerate(np.arange(0.1, dur, 0.55)):
        y = _golpe(170, 80, 0.3, 0.05, 0.6, 640 + j, 2200) + bp(ruido(int(0.3 * SR), 660 + j), 2500, 1.5) * _env(0.3, 0.05) * 0.6
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i] * (1 - 0.6 * c / dur)
    return _nrm(x, 0.7)


def s_persiana(**k):
    d = 0.7
    x = np.zeros(int(d * SR))
    for j in range(9):
        y = _golpe(1800, 1200, 0.05, 0.01, 0.5, 670 + j, 7000)
        i = int(j * 0.045 * SR)
        x[i:i + len(y)] += y[:len(x) - i]
    return _nrm(x, 0.6)


def s_focos(**k):
    """Tubos que se encienden: golpe de relé y el zumbido que parpadea."""
    d = 1.2
    t = _t(d)
    x = _golpe(300, 120, d, 0.06, 0.8, 681, 3000) + np.sin(2 * np.pi * 120 * t) * (np.sin(2 * np.pi * 15 * t) > -0.2) * np.exp(-t * 1.5) * 0.4
    return _nrm(x, 0.9)


# ================================================================== transiciones y atmósferas
def s_barrido_aire(dur=0.6, **k):
    t = _t(dur)
    f = 300 + 3000 * np.sin(np.pi * t / dur) ** 2
    x = np.zeros(len(t))
    y = ruido(len(t), 691)
    for j in range(0, len(t), 512):
        x[j:j + 512] = bp(y[j:j + 512 + 64], f[j], 1.2)[:len(x[j:j + 512])]
    return _nrm(x * np.sin(np.pi * t / dur) ** 2, 0.7)


def s_relampago_corto(**k):
    d = 0.6
    t = _t(d)
    return _nrm(butter_hp(ruido(len(t), 701), 1500, 2) * np.exp(-t * 18) + butter_lp(ruido(len(t), 702), 200, 2) * np.exp(-t * 4) * 0.8, 0.8)


def s_tinta_mancha(dur=0.8, **k):
    t = _t(dur)
    gota = np.sin(2 * np.pi * np.cumsum(500 * np.exp(-t * 12) + 120) / SR) * np.exp(-t * 6)
    return _nrm(gota + butter_lp(ruido(len(t), 711), 700, 2) * np.sin(np.pi * t / dur) * 0.5, 0.6)


def s_grave_inquietante(dur=3.0, **k):
    t = _t(dur)
    x = np.sin(2 * np.pi * 41 * t) + 0.6 * np.sin(2 * np.pi * 43.3 * t) + 0.3 * np.sin(2 * np.pi * 61.5 * t)
    x += butter_lp(ruido(len(t), 721), 120, 2) * 0.5
    return _nrm(_fade(x, min(1.0, dur * 0.3), min(1.2, dur * 0.4)), 0.8)


def s_sombra_crece(dur=3.0, **k):
    t = _t(dur)
    f = 50 + 40 * t / dur
    x = saturar(np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5, 2) * (t / dur) + butter_lp(ruido(len(t), 731), 600, 2) * 0.6 * (t / dur)
    return _nrm(_fade(x, 0.3, 0.2), 0.85)


def s_subida(dur=1.0, **k):
    t = _t(dur)
    f = 200 * (8 ** (t / dur))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + bp(ruido(len(t), 741), 2000, 1) * (t / dur) * 0.4
    return _nrm(x * (t / dur) ** 1.5, 0.75)


def s_golpe_grave(**k):
    d = 1.4
    t = _t(d)
    x = np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-t * 10)) / SR) * np.exp(-t * 2.5) + butter_lp(ruido(len(t), 751), 900, 2) * np.exp(-t * 12)
    return _nrm(saturar(x, 1.5), 0.95)


def s_caida(dur=1.0, **k):
    t = _t(dur)
    f = 1200 * (0.15 ** (t / dur))
    return _nrm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.5) * 0.7, 0.7)


def s_teletipo(dur=2.0, **k):
    x = np.zeros(int(dur * SR))
    c = 0.0
    j = 0
    while c < dur:
        y = _golpe(1400, 900, 0.03, 0.006, 0.5, 760 + j, 8000)
        i = int(c * SR)
        x[i:i + len(y)] += y[:len(x) - i]
        c += 0.035
        j += 1
    return _nrm(x, 0.5)


def s_crecer(dur=2.0, **k):
    t = _t(dur)
    x = np.zeros(len(t))
    for j, f in enumerate((220, 330, 440, 660, 880)):
        x += np.sin(2 * np.pi * f * t) * np.clip((t / dur - j * 0.15) * 4, 0, 1) * 0.3
    x += _granos(dur, dur * 40, lambda q: q.uniform(1000, 3000), 771, 0.01, 0.3)
    return _nrm(_fade(x, 0.05, 0.6), 0.6)


def s_tunel(dur=3.0, **k):
    t = _t(dur)
    x = sum(np.sin(2 * np.pi * f * t + j) for j, f in enumerate((55, 82.5, 110, 165))) * 0.3
    x = x * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t)) + bp(ruido(len(t), 781), 1200, 3) * 0.2
    return _nrm(_fade(x, 0.5, 0.8), 0.7)


def s_silencio_tono(dur=2.0, **k):
    t = _t(dur)
    return _nrm(_fade(np.sin(2 * np.pi * 2200 * t) * 0.15 + butter_lp(ruido(len(t), 791), 80, 2) * 0.2, 0.5, 0.8), 0.3)


def s_campana_bolsa(**k):
    d = 2.5
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (1.2 + j * 0.6)) for j, f in enumerate((523, 1046 * 1.01, 1568, 2093 * 0.99)))
    return _nrm(x, 0.6)


def s_trueno_noir(dur=4.0, **k):
    t = _t(dur)
    crack = butter_hp(ruido(len(t), 801), 800, 2) * np.exp(-t * 9)
    rodar = butter_lp(ruido(len(t), 802), 160, 2) * np.exp(-t * 0.9) * (1 + 0.8 * np.sin(2 * np.pi * 2.2 * t) ** 2)
    x = crack * 0.7 + rodar * 2.0
    return _nrm(_st(x, np.roll(x, 1200)), 0.95)
