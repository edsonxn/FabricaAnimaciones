# -*- coding: utf-8 -*-
import sys, os
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, componer, a_uint8, W, H
import mundo as M

lz = Lienzo()
tiles = []
def cuadro(nombre, fn, t=1.0):
    lz.nuevo(t, wob=0.0)
    fn(lz, t)
    bg = np.zeros((H, W, 3), np.float32)
    img = componer(bg, lz.resolver(), boil=0)
    im = cv2.resize(a_uint8(np.clip(img, 0, 1)), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(im, nombre, (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    tiles.append(im)
    return img

def pan(hora, cam, **k):
    est = dict(hora=hora, fuego=0, ruina=0, gente=0.6, luces=0); est.update(k)
    return lambda lz, t: M.panorama(lz, t, est, cam)

cuadro("fuego+estatuas", pan(3.1, (900, -200, 0.8), fuego=1, luces=0.5, estatuas=1, rotura=0.7))
cuadro("tunel", pan(2.0, (-1650, 60, 5.0), tunel=1, hueco=1))
cuadro("hueco+lluvia", pan(3.0, (-1700, -60, 1.6), hueco=1, lluvia=1))
cuadro("turistas", pan(1.4, (1300, -200, 1.0), turistas=1, gente=0, brazos=0.8))
cuadro("obreros", pan(2.0, (900, -100, 1.0), obreros=1, gente=0))
cuadro("camara zoom", pan(2.0, (-1500, 90, 12.0), tunel=1, hueco=1))
rows = [np.hstack(tiles[i:i+3]) for i in range(0, len(tiles), 3)]
out = np.vstack(rows)
cv2.imwrite(os.path.join(os.path.dirname(__file__), "previews", "prueba_mundo.jpg"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
print("ok")
