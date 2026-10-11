# -*- coding: utf-8 -*-
"""5. LA COSA: el refri revienta (cubitos, escarcha) y sale un monstruo gordo y peludo, ¡hambriento! Agarra la tarta, un crujido en el techo,
ve al gato colgado; éste se cae, los dos GRITAN a coro, la tarta sale volando y cae en la bocaza del monstruo: silencio, mastica feliz. El
monstruo tenía tanto miedo como él (y solo quería tarta). Eructo, tripas, el gato se atreve y va por el pescado. Barrido a la derecha."""
import math

import numpy as np

from basec import Base
from motor import H, W, clamp01, e_out, prog, ruido1, smooth
import mundos_cocina as MC
import props as PR
import props2 as P2
import toon as TN
from toon import Pista, elipse_, muelle, pulso, tiembla
from toon_cosa import AnimCosa, Cosa
from toon_gato import AnimGato, Gato, pasos

MX, MY, MS = 470.0, 1690.0, 1.1
S = 1.35
V = 205.0
ZANC = 40.0
D_CICLO = 4 * ZANC * S
X_CAT = 900.0
U_CRACK = 2.9
U_CAE = 4.5
U_ATERRIZA = 4.82
U_GRITO = 4.95
U_CHOMP = 5.95
U_ERUCTO = 7.4
SEG_CAMINA = (8.5, 10.2)
U_PESCADO = 10.3


def _dist(u):
    a, b = SEG_CAMINA
    dt = 0.002
    us = np.arange(a, min(u, b + 0.3), dt)
    if len(us) == 0:
        return 0.0
    v = np.clip((us - a) / 0.2, 0, 1) * np.clip((b + 0.2 - us) / 0.2, 0, 1)
    return float(np.sum(v) * dt * V)


def x_gato(u):
    if u < U_CAE + 0.35:
        return X_CAT
    return X_CAT - _dist(u)


def fase(u):
    return _dist(u) / D_CICLO


def y_gato(u):
    if u < U_CAE:
        return 1175.0 + 3 * math.sin(2 * math.pi * 0.9 * u)
    if u < U_ATERRIZA:
        k = (u - U_CAE) / (U_ATERRIZA - U_CAE)
        return 1175.0 + (MY - 1175.0) * k * k
    return MY + (pasos(fase(u), ZANC, 34, -1)["bob"] * S * 0.8 if SEG_CAMINA[0] < u < SEG_CAMINA[1] + 0.3 else 0.0)


