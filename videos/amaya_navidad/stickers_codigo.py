# -*- coding: utf-8 -*-
"""Stickers dibujados por código para lo que la voz nombra y Flow no trae (aguacate, fresa, martillo, celular, jabón…).
Mismo lenguaje que los de Flow: relleno pastel, sombreado suave, contorno café; el contorno blanco lo pone coquette.sticker.
python dibujos.py → stickers/<nombre>.png (no pisa los que ya existen salvo con --todo)."""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "stickers")
K = 2                     # supermuestreo
L = (96, 62, 64, 255)     # contorno café
LW = 7 * K


def lienzo(w, h):
    im = Image.new("RGBA", (w * K, h * K), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def S(v):
    if isinstance(v, (list, tuple)):
        return [S(x) if isinstance(x, (list, tuple)) else x * K for x in v]
    return v * K


def cara(d, cx, cy, r, ojos=0.55):
    """Carita kawaii: ojos, cachetes, boquita."""
    for s in (-1, 1):
        x = cx + s * r * ojos
        d.ellipse(S((x - r * 0.12, cy - r * 0.16, x + r * 0.12, cy + r * 0.16)), fill=(60, 36, 40, 255))
        d.ellipse(S((x - r * 0.05 + r * 0.04, cy - r * 0.1, x + r * 0.03 + r * 0.04, cy - r * 0.02)), fill=(255, 255, 255, 255))
        d.ellipse(S((x + s * r * 0.12 - r * 0.2, cy + r * 0.18, x + s * r * 0.12 + r * 0.2, cy + r * 0.36)), fill=(245, 140, 160, 170))
    d.arc(S((cx - r * 0.16, cy + r * 0.05, cx + r * 0.16, cy + r * 0.3)), 20, 160, fill=(60, 36, 40, 255), width=S(5))


def guardar(im, nombre):
    im = im.resize((im.width // K, im.height // K), Image.LANCZOS)
    im.save(os.path.join(OUT, nombre + ".png"))
    print("ok", nombre, im.size)


def aguacate():
    im, d = lienzo(460, 600)
    d.ellipse(S((40, 170, 420, 580)), fill=(92, 140, 70, 255), outline=L, width=LW)
    d.ellipse(S((110, 40, 350, 330)), fill=(92, 140, 70, 255), outline=L, width=LW)
    d.rectangle(S((118, 170, 342, 330)), fill=(92, 140, 70, 255))
    d.ellipse(S((75, 200, 385, 550)), fill=(214, 232, 150, 255))
    d.ellipse(S((140, 80, 320, 300)), fill=(214, 232, 150, 255))
    d.rectangle(S((146, 200, 314, 300)), fill=(214, 232, 150, 255))
    d.ellipse(S((160, 330, 300, 480)), fill=(150, 96, 62, 255), outline=L, width=LW)
    d.ellipse(S((185, 350, 225, 395)), fill=(200, 150, 110, 255))
    cara(d, 230, 240, 80)
    guardar(im, "aguacate")


def fresa():
    im, d = lienzo(460, 560)
    pts = [(230 + 200 * math.sin(a) * (1 - 0.35 * (math.cos(a) + 1) / 2 * 0), 0) for a in [0]]
    poly = []
    for i in range(60):
        a = 2 * math.pi * i / 60
        x = math.sin(a)
        y = math.cos(a)
        r = 1 - 0.45 * max(0, -y)       # punta abajo
        poly.append((230 + 200 * x * r, 300 - 190 * y * (1.0 if y > 0 else 1.25)))
    d.polygon(S(poly), fill=(232, 72, 92, 255), outline=L)
    d.line(S(poly + [poly[0]]), fill=L, width=LW)
    for (x, y) in [(150, 230), (310, 230), (230, 200), (120, 320), (340, 320), (190, 400), (270, 400), (230, 470), (170, 300),
                   (290, 300)]:
        d.ellipse(S((x - 9, y - 13, x + 9, y + 13)), fill=(255, 226, 140, 255))
    for k in range(5):
        a = math.radians(-160 + k * 35)
        d.polygon(S([(230, 120), (230 + 150 * math.cos(a) - 30, 120 + 70 * math.sin(a)), (230 + 150 * math.cos(a) + 30,
                                                                                            120 + 70 * math.sin(a) + 20)]),
                  fill=(96, 160, 80, 255), outline=L)
    d.rectangle(S((220, 40, 240, 120)), fill=(96, 160, 80, 255), outline=L, width=S(4))
    cara(d, 230, 300, 85)
    guardar(im, "fresa")


def martillo():
    im, d = lienzo(520, 560)
    d.rounded_rectangle(S((225, 150, 295, 540)), radius=S(30), fill=(214, 164, 112, 255), outline=L, width=LW)
    d.line(S((245, 200, 245, 500)), fill=(236, 196, 150, 255), width=S(10))
    d.rounded_rectangle(S((60, 50, 470, 190)), radius=S(26), fill=(186, 190, 200, 255), outline=L, width=LW)
    d.rectangle(S((80, 70, 450, 100)), fill=(226, 230, 236, 255))
    guardar(im, "martillo")


def celular():
    im, d = lienzo(320, 580)
    d.rounded_rectangle(S((20, 20, 300, 560)), radius=S(50), fill=(246, 170, 196, 255), outline=L, width=LW)
    d.rounded_rectangle(S((44, 60, 276, 520)), radius=S(30), fill=(255, 244, 248, 255), outline=L, width=S(4))
    d.rounded_rectangle(S((120, 34, 200, 48)), radius=S(7), fill=L)
    d.ellipse(S((90, 300, 160, 360)), fill=(217, 79, 134, 255))
    d.ellipse(S((170, 270, 240, 330)), fill=(217, 79, 134, 255))
    d.rectangle(S((146, 160, 160, 330)), fill=(217, 79, 134, 255))
    d.rectangle(S((226, 130, 240, 300)), fill=(217, 79, 134, 255))
    d.polygon(S([(146, 160), (240, 130), (240, 175), (146, 205)]), fill=(217, 79, 134, 255))
    d.rounded_rectangle(S((80, 420, 240, 440)), radius=S(10), fill=(240, 200, 214, 255))
    d.rounded_rectangle(S((80, 420, 180, 440)), radius=S(10), fill=(217, 79, 134, 255))
    guardar(im, "celular")


def jabon():
    im, d = lienzo(520, 420)
    for (x, y, r) in [(120, 90, 60), (210, 60, 44), (300, 95, 34), (380, 70, 26)]:
        d.ellipse(S((x - r, y - r + 80, x + r, y + r + 80)), fill=(236, 246, 255, 230), outline=(150, 180, 210, 255), width=S(4))
    d.rounded_rectangle(S((40, 170, 480, 400)), radius=S(70), fill=(248, 190, 210, 255), outline=L, width=LW)
    d.rounded_rectangle(S((90, 200, 430, 250)), radius=S(25), fill=(255, 220, 232, 255))
    guardar(im, "jabon")


def esponja():
    im, d = lienzo(500, 380)
    d.rounded_rectangle(S((30, 30, 470, 350)), radius=S(60), fill=(250, 214, 110, 255), outline=L, width=LW)
    d.rounded_rectangle(S((30, 30, 470, 120)), radius=S(40), fill=(118, 190, 120, 255), outline=L, width=LW)
    for (x, y, r) in [(110, 190, 26), (210, 240, 18), (320, 180, 30), (400, 270, 20), (150, 290, 16), (270, 300, 22)]:
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=(222, 176, 70, 255))
    guardar(im, "esponja")


def gel():
    im, d = lienzo(320, 600)
    d.rectangle(S((130, 30, 190, 130)), fill=(240, 236, 228, 255), outline=L, width=S(5))
    d.rounded_rectangle(S((100, 20, 260, 60)), radius=S(14), fill=(240, 236, 228, 255), outline=L, width=S(5))
    d.rounded_rectangle(S((40, 120, 280, 580)), radius=S(50), fill=(196, 226, 190, 255), outline=L, width=LW)
    d.rounded_rectangle(S((70, 260, 250, 450)), radius=S(20), fill=(255, 252, 244, 255), outline=L, width=S(4))
    d.ellipse(S((125, 300, 195, 370)), fill=(190, 170, 220, 255))
    guardar(im, "gel")


def bloqueador():
    im, d = lienzo(300, 600)
    d.polygon(S([(40, 40), (260, 40), (240, 470), (60, 470)]), fill=(255, 238, 170, 255), outline=L)
    d.line(S([(40, 40), (260, 40), (240, 470), (60, 470), (40, 40)]), fill=L, width=LW)
    d.rounded_rectangle(S((80, 460, 220, 580)), radius=S(20), fill=(250, 150, 110, 255), outline=L, width=LW)
    d.ellipse(S((90, 120, 210, 240)), fill=(252, 186, 90, 255))
    from coquette import fuente
    f = fuente("Poppins-ExtraBold.ttf", 52 * K)
    d.text(S((70, 280)), "SPF", font=f, fill=(150, 80, 60, 255))
    d.text(S((90, 350)), "50", font=f, fill=(150, 80, 60, 255))
    guardar(im, "bloqueador")


def dados():
    im, d = lienzo(560, 440)
    for (x0, y0, n, col) in [(30, 120, 5, (255, 255, 255, 255)), (260, 40, 3, (250, 210, 226, 255))]:
        d.rounded_rectangle(S((x0, y0, x0 + 270, y0 + 270)), radius=S(50), fill=col, outline=L, width=LW)
        pos = {5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)], 3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)]}[n]
        for (u, v) in pos:
            cx, cy = x0 + 270 * u, y0 + 270 * v
            d.ellipse(S((cx - 24, cy - 24, cx + 24, cy + 24)), fill=(217, 79, 134, 255) if n == 3 else (80, 50, 56, 255))
    guardar(im, "dados")


