# -*- coding: utf-8 -*-
"""SFX propios del video (sfx/*.mp3, ElevenLabs del 8-oct-2026: sello de metal, cerrojo, puerta, pulso grave, estática, cristal,
alarma) colocados según `escenas.FXP` → audio/fx.wav, que `mezcla` suma con MEZCLA["fx"] (misma receta que wow_darrowshire).
Uso: desde C:\\FabricaAnimaciones, `python videos/secreto_ia/_sfx_propios.py`."""
import os
import sys

import librosa
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import escenas  # noqa: E402

SR = 48000
N = int(escenas.TOTAL * SR) + SR
out = np.zeros((2, N), np.float32)
_cache = {}


def cargar(n):
    if n not in _cache:
        y, _ = librosa.load(os.path.join("sfx", n + ".mp3"), sr=SR, mono=False)
        if y.ndim == 1:
            y = np.vstack([y, y])
        _cache[n] = (y / (np.abs(y).max() + 1e-9)).astype(np.float32)
    return _cache[n]


for t, n, vol, dur, fade in escenas.FXP:
    y = cargar(n) * 0.5                         # pico -6 dBFS
    if dur is not None:
        y = y[:, :int(dur * SR)]
    k = int(fade * SR)
    if k > 0 and y.shape[1] > 2 * k:
        f = np.linspace(0, 1, k, dtype=np.float32)
        y[:, :k] *= f
        y[:, -k:] *= f[::-1]
    i = int(t * SR)
    j = min(N, i + y.shape[1])
    if j > i:
        out[:, i:j] += vol * y[:, :j - i]

pico = np.abs(out).max()
if pico > 0.98:
    out *= 0.98 / pico
os.makedirs("audio", exist_ok=True)
sf.write("audio/fx.wav", out.T, SR, subtype="FLOAT")
print(f"audio/fx.wav: {len(escenas.FXP)} sonidos propios, {N / SR:.1f} s, pico {pico:.2f}")
