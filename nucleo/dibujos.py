# -*- coding: utf-8 -*-
"""Biblioteca de dibujos doodle (coordenadas locales; usar con lz.grupo)."""
import math

import cv2
import numpy as np

from motor import (NEGRO, BLANCO, OCRE, OCRE_CLARO, PIEL, PIEL_N, arco, bezier, blob, catmull, circulo,
                   clamp01, corazon, e_out, elipse, espiral, estrella, h01, lerp, r1, rect_red, ruido1, smooth)

OW = 7.0
ROJO = (226, 52, 58)
AMARILLO = (255, 214, 64)
CIAN = (60, 220, 240)
MAGENTA = (240, 70, 190)
VERDE = (90, 205, 90)
AZUL = (60, 110, 230)
MARFIL = (236, 224, 192)
MARRON = (120, 72, 38)
PELO = (70, 40, 22)


def miembro(lz, pts, color, grosor, seed):
    lz.trazo(pts, NEGRO, grosor + OW * 1.6, seed=seed, afinar=False)
    lz.trazo(pts, color, grosor, seed=seed, afinar=False)


def trazo_parcial(lz, pts, frac, color=NEGRO, ancho=OW, seed=0, **kw):
    pts = np.asarray(pts, dtype=np.float64)
    if frac <= 0 or len(pts) < 2:
        return
    seg = np.hypot(*np.diff(pts, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    L = d[-1] * clamp01(frac)
    k = int(np.searchsorted(d, L))
    sub = list(pts[:k])
    if 0 < k < len(pts):
        u = (L - d[k - 1]) / max(1e-9, d[k] - d[k - 1])
        sub.append(pts[k - 1] + (pts[k] - pts[k - 1]) * u)
    if len(sub) >= 2:
        lz.trazo(np.array(sub), color, ancho, seed=seed, **kw)


def capsula(bx, by, ang, L, w, n=10):
    d = np.array([math.cos(ang), math.sin(ang)])
    nrm = np.array([-d[1], d[0]])
    b = np.array([bx, by])
    tip = b + d * L
    a0 = math.atan2(nrm[1], nrm[0])
    semi = [tip + (w / 2) * np.array([math.cos(a0 - k * math.pi / n), math.sin(a0 - k * math.pi / n)]) for k in range(n + 1)]
    return np.vstack([[b + nrm * w / 2], semi, [b - nrm * w / 2]])


def contorno_unido(lz, partes, relleno, seed=0, ancho=OW, capa=None):
    """Silueta unida de varias partes: contornos gruesos debajo, rellenos encima."""
    for i, p in enumerate(partes):
        lz.trazo(p, NEGRO, ancho * 2.1, cerrado=True, seed=seed + i, capa=capa)
    for i, p in enumerate(partes):
        lz.relleno(p, relleno, seed=seed + i, capa=capa)


# ============================================================ personaje
def _parpadea(t, seed):
    periodo = 2.6 + 1.8 * h01(seed, 1)
    fase = (t + h01(seed, 2) * periodo) % periodo
    return fase < 0.13


def personaje(lz, x, y, s=1.0, t=0.0, tipo="cave", seed=1, mano_i=(-125, -175), mano_d=(125, -175),
              boca=0.0, mirar=(0.0, 0.0), salto=0.0, incl=0.0, cejas=0.0, paso=0.0, obj_i=None, obj_d=None,
              ojos="normal", accesorios=(), pupila=1.0, rot_cabeza=0.0):
    """Origen en los pies. Altura ~480. tipo: cave | tu | neander."""
    neander = tipo == "neander"
    tu = tipo == "tu"
    piel = PIEL_N if neander else PIEL
    with lz.grupo(x, y - salto, s, incl):
        # ---- piernas y pies
        for lado in (-1, 1):
            cad = (lado * 36, -105)
            pie = (lado * 50 + paso * lado * 22, -10)
            rod = ((cad[0] + pie[0]) / 2 + lado * 12, -58)
            pts = bezier(cad, rod, rod, pie, 16)
            col = (58, 88, 170) if tu else piel
            miembro(lz, pts, col, 26 if neander else 22, seed + 10 + lado)
            if tu:
                zap = rect_red(pie[0] - 34 + lado * 10, -26, 68, 28, 12)
                lz.forma(zap, BLANCO, NEGRO, OW, seed + 20 + lado)
                lz.trazo([(pie[0] - 18 + lado * 10, -14), (pie[0] + 16 + lado * 10, -14)], ROJO, 6, seed=seed + 22)
            else:
                lz.forma(elipse(pie[0] + lado * 16, -8, 34, 15), piel, NEGRO, OW, seed + 20 + lado)
        # ---- cuerpo
        ancho = 1.18 if neander else 1.0
        cuerpo = catmull([(-62 * ancho, -278), (0, -284), (62 * ancho, -278), (90 * ancho, -200),
                          (98 * ancho, -122), (72 * ancho, -94), (0, -88), (-72 * ancho, -94),
                          (-98 * ancho, -122), (-90 * ancho, -200)], 8, cerrado=True)
        if tu:
            hue = (t * 0.15) % 1.0
            c1 = tuple(int(255 * v) for v in _hsv(hue, 0.75, 1.0))
            lz.forma(cuerpo, c1, NEGRO, OW, seed + 30)
            for k, col in enumerate((MAGENTA, CIAN, AMARILLO)):
                lz.trazo(espiral(0, -185, 8 + k * 6, 70 - k * 8, 1.6, 60, a0=t * 2 + k * 2.1), col, 9, seed=seed + 31 + k)
        elif neander:
            lz.forma(cuerpo, (150, 96, 56), NEGRO, OW, seed + 30)
            zig = [(-100 + k * 20, -98 + (12 if k % 2 else 0)) for k in range(11)]
            lz.trazo(zig, (95, 55, 30), 6, seed=seed + 33)
            for k in range(6):
                px, py = -60 + k * 24, -230 + (k % 2) * 40
                lz.trazo([(px, py), (px + 8, py + 18)], (95, 55, 30), 5, seed=seed + 34 + k)
        else:
            lz.forma(cuerpo, (236, 146, 48), NEGRO, OW, seed + 30)
            for k in range(8):
                px = -60 + 120 * h01(seed, k, 1)
                py = -250 + 140 * h01(seed, k, 2)
                lz.relleno(blob(px, py, 11, seed=seed + k, irr=0.35), (110, 58, 20), seed=seed + 40 + k)
        if "cadena" in accesorios:
            ch = arco(0, -262, 58, 0.25, math.pi - 0.25, 18, ry=52)
            lz.trazo(ch, (255, 205, 60), 9, seed=seed + 45)
            lz.forma(circulo(0, -206, 16, 20), (255, 215, 70), NEGRO, 4, seed + 46)
        if "collar" in accesorios:
            ch = arco(0, -262, 58, 0.25, math.pi - 0.25, 12, ry=52)
            lz.trazo(ch, MARRON, 4, seed=seed + 47)
            for k, p in enumerate(ch[1:-1:2]):
                lz.forma(circulo(p[0], p[1], 8, 14), MARFIL if k % 2 else (250, 245, 230), NEGRO, 3, seed + 48 + k)
        # ---- brazos
        for lado, mano, obj in ((-1, mano_i, obj_i), (1, mano_d, obj_d)):
            hom = (lado * 64 * ancho, -252)
            mx, my = mano
            mid = ((hom[0] + mx) / 2 + lado * 28, (hom[1] + my) / 2 + 30)
            pts = bezier(hom, mid, mid, (mx, my), 16)
            miembro(lz, pts, piel, 24 if neander else 20, seed + 50 + lado)
            if obj is not None:
                obj(lz, mx, my)
            lz.forma(circulo(mx, my, 21, 24), piel, NEGRO, OW, seed + 55 + lado)
            lz.forma(circulo(mx - lado * 14, my - 12, 9, 14), piel, NEGRO, 5, seed + 57 + lado)
        # ---- cabeza
        with lz.grupo(0, -360, 1.0, rot_cabeza):
            _cabeza(lz, t, tipo, seed, piel, boca, mirar, cejas, ojos, accesorios, pupila)


def _hsv(h, s, v):
    i = int(h * 6) % 6
    f = h * 6 - int(h * 6)
    p, q, u = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    return [(v, u, p), (q, v, p), (p, v, u), (p, q, v), (u, p, v), (v, p, q)][i]


def _cabeza(lz, t, tipo, seed, piel, boca, mirar, cejas, ojos, accesorios, pupila):
    neander = tipo == "neander"
    tu = tipo == "tu"
    r = 100 if neander else 92
    colpelo = (150, 62, 30) if neander else ((40, 28, 30) if tu else PELO)
    # pelo trasero en picos
    n = 18
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * (1.28 if k % 2 == 0 else 1.02) * (0.9 if tu else 1.0)
        pts.append((rr * math.cos(a), -18 + rr * math.sin(a) * 0.95))
    lz.forma(np.array(pts), colpelo, NEGRO, OW, seed + 60)
    # orejas
    for lado in (-1, 1):
        lz.forma(elipse(lado * r * 0.98, 6, 20, 26), piel, NEGRO, OW, seed + 62 + lado)
    cara = elipse(0, 0, r * (1.06 if neander else 1.0), r * 0.98, 0, 64)
    lz.forma(cara, piel, NEGRO, OW, seed + 64)
    # flequillo
    fl = [(r * math.cos(a), r * 0.98 * math.sin(a)) for a in np.linspace(math.pi * 1.08, math.pi * 1.92, 12)]
    zz = []
    for k, a in enumerate(np.linspace(math.pi * 1.92, math.pi * 1.08, 9)):
        rr = r * (0.62 if k % 2 == 0 else 0.78)
        zz.append((rr * math.cos(a), rr * 0.9 * math.sin(a) - 4))
    lz.forma(np.array(fl + zz), colpelo, NEGRO, OW, seed + 66)
    if tipo == "cave":
        # hueso en el pelo
        with lz.grupo(52, -96, 1.0, -0.5):
            hueso_mini(lz, seed + 67)
    # ceja / arco superciliar
    cy = -44 - cejas * 12
    if neander:
        lz.forma(catmull([(-80, cy - 6), (0, cy - 18), (80, cy - 6), (78, cy + 14), (0, cy + 6), (-78, cy + 14)], 6, True),
                 (190, 136, 92), NEGRO, OW, seed + 68)
    ceja = catmull([(-64, cy), (-32, cy - 10 - cejas * 4), (0, cy - 2), (32, cy - 10 - cejas * 4), (64, cy)], 6)
    lz.trazo(ceja, colpelo if not tu else NEGRO, 14 if neander else 12, seed=seed + 69)
    # ojos
    ex, ey = 34, -10
    cerrado = ojos == "cerrados" or (ojos == "normal" and _parpadea(t, seed))
    for lado in (-1, 1):
        cx = lado * ex
        if cerrado:
            lz.trazo(arco(cx, ey, 20, 0.2, math.pi - 0.2, 12), NEGRO, 6, seed=seed + 70 + lado)
            continue
        if ojos == "corazon":
            lz.forma(corazon(cx, ey + 2, 30), ROJO, NEGRO, 5, seed + 70 + lado)
            continue
        if ojos == "espiral":
            lz.forma(elipse(cx, ey, 25, 30), BLANCO, NEGRO, OW, seed + 70 + lado)
            lz.trazo(espiral(cx, ey, 1, 21, 2.5, 60, a0=t * 9 * lado), (120, 40, 200), 4, seed=seed + 72 + lado)
            continue
        lz.forma(elipse(cx, ey, 26, 31), BLANCO, NEGRO, 4.5, seed + 70 + lado)
        px, py = cx + mirar[0] * 11, ey + mirar[1] * 13
        lz.relleno(circulo(px, py, 11 * pupila, 20), NEGRO, seed + 74 + lado, temblor=0.3)
        lz.relleno(circulo(px - 4, py - 5, 3.6, 10), BLANCO, seed + 76 + lado, temblor=0.2)
    if "gafas" in accesorios:
        for lado in (-1, 1):
            lz.forma(rect_red(lado * ex - 30, ey - 22, 60, 42, 14), (30, 30, 40), NEGRO, 5, seed + 78 + lado)
            lz.trazo([(lado * ex - 18, ey - 12), (lado * ex - 4, ey - 12)], (200, 200, 255), 4, seed=seed + 80)
        lz.trazo([(-6, ey - 8), (6, ey - 8)], NEGRO, 6, seed=seed + 81)
    # nariz
    lz.forma(blob(0, 20, 24 if neander else 17, seed=seed, irr=0.1), (piel[0] - 25, piel[1] - 35, piel[2] - 35), NEGRO, OW, seed + 82)
    # boca
    my = 52
    if boca > 0.06:
        bo = elipse(0, my, 26, 6 + 22 * boca)
        lz.forma(bo, (120, 22, 40), NEGRO, OW, seed + 84)
        lz.relleno(elipse(0, my + 6 + 12 * boca, 14, 5 + 6 * boca), (240, 110, 130), seed + 85)
        lz.relleno(rect_red(-14, my - 4 - 20 * boca, 28, 9, 3), BLANCO, seed + 86)
    elif boca < -0.06:
        # sonrisa abierta (boca negativa): borde de arriba recto, de abajo redondo
        h = 14 + 22 * -boca
        son = np.array([(34 * math.cos(a), my - 8 + h * math.sin(a)) for a in np.linspace(0, math.pi, 24)])
        lz.forma(son, (120, 22, 40), NEGRO, OW, seed + 84)
        lz.relleno(elipse(0, my - 8 + h * 0.72, 17, 5 + 5 * -boca), (240, 110, 130), seed + 85)
        lz.relleno(rect_red(-24, my - 8, 48, 10, 3), BLANCO, seed + 86)
    else:
        lz.trazo(catmull([(-30, my - 4), (0, my + 14), (30, my - 4)], 6), NEGRO, 6.5, seed=seed + 84)
    if tipo == "cave":
        rng = np.random.default_rng(seed)
        pp = np.array([(r * 0.8 * math.cos(a), r * 0.72 * math.sin(a) + 8) for a in rng.uniform(0.35, 2.8, 26)])
        lz.puntos(pp, 2.2, (110, 70, 45))
    if "auriculares" in accesorios:
        lz.trazo(arco(0, -8, r * 1.12, math.pi * 1.05, math.pi * 1.95, 30), (40, 40, 50), 16, seed=seed + 88)
        for lado in (-1, 1):
            lz.forma(rect_red(lado * r * 1.05 - 20, -34, 40, 68, 16), MAGENTA if lado < 0 else CIAN, NEGRO, OW, seed + 89 + lado)
    if "aro" in accesorios:
        lz.trazo(circulo(-r * 0.98, 38, 11, 16), (255, 205, 60), 5, cerrado=True, seed=seed + 92)


def hueso_mini(lz, seed=0, largo=60, col=MARFIL):
    partes = [rect_red(-largo / 2, -6, largo, 12, 5)]
    for lado in (-1, 1):
        partes += [circulo(lado * largo / 2, -7, 9, 14), circulo(lado * largo / 2, 7, 9, 14)]
    contorno_unido(lz, partes, col, seed, ancho=4)


# ============================================================ mano
def partes_mano():
    partes = [elipse(0, -78, 70, 80)]
    dedos = [(55, -70, -0.62, 92, 40), (44, -140, -1.38, 112, 34), (12, -152, -1.6, 126, 34),
             (-20, -146, -1.8, 114, 33), (-50, -124, -2.08, 90, 29)]
    for bx, by, a, L, w in dedos:
        partes.append(capsula(bx, by, a, L, w))
    partes.append(rect_red(-46, -30, 92, 150, 20))
    return partes


PARTES_MANO = partes_mano()


def mano(lz, x, y, s=1.0, rot=0.0, color=PIEL, seed=0, capa=None):
    with lz.grupo(x, y, s, rot):
        contorno_unido(lz, PARTES_MANO, color, seed, capa=capa)
        for k, (a, b) in enumerate([((-20, -20), (-8, -6)), ((20, -24), (10, -8))]):
            lz.trazo([a, b], NEGRO, 3, seed=seed + 30 + k, capa=capa)


def _puntos_spray(n=2600, seed=4):
    """Puntos de pigmento: densos pegados al contorno de la mano, dispersos lejos."""
    rng = np.random.default_rng(seed)
    polys = [np.round(p * 4).astype(np.int32).reshape(-1, 1, 2) for p in PARTES_MANO]
    pts, rad, orden = [], [], []
    while len(pts) < n:
        px, py = rng.uniform(-330, 330), rng.uniform(-430, 150)
        d = max(cv2.pointPolygonTest(pp, (px * 4, py * 4), True) for pp in polys) / 4
        if d > -4 or py > 110:
            continue
        dist = -d
        if rng.random() > math.exp(-dist / 50.0):
            continue
        pts.append((px, py))
        rad.append(rng.uniform(2.5, 6.5) * (1.35 if dist < 30 else 0.9))
        orden.append(rng.random())
    return np.array(pts), np.array(rad), np.argsort(orden)


SPRAY = _puntos_spray()


def estarcido(lz, x, y, s, prog, color=OCRE, rot=0.0, capa=0):
    """Mano en negativo sobre la roca: el spray aparece según prog (0..1)."""
    pts, rad, orden = SPRAY
    k = int(len(pts) * clamp01(prog))
    if k <= 0:
        return
    idx = orden[:k]
    with lz.grupo(x, y, s, rot):
        lz.puntos(pts[idx], rad[idx], color, capa=capa)


# ============================================================ cerdo de Sulawesi
CERDO_CUERPO = catmull([(-230, -20), (-215, -95), (-140, -145), (-30, -162), (80, -150), (160, -118),
                        (190, -70), (185, 10), (160, 85), (60, 106), (-60, 106), (-160, 96), (-215, 62),
                        (-236, 20)], 6, cerrado=True)
CERDO_CABEZA = catmull([(140, -122), (212, -112), (280, -72), (334, -14), (346, 28), (322, 48), (272, 54),
                        (214, 64), (168, 72), (140, 20)], 6, cerrado=True)
CERDO_PATAS = [[(150, 80), (166, 196)], [(100, 98), (94, 200)], [(-140, 90), (-154, 194)], [(-190, 70), (-212, 184)]]


def cerdo_rupestre(lz, x, y, s, prog, color=OCRE, oscuro=(110, 30, 18), seed=5, capa=0):
    """Cerdo verrugoso de Sulawesi pintado en la roca. prog 0..1 = avance de la pintura."""
    with lz.grupo(x, y, s):
        with lz.capa(capa):
            p1 = clamp01(prog / 0.5)
            p2 = clamp01((prog - 0.4) / 0.35)
            p3 = clamp01((prog - 0.72) / 0.28)
            partes = [CERDO_CUERPO, CERDO_CABEZA]
            if p2 >= 1:
                for k, pa in enumerate(CERDO_PATAS):
                    lz.trazo(pa, oscuro, 40, seed=seed + k, afinar=False)
                for k, pp in enumerate(partes):
                    lz.trazo(pp, oscuro, 16, cerrado=True, seed=seed + 10 + k)
                for k, pa in enumerate(CERDO_PATAS):
                    lz.trazo(pa, color, 26, seed=seed + k, afinar=False)
                for k, pp in enumerate(partes):
                    lz.relleno(pp, color, seed + 10 + k)
            else:
                if p2 > 0:
                    for k, pa in enumerate(CERDO_PATAS):
                        trazo_parcial(lz, pa, p2, color, 26, seed + k, afinar=False)
                    for k, pp in enumerate(partes):
                        lz.relleno(pp, color, seed + 10 + k, alfa=p2)
                trazo_parcial(lz, CERDO_CUERPO, clamp01(p1 * 1.6), oscuro, 8, seed + 10)
                trazo_parcial(lz, CERDO_CABEZA, clamp01(p1 * 1.6 - 0.6), oscuro, 8, seed + 11)
            if p3 > 0:
                # cresta de cerdas sobre lomo y nuca
                cresta = catmull([(-60, -160), (60, -152), (150, -124), (212, -112), (250, -92)], 6)
                for k in range(0, len(cresta), 2):
                    bx, by = cresta[k]
                    lz.trazo([(bx, by), (bx - 8, by - 34 * p3)], oscuro, 6, seed=seed + 20 + k)
                # disco del hocico, verrugas faciales, ojo, oreja, cola
                lz.relleno(elipse(343, 17, 8, 20, 0.3), oscuro, seed + 39)
                for k, (wx, wy) in enumerate([(286, -14), (300, 22), (250, 26)]):
                    lz.relleno(circulo(wx, wy, 11 * p3, 12), oscuro, seed + 40 + k)
                lz.relleno(circulo(258, -60, 8 * p3, 12), oscuro, seed + 45)
                lz.forma([(196, -110), (214, -172), (240, -100)], color, oscuro, 6, seed + 46)
                lz.trazo(espiral(-240, -30, 4, 22, 1.3, 30), oscuro, 6, seed=seed + 47)


# ============================================================ comida moderna
def hamburguesa(lz, x, y, s, seed=9):
    with lz.grupo(x, y, s):
        lz.forma(elipse(0, 70, 190, 38), BLANCO, NEGRO, OW, seed)
        lz.trazo(elipse(0, 70, 160, 28), (120, 170, 230), 5, cerrado=True, seed=seed + 1)
        lz.forma(rect_red(-120, 20, 240, 40, 18), (222, 160, 80), NEGRO, OW, seed + 2)
        lz.forma(rect_red(-128, -8, 256, 34, 16), (110, 60, 35), NEGRO, OW, seed + 3)
        lz.forma([(-130, -10), (130, -10), (60, 30), (0, -5), (-60, 30)], AMARILLO, NEGRO, 5, seed + 4)
        zig = [(-135 + k * 18, -18 + (10 if k % 2 else -4)) for k in range(16)]
        lz.trazo(zig, VERDE, 12, seed=seed + 5)
        lz.forma(np.vstack([arco(0, -20, 130, math.pi, 2 * math.pi, 30, ry=95)]), (236, 170, 80), NEGRO, OW, seed + 6)
        rng = np.random.default_rng(seed)
        for k in range(12):
            a = rng.uniform(math.pi * 1.15, math.pi * 1.85)
            rr = rng.uniform(40, 110)
            lz.relleno(elipse(rr * math.cos(a), -20 + rr * 0.7 * math.sin(a), 7, 4, rng.uniform(0, 3)), BLANCO, seed + 10 + k, temblor=0.3)


def telefono(lz, x, y, s=1.0, rot=0.0, pantalla=None, seed=13, t=0.0, color=(34, 32, 44)):
    """Pantalla local: x∈[-95,95], y∈[-185,185]. pantalla(lz) dibuja dentro."""
    with lz.grupo(x, y, s, rot):
        lz.forma(rect_red(-110, -210, 220, 420, 34), color, NEGRO, OW, seed)
        lz.relleno(rect_red(-95, -185, 190, 370, 20), (245, 245, 250), seed + 1, temblor=0.4)
        if pantalla is not None:
            pantalla(lz)
        lz.relleno(rect_red(-30, -202, 60, 12, 6), (15, 15, 20), seed + 2, temblor=0.3)


def ui_camara(lz, t, seed=0):
    lz.relleno(rect_red(-95, 120, 190, 65, 14), (20, 20, 26), seed, temblor=0.3)
    lz.forma(circulo(0, 152, 22, 24), BLANCO, (200, 200, 200), 5, seed + 1)
    for k, (cx, cy) in enumerate([(-60, -150), (60, -150)]):
        lz.trazo([(cx - 16, cy), (cx + 16, cy)], (255, 255, 255), 3, seed=seed + 2 + k)


def corazon_like(lz, x, y, s, seed=0, col=ROJO):
    lz.forma(corazon(x, y, 30 * s), col, NEGRO, 5, seed)


# ============================================================ música
def flauta(lz, x, y, s=1.0, rot=0.0, seed=21, agujeros_on=()):
    with lz.grupo(x, y, s, rot):
        arriba = catmull([(-230, -20), (-120, -26), (0, -22), (120, -24), (230, -18)], 8)
        abajo = catmull([(230, 18), (120, 24), (0, 22), (-120, 26), (-230, 20)], 8)
        cuerpo = np.vstack([arriba, abajo])
        contorno_unido(lz, [cuerpo, circulo(-232, -14, 20, 16), circulo(-232, 14, 20, 16)], MARFIL, seed)
        lz.trazo(catmull([(-200, 8), (-60, 12), (100, 10), (210, 6)], 6), (200, 186, 150), 5, seed=seed + 5)
        for k in range(5):
            hx = -110 + k * 58
            lleno = k in agujeros_on
            lz.forma(elipse(hx, -2, 11, 8), (60, 40, 30) if not lleno else PIEL, NEGRO, 3, seed + 6 + k)
        lz.forma([(212, -18), (232, -2), (212, 16)], (60, 40, 30), NEGRO, 3, seed + 12)


def nota(lz, x, y, s=1.0, color=MAGENTA, rot=0.0, seed=31, doble=False):
    with lz.grupo(x, y, s, rot):
        lz.forma(elipse(0, 0, 22, 15, -0.4), color, NEGRO, 5, seed)
        lz.trazo([(19, -4), (19, -86)], NEGRO, 6, seed=seed + 1, afinar=False)
        if doble:
            lz.forma(elipse(70, -12, 22, 15, -0.4), color, NEGRO, 5, seed + 3)
            lz.trazo([(89, -16), (89, -98)], NEGRO, 6, seed=seed + 4, afinar=False)
            lz.trazo([(19, -86), (89, -98)], NEGRO, 12, seed=seed + 5, afinar=False)
        else:
            lz.trazo(bezier((19, -86), (50, -70), (58, -50), (44, -30), 12), NEGRO, 7, seed=seed + 2)


def ecualizador(lz, x, y, w, h, t, beat_env, n=9, seed=0):
    bw = w / n
    for k in range(n):
        v = 0.25 + 0.75 * abs(math.sin(t * (3 + k * 0.7) + k)) * (0.6 + 0.4 * beat_env)
        bh = h * v
        col = tuple(int(255 * c) for c in _hsv((k / n + t * 0.1) % 1, 0.8, 1.0))
        lz.relleno(rect_red(x + k * bw + 2, y - bh, bw - 4, bh, 4), col, seed + k, temblor=0.3)


# ============================================================ Hombre León
def hombre_leon(lz, x, y, s=1.0, giro=1.0, seed=41, color=MARFIL, capa=None):
    tallado = (150, 128, 96)
    with lz.grupo(x, y, s * max(0.08, abs(giro)), sy=s):
        partes = [
            catmull([(-86, -400), (86, -400), (70, -300), (62, -225), (-62, -225), (-70, -300)], 6, True),
            capsula(-38, -235, math.pi / 2 + 0.04, 230, 56), capsula(38, -235, math.pi / 2 - 0.04, 230, 56),
            capsula(-80, -392, math.pi / 2 + 0.12, 190, 42), capsula(80, -392, math.pi / 2 - 0.12, 190, 42),
            circulo(0, -470, 88, 40),
        ]
        melena = []
        for k in range(28):
            a = k / 28 * 2 * math.pi
            rr = 128 if k % 2 == 0 else 104
            melena.append((rr * math.cos(a), -474 + rr * math.sin(a)))
        lz.forma(np.array(melena), (214, 188, 140), NEGRO, OW, seed + 90, capa=capa)
        contorno_unido(lz, partes, color, seed, capa=capa)
        # rayas talladas del brazo izquierdo (el original tiene 7)
        for k in range(7):
            yy = -370 + k * 20
            lz.trazo([(-100 - k * 2, yy), (-70 - k * 1.5, yy + 4)], tallado, 4, seed=seed + 10 + k, capa=capa)
        # cabeza de león
        for lado in (-1, 1):
            lz.forma(circulo(lado * 58, -540, 20, 16), color, NEGRO, 6, seed + 20 + lado, capa=capa)
        lz.forma(elipse(0, -448, 44, 34), (246, 236, 208), NEGRO, 6, seed + 22, capa=capa)
        lz.forma([(-14, -468), (14, -468), (0, -452)], (120, 90, 70), NEGRO, 4, seed + 23, capa=capa)
        lz.trazo(catmull([(-22, -430), (0, -438), (22, -430)], 5), NEGRO, 4, seed=seed + 24, capa=capa)
        for lado in (-1, 1):
            lz.trazo([(lado * 44, -500), (lado * 18, -492)], NEGRO, 6, seed=seed + 25 + lado, capa=capa)
        for k in range(10):
            a = -math.pi / 2 + (k - 4.5) * 0.32
            lz.trazo([(80 * math.cos(a), -470 + 80 * math.sin(a)), (98 * math.cos(a), -470 + 98 * math.sin(a))],
                     tallado, 4, seed=seed + 30 + k, capa=capa)


def mascara_arana(lz, x, y, s=1.0, seed=51, rot=0.0):
    with lz.grupo(x, y, s, rot):
        lz.forma(elipse(0, 0, 110, 132), (214, 30, 44), NEGRO, OW, seed)
        for k in range(12):
            a = k / 12 * 2 * math.pi
            lz.trazo([(0, 10), (108 * math.cos(a), 10 + 128 * math.sin(a))], (40, 10, 20), 3, seed=seed + 1 + k)
        for rr in (35, 65, 95):
            pts = []
            for k in range(13):
                a = k / 12 * 2 * math.pi
                m = rr * (0.92 if k % 2 else 1.0)
                pts.append((m * math.cos(a) * 0.92, 10 + m * math.sin(a) * 1.08))
            lz.trazo(pts, (40, 10, 20), 3, seed=seed + 20 + rr)
        for lado in (-1, 1):
            ojo = catmull([(lado * 12, -20), (lado * 50, -58), (lado * 88, -40), (lado * 70, 8), (lado * 22, 4)], 6, True)
            lz.forma(ojo, BLANCO, NEGRO, 9, seed + 40 + lado)


# ============================================================ joyas
def _catenaria(n, ancho=560, caida=150):
    xs = np.linspace(-ancho / 2, ancho / 2, n)
    ys = -caida * (1 - (xs / (ancho / 2)) ** 2) * -1
    return np.stack([xs, ys - caida * 0.6], 1)


def collar(lz, x, y, s=1.0, n_vis=99, seed=61, t=0.0):
    cuerda = _catenaria(40)
    with lz.grupo(x, y, s):
        lz.trazo(cuerda, MARRON, 5, seed=seed)
        pos = _catenaria(17)[1:-1]
        for k, (px, py) in enumerate(pos):
            if k >= n_vis:
                break
            tipo = k % 3
            bob = 3 * math.sin(t * 4 + k)
            if tipo == 0:   # cuenta de cáscara de avestruz
                lz.forma(circulo(px, py + bob, 17, 18), (250, 244, 226), NEGRO, 5, seed + k)
                lz.relleno(circulo(px, py + bob, 5, 10), (80, 60, 40), seed + 30 + k, temblor=0.3)
            elif tipo == 1:  # concha
                lz.forma(elipse(px, py + 6 + bob, 17, 24, 0.2), (246, 214, 180), NEGRO, 5, seed + k)
                lz.trazo([(px - 2, py - 8 + bob), (px + 3, py + 20 + bob)], (120, 80, 60), 4, seed=seed + 40 + k)
            else:            # diente perforado
                d = catmull([(px - 11, py - 6), (px + 11, py - 6), (px + 6, py + 26), (px, py + 44), (px - 6, py + 26)], 5, True)
                lz.forma(d + [0, bob], (252, 248, 236), NEGRO, 5, seed + k)


def destellos(lz, pts, t, s=1.0, seed=0, col=(255, 255, 220)):
    for k, (px, py) in enumerate(pts):
        f = 0.5 + 0.5 * math.sin(t * 6 + k * 1.7)
        if f < 0.2:
            continue
        r = 22 * s * f
        lz.forma(estrella(px, py, r, r * 0.3, 4, rot=t), col, NEGRO, 3, seed + k)


# ============================================================ aguja y moda
def aguja(lz, x, y, s=1.0, rot=0.0, seed=71):
    with lz.grupo(x, y, s, rot):
        cuerpo = catmull([(-180, 0), (-170, -12), (-60, -13), (100, -8), (180, 0), (100, 8), (-60, 13), (-170, 12)], 6, True)
        lz.forma(cuerpo, MARFIL, NEGRO, 6, seed)
        lz.forma(elipse(-150, 0, 12, 5), (70, 50, 40), NEGRO, 3, seed + 1)


def cuero(lz, x, y, s=1.0, seed=73, col=(176, 118, 70)):
    with lz.grupo(x, y, s):
        lz.forma(blob(0, 0, 230, seed=seed, irr=0.16, lob=6), col, NEGRO, OW, seed)
        rng = np.random.default_rng(seed)
        for k in range(22):
            px, py = rng.uniform(-170, 170), rng.uniform(-150, 150)
            if px * px + py * py > 170 ** 2:
                continue
            lz.trazo([(px, py), (px + 10, py + 14)], (140, 88, 50), 4, seed=seed + k)


# ============================================================ hueso de Lebombo
def hueso(lz, x, y, s=1.0, rot=0.0, marcas=0, seed=81, col=(232, 218, 182)):
    with lz.grupo(x, y, s, rot):
        partes = [rect_red(-280, -26, 560, 52, 24)]
        for lado in (-1, 1):
            partes += [circulo(lado * 282, -26, 38, 20), circulo(lado * 282, 26, 38, 20)]
        contorno_unido(lz, partes, col, seed)
        lz.trazo(catmull([(-240, 12), (-80, 16), (80, 14), (240, 10)], 5), (205, 188, 150), 5, seed=seed + 9)
        for k in range(int(marcas)):
            mx = -224 + k * 16
            lz.trazo([(mx, -26), (mx + 3, 4)], (70, 44, 30), 5, seed=seed + 20 + k)


# ============================================================ mar
def atun(lz, x, y, s=1.0, t=0.0, seed=91, rot=0.0):
    with lz.grupo(x, y, s, rot):
        cola_rot = 0.22 * math.sin(t * 7)
        with lz.grupo(-190, 2, 1.0, cola_rot):
            lz.forma([(0, 0), (-80, -86), (-52, -2), (-82, 86)], (40, 60, 120), NEGRO, OW, seed)
        lz.forma([(-10, -66), (40, -128), (70, -58)], (40, 60, 120), NEGRO, OW, seed + 1)
        lz.forma([(-20, 58), (20, 104), (40, 52)], (170, 180, 200), NEGRO, OW, seed + 2)
        cuerpo = catmull([(-195, 0), (-120, -58), (20, -74), (140, -44), (200, -8), (206, 6), (140, 40), (20, 64),
                          (-120, 50), (-195, 8)], 6, True)
        lz.forma(cuerpo, (200, 212, 226), NEGRO, OW, seed + 3)
        lomo = catmull([(-190, -2), (-120, -54), (20, -70), (140, -40), (200, -6), (130, -8), (20, -10), (-120, -6)], 6, True)
        lz.relleno(lomo, (38, 62, 128), seed + 4)
        lz.trazo(cuerpo, NEGRO, OW, cerrado=True, seed=seed + 3)
        for k in range(6):
            fx = -160 + k * 22
            lz.relleno([(fx, -40 + k * 3), (fx + 10, -54 + k * 4), (fx + 16, -38 + k * 3)], AMARILLO, seed + 10 + k, temblor=0.3)
        lz.trazo(arco(120, 4, 36, -1.2, 1.2, 12), NEGRO, 5, seed=seed + 20)
        lz.forma(circulo(160, -14, 12, 16), BLANCO, NEGRO, 4, seed + 21)
        lz.relleno(circulo(163, -14, 6, 10), NEGRO, seed + 22, temblor=0.2)


def canoa(lz, x, y, s=1.0, seed=101, t=0.0):
    with lz.grupo(x, y + 6 * math.sin(t * 2.2), s, 0.04 * math.sin(t * 1.7)):
        casco = catmull([(-260, -30), (260, -30), (220, 20), (0, 40), (-220, 20)], 8, True)
        lz.forma(casco, (140, 84, 44), NEGRO, OW, seed)
        lz.trazo([(-230, -12), (230, -12)], (100, 58, 30), 5, seed=seed + 1)


def olas(lz, y, t, amp=18, col=(40, 120, 220), seed=111, capas=3, w=1920, x0=-40, fondo=1200):
    for k in range(capas):
        xs = np.linspace(x0, w + 40, int(60 * (w - x0) / 1960) + 2)
        ys = y + k * 34 + amp * np.sin(xs / 80 + t * (2 + k * 0.4) + k)
        poly = np.vstack([np.stack([xs, ys], 1), [(w + 40, fondo), (x0, fondo)]])
        cc = (min(255, col[0] + k * 20), min(255, col[1] + k * 20), min(255, col[2] + k * 12))
        lz.forma(poly, cc, NEGRO, 6, seed + k)


def sushi(lz, x, y, s=1.0, seed=121):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-110, -10, 220, 70, 30), (250, 250, 244), NEGRO, OW, seed)
        rng = np.random.default_rng(seed)
        for k in range(14):
            px, py = rng.uniform(-90, 90), rng.uniform(5, 50)
            lz.trazo(elipse(px, py, 7, 3.5, rng.uniform(0, 3)), (220, 220, 210), 2.5, cerrado=True, seed=seed + k)
        pez = catmull([(-128, -4), (-110, -46), (0, -60), (110, -46), (132, -2), (0, -12)], 6, True)
        lz.forma(pez, (238, 96, 92), NEGRO, OW, seed + 20)
        for k in range(4):
            px = -70 + k * 44
            lz.trazo([(px, -12), (px + 24, -50)], (255, 190, 180), 6, seed=seed + 30 + k)


