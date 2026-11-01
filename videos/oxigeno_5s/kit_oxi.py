# -*- coding: utf-8 -*-
"""Utilería propia del video «oxígeno 5 s» (vector plano estilo Kurzgesagt, sin contornos): átomos y moléculas, llamas y
humo, velas, parrilla, coches, jumbo, central térmica, torres de luz, semáforo, farola, nubes, pinos, peces, perro,
pájaros, cohete, satélite y balanza. Coordenadas locales en px (origen en la base salvo que se diga otra cosa)."""
import math

import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer, SOMBRA, TINTA
from motor import circulo, elipse, rect_red, catmull, clamp01, lerp, h01, ruido1

# ======================================================================== átomos y moléculas
COL_AT = dict(O=(236, 72, 84), N=(84, 140, 240), H=(236, 242, 255), Si=(160, 150, 196), C=(86, 84, 108),
              Fe=(176, 182, 196))
R_AT = dict(O=20, N=21, H=13, Si=24, C=21, Fe=23)
FORMAS = {   # (átomo, dx, dy) en px locales
    "O2": [("O", -15, 0), ("O", 15, 0)],
    "N2": [("N", -16, 0), ("N", 16, 0)],
    "H2": [("H", -9, 0), ("H", 9, 0)],
    "H2O": [("O", 0, 0), ("H", -21, 14), ("H", 21, 14)],
    "CO2": [("O", -34, 0), ("C", 0, 0), ("O", 34, 0)],
    "O": [("O", 0, 0)], "H": [("H", 0, 0)], "N": [("N", 0, 0)], "Si": [("Si", 0, 0)], "Fe": [("Fe", 0, 0)],
}


def atomo(lz, x, y, r, col, alfa=1.0, brillo=0.0):
    if alfa <= 0.01 or r <= 0.3:
        return
    if brillo > 0.01:
        lz.halo(x, y, r * 2.6, col, alfa=0.55 * brillo * alfa, r0=0.3)
    lz.relleno(circulo(x, y, r, 28), col, alfa=alfa)
    lz.relleno(P.terminador(x, y, r, -math.pi * 0.75, 0.25, 16), oscurecer(col, 0.35), alfa=0.35 * alfa)
    lz.relleno(circulo(x - r * 0.35, y - r * 0.38, r * 0.28, 14), (255, 255, 255), alfa=0.55 * alfa)


def fantasma(lz, x, y, r, col=(255, 255, 255), alfa=0.8, fase=0.0, ancho=2.6):
    """Círculo punteado: el hueco que deja un átomo que ha desaparecido."""
    if alfa <= 0.01:
        return
    P.discontinua(lz, P.arco_pts(x, y, r, 0, 2 * math.pi, 40), col + (int(255 * alfa),) if len(col) == 3 else col,
                  ancho, r * 0.38, r * 0.3, fase=fase)


def molecula(lz, x, y, s, tipo="O2", rot=0.0, alfa=1.0, falta_o=0.0, hueco=0.0, brillo_o=0.0, col_o=None):
    """Molécula de esferas. falta_o 0..1: los oxígenos se desvanecen (si hueco > 0 queda su círculo punteado)."""
    if alfa <= 0.01 or s <= 0.01:
        return
    with lz.grupo(x, y, s, rot):
        for el, dx, dy in sorted(FORMAS[tipo], key=lambda a: a[0] == "O"):
            r = R_AT[el]
            a = alfa
            if el == "O":
                a = alfa * (1 - falta_o)
                if hueco > 0.01 and falta_o > 0.05:
                    fantasma(lz, dx, dy, r, (255, 255, 255), alfa=hueco * alfa * min(1.0, falta_o * 2))
            atomo(lz, dx, dy, r, (col_o or COL_AT[el]) if el == "O" else COL_AT[el], a, brillo_o if el == "O" else 0.0)


