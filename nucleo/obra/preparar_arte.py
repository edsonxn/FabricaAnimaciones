# -*- coding: utf-8 -*-
"""Arte de «La obra» (vista RTS del panel y de la tele): recorta los dibujos de Flow (fondo magenta) en sprites PNG con
transparencia y hace las texturas de suelo repetibles.

  python nucleo/obra/preparar_arte.py        flow/*.jpg  ->  img/*.png  (+ img/hoja.jpg para revisarlos)

Los originales de Flow (Nano Banana 2.1, 19-nov-2026; prompts en el docstring de abajo) viven en flow/. Estilo pedido:
«classic late-1990s isometric medieval real-time strategy», arte nuevo, nada copiado de ningún juego.
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
FLOW = os.path.join(AQUI, "flow")
IMG = os.path.join(AQUI, "img")

# hoja -> nombres de sus piezas en orden de lectura (filas de arriba abajo, luego izquierda a derecha); alto final en px
HOJAS = {
    "edificio_1": (["cimientos"], 330),
    "edificio_2": (["armazon"], 400),
    "edificio_3": (["taller"], 400),
    "recursos": (["madera", "silicio", "componentes", "pelicula"], 120),
    "adornos": (["roca", "piedras", "arbusto", "arbusto_flor", "tocon", "barril", "cajas", "carretilla", "costal", "cerca"], 70),
    "arboles": (["roble", "pino", "abedul", "castano", "pino_chico", "arce"], 210),
}
# alto propio de algunas piezas (relativo al de su hoja)
ALTO = {"piedras": 40, "cerca": 55, "costal": 50, "barril": 55, "pino_chico": 150, "arbusto": 60, "arbusto_flor": 60, "roca": 70}


def alfa(rgb):
    """Transparencia por distancia al magenta, con borde suave y sin halo rosa (despill)."""
    a = rgb.astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = np.minimum(r, b) - g                     # cuánto «magenta» tiene el pixel
    al = np.clip(1 - (m - 60) / 90, 0, 1)        # m >= 150: fondo; m <= 60: objeto
    tope = np.maximum(g, np.minimum(r, b) - np.clip(m, 0, None) * (1 - al))
    a[..., 0] = np.minimum(r, np.maximum(tope, g + (r - g) * al))
    a[..., 2] = np.minimum(b, np.maximum(tope, g + (b - g) * al))
    return np.dstack([np.clip(a, 0, 255), al * 255]).astype(np.uint8)


def piezas(rgba, n):
    """Las `n` manchas más grandes (cada una con sus pedacitos cercanos), en orden de lectura."""
    sol = rgba[..., 3] > 40
    lab, k = ndimage.label(ndimage.binary_dilation(sol, iterations=9))
    tam = ndimage.sum(sol, lab, range(1, k + 1))
    mayores = sorted(np.argsort(tam)[::-1][:n] + 1)
    cajas = [ndimage.find_objects((lab == i).astype(int))[0] for i in mayores]
    alto = rgba.shape[0]
    cajas.sort(key=lambda s: (round((s[0].start + s[0].stop) / 2 / (alto / 2.2)), s[1].start))   # filas, luego x
    out = []
    for s in cajas:
        i = lab[s]
        mancha = np.bincount(i[i > 0].ravel()).argmax()
        p = rgba[s].copy()
        p[..., 3] = np.where(i == mancha, p[..., 3], 0)
        out.append(p)
    return out


def recortar(p):
    ys, xs = np.nonzero(p[..., 3] > 8)
    return p[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def repetible(ruta, lado=512):
    """Textura que se repite sin costura: centro del dibujo mezclado con su versión desplazada media vuelta."""
    im = np.asarray(Image.open(ruta).convert("RGB"), dtype=np.float32)
    h, w = im.shape[:2]
    c = im[(h - lado) // 2:(h + lado) // 2, (w - lado) // 2:(w + lado) // 2]
    rod = np.roll(c, (lado // 2, lado // 2), axis=(0, 1))
    t = np.linspace(0, 1, lado)
    peso = (1 - np.abs(2 * t - 1))
    wgt = np.clip(np.outer(peso, peso) * 3, 0, 1)[..., None]
    return Image.fromarray((c * wgt + rod * (1 - wgt)).astype(np.uint8))


def main():
    os.makedirs(IMG, exist_ok=True)
    hechos = []
    for hoja, (nombres, alto) in HOJAS.items():
        rgba = alfa(np.asarray(Image.open(os.path.join(FLOW, hoja + ".jpg")).convert("RGB")))
        ps = piezas(rgba, len(nombres))
        if len(ps) != len(nombres):
            print(f"  ¡{hoja}: salieron {len(ps)} piezas y esperaba {len(nombres)}!")
        for nom, p in zip(nombres, ps):
            im = Image.fromarray(recortar(p))
            h = ALTO.get(nom, alto) * 2                 # el doble: se ve nítido de cerca y la tele lo reduce
            im = im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
            im.save(os.path.join(IMG, nom + ".png"), optimize=True)
            hechos.append(nom)
            print(f"  {nom:14s} {im.width}x{im.height}")
    for t in ("pasto", "tierra"):
        repetible(os.path.join(FLOW, t + ".jpg")).save(os.path.join(IMG, t + ".jpg"), quality=88)
    # hoja de revisión sobre gris, para mirar los bordes a mano
    ims = [Image.open(os.path.join(IMG, n + ".png")) for n in hechos]
    W = 1600
    hoja = Image.new("RGB", (W, 900), (96, 110, 96))
    x = y = fila = 0
    for im in ims:
        im.thumbnail((180, 180))
        if x + im.width > W:
            x, y, fila = 0, y + fila + 10, 0
        hoja.paste(im, (x, y), im)
        x += im.width + 10
        fila = max(fila, im.height)
    hoja.save(os.path.join(IMG, "hoja.jpg"), quality=80)


if __name__ == "__main__":
    main()
