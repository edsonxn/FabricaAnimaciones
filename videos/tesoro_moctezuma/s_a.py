# -*- coding: utf-8 -*-
"""Escenas 1-4: gancho (mapa nocturno y columna en fuga), llegada (ruta de Cortés y encuentro en la calzada), puerta (pared que cae) y valor (podio)."""
import math

import numpy as np

from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, catmull, bezier, h01
import plano as P
import mapa as MP
import mapa_local as ML
import figuras as F
from mundo import degradado_v, llama, humo, estrellas
from reg import shot, snd
from util import *

PANT = np.array([[0, 0], [W, 0], [W, H], [0, H]], float)


def km2s(c, x, y):
    return W / 2 + (x - c[0]) * ML.PXKM * c[2], H / 2 - (y - c[1]) * ML.PXKM * c[2]


# ======================================================================== 1. GANCHO
E1 = "gancho"


@shot(0.0, bg=lambda t: bg_grad((6, 8, 30), (14, 18, 60)), ent=("fundido", 0.01))
def g_mapa(lz, t):
    c = Klog(t, [(0, (-98.6, 20.7, 1.0)), (7.4, (-99.13, 19.55, 7.0))])
    MP.mapa(lz, t, c, dict(ciudad_alfa=0.0, cdmx=0.0))
    lz.relleno(PANT, (10, 12, 58), alfa=0.62, capa=2)
    x, y = MP.scr(c, *MP.CDMX)
    a = smooth(prog(t, 3.0, 6.0))
    lz.halo(x, y, 90 + 12 * c[2], (255, 200, 110), alfa=0.6 * a, capa=2)
    MP.marcador(lz, c, MP.CDMX, "Tenochtitlan", alfa=smooth(prog(t, 4.6, 6.0)), dy=-70)
    gran(lz, t, w_(E1, 0, 3), 8.0, "30 de junio de 1520", W / 2, 120, px=86)
    etq(lz, t, 1.6, 4.4, "México, 1520", 260, 220, px=40)


@shot(7.6, bg=lambda t: bg_plano((18, 22, 58)), ent=("zoom", 0.9))
def g_calzada(lz, t):
    c = Klog(t, [(7.6, (5.5, -2.0, 0.72)), (10.3, (-0.5, 0.0, 2.3)), (12.5, (-2.5, 0.1, 2.7)), (15.6, (-3.0, 0.1, 2.7)), (18.8, (0.3, -0.4, 0.85))])
    alba = smooth(prog(t, 12.2, 16.5))
    noche = 1.0 - 0.75 * alba
    ML.dibujar_valle(lz, t, c, noche=noche, luces=1.0 - 0.7 * alba, detalle=smooth(prog(c[2], 0.9, 1.6)))
    n = 18
    head = None
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        for k in range(n):
            ts = 9.2 + k * 0.30
            x = -1.35 - 0.30 * max(0.0, t - ts)
            if t < ts:
                continue
            td = 12.6 + 3.0 * h01(11, k) if k not in (3, 9) else 99
            y = 0.05 + 0.02 * math.sin(k * 2.3)
            X0, Y0 = ML.km(x, y)
            if t < td:
                F.soldado(lz, X0, Y0, 0.15, t, paso=1.6, lado=-1, carga=1.0, seed=k)
                if k == 0:
                    head = (x, y)
            else:
                u = t - td
                if u < 0.6:
                    F.soldado(lz, X0, Y0 + u * 30, 0.15 * (1 - u * 0.4), t, paso=0.0, lado=-1, carga=1.0, seed=k)
                    ondas(lz, X0, Y0, t, td, 1.4, 30, (255, 255, 255), 2)
                lz.halo(X0, Y0, 16, ORO, alfa=0.55 * (0.6 + 0.4 * math.sin(t * 3 + k)) * smooth(prog(u, 0.2, 0.8)), capa=2)
    if head is not None and t < 12.5:
        sx, sy = km2s(c, head[0], head[1])
        for txt, ic, tt in (("Oro", 0, w_(E1, 1, 5)), ("Joyas", 1, w_(E1, 1, 6)), ("Plumas", 2, w_(E1, 1, 8))):
            a = vent(t, tt, tt + 1.9, 0.2, 0.4)
            if a > 0.01:
                px, py = sx + (ic - 1) * 210, sy - 150 - 40 * (t - tt) * 0.5
                with lz.capa(2):
                    if ic == 0:
                        F.barra_oro(lz, px, py, 1.3, 0.0, 0.8, alfa=a)
                    elif ic == 1:
                        F.joya(lz, px, py, 1.6, "collar", t)
                    else:
                        F.pluma(lz, px, py + 60, 0.9, 0.0, (60, 200, 130), t)
                    P.pastilla(lz, px, py + 62, txt, px=36, alfa=a)
    lz.relleno(PANT, (255, 176, 110), alfa=0.16 * alba * (1 - smooth(prog(t, 17.5, 18.8))), capa=2)
    cifra(lz, t, w_(E1, 2, 7), "500 años", W / 2, 130, px=110, col=ORO, t1=w_(E1, 2, 10) + 0.2)
    if t > w_(E1, 2, 10):
        k = e_back(prog(t, w_(E1, 2, 10), w_(E1, 2, 10) + 0.5))
        for i in range(3):
            u = ((t - w_(E1, 2, 10)) * 0.5 + i / 3) % 1.0
            lz.trazo(circulo(W / 2, 470, 60 + 420 * u, 60), (255, 220, 120), 4.0, cerrado=True, temblor=0.0, capa=2, )
        P.rotulo(lz, W / 2, 470, "?", px=330, k=0.6 + 0.4 * k, color=(255, 90, 90), alfa=smooth(prog(t, w_(E1, 2, 10), w_(E1, 2, 10) + 0.3)))


