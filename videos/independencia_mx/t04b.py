# -*- coding: utf-8 -*-
"""Escena 4 (continuación) · el líder que falta, Hidalgo y sus oficios, la fecha y la delación, Josefa Ortiz avisa desde su encierro."""
import datetime
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import kz_retrato as RT
import kz_ui as U
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_e as me
from t04 import *  # noqa: F401,F403  (anclas, MP, BASE, CAL, TAL, GRAD, PURPURA, E4…)
from t04 import E4, MP, BASE, CAL, TAL, GRAD, PURPURA

t_logro = T(E4, "logro", frase=6)
T_H = t_cons - 0.2

PLA = me.PlazaPueblo()


def _espadas(lz, x, y, s=1.0, k=1.0, col=(238, 240, 250)):
    """Espadas cruzadas (icono de levantamiento armado) en coordenadas de pantalla."""
    for sg in (-1, 1):
        p0 = np.array([x - sg * 70 * s * k, y - 70 * s * k])
        p1 = np.array([x + sg * 70 * s * k, y + 70 * s * k])
        lz.trazo(np.array([p0, p1]), col, 12 * s * k, afinar=False, temblor=0.0, capa=2)
        lz.trazo(np.array([p0 * 0.8 + p1 * 0.2, p0 * 0.8 + p1 * 0.2]) + np.array([[-sg * 0, 0], [0, 0]]), col, 1.0, afinar=False, temblor=0.0, capa=2)
        gx, gy = x - sg * 30 * s * k, y - 30 * s * k
        lz.trazo(np.array([[gx - 22 * s * k, gy + sg * 22 * s * k], [gx + 22 * s * k, gy - sg * 22 * s * k]]), (250, 206, 70), 9 * s * k, afinar=False, temblor=0.0, capa=2)


# ------------------------------------------------------------------------------------------------ 4. FALTABA UN LÍDER
def cam_plaza_p(t):
    return K(t, [(T_D, (170, 190, 22, 2.6)), (t_lid, (165, 165, 26, 3.4)), (t_pue, (170, 185, 22, 3.0)), (t_enc - 0.5, (172, 200, 20, 2.5))])


@shot(T_D, bg=lambda t: bg_grad((120, 190, 240), (250, 232, 200), mid=(190, 214, 236), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def q_sillon(lz, t):
    cx, cy, cz, zm = cam_plaza_p(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz()
    PLA.suelo(lz, iso, t)
    m = PLA.objetos(t)
    # el pueblo se va juntando frente a la tarima; los cuatro conspiradores miran el sillón vacío
    mu = G.Multitud()
    tipos = ("campesino", "campesina", "mestizo", "indigena", "indigena_f", "arriero", "nino", "comerciante")
    reunido = e_inout(prog(t, t_pue - 0.2, t_pue + 1.4))
    for i in range(26):
        ang = 6.28 * h01(9, i)
        rad = 60 + 110 * h01(10, i)
        cx0, cy0 = 165 + 150 * math.cos(ang) * (1 - 0.15 * reunido), 250 + 70 * math.sin(ang) * (1 - 0.15 * reunido)
        mu.ronda((cx0, cy0), 24, tipos[i % len(tipos)], n=1, seed=5000 + i * 3, h=40 if tipos[i % len(tipos)] != "nino" else 28)
    mu.dibujar(m, t)
    for i, (x, y, tp, cr) in enumerate(((104, 150, "oficial", "serio"), (110, 190, "dragon", "serio"), (238, 150, "noble", "normal"), (232, 190, "regidor", "normal"))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, cr, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(1, -0.3) if i < 2 else (-1, -0.3), seed=5200 + i, h=50, cara=cr, accion=("habla" if (i % 2 == 0 and t > t_lid) else None))))(x, y, tp, cr, i), fijo=False, clave=x + y + 4)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=31, y0=80, y1=260)
    # signos de interrogación sobre el sillón y la pregunta del pueblo
    sx, sy = iso.P(165, 140, 74)
    kq = U.pop(t, t_falt - 0.05) * U.salida(t, t_enc - 0.1, 0.25)
    if kq > 0.01:
        P.rotulo(lz, float(sx), float(sy) - 20 + 10 * math.sin(t * 3), "?", px=int(220 * kq + 10), k=kq, color=(255, 214, 72))
    for i, dx in enumerate((-230, 230)):
        kk = U.pop(t, t_lid + 0.1 * i) * U.salida(t, t_enc - 0.1, 0.25)
        if kk > 0.01:
            U.globo(lz, float(sx) + dx, float(sy) + 40, "¿quién?", px=34, k=kk)
    kl = U.pop(t, t_lid - 0.1) * U.salida(t, t_pue, 0.2)
    if kl > 0.01:
        U.llamada(lz, W / 2, 130, "un líder", color=U.COL["naranja"], px=84, k=kl * U.repop(t, t_lid + 0.3), cola=None)
    kp = U.pop(t, t_pue - 0.1) * U.salida(t, t_enc - 0.1, 0.25)
    if kp > 0.01:
        U.llamada(lz, W / 2, 130, "que el pueblo sintiera suyo", color=U.COL["verde"], px=62, k=kp * U.repop(t, t_pue + 0.5), cola=None)