def pulsera(nombre="pulsera", cols=((246, 160, 190), (255, 230, 150), (170, 210, 245), (200, 170, 230), (255, 255, 255))):
    im, d = lienzo(460, 460)
    d.ellipse(S((70, 70, 390, 390)), outline=(210, 200, 200, 255), width=S(6))
    n = 18
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = 230 + 160 * math.cos(a), 230 + 160 * math.sin(a)
        r = 34 if i % 6 else 44
        c = cols[i % len(cols)] + (255,)
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=c, outline=L, width=S(5))
        d.ellipse(S((x - r * 0.45, y - r * 0.55, x - r * 0.05, y - r * 0.15)), fill=(255, 255, 255, 200))
    guardar(im, nombre)


def nube():
    im, d = lienzo(620, 380)
    blobs = [(170, 230, 120), (300, 170, 150), (450, 230, 120), (310, 280, 120), (110, 290, 80), (520, 290, 80)]
    for (x, y, r) in blobs:
        d.ellipse(S((x - r - 6, y - r - 6, x + r + 6, y + r + 6)), fill=L)
    for (x, y, r) in blobs:
        d.ellipse(S((x - r, y - r, x + r, y + r)), fill=(255, 255, 255, 255))
    d.ellipse(S((210, 140, 280, 190)), fill=(255, 255, 255, 255))
    cara(d, 310, 240, 80)
    guardar(im, "nube")


