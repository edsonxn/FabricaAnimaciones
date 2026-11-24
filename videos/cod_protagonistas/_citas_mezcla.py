# -*- coding: utf-8 -*-
"""REGLA 10 (19-nov-2026): cada cita que la voz manda escuchar, extraída de la MEZCLA (audio/final.wav), por Whisper + nivel
contra la música. Junta todas en previews/citas_audio.mp3.   python _citas_mezcla.py"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
ESP = {"p11": "one less loose end", "p09": "for you mason not for me", "p08": "makarov knows yuri", "p06": "never personal",
       "p03": "there is a line one we don't cross", "p02": "he was the best of us", "p01": "gaz was right hold the line"}
tl = json.load(open("timeline.json", encoding="utf-8"))
tramos = [(e["id"], float(e["frases"][-1]["t1"]), float(e["t1"])) for e in tl["escenas"] if e["id"] in ESP]
x, sr = sf.read("audio/final.wav", always_2d=True)
m = sf.read("audio/musica.wav", always_2d=True)[0]
wm = WhisperModel("medium", device="cpu", compute_type="int8")
os.makedirs("previews/_citas", exist_ok=True)
partes = []
for k, a, b in tramos:
    seg = x[int(a * sr):int(b * sr)]
    f = f"previews/_citas/{k}.wav"
    sf.write(f, seg, sr)
    rms = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
    mus = m[int(a * 48000):int(b * 48000)]
    rmm = 20 * np.log10(np.sqrt(np.mean(mus ** 2)) + 1e-9) - 14   # la música va apartada −14 dB en el hueco
    segs, _ = wm.transcribe(f, language="en", vad_filter=False)
    txt = " ".join(s.text.strip() for s in segs)
    print(f"{k} {a:7.1f}-{b:7.1f}  mezcla {rms:6.1f} dBFS · música≈{rmm:6.1f}  → «{txt}»   (esperado: {ESP[k]})", flush=True)
    partes.append(f)
lista = "previews/_citas/lista.txt"
open(lista, "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in partes))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-ac", "2", "-b:a", "160k",
                "previews/citas_audio.mp3"], check=True)
print("previews/citas_audio.mp3")
