# -*- coding: utf-8 -*-
"""MOTION GRAPHICS «interfaz de Elden Ring» por código (Runa Caída; primer uso `er_radagon_atrocidades`, 14-oct-2026).
Hermano de nucleo/mg_tes.py (Skyrim) y mg_wow.py con la estética de los menús de Elden Ring: Garamond (la serif del juego
es una garalda; en Windows la más parecida es GARA.TTF), dorado viejo para los títulos, pergamino para el texto, paneles
casi negros con filete dorado fino y el rótulo grande con banda negra difusa de «ENEMIGO ABATIDO». CERO cifras ni citas
inventadas: solo lo que el guion ya dice.

Uso desde videos/<v>/efectos.py (FX `mg` de nucleo/secuencia_fx.py; acepta de/a o en/dur):
    import mg_er as E
  puesto(arriba, titulo)                         banda negra a lo ancho + título dorado que entra cerrando el espaciado
  descripcion(nombre, texto, tipo=None, icono=None)   ficha de descripción de objeto; *entre asteriscos* = dorado
  mensaje(lineas)                                mensaje del suelo (texto ámbar que brilla); una línea por marca
  doble_vida()                                   esquema de matrimonios: Márika-Godfrey / Radagon-Rennala -> exilio -> fusión
  gemelos()                                      un solo dios que se parte en dos hijos con su maldición
  hilos(centro, nombres, titulo)                 el encanto: un centro dorado con seguidores atados por hilos; la última marca
                                                 corta los hilos y los seguidores se enfrentan (rojo)   (er_miquella_atrocidades)
  cosido(alma, cuerpo, resultado)                alma de uno + cuerpo de otro -> un solo ser «cosido»
  cruces(etiquetas, total=13)                    fila de cruces que se encienden una por marca con lo que se abandona
  triada(filas, titulo)                          columnas que entran por marca; la última resalta en ámbar
  marionetas(titiritero, munecos, dueno)         cruceta con muñecos colgando; la última marca le da la vuelta: el titiritero
                                                 cuelga de los hilos de `dueno` (er_ranni_atrocidades, 21-oct-2026)
  sombra(ama, sombra, amos)                      los Dos Dedos atan a la Empírea y a su sombra; ella corta su hilo y la
                                                 sombra enloquece en rojo
  domino(fichas)                                 fila de fichas que caen una sobre otra (causa -> efecto); la última en rojo
  constelacion(nombres, centro, tu, remate)      estrellas unidas a la Luna que se apagan una por marca; quedan la Luna y «Tú»
  juramento(clausulas, firmas, remate)           contrato en pergamino: cláusulas por marca, firmas que se pudren, sello rojo
                                                 (er_malenia_atrocidades, 23-oct-2026)
  contagio(nombres, centro, remate)              flor escarlata que late; una vena roja tiñe cada nombre del anillo por marca
  floraciones(etiquetas, final)                  tres capullos: se abren la 1.ª y la 2.ª; la 3.ª late en rojo con `final`
  repudio(madre, hijas, remate)                  madre unida a sus hijas por hilos dorados que se parten en rojo
  acuerdo(da, pides, letra, remate)              contrato de dos columnas; la letra pequeña crece en rojo y sella «Deber»
                                                 (er_melina_atrocidades, 27-oct-2026)
  ecos(lineas, firma, revela)                    citas que se escriben con el Círculo de Elden girando; la firma se tacha
  arbol_arde(etapas)                             el Árbol Áureo por código: la llama llega, trepa, la copa arde, llueve ceniza
  muerte_suelta(nombres, remate)                 Runa de la Muerte presa en eslabones que saltan; ondas que tachan a todos
  lanzas(bando, centro, tu)                      las lanzas del enemigo se clavan en el león rojo y vuelven contra ti como
                                                 flechas de gravedad (er_radahn_atrocidades, 28-oct-2026)
  cielo_sujeto(atados, quien, remate)            cielo quieto: hilos de gravedad atan estrellas (destinos) a `quien`; al caer
                                                 se rompen, el cielo gira y cae una estrella
  balanza(izq, der, pesos, remate)               balanza de pruebas que se inclina por marca; al final vuelve al centro
  espejo(padre, hijo, papel_padre, papel_hijo, idolo)   el padre y el hijo acaban en el mismo papel; el ídolo se tacha
  cien(titulo, encendidos, remate)               100 estrellas apagadas; se encienden N (campaña de suscripción, 30-oct-2026)
  dos_nombres(a, b, remate)                      dos cartas (Margit / Morgott) que se funden en una; la primera se deshace
                                                 como su capa raída (er_morgott_atrocidades, 5-nov-2026)
  pila(etiquetas, remate)                        capas de cadáveres que caen sobre la muralla; el Árbol brilla encima
  subsuelo(arriba, abajo, sello, remate)         corte de la ciudad dorada y las celdas del subsuelo; el sello se estampa
  cuenta_atras(numeros, final, sub_final, remate)  Tres/Duo/Unus: anillos rojos que se cierran sobre «Tú»; NIHIL late y vacía
                                                 tu vida (er_mohg_atrocidades, 10-nov-2026)
  reclutamiento(pasos, remate)                   escalera de sangre (Varré, dedo, paño, medalla); arriba, Mohg no responde
  dinastia(cabeza, sub, filas, arriba, remate)   organigrama de la dinastía; la sangre de todas las ramas sube a la Madre Informe
  trono_vacio(nombres, remate)                   nombres que buscan el trono y se tachan; crece el muro de espinas
  votacion(a, b, titulo, caja, remate)           dos voces con su onda (la que habla brilla), caja de comentario que se escribe
                                                 sola y balanza SIN cifras (er_godrick_atrocidades, 11-nov-2026)
  injerto(centro, sub, miembros, remate)         torso al que vuelan miembros uno por marca y se cosen con puntadas rojas
  linaje(raiz, hijos, medio, remate)             corona de Godfrey; el tronco se apaga de oro a gris; los hijos brotan miembros cosidos
  cadena(eslabones, preso, amo, remate)          eslabones de la Orden al preso que se encienden en rojo por marca
  expediente(acusado, sub, cargos, ya, sello)    ficha de acusación recurrente: un cargo por marca con palomita roja y sello
                                                 CULPABLE (er_sinluz_atrocidades, 16-nov-2026)
  audiencia(campeones, tu, remate)               campeones que entran en las fauces de la serpiente; «Tú», el siguiente
  uvas(etiquetas, remate)                        racimo de uvas que giran y son ojos; etiquetas a sus dueños; remate rojo
  paciencia(n, umbral, quien, basta, remate)     9 raíces: doradas hasta la 4.ª, sello «Basta», luego rojas hasta la 9.ª
  estandartes / contencion / gracia_perdida      (er_godfrey_atrocidades, 19-nov-2026)
  inquisicion(instrumentos, remate, titulo)      archivo de la inquisición: una ficha (icono + nombre) por marca y sello rojo
                                                 final (er_rykard_atrocidades, 22-nov-2026)
  red_secuestro(origenes, destino, remate)       lugares que se encienden por marca; líneas punteadas rojas convergen en la placa
  estandarte_caido(emblema, quien, remate)       estandarte con emblema dorado que se agrieta, se tacha en X y cae
  incubadora(etiqueta, sub, remate)              bolsa amniótica húmeda que gotea; serpiente enroscada dentro; etiqueta escrita
  recibo(concepto, pagador, cobrador, pago, sello)   recibo en pergamino, una línea por marca, sello rojo «COBRADO»
  medalla(icono, nombre, efecto, cita, remate)  ficha de talismán: barra de ATAQUE que sube con cada baja, cita en carmín y
                                                 sello sobre el medallón (er_messmer_atrocidades, 24-nov-2026)
  empalados(n, titulo, sub, remate)              lanzas que se alzan con una bestia divina colgada; el fuego sube de todas
  tumba(nombres, motivo, lloro, remate)          corte del suelo: losas con nombre que bajan y se encadenan; cae una lágrima
  sopa(nombre, antes, despues, remate, icono)    cuenco que humea; el vapor se apaga y el termómetro baja a gris frío
  despojados(dentro, fuera, cita, remate)        círculo de la gracia del oro; los de fuera se tachan en carmín con llamas
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ORO, ORO_OSC, PERGAMINO, GRIS, AMBAR, ROJO = (214, 182, 110), (140, 112, 60), (226, 216, 190), (150, 142, 126), (255, 186, 92), (176, 52, 40)
_fc = {}


def fuente(estilo, tam):
    """estilo: «r» (GARA), «b» (GARABD), «i» (GARAIT)."""
    k = (estilo, tam)
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"r": "C:/Windows/Fonts/GARA.TTF", "b": "C:/Windows/Fonts/GARABD.TTF",
                                     "i": "C:/Windows/Fonts/GARAIT.TTF"}[estilo], tam)
    return _fc[k]


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _ancho(d, s, f, track):
    return sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)


def _texto(d, xy, s, f, color, ancla="la", alfa=255, track=0, sombra=True):
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if not track:
        if sombra:
            d.text((xy[0] + 2, xy[1] + 2), s, font=f, fill=(0, 0, 0, int(a * .85)), anchor=ancla)
        d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla)
        return
    w = _ancho(d, s, f, track)
    x = xy[0] - (w / 2 if ancla[0] == "m" else w if ancla[0] == "r" else 0)
    for c in s:
        if sombra:
            d.text((x + 2, xy[1] + 2), c, font=f, fill=(0, 0, 0, int(a * .85)), anchor="l" + ancla[1])
        d.text((x, xy[1]), c, font=f, fill=tuple(color) + (a,), anchor="l" + ancla[1])
        x += d.textlength(c, font=f) + track


def _brillo(im, radio=10, fuerza=1.0):
    """Halo: copia desenfocada del propio texto debajo (el dorado del juego brilla un poco)."""
    g = im.filter(ImageFilter.GaussianBlur(float(radio)))
    a = np.array(g)
    a[..., 3] = np.clip(a[..., 3].astype(np.float32) * fuerza, 0, 255).astype(np.uint8)
    out = Image.fromarray(a)
    out.alpha_composite(im)
    return out


def _filete(d, cx, y, medio, color=ORO, alfa=255):
    """Línea dorada fina que se desvanece hacia los extremos."""
    for i in range(50):
        u0, u1 = i / 50, (i + 1) / 50
        k = (1 - u0) ** 1.2
        for s in (-1, 1):
            d.line([(cx + s * u0 * medio, y), (cx + s * u1 * medio, y)], fill=color + (int(220 * k * alfa / 255),), width=2)


def _bgra(im, alfa=1.0):
    a = np.array(im)
    if alfa < 1:
        a[..., 3] = (a[..., 3] * max(0.0, alfa)).astype(np.uint8)
    return a[..., [2, 1, 0, 3]].copy()


def _partir(d, s, f, ancho):
    lineas, cur = [], ""
    for w in s.split():
        prueba = (cur + " " + w).strip()
        if d.textlength(prueba.replace("*", ""), font=f) <= ancho or not cur:
            cur = prueba
        else:
            lineas.append(cur)
            cur = w
    return lineas + [cur] if cur else lineas


# ------------------------------------------------------------------ rótulo de puesto («ENEMIGO ABATIDO»)
def puesto(arriba, titulo, ancho=1920, color=ORO):
    """Banda negra difusa a lo ancho; `arriba` chico en pergamino y `titulo` grande dorado con halo, que entra cerrando el
    espaciado (como el aviso de jefe derrotado). Sale fundiéndose."""
    h = 250
    f1, f2 = fuente("r", 40), fuente("r", 92)
    # MIDE (22-nov-2026, er_rykard: «IGLESIA DE LA CIUDAD DE LOS PENADOS» se salía por los dos lados): la letra baja hasta que
    # el texto (con el espaciado final) cabe en el 86 % del ancho; los títulos cortos quedan igual que antes.
    _tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    t2, t1 = 92, 40
    while t2 > 50 and _ancho(_tmp, titulo.upper(), f2, 6) > ancho * .86:
        t2 -= 4
        f2 = fuente("r", t2)
    while t1 > 26 and _ancho(_tmp, arriba.upper(), f1, 8) > ancho * .86:
        t1 -= 2
        f1 = fuente("r", t1)
    # el espaciado de entrada (6 → 36) tampoco puede sacar el título del cuadro: se limita a lo que cabe en el 94 %
    _n = max(1, len(titulo) - 1)
    _extra = max(0.0, min(30.0, (ancho * .94 - _ancho(_tmp, titulo.upper(), f2, 6)) / _n))

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, h), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rectangle((ancho * .06, 52, ancho * .94, h - 52), fill=190)
        banda = Image.new("RGBA", im.size, (4, 3, 2, 255))
        banda.putalpha(m.filter(ImageFilter.GaussianBlur(34)))
        im.alpha_composite(banda)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        a = 255 * _eo(dt / .6)
        _texto(d, (ancho / 2, 72), arriba.upper(), f1, PERGAMINO, "mm", a * .9, track=8)
        tr = 6 + _extra * (1 - _eo(dt / 1.1))
        _texto(d, (ancho / 2, 152), titulo.upper(), f2, color, "mm", a, track=tr, sombra=False)
        im.alpha_composite(_brillo(txt, 9, 1.3))
        return _bgra(im, min(1.0, (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ ficha de descripción de objeto
def descripcion(nombre, texto, tipo=None, icono=None, ancho=900):
    """Panel del inventario: icono opcional a la izquierda (ruta de imagen), nombre en pergamino, `tipo` gris en cursiva,
    filete dorado y el texto de la descripción, que aparece línea a línea. *Entre asteriscos* sale en dorado."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fn_, ft, fd = fuente("r", 56), fuente("i", 34), fuente("r", 42)
    ic = None
    if icono:
        ic = Image.open(icono).convert("RGBA")
        ic.thumbnail((150, 150), Image.LANCZOS)
    x_txt = 40 + (175 if ic else 0)
    lineas = _partir(tmp, texto, fd, ancho - 80)
    nombres = _partir(tmp, nombre, fn_, ancho - x_txt - 40)
    alto_cab = max(30 + 60 * len(nombres) + (40 if tipo else 0), 190 if ic else 0)
    h = alto_cab + 40 + len(lineas) * 52 + 36
    M = 40

    def base():
        im = Image.new("RGBA", (ancho + 2 * M, h + 2 * M), (0, 0, 0, 0))
        sh = Image.new("L", im.size, 0)
        ImageDraw.Draw(sh).rectangle((M - 6, M - 6, M + ancho + 6, M + h + 6), fill=200)
        sombra = Image.new("RGBA", im.size, (0, 0, 0, 255))
        sombra.putalpha(sh.filter(ImageFilter.GaussianBlur(22)))
        im.alpha_composite(sombra)
        d = ImageDraw.Draw(im)
        d.rectangle((M, M, M + ancho, M + h), fill=(14, 12, 9, 228))
        d.rectangle((M, M, M + ancho, M + h), outline=ORO_OSC + (255,), width=2)
        d.rectangle((M + 7, M + 7, M + ancho - 7, M + h - 7), outline=ORO_OSC + (110,), width=1)
        for cx, cy in ((M, M), (M + ancho, M), (M, M + h), (M + ancho, M + h)):     # rombos en las esquinas
            d.polygon([(cx - 8, cy), (cx, cy - 8), (cx + 8, cy), (cx, cy + 8)], fill=(14, 12, 9, 255), outline=ORO + (255,))
        if ic:
            x0, y0 = M + 34, M + 26
            d.rectangle((x0 - 4, y0 - 4, x0 + 154, y0 + 154), fill=(28, 24, 18, 255), outline=ORO_OSC + (200,))
            im.alpha_composite(ic, (x0 + (150 - ic.width) // 2, y0 + (150 - ic.height) // 2))
        y = M + 30
        for k, ln in enumerate(nombres):
            _texto(d, (M + x_txt, y + 28 + 60 * k), ln, fn_, PERGAMINO, "lm")
        y += 60 * len(nombres)
        if tipo:
            _texto(d, (M + x_txt, y + 18), tipo, ft, GRIS, "lm")
        y = M + alto_cab + 12
        _filete(d, M + ancho / 2, y, ancho * .46)
        return im, y + 28

    cache = {}

    def fn(dt, dur, marcas):
        if "b" not in cache:
            cache["b"] = base()
        im0, y0 = cache["b"]
        im = im0.copy()
        d = ImageDraw.Draw(im)
        y = y0
        dorado = False                                  # el dorado sigue de una línea a la siguiente
        for k, ln in enumerate(lineas):                 # línea a línea, cada 0,35 s
            a = 255 * _eo((dt - .25 - k * .35) / .4)
            x = M + 40
            trozos = ln.split("*")
            for j, trozo in enumerate(trozos):
                if j:
                    dorado = not dorado
                if trozo:
                    _texto(d, (x, y + 22), trozo, fd, ORO if dorado else PERGAMINO, "lm", a)
                    x += d.textlength(trozo, font=fd)
            y += 52
        u = _eo(dt / .35)
        if u < 1:
            im = im.resize((im.width, max(2, int(im.height * (.6 + .4 * u)))), Image.BILINEAR)
        return _bgra(im, min(u, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ mensaje del suelo
def mensaje(lineas, ancho=1500):
    """Mensaje grabado en el suelo: letras ámbar con halo fuerte que aparecen de izquierda a derecha.
    La línea k entra en la marca k (si faltan marcas, cada 1,6 s); las anteriores se atenúan."""
    f = fuente("r", 84)
    h = 140 + 120 * len(lineas)

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, h), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).ellipse((ancho * .08, 30, ancho * .92, h - 30), fill=170)
        fondo = Image.new("RGBA", im.size, (3, 2, 1, 255))
        fondo.putalpha(m.filter(ImageFilter.GaussianBlur(40)))
        im.alpha_composite(fondo)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        for k, s in enumerate(lineas):
            t0 = marcas[k] if k < len(marcas) else k * 1.6
            u = (dt - t0) / max(.5, .05 * len(s))
            if u <= 0:
                continue
            n = int(len(s) * min(1.0, u)) + (1 if u < 1 else 0)
            siguiente_ = marcas[k + 1] if k + 1 < len(marcas) else (k + 1) * 1.6 if k + 1 < len(lineas) else 1e9
            a = 255 if dt < siguiente_ else 150
            w = d.textlength(s, font=f)
            y = 70 + 120 * k + 60
            d.text((ancho / 2 - w / 2, y), s[:n], font=f, fill=AMBAR + (a,), anchor="lm")
        im.alpha_composite(_brillo(txt, 14, 2.2))
        return _bgra(im, min(_eo(dt / .4), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ esquemas
def _nodo(d, cx, cy, nombre, sub, color, a, fn_, fs, abajo=False):
    """Nodo con nombre encima (o debajo con `abajo`, cuando la línea llega desde arriba) y subtítulo gris debajo."""
    if a <= 0:
        return
    d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(14, 12, 9, int(a)), outline=color + (int(a),), width=3)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=color + (int(a),))
    if abajo:
        _texto(d, (cx, cy + 24), nombre, fn_, color, "mt", a)
    else:
        _texto(d, (cx, cy - 34), nombre, fn_, color, "mb", a)
    if sub:
        _texto(d, (cx, cy + (90 if abajo else 30)), sub, fs, GRIS, "mt", a)


def _linea(d, p0, p1, u, color, a, ancho=3):
    if u <= 0 or a <= 0:
        return
    x = p0[0] + (p1[0] - p0[0]) * min(1, u)
    y = p0[1] + (p1[1] - p0[1]) * min(1, u)
    d.line([p0, (x, y)], fill=color + (int(a),), width=ancho)


def _panel(w, h):
    M = 50
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((M, M, M + w, M + h), 30, fill=215)
    fondo = Image.new("RGBA", im.size, (8, 7, 5, 255))
    fondo.putalpha(m.filter(ImageFilter.GaussianBlur(24)))
    im.alpha_composite(fondo)
    return im, M


def doble_vida(titulo="Dos matrimonios a la vez", w=1500, h=620):
    """marca 0: Márika = Godfrey (arriba) · marca 1: Radagon = Rennala (abajo) · marca 2: Godfrey se apaga («exiliado») y
    Radagon sube a casarse con Márika · marca 3: Radagon se funde con Márika y queda «RADAGON ES MÁRIKA»."""
    fn_, fs, ftit = fuente("r", 50), fuente("i", 36), fuente("r", 40)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", 255 * _eo(dt / .4), track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=255 * _eo(dt / .4))
        yA, yB = M + 210, M + 490
        xM, xG, xR, xN = M + w * .32, M + w * .68, M + w * .32, M + w * .68
        uA, uB, uC, uD = (_eo((dt - mk[i]) / .6) for i in range(4))
        # arriba: Márika - Godfrey
        _nodo(d, xM, yA, "Márika", "reina", ORO, 255 * uA, fn_, fs)
        aG = 255 * uA * (1 - .7 * uC)
        _nodo(d, xG, yA, "Godfrey", "exiliado" if uC > .5 else "primer Señor del Círculo", ORO if uC < .5 else GRIS, aG, fn_, fs)
        _linea(d, (xM + 16, yA), (xG - 16, yA), uA, ORO, 255 * (1 - uC))
        if uC > 0:                                          # la línea rota del exilio
            d.line([(xM + 16, yA), ((xM + xG) / 2 - 20, yA)], fill=GRIS + (int(200 * uC),), width=2)
            d.line([((xM + xG) / 2 + 20, yA), (xG - 16, yA)], fill=GRIS + (int(200 * uC),), width=2)
        # abajo: Radagon - Rennala; en la marca 2 Radagon sube junto a Márika
        sube = uC
        xr = xR + (xM - 270 - xR) * sube
        yr = yB + (yA - yB) * sube
        fusion = uD
        xr = xr + (xM - xr) * fusion
        _nodo(d, xN, yB, "Rennala", "abandonada" if uC > .5 else "reina de Caria", PERGAMINO if uC < .5 else GRIS,
              255 * uB * (1 - .5 * uC), fn_, fs)
        _linea(d, (xr + 16, yr), (xN - 16, yB), uB, PERGAMINO, 255 * uB * (1 - uC))
        if fusion < .98:
            _nodo(d, xr, yr, "Radagon", "rey consorte" if uC > .5 else "", ROJO if uC < .5 else ORO, 255 * uB * (1 - fusion), fn_, fs)
        if uC > 0 and fusion < .9:
            _linea(d, (xr + 16, yr), (xM - 16, yA), 1, ORO, 255 * uC * (1 - fusion), 2)
        if fusion > 0:
            txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dt_ = ImageDraw.Draw(txt)
            _texto(dt_, (M + w / 2, M + 350), "RADAGON ES MÁRIKA", fuente("r", 70), AMBAR, "mm", 255 * fusion, track=6, sombra=False)
            im.alpha_composite(_brillo(txt, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def gemelos(w=1300, h=620):
    """marca 0: «Un solo dios» · marca 1: se parte en dos ramas · marca 2: Miquella «infancia eterna» · marca 3: Malenia
    «putrefacción» (la rama de Malenia se tiñe de rojo)."""
    fn_, fs, ftit = fuente("r", 54), fuente("i", 38), fuente("r", 44)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        u0, u1, u2, u3 = (_eo((dt - mk[i]) / .6) for i in range(4))
        cx, ytop = M + w / 2, M + 130
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        _texto(ImageDraw.Draw(txt), (cx, ytop - 20), "UN SOLO DIOS", ftit, ORO, "mm", 255 * u0, track=8, sombra=False)
        im.alpha_composite(_brillo(txt, 10, 1.5))
        d = ImageDraw.Draw(im)
        d.ellipse((cx - 13, ytop + 30, cx + 13, ytop + 56), fill=(14, 12, 9, int(255 * u0)), outline=ORO + (int(255 * u0),), width=3)
        yb = M + 380
        xa, xb = M + w * .27, M + w * .73
        _linea(d, (cx, ytop + 58), (cx, ytop + 140), u1, ORO, 255 * u1)
        _linea(d, (cx, ytop + 140), (xa, ytop + 140), u1, ORO, 255 * u1)
        _linea(d, (cx, ytop + 140), (xb, ytop + 140), u1, ROJO if u3 > .5 else ORO, 255 * u1)
        _linea(d, (xa, ytop + 140), (xa, yb - 14), u1, ORO, 255 * u1)
        _linea(d, (xb, ytop + 140), (xb, yb - 14), u1, ROJO if u3 > .5 else ORO, 255 * u1)
        _nodo(d, xa, yb, "Miquella", None, PERGAMINO, 255 * u1, fn_, fs, abajo=True)
        _nodo(d, xb, yb, "Malenia", None, PERGAMINO, 255 * u1, fn_, fs, abajo=True)
        if u2 > 0:
            _texto(d, (xa, yb + 96), "infancia eterna", fs, GRIS, "mt", 255 * u2)
        if u3 > 0:
            _texto(d, (xb, yb + 96), "putrefacción", fs, ROJO, "mt", 255 * u3)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_miquella_atrocidades (19-oct-2026)
def _cruz(d, cx, cy, s, color, a, ancho=4):
    """La cruz de Miquella simplificada: palo largo, travesaño y el arco de la izquierda."""
    if a <= 0:
        return
    c = color + (int(a),)
    d.line([(cx, cy - s), (cx, cy + s * 1.5)], fill=c, width=ancho)
    d.line([(cx - s * .45, cy - s * .35), (cx + s * .45, cy - s * .35)], fill=c, width=ancho)
    d.arc((cx - s * .55, cy - s * .9, cx + s * .25, cy - s * .1), 90, 270, fill=c, width=max(2, ancho - 1))


def hilos(centro, nombres, titulo="El encanto", w=1500, h=640):
    """marca 0: el centro brilla · marcas 1..n: cada seguidor entra atado con un hilo dorado · marca n+1: los hilos se
    cortan, el centro se apaga y los seguidores quedan unidos por líneas rojas (se enfrentan)."""
    fn_, ftit, fs = fuente("r", 46), fuente("r", 40), fuente("i", 34)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 250
        rota = _eo((dt - mk[n + 1]) / .5)
        pts = []
        for i in range(n):
            ang = math.pi * (.92 - .84 * i / max(1, n - 1))
            pts.append((cx + math.cos(ang) * w * .40, cy + math.sin(ang) * 260))
        for i, (x, y) in enumerate(pts):
            u = _eo((dt - mk[1 + i]) / .5)
            if u <= 0:
                continue
            if rota < 1:                                    # hilo dorado que ondula; al romperse le falta el centro
                seg, ant = 24, (cx, cy)
                for k in range(1, seg + 1):
                    t = k / seg * u
                    p = (cx + (x - cx) * t, cy + (y - cy) * t + math.sin(t * 9 + dt * 3 + i) * 6)
                    if not (rota > 0 and abs(t - .5) < .1 * rota + .02):
                        d.line([ant, p], fill=ORO + (int(200 * u * (1 - rota)),), width=2)
                    ant = p
            _nodo(d, x, y, nombres[i], None, PERGAMINO if rota < .5 else ROJO, 255 * u, fn_, fs, abajo=True)
        if rota > 0:                                        # se enfrentan entre ellos
            for i in range(n):
                for j in range(i + 1, n):
                    if (i + j) % 2:
                        _linea(d, pts[i], pts[j], rota, ROJO, 150 * rota, 2)
        uc = _eo((dt - mk[0]) / .5)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        col = ORO if rota < .5 else GRIS
        r = 16 + 3 * math.sin(dt * 4) * (1 - rota)
        dd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(255 * uc),))
        _texto(dd, (cx, cy - 34), centro, fuente("r", 60), col, "mb", 255 * uc, sombra=False)
        im.alpha_composite(_brillo(txt, 14, 2.0 * (1 - .6 * rota)))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cosido(alma=("Radahn", "el alma"), cuerpo=("Mohg", "el cuerpo"), resultado="Consorte prometido",
           titulo="Dos hermanos cosidos en uno", w=1400, h=640):
    """marca 0: el alma (izquierda, dorado) · marca 1: el cuerpo (derecha, rojo) · marca 2: los dos se juntan al centro con
    una costura en zigzag y aparece `resultado`."""
    fn_, fs, fr = fuente("r", 64), fuente("i", 38), fuente("r", 70)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        u0, u1, u2 = (_eo((dt - mk[i]) / .6) for i in range(3))
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), fuente("r", 40), PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cy = M + h * .45
        xa = M + w * .22 + (w * .12) * u2
        xb = M + w * .78 - (w * .12) * u2
        for x, (nom, sub), col, u in ((xa, alma, ORO, u0), (xb, cuerpo, ROJO, u1)):
            if u <= 0:
                continue
            a = 255 * u
            d.ellipse((x - 110, cy - 110, x + 110, cy + 110), outline=col + (int(a),), width=4)
            _texto(d, (x, cy), nom, fn_, col, "mm", a)
            _texto(d, (x, cy + 130), sub, fs, GRIS, "mt", a * (1 - u2))
        if u2 > 0:                                          # costura entre los dos círculos
            cx = M + w / 2
            for k in range(int(9 * u2)):
                y0 = cy - 120 + k * 27
                d.line([(cx - 16, y0), (cx + 16, y0 + 13)], fill=PERGAMINO + (int(230 * u2),), width=3)
                d.line([(cx + 16, y0 + 13), (cx - 16, y0 + 27)], fill=PERGAMINO + (int(230 * u2),), width=3)
            txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(txt), (cx, M + h - 70), resultado.upper(), fr, AMBAR, "mm", 255 * u2, track=6, sombra=False)
            im.alpha_composite(_brillo(txt, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cruces(etiquetas, total=13, titulo="Las cruces de Miquella", w=1700, h=470, rojo_ultima=False):
    """Fila de `total` cruces apagadas; en la marca k se enciende la cruz k y su etiqueta sale debajo (la anterior se
    atenúa). Con `rojo_ultima`, la última etiqueta va en rojo."""
    ftit, fe = fuente("r", 40), fuente("i", 56)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(etiquetas) + 1)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        paso = (w - 160) / (total - 1)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i in range(total):
            x = M + 80 + i * paso
            u = _eo((dt - mk[i]) / .4) if i < len(etiquetas) else 0
            _cruz(d, x, M + 175, 44, GRIS, a0 * .55 * (1 - u))
            col = ROJO if (rojo_ultima and i == len(etiquetas) - 1) else ORO
            _cruz(dd, x, M + 175, 44, col, 255 * u)
        im.alpha_composite(_brillo(txt, 10, 1.6))
        d = ImageDraw.Draw(im)
        for k, s in enumerate(etiquetas):
            u = _eo((dt - mk[k]) / .4)
            fin = _eo((dt - mk[k + 1]) / .3) if k + 1 < len(etiquetas) else 0
            a = 255 * u * (1 - fin)
            if a > 0:
                col = ROJO if (rojo_ultima and k == len(etiquetas) - 1) else AMBAR
                _texto(d, (M + w / 2, M + h - 80), "Aquí abandono " + s, fe, col, "mm", a)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def triada(filas, titulo="Lo que quería de cada uno", w=1500, h=520):
    """filas = [(arriba, abajo), ...]: una columna por marca; la última se resalta en ámbar y las otras se tachan."""
    ftit, fa, fb = fuente("r", 40), fuente("r", 64), fuente("i", 44)
    n = len(filas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * n
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        ult = _eo((dt - mk[n - 1]) / .5)
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i, (arriba, abajo) in enumerate(filas):
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            x = M + w * (i + .5) / n
            if i == n - 1:
                _texto(dd, (x, M + 230), arriba.upper(), fa, AMBAR, "mm", 255 * u, track=4, sombra=False)
                _texto(dd, (x, M + 330), abajo, fb, PERGAMINO, "mm", 255 * u, sombra=False)
            else:
                a = 255 * u * (1 - .5 * ult)
                _texto(d, (x, M + 230), arriba.upper(), fa, ORO, "mm", a, track=4)
                _texto(d, (x, M + 330), abajo, fb, GRIS, "mm", a)
                if ult > 0:                                 # tachado
                    _linea(d, (x - 160, M + 330), (x + 160, M + 330), ult, ROJO, 220 * ult, 4)
        im.alpha_composite(_brillo(txt, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_ranni_atrocidades (21-oct-2026)
LUNA = (150, 186, 255)


def _muneco(d, cx, cy, s, color, a, bal=0.0):
    """Muñeco de hilo con la cabeza en (cx, cy); `bal` lo balancea. Devuelve (cabeza, mano izq., mano der.) para atar hilos."""
    cadera = (cx + bal * s * .12, cy + s * 1.0)
    hombro = (cx + bal * s * .06, cy + s * .4)
    manos = [(hombro[0] + sg * s * .45, hombro[1] + s * .38 - sg * bal * s * .2) for sg in (-1, 1)]
    if a > 0:
        c = color + (int(a),)
        d.ellipse((cx - s * .22, cy - s * .22, cx + s * .22, cy + s * .22), fill=(14, 12, 9, int(a)), outline=c, width=4)
        d.line([(cx, cy + s * .22), cadera], fill=c, width=5)
        for sg, mano in zip((-1, 1), manos):
            d.line([hombro, (hombro[0] + sg * s * .28, hombro[1] + s * .12), mano], fill=c, width=4)
            d.line([cadera, (cadera[0] + sg * s * .14, cadera[1] + s * .32),
                    (cadera[0] + sg * s * .2, cadera[1] + s * .66 + sg * bal * s * .08)], fill=c, width=4)
    return (cx, cy - s * .22), manos[0], manos[1]


def _cruceta(d, cx, y, ancho, color, a):
    if a <= 0:
        return
    c = color + (int(a),)
    d.line([(cx - ancho / 2, y), (cx + ancho / 2, y)], fill=c, width=7)
    d.line([(cx, y - 34), (cx, y + 34)], fill=c, width=7)
    d.ellipse((cx - 9, y - 9, cx + 9, y + 9), fill=c)


def marionetas(titiritero="Seluvis", munecos=("Nepheli", "Ranni"), dueno="Ranni", titulo="Quién mueve los hilos",
               remate="El titiritero era el muñeco", w=1500, h=660):
    """marca 0: la cruceta del titiritero · marcas 1..n: cada muñeco cuelga de sus hilos (el último en ámbar: el objetivo)
    · marca n+1: la escena se apaga y aparece la cruceta de `dueno` (azul luna) con el titiritero colgando en rojo."""
    fn_, ftit, fr = fuente("r", 48), fuente("r", 40), fuente("i", 50)
    n = len(munecos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx = M + w / 2
        vuelta = _eo((dt - mk[n + 1]) / .7)
        a1 = 255 * _eo((dt - mk[0]) / .5) * (1 - vuelta)
        yc = M + 190
        # --- 1.ª parte: el titiritero y sus muñecos
        _cruceta(d, cx, yc, w * .62, ORO, a1)
        _texto(d, (cx, yc - 48), titiritero, fn_, ORO, "mb", a1)
        for i, nom in enumerate(munecos):
            u = _eo((dt - mk[1 + i]) / .6)
            a = 255 * u * (1 - vuelta)
            if a <= 0:
                continue
            x = M + w * (.5 + (i - (n - 1) / 2) * (.62 / max(1, n)))
            yh = M + 290 - 40 * (1 - u)
            col = AMBAR if i == n - 1 else PERGAMINO
            cab, mi, md = _muneco(d, x, yh, 150, col, a, math.sin(dt * 1.6 + i * 1.3))
            for p, xo in ((cab, 0), (mi, -.12), (md, .12)):
                d.line([(x + xo * w * .3, yc), p], fill=PERGAMINO + (int(a * .55),), width=2)
            _texto(d, (x, yh + 268), nom, fn_, col, "mt", a)
        # --- 2.ª parte: la vuelta
        if vuelta > 0:
            a2 = 255 * vuelta
            txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dd = ImageDraw.Draw(txt)
            _cruceta(dd, cx, yc, w * .34, LUNA, a2)
            _texto(dd, (cx, yc - 48), dueno, fn_, LUNA, "mb", a2, sombra=False)
            im.alpha_composite(_brillo(txt, 12, 1.6))
            d = ImageDraw.Draw(im)
            yh = M + 290
            cab, mi, md = _muneco(d, cx, yh, 150, ROJO, a2, math.sin(dt * 2.2) * 1.3)
            for p, xo in ((cab, 0), (mi, -.1), (md, .1)):
                d.line([(cx + xo * w * .3, yc), p], fill=LUNA + (int(a2 * .7),), width=2)
            _texto(d, (cx + 150, yh + 60), titiritero, fn_, ROJO, "lm", a2)
            _texto(d, (cx, M + h - 60), remate, fr, AMBAR, "mm", 255 * _eo((dt - mk[n + 1] - .6) / .6))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _dedos(d, cx, cy, color, a):
    """Los Dos Dedos: dos dedos largos y pálidos con sus pliegues."""
    if a <= 0:
        return
    for alto, dx in ((120, -22), (104, 22)):
        d.rounded_rectangle((cx + dx - 15, cy - alto, cx + dx + 15, cy), 15, fill=(30, 26, 20, int(a)), outline=color + (int(a),), width=3)
        for f in (.55, .28):
            d.line([(cx + dx - 8, cy - alto * f), (cx + dx + 8, cy - alto * f)], fill=color + (int(a * .6),), width=2)


def sombra(ama="Ranni", sombra_="Blaidd", amos="Los Dos Dedos", titulo="La sombra de Ranni", w=1500, h=660):
    """marca 0: los Dos Dedos · marca 1: hilos dorados a la Empírea y a su sombra (unidos entre sí) · marca 2: ella corta su
    hilo y se vuelve azul luna («libre») · marca 3: la sombra tiembla en rojo («maldición»)."""
    fn_, fs, ftit = fuente("r", 54), fuente("i", 38), fuente("r", 40)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        u0, u1, u2, u3 = (_eo((dt - mk[i]) / .6) for i in range(4))
        cx, ya = M + w / 2, M + 250
        xa, xs, yb = M + w * .30, M + w * .70, M + 470
        _dedos(d, cx, ya, PERGAMINO, 255 * u0)
        _texto(d, (cx, ya + 14), amos, fs, PERGAMINO, "mt", 255 * u0)
        for (x, y), roto, col in (((xa, yb), u2, ORO), ((xs, yb), 0, ROJO if u3 > .5 else ORO)):
            if u1 <= 0:
                continue
            seg, ant = 22, (cx, ya + 56)
            for k in range(1, seg + 1):
                t = k / seg * u1
                p = (cx + (x - cx) * t, ya + 56 + (y - 70 - ya - 56) * t + math.sin(t * 8 + dt * 3) * 5)
                if not (roto > 0 and abs(t - .55) < .14 * roto):
                    d.line([ant, p], fill=col + (int(220 * u1 * (1 - .6 * roto)),), width=3)
                ant = p
        # la Empírea
        col_a = LUNA if u2 > .5 else PERGAMINO
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        r = 18 + 3 * math.sin(dt * 3) * u2
        dd.ellipse((xa - r, yb - r, xa + r, yb + r), fill=col_a + (int(255 * u1),))
        _texto(dd, (xa, yb + 34), ama, fn_, col_a, "mt", 255 * u1, sombra=False)
        im.alpha_composite(_brillo(txt, 12, 1.2 + 1.2 * u2))
        d = ImageDraw.Draw(im)
        _texto(d, (xa, yb + 102), "libre" if u2 > .5 else "Empírea", fs, LUNA if u2 > .5 else GRIS, "mt", 255 * u1)
        # la sombra: tiembla al enloquecer
        xs_ = xs + math.sin(dt * 37) * 7 * u3
        yb_ = yb + math.cos(dt * 29) * 5 * u3
        col_s = ROJO if u3 > .5 else GRIS
        if u1 <= 0:                                          # ImageDraw no mezcla alfa: con 0 abriría un agujero en el panel
            return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
        d.ellipse((xs_ - 26, yb_ - 26, xs_ + 26, yb_ + 26), fill=(6, 5, 4, int(255 * u1)), outline=col_s + (int(255 * u1),), width=4)
        _texto(d, (xs_, yb_ + 34), sombra_, fn_, ROJO if u3 > .5 else PERGAMINO, "mt", 255 * u1)
        _texto(d, (xs_, yb_ + 102), "maldición" if u3 > .5 else "su sombra", fs, col_s, "mt", 255 * u1)
        paso = (xs - xa - 80) / 22                           # el lazo ama-sombra (línea de puntos)
        for k in range(0, int(22 * u1), 2):
            x0 = xa + 40 + k * paso
            d.line([(x0, yb), (x0 + paso, yb)], fill=col_s + (int(200 * u1),), width=3)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def domino(fichas, titulo="La primera ficha", w=1700, h=600):
    """fichas = textos cortos (causa -> efecto). En la marca k cae la ficha k sobre la siguiente y su texto se enciende en
    ámbar (luego queda en pergamino); la última cae del todo y se tiñe de rojo."""
    ftit, fe = fuente("r", 40), fuente("i", 40)
    n = len(fichas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 1)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        sp = (w - 280) / n                                   # sitio a la derecha para la última, que cae del todo
        tw, th, base = 66, 240, M + 330
        for i, s in enumerate(fichas):
            xc = M + 60 + sp * (i + .5)
            u = _eo((dt - mk[i]) / .55)
            ult = i == n - 1
            tmax = math.radians(76) if ult else math.asin(min(1.0, (sp - tw) / th))
            ang = tmax * (u ** 1.6)
            piv = (xc + tw / 2, base)
            pts = [(piv[0] + px * math.cos(ang) - py * math.sin(ang), piv[1] + px * math.sin(ang) + py * math.cos(ang))
                   for px, py in ((-tw, 0), (0, 0), (0, -th), (-tw, -th))]
            col = ROJO if (ult and u > .5) else (ORO if u > 0 else ORO_OSC)
            d.polygon(pts, fill=(18, 15, 11, int(a0)))
            d.line(pts + [pts[0]], fill=col + (int(a0),), width=3)
            mx, my = (pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2
            d.ellipse((mx - 7, my - 7, mx + 7, my + 7), fill=col + (int(a0),))
            sig = _eo((dt - mk[i + 1]) / .4) if i + 1 < n else 0
            ct = ROJO if ult else (AMBAR if sig < .5 else PERGAMINO)
            for k, ln in enumerate(_partir(d, s, fe, sp - 14)):
                _texto(d, (xc, base + 40 + k * 46), ln, fe, ct, "mt", 255 * u)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _estrella(d, x, y, r, color, a):
    if a <= 0:
        return
    d.polygon([(x, y - r), (x + r * .28, y - r * .28), (x + r, y), (x + r * .28, y + r * .28), (x, y + r),
               (x - r * .28, y + r * .28), (x - r, y), (x - r * .28, y - r * .28)], fill=color + (int(a),))


def constelacion(nombres, centro="Ranni", tu="Tú", remate="Mil años de noche", titulo="Los que la quisieron", w=1500, h=660):
    """La Luna (`centro`) con una estrella por nombre unida por un hilo de luz; en la marca k la estrella k se apaga y su
    hilo se corta · marca n: aparece «Tú» pegado a la Luna · marca n+1: `remate` en ámbar."""
    fn_, ftit, fr = fuente("r", 42), fuente("r", 40), fuente("r", 64)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 300
        for k in range(40):                                  # polvo de estrellas que titila
            x = M + 40 + (k * 337) % (w - 80)
            y = M + 110 + (k * 191) % (h - 160)
            d.point((x, y), fill=PERGAMINO + (int(a0 * .25 * (1 + math.sin(dt * 2 + k))),))
        pts = [(cx + math.cos(-math.pi / 2 + 2 * math.pi * i / n + .3) * w * .36,
                cy + math.sin(-math.pi / 2 + 2 * math.pi * i / n + .3) * 175) for i in range(n)]
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i, (x, y) in enumerate(pts):
            ua = _eo((dt - .15 * i) / .5)
            off = _eo((dt - mk[i]) / .5)
            if off < 1:
                _linea(dd, (cx, cy), (x, y), ua, LUNA, 120 * ua * (1 - off), 2)
            col = PERGAMINO if off < .5 else GRIS
            _estrella(dd if off < .5 else d, x, y, 16 + 3 * math.sin(dt * 3 + i) * (1 - off), col, 255 * ua * (1 - .55 * off))
            _texto(d, (x, y + 26), nombres[i], fn_, col, "mt", 255 * ua * (1 - .45 * off))
        dd.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=LUNA + (int(a0),))          # la Luna, en cuarto
        dd.ellipse((cx - 40, cy - 70, cx + 70, cy + 40), fill=(8, 7, 5, int(a0 * .55)))
        u_tu = _eo((dt - mk[n]) / .6)
        if u_tu > 0:
            xt, yt = cx + 150, cy - 30
            _linea(dd, (cx + 55, cy - 10), (xt, yt), u_tu, AMBAR, 255 * u_tu, 4)
            _estrella(dd, xt, yt, 22, AMBAR, 255 * u_tu)
            _texto(dd, (xt + 34, yt), tu, fn_, AMBAR, "lm", 255 * u_tu, sombra=False)
        im.alpha_composite(_brillo(txt, 12, 1.7))
        d = ImageDraw.Draw(im)
        _texto(d, (cx, cy + 80), centro, fn_, LUNA, "mt", a0)
        u_r = _eo((dt - mk[n + 1]) / .6)
        if u_r > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (cx, M + h - 38), remate.upper(), fr, AMBAR, "mm", 255 * u_r, track=8, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_malenia_atrocidades (23-oct-2026)
CARMIN = (196, 40, 52)
TINTA = (46, 32, 20)


def _petalos(d, cx, cy, r, abre, color, a, n=7, giro=0.0):
    """Flor escarlata: `n` pétalos (elipses rotadas) que se abren con `abre` (0 = capullo cerrado, 1 = abierta)."""
    if a <= 0:
        return
    for i in range(n):
        ang = giro + 2 * math.pi * i / n
        sep = r * (.15 + .55 * abre)
        px, py = cx + math.cos(ang) * sep, cy + math.sin(ang) * sep
        largo, ancho = r * (.45 + .5 * abre), r * (.22 + .18 * abre)
        pts = []
        for k in range(16):
            t = 2 * math.pi * k / 16
            ex, ey = math.cos(t) * largo, math.sin(t) * ancho
            pts.append((px + ex * math.cos(ang) - ey * math.sin(ang), py + ex * math.sin(ang) + ey * math.cos(ang)))
        d.polygon(pts, fill=color + (int(a * .85),))
    d.ellipse((cx - r * .18, cy - r * .18, cx + r * .18, cy + r * .18), fill=AMBAR + (int(a),))


def juramento(clausulas, firmas=5, remate="Firme aquí", titulo="Juramento de los caballeros", w=1240, h=660):
    """Contrato en pergamino: marca k (< n) escribe la cláusula k; marca n: aparecen las firmas de los caballeros, que
    luego se pudren (manchas rojas que crecen sin parar); marca n+1: sello rojo `remate` que cae sobre el papel."""
    ftit, fc, fs = fuente("b", 42), fuente("i", 40), fuente("b", 64)
    n = len(clausulas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        pap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dp = ImageDraw.Draw(pap)
        x0, y0, x1, y1 = M + 70, M + 40, M + w - 70, M + h - 40
        dp.rounded_rectangle((x0, y0, x1, y1), 10, fill=(214, 198, 158, int(a0)))
        dp.rounded_rectangle((x0 + 14, y0 + 14, x1 - 14, y1 - 14), 6, outline=ORO_OSC + (int(a0 * .8),), width=2)
        _texto(dp, ((x0 + x1) / 2, y0 + 58), titulo.upper(), ftit, TINTA, "mm", a0, track=5, sombra=False)
        _filete(dp, (x0 + x1) / 2, y0 + 92, (x1 - x0) * .32, color=ORO_OSC, alfa=a0)
        y = y0 + 140
        for k, c in enumerate(clausulas):
            u = _eo((dt - mk[k]) / 1.1)
            if u <= 0:
                continue
            for ln in _partir(dp, f"{k + 1}. {c}", fc, x1 - x0 - 120):
                vis = ln[:int(len(ln) * u + .999)]
                _texto(dp, (x0 + 60, y), vis, fc, TINTA, "lm", 255 * min(1, u * 3), sombra=False)
                y += 50
            y += 14
        u_f = _eo((dt - mk[n]) / .9)
        manchas = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dm = ImageDraw.Draw(manchas)
        yf = y1 - 90
        for i in range(firmas):
            cx = x0 + 90 + (x1 - x0 - 180) * (i + .5) / firmas
            p = _eo((dt - mk[n] - .18 * i) / .7)
            if p <= 0:
                continue
            pts = [(cx - 70 + 140 * t, yf + 16 * math.sin(t * 9 + i * 1.7) * (1 - t * .4) - 10 * math.cos(t * 21 + i))
                   for t in [j / 40 for j in range(int(40 * p) + 1)]]
            if len(pts) > 1:
                dp.line(pts, fill=TINTA + (int(a0),), width=3)
            dp.line([(cx - 80, yf + 30), (cx + 80, yf + 30)], fill=TINTA + (int(a0 * .5),), width=1)
            pod = max(0.0, dt - mk[n] - .9 - .25 * i)                         # la carne se pudre: no para de crecer
            if pod > 0:
                r = min(70, 14 + 26 * pod)
                for j in range(3):
                    ox, oy = 26 * math.sin(i * 3 + j * 2.1), 14 * math.cos(i * 5 + j)
                    dm.ellipse((cx + ox - r * .7, yf + oy - r * .5, cx + ox + r * .7, yf + oy + r * .5),
                               fill=CARMIN + (int(min(150, 60 + 50 * pod)),))
        pap.alpha_composite(manchas.filter(ImageFilter.GaussianBlur(6)))
        u_s = _eo((dt - mk[n + 1]) / .35)
        if u_s > 0:
            sello = Image.new("RGBA", (560, 170), (0, 0, 0, 0))
            ds = ImageDraw.Draw(sello)
            ds.rounded_rectangle((8, 8, 552, 162), 12, outline=CARMIN + (230,), width=8)
            _texto(ds, (280, 88), remate.upper(), fs, CARMIN, "mm", 235, track=4, sombra=False)
            esc = 1.7 - .7 * u_s
            sello = sello.resize((int(560 * esc), int(170 * esc))).rotate(-9, expand=True)
            sa = np.array(sello)
            sa[..., 3] = (sa[..., 3] * u_s).astype(np.uint8)
            sello = Image.fromarray(sa)
            pap.alpha_composite(sello, (int((x0 + x1) / 2 + 150 - sello.width / 2), int(y0 + 345 - sello.height / 2)))
        im.alpha_composite(pap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def contagio(nombres, centro="La flor", remate=None, titulo="Lo que pudrió una flor", w=1500, h=660):
    """Flor escarlata al centro que late; un nombre por marca en el anillo: una vena roja sale de la flor y lo tiñe
    (pergamino -> carmín). Con `remate`, la última marca + 1 lo enciende abajo en ámbar."""
    fn_, ftit, fr = fuente("r", 46), fuente("r", 40), fuente("r", 58)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 1)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 285
        pts = [(M + 110 + (w - 220) * (i + .5) / n, M + 505 + 22 * math.sin(i * 1.9)) for i in range(n)]
        venas = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dv = ImageDraw.Draw(venas)
        tocados = 0
        for i, (x, y) in enumerate(pts):
            u = _eo((dt - mk[i]) / .7)
            tocados += u > .5
            if u > 0:
                mx, my = (cx + x) / 2 + 40 * math.sin(i * 2.3), (cy + y) / 2 + 30
                seg = [(cx + (mx - cx) * t * 2, cy + (my - cy) * t * 2) if t < .5 else
                       (mx + (x - mx) * (t - .5) * 2, my + (y - my) * (t - .5) * 2) for t in [j / 30 for j in range(int(30 * u) + 1)]]
                if len(seg) > 1:
                    dv.line(seg, fill=CARMIN + (int(230 * u),), width=6)
        im.alpha_composite(_brillo(venas, 8, 1.4))
        d = ImageDraw.Draw(im)
        for i, (x, y) in enumerate(pts):
            u = _eo((dt - mk[i]) / .7)
            ua = _eo((dt - .12 * i) / .5)
            col = tuple(int(PERGAMINO[c] + (CARMIN[c] - PERGAMINO[c]) * u) for c in range(3))
            r = 9 + 5 * u * (1 + math.sin(dt * 5 + i))
            d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(255 * ua),))
            _texto(d, (x, y + 22), nombres[i], fn_, col, "mt", 255 * ua)
        flor = Image.new("RGBA", im.size, (0, 0, 0, 0))
        lat = 1 + .06 * math.sin(dt * 3.2) + .04 * tocados
        _petalos(ImageDraw.Draw(flor), cx, cy, 78 * lat, _eo(dt / 1.2), CARMIN, a0, giro=dt * .15)
        im.alpha_composite(_brillo(flor, 14, 1.5))
        d = ImageDraw.Draw(im)
        _texto(d, (cx + 120, cy - 20), centro, fuente("i", 38), AMBAR, "lm", a0)
        if remate:
            u_r = _eo((dt - mk[n]) / .6)
            if u_r > 0:
                t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
                _texto(ImageDraw.Draw(t2), (cx, M + h - 40), remate.upper(), fr, AMBAR, "mm", 255 * u_r, track=8, sombra=False)
                im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def floraciones(etiquetas, final="Diosa de la putrefacción", titulo="Las tres flores", w=1500, h=600):
    """Tres capullos en fila. Marca k (k < 2) abre la flor k con su etiqueta; la marca 2 enciende el tercero en rojo, que
    late cada vez más grande con `final` debajo (lo que pasaría con la tercera flor)."""
    fe, ftit, ff = fuente("r", 42), fuente("r", 40), fuente("b", 50)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        flor = Image.new("RGBA", im.size, (0, 0, 0, 0))
        df = ImageDraw.Draw(flor)
        for i in range(3):
            cx, cy = M + w * (i + .5) / 3, M + 280
            u = _eo((dt - mk[i]) / .9)
            ua = _eo((dt - .15 * i) / .5)
            if i < 2:
                _petalos(df, cx, cy, 95, u, CARMIN if u > 0 else ORO_OSC, 255 * ua * (.45 + .55 * max(u, .0)), giro=i)
                txt = f"{i + 1}.ª · {etiquetas[i]}" if u > 0 else f"{i + 1}.ª"
                _texto(d, (cx, cy + 135), txt, fe, PERGAMINO if u > 0 else GRIS, "mt", 255 * ua)
            else:
                lat = (1 + .10 * math.sin(dt * (4 + 3 * u))) * (1 + .35 * u)
                col = ROJO if u > 0 else ORO_OSC
                _petalos(df, cx, cy, 95 * lat, .25 + .75 * u, col, 255 * ua * (.45 + .55 * u), giro=dt * .3 * u)
                _texto(d, (cx, cy + 135), "3.ª · ?" if u <= 0 else "3.ª", fe, GRIS if u <= 0 else ROJO, "mt", 255 * ua)
                if u > 0:
                    _texto(d, (M + w / 2, M + h - 40), final.upper(), ff, ROJO, "mm", 255 * u, track=4)
        im.alpha_composite(_brillo(flor, 12, 1.4))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def repudio(madre, hijas, titulo="Las hijas de la flor", remate="Como hizo tu madre", w=1500, h=640):
    """`madre` arriba unida por hilos dorados a cada hija (entran escalonadas desde la marca 0). Marca 1: los hilos se
    tiñen de rojo y se parten por la mitad, y aparece `remate`. Marca 2 (opcional): la primera hija se enciende en ámbar."""
    fn_, fs, ftit, fr = fuente("r", 46), fuente("i", 32), fuente("r", 40), fuente("i", 44)
    n = len(hijas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        mx, my = M + w / 2, M + 170
        corte = _eo((dt - mk[1]) / .6)
        luz = _eo((dt - mk[2]) / .6)
        hil = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(hil)
        for i, (nom, sub) in enumerate(hijas):
            hx, hy = M + 120 + (w - 240) * (i + .5) / n, M + 430
            u = _eo((dt - mk[0] - .25 * i) / .6)
            col = tuple(int(ORO[c] + (ROJO[c] - ORO[c]) * corte) for c in range(3))
            if corte < .05:
                _linea(dh, (mx, my + 16), (hx, hy - 16), u, col, 230 * u, 3)
            else:
                g = 40 * corte
                vx, vy = hx - mx, hy - my
                L = math.hypot(vx, vy)
                ux, uy = vx / L, vy / L
                medio = (mx + vx / 2, my + vy / 2)
                dh.line([(mx, my + 16), (medio[0] - ux * g, medio[1] - uy * g - 10 * corte)], fill=col + (230,), width=3)
                dh.line([(medio[0] + ux * g, medio[1] + uy * g + 18 * corte), (hx, hy - 16)], fill=col + (int(230 * (1 - .5 * corte)),), width=3)
            c_h = AMBAR if (i == 0 and luz > .5) else PERGAMINO
            _nodo(d, hx, hy, nom, sub, c_h, 255 * u, fn_, fs, abajo=True)
        im.alpha_composite(_brillo(hil, 6, 1.3))
        d = ImageDraw.Draw(im)
        _nodo(d, mx, my, madre, None, CARMIN if corte > .5 else ORO, a0, fuente("b", 54), fs)
        if corte > 0:
            _texto(d, (mx, M + h - 46), f"«{remate}»", fr, ROJO, "mm", 255 * corte)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn



# ------------------------------------------------------------------ er_melina_atrocidades (27-oct-2026)
def acuerdo(da, pides, letra=None, titulo="El acuerdo", remate="Deber", w=1500, h=660, cab=("Ella te da", "Tú la llevas")):
    """El trato de Melina como un contrato de dos columnas: «Ella te da» (una línea por marca, con un rombo dorado) y
    «Tú la llevas» (marca len(da)). Con `letra`, la marca siguiente hace crecer la letra pequeña abajo en rojo, los
    regalos se tiñen de carmín (eran un préstamo) y la siguiente estampa el sello `remate`. Pensado para salir dos veces.
    `cab` = las dos cabeceras de columna (19-nov-2026, Godfrey: «Ella os da» / «Vosotros pagáis»)."""
    ftit, fc = fuente("r", 40), fuente("r", 42)
    fs = fuente("b", 60)
    n = len(da)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        xm = M + w * .60
        d.line([(xm, M + 120), (xm, M + h - 170)], fill=ORO_OSC + (int(a0 * .7),), width=2)
        _texto(d, (M + 80, M + 130), cab[0].upper(), fuente("r", 32), GRIS, "lm", a0, track=4)
        _texto(d, (xm + 50, M + 130), cab[1].upper(), fuente("r", 32), GRIS, "lm", a0, track=4)
        u_l = _eo((dt - mk[n + 1]) / .9) if letra else 0.0
        for k, s in enumerate(da):
            u = _eo((dt - mk[k]) / .5)
            if u <= 0:
                continue
            y = M + 200 + 70 * k
            col = tuple(int(ORO[c] + (CARMIN[c] - ORO[c]) * u_l) for c in range(3))
            cx = M + 98 - 30 * (1 - u)
            d.polygon([(cx, y - 14), (cx + 12, y), (cx, y + 14), (cx - 12, y)], fill=col + (int(255 * u * (.78 + .22 * math.sin(dt * 2.4 + k))),))
            _texto(d, (cx + 34, y), s, fc, PERGAMINO if u_l < .5 else (236, 196, 188), "lm", 255 * u)
        u_p = _eo((dt - mk[n]) / .6)
        if u_p > 0:
            for j, ln in enumerate(_partir(d, pides, fc, w * .34)):
                _texto(d, (xm + 50, M + 210 + 56 * j), ln, fc, AMBAR, "lm", 255 * u_p)
        if letra and u_l > 0:
            esc = .35 + .65 * u_l
            f2 = fuente("i", max(12, int(48 * esc)))
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d2 = ImageDraw.Draw(t2)
            lineas = _partir(d2, letra, f2, w - 200)
            for j, ln in enumerate(lineas):
                yl = M + h - 110 + (j - (len(lineas) - 1) / 2) * 48 * esc
                _texto(d2, (M + w / 2, yl), ln, f2, ROJO, "mm", 255 * u_l)
            im.alpha_composite(_brillo(t2, 8, 1.2 + .4 * math.sin(dt * 4)))
            u_s = _eo((dt - mk[n + 2]) / .35)
            if u_s > 0:
                sello = Image.new("RGBA", (420, 150), (0, 0, 0, 0))
                ds = ImageDraw.Draw(sello)
                ds.rounded_rectangle((8, 8, 412, 142), 12, outline=CARMIN + (235,), width=8)
                _texto(ds, (210, 76), remate.upper(), fs, CARMIN, "mm", 240, track=6, sombra=False)
                e = 1.7 - .7 * u_s
                sello = sello.resize((int(420 * e), int(150 * e))).rotate(8, expand=True)
                sa = np.array(sello)
                sa[..., 3] = (sa[..., 3] * u_s).astype(np.uint8)
                sello = Image.fromarray(sa)
                im.alpha_composite(sello, (int(M + w * .34 - sello.width / 2), int(M + 430 - sello.height / 2)))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def ecos(lineas, firma="una desconocida", revela="su madre", titulo="Palabras de una reina que desapareció", w=1500, h=640):
    """Los ecos de Márika que Melina recita: la marca k escribe la línea k en cursiva (las anteriores se apagan) con el
    Círculo de Elden girando tenue detrás; abajo firma «— `firma`». La marca len(lineas) tacha la firma y escribe
    «— `revela`» en carmín, que late."""
    ftit, fl, ff = fuente("r", 40), fuente("i", 50), fuente("i", 46)
    n = len(lineas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w / 2, M + h / 2 + 10
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(halo)
        for i, r in enumerate((210, 160)):
            g = dt * (.12 if i else -.08)
            for k in range(24):
                t0 = math.degrees(g + 2 * math.pi * k / 24)
                dh.arc((cx - r, cy - r, cx + r, cy + r), t0, t0 + 9, fill=ORO + (int(a0 * .22),), width=3)
        dh.line([(cx, cy - 250), (cx, cy + 250)], fill=ORO + (int(a0 * .16),), width=3)
        im.alpha_composite(_brillo(halo, 6, 1.2))
        d = ImageDraw.Draw(im)
        _texto(d, (cx, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=5)
        _filete(d, cx, M + 80, w * .3, alfa=a0)
        actual = max([k for k in range(n) if dt >= mk[k]] or [-1])
        y = M + 150
        for k, s in enumerate(lineas):
            u = _eo((dt - mk[k]) / 1.0)
            if u <= 0:
                continue
            a = 255 * u * (1.0 if k == actual else .42)
            for ln in _partir(d, s, fl, w - 220):
                vis = ln[:int(len(ln) * min(1, u * 1.4) + .999)]
                _texto(d, (cx, y), vis, fl, PERGAMINO, "mm", a)
                y += 60
            y += 18
        u_r = _eo((dt - mk[n]) / .7)
        yf = M + h - 60
        f1 = "— " + firma
        wf = d.textlength(f1, font=ff)
        _texto(d, (M + w - 110, yf), f1, ff, GRIS, "rm", a0 * (1 - .55 * u_r))
        if u_r > 0:
            d.line([(M + w - 110 - wf * u_r, yf + 2), (M + w - 110, yf + 2)], fill=ROJO + (230,), width=4)
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            f3 = fuente("b", int(58 * (1 + .08 * math.sin(dt * 4))))
            _texto(ImageDraw.Draw(t2), (M + w - 110, yf - 64), "— " + revela.upper(), f3, CARMIN, "rm", 255 * u_r, track=4, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _llama(d, x, y, alto, ancho, t, fase, a):
    """Lengua de fuego: polígono que ondula (base ancha, punta fina); naranja por fuera, ámbar y blanco dentro."""
    if a <= 0 or alto < 4:
        return
    for capa, (col, k) in enumerate((((230, 92, 30), 1.0), (AMBAR, .62), ((255, 236, 170), .32))):
        izq, der = [], []
        for j in range(13):
            v = j / 12
            o1 = math.sin(t * 7 + fase + v * 5) * ancho * .25 * v
            o2 = math.sin(t * 7 + fase + v * 5 + 1.3) * ancho * .25 * v
            izq.append((x - ancho * k * (1 - v) ** .8 + o1, y - alto * k * v))
            der.append((x + ancho * k * (1 - v) ** .8 + o2, y - alto * k * v))
        d.polygon(izq + der[::-1], fill=col + (int(a * (.85 - .15 * capa)),))


def arbol_arde(etapas, titulo="El pecado capital", w=1500, h=760):
    """El Árbol Áureo por código (tronco y ramas doradas + copa de luces que respiran) sobre la silueta de la capital.
    Marca 0: la llama llega al pie · 1: el fuego trepa por el tronco · 2: la copa entera arde · 3: el árbol se apaga y
    llueve ceniza. Cada marca escribe su etiqueta a la izquierda (la vigente en ámbar; la de la ceniza en gris claro)."""
    ftit, fe = fuente("r", 40), fuente("r", 40)
    rng = np.random.default_rng(7)
    ramas = []

    def _crece(x, y, ang, largo, g, prof):
        x1, y1 = x + math.cos(ang) * largo, y - math.sin(ang) * largo
        ramas.append((x, y, x1, y1, g))
        if prof:
            for s in (-1, 1):
                _crece(x1, y1, ang + s * (.38 + .2 * rng.random()), largo * (.70 + .08 * rng.random()), max(2, g * .62), prof - 1)
    _crece(0, 0, math.pi / 2, 140, 24, 6)
    hojas = [(float(rng.normal(0, 170)), float(-290 - abs(rng.normal(0, 110))), float(rng.random() * 6.28)) for _ in range(150)]
    ceniza = [(float(rng.random()), float(rng.random()), float(.4 + rng.random())) for _ in range(140)]
    edif = [(-.36, .07, .05), (-.26, .10, .08), (-.15, .06, .05), (.13, .08, .06), (.23, .11, .09), (.33, .06, .04)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 5
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        bx, by = M + w * .63, M + h - 90
        u0 = _eo((dt - mk[0]) / .8)
        u1, u2 = _eo((dt - mk[1]) / 1.4), _eo((dt - mk[2]) / 1.4)
        apag = _eo((dt - mk[3]) / 1.0)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(cap)
        for x, ew, eh in edif:
            ex, ew, eh = bx + x * w, ew * w * .5, eh * w * 1.6
            dc.rectangle((ex - ew / 2, by - eh, ex + ew / 2, by + 40), fill=(34, 30, 24, int(a0)))
            dc.polygon([(ex - ew / 2, by - eh), (ex, by - eh - ew * .7), (ex + ew / 2, by - eh)], fill=(34, 30, 24, int(a0)))
        im.alpha_composite(cap)
        arb = Image.new("RGBA", im.size, (0, 0, 0, 0))
        da = ImageDraw.Draw(arb)
        col_t = tuple(int(ORO[c] * (1 - apag) + 64 * apag) for c in range(3))
        for x0, y0, x1, y1, g in ramas:
            da.line([(bx + x0, by + y0), (bx + x1, by + y1)], fill=col_t + (int(a0 * .95),), width=max(1, int(g)))
        for x, y, f in hojas:
            r = 5 + 3 * math.sin(dt * 2 + f)
            col = tuple(int(ORO[c] * (1 - u2) + (232, 96, 30)[c] * u2) for c in range(3))
            al = a0 * (.55 + .3 * math.sin(dt * 1.7 + f)) * (1 - apag)
            da.ellipse((bx + x - r, by + y - r, bx + x + r, by + y + r), fill=col + (int(max(0, al)),))
        im.alpha_composite(_brillo(arb, 12, 1.5 * (1 - .7 * apag)))
        fue = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dfu = ImageDraw.Draw(fue)
        vivo = 1 - apag
        if u0 > 0 and vivo > 0:
            _llama(dfu, bx, by + 6, 80 * u0, 36, dt, 0, 255 * u0 * vivo)
        if u1 > 0 and vivo > 0:
            for k in range(7):
                v = k / 6
                if v <= u1:
                    _llama(dfu, bx + 10 * math.sin(k * 2.1), by - 30 - 220 * v, 60 + 30 * u1, 22, dt, k, 230 * vivo)
        if u2 > 0 and vivo > 0:
            for x, y, f in hojas:
                r = (10 + 8 * math.sin(dt * 5 + f)) * u2
                dfu.ellipse((bx + x - r, by + y - r * 1.3, bx + x + r, by + y + r * .7), fill=(236, 104, 34, int(170 * u2 * vivo)))
            for x, y, f in hojas[::9]:
                _llama(dfu, bx + x, by + y + 16, 46 * u2, 16, dt, f, 200 * u2 * vivo)
        im.alpha_composite(_brillo(fue.filter(ImageFilter.GaussianBlur(2.5)), 12, 1.7))
        if apag > 0:
            cz = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dz = ImageDraw.Draw(cz)
            for x, y, v in ceniza:
                yy = M + 100 + ((y + (dt - mk[3]) * .09 * v) % 1.0) * (h - 140)
                xx = M + 60 + x * (w - 120) + 18 * math.sin(dt + y * 9)
                dz.ellipse((xx - 3, yy - 3, xx + 3, yy + 3), fill=(205, 198, 186, int(200 * apag)))
            im.alpha_composite(cz.filter(ImageFilter.GaussianBlur(1)))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        vig = max([k for k in range(len(etapas)) if dt >= mk[k]] or [-1])
        for k, s in enumerate(etapas):
            u = _eo((dt - mk[k]) / .5)
            if u <= 0:
                continue
            y = M + 170 + 90 * k
            col = (AMBAR if k < 3 else (215, 208, 196)) if k == vig else GRIS
            _texto(d, (M + 80 - 30 * (1 - u), y), s, fe, col, "lm", 255 * u)
            d.line([(M + 80, y + 30), (M + 80 + 330 * u, y + 30)], fill=ORO_OSC + (int(150 * u),), width=1)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def muerte_suelta(nombres, titulo="La Runa de la Muerte", remate="Indiscriminada", w=1500, h=660):
    """La Runa de la Muerte (hoja negra con filo rojo que late) presa en un anillo de eslabones dorados (el sello de
    Maliketh). Marca 0: «arrancada del Orden Áureo» · marca 1: los eslabones se rompen uno a uno («sello roto») · marca
    2: ondas negras y rojas se expanden, cada nombre de la fila de abajo se apaga en gris y se tacha, y sale `remate`."""
    ftit, fn_, fr, fs = fuente("r", 40), fuente("r", 42), fuente("b", 62), fuente("i", 34)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w / 2, M + 270
        u0, u1, u2 = _eo((dt - mk[0]) / .6), _eo((dt - mk[1]) / 1.2), _eo((dt - mk[2]) / 1.6)
        if u2 > 0:
            onda = Image.new("RGBA", im.size, (0, 0, 0, 0))
            do = ImageDraw.Draw(onda)
            for k in range(3):
                r = (u2 * 900 + (dt - mk[2]) * 60 - k * 140) % 1000
                do.ellipse((cx - r, cy - r * .7, cx + r, cy + r * .7), outline=(150, 20, 30, int(170 * (1 - r / 1000))), width=14)
            im.alpha_composite(onda.filter(ImageFilter.GaussianBlur(10)))
        hoja = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(hoja)
        lat = 1 + .05 * math.sin(dt * 3)
        L, A = 205 * lat, 36 * lat
        dh.polygon([(cx, cy - L), (cx + A, cy - L * .2), (cx + A * .6, cy + L * .6), (cx, cy + L),
                    (cx - A * .6, cy + L * .6), (cx - A, cy - L * .2)], fill=(18, 10, 12, int(a0)), outline=(190, 40, 50, int(a0)))
        dh.line([(cx - 70, cy - L * .25), (cx + 70, cy - L * .25)], fill=(190, 40, 50, int(a0)), width=5)
        im.alpha_composite(_brillo(hoja, 16, 1.6 + .8 * u2))
        cad = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dk = ImageDraw.Draw(cad)
        R, nb = 230, 28
        for k in range(nb):
            t = 2 * math.pi * k / nb + dt * .05
            x, y = cx + math.cos(t) * R, cy + math.sin(t) * R * .62
            orden = ((k * 11) % nb) / nb
            if dt >= mk[1] + orden * 1.2:                          # eslabón roto: sale volando y se apaga
                v = min(1.0, (dt - mk[1] - orden * 1.2) / .9)
                x, y = x + math.cos(t) * 160 * v, y + math.sin(t) * 110 * v + 60 * v * v
                a = a0 * (1 - v)
                if a > 4:
                    dk.ellipse((x - 13, y - 8, x + 13, y + 8), outline=ROJO + (int(a),), width=4)
                continue
            dk.ellipse((x - 13, y - 8, x + 13, y + 8), outline=ORO + (int(a0),), width=4)
        im.alpha_composite(_brillo(cad, 5, 1.1))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        if u0 > 0:
            _texto(d, (cx + 280, cy - 60), "arrancada del", fs, GRIS, "lm", 255 * u0 * (1 - .6 * u2))
            _texto(d, (cx + 280, cy - 18), "Orden Áureo", fuente("r", 44), ORO, "lm", 255 * u0 * (1 - .6 * u2))
        if u1 > 0:
            _texto(d, (cx - 280, cy - 40), "sello roto", fuente("i", 44), ROJO, "rm", 255 * u1 * (1 - .6 * u2))
        for i, s in enumerate(nombres):
            x, y = M + 120 + (w - 240) * (i + .5) / n, M + h - 130
            ua = _eo((dt - .1 * i) / .5)
            g = _eo(u2 * 1.6 - i / max(1, n) * .6)
            col = tuple(int(PERGAMINO[c] * (1 - g) + 96 * g) for c in range(3))
            _texto(d, (x, y), s, fn_, col, "mm", 255 * ua)
            if g > .4:
                wl = d.textlength(s, font=fn_) / 2 + 10
                d.line([(x - wl, y + 4), (x - wl + 2 * wl * min(1, (g - .4) / .6), y + 4)], fill=(170, 30, 40, 220), width=4)
        if u2 > .5:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (cx, M + h - 46), remate.upper(), fr, (210, 46, 56), "mm", 255 * _eo((u2 - .5) * 2),
                   track=8, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.8))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_radahn_atrocidades (28-oct-2026)
def cien(titulo, encendidos, remate=None, w=1240):
    """100 estrellas apagadas que aparecen en barrido desde la marca 0; en la marca 1 se encienden `encendidos`, repartidas;
    remate = (texto, i_marca) en ámbar abajo. Para «de cada 100 que ven el canal, solo N…» (mismo uso que mg_tes.rejilla)."""
    n, cols, P = 100, 20, 56
    h = 150 + 5 * P + (100 if remate else 30)
    vivas = {int(round((k + .5) * n / encendidos + 7)) % n for k in range(encendidos)}
    ftit, fr = fuente("r", 40), fuente("i", 64)

    def fn(dt, dur, marcas):
        t0 = marcas[0] if marcas else .3
        t1 = marcas[1] if len(marcas) > 1 else t0 + 2
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        x0, y0 = M + (w - (cols - 1) * P) / 2, M + 135
        txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(txt)
        for i in range(n):
            r, c = divmod(i, cols)
            u = _eo((dt - t0 - (r + c) * .025) / .25)
            v = _eo((dt - t1) / .35) if i in vivas else 0
            _estrella(d, x0 + c * P, y0 + r * P, 17, GRIS, 140 * u * (1 - v))
            _estrella(dd, x0 + c * P, y0 + r * P, 17 + 5 * v, ORO, 255 * v)
        im.alpha_composite(_brillo(txt, 10, 1.6))
        if remate and len(marcas) > remate[1] and dt >= marcas[remate[1]]:
            a = 255 * _eo((dt - marcas[remate[1]]) / .4)
            _texto(ImageDraw.Draw(im), (M + w / 2, M + h - 56), remate[0], fr, AMBAR, "mm", a)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _lanza(d, x0, y0, x1, y1, color, a, ancho=5):
    """Asta de (x0,y0) a la punta (x1,y1), con punta triangular."""
    if a <= 0:
        return
    d.line([(x0, y0), (x1, y1)], fill=color + (int(a),), width=ancho)
    ang = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1 + math.cos(ang) * 22, y1 + math.sin(ang) * 22),
               (x1 + math.cos(ang + 2.5) * 13, y1 + math.sin(ang + 2.5) * 13),
               (x1 + math.cos(ang - 2.5) * 13, y1 + math.sin(ang - 2.5) * 13)], fill=color + (int(a),))


def lanzas(bando="Caballeros de Malenia", centro="Radahn", tu="Tú", titulo="Las lanzas del festival", n=7, w=1500, h=640):
    """Marca 0: las lanzas de `bando` (izquierda, plata) vuelan y se clavan en el león rojo del centro · marca 1: salen
    girando en rojo, con halo violeta de gravedad, y vuelan hacia `tu` (derecha) como flechas."""
    ftit, fn_, fs = fuente("r", 40), fuente("r", 44), fuente("i", 34)
    rng = np.random.default_rng(3)
    angs = [(-.55 + 1.1 * k / (n - 1)) + float(rng.normal(0, .05)) for k in range(n)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 3
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w * .5, M + h * .56
        ox, tx = M + 150, M + w - 150
        u0, u1 = dt - mk[0], dt - mk[1]
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(cap)
        lat = 1 + .03 * math.sin(dt * 2.4)
        for k in range(40):                                           # la melena roja del león
            t = 2 * math.pi * k / 40
            r0, r1 = 78 * lat, (118 + 14 * math.sin(k * 1.7 + dt * 3)) * lat
            dc.line([(cx + math.cos(t) * r0, cy + math.sin(t) * r0), (cx + math.cos(t) * r1, cy + math.sin(t) * r1)],
                    fill=(196, 58, 36, int(a0 * .9)), width=6)
        dc.ellipse((cx - 80, cy - 80, cx + 80, cy + 80), fill=(24, 18, 14, int(a0)), outline=ORO + (int(a0),), width=3)
        im.alpha_composite(_brillo(cap, 14, 1.2))
        lz = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lz)
        for k, ang in enumerate(angs):
            lag = k * .12
            v0 = _eo((u0 - lag) / .55)
            if v0 <= 0:
                continue
            px, py = cx - math.cos(ang) * 92, cy + math.sin(ang) * 92           # punta clavada
            bx, by = px - math.cos(ang) * 210, py + math.sin(ang) * 210         # cola
            sx, sy = ox - 40, cy + math.sin(ang) * 260                           # de dónde sale
            v1 = _eo((u1 - lag * .6) / .9)
            if v1 <= 0:
                x1, y1 = sx + (px - sx) * v0, sy + (py - sy) * v0
                _lanza(dl, x1 - (px - bx), y1 - (py - by), x1, y1, (200, 204, 212), a0 * min(1, v0 * 2))
            else:
                gx, gy = tx - 40, cy + (k - (n - 1) / 2) * 34
                hx, hy = cx + math.cos(ang) * 120, cy - math.sin(ang) * 70
                x1, y1 = hx + (gx - hx) * v1, hy + (gy - hy) * v1
                ang2 = math.atan2(y1 - cy, x1 - (cx - 200))
                _lanza(dl, x1 - math.cos(ang2) * 200, y1 - math.sin(ang2) * 200, x1, y1, (214, 70, 50),
                       a0 * (1 - .7 * max(0, v1 - .85) / .15))
        if u1 > 0:
            ha = np.array(lz.filter(ImageFilter.GaussianBlur(9)))
            ha[..., :3] = (150, 90, 230)
            im.alpha_composite(Image.fromarray(ha))
        im.alpha_composite(lz)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        _texto(d, (cx, cy + 150), centro, fn_, ORO, "mt", a0)
        ua, ub = _eo(u0 / .5), _eo(u1 / .5)
        if ua > 0:
            _texto(d, (ox + 60, M + h - 60), bando, fs, (200, 204, 212), "mm", 255 * ua)
        if ub > 0:
            _texto(d, (tx - 60, M + h - 60), "Ahora, flechas contra ti", fs, (214, 70, 50), "mm", 255 * ub)
            _nodo(d, tx, cy, tu, None, PERGAMINO, 255 * ub, fn_, fs)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cielo_sujeto(atados, quien="Radahn", remate="Las estrellas vuelven a moverse", titulo="El cielo sujeto", w=1500, h=700):
    """Cielo de estrellas QUIETO. Cada marca ata con un hilo violeta de gravedad a `quien` (abajo) una estrella con su
    etiqueta (lo que su victoria congeló). Marca len(atados): `quien` se tacha, los hilos se rompen en rojo, el cielo empieza
    a girar y cae una estrella grande con estela; sale `remate`."""
    ftit, fe, fq, fr = fuente("r", 40), fuente("r", 36), fuente("r", 46), fuente("i", 46)
    rng = np.random.default_rng(11)
    fondo = [(float(rng.random()), float(rng.random()) * .72, float(.6 + rng.random() * 1.6), float(rng.random() * 6.28))
             for _ in range(160)]
    n = len(atados)
    pos = [(.17 + .66 * (i / max(1, n - 1)), .26 + .10 * (i % 2)) for i in range(n)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        fin = dt - mk[n]
        suelta = _eo(fin / 1.0)
        giro = fin ** 1.6 * .05 if fin > 0 else 0.0
        qx, qy = M + w / 2, M + h - 130
        cx0, cy0 = M + w / 2, M + h * .95
        st = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(st)
        for x, y, r, f in fondo:
            px, py = M + 40 + x * (w - 80), M + 110 + y * (h - 200)
            if giro:
                ang = giro * (1.2 - y)
                dx, dy = px - cx0, py - cy0
                px, py = cx0 + dx * math.cos(ang) - dy * math.sin(ang), cy0 + dx * math.sin(ang) + dy * math.cos(ang)
            if M + 90 < py < M + h - 30 and M + 20 < px < M + w - 20:
                ds.ellipse((px - r, py - r, px + r, py + r), fill=(230, 226, 240, int(a0 * (.45 + .3 * math.sin(dt * 1.3 + f)))))
        im.alpha_composite(st)
        hl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(hl)
        for i in range(n):
            u = _eo((dt - mk[i]) / .7)
            if u <= 0:
                continue
            sx, sy = M + pos[i][0] * w, M + pos[i][1] * h + 40
            col = tuple(int((170, 120, 250)[c] * (1 - suelta) + ROJO[c] * suelta) for c in range(3))
            al = 255 * u * (1 - suelta)
            if al > 2:
                for j in range(3):                                     # hilo tenso que vibra
                    off = math.sin(dt * 9 + i + j) * 2
                    _linea(dh, (qx + off, qy - 30), (sx + off, sy), u, col, al * (.6 if j else 1), 3 if j == 0 else 1)
            r = 13 + 2 * math.sin(dt * 2 + i)
            dh.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(250, 244, 255, int(255 * u)))
        im.alpha_composite(_brillo(hl, 10, 1.6))
        d = ImageDraw.Draw(im)
        for i, s in enumerate(atados):
            u = _eo((dt - mk[i]) / .7)
            if u > 0:
                sx, sy = M + pos[i][0] * w, M + pos[i][1] * h + 40
                _texto(d, (sx, sy - 30), s, fe, PERGAMINO, "mb", 255 * u)
        cq = tuple(int(ORO[c] * (1 - suelta) + 90 * suelta) for c in range(3))
        d.ellipse((qx - 26, qy - 26, qx + 26, qy + 26), fill=(20, 14, 10, int(a0)), outline=cq + (int(a0),), width=4)
        _texto(d, (qx, qy + 40), quien, fq, cq, "mt", a0)
        if suelta > 0:
            wl = d.textlength(quien, font=fq) / 2 + 10
            d.line([(qx - wl, qy + 66), (qx - wl + 2 * wl * suelta, qy + 66)], fill=ROJO + (230,), width=4)
            v = min(1.0, max(0.0, (fin - .4) / 1.8))                  # la estrella que cae
            if 0 < v < 1:
                ex, ey = M + w * (.86 - .55 * v), M + 120 + (h - 300) * v ** 1.4
                cola = Image.new("RGBA", im.size, (0, 0, 0, 0))
                dk = ImageDraw.Draw(cola)
                for k in range(18):
                    q = k / 18
                    rr = 14 * (1 - q)
                    dk.ellipse((ex + 120 * q - rr, ey - 90 * q - rr, ex + 120 * q + rr, ey - 90 * q + rr),
                               fill=(200, 160, 255, int(220 * (1 - q))))
                im.alpha_composite(_brillo(cola, 16, 2.0))
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + 60), remate, fr, AMBAR, "mm", 255 * _eo((fin - .3) / .6), sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.4))
        else:
            _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
            _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def balanza(izq, der, pesos, remate="Nunca lo sabremos", titulo="¿Aceptó?", w=1500, h=720):
    """Balanza dorada con dos platillos (`izq`, `der`). Marca k deja caer pesos[k] = ("i"|"d", texto) en su platillo (el
    texto se apila debajo) y el brazo se inclina según cuántas pruebas tiene cada lado. Marca len(pesos): el brazo vuelve
    al centro, las pruebas se atenúan y sale `remate` en ámbar."""
    ftit, fl, fp, fr = fuente("r", 40), fuente("b", 46), fuente("r", 30), fuente("i", 50)
    n = len(pesos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        cx, cy = M + w / 2, M + 210
        L = w * .29
        ni = sum(_eo((dt - mk[k]) / .6) for k, (l, _) in enumerate(pesos) if l == "i")
        nd = sum(_eo((dt - mk[k]) / .6) for k, (l, _) in enumerate(pesos) if l == "d")
        fin = _eo((dt - mk[n]) / 1.2)
        ang = max(-.2, min(.2, (nd - ni) * .07)) * (1 - fin) + .012 * math.sin(dt * 1.5)
        d = ImageDraw.Draw(im)
        d.line([(cx, cy), (cx, M + h - 70)], fill=ORO_OSC + (int(a0),), width=8)
        d.polygon([(cx - 70, M + h - 50), (cx + 70, M + h - 50), (cx, M + h - 95)], fill=ORO_OSC + (int(a0),))
        xi, yi = cx - math.cos(ang) * L, cy - math.sin(ang) * L
        xd, yd = cx + math.cos(ang) * L, cy + math.sin(ang) * L
        br = Image.new("RGBA", im.size, (0, 0, 0, 0))
        db = ImageDraw.Draw(br)
        db.line([(xi, yi), (xd, yd)], fill=ORO + (int(a0),), width=7)
        db.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=ORO + (int(a0),))
        for px, py in ((xi, yi), (xd, yd)):
            for s in (-1, 1):
                db.line([(px, py), (px + s * 110, py + 90)], fill=ORO_OSC + (int(a0),), width=2)
            db.chord((px - 125, py + 50, px + 125, py + 130), 0, 180, fill=(40, 32, 20, int(a0)), outline=ORO + (int(a0),), width=3)
        im.alpha_composite(_brillo(br, 6, 1.0))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        _texto(d, (xi, yi - 22), izq, fl, ORO, "mb", a0)
        _texto(d, (xd, yd - 22), der, fl, ORO, "mb", a0)
        cnt = {"i": 0, "d": 0}
        for k, (lado, s) in enumerate(pesos):
            u = _eo((dt - mk[k]) / .6)
            if u <= 0:
                continue
            j = cnt[lado]
            cnt[lado] += 1
            px, py = (xi, yi) if lado == "i" else (xd, yd)
            col = tuple(int(PERGAMINO[c] * (1 - .5 * fin)) for c in range(3))
            _texto(d, (px, py + 155 + 50 * j - 40 * (1 - u)), s, fp, col, "mt", 255 * u)
        if fin > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (cx, cy - 60), remate, fr, AMBAR, "mm", 255 * fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def espejo(padre=("Radagon", "dejó a Rennala"), hijo=("Radahn", "en un cuerpo prestado"), papel_padre="Consorte de Márika",
           papel_hijo="Consorte de Miquella", idolo="Godfrey", remate="De tal palo, tal astilla", titulo="El padre y el hijo",
           w=1500, h=640):
    """Dos filas en espejo. Marca 0: arriba, `padre` → caja `papel_padre` · marca 1: abajo, `hijo`, que de niño «soñaba con
    ser» `idolo` (se tacha), y su flecha llega a `papel_hijo` · marca 2: las dos cajas se encienden en ámbar unidas por un
    «=» y sale `remate`."""
    ftit, fn_, fs, fc, fr = fuente("r", 40), fuente("b", 48), fuente("i", 32), fuente("r", 40), fuente("i", 50)

    def caja(d, x, y, s, col, a):
        wl = d.textlength(s, font=fc) / 2 + 34
        d.rounded_rectangle((x - wl, y - 40, x + wl, y + 40), 14, fill=(26, 20, 14, int(a)), outline=col + (int(a),), width=3)
        _texto(d, (x, y), s, fc, col, "mm", a)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        u0, u1, u2 = _eo((dt - mk[0]) / .7), _eo((dt - mk[1]) / .7), _eo((dt - mk[2]) / .8)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        xa, xb = M + 210, M + w - 300
        ya, yb = M + 220, M + 450
        col_p = tuple(int(ORO[c] * (1 - u2) + AMBAR[c] * u2) for c in range(3))
        if u0 > 0:
            _nodo(d, xa, ya, padre[0], padre[1], ORO, 255 * u0, fn_, fs)
            _linea(d, (xa + 40, ya), (xb - 200, ya), u0, ORO_OSC, 255 * u0, 3)
            caja(d, xb, ya, papel_padre, col_p, 255 * u0)
        if u1 > 0:
            _nodo(d, xa, yb, hijo[0], hijo[1], ORO, 255 * u1, fn_, fs)
            mx = (xa + xb) / 2 - 70
            g = _eo((dt - mk[1] - .6) / .6)
            _texto(d, (mx, yb - 34), "soñaba con ser", fs, GRIS, "mb", 255 * u1)
            _texto(d, (mx, yb + 6), idolo, fn_, PERGAMINO, "mm", 255 * u1 * (1 - .5 * g))
            if g > 0:
                wl = d.textlength(idolo, font=fn_) / 2 + 10
                d.line([(mx - wl, yb + 10), (mx - wl + 2 * wl * g, yb + 10)], fill=ROJO + (230,), width=5)
                caja(d, xb, yb, papel_hijo, col_p, 255 * g)
        if u2 > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d2 = ImageDraw.Draw(t2)
            _texto(d2, (xb, (ya + yb) / 2), "=", fuente("b", 84), AMBAR, "mm", 255 * u2, sombra=False)
            _texto(d2, (M + w / 2, M + h - 40), remate, fr, AMBAR, "mm", 255 * u2, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.6))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn



