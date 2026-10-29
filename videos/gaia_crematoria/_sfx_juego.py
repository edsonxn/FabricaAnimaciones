# -*- coding: utf-8 -*-
"""SFX REALES de World of Warcraft (Wowhead, `sfx_juego/*.ogg`) colocados según `escenas.JUEGO` → audio/fx.wav, que `mezcla`
suma con MEZCLA["fx"]. Los ambientes (dur > largo del archivo) se repiten con fundido cruzado.
Uso (desde C:\\FabricaAnimaciones): $env:PYTHONPATH="videos\\wow_darrowshire;nucleo"; python videos/gaia_crematoria/_sfx_juego.py
(o desde la carpeta del video con PYTHONPATH apuntando también a ../../nucleo)."""
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
        y, _ = librosa.load(os.path.join("sfx_juego", n + ".ogg"), sr=SR, mono=False)
        if y.ndim == 1:
            y = np.vstack([y, y])
        y = y / (np.abs(y).max() + 1e-9)
        _cache[n] = y.astype(np.float32)
    return _cache[n]


def ambiente(y, dur, cruce=1.5):
    """Repite el archivo hasta `dur` s con fundido cruzado."""
    n = int(dur * SR)
    if y.shape[1] >= n:
        return y[:, :n].copy()
    c = int(cruce * SR)
    res = y.copy()
    while res.shape[1] < n:
        f = np.linspace(0, 1, c, dtype=np.float32)
        res[:, -c:] = res[:, -c:] * (1 - f) + y[:, :c] * f
        res = np.concatenate([res, y[:, c:]], axis=1)
    return res[:, :n]


for t, n, vol, dur, fade in escenas.JUEGO:
    y = cargar(n)
    if dur is not None:
        y = ambiente(y, dur)
        rms = float(np.sqrt((y ** 2).mean()) + 1e-9)
        y = y * (0.05 / rms)                     # ambientes: a nivel de cama (≈ -26 dBFS RMS)
    else:
        y = y * 0.5                              # golpes sueltos: pico -6 dBFS
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
print(f"audio/fx.wav: {len(escenas.JUEGO)} sonidos del juego, {N / SR:.1f} s, pico {pico:.2f}")
