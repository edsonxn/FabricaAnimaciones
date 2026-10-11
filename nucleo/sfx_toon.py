# -*- coding: utf-8 -*-
"""Efectos de sonido del estilo cartoon90 (sin voz, terror cómico): gritos con formantes, cascabel, crujidos de madera, refri, tripas, eructo,
masticar, estática de TV, cuerdas de susto... Se importan al final de sfx.py (cada `s_nombre` queda en la biblioteca). Todo sintetizado."""
import math

import numpy as np

from sinte import SR, adsr, bp, butter_hp, butter_lp, cuadrada, hp, lp, mtof, ruido, saturar, sierra


def _t(d):
    return np.arange(int(d * SR)) / SR


def _nrm(x, pico=0.9):
    return x / (np.abs(x).max() + 1e-9) * pico


def _glide(f0, f1, d, curva=1.0):
    t = _t(d)
    u = (t / d) ** curva
    f = f0 * (f1 / f0) ** u
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def _env(d, caida, ataque=0.002):
    t = _t(d)
    return np.minimum(1, t / ataque) * np.exp(-t / caida)


def _campana(f, d=1.0, idx=3.0, ratio=3.5, caida=0.4):
    t = _t(d)
    ix = idx * np.exp(-t * 5)
    return np.sin(2 * np.pi * f * t + ix * np.sin(2 * np.pi * f * ratio * t)) * _env(d, caida)


def _voz(f, formantes, d, aire=0.12, seed=0):
    """Fuente glotal (sierra con la frecuencia `f` por muestra) filtrada por formantes (lista de (Hz, q, ganancia)) + un poco de aire."""
    src = sierra(f)
    out = np.zeros_like(src)
    for fc, q, g in formantes:
        out += bp(src, fc, q) * g
    out += aire * bp(ruido(len(src), seed), 2200, 0.8)
    return out


# ---------------------------------------------------------------- gritos
def s_grito_gato(dur=1.3, tono=1.0, **k):
    """El grito de pánico de Mostacho: agudo, con vibrato, que sube y se quiebra."""
    d = max(0.5, dur)
    t = _t(d)
    f0 = 520 * tono
    f = f0 * (1 + 0.55 * (1 - np.exp(-t * 9))) * (1 + 0.035 * np.sin(2 * np.pi * 7.4 * t) * np.minimum(1, t * 4))
    f = f * (1 + 0.12 * np.sin(2 * np.pi * 17 * t) * (t > 0.5 * d))                  # se quiebra al final
    x = _voz(f, ((850, 6, 1.0), (1280, 7, 0.8), (2900, 8, 0.45), (3600, 8, 0.3)), d, 0.18, 3)
    env = np.minimum(1, t / 0.018) * np.where(t < d - 0.14, 1.0, np.exp(-(t - (d - 0.14)) / 0.05)) * (0.85 + 0.15 * np.sin(2 * np.pi * 11 * t))
    return _nrm(saturar(x * env, 1.6)) * 0.95


def s_grito_cosa(dur=1.0, tono=1.0, **k):
    """El grito del monstruo: grave, rasposo, con la voz que se parte."""
    d = max(0.5, dur)
    t = _t(d)
    f = 118 * tono * (1 + 0.25 * (1 - np.exp(-t * 6))) * (1 + 0.05 * np.sin(2 * np.pi * 6.1 * t))
    x = _voz(f, ((520, 5, 1.0), (900, 6, 0.9), (2200, 7, 0.4)), d, 0.25, 5)
    x = x * (0.7 + 0.3 * np.sign(np.sin(2 * np.pi * 38 * t)))                        # rasposo
    env = np.minimum(1, t / 0.03) * np.where(t < d - 0.14, 1.0, np.exp(-(t - (d - 0.14)) / 0.06))
    return _nrm(saturar(x * env, 2.2)) * 0.95


def s_grito_lejano(dur=1.0, **k):
    """El grito de los dos, oído desde afuera de la casa: apagado y con eco."""
    g = s_grito_gato(dur=max(0.8, dur), tono=0.9) + 0.9 * s_grito_cosa(dur=max(0.8, dur))
    g = lp(g, 1100)
    out = np.zeros(len(g) + SR)
    for i, a in enumerate((1.0, 0.45, 0.2)):
        s = int(0.16 * i * SR)
        out[s:s + len(g)] += g * a
    return _nrm(out) * 0.8


