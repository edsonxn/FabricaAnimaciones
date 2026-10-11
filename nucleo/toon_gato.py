# -*- coding: utf-8 -*-
"""Mostacho: gato flaco, cabezón y miedoso (personaje ORIGINAL para el estilo cartoon90, nucleo/toon.py).

No es un recorte con partes rígidas: cada cuadro se reconstruye desde cero a partir de ~40 parámetros (`DEF`), con formas elásticas
(cabeza y cuerpo = blobs que se aplastan/estiran con volumen, brazos y piernas = tubos de goma, cola = cadena con retraso,
orejas/bigotes/cascabel = acción superpuesta calculada de la velocidad), cara con párpados que recortan el ojo, iris con pupila
rasgada, boca de 1 a 3 «piezas» (labios, lengua, dientes) y efectos de miedo (pelo erizado, temblor, sudor, rayas).

    g = Gato()
    g.dibujar(h, pose)          # pose = dict con los parámetros de DEF que cambien; h = toon.Toon
    A = AnimGato(x=[(0, 540), (2, 700, 'o')], ojo=[...])      # claves por parámetro (ver AnimGato)
    pose = A.pose(t)            # añade solo la acción superpuesta automática (orejas, cola, cascabel, estiramiento)

Poses de cara prefabricadas en `CARAS` (dormido, neutro, alerta, susto, terror, grito, alivio, sospecha, tragar...).
"""
import math

import numpy as np

from motor import FPS, clamp01, ruido1
from toon import (Pista, bezier2, blob, eje_curvo, elipse_, espinas, gota, lag, muelle, pulso, suave, tiembla, tubo, vel)

# ------------------------------------------------------------------ paleta
PEL = (236, 138, 44)
PEL_S = (178, 88, 38)
CREMA = (252, 236, 206)
CREMA_S = (224, 196, 158)
ROSA = (240, 150, 156)
ROSA_S = (200, 104, 116)
NARIZ = (178, 72, 86)
BOCA = (74, 14, 32)
LENGUA = (236, 98, 116)
DIENTE = (255, 250, 240)
ESCLERA = (255, 252, 238)
ESCLERA_S = (214, 208, 196)
IRIS = (206, 224, 64)
IRIS_S = (150, 176, 40)
PUPILA = (22, 14, 24)
COLLAR = (206, 40, 52)
COLLAR_S = (140, 22, 40)
ORO = (244, 196, 66)
ORO_S = (186, 134, 40)
TINTA = (24, 18, 26)

DEF = dict(
    x=540.0, y=1500.0, s=1.0, flip=0, rot=0.0, sq=0.0, giro=0.0,
    cab_x=0.0, cab_y=0.0, cab_rot=0.0, cab_sq=0.0,
    ojo_i=1.0, ojo_d=1.0, ojo_t=1.0, pupila=0.5, mira_x=0.0, mira_y=0.0, incl=0.0, venas=0.0,
    ceja_i=0.0, ceja_d=0.0, ceja_ang=0.0, ceja_ang_d=None,
    boca=0.0, boca_w=1.0, sonrisa=0.15, lengua=0.0, dientes=0.0, boca_forma="n", mueca=0.0,
    erizo=0.0, tiembla=0.0, palidez=0.0, sudor=0.0, rayas_miedo=0.0,
    mano_i=(-112.0, -178.0), mano_d=(112.0, -178.0), curva_i=26.0, curva_d=-26.0,
    pie_i=(-46.0, 0.0), pie_d=(46.0, 0.0), rodilla_i=-22.0, rodilla_d=22.0,
    cola_a=-0.9, cola_curl=0.30, cola_sway=0.22, cola_hincha=0.0,
    oreja_i=0.0, oreja_d=0.0, oreja_baja=0.0,
    campana=0.0, collar=1, manos_frente=0, cuerpo_x=0.0, boca_o=0.0, tragar=0.0,
    linterna=None, bigotes=0.0, gesto_mano=(0.0, 0.0), burbuja=0.0,
)

