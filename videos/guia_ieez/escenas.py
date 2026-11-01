# -*- coding: utf-8 -*-
"""Guía de estudio IEEZ — fichas y diagramas por código (PIL), 16:9.
Todas las escenas usan `Mundo`, que dibuja el cuadro completo en función del tiempo global (plano continuo):
  fondo con profundidad (degradado por bloque + 3 capas de partículas en parallax + urna/retícula al fondo),
  cabecera fija (bloque actual, índice de bloques, barra de avance) y el contenido de la escena según su "vis"
  (guion.py): portada · tarjetas (grid, grid3, letras, tabla, linea, reloj, mesa) · pregunta (reloj de cuenta atrás) · respuesta.
Cada tarjeta aparece cuando la voz dice su palabra ancla (timeline.json)."""
import math
import re
import unicodedata

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from escena_base import Escena, TL
import guion as G

W, H = 1920, 1080
TOTAL = TL["total"]
FUENTES = {"b": "C:/Windows/Fonts/segoeuib.ttf", "s": "C:/Windows/Fonts/seguisb.ttf", "r": "C:/Windows/Fonts/segoeui.ttf",
           "n": "C:/Windows/Fonts/bahnschrift.ttf"}
_fc = {}


def F(k, px):
    if (k, px) not in _fc:
        try:
            _fc[(k, px)] = ImageFont.truetype(FUENTES[k], px)
        except OSError:
            _fc[(k, px)] = ImageFont.truetype(FUENTES["b"], px)
    return _fc[(k, px)]


# --------------------------------------------------------------------------- utilidades
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]+", "", s)


def cl(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def sm(x):
    x = cl(x)
    return x * x * (3 - 2 * x)


def back(x):
    x = cl(x)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def mezcla(a, b, u):
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))


def envolver(texto, fuente, ancho):
    lineas, actual = [], ""
    for p in texto.split():
        prueba = (actual + " " + p).strip()
        if fuente.getlength(prueba) <= ancho or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def ajustar(texto, k, px, ancho, max_lineas, minimo=22):
    """Tamaño de letra que hace caber el texto en `max_lineas` renglones."""
    while px > minimo:
        ln = envolver(texto, F(k, px), ancho)
        if len(ln) <= max_lineas:
            return px, ln
        px -= 2
    return px, envolver(texto, F(k, px), ancho)


# paleta: un acento por bloque (sobre fondo azul noche)
BLANCO, TINTA2, GRIS = (246, 248, 252), (190, 200, 222), (120, 132, 160)
VERDE, ROJO, ORO = (74, 222, 128), (248, 96, 96), (250, 204, 21)
ACENTOS = {0: (96, 165, 250), 1: (250, 204, 21), 2: (45, 212, 191), 3: (244, 114, 182), 4: (129, 140, 248),
           5: (251, 146, 60), 6: (56, 189, 248), 7: (163, 230, 53), 8: (232, 121, 249), 9: (253, 186, 116), 10: (250, 204, 21)}
FONDOS = {k: mezcla((10, 16, 34), v, 0.10) for k, v in ACENTOS.items()}

# --------------------------------------------------------------------------- escenas y anclas
ESC = TL["escenas"]
GUION = {e["id"]: e for e in G.ESCENAS}


def palabras(e):
    out = []
    for f in e["frases"]:
        for w in f.get("words", []):
            out.append((norm(w["w"]), w["s"], w["e"]))
    return out


def anclar(e, anclas):
    """Tiempo de aparición de cada ancla (secuencia de palabras, coincidencia por prefijo)."""
    ws = palabras(e)
    tiempos, ultimo = [], e["t0"]
    for k, a in enumerate(anclas):
        partes = [norm(p) for p in str(a).split() if norm(p)]
        hallado = None
        for desde_ultimo in (True, False):
            for i in range(len(ws)):
                if desde_ultimo and ws[i][1] < ultimo - 0.01:
                    continue
                if all(i + j < len(ws) and ws[i + j][0].startswith(partes[j]) for j in range(len(partes))):
                    hallado = ws[i][1]
                    break
            if hallado is not None:
                break
        if hallado is None:
            hallado = e["t0"] + 0.6 + 0.7 * k
        tiempos.append(hallado)
        ultimo = max(ultimo, hallado) if hallado >= ultimo else ultimo
    return tiempos


