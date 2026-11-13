# -*- coding: utf-8 -*-
"""Mezcla y master: voz + música (con ducking) + SFX -> audio/final.wav (-14 LUFS, <= -1 dBTP)."""
import json
import math
import os

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
    if not os.path.isfile(ruta):                # float32: con float64 un video de 51 min no cabía en 32 GB (27-oct-2026)
        return np.zeros((2, N), np.float32)
    x, sr = sf.read(ruta, always_2d=True)
    assert sr == SR, (ruta, sr)
    x = np.nan_to_num(x.T)                       # una pista sin eventos (sfx vacío) sale con NaN y envenenaba toda la mezcla
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    out = np.zeros((2, N), np.float32)
    n = min(N, x.shape[1])
    out[:, :n] = x[:, :n]
    return out


def pista_voz():
    if TL.get("audio_externo"):                  # audio ya grabado (guion.AUDIO_EXTERNO): va tal cual, sin la cadena de la voz sintética
        return cargar(TL["audio_externo"])
    v = np.zeros(N)
    try:                                         # guion.VOZ_FX = {key: "espiritu"}: efecto por frase (nucleo/voz_fx.py, 13-nov-2026)
        import guion as _g
        vfx = getattr(_g, "VOZ_FX", {}) or {}
    except ImportError:
        vfx = {}
    for e in TL["escenas"]:
        for f in e["frases"]:
            x, sr = sf.read(f"voz/final/{f['key']}.wav")
            assert sr == SR
            if f["key"] in vfx:
                import voz_fx
                x = voz_fx.aplicar(x, sr, vfx[f["key"]])
                print(f"  voz_fx: {f['key']} → {vfx[f['key']]}")
            i = int(round(f["t0"] * SR))
            v[i:i + len(x)] += x[:N - i]
    # procesado de voz
    if config.CADENA_VOZ == "suave":             # Applio: ya viene procesada por RVC (A/B del usuario, 13-oct-2026)
        v = butter_hp(v, 70, 2)
        v = compresor(v, -20, 1.6, 0.006, 0.15, 1.0)
        return np.stack([v, v]).astype(np.float32)
    v = butter_hp(v, 80, 2)
    v = peq(v, 280, -2.0, 1.0)
    v = peq(v, 3500, 2.0, 0.9)
    v = shelf(v, 10000, 1.0, alto=True)
    v = compresor(v, -22, 3.0, 0.004, 0.12, 3.0)
    return np.stack([v, v]).astype(np.float32)


def curva_ducking(voz, profundidad_db, anticipo=0.06, ataque=0.03, liberacion=0.35):
    env = envolvente(voz, ataque, liberacion)
    env = env / (np.percentile(env[env > 1e-4], 90) + 1e-9)
    act = np.clip(env / 0.25, 0, 1)            # 0 = sin voz, 1 = voz presente
    k = int(anticipo * SR)
    act = np.concatenate([act[k:], np.zeros(k)])  # la música baja justo antes de que empiece la voz
    act = np.maximum.accumulate(act[::-1])[::-1] * 0 + act
    return 10 ** (-profundidad_db * act / 20)


def pico_verdadero_db(x):
    # por trozos de 30 s (con 1 s de solape): sobremuestrear ×4 un video de 51 min entero pedía 9 GB (27-oct-2026)
    paso, sol, pico = 30 * SR, SR, 0.0
    for i in range(0, x.shape[1], paso):
        up = resample_poly(x[:, max(0, i - sol):i + paso + sol], 4, 1, axis=1)
        pico = max(pico, float(np.abs(up).max()))
    return 20 * math.log10(pico + 1e-12)


