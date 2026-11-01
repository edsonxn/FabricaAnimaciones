# -*- coding: utf-8 -*-
"""Escucha en el MP4 FINAL (audio mezclado) las frases dadas con Whisper, trozo a trozo entre silencios de la voz: cada trozo debe empezar y
acabar en palabra entera. python videos/lol_semana2/investigacion/oir_mp4.py frase [frase …]"""
import json
import os
import subprocess
import sys

from faster_whisper import WhisperModel

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP4 = os.path.join(D, "salida", "lol_semana2_ACTO_A.mp4")
tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
FR = {f["key"]: f for e in tl["escenas"] for f in e["frases"]}
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
tmp = os.path.join(D, "voz", "_oir.wav")
for k in sys.argv[1:]:
    f = FR[k]
    w = f["words"]
    trozos, ini = [], w[0]["s"]
    for a, b in zip(w, w[1:]):
        if b["s"] - a["e"] > .8:                      # silencio metido: la narración original va en medio
            trozos.append((ini, a["e"]))
            ini = b["s"]
    trozos.append((ini, f["t1"]))
    print(f"\n{k} {int(f['t0'] // 60)}:{int(f['t0'] % 60):02d}\n  texto: {f['texto']}")
    for a, b in trozos:
        subprocess.run([FF, "-v", "error", "-y", "-ss", f"{a - .25:.2f}", "-i", MP4, "-t", f"{b - a + .5:.2f}", "-vn", "-ac", "1", "-ar", "16000", tmp], check=True)
        t = " ".join(s.text.strip() for s in m.transcribe(tmp, language="es", beam_size=5, initial_prompt=f["texto"], vad_filter=False)[0])
        print(f"  {int(a // 60)}:{a % 60:04.1f} «{t}»")
os.remove(tmp)
