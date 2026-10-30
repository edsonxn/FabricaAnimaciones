# -*- coding: utf-8 -*-
"""MAPA REAL DEL JUEGO CON RUTA ANIMADA (Crónicas de Warcraft, Runa Caída, Crónicas de Tamriel y Crónicas del gaming; regla del
usuario, 23-oct-2026: «cuando hablemos de misiones o cosas que el espectador quiera saber dónde es, mostrar mapas reales del juego
con rutas; tú decides en qué escenas y cómo, adaptado cada uno a su juego»).

El mapa es la imagen REAL del juego (wiki/Wowhead/UESP, nunca dibujado ni pintado en Flow). La cámara abre sobre la zona, se
acerca despacio siguiendo la cabeza de la ruta, y la ruta se traza de lugar en lugar con las `marcas` de la voz: cuando la voz
nombra un lugar, la ruta llega ahí y aparece su marcador + su nombre. El último punto (la meta) late sin parar.
Cada juego tiene su TEMA (trazo, marcadores, letra y título como en su propia interfaz):
  "wow"     trazo amarillo a rayas que avanza (ruta de misión) con borde negro; «!» de misión al inicio, «?» de entrega en la meta;
            nombres en Georgia oro con contorno negro; el título como el rótulo de zona del juego (oro grande + subtítulo).
  "er"      hilo dorado que brilla con chispas que corren por él (la guía de la gracia); marcadores = Sitio de gracia; meta con
            anillo que late; Garamond pergamino sobre banda negra difusa; título dorado entre dos filetes (rótulo de región).
  "tes"     puntos hueso con sombra; marcador de misión de Skyrim (triángulo invertido que flota) en la meta; Bahnschrift Condensed
            en MAYÚSCULAS espaciadas sobre humo negro; título con separadores de rombo (como mg_tes).
  "gaming"  (Nintendo/plataformas de Rare) bolitas miel que brotan con rebote como el mapa de un plataformas; pines de colores;
            Arial Rounded en píldora chocolate; título Cooper Black.
  "zelda"   (aventura de fantasía) puntos dorados, triángulo dorado en la meta, Engravers MT grabado sobre banda azul noche.
  "majora"  (Majora's Mask) puntos rosa, rombo amarillo de las púas en la meta, letra del diálogo N64 sobre humo; título serifa.
  "mario64" (Super Mario 64) ruta de monedas doradas que brotan con rebote; meta = la Estrella de poder con ojos y destello; nombres
            en Arial Rounded blanco sobre humo negro (como los diálogos del juego); título con contorno grueso.
Para otro juego de Crónicas del gaming: copiar un tema de TEMAS y cambiar colores/letras a la interfaz de ESE juego.

Uso desde videos/<v>/efectos.py (FX `pantalla` si cubre el cuadro, `mg` si va en ventana):
    import mg_mapa as MP
    dict(tipo="pantalla", fn=MP.mapa(os.path.join(_AQUI, "mapas", "elwynn.jpg"),
             [(.62, .30, "Villanorte", "inicio"), (.55, .52), (.42, .60, "Villadorada"), (.20, .72, "Páramos de Poniente", "meta")],
             tema="wow", titulo="Bosque de Elwynn", sub="Territorio de la Alianza"),
         de="Todo empieza en Villanorte", a=("Poniente|fin", 1.5), marcas=["Villanorte", "Villadorada", "Poniente"],
         entra=.5, sale=.5, nombre="mapa elwynn")
  puntos = (x, y) de PASO (sin marcador; da forma a la ruta para que siga caminos) o (x, y, "Nombre"[, tipo]) con tipo
  "inicio" | "paso" (por defecto) | "meta" (el último con nombre es meta si no se dice) | "peligro" (jefe, zona letal).
  FOTO (regla del usuario, 23-oct-2026, TODO mapa de cualquier canal): (x, y, "Nombre", tipo, foto) — la imagen REAL de lo que
  la voz nombra en ese lugar (personaje, sitio u objeto que hay que juntar): ruta a .png/.jpg (pegatina) o "ico:<ícono de
  Wowhead>"; sale junto al marcador con rebote cuando la ruta llega y se va al llegar al siguiente. Sin imagen real: None.
  x, y en fracción de la imagen (tras `recorte`). Para leerlas: `python nucleo/mg_mapa.py rejilla <imagen> [x0 y0 x1 y1]`.
  marcas: una por lugar CON nombre (la 1.ª = aparece el inicio; cada siguiente = la ruta llega a ese lugar). Sin marcas se
  reparten solas en la duración.
  modo="ventana" (FX `mg`, x/y del FX): el mapa en un recuadro de bordes difuminados (`ancho` px) sobre el clip, para ubicar
  algo en 3-5 s sin tapar el gameplay; modo="pantalla" (por defecto): cuadro entero, para las rutas de misión largas.
  recorte=(x0, y0, x1, y1) en fracción: recorta mapas gigantes (el de las Tierras Intermedias tiene 9644 px) a la zona.
  Si la ruta no cabe entera en pantalla (mapa chico para una ruta larga), la cámara la va siguiendo y los nombres que quedan
  bajo el título se ocultan: mejor un mapa de región, o partirla en dos mapas.
Probar SIEMPRE con la hoja ANTES de `fx`: `MP.hoja(fn, dur, marcas, salida)` (2x3 cuadros; MÍRALA) y luego `fx hoja`.
  margen (zona segura a los lados), zoom (respiración de la cámara, 1.05), ajuste (0..1: cuánto encuadra la ruta ENTERA desde
  el principio; 0 = la cámara va descubriendo la ruta), traza (s máx. que tarda cada tramo en dibujarse, 1,7; un recorrido
  largo con solo inicio y meta: traza=99 = se dibuja durante todo el tramo). La cámara no sale de la imagen ni amplía el
  original más de `amp_max` (2,0 px de salida por px del mapa; el mínimo es lo que haga falta para llenar la pantalla): con un
  mapa chico (los de Wowhead Classic miden 1024 px) y dos puntos juntos, antes llegaba a 13x y se veía pixelado (29-oct-2026).
  viajeros=[ruta .png/.jpg, ...]: quien se MUEVE por la ruta (personajes, unidades) va en ella como pegatina redonda pequeña
  con su imagen REAL del juego, en la punta del trazo (varios, en fila detrás); regla del usuario, 29-oct-2026.
"""
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

