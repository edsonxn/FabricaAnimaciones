# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Rare: el estudio que Nintendo DEJÓ IR» (SECUENCIA YT, Crónicas del gaming, 28-oct-2026).
Kit NUEVO `nucleo/mg_rare.py` con la estética del propio estudio (oro del logo de Rareware + teatro de Rare Replay) sobre humo
azul noche TRANSLÚCIDO (regla del 22-oct):
- `puesto` = cartel de CAPÍTULO con los años; `ficha` = humo azul con título oro que se escribe (citas y cifras).
- PEGATINAS reales de lo que nombra la voz (pegatinas/, fuentes en pegatinas/_fuentes.txt; bajar_pegatinas.py).
- MG NUEVOS de ESTE guion: `eras` (la vida del estudio en 7 hitos), `apuesta` (balanza: las SGI contra el trato con Nintendo),
  `acciones` (de quién es Rare: 100 casillas Stamper -> Nintendo 25/49 % -> Microsoft 100 % con el sello de 375 M), `torres`
  (ventas en cartuchos apilados: SNES y N64), `reparto` (el divorcio de 2002: cada personaje se va con su dueño) y `exodo`
  (la fuga de talento: flechas a Free Radical, los Stamper, Playtonic).
- Sin mapas: el guion no tiene geografía de un juego (regla: sin mapa real del juego, no hay mapa).
  python fab.py rare_auge_caida fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py rare_auge_caida fx         audio/fx.wav
