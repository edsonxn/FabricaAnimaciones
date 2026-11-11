# -*- coding: utf-8 -*-
"""Formas nuevas de presentar una pelea de LoL (el usuario, 10-nov-2026: «probemos nuevas formas y más dinámicas»,
`videos/lol_final_previa/`). Mismo lenguaje visual que `mg_lol` (vidrio azul noche, filo dorado, Bahnschrift).
Cada pieza devuelve fn(dt, dur, marcas) -> BGRA para el FX `mg` del motor secuencia (marcas = s desde el inicio del FX).

  marcador_pelea(izq, der, muertes, titulo)   forma 4 · barra tipo NFL al pie: 5 retratos por lado; en cada marca el retrato
                                              del que cae se agrieta, pasa a gris con un tajo rojo y el marcador «3 - 0» rebota
  oro_vivo(titulo, serie, claves, azul, rojo, notas)
                                              forma 5 · la diferencia de oro del feed oficial (cada 10 s) se dibuja en vivo
                                              sincronizada con la voz: claves[i] = segundo de juego al que llega la línea en
                                              la marca i; color por signo (azul arriba / rojo abajo), cifra grande que rebota
Datos: SOLO del feed oficial livestats (videos/<v>/investigacion/oro_<id>.json) y del kill feed del VOD.
"""
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

from mg_lol import (COL, ORO, ORO_C, _brillo_barrido, _c, _centro, _eo, _img, _mk, _np, _panel, _perspectiva, _pop, _sello,
                    _sobre, _texto, _vacio, fuente)

_cache = {}


def _circulo(foto, r, color, gris=False):
    """retrato redondo con aro del color del equipo (RGBA PIL)"""
    tam = 2 * r + 12
    im = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((4, 8, tam - 2, tam), fill=(0, 0, 0, 120))
    d.ellipse((6, 6, tam - 6, tam - 6), fill=(14, 22, 40, 255))
    try:
        f = _img(foto, alto=int(2.25 * r), gris=gris)
        cx = (tam - f.width) // 2
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).ellipse((9, 9, tam - 9, tam - 9), fill=255)
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        capa.alpha_composite(f, (cx, int(tam * .08)))
        capa.putalpha(Image.fromarray(np.minimum(np.array(capa)[..., 3], np.array(m))))
        im.alpha_composite(capa)
    except Exception:
        pass
    col = (90, 92, 100) if gris else _c(color)
    d.ellipse((6, 6, tam - 6, tam - 6), outline=col + (255,), width=5)
    return im


def _grietas(arr, cx, cy, r, u, semilla):
    """líneas de grieta que crecen desde el centro del retrato (u 0..1)"""
    if u <= 0:
        return
    rnd = np.random.RandomState(semilla)
    for k in range(7):
        a = rnd.uniform(0, 2 * math.pi)
        x, y = cx, cy
        largo = r * rnd.uniform(.7, 1.05) * u
        pasos = 4
        for _ in range(pasos):
            a += rnd.uniform(-.5, .5)
            nx, ny = x + math.cos(a) * largo / pasos, y + math.sin(a) * largo / pasos
            cv2.line(arr, (int(x), int(y)), (int(nx), int(ny)), (235, 240, 255, 255), 2, cv2.LINE_AA)
            x, y = nx, ny


