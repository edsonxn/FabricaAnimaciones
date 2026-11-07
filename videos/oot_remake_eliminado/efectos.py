# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Lo que Nintendo ELIMINÓ del REMAKE de Ocarina of Time» (SECUENCIA YT, Crónicas del gaming, 7-nov-2026).
Kit de oot_remake_cambios (todo TRANSLÚCIDO, regla del 22-oct) + regla de oro (tes_secretos_40):
- `puesto` = cartel «Eliminado número N» y `ficha` = cuadro de diálogo de N64 (mg_majora: el mismo motor de Ocarina).
- VENTANA DEL ORIGINAL (medios/n64/, bajar_ventanas.py) con marco N64 + etiqueta SWITCH 2 cada vez que se compara.
- PEGATINAS reales (pegatinas/_fuentes.txt), variadas: pv() rota marco/entrada/salida (peg_anim), y estilos de peg_estilos
  (silueta, reliquia, camafeo, legajo, abanico) en ~1 de cada 3.
- MG NUEVOS de ESTE guion (nucleo/mg_oot.py, 7-nov): lista_negra (gancho tachado), contador Metacritic 96 -> 99,
  ranuras 3 -> 1, ofrendas 25/50/500, contador del puente 60 -> 0, sangre roja -> verde -> nada, linea_tiempo de Master Quest,
  balance «se quitó / se añadió».
- SONIDO ORIGINAL del juego en 12 beats (guion.SECUENCIA["ambiente_por"]); sin SFX añadidos.
  python fab.py oot_remake_eliminado fx hoja    previews/fx_NN.jpg (MÍRALA)
