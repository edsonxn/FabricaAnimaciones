# -*- coding: utf-8 -*-
"""2. SALA: Mostacho duerme en el sillón (burbuja de moco, zzz, tele con estática fuera de cuadro). Un crujido en la cocina lo despierta:
orejas, un ojo, los dos, susto, trago de saliva, se levanta de un brinco, saca la linterna y se va de puntitas hacia el pasillo."""
import math

import numpy as np

from basec import Base, inundar
from motor import H, W, clamp01, e_back, e_out, prog, ruido1, smooth
import mundos_sala as MS
import props as PR
import toon as TN
from toon import Pista, muelle, pulso
from toon_gato import AnimGato, Gato, cara, pasos

S = 1.5           # escala del gato
SEAT_Y = 1868     # y de los pies (el cojín tapa las piernas: queda sentado)
T_PASO = 1.15     # segundos por ciclo de dos pasos
ZANC = 40.0
V_ANDAR = 4 * ZANC * S / T_PASO
U_PASEO = 5.0     # empieza a caminar
X_SALTO = 135.0   # donde cae del brinco (ya fuera del sillón)


def x_gato(u):
    if u < 4.3:
        return 650.0
    if u < U_PASEO - 0.02:
        k = (u - 4.3) / (U_PASEO - 0.02 - 4.3)
        return 650.0 + (X_SALTO - 650.0) * (1 - (1 - k) ** 2)
    return X_SALTO - V_ANDAR * (u - U_PASEO)


def y_gato(u):
    if u < 4.15:
        return SEAT_Y + 3 * math.sin(2 * math.pi * 0.42 * u)
    if u < 4.3:
        return SEAT_Y + 26 * smooth((u - 4.15) / 0.15)            # se agacha (anticipación)
    if u < U_PASEO - 0.02:
        k = (u - 4.3) / (U_PASEO - 0.02 - 4.3)
        return SEAT_Y + 26 * (1 - k) - 250 * math.sin(math.pi * k) ** 0.9
    return SEAT_Y + pasos((u - U_PASEO) / T_PASO, ZANC, 34, -1)["bob"] * S


def _seated_blend(u):
    """1 = sentado (piernas dobladas y escondidas tras el cojín), 0 = de pie; se estira durante el brinco."""
    return 1.0 - smooth(prog(u, 4.12, 4.5))


def pies(u, lado):
    b = _seated_blend(u)
    sg = -1.0 if lado == "i" else 1.0
    if u < U_PASEO - 0.02:
        return (sg * 46.0, -150.0 * b)
    f = pasos((u - U_PASEO) / T_PASO, ZANC, 34, -1)["pie_" + lado]
    return f


def rodilla(u, lado):
    b = _seated_blend(u)
    sg = -1.0 if lado == "i" else 1.0
    if u < U_PASEO - 0.02:
        return sg * (22.0 + 40 * b)
    return pasos((u - U_PASEO) / T_PASO, ZANC, 34, -1)["rodilla_" + lado]


