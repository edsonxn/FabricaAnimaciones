"""Piezas derivadas (una vez, tras `recortar`, desde la carpeta del video): piezas que traen su propio mueble o pared.
extra/diego_toca  = Diego (14) tocando SIN la puerta de madera de la hoja: toca la puerta verde PINTADA de orientación.
extra/diego_golpe = Diego (14) dando el puñetazo SIN el trozo de pared de la hoja: pega en la pared pintada del corredor.
(Lección de jalpa y la_sena: no poner un mueble-pegatina sobre el mueble pintado.)"""
import os

import numpy as np
from PIL import Image

os.makedirs("piezas/extra", exist_ok=True)


def recorta_x(src, dst, x_fin):
    """Se queda con las columnas [0, x_fin) de la pieza (fracción del ancho) y ajusta la caja al alfa."""
    a = np.asarray(Image.open(f"piezas/{src}.png").convert("RGBA")).copy()
    a = a[:, :int(a.shape[1] * x_fin)]
    ys, xs = np.nonzero(a[..., 3] > 8)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(a).save(f"piezas/{dst}.png")
    print(dst, a.shape)


recorta_x("diego14b_hoja/03", "extra/diego_toca", 0.555)
recorta_x("diego14_hoja/02", "extra/diego_golpe", 0.815)