INFO = []
for e in ESC:
    g = GUION[e["id"]]
    vis = g.get("vis", {})
    items = vis.get("items", [])
    fin_voz = max([f["t1"] for f in e["frases"]] or [e["t0"]])
    ini_voz = min([f["t0"] for f in e["frases"]] or [e["t0"]])
    INFO.append(dict(id=e["id"], t0=e["t0"], t1=e["t1"], bloque=g.get("bloque", 0), vis=vis, ini=ini_voz, fin=fin_voz,
                     tiempos=anclar(e, [it[0] for it in items]) if items else []))


def escena_en(t):
    for i, d in enumerate(INFO):
        if t < d["t1"] or i == len(INFO) - 1:
            return i
    return len(INFO) - 1


# --------------------------------------------------------------------------- fondo con profundidad
_rng = np.random.default_rng(7)
CAPAS = []
for prof, n, r0, r1, vel, al in ((0.25, 70, 2, 5, 6, 60), (0.55, 34, 4, 9, 14, 45), (1.0, 14, 10, 22, 30, 28)):
    CAPAS.append(dict(x=_rng.uniform(0, W, n), y=_rng.uniform(0, H, n), r=_rng.uniform(r0, r1, n),
                      fase=_rng.uniform(0, 6.28, n), vel=vel, al=al))
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_vin = 1.0 - 0.55 * np.clip(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H * 0.45) / (H * 0.78)) ** 2, 0, 1)
_grad = (0.75 + 0.45 * (1 - _yy / H))[..., None]
_cache_fondo = {}


def fondo_base(col):
    if col not in _cache_fondo:
        c = np.array(col, np.float32)[None, None, :] * _grad * _vin[..., None]
        _cache_fondo[col] = np.clip(c, 0, 255).astype(np.uint8)
        if len(_cache_fondo) > 24:
            _cache_fondo.pop(next(iter(_cache_fondo)))
    return _cache_fondo[col]


def urna(d, cx, cy, s, col, al):
    """Urna electoral de línea, al fondo (capa lejana)."""
    c = col + (al,)
    w = 2 if s < 1.2 else 3
    d.rounded_rectangle([cx - 150 * s, cy - 60 * s, cx + 150 * s, cy + 140 * s], radius=int(14 * s), outline=c, width=w)
    d.line([cx - 70 * s, cy - 60 * s, cx + 70 * s, cy - 60 * s], fill=c, width=w + 3)
    d.polygon([(cx - 55 * s, cy - 130 * s), (cx + 45 * s, cy - 150 * s), (cx + 60 * s, cy - 62 * s), (cx - 40 * s, cy - 62 * s)], outline=c)
    d.line([cx - 30 * s, cy - 110 * s, cx + 30 * s, cy - 122 * s], fill=c, width=w)
    d.line([cx - 26 * s, cy - 92 * s, cx + 24 * s, cy - 102 * s], fill=c, width=w)


def dibujar_fondo(t, bloque_f):
    b0 = int(math.floor(bloque_f))
    b1 = min(10, b0 + 1)
    u = bloque_f - b0
    col = mezcla(FONDOS[b0], FONDOS[b1], u)
    im = Image.fromarray(fondo_base(col)).convert("RGBA")
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    acc = mezcla(ACENTOS[b0], ACENTOS[b1], u)
    # retícula en perspectiva (piso lejano)
    hor = H * 0.62
    for k in range(-14, 15):
        x0 = W / 2 + k * 60
        x1 = W / 2 + k * 420
        d.line([x0, hor, x1, H + 40], fill=acc + (16,), width=1)
    off = (t * 18) % 60
    for k in range(9):
        z = (k * 60 + off) / 540.0
        y = hor + (H - hor) * z ** 1.8
        d.line([0, y, W, y], fill=acc + (int(10 + 14 * z),), width=1)
    # urnas lejanas que derivan despacio
    urna(d, (W * 0.84 + 30 * math.sin(t * 0.07)) % W, H * 0.30 + 12 * math.sin(t * 0.21), 1.6, acc, 22)
    urna(d, (W * 0.12 - 20 * math.sin(t * 0.05)), H * 0.74 + 10 * math.sin(t * 0.17 + 1), 1.0, acc, 16)
    # partículas en 3 profundidades
    for cp in CAPAS:
        xs = (cp["x"] + t * cp["vel"]) % (W + 60) - 30
        ys = cp["y"] + 10 * np.sin(t * 0.4 + cp["fase"])
        for x, y, r, f in zip(xs, ys, cp["r"], cp["fase"]):
            a = int(cp["al"] * (0.6 + 0.4 * math.sin(t * 0.9 + f)))
            d.ellipse([x - r, y - r, x + r, y + r], fill=acc + (a,))
    im.alpha_composite(capa)
    return im, acc


