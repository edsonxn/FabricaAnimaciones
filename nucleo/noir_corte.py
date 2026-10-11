# -*- coding: utf-8 -*-
"""NOIR CORTE: el reparto de una corte medieval para el noir feudal (nucleo/noir_feudal.py, a color con nucleo/noir_color.py).
Reyes, reinas, damas, ancianas, caballeros, bufones, enanos y comensales con el mismo claroscuro que el pesquisidor.
Personajes PROPIOS (rasgos configurables): nunca copiar el aspecto de actores de una serie; emblemas genéricos.

    import noir_color as NC, noir_feudal as NF, noir_corte as CO
    rey = CO.BustoCorte(sem=3, pelo="corto", pelo_rampa="oro", pelo_tono=160, corona="rey", ropa=("estandarte", 110), joven=True)
    rey.dibujar(h, dict(x=900, y=480, s=1.0, d=1, luz=(0.8, -0.6), boca=0.3, mira=0.0, ceño=0.5, sonrisa=0.4))
    # ahogo=0..1 (tiembla, ojos desorbitados, boca abierta, la cara se amorata), manos_cuello=0..1
    vieja = CO.Cortesano(sem=7, toca=True, edad=1.0, ropa=("tela_verde", 110), baston=True)
    vieja.dibujar(h, dict(x=600, y=950, s=1.0, d=1, mano=(70, -330), rot=0.0, andar=0.0, paso=0.0))
    CO.comensales(h, t, x0, x1, y_mesa, n=10, s=1.0, sem=1, reaccion=0.0)   # fila de invitados sentados tras una mesa

Rasgos (BustoCorte y Cortesano): pelo = corto | melena | largo | trenza | calvo | ninguno · pelo_rampa/pelo_tono · barba = None |
perilla | corta | rala · corona = None | rey | diadema · toca (velo y griñón de anciana) · edad 0..1 · joven · fem · nariz = recta |
aguileña | pequeña · ropa = (rampa, tono) · capa = (rampa, tono) | None · piel (tono) · collar = n piedras (falta = índice vacío).
Doc: docs/estilo_noir_color.md § «Variante FEUDAL» (reparto). Ejemplo: videos/got_joffrey/.
"""
import math

import numpy as np

import noir_color as NC
from motor import clamp01
from noir import gris
from noir_pers import _ik
from toon import blob, eje_curvo, elipse_, suave, tubo

NC.RAMPAS.update({
    "purpura": [(0.00, (0.030, 0.010, 0.040)), (0.25, (0.200, 0.050, 0.260)), (0.55, (0.480, 0.200, 0.540)),
                (0.80, (0.720, 0.500, 0.780)), (1.00, (0.950, 0.850, 0.970))],
    "azul": [(0.00, (0.015, 0.020, 0.040)), (0.28, (0.080, 0.130, 0.250)), (0.58, (0.300, 0.400, 0.560)),
             (1.00, (0.880, 0.900, 0.950))],
    "armino": [(0.00, (0.030, 0.030, 0.040)), (0.40, (0.420, 0.400, 0.380)), (0.75, (0.850, 0.820, 0.760)),
               (1.00, (1.000, 0.980, 0.940))],
})

TINTA = (14, 12, 16)


def _rot(P, a, c=(0.0, 0.0)):
    P = np.asarray(P, float).reshape(-1, 2)
    if a == 0:
        return P
    c = np.asarray(c, float)
    ca, sa = math.cos(a), math.sin(a)
    Q = P - c
    return np.stack([Q[:, 0] * ca - Q[:, 1] * sa, Q[:, 0] * sa + Q[:, 1] * ca], 1) + c


class _Rasgos:
    DEF = dict(pelo="corto", pelo_rampa="lana", pelo_tono=60, barba=None, corona=None, toca=False, edad=0.0, joven=False,
               fem=False, nariz="recta", ropa=("lana", 90), capa=None, piel=124, collar=0, falta=-1, cuello="alto",
               barba_tono=None)

    def __init__(self, sem=0, **kw):
        self.sem = sem
        self.r = dict(self.DEF)
        self.r.update(kw)


