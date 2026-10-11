# -*- coding: utf-8 -*-
import os
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, componer, a_uint8, W, H
import mapa as MP

lz = Lienzo()
tiles = []
def cuadro(nombre, cam, **est):
    lz.nuevo(1.0, wob=0.0)
    e = dict(cdmx=1, rutas=1, gente_top=1, ciudad_alfa=1); e.update(est)
    MP.mapa(lz, 1.0, cam, e)
    MP.marcador(lz, cam, "teo", "Teotihuacán")
    bg = np.zeros((H, W, 3), np.float32)
    img = componer(bg, lz.resolver(), boil=0)
    im = cv2.resize(a_uint8(np.clip(img, 0, 1)), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(im, nombre, (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    tiles.append(im)

cuadro("meso z.22", (-95.5, 19.5, 0.22))
cuadro("valle z3", (-99.0, 19.55, 3.0))
cuadro("z12", (-98.85, 19.69, 12))
cuadro("ciudad z60", MP.lonlat_ciudad(1, 4) + (60,), rutas=0)
cuadro("sol z250", MP.lonlat_ciudad(1.9, 7) + (250,))
cuadro("luna z300", MP.lonlat_ciudad(0, 21.4) + (300,))
rows = [np.hstack(tiles[i:i+3]) for i in range(0, len(tiles), 3)]
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews", "prueba_mapa.jpg"), cv2.cvtColor(np.vstack(rows), cv2.COLOR_RGB2BGR))
print("ok")
