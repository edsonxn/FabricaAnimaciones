# -*- coding: utf-8 -*-
"""Frases regeneradas DESPUÉS de `tiempo` (12-nov, errores del usuario sobre el MASTER): ajusta cada voz/final/<key>.wav a la duración
de su toma vieja (_dur_viejas.json) con atempo de ffmpeg y escala sus palabras en voz/palabras.json, así el timeline, los beats y
los clips no cambian. Ratio permitido 0,88-1,12 (más = reescribir la frase más corta).   python _ajustar_duracion.py"""
import json
import os
import subprocess

import soundfile as sf

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
d = json.load(open("_dur_viejas.json"))
pal = json.load(open("voz/palabras.json", encoding="utf-8"))
for k, vieja in d.items():
    f = f"voz/final/{k}.wav"
    nueva = sf.info(f).duration
    r = nueva / vieja
    if not 0.88 <= r <= 1.12:
        print(f"!! {k}: {nueva:.2f} s vs {vieja:.2f} s (ratio {r:.3f}) FUERA DE RANGO: reescribir más corta")
        continue
    tmp = f + ".tmp.wav"
    subprocess.run([FF, "-y", "-v", "error", "-i", f, "-filter:a", f"atempo={r:.5f}", "-ar", "48000", tmp], check=True)
    os.replace(tmp, f)
    p = pal.get(k)
    if p:
        esc = vieja / nueva
        for w in p.get("words", []):
            w["s"] = round(w["s"] * esc, 3)
            w["e"] = round(w["e"] * esc, 3)
        p["dur"] = vieja
    print(f"{k}: {nueva:.2f} -> {sf.info(f).duration:.2f} s (ratio {r:.3f})")
json.dump(pal, open("voz/palabras.json", "w", encoding="utf-8"), ensure_ascii=False)
