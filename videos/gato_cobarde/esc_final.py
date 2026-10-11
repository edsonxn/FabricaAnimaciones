# -*- coding: utf-8 -*-
"""6. FINAL: Mostacho y la Cosa cenan a la luz de una vela (el monstruo le pasa la tarta al gato, que solo tenía espinas). Una sombra enorme con
cuernos cae desde arriba (la de verdad, la del pasillo): la vela se apaga, los dos gritan a coro, iris... y desde afuera, la casa solitaria
tiembla, salen murciélagos de la chimenea y la ventana se apaga. Cierra el círculo con la primera escena."""
import math

import numpy as np

from basec import Base
from motor import H, W, clamp01, e_out, prog, ruido1, smooth
import mundos as MU
import mundos_cocina as MC
import props as PR
import props2 as P2
import toon as TN
from toon import Pista, elipse_, muelle, pulso, tiembla
from toon_cosa import AnimCosa, Cosa
from toon_gato import AnimGato, Gato

S = 1.35
X_GATO, Y_GATO = 300.0, 1783.0
X_COSA, Y_COSA, MS = 765.0, 1690.0, 1.0
YM = MC.MESA["y_top"]
VELA_X = 520.0
U_SOMBRA = 4.5
U_VELA = 5.85
U_GRITO = 6.1
U_IRIS = 7.15
U_EXT = 7.65