def cam_dolores_m(t):
    return Klog(t, [(t_enc - 0.4, (-100.2, 20.9, 1.4)), (t_dol, (-100.93, 21.16, 2.4)), (T_E, (-100.93, 21.16, 3.2))])


@shot(t_enc - 0.4, bg=lambda t: BASE(cam_dolores_m(t), t), post=[GRAD], ent=("zoom", 0.7))
def q_dolores_mapa(lz, t):
    cam = cam_dolores_m(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=13)
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.16, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp) in enumerate((("queretaro", "ciudad"), ("guanajuato", "ciudad"), ("san_luis", "ciudad"), ("mexico", "ciudad"))):
        MD.ciudad(lz, cam, lug, t, t_enc - 0.4 + 0.05 * j, tam=1.6, tipo=tp, bando="real", semilla=j + 41)
    MD.ciudad(lz, cam, "dolores", t, t_dol - 0.1, tam=3.2, tipo="pueblo", bando=(255, 206, 70), nombre="Dolores", px=40, llama=True)
    MD.ciudad(lz, cam, (-100.74, 20.91), t, t_dol + 0.1, tam=1.4, tipo="pueblo", bando="real", nombre="San Miguel", px=26)
    kh = U.pop(t, t_hid - 0.1)
    if kh > 0.01:
        MD.medallon(lz, 1560, 480, 190, "hidalgo", t, emocion="neutro", k=kh, seed=2)
        U.llamada(lz, 1560, 700, "Miguel Hidalgo", color=U.COL["morado"], px=52, k=kh * U.repop(t, t_hid + 0.4), cola="arriba")
        U.llamada(lz, 1560, 850, "cura de Dolores", color=U.COL["naranja"], px=44, k=U.pop(t, t_cur + 0.1), cola=None)
    kd = U.pop(t, t_dol - 0.05) * U.salida(t, t_cur, 0.2)
    if kd > 0.01:
        U.llamada(lz, 640, 130, "Dolores", color=U.COL["azul"], px=80, k=kd * U.repop(t, t_dol + 0.4), cola=None)
    MD.brujula(lz, 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 5. HIDALGO Y SUS OFICIOS
def cam_talleres(t):
    return K(t, [(T_E, (210, 200, 26, 2.4)), (t_len, (200, 190, 24, 3.1)), (t_ens, (320, 90, 26, 3.2)), (t_cam + 0.2, (330, 70, 30, 3.5)), (t_ofc + 0.2, (70, 270, 22, 3.3)), (t_pob - 0.8, (60, 60, 22, 3.2)), (T1(E4) - 12.4, (190, 190, 30, 2.5))])


@shot(T_E, bg=lambda t: bg_grad((136, 200, 240), (252, 236, 206), mid=(196, 220, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def q_talleres(lz, t):
    cx, cy, cz, zm = cam_talleres(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    TAL.suelo(lz, iso, t)
    m = TAL.objetos(t)
    # Hidalgo (cura) con un grupo de indígenas y campesinos que lo escuchan
    hx, hy = 205.0, 208.0
    m.add(hx - 4, hy - 4, hx + 4, hy + 4, 40, lambda lz, iso: G.persona(lz, iso, hx, hy, t, "cura", dir=(0.5, -0.7), seed=5300, h=50, accion="habla", cara="habla"), fijo=False, clave=hx + hy + 3)
    for i, (x, y, tp) in enumerate(((236, 190, "indigena"), (232, 224, "indigena_f"), (180, 190, "mestizo"), (262, 210, "campesino"), (190, 236, "campesina"))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(-0.8, 0.3) if x > hx else (0.8, 0.3), seed=5310 + i, h=42, accion=("habla" if (t > t_len + 0.3 and i == 1) else None))))(x, y, tp, i), fijo=False, clave=x + y + 3)
    # alfareros en el taller de barro, apicultores y viñadores
    for i, (x, y, tp, ac) in enumerate(((330, 108, "campesino", "trabaja"), (352, 112, "indigena", "trabaja"), (324, 126, "mestizo", None), (60, 270, "campesina", "trabaja"), (112, 280, "campesino", None),
                                        (40, 60, "campesino", "trabaja"), (80, 90, "indigena_f", "trabaja"), (24, 100, "mestizo", "trabaja"), (250, 304, "campesina", "trabaja"), (272, 312, "indigena_f", "trabaja"))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, ac, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(0.6, 0.8), seed=5320 + i, h=42, accion=ac)))(x, y, tp, ac, i), fijo=False, clave=x + y + 3)
    mu = G.Multitud()
    mu.camina([(-30, 340), (120, 270), (200, 200), (260, 120), (350, 60), (430, 20)], "arriero", vel=14, seed=77, bucle="ida_vuelta")
    for i in range(6):
        mu.ronda((200 + 40 * (i % 3), 200 + 30 * (i // 3)), 40, ("campesino", "indigena", "mestizo", "campesina", "indigena_f", "nino")[i], n=1, seed=5400 + i, h=40 if i != 5 else 28)
    mu.dibujar(m, t)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=6, seed=33, y0=70, y1=240)
    DC.mariposas(lz, iso, 20, 20, 400, 380, n=6, t=t)
    U.fecha_lugar(lz, t, T_E, t_len - 0.2, "Dolores", "Hidalgo, el cura", y=70)
    # idiomas indígenas: globos de diálogo con el nombre de cada lengua
    for i, (lang, dx, dy, col) in enumerate((("náhuatl", -90, -30, U.COL["naranja"]), ("otomí", 40, -80, U.COL["azul"]), ("purépecha", 150, -30, U.COL["verde"]))):
        k = U.pop(t, t_len + 0.2 + 0.35 * i) * U.salida(t, t_ens - 0.1, 0.25)
        if k > 0.01:
            sx, sy = iso.P(hx, hy, 70)
            U.llamada(lz, float(sx) + dx * 1.7, float(sy) + dy * 1.7 - 40, lang, color=col, px=44, k=k, cola="abajo")
    kh = U.pop(t, T_E + 0.1) * U.salida(t, t_len + 0.4, 0.25)
    if kh > 0.01:
        sx, sy = iso.P(hx, hy, 66)
        U.llamada(lz, float(sx), float(sy) - 8, "Hidalgo", color=U.COL["morado"], px=44, k=kh, cola="abajo")
    k = U.pop(t, t_cul) * U.salida(t, t_len - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un hombre culto", color=U.COL["morado"], px=70, k=k, cola=None)
    # oficios que enseñaba: se etiquetan cuando la cámara llega a cada taller
    for (lab, x, y, z_, t0_, t1_, col) in (("alfarería", 330, 92, 70, t_ens + 0.1, t_cam + 0.9, U.COL["naranja"]), ("apicultura", 82, 262, 40, t_ofc - 0.5, t_ofc + 1.0, U.COL["morado"]),
                                          ("vid", 52, 60, 30, t_ofc + 0.9, t_pob - 0.6, U.COL["verde"]), ("seda", 250, 296, 60, t_ofc + 1.3, t_pob, U.COL["azul"])):
        k = U.pop(t, t0_) * U.salida(t, t1_, 0.25)
        if k > 0.01:
            sx, sy = iso.P(x, y, z_)
            U.llamada(lz, float(sx), float(sy) - 10, lab, color=col, px=48, k=k * U.repop(t, t0_ + 0.5), cola="abajo")
    k = U.pop(t, t_pob - 0.6)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "para salir de la pobreza", color=U.COL["verde"], px=68, k=k * U.repop(t, t_pob + 0.2), cola=None)
        for i in range(10):
            U.chispa4(lz, 300 + 1300 * h01(8, i), 240 + 600 * h01(9, i), 10 + 8 * h01(7, i), alfa=0.8 * k)


# ------------------------------------------------------------------------------------------------ 6. LA FECHA (CALENDARIO)
def _calendario(lz, x, y, s, k, t, t_circ):
    w, h = 760 * s, 640 * s
    lz.relleno(rect_red(x - w / 2 + 16 * s, y - h / 2 + 20 * s, w, h, 30 * s), (20, 10, 50), alfa=0.35, capa=1)
    lz.relleno(rect_red(x - w / 2, y - h / 2, w, h, 30 * s), (252, 248, 238), capa=1)
    lz.relleno(rect_red(x - w / 2, y - h / 2, w, 150 * s, 30 * s), (206, 56, 70), capa=1)
    lz.relleno(np.array([[x - w / 2, y - h / 2 + 100 * s], [x + w / 2, y - h / 2 + 100 * s], [x + w / 2, y - h / 2 + 150 * s], [x - w / 2, y - h / 2 + 150 * s]]), (206, 56, 70), capa=1)
    for dx in (-0.28, 0.28):                                        # argollas
        lz.relleno(rect_red(x + dx * w - 12 * s, y - h / 2 - 22 * s, 24 * s, 56 * s, 12 * s), (90, 80, 110), capa=2)
    P.rotulo(lz, x, y - h / 2 + 76 * s, "OCTUBRE", px=int(86 * s), k=k, color=(255, 255, 255))
    P.rotulo(lz, x + w / 2 - 100 * s, y - h / 2 + 76 * s, "1810", px=int(40 * s), k=k, color=(255, 230, 160))
    d0 = datetime.date(1810, 10, 1).weekday()                          # lunes = 0
    off = (d0 + 1) % 7                                                 # semana que empieza en domingo
    gx, gy = x - w / 2 + 60 * s, y - h / 2 + 200 * s
    cw, ch = (w - 120 * s) / 7, 78 * s
    for j, dn in enumerate("DLMMJVS"):
        P.rotulo(lz, gx + (j + 0.5) * cw, gy, dn, px=int(34 * s), k=k, color=(150, 120, 160), sombra=0.0)
    for n in range(1, 32):
        c, r = (off + n - 1) % 7, (off + n - 1) // 7
        P.rotulo(lz, gx + (c + 0.5) * cw, gy + 62 * s + r * ch, str(n), px=int(46 * s), k=k, color=(206, 56, 70) if c == 0 else (70, 50, 100), sombra=0.0)
    # marca roja que se dibuja alrededor del día 2 (el levantamiento planeado)
    u = prog(t, t_circ, t_circ + 0.9)
    c, r = (off + 1) % 7, (off + 1) // 7
    if u > 0.001:
        px_, py_ = gx + (c + 0.5) * cw, gy + 62 * s + r * ch
        ang = np.linspace(-1.2, -1.2 + 6.9 * u, 40)
        pts = np.stack([px_ + 44 * s * np.cos(ang) * (1 + 0.05 * ang), py_ + 38 * s * np.sin(ang) * (1 + 0.05 * ang)], 1)
        lz.trazo(pts, (226, 40, 60), 9 * s, afinar=False, temblor=0.0, capa=2)


@shot(T_F, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def q_calendario(lz, t):
    U.bokeh(lz, t, seed=15, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, 760, 520, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    U.chispas(lz, t, n=18, seed=16, tam=(5, 12))
    k = U.pop(t, T_F + 0.05, 1.3)
    ex = U.salida(t, t_per - 0.1, 0.35)
    if ex > 0.01:
        with lz.grupo(960 - 330 * (1 - ex) * 0, 560, 1.0, rot=0.06 * math.sin(t * 1.3) * ex):
            _calendario(lz, 0, 0, 1.0 * (0.94 + 0.06 * k), k * ex, t, t_oct - 0.35)
    # espadas cruzadas que brillan junto al día marcado
    ke = U.pop(t, t_lev + 0.1) * U.salida(t, t_per - 0.1, 0.25)
    if ke > 0.01:
        _espadas(lz, 1490, 520, 1.5, ke)
        lz.halo(1490, 520, 260, (255, 220, 120), alfa=0.30 * ke, capa=0)
    kf = U.pop(t, t_fec - 0.05) * U.salida(t, t_per - 0.1, 0.25)
    if kf > 0.01:
        U.llamada(lz, 330, 190, "la fecha del levantamiento", color=U.COL["naranja"], px=54, k=kf, cola=None)


# ------------------------------------------------------------------------------------------------ 7. EL DELATOR (calle de noche)
def cam_delat(t):
    return K(t, [(t_per - 0.1, (230, 190, 30, 2.6)), (t_alg, (230, 188, 32, 3.2)), (t_del, (240, 186, 34, 3.6)), (T_G, (240, 184, 34, 3.4))])


@shot(t_per - 0.1, bg=lambda t: bg_grad((12, 14, 56), (60, 50, 118), mid=(30, 30, 92), ym=0.45), post=[lambda img, t: U.gradacion(img, luces=(1.0, 0.98, 1.04), sombras=(0.92, 0.94, 1.08), saturacion=1.04)], ent=("tinta", 0.7))
def q_delator(lz, t):
    cx, cy, cz, zm = cam_delat(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.72, 0.78, 1.0), mix=(30, 34, 100), k=0.26)
    for i in range(60):
        x, y = (h01(14, i, 1) * 2000) % 1920, (h01(14, i, 2) * 560)
        lz.relleno(circulo(x, y, 1.6 + 2.0 * h01(14, i, 3), 6), (255, 244, 210), alfa=0.4 + 0.4 * math.sin(t * 2 + i), capa=0)
    lz.halo(1560, 150, 280, (150, 170, 255), alfa=0.35, capa=0)
    lz.relleno(circulo(1560, 150, 66, 28), (242, 246, 255), capa=0)
    CAL.suelo(lz, iso, t)
    m = CAL.objetos(t, gente=0.25, farolas=1.0)
    # el delator se acerca por la calle y le entrega la carta al oficial realista que espera junto a la puerta
    ua = e_inout(prog(t, t_per, t_alg + 0.4))
    dx_, dy_ = lerp(120, 222, ua), lerp(236, 214, ua)
    m.add(dx_ - 4, dy_ - 4, dx_ + 4, dy_ + 4, 40, lambda lz, iso: G.persona(lz, iso, dx_, dy_, t, "escribano", dir=(0.9, -0.4), vel=0.0 if ua in (0.0, 1.0) else 1.0, seed=5500, h=50, cara="miedo", accion=None), fijo=False, clave=dx_ + dy_ + 5)
    m.add(236, 206, 246, 218, 40, lambda lz, iso: G.persona(lz, iso, 242, 212, t, "realista", dir=(-0.9, 0.3), seed=5501, h=52, cara="enojo" if t > t_del else "normal"), fijo=False, clave=455)
    kcarta = prog(t, t_alg + 0.2, t_del)
    if 0 < kcarta < 1:
        lx, ly = lerp(dx_ + 4, 238, kcarta), lerp(214, 214, kcarta)
        m.add(lx - 2, ly - 2, lx + 2, ly + 2, 40, lambda lz, iso: O2.pergamino(lz, iso, lx, ly, 34 + 10 * math.sin(kcarta * math.pi), w=8, h=11, abre=1.0), fijo=False, clave=lx + ly + 9)
    m.dibujar(lz, iso)
    fx, fy = iso.P(232, 212, 20)
    lz.halo(float(fx), float(fy), 220 * iso.z / 3.0, (255, 214, 140), alfa=0.30, capa=2)
    for i in range(8):                                                 # ventanas encendidas
        qx, qy = iso.P(-10 + 60 * i, 110, 28)
        lz.halo(float(qx), float(qy), 40 * iso.z / 3.0, (255, 210, 120), alfa=0.36, capa=2)
    DC.polvo_luz(lz, t, n=20, seed=17, color=(255, 214, 150), alfa=0.4)
    k = U.pop(t, t_alg) * U.salida(t, T_G - 0.2, 0.2)
    if k > 0.01:
        qx, qy = iso.P(dx_, dy_, 62)
        U.llamada(lz, float(qx), float(qy) - 10, "un delator", color=U.COL["rojo"], px=52, k=k, cola="abajo")
    k = U.pop(t, t_del - 0.1)
    if k > 0.01:
        P.rotulo(lz, W / 2, 190, "¡DELATADOS!", px=int(150 * (0.9 + 0.1 * k)), k=k * U.repop(t, t_del + 0.3), color=(255, 90, 90))


# ------------------------------------------------------------------------------------------------ 8. JOSEFA ORTIZ ENCERRADA (pantalla dividida: ella arriba, el alcaide abajo)
def _hab_josefa(lz, t, sx0):
    """Recámara donde encierran a Josefa: cama, ventana con barrotes, puerta con candado; ella golpea el suelo con el zapato."""
    iso = I.Iso(130, 112, 44, 3.3, sx0=sx0, sy0=640)
    c = I.habitacion(lz, iso, 0, 0, 260, 224, 140, piso=(190, 140, 104), pared_a=(240, 222, 188), pared_b=(228, 206, 172), friso=(130, 90, 74))
    N.ventana_vista(lz, iso, c, "yi", 104, 188, 40, 118, t=t, cielo=(150, 200, 250), marco=(250, 244, 230), cortinas=(190, 52, 66), vista="ciudad")
    for kx in range(5):
        I.cara_rect(lz, iso, c, "yi", 112 + kx * 15, 114 + kx * 15, 40, 118, (60, 56, 76))
    me.puerta_cerrada(lz, iso, c, "xi", 120, 176, 104, candado=1.0)
    B.cuadro_pared(lz, iso, c, "xi", 40, 62, 30, 38, color=(70, 120, 170))
    N.escudo(lz, iso, c, "yi", 224, 70, 1.0, "iglesia")
    N.reloj_pie(lz, iso, 14, 150, t, 1.2) if False else None
    N.chimenea(lz, iso, c, "xi", 14, t=t, w=36, h=32)
    m = I.Mundo()
    m.add(220, 120, 240, 140, 40, lambda lz, iso: N.maceta(lz, iso, 230, 130, 1.4, t), clave=230)
    m.add(150, 20, 190, 60, 50, lambda lz, iso: B.estante(lz, iso, 150, 12, 40, 12, 60), clave=170)
    m.add(30, 30, 90, 70, 40, lambda lz, iso: me.cama(lz, iso, 30, 30, t), clave=100)
    m.add(190, 36, 214, 52, 14, lambda lz, iso: N.baul(lz, iso, 190, 38), clave=190)
    m.add(150, 150, 190, 170, 12, lambda lz, iso: B.alfombra(lz, iso, 90, 120, 90, 70, (150, 70, 80), (240, 200, 120)), clave=60)
    golpe = t_logro - 0.1 < t < T_H
    m.add(116, 106, 126, 116, 40, lambda lz, iso: G.persona(lz, iso, 120, 118, t, "dama", dir=(0.2, 1.0), vel=3.0 if golpe else 0.0, seed=5601, h=58, cara="enojo" if golpe else "miedo"), fijo=False, clave=250)
    m.dibujar(lz, iso)
    return iso


def _hab_alcaide(lz, t, sx0):
    """Oficina del alcaide Ignacio Pérez en el piso de abajo: escritorio con papeles, estante, silla; oye los golpes y sale corriendo."""
    iso = I.Iso(130, 112, 44, 3.3, sx0=sx0, sy0=640)
    c = I.habitacion(lz, iso, 0, 0, 260, 224, 140, piso=(150, 108, 82), pared_a=(226, 204, 160), pared_b=(214, 188, 146), friso=(110, 78, 62))
    I.cara_arco(lz, iso, c, "xi", 120, 176, 0, 98, (96, 66, 54))
    N.cortina(lz, iso, c, "xi", 30, 44, 0, 110, (46, 96, 150), t)
    N.cuadro_retrato(lz, iso, c, "yi", 24, 62, 28, 36, fondo=(70, 90, 140))
    N.mapa_pared(lz, iso, c, "yi", 120, 40, 40, 34, t=t)
    N.chimenea(lz, iso, c, "xi", 14, t=t, w=36, h=32) if False else None
    m = I.Mundo()
    m.add(130, 70, 210, 106, 24, lambda lz, iso: B.mesa(lz, iso, 130, 70, 80, 36, 20, color=(120, 80, 60), mantel=(110, 70, 90)), clave=220)
    m.add(20, 20, 50, 60, 40, lambda lz, iso: N.baul(lz, iso, 24, 24), clave=50)
    m.add(20, 90, 40, 110, 40, lambda lz, iso: N.maceta(lz, iso, 30, 100, 1.4, t), clave=130)
    m.add(60, 150, 120, 200, 12, lambda lz, iso: B.alfombra(lz, iso, 50, 130, 100, 70, (60, 90, 150), (240, 200, 120)), clave=40)
    m.add(200, 8, 240, 22, 70, lambda lz, iso: B.estante(lz, iso, 200, 6, 40, 14, 72), clave=230)
    m.add(150, 112, 160, 122, 12, lambda lz, iso: B.silla(lz, iso, 150, 112, 12), clave=240)
    ua = e_inout(prog(t, t_avi - 0.1, t_avi + 0.7))
    px_, py_ = lerp(172, 6, ua), lerp(124, 148, ua)
    mira_arriba = t_logro + 0.5 < t < t_avi - 0.1
    m.add(px_ - 4, py_ - 4, px_ + 4, py_ + 4, 40, lambda lz, iso: G.persona(lz, iso, px_, py_, t, "realista", dir=(-1, 0.3) if ua > 0 else (0.2, -1), vel=0.0 if ua in (0.0, 1.0) else 1.5, seed=5600, h=56, cara="miedo" if mira_arriba else ("alegre" if ua > 0 else "normal")), fijo=False, clave=px_ + py_ + 6)
    m.dibujar(lz, iso)
    return iso


@shot(T_G, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def q_josefa(lz, t):
    I.luz()
    xdiv = W / 2
    pol = np.array([[-10, -10], [xdiv - 26, -10], [xdiv + 26, H / 2], [xdiv - 26, H + 10], [-10, H + 10]], float)
    with lz.recorte(pol):
        lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (66, 36, 130), capa=0)
        U.bokeh(lz, t, seed=18, n=8, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
        iso1 = _hab_josefa(lz, t, 470)
        sx, sy = iso1.P(120, 118, 100)
        k = U.pop(t, t_jos + 0.05) * U.salida(t, t_logro - 0.3, 0.2)
        if k > 0.01:
            U.llamada(lz, float(sx), float(sy) - 10, "Josefa Ortiz", color=U.COL["rojo"], px=48, k=k, cola="abajo")
        k = U.pop(t, t_cerr + 0.1) * U.salida(t, t_logro - 0.3, 0.2)
        if k > 0.01:
            qx, qy = iso1.P(0, 148, 60)
            U.llamada(lz, float(qx) + 70, float(qy) + 110, "encerrada", color=U.COL["morado"], px=58, k=k * U.repop(t, t_cerr + 0.5), cola="izq")
        # golpes del zapato: ondas desde el suelo y letras
        for i in range(4):
            tg = t_logro + 0.1 + 0.5 * i
            if tg - 0.05 < t < tg + 1.0:
                gx, gy = iso1.P(120, 124, 0)
                U.ondas_sonoras(lz, float(gx), float(gy), t, tg, dur=0.8, r1=200, n=2, color=(255, 236, 170), ancho=5.0, periodo=0.2, alfa=0.7)
                kk = U.pop(t, tg) * U.salida(t, tg + 0.45, 0.2)
                if kk > 0.01:
                    P.rotulo(lz, float(gx) + 50 + 34 * i, float(gy) - 20 + 24 * i, "¡TOC!", px=int(60 * kk + 8), k=kk, color=(255, 214, 72), rot=0.2 * (i - 1.5))
    pol2 = np.array([[xdiv + 26, -10], [W + 10, -10], [W + 10, H + 10], [xdiv - 26, H + 10], [xdiv + 26, H / 2]], float)
    with lz.recorte(pol2):
        lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (96, 50, 120), capa=0)
        iso2 = _hab_alcaide(lz, t, 1470)
        qx, qy = iso2.P(172, 124, 100)
        k = U.pop(t, t_logro + 0.2) * U.salida(t, t_avi - 0.2, 0.2)
        if k > 0.01:
            U.llamada(lz, float(qx), float(qy) - 10, "el alcaide Ignacio Pérez", color=U.COL["azul"], px=42, k=k, cola="abajo")
        for i in range(3):
            tg = t_logro + 0.3 + 0.5 * i
            if tg < t < tg + 0.8:
                U.ondas_sonoras(lz, float(qx) - 120, 60, t, tg, dur=0.7, r1=140, n=1, color=(255, 236, 170), ancho=4.0, periodo=0.2, alfa=0.55)
    lz.trazo(np.array([[xdiv - 26, -10], [xdiv + 26, H / 2], [xdiv - 26, H + 10]]), (255, 255, 255), 6.0, afinar=False, temblor=0.0, capa=2)
    U.fecha_lugar(lz, t, T_G, T_H - 0.3, "Querétaro", "Septiembre de 1810", y=70)
    k = U.pop(t, t_logro - 0.1) * U.salida(t, T_H - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 980, "golpea el suelo con el zapato", color=U.COL["naranja"], px=54, k=k * U.repop(t, t_logro + 0.4), cola=None)


# ------------------------------------------------------------------------------------------------ 9. EL AVISO CABALGA POR EL BAJÍO
RUTA_P = [(-100.40, 20.59), (-100.55, 20.75), (-100.74, 20.91), (-100.85, 21.05), (-100.93, 21.16)]


def _jinete(lz, x, y, s=1.0, t=0.0, dir=1, col=(130, 78, 54)):
    """Mensajero a caballo galopando (silueta plana) en coordenadas de pantalla."""
    ph = t * 13
    lz.relleno(elipse(x, y + 14 * s, 26 * s, 6 * s), (20, 10, 40), alfa=0.25, capa=2)
    for k_, off in enumerate((-15, -8, 10, 17)):
        a = math.sin(ph + k_ * 1.6) * 8 * s
        lz.trazo(np.array([[x + dir * off * s, y + 2 * s], [x + dir * off * s + dir * a, y + 16 * s]]), P.oscurecer(col, 0.25), 4 * s, afinar=False, temblor=0.0, capa=2)
    lz.relleno(elipse(x, y - 2 * s, 22 * s, 9 * s), col, capa=2)
    lz.relleno(np.array([[x + dir * 14 * s, y - 6 * s], [x + dir * 26 * s, y - 20 * s], [x + dir * 32 * s, y - 16 * s], [x + dir * 20 * s, y + 2 * s]]), col, capa=2)
    lz.relleno(elipse(x + dir * 32 * s, y - 16 * s, 7 * s, 4 * s, rot=0.5 * dir), col, capa=2)
    lz.trazo(np.array([[x - dir * 20 * s, y - 4 * s], [x - dir * 32 * s, y + 4 * s + 3 * math.sin(ph) * s]]), P.oscurecer(col, 0.35), 4 * s, afinar=False, temblor=0.0, capa=2)
    lz.relleno(rect_red(x - 5 * s, y - 24 * s, 10 * s, 18 * s, 4 * s), (90, 120, 200), capa=2)
    lz.relleno(circulo(x, y - 28 * s, 5 * s, 14), (232, 186, 150), capa=2)
    lz.relleno(elipse(x, y - 32 * s, 8 * s, 2.6 * s), (60, 40, 40), capa=2)
    lz.relleno(rect_red(x - 4 * s, y - 38 * s, 8 * s, 7 * s, 2 * s), (60, 40, 40), capa=2)
    for i in range(4):                                                       # polvo del galope
        u = ((t * 2.2 + i * 0.25) % 1.0)
        lz.relleno(circulo(x - dir * (24 + 40 * u) * s, y + 12 * s - 10 * u * s, (5 + 9 * u) * s, 10), (236, 220, 190), alfa=0.5 * (1 - u), capa=2)


def cam_aviso(t):
    return Klog(t, [(T_H, (-100.66, 20.88, 3.2)), (t_desc, (-100.70, 20.90, 3.9)), (T1(E4), (-100.70, 20.90, 4.0))])


@shot(T_H, bg=lambda t: BASE(cam_aviso(t), t), post=[GRAD], ent=("zoom", 0.6))
def q_aviso(lz, t):
    cam = cam_aviso(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.14, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("queretaro", "ciudad", "Querétaro", 40, 60, "arriba"), ((-100.74, 20.91), "pueblo", "San Miguel", 120, -10, "izq"), ("dolores", "pueblo", "Dolores", -110, -10, "der"))):
        MD.ciudad(lz, cam, lug, t, T_H + 0.1 * j, tam=1.25, tipo=tp, bando=(255, 206, 70), semilla=j + 7)
        MD.etiqueta(lz, cam, lug, nm, t, T_H + 0.1 * j + 0.1, px=26, dy=dy, dx=dx, lado=lado)
    f = e_inout(prog(t, T_H + 0.3, t_desc + 0.1))
    MD.ruta(lz, cam, RUTA_P, color=(255, 214, 84), frac=f, t=t, ancho=8.0, flecha=False)
    if 0.01 < f < 0.995:
        x, y, v = MD.punto_ruta(cam, RUTA_P, f)
        _jinete(lz, float(x), float(y) - 8, 2.6, t, dir=1)
    # alarma al llegar: Allende en San Miguel y Hidalgo en Dolores se enteran
    for (nm, lug, lab, dx, dy, t0_) in (("allende", (-100.74, 20.91), "Allende", -330, -150, t_desc - 0.1), ("hidalgo", (-100.93, 21.16), "Hidalgo", 330, -80, t_desc + 0.5)):
        k = U.pop(t, t0_)
        if k > 0.01:
            sx, sy = MP.proy(cam, lug[0], lug[1])
            MD.medallon(lz, float(sx) + dx, float(sy) + dy, 110, nm, t, emocion="serio", k=k, seed=4)
            U.globo(lz, float(sx) + dx, float(sy) + dy + 118, "¡nos descubrieron!", px=30, k=k * U.repop(t, t0_ + 0.3))
    k = U.pop(t, t_avi - 0.1) * U.salida(t, t_cons + 0.9, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "avisa a los conspiradores", color=U.COL["rojo"], px=62, k=k * U.repop(t, t_avi + 0.3), cola=None)
    k = U.pop(t, t_desc - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡descubiertos!", color=U.COL["rojo"], px=92, k=k * U.repop(t, t_desc + 0.4), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_D, "pluck", 0.3)
snd(t_lid, "pop", 0.4)
snd(t_pue, "pop", 0.35)
snd(t_enc - 0.4, "whoosh", 0.3, dur=0.9)
snd(t_hid, "bling", 0.5)
snd(T_E, "amanecer", 0.2, dur=1.6)
snd(t_len, "pop", 0.3)
snd(t_ens, "pop", 0.3)
snd(t_ofc + 0.2, "pop", 0.3)
snd(t_pob, "bling", 0.5)
snd(T_F, "pop", 0.3)
snd(t_oct - 0.35, "garabato", 0.4)
snd(t_alg, "pluck", 0.4)
snd(t_del, "gong", 0.6)
snd(T_G, "pop", 0.3)
for _i in range(3):
    snd(t_logro + 0.1 + 0.5 * _i, "bonk", 0.5)
snd(T_H, "galope", 0.45, dur=2.8)
snd(t_desc, "campana", 0.5)
