# -*- coding: utf-8 -*-
"""Texturas nuevas de 64 px a 15 bits (estilo PS1) para campana_dc_topes: empedrado, tope amarillo/negro, banqueta, fachadas
de Juchipila (rosa, amarillo, blanco, terracota), letrero «TORTILLERÍA», cantera de la parroquia y la cara ROJA de coraje
(cada gesto de tex/cara2_*.png teñido). Las de Daniel ya están copiadas de campana_dc_lowpoly/tex."""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "tex")
rng = np.random.default_rng(11)
FONT = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Windows", "Fonts", "Montserrat-Black.ttf")


def q15(im):
    a = np.asarray(im.convert("RGB"), np.int32)
    return Image.fromarray(((a >> 3) << 3).astype(np.uint8))


def ruido(base, amp, w=64, h=64):
    a = np.array(base, np.float32)[None, None, :] + rng.normal(0, amp, (h, w, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def empedrado():
    im = Image.new("RGB", (64, 64), (70, 62, 56)); d = ImageDraw.Draw(im)
    for fila in range(8):
        y = fila * 8
        off = (fila % 2) * 5
        x = -off
        while x < 64:
            w = int(rng.integers(7, 12))
            g = rng.normal(0, 16); c = tuple(int(v) for v in np.clip(np.array([128, 118, 106]) + g + rng.normal(0, 3, 3), 60, 200))
            d.rounded_rectangle((x + 1, y + 1, x + w - 1, y + 7), radius=2, fill=c)
            x += w
    return im


def tope():
    im = Image.new("RGB", (64, 16), (250, 204, 20)); d = ImageDraw.Draw(im)
    for k in range(-16, 64, 16):
        d.polygon([(k, 16), (k + 8, 16), (k + 16, 0), (k + 8, 0)], fill=(24, 22, 20))
    a = np.asarray(im, np.float32) + rng.normal(0, 7, (16, 64, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def letrero():
    im = Image.new("RGB", (128, 32), (250, 240, 220)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 127, 31), outline=(160, 30, 30), width=3)
    d.fontmode = "1"
    f = ImageFont.truetype(FONT, 15)
    w = d.textlength("TORTILLERÍA", font=f)
    d.text(((128 - w) / 2, 6), "TORTILLERÍA", font=f, fill=(170, 30, 30))
    return im


def main():
    q15(empedrado()).save(os.path.join(OUT, "empedrado.png"))
    q15(tope()).save(os.path.join(OUT, "tope.png"))
    p = ruido((176, 168, 158), 8); d = ImageDraw.Draw(p)
    for k in range(0, 64, 16):
        d.line((k, 0, k, 63), fill=(130, 122, 112))
    q15(p).save(os.path.join(OUT, "banqueta.png"))
    for nom, c in (("rosa", (232, 150, 160)), ("amarillo", (240, 200, 90)), ("blanco", (236, 232, 222)),
                   ("terracota", (200, 110, 70)), ("azulcasa", (110, 170, 210))):
        f = ruido(c, 7); d = ImageDraw.Draw(f)
        d.rectangle((0, 54, 63, 63), fill=tuple(max(0, v - 60) for v in c))      # guardapolvo
        q15(f).save(os.path.join(OUT, f"fachada_{nom}.png"))
    q15(letrero()).save(os.path.join(OUT, "tortilleria.png"))
    q15(ruido((214, 160, 150), 9)).save(os.path.join(OUT, "cantera_rosa.png"))
    # cara roja de coraje: piel teñida, conserva ojos y boca
    for g in ("rel", "a", "e", "o", "m", "f", "sonrisa", "parpadeo", "serio"):
        a = np.asarray(Image.open(os.path.join(OUT, f"cara2_{g}.png")).convert("RGB"), np.float32)
        r = a * np.array([1.18, .52, .46]) + np.array([30, 0, 0])
        q15(Image.fromarray(np.clip(r, 0, 255).astype(np.uint8))).save(os.path.join(OUT, f"cara2_{g}_rojo.png"))
    a = np.asarray(Image.open(os.path.join(OUT, "piel.png")).convert("RGB"), np.float32)
    q15(Image.fromarray(np.clip(a * np.array([1.18, .52, .46]) + np.array([30, 0, 0]), 0, 255).astype(np.uint8))).save(
        os.path.join(OUT, "piel_rojo.png"))
    print("OK", OUT)


if __name__ == "__main__":
    main()
