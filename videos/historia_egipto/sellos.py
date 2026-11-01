# -*- coding: utf-8 -*-
"""Sellos de época con EMBLEMAS dibujados (Egipto, 11-oct-2026: corona doble, pirámide, anj, ojo de Horus, Atón, cartucho,
disco alado, faro, minarete, espadas, ancla y águila; heredados de España: (en hueco sobre tinta de color, como un sello de caucho):
laurel (Hispania romana), corona votiva (visigodos, tesoro de Guarrazar), arco de herradura (al-Ándalus), castillo (reinos cristianos),
yugo y flechas (Reyes Católicos), columnas del Plus Ultra (Austrias), flor de lis (Borbones), constitución (Cádiz 1812),
gorro frigio (República), urna (democracia)."""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw


def _P(n, pts):
    """Puntos normalizados (-1..1) -> píxeles de un lienzo n x n."""
    c = n / 2
    k = n * 0.36
    return [(c + x * k, c + y * k) for x, y in pts]


def _elipse(d, n, cx, cy, rx, ry, fill):
    c = n / 2
    k = n * 0.36
    d.ellipse((c + (cx - rx) * k, c + (cy - ry) * k, c + (cx + rx) * k, c + (cy + ry) * k), fill=fill)


def _hoja(cx, cy, ang, L=0.30, A=0.11):
    pts = []
    for s in np.linspace(0, 1, 9):
        w = A * math.sin(math.pi * s)
        pts.append((s * L, -w))
    for s in np.linspace(1, 0, 9):
        w = A * math.sin(math.pi * s)
        pts.append((s * L, w))
    c, sn = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * sn, cy + x * sn + y * c) for x, y in pts]


