# -*- coding: utf-8 -*-
"""Piezas de decorado de «Las 1.200» (pintadas UNA vez en gris con noir_fondos.Lienzo; el color lo pone noir_color.pegar con la
rampa de cada material). Aquí solo hay piezas parametrizadas; cada lugar se arma en mundos_1.py / mundos_2.py / mundos_3.py.

    muro(L, x0, y0, x1, y1, tipo)      ladrillo · azulejo · hormigon · paneles · tapiz · chapa · corcho · pizarra · celosia
    suelo(L, x0, x1, y0, y1, tipo, vp) baldosa · tablones · hormigon · rejilla (líneas hacia el punto de fuga vp)
    ventana · puerta · tuberias · estanteria · archivador · reja · barandilla · servidor · cartel · lampara · ciudad · cielo · agua
    superficie(tipo, sem)              superficie a pantalla completa para planos cerrados (mesa, metal, fieltro, barra, corcho…)
"""
import collections
import functools
import math

import cv2
import numpy as np

from noir_fondos import Lienzo, edificio, texto_lienzo


def _r(sem):
    return np.random.default_rng(sem)


_CACHE = collections.OrderedDict()
MAX_CACHE = 8


def mundo(fn):
    """Decorado pintado una vez y guardado en una caché COMÚN a todos los lugares (las 8 últimas capas): la memoria no crece
    aunque un proceso de render recorra muchas escenas."""
    @functools.wraps(fn)
    def f(*a):
        k = (fn.__name__,) + a
        if k in _CACHE:
            _CACHE.move_to_end(k)
            return _CACHE[k]
        v = fn(*a)
        _CACHE[k] = v
        while len(_CACHE) > MAX_CACHE:
            _CACHE.popitem(last=False)
        return v
    return f


# ====================================================================== muros
def muro(L, x0, y0, x1, y1, tipo="ladrillo", tono=0.30, sem=0, var=0.06, junta=0.10, grad=None, manchas=True):
    w, hh = x1 - x0, y1 - y0
    L.rect(x0, y0, w, hh, tono, tex=0.05, grad=grad)
    rng = _r(sem)
    if tipo == "ladrillo":
        bw, bh = 120, 46
        for j, y in enumerate(np.arange(y0, y1, bh)):
            off = (bw / 2) if j % 2 else 0
            for x in np.arange(x0 - off, x1, bw):
                v = tono * (1 + rng.uniform(-var, var) * 2)
                L.rect(x + 3, y + 3, bw - 6, bh - 6, v, tex=0.07, alfa=0.9)
            L.linea([(x0, y), (x1, y)], 2.0, junta, jit=0.4, alfa=0.7)
    elif tipo == "azulejo":
        s_ = 70
        for y in np.arange(y0, y1, s_):
            for x in np.arange(x0, x1, s_):
                v = tono * (1 + rng.uniform(-var, var))
                L.rect(x + 2, y + 2, s_ - 4, s_ - 4, v, tex=0.05, alfa=0.95)
        for y in np.arange(y0, y1, s_):
            L.linea([(x0, y), (x1, y)], 1.6, tono * 0.55, jit=0.2, alfa=0.8)
        for x in np.arange(x0, x1, s_):
            L.linea([(x, y0), (x, y1)], 1.6, tono * 0.55, jit=0.2, alfa=0.8)
    elif tipo == "hormigon":
        for y in np.arange(y0, y1, 300):
            L.linea([(x0, y), (x1, y)], 2.0, tono * 0.6, jit=0.3, alfa=0.6)
        for x in np.arange(x0, x1, 600):
            L.linea([(x, y0), (x, y1)], 2.0, tono * 0.6, jit=0.3, alfa=0.5)
            for yy in np.arange(y0 + 150, y1, 300):
                for dx in (60, 540):
                    L.elipse(x + dx, yy, 6, 6, tono * 0.5, alfa=0.7)
    elif tipo == "paneles":
        pw = 160
        for x in np.arange(x0, x1, pw):
            L.rect(x + 4, y0, pw - 8, hh, tono * (1 + rng.uniform(-var, var)), tex=0.08, alfa=0.9)
            L.linea([(x, y0), (x, y1)], 2.4, tono * 0.4, alfa=0.8)
            for k in range(3):
                xx = x + rng.uniform(20, pw - 20)
                L.linea([(xx, y0), (xx + rng.uniform(-8, 8), y1)], 1.0, tono * 0.75, alfa=0.4, jit=1.4)
    elif tipo == "tapiz":
        for x in np.arange(x0, x1, 90):
            L.rect(x, y0, 40, hh, tono * 1.15, tex=0.08, alfa=0.6)
            for y in np.arange(y0 + 40, y1, 120):
                L.elipse(x + 65, y, 12, 18, tono * 1.25, alfa=0.5)
    elif tipo == "chapa":
        pw, ph = 400, 260
        for y in np.arange(y0, y1, ph):
            for x in np.arange(x0, x1, pw):
                L.rect(x + 3, y + 3, pw - 6, ph - 6, tono * (1 + rng.uniform(-var, var)), tex=0.05, alfa=0.9)
                for cx in np.arange(x + 16, x + pw, 48):
                    L.elipse(cx, y + 14, 3.5, 3.5, tono * 1.5, alfa=0.8)
                    L.elipse(cx, y + ph - 14, 3.5, 3.5, tono * 1.5, alfa=0.8)
    elif tipo == "corcho":
        for k in range(int(w * hh / 900)):
            L.elipse(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(2, 6), rng.uniform(2, 5), tono * rng.uniform(0.6, 1.4),
                     alfa=0.6, blur=0.4, tex=0)
    elif tipo == "pizarra":
        L.rect(x0, y0, w, hh, tono, tex=0.25)
        for k in range(18):                                          # restos de tiza borrada
            cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
            L.elipse(cx, cy, rng.uniform(80, 260), rng.uniform(20, 60), tono * 1.5, alfa=0.18, rug=1.2, blur=8)
    elif tipo == "celosia":
        for x in np.arange(x0, x1, 40):
            L.linea([(x, y0), (x + hh, y1)], 3, tono * 0.5, alfa=0.6, jit=0.2)
            L.linea([(x, y0), (x - hh, y1)], 3, tono * 0.5, alfa=0.6, jit=0.2)
    if manchas and tipo not in ("pizarra", "corcho"):
        for k in range(max(3, int(w / 500))):                        # humedad y suciedad
            cx = rng.uniform(x0, x1)
            L.elipse(cx, rng.uniform(y0, y1), rng.uniform(60, 220), rng.uniform(80, 300), tono * 0.7, alfa=0.12, rug=1.5, blur=12)


