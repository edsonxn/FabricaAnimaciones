# -*- coding: utf-8 -*-
"""MOTION GRAPHICS «interfaz de Skyrim» por código (Crónicas de Tamriel; primer uso `tes_misiones_daedricas`, 13-oct-2026).
Hermano de nucleo/mg_wow.py con la estética de los menús de The Elder Scrolls V: humo negro de bordes difuminados (no caja
con marco), separadores color hueso que se desvanecen en los extremos con un rombo al centro, letra condensada en
MAYÚSCULAS espaciadas (Bahnschrift Condensed, lo más parecido a la Futura Condensed del juego en Windows) y el rojo sangre
para lo daédrico. CERO cifras inventadas: solo números que el guion ya dice.

Uso desde videos/<v>/efectos.py (FX `mg` de nucleo/secuencia_fx.py; acepta de/a o en/dur):
    import mg_tes as T
    FX = [dict(tipo="mg", fn=T.mision("Misión iniciada", "La llamada de Boethiah"), en="Y llegamos al número uno", dur=4.0,
               y=.16, sale=.4)]
  mision(arriba, titulo)                       aviso de misión del juego (arriba al centro, sin panel)
  objeto(nombre, efecto, origen=None)          ficha de objeto del inventario: nombre, separador, efecto con las cifras del guion
  rejilla(titulo, n, encendidas, remate)       n casillas que se llenan en la marca 0; `encendidas` se vuelven rojas en la marca 1
  traiciones(titulo, n, ini, paso, cada, etiqueta)   n siluetas; desde la marca 1 caen una a una (hasta la marca 2) y el
                                               número sube `paso` cada `cada` caídas (Hoja de Ébano: 10 -> 30)
  reloj(titulo, minutos, remate)               anillo que se vacía de mm:00 a 0:00 entre las marcas 0 y 1; remate en la 2
  contadores(titulo, [(etiqueta, valor, i_ini, i_fin), ...], remate=(texto, i))   como mg_wow.contadores, sin íconos
  pegatina(ruta, titulo=None, tam=360)         imagen REAL (wiki) de lo que se nombra como pegatina con borde blanco que rebota y flota
  Con retratos REALES de la wiki (tes_misiones_nunca, 20-oct-2026):
  rehenes(titulo, [(ruta, etiqueta)], arriba, dudas, tachar)   la cabaña: quien está sobre el armario arriba, «?» rojos, aspa
  sospechosos(titulo, pista, falso, culpable)  tablero con hilo rojo: ARRESTADO → el hilo se corta, INOCENTE → EL CARNICERO
  cadena(titulo, [(texto, ruta)])              pasos unidos por eslabones en serpiente; el último eslabón se rompe y arde
  balanza(titulo, izq, [der], remate)          lo que te pagan contra lo que pierdes: cada cosa cae al plato y lo inclina
  tes_cosas_inutiles (23-oct-2026):
  agenda(titulo, [(h0, h1, etiqueta, color)], retrato, remate)   reloj de 24 h con los tramos del día de un PNJ
  lena(titulo, tronco, casa, precio, meta, nombre_casa, remate)  troncos apilados y contador hasta el precio de la casa
  salud(titulo, chico, grande, n_chicos)       barras de salud: lo poco que cura uno contra otro, y cuántos hacen falta
  receta(titulo, [(ruta, nombre)], resultado, efecto, remate)    ingredientes que se funden en el resultado
  trato(titulo, perro, premio_a, premio_b, condiciones, datos, sello)   bifurcación de un trato daédrico
  compraventa(titulo, objeto, [(texto, delta)], remate)          línea de tiempo de compras/ventas con el balance
  tes_armas_poderosas (23-oct-2026):
  ruleta(titulo, [(etiqueta, color)], paradas)   rueda del Wabbajack: en cada marca gira y frena en paradas[k]; lista de resultados
  barras(titulo, [(ruta, etiqueta, valor, i, color)], refs, unidad, remate)   barras comparadas + líneas de referencia punteadas
  niveles(titulo, [(rango, valor)], notas)     escalera del arma nivelada; notas enmarcan la trampa de un nivel
  golpes(titulo, objetivo, salud, [(ruta, arma, a, b)], fases, remate)   golpes para tumbar a X en dos fases (fuego / escarcha)
  tes_cosas_nunca (27-oct-2026):
  plazo(titulo, horas, retrato, avisos, curas, final, remate)   cuenta atrás en una línea de días (sol/luna), avisos del juego
                                               en su hora, remedios que se tachan al acabar (Sanguinare Vampiris, Lydia 72 h)
  paciencia(titulo, retrato, golpes, aviso, estallido, remate)  casillas de aviso que se llenan golpe a golpe y el PNJ se
                                               pone rojo: HOSTIL (fuego amigo)
  escalado(titulo, objeto, contador, niveles_, tu, hitos, remate)   contador que sube tu nivel mientras tu arma se queda; lo
                                               que el mundo trae a cada nivel aparece en la regla (dagas de hierro / dragones)
  reinicio(titulo, objetos, dias, seguro, remate)   cofre con tu botín, calendario que se tacha y todo desaparece; tu casa SEGURO
  tes_misiones_imperdibles (28-oct-2026):
  inversion(titulo, socio, [(monto, motivo)], nota, despierta, remate)   pilas de monedas que crecen pago a pago, «INVERTIDO»
                                               suma, la carta final cae como sello y el que despierta pasa de gris a rojo (Ralis/Ahzidal)
  versiones(titulo, izq, der, veredicto, remate)   dos testimonios enfrentados con retrato, «PRUEBAS: 0» y sello «SIN PRUEBAS»
  fragmentos(titulo, padre, objeto, [(ruta, nombre, lugar)], bono, remate)   un objeto que se parte entre varios: los trozos
                                               vuelan a cada uno, vuelven, se recompone y los portadores se tachan (Gauldur)
  tes_sentinel_teaser (3-nov-2026):
  cifrado(titulo, pares, palabra, remate)      números que giran y dejan su letra (Starfield 19 05 14… = SENTINEL)
  ceguera(titulo, retrato, [(texto, i)], remate)   la barra VISTA de un Sacerdote de la Polilla baja lectura a lectura
  lecturas(titulo, cita, [(nombre, texto, i)]) una cita y sus interpretaciones, la activa encendida y las demás en gris
  narrador(nombre, lema, n=None, de=None)      placa pequeña «NARRA» + nombre de la voz (videos a varias voces; n/de = turno)
  votacion(titulo, nombres, remate)            papeleta: cada marca i enciende el nombre i (quien pide el voto); el remate al final
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HUESO, BLANCO, GRIS, SANGRE, ORO = (236, 230, 214), (255, 255, 255), (150, 146, 138), (196, 38, 30), (214, 186, 120)
_fc, _bc = {}, {}


def fuente(estilo, tam):
    """estilo = variación de Bahnschrift («Condensed», «SemiBold Condensed», «Bold Condensed», «Light Condensed»)."""
    k = (estilo, tam)
    if k not in _fc:
        f = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", tam)
        try:
            f.set_variation_by_name(estilo)
        except Exception:
            pass
        _fc[k] = f
    return _fc[k]


def _pop(dt, dur=0.35):
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1.6 else 1 - math.exp(-6 * u) * math.cos(9 * u)


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _texto(d, xy, s, f, color, ancla="la", alfa=255, track=0):
    """Texto con sombra suave; track = espacio extra entre letras (px)."""
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if not track:
        d.text((xy[0] + 2, xy[1] + 2), s, font=f, fill=(0, 0, 0, int(a * .85)), anchor=ancla)
        d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla)
        return
    ancho = sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)
    x = xy[0] - (ancho / 2 if ancla[0] == "m" else ancho if ancla[0] == "r" else 0)
    for c in s:
        d.text((x + 2, xy[1] + 2), c, font=f, fill=(0, 0, 0, int(a * .85)), anchor="l" + ancla[1])
        d.text((x, xy[1]), c, font=f, fill=tuple(color) + (a,), anchor="l" + ancla[1])
        x += d.textlength(c, font=f) + track


def _ancho_track(d, s, f, track):
    return sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)


def separador(d, cx, y, medio, alfa=255, color=HUESO, rombo=True):
    """Línea fina que se desvanece hacia los extremos, con rombo al centro (separador de los menús)."""
    a = alfa / 255
    pasos = 60
    for i in range(pasos):
        u0, u1 = i / pasos, (i + 1) / pasos
        k = (1 - u0) ** 1.4
        for s in (-1, 1):
            d.line([(cx + s * (8 + u0 * medio), y), (cx + s * (8 + u1 * medio), y)], fill=color + (int(230 * k * a),), width=2)
    if rombo:
        d.polygon([(cx - 7, y), (cx, y - 7), (cx + 7, y), (cx, y + 7)], outline=color + (int(255 * a),), fill=(0, 0, 0, int(160 * a)))
        d.polygon([(cx - 3, y), (cx, y - 3), (cx + 3, y), (cx, y + 3)], fill=color + (int(255 * a),))


def _humo(w, h, titulo=None):
    """Panel de humo negro con bordes difuminados + título espaciado con separador debajo (se calcula una vez)."""
    k = (w, h, titulo)
    if k not in _bc:
        M = 60
        im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((M + 10, M + 10, M + w - 10, M + h - 10), 40, fill=205)
        m = m.filter(ImageFilter.GaussianBlur(26))
        negro = Image.new("RGBA", im.size, (6, 6, 8, 255))
        negro.putalpha(m)
        im.alpha_composite(negro)
        d = ImageDraw.Draw(im)
        if titulo:
            f = fuente("SemiBold Condensed", 40)
            _texto(d, (M + w / 2, M + 48), titulo.upper(), f, HUESO, "mm", track=5)
            separador(d, M + w / 2, M + 84, min(w * .42, _ancho_track(d, titulo.upper(), f, 5) / 2 + 120))
        _bc[k] = (im, M)
    im, M = _bc[k]
    return im.copy(), M


def _salida(im, dt, pop=True):
    s = _pop(dt, .45) if pop else _eo(dt / .35)
    if s <= 0.02:
        return np.zeros((2, 2, 4), np.uint8)
    if pop and abs(s - 1) > .004:
        im = im.resize((max(2, int(im.width * s)), max(2, int(im.height * s))), Image.BILINEAR)
    elif not pop and s < 1:
        a = np.array(im)
        a[..., 3] = (a[..., 3] * s).astype(np.uint8)
        return a[..., [2, 1, 0, 3]].copy()
    return np.array(im)[..., [2, 1, 0, 3]].copy()


# ------------------------------------------------------------------ aviso de misión
def mision(arriba, titulo, ancho=1500, color_titulo=HUESO):
    """«MISIÓN INICIADA» chico y espaciado entre dos separadores; debajo el nombre de la misión, que entra cerrando el
    espaciado (como el aviso del juego). Sin panel: solo una sombra difusa detrás para que se lea sobre cualquier clip."""
    h = 190
    f1, f2 = fuente("Condensed", 34), fuente("SemiBold Condensed", 70)

    def fn(dt, dur, marcas):
        M = 40
        im = Image.new("RGBA", (ancho + 2 * M, h + 2 * M), (0, 0, 0, 0))
        sh = Image.new("L", im.size, 0)
        ImageDraw.Draw(sh).rounded_rectangle((M + ancho * .18, M + 20, M + ancho * .82, M + h - 10), 60, fill=150)
        sombra = Image.new("RGBA", im.size, (0, 0, 0, 255))
        sombra.putalpha(sh.filter(ImageFilter.GaussianBlur(30)))
        im.alpha_composite(sombra)
        d = ImageDraw.Draw(im)
        a = 255 * _eo(dt / .5)
        cx = M + ancho / 2
        s1 = arriba.upper()
        _texto(d, (cx, M + 50), s1, f1, GRIS, "mm", a, track=6)
        mitad = _ancho_track(d, s1, f1, 6) / 2
        for s in (-1, 1):                               # separadores a los lados del rótulo chico
            x0 = cx + s * (mitad + 24)
            for i in range(40):
                u0, u1 = i / 40, (i + 1) / 40
                d.line([(x0 + s * u0 * 240, M + 50), (x0 + s * u1 * 240, M + 50)], fill=HUESO + (int(a * .9 * (1 - u0)),), width=2)
        tr = 4 + 26 * (1 - _eo(dt / .9))                # el título entra cerrando el espaciado
        _texto(d, (cx, M + 128), titulo.upper(), f2, color_titulo, "mm", a, track=tr)
        sale = max(0.0, min(1.0, (dur - dt) / .45))
        arr = np.array(im)
        arr[..., 3] = (arr[..., 3] * sale).astype(np.uint8)
        return arr[..., [2, 1, 0, 3]].copy()
    return fn


# ------------------------------------------------------------------ ficha de objeto
def _partir(d, s, f, ancho):
    lineas, cur = [], ""
    for w in s.split():
        prueba = (cur + " " + w).strip()
        if d.textlength(prueba, font=f) <= ancho or not cur:
            cur = prueba
        else:
            lineas.append(cur)
            cur = w
    return lineas + [cur] if cur else lineas


def objeto(nombre, efecto, origen=None, ancho=780, rojo=False):
    """Ficha del inventario: `origen` gris arriba (p. ej. «Artefacto de Mephala»), nombre en mayúsculas, separador y el
    efecto centrado. En `efecto`, lo que va entre *asteriscos* sale en blanco y negrita (las cifras, como en el juego)."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fe, fb = fuente("Condensed", 36), fuente("Bold Condensed", 36)
    lineas = _partir(tmp, efecto.replace("*", ""), fe, ancho - 110)
    fn_ = fuente("SemiBold Condensed", 56)
    nombres = _partir(tmp, nombre.upper(), fn_, ancho - 160)      # nombre largo (un título de video) en dos líneas
    h = (60 if origen else 20) + 96 + 66 * (len(nombres) - 1) + 40 + len(lineas) * 50 + 40

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h)
        d = ImageDraw.Draw(im)
        y = M + 30
        if origen:
            _texto(d, (M + ancho / 2, y + 16), origen.upper(), fuente("Condensed", 30), GRIS, "mm", track=4)
            y += 48
        for k, ln in enumerate(nombres):
            _texto(d, (M + ancho / 2, y + 40 + 66 * k), ln, fn_, SANGRE if rojo else HUESO, "mm", track=3)
        y += 92 + 66 * (len(nombres) - 1)
        separador(d, M + ancho / 2, y, ancho * .40)
        y += 34
        # efecto: reparte las palabras con su estilo (normal gris claro / *negrita blanca*)
        palabras, neg, pegado = [], False, False
        for trozo in efecto.split("*"):
            ws = trozo.split()
            if ws and pegado and not trozo[0].isspace():     # «*10*.»: el punto va con la palabra en negrita
                palabras[-1] = (palabras[-1][0] + ws[0], palabras[-1][1])
                ws = ws[1:]
            for w in ws:
                palabras.append((w, neg))
            pegado = bool(trozo) and not trozo[-1].isspace() and bool(palabras)
            neg = not neg
        i = 0
        for ln in lineas:
            n = len(ln.split())
            tramo = palabras[i:i + n]
            i += n
            anchos = [d.textlength(w, font=fb if b else fe) for w, b in tramo]
            esp = d.textlength(" ", font=fe)
            x = M + ancho / 2 - (sum(anchos) + esp * (len(tramo) - 1)) / 2
            for (w, b), aw in zip(tramo, anchos):
                _texto(d, (x, y + 25), w, fb if b else fe, BLANCO if b else (205, 200, 190), "lm")
                x += aw + esp
            y += 50
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ rejilla de probabilidad
def rejilla(titulo, n=100, encendidas=2, remate=None, cols=20, ancho=1180):
    """n casillas (cols por fila) que aparecen en barrido desde la marca 0; en la marca 1 `encendidas` casillas (repartidas)
    se vuelven rojo sangre con destello; remate = (texto, i_marca) en grande abajo."""
    T, G = 40, 9
    filas_ = math.ceil(n / cols)
    w_rej = cols * T + (cols - 1) * G
    h = 110 + filas_ * (T + G) + (96 if remate else 30)
    rojas = set(range(n)) if encendidas >= n else {int(round((k + .5) * n / encendidas + 7)) % n for k in range(encendidas)}

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t0 = marcas[0] if marcas else .3
        t1 = marcas[1] if len(marcas) > 1 else t0 + 2
        x0, y0 = M + (ancho - w_rej) / 2, M + 112
        for i in range(n):
            r, c = divmod(i, cols)
            u = dt - t0 - (r + c) * .025
            if u <= 0:
                continue
            a = 255 * _eo(u / .25)
            x, y = x0 + c * (T + G), y0 + r * (T + G)
            roja = i in rojas and dt >= t1
            if roja:
                v = dt - t1
                s = _pop(v, .3)
                e = int((T / 2) * (1 - s))
                d.rectangle((x - 3, y - 3, x + T + 3, y + T + 3), outline=SANGRE + (int(255 * max(0, 1 - v)),), width=3)
                d.rectangle((x + e, y + e, x + T - e, y + T - e), fill=SANGRE + (255,))
            else:
                d.rectangle((x, y, x + T, y + T), fill=(30, 29, 27, int(a * .9)), outline=HUESO + (int(a * .45),), width=1)
        if remate and len(marcas) > remate[1] and dt >= marcas[remate[1]]:
            s = _pop(dt - marcas[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 52), remate[0].upper(), fuente("Bold Condensed", max(8, int(56 * s))), SANGRE, "mm", track=3)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ siluetas que caen (Hoja de Ébano)
def _silueta(d, x, y, t, color, a):
    """Busto simple: cabeza y hombros."""
    r = t * .17
    d.ellipse((x + t / 2 - r, y + t * .04, x + t / 2 + r, y + t * .04 + 2 * r), fill=color + (int(a),))
    d.pieslice((x + t * .12, y + t * .46, x + t * .88, y + t * 1.3), 180, 360, fill=color + (int(a),))