# ================================================================== er_morgott_atrocidades (5-nov-2026)
def _cuernos(d, cx, cy, s, color, a, ancho=4):
    """Cabeza de augurio: óvalo con dos cuernos curvos y cuernecillos en la frente."""
    if a <= 0:
        return
    c = color + (int(a),)
    d.ellipse((cx - s * .55, cy - s * .7, cx + s * .55, cy + s * .7), outline=c, width=ancho)
    for sg in (-1, 1):
        pts = [(cx + sg * s * (.30 + .75 * math.sin(v * 2.2)), cy - s * (.40 + .95 * v - .35 * v * v)) for v in np.linspace(0, 1, 11)]
        d.line(pts, fill=c, width=ancho + 1)
        for j in range(3):
            x = cx + sg * s * (.12 + .1 * j)
            d.line([(x, cy - s * .62), (x + sg * s * .06, cy - s * .86)], fill=c, width=max(2, ancho - 1))


def dos_nombres(a=("Margit", "el Augurio Caído", "el portero del primer castillo"),
                b=("Morgott", "rey de los Augurios", "el último de todos los reyes"),
                remate="Siempre fue él", titulo="Dos nombres, un solo augurio", w=1500, h=640):
    """Marca 0: la carta de `a` (izq) · marca 1: la de `b` (der) · marca 2: las dos se deslizan al centro y se funden en
    una sola (la de `a` se deshace como su capa raída), la cabeza con cuernos brilla y sale `remate` en ámbar."""
    ftit, fn_, fs, fd, fr = fuente("r", 40), fuente("b", 64), fuente("i", 34), fuente("r", 30), fuente("i", 54)
    rng = np.random.default_rng(11)
    grano = rng.random((h // 8 + 14, w // 8 + 14))

    def carta(im, cx, cy, nom, sub, desc, a_, col):
        if a_ <= 0:
            return
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((cx - 270, cy - 200, cx + 270, cy + 200), 18, fill=(20, 16, 11, int(a_ * .92)),
                            outline=col + (int(a_),), width=3)
        _cuernos(d, cx, cy - 70, 78, col, a_, 4)
        _texto(d, (cx, cy + 40), nom, fn_, col, "mm", a_)
        _texto(d, (cx, cy + 95), sub, fs, PERGAMINO, "mm", a_)
        _texto(d, (cx, cy + 145), desc, fd, GRIS, "mm", a_)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        u0, u1, u2 = _eo((dt - mk[0]) / .6), _eo((dt - mk[1]) / .6), _eo((dt - mk[2]) / 1.1)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cy = M + h * .55
        xa = M + w * .27 + (w * .23) * u2
        xb = M + w * .73 - (w * .23) * u2
        if u0 > 0:                                                    # Margit, que se deshace en la fusión
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            carta(capa, xa, cy, *a, 255 * u0, GRIS if u2 > .5 else PERGAMINO)
            if u2 > 0:
                g = np.array(Image.fromarray((grano * 255).astype(np.uint8)).resize(capa.size, Image.NEAREST)) / 255.0
                arr = np.array(capa)
                arr[..., 3] = (arr[..., 3] * (g > u2 * 1.05)).astype(np.uint8)
                capa = Image.fromarray(arr)
            im.alpha_composite(capa)
        if u1 > 0:
            col = tuple(int(ORO[c] * (1 - u2) + AMBAR[c] * u2) for c in range(3))
            carta(im, xb, cy, *b, 255 * u1, col)
        if u1 > 0 and u2 < .3:
            _texto(ImageDraw.Draw(im), (M + w / 2, cy), "?", fuente("b", 90), GRIS, "mm", 255 * u1 * (1 - u2 / .3))
        if u2 > .6:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            k = (u2 - .6) / .4
            _cuernos(ImageDraw.Draw(t2), M + w / 2, cy - 70, 78 + 4 * math.sin(dt * 3), AMBAR, 255 * k, 5)
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 34), remate, fr, AMBAR, "mm", 255 * k, sombra=False)
            im.alpha_composite(_brillo(t2, 12, 1.6))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _cuerpo(d, cx, cy, L, ang, color, a):
    """Cuerpo caído: rectángulo girado + cabeza."""
    if a <= 0:
        return
    ca, sa = math.cos(ang), math.sin(ang)
    hw, hh = L / 2, L * .13
    pts = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
    d.polygon(pts, fill=(36, 30, 24, int(a)), outline=color + (int(a * .8),))
    hx, hy = cx + (hw + L * .1) * ca, cy + (hw + L * .1) * sa
    d.ellipse((hx - L * .11, hy - L * .11, hx + L * .11, hy + L * .11), fill=(36, 30, 24, int(a)), outline=color + (int(a * .8),))


