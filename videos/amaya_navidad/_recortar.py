# -*- coding: utf-8 -*-
"""Recorta las hojas de stickers de Flow y deja cada objeto con su nombre en stickers/<nombre>.png (+ hoja de control)."""
import os
import shutil
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import cv2
import numpy as np
import pegaflow

# hoja → nombres en orden de lectura (filas de 3)
HOJAS = {
    "hojaA_1": ["squishy", "pinzas", "scrunchies_a", "diario_a", "cuentas_a", "agenda_a", "pluma_a1", "pluma_a2", "tarjeta_a"],
    "hojaA_2": ["fidget", "scrunchies", "pinzas_b", "diario", "cuentas", "agenda", "pluma1", "pluma2", "tarjeta"],
    "hojaB_1": ["calcetines", "carta", "cajon", "cerezas", "megafono", "regalo"],
    "hojaC_2": ["baston", "arbolito", "gatito", "galleta", "chocolate", "esfera"],
    "hojaD_1": ["bodymist", "lampara", "paleta", "pantuflas", "sudadera", "bocina"],
    "hojaE_1": ["bolsa", "bebe", "balsamo", "balsamo_tapa", "canasta", "termo", "audifonos_pirata", "audifono_suelto"],
    "hojaF_1": ["oso", "croissant", "perrito", "controles", "serum", "crema", "audifonos"],
    "hojaG_2": ["camara", "fotos_b", "rollo", "calcetin_nav1", "calcetin_nav2", "clip_b", "sello_b"],
    "hojaG_1": ["camara_b", "fotos", "rollo_b", "calcetin_reno1", "calcetin_reno2", "clip", "sello_goma"],
}
AQUI = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(AQUI, "stickers"), exist_ok=True)
fichas = []
for hoja, nombres in HOJAS.items():
    tmp = os.path.join(AQUI, "flow", "_piezas", hoja)
    n = pegaflow.recortar_hoja(os.path.join(AQUI, "flow", hoja + ".jpg"), tmp, n_esperado=len(nombres))
    print(hoja, n, "piezas")
    for i, nom in enumerate(nombres[:n]):
        dst = os.path.join(AQUI, "stickers", nom + ".png")
        shutil.copy(os.path.join(tmp, f"{i:02d}.png"), dst)
        im = cv2.imread(dst, cv2.IMREAD_UNCHANGED)
        a = im[..., 3:4] / 255.0
        bg = np.full_like(im[..., :3], (190, 160, 230))
        c = (im[..., :3] * a + bg * (1 - a)).astype(np.uint8)
        f = 220 / max(c.shape[:2])
        c = cv2.resize(c, (int(c.shape[1] * f), int(c.shape[0] * f)))
        ficha = np.full((260, 240, 3), (190, 160, 230), np.uint8)
        ficha[:c.shape[0], :c.shape[1]] = c
        cv2.putText(ficha, nom, (4, 252), 0, 0.55, (0, 0, 0), 1)
        fichas.append(ficha)
while len(fichas) % 9:
    fichas.append(np.zeros_like(fichas[0]))
cv2.imwrite(os.path.join(AQUI, "previews", "stickers_check.jpg"),
            np.vstack([np.hstack(fichas[i:i + 9]) for i in range(0, len(fichas), 9)]), [cv2.IMWRITE_JPEG_QUALITY, 80])