def traiciones(titulo, n=10, ini=10, paso=4, cada=2, etiqueta="Absorber salud", ancho=1360):
    """n siluetas hueso aparecen en la marca 0; entre las marcas 1 y 2 caen una a una (se vuelven rojo sangre con una
    tachadura) y el número de la derecha sube `paso` cada `cada` caídas, de `ini` a ini + paso * n / cada."""
    T, G = 74, 18
    w_s = n * T + (n - 1) * G
    h = 110 + T + 30 + 70

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t0 = marcas[0] if marcas else .3
        t1 = marcas[1] if len(marcas) > 1 else t0 + 1.5
        t2 = marcas[2] if len(marcas) > 2 else t1 + 3
        x0, y0 = M + 60, M + 116
        caidas = 0
        for i in range(n):
            u = dt - t0 - i * .06
            if u <= 0:
                continue
            x = x0 + i * (T + G)
            tc = t1 + (t2 - t1) * i / max(1, n - 1) if n > 1 else t1
            if dt >= tc:
                caidas += 1
                v = dt - tc
                _silueta(d, x, y0 + 6 * _eo(v / .3), T, SANGRE, 255)
                k = _eo(v / .2)
                d.line([(x + 6, y0 + 8), (x + 6 + (T - 12) * k, y0 + 8 + (T - 4) * k)], fill=(10, 8, 8, 255), width=6)
            else:
                _silueta(d, x, y0, T, HUESO, 255 * _eo(u / .25))
        valor = ini + paso * (caidas // cada)
        xr = M + 60 + w_s + 40
        _texto(d, (xr + (ancho - 60 - w_s - 100) / 2 + 20, y0 + 18), etiqueta.upper(), fuente("Condensed", 26), GRIS, "mm", track=3)
        _texto(d, (xr + (ancho - 60 - w_s - 100) / 2 + 20, y0 + 68), str(valor), fuente("Bold Condensed", 78),
               SANGRE if caidas >= n else BLANCO, "mm")
        _texto(d, (M + ancho / 2, M + h - 40), f"{caidas} DE {n}", fuente("SemiBold Condensed", 34),
               SANGRE if caidas else GRIS, "mm", track=4)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ reloj que se vacía (Anillo de Namira)
def reloj(titulo, minutos=5, remate=None, ancho=760):
    """Anillo hueso lleno con «m:00» en la marca 0; entre las marcas 0 y 1 se vacía a 0:00 (el último tramo en rojo);
    remate = (texto, i_marca)."""
    R = 128
    h = 110 + 2 * R + 40 + (80 if remate else 10)

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t0 = marcas[0] if marcas else .3
        t1 = marcas[1] if len(marcas) > 1 else t0 + 3
        u = 0.0 if dt < t0 else min(1.0, (dt - t0) / max(.3, t1 - t0))
        resto = minutos * 60 * (1 - u)
        cx, cy = M + ancho / 2, M + 110 + R + 10
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(60, 58, 54, 255), width=16)
        col = SANGRE if u > .8 else HUESO
        if u < 1:
            d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * (1 - u), fill=col + (255,), width=16)
        _texto(d, (cx, cy), f"{int(resto // 60)}:{int(resto % 60):02d}", fuente("Bold Condensed", 96), SANGRE if u >= 1 else BLANCO, "mm")
        if remate and len(marcas) > remate[1] and dt >= marcas[remate[1]]:
            s = _pop(dt - marcas[remate[1]], .35)
            _texto(d, (cx, M + h - 46), remate[0].upper(), fuente("Bold Condensed", max(8, int(46 * s))), SANGRE, "mm", track=3)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ contadores
def contadores(titulo, filas_, remate=None, ancho=1100):
    """filas_ = [(etiqueta, valor, i_ini, i_fin), ...]: la fila aparece en la marca i_ini (None = desde el inicio) y su número
    corre de 0 a `valor` hasta la marca i_fin. remate = (texto, i_marca) en rojo sangre."""
    AF = 84
    h = 110 + len(filas_) * AF + (80 if remate else 20)

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        for k, (et, valor, i0, i1) in enumerate(filas_):
            t0 = marcas[i0] if i0 is not None and i0 < len(marcas) else 0.0
            t1 = marcas[i1] if i1 is not None and i1 < len(marcas) else t0 + 2.0
            if dt < t0:
                continue
            y = M + 120 + k * AF
            a = 255 * _eo((dt - t0) / .3)
            _texto(d, (M + 70, y + 30), et.upper(), fuente("Condensed", 40), HUESO, "lm", a, track=3)
            u = (dt - t0) / max(.3, t1 - t0)
            v = valor if u >= 1 else int(round(valor * (1 - (1 - max(0.0, u)) ** 2.2)))
            _texto(d, (M + ancho - 70, y + 30), str(max(v, 0)), fuente("Bold Condensed", 66), BLANCO, "rm", a)
            if k < len(filas_) - 1:
                separador(d, M + ancho / 2, y + 74, ancho * .38, a * .5, rombo=False)
        if remate and len(marcas) > remate[1] and dt >= marcas[remate[1]]:
            s = _pop(dt - marcas[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 50), remate[0].upper(), fuente("Bold Condensed", max(8, int(48 * s))), SANGRE, "mm", track=3)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ pegatina (17-oct-2026, petición del usuario)
def _base_pegatina(ruta, tam, borde=12):
    """Recorte con borde blanco y sombra. Render con fondo transparente (íconos de la wiki) -> contorno blanco que sigue la
    silueta; foto opaca (retratos de PNJ) -> rectángulo de esquinas redondeadas con marco blanco."""
    im = Image.open(ruta).convert("RGBA")
    a = np.array(im)[..., 3]
    recorte = (a < 10).mean() > .12
    if recorte:
        im = im.crop(im.getbbox())
    esc = tam / max(im.size)
    im = im.resize((max(2, int(im.width * esc)), max(2, int(im.height * esc))), Image.LANCZOS)
    P = borde * 3
    lienzo = Image.new("RGBA", (im.width + 2 * P, im.height + 2 * P), (0, 0, 0, 0))
    if recorte:
        al = Image.new("L", lienzo.size, 0)
        al.paste(im.getchannel("A"), (P, P))
        al = al.point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(2 * borde + 1)).filter(ImageFilter.GaussianBlur(1.2))
    else:
        al = Image.new("L", lienzo.size, 0)
        ImageDraw.Draw(al).rounded_rectangle((P - borde, P - borde, P + im.width + borde, P + im.height + borde), radius=borde * 2, fill=255)
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=borde, fill=255)
        im.putalpha(m)
    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    sombra.putalpha(al.point(lambda v: int(v * .55)).filter(ImageFilter.GaussianBlur(9)))
    lienzo.alpha_composite(sombra, (6, 10))
    blanco = Image.new("RGBA", lienzo.size, (250, 247, 238, 0))
    blanco.putalpha(al)
    lienzo.alpha_composite(blanco)
    lienzo.alpha_composite(im, (P, P))
    return lienzo


def pegatina(ruta, titulo=None, tam=360, giro=-6.0):
    """Imagen REAL de lo que nombra la voz (objeto, ropa, personaje) como pegatina: entra con rebote girando hasta quedar
    inclinada `giro` grados, se balancea y flota suave mientras está en pantalla; `titulo` en una píldora hueso debajo.
    La salida la hace el FX (`sale=`). Imágenes: la wiki de Fandom (elderscrolls.fandom.com, prop=pageimages)."""
    base = _base_pegatina(ruta, tam)
    if titulo:
        f = fuente("Bold Condensed", 34)
        tw = int(_ancho_track(ImageDraw.Draw(base), titulo.upper(), f, 2)) + 44
        alto = base.height + 40
        lien = Image.new("RGBA", (max(base.width, tw + 20), alto), (0, 0, 0, 0))
        lien.alpha_composite(base, ((lien.width - base.width) // 2, 0))
        d = ImageDraw.Draw(lien)
        cx, y0 = lien.width / 2, base.height - 46
        d.rounded_rectangle((cx - tw / 2, y0, cx + tw / 2, y0 + 52), radius=26, fill=(18, 16, 14, 235), outline=HUESO + (255,), width=2)
        _texto(d, (cx, y0 + 26), titulo.upper(), f, HUESO, "mm", track=2)
        base = lien

    def fn(dt, dur, marcas):
        s = _pop(dt, .42)
        if s <= 0.02:
            return np.zeros((2, 2, 4), np.uint8)
        ang = giro * min(1.0, dt / .5) + (1 - min(1.0, dt / .5)) * -22 + 2.2 * math.sin(dt * 2.1)
        im = base.rotate(ang, resample=Image.BICUBIC, expand=True)
        k = s * (1 + .025 * math.sin(dt * 3.0))
        im = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.BILINEAR)
        a = np.array(im)[..., [2, 1, 0, 3]]
        fl = int(round(7 * math.sin(dt * 1.7)))           # flota: margen arriba/abajo que se desplaza
        out = np.zeros((a.shape[0] + 16, a.shape[1], 4), np.uint8)
        out[8 + fl:8 + fl + a.shape[0]] = a
        return out
    return fn


# ======================================================================= MG nuevos de `tes_misiones_nunca` (19/20-oct-2026)
# Retratos REALES (pegatinas/<slug>.png de la wiki) dentro del humo de la interfaz, animados por las marcas de la voz.
_rc = {}


def _retrato(ruta, w, h, gris=0.0):
    """Recorte w×h de la parte alta de la imagen (las caras de los PNJ están arriba) con esquinas redondeadas y filete hueso.
    gris 0..1 = desaturado y oscurecido (el que sale de la historia)."""
    k = (ruta, w, h)
    if k not in _rc:
        im = Image.open(ruta).convert("RGBA")
        if (np.array(im)[..., 3] < 10).mean() > .12:            # objeto con fondo transparente: entero, centrado sobre oscuro
            im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
            esc = min((w - 24) / im.width, (h - 24) / im.height)
            im = im.resize((max(2, int(im.width * esc)), max(2, int(im.height * esc))), Image.LANCZOS)
            fondo = Image.new("RGBA", (w, h), (30, 28, 26, 255))
            fondo.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
            im = fondo
        else:
            if im.height > im.width * 1.2:                      # retrato de cuerpo entero: cabeza y torso
                im = im.crop((int(im.width * .14), 0, int(im.width * .86), int(im.height * .58)))
            esc = max(w / im.width, h / im.height)
            im = im.resize((max(w, int(im.width * esc)), max(h, int(im.height * esc))), Image.LANCZOS)
            x0 = (im.width - w) // 2
            y0 = int(min(im.height - h, im.height * .03)) if im.height > im.width else (im.height - h) // 2
            im = im.crop((x0, y0, x0 + w, y0 + h))
            a = np.array(im).astype(np.float32)               # fotos oscuras del juego (Astrid): subir la luz
            lum = a[..., :3].mean()
            if lum < 80:
                a[..., :3] = 255 * (a[..., :3] / 255) ** (math.log(80 / 255) / math.log(max(lum, 8) / 255))
                im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=255)
        im.putalpha(m)
        _rc[k] = im
    im = _rc[k].copy()
    if gris > 0:
        a = np.array(im).astype(np.float32)
        l = a[..., :3].mean(axis=2, keepdims=True)
        a[..., :3] = (a[..., :3] * (1 - gris) + l * gris) * (1 - .45 * gris)
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    return im


def _marco(d, x, y, w, h, color, a, ancho=3):
    d.rounded_rectangle((x - 4, y - 4, x + w + 4, y + h + 4), radius=17, outline=tuple(color) + (int(a),), width=ancho)


def _tacha(d, x, y, w, h, u, color=SANGRE, ancho=12):
    """Aspa roja que se dibuja en dos trazos (u 0..1)."""
    u1, u2 = min(1.0, u * 2), max(0.0, u * 2 - 1)
    if u1 > 0:
        d.line([(x + 10, y + 10), (x + 10 + (w - 20) * u1, y + 10 + (h - 20) * u1)], fill=color + (255,), width=ancho)
    if u2 > 0:
        d.line([(x + w - 10, y + 10), (x + w - 10 - (w - 20) * u2, y + 10 + (h - 20) * u2)], fill=color + (255,), width=ancho)


def _sello(im, cx, cy, texto, u, color=SANGRE, giro=-12, tam=58):
    """Sello de tinta que cae desde grande (u 0..1) y se queda torcido."""
    if u <= 0:
        return
    f = fuente("Bold Condensed", tam)
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    tw = int(_ancho_track(tmp, texto, f, 4)) + 50
    th = tam + 34
    s = Image.new("RGBA", (tw + 20, th + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.rounded_rectangle((10, 10, tw + 10, th + 10), radius=8, outline=color + (255,), width=6)
    d.rounded_rectangle((18, 18, tw + 2, th + 2), radius=5, outline=color + (170,), width=2)
    _texto(d, (10 + tw / 2, 10 + th / 2 + 2), texto, f, color, "mm", track=4)
    k = 1 + 1.4 * (1 - _eo(u / .6))
    s = s.rotate(giro, resample=Image.BICUBIC, expand=True)
    s = s.resize((max(2, int(s.width * k)), max(2, int(s.height * k))), Image.BILINEAR)
    a = np.array(s)
    a[..., 3] = (a[..., 3] * min(1.0, u / .25)).astype(np.uint8)
    im.alpha_composite(Image.fromarray(a), (int(cx - s.width / 2), int(cy - s.height / 2)))


# ------------------------------------------------------------------ la cabaña (rehenes)
def rehenes(titulo, personas, arriba=None, dudas=None, tachar=(), ancho=1500):
    """La cabaña abandonada. personas = [(ruta, etiqueta), ...]; `arriba` = índice de quien está sentado encima del armario
    (más grande, arriba al centro, con filete rojo). Cada persona entra con su marca (marca i = persona i). `dudas` = marca en la
    que aparece un «?» rojo sobre cada uno de los demás (cuál tiene el contrato). tachar = [(índice, marca), ...]: aspa roja y
    el retrato se apaga; si es el de `arriba`, el título se vuelve rojo. Puerta cerrada dibujada a la derecha."""
    RW, RH = 230, 300
    otros = [i for i in range(len(personas)) if i != arriba]
    h = 110 + (RH + 90 if arriba is not None else 0) + RH + 110

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(personas) + 4)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        tach = {i: mk[m] if m < len(mk) else 99 for i, m in tachar}
        y_fila = M + 120 + (RH + 90 if arriba is not None else 0)
        xs = {}
        sep = 70
        w_f = len(otros) * RW + (len(otros) - 1) * sep
        for k, i in enumerate(otros):
            xs[i] = (M + (ancho - w_f) / 2 - 90 + k * (RW + sep), y_fila)
        if arriba is not None:
            xs[arriba] = (M + ancho / 2 - 90 - RW / 2, M + 116)
        # puerta cerrada a la derecha (tablones + barra)
        px, py = M + ancho - 250, y_fila - 40
        a_p = 255 * _eo((dt - mk[0]) / .5)
        for t in range(4):
            d.rectangle((px + t * 42, py, px + t * 42 + 38, py + RH + 40), fill=(52, 40, 30, int(a_p)), outline=(20, 15, 10, int(a_p)))
        d.rectangle((px - 8, py + RH * .45, px + 176, py + RH * .45 + 26), fill=(90, 70, 50, int(a_p)))
        _texto(d, (px + 84, py + RH + 74), "CERRADA", fuente("SemiBold Condensed", 32), GRIS, "mm", a_p, track=4)
        for i, (ruta, et) in enumerate(personas):
            t0 = mk[i]
            if dt < t0:
                continue
            u = _eo((dt - t0) / .45)
            x, y = xs[i]
            y += 30 * (1 - u)
            ut = _eo((dt - tach.get(i, 99)) / .5)
            r = _retrato(ruta, RW, RH, gris=.85 * ut)
            if u < 1:
                a = np.array(r)
                a[..., 3] = (a[..., 3] * u).astype(np.uint8)
                r = Image.fromarray(a)
            im.alpha_composite(r, (int(x), int(y)))
            col = SANGRE if i == arriba else HUESO
            _marco(d, x, y, RW, RH, col, 255 * u, 4 if i == arriba else 2)
            _texto(d, (x + RW / 2, y + RH + 34), et.upper(), fuente("SemiBold Condensed", 34),
                   SANGRE if (i == arriba or ut > .5) else HUESO, "mm", 255 * u, track=3)
            if ut > 0:
                _tacha(d, x, y, RW, RH, ut)
            if dudas is not None and i != arriba and ut <= 0 and dt >= mk[dudas]:
                s = _pop(dt - mk[dudas] - .12 * otros.index(i), .35)
                if s > .02:
                    cx, cy = x + RW - 16, y + 14
                    rr = 34 * s
                    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=SANGRE + (255,), outline=BLANCO + (255,), width=3)
                    _texto(d, (cx, cy + 2), "?", fuente("Bold Condensed", max(8, int(52 * s))), BLANCO, "mm")
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ el tablero del Carnicero
def sospechosos(titulo, pista, falso, culpable, ancho=1500):
    """Tablero de corcho en humo. pista/falso/culpable = (ruta, etiqueta). marca 0: la pista (amuleto) al centro · marca 1:
    el sospechoso falso a la izquierda, unido por hilo rojo · marca 2: sello ARRESTADO sobre él · marca 3: el hilo se corta y
    el sello cambia a INOCENTE · marca 4: el culpable a la derecha, hilo nuevo y sello EL CARNICERO."""
    RW, RH = 300, 380
    h = 110 + RH + 120

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        y = M + 118
        cx = M + ancho / 2
        xs = {"pista": cx - 140, "falso": M + 90, "culpable": M + ancho - 90 - RW}
        pw = 280
        u_p = _eo((dt - mk[0]) / .45)
        u_f = _eo((dt - mk[1]) / .45)
        u_c = _eo((dt - mk[4]) / .45)
        corte = _eo((dt - mk[3]) / .35)
        # hilos rojos (se dibujan antes de los retratos)
        pc = (cx, y + 120)
        if u_f > 0:
            pf = (xs["falso"] + RW / 2, y + 40)
            k = u_f
            if corte <= 0:
                d.line([pc, (pc[0] + (pf[0] - pc[0]) * k, pc[1] + (pf[1] - pc[1]) * k)], fill=SANGRE + (230,), width=4)
            else:                                           # se corta: dos trozos que caen
                mx, my = (pc[0] + pf[0]) / 2, (pc[1] + pf[1]) / 2
                caida = 60 * corte
                d.line([pc, (mx + 20, my + caida)], fill=SANGRE + (int(230 * (1 - corte * .7)),), width=4)
                d.line([pf, (mx - 20, my + caida)], fill=SANGRE + (int(230 * (1 - corte * .7)),), width=4)
        if u_c > 0:
            pq = (xs["culpable"] + RW / 2, y + 40)
            d.line([pc, (pc[0] + (pq[0] - pc[0]) * u_c, pc[1] + (pq[1] - pc[1]) * u_c)], fill=SANGRE + (255,), width=5)
        for clave, (ruta, et), u, w_, h_ in (("pista", pista, u_p, pw, pw), ("falso", falso, u_f, RW, RH),
                                              ("culpable", culpable, u_c, RW, RH)):
            if u <= 0:
                continue
            x = xs[clave]
            yy = y + (40 if clave == "pista" else 0) + 26 * (1 - u)
            r = _retrato(ruta, w_, h_, gris=.6 * corte if clave == "falso" else 0)
            if u < 1:
                a = np.array(r)
                a[..., 3] = (a[..., 3] * u).astype(np.uint8)
                r = Image.fromarray(a)
            im.alpha_composite(r, (int(x), int(yy)))
            _marco(d, x, yy, w_, h_, SANGRE if clave == "culpable" else HUESO, 255 * u, 4 if clave == "culpable" else 2)
            d.ellipse((x + w_ / 2 - 11, yy - 15, x + w_ / 2 + 11, yy + 7), fill=SANGRE + (int(255 * u),),
                      outline=(40, 0, 0, int(255 * u)), width=2)       # chincheta
            _texto(d, (x + w_ / 2, yy + h_ + 36), et.upper(), fuente("SemiBold Condensed", 34),
                   SANGRE if clave == "culpable" else HUESO, "mm", 255 * u, track=3)
        if dt >= mk[2] and u_f > 0:
            u_s = (dt - mk[2]) if dt < mk[3] else 1.0
            _sello(im, xs["falso"] + RW / 2, y + RH * .55, "INOCENTE" if corte > .5 else "ARRESTADO", min(1.0, u_s),
                   color=GRIS if corte > .5 else SANGRE, giro=-12)
        if u_c > 0 and dt >= mk[4] + .5:
            _sello(im, xs["culpable"] + RW / 2, y + RH * .55, "EL CARNICERO", min(1.0, dt - mk[4] - .5), giro=10)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ la cadena de la Hermandad
