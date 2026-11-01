# -*- coding: utf-8 -*-
"""Mundos de la escena 3 (conquista y fundación): la columna de Oñate que baja por el camino, la infografía de la encomienda, el diorama de
San Miguel Atotonilco junto a la poza de agua caliente (que se levanta casa por casa), el arcángel San Miguel y las ruinas del primer templo."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_deco as DC
import kz_gente_iso as G
import kz_pers2d as K2
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H
import mundos_2 as M2

ADOBE = (196, 150, 112)


# ------------------------------------------------------------------------------------------------ la columna española en el cañón
def columna(m, t, t0, vel=26.0, y_ini=-300.0):
    """Capitán a caballo con banderas, soldados, aliados indígenas y caballos que bajan por el camino (de norte a sur). Todo es función de t."""
    u = max(0.0, t - t0)
    cam = lambda y: 236 + 18 * math.sin((y + 60) * 0.011)          # x del camino a esa altura (aprox.)
    # capitán y banderas al frente
    yc = y_ini + vel * u + 120
    m.add(cam(yc) - 10, yc - 10, cam(yc) + 10, yc + 10, 40, lambda lz, iso: G.caballo(lz, iso, cam(yc) - 4, yc, t, dir=1, seed=3, color=(236, 232, 226), vel=1.0, jinete="capitan_esp", s=1.5),
          fijo=False, clave=yc * 3 + 1)
    m.add(cam(yc) - 36, yc - 24, cam(yc) - 24, yc - 12, 90, lambda lz, iso: O2.faro_bandera(lz, iso, cam(yc) - 34, yc - 18, t=t, h=90), fijo=False, clave=yc * 3 + 2)
    # caballos de apoyo
    for i, dy in enumerate((-80, -170)):
        yy = yc + dy
        xo = cam(yy) + (22 if i % 2 else -24)
        m.add(xo - 10, yy - 10, xo + 10, yy + 10, 40, (lambda xo, yy, i: (lambda lz, iso: G.caballo(lz, iso, xo, yy, t, dir=1, seed=10 + i, vel=1.0, jinete="conquistador", s=1.35)))(xo, yy, i),
              fijo=False, clave=yy * 3 + 3)
    # infantería y aliados, en dos filas
    for i in range(14):
        yy = y_ini + vel * u - 10 - 30 * i
        tipo = ("conquistador", "conquistador_lanza")[i % 2] if i < 7 else "aliado"
        xx = cam(yy) + (-18 if i % 2 else 18)
        m.add(xx - 5, yy - 5, xx + 5, yy + 5, 48, (lambda xx, yy, tipo, i: (lambda lz, iso: G.persona(lz, iso, xx, yy, t, tipo=tipo, dir=(0.0, 1.0), vel=10.0, seed=200 + i, h=54)))(xx, yy, tipo, i),
              fijo=False, clave=yy * 3 + 5)
    return yc


# ------------------------------------------------------------------------------------------------ San Miguel Atotonilco
class Atotonilco:
    """Diorama de la fundación: poza termal con vapor, capilla de adobe, casas que se levantan, milpas y gente. obra 0..1."""
    POZA = [(250, 110), (292, 96), (330, 120), (336, 160), (306, 192), (262, 196), (236, 168)]
    LOTES = [(60, -20, 54, 40), (60, 70, 54, 40), (60, 160, 54, 40), (150, 250, 54, 40), (250, 260, 54, 40), (350, 250, 54, 40), (40, 250, 54, 40),
             (400, 80, 54, 40), (400, 170, 54, 40)]

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -160, 560, 420, color_top=(146, 190, 106), t=t, seed=61, esp=40)
        DC.parches(lz, iso, -120, -160, 560, 420, (146, 190, 106), n=26, var=20, seed=62, alfa=0.5, tam=(40, 100))
        I.camino(lz, iso, [(-100, 220), (120, 210), (320, 224), (540, 210)], 30, (232, 214, 170), borde=(208, 188, 144))
        O.bahia(lz, iso, [(x, y) for x, y in self.POZA], t, seed=7, c_orilla=(150, 236, 228), c_medio=(72, 196, 226), c_hondo=(40, 140, 214))
        DC.hierba(lz, iso, -120, -160, 560, 420, n=150, seed=63, t=t, color=(112, 170, 88), flores=0.10)

    def objetos(self, t, obra=1.0, templo=1.0, gente=1.0, vapor=1.0):
        m = I.Mundo()
        m.topo = False
        n = len(self.LOTES)
        for i, (x, y, w, d) in enumerate(self.LOTES):
            u = float(np.clip(obra * (n + 2) - i, 0.0, 1.0))
            if u <= 0.01:
                continue
            if u < 0.999:
                h = 36 * smooth(u)
                m.add(x, y, x + w, y + d, h + 6, (lambda x, y, w, d, h: (lambda lz, iso: self._obra(lz, iso, x, y, w, d, h)))(x, y, w, d, h), fijo=False, clave=x + y * 3)
            else:
                A.casa_colonial(m, x, y, w, d, 34, muro=[(236, 214, 182), (226, 196, 160), (240, 222, 190)][i % 3], eje="x" if i % 2 else "y", ventanas=1, seed=i,
                                chimenea=(i % 3 == 0), humo_t=0.0 if i % 3 == 0 else None)
        if templo > 0.02:
            m.add(120, -90, 200, 0, 70, (lambda k: (lambda lz, iso: self._capilla(lz, iso, k)))(templo), fijo=False, clave=-5)
        # rocas y vapor junto a la poza
        for i, (x, y, s) in enumerate(((236, 100, 1.1), (330, 106, 1.0), (346, 170, 1.2), (226, 176, 0.9), (290, 206, 1.0), (262, 90, 0.8))):
            m.add(x - 8, y - 8, x + 8, y + 8, 16, (lambda x, y, s, i: (lambda lz, iso: O.roca(lz, iso, x, y, s=s, seed=i, color=(158, 136, 134))))(x, y, s, i), clave=x + y)
        if vapor > 0.01:
            for i, (x, y) in enumerate(((270, 140), (300, 150), (284, 128))):
                m.add(x - 6, y - 6, x + 6, y + 6, 120, (lambda x, y, i: (lambda lz, iso: O.humo(lz, iso, x, y, 4, t, n=7, s=1.8 * vapor, color=(250, 248, 244), vel=18.0, seed=i, alfa=0.75)))(x, y, i),
                      fijo=False, clave=x + y * 5 + 1000)
        for i, (x, y) in enumerate(((20, -120), (330, -110), (-40, 300), (460, 300), (200, 330), (-60, 90))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=48, seed=i + 5, t=t)))(x, y, i), clave=x + y * 7)
        for (x, y, w, d, s) in ((-100, -140, 90, 120, 1), (420, -130, 100, 110, 2), (-100, 300, 100, 100, 3)):
            m.add(x, y, x + w, y + d, 26, (lambda x, y, w, d, s: (lambda lz, iso: O.milpa(lz, iso, x, y, w, d, t=t, seed=s)))(x, y, w, d, s), clave=x + y)
        if gente > 0.01:
            mu = G.Multitud()
            for i in range(6):
                mu.camina([(-60, 214 + 4 * i), (160, 212), (330, 224 + 2 * i), (500, 214)], "caxcan" if i % 2 else "caxcana", vel=8 + i % 3, seed=3100 + i, h=40, fase=0.15 * i,
                          accion="carga" if i % 2 else None)
            for i in range(4):
                mu.ronda((270 + 10 * i, 160), 70, "caxcana" if i % 2 else "caxcan_anciano", n=1, vel=3, seed=3120 + i, h=40)
            mu.quieto((160, 40), "fraile", dir=(0, 1), seed=3130, h=42, accion="reza")
            mu.dibujar(m, t)
        return m

    @staticmethod
    def _obra(lz, iso, x, y, w, d, h):
        I.caja(lz, iso, x, y, w, d, h, ADOBE)
        for k in range(int(h // 6)):
            z = 6 * k + 3
            a, b = iso.P(x, y + d, z), iso.P(x + w, y + d, z)
            lz.trazo(np.array([a, b]), (170, 126, 92), 1.4, afinar=False, temblor=0.0, capa=1)
        for (px, py) in ((x - 4, y + d + 4), (x + w + 4, y + d + 4)):
            a, b = iso.P(px, py, 0), iso.P(px, py, h + 12)
            lz.trazo(np.array([a, b]), (150, 106, 70), 3.0, afinar=False, temblor=0.0, capa=1)

    @staticmethod
    def _capilla(lz, iso, k=1.0):
        h = 44 * smooth(float(np.clip(k, 0, 1)))
        c = I.caja(lz, iso, 130, -80, 60, 80, max(2.0, h), (236, 214, 182))
        if k > 0.7:
            I.techo_dos_aguas(lz, iso, c, "y", 20, (200, 100, 78), tejas=True)
            I.cara_arco(lz, iso, c, "y", 22, 38, 0, 28, (96, 62, 56))
            I.cruz(lz, iso, 160, 0, 74, s=1.2)


# ------------------------------------------------------------------------------------------------ ruinas del primer templo
def ruinas(lz, iso, t):
    """Restos de la capilla de Santiago: muros a medio caer, un arco partido, vigas y piedras caídas, con una cruz inclinada."""
    c1 = I.caja(lz, iso, 100, 40, 64, 12, 56, (200, 176, 148))                        # muro frontal roto, con puerta de arco
    I.cara_arco(lz, iso, c1, "y", 22, 42, 0, 38, (80, 58, 52))
    I.caja(lz, iso, 100, 40, 20, 12, 84, (208, 184, 156))                              # pilar alto (el resto de la fachada)
    I.caja(lz, iso, 100, 52, 12, 92, 46, (190, 166, 140))                              # muro izquierdo bajo
    I.caja(lz, iso, 152, 52, 12, 52, 26, (186, 162, 136))                              # muro derecho casi caído
    I.caja(lz, iso, 100, 144, 64, 10, 14, (180, 156, 130))                             # resto del muro del fondo
    for (x, y, w, d, h, z0) in ((118, 90, 40, 5, 4, 0), (132, 110, 36, 5, 4, 0)):       # vigas caídas
        I.caja(lz, iso, x, y, w, d, h, (122, 84, 62), z0=z0)
    for (x, y, s, sd) in ((170, 90, 1.0, 1), (130, 130, 1.3, 2), (180, 120, 0.8, 3), (90, 110, 1.1, 4), (150, 160, 0.9, 5), (112, 70, 0.7, 6), (176, 60, 0.8, 7)):
        O.roca(lz, iso, x, y, s=s, seed=sd, color=(190, 166, 140))
    sx, sy = iso.P(112, 46, 86)
    z = iso.z
    lz.trazo(np.array([(sx, sy), (sx + 10 * z, sy - 48 * z)]), (240, 232, 214), 6.0 * z, afinar=False, temblor=0.0, capa=1)
    lz.trazo(np.array([(sx - 12 * z, sy - 30 * z), (sx + 28 * z, sy - 42 * z)]), (240, 232, 214), 6.0 * z, afinar=False, temblor=0.0, capa=1)


def ruinas_mundo(t):
    """Ruinas con su entorno seco: nopales, magueyes, rocas, maleza y un árbol muerto (la escena de «hoy solo quedan ruinas»)."""
    m = I.Mundo()
    m.topo = False
    m.add(96, 36, 170, 160, 130, lambda lz, iso: ruinas(lz, iso, t), fijo=False, clave=1)
    for i, (x, y) in enumerate(((236, 34), (270, 96), (34, 96), (206, 8), (24, 214), (276, 210))):
        m.add(x - 8, y - 8, x + 8, y + 8, 40, (lambda x, y, i: (lambda lz, iso: O.nopal(lz, iso, x, y, s=0.95, seed=i, t=t)))(x, y, i), clave=x + y * 7)
    for i, (x, y) in enumerate(((62, 30), (232, 190), (150, 232))):
        m.add(x - 8, y - 8, x + 8, y + 8, 30, (lambda x, y, i: (lambda lz, iso: O.maguey(lz, iso, x, y, s=0.9, seed=i, t=t)))(x, y, i), clave=x + y * 5)
    for i, (x, y, s) in enumerate(((20, 20, 1.2), (250, 20, 1.0), (130, 220, 1.3), (276, 160, 0.9), (82, 226, 1.0), (190, 20, 0.9))):
        m.add(x - 8, y - 8, x + 8, y + 8, 18, (lambda x, y, s, i: (lambda lz, iso: O.roca(lz, iso, x, y, s=s, seed=20 + i, color=(176, 154, 130))))(x, y, s, i), clave=x + y * 3)
    for i, (x, y, r) in enumerate(((120, 190, 10), (160, 24, 9), (214, 100, 8), (74, 130, 9), (190, 150, 8), (250, 90, 9))):
        m.add(x - 6, y - 6, x + 6, y + 6, 16, (lambda x, y, r, i: (lambda lz, iso: O.arbusto(lz, iso, x, y, r=r, seed=i + 3, color=(124, 138, 84))))(x, y, r, i), clave=x + y * 9)
    m.add(26, 62, 40, 76, 60, lambda lz, iso: O.arbol(lz, iso, 32, 68, h=52, seed=9, t=t, color=(118, 104, 84)), clave=77)
    return m


# ------------------------------------------------------------------------------------------------ 2D: San Miguel arcángel, encomienda
def san_miguel(lz, x, y, s, t, alfa=1.0, capa=2):
    """Arcángel San Miguel, estilizado (alas, túnica azul, capa roja, yelmo dorado, espada y escudo). (x, y) = pies; s ≈ alto/100."""
    lz.halo(x, y - 90 * s, 150 * s, (255, 236, 160), alfa=0.55 * alfa, dureza=1.2, capa=capa)
    fl = math.sin(t * 2.2) * 0.06
    for sg in (-1, 1):                                                              # alas
        for i in range(7):
            a = math.radians(-8 - 17 * i) + fl
            L = (110 - 6 * i) * s
            bx, by = x + sg * 14 * s, y - 96 * s
            tx, ty = bx + sg * math.cos(a) * L, by + math.sin(a) * L * 0.9
            nx, ny = -math.sin(a) * 9 * s, math.cos(a) * 9 * s
            lz.relleno(np.array([(bx, by), (bx + (tx - bx) * 0.5 + sg * nx, by + (ty - by) * 0.5 + ny), (tx, ty), (bx + (tx - bx) * 0.5 - sg * nx, by + (ty - by) * 0.5 - ny)]),
                       (250, 246, 236) if i % 2 else (255, 214, 120), alfa=alfa, capa=capa)
    lz.relleno(np.array([(x - 30 * s, y - 118 * s), (x + 30 * s, y - 118 * s), (x + 38 * s, y - 100 * s), (x + 30 * s, y - 40 * s), (x - 30 * s, y - 40 * s), (x - 38 * s, y - 100 * s)]),
               (200, 56, 70), alfa=alfa, capa=capa)                                  # capa
    lz.relleno(np.array([(x - 24 * s, y - 112 * s), (x + 24 * s, y - 112 * s), (x + 30 * s, y), (x - 30 * s, y)]), (60, 112, 226), alfa=alfa, capa=capa)   # túnica
    lz.relleno(np.array([(x - 24 * s, y - 112 * s), (x - 4 * s, y - 112 * s), (x - 6 * s, y), (x - 30 * s, y)]), (88, 140, 240), alfa=alfa, capa=capa)
    lz.relleno(rect_red(x - 26 * s, y - 70 * s, 52 * s, 8 * s, 2 * s), (255, 206, 72), alfa=alfa, capa=capa)                              # cinturón
    lz.relleno(circulo(x, y - 128 * s, 17 * s, 20), (246, 204, 170), alfa=alfa, capa=capa)                                              # cabeza
    lz.relleno(np.array([(x - 19 * s, y - 130 * s), (x + 19 * s, y - 130 * s), (x + 16 * s, y - 150 * s), (x, y - 156 * s), (x - 16 * s, y - 150 * s)]), (255, 206, 72), alfa=alfa, capa=capa)  # yelmo
    lz.relleno(np.array([(x - 4 * s, y - 154 * s), (x + 4 * s, y - 154 * s), (x + 12 * s, y - 178 * s), (x, y - 166 * s)]), (214, 60, 70), alfa=alfa, capa=capa)                       # penacho
    lz.relleno(circulo(x - 7 * s, y - 128 * s, 2.2 * s, 8), (50, 30, 40), alfa=alfa, capa=capa)
    lz.relleno(circulo(x + 7 * s, y - 128 * s, 2.2 * s, 8), (50, 30, 40), alfa=alfa, capa=capa)
    # espada en alto y escudo
    lz.trazo(np.array([(x + 30 * s, y - 96 * s), (x + 58 * s, y - 188 * s)]), (240, 244, 252), 7 * s, afinar=False, temblor=0.0, capa=capa)
    lz.trazo(np.array([(x + 22 * s, y - 104 * s), (x + 44 * s, y - 100 * s)]), (255, 206, 72), 7 * s, afinar=False, temblor=0.0, capa=capa)
    lz.relleno(circulo(x - 36 * s, y - 70 * s, 22 * s, 24), (250, 244, 230), alfa=alfa, capa=capa)
    lz.trazo(np.array([(x - 36 * s, y - 88 * s), (x - 36 * s, y - 52 * s)]), (214, 60, 70), 6 * s, afinar=False, temblor=0.0, capa=capa)
    lz.trazo(np.array([(x - 50 * s, y - 72 * s), (x - 22 * s, y - 72 * s)]), (214, 60, 70), 6 * s, afinar=False, temblor=0.0, capa=capa)


def saco(lz, x, y, s, color=(214, 170, 96), capa=2, alfa=1.0):
    """Costal de maíz (origen en la base)."""
    lz.relleno(np.array([(x - 20 * s, y), (x + 20 * s, y), (x + 24 * s, y - 26 * s), (x + 14 * s, y - 46 * s), (x - 14 * s, y - 46 * s), (x - 24 * s, y - 26 * s)]), color, alfa=alfa, capa=capa)
    lz.relleno(np.array([(x + 4 * s, y), (x + 20 * s, y), (x + 24 * s, y - 26 * s), (x + 14 * s, y - 46 * s), (x + 4 * s, y - 46 * s)]), P.oscurecer(color, 0.18), alfa=alfa, capa=capa)
    lz.relleno(rect_red(x - 14 * s, y - 50 * s, 28 * s, 8 * s, 3 * s), P.oscurecer(color, 0.12), alfa=alfa, capa=capa)


def manta(lz, x, y, s, color=(226, 70, 120), capa=2, alfa=1.0):
    """Manta de algodón doblada con franjas (origen en la base)."""
    lz.relleno(rect_red(x - 30 * s, y - 24 * s, 60 * s, 24 * s, 3 * s), color, alfa=alfa, capa=capa)
    for k in range(3):
        lz.relleno(rect_red(x - 30 * s, y - 20 * s + 7 * s * k, 60 * s, 3.4 * s, 0), (250, 230, 190) if k % 2 == 0 else (80, 190, 190), alfa=alfa, capa=capa)
