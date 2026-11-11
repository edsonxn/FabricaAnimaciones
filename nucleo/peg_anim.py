# -*- coding: utf-8 -*-
"""CATÁLOGO DE ANIMACIONES DE PEGATINAS (el usuario, 5-nov-2026, TODOS los canales: «hay que aumentar el catálogo de animaciones
de cómo se presentan las pegatinas e imágenes, tienen que ser muchas más formas para que no se sientan repetidas»).

Cada pegatina = MARCO (cómo va vestida la imagen) + ENTRADA (cómo aparece) + ESTANCIA (qué hace mientras está) + SALIDA (cómo se
va). Todo se dibuja en 3D (homografías de cv2 con perspectiva, sombra dinámica que se separa con la altura): nada plano.
  marcos    clasico polaroid carta cristal rasgado museo monitor aura(solo recortes sin fondo)
  entradas  pop cae volteo rasgado tinta enfoque cortinilla origami deslizar ventana bisagra glitch tijera cristal iman sello
            tiras baldosas ceniza remolino vuela
  estancias flota inclina kenburns brillo lupa quieta pulso
  salidas   funde cae volteo rasgado tinta enfoque cortinilla origami deslizar ventana bisagra glitch cristal tiras baldosas
            ceniza remolino vuela
  + AMPLIACIÓN 5-nov-2026 (`nucleo/peg_anim_mas.py`, se registra sola): marcos pergamino vitral naipe estampilla · entradas y
    salidas persiana portal escaner desenrolla aplasta · estancias orbita vela balanceo
  + pila(fotos)  pila de fotos que se reparte en fila · presentaciones de VARIAS imágenes: `nucleo/presenta.py`
VARIADO SIN REPETIR: `variado(ruta, titulo, tam, tema)` reparte las combinaciones con un rotador por video (bolsas barajadas con
afinidad por tema: nunca la misma entrada/salida/marco dos veces seguidas y recorre todo el catálogo antes de repetir).
Uso en efectos.py: helper `pv()` de videos/_plantilla_yt/efectos.py. Colores: peg_estilos.TEMAS (tes wow er gaming spyro n64
pokemon cod plasti). Receta y tabla: docs/estilo_secuencia_yt.md § «CATÁLOGO DE ANIMACIONES DE PEGATINAS».
  python nucleo/peg_anim.py hoja [--tema er] [--img ruta.png] [--fondo ruta.jpg] [--salida carpeta]   hojas de prueba (MÍRALAS)
"""
import hashlib
import math
import os
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

import mg_tes as T
import peg_estilos as PE

FOCAL = 1800.0
MARCOS_TODOS = ("clasico", "polaroid", "carta", "cristal", "rasgado", "museo", "monitor", "aura")
ENTRADAS = ("pop", "cae", "volteo", "rasgado", "tinta", "enfoque", "cortinilla", "origami", "deslizar", "ventana", "bisagra",
            "glitch", "tijera", "cristal", "iman", "sello", "tiras", "baldosas", "ceniza", "remolino", "vuela")
ESTANCIAS = ("flota", "inclina", "kenburns", "brillo", "lupa", "quieta", "pulso")
SALIDAS = ("funde", "cae", "volteo", "rasgado", "tinta", "enfoque", "cortinilla", "origami", "deslizar", "ventana", "bisagra",
           "glitch", "cristal", "tiras", "baldosas", "ceniza", "remolino", "vuela")
# afinidad por familia de tema: lo preferido sale antes en cada vuelta de la bolsa (todo sale igual, solo cambia el orden)
_FAMILIA = {"tes": "epico", "wow": "epico", "er": "epico", "gaming": "retro", "spyro": "retro", "n64": "retro", "pokemon": "retro",
            "cod": "militar", "plasti": "jugueton"}
_AFIN = {"epico": {"tinta", "ceniza", "cristal", "rasgado", "volteo", "ventana", "sello", "museo", "carta", "rasgado", "lupa", "pulso",
                   "enfoque", "bisagra", "origami"},
         "retro": {"glitch", "baldosas", "iman", "tiras", "monitor", "cortinilla", "deslizar", "carta", "pop", "brillo", "remolino"},
         "militar": {"monitor", "glitch", "cortinilla", "tiras", "sello", "legajo", "deslizar", "enfoque", "rasgado", "kenburns", "polaroid"},
         "jugueton": {"cae", "sello", "polaroid", "remolino", "iman", "pop", "baldosas", "origami", "vuela", "flota"}}
_POCO = {"epico": {"glitch", "baldosas", "monitor"}, "retro": {"ceniza", "museo", "rasgado"}, "militar": {"museo", "aura"},
         "jugueton": {"glitch", "ceniza", "monitor"}}


# ----------------------------------------------------------------------------------------------------------- utilidades
def _c(u):
    return 0.0 if u <= 0 else 1.0 if u >= 1 else u


def _eo(u):
    u = _c(u)
    return 1 - (1 - u) ** 3


def _ei(u):
    u = _c(u)
    return u * u * u


def _eio(u):
    u = _c(u)
    return u * u * (3 - 2 * u)


def _back(u, k=1.6):
    u = _c(u)
    return 1 + (k + 1) * (u - 1) ** 3 + k * (u - 1) ** 2


def _rebote(u):
    u = _c(u)
    n, d = 7.5625, 2.75
    if u < 1 / d:
        return n * u * u
    if u < 2 / d:
        u -= 1.5 / d
        return n * u * u + .75
    if u < 2.5 / d:
        u -= 2.25 / d
        return n * u * u + .9375
    u -= 2.625 / d
    return n * u * u + .984375


def _elast(u):
    u = _c(u)
    return 1.0 if u >= 1 else 1 - math.exp(-6.5 * u) * math.cos(10 * u)


def _suave(x):
    """smoothstep vectorial de 0..1 (x ya escalado)."""
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def _col(tema):
    return PE.TEMAS.get(tema, PE.TEMAS["tes"])


def _bgr(rgb):
    return np.float32([rgb[2], rgb[1], rgb[0]]) / 255


