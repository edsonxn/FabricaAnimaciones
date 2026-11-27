# -*- coding: utf-8 -*-
"""MOTION GRAPHICS de ECONOMÍA con la interfaz de WoW (panel azul noche y borde dorado de mg_wow), hechos para
«30 trucos para NUNCA quedarte sin ORO en WoW Forever» (wow_oro_forever, 15-nov-2026). Sirven a cualquier video de oro/precios.
CERO cifras inventadas: solo números que el guion dice. Uso en efectos.py igual que mg_wow (fn(dt, dur, marcas)).
  factura(titulo, [(ícono, concepto, oro), ...], total_txt, sello)   ticket que se imprime línea a línea y suma el total
  desplome(titulo, [(fecha, precio_en_platas), ...], remate)          gráfica de un precio que cae punto a punto
  balanza(titulo, (ícono, nombre), izq, der, remate)                 vendedor vs subasta: la balanza se inclina al más caro
  escalera(titulo, peldaños, plano, remate)                          costes que suben (reespecializar) contra un pago único
  techo(titulo, ícono, nombre, precios, tope, remate)                 barra de precio que sube y choca contra un techo fijo
  dia_noche(titulo, ícono, noche, dia, remate)                        el mismo objeto, precio de noche contra precio de mañana
Añadidos el 26-nov-2026 para «15 FARMEOS de ORO del 30 al 50» (wow_oro_30_50). Precios con monedas dibujadas: «1o 30p»,
«14p», «1p 12c», «13-14o/h» (número + o/p/c pegado; lo demás es texto). img = ruta de pegatina/cara o ícono de Wowhead.
  cuenta(titulo, terminos, total, op, bolsa, remate)    suma o producto con ranuras: «montura 100 + doble esp. 50 = 150»
  cronometro(titulo, ico, minutos, total, objetos, hora) cronómetro que barre N minutos mientras el oro sube; luego «por hora»
  etiquetas(titulo, ico, nombre, izq, der, sello, nota) dos etiquetas de precio colgadas (vendedor / subasta) y sello al ganador
  probabilidad(titulo, cara, ico, n, aciertos, rotulo)  n criaturas que caen una a una; en `aciertos` salta el objeto («4 de 10»)
  encoge(titulo, ico, nombre, de, a, lapso, dias)       un precio que se encoge día a día («de 1 oro a 15 platas en una semana»)
  tope(titulo, ico, n, rotulo, candado, remate)         n ranuras que se llenan y la n+1 con candado (tope de mazmorras)
  tabla_oro(titulo, filas, nueva, nota)                 tabla de oro por hora que CRECE a lo largo del video (fila nueva)
  ficha_farmeo(n, nombre, cara, nivel, zona, objetos, oro, venta)  FICHA DEL FARMEO de la pausa «post» de cada puesto
  puesto(n, nombre, img, zona, rangos)                  tarjeta de capítulo «N.º n» con barra de nivel 30-50 y su tramo
  reparto(titulo, total, partes, remate)                barra de un total que se parte («6 mollejas = la mitad del oro»)
  columnas(titulo, ico, barras, remate)                 rejillas de íconos que se llenan lado a lado («15 contra 40 valijas»)
Prueba: python nucleo/mg_oro.py nuevos → %TEMP%/_mg_oro_nuevos_N.jpg (cuadro final de cada uno; MÍRALOS).
"""
import math

from PIL import ImageDraw

from mg_wow import (BLANCO, GRIS, ORO, ORO_T, ROJO, VERDE, _base, _eo, _mk, _pegar, _pop, _salida, _sello, _texto,
                    fuente, icono)


def _moneda(oro=0, plata=0, cobre=0):
    """Texto de precio al estilo del juego: «2 o 70 p»."""
    p = []
    if oro:
        p.append(f"{oro} o")
    if plata:
        p.append(f"{plata} p")
    if cobre or not p:
        p.append(f"{cobre} c")
    return " ".join(p)


def _ptxt(platas):
    """Platas (float) -> texto de moneda."""
    o, resto = divmod(int(round(platas * 100)), 10000)
    p, c = divmod(resto, 100)
    return _moneda(o, p, c)


def factura(titulo, lineas, total_txt="TOTAL", sello=None, ancho=1240):
    """Marca k: entra la línea k (ícono, concepto, cifra que corre); marca len: TOTAL que suma; marca len+1: sello."""
    fila = 70
    h = 170 + len(lineas) * fila + 110

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, x1, y0 = M + 60, M + ancho - 60, M + 120
        acum = 0.0
        for k, (ic, txt, val) in enumerate(lineas):
            tk = _mk(marcas, k, .4 + k * .8)
            if dt < tk:
                continue
            u, y = dt - tk, y0 + k * fila
            a = 255 * _eo(u / .25)
            _pegar(im, icono(ic, 52), x0 + 30, y + 30, _pop(u))
            d = ImageDraw.Draw(im)
            _texto(d, (x0 + 76, y + 30), txt, fuente("sans", 30), BLANCO, "lm", a)
            v = val * _eo(u / .8)
            acum += v
            _texto(d, (x1, y + 30), f"{int(round(v))} de oro", fuente("negra", 32), ORO_T, "rm", a)
            for xx in range(int(x0 + 76 + d.textlength(txt, font=fuente("sans", 30)) + 18), int(x1 - 190), 16):
                d.ellipse((xx, y + 40, xx + 3, y + 43), fill=GRIS + (int(a * .6),))
        tt = _mk(marcas, len(lineas), 1e9)
        yt = y0 + len(lineas) * fila + 16
        d.line([(x0, yt), (x1, yt)], fill=ORO + (200,), width=3)
        if dt >= tt:
            u = dt - tt
            tot = sum(v for _, _, v in lineas)
            s = 1 + .12 * max(0.0, 1 - u / .4)
            _texto(d, (x0, yt + 52), total_txt, fuente("serif", int(40 * s)), ORO_T, "lm", 255 * _eo(u / .3))
            _texto(d, (x1, yt + 52), f"{int(round(tot * _eo(u / 1.0)))} de oro", fuente("negra", int(48 * s)), ROJO, "rm",
                   255 * _eo(u / .3))
        ts = _mk(marcas, len(lineas) + 1, 1e9)
        if sello and dt >= ts:
            _sello(im, sello, M + ancho * .42, yt + 52, dt - ts, ROJO, 34, ang=-7)
        return _salida(im, dt)
    return fn