def pila(etiquetas, remate="Pero el Árbol Áureo se mantiene inquebrantable", titulo="La Segunda Defensa de Leyndell",
         w=1500, h=720):
    """Muralla de Leyndell abajo y el Árbol Áureo arriba. Cada marca k deja caer una capa de cadáveres sobre la pila (cada
    vez más alta) con su etiqueta a la derecha. Marca len(etiquetas): el árbol brilla por encima de la pila y sale `remate`."""
    ftit, fe, fr = fuente("r", 40), fuente("r", 34), fuente("i", 46)
    n = len(etiquetas)
    rng = np.random.default_rng(5)
    capas = []
    for k in range(n):
        capas.append([(float(rng.uniform(-1, 1)), float(rng.uniform(-.6, .6)), float(rng.uniform(95, 135)))
                      for _ in range(max(3, 7 - k))])

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, base = M + w * .36, M + h - 70
        for j in range(9):                                            # sillares de la muralla
            d.rectangle((cx - 380 + j * 85, base, cx - 380 + j * 85 + 80, base + 26), outline=ORO_OSC + (int(a0 * .8),), width=2)
        fin = _eo((dt - mk[n]) / 1.0)
        ar = Image.new("RGBA", im.size, (0, 0, 0, 0))                  # el Árbol Áureo, lejos, arriba
        da = ImageDraw.Draw(ar)
        tx, ty = cx, M + 290
        da.line([(tx, ty + 70), (tx, ty - 10)], fill=ORO + (int(a0 * .7),), width=6)
        for r_, (ox, oy) in ((44, (0, -40)), (34, (-46, -18)), (34, (46, -18)), (28, (-24, -70)), (28, (26, -70))):
            da.ellipse((tx + ox - r_, ty + oy - r_, tx + ox + r_, ty + oy + r_), fill=ORO + (int(a0 * (.30 + .5 * fin)),))
        im.alpha_composite(_brillo(ar, float(14 + 10 * fin), float(1.2 + fin)))
        d = ImageDraw.Draw(im)
        for k, cap in enumerate(capas):
            u = _eo((dt - mk[k]) / .7)
            if u <= 0:
                continue
            ancho = 380 * (1 - .32 * k)
            yk = base - 30 - 52 * k
            for i, (fx, fa, L) in enumerate(cap):
                caida = (1 - _eo((dt - mk[k] - i * .07) / .5)) * 260
                _cuerpo(d, cx + fx * ancho, yk - caida, L, fa, ROJO if k == n - 1 else GRIS, 255 * min(1, u * 1.5))
            ue = _eo((dt - mk[k] - .3) / .5)
            ye = M + h - 110 - 62 * k
            _texto(d, (M + w * .66, ye), etiquetas[k], fe, PERGAMINO, "lm", 255 * ue)
            d.line([(M + w * .66 - 16, ye), (cx + ancho + 40, yk)], fill=ORO_OSC + (int(140 * ue),), width=2)
        if fin > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + 125), remate, fr, AMBAR, "mm", 255 * fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _sello(d, cx, cy, r, color, a, giro=0.0):
    if a <= 0:
        return
    c = color + (int(a),)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=4)
    d.ellipse((cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72), outline=c, width=2)
    for k in range(6):
        t = giro + k * math.pi / 3
        d.line([(cx + math.cos(t) * r * .72, cy + math.sin(t) * r * .72), (cx + math.cos(t) * r, cy + math.sin(t) * r)], fill=c, width=3)
    d.line([(cx - r * .45, cy), (cx + r * .45, cy)], fill=c, width=4)
    d.line([(cx, cy - r * .45), (cx, cy + r * .45)], fill=c, width=4)


