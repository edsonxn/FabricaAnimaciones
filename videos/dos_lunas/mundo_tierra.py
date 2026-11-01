# -*- coding: utf-8 -*-
"""Toma 5 «cielo» (133:1-163:6 s): inmersión en la Tierra (su borde se aplana en horizonte con `Sup`) y noche de costa con DOS
lunas en el cielo: seis puños de separación, fases desfasadas ~5 días, noches más claras, animales y corales que dudan, y la
segunda luna que se acerca (gancho hacia la toma 6). Superficie en coordenadas planas X (derecha) y H (arriba):
tierra firme a la izquierda (X < -330), mar a la derecha con corte hasta el fondo y corales."""
import math

import numpy as np

import fondos as F
import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, Sup, kf, pop, ventana, campana, smooth_arr
from anclas import A, E_CIELO
import mundo_espacio as ME
import mundo_orbita as MB
from mundo_espacio import ER, MR, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, TINTA, chip, kuri_ui

D5 = (E_CIELO, A.abajo + 1.45)        # inmersión: ≈ 133,1 – 136,8
X_COSTA = -330.0
XS = np.arange(-4200, 4201, 40.0)
H_ORIZ = 700.0                         # y de pantalla del horizonte (H = 0)
HX = 960.0
SKIN = (250, 202, 164)

# lunas en el cielo (coordenadas de pantalla): centro y radio
M1 = np.array([1020.0, 330.0])
M2 = np.array([1600.0, 400.0])
R_LUNA = 88.0


def claras(t):
    """0..1: las noches se vuelven más claras con dos lunas."""
    return e_inout(prog(t, A.noches - 0.3, A.claras + 1.0))


def tn(c, t):
    """Tinte nocturno de un color (se aclara con las noches claras)."""
    return mezcla(c, (14, 18, 54), 0.64 - 0.28 * claras(t))


def h_tierra(X):
    X = np.asarray(X, float)
    base = 40 + 14 * np.sin(X / 170) + 8 * np.sin(X / 63 + 1)
    cae = smooth_arr((X + 470) / 140)                  # baja hacia la costa
    return base * (1 - cae) + (-8.0) * cae


def fondo_mar(X):
    X = np.asarray(X, float)
    return -335 + 22 * np.sin(X / 140) + 9 * np.sin(X / 57)


# ======================================================================== inmersión
def cam_inmersion(t):
    """Cámara que cae hacia el punto más alto de la Tierra: (cam, radio de la Tierra en pantalla, u)."""
    c0 = ME.cam_espacio(D5[0])
    L0 = np.array([0.0, -ER])
    u = prog(t, *D5)
    p0 = c0.a_pant(L0)
    ue = e_inout(u)
    z = math.exp(lerp(math.log(c0.z), math.log(520.0), e_in(u) * 0.35 + ue * 0.65))
    p = p0 + (np.array([HX, H_ORIZ]) - p0) * ue
    return Cam(L0, p, z), ER * z, u


def mezcla_cielo(rs):
    return prog(math.log(max(rs, 1.0)), math.log(1300), math.log(12000))


def cielo(t):
    """Fondo del cielo nocturno (se aclara un poco con las dos lunas)."""
    c = claras(t)
    arriba = mezcla((10, 14, 54), (28, 40, 108), c)
    abajo = mezcla((44, 58, 138), (86, 104, 188), c)
    img = F.degradado(t, tuple(v / 255 for v in arriba), tuple(v / 255 for v in abajo))
    return F.estrellas(img, t, 0.95 - 0.5 * c)


