# -*- coding: utf-8 -*-
"""Épocas 1-3: Homo sapiens (200 000 a.), salida de África (70 000 a.), nace el arte (45 000 a.)."""
import math

import numpy as np

import kit as K
import plano as P
from era import Era
from escena_base import F, pop
from motor import (W, H, blob, campana, catmull, circulo, clamp01, e_back, e_in, e_inout, e_out, elipse, h01, lerp,
                   prog, rect_red, smooth)
from plano import aclarar, mezcla, oscurecer

PI = math.pi
Z = K.poli


# ============================================================ utilidades de dibujo
def acacia(lz, x, y, s, tronco=(70, 40, 76), copa=(64, 36, 88), t=0.0, sw=0.0):
    with lz.grupo(x, y, s):
        lz.relleno(K.capsula(0, 0, -14, -120, 26, 20), tronco)
        lz.relleno(K.capsula(-14, -120, 34, -230, 20, 12), tronco)
        lz.relleno(K.capsula(-8, -140, -70, -215, 12, 8), tronco)
        for dx, dy, rx, ry, c in ((30, -250, 220, 40, copa), (-60, -276, 150, 32, mezcla(copa, (255, 255, 255), 0.06)),
                                  (110, -288, 130, 28, copa)):
            lz.relleno(elipse(dx + sw, dy, rx, ry, 0, 40), c)
        lz.relleno(elipse(30 + sw, -236, 190, 16, 0, 30), oscurecer(copa, 0.3), alfa=0.6)


def lanza(lz):
    """Lanza con punta de piedra (en la mano: eje +y = a lo largo del antebrazo)."""
    lz.relleno(K.capsula(0, -70, 0, 120, 6, 5), (140, 92, 66))
    lz.relleno(Z((0, 118), (-9, 140), (0, 176), (9, 140)), (200, 204, 222))


def llama(lz, x, y, r, t, semilla=0, alfa=1.0):
    """Llama estilizada (origen en la base)."""
    f = 1 + 0.12 * math.sin(t * 17 + semilla) + 0.06 * math.sin(t * 29 + semilla * 2)
    sw = 0.16 * math.sin(t * 11 + semilla)
    lz.halo(x, y - r * 0.9, r * 4.2, (255, 150, 60), alfa=0.32 * alfa, capa=2)
    lz.relleno(Z((x - r * 0.62, y), (x - r * 0.72, y - r * 1.0), (x + r * sw * 2, y - r * 2.6 * f),
                 (x + r * 0.72, y - r * 1.0), (x + r * 0.62, y)), (255, 128, 40), alfa=alfa)
    lz.relleno(elipse(x, y - r * 0.55, r * 0.5, r * 0.85, 0, 24), (255, 198, 70), alfa=alfa)
    lz.relleno(elipse(x, y - r * 0.4, r * 0.24, r * 0.5, 0, 20), (255, 246, 190), alfa=alfa)


def mano_estarcida(lz, x, y, s, col, roca, rot=0.0, semilla=0, u=1.0):
    """Mano en negativo: mancha de pigmento con la mano (color de roca) en el centro. u = 0..1 aparición."""
    if u <= 0.01:
        return
    with lz.grupo(x, y, s * (0.7 + 0.3 * e_back(u)), rot):
        lz.relleno(blob(0, 20, 120, semilla, 0.16, 56, 6), col, alfa=min(1.0, u * 1.4))
        lz.relleno(blob(0, 20, 84, semilla + 3, 0.14, 40, 5), oscurecer(col, 0.25), alfa=min(0.5, u))
        for xx, l in ((-32, 60), (-11, 74), (10, 68), (31, 52)):
            lz.relleno(K.capsula(xx, -8, xx * 1.15, -8 - l, 20, 19), roca)
        lz.relleno(rect_red(-42, -14, 84, 92, 32), roca)
        lz.relleno(K.capsula(-38, 34, -84, -6, 22, 20), roca)


