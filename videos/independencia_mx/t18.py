# -*- coding: utf-8 -*-
"""Escena 18 · Cierre (10:21-10:50): el 16 y el 27 de septiembre, el pueblo y Porfirio Díaz con la campana, la independencia que hicieron muchos y la pregunta final al público."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq2 as B
import kz_gente_iso as G
import kz_iso_deco as DC
import kz_retrato as RT
import kz_ui as U
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_d as md
import mundos_n as mn
import t16 as T16

E18 = "cierre"
GRAD = lambda img, t: U.gradacion(img)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)
PLZ = md.PlazaMayor()

# ------------------------------------------------------------------ anclas
t_hoy, t_cel, t_16, t_sep, t_pero, t_indep, t_consu, t_27 = [T(E18, w, frase=0) for w in ("hoy", "celebramos", "dieciseis", "septiembre", "pero", "independencia", "consumo", "veintisiete")]
t_cel2, t_pueblo, t_desp, t_inst, t_pres, t_por, t_diaz, t_hizo, t_son, t_camp, t_pal, t_nac = [T(E18, w, frase=1) for w in ("celebro", "pueblo", "despues", "institucionalizo", "presidente", "porfirio", "diaz", "hizo", "sonar", "campana", "palacio", "nacional")]
t_indep2, t_solo, t_hombre, t_ni, t_bando, t_hic, t_insu, t_curas, t_arr, t_muj, t_sold, t_enem, t_mano = [T(E18, w, frase=2) for w in ("independencia", "solo", "hombre", "ni", "bando", "hicieron", "insurgentes", "curas", "arrieros", "mujeres", "soldados", "enemigos", "mano")]
t_que, t_otra, t_hist, t_mex, t_canal, t_cuent, t_com = [T(E18, w, frase=3) for w in ("que", "otra", "historia", "mexico", "canal", "cuentamelo", "comentarios")]
T_A, T_B1, T_B2, T_C1, T_C2, T_D = T0(E18), t_cel2 - 0.2, t_por - 0.2, t_indep2 - 0.15, t_hic - 0.15, t_que - 0.15


# ------------------------------------------------------------------------------------------------ 1. EL 16 Y EL 27 DE SEPTIEMBRE
def _tarjeta_fecha(lz, x, y, k, num, mes, lab, col, t):
    w, h = 620, 700
    with lz.grupo(x, y, k, 0.03 * math.sin(t * 1.3 + num)):
        lz.relleno(rect_red(-w / 2 + 14, -h / 2 + 18, w, h, 30), (20, 10, 50), alfa=0.30)
        lz.relleno(rect_red(-w / 2, -h / 2, w, h, 28), (252, 248, 238))
        lz.relleno(rect_red(-w / 2, -h / 2, w, 140, 28), col)
        lz.relleno(np.array([[-w / 2, -h / 2 + 90], [w / 2, -h / 2 + 90], [w / 2, -h / 2 + 140], [-w / 2, -h / 2 + 140]]), col)
        lz.texto(mes, 0, -h / 2 + 72, 56, "geo", color=(255, 255, 255), borde=None, temblor=0.0)
        lz.texto(str(num), 0, 20, 330, "geo", color=(60, 40, 90), borde=None, temblor=0.0)
        lz.texto(lab, 0, h / 2 - 84, 46, "geo", color=col, borde=None, temblor=0.0)


@shot(T_A, bg=lambda t: bg_grad((60, 36, 120), (170, 80, 130), mid=(110, 50, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def ci_fechas(lz, t):
    U.bokeh(lz, t, seed=141, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, W / 2, 520, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    k1 = U.pop(t, t_cel - 0.1, 1.2)
    k2 = U.pop(t, t_consu - 0.2, 1.2)
    if k1 > 0.01:
        _tarjeta_fecha(lz, 560, 560, k1, 16, "SEPTIEMBRE · 1810", "el Grito de Dolores", (226, 70, 80), t)
        for i in range(10):                                      # confeti y campana del festejo actual
            u = ((t * 0.5 + h01(321, i)) % 1.0)
            lz.relleno(circulo(300 + 520 * h01(322, i), 120 + 840 * u, 5 + 3 * h01(323, i), 6), [(255, 214, 72), (255, 120, 140), (120, 200, 255)][i % 3], alfa=0.9 * k1, capa=2)
    if k2 > 0.01:
        _tarjeta_fecha(lz, 1360, 560, k2, 27, "SEPTIEMBRE · 1821", "la consumación", (70, 170, 110), t)
        lz.trazo(np.array([[1560, 880], [1612, 932], [1722, 808]]), (70, 190, 110), 26 * min(1.0, k2), afinar=False, temblor=0.0, capa=2)
        U.chispas(lz, t, n=14, seed=142, tam=(6, 14))
    k = U.pop(t, t_hoy - 0.05) * U.salida(t, t_pero - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 120, "hoy celebramos el 16 de septiembre", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_16 + 0.1), cola=None)
    k = U.pop(t, t_pero - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 120, "pero la independencia se consumó el 27", color=U.COL["verde"], px=64, k=k * U.repop(t, t_27 + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 2a. EL PUEBLO LA CELEBRA PRIMERO (la plaza de noche)
def cam_b1(t):
    return K(t, [(T_B1, (270, 290, 30, 2.0)), (T_B2, (270, 270, 34, 2.4))])


@shot(T_B1, bg=lambda t: bg_grad((14, 16, 60), (62, 52, 120), mid=(34, 32, 96), ym=0.45), post=[lambda img, t: U.gradacion(img, luces=(1.02, 0.98, 1.02), sombras=(0.92, 0.94, 1.08), saturacion=1.05)], ent=("fundido", 0.5))
def ci_pueblo(lz, t):
    cx, cy, cz, zm = cam_b1(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.78, 0.82, 1.0), mix=(30, 34, 100), k=0.22)
    for i in range(60):
        x, y = (h01(15, i, 1) * 2000) % 1920, (h01(15, i, 2) * 560)
        lz.relleno(circulo(x, y, 1.6 + 2.0 * h01(15, i, 3), 6), (255, 244, 210), alfa=0.4 + 0.4 * math.sin(t * 2 + i), capa=0)
    PLZ.suelo(lz, iso, t, noche=0.8)
    m = PLZ.objetos(t, noche=0.8, farolas=1.0)
    for i in range(34):                                      # pueblo con faroles y banderas, vitoreando
        x, y = 130 + 280 * h01(331, i), 170 + 250 * h01(332, i)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("campesino", "campesina", "mestizo", "indigena", "indigena_f", "dama", "comerciante", "nino")[i % 8], dir=(0.0, -1.0), seed=11200 + i, h=42 if i % 8 != 7 else 30, accion="vitorea", cara="alegre")))(x, y, i), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    mn.guirnaldas(lz, iso, t, k=prog(t, T_B1, T_B1 + 2.0), postes=[(100, 140), (420, 140), (420, 430), (100, 430)], z=64)
    for j in range(4):
        T16._cohete(lz, 300 + 440 * j, 280 + 90 * (j % 2), prog(t, T_B1 + 0.4 * j, T_B1 + 2.4 + 0.4 * j) % 1.0 + 0.001, [(255, 214, 90), (110, 220, 150), (255, 120, 140), (120, 180, 255)][j])
    k = U.pop(t, t_cel2 - 0.05) * U.salida(t, t_desp - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "primero la celebró el pueblo", color=U.COL["naranja"], px=78, k=k * U.repop(t, t_pueblo + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 2b. PORFIRIO DÍAZ HACE SONAR LA CAMPANA DESDE PALACIO NACIONAL
def _campana(lz, x, y, s, ang, t):
    with lz.grupo(x, y, s, ang):
        lz.relleno(np.array([[-18, -20], [18, -20], [34, 10], [60, 60], [-60, 60], [-34, 10]]), (232, 190, 80), capa=2)
        lz.relleno(np.array([[-18, -20], [-6, -20], [-12, 10], [-34, 60], [-60, 60], [-34, 10]]), (250, 222, 130), capa=2)
        lz.relleno(rect_red(-64, 52, 128, 14, 6), (190, 150, 60), capa=2)
        lz.relleno(circulo(0, 78 + 4 * math.sin(t * 9), 14, 12), (120, 90, 50), capa=2)
        lz.relleno(rect_red(-8, -50, 16, 34, 4), (110, 80, 56), capa=2)


@shot(T_B2, bg=lambda t: bg_grad((90, 100, 190), (250, 190, 170), mid=(170, 130, 190), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def ci_campana(lz, t):
    iso = I.Iso(260, 80, 56, 3.0 + 0.04 * (t - T_B2), sx0=960, sy0=640)
    I.luz(mul=(1.02, 0.96, 0.96), mix=(255, 170, 120), k=0.08)
    PLZ.suelo(lz, iso, t)
    m = PLZ.objetos(t, noche=0.0)
    # Porfirio Díaz en el balcón central del Palacio tirando de la cuerda de la campana; el pueblo abajo con banderas
    m.add(254, 74, 266, 86, 80, lambda lz, iso: G.persona(lz, iso, 260, 84, t, "noble", dir=(0, 1), seed=11300, h=58, z=40, accion="trabaja", cara="alegre"), fijo=False, clave=345)
    for i in range(26):
        x, y = 150 + 240 * h01(341, i), 150 + 160 * h01(342, i)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("campesino", "campesina", "mestizo", "indigena", "dama", "comerciante", "nino", "indigena_f")[i % 8], dir=(0, -1), seed=11400 + i, h=42 if i % 8 != 6 else 30, accion="vitorea", cara="alegre")))(x, y, i), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    ang = 0.5 * math.sin((t - t_son) * 6.5) * math.exp(-max(0.0, t - t_son) * 0.15) if t > t_son - 0.4 else 0.0
    bx, by = iso.P(260, 66, 150)
    _campana(lz, float(bx), float(by), 1.5 * iso.z / 3.0, ang, t)
    for j in range(5):
        tg = t_son + 0.45 * j
        if tg - 0.05 < t < tg + 1.6:
            U.ondas_sonoras(lz, float(bx), float(by), t, tg, dur=1.5, r1=420, n=1, color=(255, 238, 180), ancho=4.0, periodo=0.28, alfa=0.6)
    DC.aves(lz, t, n=10, seed=151, y0=60, y1=240)
    kp = U.pop(t, t_por - 0.05)
    if kp > 0.01:
        MD.medallon(lz, 300, 470, 140, "porfirio", t, emocion="serio", k=kp * U.salida(t, T_C1 - 0.2, 0.25), seed=3)
        U.llamada(lz, 300, 640, "Porfirio Díaz", color=U.COL["morado"], px=44, k=kp * U.salida(t, T_C1 - 0.2, 0.25), cola="arriba")
    k = U.pop(t, t_desp - 0.05) * U.salida(t, t_por - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "después la institucionalizó un presidente", color=U.COL["rojo"], px=62, k=k, cola=None)
    k = U.pop(t, t_hizo - 0.05) * U.salida(t, T_C1 - 0.2, 0.2)
    if k > 0.01:
        qx, qy = iso.P(260, 66, 190)
        U.llamada(lz, float(qx) + 360, float(qy), "la campana, desde Palacio Nacional", color=U.COL["naranja"], px=48, k=k * U.repop(t, t_pal + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3a. NI UN SOLO HOMBRE, NI UN SOLO BANDO
@shot(T_C1, bg=lambda t: bg_grad((110, 150, 230), (252, 226, 200), mid=(196, 190, 236), ym=0.55), post=[GRAD], ent=("fundido", 0.4))
def ci_no_uno(lz, t):
    k = U.pop(t, T_C1 + 0.15, 1.2)
    if k > 0.01:                                             # un solo hombre, tachado
        x, y = 560, 700
        lz.relleno(rect_red(x - 90 * k, y - 120 * k, 180 * k, 300 * k, 60), (80, 70, 120), capa=2)
        lz.relleno(circulo(x, y - 190 * k, 70 * k, 24), (80, 70, 120), capa=2)
        u = prog(t, t_hombre - 0.1, t_hombre + 0.4)
        if u > 0:
            lz.trazo(np.array([[x - 220, y - 300], [x - 220 + 440 * u, y - 300 + 640 * u]]), (226, 40, 60), 26, afinar=False, temblor=0.0, capa=2)
            lz.trazo(np.array([[x + 220, y - 300], [x + 220 - 440 * u, y - 300 + 640 * u]]), (226, 40, 60), 26, afinar=False, temblor=0.0, capa=2)
    kb = U.pop(t, t_ni - 0.1, 1.2)
    if kb > 0.01:                                            # un solo bando: dos banderas, una tachada
        for (x, col) in ((1250, (214, 52, 66)), (1560, (60, 150, 110))):
            lz.trazo(np.array([[x, 960], [x, 440]]), (130, 96, 70), 9, afinar=False, temblor=0.0, capa=2)
            pts = [(x + k_ * 11, 440 + 8 * math.sin(t * 5 - k_ * 0.5) + 0.3 * k_) for k_ in range(0, 21)]
            pts += [(x + k_ * 11, 440 + 150 * kb + 8 * math.sin(t * 5 - k_ * 0.5) + 0.3 * k_) for k_ in range(20, -1, -1)]
            lz.relleno(np.array(pts), col, capa=2)
        u = prog(t, t_bando - 0.1, t_bando + 0.4)
        if u > 0:
            lz.trazo(np.array([[1150, 420], [1150 + 520 * u, 420 + 580 * u]]), (226, 40, 60), 26, afinar=False, temblor=0.0, capa=2)
    k = U.pop(t, t_indep2 - 0.05) * U.salida(t, t_hombre - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la independencia no la hizo…", color=U.COL["morado"], px=76, k=k, cola=None)
    k = U.pop(t, t_hombre - 0.05) * U.salida(t, t_ni - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un solo hombre", color=U.COL["rojo"], px=96, k=k * U.repop(t, t_hombre + 0.1), cola=None)
    k = U.pop(t, t_ni - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "ni un solo bando", color=U.COL["rojo"], px=96, k=k * U.repop(t, t_bando + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3b. LA HICIERON MUCHOS
@shot(T_C2, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def ci_muchos(lz, t):
    U.bokeh(lz, t, seed=143, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.chispas(lz, t, n=18, seed=144, tam=(5, 12))
    ocultar = U.salida(t, t_enem - 0.15, 0.3)
    grupos = ((("campesino",), "insurgentes", t_insu, U.COL["verde"]), (("hidalgo", "morelos"), "curas", t_curas, U.COL["morado"]), (("guerrero",), "arrieros", t_arr, U.COL["naranja"]), (("josefa", "leona"), "mujeres", t_muj, U.COL["rojo"]), (("allende", "aldama"), "soldados", t_sold, U.COL["azul"]))
    for i, (qs, lab, tt_, col) in enumerate(grupos):
        x = 200 + 380 * i
        k = U.pop(t, tt_ - 0.1, 1.2) * ocultar
        if k > 0.01:
            for j, q in enumerate(qs):
                dx = (j - (len(qs) - 1) / 2) * 190
                RT.retrato(lz, x + dx, 700, 62 * (0.94 + 0.06 * k), q, t, emocion="neutro", mirar=0.0, seed=i * 5 + j, alfa=min(1.0, k))
            U.llamada(lz, x, 240, lab, color=col, px=44, k=k * U.repop(t, tt_ + 0.2), cola=None)
    # enemigos que se dan la mano: Iturbide y Guerrero con un apretón gigante en el centro
    ke = U.pop(t, t_enem - 0.15, 1.3)
    if ke > 0.01:
        RT.retrato(lz, 460, 960, 150 * (0.94 + 0.06 * ke), "iturbide", t, emocion="neutro", mirar=0.4, seed=7, alfa=min(1.0, ke))
        RT.retrato(lz, 1460, 960, 150 * (0.94 + 0.06 * ke), "guerrero", t, emocion="neutro", mirar=-0.4, seed=8, alfa=min(1.0, ke))
        u = e_out(prog(t, t_enem, t_mano + 0.3))
        for sg in (-1, 1):                                    # dos brazos que se encuentran
            x0 = 700 if sg < 0 else 1220
            xm = 960 + sg * 30 * (1 - u)
            lz.relleno(rect_red(min(x0, xm) - 20, 600 - 28, abs(xm - x0) + 40, 56, 26), (232, 186, 150) if sg < 0 else (176, 120, 88), capa=2)
        lz.relleno(circulo(960, 600, 46 * u, 20), (250, 214, 150), capa=2)
        lz.halo(960, 600, 260 * u, (255, 230, 150), alfa=0.35 * u, capa=2)
        U.llamada(lz, W / 2, 240, "enemigos que se dieron la mano", color=U.COL["naranja"], px=62, k=ke * U.repop(t, t_mano + 0.1), cola=None)
    k = U.pop(t, t_hic - 0.05) * ocultar
    if k > 0.01:
        U.llamada(lz, W / 2, 110, "la hicieron…", color=U.COL["morado"], px=70, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 4. LA PREGUNTA FINAL
@shot(T_D, bg=lambda t: bg_grad((40, 22, 96), (120, 52, 130), mid=(74, 34, 116), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def ci_pregunta(lz, t):
    U.bokeh(lz, t, seed=145, n=18, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.28)
    U.haces_luz(lz, W / 2, 540, t, n=10, largo=1400, color=(255, 214, 240), alfa=0.12, ancho=0.08)
    U.chispas(lz, t, n=26, seed=146, tam=(6, 15))
    k = U.pop(t, t_que - 0.1, 1.3)
    if k > 0.01:
        P.rotulo(lz, W / 2, 300, "¿Qué otra historia", px=int(130 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
        P.rotulo(lz, W / 2, 450, "de México", px=int(130 * (0.94 + 0.06 * k)), k=U.pop(t, t_mex - 0.2, 1.2), color=(255, 255, 255))
    kc = U.pop(t, t_canal - 0.2, 1.2)
    if kc > 0.01:
        U.llamada(lz, W / 2, 610, "quieres ver en el canal", color=U.COL["naranja"], px=70, k=kc * U.repop(t, t_canal + 0.2), cola=None)
    kb = U.pop(t, t_cuent - 0.1, 1.3)
    if kb > 0.01:                                            # burbujas de comentarios que suben
        for i in range(5):
            u = ((t - t_cuent) * 0.35 + i * 0.2) % 1.0
            x = (200, 430, 1490, 1720, 330)[i] + 30 * math.sin(t * 2 + i)
            y = 1000 - 440 * u
            a = 1.0 - max(0.0, u - 0.7) / 0.3
            lz.relleno(rect_red(x - 90, y - 50, 180, 100, 40), (255, 255, 255), alfa=0.9 * a * kb, capa=2)
            lz.relleno(np.array([[x - 24, y + 48], [x - 50, y + 90], [x + 6, y + 50]]), (255, 255, 255), alfa=0.9 * a * kb, capa=2)
            for j in range(3):
                lz.relleno(circulo(x - 40 + 40 * j, y, 9, 8), [(226, 70, 80), (250, 206, 70), (70, 190, 110)][j], alfa=a * kb, capa=2)
        U.llamada(lz, W / 2, 800, "cuéntamelo en los comentarios", color=U.COL["verde"], px=76, k=kb * U.repop(t, t_com + 0.1), cola=None)
    kt = U.pop(t, t_com + 0.2)
    if kt > 0.01:
        P.rotulo(lz, W / 2, 1000, "Bitácora Perdida", px=int(80 * kt), k=1.0, color=(255, 214, 72), alfa=min(1.0, kt))


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "bling", 0.4)
snd(t_cel, "campana", 0.5)
snd(t_consu, "gong", 0.5)
snd(T_B1, "tambor", 0.4)
for _j in range(4):
    snd(T_B1 + 0.4 * _j, "explosion", 0.35)
snd(T_B2, "whoosh", 0.3, dur=0.9)
for _j in range(6):
    snd(t_son + 0.45 * _j, "campana", 0.5)
snd(T_C1, "pop", 0.3)
snd(t_hombre, "crujido", 0.5)
snd(t_bando, "crujido", 0.5)
snd(T_C2, "bling", 0.4)
for _t in (t_insu, t_curas, t_arr, t_muj, t_sold):
    snd(_t, "pop", 0.3)
snd(t_mano, "bling", 0.6)
snd(T_D, "pluck", 0.4)
snd(t_com, "bling", 0.5)