class Sala(Base):
    BLOOM = 0.06

    def sonidos(self):
        e = self.ev
        t0 = self.t0
        e(t0 + 0.0, "estatica", 0.55, dur=7.4)
        for k in range(8):
            e(t0 + 0.2 + k * 1.0, "tic" if k % 2 == 0 else "tac", 0.22, pan=0.5)
        for k in range(4):
            e(t0 + 0.5 + 1.15 * k, "ronquido", 0.5, tono=1.0 - 0.04 * k)
        e(t0 + 2.2, "crujido", 0.7, pan=-0.6)
        e(t0 + 2.85, "pop", 0.6)
        e(t0 + 3.02, "susto_cuerdas", 0.8)
        e(t0 + 3.6, "trago", 0.8)
        e(t0 + 4.3, "boing", 0.7, tono=1.1)
        e(t0 + 4.9, "puf", 0.5)
        e(t0 + 4.95, "clic", 0.7)
        for k in range(5):
            e(t0 + U_PASEO + 0.15 + T_PASO / 2 * k, "paso_suave", 0.45, pan=-0.3)
            e(t0 + U_PASEO + 0.18 + T_PASO / 2 * k, "cascabel", 0.35, pan=-0.3, tono=1.0 + 0.04 * k)
        e(t0 + 6.8, "whoosh", 0.7, dur=0.7)

    def preparar(self):
        super().preparar()
        self.g = Gato(sem=3)
        z = lambda u0: u0
        self.A = AnimGato(
            x=x_gato, y=y_gato,
            s=[(0, S)],
            cola_a=[(0, 0.7), (4.0, 0.7), (4.5, -0.9, "io")],
            cara=[(0, "dormido"), (2.25, "dormido"), (2.5, "adormilado", "o"), (2.82, "alerta", "o"), (3.02, "susto", "B"),
                  (3.5, "tragar", "io"), (4.1, "preocupado", "io"), (4.95, "alerta", "io"), (5.8, "preocupado")],
            giro=[(0, 0.0), (2.5, 0.0), (3.1, -0.75, "o"), (4.6, -0.8), (4.8, -0.95)],
            mira_x=[(0, 0), (2.7, 0), (3.0, -0.55, "o")],
            cab_rot=[(0, 0.30), (2.2, 0.30), (2.5, 0.06, "o"), (3.0, -0.08, "b"), (3.5, 0.0), (3.6, 0.1, "io"), (3.75, -0.04, "o"), (4.2, 0.0)],
            cab_y=[(0, 10), (2.2, 10), (2.7, 0, "o"), (3.0, -14, "o"), (3.6, 10, "io"), (3.8, -4, "o")],
            rot=[(0, 0.04), (2.4, 0.04), (2.9, 0.0, "o"), (4.3, 0.0), (4.6, -0.08, "o"), (5.0, -0.05)],
            sq=[(0, 0.0), (4.0, 0.0), (4.22, 0.22, "o"), (4.4, -0.2, "o"), (4.85, 0.0, "io"), (4.95, 0.12, "o"), (5.1, 0.0)],
            mano_i=[(0, (34, -206)), (2.8, (34, -206)), (3.05, (-132, -388), "B"), (3.6, (-118, -362)), (4.1, (-60, -250), "io"), (4.8, (-110, -190), "io"),
                    (5.2, (-70, -210))],
            mano_d=[(0, (-34, -206)), (2.8, (-34, -206)), (3.05, (132, -388), "B"), (3.6, (118, -362)), (4.1, (60, -250), "io"), (4.75, (118, -214), "io")],
            curva_i=[(0, 20)], curva_d=[(0, -20)],
            pie_i=lambda u: pies(u, "i"), pie_d=lambda u: pies(u, "d"),
            rodilla_i=lambda u: rodilla(u, "i"), rodilla_d=lambda u: rodilla(u, "d"),
            erizo=[(0, 0), (3.0, 0), (3.12, 0.6, "o"), (3.9, 0.3), (4.4, 0)],
            tiembla=[(0, 0), (3.05, 0), (3.1, 3.2), (4.0, 3.2), (4.2, 0)],
            sudor=[(0, 0), (3.3, 0), (3.5, 0.8), (4.7, 0.0)],
            cola_hincha=[(0, 0), (3.05, 0), (3.2, 0.7, "o"), (4.3, 0.3), (5.2, 0)],
            burbuja=lambda u: 0.0 if (u > 2.82 or u < 0.02) else 8 + 40 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.42 * u - math.pi / 2)) ** 1.4,
            oreja_i=[(0, 0), (2.2, 0), (2.3, -0.3, "o"), (2.5, -0.1)],
            linterna=lambda u: (math.pi - 0.28) if u > 4.9 else None,
            golpes=[(4.9, 0.1)],
        )

    # ------------------------------------------------------------------ cámara (claves continuas)
    def cam(self, u):
        if not hasattr(self, "_cam"):
            self._cam = (
                Pista([(0, 1.0), (2.2, 1.18, "io"), (2.95, 1.40, "o"), (3.55, 1.40), (4.35, 1.06, "io"), (5.2, 1.04)]),
                Pista([(0, 650), (2.2, 640, "io"), (2.95, 585, "o"), (3.55, 585), (4.35, 600, "io"), (5.0, 300, "io"), (5.9, -20, "io"), (7.5, -330, "i")]),
                Pista([(0, 1140), (2.2, 1110, "io"), (2.95, 1135, "o"), (3.55, 1135), (4.35, 1235, "io"), (5.2, 1262)]),
                Pista([(0, 0.0), (2.95, -0.03, "o"), (3.55, -0.03), (4.35, 0.0, "io")]),
            )
        z, cx, cy, r = self._cam
        return float(z(u)), float(cx(u)), float(cy(u)), float(r(u))

    def estatica(self, u):
        """Luz de la tele que parpadea (fuera de cuadro, delante del sillón)."""
        k = 0.26 + 0.20 * ruido1(np.array([u * 22.0]), 5, 0)[0] + 0.12 * ruido1(np.array([u * 61.0]), 6, 0)[0]
        if 2.95 < u < 3.1:
            k += 0.5
        return max(0.05, k)

    def dibujar(self, h, t, u):
        z, cx, cy, rot = self.cam(u)
        h.camara(z, cx, cy, rot)
        capas = MS.sala()
        for rgba, ox, oy, prof in capas[:2]:
            h.pegar_capa(rgba, ox, oy, prof)
        # polvo en el haz de luna
        PR.polvo(h, 380, 900, 760, 1500, t, n=22, sem=2, color=(190, 210, 255), alfa=0.55, r=3.2)
        # reloj: manecillas (las 3:00) y segundero que salta
        rx, ry, rr = MS.RELOJ
        h.trazo(np.array([[rx, ry], [rx + rr * 0.50, ry]]), 11, 7, taper=(0.1, 0.2), jit=0.5)
        h.trazo(np.array([[rx, ry], [rx, ry - rr * 0.78]]), 8, 8, taper=(0.1, 0.2), jit=0.5)
        sg = math.floor(t) * 6.0 + 2.0 * math.exp(-((t % 1.0) * 14)) * math.sin((t % 1.0) * 60)
        a = math.radians(sg - 90)
        h.trazo(np.array([[rx - 14 * math.cos(a), ry - 14 * math.sin(a)], [rx + rr * 0.86 * math.cos(a), ry + rr * 0.86 * math.sin(a)]]), 4.5, 9,
                color=(150, 30, 40), taper=(0.1, 0.1), jit=0.3)
        h.disco(rx, ry, 8, (60, 40, 44), sem=3, w=2.5)
        # el gato
        h.tinte = np.array([0.88, 0.92, 1.0], np.float32)
        pose = self.A.pose(u)
        g = self.g
        g.dibujar(h, pose)
        self.efectos_gato(h, t, u, pose)
        h.tinte = np.array([1, 1, 1], np.float32)
        for rgba, ox, oy, prof in capas[2:]:
            h.pegar_capa(rgba, ox, oy, prof)
        # luces
        h.ambiente = np.array([0.84, 0.90, 1.02], np.float32)
        h.luz_radial(660, 1960, 1500, (0.26, 0.46, 0.95), self.estatica(u))
        h.luz_radial(150, 780, 540, (0.30, 0.38, 0.75), 0.30)
        if g.luz is not None and u > 4.9:
            lx, ly, la = g.luz
            h.luz_cono(lx, ly, la, 0.34, 1000, (1.0, 0.92, 0.62), 0.85, mundo=False)
            h.luz_radial(lx, ly, 110, (1.0, 0.95, 0.7), 0.25, mundo=False)

    def efectos_gato(self, h, t, u, pose):
        """Zzz, burbuja que revienta, humito de la linterna que aparece."""
        s = S
        base = np.array([pose.get("x", 650) + 150 * s * 0.55, pose.get("y", SEAT_Y) - 690 * s * 0.88])
        for k, u0 in enumerate((0.4, 1.35, 2.15)):
            q = (u - u0) / 1.7
            if 0 <= q <= 1 and u < 2.82:
                x = base[0] + 40 * q + 12 * math.sin(q * 7)
                y = base[1] - 120 * q
                zz = (26 + 22 * k) * (0.5 + 0.8 * q)
                al = math.sin(math.pi * q)
                col = (220, 235, 255)
                pts = np.array([[x - zz, y - zz], [x + zz, y - zz], [x - zz, y + zz], [x + zz, y + zz]])
                h.trazo(pts, 8 + 2 * k, 20 + k, color=col, alfa=al, taper=(0.05, 0.05), jit=0.9)
        # estallido de la burbuja
        if 2.82 <= u < 3.12:
            q = (u - 2.82) / 0.3
            bx = pose.get("x", 650) + 20 * s * 0.0
            by = pose.get("y", SEAT_Y) - 445 * s + 62 * s
            px = bx + (-30 + 30) * s
            for i in range(9):
                a = i * 2 * math.pi / 9
                r0, r1 = 36 + 90 * q, 70 + 130 * q
                h.trazo(np.array([[px + 50 + r0 * math.cos(a), by + r0 * math.sin(a)], [px + 50 + r1 * math.cos(a), by + r1 * math.sin(a)]]), 5, 40 + i,
                        color=(190, 236, 255), alfa=1 - q, taper=(0.1, 0.8), jit=0.5)
        # puf de la linterna
        if 4.82 <= u < 5.1:
            q = (u - 4.82) / 0.28
            hx = pose.get("x", 650) + 112 * 0 - 120
            hy = pose.get("y", SEAT_Y) - 214 * s
            for i in range(7):
                a = i * 2 * math.pi / 7
                rr_ = 30 + 70 * q
                h.forma(TN.elipse_(hx + rr_ * math.cos(a) * 0.9, hy + rr_ * math.sin(a) * 0.8, 20 * (1 - q) + 8, 18 * (1 - q) + 8, n=12), (236, 236, 244),
                        None, w=0, jit=1.0, alfa=(1 - q) * 0.8, tex=0, sem=60 + i)

    def post(self, img, h, t, u):
        # empalma con la luz cálida del exterior
        w = 1 - prog(u, 0.0, 0.7)
        if w > 0:
            cx, cy = W * 0.5, H * 0.45
            img = inundar(img, h, cx, cy, 3200 * w + 1, (255, 214, 140), w)
        # barrido al pasillo: desenfoque de movimiento horizontal
        b = prog(u, 6.7, 7.5)
        if b > 0:
            import cv2
            k = int(10 + 120 * b * b) | 1
            ker = np.zeros((1, k), np.float32)
            ker[0, :] = 1.0 / k
            img = cv2.filter2D(img, -1, ker)
            img = img * (1 - 0.5 * b * b)
        return img