def marcador_pelea(izq, der, muertes, titulo="LA PELEA", r=46):
    """izq/der = dict(logo, cod, color, jugadores=[(nombre, foto), …5]); muertes = [("izq"|"der", índice), …] en el orden de
    las marcas (marca i = cae muertes[i]). Marca 0 de la lista NO es la entrada: la barra entra al empezar el FX."""
    n = 5
    paso = 2 * r + 34
    lado_w = 110 + n * paso
    W_ = 2 * lado_w + 260
    H_ = 2 * r + 120
    k = ("mpel", izq["cod"], der["cod"], tuple(j[0] for j in izq["jugadores"] + der["jugadores"]), r, titulo)
    if k not in _cache:
        panel, P = _panel(W_ - 60, H_ - 60, "oro", sesgo=16)
        caras = {}
        for lado, eq in (("izq", izq), ("der", der)):
            for i, (nom, foto) in enumerate(eq["jugadores"]):
                caras[(lado, i, 0)] = _np(_circulo(foto, r, eq["color"]))
                caras[(lado, i, 1)] = _np(_circulo(foto, r, eq["color"], gris=True))
        fija = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(fija)
        fn_ = fuente("SemiBold Condensed", 22)
        for lado, eq in (("izq", izq), ("der", der)):
            lg = _img(eq["logo"], alto=74, ancho=84)
            xl = 30 + 18 if lado == "izq" else W_ - 30 - 18 - lg.width
            fija.alpha_composite(lg, (xl, int(H_ / 2 - lg.height / 2 - 6)))
            for i, (nom, _) in enumerate(eq["jugadores"]):
                cx = _cx(lado, i, W_, lado_w, paso)
                _texto(d, (cx, H_ / 2 + r + 18), nom.upper(), fn_, (235, 235, 240), "mm", track=1)
        _texto(d, (W_ / 2, 50), titulo.upper(), fuente("Bold Condensed", 24), ORO_C, "mm", track=4)
        _cache[k] = (_np(panel), P, caras, _np(fija))
    panel, P, caras, fija = _cache[k]

    def fn(dt, dur, marcas):
        out = _vacio(W_, H_)
        u = _eo(dt / .45)
        if u <= 0:
            return out
        cw = int(W_ * u)
        out[:, :cw] = 0
        pa = panel.copy()
        pa[:, int(pa.shape[1] * u):] = 0
        _sobre(out, pa, 0, 0)
        _sobre(out, fija, 0, int(14 * (1 - u)), u)
        cuenta = {"izq": 0, "der": 0}
        for lado in ("izq", "der"):
            for i in range(n):
                cx = _cx(lado, i, W_, lado_w, paso)
                cy = H_ / 2 - 4
                ui = _pop(dt - .15 - .06 * i, .4)
                if ui <= .02:
                    continue
                tk = next((_mk(marcas, j, 99) for j, m in enumerate(muertes) if m == (lado, i)), 99)
                caido = dt >= tk
                if caido:
                    cuenta["der" if lado == "izq" else "izq"] += 1
                tem = 7 * math.exp(-(dt - tk) * 9) * math.sin((dt - tk) * 60) if caido else 0
                cara = caras[(lado, i, 1 if caido and dt - tk > .1 else 0)]
                _centro(out, cara, cx + tem, cy + 2 * math.sin(dt * 1.7 + i), clamp01(ui))
                if caido:
                    _grietas(out, cx, cy, r, _eo((dt - tk) / .25), hash((lado, i)) % 997)
                    v = _eo((dt - tk - .08) / .16)
                    x1, y1 = cx - r * .8, cy - r * .8
                    cv2.line(out, (int(x1), int(y1)), (int(x1 + 1.6 * r * v), int(y1 + 1.6 * r * v)), (60, 50, 255, 255), 9,
                             cv2.LINE_AA)
                    if dt - tk < .5:                        # destello al caer
                        a = 1 - (dt - tk) / .5
                        cv2.circle(out, (int(cx), int(cy)), int(r * (1 + .8 * (1 - a))), (120, 120, 255, int(200 * a)), 4,
                                   cv2.LINE_AA)
        # marcador central (golpe al cambiar)
        txt = f"{cuenta['izq']} - {cuenta['der']}"
        ult = max([_mk(marcas, j, -9) for j in range(len(muertes)) if _mk(marcas, j, 99) <= dt] or [-9])
        esc = 1 + .35 * math.exp(-(dt - ult) * 7) if dt - ult < 1 else 1
        tim = Image.new("RGBA", (240, 120), (0, 0, 0, 0))
        _texto(ImageDraw.Draw(tim), (120, 60), txt, fuente("Bold Condensed", 76), (255, 255, 255), "mm")
        _centro(out, _np(tim), W_ / 2, H_ / 2 + 8, esc * u)
        out = _brillo_barrido(out, (dt - .4) / .6)
        return _perspectiva(out, 4 * (1 - _eo(dt / .6)) + .8 * math.sin(dt * 1.2))

    return fn


