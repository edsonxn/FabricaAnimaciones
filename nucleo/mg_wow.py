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
  (más abajo, por video: runas/linaje/cadena/consola · ruta/forja/sorteo · paradero/simon/franquicia · altares/apariciones)
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


# ------------------------------------------------------------------ MG nuevos de `wow_objetos_raros` (22-oct-2026)
#   ruta(mapa, puntos, titulo, ...)   MAPA REAL del juego a cuadro entero (zona o continente de Wowhead Classic) con la ruta de
#                                     una cadena de misiones: pines numerados que salen en su marca, línea punteada dorada que se
#                                     dibuja de un paso al siguiente con un marcador que viaja, y una cámara que encuadra lo ya
#                                     visto. El último paso puede ser el objeto (ícono en medallón grande que late).
_mapc = {}


def _mapa(ruta, W, H, zmax):
    """Mapa escalado para cubrir W x H con resolución de sobra para el zoom máximo (se calcula una vez)."""
    k = (ruta, W, H, zmax)
    if k not in _mapc:
        im = Image.open(ruta).convert("RGB")
        e = max(W / im.width, H / im.height) * min(zmax, 2.0)
        im = im.resize((int(im.width * e), int(im.height * e)), Image.LANCZOS)
        _mapc[k] = np.array(im)[..., ::-1].copy()
    return _mapc[k]


def _bezier(a, b, curva):
    """Curva suave de a a b, arqueada `curva` veces la distancia hacia un lado; 40 puntos."""
    (x0, y0), (x1, y1) = a, b
    cx, cy = (x0 + x1) / 2 - (y1 - y0) * curva, (y0 + y1) / 2 + (x1 - x0) * curva
    t = np.linspace(0, 1, 40)[:, None]
    return (1 - t) ** 2 * np.array(a, float) + 2 * (1 - t) * t * np.array((cx, cy)) + t ** 2 * np.array(b, float)


def _panel_rotulo(l1, l2=None, color=ORO_T):
    """Rotulito de un paso: panel azul con borde dorado, línea 1 serif oro, línea 2 sans blanca."""
    f1, f2 = fuente("serif", 34), fuente("sans", 25)
    dd = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    w = int(max(dd.textlength(l1, font=f1), dd.textlength(l2 or "", font=f2))) + 44
    h = 58 + (34 if l2 else 0)
    im = Image.new("RGBA", (w + 16, h + 18), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((8, 12, w + 6, h + 12), 10, fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w + 4, h + 4), 10, fill=(14, 19, 50, 238), outline=ORO + (255,), width=3)
    _texto(d, (26, 32), l1, f1, color, "lm")
    if l2:
        _texto(d, (26, 70), l2, f2, BLANCO, "lm")
    return im


def _foto(fuente_img, alto=280, giro=0.0):
    """Foto de lo que nombra la voz en ese paso del mapa (regla del 23-oct-2026): personaje/lugar = imagen real (pegatina de
    Wowpedia, ruta a .png/.jpg) recortada a 4:5 desde arriba; objeto = 'ico:<ícono de Wowhead>' ampliado. Marco dorado, sombra
    y un giro leve, como una foto clavada en el mapa."""
    if str(fuente_img).startswith("ico:"):
        im = icono(fuente_img[4:], alto - 24).convert("RGBA")
        lienzo = Image.new("RGBA", (alto, alto), (8, 10, 26, 255))
        lienzo.alpha_composite(im, (12, 12))
        im = lienzo
    else:
        im = Image.open(fuente_img).convert("RGBA")
        w0 = int(alto * .8)
        e = max(w0 / im.width, alto / im.height)
        im = im.resize((max(w0, int(im.width * e + .5)), max(alto, int(im.height * e + .5))), Image.LANCZOS)
        x0 = (im.width - w0) // 2
        im = im.crop((x0, 0, x0 + w0, alto))
        fondo = Image.new("RGBA", im.size, (8, 10, 26, 255))
        fondo.alpha_composite(im)
        im = fondo
    w, h = im.size
    M = 22
    out = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((M + 4, M + 10, M + w + 6, M + h + 12), 12, fill=(0, 0, 0, 200))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=255)
    out.paste(im, (M, M), m)
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((M - 2, M - 2, M + w + 1, M + h + 1), 13, outline=ORO + (255,), width=5)
    d.rounded_rectangle((M + 6, M + 6, M + w - 7, M + h - 7), 8, outline=ORO + (80,), width=1)
    return out.rotate(giro, expand=True, resample=Image.BICUBIC) if giro else out


