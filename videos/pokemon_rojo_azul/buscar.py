# -*- coding: utf-8 -*-
"""Búsquedas en lote en YouTube (solo títulos): python buscar.py "consulta 1" "consulta 2" ...  (n=6 por consulta)"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def una(q):
    r = subprocess.run(["yt-dlp", "--flat-playlist", "--no-warnings", "--print",
                        "%(id)s | %(duration_string)s | %(channel)s | %(title)s", f"ytsearch6:{q}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return f"## {q}\n" + r.stdout


if __name__ == "__main__":
    with ThreadPoolExecutor(6) as ex:
        for s in ex.map(una, sys.argv[1:]):
            print(s, flush=True)
