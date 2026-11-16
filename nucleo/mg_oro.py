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


if __name__ == "__main__":   # hoja de prueba: python mg_oro.py -> previews de cada MG en su cuadro final
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
