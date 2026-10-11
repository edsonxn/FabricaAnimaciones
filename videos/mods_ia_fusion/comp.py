# -*- coding: utf-8 -*-
"""Componentes del estilo «rayos X tecno»: ventanas de proceso (con video real o mundo dibujado), mundo de bloques original,
bloque de memoria compartida, paquetes de datos, chips, rótulos de golpe, iconos."""
import math

import numpy as np

from pix import *  # noqa: F401,F403
from pix import Clip, P, pop, pr, rnd, smooth, e_out, e_back, lerp, mix, clamp, golpe, ancho_texto


# ------------------------------------------------------------------ rótulos
def slam(p, txt, x, y, px, color, t, t0, fnt="black", sale=None, esp=0.0, sombra=0.75, anchor="mm"):
    """Rótulo de golpe: entra grande, rebota y se asienta; con `sale` se va encogiéndose."""
    if t < t0:
        return
    k = pop(t, t0, 0.30)
    s = lerp(1.9, 1.0, min(1.0, k)) if k < 1 else k
    op = pr(t, t0, t0 + 0.08)
    if sale is not None:
        u = pr(t, sale, sale + 0.22)
        if u >= 1:
            return
        s *= 1 - 0.3 * u
        op *= 1 - u
    with p.pivote(x, y, s):
        p.texto(txt, x, y, px, color, fnt, op, anchor, esp, sombra)


def chip(p, txt, x, y, px, color, t, t0, sale=None, relleno=None, fnt="xbold", icono=None):
    """Etiqueta de cápsula con borde de color; entra con rebote. Devuelve su ancho."""
    w = ancho_texto(txt, px, fnt) + px * (1.3 + (1.1 if icono else 0))
    k = pop(t, t0, 0.32)
    if sale is not None:
        k *= 1 - pr(t, sale, sale + 0.2)
    if k <= 0.01:
        return w
    h = px * 1.75
    with p.pivote(x, y, k):
        p.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, relleno or mix(PANEL, color, 0.16), 0.96, borde=color, w=4)
        tx = x + (px * 0.55 if icono else 0)
        if icono:
            icono(p, x - w / 2 + px * 1.0, y, px * 0.55, color, t)
        p.texto(txt, tx, y + px * 0.02, px, BLANCO, fnt)
    return w


def tecleo(p, txt, x, y, px, color, t, t0, cps=38, fnt="mono", anchor="lm", op=1.0, cursor=True):
    n = int(clamp((t - t0) * cps, 0, len(txt)))
    if t < t0:
        return
    s = txt[:n]
    p.texto(s, x, y, px, color, fnt, op, anchor)
    if cursor and (n < len(txt) or int(t * 3) % 2 == 0) and anchor[0] == "l":
        cx = x + ancho_texto(s, px, fnt) + px * 0.12
        p.rect(cx, y - px * 0.5, cx + px * 0.5, y + px * 0.45, color, 0.9 * op)


# ------------------------------------------------------------------ iconos (centro x,y; tamaño r)
def ic_cubo(p, x, y, r, color, t=0.0):
    a = r * 0.95
    top = [(x, y - a), (x + a, y - a / 2), (x, y), (x - a, y - a / 2)]
    p.poly(top, mix(color, BLANCO, 0.35))
    p.poly([(x - a, y - a / 2), (x, y), (x, y + a), (x - a, y + a / 2)], mix(color, NEGRO, 0.25))
    p.poly([(x + a, y - a / 2), (x, y), (x, y + a), (x + a, y + a / 2)], mix(color, NEGRO, 0.5))


def ic_alas(p, x, y, r, color, t=0.0):
    f = 0.25 * math.sin(t * 9)
    for s in (-1, 1):
        p.poly([(x, y + r * 0.2), (x + s * r * 1.25, y - r * (0.75 + f)), (x + s * r * 0.95, y + r * 0.15), (x + s * r * 0.6, y + r * 0.1),
                (x + s * r * 0.45, y + r * 0.55)], color)
    p.circ(x, y, r * 0.24, BLANCO)


def ic_dinamita(p, x, y, r, color, t=0.0):
    for k in (-1, 0, 1):
        p.rrect(x + k * r * 0.52 - r * 0.22, y - r * 0.75, x + k * r * 0.52 + r * 0.22, y + r * 0.8, r * 0.1, ROJO)
    p.rect(x - r * 0.85, y - r * 0.15, x + r * 0.85, y + r * 0.2, mix(AMAR, NEGRO, 0.1))
    p.polilinea([(x, y - r * 0.75), (x + r * 0.2, y - r * 1.1), (x + r * 0.55, y - r * 1.15)], r * 0.11, BLANCO)
    ch = 0.6 + 0.4 * math.sin(t * 30)
    p.glow(x + r * 0.55, y - r * 1.15, r * 0.7, AMAR, 1.2 * ch)


