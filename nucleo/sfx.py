# -*- coding: utf-8 -*-
"""Efectos de sonido sintetizados y colocados en los tiempos que definen las escenas.
Salida: audio/sfx.wav y audio/sfx_eventos.json"""
import json
import math
import os

import numpy as np
import soundfile as sf

from sinte import (SR, adsr, bp, butter_hp, butter_lp, cuadrada, hp, lp, mtof, panear, reverb, ruido, saturar,
                   sierra, sumar, svf)

TOTAL = json.load(open("timeline.json", encoding="utf-8"))["total"]
N = int((TOTAL + 0.5) * SR)


def _t(d):
    return np.arange(int(d * SR)) / SR


def glide(f0, f1, d, curva=1.0):
    t = _t(d)
    u = (t / d) ** curva
    f = f0 * (f1 / f0) ** u
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def env_exp(d, caida, ataque=0.002):
    t = _t(d)
    return np.minimum(1, t / ataque) * np.exp(-t / caida)


def fm_campana(f, d=1.2, idx=3.0, ratio=3.5, caida=0.4):
    t = _t(d)
    ix = idx * np.exp(-t * 5)
    return np.sin(2 * np.pi * f * t + ix * np.sin(2 * np.pi * f * ratio * t)) * env_exp(d, caida)


def nrm(x, pico=0.9):
    m = np.abs(x).max()
    return x / m * pico if m > 0 else x


# ------------------------------------------------------------ biblioteca
def s_impacto(tono=1.0, **k):
    d = 1.4
    t = _t(d)
    f = 30 + 70 * np.exp(-t * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f * tono) / SR) * np.exp(-t * 2.8)
    golpe = butter_lp(ruido(len(t), 1), 1800, 2) * np.exp(-t * 14)
    crack = hp(ruido(len(t), 2), 3000) * np.exp(-t * 40) * 0.4
    return nrm(saturar(sub * 1.0 + golpe * 0.8 + crack, 1.6))


def s_pop(tono=1.0, **k):
    d = 0.12
    x = glide(380 * tono, 1250 * tono, d, 0.6) * env_exp(d, 0.035, 0.001)
    return nrm(x + hp(ruido(len(x), 3), 4000) * env_exp(d, 0.004) * 0.3)


def s_whoosh(dur=0.45, tono=1.0, **k):
    d = max(0.15, dur)
    t = _t(d)
    u = t / d
    fc = (300 + 2800 * tono * np.sin(np.pi * u) ** 1.5)
    x = svf(ruido(len(t), 4), fc, 1.8, 1) * np.sin(np.pi * u) ** 2
    pan = -0.8 + 1.6 * u
    return np.stack([x * np.cos((pan + 1) * np.pi / 4), x * np.sin((pan + 1) * np.pi / 4)]) * 0.9 / (np.abs(x).max() + 1e-9)


def s_sello(tono=1.0, **k):
    d = 0.25
    t = _t(d)
    x = butter_lp(ruido(len(t), 5), 900, 2) * np.exp(-t * 30) + np.sin(2 * np.pi * 170 * tono * t) * np.exp(-t * 25) * 0.8
    return nrm(x)


def s_error(**k):
    d = 0.42
    t = _t(d)
    x = (cuadrada(np.full(len(t), 110.0)) + cuadrada(np.full(len(t), 117.0))) * 0.5
    gate = ((t % 0.2) < 0.15).astype(float)
    return nrm(lp(x, 1800) * gate * np.exp(-t * 2)) * 0.8


def s_brillo(tono=1.0, **k):
    notas = [84, 88, 91, 96, 100, 103]
    out = np.zeros((2, int(1.4 * SR)))
    for i, m in enumerate(notas):
        b = fm_campana(mtof(m) * tono, 0.9, 1.5, 2.0, 0.25) * 0.5
        sumar(out, panear(b, -0.7 + 0.28 * i), 0.045 * i)
    return out / (np.abs(out).max() + 1e-9) * 0.8