# ======================================================================== objetos de la escena
def coral(lz, t, col, seed, alfa=1.0):
    """Coral ramificado (origen en la base, y hacia arriba = negativo) que se mece."""
    lz.relleno(elipse(0, 4, 46, 13, 0, 24), oscurecer(col, 0.45), alfa=alfa)
    for i in range(5):
        a = -math.pi / 2 + (i - 2) * 0.42
        L = 58 + 30 * h01(seed, i, 1)
        sway = 0.07 * math.sin(t * 1.3 + seed + i)
        pts = [np.array([0.0, 0.0])]
        for k in range(1, 5):
            ang = a + sway * k
            pts.append(pts[-1] + L / 4 * np.array([math.cos(ang), math.sin(ang)]))
        lz.trazo(np.array(pts), mezcla(col, aclarar(col, 0.25), i / 5), 11 - i, afinar=False, temblor=0.0)
        lz.relleno(circulo(pts[-1][0], pts[-1][1], 10 - i * 0.6, 14), aclarar(col, 0.35), alfa=alfa)


def puno(lz, x, y, s=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-26, -24, 52, 48, 15), SKIN)
        for dx in (-13, 0, 13):
            lz.trazo(np.array([[dx, -23], [dx, -2]]), oscurecer(SKIN, 0.28), 3.5, afinar=False, temblor=0.0)
        lz.relleno(elipse(-29, 10, 10, 16, 0.5, 14), SKIN)
        lz.relleno(elipse(0, 20, 26, 6, 0, 14), oscurecer(SKIN, 0.2), alfa=0.8)


FASES = (0.0, 0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25)        # 8 iconos del ciclo (los 4 primeros crecen, luego menguan)


def faja_fases(lz, t, y, offset, col_hl, k, idx_hl):
    """Fila de 8 fases lunares (iconos de r = 27); `offset` la desplaza en x; idx_hl = icono resaltado."""
    for i, f in enumerate(FASES):
        x = 62 + offset + i * 86
        K.cuerpo_rocoso(lz, x, y, 27 * k, "luna", seed=2, ang_luz=0.0 if i < 5 else math.pi, fase=f)
        if i == idx_hl and k > 0.5:
            th = np.linspace(0, 2 * np.pi, 40)
            lz.trazo(np.stack([x + 36 * np.cos(th), y + 36 * np.sin(th)], 1), col_hl, 5.0, afinar=False, temblor=0.0)


def nube(lz, x, y, s, col, alfa):
    for dx, dy, rx, ry in ((0, 0, 120, 38), (-90, 14, 80, 28), (96, 10, 90, 30), (10, -22, 70, 30)):
        lz.relleno(elipse(x + dx * s, y + dy * s, rx * s, ry * s, 0, 28), col, alfa=alfa)


def luz_mar(lz, S, t, xm, alfa):
    """Camino de luz de la luna sobre el agua (columna de destellos)."""
    for i in range(9):
        w = 78 * (1 - i / 10) * (0.8 + 0.2 * math.sin(t * 2.2 + i * 1.3))
        x, y = S.pt(xm + 7 * math.sin(t * 1.5 + i), -9 - 26 * i)
        lz.relleno(elipse(x, y, w, 5.5, 0, 18), (214, 226, 255), alfa=alfa * (0.8 - 0.07 * i))


