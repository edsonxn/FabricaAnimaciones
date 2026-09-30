# -*- coding: utf-8 -*-
"""Lyria solo entrega ~3 min por pieza: se genera la música del video de 5:00 en dos mitades (corte en un cambio de escena) y se unen con fundido.

python _lyria_partes.py gen        genera 2 candidatos por mitad (audio/lyA_k.mp3, audio/lyB_k.mp3), con reintentos
python _lyria_partes.py unir A B   une los candidatos A y B (1 o 2) -> audio/musica.wav
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
CORTE = "islam"                       # la 2.ª mitad empieza aquí
ids = [e["id"] for e in TL["escenas"]]
k = ids.index(CORTE)
t_corte = TL["escenas"][k]["t0"]
TOTAL = TL["total"]
XF = 1.6                              # fundido cruzado entre mitades (s)


def sub_tl(escenas, t0, t1):
    es = [dict(e, t0=e["t0"] - t0) for e in escenas]
    return dict(total=t1 - t0, escenas=es)


PARTES = {"A": sub_tl(TL["escenas"][:k], 0.0, t_corte), "B": sub_tl(TL["escenas"][k:], t_corte, TOTAL)}


def generar(parte, n):
    cfg = dict(guion.LYRIA)
    est = cfg["estilo"] + (" This is the FIRST HALF of a longer score: start with a short hook and keep growing." if parte == "A"
                           else " This is the SECOND HALF of a longer score: continue in the same sound world, rising to a warm final chord with a natural fade-out.")
    cfg["estilo"] = est
    texto = lyria.prompt(PARTES[parte], cfg)
    for c in range(1, n + 1):
        for intento in range(4):
            try:
                t = time.time()
                datos, mime, _ = lyria.generar(texto)
                ruta = f"audio/ly{parte}_{c}.mp3"
                open(ruta, "wb").write(datos)
                d = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout.strip()
                print(f"{ruta}: {float(d):.1f} s ({time.time() - t:.0f} s de generación; pedidos {PARTES[parte]['total']:.0f} s)", flush=True)
                break
            except Exception as ex:
                print(f"  {parte}{c} intento {intento + 1}: {ex}", flush=True)
                time.sleep(5)


def unir(a, b):
    import soundfile as sf
    durA = t_corte + XF / 2
    durB = (TOTAL - t_corte) + XF / 2
    lyria.a_wav(f"audio/lyA_{a}.mp3", "audio/_A.wav", durA, fade_in=0.6, fade_out=XF)
    lyria.a_wav(f"audio/lyB_{b}.mp3", "audio/_B.wav", durB, fade_in=XF, fade_out=3.0)
    xa, sr = sf.read("audio/_A.wav", always_2d=True)
    xb, _ = sf.read("audio/_B.wav", always_2d=True)
    out = np.zeros((int(round(TOTAL * sr)), 2), np.float32)
    out[:len(xa)] += xa[:len(out)]
    i0 = int(round((t_corte - XF / 2) * sr))
    seg = xb[:len(out) - i0]
    out[i0:i0 + len(seg)] += seg
    sf.write("audio/musica.wav", out, sr, subtype="FLOAT")
    os.remove("audio/_A.wav")
    os.remove("audio/_B.wav")
    print(f"audio/musica.wav listo ({len(out) / sr:.2f} s) = mitad A{a} + mitad B{b}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1] == "gen":
        os.makedirs("audio", exist_ok=True)
        for p in "AB":
            generar(p, 2)
    else:
        unir(int(sys.argv[2]), int(sys.argv[3]))
