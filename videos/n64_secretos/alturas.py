# -*- coding: utf-8 -*-
"""Altura máxima, fps y duración de una lista de ids de YouTube (solo metadatos).
    python alturas.py ids.txt      (un id por línea; lo que siga tras el id es comentario)"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ids = []
for l in open(sys.argv[1], encoding="utf-8"):
    l = l.strip()
    if l and not l.startswith("#"):
        ids.append(l.split()[0])


def una(i):
    r = subprocess.run(["yt-dlp", "-j", "--no-warnings", f"https://youtu.be/{i}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    try:
        j = json.loads(r.stdout)
    except Exception:
        return i, "ERR " + r.stderr.strip()[-90:]
    v = [f for f in j["formats"] if f.get("vcodec") not in (None, "none")]
    alt = max((f.get("height") or 0) for f in v) if v else 0
    fps = max((f.get("fps") or 0) for f in v) if v else 0
    return i, f"{alt}p{int(fps)} {int(j['duration'])}s {j.get('channel', '')[:18]} | {j.get('title', '')[:55]}"


with ThreadPoolExecutor(6) as ex:
    for i, s in ex.map(una, ids):
        print(i, s)
