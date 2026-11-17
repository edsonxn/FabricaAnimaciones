# -*- coding: utf-8 -*-
"""Arte del canal «Radio Yermo» (17-nov-2026): fósforo verde de terminal/Pip-Boy, como una estación de radio que transmite
desde el Yermo. Todo por código (sin marcas ni capturas de Bethesda):
  BANNER_2560x1440.jpg  (zona visible en todos los dispositivos = 1546x423 al centro; el texto va dentro)
  LOGO_800.jpg
  _banner_zona_segura.jpg  y  _logo_chico.jpg  (para revisar)
python canales/arte/radio_yermo/arte.py
"""
import math
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F = "C:/Windows/Fonts/"
VERDE = (60, 255, 140)          # fósforo
FONDO = (4, 13, 7)


def fuente(nombre, tam):
    return ImageFont.truetype(F + nombre, tam)


# ------------------------------------------------------------------ utilidades de dibujo (máscara 0..255, luego se tiñe)
def torre(d, cx, base, alto, ancho, w=4, op=255):
    """Torre de radio de celosía con antena y luz en la punta."""
    top = base - alto
    xl0, xr0 = cx - ancho / 2, cx + ancho / 2
    xl1, xr1 = cx - ancho * 0.08, cx + ancho * 0.08
    d.line([(xl0, base), (xl1, top)], fill=op, width=w)
    d.line([(xr0, base), (xr1, top)], fill=op, width=w)
    n = 9
    prev = None
    for i in range(n + 1):
        f = i / n
        y = base - alto * f
        xl = xl0 + (xl1 - xl0) * f
        xr = xr0 + (xr1 - xr0) * f
        d.line([(xl, y), (xr, y)], fill=op, width=max(1, w - 1))
        if prev:
            d.line([prev[0], (xr, y)], fill=op, width=max(1, w - 2))
            d.line([prev[1], (xl, y)], fill=op, width=max(1, w - 2))
        prev = ((xl, y), (xr, y))
    d.line([(cx, top), (cx, top - alto * 0.18)], fill=op, width=w)
    r = max(4, w * 1.6)
    d.ellipse([cx - r, top - alto * 0.18 - r, cx + r, top - alto * 0.18 + r], fill=op)
    return cx, top - alto * 0.18


def ondas(d, cx, cy, radios, w, op=255, abertura=50):
    for k, r in enumerate(radios):
        o = int(op * (1 - k * 0.18))
        for a0 in (-abertura, 180 - abertura):
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 2 * abertura, fill=o, width=w)


def ruinas(d, x0, x1, suelo, hmax, sem, op=255, w=3):
    """Horizonte de ciudad en ruinas: edificios rotos con ventanas, tanque de agua, autopista caída."""
    rnd = random.Random(sem)
    x = x0
    while x < x1:
        bw = rnd.randint(50, 150)
        bh = rnd.randint(int(hmax * 0.25), hmax)
        top = suelo - bh
        # techo roto: polilínea dentada
        pts = [(x, suelo), (x, top + rnd.randint(0, 30))]
        nx = x
        while nx < x + bw:
            nx = min(x + bw, nx + rnd.randint(10, 35))
            pts.append((nx, top + rnd.randint(0, 45)))
        pts.append((x + bw, suelo))
        d.line(pts, fill=op, width=w, joint="curve")
        # ventanas
        for wy in range(int(top + 50), int(suelo - 20), 28):
            for wx in range(int(x + 12), int(x + bw - 12), 22):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 8, wy + 12], outline=int(op * 0.55), width=1)
                elif rnd.random() < 0.12:
                    d.rectangle([wx, wy, wx + 8, wy + 12], fill=int(op * 0.9))   # una luz que sigue prendida
        x += bw + rnd.randint(6, 40)


def tanque_agua(d, cx, suelo, alto, op=255, w=3):
    r = alto * 0.22
    top = suelo - alto
    d.ellipse([cx - r, top, cx + r, top + r * 1.1], outline=op, width=w)
    d.rectangle([cx - r, top + r * 0.55, cx + r, top + r * 1.6], outline=op, width=w)
    d.polygon([(cx - r * 1.1, top + r * 0.6), (cx, top - r * 0.55), (cx + r * 1.1, top + r * 0.6)], outline=op, width=w)
    for s in (-1, 1):
        d.line([(cx + s * r * 0.8, top + r * 1.6), (cx + s * r * 1.3, suelo)], fill=op, width=w)
    d.line([(cx - r * 1.05, top + r * 2.6), (cx + r * 1.05, top + r * 2.6)], fill=op, width=w - 1)
    d.line([(cx - r * 0.8, top + r * 1.6), (cx + r * 1.2, top + r * 2.6)], fill=op, width=w - 1)


