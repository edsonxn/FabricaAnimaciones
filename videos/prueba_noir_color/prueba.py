# -*- coding: utf-8 -*-
"""Prueba de 30 s del estilo NOIR COLOR (neo-noir apagado; kit nucleo/noir_color.py, doc docs/estilo_noir_color.md).
Tres planos encadenados con mancha de tinta, sin voz: A la calle bajo la lluvia (farola de sodio, neón rojo del hotel, el
detective llega y enciende), B la oficina (persiana, neón BAR de enfrente, calada y humo), C el escritorio desde arriba
(lámpara verde, expediente que se escribe solo, whisky, sello rojo CASO ABIERTO, relámpago y tinta).

    python videos/prueba_noir_color/prueba.py hoja 2 5 9 13 17 22 26 28     -> previews/hoja.jpg (+ PNG completos)
    python videos/prueba_noir_color/prueba.py paletas 9                       -> previews/paletas_9.jpg (sodio · bourbon · medianoche)
    python videos/prueba_noir_color/prueba.py video [--procs 6] [--paleta sodio]  -> salida/prueba_noir_color_<paleta>.mp4
"""
import math
import os
import subprocess
import sys
import time
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.join(AQUI, "..", "..", "nucleo")
sys.path[:0] = [AQUI, NUCLEO]
os.chdir(AQUI)

import cv2
import numpy as np

import mundos_nc as MU
import noir as N
import noir_color as NC
from motor import FPS, H, W, clamp01, e_inout, smooth
from noir_pers import Busto, Detective, avance_paso
from toon import Pista, blob, elipse_, suave, tubo, eje_curvo

FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
DUR = 30.0
T_B, T_C = 10.6, 20.2
TR = 0.75
PALETA = os.environ.get("NC_PALETA", "sodio")

_H = None


def lienzo():
    global _H
    if _H is None:
        _H = NC.NoirColor(PALETA)
    return _H


def rect(x, y, w, h):
    return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], float)


def rot(P, a, c):
    P = np.asarray(P, float).reshape(-1, 2) - c
    ca, sa = math.cos(a), math.sin(a)
    return np.stack([P[:, 0] * ca - P[:, 1] * sa, P[:, 0] * sa + P[:, 1] * ca], 1) + c


def parpadeo_neon(t, eventos, sem=0):
    """Intensidad de un neón viejo: zumbido fino y apagones cortos (eventos = (t0, dur))."""
    v = 0.93 + 0.05 * math.sin(t * 113 + sem) * math.sin(t * 7.1 + sem)
    for t0, d in eventos:
        if t0 <= t < t0 + d:
            u = (t - t0) / d
            v *= 0.08 + 0.5 * (math.sin(u * 37) > 0.4) * (u > 0.5)
    return v


def a_pantalla(h, P, prof):
    M = h.matriz_capa(prof)
    P = np.asarray(P, float)
    return P @ M[:2, :2].T + M[:2, 2]


def reflejar(h, t, y_mundo, k=0.42):
    """Suelo mojado: refleja el cuadro, la emisión y su COLOR (el neón rojo y el sodio se repiten en el charco)."""
    ys = h.tf(np.array([[0, y_mundo]]))[0][1]
    if not (40 < ys < H - 20):
        return
    N.reflejo(h.img, ys, k=k, t=t)
    if h._E is not None:
        N.reflejo(h._E, ys, k=k * 0.9, t=t)
        Ec = h._color_emision()
        y = int(ys)
        alto = min(H - y, y)
        Ec[y:y + alto] = Ec[y - alto:y][::-1]


# ====================================================================== plano A: la calle
CAM_A = Pista([(0.0, (1000.0, -470.0, 1.15)), (1.3, (995.0, -420.0, 1.13), "io"), (4.8, (900.0, 650.0, 1.0), "io"),
               (8.0, (1010.0, 690.0, 1.04), "io"), (T_B + 0.8, (1060.0, 640.0, 1.2), "io")])