# ============================================================ genética / amor
def adn(lz, x, y, s=1.0, t=0.0, largo=700, marca=(0.62, 0.7), seed=131, vertical=False):
    with lz.grupo(x, y, s, math.pi / 2 if vertical else 0.0):
        n = 60
        xs = np.linspace(-largo / 2, largo / 2, n)
        fase = xs / 55 + t * 2.0
        a = np.stack([xs, 70 * np.sin(fase)], 1)
        b = np.stack([xs, 70 * np.sin(fase + math.pi)], 1)
        for k in range(0, n, 3):
            u = k / (n - 1)
            enm = marca[0] <= u <= marca[1]
            col = (255, 150, 40) if enm else ((90, 200, 255) if (k // 3) % 2 else (255, 90, 160))
            lz.trazo([a[k], b[k]], col, 10 if enm else 7, seed=seed + k)
        lz.trazo(a, NEGRO, 12, seed=seed + 100)
        lz.trazo(b, NEGRO, 12, seed=seed + 101)
        lz.trazo(a, (240, 240, 255), 6, seed=seed + 100)
        lz.trazo(b, (240, 240, 255), 6, seed=seed + 101)


def bebe(lz, x, y, s=1.0, t=0.0, seed=141):
    with lz.grupo(x, y, s):
        lz.forma(elipse(0, 40, 50, 42), (250, 230, 180), NEGRO, OW, seed)
        lz.forma(circulo(0, -30, 46, 30), PIEL, NEGRO, OW, seed + 1)
        lz.trazo(espiral(0, -74, 2, 12, 1.4, 24), PELO, 5, seed=seed + 2)
        cerr = _parpadea(t, seed)
        for lado in (-1, 1):
            if cerr:
                lz.trazo(arco(lado * 16, -34, 8, 0.3, math.pi - 0.3, 8), NEGRO, 4, seed=seed + 3 + lado)
            else:
                lz.relleno(circulo(lado * 16, -34, 6, 10), NEGRO, seed + 3 + lado, temblor=0.3)
        lz.trazo(arco(0, -18, 12, 0.3, math.pi - 0.3, 10), NEGRO, 4, seed=seed + 6)


# ============================================================ despedida
AUSTRALIA_LONLAT = [
    (113.5, -22.0), (114.1, -26.5), (115.0, -30.0), (115.7, -33.5), (117.9, -35.1), (123.5, -33.9), (126.0, -32.3),
    (131.0, -31.5), (134.0, -32.5), (135.6, -34.9), (137.6, -33.0), (138.1, -34.8), (139.5, -35.8), (140.9, -38.0),
    (144.0, -38.3), (146.3, -39.1), (150.0, -37.5), (150.9, -34.5), (153.1, -30.5), (153.5, -28.0), (153.1, -25.0),
    (150.8, -22.8), (149.0, -20.5), (146.3, -18.9), (145.4, -16.0), (145.2, -14.8), (143.8, -14.0), (142.5, -10.7),
    (141.6, -12.8), (141.5, -16.5), (140.5, -17.6), (139.0, -17.0), (137.6, -16.0), (135.9, -14.5), (136.9, -12.3),
    (135.0, -12.2), (132.6, -11.5), (131.0, -12.2), (129.5, -14.9), (128.1, -15.2), (126.9, -13.9), (125.2, -14.5),
    (123.5, -16.5), (122.2, -18.0), (121.0, -19.5), (119.0, -20.0), (116.7, -20.6), (114.6, -21.8)]
MUNGO = (143.0, -33.7)


def _ll(lon, lat, k=14.0):
    return ((lon - 133.5) * k, -(lat + 25.5) * k * 1.15)


def australia(lz, x, y, s=1.0, seed=151, col=(236, 160, 70), pin=1.0, t=0.0):
    with lz.grupo(x, y, s):
        pts = np.array([_ll(lo, la) for lo, la in AUSTRALIA_LONLAT])
        lz.forma(catmull(pts, 4, True), col, NEGRO, OW, seed)
        tas = [_ll(146.6 + 1.3 * math.cos(a), -42.0 + 1.0 * math.sin(a)) for a in np.linspace(0, 2 * np.pi, 10, endpoint=False)]
        lz.forma(np.array(tas), col, NEGRO, OW, seed + 1)
        if pin > 0:
            mx, my = _ll(*MUNGO)
            b = 10 * math.sin(t * 5) * (1 - pin) if pin < 1 else 4 * math.sin(t * 4)
            with lz.grupo(mx, my - 20 * (1 - e_out(pin)) + b):
                lz.forma(catmull([(0, 0), (-26, -44), (0, -72), (26, -44)], 6, True), ROJO, NEGRO, OW, seed + 2)
                lz.forma(circulo(0, -46, 10, 12), BLANCO, NEGRO, 4, seed + 3)


def fuego(lz, x, y, s=1.0, t=0.0, seed=161, capa=None):
    with lz.grupo(x, y, s):
        for k, col in enumerate(((226, 60, 30), (250, 150, 40), (255, 230, 110))):
            f = 1 - k * 0.28
            pts = []
            for i in range(9):
                u = i / 8
                a = math.pi * (1 + u)
                w = 90 * f * (1 + 0.15 * math.sin(t * 9 + i * 1.3 + k))
                h = 200 * f * (0.8 + 0.25 * r1(t * 3 + i, seed + k))
                if i in (2, 4, 6):
                    pts.append((w * math.cos(a) * 0.9, -h))
                else:
                    pts.append((w * math.cos(a), -h * 0.45 * (1 - abs(0.5 - u))))
            base = [(80 * f, 0), (0, 16), (-80 * f, 0)]
            lz.forma(catmull(pts + base, 5, True), col, NEGRO if k == 0 else None, 6, seed + k, capa=capa)
        for k in range(3):
            lz.forma(rect_red(-110 + k * 40, 6 + k * 3, 150, 26, 12), (110, 66, 36), NEGRO, 5, seed + 10 + k, capa=capa)


def humo(lz, x, y, t, seed=171, n=7, col=(200, 200, 230)):
    for k in range(n):
        u = ((t * 0.35 + k / n) % 1.0)
        px = x + 50 * math.sin(u * 7 + k) * u
        py = y - u * 520
        r = 25 + 60 * u
        lz.relleno(blob(px, py, r, seed=seed + k, irr=0.2), col, seed + k, alfa=0.55 * (1 - u))


def flor(lz, x, y, s=1.0, col=MAGENTA, seed=181, t=0.0):
    with lz.grupo(x, y, s):
        lz.trazo(bezier((0, 0), (10, 60), (-10, 120), (0, 200), 12), (60, 150, 60), 8, seed=seed)
        for k in range(6):
            a = k / 6 * 2 * math.pi + t * 0.3
            lz.forma(elipse(34 * math.cos(a), 34 * math.sin(a), 26, 16, a), col, NEGRO, 5, seed + 1 + k)
        lz.forma(circulo(0, 0, 18, 14), AMARILLO, NEGRO, 5, seed + 9)


def vela(lz, x, y, s=1.0, t=0.0, seed=191):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-26, -120, 52, 120, 8), (250, 244, 225), NEGRO, OW, seed)
        fl = catmull([(0, -205), (18, -150), (0, -128), (-18, -150)], 6, True)
        with lz.grupo(0, 0, 1.0, 0.08 * math.sin(t * 8)):
            lz.forma(fl, (255, 190, 60), NEGRO, 4, seed + 1)


