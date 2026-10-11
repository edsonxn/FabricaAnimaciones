# -*- coding: utf-8 -*-
"""1. EXTERIOR: la casa solitaria de noche; la cámara avanza hacia la ventana encendida; un golpe adentro."""
import math

import numpy as np

from basec import Base, inundar
from motor import H, W, clamp01, prog, smooth
import mundos as MU
import props as PR


class Exterior(Base):
    BLOOM = 0.12

    def sonidos(self):
        e = self.ev
        t0 = self.t0
        e(t0 + 0.0, "viento", 0.8, dur=7.4)
        e(t0 + 0.9, "aleteo", 0.5, pan=0.4)
        e(t0 + 1.4, "aleteo", 0.45, pan=-0.2)
        e(t0 + 1.9, "aleteo", 0.4, pan=0.1)
        e(t0 + 2.6, "buho", 0.6, pan=-0.5)
        e(t0 + 2.0, "chirrido", 0.4, dur=4.0, pan=-0.6)
        e(t0 + 5.15, "tum", 1.0)
        e(t0 + 5.6, "tum", 0.7, tono=0.9)

    def cam(self, u):
        p = smooth(prog(u, 0.2, 6.7))
        z = 1.0 + 1.12 * p
        cx = 540 + 150 * p + 5 * math.sin(1.1 * u)
        cy = 960 + 205 * p + 4 * math.sin(0.8 * u + 1.0)
        return z, cx, cy, 0.024 * math.sin(0.7 * u + 0.4) * (1 - p * 0.5) - 0.02 * (1 - p)

    def dibujar(self, h, t, u):
        z, cx, cy, rot = self.cam(u)
        h.camara(z, cx, cy, rot)
        capas = MU.exterior()
        # sacudida de la casa con el golpe de adentro
        tum = u - 5.15
        sh = (math.exp(-max(0, tum) * 7) * math.sin(max(0, tum) * 70) * 9) if tum > 0 else 0.0
        for i, (rgba, ox, oy, prof) in enumerate(capas):
            if i == 1:
                ox = ox - 16 * u
            elif i == 2:
                ox = ox - 30 * u
            elif i == 4:
                ox, oy = ox + sh * 0.5, oy + sh
            h.pegar_capa(rgba, ox, oy, prof)
        # estrellas
        with h.capa(0.04):
            rng = np.random.default_rng(4)
            for k in range(16):
                x, y = rng.uniform(0, W), rng.uniform(40, 820)
                if math.hypot(x - MU.LUNA[0], y - MU.LUNA[1]) < MU.LUNA[2] * 1.3:
                    continue
                PR.estrella_brillo(h, x, y, rng.uniform(7, 14), t, rng.uniform(0, 6.28), k)
        # murciélagos cruzando la luna
        with h.capa(0.10):
            for k, (u0, y0, s, vx, fase) in enumerate(((0.7, 560, 0.95, 380, 0.0), (1.3, 690, 0.8, 330, 1.7), (1.7, 450, 0.62, 300, 3.1))):
                uu = u - u0
                if 0 <= uu < 3.2:
                    x = W + 120 - vx * uu
                    y = y0 + 40 * math.sin(uu * 2.4 + k) - 22 * uu
                    PR.murcielago(h, x, y, s, t, fase, dir=-1, sem=k * 5)
        # aspas del molino (giran más rápido con las ráfagas)
        ang = 1.1 * u + 0.18 * u * u
        PR.aspas(h, 170, 920, ang)
        # humo de la chimenea
        PR.humo(h, 824, 892, t)
        # matorral rodante en primer plano
        with h.capa(1.35):
            uu = (u - 1.6) / 3.8
            if 0 <= uu <= 1:
                x = -130 + (W + 260) * uu
                hop = abs(math.sin(math.pi * (uu * 5.2)))
                y = 1640 - 170 * hop * (1 - 0.3 * uu)
                PR.matorral(h, x, y, 96, -x / 96.0 * 1.0)
        # luz de la ventana (parpadea con el golpe)
        vx, vy = MU.VENTANA
        fl = 1.0
        if u > 5.15:
            tt = u - 5.15
            fl = 0.0 if (tt < 0.12 or 0.22 < tt < 0.28 or 0.5 < tt < 0.56) else 1.0
        fl *= 0.94 + 0.06 * math.sin(u * 23) * math.sin(u * 7.1)
        h.luz_radial(vx, vy, 560, (0.95, 0.55, 0.22), 0.55 * fl)
        h.ambiente = np.array([0.90, 0.93, 1.08], np.float32)

    def post(self, img, h, t, u):
        # entra desde negro
        a = clamp01(u / 0.55)
        img = img * (a * a * (3 - 2 * a))
        # la luz de la ventana inunda el cuadro al final (empalma con la sala)
        fin = prog(u, 6.45, 7.5)
        if fin > 0:
            cx, cy = h.tf(np.array([MU.VENTANA], float))[0]
            img = inundar(img, h, cx, cy, 160 + 2600 * fin ** 1.5, (255, 214, 140), 1.0)
        return img