def ic_ventana_no(p, x, y, r, color, t=0.0):
    p.rrect(x - r, y - r * 0.72, x + r, y + r * 0.72, r * 0.16, None, borde=color, w=r * 0.14)
    p.linea((x - r, y - r * 0.38), (x + r, y - r * 0.38), r * 0.12, color)
    p.linea((x - r * 1.15, y + r * 1.0), (x + r * 1.15, y - r * 1.0), r * 0.2, ROJO)


def ic_sonido_no(p, x, y, r, color, t=0.0):
    p.poly([(x - r, y - r * 0.3), (x - r * 0.5, y - r * 0.3), (x + r * 0.05, y - r * 0.8), (x + r * 0.05, y + r * 0.8), (x - r * 0.5, y + r * 0.3),
            (x - r, y + r * 0.3)], color)
    p.elip(x + r * 0.15, y, r * 0.55, r * 0.55, color, a0=-50, a1=50, w=r * 0.13)
    p.linea((x - r * 1.15, y + r * 1.0), (x + r * 1.15, y - r * 1.0), r * 0.2, ROJO)


def ic_candado(p, x, y, r, color, t=0.0):
    p.elip(x, y - r * 0.35, r * 0.5, r * 0.6, color, a0=180, a1=360, w=r * 0.2)
    p.rrect(x - r * 0.8, y - r * 0.35, x + r * 0.8, y + r * 0.85, r * 0.15, color)
    p.circ(x, y + r * 0.15, r * 0.17, NEGRO)
    p.rect(x - r * 0.07, y + r * 0.15, x + r * 0.07, y + r * 0.55, NEGRO)


def ic_ojo(p, x, y, r, color, t=0.0, mira=(0.0, 0.0)):
    pts = [(x + r * math.cos(a), y + r * 0.55 * math.sin(a) * (1 if math.sin(a) > 0 else 1)) for a in np.linspace(0, 2 * math.pi, 22)]
    parp = 1.0 if (t * 0.37) % 1 > 0.06 else 0.15
    pts = [(px_, y + (py_ - y) * parp) for px_, py_ in pts]
    p.poly(pts, BLANCO)
    p.circ(x + mira[0] * r * 0.4, y + mira[1] * r * 0.2, r * 0.36 * parp, color)
    p.circ(x + mira[0] * r * 0.4, y + mira[1] * r * 0.2, r * 0.16 * parp, NEGRO)


# ------------------------------------------------------------------ mundo de bloques (original, isométrico)
PASTO, TIERRA, PIEDRA, AGUA, ARENA, TRONCO, HOJA = (0.36, 0.78, 0.30), (0.50, 0.33, 0.20), (0.52, 0.55, 0.60), (0.20, 0.52, 0.95), \
    (0.90, 0.80, 0.52), (0.42, 0.27, 0.15), (0.20, 0.62, 0.26)


def cubo(p, x, y, a, tope, lado=None, op=1.0, alto=1.0):
    """Cubo isométrico con su cara superior centrada en (x, y); `a` = medio ancho."""
    lado = lado or tope
    h = a * alto
    p.poly([(x - a, y), (x, y + a / 2), (x, y + a / 2 + h), (x - a, y + h)], mix(lado, NEGRO, 0.28), op)
    p.poly([(x + a, y), (x, y + a / 2), (x, y + a / 2 + h), (x + a, y + h)], mix(lado, NEGRO, 0.52), op)
    p.poly([(x, y - a / 2), (x + a, y), (x, y + a / 2), (x - a, y)], tope, op)
    p.polilinea([(x - a, y), (x, y + a / 2), (x + a, y)], max(1.0, a * 0.05), mix(tope, BLANCO, 0.4), 0.5 * op)


def _alt(i, j):
    return int(round(1.3 + 1.2 * math.sin(i * 0.9 + 0.5) * math.cos(j * 0.7) + 0.8 * math.sin((i + j) * 0.45)))


