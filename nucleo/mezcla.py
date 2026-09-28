# -*- coding: utf-8 -*-
"""Mezcla y master: voz + música (con ducking) + SFX -> audio/final.wav (-14 LUFS, <= -1 dBTP)."""
import json
import math

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

import config
from sinte import SR, butter_hp, compresor, envolvente, limitador, peq, reverb, shelf

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
N = int(TOTAL * SR)
meter = pyln.Meter(SR)


def cargar(ruta):
    x, sr = sf.read(ruta, always_2d=True)
    assert sr == SR, (ruta, sr)
    x = x.T
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    out = np.zeros((2, N))
    n = min(N, x.shape[1])
    out[:, :n] = x[:, :n]
    return out


def pista_voz():
    v = np.zeros(N)
    for e in TL["escenas"]:
        for f in e["frases"]:
            x, sr = sf.read(f"voz/final/{f['key']}.wav")
            assert sr == SR
            i = int(round(f["t0"] * SR))
            v[i:i + len(x)] += x[:N - i]
    # procesado de voz
    v = butter_hp(v, 80, 2)
    v = peq(v, 280, -2.0, 1.0)
    v = peq(v, 3500, 2.0, 0.9)
    v = shelf(v, 10000, 1.0, alto=True)
    v = compresor(v, -22, 3.0, 0.004, 0.12, 3.0)
    return np.stack([v, v])


def curva_ducking(voz, profundidad_db, anticipo=0.06, ataque=0.03, liberacion=0.35):
    env = envolvente(voz, ataque, liberacion)
    env = env / (np.percentile(env[env > 1e-4], 90) + 1e-9)
    act = np.clip(env / 0.25, 0, 1)            # 0 = sin voz, 1 = voz presente
    k = int(anticipo * SR)
    act = np.concatenate([act[k:], np.zeros(k)])  # la música baja justo antes de que empiece la voz
    act = np.maximum.accumulate(act[::-1])[::-1] * 0 + act
    return 10 ** (-profundidad_db * act / 20)


def pico_verdadero_db(x):
    up = resample_poly(x, 4, 1, axis=1)
    return 20 * math.log10(np.abs(up).max() + 1e-12)


def main():
    voz = pista_voz()
    musica = cargar("audio/musica.wav")
    sfx = cargar("audio/sfx.wav")

    # niveles de partida: voz a -16 LUFS (solo tramos con voz)
    habla = np.abs(voz[0]) > 1e-4
    lv = meter.integrated_loudness(voz.T)
    voz *= 10 ** ((-16.0 - lv) / 20)
    lm = meter.integrated_loudness(musica.T)
    musica *= 10 ** ((config.MEZCLA["musica"] - lm) / 20)
    ls = meter.integrated_loudness(sfx.T)
    sfx *= 10 ** ((config.MEZCLA["sfx"] - ls) / 20)

    duck_m = curva_ducking(voz[0], 11.0)
    duck_s = curva_ducking(voz[0], 6.0, anticipo=0.02)
    musica *= duck_m
    sfx *= duck_s
    voz = reverb(voz, 0.05, 0.9, 6000)

    mix = voz + musica + sfx
    mix = compresor(mix, -12, 1.8, 0.01, 0.2, 0.0)

    # fundido final (coincide con el fundido a negro del video)
    t = np.arange(N) / SR
    mix *= np.clip((TOTAL - 0.05 - t) / 0.55, 0, 1)

    # loudness a -14 LUFS con limitador a -1.2 dBFS (2 pasadas)
    for _ in range(3):
        l = meter.integrated_loudness(mix.T)
        mix *= 10 ** ((-14.0 - l) / 20)
        mix = limitador(mix, -1.6, 0.005, 0.1)
    l = meter.integrated_loudness(mix.T)
    tp = pico_verdadero_db(mix)
    sf.write("audio/final.wav", mix.T.astype(np.float32), SR, subtype="PCM_24")

    # ---- control de calidad de mezcla
    rms = lambda a: np.sqrt(np.mean(a ** 2) + 1e-12)
    vmr = 20 * math.log10(rms(voz[0][habla]) / rms((musica + sfx)[0][habla]))
    print(f"LUFS integrado: {l:.2f}   pico verdadero: {tp:.2f} dBTP   duración: {mix.shape[1] / SR:.2f}s")
    print(f"relación voz/(música+sfx) durante el habla: {vmr:.1f} dB")


if __name__ == "__main__":
    main()
