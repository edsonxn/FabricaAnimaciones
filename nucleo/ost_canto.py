# -*- coding: utf-8 -*-
"""¿Qué pistas de la OST llevan CANTO? (el usuario, 12-nov-2026: en tes_builds_rotas «pusiste música con voz, música cantada» en el
puesto 6 — Age of Oppression es coro de principio a fin). Bajo la narración la música va SIN voz humana (coro, letra, canto).
Demucs (htdemucs, two-stems vocals) separa la voz de cada pista y mide su energía frente al resto en ventanas de 5 s; una ventana
con voz > UMBRAL dB (−12) cuenta como canto. Resultado en audio/ost/_canto.json → {pista: [segundos con canto]} que
armar_musica_ost.py consulta para no usar esos tramos (`libre(pista, desde, dur)`).
    python nucleo/ost_canto.py <video>        (cachea los stems en E:\\FabricaAnimaciones\\_tmp_demucs\\<video>)
Excepción: cuando la voz NOMBRA la canción (regla del 31-oct: si la voz nombra un sonido, se oye), ahí sí va el canto, con la voz callada."""
import glob
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

UMBRAL = -12.0
VENT = 5


def medir(ost, cache):
    res = {}
    for f in sorted(glob.glob(os.path.join(ost, "*.wav"))):
        n = os.path.splitext(os.path.basename(f))[0]
        base = os.path.join(cache, "htdemucs", n)
        if not os.path.exists(os.path.join(base, "vocals.wav")):
            subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", cache, f],
                           capture_output=True)
        v, sr = sf.read(os.path.join(base, "vocals.wav"), always_2d=True)
        o, _ = sf.read(os.path.join(base, "no_vocals.wav"), always_2d=True)
        w = VENT * sr
        seg = []
        for i in range(0, min(len(v), len(o)) - w, w):
            a = np.sqrt(np.mean(v[i:i + w] ** 2))
            b = np.sqrt(np.mean(o[i:i + w] ** 2)) + 1e-9
            if 20 * np.log10(a / b + 1e-9) > UMBRAL:
                seg.append(i // sr)
        res[n] = seg
        print(f"{n:28s} canto en {len(seg):3d} ventanas de {VENT} s {seg[:14]}", flush=True)
    return res


def libre(canto, pista, desde, dur):
    """True si [desde, desde+dur] de la pista no pisa ninguna ventana con canto."""
    return not any(desde - VENT < s < desde + dur for s in canto.get(pista, []))


if __name__ == "__main__":
    v = sys.argv[1]
    carpeta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos", v)
    ost = os.path.join(carpeta, "audio", "ost")
    r = medir(ost, os.path.join(r"E:\FabricaAnimaciones\_tmp_demucs", v))
    json.dump(r, open(os.path.join(ost, "_canto.json"), "w", encoding="utf-8"), indent=1)
    print("audio/ost/_canto.json listo")
