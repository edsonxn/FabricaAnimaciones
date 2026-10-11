# -*- coding: utf-8 -*-
"""Prueba 3: alhóndiga + asedio, habitación en corte e isla flotante. python _iso_test3.py nombre modo [zoom] [t] [cx] [cy]"""
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
import kz_iso_arq2 as B
import kz_gente_iso as G
from util import bg_grad


def asedio(t):
    m = I.Mundo()
    tf = lambda: t
    B.alhondiga(m, 20, -140, w=170, d=130, h=84, t_fn=tf, puerta_fuego=1.0, bandera_luto=False)
    for i in range(5):
        (lambda i: m.add(30 + i * 30, -144, 40 + i * 30, -134, 40, lambda lz, iso: G.persona(lz, iso, 40 + i * 30, -138, t, "realista", dir=(0, 1), seed=i, accion="pelea", z=84)))(i)
    B.canon(m, 40, 100, dir=1, t_fn=tf, disparo=(t % 3.0))
    B.canon(m, 130, 120, dir=1, t_fn=tf, disparo=((t + 1.2) % 3.0))
    B.tienda_campana(m, -40, 60, bandera=(60, 160, 100), t_fn=tf)
    B.tienda_campana(m, -30, 110, color=(240, 226, 200), bandera=(220, 80, 80), t_fn=tf)
    for i, (x, y) in enumerate(((0, 20), (230, 30), (250, 100), (-20, 150), (200, 170), (80, 190))):
        (lambda x, y, i: m.add(x - 12, y - 12, x + 12, y + 12, 60, lambda lz, iso: O.arbol(lz, iso, x, y, h=50, seed=i, t=t)))(x, y, i)
    mu = G.Multitud()
    for i in range(34):
        fila = i // 11
        mu.camina([(40 + (i % 11) * 14, 160 + fila * 16), (40 + (i % 11) * 14 + 6, 10 + fila * 16)], "insurgente", vel=9 + (i % 5), seed=i + 100, fase=0.0, bucle="ida_vuelta", accion=None)
    for i in range(10):
        mu.quieto((60 + i * 14, 40 + (i % 3) * 8), "honda", dir=(0, -1), seed=300 + i, accion="pelea")
    mu.quieto((100, -20), "minero", dir=(0, -1), seed=900, accion="carga")
    mu.dibujar(m, t)
    m.add(120, 180, 126, 186, 30, lambda lz, iso: O.bandera(lz, iso, 124, 184, h=70, w=36, alto=24, color=(70, 150, 180), t=t))
    return m


def sala(t):
    m = I.Mundo()
    return m


def dib_sala(lz, iso, t):
    c = I.habitacion(lz, iso, 0, 0, 220, 190, 120, piso=(170, 112, 80), pared_a=(246, 226, 188))
    B.cuadro_pared(lz, iso, c, "yi", 20, 56, 40, 30, (110, 150, 200))
    B.cuadro_pared(lz, iso, c, "yi", 150, 60, 36, 28, (200, 120, 100))
    I.cara_rect(lz, iso, c, "yi", 80, 120, 40, 96, (150, 200, 230))
    I.cara_rect(lz, iso, c, "yi", 78, 82, 38, 98, (150, 100, 76))
    I.cara_rect(lz, iso, c, "yi", 118, 122, 38, 98, (150, 100, 76))
    B.estante(lz, iso, 6, 120, w=10, d=50, h=70) if False else None
    B.alfombra(lz, iso, 30, 40, 150, 120, (190, 70, 70))
    m = I.Mundo()
    m.add(60, 70, 140, 110, 30, lambda lz, iso: B.mesa(lz, iso, 60, 70, 80, 40, 18, mantel=(250, 240, 220)))
    for (x, y) in ((70, 56), (96, 56), (122, 56), (70, 112), (100, 112), (130, 112)):
        m.add(x, y, x + 10, y + 10, 14, lambda lz, iso, x=x, y=y: B.silla(lz, iso, x, y))
    m.add(88, 80, 90, 82, 40, lambda lz, iso: B.candelabro(lz, iso, 100, 88, 18, t))
    mu = G.Multitud()
    mu.quieto((80, 72), "oficial", dir=(1, 1), seed=1, accion="habla")
    mu.quieto((108, 70), "dama", dir=(0, 1), seed=2)
    mu.quieto((134, 74), "noble", dir=(-1, 0.5), seed=3, accion="habla")
    mu.quieto((110, 124), "oficial", dir=(0, -1), seed=4)
    mu.dibujar(m, t)
    return m


if __name__ == "__main__":
    nombre, modo = sys.argv[1], sys.argv[2]
    zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 1.6
    t = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    cx = float(sys.argv[5]) if len(sys.argv) > 5 else 100
    cy = float(sys.argv[6]) if len(sys.argv) > 6 else 0
    lz = Lienzo()
    lz.nuevo(t, wob=0.0)
    iso = I.Iso(cx, cy, 30, zoom)
    I.luz()
    if modo == "asedio":
        I.suelo_rect(lz, iso, -300, -300, 900, 900, (150, 190, 100))
        I.suelo_rect(lz, iso, 20, -140, 170, 150, (206, 190, 150))
        I.camino(lz, iso, [(100, 20), (110, 100), (100, 300)], 46, (230, 208, 150))
        asedio(t).dibujar(lz, iso)
        bg = bg_grad((150, 214, 240), (230, 240, 250))
    elif modo == "sala":
        dib = dib_sala(lz, iso, t)
        # el suelo fuera de la habitación: nada; fondo cálido
        dib.dibujar(lz, iso)
        bg = bg_grad((60, 40, 90), (120, 70, 90))
    else:
        I.isla(lz, iso, 0, 0, 200, 200, t=t)
        A.casa_colonial(m := I.Mundo(), 30, 30, 70, 50, 50)
        m.dibujar(lz, iso)
        bg = bg_grad((30, 20, 80), (90, 40, 110))
    img = componer(bg, lz.resolver(), boil=lz.boil)
    cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
    print("ok")
