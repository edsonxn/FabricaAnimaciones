# -*- coding: utf-8 -*-
"""Prueba 2 del motor isométrico: plaza de un pueblo colonial. python _iso_test2.py nombre [zoom] [t]"""
import sys, math
import cv2
import numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer, W, H
import plano as P
import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_gente_iso as G
from util import bg_grad


def escena(t=0.0):
    m = I.Mundo()
    # edificios
    A.iglesia(m, 60, -100, w=64, largo=116, h_nave=58)
    A.casa_colonial(m, -60, -20, 84, 50, 50, muro=A.OCRE, eje="x", ventanas=3, seed=1)
    A.casa_colonial(m, -60, 56, 70, 46, 44, muro=A.ROSA, eje="x", ventanas=2, seed=2, chimenea=True)
    A.portal_arcos(m, 150, -20, 5, paso=22, d=14, h=40, muro=A.CAL)
    A.casa_plana(m, 262, -4, 56, 48, 46, muro=A.AZUL, acento=(236, 150, 100), ventanas=2)
    A.casa_colonial(m, 262, 70, 52, 70, 52, muro=A.VERDE_CAL, eje="y", ventanas=2, puerta=False, seed=3, balcon=True)
    A.casa_colonial(m, -60, 130, 60, 56, 48, muro=A.CAL, eje="x", ventanas=2, seed=4)
    A.puesto(m, 190, 120, toldo=(236, 90, 96), seed=1)
    A.puesto(m, 222, 142, toldo=(70, 160, 200), cosas=(236, 120, 70), seed=2)
    # vegetación
    for i, (x, y) in enumerate(((24, 160), (96, 180), (200, 200), (250, 170), (-30, 112), (300, 30), (130, 230), (-40, 210), (320, 150), (28, 250))):
        (lambda x, y, i: m.add(x - 12, y - 12, x + 12, y + 12, 60, lambda lz, iso: O.arbol(lz, iso, x, y, h=48 + 8 * (i % 3), seed=i, t=t)))(x, y, i)
    for i, (x, y) in enumerate(((-12, 40), (30, 60), (140, 6), (330, 100), (60, 188))):
        (lambda x, y, i: m.add(x - 8, y - 8, x + 8, y + 8, 60, lambda lz, iso: O.cipres(lz, iso, x, y, h=54, seed=i)))(x, y, i)
    for i, (x, y) in enumerate(((90, 56), (110, 56), (206, 60), (50, 126), (240, 118), (120, 168), (170, 240))):
        (lambda x, y, i: m.add(x - 6, y - 6, x + 6, y + 6, 20, lambda lz, iso: O.arbusto(lz, iso, x, y, r=9, seed=i, flores=(236, 90, 130) if i % 2 else None)))(x, y, i)
    for (x, y, s) in ((300, 220, 1.0), (340, 190, 1.2)):
        m.add(x - 12, y - 12, x + 12, y + 12, 30, lambda lz, iso, x=x, y=y, s=s: O.maguey(lz, iso, x, y, s=s))
    for (x, y) in ((-70, 250), (-50, 262)):
        m.add(x - 10, y - 10, x + 10, y + 10, 50, lambda lz, iso, x=x, y=y: O.nopal(lz, iso, x, y))
    m.add(150, 100, 150, 100, 30, lambda lz, iso: O.fuente(lz, iso, 150, 100, t=t))
    for (x, y) in ((100, 70), (200, 70), (100, 140), (260, 120)):
        m.add(x - 3, y - 3, x + 3, y + 3, 40, lambda lz, iso, x=x, y=y: O.farol(lz, iso, x, y, t=t))
    m.add(260, 200, 262, 202, 30, lambda lz, iso: O.barril(lz, iso, 258, 200))
    m.add(266, 204, 268, 206, 30, lambda lz, iso: O.costal(lz, iso, 270, 204))
    # gente
    mu = G.Multitud()
    mu.camina([(40, 80), (140, 90), (200, 110), (270, 100)], "campesino", vel=14, seed=1, fase=0.0, bucle="ida_vuelta")
    mu.camina([(270, 110), (200, 125), (110, 120), (40, 100)], "campesina", vel=12, seed=2, fase=0.2, bucle="ida_vuelta")
    mu.camina([(100, 40), (110, 100), (120, 160), (130, 220)], "comerciante", vel=13, seed=3, fase=0.3, bucle="ida_vuelta")
    mu.camina([(180, 40), (170, 100), (160, 170)], "indigena", vel=11, seed=4, bucle="ida_vuelta")
    mu.camina([(30, 180), (110, 190), (180, 180), (250, 190)], "arriero", vel=10, seed=5, bucle="ida_vuelta")
    mu.quieto((120, 106), "cura", dir=(0, 1), seed=8, accion="habla")
    mu.quieto((128, 112), "campesino", dir=(-1, -0.2), seed=9, accion="habla")
    mu.quieto((176, 112), "dama", dir=(1, 0), seed=10)
    mu.quieto((184, 124), "nino", dir=(0, 1), seed=11, h=22)
    mu.quieto((206, 134), "comerciante", dir=(0, 1), seed=12, accion="saluda")
    mu.quieto((150, 135), "campesina", dir=(0, 1), seed=13)
    mu.quieto((90, 120), "noble", dir=(1, 0), seed=14)
    mu.quieto((98, 118), "dama", dir=(-1, 0), seed=15)
    mu.ronda((150, 100), 40, "campesino", n=6, seed=30)
    mu.ronda((200, 160), 30, "indigena_f", n=3, seed=60)
    mu.dibujar(m, t)
    # animales
    m.add(228, 178, 232, 182, 20, lambda lz, iso: O.chispas(lz, iso, 0, 0, 0, t, 0) if False else G.burro(lz, iso, 230, 180, t, dir=-1))
    for i in range(4):
        m.add(60 + i * 10, 200, 66 + i * 10, 206, 10, lambda lz, iso, i=i: G.oveja(lz, iso, 62 + i * 10 + 4 * math.sin(t + i), 202, t, 1, seed=i))
    for i in range(3):
        m.add(214 + i * 6, 190, 218 + i * 6, 194, 10, lambda lz, iso, i=i: G.gallina(lz, iso, 216 + i * 6, 192 + 3 * math.sin(t * 2 + i), t, -1 if i % 2 else 1, seed=i))
    return m