# --------------------------------------------------------------------------- piezas
def tarjeta(w, h, titulo, sub, acc, px_t=46, px_s=28, resalto=0.0, centrado=False, borde_col=None):
    """Tarjeta con sombra, cara con leve degradado y borde de acento. Devuelve RGBA (con margen para la sombra)."""
    m = 26
    im = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(8, 0, -1):
        d.rounded_rectangle([m - k + 6, m - k + 12, m + w + k + 6, m + h + k + 12], radius=24 + k, fill=(0, 0, 0, 10))
    cara = (24, 32, 56)
    d.rounded_rectangle([m, m, m + w, m + h], radius=22, fill=cara + (238,))
    d.rounded_rectangle([m, m, m + w, m + h // 2], radius=22, fill=(255, 255, 255, 8))
    bc = borde_col or acc
    d.rounded_rectangle([m, m, m + w, m + h], radius=22, outline=mezcla(bc, BLANCO, 0.25 * resalto) + (int(110 + 145 * resalto),),
                        width=2 + int(2 * resalto))
    d.rounded_rectangle([m + 18, m + 18, m + 24, m + h - 18], radius=3, fill=bc + (255,))
    pad = 44
    px_t, lt = ajustar(titulo, "b", px_t, w - pad - 30, 2 if sub else 3)
    ls = []
    if sub:
        px_s, ls = ajustar(sub, "r", px_s, w - pad - 30, 3, 18)
    alto = len(lt) * px_t * 1.12 + (12 + len(ls) * px_s * 1.25 if ls else 0)
    y = m + (h - alto) / 2
    for ln in lt:
        x = m + (w - F("b", px_t).getlength(ln)) / 2 if centrado else m + pad
        d.text((x, y), ln, font=F("b", px_t), fill=BLANCO)
        y += px_t * 1.12
    y += 12
    for ln in ls:
        x = m + (w - F("r", px_s).getlength(ln)) / 2 if centrado else m + pad
        d.text((x, y), ln, font=F("r", px_s), fill=TINTA2)
        y += px_s * 1.25
    return im


def pegar(base, pieza, cx, cy, escala=1.0, alfa=1.0, ang=0.0):
    if alfa <= 0.01 or escala <= 0.02:
        return
    p = pieza
    if abs(escala - 1) > 0.01:
        p = p.resize((max(1, int(p.width * escala)), max(1, int(p.height * escala))), Image.BILINEAR)
    if abs(ang) > 0.05:
        p = p.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alfa < 0.999:
        a = p.getchannel("A").point(lambda v: int(v * alfa))
        p = p.copy()
        p.putalpha(a)
    x, y = int(cx - p.width / 2), int(cy - p.height / 2)
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + p.width), min(H, y + p.height)
    if x1 <= x0 or y1 <= y0:
        return
    base.alpha_composite(p.crop((x0 - x, y0 - y, x1 - x, y1 - y)), dest=(x0, y0))


_cache_piezas = {}


def pieza(clave, fabrica):
    if clave not in _cache_piezas:
        _cache_piezas[clave] = fabrica()
        if len(_cache_piezas) > 300:
            _cache_piezas.pop(next(iter(_cache_piezas)))
    return _cache_piezas[clave]


def entrada(t, ta, dur=0.45):
    u = (t - ta) / dur
    return cl(u), back(u)


def texto_centrado(d, y, texto, k, px, col, ancho=1600, max_l=3, inter=1.15):
    px, ln = ajustar(texto, k, px, ancho, max_l)
    for l in ln:
        d.text(((W - F(k, px).getlength(l)) / 2, y), l, font=F(k, px), fill=col)
        y += px * inter
    return y


def titulo_escena(base, txt, acc, t, ta, alfa):
    if not txt:
        return
    d = ImageDraw.Draw(base)
    a, _ = entrada(t, ta, 0.5)
    a *= alfa
    if a <= 0:
        return
    px, ln = ajustar(txt, "b", 60, 1500, 1, 40)
    f = F("b", px)
    x, y = 120, 128 + 18 * (1 - a)
    d.text((x, y), ln[0], font=f, fill=BLANCO + (int(255 * a),))
    lw = f.getlength(ln[0])
    d.rounded_rectangle([x, y + px + 14, x + lw * sm((t - ta) / 0.8), y + px + 20], radius=3, fill=acc + (int(255 * a),))


def nota(base, txt, alfa):
    if not txt or alfa <= 0:
        return
    d = ImageDraw.Draw(base)
    f = F("s", 24)
    w = f.getlength(txt)
    d.rounded_rectangle([110, H - 92, 110 + w + 40, H - 50], radius=21, fill=(8, 12, 26, int(170 * alfa)))
    d.text((130, H - 87), txt, font=f, fill=TINTA2 + (int(255 * alfa),))


def cabecera(base, t, d_esc, acc):
    d = ImageDraw.Draw(base)
    b = d_esc["bloque"]
    etiqueta = ("BLOQUE %d · " % b if 0 < b < 10 else "") + G.BLOQUES[b].upper()
    f = F("s", 26)
    w = f.getlength(etiqueta)
    d.rounded_rectangle([110, 44, 110 + w + 64, 92], radius=24, fill=(8, 12, 26, 190), outline=acc + (200,), width=2)
    d.ellipse([128, 60, 144, 76], fill=acc + (255,))
    d.text((156, 51), etiqueta, font=f, fill=BLANCO)
    # índice de bloques
    x = W - 110 - 11 * 34
    for k in range(11):
        cx = x + k * 34 + 12
        if k < b:
            d.ellipse([cx - 7, 61, cx + 7, 75], fill=ACENTOS[k] + (210,))
        elif k == b:
            r = 11 + 2 * math.sin(t * 4)
            d.ellipse([cx - r, 68 - r, cx + r, 68 + r], outline=acc + (255,), width=3)
            d.ellipse([cx - 6, 62, cx + 6, 74], fill=acc + (255,))
        else:
            d.ellipse([cx - 6, 62, cx + 6, 74], outline=GRIS + (200,), width=2)
    # barra de avance total
    d.rectangle([0, H - 8, W, H], fill=(8, 12, 26, 255))
    d.rectangle([0, H - 8, int(W * t / TOTAL), H], fill=acc + (255,))


# --------------------------------------------------------------------------- dibujo de cada tipo
def dib_portada(base, t, de, acc, alfa):
    v = de["vis"]
    d = ImageDraw.Draw(base)
    a, s = entrada(t, de["t0"] + 0.1, 0.7)
    a *= alfa
    if a <= 0:
        return
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    cx, cy = W / 2, 330
    sc = 0.9 + 0.1 * s
    # urna grande con boleta que entra
    dc.rounded_rectangle([cx - 150 * sc, cy - 40, cx + 150 * sc, cy + 150], radius=18, fill=(24, 32, 56, 255), outline=acc + (255,), width=4)
    dc.rounded_rectangle([cx - 80, cy - 46, cx + 80, cy - 34], radius=6, fill=(8, 12, 26, 255))
    yb = cy - 150 + 100 * sm((t - de["t0"] - 0.3) / 1.2) + 6 * math.sin(t * 2)
    dc.rounded_rectangle([cx - 52, yb - 70, cx + 52, yb + 40], radius=8, fill=BLANCO + (255,))
    dc.line([cx - 30, yb - 30, cx - 8, yb - 8, cx + 30, yb - 50], fill=acc + (255,), width=8)
    dc.rounded_rectangle([cx - 150 * sc, cy - 40, cx + 150 * sc, cy - 36], radius=2, fill=acc + (255,))
    dc.text((cx - F("b", 46).getlength("VOTO") / 2, cy + 60), "VOTO", font=F("b", 46), fill=acc + (255,))
    texto_centrado(dc, 560, v.get("titulo", ""), "b", 96, BLANCO, 1600, 2)
    texto_centrado(dc, 700, v.get("sub", ""), "s", 38, TINTA2, 1500, 2)
    if a < 0.999:
        capa.putalpha(capa.getchannel("A").point(lambda q: int(q * a)))
    base.alpha_composite(capa)


def dib_tarjetas(base, t, de, acc, alfa):
    v = de["vis"]
    lay = v.get("layout", "grid")
    items, ts = v.get("items", []), de["tiempos"]
    titulo_escena(base, v.get("titulo"), acc, t, de["t0"], alfa)
    nota(base, v.get("nota"), alfa * cl((t - de["t0"] - 0.4) / 0.5))
    vivo = max([k for k, ta in enumerate(ts) if ta <= t] or [-1])
    top, bot = 250, H - 120

    def res(k):
        return 1.0 if k == vivo else 0.0

    if lay in ("grid", "grid3"):
        n = len(items)
        cols = 3 if (lay == "grid3" or n > 4) else 2
        filas = math.ceil(n / cols)
        gw, gh = 1680, bot - top
        cw, ch = gw / cols, min(260, gh / filas)
        y0 = top + (gh - ch * filas) / 2
        for k, it in enumerate(items):
            r, c = divmod(k, cols)
            a, s = entrada(t, ts[k])
            if a <= 0:
                continue
            p = pieza(("g", de["id"], k, res(k)), lambda it=it, k=k: tarjeta(int(cw - 36), int(ch - 30), it[1], it[2] if len(it) > 2 else "",
                                                                              acc, px_t=50 if lay == "grid3" and r == 0 else 44, resalto=res(k)))
            cx = 120 + cw * c + cw / 2
            cy = y0 + ch * r + ch / 2 + 40 * (1 - s) + 4 * math.sin(t * 1.3 + k)
            pegar(base, p, cx, cy, 0.85 + 0.15 * s, a * alfa)
    elif lay == "letras":
        n = len(items)
        paso = min(270, 1680 / n)
        x0 = W / 2 - paso * (n - 1) / 2
        for k, it in enumerate(items):
            a, s = entrada(t, ts[k], 0.5)
            if a <= 0:
                continue
            def fab(it=it, rk=res(k)):
                im = Image.new("RGBA", (int(paso), 520), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                cx, r = paso / 2, min(110, paso * 0.42)
                for q in range(6, 0, -1):
                    d.ellipse([cx - r - q + 6, 150 - r - q + 12, cx + r + q + 6, 150 + r + q + 12], fill=(0, 0, 0, 14))
                d.ellipse([cx - r, 150 - r, cx + r, 150 + r], fill=(24, 32, 56, 245), outline=acc + (255,), width=4 + int(3 * rk))
                f = F("b", int(r * 1.15))
                d.text((cx - f.getlength(it[1]) / 2, 150 - r * 0.78), it[1], font=f, fill=acc + (255,))
                y = 290
                px, ln = ajustar(it[2], "b", 38, paso - 14, 3, 22)
                for l in ln:
                    d.text((cx - F("b", px).getlength(l) / 2, y), l, font=F("b", px), fill=BLANCO)
                    y += px * 1.15
                return im
            p = pieza(("l", de["id"], k, res(k)), fab)
            pegar(base, p, x0 + paso * k, 600 - 50 * (1 - s) + 6 * math.sin(t * 1.1 + k), 0.7 + 0.3 * s, a * alfa)
    elif lay == "tabla":
        cols = v.get("cols", ["", ""])
        d = ImageDraw.Draw(base)
        filas = [[], []]
        for k, it in enumerate(items):
            filas[it[1]].append(k)
        n = max(len(filas[0]), len(filas[1]), 1)
        cw = 800
        rh = min(92, (bot - top - 110) / n)
        for c in range(2):
            cx = W / 2 + (c - 0.5) * (cw + 60)
            a = cl((t - de["t0"] - 0.2) / 0.5) * alfa
            colc = acc if c == 0 else ORO
            f = F("b", 44)
            d.rounded_rectangle([cx - cw / 2, top, cx + cw / 2, top + 80], radius=18, fill=colc + (int(230 * a),))
            d.text((cx - f.getlength(cols[c]) / 2, top + 12), cols[c], font=f, fill=(10, 16, 34, int(255 * a)))
            for j, k in enumerate(filas[c]):
                aa, s = entrada(t, ts[k])
                if aa <= 0:
                    continue
                p = pieza(("t", de["id"], k, res(k)), lambda k=k, colc=colc: tarjeta(cw - 10, int(rh - 12), items[k][2], "", colc,
                                                                                     px_t=34, resalto=res(k)))
                pegar(base, p, cx + 50 * (1 - s) * (1 if c else -1), top + 110 + rh * j + rh / 2, 1.0, aa * alfa)
    elif lay in ("linea", "reloj"):
        n = len(items)
        d = ImageDraw.Draw(base)
        x0, x1, yl = (200, W - 200, 655) if lay == "reloj" else (350, W - 350, 600)
        paso = (x1 - x0) / max(1, n - 1)
        prog = max([k for k, ta in enumerate(ts) if ta <= t] or [-1])
        fin = x0 + paso * prog + (paso * sm((t - ts[prog]) / 0.6) if 0 <= prog < n - 1 and False else 0)
        d.line([x0, yl, x1, yl], fill=GRIS + (int(150 * alfa),), width=6)
        if prog >= 0:
            xa = x0 + paso * (prog - 1) + paso * sm((t - ts[prog]) / 0.5) if prog > 0 else x0
            d.line([x0, yl, xa, yl], fill=acc + (int(255 * alfa),), width=8)
        for k, it in enumerate(items):
            cx = x0 + paso * k
            a, s = entrada(t, ts[k], 0.5)
            col_n = acc if a > 0 else GRIS
            r = 22 + (8 if k == vivo else 0) * (0.8 + 0.2 * math.sin(t * 5))
            d.ellipse([cx - r, yl - r, cx + r, yl + r], fill=(24, 32, 56, int(255 * alfa)), outline=col_n + (int(255 * alfa),), width=5)
            if a <= 0:
                continue
            if lay == "reloj":
                hh, mm = [int(q) for q in it[1].split(":")]
                def fabr(hh=hh, mm=mm, txt=it[1], rk=res(k)):
                    im = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
                    dd = ImageDraw.Draw(im)
                    dd.ellipse([24, 24, 236, 236], fill=(24, 32, 56, 245), outline=acc + (255,), width=5 + int(3 * rk))
                    for q in range(12):
                        an = q / 12 * 2 * math.pi
                        dd.line([130 + 92 * math.sin(an), 130 - 92 * math.cos(an), 130 + 100 * math.sin(an), 130 - 100 * math.cos(an)],
                                fill=TINTA2 + (255,), width=4)
                    am = mm / 60 * 2 * math.pi
                    ah = ((hh % 12) + mm / 60) / 12 * 2 * math.pi
                    dd.line([130, 130, 130 + 80 * math.sin(am), 130 - 80 * math.cos(am)], fill=BLANCO + (255,), width=6)
                    dd.line([130, 130, 130 + 52 * math.sin(ah), 130 - 52 * math.cos(ah)], fill=acc + (255,), width=9)
                    dd.ellipse([122, 122, 138, 138], fill=acc + (255,))
                    return im
                pegar(base, pieza(("rel", de["id"], k, res(k)), fabr), cx, yl - 190 - 30 * (1 - s), 0.6 + 0.4 * s, a * alfa)
                f = F("n", 54)
                d.text((cx - f.getlength(it[1]) / 2, yl - 360), it[1], font=f, fill=BLANCO + (int(255 * a * alfa),))
                p = pieza(("rt", de["id"], k, res(k)), lambda it=it, rk=res(k): tarjeta(int(paso - 20), 170, it[2], "", acc, px_t=32, resalto=rk, centrado=True))
                pegar(base, p, cx, yl + 150 + 30 * (1 - s), 1.0, a * alfa)
            else:
                p = pieza(("ln", de["id"], k, res(k)), lambda it=it, rk=res(k): tarjeta(int(min(paso - 16, 470)), 260, it[1], it[2], acc, px_t=40, px_s=27,
                                                                                         resalto=rk, centrado=True))
                cy = yl - 185 if k % 2 == 0 else yl + 185
                pegar(base, p, cx, cy + (30 if k % 2 == 0 else -30) * (1 - s), 0.85 + 0.15 * s, a * alfa)
    elif lay == "mesa":
        d = ImageDraw.Draw(base)
        # diagrama del consejo a la izquierda: mesa en herradura con asientos
        cx, cy = 520, 610
        a0 = cl((t - de["t0"] - 0.1) / 0.6) * alfa
        d.arc([cx - 330, cy - 250, cx + 330, cy + 250], 200, 340, fill=GRIS + (int(200 * a0),), width=42)
        asientos = [("P", ORO, 270, 0)] + [("C", acc, ang, 1) for ang in (222, 246, 294, 318)] + [("S", TINTA2, 205, 2)] + \
                   [("R", GRIS, ang, 3) for ang in (335,)]
        for etiqueta, col, ang, k in asientos:
            aa, s = entrada(t, ts[k] if k < len(ts) else de["t0"], 0.45)
            if aa <= 0:
                continue
            r = 46 * (0.7 + 0.3 * s) + (5 * math.sin(t * 5) if k == vivo else 0)
            x = cx + 330 * math.cos(math.radians(ang))
            y = cy + 250 * math.sin(math.radians(ang)) - 70
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(255 * aa * alfa),), outline=BLANCO + (int(200 * aa * alfa),), width=3)
            f = F("b", 40)
            d.text((x - f.getlength(etiqueta) / 2, y - 27), etiqueta, font=f, fill=(10, 16, 34, int(255 * aa * alfa)))
        # rótulos de los asientos
        ley = [("P", "Presidente: voz y voto", ORO, 0), ("C", "4 consejeros: voz y voto", acc, 1),
               ("S", "Secretario: solo voz", TINTA2, 2), ("R", "Representantes: solo voz", GRIS, 3)]
        for j, (e_, txt, col, k) in enumerate(ley):
            aa, _ = entrada(t, ts[k] if k < len(ts) else de["t0"])
            if aa <= 0:
                continue
            y = 760 + j * 56
            d.ellipse([200, y + 4, 236, y + 40], fill=col + (int(255 * aa * alfa),))
            d.text((212 - F("b", 24).getlength(e_) / 2 + 6, y + 6), e_, font=F("b", 24), fill=(10, 16, 34, int(255 * aa * alfa)))
            d.text((252, y), txt, font=F("s", 32), fill=BLANCO + (int(255 * aa * alfa),))
        # tarjetas de datos a la derecha
        resto = list(range(4, len(items)))
        for j, k in enumerate(resto):
            aa, s = entrada(t, ts[k])
            if aa <= 0:
                continue
            r_, c_ = divmod(j, 2)
            p = pieza(("m", de["id"], k, res(k)), lambda k=k: tarjeta(440, 150, items[k][1], items[k][2], acc, px_t=38, px_s=25, resalto=res(k)))
            pegar(base, p, 1180 + c_ * 470 + 40 * (1 - s), 330 + r_ * 175, 0.85 + 0.15 * s, aa * alfa)


