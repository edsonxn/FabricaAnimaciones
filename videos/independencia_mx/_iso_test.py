# -*- coding: utf-8 -*-
"""Prueba del motor isométrico: python _iso_test.py nombre [zoom]  -> previews/<nombre>.png"""
import sys
import cv2
import numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer, W, H
import plano as P
import kz_iso as I
from util import bg_grad


def casa(lz, iso, x, y, w, d, h, muro, techo, eje="x", puertas=True, ventanas=2, hr=None, zocalo=None):
    c = I.caja(lz, iso, x, y, w, d, h, muro)
    if zocalo:
        I.cara_rect(lz, iso, c, "y", 0, c.w, 0, 7, zocalo)
        I.cara_rect(lz, iso, c, "x", 0, c.d, 0, 7, zocalo)
    I.hilera_ventanas(lz, iso, c, "y", ventanas, h * 0.42, h * 0.34, w * 0.14 if ventanas > 1 else w * 0.18, margen_a=0.12, color=(92, 60, 88), marco=P.aclarar(muro, 0.3), rejas=True)
    I.hilera_ventanas(lz, iso, c, "x", max(1, ventanas - 1), h * 0.42, h * 0.34, d * 0.16, margen_a=0.22, color=(92, 60, 88), marco=P.aclarar(muro, 0.3), rejas=True)
    if puertas:
        I.cara_arco(lz, iso, c, "y", w * 0.43, w * 0.43 + 14, 0, h * 0.58, (120, 74, 60))
    I.techo_dos_aguas(lz, iso, c, eje, hr or (d if eje == "x" else w) * 0.30, techo, vuelo=5.0, gablete=P.aclarar(muro, 0.05))
    return c


if __name__ == "__main__":
    nombre = sys.argv[1]
    zoom = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
    lz = Lienzo()
    lz.nuevo(0.0, wob=0.0)
    iso = I.Iso(160, 150, 0, zoom)
    I.luz()
    # suelo
    I.suelo_rect(lz, iso, -200, -200, 700, 700, (150, 196, 100))
    I.suelo_curvo(lz, iso, [(-40, 20), (330, 20), (330, 300), (-40, 300)], (228, 206, 150))
    I.camino(lz, iso, [(-200, 60), (100, 60), (180, 140), (400, 140), (500, 200)], 46, (240, 224, 176), borde=(214, 190, 140))
    I.cuadricula(lz, iso, -40, 20, 330, 300, 30, color=(255, 255, 255), alfa=0.10)
    mundo = I.Mundo()
    casas = [(20, 40, 90, 52, 56, (250, 236, 208), (206, 96, 78), "x"), (140, 40, 70, 52, 50, (240, 190, 140), (190, 84, 72), "x"),
             (225, 40, 80, 52, 62, (236, 150, 140), (206, 96, 78), "x"), (20, 230, 52, 80, 58, (250, 236, 208), (190, 84, 72), "y"),
             (230, 230, 52, 80, 52, (140, 190, 224), (206, 96, 78), "y")]
    for (x, y, w, d, h, m, tcol, eje) in casas:
        mundo.add(x, y, x + w, y + d, h + 30, (lambda x, y, w, d, h, m, tcol, eje: (lambda lz, iso: (I.sombra_suelo(lz, iso, x, y, w, d, h), casa(lz, iso, x, y, w, d, h, m, tcol, eje, zocalo=P.oscurecer(m, 0.18)))))(x, y, w, d, h, m, tcol, eje))
    mundo.dibujar(lz, iso)
    bg = bg_grad((150, 214, 240), (230, 240, 250))
    img = componer(bg, lz.resolver(), boil=lz.boil)
    cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
    print("ok")
