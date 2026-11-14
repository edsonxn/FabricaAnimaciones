# -*- coding: utf-8 -*-
"""Icono del Estudio Amaya: cuadro redondeado con degradado lila → rosa → durazno, una «A» blanca y una estrella dorada.

    python nucleo/amaya/icono.py        → nucleo/amaya/web/icono-192.png, icono-512.png y manifest.webmanifest
"""
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(AQUI, "web")
FUENTES = [r"C:\Windows\Fonts\seguibl.ttf", r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"]


def _estrella(g, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    g.polygon(pts, fill=color)


def icono(lado, redondo=True):
    k = 4
    n = lado * k
    fondo = Image.new("RGB", (n, n))
    px = fondo.load()
    c = [(169, 139, 255), (255, 111, 181), (255, 179, 138)]
    for y in range(n):
        for x in range(n):
            t = (x * 0.55 + y * 0.45) / n
            a, b, u = (c[0], c[1], t / 0.55) if t < 0.55 else (c[1], c[2], (t - 0.55) / 0.45)
            u = max(0.0, min(1.0, u))
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    mascara = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * (.24 if redondo else 0)), fill=255)
    im.paste(fondo, (0, 0), mascara)
    fuente = next((f for f in FUENTES if os.path.exists(f)), None)
    f = ImageFont.truetype(fuente, int(n * 0.62)) if fuente else ImageFont.load_default()
    capa = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    g = ImageDraw.Draw(capa)
    caja = g.textbbox((0, 0), "A", font=f)
    x = (n - (caja[2] - caja[0])) / 2 - caja[0]
    y = (n - (caja[3] - caja[1])) / 2 - caja[1] + n * 0.03
    sombra = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).text((x, y + n * 0.025), "A", font=f, fill=(90, 20, 80, 110))
    im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(n * 0.012)))
    g.text((x, y), "A", font=f, fill=(255, 255, 255, 255))
    _estrella(g, n * 0.76, n * 0.25, n * 0.11, (255, 212, 92, 255))
    _estrella(g, n * 0.22, n * 0.78, n * 0.045, (255, 255, 255, 230))
    im.alpha_composite(capa)
    return im.resize((lado, lado), Image.LANCZOS)


def main():
    os.makedirs(WEB, exist_ok=True)
    for lado in (192, 512):
        icono(lado).save(os.path.join(WEB, f"icono-{lado}.png"))
    man = {"name": "Estudio Amaya", "short_name": "Amaya", "start_url": "./", "scope": "./", "display": "standalone",
           "background_color": "#1a1033", "theme_color": "#1a1033",
           "icons": [{"src": "icono-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "icono-512.png", "sizes": "512x512", "type": "image/png"}]}
    with open(os.path.join(WEB, "manifest.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)
    print("iconos listos en", WEB)


if __name__ == "__main__":
    main()