snd(0.2, "latido", 0.6, dur=1.6)
snd(7.4, "zoom_whoosh", 0.5, dur=1.0)
snd(9.2, "campana", 0.3)
for _k in range(16):
    snd(12.6 + 3.0 * h01(11, _k), "chapuzon", 0.22)
for _tt in (w_(E1, 1, 5), w_(E1, 1, 6), w_(E1, 1, 8)):
    snd(_tt, "clink", 0.4)
snd(12.4, "amanecer", 0.35, dur=3.0)
snd(w_(E1, 2, 10), "hmm", 0.45)

# ======================================================================== 2. LLEGADA
E2 = "llegada"
RUTA = [(-96.13, 19.18), (-96.42, 19.43), (-97.2, 19.32), (-98.2, 19.32), (-98.3, 19.06), (-98.75, 19.32), (-99.13, 19.43)]
GY = 830.0                 # suelo de las escenas laterales
SH = 1.75                  # escala de las personas en escena lateral


@shot(T0(E2), bg=lambda t: bg_grad((10, 20, 60), (24, 60, 120)), ent=("tinta", 0.7))
def ll_ruta(lz, t):
    c = Klog(t, [(T0(E2), (-97.25, 19.3, 1.05)), (26.8, (-97.5, 19.28, 1.25))])
    MP.mapa(lz, t, c, dict(ciudad_alfa=0.0, cdmx=0.0))
    u = K(t, [(INI(E2, 0) + 0.3, 0.0), (w_(E2, 0, 10), 1.0)], e_inout)
    pts = catmull(np.array([MP.XY(a, b) for a, b in RUTA]), 14)
    cx, cy = MP.XY(c[0], c[1])
    n = len(pts)
    z = c[2]
    with lz.grupo(960 - cx * z, 540 - cy * z, z):
        P.discontinua(lz, pts, (255, 214, 96), ancho=10.0 / z ** 0.5, largo=40 / z ** 0.5, hueco=26 / z ** 0.5, fase=-t * 40 / z ** 0.5, frac=u)
        hx, hy = pts[min(n - 1, int(u * (n - 1)))]
        with lz.grupo(hx, hy, 0.42 / z):
            for k in range(3):
                F.soldado(lz, (-26 + k * 26), 0, 1.0, t, paso=1.6, lado=-1, carga=0.0, seed=k, arma="lanza" if k != 1 else None)
    for i, (nom, (lo, la), tt) in enumerate((("Veracruz", RUTA[0], INI(E2, 0) + 0.3), ("Tlaxcala", RUTA[3], 23.0), ("Cholula", RUTA[4], 24.3), ("Tenochtitlan", RUTA[6], w_(E2, 0, 10)))):
        MP.marcador(lz, c, (lo, la), nom, alfa=smooth(prog(t, tt, tt + 0.4)), dy=-50 if i != 2 else 44, px=36)
    cifra(lz, t, w_(E2, 0, 1), "8 de noviembre de 1519", W / 2, 130, px=74, col=(255, 255, 255), t1=27.0)


snd(T0(E2) + 0.4, "pasos", 0.3, dur=5.5)
for _tt in (INI(E2, 0) + 0.3, 23.0, 24.3, w_(E2, 0, 10)):
    snd(_tt, "pop", 0.35)


