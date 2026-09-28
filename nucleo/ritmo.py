# -*- coding: utf-8 -*-
"""Patrones rítmicos compartidos por la música y la animación (pulsos visuales = bombos reales)."""
import json
import math

import numpy as np

import config

TL = json.load(open("timeline.json", encoding="utf-8"))
BPM = TL["bpm"]
BEAT = TL["beat"]
PASO = BEAT / 4  # semicorchea

# pasos (semicorcheas) donde suena el bombo, en un ciclo de 16 (un compás 4/4)
PATRONES = {
    "4x4": [0, 4, 8, 12],
    "break": [0, 7, 10],
    "medio": [0, 10],
    "latido": [0, 3, 8, 11],
    "suave": [0, 8],
    "nada": [],
}
# estilo musical por escena (bombo, modo, raíz, sabor): viene de guion.MUSICA vía config
ESTILO = config.MUSICA


def golpes_bombo():
    """Tiempos globales de todos los bombos."""
    out = []
    for e in TL["escenas"]:
        pat = PATRONES[ESTILO[e["id"]]["bombo"]]
        t0, t1 = e["t0"], e["t1"]
        if e["id"] == config.PRIMERA:
            t0 = e["frases"][0]["t0"] - 0.1   # la primera escena arranca sin bombo
            t0 = e["t0"] + math.ceil((t0 - e["t0"]) / (4 * BEAT)) * 4 * BEAT
        if e["id"] == config.ULTIMA:
            t1 = e["frases"][-1]["t1"] + 0.2
        n = int(round((t1 - t0) / PASO))
        for k in range(n):
            if (k % 16) in pat:
                out.append(t0 + k * PASO)
    return np.array(sorted(out))


BOMBOS = golpes_bombo()


def env_bombo(t, caida=7.0):
    i = np.searchsorted(BOMBOS, t + 1e-6) - 1
    if i < 0:
        return 0.0
    return math.exp(-(t - BOMBOS[i]) * caida)


def fase_beat(t):
    return (t / BEAT) % 1.0