def ruta(mapa, puntos, titulo=None, sub=None, zmax=1.7, zmin=1.0, curva=.12, objeto=None, W=1920, H=1080):
    """Ruta de una cadena de misiones (o dónde cae un objeto) sobre el MAPA REAL de la zona, a cuadro entero (FX `pantalla`).
    mapa = ruta local del mapa de Wowhead Classic (zona o continente; coordenadas 0-100 como las del juego).
    puntos = [(x, y, rótulo, subrótulo|None, foto|None), ...]; el paso k aparece en la marca k y la línea punteada va del paso
    k-1 al k en los 0,9 s que siguen (un marcador brillante la recorre). La cámara encuadra los pasos ya vistos (zoom
    zmin..zmax) y se mueve suave en 1,1 s. objeto = ícono de Wowhead del premio: el ÚLTIMO paso es un medallón grande con ese
    ícono y halo que late, que se vuelve verde en la marca extra len(puntos). titulo/sub = cartela arriba a la izquierda.
    foto (regla del 23-oct-2026, TODO mapa de cualquier canal): la imagen de lo que la voz nombra en ese paso (personaje,
    lugar u objeto; `_foto`) sale junto al pin con rebote y se va cuando entra el paso siguiente (la del último se queda)."""
    import cv2
    base = _mapa(mapa, W, H, zmax)
    bh, bw = base.shape[:2]
    P = [(p[0] / 100 * bw, p[1] / 100 * bh) for p in puntos]
    rot = [_panel_rotulo(p[2], p[3] if len(p) > 3 else None) for p in puntos]
    fotos = [_foto(p[4], giro=(-4 if k % 2 else 4)) if len(p) > 4 and p[4] else None for k, p in enumerate(puntos)]
    cart = _panel_rotulo(titulo, sub) if titulo else None
    tramos = [_bezier(P[k - 1], P[k], curva * (1 if k % 2 else -1)) for k in range(1, len(P))]
    ico = icono(objeto, 112) if objeto else None
    s_min = max(W / bw, H / bh)                        # píxeles de salida por píxel de la base con el mapa entero
    yy, xx = np.mgrid[0:H, 0:W]
    r_ = np.sqrt(((xx - W / 2) / (W * .62)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2)
    vin = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8),
                                     (np.clip(r_ - .55, 0, 1) * 330).clip(0, 175).astype(np.uint8)]), "RGBA")

    def camara(vistos):
        """(cx, cy, s): centro en la base y escala que encuadra los pasos vistos sin salirse del mapa."""
        if not vistos:
            s, cx, cy = s_min * zmin, bw / 2, bh / 2
        else:
            xs, ys = [P[i][0] for i in vistos], [P[i][1] for i in vistos]
            mw, mh = (max(xs) - min(xs)) + bw * .30, (max(ys) - min(ys)) + bh * .34   # margen para rótulos
            s = max(s_min * zmin, min(s_min * zmax, W / mw, H / mh))
            cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        hw, hh = W / s / 2, H / s / 2
        return min(max(cx, hw), bw - hw), min(max(cy, hh), bh - hh), s

    def fn(dt, dur, marcas):
        tk = [_mk(marcas, i, .5 + i * 2.2) for i in range(len(P) + 1)]
        vistos = [i for i in range(len(P)) if dt >= tk[i]]
        cam = camara(vistos)
        if vistos:
            u = _eo((dt - tk[vistos[-1]]) / 1.1)
            cam = tuple(a + (b - a) * u for a, b in zip(camara(vistos[:-1]), cam))
        cx, cy, s = cam
        s *= 1 + .03 * dt / max(dur, 1)                # empuje lento: nada se queda quieto
        Mt = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
        f = cv2.warpAffine(base, Mt, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        im = Image.fromarray(np.dstack([f[..., ::-1], np.full((H, W), 255, np.uint8)]), "RGBA")
        im.alpha_composite(vin)

        def pant(p):
            return W / 2 + s * (p[0] - cx), H / 2 + s * (p[1] - cy)

        d = ImageDraw.Draw(im)
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # halos y marcador en capa aparte (ImageDraw no mezcla alfa)
        cd = ImageDraw.Draw(capa)
        for k, tr in enumerate(tramos, 1):
            if dt < tk[k]:
                continue
            u = _eo((dt - tk[k]) / .9)
            q = np.array([pant(p) for p in tr])
            L = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(q, axis=0).T))])
            lim, pos = L[-1] * u, 0.0
            while pos < lim:                           # trazos de 15 px cada 26 px
                b_ = min(pos + 15, lim)
                pa = (np.interp(pos, L, q[:, 0]), np.interp(pos, L, q[:, 1]))
                pb = (np.interp(b_, L, q[:, 0]), np.interp(b_, L, q[:, 1]))
                d.line([(pa[0] + 2, pa[1] + 3), (pb[0] + 2, pb[1] + 3)], fill=(0, 0, 0, 255), width=8)
                d.line([pa, pb], fill=ORO_T + (255,), width=6)
                pos += 26
            if u < 1:
                mx, my = np.interp(lim, L, q[:, 0]), np.interp(lim, L, q[:, 1])
                for rr, aa in ((30, 50), (20, 90), (11, 220)):
                    cd.ellipse((mx - rr, my - rr, mx + rr, my + rr), fill=(255, 230, 120, aa))
        n_obj = len(P) - 1 if ico is not None else -1
        if n_obj in vistos:                            # halo del premio
            x, y = pant(P[n_obj])
            lat = .5 + .5 * math.sin(dt * 5)
            col = VERDE if dt >= tk[len(P)] else ORO_T
            for rr, aa in ((122 + 16 * lat, 70), (98 + 8 * lat, 120)):
                cd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col + (aa,))
        im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(im)
        rotulos = []
        for i in vistos:
            x, y = pant(P[i])
            uu = dt - tk[i]
            sp = _pop(uu, .35)
            a = _eo((uu - .15) / .3)
            if i != n_obj and i + 2 < len(P) and dt > tk[i + 2]:   # quedan los 2 últimos rótulos y el del premio
                a *= 1 - _eo((dt - tk[i + 2]) / .4)
            if a > 0:
                rotulos.append((i, x, y, a))
            if i == n_obj:
                col = VERDE if dt >= tk[len(P)] else ORO
                r = 72 * sp
                d.ellipse((x - r, y - r, x + r, y + r), fill=(8, 10, 26, 255))
                _pegar(im, ico, x, y, sp)
                d = ImageDraw.Draw(im)
                d.ellipse((x - r, y - r, x + r, y + r), outline=col + (255,), width=6)
            else:
                r = 30 * sp
                d.ellipse((x - r + 3, y - r + 5, x + r + 3, y + r + 5), fill=(0, 0, 0, 255))
                d.ellipse((x - r, y - r, x + r, y + r), fill=(150, 22, 18, 255), outline=ORO_T + (255,), width=4)
                if sp > .6:
                    _texto(d, (x, y + 1), str(i + 1), fuente("negra", 30), BLANCO, "mm")
        # rótulos: del más nuevo al más viejo, cada uno en el primer hueco libre (derecha, izquierda, abajo, arriba)
        ocup = [(x - r, y - r, x + r, y + r) for i, x, y, _ in rotulos for r in [(80 if i == n_obj else 34)]]
        if cart is not None:
            ocup.append((40, 36, 60 + cart.width, 56 + cart.height))
        for i, x, y, a in sorted(rotulos, key=lambda r: (r[0] != n_obj, -r[0])):
            rl, off = rot[i], (96 if i == n_obj else 44)
            cands = [(x + off, y - rl.height / 2), (x - off - rl.width, y - rl.height / 2),
                     (x - rl.width / 2, y + off * .9), (x - rl.width / 2, y - off * .9 - rl.height)]
            mejor = None
            for rx, ry in cands:
                rx, ry = min(max(rx, 24), W - rl.width - 24), min(max(ry, 24), H - rl.height - 24)
                caja = (rx, ry, rx + rl.width, ry + rl.height)
                choque = sum(max(0, min(caja[2], o[2]) - max(caja[0], o[0])) * max(0, min(caja[3], o[3]) - max(caja[1], o[1]))
                             for o in ocup)
                if mejor is None or choque < mejor[0]:
                    mejor = (choque, caja)
                if choque == 0:
                    break
            caja = mejor[1]
            ocup.append(caja)
            _pegar(im, rl, (caja[0] + caja[2]) / 2, (caja[1] + caja[3]) / 2, 1.0, a)
        # fotos: la del paso más nuevo (y la del premio), en el hueco libre más cercano al pin; rebotan al entrar
        for i in sorted(vistos, reverse=True):
            ft = fotos[i]
            if ft is None:
                continue
            uu = dt - tk[i]
            sig = tk[i + 1] if i + 1 < len(P) else None
            a = _eo((uu - .25) / .3)
            if sig is not None and dt > sig:
                a *= 1 - _eo((dt - sig) / .35)
            if a <= 0:
                continue
            x, y = pant(P[i])
            fw, fh = ft.size
            off = 110 if i == n_obj else 60
            cands = [(x - fw / 2, y - off - fh), (x + off, y - fh / 2), (x - off - fw, y - fh / 2), (x - fw / 2, y + off),
                     (x + off, y - fh - 20), (x - off - fw, y - fh - 20), (x + off, y + 20), (x - off - fw, y + 20)]
            mejor = None
            for rx, ry in cands:
                rx, ry = min(max(rx, 20), W - fw - 20), min(max(ry, 20), H - fh - 20)
                caja = (rx, ry, rx + fw, ry + fh)
                choque = sum(max(0, min(caja[2], o[2]) - max(caja[0], o[0])) * max(0, min(caja[3], o[3]) - max(caja[1], o[1]))
                             for o in ocup)
                if mejor is None or choque < mejor[0]:
                    mejor = (choque, caja)
                if choque == 0:
                    break
            caja = mejor[1]
            ocup.append(caja)
            _pegar(im, ft, (caja[0] + caja[2]) / 2, (caja[1] + caja[3]) / 2, .55 + .45 * _pop(uu - .25, .35), a)
        if cart is not None:
            _pegar(im, cart, 50 + cart.width / 2, 46 + cart.height / 2, 1.0, _eo(dt / .4))
        return np.array(im)[..., [2, 1, 0, 3]].copy()
    return fn


