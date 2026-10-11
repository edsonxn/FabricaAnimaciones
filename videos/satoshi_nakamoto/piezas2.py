# -*- coding: utf-8 -*-
"""Más piezas del tablero: iconos tachables, revista GENÉRICA, firma REAL del bloque 170, rejilla de direcciones, casillas, esquemas
(rotulados como esquema), bandera, mensajes REALES de Satoshi, gráfica de horas animada (datos propios)."""
import base64 as b64
import functools
import json
import math
import os
import re

import numpy as np
from PIL import Image, ImageDraw

import tablero as T
from piezas import _pil, _np, AQUI


def _lienzo(w, h, color=(0.97, 0.96, 0.92), seed=0, env=0.3):
    img, a = T._papel(w, h, color, seed, env)
    return _pil(img), a


def _fin(pil, a, sr=9):
    return T.Lam(T._a_rgba(_np(pil), a), sr=sr)


def c01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


@functools.lru_cache(maxsize=16)
def icono_card(tipo, lado=300, seed=20):
    """Tarjeta con un icono a tinta: telefono, camara, reunion, llave, sobre, documento, testigo."""
    pil, a = _lienzo(lado, lado, (0.96, 0.95, 0.90), seed)
    d = ImageDraw.Draw(pil)
    c = lado / 2
    k = lado / 300
    tinta = (30, 30, 38)
    w = int(9 * k)
    if tipo == "telefono":
        d.rounded_rectangle([c - 55 * k, c - 95 * k, c + 55 * k, c + 95 * k], 18 * k, outline=tinta, width=w)
        d.line([(c - 20 * k, c + 70 * k), (c + 20 * k, c + 70 * k)], fill=tinta, width=w)
    elif tipo == "camara":
        d.rounded_rectangle([c - 100 * k, c - 55 * k, c + 100 * k, c + 70 * k], 14 * k, outline=tinta, width=w)
        d.ellipse([c - 42 * k, c - 35 * k, c + 42 * k, c + 49 * k], outline=tinta, width=w)
        d.rectangle([c - 70 * k, c - 80 * k, c - 25 * k, c - 55 * k], outline=tinta, width=w)
    elif tipo == "reunion":
        for dx in (-50, 50):
            d.ellipse([c + dx * k - 26 * k, c - 90 * k, c + dx * k + 26 * k, c - 38 * k], outline=tinta, width=w)
            d.arc([c + dx * k - 55 * k, c - 25 * k, c + dx * k + 55 * k, c + 90 * k], 180, 360, fill=tinta, width=w)
        d.line([(c - 50 * k, c + 40 * k), (c + 50 * k, c + 40 * k)], fill=tinta, width=w)
    elif tipo == "llave":
        d.ellipse([c - 105 * k, c - 45 * k, c - 15 * k, c + 45 * k], outline=tinta, width=w)
        d.line([(c - 15 * k, c), (c + 105 * k, c)], fill=tinta, width=w)
        for xx in (60, 90):
            d.line([(c + xx * k, c), (c + xx * k, c + 30 * k)], fill=tinta, width=w)
    elif tipo == "sobre":
        d.rectangle([c - 100 * k, c - 60 * k, c + 100 * k, c + 65 * k], outline=tinta, width=w)
        d.line([(c - 100 * k, c - 60 * k), (c, c + 10 * k), (c + 100 * k, c - 60 * k)], fill=tinta, width=w)
    elif tipo == "documento":
        d.rectangle([c - 70 * k, c - 95 * k, c + 70 * k, c + 95 * k], outline=tinta, width=w)
        for yy in (-50, -15, 20, 55):
            d.line([(c - 45 * k, c + yy * k), (c + 45 * k, c + yy * k)], fill=tinta, width=int(6 * k))
    elif tipo == "testigo":
        d.ellipse([c - 30 * k, c - 95 * k, c + 30 * k, c - 35 * k], outline=tinta, width=w)
        d.arc([c - 70 * k, c - 20 * k, c + 70 * k, c + 120 * k], 180, 360, fill=tinta, width=w)
    return _fin(pil, a, 7)


