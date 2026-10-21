# -*- coding: utf-8 -*-
"""SFX y ambientes de ElevenLabs para «La seña» (lo que el sintetizador de nucleo/sfx.py no tiene: risas, grillos, la troca,
el gallo, la lluvia en la lámina, la combi). Cada sonido se genera UNA vez en sfx/<nombre>.mp3 (cuesta créditos; tts_eleven.post
pasa a la cuenta de respaldo si una se queda sin saldo) y se arma audio/fx.wav con los tiempos de escenas.py.
`mezcla` suma audio/fx.wav con el nivel MEZCLA["fx"] de guion.py.

    python fx_audio.py --seco     lista sonidos y tiempos, no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
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

SFX = {                                    # nombre: (prompt en inglés, segundos, fundido de salida s)
    "risas": ("Two young boys laughing happily outdoors on a quiet street, childish giggles, no music", 3.0, 0.3),
    "bici": ("A small kid's bicycle rolling fast down a steep cement street, chain rattling, tires on rough pavement", 6.0, 0.4),
    "grillos": ("Crickets chirping at night in a quiet small town, a dog barking far away, very calm", 14.0, 1.0),
    "troca": ("An old pickup truck engine starting and driving away down a street at night, fading into the distance", 6.0, 1.0),
    "tarde": ("Peaceful small town evening ambience: distant birds, children playing far away, a faraway rooster, soft breeze",
              16.0, 1.2),
    "zanates": ("Great-tailed grackles calling at sunset, loud whistles and clacks of black birds, outdoors", 6.0, 0.8),
    "lluvia": ("Heavy rain drumming on a corrugated metal roof, heard from inside a small kitchen at night", 22.0, 1.5),
    "aviso": ("A short soft smartphone message notification sound", 1.0, 0.1),
    "gallo": ("A rooster crowing at dawn in the countryside, slightly distant", 4.0, 0.6),
    "alba": ("Soft morning wind in a dry canyon at dawn with a few distant birds", 12.0, 1.2),
    "combi": ("A minibus van passing fast on a two-lane highway, engine roar and whoosh, then fading away", 5.0, 0.8),
    # tramo 3 (21-oct)
    "vibra": ("A smartphone vibrating on a wooden kitchen table, two short buzzes, quiet room", 2.0, 0.2),
    "moto": ("A motorcycle passing slowly on a dirt street outside a house, heard from inside, engine fading away", 5.0, 1.0),
    "fiesta": ("Outdoor school graduation ceremony in a small Mexican town: murmuring families, children, plastic chairs, light "
               "breeze, no music", 22.0, 1.5),
    "aplausos": ("A small crowd of families applauding warmly outdoors, a few cheers", 4.0, 0.8),
}
G1, G3, G7 = S.G1, S.G3, S.G7
PISTAS = [                                  # (sonido, segundo, volumen)
    # la cuesta
    ("bici", 1.0, .45), ("risas", S.CHOCA + 0.15, .8), ("risas", S.c_ya + 1.2, .5),
    # la puerta
    ("grillos", S.p0 - 0.3, .5), ("troca", S.p_desde + 0.4, .55),
    # la azotea
    ("tarde", S.a0, .45), ("tarde", S.a0 + 15.5, .45), ("zanates", S.a_ya + 0.6, .35), ("tarde", S.a0 + 30.0, .30),
    # la gotera
    ("lluvia", G1, .75), ("aviso", G3 + 0.4, .7),
    # la bendición
    ("alba", G7 + 0.2, .45), ("gallo", G7 + 1.0, .45), ("combi", S.b_jal + 0.2, .75),
    # los tenis
    ("tarde", S.e0, .22), ("vibra", S.VIBRA, .6), ("moto", S.MOTO - 0.4, .6),
    # el mensaje
    ("grillos", S.m0, .5), ("grillos", S.m0 + 12.0, .45), ("aviso", S.AVISO2, .7),
    # la recámara
    ("alba", S.r0, .35), ("gallo", S.r0 + 0.6, .4),
    # la graduación y la reja (luego, silencio total)
    ("fiesta", S.g0, .55), ("aplausos", S.GR3 + 0.6, .6), ("aplausos", S.GR4, .5), ("tarde", S.REJA1, .30),
    # el epílogo
    ("tarde", S.q0, .40), ("bici", S.q0 + 0.3, .40), ("zanates", S.q0 + 1.0, .30), ("risas", S.ABAJO - 0.3, .45),
]
SILENCIO = (S._ESC["graduacion"]["t1"] - 4.0, S._ESC["graduacion"]["t1"] - 0.2, 0.5)   # el negro: como _musica_ajuste.py


def generar():
    import tts_eleven as E
    os.makedirs("sfx", exist_ok=True)
    gasto = 0
    for n, (txt, dur, _) in SFX.items():
        if os.path.exists(f"sfx/{n}.mp3"):
            continue
        r = E.post("sound-generation", timeout=180, json=dict(text=txt, duration_seconds=min(float(dur), 22), prompt_influence=0.45))
        if r.status_code != 200:
            raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
        open(f"sfx/{n}.mp3", "wb").write(r.content)
        gasto += int(r.headers.get("character-cost") or 0)
        print(f"  sfx/{n}.mp3  {dur} s", flush=True)
    print(f"ElevenLabs: {gasto} créditos en efectos")


def main():
    if "--seco" in sys.argv:
        for n, t, v in sorted(PISTAS, key=lambda x: x[1]):
            print(f"{t:7.2f}  {n:10s} {v}")
        print(len(PISTAS), "pistas; faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")])
        return
    generar()
    from sinte import SR
    N = int(S.TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for n, t, v in PISTAS:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(SFX[n][2] * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            g = min(int(0.05 * SR), x.shape[1])
            x[:, :g] *= np.linspace(0, 1, g, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    a, b, f = SILENCIO
    tt = np.arange(N, dtype=np.float32) / SR
    out *= 1.0 - np.minimum(np.clip((tt - a) / f, 0, 1), np.clip((b - tt) / f, 0, 1))
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(PISTAS)} pistas en {S.TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