def subsuelo(arriba="Leyndell, la capital dorada", abajo="Subsuelo de los marginados", sello="Sellado por Morgott",
             remate="A los de abajo los dejó donde estaban", titulo="Lo que hay debajo del trono", w=1500, h=760, celdas=6):
    """Corte de la ciudad. Marca 0: arriba, la capital dorada (cúpulas y torres) · marca 1: abajo, celdas con augurios
    encerrados (rojo, tiemblan) · marca 2: el sello dorado se estampa en un pasaje a la derecha · marca 3: `remate`;
    las celdas siguen en rojo."""
    ftit, fe, fs, fr = fuente("r", 40), fuente("b", 38), fuente("i", 32), fuente("i", 44)
    rng = np.random.default_rng(2)
    casas, x = [], 120
    while x < w - 160:
        bw, bh = float(rng.uniform(60, 120)), float(rng.uniform(70, 190))
        casas.append((x, bw, bh, rng.random() < .45))
        x += bw + float(rng.uniform(8, 26))

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 5
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        u0, u1, u2, u3 = (_eo((dt - mk[i]) / .7) for i in range(4))
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        suelo = M + h * .46
        d.line([(M + 60, suelo), (M + w - 60, suelo)], fill=ORO_OSC + (int(a0),), width=4)
        if u0 > 0:                                                    # la ciudad dorada
            cd = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(cd)
            for x, bw, bh, cup in casas:
                x, bh = M + x, bh * u0
                dc.rectangle((x, suelo - bh, x + bw, suelo), outline=ORO + (int(255 * u0),), width=2, fill=(40, 32, 16, int(150 * u0)))
                if cup:
                    dc.pieslice((x, suelo - bh - bw / 2, x + bw, suelo - bh + bw / 2), 180, 360, outline=ORO + (int(255 * u0),),
                                fill=(70, 56, 24, int(170 * u0)), width=2)
            im.alpha_composite(_brillo(cd, 8, 1.0))
            _texto(ImageDraw.Draw(im), (M + w / 2, M + 118), arriba, fe, ORO, "mm", 255 * u0)
        d = ImageDraw.Draw(im)
        if u1 > 0:                                                    # las celdas del subsuelo
            cw = (w * .62) / celdas
            y0, y1 = suelo + 70, M + h - 90
            for i in range(celdas):
                x0 = M + 90 + i * cw
                ui = _eo((dt - mk[1] - i * .12) / .5)
                d.rectangle((x0 + 8, y0, x0 + cw - 8, y1), fill=(22, 10, 8, int(220 * ui)), outline=ROJO + (int(200 * ui),), width=2)
                tiemblo = 2.5 * math.sin(dt * 11 + i * 1.9)
                _cuernos(d, x0 + cw / 2 + tiemblo, (y0 + y1) / 2 + 14, 30, ROJO, 255 * ui, 3)
                for b in range(4):
                    bx = x0 + 18 + b * (cw - 36) / 3
                    d.line([(bx, y0), (bx, y1)], fill=(110, 96, 80, int(200 * ui)), width=3)
            _texto(d, (M + 90 + w * .31, M + h - 52), abajo, fe, ROJO, "mm", 255 * u1)
        if u2 > 0:                                                    # el sello del pasaje
            sx, sy = M + w - 230, suelo + 150
            d.rectangle((sx - 110, suelo + 50, sx + 110, M + h - 90), fill=(14, 10, 6, int(230 * u2)), outline=ORO_OSC + (int(255 * u2),), width=2)
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            esc = 1 + .6 * (1 - u2)
            _sello(ImageDraw.Draw(t2), sx, sy, 62 * esc, ORO, 255 * u2, giro=dt * .3)
            _texto(ImageDraw.Draw(t2), (sx, sy + 105), sello, fs, ORO, "mm", 255 * u2, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.4))
        if u3 > 0:
            t3 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t3), (M + w / 2, suelo + 34), remate, fr, AMBAR, "mm", 255 * u3, sombra=False)
            im.alpha_composite(_brillo(t3, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _trono(d, cx, base, s, color, a):
    if a <= 0:
        return
    c, f = color + (int(a),), (24, 19, 12, int(a * .9))
    d.polygon([(cx - s * .55, base - s * .9), (cx - s * .45, base - s * 2.1), (cx, base - s * 2.45), (cx + s * .45, base - s * 2.1),
               (cx + s * .55, base - s * .9)], fill=f, outline=c)
    d.rectangle((cx - s * .75, base - s * .95, cx + s * .75, base - s * .7), fill=f, outline=c, width=3)
    for sg in (-1, 1):
        d.line([(cx + sg * s * .65, base - s * .7), (cx + sg * s * .7, base)], fill=c, width=5)
    d.line([(cx - s * .9, base), (cx + s * .9, base)], fill=c, width=4)


def trono_vacio(nombres, remate="Nadie puede reclamar el título", titulo="El trono que defendía", w=1500, h=700):
    """Trono vacío al centro. Marca k (k < n): `nombres[k]` entra en el arco y su línea busca el trono; a los 0,8 s se tacha
    en rojo · marca n: crece un muro de espinas delante del trono y sale `remate`."""
    ftit, fn_, fr = fuente("r", 40), fuente("r", 34), fuente("i", 50)
    n = len(nombres)
    rng = np.random.default_rng(9)
    espinas = [(float(rng.uniform(-1, 1)), float(rng.uniform(.3, 1)), float(rng.uniform(-.5, .5))) for _ in range(70)]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, base = M + w / 2, M + h - 90
        tr = Image.new("RGBA", im.size, (0, 0, 0, 0))
        _trono(ImageDraw.Draw(tr), cx, base, 120, ORO, a0)
        im.alpha_composite(_brillo(tr, 9, 1.0))
        d = ImageDraw.Draw(im)
        for k, s in enumerate(nombres):
            u = _eo((dt - mk[k]) / .5)
            if u <= 0:
                continue
            ang = math.pi * (.08 + .84 * k / max(1, n - 1))
            nx, ny = cx - math.cos(ang) * w * .38, M + 180 + (1 - math.sin(ang)) * h * .42
            g = _eo((dt - mk[k] - .8) / .4)
            wl0 = d.textlength(s, font=fn_) / 2 + 14
            x0l = nx + (wl0 if nx < cx - 40 else -wl0 if nx > cx + 40 else 0)
            _linea(d, (x0l, ny + (0 if abs(nx - cx) > 40 else 24)), (cx, base - 200), u * (1 - .4 * g), ROJO if g > 0 else ORO_OSC, 200 * u, 2)
            _texto(d, (nx, ny), s, fn_, GRIS if g > .5 else PERGAMINO, "mm", 255 * u)
            if g > 0:
                wl = d.textlength(s, font=fn_) / 2 + 8
                d.line([(nx - wl, ny + 3), (nx - wl + 2 * wl * g, ny + 3)], fill=ROJO + (230,), width=4)
        fin = _eo((dt - mk[n]) / 1.2)
        if fin > 0:
            es = Image.new("RGBA", im.size, (0, 0, 0, 0))
            de = ImageDraw.Draw(es)
            for i, (fx, fh, fa) in enumerate(espinas):
                v = _eo((dt - mk[n] - i * .008) / .6)
                x0 = cx + fx * 260
                alto = fh * 300 * v
                x1, y1 = x0 + fa * 120 * v, base - alto
                de.line([(x0, base), (x1, y1)], fill=(92, 58, 34, int(240 * v)), width=5)
                for j in range(1, 4):
                    px, py = x0 + (x1 - x0) * j / 4, base - alto * j / 4
                    de.line([(px, py), (px + (12 if j % 2 else -12), py - 14)], fill=(150, 60, 40, int(230 * v)), width=3)
            im.alpha_composite(es)
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + 118), remate, fr, AMBAR, "mm", 255 * fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def cadena(eslabones, preso="Morgott", amo="La Orden Dorada", remate=None, titulo="La cadena", w=1600, h=620):
    """Cadena de eslabones de `amo` (izq, dorado) a `preso` (der). Marca k enciende el eslabón k (pasa de gris a rojo)
    con su etiqueta debajo · marca n: `preso` se enciende en ámbar y sale `remate` arriba."""
    ftit, fl, fn_, fr = fuente("r", 40), fuente("r", 30), fuente("b", 46), fuente("i", 46)
    n = len(eslabones)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        d = ImageDraw.Draw(im)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cy = M + h * .46
        xa, xb = M + 150, M + w - 150
        _nodo(d, xa, cy, amo, None, ORO, a0, fn_, fl)
        paso = (xb - xa - 160) / max(1, n)
        ca = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(ca)
        for k in range(n):
            x = xa + 80 + paso * (k + .5)
            u = _eo((dt - mk[k]) / .5)
            col = tuple(int(GRIS[c] * (1 - u) + ROJO[c] * u) for c in range(3))
            bal = 4 * math.sin(dt * 2 + k)
            alto = 34 if k % 2 == 0 else 12
            dc.ellipse((x - paso * .62, cy - alto + bal, x + paso * .62, cy + alto + bal), outline=col + (int(a0),), width=9)
            if u > 0:
                for j, ln in enumerate(_partir(dc, eslabones[k], fl, paso * 1.0)[:3]):
                    _texto(dc, (x, cy + 64 + j * 34 + (0 if k % 2 else 40)), ln, fl, PERGAMINO, "mt", 255 * u)
        im.alpha_composite(_brillo(ca, 5, .9))
        fin = _eo((dt - mk[n]) / .8)
        d = ImageDraw.Draw(im)
        col = tuple(int(PERGAMINO[c] * (1 - fin) + AMBAR[c] * fin) for c in range(3))
        _nodo(d, xb, cy, preso, None, col, a0, fn_, fl)
        if fin > 0 and remate:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 50), remate, fr, AMBAR, "mm", 255 * fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ============================================================ er_mohg_atrocidades (10-nov-2026)