# ======================================================================== el paisaje (tierra, mar y fondo)
def paisaje(lz, t, S, alfa=1.0, corte=1.0):
    cl = claras(t)
    X = XS
    # colinas lejanas (detrás del horizonte, sobre el mar)
    if S.visible_y(260, -10):
        Hf = (90 + 55 * np.sin(X / 280 + 1) + 28 * np.sin(X / 120 + 2.3)) * np.clip((1700 - np.abs(X - 1250)) / 600, 0, 1)
        lz.relleno(S.poly(np.concatenate([np.stack([X, Hf], 1), [[X[-1], -20], [X[0], -20]]])), tn((70, 96, 168), t), alfa=alfa)
        Hn = (60 + 34 * np.sin(X / 210 + 0.4) + 18 * np.sin(X / 90)) * np.clip((1200 - np.abs(X + 900)) / 500, 0, 1)
        lz.relleno(S.poly(np.concatenate([np.stack([X, Hn], 1), [[X[-1], -20], [X[0], -20]]])), tn((54, 128, 138), t), alfa=alfa)
    # mar (en corte): degradado y crestas
    Xa = np.concatenate([[X_COSTA], X[X > X_COSTA]])
    sup = -6 + 3.0 * np.sin(Xa / 55 + t * 1.6) + 1.5 * np.sin(Xa / 23 - t * 2.3)
    fm = fondo_mar(Xa)
    agua = np.concatenate([np.stack([Xa, sup], 1), np.stack([Xa[::-1], fm[::-1] - 8], 1)])
    x0, y0 = S.pt(600, 0)
    x1, y1 = S.pt(600, -340)
    lz.degradado(S.poly(agua), tn((66, 156, 232), t), tn((14, 30, 92), t), (x0, y0), (x1, y1), alfa=alfa * corte)
    xs_, ys_ = S.p(Xa, sup)
    lz.trazo(np.stack([xs_, ys_], 1), tn((176, 214, 255), t), max(2.0, 4 * S.k), afinar=False, temblor=0.0)
    # fondo marino y roca
    Xf = Xa
    arena = np.concatenate([np.stack([Xf, fondo_mar(Xf) - 8], 1), [[Xf[-1], -4400], [Xf[0], -4400]]])
    lz.relleno(S.poly(arena), tn((214, 178, 134), t), alfa=alfa * corte)
    for hh, c_ in ((-380, (196, 156, 120)), (-520, (150, 118, 108)), (-900, (96, 80, 110))):
        if S.visible_y(hh, hh - 200):
            lz.relleno(S.poly([[X_COSTA, hh], [4200, hh - 20], [4200, -4400], [X_COSTA, -4400]]), tn(c_, t), alfa=alfa * corte * 0.9)
    # tierra firme (corte con capas)
    Xs = np.concatenate([X[X < X_COSTA], [X_COSTA]])
    tope = h_tierra(Xs)
    suelo = np.concatenate([np.stack([Xs, tope], 1), [[X_COSTA, -4400], [Xs[0], -4400]]])
    Ps = S.poly(suelo)
    lz.relleno(Ps, tn((118, 84, 76), t), alfa=alfa)
    with lz.recorte(Ps):
        for h0, h1, c in ((-120, -260, (136, 98, 84)), (-260, -420, (112, 80, 78)), (-420, -900, (92, 68, 82)),
                          (-900, -4400, (66, 48, 72))):
            if S.visible_y(h0, h1):
                lz.relleno(S.poly([[-4300, h0], [400, h0 - 14], [400, h1], [-4300, h1]]), tn(c, t), alfa=alfa)
        for i in range(10):
            px_, ph = -1500 + i * 150 + 30 * math.sin(i * 7.1), -190 - 85 * (i % 4)
            with S.en(lz, px_, ph):
                lz.relleno(elipse(0, 0, 24 + 8 * (i % 3), 14, 0.3 * i, 20), tn((150, 116, 100), t), alfa=alfa)
    pasto = np.concatenate([np.stack([Xs, tope + 5], 1), np.stack([Xs[::-1], tope[::-1] - 26], 1)])
    lz.relleno(S.poly(pasto), tn((78, 168, 112), t), alfa=alfa)


