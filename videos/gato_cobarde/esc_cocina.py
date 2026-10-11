# -*- coding: utf-8 -*-
"""4. COCINA: Mostacho entra de puntitas (una gota del grifo lo asusta), abre el refri (la puerta gira, luz fría), un OJO ENORME se abre entre los
estantes, primerísimo plano, GRITO, sale disparado al techo (grieta, polvo, la lámpara se balancea) y se queda agarrado con las garras mientras
el refri empieza a temblar."""
import math

import numpy as np

from basec import Base
from motor import H, W, clamp01, e_out, prog, ruido1, smooth
import mundos_cocina as MC
import props as PR
import props2 as P2
import toon as TN
from toon import Pista, elipse_, muelle, pulso, tiembla
from toon_gato import AnimGato, Gato, pasos

S = 1.35
V = 190.0
ZANC = 40.0
D_CICLO = 4 * ZANC * S
X_INI = 1330.0
SEGS = [(0.0, 1.8), (2.75, 4.15)]
Y_PIES = 1690.0
U_GOTA = 1.8
U_ABRE = 5.1
U_OJO = 7.15
U_GRITO = 8.22
U_SALTO = 9.35
U_TECHO = 9.64
Y_TECHO = 1175.0
X_TECHO = 900.0       # donde se queda colgado del techo (sobre el mesón, lejos del refri)


def _tabla():
    dt = 0.002
    us = np.arange(0, 12.6, dt)
    v = np.zeros_like(us)
    for a, b in SEGS:
        v += np.clip((us - a) / 0.22, 0, 1) * np.clip((b + 0.22 - us) / 0.22, 0, 1) * ((us >= a) & (us <= b + 0.22))
    return us, np.cumsum(np.clip(v, 0, 1) * V) * dt


_US, _DIST = _tabla()


def dist(u):
    return float(np.interp(u, _US, _DIST))


def x_gato(u):
    x = X_INI - dist(u)
    if u > 6.2:
        x -= 38 * smooth(prog(u, 6.2, 6.9))
    if u > U_SALTO:
        x += (X_TECHO - (X_INI - dist(U_SALTO) - 38)) * e_out(prog(u, U_SALTO + 0.05, U_TECHO))
    return x


def fase(u):
    return min(dist(u), dist(4.2)) / D_CICLO


def y_gato(u):
    y = Y_PIES + (pasos(fase(u), ZANC, 34, -1)["bob"] * S * 0.8 if u < 4.3 else 0.0)
    if U_GOTA <= u < U_GOTA + 0.36:
        y -= 46 * math.sin(math.pi * (u - U_GOTA) / 0.36)
    if U_GRITO - 0.25 < u < U_GRITO:
        y -= 20 * math.sin(math.pi * (u - U_GRITO + 0.25) / 0.25)
    if u >= U_SALTO - 0.2:
        a = smooth(prog(u, U_SALTO - 0.2, U_SALTO))
        y += 34 * a * (1 - prog(u, U_SALTO, U_SALTO + 0.04))
        k = e_out(prog(u, U_SALTO + 0.03, U_TECHO))
        y = y * (1 - k) + (Y_TECHO - 48 * math.sin(math.pi * k)) * k
        if u > U_TECHO:
            y = Y_TECHO + 26 * math.exp(-5.0 * (u - U_TECHO)) * math.cos(2 * math.pi * 2.2 * (u - U_TECHO)) * -1 + 4 * math.sin(2 * math.pi * 0.9 * u)
    return y


def theta(u):
    if u < U_ABRE:
        return 0.12 + 0.012 * math.sin(2 * math.pi * 1.7 * u)        # el refri respira: la puerta se mueve un poco
    f = Pista([(U_ABRE, 0.12), (U_ABRE + 0.35, 0.10, "i"), (U_ABRE + 0.95, 1.10, "io"), (U_ABRE + 1.6, 1.94, "m")])
    return float(f(u))


def asa_mundo(u):
    xf = MC.PUERTA["bx"] + 460 * math.cos(theta(u))
    return MC.PUERTA["bx"] + 0.9 * (xf - MC.PUERTA["bx"]), 1190.0


