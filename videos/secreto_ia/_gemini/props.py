# -*- coding: utf-8 -*-
"""Utilería noir dibujada cuadro a cuadro (tinta que hierve, claroscuro de Noir.pieza). Todo en coordenadas del MUNDO.

lampara_colgante · mesa · silla · caja_negra (el «sospechoso») · revolver · tambor (cilindro de 10 recámaras) · periodico ·
mano · sobre · foto · placa (cartel de rueda de reconocimiento)."""
import math

import numpy as np

import noir as N
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from toon import blob, elipse_, suave, tubo, eje_curvo


def rect(x, y, w, h):
    return np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], float)


def rot(P, ang, c):
    P = np.asarray(P, float)
    cs, sn = math.cos(ang), math.sin(ang)
    Q = P - c
    return np.stack([c[0] + Q[:, 0] * cs - Q[:, 1] * sn, c[1] + Q[:, 0] * sn + Q[:, 1] * cs], 1)


# ---------------------------------------------------------------------- luz y mobiliario
def lampara_colgante(h, x, y_techo, largo=420, ang=0.0, k=1.0, s=1.0, cono=True, abre=0.55, alcance=1300, sem=0):
    """Lámpara de pantalla metálica colgada de un cable; ang = balanceo (rad). Emite y proyecta un cono hacia abajo."""
    bx = x + math.sin(ang) * largo
    by = y_techo + math.cos(ang) * largo
    h.trazo(np.array([[x, y_techo], [bx, by]]), 3 * s, sem, color=gris(20), jit=0.3)
    pant = np.array([[-18, 0], [18, 0], [80, 70], [-80, 70]], float) * s
    pant = rot(pant + (bx, by), -ang, np.array([bx, by]))
    h.pieza(pant, 38, sem + 1, w=5 * s, luz=(0, -1), d=8 * s, trama=0.3, rim=0.9)
    bulbo = rot(np.array(elipse_(bx, by + 72 * s, 26 * s, 12 * s, n=16)), -ang, np.array([bx, by]))
    if k > 0:
        h.emitir(bulbo, 1.2 * k)
        ca = math.pi / 2 - ang
        if cono:
            h.luz_cono(bx, by + 60 * s, ca, abre, alcance * s, (1.6, 1.6, 1.6), k=k, suave=0.45)
        h.luz_radial(bx, by + 70 * s, 220 * s, (1.0, 1.0, 1.0), k=0.8 * k)
    return np.array([bx, by + 72 * s])


def mesa(h, x, y, ancho=760, fondo=120, alto=260, tono=60, sem=0):
    """Mesa de madera en ligera perspectiva: tablero (y = borde delantero), canto y patas."""
    top = np.array([[x - ancho / 2 + 40, y - fondo], [x + ancho / 2 - 40, y - fondo], [x + ancho / 2, y], [x - ancho / 2, y]])
    for lx in (-ancho / 2 + 30, ancho / 2 - 50):
        h.pieza(rect(x + lx, y + 10, 22, alto), tono - 25, sem + 2 + int(lx > 0), w=5, luz=(0, -1), d=8, trama=0.4)
    h.pieza(rect(x - ancho / 2, y, ancho, 26), tono - 20, sem + 1, w=5, luz=(0, -1), d=6, trama=0.3)
    h.pieza(top, tono + 25, sem, w=6, luz=(0, -1), d=14, trama=0.2, rim=0.6)
    for k in range(5):                                   # vetas de la madera
        yy = y - fondo + (k + 0.5) * fondo / 5
        h.trazo(np.array([[x - ancho / 2 + 60, yy], [x - 40, yy + 2], [x + ancho / 2 - 60, yy - 1]]), 1.6, sem + 10 + k, alfa=0.35)


def silla(h, x, y, s=1.0, d=1, tono=50, sem=0):
    """Silla de madera vista de lado (respaldo alto)."""
    def T(P):
        P = np.asarray(P, float)
        return np.stack([x + d * s * P[:, 0], y + s * P[:, 1]], 1)
    for P, k in (([(-60, 0), (-48, 0), (-50, -200), (-62, -200)], 0), ([(48, 0), (60, 0), (58, -200), (46, -200)], 1),
                 ([(-66, -420), (-50, -420), (-46, -200), (-62, -200)], 2)):
        h.pieza(T(P), tono - 15, sem + k, w=4 * s, luz=(0, -1), d=6, trama=0.3)
    h.pieza(T([(-70, -214), (70, -214), (66, -194), (-66, -194)]), tono + 10, sem + 3, w=4 * s, luz=(0, -1), d=6)
    h.pieza(T([(-70, -420), (-40, -420), (-40, -300), (-70, -300)]), tono, sem + 4, w=4 * s, luz=(0, -1), d=6)