# ======================================================================== fuego, humo
def llama(lz, x, y, s, t, seed=0, fuerza=1.0, capa=None):
    """Llama que parpadea (origen en la base). fuerza 0..1 (0 = apagada)."""
    if fuerza <= 0.02:
        return
    f = fuerza
    fl = 1 + 0.12 * math.sin(t * 17 + seed * 3) + 0.08 * math.sin(t * 29 + seed)
    lean = 0.18 * math.sin(t * 6 + seed * 1.3)
    with lz.grupo(x, y, s * (0.25 + 0.75 * f)):
        lz.halo(0, -26, 70 * f, (255, 150, 60), alfa=0.45 * f, r0=0.1, capa=capa)
        for (h, w, col) in ((70, 26, (255, 112, 52)), (52, 18, (255, 176, 64)), (32, 10, (255, 236, 160))):
            hh = h * fl
            pts = np.array([[-w, 0], [-w * 0.95, -hh * 0.35], [-w * 0.4 + lean * hh * 0.3, -hh * 0.75],
                            [lean * hh * 0.5, -hh], [w * 0.4 + lean * hh * 0.3, -hh * 0.72], [w * 0.95, -hh * 0.35],
                            [w, 0], [0, w * 0.55]])
            lz.relleno(catmull(pts, 6, True), col, capa=capa)


def humo(lz, x, y, s, t, t0, dur=2.6, col=(200, 200, 214), n=6, seed=0, alfa=0.8, sube=180.0):
    """Hilos de humo que suben desde (x, y) a partir de t0 (cuando algo se apaga) y se disipan."""
    u = t - t0
    if u <= 0 or u > dur + 1.2:
        return
    with lz.grupo(x, y, s):
        for i in range(n):
            v = u - i * 0.12
            if v <= 0:
                continue
            k = v / dur
            if k > 1.3:
                continue
            yy = -sube * k * (1 + 0.15 * i)
            xx = 18 * math.sin(v * 3 + i + seed) + 12 * i * k * (1 if i % 2 else -1)
            r = 8 + 22 * k
            lz.relleno(circulo(xx, yy, r, 22), col, alfa=alfa * max(0.0, 1 - k) * (1 - 0.1 * i))


def columna_humo(lz, x, y, s, t, col=(214, 214, 226), n=9, vel=0.22, ancho=1.0, alfa=0.85, viento=60.0, alto=520.0):
    """Penacho continuo de chimenea (origen en la boca)."""
    with lz.grupo(x, y, s):
        us = sorted(((t * vel + i / n) % 1.0, i) for i in range(n))
        for u, i in reversed(us):
            r = (26 + 70 * u) * ancho
            lz.relleno(circulo(viento * u ** 1.4 * 3 + 10 * math.sin(u * 6 + i), -alto * u, r, 30), col,
                       alfa=alfa * (1 - u) ** 0.8)


def vela(lz, x, y, s, t, fuego=1.0, seed=0, col=(250, 240, 226), t_apaga=None):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-9, -46, 18, 46, 4), col)
        lz.relleno(rect_red(-9, -46, 6, 46, 3), aclarar(col, 0.5), alfa=0.6)
        lz.relleno(elipse(0, 0, 18, 5, 0, 16), (200, 190, 176))
        lz.trazo(np.array([[0, -46], [1, -54]]), TINTA, 2.4, afinar=False)
        llama(lz, 0.5, -52, 0.32, t, seed, fuego)
        if t_apaga is not None:
            humo(lz, 1, -54, 0.35, t, t_apaga, dur=2.0, n=4, seed=seed, alfa=0.7)