def _dibujar_eg(d, n, nombre):
    """Emblemas egipcios (en hueco). Devuelve True si dibujó algo."""
    F = 0
    w3 = max(3, n // 30)
    if nombre == "corona_doble":
        d.polygon(_P(n, [(-0.62, 0.8), (-0.66, -0.05), (-0.28, -0.05), (-0.22, 0.1), (0.22, 0.1), (0.3, -0.05), (0.42, -0.05), (0.42, -0.72),
                         (0.62, -0.74), (0.62, 0.8)]), fill=F)
        d.polygon(_P(n, [(-0.22, 0.1), (-0.2, -0.45), (-0.08, -0.8), (0.0, -0.88), (0.08, -0.8), (0.2, -0.45), (0.22, 0.1)]), fill=255)
        d.polygon(_P(n, [(-0.14, 0.04), (-0.12, -0.42), (0.0, -0.74), (0.12, -0.42), (0.14, 0.04)]), fill=F)
        d.line(_P(n, [(-0.28, -0.05), (-0.55, -0.35), (-0.75, -0.48), (-0.68, -0.62)]), fill=F, width=w3)
    elif nombre == "piramide":
        d.polygon(_P(n, [(-0.92, 0.82), (0.0, -0.72), (0.92, 0.82)]), fill=F)
        for k in range(1, 5):
            y = 0.82 - 0.3 * k
            x = 0.92 * (1 - 0.3 * k / 1.54)
            d.line(_P(n, [(-x + 0.05, y), (x - 0.05, y)]), fill=255, width=max(1, n // 70))
        d.line(_P(n, [(0.0, -0.72), (0.0, 0.82)]), fill=255, width=max(1, n // 70))
        _elipse(d, n, 0.62, -0.62, 0.16, 0.16, F)
    elif nombre == "anj":
        _elipse(d, n, 0.0, -0.42, 0.34, 0.44, F)
        _elipse(d, n, 0.0, -0.42, 0.17, 0.27, 255)
        d.rectangle([*_P(n, [(-0.6, -0.04)])[0], *_P(n, [(0.6, 0.14)])[0]], fill=F)
        d.rectangle([*_P(n, [(-0.11, 0.0)])[0], *_P(n, [(0.11, 0.92)])[0]], fill=F)
    elif nombre == "ojo":
        d.polygon(_P(n, [(-0.86, -0.1), (-0.4, -0.42), (0.2, -0.46), (0.82, -0.12), (0.2, 0.16), (-0.4, 0.14)]), fill=F)
        d.polygon(_P(n, [(-0.66, -0.12), (-0.3, -0.3), (0.2, -0.32), (0.6, -0.12), (0.2, 0.04), (-0.3, 0.02)]), fill=255)
        _elipse(d, n, -0.06, -0.14, 0.17, 0.17, F)
        d.line(_P(n, [(-0.9, -0.5), (-0.4, -0.7), (0.3, -0.7), (0.9, -0.44)]), fill=F, width=max(4, n // 22))
        d.line(_P(n, [(-0.2, 0.12), (-0.24, 0.85)]), fill=F, width=max(4, n // 22))
        d.line(_P(n, [(0.12, 0.14), (0.3, 0.5), (0.58, 0.58), (0.68, 0.38), (0.52, 0.3)]), fill=F, width=max(3, n // 26))
    elif nombre == "aton":
        _elipse(d, n, 0.0, -0.36, 0.38, 0.38, F)
        _elipse(d, n, 0.0, -0.36, 0.2, 0.2, 255)
        _elipse(d, n, 0.0, -0.36, 0.1, 0.1, F)
        for k in range(7):
            a = math.radians(35 + 110 * k / 6)
            x0, y0 = 0.44 * math.cos(a), -0.36 + 0.44 * math.sin(a)
            x1, y1 = 1.0 * math.cos(a), -0.36 + 1.16 * math.sin(a)
            d.line(_P(n, [(x0, y0), (x1, y1)]), fill=F, width=max(2, n // 40))
            _elipse(d, n, x1, y1, 0.07, 0.07, F)
    elif nombre == "cartucho":
        d.rounded_rectangle([*_P(n, [(-0.48, -0.92)])[0], *_P(n, [(0.48, 0.74)])[0]], radius=int(n * 0.16), fill=F)
        d.rounded_rectangle([*_P(n, [(-0.34, -0.78)])[0], *_P(n, [(0.34, 0.6)])[0]], radius=int(n * 0.12), fill=255)
        d.rectangle([*_P(n, [(-0.48, 0.74)])[0], *_P(n, [(0.48, 0.9)])[0]], fill=F)
        _elipse(d, n, 0.0, -0.5, 0.15, 0.15, F)
        d.polygon(_P(n, [(-0.2, 0.08), (0.0, -0.18), (0.18, -0.1), (0.1, 0.02), (0.2, 0.12)]), fill=F)
        d.line(_P(n, [(-0.2, 0.38), (0.2, 0.38)]), fill=F, width=w3)
        d.line(_P(n, [(0.0, 0.3), (0.0, 0.52)]), fill=F, width=w3)
    elif nombre == "alas":
        _elipse(d, n, 0.0, -0.1, 0.24, 0.24, F)
        for lado in (-1, 1):
            for k in range(4):
                y = -0.2 + 0.13 * k
                d.polygon(_P(n, [(lado * 0.24, y - 0.04), (lado * (0.95 - 0.12 * k), y - 0.12 + 0.02 * k), (lado * (0.95 - 0.12 * k), y + 0.02),
                                 (lado * 0.24, y + 0.06)]), fill=F)
        d.polygon(_P(n, [(-0.16, 0.16), (0.16, 0.16), (0.1, 0.72), (0.0, 0.84), (-0.1, 0.72)]), fill=F)
    elif nombre == "faro":
        d.polygon(_P(n, [(-0.42, 0.9), (-0.32, 0.12), (0.32, 0.12), (0.42, 0.9)]), fill=F)
        d.polygon(_P(n, [(-0.26, 0.12), (-0.2, -0.38), (0.2, -0.38), (0.26, 0.12)]), fill=F)
        d.rectangle([*_P(n, [(-0.13, -0.66)])[0], *_P(n, [(0.13, -0.38)])[0]], fill=F)
        _elipse(d, n, 0.0, -0.52, 0.07, 0.07, 255)
        d.polygon(_P(n, [(0.16, -0.54), (0.95, -0.84), (0.95, -0.28)]), fill=F)
        d.line(_P(n, [(0.0, -0.66), (0.0, -0.9)]), fill=F, width=w3)
        for y in (0.3, 0.5, 0.7):
            d.line(_P(n, [(-0.36, y), (0.36, y)]), fill=255, width=max(1, n // 70))
    elif nombre == "minarete":
        d.rectangle([*_P(n, [(-0.16, -0.2)])[0], *_P(n, [(0.16, 0.9)])[0]], fill=F)
        d.rectangle([*_P(n, [(-0.26, -0.26)])[0], *_P(n, [(0.26, -0.16)])[0]], fill=F)
        d.polygon(_P(n, [(-0.11, -0.26), (-0.13, -0.6), (0.13, -0.6), (0.11, -0.26)]), fill=F)
        d.polygon(_P(n, [(-0.13, -0.6), (0.0, -0.78), (0.13, -0.6)]), fill=F)
        d.arc([*_P(n, [(-0.12, -1.0)])[0], *_P(n, [(0.12, -0.78)])[0]], 30, 330, fill=F, width=w3)
        d.chord([*_P(n, [(-0.08, 0.3)])[0], *_P(n, [(0.08, 0.5)])[0]], 180, 360, fill=255)
        d.rectangle([*_P(n, [(-0.08, 0.4)])[0], *_P(n, [(0.08, 0.6)])[0]], fill=255)
        for x in (-0.7, 0.7):
            d.polygon(_P(n, [(x - 0.2, 0.9), (x - 0.2, 0.3), (x, 0.1), (x + 0.2, 0.3), (x + 0.2, 0.9)]), fill=F)
    elif nombre == "espadas":
        for lado in (-1, 1):
            pts = [(lado * -0.7, 0.86), (lado * -0.6, 0.94), (lado * 0.1, 0.1), (lado * 0.5, -0.5), (lado * 0.86, -0.9), (lado * 0.62, -0.46),
                   (lado * 0.22, 0.08)]
            d.polygon(_P(n, pts), fill=F)
            d.line(_P(n, [(lado * -0.78, 0.56), (lado * -0.36, 0.84)]), fill=F, width=max(4, n // 20))
    elif nombre == "ancla":
        _elipse(d, n, 0.0, -0.72, 0.14, 0.14, F)
        _elipse(d, n, 0.0, -0.72, 0.06, 0.06, 255)
        d.rectangle([*_P(n, [(-0.07, -0.6)])[0], *_P(n, [(0.07, 0.7)])[0]], fill=F)
        d.rectangle([*_P(n, [(-0.42, -0.42)])[0], *_P(n, [(0.42, -0.3)])[0]], fill=F)
        d.arc([*_P(n, [(-0.72, -0.1)])[0], *_P(n, [(0.72, 0.84)])[0]], 10, 170, fill=F, width=max(4, n // 18))
        for lado in (-1, 1):
            d.polygon(_P(n, [(lado * 0.72, 0.28), (lado * 0.88, 0.2), (lado * 0.7, 0.52)]), fill=F)
    elif nombre == "aguila":
        d.polygon(_P(n, [(-0.95, -0.5), (-0.7, -0.25), (-0.36, -0.2), (-0.24, 0.1), (-0.28, 0.5), (0.0, 0.86), (0.28, 0.5), (0.24, 0.1), (0.36, -0.2),
                         (0.7, -0.25), (0.95, -0.5), (0.62, -0.5), (0.34, -0.42), (0.18, -0.48), (0.12, -0.74), (0.0, -0.86), (-0.12, -0.74),
                         (-0.18, -0.48), (-0.34, -0.42), (-0.62, -0.5)]), fill=F)
        d.rectangle([*_P(n, [(-0.16, -0.16)])[0], *_P(n, [(0.16, 0.36)])[0]], fill=255)
        d.rectangle([*_P(n, [(-0.16, 0.0)])[0], *_P(n, [(0.16, 0.18)])[0]], fill=F)
        _elipse(d, n, 0.04, -0.72, 0.04, 0.04, 255)
    else:
        return False
    return True


def _dibujar(d, n, nombre):
    F = 0                    # hueco (el papel)
    if _dibujar_eg(d, n, nombre):
        return
    if nombre == "laurel":
        for lado in (-1, 1):
            for k in range(7):
                a = math.radians(105 + k * 24) if lado < 0 else math.radians(75 - k * 24)
                cx, cy = 0.78 * math.cos(a), 0.78 * math.sin(a) * 0.95
                tang = a + (math.pi / 2 if lado < 0 else -math.pi / 2)
                d.polygon(_P(n, _hoja(cx, cy, tang + lado * 0.5, 0.36, 0.12)), fill=F)
            d.line(_P(n, [(0.78 * math.cos(math.radians(a_)), 0.74 * math.sin(math.radians(a_))) for a_ in
                          (range(100, 262, 6) if lado < 0 else range(80, -82, -6))]), fill=F, width=max(2, n // 40))
        d.polygon(_P(n, [(-0.2, 0.86), (0.0, 0.70), (0.2, 0.86), (0.28, 1.05), (0.0, 0.88), (-0.28, 1.05)]), fill=F)
        d.text((n * 0.5, n * 0.5), "SPQR", fill=F, anchor="mm", font=_fuente(int(n * 0.17)))
    elif nombre == "corona":
        d.polygon(_P(n, [(-0.72, -0.28), (0.72, -0.28), (0.66, 0.14), (-0.66, 0.14)]), fill=F)
        for x in (-0.6, -0.2, 0.2, 0.6):
            d.polygon(_P(n, [(x - 0.12, -0.28), (x, -0.62), (x + 0.12, -0.28)]), fill=F)
        for x in np.linspace(-0.56, 0.56, 6):
            d.line(_P(n, [(x, 0.14), (x, 0.52)]), fill=F, width=max(2, n // 45))
            _elipse(d, n, x, 0.58, 0.06, 0.08, F)
        d.line(_P(n, [(0.0, 0.14), (0.0, 0.92)]), fill=F, width=max(3, n // 30))
        d.line(_P(n, [(-0.16, 0.66), (0.16, 0.66)]), fill=F, width=max(3, n // 30))
    elif nombre == "arco":
        d.rectangle([*_P(n, [(-0.82, -0.05)])[0], *_P(n, [(-0.56, 0.92)])[0]], fill=F)
        d.rectangle([*_P(n, [(0.56, -0.05)])[0], *_P(n, [(0.82, 0.92)])[0]], fill=F)
        for k in range(11):                                     # dovelas alternas, como en la mezquita de Córdoba
            a0 = math.radians(200 + k * 14)
            a1 = math.radians(200 + (k + 1) * 14)
            if k % 2:
                continue
            pts = [(0.52 * math.cos(a0), 0.08 + 0.58 * math.sin(a0)), (0.86 * math.cos(a0), 0.08 + 0.9 * math.sin(a0)),
                   (0.86 * math.cos(a1), 0.08 + 0.9 * math.sin(a1)), (0.52 * math.cos(a1), 0.08 + 0.58 * math.sin(a1))]
            d.polygon(_P(n, pts), fill=F)
        d.arc([*_P(n, [(-0.86, -0.82)])[0], *_P(n, [(0.86, 0.98)])[0]], 200, 340, fill=F, width=max(2, n // 40))
    elif nombre == "castillo":
        d.rectangle([*_P(n, [(-0.8, -0.05)])[0], *_P(n, [(0.8, 0.85)])[0]], fill=F)
        for x0, x1, top in ((-0.8, -0.4, -0.45), (-0.22, 0.22, -0.78), (0.4, 0.8, -0.45)):
            d.rectangle([*_P(n, [(x0, top)])[0], *_P(n, [(x1, 0.0)])[0]], fill=F)
            w = (x1 - x0) / 5
            for j in (0, 2, 4):
                d.rectangle([*_P(n, [(x0 + j * w, top - 0.16)])[0], *_P(n, [(x0 + (j + 1) * w, top)])[0]], fill=F)
        d.chord([*_P(n, [(-0.22, 0.30)])[0], *_P(n, [(0.22, 0.75)])[0]], 180, 360, fill=255)
        d.rectangle([*_P(n, [(-0.22, 0.52)])[0], *_P(n, [(0.22, 0.86)])[0]], fill=255)
        for x in (-0.6, 0.6):
            d.rectangle([*_P(n, [(x - 0.05, -0.32)])[0], *_P(n, [(x + 0.05, -0.12)])[0]], fill=255)
    elif nombre == "yugo":
        for k in range(5):                                      # haz de flechas
            a = math.radians(-90 + (k - 2) * 15)
            x1, y1 = 0.95 * math.cos(a), 0.62 + 1.5 * math.sin(a)
            d.line(_P(n, [(0.0, 0.62), (x1 * 0.9, y1)]), fill=F, width=max(3, n // 34))
            ux, uy = math.cos(a), math.sin(a)
            tip = (x1 * 0.9 + ux * 0.12, y1 + uy * 0.12)
            px_, py_ = -uy, ux
            d.polygon(_P(n, [tip, (x1 * 0.9 + px_ * 0.08, y1 + py_ * 0.08), (x1 * 0.9 - px_ * 0.08, y1 - py_ * 0.08)]), fill=F)
        d.arc([*_P(n, [(-0.9, -0.05)])[0], *_P(n, [(-0.1, 0.75)])[0]], 180, 360, fill=F, width=max(4, n // 22))
        d.arc([*_P(n, [(0.1, -0.05)])[0], *_P(n, [(0.9, 0.75)])[0]], 180, 360, fill=F, width=max(4, n // 22))
        d.line(_P(n, [(-0.95, 0.35), (0.95, 0.35)]), fill=F, width=max(4, n // 22))
    elif nombre == "columnas":
        for cx in (-0.48, 0.48):
            d.rectangle([*_P(n, [(cx - 0.14, -0.62)])[0], *_P(n, [(cx + 0.14, 0.72)])[0]], fill=F)
            d.rectangle([*_P(n, [(cx - 0.26, -0.82)])[0], *_P(n, [(cx + 0.26, -0.64)])[0]], fill=F)
            d.rectangle([*_P(n, [(cx - 0.26, 0.72)])[0], *_P(n, [(cx + 0.26, 0.92)])[0]], fill=F)
            for k in range(2):
                d.line(_P(n, [(cx - 0.05 + 0.1 * k, -0.58), (cx - 0.05 + 0.1 * k, 0.68)]), fill=255, width=max(1, n // 80))
        pts = [(-0.95, -0.1), (-0.5, 0.15), (0.0, -0.05), (0.5, 0.15), (0.95, -0.1), (0.95, 0.12), (0.5, 0.37), (0.0, 0.17), (-0.5, 0.37), (-0.95, 0.12)]
        d.polygon(_P(n, pts), fill=F)
        d.text((n * 0.5, n * 0.5 + n * 0.045), "PLVS VLTRA", fill=255, anchor="mm", font=_fuente(int(n * 0.085)))
    elif nombre == "lis":
        pts = [(0.0, -0.95), (0.16, -0.62), (0.16, -0.2), (0.07, 0.15), (-0.07, 0.15), (-0.16, -0.2), (-0.16, -0.62)]
        d.polygon(_P(n, pts), fill=F)
        for lado in (-1, 1):
            pts = [(lado * 0.07, 0.12), (lado * 0.30, -0.05), (lado * 0.58, -0.40), (lado * 0.78, -0.30), (lado * 0.80, -0.02),
                   (lado * 0.62, 0.20), (lado * 0.40, 0.25), (lado * 0.62, 0.0), (lado * 0.56, -0.20), (lado * 0.36, 0.08), (lado * 0.10, 0.26)]
            d.polygon(_P(n, pts), fill=F)
        d.rectangle([*_P(n, [(-0.46, 0.22)])[0], *_P(n, [(0.46, 0.36)])[0]], fill=F)
        d.polygon(_P(n, [(-0.12, 0.36), (0.12, 0.36), (0.2, 0.85), (0.0, 0.7), (-0.2, 0.85)]), fill=F)
    elif nombre == "libro":
        d.polygon(_P(n, [(-0.92, -0.55), (-0.05, -0.42), (-0.05, 0.75), (-0.92, 0.6)]), fill=F)
        d.polygon(_P(n, [(0.92, -0.55), (0.05, -0.42), (0.05, 0.75), (0.92, 0.6)]), fill=F)
        for k in range(5):
            y = -0.30 + 0.18 * k
            d.line(_P(n, [(-0.80, y), (-0.18, y + 0.08)]), fill=255, width=max(1, n // 60))
            d.line(_P(n, [(0.80, y), (0.18, y + 0.08)]), fill=255, width=max(1, n // 60))
        d.text((n * 0.5, n * 0.5 - n * 0.30), "1812", fill=F, anchor="mm", font=_fuente(int(n * 0.14)))
    elif nombre == "gorro":
        pts = [(-0.66, 0.50), (-0.72, 0.05), (-0.58, -0.42), (-0.25, -0.74), (0.18, -0.84), (0.55, -0.72), (0.80, -0.42), (0.86, -0.08),
               (0.70, 0.02), (0.62, -0.28), (0.42, -0.42), (0.36, -0.10), (0.56, 0.50)]
        d.polygon(_P(n, pts), fill=F)
        d.rounded_rectangle([*_P(n, [(-0.78, 0.44)])[0], *_P(n, [(0.66, 0.74)])[0]], radius=max(2, n // 40), fill=F)
        _elipse(d, n, -0.34, 0.59, 0.11, 0.11, 255)
        _elipse(d, n, -0.34, 0.59, 0.05, 0.05, F)
    elif nombre == "urna":
        d.polygon(_P(n, [(-0.72, -0.20), (0.72, -0.20), (0.62, 0.85), (-0.62, 0.85)]), fill=F)
        d.rectangle([*_P(n, [(-0.36, -0.28)])[0], *_P(n, [(0.36, -0.14)])[0]], fill=255)
        d.polygon(_P(n, [(-0.26, -0.20), (-0.22, -0.92), (0.30, -0.86), (0.26, -0.20)]), fill=F)
        d.line(_P(n, [(-0.10, -0.72), (0.14, -0.70)]), fill=255, width=max(2, n // 50))
        d.line(_P(n, [(-0.12, -0.55), (0.12, -0.53)]), fill=255, width=max(2, n // 50))
        d.line(_P(n, [(-0.30, 0.30), (-0.10, 0.52), (0.34, 0.06)]), fill=255, width=max(3, n // 28))


@lru_cache(maxsize=8)
def _fuente(px):
    from PIL import ImageFont
    return ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", max(8, px))


@lru_cache(maxsize=96)
def mascara(nombre, px=150, rot=0.0):
    """Sello: cuadrado redondeado lleno, filete interior y el emblema en hueco."""
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


NOMBRES = ("corona_doble", "piramide", "anj", "ojo", "aton", "cartucho", "alas", "faro", "laurel", "minarete", "castillo", "espadas", "ancla", "aguila")

if __name__ == "__main__":
    tiles = [mascara(n, 170) for n in NOMBRES]
    hoja = np.hstack([np.pad(255 - t, 8, constant_values=255) for t in tiles])
    cv2.imwrite("previews/sellos.png", hoja)