def main():
    voz = pista_voz()
    musica = cargar("audio/musica.wav")
    sfx = cargar("audio/sfx.wav")
    amb = cargar("audio/ambiente.wav")           # motor secuencia: sonido propio de los clips (ya viene con su volumen)

    # niveles de partida: voz a -16 LUFS (solo tramos con voz); sin voz (SIN_VOZ) no hay voz ni ducking
    habla = np.abs(voz[0]) > 1e-4
    hay_voz = bool(habla.any())
    if hay_voz:
        lv = meter.integrated_loudness(voz.T)
        voz *= 10 ** ((-16.0 - lv) / 20)
    fxv = cargar("audio/fx_voz.wav")             # efectos.py PISTAS voz=True (tramo de un creativo de patrocinio): nivel de voz,
    if np.abs(fxv).max() > 1e-4:                 # sin la cadena de la voz, y la música se agacha debajo igual que con la narración
        fxv *= 10 ** ((-16.0 - meter.integrated_loudness(fxv.T)) / 20)
        hay_voz = True
    guia = voz[0] + fxv[0]
    if np.abs(musica).max() > 1e-4:
        lm = meter.integrated_loudness(musica.T)
        musica *= 10 ** ((config.MEZCLA["musica"] - lm) / 20)
        if config.MEZCLA.get("musica_curva"):    # [(s, dB), ...] lineal entre puntos: la música entra y sale por escena
            pts = sorted(config.MEZCLA["musica_curva"])   # (novela: casi muda bajo la plática, sube en giros y cortinillas)
            musica *= 10 ** (np.interp(np.arange(N) / SR, [p[0] for p in pts], [p[1] for p in pts]) / 20)
    if np.abs(sfx).max() > 1e-4:
        ls = meter.integrated_loudness(sfx.T)
        sfx *= 10 ** ((config.MEZCLA["sfx"] - ls) / 20)

    # novela (SIN_VOZ + SECUENCIA dialogo=True): el audio de los clips ES el diálogo -> se trata como la voz: a -16 LUFS y la
    # música se agacha debajo. Sin esto la música iba ~6 dB bajo las voces y las tapaba (heredera cap. 1-2, 23-oct-2026).
    dialogo = (not hay_voz and getattr(config._g, "SECUENCIA", {}).get("dialogo", False)
               and np.abs(amb).max() > 1e-4)
    if dialogo:
        amb *= 10 ** ((-16.0 - meter.integrated_loudness(amb.T)) / 20)
        guia_d = butter_hp(amb[0], 250, 2)        # sin graves: que el ruido de fondo del clip no cuente como voz
        g_d = curva_ducking(guia_d, config.MEZCLA.get("duck_dialogo", 12.0), anticipo=0.12)
        habla = g_d < 10 ** (-6 / 20)
        if np.abs(musica).max() > 1e-4:
            musica *= g_d
        if np.abs(sfx).max() > 1e-4:
            sfx *= curva_ducking(guia_d, 6.0, anticipo=0.02)
    if np.abs(amb).max() > 1e-4 and hay_voz:      # su nivel ya lo fijó secuencia.ambiente (50 % = unos 10 dB bajo la voz)
        amb *= curva_ducking(guia, 5.0, anticipo=0.02)
    if hay_voz:
        if np.abs(musica).max() > 1e-4:
            musica *= curva_ducking(guia, 11.0)
        if np.abs(sfx).max() > 1e-4:
            sfx *= curva_ducking(guia, 6.0, anticipo=0.02)
        if not TL.get("audio_externo") and config.CADENA_VOZ != "suave" and np.abs(voz).max() > 1e-4:
            voz = reverb(voz, *getattr(config._g, "REVERB_VOZ", (0.05, 0.9, 6000.0)))   # guion.REVERB_VOZ: (mezcla, s, Hz)
    voz = voz + fxv

    fx = cargar("audio/fx.wav") * 10 ** (config.MEZCLA.get("fx", -6.0) / 20)   # secuencia con efectos: SFX y ambientes de
    amb = amb + fx                               # ElevenLabs anclados a la voz; cada uno ya trae su volumen (efectos.py PISTAS)

    # jumpscares: audio/sustos.json = [[apagón, golpe], ...] (lo escribe el script de SFX del video). Del apagón al golpe TODO se
    # apaga (silencio de verdad, también la cola de la reverb); el golpe (audio/fx_sustos.wav) sale al frente a MEZCLA["susto"]
    # LUFS y la cama vuelve en 1,2 s. Sin esto el golpe quedaba bajo la música (tres noches, 15-oct-2026).
    golpes = cargar("audio/fx_sustos.wav")
    if os.path.isfile("audio/sustos.json"):
        t = np.arange(N) / SR
        g = np.ones(N)
        for t_ap, t_gol in json.load(open("audio/sustos.json", encoding="utf-8")):
            baja = np.clip((t - t_ap) / 0.3, 0, 1)
            sube = np.clip((t - t_gol - 0.7) / 1.2, 0, 1)
            g = np.minimum(g, 1 - baja + sube)
        voz, musica, sfx, amb = voz * g, musica * g, sfx * g, amb * g
    if np.abs(golpes).max() > 1e-4:
        lg = meter.integrated_loudness(golpes[:, np.abs(golpes).max(0) > 1e-4].T)
        golpes *= 10 ** ((config.MEZCLA.get("susto", -9.0) - lg) / 20)
    mix = voz + musica + sfx + amb + golpes
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
    if tp > -1.0:                        # el pico verdadero (intermuestra) debe quedar <= -1 dBTP
        mix *= 10 ** ((-1.05 - tp) / 20)
        l = meter.integrated_loudness(mix.T)
        tp = pico_verdadero_db(mix)
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/final.wav", mix.T.astype(np.float32), SR, subtype="PCM_24")

    # ---- control de calidad de mezcla
    rms = lambda a: np.sqrt(np.mean(a ** 2) + 1e-12)
    print(f"LUFS integrado: {l:.2f}   pico verdadero: {tp:.2f} dBTP   duración: {mix.shape[1] / SR:.2f}s")
    if dialogo:                                   # novela: diálogo (clips) contra música; telenovela pide >= 15 dB
        vmr = 20 * math.log10(rms(amb[0][habla]) / rms(musica[0][habla]))
        print(f"relación diálogo/música durante el habla: {vmr:.1f} dB" + ("" if vmr >= 15 else "  ⚠ < 15 dB: baja MEZCLA['musica']"))
    elif habla.any():
        fondo = (musica + sfx + amb)[0][habla]
        if np.abs(fondo).max() > 1e-4:
            vmr = 20 * math.log10(rms(voz[0][habla]) / rms(fondo))
            print(f"relación voz/(música+sfx) durante el habla: {vmr:.1f} dB")
        else:
            print("mezcla solo con pista de voz (sin música ni sfx)")
    else:
        rm, rs = rms(musica[0]), rms((sfx + amb)[0])      # amb ya incluye el sonido de los clips y fx.wav
        print(f"sin voz: relación música/efectos {20 * math.log10(rm / rs):.1f} dB")


if __name__ == "__main__":
    main()
