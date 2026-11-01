# -*- coding: utf-8 -*-
"""SFX de ElevenLabs de Sonic.exe: cada sonido se genera una vez en sfx/<nombre>.mp3 (cuesta créditos) y se arma audio/fx.wav con
cada golpe anclado a la MISMA palabra que la animación (anclas.py). `mezcla` suma audio/fx.wav (MEZCLA["fx"] en guion.py).
Regla del usuario (8-oct): ningún efecto domina; cada tipo suena pocas veces y con sentido (`--seco` cuenta cuántas).

    python fx_audio.py --seco     lista los sonidos, sus segundos y cuántas veces suena cada uno; no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
"""
import collections
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
from terror_pix import TOTAL  # noqa: E402

T_APAGA = A.a_apaga - 0.1                  # = escenas.T_APAGA (el monitor se apaga)
T_REENC = A.a_ocurrio - 0.3                # = escenas.T_REENC (vuelve el escritorio «normal»)
T_FUEGO = A.a_cac - 0.5                    # primer clip de la cacería

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "crt_on": ("Old CRT computer monitor turning on, electric buzz and static crackle rising, then a steady low hum", 2.5),
    "lampara": ("Small desk lamp switching on, plastic click and a faint electric buzz, close", 1.0),
    "papel": ("Paper note being crumpled and unfolded slowly, close, dry rustle", 1.2),
    "lector": ("Old computer CD-ROM drive: tray sliding closed with a motor whine, disc spinning up, seeking clicks and whirring", 4.0),
    "chiptune": ("Slowed down, detuned and distorted 16-bit video game title jingle, creepy, warped like a dying cassette", 3.0),
    "oxido": ("Rusty metal creaking and scraping slowly, dark, horror", 2.0),
    "agua": ("Thick dark liquid sloshing slowly, heavy and unsettling, low", 3.0),
    "estatica": ("TV static noise burst, harsh white noise hiss, short and sharp", 1.2),
    "glitch": ("Digital glitch stutter with tape rewind squeal, short, unsettling", 1.0),
    "golpe": ("Deep low horror impact boom, sub bass hit with a long dark reverberant tail, cinematic", 3.0),
    "latido": ("Slow deep heartbeat thumping, dark and tense, three beats", 3.0),
    "risa": ("Distorted low demonic laughter with echo, unsettling and slow, horror", 3.0),
    "corte": ("Violent digital tear: a glitchy distorted cry cut off abruptly by a burst of static, short, horror", 1.3),
    "choque": ("Metallic crunch of a machine being smashed, sparks and a burst of static, short", 1.3),
    "susurro": ("Faint ghostly whisper, breathy and unintelligible, very close, horror", 2.5),
    "apagado": ("Old CRT television shutting off, high pitched electronic whine collapsing with a final low thump", 1.8),
    "goteo": ("Slow thick liquid dripping onto fabric, three heavy drops, quiet room", 2.0),
    "error": ("Short harsh old computer error beep, dry, small speaker", 0.6),
    "clic": ("Single computer mouse click, close and dry", 0.4),
    "ping": ("Small cold digital notification blip, short", 0.5),
    "sello": ("Heavy rubber stamp hitting paper, dull thump, short", 0.7),
    "borrar": ("Fast digital deletion sweep, descending glitchy erase, short", 1.4),
    "polvo": ("Glassy disc crumbling into fine dust, soft dissolving shimmer, quiet", 1.6),
    "cartucho": ("Video game cartridge pushed into a console slot with a plastic click and a dull clunk, close", 1.0),
    "pantallas": ("Many small old monitors and screens flickering on at once, electric buzz and crackle, rising", 2.5),
    "disco_mesa": ("Plastic disc set down on a wooden desk, soft tap and slide, close", 0.8),
    "pasos": ("Slow soft footsteps on a wooden floor in a dark quiet room, close, right behind the listener", 3.0),
}
PISTAS = [                                  # (sonido, segundo, volumen)
    # cd: el disco llega al lector
    ("crt_on", A.T_ON - 0.1, .7), ("lampara", A.a_cd - 0.4, .5), ("papel", A.a_nota - 0.05, .5),
    ("lector", A.T_DISCO1 - 1.0, .8),
    # titulo: se corrompe
    ("chiptune", A.T_TIT, .6), ("oxido", A.a_oxid - 0.1, .5), ("golpe", A.a_666 - 0.05, .8), ("agua", A.a_roja, .6),
    ("estatica", A.a_start + 0.4, .5),
    # niveles: la cacería
    ("latido", T_FUEGO, .7), ("risa", A.a_ojos - 0.3, .8),
    ("corte", A.a_tails - 0.3, .7), ("corte", A.a_knuc - 0.3, .8), ("choque", A.a_vill - 0.3, .8),
    ("susurro", A.a_queda - 0.6, .7), ("latido", A.a_queda - 0.2, .8),
    # final: el peluche
    ("apagado", T_APAGA, .9), ("golpe", A.a_pel - 0.05, 1.0), ("goteo", A.a_sang, .6), ("crt_on", T_REENC, .6),
    # autor: la verdad
    ("golpe", A.a_fic - 0.1, .7), ("error", A.a_nohab - 0.05, .6), ("glitch", A.a_idea, .5),
    ("clic", A.a_corres - 0.15, .8), ("glitch", A.a_inq, .5),
    # legado: cada hecho, una página
    ("ping", A.a_2012 - 0.05, .7), ("ping", A.a_pew - 0.05, .7), ("clic", A.a_desc - 0.1, .7),
    ("borrar", A.a_borro - 0.05, .7), ("sello", A.a_borro + 0.2, .8), ("sello", A.a_mal, .7), ("sello", A.a_clich, .7),
    ("ping", A.a_blog - 0.05, .7), ("glitch", A.a_rebel, .5),
    # cierre: algo entró al cuarto
    ("cartucho", A.a_ben, .7), ("polvo", A.a_real, .7), ("pantallas", A.a_gente - 0.3, .7), ("estatica", A.a_espe - 0.2, .4),
    ("disco_mesa", A.a_disc2, .7), ("pasos", A.a_start2 - 1.2, .5), ("golpe", A.a_start2 - 0.05, 1.0), ("estatica", A.a_start2, .6),
    ("apagado", A.T_FIN - 0.05, .8),
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
        cuenta = collections.Counter(n for n, _, _ in PISTAS)
        print(len(PISTAS), "golpes en", len(cuenta), "sonidos; repetidos:", {n: c for n, c in cuenta.items() if c > 1})
        print("faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")])
        sin_usar = [n for n in SFX if n not in cuenta]
        if sin_usar:
            print("definidos y sin usar:", sin_usar)
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
