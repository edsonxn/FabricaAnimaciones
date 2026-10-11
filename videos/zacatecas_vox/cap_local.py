# -*- coding: utf-8 -*-
"""Escenografía local compartida (cielo, cerros, suelo) y capítulos `cerro` y `campamento`."""
import math

import numpy as np

import locales as L
import subsuelo as S
import ui_vox as U
import vox as V
from ctx import LOC, T, INI, FIN, lerp_color
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

FIG = 0.32          # escala de las personas en unidades locales (~105 de alto)
MUL = 0.34          # escala de las mulas
SUR = 130           # profundidad de la capa de tierra donde caminan las personas (y del corte de la mina)

A = dict(
    indig=T("cerro", "indígenas"), tolosa=T("cerro", "Tolosa"), piedras=T("cerro", "piedras"),
    brill=T("cerro", "brillantes"), mas=T("cerro", "más"), llega=T("cerro", "llega"), odre=T("cerro", "odre"),
    bufa=T("cerro", "Bufa"), arma=T("cerro", "arma"), camp=T("cerro", "campamento"),
    ocho=T("cerro", "ocho", frase=3), veta=T("cerro", "veta"), bernabe=T("cerro", "Bernabé"),
    fiebre=T("cerro", "fiebre"), plata1=T("cerro", "plata", frase=3),
    # campamento
    c49=T("campamento", "nueve"), tres=T("campamento", "trescientas"), casas=T("campamento", "casas"),
    minas=T("campamento", "minas", frase=1), arroyo=T("campamento", "arroyo"), laderas=T("campamento", "laderas"),
    caro=T("campamento", "caro"), maiz=T("campamento", "maíz"), carne=T("campamento", "carne"),
    ranch=T("campamento", "rancherías"), aun=T("campamento", "Aun"), c50=T("campamento", "cincuenta"),
    t34=T("campamento", "treinta"), minas34=T("campamento", "minas", frase=3),
    hosp=T("campamento", "hospitales"), cfin=FIN("campamento"),
)


def alfa_local(z):
    u = clamp01((math.log(max(z, 1e-6)) - math.log(1.6)) / (math.log(5.0) - math.log(1.6)))
    return smooth(u)


def base_local(lz, t, cam_l, hora, alfa=1.0, sol_pos=(-300, -720)):
    """Sol + nubes + cerros lejanos + sierra de la Bufa + suelo (el degradado del cielo va en el fondo de pantalla)."""
    if alfa <= 0.01:
        return
    if isinstance(hora, str) and hora != "noche":
        L.sol(lz, sol_pos[0] + cam_l[0] * 0.05, sol_pos[1] + cam_l[1] * 0.05, 74, t, alfa=alfa)
    for i, (nx, ny, s) in enumerate([(-500, -1000, 1.2), (250, -1180, 0.9), (700, -900, 1.0), (-900, -820, 0.8)]):
        L.nube(lz, nx + (26 * t * 0.3) % 1200 - 200 + cam_l[0] * 0.08, ny + cam_l[1] * 0.08, s * 1.4, alfa=alfa, capa=0,
               color=(252, 248, 240))
    L.colinas_fondo(lz, cam_l[0], 0.3, -180, 520, 1.0, (206, 172, 190), -14000, 14000, alfa=alfa, cam_y=cam_l[1], paso=170)
    L.colinas_fondo(lz, cam_l[0], 0.6, -40, 360, 3.0, (196, 146, 138), -14000, 14000, alfa=alfa, cam_y=cam_l[1], paso=130)
    a3 = alfa ** 3        # el terreno solo aparece con firmeza cuando el mapa ya se desvaneció
    L.subsuelo_base(lz, a3)
    L.montaña_bufa(lz, alfa=a3)
    L.suelo(lz, -20000, 20000, SUR, alfa=a3)


# ------------------------------------------------------------------ casas del campamento
# (x, tipo, fila, semilla)   tipo: t=tienda, c=choza, a=adobe
CASAS = [(40, "t", 0, 1), (130, "t", 1, 2), (-50, "t", 1, 3), (200, "c", 0, 4), (-120, "c", 0, 5), (260, "a", 1, 6),
         (-190, "a", 1, 7), (-30, "a", 0, 8), (95, "a", 0, 9), (320, "c", 1, 10), (-260, "c", 0, 11), (170, "a", 2, 12),
         (-90, "a", 2, 13), (360, "a", 0, 14), (-330, "a", 1, 15), (10, "c", 2, 16), (290, "a", 2, 17), (-160, "c", 2, 18)]


CAMP_DX = 150.0


def casa_en(lz, t, x, tipo, fila, seed, t0, escala=1.0, humo=True):
    k = prog(t, t0, t0 + 0.45)
    if k <= 0:
        return
    x = x + CAMP_DX
    y = float(L.h(x)) + 26 + 42 * fila
    s = 1.65 * (1 + 0.1 * fila) * escala
    if tipo == "t":
        L.tienda(lz, x, y, s * 0.95, k, seed)
    elif tipo == "c":
        L.choza(lz, x, y, s, k, seed)
    else:
        L.casa_adobe(lz, x, y, s, k, seed)
        if humo and k >= 1 and seed % 2 == 0:
            L.humo(lz, x + 16 * s, y - 94 * s, t + seed, 4, esc=s * 0.9, alfa=0.55)


def bocamina(lz, x, y, s=1.0, k=1.0, t=0.0, seed=0):
    """Marco de madera de una mina con polea (aparece con rebote)."""
    kk = 0 if k <= 0 else (e_back(clamp01(k), 1.8) if k < 1 else 1)
    if kk <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * kk):
        lz.relleno(np.array([[-46, 0], [-46, -6], [46, -6], [46, 0]]), (60, 46, 40), temblor=0.0, capa=1)
        lz.relleno(np.array([[-36, 0], [0, -110], [36, 0], [24, 0], [0, -70], [-24, 0]]), L.MADERA, temblor=0.0, capa=1)
        lz.relleno(rect_red(-30, -60, 60, 10, 3), V.oscurecer(L.MADERA, 0.15), temblor=0.0, capa=1)
        lz.relleno(V.elipse_pts(0, -104, 14, 14), (90, 70, 60), temblor=0.0, capa=1)
        lz.trazo(np.array([[0, -110], [0, -150]]), (70, 50, 40), 4, afinar=False, temblor=0.0, capa=1)
        lz.relleno(np.array([[0, -150], [34, -140], [0, -128]]), V.ROJO, temblor=0.0, capa=1)
        lz.relleno(np.array([[-14, 0], [14, 0], [14, -30], [-14, -30]]), (30, 24, 28), temblor=0.0, capa=1)