Image.MAX_IMAGE_PIXELS = None
_F = "C:/Windows/Fonts/"
_fc, _sc = {}, {}


def _fuente(nombre, tam, variacion=None):
    k = (nombre, tam, variacion)
    if k not in _fc:
        f = ImageFont.truetype(_F + nombre, tam)
        if variacion:
            try:
                f.set_variation_by_name(variacion)
            except Exception:
                pass
        _fc[k] = f
    return _fc[k]


# ------------------------------------------------------------------ temas (colores RGB)
TEMAS = {
    "wow": dict(trazo="rayas", color=(255, 209, 0), borde=(0, 0, 0), grueso=6, letra=("georgiab.ttf", 46, None),
                texto=(255, 209, 0), contorno=(0, 0, 0), titulo=("georgiab.ttf", 92, None), subt=("georgia.ttf", 40, None),
                tinte=(1.0, 1.0, 1.0, 0.0), fondo=(18, 14, 8)),
    "er": dict(trazo="hilo", color=(232, 196, 110), borde=(40, 28, 8), grueso=4, letra=("GARABD.TTF", 52, None),
               texto=(236, 226, 198), contorno=None, titulo=("GARA.TTF", 96, None), subt=("GARAIT.TTF", 40, None),
               tinte=(.88, .86, .80, .06), fondo=(10, 10, 12)),
    "tes": dict(trazo="puntos", color=(236, 230, 214), borde=(10, 10, 10), grueso=5, letra=("bahnschrift.ttf", 46, "SemiBold Condensed"),
                texto=(236, 230, 214), contorno=None, titulo=("bahnschrift.ttf", 84, "Condensed"),
                subt=("bahnschrift.ttf", 34, "SemiBold Condensed"), tinte=(.84, .84, .84, .12), fondo=(8, 8, 9)),
    "gaming": dict(trazo="bolitas", color=(255, 196, 60), borde=(70, 38, 16), grueso=11, letra=("ARLRDBD.TTF", 42, None),
                   texto=(255, 244, 220), contorno=None, titulo=("COOPBL.TTF", 96, None), subt=("ARLRDBD.TTF", 38, None),
                   tinte=(1.06, 1.06, 1.06, -.04), fondo=(40, 24, 10), caja=(70, 38, 16), filo=(255, 196, 60)),
    "zelda": dict(trazo="puntos", color=(246, 206, 110), borde=(30, 22, 10), grueso=6, letra=("ENGR.TTF", 36, None),
                  texto=(250, 240, 215), contorno=None, titulo=("ENGR.TTF", 72, None), subt=("ANTQUABI.TTF", 38, None),
                  tinte=(.95, .95, .95, .05), fondo=(8, 10, 22), caja=(8, 10, 22), filo=(246, 206, 110)),
    # Majora's Mask (majora_mask, 23-oct-2026): ruta de puntos ROSA (ojos de la máscara), meta = rombo amarillo de sus púas,
    # nombres en la letra del diálogo de N64 sobre humo negro, título en la serifa blanca del cartel «Amanecer del primer día».
    "majora": dict(trazo="puntos", color=(255, 92, 150), borde=(40, 10, 50), grueso=6, letra=("ARLRDBD.TTF", 40, None),
                   texto=(250, 250, 248), contorno=None, titulo=("georgiab.ttf", 84, None), subt=("georgiaz.ttf", 38, None),
                   tinte=(.92, .90, .96, .06), fondo=(10, 4, 18)),
    # Super Mario 64 (mario64_secretos, 29-oct-2026): ruta de MONEDAS amarillas (bolitas con rebote y borde naranja), meta = la
    # Estrella de poder; nombres en la letra redonda del diálogo sobre humo negro, título blanco con contorno grueso.
    "mario64": dict(trazo="bolitas", color=(255, 214, 0), borde=(176, 96, 0), grueso=10, letra=("ARLRDBD.TTF", 40, None),
                    texto=(250, 250, 248), contorno=None, titulo=("ARLRDBD.TTF", 84, None), subt=("ARLRDBD.TTF", 38, None),
                    tinte=(1.0, 1.0, 1.0, 0.0), fondo=(10, 30, 60)),
}


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _pop(dt, dur=0.4):
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1.6 else 1 - math.exp(-6 * u) * math.cos(9 * u)


def _bgra(im):
    return np.array(im.convert("RGBA"))[..., [2, 1, 0, 3]].copy()