#   forja(titulo, [(ícono, etiqueta, cantidad), ...], (ícono, nombre), remate)   receta de un legendario: cada ingrediente
#                                     entra en su marca y una flecha punteada lo lleva al medallón del arma, que se enciende
#                                     en naranja legendario en la marca len(ingredientes); el remate sale en verde después
#   sorteo(titulo, n, ícono_premio, etiqueta, remate)  probabilidad: n casillas que se llenan de intentos fallidos (gris) con
#                                     un contador que corre; en la marca 1 se enciende UNA en dorado y sale el premio
NARANJA = (255, 128, 0)


def forja(titulo, ingredientes, premio, remate=None, ancho=1600):
    """Receta de un legendario. marca k (k < len): entra el ingrediente k (casilla con ícono, etiqueta y «×N») y su flecha
    punteada viaja hasta el medallón · marca len: el medallón del premio estalla en naranja legendario con su nombre ·
    marca len+1: `remate` en verde debajo del nombre."""
    n = len(ingredientes)
    T, FIL = 78, 96
    h = 110 + max(n * FIL, 380) + 40
    f_et, f_n, f_nom, f_rem = fuente("sans", 30), fuente("negra", 34), fuente("serif", 40), fuente("negra", 32)

    def fn(dt, dur, marcas):
        tk = [_mk(marcas, i, .4 + i * 1.0) for i in range(n + 2)]
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, cy = M + ancho - 280, M + 90 + (h - 200) / 2
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        cd = ImageDraw.Draw(capa)
        y0 = M + 100 + (h - 140 - n * FIL) / 2
        for k, (ico, et, cant) in enumerate(ingredientes):
            u = dt - tk[k]
            x, y = M + 60, y0 + k * FIL
            _casilla(im, d, x, y, T, ico, u if u > 0 else None)
            if u <= 0:
                continue
            a = 255 * _eo(u / .3)
            _texto(d, (x + T + 22, y + T / 2), et, f_et, BLANCO, "lm", a)
            if cant:
                _texto(d, (x + T + 34 + d.textlength(et, font=f_et), y + T / 2), f"×{cant}", f_n, ORO_T, "lm", a)
            ax, ay = M + ancho * .60, y + T / 2       # flecha punteada que viaja hasta el medallón
            v = _eo((u - .2) / .7)
            if v > 0:
                bx, by = ax + (cx - 112 - ax) * v, ay + (cy - ay) * v
                L = math.hypot(bx - ax, by - ay)
                p = 0.0
                while p < L:
                    q0, q1 = p / max(L, 1), min(p + 12, L) / max(L, 1)
                    d.line([(ax + (bx - ax) * q0, ay + (by - ay) * q0), (ax + (bx - ax) * q1, ay + (by - ay) * q1)],
                           fill=ORO + (255,), width=4)
                    p += 22
                if v < 1:
                    cd.ellipse((bx - 12, by - 12, bx + 12, by + 12), fill=(255, 220, 120, 200))
        hecho = dt >= tk[n]
        lat = .5 + .5 * math.sin(dt * 5)
        if hecho:                                      # estallido naranja: halo y rayos que giran
            u = dt - tk[n]
            for r_, a_ in ((150 + 18 * lat, 70), (120 + 10 * lat, 120)):
                cd.ellipse((cx - r_, cy - r_, cx + r_, cy + r_), fill=NARANJA + (int(a_ * min(1, u / .3)),))
            for j in range(12):
                ang = j * math.pi / 6 + dt * .4
                r0, r1 = 118, 118 + 80 * _eo(u / .5)
                cd.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
                        fill=NARANJA + (150,), width=6)
        im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(8)))
        d = ImageDraw.Draw(im)
        d.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), fill=(6, 8, 22, 255))
        if hecho:
            _pegar(im, icono(premio[0], 160), cx, cy, 1.0 + .06 * _pop(dt - tk[n], .4) * lat)
        else:
            _pegar(im, icono(premio[0], 160, True), cx, cy)
        d = ImageDraw.Draw(im)
        d.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), outline=(NARANJA if hecho else GRIS) + (255,), width=7)
        if hecho:
            _texto(d, (cx, cy + 142), premio[1], f_nom, NARANJA, "mm", 255 * _eo((dt - tk[n]) / .3))
        if remate and dt >= tk[n + 1]:
            _texto(d, (cx, cy + 190), remate, f_rem, VERDE, "mm", 255 * _eo((dt - tk[n + 1]) / .3))
        return _salida(im, dt)
    return fn


