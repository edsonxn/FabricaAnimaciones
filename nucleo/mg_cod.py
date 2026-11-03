# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS con la interfaz de CALL OF DUTY: MODERN WARFARE (Expediente 141; primer uso `cod_mw4_secretos`,
2-nov-2026). Regla de canal: fichas translúcidas con la interfaz de CADA juego, nunca carteles opacos que tapen el video.
La interfaz aquí es la del reboot de Modern Warfare (2019-2026):
  - texto TÁCTICO en condensada (Bahnschrift) blanca, acentos ÁMBAR (marcadores de objetivo) y verde de visión nocturna;
  - paneles de cristal oscuro con esquinas en ESCUADRA (no cajas cerradas), líneas finas y retícula de escaneo;
  - la ENTRADA DE MISIÓN de la saga: líneas que se escriben letra a letra en monoespaciada con el cursor que parpadea
    (lugar, hora, nombre) — aquí es el rótulo de cada puesto con su número de expediente;
  - el sello rojo CLASIFICADO del canal (Expediente 141).
    import mg_cod as C
  ficha(titulo, texto, tipo)          panel táctico: cabecera ámbar en mono, título, texto que se escribe; *x* = ámbar
  puesto(num, titulo, sub)            entrada de misión: «EXPEDIENTE 25/25», título y misión/lugar con cursor
  fallida(titulo, motivo)             pantalla de MISIÓN FALLIDA: viñeta roja, título y el motivo del juego
  logro(nombre, desc)                 aviso de LOGRO DESBLOQUEADO (arriba, compacto)
  radio(indicativo, texto, origen)    transmisión de radio con onda que vibra
  codigo(digitos, titulo)             teclado de la caja fuerte: los dígitos entran uno por marca (o solos)
  sello(texto, sub)                   sello rojo CLASIFICADO que cae y se estampa
  linea(titulo, hitos)                línea de tiempo con años; un hito por marca; el último en ámbar
  espejo(titulo, izq, der, centro)    dos columnas enfrentadas (2007 | 2026) con un vínculo al centro; una columna por marca
  balanza(titulo, filas)              «lo que se permite / lo que se castiga»: filas con ✓ verde o ✗ rojo; una por marca
  pegatina(ruta, titulo, tam)         imagen REAL con borde blanco; nombre en placa táctica con filo ámbar
Probar SIEMPRE con una hoja de cuadros antes de `fx`.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mg_gaming as G

BLANCO, HUESO = (244, 244, 238), (214, 210, 196)
AMBAR, VERDE, ROJO = (246, 190, 52), (130, 255, 150), (226, 54, 46)
GRIS, OSCURO = (150, 156, 160), (8, 11, 12)
_fc = {}
_eo, _reb, _escala = G._eo, G._reb, G._escala
_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
_F = {"b": "C:/Windows/Fonts/bahnschrift.ttf", "m": "C:/Windows/Fonts/consola.ttf", "mb": "C:/Windows/Fonts/consolab.ttf",
      "i": "C:/Windows/Fonts/impact.ttf"}


def fuente(estilo, tam, peso=None):
    """«b» Bahnschrift (variable: peso 'Bold'/'SemiBold'/'Condensed Bold'), «m» Consolas, «mb» Consolas negrita, «i» Impact."""
    k = (estilo, int(tam), peso)
    if k not in _fc:
        f = ImageFont.truetype(_F[estilo], int(tam))
        if estilo == "b":
            try:
                f.set_variation_by_name(peso or "SemiBold Condensed")
            except Exception:
                pass
        _fc[k] = f
    return _fc[k]


def _bgra(im, alfa=1.0):
    return G._bgra(im, max(0.0, min(1.0, alfa)))


def _ancho(s, f):
    return _D.textlength(s.replace("*", ""), font=f)


def _txt(d, xy, s, f, color, ancla="la", alfa=255, track=0):
    a = int(max(0, min(255, alfa)))
    if a <= 0 or not s:
        return
    if track:
        x = xy[0]
        tot = sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)
        if ancla[0] == "m":
            x -= tot / 2
        elif ancla[0] == "r":
            x -= tot
        for c in s:
            _txt(d, (x, xy[1]), c, f, color, "l" + ancla[1], alfa)
            x += d.textlength(c, font=f) + track
        return
    d.text((xy[0] + 2, xy[1] + 2), s, font=f, fill=(0, 0, 0, int(a * .6)), anchor=ancla)
    d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla)


