# -*- coding: utf-8 -*-
"""Capa de interfaz del plano secuencia (capa 2, encima del mundo): contador de segundos, insignia de la versión,
lupas, gráficos, llamadas y paneles de cada frase. Parte 1: intro, reglas, aire y fuego (ui2: cuerpo -> cierre)."""
import math

import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, ancho_texto, h01, smooth
from mundo_comun import ventana, campana
from anclas import A, Z1, Z2, Z3, Z4, B0, PORTAL_IN, PORTAL_OUT, TOTAL
from estado import T_FUEGO, T_O2_FUERA
import kz_ui as KU
import kit_oxi as KO
import kit_bio as KB
import ui_base as UB
from ui_base import ent, pildora, texto_q, ROJO_O, TEAL, AZUL_OSC, NARANJA, MORADO, VERDE
import mundo_paisaje as MP
import mundo_espacio as ME
import gente as G


# ======================================================================== contador de segundos e insignia
def segundo(t):
    """(versión, número, alfa) del contador."""
    if A.cero_a - 0.4 < t < A.version_facil + 1.2:
        n = 0
        for tt, v in ((A.uno_f, 1), (A.dos_c, 2), (A.cinco_ra - 0.5, 3), (A.cinco_ra - 0.25, 4), (A.cinco_ra, 5)):
            if t >= tt:
                n = v
        return "A", n, ventana(t, A.cero_a - 0.1, A.version_facil + 0.8, 0.3, 0.4)
    if A.cero_s - 0.4 < t < A.bonito + 1.5:
        n = 0
        for tt, v in ((A.uno_ag, 1), (A.nosotros, 2), (A.cinco_rb - 0.5, 3), (A.cinco_rb - 0.25, 4), (A.cinco_rb, 5)):
            if t >= tt:
                n = v
        return "B", n, ventana(t, A.cero_s - 0.1, A.bonito + 1.0, 0.3, 0.5)
    return None, 0, 0.0


_CAMBIOS = [A.cero_a, A.uno_f, A.dos_c, A.cinco_ra - 0.5, A.cinco_ra - 0.25, A.cinco_ra, A.cero_s, A.uno_ag, A.nosotros,
            A.cinco_rb - 0.5, A.cinco_rb - 0.25, A.cinco_rb]


def contador(lz, t):
    v, n, a = segundo(t)
    if a <= 0.01 or v is None:
        return
    col = TEAL if v == "A" else (226, 70, 80)
    rp = 1.0
    for tc in _CAMBIOS:
        rp = max(rp, KU.repop(t, tc, 0.22, 0.35))
    x, y = W / 2, 74
    with lz.capa(2):
        lz.relleno(rect_red(x - 170 + 3, y - 44 + 5, 340, 112, 30), (10, 6, 40), alfa=0.22 * a)
        lz.relleno(rect_red(x - 170, y - 44, 340, 112, 30), (28, 24, 70), alfa=0.82 * a)
        lz.texto("SEGUNDO", x - 40, y - 4, 30, "geo", color=(220, 220, 240), borde=None, alfa=a, temblor=0.0)
        with lz.grupo(x + 98, y - 2, rp):
            lz.relleno(circulo(0, 0, 40, 40), col, alfa=a)
            lz.texto(str(n), 0, 3, 54, "geo_x", color=(255, 255, 255), borde=None, alfa=a, temblor=0.0)
        for i in range(6):
            cx = x - 136 + i * 34
            lz.relleno(circulo(cx, y + 42, 9, 16), col if i <= n else (80, 76, 120), alfa=a)


def insignia_version(lz, t):
    aA = ventana(t, A.cero_a - 0.6, A.version_facil + 1.0, 0.3, 0.4)
    aB = ventana(t, A.dificil - 0.2, A.bonito + 1.0, 0.3, 0.5)
    for a, letra, sub, col, t0 in ((aA, "VERSIÓN A", "solo el O2 del aire", TEAL, A.cero_a - 0.6),
                                   (aB, "VERSIÓN B", "todos los átomos de O", (226, 70, 80), A.dificil - 0.2)):
        if a <= 0.01:
            continue
        k = KU.pop(t, t0)
        with lz.capa(2):
            with lz.grupo(46, 46, k):
                w1 = ancho_texto(letra, "geo_x", 30) + 36
                w2 = UB.ancho_q(sub, 24) + 30
                lz.relleno(rect_red(3, 5, w1, 50, 18), (10, 6, 40), alfa=0.22 * a)
                lz.relleno(rect_red(0, 0, w1, 50, 18), col, alfa=a)
                lz.texto(letra, w1 / 2, 26, 30, "geo_x", color=(255, 255, 255), borde=None, alfa=a, temblor=0.0)
                lz.relleno(rect_red(0, 58, w2, 40, 16), (28, 24, 70), alfa=0.8 * a)
                texto_q(lz, w2 / 2, 78, sub, 24, (236, 236, 250), alfa=a, capa=2)