# ---------------------------------------------------------------------- el sospechoso
def caja_negra(h, x, y, s=1.0, led=1.0, t=0.0, abierta=0.0, sem=0, cable=True):
    """La IA: un monolito negro de servidor (rejillas de ventilación, una sola luz que late). y = base."""
    w_, a_ = 230 * s, 520 * s
    cuerpo = rect(x - w_ / 2, y - a_, w_, a_)
    h.pieza(cuerpo, 20, sem, w=6 * s, luz=(0.3, -1), d=20 * s, trama=0.5, rim=0.95, rim_tono=200)
    h.pieza(rect(x - w_ / 2 + 14 * s, y - a_ + 14 * s, w_ - 28 * s, 40 * s), 30, sem + 1, w=3 * s, luz=(0, -1), d=4, trama=0, rim=0.5)
    for k in range(9):                                   # rejillas
        yy = y - a_ + 90 * s + k * 34 * s
        h.trazo(np.array([[x - w_ / 2 + 30 * s, yy], [x + w_ / 2 - 30 * s, yy]]), 3 * s, sem + 2 + k, color=gris(70), alfa=0.8,
                jit=0.2)
    lx, ly = x + w_ / 2 - 36 * s, y - a_ + 34 * s
    v = led * (0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 2.4)))
    if v > 0.02:
        h.emitir(elipse_(lx, ly, 7 * s, 7 * s, n=12), 1.4 * v)
        h.luz_radial(lx, ly, 140 * s, (0.8, 0.8, 0.8), k=0.7 * v)
    if cable:
        h.trazo(np.array([[x - w_ / 2 + 20 * s, y - 10 * s], [x - w_ / 2 - 80 * s, y + 6 * s], [x - w_ / 2 - 300 * s, y + 4 * s]]),
                8 * s, sem + 20, color=gris(15), jit=0.6)
    if abierta > 0:                                      # tapa abierta: dentro, oscuridad sin fondo
        P = rect(x - w_ / 2 + 22 * s, y - a_ + 80 * s, w_ - 44 * s, a_ - 120 * s)
        h.pieza(P, 4, sem + 30, w=4 * s, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=abierta)
    return np.array([lx, ly])


# ---------------------------------------------------------------------- armas
def revolver(h, x, y, s=1.0, ang=0.0, d=1, sem=0, tono=34):
    """Revólver de perfil (cañón a la derecha si d = 1)."""
    def T(P):
        P = np.asarray(P, float) * (d, 1)
        return rot(P * s + (x, y), ang, np.array([x, y]))
    h.pieza(T([(-10, -30), (190, -30), (190, -6), (-10, -6)]), tono + 10, sem, w=4 * s, luz=(0.2, -1), d=6 * s, trama=0.2,
            rim=0.95, rim_tono=230)
    h.pieza(T([(186, -36), (196, -36), (196, -28), (186, -28)]), tono, sem + 1, w=2 * s, luz=(0, -1), d=2, trama=0)
    h.pieza(T(suave([(-36, -40), (40, -42), (52, -20), (40, 6), (-36, 8), (-44, -16)], 3)), tono + 18, sem + 2, w=4 * s, luz=(0.2, -1),
            d=8 * s, trama=0.3, rim=0.9, rim_tono=230)
    for k in range(3):
        h.trazo(T([(-20 + k * 22, -36), (-20 + k * 22, 2)]), 2.5 * s, sem + 3 + k, alfa=0.7)
    h.pieza(T(suave([(-40, -10), (-20, -6), (-14, 30), (-36, 110), (-80, 116), (-90, 94), (-60, 20)], 4)), tono - 6, sem + 6,
            w=4 * s, luz=(0.2, -1), d=10 * s, trama=0.5, rim=0.8)
    h.trazo(T([(-14, 10), (6, 40), (-6, 46), (-26, 20)]), 3.5 * s, sem + 7)              # guardamonte
    h.trazo(T([(-48, -40), (-70, -60), (-62, -42)]), 4 * s, sem + 8)                      # martillo


