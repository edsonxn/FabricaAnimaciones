# -*- coding: utf-8 -*-
"""Miniatura de «El caso de la máquina» dibujada con el MISMO kit noir del video:
el detective en primer plano (persiana en rayas, cigarro) frente a la caja negra de la IA con su única luz encendida.
    python videos/ia_noir/_miniatura.py            -> salida/miniatura.jpg (1280x720) + previews/miniatura_movil.png (prueba a 240 px)
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mundos as MU
import noir as N
import props as PR
from basen import lienzo
from motor import H, W
from noir_pers import Busto
from toon import elipse_

T = 7.3                                    # instante «congelado» (fase del humo y de la luz de la caja)
TEXTO = ("¿NOS", "DESTRUIRÁ?")
CAJA = (650.0, 1050.0, 1.0)               # x, base, escala


def dibujo():
    h = lienzo()
    h.nuevo(T, None)
    h.camara(1.3, 900, 200, 0.0)
    MU.oficina().pegar(h, 1.0, oscuro=0.75)
    h.camara(1.0, W / 2, H / 2, 0.0)
    x, y, s = CAJA
    PR.mesa(h, x + 60, y - 30, ancho=900, fondo=150, alto=170, tono=50, sem=3)
    led = PR.caja_negra(h, x, y - 70, s=s, led=1.0, t=1.9 / 2.4, sem=11)
    p = dict(x=1470, y=600, s=1.18, d=-1, luz=(-1.0, -0.3), brasa=0.9, arriba=0.35, rot=0.04)
    b = Busto(sem=5)
    b.dibujar(h, p)
    tip = b.punta(p)
    h.emitir(elipse_(tip[0], tip[1], 8, 8, n=10), 1.4)
    N.humo(h, T, tip[0], tip[1], k=0.7, ancho=2.2, viento=(-60, -130))
    h.ambiente[:] = 0.2
    # la «mirada» de la máquina: un ojo que brilla con halo, y un cono de luz cenital que aísla la caja
    for r_, v_ in ((60, 0.10), (44, 0.16), (32, 0.26), (22, 0.5), (15, 2.4)):     # halo por anillos (sin cortes de caja)
        h.emitir(elipse_(led[0], led[1], r_, r_, n=28), v_, blur=4)
    h.luz_radial(led[0], led[1], 420, (1.0, 1.0, 1.0), k=1.1)
    h.luz_cono(x, -150, np.pi / 2, 0.36, 1500, (1.0, 1.0, 1.0), k=1.0)
    h.luz_persiana(np.array([[700, -200], [2200, -60], [2200, 1300], [700, 1260]]), k=1.25, n=18, abierto=0.5, mundo=False)
    N.motas(h, T, n=110, k=0.9)
    img = h.acabado(T, niebla=dict(dens=0.18, vel=12, y0=-400, y1=900, sube=False), bloom=0.7)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def rotulo(im):
    """Texto grueso de cartel (Impact) blanco con contorno de tinta y sombra, arriba a la izquierda."""
    pil = Image.fromarray(im)
    f = ImageFont.truetype(N.FUENTE_SELLO, 175)
    capa = Image.new("L", pil.size, 0)
    d = ImageDraw.Draw(capa)
    ys = (36, 212)
    for s, yy in zip(TEXTO, ys):
        d.text((70, yy), s, font=f, fill=255)
    borde = capa.filter(ImageFilter.MaxFilter(23))
    sombra = borde.filter(ImageFilter.GaussianBlur(14))
    base = np.asarray(pil).astype(np.float32)
    a_s = np.asarray(sombra, np.float32)[..., None] / 255
    a_b = np.asarray(borde, np.float32)[..., None] / 255
    a_t = np.asarray(capa, np.float32)[..., None] / 255
    base = base * (1 - 0.85 * np.roll(a_s, (18, 14), (0, 1)))
    base = base * (1 - a_b) + 8 * a_b
    rng = np.random.default_rng(4)                           # tinta de cartel: blanco con leve grano de papel
    grano = cv2.GaussianBlur(rng.normal(0, 1, base.shape[:2]).astype(np.float32), (0, 0), 1.2)[..., None]
    blanco = np.clip(246 + 9 * grano, 0, 255)
    base = base * (1 - a_t) + blanco * a_t
    return np.clip(base, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    im = rotulo(dibujo())
    os.makedirs("salida", exist_ok=True)
    out = cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA)
    cv2.imwrite("salida/miniatura.jpg", cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    mov = cv2.resize(im, (240, 135), interpolation=cv2.INTER_AREA)
    cv2.imwrite("previews/miniatura_movil.png", cv2.cvtColor(mov, cv2.COLOR_RGB2BGR))
    print("salida/miniatura.jpg", os.path.getsize("salida/miniatura.jpg") // 1024, "KB")