def figura_bloques(p, x, y, a, t, color=NARANJA, mira=1):
    """Explorador de bloques ORIGINAL (robot-cubo naranja con visor): de pie sobre (x, y), salta al andar y mueve los brazos."""
    salto = abs(math.sin(t * 5.2)) * a * 0.55
    y -= salto
    bra = math.sin(t * 5.2) * a * 0.35
    p.elip(x, y + salto + a * 0.1, a * 0.7, a * 0.25, NEGRO, 0.35)
    for s in (-1, 1):                                                   # piernas
        p.rect(x + s * a * 0.3 - a * 0.2, y - a * 0.9, x + s * a * 0.3 + a * 0.2, y + s * bra * 0.25, mix(color, NEGRO, 0.55))
    p.rect(x - a * 0.55, y - a * 2.0, x + a * 0.55, y - a * 0.8, color)   # torso
    p.rect(x - a * 0.55, y - a * 1.25, x + a * 0.55, y - a * 1.05, mix(color, NEGRO, 0.4))
    for s in (-1, 1):                                                   # brazos con mano
        bx = x + s * a * 0.78
        p.rect(bx - a * 0.2, y - a * 1.95, bx + a * 0.2, y - a * 1.05 + s * bra, mix(color, NEGRO, 0.2))
        p.rect(bx - a * 0.2, y - a * 1.05 + s * bra, bx + a * 0.2, y - a * 0.8 + s * bra, (0.95, 0.85, 0.7))
    p.rect(x - a * 0.7, y - a * 3.25, x + a * 0.7, y - a * 2.05, mix(color, BLANCO, 0.25))    # cabeza
    p.rect(x - a * 0.55, y - a * 2.95, x + a * 0.55, y - a * 2.45, (0.06, 0.08, 0.14))          # visor
    par = 1.0 if (t * 0.45) % 1 > 0.07 else 0.15
    for s in (-1, 1):
        ex = x + s * a * 0.25 + mira * a * 0.08
        p.rect(ex - a * 0.1, y - a * 2.7 - a * 0.13 * par, ex + a * 0.1, y - a * 2.7 + a * 0.13 * par, CIAN)
    p.rect(x - a * 0.18, y - a * 2.28, x + a * 0.18, y - a * 2.2, (0.06, 0.08, 0.14))            # boca
    p.rect(x - a * 0.06, y - a * 3.6, x + a * 0.06, y - a * 3.25, GRIS)                          # antena
    p.glow(x, y - a * 3.62, a * 0.5, ROJO, 0.9 * (0.5 + 0.5 * math.sin(t * 6)))


def mundo_bloques(p, x0, y0, x1, y1, t, op=1.0):
    """Diorama isométrico original: islas de cubos con pasto, agua que brilla, árbol, nubes cúbicas, bloques que aparecen
    y el explorador saltando. Todo recortado al rectángulo."""
    with p.clip(x0, y0, x1, y1):
        p.rect(x0, y0, x1, y1, None, op, grad=((0.30, 0.62, 0.98), (0.72, 0.90, 1.00)))
        p.circ(x0 + (x1 - x0) * 0.82, y0 + (y1 - y0) * 0.22, 46, (1.0, 0.97, 0.75), op)
        p.glow(x0 + (x1 - x0) * 0.82, y0 + (y1 - y0) * 0.22, 190, (1.0, 0.95, 0.6), 0.45 * op)
        for k in range(4):                                              # nubes de cubos, dos planos
            cx = x0 + ((rnd(k, 1) * 1.4 - 0.2) * (x1 - x0) + t * (14 + 9 * k)) % ((x1 - x0) * 1.3) - 80
            cy = y0 + 40 + 44 * k
            for q in range(3):
                cubo(p, cx + q * 34, cy + (q % 2) * 6, 22, (1, 1, 1), (0.82, 0.88, 0.97), 0.92 * op, 0.5)
        for k in range(7):                                              # sierra lejana de cubos
            hx = x0 + (k + 0.5) * (x1 - x0) / 7
            hh = 40 + 60 * rnd(k, 9)
            p.rect(hx - 70, y0 + (y1 - y0) * 0.50 - hh, hx + 70, y1, (0.42, 0.70, 0.78), 0.75 * op)
        a = (x1 - x0) / 15.0
        cx, cy = (x0 + x1) / 2, y0 + (y1 - y0) * 0.50
        N = 7
        pj = (3.0 + 1.6 * math.sin(t * 0.7), 3.0 + 1.6 * math.cos(t * 0.55))
        nuevo = int(t * 1.6)                                            # un bloque nuevo cada ~0,6 s
        for s in range(2 * N - 1):
            for i in range(max(0, s - N + 1), min(N, s + 1)):
                j = s - i
                hh = _alt(i, j)
                sx, sy = cx + (i - j) * a, cy + (i + j) * a / 2
                if hh <= 0:
                    br = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7 + j)
                    cubo(p, sx, sy + a * 0.35, a, mix(AGUA, BLANCO, 0.18 * br), AGUA, op, 0.6)
                    continue
                for z in range(hh):
                    cubo(p, sx, sy - z * a, a, PASTO if z == hh - 1 else TIERRA, TIERRA if z < hh - 1 or True else PASTO, op)
                tope = sy - (hh - 1) * a
                if (i, j) == (1, 5):                                    # árbol
                    for z in range(1, 3):
                        cubo(p, sx, tope - z * a, a * 0.5, TRONCO, TRONCO, op)
                    for dx, dy, dz in ((0, 0, 3), (-0.6, 0.2, 3), (0.6, 0.2, 3), (0, -0.2, 4)):
                        cubo(p, sx + dx * a, tope - dz * a + dy * a + 2 * math.sin(t * 2 + dx), a * 0.78, HOJA, mix(HOJA, NEGRO, 0.2), op)
                if (i, j) == (5, 1):                                    # bloque de piedra que se coloca una y otra vez
                    k = pop(t, nuevo / 1.6, 0.25) if nuevo % 3 else 1.0
                    for z in range(1, 1 + (nuevo % 3) + 1):
                        cubo(p, sx, tope - z * a - (1 - min(1, k)) * 40 * (z == (nuevo % 3) + 1), a, PIEDRA, mix(PIEDRA, NEGRO, 0.1),
                             op * (min(1, k) if z == (nuevo % 3) + 1 else 1))
                if abs(i - pj[0]) < 0.5 and abs(j - pj[1]) < 0.5:
                    figura_bloques(p, cx + (pj[0] - pj[1]) * a, cy + (pj[0] + pj[1]) * a / 2 - (hh - 1) * a, a * 0.6, t,
                                   mira=1 if math.cos(t * 0.7) > 0 else -1)
        for k in range(10):                                             # motas/chispas en primer plano
            mx = x0 + (rnd(k, 4) * (x1 - x0) + t * 30) % (x1 - x0)
            my = y0 + (rnd(k, 5) * (y1 - y0) - t * 22) % (y1 - y0)
            p.rect(mx, my, mx + 7, my + 7, (1, 1, 1), 0.5 * op)


