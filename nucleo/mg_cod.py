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
  fusion(izq, der, resultado)         (13-nov-2026, cod_mandela2) DOS RECUERDOS REALES que se funden en uno FALSO: dos tarjetas
                                      con su imagen se acercan (marca 0, marca 1), chocan con un fallo de señal (marca 2) y queda
                                      una sola tarjeta «TU MEMORIA» con el recuerdo mezclado tachado en rojo
  pegatina(ruta, titulo, tam)         imagen REAL con borde blanco; nombre en placa táctica con filo ámbar
  acta(nombre, foto, filas, estado)   (17-nov-2026, cod_villanos) ACTA DE DEFUNCIÓN: retrato con la cara visible + filas
                                      (CAUSA/AUTOR/LUGAR…) una por marca; la marca n+1 estampa «MUERTE CONFIRMADA» (X roja, retrato
                                      a B/N) | «SOBREVIVIÓ» | «DEPENDE DEL FINAL» | «SIN CUERPO»
  bajas(sagas, tachados, foco)        (17-nov-2026) TABLERO DE BAJAS por saga: retratos en columnas; los ya muertos en B/N con
                                      X; el `foco` en ámbar recibe su X en la marca 0 (abre cada puesto de una lista de villanos)
  placa(nombre, lineas, estado)       (24-nov-2026, cod_protagonistas) PLACA DE IDENTIFICACIÓN metálica con cadena: el nombre y
                                      las `lineas` se graban una por marca; la marca n+1 estampa el estado (vivo | kia | mia |
                                      depende | retcon | vuelve | desconocido | retirado | preso)
  servicio(nombre, foto, filas)       (24-nov-2026) HOJA DE SERVICIO: retrato + una fila por juego (juego, año, estado, nota) con
                                      píldora de color; la última fila (el destino final) en ámbar
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


# ------------------------------------------------------------------ 3-nov-2026: MG nuevos (el usuario: «faltan animaciones»)
def objetivo(texto, sub=None, cabecera="OBJETIVO ACTUALIZADO", completo=False, w=820):
    """Aviso de OBJETIVO de la campaña: rombo ámbar que late, cabecera en mono, el objetivo en condensada y una casilla
    que se MARCA en la primera marca (o a los 70 % si no hay marcas) y pasa a «OBJETIVO COMPLETADO»."""
    h = 150 if sub else 118
    fc = fuente("mb", 22)
    ft = ajustar(texto.upper(), "b", 44, w - 170, peso="Bold Condensed")
    fs = ajustar(sub, "b", 28, w - 170, peso="Light Condensed") if sub else None

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, M=30, alfa=.66)
        d = ImageDraw.Draw(im)
        hecho = completo or dt >= (marcas[0] if marcas else dur * .7)
        cx, cy = M + 56, M + 58
        r = 24 * _reb((dt - .05) / .4) * (1 + .08 * math.sin(dt * 7))
        col = VERDE if hecho else AMBAR
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], outline=col + (255,), width=4)
        d.polygon([(cx, cy - r * .45), (cx + r * .45, cy), (cx, cy + r * .45), (cx - r * .45, cy)], fill=col + (255,))
        x = M + 110
        cab = "OBJETIVO COMPLETADO" if hecho and not completo else cabecera
        vis = cab[:int(max(0, (dt - .1) * 60))]
        _txt(d, (x, M + 28), vis, fc, col, "lm", 255, track=2)
        _txt(d, (x, M + 70), texto.upper(), ft, BLANCO, "lm", 255 * _eo((dt - .25) / .3))
        if fs:
            _txt(d, (x, M + 114), sub, fs, HUESO, "lm", 230 * _eo((dt - .4) / .3))
        bx = M + w - 60                                           # casilla que se marca
        d.rectangle((bx - 18, cy - 18, bx + 18, cy + 18), outline=BLANCO + (220,), width=3)
        if hecho:
            k = _eo(((dt - (marcas[0] if marcas else dur * .7)) if not completo else dt) / .25)
            pts = [(bx - 12, cy), (bx - 3, cy + 10), (bx + 14, cy - 12)]
            d.line(pts[:2] if k < .5 else pts, fill=VERDE + (255,), width=5)
        u = _eo(dt / .3)
        out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        out.alpha_composite(im, (int(-90 * (1 - u)), 0))
        return _bgra(out, min(u, (dur - dt) / .35))
    return fn


def marcador(nombre, metros=40, sub=None):
    """Marcador de objetivo flotando SOBRE algo del clip (la tele, la impresora, la caja): rombo ámbar con halo que sube
    y baja, nombre encima y la distancia que BAJA hasta llegar («12 m» → «0 m»). Ponerlo con x/y sobre el objeto."""
    fn_ = ajustar(nombre.upper(), "b", 40, 520, peso="Bold Condensed")
    fd = fuente("mb", 28)
    fs = ajustar(sub, "b", 26, 520, peso="Light Condensed") if sub else None
    W, H = 600, 330

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        a = 255 * min(_eo(dt / .25), max(0.0, (dur - dt) / .3))
        cx, cy = W / 2, 200 + 8 * math.sin(dt * 3.2)
        r = 30 * _reb(dt / .45)
        for k in range(4, 0, -1):                                # halo
            rr = r + k * 7 + 6 * ((dt * 1.6) % 1)
            d.polygon([(cx, cy - rr), (cx + rr, cy), (cx, cy + rr), (cx - rr, cy)], outline=AMBAR + (int(a * .12 * k),), width=2)
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=AMBAR + (int(a),))
        d.polygon([(cx, cy - r * .5), (cx + r * .5, cy), (cx, cy + r * .5), (cx - r * .5, cy)], fill=OSCURO + (int(a),))
        _txt(d, (cx, cy - 78), nombre.upper(), fn_, BLANCO, "mm", a, track=1)
        m = max(0, int(round(metros * (1 - _eo(dt / max(.5, dur * .75))))))
        _txt(d, (cx, cy + 58), f"{m} m", fd, AMBAR, "mm", a)
        if fs:
            _txt(d, (cx, cy + 96), sub, fs, HUESO, "mm", a * .9)
        return _bgra(im, 1.0)
    return fn