def reloj_cuenta(base, cx, cy, r, u, seg_rest, acc, alfa):
    d = ImageDraw.Draw(base)
    col = mezcla(acc, ROJO, sm((u - 0.6) / 0.4))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 32, 56, int(240 * alfa)), outline=GRIS + (int(160 * alfa),), width=10)
    if u < 1:
        d.arc([cx - r, cy - r, cx + r, cy + r], -90 + 360 * u, 270, fill=col + (int(255 * alfa),), width=14)
    txt = str(max(0, int(math.ceil(seg_rest))))
    f = F("n", int(r * 1.0))
    d.text((cx - f.getlength(txt) / 2, cy - r * 0.62), txt, font=f, fill=BLANCO + (int(255 * alfa),))


def dib_pregunta(base, t, de, acc, alfa):
    v = de["vis"]
    d = ImageDraw.Draw(base)
    a, s = entrada(t, de["t0"] + 0.05, 0.5)
    a *= alfa
    caso = v.get("caso")
    etiqueta = ("SIMULACRO · %d de 10" % v["num"]) if v.get("num") else ("CASO PRÁCTICO" if caso else "PREGUNTA")
    col = ORO if caso else acc
    f = F("b", 40)
    w = f.getlength(etiqueta)
    d.rounded_rectangle([W / 2 - w / 2 - 34, 190, W / 2 + w / 2 + 34, 254], radius=32, fill=col + (int(255 * a),))
    d.text((W / 2 - w / 2, 196), etiqueta, font=f, fill=(10, 16, 34, int(255 * a)))
    p = pieza(("q", de["id"]), lambda: tarjeta(1500, 340, v["texto"], "", col, px_t=58, centrado=True))
    pegar(base, p, W / 2, 480 + 40 * (1 - s), 0.9 + 0.1 * s, a)
    # reloj: corre en la pausa, tras la voz
    t_ini = de["fin"] + 0.15
    u = (t - t_ini) / v.get("cuenta", 4.0)
    ar = cl((t - t_ini + 0.4) / 0.4) * alfa
    if ar > 0:
        reloj_cuenta(base, W / 2, 830, 110, cl(u), v.get("cuenta", 4.0) * (1 - cl(u)), col, ar)
        ff = F("s", 32)
        msg = "Contesta en voz alta"
        d.text((W / 2 - ff.getlength(msg) / 2, 960), msg, font=ff, fill=TINTA2 + (int(255 * ar),))