# ====================================================================== suelos
def suelo(L, x0, x1, y0, y1, tipo="baldosa", tono=0.24, sem=0, vp=None, paso=140):
    """Suelo de y0 (horizonte del suelo) a y1. vp = punto de fuga (x, y) para las juntas que convergen."""
    L.rect(x0, y0, x1 - x0, y1 - y0, tono, tex=0.06, grad=(tono * 0.7, y0, y1))
    rng = _r(sem)
    vpx, vpy = vp if vp is not None else ((x0 + x1) / 2, y0 - 900)
    if tipo in ("baldosa", "tablones", "rejilla"):
        n = int((x1 - x0) * 2.5 / paso)
        for k in range(-n, n + 1):
            xb = (x0 + x1) / 2 + k * paso * 2.2
            t0 = (y0 - vpy) / max(1.0, y1 - vpy)
            xa = vpx + (xb - vpx) * t0
            L.linea([(xa, y0), (xb, y1)], 1.8 if tipo != "rejilla" else 2.6, tono * 0.5, jit=0.3, alfa=0.7)
        if tipo != "tablones":
            y = y0
            gap = 10.0
            while y < y1:
                L.linea([(x0, y), (x1, y)], 1.8, tono * 0.5, jit=0.3, alfa=0.7)
                gap *= 1.32
                y += gap
    elif tipo == "hormigon":
        for k in range(14):
            L.elipse(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(80, 300), rng.uniform(10, 40), tono * 0.75, alfa=0.15,
                     rug=1.2, blur=6)
        for k in range(6):
            x = rng.uniform(x0, x1)
            L.linea([(x, y1), (x + rng.uniform(-200, 200), y0 + (y1 - y0) * rng.uniform(0.2, 0.6))], 1.4, tono * 0.5, alfa=0.5, jit=2.0)


