# -*- coding: utf-8 -*-
"""Mundos de la escena 8 (el virrey Mendoza): la Ciudad de México de 1541 en 2D (volcanes, calzada, iglesias, casas) de donde sale el ejército,
el virrey a caballo, y el cerco del Mixtón en isométrico (anillo de sitiadores con tiendas y fogatas que se cierra)."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_gente_iso as G
import kz_pers2d as K2
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_inout, W, H
from mundos_b import iso_en
import mundos_h as MH

VIRREY = dict(piel="clara", pelo=(150, 140, 150), peinado="corto", cejas_g=1.3, torso="levita", ropa=(120, 36, 60), ropa2=(250, 244, 230), barba="corta", bigote=True,
              tocado="sombrero_ala")


def volcanes(lz, t, cx=0.0, y=640, alfa=1.0):
    """Popocatépetl e Iztaccíhuatl al fondo, con nieve y una fumarola."""
    for (x, w, h, nieve, col) in ((1340, 420, 330, 0.30, (150, 120, 170)), (760, 620, 240, 0.22, (136, 110, 160))):
        xx = x - cx * 0.15
        if w == 620:   # Iztaccíhuatl: perfil alargado de «mujer dormida»
            pts = [(xx - w / 2, y), (xx - w * 0.30, y - h * 0.7), (xx - w * 0.12, y - h * 0.85), (xx + w * 0.05, y - h), (xx + w * 0.25, y - h * 0.8), (xx + w * 0.40, y - h * 0.55), (xx + w / 2, y)]
        else:
            pts = [(xx - w / 2, y), (xx - w * 0.08, y - h), (xx + w * 0.08, y - h), (xx + w / 2, y)]
        lz.relleno(np.array(pts), col, alfa=alfa, capa=0)
        q = np.array(pts, float)
        top = q[:, 1].min()
        cut = top + h * nieve
        nv = [p for p in pts if p[1] <= cut + 1]
        if len(nv) >= 2:
            l = [(xx - w * 0.2, cut), *[p for p in pts if p[1] < cut], (xx + w * 0.2, cut)]
            lz.relleno(np.array(sorted(l, key=lambda p: p[0])), (246, 240, 255), alfa=0.9 * alfa, capa=0)
    for k in range(6):                                                    # fumarola del Popocatépetl
        ph = (t * 0.25 + k / 6) % 1.0
        lz.relleno(circulo(1340 - cx * 0.15 + 30 * math.sin(ph * 4 + k) + 120 * ph, y - 340 - ph * 180, 18 + 50 * ph, 18), (236, 230, 246), alfa=0.45 * (1 - ph), capa=0)


def ciudad_mexico(lz, t, cx=0.0, y=820):
    """Perfil de la ciudad virreinal temprana: templos con torres y cúpulas, casas con azotea, sobre la orilla del lago."""
    col_c, col_s = (232, 206, 182), (196, 166, 150)
    for i in range(16):                                                    # casas
        x = 120 * i - (cx * 0.5) % 120 - 60
        hh = 70 + 40 * h01(9, i)
        w = 100 + 20 * h01(8, i)
        lz.relleno(rect_red(x, y - hh, w, hh, 4), col_c if i % 2 else (222, 190, 168), capa=1)
        lz.relleno(rect_red(x, y - hh, w * 0.3, hh, 0), col_s, alfa=0.6, capa=1)
        for j in range(2):
            lz.relleno(rect_red(x + 22 + 40 * j, y - hh + 22, 16, 22, 3), (110, 80, 90), capa=1)
    xc = 980 - cx * 0.5                                                   # catedral primitiva con dos torres
    lz.relleno(rect_red(xc - 170, y - 200, 340, 200, 6), (240, 220, 196), capa=1)
    for sd in (-1, 1):
        lz.relleno(rect_red(xc + sd * 150 - 40, y - 300, 80, 300, 6), (230, 206, 182), capa=1)
        lz.relleno(np.array([(xc + sd * 150 - 46, y - 300), (xc + sd * 150, y - 360), (xc + sd * 150 + 46, y - 300)]), (190, 84, 70), capa=1)
        lz.relleno(rect_red(xc + sd * 150 - 14, y - 280, 28, 40, 14), (90, 60, 70), capa=1)
    lz.relleno(elipse(xc, y - 200, 90, 70, 0, 30), (210, 110, 80), capa=1)
    lz.relleno(rect_red(xc - 40, y - 120, 80, 120, 40), (110, 70, 70), capa=1)
    lz.relleno(rect_red(xc - 4, y - 300, 8, 60, 0), (250, 240, 220), capa=1)
    lz.relleno(rect_red(xc - 22, y - 284, 44, 8, 0), (250, 240, 220), capa=1)


def virrey_a_caballo(lz, x, y, s, t, galope=0.6):
    MH.caballo2d(lz, x, y, s, t, ph=t * 7.5, galope=galope, color=(236, 230, 220), crin=(170, 160, 160), jinete=VIRREY, jinete_seed=8)
    # estandarte real que lleva un abanderado al lado
    xp = x - 13.6 * s                                                       # lo lleva el primer soldado de la columna
    lz.relleno(rect_red(xp, y - 22 * s, 0.35 * s, 22 * s, 0), (120, 90, 70), capa=2)
    ond = [(xp + 0.3 * s + 6 * s * u, y - 22 * s + 0.5 * s * math.sin(t * 5 + u * 5)) for u in np.linspace(0, 1, 8)]
    lz.relleno(np.array(ond + [(p[0], p[1] + 4 * s) for p in ond[::-1]]), (246, 240, 230), capa=2)
    cx_, cy_ = xp + 3.3 * s, y - 20.0 * s                                   # cruz de Borgoña (aspa roja)
    for sg in (-1, 1):
        lz.relleno(np.array([(cx_ - 1.2 * s, cy_ - sg * 1.3 * s), (cx_ - 0.8 * s, cy_ - sg * 1.5 * s), (cx_ + 1.2 * s, cy_ + sg * 1.3 * s), (cx_ + 0.8 * s, cy_ + sg * 1.5 * s)]), (200, 40, 50), capa=2)


# ------------------------------------------------------------------------------------------------ el cerco del Mixtón (isométrico)
CENTRO = (-20.0, -20.0)


def anillo(t, R, n=44, seed=3):
    """Posiciones del anillo de sitiadores (x, y, ángulo)."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + 0.05 * math.sin(i * 1.7)
        r = R + 14 * (h01(seed, i) - 0.5)
        out.append((CENTRO[0] + r * math.cos(a), CENTRO[1] + r * math.sin(a), a, i))
    return out