def _pegar(f, spr, cx, cy, alfa=1.0, esc=1.0):
    """spr BGRA (np) sobre f BGR (np, se modifica) centrado en (cx, cy)."""
    if alfa <= 0.01 or esc <= 0.02:
        return
    if abs(esc - 1) > .01:
        spr = cv2.resize(spr, (max(2, int(spr.shape[1] * esc)), max(2, int(spr.shape[0] * esc))), interpolation=cv2.INTER_LINEAR)
    h, w = spr.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(f.shape[1], x0 + w), min(f.shape[0], y0 + h)
    if X1 <= X0 or Y1 <= Y0:
        return
    s = spr[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    a = s[..., 3:4].astype(np.float32) / 255 * alfa
    f[Y0:Y1, X0:X1] = (f[Y0:Y1, X0:X1] * (1 - a) + s[..., :3] * a).astype(np.uint8)


def _track(d, s, f, track):
    return sum(d.textlength(c, font=f) for c in s) + track * max(0, len(s) - 1)


def _escribe(d, x, y, s, f, color, track=0, stroke=0, stroke_color=None):
    """Texto con espaciado `track` empezando en (x, y) (ancla izquierda-centro)."""
    if not track:
        d.text((x, y), s, font=f, fill=color, anchor="lm", stroke_width=stroke, stroke_fill=stroke_color)
        return
    for c in s:
        d.text((x, y), c, font=f, fill=color, anchor="lm", stroke_width=stroke, stroke_fill=stroke_color)
        x += d.textlength(c, font=f) + track


# ------------------------------------------------------------------ sprites por tema (se calculan una vez)
def _cache(k, hacer):
    if k not in _sc:
        _sc[k] = hacer()
    return _sc[k]


def _halo(r, color, fuerza=200):
    im = Image.new("RGBA", (r * 4, r * 4), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse((r, r, 3 * r, 3 * r), fill=fuerza)
    m = m.filter(ImageFilter.GaussianBlur(r * .55))
    c = Image.new("RGBA", im.size, color + (255,))
    c.putalpha(m)
    return c


def _marcador(tema, tipo):
    """Sprite BGRA del marcador de un lugar (centro del sprite = el lugar, salvo los que flotan encima)."""
    def hacer():
        T = TEMAS[tema]
        S = 160
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        c = S / 2
        rojo = (214, 44, 32)
        if tema == "wow":
            if tipo in ("inicio", "meta"):
                im.alpha_composite(_halo(30, (255, 200, 40), 150), (int(c - 60), int(c - 60)))
                g = "!" if tipo == "inicio" else "?"
                d.text((c, c), g, font=_fuente("georgiab.ttf", 92), fill=(255, 209, 0), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
            elif tipo == "peligro":
                d.ellipse((c - 24, c - 24, c + 24, c + 24), fill=rojo, outline=(0, 0, 0), width=5)
                d.text((c, c + 1), "!", font=_fuente("georgiab.ttf", 36), fill=(255, 255, 255), anchor="mm")
            else:
                d.ellipse((c - 15, c - 15, c + 15, c + 15), fill=(255, 209, 0), outline=(0, 0, 0), width=5)
        elif tema == "er":
            col = rojo if tipo == "peligro" else (250, 214, 130)
            im.alpha_composite(_halo(34 if tipo == "meta" else 24, col, 170), (int(c - (68 if tipo == "meta" else 48)),) * 2)
            r = 13 if tipo == "meta" else 10
            for k in range(8):                              # rayos del Sitio de gracia
                a = k * math.pi / 4
                l1, l2 = r + 4, r + (20 if k % 2 == 0 else 12)
                d.line([(c + l1 * math.cos(a), c + l1 * math.sin(a)), (c + l2 * math.cos(a), c + l2 * math.sin(a))],
                       fill=col + (230,), width=3)
            d.ellipse((c - r, c - r, c + r, c + r), fill=(255, 240, 200), outline=col, width=3)
        elif tema == "tes":
            if tipo == "meta":                              # marcador de misión: triángulo invertido con borde negro
                p = [(c - 26, c - 64), (c + 26, c - 64), (c, c - 18)]
                d.polygon([(x, y + 4) for x, y in p], fill=(0, 0, 0, 150))
                d.polygon(p, fill=(236, 230, 214), outline=(10, 10, 10), width=4)
                d.ellipse((c - 7, c - 7, c + 7, c + 7), fill=(236, 230, 214), outline=(10, 10, 10), width=3)
            else:
                col = (196, 38, 30) if tipo == "peligro" else (236, 230, 214)
                r = 16 if tipo == "inicio" else 12
                d.polygon([(c, c - r - 4), (c + r + 4, c), (c, c + r + 4), (c - r - 4, c)], fill=(10, 10, 10, 200))
                d.polygon([(c, c - r), (c + r, c), (c, c + r), (c - r, c)], fill=col)
        elif tema == "gaming":
            col = {"meta": (232, 48, 40), "peligro": (150, 60, 200), "inicio": (60, 140, 230)}.get(tipo, (255, 196, 60))
            d.ellipse((c - 22, c - 4, c + 22, c + 8), fill=(0, 0, 0, 90))            # sombra en el suelo
            d.polygon([(c - 22, c - 44), (c + 22, c - 44), (c, c)], fill=T["borde"])  # pin
            d.ellipse((c - 30, c - 82, c + 30, c - 22), fill=T["borde"])
            d.polygon([(c - 16, c - 42), (c + 16, c - 42), (c, c - 8)], fill=col)
            d.ellipse((c - 24, c - 76, c + 24, c - 28), fill=col)
            if tipo == "meta":
                pts = [(c + 15 * math.cos(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else .45),
                        c - 52 + 15 * math.sin(-math.pi / 2 + k * math.pi / 5) * (1 if k % 2 == 0 else .45)) for k in range(10)]
                d.polygon(pts, fill=(255, 240, 120))
            else:
                d.ellipse((c - 9, c - 61, c + 9, c - 43), fill=(255, 250, 235))
        elif tema == "majora":
            col = (255, 80, 80) if tipo == "peligro" else T["color"]
            if tipo == "meta":                              # rombo amarillo de las púas con el ojo rosa
                im.alpha_composite(_halo(30, (255, 206, 60), 150), (int(c - 60), int(c - 60)))
                p = [(c, c - 34), (c + 26, c), (c, c + 34), (c - 26, c)]
                d.polygon(p, fill=(250, 206, 60), outline=T["borde"], width=4)
                d.ellipse((c - 10, c - 10, c + 10, c + 10), fill=col, outline=T["borde"], width=3)
            else:
                r = 14 if tipo == "inicio" else 11
                d.ellipse((c - r - 5, c - r - 5, c + r + 5, c + r + 5), fill=(120, 50, 160))
                d.ellipse((c - r, c - r, c + r, c + r), fill=col)
        elif tema == "mario64":
            if tipo == "meta":                              # la Estrella de poder (mg_mario64) con halo
                import mg_mario64 as M64
                im.alpha_composite(_halo(34, (255, 230, 90), 160), (int(c - 68), int(c - 68)))
                st = M64.estrella(96)
                im.alpha_composite(st, (int(c - st.width / 2), int(c - st.height / 2)))
            elif tipo == "peligro":                         # Bob-omb: bola negra con mecha
                d.ellipse((c - 22, c - 22, c + 22, c + 22), fill=(20, 20, 24), outline=(232, 40, 40), width=4)
                d.line([(c + 8, c - 22), (c + 16, c - 34)], fill=(230, 200, 120), width=4)
            else:                                           # moneda amarilla de canto grueso
                r = 17 if tipo == "inicio" else 14
                d.ellipse((c - r - 4, c - r - 4, c + r + 4, c + r + 4), fill=T["borde"])
                d.ellipse((c - r, c - r, c + r, c + r), fill=T["color"])
                d.rectangle((c - 3, c - r * .55, c + 3, c + r * .55), fill=(255, 246, 170))
        elif tema == "zelda":
            col = (214, 44, 32) if tipo == "peligro" else T["color"]
            if tipo == "meta":                              # triángulo dorado
                im.alpha_composite(_halo(28, (255, 214, 120), 150), (int(c - 56), int(c - 56)))
                p = [(c, c - 30), (c + 30, c + 22), (c - 30, c + 22)]
                d.polygon(p, fill=col, outline=(70, 46, 10), width=4)
                d.polygon([(c, c + 22), (c + 15, c - 4), (c - 15, c - 4)], fill=(70, 46, 10))
            else:
                r = 14 if tipo == "inicio" else 11
                d.ellipse((c - r - 4, c - r - 4, c + r + 4, c + r + 4), fill=T["borde"])
                d.ellipse((c - r, c - r, c + r, c + r), fill=col)
        return _bgra(im)
    return _cache(("marc", tema, tipo), hacer)


def _etiqueta(tema, texto, tipo):
    """Sprite BGRA con el nombre del lugar."""
    def hacer():
        T = TEMAS[tema]
        nom, tam, var = T["letra"]
        f = _fuente(nom, tam, var)
        s = texto.upper() if tema in ("tes", "zelda") else texto
        track = 3 if tema == "tes" else (2 if tema == "zelda" else 0)
        dd = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw = int(_track(dd, s, f, track))
        P = 34
        w, h = tw + 2 * P + 40, tam + 2 * P
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        x0, cy = (w - tw) / 2, h / 2
        col = (226, 70, 56) if tipo == "peligro" else T["texto"]
        if tema == "wow":
            _escribe(d, x0, cy, s, f, (255, 120, 90) if tipo == "peligro" else col, stroke=4, stroke_color=(0, 0, 0))
        elif tema in ("er", "tes", "majora", "mario64"):    # banda/humo negro difuso detrás
            m = Image.new("L", im.size, 0)
            ImageDraw.Draw(m).rounded_rectangle((P - 6, P - 2, w - P + 6, h - P + 2), 20, fill=200)
            m = m.filter(ImageFilter.GaussianBlur(14))
            n = Image.new("RGBA", im.size, (6, 6, 8, 255))
            n.putalpha(m)
            im.alpha_composite(n)
            d = ImageDraw.Draw(im)
            _escribe(d, x0, cy, s, f, col, track=track)
        else:                                               # píldora (gaming / zelda)
            d.rounded_rectangle((x0 - 22, cy - tam * .72, x0 + tw + 22, cy + tam * .72), radius=int(tam * .72),
                                fill=T["caja"] + (225,), outline=T["filo"] + (255,), width=4 if tema == "gaming" else 2)
            _escribe(d, x0, cy + (2 if tema == "zelda" else 0), s, f, col, track=track)
        return _bgra(im)
    return _cache(("etq", tema, texto, tipo), hacer)


def _titulo(tema, titulo, sub):
    def hacer():
        T = TEMAS[tema]
        nom, tam, var = T["titulo"]
        f = _fuente(nom, tam, var)
        fs = _fuente(*T["subt"])
        s = titulo.upper() if tema in ("er", "tes", "zelda") else titulo
        track = {"er": 10, "tes": 9, "zelda": 6, "majora": 3}.get(tema, 0)
        dd = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw = int(_track(dd, s, f, track))
        sw = int(dd.textlength(sub or "", font=fs))
        w = max(tw, sw) + 520
        h = tam + (tam * .9 if sub else 0) + 120
        im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)                      # sombra/humo para que se lea sobre cualquier mapa
        ImageDraw.Draw(m).rounded_rectangle((180, 40, w - 180, h - 40), 40, fill=170 if tema != "wow" else 120)
        m = m.filter(ImageFilter.GaussianBlur(34))
        n = Image.new("RGBA", im.size, (4, 4, 6, 255))
        n.putalpha(m)
        im.alpha_composite(n)
        d = ImageDraw.Draw(im)
        cx, y = w / 2, 60 + tam / 2
        if tema == "wow":
            _escribe(d, cx - tw / 2, y, s, f, (255, 209, 0), stroke=5, stroke_color=(0, 0, 0))
        elif tema == "gaming":
            _escribe(d, cx - tw / 2, y, s, f, T["color"], stroke=8, stroke_color=T["borde"])
        elif tema == "mario64":
            _escribe(d, cx - tw / 2, y, s, f, (255, 255, 255), stroke=7, stroke_color=(20, 12, 6))
        else:
            _escribe(d, cx - tw / 2, y, s, f, T["color"] if tema in ("er", "zelda") else T["texto"], track=track)
            ly = y + tam * .62                               # filetes que se desvanecen hacia fuera (rombo al centro en tes)
            half = tw / 2 + 60
            for k in range(60):
                a = int(230 * (1 - k / 60))
                for sgn in (-1, 1):
                    x0 = cx + sgn * (k / 60) * half
                    d.line([(x0, ly), (x0 + sgn * half / 60, ly)], fill=T["color"] + (a,), width=2)
            if tema in ("tes", "majora"):
                d.polygon([(cx, ly - 9), (cx + 9, ly), (cx, ly + 9), (cx - 9, ly)],
                          fill=(250, 206, 60) if tema == "majora" else T["color"])
        if sub:
            col = (255, 255, 255) if tema == "wow" else T["texto"]
            st = (0, 0, 0) if tema in ("wow", "gaming", "mario64") else None
            d.text((cx, y + tam * .62 + tam * .45 + 6), sub, font=fs, fill=col, anchor="mm", stroke_width=3 if st else 0, stroke_fill=st)
        return _bgra(im)
    return _cache(("tit", tema, titulo, sub), hacer)


# ------------------------------------------------------------------ geometría
def _catmull(p, pasos=28):
    """Curva suave que pasa por todos los puntos; devuelve (N, 2) y el índice de muestra de cada punto original."""
    p = np.asarray(p, np.float64)
    if len(p) < 2:
        return p.copy(), [0]
    q = np.vstack([p[0] * 2 - p[1], p, p[-1] * 2 - p[-2]])
    out, idx = [p[0]], [0]
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(1, pasos + 1):
            t = k / pasos
            out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        idx.append(len(out) - 1)
    return np.array(out), idx


def _hasta(curva, L, largo):
    """Puntos de la curva hasta la longitud `largo` (el último interpolado)."""
    if largo <= 0:
        return curva[:1]
    i = int(np.searchsorted(L, largo))
    if i >= len(L):
        return curva
    u = (largo - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
    return np.vstack([curva[:i], curva[i - 1] + (curva[i] - curva[i - 1]) * u])


# ------------------------------------------------------------------ el MG
def mapa(ruta, puntos, tema="wow", **kw):
    """Mapa REAL con ruta animada; ver el docstring del módulo. Devuelve fn(dt, dur, marcas) -> BGRA.
    Perezoso: la imagen se carga en el primer cuadro (efectos.py se importa en cada proceso de render)."""
    if not os.path.exists(ruta):
        raise SystemExit(f"mg_mapa: no existe el mapa {ruta}")
    if tema not in TEMAS:
        raise SystemExit(f"mg_mapa: tema «{tema}» desconocido (hay {', '.join(TEMAS)})")
    real = []

    def fn(dt, dur, marcas):
        if not real:
            real.append(_mapa(ruta, puntos, tema, **kw))
        return real[0](dt, dur, marcas)
    return fn


def _medalla(fuente_img, d, color):
    """Pegatina redonda de quien viaja por la ruta: su imagen REAL (recorte cuadrado desde arriba, donde está la cara),
    aro del color del tema, borde blanco de pegatina y sombra. RGBA (PIL)."""
    im = Image.open(fuente_img).convert("RGBA")
    lado = min(im.width, im.height)
    im = im.crop(((im.width - lado) // 2, 0, (im.width - lado) // 2 + lado, lado)).resize((d, d), Image.LANCZOS)
    fondo = Image.new("RGBA", (d, d), (8, 10, 26, 255))
    fondo.alpha_composite(im)
    M, a1, a2 = 16, max(3, d // 22), max(2, d // 40)
    out = Image.new("RGBA", (d + 2 * M, d + 2 * M), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((M - a1 - a2 + 3, M - a1 - a2 + 7, M + d + a1 + a2 + 3, M + d + a1 + a2 + 7), fill=(0, 0, 0, 190))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    dr = ImageDraw.Draw(out)
    dr.ellipse((M - a1 - a2, M - a1 - a2, M + d + a1 + a2, M + d + a1 + a2), fill=(245, 240, 228, 255))
    dr.ellipse((M - a1, M - a1, M + d + a1, M + d + a1), fill=tuple(int(c) for c in color) + (255,))
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    out.paste(fondo, (M, M), m)
    return out


def _mapa(ruta, puntos, tema="wow", titulo=None, sub=None, recorte=None, modo="pantalla", ancho=1100, alto=None,
          margen=.16, zoom=1.05, ajuste=.30, traza=1.7, amp_max=2.0, viajeros=None, W=1920, H=1080):
    T = TEMAS[tema]
    im = Image.open(ruta).convert("RGB")
    if recorte:
        x0, y0, x1, y1 = recorte
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    ventana = modo == "ventana"
    VW, VH = (int(ancho), int(alto or ancho * .62)) if ventana else (W, H)

    pts = [(float(p[0]) * im.width, float(p[1]) * im.height) for p in puntos]
    # FOTO por lugar (regla del 23-oct-2026, todo mapa de cualquier canal): 5.º elemento = imagen real de lo que la voz nombra
    # ahí (personaje, lugar u objeto): ruta a .png/.jpg o "ico:<ícono de Wowhead>" (mg_wow._foto: marco dorado, giro leve)
    fotos = {}
    for i, p in enumerate(puntos):
        if len(p) > 4 and p[4]:
            import mg_wow
            fotos[i] = _bgra(mg_wow._foto(p[4], alto=int(280 * (.62 if modo == "ventana" else 1)), giro=(-4 if i % 2 else 4)))
    viaj = [_bgra(_medalla(v, int(140 * (.62 if ventana else 1)), T["color"])) for v in (viajeros or [])]
    lug = [(i, p[2], (p[3] if len(p) > 3 else None)) for i, p in enumerate(puntos) if len(p) > 2 and p[2]]
    if not lug:
        raise ValueError("mg_mapa.mapa: hace falta al menos un punto con nombre")
    lug = [(i, n, t or ("inicio" if k == 0 and len(lug) > 1 else ("meta" if k == len(lug) - 1 else "paso")))
           for k, (i, n, t) in enumerate(lug)]

    # ZONA SEGURA de la pantalla donde se encuadra la ruta (arriba queda la franja del título; abajo, aire para los nombres)
    esc_t, y_t, rect_t = (.62 if ventana else 1.0), (6 if ventana else 18), None
    S1 = VH * .12
    if titulo:                                              # caja visible del título: los nombres la esquivan y la ruta va debajo
        tt0 = _titulo(tema, titulo, sub)
        ys, xs = np.nonzero(tt0[..., 3] > 200)
        rect_t = (VW / 2 + (xs.min() - tt0.shape[1] / 2) * esc_t - 10, y_t + ys.min() * esc_t - 8,
                  VW / 2 + (xs.max() - tt0.shape[1] / 2) * esc_t + 10, y_t + ys.max() * esc_t + 8)
        S1 = rect_t[3] + {"gaming": 118, "tes": 100}.get(tema, 70) * (.9 if ventana else 1)
    S0, S2, S3 = VW * margen * .45, VW * (1 - margen * .45), VH * .88
    SW, SH = S2 - S0, S3 - S1
    a = np.array(pts)
    lado_min = max(im.width, im.height) * .05
    fw, fh = max(np.ptp(a[:, 0]), lado_min), max(np.ptp(a[:, 1]), lado_min)
    s_min_n = max(VW / im.width, VH / im.height)            # (px de salida por px del original) la vista no se sale de la imagen
    s_full_n = max(s_min_n, min(SW / fw, SH / fh))          # toda la ruta en la zona segura
    s_max_n = max(s_full_n, min(1.6, s_full_n * 2.2))       # lo más cerca: el doble que la vista entera, sin ampliar > 1,6x
    s_max_n = max(s_min_n, min(s_max_n, amp_max))           # …ni más de amp_max el original (pixelado), salvo para llenar la vista
    k = min(s_max_n * 1.05, 4200 / max(im.size))            # base de trabajo ≈ 1:1 en la vista más cerrada (≤ 4200 px)

    base = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.LANCZOS)
    arr = np.array(base)[..., ::-1].astype(np.float32)
    g, b0 = T["tinte"][:3], T["tinte"][3]
    gris = arr.mean(2, keepdims=True)
    arr = gris + (arr - gris) * g[0]                        # saturación
    arr = np.clip(arr * (1 - b0), 0, 255).astype(np.uint8)                # brillo (b0 < 0 aclara)
    pts_b = np.array(pts) * k
    curva, idx = _catmull(pts_b)
    L = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(curva, axis=0).T))])
    Lk = [L[idx[i]] for i, _, _ in lug]
    fondo = tuple(int(v) for v in T["fondo"][::-1])
    fb = np.array([*curva.min(0), *curva.max(0)])        # caja de la ruta entera (base)

    # viñeta (y en ventana, el alfa de bordes difuminados)
    yy, xx = np.mgrid[0:VH, 0:VW].astype(np.float32)
    rr = np.sqrt(((xx - VW / 2) / (VW / 2)) ** 2 + ((yy - VH / 2) / (VH / 2)) ** 2)
    vin = np.clip(1 - .55 * np.clip(rr - .55, 0, 1) ** 1.6, 0, 1)[..., None]
    if ventana:
        ex = np.minimum(xx, VW - 1 - xx) / (VW * .07)
        ey = np.minimum(yy, VH - 1 - yy) / (VH * .10)
        alfa_v = (np.clip(np.minimum(ex, ey), 0, 1) ** 1.3 * 255).astype(np.uint8)

    def tiempos(dur, marcas):
        n = len(lug)
        mk = list(marcas)[:n]
        if len(mk) < n:                                     # sin marcas (o faltan): las que faltan, repartidas hasta el final
            ini = mk[-1] + .9 if mk else .45
            fin = max(ini, dur - 1.4)
            resto = n - len(mk)
            mk += [ini + (fin - ini) * j / max(1, resto - 1) for j in range(resto)]
        return mk

    def fn(dt, dur, marcas):
        mk = tiempos(dur, marcas)
        # largo de ruta dibujado: tramo k se traza en [max(mk[k-1]+.2, mk[k]-traza), mk[k]] (traza = s máx. por tramo: 1,7 en
        # misiones; un recorrido largo con solo inicio y meta, p. ej. traza=99 = se dibuja durante todo el tramo)
        largo = 0.0
        for j in range(1, len(lug)):
            t0 = max(mk[j - 1] + .2, mk[j] - traza)
            if dt >= mk[j]:
                largo = Lk[j]
            elif dt > t0:
                u = (dt - t0) / max(.05, mk[j] - t0)
                u = u * u * (3 - 2 * u)
                largo = Lk[j - 1] + (Lk[j] - Lk[j - 1]) * u
                break
            else:
                largo = Lk[j - 1] if dt >= mk[j - 1] else 0.0
                break
        if len(lug) == 1:
            largo = 0.0
        hecho = _hasta(curva, L, largo)
        cabeza = hecho[-1]

        # cámara: encuadra lo ya recorrido (mezclado con la ruta entera) dentro de la zona segura; abre un poco más ancha,
        # respira despacio y nunca deja la cabeza de la ruta fuera de la zona segura
        pb = np.array([*hecho.min(0), *hecho.max(0)])
        bb = pb + (fb - pb) * ajuste
        w = max(bb[2] - bb[0], (fb[2] - fb[0]) * .5, lado_min * k)
        h = max(bb[3] - bb[1], (fb[3] - fb[1]) * .5, lado_min * k)
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        u = min(1.0, dt / max(dur, .5))
        s = min(SW / w, SH / h) * (1 + (zoom - 1) * u * u * (3 - 2 * u)) / (1 + .08 * (1 - _eo(dt / .9)))
        s = min(max(s, s_min_n / k), s_max_n / k)
        tx = (S0 + S2) / 2 - s * cx + 5 * math.sin(dt * .5)
        ty = (S1 + S3) / 2 - s * cy + 4 * math.cos(dt * .4)
        hx, hy = cabeza[0] * s + tx, cabeza[1] * s + ty
        tx += (S2 - hx if hx > S2 else (S0 - hx if hx < S0 else 0))
        ty += (S3 - hy if hy > S3 else (S1 - hy if hy < S1 else 0))
        aw, ah = arr.shape[1] * s, arr.shape[0] * s
        tx = (VW - aw) / 2 if aw <= VW else min(0, max(VW - aw, tx))
        ty = (VH - ah) / 2 if ah <= VH else min(0, max(VH - ah, ty))
        M = np.float32([[s, 0, tx], [0, s, ty]])
        f = cv2.warpAffine(arr, M, (VW, VH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        f = (f * vin).astype(np.uint8)

        def a_vista(p):
            p = np.asarray(p, np.float64)
            return np.stack([p[..., 0] * s + M[0, 2], p[..., 1] * s + M[1, 2]], -1)

        pv = a_vista(hecho)
        _trazo(f, pv, tema, T, dt, largo * s)
        # título que tapa un lugar ya alcanzado (lugar en el borde norte del mapa y sin margen para bajar la cámara): se
        # desvanece justo antes de que salga el marcador y le deja el sitio a su nombre
        op_t = 1.0
        if rect_t:
            for j, (i, _, _) in enumerate(lug):
                x, y = a_vista(pts_b[i])
                if dt >= mk[j] - .4 and y < rect_t[3] + 40 and rect_t[0] - 60 < x < rect_t[2] + 60:
                    op_t = min(op_t, 1 - _eo((dt - mk[j] + .4) / .4))
        # marcadores y nombres
        ocupados = [rect_t] if rect_t and op_t > .5 else []
        # viajeros: pegatinas redondas en la punta del trazo (en fila detrás de ella si son varios); saltan al moverse;
        # van debajo de los marcadores y los nombres las esquivan
        ocup_v = []
        if viaj and len(lug) > 1 and dt >= mk[0]:
            moviendo = any(max(mk[j - 1] + .2, mk[j] - traza) < dt < mk[j] for j in range(1, len(lug)))
            Lp = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pv, axis=0).T))]) if len(pv) > 1 else np.zeros(1)
            for q, spr in reversed(list(enumerate(viaj))):
                d_atras = q * spr.shape[0] * .62
                if Lp[-1] >= d_atras:
                    k_ = int(np.searchsorted(Lp, Lp[-1] - d_atras))
                    x, y = pv[min(k_, len(pv) - 1)]
                else:                                       # aún no hay trazo para la fila: en el punto de salida, de lado
                    x, y = pv[0][0] - d_atras, pv[0][1]
                rv = spr.shape[0] / 2                       # a la izquierda de la punta: no tapa el marcador ni su nombre
                x -= rv * 1.05
                y -= rv * .45 + (7 * abs(math.sin(dt * 7 + q)) if moviendo else 2 * math.sin(dt * 1.6 + q))
                ocup_v.append((x - rv, y - rv, x + rv, y + rv))
                _pegar(f, spr, x, y, _eo((dt - mk[0]) / .35), _pop(dt - mk[0] - .05 * q, .4))
        for j, (i, nombre, tipo) in enumerate(lug):
            if dt < mk[j]:
                continue
            x, y = a_vista(pts_b[i])
            e = _pop(dt - mk[j], .45)
            spr = _marcador(tema, tipo)
            dy = 0
            if tipo == "meta" and tema in ("tes", "gaming"):
                dy = -6 * abs(math.sin(dt * 2.6)) if tema == "gaming" else 5 * math.sin(dt * 2.2)
            if tipo in ("meta", "peligro"):                 # anillo que late sin parar
                fase = (dt - mk[j]) * .9 % 1
                if fase > .02:
                    o = f.copy()
                    col = T["color"][::-1] if tipo == "meta" else (40, 50, 214)
                    cv2.circle(o, (int(x), int(y)), int(18 + 60 * fase), tuple(int(c) for c in col), 4, cv2.LINE_AA)
                    cv2.addWeighted(o, 1 - fase, f, fase, 0, dst=f)
            _pegar(f, spr, x, y + dy, 1.0, e)
            et = _etiqueta(tema, nombre, tipo)
            eh, ew = et.shape[:2]
            arriba = 84 if (tipo == "meta" and tema == "tes") else (66 if tema == "gaming" else 46)
            elegido = None
            for evita in (ocupados + ocup_v, ocupados):     # mejor sin tapar a los viajeros; si no cabe, encima de ellos
                for lx, ly in ((1, -1), (-1, -1), (1, 1), (-1, 1)):    # el primer hueco libre: dentro, sin título ni otro nombre
                    ex_, ey_ = x + lx * (ew / 2 + 6), y + (-arriba if ly < 0 else 52)
                    r = (ex_ - ew / 2 + 50, ey_ - eh / 2 + 28, ex_ + ew / 2 - 50, ey_ + eh / 2 - 28)
                    libre = r[0] >= 0 and r[2] <= VW and r[1] >= 0 and r[3] <= VH and not any(
                        r[0] < q[2] and q[0] < r[2] and r[1] < q[3] and q[1] < r[3] for q in evita)
                    if libre:
                        elegido = (ex_, ey_, r)
                        break
                if elegido:
                    break
            if elegido:                                     # sin hueco (el lugar quedó bajo el título o fuera): sin nombre
                ex_, ey_, r = elegido
                ocupados.append(r)
                _pegar(f, et, ex_, ey_, _eo((dt - mk[j] - .12) / .3), 1.0)
        ocupados += ocup_v
        # fotos: la del último lugar al que llegó la ruta (se va cuando llega al siguiente), en el primer hueco libre junto a él
        for j in range(len(lug) - 1, -1, -1):
            i = lug[j][0]
            if i not in fotos or dt < mk[j]:
                continue
            a = _eo((dt - mk[j] - .25) / .3)
            if j + 1 < len(lug) and dt > mk[j + 1]:
                a *= 1 - _eo((dt - mk[j + 1]) / .35)
            if a <= .01:
                continue
            x, y = a_vista(pts_b[i])
            spr = fotos[i]
            fh, fw = spr.shape[:2]
            sep = 60 if not ventana else 36
            mejor = None                                    # sin hueco libre: el que menos tapa (el título pesa el triple)
            for cx_, cy_ in ((x, y - sep - fh / 2), (x + sep + fw / 2, y), (x - sep - fw / 2, y), (x, y + sep + fh / 2),
                             (x + sep + fw / 2, y - fh / 2), (x - sep - fw / 2, y - fh / 2),
                             (x + sep + fw / 2, y + fh / 2), (x - sep - fw / 2, y + fh / 2)):
                cx_ = min(max(cx_, fw / 2), VW - fw / 2)
                cy_ = min(max(cy_, fh / 2), VH - fh / 2)
                r = (cx_ - fw / 2, cy_ - fh / 2, cx_ + fw / 2, cy_ + fh / 2)
                tapa = sum(max(0, min(r[2], q[2]) - max(r[0], q[0])) * max(0, min(r[3], q[3]) - max(r[1], q[1]))
                           * (3 if q is rect_t else 1) for q in ocupados)
                if mejor is None or tapa < mejor[0]:
                    mejor = (tapa, cx_, cy_, r)
                if tapa == 0:
                    break
            _, cx_, cy_, r = mejor
            ocupados.append(r)
            # la foto flota despacio (un mapa esperando la siguiente marca no queda quieto > 2 s: freezedetect, majora_mask)
            _pegar(f, spr, cx_, cy_ + 7 * math.sin(dt * 1.8 + j), a,
                   (.55 + .45 * _pop(dt - mk[j] - .25, .35)) * (1 + .02 * math.sin(dt * 2.3 + j)))
        # título de la zona (arriba al centro)
        if titulo:
            e = _eo((dt - .25) / .6)
            esc = esc_t * (1 + .04 * (1 - e))
            _pegar(f, tt0, VW / 2, y_t + tt0.shape[0] * esc / 2, e * op_t, esc)
        if ventana:
            e = _pop(dt, .5)
            out = np.dstack([f, alfa_v])
            # filete del tema por dentro del borde difuminado
            cv2.rectangle(out, (int(VW * .035), int(VH * .05)), (int(VW * .965), int(VH * .95)),
                          tuple(int(c) for c in T["color"][::-1]) + (150,), 2, cv2.LINE_AA)
            if e < .999:
                out = cv2.resize(out, (max(2, int(VW * e)), max(2, int(VH * e))), interpolation=cv2.INTER_LINEAR)
            return out
        return np.dstack([f, np.full((VH, VW), 255, np.uint8)])
    return fn