# ====================================================================== aberturas
def ventana(L, x, y, w, hh, tono=0.20, persiana=0.0, noche=True, luna=None, ciudad=True, sem=0, cristal=0.10, marco=0.16,
            encendidas=0.25):
    """Ventana con marco; dentro: cielo nocturno con siluetas de ciudad y ventanas encendidas (emisión). persiana 0..1 = lamas."""
    L.rect(x - 18, y - 18, w + 36, hh + 36, marco, tex=0.1)
    L.rect(x, y, w, hh, cristal, tex=0.05, grad=(cristal * 1.8, y, y + hh))
    rng = _r(sem)
    if ciudad:
        xx = x
        while xx < x + w:
            bw = rng.uniform(40, 110)
            bh = rng.uniform(hh * 0.25, hh * 0.85)
            L.rect(xx, y + hh - bh, min(bw, x + w - xx), bh, 0.06, tex=0.1)
            for wy in np.arange(y + hh - bh + 12, y + hh - 8, 22):
                for wx in np.arange(xx + 8, min(xx + bw, x + w) - 8, 18):
                    if rng.uniform() < encendidas:
                        L.rect(wx, wy, 7, 10, 0.85, tex=0.0, emis=0.7)
            xx += bw + rng.uniform(2, 14)
    if luna is not None:
        L.elipse(luna[0], luna[1], 26, 26, 0.95, emis=0.6)
    if persiana > 0:
        n = int(hh / 26)
        for k in range(n):
            yy = y + k * 26
            L.rect(x, yy, w, 26 * persiana * 0.7, 0.30, tex=0.06, alfa=0.95)
            L.linea([(x, yy), (x + w, yy)], 1.4, 0.12, alfa=0.7)
        for cx in (x + w * 0.25, x + w * 0.75):
            L.linea([(cx, y), (cx, y + hh)], 1.2, 0.5, alfa=0.5)
    L.linea([(x, y), (x + w, y), (x + w, y + hh), (x, y + hh)], 3.0, 0.03, cerrado=True)
    L.linea([(x + w / 2, y), (x + w / 2, y + hh)], 6.0, marco)
    L.linea([(x, y + hh / 2), (x + w, y + hh / 2)], 6.0, marco)


def puerta(L, x, y, w, hh, tono=0.22, vidrio=False, texto=None, px=34, marco=0.12, sem=0, metal=False):
    L.rect(x - 20, y - 20, w + 40, hh + 20, marco, tex=0.12)
    L.rect(x, y, w, hh, tono, tex=0.18 if not metal else 0.08)
    if metal:
        for yy in (y + 60, y + hh - 80):
            L.rect(x + 10, yy, w - 20, 16, tono * 1.3, alfa=0.7)
        for cx in np.arange(x + 20, x + w, 50):
            for cy in (y + 24, y + hh - 24):
                L.elipse(cx, cy, 4, 4, tono * 1.6)
    else:
        L.rect(x + 30, y + hh * 0.55, w - 60, hh * 0.38, tono * 0.85, tex=0.2)
    if vidrio:
        L.rect(x + 34, y + 40, w - 68, hh * 0.36, 0.45, tex=0.25)
        if texto:
            texto_lienzo(L, texto, x + w / 2, y + 40 + hh * 0.18, px, tono=0.06)
    L.elipse(x + w - 40, y + hh * 0.56, 12, 12, 0.6)
    L.linea([(x, y), (x + w, y), (x + w, y + hh), (x, y + hh)], 3.0, 0.03, cerrado=True)


def reja(L, x0, x1, y0, y1, sep=60, w=14, tono=0.12, travesanos=(0.12, 0.88)):
    for x in np.arange(x0, x1 + 1, sep):
        L.rect(x - w / 2, y0, w, y1 - y0, tono, tex=0.05)
        L.linea([(x + w / 2 - 2, y0), (x + w / 2 - 2, y1)], 1.6, tono * 3.5, alfa=0.6, jit=0.2)
    for f in travesanos:
        y = y0 + (y1 - y0) * f
        L.rect(x0 - 10, y - 10, x1 - x0 + 20, 20, tono * 1.2, tex=0.05)


def barandilla(L, x0, x1, y, alto=110, sep=40, tono=0.14):
    L.rect(x0, y - alto - 8, x1 - x0, 12, tono * 1.4, tex=0.05)
    L.rect(x0, y - alto * 0.5, x1 - x0, 6, tono, tex=0.05)
    for x in np.arange(x0, x1, sep):
        L.rect(x, y - alto, 5, alto, tono, tex=0.05)


