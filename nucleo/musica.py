# -*- coding: utf-8 -*-
"""Compositor procedural: una sección musical por escena, en la misma rejilla (BPM) que la animación.
Salida: audio/musica_stems.npz (buses) y audio/musica.wav (mezcla de música)."""
import math
import os

import numpy as np
import soundfile as sf
from numba import njit

import config
import ritmo as R
from sinte import (SR, adsr, bp, butter_hp, butter_lp, compresor, cuadrada, delay_pingpong, hp, lp, mtof, panear,
                   perc, reverb, ruido, saturar, seno, sierra, sumar, supersaw, svf)

TL = R.TL
BEAT = R.BEAT
PASO = R.PASO
TOTAL = TL["total"]
N = int((TOTAL + 0.5) * SR)

MODOS = {
    "dorico": [0, 2, 3, 5, 7, 9, 10], "frigio": [0, 1, 3, 5, 7, 8, 10], "menor": [0, 2, 3, 5, 7, 8, 10],
    "mixolidio": [0, 2, 4, 5, 7, 9, 10], "lidio": [0, 2, 4, 6, 7, 9, 11],
}
# progresión (grados) y beats por acorde
PROG = {
    "build": ([0, 6, 3, 0], 4), "acid": ([0, 6, 3, 0], 4), "funk": ([0, 6, 3, 0], 4), "flauta": ([0, 1, 0, 6], 4),
    "epico": ([0, 5, 2, 6], 4), "brillo": ([0, 1, 0, 1], 4), "disco": ([0, 3, 0, 4], 4), "reloj": ([0, 3, 4, 0], 4),
    "dub": ([0, 6, 3, 0], 4), "lounge": ([0, 3, 0, 3], 4), "ambiente": ([0, 5, 3, 4], 8), "final": ([0, 6, 3, 0], 4),
    "espacio": ([0, 1, 5, 4], 8), "tension": ([0, 5, 0, 6], 8), "vacio": ([0, 1, 0, 5], 8),
    "esperanza": ([0, 1, 5, 4], 8),
}
SUAVES = config.SUAVES


def grado(raiz, modo, g, octava=0):
    esc = MODOS[modo]
    return raiz + esc[g % 7] + 12 * (g // 7 + octava)


def acorde(raiz, modo, g, septima=False):
    notas = [grado(raiz, modo, g), grado(raiz, modo, g + 2), grado(raiz, modo, g + 4)]
    if septima:
        notas.append(grado(raiz, modo, g + 6))
    return notas


# ------------------------------------------------------------ instrumentos
def bombo(vel=1.0):
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t * 30) + 60 * np.exp(-t * 180)
    cuerpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = hp(ruido(n, 1) * np.exp(-t * 700), 2500) * 0.35
    return saturar(cuerpo + click, 1.4) * vel


def caja(vel=1.0, seed=2):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    tono = np.sin(2 * np.pi * 186 * t) * np.exp(-t * 22) + 0.5 * np.sin(2 * np.pi * 332 * t) * np.exp(-t * 28)
    nz = bp(ruido(n, seed), 2600, 0.7) * np.exp(-t * 13) + 0.5 * hp(ruido(n, seed + 1), 6500) * np.exp(-t * 26)
    return (0.55 * tono + 1.1 * nz) * vel


def palmada(vel=1.0, seed=3):
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    env = np.zeros(n)
    for k, d in enumerate((0.0, 0.011, 0.023)):
        i = int(d * SR)
        env[i:] += np.exp(-(t[:n - i]) * (160 if k < 2 else 11))
    return bp(ruido(n, seed), 1400, 1.2) * env * 1.6 * vel


_METAL = [205.3, 304.4, 369.6, 522.7, 540.0, 800.0]


def metal(n, seed=0):
    x = np.zeros(n)
    for f in _METAL:
        x += cuadrada(np.full(n, f * 1.7), 0.5, (seed * 0.137 + f) % 1)
    return x


def charles(abierto=False, vel=1.0, seed=4):
    n = int((0.45 if abierto else 0.08) * SR)
    t = np.arange(n) / SR
    x = hp(bp(metal(n, seed) * 0.4 + ruido(n, seed) * 0.6, 10000, 0.8), 7000)
    return x * np.exp(-t * (7 if abierto else 55)) * 0.55 * vel


