# -*- coding: utf-8 -*-
"""Planos 2: la idea de Musk, cómo funciona la torre, una captura paso a paso. Mundo LOCAL en metros (z arriba)."""
import math

import numpy as np

from comun import (H, W, L3, Cam, S, ap, bloque, cabecera, chorro, clamp, e_inout, e_out, etiqueta3d, F0, F1, foto, lerp, nrm,
                   pr, rejilla_suelo, smooth, T0, T1, vacio, vent, ww, ancho_texto)
from planos1 import (CAPT_X, O, TORRE, X, Y, Z, ZB_SH, cam_orb, con_foto, rp, sh_atrapado, torre)
import linea3d_starship as LS


def tarjeta(lz, x0, y0, x1, y1, op, titulo=None):
    lz.r2(x0, y0, x1, y1, 0.0)
    lz.l2([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], op * 0.8, 1.2, cerrada=True)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        lz.l2([(x + sx * 26, y), (x, y), (x, y + sy * 26)], op, 2.2)
    if titulo:
        lz.texto(titulo, x0 + 24, y0 + 36, 22, "SemiBold Condensed", op * 0.85, "lm", esp=0.18)


# ------------------------------------------------------------------ LA IDEA
def i_musk(t):
    t0 = T0("idea")
    k = pr(t, t0, F0("idea", 5))
    lz = L3(cam_orb(X * 20 + Z * 80, 330, 200 + 40 * k, 5, centro=(W * 0.82, H * 0.55)))
    torre(lz, 0.0, op=0.35)
    sh_atrapado(lz, op=0.35)
    o = ap(t, t0 + 0.3)
    x0, y0, x1, y1 = 860, 230, 1830, 800
    tarjeta(lz, x0, y0, x1, y1, o, "ELON MUSK  ·  30 DIC 2020  ·  EN ESPAÑOL")
    lin = [("«VAMOS A INTENTAR ATRAPAR EL PROPULSOR", F0("idea", 2)), ("CON EL BRAZO DE LA TORRE DE LANZAMIENTO.»", F0("idea", 2) + 1.0),
           ("«AHORRA EL PESO Y EL COSTO DE LAS PATAS,", F0("idea", 3) + 0.6), ("Y PERMITE PONER EL PROPULSOR EN LA MESA", F0("idea", 4)),
           ("AL INSTANTE: LISTO PARA VOLVER A VOLAR", F0("idea", 4) + 1.6), ("EN MENOS DE UNA HORA.»", F0("idea", 4) + 3.2)]
    for i, (txt, ta) in enumerate(lin):
        lz.texto(txt, x0 + 40, y0 + 120 + i * 62 + (30 if i >= 2 else 0), 38, "SemiBold Condensed", ap(t, ta), "lm", esp=0.04)
    oh = ap(t, ww("idea", 4, "hora") - 0.2)
    if oh > 0:
        y = y0 + 120 + 5 * 62 + 30 + 28
        lz.l2([(x0 + 40, y), (x0 + 40 + 370 * e_out(oh), y)], oh, 2.0)
    on = vent(t, F0("idea", 1), F0("idea", 2) + 0.4)
    bloque(lz, (x0 + x1) / 2, (y0 + y1) / 2, "NUNCA SE HABÍA HECHO", "UN COHETE ASÍ, ATRAPADO EN EL AIRE", on, 70, "mm")
    cabecera(lz, "EL PLAN DE LOS PALILLOS")
    return lz


def i_avion(t):
    t0 = F0("idea", 5) - 0.3
    lz = vacio()
    cx, cy, R = 960, 590, 250
    o = ap(t, t0)
    pasos = [("ATERRIZAR", ww("idea", 5, "aterrizar")), ("CARGAR COMBUSTIBLE", ww("idea", 5, "cargar")), ("DESPEGAR", ww("idea", 5, "despegar"))]
    th = np.linspace(0, 2 * math.pi, 200)
    lz.l2([(cx + R * math.cos(a), cy + R * math.sin(a)) for a in th], o * 0.35, 1.0)
    for i, (txt, ta) in enumerate(pasos):
        a = -math.pi / 2 + i * 2 * math.pi / 3
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        oi = max(0.3 * o, ap(t, ta - 0.15))
        lz.c2(x, y, 16, oi, w=1.8, lleno=oi > 0.5)
        lz.texto(txt, x + (30 if math.cos(a) >= -0.1 else -30), y - 40 if i == 0 else y + 40, 40, "Bold Condensed", oi,
                 "mm" if i == 0 else ("lm" if math.cos(a) > 0 else "rm"), esp=0.06)
    ang = -math.pi / 2 + 2 * math.pi * (t - t0) / 3.5
    lz.c2(cx + R * math.cos(ang), cy + R * math.sin(ang), 9, o, lleno=True)
    lz.texto("STARSHIP", cx, cy + 90, 30, "SemiBold Condensed", o * (1 - ap(t, ww("idea", 5, "avion") - 0.1)), "mm", esp=0.2)
    lz.texto("COMO UN AVIÓN", cx, cy, 64, "Bold Condensed", ap(t, ww("idea", 5, "avion") - 0.1), "mm", esp=0.05)
    lz.texto("EL VERDADERO OBJETIVO", cx, 150, 46, "SemiBold Condensed", o, "mm", esp=0.12)
    cabecera(lz, "EL PLAN DE LOS PALILLOS")
    return lz