DET_X = Pista([(0.0, 150.0), (1.4, 150.0), (7.3, 1000.0, "io"), (30.0, 1000.0)])
FUMA_A = Pista([(0.0, 0.0), (8.1, 0.0), (8.8, 1.0, "io"), (9.8, 1.0), (10.5, 0.0, "io")])
BRASA_A = Pista([(0.0, 0.0), (8.8, 0.0), (9.3, 1.0, "o"), (9.9, 1.0), (10.8, 0.15, "io")])
DET = Detective(sem=3)
FAROL = (MU.X_FAROLA - 60, 448.0)
FAROL2 = (MU.X_FAROLA2 + 60, 448.0)


def pose_a(t):
    s = 0.95
    x = DET_X(t)
    dt = 1 / 60
    vel = abs(DET_X(t + dt) - DET_X(t - dt)) / (2 * dt)
    andar = clamp01(vel / 150.0)
    paso = (x - 150.0) / avance_paso(Detective.ZANCADA, s)
    return dict(x=x, y=915.0, s=s, d=1, luz=(0.35, -1.0), rim=0.9, andar=andar, paso=paso, fumar=float(FUMA_A(t)),
                brasa=float(BRASA_A(t)), viento=0.3 + 0.15 * math.sin(t * 1.7), hombros=0.3)


def brasa(h, tip, b):
    q = np.array([[tip[0] - 3, tip[1] - 3], [tip[0] + 3, tip[1] - 3], [tip[0] + 3, tip[1] + 3], [tip[0] - 3, tip[1] + 3]])
    h.emitir(q, 0.9 + 0.5 * b, col=(1.0, 0.38, 0.10))
    h.luz_radial(tip[0], tip[1], 60 + 110 * b, (1.0, 0.45, 0.15), k=0.5 + 0.9 * b)


def p_calle(h, t, u):
    pal = h.pal
    cx, cy, z = CAM_A(t)
    h.camara(z, cx, cy, 0.012 * math.sin(t * 0.4))
    h.rim_color(pal["sodio"])
    fn = parpadeo_neon(t, [(1.35, 0.28), (6.2, 0.18)])
    NC.pegar(MU.cielo(), h, 0.05, rampa="cielo", dx=t * 6.0)
    NC.pegar(MU.lejos(), h, 0.3, rampa="lejos", bruma=0.45)
    NC.pegar(MU.medio(), h, 0.6, rampa="ladrillo", bruma=0.22)
    NC.pegar(MU.fachadas(), h, 1.0, rampa="ladrillo", emis=0.75)
    NC.pegar(MU.neon_hotel(), h, 1.0, rampa="vino", emis=1.25 * fn, col_emis=pal["neon"])
    NC.pegar(MU.suelo(), h, 1.0, rampa="asfalto", col_emis=pal["sodio"])
    p = pose_a(t)
    DET.dibujar(h, p)
    tip = DET.punta_cigarro(p)
    brasa(h, tip, p["brasa"])
    # luces: luna fría de ambiente, cono de sodio de la farola, neón rojo que baña la fachada
    h.ambiente[:] = np.array(pal["luna"], np.float32) * 0.82
    h.luz_cono(FAROL[0], FAROL[1], math.pi / 2 + 0.03, 0.55, 720, pal["sodio"], k=1.5, suave=0.5)
    h.luz_radial(FAROL[0], FAROL[1] + 60, 430, pal["sodio"], k=0.7)
    h.luz_cono(FAROL2[0], FAROL2[1], math.pi / 2 - 0.03, 0.55, 720, pal["sodio"], k=1.2, suave=0.5)
    h.luz_radial(FAROL2[0], FAROL2[1] + 60, 380, pal["sodio"], k=0.5)
    nx, ny = MU.NEON[0] + 42, MU.NEON[1] + 175
    h.luz_radial(nx, ny, 560, pal["neon"], k=0.95 * fn)
    h.resplandor(FAROL[0], FAROL[1] - 4, 120, 0.5, col=pal["sodio"])
    h.resplandor(FAROL2[0], FAROL2[1] - 4, 110, 0.45, col=pal["sodio"])
    h.resplandor(nx, ny, 300, 0.30 * fn, col=pal["neon"])
    reflejar(h, t, MU.Y_BORDILLO + 10)
    N.lluvia(h, t, n=650)
    y0 = h.tf(np.array([[0, MU.Y_ACERA]]))[0][1]
    y1 = h.tf(np.array([[0, 1300]]))[0][1]
    if y1 > 0 and y0 < H:
        N.salpicaduras(h, t, max(0, y0), min(H, y1), n=70)
    N.humo(h, t, tip[0], tip[1], k=0.9, t_ini=8.2)
    return h.acabado(t, niebla=dict(dens=0.26, y0=0, y1=H, sem=1), flash=N.relampago(t, [0.55]))