def s_boing(tono=1.0, **k):
    d = 0.6
    t = _t(d)
    f = 170 * tono * (1 + 0.55 * np.sin(2 * np.pi * 13 * t) * np.exp(-t * 4)) * (1 + 0.8 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.22)
    return nrm(x)


def s_ding(tono=1.0, **k):
    return nrm(fm_campana(1320 * tono, 1.4, 2.0, 2.76, 0.45) + fm_campana(2640 * tono, 1.4, 1.0, 2.0, 0.2) * 0.3) * 0.8


def s_eco(**k):
    base = glide(900, 300, 0.35, 0.7) * env_exp(0.35, 0.15)
    out = np.zeros((2, int(1.8 * SR)))
    for i in range(6):
        sumar(out, panear(base * 0.75 ** i, 0.7 * (-1) ** i), 0.22 * i)
    return out / (np.abs(out).max() + 1e-9) * 0.8


def s_golpe_suave(**k):
    d = 0.2
    t = _t(d)
    return nrm(butter_lp(ruido(len(t), 6), 350, 2) * np.exp(-t * 35) + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 30))


def s_spray(dur=1.0, **k):
    d = max(0.3, dur)
    t = _t(d)
    puff = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 3.2 * t)) ** 0.6
    x = bp(hp(ruido(len(t), 7), 2500), 6500, 0.6) * puff
    fade = np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.2)
    return nrm(x * fade) * 0.7


def s_revelar(**k):
    d = 0.9
    x = glide(500, 2400, d, 1.2) * env_exp(d, 0.35, 0.05) * 0.6
    return nrm(np.stack([x, x]) + s_brillo(1.2)[:, :len(x)] * 0.5)


def s_obturador(**k):
    d = 0.2
    t = _t(d)
    c1 = bp(ruido(len(t), 8), 3200, 1.2) * np.exp(-t * 300)
    c2 = np.zeros_like(t)
    i = int(0.075 * SR)
    c2[i:] = bp(ruido(len(t) - i, 9), 2400, 1.2) * np.exp(-t[:len(t) - i] * 260)
    zumbido = bp(ruido(len(t), 10), 5000, 3) * ((t > 0.01) & (t < 0.07)) * 0.25
    return nrm(c1 + c2 + zumbido)


def s_pincel(dur=2.0, **k):
    d = max(0.3, dur)
    out = np.zeros(int(d * SR))
    rng = np.random.default_rng(11)
    tt = 0.0
    while tt < d - 0.3:
        dd = rng.uniform(0.12, 0.28)
        x = svf(ruido(int(dd * SR), int(tt * 100)), np.linspace(1200, 2600, int(dd * SR)), 1.2, 1) * np.sin(np.pi * np.linspace(0, 1, int(dd * SR)))
        i = int(tt * SR)
        out[i:i + len(x)] += x[:len(out) - i]
        tt += dd + rng.uniform(0.05, 0.15)
    return nrm(out) * 0.6


def s_oink(**k):
    out = np.zeros(int(0.8 * SR))
    for j, (t0, f0) in enumerate(((0.0, 125), (0.33, 140))):
        d = 0.26
        t = _t(d)
        f = f0 * (1 + 0.35 * np.sin(np.pi * t / d)) * (1 + 0.04 * np.sin(2 * np.pi * 28 * t))
        src = sierra(f)
        voz = bp(src, 650, 2.5) * 1.2 + bp(src, 1300, 3) * 0.8 + bp(src, 2600, 4) * 0.4
        voz = voz * np.sin(np.pi * t / d) ** 0.7
        voz = saturar(voz * 2.0, 1.8)
        i = int(t0 * SR)
        out[i:i + len(voz)] += voz
    return nrm(out)


def s_reloj_rapido(dur=1.5, **k):
    d = max(0.5, dur)
    out = np.zeros(int(d * SR))
    tt, paso, j = 0.0, 0.14, 0
    while tt < d - 0.05:
        n = int(0.03 * SR)
        tk = np.sin(2 * np.pi * (1500 + 40 * j) * _t(0.03)) * env_exp(0.03, 0.006)
        i = int(tt * SR)
        out[i:i + n] += tk[:len(out) - i]
        tt += paso
        paso = max(0.03, paso * 0.9)
        j += 1
    sw = s_whoosh(d, 0.8)[0][:len(out)]
    return nrm(out * 0.7 + sw * 0.5)


