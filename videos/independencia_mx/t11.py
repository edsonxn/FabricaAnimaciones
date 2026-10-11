# -*- coding: utf-8 -*-
"""Escena 11 · El Congreso de Chilpancingo (6:17-6:49): el primer congreso, la independencia sin importar España, los Sentimientos de la Nación (soberanía, fin de la esclavitud, fin de las castas), todos americanos y la Constitución de Apatzingán."""
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
import mundos_h as mh
import mundos_l as ml

E11 = "congreso"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)

# ------------------------------------------------------------------ anclas
t_1813, t_mor, t_reu, t_chil, t_prim, t_cong, t_hist = [T(E11, w, frase=0) for w in ("trece", "morelos", "reunio", "chilpancingo", "primer", "congreso", "historia")]
t_decl, t_pais, t_ind, t_imp, t_esp = [T(E11, w, frase=1) for w in ("declaro", "pais", "independiente", "importar", "espana")]
t_pres, t_doc, t_estudia, t_sent, t_nac = [T(E11, w, frase=2) for w in ("presento", "documento", "estudia", "sentimientos", "nacion")]
t_ahi, t_sob, t_pue, t_escl, t_abol, t_siempre, t_desap, t_castas = [T(E11, w, frase=3) for w in ("ahi", "soberania", "pueblo", "esclavitud", "abolirse", "siempre", "desaparecen", "castas")]
t_todos, t_hab, t_amer, t_color, t_piel = [T(E11, w, frase=4) for w in ("todos", "habitantes", "americanos", "color", "piel")]
t_ano, t_pub, t_const, t_apat, t_primera, t_mex, t_indep = [T(E11, w, frase=5) for w in ("ano", "publico", "constitucion", "apatzingan", "primera", "mexico", "independiente")]
T_A, T_A2, T_B, T_C, T_D1, T_D2, T_D3, T_E, T_F, T_F2 = T0(E11), t_reu + 0.1, t_decl - 0.2, t_pres - 0.2, t_ahi - 0.15, t_escl - 0.2, t_desap - 0.25, t_todos - 0.15, t_ano - 0.15, t_const + 0.4


# ------------------------------------------------------------------------------------------------ 1. CHILPANCINGO (mapa) Y EL SALÓN DEL CONGRESO
def cam_a(t):
    return Klog(t, [(T_A, (-99.2, 17.9, 1.8)), (T_A2, (-99.5, 17.55, 3.2))])


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[GRAD], ent=("fundido", 0.5))
def co_mapa(lz, t):
    cam = cam_a(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("acapulco", "puerto", "Acapulco", 130, 4, "izq"), ("cuautla", "pueblo", "Cuautla", 110, 4, "izq"), ("oaxaca", "ciudad", "Oaxaca", 120, 4, "izq"))):
        MD.ciudad(lz, cam, lug, t, T_A + 0.1 * j, tam=1.2, tipo=tp, bando="ins", semilla=j + 101)
        MD.etiqueta(lz, cam, lug, nm, t, T_A + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    MD.ciudad(lz, cam, "chilpancingo", t, t_mor, tam=2.6, tipo="ciudad", bando=(255, 206, 70), semilla=7, llama=False)
    MD.onda(lz, cam, "chilpancingo", t, t_chil, dur=2.2, r_deg=0.6, color=(255, 236, 170), n=3, ancho=5.0)
    k = U.pop(t, t_1813 - 0.05) * U.salida(t, t_reu - 0.1, 0.25)
    if k > 0.01:
        P.rotulo(lz, 330, 200, "1813", px=int(200 * (0.9 + 0.1 * k)), k=k, color=(255, 214, 72))
    k = U.pop(t, t_mor - 0.05)
    if k > 0.01:
        MD.medallon(lz, 1600, 440, 140, "morelos", t, emocion="serio", k=k, seed=3)
        U.llamada(lz, 1600, 610, "Morelos", color=U.COL["azul"], px=44, k=k, cola="arriba")
        sx, sy = MP.proy(cam, -99.5, 17.55)
        U.llamada(lz, float(sx), float(sy) - 130, "Chilpancingo", color=U.COL["morado"], px=62, k=k * U.repop(t, t_chil + 0.1), cola="abajo")
    MD.brujula(lz, W - 110, H - 120, 1.0)


def cam_s(t):
    return K(t, [(T_A2, (150, 130, 44, 3.0)), (t_prim, (150, 90, 44, 3.5)), (T_B, (150, 80, 44, 3.6))])


@shot(T_A2, bg=PURP, post=[GRAD], ent=("zoom", 0.5))
def co_salon(lz, t):
    cx, cy, cz, zm = cam_s(t)
    I.luz(mul=(1.0, 0.97, 0.94), mix=(255, 190, 120), k=0.05)
    U.bokeh(lz, t, seed=61, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm), sx0=940, sy0=650)
    ml.salon_congreso(lz, iso, t)
    m = I.Mundo()
    ml.amueblar_congreso(m, t)
    tipos = ("regidor", "noble", "cura", "escribano", "comerciante", "regidor")
    for r in range(3):
        for sg, x0 in ((0, 30), (1, 190)):
            for c in range(5):
                x, y = x0 + 12 + 19 * c, 130 + 40 * r
                ti = T_A2 + 0.1 * (c + 5 * r + 15 * sg)
                k = e_back(prog(t, ti, ti + 0.4)) if t >= ti else 0.0
                if k > 0.01:
                    m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, c, r, sg, k: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[(c + r + sg) % 6], dir=(0.0, -1.0), seed=9900 + c + 5 * r + 15 * sg, h=46 * k, cara="serio", accion="vitorea" if (t > t_cong and (c + r) % 3 == 0) else None)))(x, y, c, r, sg, k), fijo=False, clave=x + y + 3)
    m.add(150, 54, 164, 66, 40, lambda lz, iso: G.persona(lz, iso, 157, 62, t, "cura", dir=(0, 1), seed=9890, h=60, cara="habla" if (t % 0.8) < 0.5 else "serio", accion="habla"), fijo=False, clave=215)
    m.add(190, 50, 204, 62, 20, lambda lz, iso: O.bandera(lz, iso, 196, 56, h=110, w=40, alto=26, color=(60, 150, 110), t=t, franjas=[((60, 150, 110), 0.34), ((250, 246, 236), 0.33), ((206, 60, 70), 0.33)]), fijo=False, clave=220)
    m.dibujar(lz, iso)
    k = U.pop(t, t_prim - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el primer congreso de la historia de México", color=U.COL["naranja"], px=64, k=k * U.repop(t, t_hist + 0.1), cola=None)
    k = U.pop(t, t_reu - 0.1) * U.salida(t, t_prim - 0.15, 0.2)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_A2, T_B - 0.2, "Chilpancingo", "Septiembre de 1813", y=70)