def platillo(vel=1.0, seed=5):
    n = int(2.4 * SR)
    t = np.arange(n) / SR
    x = hp(metal(n, seed) * 0.3 + ruido(n, seed), 4500) * (np.exp(-t * 1.9) * 0.8 + np.exp(-t * 12) * 0.4)
    return np.stack([x, np.roll(x, 137)]) * 0.45 * vel


def maraca(vel=1.0, seed=6):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    return bp(ruido(n, seed), 6500, 1.5) * np.minimum(1, t / 0.006) * np.exp(-t * 45) * 0.5 * vel


def bloque_madera(vel=1.0, f=1400):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 60) + 0.4 * bp(ruido(n, 7), f * 1.5, 6) * np.exp(-t * 80)) * vel


def bajo_acid(midi, dur, acento=0.0, desde=None, brillo=1.0):
    n = int((dur + 0.08) * SR)
    t = np.arange(n) / SR
    f = np.full(n, mtof(midi))
    if desde is not None:
        g = np.clip(t / 0.06, 0, 1)
        f = mtof(desde) * (1 - g) + mtof(midi) * g
    osc = sierra(f)
    ef = np.exp(-t / (0.09 + 0.12 * acento))
    fc = 160 + (900 + 2600 * acento) * brillo * ef
    y = svf(osc, fc, 3.5 + 5 * acento, 0)
    amp = adsr(n, 0.003, 0.2, 0.7, 0.03, dur)
    return saturar(y * amp * (0.8 + 0.4 * acento), 2.2) * 0.6


def bajo_sub(midi, dur, vel=1.0):
    n = int((dur + 0.1) * SR)
    f = mtof(midi)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) + 0.15 * np.sin(4 * np.pi * f * t)
    return y * adsr(n, 0.005, 0.3, 0.85, 0.06, dur) * 0.7 * vel


def bajo_pluck(midi, dur, vel=1.0):
    n = int((dur + 0.08) * SR)
    t = np.arange(n) / SR
    osc = sierra(np.full(n, mtof(midi))) * 0.6 + cuadrada(np.full(n, mtof(midi)), 0.5) * 0.4
    y = lp(osc, 250 + 1500 * np.exp(-t * 18), 1.4)
    return saturar(y * adsr(n, 0.002, 0.15, 0.6, 0.04, dur) * vel, 1.6) * 0.55


def pad(notas, dur, brillo=1800.0, seed=0, ataque=0.25, lfo=0.25):
    n = int((dur + 0.7) * SR)
    t = np.arange(n) / SR
    acc = np.zeros((2, n))
    for k, m in enumerate(notas):
        acc += supersaw(mtof(m), n, 7, 0.22, seed + k)
    fc = brillo * (1 + 0.35 * np.sin(2 * np.pi * lfo * t + seed))
    y = np.stack([lp(acc[0], fc, 0.9), lp(acc[1], fc, 0.9)])
    return y * adsr(n, ataque, 0.6, 0.8, 0.5, dur) * 0.22


def pad_suave(notas, dur, seed=0):
    n = int((dur + 1.5) * SR)
    t = np.arange(n) / SR
    acc = np.zeros((2, n))
    for k, m in enumerate(notas):
        f = mtof(m)
        for d, pan in ((-0.003, -0.6), (0.003, 0.6)):
            v = np.sin(2 * np.pi * f * (1 + d) * t) + 0.3 * np.sin(4 * np.pi * f * (1 + d) * t + 1)
            acc += panear(v, pan)
    return acc * adsr(n, 1.2, 1.0, 0.8, 1.3, dur) * 0.12


def arp_nota(midi, dur, brillo=2500.0, pw=0.3):
    n = int((dur + 0.06) * SR)
    t = np.arange(n) / SR
    osc = cuadrada(np.full(n, mtof(midi)), pw)
    y = lp(osc, 300 + brillo * np.exp(-t * 20), 1.8)
    return y * adsr(n, 0.002, 0.1, 0.4, 0.05, dur) * 0.28


