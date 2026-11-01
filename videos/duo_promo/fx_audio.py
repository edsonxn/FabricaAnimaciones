# -*- coding: utf-8 -*-
"""SFX de ElevenLabs del anuncio de Dúo (sonidos de interfaz suaves, como los de la app; nada de golpes de tráiler).
Genera cada sonido una sola vez en sfx/<nombre>.mp3 (cuesta créditos) y arma audio/fx.wav con los sonidos anclados a las
MISMAS palabras que la animación (se importan de esc_1 / esc_2). `mezcla` suma audio/fx.wav (nivel: MEZCLA["fx"] en guion.py).
Regla «SFX repetidos no»: los sonidos frecuentes tienen variantes (burbuja_a/b, check_1/2/3, xp_1/2) y van bajitos.

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

import esc_1 as A  # noqa: E402
import esc_2 as B  # noqa: E402
from duo import TOTAL  # noqa: E402

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "burbuja_a": ("Soft bubbly chat message pop, friendly mobile messenger notification blip, very short, clean", 0.5),
    "burbuja_b": ("Gentle water droplet message sent sound, cute UI blip, very short, clean", 0.5),
    "tache": ("Quick marker pen scribble cross out on paper, short", 0.6),
    "aviso": ("Soft two-note phone notification chime, warm and friendly, clean", 1.0),
    "magia": ("Magical sparkle shimmer swell rising into a warm soft chime, logo reveal, romantic", 2.0),
    "confeti": ("Party popper pop with paper confetti fluttering, festive, short", 1.5),
    "sube": ("Smooth soft whoosh of a phone sliding up into view, airy, short", 0.9),
    "whoosh": ("Soft airy swoosh transition, smooth and light, short", 0.8),
    "aparece": ("Very soft UI swish of cards appearing, light and subtle", 0.6),
    "check_1": ("Satisfying bright UI checkmark ding, task completed, mobile app, short", 0.7),
    "check_2": ("Cheerful task complete chime with a soft pluck, mobile game reward, short", 0.7),
    "check_3": ("Bright sparkly success tick sound, positive UI confirmation, short", 0.7),
    "xp_1": ("Sparkly magical points collected chime, ascending little bells, short", 0.9),
    "xp_2": ("Soft coins and glitter collect sound, mobile game XP gained, short", 0.9),
    "llenado": ("Rising energetic progress bar filling sound, ascending sparkly synth tones building up", 3.5),
    "nivel": ("Triumphant level up fanfare, short bright brass and chimes, mobile game celebration", 2.2),
    "tic": ("Fast soft clock ticking, gentle, close", 1.2),
    "pestana": ("Soft UI tab switch click, smooth, short", 0.5),
    "taza": ("Ceramic tea mug gently set on a wooden table with a soft clink", 0.7),
    "corazon": ("Cute soft heart pop, warm bubbly UI like sound, short", 0.6),
    "toque": ("Phone screen tap, soft finger click on glass, short", 0.4),
    "latido": ("Soft warm heartbeat, two gentle thumps", 1.2),
    "remolino": ("Magical swirling whoosh with sparkles converging to the center", 1.5),
    "final": ("Bright sparkle chime success sting, uplifting, clean ending", 1.5),
}
TS_BURBUJAS = [ta for (q, *_), ta in zip(A.MENSAJES, A.TS_MSG) if q != "-"]
PISTAS = [                                  # (sonido, segundo, volumen)
    # gancho: la plática
    *[("burbuja_a" if i % 2 == 0 else "burbuja_b", ta, .45) for i, ta in enumerate(TS_BURBUJAS)],
    *[("tache", tx, .22) for (_, _, _, _, tx) in A.DIAS_GANCHO[1::2]],
    ("aviso", A.g_nunca - .05, .7), ("whoosh", 6.6, .45),
    # logo
    ("magia", A.a_hasta, .8), ("confeti", A.a_duo, .55),
    # teléfono de Ana: tres misiones
    ("sube", A.a_cada - .05, .6), ("aparece", A.a_mis - .1, .45),
    ("check_1", A.C1, .8), ("xp_1", A.C1 + .6, .45),
    ("tic", A.a_abr + .1, .3), ("check_2", A.C2, .8), ("xp_2", A.C2 + .6, .45),
    ("check_3", A.C3, .8), ("xp_1", A.C3 + .6, .45),
    # la barra
    ("whoosh", 18.0, .45), ("llenado", A.b_exp, .5), ("aparece", A.b_llen - .3, .45), ("xp_2", A.b_llena, .55),
    ("nivel", A.b_sub, .75), ("confeti", A.b_sub + .05, .6),
    # Leo: detalles y ciclo
    ("whoosh", A.T_DET, .55), ("aparece", A.d_cons, .35), ("pestana", A.d_cal - .15, .6), ("corazon", A.d_ciclo, .3),
    ("pestana", A.d_se - .2, .6), ("aparece", A.d_se + .25, .35), ("taza", A.d_llev, .6), ("check_1", A.C_CAL, .8),
    ("xp_2", A.C_CAL + .6, .4), ("whoosh", 31.75, .45), ("corazon", A.T_LIKE, .8), ("aviso", A.d_acu - .1, .75),
    # cuestionario
    ("sube", A.T_AJ - .45, .5), ("toque", B.j_pre + .05, .7), ("whoosh", B.j_y, .45), ("toque", B.j_las - .08, .7),
    ("latido", B.j_mis, .55), ("remolino", B.j_mis + .05, .45), ("confeti", B.j_ajus + .35, .35), ("aparece", B.j_ust - .1, .4),
    # cierre
    ("whoosh", B.T_CI - .25, .45), ("magia", B.c_duo - .1, .75), ("confeti", B.c_duo - .05, .45),
    ("aparece", B.c_desc - .15, .45), ("toque", B.c_emp, .7), ("xp_1", B.c_hoy + .3, .4), ("final", B.c_hoy + .95, .6),
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
        print(len(PISTAS), "sonidos;", dict(collections.Counter(n for n, _, _ in PISTAS).most_common(6)))
        print("faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")])
        return
    generar()
    from sinte import SR
    N = int(TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for n, t, v in PISTAS:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))     # sin silencio inicial: cae en su palabra
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(0.08 * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(PISTAS)} sonidos en {TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
