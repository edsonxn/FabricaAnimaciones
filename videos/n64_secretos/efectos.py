# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 30 SECRETOS de la Nintendo 64 QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming, 31-oct-2026).
Kit TRANSLÚCIDO nucleo/mg_n64.py con la interfaz del HARDWARE (video de toda la consola): grafito de la carcasa, los cuatro colores
del logo, el cartucho gris y letras plateadas de caja. Estructura de videos/spyro2/efectos.py (REGLA DE ORO, docs/estilo_secuencia_yt.md).
- `secreto` = cartucho con el número + contador de esquina «N/30» durante todo el secreto.
- MG del guion: barras, pantalla4, stick_optico, bits, textura, posicion, velocidad, tachones, mito, factura, dos_versiones, cadena,
  pulso, progreso, postits, sin_cara, cita, calor (+ contador, linea_tiempo, lista del kit).
- PEGATINAS reales (pegatinas/, bajar_pegatinas.py) variadas: silueta, reliquia, banda, camafeo, abanico, legajo (nucleo/peg_estilos.py).
- MAPA REAL: Yoshi Valley de VGMaps (mapas/MK64_SpecialCup_YoshiValley.jpg), dos rutas por caminos distintos (secreto 21).
- Comentarios reales de Majora's Mask en el cierre (pegatinas/com_*.png). SFX DEL JUEGO de cada secreto: sfx/n64_*.mp3.
  python fab.py n64_secretos fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py n64_secretos fx         audio/fx.wav
"""
import os

import mg_mapa as MP
import mg_n64 as N
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .42     # fichas: a la derecha (el rótulo de secreto va arriba)
TEMA = "n64"

CAMARA = {}
FUNDIDO = {}


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-5.0):
    return dict(tipo="mg", fn=N.pegatina(P(slug), titulo, tam, giro), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620, giro=-3.0):
    return peg(en, slug, titulo, dur=dur, x=.27 if lado == "izq" else .73, y=.52, tam=tam, giro=giro)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=820, encuadre=(0, 1.0)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con el video corriendo detrás."""
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.6, x=.26, y=.54, tam=560):
    """Objeto sobre el círculo (accesorios y aparatos)."""
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .4, 1.6), dur=4.5, y=.5, lado="der"):
    """Tira de cine a todo lo ancho."""
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.14, y=.68, tam=290, foco=(.5, .25, 1.6)):
    """Medallón para las menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.22, y=.54, ancho=500, giro=3.5):
    """Expediente con retrato; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.62, tam=300):
    """Cartas en abanico cuando la voz enumera. fotos = [(slug, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def com(en, cid, dur=7.0, x=.30, y=.30):
    """Captura del comentario REAL (yt comentario)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760, giro=-2.0)


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY, ancho=820):
    d = dict(tipo="mg", fn=N.ficha(titulo, texto, tipo=tipo, ancho=ancho), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=4.0)


def mapa(archivo, puntos, de, a, marcas, titulo, sub=None, viajeros=None, **kw):
    """Mapa REAL con ruta (VGMaps). Los puntos son fracciones del mapa entero (mapas/yoshi_valley_rejilla.jpg)."""
    puntos = [p[:4] + (P(p[4]),) if len(p) > 4 else p for p in puntos]
    fn = MP.mapa(os.path.join(_MAP, archivo), puntos, TEMA, titulo=titulo, sub=sub, modo="pantalla",
                 viajeros=[P(v) for v in (viajeros or [])], **kw)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=4.0)


def secreto(en, num, titulo, juego, hasta):
    """Rótulo del secreto (cartucho con el número) + contador de esquina hasta que empieza el siguiente."""
    return [dict(tipo="mg", fn=N.puesto(num, titulo, juego), en=(en, -.1), dur=3.8, x=.5, y=.14, sale=.45, nombre=f"aviso secreto {num}", ver=1.4),
            dict(tipo="mg", fn=N.hud(31 - num), de=en, a=(hasta, -.45), x=.915, y=.075, sale=.3, nombre=f"aviso hud {num}", ver=1.0)]


_NUM = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince",
        "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco",
        "veintiséis", "veintisiete", "veintiocho", "veintinueve", "treinta"]
_SEC = {30: ("El personaje que nadie pidió", "Mario Tennis"), 29: ("Un juego de NES dentro", "Excitebike 64"), 28: ("El Rushmore de Mario", "Pilotwings 64"),
        27: ("El stick no era lo que parecía", "El mando"), 26: ("Los 64 bits", "La consola"), 25: ("El temblor que cambió los mandos", "Star Fox 64"),
        24: ("El aparato de la prensa", "Wide-Boy64"), 23: ("El tapón que la hace arrancar", "Jumper Pak"), 22: ("Por qué todo se veía borroso", "La consola"),
        21: ("La pista donde el juego se rinde", "Mario Kart 64"), 20: ("Pokémon Rojo en la tele", "Pokémon Stadium"),
        19: ("El juego que no se podía comprar", "ClayFighter 63 1/3"), 18: ("Los anillos de Superman", "Superman 64"),
        17: ("Arcades sin la consola", "Killer Instinct"), 16: ("El quiosco de Pokémon Snap", "Pokémon Snap"), 15: ("La consola de los hoteles", "LodgeNet"),
        14: ("La consola dentro del mando", "iQue Player"), 13: ("Tu cara en Perfect Dark", "Perfect Dark"), 12: ("El Expansion Pak de DK64", "Donkey Kong 64"),
        11: ("El juego que Nintendo soltó", "Body Harvest"), 10: ("El reloj dentro del cartucho", "Dobutsu no Mori"), 9: ("Internet en la N64", "64DD"),
        8: ("Dos discos en un cartucho", "Resident Evil 2"), 7: ("Los guantes de Mario Party", "Mario Party"), 6: ("El Tetris que te toma el pulso", "Tetris 64"),
        5: ("Final Fantasy 64 nunca existió", "Final Fantasy VI"), 4: ("Por qué Final Fantasy VII se fue", "Final Fantasy VII"),
        3: ("El juego que murió al 60 %", "EarthBound 64"), 2: ("El juego a espaldas del jefe", "WarioWare"), 1: ("Cuatro muñecos sin cara", "Super Smash Bros.")}