def campana(midi, dur=1.4, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = mtof(midi)
    idx = 3.5 * np.exp(-t * 6)
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t))
    return y * np.exp(-t * 3.2) * np.minimum(1, t / 0.002) * 0.35 * vel


def rhodes(midi, dur, vel=1.0):
    n = int((dur + 0.6) * SR)
    t = np.arange(n) / SR
    f = mtof(midi)
    idx = 1.6 * np.exp(-t * 4) + 0.3
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    trem = 1 + 0.18 * np.sin(2 * np.pi * 4.5 * t)
    return y * trem * adsr(n, 0.004, 1.2, 0.5, 0.4, dur) * 0.25 * vel


def flauta(midi, dur, vel=1.0, seed=0):
    n = int((dur + 0.2) * SR)
    t = np.arange(n) / SR
    f0 = mtof(midi)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.3 * t) * np.clip(t / 0.3, 0, 1)
    f = f0 * vib
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.12 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    aire = bp(ruido(n, seed), f0 * 1.02, 4) * 0.35
    env = adsr(n, 0.06, 0.2, 0.85, 0.12, dur)
    return (y + aire) * env * 0.32 * vel


def metales(notas, dur):
    n = int((dur + 0.2) * SR)
    t = np.arange(n) / SR
    acc = np.zeros((2, n))
    for k, m in enumerate(notas):
        acc += supersaw(mtof(m), n, 5, 0.12, 30 + k)
    fc = 400 + 3500 * np.exp(-t * 8)
    y = np.stack([lp(acc[0], fc, 1.1), lp(acc[1], fc, 1.1)])
    return saturar(y * adsr(n, 0.01, 0.3, 0.5, 0.15, dur) * 0.35, 1.5)


def acorde_corto(notas, dur=0.12):
    n = int((dur + 0.1) * SR)
    t = np.arange(n) / SR
    acc = np.zeros(n)
    for m in notas:
        acc += cuadrada(np.full(n, mtof(m)), 0.4)
    y = bp(acc, 1400, 0.9)
    return y * adsr(n, 0.002, 0.05, 0.3, 0.05, dur) * 0.22


