# -*- coding: utf-8 -*-
"""Miniaturas de Cronopapel para «La historia de Aguascalientes» (22-oct-2026), hechas con el motor del video (receta de
historia_jalisco). Fondo = el mapa del propio video (relieve real y el estado pintado a guache) sin actores; encima, pegatinas de
Flow grandes (el escudo de los labios, Pancho Villa, la Catrina, el Cristo Roto) y el texto en Impact.
Uso: python fab.py historia_aguascalientes miniatura   (o ./run.sh miniaturas.py [variante])"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import boceto as B
import escenas as E
from core import T
from escena_base import TL
from motor import H, W
from pegflow import P

XI = lambda n, **k: P("05_xix_hoja", n, **k)
AR = lambda n, **k: P("06_arte_hoja", n, **k)
RV = lambda n, **k: P("08_revolucion_hoja", n, **k)
SX = lambda n, **k: P("09_sigloxx_hoja", n, **k)
_FONDO = {}


def _fondo(t=None, oscurecer=0.84):
    """Mapa del video en el instante t (el estado coloreado entero), sin actores, sellos ni contador."""
    if t is None:
        t = T("siglo20", "5616") + 0.6
    if t not in _FONDO:
        m = E.Mundo(TL["escenas"][0], 0)
        m.render(None, t)
        _FONDO[t] = np.clip(np.array(m.hf.componer(), dtype=np.float32), 0, 1)
    img = _FONDO[t].copy()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vi = 1.0 - 0.38 * np.clip(np.hypot((xx - W * 0.55) / (W * 0.62), (yy - H * 0.5) / (H * 0.62)) - 0.45, 0, 1)
    return np.clip(img * oscurecer * vi[..., None], 0, 1)


def _texto(linea1, linea2, px1, px2, col1=(255, 255, 255), col2=(255, 226, 30), rot=-3.0, sw=11):
    f1 = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", px1)
    f2 = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", px2)
    b1, b2 = f1.getbbox(linea1), f2.getbbox(linea2)
    w1, h1, w2, h2 = b1[2] - b1[0], b1[3] - b1[1], b2[2] - b2[0], b2[3] - b2[1]
    pad, inter = int(max(px1, px2) * 0.3), int(px1 * 0.14)
    tw, th = max(w1, w2) + pad * 2, h1 + h2 + inter + pad * 2
    masc, rgb = Image.new("L", (tw, th), 0), Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    dm, dr = ImageDraw.Draw(masc), ImageDraw.Draw(rgb)
    p1 = (pad - b1[0], pad - b1[1])
    p2 = (pad - b2[0], pad - b2[1] + h1 + inter)
    for p, txt, f, col in ((p1, linea1, f1, col1), (p2, linea2, f2, col2)):
        dm.text(p, txt, font=f, fill=255, stroke_width=sw + 10, stroke_fill=255)
        dr.text((p[0] + 7, p[1] + 9), txt, font=f, fill=(20, 18, 22, 255), stroke_width=sw, stroke_fill=(20, 18, 22, 255))
        dr.text(p, txt, font=f, fill=col + (255,), stroke_width=sw, stroke_fill=(28, 26, 30, 255))
    masc, rgb = masc.rotate(-rot, resample=Image.BICUBIC, expand=True), rgb.rotate(-rot, resample=Image.BICUBIC, expand=True)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
    return np.asarray(rgb), cv2.dilate((np.asarray(masc) > 20).astype(np.uint8) * 255, k)


def _pegar_texto(h, capas, arr, masc, x0, y0):
    """Texto con su borde de pegatina; (x0, y0) = esquina superior izquierda."""
    th, tw = masc.shape
    h.peg_mascara(masc, x0, y0)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + tw), min(H, y0 + th)
    sub = arr[ya - y0:yb - y0, xa - x0:xb - x0]
    capas.append((xa, ya, xb, yb, sub[..., :3].astype(np.float32) / 255.0, sub[..., 3:4].astype(np.float32) / 255.0))


def _componer(h, capas):
    out = np.clip(h.componer(), 0, 1)
    for xa, ya, xb, yb, col, a in capas:
        out[ya:yb, xa:xb] = out[ya:yb, xa:xb] * (1 - a) + col * a
    return out


def _dib(h, d, x, y, s, rot=0.0, flip=False, sem=1):
    d.dibujar(h, x, y, s, rot, flip, 1.0, 0, sem, peg=True)


def historia(lz=None):
    """AGUASCALIENTES / SU HISTORIA: el escudo de los labios, Villa, la Catrina y el Cristo Roto."""
    h = B.Hoja()
    h.limpiar()
    h.fondo = _fondo()
    capas = []
    _dib(h, SX(2), 300, 1070, 1.55, 0.0, sem=2)
    _dib(h, XI(6), 760, 1070, 1.25, -0.04, sem=3)
    _dib(h, RV(0), 1220, 1070, 1.55, 0.02, sem=4)
    _dib(h, AR(2), 1660, 1070, 1.65, 0.0, sem=5)
    arr, masc = _texto("AGUASCALIENTES", "SU HISTORIA", 200, 150)
    _pegar_texto(h, capas, arr, masc, 30, 20)
    return _componer(h, capas)


def beso(lz=None):
    """¿UN BESO FUNDÓ / UN ESTADO?: Santa Anna, la dama y el escudo con los labios."""
    h = B.Hoja()
    h.limpiar()
    h.fondo = _fondo()
    capas = []
    _dib(h, XI(0), 330, 1070, 1.7, 0.0, sem=6)
    _dib(h, XI(6), 960, 1080, 1.6, -0.03, sem=7)
    _dib(h, XI(1), 1600, 1070, 1.7, 0.0, flip=True, sem=8)
    arr, masc = _texto("¿UN BESO FUNDÓ", "UN ESTADO?", 190, 170)
    _pegar_texto(h, capas, arr, masc, 60, 20)
    return _componer(h, capas)


VARIANTES = {"historia": historia, "beso": beso}


if __name__ == "__main__":
    import sys
    for n in (sys.argv[1:] or list(VARIANTES)):
        im = VARIANTES[n]()
        f = f"salida/historia_aguascalientes_mini_{n}.jpg"
        cv2.imwrite(f, (np.clip(im, 0, 1)[..., ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(f)
