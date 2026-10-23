# -*- coding: utf-8 -*-
"""Pocos efectos (la música del grupo es la protagonista) → audio/fx.wav: destello y golpe al nacer el logo de la intro y
del cierre, whoosh en cada cambio de canción y un pop suave al salir cada rótulo. Piezas de sfx/ (biblioteca), con variantes.
    python sfx_tocamos.py"""
import json
import subprocess

import numpy as np
import soundfile as sf

SR = 48000
TL = json.load(open("timeline.json", encoding="utf-8"))
T = {e["id"]: e["t0"] for e in TL["escenas"]}


def leer(nombre):
    r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-i", f"sfx/{nombre}.mp3", "-f", "f32le", "-ac", "2",
                        "-ar", str(SR), "-"], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).T.copy()
    return x / max(1e-6, np.abs(x).max())


ev = [(0.25, "brillo_a", -6), (0.45, "golpe_titulo", -8), (1.2, "pop_a", -10), (1.85, "pop_b", -12),
      (T["cierre"] + 0.15, "brillo_b", -6), (T["cierre"] + 0.4, "golpe_titulo", -9), (T["cierre"] + 1.35, "pop_c", -10),
      (T["cierre"] + 2.0, "pop_d", -12)]
for j, k in enumerate(("indita", "ojos", "amor", "teodora")):
    ev += [(T[k] - 0.3, ["whoosh_a", "whoosh_b", "whoosh_c", "whoosh_d"][j], -10), (T[k] + 0.35, ["pop_a", "pop_b", "pop_c", "pop_d"][j], -13)]
out = np.zeros((2, int(TL["total"] * SR) + SR), np.float32)
cache = {}
for t, nom, g in ev:
    cache.setdefault(nom, leer(nom))
    x = cache[nom] * 10 ** (g / 20)
    i = int(t * SR)
    m = min(x.shape[1], out.shape[1] - i)
    out[:, i:i + m] += x[:, :m]
out = out[:, :int(TL["total"] * SR)]
out /= max(1.0, np.abs(out).max() / 0.98)
sf.write("audio/fx.wav", out.T, SR, subtype="PCM_24")
print(f"audio/fx.wav: {len(ev)} efectos")
