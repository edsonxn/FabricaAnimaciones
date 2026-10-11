# -*- coding: utf-8 -*-
"""Hidalgo dibujado a medida para la miniatura (estilo vectorial Kurzgesagt, sin contornos, sombras de 2 tonos).
Coordenadas locales: cabeza centrada en (0, 0), 1 unidad = s px, y hacia abajo. Todo en la capa 1, en orden de dibujo."""
import math

import numpy as np

from motor import catmull, circulo, elipse, rect_red

PIEL = (244, 202, 166)
PIEL_S = (216, 160, 128)
PIEL_L = (255, 226, 192)
RUBOR = (240, 126, 118)
PELO = (244, 242, 250)
PELO_S = (200, 196, 224)
SOTANA = (36, 30, 56)
SOTANA_L = (58, 50, 86)
SOTANA_S = (24, 20, 40)
BORDE_LUZ = (255, 138, 70)
ORO = (255, 196, 54)


class Pincel:
    def __init__(self, lz, cx, cy, s, capa=1):
        self.lz, self.cx, self.cy, self.s, self.capa = lz, cx, cy, s, capa

    def P(self, pts):
        a = np.asarray(pts, float).reshape(-1, 2)
        return np.stack([self.cx + a[:, 0] * self.s, self.cy + a[:, 1] * self.s], 1)

    def poly(self, pts, col, alfa=1.0):
        self.lz.relleno(self.P(pts), col, alfa=alfa, capa=self.capa, temblor=0.0)

    def suave(self, pts, col, alfa=1.0, n=8, cerrado=True):
        self.lz.relleno(catmull(self.P(pts), n, cerrado), col, alfa=alfa, capa=self.capa, temblor=0.0)

    def elip(self, x, y, rx, ry, col, alfa=1.0, rot=0.0):
        self.lz.relleno(elipse(self.cx + x * self.s, self.cy + y * self.s, rx * self.s, ry * self.s, rot), col, alfa=alfa, capa=self.capa, temblor=0.0)

    def disco(self, x, y, r, col, alfa=1.0):
        self.lz.relleno(circulo(self.cx + x * self.s, self.cy + y * self.s, r * self.s), col, alfa=alfa, capa=self.capa, temblor=0.0)

    def rect(self, x, y, w, h, r, col, alfa=1.0):
        self.lz.relleno(rect_red(self.cx + x * self.s, self.cy + y * self.s, w * self.s, h * self.s, r * self.s), col, alfa=alfa, capa=self.capa, temblor=0.0)

    def linea(self, pts, col, ancho, alfa=1.0):
        c = tuple(col[:3]) + (int(255 * alfa),)
        self.lz.trazo(self.P(pts), c, ancho * self.s, temblor=0.0, afinar=False, capa=self.capa)

    def tubo(self, a, b, w, col):
        """Segmento grueso (manga) de a a b con extremos redondos."""
        a, b = np.array(a, float), np.array(b, float)
        d = b - a
        n = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-9) * w / 2
        self.poly([a + n, b + n, b - n, a - n], col)
        self.disco(a[0], a[1], w / 2, col)
        self.disco(b[0], b[1], w / 2, col)


def simetrico(mitad):
    """Mitad derecha (de arriba abajo, con el primer y último punto sobre el eje) -> contorno cerrado."""
    m = [tuple(p) for p in mitad]
    return m + [(-x, y) for x, y in reversed(m[1:-1])]