def parrilla(lz, x, y, s, t, fuego=1.0, brasas=1.0, t_apaga=None):
    """Asador de carbón redondo con patas, brasas y llamitas."""
    with lz.grupo(x, y, s):
        for a in (-1, 1):
            lz.trazo(np.array([[a * 20, -70], [a * 44, 0]]), (70, 64, 86), 7, afinar=False)
        lz.trazo(np.array([[0, -70], [0, 0]]), (70, 64, 86), 7, afinar=False)
        # brasas
        bc = mezcla((70, 60, 70), (255, 120, 50), brasas)
        lz.halo(0, -96, 90, (255, 120, 50), alfa=0.35 * brasas * (0.8 + 0.2 * math.sin(t * 5)))
        for i in range(7):
            lz.relleno(circulo(-36 + i * 12, -96 - 3 * (i % 2), 9, 14), mezcla(bc, (255, 200, 90), 0.3 * (i % 2) * brasas))
        for i in range(4):
            llama(lz, -30 + i * 20, -98, 0.5, t, i, fuego)
        # cuba
        P_ = np.concatenate([[[-62, -100]], P.arco_pts(0, -100, 62, 0.0, math.pi, 24)[::-1][::-1], [[62, -100]]])
        lz.relleno(P.arco_pts(0, -100, 62, 0, math.pi, 30), (60, 56, 80))
        lz.relleno(P.arco_pts(0, -100, 62, 0.15, math.pi * 0.55, 16).tolist() + [[0, -100]], (88, 84, 112), alfa=0.6)
        # parrilla y comida
        lz.trazo(np.array([[-66, -102], [66, -102]]), (150, 150, 170), 4, afinar=False)
        for i, xx in enumerate((-30, 6, 36)):
            lz.relleno(rect_red(xx - 14, -114, 28, 12, 6), (186, 92, 70) if i != 1 else (236, 196, 90))
        if t_apaga is not None:
            humo(lz, 0, -110, 0.7, t, t_apaga, dur=2.6, n=6)
    _ = P_


def triangulo_fuego(lz, x, y, s, rotura=0.0, alfa=1.0, t=0.0):
    """Triángulo del fuego (combustible, calor, oxígeno); con rotura el lado del oxígeno se cae."""
    if alfa <= 0.01:
        return
    with lz.grupo(x, y, s):
        V = np.array([[0, -150], [-150, 110], [150, 110]], float)
        lados = [(V[1], V[2], (255, 176, 64), "COMBUSTIBLE"), (V[0], V[1], (255, 110, 70), "CALOR"),
                 (V[0], V[2], (236, 72, 84), "OXÍGENO")]
        for i, (a, b, col, txt) in enumerate(lados):
            caida = rotura if i == 2 else 0.0
            off = np.array([60 * caida, 260 * caida ** 2])
            ang = 1.2 * caida
            m = (a + b) / 2 + off
            with lz.grupo(m[0], m[1], 1.0, ang):
                d = (b - a) / 2
                lz.trazo(np.array([-d, d]), col + (int(255 * alfa * (1 - caida ** 3)),), 22, afinar=False)
            ang_t = math.atan2(b[1] - a[1], b[0] - a[0])
            if ang_t > math.pi / 2:
                ang_t -= math.pi
            if ang_t < -math.pi / 2:
                ang_t += math.pi
            n = np.array([-(b - a)[1], (b - a)[0]])
            n = n / np.linalg.norm(n)
            if n @ (m - np.array([0, 23])) < 0:
                n = -n
            P.rotulo(lz, m[0] + n[0] * 44, m[1] + n[1] * 44, txt, 30, alfa=alfa * (1 - caida), rot=ang_t + ang)
        llama(lz, 0, 60, 1.25 * (1 - rotura), t, 3, 1 - rotura)


