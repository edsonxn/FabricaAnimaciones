# -*- coding: utf-8 -*-
import os
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, componer, a_uint8, W, H
import especiales as E, mundo as M

lz = Lienzo()
tiles = []
def cuadro(nombre, fn, t=1.0):
    lz.nuevo(t, wob=0.0)
    fn(lz, t)
    img = componer(np.zeros((H, W, 3), np.float32), lz.resolver(), boil=0)
    im = cv2.resize(a_uint8(np.clip(img, 0, 1)), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(im, nombre, (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    tiles.append(im)

cuadro("casa", lambda lz, t: E.casa_corte(lz, t, dict(casa=1)), 2.0)
cuadro("mito duda", lambda lz, t: E.mito(lz, t, dict(llama=0.6, duda=1.5)))
cuadro("mito salto", lambda lz, t: E.mito(lz, t, dict(llama=1.0, duda=4, salto=0.5)))
cuadro("mito flare", lambda lz, t: E.mito(lz, t, dict(llama=1.8, duda=4, salto=0.96, alba=0.2)))
cuadro("mito sol", lambda lz, t: E.mito(lz, t, dict(llama=1.0, duda=4, salto=1.0, sol=0.6, alba=0.7)))
def por(lz, t):
    M.panorama(lz, t, dict(hora=2.0, fuego=0, ruina=0, gente=0.5, luces=0), (1300, -200, 1.0))
    with E.portal(lz, 960, 540, 380, 0.7):
        E.casa_corte(lz, t, dict(casa=1))
cuadro("portal", por)
rows = [np.hstack(tiles[i:i+3]) for i in range(0, len(tiles), 3)]
cv2.imwrite(os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews", "prueba_esp.jpg"), cv2.cvtColor(np.vstack(rows), cv2.COLOR_RGB2BGR))
print("ok")