def _lejos(lz, camx, t):
    """Fondo de la calzada: volcanes, isla-ciudad al horizonte, nubes (con paralaje). Pantalla = mundo - camx + 960."""
    with lz.grupo(W / 2 - camx * 0.06, 0, 1.0):
        for (vx, s) in ((-500, 420), (600, 340), (1500, 380)):
            lz.relleno(np.array([[vx - s * 1.2, 700], [vx, 700 - s], [vx + s * 1.2, 700]]), (150, 132, 178))
            lz.relleno(np.array([[vx, 700 - s], [vx + s * 1.2, 700], [vx + s * 0.15, 700]]), (120, 106, 160))
            lz.relleno(np.array([[vx - s * 0.22, 700 - s * 0.78], [vx, 700 - s], [vx + s * 0.22, 700 - s * 0.78]]), (250, 246, 246))
        for i in range(6):
            x = -1400 + i * 620 + 30 * math.sin(t * 0.2 + i)
            lz.relleno(circulo(x, 190 + 70 * h01(9, i), 70, 20), (255, 255, 255), alfa=0.75)
            lz.relleno(circulo(x + 70, 205 + 70 * h01(9, i), 52, 20), (255, 255, 255), alfa=0.75)
            lz.relleno(circulo(x - 66, 210 + 70 * h01(9, i), 44, 20), (255, 255, 255), alfa=0.75)
    with lz.grupo(W / 2 - camx * 0.3, 0, 1.0):
        for i in range(-14, 15):
            x = i * 190 + 40 * h01(2, i)
            h = 70 + 56 * h01(3, i)
            w = 140 + 50 * h01(4, i)
            lz.relleno(rect_red(x - w / 2, 730 - h, w, h, 3), (236, 222, 204) if i % 2 else (222, 204, 186))
            lz.relleno(rect_red(x - w / 2, 730 - h, w, 8, 0), (200, 180, 160))
            if h01(5, i) > 0.5:
                lz.relleno(rect_red(x - 10, 730 - h * 0.55, 20, 24, 3), (120, 150, 190))
        F.templo_mayor(lz, -700, 734, 0.62)