# ======================================================================== vehículos
def coche(lz, x, y, s, t, col=(236, 90, 90), rueda=0.0, motor=1.0, dir=1, seed=0, faros=0.0):
    """Coche compacto de perfil (origen en el suelo, centro). rueda: ángulo de giro de las ruedas."""
    with lz.grupo(x, y, s):
        with lz.grupo(0, 0, 1.0, 0, None):
            sx = dir
            cuerpo = np.array([[-92, -22], [-92, -48], [-60, -54], [-36, -86], [34, -86], [62, -54], [92, -48], [94, -22]])
            cuerpo[:, 0] *= sx
            lz.relleno(elipse(0, 0, 100, 8, 0, 24), (20, 16, 50), alfa=0.25)
            lz.relleno(catmull(cuerpo, 4, True), col)
            lz.relleno(np.array([[-92 * sx, -40], [94 * sx, -40], [94 * sx, -22], [-92 * sx, -22]]), oscurecer(col, 0.25))
            vent = np.array([[-30, -80], [-4, -80], [-4, -56], [-50, -56]], float)
            vent2 = np.array([[4, -80], [30, -80], [52, -56], [4, -56]], float)
            for v in (vent, vent2):
                v[:, 0] *= sx
                lz.relleno(v, (170, 214, 250))
                lz.relleno(v * [1, 1] + [0, 0], (255, 255, 255), alfa=0.0)
            lz.relleno(rect_red(84 * sx - 6, -50, 12, 8, 3), mezcla((255, 236, 170), (255, 250, 220), faros))
            if faros > 0.05:
                lz.halo(90 * sx, -46, 60, (255, 240, 180), alfa=0.6 * faros)
            lz.relleno(rect_red(-94 * sx - 4, -48, 8, 8, 3), (230, 60, 60))
            for wx in (-56, 58):
                with lz.grupo(wx * sx, -18, 1.0, rueda * sx):
                    lz.relleno(circulo(0, 0, 20, 24), (44, 40, 62))
                    lz.relleno(circulo(0, 0, 9, 16), (190, 190, 206))
                    lz.relleno(rect_red(-2, -9, 4, 18, 2), (120, 120, 140))
            if motor > 0.02:   # escape: bocanadas
                for i in range(3):
                    u = (t * 1.6 + i / 3 + seed * 0.37) % 1
                    lz.relleno(circulo(-(100 + 50 * u) * sx, -26 - 14 * u, 6 + 12 * u, 14), (210, 210, 222),
                               alfa=0.55 * motor * (1 - u))


def avion(lz, x, y, s, t, motores=1.0, rot=0.0, dir=1, estela=0.0, col=(244, 246, 252), franja=(60, 110, 200), luz=0.0):
    """Jumbo de 4 motores de perfil (origen en el centro). motores 0..1 (encendidos)."""
    sx = dir
    with lz.grupo(x, y, s, rot):
        def X(p):
            q = np.array(p, float)
            q[:, 0] *= sx
            return q
        # ala lejana y motores lejanos
        lz.relleno(X([[-10, -6], [40, -6], [-70, -64], [-92, -64]]), oscurecer(col, 0.35))
        for ex in (-44,):
            lz.relleno(rect_red(ex * sx - 18, -46, 36, 13, 6), oscurecer(col, 0.4))
        # fuselaje con joroba
        fus = X([[-250, 2], [-232, -16], [-170, -24], [150, -24], [200, -22], [222, -12], [236, 0], [226, 12], [190, 18],
                 [-150, 18], [-232, 12]])
        lz.relleno(catmull(fus, 4, True), col)
        lz.relleno(catmull(X([[110, -24], [150, -40], [196, -36], [222, -14], [150, -24]]), 4, True), col)
        lz.relleno(X([[-240, 6], [210, 6], [200, 14], [-232, 12]]), franja)
        lz.relleno(X([[-230, 12], [190, 16], [-150, 18]]), oscurecer(col, 0.2), alfa=0.6)
        # cola
        lz.relleno(X([[-200, -22], [-250, -92], [-226, -92], [-160, -24]]), col)
        lz.relleno(X([[-236, -84], [-249, -92], [-226, -92], [-210, -70]]), franja)
        lz.relleno(X([[-210, 0], [-260, 10], [-246, 18], [-190, 8]]), oscurecer(col, 0.15))
        # ventanillas
        for i in range(17):
            lz.relleno(circulo((-150 + i * 18) * sx, -6, 3.2, 8), (90, 120, 180))
        lz.relleno(X([[204, -12], [222, -10], [218, -4], [204, -4]]), (90, 120, 180))
        # ala cercana y motores cercanos
        lz.relleno(X([[-30, 6], [50, 6], [-60, 66], [-86, 66]]), aclarar(col, 0.1))
        lz.relleno(X([[-30, 6], [50, 6], [36, 14], [-36, 14]]), oscurecer(col, 0.2), alfa=0.6)
        for ex, ey in ((-6, 30), (-48, 54)):
            with lz.grupo(ex * sx, ey):
                lz.relleno(rect_red(-24, -9, 48, 18, 9), (206, 210, 224))
                lz.relleno(circulo(22 * sx, 0, 8, 14), (60, 60, 84))
                if motores > 0.02:
                    lz.halo(-30 * sx, 0, 30, (255, 170, 90), alfa=0.5 * motores)
                    lz.relleno(elipse(-34 * sx, 0, 12 * motores, 4, 0, 14), (255, 200, 120), alfa=motores)
        if luz > 0.01:
            parp = 1.0 if (t * 1.2) % 1 < 0.15 else 0.0
            lz.halo(-246 * sx, -92, 22, (255, 80, 80), alfa=parp * luz)
        if estela > 0.01:
            for ey in (30, 54):
                pts = np.array([[(-60 - 30 * k) * sx, ey + 1.5 * k] for k in range(2, 40)], float)
                lz.trazo(pts, (255, 255, 255, int(150 * estela)), 6, afinar=False)