# ------------------------------------------------------------------------------------------------ 2. INDEPENDIENTES, SIN IMPORTAR ESPAÑA
def cam_b(t):
    return Klog(t, [(T_B, (-55.5, 27.0, 0.18)), (T_C, (-55.5, 27.0, 0.2))])


@shot(T_B, bg=lambda t: MP.base(cam_b(t), t, exag=8.0, rios_umbral=3.0), post=[GRAD], ent=("zoom", 0.6))
def co_indep(lz, t):
    cam = cam_b(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=15)
    MD.pais(lz, cam, "Spain", (200, 200, 220), alfa=0.30, borde=None, ancho=3.0)
    MD.pais(lz, cam, "Mexico", (70, 200, 120), alfa=0.38, borde=(150, 255, 180), ancho=7.0, t=t, latido=1.0)
    sx, sy = MP.proy(cam, -102.0, 23.5)
    px_, py_ = MP.proy(cam, -3.7, 40.2)
    U.llamada(lz, float(sx) - 20, float(sy) + 90, "MÉXICO", color=U.COL["verde"], px=44, k=U.pop(t, T_B + 0.3), cola=None)
    U.llamada(lz, float(px_), float(py_) + 90, "ESPAÑA", color=U.COL["rojo"], px=44, k=U.pop(t, T_B + 0.5), cola=None)
    kb = U.pop(t, t_ind - 0.1)
    if kb > 0.01:
        lz.trazo(np.array([[float(sx), float(sy) + 40], [float(sx), float(sy) - 160 * kb]]), (130, 96, 70), 7, afinar=False, temblor=0.0, capa=2)
        pts = [(float(sx) + k * 5, float(sy) - 160 * kb + 5 * math.sin(t * 5 - k * 0.5) + 0.2 * k) for k in range(0, 21)]
        pts += [(float(sx) + k * 5, float(sy) - 160 * kb + 56 + 5 * math.sin(t * 5 - k * 0.5) + 0.2 * k) for k in range(20, -1, -1)]
        lz.relleno(np.array(pts), (60, 150, 110), capa=2)
    # España en la tormenta: nubes y relámpagos; no cambia nada para México
    for j, (dx, dy, s) in enumerate(((-120, -80, 1.6), (60, -110, 2.0), (180, -60, 1.5))):
        kk = U.pop(t, t_esp - 0.3 + 0.1 * j)
        if kk > 0.01:
            O2.nube_tormenta(lz, float(px_) + dx, float(py_) + dy, s * kk, t + j * 1.1, relampago=max(0.0, 1.0 - ((t - t_esp + 0.2 * j) % 1.8) * 5))
    U.pergamino_grande(lz, 560, 560, 560, 330, t, t_decl - 0.1, lineas=("Declaramos la independencia", "de la América Septentrional", "6 de noviembre de 1813"), titulo="ACTA SOLEMNE", sello=True, rot=-0.05, alfa=U.salida(t, T_C - 0.25, 0.25))
    k = U.pop(t, t_decl - 0.05) * U.salida(t, t_imp - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el país será independiente", color=U.COL["verde"], px=78, k=k * U.repop(t, t_ind + 0.1), cola=None)
    k = U.pop(t, t_imp - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "sin importar lo que pase en España", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_esp + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 3. LOS SENTIMIENTOS DE LA NACIÓN
@shot(T_C, bg=PURP, post=[GRAD], ent=("fundido", 0.4))
def co_sentimientos(lz, t):
    U.bokeh(lz, t, seed=62, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, 1300, 520, t, n=9, largo=1300, color=(255, 200, 240), alfa=0.12, ancho=0.08)
    U.chispas(lz, t, n=20, seed=63, tam=(5, 12))
    kv = U.pop(t, T_C + 0.05, 1.3)
    RT.retrato(lz, 420, 1010, 240 * (0.94 + 0.06 * kv), "morelos", t, emocion="serio", habla=0.5 + 0.5 * math.sin(t * 6) if t < t_estudia else 0.0, mirar=0.4, seed=7, alfa=min(1.0, kv))
    U.pergamino_grande(lz, 1330, 520, 720, 560, t, t_doc - 0.1, lineas=("1. La América es libre", "2. La religión católica", "3. La soberanía viene del pueblo", "…23 puntos"), titulo="SENTIMIENTOS DE LA NACIÓN", sello=True, rot=0.03)
    ke = U.pop(t, t_estudia - 0.05)
    if ke > 0.01:
        # lupa: «aún se estudia»
        with lz.grupo(1700, 880, ke, 0.0):
            lz.trazo(circulo(0, 0, 64, 28), (250, 206, 70), 14, cerrado=True, afinar=False, temblor=0.0, capa=2)
            lz.relleno(circulo(0, 0, 58, 28), (200, 236, 255), alfa=0.30, capa=2)
            lz.trazo(np.array([[46, 46], [120, 120]]), (250, 206, 70), 16, afinar=False, temblor=0.0, capa=2)
    k = U.pop(t, t_pres - 0.05) * U.salida(t, t_estudia - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 130, "un documento…", color=U.COL["naranja"], px=80, k=k, cola=None)
    k = U.pop(t, t_estudia - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 130, "que aún se estudia", color=U.COL["azul"], px=76, k=k * U.repop(t, t_estudia + 0.2), cola=None)
    k = U.pop(t, t_sent - 0.05)
    if k > 0.01:
        U.llamada(lz, 420, 190, "José María Morelos", color=U.COL["azul"], px=44, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 4a. LA SOBERANÍA VIENE DEL PUEBLO
@shot(T_D1, bg=lambda t: bg_grad((90, 150, 230), (252, 226, 200), mid=(190, 200, 240), ym=0.55), post=[GRAD], ent=("tinta", 0.5))
def co_soberania(lz, t):
    mh.multitud_espalda(lz, t, n=260, y0=700.0, y1=1100.0, seed=11, alzar=e_inout(prog(t, t_pue - 0.2, t_pue + 0.8)), banderas=2, escala=1.2)
    # la corona pasa del rey a las manos de la multitud
    u = e_inout(prog(t, t_sob, t_pue + 0.7))
    x, y = lerp(300, 1330, u), lerp(420, 640, u) - 260 * math.sin(math.pi * u)
    kt = U.pop(t, T_D1 + 0.05)
    if kt > 0.01:
        RT.retrato(lz, 260, 560, 100 * (0.94 + 0.06 * kt), "fernando", t, emocion="serio", mirar=0.3, seed=9, alfa=min(1.0, kt) * (1 - 0.5 * u))
        U.llamada(lz, 260, 300, "el rey", color=U.COL["rojo"], px=42, k=kt, cola=None)
    MD.corona(lz, x, y, 6.0, 1.0, t)
    lz.halo(x, y, 340, (255, 224, 130), alfa=0.38, capa=2)
    k = U.pop(t, t_sob - 0.05) * U.salida(t, T_D2 - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la soberanía", color=U.COL["naranja"], px=88, k=k * U.repop(t, t_sob + 0.2), cola=None)
    k = U.pop(t, t_pue - 0.05) * U.salida(t, T_D2 - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 300, "viene del pueblo", color=U.COL["verde"], px=84, k=k * U.repop(t, t_pue + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 4b. LA ESCLAVITUD SE ABOLE PARA SIEMPRE
@shot(T_D2, bg=lambda t: bg_grad((50, 28, 112), (150, 64, 130), mid=(96, 40, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.3))
def co_cadena(lz, t):
    U.bokeh(lz, t, seed=64, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
    rota = e_out(prog(t, t_abol, t_abol + 0.9))
    ml.cadena(lz, W / 2, 540, n=8, t=t, rota=rota, ancho=110)
    if rota > 0.3:
        U.chispas(lz, t, n=24, seed=65, tam=(6, 14))
        lz.halo(W / 2, 540, 420 * rota, (255, 226, 150), alfa=0.35 * rota, capa=0)
    k = U.pop(t, t_escl - 0.05) * U.salida(t, T_D3 - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 200, "la esclavitud debe abolirse", color=U.COL["rojo"], px=76, k=k * U.repop(t, t_abol + 0.1), cola=None)
    k = U.pop(t, t_siempre - 0.05)
    if k > 0.01:
        P.rotulo(lz, W / 2, 860, "¡PARA SIEMPRE!", px=int(130 * (0.94 + 0.06 * k)), k=k * U.repop(t, t_siempre + 0.1), color=(255, 255, 255))


# ------------------------------------------------------------------------------------------------ 4c. DESAPARECEN LAS CASTAS
@shot(T_D3, bg=lambda t: bg_grad((110, 150, 230), (252, 226, 200), mid=(196, 190, 236), ym=0.55), post=[GRAD], ent=("fundido", 0.3))
def co_castas(lz, t):
    ap = e_inout(prog(t, t_desap, t_castas + 0.6))
    ml.escalera_castas(lz, W / 2, 360, t, aplana=ap, k=1.0)
    k = U.pop(t, T_D3 + 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "las castas desaparecen", color=U.COL["morado"], px=82, k=k * U.repop(t, t_castas + 0.2), cola=None)
    if ap > 0.7:
        U.llamada(lz, W / 2, 900, "un solo pueblo", color=U.COL["verde"], px=78, k=U.pop(t, t_castas + 0.3), cola=None)


# ------------------------------------------------------------------------------------------------ 5. TODOS AMERICANOS
@shot(T_E, bg=lambda t: bg_grad((90, 160, 230), (254, 234, 204), mid=(196, 214, 240), ym=0.55), post=[GRAD], ent=("fundido", 0.4))
def co_americanos(lz, t):
    U.chispas(lz, t, n=16, seed=66, tam=(5, 12))
    quienes = (("campesina", 200), ("esclavo", 580), ("criollo", 960), ("campesino", 1340), ("peninsular", 1720))
    pieles = ((150, 98, 70), (110, 74, 54), (232, 190, 150), (190, 130, 98), (250, 214, 186))
    for i, (q, x) in enumerate(quienes):
        k = U.pop(t, t_hab - 0.2 + 0.18 * i, 1.2)
        if k > 0.01:
            RT.retrato(lz, x, 1010, 150 * (0.94 + 0.06 * k), q, t, emocion="neutro", mirar=0.0, seed=20 + i, alfa=min(1.0, k))
    kb = U.pop(t, t_amer - 0.1, 1.3)
    if kb > 0.01:
        P.rotulo(lz, W / 2, 200, "AMERICANOS", px=int(190 * (0.94 + 0.06 * kb)), k=kb * U.repop(t, t_amer + 0.2), color=(255, 255, 255))
    # muestras de piel: todos iguales
    for i, c in enumerate(pieles):
        kc = U.pop(t, t_color - 0.1 + 0.12 * i)
        if kc > 0.01:
            lz.relleno(circulo(W / 2 - 320 + 160 * i, 440, 54 * kc, 24), c, capa=2)
            lz.trazo(circulo(W / 2 - 320 + 160 * i, 440, 58 * kc, 24), (255, 255, 255), 6, cerrado=True, afinar=False, temblor=0.0, capa=2)
    k = U.pop(t, t_color - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 590, "sin importar el color de su piel", color=U.COL["morado"], px=58, k=k * U.repop(t, t_piel + 0.1), cola=None)
    k = U.pop(t, t_todos - 0.05) * U.salida(t, t_amer - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 180, "todos los habitantes…", color=U.COL["naranja"], px=70, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 6. LA CONSTITUCIÓN DE APATZINGÁN
def cam_f(t):
    return Klog(t, [(T_F, (-102.0, 19.3, 1.8)), (T_F2, (-102.35, 19.08, 3.4))])


@shot(T_F, bg=lambda t: BASE(cam_f(t), t), post=[GRAD], ent=("zoom", 0.5))
def co_apatzingan(lz, t):
    cam = cam_f(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "valladolid", t, T_F, tam=1.1, tipo="ciudad", bando="real", semilla=3)
    MD.etiqueta(lz, cam, "valladolid", "Valladolid", t, T_F + 0.1, px=22, dy=4, dx=-120, lado="der")
    MD.ciudad(lz, cam, "apatzingan", t, t_pub, tam=2.4, tipo="pueblo", bando=(255, 206, 70), semilla=5)
    MD.onda(lz, cam, "apatzingan", t, t_apat, dur=2.2, r_deg=0.4, color=(255, 236, 170), n=3, ancho=5.0)
    k = U.pop(t, t_ano - 0.05) * U.salida(t, t_const - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "al año siguiente…", color=U.COL["azul"], px=84, k=k, cola=None)
    k = U.pop(t, t_pub - 0.05)
    if k > 0.01:
        sx, sy = MP.proy(cam, -102.35, 19.08)
        U.llamada(lz, float(sx), float(sy) - 130, "Apatzingán", color=U.COL["morado"], px=66, k=k * U.repop(t, t_apat + 0.1), cola="abajo")
        P.rotulo(lz, 330, 200, "1814", px=int(200 * (0.9 + 0.1 * k)), k=k, color=(255, 214, 72))
    MD.brujula(lz, W - 110, H - 120, 1.0)


@shot(T_F2, bg=PURP, post=[GRAD], ent=("destello", 0.4))
def co_constitucion(lz, t):
    U.bokeh(lz, t, seed=67, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.26)
    U.haces_luz(lz, W / 2, 560, t, n=10, largo=1400, color=(255, 214, 240), alfa=0.14, ancho=0.08)
    U.chispas(lz, t, n=28, seed=68, tam=(6, 15))
    U.pergamino_grande(lz, W / 2, 560, 880, 640, t, T_F2 + 0.05, lineas=("Decreto Constitucional", "para la Libertad de la", "América Mexicana", "22 de octubre de 1814"), titulo="CONSTITUCIÓN DE APATZINGÁN", sello=True, rot=-0.02)
    k = U.pop(t, t_primera - 0.1, 1.3)
    if k > 0.01:
        lz.relleno(circulo(1560, 300, 110 * k, 28), (250, 206, 70), capa=2)
        lz.relleno(circulo(1560, 300, 92 * k, 28), (255, 232, 130), capa=2)
        P.rotulo(lz, 1560, 300, "1ª", px=int(120 * k) + 10, k=1.0, color=(150, 80, 20), sombra=0.0)
    k = U.pop(t, t_primera - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 1000, "la primera de México independiente", color=U.COL["verde"], px=66, k=k * U.repop(t, t_indep + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_mor, "pop", 0.4)
snd(t_chil, "campana", 0.4)
snd(T_A2, "tambor", 0.4)
snd(t_hist, "bling", 0.5)
snd(T_B, "whoosh", 0.3, dur=1.0)
snd(t_ind, "bling", 0.5)
snd(t_esp, "trueno", 0.4)
snd(T_C, "pop", 0.3)
snd(t_sent, "bling", 0.5)
snd(T_D1, "whoosh", 0.3, dur=0.8)
snd(t_sob, "bling", 0.5)
snd(T_D2, "pop", 0.3)
snd(t_abol, "crujido", 0.6)
snd(t_siempre, "gong", 0.5)
snd(T_D3, "whoosh", 0.3, dur=0.8)
snd(t_desap, "bling", 0.5)
snd(T_E, "pop", 0.3)
for _i in range(5):
    snd(t_hab - 0.2 + 0.18 * _i, "pop", 0.25)
snd(t_amer, "bling", 0.6)
snd(T_F, "whoosh", 0.3, dur=1.0)
snd(t_apat, "campana", 0.4)
snd(T_F2, "bling", 0.5)
snd(t_primera, "gong", 0.5)