_ROT = [x for n in range(30, 0, -1) for x in secreto("Número " + _NUM[n], n, _SEC[n][0], _SEC[n][1],
                                                     "Número " + _NUM[n - 1] if n > 1 else "Treinta años después")]

# Yoshi Valley: dos caminos por el laberinto (rejilla del mapa entero), la salida por el puente de la derecha y la meta a la derecha
_ENT, _HUEVO = (.60, .24), (.318, .765)
# Rutas de Yoshi Valley trazadas SOBRE el camino del mapa de VGMaps (31-oct-2026, rejilla a mano en tres zooms). Todos los caminos
# acaban en el brazo izquierdo de la U de arriba y bajan por la carretera exterior hasta el huevo; luego un solo puente de salida.
_VUELTA_LARGA = [(.578, .262), (.573, .305), (.572, .372), (.573, .44), (.576, .50), (.59, .534), (.605, .574), (.61, .642), (.59, .698),
                 (.55, .718), (.50, .707), (.43, .653), (.375, .622), (.33, .606), (.288, .597), (.263, .564), (.259, .516), (.272, .469),
                 (.297, .446), (.28, .412), (.263, .375), (.247, .332)]
_ATAJO = [(.582, .247), (.522, .216), (.458, .184), (.402, .154), (.354, .135), (.322, .143), (.309, .177), (.311, .222), (.324, .268),
          (.34, .30), (.36, .34), (.362, .368), (.313, .41), (.285, .395), (.263, .375), (.247, .332)]
_TRAMO_FINAL = [(.24, .29), (.23, .25), (.21, .20), (.182, .161), (.142, .154), (.114, .186), (.11, .227), (.122, .268), (.151, .289),
                (.18, .323), (.205, .356), (.213, .389), (.201, .436), (.188, .483), (.186, .535), (.195, .587), (.213, .635), (.243, .682),
                (.272, .715), (.297, .741)]
_SALIDA = [(.355, .789), (.41, .83), (.4725, .871), (.51, .897), (.555, .908), (.625, .891), (.67, .851), (.725, .806), (.78, .766),
           (.81, .721), (.82, .659)]