def ajustar(s, estilo, tam, ancho, minimo=14, peso=None):
    while tam > minimo and _ancho(s, fuente(estilo, tam, peso)) > ancho:
        tam -= 1
    return fuente(estilo, tam, peso)


def caja(s, estilo, tam, ancho, alto=10_000, interlinea=1.3, minimo=16, max_lineas=7, peso=None):
    while True:
        f = fuente(estilo, tam, peso)
        ls = G._partir(_D, s, f, ancho)
        lh = tam * interlinea
        if (len(ls) * lh <= alto and len(ls) <= max_lineas and max(_ancho(x, f) for x in ls) <= ancho) or tam <= minimo:
            return f, ls, lh
        tam -= 1


def _cristal(w, h, M=40, alfa=.62):
    """Panel de cristal oscuro (borde difuminado) con retícula de escaneo muy tenue."""
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rectangle((M, M, M + w, M + h), fill=int(255 * alfa))
    m = m.filter(ImageFilter.GaussianBlur(9))
    capa = Image.new("RGBA", im.size, OSCURO + (255,))
    capa.putalpha(m)
    im.alpha_composite(capa)
    d = ImageDraw.Draw(im)
    for y in range(M + 4, M + h, 4):                       # líneas de escaneo
        d.line([(M, y), (M + w, y)], fill=(255, 255, 255, 7))
    return im, M


def _escuadras(d, x0, y0, x1, y1, alfa=255, L=34, color=BLANCO, ancho=3):
    """Las cuatro esquinas en escuadra (marco de retícula), sin cerrar la caja."""
    a = int(alfa)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(x, y), (x + sx * L, y)], fill=color + (a,), width=ancho)
        d.line([(x, y), (x, y + sy * L)], fill=color + (a,), width=ancho)


def _rica(d, x, y, s, f, color, resalte, alfa, ancla="l", hasta=None):
    """Línea con *resaltado*; `hasta` = caracteres visibles (máquina de escribir)."""
    trozos = s.split("*")
    tot = sum(d.textlength(t, font=f) for t in trozos)
    if ancla == "m":
        x -= tot / 2
    vis = 10 ** 9 if hasta is None else hasta
    for k, t in enumerate(trozos):
        if vis <= 0:
            break
        t2 = t[:max(0, int(vis))]
        if t2:
            _txt(d, (x, y), t2, f, resalte if k % 2 else color, "lm", alfa)
        x += d.textlength(t, font=f)
        vis -= len(t)


