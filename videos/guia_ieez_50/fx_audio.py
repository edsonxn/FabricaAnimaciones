# -*- coding: utf-8 -*-
"""Sonidos de estudio -> audio/fx.wav (48 kHz): tic-tac suave en cada pausa de pregunta (un tic por segundo, el último más
agudo) y una campanita al revelar cada respuesta. Así el reloj también se «ve» con los oídos si el video solo se escucha.
Uso (desde la carpeta del video, tras `tiempo`):  python fx_audio.py"""
import json

import numpy as np
import soundfile as sf

import guion as G

SR = 48000
TL = json.load(open("timeline.json", encoding="utf-8"))
N = int(TL["total"] * SR)
out = np.zeros(N, np.float32)
VIS = {e["id"]: e.get("vis", {}) for e in G.ESCENAS}


def poner(t, x):
    i = int(t * SR)
    if 0 <= i < N:
        n = min(len(x), N - i)
        out[i:i + n] += x[:n]


def tic(f=1900.0, amp=0.16, dur=0.05):
    t = np.arange(int(dur * SR)) / SR
    return (amp * np.sin(2 * np.pi * f * t) * np.exp(-t * 90)).astype(np.float32)


def campana(amp=0.14):
    t = np.arange(int(1.2 * SR)) / SR
    x = np.zeros_like(t)
    for k, (f, t0) in enumerate(((1318.5, 0.0), (1975.5, 0.09))):
        tt = np.clip(t - t0, 0, None)
        x += (t >= t0) * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 5) * (0.8 if k else 1.0)
    return (amp * x / 1.8).astype(np.float32)


for e in TL["escenas"]:
    v = VIS.get(e["id"], {})
    if v.get("tipo") == "pregunta":
        fin = max(f["t1"] for f in e["frases"]) + 0.15
        n = int(round(v.get("cuenta", 4.0)))
        for k in range(n):
            poner(fin + k, tic(1900.0 if k < n - 1 else 2600.0, 0.16 if k < n - 1 else 0.2))
    elif v.get("tipo") == "respuesta":
        poner(e["t0"] + 0.02, campana())

sf.write("audio/fx.wav", np.stack([out, out], 1), SR, subtype="FLOAT")
print("audio/fx.wav", round(N / SR, 1), "s")