def hongo(d, cx, suelo, alto, op=120, w=3):
    """Hongo atómico lejano, solo contorno."""
    tallo = alto * 0.55
    d.line([(cx - alto * 0.06, suelo), (cx - alto * 0.04, suelo - tallo)], fill=op, width=w)
    d.line([(cx + alto * 0.06, suelo), (cx + alto * 0.04, suelo - tallo)], fill=op, width=w)
    for k in range(3):
        rr = alto * (0.12 + 0.06 * k)
        d.arc([cx - rr * 1.6, suelo - tallo - rr * 1.2 - k * alto * 0.05, cx + rr * 1.6, suelo - tallo + rr * 0.8 - k * alto * 0.05],
              180, 360, fill=op, width=w)
    d.ellipse([cx - alto * 0.32, suelo - tallo * 0.55, cx + alto * 0.32, suelo - tallo * 0.42], outline=int(op * 0.7), width=w - 1)


def dial(d, x0, x1, y, alto, aguja, op=255):
    """Sintonizador de radio con números 88-108 y la aguja en 20.77 (el año de las bombas, guiño)."""
    d.rounded_rectangle([x0, y, x1, y + alto], radius=alto // 5, outline=op, width=3)
    f = fuente("consolab.ttf", int(alto * 0.26))
    n = 41
    for i in range(n):
        x = x0 + 30 + (x1 - x0 - 60) * i / (n - 1)
        largo = alto * (0.34 if i % 5 == 0 else 0.18)
        d.line([(x, y + alto - 10), (x, y + alto - 10 - largo)], fill=int(op * 0.8), width=2)
        if i % 10 == 0:
            t = str(88 + i // 2)
            tw = d.textlength(t, font=f)
            d.text((x - tw / 2, y + 8), t, fill=int(op * 0.8), font=f)
    xa = x0 + 30 + (x1 - x0 - 60) * aguja
    d.line([(xa, y + 6), (xa, y + alto - 6)], fill=op, width=5)


def texto_centrado(d, cx, y, t, f, op=255, esp=0):
    if esp:
        anchos = [d.textlength(c, font=f) for c in t]
        total = sum(anchos) + esp * (len(t) - 1)
        x = cx - total / 2
        for c, a in zip(t, anchos):
            d.text((x, y), c, fill=op, font=f)
            x += a + esp
        return total
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, y), t, fill=op, font=f)
    return tw


# ------------------------------------------------------------------ acabado CRT
def fosforo(mask, curvar=0.0, lineas=4, vig=0.55, grano=0.05, sem=1):
    """Máscara 0..255 -> imagen de fósforo verde con brillo, líneas de barrido, viñeta y grano."""
    m = mask.astype(np.float32) / 255.0
    h, w = m.shape
    glow = cv2.GaussianBlur(m, (0, 0), max(w, h) / 260) * 0.9 + cv2.GaussianBlur(m, (0, 0), max(w, h) / 70) * 0.55
    v = np.clip(m + glow, 0, 1.4)
    yy = np.arange(h)[:, None]
    scan = 0.82 + 0.18 * (np.sin(yy * math.pi * 2 / lineas) * 0.5 + 0.5)
    v = v * scan
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    rr = ((xs - w / 2) / (w / 2)) ** 2 + ((ys - h / 2) / (h / 2)) ** 2
    viñeta = np.clip(1 - vig * rr * 0.6, 0.15, 1)
    rng = np.random.default_rng(sem)
    ruido = 1 + (rng.random((h, w), dtype=np.float32) - 0.5) * grano
    v = v * viñeta * ruido
    fondo = np.array(FONDO, np.float32)[None, None] / 255 * (0.6 + 0.4 * viñeta[..., None])
    color = np.array(VERDE, np.float32)[None, None] / 255
    img = fondo + v[..., None] * color
    blanco = np.clip(v - 1.0, 0, 0.4)[..., None]          # el centro de las letras quema a casi blanco
    img = img + blanco * 0.9
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def guardar(rgb, nombre, q=95):
    ruta = os.path.join(AQUI, nombre)
    Image.fromarray(rgb).save(ruta, quality=q)
    return ruta