def bisonte(lz, x, y, s, col=(196, 92, 60), osc=(132, 54, 52), t=0.0):
    """Bisonte rupestre (perfil, mirando a la izquierda). Origen: centro del cuerpo."""
    with lz.grupo(x, y, s):
        for lx, ly, sh in ((-140, 70, 0.30), (-70, 78, 0.12), (110, 74, 0.30), (176, 66, 0.12)):     # patas gruesas
            lz.relleno(K.capsula(lx, ly - 30, lx + 8, ly + 130, 52, 34), oscurecer(col, sh))
            lz.relleno(elipse(lx + 10, ly + 134, 30, 13, 0, 16), osc)
        lz.relleno(elipse(30, 6, 250, 122, 0, 48), col)                          # cuerpo
        lz.relleno(elipse(60, 50, 210, 64, 0, 36), osc, alfa=0.5)                # vientre en sombra
        lz.relleno(circulo(-118, -46, 128, 40), col)                              # joroba
        lz.relleno(Z((-250, -70), (-150, -170), (-30, -120), (-40, 40), (-230, 90)), osc, alfa=0.8)   # crin
        lz.relleno(elipse(-286, 66, 84, 74, 0.3, 30), osc)                       # cabeza baja
        lz.relleno(Z((-330, 100), (-360, 200), (-290, 150)), oscurecer(osc, 0.3))  # barba
        lz.relleno(K.capsula(-262, 2, -226, -70, 18, 9), (238, 214, 172))         # cuerno
        lz.relleno(K.capsula(268, -20, 316, 104, 14, 9), osc)                     # cola
        lz.relleno(circulo(-300, 44, 6, 10), (250, 236, 210))                     # ojo


# ============================================================ 1. sapiens
class Sapiens(Era):
    COL_SALIDA = (255, 214, 130)

    def sol_y(self, t):
        return lerp(1040, 770, e_out(prog(t, 0.0, 2.4)))

    def salida(self, t):
        return (W / 2, self.sol_y(t))

    def fondo(self, t):
        return K.degradado_img((48, 24, 100), (255, 200, 120), mid=(226, 92, 112), ym=0.5)

    def cam(self, t):
        u = prog(t, 0.0, self.T1)
        return 1.0 + 0.10 * (1 - e_out(u)), 0.0, 0.0, 30 * (1 - u)

    def dibujar(self, lz, t):
        sy = self.sol_y(t)
        P.sol(lz, W / 2, sy, 205, t, brillo=1.0)
        v = 385.0                                              # velocidad del suelo cercano (px/s)
        K.colinas(lz, 1040, (140, 66, 124), 50, 0.0042, 3, dx=t * v * 0.06)
        K.colinas(lz, 1110, (104, 50, 118), 46, 0.0036, 8, dx=t * v * 0.16)
        for i in range(4):                                      # acacias medias
            x = ((300 * i + 120 - t * v * 0.3) % (W + 500)) - 250
            acacia(lz, x, 1160, 0.7 + 0.12 * (i % 2), t=t, sw=4 * math.sin(t + i))
        K.colinas(lz, 1230, (72, 38, 96), 22, 0.006, 12, dx=t * v * 0.5)
        lz.relleno(K.curva(lambda x: 1290 + 8 * math.sin((x + t * v) * 0.01)), (56, 30, 80))
        K.hierba(lz, -60, W + 60, 1300, t, (96, 52, 104), 22, 52, 5, dx=-(t * v) % 90)
        # aves cruzando el sol
        for i in range(7):
            bx = 1250 - ((t * 250 + i * 70) % 1700)
            K.pajaro_v(lz, bx, 520 + 60 * math.sin(i * 1.9) + 22 * math.sin(t * 3 + i), 1.0 - 0.06 * (i % 3), t, (58, 30, 88), i)
        # --- sapiens caminando (de izquierda a derecha, el mundo se desliza)
        pt = campana(t, 1.3, 2.9)
        y0 = 1385
        A1 = K.brazos_marcha(t * 6.5, 1.0)
        pt_u = smooth(pt)
        b1 = K.mezcla_brazos((0.45, 2.15, A1[2], A1[3]), (0.45, 2.15, 2.55, 0.15), pt_u)
        K.persona(lz, 300, y0, 1.9, t, ph=t * 6.5, paso=1.0, mirar=1, piel=K.PIEL[2], pelo=(30, 22, 30), pelo_t="corto",
                  ropa=(206, 140, 92), falda=0.5, cinto=(120, 78, 62), brazos=b1, boca=0.8 * pt_u, obj_i=lanza)
        K.persona(lz, 590, y0 + 8, 1.82, t, ph=t * 6.5 + 1.4, paso=1.0, mirar=1, piel=K.PIEL[3], pelo=(24, 18, 26),
                  pelo_t="largo", ropa=(236, 176, 104), falda=0.6, cinto=(140, 90, 62))
        sal = 0.24 * abs(math.sin(t * 5.5)) * 90 * campana(t, 1.5, 3.4)
        K.persona(lz, 820, y0 + 10, 1.3, t, ph=t * 9.5 + 0.6, paso=1.0, mirar=1, piel=K.PIEL[2], pelo=(28, 20, 28), pelo_t="rizos",
                  ropa=(150, 206, 130), falda=0.3, cinto=(110, 84, 66), salto=sal, boca=0.5 * (sal > 4))
        K.hierba(lz, -60, W + 60, 1500, t, (70, 36, 92), 18, 70, 9, dx=-(t * v * 1.4) % 110)
        lz.relleno(K.curva(lambda x: 1525 + 10 * math.sin((x + t * v * 1.4) * 0.008)), (44, 24, 68))
        K.particulas(lz, t, 26, 0, W, 500, 1500, vel=(-60, -22), r=(1.5, 3.2), col=(255, 214, 150), alfa=0.6, semilla=4)

    def sfx(self, ev):
        ev(0.05, "amanecer", 0.55, 0.0, dur=2.6)
        for i in range(8):
            ev(0.4 + i * 0.4688, "pasos", 0.22, -0.2 + 0.05 * i, dur=0.4)
        ev(self.a(1.7), "pop", 0.4, 0.2, tono=1.3)
        ev(self.a(2.3), "boing", 0.25, 0.4, tono=1.1)