def cadena(titulo, pasos, ancho=1760):
    """pasos = [(texto, ruta|None), ...] en dos filas de 3. Marca i = entra el paso i (retrato chico arriba, texto debajo) con un
    eslabón que lo une al anterior. Marca len(pasos): el último eslabón se rompe (las dos mitades se separan con chispas) y el
    último paso arde en rojo. Lo usé para boda → Emperador → sopa → doble → traición → santuario en llamas."""
    n = len(pasos)
    por_fila = math.ceil(n / 2)
    CW, CH, IMG = 380, 250, 150
    h = 110 + 2 * CH + 70

    def _eslabon(d, x0, y0, x1, y1, u, a, roto=0.0):
        """Dos óvalos entrelazados entre (x0,y0) y (x1,y1); roto 0..1 los separa."""
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        vert = abs(y1 - y0) > abs(x1 - x0)
        for s in (-1, 1):
            off = s * (16 + 22 * roto)
            if vert:
                c = (mx + 4 * s * roto, my + off)
                bb = (c[0] - 14, c[1] - 22, c[0] + 14, c[1] + 22)
            else:
                c = (mx + off, my + 4 * s * roto)
                bb = (c[0] - 22, c[1] - 14, c[0] + 22, c[1] + 14)
            col = SANGRE if roto > 0 else ORO
            d.ellipse(bb, outline=col + (int(a * u),), width=6)
        col = HUESO + (int(170 * u * (1 - roto)),)
        if vert:
            d.line([(x0, y0), (mx, my - 38)], fill=col, width=3)
            d.line([(mx, my + 38), (x1, y1)], fill=col, width=3)
        else:
            d.line([(x0, y0), (mx - 38, my)], fill=col, width=3)
            d.line([(mx + 38, my), (x1, y1)], fill=col, width=3)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        pos = []
        x_ini = M + (ancho - (por_fila * CW + (por_fila - 1) * 150)) / 2
        for i in range(n):
            fila, col = divmod(i, por_fila)
            if fila % 2:                                   # la segunda fila va de derecha a izquierda (serpiente)
                col = por_fila - 1 - col
            pos.append((x_ini + col * (CW + 150), M + 116 + fila * (CH + 40)))
        rompe = _eo((dt - mk[n]) / .5)
        for i in range(1, n):                              # eslabones entre pasos
            u = _eo((dt - mk[i]) / .4)
            if u <= 0:
                continue
            (xa, ya), (xb, yb) = pos[i - 1], pos[i]
            if ya == yb:
                p0 = (xa + CW if xb > xa else xa, ya + CH / 2)
                p1 = (xb if xb > xa else xb + CW, yb + CH / 2)
            else:
                p0, p1 = (xa + CW / 2, ya + CH), (xb + CW / 2, yb)
            _eslabon(d, p0[0], p0[1], p1[0], p1[1], u, 255, roto=rompe if i == n - 1 else 0)
        for i, (txt, ruta) in enumerate(pasos):
            u = _eo((dt - mk[i]) / .45)
            if u <= 0:
                continue
            x, y = pos[i]
            ultimo = i == n - 1
            arde = ultimo and rompe > 0
            fondo = (60, 12, 10) if arde else (22, 21, 20)
            d.rounded_rectangle((x, y, x + CW, y + CH), radius=16, fill=fondo + (int(220 * u),),
                                outline=(SANGRE if arde else HUESO) + (int(200 * u),), width=3 if arde else 2)
            if ruta:
                r = _retrato(ruta, IMG, IMG)
                if u < 1:
                    a = np.array(r)
                    a[..., 3] = (a[..., 3] * u).astype(np.uint8)
                    r = Image.fromarray(a)
                im.alpha_composite(r, (int(x + (CW - IMG) / 2), int(y + 18)))
            f = fuente("Bold Condensed" if arde else "SemiBold Condensed", 38)
            lineas = _partir(d, txt.upper(), f, CW - 30)
            for k, ln in enumerate(lineas[:2]):
                _texto(d, (x + CW / 2, y + (IMG + 50 if ruta else CH / 2 - 20) + 42 * k), ln, f,
                       SANGRE if arde else HUESO, "mm", 255 * u, track=2)
            _texto(d, (x + 28, y + 26), str(i + 1), fuente("Bold Condensed", 34), ORO, "mm", 255 * u)
            if arde:                                       # llamas: chispas que suben
                for c in range(18):
                    fase = (dt * .9 + c * .137) % 1
                    cxp = x + 20 + (c * 53) % (CW - 40) + 6 * math.sin(dt * 5 + c)
                    cyp = y + CH - 10 - fase * (CH - 20)
                    rr = 5 * (1 - fase) + 1
                    d.ellipse((cxp - rr, cyp - rr, cxp + rr, cyp + rr), fill=(255, 140 + int(80 * (1 - fase)), 40, int(230 * (1 - fase) * rompe)))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ la balanza
def balanza(titulo, izq, der, remate=None, ancho=1700):
    """Balanza de dos platos. izq = (texto, ruta|None) en la marca 0. der = [(texto, ruta|None), ...]: cada cosa cae al plato
    derecho en la marca 1+k y la balanza se inclina más hacia ese lado. remate = (texto, i_marca) en rojo abajo."""
    n = len(der)
    h = 110 + 520 + (80 if remate else 20)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 4)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, top = M + ancho * .34, M + 150
        llegados = sum(1 for k in range(n) if dt >= mk[1 + k])
        frac = 0.0
        for k in range(n):
            frac += _eo((dt - mk[1 + k]) / .6)
        ang = math.radians(-4 + 16 * frac / max(1, n))   # izquierda un poco más pesada al principio; luego gana la derecha
        a0 = 255 * _eo(dt / .4)
        # poste y base
        d.line([(cx, top), (cx, top + 400)], fill=ORO + (int(a0),), width=8)
        d.polygon([(cx - 90, top + 420), (cx + 90, top + 420), (cx + 40, top + 392), (cx - 40, top + 392)], fill=ORO + (int(a0),))
        d.ellipse((cx - 16, top - 16, cx + 16, top + 16), fill=ORO + (int(a0),))
        L = ancho * .20
        pts = {}
        for s in (-1, 1):
            ex = cx + s * L * math.cos(ang)
            ey = top + s * L * math.sin(ang)
            pts[s] = (ex, ey)
        d.line([pts[-1], pts[1]], fill=ORO + (int(a0),), width=8)
        for s in (-1, 1):                                  # cuerdas y plato
            ex, ey = pts[s]
            py = ey + 150
            d.line([(ex, ey), (ex - 120, py)], fill=HUESO + (int(a0 * .8),), width=2)
            d.line([(ex, ey), (ex + 120, py)], fill=HUESO + (int(a0 * .8),), width=2)
            d.chord((ex - 150, py - 30, ex + 150, py + 40), 0, 180, fill=(70, 58, 40, int(a0)), outline=ORO + (int(a0),), width=3)
        # plato izquierdo: lo que te pagan
        u = _eo((dt - mk[0]) / .45)
        ex, ey = pts[-1]
        py = ey + 150
        if u > 0:
            if izq[1]:
                r = _retrato(izq[1], 120, 120)
                im.alpha_composite(r, (int(ex - 60), int(py - 128 - 20 * (1 - u))))
            _texto(d, (ex, py + 74), izq[0].upper(), fuente("Bold Condensed", 46), BLANCO, "mm", 255 * u, track=2)
        # plato derecho: lo que pierdes, se apila
        ex, ey = pts[1]
        py = ey + 150
        for k, (txt, ruta) in enumerate(der):
            uk = _eo((dt - mk[1 + k]) / .45)
            if uk <= 0:
                continue
            col, fila = k % 3, k // 3
            xk = ex - 150 + col * 104
            yk = py - 116 - fila * 110 - 80 * (1 - uk)
            if ruta:
                r = _retrato(ruta, 98, 98)
                a = np.array(r)
                a[..., 3] = (a[..., 3] * uk).astype(np.uint8)
                im.alpha_composite(Image.fromarray(a), (int(xk), int(yk)))
                _marco(d, xk, yk, 98, 98, HUESO, 255 * uk, 2)
        # lista de lo perdido a la derecha del todo
        for k, (txt, ruta) in enumerate(der):
            uk = _eo((dt - mk[1 + k]) / .4)
            if uk <= 0:
                continue
            _texto(d, (M + ancho * .64, M + 160 + k * 64), "- " + txt.upper(), fuente("SemiBold Condensed", 36), HUESO, "lm", 255 * uk, track=2)
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 50), remate[0].upper(), fuente("Bold Condensed", max(8, int(52 * s))), SANGRE, "mm", track=3)
        return _salida(im, dt)
    return fn


# ================================================================== tes_cosas_inutiles (23-oct-2026): 6 MG nuevos
def _pega(im, r, x, y, u):
    """Pega la imagen RGBA r con opacidad u (0..1)."""
    if u <= 0:
        return
    if u < 1:
        a = np.array(r)
        a[..., 3] = (a[..., 3] * u).astype(np.uint8)
        r = Image.fromarray(a)
    im.alpha_composite(r, (int(x), int(y)))


def _redondo(ruta, D):
    """Retrato recortado en círculo (medallón)."""
    r = _retrato(ruta, D, D)
    m = Image.new("L", (D, D), 0)
    ImageDraw.Draw(m).ellipse((0, 0, D - 1, D - 1), fill=255)
    r.putalpha(Image.fromarray(np.minimum(np.array(r)[..., 3], np.array(m))))
    return r


def agenda(titulo, tramos, retrato=None, remate=None, ancho=1500):
    """Reloj de 24 h (0 arriba) cuyos sectores se pintan con la marca de cada tramo. tramos = [(h_ini, h_fin, etiqueta,
    color), ...]; a la derecha la lista «20:00 - 08:00  POSADA». Retrato en medallón al centro. remate = (texto, i_marca).
    Primer uso: la agenda de Nazeem (posada 12 h, mercado 4 h, paseo, posada otra vez)."""
    R = 215
    h = 110 + 2 * R + 90 + (70 if remate else 0)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(tramos) + 3)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, cy = M + ancho * .29, M + 120 + R + 10
        a0 = 255 * _eo(dt / .4)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(70, 66, 60, int(a0)), width=52)
        for hh in range(24):                               # marcas de las horas
            ang = math.radians(hh * 15 - 90)
            r0, r1 = R + 34, R + (48 if hh % 6 == 0 else 40)
            d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))],
                   fill=HUESO + (int(a0 * (1 if hh % 6 == 0 else .5)),), width=3 if hh % 6 == 0 else 2)
        for hh in (0, 6, 12, 18):
            ang = math.radians(hh * 15 - 90)
            _texto(d, (cx + (R + 74) * math.cos(ang), cy + (R + 74) * math.sin(ang)), f"{hh}:00", fuente("SemiBold Condensed", 28),
                   GRIS, "mm", a0)
        aguja = None
        for k, (h0, h1, et, col) in enumerate(tramos):
            u = _eo((dt - mk[k]) / .9)
            if u <= 0:
                continue
            span = (h1 - h0) % 24 or 24
            a_ini = h0 * 15 - 90
            a_fin = a_ini + span * 15 * u
            d.arc((cx - R, cy - R, cx + R, cy + R), a_ini, a_fin, fill=tuple(col) + (255,), width=50)
            aguja = a_fin
            yl = M + 150 + k * 92
            al = 255 * _eo((dt - mk[k]) / .35)
            xl = M + ancho * .58
            d.rounded_rectangle((xl, yl - 16, xl + 32, yl + 16), radius=6, fill=tuple(col) + (int(al),))
            _texto(d, (xl + 56, yl), f"{h0:02d}:00 - {h1:02d}:00", fuente("Condensed", 34), GRIS, "lm", al, track=2)
            _texto(d, (xl + 300, yl), et.upper(), fuente("SemiBold Condensed", 44), HUESO, "lm", al, track=3)
        if retrato:
            D = 2 * R - 90
            _pega(im, _redondo(retrato, D), cx - D / 2, cy - D / 2, _eo(dt / .5))
            d.ellipse((cx - D / 2 - 3, cy - D / 2 - 3, cx + D / 2 + 3, cy + D / 2 + 3), outline=HUESO + (int(a0),), width=3)
        if aguja is not None:
            ang = math.radians(aguja)
            d.line([(cx + (R - 30) * math.cos(ang), cy + (R - 30) * math.sin(ang)),
                    (cx + (R + 30) * math.cos(ang), cy + (R + 30) * math.sin(ang))], fill=SANGRE + (255,), width=8)
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (M + ancho * .58 + 260, M + h - 70), remate[0].upper(), fuente("Bold Condensed", max(8, int(54 * s))),
                   SANGRE, "mm", track=3)
        return _salida(im, dt)
    return fn


def lena(titulo, tronco, casa, precio, meta, nombre_casa, remate=None, ancho=1560):
    """La cuenta de la leña. marca 0: cae el primer tronco «1 TRONCO = precio MONEDAS» · marca 1: aparece la casa con su
    precio y la barra vacía · entre las marcas 2 y 3 los troncos se apilan, el contador corre hasta meta/precio troncos y la
    barra se llena hasta la casa · remate = (texto, i_marca) en rojo."""
    n_meta = meta // precio
    h = 110 + 470 + (70 if remate else 10)
    TW, TH = 120, 72

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        r_t = _retrato(tronco, TW, TH)
        u0 = _eo((dt - mk[0]) / .5)
        t2 = mk[2]
        t3 = mk[3] if mk[3] < 99 else t2 + 3
        u = 0.0 if dt < t2 else min(1.0, (dt - t2) / max(.5, t3 - t2))
        u = u ** 2.2                                          # empieza tronco a tronco y luego se dispara
        n = 1 if u0 > 0 else 0
        if u > 0:
            n = max(1, int(round(n_meta * u)))
        bx, by = M + 70, M + 540                              # pila en pirámide (15 visibles)
        k = 0
        for f_i, cnt in enumerate([5, 4, 3, 2, 1]):
            for c in range(cnt):
                if k >= min(15, n):
                    break
                _pega(im, r_t, bx + f_i * TW / 2 + c * TW, by - (f_i + 1) * (TH - 6), u0)
                k += 1
        xr = M + ancho * .50
        _texto(d, (xr, M + 160), "TRONCOS", fuente("Condensed", 32), GRIS, "lm", 255 * u0, track=4)
        _texto(d, (xr + 380, M + 160), f"{n:,}".replace(",", " "), fuente("Bold Condensed", 70), BLANCO, "rm", 255 * u0)
        _texto(d, (xr, M + 250), "MONEDAS", fuente("Condensed", 32), GRIS, "lm", 255 * u0, track=4)
        _texto(d, (xr + 380, M + 250), f"{n * precio:,}".replace(",", " "), fuente("Bold Condensed", 70), ORO, "rm", 255 * u0)
        if u0 > 0 and dt < t2:
            _texto(d, (xr + 190, M + 340), f"1 TRONCO = {precio} MONEDAS", fuente("SemiBold Condensed", 36), HUESO, "mm",
                   255 * u0, track=3)
        u1 = _eo((dt - mk[1]) / .5)
        if u1 > 0:
            cw, ch = 300, 190
            cxs, cys = M + ancho - 60 - cw, M + 110
            _pega(im, _retrato(casa, cw, ch), cxs, cys + 20 * (1 - u1), u1)
            _marco(d, cxs, cys, cw, ch, ORO, 255 * u1, 2)
            _texto(d, (cxs + cw / 2, cys + ch + 34), nombre_casa.upper(), fuente("SemiBold Condensed", 30), HUESO, "mm",
                   255 * u1, track=3)
            _texto(d, (cxs + cw / 2, cys + ch + 76), f"{meta:,}".replace(",", " ") + " MONEDAS", fuente("Bold Condensed", 40),
                   ORO, "mm", 255 * u1, track=2)
            x0, x1, yb = xr, M + ancho - 60, M + 450
            d.rounded_rectangle((x0, yb, x1, yb + 30), radius=15, fill=(40, 38, 34, int(235 * u1)),
                                outline=HUESO + (int(150 * u1),), width=2)
            fr = min(1.0, n * precio / meta)
            if fr > 0:
                d.rounded_rectangle((x0, yb, x0 + max(30, (x1 - x0) * fr), yb + 30), radius=15, fill=ORO + (255,))
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 50), remate[0].upper(), fuente("Bold Condensed", max(8, int(50 * s))), SANGRE, "mm",
                   track=3)
        return _salida(im, dt)
    return fn


def salud(titulo, chico, grande, n_chicos, ancho=1400):
    """Barras de salud rojas. chico/grande = (ruta, etiqueta, puntos). marca 0: fila del chico · marca 1: fila del grande ·
    entre las marcas 2 y 3 aparecen n_chicos iconos del chico y su barra crece hasta igualar al grande."""
    h = 110 + 3 * 140 + 30
    IC = 110

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        maxp = grande[2]
        x0, x1 = M + 330, M + ancho - 170

        def barra(y, et, pts, u, rojo_final=False):
            _texto(d, (x0, y - 42), et.upper(), fuente("SemiBold Condensed", 32), HUESO, "lm", 255 * u, track=3)
            d.rectangle((x0, y - 10, x1, y + 22), fill=(30, 10, 8, int(235 * u)), outline=HUESO + (int(120 * u),), width=2)
            w = (x1 - x0) * pts / maxp * u
            if w > 6:
                d.rectangle((x0 + 3, y - 7, x0 + w - 3, y + 19), fill=SANGRE + (255,))
            _texto(d, (x1 + 24, y + 6), f"+{int(round(pts * u))}", fuente("Bold Condensed", 54),
                   SANGRE if rojo_final else BLANCO, "lm", 255 * u)

        u = _eo((dt - mk[0]) / .5)
        if u > 0:
            _pega(im, _retrato(chico[0], IC, IC), M + 90, M + 170 - IC / 2, u)
            barra(M + 170, chico[1], chico[2], u)
        u = _eo((dt - mk[1]) / .5)
        if u > 0:
            _pega(im, _retrato(grande[0], IC, IC), M + 90, M + 310 - IC / 2, u)
            barra(M + 310, grande[1], grande[2], u)
        if dt >= mk[2]:
            t3 = mk[3] if mk[3] < 99 else mk[2] + 2.5
            v = min(1.0, (dt - mk[2]) / max(.5, t3 - mk[2]))
            k = max(1, min(n_chicos, int(v * n_chicos) + 1))
            y = M + 450
            for i in range(k):
                _pega(im, _retrato(chico[0], 70, 70), M + 40 + i * 50, y - 35, 1.0)
            barra(y, f"{k} × {chico[1]}", k * chico[2] * 1.0, 1.0, rojo_final=k == n_chicos)
        return _salida(im, dt)
    return fn


