# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Zelda Ocarina of Time REMAKE: los 15 CAMBIOS frente al ORIGINAL de N64» (SECUENCIA YT, Crónicas del
gaming, 26-oct-2026). Fórmula de majora_mask con todo TRANSLÚCIDO (regla del 22-oct):
- PEGATINAS reales de lo que nombra la voz (pegatinas/, fuentes en pegatinas/_fuentes.txt; bajar_pegatinas.py), abajo a la
  izquierda o grandes del lado contrario.
- `puesto` = cartel «Cambio número N» y `ficha` = el cuadro de diálogo de N64 (mg_majora: el mismo motor de Ocarina).
- MG NUEVOS de ESTE guion (nucleo/mg_oot.py): VENTANA DEL ORIGINAL (FX `video` con el N64 de medios/n64/ + `marco` con los
  colores de N64 y la `etiqueta` SWITCH 2 en el cuadro grande) cada vez que se compara; `contador` de rupias 99 -> 200;
  `linea_tiempo` 1998 -> 2026; `partitura` de la ocarina (botones A/C -> onda del micrófono); `sticks` (uno contra dos);
  `balance` final (confirmado / sin confirmar).
- SONIDO ORIGINAL del juego en 21 beats (regla del usuario del 26-oct): guion.SECUENCIA["ambiente_por"]; sin SFX añadidos.
  python fab.py oot_remake_cambios fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py oot_remake_cambios fx         audio/fx.wav