# ------------------------------------------------------------------ banner
def banner():
    W, H = 2560, 1440
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    cx = W // 2
    sx0, sx1, sy0, sy1 = (W - 1546) // 2, (W + 1546) // 2, (H - 423) // 2, (H + 423) // 2
    suelo = sy1 + 120
    # rejilla de terminal tenue
    for x in range(0, W, 64):
        d.line([(x, 0), (x, H)], fill=14, width=1)
    for y in range(0, H, 64):
        d.line([(0, y), (W, y)], fill=14, width=1)
    hongo(d, 380, suelo - 30, 520, op=70, w=3)
    ruinas(d, 0, W, suelo, 300, sem=7, op=95, w=3)
    tanque_agua(d, W - 520, suelo, 360, op=120, w=4)
    d.line([(0, suelo), (W, suelo)], fill=130, width=3)
    # autopista caída a la derecha
    d.line([(W - 380, suelo - 210), (W - 60, suelo - 210)], fill=110, width=5)
    d.line([(W - 60, suelo - 210), (W, suelo - 120)], fill=110, width=5)
    for px in (W - 340, W - 220, W - 100):
        d.line([(px, suelo - 210), (px, suelo)], fill=110, width=5)
    # torre con ondas a la izquierda del título, dentro de la zona segura
    tx = sx0 + 150
    ax, ay = torre(d, tx, sy1 - 14, 255, 140, w=5, op=235)
    ondas(d, ax, ay, [40, 72, 104], 5, op=235, abertura=38)
    # título
    f1 = fuente("AGENCYB.TTF", 230)
    texto_centrado(d, cx + 90, sy0 + 10, "RADIO YERMO", f1, 255, esp=10)
    f2 = fuente("consolab.ttf", 46)
    texto_centrado(d, cx + 90, sy0 + 262, "SECRETOS · HISTORIA · LOCURAS DE FALLOUT", f2, 220, esp=2)
    # dial del sintonizador
    dial(d, cx - 330, cx + 510, sy1 - 92, 82, aguja=0.62, op=200)
    f3 = fuente("consola.ttf", 30)
    d.text((sx1 - 20 - d.textlength("TRANSMITIENDO DESDE EL YERMO _", font=f3), sy0 - 70), "TRANSMITIENDO DESDE EL YERMO _",
           fill=150, font=f3)
    rgb = fosforo(np.array(mask), lineas=4, sem=3)
    guardar(rgb, "BANNER_2560x1440.jpg")
    # hoja de revisión con las zonas
    rev = Image.fromarray(rgb.copy())
    dr = ImageDraw.Draw(rev)
    dr.rectangle([sx0, sy0, sx1, sy1], outline=(255, 60, 60), width=4)              # todos los dispositivos
    dr.rectangle([(W - 2560) // 2, (H - 423) // 2, (W + 2560) // 2, (H + 423) // 2], outline=(255, 200, 0), width=3)  # escritorio
    rev.resize((1280, 720)).save(os.path.join(AQUI, "_banner_zona_segura.jpg"), quality=90)


# ------------------------------------------------------------------ logo
def logo():
    S = 800
    mask = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(mask)
    c = S // 2
    d.ellipse([22, 22, S - 22, S - 22], outline=255, width=12)
    d.ellipse([52, 52, S - 52, S - 52], outline=120, width=4)
    # marcas de dial en el anillo
    for i in range(60):
        a = math.radians(i * 6)
        r0, r1 = S / 2 - 62, S / 2 - (80 if i % 5 == 0 else 70)
        d.line([(c + r0 * math.cos(a), c + r0 * math.sin(a)), (c + r1 * math.cos(a), c + r1 * math.sin(a))], fill=150, width=3)
    # suelo con ruinas recortadas al círculo
    suelo = 560
    capa = Image.new("L", (S, S), 0)
    dc = ImageDraw.Draw(capa)
    ruinas(dc, 90, 710, suelo, 120, sem=11, op=110, w=4)
    dc.line([(90, suelo), (710, suelo)], fill=160, width=5)
    circ = Image.new("L", (S, S), 0)
    ImageDraw.Draw(circ).ellipse([96, 96, S - 96, S - 96], fill=255)
    mask.paste(capa, (0, 0), circ)
    ax, ay = torre(d, c, suelo - 10, 300, 160, w=9, op=255)
    ondas(d, ax, ay, [52, 94, 136], 11, op=255, abertura=40)
    # placa con el nombre: tapa las marcas del anillo y queda dentro del círculo interior
    d.rounded_rectangle([150, 572, S - 150, 690], radius=18, fill=0, outline=255, width=6)
    f = fuente("AGENCYB.TTF", 100)
    texto_centrado(d, c, 576, "RADIO YERMO", f, 255, esp=2)
    rgb = fosforo(np.array(mask), lineas=4, vig=0.4, grano=0.04, sem=5)
    guardar(rgb, "LOGO_800.jpg")
    Image.fromarray(rgb).resize((98, 98), Image.LANCZOS).resize((294, 294), Image.NEAREST).save(
        os.path.join(AQUI, "_logo_chico.jpg"), quality=90)


if __name__ == "__main__":
    banner()
    logo()
    print("listo:", AQUI)