def mano_i(u):
    d0 = np.array([-92.0, -186.0])
    if u < 4.45:
        return d0
    x, y = x_gato(u), y_gato(u)
    ax, ay = asa_mundo(u)
    tgt = np.array([(ax - x) / S + 8, (ay - y) / S])
    if u < U_ABRE + 0.9:
        k = smooth(prog(u, 4.45, 5.0))
        return d0 + (tgt - d0) * k
    k = 1 - smooth(prog(u, U_ABRE + 0.9, U_ABRE + 1.35))
    tgt2 = np.array([(ax - x) / S + 8, (ay - y) / S])
    d1 = np.array([-70.0, -230.0])
    base = d1 + (tgt2 - d1) * k
    if u > U_SALTO - 0.1:
        k = smooth(prog(u, U_SALTO - 0.1, U_SALTO + 0.12))
        return base + (np.array([-96.0, -760.0]) - base) * k
    return base


class Cocina(Base):
    BLOOM = 0.08

    def sonidos(self):
        e = self.ev
        t0 = self.t0
        e(t0, "zumbido_refri", 0.5, dur=12.4)
        for k in range(10):
            ux = (k * 1.35 + 0.558) + 0.92 * 1.35 - 1.35
            if 0 < ux < 12.4:
                e(t0 + ux, "gota", 0.55, pan=0.5)
        for k in range(0, 12):
            f = 0.5 * k + 0.5
            d = f * D_CICLO
            u_ = float(np.interp(d, _DIST, _US)) if d < _DIST[-1] else None
            if u_ is None or u_ > 4.2:
                break
            if 1.78 < u_ < 2.78:
                continue
            e(t0 + u_, "paso_suave", 0.4, pan=0.1)
            e(t0 + u_ + 0.02, "cascabel", 0.3, tono=1.0 + 0.05 * (k % 3))
        e(t0 + U_GOTA, "susto_cuerdas", 0.35)
        e(t0 + U_ABRE + 0.1, "puerta_refri", 0.8, dur=1.6)
        e(t0 + U_ABRE + 1.0, "luz_fria", 0.7)
        e(t0 + U_OJO + 0.2, "ojo_abre", 0.9)
        for k in range(9):
            e(t0 + 7.2 + 0.12 * k + 0.0045 * k * k, "latido", 0.5 + 0.05 * k)
        e(t0 + U_GRITO, "grito_gato", 1.0, dur=1.3)
        e(t0 + U_GRITO, "estallido", 0.8)
        e(t0 + U_SALTO, "boing", 0.7, tono=0.8)
        e(t0 + U_SALTO + 0.05, "whoosh", 0.7, dur=0.4, tono=1.6)
        e(t0 + U_TECHO, "impacto", 1.0)
        e(t0 + U_TECHO + 0.05, "crujido", 0.8)
        e(t0 + U_TECHO + 0.2, "garras_techo", 0.7)
        e(t0 + U_TECHO + 0.3, "chirrido", 0.5, dur=2.4)
        e(t0 + 10.4, "rugido_bajo", 0.9, dur=2.0)
        e(t0 + 11.4, "refri_tiembla", 0.9, dur=1.1)

    def preparar(self):
        super().preparar()
        self.g = Gato(sem=7)
        colg = lambda u: U_TECHO
        self.A = AnimGato(
            x=x_gato, y=y_gato, s=[(0, S)],
            giro=[(0, -0.8), (7.2, -0.8), (7.8, -0.55, "io"), (9.3, -0.55), (9.7, -0.2, "o"), (11.0, -0.35, "io")],
            cara=[(0, "preocupado"), (1.72, "preocupado"), (1.82, "susto", "o"), (2.5, "preocupado", "io"), (4.2, "sospecha", "io"), (5.0, "tragar", "io"),
                  (6.15, "alerta", "o"), (6.8, "sospecha", "io"), (7.3, "tragar", "io"), (7.75, "terror", "o"), (8.2, "grito", "o"), (9.2, "grito"),
                  (9.5, "terror", "io"), (9.7, "susto", "o"), (10.5, "terror", "io"), (12.0, "terror")],
            mira_x=[(0, -0.5), (1.8, -0.5), (1.9, 0.8, "o"), (2.6, 0.0, "io"), (4.2, -0.7, "io"), (7.6, -0.8), (7.9, -0.6), (9.7, 0.0), (10.0, -0.7, "io")],
            mira_y=[(0, 0), (9.7, 0.0), (10.1, 0.8, "io")],
            cab_rot=[(0, -0.04), (7.3, -0.04), (7.8, 0.12, "io"), (8.0, -0.12, "o"), (9.2, -0.12), (9.7, 0.06, "o")],
            cab_x=[(0, -12), (6.4, -12), (7.0, -34, "io"), (9.3, -34), (9.6, 0, "o")],
            cab_y=[(0, 4), (7.3, 4), (7.8, 16, "io"), (8.2, -8, "o"), (9.3, -8), (9.7, 6, "o")],
            rot=[(0, -0.06), (4.2, -0.06), (5.0, -0.1, "io"), (6.5, -0.04, "io"), (9.1, -0.04), (9.3, 0.0), (9.62, 0.0), (9.9, 0.04, "m")],
            sq=[(0, 0.0), (U_SALTO - 0.2, 0.0), (U_SALTO - 0.02, 0.26, "o"), (U_SALTO + 0.1, -0.32, "o"), (U_TECHO - 0.04, -0.22), (U_TECHO + 0.02, 0.2, "o"),
                (U_TECHO + 0.3, -0.05, "m"), (U_TECHO + 1.0, 0.0)],
            mano_i=mano_i,
            mano_d=[(0, (118, -214)), (9.1, (118, -214)), (U_SALTO - 0.1, (60, -120), "io"), (U_SALTO + 0.12, (96, -760), "o"), (U_TECHO, (96, -742), "m")],
            curva_i=[(0, 26)], curva_d=[(0, -26)],
            pie_i=lambda u: pasos(fase(u), ZANC, 34, -1)["pie_i"] if u < U_SALTO - 0.15 else (-52.0 + 10 * math.sin(2 * math.pi * 3.2 * u), 0.0),
            pie_d=lambda u: pasos(fase(u), ZANC, 34, -1)["pie_d"] if u < U_SALTO - 0.15 else (52.0 + 10 * math.sin(2 * math.pi * 3.2 * u + 1), 0.0),
            rodilla_i=lambda u: pasos(fase(u), ZANC, 34, -1)["rodilla_i"] if u < U_SALTO - 0.15 else -30.0,
            rodilla_d=lambda u: pasos(fase(u), ZANC, 34, -1)["rodilla_d"] if u < U_SALTO - 0.15 else 30.0,
            erizo=[(0, 0), (1.8, 0), (1.9, 0.5, "o"), (2.6, 0.1), (7.4, 0), (7.8, 0.5, "o"), (8.2, 1.0, "o"), (12.5, 1.0)],
            tiembla=[(0, 0), (1.85, 0), (1.9, 2.0), (2.5, 0), (7.3, 0), (7.4, 2.0), (8.2, 4.0), (9.3, 4.0), (9.34, 0), (9.7, 0), (9.75, 4.5), (12.5, 5.5)],
            sudor=[(0, 0), (4.4, 0), (4.8, 0.7), (6.4, 0.0), (7.5, 0.0), (7.9, 1.0), (12.5, 1.0)],
            cola_hincha=[(0, 0), (1.85, 0), (1.95, 0.6, "o"), (2.7, 0.1), (7.7, 0.1), (8.2, 1.0, "o"), (12.5, 1.0)],
            rayas_miedo=[(0, 0), (7.8, 0), (8.1, 1.0, "o"), (9.2, 1.0), (9.5, 0)],
            linterna=lambda u: (math.pi - 0.28 + 0.12 * math.sin(3 * u)) if u < U_SALTO - 0.1 else None,
            golpes=[(U_GOTA, 0.1), (U_TECHO, 0.15)],
        )

    # ------------------------------------------------------------------ cámara
    def cam(self, u):
        if not hasattr(self, "_z"):
            self._z = Pista([(0, 1.0), (4.2, 1.0), (4.9, 1.12, "io"), (6.3, 1.12), (7.2, 1.45, "io"), (8.12, 1.55), (8.2, 1.95, "o"), (9.25, 1.95),
                             (9.42, 1.4, "i"), (9.75, 1.0, "o"), (12.5, 1.0)])
            self._cx = Pista([(0, 700), (4.2, 680, "io"), (7.2, 520, "io"), (8.2, 625, "o"), (9.25, 625), (9.75, 640, "io"), (12.5, 640)])
            self._cy = Pista([(0, 1040), (4.8, 1060), (7.2, 1070), (8.2, 1090, "o"), (9.25, 1090), (9.45, 820, "i"), (9.8, 980, "o"), (12.5, 960)])
        z, cx, cy = float(self._z(u)), float(self._cx(u)), float(self._cy(u))
        rot = 0.0
        if U_GRITO <= u < 9.3:
            dx, dy = tiembla(u, 12.0, sem=3)
            cx += dx
            cy += dy
            rot = 0.012 * dx / 12.0
        if u >= 10.4:
            k = prog(u, 10.4, 12.4)
            dx, dy = tiembla(u, 4 + 12 * k, sem=9)
            cx += dx
            cy += dy
        if U_TECHO <= u < U_TECHO + 0.6:
            dx, dy = tiembla(u, 16 * math.exp(-6 * (u - U_TECHO)), sem=5)
            cx += dx
            cy += dy
        return z, cx, cy, rot

    # ------------------------------------------------------------------ dibujo
    def dibujar(self, h, t, u):
        z, cx, cy, rot = self.cam(u)
        h.camara(z, cx, cy, rot)
        capas = MC.cocina()
        for rgba, ox, oy, prof in capas:
            h.pegar_capa(rgba, ox, oy, prof)
        # lámpara colgante: se balancea tras el golpe del techo
        ang = 0.04 * math.sin(2 * math.pi * 0.35 * u)
        if u > U_TECHO:
            q = u - U_TECHO
            ang += 0.55 * math.exp(-0.9 * q) * math.cos(2 * math.pi * 0.62 * q)
        enc = 1.0 if (U_TECHO < u < U_TECHO + 0.25 or (U_TECHO + 0.4 < u < U_TECHO + 0.5)) else 0.0
        bulb = P2.lampara(h, 560, 168, 150, ang, enc, sem=700)
        # reloj de gato, grifo que gotea
        P2.reloj_gato(h, 830, 262, 62, t, sem=720)
        P2.gota_agua(h, MC.GRIFO[0] - 5, MC.GRIFO[1], u, per=1.35, ph=0.792, sem=740)
        # ojo gigante entre los estantes
        th = theta(u)
        ox, oy = MC.OJO_COSA
        ab = float(Pista([(0, 0), (U_OJO, 0), (U_OJO + 0.45, 0.55, "o"), (U_OJO + 0.9, 0.95, "o"), (U_TECHO + 3.0, 1.0)])(u))
        if th > 1.2 and ab > 0:
            pose0 = self.A.pose(u)
            hx, hy = pose0["x"], pose0["y"] - 560 * S
            dx, dy = hx - ox, hy - oy
            L = math.hypot(dx, dy) + 1e-6
            miedo = prog(u, U_GRITO, U_GRITO + 0.3)
            P2.ojo_gigante(h, ox, oy, 150 + 28 * miedo, ab, (dx / L * 0.8, dy / L * 0.8), miedo, sem=760)
        # comida del refri (se ve con la puerta abierta)
        if th > 1.0:
            P2.tarta(h, *MC.POS_TARTA, 0.95, 0.0, sem=900)
            P2.pescado(h, *MC.POS_PESCADO, 0.9, 0.0, sem=910)
        # puerta del refri (cel)
        xa, ya = P2.puerta_refri(h, th, MC.PUERTA, sem=780)
        # el gato (con tinte frío cuando el refri está abierto)
        k_luz = smooth(prog(u, U_ABRE + 0.7, U_ABRE + 1.5))
        h.tinte = np.array([0.94, 0.94, 1.0], np.float32)
        pose = self.A.pose(u)
        g = self.g
        g.dibujar(h, pose)
        self.efectos(h, t, u, pose)
        h.tinte = np.array([1, 1, 1], np.float32)
        # techo: grieta y polvo
        P2.grieta(h, X_TECHO, 205, U_TECHO, u, 260, sem=800)
        P2.polvo_yeso(h, X_TECHO, 200, U_TECHO, u, 16, sem=810)
        # luces
        h.ambiente = np.array([0.70, 0.72, 0.92], np.float32)
        h.luz_radial(820, 640, 560, (0.30, 0.42, 0.85), 0.40)
        if th > 0.3:
            kk = smooth(prog(th, 0.3, 1.4)) * (0.92 + 0.08 * math.sin(u * 33))
            h.luz_radial(300, 900, 1250, (0.50, 0.90, 0.95), 0.62 * kk)
            h.luz_cono(520, 960, 0.38, 0.78, 1700, (0.45, 0.88, 0.95), 0.62 * kk)
        if enc > 0 or (U_TECHO < u < U_TECHO + 1.6):
            h.luz_radial(bulb[0], bulb[1], 520, (1.0, 0.9, 0.5), 0.9 * enc)
        if g.luz is not None:
            lx, ly, la = g.luz
            h.luz_cono(lx, ly, la, 0.40, 1100, (1.0, 0.94, 0.66), 1.1, mundo=False)

    def efectos(self, h, t, u, pose):
        s = S
        hx, hy = pose["x"], pose["y"] - 447 * s
        # rayas de grito y ondas de choque
        if U_GRITO <= u < 9.3:
            q = (u - U_GRITO) / 1.0
            n = 16
            for i in range(n):
                a = i * 2 * math.pi / n + (0.1 if int(u * 30) % 2 else 0.0)
                r0 = 190 + 20 * math.sin(i * 3.1 + u * 30)
                r1 = r0 + 130 + 70 * math.sin(i * 1.7 + u * 20)
                h.trazo(np.array([[hx + r0 * math.cos(a), hy + r0 * math.sin(a)], [hx + r1 * math.cos(a), hy + r1 * math.sin(a)]]), 7, 600 + i,
                        taper=(0.1, 0.8), jit=1.0, alfa=0.9)
            for kk, t0 in enumerate((U_GRITO, U_GRITO + 0.25, U_GRITO + 0.5)):
                uu = (u - t0) / 0.5
                if 0 <= uu < 1:
                    r = 120 + 520 * uu
                    pts = np.array([[hx + r * math.cos(a), hy + r * 0.9 * math.sin(a)] for a in np.linspace(0, 2 * math.pi, 40)])
                    h.trazo(pts, 10 * (1 - uu) + 2, 640 + kk, alfa=1 - uu, taper=(0.0, 0.0), jit=2.0)
        # estela de velocidad en el salto
        if U_SALTO <= u < U_TECHO:
            h.trazo(np.array([[pose["x"] - 40, pose["y"] + 200], [pose["x"] - 30, pose["y"] + 700]]), 12, 660, taper=(0.9, 0.0), jit=1.2, alfa=0.9)
            for i in (-1, 1):
                h.trazo(np.array([[pose["x"] + i * 130, pose["y"] - 100], [pose["x"] + i * 150, pose["y"] + 520]]), 9, 662 + i, taper=(0.9, 0.0), jit=1.2, alfa=0.9)

    def post(self, img, h, t, u):
        # destello blanco del grito
        f = max(0.0, 1 - abs(u - U_GRITO - 0.03) / 0.07)
        if f > 0:
            img = img * (1 - 0.8 * f) + 0.8 * f
        # entra desde el destello frío del pasillo
        w = 1 - prog(u, 0.0, 0.5)
        if w > 0:
            img = img * (1 - 0.8 * w) + np.array([0.55, 1.0, 0.85], np.float32) * 0.8 * w
        fin = prog(u, 12.2, 12.5)
        if fin > 0:
            img = img * (1 - fin) + fin
        return img