def _salida(im, dt, dur, abre=.28):
    """Entrada táctica: el panel se despliega en horizontal desde el centro con un parpadeo; salida con fundido."""
    u = _eo(dt / abre)
    if u < 1:
        W, H = im.size
        w = max(2, int(W * (.08 + .92 * u)))
        p = im.resize((w, H), Image.BICUBIC)
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        out.alpha_composite(p, ((W - w) // 2, 0))
        im = out
    parp = .55 if .12 < dt < .17 else 1.0
    return _bgra(im, min(_eo(dt / .15), (dur - dt) / .35) * parp)


def _cursor(dt):
    return (dt * 2.2) % 1 < .55


# ------------------------------------------------------------------ ficha = panel táctico de intel
def ficha(titulo, texto, tipo=None, ancho=880, vel=60):
    """Panel táctico: cabecera ámbar en monoespaciada (`tipo`, p. ej. «INTEL / CAMPAÑA»), título en condensada blanca
    con barra ámbar, y el texto que se ESCRIBE letra a letra. *x* = ámbar."""
    in_w = ancho - 2 * 44
    fcab = fuente("mb", 24)
    ft = ajustar(titulo.upper(), "b", 46, in_w, peso="Bold Condensed")
    fx, ls, lh = caja(texto, "b", 34, in_w, max_lineas=7, peso="SemiLight Condensed")
    h = int(30 + 34 + 56 + 22 + lh * len(ls) + 34)
    base, M = _cristal(ancho, h)
    letras = [len(x.replace("*", "")) for x in ls]
    cab = (tipo or "INTEL / EXPEDIENTE 141").upper()

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + ancho, M + h, 230 * _eo(dt / .3))
        x = M + 44
        y = M + 34
        d.rectangle((x, y - 12, x + 10, y + 12), fill=AMBAR + (int(255 * _eo((dt - .1) / .2)),))
        cab_vis = cab[:int(max(0, (dt - .15) * 70))]
        _txt(d, (x + 22, y), cab_vis + ("_" if _cursor(dt) and len(cab_vis) < len(cab) else ""), fcab, AMBAR, "lm", 255)
        y += 52
        _txt(d, (x, y), titulo.upper(), ft, BLANCO, "lm", 255 * _eo((dt - .25) / .3), track=1)
        y += 36
        k = _eo((dt - .3) / .4)
        d.line([(x, y), (x + in_w * k, y)], fill=AMBAR + (200,), width=2)
        y += 22 + lh / 2
        quedan = max(0.0, (dt - .45) * vel)
        for ln, n in zip(ls, letras):
            _rica(d, x, y, ln, fx, HUESO, AMBAR, 255, "l", hasta=quedan)
            quedan -= n
            y += lh
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ puesto = entrada de misión
def puesto(num, titulo, sub=None, total=25):
    """Entrada de misión de Modern Warfare: tres líneas que se escriben en monoespaciada con el cursor que parpadea
    («EXPEDIENTE 25/25», el título grande en condensada, y `sub` = misión / lugar), sobre una franja de cristal."""
    w = 1300
    l1 = f"EXPEDIENTE {num:02d}/{total}"
    f1 = fuente("mb", 34)
    f2 = ajustar(titulo.upper(), "b", 92, w - 120, peso="Bold Condensed")
    f3 = ajustar(sub or "", "m", 32, w - 120)
    h = 250 if sub else 200

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.55)
        d = ImageDraw.Draw(im)
        x = M + 60
        d.rectangle((M + 24, M + 34, M + 30, M + h - 34), fill=AMBAR + (int(255 * _eo(dt / .3)),))
        v1 = l1[:int(max(0, dt * 40))]
        _txt(d, (x, M + 52), v1, f1, AMBAR, "lm", 255, track=3)
        t2 = max(0.0, dt - .35)
        v2 = titulo.upper()[:int(t2 * 34)]
        _txt(d, (x, M + 128), v2, f2, BLANCO, "lm", 255, track=2)
        fin = len(v2) >= len(titulo)
        if sub:
            t3 = max(0.0, dt - .35 - len(titulo) / 34 - .1)
            v3 = sub[:int(t3 * 45)]
            _txt(d, (x, M + 206), v3, f3, HUESO, "lm", 235)
            yc, fc, vv = M + 206, f3, v3
            fin = len(v3) >= len(sub)
        else:
            yc, fc, vv = M + 128, f2, v2
        if _cursor(dt) and dt < dur - .5:
            cx = x + d.textlength(vv, font=fc) + (6 if fc is f3 else 2 * len(vv) + 10)
            d.rectangle((cx, yc - fc.size * .38, cx + fc.size * .45, yc + fc.size * .38), fill=AMBAR + (220 if fin else 255,))
        return _bgra(im, min(_eo(dt / .2), (dur - dt) / .45))
    return fn


