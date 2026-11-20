# -*- coding: utf-8 -*-
"""MOTION GRAPHICS de RUTA DE NIVEL con la interfaz de WoW (panel azul noche y borde dorado de mg_wow), hechos para
«La RUTA del 1 al 60 en WoW Forever, zona por zona» (wow_ruta_forever, 19-nov-2026). Sirven a cualquier guía de subida de nivel.
CERO cifras inventadas: solo números que el guion dice. Uso en efectos.py igual que mg_wow (fn(dt, dur, marcas)).
  parada(n, a, b, titulo, alianza, horda)       tarjeta de capítulo: barra 1-60 que se llena hasta el tramo a-b, y dos columnas
                                                Alianza (azul) / Horda (rojo); marca 0 = tramo, 1 = Alianza, 2 = Horda
  curva_xp(titulo, puntos, sombra, nota)        experiencia acumulada por nivel (curva que se dibuja punto a punto) y la franja
                                                `sombra` (nivel a, nivel b) sombreada con su nota; marca k = punto k, len = franja
  bifurcacion(titulo, raiz, izq, der, remate)   un camino que se parte en dos: raíz abajo; rama izquierda (azul) y derecha (rojo),
                                                cada una con sus pasos; marca 0 = raíz, 1..n = pasos izq, luego pasos der, último = remate
"""
from PIL import ImageDraw

from mg_wow import BLANCO, GRIS, ORO, ORO_T, VERDE, _base, _eo, _mk, _pegar, _pop, _salida, _texto, fuente, icono

AZUL, ROJO_H = (70, 140, 255), (225, 50, 45)
ICO_A, ICO_H = "inv_bannerpvp_02", "inv_bannerpvp_01"   # estandartes JcJ de la Alianza y la Horda (Wowhead)


def _encaja(d, s, nombre, tam, ancho):
    """La fuente más grande (≤ tam) con la que `s` cabe en `ancho`."""
    while tam > 16 and d.textlength(s, font=fuente(nombre, tam)) > ancho:
        tam -= 2
    return fuente(nombre, tam)


def parada(n, a, b, titulo, alianza, horda, ancho=1500):
    """alianza/horda = listas cortas de zonas (≤ 4 cada una; None o [] = esa columna no sale)."""
    filas = max(len(alianza or []), len(horda or []), 1)
    h = 370 + filas * 46

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, f"PARADA {n}")
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        a0 = 255 * _eo(dt / .35)
        _texto(d, (cx, M + 108), titulo, _encaja(d, titulo, "negra", 50, ancho - 120), BLANCO, "mm", a0)
        # barra 1-60
        x0, x1, yb = M + 80, M + ancho - 80, M + 212
        d.rounded_rectangle((x0, yb - 13, x1, yb + 13), 12, fill=(6, 8, 22, 240), outline=ORO + (200,), width=2)
        for lv in (1, 10, 20, 30, 40, 50, 60):
            x = x0 + (x1 - x0) * (lv - 1) / 59
            d.line([(x, yb + 15), (x, yb + 24)], fill=GRIS + (200,), width=2)
            _texto(d, (x, yb + 40), str(lv), fuente("sans", 22), GRIS, "mm", 230)
        t0 = _mk(marcas, 0, .4)
        u = max(0.0, dt - t0)
        q = _eo(u / .9)
        xa = x0 + (x1 - x0) * (a - 1) / 59
        xb = x0 + (x1 - x0) * (b - 1) / 59
        if u > 0:
            d.rounded_rectangle((x0 + 2, yb - 10, max(x0 + 14, x0 + (xa - x0) * q), yb + 10), 10, fill=(120, 100, 40, 200))
            if q > .6:
                k = _eo((u - .55) / .5)
                d.rounded_rectangle((xa, yb - 12, xa + max(12, (xb - xa) * k), yb + 12), 11, fill=ORO_T + (255,))
                _texto(d, ((xa + xb) / 2, yb - 36), f"nivel {a}-{b}", fuente("negra", 30), ORO_T, "mm", 255 * k)
        # columnas Alianza / Horda
        yc = M + 302
        for i, (lista, col, ico, nom) in enumerate(((alianza, AZUL, ICO_A, "ALIANZA"), (horda, ROJO_H, ICO_H, "HORDA"))):
            if not lista:
                continue
            ti = _mk(marcas, 1 + i, t0 + 1.2 + i * .9)
            if dt < ti:
                continue
            ui = dt - ti
            xc = M + ancho * (.27 if i == 0 else .73)
            _pegar(im, icono(ico, 46), xc - 120, yc, _pop(ui))
            d = ImageDraw.Draw(im)
            _texto(d, (xc - 88, yc), nom, fuente("negra", 32), col, "lm", 255 * _eo(ui / .3))
            for j, z in enumerate(lista):
                uj = ui - .15 - j * .12
                if uj <= 0:
                    continue
                _texto(d, (xc, yc + 50 + j * 46), z, _encaja(d, z, "sans", 30, ancho * .42), BLANCO, "mm", 255 * _eo(uj / .3))
        return _salida(im, dt)
    return fn


