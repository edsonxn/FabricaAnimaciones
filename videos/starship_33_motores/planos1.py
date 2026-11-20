# -*- coding: utf-8 -*-
"""Planos 1: gancho, el Raptor, los tres anillos, el Saturno V. Mundo LOCAL en metros (z arriba)."""
import math

import numpy as np

from comun import (H, W, L3, Cam, S, IDX, ap, bloque, cabecera, chorro, clamp, contador, e_inout, e_out, etiqueta3d, F0, F1,
                   foto, lerp, panel33, pr, real, rejilla_suelo, smooth, T0, T1, vacio, vent, ww, a_img, _Img)

X, Y, Z = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
O = np.zeros(3)

# segundos de clip (ajustados con las hojas de contacto `previews/c_*.jpg`)
SEG = dict(mesa=6.0, mesa_desp=66.0, n1_expl=80.0, b7_lenta=110.0, r3b=50.0, r3=203.0, r3_b=0.0, a11_f1=108.0, s1c_f1=294.0,
           s1c=189.0, s1c_b=217.0)


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
    def f(t):
        img = a_img(plano(t), t)
        for k in fotos:
            img = foto(img, t, **k)
        return _Img(img)
    return f


def barras(lz, t, x, y, items, t0, maxv, ancho=820, alto=46, sep=96):
    """Barras horizontales que crecen: items = [(rótulo, valor, texto_valor, t_aparece)]."""
    for i, (rot, v, tv, ta) in enumerate(items):
        k = e_out(pr(t, ta, ta + 0.9))
        o = ap(t, ta, 0.25)
        if o <= 0.01:
            continue
        yy = y + i * sep
        w = ancho * v / maxv * k
        lz.texto(rot, x, yy - alto * 0.5 - 18, 24, "SemiBold Condensed", o, "lm", esp=0.16)
        lz.l2([(x, yy - alto / 2), (x + w, yy - alto / 2), (x + w, yy + alto / 2), (x, yy + alto / 2)], o, 1.6, cerrada=True)
        for j in range(int(w // 14)):
            xx = x + 7 + j * 14
            lz.l2([(xx, yy + alto / 2 - 4), (xx + 10, yy - alto / 2 + 4)], o * 0.45, 1.0)
        lz.texto(tv, x + w + 22, yy, 40, "Bold Condensed", o * k, "lm", esp=0.04)


# ------------------------------------------------------------------ GANCHO
def g_vs(t):
    """33 contra 5: la base del Super Heavy junto a la del Saturno V (vista desde abajo, a la misma escala)."""
    t0 = F0("gancho", 2) - 0.3
    lz = vacio()
    k = e_out(pr(t, t0, t0 + 1.2))
    panel33(lz, 620, 520, 52 * k + 1e-3, op=ap(t, t0), titulo="STARSHIP · SUPER HEAVY", sub="33 MOTORES RAPTOR")
    # Saturno V: 5 F-1 en cruz (4 + 1 central), etapa de 10,1 m de diámetro
    cx, cy, e = 1300, 520, 52 * k + 1e-3
    o = ap(t, ww("gancho", 2, "cinco") - 0.2)
    if o > 0:
        lz.c2(cx, cy, 5.05 * e, o * 0.55, w=1.2)
        for (dx, dy) in ((0, 0), (2.4, 2.4), (-2.4, 2.4), (2.4, -2.4), (-2.4, -2.4)):
            lz.c2(cx + dx * e, cy + dy * e, 1.85 * e, o, w=1.4, lleno=True)
        lz.texto("SATURNO V", cx, cy + 5.6 * e, 30, "Bold Condensed", o, "mm", esp=0.08)
        lz.texto("5 MOTORES F-1", cx, cy + 5.6 * e + 32, 19, "SemiBold Condensed", o * 0.85, "mm", esp=0.16)
    lz.texto("VISTA DESDE ABAJO · MISMA ESCALA", W / 2, 1010, 20, "SemiBold Condensed", ap(t, t0 + 0.6) * 0.8, "mm", esp=0.2)
    return lz


def g_n1(t):
    o = ap(t, ww("gancho", 3, "cuatro") - 0.1)
    def ex(lz, tt):
        lz.texto("4 DE 4", W - 90, 560, 120, "Bold Condensed", o, "rm", esp=0.03)
        lz.texto("LANZAMIENTOS FALLIDOS", W - 92, 640, 26, "SemiBold Condensed", o * 0.9, "rm", esp=0.16)
    return rp("n1", SEG["n1_expl"], F0("gancho", 3) - 0.3, "N1 · URSS", "30 MOTORES · 1969-1972", extra=ex)(t)


def g_titulo(t):
    t0 = F0("gancho", 5) - 0.3
    k = pr(t, t0, T1("gancho"))
    base = O
    lz = L3(Cam(np.array([lerp(30, 24, k), -lerp(34, 26, k), -lerp(10, 16, k)]), np.array([0, 0, 22.0]), Z, 42, cerca=0.3,
                centro=(W * 0.3, H * 0.5)))
    S.super_heavy(lz, base, Z, 1.0, 1.0, op=1.0, ref=Y, rot=0.4 * k)
    for i, (txt, pal) in enumerate((("FALLAR", "fallar"), ("FABRICAR", "fabricar"), ("VOLVER A CASA", "volver"))):
        oi = vent(t, ww("gancho", 5, pal) - 0.1, F0("gancho", 6))
        lz.texto(txt, 1120, 380 + i * 84, 64, "Bold Condensed", oi, "lm", esp=0.06)
    o = ap(t, F0("gancho", 6) - 0.1)
    if o > 0:
        lz.texto("LA VERDADERA RAZÓN", 1120, 420, 70, "Bold Condensed", o, "lm", esp=0.05)
        lz.texto("DE LOS 33 MOTORES", 1120, 500, 96, "Bold Condensed", ap(t, F0("gancho", 6) + 0.4), "lm", esp=0.04)
    cabecera(lz, "STARSHIP · 33 MOTORES")
    return lz


# ------------------------------------------------------------------ RAPTOR
def r_ciclo(t):
    """Esquema del ciclo de flujo completo: cada propelente pasa ENTERO por su propia turbina antes de la cámara."""
    t0 = F0("raptor", 2) - 0.3
    lz = vacio()
    o = ap(t, t0)
    cabecera(lz, "RAPTOR · COMBUSTIÓN POR ETAPAS DE FLUJO COMPLETO", o)
    # tanques
    for (x, nom, sub) in ((520, "METANO", "LÍQUIDO"), (1400, "OXÍGENO", "LÍQUIDO")):
        lz.l2([(x - 120, 200), (x + 120, 200), (x + 120, 330), (x - 120, 330)], o, 1.6, cerrada=True)
        lz.texto(nom, x, 250, 40, "Bold Condensed", o, "mm", esp=0.06)
        lz.texto(sub, x, 292, 20, "SemiBold Condensed", o * 0.85, "mm", esp=0.2)
    # turbinas (prequemadores) y cámara
    k1 = ap(t, ww("raptor", 2, "turbinas") - 0.2)
    for (x, nom) in ((640, "TURBINA 1"), (1280, "TURBINA 2")):
        lz.c2(x, 520, 62, o * k1, w=1.6)
        for a in range(6):
            ang = t * 4.0 + a * math.pi / 3
            lz.l2([(x, 520), (x + 56 * math.cos(ang), 520 + 56 * math.sin(ang))], o * k1 * 0.7, 1.2)
        lz.texto(nom, x, 610, 22, "SemiBold Condensed", o * k1, "mm", esp=0.16)
    kc = ap(t, ww("raptor", 2, "cámara") - 0.2)
    cx = 960
    lz.l2([(cx - 90, 690), (cx + 90, 690), (cx + 70, 800), (cx + 150, 980), (cx - 150, 980), (cx - 70, 800)], o * kc, 1.8, cerrada=True)
    lz.texto("CÁMARA", cx, 745, 24, "SemiBold Condensed", o * kc, "mm", esp=0.16)
    # flujos (puntos que viajan)
    rutas = [[(520, 330), (520, 420), (640, 460), (640, 520)], [(640, 582), (640, 650), (cx - 60, 690)],
             [(1400, 330), (1400, 420), (1280, 460), (1280, 520)], [(1280, 582), (1280, 650), (cx + 60, 690)]]
    for j, r in enumerate(rutas):
        oo = o * (k1 if j in (0, 2) else kc)
        lz.l2(r, oo * 0.5, 1.2)
        L = [math.dist(r[i], r[i + 1]) for i in range(len(r) - 1)]
        tot = sum(L)
        for q in range(6):
            s = ((t * 120 + q * tot / 6) % tot)
            for i, li in enumerate(L):
                if s <= li:
                    u = s / li
                    lz.c2(r[i][0] + (r[i + 1][0] - r[i][0]) * u, r[i][1] + (r[i + 1][1] - r[i][1]) * u, 4, oo, lleno=True)
                    break
                s -= li
    on = ap(t, ww("raptor", 2, "nada") - 0.1)
    lz.texto("NADA SE DESPERDICIA", 1500, 860, 44, "Bold Condensed", on, "mm", esp=0.06)
    return lz


def r_cifras(t):
    t0 = F0("raptor", 3) - 0.3
    o1 = ap(t, ww("raptor", 3, "doscientas") - 0.1)
    o2 = ap(t, ww("raptor", 4, "mil") - 0.1)
    def ex(lz, tt):
        lz.texto("250 t", W - 100, 380, 150, "Bold Condensed", o1, "rm", esp=0.02)
        lz.texto("DE EMPUJE · NIVEL DEL MAR", W - 104, 470, 24, "SemiBold Condensed", o1 * 0.9, "rm", esp=0.16)
        lz.texto("1 525 KG", W - 100, 620, 110, "Bold Condensed", o2, "rm", esp=0.02)
        lz.texto("LO QUE PESA UN COCHE", W - 104, 690, 24, "SemiBold Condensed", o2 * 0.9, "rm", esp=0.16)
    return rp("r3", SEG["r3"], t0, "RAPTOR 3", "PRUEBA DE ENCENDIDO", extra=ex)(t)


def r_por33(t):
    t0 = F0("raptor", 5) - 0.3
    lz = vacio()
    k = pr(t, t0 + 0.3, t0 + 2.4)
    o = ap(t, t0) * (1 - ap(t, F0("raptor", 6) - 0.2))
    panel33(lz, 960, 520, 48, op=o, k_aparece=k)
    contador(lz, 960, 520, max(1, 33 * k), None, o * 0.0)
    lz.texto("× 33", 1420, 520, 140, "Bold Condensed", o * ap(t, t0 + 0.2), "lm", esp=0.02)
    lz.texto(f"{int(round(33 * k)):02d}", 520, 520, 140, "Bold Condensed", o, "rm", esp=0.02)
    # barras de empuje total
    ob = ap(t, F0("raptor", 6) - 0.2)
    if ob > 0:
        barras(lz, t, 300, 470, [("SATURNO V · 5 F-1", 34.5, "34,5 MN", F0("raptor", 6)),
                                 ("SUPER HEAVY · 33 RAPTOR 3", 80.8, "80,8 MN", ww("raptor", 6, "doble") - 0.4)], 0, 80.8,
               ancho=1100, sep=170)
        lz.texto("MÁS DEL DOBLE", 960, 880, 64, "Bold Condensed", ap(t, ww("raptor", 6, "doble")), "mm", esp=0.06)
    cabecera(lz, "EMPUJE AL DESPEGAR", max(o, ob))
    return lz


# ------------------------------------------------------------------ ANILLOS
def a_3d(t):
    """El propulsor gira y la cámara baja hasta mirar sus motores desde abajo."""
    t0 = T0("anillos")
    k = e_inout(pr(t, t0, F0("anillos", 1)))
    el = lerp(10, -80, k)
    foco = Z * lerp(30, 4, k)
    lz = L3(cam_orb(foco, lerp(110, 22, k), 200 + 40 * k, el, centro=(W * 0.5, H * 0.52)))
    S.super_heavy(lz, O, Z, 1.0, 1.0, op=1.0, ref=Y, rot=0.2 * t)
    lz.texto("MIRA LA BASE", 70, 1010, 26, "SemiBold Condensed", ap(t, ww("anillos", 0, "mira")), "lm", esp=0.16)
    return lz


def a_panel(t):
    """3 + 10 + 20 aparecen anillo por anillo; luego los 13 de adentro giran y los 20 de afuera se quedan fijos."""
    lz = vacio()
    t1, t2, t3 = F0("anillos", 1) - 0.1, F0("anillos", 2) - 0.1, F0("anillos", 3) - 0.1
    tg = F0("anillos", 4) - 0.2
    n = 3 * smooth(pr(t, t1, t1 + 0.6)) + 10 * smooth(pr(t, t2, t2 + 0.9)) + 20 * smooth(pr(t, t3, t3 + 1.1))
    gir = ap(t, tg)
    rot = 0.0
    cx, cy, e = 760, 540, 82
    # gimbal: los 13 de adentro se desplazan un poco (dibujo aparte encima)
    panel33(lz, cx, cy, e, op=1.0, k_aparece=n / 33.0, on=set(IDX[0] + IDX[1] + IDX[2]), rot=rot)
    if gir > 0:
        for i in IDX[0] + IDX[1]:
            k_, mx, my, rt = S.motores_sh()[i]
            dx = 0.35 * e * math.sin(t * 2.2) * gir
            dy = 0.25 * e * math.cos(t * 1.7) * gir
            lz.c2(cx + mx * e + dx, cy + my * e + dy, rt * e * 1.18 + 6, gir * 0.9, w=1.4)
    for (tt, txt, sub, y) in ((t1, "3", "EN EL CENTRO", 300), (t2, "10", "ANILLO INTERIOR", 470), (t3, "20", "EN LA ORILLA", 640)):
        o = ap(t, tt) * (1 - ap(t, tg - 0.1))
        lz.texto(txt, 1300, y, 110, "Bold Condensed", o, "lm", esp=0.02)
        lz.texto(sub, 1420, y, 30, "SemiBold Condensed", o, "lm", esp=0.14)
    og = vent(t, tg, F0("anillos", 5) - 0.1)
    bloque(lz, 1300, 420, "13 GIRAN", "DIRIGEN EL COHETE (GIMBAL)", og, 90)
    of = ap(t, F0("anillos", 5) - 0.2)
    bloque(lz, 1300, 420, "20 FIJOS", "SOLO EMPUJAN", of, 90)
    cabecera(lz, "SUPER HEAVY · VISTA DESDE ABAJO")
    return lz


def a_fuerza(t):
    t0 = F0("anillos", 6) - 0.3
    lz = vacio()
    panel33(lz, 560, 540, 64, op=ap(t, t0), on=set(IDX[2]), resalta={2})
    panel33(lz, 1360, 540, 64, op=ap(t, ww("anillos", 6, "precisión") - 0.2), on=set(IDX[0] + IDX[1]), resalta={0, 1})
    lz.texto("FUERZA BRUTA", 560, 170, 64, "Bold Condensed", ap(t, t0 + 0.1), "mm", esp=0.06)
    lz.texto("20 DE AFUERA", 560, 225, 22, "SemiBold Condensed", ap(t, t0 + 0.1), "mm", esp=0.2)
    op_ = ap(t, ww("anillos", 6, "precisión") - 0.1)
    lz.texto("PRECISIÓN", 1360, 170, 64, "Bold Condensed", op_, "mm", esp=0.06)
    lz.texto("13 DEL CENTRO", 1360, 225, 22, "SemiBold Condensed", op_, "mm", esp=0.2)
    lz.texto("CLAVE PARA EL FINAL DEL VIAJE", W / 2, 990, 30, "SemiBold Condensed", ap(t, ww("anillos", 6, "clave") - 0.1), "mm", esp=0.16)
    return lz


# ------------------------------------------------------------------ SATURNO V
def s_cinco(t):
    t0 = F0("saturno", 1) - 0.3
    lz = vacio()
    o = ap(t, t0)
    cx, cy, e = 1380, 520, 64
    lz.c2(cx, cy, 5.05 * e, o * 0.55, w=1.2)
    for j, (dx, dy) in enumerate(((0, 0), (2.4, 2.4), (-2.4, 2.4), (2.4, -2.4), (-2.4, -2.4))):
        oj = o * ap(t, t0 + 0.4 + 0.25 * j)
        lz.c2(cx + dx * e, cy + dy * e, 1.85 * e, oj, w=1.6, lleno=True)
        lz.c2(cx + dx * e, cy + dy * e, 1.85 * e + 8, oj * 0.5, w=1.0)
    lz.texto("5 MOTORES F-1", cx, cy + 5.7 * e, 44, "Bold Condensed", o, "mm", esp=0.06)
    lz.texto("EL MOTOR DE UNA SOLA CÁMARA MÁS POTENTE QUE HA VOLADO", cx, cy + 5.7 * e + 44, 19, "SemiBold Condensed",
             ap(t, ww("saturno", 1, "grandes") - 0.2) * 0.9, "mm", esp=0.12)
    cabecera(lz, "SATURNO V · PRIMERA ETAPA S-IC")
    return lz


def s_vs(t):
    t0 = F0("saturno", 2) - 0.3
    lz = vacio()
    barras(lz, t, 300, 430, [("UN F-1", 6770, "6 770 kN", t0 + 0.2), ("UN RAPTOR 3", 2452, "2 452 kN", t0 + 0.9)], 0, 6770,
           ancho=1100, sep=200)
    lz.texto("CASI 3 VECES", 960, 880, 72, "Bold Condensed", ap(t, ww("saturno", 2, "tres") - 0.2), "mm", esp=0.05)
    cabecera(lz, "EMPUJE DE UN SOLO MOTOR · NIVEL DEL MAR", ap(t, t0))
    return lz


def s_vibra(t):
    """El fuego que vibra: onda de presión que crece hasta romper la cámara (sobre el clip del F-1)."""
    t0 = F0("saturno", 4) - 0.3
    def ex(lz, tt):
        o = ap(tt, t0 + 0.5)
        amp = 6 + 90 * smooth(pr(tt, ww("saturno", 4, "vibrar") - 0.3, ww("saturno", 4, "milésimas")))
        pts = [(140 + i * 4, 860 + amp * math.sin(i * 0.35 + tt * 18) * (0.6 + 0.4 * math.sin(i * 0.05))) for i in range(420)]
        lz.l2(pts, o, 1.6)
        lz.texto("INESTABILIDAD DE COMBUSTIÓN", 140, 740, 40, "Bold Condensed", o, "lm", esp=0.06)
    return rp("s1c", SEG["s1c_f1"], t0, None, None, extra=ex)(t)


def s_bomba(t):
    """Corte de la cámara: una bomba pequeña detona dentro y la presión debe calmarse sola."""
    t0 = F0("saturno", 5) - 0.3
    lz = vacio()
    o = ap(t, t0)
    cx = 760
    lz.l2([(cx - 260, 260), (cx + 260, 260)], o, 2.2)                       # inyector
    for i in range(14):
        x = cx - 240 + i * 37
        lz.l2([(x, 260), (x, 285)], o * 0.7, 1.2)
    lz.l2([(cx - 260, 260), (cx - 260, 560), (cx - 120, 700), (cx - 300, 960)], o, 1.8)
    lz.l2([(cx + 260, 260), (cx + 260, 560), (cx + 120, 700), (cx + 300, 960)], o, 1.8)
    lz.texto("INYECTOR", cx, 220, 22, "SemiBold Condensed", o, "mm", esp=0.2)
    tb = ww("saturno", 5, "bombas")
    kb = pr(t, tb, tb + 0.8)
    if 0 < kb < 1:
        for a in range(16):
            ang = a * math.pi / 8
            r0, r1 = 10 + 60 * kb, 30 + 180 * kb
            lz.l2([(cx + r0 * math.cos(ang), 430 + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), 430 + r1 * math.sin(ang))], (1 - kb), 2.0)
    ob = ap(t, tb - 0.3)
    lz.texto("BOMBA", cx + 300, 430, 34, "Bold Condensed", ob * (1 - ap(t, tb + 1.2)), "lm", esp=0.08)
    # gráfica de presión: pico y amortiguación
    gx, gy = 1180, 620
    og = ap(t, tb + 0.3)
    lz.l2([(gx, gy - 220), (gx, gy + 120), (gx + 600, gy + 120)], og * 0.8, 1.2)
    lz.texto("PRESIÓN EN LA CÁMARA", gx, gy - 250, 22, "SemiBold Condensed", og, "lm", esp=0.16)
    kk = pr(t, tb + 0.3, tb + 3.5)
    pts = []
    for i in range(int(300 * kk) + 1):
        u = i / 300
        v = 0 if u < 0.15 else 180 * math.exp(-(u - 0.15) * 9) * math.sin((u - 0.15) * 70)
        pts.append((gx + u * 600, gy - v))
    if len(pts) > 1:
        lz.l2(pts, og, 1.8)
    lz.texto("¿SE RECUPERA SOLO?", gx + 300, gy + 190, 40, "Bold Condensed", ap(t, ww("saturno", 5, "recuperaba") - 0.3), "mm", esp=0.06)
    cabecera(lz, "PRUEBA DE ESTABILIDAD · F-1", o)
    return lz


def s_anos(t):
    t0 = F0("saturno", 6) - 0.3
    o = ap(t, t0 + 0.1)
    o2 = ap(t, ww("saturno", 7, "ningún") - 0.2)
    o3 = ap(t, ww("saturno", 7, "lección") - 0.2)
    def ex(lz, tt):
        k = 1 - ap(tt, F0("saturno", 7) - 0.2)
        lz.texto("MÁS DE 3 AÑOS", W / 2, 470, 130, "Bold Condensed", o * k, "mm", esp=0.03)
        lz.texto("PARA RESOLVERLO", W / 2, 560, 28, "SemiBold Condensed", o * k, "mm", esp=0.2)
        lz.texto("65 F-1 EN VUELO", W - 100, 380, 70, "Bold Condensed", o2 * (1 - o3), "rm", esp=0.04)
        lz.texto("NINGUNO FALLÓ ASÍ", W - 104, 440, 26, "SemiBold Condensed", o2 * (1 - o3), "rm", esp=0.16)
        lz.texto("UN MOTOR GIGANTE =", W - 100, 380, 50, "Bold Condensed", o3, "rm", esp=0.05)
        lz.texto("LENTO Y CARO DE PERFECCIONAR", W - 100, 450, 50, "Bold Condensed", o3, "rm", esp=0.05)
    return rp("s1c", SEG["s1c"], t0, "SATURNO V · ETAPA S-IC", "PRUEBA ESTÁTICA · NASA", extra=ex)(t)


# ------------------------------------------------------------------ montaje 1
PLANOS = [
    (0.0, rp("f10mesa", SEG["mesa"], 0.0, "STARSHIP · SUPER HEAVY", "VISTA DESDE LA MESA DE LANZAMIENTO",
             extra=lambda lz, t: lz.texto("33", W - 100, 470, 220, "Bold Condensed", ap(t, ww("gancho", 1, "treinta")), "rm", esp=0.02)
             or lz.texto("MOTORES RAPTOR", W - 106, 600, 30, "SemiBold Condensed", ap(t, ww("gancho", 1, "motores")), "rm", esp=0.18))),
    (ww("gancho", 1, "es") - 0.2, rp("f10mesa", SEG["mesa_desp"], ww("gancho", 1, "es") - 0.2, "EL COHETE MÁS PODEROSO",
                                    "QUE SE HA CONSTRUIDO")),
    (F0("gancho", 2) - 0.3, g_vs),
    (F0("gancho", 3) - 0.3, g_n1),
    (F0("gancho", 4) - 0.3, rp("b7", SEG["b7_lenta"], F0("gancho", 4) - 0.3, "¿POR QUÉ 33?", None, vel=0.6)),
    (F0("gancho", 5) - 0.3, g_titulo),
    (T0("raptor"), con_foto(rp("r3b", SEG["r3b"], T0("raptor"), "RAPTOR", "EL MOTOR DE STARSHIP"),
                            dict(nombre="raptor_merlin", cx=1380, cy=470, ancho=620, t0=ww("raptor", 0, "raptor") - 0.2,
                                 t1=F0("raptor", 1) - 0.1, rotulo="RAPTOR (DERECHA) Y MERLIN", sub="FOTO: COMMONS · CC BY-SA 4.0",
                                 estilo=3, asp=1.35))),
    (F0("raptor", 1) - 0.3, rp("r3", SEG["r3_b"], F0("raptor", 1) - 0.3, "METANO + OXÍGENO", "LOS DOS LÍQUIDOS, BAJÍSIMA TEMPERATURA")),
    (F0("raptor", 2) - 0.3, r_ciclo),
    (F0("raptor", 3) - 0.3, r_cifras),
    (F0("raptor", 5) - 0.3, r_por33),
    (T0("anillos"), a_3d),
    (F0("anillos", 1) - 0.3, a_panel),
    (F0("anillos", 5) + 2.0, rp("f10mesa", 18.0, F0("anillos", 5) + 2.0, "LOS 20 DE AFUERA", "VAN FIJOS · SOLO EMPUJAN", vel=0.8)),
    (F0("anillos", 6) - 0.3, a_fuerza),
    (T0("saturno"), rp("a11", SEG["a11_f1"], T0("saturno"), "APOLO 11 · 1969", "LOS MOTORES F-1 AL ENCENDER", vel=0.7)),
    (F0("saturno", 1) - 0.3, con_foto(s_cinco, dict(nombre="f1_vonbraun", cx=540, cy=500, ancho=560, t0=F0("saturno", 1),
                                                     t1=F0("saturno", 2) - 0.4, rotulo="WERNHER VON BRAUN Y LOS F-1",
                                                     sub="FOTO: NASA", estilo=0, asp=0.82))),
    (F0("saturno", 2) - 0.3, s_vs),
    (F0("saturno", 3) - 0.3, rp("s1c", SEG["s1c_b"], F0("saturno", 3) - 0.3, "HACER UN MOTOR TAN GRANDE", "CASI FRACASA")),
    (F0("saturno", 4) - 0.3, s_vibra),
    (F0("saturno", 5) - 0.3, s_bomba),
    (F0("saturno", 6) - 0.3, s_anos),
]


def sfx():
    v = [(0.6, "pulso", 0.9, 0.0, None), (F0("gancho", 1), "rugido", 0.8, 0.0, None), (F0("gancho", 3), "explosion", 0.7, 0.0, None),
         (F0("gancho", 6) - 0.2, "pulso", 0.9, 0.0, None), (T0("raptor"), "whoosh", 0.6, 0.0, None),
         (F0("raptor", 1), "ignicion", 0.6, 0.0, None), (F0("raptor", 5), "tic", 0.5, 0.0, None),
         (ww("raptor", 6, "doble"), "sello", 0.7, 0.0, None), (T0("anillos"), "whoosh", 0.6, 0.0, None),
         (F0("anillos", 1), "hud", 0.6, -0.2, None), (F0("anillos", 2), "hud", 0.6, 0.0, None), (F0("anillos", 3), "hud", 0.6, 0.2, None),
         (F0("anillos", 4), "gira", 0.6, 0.0, None), (T0("saturno"), "rugido", 0.7, 0.0, None),
         (F0("saturno", 4), "vibra", 0.7, 0.0, None), (ww("saturno", 5, "bombas"), "explosion", 0.5, 0.0, None),
         (F0("saturno", 6), "sello", 0.7, 0.0, None)]
    return v