# ======================================================================== intro
def aliento(lz, t, S, t0, t1, oro=False):
    """Corriente de moléculas que entra por la nariz de la protagonista (inspiración)."""
    a = ventana(t, t0, t1, 0.2, 0.4)
    if a <= 0.01 or S is None:
        return
    nx, ny = S.pt(G.X_PROTA + 6, 192)
    for i in range(16):
        u = ((t - t0) * 0.55 + i / 16) % 1
        X0 = G.X_PROTA - 470 + 240 * h01(i, 2)   # cielo abierto por encima de los árboles (si no, parecen frutas)
        H0 = 340 + 150 * h01(i, 3)
        x0, y0 = S.pt(X0, H0)
        e = u ** 1.4
        x = lerp(x0, nx, e) + 30 * math.sin(u * 6 + i) * (1 - u) * S.k
        y = lerp(y0, ny, e) + 20 * math.cos(u * 5 + i) * (1 - u) * S.k
        tipo = "O2" if i % 5 == 0 else "N2"
        al = a * min(1.0, u * 5) * (1 - prog(u, 0.85, 1.0))
        col_o = None
        if oro:
            with lz.capa(2):
                lz.halo(x, y, 40 * S.k, (255, 220, 140), alfa=0.7 * al)
            tipo = "O2"
            col_o = (255, 204, 110)
        with lz.capa(2):
            KO.molecula(lz, x, y, 0.55 * S.k * (1 - 0.5 * e), tipo, rot=u * 4 + i, alfa=al, col_o=col_o)


def intro_espacio(lz, t, ctx):
    if ctx.get("tierra") is None:
        return
    ex, ey, r = ctx["tierra"]
    # cronómetro de 5 s y pulmones (1 respiración)
    k, a = ent(t, A.siempre, A.sitios - 0.5)
    if a > 0.01:
        fr = prog(t, A.cinco_i, A.cinco_i + 5.0)
        num = max(0, math.ceil(5 - 5 * fr - 1e-6)) if t > A.cinco_i else 5
        KB.cronometro(lz, 1300, 470, 150, frac=fr, numero=num, alfa=a, k=k, col=ROJO_O, t=t)
        pildora(lz, 1300, 690, "5 segundos", 34, k=k, alfa=a)
    k2, a2 = ent(t, A.parece, A.sitios - 0.5)
    if a2 > 0.01:
        inf = 0.5 - 0.5 * math.cos(2 * math.pi * clamp01((t - A.parece) / 5.0))
        with lz.capa(2):
            with lz.grupo(1660, 470, k2):
                lz.relleno(circulo(0, 0, 175, 50), (255, 255, 255), alfa=0.12 * a2)
                KB.pulmones(lz, 0, 20, 1.05, infla=inf, alfa=a2) if False else KB.pulmones(lz, 0, 20, 1.05, infla=inf)
        k3, a3 = ent(t, A.respirar_i - 0.2, A.sitios - 0.5)
        pildora(lz, 1660, 690, "≈ 1 respiración", 34, k=k3, alfa=a3 * a2)
    # dónde hay oxígeno: aire, agua, roca, tú
    burbujas = [((520, 330), "AIRE", A.sitios - 0.3, "aire"), ((1400, 330), "AGUA", A.sitios + 0.2, "agua"),
                ((520, 890), "ROCAS", A.sitios + 0.7, "roca"), ((1400, 890), "TU CUERPO", A.crees, "cuerpo")]
    for (bx, by), txt, t0, tipo in burbujas:
        kb, ab = ent(t, t0, A.mundo_i - 0.3)
        if ab <= 0.01:
            continue
        with lz.capa(2):
            ux, uy = ex - bx, ey - by
            d = math.hypot(ux, uy)
            P.discontinua(lz, [[bx + ux / d * 120 * kb, by + uy / d * 120 * kb], [ex - ux / d * r * 1.08, ey - uy / d * r * 1.08]],
                          (255, 255, 255, int(160 * ab)), 4, 14, 10, fase=t * 30)
            with lz.grupo(bx, by, kb):
                lz.relleno(circulo(4, 8, 112, 50), (10, 6, 40), alfa=0.22 * ab)
                lz.relleno(circulo(0, 0, 112, 50), (250, 248, 255), alfa=ab)
                icono(lz, tipo, t, ab)
        pildora(lz, bx, by + 150 * kb, txt, 32, k=kb, alfa=ab, fondo=ROJO_O, color=(255, 255, 255))
    titulo(lz, t)


def icono(lz, tipo, t, a=1.0, falta=0.0):
    """Icono dentro de una burbuja de r ≈ 100 (origen en el centro)."""
    if tipo == "aire":
        for k in range(3):
            lz.trazo(np.array([[-70, -40 + k * 34], [10, -40 + k * 34]]) + [0, 0], (170, 200, 240, int(255 * a)), 8, afinar=False)
        KO.molecula(lz, 30, 10, 1.3, "O2", rot=0.3 * math.sin(t), alfa=a, falta_o=falta, hueco=1)
    elif tipo == "agua":
        gota = np.array([[0, -80], [42, -10], [44, 30], [0, 70], [-44, 30], [-42, -10]], float)
        from motor import catmull
        lz.relleno(catmull(gota, 6, True), (110, 180, 250), alfa=a)
        KO.molecula(lz, 0, 14, 1.15, "H2O", rot=0.2 * math.sin(t), alfa=a, falta_o=falta, hueco=1)
    elif tipo == "roca":
        lz.relleno(np.array([[-74, 40], [-60, -30], [-10, -62], [50, -44], [76, 20], [40, 56], [-30, 60]]), (170, 150, 176), alfa=a)
        lz.relleno(np.array([[-60, -30], [-10, -62], [50, -44], [10, -20]]), (200, 184, 206), alfa=a)
        for i, (dx, dy) in enumerate(((-30, 10), (20, -10), (30, 30), (-10, 36), (-40, -16))):
            KO.atomo(lz, dx, dy, 12 if i % 2 else 10, KO.COL_AT["O"] if i % 2 == 0 else KO.COL_AT["Si"], a * (1 - falta if i % 2 == 0 else 1))
    elif tipo == "cuerpo":
        lz.relleno(circulo(0, -50, 26, 30), (240, 186, 150), alfa=a)
        lz.relleno(rect_red(-36, -20, 72, 90, 30), (140, 108, 200), alfa=a)
        KO.atomo(lz, 30, 30, 16, KO.COL_AT["O"], a * (1 - falta))