def curva_xp(titulo, puntos, sombra=None, nota=None, ancho=1500):
    """puntos = [(nivel, experiencia_acumulada), ...] (el primero puede ser (1, 0)); sombra = (nivel_a, nivel_b)."""
    h = 600
    ymax = max(v for _, v in puntos)
    lmax = max(lv for lv, _ in puntos)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        gx0, gx1, gy0, gy1 = M + 130, M + ancho - 90, M + 110, M + h - 110

        def X(lv):
            return gx0 + (gx1 - gx0) * (lv - 1) / (lmax - 1)

        def Y(v):
            return gy1 - (gy1 - gy0) * v / ymax
        n = len(puntos)
        ts = _mk(marcas, n, 1e9)
        if sombra and dt >= ts:
            u = dt - ts
            k = _eo(u / .6)
            xa, xb = X(sombra[0]), X(sombra[1])
            d.rectangle((xa, gy0, xa + (xb - xa) * k, gy1), fill=(255, 209, 0, 46))
            d.line([(xa, gy0), (xa, gy1)], fill=ORO_T + (180,), width=2)
            if nota:
                _texto(d, ((xa + xb) / 2, gy0 + 40), nota, fuente("negra", 46), ORO_T, "mm", 255 * _eo((u - .3) / .4))
        for k in range(5):
            y = gy0 + (gy1 - gy0) * k / 4
            d.line([(gx0, y), (gx1, y)], fill=(90, 90, 120, 90), width=1)
        d.line([(gx0, gy0 - 10), (gx0, gy1)], fill=ORO + (200,), width=3)
        d.line([(gx0, gy1), (gx1 + 20, gy1)], fill=ORO + (200,), width=3)
        for lv in (1, 10, 20, 30, 40, 50, 60):
            if lv <= lmax:
                _texto(d, (X(lv), gy1 + 30), str(lv), fuente("sans", 24), GRIS, "mm", 230)
        _texto(d, (gx1, gy1 + 66), "nivel", fuente("sans", 22), GRIS, "rm", 200)
        xy = [(X(lv), Y(v)) for lv, v in puntos]
        ult = -1
        for k in range(n):
            tk = _mk(marcas, k, .4 + k * .5)
            if dt < tk:
                break
            if k > 0:
                q = _eo((dt - tk) / .45)
                (xa, ya), (xb, yb) = xy[k - 1], xy[k]
                pasos = 14
                pts = []
                for s in range(pasos + 1):           # tramo curvo (sube más al final, como la experiencia)
                    f = s / pasos * q
                    pts.append((xa + (xb - xa) * f, ya + (yb - ya) * f ** 1.6))
                d.line(pts, fill=VERDE + (255,), width=6)
            ult = k
        for k in range(ult + 1):
            u = dt - _mk(marcas, k, .4 + k * .5)
            x, y = xy[k]
            r = 10 * _pop(u)
            d.ellipse((x - r, y - r, x + r, y + r), fill=ORO_T + (255,), outline=(20, 10, 0, 255), width=3)
            v = puntos[k][1]
            if v:
                s = f"{v:,}".replace(",", " ")
                _texto(d, (x - 14, y - 26), s, fuente("negra", 26 if k == n - 1 else 22), ORO_T if k == n - 1 else BLANCO, "rm",
                       255 * _eo(u / .3))
        return _salida(im, dt)
    return fn