def copo():
    im, d = lienzo(420, 420)
    for k in range(6):
        a = math.radians(k * 60)
        x1, y1 = 210 + 180 * math.cos(a), 210 + 180 * math.sin(a)
        d.line(S((210, 210, x1, y1)), fill=(150, 196, 236, 255), width=S(26))
        for f in (0.5, 0.75):
            xm, ym = 210 + 180 * f * math.cos(a), 210 + 180 * f * math.sin(a)
            for s in (-1, 1):
                b = a + s * math.radians(45)
                d.line(S((xm, ym, xm + 55 * math.cos(b), ym + 55 * math.sin(b))), fill=(150, 196, 236, 255), width=S(18))
    d.ellipse(S((170, 170, 250, 250)), fill=(200, 226, 250, 255))
    guardar(im, "copo")


def nota_musical():
    im, d = lienzo(380, 480)
    c = (217, 79, 134, 255)
    d.ellipse(S((30, 340, 150, 440)), fill=c, outline=L, width=S(5))
    d.ellipse(S((220, 290, 340, 390)), fill=c, outline=L, width=S(5))
    d.rectangle(S((128, 80, 150, 390)), fill=c)
    d.rectangle(S((318, 40, 340, 340)), fill=c)
    d.polygon(S([(128, 80), (340, 40), (340, 110), (128, 150)]), fill=c)
    guardar(im, "nota_musical")


