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

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "impacto": ("Deep dark cinematic bass impact hit with a long low reverberant tail, film noir thriller trailer", 3.0),
    "impacto2": ("Short dry low orchestral hit, timpani and low piano cluster, noir suspense sting", 2.0),
    "subida": ("Tense dark cinematic riser, strings and reversed cymbal building up and cutting off abruptly", 3.0),
    "glitch": ("Digital video signal glitch, data corruption stutter and static burst, short", 1.2),
    "trueno": ("Close heavy thunder crack with long rolling rumble in the rain", 5.0),
    "latido": ("Slow tense human heartbeat, low and close, four beats, suspense", 4.0),
    "zumbido": ("Low ominous dark drone swell, uneasy, sub bass and distant metallic resonance, noir mystery", 5.0),
    "reloj": ("Fast frantic clock ticking accelerating, tense", 4.0),
    "susurro": ("Eerie breathy ghostly whisper whoosh passing by, unintelligible, haunting", 2.5),
    "dinero": ("Rapid counting of paper banknotes by a money counting machine, fast flutter", 3.0),
    "mazo": ("Single heavy wooden judge gavel strike on a desk in a large quiet room, reverberant", 2.0),
    "apagon": ("Large building power shutting down, electrical hum winding down to silence, deep and ominous", 4.0),
}


def pistas():
    g, cl, pf, rn, pr, es, ex, ag, ro, ej, af, me, fi, vo, ca, fr, du, ma, pl, ci = (E[k] for k in IDS)
    # pocos golpes y variados: cada tipo de sonido marca UN tipo de momento (nada de un mismo sonido por cada pieza)
    P = [
        ("trueno", g.t_visto - 0.3, .5), ("impacto2", g.t_dos, .7), ("zumbido", g.t_trab, .5), ("impacto", g.t_renun, .9),
        ("subida", g.t_2027 - 2.8, .7), ("impacto", g.t_2027, 1.0), ("susurro", g.t_mentir - 0.4, .7), ("latido", g.t_nosotros, .7),
        ("impacto2", cl.t_filo, .6), ("impacto", cl.t_acert, .8),
        ("reloj", pf.t_faltaba, .4), ("impacto2", pf.t_cerr + 0.7, .7), ("impacto", pf.t_hoy + 0.6, .8),
        ("zumbido", rn.t_maq - 0.3, .7), ("susurro", rn.t_puerta, .6),
        ("impacto2", pr.t_nunca, .8), ("impacto", pr.t_vida, .9), ("dinero", pr.t_perder, .6), ("latido", pr.t_familia, .7),
        ("subida", pr.t_firmo - 3.2, .7), ("impacto", pr.t_firmo - 0.35, 1.0),
        ("impacto2", es.t_escan, .7), ("mazo", es.t_retir + 0.5, .8), ("subida", es.t_70 - 2.9, .7), ("impacto", es.t_70, 1.0),
        ("impacto", ex.t_titulo + 0.5, .9), ("trueno", ex.t_centro - 0.2, .6), ("glitch", ex.t_tu + 0.3, .6),
        ("zumbido", ag.t_esa, .6), ("subida", ag.t_corta - 3.2, .6),
        ("trueno", ro.t_feb + 0.1, .7), ("latido", ro.t_copia, .7), ("glitch", ro.t_dos + 0.5, .7), ("impacto", ro.t_china - 0.3, 1.0),
        ("impacto2", ro.t_pierde, .8),
        ("apagon", ej.t_enc - 0.1, .5), ("impacto2", ej.t_noes + 0.2, .8), ("subida", ej.t_copias - 3.3, .8), ("impacto", ej.t_copias - 0.5, 1.0),
        ("zumbido", ej.t_humanos, .6), ("impacto2", ej.t_caber + 0.7, .8),
        ("trueno", af.t_prot + 0.2, .6), ("zumbido", af.t_nadie, .7), ("susurro", af.t_puerta - 0.3, .7),
        ("impacto2", me.t_llega + 0.5, .8), ("latido", me.t_encu - 0.6, .8), ("subida", me.t_miente - 3.1, .8), ("impacto", me.t_miente - 0.1, 1.0),
        ("susurro", me.t_propios, .7), ("glitch", me.t_parec - 0.4, .7), ("impacto", me.t_deten + 0.3, .9),
        ("susurro", fi.t_filtra - 0.3, .6), ("impacto", fi.t_control - 0.5, 1.0), ("zumbido", fi.t_decision, .7), ("reloj", fi.t_china + 0.4, .6),
        ("latido", vo.t_diez, .8), ("zumbido", vo.t_sicorr, .7), ("subida", vo.t_seis - 3.1, .8), ("mazo", vo.t_seis - 0.1, .9),
        ("impacto", vo.t_cuatro - 0.1, 1.0), ("impacto2", vo.t_parte - 0.1, .7),
        ("impacto2", ca.t_primer, .8), ("zumbido", ca.t_nose, .7), ("impacto", ca.t_millon - 0.6, .8), ("susurro", ca.t_ycuando, .7),
        ("subida", ca.t_deja - 3.0, .8), ("apagon", ca.t_deja - 0.2, .9), ("latido", ca.t_elexp + 0.5, .6),
        ("impacto2", fr.t_segundo, .7), ("apagon", fr.t_apagan + 0.1, .7), ("zumbido", fr.t_pero - 0.3, .7), ("impacto", fr.t_poder - 0.6, .9),
        ("susurro", fr.t_cadaver - 0.9, .8), ("impacto", fr.t_cadaver - 0.2, 1.0),
        ("trueno", du.t0 + 0.5, .4), ("impacto2", du.t_noapoya - 0.2, .7), ("impacto2", du.t_2030, .8),
        ("impacto2", ma.t_tres, .8), ("zumbido", ma.t_noes, .5), ("impacto", ma.t_2029 - 0.2, .9),
        ("impacto2", pl.t_yque + 0.2, .6), ("mazo", pl.t_acuerdo, .6), ("impacto", pl.t_2040, .9), ("reloj", pl.t_pide, .5),
        ("zumbido", ci.t0 + 0.2, .5), ("latido", ci.t_ensu, .7), ("impacto2", ci.t_diez, .8), ("susurro", ci.t_quien - 0.3, .7),
        ("subida", ci.t_caso - 2.6, .6), ("impacto", ci.t_caso + 0.15, 1.0), ("trueno", ci.t_caso + 0.5, .8),
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