def titulo(lz, t):
    k, a = ent(t, A.mundo_i - 0.1, A.reglas - 0.7, lento=1.2)
    if a <= 0.01:
        return
    with lz.capa(2):
        with lz.grupo(W / 2, 170, k):
            l1a, l1b = "¿Qué pasaría si el ", "OXÍGENO"
            px = 78
            w1 = ancho_texto(l1a, "geo_x", px)
            w2 = ancho_texto(l1b, "geo_x", px)
            x0 = -(w1 + w2) / 2
            P.rotulo(lz, x0 + w1 / 2, 0, l1a, px, fuente="geo_x", alfa=a, capa=2)
            lz.halo(x0 + w1 + w2 / 2, 0, w2 * 0.7, (255, 90, 100), alfa=0.35 * a)
            P.rotulo(lz, x0 + w1 + w2 / 2, 0, l1b, px, color=(255, 110, 120), fuente="geo_x", alfa=a, capa=2)
            P.rotulo(lz, 0, 96, "desapareciera 5 segundos?", px, fuente="geo_x", alfa=a, capa=2)


def kuri_intro(lz, t, ctx):
    if ctx.get("tierra") is None:
        return
    a = ventana(t, Z1[1] - 0.6, Z2[0] + 0.3, 0.6, 0.4)
    if a <= 0.01:
        return
    if t < A.reglas - 0.5:
        x, y, m = 1700, 900, (-0.8, -0.3)
        if A.sitios + 0.4 < t < A.mundo_i + 2:
            x, y = 1760, 610
    else:
        x, y, m = 760, 250, (0.8, 0.2)
    xx = float(np.interp(t, [A.reglas - 0.9, A.reglas + 0.6], [1700 if t < A.mundo_i + 3 else 1760, 760]))
    yy = float(np.interp(t, [A.reglas - 0.9, A.reglas + 0.6], [900 if t < A.sitios else 560, 250]))
    if A.reglas - 0.9 < t < A.reglas + 0.6:
        x, y = xx, yy
    with lz.capa(2):
        ME.kuri_espacio(lz, t, x, y, 0.62, mirar=m, aleteo=0.6 if A.reglas < t < A.reglas + 1.5 else 0.0, alfa=a)


# ======================================================================== reglas
def _panel(lz, x, y, w, h, a, k=1.0, col=(30, 26, 80)):
    with lz.capa(2):
        with lz.grupo(x, y, k):
            lz.relleno(rect_red(-w / 2 + 4, -h / 2 + 7, w, h, 30), (6, 4, 24), alfa=0.3 * a)
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, 30), col, alfa=0.86 * a)
            lz.relleno(rect_red(-w / 2, -h / 2, w, 6, 3), (255, 255, 255), alfa=0.0)


_MOLS_R = [(-280, -90), (-150, 40), (-40, -110), (90, 20), (210, -70), (300, 70), (-260, 100), (40, 120)]


