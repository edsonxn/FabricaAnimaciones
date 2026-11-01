# -*- coding: utf-8 -*-
"""Lyria solo entrega ~3 min por pieza: la música del video largo se genera por PARTES (cortes en cambios de escena, ≤ ~170 s cada una)
y se unen con fundido cruzado.

python _lyria_partes.py plan       muestra las partes
python _lyria_partes.py gen [n]    genera n candidatos por parte (audio/lyria_ly<P>_<k>.mp3: con «lyria» en el nombre entran en la biblioteca), con reintentos
python _lyria_partes.py unir 1 1 2 1   une el candidato indicado de cada parte -> audio/musica.wav
"""
import json
import os
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
sys.path.insert(0, ".")
import lyria  # noqa: E402
import guion  # noqa: E402

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
MAXP = 172.0
XF = 1.6

esc = TL["escenas"]
corte_idx = [0]
for i, e in enumerate(esc):
    t_fin = esc[i + 1]["t0"] if i + 1 < len(esc) else TOTAL
    if t_fin - esc[corte_idx[-1]]["t0"] > MAXP and i > corte_idx[-1]:
        corte_idx.append(i)
corte_idx.append(len(esc))
PARTES = []
for a, b in zip(corte_idx, corte_idx[1:]):
    t0 = esc[a]["t0"]
    t1 = esc[b]["t0"] if b < len(esc) else TOTAL
    es = [dict(e, t0=e["t0"] - t0) for e in esc[a:b]]
    PARTES.append(dict(t0=t0, t1=t1, tl=dict(total=t1 - t0, escenas=es), ids=[e["id"] for e in esc[a:b]]))


def generar(k, n):
    P = PARTES[k]
    cfg = dict(guion.LYRIA)
    if len(PARTES) == 1:
        extra = ""
    elif k == 0:
        extra = f" This is PART 1 of {len(PARTES)} of a longer score: start with a short hook and keep growing; do NOT end with a final chord, end with a continuing phrase."
    elif k == len(PARTES) - 1:
        extra = f" This is the LAST PART ({k + 1} of {len(PARTES)}) of a longer score: continue in the same sound world, rising to a warm final chord with a natural fade-out."
    else:
        extra = f" This is PART {k + 1} of {len(PARTES)} of a longer score: continue in the same sound world without a final chord."
    cfg["estilo"] = cfg["estilo"] + extra
    texto = lyria.prompt(P["tl"], cfg)
    for c in range(1, n + 1):
        for intento in range(4):
            try:
                t = time.time()
                datos, mime, _ = lyria.generar(texto)
                ruta = f"audio/lyria_ly{k + 1}_{c}.mp3"
                open(ruta, "wb").write(datos)
                d = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout.strip()
                print(f"{ruta}: {float(d):.1f} s ({time.time() - t:.0f} s de generación; pedidos {P['tl']['total']:.0f} s)", flush=True)
                break
            except Exception as ex:
                print(f"  parte {k + 1} cand {c} intento {intento + 1}: {ex}", flush=True)
                time.sleep(5)


def unir(cands):
    import soundfile as sf
    out = None
    sr = 48000
    n = len(PARTES)
    for k, (P, c) in enumerate(zip(PARTES, cands)):
        dur = (P["t1"] - P["t0"]) + (XF / 2 if k > 0 else 0) + (XF / 2 if k < n - 1 else 0)
        lyria.a_wav(f"audio/lyria_ly{k + 1}_{c}.mp3", f"audio/_p{k}.wav", dur, fade_in=(XF if k > 0 else 0.6), fade_out=(XF if k < n - 1 else 3.0))
        x, sr = sf.read(f"audio/_p{k}.wav", always_2d=True)
        if out is None:
            out = np.zeros((int(round(TOTAL * sr)), 2), np.float32)
        i0 = int(round((P["t0"] - (XF / 2 if k > 0 else 0)) * sr))
        seg = x[:len(out) - i0]
        out[i0:i0 + len(seg)] += seg
        os.remove(f"audio/_p{k}.wav")
    sf.write("audio/musica.wav", out, sr, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / sr:.2f} s) con {n} partes")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1]
    if a == "plan":
        for k, P in enumerate(PARTES):
            print(k + 1, f"{P['t0']:.1f}-{P['t1']:.1f} ({P['t1'] - P['t0']:.0f} s)", P["ids"])
    elif a == "gen":
        os.makedirs("audio", exist_ok=True)
        for k in range(len(PARTES)):
            generar(k, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    else:
        unir([int(x) for x in sys.argv[2:]])