def cuenta_atras(numeros=("Tres", "Duo", "Unus"), final="Nihil", sub_final="nada, en latín", titulo="El ritual de la sangre",
                 remate="Tu herida, para la madre de la verdad", w=1500, h=700):
    """La cuenta atrás de Mohg en latín. Marca k (< n): entra el número k y un anillo rojo se cierra un poco más alrededor del
    «Tú» del centro. Marca n: NIHIL gigante en rojo que late tres veces y vacía tu barra de vida. Marca n+1: `remate`."""
    ftit, fnum, fnih, fs, ftu = fuente("r", 40), fuente("r", 64), fuente("r", 150), fuente("i", 38), fuente("i", 34)
    n = len(numeros)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + h / 2 + 40
        u_nih = _eo((dt - mk[n]) / .35)
        for i in range(n):
            u = _eo((dt - mk[i]) / .6)
            if u <= 0:
                continue
            r = 250 - 55 * i - 20 * u
            al = int(a0 * (.55 + .45 * u) * (1 - .6 * u_nih))
            d.ellipse((cx - r, cy - r * .62, cx + r, cy + r * .62), outline=ROJO + (al,), width=6)
            ang = math.radians(-150 + 60 * i)
            nx, ny = cx + math.cos(ang) * (r + 120), cy + math.sin(ang) * (r * .62 + 70)
            _texto(d, (nx, ny), numeros[i].upper(), fnum, AMBAR if mk[i + 1] > dt else ORO, "mm", 255 * u * (1 - .7 * u_nih),
                   track=4)
        if u_nih < 1:
            _texto(d, (cx, cy), "Tú", ftu, PERGAMINO, "mm", a0 * (1 - u_nih))
        if u_nih > 0:
            lat = sum(max(0.0, 1 - abs((dt - mk[n] - .25 - .7 * j) / .18)) for j in range(3))
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            _texto(dc, (cx, cy - 10), final.upper(), fnih, ROJO, "mm", 255 * u_nih, track=int(30 - 18 * u_nih), sombra=False)
            im.alpha_composite(_brillo(capa, 14 + 10 * lat, 1.4 + 1.2 * lat))
            d = ImageDraw.Draw(im)
            _texto(d, (cx, cy + 100), sub_final, fs, GRIS, "mm", 255 * u_nih)
            golpes = sum(1 for j in range(3) if dt - mk[n] > .25 + .7 * j)
            vid = 1 - .3 * golpes
            bx, by, bw = cx - 300, M + h - 70, 600
            d.rectangle((bx, by, bx + bw, by + 14), outline=ORO_OSC + (int(200 * u_nih),), width=2)
            d.rectangle((bx + 2, by + 2, bx + 2 + (bw - 4) * vid, by + 12), fill=(150, 30, 30, int(230 * u_nih)))
        u_r = _eo((dt - mk[n + 1]) / .5)
        if u_r > 0:
            _texto(d, (cx, M + h - 120), remate, fs, PERGAMINO, "mm", 255 * u_r)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def reclutamiento(pasos, remate="Y Mohg nunca responde", titulo="El reclutamiento de Varré", w=1600, h=640):
    """Escalera de sangre: pasos = [(nombre, sub)]. Marca k: sube el escalón k (una gota cae y lo tiñe de rojo); una línea de
    sangre une los escalones. Marca n: arriba aparece Mohg (cabeza con cuernos) y `remate`."""
    ftit, fn_, fs = fuente("r", 40), fuente("r", 40), fuente("i", 30)
    n = len(pasos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        sx = (w - 260) / max(1, n)
        prev = None
        for i, (nom, sub) in enumerate(pasos):
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            x0 = M + 60 + sx * i
            y0 = M + h - 110 - (h - 330) * i / max(1, n - 1)
            d.rectangle((x0, y0, x0 + sx - 24, y0 + 16), fill=(30, 12, 10, int(240 * u)), outline=ORO_OSC + (int(255 * u),), width=2)
            tinte = _eo((dt - mk[i] - .35) / .5)
            d.rectangle((x0 + 2, y0 + 2, x0 + 2 + (sx - 28) * tinte, y0 + 14), fill=ROJO + (int(230 * u),))
            if dt - mk[i] < .35:
                gy = y0 - 200 + 200 * max(0.0, (dt - mk[i]) / .35)
                d.ellipse((x0 + sx / 2 - 9, gy - 14, x0 + sx / 2 + 9, gy + 6), fill=ROJO + (230,))
            _texto(d, (x0 + (sx - 24) / 2, y0 - 16), nom, fn_, AMBAR if mk[i + 1] > dt else ORO, "mb", 255 * u)
            if sub:
                _texto(d, (x0 + (sx - 24) / 2, y0 + 30), sub, fs, GRIS, "mt", 255 * u)
            if prev:
                _linea(d, prev, (x0 + 6, y0 + 8), u, ROJO, 255 * u, 3)
            prev = (x0 + sx - 30, y0 + 8)
        u_r = _eo((dt - mk[n]) / .6)
        if u_r > 0:
            tx, ty = M + w - 110, M + 190
            _cuernos(d, tx, ty, 34, ROJO, 220 * u_r, 3)
            _texto(d, (tx, ty + 56), "Mohg", fn_, ROJO, "mt", 255 * u_r)
            if prev:
                _linea(d, prev, (tx - 40, ty + 40), u_r, ROJO, 160 * u_r, 2)
            _texto(d, (M + w / 2 - 80, M + 130), remate, fs, PERGAMINO, "mt", 255 * _eo((dt - mk[n] - .5) / .5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def dinastia(cabeza="Mohg", sub_cabeza="Señor de la Sangre", filas=(), arriba="La Madre Informe", sub_arriba="un dios exterior",
             remate="Todos sangran para ella", titulo="La Dinastía Mohgwyn", w=1600, h=720):
    """Organigrama. Marca 0: Mohg (cabeza con cuernos). Marcas 1..n: cada rama de `filas` [(nombre, sub)] cuelga de él con
    una línea de sangre. Marca n+1: encima aparece `arriba`, una mancha sin forma que late, y la sangre de TODAS las ramas
    sube por las líneas hasta ella. Marca n+2: `remate`."""
    ftit, fn_, fs, fgr = fuente("r", 40), fuente("r", 34), fuente("i", 26), fuente("r", 50)
    n = len(filas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 4)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + 330
        u0 = _eo((dt - mk[0]) / .5)
        u_m = _eo((dt - mk[n + 1]) / .7)
        sp = (w - 120) / max(1, n)
        by = M + h - 150
        for i, (nom, sub) in enumerate(filas):
            u = _eo((dt - mk[i + 1]) / .5)
            if u <= 0:
                continue
            x = M + 60 + sp * (i + .5)
            _linea(d, (cx, cy + 140), (x, by - 46), u, ROJO, 200 * u, 3)
            if u_m > 0:
                for k in range(3):
                    v = ((dt - mk[n + 1]) * .9 + k / 3 + i * .13) % 1
                    px, py = x + (cx - x) * v, by - 46 + (cy + 140 - by + 46) * v
                    d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=ROJO + (int(230 * u_m),))
            d.ellipse((x - 9, by - 54, x + 9, by - 36), fill=(14, 12, 9, int(255 * u)), outline=ROJO + (int(255 * u),), width=3)
            lns = _partir(d, nom, fn_, sp - 16)
            for k, ln in enumerate(lns):
                _texto(d, (x, by - 20 + k * 38), ln, fn_, AMBAR if mk[i + 2] > dt >= mk[i + 1] else PERGAMINO, "mt", 255 * u)
            if sub:
                _texto(d, (x, by + 26 + 38 * (len(lns) - 1)), sub, fs, GRIS, "mt", 255 * u)
        if u0 > 0:
            _cuernos(d, cx, cy - 10, 40, ROJO if u_m > .5 else ORO, 255 * u0, 4)
            _texto(d, (cx, cy + 46), cabeza, fgr, ORO, "mt", 255 * u0)
            _texto(d, (cx, cy + 102), sub_cabeza, fs, GRIS, "mt", 255 * u0)
        if u_m > 0:
            lat = .5 + .5 * math.sin((dt - mk[n + 1]) * 4.2)
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            my = M + 150
            for k in range(9):
                ang = k * 0.7 + dt * (.6 + .1 * k)
                rx, ry = cx + math.cos(ang) * 60, my + math.sin(ang * 1.3) * 18
                rr = 28 + 10 * math.sin(dt * 2 + k)
                dc.ellipse((rx - rr, ry - rr * .7, rx + rr, ry + rr * .7), fill=(120 + int(60 * lat), 18, 22, int(150 * u_m)))
            im.alpha_composite(_brillo(capa, 18, 1.6))
            d = ImageDraw.Draw(im)
            _texto(d, (cx + 150, my - 10), arriba, fn_, ROJO, "lm", 255 * u_m)
            _texto(d, (cx + 150, my + 28), sub_arriba, fs, GRIS, "lm", 255 * u_m)
            _linea(d, (cx, cy - 70), (cx, my + 30), u_m, ROJO, 200 * u_m, 3)
        u_r = _eo((dt - mk[n + 2]) / .5)
        if u_r > 0:
            _texto(d, (cx - 150, M + 150), remate, fs, PERGAMINO, "rm", 255 * u_r)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn



# ───────────── er_godrick_atrocidades (11-nov-2026): votación de voces, injerto y linaje dorado ─────────────
def _onda(d, x0, cy, ancho, alto, t, color, a, activa=True, n=34):
    """Forma de onda de barras (una voz que habla); quieta y baja si no está activa."""
    paso = ancho / n
    for k in range(n):
        if activa:
            h = alto * (.18 + .82 * abs(math.sin(t * 7.3 + k * .61) * math.sin(t * 2.1 + k * .23)))
        else:
            h = alto * .08
        x = x0 + k * paso
        d.rounded_rectangle((x, cy - h / 2, x + paso * .55, cy + h / 2), 3, fill=color + (int(a),))


def votacion(a=("Narrador anterior", "la voz de siempre"), b=("Nuevo profeta", "la voz de hoy"), titulo="Tú decides",
             caja="Escríbelo en los comentarios", remate="El que tenga más comentarios se queda", w=1500, h=680):
    """La votación de voces. Marca 0: carta A con su onda (habla). Marca 1: carta B con su onda; la A se calla.
    Marca 2: caja de comentario donde se escribe «narrador anterior» / «nuevo profeta» con cursor, y una barra de balanza
    que oscila entre las dos SIN cifras (aún no hay votos). Marca 3: `remate` y las dos cartas hablan a la vez."""
    ftit, fn_, fs, fc = fuente("r", 40), fuente("r", 50), fuente("i", 30), fuente("r", 34)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 5
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cw, ch = w * .38, 250
        for i, (nom, sub) in enumerate((a, b)):
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            x0 = M + (w * .07 if i == 0 else w * .55)
            y0 = M + 120 + 30 * (1 - u)
            hablando = (mk[i] <= dt < mk[i + 1]) or dt >= mk[3]
            col = AMBAR if hablando else ORO
            d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch), 18, fill=(16, 13, 9, int(235 * u)), outline=col + (int(255 * u),),
                                width=3 if hablando else 2)
            _texto(d, (x0 + cw / 2, y0 + 52), nom, fn_, col, "mm", 255 * u)
            _texto(d, (x0 + cw / 2, y0 + 96), sub, fs, GRIS, "mm", 255 * u)
            _onda(d, x0 + 40, y0 + 175, cw - 80, 90, dt + i * 3, col, 230 * u, hablando)
        u_c = _eo((dt - mk[2]) / .5)
        if u_c > 0:
            bx, by, bw, bh = M + w * .12, M + 430, w * .76, 74
            d.rounded_rectangle((bx, by, bx + bw, by + bh), 12, fill=(24, 20, 14, int(240 * u_c)), outline=GRIS + (int(200 * u_c),),
                                width=2)
            _texto(d, (bx + 16, by - 12), caja, fs, GRIS, "lb", 255 * u_c)
            opciones = [a[0].lower(), b[0].lower()]
            ciclo = (dt - mk[2]) % 5.0
            txt = opciones[int((dt - mk[2]) // 5.0) % 2]
            vis = txt[:int(min(len(txt), max(0, ciclo - .3) * 14))] if ciclo < 4.2 else txt[:int(max(0, (5.0 - ciclo) * 30))]
            _texto(d, (bx + 24, by + bh / 2), vis, fc, PERGAMINO, "lm", 255 * u_c)
            if int(dt * 2.2) % 2 == 0:
                cxp = bx + 28 + (d.textlength(vis, font=fc) if vis else 0)
                d.rectangle((cxp, by + 18, cxp + 3, by + bh - 18), fill=PERGAMINO + (int(230 * u_c),))
            yb = by + bh + 60                                   # balanza sin cifras: oscila entre las dos
            d.rectangle((bx, yb, bx + bw, yb + 12), fill=(30, 26, 20, int(230 * u_c)), outline=ORO_OSC + (int(220 * u_c),), width=2)
            p = .5 + .32 * math.sin((dt - mk[2]) * 1.7) * (0 if dt >= mk[3] else 1)
            d.rectangle((bx + 2, yb + 2, bx + 2 + (bw - 4) * p, yb + 10), fill=AMBAR + (int(200 * u_c),))
            d.ellipse((bx + bw * p - 13, yb - 7, bx + bw * p + 13, yb + 19), fill=ORO + (int(255 * u_c),))
            _texto(d, (bx, yb + 26), a[0], fs, GRIS, "lt", 255 * u_c)
            _texto(d, (bx + bw, yb + 26), b[0], fs, GRIS, "rt", 255 * u_c)
        u_r = _eo((dt - mk[3]) / .5)
        if u_r > 0:
            _texto(d, (M + w / 2, M + h - 34), remate, fs, PERGAMINO, "mm", 255 * u_r)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _puntadas(d, p0, p1, color, a, n=4, s=9):
    """Puntadas en X a lo largo de la unión p0-p1 (costura de un injerto)."""
    for k in range(n):
        f = (k + .5) / n
        x, y = p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f
        d.line((x - s, y - s, x + s, y + s), fill=color + (int(a),), width=3)
        d.line((x - s, y + s, x + s, y - s), fill=color + (int(a),), width=3)


_ANG_INJ = [-150, -30, 165, 15, -110, -70, 140, 40]


def injerto(centro="Godrick", sub_centro="el Injertado", miembros=(), remate=None, titulo="El injerto", w=1600, h=740):
    """Un cuerpo central (torso dorado) al que vuelan miembros desde los bordes, uno por marca: cada miembro = (nombre, sub),
    entra desde lejos, se clava en el torso y se cose con puntadas rojas (gotean); su etiqueta queda en el extremo.
    Marcas 0..n-1 = miembros; marca n = `remate` y el cuerpo entero late en rojo."""
    ftit, fn_, fs, fgr = fuente("r", 40), fuente("r", 34), fuente("i", 26), fuente("r", 50)
    n = len(miembros)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + h / 2 + 60
        u_r = _eo((dt - mk[n]) / .6)
        lat = (.5 + .5 * math.sin((dt - mk[n]) * 5)) * u_r
        col_c = tuple(int(ORO[j] + (ROJO[j] - ORO[j]) * lat) for j in range(3))
        d.ellipse((cx - 95, cy - 115, cx + 95, cy + 115), fill=(26, 21, 14, int(a0)), outline=col_c + (int(a0),), width=4)
        d.ellipse((cx - 40, cy - 195, cx + 40, cy - 118), fill=(26, 21, 14, int(a0)), outline=col_c + (int(a0),), width=4)
        _texto(d, (cx, cy - 12), centro, fgr if len(centro) < 9 else fn_, col_c, "mm", a0)
        _texto(d, (cx, cy + 38), sub_centro, fs, GRIS, "mm", a0)
        for i, (nom, sub) in enumerate(miembros):
            u = _eo((dt - mk[i]) / .55)
            if u <= 0:
                continue
            ang = math.radians(_ANG_INJ[i % 8])
            ux, uy = math.cos(ang), math.sin(ang)
            off = 420 * (1 - u)
            p0 = (cx + ux * (92 + off), cy + uy * (112 + off))
            p1 = (p0[0] + ux * 190, p0[1] + uy * 190)
            col = AMBAR if mk[i + 1] > dt >= mk[i] else PERGAMINO
            d.line((p0, p1), fill=(70, 56, 36, int(255 * u)), width=26)
            d.line((p0, p1), fill=col + (int(200 * u),), width=4)
            d.ellipse((p1[0] - 20, p1[1] - 20, p1[0] + 20, p1[1] + 20), fill=(70, 56, 36, int(255 * u)), outline=col + (int(220 * u),),
                      width=3)
            cos_ = _eo((dt - mk[i] - .5) / .5)
            if cos_ > 0:
                px, py = -uy, ux
                q0 = (p0[0] + px * 26 + ux * 6, p0[1] + py * 26 + uy * 6)
                q1 = (p0[0] - px * 26 + ux * 6, p0[1] - py * 26 + uy * 6)
                _puntadas(d, q0, q1, ROJO, 255 * cos_, n=3)
                if dt - mk[i] < 1.6:
                    for k in range(3):
                        gx = p0[0] + (k - 1) * 10 + ux * 8
                        gy = p0[1] + 10 + (dt - mk[i] - .5) * 60 * (1 + k * .25)
                        d.ellipse((gx - 4, gy - 5, gx + 4, gy + 5), fill=ROJO + (int(200 * cos_),))
            lx, ly = p1[0] + ux * 34, p1[1] + uy * 34
            anc = "lm" if ux > .2 else ("rm" if ux < -.2 else "mm")
            _texto(d, (lx, ly - 16), nom, fn_, col, anc, 255 * u)
            if sub:
                _texto(d, (lx, ly + 22), sub, fs, GRIS, anc, 255 * u)
        if u_r > 0 and remate:
            _texto(d, (M + w / 2, M + h - 34), remate, fs, PERGAMINO, "mm", 255 * u_r)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def linaje(raiz=("Godfrey", "primer Señor del Círculo"), hijos=(("Godrick", "el enclenque de la camada"),
                                                                    ("Godefroy", "encerrado para siempre")),
           medio="la sangre, cada vez más diluida", remate="El linaje dorado", titulo="La sangre de Godfrey", w=1500, h=740,
           injertos=None):
    """Árbol del linaje dorado. Marca 0: la raíz (corona dorada que brilla). Marca 1: el tronco baja y se apaga de oro a gris
    (`medio`, la sangre diluida, en trazos). Marcas 2..n+1: cada hijo cuelga del tronco y le brotan miembros cosidos con
    puntadas rojas (se injerta). Marca n+2: `remate` y la corona pierde el brillo.
    `injertos` = índices de los hijos que se injertan (None = todos; () = ninguno, p. ej. los hijos de Godfrey y Márika)."""
    ftit, fn_, fs, fgr = fuente("r", 40), fuente("r", 42), fuente("i", 28), fuente("r", 56)
    n = len(hijos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 4)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, ry = M + w / 2, M + 175
        u0 = _eo((dt - mk[0]) / .5)
        u_fin = _eo((dt - mk[n + 2]) / .8)
        if u0 > 0:
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            pts = [(cx - 60, ry + 22), (cx - 60, ry - 20), (cx - 30, ry), (cx, ry - 38), (cx + 30, ry), (cx + 60, ry - 20),
                   (cx + 60, ry + 22)]
            dc.polygon(pts, fill=ORO + (int(255 * u0 * (1 - .5 * u_fin)),))
            im.alpha_composite(_brillo(capa, 16.0, 1.6 * (1 - .8 * u_fin)))
            d = ImageDraw.Draw(im)
            _texto(d, (cx + 90, ry - 8), raiz[0], fgr, ORO, "lm", 255 * u0)
            _texto(d, (cx + 92, ry + 38), raiz[1], fs, GRIS, "lm", 255 * u0)
        u1 = _eo((dt - mk[1]) / 1.0)
        yb = M + h - 250
        if u1 > 0:
            pasos = 18
            for k in range(0, int(pasos * u1), 2):
                f = k / pasos
                y0_ = ry + 40 + (yb - 60 - ry - 40) * f
                y1_ = ry + 40 + (yb - 60 - ry - 40) * (f + 1 / pasos)
                col = tuple(int(ORO[j] + (GRIS[j] - ORO[j]) * f) for j in range(3))
                d.line((cx, y0_, cx, y1_), fill=col + (int(255 * (1 - .5 * f)),), width=int(8 - 5 * f))
            _texto(d, (cx - 28, (ry + yb) / 2 - 10), medio, fs, GRIS, "rm", 255 * u1)
        sp = w * .5 / max(1, n - 1) if n > 1 else 0
        for i, (nom, sub) in enumerate(hijos):
            u = _eo((dt - mk[i + 2]) / .5)
            if u <= 0:
                continue
            x = cx - w * .25 + sp * i if n > 1 else cx
            _linea(d, (cx, yb - 60), (x, yb - 60), u, GRIS, 200 * u, 3)
            _linea(d, (x, yb - 60), (x, yb - 14), u, GRIS, 200 * u, 3)
            br = _eo((dt - mk[i + 2] - .4) / .9) if injertos is None or i in injertos else 0.0
            for k in range(5):
                if br * 5 <= k:
                    break
                ang = math.radians(150 + k * 60) if k < 3 else math.radians(-30 + (k - 3) * 240)
                ang = math.radians([160, 200, 20, -20, 90][k])
                q0 = (x + math.cos(ang) * 38, yb + math.sin(ang) * 34)
                q1 = (x + math.cos(ang) * 110, yb + math.sin(ang) * 90)
                if k == 4:
                    continue
                d.line((q0, q1), fill=(110, 80, 50, int(230 * u)), width=14)
                d.ellipse((q1[0] - 11, q1[1] - 11, q1[0] + 11, q1[1] + 11), fill=(110, 80, 50, int(230 * u)))
                _puntadas(d, (q0[0] - 9, q0[1] - 9), (q0[0] + 9, q0[1] + 9), ROJO, 240 * u, n=1, s=9)
            d.ellipse((x - 26, yb - 26, x + 26, yb + 26), fill=(16, 13, 9, int(255 * u)), outline=ORO_OSC + (int(255 * u),), width=4)
            col = AMBAR if mk[i + 3] > dt >= mk[i + 2] else PERGAMINO
            _texto(d, (x, yb + 76), nom, fn_, col, "mt", 255 * u)
            _texto(d, (x, yb + 128), sub, fs, GRIS, "mt", 255 * u)
        u_r = _eo((dt - mk[n + 2]) / .6)
        if u_r > 0:
            _texto(d, (M + w / 2, M + h - 34), remate, fs, PERGAMINO, "mm", 255 * u_r)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn



# ============================================================ er_sinluz_atrocidades (16-nov-2026)
def _sello_txt(im, cx, cy, txt, f, color, a, giro=-12, escala=1.0):
    """Sello de tinta rotado (rectángulo doble + texto) pegado sobre `im`; `escala` > 1 al caer (golpe)."""
    if a <= 0:
        return
    d0 = ImageDraw.Draw(im)
    tw = d0.textlength(txt, font=f)
    W, H = int(tw + 70), int(f.size * 1.6)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(s)
    ds.rectangle((3, 3, W - 4, H - 4), outline=color + (int(a),), width=6)
    ds.rectangle((12, 12, W - 13, H - 13), outline=color + (int(a * .7),), width=2)
    ds.text((W / 2, H / 2), txt, font=f, fill=color + (int(a),), anchor="mm")
    if escala != 1.0:
        s = s.resize((max(1, int(W * escala)), max(1, int(H * escala))))
    s = s.rotate(giro, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))


def _palomita(d, x, y, s, color, a):
    d.line((x - 22 * s, y, x - 6 * s, y + 18 * s), fill=color + (int(a),), width=7)
    d.line((x - 6 * s, y + 18 * s, x + 26 * s, y - 22 * s), fill=color + (int(a),), width=7)


def expediente(acusado="El Sinluz", sub="sin doncella, sin runas, sin nada", cargos=(), ya=0, sello="CULPABLE",
               titulo="Expediente", w=1400, h=None):
    """Ficha de acusación del juicio al jugador (recurrente: una por puesto). Los `ya` primeros cargos ya están escritos y
    sellados al entrar; marca k (k = 0..) escribe el cargo `ya + k` letra a letra en ámbar y le cae una palomita roja al
    lado; la marca siguiente al último cargo deja caer el sello grande `sello` en diagonal (None = sin sello final)."""
    ftit, fac, fs, fc, fn_, fse = fuente("r", 40), fuente("b", 58), fuente("i", 30), fuente("r", 38), fuente("b", 40), fuente("b", 92)
    n = len(cargos)
    h = h or int(320 + 82 * n + (60 if sello else 0))

    def fn(dt, dur, marcas):
        mk = [-9.0] * ya + list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        _texto(d, (M + 80, M + 150), acusado, fac, ORO, "lm", a0)
        _texto(d, (M + 84, M + 205), sub, fs, GRIS, "lm", a0)
        d.line((M + 80, M + 240, M + w - 80, M + 240), fill=ORO_OSC + (int(a0 * .8),), width=2)
        paso = 82
        for i, c in enumerate(cargos):
            tesc = max(.6, len(c) * .035)
            u = (dt - mk[i]) / tesc
            if u <= 0:
                continue
            y = M + 300 + i * paso
            vis = c[:int(len(c) * min(1, u))]
            act = mk[i + 1] > dt >= mk[i]
            _texto(d, (M + 80, y), f"{i + 1}.", fn_, ROJO, "lm", a0)
            _texto(d, (M + 140, y), vis, fc, AMBAR if act else PERGAMINO, "lm", a0)
            v = _eo((dt - mk[i] - tesc) / .25)
            if v > 0:
                _palomita(d, M + w - 120, y, 1 + 1.2 * (1 - v), ROJO, 255 * v * a0 / 255)
        if sello:
            u = _eo((dt - mk[n]) / .35)
            if u > 0:
                _sello_txt(im, M + w * .68, M + 160, sello, fse, ROJO, 235 * u, giro=-10, escala=1 + .8 * (1 - u))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _fauces(d, cx, cy, r, ab, color, a):
    """Cabeza de serpiente de perfil con la boca hacia la izquierda: cráneo a la derecha con el ojo, mandíbulas que giran
    sobre la bisagra; colmillos en el borde interior. `ab` 0..1 = apertura."""
    if a <= 0:
        return
    bx, by = cx + r * .35, cy
    d.ellipse((bx - r * .05, by - r * .55, bx + r * .95, by + r * .5), fill=(34, 22, 14, int(a)), outline=color + (int(a),), width=5)
    ang = math.radians(6 + 30 * ab)
    L = r * 1.55
    if ab > .08:
        tipu = (bx - L * math.cos(ang), by - L * math.sin(ang))
        tipd = (bx - L * math.cos(ang), by + L * math.sin(ang))
        d.polygon([(bx, by), tipu, tipd], fill=(80, 10, 8, int(a * .85)))
    for s in (-1, 1):
        tip = (bx - L * math.cos(ang), by + s * L * math.sin(ang))
        ex = (-math.sin(ang) * s * 0, 0)
        g = r * .42
        out_h = (bx + r * .1, by + s * g)
        out_t = (tip[0] - 4, tip[1] + s * g * .25)
        d.polygon([(bx, by), tip, out_t, out_h], fill=(34, 22, 14, int(a)), outline=color + (int(a),), width=5)
        for k in range(1, 7):
            f = k / 7
            px = bx + (tip[0] - bx) * f
            py = by + (tip[1] - by) * f
            largo = (38 if k == 6 else 16) * (.35 + .65 * ab)
            d.polygon([(px - 7, py), (px + 7, py), (px - 3, py - s * largo)], fill=PERGAMINO + (int(a),))
    d.ellipse((bx + r * .38, by - r * .4, bx + r * .62, by - r * .2), fill=AMBAR + (int(a),))
    d.line((bx + r * .5, by - r * .39, bx + r * .5, by - r * .21), fill=(10, 8, 6, int(a)), width=4)


def _figura(d, x, cy, esc, col, a, ancho=4):
    """Campeón encapuchado (silueta rellena con filete) con su espada al costado."""
    if a <= 2:
        return
    s = esc
    d.polygon([(x - 34 * s, cy + 95 * s), (x - 20 * s, cy - 30 * s), (x, cy - 48 * s), (x + 20 * s, cy - 30 * s),
               (x + 34 * s, cy + 95 * s)], fill=(30, 25, 18, int(a)), outline=col + (int(a),))
    d.pieslice((x - 26 * s, cy - 100 * s, x + 26 * s, cy - 30 * s), 180, 360, fill=(30, 25, 18, int(a)), outline=col + (int(a),),
               width=max(1, ancho - 1))
    d.rectangle((x - 22 * s, cy - 66 * s, x + 22 * s, cy - 36 * s), fill=(30, 25, 18, int(a)))
    d.line((x - 22 * s, cy - 66 * s, x - 22 * s, cy - 36 * s), fill=col + (int(a),), width=max(1, ancho - 1))
    d.line((x + 22 * s, cy - 66 * s, x + 22 * s, cy - 36 * s), fill=col + (int(a),), width=max(1, ancho - 1))
    d.ellipse((x - 12 * s, cy - 60 * s, x + 12 * s, cy - 40 * s), fill=(6, 5, 4, int(a)))
    d.line((x + 40 * s, cy - 10 * s, x + 40 * s, cy + 100 * s), fill=col + (int(a),), width=ancho)
    d.line((x + 30 * s, cy + 2 * s, x + 50 * s, cy + 2 * s), fill=col + (int(a),), width=ancho)


def audiencia(campeones=("Campeón", "Campeón", "Campeón"), tu="Tú", sub_tu="el siguiente", remate="Eras el siguiente menú",
              titulo="La audiencia con el señor", w=1600, h=640):
    """Fila de campeones encapuchados que avanza hacia las fauces de la serpiente (der). Marca k (0..n-1): el campeón k
    entra en las fauces (se encoge y se apaga) y las mandíbulas se cierran de golpe. Marca n: los demás rótulos se van,
    aparece «Tú» al principio de la fila en ámbar, flechas rojas lo llevan a las fauces abiertas y sale `remate` en rojo."""
    ftit, fn_, fs, fr = fuente("r", 40), fuente("r", 34), fuente("i", 28), fuente("i", 50)
    n = len(campeones)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cy = M + h * .5
        fx = M + w - 300
        ab = .3 + .1 * math.sin(dt * 2)
        for k in range(n):
            e = dt - mk[k]
            if 0 <= e < .9:
                ab = max(0.0, .3 + .7 * e / .45 if e < .45 else 1.0 - (e - .45) / .45)
        u_fin = _eo((dt - mk[n]) / .6)
        ab = ab * (1 - u_fin) + (1.0 + .05 * math.sin(dt * 4)) * u_fin
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        _fauces(ImageDraw.Draw(capa), fx, cy, 140, ab, ORO_OSC if u_fin < .5 else ROJO, a0)
        im.alpha_composite(_brillo(capa, 8, 1.0))
        d = ImageDraw.Draw(im)
        x0, paso = M + 150, (fx - 260 - (M + 150)) / max(1, n)
        for k, nom in enumerate(campeones):
            e = _eo((dt - mk[k]) / .45)
            xi = x0 + paso * (k + .5)
            x = xi + (fx - 90 - xi) * e
            _figura(d, x, cy, 1 - .85 * e, PERGAMINO, a0 * (1 - e))
            _texto(d, (xi, cy + 130), nom, fn_, GRIS if e > .5 else PERGAMINO, "mt", a0 * (1 - .6 * e) * (1 - u_fin))
        if u_fin > 0:
            x = x0 + paso * .5
            lat = .5 + .5 * math.sin(dt * 5)
            _figura(d, x, cy, 1.0, AMBAR, 255 * u_fin, 5)
            _texto(d, (x, cy + 126), tu, fuente("b", 46), AMBAR, "mt", 255 * u_fin)
            _texto(d, (x, cy + 180), sub_tu, fs, GRIS, "mt", 255 * u_fin)
            for j in range(6):
                xx = x + 110 + j * ((fx - 200 - x - 110) / 5)
                d.polygon([(xx, cy - 14), (xx + 26, cy), (xx, cy + 14)], fill=ROJO + (int((110 + 130 * lat) * u_fin),))
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 46), remate, fr, ROJO, "mm", 255 * u_fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


