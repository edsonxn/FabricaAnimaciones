# -*- coding: utf-8 -*-
"""Busca en YouTube (yt-dlp, sin descargar) una lista de consultas y escribe id / duración / canal / título.
    python buscar.py consultas.txt [n]      (una consulta por línea; n resultados cada una, por defecto 6)
Escribe en stdout. Solo lectura de metadatos."""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
qs = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]


def una(q):
    r = subprocess.run(["yt-dlp", f"ytsearch{n}:{q}", "--flat-playlist", "--no-warnings",
                        "--print", "%(id)s|%(duration)s|%(channel)s|%(title).70s"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return q, r.stdout.strip().splitlines(), r.stderr.strip()[-120:]


with ThreadPoolExecutor(4) as ex:
    for q, lins, err in ex.map(una, qs):
        print("##", q)
        for l in lins:
            i, d, c, t = (l.split("|", 3) + ["", "", ""])[:4]
            try:
                d = int(float(d))
                d = f"{d // 3600}:{d % 3600 // 60:02d}:{d % 60:02d}" if d >= 3600 else f"{d // 60}:{d % 60:02d}"
            except ValueError:
                pass
            print(f"{i} {d:>8} {c[:22]:22} {t}")
        if not lins:
            print("  (nada)", err)
