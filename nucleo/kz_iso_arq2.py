# -*- coding: utf-8 -*-
"""Más arquitectura y utilería isométrica para historia de México (estilo Kurzgesagt): alhóndiga, palacio, catedral, fuerte con baluartes, mina y malacate,
puente de piedra, acueducto, chozas, tiendas de campaña, cañones, barcos y muelle, mobiliario de habitación en corte. Todas registran sus partes en un `Mundo`."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint, caja, cara_rect, cara_arco, hilera_ventanas, techo_dos_aguas, techo_plano, techo_piramide, cilindro, cupula, cruz, sombra_suelo, Caja, suelo_rect, suelo
import kz_iso_obj as O
import kz_iso_arq as A
from motor import circulo, elipse, rect_red, h01
import plano as P

PIEDRA = (214, 196, 178)
TEZONTLE = (190, 92, 82)
SOMBRA = -1e5


def _reg(mundo, x, y, w, d, h, fn, clave=None):
    mundo.add(x, y, x + w, y + d, h, fn, clave=clave)


def alhondiga(mundo, x, y, w=150, d=120, h=84, muro=(226, 196, 176), t_fn=None, puerta_fuego=0.0, bandera_luto=False):
    """Alhóndiga de Granaditas (Guanajuato): bloque macizo de piedra rosada de dos niveles con patio, ventanas altas y estrechas, portón de madera y pretil almenado."""
    mundo.add(x - 4, y - 4, x + w + 4, y + d + 4, h, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, d, h, k=0.5), clave=SOMBRA)

    def atras(lz, iso):          # alas del fondo y de la derecha
        for (ax, ay, aw, ad) in ((x, y, w, 24), (x + w - 24, y, 24, d)):
            c = caja(lz, iso, ax, ay, aw, ad, h, muro)
            caja(lz, iso, ax - 1.5, ay - 1.5, aw + 3, ad + 3, 5, P.aclarar(muro, 0.12), z0=h)
    _reg(mundo, x, y, w, d, h + 20, atras, clave=(x + w / 2) + (y + d / 2) - 90)

    def patio(lz, iso):
        suelo_rect(lz, iso, x + 24, y + 24, w - 48, d - 24, (214, 198, 164))

    mundo.add(x + 24, y + 24, x + w - 24, y + d, 0, patio, clave=SOMBRA + 1)

    def frente(lz, iso):         # ala frontal con portón y ventanas
        c = caja(lz, iso, x, y + d - 24, w, 24, h, muro)
        cara_rect(lz, iso, c, "y", 0, w, 0, 8, P.oscurecer(muro, 0.14))
        cara_rect(lz, iso, c, "y", 0, w, h * 0.5, h * 0.5 + 3, P.aclarar(muro, 0.2))
        n = 9
        for i in range(n):
            a = w * (0.05 + 0.9 * (i + 0.5) / n) - 3
            if abs(a + 3 - w / 2) < 18:
                continue
            cara_arco(lz, iso, c, "y", a, a + 7, h * 0.58, h * 0.58 + 26, (86, 62, 84))
            cara_rect(lz, iso, c, "y", a - 1, a + 8, h * 0.58 - 2, h * 0.58, P.aclarar(muro, 0.25))
        pa = w / 2 - 15
        cara_rect(lz, iso, c, "y", pa - 6, pa + 36, 0, 60, P.aclarar(muro, 0.22))
        cara_arco(lz, iso, c, "y", pa, pa + 30, 0, 50, (120, 76, 60))
        cara_rect(lz, iso, c, "y", pa + 14.5, pa + 15.5, 0, 38, (70, 48, 44))
        if puerta_fuego > 0.02:
            for j in range(4):
                O.fuego(lz, iso, x + pa + 4 + j * 7, y + d, 0.9, (t_fn() if t_fn else 0.0), seed=j, halo=(j == 0))
        # almenas
        for i in range(int(w / 10)):
            caja(lz, iso, x + 2 + i * 10, y + d - 24 + 2, 6, 3, 5, P.aclarar(muro, 0.1), z0=h)
        caja(lz, iso, x - 1.5, y + d - 24 - 1.5, w + 3, 3, 5, P.aclarar(muro, 0.12), z0=h) if False else None
        if bandera_luto:
            for bx in (x + 6, x + w - 8):
                O.bandera(lz, iso, bx, y + d - 12, h=h + 44, w=22, alto=16, color=(36, 32, 44), t=(t_fn() if t_fn else 0.0))
    _reg(mundo, x, y + d - 24, w, 24, h + 20, frente, clave=(x + w / 2) + (y + d - 12))


def palacio(mundo, x, y, w=240, d=60, h=72, muro=TEZONTLE, t_fn=None, campana=True):
    """Palacio Nacional / Virreinal: edificio largo y bajo de piedra rojiza (tezontle) con marcos blancos, tres portones, balcón central y torre-campanario."""
    mundo.add(x - 4, y - 4, x + w + 4, y + d + 4, h, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, d, h, k=0.5), clave=SOMBRA)

    def dib(lz, iso):
        c = caja(lz, iso, x, y, w, d, h, muro)
        cara_rect(lz, iso, c, "y", 0, w, 0, 8, P.oscurecer(muro, 0.2))
        cara_rect(lz, iso, c, "y", 0, w, h * 0.5 - 2, h * 0.5 + 1, (250, 240, 226))
        cara_rect(lz, iso, c, "y", 0, w, h - 5, h, (250, 240, 226))
        n = int(w / 18)
        for i in range(n):
            a = 4 + i * (w - 8) / n + 2
            for piso, b0 in ((0, 14), (1, h * 0.5 + 8)):
                if piso == 0 and (i % 4 == 1 or abs(a + 6 - w / 2) < 40) and i in (n // 4, n // 2, (3 * n) // 4 - 1):
                    continue
                cara_rect(lz, iso, c, "y", a - 1.5, a + 9.5, b0 - 1.5, b0 + 20.5, (250, 240, 226))
                cara_rect(lz, iso, c, "y", a, a + 8, b0, b0 + 19, (86, 58, 84))
        for fr in (0.25, 0.5, 0.75):
            pa = w * fr - 9
            cara_rect(lz, iso, c, "y", pa - 3, pa + 21, 0, 38, (250, 240, 226))
            cara_arco(lz, iso, c, "y", pa, pa + 18, 0, 34, (92, 62, 54))
        lz.relleno(iso.pts([(x + w / 2 - 14, y + d, h * 0.5 + 2), (x + w / 2 + 14, y + d, h * 0.5 + 2), (x + w / 2 + 14, y + d + 6, h * 0.5 + 2), (x + w / 2 - 14, y + d + 6, h * 0.5 + 2)]), tint((250, 240, 226)))
        for i in range(8):
            lz.relleno(iso.pts([(x + w / 2 - 14 + i * 4, y + d + 6, h * 0.5 + 2), (x + w / 2 - 13 + i * 4, y + d + 6, h * 0.5 + 2), (x + w / 2 - 13 + i * 4, y + d + 6, h * 0.5 + 9), (x + w / 2 - 14 + i * 4, y + d + 6, h * 0.5 + 9)]), tint((250, 240, 226)))
        if campana:
            cx = x + w / 2
            cb = caja(lz, iso, cx - 12, y + d / 2 - 12, 24, 24, 22, (250, 240, 226), z0=h)
            cara_arco(lz, iso, cb, "y", 5, 19, 3, 18, (70, 52, 90))
            techo_piramide(lz, iso, Caja(cx - 12, y + d / 2 - 12, 24, 24, 22, h), 14, (230, 190, 120), vuelo=2)
            sx, sy = iso.P(cx, y + d / 2, h + 14)
            lz.relleno(circulo(sx, sy, 3.6 * iso.z, 8), tint((250, 206, 90)))

    _reg(mundo, x, y, w, d, h + 40, dib, clave=(x + w / 2) + (y + d / 2))


def catedral(mundo, x, y, w=120, largo=150, h=80):
    """Catedral Metropolitana (esquema): nave larga, fachada con tres portadas, dos torres altas con campanario y cúpula central."""
    A.iglesia(mundo, x, y, w=w, largo=largo, h_nave=h, muro=(228, 214, 196), techo=(150, 150, 170), torres=2, cupula_c=True)


def casa_alta(mundo, x, y, w, d, h, muro=A.CAL, acento=A.AZUL, techo=A.TEJA, seed=0):
    A.casa_colonial(mundo, x, y, w, d, h, muro=muro, techo=techo, eje="x", ventanas=3, balcon=True, seed=seed)


def choza(mundo, x, y, r=11, h=14, seed=0, techo=(226, 190, 100)):
    """Choza de adobe con techo cónico de palma (pueblos y rancherías)."""
    def dib(lz, iso):
        cilindro(lz, iso, x, y, r, h, (214, 176, 140))
        sx, sy = iso.P(x, y, h)
        k = iso.z
        ax = (r + 4) * I.C30 * math.sqrt(2) * k
        ay = iso.P(x, y, h + r * 1.3)[1]
        lz.relleno(np.array([[sx - ax, sy], [sx + ax, sy], [sx, ay]]), tint(P.oscurecer(techo, 0.3)))
        lz.relleno(np.array([[sx - ax, sy], [sx + ax * 0.1, sy], [sx, ay]]), tint(techo))
        for i in range(1, 4):
            f = i / 4
            lz.relleno(np.array([[sx - ax * (1 - f), sy - (sy - ay) * f], [sx + ax * (1 - f) * 0.1, sy - (sy - ay) * f], [sx + ax * (1 - f) * 0.1, sy - (sy - ay) * f + 1.2 * k], [sx - ax * (1 - f), sy - (sy - ay) * f + 1.2 * k]]), tint(P.oscurecer(techo, 0.18)), alfa=0.7)
        lz.relleno(rect_red(sx - 3 * k - r * 0.2 * k, sy + 4 * k, 6 * k, 9 * k, 2.4 * k), tint((120, 78, 60)))
    mundo.add(x - r, y - r, x + r, y + r, h + r, lambda lz, iso: I.sombra_elipse(lz, iso, x + 3, y + 1, r * 1.3, r * 0.8, 0.2), clave=SOMBRA)
    _reg(mundo, x - r, y - r, 2 * r, 2 * r, h + r * 1.3, dib)


def tienda_campana(mundo, x, y, w=30, d=22, color=(246, 240, 226), franja=(206, 70, 70), bandera=None, t_fn=None):
    """Tienda de campaña militar (prisma triangular con bandera)."""
    def dib(lz, iso):
        c = caja(lz, iso, x, y, w, d, 8, color)
        techo_dos_aguas(lz, iso, Caja(x, y, w, d, 8, 0), "x", 14, color, vuelo=1.5, gablete=P.oscurecer(color, 0.14), tejas=False, grosor=1.0)
        cara_rect(lz, iso, c, "y", 0, w, 0, 3, franja)
        cara_arco(lz, iso, c, "y", w * 0.4, w * 0.6, 0, 11, (60, 44, 60))
        if bandera:
            O.bandera(lz, iso, x + w / 2, y + d / 2, h=36, w=18, alto=11, color=bandera, t=(t_fn() if t_fn else 0.0))
    mundo.add(x - 2, y - 2, x + w + 2, y + d + 2, 12, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, d, 10, k=0.7), clave=SOMBRA)
    _reg(mundo, x, y, w, d, 30, dib)


def canon(mundo, x, y, dir=1, t_fn=None, disparo=-1.0, escala=1.0):
    """Cañón sobre cureña con ruedas (apunta hacia ±x en pantalla). disparo = tiempo desde el disparo (para humo y retroceso)."""
    def dib(lz, iso):
        sx, sy = iso.P(x, y, 0)
        k = iso.z * escala
        u = max(0.0, disparo)
        rec = -3.0 * math.exp(-u * 7) * dir if disparo >= 0 else 0.0
        lz.relleno(elipse(sx, sy, 15 * k, 5 * k, 0, 14), (30, 24, 70), alfa=0.2)
        for dx in (-7, 7):
            lz.relleno(circulo(sx + dx * k, sy - 8 * k, 8.4 * k, 14), tint((110, 76, 56)))
            lz.relleno(circulo(sx + dx * k, sy - 8 * k, 5.4 * k, 12), tint((166, 120, 84)))
        lz.relleno(rect_red(sx - 12 * k + rec * k, sy - 15 * k, 24 * k, 8 * k, 1.4 * k), tint((130, 96, 70)))
        bx = sx + rec * k
        lz.relleno(np.array([[bx - 12 * k * dir, sy - 14.4 * k], [bx + 16 * k * dir, sy - 17 * k], [bx + 16 * k * dir, sy - 10.6 * k], [bx - 12 * k * dir, sy - 8.4 * k]]), tint((62, 66, 86)))
        lz.relleno(np.array([[bx - 12 * k * dir, sy - 14.4 * k], [bx + 16 * k * dir, sy - 17 * k], [bx + 16 * k * dir, sy - 15 * k], [bx - 12 * k * dir, sy - 12.4 * k]]), tint((112, 118, 144)))
        if 0.0 <= disparo < 1.6:
            fl = max(0.0, 1 - disparo * 6)
            if fl > 0:
                lz.halo(bx + 18 * k * dir, sy - 14 * k, 30 * k, (255, 214, 120), alfa=0.8 * fl, capa=2)
                lz.relleno(circulo(bx + 18 * k * dir, sy - 14 * k, 6 * k * fl + 2 * k, 10), tint((255, 236, 160)), capa=2)
            for i in range(6):
                uu = min(1.0, disparo * 0.7 + i * 0.07)
                lz.relleno(circulo(bx + (18 + 18 * uu * (i + 1) * 0.5) * k * dir, sy - (14 + 8 * uu * (i % 3)) * k, (3 + 9 * uu) * k, 10), tint((240, 238, 244)), alfa=0.7 * (1 - disparo / 1.6), capa=2)
    _reg(mundo, x - 12, y - 6, 24, 12, 24, dib)


def barco(mundo, x, y, t_fn=None, s=1.0, vela=(250, 244, 230), casco=(120, 80, 60), banderas=(206, 66, 66), dir=1):
    """Galeón de vela (3/4): casco con castillo de popa, dos mástiles y velas hinchadas, cabeceo suave sobre el agua."""
    def dib(lz, iso):
        t = t_fn() if t_fn else 0.0
        sx, sy = iso.P(x, y, 0)
        k = iso.z * s
        bob = 2.5 * math.sin(t * 1.3 + x * 0.01) * k
        sy += bob
        lz.relleno(elipse(sx, sy + 2 * k, 34 * k, 8 * k, 0, 18), (10, 30, 90), alfa=0.28)
        pts = np.array([(-30, -12), (30, -12), (26, 0), (-22, 2), (-34, -4)], float) * [dir, 1] * k + [sx, sy]
        lz.relleno(pts, tint(P.oscurecer(casco, 0.25)))
        lz.relleno(np.array([(-30, -12), (30, -12), (28, -7), (-30, -7)], float) * [dir, 1] * k + [sx, sy], tint(casco))
        lz.relleno(np.array([(-30, -12), (-18, -12), (-18, -24), (-32, -22)], float) * [dir, 1] * k + [sx, sy], tint(P.aclarar(casco, 0.1)))
        for i in range(4):
            lz.relleno(circulo(sx + (-20 + i * 14) * dir * k, sy - 3.5 * k, 1.4 * k, 6), tint((40, 30, 40)))
        for mx, hh in ((-8, 52), (14, 44)):
            lz.relleno(rect_red(sx + (mx - 1) * dir * k, sy - (12 + hh) * k, 2.0 * k, hh * k, 0.6 * k), tint((100, 70, 56)))
            vw = 16 * (0.9 + 0.12 * math.sin(t * 1.7 + mx))
            lz.relleno(np.array([(mx - vw * 0.5, -(12 + hh) + 4), (mx + vw * 0.7, -(12 + hh) + 4), (mx + vw * 0.45, -(12 + hh * 0.35)), (mx - vw * 0.4, -(12 + hh * 0.35))], float) * [dir, 1] * k + [sx, sy], tint(vela))
            lz.relleno(np.array([(mx - vw * 0.5, -(12 + hh) + 4), (mx + vw * 0.2, -(12 + hh) + 4), (mx + vw * 0.1, -(12 + hh * 0.35)), (mx - vw * 0.4, -(12 + hh * 0.35))], float) * [dir, 1] * k + [sx, sy], tint(P.oscurecer(vela, 0.16)))
        O.bandera(lz, iso, x + 14 * dir, y, h=0, w=0, alto=0) if False else None
        lz.relleno(np.array([(14, -56), (24, -54), (14, -50)], float) * [dir, 1] * k + [sx, sy], tint(banderas))
    _reg(mundo, x - 36, y - 12, 72, 24, 70, dib)


def muelle(mundo, x, y, largo=90, ancho=16, h=6, eje="x"):
    """Muelle de madera sobre pilotes. eje='x' (largo a lo largo de x) o 'y' (hacia el agua en y)."""
    def dib(lz, iso):
        w, d = (largo, ancho) if eje == "x" else (ancho, largo)
        caja(lz, iso, x, y, w, d, 4, (150, 108, 76), z0=h - 4)
        for i in range(int(largo / 12) + 1):
            if eje == "x":
                caja(lz, iso, x + i * 12 - 1.4, y - 1, 3, 3, h + 3, (110, 76, 56), z0=-6)
                caja(lz, iso, x + i * 12 - 1.4, y + ancho - 2, 3, 3, h + 3, (110, 76, 56), z0=-6)
            else:
                caja(lz, iso, x - 1, y + i * 12 - 1.4, 3, 3, h + 3, (110, 76, 56), z0=-6)
                caja(lz, iso, x + ancho - 2, y + i * 12 - 1.4, 3, 3, h + 3, (110, 76, 56), z0=-6)
        for i in range(int(largo / 9)):
            if eje == "x":
                lz.relleno(iso.pts([(x + i * 9, y, h), (x + i * 9 + 0.8, y, h), (x + i * 9 + 0.8, y + ancho, h), (x + i * 9, y + ancho, h)]), tint((120, 82, 60)), alfa=0.6)
            else:
                lz.relleno(iso.pts([(x, y + i * 9, h), (x + ancho, y + i * 9, h), (x + ancho, y + i * 9 + 0.8, h), (x, y + i * 9 + 0.8, h)]), tint((120, 82, 60)), alfa=0.6)
    w, d = (largo, ancho) if eje == "x" else (ancho, largo)
    _reg(mundo, x, y, w, d, h + 6, dib)


def puente_piedra(mundo, x, y, largo=120, ancho=30, h=26, arcos=4, muro=(214, 196, 178)):
    """Puente de piedra con arcos a lo largo de x (por ejemplo, el Puente de Calderón); el río pasa por debajo (dibujarlo aparte)."""
    def dib(lz, iso):
        c = caja(lz, iso, x, y, largo, ancho, h, muro)
        pa = largo / arcos
        for i in range(arcos):
            cara_arco(lz, iso, c, "y", i * pa + 5, (i + 1) * pa - 5, 0, h * 0.8, (110, 130, 170))
        for dy in (0, ancho - 4):
            caja(lz, iso, x, y + dy, largo, 4, 6, P.aclarar(muro, 0.1), z0=h)
        lz.relleno(iso.pts([(x + 2, y + 5, h), (x + largo - 2, y + 5, h), (x + largo - 2, y + ancho - 5, h), (x + 2, y + ancho - 5, h)]), tint((196, 176, 140)))
    mundo.add(x - 2, y - 2, x + largo + 8, y + ancho + 8, h + 8, lambda lz, iso: sombra_suelo(lz, iso, x, y, largo, ancho, h, k=0.4), clave=SOMBRA)
    _reg(mundo, x, y, largo, ancho, h + 8, dib)


def acueducto(mundo, x, y, n=8, paso=26, h=60, muro=(228, 206, 186)):
    """Acueducto de arcos (como el de Querétaro) a lo largo de x."""
    def dib(lz, iso):
        c = caja(lz, iso, x, y, n * paso, 8, h, muro)
        for i in range(n):
            cara_arco(lz, iso, c, "y", i * paso + 4, (i + 1) * paso - 4, 0, h * 0.82, (120, 150, 190))
        caja(lz, iso, x - 1, y - 1, n * paso + 2, 10, 5, P.aclarar(muro, 0.1), z0=h)
    mundo.add(x, y, x + n * paso, y + 8, h, lambda lz, iso: sombra_suelo(lz, iso, x, y, n * paso, 8, h, k=0.5), clave=SOMBRA)
    _reg(mundo, x, y, n * paso, 8, h + 6, dib)


def mina(mundo, x, y, t_fn=None, s=1.0):
    """Bocamina en una colina de roca con marco de madera, vía con vagoneta y malacate (cabrestante)."""
    def dib(lz, iso):
        t = t_fn() if t_fn else 0.0
        sx, sy = iso.P(x, y, 0)
        k = iso.z * s
        lz.relleno(np.array([(-70, 0), (-52, -44), (-20, -66), (20, -64), (52, -42), (74, 0)], float) * k + [sx, sy], tint((150, 124, 120)))
        lz.relleno(np.array([(-70, 0), (-52, -44), (-20, -66), (-4, -34), (-8, 0)], float) * k + [sx, sy], tint((184, 156, 148)))
        lz.relleno(np.array([(-52, -44), (-20, -66), (-8, -58), (-36, -38)], float) * k + [sx, sy], tint((214, 190, 180)))
        lz.relleno(rect_red(sx - 20 * k, sy - 34 * k, 40 * k, 34 * k, 18 * k), tint((52, 38, 60)))
        for dx in (-22, 22):
            lz.relleno(rect_red(sx + (dx - 3) * k, sy - 38 * k, 6 * k, 38 * k, 1.0 * k), tint((130, 90, 66)))
        lz.relleno(rect_red(sx - 28 * k, sy - 42 * k, 56 * k, 6 * k, 1.4 * k), tint((150, 106, 76)))
        for i in range(4):
            lz.relleno(rect_red(sx - 14 * k + i * 9 * k, sy - 2 * k + i * 4 * k, 12 * k, 2 * k, 0.6 * k), tint((120, 100, 100)))
    mundo.add(x - 70, y - 6, x + 70, y + 6, 70, dib)


def malacate(mundo, x, y, t_fn=None, mula=True, s=1.0):
    """Malacate: tambor de madera con aspas que gira movido por una mula en círculo."""
    def dib(lz, iso):
        t = t_fn() if t_fn else 0.0
        sx, sy = iso.P(x, y, 0)
        k = iso.z * s
        lz.relleno(elipse(sx, sy, 26 * k, 11 * k, 0, 20), (30, 24, 70), alfa=0.12)
        lz.relleno(rect_red(sx - 3 * k, sy - 30 * k, 6 * k, 30 * k, 1), tint((130, 90, 66)))
        a = t * 1.1
        for j in range(2):
            ang = a + j * math.pi
            ex, ey = sx + math.cos(ang) * 24 * k, sy - 14 * k + math.sin(ang) * 11 * k
            lz.relleno(np.array([[sx - 1.2 * k, sy - 14 * k], [sx + 1.2 * k, sy - 14 * k], [ex, ey + 1.2 * k], [ex, ey - 1.2 * k]]), tint((150, 106, 76)))
        lz.relleno(circulo(sx, sy - 30 * k, 4 * k, 8), tint((170, 130, 96)))
    mundo.add(x - 26, y - 14, x + 26, y + 14, 40, dib)
    if mula:
        def m_(lz, iso):
            t = t_fn() if t_fn else 0.0
            a = t * 1.1 + 0.4
            import kz_gente_iso as G
            G.burro(lz, iso, x + math.cos(a) * 21 * 0.9, y + math.sin(a) * 21 * 0.9 * 0.9, t, dir=(1 if math.sin(a) < 0 else -1), carga=False, s=0.9)
        a0 = 0
        mundo.add(x - 26, y - 26, x + 26, y + 26, 20, m_, fijo=False, clave=x + y + 14)


# ------------------------------------------------------------------------------------------------ mobiliario (habitación en corte)
def mesa(lz, iso, x, y, w=60, d=30, h=17, color=(150, 100, 70), mantel=None):
    I.sombra_suelo(lz, iso, x, y, w, d, h, k=0.5)
    c = caja(lz, iso, x, y, w, d, 3, color, z0=h - 3)
    for (px, py) in ((x + 2, y + 2), (x + w - 5, y + 2), (x + 2, y + d - 5), (x + w - 5, y + d - 5)):
        caja(lz, iso, px, py, 3, 3, h - 3, P.oscurecer(color, 0.2))
    if mantel:
        caja(lz, iso, x - 1, y - 1, w + 2, d + 2, 1.5, mantel, z0=h - 0.5)
    return c


def silla(lz, iso, x, y, h=11, color=(130, 86, 64), dir="y"):
    for (px, py) in ((x, y), (x + 8, y), (x, y + 8), (x + 8, y + 8)):
        caja(lz, iso, px, py, 2, 2, h * 0.5, P.oscurecer(color, 0.2))
    caja(lz, iso, x, y, 10, 10, 2, color, z0=h * 0.5)
    caja(lz, iso, x, y, 10, 2, h * 0.9, color, z0=h * 0.5 + 2)


def estante(lz, iso, x, y, w=50, d=10, h=60, color=(120, 80, 62), libros=True):
    c = caja(lz, iso, x, y, w, d, h, color)
    for i in range(1, 5):
        cara_rect(lz, iso, c, "y", 1, w - 1, i * h / 5 - 1, i * h / 5 + 1, P.aclarar(color, 0.2))
        if libros:
            a = 3
            for j in range(10):
                bw = 3 + 2.6 * h01(i, j)
                if a + bw > w - 3:
                    break
                cara_rect(lz, iso, c, "y", a, a + bw, (i - 1) * h / 5 + 2, (i - 1) * h / 5 + 2 + 8 + 5 * h01(j, i), [(200, 70, 70), (70, 120, 170), (90, 160, 100), (230, 190, 80), (140, 90, 160)][(i + j) % 5])
                a += bw + 0.6


def cuadro_pared(lz, iso, c, cara, a, b, w, h, color=(70, 120, 170), marco=(200, 150, 80)):
    cara_rect(lz, iso, c, cara, a - 2, a + w + 2, b - 2, b + h + 2, marco)
    cara_rect(lz, iso, c, cara, a, a + w, b, b + h, color)


def vela(lz, iso, x, y, z, t=0.0, seed=0):
    sx, sy = iso.P(x, y, z)
    k = iso.z
    lz.relleno(rect_red(sx - 1.2 * k, sy - 6 * k, 2.4 * k, 6 * k, 0.5 * k), tint((250, 240, 214)))
    O.fuego(lz, iso, x, y, 0.38, t, seed, z=z + 6, halo=True)


def candelabro(lz, iso, x, y, z, t=0.0, n=3):
    for i in range(n):
        vela(lz, iso, x + (i - (n - 1) / 2) * 5, y, z, t, i)
    sx, sy = iso.P(x, y, z)
    k = iso.z
    lz.relleno(rect_red(sx - n * 2.8 * k, sy - 0.5 * k, n * 5.6 * k, 2 * k, 1 * k), tint((236, 190, 80)))


def alfombra(lz, iso, x, y, w, d, color=(190, 70, 70), borde=(240, 200, 120)):
    suelo_rect(lz, iso, x, y, w, d, borde, z=0.2)
    suelo_rect(lz, iso, x + 3, y + 3, w - 6, d - 6, color, z=0.3)
    suelo_rect(lz, iso, x + 7, y + 7, w - 14, d - 14, P.oscurecer(color, 0.22), z=0.4)