_UVAS = [(0, -120), (-70, -60), (70, -60), (-120, 10), (0, 0), (120, 10), (-70, 75), (70, 75), (0, 145)]


def uvas(etiquetas=(), remate="Los dueños de los ojos", titulo="La Uva Shabriri", w=1500, h=740):
    """Racimo de uvas amarillentas colgando de un tallo. Marca 0: las uvas giran una a una y son OJOS (iris ámbar, pupila
    negra, venitas rojas) que parpadean y miran. Marcas 1..n: `etiquetas` (texto, i_uva): una línea sale de esa uva hasta su
    rótulo a los lados. Marca n+1: `remate` en rojo y todos los ojos miran al frente."""
    ftit, fl, fr = fuente("r", 40), fuente("r", 32), fuente("i", 46)
    n = len(etiquetas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + h / 2 + 40
        bal = 6 * math.sin(dt * 1.3)
        d.line((cx, cy - 250, cx + bal, cy - 165), fill=(90, 70, 40, int(a0)), width=10)
        d.polygon([(cx + bal, cy - 210), (cx + 70 + bal, cy - 240), (cx + 40 + bal, cy - 200)], fill=(70, 90, 40, int(a0)))
        R = 52
        fin = _eo((dt - mk[n + 1]) / .5)
        for i, (ox, oy) in enumerate(_UVAS):
            x, y = cx + ox + bal * (1 - (oy + 150) / 300), cy + oy
            u = _eo((dt - mk[0] - i * .18) / .45)
            d.ellipse((x - R, y - R, x + R, y + R), fill=(196, 178, 84, int(a0)), outline=(120, 96, 40, int(a0)), width=3)
            if u > 0:
                for k in range(4):
                    ang = k * 1.7 + i
                    d.line((x + math.cos(ang) * R * .95, y + math.sin(ang) * R * .95, x + math.cos(ang) * R * .58,
                            y + math.sin(ang) * R * .58), fill=ROJO + (int(170 * u),), width=2)
                mira_x = (1 - fin) * 10 * math.sin(dt * .9 + i * 1.3)
                mira_y = (1 - fin) * 6 * math.cos(dt * .7 + i)
                ir = R * .5 * u
                parp = abs(math.sin(dt * .8 + i * 2.1))
                cierre = 1.0 if parp > .06 else .15
                ex, ey = x + mira_x, y + mira_y
                d.ellipse((ex - ir, ey - ir * cierre, ex + ir, ey + ir * cierre), fill=(214, 140, 40, int(255 * u)))
                d.ellipse((ex - ir * .45, ey - ir * .45 * cierre, ex + ir * .45, ey + ir * .45 * cierre), fill=(10, 8, 6, int(255 * u)))
                if cierre > .5:
                    d.ellipse((ex - ir * .5 + 4, ey - ir * .5, ex - ir * .5 + 11, ey - ir * .5 + 7), fill=(255, 250, 230, int(220 * u)))
            else:
                d.ellipse((x - R * .5, y - R * .6, x - R * .2, y - R * .3), fill=(240, 230, 160, int(a0 * .7)))
        izq = der = 0
        for k, (txt, iu) in enumerate(etiquetas):
            ox, oy = _UVAS[iu % len(_UVAS)]
            lado = -1 if ox < 0 or (ox == 0 and k % 2 == 0) else 1
            fila = izq if lado < 0 else der
            if lado < 0:
                izq += 1
            else:
                der += 1
            u = _eo((dt - mk[k + 1]) / .5)
            if u <= 0:
                continue
            x, y = cx + ox, cy + oy
            tx = cx + lado * (w * .5 - 90)
            ty = M + 190 + fila * 150
            act = mk[k + 2] > dt >= mk[k + 1]
            col = AMBAR if act else PERGAMINO
            lineas = _partir(d, txt, fl, 380)[:2]
            ancho_t = max(d.textlength(l, font=fl) for l in lineas)
            fin_l = (tx - lado * (ancho_t + 16), ty)
            _linea(d, (x + lado * R, y), fin_l, u, col, 200 * u, 3)
            for j, ln in enumerate(lineas):
                _texto(d, (tx, ty - 14 + j * 36), ln, fl, col, "rm" if lado > 0 else "lm", 255 * u)
        if fin > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 36), remate, fr, ROJO, "mm", 255 * fin, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _raiz(d, x, y, s, color, a):
    """Raíz mortuoria esquemática: tubérculo con raicillas retorcidas."""
    if a <= 0:
        return
    d.ellipse((x - 16 * s, y - 26 * s, x + 16 * s, y + 18 * s), fill=(28, 22, 16, int(a)), outline=color + (int(a),), width=3)
    for k, (dx, l) in enumerate(((-10, 46), (0, 58), (10, 42), (-4, 50))):
        pts = [(x + dx * s, y + 14 * s)]
        for j in range(1, 5):
            pts.append((x + dx * s + 6 * s * math.sin(j * 1.9 + k), y + 14 * s + l * s * j / 4))
        d.line(pts, fill=color + (int(a),), width=3)


def paciencia(n=9, umbral=4, quien="Gurranq", basta="«Basta»", remate="Y le llevaste cinco más", titulo="Raíz mortuoria",
              icono=None, w=1600, h=500):
    """Fila de `n` raíces que se entregan a `quien`. Marca 0: se encienden en dorado de la 1 a la `umbral` (escalonadas).
    Marca 1: después de la `umbral` cae el sello `basta` en rojo y la fila se estremece. Marca 2: se encienden en rojo de la
    umbral+1 a la n, cada una con su número. Marca 3: `remate`. `icono` = PNG con alfa del objeto real (se dibuja en cada
    casilla con un halo dorado o rojo; apagado = oscuro); sin icono, raíz esquemática."""
    ftit, fq, fnum, fb, fr = fuente("r", 40), fuente("b", 44), fuente("b", 30), fuente("b", 64), fuente("i", 46)
    ico = None
    if icono:
        ico = Image.open(icono).convert("RGBA")
        bb = ico.getbbox()
        ico = ico.crop(bb) if bb else ico
        k = 150 / max(ico.size)
        ico = ico.resize((max(1, int(ico.width * k)), max(1, int(ico.height * k))), Image.LANCZOS)
        ico_osc = Image.fromarray((np.array(ico) * np.array([.35, .35, .35, 1])).astype(np.uint8))

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 5
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        _texto(d, (M + 70, M + 44), quien, fq, PERGAMINO, "lm", a0)
        cy = M + h * .55
        x0, paso = M + 130, (w - 260) / (n - 1)
        tiemb = 6 * math.sin(dt * 40) * max(0, 1 - (dt - mk[1]) / .5) if dt >= mk[1] else 0
        for i in range(n):
            x = x0 + paso * i + tiemb
            if i < umbral:
                u = _eo((dt - mk[0] - i * .35) / .35)
                col = tuple(int(GRIS[c] * (1 - u) + ORO[c] * u) for c in range(3))
            else:
                u = _eo((dt - mk[2] - (i - umbral) * .4) / .35)
                col = tuple(int(GRIS[c] * (1 - u) + ROJO[c] * u) for c in range(3))
            if ico is not None:
                if u > 0:
                    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    ImageDraw.Draw(halo).ellipse((x - 60, cy - 105, x + 60, cy + 15), fill=col + (int(150 * u * a0 / 255),))
                    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(22)))
                im.alpha_composite(ico_osc if u < .5 else ico, (int(x - ico.width / 2), int(cy - 45 - ico.height / 2)))
                d = ImageDraw.Draw(im)
            else:
                _raiz(d, x, cy - 40, 1.25, col, a0 * (.45 + .55 * u))
            if u > 0:
                _texto(d, (x, cy + 70), str(i + 1), fnum, col, "mt", 255 * u)
        ub = _eo((dt - mk[1]) / .3)
        if ub > 0:
            xm = x0 + paso * (umbral - .5)
            d.line((xm, cy - 110, xm, cy + 120), fill=ROJO + (int(200 * ub),), width=4)
            _sello_txt(im, xm, cy - 150, basta, fb, ROJO, 240 * ub, giro=-8, escala=1 + .8 * (1 - ub))
        ur = _eo((dt - mk[3]) / .5)
        if ur > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 40), remate, fr, AMBAR, "mm", 255 * ur, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ============================================================ er_godfrey_atrocidades (19-nov-2026)
def estandartes(nombres, remate="", titulo="Reinos conquistados", ya=0, w=1600, h=540):
    """Fila de estandartes con el nombre de cada pueblo vencido. Marca i: el estandarte i se apaga a gris y lo cruza un tajo
    rojo. Marca len(nombres): `remate` en ámbar. `ya` = cuántos salen ya tachados desde el principio (reapariciones)."""
    ftit, fn_, fr = fuente("r", 40), fuente("b", 34), fuente("i", 46)
    n = len(nombres)

    def fn(dt, dur, marcas):
        mk = [-9] * ya + list(marcas)[: n + 1 - ya] + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 46), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 84, w * .3, alfa=a0)
        paso = (w - 160) / n
        bw, bh, top = min(170, paso * .62), 250, M + 120
        for i, nom in enumerate(nombres):
            cx = M + 80 + paso * (i + .5)
            ui = _eo((dt - .15 - i * .18) / .35)
            if ui <= 0:
                continue
            ut = _eo((dt - mk[i]) / .45)
            col = tuple(int(ORO_OSC[c] * (1 - ut) + (70, 66, 58)[c] * ut) for c in range(3))
            sway = 3 * math.sin(dt * 2.2 + i) * (1 - ut)
            x0, x1, y1 = cx - bw / 2, cx + bw / 2, top + bh * ui
            d.line((cx, top - 18, cx, top + bh + 10), fill=ORO + (int(a0 * ui),), width=4)
            poly = [(x0 + sway, top), (x1 + sway, top), (x1, y1), (cx, y1 - 46 * ui), (x0, y1)]
            d.polygon(poly, fill=col + (int(230 * ui),), outline=ORO + (int(200 * ui * (1 - .6 * ut)),))
            d.ellipse((cx - 22, top + 70, cx + 22, top + 114), outline=PERGAMINO + (int(160 * ui * (1 - .7 * ut)),), width=3)
            colt = tuple(int(PERGAMINO[c] * (1 - ut) + GRIS[c] * ut) for c in range(3))
            for k, linea in enumerate(_partir(d, nom, fn_, paso - 16)[:2]):
                _texto(d, (cx, top + bh + 46 + k * 38), linea, fn_, colt, "mm", 255 * ui)
            if ut > 0:
                d.line((x0 - 10, top + 20, x0 - 10 + (bw + 20) * ut, top + 20 + (bh - 40) * ut), fill=ROJO + (235,), width=9)
        ur = _eo((dt - mk[n]) / .5)
        if ur > 0 and remate:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 34), remate, fr, AMBAR, "mm", 255 * ur, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def contencion(barra="Sed de batalla", freno="Serosh", grito="Hoarah Loux", remate="", icono=None, w=1500, h=460):
    """Barra de `barra` que se llena en rojo y se detiene en un broche dorado (`freno`, con el icono real si se da).
    Marca 0: se llena hasta el broche y aguanta. Marca 1: el broche se pone rojo y tiembla. Marca 2: el broche estalla, la
    barra llega al 100 % y aparece `grito` en grande. Marca 3: `remate`."""
    ftit, fb, fg, fr = fuente("r", 40), fuente("b", 34), fuente("b", 92), fuente("i", 44)
    ico = None
    if icono:
        ico = Image.open(icono).convert("RGBA")
        bb = ico.getbbox()
        ico = ico.crop(bb) if bb else ico
        ico.thumbnail((112, 112), Image.LANCZOS)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 5
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + 70, M + 52), barra.upper(), ftit, PERGAMINO, "lm", a0, track=5)
        x0, x1, cy, bh = M + 70, M + w - 70, M + h * .46, 56
        xf = x0 + (x1 - x0) * .78
        d.rounded_rectangle((x0, cy - bh / 2, x1, cy + bh / 2), 14, outline=ORO + (int(a0),), width=3,
                            fill=(20, 16, 12, int(a0 * .9)))
        u0 = _eo((dt - mk[0]) / 1.6)
        u2 = _eo((dt - mk[2]) / .5)
        xe = x0 + 6 + (xf - 30 - x0) * u0 + (x1 - 36 - xf) * u2
        if xe > x0 + 8:
            pul = .5 + .5 * math.sin(dt * 9)
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(capa).rounded_rectangle((x0 + 6, cy - bh / 2 + 6, xe, cy + bh / 2 - 6), 10,
                                                   fill=(int(150 + 60 * pul), 30, 26, 255))
            im.alpha_composite(_brillo(capa, 8, 1.0 + u2))
            d = ImageDraw.Draw(im)
        u1 = _eo((dt - mk[1]) / .3)
        tiemb = 7 * math.sin(dt * 45) * u1 * (1 - u2)
        r = 62
        if u2 < 1:
            col = tuple(int(ORO[c] * (1 - u1) + ROJO[c] * u1) for c in range(3))
            a_b = 255 * (1 - u2) * _eo((dt - .2) / .4)
            fx = xf + tiemb
            halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(halo).ellipse((fx - r - 18, cy - r - 18, fx + r + 18, cy + r + 18), fill=col + (int(110 * a_b / 255),))
            im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(16)))
            d = ImageDraw.Draw(im)
            d.ellipse((fx - r, cy - r, fx + r, cy + r), fill=(16, 12, 9, int(a_b)), outline=col + (int(a_b),), width=5)
            if ico is not None and a_b > 0:
                ic = ico.copy()
                ic.putalpha(Image.fromarray((np.array(ic.split()[3]) * (a_b / 255)).astype(np.uint8)))
                im.alpha_composite(ic, (int(fx - ic.width / 2), int(cy - ic.height / 2)))
                d = ImageDraw.Draw(im)
            if u1 > 0:
                for k in range(3):
                    ang = -1.1 + k * 1.05
                    d.line((fx, cy, fx + r * math.cos(ang) * u1, cy + r * math.sin(ang) * u1), fill=ROJO + (int(a_b),), width=3)
            _texto(d, (fx, cy + r + 32), freno, fb, col, "mm", a_b)
        if u2 > 0:
            for k in range(10):
                ang = k * .63
                dist = 40 + 260 * u2
                px, py = xf + dist * math.cos(ang), cy + dist * math.sin(ang) * .7 + 90 * u2 * u2
                d.polygon([(px, py - 12), (px + 12, py), (px, py + 12), (px - 12, py)], fill=ORO + (int(230 * (1 - u2 * .8)),))
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h * .80), grito.upper(), fg, ROJO, "mm", 255 * u2, track=8,
                   sombra=False)
            im.alpha_composite(_brillo(t2, 14, 2.0))
            d = ImageDraw.Draw(im)
        ur = _eo((dt - mk[3]) / .5)
        if ur > 0 and remate:
            _texto(d, (M + w / 2, M + h - 24), remate, fr, AMBAR, "mm", 255 * ur)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def gracia_perdida(enemigos, remate="Cuando cayó su último enemigo", titulo="La gracia en sus ojos", w=1600, h=560):
    """Dos ojos con el iris dorado de la gracia y una lista de enemigos a la izquierda. Marca i (< n): se tacha el enemigo i.
    Marca n: el iris se apaga de oro a gris ceniza. Marca n+1: `remate`."""
    ftit, fn_, fr = fuente("r", 40), fuente("b", 38), fuente("i", 46)
    n = len(enemigos)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 46), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 84, w * .3, alfa=a0)
        lx, ly = M + 90, M + 150
        paso = min(70, (h - 230) / max(1, n))
        for i, e in enumerate(enemigos):
            ui = _eo((dt - .2 - i * .15) / .35)
            ut = _eo((dt - mk[i]) / .35)
            col = tuple(int(PERGAMINO[c] * (1 - ut) + GRIS[c] * ut) for c in range(3))
            y = ly + i * paso
            _texto(d, (lx, y), e, fn_, col, "lm", 255 * ui)
            if ut > 0:
                ancho = _ancho(d, e, fn_, 0)
                d.line((lx - 6, y + 2, lx - 6 + (ancho + 12) * ut, y + 2), fill=ROJO + (235,), width=5)
        ua = _eo((dt - mk[n]) / 1.4)
        cy = M + h * .52
        for cx in (M + w * .60, M + w * .82):
            rx, ry = 150, 78
            ojo = Image.new("RGBA", im.size, (0, 0, 0, 0))
            o = ImageDraw.Draw(ojo)
            o.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(226, 216, 190, int(a0 * .9)))
            iris = tuple(int(ORO[c] * (1 - ua) + (84, 80, 74)[c] * ua) for c in range(3))
            o.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill=iris + (int(a0),))
            o.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=(10, 8, 6, int(a0)))
            msk = Image.new("L", im.size, 0)
            ImageDraw.Draw(msk).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
            ojo.putalpha(Image.fromarray(np.minimum(np.array(ojo.split()[3]), np.array(msk))))
            if ua < 1:
                hal = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(hal).ellipse((cx - 90, cy - 90, cx + 90, cy + 90), fill=ORO + (int(120 * (1 - ua) * a0 / 255),))
                im.alpha_composite(hal.filter(ImageFilter.GaussianBlur(26)))
            im.alpha_composite(ojo)
            d = ImageDraw.Draw(im)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=ORO + (int(a0),), width=4)
        ur = _eo((dt - mk[n + 1]) / .5)
        if ur > 0 and remate:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w * .71, M + h - 40), remate, fr, AMBAR, "mm", 255 * ur, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ============================================================ er_rykard_atrocidades (22-nov-2026)
def _ajustar(d, s, estilo, tam, ancho, max_lineas=2, minimo=20):
    """Fuente y líneas para que `s` quepa en `ancho` px en ≤ `max_lineas` líneas: baja el cuerpo de 2 en 2 hasta que
    quepa (tampoco deja que una palabra sola se salga)."""
    t = tam
    while True:
        f = fuente(estilo, t)
        ls = _partir(d, s, f, ancho) or [""]
        if (len(ls) <= max_lineas and max(d.textlength(x, font=f) for x in ls) <= ancho) or t <= minimo:
            return f, ls
        t -= 2


def _f_sello(d, txt, ancho, tam=92):
    """Fuente negrita para un sello de `_sello_txt` que no pase de `ancho` px (texto + marco)."""
    t = tam
    while t > 24 and d.textlength(txt, font=fuente("b", t)) + 70 > ancho:
        t -= 4
    return fuente("b", t)


def _icono(ruta, lado):
    """PNG con alfa recortado a su contenido y escalado a que su lado mayor mida `lado`."""
    if not ruta:
        return None
    ic = Image.open(ruta).convert("RGBA")
    bb = ic.getbbox()
    ic = ic.crop(bb) if bb else ic
    k = lado / max(ic.size)
    return ic.resize((max(1, int(ic.width * k)), max(1, int(ic.height * k))), Image.LANCZOS)


def _con_alfa(ic, a):
    if a >= 255:
        return ic
    c = ic.copy()
    c.putalpha(Image.fromarray((np.array(ic.split()[3]) * (max(0, a) / 255)).astype(np.uint8)))
    return c


def _mezcla(c0, c1, u):
    return tuple(int(c0[i] * (1 - u) + c1[i] * u) for i in range(3))


def _pua(d, cx, cy, r, color, a):
    """Instrumento esquemático (sin icono): estrella de púas con un aro."""
    if a <= 0:
        return
    pts = []
    for k in range(16):
        rr = r if k % 2 == 0 else r * .45
        ang = math.pi * k / 8
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(34, 26, 18, int(a)), outline=color + (int(a),))
    d.ellipse((cx - r * .3, cy - r * .3, cx + r * .3, cy + r * .3), outline=color + (int(a),), width=3)


def inquisicion(instrumentos, remate="En secreto · contra nobles", titulo="Archivo de la inquisición", w=1600, h=None):
    """Archivo de la inquisición: una ficha por instrumento de tortura. Cada elemento = «texto», (texto, icono) o
    (texto, icono, sub); icono = ruta de PNG con alfa (None = púas esquemáticas). Marca k (< n): entra la ficha k (sube y
    se enciende; su icono late en ámbar mientras es la activa). Marca n: los iconos se tiñen de rojo y cae el sello `remate`
    en su franja de abajo. Espera n + 1 marcas."""
    items = []
    for it in instrumentos:
        it = (it,) if isinstance(it, str) else tuple(it)
        items.append((it[0], it[1] if len(it) > 1 else None, it[2] if len(it) > 2 else None))
    n = max(1, len(items))
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    pad, gap = 70, 34
    cw = (w - 2 * pad - gap * (n - 1)) / n
    lado = int(min(210, cw - 40))
    icos = [_icono(ic, lado - 30) for _, ic, _ in items]
    noms = [_ajustar(tmp, t, "b", 38, cw - 28, 2) for t, _, _ in items]
    subs = [_ajustar(tmp, s, "i", 28, cw - 28, 2) if s else None for _, _, s in items]
    alto_txt = max(len(ls) * int(f.size * 1.12) + (len(ss[1]) * int(ss[0].size * 1.15) + 10 if ss else 0)
                   for (f, ls), ss in zip(noms, subs))
    ch = 24 + lado + 22 + alto_txt + 22
    ftit, fnum = fuente("r", 40), fuente("b", 30)
    fse = _f_sello(tmp, remate.upper(), w * .62, 70) if remate else None
    banda = 190 if remate else 30
    top = 120
    h = h or int(top + ch + banda)
    ys = top + ch + banda / 2

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        us = _eo((dt - mk[n]) / .35)
        lat = .5 + .5 * math.sin(dt * 4)
        for i, (texto, _, _) in enumerate(items):
            u = _eo((dt - mk[i]) / .45)
            if u <= 0:
                continue
            act = mk[i + 1] > dt >= mk[i] and i < n
            x0 = M + pad + i * (cw + gap)
            y0 = M + top + 40 * (1 - u)
            cx = x0 + cw / 2
            col = ROJO if us > .5 else AMBAR if act else ORO_OSC
            d.rectangle((x0, y0, x0 + cw, y0 + ch), fill=(18, 15, 11, int(235 * u)), outline=col + (int(255 * u),), width=2)
            bx0, by0 = cx - lado / 2, y0 + 24
            d.rectangle((bx0, by0, bx0 + lado, by0 + lado), fill=(28, 24, 18, int(255 * u)), outline=ORO_OSC + (int(200 * u),))
            if act or us > 0:
                k = (.55 + .45 * lat) * (us if not act else max(us, 1.0))
                hc = ROJO if us > .5 else AMBAR
                halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(halo).ellipse((cx - lado * .38, by0 + lado * .12, cx + lado * .38, by0 + lado * .88),
                                             fill=hc + (int(130 * k * u),))
                im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(20)))
                d = ImageDraw.Draw(im)
            ic = icos[i]
            if ic is not None:
                im.alpha_composite(_con_alfa(ic, 255 * u), (int(cx - ic.width / 2), int(by0 + (lado - ic.height) / 2)))
                d = ImageDraw.Draw(im)
            else:
                _pua(d, cx, by0 + lado / 2, lado * .32, col, 255 * u)
            _texto(d, (bx0 + 10, by0 + 8), str(i + 1), fnum, ROJO, "lt", 255 * u)
            f, ls = noms[i]
            y = by0 + lado + 22
            for ln in ls:
                _texto(d, (cx, y), ln, f, AMBAR if act else PERGAMINO, "mt", 255 * u)
                y += int(f.size * 1.12)
            if subs[i]:
                fs_, ss = subs[i]
                y += 10
                for ln in ss:
                    _texto(d, (cx, y), ln, fs_, GRIS, "mt", 255 * u)
                    y += int(fs_.size * 1.15)
        if remate and us > 0:
            _sello_txt(im, M + w / 2, M + ys, remate.upper(), fse, ROJO, 240 * us, giro=-4, escala=1 + .7 * (1 - us))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _punteada(d, p0, p1, u, fase, color, a, guion=18, hueco=12, ancho=4):
    """Línea punteada de p0 a p1 dibujada hasta la fracción `u`; `fase` (px) hace correr los guiones hacia p1."""
    if u <= 0 or a <= 0:
        return
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L < 1:
        return
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    fin, per = L * min(1, u), guion + hueco
    s = (fase % per) - per
    while s < fin:
        s0, s1 = max(0, s), min(fin, s + guion)
        if s1 > s0:
            d.line([(p0[0] + ux * s0, p0[1] + uy * s0), (p0[0] + ux * s1, p0[1] + uy * s1)], fill=color + (int(a),), width=ancho)
        s += per


