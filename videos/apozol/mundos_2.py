# -*- coding: utf-8 -*-
"""Mundos de la escena 2 (el valle): el cañón en isométrico con el río, las paredes en terrazas de roca (sierra de Morones al oeste, de Nochistlán
al este), el pueblo de hoy (templo, casas, milpas) y, al poniente, la aldea caxcana en terrazas de cultivo; más la ciudad de Tlatlán al sur."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_deco as DC
import kz_gente_iso as G
import plano as P
from motor import catmull, h01, prog, smooth, W, H

ROCA = [(150, 108, 138), (186, 124, 130), (214, 150, 120)]            # estratos: violeta, rosado, ocre
TOPE = (118, 170, 100)
RIO = [(440, -300), (410, -140), (452, 40), (420, 220), (460, 400), (430, 700)]
X0, X1, Y0, Y1 = -150, 700, -300, 760


def iso_en(iso, zb):
    """Cámara desplazada: lo que se dibuja con z = 0 aparece sobre una terraza de altura zb."""
    return I.Iso(iso.cx, iso.cy, iso.cz - zb, iso.z, sx0=iso.sx0, sy0=iso.sy0)


def terraza(lz, iso, x, y, w, d, h, estratos=ROCA, tope=TOPE, seed=0):
    n = max(1, int(h // 22))
    for k in range(n):
        I.caja(lz, iso, x, y, w, d, h / n + 0.6, estratos[(k + seed) % len(estratos)], z0=h * k / n)
    I.suelo_rect(lz, iso, x, y, w, d, tope, z=h)


def cinta(pts, ancho):
    c = np.array(catmull(np.array(pts, float), 10, False))
    d = np.gradient(c, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= (np.hypot(nrm[:, 0], nrm[:, 1])[:, None] + 1e-9)
    return np.vstack([c + nrm * ancho / 2, (c - nrm * ancho / 2)[::-1]])


def piramide(m, x, y, w=90, niveles=3, h=64, color=(222, 198, 168), clave=0):
    """Pirámide escalonada con escalinata al frente y un templete arriba."""
    def dib(lz, iso):
        hh = h / niveles
        for k in range(niveles):
            o = k * w * 0.13
            c = I.caja(lz, iso, x + o, y + o, w - 2 * o, w - 2 * o, hh + 0.5, P.aclarar(color, 0.03 * k), z0=hh * k)
            ww = (w - 2 * o) * 0.26
            I.cara_rect(lz, iso, c, "y", (w - 2 * o) / 2 - ww / 2, (w - 2 * o) / 2 + ww / 2, 0, hh, (196, 172, 144))
        tx, ty = x + w / 2 - w * 0.1, y + w / 2 - w * 0.1
        c2 = I.caja(lz, iso, tx, ty, w * 0.2, w * 0.2, 14, (236, 214, 176), z0=h)
        I.techo_piramide(lz, iso, c2, 10, (190, 90, 70))
    m.add(x, y, x + w, y + w, h + 26, dib, clave=clave or x * 5 + y)


class Canon:
    """Mundo del valle. `modo`: "hoy" (pueblo colonial) | "caxcan" (aldea de terrazas al poniente + contorno fantasma del pueblo) | "ambos"."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    # ------------------------------------------------------------------ suelo
    def suelo(self, lz, iso, t):
        I.isla(lz, iso, X0, Y0, X1, Y1, color_top=(150, 190, 112), t=t, seed=21, esp=44)
        DC.parches(lz, iso, X0, Y0, X1, Y1, (150, 190, 112), n=34, var=22, seed=22, alfa=0.55, tam=(50, 120))
        O.agua(lz, iso, cinta(RIO, 64), t, z=-1.0, seed=4)
        DC.hierba(lz, iso, X0, Y0, X1, Y1, n=210, seed=8, t=t, color=(112, 170, 92), flores=0.10)

    # ------------------------------------------------------------------ objetos
    def _estatico(self, t_fn):
        m = I.Mundo()
        # paredes de roca en terrazas a ambos lados (el oeste, la sierra de Morones, más alta)
        pasos = {-1: ((90, 60), (110, 130), (120, 214)), 1: ((90, 44), (100, 92))}
        for lado, base in ((-1, X0 + 8), (1, X1 - 8)):
            acum = 0
            for k, (ancho, alto) in enumerate(pasos[lado]):
                x = base - acum - ancho if lado < 0 else base + acum
                acum += ancho
                for j in range(9):
                    y = Y0 - 40 + j * 130
                    h = alto + 10 * math.sin(j * 1.3 + k)
                    m.add(x, y, x + ancho, y + 134, h + 4, (lambda x, y, ancho, h, k, j: (lambda lz, iso: terraza(lz, iso, x, y, ancho, 134, h, seed=j + k)))(x, y, ancho, h, k, j),
                          clave=x * 3 + y)
                    for q in range(2):
                        px, py = x + 14 + (ancho - 28) * h01(40 + k, j, q), y + 10 + 110 * h01(41 + k, j, q + 3)
                        tipo = (j + q + k) % 3
                        fn = (lambda px, py, h, tipo: (lambda lz, iso: (O.arbol(lz, iso_en(iso, h), px, py, h=46, seed=int(px + py), t=t_fn()) if tipo == 0 else
                                                                         O.organo(lz, iso_en(iso, h), px, py, h=40, seed=int(px)) if tipo == 1 else
                                                                         O.nopal(lz, iso_en(iso, h), px, py, s=1.0, seed=int(py)))))(px, py, h, tipo)
                        m.add(px - 6, py - 6, px + 6, py + 6, h + 40, fn, clave=px + py * 7)
        return m

    def objetos(self, t, modo="hoy", gente=1.0, tributo=0.0, ciudad=False, contorno=True):
        self._t = t
        if self._est is None:
            self._est = self._estatico(lambda: self._t)
        m = I.Mundo()
        m.topo = False
        m.fijos = list(self._est.fijos)
        if modo in ("hoy", "ambos"):
            self._pueblo(m, t, fantasma=(modo == "ambos"))
        if modo in ("caxcan", "ambos"):
            self._aldea(m, t, gente)
            if modo == "caxcan" and contorno:
                self._contorno(m)
        # milpas junto al río
        for (x, y, w, d, s) in ((300, -230, 90, 120, 1), (300, -40, 90, 120, 2), (300, 150, 90, 130, 3), (300, 350, 90, 130, 4), (500, -210, 90, 130, 5), (510, 30, 90, 130, 6), (500, 270, 90, 130, 7)):
            m.add(x, y, x + w, y + d, 26, (lambda x, y, w, d, s: (lambda lz, iso: O.milpa(lz, iso, x, y, w, d, t=self._t, seed=s)))(x, y, w, d, s), clave=x + y)
        # el camino
        # (el camino va en el suelo: ver suelo_camino)
        if ciudad:
            self._tlatlan(m, t, tributo, gente)
        DC.bosque(m, X0 + 20, Y0 + 10, X1 - 20, Y1 - 10, n=26, seed=51, evitar=((-110, -300, 10, 760), (110, -300, 330, 760), (300, -300, 600, 760)), t_fn=lambda: self._t,
                  tipos=("arbol", "arbusto"), colores=[(110, 168, 98), (96, 150, 90), (128, 176, 104)])
        return m

    def camino(self, lz, iso):
        I.camino(lz, iso, [(250, -280), (236, -60), (270, 140), (244, 360), (262, 680)], 34, (232, 214, 170), borde=(208, 188, 144))

    def _pueblo(self, m, t, fantasma=False):
        A.iglesia(m, 150, 70, w=64, largo=104, h_nave=54, muro=A.CANTERA, techo=A.TEJA, torres=1, cupula_c=False)
        casas = ((60, -150, 60, 44), (60, -60, 62, 44), (60, 230, 58, 44), (60, 320, 64, 44), (170, 200, 62, 46), (170, 290, 60, 46), (170, 380, 66, 46), (170, -130, 60, 44),
                 (170, -40, 64, 44), (60, 410, 60, 42), (-30, 40, 58, 42), (-30, 140, 62, 42))
        for i, (x, y, w, d) in enumerate(casas):
            A.casa_colonial(m, x, y, w, d, 36 + 6 * (i % 3), muro=[A.CAL, A.OCRE, A.ROSA, A.VERDE_CAL][i % 4], techo=A.TEJA if i % 2 else A.TEJA2, eje="x", ventanas=2, seed=i,
                            puerta=True, chimenea=(i % 3 == 0), humo_t=(lambda: self._t) if i % 3 == 0 else None)
        m.add(120, 195, 140, 215, 24, lambda lz, iso: O.pozo(lz, iso, 130, 205), clave=3)

    def _aldea(self, m, t, gente):
        # terrazas de cultivo que suben por la ladera del poniente y chozas de adobe con techo de palma
        for k, (x, w, h) in enumerate(((-100, 70, 10), (-170, 70, 22), (-240, 70, 34))):
            for j in range(5):
                y = -200 + j * 190
                m.add(x, y, x + w, y + 180, h + 4,
                      (lambda x, y, w, h, k, j: (lambda lz, iso: (I.caja(lz, iso, x, y, w, 180, h, (176, 130, 98), z0=0), I.suelo_rect(lz, iso, x, y, w, 180, (134, 178, 96), z=h),
                                                                   O.milpa(lz, iso_en(iso, h), x + 6, y + 8, w - 12, 164, t=self._t, seed=k * 9 + j, color=(96, 170, 86)))))(x, y, w, h, k, j),
                      clave=x * 3 + y + 1)
        chozas = ((-40, -50), (10, -30), (-44, 20), (6, 40), (-36, 90), (14, 112), (-48, 160), (2, 180), (-20, 230), (30, 210), (-70, 60), (-76, 130), (34, 270), (-4, 20))
        for i, (x, y) in enumerate(chozas):
            B.choza(m, x, y, r=14 + 2 * (i % 3), h=19, seed=i, techo=(226, 190, 100) if i % 2 else (210, 168, 92))
        # fogatas con humo
        for (x, y) in ((-14, 0), (-10, 130), (-4, 250)):
            m.add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y: (lambda lz, iso: (O.fuego(lz, iso, x, y, s=0.7, t=self._t, seed=int(y)), O.humo(lz, iso, x, y, 14, self._t, n=5, s=0.9, seed=int(x)))))(x, y),
                  fijo=False, clave=x + y * 9)
        if gente > 0.01:
            mu = G.Multitud()
            for i in range(7):
                mu.ronda((-30 + 16 * (i % 3), -40 + 44 * i), 30, "caxcana" if i % 2 else "caxcan", n=1, vel=3 + i % 3, seed=900 + i, h=46, accion="trabaja" if i % 3 == 0 else None)
            mu.quieto((50, 90), "caxcan_anciano", dir=(1, 0), seed=920, h=46, accion="habla")
            mu.quieto((66, 100), "caxcana", dir=(-1, 0), seed=921, h=46, accion="habla")
            mu.camina([(110, -150), (60, -20), (70, 120), (60, 260)], "caxcan_mazo", vel=8, seed=930, h=46)
            mu.dibujar(m, t)

    def _contorno(self, m):
        """Contorno fantasma de donde hoy está el pueblo (para decir «al poniente de donde hoy está»)."""
        def dib(lz, iso):
            x, y, w, d = 40, -170, 220, 600
            pts = np.array([[x, y, 0], [x + w, y, 0], [x + w, y + d, 0], [x, y + d, 0]], float)
            q = iso.pts(pts)
            lz.relleno(q, (255, 255, 255), alfa=0.16)
            P.discontinua(lz, np.vstack([q, q[:1]]), (255, 255, 255), ancho=5.0, largo=26.0, hueco=18.0, fase=-self._t * 22.0)
        m.add(40, -170, 260, 430, 4, dib, fijo=False, clave=-77)

    def _tlatlan(self, m, t, tributo, gente):
        """Tlatlán (hoy Juchipila), al sur: plaza con pirámides, chozas y gente; el tributo llega por el camino desde el norte."""
        piramide(m, 160, 520, w=110, niveles=4, h=78, clave=501)
        piramide(m, 330, 560, w=80, niveles=3, h=52, color=(214, 188, 158), clave=502)
        for i, (x, y) in enumerate(((60, 560), (60, 620), (100, 660), (260, 640), (230, 700), (330, 690), (400, 640), (30, 480), (300, 470), (380, 500))):
            B.choza(m, x, y, r=12 + (i % 2) * 2, h=16, seed=40 + i, techo=(226, 190, 100) if i % 2 else (208, 170, 96))
        mu = G.Multitud()
        for i in range(7):
            mu.camina([(240, -200), (236, -20), (270, 160), (246, 360), (262, 560)], "caxcan_mazo" if i % 3 == 0 else "caxcan", vel=14, seed=700 + i, h=38,
                      fase=0.14 * i * (1 if tributo >= 0 else 0), accion="carga", bucle=True)
        for i in range(5):
            mu.ronda((250 + 30 * (i % 3), 600), 50, "caxcana" if i % 2 else "caxcan_sacerdote", n=1, vel=3, seed=720 + i, h=38)
        mu.dibujar(m, t)
