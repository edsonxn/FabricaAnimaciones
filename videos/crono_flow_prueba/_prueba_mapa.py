# -*- coding: utf-8 -*-
"""Prueba: pegatinas de Flow (con la referencia del kit como ingrediente) sobre un cuadro real del mapa de historia_egipto.
8 s a 24 fps → previews/prueba_mapa.mp4 + previews/prueba_mapa.jpg. Uso: python _prueba_mapa.py"""
import os
import subprocess

import numpy as np
from PIL import Image, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
FPS, DUR, W, H = 24, 8.0, 1920, 1080
FONDO = Image.open(os.path.join(D, "ref", "fondo_mapa.png")).convert("RGBA")
_cache = {}


def pegatina(ruta, alto, voltear=False):
    """Pieza RGBA → pegatina del kit: borde crema + sombra suave, escalada a `alto` px."""
    k = (ruta, alto, voltear)
    if k in _cache:
        return _cache[k]
    im = Image.open(os.path.join(D, "piezas", ruta)).convert("RGBA")
    if voltear:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    s = alto / im.height
    im = im.resize((max(1, int(im.width * s)), alto), Image.LANCZOS)
    b = max(4, alto // 22)                       # grosor del borde blanco
    pad = b * 3
    lz = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", lz.size, 0)
    a.paste(im.getchannel("A"), (pad, pad))
    borde = a.filter(ImageFilter.MaxFilter(2 * b + 1)).filter(ImageFilter.GaussianBlur(1))
    sombra = borde.filter(ImageFilter.GaussianBlur(b)).point(lambda v: int(v * 0.35))
    out = Image.new("RGBA", lz.size, (0, 0, 0, 0))
    out.paste(Image.new("RGBA", lz.size, (40, 30, 20, 255)), (b // 2, b), sombra)
    out.paste(Image.new("RGBA", lz.size, (250, 247, 240, 255)), (0, 0), borde)
    out.alpha_composite(im, (pad, pad))
    _cache[k] = out
    return out


def poner(cuadro, peg, x, y, esc=1.0):
    """Pega con los pies (borde inferior) en (x, y)."""
    if esc != 1.0:
        peg = peg.resize((max(1, int(peg.width * esc)), max(1, int(peg.height * esc))), Image.LANCZOS)
    cuadro.alpha_composite(peg, (int(x - peg.width / 2), int(y - peg.height)))


def suave(u):
    u = min(1, max(0, u))
    return u * u * (3 - 2 * u)


def pop(t, t0):
    """Aparición con rebote (0 → 1,12 → 1)."""
    u = (t - t0) / 0.35
    if u <= 0:
        return 0
    if u >= 1:
        return 1
    return 1.12 * np.sin(u * np.pi / 2) ** 0.6 if u < 0.7 else 1.12 - 0.12 * (u - 0.7) / 0.3


CICLO = sorted(f for f in os.listdir(os.path.join(D, "piezas", "07_marcha_ref")) if f.startswith("ciclo_"))


def cuadro(t):
    c = FONDO.copy()
    # barco fenicio por el Mediterráneo, meciéndose
    x = 430 + 170 * suave(t / DUR)               # a la derecha del contador del año
    poner(c, pegatina("05_barcos_ref/01.png", 110), x, 160 + 4 * np.sin(t * 3), 1)
    # camello cruzando el Sinaí con un paso que sube y baja
    if t > 0.6:
        x = 1080 + 230 * (t - 0.6) / (DUR - 0.6)
        poner(c, pegatina("08_animales_ref/00.png", 120), x, 560 - abs(np.sin(t * 6)) * 6, pop(t, 0.6))
    # carro de guerra que entra por Arabia (en la hoja mira a la izquierda: ya va hacia el oeste)
    if t > 1.4:
        x = 2000 - 380 * suave((t - 1.4) / 4)
        poner(c, pegatina("08_animales_ref/02.png", 115), x, 400 - abs(np.sin(t * 9)) * 4)
    # legión de 4 en formación con el ciclo de marcha (cuadro según distancia: los pies no patinan)
    for k in range(4):
        d = 150 * t                               # px recorridos
        x = -120 + d - k * 95
        fr = CICLO[int((d + k * 37) / 22) % len(CICLO)]
        poner(c, pegatina("07_marcha_ref/" + fr, 140), x, 985 + (k % 2) * 18)
    # faraón a la derecha, presentado con rebote
    e = pop(t, 2.2)
    if e:
        poner(c, pegatina("06_personas_ref/00.png", 360), 1660, 1030 + 6 * np.sin(t * 2.2), e)
    # barca de papiro por el Nilo
    if t > 3.2:
        y = 860 - 240 * suave((t - 3.2) / 4.8)
        poner(c, pegatina("05_barcos_ref/00.png", 95), 800 + (860 - y) * 0.05, y, pop(t, 3.2))
    return c.convert("RGB")


if __name__ == "__main__":
    pv = os.path.join(D, "previews")
    os.makedirs(pv, exist_ok=True)
    cuadro(5.5).save(os.path.join(pv, "prueba_mapa.jpg"), quality=88)
    ff = subprocess.Popen([r"C:\ffmpeg\bin\ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           os.path.join(pv, "prueba_mapa.mp4")], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        ff.stdin.write(np.asarray(cuadro(i / FPS)).tobytes())
    ff.stdin.close()
    ff.wait()
    print("listo", os.path.join(pv, "prueba_mapa.mp4"))
