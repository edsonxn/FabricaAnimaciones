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
  juramento(clausulas, firmas, remate)           contrato en pergamino: cláusulas por marca, firmas que se pudren, sello rojo
                                                 (er_malenia_atrocidades, 23-oct-2026)
  contagio(nombres, centro, remate)              flor escarlata que late; una vena roja tiñe cada nombre del anillo por marca
  floraciones(etiquetas, final)                  tres capullos: se abren la 1.ª y la 2.ª; la 3.ª late en rojo con `final`
  repudio(madre, hijas, remate)                  madre unida a sus hijas por hilos dorados que se parten en rojo
  acuerdo(da, pides, letra, remate)              contrato de dos columnas; la letra pequeña crece en rojo y sella «Deber»
                                                 (er_melina_atrocidades, 27-oct-2026)
  ecos(lineas, firma, revela)                    citas que se escriben con el Círculo de Elden girando; la firma se tacha
  arbol_arde(etapas)                             el Árbol Áureo por código: la llama llega, trepa, la copa arde, llueve ceniza
  muerte_suelta(nombres, remate)                 Runa de la Muerte presa en eslabones que saltan; ondas que tachan a todos
  lanzas(bando, centro, tu)                      las lanzas del enemigo se clavan en el león rojo y vuelven contra ti como
                                                 flechas de gravedad (er_radahn_atrocidades, 28-oct-2026)
  cielo_sujeto(atados, quien, remate)            cielo quieto: hilos de gravedad atan estrellas (destinos) a `quien`; al caer
                                                 se rompen, el cielo gira y cae una estrella
  balanza(izq, der, pesos, remate)               balanza de pruebas que se inclina por marca; al final vuelve al centro
  espejo(padre, hijo, papel_padre, papel_hijo, idolo)   el padre y el hijo acaban en el mismo papel; el ídolo se tacha
  cien(titulo, encendidos, remate)               100 estrellas apagadas; se encienden N (campaña de suscripción, 30-oct-2026)
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


# ------------------------------------------------------------------ er_malenia_atrocidades (23-oct-2026)
CARMIN = (196, 40, 52)
TINTA = (46, 32, 20)


def _petalos(d, cx, cy, r, abre, color, a, n=7, giro=0.0):
    """Flor escarlata: `n` pétalos (elipses rotadas) que se abren con `abre` (0 = capullo cerrado, 1 = abierta)."""
    if a <= 0:
        return
    for i in range(n):
        ang = giro + 2 * math.pi * i / n
        sep = r * (.15 + .55 * abre)
        px, py = cx + math.cos(ang) * sep, cy + math.sin(ang) * sep
        largo, ancho = r * (.45 + .5 * abre), r * (.22 + .18 * abre)
        pts = []
        for k in range(16):
            t = 2 * math.pi * k / 16
            ex, ey = math.cos(t) * largo, math.sin(t) * ancho
            pts.append((px + ex * math.cos(ang) - ey * math.sin(ang), py + ex * math.sin(ang) + ey * math.cos(ang)))
        d.polygon(pts, fill=color + (int(a * .85),))
    d.ellipse((cx - r * .18, cy - r * .18, cx + r * .18, cy + r * .18), fill=AMBAR + (int(a),))


