# -*- coding: utf-8 -*-
"""«La Cosa»: monstruo morado, peludo y gelatinoso (personaje ORIGINAL del estilo cartoon90): tres ojos distintos, bocaza torcida con dientes
disparejos, bracitos con garras y patas gordas. Igual que Mostacho, se redibuja cada cuadro desde sus parámetros (`DEF`); el cuerpo ondula
como gelatina, el pelo es una franja de picos y las garras/dientes son formas propias.

    c = Cosa(); anclas = c.dibujar(h, pose)          # devuelve puntos útiles en coordenadas del mundo (cabeza, manos, boca, centro)
    A = AnimCosa(x=[...], boca=[...])                # claves por parámetro; cara=[(t, 'miedo'), ...] mezcla caras prefabricadas
"""
import math

import numpy as np

from motor import clamp01, remuestrear, ruido1
from toon import (Pista, bezier2, blob, elipse_, eje_curvo, espinas, ondular, suave, tiembla, tubo, _ease)

MOR = (128, 76, 170)
MOR_S = (84, 46, 124)
VIEN = (186, 146, 222)
VIEN_S = (150, 112, 190)
OSC = (62, 34, 92)
CORN = (238, 226, 188)
GARRA = (44, 30, 54)
DIEN = (244, 236, 196)
DIEN_S = (206, 192, 142)
BOCA_I = (52, 14, 52)
LENG = (222, 82, 118)
LENG_S = (176, 52, 92)
ESCL = (250, 246, 206)
ESCL_S = (214, 206, 156)
TINTA = (24, 18, 26)

DEF = dict(
    x=540.0, y=1690.0, s=1.0, flip=0, rot=0.0, sq=0.0, sesgo=0.0,
    boca=0.1, boca_w=1.0, sonrisa=0.2, lengua=0.0, dientes=1.0, babeo=0.0,
    ojo_t=1.0, pupila=0.5, mira_x=0.0, mira_y=0.0, suelto=0.0, abre=(1.0, 1.0, 1.0), cejas=0.0,
    mano_i=(-300.0, -190.0), mano_d=(300.0, -190.0), curva_i=40.0, curva_d=-40.0, garras=1.0,
    pie_i=(-130.0, 0.0), pie_d=(130.0, 0.0),
    gelatina=1.0, erizo=0.0, tiembla=0.0, sudor=0.0, mareo=0.0, barriga=0.0,
)

CARAS = dict(
    neutro=dict(boca=0.1, boca_w=1.0, sonrisa=0.2, lengua=0, ojo_t=1.0, pupila=0.5, cejas=0.0),
    hambre=dict(boca=0.35, boca_w=1.1, sonrisa=0.5, lengua=0.4, ojo_t=0.95, pupila=0.7, cejas=-0.3, babeo=1.0),
    sorpresa=dict(boca=0.5, boca_w=0.8, sonrisa=-0.1, lengua=0.0, ojo_t=1.3, pupila=0.3, cejas=0.4, babeo=0.0),
    miedo=dict(boca=0.55, boca_w=1.0, sonrisa=-0.7, lengua=0.2, ojo_t=1.45, pupila=0.14, cejas=0.8, babeo=0.0),
    grito=dict(boca=1.0, boca_w=1.2, sonrisa=-0.4, lengua=1.0, ojo_t=1.55, pupila=0.1, cejas=0.9, babeo=0.0),
    timido=dict(boca=0.0, boca_w=0.7, sonrisa=0.55, lengua=0, ojo_t=0.9, pupila=0.75, cejas=0.5),
    feliz=dict(boca=0.45, boca_w=1.15, sonrisa=1.0, lengua=0.3, ojo_t=0.9, pupila=0.7, cejas=0.1),
    mareado=dict(boca=0.2, boca_w=0.9, sonrisa=-0.2, lengua=0.7, ojo_t=1.0, pupila=0.6, cejas=0.2),
    enojo=dict(boca=0.45, boca_w=1.1, sonrisa=-0.5, lengua=0.0, ojo_t=0.95, pupila=0.3, cejas=-0.9),
)


def cara(nombre, u=1.0):
    n, c = CARAS["neutro"], CARAS[nombre]
    return {k: n.get(k, DEF.get(k)) + (c.get(k, n.get(k, 0)) - n.get(k, DEF.get(k))) * u for k in set(n) | set(c)}


