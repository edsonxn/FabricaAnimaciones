# -*- coding: utf-8 -*-
"""¿Cuánto pesa una nube?: gancho, peso, gotas, aire, lluvia, cierre."""
import math

import cv2
import numpy as np

import sh_kit as K
import sh_props as X
import sh_pintura as P
from sh_motor import FIN, INI, T, escena
from sh_util import balistica, bump, kf, pulso
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY
CREMA = (255, 250, 232)
AZUL_T = (60, 120, 230)
NARANJA = (255, 140, 70)


def flash(out, a, col=255):
    if a <= 0.01:
        return out
    return np.clip(out.astype(np.float32) * (1 - a) + col * a, 0, 255).astype(np.uint8)


def capas_cielo(seed=5, c0=(96, 170, 248), c1=(190, 228, 255), colinas=True, gris=0.0):
    far = P.fondo_liso(seed, c0, c1, [(520, 0.7, (150, 200, 252), .55), (300, 1.2, (214, 238, 255), .5), (220, 1.6, (255, 255, 255), .25)])
    cap = [(far, 0.25)]
    if colinas:
        h1 = P.vacio()
        P.mancha(h1, 300, BH - 220, 700, 300, (118, 196, 120), seed + 1, rough=0.06)
        P.mancha(h1, 900, BH - 180, 760, 280, (96, 176, 110), seed + 2, rough=0.06)
        P.textura(h1, 0.02, 0.04)
        h2 = P.vacio()
        P.mancha(h2, 120, BH - 70, 560, 220, (74, 150, 90), seed + 3, rough=0.05)
        P.mancha(h2, 980, BH - 40, 600, 220, (62, 136, 80), seed + 4, rough=0.05)
        P.textura(h2, 0.02, 0.04)
        cap += [(h1, 0.6), (h2, 1.0)]
    return cap


def cam_suave(C, t, a, b, z=0.05):
    u = (t - a) / max(1e-6, b - a)
    C.cam = (1.0 + z * u, 8 * math.sin(t * 0.7), -10 * math.cos(t * 0.5))


def sol_cielo(img, x, y, t, r=110):
    P.halo(img, x, y, r * 3.4, (255, 240, 170), 0.55, 6)
    P.rayos(img, x, y, r, r * 2.2, 14, t * 0.3, [(255, 226, 120)], 0.5, 0.4)
    P.disco(img, x, y, r, (255, 236, 130), 1.0)


