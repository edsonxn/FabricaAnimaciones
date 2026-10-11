# -*- coding: utf-8 -*-
"""Mundos de la escena 7 (la guerra del Mixtón): el peñol en diorama isométrico (mesa de roca escalonada, chozas, fogatas, honderos arriba;
españoles y aliados que atacan la base y se retiran bajo una lluvia de piedras), el Templo Mayor en 2D, el caballo 2D con jinete
(galope y caída) y el sobre del mensajero."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_deco as DC
import kz_gente_iso as G
import kz_pers2d as K2
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_in, e_inout, e_back, W, H
from mundos_b import terraza, iso_en
from mundos_c import CerroVentanas

ROCA_M = ((150, 100, 132), (178, 116, 124), (200, 138, 118), (164, 106, 128))
TOPE_M = (132, 168, 96)
ZT = 280.0                                          # altura de la cumbre del peñol (unidades de mundo)
# bloques de la mesa: (x, y, w, d, h, z0) — escalonada e irregular para que no sea una caja
BLOQUES = [(-200, -180, 360, 320, 70, 0), (-176, -156, 312, 272, 70, 70), (-154, -134, 266, 228, 70, 140), (-130, -112, 220, 186, 70, 210),
           (-236, -70, 40, 130, 110, 0), (156, -170, 40, 100, 150, 0), (-150, 140, 80, 30, 46, 0), (60, 140, 60, 26, 80, 0), (100, 112, 52, 30, 120, 70)]
CHOZAS = [(-110, -95), (-62, -100), (-14, -96), (36, -92), (-112, -40), (58, -44)]
FOGATAS = [(-80, 10), (10, -30), (60, 20)]
TOP = (-130, -112, 90, 74)                       # x0, y0, x1, y1 de la cumbre


class PenolIso:
    """El peñol del Mixtón con su llano. objetos(t, asalto, retirada, piedras): asalto 0..1 = avance de los atacantes hacia la base;
    retirada 0..1 = media vuelta y huida; piedras 0..1 = intensidad de la lluvia de piedras desde la cumbre."""

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -360, -320, 520, 520, color_top=(168, 182, 104), t=t, seed=41, esp=36)
        DC.parches(lz, iso, -360, -320, 520, 520, (168, 182, 104), n=24, var=22, seed=42, alfa=0.5, tam=(50, 110))
        I.camino(lz, iso, [(-340, 470), (-180, 360), (-40, 300), (200, 300), (480, 380)], 30, (226, 206, 160), borde=(206, 184, 140))
        DC.hierba(lz, iso, -360, -320, 520, 520, n=150, seed=43, t=t, color=(120, 168, 88), flores=0.06)

    def penol(self, lz, iso, t):
        for (x, y, w, d, h, z0) in BLOQUES:
            terraza(lz, iso_en(iso, z0), x, y, w, d, h, estratos=ROCA_M, tope=TOPE_M, seed=int(z0 // 70) + int(x) % 3)
        # matorral en las cornisas de cada escalón (frente y derecha)
        for k, (x, y, w, d, hh, z0) in enumerate(BLOQUES[:3]):
            ie = iso_en(iso, z0 + hh)
            for i in range(int(w // 36)):
                O.arbusto(lz, ie, x + 18 + 36 * i, y + d - 9, r=7 + 3 * h01(k, i), seed=k * 10 + i, flores=(255, 200, 90) if i % 4 == 0 else None)
            for i in range(int(d // 40)):
                O.maguey(lz, ie, x + w - 9, y + 20 + 40 * i, s=0.7, seed=k * 10 + i, t=t)
        it = iso_en(iso, ZT)
        x0, y0, x1, y1 = TOP
        I.cuadricula(lz, it, x0 + 8, y0 + 8, x1 - 8, y1 - 8, 30, color=(255, 255, 255), alfa=0.05)
        for i in range(7):
            O.maguey(lz, it, x0 + 14 + 32 * i, y1 - 6, s=0.85, seed=i, t=t)
        for i in range(4):
            O.arbol(lz, it, x1 - 10, y0 + 16 + 46 * i, h=40, seed=i + 5, t=t)
        for (x, y) in CHOZAS:
            CerroVentanas.choza(lz, iso, x, y, ZT)
        for i, (x, y) in enumerate(FOGATAS):
            O.fuego(lz, iso, x, y, s=1.1, t=t, seed=i, z=ZT)
            O.humo(lz, iso, x, y, ZT + 20, t, n=6, s=1.0, color=(220, 214, 236), seed=i, alfa=0.55)

    def defensores(self, lz, iso, t, n=16, piedras=0.0):
        """Honderos y lanceros en el borde de la cumbre (de frente al llano)."""
        gente = []
        for i in range(n):
            x = -122 + 196 * (i + 0.5) / n + 5 * (h01(7, i) - 0.5)
            y = 46 + 18 * h01(8, i)
            tipo = ("honda", "caxcan_lanza", "caxcan_mazo", "caxcan", "caxcan_jefe")[i % 5] if i != 7 else "caxcan_jefe"
            accion = "pelea" if piedras > 0.1 else ("vitorea" if i % 4 == 0 else None)
            gente.append((x + y, x, y, tipo, accion, i))
        for _, x, y, tipo, accion, i in sorted(gente):
            G.persona(lz, iso, x, y, t, tipo=tipo, dir=(0.3, 1.0), seed=600 + i, h=40, accion=accion, z=ZT)

    def atacantes(self, lz, iso, t, asalto, retirada, n=26):
        """Conquistadores y aliados en el llano: avanzan hacia la base del peñol (asalto) y luego huyen (retirada)."""
        gente = []
        for i in range(n):
            col, fila = i % 9, i // 9
            x0 = -170 + 36 * col + 10 * (fila % 2) + 8 * h01(3, i)
            y_lejos, y_cerca = 430 + 34 * fila, 190 + 26 * fila
            u = e_inout(asalto) * (1 - e_in(retirada) * 1.15) + 0.04 * math.sin(t * 2 + i) * asalto
            y = y_lejos + (y_cerca - y_lejos) * u
            huye = retirada > 0.05
            tipo = ("conquistador", "conquistador_lanza", "aliado", "aliado", "conquistador")[i % 5] if i != 4 else "capitan_esp"
            vel = 1.6 if (asalto < 0.98 or huye) else 0.0
            accion = "cae" if (huye and i % 7 == 3 and retirada > 0.5) else ("pelea" if not huye and asalto > 0.6 else None)
            gente.append((x0 + y, x0, y, tipo, (0.2, 1.0) if huye else (-0.2, -1.0), vel, accion, i))
        for _, x, y, tipo, dr, vel, accion, i in sorted(gente):
            G.persona(lz, iso, x, y, t, tipo=tipo, dir=dr, vel=vel, seed=700 + i, h=40, accion=accion)
        # caballería: dos jinetes, uno de ellos Alvarado
        for j, (x, ya, yc) in enumerate(((-210, 470, 260), (150, 480, 270))):
            u = e_inout(asalto) * (1 - e_in(retirada) * 1.15)
            G.caballo(lz, iso, x, ya + (yc - ya) * u, t=t, dir=-1 if retirada < 0.05 else 1, seed=j, color=((120, 80, 56), (226, 220, 210))[j], vel=1.0 if (asalto < 0.98 or retirada > 0.05) else 0.0,
                      jinete="capitan_esp", s=1.15)

    def lluvia_piedras(self, lz, iso, t, piedras, seed=3):
        """Piedras que caen de la cumbre al llano en parábola, con polvo al tocar el suelo."""
        if piedras <= 0.01:
            return
        n = int(26 * piedras)
        for i in range(n):
            per = 1.3 + 0.5 * h01(seed, i)
            u = ((t + h01(seed, i, 2) * per) % per) / per
            x0, y0 = -120 + 200 * h01(seed, i, 3), 74
            x1, y1 = x0 + 30 * (h01(seed, i, 4) - 0.5), 190 + 140 * h01(seed, i, 5)
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            z = ZT * (1 - u * u) + 30 * math.sin(math.pi * u)
            sx, sy = iso.P(x, y, z)
            r = 4.0 * iso.z * (0.8 + 0.5 * h01(seed, i, 6))
            if u < 0.93:
                lz.relleno(circulo(sx, sy, r, 8), (120, 100, 110), capa=2)
                lz.relleno(circulo(sx - r * 0.3, sy - r * 0.3, r * 0.5, 6), (170, 150, 150), capa=2)
            else:
                gx, gy = iso.P(x1, y1, 0)
                a = (u - 0.93) / 0.07
                lz.relleno(circulo(gx, gy, r * (2 + 4 * a), 12), (236, 222, 200), alfa=0.6 * (1 - a), capa=2)

    def flechas(self, lz, iso, t, k, seed=5):
        """Flechas que caen en arco desde la cumbre (trazos cortos)."""
        if k <= 0.01:
            return
        for i in range(int(18 * k)):
            per = 1.0 + 0.4 * h01(seed, i)
            u = ((t + h01(seed, i, 2) * per) % per) / per
            x0, x1 = -120 + 200 * h01(seed, i, 3), -160 + 260 * h01(seed, i, 4)
            y0, y1 = 70, 220 + 160 * h01(seed, i, 5)
            p = [(x0 + (x1 - x0) * v, y0 + (y1 - y0) * v, ZT * (1 - v) + 120 * math.sin(math.pi * v)) for v in (u, min(1.0, u + 0.05))]
            a, b = iso.P(*p[0]), iso.P(*p[1])
            lz.trazo(np.array([a, b]), (60, 40, 50), 2.6, afinar=False, temblor=0.0, capa=2)


# ------------------------------------------------------------------------------------------------ Templo Mayor (2D, para el «hombre de la matanza»)
def templo_mayor(lz, x, y, s, alfa=1.0, capa=1):
    """Basamento doble con los dos adoratorios (Tláloc azul y Huitzilopochtli rojo). Origen = centro de la base."""
    base, sombra, luz = (214, 196, 170), (170, 146, 132), (236, 222, 200)
    for i in range(5):
        w, h = (5.0 - 0.75 * i) * s, 0.7 * s
        yb = y - i * h
        lz.relleno(np.array([(x - w, yb), (x + w, yb), (x + w - 0.3 * s, yb - h), (x - w + 0.3 * s, yb - h)]), base, alfa=alfa, capa=capa)
        lz.relleno(np.array([(x + w * 0.45, yb), (x + w, yb), (x + w - 0.3 * s, yb - h), (x + w * 0.45, yb - h)]), sombra, alfa=alfa * 0.8, capa=capa)
        lz.relleno(rect_red(x - w + 0.3 * s, yb - h, 2 * w - 0.6 * s, 0.1 * s, 0), luz, alfa=alfa, capa=capa)
    for sd in (-1, 1):                                                   # escalinatas gemelas
        lz.relleno(np.array([(x + sd * 1.9 * s - 0.55 * s, y), (x + sd * 1.9 * s + 0.55 * s, y), (x + sd * 1.3 * s + 0.4 * s, y - 3.5 * s), (x + sd * 1.3 * s - 0.4 * s, y - 3.5 * s)]),
                   luz, alfa=alfa, capa=capa)
    top = y - 3.5 * s
    for sd, col in ((-1, (70, 130, 210)), (1, (214, 60, 60))):
        cx = x + sd * 1.25 * s
        lz.relleno(rect_red(cx - 0.8 * s, top - 1.3 * s, 1.6 * s, 1.3 * s, 0.05 * s), (236, 226, 210), alfa=alfa, capa=capa)
        lz.relleno(rect_red(cx - 0.3 * s, top - 0.8 * s, 0.6 * s, 0.8 * s, 0.1 * s), (60, 40, 50), alfa=alfa, capa=capa)
        lz.relleno(np.array([(cx - 0.95 * s, top - 1.3 * s), (cx + 0.95 * s, top - 1.3 * s), (cx + 0.7 * s, top - 2.2 * s), (cx - 0.7 * s, top - 2.2 * s)]), col, alfa=alfa, capa=capa)
        for k in range(4):
            lz.relleno(rect_red(cx - 0.6 * s + 0.35 * s * k, top - 2.0 * s, 0.18 * s, 0.6 * s, 0), P.aclarar(col, 0.3), alfa=alfa, capa=capa)


# ------------------------------------------------------------------------------------------------ caballo 2D de perfil (con jinete) — galope y caída
CAB = (120, 76, 52)


def caballo2d(lz, x, y, s, t, ph=None, galope=1.0, color=CAB, mirar=1, jinete=None, jinete_seed=0, crin=(50, 30, 30), alfa=1.0, capa=1, patas_caida=0.0):
    """Caballo de perfil (x, y = suelo bajo el centro del cuerpo; s = px por unidad, ~1 u = 1/10 del largo del cuerpo).
    galope 0..1 mezcla el ciclo de galope con la postura quieta. jinete = spec de K2 (sentado sobre la silla). patas_caida 0..1 = patas al aire."""
    ph = t * 11.0 if ph is None else ph
    sh = P.oscurecer(color, 0.25)
    lu = P.aclarar(color, 0.15)
    rebote = -0.35 * s * abs(math.sin(ph)) * galope
    with lz.grupo(x, y + rebote, 1.0, 0.0):
        f = mirar

        def pt(px_, py_):
            return (px_ * s * f, py_ * s)

        def pata(cx, cy, fase, delante, lejos):
            a = (0.55 * math.sin(ph + fase) * galope) + (1.2 if delante else -1.0) * patas_caida
            kn = 0.6 * max(0.0, math.sin(ph + fase + 1.2)) * galope + 0.6 * patas_caida
            col = sh if lejos else color
            p0 = np.array(pt(cx, cy))
            p1 = p0 + np.array([math.sin(a) * 2.4 * s * f, math.cos(a) * 2.4 * s])
            a2 = a + (kn if delante else -kn)
            p2 = p1 + np.array([math.sin(a2) * 2.2 * s * f, math.cos(a2) * 2.2 * s])
            for q0, q1, r0, r1 in ((p0, p1, 0.55, 0.38), (p1, p2, 0.36, 0.28)):
                d = q1 - q0
                n = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-6)
                lz.relleno(np.array([q0 + n * r0 * s, q1 + n * r1 * s, q1 - n * r1 * s, q0 - n * r0 * s]), col, alfa=alfa, capa=capa)
            lz.relleno(elipse(p2[0], p2[1], 0.42 * s, 0.26 * s, 0, 10), (40, 30, 30), alfa=alfa, capa=capa)

        # patas lejanas
        pata(3.0, -4.6, 0.0, True, True)
        pata(-3.0, -4.6, 2.6, False, True)
        # cola
        cola = [pt(-4.6, -6.6), pt(-6.6 - 0.6 * math.sin(ph * 0.5), -5.4 + 0.6 * math.sin(ph)), pt(-6.2, -3.4), pt(-5.0, -5.6)]
        lz.relleno(np.array(catmull(np.array(cola, float), 6, True)), crin, alfa=alfa, capa=capa)
        # cuerpo
        cuerpo = [pt(-4.8, -6.6), pt(-2.0, -7.3), pt(2.6, -7.2), pt(4.6, -6.6), pt(4.9, -5.0), pt(3.2, -4.1), pt(-2.8, -4.0), pt(-4.9, -4.9)]
        c = np.array(catmull(np.array(cuerpo, float), 8, True))
        lz.relleno(c, color, alfa=alfa, capa=capa)
        with lz.recorte(c):
            lz.relleno(c + np.array([0, 0.9 * s]), sh, alfa=alfa * 0.8, capa=capa)
            lz.relleno(elipse(pt(-1.0, -6.6)[0], pt(-1.0, -6.6)[1], 2.6 * s, 0.6 * s, 0, 16), lu, alfa=alfa * 0.6, capa=capa)
        # cuello y cabeza
        cab_bob = 0.25 * math.sin(ph + 0.8) * galope
        cuello = [pt(3.2, -7.0), pt(4.6, -9.6 + cab_bob), pt(5.8, -10.2 + cab_bob), pt(6.2, -9.4 + cab_bob), pt(5.4, -6.0)]
        lz.relleno(np.array(catmull(np.array(cuello, float), 6, True)), color, alfa=alfa, capa=capa)
        cabeza = [pt(5.2, -10.4 + cab_bob), pt(6.4, -10.6 + cab_bob), pt(8.6, -8.6 + cab_bob), pt(8.4, -7.9 + cab_bob), pt(7.4, -8.0 + cab_bob), pt(5.6, -8.9 + cab_bob)]
        lz.relleno(np.array(catmull(np.array(cabeza, float), 6, True)), color, alfa=alfa, capa=capa)
        lz.relleno(np.array([pt(5.4, -10.3 + cab_bob), pt(5.8, -11.4 + cab_bob), pt(6.1, -10.4 + cab_bob)]), sh, alfa=alfa, capa=capa)        # oreja
        ox, oy = pt(6.6, -9.6 + cab_bob)
        lz.relleno(circulo(ox, oy, 0.28 * s, 10), (30, 20, 24), alfa=alfa, capa=capa)
        lz.relleno(circulo(ox + 0.08 * s * f, oy - 0.08 * s, 0.09 * s, 6), (255, 255, 255), alfa=alfa, capa=capa)
        crines = [pt(3.0, -7.4), pt(4.4, -10.0 + cab_bob), pt(5.4, -10.8 + cab_bob), pt(4.8, -9.4 + cab_bob), pt(3.6, -7.0)]
        lz.relleno(np.array(catmull(np.array(crines, float), 6, True)), crin, alfa=alfa, capa=capa)
        # silla y manta
        lz.relleno(np.array([pt(-1.6, -7.4), pt(1.6, -7.4), pt(1.4, -5.6), pt(-1.4, -5.6)]), (170, 40, 50), alfa=alfa, capa=capa)
        lz.relleno(elipse(0, pt(0, -7.6)[1], 1.6 * s, 0.4 * s, 0, 14), (90, 50, 36), alfa=alfa, capa=capa)
        # patas cercanas
        pata(3.0, -4.6, 3.6, True, False)
        pata(-3.0, -4.6, 1.0, False, False)
        if jinete is not None:
            K2.cuerpo(lz, -0.3 * s * f, -6.9 * s, 1.2 * s, jinete, t, piernas="sentado", brazos="idle", mirar=f, vista="perfil", seed=jinete_seed, sombra=False, alfa=alfa,
                      cara="minima" if 2.4 * 1.2 * s >= 30 else "auto")


def polvo2d(lz, x, y, t, t0, dur=1.4, n=14, s=1.0, color=(236, 220, 200), seed=0, capa=2):
    """Nube de polvo que se expande desde (x, y) a partir de t0."""
    u = prog(t, t0, t0 + dur)
    if u <= 0 or u >= 1:
        return
    for k in range(n):
        a = math.pi * (0.05 + 0.9 * h01(seed, k))
        d = (60 + 160 * h01(seed, k, 2)) * s * e_out(u)
        r = (24 + 40 * h01(seed, k, 3)) * s * (0.5 + u)
        lz.relleno(circulo(x - math.cos(a) * d, y - math.sin(a) * d * 0.5, r, 18), color, alfa=0.7 * (1 - u), capa=capa)


def sobre(lz, x, y, s, rot=0.0, alfa=1.0, capa=2, sello=(200, 50, 60)):
    """Sobre de carta con sello de lacre (mensaje)."""
    with lz.grupo(x, y, 1.0, rot):
        lz.relleno(rect_red(-1.6 * s, -1.0 * s, 3.2 * s, 2.0 * s, 0.12 * s), (250, 240, 214), alfa=alfa, capa=capa)
        lz.relleno(np.array([(-1.6 * s, -1.0 * s), (0, 0.25 * s), (1.6 * s, -1.0 * s)]), (226, 212, 180), alfa=alfa, capa=capa)
        lz.relleno(circulo(0, 0.2 * s, 0.35 * s, 14), sello, alfa=alfa, capa=capa)