# ======================================================================== ciudad
def semaforo(lz, x, y, s, t, on=1.0, fase=0.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-4, -150, 8, 150, 3), (70, 74, 96))
        lz.relleno(rect_red(-15, -206, 30, 70, 8), (52, 54, 76))
        ciclo = (t * 0.25 + fase) % 1
        act = 0 if ciclo < 0.45 else (1 if ciclo < 0.55 else 2)
        for i, col in enumerate(((230, 60, 60), (255, 196, 60), (90, 220, 120))):
            enc = on if i == act else 0.0
            c = mezcla((40, 40, 60), col, 0.25 + 0.75 * enc)
            lz.relleno(circulo(0, -194 + i * 21, 8, 14), c)
            if enc > 0.05:
                lz.halo(0, -194 + i * 21, 26, col, alfa=0.6 * enc)


def farola(lz, x, y, s, on=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-4, -200, 8, 200, 3), (80, 84, 110))
        lz.trazo(np.array([[0, -196], [10, -212], [30, -214]]), (80, 84, 110), 7, afinar=False)
        lz.relleno(rect_red(20, -216, 26, 10, 4), (80, 84, 110))
        lz.relleno(elipse(33, -204, 11, 5, 0, 14), mezcla((90, 90, 110), (255, 236, 160), on))
        if on > 0.05:
            lz.halo(33, -200, 70, (255, 230, 150), alfa=0.35 * on)


def torre_luz(lz, x, y, s, col=(120, 126, 160)):
    """Torre de alta tensión (origen en la base). Devuelve las alturas de los cables (locales)."""
    with lz.grupo(x, y, s):
        lz.trazo(np.array([[-40, 0], [-12, -300]]), col, 6, afinar=False)
        lz.trazo(np.array([[40, 0], [12, -300]]), col, 6, afinar=False)
        for i in range(6):
            y0, y1 = -i * 50, -(i + 1) * 50
            w0, w1 = 40 - 28 * i / 6, 40 - 28 * (i + 1) / 6
            lz.trazo(np.array([[-w0, y0], [w1, y1]]), col, 3, afinar=False)
            lz.trazo(np.array([[w0, y0], [-w1, y1]]), col, 3, afinar=False)
        for yy, w in ((-240, 60), (-290, 44)):
            lz.trazo(np.array([[-w, yy], [w, yy]]), col, 5, afinar=False)
        lz.trazo(np.array([[-12, -300], [0, -330], [12, -300]]), col, 5, afinar=False)