class Cosa5(Base):
    BLOOM = 0.08

    def sonidos(self):
        e = self.ev
        t0 = self.t0
        e(t0, "zumbido_refri", 0.35, dur=12.4)
        e(t0 + 0.05, "estallido", 1.0)
        e(t0 + 0.1, "hielo", 0.8)
        e(t0 + 0.3, "rugido_bajo", 0.9, dur=1.0)
        e(t0 + 0.85, "impacto", 0.9)
        e(t0 + 1.1, "tripas", 0.8)
        e(t0 + 1.6, "gruni_hambre", 0.6)
        e(t0 + 2.3, "baba", 0.5)
        e(t0 + U_CRACK, "crujido", 0.9, pan=0.4)
        e(t0 + U_CRACK + 0.05, "tink", 0.5)
        e(t0 + 3.2, "susto_cuerdas", 0.5)
        e(t0 + U_CAE, "garras_techo", 0.8)
        e(t0 + U_CAE + 0.05, "whoosh", 0.5, dur=0.3, tono=0.6)
        e(t0 + U_ATERRIZA, "impacto", 0.8)
        e(t0 + U_GRITO, "grito_gato", 0.9, dur=1.0)
        e(t0 + U_GRITO, "grito_cosa", 1.0, dur=1.0)
        e(t0 + U_CHOMP, "chomp", 1.0)
        e(t0 + U_CHOMP + 0.2, "trago", 0.9)
        for k in range(6):
            e(t0 + 6.15 + 0.38 * k, "mastica", 0.6, tono=1.0 + 0.04 * (k % 2))
        e(t0 + U_ERUCTO, "eructo", 1.0)
        e(t0 + 7.9, "tripas", 1.0)
        for k in range(5):
            e(t0 + SEG_CAMINA[0] + 0.3 + 0.6 * k, "paso_suave", 0.35, pan=-0.2)
            e(t0 + SEG_CAMINA[0] + 0.32 + 0.6 * k, "cascabel", 0.3, tono=1.0 + 0.05 * k)
        e(t0 + U_PESCADO, "plop", 0.7)
        e(t0 + 11.4, "whoosh", 0.8, dur=0.8)

    def preparar(self):
        super().preparar()
        self.g = Gato(sem=11)
        self.c = Cosa(sem=21)
        tgt_pie = ((MC.POS_TARTA[0] - MX) / MS, (MC.POS_TARTA[1] - 40 - MY) / MS)
        self._tgt_pie = tgt_pie

        def barriga(u):
            return 0.9 * pulso(u, 1.1, 0.5) + 0.7 * pulso(u, 1.9, 0.4) + 1.0 * pulso(u, 7.8, 0.6) + 0.8 * pulso(u, 8.5, 0.4)

        def boca(u):
            if 6.12 < u < 7.35:
                return 0.04 + 0.26 * (0.5 + 0.5 * math.sin(2 * math.pi * 2.6 * (u - 6.12) - math.pi / 2))
            return None

        def cuerpo_sq(u):
            v = muelle(u, [(0.9, 0.2), (U_ATERRIZA, 0.1), (U_GRITO, 0.0)], 3.0, 0.2)
            if 0.25 < u < 0.82:
                v += -0.3 * smooth((u - 0.25) / 0.57)
            if 0.82 <= u < 0.9:
                v += -0.3 + 0.6 * smooth((u - 0.82) / 0.08)
            return v

        self.AC = AnimCosa(
            s=[(0, 0.30), (0.25, 0.30), (1.0, MS, "M")],
            x=[(0, 310), (0.25, 310), (1.0, MX, "o")],
            y=[(0, 1330), (0.25, 1330), (0.85, MY, "i")],
            sq=cuerpo_sq,
            cara=[(0, "sorpresa"), (1.1, "sorpresa"), (1.5, "hambre", "io"), (2.9, "hambre"), (3.1, "sorpresa", "o"), (3.5, "miedo", "io"),
                  (4.9, "miedo"), (4.97, "grito", "o"), (5.9, "grito"), (5.98, "neutro", "o"), (6.1, "feliz", "io"), (7.3, "feliz"), (7.4, "sorpresa", "o"),
                  (7.9, "neutro", "io"), (8.3, "hambre", "io"), (10.4, "feliz", "io")],
            boca=boca,
            mira_x=[(0, 0), (1.3, 0), (1.5, -0.9, "o"), (2.8, -0.9), (3.05, 0.8, "o"), (4.9, 0.8), (6.0, 0.0), (7.6, -0.8, "io"), (8.3, 0.9, "io"), (10.0, 0.9)],
            mira_y=[(0, 0), (1.3, 0.2), (3.05, -0.8, "o"), (4.6, 0.3, "io"), (6.0, 0.0)],
            suelto=[(0, 0), (0.9, 0), (1.0, 1.0), (1.4, 0.0), (7.6, 0), (7.7, 1.0), (8.2, 0)],
            abre=lambda u: (0.15, 0.15, 0.15) if 6.1 < u < 7.3 else (1.0, 1.0, 1.0),
            mano_i=[(0, (-300, -190)), (1.5, (-300, -190)), (2.2, self._tgt_pie, "o"), (2.35, self._tgt_pie), (2.9, (-120, -330), "io"), (4.9, (-120, -330)),
                    (5.05, (-200, -800), "o"), (5.7, (-300, -190), "io"), (8.0, (-300, -190)), (8.5, (-380, -540), "io"), (9.8, (-380, -540)), (10.3, (-300, -190), "io")],
            mano_d=[(0, (300, -190)), (3.4, (300, -190)), (3.9, (170, -520), "io"), (5.8, (170, -520)), (6.1, (240, -360), "io"), (7.3, (250, -350)),
                    (7.45, (60, -300), "o"), (7.9, (300, -190), "io")],
            curva_i=[(0, 40)], curva_d=[(0, -40)],
            sudor=[(0, 0), (3.2, 0), (3.6, 0.8), (6.0, 0.2), (6.3, 0)],
            erizo=[(0, 0), (U_GRITO - 0.02, 0), (U_GRITO + 0.1, 0.8, "o"), (6.0, 0.0, "io")],
            tiembla=[(0, 0), (3.4, 0), (3.5, 2.5), (4.9, 2.5), (U_GRITO, 6), (5.9, 6), (5.98, 0)],
            barriga=barriga,
            gelatina=[(0, 1.0), (U_GRITO, 1.0), (U_GRITO + 0.1, 1.8), (5.9, 1.8), (6.2, 1.0)],
            sesgo=lambda u: 0.0,
        )
        self.AG = AnimGato(
            x=x_gato, y=y_gato, s=[(0, S)],
            giro=[(0, -0.35), (U_CAE, -0.35), (U_ATERRIZA, -0.85, "o")],
            cara=[(0, "terror"), (U_CAE - 0.15, "terror"), (U_CAE + 0.1, "grito", "o"), (U_ATERRIZA + 0.05, "terror", "io"), (U_GRITO, "grito", "o"),
                  (5.9, "grito"), (6.0, "tragar", "io"), (6.4, "sospecha", "io"), (7.3, "sorpresa", "io"), (7.4, "susto", "o"), (7.9, "preocupado", "io"),
                  (8.4, "sospecha", "io"), (10.2, "alerta", "io"), (10.5, "alivio", "io")],
            mira_x=[(0, 0), (U_CAE, 0), (U_ATERRIZA, -0.7), (8.3, -0.7), (8.6, -0.9), (10.5, 0.4)],
            cab_rot=[(0, 0.0), (U_CAE, 0.0), (U_CAE + 0.2, 0.2, "o"), (U_ATERRIZA, -0.1), (6.0, 0.0)],
            rot=lambda u: (0.12 * math.sin(2 * math.pi * 3 * u) if 4.2 < u < U_CAE else 0.0) + (0.5 * (1 - prog(u, U_CAE + 0.0, U_ATERRIZA)) * math.sin(math.pi * prog(u, U_CAE, U_ATERRIZA)) * 0 if True else 0)
            + (0.20 * smooth(prog(u, U_ERUCTO, U_ERUCTO + 0.12)) * (1 - smooth(prog(u, U_ERUCTO + 0.12, U_ERUCTO + 0.7)))),
            sq=[(0, 0.0), (U_ATERRIZA - 0.02, 0.0), (U_ATERRIZA, 0.34, "o"), (U_ATERRIZA + 0.25, -0.08, "m"), (U_ATERRIZA + 0.7, 0.0)],
            mano_i=lambda u: self._mano_i_gato(u),
            mano_d=[(0, (96, -742)), (4.45, (96, -742)), (4.7, (112, -214), "o"), (U_CAE + 0.1, (50, -520), "o"), (U_ATERRIZA, (120, -300), "o"), (6.0, (112, -214), "io")],
            curva_i=[(0, 22)], curva_d=[(0, -22)],
            pie_i=lambda u: pasos(fase(u), ZANC, 34, -1)["pie_i"] if u > U_ATERRIZA + 0.9 else ((-52.0 + 24 * math.sin(2 * math.pi * 5 * u), -30 * (0.5 + 0.5 * math.sin(2 * math.pi * 5 * u))) if U_CAE < u < U_ATERRIZA else (-52.0, 0.0)),
            pie_d=lambda u: pasos(fase(u), ZANC, 34, -1)["pie_d"] if u > U_ATERRIZA + 0.9 else ((52.0 - 24 * math.sin(2 * math.pi * 5 * u), -30 * (0.5 - 0.5 * math.sin(2 * math.pi * 5 * u))) if U_CAE < u < U_ATERRIZA else (52.0, 0.0)),
            rodilla_i=lambda u: pasos(fase(u), ZANC, 34, -1)["rodilla_i"] if u > U_ATERRIZA + 0.9 else -26.0,
            rodilla_d=lambda u: pasos(fase(u), ZANC, 34, -1)["rodilla_d"] if u > U_ATERRIZA + 0.9 else 26.0,
            erizo=[(0, 1.0), (U_ATERRIZA, 1.0), (6.2, 0.1, "io"), (7.4, 0.0), (U_ERUCTO + 0.05, 0.8, "o"), (7.9, 0.0, "io")],
            tiembla=[(0, 5.5), (U_CAE - 0.02, 5.5), (U_CAE, 0), (U_ATERRIZA, 0), (U_GRITO, 6.0), (5.9, 6.0), (6.2, 1.0), (7.3, 0)],
            sudor=[(0, 1.0), (6.0, 1.0), (6.8, 0.0)],
            cola_hincha=[(0, 1.0), (6.0, 0.8), (7.4, 0.0), (U_ERUCTO + 0.05, 0.9), (8.0, 0.0)],
            rayas_miedo=[(0, 0), (U_GRITO, 0), (U_GRITO + 0.1, 1.0), (5.9, 1.0), (6.1, 0)],
            linterna=lambda u: None,
            golpes=[(U_ATERRIZA, 0.1)],
        )

    def _mano_i_gato(self, u):
        if u < 4.45:
            return np.array([-96.0, -742.0])
        if u < 4.62:
            return np.array([-96.0, -742.0]) + (np.array([-130.0, -500.0]) - np.array([-96.0, -742.0])) * smooth(prog(u, 4.45, 4.62))
        if u < U_ATERRIZA:
            return np.array([-70.0, -520.0])
        d0 = np.array([-70.0, -300.0])
        if u < 8.5:
            return d0 + (np.array([-92.0, -186.0]) - d0) * smooth(prog(u, 6.0, 6.5))
        # va por el pescado y lo agarra con la mano de la izquierda de la pantalla
        pe = np.array([(MC.POS_PESCADO[0] - x_gato(u)) / S, (MC.POS_PESCADO[1] - 50 - MY) / S])
        if u < U_PESCADO:
            return np.array([-92.0, -186.0]) + (pe - np.array([-92.0, -186.0])) * smooth(prog(u, 9.7, 10.2))
        return pe + (np.array([-60.0, -230.0]) - pe) * smooth(prog(u, U_PESCADO, U_PESCADO + 0.5))

    # ------------------------------------------------------------------ cámara
    def cam(self, u):
        if not hasattr(self, "_z"):
            self._z = Pista([(0, 1.0), (0.9, 0.95, "io"), (2.8, 0.95), (3.2, 1.2, "io"), (4.3, 1.2), (4.5, 0.92, "o"), (U_GRITO, 1.1, "o"), (5.9, 1.1),
                             (6.3, 0.95, "io"), (7.3, 0.95), (7.5, 0.9, "o"), (9.2, 0.9), (10.4, 1.05, "io"), (11.0, 1.05), (11.4, 1.0)])
            self._cx = Pista([(0, 520), (0.9, 600, "io"), (2.8, 600), (3.2, 540, "io"), (4.3, 600), (4.5, 660, "o"), (U_GRITO, 640), (6.3, 660, "io"),
                              (8.3, 680), (10.0, 560, "io"), (11.0, 600), (11.4, 700, "i"), (12.5, 1500, "i")])
            self._cy = Pista([(0, 1020), (0.9, 1000, "io"), (2.8, 1010), (3.2, 1120, "io"), (4.3, 1100), (4.5, 1000, "o"), (6.3, 1020), (12.5, 1020)])
        z, cx, cy = float(self._z(u)), float(self._cx(u)), float(self._cy(u))
        if 0.0 < u < 0.6:
            dx, dy = tiembla(u, 14 * (1 - u / 0.6), sem=2)
            cx, cy = cx + dx, cy + dy
        if U_ATERRIZA <= u < U_ATERRIZA + 0.4:
            dx, dy = tiembla(u, 18 * math.exp(-8 * (u - U_ATERRIZA)), sem=3)
            cx, cy = cx + dx, cy + dy
        if U_GRITO <= u < U_CHOMP:
            dx, dy = tiembla(u, 9, sem=4)
            cx, cy = cx + dx, cy + dy
        return z, cx, cy, 0.0

    # ------------------------------------------------------------------ dibujo
    def dibujar(self, h, t, u):
        z, cx, cy, rot = self.cam(u)
        h.camara(z, cx, cy, rot)
        for rgba, ox, oy, prof in MC.cocina():
            h.pegar_capa(rgba, ox, oy, prof)
        # lámpara que sigue balanceándose (viene del golpe de la escena anterior)
        q = u + 12.5 - 9.64
        ang = 0.55 * math.exp(-0.9 * q) * math.cos(2 * math.pi * 0.62 * q) + 0.02 * math.sin(2 * math.pi * 0.35 * u)
        P2.lampara(h, 560, 168, 150, ang, 0.0, sem=700)
        P2.reloj_gato(h, 830, 262, 62, t, sem=720)
        P2.gota_agua(h, MC.GRIFO[0] - 5, MC.GRIFO[1], u + 12.5, per=1.35, ph=0.792, sem=740)
        # pescado en su estante (hasta que el gato lo agarra) y tarta (hasta que el monstruo la agarra)
        if u < U_PESCADO:
            P2.pescado(h, *MC.POS_PESCADO, 0.9, 0.0, sem=910)
        if u < 1.5:
            P2.tarta(h, *MC.POS_TARTA, 0.95, 0.0, sem=900)
        # puerta del refri abierta (rebota un poco al reventar)
        th = 1.94 + 0.30 * math.exp(-2.4 * u) * math.cos(2 * math.pi * 1.5 * u)
        P2.puerta_refri(h, th, MC.PUERTA, sem=780)
        # el gato colgado (detrás del monstruo mientras está en el techo)
        h.tinte = np.array([0.94, 0.94, 1.0], np.float32)
        pg = self.AG.pose(u)
        g = self.g
        if u < U_CAE + 0.2:
            g.dibujar(h, pg)
        # el monstruo
        pm = self.AC.pose(u)
        an = self.c.dibujar(h, pm)
        h.tinte = np.array([1, 1, 1], np.float32)
        self.props_monstruo(h, t, u, pm, an)
        if u >= U_CAE + 0.2:
            h.tinte = np.array([0.94, 0.94, 1.0], np.float32)
            g.dibujar(h, pg)
            h.tinte = np.array([1, 1, 1], np.float32)
            if SEG_CAMINA[0] < u:
                self.pescado_gato(h, u, pg, g)
        self.efectos(h, t, u, pm, an, pg)
        # luces
        h.ambiente = np.array([0.72, 0.74, 0.92], np.float32)
        h.luz_radial(820, 640, 560, (0.30, 0.42, 0.85), 0.40)
        kk = 0.6 * (0.92 + 0.08 * math.sin(u * 33)) * (1 if u > 0.2 else 0.3 + 3 * u)
        h.luz_radial(300, 900, 1250, (0.50, 0.90, 0.95), 0.55 * kk)
        h.luz_cono(520, 960, 0.38, 0.78, 1700, (0.45, 0.88, 0.95), 0.50 * kk)

    def pescado_gato(self, h, u, pg, g):
        """El pescado en la mano del gato después de agarrarlo."""
        if u < U_PESCADO:
            return
        x, y = pg["x"], pg["y"]
        mx_, my_ = self._mano_i_gato(u)
        P2.pescado(h, x + mx_ * S, y + my_ * S + 20, 0.55, -0.35, sem=930)

    def props_monstruo(self, h, t, u, pm, an):
        # tarta en la mano del monstruo y su vuelo hasta la boca
        if 1.5 <= u < U_GRITO:
            mx, my = an["mano_i"]
            P2.tarta(h, mx + 6, my + 52, 0.7 * (MS / 1.1), -0.12, sem=950)
        elif U_GRITO <= u < U_CHOMP:
            p0 = self.c.anclas(self.AC.pose(U_GRITO), h)["mano_i"]
            p1 = self.c.anclas(self.AC.pose(U_CHOMP), h)["boca"]
            tau = u - U_GRITO
            T_ = U_CHOMP - U_GRITO
            gv = 2800.0
            vy = ((p1[1] - p0[1]) - 0.5 * gv * T_ * T_) / T_
            x = p0[0] + (p1[0] - p0[0]) * tau / T_
            y = p0[1] + vy * tau + 0.5 * gv * tau * tau
            P2.tarta(h, x, y, 0.7, 0.25 + 5.2 * tau, sem=950)
        if U_CHOMP <= u < U_CHOMP + 0.35:
            q = (u - U_CHOMP) / 0.35
            bx, by = an["boca"]
            for i in range(6):
                a = math.radians(-160 + i * 28)
                h.forma(elipse_(bx + math.cos(a) * (60 + 120 * q), by + math.sin(a) * (40 + 80 * q), 14, 11, n=8), (216, 152, 66), None, w=0, jit=1.0,
                        alfa=1 - q, tex=0, sem=960 + i)

    def efectos(self, h, t, u, pm, an, pg):
        # revienta el refri: cubitos y escarcha
        if u < 1.5:
            rng = np.random.default_rng(8)
            for i in range(12):
                a = math.radians(rng.uniform(-170, -10)) + 0.1
                v = rng.uniform(500, 1100)
                t0 = 0.05 + rng.uniform(0, 0.15)
                tau = u - t0
                if tau < 0 or tau > 1.3:
                    continue
                x = 310 + math.cos(a) * v * tau * 0.9 + (240 if i % 2 else -80) * tau
                y = 1300 + math.sin(a) * v * tau + 1500 * tau * tau
                if y > 1660:
                    y = 1660
                P2.hielo(h, x, y, 4 * tau * (1 if i % 2 else -1) + i, 0.9, sem=980 + i, alfa=clamp01(1.4 - tau))
            for i in range(5):
                k = clamp01((u - 0.1 - 0.1 * i) / 1.2)
                if 0 < k < 1:
                    P2.nube_escarcha(h, 280 + 60 * i, 1500 - 120 * i * 0.4, 150, k, sem=990 + i)
        # polvo del aterrizaje del monstruo y del gato
        for u0, x0 in ((0.85, MX), (U_ATERRIZA, X_CAT)):
            q = (u - u0) / 0.7
            if 0 <= q < 1:
                for s in (-1, 1):
                    for k in range(3):
                        h.forma(elipse_(x0 + s * (90 + 190 * q + 40 * k), MY - 10 - 24 * k * q, 40 + 40 * q, 24 + 18 * q, n=10), (226, 220, 206), None, w=0, jit=1.5,
                                alfa=(1 - q) * 0.7, tex=0, sem=1000 + k + (3 if s > 0 else 0))
        # grieta del techo y yeso al crujir
        if u >= U_CRACK:
            P2.grieta(h, X_CAT, 205, U_CRACK, u, 280, sem=800)
            P2.polvo_yeso(h, X_CAT, 200, U_CRACK, u, 14, sem=810)
        if U_CAE <= u < U_CAE + 0.5:
            P2.polvo_yeso(h, X_CAT, 200, U_CAE, u, 18, sem=820)
        # grito a coro: rayas y ondas desde los dos
        if U_GRITO <= u < U_CHOMP:
            hx, hy = an["ojo_g"]
            gx, gy = pg["x"], pg["y"] - 447 * S
            for (cx_, cy_, sem0) in ((hx + 80, hy + 20, 0), (gx, gy, 20)):
                for i in range(12):
                    a = i * 2 * math.pi / 12 + (0.1 if int(u * 30) % 2 else 0.0)
                    r0 = 230 + 20 * math.sin(i * 3.1 + u * 30)
                    r1 = r0 + 110 + 60 * math.sin(i * 1.7 + u * 20)
                    h.trazo(np.array([[cx_ + r0 * math.cos(a), cy_ + r0 * math.sin(a)], [cx_ + r1 * math.cos(a), cy_ + r1 * math.sin(a)]]), 6, 1100 + sem0 + i,
                            taper=(0.1, 0.8), jit=1.0, alfa=0.85)
            for kk, t0 in enumerate((U_GRITO, U_GRITO + 0.3, U_GRITO + 0.6)):
                uu = (u - t0) / 0.5
                if 0 <= uu < 1:
                    r = 150 + 560 * uu
                    pts = np.array([[(hx + 80 + gx) / 2 + r * 1.4 * math.cos(a), (hy + gy) / 2 + r * math.sin(a)] for a in np.linspace(0, 2 * math.pi, 44)])
                    h.trazo(pts, 9 * (1 - uu) + 2, 1140 + kk, alfa=1 - uu, taper=(0.0, 0.0), jit=2.0)
        # eructo: nube que sale de la boca hacia el gato
        if U_ERUCTO <= u < U_ERUCTO + 0.7:
            q = (u - U_ERUCTO) / 0.7
            bx, by = an["boca"]
            for i in range(6):
                r = 40 + 110 * q + 16 * i
                h.forma(elipse_(bx + 160 * q * (1 + 0.2 * i) + 40 * i, by - 20 + 10 * i - 40 * q, r * 0.7, r * 0.55, n=12), (170, 214, 120), None, w=0, jit=2.0,
                        alfa=(1 - q) * 0.6, tex=0, sem=1160 + i)
        # tripas: ondas junto a la barriga
        for u0 in (1.1, 7.8):
            if u0 <= u < u0 + 0.6:
                q = (u - u0) / 0.6
                cx_, cy_ = an["centro"]
                for i in (-1, 1):
                    for k in range(3):
                        h.trazo(np.array([[cx_ + i * (330 + 22 * k), cy_ + 80 + 40 * k - 30 * math.sin(q * 20 + k)], [cx_ + i * (390 + 22 * k), cy_ + 100 + 40 * k]]), 6,
                                1170 + k + i * 3, alfa=1 - q, taper=(0.2, 0.7), jit=0.8)
        # estrellitas sobre el gato al caer
        if U_ATERRIZA + 0.1 < u < U_GRITO:
            P2.estrellitas(h, pg["x"], pg["y"] - 640 * S, t, 110, 4, sem=1200)

    def post(self, img, h, t, u):
        w = 1 - prog(u, 0.0, 0.45)
        if w > 0:
            img = img * (1 - w) + w
        b = prog(u, 11.4, 12.5)
        if b > 0:
            import cv2
            k = int(10 + 120 * b * b) | 1
            ker = np.zeros((1, k), np.float32)
            ker[0, :] = 1.0 / k
            img = cv2.filter2D(img, -1, ker) * (1 - 0.5 * b * b)
        return img