def dib_respuesta(base, t, de, acc, alfa):
    v = de["vis"]
    d = ImageDraw.Draw(base)
    # la pregunta anterior queda arriba, atenuada
    i = [x["id"] for x in INFO].index(de["id"])
    prev = INFO[i - 1]["vis"] if i > 0 else {}
    if prev.get("tipo") == "pregunta":
        y = texto_centrado(d, 190, prev["texto"], "s", 36, TINTA2 + (int(200 * alfa),), 1500, 2)
    a, s = entrada(t, de["t0"] + 0.05, 0.55)
    a *= alfa
    if a <= 0:
        return
    def fab():
        w, h, m = 1500, 330, 26
        im = tarjeta(w, h, v["texto"], "", VERDE, px_t=64, centrado=True, resalto=1.0, borde_col=VERDE)
        dd = ImageDraw.Draw(im)
        dd.ellipse([m + w - 60, m - 40, m + w + 40, m + 60], fill=VERDE + (255,))
        dd.line([m + w - 32, m + 10, m + w - 12, m + 32, m + w + 18, m - 12], fill=(10, 40, 20, 255), width=10)
        return im
    pegar(base, pieza(("a", de["id"]), fab), W / 2, 560 - 30 * (1 - s), 0.88 + 0.12 * s, a)
    if v.get("fuente"):
        ff = F("s", 30)
        txt = "Fundamento: " + v["fuente"]
        aa = cl((t - de["t0"] - 0.6) / 0.5) * alfa
        w = ff.getlength(txt)
        d.rounded_rectangle([W / 2 - w / 2 - 30, 790, W / 2 + w / 2 + 30, 846], radius=28, fill=(8, 12, 26, int(200 * aa)),
                            outline=VERDE + (int(160 * aa),), width=2)
        d.text((W / 2 - w / 2, 798), txt, font=ff, fill=BLANCO + (int(255 * aa),))


