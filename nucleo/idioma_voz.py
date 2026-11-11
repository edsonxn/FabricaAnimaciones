# -*- coding: utf-8 -*-
"""REGLA (el usuario, 10-nov-2026): la voz NUNCA habla en otro idioma. Applio (Edge TTS RemyMultilingual + RVC) a veces lee una
oración entera en inglés/francés/italiano/portugués porque una palabra extranjera («Terminator», «Kyle») le hace creer que la frase
es de otro idioma. `seleccionar` mide el idioma de la TOMA ENTERA (p >= 0,90): una oración corta en otro idioma se esconde dentro
de una toma larga, y `IDIOMA_LIBRE` dejaba pasar tomas malas. Este chequeo mide CADA ORACIÓN (segmento de Whisper) de cada toma
elegida (`voz/final/*.wav`) y sale con código 3 si alguna no es español.

    python nucleo/idioma_voz.py <video> [--umbral 0.80] [--solo intro_4,s05_0]
Escribe voz/idioma.json. Arreglo: reescribir la frase (FONETICA en español para el nombre extranjero: «Terminátor», «Cáil»;
oraciones más largas, nunca de 1-3 palabras) y regenerar SOLO esa frase. Nunca `IDIOMA_LIBRE` sin oírla.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--umbral", type=float, default=0.80)
    ap.add_argument("--solo", default="")
    ap.add_argument("--idioma", default="es")
    a = ap.parse_args()
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", a.video)
    os.chdir(base)
    from faster_whisper import WhisperModel
    import librosa
    wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
    solo = {s for s in a.solo.split(",") if s}
    res, malas = {}, []
    for p in sorted(glob.glob("voz/final/*.wav")):
        key = os.path.basename(p)[:-4]
        if solo and key not in solo:
            continue
        y, sr = librosa.load(p, sr=16000)
        segs, _ = wm.transcribe(y, language=a.idioma, beam_size=1, vad_filter=True)
        partes = []
        for s in segs:
            t0, t1 = max(0, s.start - .05), s.end + .05
            if t1 - t0 < 0.9:
                continue
            trozo = y[int(t0 * sr):int(t1 * sr)]
            _, info = wm.transcribe(trozo, language=None, beam_size=1)
            probs = dict(info.all_language_probs or [])
            pe = round(probs.get(a.idioma, 0.0), 3)
            otro = max(((k, v) for k, v in probs.items() if k != a.idioma), key=lambda kv: kv[1], default=("?", 0))
            partes.append(dict(t0=round(t0, 2), t1=round(t1, 2), texto=s.text.strip(), p=pe, otro=otro[0], p_otro=round(otro[1], 3)))
            if pe < a.umbral:
                malas.append((key, t0, t1, pe, otro[0], s.text.strip()))
        res[key] = partes
    json.dump(res, open("voz/idioma.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(res)} frases revisadas oración por oración (umbral p({a.idioma}) >= {a.umbral})")
    for key, t0, t1, pe, ot, tx in malas:
        print(f"  X {key} {t0:.1f}-{t1:.1f} s  p({a.idioma})={pe:.2f}  suena a «{ot}»: {tx[:90]}")
    if malas:
        print("Arreglo: FONETICA en español para el nombre extranjero / reescribir la oración, regenerar SOLO esas frases.")
        sys.exit(3)
    print("OK todas las oraciones en", a.idioma)


if __name__ == "__main__":
    main()