def cerco(lz, iso, t, R, frente, seed=3, tiendas=True):
    """Sitiadores (personas mirando al centro), tiendas y fogatas en el anillo de radio R. frente=True dibuja solo la mitad delantera (x+y mayor)."""
    cosas = []
    for x, y, a, i in anillo(t, R, seed=seed):
        delante = (x - CENTRO[0]) + (y - CENTRO[1]) > 0
        if delante != frente:
            continue
        cosas.append((x + y, "p", x, y, a, i))
        if tiendas and i % 3 == 0:
            tx, ty = CENTRO[0] + (R + 46) * math.cos(a), CENTRO[1] + (R + 46) * math.sin(a)
            cosas.append((tx + ty, "t", tx, ty, a, i))
        if i % 5 == 2:
            fx, fy = CENTRO[0] + (R + 24) * math.cos(a + 0.05), CENTRO[1] + (R + 24) * math.sin(a + 0.05)
            cosas.append((fx + fy, "f", fx, fy, a, i))
    for _, k, x, y, a, i in sorted(cosas):
        if k == "p":
            tipo = ("conquistador", "aliado", "aliado", "conquistador_lanza", "aliado")[i % 5]
            G.persona(lz, iso, x, y, t, tipo=tipo, dir=(-math.cos(a), -math.sin(a)), seed=800 + i, h=40, accion="pelea" if i % 4 == 0 else None)
        elif k == "t":
            I.cono(lz, iso, x, y, 18, 30, (236, 226, 206) if i % 2 else (214, 120, 100))
        else:
            O.fuego(lz, iso, x, y, s=0.9, t=t, seed=i)
