# -*- coding: utf-8 -*-
"""Miniatura de «La videollamada donde nadie era real» dibujada con el MISMO kit noir del video: el empleado de espaldas ante el
monitor; en la videollamada, todos los recuadros son máscaras (uno todavía se está descomponiendo).
    python videos/videollamada_falsa/_miniatura.py   -> salida/miniatura.jpg (1280x720) + previews/miniatura_movil.png (prueba a 240 px)
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import comun as C
import noir as N
from basen import lienzo
from motor import H, W

T = 7.3
TEXTO = ("NADIE", "ERA REAL")
CAJA = (760.0, 190.0, 1110.0, 640.0)


def dibujo():
    h = lienzo()
    h.nuevo(T, None)
    C.oficina_hk().pegar(h, 1.0, oscuro=0.7)
    C.monitor(h, CAJA, sem=60)
    C.Llamada(sem=40).dibujar(h, T, CAJA, falso=[1.0, 1.0, 0.45, 1.0, 1.0, 1.0], rotulos=False, enc=1.05)
    C.espalda(h, 560, 900, 1.12, sem=80, luz=(0.6, -0.8), gira=0.4, hombros=1.0)
    h.ambiente[:] = 0.26
    h.luz_radial(700, 800, 700, (0.9, 0.9, 0.9), k=1.1)
    h.luz_cono(560, -260, np.pi / 2, 0.34, 1500, (1.5, 1.5, 1.5), k=0.9, suave=0.5)
    N.motas(h, T, n=90, k=0.7)
    img = h.acabado(T, niebla=None, bloom=0.6)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def rotulo(im):
    """Texto grueso de cartel blanco con contorno de tinta y sombra, arriba a la izquierda."""
    pil = Image.fromarray(im)
    f = ImageFont.truetype(N.FUENTE_SELLO, 168)
    capa = Image.new("L", pil.size, 0)
    d = ImageDraw.Draw(capa)
    for s, yy in zip(TEXTO, (30, 200)):
        d.text((60, yy), s, font=f, fill=255)
    borde = capa.filter(ImageFilter.MaxFilter(23))
    sombra = borde.filter(ImageFilter.GaussianBlur(14))
    base = np.asarray(pil).astype(np.float32)
    a_s = np.asarray(sombra, np.float32)[..., None] / 255
    a_b = np.asarray(borde, np.float32)[..., None] / 255
    a_t = np.asarray(capa, np.float32)[..., None] / 255
    base = base * (1 - 0.85 * np.roll(a_s, (18, 14), (0, 1)))
    base = base * (1 - a_b) + 8 * a_b
    rng = np.random.default_rng(4)
    grano = cv2.GaussianBlur(rng.normal(0, 1, base.shape[:2]).astype(np.float32), (0, 0), 1.2)[..., None]
    base = base * (1 - a_t) + np.clip(246 + 9 * grano, 0, 255) * a_t
    return np.clip(base, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    im = rotulo(dibujo())
    os.makedirs("salida", exist_ok=True)
    out = cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA)
    cv2.imwrite("salida/miniatura.jpg", cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    mov = cv2.resize(im, (240, 135), interpolation=cv2.INTER_AREA)
    cv2.imwrite("previews/miniatura_movil.png", cv2.cvtColor(mov, cv2.COLOR_RGB2BGR))
    print("salida/miniatura.jpg", os.path.getsize("salida/miniatura.jpg") // 1024, "KB")
