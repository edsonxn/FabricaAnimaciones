# -*- coding: utf-8 -*-
"""Control de la regla «nunca cámara rápida» (docs/estilo_analisis_tactico.md): lista cada FX `video` con vel > 1,05, los saltos del VOD
(--cortes) y lo que se pasa del final de su fuente. Los REBOBINANDO (vel < 0) y las mesas 3D no cuentan.
python videos/lol_final_previa/investigacion/velocidades.py [--cortes]"""
import json
import os
import subprocess
import sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.dirname(os.path.dirname(D))
sys.path[:0] = [D, os.path.join(R, "nucleo")]          # D primero: nucleo también tiene un efectos.py
os.chdir(D)
import efectos as E  # noqa: E402

tl = json.load(open("timeline.json", encoding="utf-8"))


def esc(t):
    return next((e["id"] for e in tl["escenas"] if e["t0"] <= t < e["t1"]), "?")


def duracion(r, _c={}):
    if r not in _c:
        _c[r] = float(subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", r],
                                     capture_output=True, text=True).stdout or 0)
    return _c[r]


malos = 0
vs = sorted((f for f in E.FX if f.get("tipo") == "video"), key=lambda f: f["de"])
prev = None
for f in vs:
    v, dur = f.get("vel", 1.0), f["a"] - f["de"]
    nom, fin = os.path.basename(f["ruta"])[:-4], f["desde"] + v * dur
    if v > 1.05:
        malos += 1
        print(f"RÁPIDO {esc(f['de']):12s} {f['de']:7.2f}-{f['a']:7.2f} x{v:5.2f}  {nom} {f['desde']:7.2f}→{fin:7.2f}")
    if fin > duracion(f["ruta"]) + .05:
        print(f"SE PASA {esc(f['de']):12s} {f['de']:7.2f} {nom}: pide hasta {fin:.1f}, dura {duracion(f['ruta']):.1f}")
    if "--cortes" in sys.argv and prev and prev["ruta"] == f["ruta"] and v >= 0 and prev.get("vel", 1) >= 0:
        salto = f["desde"] - (prev["desde"] + prev.get("vel", 1.0) * (prev["a"] - prev["de"]))
        if abs(salto) > .25:
            print(f"corte  {esc(f['de']):12s} {f['de']:7.2f}  {nom} salta {salto:+6.1f} s → {f['desde']:.1f}")
    prev = f
print(f"\ntotal {tl['total']:.1f} s · {len(vs)} FX video · {malos} con vel > 1,05 · {sum(x[4] - x[3] for x in E.AUD_VIVOS):.0f} s de narración original")
sys.exit(1 if malos else 0)