def _trazo(f, pv, tema, T, dt, largo_px):
    """Dibuja la ruta ya trazada (pv en px de salida) con el estilo del tema; modifica f."""
    if len(pv) < 2:
        return
    col = tuple(int(c) for c in T["color"][::-1])
    bor = tuple(int(c) for c in T["borde"][::-1])
    gr = T["grueso"]
    P = np.round(pv * 4).astype(np.int32)                   # subpíxel (shift=2)
    if T["trazo"] == "rayas":                               # WoW: rayas que avanzan, borde negro
        cv2.polylines(f, [P], False, bor, gr + 6, cv2.LINE_AA, 2)
        seg = np.hypot(*np.diff(pv, axis=0).T)
        acc = np.concatenate([[0], np.cumsum(seg)])
        fase = (dt * 60) % 36
        on = ((acc - fase) % 36) < 22
        for i in range(len(pv) - 1):
            if on[i]:
                cv2.line(f, tuple(P[i]), tuple(P[i + 1]), col, gr, cv2.LINE_AA, 2)
    elif T["trazo"] == "hilo":                              # Elden Ring: hilo dorado con halo y chispas que corren
        capa = np.zeros_like(f)
        cv2.polylines(capa, [P], False, col, gr + 14, cv2.LINE_AA, 2)
        capa = cv2.GaussianBlur(capa, (0, 0), 9)
        f[:] = cv2.add(f, (capa * .55).astype(np.uint8))
        cv2.polylines(f, [P], False, bor, gr + 3, cv2.LINE_AA, 2)
        cv2.polylines(f, [P], False, col, gr, cv2.LINE_AA, 2)
        seg = np.hypot(*np.diff(pv, axis=0).T)
        acc = np.concatenate([[0], np.cumsum(seg)])
        tot = acc[-1]
        for c in range(max(1, int(tot / 160))):             # chispas
            d0 = (dt * 140 + c * 160) % max(1, tot)
            i = min(len(pv) - 1, int(np.searchsorted(acc, d0)))
            x, y = pv[i]
            cv2.circle(f, (int(x), int(y)), 4, (225, 250, 255), -1, cv2.LINE_AA)
        x, y = pv[-1]                                       # cabeza: luz de gracia
        g = np.zeros_like(f)
        cv2.circle(g, (int(x), int(y)), 16, col, -1, cv2.LINE_AA)
        f[:] = cv2.add(f, cv2.GaussianBlur(g, (0, 0), 10))
        cv2.circle(f, (int(x), int(y)), 5, (235, 250, 255), -1, cv2.LINE_AA)
    else:                                                   # puntos (tes, zelda) o bolitas (gaming)
        seg = np.hypot(*np.diff(pv, axis=0).T)
        acc = np.concatenate([[0], np.cumsum(seg)])
        paso = 26 if T["trazo"] == "puntos" else 34
        n = int(acc[-1] / paso) + 1
        for j in range(n):
            d0 = j * paso
            i = min(len(pv) - 1, int(np.searchsorted(acc, d0)))
            x, y = pv[i]
            r = gr / 2 + 1
            if T["trazo"] == "bolitas":                     # brota con rebote al pasar la cabeza
                edad = (acc[-1] - d0) / 160
                r = r * min(1.25, _pop(edad, .5) if edad < 1 else 1.0) * (1 + .08 * math.sin(dt * 5 + j))
            cv2.circle(f, (int(x + 1), int(y + 2)), int(r + 3), bor, -1, cv2.LINE_AA)
            cv2.circle(f, (int(x), int(y)), max(1, int(r)), col, -1, cv2.LINE_AA)