# caras prefabricadas (solo parámetros de la cara): se mezclan con `cara(nombre, u)` o se usan como claves
CARAS = dict(
    neutro=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=1.0, pupila=0.55, ceja_i=0, ceja_d=0, ceja_ang=0.0, boca=0.0, sonrisa=0.1, boca_w=1.0,
                dientes=0, lengua=0, venas=0, incl=0.0),
    dormido=dict(ojo_i=0.0, ojo_d=0.0, ojo_t=1.0, pupila=0.5, ceja_i=-4, ceja_d=-4, ceja_ang=-0.1, boca=0.0, sonrisa=0.35, boca_w=0.8),
    adormilado=dict(ojo_i=0.34, ojo_d=0.34, ojo_t=1.0, pupila=0.5, ceja_i=-8, ceja_d=-8, ceja_ang=-0.08, boca=0.08, sonrisa=-0.05,
                    boca_w=0.8, incl=0.1),
    alerta=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=1.25, pupila=0.34, ceja_i=-22, ceja_d=-22, ceja_ang=0.25, boca=0.12, sonrisa=-0.25,
                boca_w=0.9),
    susto=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=1.7, pupila=0.2, ceja_i=-46, ceja_d=-46, ceja_ang=0.35, boca=0.55, sonrisa=-0.5, boca_w=1.15,
               dientes=0.5, lengua=0.3, venas=0.4),
    terror=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=2.1, pupila=0.11, ceja_i=-62, ceja_d=-62, ceja_ang=0.5, boca=1.0, sonrisa=-0.8, boca_w=1.2,
                dientes=1.0, lengua=1.0, venas=1.0, boca_forma="g"),
    grito=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=2.3, pupila=0.08, ceja_i=-70, ceja_d=-70, ceja_ang=0.55, boca=1.0, sonrisa=-0.9, boca_w=1.45,
               dientes=1.0, lengua=1.0, venas=1.0, boca_forma="g"),
    alivio=dict(ojo_i=0.45, ojo_d=0.45, ojo_t=1.0, pupila=0.5, ceja_i=8, ceja_d=8, ceja_ang=0.25, boca=0.0, sonrisa=0.55, boca_w=1.0),
    sospecha=dict(ojo_i=0.5, ojo_d=0.55, ojo_t=1.0, pupila=0.5, ceja_i=-4, ceja_d=-14, ceja_ang=-0.45, ceja_ang_d=-0.1, boca=0.0,
                  sonrisa=-0.2, boca_w=0.9, incl=-0.3),
    tragar=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=1.55, pupila=0.2, ceja_i=-38, ceja_d=-38, ceja_ang=0.45, boca=0.0, sonrisa=-0.6,
                boca_w=0.9, mueca=1.0),
    preocupado=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=1.3, pupila=0.3, ceja_i=-30, ceja_d=-30, ceja_ang=0.5, boca=0.0, sonrisa=-0.5,
                    boca_w=0.9, mueca=0.6),
    sorpresa=dict(ojo_i=1.0, ojo_d=1.0, ojo_t=1.5, pupila=0.28, ceja_i=-40, ceja_d=-40, ceja_ang=0.1, boca=0.4, sonrisa=-0.1,
                  boca_w=0.55, boca_forma="o"),
    feliz=dict(ojo_i=0.55, ojo_d=0.55, ojo_t=1.05, pupila=0.62, ceja_i=6, ceja_d=6, ceja_ang=-0.1, boca=0.42, sonrisa=1.0, boca_w=1.15,
               dientes=0.3, lengua=0.35),
    llanto=dict(ojo_i=0.8, ojo_d=0.8, ojo_t=1.2, pupila=0.45, ceja_i=-24, ceja_d=-24, ceja_ang=0.6, boca=0.55, sonrisa=-0.7,
                boca_w=1.1, dientes=0.3, lengua=0.4),
)
CLAVES_CARA = [k for k in DEF if k in CARAS["neutro"]]


def cara(nombre, u=1.0, base=None):
    """Mezcla la cara `nombre` con la cara neutra (u=0 neutra, 1 completa)."""
    b = dict(CARAS["neutro"] if base is None else base)
    c = CARAS[nombre]
    out = {}
    for k in set(b) | set(c):
        v0 = b.get(k, DEF.get(k))
        v1 = c.get(k, v0)
        if isinstance(v1, str) or v0 is None or v1 is None:
            out[k] = v1 if u >= 0.5 else v0
        else:
            out[k] = v0 + (v1 - v0) * u
    return out


def _rot(P, a):
    c, s = math.cos(a), math.sin(a)
    P = np.asarray(P, float)
    return np.stack([P[:, 0] * c - P[:, 1] * s, P[:, 0] * s + P[:, 1] * c], 1)