def figura_yacente(lz, x, y, s=1.0, seed=201, col=(170, 150, 140), ocre=0.0, t=0.0):
    """Silueta estilizada y respetuosa, vista desde arriba, cubierta de ocre según 'ocre'."""
    with lz.grupo(x, y, s):
        partes = [circulo(-230, 0, 42, 24), elipse(-60, 0, 150, 58), capsula(80, -24, 0.03, 200, 40), capsula(80, 24, -0.03, 200, 40)]
        contorno_unido(lz, partes, col, seed)
        if ocre > 0:
            rng = np.random.default_rng(seed)
            n = int(420 * ocre)
            px = rng.uniform(-280, 290, 420)[:n]
            py = rng.normal(0, 36, 420)[:n]
            lz.puntos(np.stack([px, py], 1), rng.uniform(2, 6, 420)[:n], (190, 40, 28))


# ============================================================ íconos y varios
def wifi(lz, x, y, s=1.0, col=CIAN, seed=211, n=3):
    with lz.grupo(x, y, s):
        lz.forma(circulo(0, 0, 16, 16), col, NEGRO, 5, seed)
        for k in range(n):
            r = 50 + k * 42
            lz.trazo(arco(0, 0, r, -math.pi * 0.78, -math.pi * 0.22, 20), NEGRO, 22, seed=seed + 1 + k)
            lz.trazo(arco(0, 0, r, -math.pi * 0.78, -math.pi * 0.22, 20), col, 12, seed=seed + 1 + k)


