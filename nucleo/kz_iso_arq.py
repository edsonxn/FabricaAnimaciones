# -*- coding: utf-8 -*-
"""Arquitectura colonial mexicana en isométrico (estilo Kurzgesagt): casas, iglesias de dos torres, portales, haciendas, alhóndiga, fuertes, minas, puentes…
Cada función REGISTRA sus partes en un `Mundo` (cada parte con su profundidad, para que la gente pase por delante o por detrás bien).
Colores por defecto de la paleta de México colonial: cal blanca, ocre, rosa de cantera, azul añil, teja de barro, madera oscura."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint, tonos, caja, cara_rect, cara_arco, hilera_ventanas, techo_dos_aguas, techo_plano, techo_piramide, cilindro, cupula, cruz, sombra_suelo, Caja
import kz_iso_obj as O
from motor import circulo, elipse, rect_red, h01
import plano as P

CAL = (250, 238, 214)
OCRE = (240, 196, 140)
ROSA = (236, 156, 142)
CANTERA = (232, 168, 150)
AZUL = (132, 182, 218)
VERDE_CAL = (170, 214, 170)
TEJA = (206, 96, 78)
TEJA2 = (186, 80, 70)
MADERA = (120, 74, 60)
VENTANA = (96, 60, 92)
PIEDRA = (214, 200, 184)

SOMBRA = -1e5


def _reg(mundo, x, y, w, d, h, fn, clave=None):
    mundo.add(x, y, x + w, y + d, h, fn, clave=clave)


def casa_colonial(mundo, x, y, w, d, h, muro=CAL, techo=TEJA, eje="x", zocalo=None, ventanas=2, puerta=True, balcon=False, chimenea=False, humo_t=None, toldo=None, seed=0, hr=None, t_fn=None):
    """Casa de uno o dos niveles con techo de teja a dos aguas, zócalo de color, ventanas con rejas, puerta con arco y (opcional) balcón y chimenea."""
    zocalo = zocalo or P.oscurecer(muro, 0.16)

    def dib(lz, iso):
        c = caja(lz, iso, x, y, w, d, h, muro)
        cara_rect(lz, iso, c, "y", 0, c.w, 0, 6, zocalo)
        cara_rect(lz, iso, c, "x", 0, c.d, 0, 6, zocalo)
        cara_rect(lz, iso, c, "y", 0, c.w, h - 5, h - 3, P.oscurecer(muro, 0.10))
        nv = 2 if h > 60 else 1
        for piso in range(nv):
            b0 = (h / nv) * piso + (h / nv) * (0.34 if nv == 1 else 0.28)
            alto = (h / nv) * (0.36 if nv == 1 else 0.40)
            if piso == 0 and puerta:
                pass
            hilera_ventanas(lz, iso, c, "y", ventanas, b0 + (4 if (piso == 0 and nv == 1) else 0), alto, w * 0.13, margen_a=0.11, color=VENTANA, marco=P.aclarar(muro, 0.35), rejas=True, postigo=None if seed % 2 else (80, 140, 120))
            hilera_ventanas(lz, iso, c, "x", max(1, ventanas - 1), b0 + (4 if (piso == 0 and nv == 1) else 0), alto, d * 0.15, margen_a=0.22, color=VENTANA, marco=P.aclarar(muro, 0.35), rejas=True)
        if puerta:
            pa = w * 0.5 - 8 if ventanas % 2 == 0 else w * 0.5 - 8
            cara_arco(lz, iso, c, "y", pa, pa + 16, 0, min(h * 0.62, 34), MADERA)
            cara_rect(lz, iso, c, "y", pa - 2, pa, 0, min(h * 0.62, 34) - 8, P.aclarar(muro, 0.3))
            cara_rect(lz, iso, c, "y", pa + 16, pa + 18, 0, min(h * 0.62, 34) - 8, P.aclarar(muro, 0.3))
        if balcon:
            bz = h * 0.5
            lz.relleno(iso.pts([(x - 3, y + d, bz), (x + w + 3, y + d, bz), (x + w + 3, y + d + 9, bz), (x - 3, y + d + 9, bz)]), tint(P.oscurecer(muro, 0.25)))
            for i in range(12):
                a = (w + 6) * i / 11 - 3
                lz.relleno(iso.pts([(x + a, y + d + 9, bz), (x + a + 1.2, y + d + 9, bz), (x + a + 1.2, y + d + 9, bz + 8), (x + a, y + d + 9, bz + 8)]), tint((70, 60, 80)))
        if toldo:
            tz = 24
            lz.relleno(iso.pts([(x + 6, y + d, tz + 10), (x + w - 6, y + d, tz + 10), (x + w - 6, y + d + 12, tz), (x + 6, y + d + 12, tz)]), tint(toldo))
            for i in range(1, 6):
                a = 6 + (w - 12) * i / 6
                lz.relleno(iso.pts([(x + a, y + d, tz + 10), (x + a + 2.4, y + d, tz + 10), (x + a + 2.4, y + d + 12, tz), (x + a, y + d + 12, tz)]), tint(P.aclarar(toldo, 0.5)))
        techo_dos_aguas(lz, iso, c, eje, hr or ((d if eje == "x" else w) * 0.30), techo, vuelo=5.0, gablete=P.aclarar(muro, 0.05))
        if chimenea:
            cx, cy = x + w * 0.7, y + d * 0.35
            caja(lz, iso, cx, cy, 6, 6, 18, P.oscurecer(muro, 0.1), z0=h + (d * 0.30 if eje == "x" else w * 0.3) * 0.6)

    mundo.add(x, y, x + w, y + d, h + 30, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, d, h), clave=SOMBRA)
    _reg(mundo, x, y, w, d, h + 30, dib)


def casa_plana(mundo, x, y, w, d, h, muro=CAL, acento=AZUL, seed=0, ventanas=2):
    """Casa de azotea plana con pretil (típica de pueblo y ciudad), con barda y puerta con marco de color."""
    def dib(lz, iso):
        c = caja(lz, iso, x, y, w, d, h, muro)
        cara_rect(lz, iso, c, "y", 0, c.w, 0, 7, acento)
        cara_rect(lz, iso, c, "x", 0, c.d, 0, 7, acento)
        cara_rect(lz, iso, c, "y", 0, c.w, h - 6, h - 4, acento)
        hilera_ventanas(lz, iso, c, "y", ventanas, h * 0.40, h * 0.34, w * 0.14, margen_a=0.12, color=VENTANA, marco=acento, rejas=True)
        hilera_ventanas(lz, iso, c, "x", 1, h * 0.40, h * 0.34, d * 0.2, margen_a=0.3, color=VENTANA, marco=acento, rejas=True)
        cara_arco(lz, iso, c, "y", w * 0.5 - 7, w * 0.5 + 7, 0, h * 0.58, MADERA)
        techo_plano(lz, iso, c, P.oscurecer(muro, 0.06), borde=3.0, alto=4.0)

    mundo.add(x, y, x + w, y + d, h + 6, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, d, h), clave=SOMBRA)
    _reg(mundo, x, y, w, d, h + 6, dib)


def iglesia(mundo, x, y, w=70, largo=120, h_nave=60, muro=CANTERA, techo=TEJA, torres=2, cupula_c=True, luz_ventanas=0.0, campana=None, t_fn=None):
    """Iglesia colonial: nave a dos aguas con la fachada en el extremo +y (cara iluminada), portada de cantera con arco, columnas, nicho, ventana del coro y 1-2 torres con campanario.
    La nave corre a lo largo de y. (x, y) = esquina mínima de la nave."""
    fz = h_nave + 28                                                             # altura de la fachada
    d_f = 10
    yf = y + largo
    mundo.add(x - 6, y - 6, x + w + 6, yf + 14, h_nave + 30, lambda lz, iso: sombra_suelo(lz, iso, x - 6, y, w + 12, largo + 14, fz + 30, k=0.5), clave=SOMBRA)

    # nave + cúpula
    def nave(lz, iso):
        c = caja(lz, iso, x, y, w, largo, h_nave, muro)
        for i in range(4):
            a = largo * (0.16 + 0.24 * i)
            cara_arco(lz, iso, c, "x", a, a + 11, h_nave * 0.38, h_nave * 0.38 + 22, (96, 70, 100))
        cara_rect(lz, iso, c, "x", 0, c.d, 0, 8, P.oscurecer(muro, 0.14))
        techo_dos_aguas(lz, iso, c, "y", h_nave * 0.32, techo, vuelo=5.0, gablete=P.aclarar(muro, 0.04))
        if cupula_c:
            cx, cy = x + w / 2, y + largo * 0.34
            tz = h_nave + h_nave * 0.32
            cilindro(lz, iso, cx, cy, 15, 16, P.aclarar(muro, 0.08), z0=h_nave + 6)
            cupula(lz, iso, cx, cy, 15, (232, 190, 110), z0=h_nave + 22)
            cruz(lz, iso, cx, cy, h_nave + 22 + 22, s=0.9)
    _reg(mundo, x, y, w, largo, h_nave + 40, nave)

    # fachada
    def fachada(lz, iso):
        c = caja(lz, iso, x - 2, yf, w + 4, d_f, fz, muro)
        cara_rect(lz, iso, c, "y", 0, c.w, 0, 8, P.oscurecer(muro, 0.14))
        # portada: marco con arco
        pw = 26
        pa = (c.w - pw) / 2
        cara_rect(lz, iso, c, "y", pa - 5, pa + pw + 5, 0, 52, P.aclarar(muro, 0.22))
        cara_arco(lz, iso, c, "y", pa, pa + pw, 0, 46, MADERA)
        cara_arco(lz, iso, c, "y", pa + 4, pa + pw - 4, 0, 38, (84, 54, 50))
        for a in (pa - 8, pa + pw + 3):
            cara_rect(lz, iso, c, "y", a, a + 5, 0, 54, P.aclarar(muro, 0.3))
            cara_rect(lz, iso, c, "y", a - 1, a + 6, 52, 56, P.aclarar(muro, 0.4))
        # nicho con santo, ventana del coro y remate
        cara_arco(lz, iso, c, "y", pa + 6, pa + pw - 6, 62, 84, P.oscurecer(muro, 0.30))
        cara_rect(lz, iso, c, "y", pa + pw / 2 - 2, pa + pw / 2 + 2, 62, 76, (250, 244, 232))
        cara_arco(lz, iso, c, "y", pa + 7, pa + pw - 7, 90, 106, (96, 70, 100))
        cara_rect(lz, iso, c, "y", -1, c.w + 1, fz - 7, fz - 3, P.aclarar(muro, 0.25))
        # frontón triangular con cruz
        lz.relleno(iso.pts([(c.x - 1, c.y + c.d, fz), (c.x + c.w + 1, c.y + c.d, fz), (c.x + c.w / 2, c.y + c.d, fz + 16)]), tint(P.aclarar(muro, 0.12)))
        cruz(lz, iso, c.x + c.w / 2, c.y + c.d, fz + 16, s=1.0)
    _reg(mundo, x - 2, yf, w + 4, d_f, fz + 20, fachada, clave=(x + w / 2) + yf + d_f / 2 + 0.5)

    # torres
    def torre(tx, ty, tw, th_, alto, lado):
        def dib(lz, iso):
            c = caja(lz, iso, tx, ty, tw, tw, alto, muro)
            cara_rect(lz, iso, c, "y", 0, tw, 0, 8, P.oscurecer(muro, 0.14))
            cara_rect(lz, iso, c, "x", 0, tw, 0, 8, P.oscurecer(muro, 0.14))
            cara_arco(lz, iso, c, "y", tw * 0.3, tw * 0.7, alto * 0.38, alto * 0.38 + 16, (96, 70, 100))
            cara_rect(lz, iso, c, "y", 0, tw, alto * 0.62, alto * 0.62 + 3, P.aclarar(muro, 0.22))
            cb = caja(lz, iso, tx + 1.5, ty + 1.5, tw - 3, tw - 3, 26, P.aclarar(muro, 0.08), z0=alto)
            for cara in ("y", "x"):
                cara_arco(lz, iso, cb, cara, (tw - 3) * 0.25, (tw - 3) * 0.75, 4, 22, (70, 52, 90))
            cara_rect(lz, iso, cb, "y", 0, tw - 3, 22, 26, P.aclarar(muro, 0.25))
            if campana is not None:
                _campana(lz, iso, tx + tw / 2, ty + tw / 2, alto + 21, campana())
            techo_piramide(lz, iso, cb, 22, (232, 182, 110), vuelo=2.0)
            cruz(lz, iso, tx + tw / 2, ty + tw / 2, alto + 26 + 22, s=0.9)
        return dib

    nt = 2 if torres >= 2 else 1
    tw = 24
    xs = [x - tw - 2, x + w + 2 - 0] if nt == 2 else [x + w + 2]
    for tx in xs:
        ty = yf - 2
        _reg(mundo, tx, ty, tw, tw, fz + 70, torre(tx, ty, tw, tw, fz + 18, 1), clave=tx + tw / 2 + ty + tw / 2 + 0.2)


def portal_arcos(mundo, x, y, n, paso=20, d=14, h=40, muro=CAL, eje="x", techo=TEJA):
    """Portal con arcos (arcada de un edificio público): n arcos a lo largo de x, con columnas y techo plano."""
    w = n * paso

    def dib(lz, iso):
        base = caja(lz, iso, x, y, w, d, 3, P.oscurecer(muro, 0.1))
        c = caja(lz, iso, x, y + d - 4, w, 4, h, muro, z0=3)
        for i in range(n):
            a = i * paso
            cara_arco(lz, iso, c, "y", a + 3, a + paso - 3, 0, h * 0.8, (86, 62, 84))
            cara_rect(lz, iso, c, "y", a - 1.4, a + 1.4, 0, h, P.aclarar(muro, 0.25))
        cara_rect(lz, iso, c, "y", 0, w, h - 4, h, P.aclarar(muro, 0.2))
        caja(lz, iso, x, y, w, d, 4, P.oscurecer(muro, 0.05), z0=h + 3)

    mundo.add(x, y, x + w, y + d, h + 6, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, d, h), clave=SOMBRA)
    _reg(mundo, x, y, w, d, h + 6, dib)
    return w


def puesto(mundo, x, y, w=26, d=18, toldo=(236, 90, 96), cosas=(250, 190, 70), seed=0):
    """Puesto de mercado: mesa de madera, 4 postes y toldo a rayas."""
    def dib(lz, iso):
        for (px, py) in ((x, y), (x + w, y), (x, y + d), (x + w, y + d)):
            sx, sy = iso.P(px, py, 0)
            sy2 = iso.P(px, py, 24)[1]
            k = iso.z
            lz.relleno(rect_red(sx - 1.0 * k, sy2, 2.0 * k, sy - sy2, 0.5 * k), tint((130, 90, 66)))
        caja(lz, iso, x + 2, y + 2, w - 4, d - 4, 8, (170, 116, 80))
        sx, sy = iso.P(x + w / 2, y + d / 2, 8)
        k = iso.z
        for i in range(5):
            lz.relleno(circulo(sx + (i - 2) * 3.4 * k, sy - 2 * k - (i % 2) * 1.2 * k, 2.0 * k, 6), tint(cosas if i % 2 else P.aclarar(cosas, 0.2)))
        pts = [(x - 2, y - 2, 28), (x + w + 2, y - 2, 28), (x + w + 2, y + d + 2, 22), (x - 2, y + d + 2, 22)]
        lz.relleno(iso.pts(pts), tint(toldo))
        for i in range(0, 6, 2):
            a = (w + 4) * i / 6
            lz.relleno(iso.pts([(x - 2 + a, y - 2, 28), (x - 2 + a + (w + 4) / 6, y - 2, 28), (x - 2 + a + (w + 4) / 6, y + d + 2, 22), (x - 2 + a, y + d + 2, 22)]), tint((252, 246, 236)))

    _reg(mundo, x - 2, y - 2, w + 4, d + 4, 30, dib)


def hacienda(mundo, x, y, w=150, d=110, muro=OCRE, techo=TEJA2, capilla=True):
    """Casa grande de hacienda: cuerpo en L con portal, capilla y torre-campanario pequeña."""
    casa_colonial(mundo, x, y, w, 34, 52, muro=muro, techo=techo, eje="x", ventanas=5, balcon=True, seed=1)
    casa_colonial(mundo, x, y + 34, 34, d - 34, 52, muro=muro, techo=techo, eje="y", ventanas=2, puerta=False, seed=2)
    if capilla:
        iglesia(mundo, x + w - 46, y + 40, w=34, largo=44, h_nave=34, muro=P.aclarar(muro, 0.1), techo=techo, torres=1, cupula_c=False)


def torre_vigia(mundo, x, y, h=64, w=26, base=PIEDRA, techo=(210, 150, 80)):
    def dib(lz, iso):
        c = caja(lz, iso, x, y, w, w, h * 0.7, base)
        cara_rect(lz, iso, c, "y", 0, w, 0, 6, P.oscurecer(base, 0.15))
        cb = caja(lz, iso, x - 3, y - 3, w + 6, w + 6, 6, P.oscurecer(base, 0.05), z0=h * 0.7)
        for i in range(4):
            caja(lz, iso, x - 3 + i * ((w + 6) / 3.6), y - 3, 4.4, 3, 6, base, z0=h * 0.7 + 6)
        techo_piramide(lz, iso, Caja(x - 3, y - 3, w + 6, w + 6, 6, h * 0.7), h * 0.3, techo, vuelo=3)
    mundo.add(x, y, x + w, y + w, h + 10, lambda lz, iso: sombra_suelo(lz, iso, x, y, w, w, h), clave=SOMBRA)
    _reg(mundo, x, y, w, w, h + 10, dib)


def _campana(lz, iso, x, y, z, ang):
    """Campana de bronce colgada del travesaño del campanario; se balancea en el plano de la pantalla (ang en rad)."""
    sx, sy = iso.P(x, y, z)
    k = iso.z * 1.0
    c, s_ = math.cos(ang), math.sin(ang)

    def R(pts):
        a = np.asarray(pts, float)
        return np.stack([sx + (a[:, 0] * c - a[:, 1] * s_) * k, sy + (a[:, 0] * s_ + a[:, 1] * c) * k], 1)

    lz.relleno(R([(-6.6, -1.2), (6.6, -1.2), (6.6, 0.8), (-6.6, 0.8)]), tint((120, 78, 60)))
    lz.relleno(R([(-1.6, 0.8), (1.6, 0.8), (3.0, 3.6), (5.4, 9.2), (6.4, 11.6), (-6.4, 11.6), (-5.4, 9.2), (-3.0, 3.6)]), tint((222, 160, 50)))
    lz.relleno(R([(-1.6, 0.8), (0.4, 0.8), (0.6, 3.6), (0.8, 9.2), (0.8, 11.6), (-6.4, 11.6), (-5.4, 9.2), (-3.0, 3.6)]), tint((250, 208, 92)))
    lz.relleno(R([(2.2, 3.4), (3.0, 3.6), (5.4, 9.2), (6.4, 11.6), (4.0, 11.6), (3.2, 9.2)]), tint((176, 112, 36)))
    lz.relleno(elipse(sx + (-0.0 * c - 11.8 * s_) * k, sy + (0.0 * s_ + 11.8 * c) * k, 6.4 * k, 1.5 * k, ang, 14), tint((120, 70, 30)))
    cx_, cy_ = math.sin(ang * -1.6) * 2.4, 12.6
    lz.relleno(circulo(sx + (cx_ * c - cy_ * s_) * k, sy + (cx_ * s_ + cy_ * c) * k, 1.5 * k, 8), tint((90, 60, 40)))