def s_aparicion(**k):
    d = 1.6
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t) for f in (220, 330, 440, 660)) * adsr(len(t), 0.5, 0.5, 0.6, 0.6, 0.9)
    boom = np.sin(2 * np.pi * np.cumsum(40 + 40 * np.exp(-t * 6)) / SR) * np.exp(-t * 2.5)
    return nrm(x * 0.4 + boom)


def s_rugido(**k):
    d = 1.1
    t = _t(d)
    f = 85 * (1 + 0.25 * np.sin(np.pi * t / d))
    fuente = sierra(f) * (1 + 0.6 * np.sin(2 * np.pi * 32 * t)) + ruido(len(t), 12) * 0.7
    x = bp(fuente, 450, 1.2) + bp(fuente, 900, 2) * 0.6 + lp(fuente, 250) * 0.8
    x = saturar(x * 2.5 * np.sin(np.pi * t / d) ** 0.5, 2.0)
    return nrm(x)


def s_comic(**k):
    d = 0.6
    t = _t(d)
    golpe = np.sin(2 * np.pi * np.cumsum(90 + 140 * np.exp(-t * 20)) / SR) * np.exp(-t * 8)
    ting = fm_campana(2100, d, 1.2, 1.5, 0.15)
    return nrm(golpe + ting * 0.4 + hp(ruido(len(t), 13), 2000) * np.exp(-t * 25) * 0.5)


def s_clink(tono=1.0, **k):
    d = 0.18
    t = _t(d)
    f = 2900 * tono
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 30) + 0.5 * np.sin(2 * np.pi * f * 1.51 * t) * np.exp(-t * 45)
    return nrm(x + hp(ruido(len(t), 14), 5000) * np.exp(-t * 200) * 0.4) * 0.7


def s_bling(**k):
    a = fm_campana(mtof(88), 1.2, 2.0, 2.0, 0.4)
    b = fm_campana(mtof(95), 1.2, 2.0, 2.0, 0.4)
    out = np.zeros((2, int(1.5 * SR)))
    sumar(out, panear(a, -0.4), 0.0)
    sumar(out, panear(b, 0.4), 0.09)
    sumar(out, s_brillo(1.3) * 0.6, 0.05)
    return out / (np.abs(out).max() + 1e-9) * 0.85


def s_viento(dur=1.3, **k):
    d = max(0.5, dur)
    t = _t(d)
    fc = 600 + 300 * np.sin(2 * np.pi * 0.7 * t) + 200 * np.sin(2 * np.pi * 1.9 * t)
    x = svf(ruido(len(t), 15), fc, 3.0, 1) * np.sin(np.pi * t / d) ** 0.8
    return nrm(np.stack([x, np.roll(x, 400)])) * 0.7


def s_brr(**k):
    d = 0.7
    t = _t(d)
    x = sierra(np.full(len(t), 95.0)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 26 * t)))
    x = lp(x, 900) * np.sin(np.pi * t / d)
    return nrm(x) * 0.8


def s_puntada(**k):
    d = 0.09
    t = _t(d)
    x = svf(ruido(len(t), 16), np.linspace(2000, 6000, len(t)), 2, 1) * np.sin(np.pi * t / d)
    return nrm(x) * 0.7


def s_flashes(dur=1.0, **k):
    out = np.zeros((2, int((dur + 0.3) * SR)))
    rng = np.random.default_rng(17)
    tt = 0.0
    while tt < dur:
        sumar(out, panear(s_obturador() * 0.8, rng.uniform(-0.8, 0.8)), tt)
        tt += rng.uniform(0.08, 0.2)
    return out / (np.abs(out).max() + 1e-9) * 0.8


def s_tick(tono=1.0, **k):
    d = 0.05
    t = _t(d)
    x = bp(ruido(len(t), 18), 3000, 6) * np.exp(-t * 180) + np.sin(2 * np.pi * 1900 * tono * t) * np.exp(-t * 90) * 0.7
    return nrm(x)


