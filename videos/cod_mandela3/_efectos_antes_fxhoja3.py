# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 EFECTOS MANDELA de Call of Duty, parte 3» (SECUENCIA YT, Expediente 141, 19-nov-2026).
Plantilla: videos/cod_mandela2/efectos.py (kit nucleo/mg_cod.py + peg_estilos/peg_anim/presenta, tema «cod»).
MG NUEVO de este guion: `C.rachas` (escalera de rachas de CoD 4 con la nuke fantasma tachada, n.º 18).
Citas (post): el clip va alineado al hueco (_escribir_busquedas.py) y lo que se OYE es sfx/s_*.mp3 (recortes medidos con
_citas.py) en PISTAS voz=True, al acabar la frase; `ambiente_por` no sirve: suena el beat entero, encima de la voz.
    python fab.py cod_mandela3 fx --seco   tiempos      FAB_FX_FINAL=1 python fab.py cod_mandela3 fx hoja
"""
import os

import mg_cod as C
import mg_wow as W
import peg_estilos as PE

TEMA = "cod"
CAMARA = {}
FUNDIDO = {}

_FX, _FY = .75, .30            # fichas: arriba a la derecha
_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_MAPA = "cod"


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    return os.path.join(_PEG, slug + ".png")


def ficha(en, titulo, texto, tipo=None, dur=4.0, x=.27, y=.28, ancho=640):
    return dict(tipo="mg", fn=C.ficha(titulo, texto, tipo, ancho=ancho), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + titulo, ver=1.2)


def peg(en, slug, titulo, dur=3.4, x=.17, y=.64, tam=380, giro=-5.0):
    return dict(tipo="mg", fn=C.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def pv(en, slug, titulo, dur=3.6, x=.17, y=.62, tam=400, **anim):
    """Pegatina con marco + entrada + estancia + salida que rotan (catálogo 5-nov-2026)."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(P(slug), titulo, tam, tema=TEMA, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila([(P(s), e) for s, e in fotos], tam, TEMA, marco), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.06, nombre="pegatina pila " + nombre, ver=2.0)


def sil(en, slug, nombre=None, sub=None, dur=4.2, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=3.8, x=.77, y=.52, tam=440):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.0, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.2, x=.16, y=.66, tam=300, foco=(.5, .3, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.78, y=.52, ancho=460, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.64, tam=280):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.4, sale=.4,
                nombre="pantalla " + slug, ver=2.0)


def puesto(en, n, titulo, sub, dur=4.2):
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub, total=20), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


def mg(fn, de, a, marcas, nombre, x=.5, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def caso(en, estado, titulo, sub=None, dur=3.2, x=.72, y=.26):
    """Veredicto del expediente (MG propio de este guion): al cerrar cada puesto."""
    return mg_en(C.caso(estado, titulo, sub), en, dur, "caso " + titulo, x=x, y=y)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def vid(n, de, a, desde=0.0, recorte=0.0):
    """Corte rápido con OTRO clip ya bajado (medios/scene-NNN.mp4) a cuadro entero (va PRIMERO en FX)."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", f"scene-{n:03d}.mp4"), de=de, a=a, desde=desde,
                recorte=recorte, entra=.12, sale=.12, nombre=f"corte clip {n:03d}")


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    fx = dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)
    if kw.get("entrada"):
        fx["entra"] = fx["sale"] = .05
    return fx


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def tabl(fotos, hilos, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.tablero(_f(fotos), hilos, titulo, TEMA), de, a, marcas, "tablero")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA, titulo), de, a, marcas, "versus")


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro(_f(fotos), tema=TEMA, destaca=destaca, titulo=titulo), de, a, marcas, "muro")





def com(en, cid, dur=6.4, x=.36, y=.30, giro=-2):
    """Comentario real del canal (pegatinas/com_<id>.png, ≤ 10 días, ninguno repetido)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760, giro=giro)


_D, _I = dict(x=.80, y=.62), dict(x=.18, y=.64)