def estandarte(p, x_asta, y_arriba, y_abajo, t, ancho=2.5, alto=1.5, hacia=-1):
    """Asta con bandera guadalupana que ondea hacia `hacia` (-1 = a la izquierda)."""
    # asta
    p.rect(x_asta - 0.055, y_arriba - 0.1, 0.11, y_abajo - y_arriba + 0.1, 0.05, (116, 72, 46))
    p.rect(x_asta - 0.055, y_arriba - 0.1, 0.035, y_abajo - y_arriba + 0.1, 0.02, (168, 112, 70))
    # moharra dorada
    p.poly([(x_asta, y_arriba - 0.42), (x_asta + 0.11, y_arriba - 0.05), (x_asta - 0.11, y_arriba - 0.05)], ORO)
    p.disco(x_asta, y_arriba - 0.05, 0.1, (214, 140, 30))
    # tela con ondas
    N = 10
    top = y_arriba + 0.06
    azul = ((60, 108, 204), (48, 92, 184))
    for i in range(N):
        u0, u1 = i / N, (i + 1) / N

        def off(u):
            return 0.11 * math.sin(u * 5.2 - t * 3.0) * (0.25 + u)

        x0, x1 = x_asta + hacia * u0 * ancho, x_asta + hacia * u1 * ancho
        p.poly([(x0, top + off(u0)), (x1, top + off(u1)), (x1, top + alto + off(u1)), (x0, top + alto + off(u0))], azul[i % 2])
    # orlas doradas
    for yy in (0.0, alto - 0.07):
        pts = []
        for i in range(N + 1):
            u = i / N
            pts.append((x_asta + hacia * u * ancho, top + yy + 0.11 * math.sin(u * 5.2 - t * 3.0) * (0.25 + u)))
        p.poly(pts + [(x, y + 0.07) for x, y in reversed(pts)], ORO)
    # la Virgen: óvalo dorado, manto rojo, rostro y corona
    u = 0.5
    cxm = x_asta + hacia * u * ancho
    cym = top + alto / 2 + 0.11 * math.sin(u * 5.2 - t * 3.0) * (0.25 + u)
    p.elip(cxm, cym, 0.36, 0.5, ORO)
    p.elip(cxm, cym + 0.03, 0.29, 0.43, (214, 74, 96))
    p.elip(cxm, cym + 0.1, 0.17, 0.3, (84, 168, 168))
    p.disco(cxm, cym - 0.1, 0.1, (244, 206, 176))
    p.poly([(cxm - 0.09, cym - 0.2), (cxm - 0.06, cym - 0.3), (cxm, cym - 0.24), (cxm + 0.06, cym - 0.3), (cxm + 0.09, cym - 0.2)], ORO)


