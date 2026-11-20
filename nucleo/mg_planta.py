# -*- coding: utf-8 -*-
"""MOTION GRAPHICS de MIL POR MINUTO (canal de cómo se fabrican las marcas; primer uso `mpm_takis`, 19-nov-2026).
Interfaz = la de una PLANTA INDUSTRIAL: plano de ingeniería (cian sobre azul acero), naranja de seguridad, amarillo de peligro,
franjas negro/amarillo, letra condensada (Bahnschrift) en MAYÚSCULAS y monoespaciada para lecturas de máquina.
Fichas translúcidas: el clip sigue debajo (regla de canal de la Secuencia YT).
    import mg_planta as P
  contador_produccion(por_seg, unidad, desde)   FIRMA DEL CANAL: contador en la esquina de cuántas piezas salieron de la planta
                                    desde que empezó el video (FX con de=0 → dt = segundo del video). Cifra real ÷ segundos.
  plano(estaciones, activa, titulo) FIRMA DEL CANAL: PLANO de la línea, estación por estación; la bolsa/pieza avanza por la banda
                                    hasta la estación `activa`, que se enciende en naranja (pantalla completa, 1920×1080)
  estacion(num, total, nombre, porque)  tarjeta de ESTACIÓN 03/10 con el porqué en una línea
  cifra(valor, prefijo, unidad, titulo, decimales)  cifra GIGANTE amarilla con contorno que rueda (dinero o volumen)
  cuenta(filas, resultado, titulo)  la cuenta hecha en voz alta (÷ 365…): una fila por marca y el resultado al final
  etiqueta(texto, sub)              cinta de peligro con una palabra clave en MAYÚSCULAS («REVISADAS»)
  trivia(pregunta, opciones, correcta)  pregunta con 3 opciones A/B/C; `correcta` = índice que se enciende (None = sin respuesta)
  sellos(textos)                    octágonos negros de advertencia de la NOM-051 (México), uno por marca
  barras(titulo, filas, unidad)     barras horizontales que crecen (comparar marcas, países, años); una por marca
  ingredientes(lista, resalta)      etiqueta de ingredientes que se escribe; los índices de `resalta` se marcan en naranja
  linea_tiempo(titulo, hitos)       años sobre una banda transportadora; un hito por marca
Probar SIEMPRE con una hoja de cuadros (`hoja()`) antes de `fx`.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

NARANJA, AMARILLO, ACERO = (255, 106, 26), (255, 196, 0), (15, 18, 22)
BLANCO, HUESO, GRIS = (246, 246, 240), (214, 210, 196), (150, 156, 160)
CIAN, AZUL = (120, 220, 255), (14, 38, 62)
VERDE, ROJO = (120, 230, 120), (232, 60, 48)
_F = {"b": "C:/Windows/Fonts/bahnschrift.ttf", "m": "C:/Windows/Fonts/consola.ttf", "mb": "C:/Windows/Fonts/consolab.ttf",
      "i": "C:/Windows/Fonts/impact.ttf"}
_fc = {}
_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))


def fuente(estilo, tam, peso=None):
    k = (estilo, int(tam), peso)
    if k not in _fc:
        f = ImageFont.truetype(_F[estilo], int(tam))
        if estilo == "b":
            try:
                f.set_variation_by_name(peso or "Bold Condensed")
            except Exception:
                pass
        _fc[k] = f
    return _fc[k]


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _reb(u):
    u = max(0.0, min(1.0, u))
    c = 2.0
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def _bgra(im, alfa=1.0):
    a = np.asarray(im.convert("RGBA")).copy()
    if alfa < 1:
        a[..., 3] = (a[..., 3] * max(0.0, alfa)).astype(np.uint8)
    return a[..., [2, 1, 0, 3]]


def ajustar(s, estilo, tam, ancho, minimo=14, peso=None):
    while tam > minimo and _D.textlength(s, font=fuente(estilo, tam, peso)) > ancho:
        tam -= 2
    return fuente(estilo, tam, peso)


def _txt(d, xy, s, f, color, ancla="la", alfa=255, track=0, stroke=0, stroke_color=ACERO):
    a = int(max(0, min(255, alfa)))
    if a <= 0 or not s:
        return
    if track:
        w = sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)
        x, y = xy
        if ancla[0] == "m":
            x -= w / 2
        elif ancla[0] == "r":
            x -= w
        for c in s:
            d.text((x, y), c, font=f, fill=color + (a,), anchor="l" + ancla[1], stroke_width=stroke,
                   stroke_fill=stroke_color + (a,))
            x += d.textlength(c, font=f) + track
        return
    d.text(xy, s, font=f, fill=color + (a,), anchor=ancla, stroke_width=stroke, stroke_fill=stroke_color + (a,))


def _num(v, decimales=0):
    """Formato de México: coma de miles, punto decimal."""
    return f"{v:,.{decimales}f}"


def _panel(w, h, M=34, alfa=.70, color=ACERO):
    """Placa de acero translúcida con sombra, filo naranja arriba y remaches en las esquinas."""
    W, H = w + 2 * M, h + 2 * M
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((M, M + 8, M + w, M + h + 8), 10, fill=(0, 0, 0, 120))
    im = sombra.filter(ImageFilter.GaussianBlur(14))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, M, M + w, M + h), 10, fill=color + (int(255 * alfa),), outline=(70, 76, 82, 230), width=2)
    d.rectangle((M + 10, M, M + w - 10, M + 6), fill=NARANJA + (255,))
    for x, y in ((M + 16, M + 22), (M + w - 16, M + 22), (M + 16, M + h - 16), (M + w - 16, M + h - 16)):
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(120, 126, 132, 255))
        d.ellipse((x - 2, y - 3, x + 2, y + 1), fill=(200, 204, 208, 255))
    return im, M


def _franjas(d, x0, y0, x1, y1, alfa=255, paso=34, off=0):
    """Franjas de peligro negro/amarillo a 45° dentro del rectángulo."""
    d.rectangle((x0, y0, x1, y1), fill=AMARILLO + (alfa,))
    h = y1 - y0
    x = x0 - h + (off % (2 * paso))
    while x < x1:
        pts = [(max(x0, x), y1), (min(x1, x + h), y0)]
        poly = [(x, y1), (x + h, y0), (x + h + paso, y0), (x + paso, y1)]
        poly = [(min(max(px, x0), x1), py) for px, py in poly]
        d.polygon(poly, fill=(20, 20, 20, alfa))
        x += 2 * paso


def _entrada(im, dt, dur, abre=.32, desde="izq"):
    """Entra deslizando con un rebote corto; sale con fundido."""
    u = _eo(dt / abre)
    W, H = im.size
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dx = int((-1 if desde == "izq" else 1) * 120 * (1 - u))
    out.alpha_composite(im, (dx, 0) if dx > -W and dx < W else (0, 0))
    return _bgra(out, min(u, max(0.0, (dur - dt) / .35)))


# ------------------------------------------------------------------ contador de producción (firma del canal)
def contador_produccion(por_seg, unidad="BOLSAS", titulo="SALIERON DE LA LÍNEA DESDE QUE EMPEZÓ ESTE VIDEO", desde=0.0,
                        nota=None, w=560, prefijo=""):
    """Contador fijo de esquina: piezas producidas = desde + por_seg × dt. Ponerlo con de=0, a=fin, x≈.86, y≈.10.
    `nota` = la fuente del cálculo en chiquito («estimado: 1 bolsa cada 0,4 s»)."""
    ft = fuente("b", 20, "SemiBold Condensed")
    fu = fuente("b", 26, "Bold Condensed")
    fn_ = fuente("b", 16, "Light Condensed")
    h = 118 if nota else 100

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, M=20, alfa=.62)
        d = ImageDraw.Draw(im)
        _franjas(d, M + 8, M + 12, M + 30, M + h - 10, 255, paso=9, off=int(dt * 30))
        v = desde + por_seg * dt
        s = prefijo + _num(int(v))                  # prefijo="$" para dinero (mpm_takis, 19-nov-2026)
        f = ajustar(s, "mb", 52, w - 190)
        _txt(d, (M + 48, M + 30), titulo, ajustar(titulo, "b", 20, w - 70, peso="SemiBold Condensed"), HUESO, "lm", 235)
        _txt(d, (M + 48, M + 70), s, f, AMARILLO, "lm", 255)
        _txt(d, (M + w - 18, M + 72), unidad, fu, NARANJA, "rm", 255)
        if nota:
            _txt(d, (M + 48, M + 104), nota, fn_, GRIS, "lm", 220)
        # luz de máquina que parpadea
        on = (dt * 2.4) % 1 < .5
        d.ellipse((M + w - 30, M + 18, M + w - 18, M + 30), fill=(VERDE if on else (40, 70, 40)) + (255,))
        return _bgra(im, min(_eo(dt / .5), max(0.0, (dur - dt) / .5)))
    return fn


# ------------------------------------------------------------------ PLANO de la línea (firma del canal)
def _icono(d, tipo, cx, cy, s, col, a, t):
    """Íconos de máquina dibujados a línea (estilo plano técnico)."""
    c = col + (a,)
    lw = max(2, int(s * .06))
    if tipo == "silo":
        d.rectangle((cx - s * .3, cy - s * .45, cx + s * .3, cy + s * .2), outline=c, width=lw)
        d.polygon([(cx - s * .3, cy + s * .2), (cx + s * .3, cy + s * .2), (cx, cy + s * .48)], outline=c, width=lw)
        d.arc((cx - s * .3, cy - s * .62, cx + s * .3, cy - s * .28), 180, 360, fill=c, width=lw)
    elif tipo == "olla":
        d.rounded_rectangle((cx - s * .4, cy - s * .2, cx + s * .4, cy + s * .4), 8, outline=c, width=lw)
        for k in range(3):
            yy = cy - s * .3 - ((t * 30 + k * 12) % 26)
            d.arc((cx - s * .25 + k * s * .18, yy - 8, cx - s * .1 + k * s * .18, yy + 8), 200, 340, fill=c, width=lw)
    elif tipo == "molino":
        for k in (-1, 1):
            r = s * .22
            ox = cx + k * r
            d.ellipse((ox - r, cy - r, ox + r, cy + r), outline=c, width=lw)
            ang = t * 4 * k
            d.line((ox, cy, ox + r * math.cos(ang), cy + r * math.sin(ang)), fill=c, width=lw)
    elif tipo == "laminadora":
        d.rectangle((cx - s * .45, cy + s * .1, cx + s * .45, cy + s * .18), outline=c, width=lw)
        for k in (-1, 1):
            r = s * .16
            d.ellipse((cx - r, cy + k * r * 1.05 - r - s * .05, cx + r, cy + k * r * 1.05 + r - s * .05), outline=c, width=lw)
    elif tipo == "corte":
        d.rectangle((cx - s * .45, cy + s * .15, cx + s * .45, cy + s * .23), outline=c, width=lw)
        yy = cy - s * .3 + s * .25 * abs(math.sin(t * 5))
        d.polygon([(cx - s * .18, yy - s * .15), (cx + s * .18, yy - s * .15), (cx, yy + s * .1)], outline=c, width=lw)
    elif tipo == "enrollado":
        for k in range(3):
            r = s * (.1 + k * .09)
            d.arc((cx - r, cy - r, cx + r, cy + r), 30 + t * 90, 330 + t * 90, fill=c, width=lw)
    elif tipo == "freidora":
        d.rectangle((cx - s * .45, cy - s * .05, cx + s * .45, cy + s * .35), outline=c, width=lw)
        for k in range(5):
            bx = cx - s * .35 + k * s * .17
            by = cy + s * .25 - ((t * 40 + k * 9) % (s * .28))
            d.ellipse((bx - 4, by - 4, bx + 4, by + 4), outline=c, width=2)
    elif tipo == "tambor":
        r = s * .32
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=lw)
        ang = t * 3
        for k in range(4):
            a2 = ang + k * math.pi / 2
            d.line((cx, cy, cx + r * math.cos(a2), cy + r * math.sin(a2)), fill=c, width=max(1, lw - 1))
    elif tipo == "bolsa":
        d.polygon([(cx - s * .25, cy - s * .38), (cx + s * .25, cy - s * .38), (cx + s * .3, cy + s * .38),
                   (cx - s * .3, cy + s * .38)], outline=c, width=lw)
        d.line((cx - s * .25, cy - s * .26, cx + s * .25, cy - s * .26), fill=c, width=lw)
    elif tipo == "caja":
        d.rectangle((cx - s * .35, cy - s * .2, cx + s * .35, cy + s * .35), outline=c, width=lw)
        d.line((cx - s * .35, cy - s * .2, cx - s * .2, cy - s * .38), fill=c, width=lw)
        d.line((cx + s * .35, cy - s * .2, cx + s * .5, cy - s * .38), fill=c, width=lw)
    elif tipo == "ojo":            # control de calidad
        d.ellipse((cx - s * .4, cy - s * .2, cx + s * .4, cy + s * .2), outline=c, width=lw)
        r = s * .12
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
        d.line((cx - s * .48, cy - s * .38 + (t * 60 % (s * .76)), cx + s * .48, cy - s * .38 + (t * 60 % (s * .76))),
               fill=NARANJA + (a,), width=2)
    elif tipo == "camion":
        d.rectangle((cx - s * .45, cy - s * .2, cx + s * .12, cy + s * .2), outline=c, width=lw)
        d.rectangle((cx + s * .12, cy - s * .05, cx + s * .4, cy + s * .2), outline=c, width=lw)
        for xx in (cx - s * .3, cx + s * .25):
            d.ellipse((xx - s * .08, cy + s * .14, xx + s * .08, cy + s * .3), outline=c, width=lw)
    else:                          # máquina genérica
        d.rectangle((cx - s * .38, cy - s * .3, cx + s * .38, cy + s * .3), outline=c, width=lw)
        d.line((cx - s * .38, cy, cx + s * .38, cy), fill=c, width=lw)


def plano(estaciones, activa=None, titulo="LÍNEA DE PRODUCCIÓN", sub=None, w=1920, h=1080):
    """Plano de la línea a pantalla completa. estaciones = [(nombre, icono)] (íconos: silo olla molino laminadora corte
    enrollado freidora tambor bolsa caja ojo camion). `activa` = índice que se enciende (la pieza viaja hasta ahí);
    None = recorrido completo de la primera a la última con las marcas de la voz (una marca por estación).
    Las estaciones van en dos filas (serpentina) si son más de 6."""
    n = len(estaciones)
    filas = 1 if n <= 6 else 2
    por_fila = math.ceil(n / filas)
    mx, top = 150, 330 if filas == 2 else 470
    paso = (w - 2 * mx) / max(1, por_fila - 1)
    alto_fila = 380
    pos = []
    for i in range(n):
        fi, k = divmod(i, por_fila)
        x = mx + (k if fi % 2 == 0 else por_fila - 1 - k) * paso
        pos.append((x, top + fi * alto_fila))
    ftit = fuente("b", 64, "Bold Condensed")
    fsub = fuente("b", 30, "Light Condensed")
    fnum = fuente("mb", 24)
    fest = [ajustar(e[0].upper(), "b", 30, paso * .92 if n > 1 else 400, peso="SemiBold Condensed") for e in estaciones]

    # fondo: papel de plano azul con rejilla (se cachea)
    fondo = Image.new("RGBA", (w, h), AZUL + (255,))
    d0 = ImageDraw.Draw(fondo)
    for x in range(0, w, 40):
        d0.line((x, 0, x, h), fill=(40, 80, 112, 255 if x % 200 == 0 else 120), width=1)
    for y in range(0, h, 40):
        d0.line((0, y, w, y), fill=(40, 80, 112, 255 if y % 200 == 0 else 120), width=1)
    d0.rectangle((24, 24, w - 24, h - 24), outline=CIAN + (160,), width=3)
    d0.rectangle((w - 520, h - 130, w - 24, h - 24), outline=CIAN + (160,), width=2)
    _txt(d0, (w - 500, h - 100), "MIL POR MINUTO · PLANO DE LÍNEA", fuente("mb", 22), CIAN, "lm", 200)
    _txt(d0, (w - 500, h - 60), "ESCALA: NINGUNA · DIBUJO DIDÁCTICO", fuente("m", 20), CIAN, "lm", 160)
    vig = Image.new("L", (w, h), 0)
    ImageDraw.Draw(vig).ellipse((-w * .2, -h * .3, w * 1.2, h * 1.3), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    sombra = Image.new("RGBA", (w, h), (0, 8, 18, 255))
    fondo = Image.composite(fondo, sombra, vig)

    def fn(dt, dur, marcas):
        im = fondo.copy()
        d = ImageDraw.Draw(im)
        ap = _eo(dt / .6)
        _txt(d, (80, 110), titulo.upper(), ftit, BLANCO, "lm", 255 * ap, track=2)
        if sub:
            _txt(d, (82, 170), sub, fsub, CIAN, "lm", 230 * _eo((dt - .3) / .4))
        # hasta dónde llega la pieza
        if activa is None:
            if marcas:
                llegado = sum(1 for m in marcas if dt >= m) - 1
            else:
                llegado = int(min(n - 1, dt / max(.1, dur * .85) * n))
            objetivo = max(0, llegado)
            t_ult = marcas[objetivo] if marcas and objetivo < len(marcas) else 0
        else:
            objetivo = activa
            t_ult = .5
        # banda (tramos entre estaciones), se dibuja de golpe con la entrada
        dibujo = _eo((dt - .1) / .9)
        tramos = n - 1
        for i in range(tramos):
            if i / max(1, tramos) > dibujo:
                break
            (x0, y0), (x1, y1) = pos[i], pos[i + 1]
            hecho = i < objetivo
            col = NARANJA if hecho else CIAN
            if abs(y0 - y1) < 1:
                d.line((x0, y0 + 95, x1, y1 + 95), fill=col + (230,), width=6)
                for xx in np.arange(min(x0, x1), max(x0, x1), 28):
                    off = (dt * 60) % 28
                    d.line((xx + off, y0 + 89, xx + off, y0 + 101), fill=col + (140,), width=2)
            else:                                   # bajada de la serpentina
                xx = x0
                d.line((xx, y0 + 95, xx + (60 if xx > w / 2 else -60), y0 + 95), fill=col + (230,), width=6)
                xb = xx + (60 if xx > w / 2 else -60)
                d.line((xb, y0 + 95, xb, y1 + 95), fill=col + (230,), width=6)
                d.line((xb, y1 + 95, x1, y1 + 95), fill=col + (230,), width=6)
        # estaciones
        for i, ((nom, ico), (x, y)) in enumerate(zip(estaciones, pos)):
            ai = 255 * _eo((dt - .15 - i * .06) / .4)
            on = i == objetivo
            pasado = i < objetivo
            col = NARANJA if on else (AMARILLO if pasado else CIAN)
            bw = 96
            if on:
                pul = 1 + .05 * math.sin(dt * 6)
                for k in range(3, 0, -1):
                    rr = bw * pul + k * 10
                    d.rounded_rectangle((x - rr, y - rr, x + rr, y + rr), 18, outline=NARANJA + (int(ai * .12 * k),), width=3)
            d.rounded_rectangle((x - bw, y - bw, x + bw, y + bw), 14, fill=(8, 22, 38, int(ai * .85)),
                                outline=col + (int(ai),), width=4 if on else 2)
            _icono(d, ico, x, y - 10, 120, col, int(ai), dt if (on or activa is None) else 0)
            _txt(d, (x - bw + 12, y - bw + 18), f"{i + 1:02d}", fnum, col, "lm", ai)
            _txt(d, (x, y + bw + 34), nom.upper(), fest[i], BLANCO if (on or pasado) else HUESO, "mm", ai, track=1)
        # la pieza que viaja (una bolsa naranja) hasta la estación objetivo
        if objetivo >= 0:
            k = _eo((dt - t_ult) / .8) if activa is None else _eo((dt - .4) / 1.4)
            if activa is None:
                desde_i = max(0, objetivo - 1)
            else:
                desde_i = 0
            xs = np.array([p[0] for p in pos[desde_i:objetivo + 1]] or [pos[0][0]])
            ys = np.array([p[1] for p in pos[desde_i:objetivo + 1]] or [pos[0][1]])
            if len(xs) > 1:
                L = np.r_[0, np.cumsum(np.hypot(np.diff(xs), np.diff(ys)))]
                s_ = k * L[-1]
                j = min(len(L) - 2, int(np.searchsorted(L, s_, side="right") - 1))
                u = (s_ - L[j]) / max(1e-6, L[j + 1] - L[j])
                px, py = xs[j] + (xs[j + 1] - xs[j]) * u, ys[j] + (ys[j + 1] - ys[j]) * u
            else:
                px, py = xs[0], ys[0]
            py += 95 - 22
            d.rounded_rectangle((px - 16, py - 20, px + 16, py + 20), 5, fill=NARANJA + (255,), outline=BLANCO + (255,), width=2)
        return _bgra(im, min(_eo(dt / .35), max(0.0, (dur - dt) / .35)))
    return fn


# ------------------------------------------------------------------ tarjeta de estación
def estacion(num, total, nombre, porque=None, w=980):
    fc = fuente("mb", 26)
    fnom = ajustar(nombre.upper(), "b", 92, w - 80)
    fp = ajustar(porque, "b", 34, w - 80, peso="Light Condensed") if porque else None
    h = 230 if porque else 176

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.72)
        d = ImageDraw.Draw(im)
        _franjas(d, M + 2, M + h - 18, M + w - 2, M + h - 2, 230, paso=16, off=int(dt * 40))
        cab = f"ESTACIÓN {num:02d} / {total:02d}"
        _txt(d, (M + 36, M + 40), cab[:int(max(0, dt * 50))], fc, NARANJA, "lm", 255, track=3)
        k = _eo((dt - .15) / .35)
        _txt(d, (M + 34 - 40 * (1 - k), M + 108), nombre.upper(), fnom, BLANCO, "lm", 255 * k, track=1)
        if fp:
            _txt(d, (M + 36, M + 176), porque, fp, HUESO, "lm", 235 * _eo((dt - .5) / .4))
        return _entrada(im, dt, dur)
    return fn


# ------------------------------------------------------------------ cifra gigante
def cifra(valor, prefijo="", unidad="", titulo="", decimales=0, desde=0, color=AMARILLO, w=1500, h=420, texto=None):
    """Cifra ENORME amarilla con contorno grueso que rueda hasta `valor`; `texto` fija la cadena final (p. ej. «1,100 MILLONES»)
    y entonces rueda solo la parte numérica de `valor`. Sin panel: va directo sobre el clip (con sombra)."""
    ft = fuente("b", 46, "SemiBold Condensed")

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        k = _eo((dt - .1) / 1.1)
        v = desde + (valor - desde) * k
        s = prefijo + _num(v, decimales) + (" " + unidad if unidad else "")
        if texto and k >= 1:
            s = texto
        f = ajustar(s, "b", 230, w - 60)
        sc = _reb((dt) / .5)
        sombra = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ds = ImageDraw.Draw(sombra)
        _txt(ds, (w / 2 + 8, h * .58 + 10), s, f, (0, 0, 0), "mm", 200, stroke=14, stroke_color=(0, 0, 0))
        im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(10)))
        _txt(d, (w / 2, h * .58), s, f, color, "mm", 255, stroke=12, stroke_color=ACERO)
        if titulo:
            ka = _eo((dt - .25) / .3)
            tw = d.textlength(titulo.upper(), font=ft) + 60
            d.rectangle((w / 2 - tw / 2, 12, w / 2 + tw / 2, 78), fill=NARANJA + (int(240 * ka),))
            _txt(d, (w / 2, 45), titulo.upper(), ft, ACERO, "mm", 255 * ka, track=2)
        if abs(sc - 1) > .01:
            W, H = im.size
            p = im.resize((max(1, int(W * sc)), max(1, int(H * sc))), Image.BICUBIC)
            out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            out.alpha_composite(p.crop((max(0, (p.width - W) // 2), max(0, (p.height - H) // 2),
                                        max(0, (p.width - W) // 2) + min(W, p.width), max(0, (p.height - H) // 2) + min(H, p.height))),
                                (max(0, (W - p.width) // 2), max(0, (H - p.height) // 2)))
            im = out
        return _bgra(im, min(_eo(dt / .2), max(0.0, (dur - dt) / .3)))
    return fn


# ------------------------------------------------------------------ la cuenta en voz alta
def cuenta(filas, resultado, titulo="LA CUENTA", w=900):
    """filas = ["3,600 MILLONES AL AÑO", "÷ 365 DÍAS"]; resultado = "≈ 9.8 MILLONES AL DÍA". Una fila por marca,
    el resultado en la última marca (o al 70 %)."""
    fc = fuente("mb", 28)
    resultado = resultado.replace("≈", "~")          # Bahnschrift no trae ≈
    ff = [ajustar(s, "mb", 54, w - 100) for s in filas]
    fr = ajustar(resultado, "b", 76, w - 80)
    h = 120 + 78 * len(filas) + 120

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.74)
        d = ImageDraw.Draw(im)
        _txt(d, (M + 40, M + 50), titulo.upper(), fc, NARANJA, "lm", 255, track=3)
        for i, s in enumerate(filas):
            t0 = marcas[i] if i < len(marcas) else .3 + i * .6
            k = _eo((dt - t0) / .3)
            _txt(d, (M + w - 50 + 30 * (1 - k), M + 130 + 78 * i), s, ff[i], BLANCO, "rm", 255 * k)
        yl = M + 120 + 78 * len(filas) + 4
        t1 = marcas[len(filas)] if len(marcas) > len(filas) else max(.3 + len(filas) * .6, dur * .6)
        kl = _eo((dt - t1 + .2) / .3)
        d.line((M + w - 50 - (w - 100) * kl, yl, M + w - 50, yl), fill=AMARILLO + (255,), width=4)
        k = _reb((dt - t1) / .45)
        _txt(d, (M + w - 50, yl + 62), resultado, fr, AMARILLO, "rm", 255 * min(1, max(0, (dt - t1) / .15)))
        return _entrada(im, dt, dur, desde="der")
    return fn


# ------------------------------------------------------------------ cinta con palabra clave
def etiqueta(texto, sub=None, giro=-3.0):
    f = fuente("b", 110, "Bold Condensed")
    fs = fuente("b", 34, "SemiBold Condensed")
    tw = _D.textlength(texto.upper(), font=f) + 120
    W, H = int(tw + 80), 260 if sub else 210

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        k = _eo(dt / .3)
        x1 = 40 + (tw) * k
        d.rectangle((40, 30, x1, 170), fill=AMARILLO + (255,))
        _franjas(d, 40, 30, x1, 46, 255, paso=12)
        _franjas(d, 40, 154, x1, 170, 255, paso=12)
        _txt(d, (40 + tw / 2, 102), texto.upper(), f, ACERO, "mm", 255 * _eo((dt - .15) / .2), track=3)
        if sub:
            _txt(d, (40 + tw / 2, 212), sub, fs, BLANCO, "mm", 255 * _eo((dt - .3) / .3), stroke=4)
        im = im.rotate(giro, Image.BICUBIC, expand=False)
        return _bgra(im, min(1.0, max(0.0, (dur - dt) / .3)))
    return fn


# ------------------------------------------------------------------ trivia
def trivia(pregunta, opciones, correcta=None, cabecera="TRIVIA · RESPUESTA AL FINAL DEL VIDEO", w=1180):
    """Tres opciones A/B/C que entran una por marca; con `correcta`, la opción se enciende en la última marca (o al 75 %)."""
    fc = fuente("mb", 26)
    fp = ajustar(pregunta, "b", 56, w - 80)
    fo = [ajustar(o, "b", 46, w - 210, peso="SemiBold Condensed") for o in opciones]
    h = 170 + 104 * len(opciones)

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.76)
        d = ImageDraw.Draw(im)
        _txt(d, (M + 40, M + 46), cabecera, fc, NARANJA, "lm", 255, track=2)
        _txt(d, (M + 40, M + 112), pregunta, fp, BLANCO, "lm", 255 * _eo((dt - .1) / .3))
        tr = (marcas[len(opciones)] if len(marcas) > len(opciones) else dur * .75) if correcta is not None else 1e9
        for i, o in enumerate(opciones):
            t0 = marcas[i] if i < len(marcas) else .5 + i * .5
            k = _eo((dt - t0) / .3)
            y = M + 190 + 104 * i
            ok = dt >= tr and i == correcta
            mal = dt >= tr and i != correcta
            col = VERDE if ok else ((90, 96, 100) if mal else AMARILLO)
            d.rounded_rectangle((M + 40 + 60 * (1 - k), y - 40, M + w - 40, y + 40), 10,
                                fill=(30, 34, 38, int(220 * k)), outline=col + (int(255 * k),), width=4 if ok else 2)
            d.rectangle((M + 40 + 60 * (1 - k), y - 40, M + 120 + 60 * (1 - k), y + 40), fill=col + (int(255 * k),))
            _txt(d, (M + 80 + 60 * (1 - k), y), "ABC"[i], fuente("b", 50), ACERO, "mm", 255 * k)
            _txt(d, (M + 150 + 60 * (1 - k), y), o, fo[i], (130, 134, 138) if mal else BLANCO, "lm", 255 * k)
        return _entrada(im, dt, dur)
    return fn


# ------------------------------------------------------------------ sellos de advertencia (NOM-051)
def sellos(textos, w=None):
    """Octágonos negros con borde blanco tipo etiquetado frontal de México («EXCESO / SODIO»); uno por marca."""
    n = len(textos)
    lado = 250
    W = w or (lado + 30) * n + 40
    H = lado + 60
    f1 = fuente("b", 50, "Bold Condensed")
    f2 = fuente("b", 26, "SemiBold Condensed")

    def octo(cx, cy, r):
        return [(cx + r * math.cos(math.radians(22.5 + 45 * k)), cy + r * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for i, t in enumerate(textos):
            t0 = marcas[i] if i < len(marcas) else .2 + i * .35
            k = _reb((dt - t0) / .35)
            if dt < t0:
                continue
            cx, cy = 20 + lado / 2 + 15 + i * (lado + 30), H / 2
            r = lado / 2 * k
            d.polygon(octo(cx, cy, r), fill=(255, 255, 255, 255))
            d.polygon(octo(cx, cy, r * .92), fill=(10, 10, 10, 255))
            if k > .7:
                partes = t.upper().split(" ", 1)
                _txt(d, (cx, cy - 26), partes[0], f1, BLANCO, "mm")
                if len(partes) > 1:
                    _txt(d, (cx, cy + 22), partes[1], ajustar(partes[1], "b", 34, lado * .7), BLANCO, "mm")
                _txt(d, (cx, cy + 66), "SECRETARÍA DE SALUD", ajustar("SECRETARÍA DE SALUD", "b", 15, lado * .6), BLANCO, "mm", 220)
        return _bgra(im, min(1.0, max(0.0, (dur - dt) / .3)))
    return fn


# ------------------------------------------------------------------ barras
def barras(titulo, filas, unidad="", w=1300, decimales=1, resalta=0):
    """filas = [(nombre, valor)]; una barra por marca; `resalta` = índice en naranja (el resto acero claro)."""
    fc = fuente("b", 44, "Bold Condensed")
    fn_ = fuente("b", 36, "SemiBold Condensed")
    fv = fuente("mb", 34)
    h = 120 + 90 * len(filas)
    vmax = max(v for _, v in filas) or 1

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.74)
        d = ImageDraw.Draw(im)
        _txt(d, (M + 40, M + 56), titulo.upper(), fc, BLANCO, "lm", 255, track=1)
        x0 = M + 320
        x1 = M + w - 40 - max(d.textlength(_num(v_, decimales) + unidad, font=fv) for _, v_ in filas) - 24
        for i, (nom, v) in enumerate(filas):
            t0 = marcas[i] if i < len(marcas) else .3 + i * .4
            k = _eo((dt - t0) / .7)
            y = M + 130 + 90 * i
            col = NARANJA if i == resalta else (170, 176, 182)
            _txt(d, (M + 300, y), nom.upper(), ajustar(nom.upper(), "b", 36, 270, peso="SemiBold Condensed"), BLANCO, "rm",
                 255 * min(1, (dt - t0 + .3) / .3))
            d.rectangle((x0, y - 26, x0 + (x1 - x0) * v / vmax * k, y + 26), fill=col + (255,))
            if k > .05:
                _txt(d, (x0 + (x1 - x0) * v / vmax * k + 14, y), _num(v * k, decimales) + unidad, fv, AMARILLO, "lm", 255 * k)
        return _entrada(im, dt, dur)
    return fn


# ------------------------------------------------------------------ ingredientes
def ingredientes(lista, resalta=(), titulo="INGREDIENTES", w=1100):
    """Etiqueta del empaque que se escribe; los índices de `resalta` se marcan con un recuadro naranja por marca."""
    fc = fuente("b", 44, "Bold Condensed")
    fi = fuente("b", 34, "SemiBold Condensed")
    # acomodar en renglones
    lineas, act = [], []
    for i, s in enumerate(lista):
        prueba = act + [(i, s)]
        texto = ", ".join(x for _, x in prueba)
        if _D.textlength(texto, font=fi) > w - 80 and act:
            lineas.append(act)
            act = [(i, s)]
        else:
            act = prueba
    if act:
        lineas.append(act)
    h = 120 + 52 * len(lineas)

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.80, color=(246, 244, 236))
        d = ImageDraw.Draw(im)
        _txt(d, (M + 40, M + 56), titulo.upper(), fc, ACERO, "lm", 255)
        vis = int(max(0, (dt - .2) * 120))
        cuenta_ = 0
        for r, fila in enumerate(lineas):
            x = M + 40
            y = M + 118 + 52 * r
            for j, (i, s) in enumerate(fila):
                txt = s + ("," if (r < len(lineas) - 1 or j < len(fila) - 1) else ".")
                visibles = max(0, min(len(txt), vis - cuenta_))
                cuenta_ += len(txt) + 1
                if visibles <= 0:
                    continue
                ancho = d.textlength(txt + " ", font=fi)
                if i in resalta:
                    k_ = list(resalta).index(i)
                    t0 = marcas[k_] if k_ < len(marcas) else 1e9
                    if dt >= t0:
                        k = _eo((dt - t0) / .3)
                        d.rounded_rectangle((x - 6, y - 24, x + d.textlength(s, font=fi) + 6, y + 24), 6,
                                            outline=NARANJA + (int(255 * k),), width=4, fill=NARANJA + (int(60 * k),))
                _txt(d, (x, y), txt[:visibles], fi, ACERO, "lm", 255)
                x += ancho
        return _entrada(im, dt, dur)
    return fn


# ------------------------------------------------------------------ línea de tiempo sobre una banda
def linea_tiempo(titulo, hitos, w=1700, h=420):
    """hitos = [(año, texto)]; cada hito entra por marca como una caja sobre la banda transportadora que corre."""
    n = len(hitos)
    fc = fuente("b", 48, "Bold Condensed")
    fa = fuente("b", 64, "Bold Condensed")
    ft = [ajustar(t, "b", 28, (w - 160) / max(1, n) - 20, peso="SemiBold Condensed") for _, t in hitos]

    def fn(dt, dur, marcas):
        im, M = _panel(w, h, alfa=.72)
        d = ImageDraw.Draw(im)
        _txt(d, (M + 40, M + 56), titulo.upper(), fc, BLANCO, "lm", 255, track=1)
        yb = M + h - 90
        d.rectangle((M + 30, yb, M + w - 30, yb + 22), fill=(60, 64, 70, 255))
        off = (dt * 80) % 40
        for xx in np.arange(M + 30, M + w - 30, 40):
            d.line((xx + off, yb + 4, xx + off, yb + 18), fill=(110, 116, 122, 255), width=3)
        paso = (w - 160) / max(1, n)
        for i, (a, t) in enumerate(hitos):
            t0 = marcas[i] if i < len(marcas) else .3 + i * .5
            k = _eo((dt - t0) / .4)
            if k <= 0:
                continue
            cx = M + 80 + paso * (i + .5)
            ycaja = yb - 10 - 80 * k
            col = NARANJA if i == n - 1 else AMARILLO
            d.rectangle((cx - paso / 2 + 12, ycaja - 150, cx + paso / 2 - 12, ycaja), fill=(28, 32, 36, 235), outline=col + (255,), width=3)
            _txt(d, (cx, ycaja - 105), str(a), fa, col, "mm", 255 * k)
            _txt(d, (cx, ycaja - 40), t, ft[i], BLANCO, "mm", 255 * k)
        return _entrada(im, dt, dur)
    return fn


# ------------------------------------------------------------------ hoja de prueba
def hoja(fn, dur, marcas, salida, tiempos=None, ancho=640, fondo=(60, 70, 60)):
    tiempos = tiempos or [dur * k for k in (.1, .3, .5, .7, .9, .99)]
    cuadros = []
    for t in tiempos:
        a = fn(t, dur, marcas)
        im = Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")
        base = Image.new("RGBA", im.size, fondo + (255,))
        base.alpha_composite(im)
        r = ancho / im.width
        cuadros.append(base.convert("RGB").resize((ancho, max(1, int(im.height * r)))))
    H = sum(c.height for c in cuadros) + 6 * len(cuadros)
    out = Image.new("RGB", (ancho, H), (0, 0, 0))
    y = 0
    for c in cuadros:
        out.paste(c, (0, y))
        y += c.height + 6
    out.save(salida, quality=85)
    return salida