def corales_y_vida(lz, t, S, alfa=1.0):
    """Corales en el fondo; chispeo de huevos que sube hacia las lunas; peces."""
    cols = [(255, 120, 150), (255, 170, 80), (186, 120, 236), (86, 214, 196), (255, 214, 90), (255, 120, 150), (120, 190, 255)]
    for i, xc in enumerate((-120, 60, 250, 450, 640, 820, 960)):
        yb = float(fondo_mar(xc)) - 4
        with S.en(lz, xc, yb, 1.15):
            coral(lz, t, tn(cols[i], t), i * 3 + 1, alfa)
    # huevos/esperma de coral: suben desde el fondo siguiendo a la luna llena (y dudan)
    t0 = A.llena - 0.6
    t1 = A.obedecer + 1.2
    if t0 < t < t1:
        for i in range(70):
            xc = (-120, 60, 250, 450, 640, 820, 960)[i % 7]
            ts = t0 + (i % 14) * 0.17
            u = prog(t, ts, ts + 3.4)
            if u <= 0 or u >= 1:
                continue
            yb = float(fondo_mar(xc)) + 40
            Hh = lerp(yb, -14, e_in(u) * 0.35 + u * 0.65)
            # tras «no sabrían»: unos se van hacia la luna 1 y otros hacia la 2
            d = prog(t, A.sabrian, A.sabrian + 1.2)
            tgt = (M1[0] - HX if i % 2 else M2[0] - HX)
            Xx = xc + 14 * math.sin(t * 2 + i) + (tgt - xc) * 0.30 * d * u
            c = (255, 224, 200) if i % 3 else (255, 170, 190)
            x, y = S.pt(Xx, Hh)
            lz.halo(x, y, 14, c, alfa=0.35 * alfa, r0=0.2)
            lz.relleno(circulo(x, y, 4.2 + 1.5 * (i % 3), 10), c, alfa=alfa)
    # algas
    for i, xa in enumerate((-250, -60, 140, 350, 560, 740, 905)):
        yb = float(fondo_mar(xa)) - 2
        pts = []
        for k in range(7):
            hh = k * 34
            pts.append(S.pt(xa + 14 * math.sin(t * 1.1 + i * 1.7 + k * 0.7) * (k / 6) * 1.6, yb + hh))
        lz.trazo(np.array(pts), tn((60, 168, 120), t), max(3.0, 9 * S.k), afinar=True, temblor=0.0)
    # peces en cardumen (dos grupos que nadan en sentidos contrarios)
    for i in range(14):
        sent = 1 if i < 8 else -1
        v = 26 + 4 * (i % 4)
        fx = (-300 + ((t * v * sent + i * 211) % 1500))
        fh = -105 - 38 * (i % 5) - (130 if i >= 8 else 0) + 7 * math.sin(t * 1.7 + i)
        x, y = S.pt(fx, fh)
        with lz.grupo(x, y, S.k * (0.85 + 0.12 * (i % 3)), 0.0, 1.0):
            c = tn([(255, 160, 90), (120, 200, 255), (255, 120, 170), (160, 230, 150)][i % 4], t)
            sx = sent
            lz.relleno(elipse(0, 0, 22, 11, 0, 20), c, alfa=alfa)
            lz.relleno(np.array([[-20 * sx, 0], [-35 * sx, -10], [-35 * sx, 10]]), oscurecer(c, 0.2), alfa=alfa)
            lz.relleno(circulo(11 * sx, -2, 2.4, 8), (255, 255, 255), alfa=alfa)
    # medusas que brillan
    for i, (jx, jh, jv) in enumerate(((120, -180, 0.7), (640, -150, 0.9))):
        x, y = S.pt(jx + 40 * math.sin(t * 0.5 + i * 2), jh + 22 * math.sin(t * 0.9 + i))
        lz.halo(x, y, 70 * S.k, (255, 140, 220), alfa=0.35 * alfa, r0=0.2)
        with lz.grupo(x, y, S.k * 1.0):
            lz.relleno(elipse(0, 0, 28, 20, 0, 24), tn((255, 150, 220), t), alfa=0.9 * alfa)
            lz.relleno(rect_red(-28, -2, 56, 8, 4), tn((255, 150, 220), t), alfa=0.9 * alfa)
            for k in range(5):
                lz.trazo(np.array([[(-20 + 10 * k), 6], [(-20 + 10 * k) + 6 * math.sin(t * 3 + k + i), 30]]),
                         tn((255, 190, 235), t), 3.0, afinar=False, temblor=0.0)
    # burbujas
    for i in range(10):
        bx = -200 + (i * 173) % 1100
        u = (t * 0.22 + i * 0.37) % 1.0
        x, y = S.pt(bx + 8 * math.sin(t * 2 + i), lerp(float(fondo_mar(bx)) + 20, -12, u))
        lz.relleno(circulo(x, y, 3.0 + 2 * (i % 3), 10), (200, 228, 255), alfa=0.55 * alfa)


