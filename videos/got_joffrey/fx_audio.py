# -*- coding: utf-8 -*-
"""SFX de ElevenLabs para el DRAMA de «¿Quién envenenó al rey?»: se generan una vez en sfx/<nombre>.mp3 (los genéricos se copiaron
de videos/informante_2027/sfx/) y se arman en audio/fx.wav con cada golpe anclado a la MISMA palabra que la animación (los `t_*`
de cada escena). `mezcla` suma audio/fx.wav (nivel: MEZCLA["fx"] en guion.py).

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

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "impacto": ("", 3.0), "impacto2": ("", 2.0), "subida": ("", 3.0), "trueno": ("", 5.0), "latido": ("", 4.0),
    "zumbido": ("", 5.0), "susurro": ("", 2.5),
    "copa": ("Heavy golden metal goblet dropped on a stone floor in a large hall, clanging, bouncing and rolling, reverberant", 3.0),
    "palomas": ("A flock of doves bursting out and flying away, loud wing flapping, close", 3.0),
    "tos": ("A young man coughing and then choking, gasping for air, struggling to breathe, dramatic", 4.0),
    "grito": ("Medieval crowd in a stone banquet hall gasping in shock, a woman screams, chairs scraping, panic", 4.0),
    "ballesta": ("Crossbow shot, sharp string twang and a bolt whooshing, then a dull thud into a body", 1.5),
    "campanas": ("Distant medieval city church bells tolling slowly at dawn, melancholic, with light wind", 6.0),
}


def pistas():
    g, vi, ba, mu, ac, ve, co, cu, ci = (E[k] for k in IDS)
    P = [
        ("trueno", g.t_visto - 0.2, .5), ("zumbido", g.t_del, .4), ("copa", g.t_caer - 0.3, .8), ("susurro", g.t_nadie - 0.2, .6),
        ("subida", g.t_purp - 3.0, .5), ("impacto", g.t_purp, .9), ("impacto2", g.t_env, .8),
        ("impacto2", vi.t_yof, .6), ("impacto", vi.t_medio, .7),
        ("impacto2", ba.t_partio + 0.1, .9), ("palomas", ba.t_palomas - 0.3, .7), ("susurro", ba.t_obl, .4),
        ("tos", mu.t_tosio - 0.1, .7), ("latido", mu.t_tragar, .8), ("subida", mu.t_manos - 3.0, .6), ("impacto", mu.t_manos - 0.3, 1.0),
        ("zumbido", mu.t_cara, .6), ("grito", mu.t_madre - 0.3, .6), ("impacto", mu.t_tirion, .9),
        ("impacto2", ac.t_sosp, .7), ("susurro", ac.t_puso - 0.6, .6), ("impacto", ac.t_puso, .8),
        ("zumbido", ve.t_estr, .5), ("impacto2", ve.t_crist, .6), ("latido", ve.t_garg, .6), ("impacto2", ve.t_todos - 0.2, .7),
        ("susurro", co.t_anciana - 0.3, .6), ("subida", co.t_faltaba - 2.6, .6), ("impacto", co.t_piedra - 0.1, 1.0),
        ("impacto2", cu.t_olena, .7), ("impacto", cu.t_monstruo, .8), ("impacto2", cu.t_menique, .6), ("trueno", cu.t_caos, .5),
        ("ballesta", cu.t_saeta - 0.2, .9), ("impacto", cu.t_saeta + 0.05, .9),
        ("zumbido", ci.t_copa, .5), ("impacto", ci.t_ella, .8), ("susurro", ci.t_mano - 0.2, .6),
        ("campanas", ci.t_caso - 0.6, .5), ("impacto", ci.t_caso, 1.0),
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