class Gato:
    """Dibuja a Mostacho completo a partir de una pose. Una instancia por escena (no guarda estado entre cuadros)."""

    def __init__(self, sem=0, pelo=PEL, pelo_s=PEL_S):
        self.luz = None                      # (x, y, ángulo) del haz de la linterna en pantalla tras dibujar
        self.sem = sem
        self.pelo, self.pelo_s = pelo, pelo_s

    # ---------------------------------------------------------- transformaciones
    def _mk(self, p, h):
        """Devuelve T(P_local) -> pantalla (con la cámara de h)."""
        sg = -1.0 if p["flip"] else 1.0
        sx, sy = (1 + p["sq"]) * sg, 1 - p["sq"]
        c, s_ = math.cos(p["rot"]), math.sin(p["rot"])
        sc = p["s"]
        tx, ty = 0.0, 0.0
        if p["tiembla"] > 0:
            tx, ty = tiembla(h.t, p["tiembla"] * sc, sem=self.sem)
        ox, oy = p["x"] + tx, p["y"] + ty
        cx = p["cuerpo_x"]

        def T(P):
            P = np.asarray(P, float)
            Q = np.stack([(P[:, 0] + cx * 0) * sx, P[:, 1] * sy], 1)
            Q = np.stack([Q[:, 0] * c - Q[:, 1] * s_, Q[:, 0] * s_ + Q[:, 1] * c], 1) * sc + (ox, oy)
            return Q                    # coordenadas del MUNDO: forma/trazo aplican la cámara; relleno/anillo piden h.tf(...)
        T.sg = sg
        return T

    def _cabeza_T(self, p, T):
        """Transformación de coordenadas locales de la cabeza (origen = centro) a pantalla."""
        neck = np.array([0.0, -345.0])
        hc0 = np.array([p["cab_x"] + p["giro"] * 10, -447.0 + p["cab_y"]])
        a = p["cab_rot"]
        cs, sn = math.cos(a), math.sin(a)
        q = 1 + p["cab_sq"], 1 - p["cab_sq"]

        def HT(P):
            P = np.asarray(P, float)
            L = np.stack([P[:, 0] * q[0], P[:, 1] * q[1]], 1)
            L = np.stack([L[:, 0] * cs - L[:, 1] * sn, L[:, 0] * sn + L[:, 1] * cs], 1)
            C = hc0 - neck
            Cr = np.array([C[0] * cs - C[1] * sn, C[0] * sn + C[1] * cs]) + neck
            return T(L + Cr)
        return HT

    # ---------------------------------------------------------- partes del cuerpo
    def _cola(self, h, p, T):
        t = h.t
        n = 9
        a = p["cola_a"] + p["cola_curl"] * 0.0
        pts = [np.array([-6.0, -168.0])]
        ang = a
        L = 40.0 + 10 * p["cola_hincha"]
        for j in range(1, n + 1):
            ang_j = ang + p["cola_curl"] * (j / n) * 2.2 + p["cola_sway"] * math.sin(2 * math.pi * 0.7 * (t - 0.13 * j) + self.sem) * (j / n)
            pts.append(pts[-1] + L * np.array([math.cos(ang_j), math.sin(ang_j)]))
        eje = suave(np.array(pts), 6, False)
        w0, w1 = 38.0 + 24 * p["cola_hincha"], 26.0 + 36 * p["cola_hincha"]
        P = tubo(eje, w0, w1, wmed=(w0 + w1) / 2 + 4)
        if p["cola_hincha"] > 0.05 or p["erizo"] > 0.05:
            from motor import remuestrear
            P = espinas(remuestrear(P, 6.0, True)[:-1], max(p["cola_hincha"], p["erizo"] * 0.6) * 0.9, amp=14, per=4, sem=self.sem + 9)
        h.forma(T(P), self.pelo, self.pelo_s, w=9, sem=self.sem + 1)
        # anillos oscuros
        for j in (3, 5, 7):
            k = j * 6
            if k + 1 < len(eje):
                a0 = eje[k]
                d = eje[k + 1] - eje[k - 1]
                d = d / (np.hypot(*d) + 1e-9)
                nr = np.array([d[1], -d[0]])
                hw = (w0 + (w1 - w0) * k / len(eje)) / 2 * 0.86
                h.trazo(T(np.array([a0 + nr * hw, a0 - nr * hw])), 8, self.sem + 40 + j, color=PEL_S, taper=(0.2, 0.2), jit=0.6)

    def _pierna(self, h, p, T, lado):
        s = lado  # -1 izq, 1 der (en coordenadas locales)
        pie = np.array(p["pie_i"] if s < 0 else p["pie_d"], float)
        rod = p["rodilla_i"] if s < 0 else p["rodilla_d"]
        cadera = np.array([40.0 * s, -165.0])
        eje = eje_curvo(cadera, pie + np.array([0.0, -16.0]), rod, 18)
        P = tubo(eje, 40, 31, extremo=True)
        h.forma(T(P), self.pelo, self.pelo_s, w=9, sem=self.sem + 10 + s)
        # pie (patita crema)
        ang = 0.0
        sg = 1 if s > 0 else -1
        F = blob(pie[0] + 6 * sg + p["giro"] * 10, pie[1] - 10, 50, 26, rad=[1, 0.96, 1.0, 1.08, 1.0, 0.96, 1.0, 1.0], rot=ang, n=8, sub=8)
        h.forma(T(F), CREMA, CREMA_S, w=9, sem=self.sem + 12 + s, d_sombra=(10, 14))
        for k in (-1, 0, 1):
            h.trazo(T(np.array([[pie[0] + 6 * sg + k * 17 + p["giro"] * 10, pie[1] - 22], [pie[0] + 6 * sg + k * 17 + p["giro"] * 10, pie[1] - 7]])),
                    5, self.sem + 14 + k, taper=(0.1, 0.3), jit=0.5)

    def _cuerpo(self, h, p, T):
        rad = [1.0, 1.04, 1.12, 1.13, 1.1, 1.0, 0.92, 0.84, 0.8, 0.82, 0.88, 0.96]
        P = blob(0, -245, 82, 104, rad=rad, n=12, sub=8)
        from motor import remuestrear
        if p["erizo"] > 0.02:
            P = espinas(remuestrear(P, 7.0, True)[:-1], p["erizo"], amp=20, per=4, sem=self.sem + 3)
        h.forma(T(P), self.pelo, self.pelo_s, w=11, sem=self.sem + 20, d_sombra=(18, 24), sketch=0.9)
        B = blob(0, -226, 50, 70, rad=[1, 1, 1, 1], n=8, sub=8)
        h.forma(T(B), CREMA, CREMA_S, w=0, sem=self.sem + 21, d_sombra=(10, 12), jit=1.0)

    def _linterna(self, h, p, T, mano, ang):
        """Linterna roja sujeta por la mano (ang = dirección local en rad). Guarda en self.luz el origen y la dirección del haz en pantalla."""
        d = np.array([math.cos(ang), math.sin(ang)])
        n = np.array([-d[1], d[0]])
        c0 = mano - d * 26
        cuerpo = np.array([c0 + n * 17, c0 + d * 78 + n * 17, c0 + d * 78 - n * 17, c0 - n * 17])
        h.forma(T(suave(cuerpo, 3, True)), (200, 52, 48), (140, 30, 40), w=8, sem=self.sem + 190, jit=0.8, d_sombra=(6, 8))
        cab = np.array([c0 + d * 74 + n * 17, c0 + d * 112 + n * 30, c0 + d * 112 - n * 30, c0 + d * 74 - n * 17])
        h.forma(T(cab), (150, 150, 168), (100, 100, 128), w=8, sem=self.sem + 191, jit=0.8, d_sombra=(6, 8))
        lente = elipse_(*(c0 + d * 112), 8, 30, rot=ang, n=16)
        h.forma(T(lente), (255, 246, 190), None, w=5, sem=self.sem + 192, jit=0.4, tex=0.0)
        a = h.tf(T(np.array([c0 + d * 176])))[0]
        b = h.tf(T(np.array([c0 + d * 276])))[0]
        self.luz = (float(a[0]), float(a[1]), math.atan2(b[1] - a[1], b[0] - a[0]))

    def _brazo(self, h, p, T, lado, hombro_extra=(0, 0)):
        s = lado
        hombro = np.array([66.0 * s, -296.0]) + np.array(hombro_extra)
        mano = np.array(p["mano_i"] if s < 0 else p["mano_d"], float)
        curva = p["curva_i"] if s < 0 else p["curva_d"]
        eje = eje_curvo(hombro, mano, curva, 18)
        P = tubo(eje, 34, 28, extremo=True)
        h.forma(T(P), self.pelo, self.pelo_s, w=9, sem=self.sem + 30 + s)
        if s > 0 and p["linterna"] is not None:
            self._linterna(h, p, T, mano, p["linterna"])
        # mano (mitón crema con dos deditos)
        M = blob(mano[0], mano[1], 31, 28, rad=[1, 1.08, 1, 0.94, 1.04, 1.0, 0.96, 1.05], n=8, sub=8)
        h.forma(T(M), CREMA, CREMA_S, w=8, sem=self.sem + 32 + s, d_sombra=(8, 10))
        d = mano - hombro
        d = d / (np.hypot(*d) + 1e-9)
        for k in (-1, 1):
            b = mano + d * 6 + np.array([-d[1], d[0]]) * 9 * k
            h.trazo(T(np.array([b, b + d * 16])), 4.5, self.sem + 34 + k, taper=(0.1, 0.5), jit=0.4)
        return mano

    # ---------------------------------------------------------- cabeza y cara
    def _cabeza(self, h, p, T, HT):
        g = p["giro"]
        ge = abs(g)
        # orejas (detrás de la cabeza)
        for s in (-1, 1):
            rot = p["oreja_i"] if s < 0 else p["oreja_d"]
            baja = p["oreja_baja"]
            lado = ge * (0.14 if (s * g) < 0 else -0.10)
            O = suave([(s * 52, -102), (s * (112 + 14 * lado * s), -232 + baja * 70), (s * 150, -92)], 10, True)
            O = _rot(O - np.array([s * 100.0, -100.0]), rot * s + baja * 0.55 * s) + np.array([s * 100.0, -100.0])
            h.forma(HT(O), self.pelo, self.pelo_s, w=10, sem=self.sem + 50 + s, d_sombra=(10, 14))
            I = suave([(s * 70, -110), (s * (112 + 6 * lado * s), -196 + baja * 56), (s * 130, -110)], 8, True)
            I = _rot(I - np.array([s * 100.0, -100.0]), rot * s + baja * 0.55 * s) + np.array([s * 100.0, -100.0])
            h.forma(HT(I), ROSA, ROSA_S, w=0, sem=self.sem + 52 + s, d_sombra=(6, 8), jit=0.8)
        # mechones de las mejillas (salen de detrás de la cabeza)
        for s in (-1, 1):
            for k, (yy, ll) in enumerate(((44, 52), (76, 44))):
                M = np.array([(s * 124, yy - 20), (s * (128 + ll), yy + 22), (s * 104, yy + 20)])
                h.forma(HT(M), self.pelo, self.pelo_s, w=8, sem=self.sem + 56 + s * 3 + k, d_sombra=(6, 8), jit=0.8)
        # cabeza
        rad = [1.0, 1.03, 1.06, 1.05, 0.98, 1.0, 1.0, 0.98, 0.95, 0.98, 1.0, 1.03]
        ab_ = p["boca"] * (1.0 if p["boca_forma"] != "o" else 0.4)
        for i_, k_ in ((2, 0.45), (3, 0.62), (4, 0.45)):         # la mandíbula baja cuando abre la boca
            rad[i_] *= 1 + k_ * ab_
        P = blob(0, 0, 152, 119 * (1 + 0.04 * ab_), rad=rad, n=12, sub=8)
        from motor import remuestrear
        if p["erizo"] > 0.02:
            P = espinas(remuestrear(P, 7.0, True)[:-1], p["erizo"], amp=30, per=6, sem=self.sem + 4)
        h.forma(HT(P), self.pelo, self.pelo_s, w=12.5, sem=self.sem + 60, d_sombra=(20, 26), sketch=0.9)
        # palidez de miedo: capa clara encima
        # hocico crema
        for s in (-1, 1):
            xo = s * 30 + g * 30
            M = blob(xo, 54, 44 * (1 - 0.12 * ge * (1 if s * g < 0 else -1)), 33, rad=[1, 1, 1, 1], n=8, sub=8)
            h.forma(HT(M), CREMA, CREMA_S, w=0, sem=self.sem + 62 + s, d_sombra=(8, 10), jit=0.8)
        # rayas de la frente
        for k, (xx, yy, a_) in enumerate(((0, -112, 0), (-34, -104, 0.28), (34, -104, -0.28))):
            xx += g * 14
            h.trazo(HT(np.array([[xx, yy], [xx + 8 * math.sin(a_) * 2, yy + 34]])), 10, self.sem + 70 + k, color=PEL_S, taper=(0.1, 0.7), jit=0.8)
        self._bigotes(h, p, HT)
        self._ojos(h, p, HT)
        self._nariz_boca(h, p, HT)
        self._cejas(h, p, HT)

    def _ojo(self, h, p, HT, s, abre, tam):
        g = p["giro"]
        ge = abs(g)
        cerca = (s * g > 0)
        rx, ry = 41.0 * tam, 49.0 * tam
        esc = 1 + 0.10 * ge * (1 if cerca else -1)
        rx, ry = rx * esc, ry * esc
        cx = s * (56 * (1 - 0.14 * ge) + 12 * (tam - 1)) + g * 40
        cy = -10.0 - (tam - 1) * 8
        if abre < 0.07:
            # párpado cerrado: arco hacia abajo
            xs = np.linspace(-rx * 0.95, rx * 0.95, 14)
            ys = 10 * (1 - (xs / (rx * 0.95)) ** 2)
            h.trazo(HT(np.stack([cx + xs, cy + ys + ry * 0.35], 1)), 10, self.sem + 80 + s, taper=(0.2, 0.2), jit=0.6)
            return None
        a = np.linspace(0, 2 * math.pi, 46, endpoint=False)
        x, y = rx * np.cos(a), ry * np.sin(a)
        ytop = -ry * (2 * abre - 1) - p["incl"] * s * 0.0 + (p["incl"] * (-s * x / rx)) * ry * 0.55
        y = np.clip(y, ytop, ry)
        P = np.stack([cx + x, cy + y], 1)
        r = h.forma(HT(P), ESCLERA, ESCLERA_S, w=9, sem=self.sem + 82 + s, d_sombra=(8, 12), jit=0.9, tex=0.01)
        clip = r
        # venas
        if p["venas"] > 0.05 and r is not None:
            rng = np.random.default_rng(5 + s)
            for k in range(6):
                ang = rng.uniform(0, 2 * math.pi)
                ln = rx * (0.55 + 0.4 * rng.uniform()) * p["venas"]
                a0 = np.array([cx + math.cos(ang) * rx * 0.98, cy + math.sin(ang) * ry * 0.98])
                a1 = np.array([cx + math.cos(ang) * (rx * 0.98 - ln), cy + math.sin(ang) * (ry * 0.98 - ln * ry / rx)])
                h.trazo(HT(np.array([a0, (a0 + a1) / 2 + rng.uniform(-6, 6, 2), a1])), 3.4, self.sem + 90 + k, color=(214, 48, 56),
                        taper=(0.0, 0.8), jit=0.5)
        # iris + pupila (se recortan con el párpado)
        pr = rx * (0.30 + 1.15 * p["pupila"] * 0.62)
        pr = min(pr, rx * 0.86)
        mx = p["mira_x"] + (g * 0.25)
        my = p["mira_y"]
        ix = cx + mx * (rx - pr) * 0.95
        iy = cy + my * (ry - pr) * 0.95
        irisP = elipse_(ix, iy, pr, pr * 1.02, n=28)
        h.relleno(h.tf(HT(irisP)), IRIS, grad=(IRIS_S, h.tf(HT(np.array([[0, cy]])))[0][1] - 10, h.tf(HT(np.array([[0, cy + ry]])))[0][1]), clip=r, tex=0.01)
        pw = pr * (0.18 + 0.82 * clamp01(p["pupila"] * 1.8)) * (0.55 if p["pupila"] < 0.3 else 1.0)
        pw = max(pr * 0.12, pw * 0.8)
        pup = elipse_(ix, iy, pw, pr * 0.96, n=24)
        h.relleno(h.tf(HT(pup)), PUPILA, clip=r, tex=0.0)
        if p["pupila"] > 0.2:
            hl = elipse_(ix - pr * 0.28, iy - pr * 0.34, pr * 0.2, pr * 0.2, n=14)
            h.relleno(h.tf(HT(hl)), (255, 255, 255), clip=r, tex=0.0)
        # contorno otra vez (encima del iris)
        h.anillo(h.tf(HT(P)), 8.0, self.sem + 84 + s, jit=0.0)
        # párpado (línea gruesa arriba) si está medio cerrado
        if abre < 0.95:
            xs = np.linspace(-rx, rx, 16)
            ytl = (-ry * (2 * abre - 1)) + (p["incl"] * (-s * xs / rx)) * ry * 0.55
            h.trazo(HT(np.stack([cx + xs, cy + ytl], 1)), 11, self.sem + 86 + s, taper=(0.1, 0.1), jit=0.5)
        return (cx, cy, rx, ry)

    def _bigotes(self, h, p, HT):
        g = p["giro"]
        bw = p["bigotes"]
        for s in (-1, 1):
            for k, ay in enumerate((-0.30, 0.0, 0.30)):
                x0 = s * 40 + g * 32
                y0 = 64 + 7 * k
                ex = s * (176 + 26 * abs(g) * (1 if s * g > 0 else -0.4)) + g * 20
                ey = y0 + 62 * ay + 8 + bw * 16
                pts = bezier2((x0, y0), (x0 + s * 80, y0 + 14 * ay - 6 + bw * 8), (ex, ey), 12)
                h.trazo(HT(pts), 4.0, self.sem + 114 + s * 3 + k, taper=(0.08, 0.8), jit=0.5)

    def _ojos(self, h, p, HT):
        self._ojo(h, p, HT, -1, p["ojo_i"], p["ojo_t"])
        self._ojo(h, p, HT, 1, p["ojo_d"], p["ojo_t"])

    def _cejas(self, h, p, HT):
        g = p["giro"]
        for s in (-1, 1):
            alt = p["ceja_i"] if s < 0 else p["ceja_d"]
            ang = p["ceja_ang"] if (s < 0 or p["ceja_ang_d"] is None) else p["ceja_ang_d"]
            tam = p["ojo_t"]
            cx = s * 56 * (1 - 0.14 * abs(g)) + g * 40
            cy = max(-112.0, -78 - (tam - 1) * 12 + alt * 0.45)
            ln = 46
            # ang>0 = preocupada (extremo interior arriba)
            ai = np.array([cx - s * ln * 0.55, cy - ang * ln * 0.9])
            ao = np.array([cx + s * ln * 0.55, cy + ang * ln * 0.9])
            mid = (ai + ao) / 2 + np.array([0, -10 - 8 * abs(ang)])
            h.trazo(HT(bezier2(ai, mid, ao, 12)), 14, self.sem + 100 + s, taper=(0.15, 0.4), jit=0.8)

    def _nariz_boca(self, h, p, HT):
        g = p["giro"]
        nx = g * 38
        N = suave([(nx - 18, 34), (nx + 18, 34), (nx, 52)], 8, True)
        h.forma(HT(N), NARIZ, None, w=6, sem=self.sem + 110, jit=0.5, tex=0.0)
        # burbuja de moco (ronquido): crece y se encoge con la respiración
        if p["burbuja"] > 1.0:
            r = p["burbuja"]
            bx, by = nx + 18 + r * 0.55, 46 + r * 0.25
            B = elipse_(bx, by, r, r * 0.98, n=24)
            rb = h.forma(HT(B), (190, 236, 255), (140, 196, 232), w=3.5, sem=self.sem + 108, jit=0.6, alfa=0.55, tex=0.0, d_sombra=(6, 8))
            hl = elipse_(bx - r * 0.38, by - r * 0.4, r * 0.2, r * 0.13, rot=-0.7, n=12)
            h.relleno(h.tf(HT(hl)), (255, 255, 255), alfa=0.9, tex=0.0)
        # boca
        w = 74.0 * p["boca_w"]
        ab = p["boca"]
        sonr = p["sonrisa"]
        cx = g * 30
        y0 = 70.0
        forma = p["boca_forma"]
        if ab < 0.04:
            esq = 0.2 * w * 0.5 * sonr
            ctr = 0.1 * w * 0.5 * sonr
            ys = y0 - 0.0
            L, R = (cx - w / 2, ys - esq), (cx + w / 2, ys - esq)
            # sonrisa estilo gato «ω»
            m1 = (cx - w / 4, ys + ctr + 2)
            m2 = (cx + w / 4, ys + ctr + 2)
            pts = suave([L, m1, (cx, ys - 4), m2, R], 8, False)
            if p["mueca"] > 0.05:
                k = np.linspace(0, 1, 40)
                xs = cx - w / 2 + w * k
                ys_ = y0 - 8 * sonr + 5 * np.sin(k * 2 * math.pi * 5 + h.dib * 1.9) * p["mueca"] * 1.5 - 8 * np.sin(math.pi * k) * sonr
                pts = np.stack([xs, ys_], 1)
            h.trazo(HT(pts), 7.5, self.sem + 120, taper=(0.15, 0.15), jit=0.7)
            # la «ω» se completa con la línea del filtro
            h.trazo(HT(np.array([[cx, 52], [cx, y0 - 4]])), 5, self.sem + 121, taper=(0.1, 0.1), jit=0.4)
            return
        hh = 8 + 150 * ab
        if forma == "g":
            hh = 150 * ab + 20
        top_y = y0 - 6
        wv = w * (1.0 if forma != "o" else 0.55)
        if forma == "o":
            hh = max(hh, 44)
            P = blob(cx, y0 + hh * 0.38, wv / 2, hh / 2, rad=[1, 1, 1, 1], n=8, sub=8)
        else:
            # boca abierta: labio superior curvo + mandíbula redonda
            n = 28
            u = np.linspace(0, math.pi, n)
            xs = (wv / 2) * np.cos(u)
            alto_s = -10 - 16 * max(0.0, -sonr)
            yl = y0 + hh * (np.sin(u) ** 0.8)
            yu = top_y + alto_s * 0.4 * np.sin(u) * 0 - 0.0 * u
            esquina = -sonr * 0.16 * wv * 0.5
            # arriba: del extremo izquierdo al derecho (ligeramente curvo); abajo: semielipse
            xs_top = np.linspace(-wv / 2, wv / 2, 16)
            ys_top = top_y + esquina * (1 - (2 * xs_top / wv) ** 2) * 0 - 4 * np.sin(np.linspace(0, math.pi, 16)) * (1 if sonr < 0 else -1) \
                - esquina * (2 * np.abs(xs_top) / wv) ** 2 * 0.0
            arr = np.stack([cx + xs_top, ys_top], 1)
            ang2 = np.linspace(0, math.pi, 24)
            aba = np.stack([cx + (wv / 2) * np.cos(ang2), top_y + hh * np.sin(ang2) ** 0.9], 1)
            P = np.vstack([arr, aba[1:-1]])
            P = suave(P, 3, True)
        r = h.forma(HT(P), BOCA, None, w=9, sem=self.sem + 124, jit=0.9, tex=0.0)
        clip = r
        if r is None:
            return
        # lengua
        if p["lengua"] > 0.03:
            lw = wv * 0.62
            L_ = blob(cx, y0 + hh * 0.9, lw / 2, hh * 0.46 * (0.5 + 0.5 * p["lengua"]), rad=[1, 1, 1, 1], n=8, sub=8)
            h.relleno(h.tf(HT(L_)), LENGUA, clip=clip, tex=0.01)
            h.trazo(HT(np.array([[cx, y0 + hh * 0.55], [cx + 2, y0 + hh * 0.9]])), 4, self.sem + 125, color=(180, 60, 84), taper=(0.1, 0.6), jit=0.4)
        # dientes superiores y colmillos
        if p["dientes"] > 0.03:
            dh = (14 + 34 * p["dientes"])
            nd = 5 if forma == "g" else 4
            for k in range(nd):
                xc = cx + (k - (nd - 1) / 2) * (wv / nd) * 0.95
                T_ = np.array([(xc - wv / nd * 0.46, top_y - 6), (xc + wv / nd * 0.46, top_y - 6), (xc + wv / nd * 0.4, top_y + dh * (0.8 if k % 2 else 1.0)),
                               (xc - wv / nd * 0.4, top_y + dh * (0.8 if k % 2 else 1.0))])
                h.relleno(h.tf(HT(T_)), DIENTE, clip=clip, tex=0.0)
                if k:
                    h.trazo(HT(np.array([[xc - wv / nd * 0.46, top_y], [xc - wv / nd * 0.46, top_y + dh * 0.85]])), 3.5, self.sem + 126 + k,
                            taper=(0.1, 0.1), jit=0.3)
            for s in (-1, 1):
                F = np.array([(cx + s * wv * 0.36 - 9, top_y + hh * 0.5), (cx + s * wv * 0.36 + 9, top_y + hh * 0.5), (cx + s * wv * 0.36, top_y + hh * 0.5 - 20 - 22 * p["dientes"])])
                h.relleno(h.tf(HT(F)), DIENTE, clip=clip, tex=0.0)
        # el contorno encima
        h.anillo(h.tf(HT(P)), 9.0, self.sem + 127, jit=0.0)
        # úvula
        if forma == "g" and ab > 0.7:
            U = blob(cx, y0 + hh * 0.3, 12, 18, rad=[1, 1, 1, 1], n=8, sub=6)
            h.forma(HT(U), (200, 70, 90), None, w=5, sem=self.sem + 128, jit=0.4, clip=clip, tex=0.0)

    # ---------------------------------------------------------- efectos de miedo
    def _efectos(self, h, p, T, HT):
        t = h.t
        if p["sudor"] > 0.02:
            for k in range(4):
                ph = (t * 1.35 + k * 0.27) % 1.0
                if ph * p["sudor"] < 0.02 and p["sudor"] < 0.5:
                    continue
                side = -1 if k % 2 == 0 else 1
                x0 = side * (150 + 22 * (k // 2))
                y0 = -90 + 42 * (k // 2)
                d = np.array([x0 + side * 90 * ph, y0 - 60 * ph + 330 * ph * ph])
                r = 15 * (1.0 - 0.3 * ph) * min(1.0, p["sudor"] * 1.4)
                G = gota(d[0], d[1], r, ang=side * (0.6 - 1.0 * ph) * 0.5)
                h.forma(HT(G), (170, 220, 255), (120, 176, 230), w=5, sem=self.sem + 140 + k, jit=0.4, d_sombra=(4, 6), tex=0.0)
        if p["rayas_miedo"] > 0.02:
            r = p["rayas_miedo"]
            for k in range(5):
                x = (k - 2) * 28
                a = np.array([x, -138 - 22 * abs(k - 2) * 0.0])
                h.trazo(HT(np.array([a, a + np.array([0, -46 * r])])), 6, self.sem + 150 + k, taper=(0.2, 0.2), jit=0.7)
        if p["tiembla"] > 0.4:
            # líneas de tembleque a los lados de la cabeza
            for s in (-1, 1):
                for k in range(3):
                    yy = -50 + 52 * k
                    ph = h.dib * 2.2 + k + s
                    pts = np.array([[s * (176 + 20 * math.sin(ph)), yy], [s * (194 + 20 * math.sin(ph + 1)), yy + 22]])
                    h.trazo(HT(pts), 5.5, self.sem + 160 + k + s * 4, taper=(0.1, 0.6), jit=0.6)

    def _collar(self, h, p, T, HT):
        t = h.t
        u = np.linspace(-1, 1, 14)
        pts = np.stack([u * 74, -320 + 14 * (1 - u * u) * 0.0 + 28 * u * u * -0.5 + 16], 1)
        P = tubo(pts, 24, 24, extremo=True)
        h.forma(T(P), COLLAR, COLLAR_S, w=8, sem=self.sem + 170, d_sombra=(6, 8), jit=0.8)
        # cascabel colgando (retraso + temblor)
        sw = p["campana"]
        ang = 0.0 + 0.5 * sw
        cb = np.array([0 + 40 * math.sin(ang) * 0.2, -296 + 8 * abs(math.cos(ang))])
        C = elipse_(cb[0], cb[1], 17, 17, n=18)
        h.forma(T(C), ORO, ORO_S, w=6, sem=self.sem + 172, d_sombra=(5, 7), jit=0.5, tex=0.0)
        h.trazo(T(np.array([[cb[0] - 9, cb[1] + 5], [cb[0] + 9, cb[1] + 5]])), 3.5, self.sem + 173, taper=(0.1, 0.1), jit=0.2)
        h.disco(*T(np.array([[cb[0], cb[1] + 9]]))[0], 2.6, TINTA)

    # ---------------------------------------------------------- dibujo completo
    def dibujar(self, h, pose):
        p = dict(DEF)
        p.update(pose)
        self.luz = None
        T = self._mk(p, h)
        HT = self._cabeza_T(p, T)
        # orden de atrás hacia adelante
        self._cola(h, p, T)
        for s in (-1, 1):
            self._pierna(h, p, T, s)
        self._cuerpo(h, p, T)
        if p["collar"]:
            self._collar(h, p, T, HT)
        manos = []
        if not p["manos_frente"]:
            for s in (-1, 1):
                self._brazo(h, p, T, s)
        self._cabeza(h, p, T, HT)
        self._efectos(h, p, T, HT)
        if p["manos_frente"]:
            for s in (-1, 1):
                self._brazo(h, p, T, s)
        return T, HT



# ------------------------------------------------------------------ animación por claves + acción superpuesta automática
class AnimGato:
    """Claves por parámetro: AnimGato(x=[(t, v[, tipo]), ...], ojo_i=[...]). Los parámetros sin claves usan DEF. `cara=` admite
    una lista [(t, 'nombre'[, tipo])] que mezcla caras prefabricadas. pose(t) añade la acción superpuesta: orejas, bigotes, cola y
    cascabel reaccionan a la velocidad y a los golpes (sin simular: todo es función de t)."""

    def __init__(self, auto=True, golpes=None, **tracks):
        self.tr = {}
        self.cara_cl = tracks.pop("cara", None)
        self.golpes = golpes or []                 # (t0, amplitud) de aplastamientos / sacudidas del cuerpo
        for k, v in tracks.items():
            self.tr[k] = v if callable(v) else Pista(v)
        self.auto = auto

    def _base(self, t):
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
                        from toon import _ease
                        u = _ease((t - a[0]) / (b[0] - a[0]), b[2] if len(b) > 2 else "io")
                        ca, cb = cara(a[1]), cara(b[1])
                        for k in set(ca) | set(cb):
                            v0, v1 = ca.get(k, DEF.get(k)), cb.get(k, DEF.get(k))
                            p[k] = (v1 if u >= 0.5 else v0) if isinstance(v0, str) or v0 is None or v1 is None else v0 + (v1 - v0) * u
                        break
        for k, f in self.tr.items():
            v = f(t)
            p[k] = None if v is None else (tuple(float(c) for c in v) if np.ndim(v) > 0 else float(v))
        return p

    def pose(self, t):
        p = self._base(t)
        if not self.auto:
            return p
        x, y = p.get("x", DEF["x"]), p.get("y", DEF["y"])
        if "x" in self.tr and "y" in self.tr:
            vx, vy = vel(self.tr["x"], t), vel(self.tr["y"], t)
            vx, vy = float(vx), float(vy)
            sc = p.get("s", 1.0)
            # estiramiento por velocidad vertical (solo si el usuario no fijó sq)
            if "sq" not in self.tr:
                p["sq"] = float(np.clip(-abs(vy) / 3600.0, -0.22, 0.0)) + muelle(t, self.golpes, 3.4, 0.18)
            p["rot"] = p.get("rot", 0.0) + float(np.clip(vx / 9000.0, -0.12, 0.12))
            p["oreja_baja"] = p.get("oreja_baja", 0.0) + float(np.clip(vy / 4200.0, -0.5, 0.6)) + float(np.clip(abs(vx) / 4500.0, 0, 0.3))
            p["oreja_i"] = p.get("oreja_i", 0.0) + float(np.clip(-vx / 3500.0, -0.4, 0.4)) + 0.05 * math.sin(7 * t)
            p["oreja_d"] = p.get("oreja_d", 0.0) + float(np.clip(-vx / 3500.0, -0.4, 0.4)) + 0.05 * math.sin(7 * t + 1.3)
            p["cola_a"] = p.get("cola_a", DEF["cola_a"]) + float(np.clip(-vx / 2200.0, -0.8, 0.8))
            p["campana"] = float(np.clip(vx / 700.0, -1, 1)) + 0.15 * math.sin(11 * t)
            p["bigotes"] = float(np.clip(-vx / 900.0, -1, 1) + np.clip(vy / 1200.0, -1, 1))
        elif self.golpes:
            p["sq"] = p.get("sq", 0.0) + muelle(t, self.golpes, 3.4, 0.18)
        return p


def pasos(fase, zancada=42.0, alt=34.0, dir=1):
    """Ciclo de caminar de puntitas (fase en ciclos: 0..1 = dos pasos). Devuelve pie_i, pie_d, rodillas y el rebote vertical de la
    cadera en px locales (+x = hacia donde mira). Para que el pie apoyado no patine: velocidad del cuerpo = 4*zancada*s/T."""
    out = {}
    lifts = []
    for lado, off, bx in (("i", 0.0, -34.0), ("d", 0.5, 34.0)):
        f = (fase + off) % 1.0
        if f < 0.5:
            u = f / 0.5
            e = u * u * (3 - 2 * u)
            x = -zancada + 2 * zancada * e
            y = -alt * math.sin(math.pi * u)
            lift = math.sin(math.pi * u)
        else:
            u = (f - 0.5) / 0.5
            x = zancada - 2 * zancada * u
            y = 0.0
            lift = 0.0
        out["pie_" + lado] = (bx * 0.8 + dir * x, y)
        out["rodilla_" + lado] = (-22 if lado == "i" else 22) * (1 + 0.9 * lift) + 18 * lift * (1 if lado == "d" else -1) * 0
        lifts.append(lift)
    out["bob"] = -9.0 * abs(math.sin(2 * math.pi * fase)) + 5.0
    out["lift"] = lifts
    return out
