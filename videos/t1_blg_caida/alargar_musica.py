# -*- coding: utf-8 -*-
"""Las piezas de la biblioteca quedaron cortas al alargar las escenas (nunca cámara rápida, 31-oct-2026) y `armar` solo estira ±12 %: el
resto sería silencio. Aquí cada pieza se alarga con ella misma (repite desde RETOMA con cruce largo), sin pedir Lyria nueva. Los
originales quedan en audio/lyria_orig/; se puede repetir tras cambiar el timeline. Luego: python fab.py lol_semana2 musica
python videos/lol_final_previa/alargar_musica.py"""
import json
import os
import shutil
import subprocess
import sys

import numpy as np
import soundfile as sf

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
os.chdir(D)
from guion import LYRIA  # noqa: E402

CRUCE, RETOMA, SR = 6.0, .2, 48000
tl = json.load(open("timeline.json", encoding="utf-8"))
ESC = {e["id"]: e for e in tl["escenas"]}
os.makedirs("audio/lyria_orig", exist_ok=True)
for n, (ids, _) in enumerate(LYRIA["tramos"], 1):
    pieza, orig = f"audio/lyria_tramo{n}.mp3", f"audio/lyria_orig/tramo{n}.mp3"
    if not os.path.exists(orig):
        shutil.copy2(pieza, orig)
    objetivo = ESC[ids[-1]]["t1"] - ESC[ids[0]]["t0"] + 3.0 + 1.0
    tmp = f"audio/_largo{n}.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", orig, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", tmp], check=True)
    x, _sr = sf.read(tmp, always_2d=True, dtype="float32")
    d = len(x) / SR
    if d >= objetivo * .95:
        shutil.copy2(orig, pieza)
        os.remove(tmp)
        print(f"tramo {n}: {d:.1f} s, le basta ({objetivo:.1f} s)")
        continue
    y, f = x, int(CRUCE * SR)
    cola = x[int(len(x) * RETOMA):]
    while len(y) / SR < objetivo:
        sube = np.sin(np.linspace(0, np.pi / 2, f))[:, None].astype(np.float32)
        y = np.vstack([y[:-f], y[-f:] * sube[::-1] + cola[:f] * sube, cola[f:]])
    sf.write(tmp, y[:int(objetivo * SR)], SR, subtype="FLOAT")
    subprocess.run([FF, "-v", "error", "-y", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "256k", pieza], check=True)
    os.remove(tmp)
    print(f"tramo {n}: {d:.1f} → {objetivo:.1f} s")
