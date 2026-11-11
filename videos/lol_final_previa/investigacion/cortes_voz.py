# -*- coding: utf-8 -*-
"""CHEQUEO: ningún silencio de ESPACIOS_VOZ puede caer dentro de una palabra (el usuario, 31-oct-2026: «hay sílabas que se cortan y se
continúan después del clip»). Mide la SEÑAL del original (voz/final_orig), no solo los tiempos de las palabras: cada corte debe estar en
una pausa real de al menos ANCHO_MIN, con margen a los dos lados. Sale con error si alguno falla; render_par.py lo corre antes de renderizar.
python videos/lol_final_previa/investigacion/cortes_voz.py [--whisper]   --whisper: además escucha 1,5 s a cada lado de cada corte."""
import json
import os
import sys

import numpy as np
import soundfile as sf

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D)
from espaciar_voz import ANCHO_MIN, MARGEN, envolvente, indice, norm, pausa  # noqa: E402
from guion import ESPACIOS_VOZ  # noqa: E402

pal = json.load(open(os.path.join(D, "voz", "palabras.json"), encoding="utf-8"))
tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
FR = {f["key"]: f for e in tl["escenas"] for f in e["frases"]}


def cortes():
    """(frase, palabra anterior, palabra siguiente, instante en el original, ancho de la pausa, centro de la pausa elegido)"""
    for key, spec in ESPACIOS_VOZ.items():
        x, sr = sf.read(os.path.join(D, "voz", "final_orig", key + ".wav"), always_2d=True)
        p = pal[key]
        words = p.get("espaciado", p)["words"]
        env, hop, umbral = envolvente(x, sr)
        for palabra, n, seg, *t in spec:
            if palabra in ("$ini", "$fin"):
                continue
            i = indice(words, palabra, n)
            c, ancho = pausa(env, hop, umbral, *(t * 2 or (words[i - 1]["e"], words[i]["s"])))
            yield key, words[i - 1]["w"], words[i]["w"], c, ancho, x, sr, seg


def main():
    malos = n = 0
    for key, ant, sig, c, ancho, x, sr, seg in cortes():
        n += 1
        ok = ancho >= ANCHO_MIN
        malos += not ok
        t = FR[key]["t0"] + c
        print(f"{'ok ' if ok else 'MAL'} {int(t // 60)}:{int(t % 60):02d} {key:12s} «{ant} | {sig}» pausa {ancho * 1000:4.0f} ms (+{seg:.1f} s)")
    print(f"{n} cortes dentro de frases · {malos} sin pausa real de {ANCHO_MIN * 1000:.0f} ms (margen {MARGEN * 1000:.0f} ms)")
    if "--whisper" in sys.argv:
        from faster_whisper import WhisperModel
        m = WhisperModel("large-v3", device="cuda", compute_type="float16")
        tmp = os.path.join(D, "voz", "_corte.wav")

        def oye(y, sr):
            sf.write(tmp, y, sr)
            return [w.word.strip() for s in m.transcribe(tmp, language="es", word_timestamps=True, vad_filter=False)[0] for w in s.words]

        fallos = 0
        for key, ant, sig, c, ancho, x, sr, seg in cortes():
            i = int(c * sr)
            antes, despues = oye(x[max(0, i - int(1.5 * sr)):i], sr), oye(x[i:i + int(1.5 * sr)], sr)
            bien = bool(antes) and bool(despues) and norm(antes[-1]) == norm(ant) and norm(despues[0]) == norm(sig)
            fallos += not bien
            print(f"{'ok ' if bien else 'OJO'} {key:12s} espera «{ant} | {sig}» · oye «{' '.join(antes[-2:])} | {' '.join(despues[:2])}»")
        os.remove(tmp)
        print(f"Whisper: {fallos} cortes a revisar")
    sys.exit(1 if malos else 0)


if __name__ == "__main__":
    main()
