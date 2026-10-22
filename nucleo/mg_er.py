# -*- coding: utf-8 -*-
"""MOTION GRAPHICS «interfaz de Elden Ring» por código (Runa Caída; primer uso `er_radagon_atrocidades`, 14-oct-2026).
Hermano de nucleo/mg_tes.py (Skyrim) y mg_wow.py con la estética de los menús de Elden Ring: Garamond (la serif del juego
es una garalda; en Windows la más parecida es GARA.TTF), dorado viejo para los títulos, pergamino para el texto, paneles
casi negros con filete dorado fino y el rótulo grande con banda negra difusa de «ENEMIGO ABATIDO». CERO cifras ni citas
inventadas: solo lo que el guion ya dice.

Uso desde videos/<v>/efectos.py (FX `mg` de nucleo/secuencia_fx.py; acepta de/a o en/dur):
    import mg_er as E
  puesto(arriba, titulo)                         banda negra a lo ancho + título dorado que entra cerrando el espaciado
  descripcion(nombre, texto, tipo=None, icono=None)   ficha de descripción de objeto; *entre asteriscos* = dorado
  mensaje(lineas)                                mensaje del suelo (texto ámbar que brilla); una línea por marca
  doble_vida()                                   esquema de matrimonios: Márika-Godfrey / Radagon-Rennala -> exilio -> fusión
  gemelos()                                      un solo dios que se parte en dos hijos con su maldición
  hilos(centro, nombres, titulo)                 el encanto: un centro dorado con seguidores atados por hilos; la última marca
                                                 corta los hilos y los seguidores se enfrentan (rojo)   (er_miquella_atrocidades)
  cosido(alma, cuerpo, resultado)                alma de uno + cuerpo de otro -> un solo ser «cosido»
  cruces(etiquetas, total=13)                    fila de cruces que se encienden una por marca con lo que se abandona
  triada(filas, titulo)                          columnas que entran por marca; la última resalta en ámbar
  marionetas(titiritero, munecos, dueno)         cruceta con muñecos colgando; la última marca le da la vuelta: el titiritero
                                                 cuelga de los hilos de `dueno` (er_ranni_atrocidades, 21-oct-2026)
  sombra(ama, sombra, amos)                      los Dos Dedos atan a la Empírea y a su sombra; ella corta su hilo y la
                                                 sombra enloquece en rojo
  domino(fichas)                                 fila de fichas que caen una sobre otra (causa -> efecto); la última en rojo
  constelacion(nombres, centro, tu, remate)      estrellas unidas a la Luna que se apagan una por marca; quedan la Luna y «Tú»
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ORO, ORO_OSC, PERGAMINO, GRIS, AMBAR, ROJO = (214, 182, 110), (140, 112, 60), (226, 216, 190), (150, 142, 126), (255, 186, 92), (176, 52, 40)
_fc = {}


def fuente(estilo, tam):
    """estilo: «r» (GARA), «b» (GARABD), «i» (GARAIT)."""
    k = (estilo, tam)
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"r": "C:/Windows/Fonts/GARA.TTF", "b": "C:/Windows/Fonts/GARABD.TTF",
                                     "i": "C:/Windows/Fonts/GARAIT.TTF"}[estilo], tam)
    return _fc[k]


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _ancho(d, s, f, track):
    return sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)


def _texto(d, xy, s, f, color, ancla="la", alfa=255, track=0, sombra=True):
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if not track:
        if sombra:
            d.text((xy[0] + 2, xy[1] + 2), s, font=f, fill=(0, 0, 0, int(a * .85)), anchor=ancla)
        d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla)
        return
    w = _ancho(d, s, f, track)
    x = xy[0] - (w / 2 if ancla[0] == "m" else w if ancla[0] == "r" else 0)
    for c in s:
        if sombra:
            d.text((x + 2, xy[1] + 2), c, font=f, fill=(0, 0, 0, int(a * .85)), anchor="l" + ancla[1])
        d.text((x, xy[1]), c, font=f, fill=tuple(color) + (a,), anchor="l" + ancla[1])
        x += d.textlength(c, font=f) + track


def _brillo(im, radio=10, fuerza=1.0):
    """Halo: copia desenfocada del propio texto debajo (el dorado del juego brilla un poco)."""
    g = im.filter(ImageFilter.GaussianBlur(radio))
    a = np.array(g)
    a[..., 3] = np.clip(a[..., 3].astype(np.float32) * fuerza, 0, 255).astype(np.uint8)
    out = Image.fromarray(a)
    out.alpha_composite(im)
    return out


def _filete(d, cx, y, medio, color=ORO, alfa=255):
    """Línea dorada fina que se desvanece hacia los extremos."""
    for i in range(50):
        u0, u1 = i / 50, (i + 1) / 50
        k = (1 - u0) ** 1.2
        for s in (-1, 1):
            d.line([(cx + s * u0 * medio, y), (cx + s * u1 * medio, y)], fill=color + (int(220 * k * alfa / 255),), width=2)


def _bgra(im, alfa=1.0):
    a = np.array(im)
    if alfa < 1:
        a[..., 3] = (a[..., 3] * max(0.0, alfa)).astype(np.uint8)
    return a[..., [2, 1, 0, 3]].copy()


def _partir(d, s, f, ancho):
    lineas, cur = [], ""
    for w in s.split():
        prueba = (cur + " " + w).strip()
        if d.textlength(prueba.replace("*", ""), font=f) <= ancho or not cur:
            cur = prueba
        else:
            lineas.append(cur)
            cur = w
    return lineas + [cur] if cur else lineas


# ------------------------------------------------------------------ rótulo de puesto («ENEMIGO ABATIDO»)
def puesto(arriba, titulo, ancho=1920, color=ORO):
    """Banda negra difusa a lo ancho; `arriba` chico en pergamino y `titulo` grande dorado con halo, que entra cerrando el
    espaciado (como el aviso de jefe derrotado). Sale fundiéndose."""
    h = 250
    f1, f2 = fuente("r", 40), fuente("r", 92)

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, h), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rectangle((ancho * .06, 52, ancho * .94, h - 52), fill=190)
        banda = Image.new("RGBA", im.size, (4, 3, 2, 255))
        banda.putalpha(m.filter(ImageFilter.GaussianBlur(34)))
        im.alpha_composite(banda)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        a = 255 * _eo(dt / .6)
        _texto(d, (ancho / 2, 72), arriba.upper(), f1, PERGAMINO, "mm", a * .9, track=8)
        tr = 6 + 30 * (1 - _eo(dt / 1.1))
        _texto(d, (ancho / 2, 152), titulo.upper(), f2, color, "mm", a, track=tr, sombra=False)
        im.alpha_composite(_brillo(txt, 9, 1.3))
        return _bgra(im, min(1.0, (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ ficha de descripción de objeto
def descripcion(nombre, texto, tipo=None, icono=None, ancho=900):
    """Panel del inventario: icono opcional a la izquierda (ruta de imagen), nombre en pergamino, `tipo` gris en cursiva,
    filete dorado y el texto de la descripción, que aparece línea a línea. *Entre asteriscos* sale en dorado."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fn_, ft, fd = fuente("r", 56), fuente("i", 34), fuente("r", 42)
    ic = None
    if icono:
        ic = Image.open(icono).convert("RGBA")
        ic.thumbnail((150, 150), Image.LANCZOS)
    x_txt = 40 + (175 if ic else 0)
    lineas = _partir(tmp, texto, fd, ancho - 80)
    nombres = _partir(tmp, nombre, fn_, ancho - x_txt - 40)
    alto_cab = max(30 + 60 * len(nombres) + (40 if tipo else 0), 190 if ic else 0)
    h = alto_cab + 40 + len(lineas) * 52 + 36
    M = 40

    def base():
        im = Image.new("RGBA", (ancho + 2 * M, h + 2 * M), (0, 0, 0, 0))
        sh = Image.new("L", im.size, 0)
        ImageDraw.Draw(sh).rectangle((M - 6, M - 6, M + ancho + 6, M + h + 6), fill=200)
        sombra = Image.new("RGBA", im.size, (0, 0, 0, 255))
        sombra.putalpha(sh.filter(ImageFilter.GaussianBlur(22)))
        im.alpha_composite(sombra)
        d = ImageDraw.Draw(im)
        d.rectangle((M, M, M + ancho, M + h), fill=(14, 12, 9, 228))
        d.rectangle((M, M, M + ancho, M + h), outline=ORO_OSC + (255,), width=2)
        d.rectangle((M + 7, M + 7, M + ancho - 7, M + h - 7), outline=ORO_OSC + (110,), width=1)
        for cx, cy in ((M, M), (M + ancho, M), (M, M + h), (M + ancho, M + h)):     # rombos en las esquinas
            d.polygon([(cx - 8, cy), (cx, cy - 8), (cx + 8, cy), (cx, cy + 8)], fill=(14, 12, 9, 255), outline=ORO + (255,))
        if ic:
            x0, y0 = M + 34, M + 26
            d.rectangle((x0 - 4, y0 - 4, x0 + 154, y0 + 154), fill=(28, 24, 18, 255), outline=ORO_OSC + (200,))
            im.alpha_composite(ic, (x0 + (150 - ic.width) // 2, y0 + (150 - ic.height) // 2))
        y = M + 30
        for k, ln in enumerate(nombres):
            _texto(d, (M + x_txt, y + 28 + 60 * k), ln, fn_, PERGAMINO, "lm")
        y += 60 * len(nombres)
        if tipo:
            _texto(d, (M + x_txt, y + 18), tipo, ft, GRIS, "lm")
        y = M + alto_cab + 12
        _filete(d, M + ancho / 2, y, ancho * .46)
        return im, y + 28

    cache = {}

    def fn(dt, dur, marcas):
        if "b" not in cache:
            cache["b"] = base()
        im0, y0 = cache["b"]
        im = im0.copy()
        d = ImageDraw.Draw(im)
        y = y0
        dorado = False                                  # el dorado sigue de una línea a la siguiente
        for k, ln in enumerate(lineas):                 # línea a línea, cada 0,35 s
            a = 255 * _eo((dt - .25 - k * .35) / .4)
            x = M + 40
            trozos = ln.split("*")
            for j, trozo in enumerate(trozos):
                if j:
                    dorado = not dorado
                if trozo:
                    _texto(d, (x, y + 22), trozo, fd, ORO if dorado else PERGAMINO, "lm", a)
                    x += d.textlength(trozo, font=fd)
            y += 52
        u = _eo(dt / .35)
        if u < 1:
            im = im.resize((im.width, max(2, int(im.height * (.6 + .4 * u)))), Image.BILINEAR)
        return _bgra(im, min(u, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ mensaje del suelo
def mensaje(lineas, ancho=1500):
    """Mensaje grabado en el suelo: letras ámbar con halo fuerte que aparecen de izquierda a derecha.
    La línea k entra en la marca k (si faltan marcas, cada 1,6 s); las anteriores se atenúan."""
    f = fuente("r", 84)
    h = 140 + 120 * len(lineas)

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, h), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).ellipse((ancho * .08, 30, ancho * .92, h - 30), fill=170)
        fondo = Image.new("RGBA", im.size, (3, 2, 1, 255))
        fondo.putalpha(m.filter(ImageFilter.GaussianBlur(40)))
        im.alpha_composite(fondo)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        for k, s in enumerate(lineas):
            t0 = marcas[k] if k < len(marcas) else k * 1.6
            u = (dt - t0) / max(.5, .05 * len(s))
            if u <= 0:
                continue
            n = int(len(s) * min(1.0, u)) + (1 if u < 1 else 0)
            siguiente_ = marcas[k + 1] if k + 1 < len(marcas) else (k + 1) * 1.6 if k + 1 < len(lineas) else 1e9
            a = 255 if dt < siguiente_ else 150
            w = d.textlength(s, font=f)
            y = 70 + 120 * k + 60
            d.text((ancho / 2 - w / 2, y), s[:n], font=f, fill=AMBAR + (a,), anchor="lm")
        im.alpha_composite(_brillo(txt, 14, 2.2))
        return _bgra(im, min(_eo(dt / .4), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ esquemas
def _nodo(d, cx, cy, nombre, sub, color, a, fn_, fs, abajo=False):
    """Nodo con nombre encima (o debajo con `abajo`, cuando la línea llega desde arriba) y subtítulo gris debajo."""
    if a <= 0:
        return
    d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(14, 12, 9, int(a)), outline=color + (int(a),), width=3)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=color + (int(a),))
    if abajo:
        _texto(d, (cx, cy + 24), nombre, fn_, color, "mt", a)
    else:
        _texto(d, (cx, cy - 34), nombre, fn_, color, "mb", a)
    if sub:
        _texto(d, (cx, cy + (90 if abajo else 30)), sub, fs, GRIS, "mt", a)


def _linea(d, p0, p1, u, color, a, ancho=3):
    if u <= 0 or a <= 0:
        return
    x = p0[0] + (p1[0] - p0[0]) * min(1, u)
    y = p0[1] + (p1[1] - p0[1]) * min(1, u)
    d.line([p0, (x, y)], fill=color + (int(a),), width=ancho)


def _panel(w, h):
    M = 50
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((M, M, M + w, M + h), 30, fill=215)
    fondo = Image.new("RGBA", im.size, (8, 7, 5, 255))
    fondo.putalpha(m.filter(ImageFilter.GaussianBlur(24)))
    im.alpha_composite(fondo)
    return im, M


def doble_vida(titulo="Dos matrimonios a la vez", w=1500, h=620):
    """marca 0: Márika = Godfrey (arriba) · marca 1: Radagon = Rennala (abajo) · marca 2: Godfrey se apaga («exiliado») y
    Radagon sube a casarse con Márika · marca 3: Radagon se funde con Márika y queda «RADAGON ES MÁRIKA»."""
    fn_, fs, ftit = fuente("r", 50), fuente("i", 36), fuente("r", 40)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", 255 * _eo(dt / .4), track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=255 * _eo(dt / .4))
        yA, yB = M + 210, M + 490
        xM, xG, xR, xN = M + w * .32, M + w * .68, M + w * .32, M + w * .68
        uA, uB, uC, uD = (_eo((dt - mk[i]) / .6) for i in range(4))
        # arriba: Márika - Godfrey
        _nodo(d, xM, yA, "Márika", "reina", ORO, 255 * uA, fn_, fs)
        aG = 255 * uA * (1 - .7 * uC)
        _nodo(d, xG, yA, "Godfrey", "exiliado" if uC > .5 else "primer Señor del Círculo", ORO if uC < .5 else GRIS, aG, fn_, fs)
        _linea(d, (xM + 16, yA), (xG - 16, yA), uA, ORO, 255 * (1 - uC))
        if uC > 0:                                          # la línea rota del exilio
            d.line([(xM + 16, yA), ((xM + xG) / 2 - 20, yA)], fill=GRIS + (int(200 * uC),), width=2)
            d.line([((xM + xG) / 2 + 20, yA), (xG - 16, yA)], fill=GRIS + (int(200 * uC),), width=2)
        # abajo: Radagon - Rennala; en la marca 2 Radagon sube junto a Márika
        sube = uC
        xr = xR + (xM - 270 - xR) * sube
        yr = yB + (yA - yB) * sube
        fusion = uD
        xr = xr + (xM - xr) * fusion
        _nodo(d, xN, yB, "Rennala", "abandonada" if uC > .5 else "reina de Caria", PERGAMINO if uC < .5 else GRIS,
              255 * uB * (1 - .5 * uC), fn_, fs)
        _linea(d, (xr + 16, yr), (xN - 16, yB), uB, PERGAMINO, 255 * uB * (1 - uC))
        if fusion < .98:
            _nodo(d, xr, yr, "Radagon", "rey consorte" if uC > .5 else "", ROJO if uC < .5 else ORO, 255 * uB * (1 - fusion), fn_, fs)
        if uC > 0 and fusion < .9:
            _linea(d, (xr + 16, yr), (xM - 16, yA), 1, ORO, 255 * uC * (1 - fusion), 2)
        if fusion > 0:
            txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dt_ = ImageDraw.Draw(txt)
            _texto(dt_, (M + w / 2, M + 350), "RADAGON ES MÁRIKA", fuente("r", 70), AMBAR, "mm", 255 * fusion, track=6, sombra=False)
            im.alpha_composite(_brillo(txt, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def gemelos(w=1300, h=620):
    """marca 0: «Un solo dios» · marca 1: se parte en dos ramas · marca 2: Miquella «infancia eterna» · marca 3: Malenia
    «putrefacción» (la rama de Malenia se tiñe de rojo)."""
    fn_, fs, ftit = fuente("r", 54), fuente("i", 38), fuente("r", 44)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        u0, u1, u2, u3 = (_eo((dt - mk[i]) / .6) for i in range(4))
        cx, ytop = M + w / 2, M + 130
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        _texto(ImageDraw.Draw(txt), (cx, ytop - 20), "UN SOLO DIOS", ftit, ORO, "mm", 255 * u0, track=8, sombra=False)
        im.alpha_composite(_brillo(txt, 10, 1.5))
        d = ImageDraw.Draw(im)
        d.ellipse((cx - 13, ytop + 30, cx + 13, ytop + 56), fill=(14, 12, 9, int(255 * u0)), outline=ORO + (int(255 * u0),), width=3)
        yb = M + 380
        xa, xb = M + w * .27, M + w * .73
        _linea(d, (cx, ytop + 58), (cx, ytop + 140), u1, ORO, 255 * u1)
        _linea(d, (cx, ytop + 140), (xa, ytop + 140), u1, ORO, 255 * u1)
        _linea(d, (cx, ytop + 140), (xb, ytop + 140), u1, ROJO if u3 > .5 else ORO, 255 * u1)
        _linea(d, (xa, ytop + 140), (xa, yb - 14), u1, ORO, 255 * u1)
        _linea(d, (xb, ytop + 140), (xb, yb - 14), u1, ROJO if u3 > .5 else ORO, 255 * u1)
        _nodo(d, xa, yb, "Miquella", None, PERGAMINO, 255 * u1, fn_, fs, abajo=True)
        _nodo(d, xb, yb, "Malenia", None, PERGAMINO, 255 * u1, fn_, fs, abajo=True)
        if u2 > 0:
            _texto(d, (xa, yb + 96), "infancia eterna", fs, GRIS, "mt", 255 * u2)
        if u3 > 0:
            _texto(d, (xb, yb + 96), "putrefacción", fs, ROJO, "mt", 255 * u3)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_miquella_atrocidades (19-oct-2026)
def _cruz(d, cx, cy, s, color, a, ancho=4):
    """La cruz de Miquella simplificada: palo largo, travesaño y el arco de la izquierda."""
    if a <= 0:
        return
    c = color + (int(a),)
    d.line([(cx, cy - s), (cx, cy + s * 1.5)], fill=c, width=ancho)
    d.line([(cx - s * .45, cy - s * .35), (cx + s * .45, cy - s * .35)], fill=c, width=ancho)
    d.arc((cx - s * .55, cy - s * .9, cx + s * .25, cy - s * .1), 90, 270, fill=c, width=max(2, ancho - 1))


def hilos(centro, nombres, titulo="El encanto", w=1500, h=640):
    """marca 0: el centro brilla · marcas 1..n: cada seguidor entra atado con un hilo dorado · marca n+1: los hilos se
    cortan, el centro se apaga y los seguidores quedan unidos por líneas rojas (se enfrentan)."""
    fn_, ftit, fs = fuente("r", 46), fuente("r", 40), fuente("i", 34)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 250
        rota = _eo((dt - mk[n + 1]) / .5)
        pts = []
        for i in range(n):
            ang = math.pi * (.92 - .84 * i / max(1, n - 1))
            pts.append((cx + math.cos(ang) * w * .40, cy + math.sin(ang) * 260))
        for i, (x, y) in enumerate(pts):
            u = _eo((dt - mk[1 + i]) / .5)
            if u <= 0:
                continue
            if rota < 1:                                    # hilo dorado que ondula; al romperse le falta el centro
                seg, ant = 24, (cx, cy)
                for k in range(1, seg + 1):
                    t = k / seg * u
                    p = (cx + (x - cx) * t, cy + (y - cy) * t + math.sin(t * 9 + dt * 3 + i) * 6)
                    if not (rota > 0 and abs(t - .5) < .1 * rota + .02):
                        d.line([ant, p], fill=ORO + (int(200 * u * (1 - rota)),), width=2)
                    ant = p
            _nodo(d, x, y, nombres[i], None, PERGAMINO if rota < .5 else ROJO, 255 * u, fn_, fs, abajo=True)
        if rota > 0:                                        # se enfrentan entre ellos
            for i in range(n):
                for j in range(i + 1, n):
                    if (i + j) % 2:
                        _linea(d, pts[i], pts[j], rota, ROJO, 150 * rota, 2)
        uc = _eo((dt - mk[0]) / .5)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        col = ORO if rota < .5 else GRIS
        r = 16 + 3 * math.sin(dt * 4) * (1 - rota)
        dd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(255 * uc),))
        _texto(dd, (cx, cy - 34), centro, fuente("r", 60), col, "mb", 255 * uc, sombra=False)
        im.alpha_composite(_brillo(txt, 14, 2.0 * (1 - .6 * rota)))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cosido(alma=("Radahn", "el alma"), cuerpo=("Mohg", "el cuerpo"), resultado="Consorte prometido",
           titulo="Dos hermanos cosidos en uno", w=1400, h=640):
    """marca 0: el alma (izquierda, dorado) · marca 1: el cuerpo (derecha, rojo) · marca 2: los dos se juntan al centro con
    una costura en zigzag y aparece `resultado`."""
    fn_, fs, fr = fuente("r", 64), fuente("i", 38), fuente("r", 70)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        u0, u1, u2 = (_eo((dt - mk[i]) / .6) for i in range(3))
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), fuente("r", 40), PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cy = M + h * .45
        xa = M + w * .22 + (w * .12) * u2
        xb = M + w * .78 - (w * .12) * u2
        for x, (nom, sub), col, u in ((xa, alma, ORO, u0), (xb, cuerpo, ROJO, u1)):
            if u <= 0:
                continue
            a = 255 * u
            d.ellipse((x - 110, cy - 110, x + 110, cy + 110), outline=col + (int(a),), width=4)
            _texto(d, (x, cy), nom, fn_, col, "mm", a)
            _texto(d, (x, cy + 130), sub, fs, GRIS, "mt", a * (1 - u2))
        if u2 > 0:                                          # costura entre los dos círculos
            cx = M + w / 2
            for k in range(int(9 * u2)):
                y0 = cy - 120 + k * 27
                d.line([(cx - 16, y0), (cx + 16, y0 + 13)], fill=PERGAMINO + (int(230 * u2),), width=3)
                d.line([(cx + 16, y0 + 13), (cx - 16, y0 + 27)], fill=PERGAMINO + (int(230 * u2),), width=3)
            txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(txt), (cx, M + h - 70), resultado.upper(), fr, AMBAR, "mm", 255 * u2, track=6, sombra=False)
            im.alpha_composite(_brillo(txt, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cruces(etiquetas, total=13, titulo="Las cruces de Miquella", w=1700, h=470, rojo_ultima=False):
    """Fila de `total` cruces apagadas; en la marca k se enciende la cruz k y su etiqueta sale debajo (la anterior se
    atenúa). Con `rojo_ultima`, la última etiqueta va en rojo."""
    ftit, fe = fuente("r", 40), fuente("i", 56)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(etiquetas) + 1)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        paso = (w - 160) / (total - 1)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i in range(total):
            x = M + 80 + i * paso
            u = _eo((dt - mk[i]) / .4) if i < len(etiquetas) else 0
            _cruz(d, x, M + 175, 44, GRIS, a0 * .55 * (1 - u))
            col = ROJO if (rojo_ultima and i == len(etiquetas) - 1) else ORO
            _cruz(dd, x, M + 175, 44, col, 255 * u)
        im.alpha_composite(_brillo(txt, 10, 1.6))
        d = ImageDraw.Draw(im)
        for k, s in enumerate(etiquetas):
            u = _eo((dt - mk[k]) / .4)
            fin = _eo((dt - mk[k + 1]) / .3) if k + 1 < len(etiquetas) else 0
            a = 255 * u * (1 - fin)
            if a > 0:
                col = ROJO if (rojo_ultima and k == len(etiquetas) - 1) else AMBAR
                _texto(d, (M + w / 2, M + h - 80), "Aquí abandono " + s, fe, col, "mm", a)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def triada(filas, titulo="Lo que quería de cada uno", w=1500, h=520):
    """filas = [(arriba, abajo), ...]: una columna por marca; la última se resalta en ámbar y las otras se tachan."""
    ftit, fa, fb = fuente("r", 40), fuente("r", 64), fuente("i", 44)
    n = len(filas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * n
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        ult = _eo((dt - mk[n - 1]) / .5)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i, (arriba, abajo) in enumerate(filas):
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            x = M + w * (i + .5) / n
            if i == n - 1:
                _texto(dd, (x, M + 230), arriba.upper(), fa, AMBAR, "mm", 255 * u, track=4, sombra=False)
                _texto(dd, (x, M + 330), abajo, fb, PERGAMINO, "mm", 255 * u, sombra=False)
            else:
                a = 255 * u * (1 - .5 * ult)
                _texto(d, (x, M + 230), arriba.upper(), fa, ORO, "mm", a, track=4)
                _texto(d, (x, M + 330), abajo, fb, GRIS, "mm", a)
                if ult > 0:                                 # tachado
                    _linea(d, (x - 160, M + 330), (x + 160, M + 330), ult, ROJO, 220 * ult, 4)
        im.alpha_composite(_brillo(txt, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_ranni_atrocidades (21-oct-2026)
LUNA = (150, 186, 255)


def _muneco(d, cx, cy, s, color, a, bal=0.0):
    """Muñeco de hilo con la cabeza en (cx, cy); `bal` lo balancea. Devuelve (cabeza, mano izq., mano der.) para atar hilos."""
    cadera = (cx + bal * s * .12, cy + s * 1.0)
    hombro = (cx + bal * s * .06, cy + s * .4)
    manos = [(hombro[0] + sg * s * .45, hombro[1] + s * .38 - sg * bal * s * .2) for sg in (-1, 1)]
    if a > 0:
        c = color + (int(a),)
        d.ellipse((cx - s * .22, cy - s * .22, cx + s * .22, cy + s * .22), fill=(14, 12, 9, int(a)), outline=c, width=4)
        d.line([(cx, cy + s * .22), cadera], fill=c, width=5)
        for sg, mano in zip((-1, 1), manos):
            d.line([hombro, (hombro[0] + sg * s * .28, hombro[1] + s * .12), mano], fill=c, width=4)
            d.line([cadera, (cadera[0] + sg * s * .14, cadera[1] + s * .32),
                    (cadera[0] + sg * s * .2, cadera[1] + s * .66 + sg * bal * s * .08)], fill=c, width=4)
    return (cx, cy - s * .22), manos[0], manos[1]


def _cruceta(d, cx, y, ancho, color, a):
    if a <= 0:
        return
    c = color + (int(a),)
    d.line([(cx - ancho / 2, y), (cx + ancho / 2, y)], fill=c, width=7)
    d.line([(cx, y - 34), (cx, y + 34)], fill=c, width=7)
    d.ellipse((cx - 9, y - 9, cx + 9, y + 9), fill=c)


def marionetas(titiritero="Seluvis", munecos=("Nepheli", "Ranni"), dueno="Ranni", titulo="Quién mueve los hilos",
               remate="El titiritero era el muñeco", w=1500, h=660):
    """marca 0: la cruceta del titiritero · marcas 1..n: cada muñeco cuelga de sus hilos (el último en ámbar: el objetivo)
    · marca n+1: la escena se apaga y aparece la cruceta de `dueno` (azul luna) con el titiritero colgando en rojo."""
    fn_, ftit, fr = fuente("r", 48), fuente("r", 40), fuente("i", 50)
    n = len(munecos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx = M + w / 2
        vuelta = _eo((dt - mk[n + 1]) / .7)
        a1 = 255 * _eo((dt - mk[0]) / .5) * (1 - vuelta)
        yc = M + 190
        # --- 1.ª parte: el titiritero y sus muñecos
        _cruceta(d, cx, yc, w * .62, ORO, a1)
        _texto(d, (cx, yc - 48), titiritero, fn_, ORO, "mb", a1)
        for i, nom in enumerate(munecos):
            u = _eo((dt - mk[1 + i]) / .6)
            a = 255 * u * (1 - vuelta)
            if a <= 0:
                continue
            x = M + w * (.5 + (i - (n - 1) / 2) * (.62 / max(1, n)))
            yh = M + 290 - 40 * (1 - u)
            col = AMBAR if i == n - 1 else PERGAMINO
            cab, mi, md = _muneco(d, x, yh, 150, col, a, math.sin(dt * 1.6 + i * 1.3))
            for p, xo in ((cab, 0), (mi, -.12), (md, .12)):
                d.line([(x + xo * w * .3, yc), p], fill=PERGAMINO + (int(a * .55),), width=2)
            _texto(d, (x, yh + 268), nom, fn_, col, "mt", a)
        # --- 2.ª parte: la vuelta
        if vuelta > 0:
            a2 = 255 * vuelta
            txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dd = ImageDraw.Draw(txt)
            _cruceta(dd, cx, yc, w * .34, LUNA, a2)
            _texto(dd, (cx, yc - 48), dueno, fn_, LUNA, "mb", a2, sombra=False)
            im.alpha_composite(_brillo(txt, 12, 1.6))
            d = ImageDraw.Draw(im)
            yh = M + 290
            cab, mi, md = _muneco(d, cx, yh, 150, ROJO, a2, math.sin(dt * 2.2) * 1.3)
            for p, xo in ((cab, 0), (mi, -.1), (md, .1)):
                d.line([(cx + xo * w * .3, yc), p], fill=LUNA + (int(a2 * .7),), width=2)
            _texto(d, (cx + 150, yh + 60), titiritero, fn_, ROJO, "lm", a2)
            _texto(d, (cx, M + h - 60), remate, fr, AMBAR, "mm", 255 * _eo((dt - mk[n + 1] - .6) / .6))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _dedos(d, cx, cy, color, a):
    """Los Dos Dedos: dos dedos largos y pálidos con sus pliegues."""
    if a <= 0:
        return
    for alto, dx in ((120, -22), (104, 22)):
        d.rounded_rectangle((cx + dx - 15, cy - alto, cx + dx + 15, cy), 15, fill=(30, 26, 20, int(a)), outline=color + (int(a),), width=3)
        for f in (.55, .28):
            d.line([(cx + dx - 8, cy - alto * f), (cx + dx + 8, cy - alto * f)], fill=color + (int(a * .6),), width=2)


def sombra(ama="Ranni", sombra_="Blaidd", amos="Los Dos Dedos", titulo="La sombra de Ranni", w=1500, h=660):
    """marca 0: los Dos Dedos · marca 1: hilos dorados a la Empírea y a su sombra (unidos entre sí) · marca 2: ella corta su
    hilo y se vuelve azul luna («libre») · marca 3: la sombra tiembla en rojo («maldición»)."""
    fn_, fs, ftit = fuente("r", 54), fuente("i", 38), fuente("r", 40)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        u0, u1, u2, u3 = (_eo((dt - mk[i]) / .6) for i in range(4))
        cx, ya = M + w / 2, M + 250
        xa, xs, yb = M + w * .30, M + w * .70, M + 470
        _dedos(d, cx, ya, PERGAMINO, 255 * u0)
        _texto(d, (cx, ya + 14), amos, fs, PERGAMINO, "mt", 255 * u0)
        for (x, y), roto, col in (((xa, yb), u2, ORO), ((xs, yb), 0, ROJO if u3 > .5 else ORO)):
            if u1 <= 0:
                continue
            seg, ant = 22, (cx, ya + 56)
            for k in range(1, seg + 1):
                t = k / seg * u1
                p = (cx + (x - cx) * t, ya + 56 + (y - 70 - ya - 56) * t + math.sin(t * 8 + dt * 3) * 5)
                if not (roto > 0 and abs(t - .55) < .14 * roto):
                    d.line([ant, p], fill=col + (int(220 * u1 * (1 - .6 * roto)),), width=3)
                ant = p
        # la Empírea
        col_a = LUNA if u2 > .5 else PERGAMINO
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        r = 18 + 3 * math.sin(dt * 3) * u2
        dd.ellipse((xa - r, yb - r, xa + r, yb + r), fill=col_a + (int(255 * u1),))
        _texto(dd, (xa, yb + 34), ama, fn_, col_a, "mt", 255 * u1, sombra=False)
        im.alpha_composite(_brillo(txt, 12, 1.2 + 1.2 * u2))
        d = ImageDraw.Draw(im)
        _texto(d, (xa, yb + 102), "libre" if u2 > .5 else "Empírea", fs, LUNA if u2 > .5 else GRIS, "mt", 255 * u1)
        # la sombra: tiembla al enloquecer
        xs_ = xs + math.sin(dt * 37) * 7 * u3
        yb_ = yb + math.cos(dt * 29) * 5 * u3
        col_s = ROJO if u3 > .5 else GRIS
        if u1 <= 0:                                          # ImageDraw no mezcla alfa: con 0 abriría un agujero en el panel
            return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
        d.ellipse((xs_ - 26, yb_ - 26, xs_ + 26, yb_ + 26), fill=(6, 5, 4, int(255 * u1)), outline=col_s + (int(255 * u1),), width=4)
        _texto(d, (xs_, yb_ + 34), sombra_, fn_, ROJO if u3 > .5 else PERGAMINO, "mt", 255 * u1)
        _texto(d, (xs_, yb_ + 102), "maldición" if u3 > .5 else "su sombra", fs, col_s, "mt", 255 * u1)
        paso = (xs - xa - 80) / 22                           # el lazo ama-sombra (línea de puntos)
        for k in range(0, int(22 * u1), 2):
            x0 = xa + 40 + k * paso
            d.line([(x0, yb), (x0 + paso, yb)], fill=col_s + (int(200 * u1),), width=3)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def domino(fichas, titulo="La primera ficha", w=1700, h=600):
    """fichas = textos cortos (causa -> efecto). En la marca k cae la ficha k sobre la siguiente y su texto se enciende en
    ámbar (luego queda en pergamino); la última cae del todo y se tiñe de rojo."""
    ftit, fe = fuente("r", 40), fuente("i", 40)
    n = len(fichas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 1)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        sp = (w - 280) / n                                   # sitio a la derecha para la última, que cae del todo
        tw, th, base = 66, 240, M + 330
        for i, s in enumerate(fichas):
            xc = M + 60 + sp * (i + .5)
            u = _eo((dt - mk[i]) / .55)
            ult = i == n - 1
            tmax = math.radians(76) if ult else math.asin(min(1.0, (sp - tw) / th))
            ang = tmax * (u ** 1.6)
            piv = (xc + tw / 2, base)
            pts = [(piv[0] + px * math.cos(ang) - py * math.sin(ang), piv[1] + px * math.sin(ang) + py * math.cos(ang))
                   for px, py in ((-tw, 0), (0, 0), (0, -th), (-tw, -th))]
            col = ROJO if (ult and u > .5) else (ORO if u > 0 else ORO_OSC)
            d.polygon(pts, fill=(18, 15, 11, int(a0)))
            d.line(pts + [pts[0]], fill=col + (int(a0),), width=3)
            mx, my = (pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2
            d.ellipse((mx - 7, my - 7, mx + 7, my + 7), fill=col + (int(a0),))
            sig = _eo((dt - mk[i + 1]) / .4) if i + 1 < n else 0
            ct = ROJO if ult else (AMBAR if sig < .5 else PERGAMINO)
            for k, ln in enumerate(_partir(d, s, fe, sp - 14)):
                _texto(d, (xc, base + 40 + k * 46), ln, fe, ct, "mt", 255 * u)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _estrella(d, x, y, r, color, a):
    if a <= 0:
        return
    d.polygon([(x, y - r), (x + r * .28, y - r * .28), (x + r, y), (x + r * .28, y + r * .28), (x, y + r),
               (x - r * .28, y + r * .28), (x - r, y), (x - r * .28, y - r * .28)], fill=color + (int(a),))


def constelacion(nombres, centro="Ranni", tu="Tú", remate="Mil años de noche", titulo="Los que la quisieron", w=1500, h=660):
    """La Luna (`centro`) con una estrella por nombre unida por un hilo de luz; en la marca k la estrella k se apaga y su
    hilo se corta · marca n: aparece «Tú» pegado a la Luna · marca n+1: `remate` en ámbar."""
    fn_, ftit, fr = fuente("r", 42), fuente("r", 40), fuente("r", 64)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 300
        for k in range(40):                                  # polvo de estrellas que titila
            x = M + 40 + (k * 337) % (w - 80)
            y = M + 110 + (k * 191) % (h - 160)
            d.point((x, y), fill=PERGAMINO + (int(a0 * .25 * (1 + math.sin(dt * 2 + k))),))
        pts = [(cx + math.cos(-math.pi / 2 + 2 * math.pi * i / n + .3) * w * .36,
                cy + math.sin(-math.pi / 2 + 2 * math.pi * i / n + .3) * 175) for i in range(n)]
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i, (x, y) in enumerate(pts):
            ua = _eo((dt - .15 * i) / .5)
            off = _eo((dt - mk[i]) / .5)
            if off < 1:
                _linea(dd, (cx, cy), (x, y), ua, LUNA, 120 * ua * (1 - off), 2)
            col = PERGAMINO if off < .5 else GRIS
            _estrella(dd if off < .5 else d, x, y, 16 + 3 * math.sin(dt * 3 + i) * (1 - off), col, 255 * ua * (1 - .55 * off))
            _texto(d, (x, y + 26), nombres[i], fn_, col, "mt", 255 * ua * (1 - .45 * off))
        dd.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=LUNA + (int(a0),))          # la Luna, en cuarto
        dd.ellipse((cx - 40, cy - 70, cx + 70, cy + 40), fill=(8, 7, 5, int(a0 * .55)))
        u_tu = _eo((dt - mk[n]) / .6)
        if u_tu > 0:
            xt, yt = cx + 150, cy - 30
            _linea(dd, (cx + 55, cy - 10), (xt, yt), u_tu, AMBAR, 255 * u_tu, 4)
            _estrella(dd, xt, yt, 22, AMBAR, 255 * u_tu)
            _texto(dd, (xt + 34, yt), tu, fn_, AMBAR, "lm", 255 * u_tu, sombra=False)
        im.alpha_composite(_brillo(txt, 12, 1.7))
        d = ImageDraw.Draw(im)
        _texto(d, (cx, cy + 80), centro, fn_, LUNA, "mt", a0)
        u_r = _eo((dt - mk[n + 1]) / .6)
        if u_r > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (cx, M + h - 38), remate.upper(), fr, AMBAR, "mm", 255 * u_r, track=8, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn
