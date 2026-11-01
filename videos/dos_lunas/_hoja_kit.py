# -*- coding: utf-8 -*-
"""Hoja de prueba del kit espacial (nucleo/kz_espacio.py). Uso (desde esta carpeta):
   $env:PYTHONPATH = "C:\\FabricaAnimaciones\\nucleo"; python _hoja_kit.py [t]
Escribe previews/kit_1..6.jpg (1920x1080) y previews/kit_hoja.jpg (2x3)."""
import math
import os
import sys

import cv2
import numpy as np

import estilos
import motor
from motor import Lienzo, componer, W, H
import plano as P
import kz_espacio as K

estilos.activar("kurzgesagt")
SAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews")
os.makedirs(SAL, exist_ok=True)
t = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0


def cuadro(fn, nombre, bg=None):
    lz = Lienzo()
    lz.nuevo(t, wob=0.0)
    bgi = K.fondo_espacio(t) if bg is None else bg
    fn(lz)
    img = componer(bgi, lz.resolver(), boil=lz.boil)
    im8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(SAL, nombre), cv2.cvtColor(im8, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    return im8


def p1(lz):   # galería de cuerpos rocosos
    tipos = ["luna", "ceniza", "rojiza", "hielo", "volcanica", "mercurio", "oscura"]
    for i, tp in enumerate(tipos):
        K.cuerpo_rocoso(lz, 190 + i * 240, 300, 95, tp, seed=i + 1, rot=t * 0.3, ang_luz=math.pi * 1.25)
    for i in range(5):
        K.roca(lz, 220 + i * 330, 560, 52 + 10 * (i % 2), seed=i + 4, rot=t * 0.6 + i, tipo="ceniza")
    for i, ph in enumerate([0.0, 0.2, 0.5, 0.8, 1.0]):
        K.cuerpo_rocoso(lz, 260 + i * 350, 820, 100, "luna", seed=3, ang_luz=0.0, fase=ph)
    P.rotulo(lz, 960, 60, "Lunas, rocas y fases", px=54)


def p2(lz):   # gigantes + anillos
    K.nebulosa(lz, 600, 400, 700, (150, 80, 220), seed=2, alfa=0.55)
    K.anillo(lz, 540, 540, 190, 380, tilt=-0.28, incl=0.28, mitad=0, col=(226, 204, 150))
    K.planeta_gas(lz, 540, 540, 150, t, "saturno", seed=2)
    K.anillo(lz, 540, 540, 190, 380, tilt=-0.28, incl=0.28, mitad=1, col=(226, 204, 150))
    K.planeta_gas(lz, 1250, 400, 170, t, "jupiter", seed=5)
    K.planeta_gas(lz, 1620, 760, 120, t, "hielo", seed=8, tormenta=False)
    K.planeta_gas(lz, 1000, 840, 80, t, "violeta", seed=3)
    K.destello(lz, 1700, 160, 40, t)


def p3(lz):   # órbitas, Hill, Lagrange
    ex, ey = 700, 560
    K.esfera_hill(lz, ex, ey, 480, t)
    K.orbita(lz, ex, ey, 300, 300, 0, (160, 180, 255), 3, fase=t * 25)
    th = t * 0.6
    mx, my = K.pos_orbita(ex, ey, 300, 300, 0, th)
    K.estela(lz, ex, ey, 300, 300, 0, th, largo=1.0)
    P.tierra(lz, ex, ey, 75, t, rot=t * 0.4, ang_luz=math.pi)
    K.cuerpo_rocoso(lz, mx, my, 34, "luna", seed=1, ang_luz=math.atan2(ey - my, ex - mx) + math.pi)
    l4 = K.pos_orbita(ex, ey, 300, 300, 0, th + math.pi / 3)
    K.triangulo_equilibrio(lz, (ex, ey), (mx, my), l4, t, frac=0.8 + 0.2 * math.sin(t))
    K.punto_lagrange(lz, l4[0], l4[1], "L4", t)
    K.cuerpo_rocoso(lz, l4[0], l4[1], 22, "ceniza", seed=9)
    K.regla(lz, (ex, ey + 400), (ex + 300, ey + 400), "384 400 km", px=32)
    K.etiqueta(lz, ex + 150, ey - 330, "Esfera de Hill", dx=240, dy=-20, px=32)
    P.kuri(lz, 1500, 900, 1.2, t, mirar=(-0.6, -0.3))


def p4(lz):   # marea: Tierra con dos lunas
    ex, ey = 960, 540
    lunas = [(0.35, 1.0), (math.pi * 0.9, 0.75)]
    K.tierra_marea(lz, ex, ey, 230, t, lunas, rot=t * 0.3, amp=0.2)
    for (a, f), tp, sd in zip(lunas, ("luna", "ceniza"), (1, 4)):
        px, py = ex + math.cos(a) * 640, ey + math.sin(a) * 640
        K.cuerpo_rocoso(lz, px, py, 60 * f ** 0.5 + 10, tp, seed=sd, ang_luz=math.pi)
        K.flechas_marea(lz, ex, ey, 230, a, f, t=t)


def p5(lz):   # luna rota + anillo + lluvia
    ex, ey = 520, 620
    K.anillo_escombros(lz, ex, ey, 360, 560, t, n=140, seed=3, incl=0.3, mitad=0, tam=9)
    P.tierra(lz, ex, ey, 230, t, rot=t * 0.3, ang_luz=math.pi)
    K.anillo_escombros(lz, ex, ey, 360, 560, t, n=140, seed=3, incl=0.3, mitad=1, tam=9)
    K.lluvia_rocas(lz, t, ex, ey, 230, n=14, seed=2)
    K.luna_rota(lz, 1400, 300, 85, 0.6, math.atan2(ey - 300, ex - 1400), t, seed=2, rompe=0.0)
    K.luna_rota(lz, 1300, 780, 85, 1.0, math.atan2(ey - 780, ex - 1300), t, seed=2, rompe=0.75)


def p6(lz):   # Marte y Fobos / Hill grande
    K.cuerpo_rocoso(lz, 700, 560, 220, "rojiza", seed=6, ang_luz=math.pi * 1.2)
    K.orbita(lz, 700, 560, 420, 330, 0.2, (255, 190, 150), 3, fase=t * 20)
    a = t * 1.1
    x, y = K.pos_orbita(700, 560, 420, 330, 0.2, a)
    K.estela(lz, 700, 560, 420, 330, 0.2, a, color=(255, 210, 170), largo=1.2)
    K.roca(lz, x, y, 42, seed=7, rot=t, tipo="mercurio")
    K.flecha(lz, (x, y), (x - 160, y + 120), (255, 214, 90), 6)
    K.regla(lz, (1300, 300), (1700, 300), "6 000 km", px=34)
    P.tierra(lz, 1500, 760, 160, t, rot=t * 0.2, ang_luz=math.pi)


paneles = [("kit_1.jpg", p1), ("kit_2.jpg", p2), ("kit_3.jpg", p3), ("kit_4.jpg", p4), ("kit_5.jpg", p5), ("kit_6.jpg", p6)]
ims = []
for nom, fn in paneles:
    ims.append(cuadro(fn, nom))
    print("ok", nom)
chicos = [cv2.resize(i, (960, 540), interpolation=cv2.INTER_AREA) for i in ims]
hoja = np.vstack([np.hstack(chicos[:2]), np.hstack(chicos[2:4]), np.hstack(chicos[4:6])])
cv2.imwrite(os.path.join(SAL, "kit_hoja.jpg"), cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