@functools.lru_cache(maxsize=4)
def revista(seed=21, ancho=560):
    """Revista GENÉRICA (no imita ninguna portada real): banda roja, silueta y signo; rotulada como ilustración."""
    alto = int(ancho * 1.33)
    img, a = T._papel(ancho, alto, (0.92, 0.92, 0.94), seed, 0.2)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    d.rectangle([0, 0, ancho, alto * 0.13], fill=(180, 30, 35))
    d.text((ancho / 2, alto * 0.065), "REVISTA · 6 MAR 2014", font=T.fnt("oswald", int(ancho * 0.075)), fill=(250, 245, 240), anchor="mm")
    d.rectangle([ancho * 0.08, alto * 0.18, ancho * 0.92, alto * 0.80], fill=(52, 56, 66))
    d.ellipse([ancho * 0.36, alto * 0.28, ancho * 0.64, alto * 0.50], fill=(18, 20, 26))
    d.chord([ancho * 0.18, alto * 0.50, ancho * 0.82, alto * 0.98], 180, 360, fill=(18, 20, 26))
    d.rectangle([ancho * 0.08, alto * 0.80, ancho * 0.92, alto * 0.98], fill=(235, 235, 238))
    d.text((ancho / 2, alto * 0.39), "?", font=T.fnt("serif", int(ancho * 0.16)), fill=(210, 40, 40), anchor="mm")
    T._texto_en(pil, (ancho * 0.08, alto * 0.83), "«ENCONTRAMOS A SATOSHI»", "oswald", int(ancho * 0.07), (0.1, 0.1, 0.12), ancho * 0.84)
    d.text((ancho - 14, alto - 10), "ilustración", font=T.fnt("courier", 16), fill=(120, 120, 125), anchor="rs")
    return _fin(pil, a, 11)


FIRMA_HEX = ("304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac46"
             "22082221a8768d1d09")


@functools.lru_cache(maxsize=4)
def hoja_firma(titulo, sub, seed=22, ancho=640, base64=False):
    """Firma REAL de la transacción del bloque 170 (2009): en hex (como en la cadena) o en base64 (como apareció en 2016)."""
    txt = FIRMA_HEX if not base64 else b64.b64encode(bytes.fromhex(FIRMA_HEX)).decode()
    alto = int(ancho * 0.62)
    pil, a = _lienzo(ancho, alto, (0.97, 0.97, 0.95), seed)
    d = ImageDraw.Draw(pil)
    d.text((24, 20), titulo, font=T.fnt("courier_b", 28), fill=(40, 40, 50))
    d.text((24, 58), sub, font=T.fnt("courier", 20), fill=(110, 110, 120))
    f = T.fnt("courier", 23)
    y = 110
    n = 36
    for i in range(0, len(txt), n):
        d.text((24, y), txt[i:i + n], font=f, fill=(35, 35, 45))
        y += 31
    return _fin(pil, a)


@functools.lru_cache(maxsize=2)
def rejilla_direcciones(ancho=760, alto=560, seed=23):
    """Hoja con cientos de candados diminutos: representación de las ~22.000 direcciones atribuidas a Satoshi."""
    pil, a = _lienzo(ancho, alto, (0.97, 0.96, 0.92), seed)
    d = ImageDraw.Draw(pil)
    d.text((24, 18), "≈ 22.000 DIRECCIONES · 0 MOVIMIENTOS", font=T.fnt("courier_b", 26), fill=(40, 40, 50))
    for yy in range(70, alto - 40, 22):
        for xx in range(24, ancho - 24, 20):
            d.rectangle([xx, yy + 6, xx + 12, yy + 16], fill=(150, 110, 40))
            d.arc([xx + 2, yy, xx + 10, yy + 12], 180, 360, fill=(110, 110, 110), width=2)
    d.text((ancho - 20, alto - 12), "representación · estimación de Arkham", font=T.fnt("courier", 16), fill=(110, 110, 120), anchor="rs")
    return _fin(pil, a)