def reglas(lz, t, ctx):
    k, a = ent(t, A.reglas - 0.15, A.dos_formas - 0.2)
    if a > 0.01:
        pildora(lz, 1300, 150, "LAS REGLAS DEL JUEGO", 40, k=k, alfa=a, fondo=(255, 214, 90), color=AZUL_OSC)
    k, a = ent(t, A.deja - 1.2, A.dos_formas - 0.2)
    if a > 0.01:
        _panel(lz, 1300, 480, 820, 440, a, k)
        falta = e_out(prog(t, A.deja, A.deja + 0.3)) * (1 - e_out(prog(t, A.vuelve_r, A.vuelve_r + 0.3)))
        with lz.capa(2):
            with lz.grupo(1300, 470, k):
                for i, (mx, my) in enumerate(_MOLS_R):
                    bob = 8 * math.sin(t * 1.5 + i)
                    KO.molecula(lz, mx, my + bob, 1.2, "O2", rot=0.4 * math.sin(t * 0.8 + i), alfa=a, falta_o=falta, hueco=1.0)
                    if t > A.exactamente:
                        UB.check(lz, mx + 34, my + bob - 34, 12 * KU.pop(t, A.exactamente + 0.06 * i), (120, 230, 150), a)
                    if A.vuelve_r < t < A.vuelve_r + 0.6:
                        lz.halo(mx, my + bob, 60, (255, 230, 170), alfa=a * (1 - prog(t, A.vuelve_r, A.vuelve_r + 0.6)))
                fr = prog(t, A.deja, A.vuelve_r)
                if A.deja - 0.2 < t < A.vuelve_r + 0.8:
                    KB.cronometro(lz, 330, -150, 46, frac=fr, numero=max(0, math.ceil(5 - 5 * fr - 1e-6)), alfa=a, col=ROJO_O)
        k2, a2 = ent(t, A.exactamente - 0.1, A.dos_formas - 0.2)
        pildora(lz, 1300, 650, "vuelve exactamente a su sitio", 30, k=k2, alfa=a2 * a)
    # las dos versiones
    hlA = campana(t, A.primera - 0.2, A.segunda - 0.2) if t < A.segunda else 0.0
    hlB = campana(t, A.segunda - 0.2, A.facil - 0.3) if A.segunda - 0.2 < t < A.facil else 0.0
    dimA = 1 - 0.45 * (hlB > 0.05)
    dimB = 1 - 0.45 * (hlA > 0.05)
    if t > A.facil - 0.3:
        hlA, dimB = 1.0, 0.55
    salida = 1 - e_in(prog(t, Z2[0] - 0.1, Z2[0] + 0.5))
    for i, (cx, letra, sub, col, t0, hl, dim, tipo) in enumerate((
            (1080, "VERSIÓN A", "solo el O2 del aire", TEAL, A.dos_formas, hlA, dimA, "A"),
            (1530, "VERSIÓN B", "todos los átomos de O", (226, 70, 80), A.dos_formas + 0.25, hlB, dimB, "B"))):
        kc = KU.pop(t, t0)
        ac = min(1.0, kc * 3) * salida
        if ac <= 0.01:
            continue
        kc *= 1 + 0.07 * hl
        _panel(lz, cx, 560, 400, 540, ac * dim, kc, col=mezcla((30, 26, 80), col, 0.18 * hl))
        with lz.capa(2):
            with lz.grupo(cx, 560, kc):
                pildora(lz, 0, -210, letra, 34, fondo=col, color=(255, 255, 255), alfa=ac)
                if tipo == "A":
                    for j, (mx, my, tp) in enumerate(((-110, -80, "N2"), (40, -100, "N2"), (-60, 20, "O2"), (100, 10, "N2"),
                                                      (-120, 110, "N2"), (60, 120, "N2"))):
                        brillo = hl if tp == "O2" else 0.0
                        KO.molecula(lz, mx, my + 6 * math.sin(t * 1.4 + j), 1.2 if tp == "O2" else 1.0, tp, rot=0.3 * math.sin(t + j),
                                    alfa=ac * (1.0 if tp == "O2" or hl < 0.3 else 0.55), brillo_o=brillo)
                else:
                    parp = 0.5 + 0.5 * math.sin(t * 9) if A.ultimo - 0.3 < t < A.ultimo + 1.6 else 1.0
                    with lz.grupo(-90, -60, 0.62):
                        icono(lz, "agua", t, ac)
                    with lz.grupo(90, -60, 0.62):
                        icono(lz, "roca", t, ac)
                    with lz.grupo(-90, 90, 0.62):
                        icono(lz, "cuerpo", t, ac)
                    with lz.grupo(90, 90, 0.62):
                        icono(lz, "aire", t, ac)
                    if hl > 0.05:
                        for (dx, dy) in ((-90, -50), (110, -60), (-70, 110), (110, 96)):
                            lz.halo(dx, dy, 40, (255, 90, 100), alfa=0.6 * hl * parp)
                pildora(lz, 0, 215, sub, 26, fondo=(250, 248, 255), alfa=ac)


# ======================================================================== aire
_MOLS_AIRE = [(-120, -100, "N2"), (40, -130, "N2"), (130, -40, "O2"), (-40, -10, "N2"), (-150, 40, "N2"), (100, 80, "N2"),
              (-60, 130, "O2"), (60, 160, "N2"), (150, 160, "N2"), (-160, 150, "N2")]


def lupa_aire(lz, t, S, t_in, t_out, vuelve=None):
    k, a = ent(t, t_in, t_out)
    if a <= 0.01:
        return
    if vuelve is None:
        falta = e_out(prog(t, T_O2_FUERA, T_O2_FUERA + 0.35))
    else:
        falta = 1 - e_out(prog(t, vuelve, vuelve + 0.4))

    def cont(lz):
        lz.relleno(circulo(0, 0, 230, 40), (150, 200, 250))
        for i, (mx, my, tp) in enumerate(_MOLS_AIRE):
            dx = 30 * math.sin(t * 0.7 + i * 1.3)
            dy = 24 * math.cos(t * 0.6 + i)
            KO.molecula(lz, mx + dx, my + dy, 1.25, tp, rot=t * 0.6 + i, falta_o=falta if tp == "O2" else 0.0, hueco=1.0)
            if tp == "O2" and vuelve is None and T_O2_FUERA < t < T_O2_FUERA + 0.7:
                lz.halo(mx + dx, my + dy, 70, (255, 200, 200), alfa=1 - prog(t, T_O2_FUERA, T_O2_FUERA + 0.7))
    obj = S.pt(G.X_PROTA - 250, 520) if S is not None else None
    KB.lupa(lz, 1450, 340, 210, cont, fondo=(150, 200, 250), k=k, alfa=a, objetivo=obj)


