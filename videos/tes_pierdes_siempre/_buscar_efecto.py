# -*- coding: utf-8 -*-
"""Hoja de candidatos para un efecto: python buscar_efecto.py "<búsqueda>" <salida.jpg> [n_videos=3] [max_min=15]
Por cada video, una fila de 8 cuadros repartidos (fino.py sobre el video entero a 360p), con el título encima."""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
q, out = sys.argv[1], sys.argv[2]
nv = int(sys.argv[3]) if len(sys.argv) > 3 else 3
mx = float(sys.argv[4]) if len(sys.argv) > 4 else 15
r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", f"ytsearch{nv * 3}:{q}"], capture_output=True, text=True, encoding="utf-8",
                   errors="replace")
ents = [e for e in json.loads(r.stdout).get("entries", []) if e.get("duration") and 20 < e["duration"] < mx * 60][:nv]
filas = []
for e in ents:
    d = e["duration"]
    paso = max(1.0, round((d - 4) / 7.0, 1))
    tmp = out + f".{e['id']}.jpg"
    subprocess.run([sys.executable, os.path.join(AQUI, "_fino.py"), e["id"], "2", str(2 + 7 * paso), str(paso), tmp], capture_output=True)
    filas.append((e, Image.open(tmp) if os.path.exists(tmp) else Image.new("RGB", (1920, 135))))
f = ImageFont.truetype("arial.ttf", 15)
L = Image.new("RGB", (1920, max(1, len(filas)) * (135 + 22)))
dr = ImageDraw.Draw(L)
for i, (e, im) in enumerate(filas):
    y = i * 157
    dr.text((4, y + 2), f"{e['id']} · {e.get('channel') or e.get('uploader')} · {e['title'][:100]} · {int(e['duration'])} s",
            fill=(255, 255, 0), font=f)
    L.paste(im.crop((0, 0, 1920, 135)), (0, y + 22))
L.save(out, quality=78)
print(out, [(e["id"], int(e["duration"])) for e, _ in filas])