# ------------------------------------------------------------------ hojas de prueba y rejilla de coordenadas
def hoja(fn, dur, marcas, salida, tiempos=None, ancho=640):
    """Hoja 2x3 de cuadros (mapa sobre gris medio si es ventana) para MIRARLA antes de `fx`."""
    tiempos = tiempos or [dur * k / 5.6 + .3 for k in range(6)]
    cuadros = []
    for t in tiempos:
        o = fn(t, dur, marcas)
        if o.shape[2] == 4 and o[..., 3].min() < 255:
            bg = np.full((1080, 1920, 3), 90, np.uint8)
            _pegar(bg, o, 960, 540)
            o = bg
        o = cv2.resize(o[..., :3], (ancho, int(ancho * o.shape[0] / o.shape[1])), interpolation=cv2.INTER_AREA)
        cv2.putText(o, f"{t:.1f}s", (10, 28), cv2.FONT_HERSHEY_SIMPLEX, .8, (255, 255, 255), 2, cv2.LINE_AA)
        cuadros.append(o)
    h = max(c.shape[0] for c in cuadros)
    cuadros = [cv2.copyMakeBorder(c, 0, h - c.shape[0], 0, 0, cv2.BORDER_CONSTANT) for c in cuadros]
    cv2.imwrite(salida, np.vstack([np.hstack(cuadros[:3]), np.hstack(cuadros[3:6])]))
    return salida


