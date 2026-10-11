# -*- coding: utf-8 -*-
"""Fábrica de piezas del tablero (impresiones de código REAL de Bitcoin 0.1, volcado hexadecimal REAL del bloque génesis, gráfica con
datos propios, calendarios, mapa con Natural Earth, recortes) y el RELLENO de fondo del corcho (papeles viejos, notas, garabatos) para
que nunca se vea un corcho vacío. Nada imita un documento real concreto: lo real (código, hex, white paper, fotos) es real."""
import functools
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

import tablero as T

AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGO = open(os.path.join(AQUI, "datos", "v01_main.cpp"), encoding="utf-8", errors="ignore").read().split("\n")


def _pil(img):
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))


def _np(pil):
    return np.asarray(pil, np.float32) / 255.0


@functools.lru_cache(maxsize=32)
def impresion_codigo(l0, n=34, ancho=700, px=17, seed=0, resaltar=None, titulo="main.cpp — Bitcoin v0.1 (2009)"):
    """Hoja impresa con líneas REALES de src/main.cpp de Bitcoin 0.1 (licencia MIT). resaltar = índice de línea (relativo) a marcar."""
    lineas = [l.replace("\t", "    ") for l in CODIGO[l0:l0 + n]]
    alto = int(70 + n * px * 1.32 + 40)
    img, a = T._papel(ancho, alto, (0.97, 0.97, 0.95), seed, 0.35)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    f = T.fnt("courier", px)
    d.text((26, 22), titulo, font=T.fnt("courier_b", px + 1), fill=(60, 60, 70))
    d.line([(26, 52), (ancho - 26, 52)], fill=(160, 160, 165), width=1)
    y = 62
    for i, ln in enumerate(lineas):
        if resaltar is not None and i == resaltar:
            d.rectangle([22, y - 2, ancho - 18, y + px + 4], fill=(250, 236, 90))
        d.text((26, y), f"{l0 + i + 1:5d}  " + ln[:int((ancho - 100) / (px * 0.6))], font=f, fill=(35, 35, 45))
        y += px * 1.32
    return T.Lam(T._a_rgba(_np(pil), a), sr=9)


GENESIS_HEX = ("01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65"
               "732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062"
               "616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4c"
               "ef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000")


@functools.lru_cache(maxsize=8)
def impresion_hex(ancho=860, px=19, seed=6, resalte=0.0):
    """Volcado hexadecimal REAL de la transacción coinbase del bloque génesis (con su columna ASCII)."""
    b = bytes.fromhex(GENESIS_HEX)
    filas = [b[i:i + 16] for i in range(0, len(b), 16)]
    alto = int(80 + len(filas) * px * 1.45 + 40)
    img, a = T._papel(ancho, alto, (0.97, 0.97, 0.95), seed, 0.3)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    f = T.fnt("courier", px)
    d.text((24, 20), "BLOQUE 0 · transacción coinbase (hex)", font=T.fnt("courier_b", px + 2), fill=(60, 60, 70))
    y = 64
    for i, fl in enumerate(filas):
        hx = " ".join(f"{c:02x}" for c in fl)
        asc = "".join(chr(c) if 32 <= c < 127 else "." for c in fl)
        d.text((24, y), f"{i * 16:04x}  {hx:<47}  {asc}", font=f, fill=(40, 40, 50))
        y += px * 1.45
    return T.Lam(T._a_rgba(_np(pil), a), sr=9), filas


@functools.lru_cache(maxsize=4)
def grafica_horas(ancho=900, alto=620, seed=7):
    """Gráfica de barras con datos PROPIOS: mensajes de Satoshi en foros por hora UTC (datos/horas_utc.json)."""
    dat = json.load(open(os.path.join(AQUI, "datos", "horas_utc.json")))
    hs = dat["horas"]
    img, a = T._papel(ancho, alto, (0.97, 0.97, 0.95), seed, 0.3)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    d.text((30, 22), f"MENSAJES DE SATOSHI POR HORA (UTC) · n = {dat['n']}", font=T.fnt("courier_b", 24), fill=(40, 40, 50))
    x0, x1, y0, y1 = 70, ancho - 30, 90, alto - 70
    d.rectangle([x0 + (x1 - x0) * 5 / 24, y0, x0 + (x1 - x0) * 12 / 24, y1], fill=(238, 222, 222))
    mx = max(hs)
    bw = (x1 - x0) / 24
    for h, v in enumerate(hs):
        bh = (y1 - y0) * v / mx
        d.rectangle([x0 + h * bw + 3, y1 - bh, x0 + (h + 1) * bw - 3, y1], fill=(40, 70, 120) if not 5 <= h < 12 else (180, 40, 40))
        if h % 3 == 0:
            d.text((x0 + h * bw + bw / 2, y1 + 10), f"{h:02d}", font=T.fnt("courier", 20), fill=(60, 60, 70), anchor="ma")
    d.line([(x0, y1), (x1, y1)], fill=(40, 40, 50), width=2)
    d.text((ancho - 30, alto - 30), "Fuente: archivo del Satoshi Nakamoto Institute · análisis propio", font=T.fnt("courier", 16),
           fill=(90, 90, 100), anchor="rs")
    return T.Lam(T._a_rgba(_np(pil), a), sr=10), (x0, y0, x1, y1)


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


@functools.lru_cache(maxsize=4)
def _paises():
    return json.load(open(r"C:\FabricaAnimaciones\nucleo\datos\paises.json", encoding="utf-8"))


def proy_mundo(lon, lat, ancho, alto, caja=(-170, 80, 190, -60)):
    l0, la0, l1, la1 = caja
    return (lon - l0) / (l1 - l0) * ancho, (la0 - lat) / (la0 - la1) * alto


