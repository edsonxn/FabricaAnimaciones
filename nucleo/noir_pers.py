# -*- coding: utf-8 -*-
"""Personajes del estilo NOIR (nucleo/noir.py): el DETECTIVE (fedora, gabardina de cuello alzado, cigarro) y figuras de reparto
(testigos, científicos, jugadores). Claroscuro de novela gráfica: masas oscuras, contraluz blanco del lado de la lámpara, sombras
con tramado de plumilla (Noir.pieza) y tinta que hierve a 12 dibujos/s.

    det = Detective()
    det.dibujar(h, dict(x=900, y=980, s=1.0, d=1, luz=(0.3, -1), fumar=0.0, giro=0.0, paso=0.0, andar=0.0, viento=0.3, ...))
    det.punta_cigarro(pose) -> (x, y) del mundo (para el humo y el brillo de la brasa)

Coordenadas locales: pies en (0, 0), arriba negativo, ~560 px de alto a s = 1, mirando a la derecha (d = 1) en vista 3/4.
`luz` = dirección HACIA la luz en pantalla (p. ej. farola arriba: (0.2, -1); ventana a la izquierda: (-1, -0.3)).
"""
import math

import numpy as np

from toon import blob, elipse_, suave, tubo, eje_curvo
from noir import gris

TONOS = dict(abrigo=78, sombrero=40, cinta=12, piel=118, camisa=190, corbata=16, pantalon=34, zapato=14, mano=112)


def _ik_adelante(S, Hd, l1, l2):
    """Codo continuo: de las dos soluciones toma siempre la que queda más adelante (x local mayor); no salta de lado."""
    a = _ik(S, Hd, l1, l2, 1.0)
    b = _ik(S, Hd, l1, l2, -1.0)
    return a if a[0] >= b[0] else b


def _ik(S, Hd, l1, l2, flex=1.0):
    """Codo de un brazo de 2 huesos (hombro S, mano Hd); flex = lado hacia el que dobla (+1 / -1)."""
    S, Hd = np.asarray(S, float), np.asarray(Hd, float)
    d = Hd - S
    L = float(np.hypot(*d))
    L = min(max(L, 1e-3), l1 + l2 - 1e-3)
    a = (l1 * l1 - l2 * l2 + L * L) / (2 * L)
    hgt = math.sqrt(max(0.0, l1 * l1 - a * a))
    u = d / (np.hypot(*d) + 1e-9)
    n = np.array([-u[1], u[0]]) * flex
    return S + u * a + n * hgt


def avance_paso(zancada, s=1.0):
    """Px del mundo que avanza el cuerpo por radián de fase para que el pie apoyado NO patine: fase = distancia / avance_paso."""
    return 2.0 * zancada * s / math.pi


def pierna_paso(ph, cad, l1, l2, zancada, alt, suelo=0.0):
    """Una pierna del ciclo de caminar (perfil, mirando a +x). ph en rad (la otra pierna va a ph + pi). Media vuelta APOYADA: el
    pie va pegado al suelo de delante (+zancada) hacia atrás, con la pierna casi recta; la otra media en el AIRE: el pie se levanta
    y vuelve hacia delante con la rodilla doblada AL FRENTE (si la rodilla dobla mientras el pie va hacia atrás, el personaje
    parece caminar de espaldas). Devuelve (rodilla, pie) en px locales; cad = cadera."""
    cad = np.asarray(cad, float)
    u = ((ph - math.pi / 2) / (2 * math.pi)) % 1.0
    if u < 0.5:                                   # apoyo
        pie = np.array([cad[0] + zancada * (1 - 4 * u), suelo])
    else:                                         # vuelo
        v = (u - 0.5) * 2
        e = v * v * (3 - 2 * v)
        pie = np.array([cad[0] - zancada + 2 * zancada * e, suelo - alt * math.sin(math.pi * v) ** 1.5])
    return _ik_adelante(cad, pie, l1, l2), pie


def cadera_paso(ph, largo, zancada):
    """Altura de la cadera sobre el suelo para que la pierna APOYADA vaya casi estirada todo el paso (péndulo invertido: el
    cuerpo sube al pasar sobre el pie y baja cuando los dos pies tocan). largo = un poco menos que muslo + pantorrilla."""
    u = ((ph - math.pi / 2) / (2 * math.pi)) % 0.5
    return math.sqrt(max(1.0, largo * largo - (zancada * (1 - 4 * u)) ** 2))


