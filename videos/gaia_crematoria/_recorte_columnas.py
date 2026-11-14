"""2-nov: recorte por COLUMNAS para hojas cuyas figuras se tocan (rembg las junta y `recortar` las parte mal).

Corta la hoja en franjas por el valle de alfa más cercano a cada corte aproximado; cada franja = UNA pieza (con todo lo
que tenga dentro: el orbe de Isillien va con su figura). Pisa piezas/<hoja>/ (NN.png, _indice.jpg, meta.json).
Uso: python _recorte_columnas.py h16_consejo_hoja h31_isillien_joven
"""
import json
import os
import sys

import numpy as np
from scipy import ndimage
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "..", "nucleo"))
import pegaflow  # noqa: E402

CORTES = {"h16_consejo_hoja": [380, 590, 805, 1015, 1195],        # x aprox. (1376 px) entre figuras
          "h31_isillien_joven": [326, 598, (862, 4), 1067]}      # (x, ventana): el rayo entero va con su figura


def recortar(nom, sesion):
    ruta = os.path.join(D, "hojas", f"{nom}_a.jpg")
    rgb = np.asarray(Image.open(ruta).convert("RGB"))
    h, w = rgb.shape[:2]
    dec, a = pegaflow._alfa_hoja(rgb, sesion=sesion)
    perfil = a.sum(axis=0)
    xs = [0]
    for c in CORTES[nom]:
        c, r = c if isinstance(c, tuple) else (c, 30)
        lo, hi = c - r, c + r
        xs.append(lo + int(np.argmin(perfil[lo:hi])))
    xs.append(w)
    dst = os.path.join(D, "piezas", nom)
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(dst):
        if f.endswith(".png"):
            os.remove(os.path.join(dst, f))
    piezas, meta = [], []
    for i in range(len(xs) - 1):
        al = a[:, xs[i]:xs[i + 1]].copy()
        lab, n = ndimage.label(al > 0.1)
        if n > 1:                                  # trocitos del vecino pegados al borde de la franja → fuera
            areas = ndimage.sum(np.ones_like(al), lab, range(1, n + 1))
            for j, ar in enumerate(areas, 1):
                cx = np.nonzero((lab == j).any(axis=0))[0]
                if ar < 0.08 * areas.max() and (cx[0] == 0 or cx[-1] == al.shape[1] - 1):
                    al[ndimage.binary_dilation(lab == j, iterations=2)] = 0
        ys, xx = np.nonzero(al > 0.02)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xx.min(), xx.max() + 1
        p = 3
        sa = np.pad(al[y0:y1, x0:x1], p)
        sc = np.pad(dec[y0:y1, xs[i] + x0:xs[i] + x1], ((p, p), (p, p), (0, 0)), mode="edge")
        pz = np.dstack([sc, (sa * 255).round().astype(np.uint8)])
        Image.fromarray(pz).save(os.path.join(dst, f"{i:02d}.png"))
        piezas.append(pz)
        meta.append(dict(n=i, w=int(pz.shape[1]), h=int(pz.shape[0]), caja=[int(xs[i] + x0), int(y0), int(x1 - x0), int(y1 - y0)]))
    pegaflow._indice(piezas, os.path.join(dst, "_indice.jpg"))
    json.dump(dict(fuente=os.path.basename(ruta), tam=[w, h], piezas=meta, ciclo=None, columnas=xs),
              open(os.path.join(dst, "meta.json"), "w", encoding="utf-8"), indent=1)
    print(nom, len(piezas), "piezas, cortes", xs)


if __name__ == "__main__":
    from rembg import new_session
    ses = new_session("isnet-anime")
    for n in sys.argv[1:]:
        recortar(n, ses)
