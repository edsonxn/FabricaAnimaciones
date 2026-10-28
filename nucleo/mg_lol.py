# -*- coding: utf-8 -*-
"""Kit de GRÁFICOS DE TRANSMISIÓN de esports (League of Legends) para el estilo análisis táctico (docs/estilo_analisis_tactico.md).
Nace el 27-oct-2026 en `videos/lol_worlds_2026/` porque el usuario vio las píldoras planas de mg_tactica.chip («se ven muy
básicas, poco impresionantes… aprende cómo se editan los videos de Warcraft, Tamriel, Runa Caída») y pidió pegatinas, imágenes
y animación en general. Mismo método que esos canales: pegatinas reales cada pocos segundos, MG propios del guion que entran
por partes con las `marcas` de la voz, nada quieto más de ~2 s.

Todas las piezas devuelven fn(dt, dur, marcas) -> BGRA (numpy) para el FX `mg` de nucleo/secuencia_fx.py (x, y = centro).
El lienzo de cada pieza es de tamaño FIJO (la animación vive dentro) para que no tiemble al centrarse.
Lenguaje visual: panel de vidrio azul noche con filo dorado (oro de LoL), esquina cortada tipo hextech, barra de color del
equipo, tipografía Bahnschrift condensada en mayúsculas, brillo que barre al entrar, leve giro 3D (perspectiva) que respira.
Imágenes: logos oficiales (static.lolesports.com, API pública getTeams), fotos oficiales de jugadores (misma API, PNG
recortado) y arte de campeones (Data Dragon). Cero datos inventados: todo sale del guion.

  tarjeta(titulo, sub, color, logo|icono, dato)      tercio inferior de transmisión (sustituye a mg_tactica.chip)
  pegatina(foto, nombre, color, logo, gris, sello)   jugador recortado con borde blanco, placa con su equipo; sello opcional
  resultados(titulo, partidos)                       marcadores que entran uno por marca (ganador brilla, perdedor gris)
  caida(titulo, equipos, remate)                     logos en fila; en cada marca un tajo rojo los apaga; remate «0-4»
  eliminado(logo, nombre, sub)                       el escudo se parte en esquirlas, se apaga y cae el sello ELIMINADO
  apertura(titulo, sub, fondo)                       portada en frío: destellos dorados, golpe del título, glitch
  menu(items)                                        mosaicos con imagen que giran en 3D uno por marca (lo que viene)
  versus(a, b, titulo, sub)                          duelo: dos escudos que chocan desde los lados con «VS»
  suiza(titulo, ...)                                 el formato suizo: nodos de récord que se encienden y flechas
  ficha_jugador(foto, nombre, logo, n, stats)        top de jugadores: foto, «N.º k», barras de estadística por marca
  ranking(titulo, filas)                             ranking de equipos con puesto en rombo dorado y récord
  tabla(titulo, columnas)                            equipos por récord en columnas (2-0 | 0-2)
  calendario(titulo, hitos)                          línea de fechas; la última (la final) con halo
  barras(titulo, items, total)                       picks de campeones: barra por marca, «12 de 29»
  duelo(a, b, titulo, filas)                         cara a cara por posición: dos fotos y barras que crecen desde el centro
"""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ORO, ORO_C, NOCHE = (200, 170, 110), (240, 230, 210), (6, 12, 24)
HEX = (10, 200, 185)
COL = dict(azul=(70, 165, 255), rojo=(255, 68, 82), oro=ORO, amarillo=(255, 214, 10), blanco=(245, 245, 245),
           verde=(60, 230, 140), gris=(140, 148, 160), hex=HEX)
_fc, _cache = {}, {}


def _c(c):
    return COL.get(c, c) if isinstance(c, str) else tuple(c)


def fuente(estilo, tam):
    """Bahnschrift con su variación («Bold Condensed», «SemiBold Condensed», «Condensed», «Bold»)."""
    k = (estilo, tam)
    if k not in _fc:
        f = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", tam)
        try:
            f.set_variation_by_name(estilo)
        except Exception:
            pass
        _fc[k] = f
    return _fc[k]


clamp = lambda u: max(0.0, min(1.0, u))


def _eo(u):
    u = clamp(u)
    return 1 - (1 - u) ** 3


