# -*- coding: utf-8 -*-
"""Hoja de CADA mapa de efectos.py (MP.hoja, marcas repartidas) -> previews/mapa_NN.jpg y un mosaico previews/mapas_todos.jpg
con el último cuadro de cada uno (ruta completa)."""
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)
import efectos as E  # noqa: E402

mapas = [d for d in E.FX if str(d.get("nombre", "")).startswith("mapa")]
finales = []
for k, d in enumerate(mapas):
    n = len(d["marcas"])
    dur = 8.0
    marcas = [0.3 + i * (dur - 2.5) / max(1, n - 1) for i in range(n)] if n > 1 else [0.6]
    im = d["fn"](dur - .2, dur, marcas)
    im = Image.fromarray(im[..., [2, 1, 0, 3]] if im.shape[2] == 4 else im[..., ::-1])
    lien = Image.new("RGB", (1920, 1080), (60, 60, 60))
    lien.paste(im.convert("RGB"), ((1920 - im.width) // 2, (1080 - im.height) // 2), im if im.mode == "RGBA" else None)
    ImageDraw.Draw(lien).text((20, 20), f"{k + 1} {d['de']}", fill=(255, 255, 0))
    finales.append(lien.resize((640, 360)))
cols = 3
filas = (len(finales) + cols - 1) // cols
hoja = Image.new("RGB", (cols * 640, filas * 360))
for i, c in enumerate(finales):
    hoja.paste(c, ((i % cols) * 640, (i // cols) * 360))
hoja.save(os.path.join(AQUI, "previews", "mapas_todos.jpg"), quality=85)
print("previews/mapas_todos.jpg", len(finales))
