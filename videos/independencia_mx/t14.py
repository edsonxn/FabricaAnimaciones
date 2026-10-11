# -*- coding: utf-8 -*-
"""Escena 14 · El giro de 1820 (8:06-8:39): la revolución liberal en España, el rey obligado a aceptar la constitución, el recorte de poderes a la Iglesia y al ejército, el susto de los conservadores novohispanos (La Profesa) y su independencia «a su manera»."""
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
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_e as me

E14 = "giro"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)

# ------------------------------------------------------------------ anclas
t_nuevo, t_acon, t_esp, t_cambio, t_todo = [T(E14, w, frase=0) for w in ("nuevo", "acontecimiento", "espana", "cambio", "todo")]
t_1820, t_golpe, t_mil, t_oblig, t_rey, t_acept, t_const, t_lib = [T(E14, w, frase=1) for w in ("veinte", "golpe", "militar", "obligo", "rey", "aceptar", "constitucion", "liberal")]
t_esa, t_recort, t_pod, t_igl, t_ejer = [T(E14, w, frase=2) for w in ("esa", "recortaba", "poderes", "iglesia", "ejercito")]
t_nesp, t_obis, t_ricos, t_ofic, t_cons, t_asust = [T(E14, w, frase=3) for w in ("nueva", "obispos", "ricos", "oficiales", "conservadores", "asustaron")]
t_hicie, t_incre, t_def, t_rey2, t_pens, t_mejor, t_sep, t_esp2 = [T(E14, w, frase=4) for w in ("hicieron", "increible", "defensores", "rey", "pensar", "mejor", "separarse", "espana")]
t_quer, t_indep, t_manera, t_prot, t_priv = [T(E14, w, frase=5) for w in ("querian", "independencia", "manera", "protegiera", "privilegios")]
T_A, T_B, T_C, T_D, T_E, T_F = T0(E14), t_1820 - 0.2, t_esa - 0.15, t_nesp - 0.15, t_hicie - 0.15, t_quer - 0.15


# ------------------------------------------------------------------------------------------------ 1. «DE NUEVO, ALGO EN ESPAÑA» (mapa del Atlántico)
def cam_a(t):
    return Klog(t, [(T_A, (-52.0, 29.0, 0.17)), (T_B, (-52.0, 29.0, 0.19))])