"""
import os

import mg_rare as R

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_FX, _FY = .74, .42     # fichas: a la derecha (el cartel del capítulo va arriba)

CAMARA = {}
FUNDIDO = {}


def _img(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def _p(slug):
    """Ruta si existe, None si no (para los MG, que aguantan huecos)."""
    try:
        return _img(slug)
    except FileNotFoundError:
        return None


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=R.pegatina(_img(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(en, items, y=.66, tam=320, dur=5.0):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    paso = max(.17, (tam + 90) / 1920)
    return [peg(a or en, s, t, dur=dur, x=.12 + paso * i, y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY):
    d = dict(tipo="mg", fn=R.ficha(titulo, texto, tipo=tipo), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, años, dur=4.0):
    return dict(tipo="mg", fn=R.puesto(num, titulo, años), en=en, dur=dur, x=.5, y=.17, sale=.45, nombre=f"capítulo {num}",
                ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


_P = _p
FX = [
    # ================================================================ GANCHO
    grande("En septiembre de 2002", "nintendo_logo", "Nintendo", lado="der", dur=4.2, tam=520),
    *fila("Ese estudio había hecho", [("dkc", "Donkey Kong Country", "Donkey Kong Country"),
                                     ("goldeneye", "GoldenEye 007", "GoldenEye"),
                                     ("banjo_kazooie", "Banjo-Kazooie", "Banjo-Kazooie"),
                                     ("perfect_dark", "Perfect Dark", "Perfect Dark")], tam=300, dur=6.4),
    peg("Microsoft lo compró entero", "microsoft_logo", "Microsoft", tam=360, x=.80, y=.30, dur=4.4),
    ficha("Microsoft lo compró entero", "La compra", "*375 millones* de dólares, en efectivo.", tipo="24 de septiembre de 2002",
          a=("de los videojuegos|fin", .3), x=.27, y=.60),
    grande("porque el estudio se llamaba Rare", "rare_logo", "Rare", lado="der", dur=4.8, tam=560),
    mg(R.eras([("1982", "Ultimate Play the Game", _P("jetpac")), ("1985", "Rare y la NES", _P("nes")),
               ("1994", "Donkey Kong Country", _P("dkc")), ("1997", "GoldenEye 007", _P("goldeneye")),
               ("2002", "La compra de Microsoft", _P("microsoft_logo")), ("2010", "Kinect Sports", _P("kinect_sports")),
               ("2018", "Sea of Thieves", _P("sot"))], titulo="Rare, 1982 - 2026"),
       ("Hoy te cuento cómo dos hermanos", -.2), ("casi nadie vio venir|fin", .5),
       ["dos hermanos", "un pueblo inglés", "llegaron a la cima", "de Nintendo", "por qué cayeron", "qué les pasó",
        "este mismo año"], "eras", y=.66),

    # ================================================================ 1 / DOS HERMANOS Y UN SECRETO
    puesto("Capítulo 1.", 1, "Dos hermanos y un secreto", "1982 - 1985"),
    grande("Tim y Chris Stamper", "tim_stamper", "Tim y Chris Stamper", lado="izq", dur=6.4, tam=560),
    peg("Ultimate Play the Game", "atic_atac", "Ultimate Play the Game", tam=380, x=.80, y=.56, dur=3.8),
    peg("El primero, Jetpac", "jetpac", "Jetpac (1983)", tam=380, x=.80, y=.58),
    peg("para la computadora ZX Spectrum", "zx_spectrum", "ZX Spectrum", tam=360, x=.18, y=.64),
    ficha("Según la revista Retro Gamer", "Jetpac", "Más de *300 000 copias* y más de *un millón de libras*.",
          tipo="Según Retro Gamer", a=("más de un millón de libras|fin", .6)),
    peg("Después vino Atic Atac", "atic_atac", "Atic Atac (1983)", tam=360, x=.18, y=.64, dur=3.2),
    peg("Y en 1984, Sabre Wulf", "sabreman", "Sabreman", tam=300, x=.18, y=.30, dur=5.0),
    peg("Y en 1984, Sabre Wulf", "sabre_wulf", "Sabre Wulf (1984)", tam=380, x=.80, y=.58, dur=5.4),
    ficha("Cuando una revista les preguntó", "Ultimate", "«Eso no te lo *podemos decir*.»", tipo="A la revista CRASH, 1985",
          a=("eso no te lo podemos decir|fin", 1.0)),
    grande("Tim Stamper contó que Knight Lore", "knight_lore", "Knight Lore (1984)", lado="der", dur=6.0, tam=560),
    ficha("Eso sí. Años después", "Leyenda discutida", "Retro Gamer analizó el código: la historia es *probablemente "
          "exagerada*.", tipo="Knight Lore", a=("probablemente es exagerada|fin", .6), x=.27),
    peg("una consola japonesa estaba arrasando", "nes", "Famicom / NES", tam=420, x=.75, y=.55),

    # ================================================================ 2 / ABRIR LA CAJA DE NINTENDO
    puesto("Capítulo 2.", 2, "Abrir la caja de Nintendo", "1985 - 1993"),
    peg("registraron una empresa nueva, Rare Limited", "rare_logo", "Rare Limited (1985)", tam=360, x=.18, y=.64),
    ficha("Uno de sus trabajadores, Dave Thomas", "Dave Thomas", "«Era mandar valores a la memoria, *uno por uno*, hasta "
          "que pasara algo.»", tipo="Sobre la NES, a GamesTM", a=("hasta que pasara algo|fin", .8)),
    ficha("Entre 1987 y 1993", "Rare en la NES", "Unos *47 juegos* entre 1987 y 1993.", tipo="Para Nintendo, Tradewest "
          "y Milton Bradley", a=("y para Milton Bradley|fin", .4), x=.27),
    *fila("Ahí están R.C. Pro-Am", [("rc_pro_am", "R.C. Pro-Am", "R.C. Pro-Am"),
                                   ("snake_rattle", "Snake Rattle 'n' Roll", "Snake Rattle"),
                                   ("battletoads", "Battletoads (1991)", "Battletoads")], tam=320, dur=5.4),

    # ================================================================ 3 / LA APUESTA
    puesto("Capítulo 3.", 3, "La apuesta", "1993 - 1996"),
    peg("Silicon Graphics fabricaba", "sgi", "Silicon Graphics", tam=380, x=.80, y=.30, dur=4.4),
    peg("El compositor David Wise", "david_wise", "David Wise", tam=360, x=.18, y=.62, dur=6.0),
    mg(R.apuesta("La apuesta", ("Lo que arriesgaron", "Dos estaciones de unas 80 000 libras cada una", _P("sgi")),
                 ("Lo que ganaron", "Nintendo, convencida", _P("nintendo_logo"))),
       ("La idea era modelar personajes", -.2), ("quedaron convencidos|fin", .6),
       ["La idea era modelar", "quedaron convencidos"], "apuesta", y=.52),
    mg(R.acciones([("Hermanos Stamper", 100, R.AZUL, _P("rare_logo")), ("Nintendo, 1994", 25, R.ROJO, _P("nintendo_logo")),
                   ("Nintendo, después", 49, R.ROJO, _P("nintendo_logo"))]),
       ("En 1994, Nintendo compró", -.4), ("de 84 personas a 250|fin", .6),
       [("En 1994, Nintendo compró", -.3), "el 25 %", "subió al 49 %"], "acciones 1", y=.50),
    grande(("de sus personajes más famosos", 1.2), "donkey_kong", "Donkey Kong", lado="der", dur=4.4, tam=520),
    peg("Donkey Kong Country salió en noviembre", "dkc", "Donkey Kong Country (1994)", tam=400, x=.18, y=.62, dur=5.0),
    peg("Hay una leyenda de que a Shigeru Miyamoto", "miyamoto", "Shigeru Miyamoto", tam=380, x=.18, y=.62, dur=7.0),
    ficha("Él mismo la desmintió", "Shigeru Miyamoto", "Trabajó muy de cerca con Rare y se escribía *casi a diario* con "
          "Tim Stamper.", tipo="Entrevista, 2010", a=("casi a diario con Tim Stamper|fin", .6)),
    peg("Así nació Diddy Kong", "diddy", "Diddy Kong", tam=400, x=.80, y=.56),
    peg("Aquatic Ambience", "david_wise", "David Wise", tam=320, x=.18, y=.64, dur=4.6),
    mg(R.torres([("Donkey Kong Country", 9.3, _P("dkc")), ("Killer Instinct", 3.2, _P("ki")),
                 ("Donkey Kong Country 2", 5.15, _P("dkc2")), ("Donkey Kong Country 3", 3.51, _P("dkc3"))],
                titulo="Rare en Super Nintendo", unidad="millones de copias"),
       ("Después llegaron Killer Instinct", -.6), ("algo todavía más difícil|fin", .3),
       [("Después llegaron Killer Instinct", -.4), "Killer Instinct", "Donkey Kong Country 2", "Donkey Kong Country 3"],
       "torres SNES", y=.50),

    # ================================================================ 4 / EL JUEGO QUE NADIE ESPERABA
    puesto("Capítulo 4.", 4, "El juego que nadie esperaba", "1995 - 1997"),
    grande("la película de James Bond de 1995", "pierce_brosnan", "GoldenEye (1995)", lado="der", dur=4.6, tam=480),
    peg("El compositor Grant Kirkhope", "kirkhope", "Grant Kirkhope", tam=380, x=.80, y=.30, dur=6.4),
    ficha("probablemente eran 12 personas", "Grant Kirkhope", "Unas *12 personas*, y ninguno había hecho un juego antes.",
          tipo="Septiembre de 2026", a=("había hecho un juego antes|fin", .8), x=.27, y=.62),
    ficha("El modo multijugador lo programó", "El multijugador", "Steve Ellis lo programó en *un mes*, sin que la "
          "dirección lo supiera.", tipo="1997", a=("sin que la dirección lo supiera|fin", .8)),
    peg("Hasta Miyamoto opinó", "miyamoto", "Shigeru Miyamoto", tam=380, x=.18, y=.62, dur=6.2),
    ficha("Envió una sugerencia", "La idea de Miyamoto", "Que Bond visitara a sus enemigos *en el hospital*, y les diera "
          "la mano.", tipo="GoldenEye 007", a=("y les diera la mano|fin", .8)),
    ficha("en palabras de Kirkhope", "Lo que esperaba el equipo", "«Un *desastre total*.»", tipo="Grant Kirkhope",
          a=("un desastre total|fin", 1.0), x=.27),
    peg("GoldenEye 007 salió en agosto de 1997", "goldeneye", "GoldenEye 007 (1997)", tam=420, x=.80, y=.56, dur=5.0),
    ficha("Vendió unos 8 millones", "GoldenEye 007", "Unos *8 millones* de copias: el juego de James Bond *más vendido* "
          "de la historia.", tipo="Según Guinness", a=("más vendido de la historia|fin", .6), x=.27),
    peg("Era la gran estrella de la consola", "n64", "Nintendo 64", tam=420, x=.75, y=.55, dur=4.0),

    # ================================================================ 5 / LA FÁBRICA DE CLÁSICOS
    puesto("Capítulo 5.", 5, "La fábrica de clásicos", "1997 - 2001"),
    mg(R.torres([("GoldenEye 007", 8.09, _P("goldeneye")), ("Diddy Kong Racing", 4.88, _P("dkr")),
                 ("Banjo-Kazooie", 3.65, _P("banjo_kazooie")), ("Donkey Kong 64", 5.27, _P("dk64")),
                 ("Banjo-Tooie", 3.0, _P("banjo_tooie"))], titulo="Rare en Nintendo 64", unidad="millones de copias"),
       ("Lo que vino después parece una lista", -.3), ("Y aquí hay una curiosidad|fin", .3),
       [("Lo que vino después", -.1), "Diddy Kong Racing", ("En 1998, Banjo-Kazooie", .1)], "torres N64 a", y=.50),
    grande("un proyecto cancelado llamado Dream", "dream", "Edson, de Dream (cancelado)", lado="der", dur=5.0, tam=600),
    ficha("cuyo protagonista era un niño llamado Edson", "Dream", "El protagonista era un niño llamado *Edson*, con su "
          "perro Dinger y un loro.", tipo="El proyecto que se volvió Banjo", a=("y al final, por un oso|fin", .8), x=.27, y=.40),
    peg("y al final, por un oso", "banjo", "Banjo", tam=420, x=.78, y=.58, dur=4.4),
    *fila("Banjo-Kazooie vendió más de 3,6 millones", [("banjo_kazooie", "Banjo-Kazooie (1998)", None),
                                                      ("banjo_tooie", "Banjo-Tooie (2000)", "y Banjo-Tooie")], tam=340, dur=6.0),
    *fila("Entre medias llegaron Jet Force Gemini", [("jfg", "Jet Force Gemini (1999)", None),
                                                    ("dk64", "Donkey Kong 64 (1999)", "y Donkey Kong 64")], tam=340, dur=6.0),
    grande("necesitaba el Expansion Pak", "expansion_pak", "Expansion Pak", lado="der", dur=4.6, tam=460),
    ficha("Unos dicen que fue para esquivar", "Dato discutido", "¿Un error que colgaba el juego? ¿O la *iluminación*, "
          "desde el principio?", tipo="El Expansion Pak de Donkey Kong 64", a=("para la iluminación|fin", .6), x=.27),
    peg("también traía el DK Rap", "kirkhope", "Grant Kirkhope", tam=360, x=.80, y=.30, dur=5.6),
    peg("En el año 2000 llegó Perfect Dark", "joanna", "Joanna Dark", tam=440, x=.78, y=.56, dur=5.0),
    peg("Martin Hollis había dejado el proyecto", "perfect_dark", "Perfect Dark (2000)", tam=360, x=.18, y=.62, dur=4.4),
    peg("fundaron su propio estudio, Free Radical", "free_radical", "Free Radical", tam=380, x=.80, y=.30, dur=4.4),
    peg("sacaron TimeSplitters", "timesplitters2", "TimeSplitters", tam=360, x=.18, y=.62, dur=4.0),
    grande("Conker.", "conker_personaje", "Conker", lado="der", dur=4.0, tam=520),
    peg("Así que Rare lo convirtió", "conker", "Conker's Bad Fur Day (2001)", tam=420, x=.80, y=.56, dur=5.4),
    ficha("Hasta hubo una gira de torneos", "Conker's Bad Fur Day", "Una gira de torneos por *20 universidades*, "
          "organizada por Playboy.", tipo="2001", a=("organizada por Playboy|fin", .6), x=.27, y=.40),
    peg("Su socio ya no la miraba igual", "nintendo_logo", "Nintendo", tam=380, x=.75, y=.55, dur=3.8),

    # ================================================================ 6 / EL DIVORCIO
    puesto("Capítulo 6.", 6, "El divorcio", "2002"),
    peg("llamado Dinosaur Planet", "n64", "Nintendo 64", tam=340, x=.18, y=.62, dur=4.0),
    grande("nació Star Fox Adventures", "sfa", "Star Fox Adventures (2002)", lado="der", dur=5.0, tam=520),
    peg("Y fue el último juego de Rare para Nintendo", "gamecube", "Nintendo GameCube", tam=340, x=.18, y=.64, dur=3.6),
    mg(R.acciones([("Hermanos Stamper", 100, R.AZUL, _P("rare_logo")), ("Nintendo", 49, R.ROJO, _P("nintendo_logo")),
                   ("Microsoft", 100, R.VERDE, _P("microsoft_logo"))], titulo="¿De quién es Rare?",
                  precio=("375 M US$", "24 de septiembre de 2002")),
       ("Porque al día siguiente", -.2), ("el 51 % que le faltaba|fin", .5),
       [("Porque al día siguiente", .0), ("Porque al día siguiente", .4), "Microsoft anunció que había comprado",
        "Por 375 millones"], "acciones 2", y=.50),
    peg("Peter MacDougall, de Nintendo of America", "nintendo_logo", "Nintendo of America", tam=320, x=.18, y=.64, dur=5.0),
    ficha("Peter MacDougall, de Nintendo of America", "Peter MacDougall", "«El valor de Rare para el futuro de Nintendo "
          "sería *limitado*.»", tipo="Nintendo of America, 2002", a=("sería limitado|fin", .6)),
    ficha("Y dio un dato", "Año fiscal 2002", "Rare aportó solo el *1,5 %* de las ventas de software de Nintendo.",
          tipo="Según Nintendo of America", a=("software de Nintendo|fin", .8), x=.27),
    peg("Tim Stamper lo vio de otra forma", "tim_stamper", "Tim y Chris Stamper", tam=400, x=.80, y=.56, dur=6.0),
    peg("Según Ed Fries", "ed_fries", "Ed Fries", tam=380, x=.18, y=.62, dur=8.0),
    ficha("Activision llegó a ir ganando la puja", "La puja", "*Activision* llegó a ir ganando. Nintendo podía igualar "
          "cualquier oferta, y no lo hizo.", tipo="Según Ed Fries", a=("Microsoft subió la suya al final|fin", .6)),
    mg(R.reparto(("Nintendo", _P("nintendo_logo"), R.ROJO), ("Rare / Microsoft", _P("microsoft_logo"), R.VERDE),
                 [("Donkey Kong", _P("donkey_kong"), "i"), ("Banjo", _P("banjo"), "d"), ("Diddy Kong", _P("diddy"), "i"),
                  ("Conker", _P("conker_personaje"), "d"), ("Fox McCloud", _P("fox"), "i"), ("Joanna Dark", _P("joanna"), "d")],
                 titulo="El reparto"),
       ("Pero todo divorcio tiene un reparto", -.2), ("la había hecho famosa|fin", .6),
       ["Donkey Kong, Diddy", "Banjo, Conker", "Diddy y Star Fox", "Conker y Joanna", "Star Fox se quedaron",
        "Joanna Dark se fueron"], "reparto", y=.52),

    # ================================================================ 7 / LA CAÍDA
    puesto("Capítulo 7.", 7, "La caída", "2003 - 2014"),
    peg("Grabbed by the Ghoulies, en 2003", "ghoulies", "Grabbed by the Ghoulies (2003)", tam=400, x=.80, y=.56, dur=5.0),
    peg("lanzamiento de Xbox 360", "x360", "Xbox 360", tam=360, x=.80, y=.30, dur=4.0),
    *fila("Kameo, y Perfect Dark Zero", [("kameo", "Kameo (2005)", "Kameo"), ("pdz", "Perfect Dark Zero (2005)", "Perfect Dark Zero")],
         tam=340, dur=5.4),
    ficha("Los dos equipos admitieron", "Kameo y Perfect Dark Zero", "Les habrían venido bien *seis meses más*.",
          tipo="Según Rare, 2010", a=("seis meses más|fin", .8)),
    grande("En 2006 llegó Viva Piñata", "viva", "Viva Piñata (2006)", lado="der", dur=6.0, tam=520),
    ficha("Pero casi un año después de salir", "Viva Piñata", "Unas *500 000 copias* casi un año después.",
          tipo="Ventas", a=("unas 500 000 copias|fin", .8), x=.27),
    peg("Tim y Chris Stamper dejaron Rare", "tim_stamper", "Tim y Chris Stamper", tam=420, x=.20, y=.60, dur=5.6),
    ficha("Tim y Chris Stamper dejaron Rare", "2 de enero de 2007", "Los hermanos Stamper *dejan Rare*.",
          tipo="Fin de una era", a=("a otros proyectos|fin", .6)),
    grande("En 2008 volvió Banjo", "nuts_bolts", "Nuts and Bolts (2008)", lado="der", dur=6.4, tam=520),
    peg("Gregg Mayles, el creador de Banjo", "banjo", "Banjo", tam=380, x=.18, y=.62, dur=6.0),
    ficha("Vendió 140 000 copias", "Nuts and Bolts", "*140 000 copias* en su primer mes en Estados Unidos.",
          tipo="Ventas", a=("primer mes|fin", .6)),
    peg("Los avatares de Xbox 360", "avatars", "Avatares de Xbox 360", tam=420, x=.80, y=.56, dur=4.6),
    peg("Y en 2010, Kinect Sports", "kinect_sports", "Kinect Sports (2010)", tam=400, x=.18, y=.62, dur=5.0),
    peg("para la cámara de movimiento de Microsoft", "kinect", "Kinect", tam=360, x=.80, y=.30, dur=4.0),
    mg(R.exodo(("Rare", _P("rare_logo")), [("Free Radical", "1999", _P("timesplitters2"), "TimeSplitters"),
                                         ("Los Stamper", "2007", _P("tim_stamper"), "Dejan Rare"),
                                         ("Playtonic", "2015", _P("yooka"), "Yooka-Laylee")], titulo="La fuga de talento"),
       ("Y la gente que había hecho los clásicos", -.2), ("Yooka-Laylee.|fin", .4),
       ["Unos treinta empleados", "Y muchos más", "Playtonic"], "éxodo", y=.50),
    ficha("Pedían 175 000 libras", "Kickstarter de Yooka-Laylee", "Meta de *175 000 libras* en unos 40 minutos. Al "
          "final, más de *2 millones*.", tipo="Mayo de 2015", a=("un récord en el Reino Unido|fin", .6)),

    # ================================================================ 8 / UN BARCO PIRATA
    puesto("Capítulo 8.", 8, "Un barco pirata", "2015 - 2026"),
    grande("Rare sacó Rare Replay", "rare_replay", "Rare Replay (2015)", lado="der", dur=6.0, tam=480),
    ficha("30 juegos de su historia", "Rare Replay", "*30 juegos* por *30 dólares*, con más de una hora de documentales.",
          tipo="Agosto de 2015", a=("una hora de documentales|fin", .6), x=.27),
    grande("Sea of Thieves.", "sot", "Sea of Thieves (2018)", lado="izq", dur=5.0, tam=520),
    ficha("En abril de 2024, Rare dijo", "Sea of Thieves", "*40 millones* de jugadores, contando Game Pass.",
          tipo="Abril de 2024", a=("contando Game Pass|fin", .8)),
    ficha("Y ese mismo mes llegó a PlayStation 5", "PlayStation 5", "El juego *más descargado* de PS5 en Europa en abril "
          "de 2024.", tipo="Salió el 30 de abril", a=("el último día del mes|fin", .6), x=.27),
    peg("otro juego nuevo, Everwild", "everwild", "Everwild", tam=420, x=.80, y=.56, dur=5.6),
    ficha("Everwild fue cancelado", "Everwild", "*Cancelado* el 2 de julio de 2025.", tipo="Despidos de Microsoft",
          a=("Everwild fue cancelado|fin", 1.4), x=.27),
    *fila("Y en octubre de 2025, Gregg Mayles", [("dkc", "Donkey Kong Country", None), ("banjo_kazooie", "Banjo-Kazooie", None)],
         tam=320, dur=6.4),
    ficha("Xbox anunció unos 3 200 despidos", "Julio de 2026", "Unos *3 200 despidos* y cinco estudios fuera. Rare *no* "
          "estaba entre ellos.", tipo="Xbox", a=("Rare no estaba entre ellos|fin", 1.0)),

    # ================================================================ CIERRE
    ficha("llegó un memorando de Matt Booty", "22 de septiembre de 2026", "«Activision ampliará su responsabilidad... "
          "*también a Rare*.»", tipo="Memorando de Matt Booty, Xbox", a=("También a Rare|fin", 1.4), x=.5, y=.40),
    peg("Activision. La misma empresa", "activision_logo", "Activision", tam=440, x=.24, y=.66, dur=5.4),
    *fila("Rare sigue en Twycross", [("rare_logo", "Rare", None), ("sot", "Sea of Thieves", None)], tam=340, dur=5.6),
    peg("aquí tienes la historia de Banjo-Tooie", "banjo_tooie", "Banjo-Tooie", tam=420, x=.75, y=.50, dur=5.0),
]
ROTULOS = []
SFX = {}
PISTAS = []
