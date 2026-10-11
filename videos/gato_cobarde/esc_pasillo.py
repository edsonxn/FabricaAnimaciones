# -*- coding: utf-8 -*-
"""3. PASILLO: Mostacho avanza de puntitas (derecha -> izquierda) con la linterna. Gags: una tabla del suelo cruje y se congela con un pie en el
aire; el cascabel delata cada paso y lo ahoga con la mano; los retratos lo siguen con la mirada (uno le guiña); una sombra enorme crece
detrás de él y desaparece justo cuando se voltea. Al final, el resplandor frío de la cocina."""
import math

import numpy as np

from basec import Base
from motor import H, W, clamp01, e_back, e_out, prog, ruido1, smooth
import mundos_pasillo as MP
import props as PR
import toon as TN
from toon import Pista, blob, elipse_, espinas, muelle, pulso, suave, tubo
from toon_gato import AnimGato, Gato, cara, pasos

S = 1.25
V = 290.0                       # velocidad de caminata (px/s)
ZANC = 40.0
D_CICLO = 4 * ZANC * S          # px recorridos en un ciclo de dos pasos (el pie apoyado no patina)
X_INI = 3010.0
SEGS = [(0.0, 1.7), (2.8, 3.7), (4.7, 10.0)]     # tramos en que camina; el resto son «congelados»
Y_PIES = MP.SUELO_Y + 120                         # los pies pisan la alfombra


def _tabla():
    dt = 0.002
    us = np.arange(0, 10.6, dt)
    v = np.zeros_like(us)
    for a, b in SEGS:
        v += np.clip((us - a) / 0.22, 0, 1) * np.clip((b + 0.22 - us) / 0.22, 0, 1) * ((us >= a) & (us <= b + 0.22))
    v = np.clip(v, 0, 1) * V
    dist = np.cumsum(v) * dt
    return us, dist


_US, _DIST = _tabla()


def dist(u):
    return float(np.interp(u, _US, _DIST))


def x_gato(u):
    return X_INI - dist(u)


def fase(u):
    return dist(u) / D_CICLO


def y_gato(u):
    return Y_PIES + pasos(fase(u), ZANC, 34, -1)["bob"] * S * 0.8