def ciudad(lz, x, y, s=1.0, seed=221, t=0.0):
    with lz.grupo(x, y, s):
        edif = [(-150, 180, 70), (-80, 250, 60), (-20, 150, 50), (30, 290, 70), (100, 200, 60)]
        for k, (bx, h, w) in enumerate(edif):
            lz.forma(rect_red(bx, -h, w, h, 6), (120 + k * 20, 130, 200 - k * 15), NEGRO, 6, seed + k)
            for j in range(int(h / 50)):
                lz.relleno(rect_red(bx + 12, -h + 20 + j * 45, 14, 18, 3), AMARILLO, seed + 20 + k * 10 + j, temblor=0.2)


def trigo(lz, x, y, s=1.0, seed=231):
    with lz.grupo(x, y, s):
        for k, dx in enumerate((-40, 0, 40)):
            lz.trazo(bezier((dx, 60), (dx, 0), (dx * 0.5, -80), (dx * 0.3, -160), 12), (130, 150, 50), 7, seed=seed + k)
            for j in range(6):
                yy = -90 - j * 16
                xx = dx * 0.4
                lz.forma(elipse(xx - 12, yy, 12, 7, -0.6), (236, 190, 70), NEGRO, 3, seed + 10 + k * 6 + j)
                lz.forma(elipse(xx + 12, yy, 12, 7, 0.6), (236, 190, 70), NEGRO, 3, seed + 40 + k * 6 + j)