def bateria(nombre, nivel, col):
    im, d = lienzo(520, 280)
    d.rounded_rectangle(S((20, 30, 450, 250)), radius=S(40), fill=(255, 255, 255, 255), outline=L, width=LW)
    d.rounded_rectangle(S((452, 100, 500, 180)), radius=S(14), fill=L)
    if nivel > 0:
        d.rounded_rectangle(S((50, 60, 50 + 370 * nivel, 220)), radius=S(24), fill=col)
    guardar(im, nombre)


def lata():
    im, d = lienzo(360, 500)
    d.rectangle(S((40, 80, 320, 420)), fill=(196, 200, 208, 255))
    d.ellipse(S((40, 360, 320, 470)), fill=(176, 180, 190, 255), outline=L, width=LW)
    d.rectangle(S((40, 80, 320, 415)), fill=(196, 200, 208, 255))
    d.line(S((40, 80, 40, 415)), fill=L, width=LW)
    d.line(S((320, 80, 320, 415)), fill=L, width=LW)
    for y in (160, 240, 320):
        d.line(S((44, y, 316, y)), fill=(160, 164, 176, 255), width=S(6))
    d.ellipse(S((40, 30, 320, 140)), fill=(220, 224, 230, 255), outline=L, width=LW)
    d.ellipse(S((70, 50, 290, 120)), fill=(186, 190, 200, 255))
    guardar(im, "lata")


def claqueta():
    im, d = lienzo(560, 480)
    d.rounded_rectangle(S((40, 170, 520, 450)), radius=S(20), fill=(60, 52, 60, 255), outline=L, width=LW)
    d.polygon(S([(40, 170), (500, 70), (520, 140), (60, 240)]), fill=(255, 255, 255, 255), outline=L)
    for k in range(5):
        x = 80 + k * 90
        d.polygon(S([(x, 160 - k * 20), (x + 45, 150 - k * 20), (x + 60, 215 - k * 20), (x + 15, 225 - k * 20)]), fill=(60, 52, 60, 255))
    d.line(S((70, 300, 490, 300)), fill=(255, 255, 255, 255), width=S(5))
    d.line(S((280, 300, 280, 430)), fill=(255, 255, 255, 255), width=S(5))
    guardar(im, "claqueta")


def tienda():
    im, d = lienzo(620, 460)
    d.polygon(S([(310, 30), (590, 430), (30, 430)]), fill=(120, 186, 140, 255), outline=L)
    d.line(S([(310, 30), (590, 430), (30, 430), (310, 30)]), fill=L, width=LW)
    d.polygon(S([(310, 140), (400, 430), (220, 430)]), fill=(60, 110, 80, 255))
    d.line(S((310, 30, 310, 430)), fill=L, width=S(4))
    guardar(im, "tienda")


def burbuja():
    im, d = lienzo(560, 380)
    d.rounded_rectangle(S((20, 20, 540, 300)), radius=S(60), fill=(255, 255, 255, 255), outline=L, width=LW)
    d.polygon(S([(120, 290), (100, 370), (200, 295)]), fill=(255, 255, 255, 255), outline=L)
    d.line(S([(120, 296), (100, 370), (200, 296)]), fill=L, width=LW)
    for k in range(3):
        d.ellipse(S((170 + k * 90, 130, 220 + k * 90, 180)), fill=(217, 79, 134, 255))
    guardar(im, "burbuja")


def pulgar():
    im, d = lienzo(460, 460)
    d.ellipse(S((20, 20, 440, 440)), fill=(217, 79, 134, 255), outline=L, width=LW)
    w = (255, 255, 255, 255)
    d.rounded_rectangle(S((120, 210, 190, 350)), radius=S(14), fill=w)
    d.rounded_rectangle(S((200, 200, 340, 350)), radius=S(30), fill=w)
    d.polygon(S([(200, 215), (250, 100), (290, 120), (275, 205)]), fill=w)
    guardar(im, "pulgar")