# ------------------------------------------------------------------ 1. gancho
@escena("gancho")
def gancho(C, t):
    t0 = INI("gancho")
    t_ele, t_flo = T("gancho", "elefantes"), T("gancho", "flota", frase=1)
    capas = C.capas_de("dia", capas_cielo)
    cam_suave(C, t, t0, FIN("gancho"))
    img = C.base("gancho", capas)
    sol_cielo(img, *C.xy(900, 280), t)
    C.fondo(img)
    # la nube arriba, los elefantes abajo
    subida = 70 * e_inout(prog(t, t_flo, t_flo + 1.2))
    C.pon(X.nube("grandes", "sonrisa" if t < t_flo else "o"), 540, 500 - subida + 14 * math.sin(t * 1.6), 1.55, 0.02 * math.sin(t * 1.3), t_in=t0 + 0.05, vida=1.0)
    C.rot("=", 540, 900, 220, 0.0, (255, 236, 120), t_in=T("gancho", "mismo"), dur=0.3, t_out=t_flo + 0.1, d_out=0.2)
    n = int(6 * smooth(prog(t, t_ele - 0.2, t_ele + 1.0)))
    for i in range(6):
        gx, gy = 200 + (i % 3) * 330, 1150 + (i // 3) * 330
        C.pon(X.elefante("grandes", "sonrisa"), gx, gy, 0.82, 0.04 * math.sin(t * 2 + i), t_in=(None if i == 0 else t_ele - 0.2 + 0.15 * i), modo="cae", dur=0.4, vida=0.5, flip=(i % 2 == 1),
              t_out=t_flo + 0.1, d_out=0.3, sale="baja")
    C.rot("×80", 840, 930, 160, -0.04, (255, 120, 90), t_in=t_ele, dur=0.3, t_out=t_flo + 0.1, d_out=0.2, tira=True)
    C.rot("¿Y NO CAE?", 540, 1330, 130, 0.03, (255, 236, 120), t_in=t_flo + 0.3, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 2. peso
@escena("peso")
def peso(C, t):
    t0 = INI("peso")
    t_500, t_ton = T("peso", "quinientas"), T("peso", "toneladas")
    t_med, t_lit = T("peso", "medio", frase=1), T("peso", "litros", frase=1)
    capas = C.capas_de("dia2", lambda: capas_cielo(9))
    cam_suave(C, t, t0, FIN("peso"))
    img = C.base("peso", capas)
    # gotas que caen de la nube
    for i in range(14):
        ph = ((t - t0) * 0.7 + i / 14) % 1.0
        cv2.circle(img, (int((220 + (i * 137) % 640 + 20 * math.sin(i)) * 4), int((620 + ph * 760) * 4)), int(10 * 4), (92, 150, 240), -1, cv2.LINE_AA, 2)
    C.fondo(img)
    C.pon(X.nube("grandes", "o"), 540, 470 + 10 * math.sin(t * 1.5), 1.6, 0.0, t_in=t0 + 0.05, vida=1.0)
    C.rot(f"{int(500 * e_out(prog(t, t_500, t_500 + 1.2)))} TONELADAS", 540, 330, 100, -0.03, (255, 236, 120), t_in=t_500, dur=0.3, tira=True) if t >= t_500 else None
    if t >= t_lit - 0.4:
        v = 500000 * e_out(prog(t, t_med, t_lit + 0.6))
        C.rot(f"{int(v):,}".replace(",", " "), 540, 1000, 170, 0.02, AZUL_T, t_in=t_med, dur=0.3)
        C.rot("LITROS DE AGUA", 540, 1170, 96, -0.02, CREMA, t_in=t_lit, dur=0.3, tira=True)
    C.pon(K.persona("miedo", "grito", "arriba"), 540, 1590, 1.2, 0.0, t_in=t0 + 0.5, vida=2.0)
    return C.fin()


# ------------------------------------------------------------------ 3. gotas
_rg = np.random.default_rng(3)
GOTAS = [(_rg.uniform(120, 960), _rg.uniform(500, 1500), _rg.uniform(0, 6.28), _rg.uniform(0.5, 1.1)) for _ in range(46)]


@escena("gotas")
def gotas(C, t):
    t0 = INI("gotas")
    t_mil, t_cm = T("gotas", "millones"), T("gotas", "centimetro", frase=1)
    capas = C.capas_de("gris", lambda: capas_cielo(13, (120, 150, 200), (196, 214, 240), colinas=False))
    cam_suave(C, t, t0, FIN("gotas"))
    img = C.base("gotas", capas)
    C.fondo(img)
    for i, (x, y, ph, s) in enumerate(GOTAS):
        C.pon(X.gotita("grandes" if i % 3 else "feliz", "sonrisa", 1.0), x + 18 * math.sin(t * 0.8 + ph), y + 10 * math.sin(t * 1.1 + ph * 2), 1.1 * s, 0.1 * math.sin(t + ph),
              t_in=t0 + 0.04 * i, modo="pop", dur=0.25, vida=0.7)
    C.rot("MILES DE MILLONES", 540, 300, 100, -0.03, (255, 236, 120), t_in=t_mil - 0.3, dur=0.3, tira=True)
    C.rot("DE GOTITAS", 540, 430, 120, 0.03, CREMA, t_in=t_mil + 0.3, dur=0.3)
    if t >= t_cm - 0.5:
        # una gotita cae despacísimo junto a una regla de 1 cm
        u = ((t - t_cm + 0.5) % 2.0) / 2.0
        C.pon(X.regla(3, 56), 930, 1020, 2.0, pi / 2, t_in=t_cm - 0.5, dur=0.3)
        C.pon(X.gotita("grandes", "sonrisa", 1.0), 800, 880 + 300 * u, 1.6, 0.0, t_in=t_cm - 0.4)
        C.rot("< 1 CM POR SEGUNDO", 540, 1640, 78, -0.02, (255, 150, 90), t_in=t_cm, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 4. aire
@escena("aire")
def aire(C, t):
    t0 = INI("aire")
    t_cal, t_emp = T("aire", "caliente"), T("aire", "empuja")
    t_cor = T("aire", "corriente", frase=1)
    capas = C.capas_de("dia3", lambda: capas_cielo(21))
    cam_suave(C, t, t0, FIN("aire"))
    img = C.base("aire", capas)
    sol_cielo(img, *C.xy(190, 300), t, 100)
    # ondas de calor sobre el suelo
    for k in range(5):
        y = 1500 - k * 40
        pts = np.array([(x, y + 10 * math.sin(x / 70 + t * 3 + k)) for x in range(0, W + 40, 40)])
        cv2.polylines(img, [np.rint(pts * 4).astype(np.int32).reshape(-1, 1, 2)], False, (255, 210, 130), 6, cv2.LINE_AA, 2)
    C.fondo(img)
    C.pon(X.nube("grandes", "sonrisa"), 560, 560 + 24 * math.sin(t * 1.2) - 20 * prog(t, t_emp, t_emp + 1.5), 1.5, 0.0, t_in=t0 + 0.05, vida=1.0)
    # flechas de aire caliente que suben
    for i in range(5):
        ph = ((t - t0) * 0.5 + i / 5) % 1.0
        x = 200 + i * 170
        C.pon(X.flecha_arriba((255, 140, 70), 220), x, 1500 - 700 * ph, 0.9 * (1 - 0.3 * ph), 0.0, t_in=t_cal - 0.2 + 0.1 * i, dur=0.3)
    C.rot("AIRE CALIENTE", 540, 300, 112, -0.03, (255, 150, 90), t_in=t_cal, dur=0.3, tira=True)
    C.rot("¡SUBE!", 760, 1280, 140, 0.05, (255, 236, 120), t_in=t_emp, dur=0.3)
    if t >= t_cor:
        C.rot("CORRIENTE INVISIBLE", 540, 1700, 78, 0.02, CREMA, t_in=t_cor, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 5. lluvia
@escena("lluvia")
def lluvia(C, t):
    t0 = INI("lluvia")
    t_jun, t_gra = T("lluvia", "juntan"), T("lluvia", "grandes")
    t_pes = T("lluvia", "demasiado")
    t_llu = T("lluvia", "llueve", frase=1)
    capas = C.capas_de("gris2", lambda: capas_cielo(27, (110, 130, 176), (176, 192, 226)))
    cam_suave(C, t, t0, FIN("lluvia"))
    img = C.base("lluvia", capas)
    # llueve
    if t >= t_pes:
        n = int(60 * smooth(prog(t, t_pes, t_llu + 0.6)))
        for i in range(n):
            x = (i * 97) % W
            y = ((t * (900 + (i % 5) * 120) + i * 211) % (H - 560)) + 560
            cv2.line(img, (int(x * 4), int(y * 4)), (int((x - 12) * 4), int((y + 52) * 4)), (96, 150, 240), 6, cv2.LINE_AA, 2)
    C.fondo(img)
    C.pon(X.nube("grandes" if t < t_pes else "miedo", "sonrisa" if t < t_pes else "o", gris=t >= t_jun), 540, 430 + 10 * math.sin(t * 1.5), 1.6, 0.0, t_in=t0 + 0.05, vida=1.0)
    # las gotas se juntan y crecen
    g = e_inout(prog(t, t_jun, t_gra + 0.8))
    for i in range(6):
        a = 2 * pi * i / 6
        x = lerp(540 + 330 * math.cos(a), 540, g)
        y = lerp(880 + 200 * math.sin(a), 880, g)
        if g < 0.98:
            C.pon(X.gotita("grandes", "sonrisa", 1.0), x, y, 1.0, 0.0, t_in=t0 + 0.3 + 0.07 * i, vida=0.8)
    if g >= 0.9:
        sz = 1.0 + 3.0 * e_out(prog(t, t_gra + 0.6, t_gra + 1.1))
        caer = 700 * e_in(prog(t, t_pes + 0.2, t_llu))
        C.pon(X.gotita("miedo", "grito", 1.0), 540, 900 + caer, sz, 0.0, vida=1.0)
    C.rot("MÁS GRANDES", 540, 1350, 120, -0.03, (255, 236, 120), t_in=t_gra, dur=0.3, t_out=t_pes, d_out=0.2, tira=True)
    C.rot("¡PESAN DEMASIADO!", 540, 1350, 84, 0.03, (255, 130, 90), t_in=t_pes, dur=0.3, tira=True, t_out=t_llu, d_out=0.2)
    if t >= t_llu - 0.3:
        C.pon(K.persona("feliz", "sonrisa", "abajo"), 400, 1590, 1.2, 0.0, t_in=t_llu - 0.3, vida=1.0)
        C.pon(X.paraguas(), 400, 1330, 1.25, 0.1 * math.sin(t * 2), t_in=t_llu, modo="pop", dur=0.3)
        C.rot("¡LLUEVE!", 540, 300, 190, -0.04, AZUL_T, t_in=t_llu, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 6. cierre
@escena("cierre")
def cierre(C, t):
    t0 = INI("cierre")
    t_rec, t_80 = T("cierre", "recuerda"), T("cierre", "ochenta", frase=1)
    capas = C.capas_de("dia4", lambda: capas_cielo(33))
    cam_suave(C, t, t0, FIN("cierre"))
    img = C.base("cierre", capas)
    sol_cielo(img, *C.xy(900, 250), t)
    C.fondo(img)
    C.pon(X.nube("grandes", "sonrisa"), 540, 560 + 12 * math.sin(t * 1.4), 1.9, 0.0, t_in=t0 + 0.05, vida=1.0)
    # elefantes flotando dentro de la nube
    n = int(10 * smooth(prog(t, t_80, t_80 + 1.5)))
    for i in range(10):
        gx = 170 + (i % 5) * 175
        gy = 520 + (i // 5) * 150 + 14 * math.sin(t * 1.3 + i)
        C.pon(X.elefante("feliz", "sonrisa"), gx, gy, 0.5, 0.2 * math.sin(t + i), t_in=t_80 - 0.1 + 0.12 * i, modo="pop", dur=0.3, vida=0.6, flip=(i % 2 == 1))
    C.pon(K.persona("grandes", "o", "abajo"), 540, 1500, 1.5, 0.0, t_in=t0 + 0.3, vida=0.8)
    C.rot("RECUERDA", 540, 1180, 100, -0.03, CREMA, t_in=t_rec, dur=0.3, t_out=t_80 - 0.1, d_out=0.2, tira=True)
    C.rot("80 ELEFANTES", 540, 1180, 120, 0.03, (255, 130, 90), t_in=t_80, dur=0.3, tira=True)
    return C.fin()