def s_gruni_hambre(**k):
    d = 1.1
    t = _t(d)
    f = 70 + 18 * np.sin(2 * np.pi * 3.2 * t) + 10 * np.sin(2 * np.pi * 9 * t)
    x = lp(sierra(f), 420) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t) ** 2) * np.sin(np.pi * t / d) ** 0.6
    return _nrm(saturar(x, 2.0)) * 0.85


def s_rugido_bajo(dur=1.6, **k):
    d = max(0.6, dur)
    t = _t(d)
    f = 62 + 26 * np.sin(2 * np.pi * 0.7 * t) + 8 * np.sin(2 * np.pi * 7 * t)
    x = lp(sierra(f), 520) + 0.35 * lp(ruido(len(t), 9), 380)
    x = x * (0.7 + 0.3 * np.sin(2 * np.pi * 13 * t)) * np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.5)
    return _nrm(saturar(x, 1.8)) * 0.9


def s_risa_cosa(**k):
    out = np.zeros(int(1.3 * SR))
    for i in range(5):
        d = 0.16
        t = _t(d)
        f = 110 * (1.0 + 0.1 * i % 3) * (1 + 0.12 * np.sin(np.pi * t / d))
        x = _voz(f, ((560, 5, 1.0), (1000, 6, 0.6)), d, 0.2, 20 + i) * np.sin(np.pi * t / d) ** 0.7
        s = int((0.0 + 0.2 * i) * SR)
        out[s:s + len(x)] += x
    return _nrm(saturar(out, 1.5)) * 0.8


def s_eructo(**k):
    d = 1.0
    t = _t(d)
    f = 95 * (1 - 0.3 * t / d) * (1 + 0.18 * np.sin(2 * np.pi * 21 * t))
    x = _voz(f, ((380, 5, 1.0), (760, 6, 0.8), (1500, 7, 0.3)), d, 0.3, 12)
    env = np.minimum(1, t / 0.05) * np.exp(-t / 0.5) * (0.8 + 0.2 * np.sin(2 * np.pi * 28 * t))
    return _nrm(saturar(x * env, 2.0)) * 0.9


# ---------------------------------------------------------------- cuerpo y comida
def s_trago(**k):
    d = 0.4
    t = _t(d)
    f = 320 * np.exp(-t * 6) + 90
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) + 0.3 * bp(ruido(len(t), 4), 600, 2) * np.exp(-t * 14)
    return _nrm(x) * 0.85


def s_mastica(tono=1.0, **k):
    d = 0.28
    t = _t(d)
    x = bp(ruido(len(t), 31), 480 * tono, 1.4) * np.exp(-t * 22) + np.sin(2 * np.pi * 75 * tono * t) * np.exp(-t * 28)
    x += 0.4 * bp(ruido(len(t), 32), 1700, 2.5) * np.exp(-t * 60) * (t > 0.09)
    return _nrm(x) * 0.8


def s_chomp(**k):
    d = 0.5
    t = _t(d)
    x = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-t * 20) + 45) / SR) * np.exp(-t * 14) + hp(ruido(len(t), 41), 2200) * np.exp(-t * 60) * 0.7
    x += bp(ruido(len(t), 42), 400, 1.6) * np.exp(-t * 18) * 0.6
    return _nrm(saturar(x, 1.4)) * 0.95


def s_baba(**k):
    d = 0.6
    t = _t(d)
    out = np.zeros(len(t))
    rng = np.random.default_rng(55)
    for _ in range(9):
        i = int(rng.random() * (len(t) - 3000))
        L = int(SR * (0.02 + 0.03 * rng.random()))
        tt = np.arange(L) / SR
        out[i:i + L] += np.sin(2 * np.pi * np.cumsum(np.linspace(300, 900, L) * (0.8 + 0.4 * rng.random())) / SR) * np.exp(-tt * 70) * rng.random()
    return _nrm(lp(out, 2400)) * 0.5