# ======================================================================== el cielo con dos lunas
def luna_cielo(lz, t, p, r, tipo, seed, fase, ang_luz, alfa, glow):
    lz.halo(p[0], p[1], r * 2.6, (196, 210, 255), alfa=(0.16 + 0.22 * glow) * alfa, r0=0.25)
    K.cuerpo_rocoso(lz, p[0], p[1], r, tipo, seed=seed, ang_luz=ang_luz, fase=fase, alfa=alfa, rot=0.03 * t)


def pos_luna2(t):
    """La 2.ª luna se queda en su sitio y, al final, se acerca (y crece)."""
    u = e_in(prog(t, A.vamos, A.cerca + 1.45))
    c = M2 + (np.array([1440.0, 440.0]) - M2) * u
    r = R_LUNA * (1 + 2.35 * u)
    return c, r


def cielo_dos_lunas(lz, t, S, alfa):
    cl = claras(t)
    # nubes que pasan (detrás de las lunas)
    for i, (x0, y0, s, v) in enumerate(((100, 190, 0.9, 11), (1100, 90, 1.2, 7), (1700, 430, 0.8, 14))):
        x = (x0 + v * t * 1.2) % (W + 500) - 250
        nube(lz, x, y0, s, tn((92, 110, 190), t), 0.55 * alfa)
    p2, r2 = pos_luna2(t)
    k1 = pop(t, A.imagina + 1.0, 0.5)
    luna_cielo(lz, t, M1, R_LUNA * k1, "luna", 1, 0.32, 0.0, alfa, cl)
    luna_cielo(lz, t, p2, r2 * pop(t, A.dos_c - 0.1, 0.5), "ceniza", 5, 0.62, math.pi, alfa, cl)
    # destello de aparición de la 2.ª luna
    kd = campana(t, A.dos_c - 0.1, A.dos_c + 0.9)
    if kd > 0.01:
        K.destello(lz, p2[0], p2[1], 120 * kd, t, alfa=min(1.0, kd * 1.4))
    # caminos de luz en el mar
    luz_mar(lz, S, t, M1[0] - HX, 0.55 * alfa)
    luz_mar(lz, S, t, p2[0] - HX, 0.55 * alfa)
    return M1, p2, r2


def seis_punos(lz, t, M1_, p2, r2):
    """Seis puños entre las dos lunas (Kuri los usa de regla)."""
    ks = e_out(prog(t, A.punos - 0.5, A.punos - 0.1)) * (1 - e_in(prog(t, A.fases - 0.4, A.fases)))
    if ks < 0.01:
        return
    a = M1_ + np.array([R_LUNA + 40, 0.0])
    b = p2 - np.array([r2 + 40, 0.0])
    n = 6
    for i in range(n):
        ts = A.seis - 0.1 + i * 0.16 if i else A.seis - 0.1
        k = pop(t, ts, 0.3) * ks
        if k < 0.01:
            continue
        u = (i + 0.5) / n
        q = a + (b - a) * u
        puno(lz, q[0], q[1] - 6 + 4 * math.sin(t * 3 + i), 0.95 * k)
        P.rotulo(lz, q[0], q[1] + 54, str(i + 1), px=34, alfa=k, color=ORO)
    kc = pop(t, A.punos + 0.1, 0.4) * ks
    if kc > 0.01:
        P.pastilla(lz, (a[0] + b[0]) / 2, a[1] - 118, "≈ 6 puños", px=44, k=kc, fondo=ORO, color=TINTA)