# ====================================================================== instalaciones
def tuberias(L, x0, x1, y, n=3, sep=34, tono=0.22, sem=0, valvulas=True):
    rng = _r(sem)
    for k in range(n):
        yy = y + k * sep
        r = 10 + (k % 2) * 4
        L.rect(x0, yy - r, x1 - x0, 2 * r, tono * (1 + 0.1 * k), tex=0.1)
        L.linea([(x0, yy - r + 3), (x1, yy - r + 3)], 2.0, min(0.9, tono * 2.4), alfa=0.6, jit=0.3)
        for x in np.arange(x0 + rng.uniform(40, 200), x1, rng.uniform(260, 420)):
            L.rect(x - 6, yy - r - 4, 12, 2 * r + 8, tono * 1.3)
        if valvulas:
            vx = rng.uniform(x0 + 100, x1 - 100)
            L.elipse(vx, yy - r - 22, 22, 6, tono * 1.4)
            L.rect(vx - 3, yy - r - 22, 6, 22, tono * 1.2)


def conducto(L, x, y0, y1, r=16, tono=0.22):
    L.rect(x - r, y0, 2 * r, y1 - y0, tono, tex=0.1)
    L.linea([(x - r + 4, y0), (x - r + 4, y1)], 2.0, min(0.9, tono * 2.4), alfa=0.6)
    for y in np.arange(y0 + 80, y1, 260):
        L.rect(x - r - 5, y, 2 * r + 10, 12, tono * 1.3)


def estanteria(L, x, base, w, hh, niveles=5, tono=0.18, cajas=True, sem=0, rotulos=False, tono_caja=0.34):
    rng = _r(sem)
    for xx in (x, x + w - 14):
        L.rect(xx, base - hh, 14, hh, tono, tex=0.1)
    paso = hh / niveles
    for k in range(niveles + 1):
        y = base - k * paso
        L.rect(x, y - 8, w, 10, tono * 1.2, tex=0.1)
        if cajas and k < niveles:
            xx = x + 20
            while xx < x + w - 40:
                bw = rng.uniform(60, 150)
                bh = rng.uniform(paso * 0.45, paso * 0.85)
                if xx + bw > x + w - 20:
                    break
                v = tono_caja * rng.uniform(0.7, 1.2)
                L.rect(xx, y - 8 - bh, bw, bh, v, tex=0.25)
                L.linea([(xx, y - 8 - bh), (xx + bw, y - 8 - bh), (xx + bw, y - 8), (xx, y - 8)], 1.6, 0.04, cerrado=True, alfa=0.8)
                if rotulos and bw > 90:
                    L.rect(xx + bw * 0.2, y - 8 - bh * 0.6, bw * 0.6, bh * 0.22, 0.7, alfa=0.85)
                xx += bw + rng.uniform(4, 20)


def archivador(L, x, base, w=220, hh=560, cajones=4, tono=0.28):
    L.rect(x, base - hh, w, hh, tono, tex=0.1)
    ch = hh / cajones
    for k in range(cajones):
        y = base - hh + k * ch
        L.rect(x + 12, y + 10, w - 24, ch - 20, tono * 1.15, tex=0.08)
        L.rect(x + w / 2 - 34, y + ch * 0.35, 68, 14, 0.6)
        L.rect(x + w / 2 - 28, y + ch * 0.18, 56, 20, 0.75, alfa=0.8)
        L.linea([(x + 12, y + 10), (x + w - 12, y + 10)], 1.6, 0.04, alfa=0.8)
    L.linea([(x, base - hh), (x + w, base - hh), (x + w, base), (x, base)], 2.4, 0.03, cerrado=True)


def servidor(L, x, base, w=200, hh=700, tono=0.10, sem=0, leds=0.35):
    """Bastidor de servidores con unidades y luces (emisión)."""
    rng = _r(sem)
    L.rect(x, base - hh, w, hh, tono, tex=0.08)
    for y in np.arange(base - hh + 20, base - 20, 34):
        L.rect(x + 10, y, w - 20, 28, tono * 1.6, tex=0.06)
        L.linea([(x + 10, y + 28), (x + w - 10, y + 28)], 1.2, 0.02, alfa=0.8)
        for k in range(6):
            if rng.uniform() < leds:
                cx = x + 24 + k * 14
                L.elipse(cx, y + 14, 3, 3, 0.95, emis=0.8)
        L.rect(x + w - 70, y + 8, 50, 12, tono * 0.6)
    L.linea([(x, base - hh), (x + w, base - hh), (x + w, base), (x, base)], 2.4, 0.02, cerrado=True)