def tache(lz, x, y, s=1.0, prog=1.0, seed=241):
    with lz.grupo(x, y, s):
        trazo_parcial(lz, [(-130, -130), (130, 130)], clamp01(prog * 2), ROJO, 28, seed)
        trazo_parcial(lz, [(130, -130), (-130, 130)], clamp01(prog * 2 - 1), ROJO, 28, seed + 1)


def cerebro(lz, x, y, s=1.0, t=0.0, seed=251, col=(255, 150, 190), brillo=0.0):
    with lz.grupo(x, y, s):
        forma = blob(0, 0, 150, seed=seed, irr=0.08, lob=9)
        forma[:, 1] *= 0.78
        lz.forma(forma, col, NEGRO, OW, seed)
        lz.trazo([(0, -112), (6, -40), (-4, 30), (4, 100)], NEGRO, 5, seed=seed + 1)
        rng = np.random.default_rng(seed)
        for k in range(10):
            cx, cy = rng.uniform(-110, 110), rng.uniform(-70, 70)
            pts = [(cx + 18 * math.cos(a) * (1 + 0.3 * math.sin(a * 3)), cy + 14 * math.sin(a)) for a in np.linspace(0, 4.5, 10)]
            lz.trazo(pts, (200, 80, 130), 5, seed=seed + 10 + k)
        if brillo > 0:
            for k in range(8):
                a = k / 8 * 2 * math.pi + t
                r0, r1_ = 170, 170 + 60 * brillo
                lz.trazo([(r0 * math.cos(a), r0 * 0.78 * math.sin(a)), (r1_ * math.cos(a), r1_ * 0.78 * math.sin(a))],
                         AMARILLO, 10, seed=seed + 30 + k)


