# -*- coding: utf-8 -*-
"""Recortes de rembg para las siluetas e imágenes nuevas -> previews/_rec.jpg"""
import sys
sys.path.insert(0, "../../nucleo")
import peg_estilos as PE
from PIL import Image
L = ["runil_b", "cicero", "erik", "ulfric", "paarthurnax", "esbern", "tullius", "arngeir", "margret", "jurgen", "alduin", "f_delphine.jpg", "f_neloth.jpg", "f_neloth2.jpg"]
cel = []
for n in L:
    p = "pegatinas/" + (n if "." in n else n + ".png")
    r = PE.recorte(p)
    print(n, r.size, flush=True)
    bg = Image.new("RGBA", r.size, (90, 120, 90, 255))
    bg.alpha_composite(r)
    k = 300 / bg.height
    cel.append(bg.convert("RGB").resize((max(1, int(bg.width * k)), 300)))
for n in ["torre_skyrim", "montana_roja", "nave_extrana", "martinet", "ramati", "madre_noche_ob", "alisanne", "garnag", "sala_falkreath", "karan_diario", "com_UgzJYFZJk-eBnw3xQoB4AaABAg", "com_Ugw36BCPJX6pZT5glDh4AaABAg"]:
    im = Image.open("pegatinas/" + n + ".png").convert("RGBA")
    bg = Image.new("RGBA", im.size, (40, 40, 40, 255))
    bg.alpha_composite(im)
    k = 300 / bg.height
    cel.append(bg.convert("RGB").resize((min(900, max(1, int(bg.width * k))), 300)))
hoja = Image.new("RGB", (1920, 1200), (0, 0, 0))
x = y = 0
for c in cel:
    if x + c.width > 1920:
        x, y = 0, y + 300
    hoja.paste(c, (x, y))
    x += c.width
hoja.save("previews/_rec.jpg", quality=82)
