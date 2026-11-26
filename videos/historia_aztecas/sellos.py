# -*- coding: utf-8 -*-
"""Sellos de época con EMBLEMAS dibujados para «La historia de México en 5 minutos»:
maiz (domesticación), olmeca (cabeza colosal), piramide_mx (Clásico: Teotihuacán y mayas), aguila_nopal (Tenochtitlan),
espadas (Conquista), columnas (Virreinato de la Nueva España), campana (Independencia 1810), gorro (República 1824),
balanza (Reforma y Juárez), locomotora (Porfiriato), sombrero_rev (Revolución 1910), libro (Constitución 1917),
torre_petroleo (Expropiación 1938), aguila (México moderno)."""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw


def _P(n, pts):
    c = n / 2
    k = n * 0.36
    return [(c + x * k, c + y * k) for x, y in pts]


def _elipse(d, n, cx, cy, rx, ry, fill):
    c = n / 2
    k = n * 0.36
    d.ellipse((c + (cx - rx) * k, c + (cy - ry) * k, c + (cx + rx) * k, c + (cy + ry) * k), fill=fill)


def _dibujar_mx(d, n, nombre):
    F = 0
    w3 = max(3, n // 30)
    if nombre == "maiz":
        _elipse(d, n, 0.0, -0.1, 0.32, 0.68, F)
        for rx in (-0.14, 0.0, 0.14):
            d.line(_P(n, [(rx, -0.62), (rx, 0.42)]), fill=255, width=max(1, n // 65))
        for ry in np.linspace(-0.5, 0.35, 6):
            d.line(_P(n, [(-0.26, ry), (0.26, ry)]), fill=255, width=max(1, n // 65))
        d.polygon(_P(n, [(-0.08, 0.55), (-0.48, 0.05), (-0.72, -0.35), (-0.36, 0.45), (0.0, 0.85)]), fill=F)
        d.polygon(_P(n, [(0.08, 0.55), (0.48, 0.05), (0.72, -0.35), (0.36, 0.45), (0.0, 0.85)]), fill=F)
    elif nombre == "olmeca":
        _elipse(d, n, 0.0, 0.05, 0.72, 0.78, F)
        d.polygon(_P(n, [(-0.76, -0.18), (-0.68, -0.72), (0.68, -0.72), (0.76, -0.18)]), fill=F)
        d.line(_P(n, [(-0.74, -0.22), (0.74, -0.22)]), fill=255, width=w3)
        for sx in (-1, 1):
            _elipse(d, n, sx * 0.28, -0.02, 0.16, 0.09, 255)
        d.polygon(_P(n, [(-0.22, 0.22), (0.0, 0.02), (0.22, 0.22)]), fill=255)
        d.rounded_rectangle([*_P(n, [(-0.34, 0.34)])[0], *_P(n, [(0.34, 0.54)])[0]], radius=max(2, n // 40), fill=255)
    elif nombre == "piramide_mx":
        for k, (w, y0, y1) in enumerate(((0.88, 0.48, 0.84), (0.66, 0.14, 0.48), (0.44, -0.18, 0.14))):
            d.rectangle([*_P(n, [(-w, y0)])[0], *_P(n, [(w, y1)])[0]], fill=F)
        d.rectangle([*_P(n, [(-0.24, -0.52)])[0], *_P(n, [(0.24, -0.18)])[0]], fill=F)
        d.polygon(_P(n, [(-0.18, 0.84), (-0.12, -0.18), (0.12, -0.18), (0.18, 0.84)]), fill=255)
        for y in np.linspace(-0.1, 0.76, 6):
            d.line(_P(n, [(-0.13, y), (0.13, y)]), fill=F, width=max(1, n // 70))
        _elipse(d, n, 0.58, -0.62, 0.16, 0.16, F)
    elif nombre == "aguila_nopal":
        d.polygon(_P(n, [(-0.85, -0.45), (-0.35, -0.22), (0.0, -0.68), (0.35, -0.22), (0.85, -0.45),
                         (0.55, 0.05), (0.18, 0.18), (-0.18, 0.18), (-0.55, 0.05)]), fill=F)
        _elipse(d, n, 0.0, 0.55, 0.18, 0.28, F)
        _elipse(d, n, -0.34, 0.42, 0.16, 0.22, F)
        _elipse(d, n, 0.34, 0.42, 0.16, 0.22, F)
        d.line(_P(n, [(0.15, -0.55), (0.48, -0.72), (0.62, -0.52), (0.78, -0.65)]), fill=F, width=w3)
    elif nombre == "campana":
        d.polygon(_P(n, [(-0.28, -0.62), (0.28, -0.62), (0.52, 0.25), (0.72, 0.52), (-0.72, 0.52), (-0.52, 0.25)]), fill=F)
        d.rectangle([*_P(n, [(-0.22, -0.84)])[0], *_P(n, [(0.22, -0.62)])[0]], fill=F)
        _elipse(d, n, 0.0, 0.66, 0.14, 0.14, F)
        d.line(_P(n, [(-0.46, 0.34), (0.46, 0.34)]), fill=255, width=max(2, n // 50))
    elif nombre == "balanza":
        d.rectangle([*_P(n, [(-0.06, -0.72)])[0], *_P(n, [(0.06, 0.76)])[0]], fill=F)
        d.rectangle([*_P(n, [(-0.42, 0.68)])[0], *_P(n, [(0.42, 0.84)])[0]], fill=F)
        d.line(_P(n, [(-0.68, -0.38), (0.68, -0.38)]), fill=F, width=w3)
        for sx in (-1, 1):
            cx = sx * 0.58
            d.line(_P(n, [(cx, -0.38), (cx - 0.18, 0.12)]), fill=F, width=max(2, n // 50))
            d.line(_P(n, [(cx, -0.38), (cx + 0.18, 0.12)]), fill=F, width=max(2, n // 50))
            d.chord([*_P(n, [(cx - 0.24, 0.02)])[0], *_P(n, [(cx + 0.24, 0.34)])[0]], 0, 180, fill=F)
    elif nombre == "locomotora":
        d.rectangle([*_P(n, [(-0.72, -0.22)])[0], *_P(n, [(0.36, 0.34)])[0]], fill=F)
        d.rectangle([*_P(n, [(-0.76, -0.58)])[0], *_P(n, [(-0.22, -0.22)])[0]], fill=F)
        d.polygon(_P(n, [(0.16, -0.22), (0.10, -0.68), (0.34, -0.68), (0.28, -0.22)]), fill=F)
        d.polygon(_P(n, [(0.36, 0.10), (0.78, 0.48), (0.36, 0.48)]), fill=F)
        for x in (-0.48, -0.06, 0.28):
            _elipse(d, n, x, 0.48, 0.17, 0.17, F)
            _elipse(d, n, x, 0.48, 0.07, 0.07, 255)
    elif nombre == "sombrero_rev":
        d.polygon(_P(n, [(-0.34, -0.10), (-0.18, -0.76), (0.0, -0.84), (0.18, -0.76), (0.34, -0.10)]), fill=F)
        d.chord([*_P(n, [(-0.92, -0.32)])[0], *_P(n, [(0.92, 0.28)])[0]], 0, 180, fill=F)
        d.line(_P(n, [(-0.62, 0.82), (0.62, 0.22)]), fill=F, width=max(4, n // 18))
        d.line(_P(n, [(-0.62, 0.22), (0.62, 0.82)]), fill=F, width=max(4, n // 18))
    elif nombre == "torre_petroleo":
        d.polygon(_P(n, [(-0.46, 0.84), (-0.14, -0.62), (0.14, -0.62), (0.46, 0.84), (0.30, 0.84), (0.0, -0.44), (-0.30, 0.84)]), fill=F)
        for y in (-0.18, 0.18, 0.52):
            w = 0.18 + (y + 0.4) * 0.22
            d.line(_P(n, [(-w, y), (w, y)]), fill=F, width=w3)
        d.polygon(_P(n, [(0.0, -0.92), (-0.24, -0.62), (0.24, -0.62)]), fill=F)
    else:
        return False
    return True


def _dibujar(d, n, nombre):
    F = 0
    if _dibujar_mx(d, n, nombre):
        return
    w3 = max(3, n // 30)
    if nombre == "espadas":
        for lado in (-1, 1):
            pts = [(lado * -0.7, 0.86), (lado * -0.6, 0.94), (lado * 0.1, 0.1), (lado * 0.5, -0.5), (lado * 0.86, -0.9), (lado * 0.62, -0.46),
                   (lado * 0.22, 0.08)]
            d.polygon(_P(n, pts), fill=F)
            d.line(_P(n, [(lado * -0.78, 0.56), (lado * -0.36, 0.84)]), fill=F, width=max(4, n // 20))
    elif nombre == "columnas":
        for cx in (-0.48, 0.48):
            d.rectangle([*_P(n, [(cx - 0.14, -0.62)])[0], *_P(n, [(cx + 0.14, 0.72)])[0]], fill=F)
            d.rectangle([*_P(n, [(cx - 0.26, -0.82)])[0], *_P(n, [(cx + 0.26, -0.64)])[0]], fill=F)
            d.rectangle([*_P(n, [(cx - 0.26, 0.72)])[0], *_P(n, [(cx + 0.26, 0.92)])[0]], fill=F)
        pts = [(-0.95, -0.1), (-0.5, 0.15), (0.0, -0.05), (0.5, 0.15), (0.95, -0.1), (0.95, 0.12), (0.5, 0.37), (0.0, 0.17), (-0.5, 0.37), (-0.95, 0.12)]
        d.polygon(_P(n, pts), fill=F)
    elif nombre == "libro":
        d.polygon(_P(n, [(-0.92, -0.55), (-0.05, -0.42), (-0.05, 0.75), (-0.92, 0.6)]), fill=F)
        d.polygon(_P(n, [(0.92, -0.55), (0.05, -0.42), (0.05, 0.75), (0.92, 0.6)]), fill=F)
        for k in range(5):
            y = -0.30 + 0.18 * k
            d.line(_P(n, [(-0.80, y), (-0.18, y + 0.08)]), fill=255, width=max(1, n // 60))
            d.line(_P(n, [(0.80, y), (0.18, y + 0.08)]), fill=255, width=max(1, n // 60))
        d.text((n * 0.5, n * 0.5 - n * 0.30), "1917", fill=F, anchor="mm", font=_fuente(int(n * 0.14)))
    elif nombre == "gorro":
        pts = [(-0.66, 0.50), (-0.72, 0.05), (-0.58, -0.42), (-0.25, -0.74), (0.18, -0.84), (0.55, -0.72), (0.80, -0.42), (0.86, -0.08),
               (0.70, 0.02), (0.62, -0.28), (0.42, -0.42), (0.36, -0.10), (0.56, 0.50)]
        d.polygon(_P(n, pts), fill=F)
        d.rounded_rectangle([*_P(n, [(-0.78, 0.44)])[0], *_P(n, [(0.66, 0.74)])[0]], radius=max(2, n // 40), fill=F)
        _elipse(d, n, -0.34, 0.59, 0.11, 0.11, 255)
        _elipse(d, n, -0.34, 0.59, 0.05, 0.05, F)
    elif nombre == "aguila":
        d.polygon(_P(n, [(-0.95, -0.5), (-0.7, -0.25), (-0.36, -0.2), (-0.24, 0.1), (-0.28, 0.5), (0.0, 0.86), (0.28, 0.5), (0.24, 0.1), (0.36, -0.2),
                         (0.7, -0.25), (0.95, -0.5), (0.62, -0.5), (0.34, -0.42), (0.18, -0.48), (0.12, -0.74), (0.0, -0.86), (-0.12, -0.74),
                         (-0.18, -0.48), (-0.34, -0.42), (-0.62, -0.5)]), fill=F)
        d.rectangle([*_P(n, [(-0.16, -0.16)])[0], *_P(n, [(0.16, 0.36)])[0]], fill=255)
        d.rectangle([*_P(n, [(-0.16, 0.0)])[0], *_P(n, [(0.16, 0.18)])[0]], fill=F)
        _elipse(d, n, 0.04, -0.72, 0.04, 0.04, 255)
    elif nombre == "corona":
        d.polygon(_P(n, [(-0.72, -0.28), (0.72, -0.28), (0.66, 0.14), (-0.66, 0.14)]), fill=F)
        for x in (-0.6, -0.2, 0.2, 0.6):
            d.polygon(_P(n, [(x - 0.12, -0.28), (x, -0.62), (x + 0.12, -0.28)]), fill=F)
        d.line(_P(n, [(0.0, 0.14), (0.0, 0.92)]), fill=F, width=w3)


@lru_cache(maxsize=8)
def _fuente(px):
    from PIL import ImageFont
    return ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", max(8, px))


@lru_cache(maxsize=96)
def mascara(nombre, px=150, rot=0.0):
    n = int(px * 1.25)
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, n - 4, n - 4), radius=int(px * 0.14), fill=255)
    d.rounded_rectangle((int(px * 0.08), int(px * 0.08), n - int(px * 0.08), n - int(px * 0.08)), radius=int(px * 0.09), outline=0,
                        width=max(2, int(px * 0.026)))
    _dibujar(d, n, nombre)
    a = np.asarray(im, np.uint8)
    if rot:
        Mr = cv2.getRotationMatrix2D((n / 2, n / 2), math.degrees(rot), 1.0)
        a = cv2.warpAffine(a, Mr, (n, n), flags=cv2.INTER_LINEAR)
    return a


def estampar(h, nombre, x, y, px, rot=0.0, color=(198, 52, 52), desgaste=0.0, semilla=0, peg=True):
    m = mascara(nombre, int(px), round(rot, 2))
    x0, y0 = x - m.shape[1] / 2, y - m.shape[0] / 2
    if peg:
        h.peg_mascara(cv2.dilate(m, np.ones((3, 3), np.uint8)), x0, y0)
    h.sello(m, x0, y0, color, 240, desgaste, semilla)


NOMBRES = ("maiz", "olmeca", "piramide_mx", "aguila_nopal", "espadas", "columnas", "campana", "gorro", "balanza",
           "locomotora", "sombrero_rev", "libro", "torre_petroleo", "aguila")

if __name__ == "__main__":
    tiles = [mascara(n, 170) for n in NOMBRES]
    hoja = np.hstack([np.pad(255 - t, 8, constant_values=255) for t in tiles])
    cv2.imwrite("previews/sellos.png", hoja)