def mamut(lz, x, y, s=1.0, t=0.0, seed=261):
    with lz.grupo(x, y, s):
        pas = math.sin(t * 5)
        for k, lx in enumerate((-110, -50, 70, 130)):
            ph = pas * (1 if k % 2 else -1)
            miembro(lz, [(lx, -60), (lx + ph * 14, 60)], (120, 76, 50), 42, seed + k)
        lz.forma(blob(0, -120, 170, seed=seed, irr=0.1, lob=6) * [1.0, 0.72] + [0, -30], (136, 86, 54), NEGRO, OW, seed + 5)
        lz.forma(circulo(170, -170, 72, 30), (136, 86, 54), NEGRO, OW, seed + 6)
        lz.trazo(bezier((215, -150), (270, -60), (230, 20), (260, 50), 16), NEGRO, 40, seed=seed + 7, afinar=False)
        lz.trazo(bezier((215, -150), (270, -60), (230, 20), (260, 50), 16), (136, 86, 54), 26, seed=seed + 7, afinar=False)
        lz.trazo(bezier((190, -120), (260, -80), (300, -120), (290, -180), 14), NEGRO, 22, seed=seed + 8)
        lz.trazo(bezier((190, -120), (260, -80), (300, -120), (290, -180), 14), (250, 244, 225), 12, seed=seed + 8)
        lz.relleno(circulo(190, -190, 9, 10), NEGRO, seed + 9, temblor=0.3)
        for k in range(14):
            px = -150 + k * 22
            lz.trazo([(px, -60 - 10 * math.sin(k)), (px + 4, -28)], (100, 60, 36), 4, seed=seed + 20 + k)


def copo(lz, x, y, s=1.0, rot=0.0, seed=271, col=(230, 245, 255)):
    with lz.grupo(x, y, s, rot):
        for k in range(6):
            a = k * math.pi / 3
            lz.trazo([(0, 0), (40 * math.cos(a), 40 * math.sin(a))], col, 6, seed=seed + k)
            for u in (0.55,):
                bx, by = 40 * u * math.cos(a), 40 * u * math.sin(a)
                for d in (-0.6, 0.6):
                    lz.trazo([(bx, by), (bx + 14 * math.cos(a + d), by + 14 * math.sin(a + d))], col, 4, seed=seed + 10 + k)


def ojo_flotante(lz, x, y, s=1.0, t=0.0, seed=281, mirar=(0.0, 0.0)):
    with lz.grupo(x, y, s):
        lz.forma(elipse(0, 0, 60, 60), BLANCO, NEGRO, OW, seed)
        rng = np.random.default_rng(seed)
        for k in range(5):
            a = rng.uniform(0, 2 * np.pi)
            lz.trazo([(58 * math.cos(a), 58 * math.sin(a)), (36 * math.cos(a + 0.2), 36 * math.sin(a + 0.2))], ROJO, 3, seed=seed + k)
        col = tuple(int(255 * c) for c in _hsv((t * 0.2 + h01(seed)) % 1, 0.8, 1.0))
        px, py = mirar[0] * 18, mirar[1] * 18
        lz.forma(circulo(px, py, 28, 24), col, NEGRO, 5, seed + 10)
        lz.relleno(circulo(px, py, 13, 16), NEGRO, seed + 11, temblor=0.3)
        lz.relleno(circulo(px - 8, py - 8, 5, 10), BLANCO, seed + 12, temblor=0.2)
        if _parpadea(t, seed):
            lz.relleno(elipse(0, 0, 62, 62), (240, 180, 150), seed + 13)
            lz.trazo([(-60, 0), (60, 0)], NEGRO, OW, seed=seed + 14)


def bandera(lz, x, y, s, franjas, seed=291, vertical=False, t=0.0):
    """franjas: lista de (color, proporción)."""
    with lz.grupo(x, y, s):
        w, h = 180, 120
        lz.trazo([(-w / 2 - 10, -h / 2 - 10), (-w / 2 - 10, h / 2 + 90)], (90, 60, 40), 9, seed=seed)
        y0 = -h / 2
        tot = sum(p for _, p in franjas)
        for k, (col, p) in enumerate(franjas):
            hh = h * p / tot
            xs = np.linspace(-w / 2, w / 2, 12)
            ond = 6 * np.sin(xs / 40 + t * 4)
            top = np.stack([xs, y0 + ond], 1)
            bot = np.stack([xs[::-1], (y0 + hh + ond)[::-1]], 1)
            lz.relleno(np.vstack([top, bot]), col, seed + 1 + k, temblor=0.5)
            y0 += hh
        xs = np.linspace(-w / 2, w / 2, 12)
        ond = 6 * np.sin(xs / 40 + t * 4)
        marco = np.vstack([np.stack([xs, -h / 2 + ond], 1), np.stack([xs[::-1], (h / 2 + ond)[::-1]], 1)])
        lz.trazo(marco, NEGRO, 6, cerrado=True, seed=seed + 9)


def etiqueta(lz, x, y, texto, px=46, fondo=(255, 250, 235), color=NEGRO, rot=-0.03, seed=301, k=1.0,
             fuente="print", cinta=True, alfa=1.0):
    """Papelito pegado con cinta con texto."""
    from motor import ancho_texto
    w = ancho_texto(texto, fuente, px) + px * 1.2
    h = px * 1.75
    with lz.grupo(x, y, k, rot):
        if alfa < 0.999:
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, 10), fondo, seed, alfa=alfa)
        else:
            lz.forma(rect_red(-w / 2, -h / 2, w, h, 10), fondo, NEGRO, 5, seed)
            if cinta:
                for lado in (-1, 1):
                    lz.relleno(rect_red(lado * w / 2 - 34, -h / 2 - 16, 68, 30, 4) , (250, 230, 140), seed + 2 + lado, alfa=0.75)
        lz.texto(texto, 0, 2, px, fuente, color=color, borde=None, temblor=0.6, seed=seed, alfa=alfa)


# ============================================================ inventos antiguos (agregados para "7 inventos")
def pan_plano(lz, x, y, s=1.0, seed=501, quemado=1.0):
    """Pan plano redondo visto en 3/4, con manchas tostadas."""
    with lz.grupo(x, y, s):
        forma = blob(0, 0, 170, seed=seed, irr=0.07, lob=7) * [1.0, 0.55]
        lz.forma(forma + [0, 14], (170, 120, 70), NEGRO, OW, seed)
        lz.forma(forma, (222, 176, 112), NEGRO, OW, seed + 1)
        rng = np.random.default_rng(seed)
        for k in range(int(9 * quemado)):
            px, py = rng.uniform(-120, 120), rng.uniform(-55, 55)
            lz.relleno(blob(px, py, rng.uniform(9, 20), seed=seed + 10 + k, irr=0.3) * [1, 0.6] + [0, py * 0.4],
                       (130, 80, 40), seed + 10 + k)


def tostada(lz, x, y, s=1.0, seed=511):
    """Rebanada de pan tostado con mantequilla."""
    with lz.grupo(x, y, s):
        silueta = catmull([(-120, 140), (-120, -40), (-150, -90), (-120, -150), (0, -175), (120, -150),
                           (150, -90), (120, -40), (120, 140)], 8, True)
        lz.forma(silueta, (190, 120, 55), NEGRO, OW, seed)
        interior = silueta * 0.8 + [0, 8]
        lz.relleno(interior, (236, 180, 95), seed + 1)
        lz.forma(rect_red(-45, -40, 90, 60, 10), (255, 232, 130), NEGRO, 5, seed + 2)
        lz.trazo([(-30, -30), (20, -34)], BLANCO, 5, seed=seed + 3)


def espejo_obsidiana(lz, x, y, s=1.0, t=0.0, seed=521, reflejo=True):
    """Espejo de obsidiana pulida (negro brillante) sobre base de yeso."""
    with lz.grupo(x, y, s):
        lz.forma(blob(0, 20, 190, seed=seed, irr=0.06) * [1.0, 0.95], (226, 214, 190), NEGRO, OW, seed)
        lz.forma(elipse(0, 10, 150, 140), (28, 24, 34), NEGRO, OW, seed + 1)
        if reflejo:
            lz.trazo(arco(0, 10, 118, math.pi * 1.1, math.pi * 1.45, 16, ry=108), (200, 210, 240), 12, seed=seed + 2)
            lz.trazo(arco(0, 10, 95, math.pi * 1.15, math.pi * 1.3, 10, ry=86), (150, 160, 190), 7, seed=seed + 3)
            # silueta de cara reflejada, tenue
            lz.trazo(elipse(20, 20, 45, 55), (70, 70, 95), 4, cerrado=True, seed=seed + 4)
            u = 0.5 + 0.5 * math.sin(t * 2.5)
            lz.forma(estrella(-70 + 30 * u, -60, 22, 6, 4, rot=t), (255, 255, 255), None, 0, seed + 5)


