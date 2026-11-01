# -*- coding: utf-8 -*-
"""SFX de ElevenLabs para el DRAMA (lo pidió el usuario): impactos, subidas, truenos, la señal que se rompe, tonos de llamada…
Se generan una sola vez en sfx/<nombre>.mp3 (cuesta créditos) y se arman en audio/fx.wav con cada golpe anclado a la MISMA palabra
que la animación (los tiempos salen de los `t_*` de cada escena). `mezcla` suma audio/fx.wav (nivel: MEZCLA["fx"] en guion.py).

    python fx_audio.py --seco     lista los sonidos y sus segundos, no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import requests  # noqa: E402
import soundfile as sf  # noqa: E402

import escenas as S  # noqa: E402

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
IDS = [e["id"] for e in TL["escenas"]]
E = {e["id"]: S.CLASES[e["id"]](e, IDS.index(e["id"])) for e in TL["escenas"]}

SFX = {                                    # nombre: (prompt en inglés, segundos). Sonidos propios de este video.
    "pulso_grave": ("Deep low slow pulse thump, like a heartbeat under a cold floor, suspense, noir", 3.0),
    "cerrojo": ("Heavy steel padlock snapping shut and a combination dial spinning, close and tense", 2.5),
    "golpe_puerta": ("Heavy steel door slamming shut in an empty corridor, reverberant echo, noir", 3.0),
    "alarma_suave": ("Muffled distant security alarm, three soft rising chirps, far away in a building", 2.5),
    "estatica": ("Old radio static burst that cuts out abruptly, short and eerie", 1.5),
    "cristal": ("A fingernail tapping on thick glass, cold and echoing in a silent room", 2.0),
    "sello_metal": ("Heavy rubber stamp hitting paper on a metal desk, sharp and final", 1.5),
}


def pistas():
    g, pu, it, fi, ci = (E[k] for k in ("gancho", "puerta", "interrogatorio", "fingir", "cierre"))
    # pocos golpes y variados: cada sonido marca UN tipo de momento (nada de un mismo sonido por cada pieza)
    P = [
        ("pulso_grave", g.t_llego - 0.3, .5), ("sello_metal", g.t_expe + 0.2, .6),
        ("cerrojo", pu.t_2024 + 0.2, .6), ("golpe_puerta", pu.t_nofun + 0.2, .9),
        ("alarma_suave", it.t_apagar, .6), ("estatica", it.t_conf, .5), ("cristal", it.t_inv + 0.1, .5),
        ("pulso_grave", fi.t_razon - 0.2, .6), ("sello_metal", fi.t_real, .9),
        ("cerrojo", ci.t_alf + 0.6, .6), ("estatica", ci.t_caso + 0.4, .5), ("pulso_grave", ci.t_caso + 0.9, .7),
    ]
    return P


def generar():
    clave = open(os.path.join(AQUI, "..", "..", "canales", "tokens", "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
    os.makedirs("sfx", exist_ok=True)
    gasto = 0
    for n, (txt, dur) in SFX.items():
        if os.path.exists(f"sfx/{n}.mp3"):
            continue
        for intento in range(4):
            r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers={"xi-api-key": clave}, timeout=180,
                              json=dict(text=txt, duration_seconds=max(0.5, float(dur)), prompt_influence=0.5))
            if r.status_code == 200:
                open(f"sfx/{n}.mp3", "wb").write(r.content)
                gasto += int(r.headers.get("character-cost") or 0)
                print(f"  sfx/{n}.mp3  {dur} s", flush=True)
                break
            if r.status_code not in (429, 500, 502, 503):
                raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
            time.sleep(5 * (intento + 1))
    print(f"ElevenLabs: {gasto} créditos en efectos")


def main():
    P = pistas()
    if "--seco" in sys.argv:
        for n, t, v in sorted(P, key=lambda x: x[1]):
            print(f"{t:7.2f}  {n:10s} {v}")
        print(len(P), "golpes;", "faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")],
              "| segundos a generar:", sum(d for n, (_, d) in SFX.items() if not os.path.exists(f"sfx/{n}.mp3")))
        return
    generar()
    SR = 48000
    N = int(TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for n, t, v in P:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))     # sin silencio inicial: el golpe cae en su palabra
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(0.15 * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(P)} golpes en {TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
