# -*- coding: utf-8 -*-
"""Miniaturas 1280x720 del documental (python hacer_miniaturas.py, desde la carpeta del video con PYTHONPATH=<nucleo>;.).
Salida: salida/tesoro_moctezuma_mini_<variante>.jpg y previews/miniaturas.jpg (con vista a tamaño de celular)."""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8
import escenas as S
import docu as D

W, H = 1280, 720
AMARILLO, BLANCO, NEGRO = (255, 226, 30), (255, 255, 255), (0, 0, 0)
IMPACT = "C:/Windows/Fonts/impact.ttf"


def cubrir(nombre, brillo=0.55, cx=0.5, cy=0.5, zoom=1.0, tinte=(1, 1, 1)):
    im = D.cargar(D.ruta_img(nombre), 2600).astype(np.float32) / 255.0
    h, w = im.shape[:2]
    k = max(W / w, H / h) * zoom
    M = np.array([[k, 0, W / 2 - cx * w * k], [0, k, H / 2 - cy * h * k]], np.float32)
    out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return np.clip(out * brillo * np.float32(tinte), 0, 1)


def vineta(img, fuerza=0.75):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
    return img * (1 - fuerza * np.clip(r - 0.35, 0, 1) ** 1.6)[..., None]


def brillo_oro(img, cx, cy, r, k):
    g = S._glow_map()
    s = int(2 * r)
    m = cv2.resize(g, (s, s))
    x0, y0 = int(cx - s / 2), int(cy - s / 2)
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + s, W), min(y0 + s, H)
    img[ya:yb, xa:xb] += m[ya - y0:yb - y0, xa - x0:xb - x0, None] * np.float32(S.ORO) * k
    return img


def pegar_barra(img, cx, cy, ancho, rot):
    sp = S.barra_sp()
    a = sp.a
    pm = sp.pm
    k = ancho / sp.w
    M = cv2.getRotationMatrix2D((sp.w / 2, sp.h / 2), rot, k)
    M[0, 2] += cx - sp.w / 2
    M[1, 2] += cy - sp.h / 2
    aw = cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR)
    pw = cv2.warpAffine(pm, M, (W, H), flags=cv2.INTER_LINEAR)
    sh = cv2.GaussianBlur(aw, (0, 0), 14)
    sh = np.roll(np.roll(sh, 16, 0), 10, 1)
    img *= (1 - 0.6 * sh)[..., None]
    img *= (1 - aw)[..., None]
    img += pw
    return img


def texto(img, lineas, x, y, px, colores, rot=0.0, borde=15, alinear="izq"):
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    f = ImageFont.truetype(IMPACT, px)
    yy = y
    for ln, col in zip(lineas, colores):
        w = d.textlength(ln, font=f)
        xx = x if alinear == "izq" else (x - w if alinear == "der" else x - w / 2)
        d.text((xx, yy), ln, font=f, fill=col, stroke_width=borde, stroke_fill=NEGRO)
        yy += px * 1.02
    if rot:
        capa = capa.rotate(rot, resample=Image.BICUBIC, center=(x, y))
    pil.alpha_composite(capa)
    return np.asarray(pil.convert("RGB"), np.float32) / 255.0


def guardar(img, nombre):
    os.makedirs("salida", exist_ok=True)
    ruta = f"salida/tesoro_moctezuma_mini_{nombre}.jpg"
    cv2.imwrite(ruta, cv2.cvtColor((np.clip(img, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    return ruta


_LZ = Lienzo()


def cuadro(t, brillo=1.0, zoom=1.0, cx=0.5, cy=0.5):
    """Cuadro del video animado a 1280x720 (con zoom opcional)."""
    img = S.render_mundo(_LZ, t)
    img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    if zoom != 1.0:
        M = np.array([[zoom, 0, W / 2 - cx * W * zoom], [0, zoom, H / 2 - cy * H * zoom]], np.float32)
        img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return np.clip(img * brillo, 0, 1)


def oro():
    img = cuadro(164.0, 1.0, 1.55, 0.40, 0.50)
    img = vineta(img, 0.55)
    img = texto(img, ["ORO", "PERDIDO"], 40, 40, 200, [BLANCO, AMARILLO], rot=1.5)
    return img


def donde():
    img = cuadro(316.9, 1.0, 1.35, 0.5, 0.66)
    img = vineta(img, 0.5)
    img = texto(img, ["¿DÓNDE", "ESTÁ?"], 40, 30, 200, [AMARILLO, BLANCO], rot=0.0)
    return img


def hundido():
    img = cuadro(175.3, 1.0, 1.5, 0.45, 0.50)
    img = vineta(img, 0.5)
    img = texto(img, ["NUNCA", "APARECIÓ"], 40, 40, 200, [BLANCO, AMARILLO], rot=1.0)
    return img


VARIANTES = {"oro": oro, "donde": donde, "hundido": hundido}


def celular(img):
    return cv2.resize(cv2.resize(img, (168, 94), interpolation=cv2.INTER_AREA), (W // 2, H // 2), interpolation=cv2.INTER_NEAREST)


if __name__ == "__main__":
    ims = []
    for n, fn in VARIANTES.items():
        im = fn()
        print(guardar(im, n))
        ims.append(im)
    fila1 = np.hstack([cv2.resize(i, (640, 360), interpolation=cv2.INTER_AREA) for i in ims[:2]])
    fila2 = np.hstack([cv2.resize(ims[2], (640, 360), interpolation=cv2.INTER_AREA)] + [celular(i)[:360, :640] if False else cv2.resize(celular(ims[0]), (640, 360)) ])
    hoja = np.vstack([fila1, fila2])
    cv2.imwrite("previews/miniaturas.jpg", cv2.cvtColor((np.clip(hoja, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
