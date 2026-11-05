# -*- coding: utf-8 -*-
"""Kit DOCUMENTAL DE PERSONAJE ANTIGUO (4-nov-2026). Calco de «Detrás del Enigma» (2026: tomas de cine oscuras + grafismos sobre negro)
con lo mejor de «Homo Narrans» (artefactos REALES sobre piedra oscura, citas de fuentes antiguas en amarillo, mapas con el territorio
en rojo que crece). Doc: docs/estilo_docu_antiguo.md.

REGLA DEL KIT (el usuario, 4-nov-2026): **cada escena tiene sus propias animaciones; nada se recicla** ni dentro del video ni entre
videos. Estas funciones son PRIMITIVAS (letra, luz, líquido, piedra, mapa); la composición de cada escena se diseña para su frase y
se declara con `firma(escena, receta)`; `verificar_firmas(video)` falla si una receta se repite (catálogo en
`nucleo/datos/docu_antiguo_firmas.json`, que `registrar_firmas(video)` amplía al cerrar el video).

Todo dibuja sobre `lz` float32 (H, W, 3) RGB 0..1 como `docu.py`; el acabado final es `cine_antiguo(img, t)`.
Tipografías (medidas en cuadros del original):
  ROTULO  Times New Roman Bold, VERSALES con tracking, blanco; la palabra clave en ROJO (rotulo_serif)   «HEMORRAGIAS POR ESTRÉS»
  NEON    el mismo serif, núcleo blanco rosado y halo rojo que parpadea al encender (neon)                 «NO ES MAGIA»
  CURSIVA Poppins SemiBold Italic MAYÚSCULAS con brillo blanco (o rojo) (cursiva_luz)                      «Y LO CONSIGUEN»
  MIXTO   Poppins SemiBold, palabras blancas y grises que suben desde una máscara (texto_mixto)             «Se acerca al cuadro»
  CITA    Arial Bold amarillo sobre piedra, línea a línea, fuente debajo (cita)                            (Homo Narrans)
"""
import functools
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from motor import H, W, clamp01, e_back, e_inout, e_out, prog
import docu as D
import docu_fx as DX

BLANCO = (0.97, 0.95, 0.92)
GRIS = (0.62, 0.62, 0.64)
ROJO = (0.86, 0.06, 0.08)
ROJO_HALO = (1.0, 0.10, 0.12)
AMARILLO = (0.98, 0.80, 0.16)          # amarillo de las citas (Homo Narrans)
VERDE_AURA = (0.35, 1.0, 0.25)
ORO = (0.93, 0.74, 0.36)

_FD = os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts")
FUENTES = dict(
    serif="C:/Windows/Fonts/timesbd.ttf",
    serif_r="C:/Windows/Fonts/times.ttf",
    sans=os.path.join(_FD, "Poppins-SemiBold.ttf"),
    sans_i=os.path.join(_FD, "Poppins-SemiBoldItalic.ttf"),
    cita="C:/Windows/Fonts/arialbd.ttf",
)
_AQUI = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(_AQUI, "datos", "docu_antiguo_firmas.json")


# ------------------------------------------------------------------ texto base
@functools.lru_cache(maxsize=64)
def _fuente(nombre, px):
    return ImageFont.truetype(FUENTES.get(nombre, nombre), int(px))