# ====================================================================== plano B: la oficina
BUSTO = Busto(sem=5)
BB = dict(brasa=Pista([(0, 0.0), (0.8, 0.0), (1.4, 1.0, "o"), (1.9, 1.0), (3.0, 0.2, "io")]),
          mano=Pista([(0, 0.0), (2.1, 0.0), (2.9, 1.0, "io"), (7.4, 1.0), (8.3, 0.0, "io")]),
          boca=Pista([(0, 0.0), (3.1, 0.0), (3.4, 0.6, "o"), (4.6, 0.5), (5.0, 0.0, "io")]),
          arriba=Pista([(0, 0.0), (5.4, 0.0), (6.3, 0.55, "io"), (8.6, 0.55), (9.6, 0.2, "io")]))


def p_oficina(h, t, u):
    pal = h.pal
    k = smooth(clamp01(u / 9.6))
    h.camara(1.02 + 0.07 * k, 940 + 40 * k, 545 - 10 * k, -0.006)
    h.rim_color(pal["neon"])
    fb = parpadeo_neon(t, [(T_B + 6.9, 0.35)], sem=2)
    NC.pegar(MU.afuera(), h, 0.15, rampa="lejos", bruma=0.15)
    NC.pegar(MU.neon_bar(), h, 0.15, rampa="vino", emis=1.2 * fb, col_emis=pal["neon"])
    x0, y0, x1, y1 = MU.VENT
    cv = a_pantalla(h, [(x0, y0), (x1, y1)], 0.5)
    caja = (int(cv[0, 0]), int(cv[0, 1]), int(cv[1, 0]), int(cv[1, 1]))
    N.lluvia(h, t, n=420, caja=caja, k=0.9)
    NC.pegar(MU.oficina(), h, 0.5, rampa="tela_verde")
    NC.pegar(MU.muebles(), h, 0.5, rampa="madera")
    N.gotas_vidrio(h, t, caja, n=60, k=0.7)
    p = dict(x=690.0, y=440.0, s=1.0, d=1, luz=(0.85, -0.5), rim=0.95, cigarro=True, brasa=float(BB["brasa"](u)),
             mano=float(BB["mano"](u)), boca=float(BB["boca"](u)), arriba=float(BB["arriba"](u)))
    with h.capa(1.0):
        BUSTO.dibujar(h, p)
        tip = BUSTO.punta(p)
        brasa(h, tip, p["brasa"])
    # luces: la persiana proyecta el sodio de la calle en franjas; el neón rojo entra por la ventana; luz de lámpara baja
    h.ambiente[:] = np.array(pal["luna"], np.float32) * 0.30
    h.luz_persiana([(200, 30), (1170, 130), (1170, 930), (120, 1090)], k=0.95, n=18, abierto=0.5,
                   col=np.array(pal["sodio"]) * 0.6)
    h.luz_radial(1720, 430, 1250, pal["neon"], k=0.62 * fb)
    h.luz_radial(260, 1080, 760, pal["lampara"], k=0.35)
    lb = BUSTO.labios(p)
    N.humo(h, t, tip[0], tip[1], k=0.8, sem=3, t_ini=T_B - 1)
    if p["boca"] > 0.05:
        N.humo(h, t, lb[0] + 10, lb[1], k=1.2 * p["boca"], sem=7, viento=(70.0, -40.0), hebras=5, ancho=1.6, vida=2.4)
    return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=2, vel=12.0))


# ====================================================================== plano C: el escritorio desde arriba
LINEAS = [("EXPEDIENTE 47-B", 44, 0.4), ("HOTEL ROYAL - HAB. 312", 32, 1.6), ("HORA: 03:10 A.M.   LLUVIA", 32, 2.7),
          ("TESTIGOS: NINGUNO", 32, 3.8), ("ARMA: NO HALLADA", 32, 4.7)]