def rejilla(ruta, recorte=None, salida=None):
    """Copia de la imagen con una rejilla cada 0,05 (números cada 0,1) para leer las coordenadas de los lugares."""
    im = Image.open(ruta).convert("RGB")
    if recorte:
        x0, y0, x1, y1 = recorte
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im.thumbnail((1920, 1920))
    d = ImageDraw.Draw(im)
    f = _fuente("arialbd.ttf", 22)
    for k in range(1, 20):
        v = k / 20
        fuerte = k % 2 == 0
        c = (255, 40, 40) if fuerte else (255, 255, 255)
        d.line([(v * im.width, 0), (v * im.width, im.height)], fill=c, width=2 if fuerte else 1)
        d.line([(0, v * im.height), (im.width, v * im.height)], fill=c, width=2 if fuerte else 1)
        if fuerte:
            d.text((v * im.width + 3, 4), f"{v:.1f}", font=f, fill=c, stroke_width=3, stroke_fill=(0, 0, 0))
            d.text((4, v * im.height + 3), f"{v:.1f}", font=f, fill=c, stroke_width=3, stroke_fill=(0, 0, 0))
    salida = salida or os.path.splitext(ruta)[0] + "_rejilla.jpg"
    im.save(salida, quality=88)
    return salida


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "rejilla":
        rec = tuple(float(v) for v in a[2:6]) if len(a) >= 6 else None
        print(rejilla(a[1], rec))
    else:
        print(__doc__)
