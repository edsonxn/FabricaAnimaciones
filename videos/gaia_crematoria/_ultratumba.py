# -*- coding: utf-8 -*-
"""Eco de ultratumba en las voces de los muertos (VOCES_ULTRATUMBA del guion + Alexandros ya muerto: caballero de la muerte,
espíritu y susurros de la espada). Procesa voz/final/<frase>.wav EN SITIO; la original queda en voz/final_orig/ (si ya existe, parte
de ella: se puede correr varias veces). Después: `python fab.py gaia_crematoria mezcla`.
Uso (desde la carpeta del video): python _ultratumba.py"""
import os
import shutil
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion  # noqa: E402

FUERTE = set(guion.VOCES_ULTRATUMBA)
MUERTO = ("naxxramas", "susurros", "monasterio", "darion_busca", "alba", "epilogo", "gancho")   # escenas donde Alexandros ya murió


def eco(x, sr, fuerte):
    cola = int(0.45 * sr)
    y = np.concatenate([x, np.zeros(cola, x.dtype)])
    out = y.copy()
    retardos = ((0.11, 0.42), (0.23, 0.28), (0.37, 0.16)) if fuerte else ((0.13, 0.26), (0.29, 0.12))
    for d, g in retardos:
        k = int(d * sr)
        out[k:] += g * y[:-k]
    sos = butter(2, 3800 if fuerte else 5200, "low", fs=sr, output="sos")
    humedo = sosfilt(sos, out - y)
    out = y + humedo
    if fuerte:                                   # un poco de «aliento» grave: suma una octava abajo muy baja
        out += 0.10 * sosfilt(butter(2, 300, "low", fs=sr, output="sos"), y)
    return (out / max(1.0, np.abs(out).max() / 0.95)).astype(np.float32)


n = 0
os.makedirs("voz/final_orig", exist_ok=True)
for k, per in guion.PERSONAJE_POR_FRASE.items():
    esc = k.rsplit("_", 1)[0]
    fuerte = per in FUERTE
    if not (fuerte or (per == "alexandros" and esc in MUERTO)):
        continue
    src = f"voz/final/{k}.wav"
    bak = f"voz/final_orig/{k}.wav"
    if not os.path.exists(bak):
        shutil.copy(src, bak)
    x, sr = sf.read(bak, dtype="float32")
    sf.write(src, eco(x, sr, fuerte), sr)
    n += 1
print(f"eco de ultratumba en {n} frases")