def sorteo(titulo, n, ico_premio, etiqueta, remate=None, ancho=1400):
    """n casillas (rejilla ~2:1) que se llenan de gris entre la marca 0 y la 1 con el contador «etiqueta: k»; en la marca 1
    la ÚLTIMA casilla se enciende en oro y el ícono del premio sale grande encima con «1 de n»; marca 2: `remate` en verde."""
    cols = max(10, int(round(math.sqrt(n * 2))))
    filas_ = math.ceil(n / cols)
    s = max(3, min(int((ancho - 120) / cols), int(380 / filas_)))
    gw, gh = cols * s, filas_ * s
    h = 110 + gh + 120
    f_c, f_g = fuente("negra", 40), fuente("negra", 64)
    ico = icono(ico_premio, 150)
    idx = np.arange(n)
    rr, cc = idx // cols, idx % cols
    m = 1 if s > 3 else 0
    ys, xs = np.meshgrid(np.arange(gh), np.arange(gw), indexing="ij")
    vacia = ((ys % s) >= m) & ((ys % s) < s - m) & ((xs % s) >= m) & ((xs % s) < s - m) & ((ys // s) * cols + xs // s < n)
    ys, xs = np.nonzero(vacia)

    def fn(dt, dur, marcas):
        t0, t1, t2 = _mk(marcas, 0, .4), _mk(marcas, 1, 4.0), _mk(marcas, 2, 6.0)
        im, M = _base(ancho, h, titulo)
        x0, y0 = M + (ancho - gw) / 2, M + 100
        u = max(0.0, min(1.0, (dt - t0) / max(t1 - t0 - .2, .5)))
        k = int((n - 1) * u ** 1.6)                   # acelera
        g = np.zeros((gh, gw, 4), np.uint8)
        g[..., :3] = (10, 13, 34)
        g[..., 3] = 255
        g[ys, xs, :3] = (44, 54, 104)                  # casillas vacías visibles (intentos por venir)
        for i_, j_ in zip(rr[:k], cc[:k]):
            g[i_ * s + m:(i_ + 1) * s - m, j_ * s + m:(j_ + 1) * s - m, :3] = (118, 118, 132)
        if dt >= t1:
            g[rr[-1] * s:(rr[-1] + 1) * s, cc[-1] * s:(cc[-1] + 1) * s, :3] = ORO_T
        im.alpha_composite(Image.fromarray(g, "RGBA"), (int(x0), int(y0)))
        d = ImageDraw.Draw(im)
        cuenta = n if dt >= t1 else k
        if not (remate and dt >= t2):
            _texto(d, (M + ancho / 2, y0 + gh + 52), f"{etiqueta}: {cuenta:,}".replace(",", " "), f_c, BLANCO, "mm")
        if dt >= t1:                                  # el premio sale grande sobre la rejilla
            v = dt - t1
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            cx, cy = M + ancho / 2, y0 + gh / 2 - 30
            ImageDraw.Draw(capa).ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=ORO_T + (int(110 * min(1, v / .3)),))
            im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(20)))
            sp = _pop(v, .4)
            d = ImageDraw.Draw(im)
            r = 92 * sp
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(6, 8, 22, 255), outline=ORO_T + (255,), width=6)
            _pegar(im, ico, cx, cy, sp)
            d = ImageDraw.Draw(im)
            _texto(d, (cx, cy + 140), f"1 de {n:,}".replace(",", " "), f_g, ORO_T, "mm", 255 * _eo(v / .3))
        if remate and dt >= t2:
            _texto(d, (M + ancho / 2, y0 + gh + 52), remate, f_c, VERDE, "mm", 255 * _eo((dt - t2) / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ MG nuevos de `wow_100_curiosidades_tbc_wotlk` (24-oct-2026)
#   paradero(titulo, [(img, nombre, lugar|None), ...], sello)   ¿dónde está cada uno? medallones en fila; los que no están, en
#                                                               gris con un «?» que late y «sin rastro», y un sello rojo encima
#   simon(titulo, sello)                                        el juego de 4 luces de colores (las reliquias apexis de Ogri'la):
#                                                               secuencias que crecen en bucle y el fallo con rayos
#   franquicia(retrato, titulo, [(lugar, sub), ...], sello)     un personaje con «sucursales»: letreros de neón que prenden
#                                                               parpadeando, unidos a su retrato, y el contador que sube
def paradero(titulo, personas, sello=None, ancho=1640):
    """¿Dónde está cada uno? (c100: los 5 héroes de la expedición de los Hijos de Lothar). personas = [(img, nombre, lugar),
    ...]: la persona k sale en la marca k (medallón con rebote; antes, su hueco vacío) con el nombre y debajo DÓNDE está, en oro;
    lugar None = medallón gris, «?» que late encima y «sin rastro» en rojo. sello = (texto, i_marca): sello rojo sobre los que
    faltan."""
    R, n = 88, len(personas)
    h = 96 + 2 * R + 150

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        paso = (ancho - 2 * 175) / max(1, n - 1)
        cy = M + 100 + R
        faltan = []
        for k, (ruta, nom, lugar) in enumerate(personas):
            tk = _mk(marcas, k, .4 + k * 1.0)
            cx = M + 175 + k * paso
            if dt < tk:                                # hueco que espera a su héroe
                lat = .5 + .5 * math.sin(dt * 3 + k)
                d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(4, 6, 18, 200), outline=ORO + (int(60 + 60 * lat),), width=3)
                continue
            u = dt - tk
            gris = lugar is None
            _pegar(im, _medallon(ruta, R, gris), cx, cy, _pop(u))
            d = ImageDraw.Draw(im)
            a = 255 * _eo(u / .3)
            _texto(d, (cx, cy + R + 36), nom, fuente("sans", 28), BLANCO, "mm", a)
            if gris:
                faltan.append(cx)
                _texto(d, (cx, cy + 4), "?", fuente("serif", 120), ORO_T, "mm", a * (.55 + .45 * math.sin(dt * 4 + k)))
                _texto(d, (cx, cy + R + 74), "sin rastro", fuente("sans", 25), ROJO, "mm", a)
            else:
                d.ellipse((cx - 7, cy + R + 66, cx + 7, cy + R + 80), fill=ORO_T + (int(a),))
                _texto(d, (cx + 16, cy + R + 74), lugar, fuente("sans", 25), ORO_T, "lm", a)
        if sello and len(marcas) > sello[1] and faltan:
            _sello(im, sello[0], sum(faltan) / len(faltan), cy - 6, dt - marcas[sello[1]], ROJO, 40)
        return _salida(im, dt)
    return fn


_SIMON = [(40, 200, 70), (225, 40, 40), (240, 200, 30), (40, 110, 235)]   # verde, rojo, amarillo, azul (como el juego)
_SEC = [1, 3, 0, 2, 3, 1, 2, 0]


def simon(titulo, sello="TE ELECTROCUTA", ancho=980):
    """El juego de luces de colores (c073: las reliquias apexis de Ogri'la, «exactamente un Simon»). Disco partido en 4 luces
    (verde, rojo, amarillo, azul) con un núcleo de cristal apexis. marca 0: las luces aparecen apagadas, una a una · 1: la
    secuencia: se encienden en orden con halo, cada ronda una más larga (1, 2, 3, 4...), en bucle · 2: el fallo: la luz
    equivocada parpadea en blanco, rayos que saltan del núcleo al borde y cae el sello rojo."""
    Ro, Ri, gap = 236, 84, 14
    h = 96 + 2 * Ro + 70

    def _lit(dt, t1, t2):
        """Índice de la luz encendida ahora en la secuencia (None = ninguna)."""
        if dt < t1 or dt >= t2:
            return None
        u, ronda = dt - t1, 1
        while True:
            largo = ronda * .55 + .55
            if u < largo:
                i = int(u / .55)
                return _SEC[i % len(_SEC)] if i < ronda and (u - i * .55) < .42 else None
            u -= largo
            ronda = ronda % 4 + 1

    def fn(dt, dur, marcas):
        t0, t1, t2 = _mk(marcas, 0, .3), _mk(marcas, 1, 1.6), _mk(marcas, 2, 99.0)
        im, M = _base(ancho, h, titulo)
        cx, cy = M + ancho / 2, M + 96 + Ro + 6
        lit, fallo = _lit(dt, t1, t2), dt >= t2
        mal = 2                                       # la luz que el jugador toca mal
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh, dc = ImageDraw.Draw(halo), ImageDraw.Draw(capa)
        for q, col in enumerate(_SIMON):
            tq = t0 + q * .14
            if dt < tq:
                continue
            s = _pop(dt - tq, .3)
            r = Ro * s
            on = lit == q or (fallo and q == mal and int((dt - t2) * 10) % 2 == 0)
            c = (255, 255, 255) if (fallo and q == mal and on) else (col if on else tuple(int(v * .32) for v in col))
            a0 = {0: 180, 1: 270, 2: 90, 3: 0}[q]    # 0 arriba-izq, 1 arriba-der, 2 abajo-izq, 3 abajo-der
            dc.pieslice((cx - r, cy - r, cx + r, cy + r), a0, a0 + 90, fill=c + (255,))
            if on:
                for k in range(3, 0, -1):
                    rr = Ro + 18 * k
                    dh.pieslice((cx - rr, cy - rr, cx + rr, cy + rr), a0, a0 + 90, fill=c + (int(50 + 20 * (3 - k)),))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(16)))
        dc.rectangle((cx - gap / 2, cy - Ro - 4, cx + gap / 2, cy + Ro + 4), fill=(0, 0, 0, 0))   # cruz que separa las luces
        dc.rectangle((cx - Ro - 4, cy - gap / 2, cx + Ro + 4, cy + gap / 2), fill=(0, 0, 0, 0))
        im.alpha_composite(capa)
        d = ImageDraw.Draw(im)
        if dt >= t0:                                   # núcleo de cristal apexis
            s = _pop(dt - t0, .35)
            r = Ri * s
            lat = .5 + .5 * math.sin(dt * 5)
            d.ellipse((cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fill=(4, 6, 18, 255), outline=ORO + (255,), width=5)
            d.ellipse((cx - r * .62, cy - r * .62, cx + r * .62, cy + r * .62), fill=(int(70 + 60 * lat), int(150 + 60 * lat), 255, 255))
            d.polygon([(cx, cy - r * .5), (cx + r * .3, cy), (cx, cy + r * .5), (cx - r * .3, cy)], fill=(235, 250, 255, 255))
        if fallo:                                      # rayos que saltan del núcleo al borde
            rng = np.random.default_rng(int(dt * 14))
            ray = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dr = ImageDraw.Draw(ray)
            for _ in range(5):
                ang = rng.uniform(0, 2 * math.pi)
                pts = [(cx + Ri * math.cos(ang), cy + Ri * math.sin(ang))]
                for j in range(1, 7):
                    rr = Ri + (Ro + 30 - Ri) * j / 6
                    aj = ang + rng.uniform(-.18, .18)
                    pts.append((cx + rr * math.cos(aj), cy + rr * math.sin(aj)))
                dr.line(pts, fill=(150, 210, 255, 200), width=12)
                dr.line(pts, fill=(255, 255, 255, 255), width=4)
            im.alpha_composite(ray.filter(ImageFilter.GaussianBlur(1)))
            _sello(im, sello, cx, cy + Ro - 30, dt - t2 - .25, ROJO, 46, ang=-7)
        return _salida(im, dt)
    return fn


def franquicia(retrato, titulo, sedes, sello=None, ancho=1500):
    """Un personaje que vuelve con negocio propio en otras zonas (c079: Gurgthock, del pozo de Nagrand al Anfiteatro de la
    Angustia y más allá). retrato = ruta de su imagen real (medallón a la izquierda); sedes = [(lugar, sub), ...]: la sede k
    se enciende en la marca k como un letrero de neón que parpadea al prender, unido al retrato por una línea dorada; la 1.ª
    es la MATRIZ (oro) y las demás sucursales (cian), con el contador de sucursales bajo el retrato. sello = (texto, i_marca)
    en verde."""
    R, AL, G = 124, 78, 16
    n = len(sedes)
    h = 96 + n * (AL + G) + 30 + (70 if sello else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        mx, my = M + 200, M + 96 + n * (AL + G) / 2
        t0 = _mk(marcas, 0, .3)
        if dt >= t0 - .25:
            _pegar(im, _medallon(retrato, R), mx, my - 20, _pop(dt - t0 + .25))
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(halo)
        d = ImageDraw.Draw(im)
        x0, x1 = M + 420, M + ancho - 50
        encendidas = 0
        for k, (lugar, sub) in enumerate(sedes):
            tk = _mk(marcas, k, .4 + k * 1.3)
            y = M + 96 + k * (AL + G)
            if dt < tk:
                d.rounded_rectangle((x0, y, x1, y + AL), 12, fill=(4, 6, 18, 160), outline=(60, 60, 80, 200), width=2)
                continue
            u = dt - tk
            encendidas += 1
            on = u > .55 or int(u * 18) % 3 != 1        # parpadeo del neón al prender
            col = ORO_T if k == 0 else CIAN
            ya = y + AL / 2                            # línea retrato -> letrero
            xe = mx + R + 14 + (x0 - 18 - mx - R - 14) * _eo(u / .35)
            d.line([(mx + R + 14, my - 20), ((mx + R + x0) / 2, my - 20), ((mx + R + x0) / 2, ya), (xe, ya)],
                   fill=col + (200,), width=4)
            d.rounded_rectangle((x0, y, x1, y + AL), 12, fill=(8, 10, 28, 245),
                                outline=col + ((255,) if on else (70,)), width=4)
            if on:
                dh.rounded_rectangle((x0 - 6, y - 6, x1 + 6, y + AL + 6), 16, outline=col + (150,), width=10)
            a = 255 if on else 90
            _texto(d, (x0 + 28, ya), lugar, fuente("serif", 36), col, "lm", a)
            tag = "MATRIZ" if k == 0 else f"SUCURSAL {k}"
            _texto(d, (x1 - 26, ya - 14), tag, fuente("negra", 22), BLANCO, "rm", a)
            _texto(d, (x1 - 26, ya + 16), sub, fuente("sans", 22), GRIS if not on else BLANCO, "rm", a)
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(9)))
        d = ImageDraw.Draw(im)
        if dt >= t0:
            suc = max(0, encendidas - 1)
            _texto(d, (mx, my + R + 10), "SUCURSALES", fuente("sans", 24), GRIS, "mm")
            _texto(d, (mx, my + R + 52), str(suc), fuente("serif", 58), VERDE if suc == n - 1 and n > 1 else ORO_T, "mm")
        if sello and len(marcas) > sello[1]:
            _sello(im, sello[0], (x0 + x1) / 2, M + h - 52, dt - marcas[sello[1]], VERDE, 34, ang=-4)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ MG nuevos de Rasganorte (26-oct-2026, mismo video)