def desplome(titulo, puntos, remate=None, ico=None, ancho=1500):
    """puntos = [(etiqueta, platas), ...]; marca k: aparece el punto k y la línea baja hasta él (con su precio);
    marca len: remate en rojo. ico: ícono del objeto junto al título."""
    h = 560
    ymax = max(p for _, p in puntos)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        gx0, gx1, gy0, gy1 = M + 150, M + ancho - 110, M + 120, M + h - 120
        for k in range(5):                                         # rejilla
            y = gy0 + (gy1 - gy0) * k / 4
            d.line([(gx0, y), (gx1, y)], fill=(90, 90, 120, 90), width=1)
        d.line([(gx0, gy0 - 10), (gx0, gy1)], fill=ORO + (200,), width=3)
        d.line([(gx0, gy1), (gx1 + 20, gy1)], fill=ORO + (200,), width=3)
        if ico:
            _pegar(im, icono(ico, 70), M + 80, M + 150, _pop(dt))
            d = ImageDraw.Draw(im)
        n = len(puntos)
        xy = [(gx0 + 40 + (gx1 - gx0 - 80) * k / max(1, n - 1), gy1 - (gy1 - gy0) * p / ymax * .92) for k, (_, p) in enumerate(puntos)]
        ult = None
        for k in range(n):
            tk = _mk(marcas, k, .4 + k * .9)
            if dt < tk:
                break
            u = dt - tk
            if k > 0:
                q = _eo(u / .5)
                xa, ya = xy[k - 1]
                xb, yb = xy[k]
                d.line([(xa, ya), (xa + (xb - xa) * q, ya + (yb - ya) * q)], fill=ROJO + (255,), width=7)
            ult = k
        for k in range(0 if ult is None else ult + 1):
            u = dt - _mk(marcas, k, .4 + k * .9)
            x, y = xy[k]
            r = 13 * _pop(u)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(ORO_T if k == 0 else ROJO) + (255,), outline=(20, 10, 0, 255), width=3)
            a = 255 * _eo(u / .3)
            _texto(d, (x, y - 34), _ptxt(puntos[k][1]), fuente("negra", 30), ORO_T if k == 0 else BLANCO, "mm", a)
            _texto(d, (x, gy1 + 34), puntos[k][0], fuente("sans", 24), GRIS, "mm", a)
        tr = _mk(marcas, n, 1e9)
        if remate and dt >= tr:
            _texto(d, (M + ancho / 2, M + h - 40), remate, fuente("serif", 34), ROJO, "mm", 255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


def balanza(titulo, objeto, izq, der, remate=None, ancho=1400):
    """objeto = (ícono, nombre); izq/der = (rótulo, texto_precio, peso). Marca 0: objeto · 1: platillo izq · 2: platillo der y la
    balanza se inclina al de más peso · 3: remate en verde."""
    h = 640

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t = [_mk(marcas, i, .4 + i * 1.0) for i in range(4)]
        cx, cy = M + ancho / 2, M + 200
        if dt >= t[0]:
            _pegar(im, icono(objeto[0], 96), cx, M + 128, _pop(dt - t[0]))
            d = ImageDraw.Draw(im)
            _texto(d, (cx, M + 196), objeto[1], fuente("sans", 28), BLANCO, "mm", 255 * _eo((dt - t[0]) / .3))
        ang = 0.0
        if dt >= t[2]:
            sg = 1 if der[2] > izq[2] else -1
            u = dt - t[2]
            ang = sg * .10 * (1 - math.exp(-5 * u) * math.cos(8 * u))
        L = ancho * .32
        py = cy + 70
        d.line([(cx, py - 30), (cx, M + h - 110)], fill=ORO + (255,), width=6)
        d.polygon([(cx - 70, M + h - 100), (cx + 70, M + h - 100), (cx, M + h - 140)], fill=ORO + (255,))
        ax, ay = cx - L * math.cos(ang), py - L * math.sin(ang)
        bx, by = cx + L * math.cos(ang), py + L * math.sin(ang)
        d.line([(ax, ay), (bx, by)], fill=ORO_T + (255,), width=6)
        for (px, pyy), lado, tk in (((ax, ay), izq, t[1]), ((bx, by), der, t[2])):
            d.line([(px, pyy), (px - 60, pyy + 80)], fill=ORO + (200,), width=2)
            d.line([(px, pyy), (px + 60, pyy + 80)], fill=ORO + (200,), width=2)
            d.chord((px - 90, pyy + 50, px + 90, pyy + 120), 0, 180, fill=(30, 26, 60, 240), outline=ORO + (255,), width=3)
            if dt >= tk:
                a = 255 * _eo((dt - tk) / .3)
                _texto(d, (px, M + h - 170), lado[0], fuente("sans", 28), GRIS, "mm", a)
                _texto(d, (px, M + h - 125), lado[1], fuente("negra", 40), ORO_T, "mm", a)
        if remate and dt >= t[3]:
            _texto(d, (cx, M + h - 45), remate, fuente("serif", 32), VERDE, "mm", 255 * _eo((dt - t[3]) / .3))
        return _salida(im, dt)
    return fn


def escalera(titulo, peldanos, plano, remate=None, ancho=1500):
    """peldanos = [(rótulo, texto_precio), ...] que suben uno por marca (rojo); plano = (rótulo, texto) = pago único (verde) en la
    marca len; remate en la marca len+1."""
    h = 520
    n = len(peldanos)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, yb, wp = M + 90, M + h - 90, (ancho * .58) / max(1, n)
        for k, (rot, pre) in enumerate(peldanos):
            tk = _mk(marcas, k, .4 + k * .8)
            if dt < tk:
                continue
            u = dt - tk
            hh = (k + 1) * (h - 300) / n * _eo(u / .4)
            x = x0 + k * wp
            d.rounded_rectangle((x + 6, yb - hh, x + wp - 6, yb), 6, fill=(150, 30, 30, 235), outline=ROJO + (255,), width=3)
            a = 255 * _eo(u / .3)
            _texto(d, (x + wp / 2, yb - hh - 28), pre, fuente("negra", 30), ORO_T, "mm", a)
            _texto(d, (x + wp / 2, yb + 30), rot, fuente("sans", 22), GRIS, "mm", a)
        tp = _mk(marcas, n, 1e9)
        if dt >= tp:
            u = dt - tp
            xp = x0 + n * wp + 60
            wpl = M + ancho - 70 - xp
            hp = (h - 300) * .45
            q = _eo(u / .4)
            d.rounded_rectangle((xp, yb - hp, xp + wpl * q, yb), 8, fill=(20, 120, 40, 240), outline=VERDE + (255,), width=3)
            a = 255 * _eo(u / .3)
            _texto(d, (xp + wpl / 2, yb - hp - 30), plano[1], fuente("negra", 34), VERDE, "mm", a)
            _texto(d, (xp + wpl / 2, yb + 30), plano[0], fuente("sans", 22), BLANCO, "mm", a)
        tr = _mk(marcas, n + 1, 1e9)
        if remate and dt >= tr:
            _texto(d, (M + ancho / 2, M + 112), remate, fuente("serif", 32), VERDE, "mm", 255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


def techo(titulo, ico, nombre, precios, tope, remate=None, ancho=1400):
    """precios = [(rótulo, oro), ...]: la barra sube en cada marca; `tope` = (rótulo, oro) = techo fijo que se dibuja en la marca
    len (línea roja con candado); remate en la marca len+1."""
    h = 580
    ymax = tope[1] * 1.12

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        _pegar(im, icono(ico, 90), M + 110, M + 170, _pop(dt))
        d = ImageDraw.Draw(im)
        _texto(d, (M + 110, M + 236), nombre, fuente("sans", 24), BLANCO, "mm")
        gx0, gx1, gy0, gy1 = M + 260, M + ancho - 80, M + 110, M + h - 110
        d.line([(gx0, gy1), (gx1, gy1)], fill=ORO + (200,), width=3)
        n = len(precios)
        wb = (gx1 - gx0) / (n + 1)
        for k, (rot, val) in enumerate(precios):
            tk = _mk(marcas, k, .4 + k * .8)
            if dt < tk:
                continue
            u = dt - tk
            hh = (gy1 - gy0) * val / ymax * _eo(u / .5)
            x = gx0 + wb * (k + .5)
            d.rounded_rectangle((x - wb * .3, gy1 - hh, x + wb * .3, gy1), 6, fill=(200, 160, 40, 235), outline=ORO_T + (255,), width=2)
            a = 255 * _eo(u / .3)
            _texto(d, (x, gy1 - hh - 26), f"{val:g} de oro", fuente("negra", 28), ORO_T, "mm", a)
            _texto(d, (x, gy1 + 26), rot, fuente("sans", 22), GRIS, "mm", a)
        tt = _mk(marcas, n, 1e9)
        if dt >= tt:
            u = dt - tt
            yt = gy1 - (gy1 - gy0) * tope[1] / ymax
            q = _eo(u / .5)
            for xx in range(int(gx0), int(gx0 + (gx1 - gx0) * q), 28):
                d.line([(xx, yt), (xx + 16, yt)], fill=ROJO + (255,), width=5)
            _texto(d, (gx1, yt - 26), f"{tope[0]}: {tope[1]:g} de oro", fuente("negra", 30), ROJO, "rm", 255 * _eo(u / .3))
        tr = _mk(marcas, n + 1, 1e9)
        if remate and dt >= tr:
            _texto(d, (M + ancho / 2 + 90, M + h - 34), remate, fuente("serif", 30), VERDE, "mm", 255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


def dia_noche(titulo, ico, nombre, noche, dia, remate=None, ancho=1400):
    """noche/dia = texto de precio. Marca 0: luna y precio de noche · 1: sol y precio de mañana (verde) · 2: remate."""
    h = 440

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t = [_mk(marcas, i, .4 + i * 1.2) for i in range(3)]
        cx = M + ancho / 2
        _pegar(im, icono(ico, 96), cx, M + 170, _pop(dt))
        d = ImageDraw.Draw(im)
        _texto(d, (cx, M + 240), nombre, fuente("sans", 26), BLANCO, "mm")
        for k, (lx, etiqueta, precio, col, tk) in enumerate(((M + ancho * .2, "DE NOCHE", noche, GRIS, t[0]),
                                                               (M + ancho * .8, "POR LA MAÑANA", dia, VERDE, t[1]))):
            if dt < tk:
                continue
            u = dt - tk
            s = _pop(u)
            r = 46 * s
            if k == 0:                                             # luna
                d.ellipse((lx - r, M + 150 - r, lx + r, M + 150 + r), fill=(220, 225, 255, 255))
                d.ellipse((lx - r + 22, M + 150 - r - 8, lx + r + 22, M + 150 + r - 8), fill=(16, 22, 56, 255))
            else:                                                  # sol
                for j in range(12):
                    a_ = j * math.pi / 6 + dt * .4
                    d.line([(lx + math.cos(a_) * r * 1.1, M + 150 + math.sin(a_) * r * 1.1),
                            (lx + math.cos(a_) * r * 1.5, M + 150 + math.sin(a_) * r * 1.5)], fill=ORO_T + (255,), width=5)
                d.ellipse((lx - r, M + 150 - r, lx + r, M + 150 + r), fill=ORO_T + (255,))
            a = 255 * _eo(u / .3)
            _texto(d, (lx, M + 240), etiqueta, fuente("sans", 26), GRIS, "mm", a)
            _texto(d, (lx, M + 300), precio, fuente("negra", 46), col, "mm", a)
        if remate and dt >= t[2]:
            _texto(d, (cx, M + h - 50), remate, fuente("serif", 32), VERDE, "mm", 255 * _eo((dt - t[2]) / .3))
        return _salida(im, dt)
    return fn


# ============================================================================ wow_oro_30_50 (26-nov-2026)
import os as _os
import re as _re

from PIL import Image as _Image

from mg_wow import _medallon
from mg_wow60 import _img

COB, PLA = (215, 130, 65), (205, 212, 222)
AZUL_A, ROJO_H, GRIS_N = (50, 110, 225), (190, 38, 34), (110, 110, 120)
_MON = {"o": ORO_T, "p": PLA, "c": COB}
_TOK = _re.compile(r"^([~+≈]?\d[\d.,\-]*)([opc])(\S*)$")


def _capa(im):
    return _Image.new("RGBA", im.size, (0, 0, 0, 0))


def _encaja(d, s, nombre, tam, ancho):
    while tam > 16 and d.textlength(s, font=fuente(nombre, tam)) > ancho:
        tam -= 2
    return fuente(nombre, tam)


def _partes(txt):
    """«1o 30p» → [("1", "o", ""), ("30", "p", "")]; una palabra sin moneda → (palabra, None, "")."""
    out = []
    for w in str(txt).split():
        m = _TOK.match(w)
        out.append((m.group(1), m.group(2), m.group(3)) if m else (w, None, ""))
    return out


def ancho_precio(d, txt, tam):
    f, r, w = fuente("negra", tam), tam * .36, 0.0
    for num, mon, suf in _partes(txt):
        w += d.textlength(num, font=f) + (2 * r + 12 if mon else 0) + (d.textlength(suf, font=f) if suf else 0) + tam * .26
    return max(0.0, w - tam * .26)


def precio(im, x, y, txt, tam=44, ancla="l", alfa=255, color=BLANCO):
    """Precio al estilo del juego (número + moneda de oro/plata/cobre dibujada), centrado en vertical en y; ancla l/m/r."""
    d = ImageDraw.Draw(im)
    w = ancho_precio(d, txt, tam)
    x0 = x if ancla == "l" else x - w / 2 if ancla == "m" else x - w
    f, r, a = fuente("negra", tam), tam * .36, int(max(0, min(255, alfa)))
    if a <= 0:
        return w
    for num, mon, suf in _partes(txt):
        _texto(d, (x0, y), num, f, color, "lm", a)
        x0 += d.textlength(num, font=f)
        if mon:
            cx = x0 + 7 + r
            d.ellipse((cx - r, y - r, cx + r, y + r), fill=_MON[mon] + (a,), outline=(40, 28, 8, a), width=2)
            d.ellipse((cx - r * .55, y - r * .62, cx + r * .02, y - r * .08), fill=(255, 255, 255, int(a * .5)))
            x0 = cx + r + 5
        if suf:
            _texto(d, (x0, y), suf, f, color, "lm", a)
            x0 += d.textlength(suf, font=f)
        x0 += tam * .26
    return w


def _cobre(txt):
    """Valor en cobre de un precio hecho solo de monedas («6o 84p» → 68400), o None."""
    v, hay = 0, False
    for num, mon, suf in _partes(txt):
        if not mon:
            if num in ("~", "≈", "+"):
                continue
            return None
        try:
            n = float(num.lstrip("~+≈").replace(",", "."))
        except ValueError:
            return None
        v += n * {"o": 10000, "p": 100, "c": 1}[mon]
        hay = True
    return int(v) if hay else None


def _fmt(cobre):
    o, r = divmod(int(cobre), 10000)
    p, c = divmod(r, 100)
    s = ([f"{o}o"] if o else []) + ([f"{p}p"] if p else []) + ([f"{c}c"] if c and not o else [])
    return " ".join(s) or "0c"


def _ranura(im, cx, cy, t, src, u=1.0, borde=ORO):
    """Casilla de inventario con su imagen (ruta, ícono de Wowhead o «txt:2» = texto grande); u = s desde que entra."""
    d = ImageDraw.Draw(im)
    x, y = cx - t / 2, cy - t / 2
    d.rounded_rectangle((x, y, x + t, y + t), 12, fill=(4, 6, 18, 245), outline=tuple(borde) + (255,), width=3)
    if u is None or u <= 0:
        return
    s = _pop(u, .3)
    if str(src).startswith("txt:"):
        _texto(d, (cx, cy + 2), src[4:], fuente("negra", max(8, int(t * .5 * s))), ORO_T, "mm")
    else:
        _pegar(im, _img(src, int(t - 14)), cx, cy, s)


def _faccion(im, x, y, bando, alfa=255):
    """Píldora de facción (blanco sobre rojo/azul/gris); devuelve su ancho."""
    d = ImageDraw.Draw(im)
    txt = {"horda": "HORDA", "alianza": "ALIANZA"}.get(bando.lower(), "LOS DOS")
    col = {"HORDA": ROJO_H, "ALIANZA": AZUL_A}.get(txt, GRIS_N)
    f = fuente("negra", 24)
    w = d.textlength(txt, font=f) + 30
    a = int(alfa)
    d.rounded_rectangle((x, y - 21, x + w, y + 21), 21, fill=col + (a,), outline=(255, 255, 255, int(a * .7)), width=2)
    _texto(d, (x + w / 2, y + 1), txt, f, BLANCO, "mm", a)
    return w


def cuenta(titulo, terminos, total, op="+", bolsa=None, remate=None, ancho=1560):
    """terminos = [(img, rótulo, precio)]; total = (rótulo, precio, sello|None). Marca k = término k (con su operador);
    marca len = «=» y el total con sello; len+1 = bolsa (rótulo, valor, de, precio) que se llena hasta valor/de;
    len+2 = remate en verde."""
    n = len(terminos)
    h = 430 + (130 if bolsa else 0) + (56 if remate else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        gap = 120
        wb = (ancho - 80 - gap * n) / (n + 1)
        cy = M + 180
        for k in range(n + 1):
            cx = M + 40 + wb / 2 + k * (wb + gap)
            tk = _mk(marcas, k, .4 + k * .9)
            if dt < tk:
                continue
            u, a = dt - tk, 255 * _eo((dt - tk) / .3)
            d = ImageDraw.Draw(im)
            if k:
                _texto(d, (cx - wb / 2 - gap / 2, cy + 44), "=" if k == n else op, fuente("serif", 96), ORO_T, "mm", a)
            if k == n:
                rot, pre, sello = (list(total) + [None])[:3]
                s = 1 + .25 * max(0.0, 1 - u / .35)
                wtot = ancho_precio(d, pre, int(78 * s)) + 60
                d.rounded_rectangle((cx - wtot / 2, cy - 62, cx + wtot / 2, cy + 62), 18, fill=(40, 8, 8, 245),
                                    outline=ROJO + (255,), width=4)
                precio(im, cx, cy, pre, int(78 * s), "m", a, ORO_T)
                d = ImageDraw.Draw(im)
                _texto(d, (cx, cy + 100), rot, _encaja(d, rot, "sans", 32, wb + gap - 10), BLANCO, "mm", a)
                if sello:
                    _sello(im, sello, cx, cy + 162, u - .35, ROJO, 34, ang=-6)
            else:
                img, rot, pre = terminos[k]
                _ranura(im, cx, cy, 124, img, u)
                d = ImageDraw.Draw(im)
                _texto(d, (cx, cy + 100), rot, _encaja(d, rot, "sans", 32, wb + gap - 10), BLANCO, "mm", a)
                precio(im, cx, cy + 160, pre, 52, "m", a, BLANCO)
        if bolsa:
            tb = _mk(marcas, n + 1, 1e9)
            if dt >= tb:
                rot, valor, de, pre = bolsa
                u = dt - tb
                d = ImageDraw.Draw(im)
                x0, x1, yb = M + 70, M + ancho - 70, M + 430 + 62
                a = 255 * _eo(u / .3)
                _texto(d, (x0, yb - 44), rot, fuente("sans", 30), BLANCO, "lm", a)
                d.rounded_rectangle((x0, yb - 18, x1, yb + 18), 18, fill=(6, 8, 22, 245), outline=ORO + (200,), width=2)
                q = _eo((u - .2) / .9) * valor / de
                if q > 0:
                    d.rounded_rectangle((x0 + 3, yb - 15, x0 + 3 + (x1 - x0 - 6) * q, yb + 15), 15, fill=ORO_T + (255,))
                precio(im, x0 + (x1 - x0) * q + 14, yb - 44, pre, 34, "l", a, ORO_T)
                precio(im, x1, yb - 44, total[1], 30, "r", a * .8, GRIS)
        tr = _mk(marcas, n + 2, 1e9)
        if remate and dt >= tr:
            d = ImageDraw.Draw(im)
            _texto(d, (M + ancho / 2, M + h - 40), remate, _encaja(d, remate, "serif", 36, ancho - 100), VERDE, "mm",
                   255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


def cronometro(titulo, ico, minutos, total, objetos=None, hora=None, ancho=1440):
    """Marca 0 = arranca; marca 1 = llega a `minutos` (el oro `total` sube a la vez); marca 2 = «por hora» (`hora`) en verde.
    objetos = (img, texto) bajo el total, p. ej. ("o_molleja_buitre", "92 objetos")."""
    h = 540
    c_tot = _cobre(total)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        t0, t1, t2 = _mk(marcas, 0, .4), _mk(marcas, 1, 3.2), _mk(marcas, 2, 1e9)
        q = _eo(max(0.0, min(1.0, (dt - t0) / max(.6, t1 - t0)))) if dt >= t0 else 0.0
        cx, cy, r = M + 250, M + 300, 170
        capa = _capa(im)
        dc = ImageDraw.Draw(capa)
        dc.rounded_rectangle((cx - 24, cy - r - 52, cx + 24, cy - r - 14), 7, fill=ORO + (255,))
        dc.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=(34, 28, 10, 255), outline=ORO + (255,), width=6)
        dc.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(8, 10, 28, 255))
        ang = 360 * minutos / 60 * q
        if ang > .5:
            dc.pieslice((cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), -90, -90 + ang, fill=(255, 196, 30, 110))
        for i in range(60):
            a_, larga = math.radians(i * 6 - 90), i % 5 == 0
            l = 24 if larga else 10
            dc.line([(cx + math.cos(a_) * (r - 6), cy + math.sin(a_) * (r - 6)),
                     (cx + math.cos(a_) * (r - 6 - l), cy + math.sin(a_) * (r - 6 - l))],
                    fill=(BLANCO if larga else GRIS) + (255,), width=4 if larga else 2)
        a_ = math.radians(-90 + ang)
        dc.line([(cx, cy), (cx + math.cos(a_) * (r - 34), cy + math.sin(a_) * (r - 34))], fill=ROJO + (255,), width=8)
        dc.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill=ORO_T + (255,))
        im.alpha_composite(capa)
        d = ImageDraw.Draw(im)
        _texto(d, (cx, cy + r * .5), f"{int(round(minutos * q))} MIN", fuente("negra", 42), BLANCO, "mm")
        xr = M + 500
        _pegar(im, _img(ico, 120), xr + 70, M + 190, _pop(dt - t0) if dt >= t0 else 0)
        d = ImageDraw.Draw(im)
        if dt >= t0:
            a = 255 * _eo((dt - t0) / .3)
            _texto(d, (xr + 160, M + 150), "ORO EN LA BOLSA", fuente("sans", 30), GRIS, "lm", a)
            txt = total if (q >= .999 or c_tot is None) else _fmt(c_tot * q)
            precio(im, xr + 160, M + 214, txt, 70 if q >= .999 else 64, "l", a, ORO_T if q >= .999 else BLANCO)
            if objetos and q >= .999:
                ob_img, ob_txt = objetos
                u = dt - t1
                _pegar(im, _img(ob_img, 60), xr + 70, M + 310, _pop(u))
                d = ImageDraw.Draw(im)
                _texto(d, (xr + 160, M + 310), ob_txt, fuente("sans", 34), BLANCO, "lm", 255 * _eo(u / .3))
        if hora and dt >= t2:
            u = dt - t2
            d = ImageDraw.Draw(im)
            y = M + 430
            d.rounded_rectangle((xr + 20, y - 52, M + ancho - 50, y + 52), 20, fill=(8, 40, 14, 245), outline=VERDE + (255,), width=4)
            _texto(d, (xr + 50, y), "POR HORA", fuente("sans", 30), BLANCO, "lm", 255 * _eo(u / .3))
            s = 1 + .2 * max(0.0, 1 - u / .35)
            precio(im, M + ancho - 80, y, hora, int(56 * s), "r", 255 * _eo(u / .3), VERDE)
        return _salida(im, dt)
    return fn


def _etiqueta(rot, pre, gana, ancho=430):
    """Etiqueta de precio (cartón azul noche con ojal y borde de oro; verde si gana)."""
    w, h = ancho, 214
    im = _Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    col = VERDE if gana else ORO
    d.rounded_rectangle((10, 10, w + 10, h + 10), 22, fill=(14, 20, 52, 248), outline=col + (255,), width=5)
    d.ellipse((w / 2 + 10 - 13, 22, w / 2 + 10 + 13, 48), fill=(0, 0, 0, 0), outline=col + (255,), width=4)
    _texto(d, (w / 2 + 10, 84), rot, _encaja(d, rot, "sans", 34, w - 40), BLANCO, "mm")
    tam = 56
    while tam > 24 and ancho_precio(d, pre, tam) > w - 40:
        tam -= 2
    precio(im, w / 2 + 10, 154, pre, tam, "m", 255, VERDE if gana else ORO_T)
    return im


def etiquetas(titulo, ico, nombre, izq, der, sello=None, nota=None, ancho=1400):
    """izq/der = (rótulo, precio); marca 0 = cuelga la izquierda, 1 = la derecha (se balancean); marca 2 = sello
    (lado, texto) sobre la ganadora (lado 0/1) y nota debajo. El ícono y el nombre arriba desde el inicio."""
    h = 700
    gana = sello[0] if sello else None
    tags = [None, None]

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        _pegar(im, _img(ico, 92), M + ancho / 2 - 220, M + 150, _pop(dt))
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2 - 160, M + 150), nombre, _encaja(d, nombre, "negra", 44, ancho / 2 + 100), BLANCO, "lm",
               255 * _eo(dt / .3))
        yb = M + 236
        d.line([(M + 80, yb), (M + ancho - 80, yb)], fill=ORO + (255,), width=6)
        t2 = _mk(marcas, 2, 1e9)
        for k, (rot, pre) in enumerate((izq, der)):
            tk = _mk(marcas, k, .4 + k * 1.0)
            if dt < tk:
                continue
            u = dt - tk
            g = gana == k and dt >= t2
            if tags[k] is None or tags[k][0] != g:
                tags[k] = (g, _etiqueta(rot, pre, g))
            tag = tags[k][1]
            ang = 14 * math.exp(-2.6 * u) * math.cos(7 * u) * (1 if k else -1)
            cx = M + ancho * (.27 if k == 0 else .73)
            d = ImageDraw.Draw(im)
            caida = 1 - _eo(u / .35)
            px, py = cx, yb + 4
            ex, ey = px + math.sin(math.radians(ang)) * 70, py + 70 - caida * 60
            d.line([(px, py), (ex, ey)], fill=ORO + (255,), width=3)
            rt = tag.rotate(ang, expand=True, resample=_Image.BICUBIC)
            if g:
                _brillo_caja(im, (ex - tag.width / 2, ey, ex + tag.width / 2, ey + tag.height), VERDE)
            _pegar(im, rt, ex, ey + tag.height / 2 + 4, 1.0, _eo(u / .2))
        if sello and dt >= t2:
            cx = M + ancho * (.27 if sello[0] == 0 else .73)
            _sello(im, sello[1], cx, yb + 352, dt - t2, VERDE, 34, ang=-7)
        if nota and dt >= t2:
            d = ImageDraw.Draw(im)
            _texto(d, (M + ancho / 2, M + h - 34), nota, _encaja(d, nota, "serif", 32, ancho - 100), GRIS, "mm",
                   255 * _eo((dt - t2 - .3) / .3))
        return _salida(im, dt)
    return fn