class Final(Base):
    BLOOM = 0.10

    def sonidos(self):
        e = self.ev
        t0 = self.t0
        e(t0, "grillos", 0.5, dur=7.4)
        e(t0, "viento", 0.25, dur=10.0)
        for k in range(5):
            e(t0 + 0.4 + 0.42 * k, "mastica", 0.5, tono=0.9 + 0.05 * (k % 2))
        e(t0 + 1.0, "snif", 0.5)
        e(t0 + 2.4, "arrastra", 0.6, dur=0.7)
        e(t0 + 3.3, "ding", 0.6, tono=1.4)
        e(t0 + 3.35, "brillo", 0.5)
        e(t0 + 3.5, "mastica", 0.7)
        e(t0 + 3.9, "risa_cosa", 0.7)
        e(t0 + U_SOMBRA, "rugido_bajo", 0.9, dur=1.6)
        for k in range(8):
            e(t0 + U_SOMBRA + 0.2 * k, "latido", 0.5 + 0.06 * k)
        e(t0 + U_VELA, "soplo", 0.8)
        e(t0 + U_GRITO, "grito_gato", 1.0, dur=1.0)
        e(t0 + U_GRITO, "grito_cosa", 1.0, dur=1.0)
        e(t0 + U_GRITO, "estallido", 0.9)
        e(t0 + U_IRIS, "iris", 0.9)
        e(t0 + U_IRIS + 0.25, "bonk", 1.0)
        e(t0 + U_EXT, "grito_lejano", 0.9, dur=1.0)
        e(t0 + U_EXT + 0.1, "aleteo", 0.8, pan=-0.3)
        e(t0 + U_EXT + 0.3, "aleteo", 0.7, pan=0.3)
        e(t0 + U_EXT + 1.25, "apagon", 0.7)
        e(t0 + 9.0, "tum", 0.5, tono=0.8)

    def preparar(self):
        super().preparar()
        self.g = Gato(sem=13)
        self.c = Cosa(sem=23)
        mx_pie = lambda u: 650.0 - 260.0 * smooth(prog(u, 2.4, 3.2))
        self.mx_pie = mx_pie

        def mastica(u):
            if 0.0 < u < 1.8 or 3.3 < u < 4.5:
                return 0.04 + 0.28 * (0.5 + 0.5 * math.sin(2 * math.pi * 2.7 * u - math.pi / 2))
            return None

        def risa(u):
            if 3.5 < u < 4.5:
                return 0.5 + 0.3 * math.sin(2 * math.pi * 6 * u)
            return None

        def rebote_risa(u):
            return 0.05 * math.sin(2 * math.pi * 6 * u) * (1 if 3.5 < u < 4.5 else 0)

        self.AC = AnimCosa(
            s=[(0, MS)], x=[(0, X_COSA)], y=[(0, Y_COSA), (5.35, Y_COSA), (5.58, Y_COSA - 100, "o"), (7.2, Y_COSA - 100)],
            sq=lambda u: rebote_risa(u) + muelle(u, [(U_GRITO, 0.1)], 3.0, 0.2),
            cara=[(0, "feliz"), (1.7, "feliz"), (1.9, "sorpresa", "o"), (2.4, "timido", "io"), (3.3, "feliz", "io"), (4.5, "feliz"), (4.9, "neutro", "io"),
                  (5.4, "miedo", "o"), (6.05, "miedo"), (U_GRITO, "grito", "o"), (7.1, "grito")],
            boca=lambda u: (mastica(u) if mastica(u) is not None else risa(u)),
            mira_x=[(0, 0.3), (1.7, 0.3), (1.9, -0.9, "o"), (2.4, 0.2, "io"), (3.0, -0.8), (4.8, -0.8), (5.3, 0.0, "io")],
            mira_y=[(0, 0.2), (4.9, 0.2), (5.4, -0.9, "o"), (7.2, -0.9)],
            abre=lambda u: (0.2, 0.2, 0.2) if (3.5 < u < 4.5 and (u * 5) % 1 > 0.5) else (1.0, 1.0, 1.0),
            mano_i=[(0, (-300, -190)), (2.3, (-300, -190)), (2.45, (-210, -230), "io"), (3.2, (-300, -240), "io"), (3.5, (-300, -190), "io"),
                    (3.7, (-280, -420), "o"), (3.85, (-300, -190)), (4.0, (-280, -420), "o"), (4.15, (-300, -190)), (5.4, (-300, -190)), (5.6, (-250, -420), "o")],
            mano_d=[(0, (-120, -300)), (1.6, (-120, -300)), (1.7, (-70, -420), "io"), (2.3, (-120, -300), "io"), (4.9, (-120, -300)), (5.6, (240, -420), "o")],
            sudor=[(0, 0), (5.2, 0), (5.6, 1.0)],
            erizo=[(0, 0), (5.2, 0), (U_GRITO, 0.8, "o")],
            tiembla=[(0, 0), (5.3, 0), (5.5, 2.5), (U_GRITO, 6.0)],
            gelatina=[(0, 1.0), (U_GRITO, 1.0), (U_GRITO + 0.1, 1.8)],
            barriga=[(0, 0.0)],
        )
        self.AG = AnimGato(
            auto=False,
            x=[(0, X_GATO)], y=[(0, Y_GATO), (5.35, Y_GATO), (5.58, Y_GATO - 120, "o"), (7.2, Y_GATO - 120)], s=[(0, S)],
            cola_a=[(0, 2.5)],
            cara=[(0, "llanto"), (1.7, "llanto"), (2.3, "sorpresa", "o"), (2.8, "alivio", "io"), (3.3, "feliz", "o"), (4.5, "feliz"), (4.9, "alerta", "io"),
                  (5.4, "susto", "o"), (5.85, "terror", "io"), (U_GRITO, "grito", "o"), (7.1, "grito")],
            mira_x=[(0, 0.8), (1.7, 0.8), (2.3, 0.9), (2.6, 0.0, "io")],
            mira_y=[(0, 0.3), (2.4, 0.3), (2.7, 0.0), (5.3, 0.0), (5.4, -0.9, "o"), (7.2, -0.9)],
            cab_y=lambda u: (50 * smooth(prog(u, 3.2, 3.5)) * (0.5 + 0.5 * math.sin(2 * math.pi * 2.4 * u)) if 3.2 < u < 4.5 else 0.0) + (6 if u < 2.3 else 0),
            cab_rot=lambda u: (0.15 * math.sin(2 * math.pi * 1.2 * u) if u < 2.3 else 0.0) + (-0.22 * smooth(prog(u, 5.3, 5.5)) if u > 5.3 else 0.0),
            mano_i=[(0, (-90, -292)), (3.2, (-90, -292)), (3.4, (-70, -300)), (4.5, (-70, -300)), (5.5, (-120, -420), "o")],
            mano_d=[(0, (60, -440)), (0.4, (60, -440)), (0.6, (88, -292), "io"), (1.0, (50, -432), "io"), (1.4, (90, -292), "io"), (2.3, (90, -292)),
                    (3.2, (130, -300)), (4.5, (130, -300)), (5.5, (110, -430), "o")],
            curva_i=[(0, 22)], curva_d=[(0, -22)],
            pie_i=[(0, (-46, -150))], pie_d=[(0, (46, -150))], rodilla_i=[(0, -62)], rodilla_d=[(0, 62)],
            erizo=[(0, 0), (5.3, 0), (U_GRITO, 1.0, "o")],
            tiembla=[(0, 0), (5.3, 0), (5.5, 2.5), (U_GRITO, 6.0)],
            sudor=[(0, 0), (5.2, 0), (5.6, 1.0)],
            cola_hincha=[(0, 0), (5.3, 0), (U_GRITO, 1.0, "o")],
            sq=[(0, 0.0)],
            golpes=[],
        )

    def cam(self, u):
        z = 1.0 + 0.06 * smooth(prog(u, 0.0, 5.0))
        cx, cy = 540.0, 1010.0
        if u >= 5.9:
            k = smooth(prog(u, 5.9, 6.15))
            z = z + (1.16 - z) * k
            cx, cy = 540 - 10 * k, 1010 + 30 * k
        if U_GRITO <= u < U_IRIS:
            dx, dy = tiembla(u, 11, sem=6)
            cx, cy = cx + dx, cy + dy
        return z, cx, cy, 0.0

    # ---------------------------------------------------------------- cuadro de la cocina
    def cocina(self, h, t, u):
        z, cx, cy, rot = self.cam(u)
        h.camara(z, cx, cy, rot)
        for rgba, ox, oy, prof in MC.cocina():
            h.pegar_capa(rgba, ox, oy, prof)
        P2.lampara(h, 560, 168, 150, 0.01 * math.sin(u * 1.5), 0.0, sem=700)
        P2.reloj_gato(h, 830, 262, 62, t, sem=720)
        P2.gota_agua(h, MC.GRIFO[0] - 5, MC.GRIFO[1], u + 24.0, per=1.35, ph=0.792, sem=740)
        P2.puerta_refri(h, 1.94, MC.PUERTA, sem=780)
        # personajes sentados
        h.tinte = np.array([1.0, 0.96, 0.9], np.float32)
        pm = self.AC.pose(u)
        an = self.c.dibujar(h, pm)
        pg = self.AG.pose(u)
        self.g.dibujar(h, pg)
        h.tinte = np.array([1, 1, 1], np.float32)
        for rgba, ox, oy, prof in MC.mesa():
            h.pegar_capa(rgba, ox, oy, prof)
        # en la mesa: plato del gato con espinas, tarta, vela
        P2.pescado(h, X_GATO, YM + 4, 0.85, 0.0, sem=910)
        px = float(self.mx_pie(u))
        salto = 260 * math.sin(math.pi * clamp01((u - U_GRITO) / 0.7)) if u >= U_GRITO else 0.0
        P2.tarta(h, px, YM + 4 - salto, 0.9, 0.5 * salto / 260.0, sem=900, rebanada=(u < 1.8))
        if u > 3.3:
            # la cara del gato se hunde en la tarta: restos de crema
            q = clamp01((u - 3.3) / 0.4)
            for i in range(4):
                h.forma(elipse_(px + 40 - 40 * i + 20 * math.sin(u * 5 + i), YM - 40 - 14 * (i % 2), 16, 12, n=10), (248, 224, 158), None, w=0, jit=1.0,
                        alfa=q * 0.0, tex=0, sem=1300 + i)
        vk = 1.0 if u < U_SOMBRA else max(0.0, 1.0 - 0.9 * prog(u, U_SOMBRA, U_VELA - 0.1) + 0.3 * math.sin(u * 30) * prog(u, U_SOMBRA, U_VELA))
        if u >= U_VELA:
            vk = 0.0
        P2.vela(h, VELA_X, YM - 104, sem=1310)
        P2.llama(h, VELA_X, YM - 110, t, vk, sem=1320)
        # la sombra enorme que cae desde arriba
        if u >= U_SOMBRA:
            a = prog(u, U_SOMBRA, U_VELA + 0.2)
            P2.sombra_techo(h, a, u, sem=1400)
        # luces
        luz = max(0.0, 0.22 + 0.78 * vk) if u < 7.3 else 0.0
        h.ambiente = np.array([0.40, 0.44, 0.60], np.float32) * (1.0 if u < U_VELA else max(0.25, 1 - 3.0 * (u - U_VELA)))
        h.luz_radial(VELA_X, YM - 100, 980, (1.0, 0.68, 0.32), 1.15 * vk * (0.94 + 0.06 * math.sin(t * 17)))
        h.luz_radial(300, 900, 1050, (0.45, 0.85, 0.95), 0.30)
        if U_GRITO <= u < U_IRIS:
            f = 0.30 if int(u * 15) % 2 == 0 else 0.04
            h.luz_radial(540, 1150, 1100, (1.0, 0.92, 0.80), f)

    # ---------------------------------------------------------------- cierre desde afuera
    def exterior(self, h, t, u):
        q = u - U_EXT
        h.camara(1.0, 540 + 4 * math.sin(q * 40) * math.exp(-q * 1.2), 960 + 5 * math.sin(q * 33) * math.exp(-q * 1.2), 0.0)
        capas = MU.exterior()
        sh = math.sin(q * 70) * 9 * math.exp(-q * 2.2)
        for i, (rgba, ox, oy, prof) in enumerate(capas):
            if i == 1:
                ox = ox - 16 * (q + 7.6)
            elif i == 2:
                ox = ox - 30 * (q + 7.6)
            elif i == 4:
                ox, oy = ox + sh * 0.5, oy + sh
            h.pegar_capa(rgba, ox, oy, prof)
        with h.capa(0.04):
            rng = np.random.default_rng(4)
            for k in range(16):
                x, y = rng.uniform(0, W), rng.uniform(40, 820)
                if math.hypot(x - MU.LUNA[0], y - MU.LUNA[1]) < MU.LUNA[2] * 1.3:
                    continue
                PR.estrella_brillo(h, x, y, rng.uniform(7, 14), t, rng.uniform(0, 6.28), k)
        PR.aspas(h, 170, 920, 1.1 * 8 + 0.4 * q)
        PR.humo(h, 824, 892, t)
        # murciélagos que salen disparados de la chimenea
        with h.capa(1.0):
            for k in range(7):
                uu = q - 0.10 - 0.06 * k
                if 0 <= uu < 1.6:
                    ang = math.radians(-100 + 14 * k - 40)
                    x = 826 + math.cos(ang) * 560 * uu + 40 * k * uu
                    y = 880 + math.sin(ang) * 760 * uu + 160 * uu * uu * 0
                    PR.murcielago(h, x, y, 0.75 + 0.1 * (k % 3), t, k * 0.9, dir=1 if k % 2 else -1, sem=k * 5)
        # ventana: destello con el grito y luego se apaga
        vx, vy = MU.VENTANA
        fl = 1.0 if q < 1.15 else 0.0
        if 0.0 <= q < 0.5:
            fl = 1.6 + 0.4 * math.sin(q * 90)
        fl *= (1 if (q < 1.15 or q > 1.3) else 0)
        if q >= 1.15:
            h.forma(np.array([(vx - 58, vy - 74), (vx + 54, vy - 78), (vx + 58, vy + 70), (vx - 54, vy + 76)], float), (26, 22, 44), None, w=0, jit=0.5, tex=0, sem=1500)
            for dx_, dy_, w_, h_ in ((-4, -78, 10, 152), (-56, -2, 112, 10)):
                h.forma(np.array([(vx + dx_, vy + dy_), (vx + dx_ + w_, vy + dy_), (vx + dx_ + w_, vy + dy_ + h_), (vx + dx_, vy + dy_ + h_)], float), (40, 28, 52), None, w=0, jit=0.3, tex=0, sem=1501)
        h.luz_radial(vx, vy, 560, (0.95, 0.55, 0.22), 0.55 * fl)
        h.ambiente = np.array([0.90, 0.93, 1.08], np.float32)

    def dibujar(self, h, t, u):
        if u < U_IRIS + 0.45:
            self.cocina(h, t, u)
        else:
            self.exterior(h, t, u)

    def post(self, img, h, t, u):
        # entra del barrido a la derecha
        b = 1 - prog(u, 0.0, 0.5)
        if b > 0:
            import cv2
            k = int(10 + 120 * b * b) | 1
            ker = np.zeros((1, k), np.float32)
            ker[0, :] = 1.0 / k
            img = cv2.filter2D(img, -1, ker)
        # destello del grito
        f = max(0.0, 1 - abs(u - U_GRITO - 0.03) / 0.07)
        if f > 0:
            img = img * (1 - 0.85 * f) + 0.85 * f
        # iris que se cierra sobre los dos caras (cartoon clásico)
        if U_IRIS <= u < U_IRIS + 0.45:
            q = prog(u, U_IRIS, U_IRIS + 0.4)
            cx, cy = h.tf(np.array([[520.0, 1120.0]]))[0]
            yy, xx = np.mgrid[0:H:2, 0:W:2].astype(np.float32)
            d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            r = (1 - e_out(q)) * 1700 + 1
            import cv2
            m = np.clip((r - d) / 2.0 + 0.5, 0, 1)
            m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
            img = img * m
        if u >= U_IRIS + 0.45:
            # iris que se abre sobre el exterior y luego funde a negro
            q = prog(u, U_EXT, U_EXT + 0.35)
            if q < 1:
                cx, cy = W / 2, 1150
                yy, xx = np.mgrid[0:H:2, 0:W:2].astype(np.float32)
                d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
                import cv2
                m = np.clip((e_out(q) * 1900 - d) / 2.0 + 0.5, 0, 1)
                m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
                img = img * m
            img = img * (1 - prog(u, 9.35, 10.0))
        return img