def _jaula(d, cx, cy, s, color, a):
    """Celda esquemática: arco con barrotes."""
    if a <= 0:
        return
    w_, h_ = 26 * s, 34 * s
    d.rectangle((cx - w_, cy - h_ * .4, cx + w_, cy + h_), fill=(20, 14, 10, int(a)), outline=color + (int(a),), width=3)
    d.pieslice((cx - w_, cy - h_ * 1.2, cx + w_, cy + h_ * .4), 180, 360, fill=(20, 14, 10, int(a)), outline=color + (int(a),),
               width=3)
    for k in (-2, -1, 0, 1, 2):
        x = cx + k * w_ / 2.6
        d.line((x, cy - h_ * .55 + abs(k) * 4 * s, x, cy + h_), fill=color + (int(a),), width=3)


def red_secuestro(origenes, destino="Cámara de la inquisición", remate="", titulo="Red de secuestro", sub_destino=None,
                  w=1600, h=760):
    """Red de vírgenes raptoras: los `origenes` (lugares) rodean una placa central `destino` (celda + nombre). Todos salen
    apagados en gris. Marca k (< n): se enciende el origen k (onda ámbar) y sale de él una línea punteada roja que corre
    hasta la placa, por la que viajan «pasajeros»; la placa enrojece con cada línea. Marca n: `remate` abajo y la placa
    late. Espera n + 1 marcas (n si no hay remate)."""
    n = max(1, len(origenes))
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ftit = fuente("r", 40)
    labs = [_ajustar(tmp, o, "b", 34, 400, 2) for o in origenes]
    fd_, lds = _ajustar(tmp, destino, "b", 38, w * .26, 2)
    fsd_, lsd = _ajustar(tmp, sub_destino, "i", 28, w * .26, 1) if sub_destino else (None, [])
    tw = max([tmp.textlength(x, font=fd_) for x in lds] + [tmp.textlength(x, font=fsd_) for x in lsd])
    th = len(lds) * int(fd_.size * 1.1) + (len(lsd) * int(fsd_.size * 1.2) + 6 if lsd else 0)
    pw, ph = 30 + 70 + 22 + tw + 34, max(130, th + 44)
    fr_, lr = _ajustar(tmp, remate, "i", 46, w - 160, 1) if remate else (None, [])
    off = 0 if n % 2 else 180 / n
    angs = [math.radians(180 + 360 * i / n + off) for i in range(n)]
    ss = [math.sin(a) for a in angs]
    alto_lab = [len(ls) * int(f.size * 1.1) for f, ls in labs]
    lab_top = max([a for a, s in zip(alto_lab, ss) if s <= .35] or [0])
    lab_bot = max([a for a, s in zip(alto_lab, ss) if s > .35] or [0])
    ytop, ybot = 110 + lab_top + 40, h - (104 if remate else 30) - lab_bot - 40
    smin, smax = min(ss), max(ss)
    if smax - smin < .3:
        ry, cyr = 0, (ytop + ybot) / 2
    else:
        ry = (ybot - ytop) / (smax - smin)
        cyr = ytop - smin * ry
    rx = w / 2 - 230

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        cx, cy = M + w / 2, M + cyr
        conectadas = sum(_eo((dt - mk[i] - .7) / .5) for i in range(n))
        ur = _eo((dt - mk[n]) / .5) if remate else 0
        roj = min(1.0, conectadas / max(1, n))
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(capa)
        for i in range(n):
            u = _eo((dt - mk[i]) / .35)
            if u <= 0:
                continue
            px, py = cx + rx * math.cos(angs[i]), cy + ry * math.sin(angs[i])
            vx, vy = cx - px, cy - py
            L = math.hypot(vx, vy) or 1
            hw, hh = pw / 2 + 10, ph / 2 + 10
            sx = hw / abs(vx) if abs(vx) > 1e-6 else 9e9
            sy = hh / abs(vy) if abs(vy) > 1e-6 else 9e9
            s_ = 1 - min(sx, sy)
            p0 = (px + vx / L * 20, py + vy / L * 20)
            p1 = (px + vx * s_, py + vy * s_)
            ul = _eo((dt - mk[i] - .15) / .7)
            _punteada(dc, p0, p1, ul, dt * 60, ROJO, 230 * a0 / 255, ancho=5)
            if ul >= 1:
                for j in range(2):
                    f_ = ((dt - mk[i]) * .45 + j * .5) % 1
                    qx, qy = p0[0] + (p1[0] - p0[0]) * f_, p0[1] + (p1[1] - p0[1]) * f_
                    dc.ellipse((qx - 8, qy - 8, qx + 8, qy + 8), fill=(235, 90, 70, int(230 * a0 / 255)))
        im.alpha_composite(_brillo(capa, 6, .9))
        d = ImageDraw.Draw(im)
        for i in range(n):
            px, py = cx + rx * math.cos(angs[i]), cy + ry * math.sin(angs[i])
            u = _eo((dt - mk[i]) / .35)
            act = mk[i + 1] > dt >= mk[i] and i < n
            col = _mezcla(GRIS, AMBAR if act else ORO, u)
            e = dt - mk[i]
            if 0 <= e < 1.2:
                r = 16 + 14 * e
                d.ellipse((px - r, py - r, px + r, py + r), outline=AMBAR + (int(230 * (1 - e / 1.2) * a0 / 255),), width=3)
            d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=(14, 12, 9, int(a0)), outline=col + (int(a0 * (.55 + .45 * u)),),
                      width=4)
            d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=col + (int(a0 * (.4 + .6 * u)),))
            f, ls = labs[i]
            lw = max(d.textlength(x, font=f) for x in ls)
            lx = min(max(px, M + 30 + lw / 2), M + w - 30 - lw / 2)
            lh = int(f.size * 1.1)
            abajo = math.sin(angs[i]) > .35
            y = py + 36 if abajo else py - 36 - lh * len(ls)
            for ln in ls:
                _texto(d, (lx, y), ln, f, col, "mt", a0 * (.6 + .4 * u))
                y += lh
        lat = .5 + .5 * math.sin(dt * 5)
        cpl = _mezcla(ORO_OSC, ROJO, roj)
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        k = roj * (.6 + .4 * lat * (1 if ur > 0 else .5))
        ImageDraw.Draw(halo).rounded_rectangle((cx - pw / 2 - 30, cy - ph / 2 - 30, cx + pw / 2 + 30, cy + ph / 2 + 30), 30,
                                               fill=ROJO + (int(170 * k * a0 / 255),))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(22)))
        d = ImageDraw.Draw(im)
        x0, y0 = cx - pw / 2, cy - ph / 2
        d.rectangle((x0, y0, x0 + pw, y0 + ph), fill=(16, 12, 9, int(a0)), outline=cpl + (int(a0),), width=4)
        d.rectangle((x0 + 7, y0 + 7, x0 + pw - 7, y0 + ph - 7), outline=cpl + (int(a0 * .45),), width=1)
        _jaula(d, x0 + 30 + 35, cy + 4, 1.15, cpl, a0)
        y = cy - th / 2
        tx = x0 + 30 + 70 + 22
        for ln in lds:
            _texto(d, (tx, y), ln, fd_, _mezcla(PERGAMINO, (240, 120, 100), roj), "lt", a0)
            y += int(fd_.size * 1.1)
        if lsd:
            y += 6
            for ln in lsd:
                _texto(d, (tx, y), ln, fsd_, GRIS, "lt", a0)
                y += int(fsd_.size * 1.2)
        if ur > 0:
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _texto(ImageDraw.Draw(t2), (M + w / 2, M + h - 44), lr[0], fr_, AMBAR, "mm", 255 * ur, sombra=False)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _blason(d, cx, cy, r, color, a):
    """Emblema heráldico genérico (sin pretender ser el del juego): aro doble, rombo y estrella de ocho puntas."""
    if a <= 0:
        return
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(40, 14, 12, int(a)), outline=color + (int(a),), width=6)
    d.ellipse((cx - r * .84, cy - r * .84, cx + r * .84, cy + r * .84), outline=color + (int(a * .7),), width=2)
    pts = []
    for k in range(16):
        rr = r * (.72 if k % 2 == 0 else .3)
        ang = math.pi * k / 8 - math.pi / 2
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color + (int(a),))
    d.polygon([(cx, cy - r * .26), (cx + r * .2, cy), (cx, cy + r * .26), (cx - r * .2, cy)], fill=(40, 14, 12, int(a)))


def estandarte_caido(emblema="Caballeros de Gelmir", quien="", remate="Un emblema que ya nadie usa", icono=None, titulo="",
                     w=1500, h=640):
    """Estandarte carmesí con un emblema dorado (icono = PNG con alfa del emblema real; None = blasón genérico) y a la
    derecha el nombre `emblema` y `quien` (a quién representa). Marca 0: el emblema se agrieta (grietas que crecen y el oro
    se apaga a gris). Marca 1: tajo rojo en X, el estandarte se ladea y cae un poco; el nombre se tacha. Marca 2: `remate`.
    Espera 3 marcas."""
    import random
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ftit = fuente("r", 40)
    col_x0 = w * .50
    col_w = w - col_x0 - 70
    fe_, les = _ajustar(tmp, emblema, "b", 60, col_w, 2)
    fq_, lqs = _ajustar(tmp, quien, "i", 36, col_w, 3) if quien else (None, [])
    fr_, lrs = _ajustar(tmp, remate, "i", 46, col_w, 2) if remate else (None, [])
    top = 120 if titulo else 70
    bw, bh = 300, h - top - 70
    px = w * .25
    ecy = top + 30 + bh * .40
    er = 92
    ico = _icono(icono, er * 1.5)
    rng = random.Random(7)
    grietas = []
    for k in range(8):
        ang = k * math.pi / 4 + rng.uniform(-.3, .3)
        pts, x, y = [(0.0, 0.0)], 0.0, 0.0
        for j in range(7):
            ang += rng.uniform(-.5, .5)
            paso = rng.uniform(16, 30)
            x, y = x + paso * math.cos(ang), y + paso * math.sin(ang)
            pts.append((x, y))
        grietas.append(pts)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        if titulo:
            _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
            _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        ug = _eo((dt - mk[0]) / 1.4)
        ux = _eo((dt - mk[1]) / .5)
        uc = _eo((dt - mk[1] - .2) / .9)
        ur = _eo((dt - mk[2]) / .5)
        ban = Image.new("RGBA", im.size, (0, 0, 0, 0))
        db = ImageDraw.Draw(ban)
        cx, y0 = M + px, M + top + 30
        x0, x1, y1 = cx - bw / 2, cx + bw / 2, y0 + bh - 40
        ue = _eo(dt / .7)
        db.line((x0 - 26, y0 - 6, x1 + 26, y0 - 6), fill=ORO + (int(a0),), width=8)
        for xx in (x0 - 26, x1 + 26):
            db.ellipse((xx - 9, y0 - 15, xx + 9, y0 + 3), fill=ORO + (int(a0),))
        yb = y0 + (y1 - y0) * ue
        ola = 7 * math.sin(dt * 2.1) * (1 - .6 * uc)
        poly = [(x0, y0), (x1, y0), (x1 + ola, yb), (cx + ola, yb - 70 * ue), (x0 + ola, yb)]
        tela = _mezcla((112, 26, 22), (64, 30, 26), uc)
        db.polygon(poly, fill=tela + (int(a0),), outline=ORO + (int(a0),))
        db.line([(x0 + 14, y0 + 8), (x0 + 14 + ola, yb - 8)], fill=ORO_OSC + (int(a0),), width=3)
        db.line([(x1 - 14, y0 + 8), (x1 - 14 + ola, yb - 8)], fill=ORO_OSC + (int(a0),), width=3)
        ecx, ecy_ = cx + ola * .4, M + ecy
        if ue > .6:
            ae = 255 * _eo((ue - .6) / .4)
            col = _mezcla(ORO, (110, 104, 92), ug)
            if ug < 1:
                halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ImageDraw.Draw(halo).ellipse((ecx - er - 30, ecy_ - er - 30, ecx + er + 30, ecy_ + er + 30),
                                             fill=ORO + (int(110 * (1 - ug) * ae / 255),))
                ban.alpha_composite(halo.filter(ImageFilter.GaussianBlur(20)))
                db = ImageDraw.Draw(ban)
            if ico is not None:
                db.ellipse((ecx - er, ecy_ - er, ecx + er, ecy_ + er), fill=(40, 14, 12, int(ae)), outline=col + (int(ae),), width=6)
                ic = ico
                if ug > 0:
                    g = np.array(ic).astype(np.float32)
                    gris = g[..., :3].mean(axis=2, keepdims=True) * .6
                    g[..., :3] = g[..., :3] * (1 - ug) + gris * ug
                    ic = Image.fromarray(g.astype(np.uint8))
                ban.alpha_composite(_con_alfa(ic, ae), (int(ecx - ic.width / 2), int(ecy_ - ic.height / 2)))
                db = ImageDraw.Draw(ban)
            else:
                _blason(db, ecx, ecy_, er, col, ae)
            if ug > 0:
                for pts in grietas:
                    m = max(2, int(len(pts) * ug + .999))
                    pp = [(ecx + x * (er / 100) * 1.25, ecy_ + y * (er / 100) * 1.25) for x, y in pts[:m]]
                    db.line(pp, fill=(10, 7, 5, int(ae)), width=4)
                    db.line([(x + 2, y + 1) for x, y in pp], fill=PERGAMINO + (int(70 * ae / 255),), width=1)
        if ux > 0:
            db.line((x0 - 16, y0 + 10, x0 - 16 + (bw + 32) * min(1, ux * 2), y0 + 10 + (bh - 60) * min(1, ux * 2)),
                    fill=ROJO + (240,), width=13)
            if ux > .5:
                v = (ux - .5) * 2
                db.line((x1 + 16, y0 + 10, x1 + 16 - (bw + 32) * v, y0 + 10 + (bh - 60) * v), fill=ROJO + (240,), width=13)
        if uc > 0:
            ban = ban.rotate(-9 * uc, resample=Image.BICUBIC, center=(x0 - 26, y0 - 6), translate=(0, 26 * uc))
        im.alpha_composite(ban)
        d = ImageDraw.Draw(im)
        d.line((cx - bw / 2 - 26, M + top + 18, cx - bw / 2 - 26, M + h - 40), fill=ORO_OSC + (int(a0),), width=6)
        if uc > 0:
            for k in range(14):
                t_ = (dt * .35 + k * .137) % 1
                ax = M + px - bw / 2 + (k * 53) % (bw + 60) + 10 * math.sin(dt + k)
                ay = M + top + t_ * (h - top - 60)
                d.ellipse((ax - 3, ay - 3, ax + 3, ay + 3), fill=(150, 142, 126, int(160 * uc * math.sin(t_ * math.pi))))
        cxl = M + col_x0
        alto = len(les) * int(fe_.size * 1.1) + (16 + len(lqs) * int(fq_.size * 1.18) if lqs else 0) + \
            (40 + len(lrs) * int(fr_.size * 1.18) if lrs else 0)
        y = M + top + 30 + (bh - 40 - alto) / 2
        cole = _mezcla(ORO, GRIS, uc)
        for ln in les:
            _texto(d, (cxl, y), ln, fe_, cole, "lt", a0)
            if ux > 0:
                lw = d.textlength(ln, font=fe_)
                yy = y + fe_.size * .55
                d.line((cxl - 8, yy, cxl - 8 + (lw + 16) * ux, yy), fill=ROJO + (235,), width=6)
            y += int(fe_.size * 1.1)
        if lqs:
            y += 16
            for ln in lqs:
                _texto(d, (cxl, y), ln, fq_, GRIS if uc < .5 else (120, 114, 102), "lt", a0)
                y += int(fq_.size * 1.18)
        if lrs and ur > 0:
            y += 40
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dt2 = ImageDraw.Draw(t2)
            for ln in lrs:
                _texto(dt2, (cxl, y), ln, fr_, AMBAR, "lt", 255 * ur, sombra=False)
                y += int(fr_.size * 1.18)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _bolsa(bx, by, rx, ry):
    """Contorno de bolsa amniótica: óvalo con cuello atado arriba y punta de goteo abajo."""
    pts = []
    for k in range(120):
        p = 2 * math.pi * k / 120
        ancho = 1 - .62 * math.exp(-(p / .55) ** 2) - .62 * math.exp(-((2 * math.pi - p) / .55) ** 2)
        x = bx + rx * math.sin(p) * ancho
        y = by - ry * math.cos(p) + 46 * math.exp(-((p - math.pi) / .32) ** 2)
        pts.append((x, y))
    return pts


def incubadora(etiqueta="Vástago no deseado", sub="fruto de un repulsivo ritual de parto", remate="Jamás llegará a secarse",
               titulo="Amnios de serpiente", w=1500, h=700):
    """Bolsa amniótica translúcida y húmeda colgando (gotas que caen sin parar a un charco que crece) con una etiqueta de
    pergamino atada a la derecha. Marca 0: dentro se dibuja una serpiente enroscada que se mueve y la bolsa late en rojo.
    Marca 1: la etiqueta se escribe letra a letra (`etiqueta`) y luego aparece `sub`. Marca 2: `remate` bajo la etiqueta.
    Espera 3 marcas."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ftit = fuente("r", 40)
    col_x0, col_x1 = w * .55, w - 70
    tag_w = col_x1 - col_x0
    fe_, les = _ajustar(tmp, etiqueta, "b", 54, tag_w - 90, 2)
    fs_, lss = _ajustar(tmp, sub, "i", 32, tag_w - 90, 2) if sub else (None, [])
    fr_, lrs = _ajustar(tmp, remate, "i", 44, tag_w, 2) if remate else (None, [])
    tag_h = 50 + len(les) * int(fe_.size * 1.1) + (14 + len(lss) * int(fs_.size * 1.2) if lss else 0) + 40
    bx, rx = w * .29, 170
    top = 110
    ry = min(200, (h - top - 150) / 2 - 20)
    by = top + 50 + ry
    tip = by + ry + 46
    pool = h - 50
    rem_h = (36 + len(lrs) * int(fr_.size * 1.18)) if lrs else 0
    tag_y = max(top + 20, (h - tag_h - rem_h) / 2 + 10)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 44), titulo.upper(), ftit, PERGAMINO, "mm", a0, track=6)
        _filete(d, M + w / 2, M + 80, w * .3, alfa=a0)
        us = _eo((dt - mk[0]) / .9)
        ue = dt - mk[1]
        ur = _eo((dt - mk[2]) / .5)
        lat = max(0.0, math.sin(dt * 2 * math.pi * .9)) ** 6 if us > 0 else 0
        resp = 1 + .025 * math.sin(dt * 2.3) + .03 * lat
        X, Y, TIP = M + bx, M + by, M + tip
        cuerpo = _bolsa(X, Y, rx * resp, ry * resp)
        d.line((X, M + top - 10, X, Y - ry * resp + 12), fill=ORO_OSC + (int(a0),), width=4)
        d.ellipse((X - 10, Y - ry * resp, X + 10, Y - ry * resp + 18), fill=(120, 60, 46, int(a0)))
        if us > 0:
            halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(halo).polygon(_bolsa(X, Y, rx * 1.12, ry * 1.1), fill=ROJO + (int((50 + 120 * lat) * us * a0 / 255),))
            im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(26)))
        bol = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dbo = ImageDraw.Draw(bol)
        dbo.polygon(cuerpo, fill=(156, 74, 52, int(120 * a0 / 255)))
        dbo.polygon(_bolsa(X, Y + 10, rx * .8 * resp, ry * .8 * resp), fill=(176, 92, 62, int(70 * a0 / 255)))
        for k in range(5):
            ang0 = -2.4 + k * .9
            pts = [(X + rx * .9 * math.sin(ang0 + j * .12) * (1 - j * .07), Y - ry * .7 * math.cos(ang0 + j * .1) + j * 14)
                   for j in range(8)]
            dbo.line(pts, fill=(110, 30, 26, int(110 * a0 / 255)), width=2)
        if us > 0:
            ser = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ds = ImageDraw.Draw(ser)
            ond = .18 * math.sin(dt * 1.6)
            esc = (.7 + .3 * us) * resp
            tmax = 3.0 * math.pi
            prev = None
            for j in range(140):
                t = tmax * j / 139
                r = (16 + 23 * t / math.pi) * esc
                ang = t + ond + dt * .35
                x, y = X + r * math.cos(ang), Y + 16 + r * math.sin(ang) * .92
                g = (8 + 22 * t / tmax) * esc
                ds.ellipse((x - g, y - g, x + g, y + g), fill=(34, 14, 10, int(225 * us)))
                prev = (x, y, g, ang)
            x, y, g, ang = prev
            hx, hy = x + math.cos(ang + 1.3) * g * 1.4, y + math.sin(ang + 1.3) * g * 1.4
            ds.ellipse((hx - g * 1.5, hy - g * 1.15, hx + g * 1.5, hy + g * 1.15), fill=(34, 14, 10, int(225 * us)))
            ds.ellipse((hx - 5, hy - 6, hx + 5, hy + 2), fill=AMBAR + (int(255 * us),))
            msk = Image.new("L", im.size, 0)
            ImageDraw.Draw(msk).polygon(_bolsa(X, Y, rx * .93 * resp, ry * .93 * resp), fill=255)
            ser.putalpha(Image.fromarray(np.minimum(np.array(ser.split()[3]), np.array(msk))))
            bol.alpha_composite(ser)
            dbo = ImageDraw.Draw(bol)
        brillo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dbr = ImageDraw.Draw(brillo)
        dbr.arc((X - rx * .78, Y - ry * .82, X + rx * .5, Y + ry * .6), 200, 250, fill=(255, 236, 214, int(150 * a0 / 255)), width=10)
        for k in range(6):
            f_ = (dt * .18 + k / 6) % 1
            p = -1.9 + k * .62
            sx = X + rx * .82 * math.sin(p)
            sy = Y - ry * .55 + f_ * ry * 1.2
            dbr.ellipse((sx - 4, sy - 6, sx + 4, sy + 6), fill=(255, 240, 225, int(170 * math.sin(f_ * math.pi) * a0 / 255)))
        bol.alpha_composite(brillo.filter(ImageFilter.GaussianBlur(2)))
        dbo = ImageDraw.Draw(bol)
        dbo.line(cuerpo + [cuerpo[0]], fill=(214, 140, 104, int(210 * a0 / 255)), width=3)
        im.alpha_composite(bol)
        d = ImageDraw.Draw(im)
        PO = M + pool
        prx = min(150, 36 + 14 * dt)
        d.ellipse((X - prx, PO - prx * .16, X + prx, PO + prx * .16), fill=(120, 54, 40, int(200 * a0 / 255)),
                  outline=(190, 110, 84, int(160 * a0 / 255)), width=2)
        per = .85
        for k in range(3):
            t_ = (dt + k * per / 3) % per / per
            cae = TIP + 4 + (PO - TIP - 4) * t_ ** 2
            if t_ < .93:
                d.ellipse((X - 6, cae - 10, X + 6, cae + 8), fill=(196, 104, 80, int(220 * a0 / 255)))
            else:
                v = (t_ - .93) / .07
                rr = 10 + 40 * v
                d.ellipse((X - rr, PO - rr * .22, X + rr, PO + rr * .22), outline=(230, 150, 120, int(200 * (1 - v))), width=2)
        if ue > 0:
            ut = _eo(ue / .45)
            tx0, ty0 = M + col_x0, M + tag_y + 20 * (1 - ut)
            hx, hy = tx0 + 40, ty0 + 40
            d.line([(X + rx * .9, Y - ry * .2), ((X + rx + tx0) / 2, Y - ry * .2 + 60), (hx, hy)],
                   fill=(200, 180, 140, int(220 * ut)), width=3)
            pap = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dp = ImageDraw.Draw(pap)
            dp.polygon([(tx0, ty0 + 30), (tx0 + 30, ty0), (tx0 + tag_w, ty0), (tx0 + tag_w, ty0 + tag_h), (tx0 + 30, ty0 + tag_h),
                        (tx0, ty0 + tag_h - 30)], fill=(214, 198, 158, int(255 * ut)), outline=ORO_OSC + (int(255 * ut),))
            dp.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=(60, 44, 30, int(255 * ut)), outline=ORO_OSC + (int(255 * ut),),
                       width=2)
            tot = sum(len(x) for x in les)
            nv = int(tot * min(1, max(0, ue - .3) / max(.6, tot * .05)) + .999)
            y = ty0 + 50
            for ln in les:
                vis = ln[:max(0, nv)]
                nv -= len(ln)
                _texto(dp, (tx0 + 70, y), vis, fe_, CARMIN, "lt", 255 * ut, sombra=False)
                y += int(fe_.size * 1.1)
            usub = _eo((ue - .3 - max(.6, tot * .05)) / .5)
            if lss and usub > 0:
                y += 14
                for ln in lss:
                    _texto(dp, (tx0 + 70, y), ln, fs_, TINTA, "lt", 255 * usub, sombra=False)
                    y += int(fs_.size * 1.2)
            im.alpha_composite(pap)
            d = ImageDraw.Draw(im)
        if lrs and ur > 0:
            y = M + tag_y + tag_h + 36
            t2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dt2 = ImageDraw.Draw(t2)
            for ln in lrs:
                _texto(dt2, (M + col_x0, y), ln, fr_, AMBAR, "lt", 255 * ur, sombra=False)
                y += int(fr_.size * 1.18)
            im.alpha_composite(_brillo(t2, 10, 1.5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def recibo(concepto, pagador, cobrador, pago, sello="COBRADO", titulo="Recibo",
           etiquetas=("Pagado a", "Por", "Concepto", "Pago"), w=1240, h=None):
    """Recibo en pergamino con bordes dentados que se despliega. Una línea por marca, escrita a pluma letra a letra:
    marca 0 «Pagado a: `cobrador`», 1 «Por: `pagador`», 2 «Concepto: `concepto`», 3 «Pago: `pago`»; marca 4: cae el sello
    rojo `sello` en su franja de abajo (None = sin sello). Etiquetas medidas: la columna de valores empieza tras la más ancha
    y cada valor se parte en líneas si no cabe. Espera 5 marcas (4 sin sello)."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    filas = list(zip(etiquetas, (cobrador, pagador, concepto, pago)))
    ftit, fl_ = fuente("b", 50), fuente("b", 30)
    pad = 70
    x0r, x1r = 60, w - 60
    lab_w = max(_ancho(tmp, (e + ":").upper(), fl_, 3) for e, _ in filas)
    xv = x0r + pad + lab_w + 34
    val_w = x1r - pad - xv
    vals = [_ajustar(tmp, v, "i", 46, val_w, 2) for _, v in filas]
    alt = [max(56, len(ls) * int(f.size * 1.12)) + 34 for f, ls in vals]
    fse = _f_sello(tmp, sello.upper(), (x1r - x0r) * .55, 84) if sello else None
    banda = 200 if sello else 40
    cab = 150
    h = h or int(30 + cab + sum(alt) + banda + 40)
    y0r, y1r = 30, h - 30
    n = len(filas)

    def dentado(x0, y0, x1, y1):
        pts, dz = [], 22
        k = int((x1 - x0) / dz)
        for i in range(k + 1):
            pts.append((x0 + i * (x1 - x0) / k, y0 + (8 if i % 2 else 0)))
        for i in range(k, -1, -1):
            pts.append((x0 + i * (x1 - x0) / k, y1 - (8 if i % 2 else 0)))
        return pts

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        a0 = 255 * _eo(dt / .4)
        bob = 2 * math.sin(dt * 1.4)
        X0, X1, Y0, Y1 = M + x0r, M + x1r, M + y0r + bob, M + y1r + bob
        pap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dp = ImageDraw.Draw(pap)
        dp.polygon(dentado(X0, Y0, X1, Y1), fill=(218, 202, 162, 255))
        dp.rectangle((X0 + 16, Y0 + 22, X1 - 16, Y1 - 22), outline=ORO_OSC + (200,), width=2)
        _texto(dp, ((X0 + X1) / 2, Y0 + 66), titulo.upper(), ftit, TINTA, "mm", 255, track=10, sombra=False)
        _filete(dp, (X0 + X1) / 2, Y0 + 108, (X1 - X0) * .3, color=ORO_OSC)
        y = Y0 + cab
        for i, (et, _) in enumerate(filas):
            f, ls = vals[i]
            act = mk[i + 1] > dt >= mk[i]
            ue = dt - mk[i]
            ua = _eo(ue / .3)
            colet = _mezcla((150, 124, 92), CARMIN, ua if act else 0)
            yc = y + 28
            _texto(dp, (X0 + pad, yc), (et + ":").upper(), fl_, colet, "lm", 255, track=3, sombra=False)
            if act:
                dp.polygon([(X0 + pad - 34, yc - 10), (X0 + pad - 18, yc), (X0 + pad - 34, yc + 10)], fill=CARMIN + (int(255 * ua),))
            lh = int(f.size * 1.12)
            for j in range(len(ls)):
                yy = yc + j * lh + f.size * .5
                xb = X1 - pad
                k_ = X0 + (xv - x0r)
                while k_ < xb:
                    dp.line((k_, yy, min(xb, k_ + 6), yy), fill=(150, 124, 92, 170), width=2)
                    k_ += 14
            if ue > 0:
                tot = sum(len(x) for x in ls)
                nv = int(tot * min(1, ue / max(.5, tot * .045)) + .999)
                for j, ln in enumerate(ls):
                    _texto(dp, (X0 + (xv - x0r), yc + j * lh), ln[:max(0, nv)], f, TINTA, "lm", 255, sombra=False)
                    nv -= len(ln)
            y += alt[i]
        if sello:
            us = _eo((dt - mk[n]) / .35)
            if us > 0:
                _sello_txt(pap, (X0 + X1) / 2 + (X1 - X0) * .12, Y1 - 30 - banda / 2, sello.upper(), fse, CARMIN, 235 * us,
                           giro=-6, escala=1 + .8 * (1 - us))
        uabre = _eo(dt / .55)
        if uabre < 1:
            msk = Image.new("L", im.size, 0)
            ImageDraw.Draw(msk).rectangle((0, 0, im.width, Y0 + (Y1 - Y0 + 12) * uabre), fill=255)
            pap.putalpha(Image.fromarray(np.minimum(np.array(pap.split()[3]), np.array(msk))))
        im.alpha_composite(_con_alfa(pap, a0))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ er_messmer_atrocidades (24-nov-2026)
