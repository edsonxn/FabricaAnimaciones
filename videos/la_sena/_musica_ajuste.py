# -*- coding: utf-8 -*-
"""Silencios del guion que Lyria no respeta (20-oct-2026): la gotera va casi sin música (solo lluvia y la gota) y el negro tras
«pero seguía ahí» es silencio total. Correr DESPUÉS de `lyria_tramos.py armar` (que reescribe audio/musica.wav) y antes de `mezcla`.
    python _musica_ajuste.py"""
import numpy as np
import soundfile as sf

import escenas as S

BAJAS = [                                       # (desde, hasta, dB, fundido s)
    (S.G1 + 1.0, S.G7 - 0.6, -16.0, 2.0),       # la gotera: la lluvia manda
    (S._ESC["graduacion"]["t1"] - 4.0, S._ESC["graduacion"]["t1"] - 0.2, -60.0, 0.5),   # negro con silencio total
]

a, sr = sf.read("audio/musica.wav", dtype="float32")
t = np.arange(len(a), dtype=np.float32) / sr
g_db = np.zeros_like(t)
for t0, t1, db, f in BAJAS:
    sube = np.clip((t - t0) / f, 0, 1)
    baja = np.clip((t1 - t) / f, 0, 1)
    g_db = np.minimum(g_db, db * np.minimum(sube, baja))
a *= (10 ** (g_db / 20))[:, None] if a.ndim > 1 else 10 ** (g_db / 20)
sf.write("audio/musica.wav", a, sr, subtype="FLOAT")
print("audio/musica.wav ajustada:", [(round(x, 1), round(y, 1), d) for x, y, d, _ in BAJAS])
