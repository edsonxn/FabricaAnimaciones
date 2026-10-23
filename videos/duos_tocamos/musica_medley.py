# -*- coding: utf-8 -*-
"""Medley de las canciones del grupo → audio/musica.wav (48 kHz). Cada sección de canción suena COMPLETA (con las voces
del grupo) desde guion.CANCION[s][1]; entre canciones, fundido de potencia constante de 0,6 s centrado en el cambio.
La intro lleva el instrumental de La indita (Demucs) y entra la voz al empezar la canción; el cierre sigue el corrido sin
voces (el instrumental) y se desvanece.    python musica_medley.py"""
import json
import runpy

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

SR = 44100
G = runpy.run_path("guion.py")
ST, CANCION = G["STEMS"], G["CANCION"]
TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}
CRUCE = 0.6
_c = {}


def pista(n, stem):
    if (n, stem) not in _c:
        ruta = f"{ST}/{n}.wav" if stem == "mix" else f"{ST}/htdemucs/{n}/{stem}.wav"
        x, sr = sf.read(ruta, dtype="float32", always_2d=True)
        assert sr == SR
        _c[(n, stem)] = x.T
    return _c[(n, stem)]


def tramo(n, src0, t0, t1, voz_desde=None, voz_hasta=None):
    """Pieza `n` puesta en [t0, t1] de la línea de tiempo (src0 suena en t0); con voces solo entre voz_desde y voz_hasta."""
    a0, a1 = int(round(t0 * SR)), int(round(t1 * SR))
    s0 = int(round(src0 * SR))
    mix = pista(n, "mix")[:, s0:s0 + (a1 - a0)]
    inst = pista(n, "no_vocals")[:, s0:s0 + (a1 - a0)]
    tt = t0 + np.arange(mix.shape[1]) / SR
    u = np.ones_like(tt)
    if voz_desde is not None:
        u = np.minimum(u, np.clip((tt - voz_desde) / 0.3 + 0.5, 0, 1))
    if voz_hasta is not None:
        u = np.minimum(u, np.clip((voz_hasta - tt) / 0.8 + 0.5, 0, 1))
    seg = inst * (1 - u) + mix * u
    ref = pista(n, "mix")[:, int(src0 * SR):int((src0 + 20) * SR)]
    seg = seg * (0.12 / (np.sqrt(np.mean(ref ** 2)) + 1e-9))       # mismo nivel entre canciones
    return a0, seg


def main():
    out = np.zeros((2, int(round(TOTAL * SR))), np.float32)
    secs = [k for k in ("indita", "ojos", "amor", "teodora")]
    for i, k in enumerate(secs):
        n, src, _ = CANCION[k]
        t0, t1 = ESC[k]["t0"], ESC[k]["t1"]
        a = t0 - CRUCE / 2
        b = t1 + CRUCE / 2
        voz_desde = voz_hasta = None
        if k == "indita":                                   # la intro (instrumental) es parte del mismo tramo
            a, voz_desde = 0.0, t0
        if k == "teodora":                                  # sigue en el cierre, ya sin voces
            b, voz_hasta = TOTAL, t1
        a0, seg = tramo(n, src - (t0 - a), a, b, voz_desde, voz_hasta)
        m = seg.shape[1]
        env = np.ones(m, np.float32)
        nc = int(CRUCE * SR)
        if a > 0:
            env[:nc] = np.sin(np.linspace(0, np.pi / 2, nc))
        if b < TOTAL:
            env[-nc:] *= np.cos(np.linspace(0, np.pi / 2, nc))
        out[:, a0:a0 + m] += seg * env
        print(f"{k:8s} {n}  {a:6.2f}-{b:6.2f}  pieza desde {src - (t0 - a):6.2f}s")
    nf = int(3.0 * SR)
    out[:, -nf:] *= np.linspace(1, 0, nf) ** 1.6
    out[:, :int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))
    out /= max(1.0, np.abs(out).max() / 0.95)
    out = resample_poly(out, 160, 147, axis=1).astype(np.float32)       # 44,1 → 48 kHz (el de la mezcla)
    sf.write("audio/musica.wav", out.T, 48000, subtype="PCM_24")
    print(f"audio/musica.wav {TOTAL:.1f}s")


if __name__ == "__main__":
    main()