FX = [
    # ---------------- gancho: un elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.33, y=.42),
    leg("c_bo2", "EXPEDIENTE 141 · PARTE 3", ["Asunto: tu memoria", "20 efectos Mandela", "Tercera parte"],
        de="Asunto: tu memoria", a=("Uno de ustedes me escribió", -.1), x=.78, y=.50),
    pv("un zombi lo perseguía", "nuketown", "¿Zombis en Nuketown?", dur=2.8, tam=330, **_D),
    pv("Uno solo. Y que nadie", "mannequin", "Uno solo", dur=2.4, tam=300, **_I),
    pv("Otro jura que Mason perdonó", "alex_mason", "Alex Mason", dur=2.6, tam=320, **_D),
    pv("terminaba con Menéndez en una celda", "menendez", "¿Menéndez preso?", dur=2.8, tam=320, **_I),
    com("Y alguien más me dejó esto", "UgzjkWiRTlxvy5k7SEZ4AaABAg", dur=5.6),
    mg_en(C.objetivo("Revisar cada recuerdo", "Con el juego en pantalla", completo=True), "Lo revisé todo", 2.6,
          "objetivo revisar", x=.30, y=.82),
    pv("Hay un helicóptero que cambió", "seaknight", "El helicóptero · 2016", dur=2.4, tam=300, **_D),
    pv("una frase que en Japón", "makarov", "¿Qué dijo en Japón?", dur=2.4, tam=300, **_I),
    pv("una Ray Gun que llegó antes", "raygun2", "¿Antes de tiempo?", dur=2.4, tam=300, **_D),
    mg_en(C.contador(20, "EFECTOS MANDELA", "PARTE 3"), "Veinte efectos Mandela de Call", 2.8, "contador 20", x=.30, y=.30),
    mg_en(C.marcador("Número 1", 20, "Black Ops 7"), "Y en el número uno", 2.4, "marcador numero uno", x=.55, y=.36),
    pv("Black Ops 7 te mintió", "c_bo7", "Black Ops 7", dur=2.6, tam=320, **_D),

    # ---------------- 20 · Gaz en MW2
    puesto("Número veinte", 20, "¿Gaz en Modern Warfare 2?", "CAMPAÑA / MODERN WARFARE 2"),
    sil("Hoy Gaz es del ciento", "gaz19", "Gaz", "Task Force 141 · 2019", lado="der", dur=3.6),
    carr([("price", "Price"), ("soap", "Soap"), ("ghost", "Ghost")], de="al lado de Price", a=("Pero en el Modern Warfare 2 original", -.1),
         marcas=["al lado de Price", "Price, Soap", "Soap y Ghost"], titulo="La 141 de hoy"),
    pv("el de dos mil nueve, Gaz", "c_mw2", "Modern Warfare 2 · 2009", dur=2.6, tam=320, **_I),
    pv("Gaz ya estaba muerto", "gaz", "Gaz · Call of Duty 4", dur=2.8, tam=320, **_D),
    sil("Zakhaev lo mata con", "zakhaev", "Zakhaev", "Call of Duty 4", lado="izq", dur=3.4),
    ficha("en el puente, al final", "Game Over", "Gaz muere *en el puente*.", "INTEL / CALL OF DUTY 4", dur=3.2, x=.73),
    mg_en(C.contador(3, "SEGUNDOS", "EN LA INTRO DE MW2"), "Tres segundos, en el video", 2.8, "contador tres", x=.30, y=.30),
    mg_en(C.marcador("Gaz", 3, "Video de introducción"), "el que repasa lo que pasó", 2.8, "marcador gaz", x=.55, y=.36),
    caso("Solo en sus recuerdos", "a_medias", "Gaz en Modern Warfare 2", "Solo en la intro", dur=2.6),

    # ---------------- 19 · Max Ammo
    puesto("En el diecinueve", 19, "Max Ammo", "ZOMBIES / DE WORLD AT WAR A BLACK OPS 4"),
    rel("La lata verde de munición", "max_ammo", "Max Ammo", "Potenciador", dur=3.4, x=.77, y=.52, tam=420),
    ficha("con el letrero de Max Ammo", "Max Ammo", "Llena *la reserva* de todas tus armas.", "INTEL / ZOMBIES", dur=3.2),
    mg_en(C.objetivo("¿También el cargador?", "Lo que jura mucha gente"), "Mucha gente jura que siempre", 2.6, "objetivo cargador",
          x=.30, y=.82),
    mg_en(C.balanza("¿Max Ammo llena el cargador?", [("World at War", False, "solo reserva"), ("Black Ops 1", False, "solo reserva"),
                                                     ("Black Ops 2", False, "solo reserva"), ("Black Ops 3", False, "solo reserva")]),
          "En los zombis de World at War", 6.0, "balanza max ammo", y=.50),
    mg_en(C.linea("Max Ammo", [("2008", "World at War", "Solo la reserva"), ("2018", "Black Ops 4", "También el cargador")], h=400),
          "El cambio llegó con Black Ops 4", 4.0, "linea max ammo", x=.5, y=.30),
    pv("hay veteranos que todavía recargan", "c_waw", "Los veteranos", dur=2.8, tam=300, **_I),
    caso("La costumbre, no", "falso", "Siempre llenaba el cargador", "Solo desde Black Ops 4", dur=2.6),

    # ---------------- 18 · la nuke de CoD 4 (MG nuevo: rachas)
    puesto("Número dieciocho", 18, "La nuke de Call of Duty 4", "MULTIJUGADOR / CALL OF DUTY 4"),
    mg_en(C.contador(25, "BAJAS", "SIN MORIR"), "Veinticinco bajas sin morir", 2.4, "contador 25", x=.30, y=.30),
    mg_en(C.contador(10, "SEGUNDOS", "CUENTA ATRÁS"), "una cuenta atrás de diez", 2.4, "contador diez", x=.70, y=.30),
    rel("el mapa entero se pone blanco", "nuke", "Nuke táctica", "25 bajas", dur=3.0, x=.77, y=.52, tam=420),
    mg(C.rachas("RACHAS DE CALL OF DUTY 4", [(3, "UAV"), (5, "Ataque aéreo"), (7, "Helicóptero")], fantasma=(25, "Nuke táctica")),
       de="mira sus rachas", a=("La nuke táctica nació", -.1),
       marcas=["tres bajas para el UAV", "cinco para el ataque", "siete para el helicóptero", "Y ahí se acaba la lista"],
       nombre="rachas cod4", x=.28, y=.50),
    pv("tres bajas para el UAV", "uav", "UAV", dur=1.8, x=.78, y=.56, tam=300),
    pv("cinco para el ataque aéreo", "airstrike", "Ataque aéreo", dur=1.8, x=.78, y=.56, tam=300),
    pv("siete para el helicóptero", "heli", "Helicóptero", dur=2.2, x=.78, y=.56, tam=300),
    pv("La nuke táctica nació", "c_mw2", "Modern Warfare 2 · 2009", dur=2.8, tam=320, **_D),
    ficha("una bomba nuclear en la campaña", "Shock and Awe", "La bomba era *de la campaña*.", "INTEL / CALL OF DUTY 4", dur=3.2),
    caso("la metió en el multijugador", "falso", "La nuke en Call of Duty 4", "Llegó con MW2", dur=2.6),

    # ---------------- 17 · el hombre del menú (caso abierto)
    puesto("En el diecisiete", 17, "El hombre del menú", "CASO ABIERTO / BLACK OPS"),
    pv("El menú de Black Ops, dos mil diez", "c_bo1", "Black Ops · 2010", dur=2.8, tam=320, **_D),
    mg_en(C.marcador("Detrás del cristal", 3, "Menú principal"), "alguien detrás del cristal", 3.0, "marcador cristal", x=.55, y=.36),
    mg_en(C.espejo("¿Qué le pasa al hombre del cristal?", ("SE LO COMEN", "Versión 1", ["Al entrar en Zombies", "Aparece un zombi"], None),
                   ("GOLPEA", "Versión 2", ["Sale de la sala", "Vuelve golpeando el cristal"], None), "MISMO MENÚ"),
          "Unos juran que al entrar en Zombies", 8.0, "espejo menu", x=.5, y=.40),
    caso("Este expediente se queda abierto", "sin_resolver", "El hombre del menú", "Sin grabación", dur=2.8),
    mg_en(C.objetivo("Manda la grabación", "Ya sabes dónde"), "Si tienes la grabación", 3.0, "objetivo grabacion", x=.30, y=.82),

    # ---------------- interludio: Jesús (contraburla del comentario)
    mg_en(C.sello("CORRECCIÓN", "DEL PÚBLICO"), "una corrección del público", 2.2, "sello correccion", x=.70, y=.40),
    com("Jesús escribió que el de Shepherd", "UgyYqIenX5EYJiKCktZ4AaABAg", dur=7.0),
    pv("los miles que escribieron que fue Makárov", "makarov", "«Fue Makárov»", dur=3.0, tam=320, **_D),
    mg_en(C.logro("Tu memoria funciona", "Felicidades, Jesús"), "Felicidades: tu memoria funciona", 3.0, "logro jesus", x=.5, y=.84),

    # ---------------- 16 · Speed Cola en el balcón
    puesto("Número dieciséis", 16, "Speed Cola en el balcón", "ZOMBIES / BLACK OPS 2"),
    rel("TranZit, Black Ops 2", "tranzit", "TranZit", "Black Ops 2 · 2012", dur=3.0, x=.77, y=.52, tam=420),
    pv("la granja con su granero rojo", "farm", "La granja", dur=2.6, tam=320, **_I),
    pv("Hay quien recuerda la máquina", "speed_cola", "¿Speed Cola arriba?", dur=3.0, tam=320, **_D),
    mg_en(C.marcador("Double Tap", 6, "Arriba del granero"), "la máquina es de Double Tap", 2.8, "marcador double tap", x=.55, y=.36),
    mg_en(C.espejo("¿Qué máquina hay en la granja?", ("DOUBLE TAP", "TranZit", ["Arriba, en el granero"], P("double_tap")),
                   ("SPEED COLA", "Supervivencia", ["Abajo, dentro de la casa"], P("speed_cola")), "MISMA GRANJA"),
          "La Speed Cola de la granja existe", 7.0, "espejo granja", x=.5, y=.40),
    caso("Una sola granja en tu cabeza", "a_medias", "Speed Cola en el balcón", "Arriba era Double Tap", dur=2.6),

    # ---------------- 15 · Zombie Flesh
    puesto("En el quince", 15, "La carne", "ZOMBIES / BLACK OPS 2"),
    pv("Uno de los recuerdos más raros", "c_bo2", "Black Ops 2", dur=2.4, tam=300, **_D),
    rel("un trozo de carne cruda", "zombie_flesh", "Zombie Flesh", "La carne", dur=3.4, x=.77, y=.52, tam=420),
    pv("como con el mono", "monkey_bomb", "Como el mono", dur=2.6, tam=300, **_I),
    mg_en(C.logro("Existe", "Se llama Zombie Flesh"), "Y no. Existe", 2.8, "logro existe", x=.5, y=.84),
    rel("solo sale en el modo Grief", "grief", "Grief", "Dos equipos", dur=3.2, x=.77, y=.52, tam=400),
    ficha("el de dos equipos contra", "Grief", "*Dos equipos* contra los zombis.", "INTEL / BLACK OPS 2", dur=3.0),
    mg_en(C.contador(30, "SEGUNDOS", "LOS ZOMBIS LO PERSIGUEN"), "lo persiguen treinta segundos", 2.8, "contador treinta", x=.30, y=.30),
    caso("Esta vez la memoria no mintió", "verdad", "La carne de Black Ops 2", "Zombie Flesh · Grief", dur=2.8),

    # ---------------- 14 · Extinction
    puesto("Número catorce", 14, "Extinction no era de Battlefield", "COOPERATIVO / CALL OF DUTY: GHOSTS"),
    mg_en(C.contador(4, "JUGADORES", "Y UN TALADRO"), "Cuatro jugadores, un taladro", 2.6, "contador cuatro", x=.30, y=.30),
    rel("unos aliens enormes llamados", "cryptid", "Cryptids", "Extinction", dur=3.4, x=.77, y=.52, tam=440),
    pv("Hay quien jura que Extinction", "c_bf4", "¿Battlefield 4?", dur=3.0, tam=320, **_I),
    pv("Es de Call of Duty: Ghosts", "c_gh", "Ghosts · 2013", dur=3.0, tam=320, **_D),
    mg_en(C.logro("El único modo de aliens", "De toda la saga"), "El único modo de aliens", 2.8, "logro aliens", x=.5, y=.84),
    caso("se lo regalaste a la competencia", "falso", "Extinction en Battlefield", "Es de Ghosts", dur=2.6),

    # ---------------- 13 · Reznov (dos citas)
    puesto("En el trece", 13, "La frase de Reznov", "CAMPAÑA / WORLD AT WAR"),
    pv("En el World at War del año", "c_waw", "World at War · 2008", dur=2.4, tam=300, **_D),
    sil("Viktor Reznov, el sargento", "reznov", "Viktor Reznov", "Ejército Rojo", lado="der", dur=3.6),
    ficha("en Stalingrado, entre las ruinas", "Vendetta", "Stalingrado · *la primera misión*.", "INTEL / WORLD AT WAR", dur=3.0),
    mg_en(C.radio("REZNOV", "«…to their land, to their people, to their blood»", "VENDETTA / STALINGRADO"),
          ("Escucha la primera parte|fin", -.1), 4.0, "radio reznov 1", x=.5, y=.26),
    mg_en(C.linea("La frase de Reznov", [("Stalingrado", "Vendetta", "«…to their land»"), ("Alemania", "Su misión", "«…their land»")], h=400),
          "Y la segunda parte llega", 4.4, "linea reznov", x=.5, y=.30),
    mg_en(C.radio("REZNOV", "«Now it is their land…»", "LA MISIÓN QUE LLEVA SU NOMBRE"), ("lleva su nombre|fin", -.1), 3.8,
          "radio reznov 2", x=.5, y=.26),
    mg(C.fusion((P("reznov"), "STALINGRADO", "«…to their land»"), (P("reznov"), "ALEMANIA", "«Now it is their land»"), "Un solo discurso"),
       de="Su tierra, su gente", a=("en un solo discurso|fin", 0), marcas=["Su tierra, su gente", "Son dos frases", "Y tu memoria las juntó"],
       nombre="fusion reznov", y=.50),
    caso(("en un solo discurso|fin", 0), "falso", "El discurso de Reznov", "Son dos frases", dur=2.4),

    # ---------------- 12 · One in the Chamber
    puesto("Número doce", 12, "One in the Chamber", "PARTIDAS DE APUESTAS / BLACK OPS"),
    rel("las partidas de apuestas", "oitc", "One in the Chamber", "Black Ops · 2010", dur=3.2, x=.77, y=.52, tam=420),
    mg_en(C.contador(1, "BALA", "UNA PISTOLA · UN CUCHILLO"), "una pistola, una bala", 2.6, "contador bala", x=.30, y=.30),
    mg_en(C.objetivo("30 bajas, sin vidas", "Lo que recuerdan"), "Hay quien lo recuerda como", 2.8, "objetivo oitc", x=.30, y=.82),
    mg_en(C.contador(3, "VIDAS", "DESDE EL PRIMER DÍA"), "Desde el primer día tenía", 2.6, "contador vidas", x=.70, y=.30),
    mg_en(C.fallida("Fuera de la partida", "Tres muertes y fuera"), "Mueres tres veces", 2.2, "fallida oitc"),
    caso("tu memoria te dio infinitas", "falso", "OITC sin vidas", "Siempre fueron tres", dur=2.6),

    # ---------------- 11 · la bufanda de Ghost
    puesto("En el once", 11, "La bufanda de Ghost", "CAMPAÑA / MODERN WARFARE 2"),
    sil("Simon Ghost Riley", "ghost", "Simon «Ghost» Riley", "Modern Warfare 2 · 2009", lado="der", dur=3.8),
    ficha("el pasamontañas de calavera", "Ghost · 2009", "Calavera · *gafas* · auriculares.", "INTEL / MODERN WARFARE 2", dur=3.4),
    mg_en(C.objetivo("¿Bufanda de cuadros?", "Lo que recuerda media generación"), "Media generación lo recuerda", 3.0,
          "objetivo bufanda", x=.30, y=.82),
    mg_en(C.fallida("Sin bufanda", "En ninguna misión del original"), "En ninguna misión del original", 2.4, "fallida bufanda"),
    caso("Te disfrazaste de un Ghost", "falso", "La bufanda de Ghost", "Salió de los fans", dur=2.6),

    # ---------------- 10 · los dos Price
    puesto("Número diez", 10, "Los dos capitanes Price", "CAMPAÑA / CALL OF DUTY 1, 2 Y 4"),
    sil("Bigote enorme, boina", "price_ww2", "Capitán Price", "Segunda Guerra Mundial", lado="izq", dur=3.6),
    pv("El Capitán Price de Call of Duty 1", "c_cod1", "Call of Duty · 2003", dur=2.6, tam=300, **_D),
    mg_en(C.espejo("¿Es el mismo Price?", ("1944", "Call of Duty 1 y 2", ["Bigote y boina"], P("price_ww2")),
                   ("2007", "Call of Duty 4", ["Gorro militar"], P("price")), "¿EL MISMO?"),
          "Mucha gente cree que es el mismo", 6.4, "espejo price", x=.5, y=.40),
    mg_en(C.contador(1944, "", "MUERE EL PRICE DE LA GUERRA", desde=1939), "muere en mil novecientos", 2.8, "contador 1944", x=.30, y=.30),
    rel("saboteando el acorazado Tirpitz", "tirpitz", "Tirpitz", "El acorazado", dur=3.4, x=.77, y=.52, tam=440),
    caso("Nunca se confirmó", "falso", "El mismo Price", "Son dos capitanes", dur=2.6),
    mg_en(C.sello("BIGOTE", "HEREDADO"), "el bigote se heredó", 2.4, "sello bigote", x=.70, y=.40),

    # ---------------- 9 · el poste de Piccadilly
    puesto("En el nueve", 9, "El poste de Piccadilly", "MULTIJUGADOR / MODERN WARFARE 2019"),
    pv("Modern Warfare, dos mil diecinueve. Piccadilly", "c_mw19", "Modern Warfare · 2019", dur=2.6, tam=320, **_I),
    rel("Piccadilly, en Londres", "piccadilly", "Piccadilly", "Londres", dur=3.2, x=.77, y=.52, tam=440),
    mg_en(C.marcador("Semáforo", 15, "Entre los autobuses"), "y un semáforo entre ellos", 3.0, "marcador semaforo", x=.55, y=.36),
    mg_en(C.contador(2020, "", "«ESE POSTE ES NUEVO»", desde=2019), "En abril de dos mil veinte", 2.8, "contador 2020", x=.30, y=.30),
    mg_en(C.objetivo("Esquiva el poste", "Un jugador profesional"), "Hasta un jugador profesional", 2.8, "objetivo poste", x=.30, y=.82),
    mg_en(C.linea("El poste de Piccadilly", [("Tráiler", "Seis meses antes", "Ya estaba"), ("Lanzamiento", "Primeras partidas", "Ya estaba"),
                                             ("Abril 2020", "«Es nuevo»", "El mismo poste")], h=400),
          "El poste estaba desde el principio", 4.6, "linea poste", x=.5, y=.30),
    caso("tiene un primo en Londres", "falso", "El poste nuevo", "Siempre estuvo", dur=2.6),

    # ---------------- 8 · Mule Kick en Nacht
    puesto("Número ocho", 8, "Mule Kick en Nacht", "ZOMBIES / NACHT DER UNTOTEN"),
    rel("El mapa donde empezó todo", "nacht", "Nacht der Untoten", "El primer mapa", dur=3.2, x=.77, y=.52, tam=420),
    ficha("la casa en ruinas", "Nacht der Untoten", "Ventanas con tablas · *la caja*.", "INTEL / WORLD AT WAR", dur=3.0),
    pv("Otros, que tenía Mule Kick", "mule_kick", "Mule Kick", dur=3.0, tam=320, **_I),
    mg_en(C.balanza("¿Perks en Nacht?", [("World at War", False, "ninguna"), ("Black Ops con internet", True, "Mule Kick"),
                                         ("Black Ops sin conexión", False, "ninguna")]),
          "Los dos tienen razón", 7.0, "balanza nacht", y=.50),
    pv("En Black Ops, un parche", "c_bo1", "Black Ops · parche de 2011", dur=2.8, tam=300, **_D),
    caso("Mismo mapa. Dos memorias", "a_medias", "Mule Kick en Nacht", "Solo con conexión", dur=2.6),

    # ---------------- 7 · la frase de Prípiat (dos citas)
    puesto("En el siete", 7, "La frase de Prípiat", "CAMPAÑA / CALL OF DUTY 4"),
    rel("All Ghillied Up. El capitán", "all_ghillied", "All Ghillied Up", "Call of Duty 4", dur=3.0, x=.77, y=.52, tam=420),
    pv("El capitán MacMillan y Price", "macmillan", "Capitán MacMillan", dur=2.6, tam=320, **_I),
    pv("la ciudad abandonada de Chernóbil", "price", "Price · traje de camuflaje", dur=2.6, tam=300, **_D),
    mg_en(C.radio("MENÚ DE CALL OF DUTY 4", "«Fifty thousand people used to live here…»", "VIDEO DEL MENÚ"),
          ("en el menú del juego|fin", -.1), 4.4, "radio menu", x=.5, y=.26),
    mg_en(C.descifra("45 000", "50 000", "LA CIFRA DE MACMILLAN", "No cuarenta y cinco mil"), "Cincuenta mil, no cuarenta", 3.6,
          "descifra 50000", x=.5, y=.30),
    mg_en(C.sello("SIN PALABROTA", "VIDEO DEL MENÚ"), "Y sin palabrota", 2.4, "sello palabrota", x=.70, y=.42),
    mg_en(C.radio("MACMILLAN", "«Look at this place. Fifty thousand people used to live in this city»", "ALL GHILLIED UP / MISIÓN"),
          ("En la misión es otra. Escucha|fin", -.1), 5.0, "radio mision", x=.5, y=.26),
    mg(C.fusion((P("macmillan"), "MACMILLAN", "CoD 4 · «50 000»"), (P("c_mw2"), "SHEPHERD", "MW2 · la palabrota"), "Una sola frase"),
       de="En esta ciudad", a=("Una sola frase en tu cabeza|fin", 0), marcas=["En esta ciudad", "es del general Shepherd", "Dos juegos, dos"],
       nombre="fusion pripiat", y=.50),
    caso(("Una sola frase en tu cabeza|fin", 0), "falso", "«45 000» con palabrota", "Dos juegos mezclados", dur=2.4),

    # ---------------- 6 · Outbreak
    puesto("Número seis", 6, "El mapa soleado que no existe", "ZOMBIES / BLACK OPS COLD WAR"),
    mg_en(C.objetivo("Encuentra el mapa soleado", "Hierba, bosques y un portal"), "Hay quien recuerda un mapa", 3.2, "objetivo mapa",
          x=.30, y=.82),
    mg_en(C.fallida("Sin resultados", "Ni su amigo ni internet"), "Y en internet no lo encontraba", 2.2, "fallida mapa"),
    mg_en(C.logro("Ese mapa existe", "Se llama Outbreak"), "Ese mapa existe", 2.8, "logro outbreak", x=.5, y=.84),
    rel("Se llama Outbreak", "outbreak", "Outbreak", "Zombies en mapa abierto", dur=3.2, x=.77, y=.52, tam=440),
    pv("es de Black Ops Cold War", "c_cw", "Black Ops Cold War", dur=2.6, tam=320, **_I),
    pv("como el pueblo de Golova", "golova", "Golova", dur=3.0, tam=340, **_D),
    mg_en(C.sello("PRUEBA GRATIS", "UN FIN DE SEMANA"), "lo jugó un fin de semana", 2.6, "sello prueba", x=.30, y=.40),
    caso("Y años buscándolo", "verdad", "El mapa soleado", "Outbreak · Cold War", dur=2.8),

    # ---------------- 5 · la Ray Gun Mark II
    puesto("En el cinco", 5, "La Ray Gun Mark II", "ZOMBIES / BLACK OPS 2"),
    rel("La Ray Gun de tres disparos", "raygun2", "Ray Gun Mark II", "Black Ops 2", dur=3.4, x=.77, y=.52, tam=440),
    mg_en(C.contador(3, "DISPAROS", "POR RÁFAGA"), "de tres disparos", 2.4, "contador disparos", x=.30, y=.30),
    pv("en la caja desde el primer día", "raygun", "¿Desde el primer día?", dur=2.6, tam=300, **_I),
    mg_en(C.linea("Ray Gun Mark II", [("Nov 2012", "Black Ops 2", "No está en la caja"), ("Jul 2013", "Vengeance · Buried", "Llega")], h=400),
          "Llegó ocho meses después", 4.6, "linea raygun", x=.5, y=.30),
    pv("con el paquete Vengeance", "vengeance", "Vengeance", dur=2.4, tam=300, x=.18, y=.66),
    pv("y el mapa Buried", "buried", "Buried", dur=2.6, tam=300, x=.80, y=.66),
    ficha("un parche la coló por error", "El error", "Un parche la puso *en todos los mapas*.", "INTEL / BLACK OPS 2", dur=3.4),
    caso("no lo soñaste", "a_medias", "Ray Gun desde el día uno", "Unos días, por error", dur=2.4),
    mg_en(C.logro("Testigo de un error", "Ray Gun antes de tiempo"), "Fuiste testigo de un error", 2.8, "logro testigo", x=.5, y=.84),

    # ---------------- 4 · No Russian (solo el ascensor; dos citas)
    puesto("Número cuatro", 4, "Remember, no Russian", "CAMPAÑA / MODERN WARFARE 2"),
    pv("Modern Warfare 2, el ascensor", "c_mw2", "Modern Warfare 2 · 2009", dur=2.4, tam=300, **_I),
    sil("Makárov carga su arma", "makarov", "Makárov", "Modern Warfare 2", lado="der", dur=3.4),
    mg_en(C.radio("MAKÁROV", "«Remember… no Russian.»", "EL ASCENSOR"), ("la frase más famosa de la saga|fin", -.1), 3.8,
          "radio no russian", x=.5, y=.26),
    mg_en(C.objetivo("«Que no quede ningún ruso»", "Lo que entendieron muchos"), "Mucha gente entendió", 3.0, "objetivo ruso", x=.30, y=.82),
    mg_en(C.descifra("NO RUSSIAN", "NADA DE RUSO", "LO QUE SIGNIFICA", "No hablen ruso"), "Significa otra cosa", 4.0, "descifra ruso",
          x=.5, y=.30),
    mg_en(C.radio("DOBLAJE JAPONÉS", "«Korose, Roshia-jin da»", "MODERN WARFARE 2 / JAPÓN"), ("la frase salió así|fin", -.1), 3.2,
          "radio japon", x=.5, y=.26),
    ficha("Mátenlos, son rusos", "Doblaje japonés", "«Mátenlos, *son rusos*».", "INTEL / MODERN WARFARE 2", dur=3.2),
    mg_en(C.contador(11, "AÑOS", "HASTA LA CORRECCIÓN"), "Se corrigió once años", 2.8, "contador once", x=.70, y=.30),
    pv("en la versión remasterizada", "c_mw2r", "MW2 Remastered", dur=2.8, tam=320, **_D),
    mg_en(C.objetivo("Sigue a Makárov", "Tu único objetivo", completo=True), "Tu único objetivo es seguir", 3.0, "objetivo seguir",
          x=.30, y=.82),
    caso("Fue tu memoria", "falso", "Matar a todos los rusos", "Era «no hablen ruso»", dur=2.4),

    # ---------------- 3 · el brazo de Jackson (cita del original)
    puesto("En el tres", 3, "El brazo de Jackson", "CAMPAÑA / CALL OF DUTY 4"),
    pv("Call of Duty 4, Shock and Awe", "c_cod4", "Call of Duty 4 · 2007", dur=2.4, tam=300, **_D),
    pv("el helicóptero se ladea", "seaknight", "El helicóptero", dur=2.6, tam=320, **_I),
    mg_en(C.marcador("Volker", 8, "Sale por la rampa"), "sale volando por la rampa", 2.8, "marcador volker", x=.55, y=.36),
    mg_en(C.objetivo("Salva a Volker", "Lo que recuerdan muchos"), "Muchos recuerdan al sargento", 2.8, "objetivo volker", x=.30, y=.82),
    mg_en(C.contador(2007, "", "EL ORIGINAL", desde=2000), "Mira el original", 2.4, "contador 2007", x=.30, y=.30),
    mg_en(C.sello("NI UN GESTO", "ORIGINAL · 2007"), "Ni un gesto", 2.2, "sello gesto", x=.70, y=.42),
    pv("Ahora el remasterizado", "c_mwr", "Modern Warfare Remastered", dur=2.8, tam=320, **_I),
    mg_en(C.espejo("¿Jackson estira el brazo?", ("NO", "Original · 2007", ["Ni un gesto"], P("c_cod4")),
                   ("SÍ", "Remastered · 2016", ["Estira el brazo"], P("c_mwr")), "MISMA ESCENA"),
          "Los dos bandos tienen razón", 6.0, "espejo jackson", x=.5, y=.40),
    mg_en(C.contador(9, "AÑOS DESPUÉS", "EL BRAZO DE JACKSON"), "nueve años después", 2.6, "contador nueve", x=.30, y=.30),
    caso("desde el principio", "a_medias", "El brazo de Jackson", "Solo en el remaster", dur=2.4),

    # ---------------- 2 · el zombi de Nuketown (@gxlfredo07 + contraburla @felixhd7436)
    puesto("Número dos", 2, "El zombi de Nuketown", "DE LOS COMENTARIOS"),
    com("Este viene de los comentarios", "Ugzku_dcNco_CkxQ0zN4AaABAg", dur=6.4, giro=2),
    rel("el colorido de Black Ops 1", "nuketown", "Nuketown", "Black Ops 1 · 2010", dur=3.0, x=.77, y=.52, tam=420),
    mg_en(C.fallida("Sin zombis", "El Nuketown de Black Ops 1"), "nunca tuvo zombis", 2.2, "fallida nuketown"),
    pv("volarles la cabeza a todos", "mannequin", "Los maniquíes", dur=3.0, tam=320, **_I),
    rel("En Black Ops 4 está Alpha Omega", "alpha_omega", "Alpha Omega", "Black Ops 4", dur=3.2, x=.77, y=.52, tam=420),
    pv("Nuketown antes de la bomba", "nuketown_z", "Antes de la bomba", dur=2.8, tam=320, **_I),
    mg_en(C.marcador("Maniquí", 12, "Se congela si lo miras"), "aparece uno solo", 3.2, "marcador maniqui", x=.55, y=.36),
    pv("en Nuk3town, los maniquíes", "nuk3town", "Nuk3town · Black Ops 3", dur=3.0, tam=320, **_D),
    caso("no era Black Ops 1", "a_medias", "El zombi de Nuketown", "Alpha Omega y Nuk3town", dur=2.6),
    com("Félix tiene una teoría", "UgzOOpLTLsVabLRUX2l4AaABAg", dur=6.0, x=.62, giro=-2),
    mg_en(C.sello("SIN MODS", "TREYARCH LO METIÓ DOS VECES"), "Treyarch lo metió dos veces", 2.6, "sello mods", x=.30, y=.42),

    # ---------------- 1 · Menéndez en la celda (@rafaeltroconis6615)
    puesto("Y el número uno", 1, "Menéndez en la celda", "CAMPAÑA / BLACK OPS 2 Y BLACK OPS 7"),
    com("Este me lo mandó Rafael", "Ugw-12ZYVJ3LQqiUPmx4AaABAg", dur=6.4),
    pv("antes de Black Ops 7, juraba", "c_bo7", "Black Ops 7", dur=2.4, tam=300, **_D),
    mg_en(C.logro("Ese final existe", "Primera sorpresa"), "Primera sorpresa", 2.8, "logro final", x=.5, y=.84),
    sil("es su hijo, David Mason", "david_mason", "David Mason", "Black Ops 2", lado="der", dur=3.4),
    mg_en(C.objetivo("Perdónale la vida", "Última misión"), "Si le perdonas la vida", 2.8, "objetivo perdon", x=.30, y=.82),
    leg("menendez", "RAÚL MENÉNDEZ", ["En su celda", "Uniforme naranja", "Mirando la tele"], de="lo ves en su celda",
        a=("Segunda sorpresa", -.1), x=.78, y=.50),
    mg_en(C.fallida("Final no oficial", "Muere al intentar escapar"), "Segunda sorpresa", 2.4, "fallida final"),
    ficha("En la línea de tiempo oficial", "Línea de tiempo de Treyarch", "Muere el *19 de junio de 2025*.", "INTEL / TREYARCH", dur=3.6),
    mg_en(C.contador(10, "AÑOS DESPUÉS", "MENÉNDEZ VUELVE"), "diez años después", 2.6, "contador diez anos", x=.30, y=.30),
    mg_en(C.descifra("MENÉNDEZ", "DEEPFAKE", "¿QUIÉN AMENAZA AL MUNDO?", "Su cara y su voz, imitadas"), "Y no es él", 4.0,
          "descifra deepfake", x=.5, y=.30),
    pv("una inteligencia artificial", "c_bo7", "Black Ops 7 · 2025", dur=2.8, tam=300, **_I),
    caso("se inventaron fue a Menéndez", "a_medias", "Menéndez en la celda", "El final existe, no es el oficial", dur=2.8),

    # ---------------- cierre (@papelotespro y @hildas.4222)
    mg_en(C.sello("EXPEDIENTE CERRADO", "141"), "Expediente cerrado", 2.4, "sello cerrado", x=.5, y=.46),
    mg_en(C.balanza("Veinte efectos Mandela", [("Falsos", False, "10"), ("A medias", None, "7"), ("Eran verdad", True, "2"),
                                               ("Caso abierto", None, "1")]), "varios me los dieron ustedes", 3.8, "balanza cierre", y=.50),
    com("Como el de papelotes", "UgxyWfpSBuQuLKdcdkB4AaABAg", dur=4.4, giro=2),
    com("O el de Hilda", "Ugx5UslEH-wBRR1S29F4AaABAg", dur=4.4, x=.62, giro=-2),
    mg_en(C.objetivo("¿Qué recuerdas tú?", "Escríbelo en los comentarios"), "Escríbelo", 3.2, "objetivo comentarios", x=.30, y=.82),
    mg_en(C.logro("Sale en la parte cuatro", "Si tu efecto es bueno"), "sale en la parte cuatro", 2.8, "logro parte cuatro", x=.5, y=.30),
    pv("tienes la parte uno", "c_bo2", "Efectos Mandela · parte 1", dur=2.4, tam=300, **_I),
    pv("la parte dos", "c_cod4", "Efectos Mandela · parte 2", dur=2.4, tam=300, **_D),
    pv("cómo murió de verdad cada villano", "zakhaev", "Cómo murió cada villano", dur=2.8, tam=300, **_I),
    mg_en(C.objetivo("Suscríbete", "El siguiente expediente te llega primero"), "Suscríbete", 3.0, "objetivo suscribete", x=.30, y=.82),
    mg_en(C.sello("RETÍRATE, SOLDADO", "EXPEDIENTE 141"), "Retírate, soldado", 3.0, "sello retirate", x=.5, y=.46),
]

