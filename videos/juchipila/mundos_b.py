# -*- coding: utf-8 -*-
"""Mundos de la escena 2 (el cañón): el pueblo en el fondo del cañón (isométrico, con paredes en terrazas, río, milpas) y el corte transversal (2D)."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_deco as DC
import kz_gente_iso as G
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, W, H, ruido1
import paisajes as PA


def iso_en(iso, zb):
    """Cámara desplazada: lo que se dibuja con z = 0 aparece sobre una terraza de altura zb."""
    return I.Iso(iso.cx, iso.cy, iso.cz - zb, iso.z, sx0=iso.sx0, sy0=iso.sy0)


ROCA = [(150, 108, 138), (186, 124, 130), (214, 150, 120)]            # estratos: violeta, rosado, ocre
TOPE = (118, 170, 100)


def terraza(lz, iso, x, y, w, d, h, estratos=ROCA, tope=TOPE, seed=0):
    """Bloque de roca con estratos horizontales y tope de pasto."""
    n = max(1, int(h // 22))
    for k in range(n):
        z0 = h * k / n
        c = I.caja(lz, iso, x, y, w, d, h / n + 0.6, estratos[(k + seed) % len(estratos)], z0=z0)
    I.suelo_rect(lz, iso, x, y, w, d, tope, z=h)
    return c


class CanonPueblo:
    """El pueblo de Juchipila en el fondo del cañón: río serpenteando, calle con casas e iglesia en la orilla oeste, milpas al este y paredes en terrazas con árboles."""
    RIO = [(250, -200), (232, -40), (262, 120), (236, 270), (276, 430), (258, 560)]

    def __init__(self):
        self._est = None
        self._t = 0.0

    def _cinta(self, pts, ancho):
        c = np.array(catmull(np.array(pts, float), 10, False))
        d = np.gradient(c, axis=0)
        nrm = np.stack([-d[:, 1], d[:, 0]], 1)
        nrm /= (np.hypot(nrm[:, 0], nrm[:, 1])[:, None] + 1e-9)
        return np.vstack([c + nrm * ancho / 2, (c - nrm * ancho / 2)[::-1]])

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -140, -230, 640, 620, color_top=(150, 190, 112), t=t, seed=21, esp=40)
        DC.parches(lz, iso, -140, -230, 640, 620, (150, 190, 112), n=26, var=22, seed=22, alfa=0.55, tam=(50, 110))
        O.agua(lz, iso, self._cinta(self.RIO, 58), t, z=-1.0, seed=4)
        I.camino(lz, iso, [(120, -200), (110, 20), (140, 200), (110, 380), (130, 560)], 34, (230, 212, 168), borde=(206, 186, 142))
        DC.hierba(lz, iso, -140, -230, 640, 620, n=170, seed=8, t=t, color=(112, 170, 92), flores=0.10)

    def paredes(self, lz, iso, t):
        """Paredes del cañón (a ambos lados) en terrazas de roca con estratos, árboles y cactus encima."""
        for lado, base in ((-1, -140), (1, 640)):
            for k, (ancho, alto) in enumerate(((70, 46), (80, 96), (90, 150))):
                if lado < 0:
                    x = base - sum((70, 80, 90)[:k + 1])
                else:
                    x = base + sum((70, 80, 90)[:k])
                for j in range(8):
                    y = -300 + j * 120
                    terraza(lz, iso, x, y, ancho, 124, alto + 12 * math.sin(j * 1.3 + k), seed=j + k)
        return

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            # paredes: bloques de roca con estratos (uno por celda) y vegetación encima
            for lado, base in ((-1, -140), (1, 640)):
                for k, (ancho, alto) in enumerate(((70, 46), (80, 96), (90, 150))):
                    x = base - sum((70, 80, 90)[:k + 1]) if lado < 0 else base + sum((70, 80, 90)[:k])
                    for j in range(9):
                        y = -330 + j * 120
                        h = alto + 10 * math.sin(j * 1.3 + k)
                        m.add(x, y, x + ancho, y + 124, h + 4, (lambda x, y, ancho, h, k, j: (lambda lz, iso: terraza(lz, iso, x, y, ancho, 124, h, seed=j + k)))(x, y, ancho, h, k, j), clave=x * 3 + y)
                        for q in range(2):
                            px, py = x + 14 + (ancho - 28) * h01(40 + k, j, q), y + 10 + 100 * h01(41 + k, j, q + 3)
                            tipo = (j + q + k) % 3
                            if tipo == 0:
                                m.add(px - 6, py - 6, px + 6, py + 6, h + 40, (lambda px, py, h: (lambda lz, iso: O.arbol(lz, iso_en(iso, h), px, py, h=46, seed=int(px + py), t=self._t)))(px, py, h), clave=px + py * 7)
                            elif tipo == 1:
                                m.add(px - 6, py - 6, px + 6, py + 6, h + 30, (lambda px, py, h: (lambda lz, iso: O.organo(lz, iso_en(iso, h), px, py, h=40, seed=int(px))))(px, py, h), clave=px + py * 7)
                            else:
                                m.add(px - 6, py - 6, px + 6, py + 6, h + 20, (lambda px, py, h: (lambda lz, iso: O.nopal(lz, iso_en(iso, h), px, py, s=1.0, seed=int(py))))(px, py, h), clave=px + py * 7)
            # pueblo: iglesia, casas, milpas, árboles, pozo, mercado
            A.iglesia(m, 60, 110, w=62, largo=100, h_nave=52, muro=A.CANTERA, techo=A.TEJA, torres=1, cupula_c=False)
            for i, (x, y, w, d) in enumerate(((30, 250, 64, 46), (30, 330, 60, 46), (30, 410, 66, 46), (30, 480, 62, 46), (160, 240, 60, 44), (160, 330, 66, 44), (160, 420, 60, 44), (-40, 30, 58, 42), (-40, 150, 62, 42))):
                A.casa_colonial(m, x, y, w, d, 38 + 6 * (i % 3), muro=[A.CAL, A.OCRE, A.ROSA, A.VERDE_CAL][i % 4], techo=A.TEJA if i % 2 else A.TEJA2, eje="x", ventanas=2, seed=i, puerta=True,
                                chimenea=(i % 3 == 0), humo_t=(lambda: self._t) if i % 3 == 0 else None)
            m.add(110, 215, 130, 235, 24, lambda lz, iso: O.pozo(lz, iso, 120, 225), clave=3)
            for (x, y, w, d, s) in ((320, 40, 140, 120, 1), (320, 190, 140, 110, 2), (320, 330, 150, 120, 3), (-90, 330, 90, 110, 4)):
                m.add(x, y, x + w, y + d, 26, (lambda x, y, w, d, s: (lambda lz, iso: O.milpa(lz, iso, x, y, w, d, t=self._t, seed=s)))(x, y, w, d, s), clave=x + y)
            DC.bosque(m, -130, -220, 630, 600, n=26, seed=51, evitar=((20, 20, 220, 600), (300, -200, 480, 600), (-100, 20, 100, 450)), t_fn=lambda: self._t, tipos=("arbol", "arbusto"), colores=[(110, 168, 98), (96, 150, 90), (128, 176, 104)])
            self._est = m
        m = I.Mundo()
        m.topo = False
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        mu.camina([(116, -160), (112, 40), (132, 200), (112, 380), (130, 540)], "campesina", vel=9, seed=71, fase=0.05, h=44)
        mu.camina([(130, 540), (112, 380), (132, 200), (112, 40), (116, -160)], "campesino", vel=10, seed=72, fase=0.40, h=44)
        mu.camina([(110, 300), (138, 260), (112, 200)], "nino", vel=8, seed=73, fase=0.2, h=30)
        mu.ronda((350, 120), 40, "campesino", n=2, vel=4, seed=74, h=44, accion="trabaja")
        mu.ronda((380, 260), 40, "campesina", n=2, vel=4, seed=76, h=44, accion="trabaja")
        mu.ronda((380, 400), 40, "campesino", n=2, vel=4, seed=78, h=44, accion="trabaja")
        mu.quieto((100, 200), "indigena_f", dir=(1, 0), seed=80, h=44, accion="habla")
        mu.dibujar(m, t)
        px_ = -140 + 640 * ((t * 0.03 + 0.2) % 1.0)
        m.add(px_ - 6, 70, px_ + 6, 80, 22, (lambda px_: (lambda lz, iso: G.burro(lz, iso, px_, 75, t, dir=1, seed=3)))(px_), fijo=False, clave=px_ + 75)
        return m


# ------------------------------------------------------------------------------------------------ corte transversal (infografía 2D)
BASE_Y = 900.0
M_IZQ = [(-80, -20), (140, -330), (330, -520), (520, -430), (690, -250), (830, -110), (905, -62)]        # (x, altura sobre la base) — sierra de Morones
M_DER = [(1015, -62), (1090, -110), (1240, -290), (1470, -440), (1680, -350), (1850, -250), (2000, -300)]  # sierra de Nochistlán


def _perfil(pts, e):
    P_ = [(x, BASE_Y + dy * e) for x, dy in pts]
    return catmull(np.array(P_, float), 8, False)


def corte_canon(lz, t, u, alfa=1.0, estratos=True):
    """Corte del cañón de lado a lado: sierra de Morones (izquierda), sierra de Nochistlán (derecha) y el pueblo en el fondo.
    u 0..1 = el relieve se levanta. Devuelve los puntos clave (cima izquierda, cima derecha, fondo del valle) para colocar rótulos."""
    e = smooth(u)
    for pts, col, luz, sh in ((M_IZQ, (126, 72, 134), (255, 176, 104), (96, 52, 108)), (M_DER, (100, 58, 118), (255, 176, 104), (76, 42, 92))):
        per = _perfil(pts, e)
        poli = np.vstack([per, [(per[-1][0], BASE_Y + 200), (per[0][0], BASE_Y + 200)]])
        lz.relleno(poli, sh, alfa=alfa, capa=1)
        lz.relleno(np.vstack([per + np.array([0.0, 0.0]), [(per[-1][0], BASE_Y + 200), (per[0][0], BASE_Y + 200)]]) + np.array([0.0, 0.0]), col, alfa=alfa, capa=1)
        if estratos:
            for k in range(7):
                yk = BASE_Y - 60 * k * e - 30
                with lz.recorte(poli):
                    lz.relleno(np.array([(-100, yk), (2100, yk - 18), (2100, yk - 4), (-100, yk + 12)]), sh, alfa=0.35 * alfa, capa=1)
        lz.relleno(np.vstack([per, per[::-1] + np.array([0.0, 16.0])]), luz, alfa=0.55 * alfa, capa=1)          # filo de luz en la cresta
        for q in range(15):                                                                                     # árboles y cactus sobre la ladera
            xq = per[0][0] + (per[-1][0] - per[0][0]) * (0.04 + 0.92 * h01(60 + int(pts[0][0]), q, 1))
            yq = float(np.interp(xq, per[:, 0], per[:, 1]))
            if e > 0.4 and abs(xq - 960) > 110:
                PA.arbol(lz, xq, yq + 10, (0.55 + 0.45 * h01(61, q, 2)) * e, 0.0, seed=q, t=t, capa=1)
    # fondo del valle: roca continua con una cinta de pasto y el río arriba, y las casitas del pueblo
    yv = BASE_Y - 62 * e
    lz.relleno(np.array([(880, BASE_Y + 200), (905, yv), (1015, yv), (1040, BASE_Y + 200)]), (112, 65, 124), alfa=alfa, capa=1)
    lz.relleno(np.array([(905, yv), (1015, yv), (1020, yv + 22), (900, yv + 22)]), (140, 188, 108), alfa=alfa, capa=1)
    lz.relleno(elipse(960, yv + 8, 46, 7, 0, 24), (86, 170, 226), alfa=alfa, capa=2)
    if e > 0.7:
        for dx in (-30, 24):
            lz.relleno(np.array([(960 + dx - 14, yv + 4), (960 + dx + 14, yv + 4), (960 + dx + 14, yv - 14), (960 + dx - 14, yv - 14)]), (240, 214, 170), alfa=alfa, capa=2)
            lz.relleno(np.array([(960 + dx - 18, yv - 12), (960 + dx + 18, yv - 12), (960 + dx, yv - 28)]), (196, 90, 76), alfa=alfa, capa=2)
    return dict(izq=(330, BASE_Y - 520 * e), der=(1470, BASE_Y - 440 * e), valle=(960, BASE_Y - 62 * e))
