# -*- coding: utf-8 -*-
"""Piezas propias de «La videollamada donde nadie era real» (estilo noir): Hong Kong de noche, la oficina del empleado,
el MONITOR con la rejilla de la videollamada (caras que se descomponen en máscaras) y el empleado visto de espaldas.

    Llamada(sem).dibujar(h, t, caja, falso=[0..1 por recuadro], habla=k, asiente=0..1, apagado=[0..1])
    espalda(h, x, y, s)            empleado de espaldas (cabeza, hombros, respaldo de la silla) con contraluz de la pantalla
    luz_rect(h, quad, k)           luz rectangular (pantalla encendida) en coordenadas del mundo
"""
import functools
import math

import cv2
import numpy as np

from motor import H, W, clamp01, smooth
from noir import gris
from noir_fondos import Lienzo, edificio, letrero_vertical, texto_lienzo
from noir_pers import Frontal
from toon import blob, elipse_, suave

SW, SH = W // 3, H // 3


def rect(x, y, w, h):
    return np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], float)


def luz_rect(h, quad, k=1.0, suave_=6.0):
    """Luz con forma de cuadrilátero (una pantalla, una puerta abierta). quad en el MUNDO."""
    Q = (h.tf(np.asarray(quad, float)) / 3.0).astype(np.int32)
    m = np.zeros((SH, SW), np.float32)
    cv2.fillConvexPoly(m, Q, 1.0, cv2.LINE_AA)
    if suave_ > 0:
        m = cv2.GaussianBlur(m, (0, 0), suave_)
    h.luz_mascara(m, k)


# ====================================================================== HONG KONG
@functools.lru_cache(maxsize=1)
def hk_cielo():
    """Cielo nocturno cargado, con el resplandor de la ciudad en el horizonte y la silueta del Pico."""
    from noir import fbm
    L = Lienzo(3400, 1700, origen=(-700, -600), base=0.0, sem=301)
    L.poli([(-700, -600), (2700, -600), (2700, 1100), (-700, 1100)], 0.16, tex=0.05, grad=(0.40, -600, 760))
    n = 0.6 * fbm(L.w, L.h, 300, 5, 302) + 0.4 * fbm(L.w, L.h, 80, 3, 303)
    L.g = L.g * (0.75 + 0.5 * n)
    P = [(-700, 760)]
    r = np.random.default_rng(304)
    for x in range(-700, 2701, 100):                       # montañas detrás de la bahía
        P.append((x, 560 - 190 * math.exp(-((x - 700) / 700.0) ** 2) - 110 * math.exp(-((x - 2000) / 500.0) ** 2) + r.uniform(-14, 14)))
    P.append((2700, 760))
    L.poli(P, 0.09, tex=0.08, rug=0.6)
    for k in range(60):                                    # lucecitas en la ladera
        x = r.uniform(-600, 2600)
        L.rect(x, r.uniform(560, 740), 4, 4, 0.9, emis=0.5, tex=0.0)
    return L.capa(opaco=True)