@functools.lru_cache(maxsize=4)
def mapa_mundo(ancho=1500, alto=820, seed=9, resaltar=()):
    """Mapa del mundo con costas reales (Natural Earth) impreso en papel, para husos horarios y lugares."""
    img, a = T._papel(ancho, alto, (0.90, 0.92, 0.90), seed, 0.35)
    img *= np.float32([0.86, 0.93, 0.98])
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    for nombre, polys in _paises().items():
        col = (205, 196, 170) if nombre not in resaltar else (226, 196, 120)
        for poly in polys:
            ring = poly[0] if isinstance(poly[0][0], list) else poly
            pts = [proy_mundo(lo, la, ancho, alto) for lo, la in ring]
            if len(pts) > 2:
                d.polygon(pts, fill=col, outline=(120, 110, 90))
    for k in range(-165, 195, 15):        # meridianos de husos
        x, _ = proy_mundo(k, 0, ancho, alto)
        d.line([(x, 0), (x, alto)], fill=(150, 170, 190), width=1)
    return T.Lam(T._a_rgba(_np(pil), a), sr=10)


@functools.lru_cache(maxsize=32)
def recorte(titular, ancho=520, seed=10, foto=False, px=40):
    """Recorte de papel de periódico GENÉRICO (sin cabecera de ningún diario real): titular propio + columnas ilegibles."""
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
def tarjeta_cita(txt, autor, ancho=640, px=36, seed=12, idioma_original=True):
    """Cita textual (traducción en grande + original en pequeño) a máquina sobre papel."""
    alto = int(ancho * 0.52)
    img, a = T._papel(ancho, alto, (0.97, 0.96, 0.92), seed, 0.3)
    pil = _pil(img)
    d = ImageDraw.Draw(pil)
    d.text((24, 6), "“", font=T.fnt("serif", 110), fill=(190, 40, 40))
    y = T._texto_en(pil, (70, 40), txt, "maquina", px, (0.10, 0.10, 0.12), ancho - 100, 1.15)
    pa = int(max(15, min(px * 0.6, 24)))
    f_a = T.fnt("courier", pa)
    lineas, cur = [], ""
    for w in autor.split(" "):
        pr_ = (cur + " " + w).strip()
        if f_a.getlength(pr_) > ancho - 60 and cur:
            lineas.append(cur)
            cur = w
        else:
            cur = pr_
    lineas.append(cur)
    yy = alto - 22 - (len(lineas) - 1) * pa * 1.2
    for ln in lineas:
        d.text((ancho - 30, yy), ln, font=f_a, fill=(90, 90, 100), anchor="rs")
        yy += pa * 1.2
    return T.Lam(T._a_rgba(_np(pil), a), sr=9)


# =====================================================================================================================  RELLENO DE FONDO
NOTAS_FONDO = ["¿Japón?", "GMT?", "¿equipo?", "revisar 2010", "¿llaves?", "bloque 0", "firma PGP", "¿Londres?", "¿quién?", "foros", "2 espacios",
               "¿por qué 2008?", "hora UTC", "correos", "¿1 o 2?", "cifrado", "¿cuántos?", "ver código", "¿alias?", "¿EE. UU.?"]


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
                L = impresion_codigo(int(rng.integers(30, 2500)), 22, 560, 15, int(rng.integers(0, 50)))
            elif tipo == 1:
                L = T.nota(NOTAS_FONDO[int(rng.integers(0, len(NOTAS_FONDO)))], 220, [(0.98, 0.86, 0.25), (0.95, 0.55, 0.60), (0.55, 0.85, 0.95),
                                                                                  (0.70, 0.92, 0.55)][rng.integers(0, 4)], 40, int(rng.integers(0, 40)))
                s = rng.uniform(0.75, 1.0)
            elif tipo == 2:
                L = recorte("", 420, int(rng.integers(0, 60)), bool(rng.integers(0, 2)))
            elif tipo == 3:
                L = T.ficha("", 420, 260, None, int(rng.integers(0, 40)))
            elif tipo == 4:
                L = calendario(int(rng.integers(1, 13)), int(rng.choice([2008, 2009, 2010, 2011])), (), 320, int(rng.integers(0, 30)))
            elif tipo == 5:
                L = impresion_codigo(int(rng.integers(30, 2500)), 30, 640, 15, int(rng.integers(0, 50)), titulo="main.cpp")
            elif tipo == 6:
                L = T.ficha(NOTAS_FONDO[int(rng.integers(0, len(NOTAS_FONDO)))], 400, 250, None, int(rng.integers(0, 40)), px=40, fuente="mano")
            elif tipo == 7:
                L = recorte("", 360, int(rng.integers(0, 60)), False)
            else:
                L = T.Lam(np.dstack([np.ones((300, 300, 3), np.float32) * np.float32([0.36, 0.22, 0.10]), _mancha_cafe(int(rng.integers(0, 20)))]), sr=0)
                s = rng.uniform(0.6, 1.1)
            L = T.oscura(L, 0.66)
            p = T.Pieza(L, x, y, rot, s, t_in=-10, entrada=None, chinchetas=((0, None, col),) if tipo != 8 else (), z=-1.0, capa=0, op=0.80,
                        sonido=False, flota=False)
            k += 1
    return k


@functools.lru_cache(maxsize=24)
def _mancha_cafe(seed):
    """Aro de café (alfa): solo un anillo tenue."""
    rng = np.random.default_rng(seed)
    a = np.zeros((300, 300), np.float32)
    cv2.circle(a, (150, 150), 110, 1.0, 5, cv2.LINE_AA)
    a = cv2.GaussianBlur(a, (0, 0), 2.5) * 0.35
    return a