# ------------------------------------------------------------------ misión fallida
def fallida(titulo="MISIÓN FALLIDA", motivo="", w=1920, h=1080):
    """Pantalla de MISIÓN FALLIDA a cuadro entero: viñeta roja que late, el título que entra con desenfoque y el motivo del
    juego que se escribe debajo. Se usa con x=.5, y=.5 (tipo mg) o como pantalla."""
    vig = Image.new("L", (w, h), 0)
    dv = ImageDraw.Draw(vig)
    for i in range(24):
        k = i / 24
        dv.rectangle((w * k * .32, h * k * .32, w * (1 - k * .32), h * (1 - k * .32)), fill=int(210 * (1 - k) ** 1.6))
    vig = vig.filter(ImageFilter.GaussianBlur(60))
    ft = ajustar(titulo.upper(), "b", 150, w - 300, peso="Bold Condensed")
    fm, ls, lh = caja(motivo.upper(), "m", 40, w - 520, max_lineas=3)

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        lat = .8 + .2 * math.sin(dt * 5)
        capa = Image.new("RGBA", (w, h), (120, 0, 0, 255))
        capa.putalpha(vig.point(lambda p: int(p * lat * _eo(dt / .5))))
        im.alpha_composite(capa)
        fondo = Image.new("RGBA", (w, h), (0, 0, 0, int(95 * _eo(dt / .5))))
        im.alpha_composite(fondo)
        t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(t)
        u = _eo((dt - .15) / .5)
        _txt(d, (w / 2, h * .44), titulo.upper(), ft, BLANCO, "mm", 255 * u, track=int(30 * (1 - u)) + 4)
        d.line([(w / 2 - 360 * u, h * .44 + 92), (w / 2 + 360 * u, h * .44 + 92)], fill=ROJO + (230,), width=3)
        quedan = max(0.0, (dt - .8) * 55)
        y = h * .44 + 150
        for ln in ls:
            vis = ln[:int(quedan)]
            _txt(d, (w / 2, y), vis, fm, HUESO, "mm", 240)
            quedan -= len(ln)
            y += lh
        if u < 1:
            t = t.filter(ImageFilter.GaussianBlur(10 * (1 - u)))
        im.alpha_composite(t)
        return _bgra(im, min(1.0, (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ logro desbloqueado
def logro(nombre, desc="", icono=None, w=760):
    """Aviso de LOGRO DESBLOQUEADO: placa compacta con un trofeo (o `icono` = ruta de imagen), que entra deslizando."""
    h = 150
    fl = fuente("mb", 24)
    fn_ = ajustar(nombre.upper(), "b", 48, w - 210, peso="Bold Condensed")
    fd = ajustar(desc, "b", 28, w - 210, peso="Light Condensed") if desc else None
    ico = None
    if icono:
        ico = Image.open(icono).convert("RGBA")
        ico.thumbnail((104, 104))

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, M=30, alfa=.72)
        d = ImageDraw.Draw(im)
        d.rectangle((M, M, M + 8, M + h), fill=AMBAR + (255,))
        cx, cy = M + 90, M + h / 2
        if ico is not None:
            im.alpha_composite(ico, (int(cx - ico.width / 2), int(cy - ico.height / 2)))
        else:                                                          # copa de trofeo dibujada
            g = _reb((dt - .2) / .5)
            r = 34 * g
            d.pieslice((cx - r, cy - r * 1.2, cx + r, cy + r * .8), 0, 180, fill=AMBAR + (255,))
            d.rectangle((cx - r, cy - r * 1.2, cx + r, cy - r * .2), fill=AMBAR + (255,))
            d.rectangle((cx - 5 * g, cy + r * .7, cx + 5 * g, cy + r * 1.1), fill=AMBAR + (255,))
            d.rectangle((cx - 20 * g, cy + r * 1.1, cx + 20 * g, cy + r * 1.3), fill=AMBAR + (255,))
        x = M + 170
        _txt(d, (x, M + 34), "LOGRO DESBLOQUEADO", fl, AMBAR, "lm", 255 * _eo((dt - .2) / .3), track=2)
        _txt(d, (x, M + 82), nombre.upper(), fn_, BLANCO, "lm", 255 * _eo((dt - .35) / .3))
        if fd:
            _txt(d, (x, M + 122), desc, fd, HUESO, "lm", 230 * _eo((dt - .5) / .3))
        u = _eo(dt / .35)
        out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        out.alpha_composite(im, (int(-120 * (1 - u)), 0))
        return _bgra(out, min(u, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ radio
def radio(indicativo, texto="", origen="RADIO / CANAL TÁCTICO", w=900):
    """Transmisión de radio: indicativo grande en verde de visión nocturna, onda que vibra mientras «habla», texto debajo."""
    h = 220 if texto else 170
    fo = fuente("mb", 22)
    fi = ajustar(indicativo.upper(), "b", 68, w - 120, peso="Bold Condensed")
    ft = ajustar(texto, "b", 32, w - 120, peso="Light Condensed") if texto else None
    rng = np.random.default_rng(len(indicativo))
    fases = rng.uniform(0, 6.28, 64)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.64)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 200, L=26, color=VERDE, ancho=2)
        x = M + 48
        on = (dt * 3) % 1 < .6
        d.ellipse((x, M + 30, x + 14, M + 44), fill=(ROJO if on else GRIS) + (255,))
        _txt(d, (x + 28, M + 37), origen, fo, VERDE, "lm", 230)
        _txt(d, (x, M + 100), indicativo.upper(), fi, VERDE, "lm", 255 * _eo((dt - .15) / .3), track=2)
        x0, x1, yc = M + w - 330, M + w - 50, M + 100
        n = 48
        for i in range(n):
            amp = (8 + 30 * abs(math.sin(dt * 9 + fases[i]))) * _eo((dt - .2) / .3) * (.25 + .75 * math.sin(math.pi * i / n))
            xx = x0 + (x1 - x0) * i / n
            d.line([(xx, yc - amp), (xx, yc + amp)], fill=VERDE + (210,), width=3)
        if ft:
            _txt(d, (x, M + 168), texto, ft, HUESO, "lm", 240 * _eo((dt - .4) / .3))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ código de la caja fuerte
def codigo(digitos, titulo="CÓDIGO", sub=None, w=None):
    """Teclado de caja fuerte: casillas vacías; cada dígito entra en su marca (o cada 0,45 s) con destello ámbar; al
    completarse, «ACCESO CONCEDIDO» en verde."""
    n = len(digitos)
    L = 140
    w = w or max(620, n * (L + 26) + 120)
    h = 380 if sub else 330
    ft = ajustar(titulo.upper(), "mb", 30, w - 80)
    fdg = fuente("b", 110, "Bold Condensed")
    fs = fuente("mb", 26)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.66)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + w / 2, M + 44), titulo.upper(), ft, AMBAR, "mm", 255, track=3)
        mk = list(marcas or [.5 + .45 * i for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + .45)
        x0 = M + (w - (n * L + (n - 1) * 26)) / 2
        for i, c in enumerate(digitos):
            bx, by = x0 + i * (L + 26), M + 84
            entra = dt >= mk[i]
            d.rectangle((bx, by, bx + L, by + L + 20), outline=(AMBAR if entra else GRIS) + (255,), width=3,
                        fill=(255, 255, 255, 14))
            if entra:
                k = _eo((dt - mk[i]) / .25)
                _txt(d, (bx + L / 2, by + (L + 20) / 2), c, fdg, BLANCO, "mm", 255 * k)
                if dt - mk[i] < .2:
                    d.rectangle((bx, by, bx + L, by + L + 20), fill=AMBAR + (int(110 * (1 - (dt - mk[i]) / .2)),))
        if dt > mk[-1] + .5:
            _txt(d, (M + w / 2, M + h - 52 - (34 if sub else 0)), "ACCESO CONCEDIDO", fs, VERDE, "mm",
                 255 * _eo((dt - mk[-1] - .5) / .3), track=4)
        if sub:
            _txt(d, (M + w / 2, M + h - 40), sub, fs, HUESO, "mm", 220)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ sello CLASIFICADO
def sello(texto="CLASIFICADO", sub="EXPEDIENTE 141", giro=-8):
    """Sello rojo que cae grande y se estampa (rebote + sacudida); textura gastada."""
    f1 = fuente("i", 150)
    f2 = fuente("mb", 46)
    W = int(_ancho(texto, f1) + 140)
    H = 300
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    d.rectangle((10, 10, W - 10, H - 10), outline=ROJO + (255,), width=12)
    d.rectangle((28, 28, W - 28, H - 28), outline=ROJO + (255,), width=4)
    d.text((W / 2, H * .42), texto, font=f1, fill=ROJO + (255,), anchor="mm")
    d.text((W / 2, H * .80), sub, font=f2, fill=ROJO + (255,), anchor="mm")
    a = np.array(base)
    rng = np.random.default_rng(141)
    ruido = rng.random(a.shape[:2])
    a[..., 3] = (a[..., 3] * np.where(ruido < .10, .35, 1.0)).astype(np.uint8)        # tinta gastada
    base = Image.fromarray(a).rotate(giro, resample=Image.BICUBIC, expand=True)

    def fn(dt, dur, marcas):
        u = _eo(dt / .22)
        s = 2.4 - 1.4 * u
        if dt > .22:
            s = 1 + .04 * math.exp(-(dt - .22) * 10) * math.sin((dt - .22) * 40)
        im = base.resize((max(2, int(base.width * s)), max(2, int(base.height * s))), Image.BICUBIC)
        return _bgra(im, min(u, (dur - dt) / .4) * .92)
    return fn


# ------------------------------------------------------------------ línea de tiempo
def linea(titulo, hitos, w=1700, h=430):
    """hitos = [(año, juego, frase)]; marca k = el hito k: punto que se enciende y su texto; el último en ámbar."""
    n = len(hitos)
    ft = ajustar(titulo.upper(), "b", 46, w - 120, peso="Bold Condensed")
    fa = fuente("b", 56, "Bold Condensed")
    fj = fuente("mb", 24)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.62)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + 60, M + 50), titulo.upper(), ft, BLANCO, "lm", 255, track=2)
        mk = list(marcas or [.5 + 1.0 * i for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + 1.0)
        y = M + 190
        x0, x1 = M + 120, M + w - 120
        fin = max(0.0, min(1.0, (dt - mk[0] + .3) / max(.3, mk[-1] - mk[0] + .3)))
        d.line([(x0, y), (x0 + (x1 - x0) * fin, y)], fill=GRIS + (200,), width=3)
        paso = (x1 - x0) / max(1, n - 1)
        for i, ((anio, juego, frase), m) in enumerate(zip(hitos, mk)):
            if dt < m:
                continue
            x = x0 + paso * i if n > 1 else (x0 + x1) / 2
            u = _reb((dt - m) / .4)
            col = AMBAR if i == n - 1 else BLANCO
            r = 14 * u
            d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,))
            _txt(d, (x, y - 58), str(anio), fa, col, "mm", 255 * _eo((dt - m) / .3))
            _txt(d, (x, y + 46), juego.upper(), ajustar(juego.upper(), "mb", 24, paso - 20), GRIS, "mm", 255 * _eo((dt - m - .1) / .3))
            if frase:
                fff, ls, lh = caja(frase, "b", 30, paso - 30, 100, max_lineas=3, peso="SemiLight Condensed")
                for k, l_ in enumerate(ls):
                    _txt(d, (x, y + 92 + k * lh), l_, fff, HUESO, "mm", 255 * _eo((dt - m - .2) / .3))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ espejo 2007 | 2026