def s_hmm(**k):
    a = glide(500, 520, 0.16) * env_exp(0.16, 0.08, 0.01)
    b = glide(520, 780, 0.22, 0.5) * env_exp(0.22, 0.12, 0.01)
    out = np.zeros(int(0.5 * SR))
    out[:len(a)] += a
    i = int(0.2 * SR)
    out[i:i + len(b)] += b
    return nrm(out) * 0.7


def s_chapuzon(tono=1.0, **k):
    d = 0.9
    t = _t(d)
    x = hp(ruido(len(t), 19), 700) * np.exp(-t * 6) * np.minimum(1, t / 0.01)
    rng = np.random.default_rng(20)
    for j in range(10):
        dd = 0.06
        b = glide(rng.uniform(300, 700) * tono, rng.uniform(900, 1600) * tono, dd) * env_exp(dd, 0.02)
        i = int(rng.uniform(0.05, 0.6) * SR)
        x[i:i + len(b)] += b * 0.5
    return nrm(x)


def s_pasos(dur=1.0, **k):
    out = np.zeros(int((dur + 0.2) * SR))
    tt, j = 0.0, 0
    while tt < dur:
        g = butter_lp(ruido(int(0.08 * SR), 30 + j), 380, 2) * env_exp(0.08, 0.02)
        i = int(tt * SR)
        out[i:i + len(g)] += g
        tt += 0.22
        j += 1
    return nrm(out) * 0.7


def s_latido(**k):
    out = np.zeros(int(1.3 * SR))
    for tt, a in ((0.0, 1.0), (0.2, 0.7), (0.62, 1.0), (0.82, 0.7)):
        t = _t(0.18)
        g = np.sin(2 * np.pi * 52 * t) * np.exp(-t * 22) * a
        i = int(tt * SR)
        out[i:i + len(g)] += g
    return nrm(out)


def s_bebe(**k):
    out = np.zeros((2, int(1.6 * SR)))
    for i, m in enumerate((84, 88, 91, 96)):
        sumar(out, panear(fm_campana(mtof(m), 1.0, 0.8, 1.0, 0.35) * 0.6, -0.3 + 0.2 * i), 0.13 * i)
    sumar(out, s_pop(1.3), 0.0)
    return out / (np.abs(out).max() + 1e-9) * 0.8


def s_match(**k):
    out = np.zeros((2, int(1.5 * SR)))
    sumar(out, panear(fm_campana(mtof(79), 1.0, 1.5, 2.0, 0.35), -0.2), 0.0)
    sumar(out, panear(fm_campana(mtof(86), 1.2, 1.5, 2.0, 0.45), 0.2), 0.12)
    sumar(out, s_brillo(1.1) * 0.5, 0.1)
    return out / (np.abs(out).max() + 1e-9) * 0.85


def s_pin(**k):
    d = 0.35
    x = glide(1600, 420, d, 0.8) * env_exp(d, 0.2, 0.005)
    t = _t(0.1)
    th = butter_lp(ruido(len(t), 21), 500, 2) * np.exp(-t * 40)
    out = np.zeros(int(0.5 * SR))
    out[:len(x)] += x * 0.6
    i = int(0.3 * SR)
    out[i:i + len(th)] += th
    return nrm(out) * 0.7


def s_fuego(dur=3.0, **k):
    d = max(0.5, dur)
    t = _t(d)
    rumor = butter_lp(ruido(len(t), 22), 220, 2) * 0.6
    cr = np.zeros(len(t))
    rng = np.random.default_rng(23)
    for _ in range(int(d * 18)):
        i = rng.integers(0, len(t) - 400)
        cr[i:i + 300] += hp(ruido(300, int(i)), 2000) * np.exp(-np.arange(300) / 40) * rng.uniform(0.3, 1)
    fade = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.8)
    return nrm((rumor + cr) * fade) * 0.6


def s_campana(tono=1.0, **k):
    return nrm(fm_campana(660 * tono, 3.0, 1.4, 1.41, 1.1) + fm_campana(1320 * tono, 3.0, 0.8, 2.0, 0.6) * 0.25) * 0.7