def receta(titulo, ingredientes, resultado, efecto, remate=None, ancho=1640):
    """ingredientes = [(ruta, nombre)]: entran uno por marca (0..n-1) en fila; en la marca n se juntan hacia el centro y sale
    resultado = (ruta, nombre) grande con `efecto` («+5 DE SALUD»); remate = (texto, i_marca)."""
    n = len(ingredientes)
    IW = 200
    h = 110 + 300 + 220 + (60 if remate else 0)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 4)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        sep = (ancho - 120 - n * IW) / max(1, n - 1)
        junta = _eo((dt - mk[n]) / .7)
        cx = M + ancho / 2
        for k, (ruta, nom) in enumerate(ingredientes):
            u = _eo((dt - mk[k]) / .45)
            if u <= 0:
                continue
            x = M + 60 + k * (IW + sep)
            y = M + 130 + 30 * (1 - u)
            x += (cx - IW / 2 - x) * junta
            y += 120 * junta
            a = u * (1 - junta)
            _pega(im, _retrato(ruta, IW, IW), x, y, a)
            _marco(d, x, y, IW, IW, HUESO, 255 * a, 2)
            if junta < .05:                                    # al juntarse, los nombres se amontonarían
                _texto(d, (x + IW / 2, y + IW + 30), nom.upper(), fuente("SemiBold Condensed", 32), HUESO, "mm", 255 * a, track=3)
            if k < n - 1 and junta <= 0:
                _texto(d, (x + IW + sep / 2, y + IW / 2), "+", fuente("Bold Condensed", 60), ORO, "mm", 255 * u)
        if junta > 0:
            s = _pop(dt - mk[n] - .4, .45)
            if s > .02:
                D = max(2, int(260 * s))
                _pega(im, _retrato(resultado[0], D, D), cx - D / 2, M + 120, 1.0)
                _texto(d, (cx, M + 120 + 260 + 40), resultado[1].upper(), fuente("SemiBold Condensed", 40), HUESO, "mm", track=4)
                _texto(d, (cx, M + 120 + 260 + 100), efecto.upper(), fuente("Bold Condensed", 64), SANGRE, "mm", track=3)
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (cx, M + h - 46), remate[0].upper(), fuente("Bold Condensed", max(8, int(46 * s))), ORO, "mm", track=3)
        return _salida(im, dt)
    return fn


def trato(titulo, perro, premio_a, premio_b, condiciones, datos, sello=None, ancho=1700):
    """Bifurcación del trato daédrico. perro = (ruta, nombre). marca 0: camino A (el perro vivo → premio_a = (ruta, nombre),
    texto condiciones[0]) · marca 1: camino B (el perro con aspa → premio_b, condiciones[1]) y el A se apaga · marcas 2..: una
    línea de `datos` por marca bajo el camino B · sello = (texto, i_marca) sobre el premio B."""
    RW, RH = 210, 250
    h = 110 + RH + 130 + len(datos) * 52 + 30

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(datos) + 6)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        ua, ub = _eo((dt - mk[0]) / .5), _eo((dt - mk[1]) / .5)
        apaga = .75 * ub
        y = M + 150
        for lado, u, prem, cond, tach in ((0, ua, premio_a, condiciones[0], False), (1, ub, premio_b, condiciones[1], True)):
            if u <= 0:
                continue
            x0 = M + 50 + lado * ancho / 2
            gris = apaga if lado == 0 else 0
            ut = _eo((dt - mk[1] - .4) / .5) if tach else 0
            _pega(im, _retrato(perro[0], RW, RH, gris=max(gris, .8 * ut)), x0, y, u)
            _marco(d, x0, y, RW, RH, HUESO, 255 * u, 2)
            if ut > 0:
                _tacha(d, x0, y, RW, RH, ut)
            _texto(d, (x0 + RW / 2, y + RH + 30), perro[1].upper(), fuente("SemiBold Condensed", 30),
                   SANGRE if ut > .5 else HUESO, "mm", 255 * u, track=3)
            ax = x0 + RW + 24
            k = _eo((dt - mk[lado] - .3) / .5)
            colf = SANGRE if tach else ORO
            if k > 0:
                d.line([(ax, y + RH / 2), (ax + 130 * k, y + RH / 2)], fill=colf + (255,), width=6)
            if k > .9:
                d.polygon([(ax + 130, y + RH / 2 - 16), (ax + 156, y + RH / 2), (ax + 130, y + RH / 2 + 16)], fill=colf + (255,))
            px = ax + 176
            if k > 0:
                _pega(im, _retrato(prem[0], RW, RH, gris=gris), px, y, k)
                _marco(d, px, y, RW, RH, colf, 255 * k, 3)
                _texto(d, (px + RW / 2, y + RH + 30), prem[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * k,
                       track=3)
            _texto(d, ((x0 + px + RW) / 2, y - 34), cond.upper(), fuente("Condensed", 30), GRIS if gris > .3 else HUESO, "mm",
                   255 * u, track=3)
        xb = M + 50 + ancho / 2
        for i, txt in enumerate(datos):
            u = _eo((dt - mk[2 + i]) / .35)
            if u <= 0:
                continue
            yy = y + RH + 92 + i * 52
            _texto(d, (xb, yy), "- " + txt.upper(), fuente("SemiBold Condensed", 36), HUESO, "lm", 255 * u, track=2)
        if sello and dt >= mk[sello[1]]:
            _sello(im, xb + RW + 176 + RW / 2, y + RH * .55, sello[0], min(1.0, dt - mk[sello[1]]), giro=-10, tam=40)
        return _salida(im, dt)
    return fn


def compraventa(titulo, objeto, pasos, remate=None, ancho=1700):
    """Libro de cuentas en línea de tiempo. objeto = (ruta, nombre) arriba al centro. pasos = [(texto, delta|None), ...]: el nodo
    i entra en la marca i con su texto y su movimiento (+2 000 en oro, -4 000 en rojo); abajo «TU BALANCE» corre con cada
    movimiento. remate = (texto, i_marca)."""
    n = len(pasos)
    h = 110 + 200 + 250 + (60 if remate else 0)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 4)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        ow, oh = 520, 120
        _pega(im, _retrato(objeto[0], ow, oh), M + ancho / 2 - ow / 2, M + 112, a0)
        y = M + 350
        x0, x1 = M + 170, M + ancho - 170
        d.line([(x0, y), (x1, y)], fill=(70, 66, 60, int(255 * a0)), width=6)
        bal = 0.0
        for i, (txt, delta) in enumerate(pasos):
            u = _eo((dt - mk[i]) / .5)
            x = x0 + (x1 - x0) * i / max(1, n - 1)
            if i > 0 and u > 0:
                xa = x0 + (x1 - x0) * (i - 1) / max(1, n - 1)
                d.line([(xa, y), (xa + (x - xa) * u, y)], fill=HUESO + (255,), width=6)
            if u <= 0:
                d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(30, 30, 30, int(230 * a0)), outline=GRIS + (int(220 * a0),), width=3)
                continue
            col = ORO if (delta or 0) > 0 else SANGRE if (delta or 0) < 0 else HUESO
            r = 12 + 10 * min(1.0, _pop(dt - mk[i], .35))
            d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,), outline=BLANCO + (255,), width=3)
            for k, ln in enumerate(_partir(d, txt.upper(), fuente("SemiBold Condensed", 30), 320)[:3]):
                _texto(d, (x, y + 50 + 36 * k), ln, fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * u, track=2)
            if delta:
                _texto(d, (x, y - 50), ("+" if delta > 0 else "-") + f"{abs(delta):,}".replace(",", " "),
                       fuente("Bold Condensed", 50), col, "mm", 255 * u)
                bal += delta * min(1.0, (dt - mk[i]) / .8)
        yb = M + h - (110 if remate else 55)
        _texto(d, (M + ancho / 2 - 20, yb), "TU BALANCE", fuente("Condensed", 30), GRIS, "rm", 255 * a0, track=4)
        _texto(d, (M + ancho / 2 + 20, yb), ("-" if bal < 0 else "") + f"{abs(int(bal)):,}".replace(",", " "),
               fuente("Bold Condensed", 56), SANGRE if bal < 0 else ORO, "lm", 255 * a0)
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 44), remate[0].upper(), fuente("Bold Condensed", max(8, int(44 * s))), SANGRE, "mm",
                   track=3)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ tes_armas_poderosas (23-oct-2026)
def _num(v):
    """1980 -> «1 980» (separador de miles con espacio, como el resto del canal)."""
    if isinstance(v, float) and not v.is_integer() and abs(v) < 100:
        return f"{v:.3f}".rstrip("0").replace(".", ",")   # 1,045 sin redondear: 1,08 y 1,03 no pueden salir iguales
    return f"{int(round(v)):,}".replace(",", " ")


_rul = {}
_ic = {}


def _icono(ruta, w, h):
    """Como _retrato, pero un arma larga con fondo transparente (espada, arco) se tumba en horizontal para llenar un icono
    apaisado en vez de quedar como una astilla."""
    k = (ruta, w, h)
    if k not in _ic:
        im = Image.open(ruta).convert("RGBA")
        if (np.array(im)[..., 3] < 10).mean() > .12:
            im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox())
            if im.height > im.width * 1.6:
                im = im.rotate(-90, expand=True, resample=Image.BICUBIC)
            esc = min((w - 16) / im.width, (h - 16) / im.height)
            im = im.resize((max(2, int(im.width * esc)), max(2, int(im.height * esc))), Image.LANCZOS)
            fondo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            m = Image.new("L", (w, h), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=255)
            fondo.paste(Image.new("RGBA", (w, h), (30, 28, 26, 235)), (0, 0), m)
            ImageDraw.Draw(fondo).rounded_rectangle((0, 0, w - 1, h - 1), 14, outline=HUESO + (150,), width=2)
            fondo.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
            _ic[k] = fondo
        else:
            _ic[k] = _retrato(ruta, w, h)
    return _ic[k]


def ruleta(titulo, opciones, paradas, ancho=1560):
    """Ruleta del Wabbajack: rueda con un sector por opción [(etiqueta, color)] que gira despacio y, en cada marca k, da
    dos vueltas y frena con `paradas[k]` (índice de opción) bajo el puntero de arriba; cada resultado se apunta en la lista
    de la derecha (el último en su color). Primer uso: «Puede lanzar fuego… o en un bollo dulce» (n.º 14)."""
    n = len(opciones)
    h = 760
    R = 270
    paso = 360 / n

    def rueda():
        k = (titulo, n)
        if k not in _rul:
            D = 2 * R + 20
            im = Image.new("RGBA", (D, D), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            c = D / 2
            for i in range(n):
                base = (34, 30, 28) if i % 2 == 0 else (18, 16, 15)
                d.pieslice((c - R, c - R, c + R, c + R), i * paso, (i + 1) * paso, fill=base + (245,))
            for i in range(n):                                   # radios color hueso
                a = math.radians(i * paso)
                d.line([(c, c), (c + R * math.cos(a), c + R * math.sin(a))], fill=HUESO + (200,), width=3)
            d.ellipse((c - R, c - R, c + R, c + R), outline=HUESO + (255,), width=5)
            d.ellipse((c - R + 14, c - R + 14, c + R - 14, c + R - 14), outline=(120, 112, 100, 160), width=2)
            f = fuente("SemiBold Condensed", 30)
            for i, (et, col) in enumerate(opciones):             # etiqueta radial, leyendo hacia fuera
                s = et.upper()
                tw = int(_ancho_track(d, s, f, 2)) + 10
                t = Image.new("RGBA", (tw, 44), (0, 0, 0, 0))
                _texto(ImageDraw.Draw(t), (tw / 2, 22), s, f, col, "mm", track=2)
                ang = (i + .5) * paso
                t = t.rotate(-ang, expand=True, resample=Image.BICUBIC)
                rr = R * .60
                x = c + rr * math.cos(math.radians(ang)) - t.width / 2
                y = c + rr * math.sin(math.radians(ang)) - t.height / 2
                im.alpha_composite(t, (int(x), int(y)))
            d.ellipse((c - 46, c - 46, c + 46, c + 46), fill=(10, 10, 12, 255), outline=HUESO + (255,), width=4)
            d.polygon([(c - 12, c), (c, c - 12), (c + 12, c), (c, c + 12)], fill=SANGRE + (255,))
            _rul[k] = im
        return _rul[k]

    def durs(mk):                                                 # giros seguidos más cortos (nunca se pisan)
        return [max(.6, min(1.6, mk[k + 1] - mk[k] - .15)) if mk[k + 1] < 99 else 1.6 for k in range(len(paradas))]

    def angulo(dt, mk):
        a = 18.0 * min(dt, mk[0])                                 # deriva lenta antes del primer giro
        ds = durs(mk)
        for k, idx in enumerate(paradas):
            if dt < mk[k]:
                break
            meta = (idx + .5) * paso + 90                         # sector idx bajo el puntero (arriba)
            fin = a + ((meta - a) % 360) + (720 if ds[k] > 1.2 else 360)
            u = _eo((dt - mk[k]) / ds[k])
            a = a + (fin - a) * u
            if u < 1:
                break
        return a

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(paradas) + 2)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        rw = rueda()
        cx, cy = M + 90 + R + 10, M + 120 + R + 10
        r = rw.rotate(angulo(dt, mk), resample=Image.BICUBIC)
        im.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))
        d.polygon([(cx - 22, cy - R - 34), (cx + 22, cy - R - 34), (cx, cy - R + 6)], fill=HUESO + (255,),
                  outline=(0, 0, 0, 255))                          # puntero
        ds = durs(mk)
        hechos = [k for k in range(len(paradas)) if dt >= mk[k] + ds[k]]
        if hechos:                                                 # el sector ganador brilla bajo el puntero
            k = hechos[-1]
            et, col = opciones[paradas[k]]
            br = .55 + .45 * math.sin((dt - mk[k]) * 6)
            d.pieslice((cx - R, cy - R, cx + R, cy + R), 270 - paso / 2, 270 + paso / 2, outline=col + (int(255 * br),),
                       width=6)
        xl = M + 2 * R + 190
        _texto(d, (xl, M + 150), "RESULTADOS", fuente("Condensed", 30), GRIS, "lm", track=5)
        for j, k in enumerate(hechos[-9:]):
            et, col = opciones[paradas[k]]
            u = _eo((dt - mk[k] - ds[k]) / .35)
            y = M + 210 + j * 58
            _texto(d, (xl + 40 * (1 - u), y), et.upper(), fuente("Bold Condensed", 46), col if k == hechos[-1] else HUESO, "lm",
                   255 * u, track=2)
        return _salida(im, dt)
    return fn


def barras(titulo, filas, refs=(), unidad="", remate=None, ancho=1660):
    """Barras horizontales comparadas. filas = [(ruta|None, etiqueta, valor, i_marca, color)]: cada barra crece en su marca
    y su número corre. refs = [(etiqueta, valor, i_marca)]: líneas verticales punteadas de referencia (salud de un dragón).
    La escala la fija el mayor de todos los valores. remate = (texto, i_marca). Primer uso: «Una sola puñalada» (n.º 1)."""
    AF = 104
    h = 200 + len(filas) * AF + (90 if remate else 40)
    vmax = max([f[2] for f in filas] + [r[1] for r in refs]) * 1.04
    IW, IC = 170, 84

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 12
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, x1 = M + 560, M + ancho - 200
        ytop = M + 190
        for k, (ruta, et, v, i, col) in enumerate(filas):
            t0 = mk[i]
            if dt < t0:
                continue
            u = _eo((dt - t0) / .9)
            y = ytop + k * AF + AF / 2
            a = 255 * _eo((dt - t0) / .3)
            if ruta:
                _pega(im, _icono(ruta, IW, IC), M + 50, y - IC / 2, a / 255)
            lns = _partir(d, et.upper(), fuente("SemiBold Condensed", 30), 230)[:2]
            for j, ln in enumerate(lns):
                _texto(d, (M + 240, y + 32 * j - 16 * (len(lns) - 1)), ln, fuente("SemiBold Condensed", 30), HUESO, "lm", a,
                       track=2)
            d.rectangle((x0, y - 20, x1, y + 20), fill=(24, 20, 18, int(.8 * a)))
            w = (x1 - x0) * v / vmax * u
            if w > 4:
                d.rectangle((x0, y - 16, x0 + w, y + 16), fill=col + (255,))
                d.rectangle((x0, y - 16, x0 + w, y - 9), fill=tuple(min(255, c + 40) for c in col) + (255,))
            _texto(d, (min(x0 + w + 18, x1 + 10), y + 2), _num(v * u if u < 1 else v) + unidad, fuente("Bold Condensed", 48),
                   BLANCO, "lm", a)
        for kr, (et, v, i) in enumerate(refs):
            if dt < mk[i]:
                continue
            a = 255 * _eo((dt - mk[i]) / .4)
            x = x0 + (x1 - x0) * v / vmax
            yb = ytop + len(filas) * AF
            for yy in range(int(ytop - 6 - 32 * (kr % 2)), int(yb), 18):
                d.line([(x, yy), (x, yy + 10)], fill=SANGRE + (int(a),), width=4)
            _texto(d, (min(x, M + ancho - 250), ytop - 26 - 32 * (kr % 2)),f"{et.upper()} · {_num(v)}", fuente("SemiBold Condensed", 28),
                   SANGRE, "mm", a, track=2)
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 48), remate[0].upper(), fuente("Bold Condensed", max(8, int(46 * s))), ORO, "mm",
                   track=3)
        return _salida(im, dt)
    return fn


