# -*- coding: utf-8 -*-
"""Escenas DIBUJADAS que viven dentro de las polaroids del tablero (portales). Cada una: f(p, t) pinta en el pintor `P` (960x540, coordenadas
de 1920x1080) el instante absoluto `t`. PORTAL[nombre](t) devuelve la imagen float32 (540, 960, 3) que el tablero deforma dentro de la foto.
Paleta: noche azul marino, luces cálidas, naranja bitcoin, rojo de tinta. Todo procedural (siluetas con esqueleto, objetos, ambientes)."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

from kit import INI, FIN, ww, we, TL  # anclas de la voz
from mg import *  # noqa: F401,F403
from mg_obj import *  # noqa: F401,F403
import tablero as T

PORTAL = {}
NARANJA = (0.97, 0.58, 0.10)
ORO = (1.0, 0.78, 0.25)
NAVY = (0.025, 0.040, 0.075)
NAVY2 = (0.060, 0.090, 0.150)


def portal(nombre):
    def deco(fn):
        def f(t):
            p = P()
            fn(p, t)
            vineta_p(p, 0.45)
            return np.clip(p.im, 0, 1.5)
        PORTAL[nombre] = f
        return fn
    return deco


# ------------------------------------------------------------------------------------------------ utilidades
@functools.lru_cache(maxsize=64)
def _sprite_moneda(r):
    """Moneda de bitcoin (RGBA float32, r en px del lienzo de media resolución)."""
    d = int(r * 2 + 4)
    pil = Image.new("RGBA", (d * 4, d * 4), (0, 0, 0, 0))
    dr = ImageDraw.Draw(pil)
    c = d * 2
    R = r * 4
    dr.ellipse([c - R, c - R, c + R, c + R], fill=(176, 96, 12, 255))
    dr.ellipse([c - R * 0.92, c - R * 0.92, c + R * 0.92, c + R * 0.92], fill=(247, 147, 26, 255))
    dr.ellipse([c - R * 0.80, c - R * 0.80, c + R * 0.80, c + R * 0.80], outline=(255, 200, 110, 255), width=max(1, int(R * 0.06)))
    f = T.fnt("sans_b", int(R * 1.15))
    dr.text((c, c + R * 0.04), "B", font=f, fill=(255, 250, 240, 255), anchor="mm")
    for dx in (-0.12, 0.12):
        dr.line([(c + R * dx, c - R * 0.72), (c + R * dx, c - R * 0.52)], fill=(255, 250, 240, 255), width=max(1, int(R * 0.09)))
        dr.line([(c + R * dx, c + R * 0.52), (c + R * dx, c + R * 0.72)], fill=(255, 250, 240, 255), width=max(1, int(R * 0.09)))
    pil = pil.resize((d, d), Image.LANCZOS)
    a = np.asarray(pil, np.float32) / 255.0
    return a


def moneda(p, x, y, r, op=1.0, giro=0.0):
    """Moneda en (x, y) coordenadas de 1920x1080; giro (0..1) la achata como si rotara."""
    rr = max(2, int(r * K))
    s = _sprite_moneda(rr)
    sx = max(1, int(s.shape[1] * abs(math.cos(giro * math.pi))))
    if sx < s.shape[1]:
        s = cv2.resize(s, (sx, s.shape[0]), interpolation=cv2.INTER_AREA)
    h, w = s.shape[:2]
    x0, y0 = int(x * K - w / 2), int(y * K - h / 2)
    xs0, ys0, xs1, ys1 = max(x0, 0), max(y0, 0), min(x0 + w, HW), min(y0 + h, HH)
    if xs1 <= xs0 or ys1 <= ys0:
        return
    sub = s[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    a = sub[..., 3:4] * op
    reg = p.im[ys0:ys1, xs0:xs1]
    reg *= 1 - a
    reg += sub[..., :3] * a


def candado(p, x, y, s, color=(0.75, 0.62, 0.28), op=1.0, abierto=0.0):
    p.rrect(x - s * 0.5, y - s * 0.2, x + s * 0.5, y + s * 0.6, s * 0.08, color, op)
    yy = y - s * 0.2 - abierto * s * 0.3
    p.polilinea([(x - s * 0.30, yy), (x - s * 0.30, yy - s * 0.32), (x - s * 0.18, yy - s * 0.48), (x + s * 0.18, yy - s * 0.48),
                 (x + s * 0.30, yy - s * 0.32), (x + s * 0.30, yy - (0 if abierto < 0.5 else s * 0.1))], s * 0.12, mix(color, (0.3, 0.3, 0.3), 0.3), op)
    p.circ(x, y + s * 0.15, s * 0.08, (0.12, 0.10, 0.08), op)
    p.rect(x - s * 0.03, y + s * 0.15, x + s * 0.03, y + s * 0.35, (0.12, 0.10, 0.08), op)


def sobre(p, x, y, w, color=CREMA, op=1.0, ang=0.0):
    h = w * 0.62
    R = rot((x, y), ang)
    pts = [R((x - w / 2, y - h / 2)), R((x + w / 2, y - h / 2)), R((x + w / 2, y + h / 2)), R((x - w / 2, y + h / 2))]
    p.poly([(q[0] + 8, q[1] + 10) for q in pts], (0, 0, 0), 0.3 * op)
    p.poly(pts, color, op)
    p.polilinea([pts[0], R((x, y + h * 0.08)), pts[1]], 4, mix(color, (0.4, 0.35, 0.3), 0.5), op)


def edificio_banco(p, cx, y, w, h, color=(0.80, 0.80, 0.78), sombra=SIL, op=1.0, letrero="BANCO"):
    columnas(p, cx, y, w, h, color, sombra, 6, op)
    if letrero:
        p.rrect(cx - w * 0.36, y - h * 1.30, cx + w * 0.36, y - h * 1.10, 8, (0.10, 0.10, 0.12), 0.85 * op)
        p.texto(letrero, cx, y - h * 1.20, h * 0.13, (0.95, 0.92, 0.80), "sans_b", op)


def flecha_p(p, a, b, w, color, op=1.0):
    p.linea(a, b, w, color, op)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = w * 3.2
    for s in (1, -1):
        p.linea(b, (b[0] - L * math.cos(ang + s * 0.5), b[1] - L * math.sin(ang + s * 0.5)), w, color, op)


def coche(p, x, y, esc, color=SIL, dir=1, luces=True, t=0.0, op=1.0):
    """Coche de perfil (silueta) con ruedas que giran; (x, y) = suelo bajo el centro."""
    E = esc
    f = dir
    p.poly([(x - f * E * 0.95, y - E * 0.18), (x - f * E * 0.95, y - E * 0.42), (x - f * E * 0.55, y - E * 0.48), (x - f * E * 0.32, y - E * 0.78),
            (x + f * E * 0.35, y - E * 0.78), (x + f * E * 0.62, y - E * 0.48), (x + f * E * 0.95, y - E * 0.42), (x + f * E * 0.98, y - E * 0.18)], color, op)
    p.poly([(x - f * E * 0.26, y - E * 0.72), (x + f * E * 0.02, y - E * 0.72), (x + f * E * 0.02, y - E * 0.50), (x - f * E * 0.48, y - E * 0.50)],
           (0.35, 0.45, 0.55), 0.35 * op)
    p.poly([(x + f * E * 0.08, y - E * 0.72), (x + f * E * 0.32, y - E * 0.72), (x + f * E * 0.55, y - E * 0.50), (x + f * E * 0.08, y - E * 0.50)],
           (0.35, 0.45, 0.55), 0.35 * op)
    for wx in (-0.58, 0.60):
        cxw = x + f * E * wx
        p.circ(cxw, y - E * 0.16, E * 0.18, (0.02, 0.02, 0.03), op)
        p.circ(cxw, y - E * 0.16, E * 0.09, (0.30, 0.30, 0.32), op)
        a = t * 12 * f
        p.linea((cxw - E * 0.08 * math.cos(a), y - E * 0.16 - E * 0.08 * math.sin(a)), (cxw + E * 0.08 * math.cos(a), y - E * 0.16 + E * 0.08 * math.sin(a)),
                E * 0.025, (0.1, 0.1, 0.1), op)
    if luces:
        p.haz(x + f * E * 0.97, y - E * 0.34, 0 if f > 0 else 180, E * 3.2, 18, (1.0, 0.95, 0.75), 0.35 * op)
        p.glow(x + f * E * 0.97, y - E * 0.34, E * 0.25, (1.0, 0.95, 0.8), 0.9 * op)
        p.glow(x - f * E * 0.95, y - E * 0.34, E * 0.18, (1.0, 0.15, 0.1), 0.8 * op)


def flash(p, x, y, t, t0, r=260):
    """Destello de cámara de fotos."""
    e = t - t0
    if 0 <= e < 0.25:
        a = (1 - e / 0.25) ** 2
        p.glow(x, y, r, (1.0, 1.0, 0.95), 1.4 * a)
        p.glow(x, y, r * 0.25, (1, 1, 1), 2.0 * a)


def camara_foto(p, x, y, s, color=SIL, op=1.0):
    p.rrect(x - s * 0.5, y - s * 0.32, x + s * 0.5, y + s * 0.32, s * 0.06, color, op)
    p.circ(x + s * 0.05, y, s * 0.22, (0.1, 0.12, 0.15), op)
    p.circ(x + s * 0.05, y, s * 0.14, (0.25, 0.35, 0.45), 0.6 * op)
    p.rect(x - s * 0.40, y - s * 0.44, x - s * 0.12, y - s * 0.32, color, op)


def fondo_noche(p, t, top=NAVY, bot=NAVY2, estrellas_=True):
    p.fondo(top, bot)
    if estrellas_:
        estrellas(p, t, 90, 4, 0.55, 0.6)


def foto_fondo(p, nombre, t, z0=1.05, z1=1.15, dur=8.0, t0=0.0, cx=0.5, cy=0.5, tono=(1.0, 1.0, 1.0), brillo=0.85, gris=False):
    """Foto real como fondo del lienzo con zoom lento (Ken Burns)."""
    im = _foto(nombre)
    z = z0 + (z1 - z0) * smooth((t - t0) / dur)
    h, w = im.shape[:2]
    k = max(HW / w, HH / h) * z
    M = np.array([[k, 0, HW / 2 - k * w * cx], [0, k, HH / 2 - k * h * cy]], np.float32)
    out = cv2.warpAffine(im, M, (HW, HH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if gris:
        out = np.repeat(out.mean(2, keepdims=True), 3, 2)
    p.im[:] = out * np.float32(tono) * brillo


@functools.lru_cache(maxsize=16)
def _foto(nombre):
    im = T.cargar_img(nombre, 1400).astype(np.float32) / 255.0
    return im


# ================================================================================================ GANCHO / FORTUNA: la bóveda
@portal("boveda")
def boveda(p, t):
    """Montaña de monedas de bitcoin en una bóveda oscura, intacta: polvo, telarañas, luz que barre."""
    p.fondo((0.015, 0.018, 0.03), (0.05, 0.045, 0.04))
    # pared de bóveda con remaches
    for x in range(0, W, 160):
        p.rect(x, 0, x + 6, 720, (0.0, 0.0, 0.0), 0.25)
    for y in range(80, 720, 140):
        for x in range(60, W, 160):
            p.circ(x, y, 6, (0.12, 0.12, 0.13))
    # haz de linterna que barre
    ang = 70 + 25 * math.sin(t * 0.5)
    p.haz(960, -60, ang, 1500, 26, (1.0, 0.85, 0.55), 0.22)
    # montaña de monedas (determinista)
    rng = np.random.default_rng(7)
    for i in range(520):
        u = rng.random()
        x = 960 + (rng.random() - 0.5) * 1700 * (1 - u * 0.75)
        y = 1060 - u * 520 + rng.random() * 40
        r = 30 + rng.random() * 16
        g = rng.random() * 0.45
        moneda(p, x, y, r, 1.0, g)
    # brillos que pasan por la montaña
    for k in range(6):
        x = 960 + 700 * math.sin(t * 0.8 + k * 1.7)
        y = 820 + 140 * math.cos(t * 0.6 + k)
        p.glow(x, y, 90, (1.0, 0.85, 0.5), 0.25 + 0.2 * math.sin(t * 3 + k))
    polvo(p, t, 70, 3, 0.5, (1.0, 0.9, 0.7), 10)
    # telaraña en la esquina
    for k in range(7):
        a = math.radians(5 + k * 13)
        p.linea((0, 0), (420 * math.cos(a), 420 * math.sin(a)), 2, (0.7, 0.7, 0.7), 0.25)
    for r in (90, 170, 250, 330):
        pts = [(r * math.cos(math.radians(5 + k * 13)), r * math.sin(math.radians(5 + k * 13))) for k in range(7)]
        p.polilinea(pts, 2, (0.7, 0.7, 0.7), 0.22)


# ================================================================================================ ORIGEN
@portal("lehman")
def lehman(p, t):
    """Foto real de la noche de la quiebra (Robert Scoble, CC BY 2.0) + gráfica de bolsa que se desploma encima."""
    t0 = ww("origen", 1, "quince") - 0.4
    foto_fondo(p, "lehman_dia", t, 1.04, 1.16, 7.0, t0, 0.5, 0.45, (0.9, 0.95, 1.05), 0.8)
    p.rect(0, 0, W, H, (0.0, 0.02, 0.06), 0.35)
    u = smooth((t - t0 - 0.6) / 3.0)
    pts = []
    rng = np.random.default_rng(3)
    n = 60
    for i in range(int(n * u) + 1):
        s = i / n
        yv = 330 + 80 * math.sin(s * 9) * (1 - s) + 600 * s ** 2.2 + rng.normal(0, 14)
        pts.append((140 + s * 1640, yv))
    if len(pts) > 1:
        p.polilinea(pts, 9, (1.0, 0.18, 0.15), 0.95)
        p.glow(pts[-1][0], pts[-1][1], 70, (1.0, 0.2, 0.15), 0.9)
    p.texto("15 · SEP · 2008", 1620, 120, 70, (1.0, 0.95, 0.85), "abril", 0.95 * smooth((t - t0) / 0.6))


@portal("rescate")
def rescate(p, t):
    """Dinero público (sacos con monedas) que sale de un edificio de gobierno y viaja en cinta hacia los bancos; gente protestando."""
    t0 = INI("origen", 2)
    fondo_noche(p, t, (0.03, 0.05, 0.09), (0.09, 0.12, 0.18))
    ciudad(p, t, 760, (0.04, 0.06, 0.10), off=t * 8, seed=4, h_max=380)
    suelo(p, 760, (0.06, 0.07, 0.09), (0.02, 0.02, 0.03))
    edificio_banco(p, 330, 740, 420, 420, (0.82, 0.82, 0.80), SIL, 1.0, "GOBIERNO")
    for i, x in enumerate((1250, 1650)):
        edificio_banco(p, x, 740, 300, 360, (0.70, 0.72, 0.76), SIL, 1.0, "BANCO")
    # cinta transportadora
    p.rect(520, 690, 1520, 704, (0.25, 0.25, 0.28))
    for k in range(14):
        x = 520 + ((t - t0) * 180 + k * 72) % 1000
        p.rect(x, 692, x + 4, 702, (0.4, 0.4, 0.42))
    for k in range(6):
        s = ((t - t0) * 0.22 + k / 6) % 1.0
        x = 540 + s * 960
        y = 640 - 30 * math.sin(s * math.pi * 6) * 0.1
        p.elip(x, y + 10, 44, 48, 0, (0.55, 0.42, 0.22))
        p.rect(x - 12, y - 46, x + 12, y - 32, (0.45, 0.33, 0.16))
        p.texto("$", x, y + 14, 46, (0.95, 0.88, 0.55), "sans_b")
    # gente con carteles (abajo, en primer plano)
    p.rect(0, 900, W, H, (0.01, 0.012, 0.02), 0.7)
    multitud(p, 11, 80, 1840, 1130, 230, (0.03, 0.035, 0.05), t, 5, pose=lambda tt, i: pose_cartel(tt + i, i * 0.7),
             objeto=lambda pp, wr, wl, f: (pp.linea((wr[0], wr[1]), (wr[0], wr[1] - 70), 5, (0.35, 0.25, 0.15)), pp.rect(wr[0] - 46, wr[1] - 130, wr[0] + 46, wr[1] - 66, (0.85, 0.82, 0.74))))


@portal("escritorio")
def escritorio(p, t):
    """Alguien, de noche, escribiendo código: silueta de espaldas, monitor, ventana con ciudad; calendario 2007 -> 2008."""
    t0 = INI("origen", 3)
    p.fondo((0.012, 0.016, 0.028), (0.03, 0.035, 0.05))
    # ventana
    p.rect(1180, 120, 1760, 600, (0.04, 0.07, 0.13))
    p.im_save = None
    ciudad(p, t, 600, (0.02, 0.03, 0.06), off=0, seed=8, h_max=300, ancho_med=70)
    p.rect(1170, 110, 1770, 122, (0.08, 0.08, 0.1))
    p.rect(1170, 598, 1770, 610, (0.08, 0.08, 0.1))
    p.rect(1465, 110, 1475, 610, (0.08, 0.08, 0.1))
    luna(p, 1640, 210, 34)
    suelo(p, 880, (0.03, 0.03, 0.04), (0.01, 0.01, 0.015))
    escritorio_pc(p, 760, 900, 900, t - t0, True, (0.55, 0.95, 0.65))
    _de_espaldas(p, 760, 900, 1.0, t)
    # calendario de pared que pasa de 2007 a 2008
    u = smooth((t - t0 - 1.0) / 1.2)
    hoja_cal(p, 330, 330, 230, 250, "AÑO", "2007" if u < 0.5 else "2008", (u * 2 if u < 0.5 else 0.0))
    p.glow(760, 520, 520, (0.4, 0.9, 0.6), 0.10)
    vela(p, 1200, 860, 60, t, amt=0.6)


def _de_espaldas(p, x, y, e, t, col=(0.012, 0.014, 0.022)):
    """Persona sentada de espaldas ante el escritorio: respaldo de silla, hombros, cabeza con pelo, brazos hacia el teclado."""
    p.rrect(x - 150 * e, y - 330 * e, x + 150 * e, y - 40 * e, 30 * e, (0.05, 0.05, 0.06))
    p.rect(x - 12 * e, y - 40 * e, x + 12 * e, y + 60 * e, (0.05, 0.05, 0.06))
    p.poly([(x - 175 * e, y - 300 * e), (x + 175 * e, y - 300 * e), (x + 150 * e, y - 120 * e), (x - 150 * e, y - 120 * e)], col)
    p.elip(x, y - 300 * e, 175 * e, 50 * e, 0, col)
    tecleo = 4 * math.sin(t * 14)
    for s_ in (-1, 1):
        p.polilinea([(x + s_ * 160 * e, y - 290 * e), (x + s_ * 200 * e, y - 360 * e), (x + s_ * 110 * e, y - 415 * e + s_ * tecleo)], 46 * e, col)
    p.capsula = None
    p.rect(x - 28 * e, y - 360 * e, x + 28 * e, y - 320 * e, col)
    p.elip(x, y - 410 * e, 70 * e, 82 * e, 0, col)
    p.elip(x, y - 440 * e, 74 * e, 58 * e, 0, (0.02, 0.018, 0.02))
    p.glow(x, y - 470 * e, 160 * e, (0.35, 0.95, 0.55), 0.10)


@portal("navegador")
def navegador(p, t):
    """Ventana de navegador de 2008 donde se escribe el dominio y se registra."""
    t0 = ww("origen", 4, "registrado") - 0.3
    p.fondo((0.10, 0.13, 0.20), (0.04, 0.05, 0.09))
    x0, y0, x1, y1 = 260, 170, 1660, 900
    p.rect(x0 + 18, y0 + 22, x1 + 18, y1 + 22, (0, 0, 0), 0.4)
    p.rect(x0, y0, x1, y1, (0.92, 0.92, 0.90))
    p.rect(x0, y0, x1, y0 + 70, (0.62, 0.68, 0.80), grad=((0.70, 0.76, 0.88), (0.50, 0.56, 0.70)))
    for k, c in enumerate(((0.9, 0.3, 0.3), (0.95, 0.8, 0.3), (0.4, 0.8, 0.4))):
        p.circ(x0 + 34 + k * 34, y0 + 35, 11, c)
    p.rrect(x0 + 160, y0 + 92, x1 - 40, y0 + 152, 10, (1, 1, 1))
    url = "http://www.bitcoin.org"
    n = int(clamp((t - t0) / 1.6) * len(url))
    p.texto(url[:n] + ("|" if int(t * 3) % 2 == 0 else ""), x0 + 190, y0 + 122, 40, (0.1, 0.1, 0.15), "mono", 1, "lm")
    if t > t0 + 1.9:
        u = smooth((t - t0 - 1.9) / 0.5)
        p.texto("Dominio registrado", (x0 + x1) / 2, 470, 64, (0.12, 0.30, 0.55), "sans_b", u)
        p.texto("18 · 08 · 2008", (x0 + x1) / 2, 590, 90, (0.80, 0.10, 0.10), "abril", u)
        check(p, (x0 + x1) / 2, 760, 70, smooth((t - t0 - 2.3) / 0.5))


@portal("p2p")
def p2p(p, t):
    """Dos personas se pasan una moneda directamente por una red de nodos; el banco del medio se tacha."""
    t0 = INI("origen", 9)
    fondo_noche(p, t)
    rng = np.random.default_rng(12)
    nodos = [(rng.uniform(80, 1840), rng.uniform(60, 640)) for _ in range(26)]
    for i, a in enumerate(nodos):
        for b in nodos[i + 1:i + 3]:
            p.linea(a, b, 2, (0.3, 0.5, 0.8), 0.25)
        p.circ(a[0], a[1], 7, (0.5, 0.75, 1.0), 0.6 + 0.4 * math.sin(t * 2 + i))
    suelo(p, 900, (0.05, 0.06, 0.09), (0.02, 0.02, 0.03))
    persona(p, 420, 900, 420, pose_señalar(1.0), (0.01, 0.012, 0.02), 1)
    persona(p, 1500, 900, 400, pose_señalar(0.8), (0.01, 0.012, 0.02), -1, pelo="largo")
    edificio_banco(p, 960, 880, 260, 300, (0.55, 0.56, 0.60), SIL, 0.8, "BANCO")
    u = smooth((t - t0 - 0.3) / 1.6)
    x = 560 + u * 800
    y = 560 - 260 * math.sin(u * math.pi)
    moneda(p, x, y, 52, 1.0, (t * 1.5) % 1.0 * 0.4)
    p.glow(x, y, 160, NARANJA, 0.6)
    if t > t0 + 1.0:
        cruz(p, 960, 720, 170, smooth((t - t0 - 1.0) / 0.5), ROJO, 22)


# ================================================================================================ GÉNESIS
@portal("bloques")
def bloques(p, t):
    """La cadena se forma: el bloque 0 se enciende y los siguientes se enganchan."""
    t0 = INI("genesis", 0)
    fondo_noche(p, t, (0.02, 0.03, 0.06), (0.05, 0.07, 0.12))
    n = int(clamp((t - t0) / 0.55) * 6) + 1
    for k in range(min(n, 6)):
        x = 330 + k * 290 - (t - t0) * 20
        y = 540 + 18 * math.sin(t * 1.2 + k)
        u = smooth((t - t0 - k * 0.55) / 0.4)
        if k == 0:
            u = max(u, 0.85)
        s = 200 * (0.6 + 0.4 * u)
        col = (0.95, 0.60, 0.12) if k == 0 else (0.30, 0.42, 0.62)
        p.glow(x, y, s * 1.4, col, 0.25 * u)
        # cubo isométrico sencillo
        p.poly([(x - s / 2, y - s * 0.3), (x, y - s * 0.55), (x + s / 2, y - s * 0.3), (x, y - s * 0.05)], mix(col, (1, 1, 1), 0.35), u)
        p.poly([(x - s / 2, y - s * 0.3), (x, y - s * 0.05), (x, y + s * 0.5), (x - s / 2, y + s * 0.25)], col, u)
        p.poly([(x + s / 2, y - s * 0.3), (x, y - s * 0.05), (x, y + s * 0.5), (x + s / 2, y + s * 0.25)], mix(col, (0, 0, 0), 0.35), u)
        p.texto(str(k), x - s * 0.24, y + s * 0.12, s * 0.28, (1, 1, 1), "sans_b", u)
        if k > 0:
            p.linea((x - 290 + s / 2, y), (x - s / 2, y), 8, (0.7, 0.8, 0.95), u * 0.8)
    p.texto("BLOQUE 0", 330 - (t - t0) * 20, 830, 64, (1.0, 0.8, 0.4), "sans_b", smooth((t - t0 - 0.4) / 0.5))
    p.texto("3 · ENE · 2009", 330 - (t - t0) * 20, 905, 48, (0.95, 0.95, 0.95), "mono", smooth((t - t0 - 0.6) / 0.5))


# ================================================================================================ FANTASMA
@portal("pizza")
def pizza(p, t):
    """Dos pizzas a cambio de una montaña de 10.000 monedas; el valor de hoy sube en un contador."""
    t0 = INI("fantasma", 4)
    p.fondo((0.10, 0.06, 0.04), (0.03, 0.02, 0.02))
    p.rect(0, 760, W, H, (0.30, 0.18, 0.10), grad=((0.36, 0.22, 0.12), (0.16, 0.10, 0.06)))
    for k in range(2):
        x, y = 470 + k * 120, 640 - k * 60
        p.rect(x - 230, y - 20, x + 230, y + 30, (0.90, 0.86, 0.78))
        p.rect(x - 230, y - 26, x + 230, y - 16, (0.75, 0.68, 0.58))
    cx, cy = 590, 520
    p.circ(cx, cy, 210, (0.85, 0.55, 0.20))
    p.circ(cx, cy, 186, (0.92, 0.36, 0.16))
    rng = np.random.default_rng(4)
    for i in range(14):
        a, r = rng.random() * 6.28, rng.random() * 150
        p.circ(cx + r * math.cos(a), cy + r * math.sin(a), 18, (0.65, 0.12, 0.08))
    for k in range(4):
        a = k * math.pi / 4 + 0.3
        p.linea((cx - 200 * math.cos(a), cy - 200 * math.sin(a)), (cx + 200 * math.cos(a), cy + 200 * math.sin(a)), 3, (0.6, 0.3, 0.1), 0.8)
    flecha_p(p, (860, 470), (1080, 470), 14, (1, 1, 1), 0.9)
    flecha_p(p, (1080, 570), (860, 570), 14, (1, 1, 1), 0.9)
    u = smooth((t - t0 - 0.3) / 2.5)
    rng = np.random.default_rng(9)
    for i in range(int(260 * u)):
        uu = rng.random()
        x = 1430 + (rng.random() - 0.5) * 620 * (1 - uu * 0.7)
        y = 900 - uu * 420 + rng.random() * 20
        moneda(p, x, y, 26, 1.0, rng.random() * 0.4)
    p.texto("10.000 BTC", 1430, 230, 84, NARANJA, "abril", smooth((t - t0) / 0.5))
    p.texto("22 · MAYO · 2010", 590, 230, 60, (1, 0.95, 0.85), "abril", smooth((t - t0) / 0.5))


@portal("wikileaks")
def wikileaks(p, t):
    """Tarjetas de pago con candado: las donaciones quedan bloqueadas; alguien en el foro señala la moneda."""
    t0 = INI("fantasma", 5)
    fondo_noche(p, t, (0.03, 0.03, 0.05), (0.08, 0.06, 0.08))
    for k in range(3):
        x, y = 420 + k * 360, 420 + 40 * math.sin(k)
        p.rrect(x - 150, y - 95, x + 150, y + 95, 18, [(0.25, 0.35, 0.65), (0.75, 0.25, 0.22), (0.30, 0.55, 0.40)][k])
        p.rect(x - 150, y - 50, x + 150, y - 20, (0.05, 0.05, 0.06))
        p.rrect(x - 120, y + 10, x - 60, y + 50, 6, (0.85, 0.75, 0.35))
        uu = smooth((t - t0 - 0.4 - k * 0.35) / 0.4)
        candado(p, x + 70, y + 30, 120 * (0.6 + 0.4 * uu), (0.70, 0.70, 0.74), uu)
    # caja de donaciones vacía
    p.rect(1450, 520, 1750, 760, (0.55, 0.40, 0.22))
    p.rect(1450, 500, 1750, 530, (0.45, 0.32, 0.18))
    p.rect(1560, 506, 1640, 518, (0.05, 0.04, 0.03))
    p.texto("DONACIONES", 1600, 640, 34, (0.95, 0.92, 0.85), "sans_b")
    cruz(p, 1600, 630, 160, smooth((t - t0 - 1.6) / 0.5), ROJO, 18)
    suelo(p, 900, (0.04, 0.04, 0.06), (0.01, 0.01, 0.02))
    persona(p, 1200, 1000, 300, pose_señalar(1.0), (0.01, 0.01, 0.02), 1)
    moneda(p, 1340, 760, 46, smooth((t - t0 - 2.2) / 0.4), (t * 0.8) % 0.5)


# ================================================================================================ PERFIL
@portal("maquina")
def maquina(p, t):
    """Máquina de escribir que teclea una frase con DOS espacios tras el punto (el hueco se resalta)."""
    t0 = INI("perfil", 3)
    p.fondo((0.08, 0.06, 0.05), (0.03, 0.025, 0.02))
    # hoja
    p.rect(560, 60, 1360, 560, (0.95, 0.93, 0.86))
    txt = "It works.  The next step"
    n = int(clamp((t - t0) / 2.0) * len(txt))
    x = 620
    for i, ch in enumerate(txt[:n]):
        p.texto(ch, x, 300, 64, (0.08, 0.08, 0.10), "mono", 1, "lm")
        x += 39
    i_pt = txt.index(".") + 1
    if n > i_pt + 2:
        u = smooth((t - t0 - 1.2) / 0.4)
        xa = 620 + i_pt * 39
        p.rect(xa - 4, 250, xa + 2 * 39 - 4, 350, (1.0, 0.85, 0.15), 0.55 * u)
        p.texto("2 espacios", xa + 39, 420, 50, ROJO, "sans_b", u)
    # cuerpo de la máquina
    p.poly([(420, 620), (1500, 620), (1620, 1000), (300, 1000)], (0.10, 0.10, 0.11))
    p.rect(470, 560, 1450, 640, (0.16, 0.16, 0.17))
    p.rect(470, 590, 1450, 610, (0.05, 0.05, 0.05))
    rng = np.random.default_rng(1)
    for f in range(4):
        for k in range(12):
            x = 520 + f * 30 + k * 82
            y = 700 + f * 70
            pul = 1 if (int((t - t0) * 9) % 12 == k and f == int((t - t0) * 3) % 4) else 0
            p.circ(x, y + pul * 8, 30, (0.85, 0.83, 0.78) if not pul else (1.0, 0.9, 0.6))
            p.circ(x, y + pul * 8, 30, (0, 0, 0), 0.0)
    # brazo de tipo que golpea
    if n < len(txt):
        a = abs(math.sin((t - t0) * 9 * math.pi))
        p.linea((960, 600), (960 - 0, 600 - 260 * a), 10, (0.6, 0.6, 0.62))


@portal("relojes")
def relojes(p, t):
    """Tres relojes: Londres, Nueva York y Tokio en el hueco sin mensajes (5:00-12:00 UTC)."""
    t0 = ww("perfil", 7, "costa")
    p.fondo((0.03, 0.04, 0.07), (0.08, 0.09, 0.13))
    hora_utc = 5.0 + 7.0 * clamp((t - t0 + 1.0) / 6.0)
    for k, (nom, off) in enumerate((("LONDRES", 0), ("NUEVA YORK", -5), ("TOKIO", 9))):
        cx = 400 + k * 560
        h = (hora_utc + off) % 24
        noche = h < 6 or h >= 20
        p.glow(cx, 450, 330, (0.25, 0.35, 0.65) if noche else (1.0, 0.8, 0.4), 0.25)
        reloj(p, cx, 450, 200, 0.0, h % 12, (h % 1) * 60, False)
        p.texto(nom, cx, 740, 52, (0.95, 0.95, 0.95), "sans_b")
        p.texto(f"{int(h):02d}:{int((h % 1) * 60):02d}", cx, 820, 60, (1.0, 0.8, 0.3) if not noche else (0.6, 0.75, 1.0), "mono")
        p.texto("NOCHE" if noche else "DÍA", cx, 900, 40, (0.6, 0.75, 1.0) if noche else (1.0, 0.8, 0.3), "sans", 0.9)


# ================================================================================================ DORIAN
@portal("puerta")
def puerta(p, t):
    """Una casa de suburbio a pleno día: un hombre mayor en la puerta y una periodista con libreta."""
    t0 = INI("dorian", 2)
    p.fondo((0.45, 0.62, 0.82), (0.80, 0.86, 0.90))
    p.circ(1600, 160, 70, (1.0, 0.95, 0.75))
    p.glow(1600, 160, 300, (1.0, 0.9, 0.6), 0.4)
    p.rect(0, 820, W, H, (0.42, 0.55, 0.30), grad=((0.45, 0.58, 0.32), (0.30, 0.40, 0.22)))
    # casa
    p.rect(200, 420, 1300, 840, (0.88, 0.84, 0.74))
    p.poly([(150, 430), (750, 220), (1350, 430)], (0.45, 0.28, 0.22))
    p.rect(640, 520, 860, 840, (0.30, 0.20, 0.14))
    p.rect(660, 540, 840, 830, (0.42, 0.36, 0.30))
    p.glow(750, 700, 160, (1.0, 0.9, 0.7), 0.15)
    for x in (330, 1040):
        p.rect(x, 520, x + 180, 680, (0.55, 0.70, 0.85))
        p.rect(x + 86, 520, x + 94, 680, (0.88, 0.84, 0.74))
    palmera(p, 1500, 840, 520, t)
    persona(p, 750, 830, 290, pose_estar(t), (0.07, 0.07, 0.09), 1, ropa="chaqueta", pelo="corto")
    persona(p, 1060, 905, 330, pose_señalar(0.35), (0.10, 0.11, 0.16), -1, pelo="largo",
            objeto=lambda pp, wr, wl, f: pp.rect(wr[0] - 26, wr[1] - 40, wr[0] + 26, wr[1] + 10, (0.95, 0.95, 0.9)))
    u = smooth((t - t0 - 0.8) / 0.4)
    if u > 0:
        p.rrect(520, 300, 940, 420, 30, (1, 1, 1), 0.95 * u)
        p.poly([(700, 418), (740, 418), (720, 470)], (1, 1, 1), 0.95 * u)
        p.texto("...", 730, 360, 70, (0.1, 0.1, 0.1), "sans_b", u)


def palmera(p, x, y, h, t, color=(0.08, 0.10, 0.08)):
    p.polilinea([(x, y), (x + h * 0.05, y - h * 0.5), (x + h * 0.02, y - h)], h * 0.04, (0.35, 0.25, 0.15))
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.45 + 0.05 * math.sin(t * 1.2 + k)
        L = h * 0.42
        tip = (x + h * 0.02 + L * math.cos(a), y - h + L * math.sin(a) + L * 0.35)
        mid = (x + h * 0.02 + L * 0.55 * math.cos(a), y - h + L * 0.55 * math.sin(a) - L * 0.05)
        p.polilinea([(x + h * 0.02, y - h), mid, tip], h * 0.028, (0.15, 0.35, 0.15))


@portal("persecucion")
def persecucion(p, t):
    """Calles de Los Ángeles: un coche y detrás varios coches de reporteros con flashes."""
    t0 = INI("dorian", 4)
    p.fondo((0.55, 0.70, 0.88), (0.92, 0.85, 0.72))
    off = (t - t0) * 600
    for k in range(10):
        x = (k * 380 - off * 0.3) % 2300 - 200
        palmera(p, x, 760, 420 + 80 * (k % 3), t, (0.1, 0.12, 0.1))
    ciudad(p, t, 720, (0.55, 0.58, 0.65), off=off * 0.15, seed=3, ventanas=False, h_max=260)
    p.rect(0, 740, W, H, (0.22, 0.22, 0.24))
    for k in range(12):
        x = (k * 260 - off) % 2400 - 200
        p.rect(x, 900, x + 130, 914, (0.95, 0.85, 0.3))
    coche(p, 1500, 1000, 330, (0.70, 0.71, 0.75), 1, False, t)
    for k, x in enumerate((880, 380, -60)):
        coche(p, x + 20 * math.sin(t * 2 + k), 1030 + k * 8, 300, [(0.15, 0.30, 0.55), (0.55, 0.12, 0.10), (0.20, 0.20, 0.22)][k], 1, False, t)
        flash(p, x + 120, 820, t, t0 + 0.6 + k * 0.7 + 1.9 * (int((t - t0) / 1.9)))


@portal("cuadras")
def cuadras(p, t):
    """Esquema de calles (vista de plano): dos casas a unas cuadras, en el mismo pueblo."""
    t0 = ww("dorian", 8, "cuadras")
    p.fondo((0.90, 0.88, 0.82), (0.86, 0.84, 0.78))
    for x in range(100, W, 260):
        p.rect(x, 0, x + 34, H, (0.70, 0.68, 0.64))
    for y in range(80, H, 220):
        p.rect(0, y, W, y + 34, (0.70, 0.68, 0.64))
    rng = np.random.default_rng(5)
    for x in range(134, W, 260):
        for y in range(114, H, 220):
            for k in range(3):
                p.rect(x + 18 + k * 72, y + 30, x + 76 + k * 72, y + 150, (0.80, 0.77, 0.70))
    a, b = (520, 420), (1350, 640)
    u = smooth((t - t0) / 1.6)
    pin(p, a[0], a[1], 26, ROJO, t, True)
    p.texto("DORIAN", a[0], a[1] - 70, 46, (0.6, 0.06, 0.06), "sans_b")
    if u > 0.05:
        pts = [(a[0], a[1]), (a[0], 560), (b[0] * u + a[0] * (1 - u), 560)]
        if u > 0.6:
            pts.append((b[0], 560 + (b[1] - 560) * smooth((u - 0.6) / 0.4)))
        p.polilinea(pts, 10, (0.15, 0.35, 0.80), 0.85)
    if u > 0.95:
        pin(p, b[0], b[1], 26, (0.15, 0.35, 0.80), t, True)
        p.texto("¿?", b[0], b[1] - 70, 56, (0.15, 0.35, 0.80), "sans_b")
    p.texto("TEMPLE CITY, CALIFORNIA · ESQUEMA", 960, 1020, 34, (0.3, 0.3, 0.3), "sans")


# ================================================================================================ HAL
@portal("carrera")
def carrera(p, t):
    """18-abr-2009: corredores en Santa Bárbara (mar, palmeras); reloj de carrera; un correo sale a las 9:16 y él cruza la meta a las 9:18."""
    t0 = INI("hal", 6)
    p.fondo((0.50, 0.72, 0.92), (0.95, 0.88, 0.72))
    p.rect(0, 520, W, 640, (0.20, 0.45, 0.65), grad=((0.25, 0.52, 0.72), (0.15, 0.38, 0.55)))
    for k in range(8):
        x = (k * 300 - (t - t0) * 90) % 2300 - 200
        p.linea((x, 560 + 10 * (k % 3)), (x + 120, 560 + 10 * (k % 3)), 4, (1, 1, 1), 0.4)
    for k in range(7):
        x = (k * 340 - (t - t0) * 260) % 2400 - 200
        palmera(p, x, 700, 380 + 60 * (k % 2), t)
    p.rect(0, 690, W, H, (0.40, 0.40, 0.42))
    p.rect(0, 690, W, 704, (0.85, 0.85, 0.80))
    for k in range(6):
        ph = (t - t0) * 9 + k * 1.3
        x = 380 + k * 230 + 30 * math.sin(t + k)
        persona(p, x, 980 + (k % 2) * 30, 330, pose_correr(ph), [(0.10, 0.10, 0.14), (0.55, 0.12, 0.10), (0.10, 0.25, 0.55)][k % 3], 1,
                pelo="largo" if k % 3 == 1 else "corto")
    # reloj de carrera: 8:00 + minutos
    h_min = 76.0 + clamp((t - t0) / 6.0) * 2.0      # 9:16 -> 9:18
    hh, mm = 8 + int(h_min // 60), int(h_min % 60)
    p.rrect(1380, 70, 1840, 230, 14, (0.05, 0.05, 0.06))
    p.texto(f"{hh}:{mm:02d}", 1610, 150, 110, (1.0, 0.25, 0.15), "mono")
    # el correo sale de una silueta-pantalla en la esquina
    u = smooth((t - t0 - 0.5) / 2.2)
    sobre(p, 200 + u * 900, 240 - math.sin(u * math.pi) * 120, 160, CREMA, smooth((t - t0 - 0.3) / 0.3) * (1 - smooth((u - 0.9) / 0.1)))
    p.texto("correo de Satoshi · 9:16", 420, 120, 44, (0.1, 0.1, 0.15), "sans_b", smooth((t - t0 - 0.3) / 0.4))
    if t > t0 + 3.2:
        p.texto("META · 9:18", 960, 360, 80, (0.85, 0.08, 0.08), "abril", smooth((t - t0 - 3.2) / 0.4))


@portal("crio")
def crio(p, t):
    """Cápsula criogénica con escarcha y luz azul (ilustración)."""
    t0 = INI("hal", 9)
    p.fondo((0.01, 0.02, 0.04), (0.03, 0.05, 0.09))
    p.haz(960, -40, 90, 1200, 30, (0.6, 0.85, 1.0), 0.25)
    p.rrect(760, 140, 1160, 1000, 180, (0.55, 0.62, 0.70))
    p.rrect(790, 170, 1130, 970, 160, (0.18, 0.30, 0.42))
    p.glow(960, 560, 380, (0.4, 0.75, 1.0), 0.35 + 0.08 * math.sin(t * 1.5))
    for k in range(9):
        y = 230 + k * 85
        p.linea((820, y), (1100, y + 10 * math.sin(k)), 3, (0.85, 0.95, 1.0), 0.25)
    polvo(p, t, 60, 9, 0.6, (0.8, 0.95, 1.0), 14)
    niebla(p, t, 900, 220, (0.6, 0.8, 1.0), 0.35, 20, 3)
    p.texto("ILUSTRACIÓN", 960, 1040, 26, (0.6, 0.7, 0.8), "sans", 0.7)


# ================================================================================================ SZABO
@portal("bitgold")
def bitgold(p, t):
    """Oro digital: computadoras calculan y de sus pantallas salen lingotes de oro (bit gold, 1998)."""
    t0 = ww("szabo", 1, "llamado")
    fondo_noche(p, t, (0.02, 0.03, 0.05), (0.06, 0.06, 0.08))
    for k in range(3):
        x = 380 + k * 580
        escritorio_pc(p, x, 760, 520, t - t0 + k, True, (0.95, 0.80, 0.30))
    for k in range(9):
        s = ((t - t0) * 0.35 + k / 9) % 1.0
        x = 380 + (k % 3) * 580 + (s * 200 - 100)
        y = 380 - s * 280 + 1080 * 0
        u = 1 - abs(s - 0.5) * 2
        p.poly([(x - 60, y), (x + 60, y), (x + 40, y - 40), (x - 40, y - 40)], ORO, u)
        p.poly([(x - 40, y - 40), (x + 40, y - 40), (x + 30, y - 52), (x - 30, y - 52)], mix(ORO, (1, 1, 1), 0.4), u)
        p.glow(x, y - 20, 90, ORO, 0.4 * u)
    p.texto("BIT GOLD · 1998", 960, 960, 76, ORO, "abril", smooth((t - t0) / 0.5))


# ================================================================================================ WRIGHT
@portal("escenario")
def escenario(p, t):
    """Mayo de 2016: un foco sobre un atril; la silueta anuncia «yo soy Satoshi»; flashes."""
    t0 = INI("wright", 2)
    p.fondo((0.01, 0.01, 0.02), (0.04, 0.03, 0.05))
    p.haz(960, -40, 90, 1150, 28, (1.0, 0.95, 0.85), 0.45)
    p.elip(960, 960, 360, 60, 0, (1.0, 0.95, 0.85), 0.18)
    persona(p, 960, 960, 430, pose_señalar(0.4 + 0.3 * math.sin(t * 1.3)), (0.02, 0.02, 0.03), 1, ropa="chaqueta")
    p.poly([(860, 980), (1060, 980), (1030, 720), (890, 720)], (0.22, 0.16, 0.12))
    multitud(p, 12, 60, 1860, 1120, 260, (0.0, 0.0, 0.0), t, 3)
    for k in range(5):
        flash(p, 200 + k * 380, 900, t, t0 + 0.4 + k * 0.45 + 2.3 * int((t - t0) / 2.3))
    u = smooth((t - t0 - 0.8) / 0.4)
    if u > 0:
        p.rrect(1150, 300, 1760, 450, 30, (1, 1, 1), 0.95 * u)
        p.poly([(1180, 440), (1240, 440), (1120, 520)], (1, 1, 1), 0.95 * u)
        p.texto("«Yo soy Satoshi»", 1455, 375, 60, (0.1, 0.1, 0.12), "serif", u)


@portal("fotocopia")
def fotocopia(p, t):
    """Una fotocopiadora copia una firma ajena: la luz pasa y sale la misma firma."""
    t0 = INI("wright", 5)
    p.fondo((0.06, 0.07, 0.09), (0.02, 0.02, 0.03))
    p.rect(420, 380, 1500, 860, (0.80, 0.80, 0.78))
    p.rect(420, 340, 1500, 400, (0.65, 0.66, 0.66))
    p.rect(470, 410, 1450, 460, (0.15, 0.20, 0.25))
    s = ((t - t0) * 0.6) % 1.0
    p.rect(470 + s * 960, 410, 520 + s * 960, 460, (0.7, 1.0, 0.8), 0.9)
    p.glow(495 + s * 960, 435, 120, (0.6, 1.0, 0.8), 0.5)
    # hoja original (arriba) y copia que sale (derecha)
    for k, (x, y, op) in enumerate(((960, 250, 1.0), (1500 + 200 * smooth(((t - t0) % 1.6) / 1.0), 640, 1.0))):
        p.rect(x - 200, y - 110, x + 200, y + 110, (0.97, 0.97, 0.94), op)
        pts = [(x - 150 + i * 9, y + 25 * math.sin(i * 0.55) - (i % 7) * 3) for i in range(34)]
        p.polilinea(pts, 5, (0.10, 0.12, 0.35), op)
    p.texto("COPIA", 1700, 800, 46, ROJO, "sans_b", smooth(((t - t0) % 1.6 - 0.8) / 0.3))


@portal("tribunal")
def tribunal(p, t):
    """Sala del Tribunal Superior de Londres (ilustración): estrado, juez, mazo que cae."""
    t0 = ww("wright", 8, "tajante")
    p.fondo((0.20, 0.13, 0.08), (0.08, 0.05, 0.03))
    for x in range(0, W, 180):
        p.rect(x, 0, x + 170, 560, (0.30, 0.19, 0.11))
        p.rect(x + 12, 20, x + 158, 540, (0.26, 0.16, 0.09))
    p.circ(960, 170, 90, (0.75, 0.62, 0.30))
    p.circ(960, 170, 70, (0.55, 0.40, 0.18))
    persona(p, 960, 700, 440, pose_sentado(t), (0.05, 0.04, 0.04), 1, ropa="chaqueta")
    p.rect(360, 560, 1560, 820, (0.36, 0.22, 0.12))
    p.rect(360, 540, 1560, 580, (0.45, 0.29, 0.16))
    p.texto("TRIBUNAL SUPERIOR · LONDRES", 960, 690, 40, (0.85, 0.72, 0.45), "serif", 0.9)
    p.rect(860, 360, 1060, 380, (0.92, 0.92, 0.88), 0.0)
    u = clamp((t - t0) / 0.35)
    mazo(p, 1280, 520, 1.7, u)
    if t > t0 + 0.35:
        onda_choque(p, 1300, 540, clamp((t - t0 - 0.35) / 0.6), 300, LUZ, 0.6)
    multitud(p, 10, 60, 1860, 1150, 280, (0.03, 0.02, 0.02), t, 9)


# ================================================================================================ TODD
@portal("tele")
def tele(p, t):
    """Un televisor viejo: estática, y luego un documental con una silueta y un signo de interrogación."""
    t0 = INI("todd", 1)
    p.fondo((0.05, 0.04, 0.05), (0.02, 0.02, 0.02))
    p.rrect(330, 120, 1590, 900, 60, (0.18, 0.14, 0.11))
    p.rrect(400, 180, 1420, 840, 40, (0.02, 0.02, 0.02))
    u = smooth((t - t0 - 0.8) / 0.5)
    if u < 1:
        rng = np.random.default_rng(int(t * 30))
        n = rng.random((33, 51)).astype(np.float32)
        n = cv2.resize(n, (int(1020 * K), int(660 * K)), interpolation=cv2.INTER_NEAREST)
        y0, x0 = int(180 * K), int(400 * K)
        p.im[y0:y0 + n.shape[0], x0:x0 + n.shape[1]] = n[..., None] * (1 - u) * 0.8
    if u > 0:
        p.rect(400, 180, 1420, 840, (0.05, 0.08, 0.12), u)
        persona(p, 900, 840, 520, pose_estar(t), (0.0, 0.0, 0.0), 1, alpha=u)
        p.texto("?", 1180, 460, 300, (0.9, 0.15, 0.12), "serif", u)
    for k in range(2):
        p.circ(1500, 360 + k * 160, 40, (0.35, 0.30, 0.25))
    p.linea((700, 120), (560, -40), 6, (0.4, 0.4, 0.4))
    p.linea((1000, 120), (1180, -40), 6, (0.4, 0.4, 0.4))


@portal("foro_hora")
def foro_hora(p, t):
    """Esquema: un mensaje de Satoshi y, una hora después, la corrección de un recién llegado."""
    t0 = ww("todd", 2, "corrigio")
    p.fondo((0.88, 0.89, 0.92), (0.80, 0.82, 0.86))
    t_ini = INI("todd", 2)
    for k, (x, y, quien, col, ta) in enumerate(((200, 170, "Satoshi", (0.20, 0.35, 0.60), t_ini + 0.3), (360, 600, "recién llegado", (0.55, 0.20, 0.15), t0))):
        u = smooth((t - ta) / 0.4)
        p.rect(x, y, x + 1300, y + 330, (1, 1, 1), u)
        p.rect(x, y, x + 1300, y + 64, col, u)
        p.texto(quien, x + 30, y + 32, 40, (1, 1, 1), "sans_b", u, "lm")
        for j in range(4):
            p.rect(x + 40, y + 110 + j * 48, x + 40 + (1100 if j < 3 else 600), y + 130 + j * 48, (0.70, 0.72, 0.76), u)
    ur = smooth((t - t0 - 0.2) / 1.2)
    reloj(p, 1680, 520, 150, 0, 12 + ur, (ur * 60) % 60, False)
    p.texto("+1 HORA", 1680, 730, 56, ROJO, "sans_b", smooth((t - t0 - 1.2) / 0.4))
    p.texto("ESQUEMA", 1760, 1040, 30, (0.4, 0.4, 0.45), "sans", 0.8)


@portal("homenaje")
def homenaje(p, t):
    """Un bloque de la cadena con un homenaje grabado que brilla (ilustración)."""
    t0 = INI("todd", 8)
    fondo_noche(p, t, (0.02, 0.02, 0.04), (0.04, 0.05, 0.08))
    x, y, s = 960, 520, 520
    col = (0.30, 0.42, 0.62)
    p.poly([(x - s / 2, y - s * 0.3), (x, y - s * 0.55), (x + s / 2, y - s * 0.3), (x, y - s * 0.05)], mix(col, (1, 1, 1), 0.35))
    p.poly([(x - s / 2, y - s * 0.3), (x, y - s * 0.05), (x, y + s * 0.5), (x - s / 2, y + s * 0.25)], col)
    p.poly([(x + s / 2, y - s * 0.3), (x, y - s * 0.05), (x, y + s * 0.5), (x + s / 2, y + s * 0.25)], mix(col, (0, 0, 0), 0.35))
    u = smooth((t - t0 - 0.3) / 1.2)
    p.glow(x - s * 0.25, y + s * 0.1, 260, (1.0, 0.9, 0.6), 0.5 * u)
    p.texto("LEN", x - s * 0.25, y + s * 0.02, 54, (1.0, 0.95, 0.8), "serif", u)
    p.texto("SASSAMAN", x - s * 0.25, y + s * 0.13, 40, (1.0, 0.95, 0.8), "serif", u)
    p.texto("1980–2011", x - s * 0.25, y + s * 0.24, 34, (1.0, 0.95, 0.8), "mono", u)
    for k in range(5):
        xx = x - 900 + k * 420
        if abs(xx - x) > 200:
            p.rect(xx - 70, y - 50, xx + 70, y + 90, (0.22, 0.30, 0.45), 0.7)
    p.texto("ILUSTRACIÓN", 960, 1040, 26, (0.6, 0.7, 0.8), "sans", 0.7)


# ================================================================================================ BACK
@portal("hashcash")
def hashcash(p, t):
    """Hashcash (1997): un correo solo pasa si lleva pegado un sello de trabajo de cómputo (el hash gira hasta dar con los ceros)."""
    t0 = ww("back", 1, "invento")
    fondo_noche(p, t, (0.03, 0.04, 0.07), (0.07, 0.08, 0.12))
    sobre(p, 640, 470, 560, CREMA, 1.0, -0.06)
    rng = np.random.default_rng(int(t * 12))
    u = clamp((t - t0) / 2.4)
    hx = "".join("0123456789abcdef"[rng.integers(0, 16)] for _ in range(12))
    if u >= 1:
        hx = "00000" + "3f9a1c2"
    p.rrect(1150, 380, 1760, 520, 16, (0.05, 0.08, 0.06))
    p.texto(hx, 1455, 450, 56, (0.4, 1.0, 0.6) if u >= 1 else (0.7, 0.9, 0.75), "mono")
    p.texto("prueba de trabajo", 1455, 580, 46, (0.9, 0.9, 0.9), "sans")
    if u >= 1:
        p.rrect(780, 380, 940, 520, 10, (0.85, 0.20, 0.15))
        check(p, 860, 450, 46, 1.0, (1, 1, 1), 14)
    p.texto("HASHCASH · 1997", 960, 900, 76, NARANJA, "abril", smooth((t - t0) / 0.5))


@portal("ia")
def ia(p, t):
    """Miles de mensajes de listas de correo que un haz analiza; barras de parecido por candidato (ESQUEMA)."""
    t0 = INI("back", 5)
    p.fondo((0.02, 0.03, 0.05), (0.04, 0.05, 0.08))
    rng = np.random.default_rng(2)
    for i in range(240):
        x = (i % 24) * 80 + 20
        y = (i // 24) * 56 + 40
        p.rect(x, y, x + 64, y + 40, (0.75, 0.78, 0.85), 0.25)
        p.rect(x + 6, y + 8, x + 50, y + 12, (0.3, 0.3, 0.35), 0.3)
    s = ((t - t0) * 0.4) % 1.0
    p.rect(0, s * 600, W, s * 600 + 26, (0.4, 0.9, 1.0), 0.35)
    p.glow(960, s * 600 + 13, 600, (0.4, 0.9, 1.0), 0.15)
    p.rect(0, 620, W, H, (0.03, 0.04, 0.06))
    noms = ["A", "B", "C", "D", "BACK", "E", "F"]
    vals = [0.42, 0.35, 0.55, 0.30, 0.92, 0.48, 0.38]
    u = smooth((t - t0 - 1.0) / 1.5)
    for k, (n_, v) in enumerate(zip(noms, vals)):
        x = 330 + k * 200
        hb = 340 * v * u
        col = (0.95, 0.60, 0.12) if n_ == "BACK" else (0.35, 0.45, 0.62)
        p.rect(x - 60, 1010 - hb, x + 60, 1010, col)
        p.texto(n_, x, 1045, 34, (0.9, 0.9, 0.9), "sans_b")
    p.texto("ESQUEMA · parecido de estilo con Satoshi", 1580, 680, 30, (0.6, 0.7, 0.8), "sans")


@portal("el_salvador")
def el_salvador(p, t):
    """Una conferencia en El Salvador: dos siluetas frente a frente; los «no» se acumulan."""
    t0 = INI("back", 8)
    p.fondo((0.05, 0.03, 0.08), (0.10, 0.06, 0.06))
    for k in range(6):
        x = 160 + k * 320
        p.haz(x, -20, 90 + 15 * math.sin(t * 0.7 + k), 900, 14, [(0.95, 0.6, 0.15), (0.3, 0.5, 1.0)][k % 2], 0.18)
    p.rect(0, 860, W, H, (0.04, 0.03, 0.04))
    p.glow(960, 640, 700, (0.55, 0.40, 0.70), 0.22)
    persona(p, 700, 900, 460, pose_señalar(0.6), (0.10, 0.08, 0.13), 1)
    persona(p, 1220, 900, 470, pose_estar(t), (0.10, 0.08, 0.13), -1, ropa="chaqueta")
    n = int(clamp((t - t0 - 0.5) / 3.0) * 7)
    for k in range(n):
        x = 1250 + (k % 3) * 190 - 60
        y = 200 + (k // 3) * 130
        p.rrect(x - 80, y - 46, x + 80, y + 46, 20, (1, 1, 1), 0.92)
        p.texto("NO", x, y, 54, (0.85, 0.08, 0.08), "sans_b")
    p.texto(f"{n}", 300, 220, 140, (1, 0.8, 0.3), "abril", 1.0 if n else 0.0)


# ================================================================================================ CIERRE
@portal("estatua")
def estatua(p, t):
    """Foto real de la estatua de Satoshi en Lugano (Valentina Picozzi, CC BY-SA 4.0): de frente, la figura casi desaparece."""
    t0 = INI("cierre", 5)
    foto_fondo(p, "estatua_lugano", t, 1.02, 1.18, 6.0, t0, 0.5, 0.42, (0.95, 0.97, 1.0), 0.85)


# ================================================================================================ LE ROUX / ARCHIVO / ESPEJO
@portal("carcel")
def carcel(p, t):
    """Una prisión de noche con reflector; en primer plano, una bóveda con monedas cubiertas de polvo (ilustración)."""
    t0 = INI("leroux", 3)
    fondo_noche(p, t, (0.015, 0.02, 0.04), (0.05, 0.06, 0.09))
    suelo(p, 780, (0.04, 0.045, 0.06), (0.01, 0.012, 0.02))
    prision(p, 1280, 780, 950, t, (0.06, 0.07, 0.09), True, True, True)
    p.rrect(140, 560, 700, 1000, 20, (0.10, 0.10, 0.12))
    p.rrect(170, 590, 670, 970, 14, (0.03, 0.03, 0.04))
    rng = np.random.default_rng(3)
    for i in range(70):
        uu = rng.random()
        moneda(p, 420 + (rng.random() - 0.5) * 420 * (1 - uu * 0.6), 950 - uu * 260, 24, 0.85, rng.random() * 0.3)
    polvo(p, t, 30, 5, 0.35, (0.8, 0.8, 0.8), 6)
    p.texto("ILUSTRACIÓN", 960, 1040, 26, (0.6, 0.7, 0.8), "sans", 0.7)


@portal("archivo")
def archivo(p, t):
    """Un archivo del gobierno: filas de archivadores, un cajón que se abre, una carpeta con un signo de interrogación (ilustración)."""
    t0 = INI("archivo", 0)
    p.fondo((0.05, 0.06, 0.07), (0.02, 0.02, 0.03))
    p.haz(960, -60, 90, 1200, 34, (0.85, 0.92, 1.0), 0.18)
    for fila in range(2):
        for k in range(7):
            x = 120 + k * 260 - fila * 60
            y = 330 + fila * 260
            col = (0.30, 0.33, 0.36) if fila else (0.22, 0.24, 0.27)
            p.rect(x, y - 240, x + 220, y + 260, col)
            for c in range(4):
                p.rect(x + 14, y - 225 + c * 120, x + 206, y - 125 + c * 120, mix(col, (0, 0, 0), 0.25))
                p.rect(x + 90, y - 185 + c * 120, x + 130, y - 172 + c * 120, (0.7, 0.7, 0.72))
    u = smooth((t - t0 - 0.6) / 1.2)
    x, y = 960, 640
    p.rect(x - 160, y, x + 160, y + 40 + 220 * u, (0.36, 0.38, 0.40))
    p.rect(x - 150, y + 10, x + 150, y + 30 + 220 * u, (0.12, 0.12, 0.13))
    if u > 0.6:
        uu = smooth((u - 0.6) / 0.4)
        p.rect(x - 120, y - 120 * uu, x + 120, y + 60, (0.82, 0.70, 0.45), uu)
        p.rect(x - 120, y - 140 * uu, x - 20, y - 110 * uu, (0.82, 0.70, 0.45), uu)
        p.texto("?", x, y - 40 * uu, 120, (0.75, 0.12, 0.10), "serif", uu)
        p.glow(x, y - 40, 260, (1.0, 0.9, 0.7), 0.25 * uu)
    p.texto("ILUSTRACIÓN", 960, 1040, 26, (0.6, 0.7, 0.8), "sans", 0.7)


@portal("busto")
def busto(p, t):
    """Foto real del busto de Satoshi en Budapest (Fekist, CC BY-SA 4.0): un brillo recorre la cara de metal pulido."""
    t0 = INI("espejo", 0)
    foto_fondo(p, "busto_budapest", t, 1.05, 1.25, 7.0, t0, 0.5, 0.33, (1.0, 1.0, 1.0), 0.9)
    s = ((t - t0) * 0.35) % 1.4 - 0.2
    x = 760 + s * 420
    p.poly([(x - 30, 140), (x + 40, 140), (x - 60, 560), (x - 130, 560)], (1.0, 1.0, 0.95), 0.18)
    p.glow(x - 30, 330, 150, (1.0, 1.0, 0.95), 0.22)