def s_arena(dur=1.2, **k):
    d = max(0.3, dur)
    t = _t(d)
    x = hp(ruido(len(t), 24), 4500) * (np.random.default_rng(25).random(len(t)) < 0.02) * 3
    x = butter_lp(x, 9000, 1) * np.sin(np.pi * t / d)
    return nrm(x) * 0.5


def s_morph(**k):
    d = 0.7
    t = _t(d)
    f = 200 * (1 + 3 * t / d) * (1 + 0.1 * np.sin(2 * np.pi * 18 * t))
    x = svf(sierra(f), 400 + 3500 * np.sin(np.pi * t / d), 3, 0) * np.sin(np.pi * t / d)
    return nrm(np.stack([x, x]) * 0.7 + s_whoosh(d, 1.2) * 0.5)


def s_zap(**k):
    d = 0.3
    x = glide(2600, 280, d, 0.5) * env_exp(d, 0.12)
    return nrm(x + np.roll(x, 480) * 0.4)


def s_puf(**k):
    d = 0.5
    t = _t(d)
    x = butter_lp(ruido(len(t), 26), 1500, 2) * np.exp(-t * 9) * np.minimum(1, t / 0.005)
    return nrm(x + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18) * 0.6)


# --- transiciones
def s_escribir(dur=1.0, **k):
    d = dur
    t = _t(d)
    zig = np.abs(np.sin(2 * np.pi * 7 * t)) ** 0.5
    x = bp(ruido(len(t), 27), 2600 + 900 * np.sin(2 * np.pi * 7 * t), 1.5) * zig * np.minimum(1, (d - t) / 0.1)
    return nrm(x) * 0.7


def s_splat(**k):
    d = 0.5
    t = _t(d)
    x = butter_lp(ruido(len(t), 28), 1300, 2) * np.exp(-t * 10) + np.sin(2 * np.pi * np.cumsum(120 - 60 * t) / SR) * np.exp(-t * 12)
    sq = svf(ruido(len(t), 29), 1800 * np.exp(-t * 5) + 200, 4, 1) * np.exp(-t * 6)
    return nrm(x + sq * 0.6)