def subida(dur, seed=0):
    """Riser de ruido filtrado (termina en el tiempo fuerte)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    u = t / dur
    x = ruido(n, seed)
    fc = 400 + 9000 * u ** 2
    y = svf(x, fc, 2.5, 1)
    return np.stack([y, np.roll(y, 97)]) * (u ** 2) * 0.35


@njit(cache=True)
def _flanger(x, lfo_ms, sr):
    n = x.shape[0]
    out = np.empty(n)
    for i in range(n):
        d = lfo_ms[i] * sr / 1000.0
        j = i - d
        j0 = int(math.floor(j))
        fr = j - j0
        if j0 < 0:
            out[i] = x[i]
        else:
            out[i] = 0.6 * x[i] + 0.4 * (x[j0] * (1 - fr) + x[min(j0 + 1, n - 1)] * fr)
    return out


def flanger(x, rate=0.12, depth_ms=3.0):
    t = np.arange(x.shape[1]) / SR
    out = np.empty_like(x)
    for c in range(2):
        lfo = 1.0 + depth_ms * (0.5 + 0.5 * np.sin(2 * np.pi * rate * t + c * 1.7))
        out[c] = _flanger(np.ascontiguousarray(x[c]), lfo, float(SR))
    return out


# ------------------------------------------------------------ composición por escena
def componer():
    B = {k: np.zeros((2, N)) for k in ("bateria", "bajo", "pad", "arp", "lead", "fx")}
    rng = np.random.default_rng(7)
    for e in TL["escenas"]:
        est = R.ESTILO[e["id"]]
        sab, modo, raiz = est["sabor"], est["modo"], est["raiz"]
        prog_, bpc = PROG[sab]
        t0, t1 = e["t0"], e["t1"]
        fin_musica = t1
        primera, ultima = e["id"] == config.PRIMERA, e["id"] == config.ULTIMA
        if ultima:
            fin_musica = e["frases"][-1]["t1"] + 0.12   # golpe final
        nst = int(round((fin_musica - t0) / PASO))
        pat = R.PATRONES[R.ESTILO[e["id"]]["bombo"]]
        inicio_bombo = t0
        if primera:
            inicio_bombo = R.BOMBOS[0] if len(R.BOMBOS) else t0
        cambio = [k for k in range(nst)]
        print(f"  {e['id']:10s} {sab:9s} {modo:9s} {nst} pasos")
        for k in range(nst):
            t = t0 + k * PASO
            paso = k % 16
            ci = (k // (4 * bpc)) % len(prog_)
            g = prog_[ci]
            notas = acorde(raiz + 12, modo, g, septima=sab in ("lounge", "ambiente", "brillo", "espacio", "esperanza"))
            nuevo_acorde = k % (4 * bpc) == 0
            u_sec = k / max(1, nst - 1)
            bateria = sab not in SUAVES and t >= inicio_bombo - 1e-6
            # --- bombo (coincide con ritmo.BOMBOS)
            if bateria and paso in pat:
                sumar(B["bateria"], bombo(1.0), t)
            # --- caja / palmas
            if bateria and sab not in ("lounge",):
                if sab == "epico":
                    if paso == 8:
                        sumar(B["bateria"], caja(1.0), t, 0.9)
                elif sab == "dub":
                    if paso == 8:
                        sumar(B["bateria"], caja(0.8, seed=k), t, 0.8)
                elif paso in (4, 12) and not (primera and t < 6.0):
                    sumar(B["bateria"], palmada(1.0, seed=k) if sab in ("acid", "disco", "final", "build") else caja(1.0, seed=k), t, 0.75)
            if bateria and sab == "lounge" and paso in (4, 12):
                sumar(B["bateria"], bloque_madera(0.5, 900), t, 0.6)
            # --- charles
            if bateria and not (primera and t < 9.5):
                if sab in ("disco", "final", "acid") and paso in (2, 6, 10, 14):
                    sumar(B["bateria"], panear(charles(True, 0.8, seed=k), 0.25), t)
                elif sab in ("funk", "reloj", "brillo", "flauta", "build", "acid", "final", "disco", "epico") and paso % 2 == 0:
                    sumar(B["bateria"], panear(charles(False, 0.9 if paso % 4 == 2 else 0.55, seed=k), 0.3), t)
                if sab in ("funk", "dub", "lounge", "flauta") and paso % 2 == 1:
                    sumar(B["bateria"], panear(maraca(0.7, seed=k), -0.35), t)
            if sab == "reloj" and paso % 2 == 0:
                sumar(B["bateria"], panear(bloque_madera(0.55, 1500 if paso % 4 == 0 else 1100), -0.2), t)
            # --- bajo
            r = grado(raiz, modo, g, -1)
            if sab in ("acid", "final") or (sab == "build" and t >= inicio_bombo):
                patron = [0, 0, 12, 0, 7, 0, 12, 10, 0, 0, 12, 0, 3, 7, 12, 15]
                if rng.random() < 0.88 or paso % 4 == 0:
                    acento = 1.0 if paso in (0, 6, 10, 14) else 0.2
                    desde = r + patron[(paso - 1) % 16] if paso in (7, 15) else None
                    brillo = 0.4 + 0.6 * u_sec if sab == "build" else 1.0
                    sumar(B["bajo"], bajo_acid(r + patron[paso], PASO * 0.9, acento, desde, brillo), t)
            elif sab == "funk":
                if paso in (0, 3, 6, 8, 10, 11, 14):
                    off = {0: 0, 3: 12, 6: 7, 8: 0, 10: 12, 11: 10, 14: 7}[paso]
                    sumar(B["bajo"], bajo_pluck(r + off, PASO * 1.5), t)
            elif sab == "disco":
                if paso % 2 == 0:
                    sumar(B["bajo"], bajo_pluck(r + (12 if paso % 4 == 2 else 0), PASO * 1.6, 1.0), t)
            elif sab in ("dub",):
                if paso in (0, 6, 10):
                    sumar(B["bajo"], bajo_sub(r, PASO * (5 if paso == 0 else 3)), t)
            elif sab == "epico":
                if paso % 2 == 0:
                    sumar(B["bajo"], bajo_pluck(r, PASO * 1.8, 0.9), t)
            elif sab == "lounge":
                if paso % 4 == 0:
                    camino = [0, 7, 12, 10]
                    sumar(B["bajo"], bajo_sub(r + camino[(paso // 4)], BEAT * 0.9, 0.9), t)
            elif sab in ("flauta", "reloj", "brillo"):
                if paso % 4 == 0 or (sab == "reloj" and paso % 2 == 0):
                    sumar(B["bajo"], bajo_pluck(r, PASO * 1.8, 0.85), t)
            elif sab == "ambiente" and nuevo_acorde:
                sumar(B["bajo"], bajo_sub(r, PASO * 4 * bpc, 0.6), t)
            elif sab in ("espacio", "vacio") and nuevo_acorde:
                sumar(B["bajo"], bajo_sub(r, PASO * 4 * bpc, 0.55), t)
            elif sab == "tension" and paso in (0, 3):          # latido grave: pum-pum
                sumar(B["bajo"], bajo_sub(r, PASO * 1.6, 0.75 if paso == 0 else 0.5), t)
            elif sab == "esperanza" and paso in (0, 6, 8, 14):
                sumar(B["bajo"], bajo_pluck(r + (12 if paso == 14 else 0), PASO * 2.5, 0.6), t)
            # --- pads / acordes
            dur_ac = min(PASO * 4 * bpc, fin_musica - t)
            if nuevo_acorde and dur_ac > 0.05:
                if sab == "ambiente":
                    sumar(B["pad"], pad_suave(notas, dur_ac, seed=k), t)
                elif sab in ("espacio", "tension", "vacio", "esperanza"):
                    graves = [n - 12 for n in notas] if sab in ("tension", "vacio") else notas
                    sumar(B["pad"], pad_suave(graves, dur_ac, seed=k), t, 1.3)
                    br = dict(espacio=1100, tension=700, vacio=520, esperanza=1700)[sab]
                    sumar(B["pad"], pad(graves, dur_ac, br, seed=k, ataque=1.4, lfo=0.12), t, 0.55)
                elif sab == "lounge":
                    for m in notas:
                        sumar(B["pad"], panear(rhodes(m, BEAT * 1.5), -0.2), t)
                        sumar(B["pad"], panear(rhodes(m, BEAT * 1.2, 0.7), 0.2), t + BEAT * 1.5)
                elif sab == "epico":
                    sumar(B["pad"], metales(notas, BEAT * 1.5), t)
                    sumar(B["pad"], pad(notas, dur_ac, 1400, seed=k), t, 0.6)
                else:
                    brillo = 700 + 2500 * u_sec if sab == "build" else (2200 if sab in ("final", "disco") else 1600)
                    sumar(B["pad"], pad(notas, dur_ac, brillo, seed=k), t, 0.9 if sab != "dub" else 0.5)
            if sab == "dub" and paso in (4, 12):
                sumar(B["arp"], panear(acorde_corto(notas), 0.3), t)
            if sab == "epico" and paso in (6, 14):
                sumar(B["pad"], metales(notas, PASO * 1.5), t, 0.7)
            # --- arpegios
            if sab in ("build", "acid", "final", "disco") and (sab != "build" or t > 5.5):
                tonos = notas + [n + 12 for n in notas]
                sec = tonos + tonos[-2:0:-1]
                m = sec[k % len(sec)] + 12
                br = 900 + 3000 * u_sec if sab == "build" else 2600
                sumar(B["arp"], panear(arp_nota(m, PASO * 0.8, br), 0.4 * math.sin(k * 0.7)), t, 0.8 if sab != "disco" else 0.6)
            if sab == "brillo" and paso % 2 == 0:
                tonos = notas + [n + 12 for n in notas]
                m = tonos[(k // 2) % len(tonos)] + 12
                sumar(B["arp"], panear(campana(m, 1.2), 0.5 * math.sin(k * 0.9)), t, 0.8)
            if sab == "reloj" and paso % 4 == 2:
                sumar(B["arp"], panear(arp_nota(notas[(k // 4) % 3] + 24, PASO * 0.6, 1800, 0.5), 0.3), t, 0.6)
            if sab in ("espacio", "esperanza") and paso % 2 == 0:          # celesta en corcheas
                tonos = notas + [n + 12 for n in notas]
                sec = tonos + tonos[-2:0:-1]
                m = sec[(k // 2) % len(sec)] + 12
                v = (0.32 if sab == "espacio" else 0.42) * (0.7 + 0.3 * (paso % 8 == 0))
                sumar(B["arp"], panear(campana(m, 1.6, v), 0.45 * math.sin(k * 0.37)), t)
            if sab == "tension" and paso % 4 == 0:                        # reloj: tic-tac
                sumar(B["arp"], panear(bloque_madera(0.28, 1900 if paso % 8 == 0 else 1500), 0.25), t)
            if sab == "tension" and paso == 8 and (k // 16) % 2 == 1:
                sumar(B["arp"], panear(campana(notas[0] + 24, 2.2, 0.35), -0.3), t)
            if sab == "vacio" and paso == 0 and (k // 16) % 2 == 0:
                sumar(B["arp"], panear(campana(notas[(k // 32) % 3] + 24, 3.0, 0.3), 0.4 * math.sin(k)), t)
            if sab == "ambiente" and paso in (0, 10) and (k // 16) % 2 == 0:
                sumar(B["arp"], panear(campana(notas[(k // 16) % 3] + 24, 2.5, 0.5), -0.3 + 0.6 * ((k // 16) % 2)), t, 0.6)
            # --- flauta (escena música)
        if sab == "flauta":
            frase = [(0, 2), (2, 1), (3, 1), (4, 2), (3, 1), (2, 1), (0, 4), (4, 2), (5, 1), (4, 1), (2, 2), (1, 2), (0, 4)]
            tt = t0 + 4 * BEAT
            i = 0
            while tt < fin_musica - 0.5:
                gd, durb = frase[i % len(frase)]
                d = durb * BEAT / 2
                sumar(B["lead"], panear(flauta(grado(raiz, modo, gd, 2), d * 0.95, 1.0, seed=i), 0.1), tt)
                tt += d
                i += 1
        # --- transición: subida + platillo en el "uno" de la escena siguiente
        if not ultima:
            dur_sub = 2 * BEAT
            sumar(B["fx"], subida(dur_sub, seed=int(t1)), t1 - dur_sub,
                  0.8 if sab not in SUAVES else (0.5 if sab == "ambiente" else 0.4))
        if not primera:
            sumar(B["fx"], platillo(0.9 if sab not in SUAVES else (0.45 if sab == "ambiente" else 0.35), seed=int(t0)), t0)
        # redoble antes del cambio (estilos con batería)
        if sab not in SUAVES + ("lounge",) and not ultima:
            for j in range(8):
                tt = t1 - BEAT + j * PASO / 2
                sumar(B["bateria"], caja(0.35 + 0.08 * j, seed=j), tt, 0.6)
    # golpe final
    fin = TL["escenas"][-1]["frases"][-1]["t1"] + 0.12
    est = R.ESTILO[config.ULTIMA]
    notas = acorde(est["raiz"] + 12, est["modo"], 0)
    if est["sabor"] in SUAVES and est["sabor"] != "ambiente":     # cierre documental: acorde que florece + campanas, sin golpe
        sumar(B["pad"], pad_suave(notas + [notas[0] + 12], 2.6, seed=77), fin - 0.3, 1.6)
        sumar(B["pad"], pad(notas + [notas[0] + 12], 2.8, 1800, seed=77, ataque=0.3), fin - 0.3, 0.9)
        for j, m in enumerate(notas + [notas[0] + 12]):
            sumar(B["arp"], panear(campana(m + 24, 2.8, 0.45), -0.4 + 0.27 * j), fin + 0.09 * j)
        sumar(B["bajo"], bajo_sub(grado(est["raiz"], est["modo"], 0, -1), 2.5, 0.9), fin)
        return B
    sumar(B["bateria"], bombo(1.2), fin)
    sumar(B["fx"], platillo(1.2, seed=99), fin)
    sumar(B["pad"], pad(notas + [notas[0] + 12], 2.8, 2600, seed=77, ataque=0.01), fin, 1.2)
    sumar(B["bajo"], bajo_sub(grado(est["raiz"], est["modo"], 0, -1), 2.5, 1.2), fin)
    return B


def bombeo():
    """Curva de 'pump' (sidechain) sincronizada a los bombos."""
    g = np.ones(N)
    t = np.arange(N) / SR
    for tb in R.BOMBOS:
        i0 = int(tb * SR)
        i1 = min(N, i0 + int(0.35 * SR))
        tt = t[i0:i1] - tb
        g[i0:i1] = np.minimum(g[i0:i1], 1 - 0.55 * np.exp(-tt / 0.09))
    return g


def nivelar(x):
    """Iguala la sonoridad de cada sección (rampas de 0.3 s en las fronteras), quita DC y suaviza agudos."""
    import pyloudnorm as pyln
    from sinte import shelf
    x = butter_hp(x, 25, 2)
    x = shelf(x, 7000, -2.5, alto=True)
    m = pyln.Meter(SR)
    objetivo = {i: -21.0 for i, m in R.ESTILO.items() if m["sabor"] == "ambiente"}
    objetivo.update({i: -19.5 for i, m in R.ESTILO.items() if m["sabor"] in SUAVES and m["sabor"] != "ambiente"})
    objetivo[config.PRIMERA] = -18.0
    g = np.ones(x.shape[1])
    puntos = []
    for e in TL["escenas"]:
        a, b = int(e["t0"] * SR), int(min(e["t1"], TOTAL) * SR)
        lufs = m.integrated_loudness(x[:, a:b].T)
        db = objetivo.get(e["id"], -17.5) - lufs
        puntos.append((e["t0"], e["t1"], 10 ** (db / 20)))
        print(f"    {e['id']:10s} {lufs:6.1f} LUFS -> ganancia {db:+5.1f} dB")
    t = np.arange(x.shape[1]) / SR
    g[:] = puntos[0][2]
    for (a0, a1, ga), (b0, b1, gb) in zip(puntos[:-1], puntos[1:]):
        u = np.clip((t - (b0 - 0.15)) / 0.3, 0, 1)
        g = np.where(t >= b0 - 0.15, ga * (1 - u) + gb * u, g)
    return x * g


def main():
    os.makedirs("audio", exist_ok=True)
    print("componiendo...")
    B = componer()
    pump = bombeo()
    print("procesando buses...")
    B["pad"] = flanger(B["pad"] * pump, 0.1, 2.5)
    B["arp"] = delay_pingpong(B["arp"] * pump, BEAT * 0.75, 0.45, 0.35)
    B["bajo"] = B["bajo"] * (0.65 + 0.35 * pump)
    B["bajo"] = butter_hp(B["bajo"], 32, 2)
    B["bateria"] = compresor(B["bateria"], -14, 3.0, 0.003, 0.08, 2.0)
    B["pad"] = reverb(B["pad"], 0.35, 2.8, 5000)
    B["arp"] = reverb(B["arp"], 0.3, 2.2, 6500)
    B["lead"] = reverb(delay_pingpong(B["lead"], BEAT * 0.5, 0.3, 0.2), 0.35, 2.6, 7000)
    B["fx"] = reverb(B["fx"], 0.25, 2.0, 8000)
    niveles = dict(bateria=0.9, bajo=0.85, pad=0.7, arp=0.55, lead=0.9, fx=0.6)
    mezcla = sum(B[k] * v for k, v in niveles.items())
    mezcla = nivelar(mezcla)
    if os.environ.get("FAB_STEMS"):   # pistas separadas solo si se piden (ocupan ~300 MB)
        np.savez_compressed("audio/musica_stems.npz", **{k: v.astype(np.float32) for k, v in B.items()})
    pico = np.abs(mezcla).max()
    mezcla = mezcla / pico * 0.89
    sf.write("audio/musica.wav", mezcla.T.astype(np.float32), SR, subtype="FLOAT")
    print("listo audio/musica.wav  pico previo", round(float(pico), 3))


if __name__ == "__main__":
    main()