def contador(valor, unidad="", titulo="", desde=0, decimales=0, w=760):
    """Cifra GRANDE que rueda de `desde` a `valor` (19 AÑOS, 0,5 S, 2007…) con el título en mono encima y la unidad en
    ámbar; panel de cristal con escuadras. La cifra se asienta con un pequeño rebote."""
    h = 250
    ft = fuente("mb", 26)
    fv = fuente("b", 150, "Bold Condensed")
    fu = fuente("b", 64, "SemiBold Condensed")

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.6)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220 * _eo(dt / .3))
        if titulo:
            vis = titulo.upper()[:int(max(0, (dt - .05) * 60))]
            _txt(d, (M + w / 2, M + 36), vis, ft, AMBAR, "mm", 255, track=3)
        k = _eo((dt - .15) / .9)
        v = desde + (valor - desde) * k
        s = f"{v:.{decimales}f}".replace(".", ",")
        sc = 1 + .12 * max(0.0, 1 - abs(dt - 1.05) / .18) if k >= 1 else 1.0
        f = fuente("b", int(150 * sc), "Bold Condensed")
        anchov = d.textlength(s, font=f)
        anchou = d.textlength(" " + unidad, font=fu) if unidad else 0
        x0 = M + (w - anchov - anchou) / 2
        _txt(d, (x0, M + 150), s, f, BLANCO, "lm", 255)
        if unidad:
            _txt(d, (x0 + anchov + d.textlength(" ", font=fu), M + 168), unidad, fu, AMBAR, "lm", 255 * _eo((dt - .3) / .3))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ MG nuevos de `cod_misterios` (9-nov-2026)
def caso(estado, titulo, sub=None, w=900):
    """Estado del CASO de un misterio: la barra de escaneo recorre el panel («ANALIZANDO…») y se estampa el veredicto.
    estado = "resuelto" (verde) | "sin_resolver" (ámbar) | "falso" (rojo) | "verdad" (verde) | "a_medias" (ámbar, 13-nov-2026);
    `sub` = p. ej. «Tardaron 4 años»."""
    col, rot = {"resuelto": (VERDE, "RESUELTO"), "sin_resolver": (AMBAR, "SIN RESOLVER"), "falso": (ROJO, "FALSO"),
                "verdad": (VERDE, "ERA VERDAD"), "a_medias": (AMBAR, "A MEDIAS")}[estado]
    h = 300 if sub else 250
    ft = ajustar(titulo.upper(), "mb", 28, w - 90)
    fv = fuente("b", 108, "Bold Condensed")
    fs = fuente("mb", 26)
    fa = fuente("mb", 22)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.64)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + 40, M + 38), "EXPEDIENTE / ESTADO DEL CASO", fa, GRIS, "lm", 230, track=2)
        _txt(d, (M + w / 2, M + 82), titulo.upper(), ft, BLANCO, "mm", 255, track=2)
        t_scan = .9
        if dt < t_scan:                                       # escaneo
            x = M + 30 + (w - 60) * _eo(dt / t_scan)
            d.rectangle((x - 3, M + 112, x + 3, M + h - 26), fill=col + (220,))
            d.rectangle((M + 30, M + 112, x, M + h - 26), fill=col + (26,))
            pts = "." * (1 + int(dt * 6) % 3)
            _txt(d, (M + w / 2, M + 172), "ANALIZANDO" + pts, fs, HUESO, "mm", 220, track=4)
        else:
            u = dt - t_scan
            s = 1.6 - .6 * _eo(u / .18)
            f = fuente("b", int(108 * s), "Bold Condensed")
            _txt(d, (M + w / 2, M + 170), rot, f, col, "mm", 255 * _eo(u / .12), track=3)
            if u < .25:
                d.rectangle((M + 6, M + 6, M + w - 6, M + h - 6), outline=col + (int(200 * (1 - u / .25)),), width=6)
            if sub:
                vis = sub[:int(max(0, (u - .3) * 55))]
                _txt(d, (M + w / 2, M + h - 48), vis, fs, HUESO, "mm", 235)
        return _salida(im, dt, dur)
    return fn