CPS = 20.0
T_SELLO = T_C + 5.9
T_RAYO = T_C + 7.75
T_TINTA = DUR - 0.8


def hoja_T(cx, cy, ang, s=1.0):
    c = np.array([cx, cy], float)
    return lambda P: rot(np.asarray(P, float).reshape(-1, 2) * s + c, ang, c)


def p_mesa(h, t, u):
    pal = h.pal
    k = smooth(clamp01(u / 9.8))
    h.camara(1.0 + 0.12 * k, 930 - 40 * k, 560 - 30 * k, -0.025 + 0.035 * k)
    h.rim_color(pal["lampara"])
    NC.pegar(MU.escritorio(), h, 1.0, rampa="madera")
    # lámpara de banquero (arriba a la izquierda): pie de latón, brazo, pantalla de vidrio verde que brilla por dentro
    with h.con_rampa("laton"):
        h.pieza(elipse_(150, 360, 100, 92, n=40), 150, 1, w=5, d=14, rim=0.7, trama=0.3)
        h.pieza(elipse_(150, 360, 54, 50, n=30), 200, 2, w=3, d=6, rim=0.8, trama=0)
        h.pieza(tubo(eje_curvo((150, 360), (250, 210), 0.2, 10), 18, 14), 170, 3, w=3, d=6, rim=0.6, trama=0)
    with h.con_rampa("vidrio_verde"):
        P = rot(elipse_(0, 0, 230, 92, n=48) + (290, 170), 0.32, np.array([290.0, 170.0]))
        h.pieza(P, 120, 4, w=6, d=16, rim=0.9, trama=0.4)
        h.pieza(rot(elipse_(0, -30, 170, 22, n=30) + (290, 170), 0.32, np.array([290.0, 170.0])), 215, 5, w=0, d=0,
                sombra=0, rim=0, alfa=0.55)
    h.emitir(rot(elipse_(0, 70, 200, 28, n=30) + (290, 170), 0.32, np.array([290.0, 170.0])), 0.55, col=pal["verde"], blur=8)
    # la carpeta manila abierta y la hoja del expediente
    Tc = hoja_T(880, 590, -0.04)
    with h.con_rampa("papel"):
        h.pieza(Tc([(-530, -400), (-180, -400), (-150, -440), (120, -440), (150, -400), (530, -400), (530, 420), (-530, 420)]),
                150, 10, w=6, d=18, trama=0.4, rim=0.5)
        h.pieza(Tc(rect(-500, -380, 990, 790)), 175, 11, w=3, d=6, trama=0, rim=0, alfa=0.6)
        Th = hoja_T(860, 610, 0.02)
        h.pieza(Th(rect(-330, -430, 660, 880)), 228, 12, w=4, luz=(0.2, -1), d=10, trama=0, rim=0)
    N.soporte(h, 860, 610, 660, 880, 0.02, 1.0)
    for i, (s, px, t0) in enumerate(LINEAS):
        P = Th([(-270, -360 + (0 if i == 0 else 40) + i * 62)])[0]
        N.texto_maquina(h, s, P[0], P[1], px, t, T_C + t0, cps=CPS, tono=np.array(pal["tinta"]) * 2.4,
                        fuente=N.FUENTE_MAQ if i else "C:/Windows/Fonts/impact.ttf", track=1.0 if i else 3.0)
    for i in range(6):                                                          # renglones del informe ya impresos
        y = -10 + i * 46
        L = 520 * (0.6 + 0.4 * abs(math.sin(i * 2.3)))
        with h.con_rampa("papel"):
            h.pieza(Th(rect(-270, y, L, 7)), 110, 40 + i, w=0, d=0, sombra=0, rim=0, alfa=0.55)
    # la foto en blanco y negro sujeta con un clip (la única cosa sin color de la mesa)
    Tf = hoja_T(1250, 300, 0.11)
    with h.con_rampa("neutro"):
        h.pieza(Tf(rect(-170, -125, 340, 250)), 226, 20, w=4, d=10, trama=0, rim=0.3)
        h.pieza(Tf(rect(-150, -105, 300, 190)), 52, 21, w=2, d=0, sombra=0, rim=0)
        h.pieza(Tf(rect(-150, 40, 300, 45)), 30, 22, w=0, d=0, sombra=0, rim=0)
        h.pieza(Tf(blob(10, -10, 34, 40, n=12)), 150, 23, w=2, d=0, sombra=0, rim=0)                  # cara
        h.pieza(Tf([(-60, -40), (80, -40), (60, -60), (-40, -60)]), 18, 24, w=2, d=0, sombra=0, rim=0)  # ala del sombrero
        h.pieza(Tf([(-30, -60), (50, -60), (40, -95), (-20, -95)]), 18, 25, w=2, d=0, sombra=0, rim=0)
        h.pieza(Tf([(-70, 85), (-50, 30), (70, 30), (90, 85)]), 26, 26, w=2, d=0, sombra=0, rim=0)
    with h.con_rampa("laton"):
        h.pieza(Tf(suave([(-110, -150), (-110, -95), (-80, -95), (-80, -140), (-100, -140), (-100, -105)], 2)), 190, 27,
                w=3, d=4, trama=0, rim=0.8, sombra=0.4)
    # vaso de whisky con hielo (arriba a la derecha) y su cerco
    gx, gy = 1600, 250
    with h.con_rampa("piedra"):
        h.pieza(elipse_(gx + 18, gy + 22, 104, 104, n=48), 20, 30, w=0, d=0, sombra=0, rim=0, alfa=0.45)
        h.pieza(elipse_(gx, gy, 104, 104, n=48), 200, 31, w=4, d=8, trama=0, rim=0.9, alfa=0.55)
    with h.con_rampa("whisky"):
        h.pieza(elipse_(gx, gy, 88, 88, n=40), 130, 32, w=2, d=10, trama=0, rim=0.5)
    with h.con_rampa("piedra"):
        for j, (dx, dy, a) in enumerate(((-24, -14, 0.3), (26, 20, -0.4))):
            h.pieza(rot(rect(gx + dx - 30, gy + dy - 30, 60, 60), a + 0.05 * math.sin(t * 0.7 + j), np.array([gx + dx, gy + dy])),
                    215, 33 + j, w=2, d=6, trama=0, rim=0.9, alfa=0.7)
        h.pieza(TN_arco(gx, gy, 80, -2.5, -1.4), 250, 35, w=0, d=0, sombra=0, rim=0, alfa=0.7)
    # cenicero con el cigarro consumiéndose
    ax, ay = 1590, 830
    with h.con_rampa("piedra"):
        h.pieza(elipse_(ax, ay, 132, 120, n=48), 96, 40, w=5, d=14, trama=0.3, rim=0.7)
        h.pieza(elipse_(ax, ay + 6, 92, 82, n=40), 40, 41, w=3, d=0, sombra=0, rim=0)
        for c in range(5):
            h.pieza(blob(ax - 40 + c * 18, ay + 10 + 8 * math.sin(c), 10, 7, n=8), 120, 42 + c, w=1, d=0, sombra=0, rim=0)
    with h.con_rampa("papel"):
        h.pieza(rot(rect(ax - 10, ay - 12, 210, 22), -0.5, np.array([ax, ay])), 225, 50, w=3, d=6, trama=0, rim=0.6)
    ce = rot(np.array([[ax + 200, ay]]), -0.5, np.array([ax, ay]))[0]
    with h.con_rampa("piedra"):
        h.pieza(rot(rect(ce[0] - 34, ce[1] - 11, 34, 22), -0.5, ce), 150, 51, w=2, d=0, sombra=0, rim=0)
    brasa(h, ce, 0.35 + 0.25 * math.sin(t * 2.3) ** 2)
    # cerillas de un bar y estilográfica
    with h.con_rampa("vino"):
        h.pieza(rot(rect(230, 820, 190, 110), 0.25, np.array([325.0, 875.0])), 120, 60, w=4, d=10, trama=0.3, rim=0.6)
        h.pieza(rot(tubo(np.array([[1180.0, 640.0], [1420.0, 780.0]]), 18, 14), 0, np.array([0.0, 0.0])), 70, 61, w=4, d=8,
                trama=0, rim=0.9)
    with h.con_rampa("laton"):
        h.pieza(tubo(np.array([[1390.0, 762.0], [1430.0, 786.0]]), 14, 10), 190, 62, w=2, d=4, trama=0, rim=0.9)
    # sello rojo sobre el expediente
    P = Th([(60, 200)])[0]
    N.sello(h, "CASO ABIERTO", P[0], P[1], 84, t, T_SELLO, rot=-9, tono=np.array(pal["sello"]), alfa=0.95)
    # luces: charco cálido de la lámpara, ambiente frío, el neón de la calle asoma por la derecha; el relámpago entra por la ventana
    fl = N.relampago(t, [T_RAYO])
    h.ambiente[:] = np.array(pal["luna"], np.float32) * 0.24
    h.luz_radial(700, 560, 1150, pal["lampara"], k=1.05)
    h.luz_radial(330, 230, 420, pal["verde"], k=0.35)
    h.luz_radial(2150, 250, 900, pal["neon"], k=0.3 * parpadeo_neon(t, [], sem=4))
    if fl > 0:
        h.luz_persiana([(1900, -200), (2300, 400), (600, 1500), (-200, 900)], k=2.4 * fl, n=14, abierto=0.55,
                       col=pal["relampago"])
    N.humo(h, t, ce[0], ce[1], k=0.85, sem=11, viento=(-10.0, -60.0))
    N.motas(h, t, n=80, k=0.5)
    img = h.acabado(t, flash=0.35 * fl)
    if t >= T_TINTA:
        img = N.tinta_cubre(img, (t - T_TINTA) / (DUR - T_TINTA) * 1.05, sem=5, tono=np.array(pal["tinta"]))
    return img