def iconos_fases(lz, t):
    k = e_out(prog(t, A.fases - 0.2, A.fases + 0.5)) * (1 - e_in(prog(t, A.noches - 0.1, A.noches + 0.4)))
    if k < 0.01:
        return
    # filas de fases; la B va desfasada ~1/6 de ciclo
    faja_fases(lz, t, 90, 0, ORO, k, 1)
    faja_fases(lz, t, 190, 98, MENTA, k, 5)
    P.rotulo(lz, 36, 90, "A", px=34, alfa=k, color=ORO, ancla=(0.0, 0.5))
    P.rotulo(lz, 36, 190, "B", px=34, alfa=k, color=MENTA, ancla=(0.0, 0.5))
    kc = e_out(prog(t, A.creciente - 0.1, A.creciente + 0.4))
    kg = e_out(prog(t, A.menguando - 0.1, A.menguando + 0.4))
    if kc > 0.01:
        P.pastilla(lz, 880, 90, "creciente", px=36, k=kc * k, fondo=ORO, color=TINTA)
    if kg > 0.01:
        P.pastilla(lz, 880, 190, "menguante", px=36, k=kg * k, fondo=MENTA, color=TINTA)
    # desfase de 5 días
    kd = pop(t, A.cinco - 0.2, 0.4) * k * (1 - 0.0)
    if kd > 0.01:
        xa = 62 + 4 * 86
        xb = 62 + 98 + 4 * 86
        lz.trazo(np.array([[xa, 138], [xa, 150], [xb, 150], [xb, 138]]), (255, 255, 255), 4.0, afinar=False, temblor=0.0)
        P.pastilla(lz, (xa + xb) / 2 + 40, 142, "≈ 5 días", px=36, k=kd, fondo=(255, 255, 255), color=TINTA)


def arbol_noche(lz, x, y, s, t, seed=0):
    """Árbol de copa redonda de noche: tronco y tres masas de hojas (sin discos de brillo)."""
    tronco = tn((98, 70, 70), t)
    hoja = tn((70, 160, 112), t)
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-13, -150, 26, 154, 8), tronco)
        lz.trazo(np.array([[0, -96], [34, -140]]), tronco, 10, afinar=False, temblor=0.0)
        for dx, dy, r, k in ((-46, -190, 74, 0.0), (50, -196, 66, 0.1), (0, -246, 82, 0.0), (-6, -170, 60, 0.18)):
            sw = 3 * math.sin(t * 0.9 + seed + dx)
            lz.relleno(circulo(dx + sw, dy, r, 36), oscurecer(hoja, k * 0.5) if k else hoja)
        lz.relleno(elipse(-30 + 3 * math.sin(t * 0.9 + seed), -214, 42, 30, 0.4, 24), aclarar(hoja, 0.10), alfa=0.8)


def arboles(lz, t, S, alfa=1.0):
    for X, s in ((-930, 1.35), (-372, 0.78)):
        x, y = S.pt(X, float(h_tierra(X)) + 4)
        arbol_noche(lz, x, y, s * S.k, t, seed=int(abs(X)) % 7)


def animales(lz, t, S):
    """Conejo y zorro que miran a las dos lunas y dudan; Kuri les hace de guía."""
    k = pop(t, A.noches, 0.4) if t > A.noches else 1.0
    duda = ventana(t, A.animales, A.obedecer + 1.4, 0.4, 0.5)
    for X, tipo, s in ((-585, "conejo", 1.7), (-455, "zorro", 1.35)):
        Hh = float(h_tierra(X))
        x, y = S.pt(X, Hh + 3)
        volt = (math.sin(t * 3.0 + X) > 0) if duda > 0.3 else False
        if tipo == "conejo":
            P.conejo(lz, x, y, s, t, voltear=volt, salto=4 * max(0.0, math.sin(t * 5)) * duda)
        else:
            P.zorro(lz, x, y, s, t, voltear=volt)
        if duda > 0.05:
            P.rotulo(lz, x, y - 150 * (s / 1.4), "?", px=70, color=ORO, alfa=duda * (0.7 + 0.3 * math.sin(t * 5 + X)))


def pregunta_corales(lz, t, S):
    d = ventana(t, A.sabrian, A.obedecer + 1.4, 0.4, 0.5)
    if d < 0.05:
        return
    for xc in (60, 450, 820):
        x, y = S.pt(xc, fondo_mar(xc) + 175)
        P.rotulo(lz, x, y, "?", px=70, color=ORO, alfa=d * (0.7 + 0.3 * math.sin(t * 5 + xc)))