def central(lz, x, y, s, t, llama_f=1.0, humo_f=1.0, alarma=0.0, t_apaga=None):
    """Central térmica: nave de calderas con la llama visible, chimenea alta con humo, cinta de carbón y pila."""
    with lz.grupo(x, y, s):
        # pila de carbón
        lz.relleno(np.array([[-430, 0], [-360, -70], [-300, -84], [-240, -40], [-210, 0]]), (58, 54, 72))
        lz.relleno(np.array([[-360, -70], [-300, -84], [-280, -60], [-330, -50]]), (86, 82, 102))
        lz.trazo(np.array([[-260, -40], [-150, -180]]), (110, 110, 134), 12, afinar=False)
        # chimenea
        lz.relleno(np.array([[150, 0], [170, -620], [214, -620], [234, 0]]), (210, 204, 214))
        lz.relleno(np.array([[150, 0], [170, -620], [186, -620], [176, 0]]), (236, 232, 240))
        for yy in (-560, -520):
            lz.relleno(np.array([[168, yy], [216, yy], [216, yy + 14], [168, yy + 14]]), (226, 76, 70))
        if humo_f > 0.01:
            columna_humo(lz, 192, -626, 1.0, t, col=(220, 220, 232), alfa=0.85 * humo_f, viento=70)
        if t_apaga is not None:
            humo(lz, 192, -630, 2.2, t, t_apaga, dur=3.0, n=6, col=(160, 160, 180), alfa=0.6)
        # nave de calderas
        lz.relleno(rect_red(-180, -320, 330, 320, 6), (196, 184, 196))
        lz.relleno(rect_red(-180, -320, 330, 30, 4), (160, 148, 170))
        lz.relleno(rect_red(-180, -320, 90, 320, 4), (214, 204, 214))
        lz.relleno(rect_red(-90, -200, 120, 120, 10), (60, 50, 76))      # ventana de la caldera
        if llama_f > 0.01:
            with lz.recorte(rect_red(-90, -200, 120, 120, 10)):
                lz.halo(-30, -100, 140, (255, 140, 60), alfa=0.8 * llama_f)
                for i in range(5):
                    llama(lz, -78 + i * 24, -82, 0.9, t, i, llama_f)
        for i in range(4):
            lz.relleno(rect_red(46 + (i % 2) * 52, -280 + (i // 2) * 100, 34, 50, 4), (150, 196, 236))
        # turbina / transformadores
        lz.relleno(rect_red(-330, -150, 140, 150, 6), (172, 164, 186))
        lz.relleno(rect_red(-310, -120, 100, 60, 8), (120, 120, 150))
        for i in range(3):
            lz.relleno(rect_red(-420 + i * 30, -60, 18, 60, 3), (110, 116, 146))
        # luz de alarma
        if alarma > 0.01:
            parp = 0.5 + 0.5 * math.sin(t * 12)
            lz.halo(-20, -336, 60, (255, 60, 60), alfa=0.8 * alarma * parp)
            lz.relleno(circulo(-20, -332, 12, 16), mezcla((120, 40, 50), (255, 80, 80), alarma * parp))


# ======================================================================== naturaleza
def nube(lz, x, y, s, col=(255, 255, 255), alfa=1.0, seed=0, sombra=True):
    with lz.grupo(x, y, s):
        bolas = [(-90, 0, 46), (-40, -22, 60), (24, -30, 70), (86, -6, 50), (0, 6, 56)]
        if sombra:
            lz.relleno(rect_red(-136, -6, 272, 40, 20), oscurecer(col, 0.18), alfa=alfa)
            for bx, by, br in bolas:
                lz.relleno(circulo(bx, by + 8, br, 30), oscurecer(col, 0.12), alfa=alfa)
        for bx, by, br in bolas:
            lz.relleno(circulo(bx, by, br * (1 + 0.04 * math.sin(seed + bx)), 30), col, alfa=alfa)
        lz.relleno(rect_red(-136, -6, 272, 34, 17), col, alfa=alfa)


def pino(lz, x, y, s, col=(60, 150, 110), oscuro=0.0):
    c = mezcla(col, (20, 30, 60), oscuro)
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-7, -40, 14, 42, 4), mezcla((110, 76, 70), (20, 30, 60), oscuro))
        for i, (w, h) in enumerate(((70, -30), (56, -90), (40, -145))):
            lz.relleno(np.array([[-w, h], [0, h - 90], [w, h]]), c)
            lz.relleno(np.array([[0, h - 90], [w, h], [w * 0.2, h]]), oscurecer(c, 0.2), alfa=0.6)


def arbusto(lz, x, y, s, col=(80, 170, 100), seed=0):
    with lz.grupo(x, y, s):
        for i in range(4):
            bx = -40 + i * 27 + 6 * math.sin(seed + i)
            r = 26 + 10 * h01(seed, i)
            lz.relleno(circulo(bx, -r * 0.7, r, 24), col if i % 2 else aclarar(col, 0.08))
        lz.relleno(rect_red(-60, -12, 120, 12, 6), oscurecer(col, 0.15))


def pez(lz, x, y, s, t, col=(255, 170, 70), dir=1, seed=0):
    with lz.grupo(x, y, s):
        sx = dir
        cola = 0.35 * math.sin(t * 8 + seed)
        lz.relleno(elipse(0, 0, 34, 16, 0, 24), col)
        with lz.grupo(-30 * sx, 0, 1.0, cola * sx):
            lz.relleno(np.array([[0, 0], [-22 * sx, -15], [-22 * sx, 15]]), oscurecer(col, 0.15))
        lz.relleno(elipse(4 * sx, 6, 22, 7, 0, 16), aclarar(col, 0.3), alfa=0.7)
        lz.relleno(circulo(18 * sx, -4, 4, 10), (255, 255, 255))
        lz.relleno(circulo(19 * sx, -4, 2, 8), TINTA)


def pajaros(lz, x, y, s, t, n=5, seed=0, col=(60, 60, 96)):
    """Bandada de pájaros lejanos (V que aletean)."""
    for i in range(n):
        px = x + (i * 53 + 30 * math.sin(seed + i)) * s
        py = y + (i % 3) * 24 * s + 10 * math.sin(t * 1.3 + i) * s
        a = 0.5 + 0.4 * math.sin(t * 9 + i * 1.7)
        w = 16 * s
        lz.trazo(np.array([[px - w, py - w * a], [px, py], [px + w, py - w * a]]), col, 3.4 * s, afinar=False)


def perro(lz, x, y, s, t, col=(196, 140, 90), dir=1, corre=0.0):
    sx = dir
    with lz.grupo(x, y, s):
        ph = t * 12 * corre
        lz.relleno(elipse(0, 0, 50, 6, 0, 20), (20, 16, 50), alfa=0.2)
        for k, px_ in enumerate((-30, -18, 20, 32)):
            a = 0.5 * math.sin(ph + k * 1.6) * corre
            with lz.grupo(px_ * sx, -34, 1.0, a):
                lz.relleno(rect_red(-5, 0, 10, 34, 5), oscurecer(col, 0.25 if k % 2 else 0.1))
        with lz.grupo(-44 * sx, -50, 1.0, (0.6 + 0.3 * math.sin(t * 10)) * sx):
            lz.relleno(elipse(-14 * sx, 0, 18, 6, 0, 14), col)
        lz.relleno(elipse(0, -50, 46, 22, 0, 30), col)
        lz.relleno(elipse(4 * sx, -40, 30, 10, 0, 20), aclarar(col, 0.25), alfa=0.8)
        lz.relleno(circulo(44 * sx, -74, 20, 24), col)
        lz.relleno(elipse(62 * sx, -68, 14, 9, 0, 16), aclarar(col, 0.2))
        lz.relleno(circulo(72 * sx, -70, 5, 10), TINTA)
        lz.relleno(elipse(34 * sx, -84, 8, 16, 0.4 * sx, 16), oscurecer(col, 0.3))
        lz.relleno(circulo(50 * sx, -78, 3.5, 8), TINTA)


# ======================================================================== espacio y física
def cohete(lz, x, y, s, t, fuego=1.0, col=(240, 240, 250)):
    """Cohete de etapa criogénica (origen en la base de la tobera)."""
    with lz.grupo(x, y, s):
        if fuego > 0.01:
            fl = 1 + 0.1 * math.sin(t * 30)
            lz.halo(0, 60, 130, (255, 170, 90), alfa=0.6 * fuego)
            lz.relleno(np.array([[-22, 0], [0, 150 * fl * fuego], [22, 0]]), (255, 160, 70))
            lz.relleno(np.array([[-12, 0], [0, 90 * fl * fuego], [12, 0]]), (255, 240, 190))
        lz.relleno(np.array([[-26, 0], [-18, -26], [18, -26], [26, 0]]), (90, 90, 110))
        lz.relleno(rect_red(-36, -300, 72, 276, 10), col)
        lz.relleno(rect_red(-36, -300, 22, 276, 8), aclarar(col, 0.4), alfa=0.7)
        lz.relleno(np.array([[-36, -300], [0, -380], [36, -300]]), (236, 90, 90))
        import ui_base as UB
        for yy, txt, c in ((-250, "O2", (236, 72, 84)), (-130, "H2", (110, 170, 255))):
            lz.relleno(rect_red(-30, yy - 50, 60, 100, 10), aclarar(c, 0.55))
            UB.texto_q(lz, 0, yy, txt, 30, color=oscurecer(c, 0.3), capa=None)
        for a in (-1, 1):
            lz.relleno(np.array([[a * 36, -90], [a * 70, -10], [a * 36, -40]]), (236, 90, 90))


def satelite(lz, x, y, s, t, pegado=0.0, chispa=0.0):
    """Satélite con dos paneles; el brazo de la antena se queda pegado (pegado 0..1)."""
    with lz.grupo(x, y, s):
        for a in (-1, 1):
            lz.relleno(rect_red(a * 60 - (110 if a < 0 else 0), -26, 110, 52, 4), (60, 100, 200))
            for i in range(1, 4):
                xx = a * 60 + (i * 27.5 if a > 0 else -i * 27.5)
                lz.trazo(np.array([[xx, -26], [xx, 26]]), (40, 70, 150), 2.5, afinar=False)
        lz.relleno(rect_red(-44, -46, 88, 92, 10), (232, 200, 110))
        lz.relleno(rect_red(-44, -46, 30, 92, 8), (250, 224, 150), alfa=0.8)
        ang = lerp(-1.2, -0.35, (0.5 + 0.5 * math.sin(t * 2.2)) * (1 - pegado))
        with lz.grupo(0, -46, 1.0, ang):
            lz.relleno(rect_red(-5, -80, 10, 80, 4), (190, 190, 210))
            lz.relleno(P.arco_pts(0, -96, 34, 0, math.pi, 20), (236, 236, 246))
        lz.relleno(circulo(0, -46, 10, 16), (150, 150, 170))
        if chispa > 0.01:
            lz.halo(0, -46, 50, (255, 230, 150), alfa=chispa)


def balanza(lz, x, y, s, inclin=0.0, izq=None, der=None):
    """Balanza de platillos (origen en la base); izq/der: fn(lz) dibujan el contenido de cada platillo (origen en él)."""
    with lz.grupo(x, y, s):
        lz.relleno(np.array([[-70, 0], [70, 0], [20, -30], [-20, -30]]), (110, 100, 150))
        lz.relleno(rect_red(-8, -300, 16, 280, 6), (140, 130, 180))
        with lz.grupo(0, -300, 1.0, inclin):
            lz.relleno(rect_red(-260, -8, 520, 16, 8), (170, 160, 210))
        lz.relleno(circulo(0, -300, 16, 20), (200, 190, 236))
        for lado, fn in ((-1, izq), (1, der)):
            px = lado * 250 * math.cos(inclin)
            py = -300 + lado * 250 * math.sin(inclin)
            lz.trazo(np.array([[px, py], [px - 70, py + 110]]), (170, 160, 210), 3, afinar=False)
            lz.trazo(np.array([[px, py], [px + 70, py + 110]]), (170, 160, 210), 3, afinar=False)
            lz.relleno(np.array([[px - 90, py + 110], [px + 90, py + 110], [px + 60, py + 130], [px - 60, py + 130]]),
                       (200, 190, 236))
            if fn is not None:
                with lz.grupo(px, py + 108):
                    fn(lz)


def ruido(t, seed=0):
    return ruido1(t, seed, 1)