# ------------------------------------------------------------------ ventana de proceso
def ventana(p, x0, y0, x1, y1, titulo, sub, color, t, op=1.0, fantasma=0.0, vivo=1.0):
    """Marco de ventana de programa (barra de título con luces, nombre y proceso). Devuelve el rectángulo interior.
    `fantasma` 0..1 = proceso oculto: el marco se vuelve punteado y tenue."""
    bar = 62
    col = mix(color, GRIS2, 0.75 * fantasma)
    p.rrect(x0 - 10, y0 - 10, x1 + 10, y1 + 10, 30, NEGRO, 0.45 * op)
    p.rrect(x0, y0, x1, y1, 22, PANEL, 0.97 * op)
    if fantasma < 0.5:
        p.rrect(x0, y0, x1, y1, 22, None, op, borde=col, w=5)
    else:
        per = 2 * (x1 - x0 + y1 - y0)
        n = int(per / 34)
        pts = P._pts_rr(x0, y0, x1, y1, 22)
        lon = np.cumsum([0] + [math.dist(pts[k], pts[(k + 1) % len(pts)]) for k in range(len(pts))])
        for k in range(n):                                              # borde punteado que circula
            d = ((k + t * 1.5) % n) / n * lon[-1]
            q = int(np.searchsorted(lon, d) - 1) % len(pts)
            a, b = pts[q], pts[(q + 1) % len(pts)]
            u = (d - lon[q]) / max(lon[q + 1] - lon[q], 1e-3)
            p.circ(lerp(a[0], b[0], u), lerp(a[1], b[1], u), 4, col, op)
    p.rect(x0 + 5, y0 + bar, x1 - 5, y0 + bar + 3, col, 0.6 * op)
    for k, c in enumerate((ROJO, AMAR, VERDE)):
        p.circ(x0 + 34 + k * 30, y0 + bar / 2 + 2, 9, mix(c, GRIS2, fantasma), op)
    p.texto(titulo, x0 + 132, y0 + bar / 2 + 3, 34, mix(BLANCO, GRIS, fantasma), "mono", op, "lm")
    p.texto(sub, x1 - 26, y0 + bar / 2 + 3, 26, col, "mono", op, "rm")
    if vivo > 0 and fantasma < 0.9:                                     # indicador de que corre: barras que laten
        for k in range(4):
            hb = 6 + 16 * abs(math.sin(t * (5 + k) + k))
            p.rect(x1 - 26 - ancho_texto(sub, 26, "mono") - 56 + k * 10, y0 + bar / 2 + 14 - hb, x1 - 26 - ancho_texto(sub, 26, "mono") - 50 + k * 10,
                   y0 + bar / 2 + 14, col, op * vivo)
    return x0 + 8, y0 + bar + 8, x1 - 8, y1 - 8


