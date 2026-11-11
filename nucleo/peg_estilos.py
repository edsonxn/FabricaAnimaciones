# -*- coding: utf-8 -*-
"""Estilos NUEVOS de pegatina para SECUENCIA YT (el usuario, 30-oct-2026, sobre Runil: «cámbialas de tamaño, de posición y de estilo;
atrévete a diseñar nuevos tipos»). Se mezclan con la pegatina de siempre (mg_*.pegatina) para que no todas se vean iguales:
  silueta   personaje SIN FONDO a media pantalla, saliendo del borde inferior, con la cara bien visible y su nombre al lado
  reliquia  objeto sin fondo flotando sobre un círculo de runas que gira, con rayos y chispas
  banda     tira de cine a todo lo ancho con los OJOS o la cara en primer plano
  camafeo   medallón redondo con anillo de runas, para menciones rápidas
  legajo    expediente de pergamino rasgado con retrato en sepia, datos y sello
  abanico   cartas que se abren en abanico cuando la voz enumera
Todas son fn(dt, dur, marcas) -> BGRA, como los MG. Los colores salen de TEMAS: para otro juego, añade su entrada.
Primer uso: videos/tes_secretos_40/efectos.py · receta: docs/estilo_secuencia_yt.md § PEGATINAS.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

import mg_tes as T

TEMAS = {"tes": dict(luz=T.ORO, texto=T.HUESO, rojo=T.SANGRE, papel=(214, 194, 150), tinta=(58, 40, 24)),
         "wow": dict(luz=(255, 205, 90), texto=(244, 236, 220), rojo=(196, 40, 52), papel=(222, 200, 150), tinta=(58, 40, 24)),
         "er": dict(luz=(214, 186, 120), texto=(232, 226, 210), rojo=(196, 40, 52), papel=(206, 196, 168), tinta=(46, 32, 20)),
         "gaming": dict(luz=(255, 214, 64), texto=(248, 248, 248), rojo=(224, 48, 56), papel=(232, 222, 190), tinta=(40, 36, 60)),
         "spyro": dict(luz=(250, 190, 40), texto=(240, 222, 86), rojo=(226, 54, 88), papel=(206, 214, 232), tinta=(22, 34, 56)),
         "n64": dict(luz=(250, 200, 24), texto=(250, 250, 248), rojo=(226, 38, 48), papel=(214, 216, 222), tinta=(24, 26, 32)),
         "pokemon": dict(luz=(248, 208, 48), texto=(248, 248, 232), rojo=(232, 56, 48), papel=(224, 236, 200), tinta=(15, 56, 15)),
         "cod": dict(luz=(246, 190, 52), texto=(244, 244, 238), rojo=(226, 54, 46), papel=(200, 196, 178), tinta=(20, 24, 26)),
         "plasti": dict(luz=(255, 205, 0), texto=(250, 244, 228), rojo=(214, 32, 40), papel=(238, 228, 204), tinta=(40, 30, 24))}
_rec = {}


def _eo(u):
    u = min(1.0, max(0.0, u))
    return 1 - (1 - u) ** 3


def recorte(ruta, modelo="isnet-general-use"):
    """RGBA sin fondo, recortado a su caja. Guarda el resultado en <carpeta>/_rec/ para no repetir rembg."""
    if ruta in _rec:
        return _rec[ruta]
    im = Image.open(ruta).convert("RGBA")
    if im.getchannel("A").getextrema()[0] > 10:         # sin transparencia: hay que quitar el fondo
        carpeta = os.path.join(os.path.dirname(ruta), "_rec")
        cache = os.path.join(carpeta, os.path.splitext(os.path.basename(ruta))[0] + ".png")
        if os.path.exists(cache):
            im = Image.open(cache).convert("RGBA")
        else:
            from rembg import new_session, remove
            im = remove(im.convert("RGB"), session=new_session(modelo)).convert("RGBA")
            os.makedirs(carpeta, exist_ok=True)
            im.save(cache)
    a = im.getchannel("A").point(lambda v: 255 if v > 24 else 0)
    im = im.crop(a.getbbox() or (0, 0) + im.size)
    _rec[ruta] = im
    return im


def _salida_bgra(im):
    return np.array(im)[..., [2, 1, 0, 3]].copy()


def _alfa(im, k):
    if k >= .999:
        return im
    a = np.array(im)
    a[..., 3] = (a[..., 3] * k).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def _pegar(out, im, x, y):
    """alpha_composite que admite coordenadas negativas (recorta lo que se sale del lienzo)."""
    sx, sy = max(0, -x), max(0, -y)
    ex, ey = min(im.width, sx + out.width - max(0, x)), min(im.height, sy + out.height - max(0, y))
    if ex > sx and ey > sy:
        out.alpha_composite(im, (max(0, x), max(0, y)), (sx, sy, ex, ey))


def _rotulo(ancho, nombre, sub, tema, tam=86):
    """Nombre grande + separador + subtítulo sobre sombra difusa, legible encima de cualquier clip."""
    t = TEMAS[tema]
    h = tam + 90
    im = Image.new("RGBA", (ancho, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f, fs = T.fuente("Bold Condensed", tam), T.fuente("Condensed", 36)
    cabe = ancho * .90                                     # nombre largo: se encoge, nunca se sale del lienzo («BALDÍ», 2-nov)
    track, ft = 4, tam
    while T._ancho_track(d, nombre.upper(), f, track) > cabe and ft > 20:   # el track NO escala con la letra: se mide
        ft -= 2                                            # en cada paso («LAS VERDES COLINAS DE TUERCESPINA» se cortaba, 11-nov)
        track = 4 if ft > tam * .6 else 2
        f = T.fuente("Bold Condensed", ft)
    T._texto(d, (ancho / 2, tam * .62), nombre.upper(), f, t["texto"], "mm", track=track)
    T.separador(d, ancho / 2, tam * 1.22, min(ancho * .42, 190), color=t["luz"])
    if sub:
        fsz = 36
        while d.textlength(sub, font=fs) > ancho * .94 and fsz > 18:   # el subtítulo tampoco se sale (11-nov-2026)
            fsz -= 2
            fs = T.fuente("Condensed", fsz)
        T._texto(d, (ancho / 2, tam * 1.22 + 42), sub, fs, t["texto"], "mm")
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sombra.paste((0, 0, 0, 215), mask=im.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(12)))
    sombra.alpha_composite(im)
    return sombra


def silueta(ruta, nombre=None, sub=None, alto=880, encuadre=(0.0, 1.0), lado="izq", tema="tes"):
    """Personaje SIN FONDO saliendo del borde inferior. encuadre = (arriba, abajo) en fracción del recorte (para enseñar de la
    cintura para arriba). lado = dónde va el personaje; el nombre va del lado de dentro. Colócalo con pos_silueta().
    NO para fotos de PERSONAS REALES (el usuario, 10-nov-2026): rembg les deja alfa parcial y la cara se funde con el gameplay;
    para ellas un marco opaco de peg_anim (museo/polaroid/carta, tam >= 600) o una pantalla."""
    t = TEMAS[tema]
    fig = recorte(ruta)
    fig = fig.crop((0, int(fig.height * encuadre[0]), fig.width, int(fig.height * encuadre[1])))
    k = alto / fig.height
    fig = fig.resize((max(2, int(fig.width * k)), alto), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 70, 2))
    a = np.array(fig)
    a[..., 3] = (a[..., 3] * np.clip((alto - 1 - np.arange(alto))[:, None] / (alto * .09), 0, 1)).astype(np.uint8)   # base que se funde
    fig = Image.fromarray(a, "RGBA")
    M = 46
    lienzo = (fig.width + 2 * M, alto + M)
    base = Image.new("RGBA", lienzo, (0, 0, 0, 0))
    mascara = Image.new("L", lienzo, 0)
    mascara.paste(fig.getchannel("A"), (M, M))
    halo = mascara.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(16))
    base.paste((0, 0, 0, 255), mask=mascara.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * .62)))
    base.paste(t["luz"] + (255,), mask=halo.point(lambda v: int(v * .42)))
    base.alpha_composite(fig, (M, M))
    rot = _rotulo(560, nombre, sub, tema) if nombre else None
    W, H = base.width + (500 if rot else 0), base.height
    xfig = 0 if lado == "izq" else W - base.width
    xrot = base.width - 90 if lado == "izq" else 30
    if W > 1920:   # figura muy ancha (cara de cerca): el lienzo se sale de pantalla; el rótulo se queda dentro (2-nov, Graves)
        xrot = min(xrot, 1920 - 600) if lado == "izq" else W - 1920 + 40
    dentro = 1 if lado == "izq" else -1

    def fn(dt, dur, marcas):
        s = _eo(dt / .55)
        if s <= .01:
            return np.zeros((2, 2, 4), np.uint8)
        z = 1 + .04 * min(1.0, dt / max(1.0, dur))           # acercamiento lento desde la base
        im = base.resize((int(base.width * z), int(base.height * z)), Image.BILINEAR)
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        _pegar(out, _alfa(im, s), xfig - (im.width - base.width) // 2 - int((1 - s) * 150 * dentro), H - im.height)
        if rot:
            r = _eo((dt - .3) / .4)
            if r > .01:
                out.alpha_composite(_alfa(rot, r), (xrot + int((1 - r) * 40 * -dentro), int(H * .50)))
        return _salida_bgra(out)
    fn.tam = (W, H)
    return fn


def pos_silueta(fn, lado="izq"):
    """(x, y) en fracción de pantalla para que la silueta quede pegada al borde inferior y al lateral."""
    W, H = fn.tam
    return (W / 2 / 1920 if lado == "izq" else 1 - W / 2 / 1920), 1 - H / 2 / 1080


def _anillo(C, r, tema, n=26, semilla=7):
    """Círculo de runas (trazos tipo escritura de dragón) sobre lienzo C×C."""
    t = TEMAS[tema]
    rnd = random.Random(semilla)
    im = Image.new("RGBA", (C * 2, C * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, R = C, r * 2
    col = t["luz"] + (235,)
    for rad, ancho in ((R, 5), (R - 66, 3), (R + 14, 2)):
        d.ellipse((c - rad, c - rad, c + rad, c + rad), outline=col, width=ancho)
    for i in range(n):
        ang = 2 * math.pi * i / n
        rm = R - 33
        px, py = c + rm * math.cos(ang), c + rm * math.sin(ang)
        for _ in range(rnd.randint(2, 3)):                  # garras: trazos cortos en cuña
            a2 = ang + rnd.uniform(-1.2, 1.2) + math.pi / 2
            lg = rnd.uniform(12, 22)
            dx, dy = rnd.uniform(-9, 9), rnd.uniform(-9, 9)
            d.line((px + dx, py + dy, px + dx + lg * math.cos(a2), py + dy + lg * math.sin(a2)), fill=col, width=4)
    return im.resize((C, C), Image.LANCZOS)


def recorte_fallido(im):
    """True si rembg se comió el objeto: pasa con los ICONOS de objeto (ilustración cuadrada a sangre, sin fondo que quitar).
    Con menos del 17 % de píxeles opacos en su caja el medallón sale vacío (wow_objetos_secretos_forever, 2-nov-2026)."""
    a = np.array(im.getchannel("A"))
    return (a > 200).mean() < .17


def _icono(ruta, lado, tema):
    """El icono ENTERO con esquinas redondeadas, bisel oscuro y filo de luz del tema (marco de icono de MMO)."""
    t = TEMAS[tema]
    im = Image.open(ruta).convert("RGB")
    q = min(im.size)
    y0 = int((im.height - q) * .06) if im.height > im.width * 1.12 else (im.height - q) // 2   # alta: la cara (11-nov-2026)
    im = im.crop(((im.width - q) // 2, y0, (im.width - q) // 2 + q, y0 + q))
    m, b = int(lado * .07), max(4, int(lado * .035))
    dentro = lado - 2 * b
    foto = im.resize((dentro, dentro), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2)).convert("RGBA")
    sombra = np.zeros((dentro, dentro, 4), np.uint8)       # viñeta interior: hunde el icono en el marco
    yy, xx = np.mgrid[0:dentro, 0:dentro]
    borde = np.minimum.reduce([xx, yy, dentro - 1 - xx, dentro - 1 - yy]) / (dentro * .14)
    sombra[..., 3] = (np.clip(1 - borde, 0, 1) ** 1.6 * 150).astype(np.uint8)
    foto.alpha_composite(Image.fromarray(sombra, "RGBA"))
    mascara = Image.new("L", (dentro, dentro), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, dentro - 1, dentro - 1), m, fill=255)
    out = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((0, 0, lado - 1, lado - 1), m + b, fill=(10, 8, 6, 255))
    d.rounded_rectangle((1, 1, lado - 2, lado - 2), m + b, outline=t["luz"] + (255,), width=max(2, b // 2))
    out.paste(foto, (b, b), mascara)
    return out


def reliquia(ruta, nombre=None, sub=None, tam=620, tema="tes"):
    """Objeto sin fondo que flota sobre un círculo de runas que gira, con rayos y chispas.
    Si el recorte falla (iconos de objeto), flota el icono entero en su marco: nunca un medallón vacío."""
    t = TEMAS[tema]
    obj = recorte(ruta)
    if recorte_fallido(obj):
        obj = _icono(ruta, int(tam * .60), tema)           # cabe entero dentro del anillo (diagonal < diámetro)
    else:
        lado = int(tam * .70)
        k = lado / max(obj.size)
        obj = obj.resize((max(2, int(obj.width * k)), max(2, int(obj.height * k))), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    C = tam + 90
    anillo = _anillo(C, tam * .46, tema)
    glow = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    yy, xx = np.mgrid[0:C, 0:C]
    dist = np.hypot(xx - C / 2, yy - C / 2) / (C / 2)
    g = np.zeros((C, C, 4), np.uint8)
    g[..., :3] = t["luz"]
    g[..., 3] = (np.clip(1 - dist / .92, 0, 1) ** 1.7 * 170).astype(np.uint8)
    n = np.zeros((C, C, 4), np.uint8)
    n[..., 3] = (np.clip(1 - dist / .98, 0, 1) ** .9 * 165).astype(np.uint8)
    fondo = Image.fromarray(n, "RGBA")
    fondo.alpha_composite(Image.fromarray(g, "RGBA"))
    rayos = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    dr = ImageDraw.Draw(rayos)
    for i in range(12):
        a, ab = 2 * math.pi * i / 12, .05
        dr.polygon([(C / 2, C / 2), (C / 2 + C * math.cos(a - ab), C / 2 + C * math.sin(a - ab)),
                    (C / 2 + C * math.cos(a + ab), C / 2 + C * math.sin(a + ab))], fill=t["luz"] + (34,))
    rayos = rayos.filter(ImageFilter.GaussianBlur(8))
    alto = C + (120 if nombre else 0)
    rot = _rotulo(C, nombre, sub, tema, tam=66) if nombre else None
    rnd = random.Random(3)
    chispas = [(rnd.uniform(0, 6.28), rnd.uniform(.28, .46), rnd.uniform(.4, 1.1), rnd.uniform(2, 5)) for _ in range(22)]

    def fn(dt, dur, marcas):
        s = T._pop(dt, .5)
        if s <= .02:
            return np.zeros((2, 2, 4), np.uint8)
        out = Image.new("RGBA", (C, alto), (0, 0, 0, 0))
        capa = fondo.copy()
        capa.alpha_composite(rayos.rotate(-dt * 9, resample=Image.BILINEAR))
        capa.alpha_composite(anillo.rotate(dt * 16, resample=Image.BILINEAR))
        o = obj.rotate(5 * math.sin(dt * 1.15), resample=Image.BICUBIC, expand=True)
        y = C / 2 + 12 * math.sin(dt * 1.7)
        capa.alpha_composite(o, (int(C / 2 - o.width / 2), int(y - o.height / 2)))
        d = ImageDraw.Draw(capa)
        for a0, rr, v, tm in chispas:
            a = a0 + dt * v
            x, yc = C / 2 + rr * C * math.cos(a), C / 2 + rr * C * math.sin(a) * .92
            d.ellipse((x - tm, yc - tm, x + tm, yc + tm), fill=T.BLANCO + (int(150 + 100 * math.sin(dt * 5 + a0)),))
        if abs(s - 1) > .004:
            ns = max(2, int(C * s))
            capa2 = capa.resize((ns, ns), Image.BILINEAR)
            out.alpha_composite(capa2, ((C - ns) // 2, (C - ns) // 2) if ns <= C else (0, 0), (0, 0) if ns <= C else ((ns - C) // 2, (ns - C) // 2))
        else:
            out.alpha_composite(capa)
        if rot:
            r = _eo((dt - .35) / .4)
            if r > .01:
                out.alpha_composite(_alfa(rot, r), (0, C - 66))
        return _salida_bgra(out)
    return fn


def _encuadre(im, foco, w, h):
    """Recorte de `im` centrado en foco = (cx, cy, zoom) con la proporción w:h."""
    cx, cy, z = foco
    cw = im.width / z
    ch = cw * h / w
    if ch > im.height:
        ch, cw = im.height, im.height * w / h
    x0 = min(max(0, cx * im.width - cw / 2), im.width - cw)
    y0 = min(max(0, cy * im.height - ch / 2), im.height - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))


def banda(ruta, nombre=None, sub=None, foco=(.5, .25, 2.0), alto=340, lado="der", tema="tes"):
    """Tira de cine a todo lo ancho con el rostro en primer plano; se abre desde su eje y se desliza despacio."""
    t = TEMAS[tema]
    W = 1920
    base = _encuadre(Image.open(ruta).convert("RGB"), foco, W + 120, alto)
    base = base.resize((W + 120, alto), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    tira = base.convert("RGBA")
    if nombre:
        g = np.zeros((alto, W + 120, 4), np.uint8)
        x = np.linspace(0, 1, W + 120)
        g[..., 3] = (np.clip((x - .48) / .22 if lado == "der" else (.52 - x) / .22, 0, 1) * 230).astype(np.uint8)[None, :]
        tira.alpha_composite(Image.fromarray(g, "RGBA"))
    rot = _rotulo(640, nombre, sub, tema, tam=84) if nombre else None

    def fn(dt, dur, marcas):
        s = _eo(dt / .4)
        if s <= .02:
            return np.zeros((2, 2, 4), np.uint8)
        dx = int(120 * min(1.0, dt / max(1.0, dur)))
        im = tira.crop((dx, 0, dx + W, alto)).copy()
        if rot:
            r = _eo((dt - .3) / .4)
            if r > .01:
                im.alpha_composite(_alfa(rot, r), (1220 if lado == "der" else 60, (alto - rot.height) // 2))
        hv = max(2, int(alto * s))
        out = Image.new("RGBA", (W, alto + 12), (0, 0, 0, 0))
        y0 = (alto + 12 - hv) // 2
        out.paste(im.crop((0, (alto - hv) // 2, W, (alto - hv) // 2 + hv)), (0, y0))
        d = ImageDraw.Draw(out)
        for y in (y0 - 3, y0 + hv):
            d.rectangle((0, max(0, y), W, max(0, y) + 3), fill=t["luz"] + (255,))
        return _salida_bgra(out)
    return fn


def camafeo(ruta, nombre=None, tam=300, foco=(.5, .2, 2.0), tema="tes"):
    """Medallón redondo con anillo de runas que gira despacio; entra girando. Para menciones rápidas."""
    t = TEMAS[tema]
    C = tam + 70
    im = Image.open(ruta).convert("RGB")
    zmax = max(1.0, min(im.size) * 1.25 / tam)             # el zoom nunca amplía el recorte más de 1,25x (icono borroso, 2-nov)
    foco = (foco[0], foco[1], min(foco[2], zmax))
    foto = _encuadre(im, foco, 1, 1).resize((tam, tam), Image.LANCZOS)
    m = Image.new("L", (tam * 2, tam * 2), 0)
    ImageDraw.Draw(m).ellipse((0, 0, tam * 2 - 1, tam * 2 - 1), fill=255)
    cara = foto.convert("RGBA")
    cara.putalpha(m.resize((tam, tam), Image.LANCZOS))
    anillo = _anillo(C, tam * .50 + 22, tema, n=20, semilla=11)
    plano = Image.new("RGBA", (C, C), (0, 0, 0, 0))
    ImageDraw.Draw(plano).ellipse((C / 2 - tam / 2 - 34, C / 2 - tam / 2 - 34, C / 2 + tam / 2 + 34, C / 2 + tam / 2 + 34), fill=(8, 7, 6, 225))
    rot = None
    alto = C
    if nombre:
        rot = _rotulo(C + 80, nombre, None, tema, tam=46)
        alto = C + 58

    def fn(dt, dur, marcas):
        s = T._pop(dt, .45)
        if s <= .02:
            return np.zeros((2, 2, 4), np.uint8)
        out = Image.new("RGBA", (C + 80, alto), (0, 0, 0, 0))
        capa = plano.copy()
        capa.alpha_composite(anillo.rotate(dt * 22, resample=Image.BILINEAR))
        capa.alpha_composite(cara, ((C - tam) // 2, (C - tam) // 2))
        if abs(s - 1) > .004 or dt < .5:
            capa = capa.rotate(-200 * (1 - _eo(dt / .5)), resample=Image.BILINEAR)
            ns = max(2, min(C, int(C * s)))
            capa = capa.resize((ns, ns), Image.BILINEAR)
        out.alpha_composite(capa, (40 + (C - capa.width) // 2, (C - capa.height) // 2))
        if rot:
            r = _eo((dt - .3) / .3)
            if r > .01:
                out.alpha_composite(_alfa(rot, r), (0, C - 34))
        return _salida_bgra(out)
    return fn


def _papel(w, h, tema, semilla=5):
    """Hoja de pergamino con manchas y borde rasgado."""
    t = TEMAS[tema]
    rng = np.random.default_rng(semilla)
    ruido = Image.fromarray((rng.random((h // 8 + 2, w // 8 + 2)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    n = (np.array(ruido, np.float32) / 255 - .5)[..., None]
    a = np.clip(np.array(t["papel"], np.float32) * (1 + n * .22), 0, 255)
    borde = np.minimum.reduce([np.arange(w)[None, :].repeat(h, 0), (w - 1 - np.arange(w))[None, :].repeat(h, 0),
                               np.arange(h)[:, None].repeat(w, 1), (h - 1 - np.arange(h))[:, None].repeat(w, 1)]).astype(np.float32)
    a *= np.clip(.62 + borde / 70, 0, 1)[..., None]
    fino = Image.fromarray((rng.random((h // 3 + 2, w // 3 + 2)) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)
    alfa = np.clip((borde - 3 - np.array(fino, np.float32) / 255 * 15) * 2.4, 0, 1) * 255
    return Image.fromarray(np.dstack([a, alfa]).astype(np.uint8), "RGBA")


def legajo(ruta, titulo, lineas, sello=None, ancho=560, giro=3.5, tema="tes"):
    """Expediente de pergamino: retrato en sepia, título y datos a mano; `sello` (texto, i_marca) se estampa con la voz."""
    t = TEMAS[tema]
    RH = int(ancho * .78)
    tmp = ImageDraw.Draw(Image.new("RGBA", (9, 9)))
    fl = T.fuente("SemiBold Condensed", 34)
    filas = [x for ln in lineas for x in T._partir(tmp, ln, fl, ancho - 96)]
    h = 40 + RH + 92 + len(filas) * 44 + 34
    hoja = _papel(ancho, h, tema)
    d = ImageDraw.Draw(hoja)
    foto = ImageOps.colorize(ImageOps.autocontrast(_encuadre(Image.open(ruta).convert("L"), (.5, .3, 1.15), ancho - 90, RH)), (34, 22, 12), (232, 210, 170))
    foto = foto.resize((ancho - 90, RH), Image.LANCZOS)
    hoja.paste(foto, (45, 40))
    d.rectangle((45, 40, ancho - 45, 40 + RH), outline=t["tinta"] + (255,), width=3)
    T._texto(d, (ancho / 2, 40 + RH + 48), titulo.upper(), T.fuente("Bold Condensed", 54), t["tinta"], "mm", track=3)
    y = 40 + RH + 92
    for fl_ in filas:
        T._texto(d, (ancho / 2, y + 20), fl_, fl, t["tinta"], "mm")
        y += 44
    M = 50
    C = (ancho + 2 * M, h + 2 * M)

    def fn(dt, dur, marcas):
        s = _eo(dt / .45)
        if s <= .01:
            return np.zeros((2, 2, 4), np.uint8)
        mk = list(marcas) + [99] * 3
        im = hoja.copy()
        if sello and dt >= mk[sello[1]]:
            u = T._pop(dt - mk[sello[1]], .3)
            T._sello(im, ancho * .66, 40 + RH * .80, sello[0], u)
        out = Image.new("RGBA", C, (0, 0, 0, 0))
        sombra = Image.new("RGBA", C, (0, 0, 0, 0))
        sombra.paste((0, 0, 0, 150), (M + 8, M + 12), im.getchannel("A"))
        out.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(10)))
        out.alpha_composite(im, (M, M))
        out = out.rotate(giro * s + (1 - s) * 16 + .6 * math.sin(dt * 1.3), resample=Image.BICUBIC)
        return _salida_bgra(_alfa(out, s))
    return fn


def abanico(fotos, tam=320, apertura=13, tema="tes"):
    """Cartas que salen de abajo y se abren en abanico, una por marca (o escalonadas sin marcas). fotos = [(ruta, etiqueta)]."""
    t = TEMAS[tema]
    n = len(fotos)
    cartas = []
    for ruta, etiqueta in fotos:
        H = int(tam * 1.32)
        c = Image.new("RGBA", (tam, H), t["papel"] + (255,))
        im = Image.open(ruta).convert("RGBA")
        fondo = Image.new("RGBA", im.size, (20, 18, 16, 255))
        fondo.alpha_composite(im)
        c.paste(ImageOps.fit(fondo.convert("RGB"), (tam - 24, H - 74), Image.LANCZOS, centering=(.5, .3)), (12, 12))
        d = ImageDraw.Draw(c)
        d.rectangle((0, 0, tam - 1, H - 1), outline=t["tinta"] + (255,), width=3)
        T._texto(d, (tam / 2, H - 32), etiqueta.upper(), T.fuente("Bold Condensed", 32), t["tinta"], "mm", track=1)
        cartas.append(c)
    W = int(tam * (1 + .86 * (n - 1)) + 220)
    Hc = int(tam * 1.32 + 190)

    def fn(dt, dur, marcas):
        out = Image.new("RGBA", (W, Hc), (0, 0, 0, 0))
        mk = list(marcas) + [.28 * k for k in range(len(marcas), n)]
        for k, c in enumerate(cartas):
            s = _eo((dt - mk[k]) / .4)
            if s <= .01:
                continue
            ang = -(k - (n - 1) / 2) * apertura * s + 1.2 * math.sin(dt * 1.4 + k)
            r = c.rotate(ang, resample=Image.BICUBIC, expand=True)
            x = W / 2 + (k - (n - 1) / 2) * tam * .84 * s - r.width / 2
            y = 70 + abs(k - (n - 1) / 2) * 26 + (1 - s) * 420
            sombra = Image.new("RGBA", (W, Hc), (0, 0, 0, 0))
            sombra.paste((0, 0, 0, 120), (int(x) + 7, int(y) + 10), r.getchannel("A"))
            out.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(7)))
            out.alpha_composite(r, (max(0, int(x)), max(0, int(y))))
        return _salida_bgra(out)
    return fn