FX = _ROT + [
    # ================================================================ GANCHO
    grande("Nintendo tuvo que repartir guantes", "c_marioparty", "Mario Party (1998)", lado="der", dur=6.0, tam=560),
    rel("Hubo un Tetris que te medía el pulso", "c_tetris64", "Tetris 64", "Japón, 1998", dur=6.2, x=.74, y=.52),
    sil("Hubo una Nintendo 64 escondida dentro de un mando", "ique", "iQue Player", "Solo en China", dur=5.4, lado="der"),
    mg(N.sin_cara([(P("mario"), "Mario"), (P("donkey_kong"), "Donkey Kong"), (P("samus"), "Samus"), (P("fox"), "Fox")], "Cuatro muñecos sin cara",
                  w=1300, revela=False), ("Y el juego de peleas más famoso", -.1), ("con cuatro muñecos sin cara|fin", .7), ["un hombre solo", "cuatro muñecos"],
       "sin cara gancho", y=.6),
    mg(N.contador("La Nintendo 64 cumple", [(30, "años en 2026", "30 años")], w=900), ("Todo eso pasó en la misma consola", -.1),
       ("treinta años en 2026", 1.6), ["cumplió treinta años"], "contador 30 años", y=.66, x=.3),
    peg("con el remake de Ocarina of Time", "c_oot_remake", "Ocarina of Time", x=.8, y=.58, tam=420, dur=4.6, giro=4),
    mg(N.lista(["Cómo *nació*", "Por qué *perdió la guerra*", "Los *30 secretos* que ignoraste"], "Hoy, en este video", w=1060),
       ("Hoy te cuento cómo nació", -.1), ("seguramente ignoraste|fin", .9), ["cómo nació", "por qué perdió", "los 30 secretos"], "lista hoy"),

    # ================================================================ HISTORIA 1: PROJECT REALITY
    ban("Jim Clark, el fundador de Silicon Graphics", "jim_clark", "Jim Clark", "Fundador de Silicon Graphics", dur=5.6),
    peg("meter la tecnología de sus estaciones", "sgi", "Silicon Graphics", x=.2, y=.74, tam=360, dur=4.0, giro=3),
    cam("Se reunió con Hiroshi Yamauchi", "yamauchi", "Hiroshi Yamauchi", dur=4.4, x=.86, y=.66),
    ficha("Y el 23 de agosto de 1993", "Project Reality", "23 de agosto de 1993: *Silicon Graphics* y *Nintendo*.", tipo="El acuerdo", dur=5.2, x=.28),
    ficha("La promesa era enorme", "La promesa", "Arcades en *1994*, consola a finales de *1995*, por menos de *250 dólares*.", a=("por menos de 250 dólares|fin", .8)),
    mg(N.tachones(["Project Reality", "Ultra 64", "Nintendo 64"], "Cómo se llamó", w=760), ("En 1994 la rebautizaron", -.1), ("se quedó en Nintendo 64|fin", 1.0),
       ["En 1994", "Ultra 64", "se quedó en Nintendo 64"], "tachones nombres", y=.6, x=.3),
    aba([("saturn", "Sega Saturn"), ("playstation", "PlayStation")], ("Mientras tanto, Sega ya vendía", -.1), ("Sony la PlayStation", 2.0),
        ["Sega ya vendía la Saturn", "Sony la PlayStation"], "abanico rivales", x=.74),
    mg(N.linea_tiempo([("1995", "Lo prometido"), ("Abril 1996", "Primer retraso"), ("Junio 1996", "Sale en Japón")], "El retraso", w=1500),
       ("Y la consola que iba a llegar en 1995", -.1), ("Y luego, a junio|fin", .9), ["llegar en 1995", "abril de 1996", "a junio"], "linea retraso", y=.76),
    mg(N.dos_versiones("¿Por qué se retrasó?", ("Nintendo", "No podía fabricar *suficientes unidades*."), ("Un exingeniero de SGI", "La culpa fue de *los chips*."), w=1300),
       ("Nintendo dijo que no podía", -.1), ("Nadie lo ha cerrado del todo|fin", .8), ["Nintendo dijo", "culpó a los chips", "Nadie lo ha cerrado"], "versiones retraso", y=.62),

    # ================================================================ HISTORIA 2: EL CARTUCHO
    grande("Mientras todos se pasaban al CD", "cd", "El CD", lado="izq", dur=4.4, tam=480),
    ficha("Tenía sus razones", "El cartucho", "Casi *sin tiempos de carga*, y mucho más *difícil de piratear*.", dur=5.0),
    mg(N.barras("Cuánto cabía", [(650, "Un CD", "650 MB"), (64, "El cartucho mayor", "64 MB")]), ("Pero un CD guardaba", -.1), ("el cartucho más grande de la consola, 64|fin", .9),
       ["650 megabytes", "el cartucho más grande"], "barras cd", y=.6),
    ficha("Cada tirada de cartuchos", "Fabricar cartuchos", "*Dos semanas* por tirada, y unos *diez dólares más* por juego.", a=("más caro que en PlayStation|fin", .6), x=.28),
    grande("Square se llevó Final Fantasy VII", "c_ff7", "Final Fantasy VII", lado="der", dur=5.6, tam=520, giro=3),
    mg(N.barras("Juegos oficiales", [(388, "Nintendo 64", "388"), (4000, "PlayStation", "más de 4 000")]), ("Y vaya si se limitaron", -.1),
       ("más de cuatro mil en PlayStation|fin", 1.0), ["388 juegos", "más de cuatro mil"], "barras juegos", y=.6),

    # ================================================================ HISTORIA 3: EL LANZAMIENTO
    aba([("c_mario64", "Super Mario 64"), ("c_pilotwings", "Pilotwings 64"), ("c_shogi", "Shogi")], ("con solo tres juegos", -.2),
        ("y uno de shogi|fin", 1.4), ["Super Mario 64", "Pilotwings 64", "uno de shogi"], "abanico lanzamiento"),
    mg(N.contador("Primer día en Japón", [(300000, "consolas agotadas", "300 000")], w=900), ("Las 300 000 consolas", -.1), ("se agotaron|fin", .9),
       ["Las 300 000"], "contador japon", x=.66, y=.6),
    mg(N.barras("Estados Unidos, en tres días", [(350000, "Vendidas", "350 000"), (500000, "Disponibles", "500 000")]), ("Y en tres días vendió", -.1),
       ("de las 500 000 disponibles|fin", .9), ["vendió 350 000", "500 000 disponibles"], "barras eeuu", y=.62),
    ficha("En Estados Unidos llegó en septiembre", "Estados Unidos", "Septiembre de 1996, a *199,99 dólares*.", dur=4.0, x=.28, y=.30),
    cam("Miyamoto explicó por qué", "miyamoto", "Shigeru Miyamoto", dur=4.6, x=.86, y=.68),
    mg(N.pantalla4(), ("Traía cuatro puertos", -.1), ("sin arrastrarse|fin", .9), ["cuatro puertos", "dividir la pantalla", "en cuatro", "sin arrastrarse"],
       "pantalla4", x=.36, y=.55),
    aba([("c_mariokart", "Mario Kart 64"), ("c_goldeneye", "GoldenEye 007")], ("Y ahí nacieron las tardes", -.1), ("de perder amistades|fin", .8),
        ["Mario Kart", "GoldenEye"], "abanico multijugador", x=.72),

    # ================================================================ HISTORIA 4: LA GUERRA
    mg(N.barras("Consolas vendidas", [(32.93, "Nintendo 64", "32,93 millones"), (102, "PlayStation", "más de 100 millones")]),
       ("Pero la guerra se decidía", -.1), ("PlayStation, más de cien millones|fin", .9), ["32,93 millones", "más de cien millones"], "barras ventas", y=.6),
    mg(N.barras("En casa y fuera", [(5.54, "Japón", "5,54 millones"), (20.63, "América", "20,63 millones")]), ("Y en su propio país", -.1),
       ("frente a 20,63 en América|fin", .9), ["5,54 millones", "20,63 en América"], "barras regiones", y=.6),
    peg("GameCube llegó en 2001", "gamecube", "GameCube (2001)", x=.2, y=.62, tam=420, dur=4.6),
    ficha("Perdió en las cifras", "Una consola rara", "Pocos juegos, *muchas ideas raras*, y accesorios que *cuesta creer*.", a=("cuesta creer que existieran|fin", .6)),
    grande("Así que vamos con lo bueno", "n64", "Nintendo 64", lado="izq", dur=4.4, tam=560),

    # ================================================================ 30 · WALUIGI
    sil("Waluigi nació en Mario Tennis", "waluigi", "Waluigi", "Mario Tennis, 2000", dur=6.4, lado="izq"),
    cam("que Wario tuviera pareja", "wario", "Wario", dur=3.6, x=.86, y=.68),
    ficha("Su nombre mezcla Luigi", "Wa + Luigi", "*Warui* (malo, en japonés) + *Luigi*. Y una *L invertida* en la gorra.", a=("su forma de ser malvado|fin", .6)),
    mg(N.contador("Juegos propios de Waluigi", [(25, "años de vida", "25 años"), (0, "juegos propios", "0")], w=900), ("Un cuarto de siglo después", -.1),
       ("internet lo adora|fin", .9), ["Un cuarto de siglo", "sin juego propio"], "contador waluigi", x=.3, y=.62),

    # ================================================================ 29 · EXCITEBIKE
    peg("una versión emulada del Excitebike original", "c_excitebike_nes", "Excitebike (NES)", x=.2, y=.6, tam=400, dur=4.6),
    mg(N.lista(["El *Excitebike* original, emulado", "*Excite 3D*", "*Fútbol* con motos y un balón gigante"], "Escondido en el cartucho", w=1060),
       ("versión emulada del Excitebike", -.4), ("un balón gigante|fin", .8), ["versión emulada", "Excite 3D", "un partido de fútbol"], "lista excitebike", y=.62),
    ficha("Un juego viejo emulado", "Excitebike 64", "Un juego viejo dentro de uno nuevo: *Switch Online*, en el año 2000.", a=("y no lo sabía|fin", .6), x=.5, y=.34),

    # ================================================================ 28 · PILOTWINGS
    ficha("la isla Little States", "Little States", "Estados Unidos *en miniatura*.", tipo="Pilotwings 64", dur=4.4),
    cam("Es la de Mario", "mario", "Mario", dur=3.8, x=.14, y=.66),
    mg(N.cadena([("La cara de Mario", None, P("mario")), ("Misiles del girocóptero", None, None), ("Aparece Wario", None, P("wario"))], "El monte Rushmore", w=1300),
       ("Si le disparas", -.1), ("Y aparece Wario|fin", 1.0), ["Si le disparas", "con los misiles", "aparece Wario"], "cadena rushmore", y=.6),
    ficha("con Paradigm", "Paradigm Simulation", "Hacían *simuladores militares*. De ahí los misiles.", a=("bombardear a su mascota|fin", .6)),

    # ================================================================ 27 · EL STICK
    rel("El famoso stick analógico", "mando_n64", "El mando", "Nintendo 64", dur=4.0, x=.22),
    mg(N.stick_optico(), ("Mueve una rueda", -.3), ("lo vuelve a centrar|fin", .9), ["Mueve una rueda", "al encender la consola", "apretar L, R y Start"], "stick optico", y=.55),
    ficha("con el uso, el mecanismo se aflojaba", "Apunta esto", "Con el uso, *el stick se aflojaba*. Volverá en esta lista.", a=("y no para bien|fin", .6), x=.5, y=.36),

    # ================================================================ 26 · 64 BITS
    peg("Los 64 bits de la Nintendo 64", "n64", "Nintendo 64", x=.18, y=.66, tam=380, dur=3.6),
    mg(N.bits(), ("El nombre lo vendía todo", -.1), ("porque va mejor|fin", 1.0), ["El nombre lo vendía", "Pero casi nadie los usaba", "en segunda"], "bits", y=.55),

    # ================================================================ 25 · RUMBLE PAK
    peg("Star Fox 64 llegó con un regalo", "c_starfox", "Star Fox 64 (1997)", x=.8, y=.58, tam=420, dur=4.6, giro=4),
    rel("el Rumble Pak", "rumble_pak", "Rumble Pak", "Abril de 1997", dur=5.0, x=.25),
    mg(N.lista(["Te dan un golpe", "El mando *tiembla*", "Para guardar: *sácalo*"], "Rumble Pak", w=900), ("Cuando te daban un golpe", -.1),
       ("te tocaba sacarlo|fin", .8), ["Cuando te daban", "el mando temblaba", "te tocaba sacarlo"], "lista rumble", x=.66, y=.62),
    ficha("funcionaba con dos pilas AAA", "Rumble Pak", "*Dos pilas AAA*, y ocupaba el puerto de la *tarjeta de memoria*.", dur=5.4, x=.26, y=.22),

    # ================================================================ 24 · WIDE-BOY64
    ficha("Con esto: el Wide-Boy64", "Wide-Boy64", "Hardware real de *Game Boy* dentro. Para *prensa y desarrolladores*.", a=("hardware real de Game Boy dentro|fin", .6)),
    cam("ponía los juegos de Game Boy", "game_boy", "Game Boy", dur=4.0, x=.14, y=.66),
    mg(N.contador("Precio del Wide-Boy64", [(1400, "dólares", "1 400 US$")], w=900), ("Costaba 1 400 dólares", -.1), ("soplándole al cartucho|fin", .6),
       ["Costaba 1 400"], "contador wideboy", x=.32, y=.6),

    # ================================================================ 23 · JUMPER PAK
    mg(N.mito("Es una pieza *que no hace nada*.", "Sin ella, ni un Expansion Pak, la consola *no arranca*.", "El tapón", w=1000),
       ("encuentras una pieza que parece no hacer nada", -.3), ("la tele se queda en negro|fin", .8),
       ["parece no hacer nada", "No tiene memoria", "la consola no arranca"], "mito jumper", x=.6, y=.58),
    ficha("antes de dar por muerta", "Consejo", "Antes de dar por muerta una N64, *mira ese tapón*.", dur=4.6, x=.5, y=.34),

    # ================================================================ 22 · 4 KB
    mg(N.textura(), ("La culpa la tenían cuatro kilobytes", -.1), ("Era supervivencia|fin", .8), ["cuatro kilobytes", "se quedaban en la mitad", "tantas superficies"],
       "textura", y=.55),
    peg("Por eso Super Mario 64", "c_mario64", "Super Mario 64", x=.88, y=.74, tam=300, dur=4.4, giro=5),
    ficha("Para que te hagas una idea", "4 KB", "El texto de este guion *no cabría ahí*.", dur=4.2, x=.5, y=.36),

    # ================================================================ 21 · YOSHI VALLEY
    peg("En Mario Kart 64, Yoshi Valley", "c_mariokart", "Mario Kart 64", x=.16, y=.64, tam=360, dur=3.4),
    mapa("MK64_SpecialCup_YoshiValley.jpg", [(_ENT[0], _ENT[1], "Entrada al valle", "inicio")] + _VUELTA_LARGA + _TRAMO_FINAL + [(_HUEVO[0], _HUEVO[1], "El huevo de Yoshi", "meta")],
         ("Yoshi Valley es un laberinto", -.1), ("solo verás un signo de interrogación|fin", .2), ["Yoshi Valley", "varios caminos", "Tantos, que el juego"],
         "Yoshi Valley", sub="Mapa de VGMaps · el camino largo", viajeros=["mario"]),
    mg(N.posicion(), ("Lo reconoce hasta el manual", -.1), ("solo verás un signo de interrogación|fin", 1.0), ["un signo de interrogación"], "posicion", x=.82, y=.5),
    mapa("MK64_SpecialCup_YoshiValley.jpg", [(_ENT[0], _ENT[1], "Entrada al valle", "inicio")] + _ATAJO + _TRAMO_FINAL + [(_HUEVO[0], _HUEVO[1], "El huevo de Yoshi", "paso")] + _SALIDA
         + [(.8225, .605, "Meta", "meta")],
         ("Mira el mapa", -.1), ("hasta cruzar la meta|fin", .6), ["Mira el mapa", "caminos distintos", "hasta cruzar la meta"],
         "Yoshi Valley", sub="Otro camino, otra distancia", viajeros=["luigi"]),

    # ================================================================ 20 · POKÉMON STADIUM
    peg("Pokémon Stadium traía el Transfer Pak", "c_stadium", "Pokémon Stadium", x=.82, y=.58, tam=400, dur=4.2, giro=4),
    rel("el Transfer Pak", "transfer_pak", "Transfer Pak", "Cartuchos de Game Boy al mando", dur=4.6, x=.24),
    peg("jugar a Rojo y Azul", "c_pokered", "Pokémon Rojo y Azul", x=.2, y=.62, tam=400, dur=4.4),
    mg(N.velocidad([(1, "Velocidad normal", None), (2, "Torre Doduo", P("doduo")), (3, "Torre Dodrio", P("dodrio"))], "Game Boy Tower"),
       ("Y con la torre Doduo", -.2), ("subido de nivel a un Magikarp|fin", .3), ["Y con la torre", "al doble de velocidad", "al triple"], "velocidad", x=.6, y=.55),
    cam("subido de nivel a un Magikarp", "magikarp", "Magikarp", dur=3.4, x=.14, y=.66),

    # ================================================================ 19 · CLAYFIGHTER
    grande("ClayFighter sesenta y tres y un tercio", "c_clayfighter", "ClayFighter 63 1/3", lado="der", dur=5.0, tam=520, giro=3),
    peg("solo para alquilar en Blockbuster", "blockbuster", "Blockbuster", x=.2, y=.7, tam=340, dur=3.6),
    mg(N.contador("Heritage, noviembre de 2024", [(175000, "dólares por un ejemplar sellado", "175 000 US$")], w=1000), ("un ejemplar sellado", -.8),
       ("175 000 dólares|fin", 1.2), ["se vendió en Heritage"], "contador subasta", y=.6),
    ficha("Seguro que tú lo devolviste", "Blockbuster", "Lo devolviste a tiempo, ¿verdad? *Una lástima.*", dur=3.6, x=.5, y=.36),

    # ================================================================ 18 · SUPERMAN 64
    sil("Superman 64 es famoso por dos cosas", "superman", "Superman", "Superman 64, 1999", dur=5.4, lado="izq"),
    peg("y esos anillos", "c_superman", "Superman 64", x=.82, y=.58, tam=380, dur=3.4, giro=4),
    mg(N.tachones(["Un mundo abierto", "Un SimCity con Superman de alcalde", "Sin poderes ni destrozos", "Anillos"], "Lo que iba a ser", w=980),
       ("Pero ese no era el plan", -.1), ("Y acabaron siendo el juego", 1.2), ["quería un mundo abierto", "un SimCity", "le limitó los poderes", "Los anillos eran"],
       "tachones superman", x=.62, y=.55),
    cam("creado por Lex Luthor", "lex_luthor", "Lex Luthor", dur=3.8, x=.14, y=.66),
    ficha("la famosa niebla de kriptonita", "La niebla", "Era una forma de *no dibujar el horizonte*.", a=("no dibujar el horizonte|fin", .8), x=.5, y=.34),

    # ================================================================ 17 · ARCADES ULTRA 64
    aba([("ultra64_arcade", "Killer Instinct"), ("cruisn", "Cruis'n USA")], ("Killer Instinct y Cruis'n USA", -.6), ("Killer Instinct y Cruis'n USA|fin", 2.0),
        ["Killer Instinct", "Cruis'n USA"], "abanico arcades", x=.26),
    mg(N.mito("Los arcades *Ultra 64* llevaban el hardware de la consola.", "Cada máquina tenía *su propia placa*.", "Publicidad", w=1000),
       ("Las vendían como un adelanto", -.1), ("Cada una tenía su propia placa|fin", .9), ["Las vendían como", "ninguna llevaba", "Cada una tenía"], "mito arcades", x=.6, y=.58),
    peg("Killer Instinct Gold", "c_ki_gold", "Killer Instinct Gold", x=.8, y=.6, tam=400, dur=4.2, giro=4),

    # ================================================================ 16 · POKÉMON SNAP
    peg("en los Blockbuster de Estados Unidos", "blockbuster", "Blockbuster, 1999", x=.84, y=.66, tam=320, dur=3.8, giro=4),
    peg("Llevabas tu cartucho de Pokémon Snap", "c_snap", "Pokémon Snap", x=.2, y=.6, tam=400, dur=4.0),
    mg(N.lista(["Tu cartucho de *Pokémon Snap*", "Eliges tus *mejores fotos*", "*3 dólares* = *16 pegatinas*"], "El quiosco", w=980),
       ("Llevabas tu cartucho", .6), ("te llevabas dieciséis pegatinas|fin", .9), ["Llevabas tu cartucho", "elegías tus mejores fotos", "dieciséis pegatinas"],
       "lista quiosco", x=.64, y=.6),
    ficha("En Japón se hizo lo mismo", "Japón", "Lo mismo, en las tiendas *Lawson*.", dur=3.6, x=.3, y=.34),
    cam("presumir a tu Pikachu", "pikachu", "Pikachu", dur=3.6, x=.86, y=.66),

    # ================================================================ 15 · HOTELES
    ficha("Era el sistema Nintendo Gateway", "Nintendo Gateway", "Con *LodgeNet*. Febrero de 2000: *100 000 habitaciones*, *620 hoteles*.",
          a=("de 620 hoteles|fin", .6)),
    mg(N.factura([("Habitación 512", "1 noche"), ("Nintendo 64: Mario Kart", "3 h"), ("Se paga por hora", "sí")], "3 h de juego"),
       ("Pagabas por hora", -.1), ("tres horas de Mario Kart|fin", 1.2), ["Pagabas por hora", "cuenta de la habitación", "Imagina justificarle", "tres horas de Mario Kart"],
       "factura hotel", x=.3, y=.5),

    # ================================================================ 14 · iQUE
    sil("el iQue Player", "ique", "iQue Player", "China, noviembre de 2003", dur=5.6, lado="der"),
    mg(N.cadena([("Prohibición en China", "2000", None), ("iQue Player", "2003", P("ique")), ("Juegos en quioscos", None, None), ("Fin del servicio", "2016", None)],
                "La Nintendo 64 china", w=1500), ("China prohibía las consolas", -.1), ("de la Nintendo 64 original|fin", .6),
       ["China prohibía", "esto sorteaba", "los juegos se bajaban", "hasta finales de 2016"], "cadena ique", y=.6),
    ficha("Se calcula que vendió", "Ventas", "Entre *8 000 y 12 000* unidades.", tipo="Estimación", dur=4.0, x=.5, y=.3),

    # ================================================================ 13 · PERFECT DARK
    grande("En el E3 de 1999, Rare", "c_perfectdark", "Perfect Dark", lado="der", dur=4.6, tam=480, giro=3),
    rel("Con una Game Boy Camera", "gb_camera", "Game Boy Camera", "+ Transfer Pak", dur=4.6, x=.24),
    ficha("Se llamaba Perfect Head", "Perfect Head", "Probado de verdad: capturas internas con *la cara de Ken Lobb*.", a=("la cara de Ken Lobb|fin", .6)),
    mg(N.mito("Se cortó *por Columbine*.", "Es lo que se cree, pero *no hay confirmación oficial*.", "¿Por qué se eliminó?", w=1000),
       ("La función se eliminó", -.1), ("ninguna confirmación oficial|fin", .9), ["La función se eliminó", "Mucha gente lo atribuye", "no hay ninguna confirmación"],
       "mito perfect head", y=.58),

    # ================================================================ 12 · DK64
    rel("El Expansion Pak de Donkey Kong 64", "expansion_pak", "Expansion Pak", "4 MB más de RAM", dur=4.6, x=.25),
    peg("Donkey Kong 64 es uno de los dos", "c_dk64", "Donkey Kong 64", x=.8, y=.6, tam=420, dur=4.6, giro=4),
    mg(N.dos_versiones("El Expansion Pak de DK64", ("Chris Marlow", "Tapaba un *bug* que colgaba el juego."), ("Simon Craddick", "Solo era para la *iluminación*.")),
       ("El programador Chris Marlow", -.1), ("como si estuviera cerrada|fin", .8), ["Chris Marlow", "Simon Craddick", "Dos personas del mismo equipo"], "versiones dk64", y=.6),

    # ================================================================ 11 · BODY HARVEST
    peg("DMA Design, un estudio escocés", "dma", "DMA Design", x=.2, y=.64, tam=360, dur=4.2),
    peg("enseñó Body Harvest en 1995", "c_bodyharvest", "Body Harvest", x=.8, y=.6, tam=420, dur=4.6, giro=4),
    ficha("Nintendo lo vio demasiado violento", "Body Harvest", "Retrasado y soltado. Salió en *1998* con otras editoras.", a=("con otras editoras|fin", .6), x=.3, y=.36),
    mg(N.cadena([("Body Harvest", "1998", P("c_bodyharvest")), ("Rockstar North", None, P("rockstar_north")), ("Grand Theft Auto III", "2001", P("c_gta3"))],
                "El mismo estudio", w=1300), ("Ese estudio hoy se llama", -.1), ("ponlos uno al lado del otro|fin", 1.0),
       ["Ese estudio", "Rockstar North", "Grand Theft Auto III"], "cadena dma", y=.6),

    # ================================================================ 10 · ANIMAL FOREST
    grande("con el nombre de Dobutsu no Mori", "c_animalforest", "Dobutsu no Mori (2001)", lado="der", dur=4.8, tam=500, giro=3),
    cam("Katsuya Eguchi lo diseñó", "eguchi", "Katsuya Eguchi", dur=4.0, x=.14, y=.66),
    mg(N.cadena([("Diseñado para el 64DD", None, P("dd64")), ("Un reloj en el cartucho", None, None), ("Un pueblo que sigue vivo", None, P("c_animalforest"))],
                "Del disco al cartucho", w=1300), ("porque ese accesorio llevaba reloj", -.2), ("Por culpa de un accesorio que no funcionó|fin", .8),
       ["llevaba reloj interno", "meter un reloj", "Así nació la idea"], "cadena animal", y=.6),

    # ================================================================ 9 · 64DD Y RANDNET
    rel("El 64DD, ese accesorio de discos", "dd64", "64DD", "Japón, diciembre de 1999", dur=5.0, x=.25),
    peg("un servicio en línea: Randnet", "randnet", "Randnet", x=.8, y=.62, tam=380, dur=3.8, giro=4),
    mg(N.barras("Randnet", [(100000, "Sitio para", "100 000"), (15000, "Al cierre", "poco más de 15 000")]), ("Costaba 2 500 yenes", -.1),
       ("poco más de 15 000|fin", .9), ["Tenía sitio para", "poco más de 15 000"], "barras randnet", y=.6),
    mg(N.linea_tiempo([("Dic 1999", "Sale el 64DD"), ("28 feb 2001", "Se apaga Randnet"), ("Total", "Diez discos")], "Catorce meses", w=1400),
       ("El 28 de febrero de 2001", -.1), ("se quedó con diez discos|fin", .8), ["El 28 de febrero", "catorce meses", "diez discos"], "linea randnet", y=.76),
    ficha("Pero de ese accesorio salieron", "Del 64DD", "Salieron *tres* de los secretos más grandes de esta lista.", dur=4.4, x=.5, y=.36),

    # ================================================================ 8 · RESIDENT EVIL 2
    grande("Resident Evil 2 ocupaba dos CD", "c_re2", "Resident Evil 2 (N64)", lado="der", dur=4.6, tam=480, giro=3),
    mg(N.barras("Resident Evil 2", [(1300, "PlayStation", "dos CD"), (64, "Nintendo 64", "64 MB")]), ("Y Angel Studios lo metió", -.2),
       ("un cartucho de 64 megabytes|fin", .9), ["Angel Studios", "un cartucho de 64"], "barras re2", x=.4, y=.62),
    ficha("Nueve personas a tiempo completo", "Angel Studios", "*9 personas*, unos *12 meses*. Comprimieron hasta las *cinemáticas*.",
          a=("nadie esperaba ver en esa consola|fin", .6)),
    cam("Digital Foundry lo llamó", "digital_foundry", "Digital Foundry", dur=4.0, x=.14, y=.66, foco=(.5, .5, 1.05)),
    ficha("Un milagro técnico", "Ventas", "En Estados Unidos: poco más de *326 000* copias.", dur=4.4, x=.5, y=.36),

    # ================================================================ 7 · MARIO PARTY
    grande("Mario Party tenía minijuegos", "c_marioparty", "Mario Party", lado="der", dur=4.2, tam=460, giro=3),
    mg(N.calor(), ("Y los niños descubrieron", -.1), ("hasta cuatro por familia|fin", .9),
       ["lo girabas con la palma", "las ampollas", "unas 90 quejas", "guantes acolchados"], "calor", y=.55),
    ficha("Piénsalo", "Ironía", "La consola del *stick analógico*, repartiendo *material de protección*.", a=("material de protección|fin", .6), x=.5, y=.36),

    # ================================================================ 6 · TETRIS 64
    grande("salió en Japón Tetris 64", "c_tetris64", "Tetris 64 (1998)", lado="der", dur=4.4, tam=460, giro=3),
    ficha("el Bio Sensor", "Bio Sensor", "Una *pinza para la oreja* enchufada al mando.", dur=4.6, x=.3, y=.36),
    mg(N.pulso(), ("En el modo Bio Tetris", -.1), ("demasiado tranquilo|fin", .9), ["En el modo Bio Tetris", "se te aceleraba el pulso", "un modo al revés"], "pulso", y=.55),
    rel("el Vitality Sensor de Wii", "vitality", "Vitality Sensor", "Wii, 2009: nunca salió", dur=5.0, x=.25),

    # ================================================================ 5 · FINAL FANTASY 64
    peg("Una demo de Final Fantasy en 3D", "c_ff6", "Final Fantasy VI", x=.82, y=.6, tam=380, dur=4.2, giro=4),
    mg(N.mito("La demo de Final Fantasy *corría en Nintendo 64*.", "Corría en estaciones *Silicon Graphics Onyx*, en SIGGRAPH 1995.", "Final Fantasy 64", w=1100),
       ("la prueba de que venía a Nintendo 64", -.6), ("Silicon Graphics Onyx|fin", .8), ["la prueba de que venía", "jamás corrió", "Corría en estaciones"],
       "mito ff", y=.58),
    cam("Corría en estaciones Silicon Graphics Onyx", "sgi_onyx", "SGI Onyx", dur=4.0, x=.14, y=.7),
    ficha("lo lanzó la revista GameFan", "El rumor", "Lo lanzó *GameFan*. Square *nunca anunció nada* para la N64.", a=("nada para esa consola|fin", .6)),

    # ================================================================ 4 · FINAL FANTASY VII
    ban("Hironobu Sakaguchi quería cine", "sakaguchi", "Sakaguchi", "Hironobu Sakaguchi, creador de Final Fantasy", dur=5.2),
    ficha("Según contó en 2024", "Sakaguchi, 2024", "En cartucho habría pasado de los *10 000 yenes*.", dur=5.0, x=.3, y=.36),
    cam("hablar con Yamauchi", "yamauchi", "Hiroshi Yamauchi", dur=3.6, x=.86, y=.66),
    grande("Final Fantasy VII salió en tres discos", "c_ff7", "Final Fantasy VII (1997)", lado="izq", dur=4.4, tam=480),
    peg("Y Dragon Quest VII se fue detrás", "c_dq7", "Dragon Quest VII", x=.8, y=.6, tam=380, dur=3.8, giro=4),
    mg(N.dos_versiones("¿Y después?", ("Una versión", "A Square le dijeron *que no volviera nunca*."), ("La otra", "Yamauchi *lo aceptó sin más*.")),
       ("Lo que pasó después", -.1), ("Ninguna está cerrada|fin", .8), ["En una,", "En otra,", "Ninguna está cerrada"], "versiones square", y=.6),

    # ================================================================ 3 · EARTHBOUND 64
    sil("Shigesato Itoi enseñó EarthBound 64", "itoi", "Shigesato Itoi", "Space World 1997", dur=5.4, lado="izq"),
    peg("EarthBound 64 para el 64DD", "c_earthbound64", "EarthBound 64", x=.8, y=.6, tam=400, dur=4.0, giro=4),
    mg(N.progreso(60, "EarthBound 64"), ("El juego acabó pasando a cartucho", -.1), ("Iba por el 60 por ciento|fin", .8),
       ["El juego acabó", "anunció que se cancelaba"], "progreso earthbound", y=.62),
    ban("Quien tomó la decisión fue Satoru Iwata", "iwata", "Satoru Iwata", "Quédate con ese nombre", dur=5.0),
    peg("como Mother 3", "c_mother3", "Mother 3 (2006)", x=.2, y=.62, tam=380, dur=3.8),
    mg(N.contador("Subasta de 2021", [(357, "dólares por un CD", "357 US$"), (25, "segundos inéditos", "25 s")], w=900), ("un fan pagó 357 dólares", -.6),
       ("Veinticinco segundos|fin", .8), ["357 dólares", "25 segundos"], "contador subasta mother", x=.66, y=.6),

    # ================================================================ 2 · WARIOWARE
    peg("Mario Artist: Polygon Studio", "c_polygon", "Mario Artist", x=.82, y=.6, tam=380, dur=4.4, giro=4),
    ficha("Sound Bomber", "Sound Bomber", "Juegos que *duraban segundos*.", tipo="Mario Artist: Polygon Studio (64DD)", dur=4.4, x=.3, y=.36),
    mg(N.postits(["Juegos de segundos", "Sin decírselo al jefe", "Ideas en Post-it", "Protagonista: Wario"], "Ideas en secreto"),
       ("retomaron la idea", -.4), ("siempre anda haciendo tonterías|fin", .6), ["retomaron la idea", "sin decírselo a su jefe", "notas Post-it", "eligieron a Wario"],
       "postits", y=.6),
    grande("Eso se convirtió en WarioWare", "c_warioware", "WarioWare", lado="der", dur=4.0, tam=440, giro=3),
    cam("según Yoshio Sakamoto", "sakamoto", "Yoshio Sakamoto", dur=4.0, x=.88, y=.72),
    sil("Una saga entera", "wario", "Wario", "Haciendo tonterías desde 2003", dur=5.0, lado="der"),

    # ================================================================ 1 · SMASH BROS.
    ban("Masahiro Sakurai, de HAL Laboratory", "sakurai", "Masahiro Sakurai", "HAL Laboratory", dur=5.0),
    sil("Y quien le programó el prototipo fue Satoru Iwata", "iwata", "Satoru Iwata", "Programó el prototipo", dur=5.4, lado="der"),
    ficha("Iwata llevaba otro proyecto", "Fines de semana", "Lo programó *él solo*, en sus *fines de semana*.", dur=6.6, x=.3, y=.36),
    mg(N.sin_cara([(P("mario"), "Mario"), (P("donkey_kong"), "Donkey Kong"), (P("samus"), "Samus"), (P("fox"), "Fox")], "Dragon King: The Fighting Game"),
       ("El prototipo se llamaba Dragon King", -.1), ("Samus y Fox|fin", 1.2), ["El prototipo se llamaba", "meter a Mario", "Donkey Kong", "Samus", "y Fox"],
       "sin cara smash", y=.58),
    grande("Super Smash Bros. salió en enero de 1999", "c_smash", "Super Smash Bros. (1999)", lado="der", dur=4.6, tam=480, giro=3),
    mg(N.contador("Super Smash Bros.", [(5.55, "millones de copias", "5,55 millones")], w=900), ("vendió 5,55 millones", -.4),
       ("una de las grandes sagas de Nintendo|fin", .4), ["vendió 5,55"], "contador smash", x=.32, y=.6),
    mg(N.cita(["En mi tarjeta, soy *presidente*.", "En mi mente, soy *desarrollador*.", "En mi corazón, soy *un jugador*."], "Satoru Iwata · GDC 2005"),
       ("En mi tarjeta soy presidente", -.2), ("soy un jugador|fin", 1.4), ["En mi tarjeta", "En mi mente", "Pero en mi corazón"], "cita iwata", y=.66),
    leg("iwata", "Satoru Iwata", ["1959 - 2015", "Presidente de Nintendo", "Programador de fin de semana"], ("Satoru Iwata murió", -.1),
        ("porque le encantaba|fin", .8), marcas=["Satoru Iwata murió"], x=.24, y=.52),

    # ================================================================ CIERRE
    peg("ya está en Switch 2", "switch2", "Switch 2", x=.2, y=.7, tam=360, dur=3.6),
    aba([("c_dk64", "Donkey Kong 64"), ("c_pilotwings", "Pilotwings 64")], ("y Donkey Kong 64 y Pilotwings 64", -.2), ("están en Switch Online|fin", .8),
        ["Donkey Kong 64", "Pilotwings 64"], "abanico switch online", x=.74),
    com("Antilopez Mexicanos escribió", "Ugw2j_5-7ktR9uVpcxl4AaABAg", dur=7.6, x=.30, y=.32),
    com("Y Riuma sueña con que Nintendo", "UgxdnznPHsijj-I2lE94AaABAg", dur=7.4, x=.68, y=.34),
    ficha("Ahora dime tú", "Te leo", "¿Cuál de estos *treinta* no conocías?", tipo="En los comentarios", a=("Te leo abajo|fin", .8), x=.5, y=.40),
    peg("Y ponte los guantes", "c_marioparty", "Ponte los guantes", x=.78, y=.6, tam=420, dur=3.6, giro=4),
]
ROTULOS = []
SFX = {}
# SONIDOS DEL PROPIO JUEGO de cada secreto (regla del 29-oct-2026): sfx/n64_*.mp3
_ESTRIBILLO = {"treinta": "n64_mariotennis_waluigi_risa", "veinticinco": "n64_starfox_barrel_roll", "veintiuno": "n64_mk64_cuenta_regresiva",
               "veinte": "n64_stadium_pikachu", "diecisiete": "n64_ki_combo_breaker", "dieciséis": "n64_snap_pikachu", "doce": "n64_dk64_banana_ficha",
               "ocho": "n64_re2_puerta", "siete": "n64_marioparty_anunciador_start", "uno": "n64_smash_anunciador_super_smash_bros"}
