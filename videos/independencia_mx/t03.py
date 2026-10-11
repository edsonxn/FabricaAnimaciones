# -*- coding: utf-8 -*-
"""Escena 3 · Napoleón y el golpe al virrey (1:06-1:45): el océano, la invasión, Bayona, el trono y la celda (pantalla dividida), el ayuntamiento, el virrey y los ricos, el arresto de noche y el poder que cambia de manos."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
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
import mundos_d as md

E3 = "napoleon"
MP = KM.MAPA
PLZ = md.PlazaMayor()
GRAD = lambda img, t: U.gradacion(img)

# ------------------------------------------------------------------ anclas
t_ent, t_oc, t_ocu, t_algo, t_camb = T(E3, "entonces", frase=0), T(E3, "oceano", frase=0), T(E3, "ocurrio", frase=0), T(E3, "algo", frase=0), T(E3, "cambio", frase=0)
t_mil, t_ocho, t_nap, t_inv, t_esp, t_obl, t_rey, t_abd = T(E3, "mil", frase=1), T(E3, "ocho", frase=1), T(E3, "napoleon", frase=1), T(E3, "invadio", frase=1), T(E3, "espana", frase=1), T(E3, "obligo", frase=1), T(E3, "rey", frase=1), T(E3, "abdicar", frase=1)
t_puso, t_trono, t_herm, t_pron, t_rey2, t_obed, t_pris = T(E3, "puso", frase=2), T(E3, "trono", frase=2), T(E3, "hermano", frase=2), T(E3, "pronto", frase=2), T(E3, "rey", frase=2), T(E3, "obedecian", frase=2), T(E3, "prisionero", frase=2)
t_cap, t_nesp, t_ayu, t_prop, t_inau, t_sinrey, t_poder, t_pueblo = T(E3, "capital", frase=3), T(E3, "nueva", frase=3), T(E3, "ayuntamiento", frase=3), T(E3, "propuso", frase=3), T(E3, "inaudito", frase=3), T(E3, "rey", frase=3), T(E3, "poder", frase=3), T(E3, "pueblo", frase=3)
t_vir, t_acep, t_esc, t_grupo, t_ricos, t_espan, t_trai = T(E3, "virrey", frase=4), T(E3, "acepto", frase=4), T(E3, "escuchar", frase=4), T(E3, "grupo", frase=4), T(E3, "ricos", frase=4), T(E3, "espanoles", frase=4), T(E3, "traicion", frase=4)
t_noche, t_sep, t_arr, t_mand, t_regr = T(E3, "noche", frase=5), T(E3, "septiembre", frase=5), T(E3, "arrestaron", frase=5), T(E3, "mandaron", frase=5), T(E3, "regreso", frase=5)
t_golpe, t_estado, t_dem, t_nesp2, t_pod2, t_camb2, t_manos, t_fuerza = T(E3, "golpe", frase=6), T(E3, "estado", frase=6), T(E3, "demostro", frase=6), T(E3, "nueva", frase=6), T(E3, "poder", frase=6), T(E3, "cambiar", frase=6), T(E3, "manos", frase=6), T(E3, "fuerza", frase=6)
T_INV, T_ABD, T_TRONO, T_PRIS, T_AYU, T_PLAZA, T_VIR, T_RICOS, T_ARR, T_GOLPE = t_mil - 0.4, t_obl - 0.15, t_puso - 0.25, t_pron - 0.35, t_cap - 0.3, t_ayu - 0.7, t_vir - 0.2, t_grupo - 0.25, t_noche - 0.2, t_golpe - 0.25
BAYONA = (-1.47, 43.49)
RUTA_INV = [(2.35, 48.86), (1.0, 46.0), (-0.5, 44.2), (-1.47, 43.49), (-1.9, 42.8), (-3.0, 41.4), (-3.7, 40.42)]

PICOS_PIRINEOS = [(-1.6, 42.9, 3000), (-0.7, 42.8, 3300), (0.3, 42.7, 3400), (1.2, 42.7, 3000), (2.0, 42.5, 2800), (-2.3, 42.9, 2600), (6.8, 45.8, 4700), (7.6, 46.0, 4400), (8.5, 46.5, 3900), (9.5, 46.4, 3600)]


def cielo_n(lz, t, base=(40, 30, 90), n=7, y0=40, y1=300, seed=3):
    for i in range(n):
        x = (h01(seed, i, 1) * 2600 - 360 + t * (5 + 4 * h01(seed, i, 2))) % 2600 - 360
        y = y0 + (y1 - y0) * h01(seed, i, 3)
        r = 70 + 60 * h01(seed, i, 5)
        for (dx, dy, rr, c) in ((0, r * 0.2, 1.0, P.oscurecer(base, 0.2)), (-r * 0.7, r * 0.08, 0.7, P.oscurecer(base, 0.2)), (r * 0.7, r * 0.12, 0.74, P.oscurecer(base, 0.2)),
                                (0, 0, 0.95, base), (-r * 0.65, -r * 0.05, 0.66, base), (r * 0.65, 0, 0.7, base)):
            lz.relleno(circulo(x + dx, y + dy, r * rr, 18), c, capa=0)


# ------------------------------------------------------------------------------------------------ 1. «AL OTRO LADO DEL OCÉANO»
def cam_oc(t):
    return Klog(t, [(T0(E3), (-100.0, 23.0, 0.74)), (t_oc + 0.2, (-62.0, 29.5, 0.21)), (t_algo - 0.3, (-20.0, 36.0, 0.34)), (T_INV, (-3.0, 41.0, 0.95))])


@shot(T0(E3), bg=lambda t: MP.base(cam_oc(t), t), post=[GRAD], ent=("fundido", 0.5))
def p_oceano(lz, t):
    cam = cam_oc(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=4)
    MD.montes(lz, cam)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.28, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.pais(lz, cam, "Spain", (255, 210, 70), alfa=0.36, borde=(255, 236, 130), ancho=3.0)
    f = e_inout(prog(t, T0(E3) + 0.2, t_algo + 0.6))
    cab = MD.ruta(lz, cam, [(-96.13, 19.18), (-85.2, 24.6), (-70.0, 29.0), (-45.0, 33.0), (-20.0, 35.8), (-6.3, 36.5)], color=(255, 236, 160), frac=f, t=t, ancho=5.0, flecha=False)
    if cab is not None:
        MD.barco_plano(lz, cab[0], cab[1] - 6, 1.0, t, dir=-1)
    MD.ciudad(lz, cam, "mexico", t, T0(E3), tam=1.5 if cam[2] > 0.5 else 0.8, tipo="ciudad", bando="real", semilla=3)
    MD.ciudad(lz, cam, "madrid", t, t_algo - 0.4, tam=1.6, tipo="ciudad", bando=(255, 206, 70), semilla=9)
    MD.region(lz, cam, "OCÉANO ATLÁNTICO", (-45.0, 26.0), px=36, alfa=0.5, z_max=0.7)
    # tormenta sobre España: nubes oscuras, relámpagos, «!» enorme
    k = U.pop(t, t_algo - 0.2)
    if k > 0.01:
        sx, sy = MP.proy(cam, -3.7, 41.5)
        for j, (dx, dy, s) in enumerate(((-140, -150, 1.8), (0, -190, 2.2), (150, -140, 1.7))):
            O2.nube_tormenta(lz, float(sx) + dx, float(sy) + dy, s * k, t + j * 1.3, relampago=max(0.0, 1.0 - ((t - t_algo + 0.2 * j) % 1.8) * 5))
        U.llamada(lz, float(sx), float(sy) - 20, "!", color=U.COL["rojo"], px=130, k=k * U.repop(t, t_camb), cola="abajo")
    kk = U.pop(t, t_ocu)
    if kk > 0.01 and cam[2] < 0.5:
        U.llamada(lz, W / 2, 140, "Al otro lado del océano", color=U.COL["azul"], px=64, k=kk * U.salida(t, t_algo, 0.3), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. LA INVASIÓN FRANCESA
def cam_inv(t):
    return Klog(t, [(T_INV, (-1.5, 44.5, 1.15)), (t_inv, (-1.5, 43.5, 1.7)), (t_esp, (-2.5, 42.0, 1.9)), (T_ABD, (-3.0, 41.5, 2.1))])


@shot(T_INV, bg=lambda t: MP.base(cam_inv(t), t), post=[GRAD], ent=("zoom", 0.7))
def p_invasion(lz, t):
    cam = cam_inv(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=6)
    MD.montes_lista(lz, cam, PICOS_PIRINEOS)
    for nombre, col in (("France", (80, 130, 230)), ("Spain", (255, 210, 70)), ("Portugal", (90, 190, 120)), ("Italy", (150, 130, 230)), ("Germany", (240, 160, 70)), ("Switzerland", (230, 90, 100))):
        MD.pais(lz, cam, nombre, col, alfa=0.10, borde=col if nombre in ("Spain", "France") else None, ancho=4.0)
    for txt, ll, col in (("FRANCIA", (2.2, 46.4), U.COL["azul"]), ("ESPAÑA", (-2.1, 40.2), U.COL["rojo"]), ("PORTUGAL", (-8.2, 40.4), U.COL["verde"])):
        sx, sy = MP.proy(cam, ll[0], ll[1])
        k_ = U.pop(t, T_INV + 0.2)
        if k_ > 0.01 and cam[2] > 1.2:
            U.llamada(lz, float(sx), float(sy), txt, color=col, px=34, k=k_, cola=None)
    for j, (lug, tp, col) in enumerate((("paris", "ciudad", (80, 130, 230)), ("madrid", "ciudad", (255, 206, 70)), ("lisboa", "puerto", (90, 190, 120)), ("cadiz", "puerto", (255, 206, 70)), ("roma", "ciudad", (150, 130, 230)))):
        MD.ciudad(lz, cam, lug, t, T_INV + 0.1 * j, tam=1.6, tipo=tp, bando=col, semilla=j + 20)
    MD.ciudad(lz, cam, BAYONA, t, T_INV + 0.3, tam=1.2, tipo="puerto", bando=(80, 130, 230), nombre="Bayona", px=26)
    for j, (lug, nom) in enumerate((((-0.88, 41.65), "Zaragoza"), ((-3.70, 42.34), "Burgos"), ((-4.72, 41.65), "Valladolid"), ((-0.58, 44.84), "Burdeos"), ((1.44, 43.60), "Toulouse"), ((2.17, 41.39), "Barcelona"),
                                    ((-5.99, 37.39), "Sevilla"), ((-0.38, 39.47), "Valencia"))):
        MD.pueblo(lz, cam, lug, nom, t, T_INV + 0.4 + 0.08 * j)
    P.rotulo(lz, 330, 150, "1808", px=200, k=U.pop(t, t_mil - 0.2, 1.2) * U.salida(t, t_nap + 1.0, 0.3), color=(255, 214, 72))
    kn = U.pop(t, t_nap) * U.salida(t, T_ABD, 0.2)
    if kn > 0.01:
        MD.medallon(lz, 300, 540, 120, "napoleon", t, emocion="serio", k=kn)
        U.llamada(lz, 300, 720, "Napoleón", color=U.COL["azul"], px=44, k=kn, cola="arriba")
    # tres columnas del ejército francés avanzan por la ruta; bandera tricolor y humo de cañones
    f = e_inout(prog(t, t_nap + 0.3, t_esp + 0.6))
    cab = MD.ruta(lz, cam, RUTA_INV, color=(120, 170, 255), frac=f, t=t, ancho=8.0, flecha=True)
    TRI = [((46, 80, 190), 1 / 3), ((250, 250, 248), 1 / 3), ((214, 52, 66), 1 / 3)]
    for j in range(3):
        u = max(0.0, min(1.0, f - 0.05 * j))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_INV, u)
            MD.ejercito(lz, x + 26 * j, y + 18 * j, 12, bando=(46, 80, 190), t=t + j, s=2.5 * max(1.0, cam[2] ** 0.2), dir=1, estandarte=TRI, semilla=j)
    if t > t_esp:
        MD.insignia_batalla(lz, cam, "madrid", t, t_esp + 0.1, s=1.3)
        sx, sy = MP.proy(cam, -3.7, 40.42)
        for i in range(5):
            u = ((t - t_esp) * 0.9 + i * 0.2) % 1.0
            lz.relleno(circulo(float(sx) + 14 * math.sin(i * 2 + t), float(sy) - 40 - 90 * u, 10 + 22 * u, 12), (236, 232, 240), alfa=0.5 * (1 - u), capa=2)
    kk = U.pop(t, t_inv - 0.1) * U.salida(t, T_ABD - 0.1)
    if kk > 0.01:
        sx, sy = MP.proy(cam, -1.0, 44.4)
        U.llamada(lz, float(sx) + 40, float(sy) - 30, "invasión de España", color=U.COL["rojo"], px=44, k=kk, cola="abajo")
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 3. BAYONA: LA ABDICACIÓN
@shot(T_ABD, bg=lambda t: bg_grad((40, 24, 80), (110, 54, 110), mid=(70, 36, 100), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def p_abdica(lz, t):
    import kz_iso_int as N
    I.luz()
    U.bokeh(lz, t, seed=5, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
    iso = I.Iso(130, 130, 36, 3.5 + 0.06 * (t - T_ABD), sx0=900, sy0=620)
    c = md.dibujar_salon(lz, iso, t)
    md._alfombra(lz, iso, 40, 70, 210, 150)
    m = I.Mundo()
    firma = prog(t, t_rey - 0.4, t_abd + 0.2)
    m.add(70, 100, 160, 150, 40, lambda lz, iso: md.mesa_firma(lz, iso, 70, 100, t, firma), clave=170)
    m.add(60, 90, 70, 100, 40, lambda lz, iso: G.persona(lz, iso, 82, 156, t, "monarca", dir=(1, -0.6), seed=71, piel=G.PIELES[0], h=58, accion="trabaja" if firma < 1 else None, cara="triste"), fijo=False, clave=190)
    m.add(190, 100, 200, 110, 40, lambda lz, iso: G.persona(lz, iso, 200, 112, t, "napoleon", dir=(-0.5, 1.0), seed=72, piel=G.PIELES[0], h=58, accion="chaleco", cara="serio"), fijo=False, clave=300)
    for i, (x, y) in enumerate(((36, 56), (36, 120), (262, 62), (262, 140), (130, 40))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, "granadero", dir=(0.5, 1) if x < 150 else (-0.5, 1), seed=73 + i, h=56)))(x, y, i), fijo=False, clave=x + y)
    m.add(110, 150, 130, 170, 40, lambda lz, iso: G.persona(lz, iso, 120, 184, t, "escribano", dir=(0.4, -1), seed=80, h=52), fijo=False, clave=260)
    m.add(10, 200, 24, 214, 30, lambda lz, iso: N.maceta(lz, iso, 16, 206, 1.4, t))
    m.add(270, 200, 284, 214, 30, lambda lz, iso: N.maceta(lz, iso, 276, 206, 1.4, t))
    m.add(8, 130, 24, 146, 60, lambda lz, iso: N.reloj_pie(lz, iso, 16, 138, t, 1.3))
    u = prog(t, t_abd - 0.1, t_abd + 1.4)
    if u > 0:
        cx_ = lerp(94, 150, e_out(u))
        cy_ = lerp(146, 190, u)
        z_ = 30 * (1 - e_out(min(1.0, u * 1.6))) + 3
        m.add(cx_ - 4, cy_ - 4, cx_ + 4, cy_ + 4, 20, lambda lz, iso: O2.corona(lz, iso, cx_, cy_, z_, 0.9, rot=u * 9.0), fijo=False, clave=cx_ + cy_ + 50)
    m.dibujar(lz, iso)
    N.araña(lz, iso, 140, 120, 140, t, velas=6, s=1.4)
    U.fecha_lugar(lz, t, T_ABD, T1(E3) - 20, "Bayona, Francia", "Mayo de 1808", y=70)
    k = U.pop(t, t_abd - 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 340, 250, "abdicar", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_abd + 0.3), cola="izq")
    qx, qy = iso.P(200, 112, 120)
    ks = U.pop(t, T_ABD + 0.25) * U.salida(t, t_abd - 0.3, 0.2)
    if ks > 0.01:
        U.llamada(lz, float(qx), float(qy) - 10, "Napoleón", color=U.COL["azul"], px=44, k=ks, cola="abajo")
        qx, qy = iso.P(82, 156, 120)
        U.llamada(lz, float(qx), float(qy) - 10, "Carlos IV", color=U.COL["rojo"], px=44, k=ks, cola="abajo")


# ------------------------------------------------------------------------------------------------ 4. EL TRONO Y LA CELDA (pantalla dividida con muesca)
def _celda(lz, iso, t):
    import kz_iso_int as N
    c = I.habitacion(lz, iso, 0, 0, 260, 220, 140, piso=(104, 100, 112), pared_a=(142, 138, 152), pared_b=(122, 118, 136), friso=(86, 82, 98))
    for i in range(7):
        for j in range(6):
            I.suelo_rect(lz, iso, 6 + i * 36, 6 + j * 34, 34, 32, (120 + 8 * ((i + j) % 2), 116 + 8 * ((i + j) % 2), 130), z=0.1, alfa=0.8)
    # ventana alta con barrotes y haz de luz
    I.cara_rect(lz, iso, c, "yi", 100, 150, 70, 120, (180, 210, 250))
    for kx in range(4):
        I.cara_rect(lz, iso, c, "yi", 108 + kx * 12, 111 + kx * 12, 70, 120, (60, 56, 76))
    lz.relleno(iso.pts([(100, 4, 120), (150, 4, 120), (190, 150, 0), (110, 150, 0)]), (255, 244, 200), alfa=0.20, capa=2)
    # sillares en la pared, cadenas, antorcha, paja, jarra y un baúl
    for k in range(1, 8):
        I.cara_rect(lz, iso, c, "yi", 0, 260, k * 18 - 0.5, k * 18 + 0.5, (110, 106, 124), tono=False)
        I.cara_rect(lz, iso, c, "xi", 0, 220, k * 18 - 0.5, k * 18 + 0.5, (96, 92, 110), tono=False)
    N.cadenas(lz, iso, c, "yi", 40, 96, n=6, t=t)
    N.cadenas(lz, iso, c, "yi", 60, 90, n=5, t=t + 1.0)
    N.cadenas(lz, iso, c, "xi", 150, 96, n=6, t=t + 0.5)
    N.paja(lz, iso, 20, 120, 140, 210, n=110, seed=5)
    O.antorcha(lz, iso, 6, 80, t, h=64, seed=3)
    lz.halo(*iso.P(6, 80, 80), 200 * iso.z / 3.0, (255, 160, 80), alfa=0.18, capa=2)
    return c


@shot(T_TRONO, bg=lambda t: bg_grad((50, 28, 112), (140, 60, 130)), post=[GRAD], ent=("fundido", 0.5))
def p_trono(lz, t):
    import kz_iso_int as N
    I.luz()
    tn = e_inout(prog(t, T_PRIS, T_PRIS + 0.8))            # 0: pantalla completa del trono; 1: dividida por la mitad
    xdiv = lerp(W + 40, W / 2, tn)
    # --- mitad izquierda: el trono y José Bonaparte
    pol = np.array([[-10, -10], [xdiv - 26, -10], [xdiv + 26, H / 2], [xdiv - 26, H + 10], [-10, H + 10]], float)
    with lz.recorte(pol):
        lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (66, 36, 130), capa=0)
        U.bokeh(lz, t, seed=5, n=10, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
        iso = I.Iso(150, 140, 30, 3.4, sx0=lerp(W / 2 + 40, 520, tn), sy0=640)
        c = md.dibujar_salon(lz, iso, t, tipo="trono")
        md._alfombra(lz, iso, 80, 60, 140, 190)
        m = I.Mundo()
        m.add(130, 40, 170, 80, 60, lambda lz, iso: md.trono(lz, iso, 150, 60, t, 1.2, corona=False), clave=100)
        k_c = e_inout(prog(t, t_herm - 0.2, t_herm + 0.9))
        m.add(130, 40, 170, 80, 60, lambda lz, iso: O2.corona(lz, iso, lerp(210, 150, k_c), lerp(100, 78, k_c), lerp(80, 74, k_c) + 12 * math.sin(math.pi * k_c), 0.9, rot=0.0), fijo=False, clave=300)
        m.add(140, 62, 160, 92, 60, lambda lz, iso: G.persona(lz, iso, 150, 82, t, "monarca", dir=(0, 1), seed=90, piel=G.PIELES[0], h=54, accion="saluda" if t > t_herm + 0.8 else None, z=14, cara="alegre" if t > t_herm + 0.8 else None), fijo=False, clave=250)
        m.add(190, 90, 210, 110, 60, lambda lz, iso: G.persona(lz, iso, 198, 100, t, "napoleon", dir=(-0.5, 1.0), seed=91, h=54, accion="chaleco" if t > t_herm + 0.8 else "habla", cara="serio"), fijo=False, clave=330)
        for i, (x, y) in enumerate(((70, 60), (70, 120), (230, 60), (230, 120), (80, 200), (220, 200))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, "granadero" if i < 4 else "noble", dir=(0.6 if x < 150 else -0.6, 1), seed=92 + i, h=52, accion="vitorea" if (i >= 4 and t > t_herm + 1.0) else None)))(x, y, i), fijo=False, clave=x + y)
        m.add(14, 200, 28, 214, 30, lambda lz, iso: N.maceta(lz, iso, 20, 206, 1.3, t))
        m.dibujar(lz, iso)
        N.araña(lz, iso, 150, 130, 140, t, velas=6, s=1.3)
        kk = U.pop(t, t_herm - 0.1)
        if kk > 0.01:
            qx, qy = iso.P(150, 82, 110)
            U.llamada(lz, float(qx), float(qy) - 20, "José Bonaparte", color=U.COL["azul"], px=44, k=kk, cola="abajo")
    # --- mitad derecha: la celda del rey prisionero
    if tn > 0.01:
        pol2 = np.array([[xdiv + 26, -10], [W + 10, -10], [W + 10, H + 10], [xdiv - 26, H + 10], [xdiv + 26, H / 2]], float)
        with lz.recorte(pol2):
            lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (34, 36, 70), capa=0)
            iso2 = I.Iso(120, 120, 30, 3.4, sx0=lerp(W + 700, 1430, tn), sy0=640)
            _celda(lz, iso2, t)
            m2 = I.Mundo()
            m2.add(100, 80, 140, 130, 60, lambda lz, iso: G.persona(lz, iso, 112, 124, t, "monarca", dir=(0.3, 1), seed=71, piel=G.PIELES[0], h=54, cara="triste"), fijo=False, clave=200)
            m2.add(100, 80, 140, 130, 60, lambda lz, iso: O2.grillete(lz, iso, 112, 124, 4, t), fijo=False, clave=201)
            m2.add(60, 150, 70, 160, 60, lambda lz, iso: G.persona(lz, iso, 190, 166, t, "granadero", dir=(-1, 0.4), seed=95, h=54), fijo=False, clave=350)
            m2.add(50, 20, 60, 30, 60, lambda lz, iso: O.barril(lz, iso, 40, 40, 1.2), clave=90)
            m2.add(60, 60, 70, 70, 30, lambda lz, iso: N.jarra_pan(lz, iso, 70, 150, 1.3), clave=140)
            m2.add(200, 20, 224, 40, 40, lambda lz, iso: N.baul(lz, iso, 200, 24), clave=100)
            m2.dibujar(lz, iso2)
            O2.barrotes(lz, iso2, 10, 214, 240, 100, n=12, z=0.0)
            kk = U.pop(t, t_pris - 0.5)
            if kk > 0.01:
                qx, qy = iso2.P(112, 124, 110)
                U.llamada(lz, float(qx) + 40, float(qy) - 30, "El rey, prisionero", color=U.COL["rojo"], px=44, k=kk, cola="abajo")
        lz.trazo(np.array([[xdiv - 26, -10], [xdiv + 26, H / 2], [xdiv - 26, H + 10]]), (255, 255, 255), 6.0, afinar=False, temblor=0.0, capa=2)
    kf = U.pop(t, T_TRONO + 0.2) * U.salida(t, t_pron - 0.1, 0.3)
    if kf > 0.01:
        U.llamada(lz, 440, 130, "su propio hermano", color=U.COL["naranja"], px=56, k=kf, cola=None)


# ------------------------------------------------------------------------------------------------ 5. LA CAPITAL: EL AYUNTAMIENTO
def cam_cdmx(t):
    return Klog(t, [(T_AYU, (-99.13, 19.43, 1.6)), (T_AYU + 1.4, (-99.13, 19.43, 6.0))])


@shot(T_AYU, bg=lambda t: MP.base(cam_cdmx(t), t), post=[GRAD], ent=("tinta", 0.7))
def p_capital(lz, t):
    cam = cam_cdmx(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=7)
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.22, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "mexico", t, T_AYU + 0.05, tam=2.4 if cam[2] < 4 else 1.2, tipo="ciudad", bando="real", nombre="Ciudad de México", px=32)
    for j, (lug, tp) in enumerate((("puebla", "ciudad"), ("veracruz", "puerto"), ("queretaro", "ciudad"), ("zitacuaro", "pueblo"), ("cuautla", "pueblo"))):
        MD.ciudad(lz, cam, lug, t, T_AYU + 0.2 + 0.1 * j, tam=1.5, tipo=tp, bando="real", semilla=j + 6)
    kk = U.pop(t, t_cap) * U.salida(t, T_PLAZA - 0.2, 0.2)
    if kk > 0.01:
        U.llamada(lz, W / 2, 130, "Capital de la Nueva España", color=U.COL["naranja"], px=66, k=kk, cola=None)


def cam_plaza(t):
    return K(t, [(T_PLAZA, (260, 330, 50, 2.0)), (t_prop, (230, 160, 70, 2.4)), (t_inau, (240, 170, 70, 2.2)), (t_sinrey, (260, 260, 40, 1.9)), (t_poder, (260, 300, 30, 1.8)), (T_VIR, (260, 320, 20, 1.7))])


@shot(T_PLAZA, bg=lambda t: bg_grad((90, 150, 220), (230, 240, 252)), post=[GRAD], ent=("fundido", 0.5))
def p_ayuntamiento(lz, t):
    cx, cy, cz, zm = cam_plaza(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz()
    PLZ.suelo(lz, iso, t)
    m = PLZ.objetos(t)
    # regidores en el balcón del Palacio con el pergamino (el ayuntamiento)
    vit = t > t_pueblo - 0.2
    for i, x in enumerate((190, 214, 238, 262, 286, 310)):
        m.add(x - 4, 74, x + 4, 82, 40, (lambda x, i: (lambda lz, iso: G.persona(lz, iso, x, 82, t, "regidor", dir=(0, 1), seed=1100 + i, h=44, z=40, accion=("habla" if (i % 2 and t > t_prop) else None))))(x, i), fijo=False, clave=x + 90)
    m.add(260, 76, 270, 86, 60, lambda lz, iso: O2.pergamino(lz, iso, 250, 86, 66, w=18, h=24, abre=min(1.0, prog(t, t_prop - 0.2, t_prop + 0.4))), fijo=False, clave=380)
    # más multitud que vitorea cuando «el poder vuelve al pueblo»
    for i in range(16):
        x, y = 150 + 220 * h01(77, i), 170 + 220 * h01(78, i)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ["campesino", "campesina", "mestizo", "indigena", "indigena_f", "nino"][i % 6], dir=(0, -1), seed=1200 + i, h=42 if i % 6 != 5 else 30, accion="vitorea" if vit else None)))(x, y, i),
              fijo=False, clave=x + y)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=8, seed=11, y0=90, y1=300)
    # la corona de la monarquía sobre el Palacio: se agrieta con «sin rey» y el poder (halo dorado) baja a la multitud
    qx, qy = iso.P(260, 40, 150)
    kc = U.pop(t, t_inau + 0.2) * (1 - prog(t, t_sinrey + 0.4, t_sinrey + 0.9))
    if kc > 0.01:
        O2.corona(lz, iso, 260, 40, 150 + 6 * math.sin(t * 2), 3.2 * kc, brillo=1.0)
    if t > t_sinrey + 0.4:
        for i in range(14):
            a = i * 0.45 + t
            u = prog(t, t_sinrey + 0.4, t_sinrey + 1.4)
            lz.relleno(circulo(float(qx) + math.cos(a) * 160 * u, float(qy) + math.sin(a) * 100 * u + 140 * u * u, 6 * (1 - u * 0.7), 8), (255, 214, 100), alfa=1 - u, capa=2)
    kp = prog(t, t_poder - 0.1, t_poder + 1.2)
    if kp > 0.01:
        px_, py_ = iso.P(260, 290, 0)
        lz.halo(float(px_), float(py_) - 40, 420 * kp, (255, 224, 130), alfa=0.35 * min(1.0, kp * 2), capa=2)
        for i in range(10):
            U.chispa4(lz, float(px_) + 300 * math.cos(i * 0.63 + t * 0.4), float(py_) - 30 + 180 * math.sin(i * 0.63 + t * 0.4), 14 + 8 * (i % 3), alfa=0.85 * kp)
    qx, qy = iso.P(262, 82, 100)
    k = U.pop(t, t_ayu - 0.1) * U.salida(t, t_prop + 1.6)
    if k > 0.01:
        U.llamada(lz, float(qx), float(qy) - 20, "El ayuntamiento", color=U.COL["morado"], px=52, k=k, cola="abajo")
    k = U.pop(t, t_inau) * U.salida(t, t_sinrey)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "¡Algo inaudito!", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_inau + 0.4), cola=None)
    k = U.pop(t, t_pueblo - 0.4)
    if k > 0.01:
        px_, py_ = iso.P(260, 300, 40)
        U.llamada(lz, float(px_), float(py_) - 90, "el poder al pueblo", color=U.COL["verde"], px=58, k=k * U.repop(t, t_pueblo + 0.3), cola="abajo")


# ------------------------------------------------------------------------------------------------ 6. EL VIRREY ESCUCHA / LOS RICOS SE ENOJAN
@shot(T_VIR, bg=lambda t: bg_grad((54, 30, 110), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def p_virrey(lz, t):
    U.bokeh(lz, t, seed=7, n=16, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.26)
    U.haces_luz(lz, 700, 480, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    U.chispas(lz, t, n=20, seed=14, tam=(5, 12))
    k = U.pop(t, T_VIR + 0.05, 1.3)
    kv = U.salida(t, T_RICOS - 0.1, 0.25)
    if kv > 0.01:
        RT.retrato(lz, 640, 960, 215 * (0.92 + 0.08 * k), "virrey", t, emocion="serio" if t < t_acep else "pensativo", habla=0.0, mirar=0.35, seed=5, alfa=kv)
    U.llamada(lz, 640, 150, "El virrey Iturrigaray", color=U.COL["rojo"], px=56, k=U.pop(t, t_vir) * U.salida(t, T_RICOS - 0.2), cola=None)
    # aceptó escuchar: ondas de sonido hacia el virrey y un regidor que habla (retrato pequeño)
    ke = U.pop(t, t_acep - 0.1) * U.salida(t, T_RICOS - 0.2)
    if ke > 0.01:
        MD.medallon(lz, 1400, 560, 150, "criollo", t, emocion="serio", habla=1.0, k=ke, seed=2)
        for i in range(4):
            u = ((t - t_acep) * 0.9 + i * 0.25) % 1.0
            lz.trazo(np.array([[1230 - 250 * u, 560 - 90 * u], [1230 - 250 * u, 560 + 90 * u]]) + 0 * 0, (255, 236, 170, int(255 * (1 - u))), 8, afinar=False, temblor=0.0, capa=2)
        U.llamada(lz, 1400, 760, "escuchar", color=U.COL["azul"], px=46, k=ke * U.repop(t, t_esc), cola="arriba")
    # los ricos españoles: tres retratos furiosos en fila + «¡TRAICIÓN!» (el virrey sale de escena)
    kr = U.pop(t, T_RICOS)
    if kr > 0.01:
        lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (60, 10, 40), alfa=0.9 * min(1.0, kr), capa=0)
        for i, (qn, px_, sh) in enumerate((("garibay", 330, 0), ("yermo", 960, 1), ("carlos", 1590, 2))):
            ki = U.pop(t, T_RICOS + 0.15 * i, 1.2)
            if ki > 0.01:
                RT.retrato(lz, px_, 1010, 150 * ki, qn, t, emocion="enojo", habla=0.3 if t > t_trai else 0.0, mirar=(i - 1) * 0.2, seed=20 + i, luz_borde=(255, 120, 90))
        U.titulo_grande(lz, t, t_trai - 0.1, T1(E3) - 18, "¡TRAICIÓN!", x=W / 2, y=240, px=170, color=(255, 90, 90))
        kk = U.pop(t, t_ricos) * U.salida(t, t_trai, 0.2)
        if kk > 0.01:
            U.llamada(lz, W / 2, 130, "ricos españoles", color=U.COL["naranja"], px=60, k=kk, cola=None)


# ------------------------------------------------------------------------------------------------ 7. EL ARRESTO DE NOCHE
def _soldado_antorcha(lz, iso, x, y, i, ent):
    G.persona(lz, iso, x, y, T_ACT[0], "granadero" if i % 2 else "yermo", dir=(-1, 0.3), vel=0.0 if ent > 0.98 else 1.0, seed=1300 + i, h=52, cara="enojo")
    O.antorcha(lz, iso, x + 6, y + 3, T_ACT[0], h=34, seed=i)
    sx, sy = iso.P(x + 6, y + 3, 52)
    lz.halo(float(sx), float(sy), 150 * iso.z / 3.0, (255, 168, 84), alfa=0.28, capa=2)


T_ACT = [0.0]


def cam_arr(t):
    return K(t, [(T_ARR, (300, 330, 30, 2.5)), (t_arr, (250, 140, 40, 3.3)), (t_mand, (290, 250, 20, 2.8)), (t_regr + 0.6, (400, 380, 10, 2.1))])


@shot(T_ARR, bg=lambda t: bg_grad((14, 16, 60), (62, 52, 120), mid=(34, 32, 96), ym=0.45), post=[lambda img, t: U.gradacion(img, luces=(1.0, 0.98, 1.04), sombras=(0.92, 0.94, 1.08), saturacion=1.04)], ent=("fundido", 0.5))
def p_arresto(lz, t):
    T_ACT[0] = t
    cx, cy, cz, zm = cam_arr(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.72, 0.78, 1.0), mix=(30, 34, 100), k=0.26)
    # cielo de noche: estrellas (con destellos de 4 puntas) y luna grande con halo
    for i in range(70):
        x, y = (h01(4, i, 1) * 2000) % 1920, (h01(4, i, 2) * 640)
        lz.relleno(circulo(x, y, 1.6 + 2.2 * h01(4, i, 3), 6), (255, 244, 210), alfa=0.45 + 0.4 * math.sin(t * 2 + i), capa=0)
    for i in range(6):
        U.chispa4(lz, (h01(5, i, 1) * 1900), (h01(5, i, 2) * 560), 8 + 6 * h01(5, i, 3), alfa=0.6 + 0.3 * math.sin(t * 3 + i), capa=0)
    lz.halo(1560, 170, 300, (150, 170, 255), alfa=0.35, capa=0)
    lz.relleno(circulo(1560, 170, 72, 28), (242, 246, 255), capa=0)
    lz.relleno(circulo(1536, 150, 14, 12), (214, 222, 244), capa=0)
    lz.relleno(circulo(1590, 192, 10, 10), (214, 222, 244), capa=0)
    PLZ.suelo(lz, iso, t, noche=1.0)
    m = PLZ.objetos(t, noche=1.0, farolas=1.0)
    ent = e_inout(prog(t, t_noche, t_arr - 0.3))
    for i in range(7):
        x = lerp(520, 170 + 20 * i, ent)
        y = 108 + 14 * i - 8 * (i % 2)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: _soldado_antorcha(lz, iso, x, y, i, ent)))(x, y, i), fijo=False, clave=x + y)
    sal = e_inout(prog(t, t_arr, t_mand + 0.2))
    vx, vy = lerp(250, 300, sal), lerp(76, 260, sal)
    m.add(vx - 4, vy - 4, vx + 4, vy + 4, 40, lambda lz, iso: G.persona(lz, iso, vx, vy, t, "pijama", dir=(0.3, 1), vel=0.0 if sal in (0.0, 1.0) else 1.0, seed=1350, h=54, accion="saluda" if (t_arr < t < t_arr + 0.9) else None, cara="miedo"), fijo=False, clave=vx + vy + 5)
    for j, dx in enumerate((-14, 14)):          # dos granaderos lo flanquean mientras sale
        m.add(vx + dx - 4, vy - 4, vx + dx + 4, vy + 4, 40, (lambda dx, j: (lambda lz, iso: G.persona(lz, iso, vx + dx, vy + 6, t, "granadero", dir=(0.3, 1), vel=0.0 if sal in (0.0, 1.0) else 1.0, seed=1360 + j, h=54, cara="enojo")))(dx, j), fijo=False, clave=vx + vy + 6)
    ck = e_in(prog(t, t_mand, t_regr + 0.8))
    cxx, cyy = lerp(320, 600, ck), lerp(300, 470, ck)
    m.add(cxx - 20, cyy - 10, cxx + 20, cyy + 10, 40, lambda lz, iso: O2.carruaje(lz, iso, cxx, cyy, t, mov=1.0 if ck > 0 else 0.0, color=(60, 56, 90), s=1.3), fijo=False, clave=cxx + cyy)
    m.dibujar(lz, iso)
    # ventanas del Palacio encendidas
    for i in range(10):
        qx, qy = iso.P(112 + 32 * i, 84, 30)
        lz.halo(float(qx), float(qy), 46 * iso.z / 3.0, (255, 214, 120), alfa=0.40, capa=2)
    DC.polvo_luz(lz, t, n=24, seed=9, color=(255, 214, 150), alfa=0.5)
    fecha = U.pop(t, t_noche - 0.2) * U.salida(t, t_regr)
    if fecha > 0.01:
        P.rotulo(lz, 430, 140, "15 de septiembre de 1808", px=60, k=fecha, color=(255, 255, 255))
    k = U.pop(t, t_arr) * U.salida(t, t_mand + 0.4)
    if k > 0.01:
        qx, qy = iso.P(vx, vy, 110)
        U.llamada(lz, float(qx), float(qy), "arrestado", color=U.COL["rojo"], px=52, k=k, cola="abajo")
    k = U.pop(t, t_mand)
    if k > 0.01:
        qx, qy = iso.P(cxx, cyy, 70)
        U.llamada(lz, float(qx), float(qy) - 20, "rumbo a España", color=U.COL["naranja"], px=46, k=k, cola="abajo")


# ------------------------------------------------------------------------------------------------ 8. GOLPE DE ESTADO (A: el Palacio es tomado)
T_PODER = t_dem - 0.2


def cam_golpe(t):
    return K(t, [(T_GOLPE, (260, 104, 40, 3.5)), (t_dem, (260, 96, 50, 4.0)), (T_PODER, (260, 94, 54, 4.2)), (t_camb2, (260, 94, 56, 4.3)), (t_fuerza, (260, 96, 56, 4.2)), (T1(E3), (260, 104, 52, 3.7))])


XB = (170, 230, 290, 350)          # posiciones de los cuatro del relevo en el balcón (separados 60 unidades)


@shot(T_GOLPE, bg=lambda t: bg_grad((100, 30, 60), (44, 20, 80), mid=(70, 26, 80), ym=0.5), post=[GRAD], ent=("destello", 0.5))
def p_golpe(lz, t):
    sh = 0.0
    if t_golpe < t < t_golpe + 0.6:
        sh = 12 * (1 - (t - t_golpe) / 0.6)
    cx, cy, cz, zm = cam_golpe(t)
    with lz.grupo(sh * math.sin(t * 90), sh * math.cos(t * 77), 1.0):
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
        I.luz(mul=(1.0, 0.92, 0.92), mix=(120, 40, 60), k=0.14)
        U.haces_luz(lz, W / 2, 400, t, n=10, largo=1500, color=(255, 120, 130), alfa=0.10, ancho=0.07)
        PLZ.suelo(lz, iso, t)
        m = PLZ.objetos(t)
        # los soldados toman el balcón por los dos extremos
        entra = e_inout(prog(t, t_golpe, t_estado + 0.4))
        for i, (x, lado) in enumerate(((110, -1), (136, -1), (404, 1), (378, 1))):
            m.add(x - 4, 74, x + 4, 82, 40, (lambda x, i, lado: (lambda lz, iso: G.persona(lz, iso, lerp(x + lado * 90, x, entra), 84, t, "granadero", dir=(0, 1), vel=0.0 if entra > 0.98 else 1.0, seed=1500 + i, h=52, z=40, cara="enojo", accion="vitorea" if t > t_dem else None)))(x, i, lado), fijo=False, clave=x + 90)
        # el relevo del poder: Iturrigaray -> Yermo -> Garibay -> Calleja
        quienes = (("pijama", "miedo"), ("yermo", "enojo"), ("virrey", "serio"), ("dragon", "enojo"))
        tt = [t_pod2 - 0.1, t_camb2 + 0.1, t_manos - 0.2, t_fuerza + 0.4]
        for i, (tp_, emo) in enumerate(quienes):
            ki = 1.0 if i < 2 else e_back(prog(t, tt[i - 1] - 0.15, tt[i - 1] + 0.3))
            if ki > 0.01:
                x = XB[i]
                m.add(x - 4, 74, x + 4, 82, 40, (lambda tp_, x, emo, ki, i: (lambda lz, iso: G.persona(lz, iso, x, 84, t, tp_, dir=(0, 1), seed=1600 + i, h=56 * ki, z=40, cara=emo, accion="habla" if (i == 1 and t > t_camb2) else None)))(tp_, x, emo, ki, i), fijo=False, clave=x + 91)
        # cetro de mando con arcos y destellos entre las manos
        seg = 0
        while seg < 3 and t > tt[seg]:
            seg += 1
        a0 = XB[max(0, seg - 1)]
        a1 = XB[seg]
        u = prog(t, tt[max(0, seg - 1)], tt[max(0, seg - 1)] + 0.55) if seg > 0 else 0.0
        xs = lerp(a0, a1, e_inout(u)) if seg > 0 else XB[0]
        zs = 58 + 40 * math.sin(math.pi * u) if seg > 0 else 58
        m.add(xs - 3, 80, xs + 3, 88, 60, lambda lz, iso: _cetro(lz, iso, xs, 90, zs, t), fijo=False, clave=xs + 95)
        m.dibujar(lz, iso)
        bx, by = 262, 72
        k_b = e_inout(prog(t, t_estado, t_estado + 0.9))
        O.bandera(lz, iso, bx, by, h=110 * max(0.2, k_b), w=50, alto=32, color=(206, 56, 70), t=t, franjas=[((206, 56, 70), 0.25), ((250, 206, 90), 0.5), ((206, 56, 70), 0.25)])
        DC.aves(lz, t, n=8, seed=11, y0=60, y1=240)
        kg = U.pop(t, t_golpe - 0.1, 1.2) * U.salida(t, t_dem + 0.3, 0.3)
        if kg > 0.01:
            P.rotulo(lz, W / 2, 150, "GOLPE DE ESTADO", px=170, k=kg, color=(255, 255, 255))
        k = U.pop(t, t_fuerza - 0.2)
        if k > 0.01:
            U.llamada(lz, W / 2, 980, "por la fuerza", color=U.COL["rojo"], px=84, k=k * U.repop(t, t_fuerza + 0.3), cola=None)
        for i, (lab, col) in enumerate((("Iturrigaray", U.COL["rojo"]), ("Yermo", U.COL["morado"]), ("Garibay", U.COL["azul"]), ("Calleja", U.COL["naranja"]))):
            t0 = t_pod2 - 0.1 if i < 2 else tt[i - 1] + 0.1
            kk = U.pop(t, t0 + (0.0 if i == 0 else 0.25)) * U.salida(t, T1(E3) - 0.2, 0.2)
            if kk > 0.01:
                qx, qy = iso.P(XB[i], 84, 118)
                U.llamada(lz, float(qx), float(qy) - 6 - 92 * (i % 2), lab, color=col, px=32, k=kk, cola="abajo")


def _cetro(lz, iso, x, y, z, t):
    sx, sy = iso.P(x, y, z)
    k = iso.z
    lz.halo(sx, sy - 12 * k, 30 * k, (255, 230, 140), alfa=0.55, capa=2)
    lz.relleno(rect_red(sx - 1.8 * k, sy - 22 * k, 3.6 * k, 26 * k, 1.6 * k), tint((250, 206, 70)))
    lz.relleno(circulo(sx, sy - 24 * k, 4.6 * k, 12), tint((250, 206, 70)))
    lz.relleno(circulo(sx, sy - 24 * k, 2.4 * k, 8), tint((214, 52, 70)))
    for j in range(5):
        a = t * 3 + j
        U.chispa4(lz, sx + 12 * k * math.cos(a), sy - 12 * k + 12 * k * math.sin(a), 5 * k, alfa=0.8)


# ------------------------------------------------------------------------------------------------ sonido
snd(T0(E3) + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_oc, "ola", 0.3, dur=1.4)
snd(t_algo, "trueno", 0.5)
snd(T_INV, "whoosh", 0.35, dur=0.8)
snd(t_nap, "pluck", 0.5)
for _k in range(4):
    snd(t_inv + 0.35 * _k, "tambor", 0.3)
snd(t_esp, "canonazo", 0.5)
snd(T_ABD, "pop", 0.4)
snd(t_abd, "gong", 0.4)
snd(T_TRONO, "bling", 0.5)
snd(t_herm + 0.5, "pluck", 0.5)
snd(t_pris - 0.1, "gong", 0.45)
snd(T_AYU, "whoosh", 0.3, dur=1.2)
snd(t_prop, "pop", 0.4)
snd(t_inau, "pluck", 0.5)
snd(t_sinrey + 0.4, "crujido", 0.4)
snd(t_pueblo, "bling", 0.5)
snd(T_VIR, "pop", 0.4)
snd(t_grupo, "tambor", 0.4)
snd(t_trai, "gong", 0.6)
snd(t_noche, "amanecer", 0.3, dur=2.0)
snd(t_arr, "pop", 0.5)
snd(t_mand, "galope", 0.4, dur=1.5)
snd(t_golpe, "canonazo", 0.6)
snd(t_pod2, "bling", 0.4)
snd(t_camb2 + 0.2, "bling", 0.4)
snd(t_manos, "bling", 0.4)
snd(t_fuerza, "gong", 0.55)