def cartel(L, x, y, w, hh, texto, px=40, tono=0.75, tinta=0.06, fuente="C:/Windows/Fonts/impact.ttf", sub=None, sem=0, rot_=0.0):
    L.rect(x, y, w, hh, tono, tex=0.2)
    L.linea([(x, y), (x + w, y), (x + w, y + hh), (x, y + hh)], 2.0, 0.05, cerrado=True)
    texto_lienzo(L, texto, x + w / 2, y + hh * (0.38 if sub else 0.5), px, tono=tinta, fuente=fuente)
    if sub:
        texto_lienzo(L, sub, x + w / 2, y + hh * 0.72, px * 0.45, tono=tinta, fuente="C:/Windows/Fonts/courbd.ttf")


def lampara(L, x, y_techo, largo=200, ancho=120, tono=0.12, enc=True):
    """Lámpara industrial colgante (pantalla cónica); la luz se pone por cuadro."""
    L.linea([(x, y_techo), (x, y_techo + largo)], 2.4, 0.05)
    L.poli([(x - 18, y_techo + largo), (x + 18, y_techo + largo), (x + ancho / 2, y_techo + largo + ancho * 0.45),
            (x - ancho / 2, y_techo + largo + ancho * 0.45)], tono, tex=0.08)
    if enc:
        L.elipse(x, y_techo + largo + ancho * 0.45, ancho * 0.36, 9, 0.95, emis=0.9)


# ====================================================================== exteriores
def cielo(L, x0, y0, x1, y1, tono=0.10, sem=0, estrellas=120, nubes=20, luna=None):
    L.rect(x0, y0, x1 - x0, y1 - y0, tono * 0.5, tex=0.06, grad=(tono * 1.6, y0, y1))
    rng = _r(sem)
    for k in range(nubes):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y0 + (y1 - y0) * 0.75)
        rx, ry = rng.uniform(160, 480), rng.uniform(20, 60)
        L.elipse(cx, cy, rx, ry, tono * rng.uniform(1.4, 2.4), alfa=0.45, rug=1.4, blur=10, tex=0.15)
    for k in range(estrellas):
        L.elipse(rng.uniform(x0, x1), rng.uniform(y0, y0 + (y1 - y0) * 0.6), 1.3, 1.3, rng.uniform(0.5, 0.9), tex=0, blur=0.4,
                 alfa=rng.uniform(0.3, 0.8))
    if luna is not None:
        L.elipse(luna[0], luna[1], 46, 46, 0.95, tex=0.0, emis=0.6)
        L.brillo(luna[0], luna[1], 260, 0.3, tono=0.8)


def ciudad(L, x0, x1, base, alto=(300, 900), sem=0, encendidas=0.22, tipos=("ladrillo", "deco", "cristal"), detalle=0.7,
           tono=None):
    rng = _r(sem)
    x = x0
    while x < x1:
        an = rng.uniform(160, 340)
        al = rng.uniform(*alto)
        edificio(L, x, base, an, al, tipo=str(rng.choice(tipos)), sem=int(rng.integers(9999)), encendidas=encendidas, detalle=detalle)
        x += an + rng.uniform(4, 40)


def agua(L, x0, x1, y0, y1, tono=0.10, sem=0, reflejos=40):
    L.rect(x0, y0, x1 - x0, y1 - y0, tono, tex=0.1, grad=(tono * 0.6, y0, y1))
    rng = _r(sem)
    for k in range(reflejos):
        y = rng.uniform(y0, y1)
        x = rng.uniform(x0, x1)
        L.rect(x, y, rng.uniform(40, 200), 2.5, tono * 3.0, alfa=0.5)


def colinas(L, x0, x1, base, alto=260, tono=0.08, sem=0, n=5):
    rng = _r(sem)
    P = [(x0, base)]
    for x in np.linspace(x0, x1, 40):
        y = base - alto * (0.5 + 0.5 * math.sin(x * 0.0021 + sem) * math.sin(x * 0.0007 + 1.3))
        P.append((x, y))
    P.append((x1, base))
    L.poli(P, tono, tex=0.15)


