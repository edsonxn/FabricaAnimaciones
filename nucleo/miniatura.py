# -*- coding: utf-8 -*-
"""Miniaturas (thumbnails) con el mismo motor, personajes y estilo del video.

El video define en su carpeta `miniaturas.py` un dict VARIANTES = {nombre: fn(lz) -> fondo}: cada fn dibuja en el
lienzo (ya limpio) y devuelve el fondo float32 HxWx3 en [0,1]. Para cada variante se guarda
salida/<ARCHIVO>_mini_<nombre>.jpg a 1280x720 (< 2 MB, límite de YouTube) y previews/miniaturas.jpg con cada una a
tamaño grande y al tamaño en que se ve en el celular (~250 px de ancho) para comprobar que se entiende de un vistazo.
Consejos (lo que mejor funciona en el nicho): 1-3 palabras enormes con contorno, un personaje con cara expresiva,
alto contraste y una idea que se capte en 1 segundo; el texto complementa al título, no lo repite.
Uso: python fab.py <video> miniatura [nombre ...]"""
import os
import sys

import cv2
import numpy as np

import config
import escena_base  # noqa: F401  (activa el estilo del video)
import efectos as E
import miniaturas as V
from final import slug
from motor import Lienzo, a_uint8, componer, VERTICAL, W

os.makedirs("salida", exist_ok=True)
os.makedirs("previews", exist_ok=True)
base = os.path.join("salida", (config.ARCHIVO or slug(config.TITULO)) + "_mini_")
pedidas = sys.argv[1:] or list(V.VARIANTES)
lz = Lienzo()
filas = []
for nombre in pedidas:
    lz.nuevo(getattr(V, "T", 0.37), wob=getattr(V, "WOB", 1.2))
    fondo = V.VARIANTES[nombre](lz)
    img = componer(fondo, lz.resolver(), boil=lz.boil)
    img = E.acabado(img, 3)
    rgb = a_uint8(np.clip(img, 0, 1))
    if VERTICAL:      # video vertical: la miniatura 16:9 se dibuja en una franja del lienzo
        y0 = getattr(V, "CROP_Y", 0)
        rgb = rgb[y0:y0 + int(W * 9 / 16)]
    mini = cv2.resize(rgb, (1280, 720), interpolation=cv2.INTER_AREA)
    ruta = f"{base}{nombre}.jpg"
    for q in (95, 90, 85, 80):
        cv2.imwrite(ruta, cv2.cvtColor(mini, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, q])
        if os.path.getsize(ruta) < 1_900_000:
            break
    print(f"{ruta}  {os.path.getsize(ruta) / 1e6:.2f} MB")
    grande = cv2.resize(rgb, (768, 432), interpolation=cv2.INTER_AREA)
    movil = cv2.resize(rgb, (246, 138), interpolation=cv2.INTER_AREA)
    col = np.full((432, 280, 3), 30, np.uint8)
    col[20:158, 17:263] = movil
    cv2.putText(col, nombre, (17, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    filas.append(np.hstack([grande, col]))
cv2.imwrite("previews/miniaturas.jpg", cv2.cvtColor(np.vstack(filas), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("previews/miniaturas.jpg")