ROTULOS = [
    dict(texto="SOLO EN SUS RECUERDOS", en="Solo en sus recuerdos", tam=100, color="amarillo", y=.22, dur=2.0),
    dict(texto="LA COSTUMBRE, NO", en="La costumbre, no", tam=130, color="amarillo", y=.22, dur=1.8),
    dict(texto="CASO ABIERTO", en="Este expediente se queda abierto", tam=140, color="amarillo", y=.22, dur=2.0),
    dict(texto="EXISTE", en="Y no. Existe", tam=180, color="amarillo", y=.22, dur=1.4),
    dict(texto="DOS FRASES", en="Son dos frases", tam=160, color="amarillo", y=.22, dur=1.6),
    dict(texto="TRES VIDAS", en="Una bala, tres vidas", tam=150, color="amarillo", y=.22, dur=1.6),
    dict(texto="SOLO CON INTERNET", en="Pero solo si estabas conectado", tam=110, color="amarillo", y=.22, dur=2.0),
    dict(texto="50 000", en="Cincuenta mil, no cuarenta", tam=180, color="amarillo", y=.86, dur=1.6),
    dict(texto="UN FIN DE SEMANA", en="Un fin de semana. Y años", tam=110, color="amarillo", y=.22, dur=1.8),
    dict(texto="JUSTO LO CONTRARIO", en="Justo lo contrario", tam=110, color="amarillo", y=.22, dur=1.8),
    dict(texto="JUEGOS DISTINTOS", en="Solo jugaron juegos distintos", tam=120, color="amarillo", y=.22, dur=1.8),
    dict(texto="DEEPFAKE", en="Es un deepfake", tam=170, color="amarillo", y=.22, dur=1.6),
]