def bifurcacion(titulo, raiz, izq, der, remate=None, ancho=1500):
    """raiz = texto; izq/der = (rótulo, [paso, ...]) con ≤ 4 pasos cada una (izq = Alianza azul, der = Horda roja)."""
    pasos = max(len(izq[1]), len(der[1]))
    h = 250 + pasos * 92 + (70 if remate else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        yr = M + h - (120 if remate else 60)
        t0 = _mk(marcas, 0, .4)
        if dt >= t0:
            u = dt - t0
            w = d.textlength(raiz, font=fuente("negra", 32)) / 2 + 30
            d.rounded_rectangle((cx - w, yr - 30, cx + w, yr + 30), 14, fill=(30, 26, 10, 240), outline=ORO_T + (255,), width=3)
            _texto(d, (cx, yr), raiz, fuente("negra", 32), ORO_T, "mm", 255 * _eo(u / .3))
        k = 1
        for lado, (rot, lista), col, ico in ((-1, izq, AZUL, ICO_A), (1, der, ROJO_H, ICO_H)):
            xr = cx + lado * ancho * .27
            ytop = M + 112
            tl = _mk(marcas, k, t0 + .8)
            if dt >= tl:
                u = dt - tl
                q = _eo(u / .6)
                # tronco que sube desde la raíz y se abre hacia su columna
                ym = yr - 30 - (yr - 30 - ytop - 40) * .25
                pts = [(cx, yr - 30), (cx + (xr - cx) * q, yr - 30 - (yr - 30 - ym) * q)]
                d.line(pts, fill=col + (255,), width=8)
                if q >= 1:
                    d.line([(xr, ym), (xr, ytop + 40)], fill=col + (140,), width=5)
                _pegar(im, icono(ico, 44), xr - d.textlength(rot, font=fuente("negra", 34)) / 2 - 36, ytop, _pop(u))
                d = ImageDraw.Draw(im)
                _texto(d, (xr + 10, ytop), rot, fuente("negra", 34), col, "mm", 255 * _eo(u / .3))
            for j, p in enumerate(lista):
                tj = _mk(marcas, k + j, tl + .6 + j * .7)
                if dt < tj:
                    continue
                u = dt - tj
                yj = ytop + 78 + j * 92
                f = _encaja(d, p, "sans", 30, ancho * .40)
                w = d.textlength(p, font=f) / 2 + 26
                s = _pop(u)
                d.rounded_rectangle((xr - w * s, yj - 30, xr + w * s, yj + 30), 12, fill=(8, 10, 28, 245), outline=col + (255,), width=3)
                _texto(d, (xr, yj), p, f, BLANCO, "mm", 255 * _eo((u - .1) / .3))
            k += len(lista)
        tr = _mk(marcas, k, 1e9)
        if remate and dt >= tr:
            _texto(d, (cx, M + h - 42), remate, fuente("serif", 34), VERDE, "mm", 255 * _eo((dt - tr) / .3))
        return _salida(im, dt)
    return fn


if __name__ == "__main__":
    import os
    import tempfile

    import numpy as np
    from PIL import Image
    fondo = Image.new("RGB", (1920, 1080), (40, 70, 50))
    pruebas = [
        (parada(8, 36, 45, "CLAROS DEL RÍO, LA ZONA NUEVA", ["a pie desde Villa del Lago", "Fortaleza de Farholde"],
                ["barco desde Tanaris", "Puerto Polvomecha", "Rog'mar"]), [0.3, 1.5, 2.5], 4.5),
        (curva_xp("EXPERIENCIA PARA LLEGAR AL 60", [(1, 0), (10, 27600), (20, 167200), (30, 499000), (40, 1154400), (50, 2306100),
                                                   (60, 4084700)], (30, 60), "88 %"), [.2, .5, .8, 1.1, 1.4, 1.7, 2.0, 2.6], 4.5),
        (bifurcacion("AL 36, LA RUTA SE PARTE EN DOS", "nivel 36 · Claros del Río",
                     ("ALIANZA · a pie", ["Villa del Lago", "Colinas Espinosas", "Fortaleza de Farholde"]),
                     ("HORDA · en barco", ["muelle de Tanaris", "Puerto Polvomecha", "Rog'mar"]), "Dos caminos, una zona"),
         [.3, 1, 1.5, 2, 2.5, 3, 3.5, 4.2], 5.5),
    ]
    for i, (fn, marcas, t) in enumerate(pruebas):
        a = fn(t, 8, marcas)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        f = fondo.copy()
        f.paste(im, ((1920 - im.width) // 2, (1080 - im.height) // 2), im)
        r = os.path.join(tempfile.gettempdir(), f"_mg_ruta_prueba{i}.jpg")
        f.resize((960, 540)).save(r, quality=85)
        print(r)