def rueda_madera(lz, x, y, s=1.0, rot=0.0, seed=531):
    """Rueda maciza de dos tablones con agujero cuadrado para el eje (como la de Liubliana)."""
    with lz.grupo(x, y, s, rot):
        lz.forma(circulo(0, 0, 170, 60), (168, 116, 66), NEGRO, OW, seed)
        lz.trazo([(0, -168), (0, 168)], (110, 70, 36), 7, seed=seed + 1)
        for k, dx in enumerate((-110, -60, 50, 105)):
            h = math.sqrt(max(0, 170 ** 2 - dx ** 2)) * 0.9
            lz.trazo(catmull([(dx, -h), (dx + 6, -h / 3), (dx - 4, h / 3), (dx + 3, h)], 5), (140, 94, 50), 4, seed=seed + 2 + k)
        lz.forma(rect_red(-26, -26, 52, 52, 4), (60, 40, 25), NEGRO, 5, seed + 8)


def bici(lz, x, y, s=1.0, t=0.0, seed=541, col=(230, 70, 80)):
    with lz.grupo(x, y, s):
        for k, cx in enumerate((-150, 150)):
            lz.trazo(circulo(cx, 60, 95, 40), NEGRO, 14, cerrado=True, seed=seed + k)
            for j in range(8):
                a = j * math.pi / 4 + t * 4
                lz.trazo([(cx, 60), (cx + 88 * math.cos(a), 60 + 88 * math.sin(a))], (120, 120, 130), 3, seed=seed + 10 + j)
        cuadro = [(-150, 60), (-40, -60), (110, -60), (0, 60), (-150, 60)]
        lz.trazo(cuadro, col, 16, seed=seed + 3, afinar=False)
        lz.trazo([(110, -60), (150, 60)], col, 14, seed=seed + 4, afinar=False)
        lz.trazo([(0, 60), (-40, -60)], col, 12, seed=seed + 5, afinar=False)
        lz.forma(rect_red(-80, -100, 80, 22, 10), (40, 40, 45), NEGRO, 5, seed + 6)
        lz.trazo([(110, -60), (100, -110), (150, -120)], (40, 40, 45), 10, seed=seed + 7)


def auto(lz, x, y, s=1.0, t=0.0, seed=551, col=(70, 150, 230)):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-200, -40, 400, 90, 30), col, NEGRO, OW, seed)
        lz.forma(catmull([(-110, -40), (-70, -110), (80, -110), (130, -40)], 6, True), col, NEGRO, OW, seed + 1)
        for k, (a0, a1) in enumerate(((-95, -10), (10, 95))):
            lz.relleno(rect_red(a0, -98, a1 - a0 - 8, 52, 8), (200, 235, 255), seed + 2 + k, temblor=0.4)
        for k, cx in enumerate((-120, 120)):
            lz.forma(circulo(cx, 55, 45, 30), (40, 40, 45), NEGRO, OW, seed + 5 + k)
            lz.forma(circulo(cx, 55, 18, 16), (190, 190, 200), NEGRO, 4, seed + 7 + k)
        lz.forma(circulo(185, -10, 12, 12), AMARILLO, NEGRO, 3, seed + 9)


def maleta(lz, x, y, s=1.0, seed=561, col=(240, 120, 60)):
    with lz.grupo(x, y, s):
        lz.trazo([(-40, -170), (-40, -220), (40, -220), (40, -170)], (60, 60, 70), 12, seed=seed, afinar=False)
        lz.forma(rect_red(-110, -170, 220, 290, 26), col, NEGRO, OW, seed + 1)
        for k in (-45, 45):
            lz.trazo([(k, -160), (k, 110)], (200, 90, 40), 6, seed=seed + 2)
        for k, cx in enumerate((-70, 70)):
            lz.forma(circulo(cx, 140, 22, 16), (40, 40, 45), NEGRO, 5, seed + 4 + k)


def silla(lz, x, y, s=1.0, seed=571, col=(80, 80, 95)):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-90, -230, 180, 150, 30), col, NEGRO, OW, seed)
        lz.trazo([(0, -80), (0, -40)], (60, 60, 70), 14, seed=seed + 1)
        lz.forma(rect_red(-110, -60, 220, 40, 18), col, NEGRO, OW, seed + 2)
        lz.trazo([(0, -20), (0, 70)], (60, 60, 70), 16, seed=seed + 3)
        for k, dx in enumerate((-110, -55, 55, 110)):
            lz.trazo([(0, 70), (dx, 110)], (60, 60, 70), 12, seed=seed + 4 + k)
            lz.forma(circulo(dx, 122, 14, 12), (30, 30, 35), NEGRO, 4, seed + 8 + k)


def tablilla(lz, x, y, s=1.0, marcas=99, seed=581, numeros=False, rot=0.0):
    """Tablilla de arcilla con cuñas cuneiformes (o numerales sexagesimales si numeros=True)."""
    with lz.grupo(x, y, s, rot):
        lz.forma(rect_red(-150, -190, 300, 380, 40), (190, 146, 104), NEGRO, OW, seed)
        lz.trazo(rect_red(-138, -178, 276, 356, 34), (165, 122, 84), 4, cerrado=True, seed=seed + 1)
        rng = np.random.default_rng(seed)
        k = 0
        for fila in range(6):
            yy = -140 + fila * 56
            lz.trazo([(-125, yy + 26), (125, yy + 26)], (160, 118, 80), 3, seed=seed + 2 + fila)
            xx = -110
            while xx < 105 and k < marcas:
                if numeros:
                    n = 1 + rng.integers(0, 3)
                    for j in range(n):
                        cuna(lz, xx + j * 16, yy, 0.8, seed + 20 + k * 3 + j, vertical=True)
                    xx += 16 * n + 18
                else:
                    if rng.random() < 0.35:
                        lz.forma(circulo(xx + 8, yy + 2, 10, 14), (120, 84, 56), None, 0, seed + 20 + k)
                        xx += 30
                    else:
                        cuna(lz, xx, yy, 0.9, seed + 20 + k, vertical=rng.random() < 0.5)
                        xx += 26
                k += 1


def cuna(lz, x, y, s, seed, vertical=False):
    """Una marca en forma de cuña (cuneiforme)."""
    with lz.grupo(x, y, s, 0.0 if vertical else -math.pi / 2):
        lz.forma([(-8, -12), (8, -12), (0, 2)], (110, 76, 50), None, 0, seed)
        lz.trazo([(0, 0), (0, 18)], (110, 76, 50), 4, seed=seed + 1)


def vasija(lz, x, y, s=1.0, seed=591, col=(190, 110, 70)):
    with lz.grupo(x, y, s):
        cuerpo = catmull([(-40, -140), (40, -140), (50, -110), (110, -40), (100, 60), (60, 120), (-60, 120), (-100, 60),
                          (-110, -40), (-50, -110)], 6, True)
        lz.forma(cuerpo, col, NEGRO, OW, seed)
        lz.trazo(catmull([(-100, 0), (0, 20), (100, 0)], 6), (150, 80, 50), 6, seed=seed + 1)
        lz.forma(elipse(0, -140, 44, 12), (120, 70, 45), NEGRO, 5, seed + 2)


def chat(lz, x, y, s=1.0, t=0.0, n=3, seed=601):
    """Burbujas de mensajes (izquierda gris, derecha verde) apareciendo."""
    with lz.grupo(x, y, s):
        for k in range(n):
            der = k % 2 == 1
            yy = -150 + k * 115
            w = 240 - 40 * (k % 3)
            x0 = 30 if der else -270
            col = (170, 235, 160) if der else (250, 250, 250)
            lz.forma(rect_red(x0, yy, w, 80, 30), col, NEGRO, 5, seed + k)
            cola = [(x0 + w - 30, yy + 75), (x0 + w + 5, yy + 95), (x0 + w - 5, yy + 70)] if der else \
                [(x0 + 30, yy + 75), (x0 - 5, yy + 95), (x0 + 5, yy + 70)]
            lz.relleno(cola, col, seed + 10 + k)
            for j in range(2):
                lz.trazo([(x0 + 25, yy + 28 + j * 24), (x0 + w - 40 - 40 * j, yy + 28 + j * 24)], (120, 120, 130), 6, seed=seed + 20 + k * 2 + j)


def drenaje(lz, x, y, s=1.0, t=0.0, seed=611):
    """Corte de una casa del valle del Indo: baño de ladrillo -> tubo -> drenaje cubierto bajo la calle."""
    with lz.grupo(x, y, s):
        ladrillo = (190, 110, 80)
        lz.forma(rect_red(-330, -40, 330, 60, 6), ladrillo, NEGRO, OW, seed)
        lz.forma(rect_red(-260, -110, 140, 70, 10), (210, 200, 180), NEGRO, OW, seed + 1)
        lz.forma(rect_red(-10, 80, 340, 110, 12), (150, 90, 60), NEGRO, OW, seed + 2)
        lz.relleno(rect_red(10, 110, 300, 55, 8), (70, 60, 60), seed + 3)
        tubo = [(-190, -40), (-190, 40), (-60, 40), (-60, 135), (20, 135)]
        lz.trazo(tubo, NEGRO, 34, seed=seed + 4, afinar=False)
        lz.trazo(tubo, (120, 100, 90), 22, seed=seed + 4, afinar=False)
        for k in range(8):
            u = ((t * 0.8 + k / 8) % 1.0)
            if u < 0.35:
                px, py = -190, -40 + u / 0.35 * 80
            elif u < 0.6:
                px, py = -190 + (u - 0.35) / 0.25 * 130, 40
            else:
                px, py = -60 + (u - 0.6) / 0.4 * 330, 135
            lz.forma(elipse(px, py, 12, 7), (80, 160, 240), None, 0, seed + 10 + k)
        for k in range(6):
            bx = -320 + k * 55
            lz.trazo([(bx, -40), (bx, 20)], (150, 85, 60), 3, seed=seed + 20 + k)


