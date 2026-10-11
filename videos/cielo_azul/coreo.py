# -*- coding: utf-8 -*-
"""¿Por qué el cielo es azul?: gancho, blanca, dispersion, violeta, atardecer, marte, cierre."""
import math

import cv2
import numpy as np

import sh_kit as K
import sh_props as X
import sh_pintura as P
from sh_motor import FIN, INI, T, escena
from sh_util import balistica, bump, estela, kf, pulso
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

pi = math.pi
BW, BH, MX, MY = P.BW, P.BH, P.MX, P.MY
CREMA = (255, 250, 232)
AZUL_T = (70, 130, 240)
VIOLETA_T = (160, 100, 230)
NARANJA = (255, 150, 70)
ORO = (255, 230, 120)
COL_ONDA = {"violeta": (150, 90, 240), "azul": (70, 140, 250), "rojo": (240, 70, 70)}


def capas_cielo(seed, c0, c1, colinas=True, col_c=((118, 196, 120), (96, 176, 110))):
    far = P.fondo_liso(seed, c0, c1, [(520, 0.7, tuple(min(255, int(a * 0.9 + b * 0.1)) for a, b in zip(c0, c1)), .5),
                                       (300, 1.2, tuple(min(255, int(v * 1.1)) for v in c1), .4), (220, 1.6, (255, 255, 255), .22)])
    cap = [(far, 0.25)]
    if colinas:
        h1 = P.vacio()
        P.mancha(h1, 300, BH - 200, 700, 280, col_c[0], seed + 1, rough=0.06)
        P.mancha(h1, 900, BH - 160, 760, 260, col_c[1], seed + 2, rough=0.06)
        P.textura(h1, 0.02, 0.04)
        cap += [(h1, 1.0)]
    return cap


def cielo_azul():
    return capas_cielo(5, (70, 150, 246), (170, 216, 255))


def cielo_violeta():
    return capas_cielo(5, (120, 70, 220), (200, 160, 250))


def cielo_atardecer():
    return capas_cielo(11, (250, 100, 70), (255, 214, 120), col_c=((90, 60, 100), (70, 46, 90)))


def cam_suave(C, t, a, b, z=0.05):
    u = (t - a) / max(1e-6, b - a)
    C.cam = (1.0 + z * u, 8 * math.sin(t * 0.7), -10 * math.cos(t * 0.5))


def sol(img, x, y, t, r=110, col=(255, 236, 130)):
    P.halo(img, x, y, r * 3.4, col, 0.55, 6)
    P.rayos(img, x, y, r, r * 2.2, 14, t * 0.3, [col], 0.5, 0.4)
    P.disco(img, x, y, r, col, 1.0)


def mezclar(a, b, u):
    return (a.astype(np.float32) * (1 - u) + b.astype(np.float32) * u).astype(np.uint8)


