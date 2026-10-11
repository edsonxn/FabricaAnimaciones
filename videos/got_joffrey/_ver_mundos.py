# -*- coding: utf-8 -*-
"""Hoja de los mundos pintados (composición base de cada uno con su rampa y su luz) -> previews/mundos_<grupo>.jpg
    python videos/got_joffrey/_ver_mundos.py j1|j2|j3 [t]"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import noir as N
import noir_color as NC
import noir_feudal as NF
import noir_corte as CO  # noqa: F401

grupo = sys.argv[1] if len(sys.argv) > 1 else "j1"
t = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
h = NC.NoirColor("antorcha")


def amb(k):
    h.ambiente[:] = np.array(h.pal["luna"], np.float32) * k


COMPOS = {}
if grupo == "j1":
    import mundos_j1 as M

    def ciudad():
        h.camara(1.0, 900, 300)
        NC.pegar(M.cielo_fiesta(), h, 0.05, rampa="cielo")
        NC.pegar(M.fortaleza(), h, 0.3, rampa="ladrillo", bruma=0.22)
        NC.pegar(M.tejados(), h, 0.6, rampa="entramado", bruma=0.2)
        NC.pegar(M.calle_fiesta(), h, 1.0, rampa="entramado", emis=0.9)
        NC.pegar(M.empedrado(), h, 1.0, rampa="muralla")
        amb(0.8)
        h.luz_radial(900, 200, 900, h.pal["antorcha"], k=0.6)

    def salon():
        h.camara(1.0, 960, 540)
        NC.pegar(M.salon_muro(), h, 1.0, rampa="muralla")
        NC.pegar(M.salon_ventanas(), h, 1.0, rampa="hierro", col_emis=h.pal["luna"])
        NC.pegar(M.salon_suelo(), h, 1.0, rampa="muralla")
        NC.pegar(M.salon_mesas(), h, 1.0, rampa="pergamino")
        amb(0.35)
        h.luz_radial(960, 300, 1100, h.pal["vela"], k=1.1)

    def lado():
        h.camara(1.0, 960, 540)
        NC.pegar(M.tapiz_muro(), h, 0.8, rampa="estandarte")
        NC.pegar(M.mesa_larga(), h, 1.0, rampa="pergamino")
        amb(0.35)
        h.luz_radial(960, 400, 1100, h.pal["vela"], k=1.1)

    def estrado():
        h.camara(1.0, 960, 540)
        NC.pegar(M.estrado_muro(), h, 0.8, rampa="muralla")
        NC.pegar(M.estrado(), h, 1.0, rampa="madera")
        amb(0.35)
        h.luz_radial(960, 400, 1100, h.pal["vela"], k=1.1)

    def losas():
        h.camara(1.0, 960, 540)
        NC.pegar(M.losas(), h, 1.0, rampa="muralla")
        amb(0.35)
        h.luz_radial(960, 400, 900, h.pal["vela"], k=1.1)
    COMPOS = dict(ciudad=ciudad, salon=salon, lado=lado, estrado=estrado, losas=losas)
elif grupo == "j2":
    import mundos_j2 as M
    COMPOS = M.VER(h, amb)
elif grupo == "j3":
    import mundos_j3 as M
    COMPOS = M.VER(h, amb)

tiles = []
for nom, fn in COMPOS.items():
    h.nuevo(t, None)
    h.rim_color(h.pal["luna"])
    fn()
    im = (np.clip(h.acabado(t, niebla=dict(dens=0.12)), 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(f"previews/m_{nom}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, nom, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    tiles.append(sm)
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
cv2.imwrite(f"previews/mundos_{grupo}.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print(f"-> previews/mundos_{grupo}.jpg")