def juramento(clausulas, firmas=5, remate="Firme aquí", titulo="Juramento de los caballeros", w=1240, h=660):
    """Contrato en pergamino: marca k (< n) escribe la cláusula k; marca n: aparecen las firmas de los caballeros, que
    luego se pudren (manchas rojas que crecen sin parar); marca n+1: sello rojo `remate` que cae sobre el papel."""
    ftit, fc, fs = fuente("b", 42), fuente("i", 40), fuente("b", 64)
    n = len(clausulas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        pap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dp = ImageDraw.Draw(pap)
        x0, y0, x1, y1 = M + 70, M + 40, M + w - 70, M + h - 40
        dp.rounded_rectangle((x0, y0, x1, y1), 10, fill=(214, 198, 158, int(a0)))
        dp.rounded_rectangle((x0 + 14, y0 + 14, x1 - 14, y1 - 14), 6, outline=ORO_OSC + (int(a0 * .8),), width=2)
        _texto(dp, ((x0 + x1) / 2, y0 + 58), titulo.upper(), ftit, TINTA, "mm", a0, track=5, sombra=False)
        _filete(dp, (x0 + x1) / 2, y0 + 92, (x1 - x0) * .32, color=ORO_OSC, alfa=a0)
        y = y0 + 140
        for k, c in enumerate(clausulas):
            u = _eo((dt - mk[k]) / 1.1)
            if u <= 0:
                continue
            for ln in _partir(dp, f"{k + 1}. {c}", fc, x1 - x0 - 120):
                vis = ln[:int(len(ln) * u + .999)]
                _texto(dp, (x0 + 60, y), vis, fc, TINTA, "lm", 255 * min(1, u * 3), sombra=False)
                y += 50
            y += 14
        u_f = _eo((dt - mk[n]) / .9)
        manchas = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dm = ImageDraw.Draw(manchas)
        yf = y1 - 90
        for i in range(firmas):
            cx = x0 + 90 + (x1 - x0 - 180) * (i + .5) / firmas
            p = _eo((dt - mk[n] - .18 * i) / .7)
            if p <= 0:
                continue
            pts = [(cx - 70 + 140 * t, yf + 16 * math.sin(t * 9 + i * 1.7) * (1 - t * .4) - 10 * math.cos(t * 21 + i))
                   for t in [j / 40 for j in range(int(40 * p) + 1)]]
            if len(pts) > 1:
                dp.line(pts, fill=TINTA + (int(a0),), width=3)
            dp.line([(cx - 80, yf + 30), (cx + 80, yf + 30)], fill=TINTA + (int(a0 * .5),), width=1)
            pod = max(0.0, dt - mk[n] - .9 - .25 * i)                         # la carne se pudre: no para de crecer
            if pod > 0:
                r = min(70, 14 + 26 * pod)
                for j in range(3):
                    ox, oy = 26 * math.sin(i * 3 + j * 2.1), 14 * math.cos(i * 5 + j)
                    dm.ellipse((cx + ox - r * .7, yf + oy - r * .5, cx + ox + r * .7, yf + oy + r * .5),
                               fill=CARMIN + (int(min(150, 60 + 50 * pod)),))
        pap.alpha_composite(manchas.filter(ImageFilter.GaussianBlur(6)))
        u_s = _eo((dt - mk[n + 1]) / .35)
        if u_s > 0:
            sello = Image.new("RGBA", (560, 170), (0, 0, 0, 0))
            ds = ImageDraw.Draw(sello)
            ds.rounded_rectangle((8, 8, 552, 162), 12, outline=CARMIN + (230,), width=8)
            _texto(ds, (280, 88), remate.upper(), fs, CARMIN, "mm", 235, track=4, sombra=False)
            esc = 1.7 - .7 * u_s
            sello = sello.resize((int(560 * esc), int(170 * esc))).rotate(-9, expand=True)
            sa = np.array(sello)
            sa[..., 3] = (sa[..., 3] * u_s).astype(np.uint8)
            sello = Image.fromarray(sa)
            pap.alpha_composite(sello, (int((x0 + x1) / 2 + 150 - sello.width / 2), int(y0 + 345 - sello.height / 2)))
        im.alpha_composite(pap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def contagio(nombres, centro="La flor", remate=None, titulo="Lo que pudrió una flor", w=1500, h=660):
    """Flor escarlata al centro que late; un nombre por marca en el anillo: una vena roja sale de la flor y lo tiñe
    (pergamino -> carmín). Con `remate`, la última marca + 1 lo enciende abajo en ámbar."""
    fn_, ftit, fr = fuente("r", 46), fuente("r", 40), fuente("r", 58)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 1)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 285
        pts = [(M + 110 + (w - 220) * (i + .5) / n, M + 505 + 22 * math.sin(i * 1.9)) for i in range(n)]
        venas = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dv = ImageDraw.Draw(venas)
        tocados = 0
        for i, (x, y) in enumerate(pts):
            u = _eo((dt - mk[i]) / .7)
            tocados += u > .5
            if u > 0:
                mx, my = (cx + x) / 2 + 40 * math.sin(i * 2.3), (cy + y) / 2 + 30
                seg = [(cx + (mx - cx) * t * 2, cy + (my - cy) * t * 2) if t < .5 else
                       (mx + (x - mx) * (t - .5) * 2, my + (y - my) * (t - .5) * 2) for t in [j / 30 for j in range(int(30 * u) + 1)]]
                if len(seg) > 1:
                    dv.line(seg, fill=CARMIN + (int(230 * u),), width=6)
        im.alpha_composite(_brillo(venas, 8, 1.4))
        d = ImageDraw.Draw(im)
        for i, (x, y) in enumerate(pts):
            u = _eo((dt - mk[i]) / .7)
            ua = _eo((dt - .12 * i) / .5)
            col = tuple(int(PERGAMINO[c] + (CARMIN[c] - PERGAMINO[c]) * u) for c in range(3))
            r = 9 + 5 * u * (1 + math.sin(dt * 5 + i))
            d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(255 * ua),))
            _texto(d, (x, y + 22), nombres[i], fn_, col, "mt", 255 * ua)
        flor = Image.new("RGBA", im.size, (0, 0, 0, 0))
        lat = 1 + .06 * math.sin(dt * 3.2) + .04 * tocados
        _petalos(ImageDraw.Draw(flor), cx, cy, 78 * lat, _eo(dt / 1.2), CARMIN, a0, giro=dt * .15)
        im.alpha_composite(_brillo(flor, 14, 1.5))
        d = ImageDraw.Draw(im)
        _texto(d, (cx + 120, cy - 20), centro, fuente("i", 38), AMBAR, "lm", a0)
        if remate:
            u_r = _eo((dt - mk[n]) / .6)
            if u_r > 0:
                t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
                _texto(ImageDraw.Draw(t2), (cx, M + h - 40), remate.upper(), fr, AMBAR, "mm", 255 * u_r, track=8, sombra=False)
                im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def floraciones(etiquetas, final="Diosa de la putrefacción", titulo="Las tres flores", w=1500, h=600):
    """Tres capullos en fila. Marca k (k < 2) abre la flor k con su etiqueta; la marca 2 enciende el tercero en rojo, que
    late cada vez más grande con `final` debajo (lo que pasaría con la tercera flor)."""
    fe, ftit, ff = fuente("r", 42), fuente("r", 40), fuente("b", 50)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        flor = Image.new("RGBA", im.size, (0, 0, 0, 0))
        df = ImageDraw.Draw(flor)
        for i in range(3):
            cx, cy = M + w * (i + .5) / 3, M + 280
            u = _eo((dt - mk[i]) / .9)
            ua = _eo((dt - .15 * i) / .5)
            if i < 2:
                _petalos(df, cx, cy, 95, u, CARMIN if u > 0 else ORO_OSC, 255 * ua * (.45 + .55 * max(u, .0)), giro=i)
                txt = f"{i + 1}.ª · {etiquetas[i]}" if u > 0 else f"{i + 1}.ª"
                _texto(d, (cx, cy + 135), txt, fe, PERGAMINO if u > 0 else GRIS, "mt", 255 * ua)
            else:
                lat = (1 + .10 * math.sin(dt * (4 + 3 * u))) * (1 + .35 * u)
                col = ROJO if u > 0 else ORO_OSC
                _petalos(df, cx, cy, 95 * lat, .25 + .75 * u, col, 255 * ua * (.45 + .55 * u), giro=dt * .3 * u)
                _texto(d, (cx, cy + 135), "3.ª · ?" if u <= 0 else "3.ª", fe, GRIS if u <= 0 else ROJO, "mt", 255 * ua)
                if u > 0:
                    _texto(d, (M + w / 2, M + h - 40), final.upper(), ff, ROJO, "mm", 255 * u, track=4)
        im.alpha_composite(_brillo(flor, 12, 1.4))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def repudio(madre, hijas, titulo="Las hijas de la flor", remate="Como hizo tu madre", w=1500, h=640):
    """`madre` arriba unida por hilos dorados a cada hija (entran escalonadas desde la marca 0). Marca 1: los hilos se
    tiñen de rojo y se parten por la mitad, y aparece `remate`. Marca 2 (opcional): la primera hija se enciende en ámbar."""
    fn_, fs, ftit, fr = fuente("r", 46), fuente("i", 32), fuente("r", 40), fuente("i", 44)
    n = len(hijas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        mx, my = M + w / 2, M + 170
        corte = _eo((dt - mk[1]) / .6)
        luz = _eo((dt - mk[2]) / .6)
        hil = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(hil)
        for i, (nom, sub) in enumerate(hijas):
            hx, hy = M + 120 + (w - 240) * (i + .5) / n, M + 430
            u = _eo((dt - mk[0] - .25 * i) / .6)
            col = tuple(int(ORO[c] + (ROJO[c] - ORO[c]) * corte) for c in range(3))
            if corte < .05:
                _linea(dh, (mx, my + 16), (hx, hy - 16), u, col, 230 * u, 3)
            else:
                g = 40 * corte
                vx, vy = hx - mx, hy - my
                L = math.hypot(vx, vy)
                ux, uy = vx / L, vy / L
                medio = (mx + vx / 2, my + vy / 2)
                dh.line([(mx, my + 16), (medio[0] - ux * g, medio[1] - uy * g - 10 * corte)], fill=col + (230,), width=3)
                dh.line([(medio[0] + ux * g, medio[1] + uy * g + 18 * corte), (hx, hy - 16)], fill=col + (int(230 * (1 - .5 * corte)),), width=3)
            c_h = AMBAR if (i == 0 and luz > .5) else PERGAMINO
            _nodo(d, hx, hy, nom, sub, c_h, 255 * u, fn_, fs, abajo=True)
        im.alpha_composite(_brillo(hil, 6, 1.3))
        d = ImageDraw.Draw(im)
        _nodo(d, mx, my, madre, None, CARMIN if corte > .5 else ORO, a0, fuente("b", 54), fs)
        if corte > 0:
            _texto(d, (mx, M + h - 46), f"«{remate}»", fr, ROJO, "mm", 255 * corte)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn



# ------------------------------------------------------------------ er_melina_atrocidades (27-oct-2026)
def acuerdo(da, pides, letra=None, titulo="El acuerdo", remate="Deber", w=1500, h=660):
    """El trato de Melina como un contrato de dos columnas: «Ella te da» (una línea por marca, con un rombo dorado) y
    «Tú la llevas» (marca len(da)). Con `letra`, la marca siguiente hace crecer la letra pequeña abajo en rojo, los
    regalos se tiñen de carmín (eran un préstamo) y la siguiente estampa el sello `remate`. Pensado para salir dos veces."""
    ftit, fc = fuente("r", 40), fuente("r", 42)
    fs = fuente("b", 60)
    n = len(da)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        xm = M + w * .60
        d.line([(xm, M + 120), (xm, M + h - 170)], fill=ORO_OSC + (int(a0 * .7),), width=2)
        _texto(d, (M + 80, M + 130), "ELLA TE DA", fuente("r", 32), GRIS, "lm", a0, track=4)
        _texto(d, (xm + 50, M + 130), "TÚ LA LLEVAS", fuente("r", 32), GRIS, "lm", a0, track=4)
        u_l = _eo((dt - mk[n + 1]) / .9) if letra else 0.0
        for k, s in enumerate(da):
            u = _eo((dt - mk[k]) / .5)
            if u <= 0:
                continue
            y = M + 200 + 70 * k
            col = tuple(int(ORO[c] + (CARMIN[c] - ORO[c]) * u_l) for c in range(3))
            cx = M + 98 - 30 * (1 - u)
            d.polygon([(cx, y - 14), (cx + 12, y), (cx, y + 14), (cx - 12, y)], fill=col + (int(255 * u * (.78 + .22 * math.sin(dt * 2.4 + k))),))
            _texto(d, (cx + 34, y), s, fc, PERGAMINO if u_l < .5 else (236, 196, 188), "lm", 255 * u)
        u_p = _eo((dt - mk[n]) / .6)
        if u_p > 0:
            for j, ln in enumerate(_partir(d, pides, fc, w * .34)):
                _texto(d, (xm + 50, M + 210 + 56 * j), ln, fc, AMBAR, "lm", 255 * u_p)
        if letra and u_l > 0:
            esc = .35 + .65 * u_l
            f2 = fuente("i", max(12, int(48 * esc)))
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d2 = ImageDraw.Draw(t2)
            lineas = _partir(d2, letra, f2, w - 200)
            for j, ln in enumerate(lineas):
                yl = M + h - 110 + (j - (len(lineas) - 1) / 2) * 48 * esc
                _texto(d2, (M + w / 2, yl), ln, f2, ROJO, "mm", 255 * u_l)
            im.alpha_composite(_brillo(t2, 8, 1.2 + .4 * math.sin(dt * 4)))
            u_s = _eo((dt - mk[n + 2]) / .35)
            if u_s > 0:
                sello = Image.new("RGBA", (420, 150), (0, 0, 0, 0))
                ds = ImageDraw.Draw(sello)
                ds.rounded_rectangle((8, 8, 412, 142), 12, outline=CARMIN + (235,), width=8)
                _texto(ds, (210, 76), remate.upper(), fs, CARMIN, "mm", 240, track=6, sombra=False)
                e = 1.7 - .7 * u_s
                sello = sello.resize((int(420 * e), int(150 * e))).rotate(8, expand=True)
                sa = np.array(sello)
                sa[..., 3] = (sa[..., 3] * u_s).astype(np.uint8)
                sello = Image.fromarray(sa)
                im.alpha_composite(sello, (int(M + w * .34 - sello.width / 2), int(M + 430 - sello.height / 2)))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def ecos(lineas, firma="una desconocida", revela="su madre", titulo="Palabras de una reina que desapareció", w=1500, h=640):
    """Los ecos de Márika que Melina recita: la marca k escribe la línea k en cursiva (las anteriores se apagan) con el
    Círculo de Elden girando tenue detrás; abajo firma «— `firma`». La marca len(lineas) tacha la firma y escribe
    «— `revela`» en carmín, que late."""
    ftit, fl, ff = fuente("r", 40), fuente("i", 50), fuente("i", 46)
    n = len(lineas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w / 2, M + h / 2 + 10
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(halo)
        for i, r in enumerate((210, 160)):
            g = dt * (.12 if i else -.08)
            for k in range(24):
                t0 = math.degrees(g + 2 * math.pi * k / 24)
                dh.arc((cx - r, cy - r, cx + r, cy + r), t0, t0 + 9, fill=ORO + (int(a0 * .22),), width=3)
        dh.line([(cx, cy - 250), (cx, cy + 250)], fill=ORO + (int(a0 * .16),), width=3)
        im.alpha_composite(_brillo(halo, 6, 1.2))
        d = ImageDraw.Draw(im)
        _texto(d, (cx, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=5)
        _filete(d, cx, M + 80, w * .3, alfa=a0)
        actual = max([k for k in range(n) if dt >= mk[k]] or [-1])
        y = M + 150
        for k, s in enumerate(lineas):
            u = _eo((dt - mk[k]) / 1.0)
            if u <= 0:
                continue
            a = 255 * u * (1.0 if k == actual else .42)
            for ln in _partir(d, s, fl, w - 220):
                vis = ln[:int(len(ln) * min(1, u * 1.4) + .999)]
                _texto(d, (cx, y), vis, fl, PERGAMINO, "mm", a)
                y += 60
            y += 18
        u_r = _eo((dt - mk[n]) / .7)
        yf = M + h - 60
        f1 = "— " + firma
        wf = d.textlength(f1, font=ff)
        _texto(d, (M + w - 110, yf), f1, ff, GRIS, "rm", a0 * (1 - .55 * u_r))
        if u_r > 0:
            d.line([(M + w - 110 - wf * u_r, yf + 2), (M + w - 110, yf + 2)], fill=ROJO + (230,), width=4)
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            f3 = fuente("b", int(58 * (1 + .08 * math.sin(dt * 4))))
            _texto(ImageDraw.Draw(t2), (M + w - 110, yf - 64), "— " + revela.upper(), f3, CARMIN, "rm", 255 * u_r, track=4, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _llama(d, x, y, alto, ancho, t, fase, a):
    """Lengua de fuego: polígono que ondula (base ancha, punta fina); naranja por fuera, ámbar y blanco dentro."""
    if a <= 0 or alto < 4:
        return
    for capa, (col, k) in enumerate((((230, 92, 30), 1.0), (AMBAR, .62), ((255, 236, 170), .32))):
        izq, der = [], []
        for j in range(13):
            v = j / 12
            o1 = math.sin(t * 7 + fase + v * 5) * ancho * .25 * v
            o2 = math.sin(t * 7 + fase + v * 5 + 1.3) * ancho * .25 * v
            izq.append((x - ancho * k * (1 - v) ** .8 + o1, y - alto * k * v))
            der.append((x + ancho * k * (1 - v) ** .8 + o2, y - alto * k * v))
        d.polygon(izq + der[::-1], fill=col + (int(a * (.85 - .15 * capa)),))


def arbol_arde(etapas, titulo="El pecado capital", w=1500, h=760):
    """El Árbol Áureo por código (tronco y ramas doradas + copa de luces que respiran) sobre la silueta de la capital.
    Marca 0: la llama llega al pie · 1: el fuego trepa por el tronco · 2: la copa entera arde · 3: el árbol se apaga y
    llueve ceniza. Cada marca escribe su etiqueta a la izquierda (la vigente en ámbar; la de la ceniza en gris claro)."""
    ftit, fe = fuente("r", 40), fuente("r", 40)
    rng = np.random.default_rng(7)
    ramas = []

    def _crece(x, y, ang, largo, g, prof):
        x1, y1 = x + math.cos(ang) * largo, y - math.sin(ang) * largo
        ramas.append((x, y, x1, y1, g))
        if prof:
            for s in (-1, 1):
                _crece(x1, y1, ang + s * (.38 + .2 * rng.random()), largo * (.70 + .08 * rng.random()), max(2, g * .62), prof - 1)
    _crece(0, 0, math.pi / 2, 140, 24, 6)
    hojas = [(float(rng.normal(0, 170)), float(-290 - abs(rng.normal(0, 110))), float(rng.random() * 6.28)) for _ in range(150)]
    ceniza = [(float(rng.random()), float(rng.random()), float(.4 + rng.random())) for _ in range(140)]
    edif = [(-.36, .07, .05), (-.26, .10, .08), (-.15, .06, .05), (.13, .08, .06), (.23, .11, .09), (.33, .06, .04)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 5
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        bx, by = M + w * .63, M + h - 90
        u0 = _eo((dt - mk[0]) / .8)
        u1, u2 = _eo((dt - mk[1]) / 1.4), _eo((dt - mk[2]) / 1.4)
        apag = _eo((dt - mk[3]) / 1.0)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(cap)
        for x, ew, eh in edif:
            ex, ew, eh = bx + x * w, ew * w * .5, eh * w * 1.6
            dc.rectangle((ex - ew / 2, by - eh, ex + ew / 2, by + 40), fill=(34, 30, 24, int(a0)))
            dc.polygon([(ex - ew / 2, by - eh), (ex, by - eh - ew * .7), (ex + ew / 2, by - eh)], fill=(34, 30, 24, int(a0)))
        im.alpha_composite(cap)
        arb = Image.new("RGBA", im.size, (0, 0, 0, 0))
        da = ImageDraw.Draw(arb)
        col_t = tuple(int(ORO[c] * (1 - apag) + 64 * apag) for c in range(3))
        for x0, y0, x1, y1, g in ramas:
            da.line([(bx + x0, by + y0), (bx + x1, by + y1)], fill=col_t + (int(a0 * .95),), width=max(1, int(g)))
        for x, y, f in hojas:
            r = 5 + 3 * math.sin(dt * 2 + f)
            col = tuple(int(ORO[c] * (1 - u2) + (232, 96, 30)[c] * u2) for c in range(3))
            al = a0 * (.55 + .3 * math.sin(dt * 1.7 + f)) * (1 - apag)
            da.ellipse((bx + x - r, by + y - r, bx + x + r, by + y + r), fill=col + (int(max(0, al)),))
        im.alpha_composite(_brillo(arb, 12, 1.5 * (1 - .7 * apag)))
        fue = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dfu = ImageDraw.Draw(fue)
        vivo = 1 - apag
        if u0 > 0 and vivo > 0:
            _llama(dfu, bx, by + 6, 80 * u0, 36, dt, 0, 255 * u0 * vivo)
        if u1 > 0 and vivo > 0:
            for k in range(7):
                v = k / 6
                if v <= u1:
                    _llama(dfu, bx + 10 * math.sin(k * 2.1), by - 30 - 220 * v, 60 + 30 * u1, 22, dt, k, 230 * vivo)
        if u2 > 0 and vivo > 0:
            for x, y, f in hojas:
                r = (10 + 8 * math.sin(dt * 5 + f)) * u2
                dfu.ellipse((bx + x - r, by + y - r * 1.3, bx + x + r, by + y + r * .7), fill=(236, 104, 34, int(170 * u2 * vivo)))
            for x, y, f in hojas[::9]:
                _llama(dfu, bx + x, by + y + 16, 46 * u2, 16, dt, f, 200 * u2 * vivo)
        im.alpha_composite(_brillo(fue.filter(ImageFilter.GaussianBlur(2.5)), 12, 1.7))
        if apag > 0:
            cz = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dz = ImageDraw.Draw(cz)
            for x, y, v in ceniza:
                yy = M + 100 + ((y + (dt - mk[3]) * .09 * v) % 1.0) * (h - 140)
                xx = M + 60 + x * (w - 120) + 18 * math.sin(dt + y * 9)
                dz.ellipse((xx - 3, yy - 3, xx + 3, yy + 3), fill=(205, 198, 186, int(200 * apag)))
            im.alpha_composite(cz.filter(ImageFilter.GaussianBlur(1)))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        vig = max([k for k in range(len(etapas)) if dt >= mk[k]] or [-1])
        for k, s in enumerate(etapas):
            u = _eo((dt - mk[k]) / .5)
            if u <= 0:
                continue
            y = M + 170 + 90 * k
            col = (AMBAR if k < 3 else (215, 208, 196)) if k == vig else GRIS
            _texto(d, (M + 80 - 30 * (1 - u), y), s, fe, col, "lm", 255 * u)
            d.line([(M + 80, y + 30), (M + 80 + 330 * u, y + 30)], fill=ORO_OSC + (int(150 * u),), width=1)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def muerte_suelta(nombres, titulo="La Runa de la Muerte", remate="Indiscriminada", w=1500, h=660):
    """La Runa de la Muerte (hoja negra con filo rojo que late) presa en un anillo de eslabones dorados (el sello de
    Maliketh). Marca 0: «arrancada del Orden Áureo» · marca 1: los eslabones se rompen uno a uno («sello roto») · marca
    2: ondas negras y rojas se expanden, cada nombre de la fila de abajo se apaga en gris y se tacha, y sale `remate`."""
    ftit, fn_, fr, fs = fuente("r", 40), fuente("r", 42), fuente("b", 62), fuente("i", 34)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w / 2, M + 270
        u0, u1, u2 = _eo((dt - mk[0]) / .6), _eo((dt - mk[1]) / 1.2), _eo((dt - mk[2]) / 1.6)
        if u2 > 0:
            onda = Image.new("RGBA", im.size, (0, 0, 0, 0))
            do = ImageDraw.Draw(onda)
            for k in range(3):
                r = (u2 * 900 + (dt - mk[2]) * 60 - k * 140) % 1000
                do.ellipse((cx - r, cy - r * .7, cx + r, cy + r * .7), outline=(150, 20, 30, int(170 * (1 - r / 1000))), width=14)
            im.alpha_composite(onda.filter(ImageFilter.GaussianBlur(10)))
        hoja = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(hoja)
        lat = 1 + .05 * math.sin(dt * 3)
        L, A = 205 * lat, 36 * lat
        dh.polygon([(cx, cy - L), (cx + A, cy - L * .2), (cx + A * .6, cy + L * .6), (cx, cy + L),
                    (cx - A * .6, cy + L * .6), (cx - A, cy - L * .2)], fill=(18, 10, 12, int(a0)), outline=(190, 40, 50, int(a0)))
        dh.line([(cx - 70, cy - L * .25), (cx + 70, cy - L * .25)], fill=(190, 40, 50, int(a0)), width=5)
        im.alpha_composite(_brillo(hoja, 16, 1.6 + .8 * u2))
        cad = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dk = ImageDraw.Draw(cad)
        R, nb = 230, 28
        for k in range(nb):
            t = 2 * math.pi * k / nb + dt * .05
            x, y = cx + math.cos(t) * R, cy + math.sin(t) * R * .62
            orden = ((k * 11) % nb) / nb
            if dt >= mk[1] + orden * 1.2:                          # eslabón roto: sale volando y se apaga
                v = min(1.0, (dt - mk[1] - orden * 1.2) / .9)
                x, y = x + math.cos(t) * 160 * v, y + math.sin(t) * 110 * v + 60 * v * v
                a = a0 * (1 - v)
                if a > 4:
                    dk.ellipse((x - 13, y - 8, x + 13, y + 8), outline=ROJO + (int(a),), width=4)
                continue
            dk.ellipse((x - 13, y - 8, x + 13, y + 8), outline=ORO + (int(a0),), width=4)
        im.alpha_composite(_brillo(cad, 5, 1.1))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        if u0 > 0:
            _texto(d, (cx + 280, cy - 60), "arrancada del", fs, GRIS, "lm", 255 * u0 * (1 - .6 * u2))
            _texto(d, (cx + 280, cy - 18), "Orden Áureo", fuente("r", 44), ORO, "lm", 255 * u0 * (1 - .6 * u2))
        if u1 > 0:
            _texto(d, (cx - 280, cy - 40), "sello roto", fuente("i", 44), ROJO, "rm", 255 * u1 * (1 - .6 * u2))
        for i, s in enumerate(nombres):
            x, y = M + 120 + (w - 240) * (i + .5) / n, M + h - 130
            ua = _eo((dt - .1 * i) / .5)
            g = _eo(u2 * 1.6 - i / max(1, n) * .6)
            col = tuple(int(PERGAMINO[c] * (1 - g) + 96 * g) for c in range(3))
            _texto(d, (x, y), s, fn_, col, "mm", 255 * ua)
            if g > .4:
                wl = d.textlength(s, font=fn_) / 2 + 10
                d.line([(x - wl, y + 4), (x - wl + 2 * wl * min(1, (g - .4) / .6), y + 4)], fill=(170, 30, 40, 220), width=4)
        if u2 > .5:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (cx, M + h - 46), remate.upper(), fr, (210, 46, 56), "mm", 255 * _eo((u2 - .5) * 2),
                   track=8, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_radahn_atrocidades (28-oct-2026)
def cien(titulo, encendidos, remate=None, w=1240):
    """100 estrellas apagadas que aparecen en barrido desde la marca 0; en la marca 1 se encienden `encendidos`, repartidas;
    remate = (texto, i_marca) en ámbar abajo. Para «de cada 100 que ven el canal, solo N…» (mismo uso que mg_tes.rejilla)."""
    n, cols, P = 100, 20, 56
    h = 150 + 5 * P + (100 if remate else 30)
    vivas = {int(round((k + .5) * n / encendidos + 7)) % n for k in range(encendidos)}
    ftit, fr = fuente("r", 40), fuente("i", 64)

    def fn(dt, dur, marcas):
        t0 = marcas[0] if marcas else .3
        t1 = marcas[1] if len(marcas) > 1 else t0 + 2
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        x0, y0 = M + (w - (cols - 1) * P) / 2, M + 135
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i in range(n):
            r, c = divmod(i, cols)
            u = _eo((dt - t0 - (r + c) * .025) / .25)
            v = _eo((dt - t1) / .35) if i in vivas else 0
            _estrella(d, x0 + c * P, y0 + r * P, 17, GRIS, 140 * u * (1 - v))
            _estrella(dd, x0 + c * P, y0 + r * P, 17 + 5 * v, ORO, 255 * v)
        im.alpha_composite(_brillo(txt, 10, 1.6))
        if remate and len(marcas) > remate[1] and dt >= marcas[remate[1]]:
            a = 255 * _eo((dt - marcas[remate[1]]) / .4)
            _texto(ImageDraw.Draw(im), (M + w / 2, M + h - 56), remate[0], fr, AMBAR, "mm", a)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _lanza(d, x0, y0, x1, y1, color, a, ancho=5):
    """Asta de (x0,y0) a la punta (x1,y1), con punta triangular."""
    if a <= 0:
        return
    d.line([(x0, y0), (x1, y1)], fill=color + (int(a),), width=ancho)
    ang = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1 + math.cos(ang) * 22, y1 + math.sin(ang) * 22),
               (x1 + math.cos(ang + 2.5) * 13, y1 + math.sin(ang + 2.5) * 13),
               (x1 + math.cos(ang - 2.5) * 13, y1 + math.sin(ang - 2.5) * 13)], fill=color + (int(a),))


def lanzas(bando="Caballeros de Malenia", centro="Radahn", tu="Tú", titulo="Las lanzas del festival", n=7, w=1500, h=640):
    """Marca 0: las lanzas de `bando` (izquierda, plata) vuelan y se clavan en el león rojo del centro · marca 1: salen
    girando en rojo, con halo violeta de gravedad, y vuelan hacia `tu` (derecha) como flechas."""
    ftit, fn_, fs = fuente("r", 40), fuente("r", 44), fuente("i", 34)
    rng = np.random.default_rng(3)
    angs = [(-.55 + 1.1 * k / (n - 1)) + float(rng.normal(0, .05)) for k in range(n)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w * .5, M + h * .56
        ox, tx = M + 150, M + w - 150
        u0, u1 = dt - mk[0], dt - mk[1]
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(cap)
        lat = 1 + .03 * math.sin(dt * 2.4)
        for k in range(40):                                           # la melena roja del león
            t = 2 * math.pi * k / 40
            r0, r1 = 78 * lat, (118 + 14 * math.sin(k * 1.7 + dt * 3)) * lat
            dc.line([(cx + math.cos(t) * r0, cy + math.sin(t) * r0), (cx + math.cos(t) * r1, cy + math.sin(t) * r1)],
                    fill=(196, 58, 36, int(a0 * .9)), width=6)
        dc.ellipse((cx - 80, cy - 80, cx + 80, cy + 80), fill=(24, 18, 14, int(a0)), outline=ORO + (int(a0),), width=3)
        im.alpha_composite(_brillo(cap, 14, 1.2))
        lz = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lz)
        for k, ang in enumerate(angs):
            lag = k * .12
            v0 = _eo((u0 - lag) / .55)
            if v0 <= 0:
                continue
            px, py = cx - math.cos(ang) * 92, cy + math.sin(ang) * 92           # punta clavada
            bx, by = px - math.cos(ang) * 210, py + math.sin(ang) * 210         # cola
            sx, sy = ox - 40, cy + math.sin(ang) * 260                           # de dónde sale
            v1 = _eo((u1 - lag * .6) / .9)
            if v1 <= 0:
                x1, y1 = sx + (px - sx) * v0, sy + (py - sy) * v0
                _lanza(dl, x1 - (px - bx), y1 - (py - by), x1, y1, (200, 204, 212), a0 * min(1, v0 * 2))
            else:
                gx, gy = tx - 40, cy + (k - (n - 1) / 2) * 34
                hx, hy = cx + math.cos(ang) * 120, cy - math.sin(ang) * 70
                x1, y1 = hx + (gx - hx) * v1, hy + (gy - hy) * v1
                ang2 = math.atan2(y1 - cy, x1 - (cx - 200))
                _lanza(dl, x1 - math.cos(ang2) * 200, y1 - math.sin(ang2) * 200, x1, y1, (214, 70, 50),
                       a0 * (1 - .7 * max(0, v1 - .85) / .15))
        if u1 > 0:
            ha = np.array(lz.filter(ImageFilter.GaussianBlur(9)))
            ha[..., :3] = (150, 90, 230)
            im.alpha_composite(Image.fromarray(ha))
        im.alpha_composite(lz)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        _texto(d, (cx, cy + 150), centro, fn_, ORO, "mt", a0)
        ua, ub = _eo(u0 / .5), _eo(u1 / .5)
        if ua > 0:
            _texto(d, (ox + 60, M + h - 60), bando, fs, (200, 204, 212), "mm", 255 * ua)
        if ub > 0:
            _texto(d, (tx - 60, M + h - 60), "Ahora, flechas contra ti", fs, (214, 70, 50), "mm", 255 * ub)
            _nodo(d, tx, cy, tu, None, PERGAMINO, 255 * ub, fn_, fs)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cielo_sujeto(atados, quien="Radahn", remate="Las estrellas vuelven a moverse", titulo="El cielo sujeto", w=1500, h=700):
    """Cielo de estrellas QUIETO. Cada marca ata con un hilo violeta de gravedad a `quien` (abajo) una estrella con su
    etiqueta (lo que su victoria congeló). Marca len(atados): `quien` se tacha, los hilos se rompen en rojo, el cielo empieza
    a girar y cae una estrella grande con estela; sale `remate`."""
    ftit, fe, fq, fr = fuente("r", 40), fuente("r", 36), fuente("r", 46), fuente("i", 46)
    rng = np.random.default_rng(11)
    fondo = [(float(rng.random()), float(rng.random()) * .72, float(.6 + rng.random() * 1.6), float(rng.random() * 6.28))
             for _ in range(160)]
    n = len(atados)
    pos = [(.17 + .66 * (i / max(1, n - 1)), .26 + .10 * (i % 2)) for i in range(n)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        fin = dt - mk[n]
        suelta = _eo(fin / 1.0)
        giro = fin ** 1.6 * .05 if fin > 0 else 0.0
        qx, qy = M + w / 2, M + h - 130
        cx0, cy0 = M + w / 2, M + h * .95
        st = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(st)
        for x, y, r, f in fondo:
            px, py = M + 40 + x * (w - 80), M + 110 + y * (h - 200)
            if giro:
                ang = giro * (1.2 - y)
                dx, dy = px - cx0, py - cy0
                px, py = cx0 + dx * math.cos(ang) - dy * math.sin(ang), cy0 + dx * math.sin(ang) + dy * math.cos(ang)
            if M + 90 < py < M + h - 30 and M + 20 < px < M + w - 20:
                ds.ellipse((px - r, py - r, px + r, py + r), fill=(230, 226, 240, int(a0 * (.45 + .3 * math.sin(dt * 1.3 + f)))))
        im.alpha_composite(st)
        hl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(hl)
        for i in range(n):
            u = _eo((dt - mk[i]) / .7)
            if u <= 0:
                continue
            sx, sy = M + pos[i][0] * w, M + pos[i][1] * h + 40
            col = tuple(int((170, 120, 250)[c] * (1 - suelta) + ROJO[c] * suelta) for c in range(3))
            al = 255 * u * (1 - suelta)
            if al > 2:
                for j in range(3):                                     # hilo tenso que vibra
                    off = math.sin(dt * 9 + i + j) * 2
                    _linea(dh, (qx + off, qy - 30), (sx + off, sy), u, col, al * (.6 if j else 1), 3 if j == 0 else 1)
            r = 13 + 2 * math.sin(dt * 2 + i)
            dh.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(250, 244, 255, int(255 * u)))
        im.alpha_composite(_brillo(hl, 10, 1.6))
        d = ImageDraw.Draw(im)
        for i, s in enumerate(atados):
            u = _eo((dt - mk[i]) / .7)
            if u > 0:
                sx, sy = M + pos[i][0] * w, M + pos[i][1] * h + 40
                _texto(d, (sx, sy - 30), s, fe, PERGAMINO, "mb", 255 * u)
        cq = tuple(int(ORO[c] * (1 - suelta) + 90 * suelta) for c in range(3))
        d.ellipse((qx - 26, qy - 26, qx + 26, qy + 26), fill=(20, 14, 10, int(a0)), outline=cq + (int(a0),), width=4)
        _texto(d, (qx, qy + 40), quien, fq, cq, "mt", a0)
        if suelta > 0:
            wl = d.textlength(quien, font=fq) / 2 + 10
            d.line([(qx - wl, qy + 66), (qx - wl + 2 * wl * suelta, qy + 66)], fill=ROJO + (230,), width=4)
            v = min(1.0, max(0.0, (fin - .4) / 1.8))                  # la estrella que cae
            if 0 < v < 1:
                ex, ey = M + w * (.86 - .55 * v), M + 120 + (h - 300) * v ** 1.4
                cola = Image.new("RGBA", im.size, (0, 0, 0, 0))
                dk = ImageDraw.Draw(cola)
                for k in range(18):
                    q = k / 18
                    rr = 14 * (1 - q)
                    dk.ellipse((ex + 120 * q - rr, ey - 90 * q - rr, ex + 120 * q + rr, ey - 90 * q + rr),
                               fill=(200, 160, 255, int(220 * (1 - q))))
                im.alpha_composite(_brillo(cola, 16, 2.0))
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + 60), remate, fr, AMBAR, "mm", 255 * _eo((fin - .3) / .6), sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.4))
        else:
            _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
            _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def balanza(izq, der, pesos, remate="Nunca lo sabremos", titulo="¿Aceptó?", w=1500, h=720):
    """Balanza dorada con dos platillos (`izq`, `der`). Marca k deja caer pesos[k] = ("i"|"d", texto) en su platillo (el
    texto se apila debajo) y el brazo se inclina según cuántas pruebas tiene cada lado. Marca len(pesos): el brazo vuelve
    al centro, las pruebas se atenúan y sale `remate` en ámbar."""
    ftit, fl, fp, fr = fuente("r", 40), fuente("b", 46), fuente("r", 30), fuente("i", 50)
    n = len(pesos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w / 2, M + 210
        L = w * .29
        ni = sum(_eo((dt - mk[k]) / .6) for k, (l, _) in enumerate(pesos) if l == "i")
        nd = sum(_eo((dt - mk[k]) / .6) for k, (l, _) in enumerate(pesos) if l == "d")
        fin = _eo((dt - mk[n]) / 1.2)
        ang = max(-.2, min(.2, (nd - ni) * .07)) * (1 - fin) + .012 * math.sin(dt * 1.5)
        d = ImageDraw.Draw(im)
        d.line([(cx, cy), (cx, M + h - 70)], fill=ORO_OSC + (int(a0),), width=8)
        d.polygon([(cx - 70, M + h - 50), (cx + 70, M + h - 50), (cx, M + h - 95)], fill=ORO_OSC + (int(a0),))
        xi, yi = cx - math.cos(ang) * L, cy - math.sin(ang) * L
        xd, yd = cx + math.cos(ang) * L, cy + math.sin(ang) * L
        br = Image.new("RGBA", im.size, (0, 0, 0, 0))
        db = ImageDraw.Draw(br)
        db.line([(xi, yi), (xd, yd)], fill=ORO + (int(a0),), width=7)
        db.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=ORO + (int(a0),))
        for px, py in ((xi, yi), (xd, yd)):
            for s in (-1, 1):
                db.line([(px, py), (px + s * 110, py + 90)], fill=ORO_OSC + (int(a0),), width=2)
            db.chord((px - 125, py + 50, px + 125, py + 130), 0, 180, fill=(40, 32, 20, int(a0)), outline=ORO + (int(a0),), width=3)
        im.alpha_composite(_brillo(br, 6, 1.0))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        _texto(d, (xi, yi - 22), izq, fl, ORO, "mb", a0)
        _texto(d, (xd, yd - 22), der, fl, ORO, "mb", a0)
        cnt = {"i": 0, "d": 0}
        for k, (lado, s) in enumerate(pesos):
            u = _eo((dt - mk[k]) / .6)
            if u <= 0:
                continue
            j = cnt[lado]
            cnt[lado] += 1
            px, py = (xi, yi) if lado == "i" else (xd, yd)
            col = tuple(int(PERGAMINO[c] * (1 - .5 * fin)) for c in range(3))
            _texto(d, (px, py + 155 + 50 * j - 40 * (1 - u)), s, fp, col, "mt", 255 * u)
        if fin > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (cx, cy - 60), remate, fr, AMBAR, "mm", 255 * fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def espejo(padre=("Radagon", "dejó a Rennala"), hijo=("Radahn", "en un cuerpo prestado"), papel_padre="Consorte de Márika",
           papel_hijo="Consorte de Miquella", idolo="Godfrey", remate="De tal palo, tal astilla", titulo="El padre y el hijo",
           w=1500, h=640):
    """Dos filas en espejo. Marca 0: arriba, `padre` → caja `papel_padre` · marca 1: abajo, `hijo`, que de niño «soñaba con
    ser» `idolo` (se tacha), y su flecha llega a `papel_hijo` · marca 2: las dos cajas se encienden en ámbar unidas por un
    «=» y sale `remate`."""
    ftit, fn_, fs, fc, fr = fuente("r", 40), fuente("b", 48), fuente("i", 32), fuente("r", 40), fuente("i", 50)

    def caja(d, x, y, s, col, a):
        wl = d.textlength(s, font=fc) / 2 + 34
        d.rounded_rectangle((x - wl, y - 40, x + wl, y + 40), 14, fill=(26, 20, 14, int(a)), outline=col + (int(a),), width=3)
        _texto(d, (x, y), s, fc, col, "mm", a)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        u0, u1, u2 = _eo((dt - mk[0]) / .7), _eo((dt - mk[1]) / .7), _eo((dt - mk[2]) / .8)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        xa, xb = M + 210, M + w - 300
        ya, yb = M + 220, M + 450
        col_p = tuple(int(ORO[c] * (1 - u2) + AMBAR[c] * u2) for c in range(3))
        if u0 > 0:
            _nodo(d, xa, ya, padre[0], padre[1], ORO, 255 * u0, fn_, fs)
            _linea(d, (xa + 40, ya), (xb - 200, ya), u0, ORO_OSC, 255 * u0, 3)
            caja(d, xb, ya, papel_padre, col_p, 255 * u0)
        if u1 > 0:
            _nodo(d, xa, yb, hijo[0], hijo[1], ORO, 255 * u1, fn_, fs)
            mx = (xa + xb) / 2 - 70
            g = _eo((dt - mk[1] - .6) / .6)
            _texto(d, (mx, yb - 34), "soñaba con ser", fs, GRIS, "mb", 255 * u1)
            _texto(d, (mx, yb + 6), idolo, fn_, PERGAMINO, "mm", 255 * u1 * (1 - .5 * g))
            if g > 0:
                wl = d.textlength(idolo, font=fn_) / 2 + 10
                d.line([(mx - wl, yb + 10), (mx - wl + 2 * wl * g, yb + 10)], fill=ROJO + (230,), width=5)
                caja(d, xb, yb, papel_hijo, col_p, 255 * g)
        if u2 > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d2 = ImageDraw.Draw(t2)
            _texto(d2, (xb, (ya + yb) / 2), "=", fuente("b", 84), AMBAR, "mm", 255 * u2, sombra=False)
            _texto(d2, (M + w / 2, M + h - 40), remate, fr, AMBAR, "mm", 255 * u2, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.6))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn
