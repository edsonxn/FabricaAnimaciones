# -*- coding: utf-8 -*-
"""Escenas 1-3: gancho, calor, higgs."""
import math

import cv2
import numpy as np

import kit as K
import pintura as P
from coreo_util import ORO, balistica, bump, estela, humo, kf, pulso
from escenas import FIN, INI, T, escena
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY

# =========================================================== 1. GANCHO
_r = np.random.default_rng(21)
N_F = 44
F_ANG = _r.uniform(-0.62, 0.62, N_F)
F_VEL = _r.uniform(520, 980, N_F)
F_OFF = _r.uniform(0, 2200, N_F)
F_PH = _r.uniform(0, 6.28, N_F)
F_COL = [(255, 222, 110), (255, 240, 170), (255, 196, 90), (255, 250, 220)]


def capas_gancho():
    far = P.cosmos(11, (14, 16, 52), (96, 42, 104), [(560, 0.7, (70, 46, 120), .55), (380, 1.1, (126, 58, 122), .35),
                                                   (260, 1.6, (190, 90, 110), .22)], estrellas=320)
    P.halo_estatico(far, BW / 2, MY + 30, 1000, (255, 160, 70), .6, 9)
    colinas_l = P.vacio()
    for (cx, cy, rx, ry, col, sd) in [(180, BH - 330, 560, 250, (86, 66, 150), 1), (900, BH - 300, 640, 270, (96, 74, 160), 2)]:
        P.mancha(colinas_l, cx, cy, rx, ry, col, sd, rough=0.08)
    P.textura(colinas_l)
    cerca = P.vacio()
    for (cx, cy, rx, ry, col, sd) in [(300, BH - 120, 700, 260, (44, 40, 104), 3), (880, BH - 80, 640, 240, (54, 48, 118), 4)]:
        P.mancha(cerca, cx, cy, rx, ry, col, sd, rough=0.07)
    P.textura(cerca)
    return [(far, 0.22), (colinas_l, 0.55), (cerca, 1.0)]


def tau(t):
    """Tiempo 'acelerado' de los fotones: ganan velocidad al decir «atravesándote»."""
    if t < 1.2:
        return t
    if t < 2.4:
        return t + 0.6 * (t - 1.2) ** 2 / 2.4              # integral de prog(t, 1.2, 2.4) = (t-1.2)^2 / 2.4
    return t + 0.6 * (0.6 + (t - 2.4))


def fotones_gancho(img, t, grupo, ox, oy, k):
    tt = tau(t)
    for i in range(N_F):
        if i % 2 != grupo:
            continue
        L = 2300.0
        s = (F_OFF[i] + F_VEL[i] * tt) % L
        a = F_ANG[i]
        x, y = ox + math.sin(a) * s, oy + math.cos(a) * s
        g = 4.0 + 6.0 * s / L
        estela(img, x, y, pi / 2 - a, 110 + 0.12 * F_VEL[i], 10 + 4 * s / L, 34, t * 7 + F_PH[i], F_COL[i % 4], g)


@escena("gancho")
def gancho(C, t):
    capas = C.capas_de("gancho", capas_gancho)
    u = t / 6.5
    sc = 1.0 + 0.05 * u + bump(t, 2.31, 0.5, 0.04) + bump(t, 3.88, 0.5, 0.05)
    C.cam = (sc, 10 * math.sin(t * 0.7), -26 * u)
    img = C.base("gancho", capas)
    bx, by = C.xy(540, 70, 0.22)
    # Big Bang: sol de rayos que gira + núcleo
    P.rayos(img, bx, by, 40, 1500, 22, t * 0.16, [(255, 214, 96), (255, 150, 72)], 0.34, 0.55)
    P.rayos(img, bx, by, 40, 900, 11, -t * 0.22 + 0.3, [(255, 244, 200)], 0.22, 0.4)
    P.halo(img, bx, by, 330 + 20 * math.sin(t * 5), (255, 236, 170), 0.9, 6)
    P.disco(img, bx, by, 118 + 8 * math.sin(t * 6), (255, 250, 226), 1.0)
    P.disco(img, bx, by, 150 + 8 * math.sin(t * 6), (255, 214, 120), 0.45)
    fotones_gancho(img, t, 0, bx, by + 60, 1.0)
    C.fondo(img)
    # la persona (tú) recibe la luz
    ojos, boca = "grandes", "o"
    if t >= 1.37:
        ojos = "miedo"
    if t >= 2.31:
        boca = "grito"
    if t >= 3.42:
        ojos, boca = "grandes", "o"
    vida = 1.0 + 2.2 * prog(t, 1.37, 2.0) * (1 - prog(t, 3.2, 3.5))
    tilt = 0.07 * prog(t, 3.42, 3.9)
    mv = e_inout(prog(t, 3.42, 3.95))                 # al presentar a Foti, «tú» baja y se hace pequeño
    C.pon(K.persona(ojos, boca, "abajo"), 540, lerp(1235, 1575, mv), lerp(2.05, 1.15, mv) * (1 + bump(t, 2.31, 0.3, 0.05)), tilt, vida=vida, sem=2)
    # rótulos
    s1 = 1 + bump(t, 0.45, 0.4, 0.14) + bump(t, 1.11, 0.4, 0.12)
    C.rot("LUZ DEL", 540, 330, 118, -0.05, (255, 224, 120), s=s1, tira=False, t_out=3.3, d_out=0.3)
    C.rot("BIG BANG", 540, 468, 150, 0.04, (240, 84, 60), s=s1, t_out=3.3, d_out=0.3)
    # Foti, el primer fotón
    y = lerp(120, 840, e_out(prog(t, 3.62, 4.25)))
    spin = (1 - e_out(prog(t, 3.62, 4.4))) * 2 * pi * 1.5
    C.foti(540, y + 8 * math.sin(t * 2.6), 3.0, spin, "grandes" if t < 5.2 else "feliz", "abierta" if t > 4.6 else "o", t_in=3.62, dur=0.55,
           largo=330, amp=24)
    for j, (dx, dy, tt) in enumerate([(-300, -190, 4.45), (310, -230, 4.62), (-340, 140, 4.8), (330, 110, 4.95)]):
        C.pon(K.CHISPA, 540 + dx, 840 + dy + 6 * math.sin(t * 3 + j), 0.7 + 0.12 * (j % 2), t * 0.4 + j, t_in=tt, modo="pop", dur=0.3)
    C.rot("¿CÓMO NACIÓ", 540, 330, 118, -0.04, (255, 224, 120), t_in=4.34, dur=0.32)
    C.rot("EL PRIMER FOTÓN?", 540, 470, 100, 0.03, (240, 84, 60), t_in=5.0, dur=0.34, tira=True)
    out = C.fin()
    fotones_gancho(out, t, 1, bx, by + 60, 1.0)          # los fotones «atraviesan» a la persona: se pintan por encima
    fl = pulso(t, 2.31, 0.28) * 0.35 + pulso(t, 3.62, 0.3) * 0.25
    if fl > 0.01:
        out = np.clip(out.astype(np.float32) * (1 - fl) + 255 * fl, 0, 255).astype(np.uint8)
    return out
