# -*- coding: utf-8 -*-
"""Pulsos de cada canción llevados a la línea de tiempo → cortes.json, para que los cambios de toma caigan en el ritmo.
    {"pulsos": {sección: [t, ...]}, "cortes": {sección: [t, ...]}}    (cortes cada N pulsos, ~2,6-3,8 s según la canción)
    python plan_cortes.py"""
import json
import runpy

import librosa
import numpy as np

G = runpy.run_path("guion.py")
TL = json.load(open("timeline.json", encoding="utf-8"))
ESC = {e["id"]: e for e in TL["escenas"]}
CADA_S = {"indita": 2.7, "ojos": 2.8, "amor": 3.6, "teodora": 2.6}     # duración aproximada de cada toma

pulsos, cortes = {}, {}
for k, (n, src, _) in G["CANCION"].items():
    t0, t1 = ESC[k]["t0"], ESC[k]["t1"]
    y, sr = librosa.load(f"{G['STEMS']}/{n}.wav", sr=22050, mono=True, offset=max(0.0, src - 2), duration=t1 - t0 + 4)
    tempo, b = librosa.beat.beat_track(y=y, sr=sr, units="time")
    b = np.asarray(b) + max(0.0, src - 2) - src + t0                 # a la línea de tiempo
    b = b[(b >= t0) & (b < t1)]
    paso = float(np.median(np.diff(b)))
    nb = max(2, int(round(CADA_S[k] / paso)))
    if nb % 2:
        nb += 1                                                       # cortes en pulsos pares (cabeza de compás aprox.)
    c = [float(x) for x in b[nb::nb] if x < t1 - 1.2]
    pulsos[k] = [round(float(x), 3) for x in b]
    cortes[k] = [round(x, 3) for x in c]
    print(f"{k:8s} tempo {float(np.atleast_1d(tempo)[0]):6.1f}  pulso {paso:.3f}s  cada {nb} pulsos  {len(c) + 1} tomas")
json.dump(dict(pulsos=pulsos, cortes=cortes), open("cortes.json", "w", encoding="utf-8"), indent=1)