class BustoCorte(_Rasgos):
    """Primer plano de perfil a la derecha (cara de ~360 px con s=1; x, y = centro de la cara). p: x, y, s, d, luz, rim,
    boca 0..1, ojo 0..1 (cerrado..abierto), mira -1..1 (abajo..arriba), adelante (pupila hacia delante/atrás), ceño 0..1,
    sonrisa -1..1, ahogo 0..1, manos_cuello 0..1, cab_rot (inclina la cabeza), hombros (False = solo la cabeza)."""

    def _T(self, p):
        x, y, s, d = p["x"], p["y"], p["s"], p.get("d", 1)
        a = p.get("cab_rot", 0.0)
        tiemb = p.get("ahogo", 0.0)
        jx = tiemb * 6 * math.sin(p.get("_t", 0.0) * 41.0 + self.sem)
        jy = tiemb * 4 * math.cos(p.get("_t", 0.0) * 37.0)

        def f(P):
            P = _rot(P, a, (0, 120)) + (jx, jy)
            return np.stack([x + d * s * P[:, 0], y + s * P[:, 1]], 1)
        return f

    def _T0(self, p):
        x, y, s, d = p["x"], p["y"], p["s"], p.get("d", 1)

        def f(P):
            P = np.asarray(P, float).reshape(-1, 2)
            return np.stack([x + d * s * P[:, 0], y + s * P[:, 1]], 1)
        return f

    def boca(self, p):
        return self._T(dict(p, _t=0))(np.array([[150.0, 62.0]]))[0]

    def cuello_pos(self, p):
        return self._T0(p)(np.array([[40.0, 200.0]]))[0]

    def dibujar(self, h, p):
        p = dict(p)
        p["_t"] = h.t
        if p.get("hombros", True):
            self._hombros(h, p)
        self.cabeza(h, p)
        if p.get("manos_cuello", 0.0) > 0:
            self._manos_cuello(h, p)

    # ------------------------------------------------------------------ ropa, cuello y collar
    def _hombros(self, h, p):
        r = self.r
        T = self._T0(p)
        s = p["s"]
        sem = self.sem
        L = p.get("luz", (0.8, -0.6))
        rim = p.get("rim", 0.9)
        w = 9.0 * s
        resp = 0.5 + 0.5 * math.sin(h.t * 1.3 + sem)
        dy = -6 * resp - 14 * p.get("ahogo", 0.0) * abs(math.sin(h.t * 9.0))

        def pz(P, tono, sm, rampa=None, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", 40 * s), rampa=rampa, **kw)
        if r["pelo"] in ("largo", "trenza") and not r["toca"]:
            self._pelo_atras(h, p, T, pz)
        if r["capa"]:
            pz(suave([(-520, 640), (-400, 230 + dy), (-200, 180 + dy), (40, 186 + dy), (280, 240 + dy), (470, 420), (540, 640)], 5),
               r["capa"][1], 1, rampa=r["capa"][0], d=60 * s, trama=0.7)
        rp, tn = r["ropa"]
        ancho = 0.82 if r["fem"] else 1.0
        cuerpo = [(-470 * ancho, 640), (-330 * ancho, 228 + dy), (-170, 176 + dy), (60, 182 + dy), (250, 236 + dy),
                  (400 * ancho, 430), (470 * ancho, 640)]
        pz(suave(cuerpo, 5), tn, 2, rampa=rp, d=56 * s, trama=0.65)
        for a in (((-260, 330), (-240, 480), (-260, 640)), ((240, 340), (270, 480), (290, 640))):
            h.trazo(T(np.array(a, float)), 3.5 * s, sem + 3, color=TINTA, alfa=0.55)
        # cuello de piel
        pz([(-74, 50), (76, 110), (70, 214), (-88, 210)], r["piel"] - 30, 4, rampa="piel", d=30 * s, trama=0.6)
        if r["cuello"] == "escote":
            pz(suave([(-90, 178 + dy), (110, 188 + dy), (150, 310), (40, 360), (-80, 310)], 4), r["piel"] - 12, 5, rampa="piel",
               w=w * 0.6, d=20 * s, trama=0.3)
            with h.con_rampa("oro"):
                h.trazo(T(suave([(-100, 184 + dy), (-80, 310), (40, 368), (156, 310), (120, 192 + dy)], 6, cerrado=False)), 5 * s,
                        sem + 6, color=h.c(150, "oro"), alfa=0.9)
        else:
            pz([(-100, 178 + dy), (112, 190 + dy), (130, 246 + dy), (-104, 238 + dy)], tn - 25, 5, rampa=rp, w=w * 0.7, d=12 * s,
               trama=0.4)
            h.trazo(T([(-100, 184 + dy), (114, 194 + dy)]), 4 * s, sem + 6, color=h.c(150, "oro"), alfa=0.85)
        if r["capa"] and r["corona"] == "rey":                          # armiño sobre los hombros del rey
            pz(suave([(-420, 300), (-300, 210 + dy), (-100, 220 + dy), (120, 230 + dy), (300, 270 + dy), (420, 360), (300, 360),
                      (100, 300), (-120, 290), (-320, 320)], 4), 210, 7, rampa="armino", w=w * 0.7, d=18 * s, trama=0.3)
            rng = np.random.default_rng(sem)
            for _ in range(14):
                q = np.array([rng.uniform(-380, 360), rng.uniform(250, 300)])
                h.trazo(T(np.array([q, q + (4, 16)])), 5 * s, sem + 8, color=TINTA, alfa=0.85, taper=(0.1, 0.9))
        if r["collar"]:
            self._collar(h, p, T, dy)
        p["_dy"] = dy

    def _collar(self, h, p, T, dy):
        r = self.r
        s = p["s"]
        n = int(r["collar"])
        a = np.linspace(0.08, 0.92, n)
        cad = [(-70 + 230 * u, 194 + dy + 120 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 30)]
        h.trazo(T(np.array(cad)), 4.0 * s, self.sem + 9, color=h.c(170, "oro"), alfa=0.95)
        self._piedras = []
        for i, u in enumerate(a):
            c = np.array([-70 + 230 * u, 194 + dy + 120 * math.sin(math.pi * u) + 14])
            self._piedras.append(T(c[None])[0])
            h.pieza(T(elipse_(c[0], c[1], 17, 20, n=16)), 150, self.sem + 10 + i, w=3 * s, luz=p.get("luz", (0.8, -0.6)), d=4 * s,
                    trama=0, rim=0.8, rampa="oro")
            if i == r["falta"] and p.get("falta", True):
                h.pieza(T(elipse_(c[0], c[1], 10, 12, n=12)), 18, self.sem + 30 + i, w=2 * s, d=0, sombra=0, rim=0, rampa="oro")
                continue
            h.pieza(T(elipse_(c[0], c[1], 12, 14, n=14)), 70, self.sem + 50 + i, w=2 * s, luz=p.get("luz", (0.8, -0.6)), d=3 * s,
                    trama=0, rim=0.9, rampa="purpura")
            h.disco(*T(np.array([[c[0] + 4, c[1] - 5]]))[0], 3.0 * s, (235, 215, 240))

    def piedras(self):
        return getattr(self, "_piedras", [])

    def _pelo_atras(self, h, p, T, pz):
        r = self.r
        s = p["s"]
        largo = 520 if r["pelo"] == "largo" else 600
        mov = 10 * math.sin(h.t * 0.9 + self.sem)
        P = [(-60, -200), (-170, -150), (-210, 0), (-240, 200), (-250 + mov, largo - 120), (-200 + mov, largo), (-90, largo - 40),
             (-60, 300), (-40, 120)]
        pz(suave(P, 5), r["pelo_tono"] - 10, 11, rampa=r["pelo_rampa"], w=7 * s, d=30 * s, trama=0.5)
        for k in range(7):
            x0 = -200 + k * 22
            h.trazo(T(suave([(x0 + 40, -120), (x0 - 10, 100), (x0 + mov * 0.6, largo - 80)], 6, cerrado=False)), 2.2 * s,
                    self.sem + 12 + k, color=TINTA, alfa=0.45)

    # ------------------------------------------------------------------ cabeza (también la usa Cortesano a escala)
    def cabeza(self, h, p):
        r = self.r
        T = self._T(p)
        s = p["s"]
        sem = self.sem
        L = p.get("luz", (0.8, -0.6))
        rim = p.get("rim", 0.9)
        w = 9.0 * s
        dd = 46 * s
        boca = clamp01(p.get("boca", 0.0) + 0.9 * p.get("ahogo", 0.0))
        ah = p.get("ahogo", 0.0)
        ed = r["edad"]
        fem = r["fem"] or r["joven"]

        def pz(P, tono, sm, rampa=None, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", dd), rampa=rampa, **kw)
        if r["toca"]:                                                   # velo de la anciana: cae por la espalda
            pz(suave([(-60, -230), (-200, -170), (-250, 40), (-270, 380), (-90, 420), (-60, 160)], 5), 186, 60, rampa="lana",
               d=30 * s, trama=0.55)
        if not p.get("hombros", True) and r["pelo"] in ("largo", "trenza") and not r["toca"]:
            self._pelo_atras(h, p, T, pz)
        # nariz
        if r["nariz"] == "aguileña":
            nz = [(128, -48), (156, -20), (190, 12), (148, 24)]
        elif r["nariz"] == "pequeña" or fem:
            nz = [(128, -48), (150, -16), (170, 10), (140, 22)]
        else:
            nz = [(128, -48), (152, -18), (182, 10), (142, 22)]
        ch = 0.9 if fem else 1.0
        b = boca
        cab = [(-150, -60), (-138, -130), (-60, -190), (40, -186), (96, -150), (124, -86), (116, -62)] + nz + \
              [(138, 40), (150, 52 + 4 * b), (136, 61 + 14 * b), (145, 72 + 26 * b), (128, 88 + 28 * b), (142 * ch, 118 + 30 * b),
               (110 * ch, 152 + 24 * b + 10 * ed), (30, 142 + 10 * ed), (-36, 102), (-74, 58), (-112, 36)]
        pz(suave(cab, 4), r["piel"], 20, rampa="piel", trama=0.5)
        if ah > 0.02:                                                   # se amorata
            h.pieza(T(suave(cab, 4)), 120, sem + 21, w=0, luz=L, d=dd, sombra=0.3, trama=0, rim=0, alfa=0.78 * ah, linea=False,
                    rampa="purpura")
        # oreja
        if r["pelo"] in ("corto", "calvo", "trenza") and not r["toca"]:
            pz(suave([(-36, -50), (-6, -64), (6, -30), (-4, 10), (-30, 14)], 3), r["piel"] - 14, 22, rampa="piel", w=w * 0.6,
               d=10 * s, trama=0.3)
            h.trazo(T([(-20, -40), (-6, -24), (-18, 2)]), 2.4 * s, sem + 23, color=TINTA, alfa=0.6)
        # boca: labios, comisura y la sombra de la boca abierta
        so = p.get("sonrisa", 0.0)
        if b > 0.15:
            pz(suave([(118, 58 + 2 * b), (146, 56 + 4 * b), (142, 66 + 22 * b), (120, 70 + 16 * b)], 3), 18, 24, rampa="piel", w=w * 0.4,
               d=0, sombra=0, rim=0)
        h.trazo(T([(112, 64 - 6 * so + 3 * b), (146, 60 + 4 * b)]), 4.2 * s, sem + 25, color=TINTA, alfa=0.95)
        if fem and not ed:
            h.trazo(T([(138, 46), (150, 54 + 4 * b)]), 3 * s, sem + 26, color=h.c(90, "vino"), alfa=0.6)
        # arrugas de la edad
        if ed > 0:
            for a in (((96, 30), (110, 60), (106, 90)), ((40, -40), (70, -30)), ((60, -110), (100, -112)), ((50, -128), (96, -132)),
                      ((70, 100), (100, 120))):
                h.trazo(T(np.array(a, float)), 2.4 * s, sem + 27, color=TINTA, alfa=0.45 * ed)
        # ojo, pupila, párpado y ceja
        oy = -70
        ojo = clamp01(p.get("ojo", 1.0)) * (0.0 if self._parpadeo(h.t) else 1.0)
        abre = 1.0 + 0.8 * ah
        if ojo > 0.15:
            pz(suave([(76, oy - 4 * abre), (96, oy - 11 * abre), (114, oy - 2), (96, oy + 7 * abre)], 3), 228, 28, rampa="neutro",
               w=w * 0.45, d=2, sombra=0, trama=0, rim=0)
            mx = 3 * p.get("adelante", 1.0)
            my = -4 * p.get("mira", 0.0)
            h.disco(*T([[99 + mx, oy - 2 + my]])[0], (5.5 - 2.0 * ah) * s, gris(12))
            h.disco(*T([[101 + mx, oy - 4 + my]])[0], 1.8 * s, gris(250))
            h.trazo(T([(76, oy - 4 * abre), (96, oy - 12 * abre), (114, oy - 3)]), 3.4 * s, sem + 29, color=TINTA, alfa=0.95)
            if fem:
                for k in range(3):
                    h.trazo(T([(100 + k * 6, oy - 12), (106 + k * 7, oy - 20)]), 1.8 * s, sem + 30 + k, color=TINTA, alfa=0.8)
        else:
            h.trazo(T([(78, oy), (96, oy + 5), (112, oy)]), 3.2 * s, sem + 29, color=TINTA, alfa=0.95)
        ce = p.get("ceño", 0.0)
        h.trazo(T([(66, oy - 28 + 4 * ce - 8 * ah), (98, oy - 34 + 2 * ce - 10 * ah), (124, oy - 22 + 8 * ce - 6 * ah)]),
                (5.0 if fem else 7.0) * s, sem + 33, color=TINTA, alfa=0.95, taper=(0.2, 0.6))
        h.trazo(T([(74, oy + 10), (100, oy + 14)]), 2.0 * s, sem + 34, color=TINTA, alfa=0.5)
        # barba
        bt = r["barba_tono"] if r["barba_tono"] is not None else r["pelo_tono"]
        if r["barba"] == "perilla":
            pz(suave([(100, 84 + 28 * b), (146, 80 + 28 * b), (150, 126 + 30 * b), (120, 168 + 26 * b), (96, 130 + 26 * b)], 3), bt, 35,
               rampa=r["pelo_rampa"], w=w * 0.6, d=10 * s, trama=0.4, rim=0.5)
            pz(suave([(108, 50), (152, 48), (156, 58), (116, 60)], 3), bt, 36, rampa=r["pelo_rampa"], w=w * 0.4, d=4 * s, trama=0, rim=0.4)
        elif r["barba"] == "corta":
            pz(suave([(-10, 40), (40, 70), (110, 74 + 20 * b), (150, 84 + 26 * b), (148, 124 + 30 * b), (120, 162 + 26 * b),
                      (60, 176 + 20 * b), (0, 160), (-40, 110)], 4), bt, 35, rampa=r["pelo_rampa"], w=w * 0.6, d=16 * s, trama=0.5,
               rim=0.5)
        elif r["barba"] == "rala":
            rng = np.random.default_rng(sem)
            for _ in range(70):
                q = np.array([rng.uniform(0, 140), rng.uniform(60, 150)])
                h.disco(*T(q[None])[0], 1.3 * s, TINTA)
        # pelo
        pr, pt = r["pelo_rampa"], r["pelo_tono"]
        mov = 6 * math.sin(h.t * 0.8 + sem)
        if r["toca"]:
            pz(suave([(-170, -30), (-160, -160), (-70, -236), (60, -238), (130, -170), (126, -112), (80, -140), (10, -152),
                      (-60, -120), (-100, -40), (-120, 40)], 4), 196, 61, rampa="lana", d=24 * s, trama=0.5)
            pz(suave([(-110, 40), (-60, 120), (30, 150 + 10 * b), (112, 160 + 24 * b), (150, 140 + 30 * b), (154, 190), (120, 250),
                      (-40, 250), (-130, 160)], 4), 206, 62, rampa="lana", d=20 * s, trama=0.4)
            h.trazo(T([(-100, -60), (-130, 60), (-110, 180)]), 2.6 * s, sem + 63, color=TINTA, alfa=0.5)
            h.trazo(T([(90, -150), (40, -160), (-20, -150)]), 2.6 * s, sem + 64, color=TINTA, alfa=0.5)
        elif r["pelo"] == "corto":
            P = [(-158, -40), (-150, -140), (-70, -214), (40, -214), (110, -172), (128, -128), (104, -136 + mov * 0.3), (60, -150),
                 (10, -146), (-30, -120), (-50, -60), (-64, -10), (-100, 30), (-130, 20)]
            pz(suave(P, 4), pt, 40, rampa=pr, w=w * 0.8, d=16 * s, trama=0.45)
            for k in range(6):
                x0 = -120 + k * 38
                h.trazo(T(suave([(x0, -196 + abs(k - 3) * 8), (x0 - 20, -150), (x0 - 46, -90)], 5, cerrado=False)), 2.0 * s,
                        sem + 41 + k, color=TINTA, alfa=0.45)
        elif r["pelo"] in ("melena", "largo", "trenza"):
            P = [(-160, -30), (-156, -150), (-74, -222), (40, -220), (114, -176), (134, -126), (110, -132), (60, -160),
                 (0, -150), (-40, -110), (-60, -40), (-70, 40), (-90 + mov, 160 if r["pelo"] == "melena" else 120),
                 (-150 + mov, 170), (-170, 60)]
            pz(suave(P, 4), pt, 40, rampa=pr, w=w * 0.8, d=16 * s, trama=0.45)
            for k in range(6):
                x0 = -130 + k * 34
                h.trazo(T(suave([(x0 + 30, -200), (x0, -120), (x0 - 20 + mov, 90)], 6, cerrado=False)), 2.0 * s, sem + 41 + k,
                        color=TINTA, alfa=0.42)
        elif r["pelo"] == "calvo":
            pz(suave([(-158, -40), (-150, -100), (-120, -96), (-90, 20), (-130, 30)], 3), pt, 40, rampa=pr, w=w * 0.6, d=8 * s,
               trama=0.3)
        # corona o diadema
        if r["corona"] == "rey":
            base = [(-150, -132), (128, -150)]
            pts = [(-150, -132)]
            for k in range(6):
                u0, u1 = k / 6, (k + 0.5) / 6
                xa = -150 + 278 * u0
                xb = -150 + 278 * u1
                ya = -132 - 18 * u0
                pts += [(xa, ya - 44), (xb, ya - 92 - 6 * (k % 2)), (xa + 278 / 6, ya - 44 - 3)]
            pts += [(128, -150), (128, -196), (-150, -176)]
            P = [(-150, -132), (128, -150), (128, -196)] + [(x, y) for x, y in pts[1:-3]][::-1] + [(-150, -176)]
            pz(P, 158, 70, rampa="oro", w=w * 0.7, d=10 * s, trama=0.3, rim=1.0)
            pz([(-150, -132), (128, -150), (128, -168), (-150, -152)], 120, 71, rampa="oro", w=w * 0.5, d=4 * s, trama=0, rim=0.8)
            for k, gx in enumerate((-100, -20, 60)):
                gy = -142 - (gx + 150) * 0.065
                pz(elipse_(gx, gy, 11, 9, n=12), 120, 72 + k, rampa="estandarte", w=w * 0.3, d=2, trama=0, rim=0.9)
                h.disco(*T([[gx + 3, gy - 3]])[0], 2.4 * s, (250, 230, 210))
        elif r["corona"] == "diadema":
            pz([(-150, -128), (126, -150), (128, -136), (-150, -114)], 160, 70, rampa="oro", w=w * 0.4, d=4 * s, trama=0, rim=1.0)
            pz(elipse_(120, -146, 10, 12, n=12), 140, 71, rampa="purpura" if r.get("joya") == "purpura" else "estandarte",
               w=w * 0.3, d=2, trama=0, rim=0.9)

    def _parpadeo(self, t):
        u = (t * 0.31 + self.sem * 0.137) % 1.0
        return u < 0.03

    def _manos_cuello(self, h, p):
        T = self._T0(p)
        s = p["s"]
        k = clamp01(p["manos_cuello"])
        r = self.r
        L = p.get("luz", (0.8, -0.6))
        for i, (bx, by) in enumerate(((-150, 520), (250, 540))):
            hx, hy = (10 + 70 * i, 176 + 16 * i)
            mano = np.array([bx + (hx - bx) * k, by + (hy - by) * k])
            codo = (np.array([bx, by]) + mano) / 2 + (-30 + 60 * i, 20)
            ropa_r, ropa_t = r["ropa"]
            h.pieza(T(tubo(np.vstack([eje_curvo((bx, by), codo, 0, 8), eje_curvo(codo, mano, 0, 8)[1:]]), 92, 62)), ropa_t - 10,
                    self.sem + 80 + i, w=8 * s, luz=L, d=24 * s, trama=0.5, rim=0.8, rampa=ropa_r)
            sh = math.sin(h.t * 23 + i) * 4 * k
            h.pieza(T(blob(mano[0] + sh, mano[1], 50, 34, rad=[1, 1.1, 1.0, 0.9, 0.85, 0.95, 1.05, 1.1], n=8)), r["piel"] - 8,
                    self.sem + 82 + i, w=7 * s, luz=L, d=12 * s, trama=0.3, rim=0.8, rampa="piel")
            for f in range(4):
                q = mano + (-30 + f * 18 + sh, -20)
                h.trazo(T(np.array([q, q + (6, 34)])), 3 * s, self.sem + 84 + f, color=TINTA, alfa=0.8)


class Cortesano(_Rasgos):
    """Cuerpo entero de perfil 3/4 a la derecha (pies en y, ~540 px de alto con s=1): túnica larga o jubón, capa, cinturón,
    brazos con codo (IK), y la cabeza de BustoCorte a escala. Rasgos extra: alto (0.62 = enano: cuerpo corto, cabeza igual),
    baston (p["baston_mano"]="atras" lo pasa a la otra mano), bufon (traje de remiendos). p: x, y, s, d, luz, rim, mano=(x, y) local de la mano delantera (None = colgando),
    mano2 (la de atrás), rot (giro de todo el cuerpo sobre los pies: caer), andar 0..1, paso (fase), cab (dict extra para la
    cabeza: boca, ceño, sonrisa, ahogo, mira...), inclina (reverencia)."""

    DEF = dict(_Rasgos.DEF, alto=1.0, baston=False, bufon=False)

    def __init__(self, sem=0, **kw):
        super().__init__(sem, **kw)
        self.busto = BustoCorte(sem, **{k: v for k, v in self.r.items() if k in _Rasgos.DEF})

    def _T(self, p):
        x, y, s, d = p["x"], p["y"], p["s"], p.get("d", 1)
        a = p.get("rot", 0.0)
        inc = p.get("inclina", 0.0)

        def f(P):
            P = np.asarray(P, float).reshape(-1, 2)
            P = np.stack([P[:, 0] - inc * P[:, 1] * 0.25, P[:, 1]], 1)
            P = _rot(P, a)
            return np.stack([x + d * s * P[:, 0], y + s * P[:, 1]], 1)
        return f

    def puntos(self, p):
        """Posiciones de mundo útiles: mano delantera, hombro, cabeza (para colocar copas, espadas, luces)."""
        T = self._T(p)
        al = self.r["alto"]
        return dict(mano=T(np.array([self._mano(p, al)]))[0], cabeza=T(np.array([[8, -470 * al - 30 * (1 - al)]]))[0])

    def _mano(self, p, al):
        m = p.get("mano")
        if m is None:
            return (34.0, -230.0 * al)
        return tuple(m)

    def dibujar(self, h, p):
        r = self.r
        T = self._T(p)
        s = p["s"]
        sem = self.sem
        al = r["alto"]
        L = p.get("luz", (0.4, -1.0))
        rim = p.get("rim", 0.9)
        w = 6.5 * s
        and_ = p.get("andar", 0.0)
        bob = -4 * and_ * abs(math.cos(p.get("paso", 0.0))) - 1.6 * (1 - and_) * (0.5 + 0.5 * math.sin(h.t * 1.5 + sem))

        def pz(P, tono, sm, rampa=None, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", 18 * s), rampa=rampa, **kw)
        rp, tn = r["ropa"]
        top = -410 * al + bob
        hombro = (26.0, top + 16)
        cint = top + 150 * al ** 0.8
        sw = 10 * math.sin(h.t * 1.1 + sem)
        # capa detrás
        if r["capa"]:
            pz(suave([(-50, top - 4), (40, top - 6), (30, top + 60), (-60 + sw, -10), (-110 + sw, 0), (-130 + sw * 1.4, -40),
                      (-80, top + 80)], 5), r["capa"][1], 1, rampa=r["capa"][0], d=24 * s, trama=0.6)
        # brazo de atrás
        m2 = p.get("mano2")
        S2 = np.array([-34.0, top + 18])
        H2 = np.array(m2 if m2 is not None else (-40.0 + 4 * sw * 0.2, top + 170 * al ** 0.7))
        E2 = _ik(S2, H2, 82 * al ** 0.6, 80 * al ** 0.6, -1)
        pz(tubo(np.vstack([eje_curvo(S2, E2, 0, 8), eje_curvo(E2, H2, 0, 8)[1:]]), 28, 22, 30), tn - 24, 2, rampa=rp)
        pz(blob(H2[0], H2[1] + 6, 11, 13, n=8), r["piel"] - 10, 3, rampa="piel", d=4 * s, trama=0)
        # pies que asoman al andar
        for k in (0, 1):
            ph = p.get("paso", 0.0) + math.pi * k
            fx = 26 * and_ * math.sin(ph) + (8 if k else -8)
            pz(blob(fx + 18, -8, 26, 10, n=8), 20 + 10 * k, 4 + k, rampa="cuero", d=4 * s, trama=0)
        # túnica (hasta el suelo; las damas, más acampanada)
        acamp = 1.25 if r["fem"] else 1.0
        if r["bufon"]:
            tun = [(-52, top), (40, top - 4), (58, top + 40), (54, cint), (70, -150 * al), (60, -40), (-70, -40), (-74, -150 * al),
                   (-60, cint), (-64, top + 40)]
        else:
            tun = [(-58, top + 14), (-36, top - 2), (24, top - 6), (50, top + 6), (62, top + 44), (54, cint), (74 * acamp, -120 * al), (92 * acamp + sw * 0.3, -6),
                   (-96 * acamp + sw * 0.3, -6), (-80 * acamp, -120 * al), (-64, cint), (-68, top + 44)]
        pz(suave(tun, 5), tn, 6, rampa=rp, w=w * 1.1, d=24 * s, trama=0.6)
        if r["bufon"]:                                      # remiendos en damero y piernas a rayas
            for k in range(6):
                yy = top + 30 + k * 50 * al
                if yy > -60:
                    break
                xx = -50 + (k % 2) * 50
                pz([(xx, yy), (xx + 50, yy - 2), (xx + 48, yy + 48 * al), (xx - 2, yy + 48 * al)], 150, 30 + k, rampa="oro", w=w * 0.4,
                   d=4 * s, trama=0, rim=0.4)
            for k in (0, 1):
                lx = -24 + 40 * k
                pz(tubo(np.array([[lx, -40], [lx, -8]], float), 26, 22), 60 + 80 * k, 40 + k, rampa="estandarte", d=4 * s, trama=0)
        # pliegues, cinturón, ribete
        for a in (((-20, cint + 20), (-30 + sw * 0.2, -120 * al), (-40 + sw * 0.3, -10)),
                  ((24, cint + 20), (34 + sw * 0.2, -120 * al), (48 + sw * 0.3, -10))):
            h.trazo(T(np.array(a, float)), 2.4 * s, sem + 7, color=TINTA, alfa=0.6)
        pz([(-62, cint - 8), (54, cint - 8), (56, cint + 10), (-63, cint + 10)], 40, 8, rampa="cuero", w=w * 0.5, d=3 * s, trama=0,
           rim=0.6)
        h.trazo(T([(-52, top + 4), (40, top)]), 3.5 * s, sem + 9, color=h.c(150, "oro"), alfa=0.85)
        if r["capa"] and r["corona"] == "rey":
            pz(suave([(-60, top - 8), (44, top - 10), (50, top + 22), (-64, top + 26)], 3), 210, 10, rampa="armino", w=w * 0.5, d=6 * s,
               trama=0.2)
        if r["collar"]:
            for i in range(int(r["collar"])):
                u = (i + 0.5) / r["collar"]
                c = (-30 + 64 * u, top + 12 + 22 * math.sin(math.pi * u))
                if i == r["falta"] and p.get("falta", True):
                    continue
                h.pieza(T(elipse_(c[0], c[1], 4.5, 5.5, n=10)), 70, sem + 11 + i, w=1.5 * s, d=1, trama=0, rim=0.8, rampa="purpura")
        # cabeza (BustoCorte a escala; cara de ~95 px)
        hs = 0.27 * s * (1.0 if al > 0.8 else 1.08)
        cab_c = T(np.array([[8.0, top - 66]]))[0]
        q = dict(p.get("cab", {}))
        q.update(x=cab_c[0], y=cab_c[1], s=hs, d=p.get("d", 1), luz=L, rim=rim, hombros=False, _t=h.t,
                 cab_rot=q.get("cab_rot", 0.0) + p.get("rot", 0.0) * p.get("d", 1))
        pz([(-10, top - 30), (12, top - 26), (14, top + 4), (-12, top + 4)], r["piel"] - 40, 12, rampa="piel", w=w * 0.6, d=6 * s, trama=0.4)
        self.busto.cabeza(h, q)
        # brazo delantero (con la mano donde diga la pose)
        Hd = np.array(self._mano(p, al), float)
        S = np.array(hombro)
        E = _ik(S, Hd, 84 * al ** 0.6, 84 * al ** 0.6, 1)
        pz(tubo(np.vstack([eje_curvo(S, E, 0, 8), eje_curvo(E, Hd, 0, 8)[1:]]), 29, 22, 31), tn - 6, 13, rampa=rp)
        pz(blob(Hd[0] + 4, Hd[1], 13, 12, n=8), r["piel"], 14, rampa="piel", d=4 * s, trama=0)
        if r["baston"]:                                     # p["baston_mano"] = "atras": lo lleva la otra mano (la delantera trabaja)
            B = H2 if p.get("baston_mano") == "atras" else Hd
            pz(tubo(np.array([[B[0] + 6, B[1] - 20], [B[0] + 22, -2]], float), 9, 7), 70, 15, rampa="madera", d=3 * s, trama=0)
            pz(elipse_(B[0] + 6, B[1] - 24, 14, 10, n=12), 160, 16, rampa="oro", d=2 * s, trama=0)


def comensales(h, t, x0, x1, y, n=10, s=1.0, sem=0, reaccion=0.0, mira_x=None, luz=(0.2, -1.0), copas=True):
    """Fila de invitados sentados detrás de una mesa (y = canto de la mesa): bustos simplificados con tocados variados, cada uno
    con su ritmo (charlan, beben, giran la cabeza). reaccion 0..1: se levantan y miran hacia mira_x (el rey que cae)."""
    rng = np.random.default_rng(sem)
    tocados = ["pelo", "toca", "gorro", "calvo", "diadema", "pelo_largo", "capucha"]
    ropas = [("estandarte", 90), ("tela_verde", 90), ("azul", 100), ("lana", 100), ("purpura", 80), ("cuero", 90), ("oro", 110)]
    xs = np.linspace(x0, x1, n)
    for i, x in enumerate(xs):
        x = x + rng.uniform(-20, 20)
        ss = s * rng.uniform(0.9, 1.08)
        fase = rng.uniform(0, 10)
        ritmo = rng.uniform(0.6, 1.4)
        lev = reaccion * clamp01(1.4 - rng.uniform(0, 0.8)) * 70 * ss
        mira = 0.0 if mira_x is None else (1.0 if mira_x > x else -1.0)
        giro = reaccion * mira * 14 + (1 - reaccion) * 8 * math.sin(t * 0.5 * ritmo + fase)
        bob = 3 * math.sin(t * 2.2 * ritmo + fase) * (1 - reaccion)
        yb = y - lev + bob
        rp, tn = ropas[int(rng.integers(len(ropas)))]
        tono = tn + rng.uniform(-15, 15)
        tor = suave([(-62, 0), (-56, -70), (-30, -96), (30, -96), (56, -70), (62, 0)], 4)
        P = np.asarray(tor) * ss + (x, yb + 40 * ss)
        tr = 0.5 if ss > 0.7 else 0.0                                           # los lejanos sin tramado (cuestan y no se ve)
        h.pieza(P, tono, sem + i * 7, w=5 * ss, luz=luz, d=14 * ss, trama=tr, rim=0.8, rampa=rp)
        cx, cy = x + giro * ss, yb - 84 * ss
        h.pieza(elipse_(cx, cy, 24 * ss, 28 * ss, n=20), 118 + rng.uniform(-10, 14), sem + i * 7 + 1, w=4 * ss, luz=luz, d=10 * ss,
                trama=0.3 if ss > 0.7 else 0.0, rim=0.8, rampa="piel")
        dirx = 1 if giro >= 0 else -1
        h.pieza([(cx + dirx * 20 * ss, cy - 4 * ss), (cx + dirx * 32 * ss, cy + 6 * ss), (cx + dirx * 20 * ss, cy + 10 * ss)], 110,
                sem + i * 7 + 2, w=2.4 * ss, luz=luz, d=2, trama=0, rim=0.5, rampa="piel")
        tc = tocados[int(rng.integers(len(tocados)))]
        pt = rng.uniform(40, 150)
        prp = ["lana", "oro", "cuero", "personaje"][int(rng.integers(4))]
        if tc in ("pelo", "pelo_largo"):
            larg = 40 if tc == "pelo_largo" else 6
            h.pieza(suave([(cx - 27 * ss, cy + larg * ss), (cx - 28 * ss, cy - 18 * ss), (cx, cy - 32 * ss), (cx + 26 * ss, cy - 20 * ss),
                           (cx + 20 * ss, cy - 10 * ss), (cx - 10 * ss, cy - 12 * ss), (cx - 16 * ss, cy + larg * ss)], 3), pt,
                    sem + i * 7 + 3, w=3 * ss, luz=luz, d=6 * ss, trama=0.3, rim=0.6, rampa=prp)
        elif tc == "toca":
            h.pieza(suave([(cx - 30 * ss, cy + 30 * ss), (cx - 32 * ss, cy - 20 * ss), (cx, cy - 36 * ss), (cx + 30 * ss, cy - 22 * ss),
                           (cx + 26 * ss, cy - 8 * ss), (cx - 14 * ss, cy - 14 * ss), (cx - 18 * ss, cy + 30 * ss)], 3), 196,
                    sem + i * 7 + 3, w=3 * ss, luz=luz, d=6 * ss, trama=0.3, rim=0.6, rampa="lana")
        elif tc == "gorro":
            h.pieza(suave([(cx - 30 * ss, cy - 12 * ss), (cx - 20 * ss, cy - 44 * ss), (cx + 16 * ss, cy - 46 * ss), (cx + 32 * ss, cy - 14 * ss)],
                          3), tono - 20, sem + i * 7 + 3, w=3 * ss, luz=luz, d=6 * ss, trama=0.3, rim=0.6, rampa=rp)
        elif tc == "capucha":
            h.pieza(suave([(cx - 34 * ss, cy + 30 * ss), (cx - 34 * ss, cy - 24 * ss), (cx, cy - 40 * ss), (cx + 32 * ss, cy - 20 * ss),
                           (cx + 28 * ss, cy), (cx - 16 * ss, cy - 18 * ss), (cx - 16 * ss, cy + 30 * ss)], 3), 70, sem + i * 7 + 3,
                    w=3 * ss, luz=luz, d=6 * ss, trama=0.4, rim=0.6, rampa="lana")
        elif tc == "diadema":
            h.pieza(suave([(cx - 27 * ss, cy + 34 * ss), (cx - 28 * ss, cy - 18 * ss), (cx, cy - 32 * ss), (cx + 26 * ss, cy - 20 * ss),
                           (cx + 20 * ss, cy - 10 * ss), (cx - 16 * ss, cy + 34 * ss)], 3), pt, sem + i * 7 + 3, w=3 * ss, luz=luz,
                    d=6 * ss, trama=0.3, rim=0.6, rampa=prp)
            h.trazo([(cx - 26 * ss, cy - 16 * ss), (cx + 22 * ss, cy - 22 * ss)], 3 * ss, sem + i * 7 + 4, color=h.c(170, "oro"))
        # ojos (un punto) y, a veces, la copa que sube a la boca
        h.disco(cx + dirx * 12 * ss, cy - 4 * ss, 2.6 * ss, TINTA)
        if copas and reaccion < 0.5:
            beb = max(0.0, math.sin(t * 0.7 * ritmo + fase * 3)) ** 6
            if i % 2 == 0:
                bx = cx + dirx * (40 - 10 * beb) * ss
                by = y + 10 * ss - beb * 90 * ss
                h.pieza([(bx - 9 * ss, by - 26 * ss), (bx + 9 * ss, by - 26 * ss), (bx + 6 * ss, by - 6 * ss), (bx - 6 * ss, by - 6 * ss)], 150,
                        sem + i * 7 + 5, w=2 * ss, luz=luz, d=2, trama=0, rim=0.9, rampa="oro")
                h.trazo([(bx, by - 6 * ss), (bx, by + 8 * ss)], 3 * ss, sem + i * 7 + 6, color=h.c(140, "oro"))