def kuri_playa(lz, t, S, p2, r2):
    X = -790.0
    Hh = float(h_tierra(X))
    x, y = S.pt(X, Hh + 3)
    # Kuri llega volando desde su esquina de espacio hasta la playa durante la inmersión
    u = e_inout(prog(t, D5[0] + 0.8, D5[1] - 0.4))
    kx = lerp(1760.0, x, u)
    ky = lerp(940.0, y, u)
    if u < 1:
        ky -= 90 * math.sin(math.pi * u)
    # mira a las lunas, alterna
    m = M1 if math.sin(t * 1.2) > 0 else p2
    d = np.asarray(m, float) - np.array([kx, ky - 100])
    mirar = tuple(d / max(1.0, float(np.hypot(*d))) * 0.9)
    pun = ventana(t, A.seis - 0.2, A.punos + 1.6, 0.3, 0.4)
    sust = campana(t, A.cerca - 0.2, A.cerca + 1.6)
    s = lerp(1.0, 1.55, u)
    kuri_ui(lz, t, kx, ky, s, mirar, boca=sust, aleteo=pun)


# ======================================================================== la toma
def toma_5(lz, t, cam_sp):
    """Dibuja la toma 5. Devuelve (fondo, imagen auxiliar) para componer: aquí solo el fondo."""
    cl = claras(t)
    if t < D5[1]:
        cam, rs, u = cam_inmersion(t)
        s = mezcla_cielo(rs)
        bg = ME.fondo(t, cam) * (1 - s) + cielo(t) * s
        ME.fondo_comun(lz, t, cam)
        E = cam.a_pant((0, 0))
        r_m = max(MR * cam.z, 13.0)
        fade = 1 - e_in(prog(t, D5[0] + 0.2, D5[0] + 1.3))
        # las dos lunas de L4 y la Tierra que crece
        if rs < 6000:
            p1 = cam.a_pant(ME.luna_mundo(t))
            p2 = cam.a_pant(np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, ME.ang_luna(t) + math.pi / 3)))
            if rs < 24000:
                K.tierra_marea(lz, E[0], E[1], rs, t, [], rot=0.45 * t, ang_luz=LUZ, amp=0.0)
            if r_m < 340 and cam.visible(ME.luna_mundo(t), MR):
                K.cuerpo_rocoso(lz, p1[0], p1[1], r_m, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t)
            p2w = np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, ME.ang_luna(t) + math.pi / 3))
            if r_m < 340 and cam.visible(p2w, MR):
                K.cuerpo_rocoso(lz, p2[0], p2[1], r_m, "ceniza", seed=5, ang_luz=LUZ, rot=0.07 * t + 5)
            if fade > 0.01:
                MB.toma_L4(lz, t, cam, E, r_m, fade=fade)
        S = Sup(cam.pant[0], cam.pant[1], min(1.0, rs / 9000), 1 / rs)
        al = prog(rs, 260, 800)
        if al > 0.003:
            paisaje(lz, t, S, alfa=al, corte=1.0)
            if S.k > 0.25:
                corales_y_vida(lz, t, S, alfa=al)
        # cielo con dos lunas al final de la caída
        a_cielo = prog(t, D5[1] - 1.5, D5[1] - 0.2)
        if a_cielo > 0.01:
            cielo_dos_lunas(lz, t, S, a_cielo)
        kuri_playa(lz, t, S, pos_luna2(t)[0], pos_luna2(t)[1])
        return bg
    # --- superficie plana
    S = Sup(HX, H_ORIZ, 1.0, 0.0)
    bg = cielo(t)
    paisaje(lz, t, S)
    M1_, p2, r2 = cielo_dos_lunas(lz, t, S, 1.0)
    corales_y_vida(lz, t, S)
    arboles(lz, t, S)
    animales(lz, t, S)
    pregunta_corales(lz, t, S)
    seis_punos(lz, t, M1_, p2, r2)
    iconos_fases(lz, t)
    kuri_playa(lz, t, S, p2, r2)
    return bg