def _eio(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def _pop(dt, dur=.35):
    """Rebote elástico 0 -> 1 (pasa de 1 y vuelve)."""
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1.8 else 1 - math.exp(-5.5 * u) * math.cos(8.5 * u)


def _mk(marcas, i, defecto):
    return marcas[i] if i < len(marcas) else defecto


def _np(im):
    return np.ascontiguousarray(np.array(im.convert("RGBA"))[..., [2, 1, 0, 3]])


def _vacio(w, h):
    return np.zeros((h, w, 4), np.uint8)


def _sobre(dst, src, x, y, alfa=1.0):
    """Pega BGRA sobre BGRA (alfa premultiplicado a mano), recortando a los bordes."""
    if alfa <= 0:
        return
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    d = dst[y0:y1, x0:x1].astype(np.float32)
    a = s[..., 3:4] / 255 * alfa
    da = d[..., 3:4] / 255
    oa = a + da * (1 - a)
    rgb = (s[..., :3] * a + d[..., :3] * da * (1 - a)) / np.maximum(oa, 1e-4)
    dst[y0:y1, x0:x1, :3] = rgb.clip(0, 255).astype(np.uint8)
    dst[y0:y1, x0:x1, 3] = (oa[..., 0] * 255).clip(0, 255).astype(np.uint8)


def _centro(dst, src, cx, cy, escala=1.0, alfa=1.0):
    if escala <= .02 or alfa <= 0:
        return
    if abs(escala - 1) > .01:
        src = cv2.resize(src, None, fx=escala, fy=escala, interpolation=cv2.INTER_LINEAR)
    _sobre(dst, src, int(cx - src.shape[1] / 2), int(cy - src.shape[0] / 2), alfa)


def _perspectiva(arr, ang, margen=0):
    """Gira la pieza `ang` grados sobre su eje vertical (el borde izquierdo se acerca si ang > 0). Mismo tamaño de salida."""
    if abs(ang) < .2:
        return arr
    h, w = arr.shape[:2]
    f, a = 1600.0, math.radians(ang)
    pts = []
    for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        z = -x * math.sin(a)
        k = f / (f + z)
        pts.append((w / 2 + x * math.cos(a) * k, h / 2 + y * k))
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32(pts))
    return cv2.warpPerspective(arr, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def _texto(d, xy, s, f, color, ancla="la", alfa=255, sombra=True, track=0):
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if track:
        x, y = xy
        tot = sum(d.textlength(ch, font=f) + track for ch in s) - track
        if ancla[0] == "m":
            x -= tot / 2
        elif ancla[0] == "r":
            x -= tot
        for ch in s:
            if sombra:
                d.text((x + 2, y + 3), ch, font=f, fill=(0, 0, 0, int(a * .55)), anchor="l" + ancla[1])
            d.text((x, y), ch, font=f, fill=tuple(color[:3]) + (a,), anchor="l" + ancla[1])
            x += d.textlength(ch, font=f) + track
        return
    if sombra:
        d.text((xy[0] + 2, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(a * .55)), anchor=ancla)
    d.text(xy, s, font=f, fill=tuple(color[:3]) + (a,), anchor=ancla)


def _ancho(s, f, track=0):
    d = ImageDraw.Draw(Image.new("L", (4, 4)))
    return sum(d.textlength(ch, font=f) + track for ch in s) - track if track else d.textlength(s, font=f)


def _img(ruta, alto=None, ancho=None, gris=False):
    """Imagen RGBA recortada a su contenido y escalada (logos y fotos con fondo transparente)."""
    k = ("img", ruta, alto, ancho, gris)
    if k not in _cache:
        im = Image.open(ruta).convert("RGBA")
        bb = im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
        if bb:
            im = im.crop(bb)
        if alto and ancho:
            esc = min(alto / im.height, ancho / im.width)
        elif alto:
            esc = alto / im.height
        else:
            esc = ancho / im.width
        im = im.resize((max(2, int(im.width * esc)), max(2, int(im.height * esc))), Image.LANCZOS)
        if gris:
            g = im.convert("LA").convert("RGBA")
            g.putalpha(im.getchannel("A"))
            im = Image.blend(g, Image.new("RGBA", g.size, (40, 44, 52, 0)), .25)
            im.putalpha(g.getchannel("A").point(lambda v: int(v * .85)))
        _cache[k] = im
    return _cache[k]


# ------------------------------------------------------------------ panel base (vidrio + filo dorado + esquina cortada)
def _panel(w, h, color, corte=None, alfa=236, sesgo=0):
    """Panel de transmisión: vidrio azul noche con degradado, filo dorado fino, esquina superior derecha cortada,
    barra del color del equipo a la izquierda y brillo arriba. `sesgo` inclina el borde izquierdo (px)."""
    corte = corte if corte is not None else max(10, h // 5)
    P = 30
    im = Image.new("RGBA", (w + 2 * P, h + 2 * P), (0, 0, 0, 0))
    forma = [(P + sesgo, P), (P + w - corte, P), (P + w, P + corte), (P + w, P + h), (P, P + h)]
    sm = Image.new("L", im.size, 0)
    ImageDraw.Draw(sm).polygon([(x + 4, y + 10) for x, y in forma], fill=170)
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sombra.putalpha(sm.filter(ImageFilter.GaussianBlur(12)))
    im.alpha_composite(sombra)
    grad = Image.new("RGBA", im.size, (0, 0, 0, 0))
    g = np.zeros((im.height, im.width, 4), np.uint8)
    t = np.linspace(0, 1, im.height)[:, None]
    g[..., 0] = (16 * (1 - t) + 6 * t)
    g[..., 1] = (26 * (1 - t) + 11 * t)
    g[..., 2] = (46 * (1 - t) + 22 * t)
    g[..., 3] = alfa
    grad = Image.fromarray(g, "RGBA")
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).polygon(forma, fill=255)
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    capa.paste(grad, (0, 0), m)
    im.alpha_composite(capa)
    d = ImageDraw.Draw(im)
    # filo dorado + brillo superior
    d.line(forma + [forma[0]], fill=ORO + (170,), width=2)
    d.line([(P + sesgo + 4, P + 3), (P + w - corte - 2, P + 3)], fill=(255, 255, 255, 46), width=2)
    # barra de color del equipo
    c = _c(color)
    d.polygon([(P + sesgo, P), (P + sesgo + 12, P), (P + 12, P + h), (P, P + h)], fill=c + (255,))
    return im, P


def _brillo_barrido(arr, u, ancho=.18):
    """Banda de luz diagonal que cruza la pieza (u 0..1), recortada a su alfa."""
    if u <= 0 or u >= 1:
        return arr
    h, w = arr.shape[:2]
    xs = np.arange(w)[None, :] + np.arange(h)[:, None] * .45
    c = (-.2 + 1.4 * u) * (w + h * .45)
    banda = np.clip(1 - np.abs(xs - c) / (ancho * w), 0, 1) ** 2 * .55
    out = arr.copy()
    k = banda[..., None] * (arr[..., 3:4] / 255)
    out[..., :3] = (arr[..., :3] * (1 - k) + 255 * k).astype(np.uint8)
    return out


# ------------------------------------------------------------------ TARJETA (tercio inferior)
def tarjeta(titulo, sub=None, color="oro", logo=None, icono=None, dato=None, tam=60, ancho=None, giro=7.0):
    """Tercio inferior de transmisión. logo = escudo del equipo (PNG transparente); icono = cuadro de campeón; dato = cifra
    grande a la derecha («0-3», «10,7»). Entra: la barra de color crece, el panel se abre de izquierda a derecha girando en
    3D, el título se revela con barrido, el subtítulo sube y la cifra rebota; luego un brillo cruza y el panel respira."""
    k = ("tar", titulo, sub, color, logo, icono, dato, tam, ancho, giro)
    if k not in _cache:
        f1, f2, f3 = fuente("Bold Condensed", tam), fuente("SemiBold Condensed", int(tam * .5)), fuente("Bold Condensed", int(tam * 1.25))
        h = int(tam * 1.5) + (int(tam * .62) if sub else 0) + 18
        caja = h - 22 if (logo or icono) else 0
        tw = max(_ancho(titulo.upper(), f1, 1), _ancho(sub.upper(), f2, 2) if sub else 0)
        dw = (_ancho(dato, f3) + 50) if dato else 0
        w = ancho or int(38 + (caja + 22 if caja else 0) + tw + 40 + dw)
        panel, P = _panel(w, h, color, sesgo=10)
        x0 = P + 30
        if caja:
            d = ImageDraw.Draw(panel)
            d.rectangle((x0 - 4, P + 11, x0 + caja + 4, P + 11 + caja), fill=(255, 255, 255, 18), outline=_c(color) + (120,), width=2)
            if logo:
                lg = _img(logo, alto=caja - 14, ancho=caja - 14)
                panel.alpha_composite(lg, (x0 + (caja - lg.width) // 2, P + 11 + (caja - lg.height) // 2))
            else:
                ic = Image.open(icono).convert("RGBA").resize((caja, caja), Image.LANCZOS)
                panel.alpha_composite(ic, (x0, P + 11))
            x0 += caja + 24
        texto = Image.new("RGBA", panel.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(texto)
        _texto(d, (x0, P + 8 + tam * .62), titulo.upper(), f1, (255, 255, 255), "lm", track=1)
        subl = Image.new("RGBA", panel.size, (0, 0, 0, 0))
        if sub:
            _texto(ImageDraw.Draw(subl), (x0 + 2, P + 8 + tam * 1.42), sub.upper(), f2, ORO_C if _c(color) == ORO else _c(color),
                   "lm", track=2)
        datol = Image.new("RGBA", panel.size, (0, 0, 0, 0))
        if dato:
            dd = ImageDraw.Draw(datol)
            xd = P + w - dw + 12
            dd.line([(xd - 14, P + 14), (xd - 14, P + h - 14)], fill=ORO + (120,), width=2)
            _texto(dd, (xd + (dw - 30) / 2, P + h / 2), dato, f3, _c(color) if color != "oro" else ORO_C, "mm")
        _cache[k] = (_np(panel), _np(texto), _np(subl), _np(datol), P, x0)
    panel, texto, subl, datol, P, x0 = _cache[k]
    H_, W_ = panel.shape[:2]

    def fn(dt, dur, marcas):
        if dt <= 0:
            return _vacio(W_, H_)
        out = _vacio(W_, H_)
        u = _eo(dt / .45)                                   # el panel se abre de izquierda a derecha
        cw = int(W_ * u)
        if cw > 2:
            out[:, :cw] = panel[:, :cw]
        ut = _eo((dt - .12) / .4)                           # barrido del título
        if ut > 0:
            tt = texto.copy()
            corte = int(x0 + (W_ - x0) * ut)
            tt[:, corte:] = 0
            _sobre(out, tt, int(-18 * (1 - ut)), 0)
        us = _eo((dt - .28) / .35)
        if us > 0:
            _sobre(out, subl, 0, int(10 * (1 - us)), us)
        if dato:
            ud = _pop(dt - .4, .4)
            if ud > .02:
                _centro(out, datol, W_ / 2, H_ / 2, 1.0, clamp(ud))
        out = _brillo_barrido(out, (dt - .45) / .6)
        if dt > 1.2:                                        # destello que recorre el filo cada ~3 s: nunca quieto
            v = ((dt - 1.2) % 3.2) / 3.2
            if v < .35:
                out = _brillo_barrido(out, v / .35, .06)
        ang = giro * (1 - _eo(dt / .6)) * 4 + giro * .35 * math.sin(dt * 1.3)
        return _perspectiva(out, ang)

    return fn


# ------------------------------------------------------------------ PEGATINA de jugador / campeón
def _base_pegatina(ruta, tam, borde=10, gris=False):
    k = ("peg", ruta, tam, borde, gris)
    if k in _cache:
        return _cache[k]
    im = Image.open(ruta).convert("RGBA")
    a = np.array(im)[..., 3]
    recorte = (a < 10).mean() > .08
    if recorte:
        im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
    esc = tam / max(im.size)
    im = im.resize((max(2, int(im.width * esc)), max(2, int(im.height * esc))), Image.LANCZOS)
    if gris:
        g = im.convert("LA").convert("RGBA")
        g.putalpha(im.getchannel("A"))
        im = Image.blend(g, Image.new("RGBA", g.size, (30, 34, 44, 255)), .2)
        im.putalpha(g.getchannel("A"))
    P = borde * 3
    lienzo = Image.new("RGBA", (im.width + 2 * P, im.height + 2 * P), (0, 0, 0, 0))
    al = Image.new("L", lienzo.size, 0)
    if recorte:
        al.paste(im.getchannel("A"), (P, P))
        al = al.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(2 * borde + 1)).filter(ImageFilter.GaussianBlur(1.1))
    else:
        ImageDraw.Draw(al).rounded_rectangle((P - borde, P - borde, P + im.width + borde, P + im.height + borde), radius=borde * 2,
                                             fill=255)
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=borde, fill=255)
        im.putalpha(m)
    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    sombra.putalpha(al.point(lambda v: int(v * .6)).filter(ImageFilter.GaussianBlur(10)))
    lienzo.alpha_composite(sombra, (6, 12))
    blanco = Image.new("RGBA", lienzo.size, (250, 248, 242, 0))
    blanco.putalpha(al)
    lienzo.alpha_composite(blanco)
    lienzo.alpha_composite(im, (P, P))
    _cache[k] = lienzo
    return lienzo


def pegatina(ruta, nombre=None, color="oro", logo=None, sub=None, tam=420, giro=-5.0, gris=False, sello=None):
    """Foto/arte recortado como pegatina (borde blanco que sigue la silueta, sombra). Entra girando con rebote, se balancea y
    flota; debajo, una placa de transmisión con el escudo del equipo, el nombre y `sub`. gris = apagado (eliminado).
    sello = (texto, i_marca): sello de goma rojo que cae encima en esa marca."""
    base = _base_pegatina(ruta, tam, gris=gris)
    placa = None
    if nombre:
        placa = tarjeta(nombre, sub, color, logo=logo, tam=40, giro=0)
    W_ = max(base.width, 560) + 80
    H_ = base.height + (120 if nombre else 0) + 60

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        s = _pop(dt, .45)
        if s <= .02:
            return out
        ang = giro * min(1.0, dt / .5) + (1 - min(1.0, dt / .5)) * -24 + 2.0 * math.sin(dt * 2.0)
        im = base.rotate(ang, resample=Image.BICUBIC, expand=True)
        k = s * (1 + .02 * math.sin(dt * 3.0))
        im = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.BILINEAR)
        fl = 6 * math.sin(dt * 1.7)
        a = _np(im)
        _centro(out, a, W_ / 2, 30 + base.height / 2 + fl)
        if placa:
            p = placa(dt - .25, dur, marcas)
            _centro(out, p, W_ / 2, base.height + 40 + p.shape[0] / 2 - 30)
        if sello and len(marcas) > sello[1]:
            _sello(out, sello[0], W_ / 2, 30 + base.height * .5, dt - marcas[sello[1]], COL["rojo"], 64)
        return out

    return fn


def _sello(out, texto, cx, cy, u, color, tam=60, ang=-9):
    """Sello de goma que cae girado desde grande y rebota (u = s desde su marca)."""
    if u <= 0:
        return
    k = ("sello", texto, color, tam, ang)
    if k not in _cache:
        f = fuente("Bold Condensed", tam)
        tw = int(_ancho(texto, f, 3))
        capa = Image.new("RGBA", (tw + 70, tam + 54), (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        d.rounded_rectangle((5, 5, capa.width - 6, capa.height - 6), 10, outline=color + (255,), width=7)
        d.rounded_rectangle((14, 14, capa.width - 15, capa.height - 15), 6, outline=color + (150,), width=2)
        _texto(d, (capa.width / 2, capa.height / 2 + 2), texto, f, color, "mm", sombra=False, track=3)
        ruido = (np.random.default_rng(7).random((capa.height, capa.width)) > .14).astype(np.uint8)   # tinta gastada
        arr = np.array(capa)
        arr[..., 3] = arr[..., 3] * ruido
        capa = Image.fromarray(arr).rotate(ang, expand=True, resample=Image.BICUBIC)
        _cache[k] = _np(capa)
    s = 2.2 - 1.2 * _pop(u, .28)
    _centro(out, _cache[k], cx, cy, s, _eo(u / .12))


# ------------------------------------------------------------------ RESULTADOS (marcadores que entran por marca)
def resultados(titulo, partidos, ancho=1240, fila=112):
    """partidos = [(logoA, nombreA, logoB, nombreB, ganador 0|1), ...]: la fila k entra deslizándose en la marca k; el ganador
    queda en blanco con su lado iluminado y una flecha; el perdedor se apaga en gris."""
    n = len(partidos)
    cab = 74
    H_ = cab + n * (fila + 12) + 40
    W_ = ancho + 60
    k = ("res", titulo, tuple(p[1] for p in partidos), ancho)
    if k not in _cache:
        filas = []
        f = fuente("Bold Condensed", 50)
        for p in partidos:                     # ganador None = cruce por jugar (27-oct): los dos encendidos y «VS» o p[5]
            la, na, lb, nb, g = p[:5]
            pn, P = _panel(ancho - 40, fila, "oro" if g is None else "azul" if g == 0 else "rojo", alfa=228)
            im = pn
            d = ImageDraw.Draw(im)
            cy = P + fila / 2
            lw = fila - 22
            for lado, (lg, nm) in enumerate(((la, na), (lb, nb))):
                gana = g is None or lado == g
                img = _img(lg, alto=lw, ancho=lw, gris=not gana)
                if lado == 0:
                    im.alpha_composite(img, (P + 34 + (lw - img.width) // 2, int(cy - img.height / 2)))
                    _texto(d, (P + 34 + lw + 22, cy), nm.upper(), f, (255, 255, 255) if gana else (120, 126, 138), "lm")
                else:
                    xr = P + ancho - 40 - 30 - lw
                    im.alpha_composite(img, (xr + (lw - img.width) // 2, int(cy - img.height / 2)))
                    _texto(d, (xr - 22, cy), nm.upper(), f, (255, 255, 255) if gana else (120, 126, 138), "rm")
            cxm = P + (ancho - 40) / 2
            fm = fuente("Bold Condensed", 34)
            d.rectangle((cxm - 62, cy - 24, cxm + 62, cy + 24), fill=ORO + (255,))
            centro = (p[5] if len(p) > 5 else "VS") if g is None else "GANA"     # ◀ ▶ no existen en Bahnschrift (salían □)
            _texto(d, (cxm, cy + 1), centro, fm, NOCHE, "mm", sombra=False)
            filas.append(_np(im))
        cabe = Image.new("RGBA", (W_, cab + 10), (0, 0, 0, 0))
        dc = ImageDraw.Draw(cabe)
        ft = fuente("Bold Condensed", 46)
        tw = _ancho(titulo.upper(), ft, 3)
        dc.polygon([(30, 8), (60 + tw, 8), (80 + tw, cab - 4), (30, cab - 4)], fill=ORO + (255,))
        _texto(dc, (46, cab / 2 + 2), titulo.upper(), ft, NOCHE, "lm", sombra=False, track=3)
        _cache[k] = (filas, _np(cabe))
    filas, cabe = _cache[k]

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        uc = _eo(dt / .35)
        if uc > 0:
            _sobre(out, cabe, int(-60 * (1 - uc)), 0, uc)
        for i, fl in enumerate(filas):
            tk = _mk(marcas, i, .4 + i * .9)
            u = _eo((dt - tk) / .4)
            if u <= 0:
                continue
            a = fl
            if 0 < dt - tk < 1.0:
                a = _brillo_barrido(fl, (dt - tk - .25) / .6)
            _sobre(out, a, int(-W_ * .5 * (1 - u)) , cab + 4 + i * (fila + 12) - 22, u)
        return out

    return fn


# ------------------------------------------------------------------ CAÍDA (equipos que se apagan uno por marca)
def caida(titulo, equipos, remate=None, tam=240, sello="DERROTA"):
    """equipos = [(logo, nombre[, vive]), ...] en medallones hexagonales; marca 0: entran todos, uno tras otro · marcas
    siguientes: un tajo rojo cruza el medallón de cada equipo que cae (en orden; los que llevan vive=True no caen y al final
    se iluminan en dorado), se apaga y cae `sello` · marca siguiente: `remate` (p. ej. «0-4») golpea al centro."""
    n = len(equipos)
    sep = tam + 70
    W_ = n * sep + 120
    H_ = tam + 300

    def hexa(cx, cy, r):
        return [(cx + r * math.cos(math.radians(60 * i + 30)), cy + r * math.sin(math.radians(60 * i + 30))) for i in range(6)]

    k = ("caida", titulo, tuple(e[1] for e in equipos), tam)
    if k not in _cache:
        meds = []
        for e in equipos:
            lg, nm = e[0], e[1]
            for gris in (False, True):
                im = Image.new("RGBA", (tam + 40, tam + 90), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                cx, cy, r = (tam + 40) / 2, tam / 2 + 20, tam / 2
                d.polygon(hexa(cx + 5, cy + 9, r), fill=(0, 0, 0, 120))
                d.polygon(hexa(cx, cy, r), fill=(14, 22, 40, 240), outline=(ORO if not gris else (90, 90, 96)) + (255,))
                d.polygon(hexa(cx, cy, r - 9), outline=(ORO if not gris else (70, 70, 76)) + (110,))
                img = _img(lg, alto=int(tam * .56), ancho=int(tam * .62), gris=gris)
                im.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))
                _texto(d, (cx, tam + 62), nm.upper(), fuente("Bold Condensed", 34), (255, 255, 255) if not gris else (130, 134, 142), "mm")
                meds.append(_np(im))
        ft = fuente("Bold Condensed", 54)
        cab = Image.new("RGBA", (W_, 90), (0, 0, 0, 0))
        _texto(ImageDraw.Draw(cab), (W_ / 2, 45), titulo.upper(), ft, ORO_C, "mm", track=4)
        _cache[k] = (meds, _np(cab))
    meds, cab = _cache[k]

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        _sobre(out, cab, 0, int(-20 * (1 - _eo(dt / .4))), _eo(dt / .4))
        t0 = _mk(marcas, 0, .2)
        caen = [i for i, e in enumerate(equipos) if not (len(e) > 2 and e[2])]
        cy = 100 + tam / 2 + 30
        for i in range(n):
            cx = 60 + sep / 2 + i * sep
            u = _pop(dt - t0 - i * .15, .4)
            if u <= .02:
                continue
            tk = _mk(marcas, caen.index(i) + 1, 99) if i in caen else 99
            if i not in caen and dt >= _mk(marcas, len(caen), 99) + .4:      # el que sobrevive: halo dorado que late
                lat = .5 + .5 * math.sin(dt * 5)
                cv2.circle(out, (int(cx), int(cy)), int(tam * .56), ORO[::-1] + (int(120 + 100 * lat),), 6, cv2.LINE_AA)
            caido = dt >= tk
            m = meds[2 * i + (1 if caido and dt - tk > .12 else 0)]
            temblor = 9 * math.exp(-(dt - tk) * 9) * math.sin((dt - tk) * 60) if caido else 0
            fl = 4 * math.sin(dt * 1.6 + i)
            _centro(out, m, cx + temblor, cy + fl, u)
            if caido:                                       # tajo rojo que cruza
                v = _eo((dt - tk) / .18)
                x1, y1 = cx - tam * .5, cy - tam * .45
                x2, y2 = x1 + (tam) * v, y1 + tam * .9 * v
                cv2.line(out, (int(x1), int(y1)), (int(x2), int(y2)), (60, 50, 255, 255), 14, cv2.LINE_AA)
                cv2.line(out, (int(x1), int(y1)), (int(x2), int(y2)), (200, 200, 255, 255), 4, cv2.LINE_AA)
                _sello(out, sello, cx, cy + tam * .55, dt - tk - .1, COL["rojo"], 36, -6)
        tr = _mk(marcas, len(caen) + 1, 99)
        if remate and dt >= tr:
            _sello(out, remate, W_ / 2, cy, dt - tr, COL["rojo"], 150, -7)
        return out

    return fn


# ------------------------------------------------------------------ ELIMINADO (el escudo se parte)
def eliminado(logo, nombre, sub=None, tam=420):
    """El escudo entra grande con halo dorado; en la marca 0 se parte en esquirlas que se separan y se apaga en gris; en la
    marca 1 cae el sello rojo «ELIMINADO»; abajo, placa con `nombre` y `sub`."""
    lg = _img(logo, alto=tam, ancho=tam)
    lgg = _img(logo, alto=tam, ancho=tam, gris=True)
    W_, H_ = tam + 360, tam + 260
    rng = np.random.default_rng(3)
    cortes = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
    placa = tarjeta(nombre, sub, "rojo", tam=46, giro=0)

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        cx, cy = W_ / 2, 30 + tam / 2 + 20
        t0, t1 = _mk(marcas, 0, 1.2), _mk(marcas, 1, 2.0)
        s = _pop(dt, .5)
        if s <= .02:
            return out
        if dt < t0:                                        # halo dorado que late detrás
            halo = np.zeros((H_, W_), np.float32)
            cv2.circle(halo, (int(cx), int(cy)), int(tam * .55), 1.0, -1)
            halo = cv2.GaussianBlur(halo, (0, 0), 40) * (.55 + .2 * math.sin(dt * 4))
            capa = np.zeros((H_, W_, 4), np.uint8)
            capa[..., 0], capa[..., 1], capa[..., 2] = ORO[2], ORO[1], ORO[0]
            capa[..., 3] = (halo * 255).clip(0, 255).astype(np.uint8)
            _sobre(out, capa, 0, 0)
            _centro(out, _np(lg), cx, cy + 5 * math.sin(dt * 1.8), s)
        else:                                              # esquirlas: bandas diagonales que se separan
            u = _eo((dt - t0) / .7)
            src = _np(lgg if dt - t0 > .15 else lg)
            h, w = src.shape[:2]
            nb = 6
            for b in range(nb):
                m = np.zeros((h, w), np.uint8)
                y0, y1 = int(h * b / nb), int(h * (b + 1) / nb)
                pts = np.array([(0, y0 - 30 + 15 * b % 40), (w, y0 + 30), (w, y1 + 30), (0, y1 - 30 + 15 * (b + 1) % 40)], np.int32)
                cv2.fillPoly(m, [pts], 255)
                pz = src.copy()
                pz[..., 3] = (pz[..., 3].astype(np.uint16) * m // 255).astype(np.uint8)
                dx, dy = cortes[b]
                _centro(out, pz, cx + dx * 40 * u, cy + dy * 18 * u + (b - nb / 2) * 6 * u)
            if dt - t0 < .12:
                _sobre(out, np.dstack([np.full((H_, W_), 255, np.uint8)] * 3 + [np.full((H_, W_), int(140 * (1 - (dt - t0) / .12)), np.uint8)]), 0, 0)
        if dt >= t1:
            _sello(out, "ELIMINADO", cx, cy, dt - t1, COL["rojo"], 96, -8)
        p = placa(dt - .35, dur, marcas)
        _centro(out, p, cx, cy + tam / 2 + 70)
        return out

    return fn


# ------------------------------------------------------------------ APERTURA (portada en frío)
def apertura(titulo, sub=None, ancho=1920, alto=1080):
    """A pantalla completa sobre el clip: velo oscuro, destellos dorados que cruzan, el título golpea desde grande con
    aberración cromática y se asienta; el subtítulo se escribe; la línea dorada se abre a los lados; todo sale hacia arriba."""
    ft, fs = fuente("Bold Condensed", 210), fuente("SemiBold Condensed", 54)
    k = ("ap", titulo, sub)
    if k not in _cache:
        tw = int(_ancho(titulo, ft, 10)) + 80
        t = Image.new("RGBA", (tw, 260), (0, 0, 0, 0))
        _texto(ImageDraw.Draw(t), (tw / 2, 130), titulo, ft, (255, 255, 255), "mm", track=10)
        _cache[k] = _np(t)
    tit = _cache[k]
    rng = np.random.default_rng(11)
    rayas = [(rng.uniform(0, 1), rng.uniform(.15, .85), rng.uniform(.6, 1.6), rng.uniform(.0, .8)) for _ in range(16)]

    def fn(dt, dur, marcas):
        out = _vacio(ancho, alto)
        sal = _eo((dt - (dur - .45)) / .45) if dur else 0
        velo = int(150 * _eo(dt / .3) * (1 - sal))
        out[..., 3] = velo
        for x0, y, vel, t0 in rayas:                       # destellos dorados
            u = (dt - t0) * vel
            if 0 < u < 1.2:
                x = int((-.3 + 1.6 * u) * ancho)
                cv2.line(out, (x - 260, int(y * alto)), (x, int(y * alto)), (110, 170, 200, 255), 3, cv2.LINE_AA)
                cv2.circle(out, (x, int(y * alto)), 5, (220, 240, 255, 255), -1, cv2.LINE_AA)
        cy = alto * .44 - 120 * sal
        u = _eo((dt - .15) / .35)
        if u > 0:
            esc = 1.6 - .6 * u
            if dt - .15 < .45:                             # aberración cromática del golpe
                gl = tit.copy()
                d = int(16 * (1 - u))
                r = np.roll(gl, d, axis=1)
                r[..., :2] = 0
                b = np.roll(gl, -d, axis=1)
                b[..., 1:3] = 0
                _centro(out, r, ancho / 2, cy, esc, .8 * u)
                _centro(out, b, ancho / 2, cy, esc, .8 * u)
            _centro(out, _brillo_barrido(tit, (dt - .5) / .7), ancho / 2, cy, esc, u * (1 - sal))
        ul = _eo((dt - .45) / .5)
        if ul > 0:
            half = int(620 * ul)
            yl = int(cy + 130)
            cv2.line(out, (ancho // 2 - half, yl), (ancho // 2 + half, yl), ORO[::-1] + (int(255 * (1 - sal)),), 4, cv2.LINE_AA)
        if sub:
            n = int(len(sub) * clamp((dt - .7) / .9))
            if n > 0:
                im = Image.new("RGBA", (ancho, 90), (0, 0, 0, 0))
                _texto(ImageDraw.Draw(im), (ancho / 2, 45), sub[:n].upper(), fs, ORO_C, "mm", alfa=255 * (1 - sal), track=6)
                _sobre(out, _np(im), 0, int(cy + 150))
        return out

    return fn


# ------------------------------------------------------------------ VERSUS (dos escudos chocan)
def versus(a, b, titulo=None, sub=None, ganador=None, tam=300):
    """a, b = (logo, nombre). Los escudos entran desde los lados y chocan en el centro (destello + «VS» que golpea); en la
    marca 0, si hay `ganador` (0|1), el perdedor se apaga y el ganador crece con halo."""
    W_, H_ = 2 * tam + 520, tam + 230
    la, lb = _img(a[0], alto=tam, ancho=tam), _img(b[0], alto=tam, ancho=tam)
    lag, lbg = _img(a[0], alto=tam, ancho=tam, gris=True), _img(b[0], alto=tam, ancho=tam, gris=True)
    fn_t = tarjeta(titulo, sub, "oro", tam=44, giro=0) if titulo else None
    fv = fuente("Bold Condensed", 150)

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        u = _eo(dt / .4)
        cy = 40 + tam / 2
        t0 = _mk(marcas, 0, 99)
        dec = ganador is not None and dt >= t0
        for lado, (img, imgg) in enumerate(((la, lag), (lb, lbg))):
            pierde = dec and lado != ganador
            gana = dec and lado == ganador
            x = (W_ / 2 - tam * .75 - 60) if lado == 0 else (W_ / 2 + tam * .75 + 60)
            x += (-1 if lado == 0 else 1) * (1 - u) * W_ * .5
            esc = 1.0 + (.12 * _eo((dt - t0) / .3) if gana else 0) - (.12 * _eo((dt - t0) / .3) if pierde else 0)
            _centro(out, _np(imgg if pierde else img), x, cy + 5 * math.sin(dt * 2 + lado), esc)
        if dt > .35:                                       # choque: destello y VS
            v = _pop(dt - .35, .35)
            im = Image.new("RGBA", (360, 220), (0, 0, 0, 0))
            _texto(ImageDraw.Draw(im), (180, 110), "VS", fv, ORO_C, "mm")
            _centro(out, _np(im), W_ / 2, cy, 1.4 - .4 * clamp(v), clamp(v))
            if dt - .35 < .15:
                f = int(255 * (1 - (dt - .35) / .15))
                cv2.circle(out, (int(W_ / 2), int(cy)), int(220 * (dt - .35) / .15 + 20), (255, 255, 255, f), -1, cv2.LINE_AA)
        if fn_t:
            p = fn_t(dt - .5, dur, marcas)
            _centro(out, p, W_ / 2, H_ - p.shape[0] / 2 - 4)
        return out

    return fn


# ------------------------------------------------------------------ MENÚ (mosaicos que giran en 3D)
def menu(items, tam=(340, 420)):
    """items = [(imagen, titulo, color), ...]: mosaicos con la imagen recortada (arte de campeón, jugador, escudo...) que
    giran desde 90° hasta quedar de frente, uno por marca; el último encendido late con borde dorado."""
    w, h = tam
    n = len(items)
    sep = w + 40
    W_, H_ = n * sep + 80, h + 120
    k = ("menu", tuple(i[1] for i in items), tam)
    if k not in _cache:
        tiles = []
        for ruta, tit, col in items:
            im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            fondo = Image.open(ruta).convert("RGBA")
            transp = (np.array(fondo)[..., 3] < 10).mean() > .08
            caja = Image.new("RGBA", (w, h - 90), (14, 22, 40, 255))
            if transp:
                img = _img(ruta, alto=h - 120, ancho=w - 40)
                caja.alpha_composite(img, ((w - img.width) // 2, h - 90 - img.height))
            else:
                esc = max(w / fondo.width, (h - 90) / fondo.height)
                f2 = fondo.resize((int(fondo.width * esc) + 1, int(fondo.height * esc) + 1), Image.LANCZOS)
                caja = f2.crop(((f2.width - w) // 2, 0, (f2.width - w) // 2 + w, h - 90))
            im.paste(caja, (0, 0))
            d = ImageDraw.Draw(im)
            d.rectangle((0, h - 90, w, h), fill=(10, 16, 30, 245))
            d.rectangle((0, h - 90, w, h - 84), fill=_c(col) + (255,))
            _texto(d, (w / 2, h - 42), tit.upper(), fuente("Bold Condensed", 40), (255, 255, 255), "mm", track=2)
            d.rectangle((0, 0, w - 1, h - 1), outline=ORO + (200,), width=3)
            tiles.append(_np(im))
        _cache[k] = tiles
    tiles = _cache[k]

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        for i, t in enumerate(tiles):
            tk = _mk(marcas, i, .3 + i * .6)
            u = _eo((dt - tk) / .5)
            if u <= 0:
                continue
            ang = 85 * (1 - u) + 3 * math.sin(dt * 1.4 + i)
            pz = _perspectiva(t, ang)
            if 0 < dt - tk < 1.0:
                pz = _brillo_barrido(pz, (dt - tk - .2) / .6)
            cx = 40 + sep / 2 + i * sep
            _centro(out, pz, cx, 50 + h / 2 + 6 * math.sin(dt * 1.6 + i * .8) - 30 * (1 - u), 1, u)
        return out

    return fn


# ------------------------------------------------------------------ SUIZA (el formato)
def suiza(titulo="FASE SUIZA", ancho=1500, alto=640):
    """El formato suizo como árbol de récords: 0-0 → 1-0/0-1 → 2-0/1-1/0-2 → 3-0 … 0-3. Marcas: 0 aparece el 0-0 y salen
    las flechas de la primera ronda · 1 segunda ronda · 2 tercera ronda · 3 se enciende 3-0 en azul «CUARTOS» · 4 se
    enciende 0-3 en rojo «ELIMINADO» · 5 los 2-1 / 1-2 / 2-2 laten en oro «AL MEJOR DE 3»."""
    cols = [["0-0"], ["1-0", "0-1"], ["2-0", "1-1", "0-2"], ["3-0", "2-1", "1-2", "0-3"], ["3-1", "2-2", "1-3"], ["3-2", "2-3"]]
    nodo_w, nodo_h = 150, 66

    def pos(c, i):
        n = len(cols[c])
        x = 90 + c * (ancho - 180) / (len(cols) - 1)
        y = 110 + (alto - 170) * (i + .5) / n
        return x, y

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        ub = _eo(dt / .4)
        d.rounded_rectangle((0, 0, ancho - 1, alto - 1), 18, fill=(8, 14, 28, int(220 * ub)), outline=ORO + (int(160 * ub),), width=2)
        _texto(d, (ancho / 2, 52), titulo.upper(), fuente("Bold Condensed", 54), ORO_C, "mm", alfa=255 * ub, track=5)
        tm = [_mk(marcas, i, .5 + i * 1.2) for i in range(6)]
        fn_ = fuente("Bold Condensed", 40)
        for c, col in enumerate(cols):
            t_ap = [tm[0], tm[0] + .5, tm[1], tm[2], tm[5], tm[5] + .4][c]
            u = _eo((dt - t_ap) / .45)
            if u <= 0:
                continue
            for i, rec in enumerate(col):
                x, y = pos(c, i)
                if c > 0:                                  # flechas desde los nodos de la columna anterior
                    for j, prev in enumerate(cols[c - 1]):
                        w0, l0 = map(int, prev.split("-"))
                        w1, l1 = map(int, rec.split("-"))
                        if (w1, l1) in ((w0 + 1, l0), (w0, l0 + 1)) and w0 < 3 and l0 < 3:
                            x0, y0 = pos(c - 1, j)
                            xa, ya = x0 + nodo_w / 2, y0
                            xb = xa + (x - nodo_w / 2 - xa) * u
                            yb = ya + (y - ya) * u
                            d.line([(xa, ya), (xb, yb)], fill=(150, 160, 180, 170), width=3)
                w_, l_ = map(int, rec.split("-"))
                col_n = (24, 34, 56)
                borde = ORO
                if w_ == 3 and dt >= tm[3]:
                    col_n, borde = (30, 90, 170), COL["azul"]
                elif l_ == 3 and dt >= tm[4]:
                    col_n, borde = (130, 26, 36), COL["rojo"]
                lat = 0
                if w_ < 3 and l_ < 3 and (w_ == 2 or l_ == 2) and dt >= tm[5]:
                    lat = .5 + .5 * math.sin((dt - tm[5]) * 5)
                    borde = ORO_C
                a = int(255 * u)
                d.rounded_rectangle((x - nodo_w / 2, y - nodo_h / 2, x + nodo_w / 2, y + nodo_h / 2), 12,
                                    fill=col_n + (int(235 * u),), outline=borde + (a,), width=3 + int(3 * lat))
                _texto(d, (x, y + 2), rec, fn_, (255, 255, 255), "mm", alfa=a)
        f2 = fuente("Bold Condensed", 34)
        if dt >= tm[3]:
            x, y = pos(3, 0)
            _texto(d, (x, y - 58), "CUARTOS", f2, COL["azul"], "mm", alfa=255 * _eo((dt - tm[3]) / .3))
        if dt >= tm[4]:
            x, y = pos(3, 3)
            _texto(d, (x, y + 58), "ELIMINADO", f2, COL["rojo"], "mm", alfa=255 * _eo((dt - tm[4]) / .3))
        if dt >= tm[5]:
            _texto(d, (ancho - 40, alto - 34), "AL MEJOR DE 3: CUANDO HAY PASE O ELIMINACIÓN", fuente("SemiBold Condensed", 30),
                   ORO_C, "rm", alfa=255 * _eo((dt - tm[5]) / .4))
        arr = _np(im)
        return _perspectiva(arr, 4 * math.sin(dt * .9))

    return fn


# ================================================================== MG NUEVOS del resumen de la Worlds (27-oct-2026, tramo 3)
def _cabecera(titulo, ancho):
    """Chip dorado con el título (como el de `resultados`)."""
    k = ("cab", titulo, ancho)
    if k not in _cache:
        cab = 74
        im = Image.new("RGBA", (ancho, cab + 10), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        ft = fuente("Bold Condensed", 46)
        tw = _ancho(titulo.upper(), ft, 3)
        d.polygon([(30, 8), (60 + tw, 8), (80 + tw, cab - 4), (30, cab - 4)], fill=ORO + (255,))
        _texto(d, (46, cab / 2 + 2), titulo.upper(), ft, NOCHE, "lm", sombra=False, track=3)
        _cache[k] = _np(im)
    return _cache[k]


def ficha_jugador(foto, nombre, logo, numero, stats, color="oro", sub=None, W_=1240, H_=600):
    """Top de jugadores: panel de vidrio con la FOTO recortada que sube por la izquierda, «N.º k» en oro, el nombre que se
    revela con barrido, escudo + `sub` y filas de estadística (etiqueta, valor, fracción 0..1) cuya barra se llena en la marca
    i (marcas[0] = la primera fila). Respira en 3D como la tarjeta."""
    k = ("ficha", foto, nombre, numero, tuple(s[0] for s in stats), color)
    pw, ph, px, py = 860, 430, W_ - 860 - 40, H_ - 430 - 30
    filas_y = [py + 222 + i * 74 for i in range(len(stats))]
    bx0, bx1 = px + 300, px + 680
    c = _c(color)
    if k not in _cache:
        panel, P = _panel(pw, ph, color, sesgo=14)
        base = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        base.alpha_composite(panel, (px - P, py - P))
        d = ImageDraw.Draw(base)
        x0 = px + 300
        fn_ = fuente("Bold Condensed", 40)
        d.polygon([(x0, py + 26), (x0 + 150, py + 26), (x0 + 166, py + 70), (x0, py + 70)], fill=ORO + (255,))
        _texto(d, (x0 + 14, py + 49), f"N.º {numero}", fn_, NOCHE, "lm", sombra=False, track=2)
        if logo:
            lg = _img(logo, alto=46, ancho=46)
            base.alpha_composite(lg, (x0 + 190, py + 26 + (46 - lg.height) // 2))
        if sub:
            _texto(d, (x0 + 250, py + 49), sub.upper(), fuente("SemiBold Condensed", 30), ORO_C, "lm", track=2)
        fe = fuente("SemiBold Condensed", 30)
        fv = fuente("Bold Condensed", 38)
        for (et, val, fr), y in zip(stats, filas_y):
            _texto(d, (bx0, y - 26), et.upper(), fe, (210, 216, 228), "lm", track=1)
            d.rounded_rectangle((bx0, y - 4, bx1, y + 18), 6, fill=(255, 255, 255, 30))
        nombre_l = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        _texto(ImageDraw.Draw(nombre_l), (x0, py + 128), nombre.upper(), fuente("Bold Condensed", 104), (255, 255, 255), "lm", track=2)
        vals = []
        for (et, val, fr), y in zip(stats, filas_y):
            v = Image.new("RGBA", (220, 60), (0, 0, 0, 0))
            _texto(ImageDraw.Draw(v), (6, 30), val, fv, c if color != "oro" else ORO_C, "lm")
            vals.append(_np(v))
        foto_i = _base_pegatina(foto, 470, borde=8)
        _cache[k] = (_np(base), _np(nombre_l), vals, _np(foto_i))
    base, nombre_l, vals, foto_i = _cache[k]

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        if dt <= 0:
            return out
        u = _eo(dt / .45)
        cw = int(px - 30 + (W_ - px + 30) * u)
        out[:, :cw] = base[:, :cw]
        un = _eo((dt - .2) / .45)
        if un > 0:
            nl = nombre_l.copy()
            nl[:, int(px + 300 + (W_ - px - 300) * un):] = 0
            _sobre(out, nl, int(-24 * (1 - un)), 0)
        for i, ((et, val, fr), y) in enumerate(zip(stats, filas_y)):
            tk = _mk(marcas, i, .7 + .55 * i)
            ub = _eo((dt - tk) / .6)
            if ub <= 0:
                continue
            xe = int(bx0 + (bx1 - bx0) * fr * ub)
            if xe > bx0 + 4:
                cv2.rectangle(out, (bx0, y - 3), (xe, y + 17), c[::-1] + (255,), -1)
                cv2.rectangle(out, (bx0, y - 3), (xe, y + 2), (255, 255, 255, 140), -1)
            _sobre(out, vals[i], bx1 + 16, y - 22, clamp((dt - tk) / .3))
        s = _pop(dt - .1, .5)
        if s > .02:
            fl = 5 * math.sin(dt * 1.6)
            _centro(out, foto_i, 40 + foto_i.shape[1] * .42, H_ - foto_i.shape[0] / 2 - 10 + fl + 60 * (1 - min(1, s)), min(1.0, s) * (1 + .015 * math.sin(dt * 2.4)))
        out = _brillo_barrido(out, (dt - .5) / .7)
        ang = 6 * (1 - _eo(dt / .6)) * 3 + 2.2 * math.sin(dt * 1.2)
        return _perspectiva(out, ang)

    return fn


def ranking(titulo, filas, ancho=1180, fila=104):
    """Ranking de equipos: filas = [(logo, nombre, dato, sub, color), ...]; la fila k entra en la marca k con su número de
    puesto en un rombo dorado que rebota; `dato` (récord) a la derecha; la última encendida late."""
    n = len(filas)
    cab = 74
    H_ = cab + n * (fila + 12) + 40
    W_ = ancho + 60
    k = ("rank", titulo, tuple(f[1] for f in filas), ancho)
    if k not in _cache:
        ims = []
        fnm, fsb, fdt, fno = (fuente("Bold Condensed", 52), fuente("SemiBold Condensed", 28), fuente("Bold Condensed", 56),
                              fuente("Bold Condensed", 60))
        for i, (lg, nm, dato, sub, col) in enumerate(filas):
            pn, P = _panel(ancho - 40, fila, col, alfa=230)
            d = ImageDraw.Draw(pn)
            cy = P + fila / 2
            cx = P + 70
            d.polygon([(cx, cy - 44), (cx + 44, cy), (cx, cy + 44), (cx - 44, cy)], fill=ORO + (255,))
            _texto(d, (cx, cy + 2), str(i + 1), fno, NOCHE, "mm", sombra=False)
            img = _img(lg, alto=fila - 24, ancho=fila - 24)
            pn.alpha_composite(img, (P + 140 + (fila - 24 - img.width) // 2, int(cy - img.height / 2)))
            xt = P + 140 + fila
            _texto(d, (xt, cy - (14 if sub else 0)), nm.upper(), fnm, (255, 255, 255), "lm", track=1)
            if sub:
                _texto(d, (xt + 2, cy + 28), sub.upper(), fsb, ORO_C, "lm", track=1)
            if dato:
                _texto(d, (P + ancho - 40 - 36, cy + 2), dato, fdt, _c(col) if col != "oro" else ORO_C, "rm")
            ims.append(_np(pn))
        _cache[k] = ims
    ims = _cache[k]
    cabe = _cabecera(titulo, W_)

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        uc = _eo(dt / .35)
        if uc > 0:
            _sobre(out, cabe, int(-60 * (1 - uc)), 0, uc)
        ult = -1
        for i, fl in enumerate(ims):
            tk = _mk(marcas, i, .4 + i * .9)
            u = _eo((dt - tk) / .4)
            if u <= 0:
                continue
            ult = i
            a = _brillo_barrido(fl, (dt - tk - .2) / .6) if 0 < dt - tk < 1 else fl
            _sobre(out, a, int(W_ * .45 * (1 - u)), cab + 4 + i * (fila + 12) - 22, u)
        return out

    return fn


def tabla(titulo, columnas, ancho_col=470, fila=86):
    """Tabla por récord: columnas = [(encabezado, color, [(logo, nombre), ...]), ...]. La columna i sube en la marca i y sus
    equipos entran uno tras otro (0,22 s)."""
    nmax = max(len(c[2]) for c in columnas)
    cab = 74
    W_ = len(columnas) * (ancho_col + 30) + 60
    H_ = cab + 110 + nmax * (fila + 10) + 50
    k = ("tabla", titulo, tuple(c[0] for c in columnas), tuple(len(c[2]) for c in columnas))
    if k not in _cache:
        cols = []
        for enc, col, eqs in columnas:
            hd, P = _panel(ancho_col - 20, 90, col, alfa=240)
            _texto(ImageDraw.Draw(hd), (P + (ancho_col - 20) / 2, P + 47), enc.upper(), fuente("Bold Condensed", 58),
                   _c(col) if col != "oro" else ORO_C, "mm", track=2)
            filas = []
            for lg, nm in eqs:
                pn, P2 = _panel(ancho_col - 20, fila, col, alfa=215)
                d = ImageDraw.Draw(pn)
                img = _img(lg, alto=fila - 22, ancho=fila - 22)
                pn.alpha_composite(img, (P2 + 30 + (fila - 22 - img.width) // 2, P2 + (fila - img.height) // 2))
                _texto(d, (P2 + 30 + fila, P2 + fila / 2), nm.upper(), fuente("Bold Condensed", 42), (255, 255, 255), "lm", track=1)
                filas.append(_np(pn))
            cols.append((_np(hd), filas))
        _cache[k] = cols
    cols = _cache[k]
    cabe = _cabecera(titulo, W_)

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        uc = _eo(dt / .35)
        if uc > 0:
            _sobre(out, cabe, int(-60 * (1 - uc)), 0, uc)
        for i, (hd, filas) in enumerate(cols):
            tk = _mk(marcas, i, .4 + i * 1.2)
            x = 30 + i * (ancho_col + 30) - 30
            u = _eo((dt - tk) / .4)
            if u <= 0:
                continue
            _sobre(out, hd, x, cab + 10 + int(60 * (1 - u)) - 30, u)
            for j, fl in enumerate(filas):
                uj = _pop(dt - tk - .3 - .22 * j, .4)
                if uj <= .02:
                    continue
                a = _brillo_barrido(fl, (dt - tk - .4 - .22 * j) / .5)
                _centro(out, a, x + fl.shape[1] / 2, cab + 120 + j * (fila + 10) + fl.shape[0] / 2 - 10, min(1.0, uj), clamp(uj * 2))
        return out

    return fn


def calendario(titulo, hitos, ancho=1640, alto=420):
    """Línea de tiempo: hitos = [(fecha, texto, color), ...]. La línea dorada se dibuja; en la marca k el nodo k rebota con su
    fecha arriba y su texto abajo; el último (la final) brilla con halo."""
    W_, H_ = ancho, alto
    n = len(hitos)
    xs = [140 + i * (W_ - 280) / max(1, n - 1) for i in range(n)]
    yl = H_ * .52
    k = ("cal", titulo, tuple(h[0] for h in hitos), ancho)
    if k not in _cache:
        nodos = []
        for fe, tx, col in hitos:
            c = _c(col)
            im = Image.new("RGBA", (380, 330), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.ellipse((190 - 30, 165 - 30, 190 + 30, 165 + 30), fill=NOCHE + (255,), outline=c + (255,), width=7)
            d.ellipse((190 - 13, 165 - 13, 190 + 13, 165 + 13), fill=c + (255,))
            fw = _ancho(fe.upper(), fuente("Bold Condensed", 46), 2)
            d.rounded_rectangle((190 - fw / 2 - 18, 52, 190 + fw / 2 + 18, 112), 8, fill=c + (255,))
            _texto(d, (190, 83), fe.upper(), fuente("Bold Condensed", 46), NOCHE, "mm", sombra=False, track=2)
            for j, linea in enumerate(tx.upper().split("\n")):
                _texto(d, (190, 228 + j * 40), linea, fuente("SemiBold Condensed", 36), (255, 255, 255), "mm", track=1)
            nodos.append(_np(im))
        pn, P = _panel(W_ - 80, H_ - 120, "oro", alfa=215, sesgo=16)
        _cache[k] = (nodos, _np(pn), P)
    nodos, fondo_p, Pp = _cache[k]
    cabe = _cabecera(titulo, W_)

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        uc = _eo(dt / .35)
        if uc > 0:
            _sobre(out, cabe, int(-60 * (1 - uc)), 0, uc)
        uf = _eo((dt - .05) / .45)
        if uf > 0:
            fp = fondo_p.copy()
            fp[:, int(fp.shape[1] * uf):] = 0
            _sobre(out, fp, 40 - Pp, 96 - Pp)
        tks = [_mk(marcas, i, .4 + i * .8) for i in range(n)]
        ul = _eo((dt - .2) / .5)
        if ul > 0:
            x1 = int(xs[0] - 60 + (xs[-1] + 60 - xs[0] + 60) * ul)
            cv2.line(out, (int(xs[0] - 60), int(yl)), (x1, int(yl)), ORO[::-1] + (120,), 4, cv2.LINE_AA)
        for i in range(1, n):
            up = _eo((dt - tks[i] + .35) / .35)
            if up > 0:
                xa = int(xs[i - 1] + (xs[i] - xs[i - 1]) * up)
                cv2.line(out, (int(xs[i - 1]), int(yl)), (xa, int(yl)), ORO_C[::-1] + (255,), 9, cv2.LINE_AA)
        for i, nd in enumerate(nodos):
            s = _pop(dt - tks[i], .45)
            if s <= .02:
                continue
            if i == n - 1 and dt - tks[i] > .5:
                r = int(40 + 14 * (.5 + .5 * math.sin(dt * 4)))
                halo = _vacio(2 * r + 4, 2 * r + 4)
                cv2.circle(halo, (r + 2, r + 2), r, _c(hitos[i][2])[::-1] + (90,), 6, cv2.LINE_AA)
                _centro(out, halo, xs[i], yl)
            _centro(out, nd, xs[i], yl, min(1.0, s), clamp(s * 2))
        return out

    return fn


def barras(titulo, items, total, ancho=1340, fila=92):
    """Barras de picks: items = [(icono, nombre, valor), ...]; la barra k crece en la marca k hasta valor/total, con el icono
    del campeón y «valor de total» al final. La primera (la mayor) en oro, el resto en azul."""
    n = len(items)
    cab = 74
    W_, H_ = ancho + 60, cab + 30 + n * (fila + 14) + 30
    x0, x1 = 360, ancho - 140
    k = ("barras", titulo, tuple(i[1] for i in items), total)
    if k not in _cache:
        filas = []
        for j, (ic, nm, v) in enumerate(items):
            im = Image.new("RGBA", (W_, fila), (0, 0, 0, 0))
            pn, P = _panel(W_ - 50, fila - 4, "oro" if j == 0 else "azul", alfa=220)
            im.alpha_composite(pn.crop((P, P - 2, P + W_ - 50, P - 2 + fila)), (20, 0))
            d = ImageDraw.Draw(im)
            ico = Image.open(ic).convert("RGBA").resize((fila - 10, fila - 10), Image.LANCZOS)
            d.rectangle((38, 3, 38 + fila - 4, fila - 3), outline=ORO + (255,), width=3)
            im.alpha_composite(ico, (40, 5))
            _texto(d, (60 + fila, fila / 2), nm.upper(), fuente("Bold Condensed", 46), (255, 255, 255), "lm", track=1)
            d.rounded_rectangle((x0, fila / 2 - 18, x1, fila / 2 + 18), 8, fill=(255, 255, 255, 26))
            et = Image.new("RGBA", (240, fila), (0, 0, 0, 0))
            _texto(ImageDraw.Draw(et), (10, fila / 2), f"{v} DE {total}", fuente("Bold Condensed", 44),
                   ORO_C if j == 0 else (255, 255, 255), "lm")
            filas.append((_np(im), _np(et)))
        _cache[k] = filas
    filas = _cache[k]
    cabe = _cabecera(titulo, W_)

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        uc = _eo(dt / .35)
        if uc > 0:
            _sobre(out, cabe, int(-60 * (1 - uc)), 0, uc)
        for j, ((im, et), (ic, nm, v)) in enumerate(zip(filas, items)):
            tk = _mk(marcas, j, .4 + .7 * j)
            u = _eo((dt - tk) / .35)
            if u <= 0:
                continue
            y = cab + 30 + j * (fila + 14)
            _sobre(out, im, int(-80 * (1 - u)), y, u)
            ub = _eo((dt - tk - .15) / .7)
            xe = int(x0 + (x1 - x0) * v / total * ub)
            if xe > x0 + 4:
                col = ORO if j == 0 else COL["azul"]
                cv2.rectangle(out, (x0, int(y + fila / 2 - 16)), (xe, int(y + fila / 2 + 16)), col[::-1] + (255,), -1)
                cv2.rectangle(out, (x0, int(y + fila / 2 - 16)), (xe, int(y + fila / 2 - 9)), (255, 255, 255, 120), -1)
            if ub > .6:
                _sobre(out, et, min(xe + 16, x1 + 10), y, clamp((ub - .6) / .3))
        return out

    return fn


# ================================================================== DUELO POR POSICIÓN (28-oct-2026, `cfo_kc_worlds`)
def duelo(a, b, titulo, filas, W_=1760, H_=700):
    """Cara a cara de dos jugadores de la misma posición (previa de un partido). a, b = (foto, nombre, logo, color, sub).
    filas = [(etiqueta, valor_a, valor_b, frac_a, frac_b, mejor)] con mejor = 0|1|None: la fila k entra en la marca k; las
    barras crecen desde el centro hacia cada jugador y la del mejor brilla con su color. Las fotos suben desde abajo, el
    título dorado cae en el centro y la pieza respira en 3D como la tarjeta."""
    k = ("duelo", a[1], b[1], titulo, tuple(f[0] for f in filas))
    fw = 430                                                   # ancho de cada foto
    cx = W_ / 2
    y0, paso = 210, 92
    bw = 260                                                   # largo máximo de cada barra
    if k not in _cache:
        panel, P = _panel(W_ - 2 * fw + 40, 120 + len(filas) * paso + 40, "oro", sesgo=10)
        base = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        base.alpha_composite(panel, (int(fw - 20 - P), int(y0 - 90 - P)))
        d = ImageDraw.Draw(base)
        fe = fuente("SemiBold Condensed", 30)
        for i, f in enumerate(filas):
            y = y0 + 30 + i * paso
            _texto(d, (cx, y - 30), f[0].upper(), fe, (210, 216, 228), "mm", track=2)
            d.rounded_rectangle((cx - bw - 8, y - 4, cx - 8, y + 16), 6, fill=(255, 255, 255, 28))
            d.rounded_rectangle((cx + 8, y - 4, cx + bw + 8, y + 16), 6, fill=(255, 255, 255, 28))
        fv = fuente("Bold Condensed", 40)
        vals = []
        for f in filas:
            par = []
            for lado in (0, 1):
                v = Image.new("RGBA", (200, 60), (0, 0, 0, 0))
                col = _c((a, b)[lado][3]) if f[5] == lado else (235, 238, 245)
                _texto(ImageDraw.Draw(v), (100, 30), str(f[1 + lado]), fv, col, "mm")
                par.append(_np(v))
            vals.append(par)
        fotos, placas = [], []
        for foto, nombre, logo, color, sub in (a, b):
            fotos.append(_np(_base_pegatina(foto, 400, borde=8)))
            pl = Image.new("RGBA", (fw, 130), (0, 0, 0, 0))
            dp = ImageDraw.Draw(pl)
            c = _c(color)
            dp.polygon([(14, 10), (fw - 14, 10), (fw - 34, 120), (34, 120)], fill=NOCHE + (235,), outline=c + (255,))
            dp.rectangle((14, 10, fw - 14, 18), fill=c + (255,))
            x = fw / 2
            if logo:
                lg = _img(logo, alto=50, ancho=50)
                pl.alpha_composite(lg, (40, 46))
            _texto(dp, (x + 20, 56), nombre.upper(), fuente("Bold Condensed", 54), (255, 255, 255), "mm", track=2)
            if sub:
                _texto(dp, (x + 20, 98), sub.upper(), fuente("SemiBold Condensed", 26), ORO_C, "mm", track=2)
            placas.append(_np(pl))
        cab = _cabecera(titulo, 760)
        _cache[k] = (_np(base), vals, fotos, placas, cab)
    base, vals, fotos, placas, cab = _cache[k]
    cols = [_c(a[3]), _c(b[3])]

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        if dt <= 0:
            return out
        u = _eo(dt / .45)
        h = int(H_ * u)
        out[H_ - h:] = base[H_ - h:] if h else out[H_ - h:]
        uc = _eo((dt - .15) / .4)
        if uc > 0:
            _sobre(out, cab, int(cx - 380 + 30), int(40 - 60 * (1 - uc)), uc)
        for lado in (0, 1):
            s = _pop(dt - .1 - .12 * lado, .5)
            if s > .02:
                fx = fw / 2 if lado == 0 else W_ - fw / 2
                fl = 5 * math.sin(dt * 1.5 + lado * 2)
                _centro(out, fotos[lado], fx, H_ - 130 - fotos[lado].shape[0] / 2 + 70 + fl + 80 * (1 - min(1, s)), min(1.0, s))
                _sobre(out, placas[lado], int(fx - fw / 2), H_ - 140, clamp(s))
        for i, f in enumerate(filas):
            tk = _mk(marcas, i, .7 + .5 * i)
            ub = _eo((dt - tk) / .55)
            if ub <= 0:
                continue
            y = y0 + 30 + i * paso
            for lado in (0, 1):
                fr = f[3 + lado] * ub
                L = int(bw * fr)
                if L > 3:
                    c = cols[lado] if f[5] in (lado, None) else (120, 128, 140)
                    if lado == 0:
                        x0_, x1_ = int(cx - 8 - L), int(cx - 8)
                    else:
                        x0_, x1_ = int(cx + 8), int(cx + 8 + L)
                    cv2.rectangle(out, (x0_, y - 3), (x1_, y + 15), c[::-1] + (255,), -1)
                    cv2.rectangle(out, (x0_, y - 3), (x1_, y + 2), (255, 255, 255, 120), -1)
                vx = cx - bw - 75 if lado == 0 else cx + bw + 75
                _sobre(out, vals[i][lado], int(vx - 100), y - 24, clamp((dt - tk) / .3))
            if f[5] in (0, 1) and dt - tk > .55:                 # el mejor de la fila late
                p = .5 + .5 * math.sin((dt - tk) * 5)
                xg = int(cx - bw - 150) if f[5] == 0 else int(cx + bw + 150)
                cv2.circle(out, (xg, y + 6), int(7 + 3 * p), cols[f[5]][::-1] + (255,), -1, cv2.LINE_AA)
        out = _brillo_barrido(out, (dt - .5) / .8)
        ang = 4 * (1 - _eo(dt / .6)) * 3 + 1.6 * math.sin(dt * 1.1)
        return _perspectiva(out, ang)

    return fn
