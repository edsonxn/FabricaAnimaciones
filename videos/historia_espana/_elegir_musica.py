# -*- coding: utf-8 -*-
"""Compara los candidatos de Lyria de cada parte: correlación entre la energía por escena y la intensidad pedida, huecos de silencio y final.
python _elegir_musica.py"""
import json
import subprocess

import numpy as np

import guion
from _lyria_partes import PARTES

FF = r"C:\ffmpeg\bin\ffmpeg.exe"


def leer(ruta, sr=8000):
    x = subprocess.run([FF, "-v", "error", "-i", ruta, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(x, np.float32), sr


for k, P in enumerate(PARTES):
    print(f"== parte {k + 1}: {P['ids']}")
    pedidas = np.array([guion.LYRIA["escenas"][i][1] for i in P["ids"]], float)
    for c in (1, 2):
        try:
            x, sr = leer(f"audio/ly{k + 1}_{c}.mp3")
        except Exception as e:                       # noqa: BLE001
            print("  falta", c, e)
            continue
        dur = len(x) / sr
        esc = P["tl"]["escenas"]
        en = []
        for j, e in enumerate(esc):
            a = e["t0"]
            b = esc[j + 1]["t0"] if j + 1 < len(esc) else P["tl"]["total"]
            seg = x[int(a * sr):int(min(b, dur) * sr)]
            en.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
        en = np.array(en)
        r = float(np.corrcoef(en, pedidas)[0, 1]) if en.std() > 0 else 0.0
        v = np.sqrt(np.convolve(x ** 2, np.ones(sr // 4) / (sr // 4), "same"))
        silencio = float((v < 0.01 * v.max()).mean())
        print(f"  cand {c}: dur {dur:.1f} s, correlación energía/intensidad {r:+.2f}, silencio {silencio * 100:.1f} %, "
              f"energía por escena {np.round(en / en.max(), 2).tolist()}")