def medalla(icono=None, nombre="Insignia de cruzada", efecto="Aumenta la potencia de ataque tras derrotar a un enemigo",
            cita="estimulados por los gritos de muerte", remate="Tú la llevabas puesta", n_bajas=6, etiqueta="ATAQUE",
            w=1440, h=640):
    """Ficha de talismán con contador de bajas (la Insignia de cruzada). Marca 0: medallón con `icono` y `nombre` ·
    1: `efecto` se escribe en pergamino · 2: caen `n_bajas` marcas rojas (una cada 0,45 s) y la barra de `etiqueta` sube
    con cada una · 3: `cita` en carmín entre comillas, que late · 4: `remate` estampado sobre el medallón (None = sin
    sello). Espera 5 marcas (4 sin sello)."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    X_, W_ = 440, w - 500
    ftit = _ajustar(tmp, nombre.upper(), "b", 46, W_, 1)[0]
    fe_, le = _ajustar(tmp, efecto, "i", 38, W_, 2)
    fc_, lc = _ajustar(tmp, "«" + cita + "»", "i", 46, W_, 2)
    fl_ = fuente("b", 28)
    ic = _icono(icono, 290)
    fse = _f_sello(tmp, remate.upper(), W_ * .62, 64) if remate else None

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _panel(w, h)
        cx, cy, r = M + 215, M + h / 2, 175
        u0 = _eo((dt - mk[0]) / .5)
        if u0 > 0:
            g = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(g).ellipse((cx - r, cy - r, cx + r, cy + r), fill=(150, 50, 20, int(110 * u0)))
            im.alpha_composite(g.filter(ImageFilter.GaussianBlur(34)))
            d = ImageDraw.Draw(im)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(20, 14, 10, int(200 * u0)), outline=ORO + (int(230 * u0),), width=4)
            d.ellipse((cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12), outline=ORO_OSC + (int(200 * u0),), width=2)
            if ic:
                s = .8 + .2 * u0
                ii = ic.resize((max(1, int(ic.width * s)), max(1, int(ic.height * s))), Image.LANCZOS)
                im.alpha_composite(_con_alfa(ii, 255 * u0), (int(cx - ii.width / 2), int(cy - ii.height / 2)))
        d = ImageDraw.Draw(im)
        X = M + X_
        _texto(d, (X, M + 72), nombre.upper(), ftit, ORO, "lm", 255 * u0, track=3)
        if u0 > 0:
            d.line((X, M + 108, X + W_ * u0, M + 108), fill=ORO_OSC + (int(200 * u0),), width=2)
        ue = dt - mk[1]
        if ue > 0:
            nv = int(ue * 34)
            for j, ln in enumerate(le):
                _texto(d, (X, M + 150 + j * int(fe_.size * 1.15)), ln[:max(0, nv)], fe_, PERGAMINO, "lm", 255)
                nv -= len(ln)
        ub = dt - mk[2]
        yb = M + 150 + len(le) * int(fe_.size * 1.15) + 40
        if ub > -0.3:
            ab = 255 * _eo((ub + .3) / .3)
            k = 0 if ub < 0 else min(n_bajas, int(ub / .45) + 1)
            _texto(d, (X, yb), etiqueta, fl_, GRIS, "lm", ab, track=4)
            bx0, bx1 = X + 160, X + W_
            d.rounded_rectangle((bx0, yb - 14, bx1, yb + 14), 6, outline=ORO_OSC + (int(ab),), width=2)
            prog = .18 + .82 * (k / n_bajas) if ub >= 0 else .18
            if k and k < n_bajas:
                prog -= .82 / n_bajas * (1 - _eo((ub - (k - 1) * .45) / .3))
            col = _mezcla(ORO, CARMIN, k / n_bajas)
            d.rounded_rectangle((bx0 + 4, yb - 10, bx0 + 4 + (bx1 - bx0 - 8) * prog, yb + 10), 5, fill=col + (int(ab),))
            ys = yb + 56
            for i in range(k):
                ui = _eo((ub - i * .45) / .25)
                xs = bx0 + 20 + i * 64
                s = 15 * (1.6 - .6 * ui)
                cc = CARMIN + (int(255 * ui),)
                d.line((xs - s, ys - s, xs + s, ys + s), fill=cc, width=6)
                d.line((xs - s, ys + s, xs + s, ys - s), fill=cc, width=6)
                if ui < 1:
                    _texto(d, (xs, ys - 34 - 20 * ui), "+", fl_, AMBAR, "mm", 255 * (1 - ui))
        uc = dt - mk[3]
        if uc > 0:
            pul = .8 + .2 * math.sin(uc * 3)
            for j, ln in enumerate(lc):
                _texto(d, (X, yb + 130 + j * int(fc_.size * 1.12)), ln, fc_, CARMIN, "lm", 255 * _eo(uc / .4) * pul)
        if fse:
            us = _eo((dt - mk[4]) / .35)
            if us > 0:
                _sello_txt(im, X + W_ * .55, M + h - 85, remate.upper(), fse, CARMIN, 240 * us, giro=-6, escala=1 + .8 * (1 - us))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def _bestia(d, x, y, s, col, a, bal=0.0):
    """Bestia divina atravesada en la lanza: lomo cruzado en diagonal sobre el asta, cabeza con cuernos colgando a un lado,
    melena en hebras y cuatro patas lacias (silueta rellena con filete)."""
    if a <= 2:
        return
    c = col + (int(a),)
    dx = bal * 8
    ang = math.radians(28)
    L, R = s * 1.5, s * .48
    pts = []
    for k in range(24):
        t = 2 * math.pi * k / 24
        ex, ey = L * math.cos(t), R * math.sin(t) * (1 + .25 * math.cos(t))
        pts.append((x + dx + ex * math.cos(ang) - ey * math.sin(ang), y + ex * math.sin(ang) + ey * math.cos(ang)))
    d.polygon(pts, fill=(26, 18, 12, int(a)), outline=c)
    hx, hy = x + dx - L * math.cos(ang) * .95, y - L * math.sin(ang) * .95
    for j in range(5):
        d.line([(hx + 4 * j, hy), (hx - 6 + 5 * j + bal * 5, hy + s * (1.0 + .15 * j))], fill=c, width=2)
    d.ellipse((hx - s * .42, hy - s * .1, hx + s * .42, hy + s * .75), fill=(26, 18, 12, int(a)), outline=c, width=3)
    for sg in (-1, 1):
        cp = [(hx + sg * s * (.25 + .55 * math.sin(v * 2.0)), hy + s * (.1 - .8 * v + .3 * v * v)) for v in np.linspace(0, 1, 10)]
        d.line(cp, fill=c, width=4)
    for k, u in enumerate((-.75, -.4, .4, .75)):
        px = x + dx + L * u * math.cos(ang)
        py = y + L * u * math.sin(ang) + R * .6
        d.line([(px, py), (px + bal * 5 + (k - 1.5) * 3, py + s * (.9 + .1 * (k % 2)))], fill=c, width=4)


def empalados(n=5, titulo="Las bestias divinas", sub="destripadas, colgadas en sus lanzas y calcinadas",
              remate="Una pira funeraria para la propia torre", w=1500, h=660):
    """Marcas 0..n-1: se alza una lanza por marca con una bestia divina colgada (cabeza con cuernos y cuerpo lacio) ·
    marca n: el fuego sube desde el pie de todas, las bestias se tiñen de brasa y sale `remate`. Espera n+1 marcas."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ftit = _ajustar(tmp, titulo.upper(), "b", 44, w - 200, 1)[0]
    fsub = _ajustar(tmp, sub, "i", 34, w - 200, 1)[0]
    frem = _ajustar(tmp, remate, "i", 44, w - 200, 1)[0]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        _texto(d, (M + w / 2, M + 58), titulo.upper(), ftit, ORO, "mm", a0, track=6)
        _texto(d, (M + w / 2, M + 104), sub, fsub, PERGAMINO, "mm", a0 * .9)
        suelo = M + h - 130
        d.line((M + 80, suelo, M + w - 80, suelo), fill=ORO_OSC + (int(a0 * .7),), width=2)
        uf = _eo((dt - mk[n]) / 1.2)
        xs = [M + 190 + i * (w - 380) / max(1, n - 1) for i in range(n)]
        for i, x in enumerate(xs):
            ui = _eo((dt - mk[i]) / .6)
            if ui <= 0:
                continue
            top = suelo - (suelo - (M + 170)) * ui
            colL = _mezcla(GRIS, (120, 60, 40), uf)
            _lanza(d, x, suelo + 6, x, top, colL, 255 * ui, ancho=5)
            if ui > .6:
                ab = 255 * _eo((ui - .6) / .4)
                bal = math.sin(dt * 1.3 + i) * (1 - uf * .5)
                colB = _mezcla(PERGAMINO, (240, 110, 50), uf)
                _bestia(d, x, top + 110, 46, colB, ab, bal)
        if uf > 0:
            g = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dg = ImageDraw.Draw(g)
            for i, x in enumerate(xs):
                for k in range(3):
                    _llama(dg, x + (k - 1) * 34, suelo + 8, (140 + 60 * math.sin(dt * 2 + i + k)) * uf, 34, dt, i * 2.1 + k, 230 * uf)
            im.alpha_composite(_brillo(g, 14, 1.1))
            d = ImageDraw.Draw(im)
            _texto(d, (M + w / 2, M + h - 62), remate, frem, AMBAR, "mm", 255 * _eo((dt - mk[n] - .6) / .5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def tumba(nombres=(("Andreas", "comandante de los Caballeros Negros"), ("Huw", "capitán, su hijo")),
          motivo="Se rebelaron al conocer la naturaleza reptiliana de su señor", lloro="Messmer lloró…",
          remate="pero no los sacó", titulo="Encarcelados en una tumba subterránea", w=1500, h=680):
    """Corte del suelo. Marcas 0..k-1: cada losa con su nombre baja a su tumba bajo tierra y la atan cadenas · marca k:
    `motivo` abajo · marca k+1: una lágrima cae desde arriba y se queda en la superficie con `lloro` · marca k+2: `remate`
    en carmín al lado. Espera k+3 marcas."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    k = len(nombres)
    ftit = _ajustar(tmp, titulo.upper(), "b", 40, w - 200, 1)[0]
    fmot, lmot = _ajustar(tmp, motivo, "i", 36, w - 220, 2)
    fll = fuente("i", 44)
    fn_ = fuente("b", 46)
    fsb = fuente("i", 30)
    LAG = (170, 200, 235)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (k + 4)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .4)
        sup = M + 210
        _texto(d, (M + w / 2, M + 52), titulo.upper(), ftit, ORO, "mm", a0, track=5)
        tierra = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dt_ = ImageDraw.Draw(tierra)
        dt_.rectangle((M + 30, sup, M + w - 30, M + h - 30), fill=(44, 32, 22, int(a0 * .85)))
        for j in range(5):
            yy = sup + 60 + j * 70
            dt_.line([(M + 40 + x, yy + 6 * math.sin(x / 90 + j)) for x in range(0, w - 80, 20)], fill=(70, 54, 38, int(a0 * .7)), width=2)
        im.alpha_composite(tierra)
        d = ImageDraw.Draw(im)
        for x in range(int(M + 40), int(M + w - 40), 26):
            d.line((x, sup, x - 4, sup - 12 - 6 * math.sin(x)), fill=(120, 104, 70, int(a0 * .8)), width=2)
        d.line((M + 30, sup, M + w - 30, sup), fill=ORO_OSC + (int(a0),), width=3)
        bw, bh = 430, 126
        for i, (nom, sb) in enumerate(nombres):
            ui = _eo((dt - mk[i]) / .9)
            if ui <= 0:
                continue
            cx = M + w / 2 + (i - (k - 1) / 2) * (bw + 120)
            cy = sup - 70 + (sup + 170 - (sup - 70)) * ui
            d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 10, fill=(30, 28, 30, 245), outline=GRIS + (255,), width=3)
            _texto(d, (cx, cy - 16), nom.upper(), fn_, PERGAMINO, "mm", 255, track=4)
            _texto(d, (cx, cy + 34), sb, fsb, (190, 182, 166), "mm", 240)
            uc = _eo((dt - mk[i] - .9) / .4)
            if uc > 0:
                for sg in (-1, 1):
                    px = cx + sg * (bw / 2 + 22)
                    m = int(9 * uc)
                    for j in range(m):
                        py = cy - bh * .75 + j * bh * 1.5 / 8
                        if j % 2:
                            d.ellipse((px - 5, py - 10, px + 5, py + 10), outline=(160, 150, 140, 230), width=3)
                        else:
                            d.ellipse((px - 10, py - 6, px + 10, py + 6), outline=(160, 150, 140, 230), width=3)
        um = _eo((dt - mk[k]) / .5)
        if um > 0:
            for j, ln in enumerate(lmot):
                _texto(d, (M + w / 2, M + h - 90 + j * int(fmot.size * 1.1) - (len(lmot) - 1) * fmot.size * .55), ln, fmot, PERGAMINO, "mm", 255 * um)
        ul = dt - mk[k + 1]
        if ul > 0:
            u = _eo(ul / 1.1)
            lx, ly = M + 300, M + 90 + (sup - 22 - (M + 90)) * u
            d.ellipse((lx - 13, ly - 4, lx + 13, ly + 22), fill=LAG + (235,))
            d.polygon([(lx - 12, ly + 4), (lx + 12, ly + 4), (lx, ly - 26)], fill=LAG + (235,))
            if u >= 1:
                rr = 10 + 26 * _eo((ul - 1.1) / .6)
                d.ellipse((lx - rr * 2, sup - 4 - rr * .3, lx + rr * 2, sup - 4 + rr * .3), outline=LAG + (int(200 * (1 - _eo((ul - 1.1) / .8))),), width=2)
            tx = lx + 40
            _texto(d, (tx, M + 140), lloro, fll, LAG, "lm", 255 * _eo((ul - .3) / .4))
            ur = _eo((dt - mk[k + 2]) / .4)
            if ur > 0:
                _texto(d, (tx + d.textlength(lloro + " ", font=fll), M + 140), remate, fll, CARMIN, "lm", 255 * ur)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def sopa(nombre="Potaje de escorpión", antes="Antaño la preparaban con mimo las abuelas de la familia",
         despues="Rancio y agrio", remate="Nadie llegó a comérsela", icono=None, w=1440, h=620):
    """Cuenco (`icono` o uno por código) con vapor y un termómetro a la derecha. Marca 0: humea; `nombre` y `antes` en
    ámbar · marca 1: el vapor se apaga, el termómetro baja de ámbar a gris azulado y `despues` sale en gris frío ·
    marca 2: `remate` en carmín. Espera 3 marcas."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    X_, W_ = 640, w - 640 - 220
    ftit = _ajustar(tmp, nombre.upper(), "b", 44, W_, 1)[0]
    fan, lan = _ajustar(tmp, antes, "i", 40, W_, 3)
    fde, lde = _ajustar(tmp, despues, "i", 46, W_, 2)
    fre, lre = _ajustar(tmp, remate, "b", 40, W_, 2)
    ic = _icono(icono, 380)
    FRIO = (130, 150, 170)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        a0 = _eo((dt - mk[0]) / .5)
        cx, cy = M + 330, M + h / 2 + 60
        uf = _eo((dt - mk[1]) / 1.6)
        vap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dv = ImageDraw.Draw(vap)
        for j in range(4):
            pts = []
            for v in np.linspace(0, 1, 24):
                yy = cy - 150 - v * 230
                xx = cx - 90 + j * 60 + 26 * math.sin(v * 7 + dt * 2.2 + j) * v
                pts.append((xx, yy))
            al = 150 * a0 * (1 - uf) * (.6 + .4 * math.sin(dt * 1.7 + j))
            if al > 2:
                dv.line(pts, fill=(235, 225, 210, int(al)), width=9)
        im.alpha_composite(vap.filter(ImageFilter.GaussianBlur(6)))
        if ic:
            ii = ic if uf <= 0 else Image.blend(ic, ic.convert("LA").convert("RGBA"), .55 * uf)
            im.alpha_composite(_con_alfa(ii, 255 * a0), (int(cx - ii.width / 2), int(cy - ii.height / 2)))
        else:
            d0 = ImageDraw.Draw(im)
            d0.pieslice((cx - 170, cy - 120, cx + 170, cy + 120), 0, 180, fill=(40, 30, 22, int(255 * a0)), outline=ORO_OSC + (int(255 * a0),), width=4)
        d = ImageDraw.Draw(im)
        X = M + X_
        _texto(d, (X, M + 70), nombre.upper(), ftit, ORO, "lm", 255 * a0, track=3)
        y = M + 140
        for j, ln in enumerate(lan):
            _texto(d, (X, y + j * int(fan.size * 1.12)), ln, fan, _mezcla(AMBAR, GRIS, uf * .6), "lm", 255 * _eo((dt - mk[0] - .3) / .5))
        y += len(lan) * int(fan.size * 1.12) + 40
        ud = _eo((dt - mk[1] - .4) / .6)
        for j, ln in enumerate(lde):
            _texto(d, (X, y + j * int(fde.size * 1.12)), ln, fde, FRIO, "lm", 255 * ud)
        y += len(lde) * int(fde.size * 1.12) + 40
        ur = _eo((dt - mk[2]) / .5)
        for j, ln in enumerate(lre):
            _texto(d, (X, y + j * int(fre.size * 1.12)), ln, fre, CARMIN, "lm", 255 * ur, track=2)
        tx, t0, t1 = M + w - 110, M + 110, M + h - 150
        if a0 > 0:
            al = int(255 * a0)
            d.rounded_rectangle((tx - 16, t0, tx + 16, t1), 16, outline=PERGAMINO + (al,), width=3)
            nivel = .85 - .7 * uf
            col = _mezcla(AMBAR, FRIO, uf)
            d.rounded_rectangle((tx - 8, t1 - (t1 - t0 - 16) * nivel, tx + 8, t1), 8, fill=col + (al,))
            d.ellipse((tx - 34, t1 - 10, tx + 34, t1 + 58), fill=col + (al,), outline=PERGAMINO + (al,), width=3)
            for j in range(6):
                yy = t0 + 30 + j * (t1 - t0 - 60) / 5
                d.line((tx + 18, yy, tx + 34, yy), fill=PERGAMINO + (int(al * .7),), width=2)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def despojados(dentro="La gracia del oro", fuera=("Los cornamentados", "Sus bestias divinas", "Los Caballeros Negros", "Tú, Sinluz"),
               cita="Quienes se ven despojados del don del oro deberán hacer frente a la muerte", remate=None, w=1500, h=700):
    """Círculo dorado de la gracia en el centro y, alrededor, los que quedan FUERA. Marca 0: la `cita` se escribe arriba y
    el círculo brilla · marcas 1..n: cada nodo de `fuera` se tacha en carmín con llamas al pie · el último (`Tú`) late en
    rojo · marca n+1 (opcional): `remate` abajo. Espera n+1 marcas (+1 con remate)."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    n = len(fuera)
    fci, lci = _ajustar(tmp, "«" + cita + "»", "i", 40, w - 180, 2)
    fd = _ajustar(tmp, dentro, "b", 34, 230, 2)
    fno = fuente("r", 36)
    frem = _ajustar(tmp, remate or "", "b", 40, w - 200, 1)[0]
    angs = np.radians(np.linspace(155, 385, n)) if n > 1 else [math.pi / 2]

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 3)
        im, M = _panel(w, h)
        d = ImageDraw.Draw(im)
        uc = dt - mk[0]
        if uc > 0:
            nv = int(uc * 40)
            for j, ln in enumerate(lci):
                _texto(d, (M + w / 2, M + 60 + j * int(fci.size * 1.12)), ln[:max(0, nv)], fci, PERGAMINO, "mm", 255)
                nv -= len(ln)
        cx, cy, r = M + w / 2, M + h / 2 + 70, 135
        ua = _eo(dt / .6)
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((cx - r * 1.3, cy - r * 1.3, cx + r * 1.3, cy + r * 1.3), fill=(230, 190, 90, int(90 * ua * (.8 + .2 * math.sin(dt * 2)))))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(im)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ORO + (int(240 * ua),), width=5)
        d.ellipse((cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14), outline=ORO_OSC + (int(200 * ua),), width=2)
        f_, ls = fd
        for j, ln in enumerate(ls):
            _texto(d, (cx, cy + (j - (len(ls) - 1) / 2) * f_.size * 1.1), ln, f_, ORO, "mm", 255 * ua)
        llamas = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(llamas)
        for i, (nom, ang) in enumerate(zip(fuera, angs)):
            x, y = cx + 540 * math.cos(ang), cy + 205 * math.sin(ang)
            tw = d.textlength(nom, font=fno) + 50
            um = _eo((dt - mk[i + 1]) / .45)
            ultimo = i == n - 1
            col = _mezcla(GRIS, CARMIN, um)
            if ultimo and um > 0:
                col = _mezcla(col, (255, 90, 80), .5 + .5 * math.sin(dt * 5))
            ex, ey = cx + (r + 16) * math.cos(ang), cy + (r + 16) * math.sin(ang) * .9
            for j in range(0, 10, 2):
                u0_, u1_ = j / 10, (j + 1) / 10
                d.line((ex + (x - ex) * u0_, ey + (y - ey) * u0_, ex + (x - ex) * u1_, ey + (y - ey) * u1_), fill=GRIS + (int(150 * ua),), width=2)
            d.rounded_rectangle((x - tw / 2, y - 30, x + tw / 2, y + 30), 12, fill=(16, 12, 10, int(235 * ua)), outline=col + (int(255 * ua),), width=3)
            _texto(d, (x, y), nom, fno, _mezcla(PERGAMINO, (255, 200, 190), um * .4), "mm", 255 * ua)
            if um > 0:
                d.line((x - tw / 2 + 14, y + 2, x - tw / 2 + 14 + (tw - 28) * um, y + 2), fill=CARMIN + (240,), width=4)
                for k in range(3):
                    _llama(dl, x - tw * .3 + k * tw * .3, y + 58, (34 + 10 * math.sin(dt * 3 + k + i)) * um, 14, dt, i + k * 1.7, 220 * um)
        im.alpha_composite(_brillo(llamas, 8, 1.0))
        d = ImageDraw.Draw(im)
        if remate:
            _texto(d, (M + w / 2, M + h - 40), remate, frem, CARMIN, "mm", 255 * _eo((dt - mk[n + 1]) / .4), track=2)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn
