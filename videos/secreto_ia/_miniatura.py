# -*- coding: utf-8 -*-
"""Miniatura de «¿Puede una IA guardar un secreto?» con el MISMO kit noir del video (1920x1080 -> 1280x720): la columna de la IA
con su careta de sonrisa bajo la bombilla, y el rótulo de la pregunta en tinta sólida.
    python _miniatura.py   -> salida/miniatura.jpg (1280x720) + previews/miniatura_movil.png (prueba a 240 px)"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2  # noqa: E402
import numpy as np  # noqa: E402

import comun as C  # noqa: E402
import mundos_secreto as M  # noqa: E402
from basen import lienzo  # noqa: E402
from motor import H, W  # noqa: E402


def main():
    h = lienzo()
    h.nuevo(0.0, None)
    h.camara(1.0, W / 2, H / 2, 0.0)
    M.sala_interrogatorio(h, 0.0, sem=900)
    M.columna_ia(h, 1220, 930, s=1.3, luz=1.0, sem=910)
    M.careta(h, 1220, 470, s=0.9, sem=930)
    C.banda(h, "¿PUEDE UNA IA", 560, 330, 96, 1.0, 0.0, sem=940)
    C.banda(h, "GUARDAR UN SECRETO?", 560, 500, 96, 1.0, 0.0, claro=True, sem=941)
    img = h.acabado(0.0, niebla=None, bloom=0.5)
    im = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    im = cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA)
    os.makedirs("salida", exist_ok=True)
    os.makedirs("previews", exist_ok=True)
    cv2.imwrite("salida/miniatura.jpg", cv2.cvtColor(im, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    peq = cv2.resize(im, (240, 135), interpolation=cv2.INTER_AREA)
    cv2.imwrite("previews/miniatura_movil.png", cv2.cvtColor(peq, cv2.COLOR_RGB2BGR))
    print("ok salida/miniatura.jpg")


if __name__ == "__main__":
    main()