def brazo_con_puno(p, hombro, codo, muneca, asta_x):
    """Brazo derecho flexionado: brazo casi horizontal, antebrazo vertical y puño cerrado agarrando el asta."""
    # sombra del brazo sobre el torso, luego manga de arriba (hombro->codo) y antebrazo (codo->muñeca)
    p.tubo(hombro, codo, 0.92, SOTANA)
    p.tubo(codo, muneca, 0.70, SOTANA)
    p.disco(codo[0], codo[1], 0.46, SOTANA)
    # luz del amanecer en el borde izquierdo del antebrazo y pliegue del codo
    p.poly([(muneca[0] - 0.36, muneca[1]), (muneca[0] - 0.27, muneca[1]), (codo[0] - 0.27, codo[1] + 0.12), (codo[0] - 0.36, codo[1] + 0.12)], BORDE_LUZ, 0.55)
    p.poly([(muneca[0] + 0.12, muneca[1]), (muneca[0] + 0.35, muneca[1]), (codo[0] + 0.35, codo[1] + 0.1), (codo[0] + 0.12, codo[1] + 0.1)], SOTANA_S, 0.55)
    p.linea([(codo[0] - 0.32, codo[1] - 0.08), (codo[0] - 0.05, codo[1] + 0.12), (codo[0] + 0.08, codo[1] + 0.42)], SOTANA_L, 0.04, 0.8)
    # puño de la sotana (vuelta clara)
    p.rect(muneca[0] - 0.40, muneca[1] - 0.14, 0.80, 0.28, 0.1, SOTANA_L)
    p.rect(muneca[0] - 0.40, muneca[1] - 0.14, 0.80, 0.07, 0.04, (88, 78, 120), 0.8)
    # muñeca
    p.rect(muneca[0] - 0.20, muneca[1] - 0.34, 0.40, 0.26, 0.06, PIEL_S)
    # puño: bloque de cuatro dedos que rodean el asta (de abajo hacia arriba) + pulgar cruzado
    fx, fy_ab = muneca[0], muneca[1] - 0.22
    ancho = 0.66
    for k in range(4):
        yy = fy_ab - (k + 1) * 0.165
        p.rect(fx - ancho / 2, yy, ancho, 0.185, 0.085, PIEL_S)
        p.rect(fx - ancho / 2 + 0.01, yy + 0.005, ancho - 0.02, 0.145, 0.07, PIEL)
        p.rect(fx - ancho / 2 + 0.07, yy + 0.02, 0.22, 0.04, 0.02, PIEL_L, 0.85)
    # nudillos
    for k in range(4):
        p.disco(fx + ancho / 2 - 0.06, fy_ab - (k + 1) * 0.165 + 0.08, 0.035, PIEL_S, 0.7)
    # pulgar cruzado sobre el índice (arriba)
    ty = fy_ab - 4 * 0.165 - 0.02
    p.elip(fx - 0.04, ty + 0.03, 0.30, 0.115, PIEL_S, rot=-0.15)
    p.elip(fx - 0.05, ty + 0.015, 0.28, 0.095, PIEL, rot=-0.15)
    p.elip(fx - 0.16, ty + 0.0, 0.10, 0.03, PIEL_L, 0.9, rot=-0.15)
    p.elip(fx + 0.17, ty + 0.0, 0.055, 0.045, (255, 236, 214), 0.8)      # uña


def cuerpo(p, t):
    """Hombros y sotana negra con hilera de botones, alzacuello blanco y filo de luz del amanecer a la izquierda."""
    mitad = [(0.0, 1.50), (0.62, 1.52), (1.25, 1.66), (1.85, 1.92), (2.3, 2.38), (2.52, 3.1), (2.6, 4.0), (2.6, 5.4)]
    forma = simetrico(mitad)
    p.suave(forma[:-1] if False else forma, SOTANA, cerrado=True)
    # lado en sombra (derecha) y pliegues
    p.poly([(0.9, 1.6), (1.85, 1.92), (2.3, 2.38), (2.52, 3.1), (2.6, 4.0), (2.6, 5.4), (1.6, 5.4), (1.5, 3.4), (1.2, 2.2)], SOTANA_S, 0.55)
    for x0, x1, y1 in ((-1.2, -1.45, 5.0), (-0.55, -0.6, 5.0), (1.0, 1.2, 5.0)):
        p.poly([(x0, 2.5), (x0 + 0.08, 2.5), (x1 + 0.1, y1), (x1, y1)], SOTANA_L, 0.55)
    # filo de luz del amanecer sobre el hombro izquierdo
    p.poly([(-0.62, 1.52), (-1.25, 1.66), (-1.85, 1.92), (-2.3, 2.38), (-2.52, 3.1), (-2.6, 4.0), (-2.5, 4.0), (-2.4, 3.1), (-2.18, 2.46), (-1.8, 2.04), (-1.25, 1.78), (-0.62, 1.64)], BORDE_LUZ, 0.7)
    # botonadura
    for k in range(7):
        p.disco(0.0, 2.35 + k * 0.42, 0.045, (104, 94, 142))
    p.poly([(0.0, 2.1), (0.012, 2.1), (0.012, 5.4), (0.0, 5.4)], SOTANA_S, 0.6)