def aire(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    lupa_aire(lz, t, S, A.cero_a - 0.3, A.ligero - 0.1)
    k, a = ent(t, A.cada_cinco - 0.1, A.ligero - 0.1)
    pildora(lz, 1450, 600, "1 de cada 5 moléculas es O2", 30, k=k, alfa=a)
    # manómetro
    k, a = ent(t, A.ligero - 0.1, A.montana - 0.9)
    if a > 0.01:
        v = lerp(101.3, 80.0, e_out(prog(t, A.presion - 0.1, A.quinta + 0.5)))
        KB.manometro(lz, 1480, 360, 165, v, 0, 120, t, marcas=(0, 20, 40, 60, 80, 100, 120), texto="kPa", alfa=a, k=k)
        k2, a2 = ent(t, A.quinta, A.montana - 0.9)
        pildora(lz, 1480, 600, "−21 % de presión", 32, k=k2, alfa=a2, fondo=ROJO_O, color=(255, 255, 255))
    # montaña de 2 000 m
    am = ventana(t, A.montana - 1.0, A.oidos - 0.4, 0.4, 0.4)
    if am > 0.01:
        with lz.capa(2):
            Xr = -2330
            x0, y0 = S.pt(Xr, 0)
            x1, y1 = S.pt(Xr, MP.H_MONTE)
            fr = e_out(prog(t, A.montana - 0.8, A.montana + 0.2))
            lz.trazo(np.array([[x0, y0], [x0, y0 + (y1 - y0) * fr]]), (255, 255, 255, int(255 * am)), 6, afinar=False)
            for i in range(5):
                yy = y0 + (y1 - y0) * i / 4
                if i / 4 <= fr + 1e-3:
                    lz.trazo(np.array([[x0 - 14, yy], [x0 + 14, yy]]), (255, 255, 255, int(255 * am)), 5, afinar=False)
            if fr > 0.95:
                pildora(lz, x0 + 10, y1 - 40, "2 000 m", 34, k=KU.pop(t, A.montana + 0.2), alfa=am, fondo=(255, 214, 90))
            # «te suben de golpe»: trayecto punteado del parque a la cima
            xs, ys = S.pt(G.X_PROTA, 30)
            xc, yc = S.pt(MP.X_MONTE, MP.H_MONTE + 30)
            pts = np.array([[lerp(xs, xc, u), lerp(ys, yc, u) - 260 * math.sin(math.pi * u)] for u in np.linspace(0, 1, 30)])
            P.discontinua(lz, pts, (255, 255, 255, int(200 * am)), 5, 18, 12, fase=-t * 40,
                          frac=e_out(prog(t, A.dos_mil - 0.3, A.dos_mil + 0.5)))
            u = e_inout(prog(t, A.dos_mil, A.dos_mil + 0.6))
            if u > 0:
                q = pts[min(29, int(u * 29))]
                lz.relleno(circulo(q[0], q[1] - 34, 14, 20), (250, 204, 168), alfa=am)
                lz.relleno(rect_red(q[0] - 14, q[1] - 20, 28, 40, 12), (140, 108, 200), alfa=am)
    # oídos: el tímpano se abomba
    k, a = ent(t, A.oidos - 0.2, A.cielo - 0.3)
    if a > 0.01:
        b = 0.9 * e_out(prog(t, A.golpe - 0.2, A.golpe + 0.4))
        rot = e_out(prog(t, A.demasiado - 0.1, A.demasiado + 0.3))

        def cont(lz):
            lz.relleno(circulo(0, 0, 300, 40), (60, 40, 80))
            KB.oido(lz, 0, 0, 0.95, t, bombeo=b, rotura=rot)
            for j in range(3):
                yy = -50 + j * 50
                UB.flecha(lz, (40, yy), (-30 - 30 * b, yy), (255, 230, 120), 7, 20, alfa=b)
            if rot > 0.05:
                lz.halo(-50 - 34 * b, 0, 90, (255, 255, 255), alfa=0.8 * (1 - prog(t, A.demasiado + 0.2, A.demasiado + 1.0)))
        obj = S.pt(G.X_PROTA - 30, 190)
        KB.lupa(lz, 1420, 430, 270, cont, fondo=(60, 40, 80), k=k, alfa=a, objetivo=obj)
        k2, a2 = ent(t, A.oidos + 0.2, A.cielo - 0.3)
        pildora(lz, 1420, 740, "tímpano", 30, k=k2, alfa=a2)
        # gráfico: avión (poco a poco) vs. esto (de golpe)
        k3, a3 = ent(t, A.despegar - 0.6, A.cielo - 0.3)
        if a3 > 0.01:
            _panel(lz, 1420, 920, 560, 200, a3, k3)
            with lz.capa(2):
                with lz.grupo(1420, 920, k3):
                    lz.trazo(np.array([[-240, -70], [-240, 70], [250, 70]]), (200, 200, 230, int(255 * a3)), 4, afinar=False)
                    fr = prog(t, A.despegar - 0.4, A.despegar + 1.2)
                    xs_ = np.linspace(-240, -240 + 480 * fr, 30)
                    lz.trazo(np.stack([xs_, -50 + 100 * (xs_ + 240) / 480], 1), (120, 180, 255, int(255 * a3)), 7, afinar=False)
                    lz.trazo(np.array([[-230, -50], [-224, 50], [-224 + 470 * fr, 50]]), (255, 100, 110, int(255 * a3)), 7,
                             afinar=False)
                    lz.texto("avión: minutos", 90, -40, 26, "geo", color=(150, 200, 255), borde=None, alfa=a3, temblor=0.0)
                    lz.texto("aquí: de golpe", -40, 24, 26, "geo", color=(255, 140, 150), borde=None, alfa=a3, temblor=0.0)
    # cielo azul: la luz del Sol rebota en el nitrógeno
    ac = ventana(t, A.cielo + 0.4, A.uno_f - 0.4, 0.5, 0.5)
    if ac > 0.01:
        with lz.capa(2):
            for i in range(9):
                cx = 220 + (i * 211) % 1500 + 30 * math.sin(t * 0.5 + i)
                cy = 160 + (i * 137) % 520 + 20 * math.cos(t * 0.6 + i)
                fr = (t * 1.2 + i * 0.37) % 1
                for j in range(6):
                    ang = j / 6 * 2 * math.pi + i
                    r0, r1 = 40 + 60 * fr, 70 + 60 * fr
                    lz.trazo(np.array([[cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)], [cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)]]),
                             (120, 180, 255, int(200 * ac * (1 - fr))), 5, afinar=False)
                KO.molecula(lz, cx, cy, 1.0, "N2", rot=t * 0.4 + i, alfa=ac)
            for i in range(3):
                cx = 400 + i * 480
                KO.fantasma(lz, cx - 15, 600 + 40 * i % 3, 20, (255, 255, 255), alfa=0.6 * ac)
                KO.fantasma(lz, cx + 15, 600 + 40 * i % 3, 20, (255, 255, 255), alfa=0.6 * ac)
        k, a = ent(t, A.nitrogeno - 0.1, A.uno_f - 0.4)
        pildora(lz, 1500, 860, "N2 ≈ 78 % del aire", 36, k=k, alfa=a * ac, fondo=(84, 140, 240), color=(255, 255, 255))