@functools.lru_cache(maxsize=512)
def _glifos(txt, fnt, px, track=0.0):
    """Máscara (uint8) de un texto y la caja x de cada letra (para revelar letra a letra). `track` = espacio extra en fracción de px."""
    f = _fuente(fnt, px)
    xs, x = [], 0.0
    for ch in txt:
        w = f.getlength(ch)
        xs.append((x, x + w))
        x += w + track * px
    asc, desc = f.getmetrics()
    pad = int(px * 0.35)
    im = Image.new("L", (int(x) + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(im)
    for ch, (a, _) in zip(txt, xs):
        d.text((pad + a, pad), ch, font=f, fill=255)
    return np.asarray(im), tuple((a + pad, b + pad) for a, b in xs), pad


def _pegar_mask(lz, m, x0, y0, color, op=1.0, glow=0.0, sigma=10.0, color_glow=None):
    """Pega una máscara (float 0..1) como color sólido con halo opcional (aditivo)."""
    if op <= 0.003:
        return
    if glow > 0:
        g = cv2.GaussianBlur(m, (0, 0), sigma) * glow
        D.mezclar_pm(lz, g[..., None] * np.float32(color_glow or color), g, x0, y0, op, aditivo=True)
    D.mezclar_pm(lz, m[..., None] * np.float32(color), m, x0, y0, op)


def _ventana(t, t0, salida, dur_sal=0.45):
    """Opacidad de salida (1 hasta `salida`, luego fundido)."""
    if salida is None:
        return 1.0
    return 1.0 - e_inout(prog(t, salida, salida + dur_sal))


# ------------------------------------------------------------------ ROTULO serif en versales, letra a letra
def rotulo_serif(lz, partes, cx, cy, t, t0, px=34, track=0.06, vel=0.032, salida=None, op=1.0, glow=0.35):
    """partes = [("HEMORRAGIAS POR ", BLANCO), ("ESTRÉS", ROJO)]. Cada letra aparece con fundido y un leve desenfoque que se aclara
    (como el original); `vel` = s entre letras. Centrado en (cx, cy)."""
    txt = "".join(p for p, _ in partes)
    m, cajas, pad = _glifos(txt, "serif", px, track)
    mf = m.astype(np.float32) / 255.0
    hh, ww = mf.shape
    x0, y0 = int(cx - ww / 2), int(cy - hh / 2)
    k = _ventana(t, t0, salida) * op
    i = 0
    for parte, color in partes:
        a = cajas[i][0] if i < len(cajas) else 0
        b = cajas[min(i + len(parte), len(cajas)) - 1][1] if parte else a
        # revelado por letra: alfa por columna
        cols = np.zeros(ww, np.float32)
        for j in range(i, i + len(parte)):
            u = e_out(prog(t, t0 + j * vel, t0 + j * vel + 0.22))
            ca, cb = int(cajas[j][0]), int(math.ceil(cajas[j][1])) + 1
            cols[ca:cb] = np.maximum(cols[ca:cb], u)
        sub = mf * cols[None, :]
        sub[:, :int(a)] = 0
        sub[:, int(b) + 1:] = 0
        _pegar_mask(lz, sub, x0, y0, color, k, glow=glow, sigma=px * 0.25)
        i += len(parte)


# ------------------------------------------------------------------ NEÓN rojo con encendido
def neon(lz, txt, cx, cy, t, t0, px=58, color=ROJO_HALO, salida=None, op=1.0, barras=True):
    """Texto serif con núcleo blanco rosado y halo rojo doble; parpadea 0,35 s al encender. `barras`: las dos franjas grises
    desenfocadas que el original pone encima."""
    m, _, _ = _glifos(txt, "serif", px, 0.04)
    mf = m.astype(np.float32) / 255.0
    hh, ww = mf.shape
    x0, y0 = int(cx - ww / 2), int(cy - hh / 2)
    dt = t - t0
    if dt < 0:
        return
    flick = 1.0 if dt > 0.38 else (0.25 + 0.75 * (math.sin(dt * 90) > -0.2)) * min(1, dt / 0.1)
    k = flick * _ventana(t, t0, salida) * op
    if barras:
        bw, bh = int(ww * 0.42), max(6, int(px * 0.16))
        bar = np.zeros((bh * 5, bw), np.float32)
        bar[bh * 2:bh * 3] = 0.5
        bar = cv2.GaussianBlur(bar, (0, 0), bh * 0.6)
        for sx in (x0 - int(ww * 0.06), x0 + ww - bw + int(ww * 0.06)):
            D.mezclar_pm(lz, bar[..., None] * np.float32(GRIS), bar, sx, y0 - int(px * 1.25), k * 0.8)
    for sig, g in ((px * 0.9, 0.9), (px * 0.28, 1.4)):
        h_ = cv2.GaussianBlur(mf, (0, 0), sig) * g
        D.mezclar_pm(lz, h_[..., None] * np.float32(color), h_, x0, y0, k, aditivo=True)
    _pegar_mask(lz, mf, x0, y0, (1.0, 0.86, 0.84), k)


# ------------------------------------------------------------------ CURSIVA con brillo y TEXTO MIXTO
def cursiva_luz(lz, txt, cx, cy, t, t0, px=46, color=BLANCO, salida=None, op=1.0, glow=0.9):
    """Poppins SemiBold Italic mayúsculas con brillo; entra con fundido y un acercamiento leve (escala 0,97 -> 1)."""
    m, _, _ = _glifos(txt.upper(), "sans_i", px, 0.02)
    mf = m.astype(np.float32) / 255.0
    u = e_out(prog(t, t0, t0 + 0.5))
    if u <= 0:
        return
    s = 0.97 + 0.03 * u
    mf = cv2.resize(mf, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
    hh, ww = mf.shape
    _pegar_mask(lz, mf, int(cx - ww / 2), int(cy - hh / 2), color, u * _ventana(t, t0, salida) * op, glow=glow, sigma=px * 0.35)


def texto_mixto(lz, partes, cx, cy, t, t0, px=52, vel=0.12, salida=None, op=1.0, alinear="izq"):
    """partes = [("Se acerca", BLANCO), ("al cuadro", GRIS)]: cada palabra sube 0,4·px desde una máscara (sin verse fuera)."""
    palabras = [(w, c) for p, c in partes for w in p.split()]
    f = _fuente("sans", px)
    esp = f.getlength(" ")
    anchos = [f.getlength(w) for w, _ in palabras]
    total = sum(anchos) + esp * (len(palabras) - 1)
    x = cx if alinear == "izq" else cx - total / 2
    k = _ventana(t, t0, salida) * op
    for i, ((w, c), aw) in enumerate(zip(palabras, anchos)):
        m, _, pad = _glifos(w, "sans", px)
        u = e_out(prog(t, t0 + i * vel, t0 + i * vel + 0.45))
        if u > 0:
            mf = m.astype(np.float32) / 255.0
            dy = int((1 - u) * px * 0.45)
            vis = np.zeros_like(mf)                      # máscara: la palabra solo se ve dentro de su renglón
            vis[:mf.shape[0] - dy] = mf[dy:] if dy else mf
            _pegar_mask(lz, vis * u, int(x - pad), int(cy - mf.shape[0] / 2), c, k, glow=0.15, sigma=6)
        x += aw + esp


# ------------------------------------------------------------------ CAMAFEO (retrato circular con borde de luz)
@functools.lru_cache(maxsize=32)
def _camafeo_spr(ruta, r, fx, fy, zoom):
    img = cv2.cvtColor(cv2.imread(ruta, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    lado = int(min(h, w) / zoom)
    cx, cy = int(fx * w), int(fy * h)
    x0 = int(np.clip(cx - lado // 2, 0, w - lado)); y0 = int(np.clip(cy - lado // 2, 0, h - lado))
    rec = cv2.resize(img[y0:y0 + lado, x0:x0 + lado], (2 * r, 2 * r), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[0:2 * r, 0:2 * r]
    d = np.hypot(xx - r + 0.5, yy - r + 0.5)
    a = np.clip(r - d, 0, 1).astype(np.float32)
    aro = np.clip(1.6 - np.abs(d - (r - 1.5)), 0, 1).astype(np.float32)
    return rec, a, aro


def camafeo(lz, ruta, cx, cy, r, t, t0, foco=(0.5, 0.4), zoom=1.0, salida=None, op=1.0, flota=6.0):
    """Retrato circular con aro blanco fino y halo, entra con rebote (e_back) y flota despacio."""
    u = e_back(prog(t, t0, t0 + 0.55))
    if u <= 0:
        return
    rec, a, aro = _camafeo_spr(ruta, int(r), foco[0], foco[1], zoom)
    s = max(0.05, u)
    k = clamp01(prog(t, t0, t0 + 0.25)) * _ventana(t, t0, salida) * op
    dy = math.sin((t - t0) * 1.3) * flota
    M = D.poner(rec.shape[1], rec.shape[0], cx, cy + dy, s)
    spr = D.Sprite(rec, a, sombra=True, sr=14, off=(0, 10), sop=0.6)
    D.pegar(lz, spr, M, k)
    g = cv2.GaussianBlur(aro, (0, 0), 7) * 1.2 + aro
    gw = cv2.warpPerspective(np.clip(g, 0, 1), M, (W, H))
    lz += gw[..., None] * np.float32(BLANCO) * k * 0.9


# ------------------------------------------------------------------ LÍQUIDO (relleno orgánico que crece hacia abajo)
def liquido(lz, x, y, w, alto, u, t, color=ROJO, sem=0, op=1.0):
    """Mancha líquida que nace en (x, y) (centro superior) y baja hasta `alto`·u con borde ondulado y gotas; como la sangre bajo los
    camafeos del original. Coste bajo: se calcula solo en su caja."""
    if u <= 0:
        return
    hh = int(alto * u) + 20
    ww = int(w * 1.3)
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    rng = np.random.default_rng(sem)
    fases = rng.uniform(0, 6.3, 4)
    cxl = ww / 2
    # ancho que se abre como gota y se ensancha abajo
    prof = yy / max(1.0, alto)
    semi = (w / 2) * (0.55 + 0.45 * np.sqrt(np.clip(prof * 2.5, 0, 1))) * (1 + 0.10 * np.sin(yy * 0.012 + fases[0] + t * 0.9))
    borde_x = semi + 9 * np.sin(yy * 0.021 + fases[1] + t * 1.3) + 4 * np.sin(yy * 0.047 + fases[2])
    fondo = alto * u + 16 * np.sin(xx * 0.022 + fases[2] + t * 1.1) + 7 * np.sin(xx * 0.061 + fases[3])
    dentro = (np.abs(xx - cxl) < borde_x) & (yy < fondo)
    m = cv2.GaussianBlur(dentro.astype(np.float32), (0, 0), 2.4)
    brillo = np.clip(1 - np.abs(xx - cxl + w * 0.18) / (w * 0.12), 0, 1) * 0.18
    col = np.float32(color)[None, None] * (0.85 + brillo[..., None])
    D.mezclar_pm(lz, col * m[..., None], m, int(x - cxl), int(y), op)


# ------------------------------------------------------------------ AURA de color sobre una figura (máscara de rembg)
def aura(lz, mascara, x0, y0, color=VERDE_AURA, t=0.0, fuerza=0.8, op=1.0):
    """Ilumina una figura recortada (máscara float 0..1 del tamaño de la figura en pantalla) con relleno translúcido y halo que respira."""
    p = 0.75 + 0.25 * math.sin(t * 3.1)
    g = cv2.GaussianBlur(mascara, (0, 0), 18) * 0.9 + mascara * 0.55
    D.mezclar_pm(lz, g[..., None] * np.float32(color), g, x0, y0, op * fuerza * p, aditivo=True)


# ------------------------------------------------------------------ PIEDRA oscura, ARTEFACTO real y CITA (Homo Narrans)
@functools.lru_cache(maxsize=4)
def piedra(sem=0, tono=(0.11, 0.115, 0.12)):
    """Pizarra oscura con vetas suaves y relieve (fondo de los objetos reales). float32 HxWx3."""
    rng = np.random.default_rng(sem)
    capas = np.zeros((H, W), np.float32)
    for esc, peso in ((8, 0.5), (32, 0.3), (128, 0.2)):
        r = rng.standard_normal((H // esc + 2, W // esc + 2)).astype(np.float32)
        capas += cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC) * peso
    capas = cv2.GaussianBlur(capas, (0, 0), 1.2)
    rel = np.clip(0.5 + 0.18 * (capas - np.roll(capas, 2, 0)), 0, 1)
    base = np.float32(tono)[None, None] * (0.8 + 0.4 * rel[..., None]) * (1 + 0.18 * capas[..., None])
    return np.clip(base, 0, 1)


@functools.lru_cache(maxsize=24)
def _sprite_png(ruta, alto):
    im = Image.open(ruta).convert("RGBA")
    caja = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    if caja:
        im = im.crop(caja)                                   # sin el margen transparente del recorte
    k = alto / im.height
    im = im.resize((max(1, int(im.width * k)), int(alto)), Image.LANCZOS)
    a = np.asarray(im)
    return D.Sprite(a[..., :3], a[..., 3].astype(np.float32) / 255.0, sombra=True, sr=22, off=(14, 26), sop=0.75)


def artefacto(lz, ruta_png, cx, cy, alto, t, t0, giro=7.0, luz=True, salida=None, op=1.0, sube=40.0):
    """Objeto REAL recortado (PNG con alfa) sobre la piedra: entra subiendo con sombra, gira despacio en Y (lámina 3D) y una franja de
    luz le pasa por encima una vez."""
    u = e_out(prog(t, t0, t0 + 0.9))
    if u <= 0:
        return
    spr = _sprite_png(ruta_png, int(alto))
    ry = giro * math.sin((t - t0) * 0.45)
    M = D.poner(spr.w, spr.h, cx, cy + (1 - u) * sube, 1.0, ry=ry)
    k = u * _ventana(t, t0, salida) * op
    D.pegar(lz, spr, M, k)
    if luz:
        f = prog(t, t0 + 0.6, t0 + 2.2)
        if 0 < f < 1:
            yy, xx = np.mgrid[0:spr.h, 0:spr.w].astype(np.float32)
            banda = np.exp(-((xx + yy * 0.5 - f * (spr.w + spr.h * 0.5)) / (spr.w * 0.08)) ** 2) * spr.a * 0.35
            bw = cv2.warpPerspective(banda, M, (W, H))
            lz += bw[..., None] * np.float32((1.0, 0.95, 0.85)) * k


def cita(lz, lineas, cx, cy, t, t0, px=38, fuente_txt=None, vel=0.55, salida=None, op=1.0, color=AMARILLO):
    """Cita de una fuente antigua (estela, papiro, tablilla): Arial Bold amarillo, centrada, línea a línea; comillas incluidas por quien
    llama. `fuente_txt` (gris, pequeña) debajo. Para citas largas sobre `piedra()`."""
    inter = px * 1.28
    y = cy - inter * (len(lineas) - 1) / 2
    k = _ventana(t, t0, salida) * op
    for i, ln in enumerate(lineas):
        u = e_out(prog(t, t0 + i * vel, t0 + i * vel + 0.5))
        if u > 0:
            m, _, _ = _glifos(ln, "cita", px)
            mf = m.astype(np.float32) / 255.0
            _pegar_mask(lz, mf, int(cx - mf.shape[1] / 2), int(y - mf.shape[0] / 2 + (1 - u) * 10), color, u * k, glow=0.2, sigma=6)
        y += inter
    if fuente_txt:
        u = e_out(prog(t, t0 + len(lineas) * vel, t0 + len(lineas) * vel + 0.5))
        m, _, _ = _glifos(fuente_txt, "sans", int(px * 0.55))
        mf = m.astype(np.float32) / 255.0
        _pegar_mask(lz, mf, int(cx - mf.shape[1] / 2), int(y + px * 0.2), GRIS, u * k)


# ------------------------------------------------------------------ REJILLA 3D, ARCO de luz y POLVO
def rejilla(lz, t, horizonte=0.56, color=(0.5, 0.5, 0.55), op=0.35, paso=120, vel=0.0):
    """Suelo de rejilla en perspectiva que se pierde en la oscuridad (escenario del «UN FARSANTE»). `vel` desplaza la rejilla."""
    hz = int(H * horizonte)
    capa = np.zeros((H, W), np.float32)
    f = 900.0
    for i in range(-14, 15):                                 # líneas que fugan
        xb = W / 2 + i * paso * 6
        cv2.line(capa, (int(W / 2 + i * paso * 0.25), hz), (int(xb), H), 1.0, 1, cv2.LINE_AA)
    z = (t * vel) % 1.0
    for j in range(1, 30):                                   # horizontales con profundidad
        zz = (j - z) * 0.35
        if zz <= 0.05:
            continue
        yy = hz + f * 0.5 / zz * 0.35
        if yy < H:
            cv2.line(capa, (0, int(yy)), (W, int(yy)), 1.0, 1, cv2.LINE_AA)
    yy = np.arange(H, dtype=np.float32)
    caida = np.clip((yy - hz) / (H - hz), 0, 1) ** 0.8
    capa *= caida[:, None]
    lz += capa[..., None] * np.float32(color) * op


def arco_luz(lz, p0, p1, curva, u, color=ROJO_HALO, grosor=3, op=1.0, cola=0.45):
    """Trazo curvo de luz (bezier cuadrático) que se dibuja con cabeza brillante y cola que se apaga."""
    if u <= 0:
        return
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - curva
    n = 90
    s = np.linspace(max(0, u - cola), u, n)
    xs = (1 - s) ** 2 * x0 + 2 * (1 - s) * s * mx + s ** 2 * x1
    ys = (1 - s) ** 2 * y0 + 2 * (1 - s) * s * my + s ** 2 * y1
    capa = np.zeros((H, W), np.float32)
    for i in range(n - 1):
        cv2.line(capa, (int(xs[i]), int(ys[i])), (int(xs[i + 1]), int(ys[i + 1])), float((i + 1) / n), grosor, cv2.LINE_AA)
    g = cv2.GaussianBlur(capa, (0, 0), 9) * 1.6 + capa
    lz += np.clip(g, 0, 2)[..., None] * np.float32(color) * op


def polvo(lz, t, n=60, sem=3, op=0.5, tam=2.2):
    """Motas de polvo que flotan delante de la cámara (desenfocadas algunas)."""
    rng = np.random.default_rng(sem)
    xs, ys = rng.uniform(0, W, n), rng.uniform(0, H, n)
    vx, vy = rng.uniform(-8, 8, n), rng.uniform(-14, -3, n)
    r = rng.uniform(0.6, 1.0, n) * tam
    capa = np.zeros((H, W), np.float32)
    for i in range(n):
        x, y = (xs[i] + vx[i] * t) % W, (ys[i] + vy[i] * t) % H
        cv2.circle(capa, (int(x), int(y)), max(1, int(r[i])), float(rng.uniform(0.3, 1.0)), -1, cv2.LINE_AA)
    capa = cv2.GaussianBlur(capa, (0, 0), 1.2)
    lz += capa[..., None] * op


# ------------------------------------------------------------------ MAPA: territorio que crece y etiquetas
def territorio(lz, poligono, semilla_xy, u, t, color=ROJO, op=0.72, sem=0, borde=True):
    """Rellena `poligono` (lista de (x, y) en pantalla) creciendo desde `semilla_xy` con frente irregular (como la mancha roja del imperio
    en Homo Narrans). u 0..1."""
    if u <= 0:
        return
    poligono = np.clip(np.int32(poligono), 0, (W - 1, H - 1))        # un polígono que toca el borde rompía las máscaras (4-nov)
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [poligono], 255)
    x, y, w, h = cv2.boundingRect(poligono)
    sx, sy = semilla_xy
    yy, xx = np.mgrid[y:y + h, x:x + w].astype(np.float32)
    d = np.hypot(xx - sx, yy - sy)
    dmax = d[m[y:y + h, x:x + w] > 0].max() if (m[y:y + h, x:x + w] > 0).any() else 1.0
    ang = np.arctan2(yy - sy, xx - sx)
    ruido = 0.06 * dmax * (np.sin(ang * 5 + sem) + 0.5 * np.sin(ang * 11 + t * 0.7 + sem))
    frente = u * dmax * 1.05 + ruido
    vis = ((d < frente) & (m[y:y + h, x:x + w] > 0)).astype(np.float32)
    vis = cv2.GaussianBlur(vis, (0, 0), 2.0)
    D.mezclar_pm(lz, vis[..., None] * np.float32(color), vis * 1.0, x, y, op)
    if borde and u < 1:
        fr = np.clip(1 - np.abs(d - frente) / 6, 0, 1) * (m[y:y + h, x:x + w] > 0)
        D.mezclar_pm(lz, fr[..., None] * np.float32((1, 0.5, 0.4)), fr, x, y, 0.8, aditivo=True)


def etiqueta(lz, txt, x, y, t, t0, px=30, color=BLANCO, punto=True, salida=None, op=1.0):
    """Nombre de lugar en el mapa (Poppins SemiBold) con punto blanco que late."""
    u = e_out(prog(t, t0, t0 + 0.4))
    if u <= 0:
        return
    k = u * _ventana(t, t0, salida) * op
    if punto:
        r = 6 + 2 * math.sin((t - t0) * 4)
        capa = np.zeros((H, W), np.float32)
        cv2.circle(capa, (int(x), int(y)), int(r), 1.0, -1, cv2.LINE_AA)
        lz += (cv2.GaussianBlur(capa, (0, 0), 5) + capa)[..., None] * np.float32(BLANCO) * k * 0.8
    m, _, pad = _glifos(txt, "sans", px)
    mf = m.astype(np.float32) / 255.0
    _pegar_mask(lz, mf, int(x + 14 - pad), int(y - mf.shape[0] / 2), color, k, glow=0.25, sigma=5)


# ------------------------------------------------------------------ acabado
def cine_antiguo(img, t, tinte=None, **k):
    """Acabado del kit: el filtro `docu_fx.cine` con valores medidos en la referencia 2026 (menos escaneo, más viñeta y bloom). Sin
    tilt-shift por defecto: en el original los grafismos y rótulos van nítidos; las tomas de cine traen su propio desenfoque
    (pasa `tilt=3.5` solo en tomas de foto/película sin texto arriba)."""
    base = dict(tilt=0.0, banda=0.58, ca=1.4, bloom=0.30, escaneo=0.05, vineta=0.78, grano=0.045, polvo=0.12, sat=0.88,
                calido=0.04, teal=0.05)
    base.update(k)
    return DX.cine(img, t, tinte=tinte, **base)


# ------------------------------------------------------------------ REGLA: cada escena con animación propia
_FIRMAS = {}


def firma(escena, receta):
    """Declara la animación de una escena: `receta` describe la composición («camafeo niño + líquido rojo que baja + rótulo serif»).
    Se compara normalizada (minúsculas, sin espacios dobles)."""
    _FIRMAS[escena] = " ".join(receta.lower().split())


def verificar_firmas(video):
    """Lista de problemas: recetas repetidas dentro del video o ya usadas en otro video del kit (catálogo)."""
    prob, vistas = [], {}
    for esc, r in _FIRMAS.items():
        if r in vistas:
            prob.append(f"«{esc}» repite la animación de «{vistas[r]}»: {r}")
        vistas[r] = esc
    cat = json.load(open(CATALOGO, encoding="utf-8")) if os.path.exists(CATALOGO) else {}
    for v, recetas in cat.items():
        if v == video:
            continue
        for esc, r in _FIRMAS.items():
            if r in recetas.values():
                prob.append(f"«{esc}» repite una animación del video {v}: {r}")
    return prob


def registrar_firmas(video):
    """Al cerrar el video: guarda sus recetas en el catálogo para que ningún video futuro las repita."""
    cat = json.load(open(CATALOGO, encoding="utf-8")) if os.path.exists(CATALOGO) else {}
    cat[video] = dict(_FIRMAS)
    json.dump(cat, open(CATALOGO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