DIB = dict(portada=dib_portada, tarjetas=dib_tarjetas, pregunta=dib_pregunta, respuesta=dib_respuesta)


def cuadro(t):
    i = escena_en(t)
    de = INFO[i]
    # el fondo cambia de color suavemente al entrar a un bloque nuevo
    bf = float(de["bloque"])
    if i > 0 and INFO[i - 1]["bloque"] != de["bloque"]:
        bf = INFO[i - 1]["bloque"] + (de["bloque"] - INFO[i - 1]["bloque"]) * sm((t - de["t0"]) / 0.8)
        if de["bloque"] < INFO[i - 1]["bloque"]:
            bf = float(de["bloque"])
    base, acc = dibujar_fondo(t, min(bf, 10.0))
    acc = ACENTOS[de["bloque"]]
    alfa = sm((t - de["t0"]) / 0.3) * sm((de["t1"] - t) / 0.28)
    if i == 0:
        alfa = sm((de["t1"] - t) / 0.28)
    DIB.get(de["vis"].get("tipo", "tarjetas"), dib_tarjetas)(base, t, de, acc, alfa)
    cabecera(base, t, de, acc)
    img = np.asarray(base.convert("RGB"), dtype=np.float32) / 255.0
    img *= sm(t / 0.5) * sm((TOTAL - t) / 0.8)
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in ESC}