def kit():
    im, d = lienzo(600, 460)
    d.rounded_rectangle(S((30, 110, 570, 440)), radius=S(70), fill=(248, 180, 204, 255), outline=L, width=LW)
    d.rounded_rectangle(S((30, 110, 570, 190)), radius=S(40), fill=(236, 150, 182, 255), outline=L, width=LW)
    d.line(S((60, 150, 540, 150)), fill=(255, 240, 246, 255), width=S(6))
    d.ellipse(S((270, 30, 330, 130)), outline=L, width=S(8))
    d.rounded_rectangle(S((240, 240, 360, 360)), radius=S(16), fill=(255, 255, 255, 255))
    d.rectangle(S((285, 255, 315, 345)), fill=(230, 70, 90, 255))
    d.rectangle(S((255, 285, 345, 315)), fill=(230, 70, 90, 255))
    guardar(im, "kit")


def cepillo():
    im, d = lienzo(300, 620)
    d.rounded_rectangle(S((115, 330, 185, 600)), radius=S(30), fill=(246, 170, 196, 255), outline=L, width=LW)
    d.ellipse(S((30, 20, 270, 360)), fill=(246, 170, 196, 255), outline=L, width=LW)
    d.ellipse(S((60, 50, 240, 330)), fill=(255, 236, 242, 255))
    for i in range(5):
        for j in range(7):
            x, y = 90 + i * 30, 85 + j * 35
            if ((x - 150) / 90) ** 2 + ((y - 190) / 140) ** 2 < 1:
                d.ellipse(S((x - 7, y - 7, x + 7, y + 7)), fill=(120, 80, 90, 255))
    guardar(im, "cepillo")


def aceite():
    im, d = lienzo(280, 600)
    d.rounded_rectangle(S((100, 20, 180, 140)), radius=S(14), fill=(60, 52, 60, 255), outline=L, width=S(5))
    d.rounded_rectangle(S((40, 130, 240, 580)), radius=S(60), fill=(250, 210, 120, 230), outline=L, width=LW)
    d.rounded_rectangle(S((70, 280, 210, 440)), radius=S(18), fill=(255, 252, 244, 255), outline=L, width=S(4))
    d.ellipse(S((120, 310, 160, 370)), fill=(250, 180, 70, 255))
    d.polygon(S([(140, 295), (122, 340), (158, 340)]), fill=(250, 180, 70, 255))
    guardar(im, "aceite")


def tubo(nombre="crema_peinar", col=(200, 170, 236, 255), tapa=(255, 255, 255, 255)):
    im, d = lienzo(280, 600)
    d.polygon(S([(30, 30), (250, 30), (220, 460), (60, 460)]), fill=col, outline=L)
    d.line(S([(30, 30), (250, 30), (220, 460), (60, 460), (30, 30)]), fill=L, width=LW)
    d.rounded_rectangle(S((80, 450, 200, 580)), radius=S(20), fill=tapa, outline=L, width=LW)
    d.rounded_rectangle(S((70, 150, 210, 300)), radius=S(16), fill=(255, 255, 255, 230))
    for k in range(3):
        d.arc(S((95, 180 + k * 28, 185, 230 + k * 28)), 200, 340, fill=(150, 110, 190, 255), width=S(5))
    guardar(im, nombre)


def tinte():
    im, d = lienzo(460, 560)
    d.rounded_rectangle(S((30, 120, 300, 540)), radius=S(24), fill=(255, 255, 255, 255), outline=L, width=LW)
    for k, c in enumerate([(240, 100, 170), (150, 110, 230), (90, 170, 240), (110, 210, 160)]):
        d.rectangle(S((50, 150 + k * 55, 280, 200 + k * 55)), fill=c + (255,))
    d.rounded_rectangle(S((290, 200, 430, 540)), radius=S(40), fill=(240, 100, 170, 255), outline=L, width=LW)
    d.rounded_rectangle(S((320, 90, 400, 210)), radius=S(14), fill=(60, 52, 60, 255), outline=L, width=S(5))
    d.ellipse(S((330, 330, 390, 400)), fill=(255, 230, 245, 255))
    guardar(im, "tinte")


def gises():
    im, d = lienzo(560, 380)
    cols = [(255, 160, 190), (170, 210, 245), (255, 230, 150), (200, 170, 236), (170, 225, 190)]
    for k, c in enumerate(cols):
        x = 40 + k * 100
        d.rounded_rectangle(S((x, 60 + (k % 2) * 30, x + 80, 330 + (k % 2) * 30)), radius=S(30), fill=c + (255,), outline=L, width=S(6))
        d.rounded_rectangle(S((x + 10, 200 + (k % 2) * 30, x + 70, 250 + (k % 2) * 30)), radius=S(8), fill=(255, 255, 255, 220))
    guardar(im, "gises")


