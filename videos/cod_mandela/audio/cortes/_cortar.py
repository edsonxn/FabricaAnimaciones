# -*- coding: utf-8 -*-
"""Corta los SONIDOS NOMBRADOS (regla 31-oct-2026) a sfx/s_<n>.mp3, a -18 LUFS, con los segundos medidos con Whisper (_ubicar.py)
sobre el audio COMPLETO de cada video (sin --download-sections: así el segundo es exacto).
    python _cortar.py
"""
import os
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(AQUI, "..", "..", "sfx")
SR = 48000
# nombre: [(archivo, desde, hasta), ...]  (varios tramos = montaje con 0,15 s de aire)
CORTES = {
    "s_shepherd": [("mv88YFoq2rc", 53.05, 57.75)],                     # «Good. That's one less loose end.» + disparo + «No!»
    "s_brazo": [("ijssTVhflBc", 87.55, 90.15)],                        # «Target down. I think I saw his arm fly off.»
    "s_numbers": [("YzK11dTXbrQ", 45.95, 48.55)],                      # «The numbers… what do they mean»
    "s_115": [(os.path.join("..", "ost", "z_115"), 62.6, 68.4)],      # «115» de Elena Siegman (Kino der Toten)
    "s_ramirez": [("KEWwsYGC0HY", 185.45, 187.25), ("KEWwsYGC0HY", 208.4, 209.95),
                  ("KEWwsYGC0HY", 224.5, 226.65), ("KEWwsYGC0HY", 332.85, 335.1)],   # Foley: «Ramirez, …» ×3 + «Get to the roof…»
    "s_jingle": [("NRIkSSmXJMk", 11.4, 16.1)],                          # «…reach for Juggernog tonight»
    "s_bravo6": [("bH1lHCirCGI", 39.35, 43.3)],                         # tráiler MW2019: «Bravo Six, going dark.»
}


def leer(nombre, a, b):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", os.path.join(AQUI, nombre + ".wav"),
           "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    n = int(.06 * SR)
    r = np.linspace(0, 1, n)[:, None]
    x[:n] *= r
    x[-n:] *= r[::-1]
    return x


def main():
    os.makedirs(SFX, exist_ok=True)
    med = pyln.Meter(SR)
    for nom, tramos in CORTES.items():
        partes = []
        for i, (arch, a, b) in enumerate(tramos):
            if i:
                partes.append(np.zeros((int(.15 * SR), 2), np.float32))
            partes.append(leer(arch, a, b))
        x = np.concatenate(partes)
        x = pyln.normalize.loudness(x, med.integrated_loudness(x), -18.0)
        x = np.clip(x, -.98, .98)
        wav = os.path.join(SFX, nom + ".wav")
        sf.write(wav, x, SR)
        mp3 = wav[:-4] + ".mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "192k", mp3], check=True)
        os.remove(wav)
        vd = subprocess.run(["ffmpeg", "-i", mp3, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
        mv = [l.split(":")[1].strip() for l in vd.splitlines() if "mean_volume" in l]
        print(f"{nom}: {len(x) / SR:.2f} s · media {mv[0] if mv else '?'}")


if __name__ == "__main__":
    main()