def s_tripas(**k):
    d = 1.1
    t = _t(d)
    f = 58 + 40 * np.abs(np.sin(2 * np.pi * 1.7 * t)) + 16 * np.sin(2 * np.pi * 8 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR + 2.5 * np.sin(2 * np.pi * 5 * t))
    x += 0.5 * lp(ruido(len(t), 51), 300) * (0.5 + 0.5 * np.sin(2 * np.pi * 3.3 * t))
    return _nrm(x * np.sin(np.pi * t / d) ** 0.7) * 0.85


def s_snif(**k):
    out = np.zeros(int(0.4 * SR))
    for i in range(2):
        d = 0.11
        t = _t(d)
        x = bp(ruido(len(t), 60 + i), 3200, 1.2) * np.sin(np.pi * t / d) ** 2
        out[int(0.16 * i * SR):int(0.16 * i * SR) + len(x)] += x
    return _nrm(out) * 0.45


def s_soplo(**k):
    d = 0.8
    t = _t(d)
    x = bp(ruido(len(t), 71), 1400, 0.7) * np.exp(-t * 4.2) * np.minimum(1, t / 0.05)
    return _nrm(x) * 0.6


def s_arrastra(dur=0.7, **k):
    d = max(0.3, dur)
    t = _t(d)
    x = bp(ruido(len(t), 81), 900, 0.6) * np.sin(np.pi * t / d) ** 1.4
    return _nrm(x) * 0.5


# ---------------------------------------------------------------- casa y objetos
def s_cascabel(tono=1.0, **k):
    d = 0.7
    out = np.zeros(int(d * SR))
    rng = np.random.default_rng(int(7 * tono * 10))
    for i, (f, a) in enumerate(((2700, 1.0), (3400, 0.7), (2300, 0.5))):
        x = _campana(f * tono * (1 + 0.02 * rng.random()), 0.5, 2.5, 3.7, 0.22) * a
        s = int(0.045 * i * SR)
        out[s:s + len(x)] += x
    return _nrm(out) * 0.6


def s_cascabel_fuerte(**k):
    out = np.zeros(int(1.6 * SR))
    for i in range(7):
        x = s_cascabel(tono=0.9 + 0.1 * (i % 3))
        s = int(0.09 * i * SR)
        out[s:s + len(x)] += x * (1.0 - 0.1 * i)
    return _nrm(out) * 0.9


def s_paso_suave(**k):
    d = 0.16
    t = _t(d)
    x = lp(ruido(len(t), 91), 320) * np.exp(-t * 38) + np.sin(2 * np.pi * 85 * t) * np.exp(-t * 34) * 0.6
    return _nrm(x) * 0.5


def s_crujido_tabla(**k):
    d = 1.2
    t = _t(d)
    f = 190 * np.exp(-t * 0.8) * (1 + 0.06 * np.sin(2 * np.pi * 11 * t))
    x = bp(sierra(f), 520, 5) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * t) ** 2)
    x += bp(sierra(f * 1.5), 940, 6) * 0.5
    x += 0.25 * hp(ruido(len(t), 93), 3000) * np.exp(-t * 6) * (np.random.default_rng(3).random(len(t)) > 0.98)
    return _nrm(x * np.minimum(1, t / 0.06) * np.exp(-t * 1.6)) * 0.85


def s_chirrido(dur=3.0, **k):
    d = max(0.6, dur)
    t = _t(d)
    ciclo = (t * 1.1) % 1.0
    f = 640 + 260 * ciclo + 20 * np.sin(2 * np.pi * 9 * t)
    x = bp(sierra(f), 900, 8) * (np.sin(np.pi * ciclo) ** 2)
    return _nrm(x * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.4)) * 0.35


def s_garras_techo(**k):
    d = 0.9
    t = _t(d)
    x = hp(ruido(len(t), 95), 2200) * (0.4 + 0.6 * (np.sin(2 * np.pi * 26 * t) > 0)) * np.exp(-t * 2.8)
    x += bp(sierra(1900 + 700 * np.sin(2 * np.pi * 3 * t)), 2400, 9) * 0.35 * np.exp(-t * 3.5)
    return _nrm(x) * 0.7