@functools.lru_cache(maxsize=8)
def casillas(titulo, items, ancho=600, seed=24, px=36):
    """Lista con casillas vacías."""
    f = T.fnt("maquina", px)
    n_lin = [max(1, int(f.getlength(it) // (ancho - 90 - px)) + 1) for it in items]
    alto = int(110 + sum(n * px * 1.05 + px * 0.9 for n in n_lin))
    pil, a = _lienzo(ancho, alto, (0.97, 0.96, 0.92), seed)
    d = ImageDraw.Draw(pil)
    d.text((28, 22), titulo, font=T.fnt("courier_b", int(px * 0.95)), fill=(150, 20, 20))
    y = 90
    for it, n in zip(items, n_lin):
        d.rectangle([30, y, 30 + px, y + px], outline=(30, 30, 38), width=4)
        T._texto_en(pil, (30 + px * 1.6, y - 2), it, "maquina", px, (0.1, 0.1, 0.12), ancho - 90 - px, 1.05)
        y += n * px * 1.05 + px * 0.9
    return _fin(pil, a)


@functools.lru_cache(maxsize=2)
def esquema_patoshi(ancho=760, alto=520, seed=25):
    """Esquema ilustrativo del patrón «Patoshi»: franjas diagonales de puntos (NO son los datos reales; va rotulado)."""
    pil, a = _lienzo(ancho, alto, (0.97, 0.97, 0.95), seed)
    d = ImageDraw.Draw(pil)
    d.text((24, 18), "PATRÓN «PATOSHI» · ESQUEMA", font=T.fnt("courier_b", 26), fill=(40, 40, 50))
    x0, y0, x1, y1 = 60, 70, ancho - 30, alto - 60
    d.line([(x0, y1), (x1, y1)], fill=(40, 40, 50), width=2)
    d.line([(x0, y0), (x0, y1)], fill=(40, 40, 50), width=2)
    rng = np.random.default_rng(seed)
    for j in range(260):
        x, y = x0 + rng.random() * (x1 - x0), y1 - rng.random() * (y1 - y0) * 0.35
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(90, 110, 150))
    for k in range(9):
        xs = x0 + (k + rng.random() * 0.3) * (x1 - x0) / 9.5
        for j in range(40):
            u = j / 40
            d.ellipse([xs + u * 50 - 3, y1 - u * (y1 - y0) * 0.9 - 3, xs + u * 50 + 3, y1 - u * (y1 - y0) * 0.9 + 3], fill=(200, 110, 20))
    d.text((x1, y1 + 30), "bloques 2009-2010", font=T.fnt("courier", 18), fill=(90, 90, 100), anchor="rm")
    return _fin(pil, a)


@functools.lru_cache(maxsize=2)
def esquema_actividad(ancho=760, alto=480, seed=26):
    """Esquema (según lo que describe el NYT): actividad de Back en listas, baja mientras Satoshi estaba activo."""
    pil, a = _lienzo(ancho, alto, (0.97, 0.97, 0.95), seed)
    d = ImageDraw.Draw(pil)
    d.text((24, 18), "MENSAJES DE BACK EN LISTAS · ESQUEMA", font=T.fnt("courier_b", 24), fill=(40, 40, 50))
    x0, y0, x1, y1 = 60, 80, ancho - 30, alto - 70
    d.rectangle([x0 + (x1 - x0) * 0.42, y0, x0 + (x1 - x0) * 0.68, y1], fill=(240, 228, 200))
    d.text((x0 + (x1 - x0) * 0.55, y0 + 14), "Satoshi activo", font=T.fnt("courier", 18), fill=(150, 90, 20), anchor="ma")
    pts = []
    for i in range(41):
        u = i / 40
        v = 0.65 + 0.1 * math.sin(i * 1.3)
        if 0.42 < u < 0.68:
            v = 0.15 + 0.05 * math.sin(i)
        elif u >= 0.68:
            v = 0.55 + 0.12 * math.sin(i * 0.9)
        pts.append((x0 + u * (x1 - x0), y1 - v * (y1 - y0)))
    d.line(pts, fill=(40, 70, 130), width=5)
    d.line([(x0, y1), (x1, y1)], fill=(40, 40, 50), width=2)
    for k, an in enumerate(("2004", "2008", "2011", "2014")):
        d.text((x0 + (0.10 + k * 0.29) * (x1 - x0), y1 + 12), an, font=T.fnt("courier", 18), fill=(80, 80, 90), anchor="ma")
    return _fin(pil, a)


@functools.lru_cache(maxsize=2)
def bandera_uk(ancho=360, seed=27):
    alto = int(ancho * 0.55)
    pil = Image.new("RGB", (ancho, alto), (20, 40, 110))
    d = ImageDraw.Draw(pil)
    for wv, col in ((int(alto * 0.20), (245, 245, 245)), (int(alto * 0.08), (200, 25, 40))):
        d.line([(0, 0), (ancho, alto)], fill=col, width=wv)
        d.line([(0, alto), (ancho, 0)], fill=col, width=wv)
    d.rectangle([ancho * 0.42, 0, ancho * 0.58, alto], fill=(245, 245, 245))
    d.rectangle([0, alto * 0.36, ancho, alto * 0.64], fill=(245, 245, 245))
    d.rectangle([ancho * 0.45, 0, ancho * 0.55, alto], fill=(200, 25, 40))
    d.rectangle([0, alto * 0.41, ancho, alto * 0.59], fill=(200, 25, 40))
    img = _np(pil) * T._papel(ancho, alto, (1, 1, 1), seed, 0.3)[0]
    return T.Lam(T._a_rgba(img, np.ones((alto, ancho), np.float32)), sr=7)


@functools.lru_cache(maxsize=8)
def post_real(i0, n=3, ancho=760, seed=28):
    """Impresión de mensajes REALES de Satoshi en foros (archivo del Satoshi Nakamoto Institute)."""
    d_ = json.load(open(os.path.join(AQUI, "datos", "forum_posts.json"), encoding="utf-8"))
    sat = [p for p in d_ if p.get("satoshi_id")]
    alto = int(80 + n * 230)
    pil, a = _lienzo(ancho, alto, (0.97, 0.97, 0.95), seed)
    d = ImageDraw.Draw(pil)
    d.text((24, 18), "Satoshi Nakamoto · mensajes en foros", font=T.fnt("courier_b", 24), fill=(40, 40, 50))
    y = 64
    for p in sat[i0:i0 + n]:
        tx = re.sub(r"<[^>]+>", " ", p["text"])
        tx = re.sub(r"\s+", " ", tx).strip()[:250]
        d.text((24, y), f"{p['date'][:16].replace('T', ' ')} UTC · {p.get('subject', '')[:40]}", font=T.fnt("courier_b", 19), fill=(60, 80, 120))
        T._texto_en(pil, (24, y + 30), tx, "courier", 19, (0.12, 0.12, 0.14), ancho - 48, 1.25)
        y += 230
    return _fin(pil, a)


_HORAS = json.load(open(os.path.join(AQUI, "datos", "horas_utc.json")))


def grafica_horas_viva(u):
    """Contenido animado de la gráfica de horas (barras que crecen hasta u=1). float32 (470, 820, 3)."""
    hs = _HORAS["horas"]
    w, h = 820, 470
    pil = Image.new("RGB", (w, h), (247, 247, 242))
    d = ImageDraw.Draw(pil)
    x0, y0, x1, y1 = 40, 20, w - 20, h - 50
    d.rectangle([x0 + (x1 - x0) * 5 / 24, y0, x0 + (x1 - x0) * 12 / 24, y1], fill=(240, 222, 222))
    mx = max(hs)
    bw = (x1 - x0) / 24
    for k, v in enumerate(hs):
        uu = c01(u * 1.4 - k / 24 * 0.4)
        bh = (y1 - y0) * v / mx * uu
        if bh > 0.5:
            d.rectangle([x0 + k * bw + 3, y1 - bh, x0 + (k + 1) * bw - 3, y1], fill=(40, 70, 120) if not 5 <= k < 12 else (190, 40, 40))
        if k % 3 == 0:
            d.text((x0 + k * bw + bw / 2, y1 + 10), f"{k:02d}h", font=T.fnt("courier", 19), fill=(60, 60, 70), anchor="ma")
    d.line([(x0, y1), (x1, y1)], fill=(40, 40, 50), width=2)
    return _np(pil)


@functools.lru_cache(maxsize=2)
def marco_grafica(seed=29):
    """Papel de la gráfica con ventana transparente para la parte animada (devuelve Lam, ventana)."""
    ancho, alto = 900, 640
    pil, a = _lienzo(ancho, alto, (0.97, 0.97, 0.95), seed)
    d = ImageDraw.Draw(pil)
    d.text((30, 22), "MENSAJES DE SATOSHI POR HORA (UTC) · n = 543", font=T.fnt("courier_b", 25), fill=(40, 40, 50))
    d.text((ancho - 30, alto - 22), "Fuente: archivo del Satoshi Nakamoto Institute · análisis propio", font=T.fnt("courier", 16),
           fill=(90, 90, 100), anchor="rs")
    ven = (40, 80, 860, 550)
    a = a.copy()
    a[ven[1]:ven[3], ven[0]:ven[2]] = 0
    return _fin(pil, a, 10), ven