def s_espiral_zap(dur=0.85, **k):
    d = dur
    t = _t(d)
    f = 1800 * np.exp(-t * 2.5) * (1 + 0.3 * np.sin(2 * np.pi * (4 + 20 * t) * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)
    return nrm(np.stack([x, x]) * 0.6 + s_whoosh(d) * 0.6)


def s_glitch(dur=0.7, **k):
    rng = np.random.default_rng(31)
    out = np.zeros(int(dur * SR))
    i = 0
    while i < len(out):
        n = int(rng.uniform(0.02, 0.07) * SR)
        f = rng.choice([220, 330, 440, 880, 1760, 110])
        seg = cuadrada(np.full(n, float(f)), rng.uniform(0.1, 0.5)) * (rng.random() > 0.25)
        seg = np.round(seg * 4) / 4
        out[i:i + n] += seg[:len(out) - i] * 0.5
        i += n
    return nrm(out) * 0.6


def s_zoom_whoosh(dur=0.9, **k):
    d = dur
    t = _t(d)
    x = svf(ruido(len(t), 32), 200 + 7000 * (t / d) ** 2, 2, 1) * (t / d) ** 1.5
    out = np.stack([x, x])
    imp = s_impacto(1.2)
    res = np.zeros((2, len(t) + len(imp)))
    res[:, :len(t)] += out
    res[:, len(t) - 200:len(t) - 200 + len(imp)] += np.stack([imp, imp])[:, :res.shape[1] - (len(t) - 200)] * 0.6
    return res / (np.abs(res).max() + 1e-9) * 0.85


def s_persianas(**k):
    out = np.zeros(int(0.8 * SR))
    for j in range(7):
        t = _t(0.05)
        c = bp(ruido(len(t), 40 + j), 1800 + 150 * j, 3) * np.exp(-t * 120)
        i = int(j * 0.075 * SR)
        out[i:i + len(c)] += c
    return nrm(out) * 0.7


def s_cinta_lenta(dur=1.0, **k):
    d = dur
    t = _t(d)
    f = 440 * (1 - 0.85 * (t / d) ** 1.3)
    x = sum(sierra(f * r) for r in (1, 1.26, 1.5)) / 3
    x = lp(x, 300 + 3000 * (1 - t / d)) * (1 - t / d) ** 0.5
    return nrm(x) * 0.7


def s_ola(dur=0.85, **k):
    d = dur + 0.4
    t = _t(d)
    x = svf(ruido(len(t), 33), 500 + 1200 * np.sin(np.pi * t / d), 1.0, 1) * np.sin(np.pi * t / d) ** 1.2
    esp = hp(ruido(len(t), 34), 5000) * np.sin(np.pi * t / d) ** 3 * 0.3
    return nrm(np.stack([x + esp, np.roll(x, 300) + esp]))


def s_burbujas(dur=0.9, **k):
    out = np.zeros((2, int((dur + 0.2) * SR)))
    rng = np.random.default_rng(35)
    for j in range(22):
        b = s_pop(rng.uniform(0.7, 1.8)) * 0.6
        sumar(out, panear(b, rng.uniform(-0.9, 0.9)), rng.uniform(0, dur))
    return out / (np.abs(out).max() + 1e-9) * 0.75


def s_iris(dur=1.0, **k):
    d = dur
    x = glide(900, 250, d / 2) * env_exp(d / 2, 0.3, 0.02)
    y = glide(250, 700, d / 2) * env_exp(d / 2, 0.3, 0.02)
    return nrm(np.concatenate([x, y])) * 0.5


def s_brillo_caleido(dur=0.95, **k):
    out = np.zeros((2, int((dur + 1.0) * SR)))
    for i, m in enumerate((72, 76, 79, 83, 86, 88, 91, 95)):
        sumar(out, panear(fm_campana(mtof(m), 1.0, 1.2, 1.0, 0.3) * 0.5, math.sin(i * 1.3)), i * dur / 8)
    return out / (np.abs(out).max() + 1e-9) * 0.8


# ---- sonidos "documental" (estilo Kurzgesagt): suaves, con mucho aire
def s_apagon(dur=1.8, **k):
    """Algo enorme que se apaga: barrido grave descendente + golpe sordo."""
    d = max(0.8, dur)
    t = _t(d)
    f = 30 + 190 * np.exp(-t * 2.6)
    x = lp(sierra(f) * 0.6 + np.sin(2 * np.pi * np.cumsum(f * 0.5) / SR), 300 + 1800 * np.exp(-t * 3), 1.2)
    golpe = np.sin(2 * np.pi * np.cumsum(55 + 60 * np.exp(-t * 25)) / SR) * np.exp(-t * 5)
    x = (x * np.minimum(1, t / 0.01) * np.exp(-t * 1.6) + golpe * 0.8)
    return nrm(np.stack([x, np.roll(x, 220)])) * 0.85


def s_suspiro(dur=0.9, **k):
    """Soplo de aire muy suave (transiciones de documental)."""
    d = max(0.3, dur)
    t = _t(d)
    u = t / d
    x = svf(ruido(len(t), 23), 500 + 1400 * np.sin(np.pi * u), 0.9, 1) * np.sin(np.pi * u) ** 2.5
    pan = -0.5 + u
    return np.stack([x * np.cos((pan + 1) * np.pi / 4), x * np.sin((pan + 1) * np.pi / 4)]) * 0.5 / (np.abs(x).max() + 1e-9)


def s_hielo(dur=1.0, **k):
    """Crujidos de hielo que se forma."""
    d = max(0.4, dur)
    n = int(d * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(29)
    for _ in range(int(14 * d)):
        i = int(rng.random() * (n - 3000))
        L = int(SR * (0.004 + 0.02 * rng.random()))
        tt = np.arange(L) / SR
        out[i:i + L] += bp(ruido(L, int(rng.random() * 999)), 2500 + 4000 * rng.random(), 3) * np.exp(-tt * 250) * rng.random()
    t = _t(d)
    creak = lp(sierra(np.full(n, 70.0) * (1 + 0.1 * np.sin(2 * np.pi * 3 * t))), 500) * np.sin(np.pi * t / d) * 0.15
    return nrm(out + creak) * 0.7


def s_pio(tono=1.0, **k):
    """Pío de pajarito (dos notas rápidas)."""
    out = np.zeros(int(0.35 * SR))
    for j, (f0, f1) in enumerate(((2400, 3600), (2700, 4200))):
        g = glide(f0 * tono, f1 * tono, 0.07, 0.7) * env_exp(0.07, 0.03, 0.004)
        i = int(j * 0.11 * SR)
        out[i:i + len(g)] += g
    return nrm(out) * 0.6


def s_burbuja(tono=1.0, **k):
    d = 0.14
    return nrm(glide(500 * tono, 1500 * tono, d, 2.0) * env_exp(d, 0.05, 0.003)) * 0.5


def s_amanecer(dur=2.5, **k):
    """Acorde cálido que crece (salida del sol)."""
    d = max(1.0, dur)
    t = _t(d + 1.0)
    x = np.zeros(len(t))
    for m in (55, 62, 67, 71, 74):
        f = mtof(m)
        x += np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t + 1)
    env = np.clip(t / d, 0, 1) ** 2 * np.exp(-np.clip(t - d, 0, None) * 3)
    x = lp(x * env, 2500)
    return nrm(np.stack([x, np.roll(x, 300)])) * 0.55


BIB = {k[2:]: v for k, v in globals().items() if k.startswith("s_")}
TRANS_SFX = dict(garabato="escribir", mancha="splat", espiral="espiral_zap", glitch="glitch", zoom="zoom_whoosh",
                 persianas="persianas", derretir="cinta_lenta", ola="ola", burbujas="burbujas", iris="iris",
                 caleido="brillo_caleido", pixeles="glitch", fundido="suspiro", zoom_suave="suspiro",
                 bajada="suspiro", continua=None)


def eventos():
    import escenas as S
    tl = json.load(open("timeline.json", encoding="utf-8"))
    clases = S.CLASES
    evs = []
    for i, e in enumerate(tl["escenas"]):
        evs += clases[e["id"]](e, i).sfx
    for tr in tl["transiciones"]:
        if not TRANS_SFX.get(tr["tipo"]):
            continue
        evs.append(dict(t=tr["t0"], nombre=TRANS_SFX[tr["tipo"]], vol=0.7, pan=0.0, dur=round(tr["t1"] - tr["t0"], 3)))
    return sorted(evs, key=lambda x: x["t"])


def main():
    os.makedirs("audio", exist_ok=True)
    evs = eventos()
    faltan = sorted({e["nombre"] for e in evs} - set(BIB))
    assert not faltan, f"SFX sin sintetizar: {faltan}"
    buf = np.zeros((2, N))
    cache = {}
    for e in evs:
        params = {k: v for k, v in e.items() if k in ("tono", "dur")}
        key = (e["nombre"], tuple(sorted(params.items())))
        if key not in cache:
            x = BIB[e["nombre"]](**params)
            cache[key] = x.astype(np.float64)
        x = cache[key]
        if x.ndim == 1:
            x = panear(x, e.get("pan", 0.0))
        elif e.get("pan", 0.0):
            p = e["pan"]
            x = np.stack([x[0] * min(1, 1 - p), x[1] * min(1, 1 + p)])
        sumar(buf, x, e["t"], e.get("vol", 1.0))
    buf = butter_hp(buf, 40, 2)
    buf = reverb(buf, 0.12, 1.2, 7000)
    pico = np.abs(buf).max()
    sf.write("audio/sfx.wav", (buf / pico * 0.9).T.astype(np.float32), SR, subtype="FLOAT")
    json.dump(evs, open("audio/sfx_eventos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"{len(evs)} eventos, {len(cache)} sonidos distintos, pico previo {pico:.2f}")


if __name__ == "__main__":
    main()