def inodoro(lz, x, y, s=1.0, seed=621):
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-90, -220, 180, 110, 20), BLANCO, NEGRO, OW, seed)
        lz.forma(rect_red(-30, -205, 60, 18, 8), (200, 200, 210), NEGRO, 4, seed + 1)
        lz.forma(catmull([(-130, -100), (130, -100), (110, -20), (50, 40), (60, 120), (-60, 120), (-50, 40), (-110, -20)], 6, True),
                 BLANCO, NEGRO, OW, seed + 2)
        lz.forma(elipse(0, -100, 130, 26), (230, 235, 245), NEGRO, 5, seed + 3)


def reloj(lz, x, y, s=1.0, t=0.0, seed=631, vel=1.0):
    """Reloj de pared con 60 marcas y agujas que giran."""
    with lz.grupo(x, y, s):
        lz.forma(circulo(0, 0, 180, 60), (240, 90, 80), NEGRO, OW, seed)
        lz.forma(circulo(0, 0, 150, 60), BLANCO, NEGRO, 5, seed + 1)
        for k in range(60):
            a = k / 60 * 2 * math.pi
            r0 = 118 if k % 5 == 0 else 132
            lz.trazo([(r0 * math.sin(a), -r0 * math.cos(a)), (142 * math.sin(a), -142 * math.cos(a))], NEGRO,
                     6 if k % 5 == 0 else 2.5, seed=seed + 2 + k, temblor=0.4)
        am = t * vel * 2 * math.pi / 5
        ah = am / 12
        lz.trazo([(0, 0), (70 * math.sin(ah), -70 * math.cos(ah))], NEGRO, 12, seed=seed + 70, afinar=False)
        lz.trazo([(0, 0), (110 * math.sin(am), -110 * math.cos(am))], NEGRO, 8, seed=seed + 71, afinar=False)
        lz.forma(circulo(0, 0, 12, 12), (240, 90, 80), NEGRO, 4, seed + 72)


def dia_noche(lz, x, y, s=1.0, t=0.0, seed=641, partes_visibles=24):
    """Círculo mitad día (12 partes) y mitad noche (12 partes), como las horas egipcias."""
    with lz.grupo(x, y, s):
        dia = np.vstack([[(0, 0)], arco(0, 0, 180, math.pi, 2 * math.pi, 40)])
        noche = np.vstack([[(0, 0)], arco(0, 0, 180, 0, math.pi, 40)])
        lz.forma(dia, (130, 200, 250), NEGRO, OW, seed)
        lz.forma(noche, (40, 50, 110), NEGRO, OW, seed + 1)
        for k in range(24):
            if k >= partes_visibles:
                break
            a = math.pi + k / 24 * 2 * math.pi
            lz.trazo([(0, 0), (180 * math.cos(a), 180 * math.sin(a))], NEGRO if k < 12 else (200, 200, 230), 3,
                     seed=seed + 2 + k, temblor=0.4)
        with lz.grupo(0, -95):
            lz.forma(estrella(0, 0, 45, 32, 12, rot=t), AMARILLO, NEGRO, 4, seed + 30)
            lz.forma(circulo(0, 0, 26, 20), (255, 225, 80), NEGRO, 4, seed + 31)
        luna = np.vstack([arco(0, 95, 38, -math.pi / 2, math.pi / 2, 20),
                          arco(14, 95, 30, math.pi / 2, -math.pi / 2, 20)])
        lz.forma(luna, (240, 240, 210), NEGRO, 4, seed + 32)


def moneda_leon(lz, x, y, s=1.0, giro=1.0, seed=651):
    """Moneda de electro (oro+plata) irregular con cabeza de león en relieve. giro in [-1,1] simula voltearla."""
    with lz.grupo(x, y, s * max(0.1, abs(giro)), sy=s):
        lz.forma(blob(0, 0, 160, seed=seed, irr=0.08, lob=6), (225, 196, 112), NEGRO, OW, seed)
        lz.trazo(blob(0, 0, 138, seed=seed, irr=0.08, lob=6), (190, 160, 80), 5, cerrado=True, seed=seed + 1)
        if giro > 0:
            melena = []
            for k in range(22):
                a = math.pi * 0.2 + k / 21 * math.pi * 1.4
                rr = 88 if k % 2 == 0 else 70
                melena.append((-20 + rr * math.cos(a), rr * math.sin(a)))
            lz.forma(np.array(melena), (205, 170, 85), (130, 100, 40), 5, seed + 2)
            cabeza = catmull([(-40, -40), (20, -50), (80, -20), (95, 10), (70, 30), (30, 25), (0, 45), (-40, 30)], 6, True)
            lz.forma(cabeza, (215, 182, 95), (130, 100, 40), 5, seed + 3)
            lz.trazo([(60, 12), (92, 22)], (130, 100, 40), 5, seed=seed + 4)
            lz.forma(circulo(30, -20, 8, 10), (130, 100, 40), None, 0, seed + 5)
        else:
            lz.trazo(rect_red(-50, -50, 100, 100, 10), (160, 130, 60), 7, cerrado=True, seed=seed + 6)


def piramides(lz, x, y, s=1.0, seed=661):
    """Tres pirámides de Guiza (origen en la base)."""
    with lz.grupo(x, y, s):
        lz.trazo([(-330, 0), (480, 0)], (190, 150, 90), 8, seed=seed + 20)
        for k, (cx, w, h) in enumerate(((-150, 260, 220), (120, 320, 280), (330, 180, 150))):
            lz.forma([(cx - w / 2, 0), (cx, -h), (cx + w / 2, 0)], (226, 190, 120), NEGRO, OW, seed + k)
            lz.relleno([(cx, -h), (cx + w / 2, 0), (cx + w * 0.1, 0)], (196, 158, 92), seed + 10 + k)
            lz.trazo([(cx - w / 2, 0), (cx, -h), (cx + w / 2, 0)], NEGRO, OW, seed=seed + k)


def carreta(lz, x, y, s=1.0, t=0.0, seed=671):
    """Carreta de madera con ruedas macizas tirada por un buey (origen: suelo bajo la carreta)."""
    with lz.grupo(x, y, s):
        bx = 330
        paso = math.sin(t * 5)
        for k, lx in enumerate((bx - 80, bx - 30, bx + 60, bx + 105)):
            ph = paso * (1 if k % 2 else -1)
            miembro(lz, [(lx, -70), (lx + 10 * ph, 0)], (150, 108, 78), 26, seed + k)
        lz.forma(blob(bx + 10, -120, 115, seed=seed, irr=0.06) * [1.0, 0.5] + [0, -60], (176, 128, 92), NEGRO, OW, seed + 5)
        with lz.grupo(bx + 150, -150):
            for lado in (-1, 1):
                lz.trazo(bezier((lado * 20, -25), (lado * 60, -50), (lado * 70, -80), (lado * 45, -95), 10), (245, 238, 220), 10, seed=seed + 6 + lado)
            lz.forma(elipse(0, 0, 48, 42), (176, 128, 92), NEGRO, OW, seed + 8)
            lz.forma(elipse(10, 28, 30, 18), (225, 175, 150), NEGRO, 5, seed + 9)
            lz.relleno(circulo(-14, -8, 6, 10), NEGRO, seed + 10)
        lz.trazo([(bx - 100, -110), (70, -100)], MARRON, 12, seed=seed + 11)
        lz.forma(rect_red(-230, -190, 300, 100, 10), (160, 110, 60), NEGRO, OW, seed + 12)
        for k in range(3):
            lz.trazo([(-220, -160 + k * 30), (60, -160 + k * 30)], (120, 80, 40), 4, seed=seed + 13 + k)
        for k, cx in enumerate((-160, 10)):
            rueda_madera(lz, cx, -70, 0.38, rot=t * 2.0, seed=seed + 20 + k)


def balanza(lz, x, y, s=1.0, t=0.0, seed=681, inclinacion=0.0):
    """Balanza de platillos (origen: base). inclinacion en radianes (+ = baja el platillo derecho)."""
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-90, -20, 180, 30, 10), (140, 100, 60), NEGRO, OW, seed)
        lz.trazo([(0, -20), (0, -280)], (140, 100, 60), 16, seed=seed + 1, afinar=False)
        c, sn = math.cos(inclinacion), math.sin(inclinacion)
        extremos = [(-200 * c, -280 - 200 * sn), (200 * c, -280 + 200 * sn)]
        lz.trazo(extremos, (170, 130, 70), 12, seed=seed + 2, afinar=False)
        lz.forma(estrella(0, -285, 18, 10, 6), AMARILLO, NEGRO, 4, seed + 3)
        for k, (ex, ey) in enumerate(extremos):
            lz.trazo([(ex, ey), (ex - 55, ey + 110)], (90, 90, 90), 3, seed=seed + 4 + k)
            lz.trazo([(ex, ey), (ex + 55, ey + 110)], (90, 90, 90), 3, seed=seed + 6 + k)
            plato = np.vstack([arco(ex, ey + 110, 70, 0, math.pi, 16, ry=35)])
            lz.forma(plato, (205, 160, 80), NEGRO, 5, seed + 8 + k)
            if k == 0:
                for j in range(3):
                    lz.forma(blob(ex - 25 + j * 25, ey + 100 - 10 * (j % 2), 14, seed=seed + 20 + j, irr=0.3),
                             (175, 180, 190), NEGRO, 3, seed + 20 + j)
            else:
                lz.forma(rect_red(ex - 22, ey + 72, 44, 38, 6), (120, 120, 130), NEGRO, 4, seed + 30)
