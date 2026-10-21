"""Piezas derivadas (una vez, tras `recortar`): recortes de piezas que traen su propio mueble.
rosa_hoja/01c = Rosa dormida SIN su mesa ni su silla (solo de la cubierta de la mesa para arriba): se recarga en la mesa pintada
de cocina_noche_lluvia (lección de jalpa: no poner un mueble-pegatina sobre el mueble pintado)."""
import numpy as np
from PIL import Image

im = Image.open("piezas/rosa_hoja/01.png").convert("RGBA")
a = np.asarray(im)
corte = int(a.shape[0] * 0.355)                 # justo bajo los codos: fuera la mesa propia
b = a[:corte].copy()
xs = np.where(b[..., 3].max(0) > 8)[0]
b = b[:, xs.min():xs.min() + int((xs.max() - xs.min()) * 0.93)]   # fuera la esquina de su mesa (derecha)
Image.fromarray(b).save("piezas/rosa_hoja/01c.png")
print("rosa_hoja/01c", b.shape)