#   altares(titulo, [(img, nombre, sub, viva), ...], sello)     dioses sobre sus altares-zigurat: los sacrificados reciben un
#                                                               tajo rojo y se vuelven grises; la que sigue viva, encadenada
#   apariciones(retrato, titulo, [(lugar, sub), ...], actual, sello)   un personaje que sale en cada expansión: su medallón
#                                                               viaja por una vía de paradas que se encienden; «ESTÁS AQUÍ»
def _zigurat(d, cx, y0):
    """Altar escalonado de piedra trol (3 escalones): arriba en y0, base en y0 + 78."""
    for k, w in enumerate((140, 180, 220)):
        y = y0 + k * 26
        d.rectangle((cx - w / 2, y, cx + w / 2, y + 26), fill=(70, 104, 112, 255), outline=(28, 40, 46, 255), width=2)
        d.line([(cx - w / 2 + 4, y + 3), (cx + w / 2 - 4, y + 3)], fill=(150, 185, 190, 120), width=2)


def _eslabones(d, a, b, t=1.0):
    """Cadena de eslabones de hierro de a a b (t = fracción ya dibujada)."""
    n = 11
    for i in range(int(n * max(0.0, min(1.0, t)))):
        q = (i + .5) / n
        x, y = a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q
        rx, ry = (6, 11) if i % 2 else (11, 6)
        d.ellipse((x - rx, y - ry, x + rx, y + ry), outline=(30, 30, 34, 255), width=6)
        d.ellipse((x - rx, y - ry, x + rx, y + ry), outline=(185, 190, 200, 255), width=3)


