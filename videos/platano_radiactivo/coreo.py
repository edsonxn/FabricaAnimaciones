# -*- coding: utf-8 -*-
"""Tu plátano es radiactivo: gancho, potasio, atomos, dosis, cuerpo, cierre."""
import math

import cv2
import numpy as np

import sh_kit as K
import sh_props as X
import sh_pintura as P
from sh_motor import FIN, INI, T, escena
from sh_util import balistica, bump, estela, kf, pulso
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY
VERDE_RAD = (150, 255, 110)


# ------------------------------------------------------------------ fondos
def capas_cocina():
    pared = P.fondo_liso(5, (150, 218, 204), (116, 190, 182), [(520, 0.7, (170, 230, 214), .5), (300, 1.2, (130, 204, 190), .4)])
    P.azulejos(pared, (96, 164, 160), 128, 5)
    P.textura(pared, 0.02, 0.03)
    mid = P.vacio()
    # estante con frascos
    cv2.rectangle(mid, (MX + 60, MY + 640), (MX + 1020, MY + 668), (150, 104, 70, 255), -1)
    for k, (x, col) in enumerate([(120, (250, 120, 100)), (240, (250, 214, 90)), (360, (120, 190, 250)), (700, (250, 160, 90)), (840, (170, 220, 120)),
                                  (950, (230, 140, 200))]):
        P.mancha(mid, MX + x, MY + 580, 44, 56, col, k + 1, rough=0.03)
        cv2.rectangle(mid, (MX + x - 30, MY + 514), (MX + x + 30, MY + 534), (190, 150, 100, 255), -1)
    P.textura(mid, 0.015, 0.03)
    cerca = P.vacio()
    cv2.rectangle(cerca, (0, BH - 430), (BW, BH), (176, 120, 80, 255), -1)
    cv2.rectangle(cerca, (0, BH - 440), (BW, BH - 410), (214, 160, 110, 255), -1)
    for k in range(5):
        cv2.line(cerca, (0, BH - 380 + k * 80), (BW, BH - 380 + k * 80), (140, 92, 62, 255), 4)
    P.textura(cerca, 0.02, 0.04)
    return [(pared, 0.25), (mid, 0.5), (cerca, 1.0)]


def capas_lab(c0=(18, 50, 56), c1=(40, 110, 100)):
    far = P.fondo_liso(11, c0, c1, [(520, 0.6, (30, 90, 90), .6), (320, 1.1, (60, 150, 120), .45), (230, 1.6, (120, 220, 130), .3)])
    return [(far, 0.3)]


def capas_clinica():
    pared = P.fondo_liso(21, (200, 226, 246), (160, 200, 236), [(520, 0.8, (214, 236, 252), .5), (300, 1.2, (150, 190, 232), .4)])
    P.azulejos(pared, (136, 176, 220), 170, 5)
    P.textura(pared, 0.02, 0.03)
    suelo = P.vacio()
    cv2.rectangle(suelo, (0, BH - 380), (BW, BH), (120, 160, 210, 255), -1)
    cv2.rectangle(suelo, (0, BH - 392), (BW, BH - 368), (228, 238, 250, 255), -1)
    P.textura(suelo, 0.02, 0.04)
    return [(pared, 0.25), (suelo, 1.0)]


def capas_noche():
    far = P.fondo_liso(31, (36, 30, 84), (92, 60, 140), [(520, 0.7, (70, 50, 130), .55), (320, 1.2, (110, 76, 160), .4)])
    return [(far, 0.3)]


# ------------------------------------------------------------------ utilidades
def chispas_rad(img, cx, cy, t, n=14, r0=150, r1=420, col=(150, 255, 110), a0=0.0):
    for i in range(n):
        ang = a0 + 2 * pi * i / n + 0.4 * math.sin(i * 1.7)
        ph = (t * 1.1 + i * 0.173) % 1.0
        rr = lerp(r0, r1, ph)
        estela(img, cx + rr * math.cos(ang), cy + rr * math.sin(ang), ang, 90, 10, 30, t * 9 + i, col, 5 * (1 - ph) + 2, cabeza=False)


