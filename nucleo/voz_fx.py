# -*- coding: utf-8 -*-
"""Efectos de voz por frase, aplicados en la MEZCLA (las tomas de voz/final quedan limpias: idioma_voz, Whisper y `tiempo`
siguen leyendo la voz tal cual).

guion.py:  VOZ_FX = {"c9_5": "espiritu", ...}
    espiritu  = voz de ultratumba tipo caballero de la muerte de WoW (el usuario, 13-nov-2026, Potema muerta en
                tes_reina_loba): la voz + una copia 5 semitonos abajo, timbre metálico (filtro peine), reverb de cripta y eco.
                Deja una cola de ~1,6 s que se suma encima de lo que siga (la mezcla suma cada frase en su t0).
Probar:  python nucleo/voz_fx.py <entrada.wav> <salida.wav> [efecto]
"""
import numpy as np
from scipy.signal import butter, fftconvolve, lfilter

COLA = 1.6


def _lp(x, fc, sr):
    b, a = butter(2, fc / (sr / 2))
    return lfilter(b, a, x)


def _hp(x, fc, sr):
    b, a = butter(2, fc / (sr / 2), btype="high")
    return lfilter(b, a, x)


def _peine(x, sr, ms=9.0, fb=0.45):
    d = max(1, int(sr * ms / 1000))
    b = np.zeros(d + 1); b[0] = 1.0
    a = np.zeros(d + 1); a[0] = 1.0; a[d] = -fb
    return lfilter(b, a, x) * (1 - fb)


def espiritu(x, sr):
    import librosa
    x = np.asarray(x, np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    rms0 = np.sqrt(np.mean(x ** 2)) + 1e-9
    x = np.concatenate([x, np.zeros(int(COLA * sr))])
    grave = librosa.effects.pitch_shift(x.astype(np.float32), sr=sr, n_steps=-5).astype(np.float64)
    seco = 0.62 * x + 0.62 * _lp(grave, 3200, sr)
    metal = 0.75 * seco + 0.45 * _peine(seco, sr, 9.0, 0.5) + 0.25 * _peine(seco, sr, 13.7, 0.4)
    # reverb de cripta: ruido con caída exponencial (1,4 s), oscurecido
    rng = np.random.default_rng(7)
    n = int(1.4 * sr)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.32 * sr))
    ir = _lp(ir, 4500, sr); ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
    rev = fftconvolve(metal, ir)[:len(metal)]
    # eco: tres rebotes, cada uno más oscuro
    eco = np.zeros_like(metal)
    for k, (t, g) in enumerate(((0.24, 0.40), (0.48, 0.22), (0.72, 0.11))):
        i = int(t * sr)
        eco[i:] += g * _lp(metal, 3000 - 600 * k, sr)[:len(metal) - i]
    y = metal + 0.32 * rev + eco
    y = _hp(y, 70, sr)
    y *= rms0 / (np.sqrt(np.mean(y[:len(y) - int(COLA * sr)] ** 2)) + 1e-9)   # mismo volumen que la toma limpia
    pico = np.abs(y).max()
    if pico > 0.98:
        y *= 0.98 / pico
    return y.astype(np.float64)


EFECTOS = {"espiritu": espiritu}


def aplicar(x, sr, efecto):
    if efecto not in EFECTOS:
        raise SystemExit(f"VOZ_FX: efecto desconocido «{efecto}» (hay: {', '.join(EFECTOS)})")
    return EFECTOS[efecto](x, sr)


if __name__ == "__main__":
    import sys
    import soundfile as sf
    x, sr = sf.read(sys.argv[1])
    sf.write(sys.argv[2], aplicar(x, sr, sys.argv[3] if len(sys.argv) > 3 else "espiritu"), sr)
