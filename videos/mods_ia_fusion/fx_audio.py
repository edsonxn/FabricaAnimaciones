# -*- coding: utf-8 -*-
"""SFX de ElevenLabs para un video DIBUJADO POR CÓDIGO (el motor `secuencia` tiene su propio `fab.py <v> fx`).
Genera cada sonido una sola vez en sfx/<nombre>.mp3 (cuesta créditos) y arma audio/fx.wav con los golpes anclados a las
MISMAS palabras que la animación (se importan de esc_a / esc_b). `mezcla` suma audio/fx.wav (nivel: MEZCLA["fx"] en guion.py).

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

import esc_a as A  # noqa: E402
import esc_b as B  # noqa: E402
from pix import INI, TOTAL  # noqa: E402

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "golpe": ("Deep punchy cinematic bass impact hit with a short tail, trailer style", 1.5),
    "golpe2": ("Tight sub bass thump hit, short and dry, modern trailer", 1.0),
    "pop": ("Bright soft UI pop, bubble click, very short, clean", 0.5),
    "whoosh": ("Fast airy cinematic whoosh swoosh transition, short", 1.0),
    "glitch": ("Digital glitch static burst, data corruption stutter, short", 1.0),
    "datos": ("Fast digital data transfer, rapid computer blips and beeps, processing, futuristic interface", 4.0),
    "tecleo": ("Fast mechanical keyboard typing, close and crisp", 3.0),
    "subida": ("Tense electronic riser sweep building up fast, ending abruptly", 2.0),
    "reja": ("Heavy metal prison bars slamming shut with a loud reverberant clang", 2.0),
    "explosion": ("Punchy dynamite explosion boom with debris, short", 2.0),
    "campana": ("Bright positive success chime, single ding, clean", 1.0),
    "sello": ("Heavy rubber stamp slammed on a wooden desk, single thud", 0.8),
}
U, R, V, C = A, B, B, B
PISTAS = [                                  # (sonido, segundo, volumen)
    # gancho
    ("golpe", A.tM, .9), ("pop", A.tD, .5), ("golpe", A.tS, 1.0), ("sello", A.tN, .9), ("pop", A.tB, .7), ("whoosh", A.tV, .7),
    ("explosion", A.tT + .1, .9), ("whoosh", A.tR, .8), ("glitch", A.tR + .1, .4), ("golpe2", A.tCo - .15, .7), ("pop", A.tDos, .7),
    ("pop", A.tDos + .28, .7), ("glitch", A.tMi - .05, .8),
    # puente
    ("whoosh", A.T_PUENTE, .6), ("golpe", A.uP - .18, .8), ("whoosh", A.uJ, .8), ("golpe2", A.uJ + .42, .7), ("pop", A.uAl, .6),
    ("pop", A.uSep - .05, .6), ("glitch", A.uEsc, .6), ("pop", A.uVen, .6), ("pop", A.uSon, .6), ("golpe", A.uMem - .05, .9),
    ("pop", A.uLeer, .5), ("pop", A.uEscr, .5), ("whoosh", A.uCi - .35, .7), ("datos", A.uCi, .55), ("datos", A.uCi + 3.9, .55),
    ("pop", A.uJug - .15, .7), ("pop", A.uBlo - .15, .7), ("pop", A.uGol - .2, .7), ("whoosh", INI("puente", 5) - .45, .6),
    ("pop", A.uMan, .6), ("pop", A.uMan + .22, .6), ("pop", A.uMan + .44, .6), ("pop", A.uMun, .6), ("pop", A.uEne, .6), ("pop", A.uCho, .6),
    ("golpe2", A.uNin + .25, .9), ("pop", A.uProp - .25, .5), ("pop", A.uProp - .1, .5),
    # límite
    ("golpe", A.lLim, 1.0), ("reja", A.lAtr + .12, 1.0), ("pop", A.lMot - .25, .7), ("subida", A.T_FIN_A - 1.9, .7),
    # reescritura
    ("golpe2", 52.05, .9), ("golpe2", B.rNo, .6), ("golpe", B.rRe, .9), ("tecleo", B.rRe + .15, .6), ("golpe", B.rRe + .55, 1.0),
    ("whoosh", B.T_R1, .6), ("pop", B.rJue, .6), ("sello", B.rCod + .15, .8), ("datos", B.rMil, .6), ("golpe", B.rImp - .08, .9),
    ("glitch", B.rImp, .5), ("whoosh", B.T_R2, .6), ("golpe", B.rRec, .9), ("pop", B.rTra - .15, .7), ("pop", B.rOtra - .1, .7),
    ("sello", B.rSin - .05, .9), ("whoosh", B.T_R3, .6), ("golpe", B.rDec, .9), ("tecleo", B.rCons, .55), ("tecleo", B.rCons + 2.6, .55),
    ("campana", B.rFun + .2, .5), ("campana", B.rFun + 1.6, .5), ("campana", B.rPers - .3, .7), ("whoosh", B.T_R4, .8),
    ("golpe", B.rSka, .9), ("pop", B.rMot, .7), ("pop", B.rLib, .7), ("subida", B.rLin - 1.2, .5), ("golpe", B.rLin + .45, 1.0),
    ("glitch", B.T_V - .3, .8),
    # la verdad
    ("pop", B.vDic - .15, .7), ("campana", B.vSem, .5), ("sello", B.vNo - .05, 1.0), ("glitch", B.vNo, .5), ("whoosh", B.T_V1, .6),
    ("pop", B.vAnt - .1, .6), ("golpe", B.vDos - .1, .9), ("tecleo", B.vDos, .4), ("pop", B.vMano - .25, .6), ("whoosh", B.T_V2, .6),
    ("golpe2", B.vNada - .6, .6), ("golpe", B.vNada, 1.0), ("whoosh", B.vConv - .1, .6), ("datos", B.vConv, .5), ("subida", B.vVel - .3, .6),
    ("whoosh", B.T_C - .3, .9),
    # cierre
    ("golpe", B.T_C, .8), ("golpe2", B.cFue - .25, .7), ("pop", B.cReg, .6), ("pop", B.cRee - .1, .6), ("whoosh", B.cMez - .15, .7),
    ("golpe", B.cMez + .4, 1.0), ("campana", B.cMez + .45, .6), ("pop", B.cLim - .2, .5), ("pop", B.cSab - .25, .5), ("sello", B.cSab + .9, .6),
    ("golpe2", B.cAtr, .7), ("golpe", B.cIma, 1.0), ("campana", B.cIma + .05, .6), ("whoosh", B.T_C2, .7), ("golpe2", B.cQue + .35, .8),
    ("pop", B.cQue + .25, .6), ("pop", B.cQue + .45, .6), ("campana", B.cQue + .9, .7),
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
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))     # sin silencio inicial: el golpe cae en su palabra
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
    print(f"audio/fx.wav: {len(PISTAS)} golpes en {TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
