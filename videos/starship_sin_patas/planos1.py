# -*- coding: utf-8 -*-
"""Planos 1: gancho, Falcon 9 y sus patas, el precio de las patas, los prototipos con patas. Mundo LOCAL en metros (z arriba)."""
import math

import numpy as np

import linea3d_cohetes as F
from comun import (H, W, L3, Cam, S, ap, bloque, cabecera, chorro, clamp, e_inout, e_out, etiqueta3d, F0, F1, foto, lerp, nrm,
                   pr, real, rejilla_suelo, smooth, T0, T1, vacio, vent, ww, ancho_texto, a_img, _Img)

X, Y, Z = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
O = np.zeros(3)
TORRE = np.array([0.0, 0, 0])             # pie de la torre; los brazos apuntan a +X
CAPT_X = 35.5                             # eje del cohete atrapado (m desde el centro de la torre)
ZB_SH = 100.0                             # altura del carro al atrapar el propulsor


def torre(lz, apertura=0.0, z=ZB_SH, op=0.8, w=1.0, base=TORRE):
    return S.torre_captura(lz, base, Z, X, 1.0, alto=146.0, z_brazos=z, apertura=apertura, op=op, w=w)


def sh_atrapado(lz, op=1.0, dz=0.0, base=TORRE, z=ZB_SH):
    b = base + X * CAPT_X + Z * (z - S.Z_PERNOS_SH + dz)
    S.super_heavy(lz, b, Z, 1.0, 1.0, op=op, ref=Y)
    return b


def cam_orb(foco, dist, az, el, fov=40, centro=None):
    a, e = math.radians(az), math.radians(el)
    d = math.cos(e) * (math.sin(a) * X - math.cos(a) * Y) + math.sin(e) * Z
    return Cam(foco + d * dist, foco, Z, fov, cerca=0.5, centro=centro)


def rp(clip, s0, ta, rot=None, sub=None, top=None, vel=1.0, zoom=1.2, cy=0.42, extra=None, tfin=None):
    """Plano de video real: segundo s0 del clip al empezar el plano (ta)."""
    def f(t):
        lz = vacio()
        seg = s0 + (t - ta) * vel
        if tfin is not None:
            seg = min(seg, tfin)
        if extra:
            extra(lz, t)
        return real(t, clip, seg, lz, zoom=zoom, cy=cy, rotulo=rot, sub=sub, tmision=top)
    f.ta = ta
    return f


def con_foto(plano, *fotos):
    """Envuelve un plano y le pega fotos: cada foto = dict de argumentos de `foto`."""
    def f(t):
        img = a_img(plano(t), t)
        for k in fotos:
            img = foto(img, t, **k)
        return _Img(img)
    return f


# ------------------------------------------------------------------ GANCHO
def g_vs(t):
    t0 = F0("gancho", 4) - 0.2
    k = pr(t, t0, F0("gancho", 5))
    cam = Cam(np.array([40 + 20 * k, -270.0, 60]), np.array([40.0, 0, 62]), Z, 40, cerca=0.5, centro=(W * 0.5, H * 0.55))
    lz = L3(cam)
    rejilla_suelo(lz, np.array([60.0, 0, 0]), X, Y, 260, 12, op=0.16)
    F.etapa1(lz, np.array([-80.0, 0, 0]), Z, 1.0, aletas=1.0, patas=1.0, op=0.95, ref=Y)
    torre(lz, 0.0)
    sh_atrapado(lz)
    o = ap(t, t0 + 0.1)
    etiqueta3d(lz, np.array([-80.0, 0, 30]), "FALCON 9", "CON PATAS", dx=-120, dy=-200, op=o, px=30)
    etiqueta3d(lz, X * CAPT_X + Z * 60, "STARSHIP · SUPER HEAVY", "SIN PATAS", dx=150, dy=-170, op=o, px=30)
    lz.texto("¿POR QUÉ STARSHIP NO?", W / 2, 150, 72, "Bold Condensed", ap(t, t0 + 0.3), "mm", esp=0.05)
    return lz