@shot(T_A, bg=lambda t: MP.base(cam_a(t), t, exag=8.0, rios_umbral=3.0), post=[GRAD], ent=("fundido", 0.5))
def gi_espana(lz, t):
    cam = cam_a(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=19)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.30, borde=(255, 220, 90), ancho=5.0, t=t, latido=0.0)
    MD.pais(lz, cam, "Spain", (255, 210, 70), alfa=0.36, borde=(255, 236, 130), ancho=4.0)
    sx, sy = MP.proy(cam, -3.7, 40.2)
    mx, my = MP.proy(cam, -99.1, 19.4)
    U.llamada(lz, float(mx), float(my) + 90, "NUEVA ESPAÑA", color=U.COL["naranja"], px=40, k=U.pop(t, T_A + 0.3), cola=None)
    # algo ocurre en España: nubes de tormenta, un «!» enorme y ondas que viajan por el océano hasta la Nueva España
    kk = U.pop(t, t_acon - 0.2)
    if kk > 0.01:
        for j, (dx, dy, s) in enumerate(((-120, -90, 1.5), (60, -120, 1.9), (170, -70, 1.4))):
            O2.nube_tormenta(lz, float(sx) + dx, float(sy) + dy, s * kk, t + j * 1.2, relampago=max(0.0, 1.0 - ((t - t_acon + 0.2 * j) % 1.8) * 5))
        U.llamada(lz, float(sx), float(sy) - 60, "!", color=U.COL["rojo"], px=130, k=kk * U.repop(t, t_esp + 0.3), cola="abajo")
    if t > t_cambio - 0.3:
        U.ondas_sonoras(lz, float(sx), float(sy), t, t_cambio - 0.3, dur=3.4, r1=float(abs(mx - sx)) * 1.05, n=3, color=(255, 236, 170), ancho=5.0, periodo=0.4, alfa=0.7, capa=2)
    bx = float(sx) + (float(mx) - float(sx)) * e_inout(prog(t, t_acon, t_todo + 0.6))
    by = float(sy) + (float(my) - float(sy)) * e_inout(prog(t, t_acon, t_todo + 0.6)) - 30
    if t > t_acon:
        MD.barco_plano(lz, bx, by, 1.4, t, dir=-1)
    k = U.pop(t, T_A + 0.1) * U.salida(t, t_acon - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "y entonces, de nuevo…", color=U.COL["azul"], px=84, k=k, cola=None)
    k = U.pop(t, t_acon - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un acontecimiento en España lo cambió todo", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_cambio + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. EL REY OBLIGADO A ACEPTAR LA CONSTITUCIÓN (2D)
@shot(T_B, bg=PURP, post=[GRAD], ent=("fundido", 0.5))
def gi_rey(lz, t):
    U.bokeh(lz, t, seed=91, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, 560, 560, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    kv = U.pop(t, T_B + 0.05, 1.3)
    miedo = prog(t, t_oblig - 0.2, t_oblig + 0.5)
    RT.retrato(lz, 520, 1010, 245 * (0.94 + 0.06 * kv), "fernando", t, emocion="miedo" if miedo > 0.5 else "serio", habla=0.0, mirar=-0.4, seed=7, alfa=min(1.0, kv))
    # los militares sublevados: una hilera de fusiles con bayoneta que sube detrás del rey
    ks = e_out(prog(t, t_golpe - 0.1, t_oblig + 0.4))
    for i in range(12):
        x = 900 + 80 * i
        alto = 700 * ks * (0.7 + 0.3 * h01(251, i))
        lz.trazo(np.array([[x, 1100], [x, 1100 - alto]]), (90, 70, 60), 10, afinar=False, temblor=0.0, capa=2)
        lz.relleno(np.array([[x - 8, 1100 - alto], [x, 1100 - alto - 70], [x + 8, 1100 - alto]]), (226, 230, 240), capa=2)
        lz.relleno(rect_red(x - 30, 1100 - 200 * ks, 60, 200 * ks, 14), (44, 52, 100), capa=2)
        lz.relleno(circulo(x, 1100 - 214 * ks, 24, 14), (200, 160, 130), capa=2)
    kp = U.pop(t, t_const - 0.2)
    if kp > 0.01:
        U.pergamino_grande(lz, 1330, 420, 640, 440, t, t_const - 0.2, lineas=("Constitución", "de la monarquía", "española"), titulo="CONSTITUCIÓN LIBERAL", sello=True, rot=0.04)
    k = U.pop(t, t_1820 - 0.05) * U.salida(t, t_oblig - 0.2, 0.2)
    if k > 0.01:
        P.rotulo(lz, 1000, 150, "1820", px=int(190 * (0.9 + 0.1 * k)), k=k, color=(255, 214, 72))
        U.llamada(lz, 1500, 150, "un golpe militar", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_golpe + 0.2), cola=None)
    k = U.pop(t, t_oblig - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 150, "obliga al rey a aceptar…", color=U.COL["naranja"], px=64, k=k * U.repop(t, t_acept + 0.1), cola=None)
    U.llamada(lz, 520, 190, "Fernando VII", color=U.COL["rojo"], px=44, k=kv, cola=None)


# ------------------------------------------------------------------------------------------------ 3. RECORTA PODERES A LA IGLESIA Y AL EJÉRCITO (2D)
def _tijeras(lz, x, y, s, abre):
    a = 0.08 + 0.42 * abre
    for sg in (-1, 1):
        with lz.grupo(x, y, s, sg * a):
            lz.relleno(np.array([[0, -6], [200, -4 * sg * 0 - 4], [200, 2], [0, 8]]) * np.array([1, 1]) + np.array([0, 0]), (210, 216, 232), capa=2)
            lz.trazo(np.array([[-10, 0], [-120, 40 * sg], [-150, 20 * sg]]), (220, 80, 80), 16, afinar=False, temblor=0.0, capa=2)
            lz.trazo(circulo(-150, 20 * sg + 14 * sg, 30, 20), (220, 80, 80), 12, cerrado=True, afinar=False, temblor=0.0, capa=2)
    lz.relleno(circulo(x, y, 14 * s, 12), (120, 126, 146), capa=2)


@shot(T_C, bg=lambda t: bg_grad((110, 150, 230), (252, 226, 200), mid=(196, 190, 236), ym=0.55), post=[GRAD], ent=("fundido", 0.4))
def gi_recortes(lz, t):
    # dos barras de poder (Iglesia, Ejército) que unas tijeras recortan
    for (nom, y, col, tt_, ic) in (("Iglesia", 380, (236, 196, 90), t_igl, "c"), ("Ejército", 700, (206, 90, 90), t_ejer, "e")):
        k = U.pop(t, T_C + 0.05 if tt_ == t_igl else t_ejer - 0.4, 1.2)
        if k <= 0.01:
            continue
        corte = e_out(prog(t, t_pod - 0.1 if tt_ == t_igl else t_ejer - 0.05, (t_pod if tt_ == t_igl else t_ejer) + 0.8))
        w = 1000 - 560 * corte
        lz.relleno(rect_red(360, y - 70, w * k, 140, 28), col, capa=2)
        lz.relleno(rect_red(360, y - 70, w * k, 36, 18), (255, 255, 255), alfa=0.18, capa=2)
        # icono: iglesia (cruz y torre) o fusil/sable
        if ic == "c":
            lz.relleno(rect_red(190, y - 20, 120, 100, 6), (250, 232, 190), capa=2)
            lz.relleno(np.array([[176, y - 20], [324, y - 20], [250, y - 100]]), (190, 90, 70), capa=2)
            lz.trazo(np.array([[250, y - 100], [250, y - 150]]), (250, 206, 70), 8, afinar=False, temblor=0.0, capa=2)
            lz.trazo(np.array([[226, y - 130], [274, y - 130]]), (250, 206, 70), 8, afinar=False, temblor=0.0, capa=2)
        else:
            lz.trazo(np.array([[160, y + 70], [300, y - 70]]), (226, 230, 240), 14, afinar=False, temblor=0.0, capa=2)
            lz.trazo(np.array([[300, y + 70], [160, y - 70]]), (226, 230, 240), 14, afinar=False, temblor=0.0, capa=2)
        P.rotulo(lz, 360 + 20, y, f"poder de la {nom}" if ic == "c" else f"poder del {nom}", px=46, k=k, color=(60, 40, 90), sombra=0.0, ancla=(0.0, 0.5))
        if corte > 0.02:
            _tijeras(lz, 360 + w + 90, y, 1.0, 0.5 + 0.5 * math.sin(t * 9))
    k = U.pop(t, t_esa - 0.05) * U.salida(t, t_recort - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "esa constitución…", color=U.COL["morado"], px=86, k=k, cola=None)
    k = U.pop(t, t_recort - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "recortaba poderes", color=U.COL["rojo"], px=92, k=k * U.repop(t, t_pod + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 4. LA PROFESA: SE ASUSTAN LOS CONSERVADORES (interior)
def _salon_profesa(lz, iso, t, W_=320, D_=250, H_=140):
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(120, 86, 76), pared_a=(166, 64, 82), pared_b=(150, 52, 74), friso=(250, 206, 90))
    for i in range(int(W_ / 40)):
        for j in range(int(D_ / 40)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 10 + i * 40, 10 + j * 40, 40, 40, (96, 66, 62), z=0.1, alfa=0.55)
    N.ventana_vista(lz, iso, c, "yi", 120, 200, 40, 120, t=t, cielo=(40, 36, 100), marco=(250, 206, 90), cortinas=(250, 206, 90), vista="ciudad")
    # gran crucifijo y retratos de obispos
    I.cara_rect(lz, iso, c, "xi", 100, 108, 40, 128, (250, 206, 90))
    I.cara_rect(lz, iso, c, "xi", 84, 124, 100, 108, (250, 206, 90))
    N.escudo(lz, iso, c, "yi", 40, 70, 1.2, "iglesia")
    N.cuadro_retrato(lz, iso, c, "yi", 230, 270, 40, 44, fondo=(60, 50, 90))
    I.cara_arco(lz, iso, c, "xi", 170, 224, 0, 100, (60, 36, 40))
    return c


@shot(T_D, bg=lambda t: bg_grad((40, 24, 80), (110, 40, 90), mid=(70, 30, 86), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gi_profesa(lz, t):
    I.luz(mul=(1.0, 0.94, 0.94), mix=(255, 150, 110), k=0.08)
    U.bokeh(lz, t, seed=92, n=10, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.18)
    iso = I.Iso(160, 125, 44, 3.8 + 0.05 * (t - T_D), sx0=940, sy0=650)
    _salon_profesa(lz, iso, t)
    m = I.Mundo()
    m.add(80, 80, 240, 130, 24, lambda lz, iso: (B.mesa(lz, iso, 80, 80, 160, 50, 22, color=(90, 60, 56), mantel=(206, 160, 70)), B.candelabro(lz, iso, 130, 100, 22, t, n=3), B.candelabro(lz, iso, 190, 100, 22, t + 0.5, n=3)), clave=300)
    grupos = (("cura", 90, 66, "obispos", t_obis), ("cura", 150, 66, "obispos", t_obis), ("noble", 210, 66, "ricos", t_ricos), ("peninsular", 100, 150, "ricos", t_ricos), ("oficial", 170, 150, "oficiales", t_ofic), ("dragon", 230, 150, "oficiales", t_ofic), ("regidor", 40, 110, "ricos", t_ricos), ("granadero", 270, 110, "oficiales", t_ofic))
    for i, (tp, x, y, g, tt_) in enumerate(grupos):
        asus = t > t_asust - 0.1
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, i, asus: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(0, 1) if y < 100 else (0, -1), seed=10600 + i, h=56, cara="miedo" if asus else "serio", accion="saluda" if (asus and i % 2 == 0) else None)))(x, y, tp, i, asus), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    N.araña(lz, iso, 160, 110, 128, t, velas=5, s=1.2)
    if t > t_asust - 0.1:
        for i, (tp, x, y, g, tt_) in enumerate(grupos):
            qx, qy = iso.P(x, y, 74)
            kk = U.pop(t, t_asust - 0.1 + 0.08 * i)
            if kk > 0.01:
                U.llamada(lz, float(qx), float(qy) - 6, "¡!", color=U.COL["rojo"], px=42, k=kk, cola="abajo")
    U.fecha_lugar(lz, t, T_D, T_E - 0.3, "Ciudad de México", "La Profesa, 1820", y=70)
    for (txt, col, tt_, dx) in (("obispos", U.COL["morado"], t_obis, -420), ("ricos", U.COL["naranja"], t_ricos, 0), ("oficiales conservadores", U.COL["azul"], t_ofic, 420)):
        k = U.pop(t, tt_ - 0.1) * U.salida(t, t_asust - 0.2, 0.2)
        if k > 0.01:
            U.llamada(lz, W / 2 + dx, 130, txt, color=col, px=52 if dx else 60, k=k * U.repop(t, tt_ + 0.2), cola=None)
    k = U.pop(t, t_asust - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡se asustaron!", color=U.COL["rojo"], px=100, k=k * U.repop(t, t_asust + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 5. SEPARARSE DE ESPAÑA (2D)
def _bandera(lz, x, y, t, col, alto=200, escudo=None, lado=1):
    lz.trazo(np.array([[x, y], [x, y - alto - 80]]), (130, 96, 70), 8, afinar=False, temblor=0.0, capa=2)
    pts = [(x + lado * k * 12, y - alto - 80 + 7 * math.sin(t * 5 - k * 0.5) + 0.3 * k) for k in range(0, 21)]
    pts += [(x + lado * k * 12, y - alto - 80 + 160 + 7 * math.sin(t * 5 - k * 0.5) + 0.3 * k) for k in range(20, -1, -1)]
    lz.relleno(np.array(pts), col, capa=2)


@shot(T_E, bg=PURP, post=[GRAD], ent=("fundido", 0.5))
def gi_separarse(lz, t):
    U.bokeh(lz, t, seed=93, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    # los defensores del rey piensan: burbujas con retratos y la idea de separarse
    for (q, x, tt_) in (("garibay", 380, t_def), ("yermo", 960, t_def + 0.25), ("calleja", 1540, t_def + 0.5)):
        k = U.pop(t, tt_ - 0.05, 1.2)
        if k > 0.01:
            RT.retrato(lz, x, 1010, 130 * (0.94 + 0.06 * k), q, t, emocion="pensativo", mirar=0.3, seed=11, alfa=min(1.0, k))
    sep = e_out(prog(t, t_sep - 0.1, t_sep + 0.9))
    cxm = W / 2
    # bandera de España a la izquierda y de México a la derecha, unidas por una soga que se corta
    gap = 130 + 330 * sep
    _bandera(lz, cxm - gap, 600, t, (214, 52, 66), alto=260, lado=1)
    _bandera(lz, cxm + gap, 600, t, (60, 150, 110), alto=260, lado=-1)
    if sep < 0.05:
        lz.trazo(np.array([[cxm - gap, 470], [cxm, 540 + 20 * math.sin(t * 3)], [cxm + gap, 470]]), (240, 220, 160), 12, afinar=False, temblor=0.0, capa=2)
        if t > t_mejor:
            _tijeras(lz, cxm + 40 * math.sin(t * 6), 540, 0.9, 0.5 + 0.5 * math.sin(t * 10))
    else:
        for sg in (-1, 1):
            lz.trazo(np.array([[cxm + sg * gap, 470], [cxm + sg * (gap - 140 * (1 - sep)), 470 + 80 * sep]]), (240, 220, 160), 10, afinar=False, temblor=0.0, capa=2)
        U.chispas(lz, t, n=18, seed=94, tam=(6, 14))
    k = U.pop(t, t_hicie - 0.05) * U.salida(t, t_def - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "y hicieron algo increíble…", color=U.COL["naranja"], px=76, k=k * U.repop(t, t_incre + 0.1), cola=None)
    k = U.pop(t, t_def - 0.05) * U.salida(t, t_sep - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los defensores del rey piensan…", color=U.COL["rojo"], px=70, k=k, cola=None)
    k = U.pop(t, t_sep - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…separarse de España", color=U.COL["verde"], px=86, k=k * U.repop(t, t_esp2 + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 6. UNA INDEPENDENCIA «A SU MANERA»
@shot(T_F, bg=lambda t: bg_grad((110, 150, 230), (252, 226, 200), mid=(196, 190, 236), ym=0.55), post=[GRAD], ent=("fundido", 0.4))
def gi_manera(lz, t):
    U.chispas(lz, t, n=14, seed=95, tam=(5, 12))
    k = U.pop(t, t_indep - 0.1, 1.3)
    if k > 0.01:
        P.rotulo(lz, W / 2, 300, "INDEPENDENCIA", px=int(190 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
    # asterisco y letra chica: «*que proteja nuestros privilegios»
    ka = U.pop(t, t_manera - 0.1)
    if ka > 0.01:
        P.rotulo(lz, W / 2 + 640, 250, "*", px=int(180 * ka), k=1.0, color=(255, 214, 72))
        lz.texto("*a nuestra manera", W / 2 + 140, 460, 44, "geo_n", color=(60, 40, 90), borde=None, alfa=min(1.0, ka), temblor=0.0)
    kp = U.pop(t, t_prot - 0.1, 1.2)
    if kp > 0.01:
        # escudo que protege cofre (privilegios), mitra (Iglesia) y espada (ejército)
        cx, cy = W / 2, 760
        lz.relleno(np.array([[cx - 330, cy - 160], [cx + 330, cy - 160], [cx + 300, cy + 130], [cx, cy + 260], [cx - 300, cy + 130]]) * np.array([1, 1]) * 1.0 if False else np.array([[cx - 330 * kp, cy - 160], [cx + 330 * kp, cy - 160], [cx + 300 * kp, cy + 130], [cx, cy + 260 * kp + 0 * 130], [cx - 300 * kp, cy + 130]]), (80, 110, 200), capa=2)
        lz.relleno(np.array([[cx - 290 * kp, cy - 130], [cx + 290 * kp, cy - 130], [cx + 262 * kp, cy + 112], [cx, cy + 226 * kp], [cx - 262 * kp, cy + 112]]), (110, 140, 230), capa=2)
        # cofre de privilegios con monedas
        lz.relleno(rect_red(cx - 90, cy - 20, 180, 110, 14), (170, 110, 70), alfa=min(1.0, kp), capa=2)
        lz.relleno(rect_red(cx - 90, cy - 20, 180, 44, 14), (200, 140, 90), alfa=min(1.0, kp), capa=2)
        lz.relleno(circulo(cx, cy + 30, 16, 12), (250, 206, 70), alfa=min(1.0, kp), capa=2)
        for j in range(5):
            lz.relleno(circulo(cx - 60 + 30 * j, cy - 30 - 8 * (j % 2), 12, 12), (250, 206, 70), alfa=min(1.0, kp), capa=2)
        # iglesia y espada a los lados
        lz.relleno(rect_red(cx - 250, cy + 10, 90, 70, 6), (250, 232, 190), alfa=min(1.0, kp), capa=2)
        lz.relleno(np.array([[cx - 262, cy + 10], [cx - 148, cy + 10], [cx - 205, cy - 50]]), (190, 90, 70), alfa=min(1.0, kp), capa=2)
        lz.trazo(np.array([[cx + 160, cy + 90], [cx + 250, cy - 40]]), (226, 230, 240), 12, afinar=False, temblor=0.0, capa=2)
        lz.trazo(np.array([[cx + 190, cy + 20], [cx + 230, cy + 40]]), (250, 206, 70), 10, afinar=False, temblor=0.0, capa=2)
    k = U.pop(t, t_quer - 0.05) * U.salida(t, t_manera - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "querían una independencia…", color=U.COL["morado"], px=76, k=k, cola=None)
    k = U.pop(t, t_manera - 0.05) * U.salida(t, t_prot - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…a su manera", color=U.COL["naranja"], px=100, k=k * U.repop(t, t_manera + 0.1), cola=None)
    k = U.pop(t, t_prot - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "que protegiera sus privilegios", color=U.COL["rojo"], px=74, k=k * U.repop(t, t_priv + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_acon, "trueno", 0.5)
snd(t_cambio, "gong", 0.4)
snd(T_B, "pop", 0.3)
snd(t_golpe, "tambor", 0.5)
snd(t_oblig, "gong", 0.5)
snd(t_const, "bling", 0.4)
snd(T_C, "pop", 0.3)
snd(t_recort, "crujido", 0.5)
snd(t_ejer, "crujido", 0.5)
snd(T_D, "pluck", 0.4)
snd(t_asust, "gong", 0.5)
snd(T_E, "pop", 0.3)
snd(t_sep, "crujido", 0.6)
snd(T_F, "bling", 0.4)
snd(t_manera, "pluck", 0.4)
snd(t_prot, "bonk", 0.5)
