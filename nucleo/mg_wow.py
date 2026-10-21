# -*- coding: utf-8 -*-
"""MOTION GRAPHICS «interfaz de WoW» por código (Crónicas de Warcraft). Sustituye a los de Remotion del sistema viejo
(`C:\\googleimagenes\\holavideo\\src\\Composition_mg_wow.tsx`, aprobados por el usuario el 11-oct-2026): panel azul noche con
borde dorado, título serif oro, casillas con íconos reales de WoW, números que corren y el remate en verde; entra con rebote
y sale fundido. Regla de canal: 3 por video, en momentos con una cifra o comparación que se entienda mejor animada.
CERO cifras inventadas: el MG solo muestra números que el guion ya dice.

Uso desde videos/<v>/efectos.py (FX `mg` de nucleo/secuencia_fx.py):
    import mg_wow as M
    FX = [dict(tipo="mg", fn=M.filas("FOGATAS", [("Básica", 3, ["spell_fire_fire"]), ...]),
               de="La fogata básica", a=("experto diez|fin", 2.0), marcas=["tres muebles", "oficial cinco", "experto diez"],
               y=.80, sale=.4)]
`marcas` son anclas de la voz; cada fábrica dice qué hace en cada una. Íconos = nombres de Wowhead (wow.zamimg.com), se
guardan en nucleo/datos/iconos_wow/.
  filas(titulo, [(etiqueta, n, íconos), ...])       casillas que se llenan, una fila por marca (cuántos caben en cada cosa)
  grupos(titulo, [(n, ícono, rótulo, color), ...])  una fila de íconos partida en grupos que se encienden con cada marca;
                                                     un grupo con rótulo None se queda apagado con «?» (lo que falta)
  contadores(titulo, [(ícono, etiqueta, valor, i_ini, i_fin), ...], remate=(texto, i))   números que corren de 0 al valor
                                                     entre dos marcas; el remate sale en verde en su marca
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ORO, ORO_T, VERDE, BLANCO, GRIS = (201, 162, 39), (255, 209, 0), (30, 255, 0), (255, 255, 255), (140, 140, 150)
_FD = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]
_FUENTES = dict(serif=("georgiab.ttf",), sans=("Poppins-SemiBold.ttf", "segoeuib.ttf"), negra=("Poppins-Black.ttf", "seguibl.ttf"))
_fc, _ic, _bc = {}, {}, {}


def fuente(nombre, tam):
    if (nombre, tam) not in _fc:
        r = next((os.path.join(c, n) for n in _FUENTES[nombre] for c in _FD if os.path.exists(os.path.join(c, n))),
                 "C:/Windows/Fonts/segoeuib.ttf")
        _fc[(nombre, tam)] = ImageFont.truetype(r, tam)
    return _fc[(nombre, tam)]


def icono(nombre, tam, apagado=False):
    k = (nombre, tam, apagado)
    if k not in _ic:
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos", "iconos_wow")
        r = os.path.join(d, nombre.lower() + ".jpg")
        if not os.path.exists(r):
            import requests
            os.makedirs(d, exist_ok=True)
            x = requests.get(f"https://wow.zamimg.com/images/wow/icons/large/{nombre.lower()}.jpg", timeout=30)
            x.raise_for_status()
            open(r, "wb").write(x.content)
        im = Image.open(r).convert("RGBA").resize((tam, tam), Image.LANCZOS)
        if apagado:                                   # gris y medio transparente: lo que aún no se consigue
            g = im.convert("L").convert("RGBA")
            g.putalpha(110)
            im = g
        _ic[k] = im
    return _ic[k]


def _pop(dt, dur=0.35):
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1.6 else 1 - math.exp(-6 * u) * math.cos(9 * u)


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _texto(d, xy, s, f, color, ancla="la", alfa=255):
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    d.text((xy[0] + 2, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(a * .8)), anchor=ancla)
    d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla)


def _base(w, h, titulo):
    """Panel con sombra, degradado azul noche, doble borde dorado y título con adornos (se calcula una vez)."""
    k = (w, h, titulo)
    if k not in _bc:
        M = 26
        im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((M + 6, M + 14, M + w - 6, M + h + 8), 18, fill=(0, 0, 0, 200))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        g = Image.new("RGBA", (w, h))
        gd = ImageDraw.Draw(g)
        for y in range(h):
            q = y / h
            gd.line([(0, y), (w, y)], fill=(int(20 - 9 * q), int(27 - 12 * q), int(68 - 26 * q), 240))
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), 16, fill=255)
        im.paste(g, (M, M), mask)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((M, M, M + w - 1, M + h - 1), 16, outline=ORO + (255,), width=4)
        d.rounded_rectangle((M + 8, M + 8, M + w - 9, M + h - 9), 11, outline=ORO + (70,), width=1)
        if titulo:
            f = fuente("serif", 40)
            cx, cy = M + w / 2, M + 46
            _texto(d, (cx, cy), titulo, f, ORO_T, "mm")
            mitad = d.textlength(titulo, font=f) / 2
            for s in (-1, 1):                         # adornos: línea y rombo a cada lado del título
                x0, x1 = cx + s * (mitad + 22), cx + s * (mitad + 150)
                d.line([(x0, cy), (x1, cy)], fill=ORO + (200,), width=2)
                d.polygon([(x0, cy - 6), (x0 + s * 6, cy), (x0, cy + 6), (x0 - s * 6, cy)], fill=ORO_T + (255,))
        _bc[k] = (im, M)
    im, M = _bc[k]
    return im.copy(), M


def _casilla(im, d, x, y, t, ico, u, apagado=False):
    """Casilla de inventario; u = s desde que se llenó (None = vacía)."""
    d.rounded_rectangle((x, y, x + t, y + t), 7, fill=(4, 6, 18, 235), outline=(95, 82, 45, 255), width=2)
    if u is None or u <= 0:
        return
    s = _pop(u, .3)
    tt = max(2, int((t - 8) * s))
    ic = icono(ico, t - 8, apagado)
    if tt != t - 8:
        ic = ic.resize((tt, tt), Image.BILINEAR)
    im.alpha_composite(ic, (int(x + t / 2 - tt / 2), int(y + t / 2 - tt / 2)))
    if not apagado:
        d.rounded_rectangle((x, y, x + t, y + t), 7, outline=ORO + (255,), width=2)


def _salida(im, dt):
    s = _pop(dt, .45)
    if s <= 0.02:
        return np.zeros((2, 2, 4), np.uint8)
    if abs(s - 1) > .004:
        im = im.resize((max(2, int(im.width * s)), max(2, int(im.height * s))), Image.BILINEAR)
    return np.array(im)[..., [2, 1, 0, 3]].copy()


def filas(titulo, filas_, ancho=1240):
    """filas_ = [(etiqueta, n, [íconos]), ...]: todas las casillas se ven vacías desde el inicio; la fila k se llena en la
    marca k (una casilla cada 0,06 s) y su número corre hasta n; el número de la última fila sale en verde."""
    T, G = 64, 12
    alto_fila = T + 18
    h = 96 + len(filas_) * alto_fila + 20

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        for k, (et, n, icos) in enumerate(filas_):
            tk = marcas[k] if k < len(marcas) else 0.6 + k * 0.8
            y = M + 92 + k * alto_fila
            lleno = dt >= tk
            _texto(d, (M + 40, y + T / 2), et, fuente("sans", 34), BLANCO if lleno else GRIS, "lm")
            for i in range(n):
                _casilla(im, d, M + 320 + i * (T + G), y, T, icos[i % len(icos)], dt - tk - i * .06 if lleno else None)
            if lleno:
                v = min(n, 1 + int((dt - tk) / .06))
                ult = k == len(filas_) - 1
                _texto(d, (M + ancho - 44, y + T / 2), str(v), fuente("serif", 58), VERDE if ult and v == n else ORO_T, "rm")
        return _salida(im, dt)
    return fn


def grupos(titulo, grupos_, ancho=1560):
    """grupos_ = [(n, ícono, rótulo, color), ...] en una sola fila de íconos de 60 px; el grupo k se enciende en la marca k
    (uno cada 0,07 s) y pone su rótulo debajo. rótulo None = se queda apagado con «?»."""
    T, G, GG = 60, 10, 40
    total = sum(g[0] for g in grupos_)
    w_ico = total * T + (total - len(grupos_)) * G + (len(grupos_) - 1) * GG
    h = 96 + T + 74

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x, y, km = M + (ancho - w_ico) / 2, M + 92, 0
        for n, ico, rot, color in grupos_:
            x0 = x
            if rot is None:
                for i in range(n):
                    _casilla(im, d, int(x), y, T, ico, 1.0, apagado=True)
                    _texto(d, (x + T / 2, y + T / 2), "?", fuente("serif", 40), ORO_T, "mm", 140 + 115 * (.5 + .5 * math.sin(dt * 4)))
                    x += T + G
                x += GG - G
                continue
            tk = marcas[km] if km < len(marcas) else 0.6 + km
            km += 1
            for i in range(n):
                u = dt - tk - i * .07
                _casilla(im, d, int(x), y, T, ico, 1.0, apagado=True)
                if u > 0:
                    _casilla(im, d, int(x), y, T, ico, u)
                x += T + G
            x -= G
            if dt >= tk + n * .07:
                a = 255 * _eo((dt - tk - n * .07) / .3)
                _texto(d, ((x0 + x) / 2, y + T + 36), rot, fuente("sans", 30), color, "mm", a)
                d.line([(x0 + 6, y + T + 12), (x - 6, y + T + 12)], fill=tuple(color) + (int(a * .7),), width=3)
            x += GG
        return _salida(im, dt)
    return fn


def contadores(titulo, filas_, remate=None, ancho=1180):
    """filas_ = [(ícono, etiqueta, valor, i_ini, i_fin), ...]: la fila aparece en la marca i_ini (None = desde el inicio) y su
    número corre de 0 a `valor`, frenando, hasta la marca i_fin. remate = (texto, i_marca): en verde, con destello."""
    T = 72
    alto_fila = T + 22
    h = 96 + len(filas_) * alto_fila + (70 if remate else 10)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        for k, (ico, et, valor, i0, i1) in enumerate(filas_):
            t0 = marcas[i0] if i0 is not None else 0.0
            t1 = marcas[i1] if i1 is not None else t0 + 2.5
            if dt < t0:
                continue
            y = M + 92 + k * alto_fila
            a = 255 * _eo((dt - t0) / .3)
            _casilla(im, d, M + 40, y, T, ico, dt - t0)
            _texto(d, (M + 40 + T + 26, y + T / 2), et, fuente("sans", 34), BLANCO, "lm", a)
            u = (dt - t0) / max(.3, t1 - t0)
            v = valor if u >= 1 else int(round(valor * (1 - (1 - max(0.0, u)) ** 2.2)))
            listo = u >= 1
            f = fuente("serif", 70 if listo else 64)
            _texto(d, (M + ancho - 46, y + T / 2), str(max(v, 0)), f, ORO_T if not listo else BLANCO, "rm", a)
        if remate and len(marcas) > remate[1] and dt >= marcas[remate[1]]:
            u = dt - marcas[remate[1]]
            s = _pop(u, .35)
            f = fuente("negra", max(8, int(46 * s)))
            _texto(d, (M + ancho / 2, M + h - 44), remate[0], f, VERDE, "mm")
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ pantalla completa (18-oct-2026, petición del usuario)
def pantalla(ruta, zoom=(1.0, 1.10), pan=(0.0, 0.0, 0.0, 0.0), W=1920, H=1080, oscuro=0.0):
    """Imagen REAL a cuadro entero con movimiento lento (zoom de zoom[0] a zoom[1] y paneo de (x0, y0) a (x1, y1), -1..1 del
    margen que deja el zoom) para el FX `pantalla`: cuando el clip de fondo no enseña lo que la curiosidad necesita ver
    (el Portal Oscuro apagado, la Muralla de Cringris...). Si la imagen no es apaisada (arte vertical, carta), va entera al
    centro sobre ella misma desenfocada y oscurecida. `oscuro` (0..1) apaga un poco la imagen para que lean las pegatinas.
    Fundidos: `entra=`/`sale=` del FX."""
    import cv2
    zm = max(zoom)
    bw, bh = int(W * zm), int(H * zm)
    im = Image.open(ruta).convert("RGB")

    def cubrir(img, w, h):
        e = max(w / img.width, h / img.height)
        r = img.resize((max(w, int(img.width * e + .5)), max(h, int(img.height * e + .5))), Image.LANCZOS)
        return r.crop(((r.width - w) // 2, (r.height - h) // 2, (r.width - w) // 2 + w, (r.height - h) // 2 + h))

    if im.width / im.height < 1.45:                    # vertical o casi cuadrada: entera, sobre su propio fondo desenfocado
        base = cubrir(im, bw, bh).filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * .42))
        e = bh * .92 / im.height
        fg = im.resize((int(im.width * e), int(im.height * e)), Image.LANCZOS)
        x, y = (bw - fg.width) // 2, (bh - fg.height) // 2
        sombra = Image.new("L", base.size, 0)
        ImageDraw.Draw(sombra).rectangle((x + 14, y + 20, x + fg.width + 14, y + fg.height + 20), fill=170)
        base.paste((0, 0, 0), (0, 0), sombra.filter(ImageFilter.GaussianBlur(22)))
        base.paste(fg, (x, y))
    else:
        base = cubrir(im, bw, bh)
    arr = np.array(base)[..., ::-1].copy()
    if oscuro:
        arr = (arr * (1 - oscuro)).astype(np.uint8)

    def fn(dt, dur, marcas):
        u = min(1.0, max(0.0, dt / max(dur, .1)))
        u = u * u * (3 - 2 * u)
        z = zoom[0] + (zoom[1] - zoom[0]) * u
        px, py = pan[0] + (pan[2] - pan[0]) * u, pan[1] + (pan[3] - pan[1]) * u
        s = z / zm                                     # píxeles de salida por píxel de la base
        hx, hy = (bw - W / s) / 2, (bh - H / s) / 2    # margen que deja el zoom a cada lado
        cx, cy = bw / 2 + px * hx, bh / 2 + py * hy
        M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
        f = cv2.warpAffine(arr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return np.dstack([f, np.full((H, W), 255, np.uint8)])
    return fn


# ------------------------------------------------------------------ MG nuevos de `wow_curiosidades_kalimdor` (21-oct-2026)
# Regla del 19-oct (MG NUEVOS por guion): diseñados para ESE guion, pero genéricos para que otro video los use si de verdad
# cuentan mejor su escena. Retratos = imágenes reales (pegatinas de Wowpedia) en medallón dorado.
#   runas(titulo, n, ico_runa, ico_agua, origen, rotulo_medio, remate)   cadena de suministro: n runas que se apagan
#   linaje(madre, padre, hijos, titulo, rotulo_final)                    pareja -> hijos que se vuelven contra el padre
#   cadena(titulo, [(img, l1, l2, rojo), ...], remate)                    causa -> efecto en medallones con flechas
#   consola(titulo, [(etiqueta, estado, color, i), ...], sellos)          terminal titán que teclea su veredicto + sellos
ROJO, CIAN = (235, 45, 40), (120, 205, 255)
_mc = {}


def _medallon(ruta, r, gris=False):
    """Retrato real recortado en círculo (cuadrado de arriba si es vertical: ahí suele estar la cara) con aro dorado."""
    k = (ruta, r, gris)
    if k not in _mc:
        im = Image.open(ruta).convert("RGBA")
        lado = min(im.size)
        x0 = (im.width - lado) // 2
        y0 = 0 if im.height > im.width else (im.height - lado) // 2
        im = im.crop((x0, y0, x0 + lado, y0 + lado)).resize((2 * r, 2 * r), Image.LANCZOS)
        fondo = Image.new("RGBA", im.size, (10, 14, 34, 255))
        fondo.alpha_composite(im)
        im = fondo.convert("L").convert("RGBA") if gris else fondo
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
        out = Image.new("RGBA", (2 * r + 12, 2 * r + 12), (0, 0, 0, 0))
        out.paste(im, (6, 6), m)
        d = ImageDraw.Draw(out)
        d.ellipse((2, 2, 2 * r + 9, 2 * r + 9), outline=ORO + (255,), width=5)
        d.ellipse((10, 10, 2 * r + 1, 2 * r + 1), outline=ORO + (90,), width=1)
        _mc[k] = out
    return _mc[k]


def _pegar(im, sub, cx, cy, s=1.0, alfa=1.0):
    """Pega `sub` centrado en (cx, cy), escalado s y con opacidad alfa."""
    if s <= 0.02 or alfa <= 0.01:
        return
    if abs(s - 1) > .004:
        sub = sub.resize((max(2, int(sub.width * s)), max(2, int(sub.height * s))), Image.BILINEAR)
    if alfa < .99:
        sub = sub.copy()
        sub.putalpha(sub.getchannel("A").point(lambda v: int(v * alfa)))
    im.alpha_composite(sub, (int(cx - sub.width / 2), int(cy - sub.height / 2)))


def _mk(marcas, i, defecto):
    return marcas[i] if i < len(marcas) else defecto


def _sello(im, texto, cx, cy, u, color, tam=40, ang=-6):
    """Sello de goma que cae girado y rebota (u = s desde su marca)."""
    if u <= 0:
        return
    f = fuente("negra", tam)
    tw = int(ImageDraw.Draw(im).textlength(texto, font=f))
    capa = Image.new("RGBA", (tw + 60, tam + 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rounded_rectangle((4, 4, capa.width - 5, capa.height - 5), 10, outline=color + (255,), width=5)
    d.text((capa.width / 2, capa.height / 2), texto, font=f, fill=color + (255,), anchor="mm")
    capa = capa.rotate(ang, expand=True, resample=Image.BICUBIC)
    s = 1.6 - .6 * _pop(u, .3)                         # cae desde grande
    _pegar(im, capa, cx, cy, s, _eo(u / .15))


def runas(titulo, n, ico_runa, ico_agua, origen, rotulo_medio, remate, ancho=1500):
    """Cadena de suministro hasta un jefe (c22: las 7 runas del Núcleo de Magma y el agua de Azshara).
    marca 0: aparecen las n runas ardiendo (halo que late) · 1: entra el agua por la izquierda con `origen` debajo y una línea
    punteada avanza hasta las runas · 2: `rotulo_medio` (p. ej. «CADA SEMANA») late sobre la línea · 3: las runas se apagan
    una a una (gris azulado + vapor) con el contador k/n y al final sale `remate` en verde."""
    T, G = 92, 20
    w_r = n * T + (n - 1) * G
    h = 96 + T + 170

    def fn(dt, dur, marcas):
        t0, t1, t2, t3 = _mk(marcas, 0, .3), _mk(marcas, 1, 2.5), _mk(marcas, 2, 4.5), _mk(marcas, 3, 6.5)
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        y = M + 124
        x0 = M + ancho - 50 - w_r
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        vapor = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh, dv = ImageDraw.Draw(halo), ImageDraw.Draw(vapor)
        if dt >= t1:                                   # el agua y su camino
            u = dt - t1
            _pegar(im, icono(ico_agua, T), M + 56 + T / 2, y + T / 2, _pop(u))
            _texto(d, (M + 56 + T / 2, y + T + 34), origen, fuente("sans", 30), CIAN, "mm", 255 * _eo(u / .3))
            xa, xb = M + 56 + T + 18, x0 - 18
            xe = xa + (xb - xa) * _eo(u / 1.2)
            for xx in np.arange(xa, xe, 26):
                d.line([(xx, y + T / 2), (min(xx + 14, xe), y + T / 2)], fill=CIAN + (255,), width=5)
            if xe >= xb - 1:
                d.polygon([(xb, y + T / 2 - 11), (xb + 14, y + T / 2), (xb, y + T / 2 + 11)], fill=CIAN + (255,))
        if dt >= t2:
            u = dt - t2
            a = 255 * _eo(u / .3) * (.75 + .25 * math.sin(u * 5))
            _texto(d, ((M + 56 + T + x0) / 2, y + T / 2 - 34), rotulo_medio, fuente("negra", 30), ORO_T, "mm", a)
        apagadas = 0
        for i in range(n):                             # halos de las que arden (capa aparte, detrás)
            x = x0 + i * (T + G)
            if t0 + i * .08 <= dt < t3 + .3 + i * .32:
                lat = .55 + .45 * math.sin(dt * 7 + i * 1.3)
                for k in range(4, 0, -1):
                    rr = T * (.5 + k * .05)
                    dh.ellipse((x + T / 2 - rr, y + T / 2 - rr, x + T / 2 + rr, y + T / 2 + rr),
                               fill=(255, 110 + 25 * k, 20, int(40 * lat)))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(6)))
        for i in range(n):
            x = x0 + i * (T + G)
            ta, tz = t0 + i * .08, t3 + .3 + i * .32
            if dt < ta:
                d.rounded_rectangle((x, y, x + T, y + T), 9, fill=(4, 6, 18, 235), outline=(95, 82, 45, 255), width=2)
                continue
            if dt < tz:                                # ardiendo
                _casilla(im, d, x, y, T, ico_runa, dt - ta)
            else:                                      # apagada: gris azulado y vapor que sube
                apagadas += 1
                u = dt - tz
                _casilla(im, d, x, y, T, ico_runa, 1.0, apagado=True)
                d.rounded_rectangle((x, y, x + T, y + T), 9, outline=CIAN + (255,), width=3)
                for k in range(3):
                    v = (u * 1.4 + k * .33) % 1.0
                    rr = 7 + 10 * v
                    cx, cy = x + T / 2 + (k - 1) * 18, y - 4 - 26 * v
                    dv.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(230, 240, 255, int(120 * (1 - v) * _eo(u / .3))))
        im.alpha_composite(vapor)
        if dt >= t3:
            _texto(d, (x0 + w_r / 2, y + T + 34), f"{apagadas} / {n}", fuente("serif", 40),
                   VERDE if apagadas == n else BLANCO, "mm")
        tf = t3 + .3 + (n - 1) * .32 + .4
        if dt >= tf:
            s = _pop(dt - tf, .35)
            _texto(d, (x0 + w_r / 2, M + h - 34), remate, fuente("negra", max(8, int(40 * s))), VERDE, "mm")
        return _salida(im, dt)
    return fn


def linaje(madre, padre, hijos, titulo, rotulo_final, ancho=1500):
    """Pareja -> descendencia -> la descendencia se vuelve contra el padre (c18: Theradras + Zaetar = los centauros).
    madre/padre/hijos = (ruta_imagen, nombre, subtítulo). marca 0 madre · 1 padre · 2 lazo dorado entre ambos y línea que baja
    a los hijos · 3 flecha ROJA de los hijos al padre, el padre se vuelve gris y una cruz roja lo tacha · 4 `rotulo_final`."""
    R, h = 112, 700

    def fn(dt, dur, marcas):
        t = [_mk(marcas, i, .4 + i * 1.6) for i in range(5)]
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        pm, pp, ph = (M + 290, M + 250), (M + ancho - 290, M + 250), (M + ancho / 2, M + 500)
        mid = ((pm[0] + pp[0]) / 2, pm[1])
        if dt >= t[2]:                                 # lazo y descendencia
            u = _eo((dt - t[2]) / .6)
            for s in (-1, 1):
                xa = mid[0] + s * (mid[0] - pm[0] - R - 14)
                d.line([(xa, mid[1]), (xa + (mid[0] - xa) * u, mid[1])], fill=ORO_T + (255,), width=5)
            if u >= 1:
                d.ellipse((mid[0] - 14, mid[1] - 14, mid[0] + 14, mid[1] + 14), fill=ORO_T + (255,))
                u2 = _eo((dt - t[2] - .6) / .5)
                d.line([(mid[0], mid[1] + 14), (mid[0], mid[1] + 14 + (ph[1] - R - 30 - mid[1]) * u2)],
                       fill=ORO_T + (255,), width=5)
        roto = dt >= t[3]
        for (ruta, nom, sub), p, tk, gris in ((madre, pm, t[0], False), (padre, pp, t[1], roto), (hijos, ph, t[2] + 1.0, False)):
            if dt < tk:
                continue
            u = dt - tk
            _pegar(im, _medallon(ruta, R, gris), p[0], p[1], _pop(u))
            a = 255 * _eo(u / .3)
            if p is ph:                                # los hijos: nombre a la derecha del medallón
                _texto(d, (p[0] + R + 30, p[1] - 18), nom, fuente("sans", 34), BLANCO, "lm", a)
                _texto(d, (p[0] + R + 30, p[1] + 22), sub, fuente("sans", 25), ORO_T, "lm", a)
            else:
                _texto(d, (p[0], p[1] + R + 34), nom, fuente("sans", 34), BLANCO, "mm", a)
                _texto(d, (p[0], p[1] + R + 72), sub, fuente("sans", 25), ORO_T, "mm", a)
        if roto:                                       # traición: flecha roja hijos -> padre y cruz
            u = _eo((dt - t[3]) / .5)
            xa, ya = ph[0] + R * .75, ph[1] - R * .65
            xb, yb = pp[0] - R * .7, pp[1] + R * .75
            xe, ye = xa + (xb - xa) * u, ya + (yb - ya) * u
            d.line([(xa, ya), (xe, ye)], fill=ROJO + (255,), width=8)
            if u >= 1:
                ang = math.atan2(yb - ya, xb - xa)
                d.polygon([(xb + 18 * math.cos(ang), yb + 18 * math.sin(ang)),
                           (xb + 16 * math.cos(ang + 2.3), yb + 16 * math.sin(ang + 2.3)),
                           (xb + 16 * math.cos(ang - 2.3), yb + 16 * math.sin(ang - 2.3))], fill=ROJO + (255,))
                k = R * .8 * _eo((dt - t[3] - .5) / .35)
                d.line([(pp[0] - k, pp[1] - k), (pp[0] + k, pp[1] + k)], fill=ROJO + (255,), width=12)
                d.line([(pp[0] + k, pp[1] - k), (pp[0] - k, pp[1] + k)], fill=ROJO + (255,), width=12)
        if dt >= t[4]:
            _sello(im, rotulo_final, M + 270, M + 560, dt - t[4], ROJO, 44)
        return _salida(im, dt)
    return fn


def cadena(titulo, eslabones, remate=None, ancho=1640):
    """Causa -> efecto en medallones unidos por flechas (c02: Valstann -> Fandral -> Ragnaros).
    eslabones = [(ruta_imagen, línea1, línea2, rojo), ...]: el eslabón k aparece en la marca k y su flecha avanza desde el
    anterior; rojo=True = aro y texto en rojo. remate = (texto, i_marca): toda la cadena se tiñe de rojo y sale el texto."""
    R, n = 100, len(eslabones)
    h = 96 + 2 * R + 150 + (60 if remate else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        paso = (ancho - 2 * 215) / max(1, n - 1)
        cy = M + 100 + R
        tr = marcas[remate[1]] if remate and len(marcas) > remate[1] else None
        tinte = _eo((dt - tr) / .6) if tr is not None and dt >= tr else 0.0
        for k, (ruta, l1, l2, rojo) in enumerate(eslabones):
            tk = _mk(marcas, k, .4 + k * 1.5)
            if dt < tk:
                continue
            cx = M + 215 + k * paso
            u = dt - tk
            if k:                                      # flecha desde el anterior
                xa, xb = cx - paso + R + 22, cx - R - 30
                xe = xa + (xb - xa) * _eo(u / .45)
                q = max(tinte, 1.0 if rojo else 0.0)
                col = tuple(int(ORO_T[i] + (ROJO[i] - ORO_T[i]) * q) for i in range(3))
                d.line([(xa, cy), (xe, cy)], fill=col + (255,), width=6)
                if xe >= xb - 1:
                    d.polygon([(xb, cy - 14), (xb + 20, cy), (xb, cy + 14)], fill=col + (255,))
            ut = u - (.45 if k else 0)
            if ut <= 0:
                continue
            _pegar(im, _medallon(ruta, R), cx, cy, _pop(ut))
            if rojo or tinte > 0:
                q = 1.0 if rojo else tinte
                aro = tuple(int(ORO[i] + (ROJO[i] - ORO[i]) * q) for i in range(3))
                d.ellipse((cx - R - 9, cy - R - 9, cx + R + 9, cy + R + 9), outline=aro + (255,), width=6)
            a = 255 * _eo(ut / .3)
            _texto(d, (cx, cy + R + 40), l1, fuente("sans", 30), ROJO if rojo else BLANCO, "mm", a)
            _texto(d, (cx, cy + R + 76), l2, fuente("sans", 24), ORO_T, "mm", a)
        if tinte > 0:
            s = _pop(dt - tr, .35)
            _texto(d, (M + ancho / 2, M + h - 40), remate[0], fuente("negra", max(8, int(40 * s))), ROJO, "mm")
        return _salida(im, dt)
    return fn


def consola(titulo, lineas, sellos=(), ancho=1640):
    """Terminal de los titanes que teclea su veredicto (c01: el Vigía de Piedra de Norgannon ante la puerta de Uldum).
    lineas = [(etiqueta, estado, color, i_marca), ...]: la etiqueta se teclea (0,03 s por letra), puntos guía y el estado a
    la derecha en su color. sellos = [(texto, color, i_marca), ...]: caen como sellos de goma en fila abajo."""
    h = 96 + 30 + len(lineas) * 64 + (140 if sellos else 20)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        f, fe = fuente("sans", 36), fuente("negra", 36)
        for k, (et, est, col, i) in enumerate(lineas):
            tk = _mk(marcas, i, .4 + k * 1.2)
            if dt < tk:
                continue
            y = M + 130 + k * 64
            nch = int((dt - tk) / .03)
            cursor = "_" if nch < len(et) + 8 and int(dt * 3) % 2 == 0 else ""
            _texto(d, (M + 60, y), "> " + et[:nch] + cursor, f, CIAN, "lm")
            if nch >= len(et):
                x0 = M + 60 + d.textlength("> " + et, font=f) + 16
                x1 = M + ancho - 60 - d.textlength(est, font=fe) - 16
                u = _eo((dt - tk - len(et) * .03) / .4)
                xx = x0
                while xx < x0 + (x1 - x0) * u:
                    d.ellipse((xx, y + 4, xx + 5, y + 9), fill=CIAN + (150,))
                    xx += 16
                if u >= 1:
                    _texto(d, (M + ancho - 60, y), est, fe, col, "rm", 255 * _eo((dt - tk - len(et) * .03 - .4) / .2))
        for k, (txt, col, i) in enumerate(sellos):
            if len(marcas) <= i:
                continue
            cx = M + ancho * (k + .5) / len(sellos)
            _sello(im, txt, cx, M + h - 76, dt - marcas[i], col, 28, ang=-5 + 4 * k)
        return _salida(im, dt)
    return fn