# ======================================================================== fuego
def fuego(lz, t, ctx):
    S = ctx.get("S")
    if S is None:
        return
    for (Xo, Ho, txt, t0, par) in ((-250, 125, "velas", A.velas, 1.0), (395, 130, "fogones", A.fogones, 1.0),
                                   (MP.INC_X, 760, "incendios", A.incendios, 0.42)):
        k, a = ent(t, t0 - 0.05, A.coches - 0.5)
        if a > 0.01:
            Sx = S if par == 1.0 else S.par(par)
            x, y = Sx.pt(Xo, Ho)
            KU.llamada(lz, x, y, txt, color=NARANJA, px=34, k=k, alfa=a)
    ka, aa = ent(t, A.arder - 0.5, A.coches + 0.8)
    if aa > 0.01:
        rot = e_in(prog(t, A.arder + 0.1, A.arder + 1.2))
        with lz.capa(2):
            lz.relleno(circulo(1560, 330, 230 * ka, 50), (28, 24, 70), alfa=0.6 * aa)
            KO.triangulo_fuego(lz, 1560, 340, 0.85 * ka, rotura=rot, alfa=aa, t=t)
    # coches: sin motor, siguen rodando
    k, a = ent(t, A.coches + 0.2, A.aviones - 1.0)
    if a > 0.01:
        x, _ = MP.pos_coche(t, 1)
        xx, yy = S.pt(x, 60)
        KU.llamada(lz, xx, yy, "motor apagado", color=MORADO, px=30, k=k, alfa=a)
    if A.coches - 0.5 < t < A.aviones:
        with lz.capa(2):
            for i in range(len(MP.COCHES)):
                x, v = MP.pos_coche(t, i)
                if v < 15:
                    continue
                for j in range(3):
                    xa, ya = S.pt(x - 110 - 20 * j, -100 + 18 * j)
                    lz.trazo(np.array([[xa, ya], [xa - v * 0.35 * S.k, ya]]), (255, 255, 255, 170), 4, afinar=False)
    # aviones
    k, a = ent(t, A.aviones - 0.1, A.piedra - 0.4)
    pildora(lz, W / 2, 190, "miles de aviones en el aire", 34, k=k, alfa=a)
    k, a = ent(t, A.apagan_av - 0.1, A.planea + 0.6)
    if a > 0.01:
        X, Hh = G.pos_jumbo(t)
        x, y = S.pt(X - 20, Hh + 110)
        KU.llamada(lz, x, y, "4 motores apagados", color=(226, 70, 80), px=30, k=k, alfa=a)
    # piedra vs. planeo
    ap = ventana(t, A.piedra - 0.3, A.y1982 - 0.2, 0.3, 0.4)
    if ap > 0.01:
        X, Hh = G.pos_jumbo(A.piedra - 0.3)
        with lz.capa(2):
            xs, ys = S.pt(X - 330, Hh)
            xg, yg = S.pt(X - 330, 0)
            fr = e_in(prog(t, A.piedra, A.piedra + 0.7))
            P.discontinua(lz, [[xs, ys], [xs, ys + (yg - ys) * fr]], (255, 255, 255, int(220 * ap)), 5, 16, 12)
            lz.relleno(np.array([[-20, -12], [6, -22], [22, -4], [14, 16], [-14, 18]]) * S.k * 1.4 + [xs, ys + (yg - ys) * fr],
                       (150, 140, 160), alfa=ap)
            Xa, Ha = G.pos_jumbo(t)
            fr2 = e_out(prog(t, A.planea - 0.1, A.planea + 0.9))
            pts = [S.pt(Xa + 300 + 3000 * u * fr2, Ha - 200 * u * fr2) for u in np.linspace(0, 1, 20)]
            P.discontinua(lz, pts, (255, 236, 150, int(240 * ap)), 6, 22, 14, fase=-t * 30)
        k, a = ent(t, A.piedra - 0.05, A.y1982 - 0.2)
        x, y = S.pt(X - 330, Hh + 60)
        pildora(lz, x, y, "piedra", 28, k=k * min(1.0, S.k * 1.4), alfa=a)
        k, a = ent(t, A.planea, A.y1982 - 0.2)
        x, y = S.pt(G.pos_jumbo(t)[0] + 1300, G.pos_jumbo(t)[1] - 10)
        pildora(lz, min(x, W - 160), y, "planea", 32, k=k, alfa=a, fondo=(255, 214, 90))
    panel_1982(lz, t)
    # centrales eléctricas
    k, a = ent(t, A.centrales - 0.1, A.llama - 0.4)
    if a > 0.01:
        x, y = S.pt(MP.X_CENTRAL + 190, 620)
        KU.llamada(lz, x, y, "central térmica", color=MORADO, px=30, k=k, alfa=a)
    k, a = ent(t, A.sesenta - 0.3, A.llama + 0.2)
    if a > 0.01:
        cr = e_out(prog(t, A.sesenta - 0.1, A.sesenta + 0.9))
        KB.tarta(lz, 380, 360, 160, 0.59, col=(110, 96, 120), resto=(120, 220, 160), texto="59 %", sub="fósiles", k=k, alfa=a,
                 crece=cr)
        pildora(lz, 380, 590, "de la electricidad del mundo (2024)", 26, k=k, alfa=a)
    k, a = ent(t, A.seguridad - 0.1, A.sol_f - 0.6)
    if a > 0.01:
        x, y = S.pt(MP.X_CENTRAL - 20, 460)
        pildora(lz, x, y, "apagado de seguridad", 30, k=k, alfa=a, fondo=(226, 70, 80), color=(255, 255, 255), icono="cruz")
    k, a = ent(t, A.apagones - 0.1, A.sol_f - 0.6)
    if a > 0.01:
        x, y = S.pt(300, 640)
        pildora(lz, x, y, "APAGONES", 40, k=k, alfa=a, fondo=(28, 24, 70), color=(255, 214, 90))
    # el Sol no es fuego: fusión nuclear
    asol = ventana(t, A.brillando - 0.2, A.dos_c + 0.6, 0.4, 0.5)
    if asol > 0.01:
        x, y, r = MP.sol_paisaje(lz, t, S) if False else _sol_pant(S)
        ap = e_out(prog(t, A.fusion - 0.3, A.fusion + 0.9))
        with lz.capa(2):
            P.sol_corte(lz, x, y, r * 1.001, t, apertura=ap * asol, nucleo=1.0)
        k, a = ent(t, A.no_es_fuego - 0.1, A.dos_c + 0.4)
        if a > 0.01:
            with lz.capa(2):
                with lz.grupo(x - r - 230, y - 120, k):
                    lz.relleno(circulo(0, 0, 70, 30), (250, 248, 255), alfa=a)
                    KO.llama(lz, 0, 34, 0.75, t, 2, 1.0, capa=2)
                    UB.prohibido(lz, 0, 0, 62, a)
            pildora(lz, x - r - 230, y + 10, "no es fuego", 30, k=k, alfa=a)
        k, a = ent(t, A.fusion, A.dos_c + 0.4)
        pildora(lz, x + r + 210, y - 60, "fusión nuclear", 34, k=k, alfa=a, fondo=(255, 214, 90))
        k, a = ent(t, A.necesita - 0.1, A.dos_c + 0.4)
        pildora(lz, x + r + 210, y + 30, "no necesita O2", 32, k=k, alfa=a, icono="cruz", fondo=(226, 70, 80), color=(255, 255, 255))


