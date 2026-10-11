# -*- coding: utf-8 -*-
"""Mundos de la escena 10 (la refundación): Juchipila refundada en diorama isométrico (traza de plaza y calles junto al río; casas que se
levantan de adobe; capilla franciscana de 1542 que en 1627 ya es el templo de San Francisco de Asís), la fila de los que bajan de paz, y la
columna de insurgentes de 1810 en 2D."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_iso_deco as DC
import kz_gente_iso as G
import kz_pers2d as K2
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H

ADOBE = (196, 150, 112)
RIO = [(-260, 420), (-120, 300), (-60, 120), (-90, -80), (-40, -300)]
LOTES = [(60, -150, 0), (150, -150, 1), (240, -150, 0), (330, -140, 1), (60, 250, 0), (150, 250, 1), (240, 250, 0), (330, 240, 1),
         (420, -40, 0), (420, 60, 1), (420, 160, 0), (10, 40, 1), (10, 140, 0)]


class PuebloNuevo:
    """obra 0..1 = cuántas casas están levantadas (las que van subiendo se ven como muros de adobe crecientes con andamio);
    templo 0..1 = de capilla de adobe (0) a templo de cantera con torre (1)."""

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -300, -320, 560, 420, color_top=(136, 186, 98), t=t, seed=51, esp=34)
        DC.parches(lz, iso, -300, -320, 560, 420, (136, 186, 98), n=22, var=20, seed=52, alfa=0.5, tam=(40, 100))
        O.agua(lz, iso, self._cinta(RIO, 46), t, z=-1.0, seed=6)
        I.suelo_curvo(lz, iso, [(30, -200), (470, -200), (480, 320), (0, 320)], (214, 196, 146))
        I.camino(lz, iso, [(-40, 100), (520, 100)], 30, (236, 220, 172), borde=(212, 192, 142))
        I.camino(lz, iso, [(200, -260), (200, 380)], 30, (236, 220, 172), borde=(212, 192, 142))
        I.suelo_rect(lz, iso, 120, 20, 160, 160, (240, 226, 182))                       # plaza
        I.cuadricula(lz, iso, 120, 20, 280, 180, 32, color=(255, 255, 255), alfa=0.18)
        O.milpa(lz, iso, -280, -300, 180, 150, t=t, seed=3)
        O.milpa(lz, iso, -280, 200, 150, 160, t=t, seed=4)
        DC.hierba(lz, iso, -300, -320, 560, 420, n=120, seed=53, t=t, color=(112, 170, 88), flores=0.08)

    @staticmethod
    def _cinta(pts, ancho):
        c = np.array(catmull(np.array(pts, float), 10, False))
        d = np.gradient(c, axis=0)
        nrm = np.stack([-d[:, 1], d[:, 0]], 1)
        nrm /= (np.hypot(nrm[:, 0], nrm[:, 1])[:, None] + 1e-9)
        return np.vstack([c + nrm * ancho / 2, (c - nrm * ancho / 2)[::-1]])

    def objetos(self, t, obra, templo, gente=1.0, convento=0.0):
        m = I.Mundo()
        n = len(LOTES)
        for i, (x, y, eje) in enumerate(LOTES):
            u = np.clip(obra * (n + 2) - i, 0.0, 1.0)                   # cada casa sube a su turno
            if u <= 0.01:
                continue
            w, d = (54, 40) if eje == 0 else (40, 54)
            if u < 0.999:                                               # muros de adobe que crecen + andamio
                h = 36 * smooth(u)
                m.add(x, y, x + w, y + d, h + 6, (lambda x, y, w, d, h: (lambda lz, iso: self._obra(lz, iso, x, y, w, d, h)))(x, y, w, d, h), fijo=False)
            else:
                A.casa_colonial(m, x, y, w, d, 36, muro=(236, 214, 182) if i % 3 else (226, 196, 160), eje="x" if eje == 0 else "y", ventanas=1, seed=i,
                                chimenea=i % 4 == 0, humo_t=0.0 if i % 4 == 0 else None)
        # capilla de 1542 o templo de 1627 (al norte de la plaza)
        if templo < 0.5:
            m.add(130, -120, 210, -20, 60, lambda lz, iso: self._capilla(lz, iso), fijo=False)
        else:
            A.iglesia(m, 130, -130, w=74, largo=110, h_nave=58, muro=A.CANTERA, techo=A.TEJA, torres=1, cupula_c=True)
        if convento > 0.5:                                              # convento franciscano: claustro con arcos junto al templo
            A.portal_arcos(m, 220, -130, 4, paso=20, d=16, h=34, muro=(236, 222, 196), eje="x")
            A.casa_colonial(m, 220, -114, 84, 54, 40, muro=(236, 222, 196), eje="x", ventanas=3, seed=99)
        # árboles de la plaza y la orilla
        for i, (x, y) in enumerate(((140, 40), (260, 40), (140, 160), (260, 160))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=44, seed=i, t=t)))(x, y, i), fijo=False)
        for i in range(6):
            x, y = -160 + 20 * (i % 2), -250 + 110 * i
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=52, seed=i + 7, t=t)))(x, y, i), fijo=False)
        if gente > 0.01:
            mu = G.Multitud()
            for i in range(8):                                          # cargan adobes de la orilla a las obras
                mu.camina([(-30, 60 + 12 * i), (110 + 30 * (i % 3), 60 + 12 * i)], "caxcan" if i % 2 else "caxcana", vel=9, seed=1700 + i, h=38, fase=0.12 * i, bucle=True,
                          accion="carga")
            for i in range(4):
                mu.ronda((200 + 40 * (i % 2), 100 + 40 * (i // 2)), 30, "caxcana" if i % 2 else "caxcan_anciano", n=1, vel=3, seed=1720 + i, h=38)
            mu.quieto((170, 0), "fraile", dir=(0, 1), seed=1730, h=40, accion="habla")
            mu.quieto((230, 0), "fraile", dir=(0, 1), seed=1731, h=40, accion="saluda")
            mu.dibujar(m, t)
        return m

    @staticmethod
    def _obra(lz, iso, x, y, w, d, h):
        I.caja(lz, iso, x, y, w, d, h, ADOBE)
        for k in range(int(h // 6)):                                    # hiladas de adobe
            z = 6 * k + 3
            a, b = iso.P(x, y + d, z), iso.P(x + w, y + d, z)
            lz.trazo(np.array([a, b]), (170, 126, 92), 1.4, afinar=False, temblor=0.0, capa=1)
        for (px, py) in ((x - 4, y + d + 4), (x + w + 4, y + d + 4)):    # andamio
            a, b = iso.P(px, py, 0), iso.P(px, py, h + 12)
            lz.trazo(np.array([a, b]), (150, 106, 70), 3.0, afinar=False, temblor=0.0, capa=1)

    @staticmethod
    def _capilla(lz, iso):
        c = I.caja(lz, iso, 140, -110, 60, 80, 40, (222, 190, 150))
        I.techo_dos_aguas(lz, iso, c, "y", 18, (196, 150, 90), tejas=False)
        I.cara_arco(lz, iso, c, "y", 22, 38, 0, 26, (90, 60, 50))
        I.cruz(lz, iso, 170, -30, 62, s=1.2)


# ------------------------------------------------------------------------------------------------ 2D: los que bajan de paz
def bajada_paz(lz, t, u, cx=0.0):
    """Ladera con sendero en zigzag por la que baja una multitud (corriente de puntos lejos, personajes cerca) con mantas blancas."""
    lz.relleno(np.array([(-40, 300), (500, 160), (900, 260), (1300, 140), (1960, 300), (1960, H), (-40, H)]), (150, 120, 150), capa=0)
    lz.relleno(np.array([(-40, 520), (700, 420), (1200, 520), (1960, 460), (1960, H), (-40, H)]), (132, 160, 104), capa=0)
    zig = [(560, 200), (900, 300), (500, 400), (1000, 520), (600, 650), (1200, 800), (1500, 1100)]
    q = np.array(catmull(np.array(zig, float), 12, False))
    lz.trazo(q, (226, 206, 168), 34.0, afinar=False, temblor=0.0, capa=1)
    seg = np.hypot(*np.diff(q, axis=0).T)
    d = np.r_[0, np.cumsum(seg)]
    for i in range(42):
        f = (i / 42 + 0.025 * (t - 0.0)) % 1.0
        if f > u:
            continue
        s_ = d[-1] * f
        j = int(np.clip(np.searchsorted(d, s_) - 1, 0, len(q) - 2))
        v = (s_ - d[j]) / max(1e-6, d[j + 1] - d[j])
        px, py = q[j] + (q[j + 1] - q[j]) * v
        sc = 5 + 20 * max(0.0, (py - 200) / 900) ** 1.3
        dirx = 1 if q[j + 1][0] >= q[j][0] else -1
        spec = K2.variar("caxcana" if i % 3 == 1 else "caxcan", 1800 + i)
        K2.cuerpo(lz, px, py + 6, sc, spec, t, piernas="camina", brazos="balanceo" if i % 5 else "arriba", mirar=dirx, vista="perfil", seed=1800 + i,
                  cara="auto", sombra=False, ph=t * 4.5 + i, emocion="neutro")
        if i % 5 == 0 and sc > 8:                                       # manta blanca en alto (señal de paz)
            lz.relleno(rect_red(px + dirx * 0.6 * sc - 1.2 * sc, py - 11.5 * sc, 2.4 * sc, 1.4 * sc, 0.2 * sc), (250, 248, 240), capa=2)


# ------------------------------------------------------------------------------------------------ 2D: 1810, se suman a los insurgentes
def estandarte_guadalupano(lz, x, y, s, t, capa=2):
    """Estandarte con la Virgen de Guadalupe (óvalo de rayos dorados, manto azul-verde) en un asta."""
    lz.relleno(rect_red(x - 0.12 * s, y - 9 * s, 0.24 * s, 9 * s, 0), (120, 84, 60), capa=capa)
    ond = [(x + 0.1 * s + 4.2 * s * u, y - 9 * s + 0.3 * s * math.sin(t * 4 + u * 4)) for u in np.linspace(0, 1, 8)]
    tela = np.array(ond + [(p[0], p[1] + 5 * s) for p in ond[::-1]])
    lz.relleno(tela, (250, 240, 214), capa=capa)
    cx, cy = x + 2.2 * s, y - 6.5 * s + 0.3 * s * math.sin(t * 4 + 2)
    lz.relleno(elipse(cx, cy, 1.5 * s, 2.0 * s, 0, 28), (255, 196, 70), capa=capa)
    for k in range(16):
        a = k * math.pi / 8
        lz.trazo(np.array([(cx + math.cos(a) * 1.2 * s, cy + math.sin(a) * 1.6 * s), (cx + math.cos(a) * 1.75 * s, cy + math.sin(a) * 2.3 * s)]), (255, 214, 90), 0.12 * s,
                 afinar=False, temblor=0.0, capa=capa)
    lz.relleno(elipse(cx, cy + 0.2 * s, 0.8 * s, 1.5 * s, 0, 20), (40, 120, 120), capa=capa)
    lz.relleno(elipse(cx, cy - 0.6 * s, 0.3 * s, 0.35 * s, 0, 12), (214, 160, 120), capa=capa)
    lz.relleno(elipse(cx, cy + 0.5 * s, 0.35 * s, 0.9 * s, 0, 12), (220, 110, 110), capa=capa)