def _brillo_caja(im, caja, color, ancho=10, blur=8):
    from PIL import ImageFilter
    g = _capa(im)
    ImageDraw.Draw(g).rounded_rectangle(caja, 24, outline=tuple(color) + (200,), width=ancho)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))


def probabilidad(titulo, cara, ico, n, aciertos, rotulo, remate=None, ancho=1560, paso=.2):
    """n retratos de la criatura (cara) que caen uno a uno desde la marca 0 (cada `paso` s); en los índices `aciertos` salta
    el objeto (ico) encima con brillo y suma al contador; al final, `rotulo` grande; marca 1 = remate en verde."""
    h = 470 + (50 if remate else 0)
    r = int(min(60, (ancho - 140) / n / 2 - 10))

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        t0 = _mk(marcas, 0, .4)
        dx = (ancho - 140) / n
        cy = M + 250
        hits = 0
        for k in range(n):
            cx = M + 70 + dx * (k + .5)
            tk = t0 + paso * k
            muerto = dt >= tk
            med = _medallon(cara, r, gris=muerto and k not in aciertos)
            _pegar(im, med, cx, cy, 1.0, 1.0 if dt >= t0 - .3 else 0)
            if not muerto:
                continue
            u = dt - tk
            d = ImageDraw.Draw(im)
            if k in aciertos:
                hits += 1
                _brillo_caja(im, (cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), ORO_T, 8, 6)
                _ranura(im, cx, cy - r - 66, 76, ico, u, ORO_T)
            else:
                q = _eo(u / .2)
                d.line([(cx - r * .6, cy - r * .6), (cx - r * .6 + r * 1.2 * q, cy - r * .6 + r * 1.2 * q)], fill=ROJO + (230,), width=7)
                d.line([(cx + r * .6, cy - r * .6), (cx + r * .6 - r * 1.2 * q, cy - r * .6 + r * 1.2 * q)], fill=ROJO + (230,), width=7)
        d = ImageDraw.Draw(im)
        vistos = max(0, min(n, int((dt - t0) / paso) + 1)) if dt >= t0 else 0
        if vistos:
            fin = vistos >= n and dt >= t0 + paso * n + .2
            txt = rotulo if fin else f"{hits} de {vistos}"
            _texto(d, (M + ancho / 2, M + 380), txt, _encaja(d, txt, "negra", 56, ancho - 100), ORO_T if fin else BLANCO, "mm")
        tr = _mk(marcas, 1, 1e9)
        if remate and dt >= tr:
            _texto(d, (M + ancho / 2, M + h - 36), remate, _encaja(d, remate, "serif", 34, ancho - 100), VERDE, "mm",
                   255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


def encoge(titulo, ico, nombre, de, a, lapso="EN UNA SEMANA", dias=7, remate=None, ancho=1400):
    """Marca 0 = el objeto con su precio de antes (oro); marca 1 = pasan los días (cada 0,3 s) y el precio se encoge hasta
    `a` (rojo) con flecha; marca 2 = remate en verde."""
    h = 520 + (50 if remate else 0)
    c0, c1 = _cobre(de), _cobre(a)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        t0, t1, t2 = _mk(marcas, 0, .4), _mk(marcas, 1, 1.6), _mk(marcas, 2, 1e9)
        cx = M + 230
        q = max(0.0, min(1.0, (dt - t1) / (.3 * dias))) if dt >= t1 else 0.0
        s_ico = 1 - .22 * _eo(q)
        if dt >= t0:
            _pegar(im, _img(ico, 210), cx, M + 220, _pop(dt - t0) * s_ico)
            d = ImageDraw.Draw(im)
            _texto(d, (cx, M + 360), nombre, _encaja(d, nombre, "sans", 34, 380), BLANCO, "mm", 255 * _eo((dt - t0) / .3))
        xr = M + 480
        d = ImageDraw.Draw(im)
        if dt >= t0:
            fin = q >= .999
            if c0 is not None and c1 is not None and not fin:
                txt = _fmt(c0 + (c1 - c0) * _eo(q))
            else:
                txt = a if fin else de
            col = ROJO if fin else (ORO_T if q <= 0 else BLANCO)
            s = 1 + .2 * max(0.0, 1 - (dt - t1 - .3 * dias) / .35) if fin else 1
            precio(im, xr + 20, M + 190, txt, int(96 * s), "l", 255 * _eo((dt - t0) / .3), col)
            d = ImageDraw.Draw(im)
            if q > 0:
                xa = M + ancho - 120
                ya0, ya1 = M + 120, M + 120 + 170 * _eo(q)
                d.line([(xa, ya0), (xa, ya1)], fill=ROJO + (255,), width=14)
                d.polygon([(xa - 32, ya1 - 6), (xa + 32, ya1 - 6), (xa, ya1 + 34)], fill=ROJO + (255,))
        if dt >= t1:
            wd, gap = 92, 16
            x0 = xr + 20
            y = M + 330
            for i in range(dias):
                ti = t1 + .3 * i
                lleno = dt >= ti
                x = x0 + i * (wd + gap)
                d.rounded_rectangle((x, y, x + wd, y + wd), 12, fill=((70, 20, 20, 245) if lleno else (6, 8, 22, 245)),
                                    outline=(ROJO if lleno else ORO) + (255,), width=3)
                _texto(d, (x + wd / 2, y + wd / 2), str(i + 1), fuente("negra", 40), BLANCO if lleno else GRIS, "mm")
            _texto(d, (x0, y + wd + 40), lapso, fuente("serif", 34), ORO_T, "lm", 255 * _eo((dt - t1) / .3))
        if remate and dt >= t2:
            _texto(d, (M + ancho / 2, M + h - 36), remate, _encaja(d, remate, "serif", 34, ancho - 100), VERDE, "mm",
                   255 * _eo((dt - t2) / .3))
        return _salida(im, dt)
    return fn


def _candado(im, cx, cy, t, u):
    d = ImageDraw.Draw(im)
    s = _pop(u, .3)
    if s <= .02:
        return
    w, hh = t * .5 * s, t * .38 * s
    d.arc((cx - w * .38, cy - hh * 1.25, cx + w * .38, cy + hh * .1), 180, 360, fill=ORO_T + (255,), width=max(3, int(9 * s)))
    d.rounded_rectangle((cx - w / 2, cy - hh * .35, cx + w / 2, cy + hh * .85), 8, fill=ORO_T + (255,), outline=(60, 40, 0, 255), width=3)
    d.ellipse((cx - 7 * s, cy + hh * .1, cx + 7 * s, cy + hh * .1 + 14 * s), fill=(40, 26, 0, 255))


def tope(titulo, ico, n, rotulo, candado="TOPE", remate=None, ancho=1400):
    """Marca 0 = se llenan n ranuras (cada 0,3 s, con su número); marca 1 = la n+1 se cierra con candado y sello;
    marca 2 = remate en verde."""
    h = 460 + (56 if remate else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        t0, t1, t2 = _mk(marcas, 0, .4), _mk(marcas, 1, 2.4), _mk(marcas, 2, 1e9)
        t, gap = 140, 40
        x0 = M + (ancho - ((n + 1) * t + n * gap)) / 2 + t / 2
        cy = M + 200
        for i in range(n + 1):
            cx = x0 + i * (t + gap)
            if i < n:
                u = dt - (t0 + .3 * i)
                _ranura(im, cx, cy, t, ico, u if u > 0 else None)
                if u > 0:
                    d = ImageDraw.Draw(im)
                    _texto(d, (cx, cy + t / 2 + 34), str(i + 1), fuente("negra", 40), BLANCO, "mm", 255 * _eo(u / .3))
            else:
                d = ImageDraw.Draw(im)
                d.rounded_rectangle((cx - t / 2, cy - t / 2, cx + t / 2, cy + t / 2), 12, fill=(30, 6, 6, 245),
                                    outline=(ROJO if dt >= t1 else GRIS) + (255,), width=3)
                if dt >= t1:
                    _candado(im, cx, cy, t, dt - t1)
                    _sello(im, candado, cx, cy + t / 2 + 40, dt - t1 - .2, ROJO, 30, ang=-6)
        d = ImageDraw.Draw(im)
        if dt >= t0 + .3 * n:
            xm = x0 + (n - 1) * (t + gap) / 2
            _texto(d, (xm, M + h - (110 if remate else 60)), rotulo, _encaja(d, rotulo, "negra", 44, n * (t + gap)), ORO_T, "mm",
                   255 * _eo((dt - t0 - .3 * n) / .3))
        if remate and dt >= t2:
            _texto(d, (M + ancho / 2, M + h - 40), remate, _encaja(d, remate, "serif", 36, ancho - 100), VERDE, "mm",
                   255 * _eo((dt - t2) / .3))
        return _salida(im, dt)
    return fn


def tabla_oro(titulo, filas, nueva=None, nota=None, ancho=1440):
    """filas = [(img, rótulo, valor|None, texto_precio)] de arriba abajo; nueva = índice de la fila que entra en la marca 0
    (crece con brillo); las demás ya están desde el inicio. valor None = barra punteada «¿?»."""
    fila = 78
    h = 110 + len(filas) * fila + (60 if nota else 20)
    vmax = max([v for _, _, v, _ in filas if v] or [1])

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        t0 = _mk(marcas, 0, .5)
        xb0, xb1 = M + 560, M + ancho - 250
        for i, (img, rot, v, txt) in enumerate(filas):
            y = M + 100 + i * fila + fila / 2
            es_nueva = i == nueva
            tk = t0 if es_nueva else (0.15 * i if nueva is None else 0.0)
            if dt < tk:
                continue
            u = dt - tk
            a = 255 * _eo(u / .3)
            if es_nueva:
                _brillo_caja(im, (M + 20, y - fila / 2 + 4, M + ancho - 20, y + fila / 2 - 4), ORO_T, 6, 6)
            src = img
            if src and _os.path.exists(str(src)):
                _pegar(im, _medallon(src, 28), M + 64, y, _pop(u) if es_nueva else 1.0, _eo(u / .2))
            elif src:
                _ranura(im, M + 64, y, 60, src, u)
            d = ImageDraw.Draw(im)
            _texto(d, (M + 110, y), rot, _encaja(d, rot, "sans", 30, xb0 - M - 130), BLANCO if es_nueva else (215, 215, 225), "lm", a)
            if v:
                q = _eo((u - .1) / .8) if es_nueva else 1.0
                d.rounded_rectangle((xb0, y - 20, xb0 + max(10, (xb1 - xb0) * v / vmax * q), y + 20), 14,
                                    fill=(ORO_T if es_nueva else (190, 150, 40)) + (255,))
            else:
                for xx in range(int(xb0), int(xb0 + (xb1 - xb0) * .3), 26):
                    d.line([(xx, y), (xx + 14, y)], fill=GRIS + (int(a),), width=5)
                _texto(d, (xb0 + (xb1 - xb0) * .3 + 20, y), "¿?", fuente("negra", 38), GRIS, "lm", a)
            precio(im, M + ancho - 40, y, txt, 34, "r", a, ORO_T if es_nueva else BLANCO)
        if nota:
            d = ImageDraw.Draw(im)
            _texto(d, (M + ancho / 2, M + h - 34), nota, _encaja(d, nota, "serif", 30, ancho - 100), GRIS, "mm")
        return _salida(im, dt)
    return fn


def _lineas(d, s, f, ancho):
    """Parte s en ≤ 2 líneas que quepan en `ancho`."""
    if d.textlength(s, font=f) <= ancho:
        return [s]
    pal, l1 = s.split(), ""
    for i, w in enumerate(pal):
        c = (l1 + " " + w).strip()
        if d.textlength(c, font=f) > ancho and l1:
            return [l1, " ".join(pal[i:])]
        l1 = c
    return [l1]


def ficha_farmeo(n, nombre, cara, nivel, zona, objetos, oro, venta, ancho=1680):
    """FICHA DEL FARMEO (el usuario, 25-nov-2026: «al cierre de cada puesto: nivel, zona, qué llevar, g/h, a quién venderlo»).
    Sin marcas (va en la pausa «post»): las filas entran cada 0,4 s; con marcas, la fila k entra en la marca k. objetos = [(img, nombre, precio de vendedor|None)] (≤ 4,
    en rejilla 2×2); oro = precio («13-14o/h») o texto; venta = [(bando, lugar)] con bando Horda/Alianza/Los dos."""
    filas_obj = (len(objetos) + 1) // 2
    alto_venta = 58 * len(venta)
    h = 112 + 70 + 70 + filas_obj * 86 + 22 + 74 + alto_venta + 40
    COLX = 390

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, f"FICHA DEL FARMEO · N.º {n}")
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .35)
        _pegar(im, _medallon(cara, 118), M + 195, M + 112 + 140, _pop(dt, .4))
        d = ImageDraw.Draw(im)
        f = _encaja(d, nombre, "negra", 44, 340)
        ls = _lineas(d, nombre, fuente("negra", 40), 340) if d.textlength(nombre, font=fuente("negra", 40)) > 340 else [nombre]
        for j, l in enumerate(ls):
            _texto(d, (M + 195, M + 112 + 300 + j * 46), l, _encaja(d, l, "negra", 40, 340) if len(ls) > 1 else f, BLANCO, "mm", 255 * a0)
        x0, xv = M + COLX, M + COLX + 200
        y = M + 112

        def et(k, yy, txt, alto):
            u = dt - _mk(marcas, k, .3 + .4 * k)
            if u <= 0:
                return None
            a = 255 * _eo(u / .3)
            dd = ImageDraw.Draw(im)
            _texto(dd, (x0, yy), txt, fuente("sans", 28), ORO_T, "lm", a)
            if alto:                                   # raya al PIE de la fila (no cruza los objetos)
                dd.line([(x0, yy - 22 + alto - 6), (M + ancho - 40, yy - 22 + alto - 6)], fill=ORO + (int(a * .3),), width=1)
            return a
        a = et(0, y + 22, "NIVEL", 70)
        if a:
            _texto(ImageDraw.Draw(im), (xv, y + 22), nivel, fuente("negra", 44), BLANCO, "lm", a)
        y += 70
        a = et(1, y + 22, "ZONA", 70)
        if a:
            dd = ImageDraw.Draw(im)
            _texto(dd, (xv, y + 22), zona, _encaja(dd, zona, "sans", 36, M + ancho - 50 - xv), BLANCO, "lm", a)
        y += 70
        a = et(2, y + 22, "SE LLEVA", filas_obj * 86 + 22)
        if a:
            wc = (M + ancho - 40 - xv) / 2
            for j, (img, nom, pre) in enumerate(objetos):
                cx = xv + (j % 2) * wc
                cy = y + 30 + (j // 2) * 86
                u = dt - (_mk(marcas, 2, 1.1) + .15 * j)
                if u <= 0:
                    continue
                aj = 255 * _eo(u / .3)
                _ranura(im, cx + 34, cy, 66, img, u)
                dd = ImageDraw.Draw(im)
                _texto(dd, (cx + 82, cy - (16 if pre else 0)), nom, _encaja(dd, nom, "sans", 30, wc - 100), BLANCO, "lm", aj)
                if pre:
                    precio(im, cx + 82, cy + 20, pre, 28, "l", aj, ORO_T)
        y += filas_obj * 86 + 22
        a = et(3, y + 26, "ORO", 74)
        if a:
            if any(m for _, m, _ in _partes(oro)):
                precio(im, xv, y + 26, oro, 46, "l", a, ORO_T)
            else:
                dd = ImageDraw.Draw(im)
                _texto(dd, (xv, y + 26), oro, _encaja(dd, oro, "sans", 34, M + ancho - 50 - xv), BLANCO, "lm", a)
        y += 74
        a = et(4, y + 22, "VENDE", 0)
        if a:
            for j, (bando, lugar) in enumerate(venta):
                yy = y + 22 + j * 58
                w = _faccion(im, xv, yy, bando, a)
                dd = ImageDraw.Draw(im)
                _texto(dd, (xv + w + 18, yy), lugar, _encaja(dd, lugar, "sans", 32, M + ancho - 60 - xv - w - 18), BLANCO, "lm", a)
        return _salida(im, dt)
    return fn


def puesto(n, nombre, img, zona, rangos, ancho=1500):
    """Tarjeta de capítulo «N.º n» (marca 0): retrato (cara) en medallón, nombre y zona; barra de nivel 30-50 debajo con los
    tramos [(a, b, rótulo)] que se encienden en las marcas 1, 2… (rótulo en blanco ENCIMA de la barra, nunca negro sobre oro)."""
    h = 440

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, f"N.º {n}")
        t0 = _mk(marcas, 0, .2)
        a0 = 255 * _eo((dt - t0) / .35)
        _pegar(im, _medallon(img, 98), M + 170, M + 196, _pop(dt - t0, .4))
        d = ImageDraw.Draw(im)
        _texto(d, (M + 300, M + 160), nombre, _encaja(d, nombre, "negra", 60, ancho - 360), BLANCO, "lm", a0)
        _texto(d, (M + 302, M + 232), zona, _encaja(d, zona, "serif", 36, ancho - 360), ORO_T, "lm", a0)
        x0, x1, yb = M + 90, M + ancho - 90, M + 366
        X = lambda v: x0 + (x1 - x0) * (v - 30) / 20
        d.rounded_rectangle((x0, yb - 16, x1, yb + 16), 16, fill=(6, 8, 22, 245), outline=ORO + (200,), width=2)
        for v in range(30, 51, 5):
            d.line([(X(v), yb - 22), (X(v), yb + 22)], fill=ORO_T + (200,), width=2)
            _texto(d, (X(v), yb + 44), str(v), fuente("serif", 26), ORO_T, "mm", a0 * .9)
        for k, (a, b, rot) in enumerate(rangos):
            tk = _mk(marcas, 1 + k, t0 + .8 + k * .8)
            if dt < tk:
                continue
            u = dt - tk
            q = _eo(u / .6)
            xa, xb = X(a), X(b)
            col = ORO_T if (a, b) != (30, 50) else (150, 120, 40)
            d.rounded_rectangle((xa + 2, yb - 13, xa + max(10, (xb - xa) * q) - 2, yb + 13), 13, fill=col + (255,))
            ft = _encaja(d, rot, "negra", 32, max(220, (xb - xa) * 2.2))
            tw = d.textlength(rot, font=ft)
            xm = min(max((xa + xb) / 2, x0 + tw / 2), x1 - tw / 2)
            _texto(d, (xm, yb - 44), rot, ft, BLANCO, "mm", 255 * _eo((u - .2) / .3))
        return _salida(im, dt)
    return fn


