"""Hoja de objetos de Japón: python _obj_test.py [a|b|c]  -> previews/_o_<x>.jpg"""
import sys

import cv2
import numpy as np

import boceto as B
import mapa as M
from obj_base import *  # noqa: F401,F403
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_j as J

M.cargar()
cam = M.Cam(136.0, 37.0, 2.2)
img = M.fondo_base()
M.pintar_tierra(img, cam, 0)
h = B.Hoja()
h.limpiar()
h.fondo = img
lista = sys.argv[1] if len(sys.argv) > 1 else "a"
if lista == "a":
    D = [J.samurai(0), J.samurai_paz(0), J.ashigaru(0), J.emperador_jp(), J.dama_heian(), J.emperador_meiji(),
         J.oficial_naval(), J.marino_yanqui(), J.comerciante(), J.obrero_jp(), J.geisha(), J.campesino_jp()]
elif lista == "b":
    D = [J.torii(), J.castillo(), J.templo(), J.kofun(), J.cerezo(0), J.monte_fuji(), J.gran_ola(), J.barco_mongol(), J.barco_negro(0),
         J.locomotora(0), J.bandera_japon(), J.sol_naciente()]
else:
    D = [J.hongo(0), J.avion_zero(0), J.radio(), J.aros_olimpicos(), J.mascara_kabuki(), J.vasija_jomon(), J.tablilla_ley(),
         J.arroz_planta(0), J.nube_petalos(), J.nino_jp(), Bb.caballo(1), C.tren_bala()]
for i, d in enumerate(D):
    x = 170 + (i % 6) * 320
    y = 520 + (i // 6) * 430
    d.dibujar(h, x, y, 0.62 if lista == "a" else 0.55, 0.0, False, 1.0, 0, i + 1, peg=True)
out = np.clip(h.componer(), 0, 1)
cv2.imwrite(f"previews/_o_{lista}.jpg", (out[..., ::-1] * 255).astype(np.uint8))
print("ok")