def niveles(titulo, pasos, notas=(), unidad="", ancho=1500):
    """Escalera del arma que «sube contigo»: pasos = [(rango de nivel, valor)] que aparecen uno a uno entre las marcas 0 y 1
    (columna alta según el valor). notas = [(i_paso, texto, color, i_marca)]: en su marca la columna se enmarca en ese color
    con el texto encima (la trampa: «NO SE MEJORA», «PROMETE 30, HACE 20»). Primer uso: Hoja de Ruiseñor y Azote de dragones."""
    n = len(pasos)
    h = 700
    vmax = max(v for _, v in pasos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 10
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t0, t1 = mk[0], (mk[1] if mk[1] < 99 else mk[0] + 2.5)
        x0, x1 = M + 110, M + ancho - 110
        yb, hmax = M + h - 100, h - 400
        cw = (x1 - x0) / n
        d.line([(x0 - 20, yb), (x1 + 20, yb)], fill=HUESO + (200,), width=3)
        for i, (rango, v) in enumerate(pasos):
            ti = t0 + (t1 - t0) * i / max(1, n - 1) if n > 1 else t0
            if dt < ti:
                continue
            u = _eo((dt - ti) / .5)
            xa, xb = x0 + i * cw + 18, x0 + (i + 1) * cw - 18
            hh = hmax * (.25 + .75 * v / vmax) * u
            d.rectangle((xa, yb - hh, xb, yb), fill=(46, 40, 34, 235), outline=HUESO + (150,), width=2)
            d.rectangle((xa + 4, yb - hh + 4, xb - 4, yb - hh + 16), fill=ORO + (220,))
            _texto(d, ((xa + xb) / 2, yb + 40), "NIV. " + rango, fuente("SemiBold Condensed", 32), GRIS, "mm", 255 * u, track=2)
            _texto(d, ((xa + xb) / 2, yb - hh - 40), "+" + _num(v) + unidad, fuente("Bold Condensed", 56), BLANCO, "mm", 255 * u)
        for i, txt, col, im_ in notas:
            if dt < mk[im_]:
                continue
            rango, v = pasos[i]
            xa, xb = x0 + i * cw + 18, x0 + (i + 1) * cw - 18
            hh = hmax * (.25 + .75 * v / vmax)
            br = .65 + .35 * math.sin((dt - mk[im_]) * 5)
            d.rectangle((xa - 6, yb - hh - 6, xb + 6, yb + 6), outline=col + (int(255 * br),), width=6)
            s = _pop(dt - mk[im_], .35)
            lns = _partir(d, txt.upper(), fuente("Bold Condensed", 34), cw + 30)[:2]
            for j, ln in enumerate(lns):
                _texto(d, ((xa + xb) / 2, yb - hh - 100 - 38 * (len(lns) - 1 - j)), ln,
                       fuente("Bold Condensed", max(8, int(34 * s))), col, "mm", track=2)
        return _salida(im, dt)
    return fn


def golpes(titulo, objetivo, salud, filas, fases=("Dragón de fuego", "Dragón de escarcha"), remate=None, ancho=1500):
    """¿Cuántos golpes para tumbar a X? objetivo = (ruta, nombre); salud = su vida. filas = [(ruta, arma, golpes_a, golpes_b)].
    marca 0: la barra de salud se vacía y los contadores corren hasta golpes_a (fase A) · marca 1: la fase pasa a la B y los
    contadores ruedan hasta golpes_b; la fila con menos golpes se pone en oro y las que suben en rojo · remate = (texto, i)."""
    AF = 130
    h = 330 + len(filas) * AF + (80 if remate else 20)
    IC = 100

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        _pega(im, _retrato(objetivo[0], 220, 124), M + 70, M + 120, a0)
        fase_b = dt >= mk[1]
        _texto(d, (M + 320, M + 150), (fases[1] if fase_b else fases[0]).upper(), fuente("Bold Condensed", 46),
               (150, 200, 255) if fase_b else (255, 150, 90), "lm", 255 * a0, track=3)
        bx0, bx1, by = M + 320, M + ancho - 260, M + 205
        ua = (dt - mk[0]) / 2.2 if dt >= mk[0] else 0.0
        vida = 1.0 - min(1.0, max(0.0, ua)) if not fase_b else 1.0 - min(1.0, (dt - mk[1]) / 2.2)
        d.rectangle((bx0, by, bx1, by + 30), fill=(30, 10, 8, int(235 * a0)), outline=HUESO + (int(140 * a0),), width=2)
        if vida > .003:
            d.rectangle((bx0 + 3, by + 3, bx0 + 3 + (bx1 - bx0 - 6) * vida, by + 27), fill=SANGRE + (255,))
        _texto(d, (bx1 + 24, by + 15), _num(salud * vida), fuente("Bold Condensed", 44), BLANCO, "lm", 255 * a0)
        mejor = min(f[3] for f in filas)
        for k, (ruta, arma, ga, gb) in enumerate(filas):
            y = M + 290 + k * AF
            _pega(im, _icono(ruta, 190, IC), M + 70, y, a0)
            _texto(d, (M + 290, y + IC / 2), arma.upper(), fuente("SemiBold Condensed", 40), HUESO, "lm", 255 * a0, track=3)
            if dt < mk[0]:
                continue
            if not fase_b:
                v, col = ga * min(1.0, max(0.0, ua)), BLANCO
            else:
                ub = _eo((dt - mk[1]) / 1.6)
                v = ga + (gb - ga) * ub
                col = ORO if gb == mejor and ub >= 1 else SANGRE if gb > ga and ub >= 1 else BLANCO
            _texto(d, (M + ancho - 90, y + IC / 2), f"{int(round(v))} GOLPES", fuente("Bold Condensed", 60), col, "rm", 255,
                   track=2)
        if remate and dt >= mk[remate[1]]:
            s = _pop(dt - mk[remate[1]], .35)
            _texto(d, (M + ancho / 2, M + h - 46), remate[0].upper(), fuente("Bold Condensed", max(8, int(46 * s))), ORO, "mm",
                   track=3)
        return _salida(im, dt)
    return fn


# ================================================================== tes_cosas_nunca (27-oct-2026): 4 MG nuevos
def _remate(d, M, ancho, h, remate, dt, mk, color=SANGRE, tam=50):
    if remate and dt >= mk[remate[1]]:
        s = _pop(dt - mk[remate[1]], .35)
        _texto(d, (M + ancho / 2, M + h - 48), remate[0].upper(), fuente("Bold Condensed", max(8, int(tam * s))), color, "mm",
               track=3)


def _sol(d, x, y, r, a, noche=False):
    """Iconito de sol (rayos) o de luna (creciente) para la línea de los días."""
    if noche:
        d.ellipse((x - r, y - r, x + r, y + r), fill=(200, 205, 230, int(a)))
        d.ellipse((x - r + r * .55, y - r - r * .15, x + r + r * .55, y + r - r * .15), fill=(6, 6, 8, int(a)))
        return
    for k in range(8):
        ang = k * math.pi / 4
        d.line([(x + r * 1.35 * math.cos(ang), y + r * 1.35 * math.sin(ang)),
                (x + r * 1.8 * math.cos(ang), y + r * 1.8 * math.sin(ang))], fill=ORO + (int(a),), width=3)
    d.ellipse((x - r, y - r, x + r, y + r), fill=ORO + (int(a),))


def plazo(titulo, horas, retrato, avisos=(), curas=(), final=None, remate=None, ancho=1600):
    """Cuenta atrás de un plazo del juego en una línea de días (sol/luna). retrato = (ruta, nombre) en medallón a la izquierda.
    marca 0: el marcador echa a andar · avisos = [(hora, texto)]: salen bajo la línea cuando el marcador pasa por esa hora ·
    curas = [(ruta, nombre)]: fila de remedios que se tachan cuando el plazo se acaba · final = (texto, i_marca): el plazo
    llega a `horas` en esa marca, el medallón se pone rojo con el texto · remate = (texto, i). Primer uso: Sanguinare Vampiris
    (72 h, los dos avisos del juego, las curas tachadas) y el seguidor que se cansa de esperar (72 h)."""
    h = 110 + 300 + 46 * max(0, len(avisos) - 1) + (150 if curas else 0) + (70 if remate else 10)
    D = 210

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        t_fin = mk[final[1]] if final else dur - .8
        u = 0.0 if dt < mk[0] else min(1.0, (dt - mk[0]) / max(.6, t_fin - mk[0]))
        acabado = final and dt >= t_fin
        cx, cy = M + 60 + D / 2, M + 120 + D / 2
        _pega(im, _redondo(retrato[0], D), cx - D / 2, cy - D / 2, a0)
        d.ellipse((cx - D / 2 - 4, cy - D / 2 - 4, cx + D / 2 + 4, cy + D / 2 + 4),
                  outline=(SANGRE if acabado else HUESO) + (int(255 * a0),), width=6 if acabado else 3)
        if not acabado:
            _texto(d, (cx, cy + D / 2 + 34), retrato[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * a0, track=3)
        x0, x1, yl = M + 380, M + ancho - 90, M + 205
        d.rounded_rectangle((x0, yl - 12, x1, yl + 12), radius=12, fill=(40, 38, 34, int(235 * a0)),
                            outline=HUESO + (int(120 * a0),), width=2)
        dias = max(1, int(round(horas / 24)))
        for k in range(dias + 1):                               # divisiones por día, con sol (amanecer) y luna (anochecer)
            xk = x0 + (x1 - x0) * k / dias
            d.line([(xk, yl - 26), (xk, yl + 26)], fill=HUESO + (int(200 * a0),), width=3)
            _texto(d, (xk, yl - 54), f"{k * 24} H", fuente("Condensed", 28), GRIS, "mm", 255 * a0, track=2)
            if k < dias:
                _sol(d, xk + (x1 - x0) / dias * .25, yl + 56, 11, 230 * a0)
                _sol(d, xk + (x1 - x0) / dias * .75, yl + 56, 11, 230 * a0, noche=True)
        if u > 0:
            xm = x0 + (x1 - x0) * u
            d.rounded_rectangle((x0 + 2, yl - 9, max(x0 + 20, xm), yl + 9), radius=9, fill=(SANGRE if acabado else ORO) + (255,))
            d.polygon([(xm - 14, yl - 40), (xm + 14, yl - 40), (xm, yl - 16)], fill=BLANCO + (255,))
            _texto(d, (xm, yl - 92), f"{int(round(horas * u))} H", fuente("Bold Condensed", 46), BLANCO, "mm", 255)
        for k, (hh, txt) in enumerate(avisos):                   # los avisos del juego, cuando el marcador pasa por su hora
            if u * horas >= hh:
                ua = _eo((u * horas - hh) / (horas * .06))
                _texto(d, ((x0 + x1) / 2, yl + 112 + 46 * k), "« " + txt.upper() + " »",
                       fuente("SemiBold Condensed", 34), HUESO, "mm", 255 * ua, track=2)
        if curas:
            yc = M + 110 + 300 + 20 + 46 * max(0, len(avisos) - 1)
            n = len(curas)
            paso = (x1 - x0) / n
            for k, (ruta, nom) in enumerate(curas):
                xk = x0 + paso * k + 20
                _pega(im, _retrato(ruta, 96, 96), xk, yc, a0)
                _texto(d, (xk + 116, yc + 48), nom.upper(), fuente("SemiBold Condensed", 32), HUESO, "lm", 255 * a0, track=2)
                if acabado:
                    ux = _eo((dt - t_fin - .25 * k) / .3)
                    if ux > 0:
                        x_e = xk + (paso - 40) * ux
                        d.line([(xk - 6, yc + 48), (x_e, yc + 48)], fill=SANGRE + (255,), width=7)
        if acabado:
            s = _pop(dt - t_fin, .35)
            _texto(d, (cx, cy + D / 2 + 40), final[0].upper(), fuente("Bold Condensed", max(8, int(52 * s))), SANGRE, "mm", track=4)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def paciencia(titulo, retrato, golpes=3, aviso="Aviso", estallido="Hostil", remate=None, ancho=1100):
    """La paciencia de un PNJ: medallón y `golpes` casillas; en cada marca 0..golpes-1 un golpe llena una casilla
    («AVISO») con un temblor; en la marca `golpes` el medallón se tiñe de rojo, tiembla y sale `estallido`.
    Primer uso: el fuego amigo con Lydia (más de tres golpes y se vuelve hostil)."""
    h = 110 + 330 + (70 if remate else 10)
    D = 230

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (golpes + 4)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        roto = dt >= mk[golpes]
        sac = 0.0
        for k in range(golpes + 1):                           # temblor corto en cada golpe
            if 0 <= dt - mk[k] < .35:
                sac = (1 - (dt - mk[k]) / .35) * (16 if k == golpes else 7)
        sx = sac * math.sin(dt * 90)
        cx, cy = M + 90 + D / 2 + sx, M + 130 + D / 2
        r = _redondo(retrato[0], D)
        if roto:
            a = np.array(r).astype(np.float32)
            v = min(1.0, (dt - mk[golpes]) / .4)
            a[..., 0] = a[..., 0] * (1 - .35 * v) + 200 * .35 * v
            a[..., 1] *= 1 - .45 * v
            a[..., 2] *= 1 - .45 * v
            r = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        _pega(im, r, cx - D / 2, cy - D / 2, a0)
        d.ellipse((cx - D / 2 - 4, cy - D / 2 - 4, cx + D / 2 + 4, cy + D / 2 + 4),
                  outline=(SANGRE if roto else HUESO) + (int(255 * a0),), width=7 if roto else 3)
        _texto(d, (cx, cy + D / 2 + 36), retrato[1].upper(), fuente("SemiBold Condensed", 32), HUESO, "mm", 255 * a0, track=3)
        bw, gap = 190, 28
        x0 = M + 90 + D + 90
        for k in range(golpes):
            xk, yk = x0 + k * (bw + gap), M + 150
            lleno = dt >= mk[k]
            d.rounded_rectangle((xk, yk, xk + bw, yk + 110), radius=14, fill=(30, 26, 22, int(220 * a0)),
                                outline=(ORO if lleno else GRIS) + (int(220 * a0),), width=3)
            if lleno:
                s = _pop(dt - mk[k], .3)
                _texto(d, (xk + bw / 2, yk + 46), f"{k + 1}", fuente("Bold Condensed", max(8, int(64 * s))), ORO, "mm")
                _texto(d, (xk + bw / 2, yk + 92), aviso.upper(), fuente("SemiBold Condensed", 26), HUESO, "mm", 255, track=3)
        if roto:
            s = _pop(dt - mk[golpes], .35)
            _texto(d, (x0 + (golpes * (bw + gap) - gap) / 2, M + 340), estallido.upper(),
                   fuente("Bold Condensed", max(8, int(84 * s))), SANGRE, "mm", track=8)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def escalado(titulo, objeto, contador, niveles_, tu, hitos, remate=None, ancho=1700):
    """Subir de nivel sin pelear. objeto = (ruta, nombre) del objeto que se fabrica; contador = (n_fin, etiqueta).
    niveles_ = (nivel_ini, nivel_fin): entre las marcas 0 y 1 el contador corre hasta n_fin y TU NIVEL sube de nivel_ini a
    nivel_fin en una regla de niveles (0-80); tu = (ruta, etiqueta): tu arma, que se queda clavada en nivel_ini, en gris ·
    hitos = [(nivel, ruta, texto, i_marca)]: lo que el mundo trae a ese nivel aparece sobre la regla en su marca (en rojo) ·
    remate = (texto, i). Primer uso: cien dagas de hierro, dragones de escarcha (27) y legendarios (78)."""
    h = 110 + 620 + (70 if remate else 10)
    NMAX = 80

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        u = 0.0 if dt < mk[0] else min(1.0, (dt - mk[0]) / max(.6, mk[1] - mk[0] if mk[1] < 99 else 3.0))
        u = 1 - (1 - u) ** 2
        _pega(im, _icono(objeto[0], 150, 150), M + 70, M + 130, a0)
        _texto(d, (M + 145, M + 310), f"{int(round(contador[0] * u))}", fuente("Bold Condensed", 76), BLANCO, "mm", 255 * a0)
        _texto(d, (M + 145, M + 362), contador[1].upper(), fuente("SemiBold Condensed", 26), GRIS, "mm", 255 * a0, track=3)
        x0, x1 = M + 330, M + ancho - 110
        yr = M + 560
        d.line([(x0, yr), (x1, yr)], fill=HUESO + (int(200 * a0),), width=3)
        for nv in range(0, NMAX + 1, 10):
            xn = x0 + (x1 - x0) * nv / NMAX
            d.line([(xn, yr - 12), (xn, yr + 12)], fill=HUESO + (int(200 * a0),), width=2)
            _texto(d, (xn, yr + 38), str(nv), fuente("Condensed", 28), GRIS, "mm", 255 * a0)
        _texto(d, (x0, yr + 80), "NIVEL", fuente("SemiBold Condensed", 26), GRIS, "lm", 255 * a0, track=4)

        def xn(nv):
            return x0 + (x1 - x0) * nv / NMAX
        n_tu = niveles_[0] + (niveles_[1] - niveles_[0]) * u
        yb1, yb2 = M + 150, M + 250                                 # dos barras: tu personaje y tu arma
        _texto(d, (x0, yb1 - 32), "TU PERSONAJE", fuente("SemiBold Condensed", 30), HUESO, "lm", 255 * a0, track=3)
        d.rounded_rectangle((x0, yb1, x1, yb1 + 34), radius=17, fill=(40, 38, 34, int(230 * a0)))
        d.rounded_rectangle((x0, yb1, max(x0 + 34, xn(n_tu)), yb1 + 34), radius=17, fill=ORO + (int(255 * a0),))
        _texto(d, (xn(n_tu) + 16, yb1 + 17), f"NIVEL {int(round(n_tu))}", fuente("Bold Condensed", 36), BLANCO, "lm", 255 * a0)
        _texto(d, (x0, yb2 - 32), tu[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "lm", 255 * a0, track=3)
        d.rounded_rectangle((x0, yb2, x1, yb2 + 34), radius=17, fill=(40, 38, 34, int(230 * a0)))
        d.rounded_rectangle((x0, yb2, xn(niveles_[0]), yb2 + 34), radius=17, fill=GRIS + (int(255 * a0),))
        _texto(d, (xn(niveles_[0]) + 16, yb2 + 17), f"NIVEL {niveles_[0]}", fuente("Bold Condensed", 36), GRIS, "lm", 255 * a0)
        for nv, ruta, txt, i in hitos:                               # lo que trae el mundo a cada nivel
            uh = _eo((dt - mk[i]) / .45)
            if uh <= 0:
                continue
            xh = xn(nv)
            d.line([(xh, yb1 - 10), (xh, yr)], fill=SANGRE + (int(220 * uh),), width=4)
            iw = 170
            _pega(im, _retrato(ruta, iw, 96), xh - iw / 2, yr - 140 - 30 * (1 - uh), uh)
            _marco(d, xh - iw / 2, yr - 140 - 30 * (1 - uh), iw, 96, SANGRE, 255 * uh, 3)
            _texto(d, (min(xh, x1 - 110), yr + 80), txt.upper(), fuente("Bold Condensed", 32), SANGRE, "mm", 255 * uh, track=2)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def reinicio(titulo, objetos, dias, seguro, remate=None, ancho=1700):
    """El cofre que se reinicia. objetos = [(ruta, nombre)]: entran al cofre uno por marca (0..n-1) · marca n: el calendario
    de `dias` casillas se tacha día a día hasta la marca n+1, y en ella los objetos se desvanecen uno tras otro y queda
    «VACÍO» · seguro = (ruta, texto, i_marca): a la derecha tu casa con un sello verde «SEGURO» · remate = (texto, i)."""
    n = len(objetos)
    h = 110 + 520 + (70 if remate else 10)
    VERDE = (120, 210, 120)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 6)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        cx0, cy0, cw, ch = M + 70, M + 120, 820, 330                # el «cofre»: rejilla de inventario
        d.rounded_rectangle((cx0, cy0, cx0 + cw, cy0 + ch), radius=18, fill=(34, 26, 18, int(235 * a0)),
                            outline=ORO + (int(220 * a0),), width=4)
        _texto(d, (cx0 + cw / 2, cy0 + 34), "COFRE CUALQUIERA", fuente("SemiBold Condensed", 30), ORO, "mm", 255 * a0, track=4)
        t_vacio = mk[n + 1]
        cols = 4
        for k, (ruta, nom) in enumerate(objetos):
            uk = _eo((dt - mk[k]) / .4)
            if dt >= t_vacio:
                uk *= 1 - _eo((dt - t_vacio - .22 * k) / .35)
            if uk <= 0:
                continue
            c, f = k % cols, k // cols
            xk, yk = cx0 + 40 + c * 195, cy0 + 70 + f * 128
            _pega(im, _icono(ruta, 112, 96), xk, yk - 20 * (1 - uk), uk)
            _texto(d, (xk + 56, yk + 112), nom.upper(), fuente("Condensed", 22), HUESO, "mm", 255 * uk, track=1)
        if dt >= t_vacio + .22 * n + .2:
            s = _pop(dt - (t_vacio + .22 * n + .2), .35)
            _texto(d, (cx0 + cw / 2, cy0 + ch / 2 + 20), "VACÍO", fuente("Bold Condensed", max(8, int(110 * s))), SANGRE, "mm",
                   track=12)
        # calendario de días
        yc = cy0 + ch + 40
        cwd = (cw - (dias - 1) * 10) / dias
        uc = 0.0 if dt < mk[n] else min(1.0, (dt - mk[n]) / max(.6, t_vacio - mk[n] if t_vacio < 99 else 3.0))
        for k in range(dias):
            xk = cx0 + k * (cwd + 10)
            d.rounded_rectangle((xk, yc, xk + cwd, yc + 70), radius=8, fill=(30, 28, 24, int(220 * a0)),
                                outline=HUESO + (int(140 * a0),), width=2)
            _texto(d, (xk + cwd / 2, yc + 35), str(k + 1), fuente("SemiBold Condensed", 32), GRIS, "mm", 255 * a0)
            if dt >= mk[n] and uc * dias >= k + 1:
                d.line([(xk + 10, yc + 10), (xk + cwd - 10, yc + 60)], fill=SANGRE + (255,), width=6)
                d.line([(xk + cwd - 10, yc + 10), (xk + 10, yc + 60)], fill=SANGRE + (255,), width=6)
        _texto(d, (cx0 + cw / 2, yc + 104), f"{dias} DÍAS Y SE REINICIA", fuente("SemiBold Condensed", 30), HUESO, "mm",
               255 * _eo((dt - mk[n]) / .4), track=3)
        if seguro:
            us = _eo((dt - mk[seguro[2]]) / .45)
            sx0, sw, sh = cx0 + cw + 90, ancho - cw - 230, 300
            if us < 1:                                          # la casa, apagada, hasta que la voz la nombra
                _pega(im, _retrato(seguro[0], int(sw), sh, gris=1.0), sx0, cy0, a0 * .55 * (1 - us))
                _texto(d, (sx0 + sw / 2, cy0 + sh / 2), "?", fuente("Bold Condensed", 120), HUESO, "mm", 200 * a0 * (1 - us))
            if us > 0:
                _pega(im, _retrato(seguro[0], int(sw), sh), sx0, cy0 + 20 * (1 - us), us)
                _marco(d, sx0, cy0 + 20 * (1 - us), sw, sh, VERDE, 255 * us, 3)
                _texto(d, (sx0 + sw / 2, cy0 + sh + 50), seguro[1].upper(), fuente("SemiBold Condensed", 32), HUESO, "mm",
                       255 * us, track=3)
                s = _pop(dt - mk[seguro[2]] - .3, .35)
                _texto(d, (sx0 + sw / 2, cy0 + sh + 110), "SEGURO", fuente("Bold Condensed", max(8, int(70 * s))), VERDE, "mm",
                       track=8)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ tes_misiones_imperdibles (28-oct-2026)
def _monedas(d, cx, base, n, a, r=34):
    """Pila de n monedas de oro (elipses apiladas) con la base en `base`."""
    for k in range(n):
        y = base - k * 13
        d.ellipse((cx - r, y - 11, cx + r, y + 11), fill=(150, 116, 46, int(a)), outline=(90, 66, 22, int(a)), width=2)
        d.ellipse((cx - r + 5, y - 9, cx + r - 5, y + 5), fill=ORO + (int(a),))


def inversion(titulo, socio, pagos, nota=None, despierta=None, remate=None, ancho=1700):
    """Lo que le vas pagando a alguien. socio = (ruta, nombre) en medallón a la izquierda · pagos = [(monto, motivo)]: la pila
    i de monedas crece en la marca i con su cifra y su motivo; «INVERTIDO» suma · nota = (texto, i_marca): la carta del
    final cae al centro como sello · despierta = (ruta, nombre, i_marca): a la derecha, el que despierta (gris → rojo, con
    «DESPIERTA») · remate = (texto, i). Primer uso: Ralis Sedarys y Ahzidal (1 000 + 2 000 + 3 000 + 5 000)."""
    n = len(pagos)
    h = 110 + 430 + (70 if remate else 10)
    D = 200
    tope = max(m for m, _ in pagos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 6)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        cx, cy = M + 60 + D / 2, M + 150 + D / 2
        _pega(im, _redondo(socio[0], D), cx - D / 2, cy - D / 2, a0)
        d.ellipse((cx - D / 2 - 4, cy - D / 2 - 4, cx + D / 2 + 4, cy + D / 2 + 4), outline=HUESO + (int(255 * a0),), width=3)
        _texto(d, (cx, cy + D / 2 + 36), socio[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * a0, track=3)
        x0, x1 = M + 360, M + (ancho - 330 if despierta else ancho - 80)
        base = M + 420
        d.line([(x0 - 20, base + 16), (x1 + 20, base + 16)], fill=(70, 66, 60, int(255 * a0)), width=4)
        total = 0.0
        for i, (monto, motivo) in enumerate(pagos):
            u = _eo((dt - mk[i]) / .7)
            if u <= 0:
                continue
            xc = x0 + (x1 - x0) * (i + .5) / n
            nmon = max(1, int(round(16 * monto / tope * u)))
            _monedas(d, xc, base, nmon, 255)
            ytop = base - (nmon - 1) * 13 - 40
            _texto(d, (xc, ytop - 18), _num(monto * u), fuente("Bold Condensed", 46), ORO, "mm", 255)
            for k, ln in enumerate(_partir(d, motivo.upper(), fuente("Condensed", 24), (x1 - x0) / n - 20)[:2]):
                _texto(d, (xc, base + 48 + 28 * k), ln, fuente("Condensed", 24), HUESO, "mm", 255 * u, track=1)
            total += monto * u
        _texto(d, (M + 110, M + 118), "INVERTIDO", fuente("Condensed", 26), GRIS, "lm", 255 * a0, track=4)
        _texto(d, (M + 110 + 150, M + 118), _num(total), fuente("Bold Condensed", 48), ORO, "lm", 255 * a0)
        if despierta:
            us = _eo((dt - mk[despierta[2]]) / .5)
            dx, dy = M + ancho - 60 - D / 2, M + 150 + D / 2
            _pega(im, _redondo(despierta[0], D), dx - D / 2, dy - D / 2 + 30 * (1 - us), .35 * a0 + .65 * us)
            col = tuple(int(GRIS[j] + (SANGRE[j] - GRIS[j]) * us) for j in range(3))
            d.ellipse((dx - D / 2 - 4, dy - D / 2 - 4, dx + D / 2 + 4, dy + D / 2 + 4), outline=col + (int(255 * a0),),
                      width=3 + int(4 * us))
            if us <= 0:
                _texto(d, (dx, dy), "?", fuente("Bold Condensed", 110), HUESO, "mm", 210 * a0)
            else:
                _texto(d, (dx, dy + D / 2 + 36), despierta[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * us,
                       track=3)
                s = _pop(dt - mk[despierta[2]] - .3, .35)
                _texto(d, (dx, dy - D / 2 - 30), "DESPIERTA", fuente("Bold Condensed", max(8, int(46 * s))), SANGRE, "mm", track=5)
        if nota and dt >= mk[nota[1]]:
            _sello(im, (x0 + x1) / 2, M + 200, "« " + nota[0].upper() + " »", min(1.0, (dt - mk[nota[1]]) / .6), color=HUESO,
                   giro=-6, tam=50)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def versiones(titulo, izq, der, veredicto=None, remate=None, ancho=1760, pie="PRUEBAS: 0"):
    """Dos versiones de la misma historia, enfrentadas. izq/der = (ruta, nombre, [líneas], i_marca): la tarjeta entra en su marca
    y sus líneas aparecen una tras otra (0,7 s); debajo, «PRUEBAS: 0» · veredicto = (texto, i_marca): sello rojo cruzado sobre
    las dos (p. ej. «SIN PRUEBAS») · remate = (texto, i) · pie = línea bajo cada tarjeta (None = sin ella).
    Primer uso: Saadia contra los alik'r (ninguna versión se demuestra)."""
    RW, RH = 250, 310
    h = 110 + 520 + (70 if remate else 10)
    HUECO = 130                                                 # hueco central para el «VS» y el sello

    def lado(im, d, dt, mk, M, datos, x, w):
        ruta, nombre, lineas, i = datos
        u = _eo((dt - mk[i]) / .45)
        if u <= 0:
            return
        y = M + 120 + 20 * (1 - u)
        _pega(im, _retrato(ruta, RW, RH), x, y, u)
        _marco(d, x, y, RW, RH, HUESO, 200 * u, 2)
        _texto(d, (x + RW / 2, M + 120 + RH + 34), nombre.upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * u, track=3)
        tx, ty = x + RW + 30, M + 140
        f = fuente("SemiBold Condensed", 42)
        k = 0
        for j, ln in enumerate(lineas):
            ul = _eo((dt - mk[i] - .5 - .7 * j) / .4)
            for sub in _partir(d, "— " + ln, f, w - RW - 40):
                _texto(d, (tx, ty + 54 * k), sub, f, HUESO, "la", 255 * ul)
                k += 1
        if pie:
            _texto(d, (tx, M + 120 + RH - 10), pie, fuente("Bold Condensed", 40), SANGRE, "lm",
                   255 * _eo((dt - mk[i] - .6 - .7 * len(lineas)) / .4), track=3)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        xm = M + ancho / 2
        mitad = ancho / 2 - HUECO / 2 - 30
        lado(im, d, dt, mk, M, izq, M + 30, mitad)
        lado(im, d, dt, mk, M, der, xm + HUECO / 2, mitad)
        d.line([(xm, M + 130), (xm, M + 230)], fill=HUESO + (int(110 * a0),), width=2)
        d.line([(xm, M + 370), (xm, M + 470)], fill=HUESO + (int(110 * a0),), width=2)
        _texto(d, (xm, M + 300), "VS", fuente("Bold Condensed", 56), ORO, "mm", 255 * _eo((dt - mk[der[3]]) / .4))
        if veredicto and dt >= mk[veredicto[1]]:
            _sello(im, xm, M + 120 + RH + 110, veredicto[0].upper(), min(1.0, (dt - mk[veredicto[1]]) / .6), tam=64, giro=-5)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


_lb = {}


def _libre(ruta, w, h):
    """El objeto recortado por su contorno, sin fondo ni giro, cabiendo en w×h (amuletos, joyas)."""
    k = (ruta, w, h)
    if k not in _lb:
        im = Image.open(ruta).convert("RGBA")
        bb = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
        if bb:
            im = im.crop(bb)
        esc = min(w / im.width, h / im.height)
        _lb[k] = im.resize((max(2, int(im.width * esc)), max(2, int(im.height * esc))), Image.LANCZOS)
    return _lb[k]


def fragmentos(titulo, padre, objeto, hijos, bono=None, remate=None, ancho=1600):
    """Un objeto partido entre varios. padre = (ruta, nombre) en medallón arriba a la izquierda (apagado hasta la reunión) ·
    objeto = (ruta, nombre) arriba al centro · hijos = [(ruta, nombre, lugar)]: marca 0 = el objeto se parte y cada trozo vuela
    hacia su hijo; marcas 1..n = cada hijo aparece con su lugar · marca n+1 = los trozos vuelven y el objeto se recompone (el
    padre se enciende) · marca n+2 = los hijos se tachan y se apagan · bono = (texto, i_marca) en oro junto al objeto ·
    remate = (texto, i). Primer uso: el Amuleto de Gauldur y sus tres hijos."""
    n = len(hijos)
    RW, RH = 220, 250
    h = 110 + 260 + RH + 120 + (70 if remate else 10)
    D = 170

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 6)
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        t_par, t_jun, t_fin = mk[0], mk[n + 1], mk[n + 2]
        up = _eo((dt - t_jun) / .5)
        px, py = M + 70 + D / 2, M + 120 + D / 2
        _pega(im, _redondo(padre[0], D), px - D / 2, py - D / 2, a0 * (.4 + .6 * up))
        d.ellipse((px - D / 2 - 4, py - D / 2 - 4, px + D / 2 + 4, py + D / 2 + 4),
                  outline=(ORO if up > .5 else GRIS) + (int(255 * a0),), width=3 + int(3 * up))
        _texto(d, (px, py + D / 2 + 32), padre[1].upper(), fuente("SemiBold Condensed", 28), HUESO, "mm", 255 * a0, track=3)
        ox, oy, ow = M + ancho / 2, M + 220, 210
        ico = _libre(objeto[0], ow, ow)
        ys = M + 110 + 260 + 30
        xs = [M + ancho / 2 + (k - (n - 1) / 2) * (RW + 150) for k in range(n)]
        if dt < t_par:
            _pega(im, ico, ox - ow / 2, oy - ow / 2, a0)
        elif dt < t_jun:
            for k in range(n):
                u = _eo((dt - t_par - .15 * k) / .9)
                tx = ox + (xs[k] + RW / 2 + 40 - ox) * u
                ty = oy + (ys + 30 - oy) * u
                tr = _libre(objeto[0], 110, 110).rotate(25 * (k - 1) * u, resample=Image.BICUBIC, expand=True)
                _pega(im, tr, tx - tr.width / 2, ty - tr.height / 2, 1)
        else:
            uj = _eo((dt - t_jun) / .8)
            if uj < 1:
                for k in range(n):
                    tx = xs[k] + RW / 2 + 40 + (ox - xs[k] - RW / 2 - 40) * uj
                    ty = ys + 30 + (oy - ys - 30) * uj
                    _pega(im, _libre(objeto[0], 110, 110), tx - 55, ty - 55, 1)
            else:
                s = _pop(dt - t_jun - .8, .4)
                big = ico.resize((max(2, int(ow * s)), max(2, int(ow * s))), Image.BILINEAR)
                _pega(im, big, ox - big.width / 2, oy - big.height / 2, 1)
        _texto(d, (ox, oy + ow / 2 + 26), objeto[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * a0, track=3)
        if bono and dt >= mk[bono[1]]:
            s = _pop(dt - mk[bono[1]], .35)
            for k, ln in enumerate(bono[0].upper().split(" · ")):
                _texto(d, (ox + 400, oy - 50 + 52 * k), ln, fuente("Bold Condensed", max(8, int(44 * s))), ORO, "mm", track=2)
        for k, (ruta, nom, lugar) in enumerate(hijos):
            u = _eo((dt - mk[k + 1]) / .45)
            if u <= 0:
                d.rounded_rectangle((xs[k] - RW / 2, ys, xs[k] + RW / 2, ys + RH), radius=14, outline=GRIS + (int(140 * a0),),
                                    width=2)
                _texto(d, (xs[k], ys + RH / 2), "?", fuente("Bold Condensed", 90), GRIS, "mm", 180 * a0)
                continue
            apaga = _eo((dt - t_fin - .25 * k) / .4) if dt >= t_fin else 0
            _pega(im, _retrato(ruta, RW, RH, gris=apaga), xs[k] - RW / 2, ys + 20 * (1 - u), u)
            _marco(d, xs[k] - RW / 2, ys + 20 * (1 - u), RW, RH, HUESO, 200 * u, 2)
            _texto(d, (xs[k], ys + RH + 30), nom.upper(), fuente("SemiBold Condensed", 28), HUESO, "mm", 255 * u, track=2)
            _texto(d, (xs[k], ys + RH + 64), lugar.upper(), fuente("Condensed", 24), GRIS, "mm", 255 * u, track=2)
            if apaga > 0:
                _tacha(d, xs[k] - RW / 2, ys, RW, RH, apaga)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def nombre(titulo, retrato, partes, remate=None, ancho=1560):
    """Un nombre que se parte y confiesa lo que significa. partes = [(trozo, significado, i_marca)]: el nombre entra junto, se
    separa en su primera marca y bajo cada trozo cae su significado; el último, en rojo. Primer uso: Paar-Thur-Nax."""
    RW, RH = 280, 360
    h = 110 + 420 + (80 if remate else 20)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        _pega(im, _retrato(retrato, RW, RH), M + 40, M + 125, a0)
        _marco(d, M + 40, M + 125, RW, RH, HUESO, 200 * a0, 2)
        x0, w = M + 370, ancho - 410
        n = len(partes)
        f = fuente("Bold Condensed", 112)
        f2 = fuente("SemiBold Condensed", 46)
        anchos = [d.textlength(p[0].upper(), font=f) for p in partes]
        xj = x0 + w / 2 - sum(anchos) / 2
        s = _eo((dt - mk[partes[0][2]]) / .8)
        for i, (trozo, sig, k) in enumerate(partes):
            junto = xj + sum(anchos[:i]) + anchos[i] / 2
            x = junto + (x0 + w * (i + .5) / n - junto) * s
            u = _eo((dt - mk[k] - .35) / .45)
            color = SANGRE if i == n - 1 and u > 0 else HUESO
            _texto(d, (x, M + 215), trozo.upper(), f, color, "mm", 255 * a0)
            if u > 0:
                d.line([(x, M + 285), (x, M + 285 + 46 * u)], fill=ORO + (int(210 * u),), width=2)
                for j, sub in enumerate(_partir(d, sig, f2, w / n - 16)):
                    _texto(d, (x, M + 372 + 54 * j), sub, f2, color, "mm", 255 * u)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def cordura(titulo, retrato, paginas, final=None, ancho=1600):
    """Un diario que se desquicia. paginas = [(línea, i_marca)]: cada línea entra más roja y tiembla más que la anterior, y la
    barra de cordura baja a la vez (sin cifras) · final = (texto, i): sello rojo que la deja a cero. Primer uso: Cicerón."""
    RW, RH = 260, 330
    n = len(paginas)
    h = max(110 + 92 * n + 110, 110 + RH + 200)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        _pega(im, _retrato(retrato, RW, RH), M + 40, M + 120, a0)
        _marco(d, M + 40, M + 120, RW, RH, HUESO, 200 * a0, 2)
        hecho = sum(_eo((dt - mk[k]) / .6) for _, k in paginas) / (n + 1)
        if final:
            hecho += _eo((dt - mk[final[1]]) / .6) / (n + 1)
        by = M + 120 + RH + 56
        _texto(d, (M + 40, by - 24), "CORDURA", fuente("SemiBold Condensed", 28), HUESO, "lm", 230 * a0, track=4)
        d.rectangle([M + 40, by, M + 40 + RW, by + 22], outline=HUESO + (int(170 * a0),), width=2)
        rest = max(0.0, 1 - hecho)
        if rest > 0:
            d.rectangle([M + 43, by + 3, M + 43 + (RW - 6) * rest, by + 19], fill=(SANGRE if rest < .4 else ORO) + (int(240 * a0),))
        f = fuente("SemiBold Condensed", 46)
        for j, (ln, k) in enumerate(paginas):
            u = _eo((dt - mk[k]) / .45)
            if u <= 0:
                continue
            nv = j / max(1, n - 1)
            color = tuple(int(a + (b - a) * nv) for a, b in zip(HUESO, SANGRE))
            am = 9 * nv ** 2
            x = M + 350 + am * math.sin(dt * 23 + j * 2.1)
            y = M + 150 + 92 * j + am * .5 * math.sin(dt * 31 + j)
            if nv > .55:
                _texto(d, (x + 5 * nv, y + 3), ln, f, SANGRE, "lm", 90 * u)
            _texto(d, (x, y), ln, f, color, "lm", 255 * u)
        if final and dt >= mk[final[1]]:
            _sello(im, M + ancho * .62, M + h - 44, final[0].upper(), min(1.0, (dt - mk[final[1]]) / .6), tam=50, giro=-3)
        return _salida(im, dt)
    return fn


def informe(titulo, sujeto, campos, sello=None, remate=None, ancho=1560):
    """Expediente clasificado: cada dato empieza tachado con una barra negra que se retira en su marca. sujeto = (ruta, nombre) ·
    campos = [(etiqueta, valor, i_marca)] · sello = (texto, i). Primer uso: los informes thalmor de Ulfric y Esbern."""
    RW, RH = 280, 350
    n = len(campos)
    h = max(110 + 112 * n + 40, 110 + RH + 90) + (70 if remate else 10)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        _pega(im, _retrato(sujeto[0], RW, RH), M + 40, M + 120, a0)
        _marco(d, M + 40, M + 120, RW, RH, HUESO, 200 * a0, 2)
        _texto(d, (M + 40 + RW / 2, M + 120 + RH + 32), sujeto[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * a0, track=3)
        fe, fv = fuente("SemiBold Condensed", 28), fuente("SemiBold Condensed", 42)
        x, w = M + 360, ancho - 410
        for j, (et, val, k) in enumerate(campos):
            y = M + 130 + 112 * j
            _texto(d, (x, y), et.upper(), fe, ORO, "la", 235 * a0, track=4)
            lineas = _partir(d, val, fv, w)[:2]
            for q, ln in enumerate(lineas):
                _texto(d, (x, y + 34 + 46 * q), ln, fv, HUESO, "la", 255 * a0)
            u = _eo((dt - mk[k]) / .5)
            if u < 1:
                x1 = x + w
                d.rectangle([x + (w + 8) * u - 4, y + 38, x1 + 4, y + 36 + 46 * len(lineas)], fill=(9, 8, 8, int(250 * a0)))
        if sello and dt >= mk[sello[1]]:
            _sello(im, M + ancho * .66, h - (150 if remate else 90), sello[0].upper(), min(1.0, (dt - mk[sello[1]]) / .6), tam=62, giro=-7)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def aguante(titulo, comida, minutos, remate=None, ancho=1500):
    """La barra de aguante vacía que nunca llega a cero: late al mínimo, cada ataque poderoso la vacía y la comida la devuelve,
    mientras corre la cuenta atrás. comida = (ruta, nombre) · remate = (texto, i). Primer uso: la sopa de verduras."""
    h = 110 + 330 + (80 if remate else 20)
    VERDE = (86, 170, 104)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo(dt / .4)
        ic = _libre(comida[0], 250, 230)
        _pega(im, ic, M + 50 + (250 - ic.width) / 2, M + 125, a0)
        _texto(d, (M + 175, M + 385), comida[1].upper(), fuente("SemiBold Condensed", 30), HUESO, "mm", 255 * a0, track=3)
        x, y, w = M + 370, M + 215, ancho - 440
        t0 = mk[0]
        ciclo = ((dt - t0) % 1.3) / 1.3 if dt >= t0 else 1.0
        nivel = .012 + .05 * min(1.0, ciclo / .8)
        _texto(d, (x, y - 34), "AGUANTE", fuente("SemiBold Condensed", 32), HUESO, "lm", 240 * a0, track=5)
        d.rectangle([x, y, x + w, y + 34], outline=HUESO + (int(190 * a0),), width=2)
        d.rectangle([x + 3, y + 3, x + 3 + (w - 6) * nivel, y + 31], fill=VERDE + (int(255 * a0),))
        if dt >= t0 and ciclo < .34:
            _texto(d, (x + w / 2, y + 86), "ATAQUE PODEROSO", fuente("Bold Condensed", 66), SANGRE, "mm",
                   255 * (1 - ciclo / .34), track=4)
        fr = max(0.0, 1 - max(0.0, dt - t0) / max(.1, dur - t0 - .6))
        seg = int(round(minutos * 60 * fr))
        _texto(d, (x + w, y - 40), f"{seg // 60:02d}:{seg % 60:02d}", fuente("Bold Condensed", 62), ORO, "rm", 255 * a0, track=2)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


# ======================================================================= MG nuevos de `tes_secretos_40` rehecho (30-oct-2026)
def barra_vida(titulo, seguro, peligro, ancho=1400):
    """Dos barras de salud que se acaban: la que el juego protege y la que no. seguro/peligro = (nombre, texto final).
    marca 0: el efecto seguro se apaga y deja un punto · marca 1: entra la bendición · marca 2: se apaga y la barra llega a cero."""
    h = 110 + 390

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x, w = M + 90, ancho - 180
        for k, (nombre, final) in enumerate((seguro, peligro)):
            y = M + 170 + k * 170
            t0 = mk[0] if k == 0 else mk[2]
            a = _eo(dt / .4) if k == 0 else _eo((dt - mk[1]) / .35)
            if a <= .01:
                continue
            u = _eo((dt - t0) / .9)
            nivel = (.26 + (.008 - .26) * u) if k == 0 else (.2 * (1 - u))
            _texto(d, (x, y - 34), nombre.upper(), fuente("SemiBold Condensed", 36), HUESO, "lm", 245 * a, track=4)
            d.rectangle([x, y, x + w, y + 40], outline=HUESO + (int(190 * a),), width=2)
            if nivel > .001:
                d.rectangle([x + 3, y + 3, x + 3 + (w - 6) * nivel, y + 37], fill=(176, 36, 30, int(255 * a)))
            if u > .75:
                c = ORO if k == 0 else SANGRE
                _texto(d, (x + w, y - 34), final.upper(), fuente("Bold Condensed", 46), c, "rm", 255 * _eo((u - .75) / .25), track=3)
        return _salida(im, dt)
    return fn


def deteccion(titulo, retrato, vida, muerte, ancho=1320):
    """El mismo retrato visto con dos hechizos. vida/muerte = (nombre del hechizo, resultado). marca 0: Detectar vida no la ve
    (figura gris) · marca 1: Detectar muerte la ve (figura que arde en rojo)."""
    import peg_estilos as PE
    h = 110 + 560
    FW, FH = 330, 460
    fig = PE.recorte(retrato)
    fig = fig.crop((0, 0, fig.width, int(fig.height * .72)))
    k = min(FW / fig.width, FH / fig.height)
    fig = fig.resize((int(fig.width * k), int(fig.height * k)), Image.LANCZOS)
    L = fig.convert("L")
    gris = Image.merge("RGBA", (*Image.merge("RGB", (L, L, L)).point(lambda v: int(v * .55)).split(), fig.getchannel("A")))
    M0 = 40
    aura = Image.new("RGBA", (fig.width + 2 * M0, fig.height + 2 * M0), (0, 0, 0, 0))
    m = Image.new("L", aura.size, 0)
    m.paste(fig.getchannel("A"), (M0, M0))
    aura.paste(SANGRE + (255,), mask=m.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(18)))
    rojo = Image.merge("RGBA", (L.point(lambda v: min(255, int(v * 1.5) + 60)), L.point(lambda v: int(v * .4)), L.point(lambda v: int(v * .35)),
                                fig.getchannel("A")))

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        for j, (cx, (hechizo, res)) in enumerate(((M + ancho * .27, vida), (M + ancho * .73, muerte))):
            a = _eo((dt - mk[j]) / .4)
            if a <= .01:
                continue
            x, y = int(cx - fig.width / 2), M + 120
            if j == 1:
                lat = .72 + .28 * math.sin(dt * 5)
                _pega(im, aura, x - M0, y - M0, a * lat)
                _pega(im, rojo, x, y, a)
            else:
                _pega(im, gris, x, y, a * .8)
            d = ImageDraw.Draw(im)
            _texto(d, (cx, M + 610), hechizo.upper(), fuente("Condensed", 34), HUESO, "mm", 240 * a, track=3)
            _texto(d, (cx, M + 652), res.upper(), fuente("Bold Condensed", 42), SANGRE if j else GRIS, "mm", 255 * a, track=3)
        return _salida(im, dt)
    return fn


def semana(titulo, ideas, tachada=None, ancho=1640):
    """Siete días de plazo y lo que salió de ellos. ideas = [(texto, ruta|None, i_marca)] · tachada = (texto, i_marca): lo que se
    quedó fuera. Primer uso: la semana libre de Bethesda."""
    cols = 3
    CW, CH = 480, 214
    filas_ = math.ceil((len(ideas) + (1 if tachada else 0)) / cols)
    h = 110 + 74 + filas_ * (CH + 18) + 20

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        u = _eo(dt / 1.0)
        for k in range(7):                                    # los siete días se llenan de corrido
            x = M + ancho / 2 + (k - 3) * 92
            on = u * 7 > k
            d.rounded_rectangle((x - 36, M + 112, x + 36, M + 166), 8, outline=HUESO + (190,), width=2, fill=(ORO + (60,)) if on else None)
            _texto(d, (x, M + 139), "LMXJVSD"[k], fuente("SemiBold Condensed", 30), HUESO, "mm", 240)
        todo = list(ideas) + ([(tachada[0], None, tachada[1])] if tachada else [])
        for k, (texto, ruta, i) in enumerate(todo):
            a = _eo((dt - mk[i]) / .35)
            if a <= .01:
                continue
            x = M + (ancho - cols * CW - (cols - 1) * 18) / 2 + k % cols * (CW + 18)
            y = M + 184 + k // cols * (CH + 18)
            d.rounded_rectangle((x, y, x + CW, y + CH), 14, fill=(14, 13, 12, int(190 * a)), outline=HUESO + (int(120 * a),), width=2)
            if ruta:
                ic = _libre(ruta, 190, 180)
                _pega(im, ic, x + 12 + (190 - ic.width) / 2, y + (CH - ic.height) / 2, a)
                d = ImageDraw.Draw(im)
            tx = x + (214 if ruta else 20)
            lin = _partir(d, texto.upper(), fuente("Bold Condensed", 40), CW - (tx - x) - 16)
            for j, ln in enumerate(lin):
                _texto(d, (tx, y + CH / 2 + (j - (len(lin) - 1) / 2) * 46), ln, fuente("Bold Condensed", 40), HUESO, "lm", 255 * a, track=1)
            if tachada and k == len(todo) - 1:
                _tacha(d, x + 10, y + 10, CW - 20, CH - 20, _eo((dt - mk[i] - .3) / .35))
        return _salida(im, dt)
    return fn


def estrellas(titulo, constelaciones, ancho=1400):
    """Cielo nocturno que se dibuja solo. constelaciones = [(nombre, [(x, y)...] en 0..1, [(a, b)...] líneas, i_marca)]."""
    import random
    h = 110 + 560
    rnd = random.Random(21)
    polvo = [(rnd.random(), rnd.random(), rnd.uniform(1, 2.6), rnd.uniform(0, 6.28)) for _ in range(170)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        X, Y, W, H = M + 60, M + 112, ancho - 120, 530
        a0 = _eo(dt / .5)
        for x, y, r, f in polvo:
            br = int((110 + 90 * math.sin(dt * 2 + f)) * a0)
            px, py = X + x * W, Y + y * H
            d.ellipse((px - r, py - r, px + r, py + r), fill=(205, 212, 232, max(0, br)))
        for nombre, pts, lineas, i in constelaciones:
            u = _eo((dt - mk[i]) / .9)
            if u <= .01:
                continue
            P = [(X + a * W, Y + b * H) for a, b in pts]
            for k, (a, b) in enumerate(lineas):
                v = min(1.0, max(0.0, u * len(lineas) - k))
                if v > 0:
                    d.line((P[a], (P[a][0] + (P[b][0] - P[a][0]) * v, P[a][1] + (P[b][1] - P[a][1]) * v)), fill=ORO + (235,), width=3)
            for px, py in P:
                d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=BLANCO + (int(255 * u),))
            cx = sum(p[0] for p in P) / len(P)
            _texto(d, (cx, max(p[1] for p in P) + 42), nombre.upper(), fuente("Bold Condensed", 46), HUESO, "mm", 255 * u, track=4)
        return _salida(im, dt)
    return fn


def soldados(titulo, n, remate=None, cols=20, ancho=1400):
    """n siluetas en formación. marca 0: aparecen · marca 1: caen en ola y se apagan en rojo. Primer uso: el pozo de Forel."""
    T = 56
    filas_ = math.ceil(n / cols)
    h = 110 + filas_ * (T + 18) + (100 if remate else 30)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0 = M + (ancho - cols * (T + 6)) / 2
        for k in range(n):
            a = _eo((dt - mk[0] - k * .012) / .25)
            if a <= .01:
                continue
            c = k % cols
            u = _eo((dt - mk[1] - k * .035) / .35)
            col = tuple(int(HUESO[j] + (SANGRE[j] - HUESO[j]) * u) for j in range(3))
            _silueta(d, x0 + c * (T + 6), M + 112 + k // cols * (T + 18) + u * 12, T, col, (245 - 150 * u) * a)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def cronologia(titulo, hitos, ancho=1500):
    """Línea de tiempo sobria. hitos = [(fecha, texto, i_marca)]; el último queda dorado. Primer uso: Erik West (sin sarcasmo)."""
    h = 110 + 300

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, x1, y = M + 130, M + ancho - 130, M + 240
        paso = (x1 - x0) / max(1, len(hitos) - 1)
        u = _eo(dt / .5)
        d.line((x0, y, x0 + (x1 - x0) * u, y), fill=HUESO + (170,), width=3)
        for k, (fecha, texto, i) in enumerate(hitos):
            a = _eo((dt - mk[i]) / .4)
            if a <= .01:
                continue
            x = x0 + k * paso
            ult = k == len(hitos) - 1
            d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=(ORO if ult else HUESO) + (int(255 * a),))
            _texto(d, (x, y - 60), fecha, fuente("Bold Condensed", 58), ORO if ult else HUESO, "mm", 255 * a, track=2)
            for j, ln in enumerate(_partir(d, texto, fuente("Condensed", 34), paso - 24)):
                _texto(d, (x, y + 50 + j * 40), ln, fuente("Condensed", 34), HUESO, "mm", 240 * a)
        return _salida(im, dt)
    return fn


def vela(titulo, antes, despues, ancho=1000):
    """Figura encapuchada a oscuras. marca 0: una vela se acerca y la luz le destapa la cara · marca 1: ojos rojos, colmillos y
    el rótulo cambia de `antes` a `despues` con sello. Primer uso: el sacerdote de «Sangre inmortal»."""
    h = 110 + 500
    C = 900
    yy, xx = np.mgrid[0:C, 0:C]
    g = np.clip(1 - np.hypot(xx - C / 2, yy - C / 2) / (C / 2), 0, 1) ** 1.8
    luz = np.zeros((C, C, 4), np.uint8)
    luz[..., :3] = (255, 176, 92)
    luz[..., 3] = (g * 200).astype(np.uint8)
    luz = Image.fromarray(luz, "RGBA")

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _humo(ancho, h, titulo)
        cx, cy = M + ancho / 2, M + 300
        u = _eo((dt - mk[0]) / 1.3)
        v = _eo((dt - mk[1]) / .22)
        vx, vy = cx + 300 - 195 * u, cy + 170 - 120 * u + 5 * math.sin(dt * 2.2)
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        k = .14 + .86 * u                                     # cuánta luz recibe la figura
        tela = tuple(int(c * k) for c in (64, 50, 44))
        d.polygon([(cx - 230, M + 590), (cx - 150, cy + 30), (cx - 104, cy - 120), (cx, cy - 190), (cx + 104, cy - 120),
                   (cx + 150, cy + 30), (cx + 230, M + 590)], fill=tela + (255,))
        d.ellipse((cx - 112, cy - 150, cx + 112, cy + 90), fill=tuple(int(c * k * .45) for c in (64, 50, 44)) + (255,))
        piel = tuple(int(c * k) for c in (176, 136, 112))
        d.ellipse((cx - 72, cy - 112, cx + 72, cy + 72), fill=piel + (255,))
        d.ellipse((cx - 44, cy - 28, cx - 12, cy - 12), fill=(20, 14, 12, 255))
        d.ellipse((cx + 12, cy - 28, cx + 44, cy - 12), fill=(20, 14, 12, 255))
        d.line((cx - 26, cy + 34, cx + 26, cy + 34), fill=(32, 20, 18, 255), width=4)
        if v > 0:
            for s in (-1, 1):
                ex = cx + s * 28
                d.ellipse((ex - 12, cy - 28, ex + 12, cy - 12), fill=(236, 34, 24, int(255 * v)))
                d.polygon([(cx + s * 8, cy + 36), (cx + s * 20, cy + 36), (cx + s * 14, cy + 36 + 26 * v)], fill=BLANCO + (255,))
        for x0, x1 in ((vx - 13, vx + 13),):                  # la vela
            d.rectangle((x0, vy, x1, vy + 170), fill=(226, 214, 186, 255))
            d.polygon([(vx, vy - 54 - 7 * math.sin(dt * 9)), (vx - 13, vy - 12), (vx + 13, vy - 12)], fill=(255, 208, 110, 255))
        im.alpha_composite(capa)
        r = int(340 + 150 * u + 10 * math.sin(dt * 7))
        hal = luz.resize((r * 2, r * 2), Image.BILINEAR)
        ax, ay = int(vx - r), int(vy - 30 - r)
        sx, sy = max(0, -ax), max(0, -ay)
        ex, ey = min(hal.width, sx + im.width - max(0, ax)), min(hal.height, sy + im.height - max(0, ay))
        hal = hal.crop((sx, sy, ex, ey))
        a = np.array(hal)
        a[..., 3] = (a[..., 3] * .42 * np.array(im)[max(0, ay):max(0, ay) + a.shape[0], max(0, ax):max(0, ax) + a.shape[1], 3].astype(np.float32) / 255).astype(np.uint8)
        im.alpha_composite(Image.fromarray(a, "RGBA"), (max(0, ax), max(0, ay)))
        d = ImageDraw.Draw(im)
        _texto(d, (cx - 250, M + 530), (despues if v > .5 else antes).upper(), fuente("Bold Condensed", 58), SANGRE if v > .5 else HUESO, "mm", 255, track=4)
        if v > 0:
            _sello(im, cx + 250, M + 220, "VAMPIRO", v)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ tes_sentinel_teaser (3-nov-2026)
def cifrado(titulo, pares, palabra, remate=None, ancho=1640):
    """Número que se descifra. pares = ["19", "05", ...]; palabra = letras resultantes (mismo largo). marca 0: los pares entran en
    fila · entre las marcas 1 y 2 cada par gira y deja su letra debajo · marca 3: la palabra queda en oro. Primer uso: el número
    de empleado de Starfield (19 05 14 20 09 14 05 12 = SENTINEL)."""
    n = len(pares)
    h = 110 + 330 + (80 if remate else 20)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        paso = (ancho - 160) / n
        fn_, fl = fuente("Bold Condensed", 74), fuente("Bold Condensed", 110)
        oro = dt >= mk[3]
        for k, (p, l) in enumerate(zip(pares, palabra)):
            x = M + 80 + paso * (k + .5)
            a = _eo((dt - mk[0] - k * .12) / .3)
            if a <= .01:
                continue
            t_l = mk[1] + (mk[2] - mk[1]) * k / max(1, n)
            u = _eo((dt - t_l) / .35)
            _texto(d, (x, M + 175), p, fn_, GRIS if u > .5 else HUESO, "mm", 255 * a)
            if u > .01:
                d.line((x - 18, M + 230, x + 18, M + 230), fill=HUESO + (int(150 * u),), width=2)
                _texto(d, (x, M + 312 - 20 * (1 - u)), l, fl, ORO if oro else BLANCO, "mm", 255 * u)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def ceguera(titulo, retrato, lecturas_, remate=None, ancho=1300):
    """La vista de un Sacerdote de la Polilla: retrato que se va apagando y un ojo que se cierra. lecturas_ = [(texto, i_marca)]:
    cada lectura aparece en su marca y quita un tramo de la barra «VISTA» (la última la deja a cero y el retrato en negro)."""
    RW, RH = 300, 380
    n = len(lecturas_)
    h = 110 + 440 + (80 if remate else 20)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        hechas = sum(1 for _, i in lecturas_ if dt >= mk[i])
        u_ult = max([_eo((dt - mk[i]) / .6) for _, i in lecturas_ if dt >= mk[i]] or [0])
        vista = max(0.0, 1 - (hechas - 1 + u_ult) / n) if hechas else 1.0
        r = _retrato(retrato, RW, RH, gris=1 - vista)
        a = np.array(r).astype(np.float32)
        a[..., :3] *= .25 + .75 * vista
        im.alpha_composite(Image.fromarray(a.astype(np.uint8)), (M + 50, M + 120))
        cx, cy = M + 50 + RW // 2, M + 120 + RH + 0
        x0 = M + 420
        _texto(d, (x0, M + 150), "VISTA", fuente("SemiBold Condensed", 38), HUESO, "lm", track=4)
        bw = ancho - 520
        d.rectangle((x0, M + 185, x0 + bw, M + 215), outline=HUESO + (160,), width=2)
        d.rectangle((x0 + 3, M + 188, x0 + 3 + int((bw - 6) * vista), M + 212), fill=(SANGRE if vista < .34 else HUESO) + (230,))
        for k, (txt, i) in enumerate(lecturas_):
            al = _eo((dt - mk[i]) / .35)
            if al > .01:
                _texto(d, (x0, M + 270 + k * 64), f"{k + 1}.  {txt}", fuente("Condensed", 40), SANGRE if k == n - 1 else HUESO, "lm", 255 * al)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


def lecturas(titulo, cita, opciones, ancho=1760):
    """La misma frase leída de varias maneras. cita = [líneas] (entra en la marca 0) · opciones = [(nombre, texto, i_marca)]:
    cada lectura entra en su marca y queda encendida mientras las anteriores se apagan a gris."""
    n = len(opciones)
    h = 110 + 70 * len(cita) + 330

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        a0 = _eo((dt - mk[0]) / .5)
        for j, ln in enumerate(cita):
            _texto(d, (M + ancho / 2, M + 140 + j * 64), ln, fuente("Light Condensed", 52), HUESO, "mm", 255 * a0)
        y = M + 140 + 64 * len(cita) + 30
        separador(d, M + ancho / 2, y, ancho * .4, 255 * a0)
        col = (ancho - 120) / n
        activa = max([k for k, (_, _, i) in enumerate(opciones) if dt >= mk[i]] or [-1])
        for k, (nom, txt, i) in enumerate(opciones):
            al = _eo((dt - mk[i]) / .4)
            if al <= .01:
                continue
            x = M + 60 + col * (k + .5)
            c = (SANGRE if k == n - 1 else ORO) if k == activa else GRIS
            _texto(d, (x, y + 60), nom.upper(), fuente("Bold Condensed", 50), c, "mm", 255 * al, track=3)
            for j, ln in enumerate(_partir(d, txt, fuente("Condensed", 36), col - 50)):
                _texto(d, (x, y + 120 + j * 42), ln, fuente("Condensed", 36), HUESO if k == activa else GRIS, "mm", 255 * al)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ varias voces (tes_sentinel_teaser, 3-nov-2026)
def narrador(nombre, lema, n=None, de=None, ancho=600):
    """Placa pequeña de quién narra (videos con varias voces que compiten): «NARRA · VOZ 3 DE 7» chico y gris, el nombre grande que
    entra cerrando el espaciado y un lema en gris debajo. Panel de humo; va abajo a la izquierda para no tapar el clip."""
    h = 200

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h)
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        arriba = "NARRA" + (f"  ·  VOZ {n} DE {de}" if n else "")
        _texto(d, (cx, M + 42), arriba, fuente("Condensed", 28), GRIS, "mm", track=5)
        tr = 3 + 20 * (1 - _eo(dt / .8))
        _texto(d, (cx, M + 96), nombre.upper(), fuente("SemiBold Condensed", 62), ORO, "mm", track=tr)
        separador(d, cx, M + 136, ancho * .32)
        _texto(d, (cx, M + 166), lema, fuente("Condensed", 30), (205, 200, 190), "mm", 255 * _eo((dt - .4) / .5))
        return _salida(im, dt)
    return fn


def votacion(titulo, nombres, remate=None, ancho=1180):
    """Papeleta de la votación: los nombres en dos columnas con su casilla; la marca k enciende el nombre k (dorado, casilla
    marcada con un golpe) cuando esa voz pide el voto, en cualquier orden; los ya marcados quedan en hueso. Con `remate`, la marca
    len(nombres) lo saca."""
    filas = (len(nombres) + 1) // 2
    h = 150 + filas * 92 + (90 if remate else 30)

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        ms = list(marcas[:len(nombres)]) + [None] * max(0, len(nombres) - len(marcas))
        on_ = [m is not None and dt >= m for m in ms]
        activa = max((k for k in range(len(nombres)) if on_[k]), key=lambda k: ms[k], default=-1)
        f = fuente("SemiBold Condensed", 50)
        for k, nom in enumerate(nombres):
            col, fila = k // filas, k % filas
            x = M + (ancho * .14 if col == 0 else ancho * .58)
            y = M + 150 + fila * 92
            on = on_[k]
            c = ORO if k == activa else HUESO if on else GRIS
            d.rectangle((x, y - 22, x + 44, y + 22), outline=c + (255,), width=3)
            if on:
                u = _pop(dt - marcas[k], .35)
                r = 18 * u
                d.line([(x + 22 - r, y), (x + 22 - r * .3, y + r * .8), (x + 22 + r, y - r)], fill=c + (255,), width=6)
            _texto(d, (x + 70, y), nom.upper(), f, c, "lm", track=3)
        mr = marcas[len(nombres)] if remate and len(marcas) > len(nombres) else None
        if mr is not None and dt >= mr:
            _texto(d, (M + ancho / 2, M + h - 52), remate, fuente("Condensed", 38), BLANCO, "mm", 255 * _eo((dt - mr) / .5))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ destello (la desaparición de los dwemer, 4-nov-2026)
def destello(titulo, n=60, remate=None, cols=20, ancho=1400):
    """n siluetas de bronce. marca 0: aparecen en barrido · marca 1: destello blanco que llena el panel y TODAS se borran a la
    vez; donde estaban queda ceniza que cae y se apaga. remate = (texto, i_marca). Primer uso: los dwemer en 1E 700."""
    T = 56
    filas_ = math.ceil(n / cols)
    h = 110 + filas_ * (T + 18) + (100 if remate else 30)
    rng = np.random.default_rng(700)
    ceniza = [(rng.uniform(.1, .9), rng.uniform(.2, 1.0), rng.uniform(.6, 1.6)) for _ in range(n * 4)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0 = M + (ancho - cols * (T + 6)) / 2
        t1 = mk[1]
        for k in range(n):
            x, y = x0 + k % cols * (T + 6), M + 112 + k // cols * (T + 18)
            if dt < t1:
                a = _eo((dt - mk[0] - k * .012) / .25)
                if a > .01:
                    _silueta(d, x, y, T, ORO, 235 * a)
            else:
                v = dt - t1
                for j in range(4):
                    fx, fy, vel = ceniza[k * 4 + j]
                    cy = y + T * fy + v * 26 * vel
                    a = 200 * max(0.0, 1 - v / 2.6)
                    if a > 4:
                        r = 2.2
                        d.ellipse((x + T * fx - r, cy - r, x + T * fx + r, cy + r), fill=GRIS + (int(a),))
        if dt >= t1:
            v = dt - t1
            fl = max(0.0, 1 - v / .45)
            if fl > 0:
                capa = Image.new("RGBA", im.size, BLANCO + (int(235 * fl),))
                im.alpha_composite(capa)
                d = ImageDraw.Draw(im)
        _remate(d, M, ancho, h, remate, dt, mk)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ escalera y cosmología («Los 20 seres más poderosos», 5-nov-2026)
def escalera(titulo, peldanos, ancho=760):
    """Escala de poder vertical. peldanos = [etiqueta, ...] de abajo arriba. La marca k lleva el rombo dorado al peldaño k (sube
    con rebote): los de abajo quedan en hueso, el actual en oro con su etiqueta grande, los de arriba en gris. Sin marcas: peldaño 0."""
    n = len(peldanos)
    PH = 74
    h = 110 + n * PH + 30

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        ms = [m for m in marcas if m is not None]
        k = max([i for i, m in enumerate(ms) if dt >= m] or [0])
        prev = max([i for i, m in enumerate(ms) if dt >= m][:-1] or [0]) if k else 0
        u = _eo((dt - ms[k]) / .6) if ms and dt >= ms[k] else 1.0
        pos = prev + (k - prev) * u
        xl, xr = M + 70, M + ancho - 50
        for i, et in enumerate(peldanos):
            y = M + 110 + (n - 1 - i) * PH + PH / 2
            c = ORO if i == k else HUESO if i < k else GRIS
            a = 255 * _eo((dt - i * .06) / .3)
            d.line([(xl, y + 26), (xr, y + 26)], fill=c + (int(a * .5),), width=2)
            _texto(d, (xl + 46, y), et.upper(), fuente("SemiBold Condensed" if i == k else "Condensed", 44 if i == k else 34),
                   c, "lm", a, track=3)
        yy = M + 110 + (n - 1 - pos) * PH + PH / 2
        r = 15
        d.polygon([(xl, yy - r), (xl + r, yy), (xl, yy + r), (xl - r, yy)], fill=ORO + (255,))
        d.line([(xl, M + 120), (xl, M + 110 + n * PH - 20)], fill=HUESO + (90,), width=2)
        return _salida(im, dt)
    return fn


def cosmologia(titulo, anillos, ancho=1500):
    """Cosmología en anillos concéntricos. anillos = [(nombre, sub), ...] de dentro afuera (Mundus → Oblivion → Aetherius → el
    vacío → el Soñador). La marca k dibuja el anillo k (círculo que se cierra) con su nombre a la derecha; el último encendido va en
    oro y los anteriores en hueso tenue. El centro late como un punto de luz (Nirn)."""
    n = len(anillos)
    h = 110 + 640

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, cy = M + ancho * .34, M + 110 + 320
        R0, paso = 46, 270 / max(1, n)
        ms = list(marcas[:n]) + [None] * max(0, n - len(marcas))
        on = [m is not None and dt >= m for m in ms]
        act = max([i for i in range(n) if on[i]] or [-1])
        pul = .5 + .5 * math.sin(dt * 3.2)
        d.ellipse((cx - 14 - 4 * pul, cy - 14 - 4 * pul, cx + 14 + 4 * pul, cy + 14 + 4 * pul), fill=BLANCO + (230,))
        for i, (nom, sub) in enumerate(anillos):
            if not on[i]:
                continue
            u = _eo((dt - ms[i]) / .9)
            r = R0 + (i + 1) * paso
            c = ORO if i == act else HUESO
            a = 255 if i == act else 120
            d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * u, fill=c + (a,), width=6 if i == act else 3)
            ty = M + 150 + i * (520 / max(1, n))
            tx = M + ancho * .66
            aa = 255 * _eo((dt - ms[i] - .3) / .5) * (1 if i == act else .55)
            dy = max(-r * .96, min(r * .96, ty - cy))
            d.line([(cx + math.sqrt(r * r - dy * dy), cy + dy), (tx - 20, ty)], fill=c + (int(aa * .5),), width=2)
            _texto(d, (tx, ty), nom.upper(), fuente("SemiBold Condensed", 46 if i == act else 36), c, "lm", aa, track=4)
            if sub:
                _texto(d, (tx, ty + 42), sub, fuente("Condensed", 30), (205, 200, 190), "lm", aa)
        return _salida(im, dt)
    return fn


def bucle(titulo, pasos, valores, unidad="%", remate=None, ancho=1100):
    """Bucle que se alimenta solo (tes_builds_rotas, 10-nov-2026: Reforzar restauración y el crafteo encadenado). pasos = [texto]
    (3-4) en círculo; un rombo dorado da la vuelta sin parar y cada nodo se enciende al pasar. valores = [número] por marca: el
    contador del centro corre al valor de la marca alcanzada (crece a saltos, en oro; el último en rojo sangre si hay remate).
    remate = (texto, i_marca) debajo del círculo. Sin marcas: valores[0]."""
    n = len(pasos)
    R = 300
    h = 140 + 2 * R + 140 + (90 if remate else 0)

    def fn(dt, dur, marcas):
        im, M = _humo(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        ms = [m for m in marcas if m is not None]
        k = max([i for i, m in enumerate(ms) if dt >= m] or [0])
        cx, cy = M + ancho / 2, M + 120 + R + 40
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=HUESO + (110,), width=3)
        vel = 1.0 + .5 * k                                    # cada vuelta más rápida
        ang = (dt * vel * 2 * math.pi / 2.6) % (2 * math.pi)
        for i, t in enumerate(pasos):
            a_i = -math.pi / 2 + i * 2 * math.pi / n
            x, y = cx + R * math.cos(a_i), cy + R * math.sin(a_i)
            dif = abs(((ang - (a_i + math.pi / 2)) + math.pi) % (2 * math.pi) - math.pi)
            c = ORO if dif < .5 else HUESO
            al = 255 * _eo((dt - i * .12) / .35)
            d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=c + (int(al),))
            ox = 0 if abs(math.cos(a_i)) < .3 else (40 if math.cos(a_i) > 0 else -40)
            oy = -46 if math.sin(a_i) < -.5 else (46 if math.sin(a_i) > .5 else 0)
            anc = "mm" if ox == 0 else ("lm" if ox > 0 else "rm")
            _texto(d, (x + ox, y + oy), t.upper(), fuente("SemiBold Condensed", 38), c, anc, al, track=2)
        a_r = ang - math.pi / 2
        rx, ry = cx + R * math.cos(a_r), cy + R * math.sin(a_r)
        r = 16
        d.polygon([(rx, ry - r), (rx + r, ry), (rx, ry + r), (rx - r, ry)], fill=ORO + (255,))
        v0 = valores[k - 1] if k and dt >= ms[k] else 0
        v1 = valores[min(k, len(valores) - 1)]
        u = _eo((dt - ms[k]) / .8) if ms and dt >= ms[k] else _eo(dt / .8)
        v = v0 + (v1 - v0) * u
        txt = f"{v:,.0f}".replace(",", ".") + unidad
        rojo = remate and k >= remate[1]
        _texto(d, (cx, cy), txt, fuente("Bold Condensed", 120), SANGRE if rojo else ORO, "mm", 255)
        if remate and k >= remate[1]:
            _texto(d, (cx, cy + R + 120), remate[0].upper(), fuente("SemiBold Condensed", 46), SANGRE, "mm",
                   255 * _eo((dt - ms[remate[1]]) / .4), track=4)
        return _salida(im, dt)
    return fn