def g_titulo(t):
    t0 = F0("gancho", 5) - 0.3
    k = pr(t, t0, T1("gancho"))
    foco = X * 20 + Z * 78
    lz = L3(cam_orb(foco, lerp(250, 215, e_inout(k)), lerp(205, 240, k), 6, centro=(W * 0.32, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 200, 10, op=0.16)
    torre(lz, 0.0)
    sh_atrapado(lz)
    for i, (txt, pal) in enumerate((("PESO", "peso"), ("TIEMPO", "tiempo"), ("UN PLAN MÁS AMBICIOSO", "plan"))):
        oi = vent(t, ww("gancho", 5, pal) - 0.1, F0("gancho", 6))
        lz.texto(txt, 1120, 360 + i * 80, 56, "Bold Condensed", oi, "lm", esp=0.06)
    o = ap(t, F0("gancho", 6) - 0.1)
    if o > 0:
        lz.texto("LA VERDADERA RAZÓN", 1120, 410, 70, "Bold Condensed", o, "lm", esp=0.05)
        lz.texto("DE LOS PALILLOS", 1120, 490, 96, "Bold Condensed", ap(t, F0("gancho", 6) + 0.4), "lm", esp=0.04)
    cabecera(lz, "STARSHIP SIN PATAS")
    return lz


# ------------------------------------------------------------------ FALCON 9
def f_patas(t):
    t0 = T0("falcon")
    k = pr(t, t0, F0("falcon", 3))
    pat = smooth(pr(t, F0("falcon", 2) - 0.2, F0("falcon", 2) + 1.6))
    foco = Z * 22
    lz = L3(cam_orb(foco, lerp(95, 80, k), 200 + 80 * k, lerp(14, 4, k), centro=(W * 0.36, H * 0.5)))
    rejilla_suelo(lz, O, X, Y, 60, 4, op=0.18)
    F.etapa1(lz, Z * 0.6 * pat, Z, 1.0, aletas=1.0, patas=pat, op=1.0, ref=Y)
    o1 = vent(t, F0("falcon", 1), F0("falcon", 2) - 0.1)
    etiqueta3d(lz, Z * 8 + X * 2, "4 PATAS PLEGADAS", "CONTRA EL CUERPO AL DESPEGAR", dx=260, dy=-60, op=o1, px=30)
    o2 = ap(t, F0("falcon", 2))
    if o2 > 0:                                        # regla de punta a punta (~18 m)
        cam = lz.cam
        a, b = cam.px(-X * 9 + Z * 0.3), cam.px(X * 9 + Z * 0.3)
        lz.l2([a, b], o2 * pat, 1.4)
        for p in (a, b):
            lz.l2([(p[0], p[1] - 12), (p[0], p[1] + 12)], o2 * pat, 1.4)
        lz.texto("UNOS 18 M", (a[0] + b[0]) / 2, max(a[1], b[1]) + 34, 34, "Bold Condensed", o2 * pat, "mm", esp=0.08)
    bloque(lz, 1240, 200, "FIBRA DE CARBONO", "Y ALUMINIO", ap(t, ww("falcon", 2, "fibra")), 54)
    lz.texto("FALCON 9 · PRIMERA ETAPA", 70, 1010, 26, "SemiBold Condensed", ap(t, t0), "lm", esp=0.16)
    return lz


def f_hover(t):
    t0 = F0("falcon", 4) - 0.3
    t5 = F0("falcon", 5)
    lz = L3(Cam(np.array([0.0, -150, 30]), np.array([0, 0, 28.0]), Z, 40, cerca=0.5, centro=(W * 0.3, H * 0.55)))
    rejilla_suelo(lz, O, X, Y, 70, 5, op=0.18)
    F.zona_aterrizaje(lz, O, Z, 1.0, op=0.7, r=18)
    # altura: baja rápido y frena justo al tocar
    q = clamp(pr(t, t5 - 0.3, t5 + 3.6))
    h = 40 * (1 - q) ** 2 if t >= t5 - 0.3 else 40.0 + 2 * math.sin(t * 1.5)
    pat = smooth(pr(t, t5 + 1.6, t5 + 2.6))
    F.etapa1(lz, Z * h, Z, 1.0, aletas=1.0, patas=pat, ref=Y)
    if q < 0.999:
        for i, p in enumerate(F.salidas_motores(Z * h, Z, 1.0, Y, cuales=[0])):
            chorro(lz, p, -Z, 16 + 6 * (t5 > t), 1.6, t, n=40, op=0.9, semilla=i)
    cam = lz.cam
    o = ap(t, ww("falcon", 4, "no"))
    if o > 0 and t < t5:
        x, y = cam.px(Z * (h + 24) + X * 4)
        lz.l2([(x + 60, y + 120), (x + 60, y - 40)], o, 2.2)
        lz.l2([(x + 48, y - 26), (x + 60, y - 44), (x + 72, y - 26)], o, 2.2)
        lz.l2([(x - 60, y - 40), (x - 60, y + 80)], o, 2.2)
        lz.l2([(x - 72, y + 66), (x - 60, y + 84), (x - 48, y + 66)], o, 2.2)
    bloque(lz, 1150, 300, "NO PUEDE FLOTAR", None, o * (1 - ap(t, t5)), 64)
    o2 = ap(t, ww("falcon", 4, "minimo"))
    lz.texto("EMPUJE: 1 MOTOR AL MÍNIMO", 1150, 400, 34, "SemiBold Condensed", o2 * (1 - ap(t, t5)), "lm", esp=0.1)
    lz.texto(">  PESO DE LA ETAPA CASI VACÍA", 1150, 450, 34, "SemiBold Condensed", ap(t, ww("falcon", 4, "pesa")) * (1 - ap(t, t5)), "lm", esp=0.1)
    o5 = ap(t, t5)
    if o5 > 0:                                        # velocidad que llega a cero justo en el suelo
        bloque(lz, 1150, 300, "FRENADO JUSTO", "VELOCIDAD 0 AL TOCAR EL SUELO", o5, 64)
        v = 1 - q
        lz.l2([(1150, 520), (1150 + 520, 520)], o5 * 0.4, 1.0)
        lz.l2([(1150, 520), (1150 + 520 * v, 520)], o5, 6.0)
        lz.texto(f"VELOCIDAD  {int(round(v * 100)):3d} %", 1150, 560, 26, "SemiBold Condensed", o5, "lm", esp=0.12)
    cabecera(lz, "EL FALCON 9 Y SUS PATAS")
    return lz


def f_37(t):
    t0 = F0("falcon", 8) - 0.3
    k = pr(t, t0, T1("falcon"))
    lz = L3(cam_orb(Z * 22, 95, 215 + 30 * k, 6, centro=(W * 0.3, H * 0.5)))
    rejilla_suelo(lz, O, X, Y, 60, 4, op=0.16)
    F.etapa1(lz, O + Z * 0.6, Z, 1.0, aletas=1.0, patas=1.0, ref=Y)
    n = int(37 * e_out(pr(t, F0("falcon", 8), F1("falcon", 8))))
    for i in range(37):
        x, y = 1080 + (i % 10) * 64, 380 + (i // 10) * 70
        on = i < n
        lz.l2([(x, y - 22), (x + 8, y - 30), (x + 16, y - 22), (x + 16, y + 22), (x, y + 22)], (1.0 if on else 0.25) * ap(t, t0), 1.4, cerrada=True)
    lz.texto(f"{n}", 1080, 260, 110, "Bold Condensed", ap(t, t0 + 0.2), "lm", esp=0.04)
    lz.texto("VUELOS DE UN MISMO PROPULSOR", 1210, 270, 30, "SemiBold Condensed", ap(t, t0 + 0.2), "lm", esp=0.12)
    lz.texto("B1067 · RÉCORD (AGO 2026)", 1084, 680, 26, "SemiBold Condensed", ap(t, t0 + 0.6), "lm", esp=0.14)
    cabecera(lz, "EL FALCON 9 Y SUS PATAS")
    return lz


# ------------------------------------------------------------------ EL PRECIO
def p_peso(t):
    t0 = T0("precio")
    lz = L3(cam_orb(Z * 22, 90, 160 + 20 * pr(t, t0, F0("precio", 3)), 6, centro=(W * 0.24, H * 0.5)))
    rejilla_suelo(lz, O, X, Y, 60, 4, op=0.14)
    F.etapa1(lz, Z * 0.6, Z, 1.0, aletas=1.0, patas=1.0, op=0.75, ref=Y)
    lz.texto("EL PRECIO DE LAS PATAS", 820, 170, 60, "Bold Condensed", ap(t, t0 + 0.2), "lm", esp=0.05)
    o1 = ap(t, F0("precio", 1))
    if o1 > 0:
        x0, L = 820, 900
        lz.l2([(x0, 330), (x0 + L * e_out(o1), 330)], o1, 30.0)
        lz.texto("ETAPA VACÍA  ·  22,2 T", x0, 290, 30, "SemiBold Condensed", o1, "lm", esp=0.1)
        o2 = ap(t, ww("precio", 1, "dos") - 0.2)
        lp = L * 2.1 / 22.2
        lz.l2([(x0, 420), (x0 + lp * e_out(o2), 420)], o2, 30.0)
        lz.texto("4 PATAS  ·  CASI 2 T", x0, 380, 30, "SemiBold Condensed", o2, "lm", esp=0.1)
        lz.texto("1/10", x0 + lp + 40, 420, 54, "Bold Condensed", ap(t, ww("precio", 1, "decima") - 0.1), "lm", esp=0.05)
    o3 = ap(t, F0("precio", 2))
    if o3 > 0:
        lz.texto("+1 KG EN EL COHETE", 820, 560, 48, "Bold Condensed", o3, "lm", esp=0.06)
        lz.texto("=  MÁS COMBUSTIBLE", 840, 630, 34, "SemiBold Condensed", ap(t, ww("precio", 2, "combustible") - 0.2), "lm", esp=0.12)
        lz.texto("O MENOS CARGA AL ESPACIO", 840, 680, 34, "SemiBold Condensed", ap(t, ww("precio", 2, "carga") - 0.2), "lm", esp=0.12)
    cabecera(lz, "EL PRECIO DE LAS PATAS")
    return lz


# ------------------------------------------------------------------ PROTOTIPOS
def r_tamanos(t):
    t0 = F0("prototipos", 4) - 0.3
    k = pr(t, t0, T1("prototipos"))
    cam = Cam(np.array([10 + 10 * k, -260.0, 50]), np.array([10.0, 0, 42]), Z, 40, cerca=0.5, centro=(W * 0.42, H * 0.56))
    lz = L3(cam)
    rejilla_suelo(lz, np.array([10.0, 0, 0]), X, Y, 200, 10, op=0.15)
    F.etapa1(lz, np.array([-55.0, 0, 0]), Z, 1.0, aletas=1.0, patas=1.0, op=0.7, ref=Y)
    S.nave(lz, np.array([-15.0, 0, 0]), Z, 1.0, op=0.7, ref=Y, flaps=0.0)
    S.super_heavy(lz, np.array([40.0, 0, 0]), Z, 1.0, 1.0, op=ap(t, F0("prototipos", 4) + 0.6), ref=Y)
    o = ap(t, t0 + 0.2)
    etiqueta3d(lz, np.array([-55.0, 0, 47]), "FALCON 9", "PRIMERA ETAPA", dx=-60, dy=-120, op=o * 0.9, px=24)
    etiqueta3d(lz, np.array([-15.0, 0, 50]), "PROTOTIPO", "TIPO SN15", dx=-30, dy=-150, op=o * 0.9, px=24)
    ob = ap(t, ww("prototipos", 4, "super") - 0.2)
    if ob > 0:
        a, b = cam.px(np.array([52.0, 0, 0])), cam.px(np.array([52.0, 0, 72.3]))
        lz.l2([a, b], ob, 1.4)
        for p in (a, b):
            lz.l2([(p[0] - 12, p[1]), (p[0] + 12, p[1])], ob, 1.4)
        lz.texto("MÁS DE 70 M", b[0] + 24, (a[1] + b[1]) / 2, 40, "Bold Condensed", ob, "lm", esp=0.06)
        lz.texto("33 MOTORES", b[0] + 24, (a[1] + b[1]) / 2 + 46, 28, "SemiBold Condensed", ap(t, ww("prototipos", 4, "treinta")), "lm", esp=0.12)
    o5 = ap(t, F0("prototipos", 5))
    bloque(lz, W / 2, 150, "PATAS ENORMES", "Y CADA TONELADA CUENTA", o5, 64, "mm")
    cabecera(lz, "STARSHIP TAMBIÉN TUVO PATAS")
    return lz


# ------------------------------------------------------------------ lista de planos
def _planos():
    p = []
    p.append((0.0, rp("f5", 125.0, 0.0)))
    a = F0("gancho", 1) - 0.3
    p.append((a, rp("f5", 131.0, a, rot=None)))
    a = F0("gancho", 2) - 0.2
    p.append((a, rp("f5", 143.0, a, rot="ATRAPADO EN EL AIRE", sub="VUELO 5 · 13 OCT 2024 · STARBASE, TEXAS")))
    a = F0("gancho", 3) - 0.3
    p.append((a, rp("f9landed", 162.5, a, rot="FALCON 9", sub="SÍ TIENE PATAS", vel=0.9)))
    p.append((F0("gancho", 4) - 0.2, g_vs))
    p.append((F0("gancho", 5) - 0.3, g_titulo))
    # Falcon 9
    p.append((T0("falcon"), con_foto(f_patas, dict(nombre="pata", cx=1480, cy=560, ancho=520, asp=2.0, foco=(0.55, 0.84), t0=ww("falcon", 2, "fibra") + 0.6,
                                                   t1=F0("falcon", 3) - 0.3, rotulo="PATA REAL DEL FALCON 9", sub="FOTO: STEVE JURVETSON · CC BY", estilo=0))))
    a = F0("falcon", 3) - 0.3
    p.append((a, rp("f9landed", 158.0, a, rot="SE ABREN AL FINAL", sub="LOS ÚLTIMOS SEGUNDOS DE LA CAÍDA", vel=0.9)))
    p.append((F0("falcon", 4) - 0.3, f_hover))
    a = F0("falcon", 6) - 0.3
    p.append((a, con_foto(rp("nolanding", 112.0, a, rot="PRIMER ATERRIZAJE", sub="21 DIC 2015 · CABO CAÑAVERAL", tfin=119.5),
                          dict(nombre="orbcomm", cx=1460, cy=420, ancho=520, asp=1.5, t0=a + 1.2, t1=F0("falcon", 7) - 0.2,
                               rotulo="ORBCOMM-2 · LZ-1", sub="FOTO: SPACEX · CC0", estilo=3))))
    a = F0("falcon", 7) - 0.3
    p.append((a, rp("crs8", 6.0, a, rot="PRIMERA BARCAZA", sub="8 ABR 2016 · EN MEDIO DEL OCÉANO")))
    p.append((F0("falcon", 8) - 0.3, f_37))
    # el precio
    p.append((T0("precio"), p_peso))
    a = F0("precio", 3) - 0.3
    p.append((a, rp("nolanding", 61.5, a, rot="LA PATA NO SE TRABÓ", sub="17 ENE 2016 · MISIÓN JASON-3", vel=0.85, tfin=74.0)))
    a = F0("precio", 5) - 0.3
    p.append((a, rp("f9landed", 194.0, a, rot="LEJOS DE SU PLATAFORMA", sub="A LEVANTARLO CON GRÚAS", vel=0.8, tfin=201.0)))
    a = F0("precio", 6) - 0.3
    p.append((a, con_foto(rp("crs8", 24.0, a, rot="DÍAS DE VUELTA A PUERTO", sub="GRÚAS · TRANSPORTE · REVISIÓN", vel=0.8, tfin=38.5),
                          dict(nombre="crs8", cx=1470, cy=400, ancho=480, asp=1.5, t0=ww("precio", 6, "gruas") - 0.3, t1=T1("precio") - 0.2,
                               rotulo="CRS-8 · DE PIE EN LA BARCAZA", sub="FOTO: SPACEX · CC0", estilo=2))))
    # prototipos
    a = T0("prototipos")
    p.append((a, rp("sn15", 0.0, a, rot="PROTOTIPOS DE STARSHIP", sub="ATERRIZABAN SOBRE PATAS CORTAS", vel=0.9, zoom=1.1)))
    a = F0("prototipos", 2) - 0.3
    p.append((a, rp("sn10", 86.0, a, rot="SN10", sub="3 MAR 2021 · ATERRIZAJE DURO", vel=1.0, tfin=103.0)))
    a = ww("prototipos", 2, "minutos") - 0.4
    p.append((a, rp("sn10b", 33.0, a, rot="MINUTOS DESPUÉS", sub="SN10 EXPLOTA EN LA PLATAFORMA", vel=1.0, zoom=1.25, cy=0.45)))
    a = F0("prototipos", 3) - 0.3
    p.append((a, rp("sn15", 46.0, a, rot="SN15 ATERRIZA ENTERO", sub="5 MAY 2021", vel=1.0, zoom=1.1, tfin=64.0)))
    p.append((F0("prototipos", 4) - 0.3, r_tamanos))
    return p


PLANOS = _planos()


def sfx():
    v = [(0.3, "pulso", 0.5, 0.0, None), (F0("gancho", 2) - 0.2, "brazos", 0.6, 0.0, None), (F0("gancho", 4) - 0.2, "whoosh", 0.5, 0.0, None),
         (F0("gancho", 6) - 0.1, "pulso", 0.8, 0.0, None)]
    v += [(T0("falcon") + 0.2, "whoosh", 0.4, 0.0, None), (F0("falcon", 2) - 0.1, "patas", 0.7, 0.0, None),
          (ww("falcon", 2, "fibra") + 0.6, "tic", 0.4, 0.3, None), (F0("falcon", 5) + 3.0, "aterriza", 0.6, 0.0, None),
          (F0("falcon", 6) + 0.9, "tic", 0.4, 0.3, None), (F0("falcon", 8), "hud", 0.4, 0.3, None)]
    v += [(F0("precio", 1), "pesa", 0.5, 0.2, None), (ww("precio", 1, "dos"), "pesa", 0.4, 0.2, None), (F0("precio", 2), "tic", 0.4, 0.3, None),
          (ww("precio", 6, "gruas") - 0.3, "tic", 0.4, 0.3, None)]
    v += [(ww("prototipos", 2, "minutos") - 0.2, "explosion", 0.6, 0.0, None), (F0("prototipos", 4) - 0.2, "whoosh", 0.4, 0.0, None),
          (ww("prototipos", 4, "super"), "hud", 0.4, 0.3, None)]
    return v