class Cosa:
    def __init__(self, sem=0):
        self.sem = sem

    # ------------------------------------------------------------ transformaciones
    def _T(self, p, h):
        sg = -1.0 if p["flip"] else 1.0
        sx, sy = (1 + p["sq"]) * sg, 1 - p["sq"]
        c, s_ = math.cos(p["rot"]), math.sin(p["rot"])
        sc = p["s"]
        tx, ty = (tiembla(h.t, p["tiembla"] * sc, sem=self.sem + 3) if p["tiembla"] > 0 else (0.0, 0.0))
        ox, oy = p["x"] + tx, p["y"] + ty
        sh = p["sesgo"]

        def T(P):
            P = np.asarray(P, float)
            q = np.stack([(P[:, 0] + sh * P[:, 1] * -1.0) * sx, P[:, 1] * sy], 1)
            q = np.stack([q[:, 0] * c - q[:, 1] * s_, q[:, 0] * s_ + q[:, 1] * c], 1) * sc + (ox, oy)
            return q
        return T

    # ------------------------------------------------------------ cuerpo
    def _cuerpo(self, h, p, T, t):
        rad = [1.0, 1.04, 1.1, 1.13, 1.1, 1.02, 0.98, 0.94, 0.9, 0.92, 0.96, 1.0]
        P = blob(0, -340, 300, 340, rad=rad, n=12, sub=7)
        P = remuestrear(P, 9.0, True)[:-1]
        g = p["gelatina"]
        P = ondular(P, 7.0 * g, 5.0, 2 * math.pi * 0.9 * t)
        P = ondular(P, 4.0 * g, 9.0, -2 * math.pi * 1.4 * t + 1.0)
        P = espinas(P, 0.24 + 0.5 * p["erizo"], amp=18 + 12 * p["erizo"], per=3, sem=self.sem + 1)
        h.forma(T(P), MOR, MOR_S, w=11, sem=self.sem + 2, d_sombra=(30, 36), sketch=0.8)
        # barriga clara con gruñidos
        B = blob(0, -230, 188 + 14 * p["barriga"], 200 + 10 * p["barriga"], rad=[1, 1, 1, 1, 1, 1], n=6, sub=8)
        h.forma(T(B), VIEN, VIEN_S, w=0, sem=self.sem + 3, d_sombra=(14, 16), jit=1.6)
        # manchas de pelo oscuro
        for k, (x, y, rx, ry) in enumerate(((-210, -430, 40, 30), (230, -330, 46, 32), (-170, -180, 36, 26), (140, -520, 30, 22))):
            h.forma(elipse_(x, y, rx, ry, n=12), MOR_S, None, w=0, sem=self.sem + 4 + k, alfa=0.6, jit=2.0, tex=0)

    def _patas(self, h, p, T):
        for s in (-1, 1):
            pie = np.array(p["pie_i"] if s < 0 else p["pie_d"], float)
            eje = eje_curvo(np.array([s * 100.0, -140.0]), pie + np.array([0, -30.0]), s * -26, 14)
            h.forma(T(tubo(eje, 150, 120)), MOR, MOR_S, w=10, sem=self.sem + 10 + s)
            F = blob(pie[0] + s * 18, pie[1] - 26, 118, 44, rad=[1, 1.02, 1, 0.96, 1, 1, 1, 1], n=8, sub=8)
            h.forma(T(F), MOR, MOR_S, w=10, sem=self.sem + 12 + s, d_sombra=(10, 14))
            for k in (-1, 0, 1):
                x0 = pie[0] + s * 18 + k * 44 + s * 18
                h.forma(T(np.array([(x0 - 16, pie[1] - 38), (x0, pie[1] - 6), (x0 + 16, pie[1] - 38)])), CORN, None, w=5, sem=self.sem + 14 + k, jit=0.6, tex=0)

    def _brazo(self, h, p, T, s):
        hombro = np.array([s * 250.0, -440.0])
        mano = np.array(p["mano_i"] if s < 0 else p["mano_d"], float)
        curva = p["curva_i"] if s < 0 else p["curva_d"]
        eje = eje_curvo(hombro, mano, curva, 16)
        h.forma(T(tubo(eje, 118, 92)), MOR, MOR_S, w=10, sem=self.sem + 20 + s, d_sombra=(14, 16))
        M = blob(mano[0], mano[1], 80, 74, rad=[1, 1.08, 1, 0.94, 1.04, 1.0, 0.96, 1.05], n=8, sub=8)
        h.forma(T(M), MOR, MOR_S, w=10, sem=self.sem + 22 + s, d_sombra=(10, 12))
        d = mano - hombro
        d = d / (np.hypot(*d) + 1e-9)
        n = np.array([-d[1], d[0]])
        for k in (-1, 0, 1):
            b = mano + d * 60 + n * 38 * k
            L = 66 * p["garras"] * (1.0 if k else 1.2)
            h.forma(T(np.array([b - n * 12, b + d * L + n * k * 6, b + n * 12])), GARRA, None, w=4, sem=self.sem + 24 + k, jit=0.6, tex=0)
        return mano

    # ------------------------------------------------------------ cara
    def _ojo(self, h, p, T, cx, cy, r, iris, k, t):
        tam = p["ojo_t"]
        r = r * tam
        ab = p["abre"][k] if hasattr(p["abre"], "__len__") else p["abre"]
        # parpadeo propio de cada ojo
        per = 3.1 + 0.9 * k
        if ((t + 0.7 * k) % per) < 0.13:
            ab = 0.0
        if ab < 0.06:
            h.trazo(T(np.array([[cx - r, cy], [cx, cy + 8], [cx + r, cy]])), 10, self.sem + 40 + k, taper=(0.2, 0.2), jit=0.8)
            return
        a = np.linspace(0, 2 * math.pi, 36, endpoint=False)
        xs, ys = r * np.cos(a), r * 0.96 * np.sin(a)
        ys = np.clip(ys, -r * 0.96 * (2 * ab - 1), r * 0.96)
        P = np.stack([cx + xs, cy + ys], 1)
        rr = h.forma(T(P), ESCL, ESCL_S, w=9, sem=self.sem + 41 + k, d_sombra=(8, 10), jit=1.4, tex=0.0)
        if rr is None:
            return
        # mirada: cada ojo con su propio desvío (los ojos sueltos escanean por separado)
        sl = p["suelto"]
        mx = p["mira_x"] + sl * math.sin(t * (1.7 + 0.8 * k) + k * 2.0) * 0.8
        my = p["mira_y"] + sl * math.sin(t * (1.3 + 0.6 * k) + k) * 0.5
        pr = r * (0.34 + 0.46 * p["pupila"])
        ix, iy = cx + mx * (r - pr) * 0.85, cy + my * (r - pr) * 0.85
        h.relleno(h.tf(T(elipse_(ix, iy, pr, pr, n=20))), iris, clip=rr, tex=0.0)
        pw = pr * (0.28 + 0.5 * p["pupila"])
        h.relleno(h.tf(T(elipse_(ix, iy, pw, pr * 0.78, n=16))), (20, 12, 22), clip=rr, tex=0.0)
        if p["pupila"] > 0.25:
            h.relleno(h.tf(T(elipse_(ix - pr * 0.3, iy - pr * 0.3, pr * 0.16, pr * 0.16, n=10))), (255, 255, 255), clip=rr, tex=0.0)
        h.anillo(h.tf(T(P)), 9.0, self.sem + 42 + k, jit=0.0)
        if ab < 0.95:
            xs2 = np.linspace(-r, r, 12)
            h.trazo(T(np.stack([cx + xs2, np.full(12, cy - r * 0.96 * (2 * ab - 1))], 1)), 13, self.sem + 43 + k, taper=(0.1, 0.1), jit=0.6)

    def _cara(self, h, p, T, t):
        # cuernos
        for s in (-1, 1):
            C = np.array([(s * 110, -640), (s * 190, -690), (s * 230, -770), (s * 232, -690), (s * 190, -610)])
            h.forma(T(suave(C, 4, True)), CORN, (196, 180, 140), w=8, sem=self.sem + 50 + s, jit=1.0, d_sombra=(8, 10))
        # ojos
        self._ojo(h, p, T, -84, -480, 88, (96, 190, 90), 0, t)
        self._ojo(h, p, T, 124, -520, 56, (236, 150, 56), 1, t)
        self._ojo(h, p, T, 14, -640, 34, (84, 150, 230), 2, t)
        # ceja pesada sobre el ojo grande
        ca = p["cejas"]
        a0 = np.array([-170.0, -590.0 - 28 * ca])
        a1 = np.array([-20.0, -590.0 + 40 * ca - 10])
        h.trazo(T(bezier2(a0, (a0 + a1) / 2 + np.array([0, -24]), a1, 12)), 22, self.sem + 60, taper=(0.2, 0.4), jit=1.0, color=OSC)
        self._boca(h, p, T, t)

    def _boca(self, h, p, T, t):
        ab = p["boca"]
        w = 440.0 * p["boca_w"]
        sonr = p["sonrisa"]
        y0 = -300.0
        hh = 24 + 270 * ab
        # sonrisa torcida: la comisura izquierda más alta
        izq = np.array([-w / 2, y0 - 70 * sonr - 24])
        der = np.array([w / 2, y0 - 70 * sonr + 18])
        n = 18
        if ab < 0.03:
            c = bezier2(izq, np.array([0, y0 + 40 * sonr]), der, n)
            h.trazo(T(c), 12, self.sem + 70, taper=(0.15, 0.15), jit=1.2)
            return
        arr = bezier2(izq, np.array([0, y0 - 20 + 10 * sonr]), der, n)
        aba = bezier2(der, np.array([0, y0 + hh * 1.5]), izq, n)
        Pm = suave(np.vstack([arr, aba[1:-1]]), 3, True)
        r = h.forma(T(Pm), BOCA_I, None, w=11, sem=self.sem + 71, jit=1.4, tex=0.0)
        if r is None:
            return
        # lengua
        if p["lengua"] > 0.03:
            L = blob(30, y0 + hh * 0.95, 130, hh * 0.6 * (0.4 + 0.6 * p["lengua"]) + 26, rad=[1, 1, 1, 1, 1, 1], n=6, sub=8)
            h.relleno(h.tf(T(L)), LENG, clip=r, tex=0.0)
            h.trazo(T(np.array([[30, y0 + hh * 0.4], [34, y0 + hh * 1.0]])), 6, self.sem + 72, color=LENG_S, taper=(0.1, 0.6), jit=0.6)
        # dientes: arriba irregulares (uno roto), abajo menos
        if p["dientes"] > 0.05:
            xs = np.linspace(-w / 2 + 40, w / 2 - 40, 7)
            alt = [58, 82, 46, 0, 74, 52, 90]
            for i, xc in enumerate(xs):
                if alt[i] <= 0:
                    continue
                ly = alt[i] * p["dientes"] * (0.7 + 0.5 * min(1.0, ab * 3))
                tp = np.array([(xc - 32, y0 - 30 + 0.0 * i), (xc + 32, y0 - 24), (xc + 26, y0 + ly), (xc - 26, y0 + ly + 4)])
                h.relleno(h.tf(T(tp)), DIEN, clip=r, tex=0.0)
                h.trazo(T(np.array([[xc - 32, y0 - 24], [xc - 26, y0 + ly]])), 4, self.sem + 73 + i, taper=(0.1, 0.1), jit=0.4)
            xs2 = np.linspace(-w / 2 + 90, w / 2 - 90, 5)
            for i, xc in enumerate(xs2):
                ly = (34 + 22 * (i % 2)) * p["dientes"]
                yb = y0 + hh * 0.78
                tp = np.array([(xc - 26, yb + 20), (xc + 26, yb + 20), (xc + 18, yb - ly), (xc - 18, yb - ly - 6)])
                h.relleno(h.tf(T(tp)), DIEN_S, clip=r, tex=0.0)
        h.anillo(h.tf(T(Pm)), 11.0, self.sem + 74, jit=0.0)
        # baba
        if p["babeo"] > 0.05:
            for k, xk in enumerate((-110, 60, 150)):
                ln = (60 + 90 * p["babeo"]) * (0.7 + 0.3 * math.sin(t * 2.0 + k * 1.7))
                yb = y0 + hh * 0.9 - 6
                h.trazo(T(np.array([[xk, yb], [xk + 4 * math.sin(t * 3 + k), yb + ln]])), 9, self.sem + 76 + k, color=(190, 232, 255), taper=(0.1, 0.5), jit=0.6)
                h.disco(*T(np.array([[xk + 4 * math.sin(t * 3 + k), yb + ln + 6]]))[0], 9, (190, 232, 255), sem=self.sem + 79 + k, w=0)

    def _efectos(self, h, p, T, t):
        if p["sudor"] > 0.03:
            for k in range(5):
                ph = (t * 1.1 + k * 0.23) % 1.0
                side = -1 if k % 2 == 0 else 1
                x0 = side * (260 + 40 * (k // 2))
                y0 = -560 + 80 * (k // 2)
                d = np.array([x0 + side * 140 * ph, y0 - 80 * ph + 520 * ph * ph])
                from toon import gota
                h.forma(T(gota(d[0], d[1], 26 * p["sudor"], ang=side * (0.7 - 1.0 * ph) * 0.5)), (170, 220, 255), (120, 176, 230), w=6, sem=self.sem + 90 + k, jit=0.6, tex=0, d_sombra=(5, 7))
        if p["mareo"] > 0.03:
            for k in range(5):
                a = t * 4.0 + k * 2 * math.pi / 5
                x, y = 0 + 330 * math.cos(a), -790 + 54 * math.sin(a)
                from toon import estrella
                h.forma(T(estrella(x, y, 36, 16, 5, rot=a)), (255, 226, 90), None, w=5, sem=self.sem + 100 + k, jit=0.6, tex=0)

    def anclas(self, pose, h):
        """Puntos útiles (mundo) de una pose SIN dibujar: para colocar objetos (la tarta en la mano, la boca) en otros instantes."""
        p = dict(DEF)
        p.update(pose)
        T = self._T(p, h)
        a = lambda x, y: tuple(T(np.array([[x, y]]))[0])
        return dict(cabeza=a(0, -690), centro=a(0, -340), boca=a(0, -260), mano_i=a(*p["mano_i"]), mano_d=a(*p["mano_d"]), ojo_g=a(-84, -480))

    def dibujar(self, h, pose):
        p = dict(DEF)
        p.update(pose)
        t = h.t
        T = self._T(p, h)
        self._patas(h, p, T)
        self._cuerpo(h, p, T, t)
        mi = self._brazo(h, p, T, -1)
        md = self._brazo(h, p, T, 1)
        self._cara(h, p, T, t)
        self._efectos(h, p, T, t)
        a = lambda x, y: tuple(T(np.array([[x, y]]))[0])
        return dict(cabeza=a(0, -690), centro=a(0, -340), boca=a(0, -260), mano_i=a(*mi), mano_d=a(*md), pie_i=a(*p["pie_i"]), pie_d=a(*p["pie_d"]),
                    ojo_g=a(-84, -480), T=T)


class AnimCosa:
    """Claves por parámetro (como AnimGato). cara=[(t, 'nombre'[, tipo])] mezcla caras prefabricadas. Admite funciones f(t)."""

    def __init__(self, **tracks):
        self.cara_cl = tracks.pop("cara", None)
        self.tr = {k: (v if callable(v) else Pista(v)) for k, v in tracks.items()}

    def pose(self, t):
        p = {}
        if self.cara_cl:
            cl = sorted(self.cara_cl, key=lambda c: c[0])
            if t <= cl[0][0]:
                p.update(cara(cl[0][1]))
            elif t >= cl[-1][0]:
                p.update(cara(cl[-1][1]))
            else:
                for a, b in zip(cl, cl[1:]):
                    if a[0] <= t < b[0]:
                        u = _ease((t - a[0]) / (b[0] - a[0]), b[2] if len(b) > 2 else "io")
                        ca, cb = cara(a[1]), cara(b[1])
                        for k in set(ca) | set(cb):
                            p[k] = ca.get(k, DEF.get(k)) + (cb.get(k, DEF.get(k)) - ca.get(k, DEF.get(k))) * u
                        break
        for k, f in self.tr.items():
            v = f(t)
            if v is None:                                  # None = «no tocar»: queda el valor de la cara/defecto
                continue
            p[k] = tuple(float(c) for c in v) if np.ndim(v) > 0 else float(v)
        return p