# ============================================================ 2. salida de África
RUTAS = [
    # (waypoints lon/lat, t inicio pulso, t fin pulso)
    ([(38, 8), (44, 14), (48, 22), (56, 26), (66, 25), (76, 18), (88, 21), (98, 14), (105, 4), (113, -5), (124, -11),
      (133, -18), (135, -25)], 0.4, 6.4),
    ([(38, 8), (44, 14), (48, 22), (52, 30), (44, 38), (34, 40), (26, 42), (18, 45), (10, 47), (2, 49)], 1.2, 5.8),
    ([(38, 8), (44, 14), (48, 22), (58, 28), (70, 30), (84, 30), (96, 33), (108, 35), (118, 38), (128, 42), (138, 45)],
     2.0, 6.9),
]
PILLS = [("ÁFRICA", (26, 6), 0.3), ("EUROPA", (12, 50), 5.2), ("ASIA", (100, 36), 5.8), ("AUSTRALIA", (134, -26), 6.2)]


class Africa(Era):
    COL_SALIDA = (120, 210, 255)
    GX, GY, GR = W / 2, 880.0, 450.0

    def preparar(self):
        self.rutas = [(catmull(np.array(w, float), 10), a, b) for w, a, b in RUTAS]

    def lon(self, t):
        return 22 + 100 * smooth(prog(t, self.a(0), self.a(7.6)))

    def proj(self, lonlat, t):
        Q, Zq = P._proy(np.array(lonlat, float), -math.radians(self.lon(t)), -0.35)
        return Q * self.GR + [self.GX, self.GY], Zq

    def salida(self, t):
        p, zz = self.proj([[120.0, -2.0]], t)
        return (float(p[0][0]), float(p[0][1]))

    def fondo(self, t):
        bg = K.degradado_img((6, 8, 32), (30, 18, 72)).copy()
        return F.estrellas(bg, t, 1.0)

    def cam(self, t):
        return 1.0 + 0.05 * prog(t, self.T0, self.T1), 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        gx, gy, r = self.GX, self.GY, self.GR
        # órbita punteada que gira
        P.discontinua(lz, P.arco_pts(gx, gy, r + 70, 0, 2 * PI - 0.001, 200), (120, 130, 220), 3.0, 14, 22, fase=t * 30)
        P.tierra(lz, gx, gy, r, t, rot=-math.radians(self.lon(t)), ang_luz=PI * 1.3, luz=1.0, nubes=0.7)
        with lz.recorte(circulo(gx, gy, r, 160)):
            for pts, ta, tb in self.rutas:
                f = e_inout(prog(t, self.a(ta), self.a(tb)))
                n = max(2, int(len(pts) * f))
                if f <= 0.001:
                    continue
                seg = pts[:n].copy()
                if n < len(pts):
                    frac = f * len(pts) - n
                    seg = np.vstack([seg, seg[-1] + (pts[n] - seg[-1]) * frac])
                Q, zz = self.proj(seg, t)
                vis = zz > 0.05
                i = 0
                while i < len(vis):
                    if vis[i]:
                        j = i
                        while j < len(vis) and vis[j]:
                            j += 1
                        if j - i > 1:
                            lz.trazo(Q[i:j], (255, 214, 90, 90), 24, afinar=False, paso=6.0)
                            lz.trazo(Q[i:j], (255, 226, 120), 9, afinar=False, paso=6.0)
                        i = j
                    else:
                        i += 1
        for pts, ta, tb in self.rutas:                     # cabezas de ruta: persona (punto luminoso)
            f = e_inout(prog(t, self.a(ta), self.a(tb)))
            if f <= 0.001:
                continue
            k = min(len(pts) - 1, int(len(pts) * f))
            q, zz = self.proj([pts[k]], t)
            if zz[0] > 0.1:
                lz.halo(float(q[0][0]), float(q[0][1]), 46, (255, 230, 140), alfa=0.9, capa=2)
                lz.relleno(circulo(float(q[0][0]), float(q[0][1]), 12, 18), (255, 255, 255), capa=2)
        for txt, ll, ta in PILLS:
            k = e_back(prog(t, self.a(ta), self.a(ta) + 0.35))
            q, zz = self.proj([ll], t)
            if k > 0.02 and zz[0] > 0.3:
                P.pastilla(lz, float(q[0][0]), float(q[0][1]) - 56, txt, 34, k=k * min(1.0, (zz[0] - 0.3) * 4))
        K.particulas(lz, t, 16, 0, W, 300, 1500, vel=(0, 0), r=(1.5, 3), col=(200, 210, 255), alfa=0.5, semilla=7, vaiven=30)

    def sfx(self, ev):
        ev(self.a(-1.4), "zoom_whoosh", 0.4, 0.0)
        ev(self.a(0.4), "pop", 0.4, -0.3, tono=0.8)
        for i, (_, _, ta) in enumerate(PILLS):
            ev(self.a(ta), "pop", 0.35, -0.4 + 0.27 * i, tono=1.0 + 0.12 * i)
        ev(self.a(1.0), "espiral_zap", 0.18, 0.0, dur=3.2)