def clamp01(x):
    return max(0.0, min(1.0, x))


def _cx(lado, i, W_, lado_w, paso):
    if lado == "izq":
        return 30 + 120 + paso / 2 + i * paso
    return W_ - 30 - 120 - paso / 2 - (4 - i) * paso


def _k(v):
    s = f"{abs(v) / 1000:.1f}".replace(".", ",")
    return ("+" if v >= 0 else "-") + s + "K"


def oro_vivo(titulo, serie, claves, azul, rojo, notas=(), W_=900, H_=470, rango=None):
    """serie = [(seg_juego, dif_azul_menos_rojo)] del feed; claves = segundo de juego que alcanza la línea en cada marca
    (antes de la marca 0 la línea llega hasta claves[0] en 0,8 s); azul/rojo = (logo, cod); notas = [(seg, «texto»)]
    que aparecen cuando la línea pasa por ahí (un punto y una etiqueta corta)."""
    g0, g1 = serie[0][0], serie[-1][0]
    vals = [v for _, v in serie]
    m = rango or max(1000, max(abs(min(vals)), abs(max(vals))) * 1.15)
    PX, PY0, PY1 = (110, W_ - 60), 120, H_ - 70
    k = ("oro", titulo, len(serie), g0, g1, W_, H_, azul[1], rojo[1])
    if k not in _cache:
        panel, P = _panel(W_ - 60, H_ - 60, "oro", sesgo=12)
        fija = Image.new("RGBA", (W_ + 2 * P - 60, H_ + 2 * P - 60), (0, 0, 0, 0))
        d = ImageDraw.Draw(fija)
        ox, oy = P - 30, P - 30
        _texto(d, (ox + 70, oy + 62), titulo.upper(), fuente("Bold Condensed", 34), ORO_C, "lm", track=2)
        y0 = oy + _y(0, m, PY0, PY1)
        d.line([(ox + PX[0], y0), (ox + PX[1], y0)], fill=(255, 255, 255, 90), width=2)
        for gm in range(int(g0 // 60) + 1, int(g1 // 60) + 1):
            x = ox + PX[0] + (PX[1] - PX[0]) * (gm * 60 - g0) / (g1 - g0)
            d.line([(x, oy + PY0), (x, oy + PY1)], fill=(255, 255, 255, 22), width=1)
            if gm % 2 == 0:
                _texto(d, (x, oy + PY1 + 22), f"{gm}:00", fuente("SemiBold Condensed", 20), (170, 175, 190), "mm")
        for (lg, cod), yy, col in ((azul, oy + PY0 + 20, "azul"), (rojo, oy + PY1 - 20, "rojo")):
            im = _img(lg, alto=40, ancho=48)
            fija.alpha_composite(im, (ox + 22, int(yy - im.height / 2)))
            _texto(d, (ox + 76, yy), cod, fuente("Bold Condensed", 22), _c(col), "lm")
        _cache[k] = (_np(panel), _np(fija), P)
    panel, fija, P = _cache[k]
    ox, oy = P - 30, P - 30
    xs = np.array([PX[0] + (PX[1] - PX[0]) * (g - g0) / (g1 - g0) for g, _ in serie]) + ox
    ys = np.array([_y(v, m, PY0, PY1) for _, v in serie]) + oy
    y0 = oy + _y(0, m, PY0, PY1)

    def g_en(dt, marcas):
        t0 = _mk(marcas, 0, .9)
        if dt < t0:
            return g0 + (claves[0] - g0) * _eo(dt / max(t0, .1))
        for i in range(len(claves) - 1):
            a, b = _mk(marcas, i, 99), _mk(marcas, i + 1, 99)
            if a <= dt < b:
                return claves[i] + (claves[i + 1] - claves[i]) * clamp01((dt - a) / max(b - a, .1))
        return claves[-1]

    def fn(dt, dur, marcas):
        out = _vacio(panel.shape[1], panel.shape[0])
        u = _eo(dt / .45)
        if u <= 0:
            return out
        pa = panel.copy()
        pa[:, int(pa.shape[1] * u):] = 0
        _sobre(out, pa, 0, 0)
        _sobre(out, fija, 0, 0, u)
        g = g_en(dt, marcas)
        idx = int(np.searchsorted([s[0] for s in serie], g))
        pts = [(xs[i], ys[i]) for i in range(min(idx, len(serie)))]
        if 0 < idx < len(serie):
            q = (g - serie[idx - 1][0]) / max(serie[idx][0] - serie[idx - 1][0], 1e-3)
            pts.append((xs[idx - 1] + (xs[idx] - xs[idx - 1]) * q, ys[idx - 1] + (ys[idx] - ys[idx - 1]) * q))
        if len(pts) >= 2:
            # relleno hasta el cero, por signo
            capa = np.zeros_like(out)
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                arriba = (ya + yb) / 2 < y0
                col = COL["azul"] if arriba else COL["rojo"]
                poly = np.array([[xa, ya], [xb, yb], [xb, y0], [xa, y0]], np.int32)
                cv2.fillPoly(capa, [poly], col[::-1] + (70,), cv2.LINE_AA)
            _sobre(out, capa, 0, 0)
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                arriba = (ya + yb) / 2 < y0
                col = COL["azul"] if arriba else COL["rojo"]
                cv2.line(out, (int(xa), int(ya)), (int(xb), int(yb)), col[::-1] + (255,), 5, cv2.LINE_AA)
            xe, ye = pts[-1]
            lat = .5 + .5 * math.sin(dt * 8)
            cv2.circle(out, (int(xe), int(ye)), int(9 + 4 * lat), (255, 255, 255, 255), -1, cv2.LINE_AA)
            # cifra actual
            v = np.interp(g, [s[0] for s in serie], vals)
            cod = azul[1] if v >= 0 else rojo[1]
            col = COL["azul"] if v >= 0 else COL["rojo"]
            tim = Image.new("RGBA", (360, 90), (0, 0, 0, 0))
            dd = ImageDraw.Draw(tim)
            _texto(dd, (350, 45), f"{_k(abs(v))} {cod}", fuente("Bold Condensed", 54), col, "rm")   # siempre «+X K» del que va arriba (11-nov)
            _sobre(out, _np(tim), int(ox + W_ - 60 - 360 - 10), int(oy + 32))
            for i_, (gn, txt) in enumerate(notas):
                if g >= gn:
                    xn = float(np.interp(gn, [s[0] for s in serie], xs))
                    yn = float(np.interp(gn, [s[0] for s in serie], ys))
                    cv2.circle(out, (int(xn), int(yn)), 8, (10, 214, 255, 255), -1, cv2.LINE_AA)
                    ti = Image.new("RGBA", (260, 44), (0, 0, 0, 0))
                    _texto(ImageDraw.Draw(ti), (130, 22), txt.upper(), fuente("Bold Condensed", 24), (255, 214, 10), "mm")
                    yy = yn - 30 if i_ % 2 == 0 else yn + 30
                    _centro(out, _np(ti), xn + (-70 if i_ % 2 == 0 else 70), yy, 1.0, 1.0)
        out = _brillo_barrido(out, (dt - .4) / .6)
        return _perspectiva(out, 5 * (1 - _eo(dt / .6)) + 1.0 * math.sin(dt * 1.1))

    return fn


def _y(v, m, PY0, PY1):
    mid = (PY0 + PY1) / 2
    return mid - (v / m) * (PY1 - PY0) / 2