def altares(titulo, dioses, sello=None, ancho=1640):
    """Los dioses que un pueblo sacrificó (c030: los Drakkari de Zul'Drak se bebieron a sus dioses). dioses = [(img, nombre,
    sub, viva), ...]: el dios k aparece sobre su altar en la marca k; si no está vivo, 0,45 s después un tajo rojo lo cruza,
    se vuelve gris y sale «SACRIFICADO»; viva=True = cadenas que lo atan al altar, halo verde que late y «VIVA · ENCADENADA».
    sello = (texto, i_marca) rojo sobre la fila."""
    R, n = 80, len(dioses)
    h = 96 + 2 * R + 24 + 78 + 112 + (70 if sello else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        paso = (ancho - 2 * 170) / max(1, n - 1)
        cy = M + 96 + R + 6
        ya = cy + R + 18                              # cima del altar
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(halo)
        for k, (_r, _n, _s, viva) in enumerate(dioses):   # halo verde DETRÁS del medallón de la que sigue viva
            tk = _mk(marcas, k, .4 + k * 1.1)
            if viva and dt >= tk:
                lat = .5 + .5 * math.sin(dt * 4)
                cx = M + 170 + k * paso
                dh.ellipse((cx - R - 24, cy - R - 24, cx + R + 24, cy + R + 24),
                           fill=VERDE + (int((70 + 80 * lat) * min(1, dt - tk)),))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(im)
        for k in range(n):
            _zigurat(d, M + 170 + k * paso, ya)
        tajos = []
        for k, (ruta, nom, sub, viva) in enumerate(dioses):
            tk = _mk(marcas, k, .4 + k * 1.1)
            cx = M + 170 + k * paso
            if dt < tk:                                # altar vacío que espera
                lat = .5 + .5 * math.sin(dt * 3 + k)
                d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(4, 6, 18, 180), outline=ORO + (int(50 + 50 * lat),), width=3)
                continue
            u = dt - tk
            s = _pop(u)
            if viva:
                _pegar(im, _medallon(ruta, R), cx, cy, s)
            else:
                q = _eo((u - .55) / .4)                # de color a gris tras el tajo
                _pegar(im, _medallon(ruta, R), cx, cy, s)
                if q > 0:
                    _pegar(im, _medallon(ruta, R, gris=True), cx, cy, s, q)
                if u > .45:
                    tajos.append((cx, cy, _eo((u - .45) / .22)))
            d = ImageDraw.Draw(im)
            a = 255 * _eo(u / .3)
            _texto(d, (cx, ya + 78 + 28), nom, fuente("sans", 28), BLANCO, "mm", a)
            if sub:
                _texto(d, (cx, ya + 78 + 60), sub, fuente("sans", 21), ORO_T, "mm", a)
            if viva and u > .35:
                tc = _eo((u - .35) / .5)
                _eslabones(d, (cx - 110, ya + 40), (cx - R * .55, cy + R * .2), tc)
                _eslabones(d, (cx + 110, ya + 40), (cx + R * .55, cy + R * .2), tc)
                _texto(d, (cx, ya + 78 + 92), "VIVA · ENCADENADA", fuente("negra", 21), VERDE, "mm", 255 * tc)
            elif not viva and u > .6:
                _texto(d, (cx, ya + 78 + 92), "SACRIFICADO", fuente("negra", 21), ROJO, "mm", 255 * _eo((u - .6) / .3))
        if tajos:                                      # tajo rojo en diagonal, con brillo
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            lineas = []
            for cx, cy_, t in tajos:
                a, b = (cx - R * .9, cy_ - R * .9), (cx + R * .9, cy_ + R * .9)
                lineas.append((a, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)))
            for a, e in lineas:
                dc.line([a, e], fill=ROJO + (170,), width=22)
            im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(6)))
            d = ImageDraw.Draw(im)
            for a, e in lineas:
                d.line([a, e], fill=(255, 235, 230, 255), width=5)
        if sello and len(marcas) > sello[1]:
            _sello(im, sello[0], M + ancho / 2, M + h - 34, dt - marcas[sello[1]], ROJO, 38, ang=-2)
        return _salida(im, dt)
    return fn