def descifra(cifrado, claro, titulo="DESCIFRANDO", sub=None, w=None):
    """El texto CIFRADO (Morse, números, símbolos) se convierte letra a letra en el texto CLARO: cada letra baraja caracteres
    al azar y se fija en ámbar → blanco. Con marcas, cada marca suelta un tramo; sin ellas, ~14 letras por segundo."""
    n = len(claro)
    fm = fuente("mb", 46)
    w = w or int(min(1700, max(760, _ancho(claro.upper(), fm) + 160, _ancho(cifrado, fm) + 160)))
    h = 330 if sub else 280
    ft = ajustar(titulo.upper(), "mb", 28, w - 90)
    fs = fuente("mb", 24)
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@%&*/-.:"
    rng = np.random.default_rng(len(claro) * 31 + 7)
    tabla = rng.integers(0, len(abc), size=(400, n))
    cla = claro.upper()

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.66)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + w / 2, M + 42), titulo.upper(), ft, AMBAR, "mm", 255, track=3)
        _txt(d, (M + w / 2, M + 110), cifrado, fuente("mb", 34), GRIS, "mm", 230)
        t0 = (marcas[0] if marcas else .4)
        k = int(max(0, (dt - t0) * 14))                       # letras ya fijadas
        out, cols = [], []
        for i in range(n):
            if cla[i] == " ":
                out.append(" "); cols.append(BLANCO)
            elif i < k:
                out.append(cla[i]); cols.append(AMBAR if i >= k - 2 else BLANCO)
            elif dt >= t0:
                out.append(abc[tabla[int(dt * 24) % 400, i]]); cols.append(GRIS)
            else:
                out.append("_"); cols.append(GRIS)
        x = M + (w - _ancho("".join(out), fm)) / 2
        for c, col in zip(out, cols):
            _txt(d, (x, M + 180), c, fm, col, "lm", 255)
            x += _ancho(c, fm)
        if k >= n and sub:
            _txt(d, (M + w / 2, M + h - 44), sub, fs, VERDE, "mm", 255 * _eo((dt - t0 - n / 14) / .3), track=2)
        return _salida(im, dt, dur)
    return fn



# ------------------------------------------------------------------ fusión: dos recuerdos reales → un recuerdo falso (13-nov-2026)
def fusion(izq, der, resultado, titulo="ASÍ SE FABRICA UN EFECTO MANDELA", w=1500, h=640):
    """izq/der = (ruta_imagen, rótulo, sub) = dos cosas REALES (p. ej. Weaver + cuchillo · Pyle + cigarro); resultado = el recuerdo
    FALSO que sale de juntarlas («Weaver + puro»). Marca 0: entra la izquierda · marca 1: entra la derecha · marca 2: se acercan,
    chocan con un fallo de señal (franjas RGB) y aparece la tarjeta central «TU MEMORIA» con el resultado tachado en rojo."""
    fT = ajustar(titulo.upper(), "b", 40, w - 140, peso="Bold Condensed")
    fR = fuente("b", 36, "Bold Condensed")
    fS = fuente("mb", 22)
    fM = fuente("mb", 24)
    fX = ajustar(resultado.upper(), "b", 54, 520, peso="Bold Condensed")
    imgs = []
    for lado in (izq, der):
        p_ = Image.open(lado[0]).convert("RGBA")
        p_.thumbnail((330, 300))
        imgs.append(p_)

    def tarjeta(im, d, img, rot, sub, cx, cy, alfa):
        a = int(255 * alfa)
        if a <= 0:
            return
        bw, bh = 380, 420
        x0, y0 = int(cx - bw / 2), int(cy - bh / 2)
        d.rectangle((x0, y0, x0 + bw, y0 + bh), fill=OSCURO + (int(150 * alfa),))
        _escuadras(d, x0, y0, x0 + bw, y0 + bh, a, L=26)
        t = img.copy()
        if alfa < 1:
            t.putalpha(t.getchannel("A").point(lambda v: int(v * alfa)))
        im.alpha_composite(t, (int(cx - t.width / 2), y0 + 20))
        _txt(d, (cx, y0 + bh - 74), rot.upper(), fR, BLANCO, "mm", a, track=2)
        _txt(d, (cx, y0 + bh - 34), sub.upper(), fS, AMBAR, "mm", a, track=2)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.60)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + w / 2, M + 52), titulo.upper(), fT, BLANCO, "mm", 255, track=2)
        mk = list(marcas or [.3, 1.4, 2.8])
        while len(mk) < 3:
            mk.append(mk[-1] + 1.3)
        cy = M + h / 2 + 30
        junta = _eo((dt - mk[2]) / .45) if dt >= mk[2] else 0.0
        sep = (w * .30) * (1 - junta)
        for k, (lado, img) in enumerate(zip((izq, der), imgs)):
            if dt < mk[k]:
                continue
            u = _eo((dt - mk[k]) / .35)
            cx = M + w / 2 + (-1 if k == 0 else 1) * (sep + 40 * (1 - u))
            tarjeta(im, d, img, lado[1], lado[2], cx, cy, u * (1 - junta))
        if dt >= mk[1] and junta < 1:
            _txt(d, (M + w / 2, cy), "+", fuente("b", 110, "Bold Condensed"), AMBAR, "mm", 255 * (1 - junta))
        if dt >= mk[2]:
            u = dt - mk[2]
            if .35 < u < .75:                                       # fallo de señal al chocar
                rng = np.random.default_rng(int(u * 40))
                for _ in range(7):
                    yy = int(M + 100 + rng.random() * (h - 160))
                    c = (ROJO, VERDE, (80, 160, 255))[int(rng.random() * 3)]
                    d.rectangle((M + 20, yy, M + w - 20, yy + int(4 + rng.random() * 14)), fill=c + (110,))
            if u > .55:
                v = _eo((u - .55) / .35)
                bw, bh = 640, 300
                x0, y0 = int(M + w / 2 - bw / 2), int(cy - bh / 2)
                d.rectangle((x0, y0, x0 + bw, y0 + bh), fill=OSCURO + (int(200 * v),))
                d.rectangle((x0, y0, x0 + bw, y0 + bh), outline=ROJO + (int(230 * v),), width=4)
                _txt(d, (x0 + bw / 2, y0 + 48), "TU MEMORIA", fM, ROJO, "mm", 255 * v, track=6)
                _txt(d, (x0 + bw / 2, y0 + 150), resultado.upper(), fX, BLANCO, "mm", 255 * v, track=2)
                if u > 1.1:                                         # tachón rojo
                    z = _eo((u - 1.1) / .3)
                    x1 = x0 + 50 + (bw - 100) * z
                    d.line([(x0 + 50, y0 + 172), (x1, y0 + 128)], fill=ROJO + (240,), width=9)
                    if z >= 1:
                        _txt(d, (x0 + bw / 2, y0 + bh - 44), "NUNCA PASÓ", fM, ROJO, "mm", 255, track=6)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 17-nov-2026 (cod_villanos): MG de VILLANOS