def tambor(h, cx, cy, r, ang=0.0, cargada=0, n=10, sem=0, brillo=1.0):
    """Cara del tambor de un revólver con n recámaras; `cargada` = índice de la única bala (su culote brilla)."""
    h.pieza(elipse_(cx, cy, r, r, n=64), 46, sem, w=7, luz=(0.3, -1), d=r * 0.08, trama=0.4, rim=0.95, rim_tono=230)
    h.pieza(elipse_(cx, cy, r * 0.16, r * 0.16, n=24), 26, sem + 1, w=4, luz=(0.3, -1), d=4, trama=0)
    for k in range(n):
        a = ang + 2 * math.pi * k / n
        px, py = cx + math.cos(a) * r * 0.66, cy + math.sin(a) * r * 0.66
        rr = r * 0.17
        if k == cargada:
            h.pieza(elipse_(px, py, rr, rr, n=24), 205, sem + 10 + k, w=4, luz=(0.3, -1), d=rr * 0.25, trama=0, rim=0.9)
            h.pieza(elipse_(px, py, rr * 0.35, rr * 0.35, n=16), 150, sem + 30 + k, w=3, luz=(0.3, -1), d=3, trama=0)
            h.emitir(elipse_(px - rr * 0.3, py - rr * 0.3, rr * 0.18, rr * 0.12, n=10), 0.6 * brillo)
        else:
            h.pieza(elipse_(px, py, rr, rr, n=24), 6, sem + 10 + k, w=4, luz=(0.3, -1), d=1, sombra=0, trama=0, rim=0)
        # estrías entre recámaras
        a2 = a + math.pi / n
        h.trazo(np.array([[cx + math.cos(a2) * r * 0.84, cy + math.sin(a2) * r * 0.84],
                          [cx + math.cos(a2) * r * 0.98, cy + math.sin(a2) * r * 0.98]]), 6, sem + 50 + k, alfa=0.8)