def s_tink(**k):
    return _nrm(_campana(3100, 0.25, 2.0, 3.0, 0.07)) * 0.5


def s_tic(**k):
    d = 0.1
    t = _t(d)
    x = bp(ruido(len(t), 101), 1800, 3) * np.exp(-t * 90) + np.sin(2 * np.pi * 1300 * t) * np.exp(-t * 110) * 0.5
    return _nrm(x) * 0.55


def s_tac(**k):
    d = 0.1
    t = _t(d)
    x = bp(ruido(len(t), 102), 1200, 3) * np.exp(-t * 90) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 110) * 0.5
    return _nrm(x) * 0.5


def s_clic(**k):
    out = np.zeros(int(0.2 * SR))
    for i in range(2):
        x = hp(ruido(int(0.012 * SR), 103 + i), 1800) * _env(0.012, 0.003)
        out[int(0.07 * i * SR):int(0.07 * i * SR) + len(x)] += x
    return _nrm(out) * 0.7


def s_guino(**k):
    return _nrm(_campana(2400, 0.3, 1.5, 2.2, 0.08)) * 0.5


def s_ojos_retrato(**k):
    d = 0.5
    t = _t(d)
    x = bp(ruido(len(t), 107), 700, 1.5) * np.sin(np.pi * t / d) ** 2 * 0.5 + _glide(220, 340, d) * 0.1 * np.sin(np.pi * t / d)
    return _nrm(x) * 0.4


def s_ronquido(tono=1.0, **k):
    d = 1.1
    t = _t(d)
    f = (170 - 60 * np.sin(np.pi * np.minimum(1, t / 0.6))) * tono * (1 + 0.1 * np.sin(2 * np.pi * 25 * t))
    x = lp(sierra(f), 600) * np.sin(np.pi * np.minimum(1, t / 0.55)) * np.exp(-np.maximum(t - 0.55, 0) * 6)
    x += 0.4 * bp(ruido(len(t), 109), 500, 1.2) * np.sin(np.pi * np.minimum(1, t / 0.5)) ** 2
    return _nrm(x) * 0.6


def s_estatica(dur=7.0, **k):
    d = max(1.0, dur)
    t = _t(d)
    x = bp(ruido(len(t), 111), 3800, 0.5) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.6 * t)) + 0.3 * hp(ruido(len(t), 112), 6000)
    x += 0.15 * np.sin(2 * np.pi * 15734 * t)
    return _nrm(x * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3)) * 0.25


def s_grillos(dur=7.0, **k):
    d = max(1.0, dur)
    t = _t(d)
    x = np.sin(2 * np.pi * 4300 * t) * (np.sin(2 * np.pi * 30 * t) > 0) * (np.sin(2 * np.pi * 2.2 * t) > 0.1)
    x += 0.6 * np.sin(2 * np.pi * 4700 * t) * (np.sin(2 * np.pi * 34 * t) > 0) * (np.sin(2 * np.pi * 1.7 * t + 1) > 0.2)
    return _nrm(x * np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.5)) * 0.2


def s_buho(**k):
    out = np.zeros(int(1.8 * SR))
    for i, (t0, d, f0) in enumerate(((0.0, 0.28, 390), (0.42, 0.28, 390), (0.86, 0.7, 360))):
        t = _t(d)
        f = f0 * (1 - 0.12 * t / d)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 0.8 + 0.25 * bp(ruido(len(t), 120 + i), 700, 1.5) * np.sin(np.pi * t / d)
        out[int(t0 * SR):int(t0 * SR) + len(x)] += lp(x, 900)
    return _nrm(out) * 0.5


def s_aleteo(**k):
    d = 0.8
    t = _t(d)
    x = bp(ruido(len(t), 131), 900, 0.8) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * t))) ** 2 * np.exp(-t * 3.0)
    return _nrm(x) * 0.55


