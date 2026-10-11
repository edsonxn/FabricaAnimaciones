# -*- coding: utf-8 -*-
"""Escena 1 · gancho (0:00-0:17): Dolores al amanecer (diorama isométrico, campana), el repique recorre el mapa con relieve y título."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_gente_iso as G
import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos

E1 = "gancho"
t_sep, t_cura, t_camp, t_igl, t_pueb = T(E1, "septiembre"), T(E1, "cura"), T(E1, "campana"), T(E1, "iglesia"), T(E1, "pueblo")
t_nadie, t_rep, t_des, t_once, t_guerra = T(E1, "nadie"), T(E1, "repique"), T(E1, "desatar"), T(E1, "once"), T(E1, "guerra")
t_hist, t_compl, t_indep = T(E1, "historia"), T(E1, "completa"), T(E1, "independencia")

DOL = mundos.Dolores()
MP = KM.MAPA
GOLPES = [t_camp + 0.45 * k for k in range(8)]


def ang_campana(t):
    if t < t_camp:
        return 0.0
    u = t - t_camp
    return 0.62 * math.sin(u * 6.98) * math.exp(-u * 0.10)


# ------------------------------------------------------------------------------------------------ fondo y cielo
def bg_amanecer(t):
    a = prog(t, T0(E1), t_nadie)
    return bg_grad((52 + int(30 * a), 30 + int(20 * a), 110), (236, 128 + int(40 * a), 120), mid=(176, 84, 150), ym=0.55)


def nubes(lz, t, escala=1.0):
    """Nubes suaves (círculos rosados con base más oscura) a la deriva debajo y alrededor de la isla (capa de fondo)."""
    for i in range(10):
        x = (h01(i, 1) * 2400 - 240 + t * (6 + 5 * h01(i, 2))) % 2400 - 240
        y = 560 + 480 * h01(i, 3) if i % 2 else 80 + 300 * h01(i, 4)
        r = 70 + 70 * h01(i, 5)
        for (dx, dy, rr, c, a) in ((0, 18, 1.0, (190, 110, 150), 0.55), (-r * 0.7, 6, 0.7, (190, 110, 150), 0.55), (r * 0.7, 10, 0.75, (190, 110, 150), 0.55),
                                   (0, 0, 0.95, (255, 214, 206), 0.9), (-r * 0.65, -4, 0.66, (255, 214, 206), 0.9), (r * 0.65, 0, 0.7, (255, 214, 206), 0.9), (-r * 0.2, -r * 0.3, 0.55, (255, 240, 232), 0.9)):
            lz.relleno(circulo(x + dx, y + dy, r * rr * escala, 18), c, alfa=a, capa=0)


def aves(lz, t, t0, origen, n=9, vel=1.0):
    """Bandada de pájaros que sale volando (V de dos alas que aletean) a partir de t0 desde un punto de pantalla."""
    if t < t0:
        return
    u = t - t0
    for i in range(n):
        ang = -2.3 + 1.6 * h01(i, 9)
        sp = (150 + 160 * h01(i, 10)) * vel
        x = origen[0] + math.cos(ang) * sp * u + 30 * (h01(i, 11) - 0.5)
        y = origen[1] + math.sin(ang) * sp * u * 0.8 - 18 * u
        a = max(0.0, 1.0 - u / 4.5)
        if a <= 0 or x < -40 or x > W + 40 or y < -40 or y > H + 40:
            continue
        al = math.sin(u * 13 + i * 1.7) * 7
        s = 0.8 + 0.5 * h01(i, 12)
        lz.relleno(np.array([[x - 11 * s, y - al * s], [x, y + 1 * s], [x + 11 * s, y - al * s], [x, y - 2 * s]]), (66, 34, 80), alfa=a, capa=2)


def bruma(lz, t, a):
    if a < 0.02:
        return
    for i in range(7):
        x = 300 + 1300 * h01(i, 20) + 40 * math.sin(t * 0.2 + i)
        lz.halo(x, 700 + 160 * h01(i, 21), 380, (255, 220, 220), alfa=0.20 * a, dureza=0.9, capa=2)


# ------------------------------------------------------------------------------------------------ 1. DOLORES
def cam_dolores(t):
    return K(t, [(T0(E1), (232, 236, 10, 0.80)), (t_cura - 0.6, (222, 218, 26, 1.05)), (t_cura + 0.8, (238, 205, 46, 1.55)), (t_camp - 0.3, (262, 176, 66, 2.55)), (T1(E1) - 5.0, (263, 176, 68, 3.0)),
                     (t_nadie - 0.2, (264, 176, 70, 3.25))])


@shot(T0(E1), bg=bg_amanecer, post=[lambda img, t: U.gradacion(img, luces=(1.05, 1.0, 0.94), sombras=(0.96, 0.97, 1.05), contraste=1.05, saturacion=1.08)], ent=("fundido", 0.01))
def g_dolores(lz, t):
    cx, cy, cz, zm = cam_dolores(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.0, 0.95, 0.92), mix=(255, 170, 130), k=0.10 * (1 - prog(t, t_cura, t_nadie)))
    nubes(lz, t)
    DOL.suelo(lz, iso, t, isla=True)
    DOL.ang = ang_campana(t)
    m = DOL.objetos(t)
    # el cura al pie de la torre derecha, tirando de la cuerda
    px, py = 264.0, 188.0
    acc = "trabaja" if t >= t_camp else "habla"
    m.add(px - 5, py - 5, px + 5, py + 5, 40, lambda lz, iso: G.persona(lz, iso, px, py, t, "cura", dir=(0, 1), seed=21, accion=acc, h=36), fijo=False)
    m.dibujar(lz, iso)
    # cuerda de la campana
    sx0, sy0 = iso.P(264, 162, 130)
    sx1, sy1 = iso.P(px, py, 24)
    sw = math.sin(max(0.0, t - t_camp) * 6.98 + 0.4) * 5 * zm if t >= t_camp else 0.0
    P_ = np.array([[sx0, sy0], [(sx0 + sx1) / 2 + sw, (sy0 + sy1) / 2], [sx1, sy1]])
    lz.trazo(np.array(catmull_(P_)), (232, 216, 180), 2.2 * zm, afinar=False, temblor=0.0, capa=2)
    # golpes: ondas sobre el suelo, ondas de pantalla desde el campanario y pájaros
    bx, by = iso.P(264, 162, 140)
    for g in GOLPES[:5]:
        if g - 0.05 < t < g + 2.4:
            U.onda_iso(lz, iso, 264, 162, t, g, dur=2.0, r1=240, n=1, color=(255, 230, 170), periodo=0.3, ancho=2.2)
    for g in GOLPES[:3]:
        if t >= g and t < g + 1.6:
            U.ondas_sonoras(lz, float(bx), float(by), t, g, dur=1.2, r1=190 * zm / 3.0, n=1, color=(255, 238, 180), ancho=3.0, periodo=0.28, alfa=0.55)
    aves(lz, t, GOLPES[0] + 0.1, (float(bx), float(by) - 20), 9)
    aves(lz, t, GOLPES[3] + 0.1, (float(bx) + 40, float(by) - 10), 6, vel=0.9)
    bruma(lz, t, 1 - prog(t, t_cura, t_camp))
    # rótulos
    U.fecha_lugar(lz, t, t_sep - 0.1, t_nadie - 0.4, "Dolores, Guanajuato", "Septiembre de 1810")
    qx, qy = iso.P(px, py, 46)
    k = U.pop(t, t_cura + 0.1) * U.salida(t, t_nadie - 0.5)
    if k > 0.01:
        U.llamada(lz, float(qx), float(qy) - 6, "Un cura de 57 años", color=U.COL["naranja"], px=32, k=k, cola="abajo")


def catmull_(P_):
    from motor import catmull
    return catmull(P_, 8, False)


# ------------------------------------------------------------------------------------------------ 2. EL REPIQUE RECORRE EL PAÍS
def cam_mapa(t):
    return Klog(t, [(t_nadie - 0.2, (-100.93, 21.16, 9.0)), (t_rep + 0.2, (-101.0, 21.2, 3.1)), (t_once, (-101.6, 21.6, 1.55)), (T1(E1) - 0.4, (-101.5, 22.2, 1.12))])


@shot(t_nadie - 0.2, bg=lambda t: MP.base(cam_mapa(t), t), post=[lambda img, t: U.gradacion(img)], ent=("zoom", 0.9))
def g_mapa(lz, t):
    cam = cam_mapa(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=2)
    MD.montes(lz, cam)
    for txt, ll, rot in (("SIERRA MADRE OCCIDENTAL", (-106.2, 25.6), -1.15), ("SIERRA MADRE ORIENTAL", (-99.9, 24.5), -1.05), ("GOLFO DE MÉXICO", (-93.0, 24.4), 0.0),
                         ("OCÉANO PACÍFICO", (-109.2, 17.6), 0.0), ("ALTIPLANO CENTRAL", (-102.4, 23.8), 0.0)):
        MD.region(lz, cam, txt, ll, px=26, rot=rot, alfa=0.55, z_max=1.7)
    # ondas del repique desde Dolores
    for k, tt in enumerate((t_rep - 0.2, t_rep + 0.9, t_des + 0.2)):
        MD.onda(lz, cam, "dolores", t, tt, dur=3.0, r_deg=7.5, n=2, ancho=3.4, periodo=0.5, alfa=0.7)
    MD.ciudad(lz, cam, "dolores", t, t_nadie, tam=1.0 if cam[2] > 2 else 0.9, tipo="pueblo", bando="ins", llama=(t > t_rep), nombre="Dolores", px=30)
    for k, (lugar, tt, tipo) in enumerate((("queretaro", t_des, "ciudad"), ("guanajuato", t_des + 0.28, "ciudad"), ("valladolid", t_once - 0.2, "ciudad"), ("mexico", t_once + 0.2, "ciudad"),
                                           ("guadalajara", t_once + 0.5, "ciudad"), ("san_luis", t_once + 0.7, "pueblo"), ("zacatecas", t_once + 0.8, "pueblo"))):
        MD.ciudad(lz, cam, lugar, t, tt, tam=0.9, tipo=tipo, bando="ins" if lugar not in ("mexico",) else "real", llama=(lugar != "mexico" and t > tt + 0.3), semilla=k + 2)
    kk = U.pop(t, t_once - 0.1, 1.2) * U.salida(t, t_hist - 0.5, 0.3)
    if kk > 0.01:
        U.llamada(lz, W / 2, 124, "11 años de guerra", color=U.COL["rojo"], px=84, k=kk * U.repop(t, t_once + 0.5), cola=None)
    MD.brujula(lz, W - 120, H - 130, 1.0)
    MD.escala(lz, 80, H - 70, cam, km=200 if cam[2] < 2 else 50)


# ------------------------------------------------------------------------------------------------ 3. TÍTULO
def emblema(lz, x, y, s, t):
    """Águila sobre un nopal (emblema nacional), estilizada y original: nopal de palas ovaladas con tunas, águila de perfil con alas abiertas y una serpiente en el pico."""
    k = s
    br = math.sin(t * 2.2) * 2.0 * k
    # nopal
    for (dx, dy, rx, ry, a, c) in ((-30, 70, 56, 40, -0.25, (52, 150, 94)), (36, 66, 52, 38, 0.3, (60, 160, 100)), (0, 20, 54, 40, 0.0, (68, 170, 108)), (-56, 6, 40, 30, -0.5, (56, 154, 98)),
                                   (56, -6, 38, 30, 0.5, (64, 164, 104))):
        lz.relleno(elipse(x + dx * k, y + dy * k, rx * k, ry * k, a, 24), c)
        lz.relleno(elipse(x + (dx - 5) * k, y + (dy - 5) * k, rx * 0.8 * k, ry * 0.8 * k, a, 24), P.aclarar(c, 0.14))
        for j in range(5):
            lz.relleno(circulo(x + (dx + (j - 2) * rx * 0.4) * k, y + (dy + ((j % 2) - 0.5) * ry * 0.6) * k, 2.4 * k, 6), (236, 232, 206))
    for (dx, dy) in ((-70, -28), (64, -34), (-52, 44)):
        lz.relleno(circulo(x + dx * k, y + dy * k, 11 * k, 12), (214, 60, 92))
        lz.relleno(circulo(x + (dx - 3) * k, y + (dy - 3) * k, 5 * k, 8), (240, 116, 130))
    # águila (de perfil, mirando a la izquierda)
    ex, ey = x - 4 * k, y - 78 * k + br
    # cola
    for i in range(5):
        a = 0.5 + i * 0.16
        lz.relleno(np.array([[ex + 40 * k, ey + 40 * k], [ex + (84 + 8 * i) * k, ey + (50 + 18 * i - 18) * k], [ex + (74 + 8 * i) * k, ey + (64 + 18 * i - 18) * k]]), (96, 62, 40) if i % 2 else (122, 80, 50))
    # alas
    for sg, col in ((-1, (118, 76, 48)), (1, (150, 98, 60))):
        ab = math.sin(t * 2.2 + (0.5 if sg > 0 else 0)) * 5 * k
        base = np.array([[ex + 6 * k, ey - 10 * k], [ex + 66 * sg * k * 0.2 + 50 * k, ey - 40 * k + ab], [ex + 130 * k, ey - 70 * k + ab * 1.5], [ex + 128 * k, ey - 20 * k + ab],
                         [ex + 70 * k, ey + 24 * k], [ex + 18 * k, ey + 30 * k]]) if sg > 0 else np.array([[ex - 4 * k, ey - 6 * k], [ex - 30 * k, ey - 50 * k + ab], [ex - 100 * k, ey - 92 * k + ab * 1.4],
                                                                                                         [ex - 112 * k, ey - 40 * k + ab], [ex - 60 * k, ey + 8 * k], [ex - 8 * k, ey + 26 * k]])
        lz.relleno(base, col)
        for j in range(6):
            fr = j / 5
            tip = base[2] * (1 - fr) + base[3] * fr
            lz.relleno(np.array([base[(2 if fr < 0.5 else 3)] * 0 + tip, tip + np.array([sg * 8 * k, 14 * k]), tip + np.array([-sg * 6 * k, 16 * k])]), P.oscurecer(col, 0.18))
        lz.relleno(np.array([base[0], base[1], base[1] * 0.6 + base[2] * 0.4, base[5] * 0.7 + base[0] * 0.3]), P.aclarar(col, 0.18), alfa=0.6)
    # cuerpo y cabeza
    lz.relleno(elipse(ex + 4 * k, ey + 6 * k, 30 * k, 40 * k, 0.25, 24), (130, 84, 52))
    lz.relleno(elipse(ex - 2 * k, ey + 12 * k, 20 * k, 30 * k, 0.25, 24), (176, 124, 80))
    for j in range(4):
        lz.relleno(np.array([[ex - 12 * k + j * 6 * k, ey + 4 * k + j * 10 * k], [ex - 2 * k + j * 6 * k, ey + 2 * k + j * 10 * k], [ex - 6 * k + j * 6 * k, ey + 14 * k + j * 10 * k]]), (206, 156, 104), alfa=0.8)
    hx, hy = ex - 26 * k, ey - 52 * k
    lz.relleno(circulo(hx, hy, 17 * k, 18), (150, 98, 60))
    lz.relleno(circulo(hx - 3 * k, hy - 3 * k, 11 * k, 14), (190, 136, 88))
    lz.relleno(np.array([[hx - 12 * k, hy - 2 * k], [hx - 34 * k, hy + 4 * k], [hx - 14 * k, hy + 15 * k]]), (250, 196, 60))
    lz.relleno(np.array([[hx - 12 * k, hy - 2 * k], [hx - 34 * k, hy + 4 * k], [hx - 18 * k, hy + 3 * k]]), (252, 220, 110))
    lz.relleno(circulo(hx - 2 * k, hy - 5 * k, 3.4 * k, 8), (255, 255, 255))
    lz.relleno(circulo(hx - 3 * k, hy - 5 * k, 2.0 * k, 8), (40, 30, 30))
    # serpiente en el pico
    pts = [(hx - 30 * k, hy + 8 * k)] + [(hx - 30 * k - 12 * k * i + 4 * k * math.sin(i * 1.3 + t * 3), hy + 16 * k + i * 9 * k + 5 * k * math.sin(i + t * 3)) for i in range(1, 7)]
    from motor import catmull
    q = np.array(catmull(np.array(pts), 6, False))
    lz.trazo(q, (60, 180, 110), 6 * k, afinar=False, temblor=0.0)
    # garras
    lz.relleno(rect_red(ex + 2 * k, ey + 40 * k, 7 * k, 22 * k, 3 * k), (250, 196, 60))


@shot(t_hist - 0.4, bg=lambda t: bg_grad((30, 14, 84), (112, 46, 128), mid=(70, 30, 120), ym=0.5), post=[lambda img, t: U.gradacion(img, luces=(1.04, 1.0, 1.0), sombras=(0.96, 0.96, 1.08), saturacion=1.1)],
      ent=("destello", 0.8))
def g_titulo(lz, t):
    U.bokeh(lz, t, seed=4, n=16, colores=((255, 190, 90), (255, 80, 150), (140, 100, 255)), r=(40, 130), alfa=0.30)
    U.haces_luz(lz, 1390, 520, t, n=9, largo=1300, color=(255, 190, 240), alfa=0.16, ancho=0.09)
    U.chispas(lz, t, n=26, seed=3, tam=(6, 15))
    lz.halo(1390, 520, 520, (255, 150, 90), alfa=0.35, capa=0)
    k = U.pop(t, t_hist - 0.2, 1.2)
    if k > 0:
        emblema(lz, 1390, 600, 1.35 * k, t)
    P.rotulo(lz, 620, 300, "La Independencia", px=124, k=U.pop(t, t_hist, 1.2), color=(255, 255, 255))
    P.rotulo(lz, 620, 450, "de México", px=124, k=U.pop(t, t_hist + 0.4, 1.2), color=(255, 255, 255))
    kc = U.pop(t, t_compl, 1.2)
    if kc > 0:
        U.llamada(lz, 620, 650, "COMPLETA", color=U.COL["naranja"], px=104, k=kc * U.repop(t, t_compl + 0.4), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T0(E1) + 0.2, "amanecer", 0.4, dur=2.5)
for _k in range(8):
    snd(GOLPES[_k], "campana", 0.6)
snd(t_cura, "pop", 0.4)
snd(t_rep, "gong", 0.3)
snd(t_des, "whoosh", 0.3, dur=1.0)
snd(t_once, "reloj_rapido", 0.45, dur=1.0)
snd(t_guerra + 0.4, "tambor", 0.25)
snd(t_hist, "pluck", 0.5)
snd(t_compl, "bling", 0.6)
