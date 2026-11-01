# -*- coding: utf-8 -*-
"""Miniatura por código:  python miniaturas.py
Parte de un cuadro propio del video (previews/c_0068.30.jpg, la cara del demonio dentro del monitor),
le sube niveles (el cuadro del video es demasiado oscuro para verse a 320 px) y pone el texto.
Salida: salida/sonic_exe_mini_final.jpg (1280x720)."""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)

W, H = 1280, 720
SRC = "previews/c_0068.30.jpg"
RECORTE = (300, 262, 1620, 1004)   # x0, y0, x1, y1 sobre 1920x1080 (16:9, la cara llena el cuadro)
TEXTO = ("NUNCA", "EXISTIÓ")
FUENTE = "C:/Windows/Fonts/impact.ttf"


def base():
    im = cv2.imread(SRC).astype(np.float32) / 255.0
    x0, y0, x1, y1 = RECORTE
    im = cv2.resize(im[y0:y1, x0:x1], (W, H), interpolation=cv2.INTER_CUBIC)
    im = cv2.GaussianBlur(im, (0, 0), 1.2)                      # quita el grano de la cinta
    im = np.clip((im - 0.03) * 2.35, 0, 1) ** 0.8               # niveles
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.45, 0, 1)
    im = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # los ojos: el rojo que ya está en el cuadro, encendido
    rojo = np.clip(im[..., 2] - np.maximum(im[..., 0], im[..., 1]) * 1.15, 0, 1)
    halo = cv2.GaussianBlur(rojo, (0, 0), 18) * 0.7
    im[..., 2] = np.clip(im[..., 2] + halo + rojo * 0.3, 0, 1)
    im[..., 1] = np.clip(im[..., 1] + halo * 0.12, 0, 1)
    # scanlines y viñeta
    im[1::3] *= 0.86
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.55) / (H / 2)) ** 2)
    im *= np.clip(1.12 - 0.5 * d ** 2.2, 0.15, 1)[..., None]
    # franja oscura arriba para el texto
    im *= np.clip(0.62 + yy / (H * 0.6), 0.62, 1)[..., None]
    return Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8)[..., ::-1])


def texto(img):
    tam = 150
    f = ImageFont.truetype(FUENTE, tam)
    d = ImageDraw.Draw(img)
    esp = 34
    anchos = [d.textlength(p, font=f) for p in TEXTO]
    while sum(anchos) + esp > W - 90:
        tam -= 4
        f = ImageFont.truetype(FUENTE, tam)
        anchos = [d.textlength(p, font=f) for p in TEXTO]
    x = (W - sum(anchos) - esp) / 2
    y = 14
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    for p, a, col in zip(TEXTO, anchos, ((245, 245, 240, 255), (255, 28, 28, 255))):
        # aberración cromática de CRT: dos copias desplazadas debajo
        dc.text((x - 5, y), p, font=f, fill=(0, 230, 255, 150))
        dc.text((x + 5, y), p, font=f, fill=(255, 0, 60, 150))
        dc.text((x, y), p, font=f, fill=col, stroke_width=7, stroke_fill=(0, 0, 0, 255))
        x += a + esp
    sombra = capa.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img.convert("RGBA"), sombra)
    img = Image.alpha_composite(img, capa)
    return img.convert("RGB")


if __name__ == "__main__":
    os.makedirs("salida", exist_ok=True)
    img = texto(base())
    img.save("salida/sonic_exe_mini_final.jpg", quality=93)
    img.resize((320, 180), Image.LANCZOS).save("previews/mini_320.jpg", quality=90)
    print("salida/sonic_exe_mini_final.jpg", img.size)
