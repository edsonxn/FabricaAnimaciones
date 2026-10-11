# -*- coding: utf-8 -*-
"""Miniatura de «El informante que le puso fecha al final» dibujada con el MISMO kit noir del video: la máquina con su careta
sonriente y, en la pared, la sombra que abre los ojos; el año en grande.
    python videos/informante_2027/_miniatura.py   -> salida/miniatura.jpg (1280x720) + previews/miniatura_movil.png (prueba a 240 px)
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
TEXTO = ("2027", "LO AVISÓ")


def dibujo():
    import kit27 as K
    import props as PR
    from esc_mentira import mascara
    from toon import elipse_, suave
    h = lienzo()
    h.nuevo(T, None)
    h.camara(1.0, 960, 540, 0.0)
    K.pared(h, 150, 80, paneles=7)
    K.plano_(h, C.rect(-300, 940, W + 600, 400), 60, 8, grad=(16, 940, 1200))
    sx, sy, ss = 1540, 1000, 1.5
    S = suave([(-170, 0), (-190, -360), (-150, -470), (-70, -520), (-60, -590), (0, -640), (60, -590), (70, -520), (150, -470),
               (190, -360), (170, 0)], 4)
    K.plano_(h, np.asarray(S) * (ss, ss) + (sx, sy), 8, 20, alfa=0.9)
    for q in (-1, 1):
        e = np.asarray(elipse_(sx + q * 34 * ss, sy - 566 * ss, 22 * ss, 10 * ss, n=14))
        K.plano_(h, e, 245, 22 + q)
        h.emitir(e, 1.0)
    PR.caja_negra(h, 1080, 1000, 1.45, 1.0, T, sem=40, cable=False)
    mascara(h, 1080, 520, 1.3, sem=70, ang=0.05, sonrisa=1.0)
    h.ambiente[:] = 0.3
    h.luz_cono(380, 760, -0.12, 0.62, 2600, (1.6, 1.6, 1.6), k=1.1, suave=0.6)
    N.motas(h, T, n=90, k=0.7)
    img = h.acabado(T, niebla=None, bloom=0.55)
    return (np.clip(img, 0, 255 / 255) * 255).astype(np.uint8)


def rotulo(im):
    """Texto grueso de cartel blanco con contorno de tinta y sombra, arriba a la izquierda."""
    pil = Image.fromarray(im)
    f = ImageFont.truetype(N.FUENTE_SELLO, 168)
    f2 = ImageFont.truetype(N.FUENTE_SELLO, 300)
    capa = Image.new("L", pil.size, 0)
    d = ImageDraw.Draw(capa)
    d.text((50, 20), TEXTO[0], font=f2, fill=255)
    d.text((60, 330), TEXTO[1], font=f, fill=255)
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
