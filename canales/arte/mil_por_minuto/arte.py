# -*- coding: utf-8 -*-
"""Arte del canal «Mil por Minuto» (19-nov-2026): cómo se fabrican las cosas que compras, a escala de fábrica.
Identidad = planta industrial: acero oscuro + naranja de seguridad + franjas de peligro + cuadrícula de plano de ingeniería,
y una banda transportadora con productos IDÉNTICOS en serie (la idea del canal: lo mismo, millones de veces, sin parar).
Todo por código (sin marcas ni logos de empresas):
  BANNER_2560x1440.jpg  (zona visible en todos los dispositivos = 1546x423 al centro; el texto va dentro)
  LOGO_800.jpg
  _banner_zona_segura.jpg  y  _logo_chico.jpg  (para revisar)
python canales/arte/mil_por_minuto/arte.py
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F = "C:/Windows/Fonts/"
FONDO = (15, 18, 22)
ACERO = (44, 51, 60)
ACERO_CLARO = (120, 132, 146)
NARANJA = (255, 106, 26)
AMARILLO = (255, 196, 0)
BLANCO = (242, 242, 236)
CIAN = (64, 160, 210)
SS = 2   # supermuestreo


def bahn(tam, var="Bold Condensed"):
    f = ImageFont.truetype(F + "bahnschrift.ttf", tam)
    try:
        f.set_variation_by_name(var)
    except Exception:
        pass
    return f


def fondo_plano(w, h, paso=40):
    """Acero oscuro con viñeta + cuadrícula de plano de ingeniería (fina y gruesa)."""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    luz = np.clip(1.15 - 0.55 * r, 0.45, 1.15)[..., None]
    base = np.array(FONDO, np.float32)[None, None] * luz + np.array([4, 6, 9], np.float32)
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for i in range(0, w, paso):
        d.line([(i, 0), (i, h)], fill=CIAN + (60 if i % (paso * 5) == 0 else 22,), width=SS)
    for j in range(0, h, paso):
        d.line([(0, j), (w, j)], fill=CIAN + (60 if j % (paso * 5) == 0 else 22,), width=SS)
    return Image.alpha_composite(im, capa)


def franjas(d, x0, y0, x1, y1, ancho=46):
    """Franja de peligro amarilla/negra en diagonal."""
    d.rectangle([x0, y0, x1, y1], fill=(20, 20, 20))
    h = y1 - y0
    k = x0 - h
    while k < x1:
        d.polygon([(k, y1), (k + ancho, y1), (k + ancho + h, y0), (k + h, y0)], fill=AMARILLO)
        k += ancho * 2


def engrane(d, cx, cy, r_ext, r_int, r_hueco, dientes, color, fondo, giro=0.0):
    pts = []
    n = dientes * 4
    for i in range(n):
        a = giro + 2 * math.pi * i / n
        rr = r_ext if (i % 4) in (1, 2) else r_int
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r_int + 4, cy - r_int + 4, cx + r_int - 4, cy + r_int - 4], fill=color)
    d.ellipse([cx - r_hueco, cy - r_hueco, cx + r_hueco, cy + r_hueco], fill=fondo)


# ------------------------------------------------------------------ productos en serie (siluetas genéricas, sin marca)
def caja(d, x, base, s, col, borde):
    d.rectangle([x, base - 0.8 * s, x + s, base], fill=col, outline=borde, width=2 * SS)
    d.line([(x + s / 2, base - 0.8 * s), (x + s / 2, base - 0.55 * s)], fill=borde, width=2 * SS)


def lata(d, x, base, s, col, borde):
    w = 0.55 * s
    d.rounded_rectangle([x, base - s, x + w, base], radius=int(0.08 * s), fill=col, outline=borde, width=2 * SS)
    d.line([(x, base - 0.82 * s), (x + w, base - 0.82 * s)], fill=borde, width=2 * SS)
    d.line([(x, base - 0.18 * s), (x + w, base - 0.18 * s)], fill=borde, width=2 * SS)


def botella(d, x, base, s, col, borde):
    w = 0.42 * s
    cx = x + w / 2
    d.rounded_rectangle([x, base - 0.68 * s, x + w, base], radius=int(0.1 * s), fill=col, outline=borde, width=2 * SS)
    d.polygon([(x + 0.06 * s, base - 0.66 * s), (cx - 0.07 * s, base - 0.9 * s), (cx + 0.07 * s, base - 0.9 * s),
               (x + w - 0.06 * s, base - 0.66 * s)], fill=col, outline=borde)
    d.rectangle([cx - 0.07 * s, base - 1.0 * s, cx + 0.07 * s, base - 0.9 * s], fill=borde)


def vaso(d, x, base, s, col, borde):
    d.polygon([(x, base - 0.85 * s), (x + 0.7 * s, base - 0.85 * s), (x + 0.6 * s, base), (x + 0.1 * s, base)],
              fill=col, outline=borde)
    d.rectangle([x - 0.03 * s, base - 0.92 * s, x + 0.73 * s, base - 0.85 * s], fill=borde)


PRODUCTOS = (caja, lata, botella, vaso)


def banda(d, x0, x1, y, alto, paso, rodillo):
    """Banda transportadora: cinta con marcas de avance, rodillos y patas."""
    d.rectangle([x0, y, x1, y + alto], fill=(30, 34, 40), outline=ACERO_CLARO, width=2 * SS)
    for k in range(int(x0), int(x1), paso // 2):
        d.line([(k, y + 3 * SS), (k + paso // 6, y + alto - 3 * SS)], fill=(58, 64, 74), width=2 * SS)
    for k in range(int(x0) + rodillo, int(x1), rodillo * 3):
        cy = y + alto + rodillo * 0.9
        d.ellipse([k - rodillo, cy - rodillo, k + rodillo, cy + rodillo], fill=ACERO, outline=ACERO_CLARO, width=2 * SS)
        d.ellipse([k - rodillo * 0.3, cy - rodillo * 0.3, k + rodillo * 0.3, cy + rodillo * 0.3], fill=ACERO_CLARO)


def lineas_velocidad(d, x0, x1, y0, y1, n, col):
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 0.5) / n
        largo = (x1 - x0) * (0.45 + 0.55 * ((i * 37) % 11) / 10)
        d.line([(x1 - largo, y), (x1, y)], fill=col, width=3 * SS)


def guardar(im, nombre, q=95):
    ruta = os.path.join(AQUI, nombre)
    im.convert("RGB").save(ruta, quality=q)
    print("ok", ruta)


# ------------------------------------------------------------------ banner
def banner():
    W, H = 2560 * SS, 1440 * SS
    sw, sh = 1546 * SS, 423 * SS
    sx0, sy0 = (W - sw) // 2, (H - sh) // 2
    sx1, sy1 = sx0 + sw, sy0 + sh
    im = fondo_plano(W, H, paso=40 * SS)
    d = ImageDraw.Draw(im)
    # franjas de peligro arriba y abajo de la franja de escritorio (2560x423)
    franjas(d, 0, sy0 + 10 * SS, W, sy0 + 34 * SS, ancho=40 * SS)
    franjas(d, 0, sy1 - 34 * SS, W, sy1 - 10 * SS, ancho=40 * SS)
    # banda transportadora a todo lo ancho con productos idénticos en serie; uno resaltado en naranja
    yb = sy1 - 84 * SS
    banda(d, -20, W + 20, yb, 16 * SS, 70 * SS, 10 * SS)
    s = 46 * SS
    paso = 96 * SS
    tipo = 0
    x = 30 * SS
    k = 0
    while x < W:
        f = PRODUCTOS[(k // 6) % 4]
        destacado = abs((x + s / 2) - (sx0 + sw * 0.86)) < paso / 2
        f(d, x, yb, s, NARANJA if destacado else (72, 80, 92), (20, 23, 28) if destacado else ACERO_CLARO)
        x += paso
        k += 1
    # brazo robótico/engrane a la izquierda del título, dentro de la zona segura
    gx, gy = sx0 + 140 * SS, sy0 + 150 * SS
    engrane(d, gx, gy, 96 * SS, 79 * SS, 38 * SS, 12, NARANJA, FONDO, giro=0.13)
    engrane(d, gx + 112 * SS, gy - 62 * SS, 50 * SS, 40 * SS, 17 * SS, 9, ACERO_CLARO, FONDO, giro=0.3)
    # título
    ft = bahn(164 * SS)
    tx = sx0 + 272 * SS
    ty = sy0 + 44 * SS
    d.text((tx, ty), "MIL", font=ft, fill=NARANJA)
    wmil = d.textlength("MIL ", font=ft)
    d.text((tx + wmil, ty), "POR MINUTO", font=ft, fill=BLANCO)
    fs = bahn(50 * SS, "SemiBold Condensed")
    d.text((tx + 6 * SS, ty + 172 * SS), "ASÍ SE FABRICA LO QUE COMPRAS", font=fs, fill=(196, 204, 214))
    # contador de producción a la derecha (pantalla de planta)
    fc = bahn(46 * SS)
    cx0, cy0 = sx1 - 330 * SS, ty + 170 * SS
    d.rounded_rectangle([cx0, cy0, cx0 + 300 * SS, cy0 + 66 * SS], radius=10 * SS, fill=(8, 10, 12), outline=NARANJA, width=3 * SS)
    d.text((cx0 + 22 * SS, cy0 + 6 * SS), "1 000 / MIN", font=fc, fill=AMARILLO)
    d.ellipse([cx0 + 266 * SS, cy0 + 24 * SS, cx0 + 284 * SS, cy0 + 42 * SS], fill=(230, 50, 40))
    im = im.resize((2560, 1440), Image.LANCZOS)
    guardar(im, "BANNER_2560x1440.jpg")
    rev = im.convert("RGB").copy()
    dr = ImageDraw.Draw(rev)
    dr.rectangle([(2560 - 1546) // 2, (1440 - 423) // 2, (2560 + 1546) // 2, (1440 + 423) // 2], outline=(0, 255, 0), width=4)
    rev.resize((1280, 720)).save(os.path.join(AQUI, "_banner_zona_segura.jpg"), quality=90)


# ------------------------------------------------------------------ logo
def logo():
    W = 800 * SS
    im = fondo_plano(W, W, paso=50 * SS)
    d = ImageDraw.Draw(im)
    c = W / 2
    engrane(d, c, c, 372 * SS, 322 * SS, 262 * SS, 14, NARANJA, (17, 20, 25), giro=0.0)
    # anillo fino de acero dentro del hueco
    d.ellipse([c - 248 * SS, c - 248 * SS, c + 248 * SS, c + 248 * SS], outline=ACERO_CLARO, width=4 * SS)
    # líneas de velocidad a la izquierda del número
    lineas_velocidad(d, c - 236 * SS, c - 150 * SS, c - 92 * SS, c + 40 * SS, 4, NARANJA)
    f = bahn(238 * SS)
    t = "1000"
    bb = d.textbbox((0, 0), t, font=f)
    d.text((c - (bb[2] + bb[0]) / 2 + 28 * SS, c - 168 * SS), t, font=f, fill=BLANCO)
    f2 = bahn(66 * SS)
    t2 = "POR MINUTO"
    bb2 = d.textbbox((0, 0), t2, font=f2)
    d.text((c - (bb2[2] + bb2[0]) / 2, c + 92 * SS), t2, font=f2, fill=NARANJA)
    im = im.resize((800, 800), Image.LANCZOS)
    guardar(im, "LOGO_800.jpg")
    # vista previa: recorte circular a 98 px como en YouTube
    chico = im.resize((98, 98), Image.LANCZOS)
    m = Image.new("L", (98, 98), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 97, 97], fill=255)
    lienzo = Image.new("RGB", (98, 98), (255, 255, 255))
    lienzo.paste(chico, (0, 0), m)
    lienzo.resize((294, 294), Image.NEAREST).save(os.path.join(AQUI, "_logo_chico.jpg"), quality=92)


if __name__ == "__main__":
    banner()
    logo()
