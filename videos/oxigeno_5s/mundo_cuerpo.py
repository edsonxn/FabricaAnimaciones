# -*- coding: utf-8 -*-
"""Dentro de la protagonista (versión A, segundo 2): se entra por un portal en el pecho y se sale por la cabeza.
  1) vaso sanguíneo: glóbulos rojos que llevan O2 (Kuri va montado en uno); el O2 desaparece y se oscurecen.
  2) una célula: mitocondrias que queman glucosa con O2 y llenan una pila; sin O2, la pila se vacía.
  3) zoom hacia fuera: la célula es una neurona del cerebro; el cerebro gasta 20 % de la energía; experimento de 1943:
     se corta el riego y el cronómetro marca 6-7 s hasta perder el conocimiento; 5 s está al borde.
Coordenadas propias (px a z = 1) con una cámara de claves (ancla, zoom en escala log)."""
import math

import numpy as np

import fondos as F
import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from mundo_comun import pop, ventana, campana, kf
from anclas import A, PORTAL_IN, PORTAL_OUT
import kit_oxi as KO
import kit_bio as KB

V_FLUJO = 260.0                 # velocidad de la sangre (u/s)
X_CEL = 4300.0                  # centro de la célula
BC = np.array([X_CEL - 2600.0, 1900.0])   # centro del cerebro (en el que la célula es una neurona)
S_CER = 60.0                    # escala del cerebro


def _ancla_vaso(t):
    return np.array([V_FLUJO * 0.55 * (t - PORTAL_IN[0]), 0.0])


def cam(t):
    """(ancla, zoom)."""
    t_cel0, t_cel1 = A.celulas - 0.5, A.celulas + 0.8
    t_cer0, t_cer1 = A.cerebro - 1.3, A.cerebro + 0.5
    if t < t_cel0:
        a, z = _ancla_vaso(t), 1.0
        if t < PORTAL_IN[1]:
            z = math.exp(lerp(math.log(0.35), 0.0, e_out(prog(t, PORTAL_IN[0], PORTAL_IN[1]))))
        return a, z
    if t < t_cel1:
        u = e_inout(prog(t, t_cel0, t_cel1))
        a0 = _ancla_vaso(t_cel0)
        return a0 + (np.array([X_CEL, 0.0]) - a0) * u, lerp(1.0, 0.78, u)
    if t < t_cer0:
        return np.array([X_CEL, 0.0]), 0.78 + 0.02 * prog(t, t_cel1, t_cer0)
    if t < t_cer1:
        u = e_inout(prog(t, t_cer0, t_cer1))
        z = math.exp(lerp(math.log(0.8), math.log(0.055), u))
        a = np.array([X_CEL, 0.0]) + (BC + np.array([-500.0, -600.0]) - np.array([X_CEL, 0.0])) * e_in(u) ** 0.6
        return a, z
    z = 0.055 + 0.004 * prog(t, t_cer1, PORTAL_OUT[0])
    if t > PORTAL_OUT[0]:
        z = math.exp(lerp(math.log(0.059), math.log(0.012), e_in(prog(t, PORTAL_OUT[0], PORTAL_OUT[1]))))
    return BC + np.array([-500.0, -600.0]), z


def fondo_img(t):
    return F.degradado(t, (0.42, 0.10, 0.20), (0.22, 0.04, 0.12))