def espejo(titulo, izq, der, centro="", w=1640, h=None):
    """izq/der = (año, juego, [líneas], ruta_imagen|None); marca 0 = izquierda, marca 1 = derecha, marca 2 = el vínculo
    del centro (`centro`, p. ej. «MISMO COMPOSITOR») que se enciende en ámbar."""
    ft = ajustar(titulo.upper(), "b", 48, w - 120, peso="Bold Condensed")
    fa = fuente("b", 80, "Bold Condensed")
    fj = fuente("mb", 26)
    fl = fuente("b", 32, "SemiLight Condensed")
    fc = ajustar(centro.upper(), "mb", 28, 300) if centro else None
    imgs = []
    for lado in (izq, der):
        r = lado[3] if len(lado) > 3 else None
        if r:
            p = Image.open(r).convert("RGBA")
            p.thumbnail((240, 240))
            imgs.append(p)
        else:
            imgs.append(None)
    h = h or (360 + max(len(izq[2]), len(der[2])) * 40 + max((i.height for i in imgs if i is not None), default=0))

    def col(d, im, M, cx, lado, img, u, dt0):
        anio, juego, lineas = lado[0], lado[1], lado[2]
        y = M + 110
        if img is not None:
            im.alpha_composite(img, (int(cx - img.width / 2), int(y)))
            y += img.height
        _txt(d, (cx, y + 40), str(anio), fa, BLANCO, "mm", 255 * u)
        _txt(d, (cx, y + 100), juego.upper(), fj, AMBAR, "mm", 255 * u, track=2)
        for k, l_ in enumerate(lineas):
            _txt(d, (cx, y + 150 + k * 40), l_, fl, HUESO, "mm", 255 * _eo((dt0 - .2 - .15 * k) / .3))

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.62)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + w / 2, M + 56), titulo.upper(), ft, BLANCO, "mm", 255, track=2)
        mk = list(marcas or [.4, 1.6, 2.8])
        while len(mk) < 3:
            mk.append(mk[-1] + 1.2)
        if dt >= mk[0]:
            col(d, im, M, M + w * .25, izq, imgs[0], _eo((dt - mk[0]) / .35), dt - mk[0])
        if dt >= mk[1]:
            col(d, im, M, M + w * .75, der, imgs[1], _eo((dt - mk[1]) / .35), dt - mk[1])
        if dt >= mk[2]:
            u = _eo((dt - mk[2]) / .4)
            cy = M + 110 + max((i.height for i in imgs if i is not None), default=0) + 105
            d.line([(M + w * .40, cy), (M + w * .40 + (w * .2) * u, cy)], fill=AMBAR + (255,), width=4)
            if fc:
                _txt(d, (M + w / 2, cy - 30), centro.upper(), fc, AMBAR, "mm", 255 * u, track=2)
        else:
            d.line([(M + w / 2, M + 110), (M + w / 2, M + h - 40)], fill=GRIS + (90,), width=2)
        return _salida(im, dt, dur)
    return fn