def en_camino(pts, u):
    """Posición y ángulo sobre una polilínea (u 0..1)."""
    pts = np.asarray(pts, float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    s = u * d[-1]
    i = min(len(seg) - 1, int(np.searchsorted(d, s, side="right") - 1))
    f = (s - d[i]) / max(1e-6, seg[i])
    p = pts[i] + (pts[i + 1] - pts[i]) * f
    ang = math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
    return p, ang


def onda(img, p, ang, col, largo=140, amp=14, lam=34, t=0.0, g=6):
    estela(img, p[0], p[1], ang, largo, amp, lam, t * 12, col, g, cabeza=False)


# ------------------------------------------------------------------ 1. gancho
@escena("gancho")
def gancho(C, t):
    t0 = INI("gancho")
    t_no, t_viol = T("gancho", "azul"), T("gancho", "violeta", frase=1)
    ca = C.capas_de("azul", cielo_azul)
    cv_ = C.capas_de("violeta", cielo_violeta)
    cam_suave(C, t, t0, FIN("gancho"))
    C.fondo(np.zeros((H, W, 3), np.uint8))
    img = C.base("gancho", ca)
    u = e_inout(prog(t, t_viol - 0.2, t_viol + 0.8))
    if u > 0.01:
        C.cam = (C.cam[0], C.cam[1], C.cam[2])
        img = mezclar(img, C.base("gancho2", cv_), u)
    sol(img, *C.xy(880, 270), t)
    C.fondo(img)
    C.pon(X.nube("grandes", "sonrisa"), 220, 560 + 12 * math.sin(t * 1.3), 0.9, 0.0, t_in=t0 + 0.3, vida=1.0)
    C.pon(X.nube("grandes", "sonrisa"), 800, 760 + 14 * math.sin(t * 1.1), 0.7, 0.0, t_in=t0 + 0.5, vida=1.0)
    C.pon(K.persona("grandes" if t < t_viol else "miedo", "o" if t < t_viol else "grito", "arriba"), 540, 1450, 1.9, 0.0, t_in=t0 + 0.1, vida=1.0 + 1.5 * (t > t_viol))
    C.rot("EL CIELO", 540, 270, 130, -0.04, CREMA, t_in=t0 + 0.4, dur=0.3, t_out=t_viol - 0.1, d_out=0.2)
    C.rot("NO ES AZUL", 540, 420, 130, 0.03, (255, 100, 100), t_in=t_no, dur=0.3, tira=True, t_out=t_viol - 0.1, d_out=0.2)
    C.rot("¡ES VIOLETA!", 540, 330, 130, -0.03, VIOLETA_T, t_in=t_viol, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 2. luz blanca
RAINBOW = [(240, 60, 70), (255, 150, 60), (255, 230, 80), (110, 210, 100), (80, 160, 250), (100, 90, 220), (170, 100, 230)]


@escena("blanca")
def blanca(C, t):
    t0 = INI("blanca")
    t_bl, t_col = T("blanca", "blanca"), T("blanca", "colores")
    capas = C.capas_de("noche", lambda: capas_cielo(15, (14, 18, 54), (60, 50, 120), colinas=False))
    cam_suave(C, t, t0, FIN("blanca"))
    img = C.base("blanca", capas)
    px, py = C.xy(560, 860)
    # rayo blanco que entra por la izquierda
    tx = C.xy(150, 520)
    sol(img, tx[0], tx[1], t, 90)
    cv2.line(img, (int(tx[0] * 4), int(tx[1] * 4)), (int((px - 60) * 4), int((py - 10) * 4)), (255, 255, 255), 22, cv2.LINE_AA, 2)
    # abanico de colores a la salida del prisma
    k = e_out(prog(t, t_col - 0.2, t_col + 0.8))
    for i, c in enumerate(RAINBOW):
        a = -0.34 + i * 0.1
        L = 900 * k
        p1 = (px + 40, py + 20)
        p2 = (p1[0] + L * math.cos(a), p1[1] + L * math.sin(a) + 160 * k)
        p3 = (p2[0] - 40 * math.sin(a), p2[1] + 40 * math.cos(a))
        P.poligono(img, [p1, p2, p3], c, 0.95)
    C.fondo(img)
    C.pon(X.prisma(), 560, 860, 2.0, 0.0, t_in=t0 + 0.1, vida=0.6)
    C.rot("LUZ BLANCA", 540, 300, 140, -0.03, CREMA, t_in=t_bl, dur=0.3, tira=True)
    C.rot("¡TODOS LOS COLORES!", 540, 1500, 84, 0.03, (255, 236, 120), t_in=t_col, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 3. dispersión
@escena("dispersion")
def dispersion(C, t):
    t0 = INI("dispersion")
    t_azul = T("dispersion", "azul")
    t_rojo = T("dispersion", "rojo", frase=1)
    capas = C.capas_de("azul2", cielo_azul)
    cam_suave(C, t, t0, FIN("dispersion"))
    img = C.base("dispersion", capas)
    C.fondo(img)
    # moléculas del aire (con cara) por toda la pantalla
    mol = [(220, 600), (520, 520), (800, 700), (330, 900), (640, 960), (900, 1010), (200, 1200), (500, 1300), (780, 1380), (360, 1560), (680, 1620), (130, 800)]
    for i, (x, y) in enumerate(mol):
        d = K.quark(("verde", "azul", "rojo")[i % 3], "grandes", "sonrisa")
        C.pon(d, x + 14 * math.sin(t * 1.2 + i), y + 12 * math.cos(t * 1.4 + i), 2.3, 0.0, t_in=t0 + 0.05 * i, modo="pop", dur=0.25, vida=0.7)
    C.rot("AL CHOCAR CON EL AIRE", 540, 270, 70, -0.02, CREMA, t_in=t0 + 0.3, dur=0.3, tira=True)
    out = C.fin()
    # ondas: azul y violeta rebotan por todas partes; la roja pasa de largo
    rutas = {"violeta": [(80, 420), (330, 640), (150, 900), (500, 1000), (300, 1260), (700, 1380), (480, 1640)],
             "azul": [(80, 500), (520, 560), (400, 820), (860, 900), (640, 1180), (900, 1420), (760, 1700)],
             "rojo": [(80, 560), (1000, 1480)]}
    for nombre, pts in rutas.items():
        for rep in range(3 if nombre != "rojo" else 2):
            u = ((t - t0) * 0.28 + rep / (3 if nombre != "rojo" else 2)) % 1.0
            p, ang = en_camino(pts, u)
            onda(out, p, ang, COL_ONDA[nombre], 260, 24, 56, t, 15)
    out = out
    return out if True else out


# ------------------------------------------------------------------ 4. violeta
@escena("violeta")
def violeta(C, t):
    t0 = INI("violeta")
    t_men, t_abs, t_oj = T("violeta", "menos"), T("violeta", "absorbe"), T("violeta", "ojos")
    t_gana = T("violeta", "gana", frase=1)
    capas = C.capas_de("noche2", lambda: capas_cielo(23, (30, 24, 80), (96, 60, 150), colinas=False))
    cam_suave(C, t, t0, FIN("violeta"))
    img = C.base("violeta", capas)
    C.fondo(img)
    if t < t_men - 0.4:
        C.pon(X.bola_cara((160, 100, 230), 80, "grandes", "triste"), 540, 1000, 3.4, 0.0, t_in=t0 + 0.1, vida=1.0)
        C.rot("¿Y EL VIOLETA?", 540, 330, 120, -0.03, VIOLETA_T, t_in=t0 + 0.3, dur=0.3, tira=True, t_out=t_men - 0.4, d_out=0.2)
    razones = [("EL SOL DA\nMENOS VIOLETA", t_men, 560, "sol"), ("LA ATMÓSFERA\nSE LO ABSORBE", t_abs, 960, "nube"), ("TUS OJOS LO\nVEN PEOR", t_oj, 1360, "ojo")]
    for txt, tt, y, ic in razones:
        if t_gana - 0.2 > t >= tt - 0.2:
            if ic == "sol":
                C.pon(X.sol_disco(70, 1.0), 220, y, 1.4, t * 0.2, t_in=tt - 0.2, dur=0.3)
            elif ic == "nube":
                C.pon(X.nube("grandes", "o", True), 230, y, 0.62, 0.0, t_in=tt - 0.2, dur=0.3, vida=0.8)
            else:
                C.pon(X.ojo(0.4 * math.sin(t * 2), 0.0), 220, y, 0.95, 0.0, t_in=tt - 0.2, dur=0.3, vida=0.6)
            a, b = txt.split("\n")
            C.rot(a, 640, y - 40, 62, -0.02, CREMA, t_in=tt, dur=0.3, t_out=t_gana - 0.2, d_out=0.2, tira=True)
            C.rot(b, 640, y + 50, 70, 0.02, VIOLETA_T if ic != "ojo" else (255, 150, 90), t_in=tt + 0.2, dur=0.3, t_out=t_gana - 0.2, d_out=0.2)
    if t >= t_gana:
        C.pon(X.medalla("1"), 540, 960, 3.4, 0.0, t_in=t_gana, modo="pop", dur=0.45, vida=0.6)
        C.rot("¡GANA EL AZUL!", 540, 560, 130, -0.03, AZUL_T, t_in=t_gana + 0.1, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 5. atardecer
@escena("atardecer")
def atardecer(C, t):
    t0 = INI("atardecer")
    t_aire, t_azul = T("atardecer", "aire"), T("atardecer", "azul")
    t_nar = T("atardecer", "naranja", frase=1)
    ca = C.capas_de("atardecer", cielo_atardecer)
    cam_suave(C, t, t0, FIN("atardecer"))
    img = C.base("atardecer", ca)
    sx, sy = C.xy(820, 1180)
    sol(img, sx, sy, t, 170, (255, 190, 80))
    # el camino de la luz a través del aire: el azul sale despedido, llega el rojo
    px, py = C.xy(330, 1440)
    cv2.line(img, (int(sx * 4), int(sy * 4)), (int(px * 4), int(py * 4)), (255, 120, 60), 24, cv2.LINE_AA, 2)
    for i in range(7):
        u = ((t - t0) * 0.35 + i / 7) % 1.0
        x, y = lerp(sx, px, u), lerp(sy, py, u)
        if u < 0.85:
            onda(img, (x, y), math.atan2(py - sy, px - sx), (255, 110, 60), 200, 16, 50, t, 13)
        # azul que se escapa hacia arriba
        if 0.1 < u < 0.7:
            vv = (u - 0.1) / 0.6
            onda(img, (x - 30 * vv, y - 330 * vv), -pi / 2 + 0.3, (60, 130, 250), 170, 16, 46, t, 12)
    C.fondo(img)
    C.pon(K.espalda(), 300, 1600, 1.6, 0.0, t_in=t0 + 0.1, vida=0.5)
    C.rot("MUCHO MÁS AIRE", 540, 300, 100, -0.03, CREMA, t_in=t_aire, dur=0.3, tira=True)
    C.rot("EL AZUL SE PIERDE", 540, 470, 90, 0.03, AZUL_T, t_in=t_azul, dur=0.3, tira=True)
    C.rot("NARANJA Y ROJO", 540, 1000, 100, -0.03, (255, 130, 70), t_in=t_nar, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 6. Marte
def capas_marte():
    far = P.fondo_liso(31, (230, 170, 110), (252, 214, 160), [(520, 0.7, (240, 190, 130), .5), (300, 1.2, (214, 140, 90), .4)])
    h = P.vacio()
    P.mancha(h, 300, BH - 220, 760, 300, (190, 90, 60), 32, rough=0.06)
    P.mancha(h, 900, BH - 160, 800, 260, (170, 76, 52), 33, rough=0.06)
    P.textura(h, 0.02, 0.04)
    return [(far, 0.25), (h, 1.0)]


@escena("marte")
def marte(C, t):
    t0 = INI("marte")
    t_rev, t_dia = T("marte", "reves"), T("marte", "dia")
    t_ata = T("marte", "atardecer")
    capas = C.capas_de("marte", capas_marte)
    cam_suave(C, t, t0, FIN("marte"))
    img = C.base("marte", capas)
    sx, sy = C.xy(540, 760)
    sol(img, sx, sy, t, 90, (255, 240, 220))
    u = e_inout(prog(t, t_ata - 0.2, t_ata + 0.8))
    if u > 0.01:                                         # al atardecer, un halo azul alrededor del Sol
        for k in range(6):
            P.disco(img, sx, sy, 380 - k * 52, (110, 160, 255), 0.16 * u)
    C.fondo(img)
    C.pon(X.marte("grandes", "sonrisa"), 540, 1230, 3.0, 0.0, t_in=t0 + 0.2, vida=0.8)
    C.rot("EN MARTE", 540, 290, 130, -0.03, CREMA, t_in=t0 + 0.3, dur=0.3, tira=True)
    C.rot("DE DÍA: ROJIZO", 540, 1650, 92, 0.02, (255, 130, 80), t_in=t_dia, dur=0.3, tira=True, t_out=t_ata, d_out=0.2)
    C.rot("AL ATARDECER: AZUL", 540, 1650, 80, -0.02, AZUL_T, t_in=t_ata, dur=0.3, tira=True)
    return C.fin()


# ------------------------------------------------------------------ 7. cierre
@escena("cierre")
def cierre(C, t):
    t0 = INI("cierre")
    t_ata, t_azul = T("cierre", "atardecer"), T("cierre", "azul")
    t_atr = T("cierre", "atras")
    ca = C.capas_de("atardecer", cielo_atardecer)
    cam_suave(C, t, t0, FIN("cierre"))
    img = C.base("cierre", ca)
    sx, sy = C.xy(540, 1120)
    sol(img, sx, sy, t, 150, (255, 190, 80))
    C.fondo(img)
    C.pon(K.espalda(), 540, 1640, 1.0, 0.0, t_in=t0 + 0.1, vida=0.5)
    # el azul que se queda atrás: pequeños azules que se despiden
    for i in range(6):
        ph = ((t - t_azul) * 0.25 + i / 6) % 1.0
        if t >= t_azul:
            C.pon(K.quark("azul", "grandes", "triste"), 150 + i * 160, 760 - 240 * ph + 20 * math.sin(i + t), 2.0 * (1 - 0.3 * ph), 0.1 * math.sin(t * 2 + i),
                  t_in=t_azul + 0.1 * i, modo="pop", dur=0.3, vida=0.8)
    C.rot("CADA ATARDECER ROJO", 540, 280, 82, -0.03, (255, 130, 70), t_in=t_ata, dur=0.3, tira=True)
    C.rot("ES EL AZUL QUE", 540, 420, 90, 0.03, CREMA, t_in=t_azul - 0.4, dur=0.3)
    C.rot("SE QUEDÓ ATRÁS", 540, 540, 100, -0.03, AZUL_T, t_in=t_atr, dur=0.3, tira=True)
    return C.fin()