def _retrato(ruta, lado, bn=False):
    """Retrato cuadrado con la CARA visible: recorta por arriba (las fichas de la wiki son de cuerpo entero)."""
    im = Image.open(ruta).convert("RGBA")
    w, h = im.size
    if h > w * 1.05:
        im = im.crop((0, 0, w, int(w * 1.05)))
    elif w > h * 1.3:
        c = (w - int(h * 1.2)) // 2
        im = im.crop((c, 0, c + int(h * 1.2), h))
    fondo = Image.new("RGBA", im.size, OSCURO + (255,))
    fondo.alpha_composite(im)
    fondo = fondo.resize((lado, max(1, int(lado * fondo.height / fondo.width))), Image.LANCZOS)
    if fondo.height > lado:
        fondo = fondo.crop((0, 0, lado, lado))
    elif fondo.height < lado:
        lien = Image.new("RGBA", (lado, lado), OSCURO + (255,))
        lien.alpha_composite(fondo, (0, (lado - fondo.height) // 2))
        fondo = lien
    if bn:
        g = fondo.convert("L").convert("RGBA")
        fondo = Image.blend(fondo, g, .85)
    return fondo


def acta(nombre, foto, filas, estado="confirmado", sub=None, cabecera="INFORME FORENSE / EXPEDIENTE 141", w=1180):
    """ACTA DE DEFUNCIÓN del villano: retrato a la izquierda (cara visible) y filas de datos que se escriben una por marca
    (`filas` = [(«CAUSA», «Disparo a la cabeza»), («AUTOR», «Soap MacTavish»), …]). La marca n+1 (tras la última fila)
    estampa el sello: estado = "confirmado" (rojo, «MUERTE CONFIRMADA», X sobre el retrato, que pasa a B/N) |
    "sobrevivio" (ámbar, «SOBREVIVIÓ») | "depende" (ámbar, «DEPENDE DEL FINAL») | "sin_cuerpo" (gris, «SIN CUERPO»).
    `sub` sale bajo el retrato tras el sello. Sin marcas: una fila cada 0,6 s desde 0,5 s."""
    col, rot = {"confirmado": (ROJO, "MUERTE CONFIRMADA"), "sobrevivio": (AMBAR, "SOBREVIVIÓ"),
                "depende": (AMBAR, "DEPENDE DEL FINAL"), "sin_cuerpo": (GRIS, "SIN CUERPO")}[estado]
    R = 330
    ret_bn = _retrato(foto, R, bn=True)
    ret = _retrato(foto, R)
    in_x = R + 90
    in_w = w - in_x - 50
    filas = [(k.upper(), v) for k, v in filas]
    fK = fuente("mb", 22)
    fV = [ajustar(v, "b", 38, in_w - 10, minimo=20, peso="SemiBold Condensed") for _, v in filas]
    fN = ajustar(nombre.upper(), "b", 62, in_w, peso="Bold Condensed")
    fC = fuente("mb", 22)
    fs2 = ajustar(sub or "", "mb", 24, R + 40, minimo=14)
    filah = 74
    h = max(R + 150, 170 + filah * len(filas) + 110)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.66)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + 40, M + 36), cabecera, fC, GRIS, "lm", 230, track=2)
        n = len(filas)
        mk = list(marcas or [])
        while len(mk) < n + 1:
            mk.append((mk[-1] + .6) if mk else .5)
        t_sello = mk[n]
        sellado = dt >= t_sello
        u = _eo(dt / .35)
        rx, ry = M + 40, M + 74
        if u > 0:
            rr = (ret_bn if (sellado and estado == "confirmado") else ret).copy()
            rr.putalpha(rr.getchannel("A").point(lambda v: int(v * u)))
            im.alpha_composite(rr, (rx, ry))
            d.rectangle((rx, ry, rx + R, ry + R), outline=BLANCO + (int(200 * u),), width=3)
        _txt(d, (M + in_x, M + 100), nombre.upper(), fN, BLANCO, "lm", 255 * _eo((dt - .15) / .3), track=1)
        k = _eo((dt - .3) / .4)
        d.line([(M + in_x, M + 142), (M + in_x + in_w * k, M + 142)], fill=AMBAR + (200,), width=2)
        y = M + 160 + filah / 2
        for i, ((clave, val), fv) in enumerate(zip(filas, fV)):
            t0 = mk[i]
            if dt >= t0:
                a = _eo((dt - t0) / .25)
                _txt(d, (M + in_x, y - 18), clave, fK, AMBAR, "lm", 255 * a, track=3)
                vis = val[:int(max(0, (dt - t0) * 60))]
                _txt(d, (M + in_x, y + 14), vis + ("_" if _cursor(dt) and len(vis) < len(val) else ""), fv, HUESO, "lm", 255)
            y += filah
        if sellado:
            u = dt - t_sello
            if estado == "confirmado":                       # X roja sobre el retrato
                for j, t_ in enumerate((0.0, .12)):
                    z = _eo((u - t_) / .25)
                    if z <= 0:
                        continue
                    if j == 0:
                        d.line([(rx + 20, ry + 20), (rx + 20 + (R - 40) * z, ry + 20 + (R - 40) * z)], fill=ROJO + (235,), width=14)
                    else:
                        d.line([(rx + R - 20, ry + 20), (rx + R - 20 - (R - 40) * z, ry + 20 + (R - 40) * z)],
                               fill=ROJO + (235,), width=14)
            s = 1.5 - .5 * _eo(u / .18)
            f = fuente("b", int(60 * s), "Bold Condensed")
            f1 = fuente("b", 60, "Bold Condensed")
            tw = _ancho(rot, f1) + 70
            sy = M + h - 66
            sx = min(M + in_x + tw / 2, M + w - 30 - tw / 2)
            a = 255 * _eo(u / .12)
            d.rectangle((sx - tw / 2, sy - 42, sx + tw / 2, sy + 42), outline=col + (int(a),), width=5)
            _txt(d, (sx, sy), rot, f, col, "mm", a, track=3)
            if sub and u > .3:
                vis = sub[:int((u - .3) * 55)]
                _txt(d, (rx + R / 2, ry + R + 32), vis, fs2, col, "mm", 240)
        return _salida(im, dt, dur)
    return fn