def reparto(titulo, total, partes, remate=None, ancho=1440):
    """total = precio del todo; partes = [(img, rótulo, fracción)]: marca 0 = barra entera con el total; marca 1 = se
    parte: el primer trozo se enciende (oro) con su ícono y rótulo, el resto queda gris con el suyo; marca 2 = remate."""
    h = 470 + (56 if remate else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        t0, t1, t2 = _mk(marcas, 0, .4), _mk(marcas, 1, 1.6), _mk(marcas, 2, 1e9)
        x0, x1, yb = M + 70, M + ancho - 70, M + 250
        if dt >= t0:
            u = dt - t0
            q = _eo(u / .6)
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((x0, yb - 40, x0 + (x1 - x0) * q, yb + 40), 22, fill=(150, 120, 40, 255), outline=ORO_T + (255,), width=3)
            precio(im, M + ancho / 2, M + 140, total, 64, "m", 255 * _eo(u / .3), ORO_T)
        if dt >= t1:
            u = dt - t1
            xa = x0
            for k, (img, rot, fr) in enumerate(partes):
                xb = xa + (x1 - x0) * fr
                d = ImageDraw.Draw(im)
                col = ORO_T if k == 0 else (80, 80, 92)
                q = _eo((u - .15 * k) / .4)
                if q <= 0:
                    continue
                d.rounded_rectangle((xa + 4, yb - 40, xb - 4, yb + 40), 22, fill=col + (255,), outline=BLANCO + (int(200 * q),), width=3)
                xm = (xa + xb) / 2
                _ranura(im, xm, yb, 70, img, u - .15 * k)
                d = ImageDraw.Draw(im)
                _texto(d, (xm, yb + 82), rot, _encaja(d, rot, "negra", 38, xb - xa - 20), ORO_T if k == 0 else BLANCO, "mm", 255 * q)
                xa = xb
        if remate and dt >= t2:
            d = ImageDraw.Draw(im)
            _texto(d, (M + ancho / 2, M + h - 44), remate, _encaja(d, remate, "serif", 38, ancho - 100), VERDE, "mm",
                   255 * _eo((dt - t2) / .3))
        return _salida(im, dt)
    return fn


def columnas(titulo, ico, barras, remate=None, ancho=1400, por_fila=5, celda=46):
    """barras = [(rótulo, n, texto)]: columna k = rejilla de íconos (por_fila de ancho) que se llena en la marca k, uno cada
    0,04 s, con el contador encima; el texto debajo; remate en la marca len."""
    filas_max = max(math.ceil(nb / por_fila) for _, nb, _ in barras)
    h = 110 + 70 + filas_max * (celda + 6) + 104 + (58 if remate else 10)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        wcol = ancho / len(barras)
        ybase = M + 110 + 70 + filas_max * (celda + 6)
        for k, (rot, nb, txt) in enumerate(barras):
            tk = _mk(marcas, k, .4 + k * 1.4)
            cx = M + wcol * (k + .5)
            gx0 = cx - (por_fila * (celda + 6)) / 2
            d = ImageDraw.Draw(im)
            for i in range(filas_max * por_fila):
                fx, fy = i % por_fila, i // por_fila
                x = gx0 + fx * (celda + 6)
                y = ybase - (fy + 1) * (celda + 6)
                d.rounded_rectangle((x, y, x + celda, y + celda), 7, fill=(4, 6, 18, 235), outline=(70, 62, 40, 255), width=1)
            if dt < tk:
                continue
            u = dt - tk
            vis = min(nb, int(u / .04) + 1)
            for i in range(vis):
                fx, fy = i % por_fila, i // por_fila
                x = gx0 + fx * (celda + 6)
                y = ybase - (fy + 1) * (celda + 6)
                _pegar(im, _img(ico, celda - 6), x + celda / 2, y + celda / 2, _pop(u - .04 * i, .25))
            d = ImageDraw.Draw(im)
            ytop = ybase - math.ceil(max(1, vis) / por_fila) * (celda + 6) - 40
            _texto(d, (cx, ytop), str(vis), fuente("negra", 56), ORO_T if vis == nb else BLANCO, "mm")
            a = 255 * _eo(u / .3)
            _texto(d, (cx, ybase + 34), rot, _encaja(d, rot, "sans", 30, wcol - 40), BLANCO, "mm", a)
            if txt:
                _texto(d, (cx, ybase + 70), txt, _encaja(d, txt, "serif", 28, wcol - 40), GRIS, "mm", a)
        tr = _mk(marcas, len(barras), 1e9)
        if remate and dt >= tr:
            d = ImageDraw.Draw(im)
            _texto(d, (M + ancho / 2, M + h - 36), remate, _encaja(d, remate, "serif", 36, ancho - 100), VERDE, "mm",
                   255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


def _prueba_nuevos():
    """Cuadro final de cada MG nuevo sobre un gris verdoso → %TEMP%/_mg_oro_nuevos_N.jpg."""
    import tempfile
    import numpy as np
    P = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "videos", "wow_oro_30_50")
    pg = lambda s: _os.path.join(P, "pegatinas", s + ".png")
    cr = lambda s: _os.path.join(P, "caras", s + ".png")
    pr = [
        (cuenta("LO QUE CUESTA EL NIVEL 40", [(pg("o_equitacion"), "Montura", "100o"), ("txt:×2", "Doble especialización", "50o")],
                ("De golpe", "150o", "DE GOLPE"), bolsa=("Un jugador llegó al 39 con", 67, 150, "67o"), remate="Y se puso a probar farmeos"),
         [.4, 1.2, 2.0, 2.8, 3.6]),
        (cronometro("COYOTES DE CLAROS DEL RÍO · CON CRONÓMETRO", pg("o_cola_tupida"), 30, "6o 84p", (pg("o_melena_espesa"), "20 de noviembre"),
                    "13-14o/h"), [.4, 2.4, 3.4]),
        (etiquetas("¿VENDEDOR O SUBASTA?", pg("o_carne_cangrejo"), "Carne de cangrejo tierna", ("VENDEDOR", "1p 12c"), ("SUBASTA", "14p"),
                   (1, "NO AL VENDEDOR"), "Precio del 12 de noviembre"), [.4, 1.4, 2.6]),
        (probabilidad("CARNE DE CANGREJO TIERNA", cr("reptador_arena"), pg("o_carne_cangrejo"), 10, [1, 4, 6, 9], "4 DE CADA 10",
                      "Y la compran los cocineros"), [.4, 4.0]),
        (encoge("REGLA 2 · LO QUE TODOS FARMEAN SE HUNDE", pg("o_huevo_gigante"), "Huevo gigante", "1o", "15p", "EN UNA SEMANA", 7,
                "El vendedor nunca te baja el precio"), [.4, 1.4, 4.4]),
        (tope("REGLA 1 · DESDE EL 20 DE NOVIEMBRE", "achievement_dungeon_gloryofthehero", 5, "CADA MAZMORRA: 5 POR HORA", "TOPE",
              "El oro del 30 al 50: en el mundo abierto"), [.4, 2.4, 3.2]),
        (tabla_oro("ORO POR HORA · LO QUE MIDIERON LOS JUGADORES", [(cr("coyote_llanuras"), "Coyotes · Claros del Río", 13.5, "13-14o/h"),
                                                                     (cr("jaguar_pantano"), "Jaguares · Pantano", 10, "+10o/h"),
                                                                     (cr("gorila_velo_bruma"), "Gorilas · Tuercespina", 5.5, "5-6o/h"),
                                                                     (cr("retador_magram"), "Centauros · Desolace", None, "sin medir")],
                   nueva=0, nota="Precios de cada día: cambian"), [.4]),
        (ficha_farmeo(15, "Centauros Magram", cr("retador_magram"), "33-38", "Desolace · Poblado Magram",
                      [(pg("o_pano_seda"), "Paño de seda", "1p 50c"), (pg("o_tejido_magico"), "Paño de tejido mágico", "2p 50c"),
                       ("inv_misc_coin_02", "Monedas", None)], "Sin medir todavía: reaparecen más rápido desde el 25-nov",
                      [("Horda", "Campamento del Espíritu Errante"), ("Alianza", "Punta de Nijel")]), []),
        (puesto(13, "GORILAS VELO DE BRUMA", cr("gorila_velo_bruma"), "Vega de Tuercespina", [(32, 35, "32-35"), (40, 41, "ancianos 40")]),
         [.2, 1.0, 1.8]),
        (reparto("30 MINUTOS DE BUITRES", "21o", [(pg("o_molleja_buitre"), "6 mollejas: la mitad", .5), ("inv_misc_bag_10", "Todo lo demás", .5)],
                 "Sin mollejas: unos 17 de oro por hora"), [.4, 1.4, 2.6]),
        (columnas("VALIJAS POR HORA", pg("o_valija_mitril"), [("Sin el talento", 15, "unas 15"), ("Con el Maestro del cebo", 40, "unas 40")],
                  "Cada valija: unas 70 platas de media"), [.4, 1.8, 3.6]),
    ]
    sel = [int(a) for a in __import__("sys").argv[2:]] or range(len(pr))
    for i in sel:
        fn, mk = pr[i]
        a = fn(7.5, 8.0, mk)
        im = _Image.fromarray(a[..., [2, 1, 0, 3]])
        fondo = _Image.new("RGB", (1920, 1080), (58, 82, 64))
        fondo.paste(im, ((1920 - im.width) // 2, (1080 - im.height) // 2), im)
        r = _os.path.join(tempfile.gettempdir(), f"_mg_oro_nuevos_{i}.jpg")
        fondo.resize((960, 540)).save(r, quality=85)
        print(r, im.size)


if __name__ == "__main__" and len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "nuevos":
    _prueba_nuevos()
elif __name__ == "__main__":   # hoja de prueba: python mg_oro.py -> previews de cada MG en su cuadro final
    import os
    import numpy as np
    from PIL import Image
    pruebas = [
        factura("LO QUE CUESTA LLEGAR AL 60 MONTADO", [("inv_misc_book_09", "Entrenar del 1 al 60", 207),
                                                        ("ability_mount_ridinghorse", "Equitación de aprendiz", 100),
                                                        ("ability_dualwield", "Doble especialización", 50),
                                                        ("ability_mount_whitetiger", "Equitación de oficial", 1000),
                                                        ("ability_mount_nightmarehorse", "Montura épica", 200)], "TOTAL", "SIN FICHA"),
        desplome("HUEVO GIGANTE EN LA SUBASTA", [("7-nov", 100), ("9-nov", 67), ("10-nov", 49), ("12-nov", 31), ("13-nov", 18)],
                 "Lo que todos farmean se hunde en días", ico="inv_egg_02"),
        balanza("¿VENDEDOR O SUBASTA?", ("inv_misc_food_72", "Carne de tortuga"), ("Vendedor", "1 c", 1), ("Subasta", "20 p", 20),
                "Escanea antes de vender"),
        escalera("REESPECIALIZAR CONTRA DOBLE ESPECIALIZACIÓN", [("1.ª vez", "1 o"), ("2.ª vez", "5 o"), ("3.ª vez", "10 o"), ("y sube…", "+")],
                 ("Doble especialización", "50 o una vez"), "Cambiar después: gratis"),
        techo("EL TECHO DEL CRISTAL ARCANO", "inv_misc_gem_pearl_05", "Cristal Arcano", [("Lo vendió", 9), ("Días después", 12.5)],
              ("Mercado negro", 50), "Nunca vale más de 50"),
        dia_noche("LA HORA SÍ IMPORTA", "inv_misc_gem_pearl_04", "Perla de oro", "2 o 70 p", "5 o", "Publica por la mañana"),
    ]
    os.makedirs("../previews", exist_ok=True)
    hoja = []
    for fn in pruebas:
        a = fn(9.0, 10.0, [0.4, 1.2, 2.0, 2.8, 3.6, 4.4, 5.2])
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        fondo = Image.new("RGB", (im.width, im.height), (60, 80, 60))
        fondo.paste(im, (0, 0), im)
        hoja.append(fondo.resize((im.width // 2, im.height // 2)))
    W = max(i.width for i in hoja)
    H = sum(i.height for i in hoja)
    out = Image.new("RGB", (W, H), (30, 30, 30))
    y = 0
    for i in hoja:
        out.paste(i, (0, y))
        y += i.height
    out.save(os.path.join(os.environ.get("TEMP", "."), "_mg_oro_prueba.jpg"), quality=85)
    print("ok", out.size)