"""
import os

import mg_majora as M
import mg_oot as O
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_N64 = os.path.join(_AQUI, "medios", "n64")
_FX, _FY = .74, .40     # fichas: a la derecha (el cartel del puesto va arriba)
_VW, _VX, _VY = 576, .79, .69
_VH = round(_VW / 1.312)
TEMA = "n64"

CAMARA = {}
FUNDIDO = {}


def _img(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


_P = _img


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    """Pegatina con la siguiente combinación del rotador (marco + entrada + estancia + salida, nunca dos iguales seguidas)."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_img(slug), titulo, tam, tema=TEMA, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return pv(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def filav(en, items, y=.66, tam=300, dur=4.6):
    xs = (.12, .28, .44, .60, .76)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=860, encuadre=(0, .62)):
    fn = PE.silueta(_img(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=480):
    return dict(tipo="mg", fn=PE.reliquia(_img(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .25, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(_img(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(_img(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=290):
    return dict(tipo="mg", fn=PE.abanico([(_img(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + nombre, ver=2.0)


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY):
    d = dict(tipo="mg", fn=M.ficha(titulo, texto, tipo=tipo), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, num, titulo, dur=3.8):
    return dict(tipo="mg", fn=M.puesto(num, titulo, arriba=f"Eliminado número {num}"), en=en, dur=dur, x=.5, y=.17, sale=.45,
                nombre=f"puesto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def ventana(slug, de, a, desde=0.0, año="1998", sw2=True):
    """El ORIGINAL de N64 en una ventana (FX video) con su marco + la etiqueta SWITCH 2 sobre el cuadro grande.
    sw2=False cuando el cuadro grande TAMBIÉN es de N64 (la ventana es un detalle, no una comparación)."""
    ruta = os.path.join(_N64, slug + ".mp4")
    fx = [dict(tipo="video", de=de, a=a, ruta=ruta, desde=desde, x=_VX, y=_VY, ancho=_VW, entra=.35, sale=.35,
               nombre="ventana " + slug),
          dict(tipo="mg", fn=O.marco(_VW, _VH, año), de=de, a=a, x=_VX, y=_VY - 25 / 1080, sale=.35,
               nombre="marco " + slug, ver=2.0)]
    if sw2:
        fx.append(dict(tipo="mg", fn=O.etiqueta("SWITCH 2", "2026"), de=de, a=a, x=.12, y=.09, sale=.35,
                       nombre="etiqueta sw2", ver=1.0))
    return fx


FX = [
    # ================================================================ GANCHO (MG desde el primer segundo)
    pv("te asomabas por la ventana del patio", "zelda_nina", "La princesa Zelda", tam=340, x=.82, y=.30, dur=3.6),
    aba([("mario", "Mario"), ("peach", "Peach"), ("bowser", "Bowser")], ("veías cuadros de Mario", -.2),
        ("de Peach y de Bowser|fin", 1.2), ["cuadros de Mario", "de Peach", "y de Bowser"], "cuadros 1998", x=.30, y=.64),
    *ventana("retratos", ("esos cuadros ya no están", -.4), ("Y Nintendo explicó por qué|fin", .5)),
    cam("Y Nintendo explicó por qué", "aonuma", "Eiji Aonuma", x=.16, y=.62, dur=3.4),
    mg(O.lista_negra([("Granja de rupias", _P("rupia_roja")), ("Master Quest", _P("mq_logo")), ("Glitches famosos", _P("n64")),
                      ("Escena de Ganondorf", _P("ganondorf"))]),
       ("Una granja de rupias", -.3), ("una escena de Ganondorf|fin", 1.4),
       ["Una granja de rupias", "Master Quest", "glitches famosos", "una escena de Ganondorf"], "lista negra", y=.48),
    ficha("Así que hoy te cuento", "Ocarina of Time (Switch 2)", "*12 cosas* que Nintendo quitó del remake, de la más pequeña "
          "a la más *polémica*.", tipo="Lo eliminado", a=("a la que más está dando que hablar|fin", .5)),

    # ================================================================ CONTEXTO
    pv("solo en Nintendo Switch 2", "switch2", "Nintendo Switch 2", tam=300, x=.84, y=.28, dur=4.0),
    ficha("En México cuesta", "El remake", "*5 de noviembre*. Solo Switch 2. *1229 pesos* en digital (México).",
          tipo="Lanzamiento", a=("en versión digital|fin", .6), x=.27),
    ficha("Lo hizo el mismo equipo", "Rehecho desde cero", "El equipo de *Breath of the Wild* y *Tears of the Kingdom*. "
          "No es el código de 1998.", tipo="Desarrollo", a=("gráficos nuevos|fin", .4)),
    mg(O.contador(96, 99, "Metacritic", sub_antes="Switch 2 (2026)", sub_despues="Nintendo 64 (1998)"),
       ("Ya tiene un 96 en Metacritic", -.2), ("sigue arriba, con un 99|fin", .9), ["El original de Nintendo 64"], "metacritic",
       y=.40),
    pv("El original de Nintendo 64", "n64", "Nintendo 64 (1998)", tam=300, x=.16, y=.66, dur=3.4),
    leg("aonuma", "Eiji Aonuma", ["Pidió teletransporte por todo Hyrule", "Luego mandó quitarlo"],
        ("lo eliminó el propio Eiji Aonuma", -.2), ("lo que hay en el camino|fin", .6),
        marcas=["Pidió añadir puntos", "mandó quitarlos todos"], sello=("ELIMINADO", 1), x=.21, y=.50),
    ficha("Según él, al final no le convencían", "Eiji Aonuma", "«Si viajas de un salto, te saltas *lo que hay en el "
          "camino*.»", tipo="Productor de la saga", a=("lo que hay en el camino|fin", .6)),

    # ================================================================ 12 / LA 3DS
    puesto("Número 12.", 12, "Un guiño de la Nintendo 3DS"),
    pv("solo existía en la Nintendo 3DS", "n3ds", "Nintendo 3DS (2011)", tam=340, x=.82, y=.62, dur=4.0),
    ficha("En el Ocarina of Time 3D de 2011", "Ocarina of Time 3D", "Cuadros de *Skyward Sword* en el *Rancho Lon Lon* y la "
          "*Fortaleza Gerudo*.", tipo="Nintendo 3DS", a=("y en la Fortaleza Gerudo|fin", .5)),
    pv("en el Rancho Lon Lon", "malon", "Malon (Rancho Lon Lon)", tam=320, x=.16, y=.64, dur=3.6),
    cam("Hidemaro Fujibayashi contestó", "fujibayashi", "Hidemaro Fujibayashi", x=.18, y=.62, dur=4.2, tam=320),
    ficha("Hidemaro Fujibayashi contestó", "Hidemaro Fujibayashi", "¿Enojo en el equipo de la 3DS? *No hay rencor.*",
          tipo="Director del remake", a=("no había rencor|fin", .5)),

    # ================================================================ 11 / LA LUPA
    puesto("En el 11, la Lupa", 11, "La Lupa de la Verdad"),
    rel("era una lupa con un ojo dibujado", "lupa", "Lupa de la Verdad", "Nintendo 64", x=.78, y=.48, tam=440),
    pv("del fondo del pozo de Kakariko", "link_nino", "Link niño", tam=300, x=.16, y=.66, dur=3.4),
    *ventana("lupa", ("Son unas gafas que Link se pone", -.3), ("su nuevo aspecto|fin", .2)),
    ficha("Son unas gafas que Link se pone", "Gafas de la Verdad", "Link se las *pone en la cara*; el ojo se *abre y se "
          "cierra*.", tipo="Switch 2", a=("se abre y se cierra|fin", .3), x=.27, y=.36),
    ficha("hasta le comentan a Link su nuevo aspecto", "Según los jugadores", "Algunos personajes *comentan* el nuevo "
          "look de Link.", tipo="Detalle", a=("su nuevo aspecto|fin", .5), x=.27, y=.36),

    # ================================================================ 10 / KAEPORA
    puesto("Número 10.", 10, "El búho que no se callaba"),
    sil("Kaepora Gaebora te soltaba", "kaepora", "Kaepora Gaebora", "El búho sabio", lado="izq", dur=5.4, encuadre=(0, .75)),
    ficha("Si el cursor quedaba en no", "¿Lo entendiste?", "*No* + botón rápido = el *discurso entero* otra vez.",
          tipo="Nintendo 64", a=("desde el principio|fin", .5)),
    *ventana("kaepora", ("Fujibayashi contó que reescribieron", -.3), ("hoy no se entienden bien|fin", .8)),
    ficha("Fujibayashi contó que reescribieron", "Switch 2", "Apariciones *más cortas* y *sin pregunta*.",
          tipo="Kaepora Gaebora", a=("hoy no se entienden bien|fin", .8), x=.27, y=.36),

    # ================================================================ 9 / SECRETOS A CIEGAS
    puesto("En el 9, se acabó buscar", 9, "Secretos a ciegas"),
    rel("la Piedra de la Agonía", "piedra_agonia", "Piedra de la Agonía", "Vibraba con el Rumble Pak", x=.78, y=.50, tam=440),
    pv("con una bomba en un sitio", "bomba", "Bomba", tam=260, x=.16, y=.66, dur=3.2),
    rel("solo reacciona a las Skulltulas doradas", "skulltula_dorada", "Skulltula dorada", "El broche las detecta", x=.80, y=.55, tam=420),
    ficha("se marcan con flores en el suelo", "Grutas escondidas", "Ahora se marcan con *flores en el suelo*.",
          tipo="Switch 2", a=("Fujibayashi lo explicó así|fin", .2), x=.27, y=.36),
    ficha("Querían que el jugador pudiera deducir", "Hidemaro Fujibayashi", "Deducir qué hacer *dentro del juego*, sin una "
          "*guía al lado*.", tipo="Director del remake", a=("sin una guía al lado|fin", .5)),
    pv("la canción de Saria", "saria", "Saria", tam=320, x=.16, y=.62, dur=4.0),
    ficha("El tronco correcto brilla en verde", "Bosque Perdido", "El tronco correcto *brilla en verde*: ya no se sigue la "
          "canción de oído.", tipo="Según Eurogamer", a=("brilla en verde|fin", 1.0), x=.70, y=.36),

    # ================================================================ 8 / NAVI
    puesto("Número 8.", 8, "¡Hey, escucha!, mucho menos"),
    grande("Navi te interrumpía con esto", "navi", "Navi", lado="der", dur=4.4, tam=460),
    ficha("casi siempre te avisa con un sonido suave", "Navi (Switch 2)", "Un *sonido suave* al explorar y pistas de *hadas* "
          "repartidas.", tipo="En el remake", a=("repartidas por el escenario|fin", .5)),
    ficha("En inglés tiene voz nueva", "Voz nueva", "*Lisa Reimold* pone la voz de Navi en inglés.", tipo="Doblaje",
          a=("Lisa Reimold|fin", .6), x=.27, y=.36),
    ficha("Y el director, HokWai Ng", "HokWai Ng", "«Algo tan icónico como el *Hey, listen* no lo queríamos tocar.»",
          tipo="Director", a=("no lo querían tocar|fin", .6)),
    pv("Así que la frase sigue ahí", "navi", "Hey! Listen!", tam=300, x=.16, y=.66, dur=3.6),

    # ================================================================ 7 / LAS GRANDES HADAS
    puesto("En el 7, las Grandes Hadas", 7, "Las Grandes Hadas cobran"),
    sil("tocabas la canción de Zelda", "gran_hada", "Gran Hada", "Nintendo 64", lado="izq", dur=4.4, encuadre=(0, .7)),
    mg(O.ofrendas([("Montaña de la Muerte", 25), ("Castillo de Hyrule", 50), ("Castillo de Ganon", 500)], _P("rupia")),
       ("ahora cada Gran Hada pide una ofrenda", -.2), ("junto al castillo de Ganon|fin", 1.0),
       ["25 la de la Montaña", "50 la del castillo", "y 500 la que está"], "ofrendas", y=.40),
    ficha("Fujibayashi dice que es una forma de reverencia", "Hidemaro Fujibayashi", "Como las *donaciones en los templos* "
          "de Japón.", tipo="La explicación", a=("Una reverencia de 500 rupias|fin", .4)),
    ficha("La clasificación del remake", "Clasificación", "Ya no avisa de *temas sugerentes* (la de 3DS sí, por la ropa de "
          "las hadas).", tipo="Switch 2", a=("por la ropa de las hadas|fin", .4), x=.27, y=.36),

    # ================================================================ 6 / UNA PARTIDA
    puesto("Número 6.", 6, "Solo una partida"),
    mg(O.ranuras(("Tú", "Tu hermano", "Tu primo")), ("tres archivos de guardado", -.6), ("con guardado automático|fin", .8),
       ["En el remake hay una sola ranura"], "ranuras", y=.48),
    ficha("Y si quieres empezar de cero", "Empezar de cero", "Borra la partida que tenías.", tipo="Switch 2",
          a=("pierdes la partida que tenías|fin", .5)),
    pv("si compartes la consola", "switch2", "Una consola, una partida", tam=300, x=.18, y=.64, dur=4.0),

    # ================================================================ 5 / GLITCHES
    puesto("En el 5, adiós a los glitches", 5, "Adiós a los glitches"),
    *filav("La espada infinita", [("espada_kokiri", "Espada infinita", None),
                                  ("link_nino", "Atravesar paredes", "atravesar paredes"),
                                  ("mido", "Escapar sin espada", "escapar del Bosque Kokiri")], dur=4.6, tam=270),
    grande("inclinaba el cartucho", "n64", "Cartucho inclinado", lado="der", dur=4.6, tam=480),
    ficha("ninguno de esos trucos funciona", "Según los jugadores", "Rehecho desde cero: *ningún truco* de la N64 funciona.",
          tipo="Switch 2", a=("sin un solo glitch|fin", .3)),
    ficha("ya están apareciendo trucos nuevos", "Speedrunners", "Un día después del estreno ya hay *trucos nuevos* para ir "
          "más rápido.", tipo="Lo que viene", a=("no descansan|fin", .5), x=.27, y=.36),

    # ================================================================ 4 / EL PUENTE
    puesto("Número 4.", 4, "La granja de rupias del puente"),
    *filav("tres rupias rojas", [("rupia_roja", "20", None), ("rupia_roja", "20", ("tres rupias rojas", .5)),
                                 ("rupia_roja", "20", ("tres rupias rojas", 1.0))], y=.64, tam=230, dur=4.6),
    mg(O.contador(60, 0, "Rupias del puente", _P("rupia_roja")), ("60 rupias gratis", -.2), ("ya no existen|fin", .8),
       ["y las rupias ya no existen"], "contador puente", y=.40),
    # clip 047 = el puente levadizo del remake con sus cadenas (cinemáticas L45cq1H2d1s 2251 s); la ventana, el N64 trepando
    *ventana("puente", ("En el remake, Link resbala", -.1), ("Nintendo no lo ha explicado|fin", .4)),
    pv("una bolsa de 200 rupias", "bolsa_adulto", "Bolsa de 200 rupias", tam=320, x=.16, y=.62, dur=4.0),

    # ================================================================ 3 / MASTER QUEST
    puesto("En el 3, Master Quest", 3, "Master Quest"),
    mg(O.linea_tiempo([("1998", "Ocarina of Time (N64)", _P("n64")), ("2003", "Master Quest en GameCube", _P("gamecube")),
                       ("2011", "3DS: incluido", _P("n3ds")), ("2026", "Switch 2: no está", _P("switch2"))],
                      titulo="Master Quest"),
       ("Master Quest era la otra versión", -.2), ("no desbloquea nada|fin", .5),
       [("Master Quest era la otra versión", .1), "Salió en GameCube en 2003", "En la versión de 3DS venía incluida",
        "En el remake no hay Master Quest"], "línea master quest", y=.70),
    pv("con las mazmorras rehechas", "mq_logo", "Master Quest", tam=340, x=.82, y=.30, dur=4.2),
    leg("aonuma", "A IGN", ["«No creo que anunciemos", "nada específico por ahora»"],
        ("Cuando IGN le preguntó a Aonuma", -.2), ("es un tal vez|fin", .5),
        marcas=["no creía que fueran", "es un tal vez"], sello=("TAL VEZ", 1), x=.22, y=.48),

    # ================================================================ 2 / GANONDORF
    puesto("Número 2.", 2, "La escena de Ganondorf"),
    sil("después de vencer a Ganondorf", "ganondorf", "Ganondorf", "El Rey Demonio", lado="izq", dur=3.2, encuadre=(0, .6)),
    mg(O.sangre([("1998", "Versión 1.0", (200, 20, 20)), ("1998", "Versión 1.2", (60, 170, 60)),
                 ("2011", "Nintendo 3DS", (60, 170, 60)), ("2026", "Switch 2", None)]),
       ("escupía sangre roja", -.6), ("ese momento no está|fin", .8),
       ["escupía sangre roja", "la sangre pasó a ser verde", "La de 3DS la dejó verde", "ese momento no está"], "sangre",
       y=.26),
    *ventana("ganon", ("escupía sangre roja", -.4), ("la sangre pasó a ser verde|fin", .4), sw2=False),
    ficha("Ganondorf cae de rodillas", "Ganondorf (remake)", "«I, the mighty *Ganondorf*, the Demon King! *Defeated*?!»",
          tipo="Voz nueva en inglés", a=("Yo, el poderoso Ganondorf", -.1), x=.27, y=.30),
    ficha("Nintendo no ha comentado nada", "Sin explicación", "Es el cambio del que *más se habla* en redes desde el estreno.",
          tipo="Nintendo no comenta", a=("desde el estreno|fin", .4)),

    # ================================================================ 1 / LOS CUADROS DE MARIO
    puesto("Y lo número 1.", 1, "Los cuadros de Mario"),
    dict(tipo="destello", en="Los cuadros de Mario", dur=.45, fuerza=.5),
    aba([("mario", "Mario"), ("luigi", "Luigi"), ("peach", "Peach"), ("bowser", "Bowser"), ("yoshi", "Yoshi")],
        ("veías cuadros de Mario, Luigi", -.2), ("Bowser y Yoshi|fin", 1.0),
        ["cuadros de Mario", "Luigi", "Peach", "Bowser", "y Yoshi"], "cuadros 1", x=.34, y=.62),
    *ventana("guardia", ("si le disparabas a la ventana", -.3), ("te lanzaba una bomba|fin", .5), sw2=False),
    pv("con la resortera", "tirachinas", "Resortera", tam=260, x=.14, y=.66, dur=3.0),
    pv("te lanzaba una bomba", "bomba", "¡Bomba!", tam=260, x=.16, y=.40, dur=2.6),
    grande("hay un tapiz que se va bordando", "tapiz", "El tapiz", lado="izq", dur=4.8, tam=560),
    leg("aonuma", "Game Informer", ["No querían interrumpir", "la experiencia del mundo"],
        ("Aonuma lo explicó en Game Informer", -.2), ("y por qué está Yoshi aquí|fin", .3),
        marcas=["No querían que ese momento", "y por qué está Yoshi aquí"], sello=("¿YOSHI?", 1), x=.22, y=.48),
    pv("y por qué está Yoshi aquí", "yoshi", "¿Yoshi?", tam=320, x=.80, y=.30, dur=3.2),
    ficha("El guardia de la bomba sigue en su sitio", "Se quedó", "El *guardia de la bomba* sigue en su sitio.",
          tipo="Según los jugadores", a=("sigue en su sitio|fin", .5), x=.27, y=.36),
    grande("el broche de Bowser que lleva Talon", "talon", "Talon", lado="der", dur=4.4, tam=480),
    pv("el broche de Bowser", "bowser", "El broche de Bowser", tam=240, x=.14, y=.66, dur=3.6),

    # ================================================================ CIERRE
    mg(O.balance(["Voces", "Orquesta", "El tapiz", "Coliseo de jefes"], ["Guiños", "Atajos", "Secretos"],
                 titulos=("SE QUITÓ", "SE AÑADIÓ"), cruz=True),
       ("el remake quita guiños", -.3), ("pelear otra vez con los jefes|fin", 1.0),
       ["quita guiños", ("guiños, atajos", .4), "y secretos", "trae voces", "orquesta", "el tapiz", "y un coliseo"], "balance",
       y=.50),
    ficha("Ahora te pregunto a ti", "Tu turno", "De estas *12 cosas*, ¿cuál vas a *extrañar más*?", tipo="Comentarios",
          a=("Te leo en los comentarios|fin", .6)),
    grande("aquí tienes los 15 cambios", "video_cambios", "Los 15 cambios del remake", lado="der", dur=6.0, tam=560),
]
ROTULOS = []
SFX = {}        # el sonido original del juego (ambiente_por) da la vida; sin SFX añadidos
PISTAS = []