def bajas(sagas, tachados=(), foco=None, titulo="LISTA DE OBJETIVOS", w=1700, lado=150):
    """TABLERO DE BAJAS por saga (el «árbol» de villanos): columnas = sagas [(«MODERN WARFARE», [(ruta, nombre), …]), …],
    retratos en B/N con X roja los ya `tachados`, a color los vivos. `foco` = nombre resaltado en ámbar que, en la
    marca 0 (o a los 1,2 s), recibe su X roja con un golpe. Sirve para el gancho (foco=None) y para abrir cada puesto."""
    tach = set(tachados)
    fT = ajustar(titulo.upper(), "b", 46, w - 120, peso="Bold Condensed")
    fS = fuente("mb", 22)
    cols = []
    for nom_saga, fotos in sagas:
        cols.append((nom_saga, [(n, _retrato(r, lado), _retrato(r, lado, bn=True)) for r, n in fotos]))
    gap = 22
    colw = (w - 80) / len(cols)
    per_fila = max(1, int((colw - 10) // (lado + gap)))
    filas = max(-(-len(c[1]) // per_fila) for c in cols)
    fnom = ajustar("X" * 13, "b", 24, lado + gap - 4, minimo=14, peso="SemiBold Condensed")
    h = int(130 + filas * (lado + 56) + 30)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.62)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + w / 2, M + 44), titulo.upper(), fT, BLANCO, "mm", 255, track=3)
        t_foco = (list(marcas)[0] if marcas else 1.2)
        k_ent = 0
        for ci, (nom_saga, fotos) in enumerate(cols):
            x0 = M + 40 + ci * colw
            _txt(d, (x0 + colw / 2, M + 98), nom_saga.upper(), fS, AMBAR, "mm", 255, track=3)
            if ci:
                d.line([(x0, M + 90), (x0, M + h - 30)], fill=(255, 255, 255, 40), width=1)
            for j, (nom, rc, rb) in enumerate(fotos):
                fi, cj = divmod(j, per_fila)
                en_fila = min(per_fila, len(fotos) - fi * per_fila)
                cx = x0 + colw / 2 + (cj - (en_fila - 1) / 2) * (lado + gap)
                y = int(M + 125 + fi * (lado + 56))
                u = _eo((dt - .06 * k_ent) / .3)
                k_ent += 1
                if u <= 0:
                    continue
                es_foco = (nom == foco)
                muerto = nom in tach or (es_foco and dt >= t_foco)
                r = (rb if muerto else rc).copy()
                r.putalpha(r.getchannel("A").point(lambda v: int(v * u)))
                xx = int(cx - lado / 2)
                im.alpha_composite(r, (xx, y))
                colm = AMBAR if es_foco else (GRIS if muerto else BLANCO)
                d.rectangle((xx, y, xx + lado, y + lado), outline=colm + (int(230 * u),), width=5 if es_foco else 2)
                fN = ajustar(nom.upper(), "b", 24, lado + gap - 4, minimo=14, peso="SemiBold Condensed")
                _txt(d, (cx, y + lado + 20), nom.upper(), fN, colm, "mm", 255 * u)
                if muerto:
                    z = 1.0 if nom in tach else _eo((dt - t_foco) / .22)
                    m = 14
                    d.line([(xx + m, y + m), (xx + m + (lado - 2 * m) * z, y + m + (lado - 2 * m) * z)], fill=ROJO + (235,), width=9)
                    d.line([(xx + lado - m, y + m), (xx + lado - m - (lado - 2 * m) * z, y + m + (lado - 2 * m) * z)],
                           fill=ROJO + (235,), width=9)
                    if es_foco and nom not in tach and dt - t_foco < .2:
                        d.rectangle((xx - 8, y - 8, xx + lado + 8, y + lado + 8), outline=ROJO + (200,), width=6)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ MG nuevo de `cod_mandela3` (19-nov-2026)
def rachas(titulo, filas, fantasma=None, nota="NO EXISTE EN ESTE JUEGO", w=760):
    """Escalera de RACHAS DE BAJAS del multijugador: filas (bajas, nombre) que se encienden una a una (una por marca, o
    repartidas en el 60 % del tiempo) y, si hay `fantasma` = (bajas, nombre), una última fila que aparece en gris,
    PARPADEA como un recuerdo y se tacha en rojo con `nota` (la nuke en CoD 4). Marcas: una por fila + la del fantasma."""
    n = len(filas) + (1 if fantasma else 0)
    fila_h = 74
    h = 96 + n * fila_h + (54 if fantasma else 0)
    ft = fuente("mb", 24)
    fnum = fuente("b", 46, "Bold Condensed")
    fnom = fuente("b", 40, "SemiBold Condensed")
    fno = fuente("mb", 22)

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.66)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220 * _eo(dt / .3))
        _txt(d, (M + 34, M + 44), titulo.upper()[:int(max(0, (dt - .05) * 60))], ft, AMBAR, "lm", 255, track=3)
        ts = list(marcas) if marcas else [dur * .6 * (k + 1) / n for k in range(n)]
        while len(ts) < n:
            ts.append(ts[-1] + .5 if ts else .3)
        for k, (bajas, nombre) in enumerate(filas):
            y = M + 96 + k * fila_h + fila_h / 2
            u = _eo((dt - ts[k]) / .3)
            if u <= 0:
                d.rectangle((M + 30, y - 26, M + w - 30, y + 26), outline=GRIS + (90,), width=2)
                continue
            d.rectangle((M + 30, y - 26, M + w - 30, y + 26), fill=AMBAR + (int(40 * u),), outline=AMBAR + (int(220 * u),), width=3)
            _txt(d, (M + 90, y), str(bajas), fnum, AMBAR, "mm", 255 * u)
            _txt(d, (M + 150, y), nombre.upper(), fnom, BLANCO, "lm", 255 * u, track=1)
        if fantasma:
            k = len(filas)
            y = M + 96 + k * fila_h + fila_h / 2
            t0 = ts[k]
            u = _eo((dt - t0) / .3)
            if u > 0:
                parp = .55 + .45 * math.sin((dt - t0) * 14) if dt - t0 < .9 else .75
                a = 255 * u * parp
                d.rectangle((M + 30, y - 26, M + w - 30, y + 26), outline=HUESO + (int(a * .7),), width=2)
                _txt(d, (M + 90, y), str(fantasma[0]), fnum, HUESO, "mm", a)
                _txt(d, (M + 150, y), fantasma[1].upper(), fnom, HUESO, "lm", a, track=1)
                c = _eo((dt - t0 - .9) / .35)                      # tachón rojo + nota
                if c > 0:
                    x1 = M + 40 + (w - 80) * c
                    d.line((M + 40, y + 4, x1, y - 4), fill=ROJO + (255,), width=7)
                    _txt(d, (M + w / 2, y + 58), nota, fno, ROJO, "mm", 255 * c, track=2)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ consola = el CÓDIGO del juego (22-nov-2026, cod_mandela_zombies)