def _calzada(lz, camx, t, y0=GY):
    with lz.grupo(W / 2 - camx, 0, 1.0):
        agua(lz, camx - 1100, camx + 1100, y0 + 40, 1120, t, (72, 152, 214), (20, 56, 130), amp=5, luna=None)
        lz.relleno(rect_red(camx - 1100, y0, 2200, 46, 0), (206, 176, 140))
        lz.relleno(rect_red(camx - 1100, y0, 2200, 9, 0), (240, 214, 176))
        for k in range(-12, 13):
            lz.relleno(rect_red((camx // 140) * 140 + k * 140, y0 + 46, 14, 80, 0), (150, 116, 96))


def _cortina_plumas(lz, x, y, s, t):
    """Sombrilla de plumas sobre el tlatoani."""
    with lz.grupo(x, y, s):
        for i in range(9):
            a = -1.3 + i * 0.325
            lz.relleno(elipse(math.sin(a) * 84, -math.cos(a) * 22 - 4, 12, 44, -a, 12), ((60, 200, 130), (255, 210, 80), (230, 80, 90), (90, 160, 240), (60, 200, 130))[i % 5])
        lz.relleno(rect_red(-4, 0, 8, 100, 2), (120, 90, 60))


def _grupo_mex(lz, x, y, t, avanza, lado=1):
    """Comitiva mexica: el tlatoani bajo una sombrilla de plumas y cuatro guerreros. x = centro."""
    F.tlatoani(lz, x, y, SH * 1.05, t, lado=lado, brazos=0.0, paso=1.0 if avanza else 0.0, seed=4)
    _cortina_plumas(lz, x, y - 250, 1.7, t)
    for k, dx in enumerate((-260, -160, 200, 300)):
        F.guerrero(lz, x + dx, y + 8 * (k % 2), SH, t, paso=1.0 if avanza else 0.0, lado=lado, arma="lanza" if k % 2 == 0 else "macuahuitl", plumas=k, seed=k + 5)


def _grupo_esp(lz, x, y, t, avanza, lado=-1):
    """Hueste de Cortés: capitán, tres soldados y dos caballos. x = centro."""
    F.soldado(lz, x, y, SH * 1.1, t, paso=1.0 if avanza else 0.0, lado=lado, arma="espada", seed=1, tunica=(150, 40, 60))
    for k, dx in enumerate((140, 250, 350)):
        F.soldado(lz, x + dx, y + 6 * (k % 2), SH, t, paso=1.0 if avanza else 0.0, lado=lado, arma="lanza" if k != 1 else "espada", seed=k + 9)
    for k, dx in enumerate((520, 760)):
        F.caballo(lz, x + dx, y + 12, SH * 0.95, t, paso=1.0 if avanza else 0.0, lado=lado, carga=0, col=(150, 98, 68) if k == 0 else (96, 70, 60), seed=k + 2)


T_PAL = -3450.0            # x del palacio (mundo)


@shot(26.6, bg=lambda t: bg_grad((90, 170, 240), (255, 226, 190), ym=0.5), ent=("tinta", 0.8))
def ll_encuentro(lz, t):
    # 26.6-28.4 se acercan; 28.4-28.9 se saludan; 28.9-30.9 caminan juntos (la cámara los sigue) hacia el palacio de la izquierda
    dx = -K(t, [(28.9, 0.0), (30.95, 2900.0)], e_inout) if t > 28.9 else 0.0
    camx = dx
    _lejos(lz, camx, t)
    _calzada(lz, camx, t)
    xm = K(t, [(26.6, -1700.0), (28.4, -340.0)], e_out)
    xe = K(t, [(26.6, 1700.0), (28.4, 340.0)], e_out)
    avanza = t < 28.4 or t > 28.9
    with lz.grupo(W / 2 - camx, 0, 1.0):
        F.palacio(lz, T_PAL, GY, 1.7, luz=smooth(prog(t, 29.8, 31.0)))
    with lz.grupo(W / 2 - camx, 0, 1.0):
        _grupo_mex(lz, xm + dx, GY, t, avanza, lado=1)
        _grupo_esp(lz, xe + dx, GY, t, avanza, lado=-1)
    if 28.4 <= t < 28.9:
        lz.halo(W / 2, GY - 250, 120 * math.sin(math.pi * (t - 28.4) / 0.5), (255, 240, 180), alfa=0.6, capa=2)
    a = vent(t, 27.0, 29.0)
    if a > 0.01:
        P.pastilla(lz, W / 2 - 340, GY - 470, "Moctezuma II", px=38, alfa=a)
        P.pastilla(lz, W / 2 + 340, GY - 470, "Hernán Cortés", px=38, alfa=a)
    etq(lz, t, 30.1, 31.2, "Palacio de Axayácatl", W / 2, 240, px=42)


@shot(31.0, bg=lambda t: bg_grad((90, 170, 240), (255, 226, 190), ym=0.5), ent=("fuga", 0.7))
def ll_regalos(lz, t):
    camx = T_PAL + 160.0
    _lejos(lz, camx, t)
    _calzada(lz, camx, t)
    items = ["disco", "plata", "joyas", "barras", "plumas", "jade", "disco", "cofre"]
    with lz.grupo(W / 2 - camx, 0, 1.0):
        F.palacio(lz, T_PAL, GY, 1.7, luz=1.0)
        avance = K(t, [(31.0, 0.0), (37.5, 3300.0)], e_inout)
        for k in range(8):
            xk = T_PAL - 2400 + 400 * k + avance
            F.guerrero(lz, xk, GY, SH, t, paso=1.0, lado=1, arma=None, escudo=False, plumas=k, seed=k + 20, brazos=(-2.75, 2.75))
            it = items[k]
            ix, iy = xk + 6, GY - 250
            if it == "disco":
                F.disco(lz, ix, iy - 26, 66, t, "oro")
            elif it == "plata":
                F.disco(lz, ix, iy - 26, 66, t, "plata")
            elif it == "joyas":
                lz.relleno(rect_red(ix - 50, iy, 100, 10, 3), (150, 100, 60))
                F.joya(lz, ix - 24, iy - 20, 1.0, "anillo", t)
                F.joya(lz, ix + 22, iy - 12, 0.8, "collar", t)
            elif it == "barras":
                F.barra_oro(lz, ix, iy - 4, 0.9, 0.0, 0.3)
                F.barra_oro(lz, ix, iy - 38, 0.9, 0.0, 0.3)
            elif it == "plumas":
                F.pluma(lz, ix - 10, iy + 10, 0.9, 0.15, (60, 200, 130), t)
                F.pluma(lz, ix + 14, iy + 12, 0.8, -0.2, (255, 190, 60), t)
            elif it == "jade":
                F.jade(lz, ix, iy - 6, 1.6, t)
            else:
                F.cofre(lz, ix, iy + 34, 0.9, 1.0)
        for k, dx in enumerate((520, 680, 830)):
            F.soldado(lz, T_PAL + dx, GY, SH * 1.05, t, paso=0.0, lado=-1, arma="lanza" if k != 1 else None, seed=k + 30)
    bub = smooth(prog(t, w_(E2, 2, 11) - 0.6, w_(E2, 2, 11)))
    if bub > 0.01:
        px = W / 2 + (T_PAL + 680 - camx)
        pulsa = 1.0 + 0.06 * math.sin(t * 6)
        with lz.capa(2):
            lz.relleno(circulo(px, 330, 110 * bub * pulsa, 40), (255, 255, 255), alfa=0.95)
            lz.relleno(circulo(px - 40, 470, 18 * bub, 20), (255, 255, 255), alfa=0.95)
            lz.relleno(circulo(px - 64, 520, 10 * bub, 20), (255, 255, 255), alfa=0.95)
            F.barra_oro(lz, px, 338, 1.3 * bub * pulsa, 0.0, 0.9)
            F.moneda(lz, px - 56, 296, 18 * bub)
            F.moneda(lz, px + 58, 300, 15 * bub)
    gran(lz, t, w_(E2, 2, 13) - 0.1, w_(E2, 2, 13) + 2.0, "CODICIA", W / 2, 170, px=120, col=(255, 96, 96))
    etq(lz, t, w_(E2, 2, 0), w_(E2, 2, 4), "Regalos de Moctezuma", W / 2, 240, px=40)


snd(26.7, "whoosh", 0.4, dur=0.8)
snd(27.0, "pasos", 0.35, dur=2.2)
snd(28.6, "campana", 0.3)
snd(29.0, "pasos", 0.3, dur=2.0)
snd(33.6, "pasos", 0.12, dur=3.6)
for _k in range(5):
    snd(33.0 + _k * 0.9, "clink", 0.25, tono=0.9 + 0.05 * _k)
snd(w_(E2, 2, 13), "impacto", 0.5)
snd(w_(E2, 2, 11) - 0.3, "bling", 0.4)

# ======================================================================== 3. PUERTA (pared tapiada)
E3 = "puerta"
PX0, PY0, PW, PH = 1090.0, 508.0, 96.0, 300.0      # el hueco de la puerta tapiada (el muro va de x=1030 a x=1150)


def _ladrillos():
    out = []
    bw, bh = 32.0, 30.0
    cols, rows = 3, 10
    for r in range(rows):
        for c in range(cols):
            off = 16 if r % 2 else 0
            out.append((PX0 - PW / 2 + c * bw + bw / 2 - off * 0.0, PY0 + r * bh + bh / 2, r, c))
    return out


LAD = _ladrillos()
T_ROMPE = w_(E3, 1, 7)


@shot(T0(E3), bg=lambda t: bg_grad((40, 24, 56), (18, 12, 38)), ent=("tinta", 0.7))
def p_cutaway(lz, t):
    zoom = K(t, [(T0(E3), 1.28), (T_ROMPE - 0.4, 1.36), (T_ROMPE + 2.5, 1.5), (FIN(E3), 1.6)], e_inout)
    cxx = K(t, [(T0(E3), 780.0), (T_ROMPE, 900.0), (T_ROMPE + 2.5, 1180.0), (FIN(E3), 1200.0)], e_inout)
    cyy = K(t, [(T0(E3), 560.0), (T_ROMPE + 2.5, 600.0)], e_inout)
    abierto = smooth(prog(t, T_ROMPE + 0.15, T_ROMPE + 1.1))
    with cam(lz, cxx, cyy, zoom):
        # edificio en corte
        lz.relleno(rect_red(120, 190, 1680, 700, 10), (74, 50, 82))
        lz.relleno(rect_red(150, 220, 880, 620, 6), (128, 92, 100))          # sala de los españoles
        lz.relleno(rect_red(1030, 220, 740, 620, 6), (108, 78, 92))          # cámara de la derecha
        lz.relleno(rect_red(150, 820, 1620, 70, 0), (86, 60, 74))
        lz.relleno(rect_red(150, 808, 1620, 14, 0), (176, 132, 118))
        for i in range(7):                                                   # vigas del techo
            lz.relleno(rect_red(150 + i * 250, 220, 40, 30, 2), (86, 60, 74))
        # --- cámara del tesoro (detrás del muro): oscura hasta que se abre
        _tesoro(lz, t, abierto)
        lz.relleno(np.array([[1030, 220], [1770, 220], [1770, 840], [1030, 840]]), (10, 6, 24), alfa=0.92 * (1 - abierto))
        # --- muro central con el hueco de la puerta
        lz.relleno(rect_red(1030, 220, 120, PY0 - 220, 0), (150, 110, 110))                      # dintel
        lz.relleno(rect_red(1030, PY0, PX0 - PW / 2 - 1030, 840 - PY0, 0), (150, 110, 110))      # jamba izquierda
        lz.relleno(rect_red(PX0 + PW / 2, PY0, 1150 - (PX0 + PW / 2), 840 - PY0, 0), (150, 110, 110))   # jamba derecha
        # yeso fresco (más claro) sobre el hueco + ladrillos que caen
        _tapia(lz, t)
        # carpintero y soldados
        _actores(lz, t)
    # etiquetas y fuente
    _etiquetas_puerta(lz, t, cxx, cyy, zoom)


def _tapia(lz, t):
    # trazo discontinuo de la puerta que se dibuja en la frase 0
    u = smooth(prog(t, w_(E3, 0, 5), w_(E3, 0, 9)))
    reg = rect_red(PX0 - PW / 2, PY0, PW, PH, 4)
    if u > 0.01 and t < T_ROMPE:
        P.discontinua(lz, np.vstack([reg, reg[:1]]), (255, 224, 120), ancho=5.0, largo=18, hueco=12, fase=-t * 30, frac=u, capa=2)
    for (bx, by, r, c) in LAD:
        d = T_ROMPE + 0.05 * r + 0.03 * c + 0.05 * h01(r, c)
        col = (196, 150, 128) if (r + c) % 2 == 0 else (184, 138, 116)
        if t < d:
            # el yeso recién puesto es más claro que el muro
            lz.relleno(rect_red(bx - 15, by - 13, 30, 26, 3), P.mezcla(col, (248, 230, 208), 0.35 * (1 - smooth(prog(t, w_(E3, 0, 9), w_(E3, 0, 13)))) + 0.15))
        else:
            u = t - d
            if u > 1.6:
                continue
            vx = (h01(r, c, 2) - 0.75) * 240
            vy = -180 - 120 * h01(r, c, 4)
            x = bx + vx * u
            y = by + vy * u + 900 * u * u
            a = 1.0 - smooth(prog(u, 0.9, 1.6))
            with lz.grupo(x, y, 1.0, (h01(r, c, 6) - 0.5) * 9 * u):
                lz.relleno(rect_red(-15, -13, 30, 26, 3), col, alfa=a)
    # polvo
    if t > T_ROMPE:
        for i in range(8):
            u = (t - T_ROMPE) * 0.5 - i * 0.04
            if 0 < u < 1:
                lz.relleno(circulo(PX0 - 40 - u * 260 * (0.4 + h01(8, i)), PY0 + 100 + i * 24 - u * 40, 30 + u * 70, 20), (220, 200, 180), alfa=0.35 * (1 - u), capa=2)


def _tesoro(lz, t, abierto):
    """Cámara del tesoro: estantes con oro, jade, gemas, plumas; los objetos van apareciendo con las palabras de la voz."""
    lz.halo(1440, 560, 560 * abierto, (255, 214, 120), alfa=0.55 * abierto)
    # estantes
    for y in (470, 640, 808):
        lz.relleno(rect_red(1140, y, 600, 14, 3), (150, 106, 80))
    ti = dict(oro=w_(E3, 1, 16), jade=w_(E3, 1, 17), gemas=w_(E3, 1, 19))
    def pop(tt):
        return e_back(prog(t, tt, tt + 0.5))
    # oro
    k = pop(ti["oro"])
    if k > 0.02:
        F.disco(lz, 1210, 744, 58 * k, t, "oro")
        for i in range(4):
            F.barra_oro(lz, 1360 + 50 * (i % 2), 790 - 26 * (i // 2), 0.62 * k, 0.05 * (i - 1), 0.5)
        F.cofre(lz, 1560, 808, 1.2 * k, 1.0)
        F.barra_oro(lz, 1450, 452, 0.7 * k, 0.0, 0.4)
    # jade
    k = pop(ti["jade"])
    if k > 0.02:
        for i, xx in enumerate((1200, 1270, 1340)):
            F.jade(lz, xx, 622, 0.9 * k, t)
        F.jade(lz, 1660, 790, 1.2 * k, t)
    # gemas y plumas
    k = pop(ti["gemas"])
    if k > 0.02:
        for i, (xx, col) in enumerate(((1430, (110, 220, 240)), (1480, (240, 90, 120)), (1530, (255, 200, 90)), (1580, (150, 120, 240)))):
            lz.relleno(np.array([[xx - 14 * k, 612], [xx + 14 * k, 612], [xx + 20 * k, 596], [xx, 574], [xx - 20 * k, 596]]), col)
            lz.relleno(np.array([[xx - 8 * k, 596], [xx, 574], [xx + 8 * k, 596]]), P.aclarar(col, 0.5))
        for i, c_ in enumerate(((60, 200, 130), (255, 190, 60), (90, 160, 240))):
            F.pluma(lz, 1200 + i * 46, 460, 0.9 * k, 0.25 * (i - 1), c_, t)
        joya_x = 1660
        F.joya(lz, joya_x, 570, 1.5 * k, "collar", t)


def _actores(lz, t):
    # carpintero: golpea con un martillo la zona de yeso fresco
    golpe = math.sin(t * 9.0)
    if t < T_ROMPE:
        F.soldado(lz, 900, 808, 1.5, t, paso=0.0, lado=1, brazos=(-0.3, 1.9 + 0.6 * golpe), seed=41, tunica=(190, 150, 90))
        xh, yh = 900 + 22 * 1.5 * 0 + 60, 808 - 120
    else:
        u = smooth(prog(t, T_ROMPE, T_ROMPE + 0.7))
        F.soldado(lz, 900 - 60 * u, 808, 1.5, t, paso=0.0, lado=1, brazos=(-2.2, 2.2), seed=41, tunica=(190, 150, 90))
    for k, (x, lado) in enumerate(((340, 1), (520, 1), (700, 1))):
        F.soldado(lz, x - (30 * smooth(prog(t, T_ROMPE, T_ROMPE + 1.0)) if k == 1 else 0), 808, 1.5, t, paso=0.0, lado=lado, seed=k + 50,
                  arma=("lanza" if k == 0 else None), brazos=(-2.6, 2.6) if (t > T_ROMPE + 0.6 and k != 0) else None)
    F.brasero(lz, 270, 808, 1.4, t)
    # signo de interrogación sobre el muro antes de romperlo
    q = vent(t, w_(E3, 0, 4), T_ROMPE - 0.2, 0.3, 0.4)
    if q > 0.01:
        P.rotulo(lz, PX0, PY0 - 50, "?", px=130, color=(255, 224, 120), alfa=q, capa=2)


def _etiquetas_puerta(lz, t, cxx, cyy, zoom):
    a = vent(t, w_(E3, 0, 6), w_(E3, 0, 13), 0.25, 0.3)
    if a > 0.01:
        sx = W / 2 + (PX0 - cxx) * zoom
        sy = H / 2 + (PY0 - 90 - cyy) * zoom
        P.pastilla(lz, sx, sy, "puerta recién tapiada", px=38, alfa=a)
    # tarjeta de la fuente: Bernal Díaz del Castillo
    fa = vent(t, INI(E3, 1) + 0.1, T_ROMPE + 0.4, 0.4, 0.4)
    if fa > 0.01:
        with lz.capa(2):
            x = 330 - 90 * (1 - fa)
            lz.relleno(rect_red(x - 250, 96, 500, 78, 14), (255, 255, 255), alfa=0.95 * fa)
            lz.relleno(rect_red(x - 250, 96, 10, 78, 4), (255, 190, 60), alfa=fa)
            P.rotulo(lz, x + 6, 118, "Bernal Díaz del Castillo", px=34, color=(34, 28, 80), sombra=0.0, alfa=fa)
            P.rotulo(lz, x + 6, 156, "soldado y cronista de la conquista", px=26, color=(90, 84, 130), sombra=0.0, alfa=fa)
    # linaje: siluetas de emperadores antepasados
    la = vent(t, INI(E3, 2), FIN(E3) + 0.6, 0.5, 0.4)
    if la > 0.01:
        with lz.capa(2):
            for i in range(4):
                xx = 260 + i * 130
                F.tlatoani(lz, xx, 290 + 0 * i, 0.62, t, lado=1, manto=(180, 200, 230))
            lz.relleno(rect_red(200, 78, 620, 30, 12), (255, 255, 255), alfa=0.9 * la)
            P.rotulo(lz, 510, 93, "sus antepasados", px=26, color=(34, 28, 80), sombra=0.0, alfa=la)
            P.discontinua(lz, np.array([[560, 250], [900, 420], [1230, 520]]), (255, 214, 96), ancho=6.0, largo=20, hueco=14, fase=-t * 60, frac=smooth(prog(t, INI(E3, 2) + 0.4, INI(E3, 2) + 2.0)), capa=2)


snd(T0(E3) + 0.2, "hmm", 0.3)
for _k in range(6):
    snd(38.8 + _k * 0.7, "golpe_suave", 0.25)
snd(T_ROMPE, "impacto", 0.7)
snd(T_ROMPE + 0.1, "puf", 0.5)
snd(T_ROMPE + 0.4, "revelar", 0.5)
snd(w_(E3, 1, 16), "bling", 0.5)
snd(w_(E3, 1, 17), "clink", 0.4)
snd(w_(E3, 1, 19), "brillo", 0.4)
snd(INI(E3, 2) + 0.4, "zoom_whoosh", 0.3, dur=1.0)

# ======================================================================== 4. VALOR (jade, plumas, oro)
E4 = "valor"


def _podio(lz, t, alt, x, w, col, col2, top_icon, label, num):
    """Columna del podio con altura animada; icono encima y rótulo debajo."""
    yb = 820.0
    lz.relleno(rect_red(x - w / 2, yb - alt, w, alt, 10), col)
    lz.relleno(rect_red(x - w / 2, yb - alt, w, 14, 6), col2)
    lz.relleno(rect_red(x - w / 2 + w * 0.68, yb - alt + 14, w * 0.32, alt - 14, 0), P.oscurecer(col, 0.14))
    if alt > 40:
        P.rotulo(lz, x, yb - alt * 0.45, str(num), px=100 if alt > 200 else 70, color=(255, 255, 255), sombra=0.25, alfa=0.9)
    top_icon(x, yb - alt - 30)
    P.pastilla(lz, x, yb + 44, label, px=36)


@shot(T0(E4), bg=lambda t: bg_grad((44, 30, 110), (18, 12, 56)), ent=("aberracion", 0.6))
def v_podio(lz, t):
    # partículas de fondo
    for i in range(50):
        x = W * h01(51, i)
        y = (H * h01(52, i) - t * (12 + 20 * h01(53, i))) % H
        lz.relleno(circulo(x, y, 2 + 3 * h01(54, i), 8), (255, 255, 255), alfa=0.12)
    mex = 1.0 - smooth(prog(t, w_(E4, 3, 0) - 0.3, w_(E4, 3, 0) + 1.0))
    ind_e = 1.0 - mex
    # alturas de los tres pilares: mexicas jade > plumas > oro; españoles oro >> resto
    a_jade = lerp(60, 360, smooth(prog(t, w_(E4, 1, 3) - 0.2, w_(E4, 1, 3) + 1.0))) * mex + 40 * ind_e
    a_plum = lerp(60, 250, smooth(prog(t, w_(E4, 1, 6) - 0.2, w_(E4, 1, 6) + 1.0))) * mex + 40 * ind_e
    a_oro = lerp(60, 150, smooth(prog(t, w_(E4, 0, 5) - 0.2, w_(E4, 0, 5) + 1.0))) * mex + 400 * ind_e
    aa = smooth(prog(t, T0(E4) + 0.2, T0(E4) + 1.0))
    xs = (500, 960, 1420)
    if aa > 0.01:
        _podio(lz, t, a_plum * aa, xs[0], 300, (60, 170, 130), (110, 226, 170), lambda x, y: F.pluma(lz, x, y + 20, 0.8, 0.1, (60, 200, 130), t), "Plumas de quetzal", 2)
        _podio(lz, t, a_jade * aa, xs[1], 300, (44, 150, 200), (110, 200, 240), lambda x, y: F.jade(lz, x, y, 1.3, t), "Jade", 1)
        _podio(lz, t, a_oro * aa, xs[2], 300, (214, 150, 40), (255, 206, 72), lambda x, y: F.barra_oro(lz, x, y - 10, 0.95, 0.0, 0.5 + 0.4 * ind_e), "Oro", 3 if mex > 0.5 else 1)
    # títulos
    tt = P.mezcla((255, 255, 255), (255, 206, 72), ind_e)
    P.rotulo(lz, W / 2, 130, "Para los mexicas" if mex > 0.5 else "Para los españoles", px=76, color=tt, alfa=aa)
    # sol y "excremento de los dioses"
    sa = vent(t, w_(E4, 2, 3) - 0.2, w_(E4, 2, 7) + 1.0, 0.4, 0.4)
    if sa > 0.01:
        with lz.capa(2):
            F.disco(lz, 1560, 300, 74 * sa, t, "oro", rot=t * 0.4)
            P.pastilla(lz, 1560, 410, "teocuitlatl", px=34, alfa=sa)
            P.pastilla(lz, 1560, 468, "«excremento de los dioses»", px=30, alfa=sa)
    # un noble mexica admira el jade; un soldado español abraza el oro
    F.tlatoani(lz, 130 - 260 * (1 - mex), 860, 1.7, t, lado=1, brazos=0.35 + 0.1 * math.sin(t * 3), seed=2)
    F.soldado(lz, 1800 + 260 * mex, 860, 1.7, t, lado=-1, brazos=(-2.6, 2.6) if ind_e > 0.5 else (-0.3, 0.3), seed=7, carga=0.3)
    # fuego que derrite para los españoles
    fa = smooth(prog(t, w_(E4, 3, 4), w_(E4, 3, 6)))
    if fa > 0.01:
        with lz.capa(2):
            for k in range(3):
                llama(lz, 1160 + k * 100, 700, 0.9, t, seed=k, alfa=fa)
            P.pastilla(lz, 1420, 940 - 200, "metal para fundir", px=38, alfa=fa)


snd(T0(E4) + 0.3, "whoosh", 0.4, dur=0.6)
snd(w_(E4, 1, 3), "ding", 0.35)
snd(w_(E4, 1, 6), "ding", 0.3, tono=0.9)
snd(w_(E4, 0, 5), "ding", 0.25, tono=0.8)
snd(w_(E4, 2, 3), "brillo", 0.4)
snd(w_(E4, 3, 0), "zoom_whoosh", 0.4, dur=0.9)
snd(w_(E4, 3, 4), "fuego", 0.4, dur=2.5)