# ======================================================================== piezas
def vaso(lz, t, a, z):
    """Paredes del vaso sanguíneo y plasma."""
    x0 = a[0] - W / z
    x1 = a[0] + W / z
    xs = np.linspace(x0, x1, 40)
    for lado in (-1, 1):
        y_in = lado * 300 + 14 * np.sin(xs / 140 + t)
        y_out = lado * 900
        lz.relleno(np.concatenate([np.stack([xs, y_in], 1), np.stack([xs[::-1], np.full(40, y_out)], 1)]), (238, 150, 160))
        lz.relleno(np.concatenate([np.stack([xs, y_in], 1), np.stack([xs[::-1], (y_in + lado * 60)[::-1]], 1)]), (250, 186, 190))
        for i in range(int(x0 // 180), int(x1 // 180) + 1):
            cx = i * 180 + 40 * math.sin(i)
            lz.relleno(elipse(cx, lado * 330 + 6 * math.sin(i + t), 60, 18, 0, 20), (255, 206, 206), alfa=0.8)
            lz.relleno(circulo(cx + 10, lado * 330, 9, 12), (220, 110, 140))
        # tejido fuera
        for i in range(int(x0 // 260), int(x1 // 260) + 1):
            cx = i * 260 + 70 * math.sin(i * 2.1)
            lz.relleno(circulo(cx, lado * (560 + 90 * math.sin(i * 1.3)), 70, 26), (246, 176, 182), alfa=0.9)
            lz.relleno(circulo(cx + 12, lado * (560 + 90 * math.sin(i * 1.3)), 22, 16), (200, 100, 140), alfa=0.8)


def globulos(lz, t, a, z, falta):
    x0 = a[0] - W / z - 200
    L = 2 * W / z + 400
    for i in range(46):
        xb = x0 + ((h01(i, 1) * 4000 + V_FLUJO * t - x0) % L)
        yb = (h01(i, 2) - 0.5) * 460 + 20 * math.sin(t * 1.3 + i)
        rot = math.sin(t * 0.8 + i) * 0.8
        KB.globulo(lz, xb, yb, 1.15, rot, oxi=1 - falta)
        with lz.grupo(xb, yb, 1.0, rot):
            for k, (dx, dy) in enumerate(((-20, -26), (22, -22))):
                KO.molecula(lz, dx, dy, 0.5, "O2", rot=k + t * 0.5, falta_o=falta, hueco=1.0)
    _ = x0


def kuri_globulo(lz, t, a, z):
    if t > A.celulas + 1.0:
        return
    xb = a[0] - 120 + 40 * math.sin(t * 0.7)
    yb = 60 + 20 * math.sin(t * 1.3)
    KB.globulo(lz, xb, yb + 26, 2.2, 0.1 * math.sin(t))
    tir = 0.6 if t > A.desaparece_c else 0.0
    P.kuri(lz, xb, yb, 0.75, t, mirar=(0.6, -0.4) if t < A.desaparece_c else (-0.6, 0.2), aleteo=0.5 if t < A.sangre else 0.0,
           tiritar=tir)


def celula(lz, t, falta):
    """Célula con núcleo, retículo, mitocondrias; glucosa que entra; pila de energía."""
    x, y, r = X_CEL, 0.0, 620.0
    lz.halo(x, y, r * 1.25, (255, 190, 190), alfa=0.35)
    lz.relleno(catmull(np.array([[x + r * (1 + 0.04 * math.sin(k * 1.7 + t)) * math.cos(k / 12 * 2 * math.pi),
                                  y + r * 0.86 * (1 + 0.04 * math.sin(k * 1.7 + t)) * math.sin(k / 12 * 2 * math.pi)]
                                 for k in range(12)]), 8, True), (250, 200, 196))
    lz.relleno(catmull(np.array([[x + r * 0.94 * math.cos(k / 12 * 2 * math.pi), y + r * 0.8 * math.sin(k / 12 * 2 * math.pi)]
                                 for k in range(12)]), 8, True), (255, 226, 216))
    lz.relleno(circulo(x - 120, y - 40, 170, 50), (170, 120, 220))
    lz.relleno(circulo(x - 150, y - 70, 70, 30), (200, 160, 240))
    for k in range(4):
        lz.trazo(P.arco_pts(x - 120, y - 40, 230 + 26 * k, -0.6, 1.2, 30), (240, 170, 200), 9, afinar=False)
    act = 1 - e_inout(prog(t, A.celulas + 0.4, A.energia + 0.6)) * falta
    for i, (mx, my, rot) in enumerate(((x + 230, y - 260, 0.3), (x + 320, y + 120, -0.5), (x + 90, y + 300, 0.9),
                                       (x - 330, y + 260, 0.2), (x + 380, y - 60, 1.4), (x - 380, y - 230, -0.8))):
        KB.mitocondria(lz, mx, my + 6 * math.sin(t + i), 1.3, t, activo=act, rot=rot + 0.1 * math.sin(t * 0.7 + i))
    # glucosa (comida) que entra desde la izquierda
    for i in range(6):
        u = (t * 0.22 + i / 6) % 1
        gx = x - r * 1.2 + u * r * 1.3
        gy = y + 180 * math.sin(i * 2.1) + 30 * math.sin(t + i)
        KB.glucosa(lz, gx, gy, 1.4, rot=t + i, alfa=min(1.0, u * 4) * (1 - max(0.0, u - 0.85) * 6))
    # O2 que debería llegar: huecos punteados cuando falta
    for i in range(5):
        u = (t * 0.3 + i / 5 + 0.1) % 1
        ox = x - r * 1.25 + u * r * 1.4
        oy = y - 300 + 140 * math.sin(i * 1.7)
        KO.molecula(lz, ox, oy, 1.1, "O2", rot=t + i, falta_o=falta, hueco=1.0)


def neuronas(lz, t, a, z):
    """Red de neuronas alrededor de la célula (se ve al alejarse)."""
    if z > 0.6:
        return
    al = 1 - prog(z, 0.3, 0.6)
    for i in range(70):
        ang = h01(i, 3) * 2 * math.pi
        d = 1600 + 5200 * h01(i, 4)
        nx, ny = X_CEL + d * math.cos(ang), d * math.sin(ang) * 0.8
        lz.relleno(circulo(nx, ny, 220 + 120 * h01(i, 5), 20), (250, 196, 200), alfa=al)
        for k in range(3):
            a2 = ang + 0.8 * k + h01(i, k)
            lz.trazo(np.array([[nx, ny], [nx + 700 * math.cos(a2), ny + 700 * math.sin(a2)]]), (250, 196, 200, int(220 * al)), 60,
                     afinar=True)


def cerebro_vista(lz, t, z):
    if z > 0.25:
        return
    al = 1 - prog(z, 0.12, 0.25)
    with lz.grupo(BC[0], BC[1], S_CER):
        lz.halo(0, 0, 220, (255, 160, 190), alfa=0.35 * al)
        en = 1.0 - 0.8 * e_inout(prog(t, A.cortan, A.seis + 0.4))
        KB.cerebro(lz, 0, 0, 1.0, t, energia=en * al, falta=0.5 * (1 - en))
        # arterias: la sangre entra por el tronco y se reparte por la corteza (se corta en 1943)
        corte = prog(t, A.cortan - 0.2, A.cortan + 0.4)
        col = mezcla((236, 50, 70), (150, 130, 160), corte)
        ramas = [[(14, 120), (10, 60), (-10, 20), (-60, -10), (-104, -36)], [(10, 60), (20, 10), (50, -40), (90, -64)],
                 [(-10, 20), (-30, -40), (-40, -96)], [(20, 10), (60, 6), (110, -6)], [(50, -40), (20, -90), (-10, -112)]]
        for i, rm in enumerate(ramas):
            Q = catmull(np.array(rm, float), 6)
            lz.trazo(Q, col + (int(255 * al),), 9 if i == 0 else 6, afinar=True)
            L = len(Q)
            for k in range(3):
                u = ((t * 0.7 if corte < 0.5 else A.cortan * 0.7) + k / 3 + i * 0.13) % 1
                q = Q[min(L - 1, int(u * (L - 1)))]
                lz.relleno(circulo(q[0], q[1], 4.5, 10), mezcla((255, 150, 150), (170, 150, 180), corte), alfa=al * (1 - corte * 0.5))


def dibujar_contenido(lz, t):
    a, z = cam(t)
    falta = e_out(prog(t, A.desaparece_c - 0.05, A.desaparece_c + 0.4))
    with lz.grupo(W / 2, H / 2, z):
        with lz.grupo(-a[0], -a[1]):
            if t < A.cerebro + 0.6:
                if z > 0.3:
                    vaso(lz, t, a, z)
                    globulos(lz, t, a, z, falta)
                celula(lz, t, falta)
                kuri_globulo(lz, t, a, z)
            cerebro_vista(lz, t, z)


def dibujar(lz, t):
    dibujar_contenido(lz, t)
    return fondo_img(t)


def portal(lz, t, S, bg, entrada=True):
    """Círculo que se abre en el pecho (entrada) o se cierra en la cabeza (salida) con el cuerpo dentro."""
    import gente as G
    if entrada:
        u = e_in(prog(t, PORTAL_IN[0], PORTAL_IN[1]))
        cx, cy = S.pt(G.X_PROTA, 118)
    else:
        u = 1 - e_out(prog(t, PORTAL_OUT[0], PORTAL_OUT[1]))
        cx, cy = S.pt(G.X_PROTA + 3, 200)
    r = 6 + 2300 * u
    if r < 2:
        return bg
    C = circulo(cx, cy, r, 160)
    lz.halo(cx, cy, r * 1.25 + 40, (255, 210, 220), alfa=0.6, r0=0.75)
    with lz.recorte(C):
        lz.degradado(C, (108, 26, 52), (56, 10, 30), (cx, cy - r), (cx, cy + r))
        dibujar_contenido(lz, t)
    lz.trazo(P.arco_pts(cx, cy, r, 0, 2 * math.pi, 160), (255, 230, 236), 8, afinar=False)
    return bg