def niebla_banda(L, x0, x1, y, alto, tono=0.5, alfa=0.4, sem=0, n=24):
    rng = _r(sem)
    for k in range(n):
        L.elipse(rng.uniform(x0, x1), y + rng.uniform(-alto / 2, alto / 2), rng.uniform(200, 600), rng.uniform(20, alto * 0.5), tono,
                 alfa=alfa * rng.uniform(0.4, 1.0), rug=1.2, blur=14, tex=0.1)


# ====================================================================== superficies (planos cerrados)
@mundo
def superficie(tipo="madera", sem=1, w=2800, hh=1700):
    """Superficie a pantalla completa (un poco mayor que la pantalla) para planos cerrados de objetos sobre una mesa / suelo /
    pared. tipo: madera · metal · fieltro · barra · corcho · hormigon · papel · pizarra · cuero."""
    ox, oy = -(w - 1920) / 2, -(hh - 1080) / 2
    L = Lienzo(w, hh, origen=(ox, oy), base=0.2, sem=sem)
    rng = _r(sem)
    x0, y0, x1, y1 = ox, oy, ox + w, oy + hh
    if tipo == "madera":
        L.rect(x0, y0, w, hh, 0.36, tex=0.08)
        for k in range(160):
            y = rng.uniform(y0, y1)
            L.linea([(x0, y), (x1, y + rng.uniform(-30, 30))], rng.uniform(1.0, 3.0), 0.36 * rng.uniform(0.6, 0.85), alfa=0.5, jit=3.0)
        for k in range(6):
            L.elipse(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(30, 70), rng.uniform(8, 16), 0.22, alfa=0.5, blur=2)
        for y in np.arange(y0, y1, 260):
            L.linea([(x0, y), (x1, y)], 3.0, 0.12, alfa=0.8)
    elif tipo == "metal":
        L.rect(x0, y0, w, hh, 0.34, tex=0.1)
        for k in range(300):
            y = rng.uniform(y0, y1)
            x = rng.uniform(x0, x1)
            L.linea([(x, y), (x + rng.uniform(40, 300), y + rng.uniform(-3, 3))], 0.8, 0.5, alfa=0.25, jit=0.2)
        for k in range(8):
            L.elipse(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(60, 200), rng.uniform(40, 140), 0.28, alfa=0.15, rug=1.3, blur=8)
    elif tipo == "fieltro":
        L.rect(x0, y0, w, hh, 0.30, tex=0.12)
    elif tipo == "barra":
        L.rect(x0, y0, w, hh, 0.26, tex=0.08)
        for k in range(120):
            y = rng.uniform(y0, y1)
            L.linea([(x0, y), (x1, y + rng.uniform(-20, 20))], rng.uniform(1, 2.5), 0.2, alfa=0.45, jit=2.5)
        for k in range(7):                                           # cercos de vasos
            cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
            L.elipse(cx, cy, 56, 56, 0.16, alfa=0.35)
            L.elipse(cx, cy, 48, 48, 0.26, alfa=0.5)
    elif tipo == "corcho":
        L.rect(x0, y0, w, hh, 0.40, tex=0.1)
        muro(L, x0, y0, x1, y1, "corcho", 0.40, sem=sem)
        L.rect(x0, y0, w, 60, 0.30, tex=0.15)
        L.rect(x0, y1 - 60, w, 60, 0.30, tex=0.15)
    elif tipo == "hormigon":
        L.rect(x0, y0, w, hh, 0.30, tex=0.1)
        suelo(L, x0, x1, y0, y1, "hormigon", 0.30, sem=sem)
    elif tipo == "papel":
        L.rect(x0, y0, w, hh, 0.72, tex=0.15)
    elif tipo == "pizarra":
        muro(L, x0, y0, x1, y1, "pizarra", 0.12, sem=sem)
        L.rect(x0, y1 - 80, w, 80, 0.30, tex=0.2)
    elif tipo == "cuero":
        L.rect(x0, y0, w, hh, 0.22, tex=0.12)
        for k in range(30):
            L.linea([(rng.uniform(x0, x1), rng.uniform(y0, y1)), (rng.uniform(x0, x1), rng.uniform(y0, y1))], 1.0, 0.3, alfa=0.2,
                    jit=3.0)
    return L.capa(opaco=True)