def consola(titulo, lineas, resalta=(), nota=None, w=1180):
    """Ventana de CÓDIGO FUENTE (script .gsc): las `lineas` se escriben en monoespaciada verde, una por marca (o repartidas
    en el 60 % del tiempo); las de índice en `resalta` se iluminan con barra ámbar al aparecer. `nota` (opcional) sale abajo
    en rojo con la última marca extra. Para demostrar un mito con el propio código (el desangrado de BO2)."""
    n = len(lineas)
    lh = 50
    h = 110 + n * lh + (70 if nota else 30)
    ft = fuente("mb", 24)
    fc = fuente("m", 30)
    fno = fuente("b", 34, "Bold Condensed")

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.74)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220 * _eo(dt / .3))
        _txt(d, (M + 34, M + 44), titulo[:int(max(0, (dt - .05) * 60))], ft, AMBAR, "lm", 255, track=2)
        d.line((M + 30, M + 76, M + w - 30, M + 76), fill=GRIS + (110,), width=1)
        k = n + (1 if nota else 0)
        ts = list(marcas) if marcas else [dur * .6 * (i + 1) / k for i in range(k)]
        while len(ts) < k:
            ts.append(ts[-1] + .6 if ts else .3)
        for i, ln in enumerate(lineas):
            y = M + 110 + i * lh
            vis = ln[:int(max(0, (dt - ts[i]) * 55))]
            if not vis:
                continue
            if i in resalta:
                u = _eo((dt - ts[i] - len(ln) / 55) / .3)
                d.rectangle((M + 24, y - 22, M + w - 24, y + 22), fill=AMBAR + (int(46 * u),), outline=AMBAR + (int(200 * u),), width=2)
            _txt(d, (M + 40, y), f"{i + 1:>2}", fc, GRIS, "lm", 200)
            escribiendo = len(vis) < len(ln)
            _txt(d, (M + 100, y), vis + ("_" if escribiendo and _cursor(dt) else ""), fc, VERDE, "lm", 255)
        if nota:
            u = _eo((dt - ts[n]) / .35)
            if u > 0:
                _txt(d, (M + w / 2, M + h - 40), nota.upper(), fno, ROJO, "mm", 255 * u, track=2)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ golpes = cuántos golpes aguantas (22-nov-2026)