class Detective:
    ZANCADA = 86.0                                # fase sin patinar: paso = distancia / avance_paso(Detective.ZANCADA, s)

    def __init__(self, sem=0, tonos=None):
        self.sem = sem
        self.k = dict(TONOS)
        self.k.update(tonos or {})

    def _T(self, p):
        x, y, s, d = p["x"], p["y"], p["s"], p["d"]
        inc = p.get("inclina", 0.0)

        def f(P):
            P = np.asarray(P, float)
            lx = P[..., 0] + inc * (-P[..., 1]) * 0.12
            return np.stack([x + d * s * lx, y + s * P[..., 1]], -1)
        return f

    def _piernas(self, p):
        fase, amp = p.get("paso", 0.0), p.get("andar", 0.0)
        out = []
        for k in (0, 1):
            ph = fase + (math.pi if k == 0 else 0.0)
            cad = np.array([-10.0 + 20 * k, -cadera_paso(ph, 294.5, self.ZANCADA * amp)])
            rod, pie = pierna_paso(ph, cad, 150, 146, self.ZANCADA * amp, 30 * amp * amp)
            out.append((cad, rod, pie))
        return out

    def dibujar(self, h, p):
        T = self._T(p)
        s, d = p["s"], p["d"]
        k = self.k
        w = 7.0 * s
        sem = self.sem
        L = p.get("luz", (0.25, -1.0))
        rim = p.get("rim", 0.9)
        dd = 22 * s
        vien = p.get("viento", 0.0) + 0.06 * math.sin(h.t * 2.3 + sem)
        quieto = 1.0 - min(1.0, p.get("andar", 0.0))
        bob = -5 * p.get("andar", 0.0) * abs(math.cos(p.get("paso", 0.0))) - 2.2 * quieto * (0.5 + 0.5 * math.sin(h.t * 1.6 + sem))
        rasp = p.get("hombros", 0.0) + 0.25 * quieto * math.sin(h.t * 1.6 + sem)
        p = dict(p)
        p["inclina"] = p.get("inclina", 0.0) + 0.05 * quieto * math.sin(h.t * 0.45 + sem)      # cambia el peso de pie
        T = self._T(p)

        def pz(P, tono, sm, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", dd), **kw)

        # ---- piernas (debajo de la gabardina)
        for i, (cad, rod, pie) in enumerate(self._piernas(p)):
            eje = np.vstack([eje_curvo(cad, rod, 3, 10), eje_curvo(rod, pie, -3, 10)[1:]])
            pz(tubo(eje, 40, 30, 36), k["pantalon"] + (8 if i else 0), 10 + i, rim=rim * 0.7)
            pz(blob(pie[0] + 16, pie[1] - 10, 32, 12, rad=[1, 1.05, 0.95, 0.8, 0.9, 1.1, 1.2, 1.1], n=8), k["zapato"], 12 + i,
               rim=rim * 0.9, d=10 * s, trama=0)
        # ---- brazo de atrás (mano en el bolsillo)
        Sb = np.array([-50.0, -402 + bob + rasp * 10])
        Hb = np.array([-44.0 + 6 * vien, -262.0 + bob])
        Eb = _ik(Sb, Hb, 84, 84, -1)
        pz(tubo(np.vstack([eje_curvo(Sb, Eb, 0, 8), eje_curvo(Eb, Hb, 0, 8)[1:]]), 44, 38, 46), k["abrigo"] - 22, 20)
        # ---- gabardina
        hx = 24 * vien
        cuerpo = [(-64, -404 + bob + rasp * 10), (-34, -418 + bob + rasp * 12), (16, -420 + bob + rasp * 12),
                  (58, -408 + bob + rasp * 10), (68, -372 + bob), (60, -300 + bob), (66, -232), (80 + hx * 0.4, -160),
                  (66 + hx, -138), (34 + hx * 0.8, -147), (2 + hx * 0.7, -140), (-34 + hx * 0.8, -149), (-70 + hx * 1.1, -142),
                  (-80 + hx * 0.7, -160), (-66, -236), (-60, -300 + bob), (-72, -362 + bob)]
        pz(suave(cuerpo, 6), k["abrigo"], 30, w=w * 1.15, d=dd * 1.3)
        # hombreras, bolsillo con solapa y pliegues
        pz([(30, -414 + bob), (62, -404 + bob), (64, -384 + bob), (34, -392 + bob)], k["abrigo"] + 10, 38, w=w * 0.6, d=8 * s)
        pz([(18, -236), (60, -240), (58, -222), (20, -218)], k["abrigo"] - 8, 39, w=w * 0.6, d=8 * s, trama=0)
        for a, b, c in (((-24, -284), (-32 + hx * 0.4, -220), (-40 + hx * 0.8, -150)),
                        ((26, -282), (34 + hx * 0.3, -226), (38 + hx * 0.7, -148)),
                        ((-4, -280), (-2 + hx * 0.3, -210), (2 + hx * 0.7, -142)),
                        ((48, -396), (54, -360), (56, -318))):
            h.trazo(T(np.array([a, b, c], float)), 3.0 * s, sem + 31, color=gris(12), alfa=0.85)
        # cinturón con hebilla y la punta colgando
        pz([(-60, -308 + bob), (60, -308 + bob), (62, -286 + bob), (-61, -287 + bob)], k["abrigo"] - 30, 32, w=w * 0.7, d=6 * s,
           trama=0, rim=rim * 0.6)
        pz([(6, -312 + bob), (28, -312 + bob), (28, -282 + bob), (6, -282 + bob)], 20, 33, w=w * 0.6, d=4 * s, trama=0, rim=0.5)
        pz(suave([(28, -300 + bob), (44 + hx * 0.5, -262), (52 + hx, -232), (40 + hx, -230), (26, -284 + bob)], 3),
           k["abrigo"] - 30, 34, w=w * 0.6, d=6 * s, trama=0)
        # camisa, corbata, solapas y botones
        pz([(-2, -416 + bob), (24, -416 + bob), (17, -350 + bob), (6, -340 + bob)], k["camisa"], 35, w=w * 0.5, d=6 * s, trama=0, rim=0)
        pz([(8, -412 + bob), (16, -412 + bob), (18, -352 + bob), (11, -342 + bob), (5, -354 + bob)], k["corbata"], 36, w=w * 0.4,
           d=4 * s, trama=0, rim=0.3)
        pz([(-8, -420 + bob), (6, -340 + bob), (-18, -362 + bob), (-30, -404 + bob)], k["abrigo"] - 10, 37, w=w * 0.8, d=10 * s)
        pz([(26, -420 + bob), (14, -342 + bob), (40, -368 + bob), (48, -404 + bob)], k["abrigo"] + 12, 40, w=w * 0.8, d=10 * s)
        for by in (-372, -334):
            h.disco(*T(np.array([[-20, by + bob]]))[0], 4.0 * s, gris(16), sem=sem + by)
        # ---- cabeza y brazo delantero
        self._cabeza(h, p, T, w, bob, pz, L)
        self._brazo(h, p, T, w, bob, rasp, pz)

    def _cabeza(self, h, p, T, w, bob, pz, L):
        sem, s, k = self.sem, p["s"], self.k
        arriba = p.get("arriba", 0.0)
        ox, oy = 4.0, bob + p.get("cab_y", 0.0)
        ang = -0.22 * arriba + p.get("cab_rot", 0.0)

        def R(P):
            P = np.asarray(P, float).reshape(-1, 2)
            c0 = np.array([0.0, -440.0])
            c, si = math.cos(ang), math.sin(ang)
            Q = P - c0
            return np.stack([c0[0] + Q[:, 0] * c - Q[:, 1] * si + ox, c0[1] + Q[:, 0] * si + Q[:, 1] * c + oy], 1)
        # cuello
        pz(R([(-16, -448), (18, -446), (22, -410), (-18, -410)]), k["piel"] - 50, 41, w=w * 0.7, rim=0.4)
        # perfil de mandíbula cuadrada
        cara = [(-28, -500), (-2, -526), (28, -514), (37, -494), (34, -485), (40, -480), (55, -463), (43, -457), (41, -452),
                (45, -447), (41, -443), (44, -439), (39, -435), (43, -426), (35, -415), (8, -419), (-10, -436), (-22, -458), (-30, -478)]
        pz(R(suave(cara, 4)), k["piel"], 42, w=w, d=26 * s, rim=p.get("rim", 0.9), trama=0.35)
        # oreja (solo línea), pómulo, surco nasolabial, boca
        h.trazo(T(R([(-10, -476), (-16, -470), (-15, -458), (-9, -454)])), 2.8 * s, sem + 43, alfa=0.9)
        h.trazo(T(R([(36, -460), (30, -448), (32, -440)])), 2.2 * s, sem + 44, alfa=0.6)
        h.trazo(T(R([(30, -445), (42, -446)])), 3.0 * s, sem + 45, alfa=0.9)
        h.trazo(T(R([(8, -421), (26, -428), (36, -438)])), 2.2 * s, sem + 46, alfa=0.45)
        # sombra del ala sobre los ojos
        som = 1 - 0.8 * max(0.0, arriba)
        ala = [(-34, -506), (56, -506), (58, -484 + 10 * arriba), (36, -476 + 10 * arriba), (-30, -482)]
        h.pieza(T(R(ala)), 14, sem + 47, w=0, luz=L, d=1, sombra=0, trama=0, rim=0, alfa=0.9 * som, linea=False, jit=0.5)
        if arriba > 0.3:
            h.pieza(T(R(blob(28, -488, 6, 3.5, n=8))), 230, sem + 48, w=w * 0.45, luz=L, d=1, sombra=0, trama=0)
            h.disco(*T(R([[30, -488]]))[0], 2.6 * s, gris(10))
            h.trazo(T(R([(16, -499), (38, -497)])), 4.0 * s, sem + 49)
        elif p.get("brillo_ojo", 0.0) > 0:
            h.disco(*T(R([[30, -489]]))[0], 2.6 * s, gris(int(40 + 200 * p["brillo_ojo"])))
        # cuello alzado de la gabardina
        pz([(-50, -414 + bob), (-38, -462 + bob), (-14, -446 + bob), (-10, -414 + bob)], k["abrigo"] - 14, 50, w=w * 0.9, d=12 * s)
        pz([(26, -418 + bob), (42, -454 + bob), (58, -422 + bob), (46, -404 + bob)], k["abrigo"] + 14, 51, w=w * 0.9, d=12 * s)
        # fedora
        tilt = p.get("sombrero", 0.0)
        copa = [(-36, -504), (-34, -538), (-24, -557), (-6, -553), (6, -561), (24, -557), (34, -541), (38, -504)]
        pz(R(suave(copa, 5)), k["sombrero"], 52, d=20 * s)
        h.trazo(T(R([(-4, -554), (4, -538), (8, -522)])), 3.0 * s, sem + 53, alfa=0.8)
        pz(R([(-37, -517), (38, -517), (38, -504), (-37, -504)]), k["cinta"], 54, w=w * 0.5, d=4 * s, trama=0, rim=0.5)
        ala_s = elipse_(6, -503, 76, 14, rot=-0.05 + tilt, n=40)
        ala_s[:, 1] += 0.10 * (ala_s[:, 0] - 6)
        pz(R(ala_s), k["sombrero"] - 6, 55, d=10 * s, trama=0.4)

    def _mano_pos(self, p, bob):
        f = p.get("fumar", 0.0)
        sost = p.get("sostener", 0.0)
        reposo = np.array([54.0, -236 + bob])
        boca = np.array([70.0, -446 + bob + p.get("cab_y", 0.0)])
        pecho = np.array([84.0, -336 + bob])
        Hd = reposo + (boca - reposo) * f + np.array([42.0, 0.0]) * math.sin(math.pi * f)     # sube en arco por delante del cuerpo
        return Hd + (pecho - Hd) * sost

    def _brazo(self, h, p, T, w, bob, rasp, pz):
        sem, s, k = self.sem, p["s"], self.k
        S = np.array([44.0, -400 + bob + rasp * 10])
        Hd = self._mano_pos(p, bob)
        E = _ik(S, Hd, 94, 94, 1.0)       # un solo lado: atrás en reposo, abajo al subir, abajo-adelante al fumar
        eje = np.vstack([eje_curvo(S, E, 0, 8), eje_curvo(E, Hd, 0, 8)[1:]])
        pz(tubo(eje, 48, 38, 46), k["abrigo"] + 6, 60, d=20 * s)
        u = (Hd - E) / (np.hypot(*(Hd - E)) + 1e-9)
        n = np.array([-u[1], u[0]])
        pz([Hd - u * 18 + n * 21, Hd - u * 2 + n * 20, Hd - u * 2 - n * 20, Hd - u * 18 - n * 21], k["abrigo"] - 24, 61, w=w * 0.8,
           d=6 * s, trama=0)
        m = blob(Hd[0] + u[0] * 15, Hd[1] + u[1] * 15, 18, 14, rad=[1, 1.15, 1.0, 0.9, 1.0, 1.1], rot=math.atan2(u[1], u[0]), n=8)
        pz(m, k["mano"], 62, w=w * 0.8, d=10 * s, trama=0)
        for i in range(3):
            a = Hd + u * (20 + i * 4) + n * (-9 + i * 7)
            h.trazo(T([a, a + u * 9 + n * 2]), 2.2 * s, sem + 63 + i, alfa=0.7)
        if p.get("cigarro", True):
            c0, c1 = self.cigarro(p)
            h.trazo(T([c0, c1]), 6.0 * s, sem + 66, color=gris(240), taper=(0.05, 0.05), jit=0.3, ruido=0.0)
            h.disco(*T(np.array([c1]))[0], 3.4 * s * (1 + 0.5 * p.get("brasa", 0.0)), gris(255))

    def cigarro(self, p):
        bob = -5 * p.get("andar", 0.0) * abs(math.cos(p.get("paso", 0.0)))
        Hd = self._mano_pos(p, bob)
        f = p.get("fumar", 0.0)
        dirc = np.array([0.9, -0.42]) * (1 - f) + np.array([1.0, 0.1]) * f
        dirc = dirc / np.hypot(*dirc)
        c0 = Hd + np.array([24.0, 0.0])
        return c0, c0 + dirc * 34

    def punta_cigarro(self, p):
        return self._T(p)(np.array([self.cigarro(p)[1]]))[0]


# ======================================================================= reparto
class Figura:
    """Figura de reparto con el mismo claroscuro: traje o bata, sombrero opcional, gafas, hoja en la mano.
    p: x, y, s, d, luz, alto (≈1), ancho (≈1), sombrero, gafas, bata, calvo, pelo (tono), brazo (0 abajo..1 al frente), hoja,
    tono (gris del traje), cabeza (giro), rim."""

    def __init__(self, sem=0):
        self.sem = sem

    def dibujar(self, h, p):
        x, y, s, d = p["x"], p["y"], p["s"], p.get("d", 1)
        al, an = p.get("alto", 1.0), p.get("ancho", 1.0)
        sem = self.sem
        w = 6.5 * s
        L = p.get("luz", (0.25, -1.0))
        rim = p.get("rim", 0.85)

        def T(P):
            P = np.asarray(P, float)
            return np.stack([x + d * s * an * P[..., 0], y + s * al * P[..., 1]], -1)

        def pz(P, tono, sm, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", 20 * s), **kw)
        tono = p.get("tono", 70)
        bata = p.get("bata", False)
        col = 205 if bata else tono
        for k, lx in enumerate((-15, 15)):
            pz(tubo(np.array([[lx, -250], [lx + 2, -130], [lx, -12]], float), 38, 30), 30 + 10 * k, k)
            pz(blob(lx + 11, -8, 25, 10, n=8), 14, 3 + k, d=6 * s, trama=0)
        largo = -150 if bata else -236
        tor = suave([(-54, -402), (-22, -414), (22, -414), (54, -402), (60, -330), (54, -260), (58, largo), (-58, largo),
                     (-54, -260), (-60, -330)], 5)
        pz(tor, col, 10, w=w * 1.05)
        pz([(-9, -414), (9, -414), (5, -348), (-5, -348)], 220, 11, w=w * 0.5, d=4 * s, trama=0, rim=0)
        pz([(-3, -410), (3, -410), (4, -356), (-3, -350)], 20, 12, w=w * 0.4, d=3 * s, trama=0, rim=0)
        h.trazo(T([(-6, -414), (-2, -330), (-4, largo + 10)]), 2.4 * s, sem + 13, alfa=0.6)
        b = p.get("brazo", 0.0)
        for k, lx in enumerate((-52, 52)):
            fin = np.array([lx * 1.05, -248.0]) if k == 0 or b <= 0 else np.array([lx + 70 * b, -322.0 - 30 * b])
            pz(tubo(eje_curvo((lx, -398), fin, 6 if k else -6, 12), 36, 28), col - 8, 20 + k)
            pz(blob(fin[0], fin[1] + 8, 12, 14, n=8), 160, 22 + k, d=6 * s, trama=0)
        if p.get("hoja"):
            hx, hy = (52 + 70 * b), (-332 - 30 * b)
            pz([(hx - 6, hy - 52), (hx + 48, hy - 58), (hx + 52, hy + 10), (hx - 2, hy + 14)], 232, 25, w=w * 0.6, d=4 * s, trama=0,
               rim=0)
            for k in range(4):
                h.trazo(T([(hx + 4, hy - 40 + k * 12), (hx + 40, hy - 43 + k * 12)]), 2.0 * s, sem + 26 + k, alfa=0.5)
        ci = p.get("cabeza", 0.0)
        cab = [(-30, -470), (-26, -494), (-4, -504), (24, -496), (34, -476), (36, -462), (44, -452), (35, -446), (36, -434),
               (30, -424), (8, -420), (-16, -432), (-28, -450)]
        pz(suave(np.array(cab) + (ci * 6, 0), 4), 160, 30, d=22 * s)
        h.trazo(T([(-8 + ci * 6, -470), (-14 + ci * 6, -462), (-10 + ci * 6, -452)]), 2.4 * s, sem + 31, alfa=0.8)
        if not p.get("calvo") and not p.get("sombrero"):
            pelo = [(-32, -468), (-30, -494), (-10, -508), (16, -506), (34, -490), (34, -478), (22, -486), (-4, -488), (-22, -474)]
            pz(suave(np.array(pelo) + (ci * 6, 0), 4), p.get("pelo", 40), 32, w=w * 0.8, d=10 * s)
        elif p.get("calvo"):
            pz(suave(np.array([(-32, -460), (-30, -476), (-24, -470), (-26, -452)]) + (ci * 6, 0), 3), p.get("pelo", 200), 32,
               w=w * 0.6, d=4 * s, trama=0)
        if p.get("gafas"):
            for gx in (10, 30):
                h.anillo(T(elipse_(gx + ci * 6, -466, 9, 7, n=16)), 2.6 * s, sem + 33 + gx)
            h.disco(*T(np.array([[30 + ci * 6, -468]]))[0], 2.4 * s, gris(250))
        if p.get("sombrero"):
            pz(suave([(-32, -480), (-30, -512), (-8, -524), (18, -520), (32, -508), (34, -480)], 4), 46, 40)
            pz(elipse_(2, -480, 62, 11, n=28), 40, 41, d=8 * s, trama=0.3)
            h.pieza(T([(-34, -482), (44, -482), (44, -462), (-34, -466)]), 14, sem + 42, w=0, luz=L, d=1, sombra=0, trama=0, rim=0,
                    alfa=0.85, linea=False)
        h.trazo(T([(26 + ci * 6, -440), (38 + ci * 6, -441)]), 2.6 * s, sem + 43, alfa=0.85)
        # ojos en cuencas de sombra (luz cenital), cejas y mentón
        for k, ex in enumerate((12, 30)):
            ex += ci * 6
            h.pieza(T(elipse_(ex, -464, 8, 5.5, n=12)), 20, sem + 44 + k, w=0, luz=L, d=1, sombra=0, trama=0, rim=0, linea=False,
                    alfa=0.85, jit=0.3)
            h.disco(*T(np.array([[ex + 2, -465]]))[0], 1.6 * s, gris(220))
            h.trazo(T([(ex - 9, -476), (ex + 9, -478 + (2 if k else -1))]), 3.2 * s, sem + 46 + k, alfa=0.9)
        h.trazo(T([(14 + ci * 6, -426), (32 + ci * 6, -428)]), 2.0 * s, sem + 48, alfa=0.45)


# ======================================================================= busto (primeros planos)
def smooth01(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


class Busto:
    """Primer plano del detective (cabeza y hombros) dibujado a escala de pantalla, con mucho más detalle que el cuerpo entero:
    perfil de mandíbula cuadrada, oreja, barba de tres días punteada, ceja, pómulo, cigarro en los labios, cuello alzado.
    p: x, y (centro de la cara en pantalla), s (≈1 = cabeza de ~420 px), d (1 mira a la derecha), luz, arriba (levanta la
    barbilla y se le ven los ojos), brasa (0..1), cigarro (bool), mano (0..1: entra la mano a quitarse el cigarro),
    tira (0..1: lanza la colilla), boca (0..1 abre un poco para soltar el humo)."""

    def __init__(self, sem=0):
        self.sem = sem

    def _T(self, p):
        x, y, s, d = p["x"], p["y"], p["s"], p.get("d", 1)
        a = p.get("rot", 0.0)
        c, si = math.cos(a), math.sin(a)

        def f(P):
            P = np.asarray(P, float).reshape(-1, 2)
            X = P[:, 0] * c - P[:, 1] * si
            Y = P[:, 0] * si + P[:, 1] * c
            return np.stack([x + d * s * X, y + s * Y], 1)
        return f

    def labios(self, p):
        return self._T(p)(np.array([[150.0, 58 + 6 * p.get("boca", 0.0)]]))[0]

    def punta(self, p):
        return self._T(p)(np.array([self._cig(p)[1]]))[0]

    def _mano_pos(self, p):
        k = p.get("mano", 0.0)
        tira = p.get("tira", 0.0)
        ini = np.array([300.0, 560.0])
        boca = np.array([200.0, 96.0])
        m = ini + (boca - ini) * smooth01(k)
        return m + np.array([200.0, 140.0]) * tira

    def _cig(self, p):
        base = np.array([150.0, 60.0])
        fin = np.array([236.0, 96.0])
        if p.get("mano", 0.0) > 0.85:                        # la mano lo sujeta y se lo lleva
            m = self._mano_pos(p)
            base = m + (-6, -22)
            fin = base + (82, 30 - 70 * p.get("tira", 0.0))
        return base, fin

    def dibujar(self, h, p):
        T = self._T(p)
        s = p["s"]
        sem = self.sem
        L = p.get("luz", (0.8, -0.7))
        w = 9.0 * s
        dd = 40 * s
        rim = p.get("rim", 0.95)
        arriba = p.get("arriba", 0.0)
        boca = p.get("boca", 0.0)

        def pz(P, tono, sm, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tono, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", dd), **kw)
        # hombros, camisa, corbata, solapas
        pz(suave([(-460, 640), (-300, 250), (-150, 205), (40, 210), (230, 262), (400, 420), (470, 640)], 5), 74, 1, d=60 * s)
        pz([(-30, 214), (90, 214), (60, 440), (10, 450)], 196, 2, w=w * 0.6, trama=0, rim=0)
        pz([(18, 220), (56, 222), (64, 262), (40, 276), (14, 260)], 18, 3, w=w * 0.5, trama=0, rim=0.4)
        pz([(26, 270), (52, 270), (70, 450), (14, 450)], 22, 4, w=w * 0.5, trama=0.3, rim=0.3)
        pz([(-40, 210), (20, 440), (-60, 490), (-150, 260)], 58, 5, d=24 * s)
        pz([(96, 210), (80, 450), (200, 400), (230, 266)], 96, 6, d=24 * s)
        h.trazo(T([(-260, 330), (-230, 470), (-250, 620)]), 3.5 * s, sem + 7, alfa=0.7)
        h.trazo(T([(300, 340), (330, 470)]), 3.5 * s, sem + 8, alfa=0.7)
        # cuello
        pz([(-70, 60), (70, 120), (64, 240), (-84, 236)], 92, 9, d=30 * s, trama=0.6)
        # cabeza (perfil a la derecha)
        cab = [(-150, -60), (-138, -130), (-60, -190), (40, -186), (96, -150), (124, -86), (116, -62), (130, -50), (186, 10),
               (142, 22), (138, 40), (152, 52 + 4 * boca), (136, 61 + 6 * boca), (147, 69 + 6 * boca), (130, 84), (144, 118),
               (112, 152), (30, 142), (-36, 102), (-74, 58), (-112, 36)]
        pz(suave(cab, 4), 120, 10, d=46 * s, trama=0.55)
        # barba de tres días: punteado que hierve con la tinta
        r = np.random.default_rng(sem * 31 + h.dib)
        for _ in range(170):
            a = r.uniform(0, 1)
            bx = -20 + a * 150 + r.uniform(-10, 10)
            by = 70 + (1 - a) * 50 + r.uniform(-30, 70) * (0.4 + 0.6 * a)
            if by > 150 - (bx - 30) * 0.05 or (bx > 120 and by < 70):
                continue
            q = T([[bx, by]])[0]
            h.disco(q[0], q[1], 1.6 * s, gris(30))
        # oreja
        pz(suave([(-52, -40), (-30, -48), (-18, -10), (-26, 30), (-44, 36), (-56, 0)], 4), 108, 11, w=w * 0.7, d=14 * s, trama=0.3)
        h.trazo(T([(-42, -26), (-30, -8), (-36, 18)]), 3.2 * s, sem + 12, alfa=0.85)
        # pómulo, surco, boca, mentón, mandíbula
        h.trazo(T([(74, -20), (96, 10), (104, 36)]), 3.0 * s, sem + 13, alfa=0.55)
        h.trazo(T([(150, 30), (128, 50), (126, 72)]), 2.6 * s, sem + 14, alfa=0.6)
        h.trazo(T([(110, 60 + 4 * boca), (148, 58 + 6 * boca)]), 4.5 * s, sem + 15, alfa=0.95)
        h.trazo(T([(90, 120), (124, 122)]), 2.8 * s, sem + 16, alfa=0.5)
        h.trazo(T([(-30, 96), (20, 136), (90, 148)]), 3.0 * s, sem + 17, alfa=0.6)
        # ojo y ceja
        oy = -70
        h.pieza(T(suave([(76, oy - 4), (96, oy - 10), (112, oy - 2), (96, oy + 6)], 3)), 230, sem + 18, w=w * 0.5, luz=L, d=2,
                sombra=0, trama=0, rim=0)
        h.disco(*T([[100, oy - 2]])[0], 5.5 * s, gris(12))
        h.disco(*T([[102, oy - 4]])[0], 1.8 * s, gris(250))
        h.trazo(T([(66, oy - 26), (98, oy - 32), (124, oy - 20)]), 7.0 * s, sem + 19, taper=(0.2, 0.6))
        h.trazo(T([(74, oy + 8), (100, oy + 12)]), 2.4 * s, sem + 20, alfa=0.6)
        # sombra del ala sobre los ojos (salvo que levante la barbilla)
        som = 1 - 0.85 * min(1.0, max(0.0, arriba))
        h.pieza(T([(-160, -150), (200, -150), (210, -88 + 50 * arriba), (130, -40 + 40 * arriba), (-40, -60), (-160, -80)]),
                12, sem + 21, w=0, luz=L, d=1, sombra=0, trama=0, rim=0, alfa=0.9 * som, linea=False, jit=0.5)
        if som > 0.3:
            h.disco(*T([[102, oy - 4]])[0], 2.6 * s, gris(int(170 * som)))
        # cuello alzado
        pz([(-210, 230), (-140, 30), (-70, 70), (-60, 214)], 64, 22, d=30 * s)
        pz([(50, 200), (150, 120), (210, 170), (180, 270)], 104, 23, d=30 * s)
        # fedora
        pz(suave([(-150, -150), (-140, -262), (-96, -320), (-20, -306), (24, -330), (96, -312), (136, -258), (148, -150)], 5),
           46, 24, d=40 * s, trama=0.5)
        h.trazo(T([(-14, -310), (6, -250), (20, -190)]), 4.5 * s, sem + 25, alfa=0.8)
        pz([(-152, -196), (150, -196), (150, -150), (-152, -150)], 12, 26, w=w * 0.6, d=6 * s, trama=0, rim=0.6)
        ala = np.array([[math.cos(a) * 290, math.sin(a) * 52] for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)])
        ala[:, 0] += 10
        ala[:, 1] += -150 + 0.13 * ala[:, 0]
        pz(ala, 40, 27, d=20 * s, trama=0.35)
        h.trazo(T(ala[6:20] + (0, -6)), 3.0 * s, sem + 28, color=gris(170), alfa=0.6)
        # cigarro y mano
        if p.get("cigarro", True):
            c0, c1 = self._cig(p)
            h.trazo(T([c0, c1]), 13 * s, sem + 29, color=gris(240), taper=(0.04, 0.04), jit=0.2, ruido=0.0)
            h.trazo(T([c1 - (c1 - c0) * 0.12, c1]), 13 * s, sem + 30, color=gris(90), taper=(0.04, 0.04), jit=0.2, ruido=0.0)
        if p.get("mano", 0.0) > 0.01:
            m = self._mano_pos(p)
            pz(tubo(np.array([m + (70, 300), m + (44, 140), m + (12, 24)]), 120, 96), 70, 31, d=30 * s)
            pz(suave([m + (-34, -12), m + (20, -44), m + (62, -22), m + (66, 32), m + (20, 54), m + (-26, 36)], 4), 116, 32,
               d=20 * s, trama=0.4)
            for k in range(3):
                a = m + (-28 + k * 4, -6 + k * 12)
                h.trazo(T([a, a + (-30, -8)]), 3.0 * s, sem + 33 + k, alfa=0.7)


# ======================================================================= reparto DE FRENTE (rueda de reconocimiento, póker, multitudes)
class Frontal:
    """Figura de frente con claroscuro cenital (cuencas de los ojos en sombra, sombra de la nariz y del mentón).
    p: x, y (pies), s, luz, traje (tono), pelo ('blanco' | 'oscuro' | 'calvo' | 'sombrero' | 'rizado'), alto, ancho,
    placa (bool: sujeta la placa con las dos manos), mira (-1..1 desvía la mirada), gafas, barba (bool), cabeza (inclinación rad)."""

    def __init__(self, sem=0):
        self.sem = sem

    def dibujar(self, h, p):
        x, y, s = p["x"], p["y"], p["s"]
        al, an = p.get("alto", 1.0), p.get("ancho", 1.0)
        sem = self.sem
        L = p.get("luz", (0.0, -1.0))
        w = 6.5 * s
        rim = p.get("rim", 0.85)
        tono = p.get("traje", 64)

        def T(P):
            P = np.asarray(P, float).reshape(-1, 2)
            return np.stack([x + s * an * P[:, 0], y + s * al * P[:, 1]], 1)

        def pz(P, tn, sm, **kw):
            kw.setdefault("rim", rim)
            return h.pieza(T(P), tn, sem + sm, w=kw.pop("w", w), luz=L, d=kw.pop("d", 18 * s), **kw)
        # piernas y zapatos
        for k, sx in enumerate((-1, 1)):
            pz([(sx * 6, -262), (sx * 52, -262), (sx * 46, -14), (sx * 14, -14)], 34 + 8 * k, k, trama=0.5)
            pz(suave([(sx * 10, -18), (sx * 54, -22), (sx * 62, -4), (sx * 8, 0)], 3), 14, 2 + k, d=5 * s, trama=0)
        # saco
        saco = suave([(-74, -398), (-30, -414), (30, -414), (74, -398), (84, -350), (76, -250), (70, -236), (-70, -236), (-76, -250),
                      (-84, -350)], 5)
        pz(saco, tono, 10, trama=0.55)
        pz([(-18, -414), (18, -414), (10, -320), (-10, -320)], 210, 11, w=w * 0.5, d=4 * s, trama=0, rim=0)          # camisa
        pz([(-6, -410), (6, -410), (8, -330), (0, -318), (-8, -330)], 18, 12, w=w * 0.4, d=3 * s, trama=0, rim=0.3)  # corbata
        pz([(-30, -416), (-4, -310), (-26, -300), (-50, -396)], tono - 14, 13, w=w * 0.7, d=8 * s)                  # solapas
        pz([(30, -416), (4, -310), (26, -300), (50, -396)], tono + 10, 14, w=w * 0.7, d=8 * s)
        for by in (-292, -262):
            h.disco(*T([[0, by]])[0], 3.2 * s, gris(20))
        # brazos: sujetan la placa delante del pecho o cuelgan
        placa = p.get("placa", False)
        for k, sx in enumerate((-1, 1)):
            ho = np.array([sx * 76.0, -392])
            if placa:
                mano = np.array([sx * 94.0, -300])
                codo = np.array([sx * 104.0, -330])
            else:
                mano = np.array([sx * 80.0, -230])
                codo = np.array([sx * 90.0, -310])
            pz(tubo(np.vstack([eje_curvo(ho, codo, 0, 8), eje_curvo(codo, mano, 0, 8)[1:]]), 40, 30, 36), tono - 6, 20 + k, d=14 * s)
            if not placa:
                pz(blob(mano[0], mano[1] + 10, 13, 17, n=8), 150, 22 + k, d=6 * s, trama=0)
        # cuello y cabeza
        pz([(-17, -446), (17, -446), (20, -406), (-20, -406)], 112, 30, w=w * 0.7, d=10 * s, trama=0.5)
        inc = p.get("cabeza", 0.0)
        mi = p.get("mira", 0.0)
        cab = suave([(-36, -488), (-30, -516), (0, -528), (30, -516), (36, -488), (36, -462), (30, -440), (14, -424), (0, -420),
                     (-14, -424), (-30, -440), (-36, -462)], 4)
        cab = np.asarray(cab) + (inc * 20, 0)
        pz(cab, 158, 31, d=16 * s, trama=0.35)
        for k, sx in enumerate((-1, 1)):                    # orejas
            pz(suave([(sx * 34, -474), (sx * 44, -478), (sx * 46, -458), (sx * 36, -448)], 3) + np.array([inc * 20, 0]), 130, 32 + k,
               w=w * 0.6, d=4 * s, trama=0)
        cx = inc * 20
        # claroscuro cenital: cuencas de los ojos en sombra, sombra de la nariz, labio y mentón
        for k, sx in enumerate((-1, 1)):
            h.pieza(T(elipse_(cx + sx * 14, -470, 12, 7, n=14)), 14, sem + 34 + k, w=0, luz=L, d=1, sombra=0, trama=0, rim=0,
                    linea=False, alfa=0.9, jit=0.3)
            h.disco(*T([[cx + sx * 14 + mi * 3, -469]])[0], 1.8 * s, gris(200))
            h.trazo(T([(cx + sx * 4, -482), (cx + sx * 24, -480 - (2 if sx > 0 else 0))]), 4.0 * s, sem + 36 + k, alfa=0.95)
        h.pieza(T([(cx - 4, -472), (cx + 4, -472), (cx + 8, -450), (cx - 8, -450)]), 120, sem + 38, w=2.5 * s, luz=L, d=3, trama=0,
                rim=0.8)
        h.pieza(T(elipse_(cx, -446, 12, 3.5, n=12)), 30, sem + 39, w=0, luz=L, d=1, sombra=0, trama=0, rim=0, linea=False, alfa=0.7)
        h.trazo(T([(cx - 11, -436), (cx + 11, -436)]), 3.0 * s, sem + 40, alfa=0.9)
        h.trazo(T([(cx - 8, -428), (cx + 8, -428)]), 2.0 * s, sem + 41, alfa=0.4)
        if p.get("barba"):
            pz(suave([(cx - 30, -446), (cx - 18, -424), (cx, -414), (cx + 18, -424), (cx + 30, -446), (cx + 14, -432), (cx - 14, -432)],
                     3), 40, 42, w=w * 0.6, d=4 * s, trama=0.4)
        if p.get("gafas"):
            for sx in (-1, 1):
                h.anillo(h.tf(T(elipse_(cx + sx * 15, -470, 11, 8, n=16))), 2.6 * s * h.zoom, sem + 43 + sx)   # anillo va en pantalla
            h.trazo(T([(cx - 4, -471), (cx + 4, -471)]), 2.4 * s, sem + 45)
        pelo = p.get("pelo", "oscuro")
        if pelo == "blanco":
            pz(suave([(cx - 40, -470), (cx - 38, -504), (cx - 12, -530), (cx + 20, -530), (cx + 40, -506), (cx + 42, -470), (cx + 34, -490),
                      (cx + 10, -508), (cx - 20, -506), (cx - 34, -488)], 4), 225, 46, w=w * 0.8, d=6 * s, trama=0, rim=0.5)
            for k in range(5):
                h.trazo(T([(cx - 30 + k * 14, -520), (cx - 24 + k * 14, -506)]), 2.0 * s, sem + 47 + k, alfa=0.5)
        elif pelo == "oscuro":
            pz(suave([(cx - 38, -474), (cx - 36, -510), (cx - 10, -532), (cx + 22, -530), (cx + 40, -508), (cx + 38, -476), (cx + 28, -500),
                      (cx - 6, -508), (cx - 28, -498)], 4), 26, 46, w=w * 0.8, d=6 * s, trama=0.2)
        elif pelo == "rizado":
            for k in range(9):
                a = math.pi * (0.05 + 0.9 * k / 8)
                pz(elipse_(cx - math.cos(a) * 34, -496 - math.sin(a) * 30, 15, 13, n=12), 30, 46 + k, w=w * 0.6, d=4 * s, trama=0.2)
        elif pelo == "calvo":
            for sx in (-1, 1):
                pz(suave([(cx + sx * 34, -460), (cx + sx * 38, -490), (cx + sx * 30, -486), (cx + sx * 28, -462)], 3), 60, 46 + sx,
                   w=w * 0.5, d=3 * s, trama=0)
        elif pelo == "sombrero":
            pz(suave([(cx - 34, -500), (cx - 32, -540), (cx - 6, -556), (cx + 6, -548), (cx + 30, -552), (cx + 36, -500)], 4), 40, 46,
               d=10 * s, trama=0.4)
            pz(elipse_(cx, -500, 66, 11, n=30), 34, 47, d=6 * s, trama=0.3)
            h.pieza(T([(cx - 38, -500), (cx + 38, -500), (cx + 38, -478), (cx - 38, -480)]), 12, sem + 48, w=0, luz=L, d=1, sombra=0,
                    trama=0, rim=0, linea=False, alfa=0.8)

    def manos_placa(self, h, p, y_placa):
        """Las manos se dibujan DESPUÉS de la placa (la sujetan por los lados)."""
        x, y, s = p["x"], p["y"], p["s"]
        an = p.get("ancho", 1.0)
        for k, sx in enumerate((-1, 1)):
            mx = x + s * an * sx * 96
            h.pieza(blob(mx, y_placa, 14 * s, 18 * s, n=8), 150, self.sem + 80 + k, w=5 * s, luz=p.get("luz", (0, -1)), d=5 * s,
                    trama=0, rim=0.6)