class Pasillo(Base):
    BLOOM = 0.05
    GRANO = 0.05

    def sonidos(self):
        e = self.ev
        t0 = self.t0
        e(t0, "viento", 0.5, dur=9.8)
        # pasos y cascabel (un golpe por cada pie que se apoya)
        for k in range(0, 40):
            f = 0.5 * k + 0.5                    # contacto de un pie (fase 0.5 por pie)
            d = f * D_CICLO
            u_ = float(np.interp(d, _DIST, _US)) if d < _DIST[-1] else None
            if u_ is None or u_ > 9.9:
                break
            if 1.65 < u_ < 2.85 or 3.7 < u_ < 4.75:
                continue
            fuerte = u_ < 3.75
            e(t0 + u_, "paso_suave", 0.4, pan=-0.2)
            e(t0 + u_ + 0.02, "cascabel", 0.5 if fuerte else 0.12, tono=1.0 + 0.05 * (k % 3))
        e(t0 + 1.7, "crujido_tabla", 0.9)
        e(t0 + 1.75, "susto_cuerdas", 0.4)
        e(t0 + 2.9, "paso_suave", 0.3)
        e(t0 + 3.7, "cascabel_fuerte", 1.0)
        e(t0 + 5.6, "ojos_retrato", 0.5, pan=0.3)
        e(t0 + 6.1, "trago", 0.6)
        e(t0 + 7.3, "guino", 0.7, pan=-0.4)
        e(t0 + 6.9, "rugido_bajo", 0.8, dur=1.4)
        e(t0 + 8.2, "susto_cuerdas", 0.5)
        for k in range(10):
            e(t0 + 6.8 + 0.34 * k, "latido", 0.55 + 0.04 * k)
        e(t0 + 9.5, "zumbido_refri", 0.7, dur=1.0)

    def preparar(self):
        super().preparar()
        self.g = Gato(sem=5)
        self.A = AnimGato(
            x=x_gato, y=y_gato, s=[(0, S)],
            giro=[(0, -0.8), (8.0, -0.8), (8.2, 0.85, "o"), (8.75, 0.85), (8.95, -0.8, "io")],
            cara=[(0, "preocupado"), (1.7, "preocupado"), (1.78, "susto", "o"), (2.4, "susto"), (2.8, "preocupado", "io"),
                  (3.68, "preocupado"), (3.74, "terror", "o"), (4.0, "tragar", "io"), (4.9, "preocupado", "io"),
                  (5.7, "preocupado"), (5.95, "sospecha", "io"), (6.2, "susto", "o"), (6.8, "tragar", "io"), (7.5, "preocupado", "io"),
                  (8.15, "alerta"), (8.25, "susto", "o"), (8.8, "alerta", "io"), (9.3, "tragar", "io")],
            mira_x=[(0, -0.5), (3.9, -0.5), (4.1, 0.7, "o"), (4.35, -0.7, "o"), (4.6, 0.5, "o"), (4.9, -0.5, "io"), (6.0, -0.5), (6.2, 0.6, "o"), (6.9, 0.2),
                    (8.2, 0.9), (8.8, 0.9), (9.0, -0.5, "io")],
            mira_y=[(0, 0.0), (1.7, 0.0), (1.85, 0.9, "o"), (2.5, 0.9), (2.7, 0.0, "io"), (6.2, -0.4), (6.9, 0.0)],
            cab_rot=[(0, -0.04), (1.7, -0.04), (1.9, 0.14, "o"), (2.5, 0.14), (2.8, -0.04, "io"), (8.1, -0.04), (8.3, 0.1, "o"), (8.8, 0.1), (9.0, -0.04, "io")],
            cab_y=[(0, 6), (1.7, 6), (1.9, 20, "o"), (2.5, 20), (2.8, 6, "io")],
            cab_x=[(0, -12)],
            rot=lambda u: -0.07 + 0.03 * math.sin(2 * math.pi * 7 * u) * (1 if 1.8 < u < 2.7 else 0) + 0.03 * math.sin(2 * math.pi * 7 * u) * (1 if 3.8 < u < 4.6 else 0),
            mano_i=[(0, (-92, -186)), (3.55, (-92, -186)), (3.85, (-6, -292), "b"), (4.8, (-6, -292)), (5.1, (-92, -186), "io")],
            mano_d=[(0, (118, -214))],
            curva_i=[(0, 26)], curva_d=[(0, -26)],
            pie_i=lambda u: pasos(fase(u), ZANC, 34, -1)["pie_i"], pie_d=lambda u: pasos(fase(u), ZANC, 34, -1)["pie_d"],
            rodilla_i=lambda u: pasos(fase(u), ZANC, 34, -1)["rodilla_i"], rodilla_d=lambda u: pasos(fase(u), ZANC, 34, -1)["rodilla_d"],
            erizo=[(0, 0), (1.75, 0), (1.85, 0.5, "o"), (2.7, 0.2), (2.9, 0), (3.7, 0), (3.78, 0.6, "o"), (4.6, 0.2), (5.0, 0),
                   (6.2, 0), (6.3, 0.5, "o"), (7.0, 0.2), (8.2, 0), (8.28, 0.6, "o"), (9.0, 0.2)],
            tiembla=[(0, 0), (1.76, 0), (1.8, 2.4), (2.7, 2.4), (2.8, 0), (3.7, 0), (3.75, 2.2), (4.7, 2.2), (4.8, 0), (6.2, 0), (6.25, 2.4), (7.0, 1.2),
                     (8.2, 0), (8.25, 2.6), (9.0, 1.5)],
            sudor=[(0, 0), (1.9, 0), (2.1, 0.8), (2.9, 0), (6.4, 0), (6.6, 0.9), (7.6, 0.2), (8.4, 0.8), (9.6, 0.8)],
            cola_hincha=[(0, 0), (1.75, 0), (1.85, 0.6, "o"), (2.9, 0.1), (3.7, 0), (3.78, 0.7, "o"), (4.8, 0.2), (6.2, 0), (6.3, 0.7, "o"), (7.2, 0.3)],
            linterna=lambda u: math.pi + 0.0 + 0.06 * math.sin(3 * u),
            golpes=[(1.72, 0.1), (3.72, 0.12), (6.22, 0.1), (8.26, 0.12)],
        )

    # ------------------------------------------------------------------ cámara
    def cam(self, u):
        if not hasattr(self, "_cam"):
            self._z = Pista([(0, 1.0), (1.55, 1.0), (1.85, 1.30, "o"), (2.7, 1.30), (3.0, 1.0, "io"), (3.62, 1.0), (3.82, 1.40, "o"), (4.6, 1.40),
                             (5.0, 1.0, "io"), (6.0, 1.0), (6.25, 1.22, "o"), (6.95, 1.22), (7.3, 1.0, "io"), (8.1, 1.0), (8.25, 1.25, "o"), (8.9, 1.25),
                             (9.2, 1.0, "io"), (9.6, 1.0), (10.0, 1.45, "i")])
            self._cam = True
        z = float(self._z(u))
        xc = x_gato(u)
        cx = xc - 150 / z + (20 * math.sin(1.7 * u))
        cy = 1010 + (-30 if z > 1.1 else 0) * 0 + 6 * math.sin(2.1 * u)
        if z > 1.2:
            cy = 1090
        return z, cx, cy, 0.0

    # ------------------------------------------------------------------ dibujo
    def ojos_retratos(self, h, t, u, cat_head):
        for k, d in enumerate(MP.RETRATOS):
            for j, (ox, oy) in enumerate((d["oi"], d["od"])):
                cx, cy = d["x"] + ox, d["y"] + oy
                r = d["r"]
                # parpadeo y guiño (el retrato de la viejita guiña al pasar el gato)
                cerrado = 0.0
                if k == 0 and j == 1 and 7.25 < u < 7.65:
                    cerrado = 1.0
                if (u * 0.9 + k * 1.7) % 4.3 < 0.12:
                    cerrado = 1.0
                dx, dy = cat_head[0] - cx, cat_head[1] - cy
                L = math.hypot(dx, dy) + 1e-6
                look = min(1.0, L / 300.0)
                px, py = cx + dx / L * r * 0.5 * look, cy + dy / L * r * 0.5 * look
                near = 1 - clamp01(L / 600.0)
                esc = 1.0 + 0.25 * near
                if cerrado > 0.5:
                    h.trazo(np.array([[cx - r, cy], [cx, cy + 6], [cx + r, cy]]), 6, 300 + k * 4 + j, taper=(0.2, 0.2), jit=0.5)
                else:
                    E = elipse_(cx, cy, r * esc, r * 1.12 * esc, n=20)
                    h.forma(E, (250, 246, 232), (210, 204, 190), w=5, sem=310 + k * 4 + j, jit=0.6, tex=0.0, d_sombra=(3, 5))
                    h.disco(px, py, r * 0.42, (16, 12, 18), sem=330 + k * 4 + j, w=0)
                    h.disco(px - r * 0.12, py - r * 0.14, r * 0.12, (255, 255, 255), sem=340 + k * 4 + j, w=0)

    def sombra_monstruo(self, h, t, u):
        """Sombra gigante en la pared, detrás del gato (aparece, crece, desaparece cuando él mira atrás)."""
        a = prog(u, 6.8, 7.5)
        if u > 8.15 and u < 8.75:
            a = 0.0
        elif u >= 8.75:
            a = prog(u, 8.75, 9.2)
        if a <= 0.01:
            return
        k = 0.85 + 0.55 * a + 0.12 * math.sin(u * 3)
        xc = x_gato(u) + 480 + 90 * (1 - a)
        yb = MP.SUELO_Y + 80
        col = (8, 6, 18)
        # cuerpo encorvado
        cuerpo = blob(xc, yb - 520 * k, 250 * k, 360 * k, rad=[1, 1.08, 0.94, 1.05, 1.0, 0.92, 1.06, 1.0], n=8, sub=8)
        h.forma(cuerpo, col, None, w=0, jit=2.0, alfa=0.80 * a, tex=0, sem=400)
        cab = blob(xc - 60 * k, yb - 900 * k, 118 * k, 104 * k, rad=[1, 1.1, 0.95, 1.05, 1, 0.92], n=6, sub=8)
        h.forma(cab, col, None, w=0, jit=2.0, alfa=0.80 * a, tex=0, sem=401)
        for sg in (-1, 1):                       # cuernos
            c0 = np.array([xc - 60 * k + sg * 70 * k, yb - 960 * k])
            h.forma(np.array([c0, c0 + np.array([sg * 40 * k, -150 * k]), c0 + np.array([-sg * 20 * k, -10 * k])]), col, None, w=0, jit=1.0,
                    alfa=0.80 * a, tex=0, sem=402 + sg)
        # brazo largo hacia el gato con garras
        base = np.array([xc - 190 * k, yb - 620 * k])
        punta = np.array([x_gato(u) + 120 + 60 * math.sin(u * 4), yb - 560 * k + 60 * math.sin(u * 2.3)])
        eje = TN.eje_curvo(base, punta, -140 * k, 20)
        h.forma(tubo(eje, 70 * k, 30 * k), col, None, w=0, jit=2.0, alfa=0.80 * a, tex=0, sem=404)
        d = punta - eje[-3]
        d = d / (np.hypot(*d) + 1e-9)
        n_ = np.array([-d[1], d[0]])
        for i in (-1, 0, 1):
            b0 = punta + n_ * i * 16 * k
            h.forma(np.array([b0 - n_ * 7 * k, b0 + d * 70 * k + n_ * i * 10 * k, b0 + n_ * 7 * k]), col, None, w=0, jit=0.8, alfa=0.80 * a, tex=0, sem=410 + i)
        # ojos que brillan
        ea = clamp01((a - 0.4) / 0.4)
        for sg in (-1, 1):
            h.forma(np.array([(xc - 60 * k + sg * 44 * k - 24 * k, yb - 900 * k - 8 * k), (xc - 60 * k + sg * 44 * k + 24 * k, yb - 900 * k + 8 * k * sg),
                              (xc - 60 * k + sg * 44 * k + 20 * k, yb - 900 * k + 22 * k)]), (255, 214, 70), None, w=0, jit=0.5, alfa=ea, tex=0, sem=420 + sg)

    def dibujar(self, h, t, u):
        z, cx, cy, rot = self.cam(u)
        h.camara(z, cx, cy, rot)
        capas = MP.pasillo()
        for rgba, ox, oy, prof in capas[:2]:
            h.pegar_capa(rgba, ox, oy, prof)
        pose = self.A.pose(u)
        pose["y"] = pose.get("y", Y_PIES)
        # los retratos miran a la cabeza del gato
        cat_head = (pose["x"], pose["y"] - 560 * S)
        self.ojos_retratos(h, t, u, cat_head)
        # luz fría de la cocina (a la izquierda) y lámpara tenue
        self.sombra_monstruo(h, t, u)
        h.tinte = np.array([0.80, 0.86, 0.96], np.float32)
        g = self.g
        T, HT = g.dibujar(h, pose)
        self.efectos_gato(h, t, u, pose)
        h.tinte = np.array([1, 1, 1], np.float32)
        h.pegar_capa(capas[2][0], capas[2][1], capas[2][2], capas[2][3])
        # luces
        h.ambiente = np.array([0.74, 0.82, 0.98], np.float32)
        a0, a1 = MP.PUERTA_COCINA
        h.luz_radial((a0 + a1) / 2, 1250, 760, (0.30, 0.95, 0.80), 0.40 + 0.22 * prog(u, 7.5, 10.0))
        h.luz_radial(2560, 1000, 520, (1.0, 0.7, 0.3), 0.20)
        am = prog(u, 6.8, 7.5) * (0 if 8.15 < u < 8.75 else 1)
        if am > 0:
            h.luz_radial(x_gato(u) + 520, 900, 760, (0.75, 0.65, 0.45), 0.85 * am)
        if g.luz is not None:
            lx, ly, la = g.luz
            h.luz_cono(lx, ly, la, 0.42, 1300, (1.0, 0.94, 0.66), 1.3, mundo=False)

    def efectos_gato(self, h, t, u, pose):
        s = S
        # líneas de crujido en la tabla del suelo
        if 1.7 <= u < 2.6:
            q = (u - 1.7) / 0.9
            x0, y0 = pose["x"] - 70, Y_PIES + 36
            for i in range(3):
                a = math.radians(-160 + i * 36 + 8 * math.sin(u * 40))
                r0, r1 = 60 + 20 * i, 110 + 40 * i + 30 * q
                h.trazo(np.array([[x0 + r0 * math.cos(a), y0 + r0 * math.sin(a) * 0.5], [x0 + r1 * math.cos(a), y0 + r1 * math.sin(a) * 0.5]]), 6, 450 + i,
                        alfa=1 - q * 0.8, taper=(0.1, 0.8), jit=0.8)
        # ondas del cascabel
        if 3.7 <= u < 4.5:
            q = (u - 3.7) / 0.8
            bx, by = pose["x"], pose["y"] - 296 * s
            for i in range(3):
                rr = 40 + 70 * q + 30 * i
                a0 = math.radians(150 + 12 * math.sin(u * 50))
                pts = np.array([[bx + rr * math.cos(a), by + rr * math.sin(a)] for a in np.linspace(a0, a0 + 1.1, 8)])
                h.trazo(pts, 5, 460 + i, color=(250, 214, 90), alfa=1 - q, taper=(0.3, 0.3), jit=0.5)

    def post(self, img, h, t, u):
        # entra desde el barrido de la sala (desenfoque que se va) y sale con un destello frío de la cocina
        b = 1 - prog(u, 0.0, 0.55)
        if b > 0:
            import cv2
            k = int(10 + 120 * b * b) | 1
            ker = np.zeros((1, k), np.float32)
            ker[0, :] = 1.0 / k
            img = cv2.filter2D(img, -1, ker) * (1 - 0.5 * b * b)
        fin = prog(u, 9.4, 10.0)
        if fin > 0:
            c = np.array([0.55, 1.0, 0.85], np.float32)
            img = img * (1 - 0.8 * fin) + c * 0.8 * fin
        return img
