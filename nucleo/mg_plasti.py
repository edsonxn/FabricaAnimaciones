# -*- coding: utf-8 -*-
"""MOTION GRAPHICS de Plastitube (secuencia Flow de plastilina; primer uso `lego_carpintero`, 3-nov-2026).
Estética de JUGUETE, coherente con la plastilina: piezas de colores con botones que caen y rebotan, letra redonda
(Arial Rounded), paneles oscuros translúcidos con esquinas muy redondeadas para no tapar la imagen de Flow.
    import mg_plasti as K
  linea(titulo, hitos, colores)     línea de tiempo: un ladrillo con el año cae por marca; texto debajo; `icono="fuego"` pone llama
  contador(valor, unidad, titulo)   cifra GRANDE que rueda sobre una placa amarilla con botones
  ladrillos(n, titulo, sub)         n ladrillos que caen y se apilan (combinaciones, pasos); uno por marca o solos
Todas son fn(dt, dur, marcas) -> BGRA (como los MG de la secuencia). Probar con `python fab.py <v> fx hoja`.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROJO, AMARILLO, AZUL, VERDE = (214, 32, 40), (255, 205, 0), (0, 108, 183), (0, 146, 72)
BLANCO, CREMA, TINTA = (255, 255, 255), (250, 244, 228), (34, 28, 24)
FUEGO = (255, 122, 24)
_F = "C:/Windows/Fonts/ARLRDBD.TTF"
_fc = {}


def fuente(tam):
    if tam not in _fc:
        _fc[tam] = ImageFont.truetype(_F, int(tam))
    return _fc[tam]


def _eo(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def _reb(x):
    """0→1 con rebote al caer (pelota de plastilina)."""
    x = max(0.0, min(1.0, x))
    if x < .6:
        return (x / .6) ** 2
    y = (x - .6) / .4
    return 1 - .16 * math.sin(math.pi * y) * (1 - y)


def _bgra(im):
    return np.array(im)[..., [2, 1, 0, 3]]


def _mezcla(c, k):
    return tuple(int(max(0, min(255, v * k))) for v in c)


def _txt(d, xy, s, f, col, anc="mm", a=255, sombra=True):
    if a <= 2:
        return
    if sombra:
        d.text((xy[0] + 3, xy[1] + 4), s, font=f, fill=(0, 0, 0, int(a * .55)), anchor=anc)
    d.text(xy, s, font=f, fill=tuple(col) + (int(a),), anchor=anc)


def _ajustar(s, tam, ancho):
    f = fuente(tam)
    while tam > 18 and _D.textlength(s, font=f) > ancho:
        tam -= 2
        f = fuente(tam)
    return f


_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))


def _panel(w, h, alfa=.55):
    M = 24
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((M, M + 8, M + w, M + h + 8), 46, fill=(0, 0, 0, int(120 * alfa)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(im).rounded_rectangle((M, M, M + w, M + h), 46, fill=(20, 16, 14, int(255 * alfa)))
    return im, M


def ladrillo(w, h, col, botones=None):
    """Pieza de juguete vista de frente: cuerpo con brillo arriba y sombra abajo, botones redondos encima."""
    n = botones or max(1, int(round(w / (h * .9))))
    rb = min(w / n * .30, h * .26)
    hb = rb * .9
    im = Image.new("RGBA", (w + 8, int(h + hb + 10)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y0 = int(hb)
    paso = w / n
    for i in range(n):                                  # botones (cilindros vistos de frente)
        cx = 4 + paso * (i + .5)
        d.rounded_rectangle((cx - rb, y0 - hb, cx + rb, y0 + 4), int(rb * .5), fill=_mezcla(col, .82) + (255,))
        d.ellipse((cx - rb, y0 - hb - rb * .35, cx + rb, y0 - hb + rb * .35), fill=_mezcla(col, 1.12) + (255,))
    d.rounded_rectangle((4, y0, 4 + w, y0 + h), int(h * .12), fill=col + (255,))
    d.rounded_rectangle((4, y0 + h * .70, 4 + w, y0 + h), int(h * .12), fill=_mezcla(col, .78) + (255,))
    d.rounded_rectangle((10, y0 + 5, w - 2, y0 + h * .22), int(h * .08), fill=_mezcla(col, 1.18) + (150,))
    return im


def _llama(r):
    im = Image.new("RGBA", (int(r * 2.4), int(r * 3.2)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = im.width / 2, im.height * .62
    for k, col in ((1.0, FUEGO), (.66, AMARILLO), (.34, CREMA)):
        rr = r * k
        d.ellipse((cx - rr, cy - rr * .9, cx + rr, cy + rr), fill=col + (255,))
        d.polygon([(cx - rr * .9, cy - rr * .2), (cx, cy - rr * 2.5), (cx + rr * .9, cy - rr * .2)], fill=col + (255,))
    return im.filter(ImageFilter.GaussianBlur(1.2))


def linea(titulo, hitos, colores=(ROJO, AMARILLO, AZUL, VERDE), icono=None, w=1500, h=470):
    """hitos = [(año, texto)]; marca k = el hito k: su ladrillo cae con rebote y aparece su texto. icono="fuego" = llama
    encima de cada ladrillo (los tres incendios)."""
    n = len(hitos)
    ft = _ajustar(titulo.upper(), 52, w - 120)
    fa = fuente(54)
    fx = fuente(30)
    paso = (w - 160) / max(1, n)
    bw, bh = int(min(paso * .72, 300)), 92
    bricks = [ladrillo(bw, bh, colores[i % len(colores)]) for i in range(n)]
    llama = _llama(26) if icono == "fuego" else None

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.58 * _eo(dt / .3))
        d = ImageDraw.Draw(im)
        _txt(d, (M + w / 2, M + 60), titulo.upper(), ft, CREMA, "mm", 255 * _eo((dt - .1) / .35))
        mk = list(marcas or [.5 + 1.1 * i for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + 1.1)
        ysuelo = M + 270
        x0 = M + 80
        d.rounded_rectangle((x0 - 20, ysuelo + 2, M + w - 60, ysuelo + 12), 5, fill=(255, 255, 255, int(70 * _eo(dt / .4))))
        for i, ((anio, texto), m) in enumerate(zip(hitos, mk)):
            if dt < m:
                continue
            u = _reb((dt - m) / .55)
            cx = x0 + paso * (i + .5)
            b = bricks[i]
            y = ysuelo - b.height - (1 - u) * 260
            im.alpha_composite(b, (int(cx - b.width / 2), int(y)))
            _txt(d, (cx, y + b.height - bh / 2 - 2), str(anio), fa, BLANCO if i % len(colores) != 1 else TINTA, "mm", 255,
                 sombra=i % len(colores) != 1)
            if llama is not None and u > .9:
                fl = llama.rotate(4 * math.sin((dt - m) * 9), resample=Image.BICUBIC)
                k = 1 + .08 * math.sin((dt - m) * 13)
                fl = fl.resize((int(fl.width * k), int(fl.height * k)))
                im.alpha_composite(fl, (int(cx - fl.width / 2), int(y - fl.height + 18)))
            if texto:
                a = 255 * _eo((dt - m - .25) / .35)
                lineas, cur = [], ""
                for p in texto.split():
                    if _D.textlength((cur + " " + p).strip(), font=fx) > paso - 24 and cur:
                        lineas.append(cur)
                        cur = p
                    else:
                        cur = (cur + " " + p).strip()
                lineas.append(cur)
                for j, s in enumerate(lineas[:3]):
                    _txt(d, (cx, ysuelo + 48 + j * 38), s, fx, CREMA, "mm", a)
        return _bgra(im)
    return fn


def contador(valor, unidad="", titulo="", desde=0, decimales=0, w=900, color=AMARILLO):
    """Cifra GRANDE que rueda de `desde` a `valor` sobre una placa de juguete con botones; título arriba, unidad abajo.
    Separador de miles con espacio fino (36 000 000 000)."""
    h = 330
    placa = ladrillo(w - 80, 190, color, botones=8)
    ft = _ajustar(titulo.upper(), 40, w - 60) if titulo else None
    fu = _ajustar(unidad.upper(), 44, w - 60) if unidad else None

    def fmt(v):
        s = f"{v:,.{decimales}f}".replace(",", " ").replace(".", ",")
        return s

    fv = _ajustar(fmt(valor), 120, w - 150)

    def fn(dt, dur, marcas):
        im, M = _panel(w, h + 70, alfa=.52 * _eo(dt / .3))
        d = ImageDraw.Draw(im)
        if ft:
            _txt(d, (M + w / 2, M + 44), titulo.upper(), ft, CREMA, "mm", 255 * _eo((dt - .05) / .3))
        u = _reb((dt - .1) / .6)
        py = int(M + 82 - (1 - u) * 120)
        im.alpha_composite(placa, (int(M + 40), py))
        k = _eo((dt - .35) / 1.1)
        v = desde + (valor - desde) * k
        tc = TINTA if color == AMARILLO else BLANCO
        _txt(d, (M + w / 2, py + placa.height - 96), fmt(v), fv, tc, "mm", 255 * _eo((dt - .3) / .2),
             sombra=color != AMARILLO)
        if fu:
            _txt(d, (M + w / 2, M + h + 30), unidad.upper(), fu, CREMA, "mm", 255 * _eo((dt - .9) / .3))
        return _bgra(im)
    return fn


def ladrillos(n, titulo="", sub="", colores=(ROJO, AMARILLO, AZUL, VERDE, ROJO, AMARILLO), w=1100, h=520):
    """n ladrillos de 2x4 que caen y se apilan en escalera (uno por marca, o cada 0,35 s); título arriba y `sub` al final."""
    bw, bh = 300, 96
    piezas = [ladrillo(bw, bh, colores[i % len(colores)], botones=4) for i in range(n)]
    ft = _ajustar(titulo.upper(), 50, w - 100) if titulo else None
    fs = _ajustar(sub.upper(), 56, w - 100) if sub else None

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.55 * _eo(dt / .3))
        d = ImageDraw.Draw(im)
        mk = list(marcas or [.3 + .35 * i for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + .35)
        base = M + h - 104
        pos, fila, quedan = [], 0, n                    # pirámide trabada: 3-2-1 (o la que salga con n)
        ancho_fila = max(1, int(math.ceil((math.sqrt(8 * n + 1) - 1) / 2)))
        while quedan > 0:
            k = min(quedan, ancho_fila - fila) or 1
            for j in range(k):
                pos.append((fila, j - (k - 1) / 2))
            quedan -= k
            fila += 1
        for i, m in enumerate(mk[:n]):
            if dt < m:
                continue
            u = _reb((dt - m) / .5)
            fila, col = pos[i]
            x = M + w / 2 - piezas[i].width / 2 + col * (bw + 6)
            y = base - piezas[i].height - fila * (bh + 2) - (1 - u) * 300
            im.alpha_composite(piezas[i], (int(x), int(y)))
        if ft:   # el título va encima: las piezas que caen pasaban por delante (lego_carpintero, 4-nov-2026)
            _txt(d, (M + w / 2, M + 52), titulo.upper(), ft, CREMA, "mm", 255 * _eo((dt - .05) / .3))
        if fs and dt > mk[min(n, len(mk)) - 1] + .4:
            _txt(d, (M + w / 2, M + h - 50), sub.upper(), fs, AMARILLO, "mm", 255 * _eo((dt - mk[n - 1] - .4) / .35))
        return _bgra(im)
    return fn