def _sol_pant(S):
    Ss = S.par(0.04)
    x, y = Ss.pt(MP.SOL_X, MP.SOL_H)
    return x, y, 2250 * Ss.k


def panel_1982(lz, t):
    a = ventana(t, A.y1982 - 0.5, A.centrales - 1.0, 0.4, 0.5)
    if a <= 0.01:
        return
    UB.oscurecer_fondo(lz, 0.45 * a)
    k = KU.pop(t, A.y1982 - 0.5)
    cx, cy, R = 1160, 620, 380

    def alt_y(km):
        return 240 - 500 * km / 11.3

    def cont(lz):
        lz.degradado(circulo(0, 0, R, 60), (36, 44, 104), (12, 14, 46), (0, -R), (0, R))
        for i in range(40):
            lz.relleno(circulo((h01(i, 1) - 0.5) * 2 * R, (h01(i, 2) - 0.5) * 1.4 * R - 100, 2 + 2 * h01(i, 3), 8), (240, 240, 255),
                       alfa=0.7)
        # volcán Galunggung y su ceniza
        lz.relleno(np.array([[-430, 330], [-300, 180], [-250, 150], [-200, 180], [-60, 330]]), (60, 52, 70))
        lz.halo(-250, 150, 60, (255, 120, 60), alfa=0.8)
        for i in range(22):   # columna de ceniza que sube del volcán y se extiende arriba
            u = h01(i, 5)
            ax = -250 + (60 + 160 * u) * (h01(i, 6) - 0.3) + 8 * math.sin(t * 0.4 + i)
            ay = 140 - 400 * u
            lz.relleno(circulo(ax, ay, 26 + 26 * u, 20), (130, 122, 140), alfa=0.28)
        # pista
        lz.relleno(rect_red(80, 262, 260, 16, 6), (90, 96, 120))
        for i in range(4):
            lz.relleno(rect_red(100 + i * 54, 268, 26, 4, 2), (255, 255, 240))
        # regla de altitud
        lz.trazo(np.array([[300, alt_y(11.3)], [300, alt_y(0)]]), (220, 220, 250, 220), 4, afinar=False)
        for km, txt in ((11.3, "11,3 km"), (3.7, "3,7 km"), (0, "0")):
            lz.trazo(np.array([[288, alt_y(km)], [312, alt_y(km)]]), (220, 220, 250, 220), 4, afinar=False)
            lz.texto(txt, 236 if km else 276, alt_y(km), 22, "geo", color=(220, 220, 250), borde=None, temblor=0.0)
        # trayectoria del jumbo
        tA, tB, tC, tD = A.y1982, A.planeo, A.encender, A.victima
        if t < tB:
            u = prog(t, tA - 0.4, tB)
            x, y = lerp(-250, -60, u), alt_y(11.3)
        elif t < tC:
            u = e_inout(prog(t, tB, tC))
            x, y = lerp(-60, 120, u), lerp(alt_y(11.3), alt_y(3.7), u)
        else:
            u = e_inout(prog(t, tC, tD + 0.2))
            x, y = lerp(120, 290, u), lerp(alt_y(3.7), 252, u)
        if t > tB:
            P.discontinua(lz, [[-60, alt_y(11.3)], [x, y]], (255, 236, 150, 200), 4, 14, 10)
        mot = 1.0 if t < A.cuatro_m else (e_out(prog(t, tC, tC + 0.5)))
        ang = 0.0 if t < tB else (0.12 if t < tC else 0.05)
        KO.avion(lz, x, y, 0.32, t, motores=mot, rot=ang, dir=1, luz=1.0)
        if A.cuatro_m < t < tC:
            for j in range(4):
                UB.cruz(lz, x - 45 + j * 30, y + 34, 8, (255, 110, 110), 1.0)

    KB.lupa(lz, cx, cy, R, cont, fondo=(20, 24, 60), k=k, alfa=a)
    kk, aa = ent(t, A.y1982 - 0.1)
    pildora(lz, cx, cy - R * k - 10, "1982 · British Airways 9", 34, k=kk, alfa=aa * a, fondo=(255, 214, 90))
    kk, aa = ent(t, A.cuatro_m - 0.1, A.planeo + 0.6)
    pildora(lz, cx - 60, cy - 150, "ceniza volcánica: 4 motores apagados", 26, k=kk, alfa=aa * a, fondo=(226, 70, 80),
            color=(255, 255, 255))
    kk, aa = ent(t, A.siete - 0.2, A.encender + 0.4)
    pildora(lz, cx - 60, cy + 40, "planeó más de 7 km", 28, k=kk, alfa=aa * a)
    kk, aa = ent(t, A.encender - 0.1)
    pildora(lz, cx + 90, cy + 120, "motores encendidos", 26, k=kk, alfa=aa * a * (1 - prog(t, A.victima - 0.2, A.victima + 0.2)),
            fondo=(120, 220, 160))
    kk, aa = ent(t, A.victima - 0.1)
    pildora(lz, cx + 120, cy + 300, "0 víctimas", 36, k=kk, alfa=aa * a, fondo=(120, 220, 160), icono="check")


# ======================================================================== orquesta
def dibujar(lz, t, ctx, est):
    import ui2
    if t < Z2[1] + 0.5:
        aliento(lz, t, ctx.get("S"), A.respira - 0.3, A.imagina + 0.4)
        intro_espacio(lz, t, ctx)
        kuri_intro(lz, t, ctx)
        if t > A.reglas - 1:
            reglas(lz, t, ctx)
    if A.cero_a - 1 < t < A.uno_f + 0.5:
        aire(lz, t, ctx)
    if A.uno_f - 1 < t < A.dos_c + 1.2:
        fuego(lz, t, ctx)
    ui2.dibujar(lz, t, ctx, est)
    contador(lz, t)
    insignia_version(lz, t)


def post(img, t, ctx, est):
    import ui2
    return ui2.post(img, t, ctx, est)
