# -*- coding: utf-8 -*-
"""Arma la narración completa (sin música) según timeline.json -> previews/voz_completa.mp3, para oírla antes de animar."""
import json
import os
import subprocess

import librosa
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
TL = json.load(open("timeline.json", encoding="utf-8"))
SR = 48000
fin = max(e["t1"] for e in TL["escenas"])
y = np.zeros(int(fin * SR) + SR, np.float32)
for e in TL["escenas"]:
    for f in e["frases"]:
        v, _ = librosa.load(f"voz/final/{f['key']}.wav", sr=SR, mono=True)
        i = int(f["t0"] * SR)
        y[i:i + len(v)] += v[:len(y) - i]
sf.write("previews/voz_completa.wav", y, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "previews/voz_completa.wav", "-b:a", "128k", "previews/voz_completa.mp3"], check=True)
os.remove("previews/voz_completa.wav")
print("previews/voz_completa.mp3", round(fin, 1), "s")
