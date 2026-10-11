# -*- coding: utf-8 -*-
"""Aplica qa.silenciar_arranque con el mismo camino que tts_select (paso 3) sin Whisper. Simula las 57 frases; solo escribe las que cambian."""
import json, os, shutil, sys
import librosa, numpy as np, pyloudnorm as pyln, soundfile as sf
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
from qa import silenciar_arranque

SR_OUT = 48000
pal = json.load(open("voz/palabras.json", encoding="utf-8"))
meter = pyln.Meter(SR_OUT)
escribir = "--escribir" in sys.argv
for key, p in pal.items():
    y, sr = librosa.load(f"voz/cands/{p['take']}", sr=None)
    y = librosa.resample(y, orig_sr=sr, target_sr=SR_OUT, res_type="soxr_vhq")
    iv = librosa.effects.split(y, top_db=45, frame_length=2048, hop_length=256)
    a = max(0, iv[0][0] - int(0.04 * SR_OUT)); b = min(len(y), iv[-1][1] + int(0.12 * SR_OUT))
    y = y[a:b].astype(np.float64)
    y, mudo = silenciar_arranque(y, SR_OUT)
    if not mudo:
        continue
    print(f"{key}: se silenciarían {mudo:.2f} s  (dur {len(y)/SR_OUT:.3f} s; palabras.json dice {p['dur']})")
    if escribir:
        fi, fo = int(0.006 * SR_OUT), int(0.05 * SR_OUT)
        y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo) ** 2
        y = pyln.normalize.loudness(y, meter.integrated_loudness(y), -20.0)
        dest = f"voz/final/{key}.wav"
        if not os.path.exists(f"voz/{key}_antes_arranque.wav"):
            shutil.copy(dest, f"voz/{key}_antes_arranque.wav")
        sf.write(dest, y.astype(np.float32), SR_OUT, subtype="FLOAT")
        print("  escrito", dest)
print("fin")