def golpes(titulo, aguanta, sub=None, w=1000):
    """Contador de GOLPES: casillas que se tiñen de rojo una por marca (o repartidas); la casilla aguanta+1 cae con una
    calavera y el rótulo «CAES». `aguanta` = golpes que resistes (Juggernog = 4, caes con el 5.º)."""
    n = aguanta + 1
    lado, gap = 120, 26
    h = 230 + (40 if sub else 0)
    ft = fuente("mb", 24)
    fnum = fuente("b", 64, "Bold Condensed")
    fsub = fuente("b", 30, "SemiLight Condensed")
    x0 = (w - (n * lado + (n - 1) * gap)) / 2

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.66)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220 * _eo(dt / .3))
        _txt(d, (M + 34, M + 44), titulo.upper()[:int(max(0, (dt - .05) * 60))], ft, AMBAR, "lm", 255, track=3)
        ts = list(marcas) if marcas else [dur * .65 * (k + 1) / n for k in range(n)]
        while len(ts) < n:
            ts.append(ts[-1] + .5 if ts else .3)
        for k in range(n):
            x = M + x0 + k * (lado + gap)
            y = M + 86
            u = _eo((dt - ts[k]) / .25)
            ultimo = k == n - 1
            col = ROJO if ultimo else AMBAR
            d.rectangle((x, y, x + lado, y + lado), outline=(col if u > 0 else GRIS) + (int(110 + 140 * u),), width=4,
                        fill=col + (int((120 if ultimo else 60) * u),))
            txt = "✕" if ultimo and u > .5 else str(k + 1)
            _txt(d, (x + lado / 2, y + lado / 2), txt if u > 0 else str(k + 1), fnum, BLANCO if u > 0 else GRIS, "mm",
                 255 if u > 0 else 120)
            if ultimo and u > 0:
                _txt(d, (x + lado / 2, y + lado + 24), "CAES", fuente("mb", 26), ROJO, "mm", 255 * u, track=3)
        if sub:
            _txt(d, (M + w / 2, M + h - 30), sub, fsub, HUESO, "mm", 230 * _eo((dt - .4) / .4))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 24-nov-2026 (cod_protagonistas): placa y hoja de servicio
_ESTADOS = {"vivo": (VERDE, "VIVO"), "kia": (ROJO, "K.I.A."), "mia": (GRIS, "M.I.A."), "depende": (AMBAR, "DEPENDE DE TI"),
            "retcon": (AMBAR, "RETCON"), "vuelve": (VERDE, "REGRESA"), "desconocido": (GRIS, "DESCONOCIDO"),
            "retirado": (HUESO, "RETIRADO"), "preso": (AMBAR, "PRESO")}


def placa(nombre, lineas, estado="vivo", sub=None, w=640):
    """PLACA DE IDENTIFICACIÓN (dog tag) del protagonista: chapa metálica con la cadena, el NOMBRE grabado y `lineas`
    (rango, unidad, juego…) que se graban una por marca; la marca n+1 estampa el ESTADO (vivo | kia | mia | depende | retcon |
    vuelve | desconocido | retirado | preso). `sub` sale bajo la placa tras el sello. Sin marcas: una línea cada 0,5 s."""
    col, rot = _ESTADOS[estado]
    pw = w - 60
    ph = 250 + 46 * max(0, len(lineas) - 2)
    h = ph + 170 + (50 if sub else 0)
    fN = ajustar(nombre.upper(), "mb", 48, pw - 140)
    fL = [ajustar(s.upper(), "mb", 28, pw - 140, minimo=15) for s in lineas]
    fS = fuente("b", 76, "Bold Condensed")
    fs2 = ajustar(sub or "", "mb", 26, w - 20, minimo=14)
    chapa = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    grad = np.linspace(0, 1, ph)[:, None] * np.ones((1, pw)) + np.linspace(0, .35, pw)[None, :]
    base = (150 + 70 * np.cos(grad * 3.1 + .6)).clip(0, 255)
    arr = np.dstack([base * .96, base, base * 1.02, np.full_like(base, 235)]).clip(0, 255).astype(np.uint8)
    met = Image.fromarray(arr, "RGBA")
    m = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=58, fill=255)
    ImageDraw.Draw(m).ellipse((30, ph / 2 - 20, 70, ph / 2 + 20), fill=0)        # agujero de la cadena
    chapa.paste(met, (0, 0), m)
    ImageDraw.Draw(chapa).rounded_rectangle((8, 8, pw - 9, ph - 9), radius=52, outline=(255, 255, 255, 90), width=3)
    W_, H_ = w + 80, h + 80

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        n = len(lineas)
        mk = list(marcas or [])
        while len(mk) < n + 1:
            mk.append((mk[-1] + .5) if mk else .55)
        u = _eo(dt / .4)
        x0, y0 = 40 + (w - pw) / 2, 40 + 60 - 50 * (1 - u)
        for k in range(16):                                    # cadena de bolitas
            cx = x0 + 50 - 6 * k
            cy = y0 + ph / 2 - 8 - 5.5 * k
            d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=(205, 205, 210, int(220 * u)), outline=(90, 90, 95, int(200 * u)))
        cc = chapa.copy()
        cc.putalpha(cc.getchannel("A").point(lambda v: int(v * u)))
        im.alpha_composite(cc, (int(x0), int(y0)))
        tx = x0 + 100
        grab = (34, 36, 38)
        vis = nombre.upper()[:int(max(0, (dt - .2) * 40))]
        d.text((tx + 2, y0 + 62 + 2), vis, font=fN, fill=(255, 255, 255, 120), anchor="lm")
        d.text((tx, y0 + 62), vis, font=fN, fill=grab + (255,), anchor="lm")
        for i, (s, f) in enumerate(zip(lineas, fL)):
            if dt < mk[i]:
                continue
            vs = s.upper()[:int((dt - mk[i]) * 45)]
            yy = y0 + 126 + i * 46
            d.text((tx + 2, yy + 2), vs, font=f, fill=(255, 255, 255, 110), anchor="lm")
            d.text((tx, yy), vs, font=f, fill=grab + (255,), anchor="lm")
        t_s = mk[n]
        if dt >= t_s:
            v = dt - t_s
            s = 1.5 - .5 * _eo(v / .18)
            f = fuente("b", int(76 * s), "Bold Condensed")
            tw = _ancho(rot, fS) + 60
            sx, sy = x0 + pw - tw / 2 - 10, y0 + ph + 8
            a = 255 * _eo(v / .12)
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            dc.rectangle((sx - tw / 2, sy - 46, sx + tw / 2, sy + 46), outline=col + (int(a),), width=6,
                         fill=(0, 0, 0, int(a * .55)))
            _txt(dc, (sx, sy), rot, f, col, "mm", a, track=3)
            capa = capa.rotate(5, center=(sx, sy), resample=Image.BICUBIC)
            im.alpha_composite(capa)
            if sub and v > .3:
                _txt(d, (W_ / 2, y0 + ph + 92), sub[:int((v - .3) * 55)], fs2, col, "mm", 240)
        return _bgra(im, min(1.0, (dur - dt) / .35))
    return fn


