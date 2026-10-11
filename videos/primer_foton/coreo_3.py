# -*- coding: utf-8 -*-
"""Escenas 7-8: hoy (la luz llega fría e invisible; la estática de la tele) y cierre (zoom a la estática -> Big Bang)."""
import math

import cv2
import numpy as np

import kit as K
import pintura as P
from coreo_1 import capas_gancho
from coreo_util import bump, kf, pulso
from escenas import FIN, INI, escena, mascara_cambio, COL_BORDE
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY

TV_X, TV_Y, TV_S = 540, 1040, 2.5
PANT = K.TELE_PANT                                  # (x0, y0, x1, y1) locales
SCR_C = (TV_X + (PANT[0] + PANT[2]) / 2 * TV_S, TV_Y + (PANT[1] + PANT[3]) / 2 * TV_S)


def flash(out, a, col=255):
    if a <= 0.01:
        return out
    return np.clip(out.astype(np.float32) * (1 - a) + col * a, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ fondos
def capas_espacio():
    far = P.cosmos(81, (4, 8, 30), (16, 36, 84), [(520, 0.8, (24, 40, 110), .5), (340, 1.2, (40, 80, 150), .35), (240, 1.7, (90, 70, 160), .25)],
                   estrellas=340)
    return [(far, 0.3)]


def capas_sala():
    pared = P.lienzo((58, 44, 82), (98, 62, 90), 90).astype(np.float32)
    xx = np.arange(BW)[None, :]
    rayas = (np.sin(xx / 34.0) > 0.2).astype(np.float32)[..., None]
    pared[..., :3] *= (1 - 0.06 * rayas)
    pared = np.clip(pared, 0, 255).astype(np.uint8)
    P.textura(pared)
    # ventana nocturna
    cv2.rectangle(pared, (MX + 60, MY + 330), (MX + 370, MY + 790), (244, 232, 206, 255), -1)
    cv2.rectangle(pared, (MX + 84, MY + 354), (MX + 346, MY + 766), (22, 30, 78, 255), -1)
    r = np.random.default_rng(3)
    for _ in range(18):
        cv2.circle(pared, (int(MX + 90 + r.uniform(0, 250)), int(MY + 360 + r.uniform(0, 400))), int(r.uniform(1.5, 3.5)), (255, 244, 214, 255), -1, cv2.LINE_AA)
    P.mancha(pared, MX + 270, MY + 450, 44, 44, (255, 238, 190), 5, rough=0.02)
    cv2.line(pared, (MX + 215, MY + 354), (MX + 215, MY + 766), (244, 232, 206, 255), 12)
    cv2.line(pared, (MX + 84, MY + 560), (MX + 346, MY + 560), (244, 232, 206, 255), 12)
    # cuadro
    cv2.rectangle(pared, (MX + 790, MY + 340), (MX + 990, MY + 600), (160, 110, 80, 255), -1)
    cv2.rectangle(pared, (MX + 806, MY + 356), (MX + 974, MY + 584), (250, 224, 170, 255), -1)
    cv2.fillPoly(pared, [np.array([(MX + 806, MY + 584), (MX + 870, MY + 440), (MX + 910, MY + 500), (MX + 940, MY + 450), (MX + 974, MY + 584)])], (120, 90, 140, 255))
    cv2.circle(pared, (MX + 940, MY + 400), 20, (255, 170, 80, 255), -1, cv2.LINE_AA)
    suelo = P.vacio()
    cv2.rectangle(suelo, (0, BH - 560), (BW, BH), (126, 80, 62, 255), -1)
    for k in range(9):
        cv2.line(suelo, (0, BH - 560 + k * 64), (BW, BH - 560 + k * 64), (96, 58, 48, 255), 4)
    cv2.rectangle(suelo, (0, BH - 580), (BW, BH - 552), (232, 214, 190, 255), -1)
    P.mancha(suelo, BW / 2, BH - 250, 560, 110, (206, 88, 96), 8, rough=0.03)
    P.mancha(suelo, BW / 2, BH - 250, 400, 74, (236, 150, 120), 9, rough=0.03)
    P.textura(suelo)
    planta = P.vacio()
    for (dx, dy, rx, ry, rot) in [(-30, -60, 36, 120, -0.5), (20, -90, 34, 140, 0.1), (60, -50, 32, 110, 0.6), (-4, -30, 30, 90, -0.1)]:
        P.mancha(planta, MX + 950 + dx, BH - 570 + dy, rx, ry, (74, 160, 100), int(dx + 50), rot=rot, rough=0.06)
    cv2.rectangle(planta, (MX + 920, BH - 560), (MX + 990, BH - 480), (206, 112, 82, 255), -1)
    P.textura(planta)
    sofa = P.vacio()
    P.mancha(sofa, BW / 2, BH - 40, 760, 260, (92, 66, 140), 11, rough=0.03)
    P.mancha(sofa, 130, BH - 200, 160, 190, (112, 82, 160), 12, rough=0.05)
    P.mancha(sofa, BW - 130, BH - 200, 160, 190, (112, 82, 160), 13, rough=0.05)
    P.textura(sofa)
    return [(pared, 0.25), (suelo, 0.5), (planta, 0.6), (sofa, 1.0)]


# ------------------------------------------------------------------ sala con la tele
def tele_pantalla(C):
    x0, y0, x1, y1 = PANT
    ax, ay = C.xy(TV_X + x0 * TV_S, TV_Y + y0 * TV_S)
    bx, by = C.xy(TV_X + x1 * TV_S, TV_Y + y1 * TV_S)
    return ax, ay, bx, by


def sala(C, t, estatica_desde, t_tele, cam_zoom=1.0, brillo=1.0, fotones=True):
    capas = C.capas_de("sala", capas_sala)
    z = cam_zoom
    qx, qy = SCR_C
    C.cam = (z, -(qx - W / 2) * (z - 1) + 5 * math.sin(t * 0.7), -(qy - H / 2) * (z - 1) - 6 * math.cos(t * 0.5))
    img = C.base("sala", capas)
    # luz azulada de la tele sobre la pared y el suelo
    cx, cy = C.xy(qx, qy)
    if t >= estatica_desde:
        P.halo(img, cx, cy, 760 * C.k() * (1 + 0.04 * math.sin(t * 30)), (120, 190, 255), 0.55 * brillo, 6)
    C.fondo(img)
    C.pon(K.tele(), TV_X, TV_Y, TV_S, 0.0, t_in=t_tele, modo="sube", dur=0.55, vida=1.0 + 2.0 * bump(t, 51.03, 0.5, 1.0))
    return img


def estatica(out, C, t, desde, a=1.0):
    if t < desde:
        return
    ax, ay, bx, by = tele_pantalla(C)
    ruido_x = (ax, ay, bx, by)
    P.ruido_tele(out, ruido_x, t, redondeo=int(26 * C.k()), brillo=a)


# ------------------------------------------------------------------ 7. HOY
@escena("hoy")
def hoy(C, t):
    t0 = INI("hoy")
    if t < 49.3:                                                     # --- espacio frío
        capas = C.capas_de("espacio", capas_espacio)
        C.cam = (1.0 + 0.04 * prog(t, t0, 49.3), 0, 0)
        img = C.base("espacio", capas)
        r = np.random.default_rng(9)
        for i in range(60):                                          # estrellas que pasan: viajamos
            d = r.uniform(0.3, 1.0)
            x = (r.uniform(0, W) - t * 900 * d) % (W + 200) - 100
            y = r.uniform(0, H)
            cv2.line(img, (int(x * 4), int(y * 4)), (int((x + 60 * d) * 4), int(y * 4)), (200, 220, 255), int(2 + 3 * d), cv2.LINE_AA, 2)
        C.fondo(img)
        ap = e_out(prog(t, t0, 48.4))
        s = lerp(0.25, 2.3, ap)
        vis = 1 - prog(t, 48.89, 49.2)                                # «no la ves»: se borra y queda el lápiz
        fx = lerp(540, 540, 1) + 18 * math.sin(t * 40)                # tiembla de frío
        if t < 49.05:
            C.foti(fx, lerp(800, 960, ap) + 10 * math.sin(t * 3), s, 0.0, "esfuerzo", "zigzag", largo=420 * min(1, ap + 0.3), amp=22, frio=True,
                   u=(vis if vis > 0.1 else 0.1), lapiz=(1.0 if vis < 1 else 0.0), sem=3, vida=2.0)
        C.rot("TAN FRÍA", 540, 340, 150, -0.03, (150, 210, 255), t_in=48.39, dur=0.3, t_out=48.9, d_out=0.2, tira=True)
        C.rot("NO LA VES", 540, 340, 150, 0.03, (190, 200, 230), t_in=48.89, dur=0.3, tira=True)
        out = C.fin()
        if t > 49.0:                                                 # la corriente de fotones fríos pasa invisible: chispas pálidas
            pass
        return out
    # --- cambio pintado hacia la sala (iris desde donde estaba Foti) y sala
    tt = 49.3
    u = prog(t, 49.3, 49.75)
    if u < 1:
        capas = C.capas_de("espacio", capas_espacio)
        C.cam = (1.04, 0, 0)
        im_a = C.base("espacio", capas)
        C.fondo(im_a)
        viejo = C.fin()
    img_n = sala(C, t, 50.25, 49.55)
    out = C.fin()
    estatica(out, C, t, 50.25, 1.0)
    if t >= 50.25:
        pass
    # rótulos
    if u < 1:
        m, ring = mascara_cambio("iris", smooth(u), cx=540, cy=960, seed=5)
        m3 = m[..., None]
        out = (viejo.astype(np.float32) * (1 - m3) + out.astype(np.float32) * m3)
        out = (out * (1 - ring[..., None]) + np.array(COL_BORDE, np.float32) * ring[..., None]).astype(np.uint8)
    return rotulos_sala(C, out, t)


def rotulos_sala(C, out, t):
    """Rótulos de papel sobre el cuadro ya compuesto (se pegan en una hoja nueva y se mezclan)."""
    h = C.main
    h.limpiar()
    h.fondo = out.astype(np.float32) * (1 / 255.0)
    C.h = h
    C.rot("ESTÁTICA", 540, 330, 160, -0.03, (150, 210, 255), t_in=50.25, dur=0.3, tira=True, t_out=FIN("hoy") + 0.05, d_out=0.2)
    C.rot("LUZ DEL", 540, 1560 - 80, 100, 0.03, (255, 246, 214), t_in=51.83, dur=0.3, t_out=FIN("hoy") + 0.05, d_out=0.2)
    C.rot("BIG BANG", 540, 1560 + 50, 150, -0.03, (255, 150, 90), t_in=51.99, dur=0.3, tira=True, t_out=FIN("hoy") + 0.05, d_out=0.2)
    return C.fin()


# ------------------------------------------------------------------ 8. CIERRE
def burst(C, t, k):
    """El Big Bang del gancho (sol de rayos + núcleo) con Foti guiñando; k = progreso de aparición."""
    C.h = C.main
    C.main.limpiar()
    capas = C.capas_de("gancho", capas_gancho)
    C.cam = (1.0 + 0.04 * (t - 55.5) / 3.5, 0.0, 0.0)
    img = C.base("gancho", capas)
    bx, by = 540, 960
    P.rayos(img, bx, by, 60, 1700, 22, t * 0.16, [(255, 214, 96), (255, 150, 72)], 0.5, 0.55)
    P.rayos(img, bx, by, 60, 1100, 11, -t * 0.22 + 0.3, [(255, 244, 200)], 0.3, 0.4)
    P.halo(img, bx, by, 560 + 24 * math.sin(t * 5), (255, 236, 170), 0.9, 6)
    P.disco(img, bx, by, 220 + 10 * math.sin(t * 6), (255, 250, 226), 1.0)
    C.fondo(img)
    C.foti(540, 960, 2.6 + bump(t, 56.9, 0.4, 0.3), 0.0, "guino", "lengua", t_in=56.75, dur=0.4, largo=330, amp=24)
    C.rot("BIG BANG", 540, 420, 190, -0.04, (240, 84, 60), t_in=56.49, dur=0.3, s=1 + bump(t, 56.49, 0.4, 0.12))
    C.rot("¡SÍGUENOS!", 540, 1330, 120, 0.03, (255, 246, 214), t_in=57.9, dur=0.3, s=1 + bump(t, 58.3, 0.5, 0.06), tira=True)
    for j, (dx, dy, tt) in enumerate([(-330, -240, 57.2), (340, -220, 57.35), (-320, 250, 57.5), (330, 230, 57.65)]):
        C.pon(K.CHISPA, 540 + dx, 960 + dy + 8 * math.sin(t * 3 + j), 0.8, t * 0.5 + j, t_in=tt, modo="pop", dur=0.3)
    return C.fin()


@escena("cierre")
def cierre(C, t):
    t0 = INI("cierre")
    zi = 1.0 + 2.5 * e_inout(prog(t, 55.2, 56.5))
    sala(C, t, 50.25, 49.55, cam_zoom=zi)
    if t > 53.3:
        C.pon(K.espalda(), 540, 1600, 1.5 * (1 + 0.01 * math.sin(t * 2)), 0.0, t_in=53.3, modo="sube", dur=0.45, vida=0.5)
    out = C.fin()
    estatica(out, C, t, 50.25, 1.0)
    c = ruido_flash = pulso(t, 56.45, 0.4)
    if t >= 56.2:                                  # la estática se vuelve Big Bang desde el centro de la pantalla
        u = prog(t, 56.25, 56.75)
        ax, ay, bx, by = tele_pantalla(C)
        cx, cy = (ax + bx) / 2, (ay + by) / 2
        nuevo = burst(C, t, u)
        m, ring = mascara_cambio("iris", smooth(u), cx=cx, cy=cy, seed=7)
        if u < 1:
            m3 = m[..., None]
            out = nuevo.astype(np.float32) * m3 + out.astype(np.float32) * (1 - m3)
            out = (out * (1 - ring[..., None]) + np.array(COL_BORDE, np.float32) * ring[..., None]).astype(np.uint8)
        else:
            out = nuevo
    return flash(out, ruido_flash * 0.5)
