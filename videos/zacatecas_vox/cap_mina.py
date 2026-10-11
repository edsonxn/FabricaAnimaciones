# -*- coding: utf-8 -*-
"""Capítulo `mina`: descenso por el pozo, barreta y vela, cargadores por las escalas de troncos, tarjetas de trabajo."""
import math

import numpy as np

import locales as L
import subsuelo as S
import ui_vox as U
import vox as V
from cap_local import FIG, SUR, bocamina
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

FM = 0.46               # escala de las personas dentro de la mina
A = dict(
    ini=INI("mina"), fin=FIN("mina"),
    bajo=T("mina", "Bajo"), brutal=T("mina", "brutal"),
    cavan=T("mina", "cavan"), barreta=T("mina", "barreta"), vela=T("mina", "vela"),
    carg=T("mina", "cargadores"), espalda=T("mina", "espalda"), escalas=T("mina", "escalas"),
    pueblos=T("mina", "pueblos"), obligar=T("mina", "obligar"),
    llegan=T("mina", "llegan"), parte=T("mina", "parte"),
    esclav=T("mina", "esclavizados"), noventa=T("mina", "noventa"), doscientos=T("mina", "doscientos"),
)
Y_G1, Y_G2, Y_G3 = 900.0, 1500.0, 2200.0
T_CLIMB0 = A["carg"] + 0.6
T_CLIMB1 = A["fin"] - 0.2


def u_escalera(t, off=0.0):
    return clamp01((t - T_CLIMB0) / (T_CLIMB1 - T_CLIMB0) + off)


def pos_cargador(t):
    """Posición absoluta (local) del cargador principal."""
    p, d, k = S.punto_escalera(u_escalera(t))
    return p[0], p[1] + SUR, d


def camara_pos(t):
    """Centro de cámara local que sigue la acción de la mina. Devuelve (lx, ly, zl)."""
    t_g1 = A["ini"] + 1.7                       # llega a la galería 1
    t_f0, t_f1 = A["carg"] - 0.5, A["carg"] + 1.5   # caída a la galería 3
    if t < t_g1:
        u = e_inout(prog(t, A["ini"], t_g1))
        return lerp(-40, -250, u), lerp(SUR + 60, SUR + Y_G1 - 40, u), lerp(1.5, 1.6, u)
    if t < t_f0:
        return -250, SUR + Y_G1 - 40, 1.6
    if t < t_f1:
        u = e_inout(prog(t, t_f0, t_f1))
        return lerp(-250, -40, u), lerp(SUR + Y_G1 - 40, SUR + Y_G3 - 100, u), lerp(1.6, 1.5, u)
    x, y, d = pos_cargador(t)
    return -40, y - 150, 1.5


def dibujar(lz, t, tc, cam_l):
    """Dibuja el subsuelo completo (si la cámara lo ve). Origen local: superficie; coordenadas relativas a SUR."""
    ly, zl = cam_l[1], cam_l[2] if len(cam_l) > 2 else 1.0
    with lz.grupo(0, SUR):
        S.seccion(lz, -380, 380, oscuridad=0.0)
        S.veta(lz, t, hasta=1.0)
        lz.trazo(np.array([[-380, 0], [380, 0], [380, 3450], [-380, 3450]]), V.CREMA, 9, cerrado=True, afinar=False, temblor=0.0, capa=1)
        S.pozo(lz, 0, 2800)
        S.galeria(lz, Y_G1, -380, -40, 160)
        S.galeria(lz, Y_G2, -40, 320, 160)
        S.galeria(lz, Y_G3, -380, 320, 160)
        S.escaleras(lz)
        # sombra de profundidad: una sola capa oscura cuyo grosor crece con la profundidad de la cámara
        osc = 0.5 * smooth(clamp01((cam_l[1] - SUR - 300) / 1500.0))
        if osc > 0.01:
            lz.relleno(np.array([[-2500, 0], [2500, 0], [2500, 3600], [-2500, 3600]]), (10, 8, 14), temblor=0.0, capa=2, alfa=osc)
        # velas
        for (vx, vy, sd) in [(-330, Y_G1 - 70, 1), (-80, Y_G3 - 70, 2), (200, Y_G3 - 70, 3), (240, Y_G2 - 70, 4)]:
            S.luz_vela(lz, vx, vy, 230, t, seed=sd)
            lz.relleno(rect_red(vx - 5, vy - 6, 10, 30, 3), (250, 244, 224), temblor=0.0, capa=1)
            lz.relleno(np.array([[vx, vy - 34], [vx + 8, vy - 12], [vx, vy - 6], [vx - 8, vy - 12]]), V.NARANJA, temblor=0.0, capa=1)
        # minero con barreta (galería 1, mirando a la izquierda)
        f = V.cuadro(V.PICAR, t, 7.5, A["cavan"] - 0.3)
        yy = Y_G1 + 3
        with lz.grupo(0, 0):
            V.figura(lz, -300, yy, FM, V.PICAR[f], "minero", -1, obj=[("d", "barreta", 0, 1.0)], seed=11)
        # chispas al golpear (cuadros 3 y 4)
        if f in (3, 4):
            for i in range(6):
                a = -math.pi + 0.5 + i * 0.35
                r = 20 + 22 * (f - 2) + 6 * i
                lz.puntos([(-378 + 36 * math.cos(a) * 0.6 + 6, yy - 34 + 30 * math.sin(a) - r * 0.3)], 3.4, (255, 226, 140), capa=2)
        # otros mineros en la galería 3 (llenan cestos) y cargador del pozo
        f2 = V.cuadro(V.PICAR, t + 0.3, 7.5)
        V.figura(lz, -230, Y_G3 + 3, FM, V.PICAR[f2], "cargador", -1, obj=[("d", "pico", 0, 0.9)], seed=21)
        V.figura(lz, 140, Y_G3 + 3, FM, V.IDLE[int(t * 2.2) % 2], "minero", -1, seed=22)
        S.mineral(lz, 60, Y_G3 + 3, 0.9, plata=True)
        S.mineral(lz, -160, Y_G3 + 3, 0.9)
        # cargadores en las escalas: varios en fila con distinto avance
        for k, off in enumerate([0.0, 0.16, 0.34, -0.14]):
            u = clamp01((t - T_CLIMB0) / (T_CLIMB1 - T_CLIMB0) + off) if off != 0 else u_escalera(t)
            if u <= 0 or u >= 1 and k > 0:
                continue
            p, d, seg = S.punto_escalera(u if k == 0 else clamp01(u))
            fr = V.cuadro(V.SUBIR, t, 15.0, 0.13 * k)
            V.figura(lz, p[0], p[1], FM, V.SUBIR[fr], ("cargador", "africano", "indigena", "minero")[k], d,
                     carga=("tenate", 1.0), seed=30 + k)