def s_tum(tono=1.0, **k):
    d = 0.8
    t = _t(d)
    x = np.sin(2 * np.pi * np.cumsum(110 * tono * np.exp(-t * 7) + 38) / SR) * np.exp(-t * 6.5)
    x += lp(ruido(len(t), 141), 260) * np.exp(-t * 20) * 0.6
    return _nrm(saturar(x, 1.6)) * 0.95


def s_estallido(**k):
    d = 0.9
    t = _t(d)
    x = hp(ruido(len(t), 151), 600) * np.exp(-t * 14) * 0.9 + np.sin(2 * np.pi * np.cumsum(180 * np.exp(-t * 12) + 40) / SR) * np.exp(-t * 7)
    return _nrm(saturar(x, 1.8)) * 0.95


# ---------------------------------------------------------------- refri, luz, cuerdas
def s_zumbido_refri(dur=12.0, **k):
    d = max(1.0, dur)
    t = _t(d)
    x = np.sin(2 * np.pi * 59.7 * t) * 0.8 + np.sin(2 * np.pi * 119.4 * t) * 0.4 + 0.15 * np.sin(2 * np.pi * 179 * t)
    x = x * (1 + 0.06 * np.sin(2 * np.pi * 0.4 * t)) + 0.05 * lp(ruido(len(t), 161), 400)
    return _nrm(x * np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.4)) * 0.35


def s_puerta_refri(dur=1.6, **k):
    d = max(0.8, dur)
    t = _t(d)
    seal = bp(ruido(int(0.3 * SR), 171), 1600, 0.8) * np.exp(-_t(0.3) * 9)
    f = (310 + 160 * (t / d)) * (1 + 0.05 * np.sin(2 * np.pi * 9 * t))
    x = bp(sierra(f), 620, 7) * (0.5 + 0.5 * np.sin(np.pi * t / d)) * 0.8
    out = x * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.2)
    out[:len(seal)] += seal * 0.8
    return _nrm(out) * 0.8


def s_luz_fria(**k):
    d = 1.4
    t = _t(d)
    x = np.sin(2 * np.pi * 440 * t) * 0.5 + np.sin(2 * np.pi * 443 * t) * 0.5 + np.sin(2 * np.pi * 659 * t) * 0.3 + np.sin(2 * np.pi * 1318 * t) * 0.12
    x = x * np.sin(np.pi * t / d) ** 1.5
    x += bp(ruido(len(t), 181), 3500, 0.6) * np.sin(np.pi * t / d) ** 3 * 0.25
    return _nrm(x) * 0.5


def s_ojo_abre(**k):
    d = 1.0
    t = _t(d)
    f = 110 + 120 * (t / d) ** 2
    x = np.sin(2 * np.pi * np.cumsum(f) / SR + 3 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / d) ** 0.8
    x += 0.4 * bp(ruido(len(t), 191), 900, 3) * np.sin(np.pi * t / d) ** 2
    return _nrm(lp(x, 1400)) * 0.85


def s_refri_tiembla(dur=1.2, **k):
    d = max(0.5, dur)
    t = _t(d)
    x = cuadrada(55 + 10 * np.sin(2 * np.pi * 14 * t)) * 0.5
    x += hp(ruido(len(t), 201), 1500) * (np.random.default_rng(5).random(len(t)) > 0.994) * 1.4
    x += bp(ruido(len(t), 202), 700, 1.2) * (0.4 + 0.6 * (np.sin(2 * np.pi * 21 * t) > 0))
    return _nrm(lp(x, 2500) * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.2)) * 0.8


def s_susto_cuerdas(**k):
    d = 1.5
    n = int(d * SR)
    t = _t(d)
    out = np.zeros(n)
    for m, a in ((71, 1.0), (72, 0.9), (75, 0.8), (77, 0.7), (82, 0.6), (83, 0.5)):
        f = mtof(m) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t + m))
        out += sierra(f) * a
    env = np.minimum(1, t / 0.012) * np.exp(-t / 0.55) + 0.5 * np.minimum(1, t / 0.25) * np.exp(-t / 0.9)
    x = lp(out * env, 3600)
    c = _campana(2900, 0.4, 2.0, 3.0, 0.1) * 0.25
    x[:len(c)] += c
    return _nrm(x) * 0.8