PISTAS = [dict(sfx=v, en="Número " + k, vol=.45) for k, v in _ESTRIBILLO.items()] + [
    dict(sfx="n64_consola_arranque", en="Todo eso pasó en la misma consola", vol=.5),
    dict(sfx="n64_mk64_mario_letsago", en="Y ahí nacieron las tardes enteras", vol=.5),
    dict(sfx="n64_mariotennis_waluigi_numero_uno", en="Y aun así, internet lo adora", vol=.5),
    dict(sfx="n64_starfox_bomba", en="Cuando te daban un golpe", vol=.45),
    dict(sfx="n64_mk64_caja_objeto_ruleta", en="Tantos, que el juego no puede", vol=.4),
    dict(sfx="n64_mk64_mario_wee_hee", en="Mira el mapa", vol=.45),
    dict(sfx="n64_stadium_doduo", en="Y con la torre Doduo", vol=.5),
    dict(sfx="n64_stadium_dodrio", en="y con la Dodrio, al triple", vol=.5),
    dict(sfx="n64_stadium_magikarp", en="subido de nivel a un Magikarp", vol=.5),
    dict(sfx="n64_ki_gold_ultra_combo", en="Y lo que llegó a casa fue Killer Instinct Gold", vol=.45),
    dict(sfx="n64_dk64_oh_banana", en="Suena perfecto", vol=.45),
    dict(sfx="n64_re2_puerta_2", en="Un milagro técnico", vol=.45),
    dict(sfx="n64_marioparty_anunciador_timeup", en="La fiscalía de Nueva York", vol=.45),
    dict(sfx="n64_marioparty_victoria", en="Nintendo ofreció guantes acolchados", vol=.35),
    dict(sfx="n64_smash_golpe", en="a algunos directivos no les gustaba", vol=.45),
    dict(sfx="n64_smash_anunciador_game_set", en="Pero la demo los convenció", vol=.5),
    dict(sfx="n64_mk64_mario_welcome", en="Y si te gustó este viaje", vol=.45),
]