def suelo_pueblo(lz, iso):
    I.suelo_rect(lz, iso, -420, -420, 1100, 1100, (140, 190, 96))
    I.suelo_curvo(lz, iso, [(-70, -10), (340, -10), (350, 150), (330, 260), (-80, 270)], (206, 188, 128))
    I.suelo_curvo(lz, iso, [(70, 36), (290, 36), (300, 220), (60, 224)], (238, 224, 178))
    I.camino(lz, iso, [(-420, 150), (-200, 150), (-70, 150)], 40, (226, 206, 150))
    I.camino(lz, iso, [(110, 30), (118, 120), (130, 260), (136, 460)], 38, (226, 206, 150))
    I.cuadricula(lz, iso, 70, 36, 300, 220, 22, color=(255, 255, 255), alfa=0.16)


if __name__ == "__main__":
    nombre = sys.argv[1]
    zoom = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    t = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    lz = Lienzo()
    lz.nuevo(t, wob=0.0)
    iso = I.Iso(float(sys.argv[4]) if len(sys.argv) > 4 else 150, float(sys.argv[5]) if len(sys.argv) > 5 else 80, 20, zoom)
    I.luz()
    suelo_pueblo(lz, iso)
    m = escena(t)
    m.dibujar(lz, iso)
    bg = bg_grad((150, 214, 240), (230, 240, 250))
    img = componer(bg, lz.resolver(), boil=lz.boil)
    cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
    print("ok")