# ---------------------------------------------------------------------- papeles
def periodico(h, t, t0, titular, sub="", cx=W / 2, cy=H / 2, dur=0.9, s=1.0, sem=0, cabecera="EL DIARIO DE LA NOCHE",
              fijo=False):
    """El periódico que llega girando hacia la cámara (recurso clásico del cine negro) y se queda quieto con el titular.
    Coordenadas de pantalla (dibujar con la cámara en identidad)."""
    if t < t0:
        return
    u = clamp01((t - t0) / dur)
    e = e_out(u)
    ang = 0.0 if fijo else (1 - e) * 6.5 + 0.04 * math.sin(t * 0.7)
    esc = s * (0.05 + 0.95 * e)
    ww, hh = 1180, 760

    def T(P):
        P = np.asarray(P, float) * esc
        return rot(P + (cx, cy), ang, np.array([cx, cy]))
    h.pieza(T(rect(-ww / 2, -hh / 2, ww, hh)), 222, sem, w=4, luz=(0.2, -1), d=10, trama=0, rim=0)
    h.pieza(T(rect(-ww / 2 + 30, -hh / 2 + 26, ww - 60, 4)), 30, sem + 1, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
    N.texto_maquina(h, cabecera, cx - 0, cy - (hh / 2 - 70) * esc, 46 * esc, t, -99, cps=1e9, tono=0.06,
                    fuente="C:/Windows/Fonts/timesbd.ttf", centro=True, track=6 * esc) if esc > 0.3 else None
    if esc > 0.3:
        pxt = min(82.0, 1900.0 / max(1, len(titular)))
        N.texto_maquina(h, titular, cx, cy - (hh / 2 - 175) * esc, pxt * esc, t, -99, cps=1e9, tono=0.03,
                        fuente="C:/Windows/Fonts/impact.ttf", centro=True, track=2 * esc)
        if sub:
            N.texto_maquina(h, sub, cx, cy - (hh / 2 - 255) * esc, 30 * esc, t, -99, cps=1e9, tono=0.12, centro=True,
                            fuente="C:/Windows/Fonts/timesbi.ttf")
    # columnas y foto
    r = np.random.default_rng(sem)
    for col in range(3):
        x0 = -ww / 2 + 50 + col * (ww - 100) / 3
        if col == 1:
            h.pieza(T(rect(x0, -hh / 2 + 300, (ww - 160) / 3, 210)), 70, sem + 5, w=3, luz=(0, -1), d=1, sombra=0, trama=0.6, rim=0)
            ystart = -hh / 2 + 530
        else:
            ystart = -hh / 2 + 300
        for k in range(int((hh / 2 - 30 - ystart) / 22)):
            y = ystart + k * 22
            L = (ww - 160) / 3 * r.uniform(0.7, 1.0)
            h.pieza(T(rect(x0, y, L, 8)), 120, sem + 100 + col * 40 + k, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False,
                    alfa=0.7, jit=0)


def sobre(h, x, y, s=1.0, ang=0.0, abierto=0.0, sem=0, texto="CONFIDENCIAL", t=0.0):
    def T(P):
        return rot(np.asarray(P, float) * s + (x, y), ang, np.array([x, y]))
    h.pieza(T(rect(-200, -130, 400, 260)), 175, sem, w=5 * s, luz=(0.2, -1), d=10 * s, trama=0.2, rim=0.5)
    sol = [(-200, -130), (200, -130), (0, 20 - 160 * abierto)]
    h.pieza(T(sol), 150, sem + 1, w=4 * s, luz=(0.2, -1), d=6 * s, trama=0.2)
    if texto:
        N.sello(h, texto, x, y + 70 * s, 40 * s, t, -99, rot=-6 - math.degrees(ang), tono=0.05, alfa=0.9)


def foto(h, x, y, s=1.0, ang=0.0, sem=0, figura=True):
    """Foto de vigilancia con borde blanco y una silueta borrosa."""
    def T(P):
        return rot(np.asarray(P, float) * s + (x, y), ang, np.array([x, y]))
    h.pieza(T(rect(-110, -80, 220, 160)), 230, sem, w=3 * s, luz=(0.2, -1), d=5 * s, trama=0, rim=0)
    h.pieza(T(rect(-96, -68, 192, 120)), 80, sem + 1, w=2 * s, luz=(0, -1), d=1, sombra=0, trama=0.4, rim=0)
    if figura:
        h.pieza(T(suave([(-20, 52), (-28, -6), (-12, -22), (-14, -46), (6, -50), (10, -22), (26, -6), (20, 52)], 3)), 20, sem + 2,
                w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)


def placa(h, x, y, texto, t, t0, s=1.0, sem=0):
    """Cartel de número/nombre que sostiene un testigo (pizarrita negra con letras blancas de máquina)."""
    if t < t0:
        return
    h.pieza(rect(x - 150 * s, y - 40 * s, 300 * s, 80 * s), 22, sem, w=4 * s, luz=(0, -1), d=4, trama=0, rim=0.5)
    N.texto_maquina(h, texto, x, y - 22 * s, 26 * s, t, t0, cps=40, tono=0.92, centro=True)


def mano(h, x, y, s=1.0, ang=0.0, d=1, tono=118, sem=0, dedos=0.0, manga=70):
    """Mano con puño de gabardina: dedos=0 cerrada (sujeta algo) .. 1 abierta y estirada."""
    def T(P):
        P = np.asarray(P, float) * (d, 1)
        return rot(P * s + (x, y), ang, np.array([x, y]))
    h.pieza(T(tubo(np.array([[-420, 30], [-200, 16], [-40, 0]]), 120, 96)), manga, sem, w=7 * s, luz=(0.3, -1), d=24 * s, trama=0.5,
            rim=0.8)
    h.pieza(T(suave([(-50, -44), (20, -50), (70, -30), (80, 20), (30, 52), (-46, 44)], 4)), tono, sem + 1, w=6 * s, luz=(0.3, -1),
            d=18 * s, trama=0.35, rim=0.8)
    for k in range(4):
        L = 40 + 60 * dedos
        y0 = -32 + k * 20
        h.pieza(T(tubo(np.array([[60, y0], [60 + L * 0.6, y0 + 4 - 6 * (1 - dedos)], [60 + L, y0 + 12 * (1 - dedos)]]), 22, 18)),
                tono + 4, sem + 2 + k, w=5 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.7)
    h.pieza(T(tubo(np.array([[0, -40], [40, -64], [76, -70]]), 26, 20)), tono + 6, sem + 9, w=5 * s, luz=(0.3, -1), d=6 * s,
            trama=0.2, rim=0.7)
