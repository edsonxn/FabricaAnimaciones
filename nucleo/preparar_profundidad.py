# -*- coding: utf-8 -*-
"""Calcula mapas de profundidad (Depth Anything V2 Small) de las fotos de `imagenes/` para el parallax 2.5D del estilo documental.
Uso (desde la carpeta del video):  python preparar_profundidad.py foto1 foto2 ...   (nombres sin extensión; sin argumentos = todas
las fotos sueltas y folios listados en DEPTH del guion si existe).  Salida: imagenes/depth/<nombre>.png (0 = lejos, 255 = cerca)."""
import os
import sys

import numpy as np
import torch
from PIL import Image
from transformers import pipeline

D = os.path.join(os.getcwd(), "imagenes")
os.makedirs(os.path.join(D, "depth"), exist_ok=True)


def ruta(n):
    for base in (D, os.path.join(D, "folios")):
        for ext in ("", ".jpg", ".png", ".jpeg"):
            p = os.path.join(base, n + ext)
            if os.path.isfile(p):
                return p
    raise FileNotFoundError(n)


def main(nombres):
    pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=0 if torch.cuda.is_available() else -1)
    for n in nombres:
        salida = os.path.join(D, "depth", n + ".png")
        if os.path.exists(salida):
            continue
        im = Image.open(ruta(n)).convert("RGB")
        im.thumbnail((1400, 1400))
        d = np.asarray(pipe(im)["depth"], np.float32)
        lo, hi = np.percentile(d, 1), np.percentile(d, 99)
        d = np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)
        Image.fromarray((d * 255).astype(np.uint8)).save(salida)
        print("profundidad", n, d.shape)


if __name__ == "__main__":
    main(sys.argv[1:])