def cabeza(p, t, boca=1.0, mira=(-0.05, -0.01)):
    # --- cuello
    p.poly([(-0.52, 0.75), (0.52, 0.75), (0.62, 1.72), (-0.62, 1.72)], PIEL_S)
    p.poly([(-0.52, 0.75), (0.30, 0.75), (0.40, 1.72), (-0.62, 1.72)], PIEL, 0.55)
    p.suave([(-0.62, 1.2), (0.0, 1.46), (0.62, 1.2), (0.62, 1.8), (-0.62, 1.8)], SOTANA_S, 0.0)
    # alzacuello: banda negra + tira blanca
    p.suave([(-0.74, 1.44), (-0.4, 1.62), (0.0, 1.68), (0.4, 1.62), (0.74, 1.44), (0.7, 1.78), (-0.7, 1.78)], SOTANA_S)
    p.rect(-0.1, 1.40, 0.2, 0.36, 0.035, (252, 250, 246))
    p.rect(-0.1, 1.40, 0.2, 0.06, 0.02, (225, 222, 238))
    # --- cabeza
    cara = simetrico([(0.0, -1.28), (0.55, -1.20), (0.93, -0.84), (1.02, -0.30), (0.96, 0.22), (0.76, 0.74), (0.40, 1.08), (0.0, 1.20)])
    p.suave(cara, PIEL_S)
    p.suave([(x * 0.965 - 0.035, y * 0.97 - 0.015) for x, y in cara], PIEL)
    # brillo en la calva
    p.elip(-0.32, -0.88, 0.42, 0.20, PIEL_L, 0.8, rot=-0.35)
    # sombra bajo la barbilla y mejillas
    p.elip(0.0, 1.14, 0.55, 0.12, PIEL_S, 0.7)
    p.elip(-0.64, 0.40, 0.21, 0.13, RUBOR, 0.55)
    p.elip(0.64, 0.40, 0.21, 0.13, RUBOR, 0.55)
    # arrugas de frente
    for dy, w in ((-0.80, 0.50), (-0.66, 0.40)):
        p.linea([(-w, dy + 0.02), (0.0, dy - 0.04), (w, dy + 0.02)], PIEL_S, 0.035, 0.85)
    # --- orejas
    for sd in (-1, 1):
        p.elip(sd * 1.02, 0.02, 0.15, 0.28, PIEL if sd < 0 else PIEL_S)
        p.elip(sd * 1.03, 0.04, 0.07, 0.17, PIEL_S, 0.7)
    # --- pelo blanco de los lados (cubre parte de las orejas) y flequillo de sienes
    for sd in (-1, 1):
        col = PELO if sd < 0 else PELO_S
        borde = [(0.90, -0.62), (1.18, -0.50), (1.40, -0.18), (1.42, 0.32), (1.26, 0.82), (0.98, 1.00), (0.78, 0.88), (0.90, 0.46), (0.98, 0.02)]
        p.suave([(sd * x, y) for x, y in borde], col)
        p.suave([(sd * (x * 0.96 + (0.02 if sd < 0 else -0.02)), y * 0.98) for x, y in borde[:6]] + [(sd * 1.0, 0.5)], PELO if sd < 0 else (222, 218, 238), 0.9)
        for y0 in (-0.28, 0.12, 0.5):
            p.linea([(sd * 1.0, y0), (sd * 1.22, y0 + 0.14), (sd * 1.30, y0 + 0.34)], PELO_S, 0.03, 0.75)
    # --- cejas gruesas y blancas, inclinadas hacia adentro
    for sd in (-1, 1):
        p.linea([(sd * 0.84, -0.50), (sd * 0.54, -0.68), (sd * 0.15, -0.50)], PELO, 0.16)
        p.linea([(sd * 0.76, -0.55), (sd * 0.54, -0.68), (sd * 0.32, -0.62)], (255, 255, 255), 0.04, 0.8)
    # --- ojos
    for sd in (-1, 1):
        ex, ey = sd * 0.41, -0.20
        p.elip(ex, ey + 0.015, 0.215, 0.215, PIEL_S, 0.55)                     # bolsa bajo el ojo
        p.elip(ex, ey, 0.205, 0.215, (255, 255, 255))
        ix, iy = ex + mira[0], ey + mira[1]
        p.disco(ix, iy, 0.135, (116, 78, 50))
        p.disco(ix, iy, 0.092, (74, 44, 30))
        p.disco(ix, iy, 0.056, (20, 12, 20))
        p.disco(ix - 0.045, iy - 0.05, 0.05, (255, 255, 255))
        p.disco(ix + 0.05, iy + 0.05, 0.022, (255, 255, 255), 0.9)
        # párpado superior
        th = np.linspace(math.pi * 1.06, math.pi * 1.94, 14)
        p.linea([(ex + 0.215 * math.cos(a), ey + 0.222 * math.sin(a)) for a in th], (50, 30, 34), 0.045)
        p.linea([(ex - sd * 0.17, ey + 0.24), (ex - sd * 0.1, ey + 0.27)], PIEL_S, 0.03, 0.8)
    # --- nariz
    p.suave([(0.0, -0.10), (0.15, 0.10), (0.21, 0.32), (0.10, 0.42), (0.0, 0.40), (-0.10, 0.42), (-0.21, 0.32), (-0.15, 0.10)], PIEL_S, 0.95)
    p.suave([(-0.02, -0.06), (0.10, 0.12), (0.13, 0.30), (0.0, 0.36), (-0.14, 0.30), (-0.11, 0.12)], PIEL)
    p.elip(-0.06, 0.18, 0.05, 0.10, PIEL_L, 0.8)
    for sd in (-1, 1):
        p.elip(sd * 0.085, 0.37, 0.04, 0.025, (150, 92, 80), 0.9)
    # --- surcos nasolabiales
    for sd in (-1, 1):
        p.linea([(sd * 0.30, 0.30), (sd * 0.46, 0.55), (sd * 0.44, 0.78)], PIEL_S, 0.04, 0.8)
    # --- boca abierta gritando
    h = 0.50 * boca
    boca_f = [(-0.40, 0.60), (-0.20, 0.56), (0.20, 0.56), (0.40, 0.60), (0.38, 0.60 + 0.34 * boca), (0.24, 0.62 + h), (0.0, 0.66 + h), (-0.24, 0.62 + h), (-0.38, 0.60 + 0.34 * boca)]
    p.suave(boca_f, (104, 22, 40))
    p.poly([(-0.37, 0.605), (-0.19, 0.575), (0.19, 0.575), (0.37, 0.605), (0.34, 0.73), (0.0, 0.76), (-0.34, 0.73)], (255, 255, 255))
    p.poly([(-0.37, 0.605), (-0.19, 0.575), (0.19, 0.575), (0.37, 0.605), (0.36, 0.65), (-0.36, 0.65)], (228, 226, 240), 0.6)
    p.elip(0.0, 0.60 + h * 0.9, 0.20, 0.10 * boca + 0.02, (232, 92, 108))
    p.linea([(-0.42, 0.58), (-0.22, 0.53), (0.0, 0.54), (0.22, 0.53), (0.42, 0.58)], (150, 70, 70), 0.04, 0.9)
    p.linea([(-0.46, 0.60), (-0.51, 0.50)], PIEL_S, 0.035, 0.9)
    p.linea([(0.46, 0.60), (0.51, 0.50)], PIEL_S, 0.035, 0.9)


def hidalgo(lz, cx, cy, s, t=0.3, asta_x=3.05, boca=1.0):
    """Hidalgo en plano medio con el puño en alto agarrando el asta del estandarte."""
    p = Pincel(lz, cx, cy, s)
    estandarte(p, asta_x, -2.95, 1.6, t, ancho=2.3, alto=1.3)
    brazo_con_puno(p, (1.95, 2.40), (3.12, 1.90), (asta_x, 0.95), asta_x)
    cuerpo(p, t)
    cabeza(p, t, boca=boca)