"""
import os

import mg_majora as M
import mg_oot as O

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_N64 = os.path.join(_AQUI, "medios", "n64")
_FX, _FY = .74, .40     # fichas: a la derecha (el cartel del cambio va arriba)
# ventana del original: abajo a la derecha; el marco tiene 25 px más arriba (sitio de la píldora)
_VW, _VX, _VY = 576, .79, .69
_VH = round(_VW / 1.312)

CAMARA = {}
FUNDIDO = {}


def _img(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=M.pegatina(_img(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(en, items, y=.66, tam=320, dur=5.0):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    paso = max(.17, (tam + 90) / 1920)
    return [peg(a or en, s, t, dur=dur, x=.12 + paso * i, y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY):
    d = dict(tipo="mg", fn=M.ficha(titulo, texto, tipo=tipo), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, dur=3.8):
    return dict(tipo="mg", fn=M.puesto(num, titulo, arriba=f"Cambio número {num}"), en=en, dur=dur, x=.5, y=.17, sale=.45,
                nombre=f"puesto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def ventana(slug, de, a, desde=0.0, año="1998"):
    """El ORIGINAL de N64 en una ventana (FX video) con su marco de colores + la etiqueta SWITCH 2 sobre el cuadro grande."""
    ruta = os.path.join(_N64, slug + ".mp4")
    return [dict(tipo="video", de=de, a=a, ruta=ruta, desde=desde, x=_VX, y=_VY, ancho=_VW, entra=.35, sale=.35,
                 nombre="ventana " + slug),
            dict(tipo="mg", fn=O.marco(_VW, _VH, año), de=de, a=a, x=_VX, y=_VY - 25 / 1080, sale=.35,
                 nombre="marco " + slug, ver=2.0),
            dict(tipo="mg", fn=O.etiqueta("SWITCH 2", "2026"), de=de, a=a, x=.12, y=.09, sale=.35, nombre="etiqueta sw2",
                 ver=1.0)]


_P = _img
FX = [
    # ================================================================ GANCHO
    peg("en Nintendo Switch 2", "switch2", "Nintendo Switch 2", tam=300, x=.84, y=.26, dur=4.4),
    peg("Y la ocarina se puede tocar tarareando", "ocarina", "La Ocarina del Tiempo", tam=340, x=.18, y=.64),
    grande("y Eiji Aonuma explicó por qué", "aonuma", "Eiji Aonuma", lado="der", dur=4.2, tam=480),
    ficha("Así que hoy te cuento", "Ocarina of Time", "Cómo llegamos al remake y *15 cambios* frente al original.",
          tipo="Nintendo Switch 2 / 5 de noviembre de 2026", a=("al Ocarina of Time de Nintendo 64|fin", .6)),

    # ================================================================ CONTEXTO
    peg("para la Nintendo 64", "n64", "Nintendo 64 (1998)", tam=380, x=.80, y=.30, dur=4.4),
    ficha("Fue el primer juego en sacar", "Ocarina of Time (1998)", "Primer *40/40* de Famitsu. Metacritic: *99*, la nota "
          "más alta.", tipo="Nintendo 64", a=("la nota más alta de Metacritic, un 99|fin", .6), x=.27),
    grande("lo llevaron a la Nintendo 3DS", "n3ds", "Ocarina of Time 3D (2011)", lado="der", dur=5.0, tam=520),
    mg(O.linea_tiempo([("1998", "Nintendo 64", _P("n64")), ("2011", "Nintendo 3DS (Grezzo)", _P("n3ds")),
                       ("9 jun 2026", "El anuncio", None), ("8 sep 2026", "La demo de Aonuma", _P("aonuma"))]),
       ("Nintendo lo anunció en su Direct", -.2), ("jugada por el propio Eiji Aonuma|fin", .6),
       [("Nintendo lo anunció en su Direct", .1), ("Nintendo lo anunció en su Direct", .7), "del 9 de junio",
        "en el Direct del 40 aniversario"], "línea de tiempo", y=.70),
    *ventana("kokiri", ("Todo está rehecho", -.2), ("Los lugares se remodelaron|fin", .3)),
    ficha("Saldrá solo en Switch 2", "Ocarina of Time (Switch 2)", "*5 de noviembre*. Solo en Switch 2, *59,99 dólares* "
          "en Estados Unidos.", tipo="El lanzamiento", a=("en Estados Unidos|fin", .6)),
    peg("Y Aonuma lo resumió así", "aonuma", "Eiji Aonuma", tam=360, x=.18, y=.62, dur=7.2),
    ficha("Y Aonuma lo resumió así", "Eiji Aonuma", "«Un remake *en gran parte fiel* al original, con *controles "
          "modernos*.»", tipo="Productor de la saga", a=("con controles modernos|fin", 1.0)),

    # ================================================================ 15 / LA BOLSA
    puesto("Número 15.", 15, "Una bolsa más grande"),
    peg("una bolsa de solo 99 rupias", "rupia", "99 rupias", tam=300, x=.80, y=.62),
    peg("La primera mejora era la bolsa de adulto", "bolsa_adulto", "Bolsa de adulto", tam=360, x=.18, y=.62),
    peg("a cambio de 10 Skulltulas doradas", "skulltula", "Skulltula dorada", tam=380, x=.80, y=.60),
    mg(O.contador(99, 200, "Bolsa inicial", _P("rupia")), ("En las imágenes del Direct", -.1), ("Parece poca cosa|fin", .6),
       ["el contador del remake ya marca 200"], "contador", y=.46),

    # ================================================================ 14 / AMIIBO
    puesto("En el 14, unas figuras", 14, "Unas figuras que traen máscaras"),
    ficha("Link niño, y Zelda niña", "amiibo (2027)", "Link niño y Zelda niña desbloquean *máscaras especiales* de estilo "
          "retro.", tipo="Se venden aparte", a=("de estilo retro|fin", .6), y=.36),
    peg("la de la tienda de máscaras felices", "vendedor", "Vendedor de máscaras felices", tam=420, x=.80, y=.58),
    peg("Aquí llegan desde fuera del juego", "mascara_keaton", "Máscara Keaton", tam=300, x=.18, y=.64),
    ficha("Nintendo todavía no ha detallado", "Sin detallar", "Qué máscaras son, y si hacen algo más que *cambiar el "
          "aspecto*.", tipo="Lo que falta saber", a=("cambiar el aspecto de Link|fin", .6)),

    # ================================================================ 13 / LA CARGA QUE SE QUEDA
    puesto("Número 13.", 13, "El cambio que no hicieron"),
    peg("Aonuma dijo que la mantuvieron", "aonuma", "Eiji Aonuma", tam=360, x=.18, y=.62, dur=5.0),
    ficha("Aonuma dijo que la mantuvieron", "Pantallas de carga", "Se quedaron *a propósito*, para conservar la esencia "
          "del original.", tipo="Eiji Aonuma", a=("la esencia del juego original|fin", .8)),
    ficha("En 1998, esa pausa", "1998", "Una necesidad del *cartucho*.", tipo="Nintendo 64",
          a=("es una decisión|fin", .8), x=.27, y=.42),
    ficha("En 2026, es una decisión", "2026", "Una *decisión*.", tipo="Nintendo Switch 2", a=("es una decisión|fin", .8),
          x=.73, y=.42),

    # ================================================================ 12 / ZELDA NOTES
    puesto("En el 12, el juego sale", 12, "El juego sale de la consola"),
    ficha("Guarda un registro de cada día", "Zelda Notes", "Un *registro de cada día* y lugares para encontrar con "
          "*imágenes de pista*.", tipo="App de Nintendo Switch", a=("a partir de imágenes de pista|fin", .4)),
    peg("una ocarina virtual en la pantalla", "ocarina", "Ocarina virtual", tam=320, x=.18, y=.64),
    ficha("Y trae un concurso", "Concurso", "Más de *2000 preguntas*: un intento gratis al día; más, con *rupias del "
          "juego*.", tipo="Zelda Notes", a=("pagas con rupias del juego|fin", .4)),

    # ================================================================ 11 / EL TIEMPO
    puesto("Número 11.", 11, "El tiempo ya no se detiene"),
    ficha("Pero al entrar a sitios como la Ciudadela", "Nintendo 64", "En la *Ciudadela* o el *Bosque Kokiri*, el reloj "
          "se congelaba.", tipo="1998", a=("y esperar|fin", .4)),
    *ventana("kokiri", ("En el remake, el ciclo de día", -.2), ("también dentro de los pueblos|fin", .5), desde=3.0),
    ficha("Así que la plaza del mercado", "Switch 2", "El *día y la noche* siguen también dentro de los pueblos.",
          tipo="Ciclo continuo", a=("deja de ser una foto fija|fin", .4)),

    # ================================================================ 10 / EL MENÚ
    puesto("En el 10, un menú nuevo", 10, "Un menú nuevo"),
    grande("Las botas de hierro del Templo del Agua", "botas_hierro", "Botas de hierro", lado="der", dur=5.6, tam=500),
    *ventana("menu", ("En la demo del remake, el inventario", -.2), ("en la cruceta|fin", .4)),
    ficha("Link puede seguir moviéndose", "En la demo", "Link se mueve *con el objeto en la mano*.",
          tipo="Según los análisis", a=("sostiene un objeto|fin", .6), x=.27),

    # ================================================================ 9 / GIROSCOPIO
    puesto("Número 9.", 9, "Apuntar moviendo el control"),
    *fila("el tirachinas, el arco y el gancho", [
        ("tirachinas", "Tirachinas", None), ("arco", "Arco de las hadas", "el arco"), ("gancho", "Gancho", "y el gancho")],
         dur=5.6, tam=280),
    ficha("En el remake se puede apuntar", "Giroscopio", "Apuntas *moviendo el control* o la consola.",
          tipo="Nintendo Switch 2", a=("moviendo el control o la consola|fin", .6)),
    peg("La versión de 3DS ya lo hacía", "n3ds", "Nintendo 3DS (2011)", tam=320, x=.18, y=.62),
    peg("para una Skulltula dorada", "skulltula", "Skulltula dorada", tam=380, x=.80, y=.58),

    # ================================================================ 8 / LA CIUDADELA
    puesto("En el 8, un pueblo", 8, "Un pueblo que por fin es de verdad"),
    ficha("Eran fondos pintados de antemano", "Nintendo 64", "La plaza eran *fondos prerrenderizados* con *cámaras "
          "fijas*.", tipo="1998", a=("que nunca llegas a ver|fin", .3)),
    *ventana("mercado3", ("Pero en el remake la cámara", -.2), ("y mucha más gente|fin", .5)),
    ficha("Hasta un mod de fans", "OoT unJPEG", "Un mod de fans que rehace en *3D* los fondos de la *Nintendo 64*.",
          tipo="Reonu / 2026", a=("este mismo año|fin", .6)),

    # ================================================================ 7 / LA ORQUESTA
    puesto("Número 7.", 7, "Una orquesta para Koji Kondo"),
    grande("La música original de Koji Kondo", "kondo", "Koji Kondo", lado="der", dur=5.6, tam=500),
    ficha("En el remake, Nintendo habla de música", "Música sinfónica", "Orquesta y *efectos de sonido renovados*.",
          tipo="Nintendo Switch 2", a=("efectos de sonido renovados|fin", .8)),
    ficha("Lo que todavía no ha dicho es si se podrá", "Sin confirmar", "¿Se podrá elegir la *banda sonora original*?",
          tipo="Lo que falta saber", a=("la banda sonora original|fin", 1.0)),

    # ================================================================ 6 / NAVI Y LOS HILOS DEL TIEMPO
    puesto("En el 6, adiós a depender de Navi", 6, "Adiós a depender de Navi"),
    peg("la ayuda principal era Navi", "navi", "Navi", tam=360, x=.18, y=.60, dur=5.0),
    ficha("El remake trae una función nueva", "Threads of Time", "Los *Hilos del Tiempo*: lo que llevas hecho y tu "
          "*siguiente objetivo*.", tipo="Opcional", a=("cuál es tu siguiente objetivo|fin", .6)),
    peg("quien quiera perderse como en 1998", "link_nino", "Link (1998)", tam=400, x=.80, y=.58),

    # ================================================================ 5 / LAS VOCES
    puesto("Número 5.", 5, "Hyrule por fin habla"),
    *ventana("mercado2", ("En el remake, las cinemáticas", -.2), ("tienen más diálogo|fin", .5)),
    ficha("Es la primera vez que la historia", "Voces", "Cinemáticas *con voz completa* y más diálogo.",
          tipo="Primera vez en Ocarina of Time", a=("con actores de voz|fin", .8), x=.27),
    grande("Si Link dirá una sola palabra", "link_nino", "Link", lado="der", dur=4.0, tam=520),

    # ================================================================ 4 / LA OCARINA
    puesto("En el 4, la ocarina", 4, "La ocarina, como nunca la tocaste"),
    mg(O.partitura(list("^<>^<>"), "Canción de Epona"), ("En el original, cada canción era", -.2), ("Y Link la toca|fin", .5),
       ["con las notas del botón A", "En Switch 2 puedes tararear"], "partitura", y=.72),
    ficha("Una se toca soplando", "Ocarinas de verdad", "Una *de soplar* y otra *electrónica*, de Hori, que toca "
          "canciones enteras.", tipo="Salen este año", a=("toca canciones enteras con un botón|fin", .4)),
    peg("la Canción de Epona puede salir", "epona", "Epona", tam=400, x=.18, y=.60),

    # ================================================================ 3 / CORRER
    puesto("Número 3.", 3, "Correr de verdad"),
    ficha("rodar era más rápido que correr", "Nintendo 64", "Rodar era *más rápido* que correr.", tipo="1998",
          a=("dando volteretas sin parar|fin", .4)),
    *ventana("rodar", ("En el remake, Link tiene un esprint", -.2), ("acelerar nadando|fin", .4)),
    ficha("Y el aire al bucear", "Buceo", "El aire ya no es una *cuenta atrás*: es una *barra* junto a Link.",
          tipo="En la demo", a=("una barra, junto a Link|fin", .5)),

    # ================================================================ 2 / LA CÁMARA
    puesto("En el 2, la cámara", 2, "La cámara"),
    mg(O.sticks(), ("La Nintendo 64 tenía un solo stick", -.2), ("alrededor de Link|fin", .5),
       ["En el remake, la cámara es libre"], "sticks", y=.70),
    ficha("Nintendo dice que los lugares", "Lugares remodelados", "Pensados para que la cámara *se mueva por ellos*.",
          tipo="Nintendo", a=("pueda moverse por ellos|fin", .6)),

    # ================================================================ 1 / EL SALTO
    puesto("Y el cambio número 1.", 1, "Link puede saltar"),
    dict(tipo="destello", en="Link puede saltar#2", dur=.45, fuerza=.55),
    ficha("Saltaba solo, al correr hacia un borde", "Nintendo 64", "Link saltaba *solo*, al correr hacia un borde.",
          tipo="1998", a=("evitaba muchas caídas|fin", .3)),
    *ventana("salto", ("En el remake hay un botón para saltar", -.2), ("cuando y donde tú quieras|fin", .8)),
    ficha("Así que la gran pregunta", "La gran pregunta", "¿Qué *atajos* van a aparecer en las mazmorras?",
          tipo="Lo veremos el 5 de noviembre", a=("para que nada se rompa|fin", .8)),

    # ================================================================ CIERRE
    mg(O.balance(["Remake fiel", "Controles modernos", "Voces", "Orquesta", "Botón de salto"],
                 ["Mazmorras nuevas", "Hyrule más grande", "Master Quest"]),
       ("Nintendo no ha confirmado mazmorras nuevas", -.2), ("un Link que por fin salta|fin", 1.0),
       ["Nintendo no ha confirmado mazmorras nuevas", "ni un campo de Hyrule más grande", "ni si vuelve Master Quest",
        "Lo confirmado es un remake fiel", ("controles modernos, voces", 0.0), ("controles modernos, voces", .9),
        ("voces, orquesta", .7), "y un Link que por fin salta"],
       "balance", y=.52),
    ficha("Ahora dime tú en los comentarios", "Tu turno", "¿Qué cambio te gusta *más*? ¿Y cuál *no debieron tocar*?",
          tipo="Comentarios", a=("cuál no debieron tocar|fin", .8)),
    peg("aquí tienes la historia de Ocarina of Time", "link_ocarina", "Ocarina of Time: historia y 12 secretos", tam=420,
        x=.20, y=.58, dur=5.0),
]
ROTULOS = []
SFX = {}        # el sonido original del juego (ambiente_por) da la vida; sin SFX añadidos
PISTAS = []
