# -*- coding: utf-8 -*-
"""Ambientes GRABADOS de la biblioteca (sfx/*.mp3: alba = viento suave de cañón con pájaros, grillos, viento_noche) en bucle con
fundido cruzado, según `escenas.AMB` = [(t0, t1, archivo, vol)] → audio/fx.wav, que `mezcla` suma con MEZCLA["fx"].
Sustituye al `viento` procedural estirado (21-oct-2026, el usuario: «en algunas partes el viento se escucha muy fuerte»: el
procedural es un golpe de aire de ~1 s y estirado a 13-41 s queda como ruido continuo en los medios, encima de la voz).
Uso: desde C:\\FabricaAnimaciones, `python videos/caxcan_mixton/_fx_ambiente.py` (antes de `fab.py caxcan_mixton mezcla`)."""
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
CRUCE, BORDE = 1.0, 1.5


def cargar(n):
    if n not in _cache:
        y, _ = librosa.load(os.path.join("sfx", n + ".mp3"), sr=SR, mono=False)
        if y.ndim == 1:
            y = np.vstack([y, y])
        rms = float(np.sqrt(np.mean(y ** 2))) + 1e-9
        _cache[n] = (y * (0.1 / rms)).astype(np.float32)     # todos a la misma sonoridad (RMS −20 dBFS) antes de `vol`
    return _cache[n]


def bucle(y, n):
    """y repetido con fundido cruzado de CRUCE s hasta n muestras."""
    k = int(CRUCE * SR)
    res = y.copy()
    f = np.linspace(0, 1, k, dtype=np.float32)
    while res.shape[1] < n:
        a = res[:, -k:] * f[::-1] + y[:, :k] * f
        res = np.concatenate([res[:, :-k], a, y[:, k:]], axis=1)
    return res[:, :n]


try:                                                     # efectos grabados anclados a la voz (ElevenLabs/biblioteca)
    import _fx_eventos as EV
    AMB2, UNA = EV.AMB2, EV.UNA
except ImportError:
    AMB2, UNA = [], []

for t0, t1, n, vol in list(escenas.AMB) + list(AMB2):
    i, j = int(t0 * SR), min(N, int(t1 * SR))
    if j <= i:
        continue
    y = bucle(cargar(n), j - i)
    k = min(int(BORDE * SR), (j - i) // 3)
    f = np.linspace(0, 1, k, dtype=np.float32)
    y[:, :k] *= f
    y[:, -k:] *= f[::-1]
    out[:, i:j] += vol * y

for t, n, vol in UNA:                                    # golpes: una vez, pico −6 dBFS × vol, fundido de salida corto
    y = cargar(n)
    y = y * (0.5 / (np.abs(y).max() + 1e-9))
    k = min(int(0.15 * SR), y.shape[1] // 4)
    y = y.copy()
    y[:, -k:] *= np.linspace(1, 0, k, dtype=np.float32)
    i = int(t * SR)
    j = min(N, i + y.shape[1])
    if j > i:
        out[:, i:j] += vol * y[:, :j - i]

pico = np.abs(out).max()
if pico > 0.98:
    out *= 0.98 / pico
os.makedirs("audio", exist_ok=True)
sf.write("audio/fx.wav", out.T, SR, subtype="FLOAT")
print(f"audio/fx.wav: {len(escenas.AMB) + len(AMB2)} ambientes, {len(UNA)} golpes, {N / SR:.1f} s, pico {pico:.2f}")
