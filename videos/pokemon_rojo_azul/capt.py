# -*- coding: utf-8 -*-
"""Cuadros sueltos de un video de YouTube sin bajarlo (URL firmada + ffmpeg, con reintento por el 403 del primer pedido).
    python capt.py <salida.jpg> <ancho_celda> <id>@<seg> [<id>@<seg> ...]     -> hoja con el id y el segundo impresos
Copiado de la idea de videos/spyro2/capturas.py (3-nov-2026).
"""
import os
import subprocess
import sys
import tempfile
import time

from PIL import Image, ImageDraw

_URL = {}


def url(vid, alto=480):
    if vid not in _URL:
        r = subprocess.run(["yt-dlp", "-g", "-f", f"bv*[height<={alto}]", "https://youtu.be/" + vid, "--no-warnings"],
                           capture_output=True, text=True)
        _URL[vid] = r.stdout.strip().split("\n")[0]
    return _URL[vid]


def cuadro(vid, s, ruta, alto=480):
    for _ in range(5):
        time.sleep(1.5)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "quiet", "-ss", str(s), "-i", url(vid, alto), "-frames:v", "1", "-q:v", "3", ruta],
                       timeout=120)
        if os.path.exists(ruta) and os.path.getsize(ruta) > 0:
            return True
    return False


if __name__ == "__main__":
    salida, ancho = sys.argv[1], int(sys.argv[2])
    pares = [a.rsplit("@", 1) for a in sys.argv[3:]]
    alto = ancho * 9 // 16
    cols = min(4, len(pares))
    hoja = Image.new("RGB", (cols * ancho, ((len(pares) + cols - 1) // cols) * alto), "black")
    tmp = tempfile.mkdtemp()
    for i, (vid, s) in enumerate(pares):
        r = os.path.join(tmp, f"{i}.jpg")
        if cuadro(vid, s, r):
            im = Image.open(r).convert("RGB")
            im.thumbnail((ancho, alto))
            c = Image.new("RGB", (ancho, alto), "black")
            c.paste(im, ((ancho - im.width) // 2, (alto - im.height) // 2))
            ImageDraw.Draw(c).text((4, 4), f"{vid}@{s}", fill=(255, 255, 0))
            hoja.paste(c, ((i % cols) * ancho, (i // cols) * alto))
        print(vid, s, os.path.exists(r), flush=True)
    hoja.save(salida, quality=80)