def servicio(nombre, foto, filas, titulo="HOJA DE SERVICIO", w=1240):
    """HOJA DE SERVICIO: retrato (cara visible) y una fila por JUEGO que entra por marca: (juego, año, estado, nota), con el
    estado como píldora de color (claves de `placa`: vivo | kia | mia | depende | retcon | vuelve | desconocido | retirado | preso).
    La última fila queda resaltada en ámbar: el destino final. Sin marcas: una fila cada 0,7 s desde 0,5 s."""
    R = 300
    ret = _retrato(foto, R)
    in_x = R + 80
    in_w = w - in_x - 50
    filah = 78
    h = max(R + 110, 150 + filah * len(filas) + 30)
    fT = fuente("mb", 22)
    fN = ajustar(nombre.upper(), "b", 58, in_w, peso="Bold Condensed")
    fJ = [ajustar(j.upper(), "b", 34, in_w - 330, minimo=18, peso="SemiBold Condensed") for j, _, _, _ in filas]
    fA = fuente("mb", 22)
    fE = fuente("b", 28, "Bold Condensed")
    fNo = [ajustar(no or "", "mb", 20, in_w - 330, minimo=12) for _, _, _, no in filas]

    def fn(dt, dur, marcas):
        im, M = _cristal(w, h, alfa=.66)
        d = ImageDraw.Draw(im)
        _escuadras(d, M, M, M + w, M + h, 220)
        _txt(d, (M + 40, M + 36), titulo + " / EXPEDIENTE 141", fT, GRIS, "lm", 230, track=2)
        u = _eo(dt / .35)
        rx, ry = M + 40, M + 70
        rr = ret.copy()
        rr.putalpha(rr.getchannel("A").point(lambda v: int(v * u)))
        im.alpha_composite(rr, (rx, ry))
        d.rectangle((rx, ry, rx + R, ry + R), outline=BLANCO + (int(200 * u),), width=3)
        _txt(d, (M + in_x, M + 96), nombre.upper(), fN, BLANCO, "lm", 255 * _eo((dt - .15) / .3), track=1)
        d.line([(M + in_x, M + 134), (M + in_x + in_w * _eo((dt - .3) / .4), M + 134)], fill=AMBAR + (200,), width=2)
        mk = list(marcas or [])
        while len(mk) < len(filas):
            mk.append((mk[-1] + .7) if mk else .5)
        y = M + 150 + filah / 2
        for i, ((jg, an, est, no), fj, fno) in enumerate(zip(filas, fJ, fNo)):
            if dt >= mk[i]:
                a = _eo((dt - mk[i]) / .25)
                ult = i == len(filas) - 1
                if ult:
                    d.rectangle((M + in_x - 14, y - filah / 2 + 4, M + w - 30, y + filah / 2 - 4), fill=AMBAR + (int(34 * a),),
                                outline=AMBAR + (int(150 * a),), width=2)
                _txt(d, (M + in_x, y - (12 if no else 0)), jg.upper(), fj, AMBAR if ult else BLANCO, "lm", 255 * a)
                if no:
                    _txt(d, (M + in_x, y + 22), no, fno, HUESO, "lm", 220 * a)
                _txt(d, (M + w - 270, y), str(an), fA, GRIS, "mm", 230 * a)
                col, rot = _ESTADOS[est]
                pw_ = _ancho(rot, fE) + 34
                px = M + w - 40 - pw_ / 2
                d.rounded_rectangle((px - pw_ / 2, y - 22, px + pw_ / 2, y + 22), radius=8, fill=col + (int(60 * a),),
                                    outline=col + (int(240 * a),), width=3)
                _txt(d, (px, y), rot, fE, col, "mm", 255 * a, track=1)
            y += filah
        return _salida(im, dt, dur)
    return fn