# ============================================================ 3. arte
class Arte(Era):
    COL_SALIDA = (255, 170, 80)
    ANTORCHA = (900.0, 640.0)

    def preparar(self):
        self.reveal = (self.a(-1.6), self.a(5.5))
        self.manos = [(120, 770, 0.95, 1.6, 0.2), (200, 950, 0.8, 2.2, -0.25), (330, 640, 0.7, 2.8, 0.1)]

    def salida(self, t):
        return (self.ANTORCHA[0], self.ANTORCHA[1] - 30)

    def fondo(self, t):
        return K.degradado_img((30, 18, 44), (78, 44, 68), mid=(58, 32, 60), ym=0.5)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.06 * u, 0.012 * math.sin(t * 0.8), -18 * u, 0

    def pared(self, lz, t):
        wall = (112, 66, 76)
        lz.relleno(K.curva(lambda x: 470 + 40 * math.sin(x * 0.008) + 20 * math.sin(x * 0.021), x0=-60, x1=W + 60,
                           paso=24, base=1420), wall)
        for i in range(7):                                   # relieve de la roca
            b = blob(150 + 150 * i, 560 + 160 * ((i * 5) % 6), 170, i, 0.22, 40, 5)
            lz.relleno(b, aclarar(wall, 0.05) if i % 2 else oscurecer(wall, 0.2), alfa=0.32)
        for i in range(9):                                   # estalactitas
            x = -20 + i * 128 + 30 * h01(i, 3)
            lz.relleno(Z((x - 34, 380), (x + 34, 380), (x + 4, 480 + 90 * h01(i, 5))), oscurecer(wall, 0.45))
        lz.relleno(K.curva(lambda x: 1360 + 8 * math.sin(x * 0.02), base=H + 40, x0=-60, x1=W + 60), (58, 32, 58))
        lz.relleno(K.curva(lambda x: 1420 + 8 * math.sin(x * 0.03), base=H + 40, x0=-60, x1=W + 60), (44, 24, 50))

    def dibujar(self, lz, t):
        self.pared(lz, t)
        roca = (112, 66, 76)
        ocre = (204, 98, 62)
        # manos estarcidas (con soplo de pigmento)
        for i, (x, y, s, tb, rot) in enumerate(self.manos):
            ua = prog(t, self.a(tb), self.a(tb) + 0.5)
            mano_estarcida(lz, x, y, s, ocre, roca, rot, i * 5, ua)
            if 0 < ua < 1.0:
                for j in range(14):
                    ang = j * 0.9 + i
                    rr = 30 + 220 * e_out(ua) * (0.5 + 0.5 * h01(i, j))
                    lz.puntos(np.array([[x + rr * math.cos(ang), y + 20 + rr * math.sin(ang) * 0.8]]), 5 * (1 - ua) + 1, ocre, capa=2)
        # bisonte que se pinta de derecha a izquierda, siguiendo al pintor
        p = prog(t, *self.reveal)
        xr = 930 - e_inout(p) * 640
        with lz.recorte(Z((xr, 500), (1100, 500), (1100, 1200), (xr + 40, 1200), (xr - 20, 900))):
            bisonte(lz, 600, 880, 1.0, ocre, (140, 56, 54), t)
        # pintor (camina despacio hacia la izquierda mientras pinta)
        px = xr + 138
        ang = self.a(0)
        if p < 1.0:
            objetivo = (xr + 8, 880 + 70 * math.sin(t * 8.5))
            pintando = 1.0
        else:
            objetivo = (xr + 8, 880)
            pintando = 0.0
        y0 = 1400
        s = 1.7
        a1, a2 = K.ik(px, y0, s, -1, objetivo)
        kk = smooth(prog(t, self.a(-0.8), self.a(0.6)))
        base = K.brazos_marcha(t * 4, 0.35)
        brazos = K.mezcla_brazos((base[0], base[1], 0.3, 0.3), (base[0], base[1], a1, a2), kk)

        def pincel(lzz):
            lzz.relleno(K.capsula(0, -4, 0, 44, 8, 6), (150, 100, 70))
            lzz.relleno(K.capsula(0, 40, 0, 62, 13, 10), (150, 40, 44))
        K.persona(lz, px, y0, s, t, ph=t * 3.4, paso=0.35 * (p < 1.0), mirar=-1, piel=K.PIEL[2], pelo=(28, 20, 28), pelo_t="corto",
                  barba=True, ropa=(182, 122, 82), falda=0.4, cinto=(96, 64, 56), brazos=brazos, obj_d=pincel, boca=0.0)
        # niño mirando las manos (esquina inferior izquierda)
        ka = K.brazos_marcha(0, 0)
        K.persona(lz, 250, 1440, 1.25, t, ph=0, paso=0.0, mirar=1, piel=K.PIEL[2], pelo=(28, 20, 28), pelo_t="rizos",
                  ropa=(150, 190, 132), falda=0.3, cinto=(90, 70, 60),
                  brazos=(0.2, 0.2, 2.6 + 0.15 * math.sin(t * 3), 0.1), boca=0.3)
        # antorcha en la pared + luz cálida
        ax, ay = self.ANTORCHA
        lz.relleno(K.capsula(ax, ay + 10, ax + 6, ay + 130, 18, 14), (110, 70, 56))
        lz.relleno(rect_red(ax - 26, ay + 6, 52, 22, 8), (70, 50, 60))
        llama(lz, ax, ay + 8, 34, t, 3)
        lz.halo(ax, ay, 720, (255, 160, 70), alfa=0.30, capa=2)
        lz.halo(ax, ay, 300, (255, 190, 100), alfa=0.30, capa=2)
        K.particulas(lz, t, 18, ax - 120, ax + 120, ay - 300, ay + 20, vel=(0, -60), r=(1.5, 3), col=(255, 200, 110), alfa=0.9,
                     semilla=3, vaiven=14)
        K.particulas(lz, t, 30, 0, W, 450, 1350, vel=(0, 0), r=(1.2, 2.5), col=(255, 220, 190), alfa=0.35, semilla=5, vaiven=18)

    def sfx(self, ev):
        ev(self.a(-1.4), "whoosh", 0.3, 0.0)
        ev(self.a(-0.6), "fuego", 0.35, 0.6, dur=6.0)
        for tb, i in ((1.6, 0), (2.2, 1), (2.8, 2)):
            ev(self.a(tb), "spray", 0.5, -0.5 + 0.2 * i, dur=0.7)
        ev(self.a(-1.0), "pincel", 0.5, 0.1, dur=5.6)
        ev(self.a(5.7), "revelar", 0.45, 0.0)
