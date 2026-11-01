# -*- coding: utf-8 -*-
"""SFX y ambientes reales de «No vuelve a pasar» (lo que el sintetizador de nucleo/sfx.py no tiene). TODOS salen de la biblioteca
(`fab.py biblioteca sfx usar <id> no_vuelve --nombre <n>`, 21-oct-2026: ElevenLabs casi sin saldo) y se arma audio/fx.wav con los
tiempos de escenas.py. El plato que se rompe no está en la biblioteca: se sintetiza aquí (ruido + astillas de barro).
`mezcla` suma audio/fx.wav con el nivel MEZCLA["fx"] de guion.py.

    python fx_audio.py --seco     lista sonidos y tiempos
    python fx_audio.py            escribe audio/fx.wav
(desde la carpeta del video, con PYTHONPATH="<video>;C:\\FabricaAnimaciones\\nucleo")
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402

import escenas as S  # noqa: E402

# nombre: fundido de salida (s) · origen en la biblioteca (para catalogar de vuelta, no se regenera)
FUNDIDO = {"troca": 1.0, "portazo": 0.2, "grillos": 1.2, "tarde": 1.2, "alba": 1.2, "gallo": 0.6, "risas": 0.4, "golpe": 0.4,
           "toc": 0.3, "reja": 0.5, "plato": 0.3}
X = S.FX_T
PISTAS = [                                  # (sonido, segundo, volumen[, al revés])
    # la feria: el pueblo de fondo (la banda la pone la música)
    ("tarde", 0.0, .30), ("risas", 4.0, .22),
    # el clima: la troca llega (al revés: se acerca), frenón, portazo
    ("tarde", S.c0_, .22), ("troca", X["troca_llega"], .40, True), ("golpe", X["frenon"], .30), ("portazo", X["portazo"], .85),
    # el silencio
    ("grillos", S.s0_, .30),
    # debajo de la mesa: un golpe sordo en la mesa y el plato que se rompe
    ("grillos", S.m0_, .18), ("golpe", X["grito"], .30), ("plato", X["plato"], .80),
    # las flores
    ("alba", S.fl0, .40), ("gallo", S.fl0 + 0.8, .30),
    # Fer
    ("tarde", S.fe0, .32), ("risas", S.fe_esa - 0.2, .35),
    # el corredor: risas, el puñetazo a la pared
    ("risas", S.k0, .30), ("golpe", X["golpe"], .95),
    # el perdón: la reja de Fer
    ("tarde", S.p0, .22), ("reja", X["reja"], .35),
    # las muñecas y el patio
    ("grillos", S.u0, .25), ("grillos", S.pa0, .45), ("grillos", S.pa0 + 13.0, .40),
    # el alba: toca la puerta de orientación; la calle al amanecer
    ("toc", S.a_toque, .70), ("alba", S.a_y - 0.3, .45), ("gallo", S.a_y + 0.8, .40),
    # el epílogo
    ("tarde", S.e0_, .32), ("risas", S.e0_ + 1.5, .25), ("tarde", S.e0_ + 15.0, .25),
]


def plato_roto(SR):
    """Plato de barro que se estrella: golpe de ruido grave + astillas agudas que rebotan."""
    rng = np.random.default_rng(5)
    n = int(1.1 * SR)
    t = np.arange(n) / SR
    x = rng.normal(0, 1, n) * np.exp(-t * 18)
    x = np.convolve(x, np.ones(6) / 6, "same") * 0.9
    for k in range(14):
        t0 = 0.01 + 0.5 * rng.random() ** 2
        f = 1800 + 3800 * rng.random()
        e = np.clip(t - t0, 0, None)
        x += (t >= t0) * np.sin(2 * np.pi * f * e) * np.exp(-e * (60 + 80 * rng.random())) * (0.5 * rng.random() + 0.2)
    x /= np.abs(x).max() + 1e-9
    return np.vstack([x, x]).astype(np.float32)


def main():
    if "--seco" in sys.argv:
        for p in sorted(PISTAS, key=lambda x: x[1]):
            print(f"{p[1]:7.2f}  {p[0]:10s} {p[2]}{'  (al revés)' if len(p) > 3 else ''}")
        print(len(PISTAS), "pistas; faltan:", [n for n in FUNDIDO if n != "plato" and not os.path.exists(f"sfx/{n}.mp3")])
        return
    from sinte import SR
    N = int(S.TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for p in PISTAS:
        n, t, v = p[:3]
        rev = len(p) > 3 and p[3]
        if (n, rev) not in cache:
            if n == "plato":
                x = plato_roto(SR)
            else:
                x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
                x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
                if rev:
                    x = x[:, ::-1]
                ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))
                x = x[:, ini:]
            x = x / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(FUNDIDO[n] * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            g = min(int((0.8 if rev else 0.05) * SR), x.shape[1])
            x[:, :g] *= np.linspace(0, 1, g, dtype=np.float32)
            cache[(n, rev)] = np.ascontiguousarray(x, np.float32)
        x = cache[(n, rev)]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(PISTAS)} pistas en {S.TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