def _fuente_ruta(nombre, tam):
    for c in (os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"):
        p = os.path.join(c, nombre)
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return T.fuente("Bold Condensed", tam)


def _texto_cabe(d, s, ancho, tam, fuente=None):
    """Fuente que hace caber `s` en `ancho` (encoge, nunca se sale)."""
    f = _fuente_ruta(fuente, tam) if fuente else T.fuente("Bold Condensed", tam)
    w = d.textlength(s, font=f)
    if w > ancho:
        tam = max(14, int(tam * ancho / w))
        f = _fuente_ruta(fuente, tam) if fuente else T.fuente("Bold Condensed", tam)
    return f


_ab = {}


def _abre(ruta):
    """(RGBA recortado si es sin fondo, es_recorte)."""
    if ruta not in _ab:
        im = Image.open(ruta).convert("RGBA")
        a = np.array(im)[..., 3]
        rec = (a < 10).mean() > .12
        if rec:
            bb = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
            if bb:
                im = im.crop(bb)
        _ab[ruta] = (im, rec)
    return _ab[ruta]


def es_recorte(ruta):
    return _abre(ruta)[1]


def _llena(im, rec, w, h, tema, foco=(.5, .35)):
    """La imagen llenando w×h: foto a sangre (fit) o recorte sin fondo sobre un degradado oscuro del tema."""
    if not rec:
        # REGLA 11-nov-2026 (el usuario: «en las tarjetas el personaje sale sin cara… se corta la cabeza»): si la foto es más
        # alta que la tarjeta (personaje de cuerpo entero), el recorte se queda con la parte de ARRIBA, donde está la cara.
        if im.height / im.width > (h / w) * 1.12:
            foco = (foco[0], min(foco[1], .04))
        return ImageOps.fit(im.convert("RGB"), (w, h), Image.LANCZOS, centering=foco)
    t = _col(tema)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h * .45) / (h / 2))
    luz = np.float32(t["luz"]) * .22
    base = np.float32((16, 15, 14))
    fondo = base + (luz - base * 0)[None, None, :] * np.clip(1 - r, 0, 1)[..., None] ** 1.5
    fondo = Image.fromarray(np.clip(fondo, 0, 255).astype(np.uint8)).convert("RGBA")
    k = min(w * .88 / im.width, h * .88 / im.height)
    o = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.LANCZOS)
    fondo.alpha_composite(o, ((w - o.width) // 2, (h - o.height) // 2 + int(h * .02)))
    return fondo.convert("RGB")


def _ruido(h, w, celda, semilla):
    rng = np.random.default_rng(semilla)
    n = rng.random((max(2, h // celda + 2), max(2, w // celda + 2))).astype(np.float32)
    return cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)


def _norm01(a):
    a = a - a.min()
    return a / max(1e-6, a.max())


# ----------------------------------------------------------------------------------------------------------- marcos
class Carta:
    """img RGBA (PIL) + ventana de la foto (para Ken Burns/lupa) + dorso (para volteos)."""

    def __init__(self, img, win=None, wmask=None, src=None, dorso=None, post=None):
        self.img, self.win, self.wmask, self.src, self.dorso, self.post = img, win, wmask, src, dorso, post


def _con_foto(lienzo, src, win, radio=0, post=None):
    x, y, w, h = win
    foto = src.resize((w, h), Image.LANCZOS)
    if post:
        foto = Image.fromarray(post(np.array(foto)))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=radio, fill=255)
    lienzo.paste(foto, (x, y), m)
    return m


def _pildora(d, cx, y, texto, f, fondo, borde, color):
    tw = d.textlength(texto, font=f) + 44
    d.rounded_rectangle((cx - tw / 2, y, cx + tw / 2, y + f.size + 22), radius=(f.size + 22) // 2, fill=fondo, outline=borde, width=2)
    d.text((cx, y + (f.size + 22) / 2), texto, font=f, fill=color, anchor="mm")


def m_clasico(im, rec, titulo, tam, tema):
    """Borde blanco de pegatina (contorno si es recorte) + píldora hueso: la de siempre, ahora en 3D."""
    borde = 12
    k = tam / max(im.size)
    o = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.LANCZOS)
    P = borde * 2
    pie = 34 if titulo else 0
    W, H = o.width + 2 * P, o.height + 2 * P + pie
    al = Image.new("L", (W, H), 0)
    win = wm = src = None
    if rec:
        al.paste(o.getchannel("A"), (P, P))
        al = al.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(2 * borde + 1)).filter(ImageFilter.GaussianBlur(1.2))
    else:
        ImageDraw.Draw(al).rounded_rectangle((P - borde, P - borde, P + o.width + borde, P + o.height + borde), radius=borde * 2, fill=255)
    out = Image.new("RGBA", (W, H), (250, 247, 238, 0))
    out.putalpha(al)
    if rec:
        out.alpha_composite(o, (P, P))
    else:
        src = _llena(im, rec, int(o.width * 1.3), int(o.height * 1.3), tema)
        win = (P, P, o.width, o.height)
        wm = _con_foto(out, src, win, radio=borde)
    dorso = Image.new("RGBA", (W, H), (232, 228, 218, 0))
    dorso.putalpha(al)
    if titulo:
        d = ImageDraw.Draw(out)
        f = _texto_cabe(d, titulo.upper(), W - 60, 34)     # la píldora nunca más ancha que la tarjeta (Franclorn, 11-nov-2026)
        _pildora(d, W / 2, H - 58, titulo.upper(), f, (18, 16, 14, 235), T.HUESO + (255,), T.HUESO + (255,))
    return Carta(out, win, wm, src, dorso)


def _grano(w, h, base, fuerza=10, semilla=3):
    n = _ruido(h, w, 3, semilla) - .5
    a = np.clip(np.float32(base)[None, None, :] + n[..., None] * fuerza, 0, 255).astype(np.uint8)
    return Image.fromarray(a).convert("RGBA")


def m_polaroid(im, rec, titulo, tam, tema):
    """Foto instantánea con pie ancho escrito a mano y una cinta adhesiva translúcida arriba."""
    t = _col(tema)
    W = int(tam * .86)
    m = int(W * .06)
    pw, ph = W - 2 * m, int((W - 2 * m) * .94)
    pie = int(W * .25) if titulo else int(W * .12)
    oh = int(W * .05)
    H = oh + m + ph + pie
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(_grano(W, H - oh, (246, 243, 234), 9), (0, oh))
    src = _llena(im, rec, int(pw * 1.3), int(ph * 1.3), tema)
    win = (m, oh + m, pw, ph)
    wm = _con_foto(out, src, win)
    d = ImageDraw.Draw(out)
    d.rectangle((m - 1, oh + m - 1, m + pw, oh + m + ph), outline=(0, 0, 0, 50), width=1)
    if titulo:
        f = _texto_cabe(d, titulo, pw * .96, int(W * .115), "Inkfree.ttf")
        d.text((W / 2, oh + m + ph + pie * .5), titulo, font=f, fill=t["tinta"] + (255,), anchor="mm")
    cinta = Image.new("RGBA", (int(W * .38), int(W * .1)), (238, 228, 196, 150))
    cd = ImageDraw.Draw(cinta)
    for x in range(0, cinta.width, 7):                     # bordes dentados de cinta cortada a mano
        cd.polygon([(x, 0), (x + 3.5, 4), (x + 7, 0)], fill=(0, 0, 0, 0))
        cd.polygon([(x, cinta.height), (x + 3.5, cinta.height - 4), (x + 7, cinta.height)], fill=(0, 0, 0, 0))
    cinta = cinta.rotate(4, expand=True, resample=Image.BICUBIC)
    out.alpha_composite(cinta, ((W - cinta.width) // 2, 0))
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dorso.paste(_grano(W, H - oh, (230, 226, 214), 14, 9), (0, oh))
    dd = ImageDraw.Draw(dorso)
    for y in range(oh + 30, H - 20, 26):
        dd.line((24, y, W - 24, y), fill=(200, 194, 178, 255), width=1)
    return Carta(out, win, wm, src, dorso)


def m_carta(im, rec, titulo, tam, tema):
    """Carta coleccionable: marco oscuro con filo de luz del tema, cinta con el nombre, gema y dorso con anillo de runas."""
    t = _col(tema)
    W = int(tam * .76)
    H = int(W * 1.38)
    r = int(W * .05)
    b = int(W * .045)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((0, 0, W - 1, H - 1), r, fill=(16, 14, 12, 255), outline=t["luz"] + (255,), width=max(4, W // 60))
    d.rounded_rectangle((b, b, W - 1 - b, H - 1 - b), max(2, r - b // 2), outline=t["luz"] + (150,), width=2)
    y = int(b * 1.8)
    if titulo:
        bh = int(W * .13)
        cinta = np.zeros((bh, W - 2 * y, 4), np.uint8)
        g = np.linspace(1.18, .78, bh)[:, None, None]
        cinta[..., :3] = np.clip(np.float32(t["luz"]) * g, 0, 255).astype(np.uint8)
        cinta[..., 3] = 255
        out.paste(Image.fromarray(cinta, "RGBA"), (y, y))
        f = _texto_cabe(d, titulo.upper(), (W - 2 * y) * .9, int(bh * .62))
        d.text((W / 2, y + bh / 2), titulo.upper(), font=f, fill=t["tinta"] + (255,), anchor="mm")
        y += bh + int(b * .7)
    pie = int(W * .15)
    win = (int(b * 1.8), y, W - int(b * 3.6), H - y - pie)
    src = _llena(im, rec, int(win[2] * 1.3), int(win[3] * 1.3), tema)
    wm = _con_foto(out, src, win, radio=6)
    d.rectangle((win[0] - 2, win[1] - 2, win[0] + win[2] + 1, win[1] + win[3] + 1), outline=t["luz"] + (200,), width=2)
    cy, cx, g = H - pie / 2 - b * .3, W / 2, W * .045
    d.line((W * .18, cy, cx - g * 1.8, cy), fill=t["luz"] + (200,), width=2)
    d.line((cx + g * 1.8, cy, W * .82, cy), fill=t["luz"] + (200,), width=2)
    d.polygon([(cx, cy - g), (cx + g, cy), (cx, cy + g), (cx - g, cy)], fill=t["rojo"] + (255,), outline=t["luz"] + (255,))
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dorso)
    dd.rounded_rectangle((0, 0, W - 1, H - 1), r, fill=(20, 17, 14, 255), outline=t["luz"] + (255,), width=max(4, W // 60))
    for k in range(-H, W + H, 22):                       # celosía en diagonal
        dd.line((k, 0, k + H, H), fill=t["luz"] + (34,), width=2)
        dd.line((k + H, 0, k, H), fill=t["luz"] + (34,), width=2)
    an = PE._anillo(int(W * .8), W * .34, tema)
    dorso.alpha_composite(an, ((W - an.width) // 2, (H - an.height) // 2))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), r, fill=255)
    dorso.putalpha(Image.fromarray(np.minimum(np.array(dorso.getchannel("A")), np.array(m))))
    return Carta(out, win, wm, src, dorso)


def m_cristal(im, rec, titulo, tam, tema):
    """Panel de cristal ahumado translúcido (el clip se ve detrás), filo de luz y reflejo arriba."""
    t = _col(tema)
    W = int(tam * .9)
    pad = int(W * .05)
    pw, ph = W - 2 * pad, int((W - 2 * pad) * .78)
    th = int(W * .14) if titulo else 0
    H = 2 * pad + ph + th
    rr = int(W * .05)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), rr, fill=255)
    panel = np.zeros((H, W, 4), np.uint8)
    panel[..., :3] = (18, 16, 14)
    g = np.clip(1 - np.arange(H) / (H * .45), 0, 1)[:, None] ** 2
    panel[..., :3] = np.clip(panel[..., :3] + g[..., None] * 44, 0, 255).astype(np.uint8)
    panel[..., 3] = (np.array(m) * (170 / 255)).astype(np.uint8)
    out = Image.fromarray(panel, "RGBA")
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((0, 0, W - 1, H - 1), rr, outline=t["luz"] + (225,), width=2)
    d.rounded_rectangle((3, 3, W - 4, H - 4), rr - 2, outline=(255, 255, 255, 60), width=1)
    win = (pad, pad, pw, ph)
    src = _llena(im, rec, int(pw * 1.3), int(ph * 1.3), tema)
    wm = _con_foto(out, src, win, radio=int(W * .035))
    if titulo:
        f = _texto_cabe(d, titulo.upper(), pw * .92, int(th * .58))
        d.text((W / 2, pad + ph + th * .55), titulo.upper(), font=f, fill=t["luz"] + (255,), anchor="mm")
    dorso = Image.fromarray(panel.copy(), "RGBA")
    an = PE._anillo(int(min(W, H) * .8), min(W, H) * .32, tema)
    dorso.alpha_composite(_alfa_pil(an, .5), ((W - an.width) // 2, (H - an.height) // 2))
    return Carta(out, win, wm, src, dorso)


def _alfa_pil(im, k):
    a = np.array(im)
    a[..., 3] = (a[..., 3] * k).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def m_rasgado(im, rec, titulo, tam, tema):
    """Recorte de papel con borde rasgado: la foto impresa en tono cálido y el nombre a mano."""
    t = _col(tema)
    W = int(tam * .88)
    pad = int(W * .085)
    pw, ph = W - 2 * pad, int((W - 2 * pad) * .8)
    th = int(W * .16) if titulo else int(W * .05)
    H = pad + ph + th + int(pad * .6)
    out = PE._papel(W, H, tema, semilla=len(titulo or "") + 5)
    src = _llena(im, rec, int(pw * 1.3), int(ph * 1.3), tema)

    def calido(a):
        f = a.astype(np.float32)
        l = f.mean(axis=2, keepdims=True)
        sep = l * np.float32([1.07, .95, .78])
        return np.clip(f * .78 + sep * .22, 0, 255).astype(np.uint8)
    win = (pad, pad, pw, ph)
    wm = _con_foto(out, src, win, post=calido)
    d = ImageDraw.Draw(out)
    d.rectangle((pad - 2, pad - 2, pad + pw + 1, pad + ph + 1), outline=t["tinta"] + (255,), width=2)
    if titulo:
        f = _texto_cabe(d, titulo, pw * .94, int(th * .62), "segoeprb.ttf")
        d.text((W / 2, pad + ph + th * .52), titulo, font=f, fill=t["tinta"] + (255,), anchor="mm")
    dorso = PE._papel(W, H, tema, semilla=31).transpose(Image.FLIP_LEFT_RIGHT)
    return Carta(out, win, wm, src, dorso, post=calido)


def m_museo(im, rec, titulo, tam, tema):
    """Cuadro de museo: moldura biselada del color de luz del tema, paspartú y placa de metal con el nombre."""
    t = _col(tema)
    W = int(tam * .92)
    fr, pp = int(W * .085), int(W * .028)
    pw = W - 2 * (fr + pp)
    ph = int(pw * .82)
    Hc = ph + 2 * (fr + pp)
    placa = int(W * .1) if titulo else 0
    H = Hc + (int(placa * .55) if titulo else 0)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    luz = np.float32(t["luz"])
    tono = lambda k: tuple(int(v) for v in np.clip(luz * k, 0, 255)) + (255,)
    d.polygon([(0, 0), (W, 0), (W - fr, fr), (fr, fr)], fill=tono(1.12))                 # arriba: luz
    d.polygon([(0, 0), (fr, fr), (fr, Hc - fr), (0, Hc)], fill=tono(.92))                 # izquierda
    d.polygon([(W, 0), (W, Hc), (W - fr, Hc - fr), (W - fr, fr)], fill=tono(.62))         # derecha: sombra
    d.polygon([(0, Hc), (fr, Hc - fr), (W - fr, Hc - fr), (W, Hc)], fill=tono(.5))        # abajo
    a = np.array(out).astype(np.float32)
    n = _ruido(H, W, 2, 12)[..., None] - .5
    a[..., :3] = np.clip(a[..., :3] * (1 + n * .22), 0, 255)
    out = Image.fromarray(a.astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(out)
    for k, c in ((0, (30, 22, 14, 255)), (fr * .45, tono(1.3)), (fr - 1, (30, 22, 14, 255))):
        d.rectangle((k, k, W - 1 - k, Hc - 1 - k), outline=c, width=2)
    d.rectangle((fr, fr, W - fr - 1, Hc - fr - 1), fill=(236, 228, 208, 255))
    win = (fr + pp, fr + pp, pw, ph)
    src = _llena(im, rec, int(pw * 1.3), int(ph * 1.3), tema)
    wm = _con_foto(out, src, win)
    sombra = np.zeros((ph, pw, 4), np.uint8)                # sombra interior: la foto se hunde en el paspartú
    yy, xx = np.mgrid[0:ph, 0:pw]
    sombra[..., 3] = (np.clip(1 - np.minimum(xx, yy) / (pw * .05), 0, 1) ** 2 * 120).astype(np.uint8)
    out.alpha_composite(Image.fromarray(sombra, "RGBA"), win[:2])
    if titulo:
        d = ImageDraw.Draw(out)
        pw2 = int(W * .62)
        x0, y0 = (W - pw2) // 2, Hc - int(placa * .45)
        pl = np.zeros((placa, pw2, 4), np.uint8)
        pl[..., :3] = np.clip(luz * np.linspace(1.25, .8, placa)[:, None, None], 0, 255).astype(np.uint8)
        pl[..., 3] = 255
        msk = Image.new("L", (pw2, placa), 0)
        ImageDraw.Draw(msk).rounded_rectangle((0, 0, pw2 - 1, placa - 1), 6, fill=255)
        out.paste(Image.fromarray(pl, "RGBA"), (x0, y0), msk)
        d.rounded_rectangle((x0, y0, x0 + pw2 - 1, y0 + placa - 1), 6, outline=(40, 30, 18, 255), width=2)
        for sx in (x0 + 12, x0 + pw2 - 12):
            d.ellipse((sx - 4, y0 + placa / 2 - 4, sx + 4, y0 + placa / 2 + 4), fill=(60, 46, 28, 255))
        f = _texto_cabe(d, titulo.upper(), pw2 - 50, int(placa * .58))
        d.text((W / 2, y0 + placa / 2), titulo.upper(), font=f, fill=(34, 24, 14, 255), anchor="mm")
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dorso)
    dd.rectangle((0, 0, W - 1, Hc - 1), fill=(92, 66, 42, 255), outline=(50, 34, 20, 255), width=6)
    for y in range(12, Hc, 18):
        dd.line((8, y, W - 8, y + 4), fill=(78, 56, 36, 255), width=2)
    return Carta(out, win, wm, src, dorso)


def m_monitor(im, rec, titulo, tam, tema):
    """Pantallita con bisel oscuro, líneas de barrido, esquinas de HUD y etiqueta del nombre (gaming, CoD, retro)."""
    t = _col(tema)
    W = int(tam * .92)
    bz = int(W * .045)
    pw, ph = W - 2 * bz, int((W - 2 * bz) * .64)
    tg = int(W * .1) if titulo else 0
    H = tg + ph + 2 * bz + int(W * .03)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    y0 = tg
    d.rounded_rectangle((0, y0, W - 1, H - 1), int(W * .04), fill=(28, 29, 33, 255), outline=(70, 72, 80, 255), width=2)
    d.line((int(W * .05), y0 + 3, int(W * .95), y0 + 3), fill=(110, 112, 120, 255), width=2)
    luz = t["luz"]

    def barrido(a):
        f = a.astype(np.float32)
        f[1::3] *= .74
        hh, ww = f.shape[:2]
        yy, xx = np.mgrid[0:hh, 0:ww]
        v = 1 - .35 * np.clip(np.hypot((xx - ww / 2) / (ww / 2), (yy - hh / 2) / (hh / 2)) - .6, 0, 1)
        f *= v[..., None]
        o = np.clip(f, 0, 255).astype(np.uint8)
        L = max(10, ww // 12)
        for (x, y, sx, sy) in ((6, 6, 1, 1), (ww - 7, 6, -1, 1), (6, hh - 7, 1, -1), (ww - 7, hh - 7, -1, -1)):
            cv2.line(o, (x, y), (x + sx * L, y), luz, 3)
            cv2.line(o, (x, y), (x, y + sy * L), luz, 3)
        return o
    win = (bz, y0 + bz, pw, ph)
    src = _llena(im, rec, int(pw * 1.3), int(ph * 1.3), tema)
    wm = _con_foto(out, src, win, radio=8, post=barrido)
    d.ellipse((W - bz * 2.6, H - bz * 1.55, W - bz * 1.6, H - bz * .55), fill=luz + (255,))
    if titulo:
        f = _texto_cabe(d, titulo.upper(), W * .7, int(tg * .62))
        tw = d.textlength(titulo.upper(), font=f) + 40
        d.polygon([(0, 0), (tw, 0), (tw + tg * .6, tg), (0, tg)], fill=luz + (255,))
        d.text((20, tg / 2), titulo.upper(), font=f, fill=t["tinta"] + (255,), anchor="lm")
    dorso = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dorso)
    dd.rounded_rectangle((0, y0, W - 1, H - 1), int(W * .04), fill=(36, 37, 42, 255), outline=(70, 72, 80, 255), width=2)
    for k in range(6):
        yy = y0 + H * .25 + k * 14
        dd.line((W * .3, yy, W * .7, yy), fill=(18, 18, 20, 255), width=5)
    return Carta(out, win, wm, src, dorso, post=barrido)


def m_aura(im, rec, titulo, tam, tema):
    """Solo recortes sin fondo: la figura con halo de luz del tema y sombra oscura detrás; dorso = silueta de luz."""
    if not rec:
        return m_cristal(im, rec, titulo, tam, tema)
    t = _col(tema)
    k = tam / max(im.size)
    o = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    M = int(tam * .1)
    pie = 64 if titulo else 0
    W, H = o.width + 2 * M, o.height + 2 * M + pie
    mk = Image.new("L", (W, H), 0)
    mk.paste(o.getchannel("A"), (M, M))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste((0, 0, 0, 255), mask=mk.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .55)))
    out.paste(t["luz"] + (255,), mask=mk.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * .7)))
    out.alpha_composite(o, (M, M))
    if titulo:
        d = ImageDraw.Draw(out)
        f = _texto_cabe(d, titulo.upper(), W * .9, 34)
        _pildora(d, W / 2, H - 60, titulo.upper(), f, (10, 9, 8, 230), t["luz"] + (255,), t["texto"] + (255,))
    dorso = Image.new("RGBA", (W, H), t["luz"] + (0,))
    dorso.putalpha(mk.filter(ImageFilter.MaxFilter(5)))
    return Carta(out, None, None, None, dorso)


MARCOS = dict(clasico=m_clasico, polaroid=m_polaroid, carta=m_carta, cristal=m_cristal, rasgado=m_rasgado, museo=m_museo,
              monitor=m_monitor, aura=m_aura)


# ----------------------------------------------------------------------------------------------------------- lienzo 3D
def _prem(pil):
    """PIL RGBA -> float32 BGRA premultiplicado 0..1."""
    a = np.asarray(pil.convert("RGBA"), np.float32)[..., [2, 1, 0, 3]] / 255
    a[..., :3] *= a[..., 3:4]
    return np.ascontiguousarray(a)


def _rot(rx, ry, rz):
    rx, ry, rz = math.radians(rx), math.radians(ry), math.radians(rz)
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def _pose(**kw):
    p = dict(x=0.0, y=0.0, z=0.0, s=1.0, sx=1.0, sy=1.0, rx=0.0, ry=0.0, rz=0.0, a=1.0, px=0.0, py=0.0, alt=0.0, sombra=1.0, sdx=0.0)
    p.update(kw)
    return p


def _quad(w, h, x0=None, y0=None, x1=None, y1=None):
    """Esquinas (TL, TR, BR, BL) en coordenadas de carta centradas, z=0. Sin args = la carta entera."""
    if x0 is None:
        x0, y0, x1, y1 = 0, 0, w, h
    return np.array([[x0 - w / 2, y0 - h / 2, 0], [x1 - w / 2, y0 - h / 2, 0], [x1 - w / 2, y1 - h / 2, 0], [x0 - w / 2, y1 - h / 2, 0]], float)


def _gira2d(q, ang, cx, cy):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    q = q.copy()
    x, y = q[:, 0] - cx, q[:, 1] - cy
    q[:, 0], q[:, 1] = cx + c * x - s * y, cy + s * x + c * y
    return q


_BUF = {}


def _u8_recto(img, relleno=None):
    """float premultiplicado 0..1 -> uint8 BGRA con alfa recta. `relleno` (uint8 BGR del mismo tamaño) pinta el color de los
    píxeles transparentes: así la interpolación del borde no mete un filo negro."""
    a = cv2.max(img[..., 3], 1e-4)
    o = cv2.convertScaleAbs(cv2.divide(img, cv2.merge((a, a, a, np.ones_like(a))), scale=255.0))
    if relleno is not None:
        m = img[..., 3] < .004
        o[..., :3][m] = relleno[m]
    return o


def _sangra(img):
    """Color de los vecinos opacos para los píxeles transparentes (uint8 BGR)."""
    a = img[..., 3]
    b = cv2.blur(img, (15, 15))
    ab = cv2.max(b[..., 3], 1e-4)
    rgb = b[..., :3] / ab[..., None]
    return np.clip(rgb * 255, 0, 255).astype(np.uint8)


class _Lienzo:
    """Búfer BGRA uint8 (alfa recta) compartido: proyecta capas (imagen + 4 esquinas 3D) con perspectiva y las mezcla con
    cv2.blendLinear (8-10x más rápido que mezclar en float)."""

    def _lienzo(self, CW, CH):
        self.CW, self.CH = -(-CW // 128) * 128, -(-CH // 128) * 128     # múltiplos de 128: varias pegatinas comparten búfer
        self._bb = None

    def _limpia(self):
        k = (self.CH, self.CW)
        if k not in _BUF:
            _BUF[k] = np.zeros((self.CH, self.CW, 4), np.uint8)
        self._L = _BUF[k]
        self._bb = None

    def proy(self, pts, pose, w, h):
        piv = np.array([pose["px"] * w, pose["py"] * h, 0.0])
        p = pts - piv
        p = p * np.array([pose["s"] * pose["sx"], pose["s"] * pose["sy"], pose["s"]])
        p = p @ _rot(pose["rx"], pose["ry"], pose["rz"]).T + piv
        p = p + np.array([pose["x"], pose["y"], pose["z"]])
        k = FOCAL / np.maximum(60.0, FOCAL + p[:, 2])
        return np.stack([self.CW / 2 + p[:, 0] * k, self.CH / 2 + p[:, 1] * k], 1)

    def _u8(self, img):
        return _u8_recto(img)

    def mezcla(self, o, x0, y0):
        """Pone la capa uint8 `o` encima del búfer en (x0, y0) (operador «over» con alfa recta)."""
        h, w = o.shape[:2]
        x1, y1 = min(self.CW, x0 + w), min(self.CH, y0 + h)
        sx, sy = max(0, -x0), max(0, -y0)
        x0, y0 = max(0, x0), max(0, y0)
        if x1 - x0 < 1 or y1 - y0 < 1:
            return
        o = o[sy:sy + y1 - y0, sx:sx + x1 - x0]
        r = self._L[y0:y1, x0:x1]
        b = self._bb
        if b is None or x0 >= b[2] or x1 <= b[0] or y0 >= b[3] or y1 <= b[1]:
            r[...] = o                                  # búfer vacío ahí: copia directa
        else:
            oa = o[..., 3].astype(np.float32) * (1 / 255)
            w2 = cv2.multiply(r[..., 3].astype(np.float32) * (1 / 255), 1 - oa)
            res = cv2.blendLinear(np.ascontiguousarray(o), np.ascontiguousarray(r), oa, w2)
            res[..., 3] = cv2.convertScaleAbs(cv2.add(oa, w2), alpha=255)
            r[...] = res
        self._bb = (x0, y0, x1, y1) if b is None else (min(b[0], x0), min(b[1], y0), max(b[2], x1), max(b[3], y1))

    def dibuja(self, img, q, pose, w, h, a=1.0, luz=1.0, dst=None):
        if a <= .003:
            return
        if dst is None:
            dst = self.proy(q, pose, w, h)
        x0, y0 = int(max(0, math.floor(dst[:, 0].min()))), int(max(0, math.floor(dst[:, 1].min())))
        x1, y1 = int(min(self.CW, math.ceil(dst[:, 0].max()) + 1)), int(min(self.CH, math.ceil(dst[:, 1].max()) + 1))
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        if img.dtype != np.uint8:
            img = self._u8(img)
        ih, iw = img.shape[:2]
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [iw, 0], [iw, ih], [0, ih]]), dst.astype(np.float32))
        M = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]], float) @ M
        o = cv2.warpPerspective(img, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        if luz != 1 or a < 1:
            o = cv2.multiply(o, (luz, luz, luz, a))
        self.mezcla(o, x0, y0)

    def _bgra(self):
        out = np.zeros((self.CH, self.CW, 4), np.uint8)
        if self._bb:
            x0, y0, x1, y1 = self._bb
            out[y0:y1, x0:x1] = self._L[y0:y1, x0:x1]
            self._L[y0:y1, x0:x1] = 0                  # el búfer queda limpio para la siguiente pegatina
        self._bb = None
        return out


def _capa_trazo(L, x0, y0, x1, y1):
    x0, y0 = int(math.floor(x0)), int(math.floor(y0))
    return x0, y0, np.zeros((max(1, int(math.ceil(y1)) - y0), max(1, int(math.ceil(x1)) - x0), 4), np.uint8)


def _linea(L, pts, color, a, grosor):
    """Polilínea (color BGR 0..1, opacidad a) encima del búfer."""
    if a <= .003 or len(pts) < 2:
        return
    x0, y0, cap = _capa_trazo(L, pts[:, 0].min() - grosor - 2, pts[:, 1].min() - grosor - 2, pts[:, 0].max() + grosor + 3, pts[:, 1].max() + grosor + 3)
    c = tuple(float(v) * 255 for v in color) + (255.0 * float(a),)
    cv2.polylines(cap, [np.round(pts - [x0, y0]).astype(np.int32)], False, c, grosor, cv2.LINE_AA)
    L.mezcla(cap, x0, y0)


def _punto(L, x, y, r, color, a):
    if a <= .003 or r < .5:
        return
    x0, y0, cap = _capa_trazo(L, x - r - 2, y - r - 2, x + r + 3, y + r + 3)
    c = tuple(float(v) * 255 for v in color) + (255.0 * float(a),)
    cv2.circle(cap, (int(x) - x0, int(y) - y0), max(1, int(r)), c, -1, cv2.LINE_AA)
    L.mezcla(cap, x0, y0)


# ----------------------------------------------------------------------------------------------------------- la pegatina
class Pegatina(_Lienzo):
    """fn(dt, dur, marcas) -> BGRA, como los MG. Se prepara la primera vez que se dibuja (el FX se arma barato al importar)."""

    def __init__(self, ruta, titulo=None, tam=400, tema="tes", entrada="cae", estancia="flota", salida="vuela", marco="polaroid",
                 semilla=0, lado=None, giro=None, te=.7, ts=.5):
        self.ruta, self.titulo, self.tam, self.tema = ruta, titulo, tam, tema
        self.entrada, self.estancia, self.salida, self.marco = entrada, estancia, salida, marco
        self.semilla = semilla
        rnd = random.Random(semilla * 7919 + 13)
        self.lado = lado if lado is not None else rnd.choice((-1, 1))
        self.giro = giro if giro is not None else rnd.uniform(-6, 6)
        self.fase = rnd.uniform(0, 6.28)
        self.rnd = rnd
        self.te, self.ts = te, ts
        self.anim = "%s+%s+%s/%s" % (entrada, estancia, salida, marco)
        self._listo = False

    def __repr__(self):
        return "<pegatina %s %s>" % (os.path.basename(self.ruta), self.anim)

    # ---------------------------------------------------------------- preparación
    def _prepara(self):
        im, rec = _abre(self.ruta)
        marco = self.marco
        if marco == "aura" and not rec:
            marco = "cristal"
        c = MARCOS[marco](im, rec, self.titulo, self.tam, self.tema)
        self.carta = c
        self.img = _prem(c.img)
        self.h, self.w = self.img.shape[:2]
        self.dorso = cv2.flip(_prem(c.dorso), 1) if c.dorso is not None else None
        if c.win:
            self.src = np.asarray(c.src, np.uint8)
            self.wm = np.asarray(c.wmask, np.float32)[..., None] / 255
        SP = int(max(self.w, self.h) * .07) + 6
        al = np.zeros((self.h + 2 * SP, self.w + 2 * SP), np.float32)
        al[SP:SP + self.h, SP:SP + self.w] = self.img[..., 3]
        al = cv2.GaussianBlur(al, (0, 0), SP / 2.6)
        self.sombra_img = np.dstack([np.zeros_like(al)] * 3 + [al])
        self.SP = SP
        self.relleno = _sangra(self.img)
        self.img_u8 = _u8_recto(self.img, self.relleno)
        self.dorso_u8 = _u8_recto(self.dorso, _sangra(self.dorso)) if self.dorso is not None else None
        self.sombra_u8 = _u8_recto(self.sombra_img)
        self._lienzo(int(self.w * 3.0) + 200, int(self.h * 2.5) + 200)
        t = _col(self.tema)
        self.c_luz, self.c_tinta, self.c_rojo, self.c_papel = _bgr(t["luz"]), _bgr(t["tinta"]), _bgr(t["rojo"]), _bgr(t["papel"])
        self._cache = {}
        self._listo = True

    def _u8(self, img):
        if img is self.img:
            return self.img_u8
        if img is self.dorso:
            return self.dorso_u8
        if img is self.sombra_img:
            return self.sombra_u8
        return _u8_recto(img, self.relleno if img.shape[:2] == self.img.shape[:2] else None)

    def _campo(self, clave, fn):
        if clave not in self._cache:
            self._cache[clave] = fn()
        return self._cache[clave]

    def _con_ventana(self, img, zoom, cx, cy):
        x, y, w, h = self.carta.win
        Hs, Ws = self.src.shape[:2]
        cw, ch = Ws / zoom, Hs / zoom
        x0 = min(max(0, Ws / 2 - cw / 2 + cx * Ws), Ws - cw)
        y0 = min(max(0, Hs / 2 - ch / 2 + cy * Hs), Hs - ch)
        M = np.float32([[cw / w, 0, x0], [0, ch / h, y0]])
        foto = cv2.warpAffine(self.src, M, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
        if self.carta.post:
            foto = self.carta.post(foto)
        f = foto[..., ::-1].astype(np.float32) / 255
        o = img.copy()
        r = o[y:y + h, x:x + w]
        r[..., :3] = r[..., :3] * (1 - self.wm) + f * self.wm
        return o

    # ---------------------------------------------------------------- cuadro
    def __call__(self, dt, dur, marcas=()):
        if not self._listo:
            self._prepara()
        self._limpia()
        if dt < 0:
            return self._bgra()
        te, ts = min(self.te, dur * .42), min(self.ts, dur * .3)
        pose = _pose()
        self.atras, self.delante = [], []
        img = EST[self.estancia](self, self.img, pose, dt, dur)
        capas = None
        if dt < te:
            capas = ENT[self.entrada](self, img, dt / te, False, pose)
        elif dt > dur - ts:
            capas = SAL[self.salida](self, img, max(0.0, (dur - dt) / ts), True, pose)
        if capas is None:
            capas = [dict(img=img, q=_quad(self.w, self.h), sombra=True)]
        for f in self.atras:
            f(self, pose)
        w, h = self.w, self.h
        for c in capas:
            if c.get("sombra") and pose["sombra"] > 0:
                ps = dict(pose)
                alt = pose["alt"]
                ps["x"] += 10 + 46 * alt + pose["sdx"]
                ps["y"] += 16 + 64 * alt
                ps["s"] *= 1 + .05 * alt
                ps["z"] += 0
                q = _quad(w, h)
                q[:, :2] *= np.array([(w + 2 * self.SP) / w, (h + 2 * self.SP) / h])
                self.dibuja(self.sombra_img, c.get("qs", q), ps, w, h, a=.62 * (1 - .45 * min(1, alt)) * pose["a"] * pose["sombra"] * c.get("a", 1))
            im = c["img"]
            if c.get("sombra") and self.dorso is not None:       # cara de atrás visible (volteos, bisagras)
                d = self.proy(c["q"], pose, w, h)
                cruz = (d[1, 0] - d[0, 0]) * (d[3, 1] - d[0, 1]) - (d[1, 1] - d[0, 1]) * (d[3, 0] - d[0, 0])
                if cruz < 0:
                    im = self.dorso
                self.dibuja(im, c["q"], pose, w, h, a=pose["a"] * c.get("a", 1), luz=c.get("luz", 1), dst=d)
            else:
                self.dibuja(im, c["q"], pose, w, h, a=pose["a"] * c.get("a", 1), luz=c.get("luz", 1))
        for f in self.delante:
            f(self, pose)
        return self._bgra()


# ----------------------------------------------------------------------------------------------------------- estancias
def es_flota(P, img, pose, dt, dur):
    pose["rz"] += P.giro + 2.0 * math.sin(dt * 2.1 + P.fase)
    pose["y"] += 7 * math.sin(dt * 1.7 + P.fase)
    pose["s"] *= 1 + .02 * math.sin(dt * 3.0)
    return img


def _brillo(P, img, pos, ancho=.12, fuerza=.55):
    D = P._campo("diag", lambda: ((np.arange(P.w)[None, :] + np.arange(P.h)[:, None] * .6) / (P.w + P.h * .6)).astype(np.float32))
    if not -.3 < pos < 1.3:
        return img
    b = np.exp(-((D - pos) / ancho) ** 2) * fuerza
    o = img.copy()
    o[..., :3] = np.minimum(o[..., 3:4], o[..., :3] + (b * o[..., 3])[..., None])
    return o


def es_inclina(P, img, pose, dt, dur):
    """Cartón que respira en 3D: inclina en X/Y y el reflejo se desliza con la inclinación."""
    ry = 10 * math.sin(dt * 1.05 + P.fase)
    pose["ry"] += ry
    pose["rx"] += 6 * math.sin(dt * .8 + P.fase * 1.3)
    pose["rz"] += P.giro * .5
    return _brillo(P, img, .5 + ry / 22, .22, .16)


def es_kenburns(P, img, pose, dt, dur):
    """La foto se acerca y se pasea DENTRO del marco quieto (si el marco no tiene ventana: flota)."""
    if not P.carta.win:
        return es_flota(P, img, pose, dt, dur)
    u = min(1.0, dt / max(1.0, dur))
    pose["rz"] += P.giro * .6 + .8 * math.sin(dt * 1.3 + P.fase)
    pose["y"] += 4 * math.sin(dt * 1.5 + P.fase)
    return P._con_ventana(img, 1 + .2 * u, P.lado * .05 * u, -.04 * u)


def es_brillo(P, img, pose, dt, dur):
    """Destello de luz que barre la pegatina cada ~2,4 s (como carta brillante)."""
    es_flota(P, img, pose, dt * .6, dur)
    pos = ((dt - .5) % 2.4) / .75 * 1.6 - .3
    return _brillo(P, img, pos, .09, .65)


def es_lupa(P, img, pose, dt, dur):
    """Una lupa con aro del tema se pasea por la imagen y aumenta el detalle (x2)."""
    pose["rz"] += P.giro * .4
    w, h = P.w, P.h
    if P.carta.win:
        wx, wy, ww, wh = P.carta.win
    else:
        wx, wy, ww, wh = 0, 0, w, h
    R = int(min(ww, wh) * .24)
    cx = wx + ww / 2 + (ww / 2 - R * .9) * math.sin(dt * .9 + P.fase)
    cy = wy + wh / 2 + (wh / 2 - R * .9) * math.sin(dt * 1.37 + P.fase * .7)
    M = np.float32([[2, 0, -cx], [0, 2, -cy]])
    M[0, 2], M[1, 2] = cx - 2 * cx, cy - 2 * cy
    zoom = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR)
    yy, xx = np.ogrid[0:h, 0:w]
    m = _suave((R - np.hypot(xx - cx, yy - cy)) / 2.5)[..., None].astype(np.float32)
    o = img * (1 - m) + zoom * m
    cv2.circle(o, (int(cx), int(cy)), R + 4, (0.04, 0.04, 0.04, 1), 9, cv2.LINE_AA)
    cv2.circle(o, (int(cx), int(cy)), R + 4, tuple(float(v) for v in P.c_luz) + (1,), 4, cv2.LINE_AA)
    cv2.ellipse(o, (int(cx - R * .25), int(cy - R * .3)), (int(R * .5), int(R * .32)), -35, 200, 290, (.9, .9, .9, .9), 3, cv2.LINE_AA)
    lado = R + 6

    def mango(L, pose_):
        a = math.radians(45)
        p0 = np.array([[cx + lado * math.cos(a) - w / 2, cy + lado * math.sin(a) - h / 2, 0],
                       [cx + (lado + R * 1.1) * math.cos(a) - w / 2, cy + (lado + R * 1.1) * math.sin(a) - h / 2, 0]])
        d = L.proy(p0, pose_, w, h)
        _linea(L, d, (0.05, 0.05, 0.05), 1, 16)
        _linea(L, d, P.c_luz * .8, 1, 9)
    P.delante.append(mango)
    return o


def es_quieta(P, img, pose, dt, dur):
    """Casi quieta, con un acercamiento lento: para tonos serios."""
    pose["rz"] += P.giro * .35
    pose["s"] *= 1 + .035 * min(1.0, dt / max(1.0, dur))
    return img


def es_pulso(P, img, pose, dt, dur):
    """Halo de luz del tema que late detrás de la pegatina."""
    es_flota(P, img, pose, dt * .7, dur)
    halo = P._campo("halo", lambda: _halo(P))
    k = .75 + .25 * math.sin(dt * 3.2)

    def dibuja(L, pose_):
        q = _quad(P.w, P.h)
        q[:, :2] *= 1.2 + .05 * math.sin(dt * 3.2)
        L.dibuja(halo, q, pose_, P.w, P.h, a=k * pose_["a"])
    P.atras.append(dibuja)
    return img


def _halo(P):
    a = cv2.resize(P.img[..., 3], None, fx=1 / 1.18, fy=1 / 1.18)
    H, W = P.h, P.w
    al = np.zeros((H, W), np.float32)
    y0, x0 = (H - a.shape[0]) // 2, (W - a.shape[1]) // 2
    al[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
    al = cv2.GaussianBlur(cv2.dilate(al, np.ones((15, 15))), (0, 0), max(W, H) * .04)
    al = np.clip(al * 1.6, 0, 1)
    return _u8_recto(np.dstack([al * P.c_luz[0], al * P.c_luz[1], al * P.c_luz[2], al]).astype(np.float32))


EST = dict(flota=es_flota, inclina=es_inclina, kenburns=es_kenburns, brillo=es_brillo, lupa=es_lupa, quieta=es_quieta, pulso=es_pulso)


# ----------------------------------------------------------------------------------------------------------- transiciones
# f(P, img, u, fuera, pose) -> capas | None. u = 1 visible del todo, 0 oculto (en la salida u baja de 1 a 0).
def t_pop(P, img, u, fuera, pose):
    s = T._pop(u * .42, .42) if not fuera else _eio(u)
    pose["s"] *= max(.02, s)
    pose["rz"] += (1 - _c(u * 1.2)) * -22
    return None


def t_funde(P, img, u, fuera, pose):
    pose["a"] *= _eio(u)
    pose["s"] *= .96 + .04 * u
    return None


def t_cae(P, img, u, fuera, pose):
    if not fuera:                                    # cae de arriba, rebota y se asienta
        b = _rebote(u)
        pose["y"] -= (1 - b) * P.h * 1.3
        pose["rz"] += (1 - _eo(u)) * -24 * P.lado
        pose["alt"] += (1 - b) * 1.2
        sq = max(0, 1 - abs(u - .364) / .07) * .08 + max(0, 1 - abs(u - .727) / .05) * .04
        pose["sy"] *= 1 - sq
        pose["sx"] *= 1 + sq
        pose["py"] = .5
        pose["a"] *= _c(u * 5)
    else:                                            # se cae por gravedad, girando
        v = 1 - u
        pose["y"] += v * v * P.h * 1.5
        pose["rz"] += v * 30 * P.lado
        pose["a"] *= _c(u / .45)
    return None


def t_vuela(P, img, u, fuera, pose):
    v = 1 - (_eo(u) if not fuera else u)
    e = v * v if fuera else v
    sgn = P.lado if fuera else -P.lado
    pose["x"] += e * P.w * 1.3 * sgn
    pose["y"] -= e * P.h * .6
    pose["rz"] += e * 40 * sgn
    pose["s"] *= 1 + .25 * e
    pose["alt"] += e * 1.2
    pose["a"] *= _c(u / .5)
    return None


def t_volteo(P, img, u, fuera, pose):
    if not fuera:
        e = _back(u, 1.3)
        pose["ry"] += (1 - e) * 180 * P.lado
        pose["s"] *= 1 + .12 * math.sin(math.pi * _c(u))
        pose["alt"] += .7 * math.sin(math.pi * _c(u))
        pose["a"] *= _c(u * 5)
    else:
        pose["ry"] += (1 - u) * -92 * P.lado
        pose["alt"] += (1 - u) * .5
        pose["a"] *= _c(u / .12)
    return None


def _corte(P):
    """Línea de rasgado dentada (x por fila) y máscaras izquierda/derecha."""
    def f():
        rng = np.random.default_rng(P.semilla + 21)
        n = 26
        ys = np.linspace(0, P.h, n)
        xs = P.w / 2 + rng.uniform(-1, 1, n) * P.w * .07
        xr = np.interp(np.arange(P.h), ys, xs) + _ruido(P.h, 1, 3, P.semilla)[:, 0] * 8 - 4
        izq = (np.arange(P.w)[None, :] < xr[:, None]).astype(np.float32)
        izq = cv2.GaussianBlur(izq, (0, 0), .8)[..., None]
        linea = np.stack([xr - P.w / 2, np.arange(P.h) - P.h / 2, np.zeros(P.h)], 1)
        return izq, linea
    return P._campo("corte", f)


def t_rasgado(P, img, u, fuera, pose):
    izq, linea = _corte(P)
    w, h = P.w, P.h
    if not fuera:                                    # una hoja de papel la tapa y se rasga en dos
        tapa = P._campo("tapa", lambda: _prem(PE._papel(w, h, P.tema, semilla=P.semilla + 3)) * (P.img[..., 3:4] > .02))
        f = _c((u - .22) / .78)
        e = f ** 1.5
        capas = [dict(img=img, q=_quad(w, h), sombra=True)]
        sac = 0 if f > 0 else 2 * math.sin(u * 90)
        for lado, m in ((-1, izq), (1, 1 - izq)):
            q = _quad(w, h)
            q = _gira2d(q, lado * e * 28, lado * w / 2, h / 2)
            q[:, 0] += lado * (e * w * .55 + sac)
            q[:, 1] += e * e * h * .35
            capas.append(dict(img=tapa * m, q=q, a=1 - f ** 2))
        k = _c(u / .22)
        if f <= 0:
            n = max(2, int(len(linea) * k))

            def grieta(L, pose_, n=n):
                d = L.proy(linea[:n:4], pose_, w, h)
                _linea(L, d, np.float32([.95, .97, 1.0]), .9, 3)
            P.delante.append(grieta)
        return capas
    v = 1 - u                                        # salida: la pegatina se rompe en dos y caen
    capas = []
    for lado, m in ((-1, izq), (1, 1 - izq)):
        q = _quad(w, h)
        q = _gira2d(q, lado * v * 32, 0, h / 2)
        q[:, 0] += lado * v * w * .3
        q[:, 1] += v * v * h * .9
        capas.append(dict(img=img * m, q=q))
    pose["a"] *= _c(u / .45)
    return capas


def _campo_tinta(P):
    def f():
        rng = random.Random(P.semilla + 5)
        ox, oy = rng.choice(((0, 0), (1, 0), (0, 1), (1, 1), (.5, .5)))
        yy, xx = np.mgrid[0:P.h, 0:P.w].astype(np.float32)
        d = np.hypot((xx / P.w - ox), (yy / P.h - oy))
        n = _ruido(P.h, P.w, 26, P.semilla) * .6 + _ruido(P.h, P.w, 7, P.semilla + 1) * .4
        return _norm01(.6 * _norm01(d) + .4 * n)
    return P._campo("tinta", f)


def t_tinta(P, img, u, fuera, pose):
    """Se revela (o se borra) con una mancha de tinta de borde irregular que se extiende."""
    g = _campo_tinta(P)
    thr = (_eo(u) if not fuera else _eio(u)) * 1.12 - .06
    m = _suave((thr - g) / .035)
    borde = np.exp(-((g - thr + .03) / .028) ** 2) * (m > 0)
    pose["sombra"] *= _eio(u) ** 2
    o = img * m[..., None]
    k = (borde * o[..., 3] * .8)[..., None]
    o[..., :3] = o[..., :3] * (1 - k) + P.c_tinta * k
    pose["s"] *= 1 + .03 * (1 - u)
    return [dict(img=o, q=_quad(P.w, P.h), sombra=True, a=1)] if u > .02 else []


def _desenfoca(img, sigma):
    if sigma < .5:
        return img
    if sigma > 5:
        k = 4
        p = cv2.resize(img, None, fx=1 / k, fy=1 / k, interpolation=cv2.INTER_AREA)
        p = cv2.GaussianBlur(p, (0, 0), sigma / k)
        return cv2.resize(p, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)
    return cv2.GaussianBlur(img, (0, 0), sigma)


def t_enfoque(P, img, u, fuera, pose):
    """Llega desde un punto lejano desenfocada y se enfoca al asentarse (o se va al fondo desenfocándose)."""
    e = _eo(u) if not fuera else _eio(u)
    rng = random.Random(P.semilla + 9)
    px, py = rng.choice(((-1, -1), (1, -1), (-1, 1), (1, 1)))
    pose["s"] *= .14 + .86 * e
    pose["x"] += (1 - e) * px * P.w * .55
    pose["y"] += (1 - e) * py * P.h * .45
    pose["rz"] += (1 - e) * P.lado * 14
    pose["a"] *= _c(u * 2.4)
    pose["alt"] += (1 - e) * .6
    return [dict(img=_desenfoca(img, (1 - e) * 18), q=_quad(P.w, P.h), sombra=True)]


def t_cortinilla(P, img, u, fuera, pose):
    """Cortinilla en diagonal con un filo de luz del tema."""
    ang = random.Random(P.semilla + 4).choice((30, 150, 210, 330))

    def campo():
        a = math.radians(ang)
        yy, xx = np.mgrid[0:P.h, 0:P.w].astype(np.float32)
        return _norm01(xx * math.cos(a) + yy * math.sin(a))
    D = P._campo("diag%d" % ang, campo)
    e = _eio(u)
    if not fuera:
        thr = e * 1.2 - .1
        m = _suave((thr - D) / .015)
    else:
        thr = (1 - e) * 1.2 - .1
        m = _suave((D - thr) / .015)
    pose["sombra"] *= e ** 2
    band = np.exp(-((D - thr) / .014) ** 2) * img[..., 3]
    o = img * m[..., None]
    o[..., :3] += band[..., None] * P.c_luz
    o[..., 3] = np.maximum(o[..., 3], band)
    o[..., :3] = np.minimum(o[..., :3], o[..., 3:4])
    return [dict(img=o, q=_quad(P.w, P.h), sombra=True, a=1 if u < 1 else 1)] if u > .01 else []


def t_origami(P, img, u, fuera, pose):
    """Se despliega como un acordeón de papel de 4 pliegues (o se pliega al irse)."""
    th = math.radians((1 - (_eo(u) if not fuera else _eio(u))) * 86)
    n, w, h = 4, P.w, P.h
    pw = w / n
    tot = w * math.cos(th)
    d = pw * math.sin(th)
    capas = []
    for i in range(n):
        xl = -tot / 2 + i * pw * math.cos(th)
        xr = xl + pw * math.cos(th)
        zl, zr = (0, -d) if i % 2 == 0 else (-d, 0)
        q = np.array([[xl, -h / 2, zl], [xr, -h / 2, zr], [xr, h / 2, zr], [xl, h / 2, zl]], float)
        sub = img[:, int(i * pw):int((i + 1) * pw)]
        capas.append(dict(img=np.ascontiguousarray(sub), q=q, luz=1 - (.42 if i % 2 else .1) * math.sin(th)))
    pose["a"] *= _c(u * 3)
    if th < .01:
        return None
    return capas


def t_deslizar(P, img, u, fuera, pose):
    """Se desliza desde el lado con el borde de ataque en perspectiva; la sombra llega tarde (paralaje)."""
    if not fuera:
        e = _back(u, 1.2)
        pose["x"] += (1 - e) * P.lado * P.w * 1.2
        pose["ry"] += (1 - _eo(u)) * P.lado * -38
        pose["sdx"] = (1 - _eo(u * .8)) * P.lado * 70
        pose["a"] *= _c(u * 3)
    else:
        v = 1 - u
        e = v * v
        pose["x"] -= e * P.lado * P.w * 1.25
        pose["ry"] += e * P.lado * 38
        pose["sdx"] = -e * P.lado * 50
        pose["a"] *= _c(u / .4)
    return None


def _puertas(P):
    def f():
        t = _col(P.tema)
        out = []
        for k, (x0, x1) in enumerate(((0, P.w // 2), (P.w // 2, P.w))):
            ww = x1 - x0
            im = Image.new("RGBA", (ww, P.h), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            base = tuple(int(v * .28 + 14) for v in t["luz"])
            d.rectangle((0, 0, ww - 1, P.h - 1), fill=base + (255,), outline=t["luz"] + (255,), width=4)
            m = int(ww * .14)
            for y0, y1 in ((m, P.h * .46), (P.h * .54, P.h - m)):
                d.rectangle((m, y0, ww - m, y1), outline=t["luz"] + (170,), width=3)
                d.rectangle((m + 6, y0 + 6, ww - m - 6, y1 - 6), outline=(0, 0, 0, 120), width=2)
            kx = ww - m * .6 if k == 0 else m * .6
            d.ellipse((kx - 8, P.h / 2 - 8, kx + 8, P.h / 2 + 8), fill=t["luz"] + (255,))
            a = np.array(im).astype(np.float32)
            a[..., :3] *= 1 + (_ruido(P.h, ww, 4, P.semilla + k)[..., None] - .5) * .25
            p = _prem(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA"))
            out.append(_u8_recto(p, _sangra(p)))
        return out
    return P._campo("puertas", f)


def t_ventana(P, img, u, fuera, pose):
    """Dos contraventanas del color del tema se abren hacia ti y descubren la imagen (al irse, se cierran)."""
    pi, pd = _puertas(P)
    w, h = P.w, P.h
    if not fuera:
        phi = _eo(_c((u - .12) / .88)) * 108
        pose["a"] *= _c(u * 6)
    else:
        phi = _eio(_c((u - .3) / .7)) * 108
        pose["a"] *= _c(u / .3)
    r = math.radians(phi)
    dw = w / 2
    cx, sz = dw * math.cos(r), -dw * math.sin(r)
    qi = np.array([[-w / 2, -h / 2, 0], [-w / 2 + cx, -h / 2, sz], [-w / 2 + cx, h / 2, sz], [-w / 2, h / 2, 0]], float)
    qd = np.array([[w / 2 - cx, -h / 2, sz], [w / 2, -h / 2, 0], [w / 2, h / 2, 0], [w / 2 - cx, h / 2, sz]], float)
    luz = 1 - .45 * math.sin(r)
    a = 1 - _c((phi - 95) / 13)
    return [dict(img=img, q=_quad(w, h), sombra=True), dict(img=pi, q=qi, luz=luz, a=a), dict(img=pd, q=qd, luz=luz, a=a)]


def t_bisagra(P, img, u, fuera, pose):
    """Gira sobre una bisagra en su borde como una puerta, con rebote elástico."""
    if not fuera:
        pose["px"] = -.5 * P.lado
        pose["ry"] += (1 - _elast(u)) * 86 * P.lado
        pose["a"] *= _c(u * 4)
    else:
        pose["px"] = .5 * P.lado
        pose["ry"] += _ei(1 - u) * 88 * P.lado
        pose["a"] *= _c(u / .25)
    return None


def t_glitch(P, img, u, fuera, pose):
    """Interferencia digital: pixelado, franjas desplazadas, separación RGB y parpadeo hasta quedar limpia."""
    k = (1 - u) ** 1.3
    if k < .02:
        return None
    rng = random.Random(P.semilla * 31 + int(u * 60))
    o = img
    h, w = P.h, P.w
    if k > .3:
        f = int(2 + k * 14)
        p = cv2.resize(o, (max(2, w // f), max(2, h // f)), interpolation=cv2.INTER_AREA)
        o = cv2.resize(p, (w, h), interpolation=cv2.INTER_NEAREST)
    else:
        o = o.copy()
    for _ in range(int(2 + k * 8)):
        y0 = rng.randrange(0, h)
        y1 = min(h, y0 + rng.randrange(4, max(6, h // 7)))
        o[y0:y1] = np.roll(o[y0:y1], int(rng.uniform(-1, 1) * k * w * .22), axis=1)
    d = int(k * 16)
    if d:
        b, r = np.roll(o[..., 0], -d, axis=1), np.roll(o[..., 2], d, axis=1)
        ab, ar = np.roll(o[..., 3], -d, axis=1), np.roll(o[..., 3], d, axis=1)
        o = np.dstack([b, o[..., 1], r, np.maximum.reduce([o[..., 3], ab, ar])])
        o[..., :3] = np.minimum(o[..., :3], o[..., 3:4])
    for _ in range(int(k * 4)):
        y = rng.randrange(0, h - 3)
        o[y:y + 3, :, :3] = np.maximum(o[y:y + 3, :, :3], P.c_luz * o[y:y + 3, :, 3:4] * .9)
    pose["x"] += rng.uniform(-1, 1) * k * 22
    pose["a"] *= (.55 + .45 * rng.random()) if k > .2 else 1
    pose["a"] *= _c(u * 4)
    return [dict(img=np.ascontiguousarray(o, np.float32), q=_quad(w, h), sombra=True)]


def _tijeras_img():
    im = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = _fuente_ruta("seguisym.ttf", 96)
    d.text((60, 60), "\u2702", font=f, fill=(250, 250, 250, 255), anchor="mm", stroke_width=5, stroke_fill=(10, 10, 10, 255))
    p = _prem(im)
    return _u8_recto(p, _sangra(p))


def _contorno(P):
    def f():
        a = (P.img[..., 3] > .5).astype(np.uint8)
        cs, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(cs, key=cv2.contourArea)[:, 0, :].astype(np.float32)
        dd = np.r_[0, np.cumsum(np.hypot(*np.diff(c, axis=0).T))]
        s = np.linspace(0, dd[-1], 240)
        pts = np.stack([np.interp(s, dd, c[:, 0]), np.interp(s, dd, c[:, 1])], 1)
        return np.c_[pts - [P.w / 2, P.h / 2], np.zeros(len(pts))]
    return P._campo("contorno", f)


def t_tijera(P, img, u, fuera, pose):
    """Unas tijeras recortan su contorno (línea discontinua) y la pegatina se despega del fondo con su sombra."""
    if fuera:
        return t_vuela(P, img, u, True, pose)
    c = _contorno(P)
    f1, f2 = _c(u / .62), _c((u - .62) / .38)
    gris = img.copy()
    l = gris[..., :3].mean(axis=2, keepdims=True)
    gris[..., :3] = gris[..., :3] * .35 + l * .65
    o = gris * (1 - f2) + img * f2
    pose["alt"] += math.sin(math.pi * f2) * .9
    pose["s"] *= 1 + .07 * math.sin(math.pi * f2)
    pose["rz"] += math.sin(math.pi * f2) * -4 * P.lado
    pose["sombra"] = f2
    pose["a"] *= .65 + .35 * f2
    pose["a"] *= _c(u * 6)
    if f1 < 1:
        n = max(2, int(len(c) * f1))
        tij = P._campo("tijeras", _tijeras_img)

        def corte(L, pose_, n=n):
            d = L.proy(c[:n], pose_, P.w, P.h)
            for i in range(0, len(d) - 3, 6):
                _linea(L, d[i:i + 4], np.float32([.04, .04, .04]), .8, 9)
                _linea(L, d[i:i + 4], P.c_luz, 1, 5)
            j = min(len(c) - 2, n - 1)
            ang = math.degrees(math.atan2(c[j + 1, 1] - c[j, 1], c[j + 1, 0] - c[j, 0]))
            q = _gira2d(_quad(120, 120) + [c[j, 0], c[j, 1], 0], ang, c[j, 0], c[j, 1])
            L.dibuja(tij, q, pose_, P.w, P.h)
        P.delante.append(corte)
    return [dict(img=o.astype(np.float32), q=_quad(P.w, P.h), sombra=True)]


def _esquirlas(P):
    def f():
        rng = random.Random(P.semilla + 77)
        w, h = P.w, P.h
        c = np.array([w * rng.uniform(.38, .62), h * rng.uniform(.38, .62)])
        n = 11
        angs = sorted((2 * math.pi * (i + rng.uniform(-.3, .3)) / n) for i in range(n))
        R = math.hypot(w, h)

        def borde(a):                                 # rayo desde c hasta el borde del rectángulo
            dx, dy = math.cos(a), math.sin(a)
            ts = []
            for t_ in ((0 - c[0]) / dx if dx else 1e9, (w - c[0]) / dx if dx else 1e9, (0 - c[1]) / dy if dy else 1e9, (h - c[1]) / dy if dy else 1e9):
                if t_ > 0:
                    ts.append(t_)
            t_ = min(ts) if ts else R
            return c + t_ * np.array([dx, dy])
        esq = [np.array(p, float) for p in ((0, 0), (w, 0), (w, h), (0, h))]
        ang_esq = [math.atan2(p[1] - c[1], p[0] - c[0]) % (2 * math.pi) for p in esq]
        piezas, grietas = [], []
        rin = [rng.uniform(.3, .5) for _ in angs]
        for i in range(n):
            a0, a1 = angs[i] % (2 * math.pi), angs[(i + 1) % n] % (2 * math.pi)
            b0, b1 = borde(a0), borde(a1)
            i0 = c + (b0 - c) * rin[i]
            i1 = c + (b1 - c) * rin[(i + 1) % n]
            piezas.append([c, i0, i1])
            ext = [i0, b0]
            span = (a1 - a0) % (2 * math.pi)
            for k, ae in sorted(((k, (ae - a0) % (2 * math.pi)) for k, ae in enumerate(ang_esq)), key=lambda z: z[1]):
                if 0 < ae < span:
                    ext.append(esq[k])
            ext += [b1, i1]
            piezas.append(ext)
            grietas.append(np.array([c, b0]))
            grietas.append(np.array([i0, i1]))
        out = []
        for poly in piezas:
            pp = np.array(poly, np.float32)
            x0, y0 = np.floor(pp.min(0)).astype(int)
            x1, y1 = np.ceil(pp.max(0)).astype(int) + 1
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
            if x1 - x0 < 3 or y1 - y0 < 3:
                continue
            m = np.zeros((y1 - y0, x1 - x0), np.uint8)
            cv2.fillPoly(m, [np.round(pp - [x0, y0]).astype(np.int32)], 255)
            m = cv2.dilate(m, np.ones((3, 3), np.uint8))
            cen = pp.mean(0)
            dirv = cen - c
            dirv = dirv / max(1e-3, np.linalg.norm(dirv))
            dist = rng.uniform(.22, .5) * max(w, h)
            out.append(dict(bb=(x0, y0, x1, y1), m=m.astype(np.float32)[..., None] / 255, cen=cen, dir=dirv, dist=dist,
                            rot=rng.uniform(-110, 110), z=rng.uniform(-260, 160), d=rng.uniform(0, .28)))
        cg = [np.c_[g - [w / 2, h / 2], np.zeros(len(g))] for g in grietas]
        return out, cg
    return P._campo("esquirlas", f)


def t_cristal(P, img, u, fuera, pose):
    """Se arma con esquirlas de cristal que vuelan hasta su sitio y dejan las grietas brillando (al irse, estalla)."""
    piezas, grietas = _esquirlas(P)
    w, h = P.w, P.h
    if not fuera and u >= .985:
        return None
    capas = []
    lleno = True
    for pz in piezas:
        if not fuera:
            e = _eo(_c((u - pz["d"]) / .62))
        else:
            e = _c((u - .2 - pz["d"] * .6) / .5) ** .7
        if e < .999:
            lleno = False
        x0, y0, x1, y1 = pz["bb"]
        q = _quad(w, h, x0, y0, x1, y1)
        q = _gira2d(q, (1 - e) * pz["rot"], pz["cen"][0] - w / 2, pz["cen"][1] - h / 2)
        q[:, 0] += (1 - e) * pz["dir"][0] * pz["dist"]
        q[:, 1] += (1 - e) * pz["dir"][1] * pz["dist"] + (1 - e) ** 2 * (h * .4 if fuera else 0)
        q[:, 2] += (1 - e) * pz["z"]
        capas.append(dict(img=np.ascontiguousarray(img[y0:y1, x0:x1] * pz["m"]), q=q, a=_c(e * 3), luz=.85 + .15 * e))
    ga = (_c((u - .55) / .2) * (1 - _c((u - .8) / .2))) if not fuera else _c((1 - u) / .2) * (1 - _c((1 - u - .2) / .1))
    if ga > .01:
        def grieta(L, pose_):
            for g in grietas:
                _linea(L, L.proy(g, pose_, w, h), np.float32([1, 1, 1]), ga * .85, 2)
        P.delante.append(grieta)
    if lleno and not fuera:
        return [dict(img=img, q=_quad(w, h), sombra=True)]
    pose["sombra"] = 0
    return capas


def t_iman(P, img, u, fuera, pose):
    """Llega acelerando como atraída por un imán, choca, se sacude y suelta líneas de impacto."""
    if fuera:
        return t_deslizar(P, img, u, True, pose)
    ph = _c(u / .45)
    e = ph ** 2.2
    pose["x"] += (1 - e) * P.lado * P.w * 1.2
    pose["rz"] += (1 - e) * P.lado * 9
    pose["a"] *= _c(u * 6)
    if u > .45:
        q = (u - .45) / .55
        pose["x"] += math.exp(-q * 5) * math.sin(q * 40) * 26 * -P.lado
        pose["sx"] *= 1 - .09 * math.exp(-q * 9)
        if q < .5:
            k = 1 - q * 2
            w, h = P.w, P.h

            def impacto(L, pose_):
                for ang in range(0, 360, 30):
                    a = math.radians(ang)
                    rx, ry = w / 2 * 1.05, h / 2 * 1.05
                    p = np.array([[rx * math.cos(a), ry * math.sin(a), 0], [(rx + 30 + 50 * (1 - k)) * math.cos(a), (ry + 30 + 50 * (1 - k)) * math.sin(a), 0]])
                    _linea(L, L.proy(p, pose_, w, h), P.c_luz, k, 5)
            P.delante.append(impacto)
    return None


def t_sello(P, img, u, fuera, pose):
    """Baja desde arriba de la cámara como un sello y estampa: anillo de polvo y motas que salen disparadas."""
    if fuera:
        return t_remolino(P, img, u, True, pose)
    ph = _c(u / .36)
    e = ph * ph
    pose["s"] *= 2.3 - 1.3 * e
    pose["alt"] += (1 - e) * 1.5
    pose["rz"] += (1 - e) * P.lado * -10
    pose["a"] *= _c(u * 5)
    if u > .36:
        q = (u - .36) / .64
        pose["s"] *= 1 - .045 * math.exp(-q * 7) * math.cos(q * 22)
        w, h = P.w, P.h
        rng = random.Random(P.semilla + 3)
        motas = [(rng.uniform(0, 6.28), rng.uniform(.8, 1.4), rng.uniform(3, 7)) for _ in range(16)]

        def polvo(L, pose_):
            k = 1 - q
            r = 1 + q * .4
            ang = np.linspace(0, 2 * math.pi, 48)
            p = np.c_[np.cos(ang) * w * .56 * r, np.sin(ang) * h * .56 * r, np.zeros(48)]
            _linea(L, L.proy(p, pose_, w, h), P.c_papel, k * .7, max(1, int(6 * k)))
            for a0, v, tm in motas:
                rr = (1.05 + q * v * .7)
                d = L.proy(np.array([[math.cos(a0) * w * .5 * rr, math.sin(a0) * h * .5 * rr, 0]]), pose_, w, h)[0]
                _punto(L, d[0], d[1], tm * k, P.c_papel, k)
        P.delante.append(polvo)
    return None


def t_tiras(P, img, u, fuera, pose):
    """Se arma con tiras que llegan alternando de cada lado, escalonadas (al irse, se reparten igual)."""
    rng = random.Random(P.semilla + 8)
    vert = rng.random() < .35
    n = rng.choice((5, 6, 7, 8))
    w, h = P.w, P.h
    capas = []
    lleno = True
    for i in range(n):
        d = (i / n) * .38
        e = _eo(_c((u - d) / .62)) if not fuera else _eio(_c((u - d) / .62))
        if e < .999:
            lleno = False
        sgn = 1 if i % 2 == 0 else -1
        if vert:
            x0, x1 = int(i * w / n), int((i + 1) * w / n)
            q = _quad(w, h, x0, 0, x1, h)
            q[:, 1] += (1 - e) * sgn * h * 1.2
            sub = img[:, x0:x1]
        else:
            y0, y1 = int(i * h / n), int((i + 1) * h / n)
            q = _quad(w, h, 0, y0, w, y1)
            q[:, 0] += (1 - e) * sgn * w * 1.25
            sub = img[y0:y1]
        capas.append(dict(img=np.ascontiguousarray(sub), q=q, a=_c(e * 2)))
    if lleno:
        return None
    pose["sombra"] = 0
    return capas


def t_baldosas(P, img, u, fuera, pose):
    """Mosaico: las baldosas aparecen (o se van) en desorden con un pequeño rebote, como un videojuego cargando."""
    w, h = P.w, P.h
    nx = 6
    ny = max(3, round(nx * h / w))

    def orden():
        rng = random.Random(P.semilla + 6)
        return [rng.uniform(0, .58) for _ in range(nx * ny)]
    ds = P._campo("baldosas", orden)
    capas = []
    lleno = True
    for j in range(ny):
        for i in range(nx):
            d = ds[j * nx + i]
            e = _back(_c((u - d) / .42), 2.0) if not fuera else _c((u - d) / .42) ** 2
            if e < .999:
                lleno = False
            if e <= .01:
                continue
            x0, x1, y0, y1 = int(i * w / nx), int((i + 1) * w / nx), int(j * h / ny), int((j + 1) * h / ny)
            q = _quad(w, h, x0, y0, x1, y1)
            cx, cy = (x0 + x1) / 2 - w / 2, (y0 + y1) / 2 - h / 2
            q[:, 0] = cx + (q[:, 0] - cx) * e
            q[:, 1] = cy + (q[:, 1] - cy) * e
            q = _gira2d(q, (1 - min(1, e)) * (30 if (i + j) % 2 else -30), cx, cy)
            sub = img[y0:y1, x0:x1]
            if sub[..., 3].max() < .02:
                continue
            capas.append(dict(img=np.ascontiguousarray(sub), q=q, a=_c(e * 2)))
    if lleno:
        return None
    pose["sombra"] = 0
    return capas


def _campo_ceniza(P):
    def f():
        yy = np.mgrid[0:P.h, 0:P.w][0].astype(np.float32)
        n = _ruido(P.h, P.w, 18, P.semilla + 2) * .55 + _ruido(P.h, P.w, 5, P.semilla + 3) * .45
        g = _norm01(.55 * _norm01(n) + .45 * (1 - yy / P.h))
        rng = np.random.default_rng(P.semilla + 4)
        pts = rng.random((60, 2)) * [P.w, P.h]
        gp = g[pts[:, 1].astype(int).clip(0, P.h - 1), pts[:, 0].astype(int).clip(0, P.w - 1)]
        return g, pts, gp
    return P._campo("ceniza", f)


def t_ceniza(P, img, u, fuera, pose):
    """Se quema desde abajo con un frente de brasas y chispas que suben (al entrar, se forma desde las brasas)."""
    g, pts, gp = _campo_ceniza(P)
    thr = (1 - _eio(u)) * 1.16 - .08                 # todo lo de g < thr está quemado
    m = _suave((g - thr) / .03)
    ascua = np.exp(-((g - thr - .025) / .022) ** 2)
    carbon = np.exp(-((g - thr - .07) / .05) ** 2) * .7
    pose["sombra"] *= _eio(u) ** 2
    o = img * m[..., None]
    a = o[..., 3:4]
    brasa = np.float32([.15, .5, 1.0])
    o[..., :3] = o[..., :3] * (1 - carbon[..., None]) + brasa * (ascua[..., None] * a)
    o[..., :3] = np.minimum(o[..., :3] + brasa * (ascua * img[..., 3] * .8)[..., None] * (1 - m[..., None]), 1)
    o[..., 3] = np.maximum(o[..., 3], ascua * img[..., 3] * .8)
    w, h = P.w, P.h

    def chispas(L, pose_):
        for (x, y), gv in zip(pts, gp):
            edad = (thr - gv) / .22
            if 0 < edad < 1:
                d = L.proy(np.array([[x - w / 2 + 10 * math.sin(edad * 6 + x), y - h / 2 - edad * 90, 0]]), pose_, w, h)[0]
                _punto(L, d[0], d[1], 4 * (1 - edad) + 1, np.float32([.3, .65, 1.0]), 1 - edad)
    P.delante.append(chispas)
    return [dict(img=o, q=_quad(w, h), sombra=True, a=1)]


def t_remolino(P, img, u, fuera, pose):
    """Entra (o se va) girando en espiral desde un punto."""
    k = _eo(u) if not fuera else _eio(u)
    pose["s"] *= .05 + .95 * k
    pose["rz"] += (1 - k) * 220 * P.lado
    pose["a"] *= _c(u * 2.5)
    pose["alt"] += (1 - k) * .5
    return None


ENT = dict(pop=t_pop, cae=t_cae, volteo=t_volteo, rasgado=t_rasgado, tinta=t_tinta, enfoque=t_enfoque, cortinilla=t_cortinilla,
           origami=t_origami, deslizar=t_deslizar, ventana=t_ventana, bisagra=t_bisagra, glitch=t_glitch, tijera=t_tijera,
           cristal=t_cristal, iman=t_iman, sello=t_sello, tiras=t_tiras, baldosas=t_baldosas, ceniza=t_ceniza, remolino=t_remolino,
           vuela=t_vuela)
SAL = dict(funde=t_funde, cae=t_cae, volteo=t_volteo, rasgado=t_rasgado, tinta=t_tinta, enfoque=t_enfoque, cortinilla=t_cortinilla,
           origami=t_origami, deslizar=t_deslizar, ventana=t_ventana, bisagra=t_bisagra, glitch=t_glitch, cristal=t_cristal,
           tiras=t_tiras, baldosas=t_baldosas, ceniza=t_ceniza, remolino=t_remolino, vuela=t_vuela)
# entradas que piden más tiempo para lucirse
_TE = dict(cae=1.0, tijera=1.25, cristal=.95, ventana=.95, rasgado=.95, tinta=.85, ceniza=.95, baldosas=.85, tiras=.8, sello=.8,
           iman=.8, bisagra=.85, origami=.75, volteo=.8)
_TS = dict(ceniza=.75, cristal=.65, rasgado=.6, tinta=.55, ventana=.75, baldosas=.6, tiras=.55, cae=.55)


# ----------------------------------------------------------------------------------------------------------- rotador
class Rotador:
    """Reparte entradas, estancias, salidas y marcos sin repetir la misma dos veces seguidas y recorriendo TODO el catálogo
    antes de repetir (bolsas barajadas; lo afín al tema sale antes en cada vuelta). Determinista por video."""

    def __init__(self, clave, tema):
        self.rnd = random.Random(int(hashlib.md5(("%s|%s" % (clave, tema)).encode("utf-8")).hexdigest()[:8], 16))
        fam = _FAMILIA.get(tema, "epico")
        self.afin, self.poco = _AFIN.get(fam, set()), _POCO.get(fam, set())
        self.bolsas, self.ultimo, self.usos = {}, {}, []

    def _orden(self, ops):
        peso = lambda o: 3.0 if o in self.afin else .45 if o in self.poco else 1.0
        return sorted(ops, key=lambda o: -self.rnd.random() ** (1 / peso(o)))

    def _saca(self, cat, ops, valido=lambda o: True, ult=None):
        ult = ult or cat                               # «marco» y «marcoR» (recortes) comparten el último usado
        for _ in range(3):
            bolsa = self.bolsas.get(cat) or []
            for i, o in enumerate(bolsa):
                if o != self.ultimo.get(ult) and valido(o):
                    bolsa.pop(i)
                    self.bolsas[cat] = bolsa
                    self.ultimo[ult] = o
                    return o
            self.bolsas[cat] = bolsa + self._orden([o for o in ops if o not in bolsa])
        o = next((o for o in ops if valido(o) and o != self.ultimo.get(ult)), ops[0])
        self.ultimo[ult] = o
        return o

    def elige(self, recorte, fijo=None):
        fijo = dict(fijo or {})
        marcos = [m for m in MARCOS_TODOS if recorte or m != "aura"]
        marco = fijo.get("marco") or self._saca("marco" + ("R" if recorte else ""), marcos, ult="marco")
        con_ventana = not (marco == "aura" or (marco == "clasico" and recorte))
        ent = fijo.get("entrada") or self._saca("entrada", ENTRADAS)
        est = fijo.get("estancia") or self._saca("estancia", ESTANCIAS, lambda o: con_ventana or o != "kenburns")
        sal = fijo.get("salida") or self._saca("salida", SALIDAS, lambda o: o != ent)
        c = dict(entrada=ent, estancia=est, salida=sal, marco=marco)
        self.usos.append(c)
        return c


_ROT = {}


def rotador(video, tema):
    k = (video, tema)
    if k not in _ROT:
        _ROT[k] = Rotador(video, tema)
    return _ROT[k]


def _video_de(ruta):
    p = os.path.abspath(ruta).replace("\\", "/").split("/")
    return p[p.index("videos") + 1] if "videos" in p and p.index("videos") + 1 < len(p) else os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(ruta))))


def pegatina(ruta, titulo=None, tam=400, tema="tes", entrada="cae", estancia="flota", salida="vuela", marco="polaroid", **kw):
    """Una pegatina con la combinación que tú elijas (para fijar una animación concreta)."""
    for nombre, cat in ((entrada, ENT), (estancia, EST), (salida, SAL), (marco, MARCOS)):
        if nombre not in cat:
            raise ValueError("peg_anim: «%s» no existe; hay: %s" % (nombre, ", ".join(cat)))
    sem = kw.pop("semilla", None)
    if sem is None:
        sem = int(hashlib.md5(("%s|%s" % (ruta, titulo)).encode("utf-8")).hexdigest()[:6], 16)
    kw.setdefault("te", _TE.get(entrada, .7))
    kw.setdefault("ts", _TS.get(salida, .5))
    return Pegatina(ruta, titulo, tam, tema, entrada, estancia, salida, marco, semilla=sem, **kw)


def variado(ruta, titulo=None, tam=400, tema="tes", video=None, **fijo):
    """Pegatina con la siguiente combinación del rotador del video: nunca la misma animación dos veces seguidas.
    `fijo` fija una parte (entrada=, estancia=, salida=, marco=) y el rotador elige el resto. `video` por defecto = carpeta."""
    rot = rotador(video or _video_de(ruta), tema)
    elegir = {k: fijo.pop(k) for k in ("entrada", "estancia", "salida", "marco") if k in fijo}
    c = rot.elige(es_recorte(ruta), elegir)
    fijo.setdefault("semilla", len(rot.usos) * 101 + int(hashlib.md5(ruta.encode("utf-8")).hexdigest()[:4], 16))
    return pegatina(ruta, titulo, tam, tema, **c, **fijo)


# ----------------------------------------------------------------------------------------------------------- pila de fotos
class Pila(_Lienzo):
    """Pila de fotos (polaroid u otro marco) que se reparte en fila con las marcas de la voz; al final se recogen."""

    def __init__(self, fotos, tam=300, tema="tes", marco="polaroid", sep=None, arco=40):
        self.fotos, self.tam, self.tema, self.marco, self.arco = fotos, tam, tema, marco, arco
        self.sep = sep
        self._listo = False
        self.anim = "pila/%s" % marco

    def _prepara(self):
        self.cartas = []
        for k, (ruta, et) in enumerate(self.fotos):
            im, rec = _abre(ruta)
            c = MARCOS[self.marco if (self.marco != "aura" or rec) else "polaroid"](im, rec, et, self.tam, self.tema)
            p = _prem(c.img)
            SP = 22
            al = np.zeros((p.shape[0] + 2 * SP, p.shape[1] + 2 * SP), np.float32)
            al[SP:-SP, SP:-SP] = p[..., 3]
            al = cv2.GaussianBlur(al, (0, 0), 8)
            self.cartas.append((_u8_recto(p, _sangra(p)), _u8_recto(np.dstack([np.zeros_like(al)] * 3 + [al])), SP))
        n = len(self.cartas)
        wmax = max(c[0].shape[1] for c in self.cartas)
        hmax = max(c[0].shape[0] for c in self.cartas)
        self.sep = self.sep or wmax * .9
        rng = random.Random(len(self.fotos) * 7 + 3)
        self.giros = [rng.uniform(-7, 7) for _ in range(n)]
        self.monton = [(rng.uniform(-14, 14), rng.uniform(-10, 10), rng.uniform(-14, 14)) for _ in range(n)]
        self._lienzo(int(self.sep * (n - 1) + wmax * 1.6) + 120, int(hmax * 1.5 + self.arco) + 160)
        self._listo = True

    def __call__(self, dt, dur, marcas=()):
        if not self._listo:
            self._prepara()
        self._limpia()
        n = len(self.cartas)
        mk = list(marcas) + [.45 + .32 * k for k in range(len(marcas), n)]
        entra = _eo(dt / .45)
        sale = _c((dur - dt) / .6)
        orden = list(range(n))
        for k in orden:                          # la de arriba del montón es la última: se reparte primero
            p, sp, SP = self.cartas[k]
            h, w = p.shape[:2]
            e = _eo((dt - mk[min(k, len(mk) - 1)]) / .5)
            tx = (k - (n - 1) / 2) * self.sep
            ty = abs(k - (n - 1) / 2) * self.arco / max(1, (n - 1) / 2) * .6
            mx, my, mr = self.monton[k]
            x = mx + (tx - mx) * e
            y = my + (ty - my) * e - math.sin(math.pi * e) * 70
            r = mr + (self.giros[k] - mr) * e + 1.2 * math.sin(dt * 1.5 + k)
            alt = math.sin(math.pi * e) * .9
            ks = 1 - sale
            pose = _pose(x=x * (1 - ks * .7), y=y + ks * ks * 260, rz=r + ks * 25 * (1 if k % 2 else -1), s=(.9 + .1 * entra), a=entra * _c(sale / .5) if sale < 1 else entra)
            qs = _quad(w, h)
            qs[:, :2] *= np.array([(w + 2 * SP) / w, (h + 2 * SP) / h])
            ps = dict(pose, x=pose["x"] + 9 + 40 * alt, y=pose["y"] + 13 + 56 * alt)
            self.dibuja(sp, qs, ps, w, h, a=.55 * (1 - .4 * alt) * pose["a"])
            self.dibuja(p, _quad(w, h), pose, w, h, a=pose["a"])
        return self._bgra()


def pila(fotos, tam=300, tema="tes", marco="polaroid", **kw):
    """fotos = [(ruta, etiqueta)]; reparte una por marca de la voz (o escalonadas)."""
    return Pila(fotos, tam, tema, marco, **kw)


def catalogo():
    return dict(marcos=list(MARCOS_TODOS), entradas=list(ENTRADAS), estancias=list(ESTANCIAS), salidas=list(SALIDAS), multi=["pila"])


# ----------------------------------------------------------------------------------------------------------- hoja de prueba
def _fondo(ruta, W=960, H=540):
    if ruta and os.path.exists(ruta):
        return cv2.resize(cv2.imread(ruta), (W, H))
    yy, xx = np.mgrid[0:H, 0:W]
    f = np.dstack([40 + 30 * xx / W, 46 + 20 * yy / H, 60 + 40 * (1 - yy / H)]).astype(np.uint8)
    return f


def _sobre(f, bgra, k=.5):
    o = cv2.resize(bgra, None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
    h, w = o.shape[:2]
    H, W = f.shape[:2]
    x, y = W // 2 - w // 2, H // 2 - h // 2
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    r = o[y0 - y:y1 - y, x0 - x:x1 - x]
    a = r[..., 3:4].astype(np.float32) / 255
    f = f.copy()
    f[y0:y1, x0:x1] = (r[..., :3] * a + f[y0:y1, x0:x1] * (1 - a)).astype(np.uint8)
    return f


def hoja(tema="tes", img=None, fondo=None, salida=".", recorte_prueba=None):
    """Una hoja por categoría: cada fila = una animación en 5 tiempos. Devuelve las rutas."""
    import time
    os.makedirs(salida, exist_ok=True)
    img = img or _img_prueba()
    recorte_prueba = recorte_prueba or _img_prueba(recorte=True)
    rutas = []
    dur = 4.0
    pruebas = [("entradas", [(e, dict(entrada=e, estancia="quieta", salida="funde", marco="polaroid" if i % 2 else "carta"))
                             for i, e in enumerate(ENTRADAS)], lambda P: [P.te * f for f in (.12, .3, .5, .75, 1.0)]),
               ("salidas", [(s, dict(entrada="pop", estancia="quieta", salida=s, marco="cristal" if i % 2 else "museo"))
                            for i, s in enumerate(SALIDAS)], lambda P: [dur - P.ts * f for f in (1.0, .75, .5, .3, .12)]),
               ("estancias", [(s, dict(entrada="pop", estancia=s, salida="funde", marco="monitor" if s in ("kenburns", "lupa") else "rasgado"))
                              for s in ESTANCIAS], lambda P: [1.0, 1.6, 2.2, 2.8, 3.3]),
               ("marcos", [(m, dict(entrada="pop", estancia="quieta", salida="funde", marco=m)) for m in MARCOS_TODOS], None)]
    bg = _fondo(fondo)
    tiempos = []
    for nombre, items, ts in pruebas:
        filas = []
        for etiqueta, combo in items:
            celdas = []
            if ts is None:                               # marcos: la misma pegatina en 5 temas de canal (y el recorte)
                for k, tm in enumerate(("tes", "wow", "gaming", "cod", tema)):
                    im_ = recorte_prueba if (k == 4 and recorte_prueba) else img
                    P = pegatina(im_, "Nombre de prueba", 520, tm, **combo)
                    c = _sobre(bg, P(1.2, dur, []), .55)
                    cv2.putText(c, tm + (" recorte" if k == 4 and recorte_prueba else ""), (10, 530), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
                    celdas.append(cv2.resize(c, (384, 216)))
            else:
                P = pegatina(img, "Nombre de prueba", 520, tema, **combo)
                P(0.0, dur, [])
                for t in ts(P):
                    t0 = time.perf_counter()
                    o = P(t, dur, [])
                    tiempos.append(time.perf_counter() - t0)
                    c = _sobre(bg, o, .55)
                    celdas.append(cv2.resize(c, (384, 216)))
            fila = np.hstack(celdas)
            cv2.rectangle(fila, (0, 0), (190, 30), (0, 0, 0), -1)
            cv2.putText(fila, etiqueta, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 255, 255), 2, cv2.LINE_AA)
            filas.append(fila)
        for k in range(0, len(filas), 7):
            r = os.path.join(salida, "peg_anim_%s_%s_%d.jpg" % (tema, nombre, k // 7 + 1))
            cv2.imwrite(r, np.vstack(filas[k:k + 7]), [cv2.IMWRITE_JPEG_QUALITY, 86])
            rutas.append(r)
    pl = pila([(img, "Uno"), (img, "Dos"), (img, "Tres"), (img, "Cuatro")], 260, tema)
    fila = np.hstack([cv2.resize(_sobre(bg, pl(t, 4.0, []), .5), (384, 216)) for t in (.3, .8, 1.3, 2.2, 3.8)])
    r = os.path.join(salida, "peg_anim_%s_pila.jpg" % tema)
    cv2.imwrite(r, fila)
    rutas.append(r)
    print("cuadros: %d · media %.1f ms · máx %.1f ms" % (len(tiempos), 1000 * np.mean(tiempos), 1000 * np.max(tiempos)))
    return rutas


def _img_prueba(recorte=False):
    for c in (("videos/banjo_tooie/pegatinas/banjo.png",) if recorte else ("videos/er_radahn_atrocidades/pegatinas/blaidd.png",)):
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), c)
        if os.path.isfile(p):
            return p
    if recorte:
        return None
    raise SystemExit("peg_anim hoja: pasa --img ruta.png")


# ampliación del 5-nov-2026 (marcos pergamino/vitral/naipe/estampilla, entradas persiana/portal/escaner/desenrolla/aplasta,
# estancias orbita/vela/balanceo): se registra aquí para que el rotador y la hoja las usen sin tocar efectos.py
import sys as _sys  # noqa: E402
import peg_anim_mas as _MAS  # noqa: E402
_MAS.registra(_sys.modules[__name__])


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=("hoja", "catalogo"))
    ap.add_argument("--tema", default="tes")
    ap.add_argument("--img")
    ap.add_argument("--fondo")
    ap.add_argument("--recorte", help="PNG sin fondo para la fila de marcos (aura)")
    ap.add_argument("--salida", default="previews")
    a = ap.parse_args()
    if a.accion == "catalogo":
        for k, v in catalogo().items():
            print("%-10s %s" % (k, " ".join(v)))
    else:
        for r in hoja(a.tema, a.img, a.fondo, a.salida, a.recorte):
            print(r)