def apariciones(retrato, titulo, paradas, actual=None, sello=None, ancho=1640):
    """Un personaje que reaparece en cada expansión (c031: Harrison Jones, de Zul'Aman a Draenor). paradas = [(lugar, sub),
    ...] sobre una vía horizontal: la parada k se enciende en la marca k y el medallón (retrato) viaja hasta ella con una
    estela; la parada `actual` va en cian con «ESTÁS AQUÍ» que late. sello = (texto, i_marca) en verde."""
    R, n = 74, len(paradas)
    h = 96 + 2 * R + 40 + 150 + (90 if sello else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        x0, x1 = M + 190, M + ancho - 190
        paso = (x1 - x0) / max(1, n - 1)
        yv = M + 96 + 2 * R + 40                       # la vía
        d = ImageDraw.Draw(im)
        d.line([(x0 - 60, yv), (x1 + 60, yv)], fill=(60, 64, 90, 255), width=6)
        prendidas = [k for k in range(n) if dt >= _mk(marcas, k, .4 + k * 1.4)]
        if prendidas:                                  # tramo de vía ya recorrido, en oro
            d.line([(x0, yv), (x0 + prendidas[-1] * paso, yv)], fill=ORO_T + (255,), width=6)
        for k, (lugar, sub) in enumerate(paradas):
            tk = _mk(marcas, k, .4 + k * 1.4)
            cx = x0 + k * paso
            if dt < tk:
                d.ellipse((cx - 16, yv - 16, cx + 16, yv + 16), fill=(4, 6, 18, 255), outline=(90, 90, 110, 255), width=3)
                continue
            u = dt - tk
            r = 18 * max(.2, _pop(u))
            col = CIAN if k == actual else ORO_T
            d.ellipse((cx - r, yv - r, cx + r, yv + r), fill=col + (255,), outline=(20, 20, 30, 255), width=3)
            a = 255 * _eo(u / .3)
            _texto(d, (cx, yv + 50), lugar, fuente("serif", 30), col, "mm", a)
            if sub:
                _texto(d, (cx, yv + 88), sub, fuente("sans", 22), BLANCO, "mm", a)
            if k == actual:
                lat = .55 + .45 * math.sin(dt * 5)
                _texto(d, (cx, yv + 124), "ESTÁS AQUÍ", fuente("negra", 22), CIAN, "mm", a * lat)
        if prendidas:                                  # el medallón viaja de la parada anterior a la última encendida
            k = prendidas[-1]
            tk = _mk(marcas, k, .4 + k * 1.4)
            q = _eo((dt - tk) / .8) if k else 1.0
            xa = x0 + (k - 1) * paso if k else x0
            mx = xa + (x0 + k * paso - xa) * q
            my = M + 96 + R
            if 0 < q < 1:                              # estela
                for j in range(1, 6):
                    _pegar(im, _medallon(retrato, R), mx - j * 26, my, .9, .14 * (6 - j) / 5)
            _pegar(im, _medallon(retrato, R), mx, my, _pop(dt - _mk(marcas, 0, .4)))
            d = ImageDraw.Draw(im)
            d.line([(mx, my + R + 8), (mx, yv - 20)], fill=ORO + (180,), width=3)
        if sello and len(marcas) > sello[1]:
            _sello(im, sello[0], M + ancho / 2, M + h - 46, dt - marcas[sello[1]], VERDE, 34, ang=-3)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ 27-oct-2026, `wow_jugadores_rompieron` (jugadores reales)
def _barra_vida(d, x, y, w, h, q, color=(40, 200, 60)):
    """Barra de vida de placa de nombre del juego: marco negro, relleno q (0..1) con brillo arriba."""
    d.rounded_rectangle((x - 3, y - 3, x + w + 3, y + h + 3), 6, fill=(0, 0, 0, 255), outline=ORO + (255,), width=2)
    d.rounded_rectangle((x, y, x + w, y + h), 4, fill=(30, 8, 8, 255))
    q = max(0.0, min(1.0, q))
    if w * q >= 10:                                    # más angosta no cabe el redondeo (PIL exige x1 >= x0)
        d.rounded_rectangle((x, y, x + w * q, y + h), 4, fill=color + (255,))
        d.rectangle((x + 3, y + 3, x + w * q - 3, y + h * .38), fill=tuple(min(255, c + 70) for c in color) + (255,))


def reckoning(titulo, ico_buff, rotulo_buff, cargas, retrato, jefe, sub_jefe, sello, tope=4, ancho=1560):
    """Un talento sin tope que revienta a un jefe (c02: la bomba de Reckoning de Karmerr contra Lord Kazzak).
    marca 0: el ícono del beneficio y su contador empiezan a subir · 1: el contador llega a `cargas` (blanco, late) ·
    2: entra el jefe (medallón + nombre + barra llena) · 3: una lluvia de íconos del beneficio cruza al jefe, la barra cae a
    cero, el medallón se apaga y se tacha · 4: `sello` rojo y el contador se desploma a `tope` en rojo (el parche)."""
    T, R, h = 132, 92, 420

    def fn(dt, dur, marcas):
        t = [_mk(marcas, i, .4 + i * 1.8) for i in range(5)]
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        bx, by = M + 70, M + 120
        if dt >= t[0]:                                  # beneficio y contador
            u = dt - t[0]
            _casilla(im, d, bx, by, T, ico_buff, u)
            _texto(d, (bx + T / 2, by + T + 36), rotulo_buff, fuente("sans", 28), BLANCO, "mm", 255 * _eo(u / .3))
            if dt < t[4]:
                q = min(1.0, (dt - t[0]) / max(.3, t[1] - t[0]))
                v = int(round(cargas * (q ** 1.8)))
                lleno = q >= 1
                lat = (.85 + .15 * math.sin(dt * 9)) if lleno else 1.0
                f = fuente("serif", int(96 * lat) if lleno else 84)
                _texto(d, (bx + T + 50, by + T / 2), f"{v:,}".replace(",", " "), f, BLANCO if lleno else ORO_T, "lm")
            else:
                u4 = dt - t[4]
                v = tope if u4 > .45 else int(cargas - (cargas - tope) * _eo(u4 / .45))
                _texto(d, (bx + T + 50, by + T / 2), f"{v:,}".replace(",", " "), fuente("serif", 96), ROJO, "lm")
        jx, jy = M + ancho - 460, M + 120 + T / 2
        q_vida = 1.0
        if dt >= t[3]:
            q_vida = 1 - _eo((dt - t[3] - .35) / .8)
        if dt >= t[2]:                                  # el jefe
            u = dt - t[2]
            muerto = dt >= t[3] + 1.15
            _pegar(im, _medallon(retrato, R, gris=muerto), jx, jy, _pop(u))
            d = ImageDraw.Draw(im)
            a = 255 * _eo(u / .3)
            _texto(d, (jx + R + 30, jy - 52), jefe, fuente("serif", 40), ROJO if not muerto else GRIS, "lm", a)
            _texto(d, (jx + R + 30, jy - 12), sub_jefe, fuente("sans", 24), ORO_T, "lm", a)
            if a > 0:
                _barra_vida(d, jx + R + 30, jy + 22, 300, 30, q_vida)
            if muerto:
                k = R * .8 * _eo((dt - t[3] - 1.15) / .3)
                d.line([(jx - k, jy - k), (jx + k, jy + k)], fill=ROJO + (255,), width=12)
                d.line([(jx + k, jy - k), (jx - k, jy + k)], fill=ROJO + (255,), width=12)
        if t[3] <= dt < t[3] + 1.4:                     # la descarga: íconos que vuelan del beneficio al jefe
            mini = icono(ico_buff, 40)
            for i in range(36):
                s0 = t[3] + i * .028
                u = (dt - s0) / .45
                if 0 <= u <= 1:
                    x = bx + T + (jx - R - bx - T) * _eo(u)
                    y = by + T / 2 + math.sin(i * 2.7) * 70 * (1 - u)
                    _pegar(im, mini, x, y, 1.0, 1 - .4 * u)
            d = ImageDraw.Draw(im)
            fl = max(0.0, 1 - abs(dt - t[3] - .6) / .5)
            if fl > 0:                                  # destello en el jefe (capa aparte: ImageDraw no mezcla alfa)
                capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(capa).ellipse((jx - R * 1.6, jy - R * 1.6, jx + R * 1.6, jy + R * 1.6),
                                             fill=(255, 230, 150, int(170 * fl)))
                im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(18)))
        if dt >= t[4]:
            _sello(im, sello, M + ancho / 2, M + h - 52, dt - t[4], ROJO, 40, ang=-3)
        return _salida(im, dt)
    return fn


