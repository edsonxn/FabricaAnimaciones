# -*- coding: utf-8 -*-
"""SFX de ElevenLabs para el terror: cada sonido se genera una vez en sfx/<nombre>.mp3 (cuesta créditos) y se arma audio/fx.wav con
cada golpe anclado a la MISMA palabra que la animación (anclas.py). `mezcla` suma audio/fx.wav (MEZCLA["fx"] en guion.py).

    python fx_audio.py --seco     lista los sonidos y sus segundos, no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
"""
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import requests  # noqa: E402
import soundfile as sf  # noqa: E402

import anclas as A  # noqa: E402
from pix import TOTAL  # noqa: E402

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "crt_on": ("Old CRT television turning on, electric buzz and static crackle rising, then a steady low hum", 2.5),
    "foco": ("Old spotlight switching on, heavy electric click and a faint hum", 1.2),
    "cartel": ("Cardboard sign swinging and tapping softly against a wall, short", 0.8),
    "cartucho": ("Video game cartridge pushed into a console slot with a plastic click and a dull clunk, close", 1.0),
    "estatica": ("TV static noise burst, harsh white noise hiss, short and sharp", 1.2),
    "glitch": ("Digital glitch stutter with tape rewind squeal, short, unsettling", 1.0),
    "golpe": ("Deep low horror impact boom, sub bass hit with a long dark reverberant tail, cinematic", 3.0),
    "reloj": ("Fast clock ticking that accelerates and then stops abruptly", 2.2),
    "risa": ("Distorted creepy laughter of a man, unsettling manic laugh with echo, horror", 3.0),
    "agua": ("Muffled underwater ambience, slow bubbles rising, deep and cold", 6.0),
    "susurro": ("Faint ghostly whisper, breathy and unintelligible, very close, horror", 2.5),
    "ping": ("Small cold digital notification blip, short", 0.5),
    "piedra": ("Heavy stone scraping slowly on a wooden floor, low rumble, horror", 2.5),
    "latido": ("Slow deep heartbeat thumping, dark and tense, three beats", 3.0),
    "apagado": ("Old CRT television shutting off, high pitched electronic whine collapsing with a final low thump", 1.8),
}
PISTAS = [                                  # (sonido, segundo, volumen)
    ("crt_on", A.T_ON - 0.1, .8),
    ("foco", A.a_car - 0.3, .6), ("cartel", A.a_ven + 0.4, .5),
    ("cartucho", A.T_INS1 - 0.05, .9), ("estatica", A.a_par - 0.1, .5), ("golpe", A.a_ben1 - 0.05, .9),
    ("glitch", A.T_JUEGO, .5), ("estatica", A.a_fal, .5), ("reloj", A.a_ter - 0.2, .5), ("golpe", A.T_SALTO, .9),
    ("glitch", A.T_SALTO, .5), ("golpe", A.a_vac - 0.05, .7),
    ("glitch", A.a_vend - 0.05, .5), ("risa", A.a_rei - 0.2, .8), ("piedra", A.a_est2 + 0.2, .6), ("susurro", A.a_mir, .5),
    ("estatica", A.a_rel - 0.45, .6), ("agua", A.a_rel, .7), ("golpe", A.a_ben2, .5), ("estatica", A.a_desde, .5),
    ("susurro", A.a_hab, .8), ("golpe", A.a_fic - 0.1, .7),
    ("ping", A.a_vid - 0.05, .8), ("ping", A.a_web - 0.05, .8), ("ping", A.a_men - 0.05, .8), ("estatica", A.a_mil, .6),
    ("glitch", A.a_sab, .6), ("golpe", A.a_jue - 0.05, 1.0), ("estatica", A.a_jue, .7),
    ("latido", A.a_alg, .8), ("piedra", A.a_alguien - 0.1, .6), ("golpe", A.a_ben3 - 0.05, 1.0), ("estatica", A.a_ben3, .6),
    ("apagado", A.T_OFF, .9),
]


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
    if "--seco" in sys.argv:
        for n, t, v in sorted(PISTAS, key=lambda x: x[1]):
            print(f"{t:7.2f}  {n:10s} {v}")
        print(len(PISTAS), "golpes;", "faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")])
        return
    generar()
    from sinte import SR
    N = int(TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for n, t, v in PISTAS:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(0.08 * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    pico = float(np.abs(out).max())
    if pico > 0.95:
        out *= 0.95 / pico
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(PISTAS)} golpes en {TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