def mochila():
    im, d = lienzo(480, 600)
    d.arc(S((150, 10, 330, 170)), 180, 360, fill=L, width=S(16))
    d.rounded_rectangle(S((40, 80, 440, 580)), radius=S(110), fill=(170, 206, 240, 255), outline=L, width=LW)
    d.rounded_rectangle(S((100, 330, 380, 540)), radius=S(50), fill=(150, 186, 226, 255), outline=L, width=LW)
    d.line(S((120, 380, 360, 380)), fill=L, width=S(5))
    d.ellipse(S((170, 150, 310, 290)), fill=(255, 210, 226, 255), outline=L, width=S(5))
    d.polygon(S([(240, 175), (258, 212), (298, 216), (268, 242), (276, 282), (240, 262), (204, 282), (212, 242), (182, 216),
                 (222, 212)]), fill=(255, 235, 150, 255))
    guardar(im, "mochila")


def curita():
    im, d = lienzo(520, 220)
    d.rounded_rectangle(S((20, 30, 500, 190)), radius=S(80), fill=(240, 196, 160, 255), outline=L, width=LW)
    d.rounded_rectangle(S((180, 50, 340, 170)), radius=S(20), fill=(250, 224, 200, 255))
    for i in range(4):
        for j in range(2):
            d.ellipse(S((210 + i * 32, 80 + j * 45, 222 + i * 32, 92 + j * 45)), fill=(220, 170, 140, 255))
    guardar(im, "curita")


def desodorante():
    im, d = lienzo(240, 560)
    d.rounded_rectangle(S((40, 20, 200, 160)), radius=S(30), fill=(255, 255, 255, 255), outline=L, width=LW)
    d.rounded_rectangle(S((30, 150, 210, 540)), radius=S(40), fill=(176, 220, 240, 255), outline=L, width=LW)
    d.rounded_rectangle(S((60, 260, 180, 420)), radius=S(16), fill=(255, 255, 255, 230))
    d.ellipse(S((95, 300, 145, 350)), fill=(120, 180, 220, 255))
    guardar(im, "desodorante")


def toallitas():
    im, d = lienzo(520, 360)
    d.rounded_rectangle(S((20, 80, 500, 340)), radius=S(50), fill=(200, 236, 214, 255), outline=L, width=LW)
    d.rounded_rectangle(S((150, 100, 370, 180)), radius=S(30), fill=(150, 206, 176, 255), outline=L, width=S(5))
    d.polygon(S([(200, 120), (260, 20), (330, 110)]), fill=(255, 255, 255, 255), outline=L)
    d.line(S([(200, 120), (260, 20), (330, 110)]), fill=L, width=S(5))
    guardar(im, "toallitas")


def sol():
    im, d = lienzo(460, 460)
    for k in range(12):
        a = math.radians(k * 30)
        d.polygon(S([(230 + 130 * math.cos(a - 0.15), 230 + 130 * math.sin(a - 0.15)), (230 + 215 * math.cos(a), 230 + 215 * math.sin(a)),
                     (230 + 130 * math.cos(a + 0.15), 230 + 130 * math.sin(a + 0.15))]), fill=(252, 196, 80, 255), outline=L)
    d.ellipse(S((95, 95, 365, 365)), fill=(255, 222, 110, 255), outline=L, width=LW)
    cara(d, 230, 230, 90)
    guardar(im, "sol")


NUEVOS = [kit, cepillo, aceite, tubo, tinte, gises, mochila, curita, desodorante, toallitas, sol]

TODOS = [aguacate, fresa, martillo, celular, jabon, esponja, gel, bloqueador, dados, pulsera, nube, copo, nota_musical,
         lambda: bateria("bateria_llena", 1.0, (110, 200, 120, 255)), lambda: bateria("bateria_vacia", 0.12, (230, 70, 80, 255)),
         lata, claqueta, tienda, burbuja, pulgar,
         lambda: pulsera("pulsera_b", ((255, 255, 255), (246, 160, 190), (217, 79, 134))),
         lambda: pulsera("pulsera_c", ((170, 210, 245), (255, 255, 255), (255, 230, 150), (200, 236, 200)))]

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
    for f in TODOS:
        f()
