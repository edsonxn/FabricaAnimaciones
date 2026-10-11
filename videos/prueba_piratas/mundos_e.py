# -*- coding: utf-8 -*-
"""Mundos de la escena 4 (la conspiración): sala criolla de la tertulia, calle de Querétaro con la casa del corregidor, casa de dos pisos en corte (Josefa Ortiz encerrada) y los talleres de Dolores."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import h01, circulo, elipse, rect_red


# ------------------------------------------------------------------------------------------------ utilería suelta
def libro(lz, iso, x, y, z, abierto=1.0, color=(170, 60, 60), rot=0):
    """Libro sobre una mesa: tapa de color y, si está abierto, dos páginas claras con renglones."""
    if abierto > 0.5:
        lz.relleno(iso.pts([(x, y, z), (x + 9, y, z), (x + 9, y + 7, z), (x, y + 7, z)]), tint(color))
        lz.relleno(iso.pts([(x + 0.6, y + 0.6, z + 0.8), (x + 4.4, y + 0.6, z + 1.0), (x + 4.4, y + 6.4, z + 1.0), (x + 0.6, y + 6.4, z + 0.8)]), tint((252, 244, 222)))
        lz.relleno(iso.pts([(x + 4.6, y + 0.6, z + 1.0), (x + 8.4, y + 0.6, z + 0.8), (x + 8.4, y + 6.4, z + 0.8), (x + 4.6, y + 6.4, z + 1.0)]), tint((246, 236, 212)))
        for j in range(3):
            lz.relleno(iso.pts([(x + 1.2, y + 1.6 + 1.6 * j, z + 1.2), (x + 3.8, y + 1.6 + 1.6 * j, z + 1.2), (x + 3.8, y + 2.0 + 1.6 * j, z + 1.2), (x + 1.2, y + 2.0 + 1.6 * j, z + 1.2)]), tint((120, 90, 80)), alfa=0.8)
    else:
        I.caja(lz, iso, x, y, 9, 7, 2.4, color, z0=z)


def sala_criolla(lz, iso, t, W_=300, D_=250, H_=140, noche=True):
    """Sala de tertulias criolla (en corte): ventana nocturna con luna, retrato del rey Fernando (la tapadera), estantes con libros, chimenea, cortinas verdes y mesa grande con velas."""
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(168, 112, 80), pared_a=(236, 214, 170), pared_b=(226, 200, 156), friso=(120, 84, 66))
    for i in range(int(W_ / 30)):
        for j in range(int(D_ / 32)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 10 + i * 30, 10 + j * 32, 30, 32, (140, 94, 68), z=0.1, alfa=0.55)
    # pared izquierda ('yi'): ventana nocturna, retrato del rey, escudo, mapa
    N.ventana_vista(lz, iso, c, "yi", 108, 190, 36, 118, t=t, cielo=(34, 36, 104) if noche else (150, 200, 250), marco=(236, 214, 170), cortinas=(46, 120, 92), vista="ciudad")
    N.cuadro_retrato(lz, iso, c, "yi", 24, 62, 28, 36, fondo=(70, 90, 140))
    N.escudo(lz, iso, c, "yi", 268, 70, 1.1, "espana")
    # luna y estrellas en la ventana
    sx, sy = iso.P(150, 3, 96)
    lz.relleno(circulo(float(sx) + 10 * iso.z / 3, float(sy) - 6 * iso.z / 3, 7 * iso.z / 3, 16), (246, 246, 255))
    # pared derecha ('xi'): puerta, cortina, estante con libros, mapa
    I.cara_arco(lz, iso, c, "xi", 150, 202, 0, 96, (96, 66, 54))
    N.cortina(lz, iso, c, "xi", 30, 44, 0, 112, (46, 120, 92), t)
    N.mapa_pared(lz, iso, c, "xi", 76, 56, 36, 30, t=t)
    N.chimenea(lz, iso, c, "xi", 108, t=t, w=40, h=34)
    return c


def mueble_sala(m, t, ocultar_plan=1.0, plan=0.0):
    """Mesa grande con mantel verde, libros abiertos (la tapadera), candelabros, el plan oculto (pergamino que asoma) y sillas. Se añade a un Mundo isométrico."""
    m.add(70, 90, 190, 150, 24, lambda lz, iso: _mesa_tertulia(lz, iso, t, plan), clave=250)
    for i, (x, y) in enumerate(((60, 96), (60, 122), (198, 96), (198, 122), (96, 78), (140, 78))):
        m.add(x, y, x + 10, y + 10, 12, (lambda x, y: (lambda lz, iso: B.silla(lz, iso, x, y, 12, (110, 70, 52))))(x, y), clave=x + y)
    for x in (64, 200):
        m.add(x, 4, x + 42, 18, 76, (lambda x: (lambda lz, iso: B.estante(lz, iso, x, 4, 42, 14, 76)))(x), clave=x + 24)


def _mesa_tertulia(lz, iso, t, plan):
    B.mesa(lz, iso, 70, 90, 120, 60, 22, color=(120, 80, 60), mantel=(40, 120, 88))
    libro(lz, iso, 80, 100, 23.4, 1.0, (170, 60, 60))
    libro(lz, iso, 150, 98, 23.4, 1.0, (60, 100, 170))
    libro(lz, iso, 112, 132, 23.4, 1.0, (200, 160, 60))
    libro(lz, iso, 168, 126, 23.4, 0.0, (110, 60, 130))
    # el pergamino del plan asoma bajo un libro y se despliega
    if plan > 0.01:
        k = min(1.0, plan)
        lz.relleno(iso.pts([(108, 108, 23.8), (108 + 30 * k, 108, 23.8), (108 + 30 * k, 122, 23.8), (108, 122, 23.8)]), tint((252, 238, 200)))
        for j in range(3):
            lz.relleno(iso.pts([(110, 111 + 3.2 * j, 24.0), (110 + 24 * k, 111 + 3.2 * j, 24.0), (110 + 24 * k, 112 + 3.2 * j, 24.0), (110, 112 + 3.2 * j, 24.0)]), tint((150, 50, 50)), alfa=0.85)
    B.candelabro(lz, iso, 96, 120, 23, t, n=3)
    B.candelabro(lz, iso, 172, 112, 23, t + 0.7, n=3)
    for (x, y, z) in ((96, 120, 40), (172, 112, 40)):
        sx, sy = iso.P(x, y, z)
        lz.halo(float(sx), float(sy), 70 * iso.z / 3.0, (255, 200, 120), alfa=0.22, capa=2)


# ------------------------------------------------------------------------------------------------ Querétaro: calle y casa del corregidor
class CalleQueretaro:
    """Calle empedrada de Querétaro con la casa de dos pisos del corregidor (balcón corrido y zaguán), casas vecinas de colores, el acueducto al fondo, faroles y gente."""
    N = 420.0

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -60, -90, 480, 420, color_top=(220, 200, 168), t=t, seed=41, esp=36)
        I.suelo_curvo(lz, iso, [(-30, -60), (450, -60), (450, 390), (-30, 390)], (236, 218, 186))
        I.suelo_rect(lz, iso, -30, 190, 480, 90, (214, 196, 168))
        I.cuadricula(lz, iso, -30, 190, 450, 280, 14, color=(255, 255, 255), alfa=0.22)
        I.camino(lz, iso, [(-40, 235), (450, 235)], 10, (200, 182, 154))
        DC.parches(lz, iso, -60, -90, 480, 420, (228, 208, 176), n=12, var=14, seed=45, alfa=0.45, tam=(30, 70))

    def objetos(self, t, gente=1.0, farolas=0.0):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.acueducto(m, -10, -70, n=11, paso=34, h=70)
            # fila de casas del lado norte (junto al fondo); la del corregidor al centro con balcón
            cols = [A.OCRE, A.ROSA, A.AZUL, A.VERDE_CAL, A.CAL, A.OCRE]
            for i, x in enumerate((-20, 52, 120, 270, 340, 410)):
                A.casa_colonial(m, x, 100, 66 if i != 0 else 60, 70, 50 + 6 * (i % 2), muro=cols[i], techo=A.TEJA if i % 2 else A.TEJA2, eje="x", ventanas=2, balcon=(i % 2 == 0), seed=i + 60)
            A.casa_colonial(m, 190, 96, 130, 84, 80, muro=(238, 206, 150), techo=A.TEJA, eje="x", ventanas=4, balcon=True, zocalo=(170, 70, 60), seed=77)
            # lado sur
            for i, x in enumerate((-10, 70, 160, 250, 330)):
                A.casa_plana(m, x, 300, 66, 70, 44 + 4 * (i % 3), muro=[A.CAL, A.ROSA, A.OCRE, A.AZUL, A.VERDE_CAL][i], acento=[A.AZUL, A.OCRE, A.ROSA, A.VERDE_CAL, A.AZUL][i], seed=i + 90)
            for (x, y) in ((40, 196), (170, 196), (300, 196), (110, 286), (260, 286), (390, 196)):
                m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=0.0)))(x, y), clave=x + y)
            for i, x in enumerate((120, 330)):
                A.puesto(m, x, 262, toldo=[(236, 90, 96), (70, 160, 200)][i], cosas=[(250, 190, 70), (236, 120, 70)][i], seed=i)
            DC.bosque(m, -50, -60, 470, 410, n=8, seed=81, evitar=((-30, 90, 460, 190), (-30, 190, 460, 290), (-30, 290, 460, 380)), t_fn=lambda: self._t, tipos=("arbol", "cipres"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        tipos = ("regidor", "dama", "comerciante", "campesino", "mestizo", "indigena", "noble", "nino")
        if gente > 0.5:
            mu.camina([(-30, 232), (440, 232)], "arriero", vel=14, seed=11, bucle="ida_vuelta")
        for i in range(int(10 * gente)):
            mu.ronda((60 + i * 40, 236), 24, tipos[i % len(tipos)], n=1, seed=500 + i * 3, h=40 if tipos[i % len(tipos)] != "nino" else 28)
        mu.dibujar(m, t)
        if gente > 0.5:
            O.Caravana([(-30, 244), (450, 244)], n=2, vel=15, fase=0.2, seed=19).dibujar(m, t)
        if farolas > 0.01:
            for (x, y) in ((40, 196), (170, 196), (300, 196), (110, 286), (260, 286), (390, 196), (232, 226), (200, 226)):
                m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=farolas)))(x, y), fijo=False, clave=x + y + 1)
        return m


# ------------------------------------------------------------------------------------------------ la casa en corte (dos pisos)
def casa_dos_pisos(lz, iso_abajo, iso_arriba, t, H_=120, W_=260, D_=190, candado=1.0):
    """Corte de una casa de dos pisos: abajo el zaguán/oficina del alcaide; arriba la recámara donde encierran a Josefa. iso_arriba es la misma cámara subida H_ unidades en pantalla."""
    ca = I.habitacion(lz, iso_abajo, 0, 0, W_, D_, H_, piso=(150, 108, 82), pared_a=(226, 204, 160), pared_b=(214, 188, 146), friso=(110, 78, 62))
    # el techo del piso de abajo = suelo del de arriba (losa gruesa)
    I.caja(lz, iso_abajo, -4, -4, W_ + 4, D_ + 4, 5, (176, 140, 104), z0=H_ - 1)
    cb = I.habitacion(lz, iso_arriba, 0, 0, W_, D_, H_, piso=(190, 140, 104), pared_a=(240, 222, 188), pared_b=(228, 206, 172), friso=(130, 90, 74))
    return ca, cb


def cama(lz, iso, x, y, t=0.0, color=(190, 60, 70)):
    I.caja(lz, iso, x, y, 56, 34, 10, (120, 80, 60))
    I.caja(lz, iso, x + 1, y + 1, 54, 32, 5, (250, 244, 232), z0=10)
    I.caja(lz, iso, x + 1, y + 14, 54, 19, 6, color, z0=10)
    I.caja(lz, iso, x + 2, y + 2, 12, 28, 6, (255, 252, 244), z0=14)
    I.caja(lz, iso, x - 2, y - 2, 4, 38, 28, (110, 72, 54))


def puerta_cerrada(lz, iso, c, cara, a0, a1, h, candado=1.0, t=0.0):
    """Puerta de madera con herrajes y candado (cierra con llave) en una pared de la habitación."""
    I.cara_arco(lz, iso, c, cara, a0, a1, 0, h, (110, 74, 54))
    for k in range(3):
        I.cara_rect(lz, iso, c, cara, a0 + 3, a1 - 3, 14 + k * 30, 17 + k * 30, (70, 54, 52))
    # chapa y candado
    p = c.punto(cara, a1 - 8, h * 0.45)
    sx, sy = iso.P(*p)
    k = iso.z
    if candado > 0.01:
        lz.relleno(rect_red(float(sx) - 5 * k * candado, float(sy) - 4 * k * candado, 10 * k * candado, 9 * k * candado, 1.6 * k), tint((250, 206, 70)))
        lz.trazo(np.array([[float(sx) - 3 * k, float(sy) - 4 * k], [float(sx) - 3 * k, float(sy) - 9 * k], [float(sx) + 3 * k, float(sy) - 9 * k], [float(sx) + 3 * k, float(sy) - 4 * k]]), tint((180, 170, 180)), 1.8 * k, afinar=False, temblor=0.0)


# ------------------------------------------------------------------------------------------------ Dolores: los talleres del cura
class TalleresDolores:
    """Campo de Dolores con los oficios que Hidalgo enseñaba: alfarería (horno de barro, torno y vasijas), apicultura (colmenas), viñedo, telar de seda y morera. Una choza-escuela al centro."""
    N = 400.0

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -40, -40, 440, 400, color_top=(150, 190, 100), t=t, seed=52, esp=36)
        DC.parches(lz, iso, -40, -40, 440, 400, (150, 190, 100), n=16, var=22, seed=53, alfa=0.5, tam=(40, 80))
        I.suelo_curvo(lz, iso, [(130, 130), (270, 130), (290, 220), (240, 280), (130, 270), (100, 200)], (214, 186, 140))
        I.camino(lz, iso, [(-30, 340), (120, 270), (200, 200), (260, 120), (350, 60), (430, 20)], 22, (200, 168, 124), borde=(176, 140, 100))
        # viñedo en hileras (arriba a la izquierda) y milpa (abajo a la derecha)
        for j in range(8):
            I.suelo_rect(lz, iso, 6, 8 + j * 14, 100, 6, (126, 92, 66), alfa=0.9)
        DC.campos(lz, iso, 300, 230, 430, 380, nx=2, ny=2, seed=5, t=t)

    def objetos(self, t, humo=True):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            # taller de alfarería (izquierda): horno de adobe con chimenea, mesa de torno y vasijas
            m.add(300, 40, 346, 86, 50, lambda lz, iso: _horno(lz, iso, 310, 50, self._t), clave=400)
            for i, (x, y) in enumerate(((356, 44), (366, 66), (350, 86), (372, 90), (338, 100))):
                m.add(x - 4, y - 4, x + 4, y + 4, 14, (lambda x, y, i: (lambda lz, iso: _vasija(lz, iso, x, y, 1.0 + 0.3 * (i % 3), [(214, 110, 70), (230, 150, 80), (190, 86, 66), (240, 190, 100)][i % 4])))(x, y, i), clave=x + y)
            # colmenas (cajas blancas en soportes) con abejas
            for i, (x, y) in enumerate(((40, 250), (70, 262), (100, 250), (130, 266), (60, 290))):
                m.add(x - 6, y - 6, x + 6, y + 6, 24, (lambda x, y: (lambda lz, iso: _colmena(lz, iso, x, y, self._t)))(x, y), clave=x + y)
            # vid (hileras de postes con racimos)
            for j in range(8):
                for i in range(7):
                    x, y = 12 + i * 14, 6 + j * 14
                    m.add(x - 2, y - 2, x + 2, y + 2, 16, (lambda x, y: (lambda lz, iso: _vid(lz, iso, x, y)))(x, y), clave=x + y - 3)
            # morera con gusanos de seda y telar de madera
            m.add(190, 296, 220, 326, 60, lambda lz, iso: O.arbol(lz, iso, 208, 312, h=54, color=(110, 176, 90), seed=8, t=self._t), clave=620)
            m.add(240, 290, 290, 330, 50, lambda lz, iso: _telar(lz, iso, 250, 296, self._t), clave=560)
            # escuela-taller al centro (choza grande con techo de teja) y un horno de leña
            A.casa_colonial(m, 150, 80, 96, 60, 46, muro=(236, 208, 160), techo=A.TEJA, eje="x", ventanas=2, balcon=False, seed=3)
            B.choza(m, 20, 190, r=16, h=18, seed=2)
            B.choza(m, 360, 150, r=14, h=16, seed=4)
            DC.bosque(m, -30, -30, 430, 390, n=10, seed=61, evitar=((120, 70, 300, 290), (290, 30, 380, 120), (0, 0, 120, 130), (20, 230, 160, 320), (180, 280, 310, 340)), t_fn=lambda: self._t, tipos=("arbol", "cipres", "nopal"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m


def _horno(lz, iso, x, y, t):
    I.sombra_suelo(lz, iso, x, y, 40, 36, 38)
    c = I.caja(lz, iso, x, y, 40, 36, 28, (206, 140, 96))
    I.cupula(lz, iso, x + 20, y + 18, 20, (190, 120, 84), z0=28)
    I.cara_arco(lz, iso, c, "y", 8, 28, 2, 18, (60, 36, 36))
    sx, sy = iso.P(x + 20, y + 36, 8)
    lz.halo(float(sx), float(sy), 40 * iso.z / 3.0, (255, 150, 70), alfa=0.35, capa=2)
    I.cilindro(lz, iso, x + 32, y + 8, 4, 54, (170, 110, 80), z0=20)
    O.humo(lz, iso, x + 32, y + 8, 76, t, n=6, s=1.1)


def _vasija(lz, iso, x, y, s, col):
    I.sombra_elipse(lz, iso, x, y, 5 * s, 3 * s)
    I.cilindro(lz, iso, x, y, 4.6 * s, 9 * s, col, tapa=False)
    I.cilindro(lz, iso, x, y, 3.2 * s, 3 * s, P.oscurecer(col, 0.2), z0=9 * s)
    I.cono(lz, iso, x, y, 3.6 * s, 4 * s, P.aclarar(col, 0.12), z0=12 * s)


def _colmena(lz, iso, x, y, t):
    for dx in (-3, 3):
        I.caja(lz, iso, x + dx - 1, y - 1, 2, 2, 8, (130, 90, 66))
    I.caja(lz, iso, x - 7, y - 6, 14, 12, 8, (250, 232, 130), z0=8)
    I.caja(lz, iso, x - 7, y - 6, 14, 12, 4, (240, 204, 90), z0=16)
    I.caja(lz, iso, x - 8, y - 7, 16, 14, 2, (190, 70, 70), z0=20)
    sx, sy = iso.P(x, y, 22)
    for i in range(3):
        a = t * 7 + i * 2.1 + x
        lz.relleno(circulo(float(sx) + 14 * math.cos(a) * iso.z / 3, float(sy) - 8 * iso.z / 3 + 8 * math.sin(a * 1.3) * iso.z / 3, 1.7 * iso.z / 3 + 0.8, 6), (60, 50, 40), capa=2)


def _vid(lz, iso, x, y):
    I.caja(lz, iso, x - 0.6, y - 0.6, 1.2, 1.2, 14, (120, 86, 64))
    sx, sy = iso.P(x, y, 12)
    k = iso.z
    lz.relleno(circulo(float(sx), float(sy) - 3 * k, 5.4 * k, 10), tint((96, 164, 80)))
    lz.relleno(circulo(float(sx) - 2 * k, float(sy) - 5 * k, 3 * k, 8), tint((130, 196, 100)))
    for i in range(3):
        lz.relleno(circulo(float(sx) + (i - 1) * 2.4 * k, float(sy) + 1.4 * k, 1.5 * k, 6), tint((120, 60, 140)))


def _telar(lz, iso, x, y, t):
    I.sombra_suelo(lz, iso, x, y, 40, 26, 36)
    c = I.caja(lz, iso, x, y, 40, 4, 40, (150, 100, 70))
    I.caja(lz, iso, x, y + 18, 40, 4, 40, (150, 100, 70))
    I.caja(lz, iso, x, y + 4, 40, 14, 4, (170, 120, 80), z0=0)
    for i in range(8):
        I.caja(lz, iso, x + 4 + i * 4.4, y + 5, 1.1, 12, 24, [(250, 206, 90), (214, 60, 70), (80, 140, 210), (110, 190, 120)][i % 4], z0=8)
    sx, sy = iso.P(x + 20, y + 11, 32)
    lz.relleno(circulo(float(sx) + 10 * math.sin(t * 3) * iso.z / 3, float(sy), 1.8 * iso.z / 3 + 0.6, 8), (250, 244, 232), capa=2)


# ------------------------------------------------------------------------------------------------ plaza del pueblo con la tarima y el sillón vacío
class PlazaPueblo:
    """Plaza de pueblo de tierra con iglesia pequeña, casas de adobe, árboles, una tarima de madera con un sillón vacío y mucha gente del pueblo mirándola."""
    N = 360.0

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -50, -50, 410, 400, color_top=(176, 190, 110), t=t, seed=63, esp=36)
        DC.parches(lz, iso, -50, -50, 410, 400, (176, 190, 110), n=14, var=20, seed=64, alfa=0.5, tam=(40, 80))
        I.suelo_curvo(lz, iso, [(20, 80), (340, 80), (350, 340), (10, 350)], (226, 200, 150))
        I.cuadricula(lz, iso, 20, 80, 340, 340, 26, color=(255, 255, 255), alfa=0.12)
        I.camino(lz, iso, [(180, 340), (180, 420)], 40, (214, 188, 140))
        DC.parches(lz, iso, 20, 80, 340, 340, (214, 188, 140), n=10, var=14, seed=65, alfa=0.5, tam=(30, 60))

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            A.iglesia(m, 110, -20, w=70, largo=80, h_nave=56, torres=2, campana=None)
            for i, x in enumerate((-30, 200, 262, 316)):
                A.casa_colonial(m, x, 0 if i else 8, 60, 56, 40 + 4 * (i % 2), muro=[A.CAL, A.OCRE, A.ROSA, A.AZUL][i], techo=A.TEJA, eje="x", ventanas=2, balcon=False, seed=i + 120)
            for i, y in enumerate((100, 170, 240, 300)):
                A.casa_plana(m, -40, y, 48, 52, 38, muro=[A.OCRE, A.CAL, A.ROSA, A.VERDE_CAL][i], acento=A.AZUL, seed=i + 130)
            # tarima con sillón vacío al centro-fondo
            m.add(130, 120, 200, 170, 20, lambda lz, iso: _tarima(lz, iso, 130, 120, self._t), clave=300)
            for (x, y) in ((50, 100), (320, 100), (50, 330), (320, 330)):
                m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=0.0)))(x, y), clave=x + y)
            m.add(180, 330, 200, 350, 30, lambda lz, iso: O.pozo(lz, iso, 190, 340, 1.3), clave=530)
            DC.bosque(m, -50, -50, 410, 400, n=10, seed=66, evitar=((100, -30, 200, 80), (-50, -10, 60, 340), (190, -10, 380, 70), (20, 80, 350, 350)), t_fn=lambda: self._t, tipos=("arbol", "cipres", "nopal"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m


def _tarima(lz, iso, x, y, t):
    I.sombra_suelo(lz, iso, x, y, 70, 50, 14)
    I.caja(lz, iso, x, y, 70, 50, 10, (160, 112, 76))
    I.caja(lz, iso, x + 2, y + 2, 66, 46, 3, (190, 140, 96), z0=10)
    N.sillon(lz, iso, x + 24, y + 12, 22, 18, (190, 52, 66), "y")
    # halo dorado difuso sobre el sillón que pulsa (el lugar del líder)
    sx, sy = iso.P(x + 35, y + 20, 30)
    lz.halo(float(sx), float(sy), (46 + 6 * math.sin(t * 3)) * iso.z / 3.0, (255, 220, 120), alfa=0.30, capa=2)