SFX = {}
# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/cod/ → sfx/cod_*.mp3), solo en momentos clave
PISTAS = [
    dict(sfx="cod_sello", en="Expediente ciento", vol=.30),
    dict(sfx="cod_puesto", en="Número veinte", vol=.24),
    dict(sfx="cod_puesto", en="Número dieciocho", vol=.22),
    dict(sfx="cod_logro", en="Felicidades: tu memoria funciona", vol=.26),
    dict(sfx="cod_logro", en="Y no. Existe", vol=.24),
    dict(sfx="cod_puesto", en="Número doce", vol=.22),
    dict(sfx="cod_fallida", en="En ninguna misión del original", vol=.24),
    dict(sfx="cod_puesto", en="Número ocho", vol=.22),
    dict(sfx="cod_fallida", en="Y en internet no lo encontraba", vol=.24),
    dict(sfx="cod_logro", en="Fuiste testigo de un error", vol=.26),
    dict(sfx="cod_puesto", en="Número cuatro", vol=.22),
    dict(sfx="cod_fallida", en="nunca tuvo zombis", vol=.24),
    dict(sfx="cod_puesto", en="Y el número uno", vol=.26),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco (post), a nivel de voz
    dict(sfx="s_reznov1", en=("Escucha la primera parte|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_reznov2", en=("lleva su nombre|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_menu50", en=("en el menú del juego|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_mision50", en=("En la misión es otra. Escucha|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_norussian", en=("la frase más famosa de la saga|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_japones", en=("la frase salió así|fin", .1), vol=1.0, voz=True),
]

# ---- 2.ª pasada (chequeo 19-nov: fichas 0,6/min contra 1,4 del canal; pegatinas 4,6 contra 5,5)
_I2, _D2 = dict(x=.18, y=.64, tam=280), dict(x=.80, y=.62, tam=280)
FX += [
    pv("el de la gorra", "gaz19", "La gorra", **_I2),
    pv("Y aun así sale", "gaz", "¿Gaz en MW2?", **_D2),
    pv("Mucha gente jura que siempre", "max_ammo", "¿El cargador?", **_D2),
    pv("Si tú la pones en Call of Duty 4", "c_cod4", "Call of Duty 4", dur=2.0, **_D2),
    pv("Lo sabemos todos", "ghost", "Ghost", **_I2),
    pv("Pero en TranZit, arriba del granero", "double_tap", "Double Tap", **_I2),
    pv("Se la tiras a un rival", "grief", "Grief", **_I2),
    pv("Muchos recuerdan una sola frase", "reznov", "Reznov", **_I2),
    pv("Eso es en Stalingrado", "c_waw", "Stalingrado", **_D2),
    pv("Hay quien lo recuerda como un todos", "oitc", "¿Sin vidas?", **_D2),
    pv("Uno lo descubrió en una foto", "ghost", "La foto del disfraz", **_D2),
    pv("¿Son familia?", "price", "¿Familia?", **_D2),
    pv("En abril de dos mil veinte", "c_mw19", "Abril de 2020", **_D2),
    pv("Unos juran que en Nacht", "nacht", "¿Sin perks?", **_D2),
    pv("Sin conexión, tu Nacht", "mule_kick", "Sin conexión", **_I2),
    pv("Y MacMillan dice algo", "macmillan", "MacMillan", **_D2),
    pv("Su amigo no tenía ni idea", "outbreak", "¿Lo soñó?", **_D2),
    pv("Y otro detalle: la misión", "makarov", "Seguir a Makárov", **_D2),
    pv("Otros juran que no hace nada", "c_cod4", "¿No hace nada?", **_D2),
    pv("Si les cortas la cabeza a los", "mannequin", "Maniquí robot", **_D2),
    pv("Menéndez sale amenazando al mundo", "menendez", "Menéndez · Black Ops 7", **_D2),
    ficha("Hoy Gaz es del ciento", "Kyle Garrick «Gaz»", "Modern Warfare *2019* · la 141.", "INTEL / REINICIO", dur=3.0),
    ficha("Por eso hay veteranos", "La costumbre", "Recargar *antes* de agarrar la lata.", "INTEL / ZOMBIES", dur=3.0, x=.73),
    ficha("Yo entré a ese menú", "Menú de Black Ops", "Teles, silla y *el cristal*.", "INTEL / BLACK OPS", dur=3.0),
    ficha("Hay quien recuerda la máquina", "Speed Cola", "La perk que *recarga más rápido*.", "INTEL / PERKS", dur=3.0),
    ficha("Es de Call of Duty: Ghosts", "Extinction", "Ghosts · *2013* · Infinity Ward.", "INTEL / COOPERATIVO", dur=3.0),
    ficha("Desde el primer día tenía", "One in the Chamber", "*3 vidas* desde el lanzamiento.", "INTEL / APUESTAS", dur=3.0),
    ficha("La bufanda salió de", "La bufanda", "De *disfraces* y fotos de fans.", "INTEL / FANS", dur=3.0),
    ficha("No es el mismo. El Price", "Capitán Price · 1944", "Muere *saboteando el Tirpitz*.", "INTEL / CALL OF DUTY 1", dur=3.2, x=.73),
    ficha("Él ni siquiera tenía Cold War", "Fin de semana gratis", "Lo jugó *en una prueba*.", "INTEL / COLD WAR", dur=3.0, x=.73),
    ficha("Mucha gente la recuerda en la caja", "Ray Gun Mark II", "Llegó *8 meses* después.", "INTEL / BLACK OPS 2", dur=3.0, x=.73),
    ficha("Explota la bomba, el helicóptero", "Shock and Awe", "La onda *tumba el helicóptero*.", "INTEL / CALL OF DUTY 4", dur=3.0),
    ficha("volarles la cabeza a todos", "Nuketown · Black Ops 1", "El secreto: *los maniquíes*.", "INTEL / BLACK OPS 1", dur=3.0, x=.73),
    ficha("Y en Black Ops 3, en Nuk3town", "Nuk3town", "Los maniquíes *te persiguen*.", "INTEL / BLACK OPS 3", dur=3.0),
    ficha("Y la tercera: Black Ops 7", "Black Ops 7", "Menéndez vuelve *como deepfake*.", "INTEL / BLACK OPS 7", dur=3.0, x=.73),
]