def _torre(L, x, base, ancho, alto, sem, corona="plana", enc=0.3):
    """Rascacielos de cristal con corona propia (aguja, escalonada, tijera) para que el horizonte se lea como Hong Kong."""
    edificio(L, x, base, ancho, alto, tipo="cristal", sem=sem, encendidas=enc, prof_lado=26, detalle=0.9)
    top = base - alto
    cx = x + ancho / 2
    if corona == "aguja":
        L.poli([(cx - ancho * 0.30, top), (cx + ancho * 0.30, top), (cx + ancho * 0.16, top - 130), (cx - ancho * 0.16, top - 130)], 0.16, tex=0.06)
        L.poli([(cx - 5, top - 130), (cx + 5, top - 130), (cx + 1, top - 420), (cx - 1, top - 420)], 0.20, tex=0.0)
        L.rect(cx - 3, top - 426, 6, 6, 1.0, emis=0.9, tex=0.0)
    elif corona == "garras":                                 # coronación en dientes (como la torre del puerto)
        for k in range(6):
            xa = x + ancho * (0.06 + 0.16 * k)
            L.poli([(xa, top), (xa + ancho * 0.10, top), (xa + ancho * 0.05, top - 90 - 30 * (k % 2))], 0.18, tex=0.04)
    elif corona == "tijera":                                 # dos antenas inclinadas
        for sx in (-1, 1):
            L.poli([(cx + sx * ancho * 0.22 - 4, top), (cx + sx * ancho * 0.22 + 4, top), (cx + sx * ancho * 0.10 + 1, top - 300),
                    (cx + sx * ancho * 0.10 - 1, top - 300)], 0.2, tex=0.0)
        L.poli([(x, top), (x + ancho, top), (x + ancho * 0.5, top - 110)], 0.15, tex=0.05)
    elif corona == "escalon":
        L.rect(x + ancho * 0.15, top - 70, ancho * 0.7, 70, 0.15, tex=0.06)
        L.rect(x + ancho * 0.32, top - 130, ancho * 0.36, 60, 0.17, tex=0.06)


@functools.lru_cache(maxsize=1)
def hk_lejos():
    L = Lienzo(3600, 1900, origen=(-500, -1100), sem=311)
    rng = np.random.default_rng(311)
    x = -480
    cor = ["plana", "escalon", "plana", "aguja", "plana", "garras", "escalon", "plana", "tijera"]
    k = 0
    while x < 3080:
        an = rng.uniform(110, 220)
        al = rng.uniform(300, 640)
        _torre(L, x, 760, an, al, int(rng.integers(1e6)), cor[k % len(cor)], enc=0.22)
        x += an + rng.uniform(-10, 50)
        k += 1
    L.e *= 0.75
    return L.capa()


@functools.lru_cache(maxsize=1)
def hk_medio():
    """Primera línea de la bahía: torres de cristal altas (la del centro, x≈880..1160, es la oficina), muelle y agua."""
    L = Lienzo(4300, 3100, origen=(-400, -1900), sem=321)
    filas = [(-380, 250, 560, "escalon"), (-90, 220, 760, "tijera"), (170, 280, 520, "plana"), (490, 240, 680, "garras"),
             (1260, 250, 720, "plana"), (1560, 300, 500, "escalon"), (1900, 230, 860, "aguja"), (2180, 280, 560, "plana"),
             (2500, 250, 700, "garras"), (2800, 300, 500, "escalon"), (3140, 260, 640, "tijera"), (3440, 300, 560, "plana")]
    for i, (x, an, al, co) in enumerate(filas):
        _torre(L, x, 1000, an, al, 400 + i, co, enc=0.26)
    _torre(L, 880, 1000, 280, 1120, 77, "aguja", enc=0.34)
    for x, s in ((330, "BANK"), (1640, "HOTEL"), (2590, "TRUST")):
        letrero_vertical(L, x, 640, s=s, ancho=64, px=52, encendido=0.9)
    L.rect(-400, 1000, 4300, 26, 0.10, tex=0.05)                        # muelle
    for k in range(40):
        L.rect(-380 + k * 108, 986, 6, 16, 0.9, emis=0.6, tex=0.0)       # farolas del paseo
    return L.capa()


@functools.lru_cache(maxsize=1)
def hk_agua():
    """La bahía (opaca) con el brillo roto de la ciudad."""
    L = Lienzo(4300, 700, origen=(-400, 1020), base=0.0, sem=331)
    L.poli([(-400, 1020), (3900, 1020), (3900, 1720), (-400, 1720)], 0.11, tex=0.10, grad=(0.03, 1020, 1700))
    r = np.random.default_rng(332)
    for k in range(260):
        x, y = r.uniform(-400, 3900), 1030 + r.uniform(0, 1) ** 2 * 560
        an = r.uniform(20, 120) * (0.5 + (y - 1020) / 500)
        L.rect(x, y, an, r.uniform(2, 5), r.uniform(0.3, 0.9), alfa=0.55, emis=0.25, tex=0.0)
    return L.capa(opaco=True)