def destello(img, x, y, r, col=(190, 255, 140)):
    P.halo(img, x, y, r, col, 0.9, 4)
    P.disco(img, x, y, r * 0.28, (250, 255, 230), 1.0)


def flash(out, a, col=255):
    if a <= 0.01:
        return out
    return np.clip(out.astype(np.float32) * (1 - a) + col * a, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ 1. gancho
@escena("gancho")
def gancho(C, t):
    t0 = INI("gancho")
    t_rad, t_pl = T("gancho", "radiactivo"), T("gancho", "platano", frase=1)
    capas = C.capas_de("cocina", capas_cocina)
    u = t / (FIN("gancho") - t0)
    C.cam = (1.0 + 0.05 * u + bump(t, t_rad, 0.5, 0.05) + bump(t, t_pl, 0.5, 0.06), 6 * math.sin(t * 0.8) + 14 * math.sin(t * 50) * pulso(t, t_rad, 0.5), -20 * u)
    img = C.base("gancho", capas)
    bx, by = C.xy(540, 800)
    if t > t_rad:
        k = min(1.0, (t - t_rad) * 2)
        P.halo(img, bx, by + 100, (520 + 40 * math.sin(t * 6)) * k, VERDE_RAD, 0.8, 6)
        chispas_rad(img, bx, by + 100, t, 16, 200, 560, VERDE_RAD)
    C.fondo(img)
    # fruta inocente en el frutero
    C.pon(X.cuenco(), 540, 1330, 1.7, 0.0, vida=0.4)
    C.pon(X.platano("grandes", "sonrisa"), 400, 1180, 0.7, -0.5, t_in=t0 + 0.05, vida=0.6)
    C.pon(X.platano("grandes", "sonrisa"), 690, 1190, 0.7, 0.5, t_in=t0 + 0.1, vida=0.6)
    # el símbolo de radiactividad, enorme, y los rótulos
    g = e_inout(prog(t, t_pl - 0.1, t_pl + 0.5))
    sc = lerp(1.3 + 1.4 * e_out(prog(t, t_rad - 0.2, t_rad + 0.25)), 1.0, g)
    C.pon(X.trebol(), lerp(540, 150, g), lerp(760, 520, g), sc, t * 0.5, vida=1.0)
    C.rot("ALGO", 540, 270, 130, -0.04, (255, 236, 120), s=1 + bump(t, t0 + 0.9, 0.3, 0.1), t_out=t_pl, d_out=0.2)
    C.rot("RADIACTIVO", 540, 420, 120, 0.03, (150, 255, 110), s=1 + bump(t, t_rad, 0.35, 0.18), t_out=t_pl, d_out=0.2, tira=True)
    # y sale el plátano
    if t >= t_pl:
        u2 = prog(t, t_pl, t_pl + 0.6)
        x, y = balistica(t, t_pl, t_pl + 0.6, (540, 1200), (540, 860), 380)
        C.pon(X.platano("grandes", "sonrisa" if t < t_pl + 1.4 else "o"), x, y, lerp(0.8, 2.6, e_out(u2)), 0.2 * math.sin(t * 3) * (u2), vida=1.5)
        C.rot("¡UN PLÁTANO!", 540, 300, 118, 0.03, (255, 236, 120), t_in=t_pl + 0.2, dur=0.3, tira=True)
    out = C.fin()
    return flash(out, pulso(t, t_rad, 0.3) * 0.5 + pulso(t, t_pl, 0.25) * 0.3)


# ------------------------------------------------------------------ 2. potasio
@escena("potasio")
def potasio(C, t):
    t0 = INI("potasio")
    t_pot, t_cor, t_mus = T("potasio", "potasio"), T("potasio", "corazon"), T("potasio", "musculos")
    t_rad = T("potasio", "radiactiva", frase=1)
    capas = C.capas_de("cocina", capas_cocina)
    C.cam = (1.0 + 0.05 * (t - t0) / (FIN("potasio") - t0), 8 * math.sin(t * 0.7), -14 * math.cos(t * 0.5))
    img = C.base("potasio", capas)
    if t > t_rad:
        k = min(1.0, (t - t_rad) * 3)
        P.halo(img, *C.xy(540, 1150), 420 * k * (1 + 0.05 * math.sin(t * 8)), VERDE_RAD, 0.6, 5)
    C.fondo(img)
    # frase 1: el plátano (con una K enorme), el corazón y el músculo
    sale = t_rad - 0.2
    C.pon(X.platano("grandes", "sonrisa"), 540, 640, 1.9, 0.05 * math.sin(t * 2), t_in=t0 + 0.1, t_out=sale, d_out=0.3, sale="sube_fuera", vida=1.2)
    C.rot("K", 540, 980, 330, -0.03, (150, 220, 255), t_in=t_pot, dur=0.35, t_out=sale, d_out=0.3)
    C.rot("POTASIO", 540, 1190, 120, 0.03, (255, 236, 120), t_in=t_pot + 0.1, dur=0.3, t_out=sale, d_out=0.3, tira=True)
    lat = 1 + 0.12 * max(0.0, math.sin(t * 7.5)) ** 2
    C.pon(K.corazon(48), 230, 1420, 2.2 * lat, 0.0, t_in=t_cor, t_out=sale, d_out=0.3)
    C.pon(X.biceps(), 800, 1440, 1.1, 0.0, t_in=t_mus, t_out=sale, d_out=0.3, vida=1.2)
    # frase 2: entre los átomos de potasio, uno solo es radiactivo
    if t >= sale + 0.2:
        cols = 4
        for i in range(12):
            gx, gy = 190 + (i % cols) * 230, 760 + (i // cols) * 230
            rad = (i == 6)
            tin = sale + 0.35 + 0.05 * i
            if rad:
                C.pon(X.bola_k(True), gx, gy, 2.1 * (1 + 0.06 * math.sin(t * 9)), 0.0, t_in=tin, modo="pop", vida=1.5)
                C.rot("K", gx, gy - 4, 90, 0.0, (40, 70, 40), t_in=tin + 0.05)
            else:
                C.pon(X.bola_k(False), gx, gy, 1.9, 0.0, t_in=tin, modo="pop", vida=0.6)
                C.rot("K", gx, gy - 4, 80, 0.0, (60, 90, 140), t_in=tin + 0.05)
        C.pon(X.trebol(), 190 + 2 * 230 + 30, 760 + 230 - 160, 0.9, t * 0.5, t_in=t_rad, dur=0.3)
        C.rot("¡RADIACTIVO!", 540, 420, 124, -0.04, (150, 255, 110), t_in=t_rad, dur=0.3, tira=True)
        C.rot("K-40", 540, 1520, 150, 0.03, (255, 236, 120), t_in=t_rad + 0.4, dur=0.3)
    return C.fin()


# ------------------------------------------------------------------ 3. átomos
@escena("atomos")
def atomos(C, t):
    t0 = INI("atomos")
    t_q = T("atomos", "quince")
    t_c = T("atomos", "cada", frase=1)
    capas = C.capas_de("lab", capas_lab)
    C.cam = (1.0 + 0.05 * (t - t0) / (FIN("atomos") - t0), 6 * math.sin(t * 0.9), -10 * math.cos(t * 0.6))
    img = C.base("atomos", capas)
    bx, by = C.xy(540, 900)
    P.halo(img, bx, by, 520 + 24 * math.sin(t * 6), VERDE_RAD, 0.35, 6)
    # ondas de radiación que salen del plátano
    for k in range(4):
        ph = ((t - t0) * 0.6 + k / 4) % 1.0
        cv2.circle(img, (int(bx * 4), int(by * 4)), int((160 + 480 * ph) * 4), (160, 255, 130), max(1, int(10 * (1 - ph)) + 1), cv2.LINE_AA, 2)
    C.fondo(img)
    C.pon(X.platano("grandes", "sonrisa"), 540, 840, 2.7, 0.04 * math.sin(t * 3), t_in=t0 + 0.05, vida=1.4)
    # cronómetro: un segundo = una vuelta
    C.pon(K.cronometro(2 * pi * ((t - t0) % 1.0)), 880, 420, 1.5, 0.0, t_in=t0 + 0.2, dur=0.3)
    C.rot("1 SEGUNDO", 880, 560, 52, 0.04, (255, 246, 214), t_in=t0 + 0.4, dur=0.25)
    C.rot("15", 330, 1370, 300, -0.04, (150, 255, 110), t_in=t_q, dur=0.3)
    C.rot("ÁTOMOS SE ROMPEN", 540, 1590, 90, 0.02, (255, 246, 214), t_in=T("atomos", "desintegran"), dur=0.3, tira=True)
    C.rot("UN POQUITO DE", 540, 300, 80, -0.03, (255, 236, 120), t_in=t_c + 0.2, dur=0.3)
    C.rot("RADIACIÓN", 540, 410, 110, 0.03, (150, 255, 110), t_in=t_c + 0.5, dur=0.3, tira=True)
    out = C.fin()
    if t > t0 + 0.5:                                      # 15 destellos por segundo, por delante del plátano
        for j in range(4):
            n = int(t * 15) - j
            rr = np.random.default_rng(n * 7 + 3)
            a_ = rr.uniform(0, 2 * pi)
            d_ = rr.uniform(0.2, 1)
            px, py = 540 + 300 * math.cos(a_) * d_, 840 + 120 * math.sin(a_) * d_ - 20
            age = t * 15 - n
            if 0 <= age < 4:
                destello(out, *C.xy(px, py), 86 * (1 - age / 4) + 14)
    return out


# ------------------------------------------------------------------ 4. dosis
@escena("dosis")
def dosis(C, t):
    t0 = INI("dosis")
    t_dim = T("dosis", "diminuta")
    t_rx, t_cin = T("dosis", "radiografia", frase=1), T("dosis", "cincuenta", frase=1)
    t_det = T("dosis", "detector", frase=2)
    capas = C.capas_de("clinica", capas_clinica)
    C.cam = (1.0 + 0.04 * (t - t0) / (FIN("dosis") - t0), 6 * math.sin(t * 0.7), -10 * math.cos(t * 0.5))
    img = C.base("dosis", capas)
    C.fondo(img)
    C.rot("DOSIS", 540, 300, 150, -0.04, (255, 120, 120), t_in=t0 + 0.5, dur=0.3, t_out=t_rx - 0.1, d_out=0.2)
    C.rot("DIMINUTA", 540, 450, 130, 0.03, (110, 170, 255), t_in=t_dim, dur=0.3, tira=True, t_out=t_rx - 0.1, d_out=0.2)
    C.pon(X.platano("grandes", "sonrisa"), 540, 1000, 1.9, 0.0, t_in=t0 + 0.1, t_out=t_rx - 0.1, d_out=0.25, vida=1.0)
    # ecuación: 1 radiografía dental = 50 plátanos
    if t_rx - 0.1 <= t < t_det + 0.3:
        C.pon(X.diente("grandes", "sonrisa"), 250, 640, 1.8, 0.04 * math.sin(t * 2), t_in=t_rx, dur=0.4, vida=1.0, t_out=t_det, d_out=0.3, sale="sube_fuera")
        C.rot("RADIOGRAFÍA", 250, 880, 64, -0.04, (255, 246, 214), t_in=t_rx + 0.2, dur=0.3, tira=True, t_out=t_det, d_out=0.3)
        C.rot("=", 540, 640, 230, 0.0, (255, 236, 120), t_in=t_rx + 0.9, dur=0.3, t_out=t_det, d_out=0.3)
        C.pon(X.platano("grandes", "sonrisa"), 830, 640, 0.9, 0.0, t_in=t_rx + 1.0, dur=0.4, vida=1.0, t_out=t_det, d_out=0.3, sale="sube_fuera")
        C.rot("×50", 830, 860, 150, 0.03, (150, 255, 110), t_in=t_cin, dur=0.3, t_out=t_det, d_out=0.3)
        # los 50 plátanos van cayendo en fila
        n = int(50 * smooth(prog(t, t_cin - 0.1, t_cin + 2.2)))
        for i in range(n):
            gx, gy = 80 + (i % 10) * 102, 1130 + (i // 10) * 118
            C.pon(X.platano("", ""), gx, gy, 0.3, 0.0, t_in=t_cin - 0.1 + i * 0.045, modo="cae", dur=0.3, vida=0.4, peg=True)
    # el detector de radiación
    if t >= t_det:
        C.pon(X.detector(0.0 + 0.7 * math.sin(t * 11) * math.sin(t * 3.1) ** 2), 540, 1080, 2.5, 0.0, t_in=t_det, modo="sube", dur=0.4, vida=1.0)
        C.pon(X.platano("grandes", "o"), 880, 1300, 1.0, -0.2, t_in=t_det + 0.1, dur=0.3, vida=1.0)
        for k in range(3):
            tt = t_det + 0.35 + 0.4 * k
            C.rot("¡CLIC!", 200 + 240 * k, 560 - 40 * (k % 2) + 80 * k, 96, (-0.1, 0.08, -0.05)[k], (255, 236, 120), t_in=tt, dur=0.15, t_out=tt + 0.35, d_out=0.12)
    return C.fin()


# ------------------------------------------------------------------ 5. cuerpo
@escena("cuerpo")
def cuerpo(C, t):
    t0 = INI("cuerpo")
    t_pot, t_4 = T("cuerpo", "potasio"), T("cuerpo", "cuatro", frase=1)
    capas = C.capas_de("noche", capas_noche)
    C.cam = (1.0 + 0.05 * (t - t0) / (FIN("cuerpo") - t0), 8 * math.sin(t * 0.7), -12 * math.cos(t * 0.5))
    img = C.base("cuerpo", capas)
    bx, by = C.xy(540, 1000)
    k = prog(t, t0 + 0.2, t0 + 1.0)
    P.halo(img, bx, by, 560 * k, VERDE_RAD, 0.5, 6)
    if t > t_4:
        # chisporroteo de desintegraciones: miles por segundo
        nn = int(min(1.0, (t - t_4) / 0.8) * 34)
        for i in range(nn):
            rr = np.random.default_rng(int(t * 24) * 131 + i)
            px, py = 540 + rr.uniform(-170, 170), 1000 + rr.uniform(-330, 330)
            destello(img, *C.xy(px, py), rr.uniform(18, 44))
    C.fondo(img)
    ojos = "grandes" if t < t_4 else "miedo"
    boca = "sonrisa" if t < t_4 else "o"
    C.pon(K.persona(ojos, boca, "abajo"), 540, 1020, 2.2 * (1 + bump(t, t_4, 0.4, 0.04)), 0.0, t_in=t0 + 0.05, modo="pop", vida=1.0 + 1.5 * prog(t, t_4, t_4 + 0.6))
    # átomos de potasio dentro del cuerpo
    for i, (dx, dy) in enumerate([(-110, -40), (110, -30), (-30, 80), (70, 150), (-120, 160), (0, -150)]):
        tin = t_pot + 0.1 * i
        C.pon(X.bola_k(i % 3 == 0), 540 + dx, 1020 + dy, 0.8, 0.0, t_in=tin, dur=0.25, vida=1.0)
    C.rot("TÚ TAMBIÉN", 540, 300, 120, -0.04, (255, 236, 120), t_in=t0 + 0.4, dur=0.3, t_out=t_4 - 0.1, d_out=0.2)
    C.rot("TIENES POTASIO", 540, 440, 100, 0.03, (150, 220, 255), t_in=t_pot, dur=0.3, tira=True, t_out=t_4 - 0.1, d_out=0.2)
    if t >= t_4:
        v = 4000 * e_out(prog(t, t_4, t_4 + 1.0))
        C.rot(f"{int(v):,}".replace(",", " "), 540, 330, 190, -0.03, (150, 255, 110), t_in=t_4, dur=0.3)
        C.rot("POR SEGUNDO", 540, 480, 100, 0.03, (255, 246, 214), t_in=t_4 + 0.6, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 6. cierre
@escena("cierre")
def cierre(C, t):
    t0 = INI("cierre")
    t_mil = T("cierre", "millones")
    t_in = T("cierre", "inocente", frase=1)
    t_dis = T("cierre", "distinto", frase=2)
    capas = C.capas_de("cocina", capas_cocina)
    C.cam = (1.0 + 0.05 * (t - t0) / (FIN("cierre") - t0), 8 * math.sin(t * 0.6), -12 * math.cos(t * 0.5))
    img = C.base("cierre", capas)
    if t_in <= t < t_dis:
        P.halo(img, *C.xy(540, 860), 520, (255, 246, 190), 0.7, 6)
    C.fondo(img)
    f2 = t < T("cierre", "tranquilo", frase=1) - 0.2
    # frase 1: lluvia de plátanos hasta formar una montaña
    if t < t_in - 0.1:
        C.pon(K.persona("miedo", "grito", "arriba"), 540, 1500, 1.5, 0.0, t_in=t0 + 0.1, vida=2.0, t_out=t_in - 0.1, d_out=0.25, sale="baja")
        npl = int(46 * smooth(prog(t, t0 + 0.3, t_mil + 2.0)))
        for i in range(npl):
            r = np.random.default_rng(i * 17 + 3)
            gx, gy = 80 + (i * 83) % 920 + 20 * math.sin(i), 1800 - (i // 9) * 100 - (i % 3) * 20
            C.pon(X.platano("", ""), gx, gy, 0.44, r.uniform(-0.6, 0.6), t_in=t0 + 0.3 + i * 0.12, modo="cae", dur=0.35, vida=0.3)
        C.rot("MILLONES", 540, 330, 190, -0.04, (255, 236, 120), t_in=t_mil, dur=0.3, t_out=t_in - 0.1, d_out=0.2)
        C.rot("DE GOLPE", 540, 500, 120, 0.03, (255, 120, 120), t_in=t_mil + 0.5, dur=0.3, tira=True, t_out=t_in - 0.1, d_out=0.2)
    # frase 2: el plátano inocente, con aureola
    if t >= t_in - 0.1:
        C.pon(X.platano("feliz", "sonrisa") if t < t_dis else X.platano("guino", "lengua"), 540, 880, 2.6, 0.05 * math.sin(t * 2.2), t_in=t_in - 0.1, vida=1.2)
        C.pon(X.aureola(), 540, 690 + 8 * math.sin(t * 3), 2.4, 0.0, t_in=t_in, dur=0.35)
        C.rot("INOCENTE", 540, 1300, 150, -0.03, (255, 236, 120), t_in=t_in, dur=0.3, tira=True)
        for j, (dx, dy, tt) in enumerate([(-330, -240, t_in + 0.3), (340, -220, t_in + 0.45), (-320, 250, t_in + 0.6), (330, 230, t_in + 0.75)]):
            C.pon(K.CHISPA, 540 + dx, 880 + dy + 8 * math.sin(t * 3 + j), 0.8, t * 0.5 + j, t_in=tt, modo="pop", dur=0.3)
    if t >= t_dis:
        C.pon(X.trebol(), 880, 600, 0.9, t * 0.8, t_in=t_dis, dur=0.3)
        C.rot("¡OJO!", 220, 640, 110, -0.08, (150, 255, 110), t_in=t_dis + 0.4, dur=0.25)
    return C.fin()
