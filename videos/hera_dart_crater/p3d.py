# -*- coding: utf-8 -*-
"""Piezas 3D compartidas por los planos: el sistema doble en METROS (Didymos en el origen, Dimorphos en órbita),
cámaras de órbita, curva de luz y diagramas de órbita alrededor del Sol (en otra escala)."""
import math

import numpy as np

from comun import E, H, W, L3, Cam, ap, circulo3d, clamp, e_inout, e_out, etiqueta3d, lerp, nrm, pr, smooth

X, Y, Z = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
O = np.zeros(3)
SOL = nrm(np.array([1.0, -0.55, 0.35]))     # dirección de la luz del Sol (fija en todos los planos del sistema)

R_DID = 390.0          # radio medio de Didymos (diámetro ~780 m), metros
DIM_EJES = (1.0, 0.98, 0.66)
R_DIM = 88.0           # semieje mayor de Dimorphos antes del choque (177 × 174 × 116 m)
R_ORB = 1190.0         # distancia entre centros (~1,19 km)
P_ANTES = 11 * 3600 + 55 * 60
P_DESPUES = 11 * 3600 + 23 * 60


def cam_orb(foco, dist, az, el, fov=40, centro=None, cerca=0.5):
    a, e = math.radians(az), math.radians(el)
    d = math.cos(e) * (math.sin(a) * X - math.cos(a) * Y) + math.sin(e) * Z
    return Cam(np.asarray(foco, np.float64) + d * dist, np.asarray(foco, np.float64), Z, fov, cerca=cerca, centro=centro)


def pos_dim(ang_deg, r=R_ORB):
    a = math.radians(ang_deg)
    return np.array([r * math.cos(a), r * math.sin(a), 0.0])


def didymos(lz, t, op=1.0, rocas=160, C=O, giro=1.0):
    """Didymos gira cada ~2,26 h: en pantalla, despacio."""
    return E.asteroide(lz, C, R_DID, forma="trompo", rot=E.rot_ypr(t * 6.0 * giro, 0, 0), sol=SOL, rocas=rocas, semilla=4, op=op)


def dimorphos(lz, P, op=1.0, despues=False, rocas=220, yaw=0.0, pitch=0.0, roll=0.0, esc=1.0, crater_r=0.62):
    if despues:      # alargado, con la cara del choque aplanada y el cráter (dirección local -y)
        return E.asteroide(lz, P, R_DIM * esc, ejes=(1.18, 0.9, 0.6), rot=E.rot_ypr(yaw, pitch, roll), sol=SOL, rocas=rocas,
                           semilla=7, crater=(0, -1, 0.05), aplanar=0.2, crater_r=crater_r, crater_prof=0.12, op=op)
    return E.asteroide(lz, P, R_DIM * esc, ejes=DIM_EJES, rot=E.rot_ypr(yaw, pitch, roll), sol=SOL, rocas=rocas, semilla=7, op=op)


def orbita(lz, op=0.5, r=R_ORB, guion=3, w=1.0, a0=0.0, a1=2 * math.pi):
    lz.linea(circulo3d(O, Z, r, 180, a0, a1), op, w, guion=guion)


def flecha3d(lz, P0, P1, op=1.0, w=1.6, cab=0.12):
    P0, P1 = np.asarray(P0, np.float64), np.asarray(P1, np.float64)
    lz.linea(np.array([P0, P1]), op, w)
    d = P1 - P0
    L = np.linalg.norm(d)
    if L < 1e-9:
        return
    d /= L
    v = nrm(np.cross(d, lz.cam.pos - P1))
    lz.linea(np.array([P1 - d * L * cab + v * L * cab * 0.6, P1, P1 - d * L * cab - v * L * cab * 0.6]), op, w)


def reloj(lz, x, y, seg, op=1.0, px=96, rotulo=None):
    h = int(seg // 3600)
    m = int(round((seg - h * 3600) / 60))
    lz.texto(f"{h} H {m:02d} MIN", x, y, px, "Bold Condensed", op, "mm", esp=0.03)
    if rotulo:
        lz.texto(rotulo, x, y + px * 0.66, 24, "SemiBold Condensed", op * 0.9, "mm", esp=0.18)


# ------------------------------------------------------------------ Sistema Solar esquemático (UA)
def orbita_planeta(lz, a_ua, op=0.4, w=1.0, e=0.0, varpi=0.0, guion=None):
    th = np.linspace(0, 2 * math.pi, 240)
    r = a_ua * (1 - e * e) / (1 + e * np.cos(th - varpi))
    lz.linea(np.stack([r * np.cos(th), r * np.sin(th), np.zeros_like(th)], -1), op, w, guion=guion)


def pos_planeta(a_ua, ang_deg, e=0.0, varpi=0.0):
    th = math.radians(ang_deg)
    r = a_ua * (1 - e * e) / (1 + e * math.cos(th - varpi))
    return np.array([r * math.cos(th), r * math.sin(th), 0.0])


def sol(lz, op=1.0):
    lz.puntos(O, r=7, op=op)
    for k in range(12):
        a = k * math.pi / 6
        x, y = lz.cam.px(O)
        if np.isfinite(x):
            lz.l2([(x + 12 * math.cos(a), y + 12 * math.sin(a)), (x + 22 * math.cos(a), y + 22 * math.sin(a))], op * 0.8, 1.2)