# ====================================================================== OFICINA DEL EMPLEADO (Hong Kong, de noche)
@functools.lru_cache(maxsize=1)
def oficina_hk():
    """Planta de oficina a oscuras: ventanal de suelo a techo con las torres vecinas, cubículos, lámparas apagadas, escritorio
    en primer término (borde en y≈860). Origen (-300, -200), 2520 x 1500."""
    L = Lienzo(2520, 1500, origen=(-300, -200), base=0.0, sem=341)
    L.poli([(-300, -200), (2220, -200), (2220, 1300), (-300, 1300)], 0.13, tex=0.10, grad=(0.09, -200, 900))
    r = np.random.default_rng(342)
    L.rect(-300, -110, 2520, 760, 0.07, tex=0.05, grad=(0.15, -110, 650))      # ventanal: la noche
    x = -300
    while x < 2220:                                                            # torres vecinas tras el cristal
        an, al = r.uniform(90, 200), r.uniform(260, 720)
        L.rect(x, 650 - al, an, al, r.uniform(0.10, 0.17), tex=0.08)
        for j in range(int(al // 26)):
            for i in range(int(an // 18)):
                if r.uniform() < 0.20:
                    L.rect(x + 5 + i * 18, 650 - al + 8 + j * 26, 9, 13, r.uniform(0.6, 1.0), emis=r.uniform(0.3, 0.6), tex=0.0)
        x += an + r.uniform(4, 30)
    for k in range(12):                                                        # montantes del ventanal
        xa = -300 + k * 230
        L.rect(xa - 7, -110, 14, 760, 0.04, tex=0.02)
        L.linea([(xa + 7, -110), (xa + 7, 650)], 1.4, 0.30, alfa=0.5, jit=0.2)
    L.rect(-300, 250, 2520, 8, 0.04)
    L.rect(-300, -200, 2520, 92, 0.10, tex=0.08)                               # falso techo con plafones apagados
    for k in range(7):
        L.rect(-220 + k * 360, -176, 220, 34, 0.20, tex=0.03)
    L.rect(-300, 650, 2520, 30, 0.05)                                          # antepecho
    for k, (xa, an) in enumerate(((-260, 520), (330, 420), (1560, 470), (1990, 240))):   # cubículos al fondo
        L.rect(xa, 600, an, 240, 0.16 + 0.02 * (k % 2), tex=0.14, grad=(0.10, 600, 840))
        L.linea([(xa, 600), (xa + an, 600)], 2.0, 0.34, alfa=0.6, jit=0.3)
        L.rect(xa + an * 0.3, 530, 110, 72, 0.06, tex=0.02)                    # monitores apagados
        L.rect(xa + an * 0.3 + 48, 600, 14, 12, 0.05)
    L.rect(1210, 430, 16, 420, 0.06)                                           # planta y perchero
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.28
        L.poli([(1218, 470), (1218 + 150 * math.cos(a - 0.08), 470 + 190 * math.sin(a - 0.08)),
                (1218 + 170 * math.cos(a), 470 + 210 * math.sin(a))], 0.08, tex=0.05)
    L.poli([(-300, 860), (2220, 860), (2220, 1300), (-300, 1300)], 0.20, tex=0.12, grad=(0.10, 860, 1300))   # el escritorio
    L.linea([(-300, 860), (2220, 860)], 2.4, 0.40, alfa=0.6, jit=0.3)
    return L.capa(opaco=True)


def monitor(h, caja, sem=0, pie=True):
    """Marco del monitor alrededor de caja=(x, y, w, hh) (la pantalla se dibuja aparte, encima)."""
    x, y, w, hh = caja
    b = 26
    h.pieza(rect(x - b, y - b, w + 2 * b, hh + 2 * b + 20), 22, sem, w=6, luz=(0, -1), d=8, trama=0.3, rim=0.5)
    if pie:
        cx = x + w / 2
        h.pieza(np.array([[cx - 60, y + hh + b + 18], [cx + 60, y + hh + b + 18], [cx + 90, y + hh + 150], [cx - 90, y + hh + 150]]), 26,
                sem + 1, w=5, luz=(0, -1), d=8, trama=0.4, rim=0.4)
        h.pieza(elipse_(cx, y + hh + 152, 210, 22, n=30), 30, sem + 2, w=5, luz=(0, -1), d=6, trama=0.3, rim=0.5)


REPARTO = [dict(pelo="blanco", traje=92, gafas=True), dict(pelo="oscuro", traje=52), dict(pelo="calvo", traje=74, barba=True),
           dict(pelo="rizado", traje=44), dict(pelo="oscuro", traje=84, gafas=True), dict(pelo="blanco", traje=60, barba=True)]
ROTULOS = ["DIR. FINANCIERO", "TESORERÍA", "LEGAL", "CONTABILIDAD", "OPERACIONES", "AUDITORÍA"]


class Llamada:
    """La rejilla de la videollamada: cols x filas recuadros con un busto de frente cada uno.
    falso[k] 0..1: el recuadro se descompone (bandas que se desplazan) y la cara queda en una máscara lisa sin rasgos.
    apagado[k] 0..1: el recuadro se va a negro (fin de la llamada). habla: índice del que tiene la palabra (borde claro
    y barras de voz). asiente 0..1: todos asienten a la vez."""

    def __init__(self, sem=0, cols=3, filas=2):
        self.sem, self.cols, self.filas = sem, cols, filas
        self.n = cols * filas
        self.F = [Frontal(sem=sem + 11 * k) for k in range(self.n)]

    def celda(self, caja, k):
        x, y, w, hh = caja
        g = 12
        tw, th = (w - g * (self.cols + 1)) / self.cols, (hh - g * (self.filas + 1)) / self.filas
        i, j = k % self.cols, k // self.cols
        return x + g + i * (tw + g), y + g + j * (th + g), tw, th

    def dibujar(self, h, t, caja, falso=None, habla=None, asiente=0.0, apagado=None, rotulos=True, enc=1.0, mira=None):
        from noir import texto_maquina
        x, y, w, hh = caja
        falso = falso or [0.0] * self.n
        apagado = apagado or [0.0] * self.n
        h.pieza(rect(x, y, w, hh), 14, self.sem + 900, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        for j in range(self.filas):
            for i in range(self.cols):
                k = j * self.cols + i
                cx0, cy0, tw, th = self.celda(caja, k)
                f, ap = falso[k], apagado[k]
                tono = 92 + 14 * ((k * 5) % 3)
                h.pieza(rect(cx0, cy0, tw, th), tono * (1 - 0.8 * ap), self.sem + 800 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                        linea=False, jit=0, grad=(tono * 0.5 * (1 - 0.8 * ap), cy0, cy0 + th))
                if ap >= 0.98:
                    continue
                # fondo del recuadro: una estantería o una persiana detrás de cada uno (oficinas distintas)
                if k % 3 == 0:
                    for q in range(5):
                        h.trazo(np.array([[cx0 + 8, cy0 + th * (0.12 + 0.17 * q)], [cx0 + tw - 8, cy0 + th * (0.12 + 0.17 * q)]]), 2.2,
                                self.sem + 700 + q, alfa=0.35, jit=0.3)
                elif k % 3 == 1:
                    h.pieza(rect(cx0 + tw * 0.62, cy0 + th * 0.10, tw * 0.28, th * 0.36), 150, self.sem + 710 + k, w=3, luz=(0, -1), d=3,
                            trama=0, sombra=0.2)
                else:
                    for q in range(4):
                        h.pieza(rect(cx0 + tw * (0.06 + 0.11 * q), cy0 + th * 0.08, tw * 0.07, th * (0.30 + 0.06 * ((q * 3) % 4))), 60 + 20 * q,
                                self.sem + 720 + q, w=2, luz=(0, -1), d=2, trama=0, sombra=0.2)
                s = 0.46 * th / 110.0
                bal = 0.012 * math.sin(t * 0.8 + k * 1.7)
                nod = asiente * 0.5 * (0.5 - 0.5 * math.cos(t * 6.0 + k * 0.6))
                p = dict(REPARTO[k % len(REPARTO)])
                p.update(x=cx0 + tw / 2 + 5 * math.sin(t * 0.6 + k), y=cy0 + th * 0.44 + 474 * s + nod * 16 * s, s=s, luz=(0.0, -1.0),
                         rim=0.8, cabeza=bal * 3, mira=(mira if mira is not None else 0.5 * math.sin(t * 0.7 + k * 2.1)))
                if f < 0.75:
                    self.F[k].dibujar(h, p)
                else:                                              # la máscara: óvalo liso con dos huecos, sobre el mismo traje
                    p2 = dict(p)
                    self.F[k].dibujar(h, p2)
                    mx, my = p["x"], p["y"] - 474 * s
                    h.pieza(elipse_(mx, my - 2 * s, 46 * s, 62 * s, n=30), 236, self.sem + 600 + k, w=5 * s, luz=(0, -1), d=10 * s,
                            trama=0, rim=0, sombra=0.35)
                    for sx in (-1, 1):
                        h.pieza(elipse_(mx + sx * 17 * s, my - 6 * s, 10 * s, 6 * s, n=14), 6, self.sem + 610 + k, w=0, luz=(0, -1), d=1,
                                sombra=0, trama=0, linea=False, jit=0)
                if ap > 0:
                    h.pieza(rect(cx0, cy0, tw, th), 6, self.sem + 650 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0,
                            alfa=ap)
            # tapar lo que desborda hacia la fila de abajo y el borde inferior
            yb = y + 12 + (j + 1) * ((hh - 12 * (self.filas + 1)) / self.filas + 12) - 12
            h.pieza(rect(x, yb, w, 12 if j < self.filas - 1 else hh + y - yb + 400), 14, self.sem + 950 + j, w=0, luz=(0, -1), d=1,
                    sombra=0, trama=0, linea=False, jit=0)
        for k in range(self.n):
            cx0, cy0, tw, th = self.celda(caja, k)
            if apagado[k] >= 0.98:
                continue
            if rotulos:
                h.pieza(rect(cx0 + 6, cy0 + th - 34, tw * 0.62, 28), 10, self.sem + 500 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                        linea=False, jit=0, alfa=0.8)
                texto_maquina(h, ROTULOS[k % len(ROTULOS)], cx0 + 14, cy0 + th - 32, th * 0.085, t, -99, cps=1e9, tono=0.95,
                              encuadrar=False)
            if habla == k and falso[k] < 0.5:
                h.anillo(h.tf(rect(cx0, cy0, tw, th)), 6 * h.zoom, self.sem + 400 + k, color=(245, 245, 245), jit=0.5)
                for q in range(5):                                # barras de voz
                    a = 6 + 18 * abs(math.sin(t * (9 + q * 2.3) + q))
                    bx = cx0 + tw - 70 + q * 11
                    h.trazo(np.array([[bx, cy0 + th - 20 - a / 2], [bx, cy0 + th - 20 + a / 2]]), 5, self.sem + 420 + q,
                            color=(240, 240, 240), jit=0, taper=(0, 0))
            if 0.02 < falso[k] < 0.98:
                self._romper(h, (cx0, cy0, tw, th), falso[k], t, k)
        luz_rect(h, rect(x, y, w, hh), 1.25 * enc, suave_=5.0)

    def _romper(self, h, celda, f, t, k):
        """Bandas horizontales del recuadro que se desplazan y parpadean (la señal se cae)."""
        P = h.tf(rect(*celda))
        x0, y0 = int(max(0, P[:, 0].min())), int(max(0, P[:, 1].min()))
        x1, y1 = int(min(W, P[:, 0].max())), int(min(H, P[:, 1].max()))
        if x1 - x0 < 8 or y1 - y0 < 8:
            return
        sub = h.img[y0:y1, x0:x1]
        rng = np.random.default_rng(int(t * 14) * 31 + k)
        amp = math.sin(math.pi * f) * (x1 - x0) * 0.35
        nb = 9
        ys = np.linspace(0, y1 - y0, nb + 1).astype(int)
        for b in range(nb):
            if rng.uniform() < 0.75:
                sub[ys[b]:ys[b + 1]] = np.roll(sub[ys[b]:ys[b + 1]], int(rng.uniform(-amp, amp)), axis=1)
            if rng.uniform() < 0.25 * math.sin(math.pi * f):
                sub[ys[b]:ys[b + 1]] = 1.0 - sub[ys[b]:ys[b + 1]] * 0.7


def espalda(h, x, y, s=1.0, sem=0, luz=(0.2, -1.0), gira=0.0, hombros=0.0):
    """Empleado visto de espaldas, sentado: respaldo de la silla, hombros de camisa, cuello, nuca con pelo corto y orejas.
    (x, y) = base del cuello. gira: -1..1 vuelve un poco la cabeza (se le ve la mejilla). hombros: 0..1 los sube (tensión)."""
    def T(P):
        P = np.asarray(P, float).reshape(-1, 2)
        return np.stack([x + s * P[:, 0], y + s * P[:, 1]], 1)
    sub = -14 * hombros
    h.pieza(T(suave([(-250, 120), (-236, -10), (-150, -40), (150, -40), (236, -10), (250, 120), (260, 700), (-260, 700)], 5)), 30,
            sem, w=8 * s, luz=luz, d=20 * s, trama=0.6, rim=0.5)                                      # respaldo
    h.pieza(T(suave([(-300, 110 + sub), (-210, 30 + sub), (-70, 4 + sub), (70, 4 + sub), (210, 30 + sub), (300, 110 + sub),
                     (330, 700), (-330, 700)], 5)), 150, sem + 1, w=8 * s, luz=luz, d=26 * s, trama=0.7, rim=0.9)          # camisa
    for sx in (-1, 1):                                                                                # pliegues de la tela
        h.trazo(T([(sx * 150, 60 + sub), (sx * 120, 260), (sx * 140, 520)]), 4 * s, sem + 3 + sx, alfa=0.5)
    h.trazo(T([(0, 30 + sub), (0, 600)]), 3 * s, sem + 5, alfa=0.35)
    h.pieza(T(suave([(-58, 20 + sub), (-40, -6 + sub), (40, -6 + sub), (58, 20 + sub), (36, 40 + sub), (-36, 40 + sub)], 4)), 200,
            sem + 6, w=5 * s, luz=luz, d=8 * s, trama=0.2, rim=0.5)                                   # cuello de la camisa
    h.pieza(T([(-40, -70), (40, -70), (44, 6 + sub), (-44, 6 + sub)]), 112, sem + 7, w=6 * s, luz=luz, d=14 * s, trama=0.6, rim=0.7)
    g = gira * 22
    cab = suave([(-96 + g, -250), (-82 + g, -330), (-30 + g, -372), (34 + g, -372), (86 + g, -330), (98 + g, -250), (90 + g, -150),
                 (56 + g, -80), (-54 + g, -80), (-88 + g, -150)], 5)
    for sx in (-1, 1):                                                                                # orejas
        h.pieza(T(suave([(sx * 92 + g, -240), (sx * 116 + g, -252), (sx * 120 + g, -200), (sx * 96 + g, -176)], 3)), 126, sem + 8 + sx,
                w=5 * s, luz=luz, d=6 * s, trama=0.3, rim=0.8)
    h.pieza(T(cab), 122, sem + 10, w=8 * s, luz=luz, d=22 * s, trama=0.6, rim=0.9)
    pelo = suave([(-98 + g, -236), (-86 + g, -332), (-30 + g, -380), (36 + g, -380), (90 + g, -332), (100 + g, -236), (84 + g, -150),
                  (40 + g, -118), (-38 + g, -118), (-82 + g, -150)], 5)
    h.pieza(T(pelo), 30, sem + 11, w=7 * s, luz=luz, d=18 * s, trama=0.5, rim=0.85)
    for q in range(7):                                                                                # mechones de la nuca
        xa = -60 + q * 20 + g
        h.trazo(T([(xa, -128), (xa + 4 * math.sin(q), -100)]), 4 * s, sem + 20 + q, alfa=0.8)
    if abs(gira) > 0.3:                                                                               # mejilla que asoma
        sx = 1 if gira > 0 else -1
        h.pieza(T(suave([(sx * 84 + g, -230), (sx * 112 + g, -210), (sx * 104 + g, -130), (sx * 70 + g, -110)], 3)), 130, sem + 30,
                w=5 * s, luz=luz, d=8 * s, trama=0.3, rim=0.8)


def banda(h, s, cx, cy, px, t, t0, claro=False, sem=0, fuente=None, mundo=False):
    """Rótulo de énfasis legible sobre cualquier fondo: banda sólida (negra con letra blanca, o blanca con letra negra) que
    entra con un golpe. (cx, cy) = centro en PANTALLA (fijo aunque la cámara empuje, y nunca se sale del cuadro);
    mundo=True lo pega al mundo (p. ej. sobre un monitor que la cámara recorre). Úsalo en vez de N.sello sobre fondos irregulares."""
    import noir as N
    if t < t0:
        return
    u = clamp01((t - t0) / 0.14)
    k = 1.0 + 0.25 * (1 - u) ** 2
    im, _ = N._txt_img(s, px, fuente or N.FUENTE_SELLO, 3.0)
    an, al = (im.shape[1] + px * 0.9) * k, (px * 1.5) * k

    def pintar(cx, cy):
        h.pieza(rect(cx - an / 2, cy - al / 2, an, al), 236 if claro else 8, sem + 770, w=5, luz=(0, -1), d=4, sombra=0, trama=0, jit=0.6)
        h.luz_fija(rect(cx - an / 2 - 4, cy - al / 2 - 4, an + 8, al + 8), 0.95)  # luz fija: ni se quema bajo un foco ni se pierde a oscuras
        N.texto_maquina(h, s, cx, cy, px * k, t, -99, cps=1e9, tono=0.04 if claro else 0.96, centro=True,
                        fuente=fuente or N.FUENTE_SELLO, track=3.0, encuadrar=False)
    if mundo:
        pintar(cx, cy)
    else:
        with h.capa(0.0):
            pintar(min(max(cx, an / 2 + 36), W - an / 2 - 36), min(max(cy, al / 2 + 36), H - al / 2 - 36))


def fijo(h):
    """`with C.fijo(h):` dibuja en coordenadas de PANTALLA (textos y cabeceras que no deben moverse con el empuje de cámara)."""
    return h.capa(0.0)


def teclado(h, x, y, w=560, sem=0):
    """Teclado en perspectiva sobre el escritorio (x, y = esquina superior izquierda)."""
    P = np.array([[x + 40, y], [x + w - 40, y], [x + w, y + 110], [x, y + 110]], float)
    h.pieza(P, 40, sem, w=5, luz=(0, -1), d=8, trama=0.3, rim=0.5)
    for j in range(4):
        v = (j + 0.5) / 4
        xa, xb = x + 40 * (1 - v) + 14, x + w - 40 * (1 - v) - 14
        n = 13
        for i in range(n):
            a = xa + (xb - xa) * i / n
            b = xa + (xb - xa) * (i + 0.78) / n
            yy = y + 10 + 96 * v - 9
            h.pieza(np.array([[a, yy], [b, yy], [b, yy + 15], [a, yy + 15]]), 88, sem + 10 + j * 13 + i, w=1.5, luz=(0, -1), d=2, trama=0,
                    sombra=0.3, jit=0.3)
