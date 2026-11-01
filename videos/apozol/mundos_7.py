# -*- coding: utf-8 -*-
"""Mundos de la escena 7 (hoy): línea de tiempo proporcional 1863–1918, la balanza del ministro, la plaza de Apozol en isométrico (kiosco, laurel,
monumento, templo, bancas y vecinos), la fiesta nocturna (papel picado, cohetes, charros), los tastoanes y el cierre de agua."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_deco as DC
import kz_gente_iso as G
import kz_pers2d as K2
import kz_ui as U
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H
import mundos_4 as M4
import mundos_2 as M2

COLORES_HOY = [(236, 120, 110), (120, 190, 210), (250, 206, 110), (170, 140, 220), (130, 200, 150), (240, 170, 120)]


# ------------------------------------------------------------------------------------------------ línea de tiempo proporcional
def linea_tiempo(lz, t, a0, a1, y, x0, x1, hitos, t_ini, k=1.0, banda=None):
    """Línea con décadas a escala. hitos = [(año, texto, color, t_aparece)]; banda = (año0, año1, texto, color) para un periodo."""
    if k <= 0.01:
        return
    X = lambda a: x0 + (x1 - x0) * (a - a0) / float(a1 - a0)
    f = smooth(prog(t, t_ini, t_ini + 1.0))
    lz.relleno(rect_red(x0 - 24, y - 70, (x1 - x0 + 48) * f, 150, 26), (30, 14, 70), alfa=0.7 * k, capa=2)
    lz.relleno(rect_red(x0, y - 5, (x1 - x0) * f, 10, 5), (255, 214, 90), alfa=k, capa=2)
    for a in range(int(math.ceil(a0 / 10.0) * 10), a1 + 1, 10):
        if X(a) <= x0 + (x1 - x0) * f:
            lz.relleno(rect_red(X(a) - 2, y - 14, 4, 28, 1), (255, 236, 170), alfa=0.9 * k, capa=2)
            P.rotulo(lz, X(a), y + 44, str(a), px=24, color=(255, 255, 255), alfa=0.8 * k, sombra=0.0)
    if banda is not None:
        b0, b1, txt, col = banda
        kb = smooth(prog(t, t_ini + 0.4, t_ini + 1.4))
        lz.relleno(rect_red(X(b0), y - 40, (X(b1) - X(b0)) * kb, 26, 8), col, alfa=0.85 * k, capa=2)
        if kb > 0.5:
            P.rotulo(lz, (X(b0) + X(b1)) / 2, y - 26, txt, px=22, color=(255, 255, 255), alfa=k, sombra=0.0)
    for a, txt, col, t0 in hitos:
        kk = U.pop(t, t0)
        if kk > 0.01:
            lz.relleno(circulo(X(a), y, 18 * kk, 18), col, capa=2)
            lz.relleno(circulo(X(a), y, 8 * kk, 12), (255, 255, 255), capa=2)
            U.llamada(lz, X(a), y - 90, txt, color=col, px=44, k=kk * k, cola="abajo")


# ------------------------------------------------------------------------------------------------ la balanza (Suprema Corte)
def balanza(lz, x, y, s, t, k=1.0, alfa=1.0, capa=2):
    """Balanza dorada con un leve vaivén. (x, y) = base."""
    if k <= 0.01:
        return
    s = s * k
    oro, oro2 = (255, 206, 72), (214, 150, 40)
    lz.relleno(rect_red(x - 60 * s, y - 14 * s, 120 * s, 14 * s, 5 * s), oro2, alfa=alfa, capa=capa)
    lz.relleno(rect_red(x - 8 * s, y - 190 * s, 16 * s, 180 * s, 4 * s), oro, alfa=alfa, capa=capa)
    lz.relleno(circulo(x, y - 196 * s, 18 * s, 16), oro, alfa=alfa, capa=capa)
    bal = 0.07 * math.sin(t * 1.5)
    L = 150 * s
    ax, ay = x - math.cos(bal) * L, y - 190 * s - math.sin(bal) * L
    bx, by = x + math.cos(bal) * L, y - 190 * s + math.sin(bal) * L
    lz.trazo(np.array([(ax, ay), (bx, by)]), oro, 12 * s, afinar=False, temblor=0.0, capa=capa)
    for (px, py) in ((ax, ay), (bx, by)):
        for dx in (-50, 50):
            lz.trazo(np.array([(px, py), (px + dx * s, py + 120 * s)]), oro2, 3.5 * s, afinar=False, temblor=0.0, capa=capa)
        lz.relleno(np.array([(px - 56 * s, py + 120 * s), (px + 56 * s, py + 120 * s), (px + 38 * s, py + 146 * s), (px - 38 * s, py + 146 * s)]), oro, alfa=alfa, capa=capa)


# ------------------------------------------------------------------------------------------------ la plaza de hoy (isométrico)
class Plaza:
    """Jardín principal: kiosco, laurel enorme, monumento a Juárez, templo, bancas, farolas, casas de colores y vecinos."""

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -160, -160, 420, 360, color_top=(140, 188, 104), t=t, seed=171, esp=36)
        DC.parches(lz, iso, -160, -160, 420, 360, (140, 188, 104), n=18, var=18, seed=172, alfa=0.5, tam=(40, 90))
        I.suelo_rect(lz, iso, 20, 20, 220, 150, (240, 226, 182))
        I.cuadricula(lz, iso, 20, 20, 240, 170, 22, color=(255, 255, 255), alfa=0.18)
        I.camino(lz, iso, [(130, -160), (130, 20)], 30, (232, 214, 170), borde=(208, 188, 144))
        I.camino(lz, iso, [(-160, 100), (20, 100)], 30, (232, 214, 170), borde=(208, 188, 144))
        I.camino(lz, iso, [(240, 100), (420, 100)], 30, (232, 214, 170), borde=(208, 188, 144))
        DC.hierba(lz, iso, -160, -160, 420, 360, n=130, seed=173, t=t, color=(112, 170, 88), flores=0.08)

    def objetos(self, t, atardecer=0.0, gente=1.0):
        m = I.Mundo()
        m.topo = False
        A.iglesia(m, -60, -130, w=72, largo=112, h_nave=58, muro=A.CANTERA, techo=A.TEJA, torres=1, cupula_c=True, luz_ventanas=atardecer)
        # casas de colores al fondo y a los lados
        for i, (x, y, w, d) in enumerate(((60, -140, 60, 44), (140, -140, 64, 44), (230, -140, 60, 44), (270, -20, 44, 60), (-150, 30, 44, 62), (-150, 130, 44, 62), (280, 130, 50, 56), (60, 240, 62, 44), (160, 240, 62, 44))):
            A.casa_colonial(m, x, y, w, d, 36 + 10 * (i % 3 == 0), muro=COLORES_HOY[i % 6], eje="x" if w >= d else "y", ventanas=1, seed=i, balcon=(i % 3 == 0))
        # kiosco
        m.add(60, 80, 100, 120, 44, lambda lz, iso: self._kiosco(lz, iso, 80, 100), fijo=False, clave=11)
        # el laurel enorme
        m.add(170, 60, 210, 100, 130, lambda lz, iso: self._laurel(lz, iso, 190, 80, t), fijo=False, clave=12)
        # monumento a Juárez
        m.add(110, 130, 130, 150, 60, lambda lz, iso: self._monumento(lz, iso, 120, 140), fijo=False, clave=13)
        # bancas y farolas
        for i, (x, y) in enumerate(((150, 126), (190, 126), (50, 40), (210, 30))):
            m.add(x - 12, y - 5, x + 12, y + 5, 14, (lambda x, y: (lambda lz, iso: self._banca(lz, iso, x, y)))(x, y), clave=x + y * 3 + 20)
        for i, (x, y) in enumerate(((30, 30), (230, 30), (30, 160), (230, 160))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, h=38, t=t, encendido=atardecer)))(x, y), fijo=False, clave=x + y * 5 + 30)
        for i, (x, y) in enumerate(((-110, -140), (330, -120), (-110, 280), (330, 260), (20, 280))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=50, seed=i + 3, t=t)))(x, y, i), clave=x + y * 7)
        if gente > 0.01:
            mu = G.Multitud()
            tipos = ("campesino", "campesina", "dama", "nino", "comerciante", "mestizo")
            for i in range(9):
                mu.camina([(30 + 40 * (i % 4), 30 + 30 * (i % 5)), (220 - 30 * (i % 3), 150 - 25 * (i % 4)), (140, 100)], tipos[i % 6], vel=6 + i % 3, seed=4100 + i, h=40, fase=0.1 * i, bucle=True)
            for i in range(5):
                mu.ronda((140, 110), 70, tipos[(i + 2) % 6], n=1, vel=3, seed=4120 + i, h=40)
            mu.quieto((160, 138), "campesina", dir=(0, 1), seed=4140, h=40, accion="habla")
            mu.quieto((176, 138), "campesino", dir=(0, 1), seed=4141, h=40, accion="habla")
            mu.dibujar(m, t)
        return m

    @staticmethod
    def _kiosco(lz, iso, x, y):
        I.cilindro(lz, iso, x, y, 22, 6, (236, 226, 206))
        for k in range(8):
            a = k * math.pi / 4
            I.cilindro(lz, iso, x + 18 * math.cos(a), y + 18 * math.sin(a), 1.4, 26, (90, 120, 110), z0=6)
        I.cono(lz, iso, x, y, 26, 16, (90, 150, 130), z0=32)

    @staticmethod
    def _laurel(lz, iso, x, y, t):
        I.sombra_elipse(lz, iso, x + 4, y + 6, 54, 30, alfa=0.28)
        I.cilindro(lz, iso, x, y, 7, 46, (122, 86, 66))
        for (dx, dy, r, h, c) in ((-26, 0, 30, 66, (60, 142, 84)), (24, 6, 32, 70, (68, 152, 90)), (0, -18, 34, 88, (76, 164, 98)), (-6, 18, 30, 84, (60, 142, 84)),
                                  (4, 0, 38, 108, (86, 176, 106)), (-30, -10, 24, 96, (68, 152, 90)), (30, -8, 24, 100, (76, 164, 98))):
            sx, sy = iso.P(x + dx, y + dy, h)
            z = iso.z
            bal = math.sin(t * 1.1 + dx) * 2 * z
            lz.relleno(circulo(float(sx) + bal, float(sy), r * z * 1.05, 20), P.oscurecer(c, 0.22))
            lz.relleno(circulo(float(sx) - 3 * z + bal, float(sy) - 4 * z, r * z * 0.92, 20), c)
            lz.relleno(circulo(float(sx) - 9 * z + bal, float(sy) - 10 * z, r * z * 0.5, 16), P.aclarar(c, 0.18))

    @staticmethod
    def _monumento(lz, iso, x, y):
        I.caja(lz, iso, x - 12, y - 12, 24, 24, 10, (206, 196, 184))
        c = I.caja(lz, iso, x - 8, y - 8, 16, 16, 30, (226, 216, 202), z0=10)
        I.cara_rect(lz, iso, c, "y", 3, 13, 8, 18, (150, 120, 70))                              # placa de bronce
        sx, sy = iso.P(x, y, 44)
        z = iso.z
        lz.relleno(np.array([(sx - 14 * z, sy + 6 * z), (sx + 14 * z, sy + 6 * z), (sx + 10 * z, sy - 10 * z), (sx - 10 * z, sy - 10 * z)]), (150, 120, 70))      # busto de bronce
        lz.relleno(circulo(float(sx), float(sy) - 18 * z, 9 * z, 14), (176, 142, 84))
        lz.relleno(circulo(float(sx) - 3 * z, float(sy) - 21 * z, 3 * z, 8), (214, 180, 120))

    @staticmethod
    def _banca(lz, iso, x, y):
        I.caja(lz, iso, x - 12, y - 4, 24, 8, 4, (150, 100, 70), z0=6)
        I.caja(lz, iso, x - 12, y - 6, 24, 2, 8, (130, 86, 60), z0=8)
        for dx in (-10, 10):
            I.caja(lz, iso, x + dx - 1, y - 3, 2, 6, 6, (96, 66, 50))


# ------------------------------------------------------------------------------------------------ fiesta nocturna
def papel_picado(lz, t, y=150, n=16, capa=1, alfa=1.0):
    """Cuerdas de banderines de papel picado que ondean."""
    cols = [(236, 70, 140), (255, 206, 72), (60, 200, 200), (122, 52, 200), (255, 130, 60), (90, 200, 120)]
    for fila, (yy, amp) in enumerate(((y, 38), (y + 90, 30))):
        pts = [(x, yy + amp * math.sin(x / W * math.pi)) for x in np.linspace(-40, W + 40, 18)]
        lz.trazo(np.array(pts), (60, 40, 80), 3.0, afinar=False, temblor=0.0, capa=capa)
        for i in range(n):
            u = (i + 0.5) / n
            x = -40 + (W + 80) * u
            yb = yy + amp * math.sin(x / W * math.pi)
            bal = math.sin(t * 2.2 + i + fila) * 5
            c = cols[(i + fila * 2) % 6]
            lz.relleno(np.array([(x - 28 + bal, yb), (x + 28 + bal, yb), (x + 28 + bal * 1.4, yb + 60), (x + bal * 1.4, yb + 74), (x - 28 + bal * 1.4, yb + 60)]), c, alfa=alfa, capa=capa)
            for q in range(3):
                lz.relleno(circulo(x - 14 + 14 * q + bal * 1.2, yb + 30, 4, 8), (255, 255, 255), alfa=0.65 * alfa, capa=capa)


def cohete(lz, x, y, R, t, t0, color=((255, 206, 72), (255, 120, 90), (120, 220, 255)), n=26, capa=0):
    """Fuego artificial radial que estalla en (x, y) a partir de t0."""
    u = prog(t, t0, t0 + 2.2)
    if u <= 0 or u >= 1:
        return
    c = color[int(h01(int(x), int(y)) * 99) % len(color)]
    for i in range(n):
        a = i * 2 * math.pi / n + 0.2
        r = R * e_out(u) * (0.8 + 0.2 * h01(9, i))
        px = x + math.cos(a) * r
        py = y + math.sin(a) * r + 70 * u * u
        al = (1 - u) ** 1.2
        lz.relleno(circulo(px, py, 9 * (1 - u * 0.5), 10), c, alfa=al, capa=capa)
        lz.relleno(circulo(px, py, 4.5 * (1 - u * 0.5), 8), (255, 255, 255), alfa=al * 0.9, capa=capa)
        lz.relleno(circulo(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8 + 56 * u * u, 5, 8), P.aclarar(c, 0.3), alfa=al * 0.7, capa=capa)
    lz.halo(x, y, R * 1.3 * (1 - u * 0.4), c, alfa=0.45 * (1 - u), dureza=1.2, capa=capa)


def multitud_silueta(lz, y, t, n=36, x0=0, x1=W, esc=1.0, color=(22, 10, 40), capa=0, seed=3, sombreros=0.4):
    """Hilera de siluetas de gente de espaldas (cabeza, hombros, algunos con sombrero y brazos en alto que se mecen)."""
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5 * h01(seed, i, 1)) / n
        s = (30 + 16 * h01(seed, i, 2)) * esc
        yy = y + 10 * math.sin(i * 1.7) * esc
        bob = 3 * math.sin(t * 2.4 + i * 0.9)
        lz.relleno(np.array([(x - 0.9 * s, yy + 2.2 * s), (x + 0.9 * s, yy + 2.2 * s), (x + 0.7 * s, yy + 0.6 * s + bob), (x - 0.7 * s, yy + 0.6 * s + bob)]), color, capa=capa)
        lz.relleno(circulo(x, yy + 0.2 * s + bob, 0.5 * s, 12), color, capa=capa)
        if h01(seed, i, 3) < sombreros:
            lz.relleno(elipse(x, yy - 0.12 * s + bob, 0.95 * s, 0.16 * s, 0, 12), color, capa=capa)
            lz.relleno(np.array([(x - 0.4 * s, yy - 0.1 * s + bob), (x + 0.4 * s, yy - 0.1 * s + bob), (x + 0.3 * s, yy - 0.5 * s + bob), (x - 0.3 * s, yy - 0.5 * s + bob)]), color, capa=capa)
        if h01(seed, i, 4) < 0.18:
            ar = 0.9 * s * (1 + 0.15 * math.sin(t * 5 + i))
            lz.trazo(np.array([(x + 0.7 * s, yy + 0.9 * s + bob), (x + 1.1 * s, yy - 0.5 * s - ar * 0.4 + bob)]), color, 0.35 * s, afinar=False, temblor=0.0, capa=capa)


def iglesia_noche(lz, x, y, s, t, capa=0):
    """Fachada de templo de dos torres en silueta violeta con ventanas y portón encendidos. (x, y) = centro de la base."""
    body, lit = (58, 32, 92), (255, 208, 120)
    lz.halo(x, y - 140 * s, 360 * s, (255, 170, 90), alfa=0.18, dureza=1.0, capa=capa)
    lz.relleno(rect_red(x - 150 * s, y - 220 * s, 300 * s, 220 * s, 0), body, capa=capa)
    for sg in (-1, 1):
        tx = x + sg * 118 * s
        lz.relleno(rect_red(tx - 40 * s, y - 380 * s, 80 * s, 380 * s, 0), body, capa=capa)
        lz.relleno(np.array([(tx - 48 * s, y - 380 * s), (tx + 48 * s, y - 380 * s), (tx, y - 450 * s)]), (74, 40, 108), capa=capa)
        lz.relleno(rect_red(tx - 14 * s, y - 350 * s, 28 * s, 54 * s, 12 * s), lit, alfa=0.95, capa=capa)
        lz.trazo(np.array([(tx, y - 450 * s), (tx, y - 490 * s)]), (230, 210, 240), 5 * s, afinar=False, temblor=0.0, capa=capa)
        lz.trazo(np.array([(tx - 14 * s, y - 472 * s), (tx + 14 * s, y - 472 * s)]), (230, 210, 240), 5 * s, afinar=False, temblor=0.0, capa=capa)
    lz.relleno(np.array([(x - 78 * s, y - 220 * s), (x + 78 * s, y - 220 * s), (x, y - 290 * s)]), (74, 40, 108), capa=capa)
    lz.relleno(rect_red(x - 30 * s, y - 150 * s, 60 * s, 150 * s, 28 * s), lit, alfa=0.95, capa=capa)                    # portón
    for (wx, wy) in ((-84, 150), (84, 150), (-84, 90), (84, 90)):
        parp = 0.85 + 0.15 * math.sin(t * 3 + wx)
        lz.relleno(rect_red(x + (wx - 14) * s, y - wy * s, 28 * s, 44 * s, 12 * s), lit, alfa=parp, capa=capa)


def fiesta_noche(lz, t, t0, cohetes_t):
    """Cielo de fiesta: estrellas, papel picado, el templo iluminado, la gente en silueta y cohetes; abajo, charros al galope (los pone la toma)."""
    for i in range(80):
        x, y = W * h01(51, i, 1), 520 * h01(51, i, 2)
        a = 0.4 + 0.5 * math.sin(t * (0.7 + h01(51, i, 3)) + i)
        lz.relleno(circulo(x, y, 1.3 + 2.0 * h01(51, i, 4), 8), (255, 244, 214), alfa=a * 0.8, capa=0)
    lz.relleno(np.array([(-40, 880), (260, 850), (520, 876), (800, 830), (1200, 870), (1500, 830), (1960, 876), (1960, H + 20), (-40, H + 20)]), (28, 14, 52), capa=0)
    for (x, w, h) in ((110, 100, 90), (330, 120, 70), (560, 90, 100), (1760, 110, 90), (1030, 100, 70)):
        lz.relleno(np.array([(x - w / 2, 876), (x + w / 2, 876), (x + w / 2, 876 - h), (x - w / 2, 876 - h)]), (44, 22, 70), capa=0)
        lz.relleno(rect_red(x - 12, 876 - h * 0.6, 24, 30, 6), (255, 214, 120), alfa=0.9, capa=0)
    lz.halo(960, 1040, 900, (255, 150, 80), alfa=0.30, dureza=0.9, capa=0)
    iglesia_noche(lz, 1330, 880, 1.05, t)
    multitud_silueta(lz, 960, t, n=34, x0=-20, x1=W + 20, esc=1.1, seed=3)
    papel_picado(lz, t, y=130, n=16, capa=1)
    for (x, y, R, tt) in cohetes_t:
        cohete(lz, x, y, R, t, tt)