# ------------------------------------------------------------------ balanza: lo permitido vs lo castigado
def balanza(titulo, filas, w=1200):
    """filas = [(texto, bien: bool, nota)]; marca k = fila k: ✓ verde (se permite) o ✗ rojo (se castiga) que se estampa."""
    n = len(filas)
    fila_h = 96
    h = 120 + n * fila_h + 30
    ft = ajustar(titulo.upper(), "b", 48, w - 120, peso="Bold Condensed")
    fx = fuente("b", 40, "SemiBold Condensed")
    fno = fuente("mb", 26)

    def fn(dt, dur, marcas):
        im, M_ = _cristal(w, h, alfa=.64)
        d = ImageDraw.Draw(im)
        _escuadras(d, M_, M_, M_ + w, M_ + h, 220)
        _txt(d, (M_ + 50, M_ + 56), titulo.upper(), ft, BLANCO, "lm", 255, track=2)
        mk = list(marcas or [.5 + .9 * i for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + .9)
        for i, ((texto, bien, nota), m) in enumerate(zip(filas, mk)):
            if dt < m:
                continue
            y = M_ + 140 + i * fila_h
            u = _eo((dt - m) / .3)
            _txt(d, (M_ + 150, y), texto, fx, BLANCO, "lm", 255 * u)
            if nota:
                _txt(d, (M_ + w - 50, y), nota.upper(), fno, VERDE if bien else ROJO, "rm", 255 * _eo((dt - m - .25) / .3), track=2)
            s = _reb((dt - m - .1) / .35)
            cx, cy, r = M_ + 85, y, 26 * s
            if r > 1:
                c = VERDE if bien else ROJO
                if bien:
                    d.line([(cx - r, cy), (cx - r * .3, cy + r * .7), (cx + r, cy - r * .8)], fill=c + (255,), width=8)
                else:
                    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=c + (255,), width=8)
                    d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=c + (255,), width=8)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-5.0):
    """Imagen REAL recortada con borde blanco (mg_tes) que entra con rebote, se balancea y flota; el nombre en una placa
    táctica negra con filo ámbar a la izquierda y letra condensada."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = titulo.upper()
        f = ajustar(tit, "b", 34, max(260, base.width + 40), peso="Bold Condensed")
        pw, ph = int(_ancho(tit, f) + 64), 60
        pil = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        dp = ImageDraw.Draw(pil)
        dp.rectangle((0, 0, pw - 1, ph - 1), fill=(8, 11, 12, 200))
        dp.rectangle((0, 0, 9, ph - 1), fill=AMBAR + (255,))
        _txt(dp, (pw / 2 + 5, ph / 2 + 1), tit, f, BLANCO, "mm", 255, track=1)
        lien = Image.new("RGBA", (max(base.width, pw), base.height + ph // 2), (0, 0, 0, 0))
        lien.alpha_composite(base, ((lien.width - base.width) // 2, 0))
        lien.alpha_composite(pil, ((lien.width - pw) // 2, base.height - ph // 2))
        base = lien

    def fn(dt, dur, marcas):
        s = T._pop(dt, .42)
        if s <= 0.02:
            return np.zeros((2, 2, 4), np.uint8)
        ang = giro * min(1.0, dt / .5) + (1 - min(1.0, dt / .5)) * -18 + 1.8 * math.sin(dt * 2.1)
        im = base.rotate(ang, resample=Image.BICUBIC, expand=True)
        k = s * (1 + .02 * math.sin(dt * 3.0))
        im = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.BILINEAR)
        a = np.array(im)[..., [2, 1, 0, 3]]
        fl = int(round(6 * math.sin(dt * 1.7)))
        out = np.zeros((a.shape[0] + 16, a.shape[1], 4), np.uint8)
        out[8 + fl:8 + fl + a.shape[0]] = a
        return out
    return fn
