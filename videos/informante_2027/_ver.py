# -*- coding: utf-8 -*-
"""Hoja de prueba de los mundos y la utilería nuevos: python videos/informante_2027/_ver.py [mundos|props] -> previews/ver_*.jpg"""
import math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)
import cv2
import numpy as np
from motor import H, W
from noir import Noir
import noir as N
import kit27 as K
import mundos27 as M
import props as PR

h = Noir()
que = sys.argv[1] if len(sys.argv) > 1 else "mundos"
tiles = []


def guarda(img, nom):
    im = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(f"previews/ver_{nom}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, nom, (8, 24), 0, 0.7, (255, 255, 255), 2)
    tiles.append(sm)


if que == "mundos":
    for nom in ("laboratorio", "sala_comite", "capitolio", "fabrica", "redaccion", "despacho"):
        h.nuevo(1.0, None)
        h.camara(1.0, 960, 540, 0.0)
        getattr(M, nom)().pegar(h, 1.0)
        h.ambiente[:] = 0.9
        guarda(h.acabado(1.0), nom)
else:
    t = 3.0
    h.nuevo(t, None); h.camara(1.0, 960, 540, 0.0); K.pared(h, 60, 24, ladrillo=True)
    K.calendario(h, t, 0, "ABRIL", "2024", "", cx=330, cy=520, s=0.8)
    K.carpeta(h, 1000, 420, 0.8, "2027", t, 0)
    K.billetes(h, 1560, 980, 6); K.pluma(h, 1500, 400, -0.8, 1.2, 40)
    K.garabato(h, 1380, 560, 1.0, 1.2, 50)
    h.ambiente[:] = 0.9; guarda(h.acabado(t), "p1")
    h.nuevo(t, None); h.camara(1.0, 960, 540, 0.0); K.pared(h, 50, 20, paneles=9)
    K.casa(h, 360, 900, 0.9, 0.85, 3); K.balanza(h, 1000, 250, 0.7, 0.8, 30); K.chip(h, 1620, 300, 0.9, 60, 1.0)
    K.interruptor(h, 1620, 760, 0.55, 0.0, 80, t=t)
    h.ambiente[:] = 0.9; guarda(h.acabado(t), "p2")
    h.nuevo(t, None); h.camara(1.0, 960, 540, 0.0); K.pared(h, 60, 24)
    K.reloj_arena(h, 300, 540, 1.0, 0.4, t, 3); K.puerta(h, 620, 200, sem=20, rendija=1.0, vidrio="COMITÉ", t=t)
    K.mano_alzada(h, 1250, 420, 1.0, 1.0, 40); K.robot(h, 1650, 1000, 1.3, t, 60, brazo=0.6)
    K.flecha(h, (1100, 150), (1500, 150), 10, 90, curva=40)
    K.barra(h, 1100, 60, 500, 40, 0.75, 95)
    h.ambiente[:] = 0.9; guarda(h.acabado(t), "p3")
    h.nuevo(t, None); h.camara(1.0, 960, 540, 0.0); M.capitolio().pegar(h, 1.0)
    K.multitud(h, t, -60, 1980, 1100, 30, 0.9, 5, carteles=("EMPLEOS", "PAREN LA IA", "¿Y NOSOTROS?"))
    h.ambiente[:] = 0.8; guarda(h.acabado(t), "p4")
    h.nuevo(t, None); h.camara(1.0, 960, 540, 0.0); h.img[:] = 0.05
    K.pantalla_codigo(h, (80, 80, 700, 420), t, 3)
    n = K.cajas(h, t, 0, 16, 5, 900, 300, 62, 150, 0.2, 100)
    PR.caja_negra(h, 400, 1040, 0.9, 1.0, t, sem=300)
    h.ambiente[:] = 0.7; guarda(h.acabado(t), "p5")
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
cv2.imwrite(f"previews/ver_{que}.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok", que)