def inmortal(retrato, jefe, sub_jefe, titulo, sello, retiro=None, ancho=1400):
    """Un jefe que se cura con cada muerte (c04: Lord Kazzak arrastrado a Ventormenta).
    marca 0: placa del jefe con la barra llena · 1: empieza la pelea: la barra baja a golpes y cada calavera que cae debajo
    (un jugador muerto) la rellena con un destello verde; nunca baja de ~60 % · 2: `sello` rojo · 3 (si hay `retiro` =
    (ruta_imagen, texto)): entra el maestro de juego y el jefe se desvanece."""
    R, h = 96, 400
    calav = "inv_misc_bone_humanskull_01"

    def fn(dt, dur, marcas):
        t = [_mk(marcas, i, .4 + i * 2.0) for i in range(4)]
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        jx, jy = M + 170, M + 110 + R
        sale = _eo((dt - t[3] - .6) / .8) if retiro and dt >= t[3] else 0.0
        if dt >= t[0]:
            u = dt - t[0]
            _pegar(im, _medallon(retrato, R), jx, jy, _pop(u), 1 - sale)
            d = ImageDraw.Draw(im)
            a = 255 * _eo(u / .3) * (1 - sale)
            _texto(d, (jx + R + 34, jy - 64), jefe, fuente("serif", 42), ROJO, "lm", a)
            _texto(d, (jx + R + 34, jy - 22), sub_jefe, fuente("sans", 25), ORO_T, "lm", a)
            q, curas = 1.0, []
            if dt >= t[1]:                              # pelea: baja 0,22/s y cada calavera (cada 0,55 s) devuelve 0,14
                v = dt - t[1]
                n = int(v / .55)
                q = max(.6, min(1.0, 1.0 - .22 * v + .14 * n))
                curas = [t[1] + (k + 1) * .55 for k in range(n)]
            if a > 0:
                _barra_vida(d, jx + R + 34, jy + 14, 560, 34, q)
            for k, tc in enumerate(curas[-14:]):        # fila de calaveras que crece (se queda con las 14 últimas)
                _pegar(im, icono(calav, 34), jx + R + 56 + k * 40, jy + 90, _pop(dt - tc, .25), 1 - sale)
            d = ImageDraw.Draw(im)
            if curas and dt - curas[-1] < .35 and sale < 1:   # destello verde de la cura
                fl = 1 - (dt - curas[-1]) / .35
                d.rounded_rectangle((jx + R + 31, jy + 11, jx + R + 597, jy + 51), 6, outline=VERDE + (int(255 * fl),), width=4)
                _texto(d, (jx + R + 614, jy + 31), "+", fuente("negra", 44), VERDE, "lm", 255 * fl)
        if dt >= t[2]:
            _sello(im, sello, M + ancho - 230, M + 92, dt - t[2], ROJO, 42, ang=-7)
        if retiro and dt >= t[3]:
            u = dt - t[3]
            _pegar(im, _medallon(retiro[0], 70), M + ancho - 170, M + h - 120, _pop(u))
            d = ImageDraw.Draw(im)
            _texto(d, (M + ancho - 270, M + h - 120), retiro[1], fuente("sans", 28), CIAN, "rm", 255 * _eo(u / .3))
        return _salida(im, dt)
    return fn


def expediente(titulo, entradas, veredicto, ancho=1500):
    """Un caso judicial que se va escribiendo (c01: Blizzard contra Glider). entradas = [(año, texto, color|None), ...]: la
    entrada k entra en la marca k (el año cae con un golpe de mazo dorado y el texto se teclea a 0,025 s por letra);
    ROJO para las sanciones. veredicto = (texto, i_marca): sello rojo grande cruzado sobre el expediente."""
    fila = 64
    h = 110 + len(entradas) * fila + 40

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, y0 = M + 60, M + 104
        d.line([(x0 + 150, y0 - 10), (x0 + 150, y0 + len(entradas) * fila - 14)], fill=ORO + (120,), width=3)
        for k, (anio, texto, color) in enumerate(entradas):
            tk = _mk(marcas, k, .4 + k * 1.2)
            if dt < tk:
                continue
            u = dt - tk
            y = y0 + k * fila + fila / 2 - 14
            s = 1.5 - .5 * _pop(u, .25)
            _texto(d, (x0 + 120, y), anio, fuente("serif", max(8, int(40 * s))), ORO_T, "rm")
            d.ellipse((x0 + 141, y - 9, x0 + 159, y + 9), fill=(color or ORO_T) + (255,))
            _texto(d, (x0 + 186, y), texto[:int(u / .025)], fuente("sans", 32), color or BLANCO, "lm")
            if u < .3:                                  # golpe del mazo: destello dorado en la línea
                capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
                rr = 20 + 60 * u
                ImageDraw.Draw(capa).ellipse((x0 + 150 - rr, y - rr, x0 + 150 + rr, y + rr), fill=ORO_T + (int(200 * (1 - u / .3)),))
                im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(8)))
                d = ImageDraw.Draw(im)
        if veredicto and len(marcas) > veredicto[1]:
            _sello(im, veredicto[0], M + ancho / 2 + 60, M + h / 2 + 30, dt - marcas[veredicto[1]], ROJO, 46, ang=-8)
        return _salida(im, dt)
    return fn
