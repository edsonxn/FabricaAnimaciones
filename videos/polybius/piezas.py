# -*- coding: utf-8 -*-
"""Fábrica de piezas del tablero de Polybius: calendarios, recortes GENÉRICOS (titular propio, sin cabecera de ningún diario real),
citas, iconos a tinta, tarjetas «NINGUNA», revista genérica, hojas con dibujos vectoriales y el RELLENO de fondo del corcho.
Nada imita un documento real concreto; lo real (fotos de Commons, capturas de dominio público) va como foto con su crédito."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

import tablero as T


def _pil(img):
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))


def _np(pil):
    return np.asarray(pil, np.float32) / 255.0


def _lienzo(w, h, color=(0.97, 0.96, 0.92), seed=0, env=0.3):
    img, a = T._papel(w, h, color, seed, env)
    return _pil(img), a


def _fin(pil, a, sr=9):
    return T.Lam(T._a_rgba(_np(pil), a), sr=sr)


@functools.lru_cache(maxsize=16)
def calendario(mes, anio, marcar=(), ancho=380, seed=8):
    import calendar
    nombres = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    alto = int(ancho * 1.05)
    img, a = T._papel(ancho, alto, (0.97, 0.96, 0.93), seed, 0.3)
    img[: int(alto * 0.20)] *= np.float32([0.85, 0.25, 0.22]) / 0.97
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    d.text((ancho / 2, alto * 0.10), f"{nombres[mes - 1]} {anio}", font=T.fnt("oswald", int(ancho * 0.10)), fill=(250, 245, 235), anchor="mm")
    cal = calendar.monthcalendar(anio, mes)
    cw = (ancho - 30) / 7
    ch = (alto * 0.78) / max(6, len(cal) + 1)
    for j, dn in enumerate("LMXJVSD"):
        d.text((15 + cw * j + cw / 2, alto * 0.23), dn, font=T.fnt("courier_b", int(ch * 0.45)), fill=(120, 40, 40), anchor="ma")
    for i, sem in enumerate(cal):
        for j, dia in enumerate(sem):
            if dia:
                cx, cy = 15 + cw * j + cw / 2, alto * 0.23 + ch * (i + 1)
                d.text((cx, cy), str(dia), font=T.fnt("courier", int(ch * 0.5)), fill=(40, 40, 50), anchor="ma")
                if dia in marcar:
                    d.ellipse([cx - cw * 0.45, cy - ch * 0.18, cx + cw * 0.45, cy + ch * 0.68], outline=(200, 20, 20), width=4)
    return T.Lam(T._a_rgba(_np(pil), a), sr=8)


@functools.lru_cache(maxsize=16)
def anio_card(anio, ancho=420, seed=30, color=(0.97, 0.96, 0.93), sub=None):
    """Hoja de calendario de pared con solo el AÑO en grande."""
    alto = int(ancho * 0.80)
    img, a = T._papel(ancho, alto, color, seed, 0.3)
    img[: int(alto * 0.22)] *= np.float32([0.85, 0.25, 0.22]) / 0.97
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    for k in range(7):
        d.ellipse([ancho * (0.12 + 0.127 * k) - 9, alto * 0.05, ancho * (0.12 + 0.127 * k) + 9, alto * 0.05 + 18], fill=(40, 30, 30))
    d.text((ancho / 2, alto * 0.60), str(anio), font=T.fnt("serif", int(ancho * 0.36)), fill=(30, 28, 34), anchor="mm")
    if sub:
        d.text((ancho / 2, alto * 0.13), sub, font=T.fnt("oswald", int(ancho * 0.075)), fill=(250, 245, 235), anchor="mm")
    return T.Lam(T._a_rgba(_np(pil), a), sr=8)


@functools.lru_cache(maxsize=48)
def recorte(titular, ancho=520, seed=10, foto=False, px=40):
    """Recorte de papel de periódico GENÉRICO: titular propio + columnas ilegibles."""
    alto = int(ancho * (1.05 if foto else 0.78))
    img, a = T._papel(ancho, alto, (0.90, 0.88, 0.80), seed, 0.55, borde=7)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    y = T._texto_en(pil, (22, 22), titular, "serif", px, (0.08, 0.08, 0.08), ancho - 44, 1.05)
    rng = np.random.default_rng(seed)
    if foto:
        d.rectangle([22, y + 8, ancho - 22, y + 8 + alto * 0.36], fill=(90, 90, 92))
        y += alto * 0.36 + 18
    col = (ancho - 44 - 16) / 2
    for c in range(2):
        yy = y + 10
        while yy < alto - 22:
            w = col * (0.6 + 0.4 * rng.random()) if rng.random() < 0.15 else col
            d.line([(22 + c * (col + 16), yy), (22 + c * (col + 16) + w, yy)], fill=(120, 118, 112), width=4)
            yy += 13
    return T.Lam(T._a_rgba(_np(pil), a), sr=8)


@functools.lru_cache(maxsize=32)
def tarjeta_cita(txt, autor, ancho=640, px=36, seed=12):
    """Cita textual a máquina sobre papel."""
    alto = int(ancho * 0.52)
    img, a = T._papel(ancho, alto, (0.97, 0.96, 0.92), seed, 0.3)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    d.text((24, 6), "“", font=T.fnt("serif", 110), fill=(190, 40, 40))
    T._texto_en(pil, (104, 50), txt, "maquina", px, (0.10, 0.10, 0.12), ancho - 140, 1.15)
    d.text((ancho - 30, alto - 22), autor, font=T.fnt("courier", 22), fill=(90, 90, 100), anchor="rs")
    return T.Lam(T._a_rgba(_np(pil), a), sr=9)


@functools.lru_cache(maxsize=32)
def icono_card(tipo, lado=300, seed=20, pie=None):
    """Tarjeta con un icono a tinta: testigo, documento, tele, musica, mando, disquete, camara, placa, moneda, ojo."""
    pil, a = _lienzo(lado, lado + (60 if pie else 0), (0.96, 0.95, 0.90), seed)
    d = ImageDraw.Draw(pil)
    c = lado / 2
    k = lado / 300
    tinta = (30, 30, 38)
    w = int(9 * k)
    if tipo == "testigo":
        d.ellipse([c - 30 * k, c - 95 * k, c + 30 * k, c - 35 * k], outline=tinta, width=w)
        d.arc([c - 70 * k, c - 20 * k, c + 70 * k, c + 120 * k], 180, 360, fill=tinta, width=w)
    elif tipo == "documento":
        d.rectangle([c - 70 * k, c - 95 * k, c + 70 * k, c + 95 * k], outline=tinta, width=w)
        for yy in (-50, -15, 20, 55):
            d.line([(c - 45 * k, c + yy * k), (c + 45 * k, c + yy * k)], fill=tinta, width=int(6 * k))
    elif tipo == "tele":
        d.rounded_rectangle([c - 105 * k, c - 70 * k, c + 105 * k, c + 75 * k], 18 * k, outline=tinta, width=w)
        d.rounded_rectangle([c - 85 * k, c - 50 * k, c + 45 * k, c + 55 * k], 12 * k, outline=tinta, width=int(6 * k))
        for yy in (-30, 5, 40):
            d.ellipse([c + 62 * k, c + yy * k - 10 * k, c + 82 * k, c + yy * k + 10 * k], outline=tinta, width=int(5 * k))
        d.line([(c - 30 * k, c - 70 * k), (c - 70 * k, c - 115 * k)], fill=tinta, width=int(6 * k))
        d.line([(c + 10 * k, c - 70 * k), (c + 55 * k, c - 115 * k)], fill=tinta, width=int(6 * k))
    elif tipo == "musica":
        for dx in (-45, 55):
            d.ellipse([c + dx * k - 30 * k, c + 40 * k, c + dx * k + 16 * k, c + 80 * k], fill=tinta)
            d.line([(c + dx * k + 12 * k, c + 60 * k), (c + dx * k + 12 * k, c - 80 * k)], fill=tinta, width=w)
        d.line([(c - 33 * k, c - 80 * k), (c + 67 * k, c - 95 * k)], fill=tinta, width=int(16 * k))
    elif tipo == "mando":
        d.rounded_rectangle([c - 110 * k, c - 45 * k, c + 110 * k, c + 55 * k], 45 * k, outline=tinta, width=w)
        d.line([(c - 75 * k, c + 5 * k), (c - 35 * k, c + 5 * k)], fill=tinta, width=w)
        d.line([(c - 55 * k, c - 15 * k), (c - 55 * k, c + 25 * k)], fill=tinta, width=w)
        for dx, dy in ((45, 15), (75, -10)):
            d.ellipse([c + dx * k - 12 * k, c + dy * k - 12 * k, c + dx * k + 12 * k, c + dy * k + 12 * k], fill=tinta)
    elif tipo == "disquete":
        d.rectangle([c - 85 * k, c - 90 * k, c + 85 * k, c + 90 * k], outline=tinta, width=w)
        d.rectangle([c - 50 * k, c - 90 * k, c + 40 * k, c - 30 * k], outline=tinta, width=int(6 * k))
        d.rectangle([c - 60 * k, c + 10 * k, c + 60 * k, c + 90 * k], outline=tinta, width=int(6 * k))
    elif tipo == "camara":
        d.rounded_rectangle([c - 100 * k, c - 55 * k, c + 100 * k, c + 70 * k], 14 * k, outline=tinta, width=w)
        d.ellipse([c - 42 * k, c - 35 * k, c + 42 * k, c + 49 * k], outline=tinta, width=w)
        d.rectangle([c - 70 * k, c - 80 * k, c - 25 * k, c - 55 * k], outline=tinta, width=w)
    elif tipo == "placa":
        pts = [(c, c - 100 * k), (c + 80 * k, c - 60 * k), (c + 70 * k, c + 40 * k), (c, c + 100 * k), (c - 70 * k, c + 40 * k), (c - 80 * k, c - 60 * k)]
        d.line(pts + [pts[0]], fill=tinta, width=w, joint="curve")
        est = [(c + (48 if i % 2 == 0 else 20) * k * math.cos(-math.pi / 2 + i * math.pi / 5), c - 5 * k + (48 if i % 2 == 0 else 20) * k * math.sin(-math.pi / 2 + i * math.pi / 5))
               for i in range(10)]
        d.polygon(est, outline=tinta, width=int(5 * k))
    elif tipo == "moneda":
        d.ellipse([c - 85 * k, c - 85 * k, c + 85 * k, c + 85 * k], outline=tinta, width=w)
        d.text((c, c), "25¢", font=T.fnt("serif", int(70 * k)), fill=tinta, anchor="mm")
    elif tipo == "ojo":
        d.arc([c - 110 * k, c - 90 * k, c + 110 * k, c + 90 * k], 200, 340, fill=tinta, width=w)
        d.arc([c - 110 * k, c - 90 * k, c + 110 * k, c + 90 * k], 20, 160, fill=tinta, width=w)
        d.ellipse([c - 35 * k, c - 35 * k, c + 35 * k, c + 35 * k], outline=tinta, width=w)
        d.ellipse([c - 12 * k, c - 12 * k, c + 12 * k, c + 12 * k], fill=tinta)
    if pie:
        px = 34
        f = T.fnt("courier_b", px)
        while f.getlength(pie) > lado - 24 and px > 14:
            px -= 2
            f = T.fnt("courier_b", px)
        d.text((c, lado + 24), pie, font=f, fill=(140, 20, 20), anchor="mm")
    return _fin(pil, a, 7)


@functools.lru_cache(maxsize=16)
def vacia_card(titulo, ancho=400, seed=40):
    """Marco de foto VACÍO con esquineras: la prueba que debería existir y no existe."""
    alto = int(ancho * 1.12)
    pil, a = _lienzo(ancho, alto, (0.95, 0.94, 0.90), seed)
    d = ImageDraw.Draw(pil)
    b = int(ancho * 0.07)
    fh = int(ancho * 0.80)
    d.rectangle([b, b, ancho - b, b + fh], fill=(222, 218, 205))
    for k in range(b + 14, ancho - b - 10, 26):                       # contorno a trazos
        d.line([(k, b + 12), (k + 13, b + 12)], fill=(150, 145, 135), width=3)
        d.line([(k, b + fh - 12), (k + 13, b + fh - 12)], fill=(150, 145, 135), width=3)
    for k in range(b + 14, b + fh - 10, 26):
        d.line([(b + 12, k), (b + 12, k + 13)], fill=(150, 145, 135), width=3)
        d.line([(ancho - b - 12, k), (ancho - b - 12, k + 13)], fill=(150, 145, 135), width=3)
    for cx, cy in ((b, b), (ancho - b, b), (b, b + fh), (ancho - b, b + fh)):
        sx, sy = (1 if cx == b else -1), (1 if cy == b else -1)
        d.polygon([(cx, cy), (cx + sx * 46, cy), (cx, cy + sy * 46)], fill=(40, 38, 44))
    d.text((ancho / 2, b + fh / 2), "NINGUNA", font=T.fnt("courier_b", int(ancho * 0.11)), fill=(170, 40, 40), anchor="mm")
    px = 36
    f = T.fnt("marcador", px)
    while f.getlength(titulo) > ancho - 26 and px > 14:
        px -= 2
        f = T.fnt("marcador", px)
    d.text((ancho / 2, b + fh + (alto - b - fh) / 2), titulo, font=f, fill=(25, 22, 30), anchor="mm")
    return _fin(pil, a, 10)


@functools.lru_cache(maxsize=4)
def revista(titular="«SECRETOS Y MENTIRAS»", fecha="REVISTA DE VIDEOJUEGOS · SEP 2003", seed=21, ancho=520):
    """Revista GENÉRICA (no imita ninguna portada real): banda, cabina dibujada con «?» y titular; rotulada como ilustración."""
    alto = int(ancho * 1.33)
    img, a = T._papel(ancho, alto, (0.92, 0.92, 0.94), seed, 0.2)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    d.rectangle([0, 0, ancho, alto * 0.13], fill=(30, 60, 150))
    px = int(ancho * 0.062)
    d.text((ancho / 2, alto * 0.065), fecha, font=T.fnt("oswald", px), fill=(250, 245, 240), anchor="mm")
    d.rectangle([ancho * 0.08, alto * 0.18, ancho * 0.92, alto * 0.78], fill=(34, 28, 58))
    cx = ancho / 2
    d.polygon([(cx - 90, alto * 0.74), (cx + 90, alto * 0.74), (cx + 90, alto * 0.24), (cx - 90, alto * 0.24)], fill=(10, 10, 16))
    d.rectangle([cx - 66, alto * 0.30, cx + 66, alto * 0.46], fill=(60, 30, 110))
    d.text((cx, alto * 0.38), "?", font=T.fnt("serif", int(ancho * 0.16)), fill=(230, 60, 60), anchor="mm")
    d.rectangle([cx - 80, alto * 0.50, cx + 80, alto * 0.53], fill=(50, 50, 62))
    d.rectangle([ancho * 0.08, alto * 0.78, ancho * 0.92, alto * 0.98], fill=(235, 235, 238))
    T._texto_en(pil, (ancho * 0.11, alto * 0.81), titular, "oswald", int(ancho * 0.085), (0.1, 0.1, 0.12), ancho * 0.80)
    d.text((ancho - 14, alto - 10), "ilustración", font=T.fnt("courier", 16), fill=(120, 120, 125), anchor="rs")
    return T.Lam(T._a_rgba(_np(pil), a), sr=11)


@functools.lru_cache(maxsize=24)
def hoja_vector(seed=0, ancho=420, tipo=0):
    """Hoja con un dibujo vectorial a lápiz verde sobre papel cuadriculado (bocetos de formas geométricas, túneles, naves)."""
    alto = int(ancho * 0.9)
    img, a = T._papel(ancho, alto, (0.93, 0.95, 0.92), seed, 0.35)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    for k in range(0, ancho, 24):
        d.line([(k, 0), (k, alto)], fill=(196, 212, 204), width=1)
    for k in range(0, alto, 24):
        d.line([(0, k), (ancho, k)], fill=(196, 212, 204), width=1)
    cx, cy, R = ancho / 2, alto / 2, alto * 0.36
    tinta = (30, 90, 60)
    rng = np.random.default_rng(seed)
    if tipo % 3 == 0:
        for j, n in enumerate((6, 4, 3, 5)):
            r = R * (1 - j * 0.22)
            a0 = rng.random() * 6
            pts = [(cx + r * math.cos(a0 + 2 * math.pi * i / n), cy + r * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]
            d.line(pts + [pts[0]], fill=tinta, width=4)
    elif tipo % 3 == 1:
        n = 12
        ext = [(cx + R * 1.2 * math.cos(2 * math.pi * i / n), cy + R * math.sin(2 * math.pi * i / n)) for i in range(n)]
        inn = [(cx + R * 0.25 * math.cos(2 * math.pi * i / n), cy + R * 0.2 * math.sin(2 * math.pi * i / n) + R * 0.2) for i in range(n)]
        d.line(ext + [ext[0]], fill=tinta, width=4)
        d.line(inn + [inn[0]], fill=tinta, width=3)
        for i in range(n):
            d.line([ext[i], inn[i]], fill=tinta, width=2)
    else:
        for i in range(5):
            x, y, r = rng.random() * ancho * 0.7 + ancho * 0.15, rng.random() * alto * 0.6 + alto * 0.2, 18 + rng.random() * 30
            pts = [(x + r * (0.7 + 0.4 * rng.random()) * math.cos(2 * math.pi * j / 7), y + r * (0.7 + 0.4 * rng.random()) * math.sin(2 * math.pi * j / 7)) for j in range(7)]
            d.line(pts + [pts[0]], fill=tinta, width=3)
        d.polygon([(cx, cy - 22), (cx - 16, cy + 18), (cx + 16, cy + 18)], outline=tinta, width=4)
    return T.Lam(T._a_rgba(_np(pil), a), sr=8)


# =====================================================================================================================  RELLENO DE FONDO
NOTAS_FONDO = ["¿Portland?", "1981", "¿ROM?", "¿testigos?", "revisar prensa", "¿quién la vio?", "¿empresa?", "sin fotos", "¿FBI?", "Tempest", "28 h",
               "¿Atari?", "año 2000", "¿quién subió la ficha?", "¿alemán?", "sin registro", "¿cuántas?", "recreativos", "¿rumor?", "25¢"]
TITULARES_FONDO = ["LOS RECREATIVOS, LLENOS", "NUEVO RÉCORD DE PUNTOS", "MÁS MÁQUINAS EN EL CENTRO", "¿DEMASIADAS HORAS JUGANDO?", "SALÓN NUEVO EN LA AVENIDA",
                   "EL NEGOCIO DE LAS MONEDAS"]


def relleno(x0, x1, y0, y1, paso=480, seed=1, libres=()):
    """Llena una región del corcho con papeles de fondo (estáticos, ya clavados). `libres` = [(x, y, r)] zonas que se dejan despejadas."""
    rng = np.random.default_rng(seed)
    k = 0
    for gy in np.arange(y0, y1, paso * 0.86):
        for gx in np.arange(x0, x1, paso):
            x = gx + rng.uniform(-0.38, 0.38) * paso + (paso / 2 if int(gy / paso) % 2 else 0)
            y = gy + rng.uniform(-0.3, 0.3) * paso
            if any(math.hypot(x - lx, y - ly) < r for lx, ly, r in libres):
                continue
            tipo = rng.integers(0, 9)
            rot = rng.uniform(-9, 9)
            col = [(0.55, 0.52, 0.48), (0.80, 0.70, 0.20), (0.25, 0.45, 0.70), (0.70, 0.20, 0.20), (0.20, 0.55, 0.35)][rng.integers(0, 5)]
            s = rng.uniform(0.55, 0.85)
            if tipo == 0:
                L = hoja_vector(int(rng.integers(0, 8)), 420, int(rng.integers(0, 3)))
            elif tipo == 1:
                L = T.nota(NOTAS_FONDO[int(rng.integers(0, len(NOTAS_FONDO)))], 220, [(0.98, 0.86, 0.25), (0.95, 0.55, 0.60), (0.55, 0.85, 0.95),
                                                                                  (0.70, 0.92, 0.55)][rng.integers(0, 4)], 40, int(rng.integers(0, 40)))
                s = rng.uniform(0.75, 1.0)
            elif tipo == 2:
                L = recorte(TITULARES_FONDO[int(rng.integers(0, len(TITULARES_FONDO)))], 420, int(rng.integers(0, 12)), bool(rng.integers(0, 2)), 34)
            elif tipo == 3:
                L = T.ficha("", 420, 260, None, int(rng.integers(0, 12)))
            elif tipo == 4:
                L = calendario(int(rng.integers(1, 13)), int(rng.choice([1981, 1982, 2000, 2003])), (), 320, int(rng.integers(0, 6)))
            elif tipo == 5:
                L = icono_card(["moneda", "mando", "disquete", "ojo", "documento"][int(rng.integers(0, 5))], 240, int(rng.integers(0, 6)))
            elif tipo == 6:
                L = T.ficha(NOTAS_FONDO[int(rng.integers(0, len(NOTAS_FONDO)))], 400, 250, None, int(rng.integers(0, 12)), px=40, fuente="mano")
            elif tipo == 7:
                L = recorte("", 360, int(rng.integers(0, 12)), False)
            else:
                L = T.Lam(np.dstack([np.ones((300, 300, 3), np.float32) * np.float32([0.36, 0.22, 0.10]), _mancha_cafe(int(rng.integers(0, 8)))]), sr=0)
                s = rng.uniform(0.6, 1.1)
            L = T.oscura(L, 0.66)
            T.Pieza(L, x, y, rot, s, t_in=-10, entrada=None, chinchetas=((0, None, col),) if tipo != 8 else (), z=-1.0, capa=0, op=0.80,
                    sonido=False, flota=False)
            k += 1
    return k


@functools.lru_cache(maxsize=24)
def _mancha_cafe(seed):
    a = np.zeros((300, 300), np.float32)
    cv2.circle(a, (150, 150), 110, 1.0, 5, cv2.LINE_AA)
    return cv2.GaussianBlur(a, (0, 0), 2.5) * 0.35
