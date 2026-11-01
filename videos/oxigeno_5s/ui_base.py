# -*- coding: utf-8 -*-
"""Piezas de interfaz del video: texto con subíndices químicos («O2» -> O₂ dibujado, Poppins no trae ₂), píldoras,
visto (check) y cruz vectoriales, entrada con rebote y salida desvaneciéndose (nunca encogiendo a ilegible)."""
import math
import re

import numpy as np

import plano as P
from motor import W, H, prog, clamp01, e_in, e_out, circulo, rect_red, ancho_texto
from kz_ui import pop as kpop

AZUL_OSC = (34, 28, 80)
ROJO_O = (236, 72, 84)
TEAL = (30, 170, 170)
NARANJA = (240, 130, 36)
MORADO = (122, 52, 200)
VERDE = (60, 168, 96)
_RX = re.compile(r"([A-Za-zÁÉÍÓÚáéíóú)])(\d+)")


def _runs(texto):
    """[(trozo, es_subindice)] — los dígitos pegados a una letra mayúscula de fórmula (O2, H2O, CO2, N2) van abajo."""
    out = []
    i = 0
    for m in re.finditer(r"\b(?:[A-Z][a-z]?\d*)+\b", texto):
        tok = m.group(0)
        if not re.search(r"[A-Z][a-z]?\d", tok) or tok.isdigit():
            continue
        if m.start() > i:
            out.append((texto[i:m.start()], False))
        for el, num in re.findall(r"([A-Z][a-z]?)(\d*)", tok):
            out.append((el, False))
            if num:
                out.append((num, True))
        i = m.end()
    if i < len(texto):
        out.append((texto[i:], False))
    return out


def ancho_q(texto, px, fuente="geo"):
    return sum(ancho_texto(s, fuente, px * (0.62 if sub else 1.0)) for s, sub in _runs(texto))


def texto_q(lz, x, y, texto, px, color=(255, 255, 255), fuente="geo", alfa=1.0, capa=2, sombra=0.0, ancla_x=0.5):
    if alfa <= 0.01:
        return
    w = ancho_q(texto, px, fuente)
    cx = x - w * ancla_x
    for s, sub in _runs(texto):
        p = px * (0.62 if sub else 1.0)
        ws = ancho_texto(s, fuente, p)
        yy = y + (px * 0.26 if sub else 0.0)
        if sombra > 0:
            lz.texto(s, cx + ws / 2 + 3, yy + 4, p, fuente, color=(12, 10, 40), borde=None, alfa=alfa * sombra, capa=capa,
                     temblor=0.0)
        lz.texto(s, cx + ws / 2, yy, p, fuente, color=color, borde=None, alfa=alfa, capa=capa, temblor=0.0)
        cx += ws


def pildora(lz, x, y, texto, px=34, k=1.0, fondo=(255, 255, 255), color=AZUL_OSC, alfa=1.0, capa=2, fuente="geo", sombra=True,
            icono=None):
    """Cápsula con texto (admite subíndices). icono: 'check' | 'cruz' | None (a la izquierda)."""
    if k <= 0.01 or alfa <= 0.01:
        return
    w = ancho_q(texto, px, fuente) + px * 1.1 + (px * 1.1 if icono else 0)
    h = px * 1.6
    with lz.capa(capa):
        with lz.grupo(x, y, k):
            if sombra:
                lz.relleno(rect_red(-w / 2 + 3, -h / 2 + 5, w, h, h / 2), (10, 6, 40), alfa=0.22 * alfa)
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, h / 2), fondo, alfa=alfa)
            dx = 0.0
            if icono:
                ix = -w / 2 + px * 0.95
                (check if icono == "check" else cruz)(lz, ix, 0, px * 0.42, color, alfa)
                dx = px * 0.55
            texto_q(lz, dx, px * 0.02, texto, px, color, fuente, alfa, capa)


def check(lz, x, y, r, color=(255, 255, 255), alfa=1.0, ancho=None):
    lz.trazo(np.array([[x - r, y], [x - r * 0.25, y + r * 0.7], [x + r, y - r * 0.75]]), tuple(color[:3]) + (int(255 * alfa),),
             ancho or r * 0.45, afinar=False)


def cruz(lz, x, y, r, color=(255, 255, 255), alfa=1.0, ancho=None):
    c = tuple(color[:3]) + (int(255 * alfa),)
    lz.trazo(np.array([[x - r, y - r], [x + r, y + r]]), c, ancho or r * 0.45, afinar=False)
    lz.trazo(np.array([[x - r, y + r], [x + r, y - r]]), c, ancho or r * 0.45, afinar=False)


def prohibido(lz, x, y, r, alfa=1.0, color=(236, 60, 70)):
    lz.trazo(P.arco_pts(x, y, r, 0, 2 * math.pi, 60), color + (int(255 * alfa),), r * 0.16, afinar=False)
    a = math.radians(-45)
    lz.trazo(np.array([[x - r * math.cos(a) * 0.92, y - r * math.sin(a) * 0.92], [x + r * math.cos(a) * 0.92, y + r * math.sin(a) * 0.92]]),
             color + (int(255 * alfa),), r * 0.16, afinar=False)


def flecha(lz, p0, p1, col=(255, 255, 255), ancho=8.0, punta=24.0, alfa=1.0, frac=1.0):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    if frac <= 0.01 or alfa <= 0.01:
        return
    p1 = p0 + (p1 - p0) * clamp01(frac)
    d = p1 - p0
    L = float(np.hypot(*d)) + 1e-6
    u = d / L
    n = np.array([-u[1], u[0]])
    base = p1 - u * min(punta, L * 0.6)
    lz.trazo(np.array([p0, base + u * 2]), tuple(col[:3]) + (int(255 * alfa),), ancho, afinar=False)
    lz.relleno(np.array([p1, base + n * punta * 0.6, base - n * punta * 0.6]), col, alfa=alfa)


def ent(t, t0, t1=None, fo=0.35, lento=1.0):
    """(escala, alfa): entra con rebote en t0 y, si hay t1, se desvanece después (sin encogerse)."""
    k = kpop(t, t0, lento)
    a = 1.0 if t1 is None else 1 - e_in(prog(t, t1, t1 + fo))
    a *= min(1.0, k * 3)
    return k, a


def oscurecer_fondo(lz, a, color=(16, 12, 44)):
    if a > 0.01:
        lz.relleno(np.array([[-10, -10], [W + 10, -10], [W + 10, H + 10], [-10, H + 10]], float), color, alfa=a, capa=2)
