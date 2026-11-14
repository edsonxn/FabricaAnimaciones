# -*- coding: utf-8 -*-
"""Clips ilegibles o más cortos que su beat (p. ej. truncados al llenarse el disco): imprime los números a rehacer."""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
malos = []
for b in json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8")):
    p = os.path.join(AQUI, "medios", b["id"] + ".mp4")
    need = b["t1"] - b["t0"]
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                           capture_output=True, text=True, timeout=30)
        dur = float(r.stdout.strip())
    except Exception:
        dur = 0.0
    if dur < need - 0.2:
        malos.append(int(b["id"][6:]))
        print(f"{b['id']}  clip {dur:.1f}s  beat {need:.1f}s")
print(",".join(map(str, malos)))