def clip_en(p, nombre, seg, x0, y0, x1, y1, op=1.0, r=12, brillo=1.0, credito=None):
    p.imagen(Clip.cuadro(nombre, seg), x0, y0, x1, y1, op, r, brillo)
    if credito:
        p.texto(credito, x1 - 14, y1 - 12, 22, BLANCO, "med", 0.85 * op, "rb", sombra=0.9)


# ------------------------------------------------------------------ memoria compartida
HEX = "0123456789ABCDEF"


def memoria(p, x0, y0, x1, y1, t, k=1.0, act=1.0, nombre=True):
    """Bloque de memoria compartida: cabecera, rejilla de bytes que cambian y dos colas con sentido contrario."""
    if k <= 0.01:
        return
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    with p.pivote(cx, cy, k):
        p.glow(cx, cy, (x1 - x0) * 0.7, AMAR, 0.10 + 0.05 * math.sin(t * 6))
        p.rrect(x0, y0, x1, y1, 18, mix(PANEL, AMAR, 0.06), 0.98, borde=AMAR, w=5)
        for k2 in range(14):                                            # patas de chip
            px_ = x0 + 40 + k2 * (x1 - x0 - 80) / 13
            p.rect(px_ - 5, y0 - 16, px_ + 5, y0, AMAR, 0.8)
            p.rect(px_ - 5, y1, px_ + 5, y1 + 16, AMAR, 0.8)
        p.texto("MEMORIA COMPARTIDA", x0 + 26, y0 + 36, 32, AMAR, "black", 1, "lm", esp=0.04)
        if nombre:
            p.texto("Local\\SkyCraft_v1", x1 - 24, y0 + 36, 25, BLANCO, "mono", 0.9, "rm")
        cols, filas = 16, 3
        gw, gh = (x1 - x0 - 52) / cols, (y1 - y0 - 86) / filas
        for f in range(filas):
            for c in range(cols):
                i = f * cols + c
                fase = int(t * (6 + 22 * act * rnd(i, 2)) + rnd(i, 3) * 9)
                caliente = rnd(i, fase) > 1 - 0.28 * act
                bx, by = x0 + 26 + c * gw, y0 + 66 + f * gh
                colc = (CIAN, VERDE, LILA)[f]
                p.rrect(bx + 2, by + 2, bx + gw - 2, by + gh - 2, 5, mix(PANEL2, colc, 0.55 if caliente else 0.10))
                v = HEX[int(rnd(i, fase) * 16)] + HEX[int(rnd(i, fase + 5) * 16)]
                p.texto(v, bx + gw / 2, by + gh / 2 + 1, min(gh * 0.5, gw * 0.5), BLANCO if caliente else GRIS, "mono", 1)


def paquete(p, pts, u, color, r=9, cola=0.16):
    """Paquete de luz que recorre la polilínea `pts` (u = 0..1) con estela."""
    if not 0 <= u <= 1:
        return
    seg = [math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]
    tot = sum(seg)

    def en(v):
        d = clamp(v) * tot
        for k, s in enumerate(seg):
            if d <= s or k == len(seg) - 1:
                w_ = d / max(s, 1e-3)
                return lerp(pts[k][0], pts[k + 1][0], w_), lerp(pts[k][1], pts[k + 1][1], w_)
            d -= s
    for q in range(6):
        x, y = en(u - cola * q / 6)
        p.circ(x, y, r * (1 - q / 7), color, 1 - q / 6.5)
    x, y = en(u)
    p.glow(x, y, r * 5, color, 0.9)
    p.circ(x, y, r * 0.55, BLANCO)


def pista(p, pts, color, t, op=1.0, w=4):
    """Pista de circuito tenue con guiones que avanzan."""
    p.polilinea(pts, w, mix(color, NEGRO, 0.6), op)
    seg = [math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]
    tot = sum(seg)
    n = max(2, int(tot / 46))
    for k in range(n):
        d = ((k + t * 2.2) % n) / n * tot
        for q, s in enumerate(seg):
            if d <= s:
                u = d / max(s, 1e-3)
                p.circ(lerp(pts[q][0], pts[q + 1][0], u), lerp(pts[q][1], pts[q + 1][1], u), w * 0.8, color, 0.85 * op)
                break
            d -= s