def TN_arco(cx, cy, r, a0, a1, w=10):
    """Brillo curvo del vidrio (media luna fina)."""
    a = np.linspace(a0, a1, 20)
    ext = np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)
    inn = np.stack([cx + (r - w) * np.cos(a[::-1]), cy + (r - w) * np.sin(a[::-1])], 1)
    return np.vstack([ext, inn])


# ====================================================================== montaje
PLANOS = [(0.0, p_calle), (T_B, p_oficina), (T_C, p_mesa)]


def _r(i, t):
    h = lienzo()
    h.nuevo(t, None)
    t0, fn = PLANOS[i]
    return fn(h, t, t - t0)


def cuadro(t):
    i = max(k for k, (t0, _) in enumerate(PLANOS) if t0 <= t)
    img = _r(i, t)
    if i > 0 and t < PLANOS[i][0] + TR:
        prev = _r(i - 1, t)
        img = N.transicion(prev, img, (t - PLANOS[i][0]) / TR, "tinta", sem=i * 3)
    return np.clip(img, 0, 1)


def a_u8(img):
    return (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)


# ====================================================================== sonido (todo sintetizado, nucleo/sfx_noir.py)
def audio(ruta):
    import sfx_noir as S
    from sinte import SR
    n = int(DUR * SR)
    mix = np.zeros((2, n))

    def mete(x, t0, g):
        x = np.asarray(x, float)
        if x.ndim == 1:
            x = np.stack([x, x])
        i = int(t0 * SR)
        m = min(x.shape[1], n - i)
        if m > 0:
            mix[:, i:i + m] += x[:, :m] * g

    mete(S.s_lluvia_amb(T_B + 0.6), 0.0, 0.42)
    mete(S.s_zumbido_lampara(T_B), 0.0, 0.05)
    mete(S.s_grave_inquietante(5.0), 0.0, 0.25)
    mete(S.s_trueno_lejano(4.0), 0.5, 0.45)
    mete(S.s_pasos_mojados(5.6), 1.6, 0.42)
    mete(S.s_cerilla(), 8.25, 0.4)
    mete(S.s_lluvia_lejana(T_C - T_B + 0.6), T_B - 0.2, 0.40)
    mete(S.s_gotas_vidrio(T_C - T_B), T_B, 0.18)
    mete(S.s_calada(), T_B + 0.7, 0.55)
    mete(S.s_exhala(), T_B + 3.2, 0.55)
    mete(S.s_lluvia_lejana(DUR - T_C), T_C - 0.2, 0.25)
    mete(S.s_reloj_pared(DUR - T_C), T_C, 0.12)
    for s, px, t0 in LINEAS:
        d = len(s) / CPS
        mete(S.s_tecleo_rapido(d), T_C + t0, 0.38)
        mete(S.s_carro_maquina(), T_C + t0 + d + 0.05, 0.25)
    mete(S.s_sello_golpe(), T_SELLO, 0.85)
    mete(S.s_sombra_crece(2.5), T_SELLO + 0.3, 0.25)
    mete(S.s_trueno_noir(4.0), T_RAYO, 0.75)
    mete(S.s_tinta_mancha(0.8), T_TINTA, 0.45)
    for tt in (T_B - 0.35, T_C - 0.35):
        mete(S.s_tinta_mancha(0.8), tt, 0.3)
    f = np.ones(n)
    f[-int(0.6 * SR):] = np.linspace(1, 0, int(0.6 * SR))
    mix *= f
    mix *= 0.85 / (np.abs(mix).max() + 1e-9)
    pcm = (mix.T * 32767).astype(np.int16)
    with wave.open(ruta, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ====================================================================== render
def _trozo(args):
    i, f0, f1, paleta = args
    os.environ["NC_PALETA"] = paleta
    global PALETA
    PALETA = paleta
    ruta = os.path.join(AQUI, "segmentos", f"seg_{paleta}_{i:03d}.mp4")
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", ruta]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        pr.stdin.write(a_u8(cuadro(f / FPS)).tobytes())
    pr.stdin.close()
    pr.wait()
    return ruta


def video(procs, paleta):
    from multiprocessing import Pool
    nf = int(DUR * FPS)
    paso = 30
    trozos = [(k, f, min(nf, f + paso), paleta) for k, f in enumerate(range(0, nf, paso))]
    t0 = time.time()
    with Pool(procs) as pool:
        rutas = []
        for r in pool.imap(_trozo, trozos):
            rutas.append(r)
            print(f"  {len(rutas)}/{len(trozos)} trozos ({time.time() - t0:.0f} s)", flush=True)
    lista = os.path.join(AQUI, "segmentos", f"lista_{paleta}.txt")
    with open(lista, "w", encoding="utf-8") as fh:
        for r in rutas:
            fh.write(f"file '{r.replace(os.sep, '/')}'\n")
    wav = os.path.join(AQUI, "segmentos", "audio.wav")
    audio(wav)
    out = os.path.join(AQUI, "salida", f"prueba_noir_color_{paleta}.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-i", wav, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(f"-> {out}  ({time.time() - t0:.0f} s)")


def hoja(tiempos, nombre="hoja"):
    tiles = []
    for t in tiempos:
        t1 = time.time()
        im = a_u8(cuadro(t))
        dt = time.time() - t1
        cv2.imwrite(os.path.join("previews", f"f_{PALETA}_{t:05.2f}.png"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
        sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
        for c, g in (((0, 0, 0), 3), ((255, 255, 255), 1)):
            cv2.putText(sm, f"t={t:.2f} {dt * 1000:.0f}ms", (6, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, g, cv2.LINE_AA)
        tiles.append(sm)
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    img = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
    cv2.imwrite(os.path.join("previews", f"{nombre}.jpg"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"{len(tiempos)} cuadros -> previews/{nombre}.jpg")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--paleta" in a:
        PALETA = a[a.index("--paleta") + 1]
    if a[0] == "hoja":
        hoja([float(x) for x in a[1:] if x.replace(".", "").isdigit()])
    elif a[0] == "paletas":
        t = float(a[1])
        tiles = []
        for pal in ("sodio", "bourbon", "medianoche"):
            _H = None
            PALETA = pal
            im = a_u8(cuadro(t))
            cv2.imwrite(os.path.join("previews", f"f_{pal}_{t:05.2f}.png"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
            sm = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
            cv2.putText(sm, pal, (14, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)
            tiles.append(sm)
        cv2.imwrite(os.path.join("previews", f"paletas_{t:05.2f}.jpg"), cv2.cvtColor(np.hstack(tiles), cv2.COLOR_RGB2BGR),
                    [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(f"-> previews/paletas_{t:05.2f}.jpg")
    elif a[0] == "video":
        procs = int(a[a.index("--procs") + 1]) if "--procs" in a else 6
        video(procs, PALETA)