def i_torre(t):
    t0 = F0("idea", 6) - 0.3
    k = pr(t, t0, T1("idea"))
    lz = L3(cam_orb(X * 20 + Z * 70, lerp(280, 230, e_inout(k)), lerp(150, 120, k), lerp(25, 8, k), centro=(W * 0.34, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 200, 10, op=0.16)
    torre(lz, 0.0, op=0.9)
    sh_atrapado(lz)
    bloque(lz, 1140, 380, "LA TORRE", "SE CONVIERTE EN", ap(t, t0 + 0.2), 90)
    bloque(lz, 1140, 560, "LAS PATAS", "DEL COHETE", ap(t, ww("idea", 6, "patas") - 0.2), 90)
    cabecera(lz, "EL PLAN DE LOS PALILLOS")
    return lz


# ------------------------------------------------------------------ LA TORRE
def t_alto(t):
    t0 = T0("torre")
    k = pr(t, t0, F0("torre", 1))
    lz = L3(cam_orb(Z * 72, lerp(205, 240, k), 210 + 15 * k, lerp(-4, 4, k), centro=(W * 0.42, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 150, 10, op=0.18)
    torre(lz, 0.7, z=110, op=0.95)
    o = ap(t, ww("torre", 0, "ciento") - 0.2)
    cam = lz.cam
    a, b = cam.px(-X * 14 + Z * 0.0), cam.px(-X * 14 + Z * 146)
    lz.l2([a, (a[0], a[1] - (a[1] - b[1]) * e_out(o))], o, 1.6)
    for p in (a, b):
        lz.l2([(p[0] - 14, p[1]), (p[0] + 14, p[1])], o, 1.6)
    lz.texto("146 M", a[0] - 30, (a[1] + b[1]) / 2, 64, "Bold Condensed", o, "rm", esp=0.05)
    lz.texto("STARBASE, TEXAS", 1250, 900, 30, "SemiBold Condensed", ap(t, t0 + 0.4), "lm", esp=0.16)
    cabecera(lz, "CÓMO FUNCIONA LA TORRE")
    return lz


def t_carro(t):
    t0 = F0("torre", 1) - 0.3
    k = pr(t, t0, F0("torre", 2))
    z = 70 + 40 * (0.5 - 0.5 * math.cos(2 * math.pi * (t - t0) / 5.0))
    lz = L3(cam_orb(Z * 78 + X * 8, 200, 235, 6, centro=(W * 0.38, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 150, 10, op=0.16)
    torre(lz, 0.6, z=z, op=0.85)
    cab = TORRE - X * 14 + Y * 0
    polea = TORRE - X * 3 + Z * 150
    carro = TORRE - X * 3 + Z * (z + 4)
    lz.linea(np.array([cab + Z * 3, polea]), 0.9, 1.4)
    lz.linea(np.array([polea, carro]), 0.9, 1.4)
    from comun import circulo3d
    lz.linea(circulo3d(cab + Z * 3, Y, 3.0), 1.0, 1.6, cerrada=True)
    lz.linea(circulo3d(polea, Y, 1.8), 1.0, 1.6, cerrada=True)
    o = ap(t, t0 + 0.3)
    etiqueta3d(lz, carro + X * 4, "CARRO CON LOS BRAZOS", "SUBE Y BAJA", dx=240, dy=-40, op=o, px=28)
    etiqueta3d(lz, cab + Z * 3, "CABRESTANTE", "EN LA BASE", dx=-200, dy=-60, op=ap(t, ww("torre", 1, "cabrestante") - 0.2), px=28)
    etiqueta3d(lz, polea, "POLEA", "EN LO ALTO", dx=-200, dy=40, op=ap(t, ww("torre", 1, "polea") - 0.2), px=28)
    cabecera(lz, "CÓMO FUNCIONA LA TORRE")
    return lz


def t_brazos(t):
    t0 = F0("torre", 2) - 0.3
    ab = 0.5 - 0.5 * math.cos(2 * math.pi * (t - t0) / 3.6)
    foco = X * 22 + Z * 100
    lz = L3(cam_orb(foco, 150, 200 + 20 * pr(t, t0, F0("torre", 3)), 34, centro=(W * 0.36, H * 0.55)))
    torre(lz, ab, z=100, op=0.95, w=1.2)
    o = ap(t, ww("torre", 2, "palillos") - 0.2)
    bloque(lz, 1240, 330, "PALILLOS", "SE ABREN Y SE CIERRAN", o, 96)
    lz.texto("SISTEMA HIDRÁULICO", 1244, 520, 30, "SemiBold Condensed", ap(t, ww("torre", 2, "hidraulico") - 0.2), "lm", esp=0.14)
    cabecera(lz, "CÓMO FUNCIONA LA TORRE")
    return lz


def t_asas(t):
    t0 = F0("torre", 5) - 0.3
    k = pr(t, t0, T1("torre"))
    foco = X * CAPT_X + Z * (ZB_SH - 6)
    lz = L3(cam_orb(foco, lerp(70, 95, k), lerp(230, 260, k), lerp(14, 6, k), centro=(W * 0.36, H * 0.5)))
    torre(lz, 0.0, op=0.85, w=1.1)
    b = sh_atrapado(lz)
    cam = lz.cam
    o = ap(t, ww("torre", 5, "aletas") - 0.2)
    for lado in (1, -1):
        p = b + Z * S.Z_PERNOS_SH + Y * lado * 5.5
        x, y = cam.px(p)
        lz.c2(x, y, 30 + 5 * math.sin(t * 4), o, w=1.6)
    bloque(lz, 1240, 300, "ALETAS = ASAS", "SE POSAN SOBRE LOS RIELES DE LOS BRAZOS", o, 72)
    o6 = ap(t, F0("torre", 6))
    if o6 > 0:
        x, y = cam.px(b + Z * 30)
        lz.l2([(x, y - 80), (x, y + 80)], o6, 2.4)
        lz.l2([(x - 16, y + 60), (x, y + 84), (x + 16, y + 60)], o6, 2.4)
        bloque(lz, 1240, 560, "TODO EL PESO", "CUELGA DE AHÍ, A DECENAS DE METROS DEL SUELO", o6, 64)
    cabecera(lz, "CÓMO FUNCIONA LA TORRE")
    return lz


# ------------------------------------------------------------------ CAPTURA PASO A PASO
PASOS = ["MEDIA VUELTA", "CAÍDA DE COLA", "¿TODO PERFECTO?", "FRENADO", "CAPTURA"]


def pasos_hud(lz, t):
    act = [F0("captura", 1), F0("captura", 2), F0("captura", 3), F0("captura", 5), F0("captura", 7)]
    o = ap(t, F0("captura", 0) + 0.5)
    for i, txt in enumerate(PASOS):
        y = 300 + i * 56
        on = t >= act[i] - 0.2
        cur = on and (i == 4 or t < act[i + 1] - 0.2)
        lz.c2(W - 330, y, 8, o * (1.0 if on else 0.35), w=1.4, lleno=on)
        lz.texto(f"{i + 1}  {txt}", W - 305, y, 28 if cur else 24, "Bold Condensed" if cur else "SemiBold Condensed",
                 o * (1.0 if cur else (0.7 if on else 0.35)), "lm", esp=0.08, fondo=True)


def c_titulo(t):
    t0 = T0("captura")
    lz = L3(cam_orb(X * 20 + Z * 75, 300, 210, 5, centro=(W * 0.3, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 200, 10, op=0.15)
    torre(lz, 0.8, op=0.6)
    lz.texto("UNA CAPTURA, PASO A PASO", 700, 160, 64, "Bold Condensed", ap(t, t0 + 0.2), "lm", esp=0.05)
    pasos_hud(lz, t)
    cabecera(lz, "LA CAPTURA")
    return lz


def c_caida(t):
    t0 = F0("captura", 2) - 0.3
    base = Z * (900 - 60 * (t - t0))
    a = nrm(Z + X * 0.06 * math.sin(t * 1.2))
    lz = L3(Cam(base + np.array([-30.0, -110, 10]), base + Z * 36, Z, 40, cerca=0.5, centro=(W * 0.38, H * 0.5)))
    S.super_heavy(lz, base, a, 1.0, 1.0, ref=Y)
    for i in range(40):                                    # aire que sube
        x, y = (i * 37) % 120 - 60, (i * 53) % 60 - 30
        z0 = (i * 71 + (t - t0) * 160) % 200 - 60
        lz.linea(np.array([base + np.array([x, y, z0]), base + np.array([x, y, z0 + 14])]), 0.35, 0.8)
    o = ap(t, t0 + 0.3)
    etiqueta3d(lz, base + Z * 66 + Y * 5, "ALETAS DE REJILLA", "LO GUÍAN EN LA CAÍDA", dx=230, dy=-40, op=o, px=28)
    pasos_hud(lz, t)
    cabecera(lz, "LA CAPTURA")
    return lz


def c_decide(t):
    t0 = F0("captura", 3) - 0.3
    k = pr(t, t0, F0("captura", 5))
    lz = L3(cam_orb(X * 30 + Z * 110, 330, lerp(200, 230, k), 8, centro=(W * 0.3, H * 0.52)))
    rejilla_suelo(lz, TORRE, X, Y, 200, 10, op=0.15)
    torre(lz, 0.85, op=0.9)
    S.super_heavy(lz, X * CAPT_X + Z * (200 - 40 * k), Z, 1.0, 1.0, op=0.8, ref=Y)
    etiqueta3d(lz, X * 40 + Z * 100, "BRAZOS ABIERTOS", "A LA ALTURA JUSTA", dx=220, dy=40, op=vent(t, t0 + 0.3, F0("captura", 4)), px=28)
    o = ap(t, F0("captura", 4) - 0.1)
    if o > 0:
        x0, y0 = 1080, 230
        tarjeta(lz, x0, y0, x0 + 480, y0 + 300, o, "COHETE Y TORRE")
        lz.texto("¿TODO PERFECTO?", x0 + 240, y0 + 95, 46, "Bold Condensed", o, "mm", esp=0.05)
        lz.texto("SÍ  >  A LA TORRE", x0 + 50, y0 + 175, 36, "SemiBold Condensed", o, "lm", esp=0.08)
        lz.texto("NO  >  AL MAR", x0 + 50, y0 + 235, 36, "SemiBold Condensed", ap(t, ww("captura", 4, "cancela") - 0.2), "lm", esp=0.08)
    pasos_hud(lz, t)
    cabecera(lz, "LA CAPTURA")
    return lz


def c_motores(t):
    t0 = F0("captura", 5) - 0.3
    t6 = F0("captura", 6)
    lz = vacio()
    cx, cy, s = 620, 560, 64.0
    o = ap(t, t0)
    lz.c2(cx, cy, 4.6 * s, o * 0.6, w=1.4)
    gir = ap(t, ww("captura", 5, "trece") - 0.1)
    for i, (kk, mx, my, rt) in enumerate(LS.motores_sh()):
        px, py = cx + mx * s, cy + my * s
        centro = kk <= 1
        if t < t6:
            lleno = centro and gir > 0.5
            op_i = o * (1.0 if (centro and gir > 0) else 0.55)
        else:
            lleno = kk == 0
            op_i = o * (1.0 if kk == 0 else 0.3)
        lz.c2(px, py, rt * s * 0.85, op_i, w=1.4, lleno=lleno)
        if centro and t < t6 and gir > 0:
            a = t * 2.0 + i
            lz.l2([(px, py), (px + 12 * math.cos(a), py + 12 * math.sin(a))], gir * 0.8, 1.0)
    lz.texto("SUPER HEAVY · VISTO DESDE ABAJO", cx, 150, 30, "SemiBold Condensed", o, "mm", esp=0.16)
    if t < t6:
        bloque(lz, 1100, 380, "13 DEL CENTRO", "GIRAN PARA DIRIGIRLO", gir, 80)
        bloque(lz, 1100, 600, "20 DE FUERA", "FIJOS", gir * 0.8, 56)
    else:
        o3 = ap(t, ww("captura", 6, "tres") - 0.2)
        bloque(lz, 1100, 420, "AL FINAL: 3", "LOS DEL CENTRO", o3, 96)
    pasos_hud(lz, t)
    cabecera(lz, "LA CAPTURA")
    return lz


def _extra_pasos(lz, t):
    pasos_hud(lz, t)


def _planos():
    p = []
    p.append((T0("idea"), con_foto(i_musk, dict(nombre="musk", cx=430, cy=500, ancho=470, asp=0.8, foco=(0.5, 0.4), t0=T0("idea") + 0.4,
                                               t1=F0("idea", 5) - 0.4, rotulo="ELON MUSK", sub="DUEÑO DE SPACEX · FOTO: U.S. AIR FORCE (DOM. PÚBLICO)", estilo=1))))
    p.append((F0("idea", 5) - 0.3, i_avion))
    p.append((F0("idea", 6) - 0.3, i_torre))
    p.append((T0("torre"), t_alto))
    p.append((F0("torre", 1) - 0.3, t_carro))
    p.append((F0("torre", 2) - 0.3, t_brazos))
    a = F0("torre", 3) - 0.3
    p.append((a, con_foto(rp("f7", 127.0, a, rot="MECHAZILLA", sub="VUELO 7 · 16 ENE 2025", vel=0.8, tfin=141.0),
                          dict(nombre="mechazilla", cx=1480, cy=420, ancho=420, asp=0.85, foco=(0.5, 0.45), t0=a + 0.8, t1=F0("torre", 5) - 0.4,
                               rotulo="ASÍ LE DICEN A LA TORRE", sub="FOTO: STEVE JURVETSON · CC BY", estilo=3))))
    p.append((F0("torre", 5) - 0.3, t_asas))
    p.append((T0("captura"), c_titulo))
    a = F0("captura", 1) - 0.3
    p.append((a, rp("f5", 99.0, a, rot="MEDIA VUELTA", sub="Y ENCIENDE MOTORES PARA REGRESAR · VUELO 5", vel=1.2, tfin=113.0, extra=_extra_pasos)))
    p.append((F0("captura", 2) - 0.3, c_caida))
    p.append((F0("captura", 3) - 0.3, c_decide))
    p.append((F0("captura", 5) - 0.3, c_motores))
    a = F0("captura", 7) - 0.3
    p.append((a, rp("f7", 126.0, a, rot="LOS PALILLOS SE CIERRAN", sub="VUELO 7 · 16 ENE 2025", vel=1.7, tfin=139.0, extra=_extra_pasos)))
    return p


PLANOS = _planos()


def sfx():
    v = [(T0("idea") + 0.3, "whoosh", 0.4, 0.0, None), (F0("idea", 1), "sello", 0.5, 0.0, None), (F0("idea", 2), "tic", 0.4, 0.3, None),
         (F0("idea", 3) + 0.6, "tic", 0.4, 0.3, None), (F0("idea", 4), "tic", 0.4, 0.3, None), (ww("idea", 4, "hora") - 0.2, "hud", 0.5, 0.3, None),
         (ww("idea", 5, "aterrizar"), "tic", 0.45, -0.2, None), (ww("idea", 5, "cargar"), "tic", 0.45, 0.2, None),
         (ww("idea", 5, "despegar"), "tic", 0.45, 0.0, None), (F0("idea", 6) - 0.3, "whoosh", 0.4, 0.0, None),
         (ww("idea", 6, "patas") - 0.2, "pulso", 0.6, 0.0, None)]
    v += [(ww("torre", 0, "ciento") - 0.2, "hud", 0.45, -0.3, None), (F0("torre", 1) - 0.1, "cabrestante", 0.6, 0.0, 4.5),
          (F0("torre", 2) - 0.2, "brazos", 0.6, 0.0, None), (F0("torre", 2) + 3.4, "brazos", 0.5, 0.0, None),
          (F0("torre", 3) + 0.5, "tic", 0.4, 0.3, None), (ww("torre", 5, "aletas") - 0.2, "hud", 0.45, 0.3, None),
          (F0("torre", 6), "pesa", 0.5, 0.0, None)]
    v += [(T0("captura") + 0.3, "pulso", 0.5, 0.0, None), (F0("captura", 1), "encendido", 0.6, 0.0, None),
          (F0("captura", 2) - 0.2, "caida", 0.6, 0.0, 4.0), (F0("captura", 4) - 0.1, "hud", 0.45, 0.3, None),
          (ww("captura", 4, "cancela") - 0.2, "alarma", 0.45, 0.3, None), (ww("captura", 5, "trece"), "tic", 0.45, 0.3, None),
          (ww("captura", 6, "tres") - 0.2, "tic", 0.45, 0.3, None), (F0("captura", 7) + 2.4, "brazos", 0.7, 0.0, None),
          (F0("captura", 7) + 3.6, "toque", 0.6, 0.0, None)]
    return v
