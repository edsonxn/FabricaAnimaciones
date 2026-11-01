# -*- coding: utf-8 -*-
"""Pone el logo real de Skyrim (Wikimedia Commons, en negro) en blanco con resplandor oscuro abajo a la izquierda de la
miniatura de Flow, como el logo de Forever en las de Crónicas de Warcraft.  python miniatura_logo.py [variante]"""
import os
import sys

from PIL import Image, ImageFilter, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
ING = os.path.join(AQUI, "miniatura_ing")
SAL = os.path.join(AQUI, "salida")
v = sys.argv[1] if len(sys.argv) > 1 else "v2"

base = Image.open(os.path.join(SAL, "flow", f"miniatura_{v}.png")).convert("RGBA").resize((1280, 720), Image.LANCZOS)


def blanco(ruta, ancho=None, alto=None):
    im = Image.open(ruta).convert("RGBA")
    im = im.crop(im.getbbox())
    a = im.getchannel("A") if im.mode == "RGBA" else ImageOps.invert(im.convert("L"))
    if ancho:
        alto = int(im.height * ancho / im.width)
    else:
        ancho = int(im.width * alto / im.height)
    a = a.resize((ancho, alto), Image.LANCZOS)
    w = Image.new("RGBA", a.size, (246, 242, 232, 255))
    w.putalpha(a)
    return w


emblema = blanco(os.path.join(ING, "logo_Skyrim_logo.png"), alto=170)
marca = blanco(os.path.join(ING, "logo_The_Elder_Scrolls_V_-_Skyrim_logo.png"), ancho=360)
x0, yb = 34, 720 - 30
capa = Image.new("RGBA", base.size, (0, 0, 0, 0))
capa.alpha_composite(emblema, (x0, yb - emblema.height))
capa.alpha_composite(marca, (x0 + emblema.width + 18, yb - emblema.height // 2 - marca.height // 2))
sombra = Image.new("RGBA", base.size, (0, 0, 0, 0))
sombra.putalpha(capa.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10)))
base.alpha_composite(sombra)
base.alpha_composite(sombra)
base.alpha_composite(capa)
out = os.path.join(SAL, "miniatura.jpg")
base.convert("RGB").save(out, quality=92)
print(out, os.path.getsize(out) // 1024, "KB")
