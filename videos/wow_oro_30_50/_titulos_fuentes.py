# -*- coding: utf-8 -*-
"""Pone título y canal reales en las entradas de fuentes.json que `bajar --url` deja como «(fijado a mano)», para que
`python fab.py <v> fuentes` escriba créditos con nombre (salida/creditos.txt). 26-nov-2026, wow_oro_30_50.
Lee primero `_fuentes_meta.json` (caché); lo que falte lo pide a yt-dlp (solo metadatos, sin bajar)."""
import json
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

fu = json.load(open("fuentes.json", encoding="utf-8"))
meta = json.load(open("_fuentes_meta.json", encoding="utf-8")) if os.path.exists("_fuentes_meta.json") else {}
ids = sorted({r["video"] for k, r in fu.items() if not k.startswith("_") and isinstance(r, dict)} - set(meta))
if ids:
    r = subprocess.run(["yt-dlp", "--skip-download", "--no-warnings", "--print", "%(id)s\t%(channel)s\t%(title)s"]
                       + [f"https://www.youtube.com/watch?v={i}" for i in ids],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV, timeout=900)
    for ln in r.stdout.splitlines():
        p = ln.split("\t")
        if len(p) == 3:
            meta[p[0]] = {"canal": p[1], "titulo": p[2]}
    json.dump(meta, open("_fuentes_meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = 0
for k, r in fu.items():
    if k.startswith("_") or not isinstance(r, dict):
        continue
    m = meta.get(r["video"])
    if m and (not r.get("canal") or r.get("titulo") == "(fijado a mano)"):
        r["canal"], r["titulo"] = m["canal"], m["titulo"]
        n += 1
json.dump(fu, open("fuentes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{n} entradas con título y canal · {len(meta)} videos en _fuentes_meta.json · sin datos: "
      f"{sorted({r['video'] for k, r in fu.items() if not k.startswith('_') and isinstance(r, dict) and r['video'] not in meta}) or '-'}")
