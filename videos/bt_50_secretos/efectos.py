# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 50 SECRETOS de Banjo-Tooie QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming, 3-nov-2026).
Kit TRANSLÚCIDO nucleo/mg_banjo.py + pegatinas reales (wiki de Banjo, Commons) en estilos variados (nucleo/peg_estilos.py, tema gaming).
- Cada secreto: `secreto` (rótulo con el Jiggy real, ~4 s) + `contador` «N/50» en la esquina todo el secreto (son «aviso», no cuentan)
  + `donde` (tira baja con el mundo/personaje) + pegatinas + MG del kit, nuevos de ESTE guion: versus, concurso, antipirata, huesos,
  cronometro, fechas, jinjos_color, rotulos, memoria, compas; y del kit anterior cadena y puesto.
- MAPAS REALES de la Guía oficial de Nintendo (mapas/_coordenadas.md) donde la voz dice dónde; tema `gaming`.
- REGLA DE ORO (30-oct): las reglas suman; lo que dice la voz se ve; MG desde el gancho; pegatinas variadas; comentarios reales.
- SFX DEL JUEGO (regla del 29-oct): sfx/bt_*.mp3.
  python fab.py bt_50_secretos fx --seco | fx hoja | fx
"""
import os

import mg_banjo as B
import mg_mapa as MP
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .42     # fichas: a la derecha (el rótulo de secreto va arriba)
TEMA = "gaming"
JIGGY = os.path.join(_PEG, "jiggy.png")

CAMARA = {}
FUNDIDO = {}


def P(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


# ------------------------------------------------------------------ pegatinas (estilos variados)
def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-6.0):
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam, giro), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return peg(en, slug, titulo, dur=dur, x=.27 if lado == "izq" else .73, y=.53, tam=tam, giro=-3.0 if lado == "izq" else 3.0)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=800, encuadre=(0, 1.0)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con el video corriendo detrás."""
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.6, x=.26, y=.54, tam=540):
    """Objeto sobre el círculo."""
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .45, 1.4), dur=4.5, y=.72, lado="der"):
    """Tira de cine a todo lo ancho."""
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.14, y=.68, tam=290, foco=(.5, .3, 1.3)):
    """Medallón para menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.22, y=.54, ancho=480, giro=3.5):
    """Expediente con retrato; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.62, tam=290):
    """Cartas en abanico cuando la voz enumera. fotos = [(slug, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def com(en, cid, dur=7.0, x=.30, y=.30):
    """Captura del comentario REAL (yt comentario)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760, giro=-2.0)


# ------------------------------------------------------------------ fichas y MG
def ficha(en, titulo, texto, sub=None, dur=5.5, a=None, x=_FX, y=_FY, ancho=820):
    d = dict(tipo="mg", fn=B.ficha(titulo, texto, sub, ancho=ancho), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def xbox(en, dur=5.0):
    return dict(tipo="mg", fn=B.ficha("Xbox 360", "Versión de 2009", ancho=430), en=en, dur=dur, x=.86, y=.24, sale=.3,
                nombre="rótulo Xbox", ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def vs(de, a, marcas, izq, der, titulo=None, marca="CAMBIÓ", y=.54):
    """versus: izq/der = (etiqueta, texto, slug o None)."""
    def col(c):
        return dict(etiqueta=c[0], texto=c[1], icono=P(c[2]) if len(c) > 2 and c[2] else None)
    return mg(B.versus(col(izq), col(der), titulo, marca), de, a, marcas, "versus " + (titulo or izq[0]), y=y)


def cad(de, a, marcas, titulo, pasos, final, y=.55):
    """cadena: pasos = [(slug o None, texto)], final = (slug o None, texto)."""
    return mg(B.cadena(titulo, [(P(s) if s else None, t) for s, t in pasos], (P(final[0]) if final[0] else None, final[1])),
              de, a, marcas, "cadena " + titulo, y=y)


def donde(en, items, dur=4.4):
    """Tira baja: items = [(slug, etiqueta, nombre)] (MUNDO / PERSONAJE…)."""
    return dict(tipo="mg", fn=B.ficha_mundo([(P(s), e, n) for s, e, n in items]), en=(en, .5), dur=dur, x=.5, y=.86, sale=.35,
                nombre="MG dónde " + items[0][2], ver=1.3)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub="Guía oficial de Nintendo", ventana=False, x=.70, y=.44, recorte=None, **kw):
    """Mapa REAL con ruta (tema gaming). `puntos` en fracciones de la imagen ENTERA; 5.º elemento = slug de la foto."""
    ruta = os.path.join(_MAP, slug + ".jpg")
    if recorte:
        x0, y0, x1, y1 = recorte
        puntos = [((p[0] - x0) / (x1 - x0), (p[1] - y0) / (y1 - y0)) + tuple(p[2:]) for p in puntos]
    puntos = [p[:4] + ((P(p[4]) if p[4] else None),) if len(p) > 4 else p for p in puntos]
    fn = MP.mapa(ruta, puntos, "gaming", titulo=titulo, sub=sub, recorte=recorte, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


# ------------------------------------------------------------------ los 50 secretos: ancla de inicio y título
SECRETOS = [
    (50, "Número cincuenta", "Ya jugaste el primero"),
    (49, "Cuarenta y nueve Cuando llamas", "¿Estás ciego?"),
    (48, "Cuarenta y ocho En los archivos", "Huevo culo"),
    (47, "Cuarenta y siete De toda", "La favorita de Kirkhope"),
    (46, "Cuarenta y seis Al llegar", "Por la puerta de atrás"),
    (45, "Cuarenta y cinco En casa", "La gorra de Ash"),
    (44, "Cuarenta y cuatro Cuando Banjo", "La mochila mágica"),
    (43, "Cuarenta y tres En el video", "Bautizados por los lectores"),
    (42, "Cuarenta y dos Al entrar", "«La música ha cambiado»"),
    (41, "Cuarenta y uno Una teoría", "La isla con forma de icono"),
    (40, "Cuarenta Los huevos misteriosos", "Los huevos misteriosos"),
    (39, "Treinta y nueve La Hag", "Matrícula GB y motor V10"),
    (38, "Treinta y ocho Todo el juego", "Dos diseñadores y un mando"),
    (37, "Treinta y siete Pawno", "El traje del pirata de Dream"),
    (36, "Treinta y seis En Xbox", "El examen cambió en Xbox"),
    (35, "Treinta y cinco La música", "La isla suena a guarida"),
    (34, "Treinta y cuatro En Hailfire", "Sabreman y el delfín"),
    (33, "Treinta y tres Lo que murmura", "Eekum Bokum"),
    (32, "Treinta y dos Rare es", "Europa, la última"),
    (31, "Treinta y uno Ya te contamos", "El castillo que se cortó"),
    (30, "Treinta Jamjars", "Las rimas de Jamjars"),
    (29, "Veintinueve En el concurso", "Abucheos en el concurso"),
    (28, "Veintiocho Kirkhope tuvo", "Kirkhope, a medias dos veces"),
    (27, "Veintisiete La música", "La canción bajo la perforadora"),
    (26, "Veintiséis Mucha gente", "La voz del sargento"),
    (25, "Veinticinco Los warp pads", "Warp pads de última hora"),
    (24, "Veinticuatro Cuando Kazooie", "La sombra del dragón"),
    (23, "Veintitrés El concurso", "Las trampas del concurso"),
    (22, "Veintidós Del Stomponadon", "El pie del dinosaurio"),
    (21, "Veintiuno En casa", "El peluche de Donkey Kong"),
    (20, "Veinte Según la wiki del juego, si", "«Otra fuerza» abrió la puerta"),
    (19, "Diecinueve En Banjo-Tooie", "Grunty deja de rimar"),
    (18, "Dieciocho Los Minjos", "El Minjo de gimnasio"),
    (17, "Diecisiete Lord Woo", "El pez con demasiados huesos"),
    (16, "Dieciséis En Grunty", "El fontanero innombrable"),
    (15, "Quince Los cuarenta", "Jinjos de color al azar"),
    (14, "Catorce Kirkhope compuso", "La intro desfasada"),
    (13, "Trece Esa intro", "Una noche en vela antes del E3"),
    (12, "Doce A Klungo", "Klungo renuncia"),
    (11, "Once Según The Cutting", "El papel tapiz del póker"),
    (10, "Diez Grunty Industries", "El primer mundo de Malpass"),
    (9, "Nueve En Jolly", "El cerdo de tres brazos"),
    (8, "Ocho Muchos recuerdan", "Sin Expansion Pak"),
    (7, "Siete Un jugador", "Cuatro horas, diez minutos"),
    (6, "Seis El huevo", "La fábrica de bugs"),
    (5, "Cinco Steve Mayles", "El golpe de Jamjars"),
    (4, "Cuatro Al final", "Banjo-Threeie nunca existió"),
    (3, ("desconfía de ti", -1.3), "El juego desconfía de ti"),
    (2, "Dos En Terrydactyland", "La montaña «accidental»"),
    (1, "Y el número uno", "La cabeza de Grunty en Japón"),
]
_FIN = {26: "Llevamos veinticinco", 1: "Esos son los cincuenta"}


def _avisos():
    out = []
    for i, (n, en, tit) in enumerate(SECRETOS):
        hasta = _FIN.get(n) or SECRETOS[i + 1][1]
        out.append(dict(tipo="mg", fn=B.secreto(n, tit, jiggy=JIGGY), en=en, dur=4.0, x=.5, y=.19, sale=.45,
                        nombre=f"aviso secreto {n}", ver=1.4))
        out.append(dict(tipo="mg", fn=B.contador(n, jiggy=JIGGY), de=(en, 4.2), a=(hasta, -.4), x=.87, y=.085, sale=.3,
                        nombre=f"aviso contador {n}", ver=1.0))
    return out


_TIT = {k: P("titulo_" + k) for k in ("mt", "ggm", "ww", "jrl", "tdl", "gi", "hfp", "ccl")}

FX = [
    # ================================================================ GANCHO (un elemento nuevo cada 2-3 s)
    grande("En Japón, Banjo-Tooie tiene otro final", "logo_bt_jp", "Japón", lado="der", dur=3.0, tam=560),
    cam("La cabeza de la bruja", "grunty_head", "Gruntilda", x=.16, y=.62, dur=3.4, tam=320),
    ficha("y la cambian por un saco", "Versión japonesa", "La cabeza de Grunty, cambiada por *un saco*", sub="El final", dur=3.6),
    ficha("cuando la patean, se le sale el ojo", "Y aun así…", "Se le sale *el ojo*", sub="Japón", dur=2.6, x=.27),
    mg(B.antipirata(), "Hay un cartucho", ("si eres un pirata|fin", .3),
       ["doscientas sesenta y ocho", ("doscientas sesenta y ocho veces|fin", .2), "si eres un pirata"], "antipirata gancho"),
    sil("Un jefe que tenía demasiados huesos", "lord_woo", "Lord Woo Fak Fak", "Demasiados huesos", lado="der", dur=3.0, alto=700),
    peg("Y una montaña que Rare jura", "titulo_tdl", "Terrydactyland", dur=3.6, x=.20, y=.60, tam=420),
    aba([("caja_bt", "Su historia"), ("jiggy", "Jiggies crueles"), ("titulo_ww", "Ocho mundos")], de="Ya te contamos su historia",
        a=("Creías que no quedaba nada|fin", .4), marcas=["su historia", "sus Jiggies", "y sus ocho mundos"], nombre="videos anteriores"),
    vs(("Quedan cincuenta", 1.6), ("ni siquiera se ven en tu versión|fin", .6), ["Y algunos ni siquiera", ("se ven en tu versión", .3)],
       ("NINTENDO 64", "El original, 2000", "n64"), ("XBOX 360", "Rare ya era de Microsoft", "xbox360"), titulo="Cada versión, su secreto",
       marca=None),
    grande("Estos son los cincuenta secretos", "caja_bt", "Banjo-Tooie (2000)", lado="der", dur=4.2, tam=560),
    peg("Del más curioso al que de verdad", "jiggy", "50 secretos", dur=3.2, x=.20, y=.62, tam=330),

    # ================================================================ 50
    donde("Número cincuenta", [("bk_1998", "PRIMERO", "Banjo-Kazooie (1998)"), ("caja_bt", "SEGUNDO", "Banjo-Tooie (2000)")]),
    cad("Empiezas en Spiral Mountain", ("de Bottles te los recuerda|fin", .5),
        ["Empiezas en Spiral Mountain", "con todos los movimientos", "desde el minuto uno", "y solo el fantasma", "de Bottles te los recuerda"],
        "TODO DESDE EL MINUTO UNO", [(None, "Saltar"), (None, "Picotazo"), (None, "Huevos"), (None, "Volar")], ("banjo", "Ya te los sabes")),
    ficha("Steve Malpass, uno de sus diseñadores", "Steve Malpass", "¿Quién iba a empezar una saga *por el segundo juego*?",
          sub="Diseñador de Rare", a=("por el segundo juego|fin", .4), x=.27),
    cam("Una revista japonesa", "logo_bt_jp", "Japón", x=.86, y=.66, dur=3.6),
    ficha("se quejó justo de eso", "La queja", "*Demasiados movimientos* para alguien nuevo", sub="Revista japonesa", dur=3.6, x=.30),

    # ================================================================ 49
    peg("al tren Chuffy", "chuffy", "Chuffy", dur=3.4),
    sil("Old King Coal, el rey", "old_king_coal", "Old King Coal", "Vive en la caldera", lado="der", dur=3.0),
    cad("te dice qué está haciendo", ("en el lado de lava|fin", .6), ["cargando mineral", "disfrutando de las atracciones", "calentando sus carbones"],
        "¿QUÉ HACE EL REY?", [("titulo_ggm", "Cargando mineral"), ("titulo_ww", "En las atracciones")], ("titulo_hfp", "Calentando carbones")),
    mapa("ggm", [(.75, .15, "Estación", "meta", "chuffy")], de="Y si lo llamas desde la estación", a=("delante de ti|fin", .6),
         marcas=["desde la estación"], titulo="Glitter Gulch Mine", ventana=True),

    # ================================================================ 48
    donde("Cuarenta y ocho En los archivos", [("kazooie", "DISPARO", "Huevos de Kazooie")]),
    rel("la animación de disparar huevos", "egg_blue", "egg head", "Hacia delante", dur=2.5, y=.60),
    vs("se llama egg head", ("se llama egg ass|fin", 1.6), ["se llama egg head", "se llama egg ass", ("se llama egg ass|fin", .4)],
       ("HACIA DELANTE", "egg head: cabeza de huevo", "egg_blue"), ("HACIA ATRÁS", "egg ass: huevo culo", "egg_yellow"), titulo="Nombres de archivo",
       marca="¿EN SERIO?"),
    grande("en Smash Ultimate", "smash_banjo", "Smash Ultimate", lado="der", dur=4.6),
    ficha("se llama, literalmente", "En japonés", "*Huevo del trasero*", sub="Smash Ultimate", dur=3.8, x=.28),

    # ================================================================ 47 (se oye Atlantis)
    leg("kirkhope", "Grant Kirkhope", ["Compositor de Rare", "Su favorita: Atlantis"], de="la canción favorita de Grant Kirkhope",
        a=("está bajo el agua|fin", .6), y=.60),
    mapa("jrl", [(.32, .04, "Inicio", "inicio"), (.35, .18), (.41, .30), (.50, .52, "El muelle", "paso"), (.57, .77, "Atlantis", "meta", "submarino")],
         de="Es Atlantis", a=("Escúchala un momento|fin", 1.0), marcas=["Es Atlantis", "la ciudad hundida", "al bajar ahí"],
         titulo="Jolly Roger's Lagoon"),
    ficha(("Escúchala un momento|fin", 1.0), "Atlantis", "Jolly Roger's Lagoon, *bajo el agua*", sub="Grant Kirkhope", dur=4.2, x=.5, y=.80),

    # ================================================================ 46
    ban("Al llegar a Cauldron Keep", "cauldron_keep", "Cauldron Keep", "La guarida final", dur=4.0, y=.74),
    mg(B.rotulos([("CAULDRON KEEP", "Secret Exit", "Salida secreta"), ("ENTRADA PRINCIPAL", "Nunca la vemos", None)]),
       "hay un letrero", ("nunca la llegamos a ver|fin", .6), ["hay un letrero", "La entrada principal"], "rótulo salida secreta", y=.42),
    peg("asaltan el castillo de la villana", "gruntilda_bt", "Gruntilda", dur=3.4, x=.15, y=.70, tam=340),

    # ================================================================ 45
    cam(("su hijo Speccy", .2), "speccy", "Speccy", x=.86, y=.66, dur=4.0),
    ficha("lleva una gorra con el símbolo", "La gorra", "El símbolo de la gorra de *Ash*, al revés", sub="Pokémon", dur=4.4, x=.27),
    aba([("juno", "Juno"), ("vela", "Vela"), ("jfg", "Jet Force Gemini")], de="cuelgan pósters de Juno", a=("otro juego de Rare|fin", .6),
        marcas=["de Juno", "y Vela", "Jet Force Gemini"], nombre="pósters"),
    vs("Una gorra de Pokémon", ("ya era de Microsoft|fin", .6), ["Una gorra de Pokémon", "incluso en la versión de Xbox", "ya era de Microsoft"],
       ("NINTENDO 64", "La gorra de Ash en casa de Bottles", "speccy"), ("XBOX 360", "Sigue ahí", "bt_xbla"), titulo="La gorra", marca="SIGUE"),

    # ================================================================ 44
    aba([("shack_pack", "Shack Pack"), ("taxi_pack", "Taxi Pack")], de="como el Shack Pack", a=("hay un truco de magia|fin", .5),
        marcas=["como el Shack Pack", "o el Taxi Pack"], nombre="mochilas"),
    leg("steve_mayles", "Steve Mayles", ["Animador de Rare", "No podía animar", "la mochila"], de="Steve Mayles, el animador",
        a=("lleva a la espalda|fin", .5), x=.75),
    cad("Así que, en un cuadro concreto", ("dura un parpadeo|fin", .6), ["en un cuadro concreto", "esa mochila se apaga", "aparece otra idéntica", "Esa sí se mueve"],
        "EL TRUCO", [(None, "Un cuadro concreto"), (None, "La mochila se apaga"), (None, "Aparece otra idéntica")], ("banjo", "Esa sí se mueve")),

    # ================================================================ 43
    cam("el nombre de Chris", "chris_bacon", "Chris P. Bacon", dur=3.6, x=.86, y=.66),
    ficha("La revista oficial de Nintendo", "Nintendo Official Magazine", "Los lectores *bautizaron* personajes", sub="Reino Unido", dur=4.6, x=.30),
    aba([("old_king_coal", "Old King Coal"), ("bullion_bill", "Bullion Bill")], de="de ahí salen también", a=("Glitter Gulch Mine|fin", .4),
        marcas=["Old King Coal, el del tren", "y Bullion Bill"], nombre="bautizados"),
    cad("El premio", ("dentro de un cartucho|fin", .8), ["El premio", "un póster firmado", "y tu nombre dentro"],
        "EL PREMIO", [("caja_bt", "El juego"), (None, "Un póster firmado")], ("jiggy", "Tu nombre en el cartucho")),

    # ================================================================ 42 (se oye el cambio de música)
    donde("Cuarenta y dos Al entrar", [("gatehouse", "LUGAR", "The Gatehouse"), ("cauldron_keep", "MUNDO", "Cauldron Keep")]),
    vs("Banjo dice que ahí no hay nadie", ("acabamos peleando|fin", .6), ["Banjo dice que ahí no hay nadie", "La música ha cambiado", "acabamos peleando"],
       ("BANJO", "«Aquí no hay nadie»", "banjo"), ("KAZOOIE", "«La música ha cambiado»", "kazooie"), titulo="Lógica de videojuego", marca="PELEA"),
    sil("Klungo cae del techo", "klungo", "Klungo", "Cae del techo", lado="der", dur=4.0),

    # ================================================================ 41
    peg(("Cuarenta y uno Una teoría", 4.1), "isla_mapa", "Isle O' Hags", dur=9.0, x=.5, y=.50, tam=1000, giro=0.0),
    cam("A la izquierda, la cabeza de Banjo", "banjo", "Banjo", x=.10, y=.78, dur=4.6, tam=250),
    cam("A la derecha, parte", "kazooie", "Kazooie", x=.90, y=.78, dur=3.6, tam=250),
    ficha("Rare nunca lo confirmó", "Teoría de fans", "¿Diseño o *casualidad*?", sub="Sin confirmar", dur=4.4, x=.5, y=.86, ancho=760),

    # ================================================================ 40
    donde("Cuarenta Los huevos misteriosos", [("heggy", "GALLINERO", "Heggy"), ("bk_1998", "VIENEN DE", "Banjo-Kazooie")]),
    peg("en el gallinero de Heggy", "heggy", "Heggy", dur=2.6, x=.80),
    cad("El rosa te da", ("quién es Jinjo|fin", .8), ["El rosa te da", "El azul, un truco", "Y el amarillo", "quién es Jinjo"],
        "HUEVOS MISTERIOSOS", [("breegull_bash", "Rosa: Breegull Bash"), ("egg_blue", "Azul: huevos que persiguen"),
                               ("egg_yellow", "Amarillo: Jinjo jugable")], ("jinjo", "«¿Quién es Jinjo?»")),

    # ================================================================ 39
    grande("La Hag 1, la perforadora", "hag1", "Hag 1", lado="der", dur=3.3),
    vs("lleva detrás una matrícula", ("encantadora perforadora|fin", .6), ["una matrícula con las letras", "siente la potencia", "Y en el concurso"],
       ("MATRÍCULA", "HAG 1 y el óvalo GB"), ("MOTOR", "«Esa bestia V10»"), titulo="La Hag 1", marca="BRITÁNICA"),
    cam("qué pone en la matrícula", "tower_tragedy", "Tower of Tragedy", x=.88, y=.80, dur=3.2, tam=240),

    # ================================================================ 38
    leg("gregg_mayles", "Gregg Mayles", ["Diseñador", "Banjo-Tooie"], de="Gregg Mayles y Steve Malpass", a=("Primero inventaban", 0), y=.60),
    cad("Primero inventaban las tareas", ("un mando de Nintendo 64|fin", .6), ["Primero inventaban las tareas", "luego hacían los mundos", "y todo en papel",
                                                                            "un mando de Nintendo 64"],
        "CÓMO SE HIZO", [(None, "Las tareas"), (None, "Los mundos a medida"), ("isla_diseno", "Todo en papel")], ("n64_mando", "Un editor con mando de N64")),
    rel("La cámara del Saucer of Peril", "saucer_peril", "Saucer of Peril", "Witchyworld", dur=3.6, x=.74),
    mapa("ww", [(.82, .58, "Entrada", "inicio"), (.70, .50), (.48, .45, "La carpa", "paso"), (.50, .68), (.62, .84, "Zona Espacial", "meta", "saucer_peril")],
         de="se trazó así", a=("a partes iguales|fin", .6), marcas=["se trazó así", "curva a curva", "la odia"], titulo="Witchyworld"),

    # ================================================================ 37
    peg("Pawno, el usurero", "pawno", "Pawno", dur=3.4, x=.80),
    vs("viste la ropa del Capitán Cockeye", ("convertido en Banjo-Kazooie|fin", .8), ["viste la ropa", "pensado para Dream", "convertido en Banjo-Kazooie"],
       ("PAWNO", "Jolly Roger's Lagoon", "pawno"), ("CAPITÁN COCKEYE", "Dream, el juego que no salió", "cockeye"), titulo="El mismo traje",
       marca="HEREDADO"),
    ficha("Lo contó Ed Bryan", "Ed Bryan", "Diseñó a los *personajes*", sub="Rare", dur=3.4, x=.27),
    sil("el traje sí lo heredó", "cockeye", "Capitán Cockeye", "Project Dream", lado="der", dur=3.6),

    # ================================================================ 36
    peg("hasta el examen de la bruja", "tower_tragedy", "Tower of Tragedy", dur=2.2, x=.80),
    vs("En Nintendo 64, el concurso pregunta", ("con trece|fin", 1.0), ["el concurso pregunta", "pasó a ser por el mando", "con trece"],
       ("NINTENDO 64", "Botones del mando oficial: *10*", "n64_mando"), ("XBOX 360", "Botones del mando de Xbox 360: *13*", "xbox360"),
       titulo="La pregunta de los botones"),
    ficha("le cambiaron la letra", "Xbox 360", "Nueva *letra* en todos los textos", sub="2009", dur=4.0),
    cam("le cambiaron la letra", "bt_xbla", "XBLA 2009", x=.16, y=.66, dur=4.0),

    # ================================================================ 35 (se oye el compás)
    peg("La música de Isle", "isla_mapa", "Isle O' Hags", dur=3.6, x=.78, y=.58, tam=520, giro=4.0),
    vs("Kirkhope le dio el mismo compás", ("el hilo entre los dos|fin", .6), ["Kirkhope le dio", "el castillo del primer juego", "el hilo entre los dos"],
       ("ISLE O' HAGS", "Banjo-Tooie (2000)", "caja_bt"), ("GRUNTY'S LAIR", "Banjo-Kazooie (1998)", "bk_1998"), titulo="Mismo compás", marca="6/8"),
    cam("Y dice que en Banjo-Tooie", "kirkhope", "Grant Kirkhope", x=.14, y=.66, dur=4.0),
    mg(B.compas(bpm=120, compases=3), "Escucha ese compás", ("Escucha ese compás|fin", 5.0), ["Escucha ese compás"], "compás"),

    # ================================================================ 34
    mapa("hfp_hielo", [(.40, .92, "Lado de lava", "inicio"), (.45, .72), (.52, .60), (.63, .50), (.64, .38), (.62, .15), (.79, .115, "Sabreman", "meta", "sabreman")],
         de=("Treinta y cuatro En Hailfire", 4.0), a=("su tienda en el lado de lava|fin", .4), marcas=[("Treinta y cuatro En Hailfire", 4.2), "descongelas a Sabreman"],
         titulo="Hailfire Peaks (hielo)"),
    sil("divaga sobre lo mucho", "sabreman", "Sabreman", "Ultimate Play the Game", dur=4.0),
    vs("Dolphin, delfín", ("Rare nunca lo confirmó#2|fin", .6), ["Dolphin, delfín", "el nombre en clave", "Según VGFacts, puede"],
       ("DOLPHIN", "Delfín"), ("GAMECUBE", "Su nombre en clave", "gamecube"), titulo="¿Un guiño?", marca="¿GUIÑO?"),

    # ================================================================ 33 (se oye el conjuro)
    sil(("Treinta y tres Lo que murmura", 4.1), "mumbo", "Mumbo Jumbo", "Chamán", lado="der", dur=3.0),
    rel("En los costados de los Mumbo Pads", "mumbo_pad", "Mumbo Pad", dur=4.0, y=.64, tam=440),
    mg(B.rotulos([("MUMBO JUMBO", "Eekum Bokum", "Lo que murmura")]), "pone: Eekum Bokum", ("pone: Eekum Bokum|fin", 2.6), ["pone: Eekum Bokum"],
       "rótulo Eekum Bokum", y=.30),
    leg("kirkhope", "Grant Kirkhope", ["La voz de Mumbo", "Compositor"], de="es del propio compositor", a=("Grant Kirkhope#2|fin", 2.0), x=.75),

    # ================================================================ 32
    cam("Rare es un estudio británico", "rare_hq", "Rare, Twycross", x=.86, y=.66, dur=3.6),
    mg(B.fechas([("Norteamérica", "20 nov 2000", "na"), ("Japón", "27 nov 2000", "jp"), ("Europa", "12 abr 2001", "eu", "cinco meses después")],
                "Una salida en tres tiempos"),
       "Salió en Norteamérica", ("abril del dos mil uno|fin", .8), ["Salió en Norteamérica", "en Japón una semana", "y en Europa no llegó"], "fechas"),
    grande("En Japón, además, se llama", "logo_bt_jp", "Banjo to Kazooie no Daibouken 2", lado="der", dur=4.0),
    ficha("La gran aventura de Banjo", "Título japonés", "*La gran aventura* de Banjo y Kazooie 2", dur=3.4, x=.28),

    # ================================================================ 31
    leg("gregg_mayles", "Gregg Mayles", ["Enseñó los dibujos", "del castillo original"], de="Ya te contamos que el último mundo",
        a=("Lo nuevo es cómo era|fin", .4), x=.75, y=.60),
    cad("En los dibujos que enseñó", ("cañones en las almenas|fin", .6), ["un castillo de piedra", "fortaleza de metal", "con un cementerio", "y cañones"],
        "EL CASTILLO ORIGINAL", [(None, "Castillo de piedra"), (None, "Fortaleza de metal"), (None, "Cementerio detrás")], (None, "Cañones en las almenas")),
    cad("Según la wiki del juego, había", ("hasta Cloud Cuckooland|fin", .6), ["una cripta", "una armadura embrujada", "y una semilla", "hasta Cloud Cuckooland"],
        "LO QUE SE CORTÓ", [(None, "Cripta con fantasma"), (None, "Armadura embrujada"), ("mumbo", "Semilla de Mumbo")], ("titulo_ccl", "Cloud Cuckooland")),
    peg(("Del castillo grande quedaron restos", .7), "gatehouse", "Lo que quedó", dur=4.4, x=.78, y=.60, tam=460),

    # ================================================================ 30 (se oye la cadencia)
    sil(("Treinta Jamjars", 4.1), "jamjars", "Jamjars", "Hermano de Bottles", dur=3.4),
    rel("rima con los botones", "n64_mando", "Mando de Nintendo 64", dur=3.6, x=.74),
    vs("en Xbox el botón de ataque", ("se quedaron sin rima|fin", 1.2), ["en Xbox el botón", "dejó de ser la B", "se quedaron sin rima"],
       ("NINTENDO 64", "Ataque: botón *B*", "n64_mando"), ("XBOX 360", "Ataque: otro botón", "xbox360"), titulo="Las rimas de Jamjars",
       marca="SIN RIMA"),

    # ================================================================ 29 (se oyen los abucheos)
    donde("Veintinueve En el concurso", [("tower_tragedy", "CONCURSO", "Tower of Tragedy"), ("grunty", "PRESENTA", "Gruntilda")]),
    ficha("el público aplaude a las hermanas", "El público", "Aplausos a las hermanas, *abucheos* a Banjo", sub="Tower of Tragedy", dur=4.6, x=.30, y=.48),
    mg(B.rotulos([("GRUNTY", "«Estoy rodeada de imbéciles»", "Casi la frase de Scar"), ("GRUNTY", "«Conozcamos a las víctimas…»", "…eh, concursantes")]),
       "Si nadie acierta", ("quiero decir, concursantes|fin", 1.0), ["estoy rodeada de imbéciles", "Y presenta así"], "rótulos Grunty", y=.40),

    # ================================================================ 28
    leg("kirkhope", "Grant Kirkhope", ["Dejó la música", "a medias dos veces"], de="Kirkhope tuvo que dejar", a=("Empezó la música", 0), x=.75, y=.60),
    aba([("dk64", "Donkey Kong 64"), ("perfect_dark", "Perfect Dark")], de="le pidieron Donkey Kong", a=("que salían antes|fin", .6),
        marcas=["le pidieron Donkey Kong", "y luego Perfect Dark"], nombre="interrupciones"),
    cad("a mitad del desarrollo", ("en un solo día|fin", 1.0), ["Rare se mudó", "una milla más abajo", "en un solo día"],
        "LA MUDANZA", [(None, "Sede vieja"), (None, "Una milla más abajo")], ("rare_hq", "Toda la empresa, en un día")),

    # ================================================================ 27 (se oye la Hag 1)
    rel("el tema de la Hag 1", "hag1", "Hag 1", "Jefe final", dur=1.4),
    vs("es en parte una variación", ("debajo del motor de la perforadora|fin", .8), ["es en parte una variación", "la del primer juego", "debajo del motor"],
       ("HAG 1", "El tema del jefe final", "hag1"), ("GRUNTY'S LAIR", "Banjo-Kazooie (1998)", "bk_1998"), titulo="Una canción escondida",
       marca="DEBAJO"),
    ficha("Escúchala#2", "Vs. Hag 1", "*Grunty's Lair*, debajo del motor", sub="Grant Kirkhope", dur=5.4, x=.5, y=.80),

    # ================================================================ 26
    leg("lee_ermey", "R. Lee Ermey", ["La chaqueta metálica", "¿La voz de Jamjars?"], de="es de R. Lee Ermey", a=("Falso|fin", 1.4),
        marcas=["Falso"], sello=("FALSO", 0)),
    cam("Es de Grant Kirkhope", "kirkhope", "Grant Kirkhope", x=.86, y=.62, dur=3.0),
    aba([("mumbo", "Mumbo"), ("jingaling", "Rey Jingaling"), ("jinjo", "Jinjos")], de="las voces de Mumbo", a=("y de los Jinjos|fin", .8),
        marcas=["las voces de Mumbo", "del rey Jingaling", "y de los Jinjos"], nombre="voces de Kirkhope"),
    ficha("Y su nombre es un insulto", "Jam jars", "En inglés británico: *cuatro ojos*", sub="Kazooie a Bottles", a=("cuatro ojos|fin", .8)),

    # ================================================================ MITAD: comentarios reales
    ficha("leemos todos sus comentarios", "Sus comentarios", "Todos se *leen* y se toman en cuenta", sub="Gracias", dur=4.4, x=.5, y=.24),
    com("Como el de Riuma", "UgxdnznPHsijj-I2lE94AaABAg", dur=8.0, x=.30, y=.42),
    com(("O el de Antilope", .6), "Ugw2j_5-7ktR9uVpcxl4AaABAg", dur=7.6, x=.68, y=.42),
    peg("déjalo abajo", "jiggy", "Tu secreto, abajo", dur=3.0, x=.80, y=.70, tam=300),

    # ================================================================ 25
    rel("Los warp pads, las baldosas", "warp_pad", "Warp Pad", "Teletransporte", dur=4.0, y=.60),
    cad("Los mundos ya estaban diseñados", ("fue Ocarina of Time|fin", .8), ["Los mundos ya estaban", "los probadores se quejaban", "ya era tarde", "fue Ocarina of Time"],
        "AL FINAL DEL DESARROLLO", [(None, "Mundos ya hechos"), (None, "Probadores hartos"), ("warp_pad", "Warp pads")], (None, "Inspiración: Ocarina of Time")),

    # ================================================================ 24
    sil("se convierte en dragón", "dragon_kazooie", "Kazooie dragón", "Hailfire Peaks", lado="der", dur=4.0),
    ficha("Su retrato al hablar no cambia", "Sin programar", "Retrato y escenas finales: *la Kazooie de siempre*", sub="Kazooie dragón",
          a=("la Kazooie de siempre|fin", .4), x=.27),
    vs("Y los colores casi se invierten", ("con ojos oscuros|fin", .8), ["Y los colores casi", "la normal es roja", "y la dragón, verde"],
       ("KAZOOIE", "Roja, ojos verdes", "kazooie"), ("DRAGÓN", "Verde, ojos oscuros", "dragon_kazooie"), titulo="Colores casi invertidos", marca="AL REVÉS"),

    # ================================================================ 23
    mg(B.concurso("¿En qué juego apareció Banjo por primera vez?", ["Banjo-Kazooie", "Diddy Kong Racing", "Super Banjo Land 64"], 1, trampa=2),
       "Una pregunta", ("Super Banjo Land 64|fin", 1.4), ["no es Banjo-Kazooie", "Es Diddy Kong Racing", "La opción falsa", ("Super Banjo Land 64|fin", .2)],
       "concurso primera aparición"),
    cam("Es Diddy Kong Racing", "dkr", "Diddy Kong Racing", x=.89, y=.80, dur=3.6, tam=230),
    aba([("perfect_dark", "Perfect Grunty"), ("dk64", "Grunty Kong 64")], de=("Y hay respuestas de broma", .7), a=("Grunty Kong 64|fin", .8),
        marcas=["como Perfect Grunty", "o Grunty Kong"], nombre="respuestas de broma"),

    # ================================================================ 22
    grande("Del Stomponadon, el dinosaurio", "stomponadon", "Stomponadon", lado="der", dur=4.0),
    vs("Y ese pie viene", ("en dos mil quince|fin", .8), ["Y ese pie viene", "al protagonista lo iba", "Rare enseñó esas"],
       ("TERRYDACTYLAND", "Solo ves el pie", "stomponadon"), ("DREAM", "Un dinosaurio gigante que aplasta", "dream"), titulo="El pie que vino de Dream",
       marca="MISMO PIE"),

    # ================================================================ 21
    cam(("su hija Goggles", .3), "goggles", "Goggles", dur=2.6),
    rel("con un peluche de Donkey Kong", "dk_plush", "Peluche de Donkey Kong", dur=1.6, x=.74, y=.62),
    vs("En la versión de Xbox, con Rare", ("ojos saltones|fin", .8), ["En la versión de Xbox", "le quitaron la corbata", "ojos saltones"],
       ("NINTENDO 64", "Donkey Kong con su corbata", "dk_plush"), ("XBOX 360", "Sin corbata y con ojos saltones"), titulo="El peluche", marca="CAMBIÓ"),
    ficha("la respuesta Donkey Kong", "Tower of Tragedy (Xbox)", "Donkey Kong pasó a ser *un gorila adorable*", sub="Xbox 360", dur=4.0, x=.28),
    cam("Y en Nintendo Switch Online, el peluche", "dk_plush", "Donkey Kong", x=.86, y=.66, dur=3.4),

    # ================================================================ 20
    cad("Si abres un mundo", ("ha abierto esa puerta|fin", .8), ["Si abres un mundo", "se da cuenta", "otra fuerza"],
        "SI USAS UN CÓDIGO", [("cheato", "Código de Cheato"), ("jiggywiggy", "Jiggywiggy se da cuenta")], (None, "«Otra fuerza abrió la puerta»")),
    sil("si fallas muchas veces", "jiggywiggy", "Jiggywiggy", "Maestro de los Jiggies", dur=3.6),
    ficha("si fallas muchas veces", "Jiggywiggy", "Si fallas mucho, *baja la dificultad*", sub="Sin decírtelo", a=("sin decírtelo|fin", .8)),

    # ================================================================ 19
    vs("En Banjo-Tooie, Grunty deja de rimar", ("le pareció gracioso|fin", .6), ["deja de rimar", "Gregg Mayles lo hizo", "le pareció gracioso"],
       ("BANJO-KAZOOIE", "Grunty habla en rimas", "grunty"), ("BANJO-TOOIE", "Deja de rimar", "gruntilda_bt"), titulo="Las rimas de Grunty",
       marca="SIN RIMAS"),
    leg("gregg_mayles", "Gregg Mayles", ["«No fue una de", "mis mejores ideas»"], de="Años después admitió", a=("nunca lo sabes|fin", .8)),
    sil("Pero, dijo, si no pruebas", "grunty", "Gruntilda", lado="der", dur=3.4, alto=720),

    # ================================================================ 18
    rel("Los Minjos son Jinjos falsos", "minjo", "Minjo", "Jinjo falso", dur=4.0, y=.58),
    vs("En los datos del juego", ("se le veía venir de lejos|fin", .6), ["hay un modelo sin usar", "musculoso y con colmillos", "descartado porque"],
       ("MINJO", "Jinjo falso que ataca", "minjo"), ("SIN USAR", "Enorme, musculoso y con colmillos"), titulo="En los datos del juego",
       marca="DESCARTADO"),
    cam("Un Minjo de gimnasio", "jinjo", "Jinjo", x=.86, y=.66, dur=3.4),

    # ================================================================ 17
    mapa("jrl", [(.57, .77, "Fondo del mar", "meta", "lord_woo")], de=("Diecisiete Lord Woo", 4.2), a=("su animador|fin", .4),
         marcas=[("Diecisiete Lord Woo", 4.4)], titulo="Jolly Roger's Lagoon", ventana=True),
    sil("Partes del jefe no se movían", "lord_woo", "Lord Woo Fak Fak", "Jefe de Jolly Roger's", dur=3.6),
    mg(B.huesos(n=12, quitar=4), "Steve Mayles descubrió", ("nunca volvió a ser el mismo|fin", .8), ["Tuvo que quitarle huesos", "nunca volvió"],
       "huesos"),
    cam("si alguna vez te pareció", "lord_woo", "Lord Woo Fak Fak", x=.86, y=.66, dur=5.4),

    # ================================================================ 16
    donde("Dieciséis En Grunty", [("titulo_gi", "MUNDO", "Grunty Industries"), ("loggo", "VÁTER", "Loggo")]),
    peg("Loggo, el váter", "loggo", "Loggo", dur=3.4, x=.80),
    vs("Si le hablas por segunda vez", ("tan famoso|fin", 1.0), ["dice el nombre", "En Xbox, con Microsoft", "Quedó como"],
       ("NINTENDO 64", "«Llama a un fontanero: *Mario*»", "n64"), ("XBOX 360", "«Ese italiano tan famoso»", "xbox360"), titulo="El fontanero",
       marca="CENSURA"),

    # ================================================================ 15
    mg(B.jinjos_color(), "Los cuarenta y cinco Jinjos", ("antes del tercer mundo|fin", .4), ["se sortea en cada partida"], "jinjos color"),
    cam("aunque es muy raro", "jinjo", "Jinjo", x=.14, y=.66, dur=3.0),
    ficha("Los speedrunners lo saben", "speedrun.com", "Categoría para partidas que *manipulan* el sorteo", sub="Speedrun", a=("ese sorteo|fin", .8)),

    # ================================================================ 14
    vs("Kirkhope compuso la música", ("desfasada|fin", .8), ["al compás del video", "En Xbox el juego", "treinta segundos desfasada"],
       ("NINTENDO 64", "La música, al compás de los tirones", "n64"), ("XBOX 360", "Más fluido: +30 s de desfase", "xbox360"), titulo="La intro",
       marca="DESFASE"),
    ficha("Y en Nintendo Switch Online, las demos", "Switch Online", "Las demos del título, *aceleradas*", sub="Nintendo Switch", dur=4.4, x=.28),
    peg("tres cafés", "banjo", "Banjo", dur=2.6, x=.80, y=.62, tam=340),

    # ================================================================ 13
    mg(B.cronometro([("La intro de Banjo-Tooie", "10:00")]), "Esa intro dura diez minutos", ("fue un castigo|fin", .6), ["Esa intro dura"], "cronómetro intro",
       y=.40),
    ficha("Ed Bryan, el encargado", "Ed Bryan", "Mover personajes por *curvas* y sincronizar a mano", sub="La intro", a=("a mano|fin", .6)),
    cad("Para el E3", ("lo lograron|fin", 1.0), ["Para el E3", "Él y su hermano Will", "pasadas las seis", "Al final, lo lograron"],
        "E3 2000", [(None, "Sin desfasarse"), (None, "Ed y Will Bryan"), (None, "Pasadas las 6 a. m.")], ("caja_bt", "Lo lograron")),

    # ================================================================ 12
    mg(B.rotulos([("KLUNGO", "Minion with a Mission", "Esbirro con una misión"), ("KLUNGO", "Revenge-Seeking Minion", "Esbirro sediento de venganza"),
                  ("KLUNGO", "Career-Questioning Minion", "Esbirro que se replantea su carrera")]),
       "el rótulo de su pelea", ("se replantea su carrera|fin", .8), ["esbirro con una misión", "esbirro sediento", "y esbirro que se replantea"],
       "rótulos Klungo", y=.48),
    sil("En la última pelea renuncia", "klungo", "Klungo", "Renuncia", dur=2.0),
    cad("sin ascensos", ("juegos estúpidos|fin", .6), ["sin ascensos", "sin días libres", "sin sueldo", "buscará un trabajo"],
        "LA RENUNCIA", [(None, "Sin ascensos"), (None, "Sin días libres"), (None, "Sin sueldo")], (None, "«Juegos estúpidos»")),
    grande("tiene su propio juego", "hero_klungo", "Hero Klungo Sssavesss Teh World", lado="der", dur=4.4),
    cam("se cambia de bando", "nuts_bolts", "Nuts & Bolts", x=.14, y=.66, dur=3.0),

    # ================================================================ 11
    ficha("Según The Cutting Room Floor", "The Cutting Room Floor", "Datos ocultos del modelo de la casa", sub="Según TCRF", dur=3.6, x=.27, y=.62),
    vs("esconde otra casa", ("ni se nota|fin", .6), ["esconde otra casa", "papel tapiz de flores", "usaría esa casa vieja"],
       ("BANJO-TOOIE", "Papel de rombos", "caja_bt"), ("COPIA OCULTA", "La casa de Banjo-Kazooie: flores amarillas", "bk_1998"),
       titulo="Dos casas en una", marca="OCULTA"),
    peg("los diez que de verdad", "jiggy", "Top 10", dur=3.0, x=.5, y=.55, tam=420, giro=0.0),

    # ================================================================ 10
    grande("Grunty Industries, la fábrica", "titulo_gi", "Grunty Industries", lado="der", dur=3.6),
    mapa("gi", [(.235, .83, "Entrada", "inicio"), (.30, .76), (.39, .63, "Puerta", "paso"), (.47, .72), (.55, .72, "Estación", "paso", "chuffy"),
                (.54, .58), (.63, .39, "Piso 1", "meta")],
         de="La dibujó en papel", a=("en todas las plantas|fin", 1.0), marcas=["La dibujó en papel", "piso a piso", "con el hueco del ascensor"],
         titulo="Grunty Industries"),
    ficha("Su consuelo", "Steve Malpass", "Muchos la odian, a algunos *les encanta*", sub="Diseñador", a=("que la indiferencia|fin", .4)),
    mg(B.puesto(8, "Grunty Industries", JIGGY, etiqueta="PUESTO"), "en nuestro ranking", ("no es personal|fin", .6), [], "ranking GI", y=.30),

    # ================================================================ 9
    peg("vive Trotty", "trotty", "Trotty", dur=6.0, x=.80),
    vs("en la versión japonesa le quitaron", ("la pelota de playa|fin", .8), ["en la versión japonesa", "solo le preocupa", "y la pelota de playa"],
       ("OCCIDENTE", "Tres brazos", "trotty"), ("JAPÓN", "Le quitaron el brazo", "trotty_jp"), titulo="Trotty", marca="CENSURA"),
    cam("El agua tóxica, no", "logo_bt_jp", "Japón", x=.14, y=.66, dur=2.6),

    # ================================================================ 8
    cam("Muchos recuerdan", "n64", "Nintendo 64", x=.86, y=.66, dur=2.0),
    mg(B.memoria(pak=P("expansion")), "necesitaba el Expansion Pak", ("la parte de atrás|fin", .8),
       ["necesitaba el Expansion Pak", "Falso: funciona", "borra sobre la marcha"], "memoria"),
    vs("El cartucho, además", ("el de Banjo-Kazooie|fin", 1.0), ["El cartucho, además", "doscientos cincuenta y seis", "el doble que"],
       ("BANJO-KAZOOIE", "128 megabits", "bk_1998"), ("BANJO-TOOIE", "256 megabits", "caja_bt"), titulo="El cartucho", marca="EL DOBLE"),

    # ================================================================ 7
    mg(B.cronometro([("Tú, al 100 %", "decenas de horas"), ("Récord 100 % (Falcon)", "4:10:46"), ("Récord, solo el final", "25:49")],
                    "Contra el reloj"),
       "Un jugador normal", ("Menos de lo que dura este video|fin", 1.0), ["Un jugador normal", "El récord mundial", "Y llegar al final"], "cronómetro récords"),

    # ================================================================ 6
    rel("El huevo Clockwork Kazooie", "clockwork", "Clockwork Kazooie", "Bomba de cuerda", dur=3.8, y=.60),
    cad("Podía cruzar puertas", ("se quedaba quieto|fin", .6), ["Podía cruzar puertas", "recoger objetos", "y disparar escenas", "mientras Banjo"],
        "LO QUE PODÍA HACER", [(None, "Cruzar puertas"), (None, "Recoger objetos"), (None, "Disparar escenas")], ("banjo", "Banjo, quieto")),
    ficha("Chris Sutherland cuenta", "Nombre interno", "*babykaz*: Kazooie bebé", sub="Chris Sutherland", a=("Kazooie bebé|fin", .6)),
    aba([("titulo_gi", "Grunty Industries sin tren"), ("titulo_hfp", "Dos Banjos")], de="glitches como entrar", a=("en Hailfire Peaks#3|fin", .8),
        marcas=["entrar en Grunty Industries", "el de los dos Banjos"], nombre="glitches"),

    # ================================================================ 5
    rel("en su silo", "jamjars_silo", "Silo de Jamjars", dur=3.6, x=.74),
    sil("la tapa se cierra antes", "jamjars", "Jamjars", "Se da en la cabeza", dur=3.4),
    grande("Awesome Games Done Quick", "agdq", "Awesome Games Done Quick", lado="der", dur=4.2, tam=560),
    cam("Mayles la vio salir", "steve_mayles", "Steve Mayles", x=.14, y=.66, dur=3.4),
    ficha("Su reacción", "Steve Mayles", "Uno de sus momentos de *mayor orgullo*", sub="Animador de Rare", a=("a ese speedrunner|fin", .6)),

    # ================================================================ 4
    vs("Grunty promete venganza", ("tercer Banjo planeado para GameCube|fin", .6), ["en Banjo-Threeie", "Durante años se creyó", "era solo un chiste"],
       ("EL MITO", "Banjo-Threeie para GameCube"), ("LA VERDAD", "Solo un chiste"), titulo="Banjo-Threeie", marca="FALSO"),
    cam("Gregg Mayles confirmó", "gregg_mayles", "Gregg Mayles", x=.10, y=.32, dur=3.6, tam=240),
    rel("el video de Space World", "gamecube", "GameCube", "Space World 2000", dur=8.0),
    aba([("gobi", "Gobi"), ("alphette", "Alphette")], de="Entre los perseguidores", a=("a nadie|fin", .8), marcas=["hasta Gobi", "y Alphette"],
        nombre="perseguidores", x=.70),

    # ================================================================ 3
    ficha("Si el chip de guardado", "Chip incorrecto", "«*No controller*» y no responde a nada", sub="Antipiratería", a=("no responde a nada|fin", .6)),
    mg(B.antipirata(letrero="SE CONGELA"), "Y eso no es todo", ("se congela sin avisar|fin", .8),
       ["le pregunta al chip", ("doscientas sesenta y ocho veces#2|fin", .2), "se congela sin avisar"], "antipirata 268"),
    cam("Ni el examen de la bruja", "tower_tragedy", "Tower of Tragedy", x=.86, y=.66, dur=3.0),

    # ================================================================ 2
    grande("En Terrydactyland, junto al cráneo", "titulo_tdl", "Terrydactyland", lado="der", dur=4.0),
    ficha("Nintendo Life se lo preguntó", "Nintendo Life", "Entrevista a *Steven Hurst*", sub="Escenarios de Rare", dur=3.8, x=.28),
    cad("Su defensa", ("salió así por accidente#2|fin", .8), ["Su defensa", "el dibujo original", "de verdad cree"],
        "¿ACCIDENTE?", [(None, "Steven Hurst lo pasó a 3D"), ("gregg_mayles", "El dibujo de Gregg Mayles")], (None, "«Salió así por accidente»")),
    peg("Juzga tú", "titulo_tdl", "Juzga tú", dur=2.4, x=.5, y=.50, tam=440, giro=0.0),

    # ================================================================ 1
    vs("En el final, Banjo, Kazooie", ("la tela de su ropa|fin", .8), ["En el final, Banjo", "En la versión japonesa, esa cabeza", "hecho con la tela"],
       ("OCCIDENTE", "Juegan con la cabeza de Grunty", "grunty_head"), ("JAPÓN", "Un saco con la tela de su ropa"), titulo="El final", marca="CENSURA"),
    ficha("Lo absurdo", "El ojo", "Sigue *saliéndose* del saco", sub="Versión japonesa", dur=4.0, x=.28),
    ficha("No hay explicación oficial", "Sin explicación", "Se cree que por un *crimen real* en Japón", sub="Nunca confirmado", dur=7.6),
    grande("En Xbox, por cierto, la cabeza volvió", "grunty_head", "La cabeza de Grunty", lado="izq", dur=3.8),
    xbox("En Xbox, por cierto, la cabeza volvió", dur=3.8),
    cam("sin saber que en Japón", "logo_bt_jp", "Japón", x=.14, y=.66, dur=3.0),

    # ================================================================ CIERRE
    peg("Esos son los cincuenta secretos", "caja_bt", "Banjo-Tooie", dur=3.6, x=.78, y=.56, tam=500, giro=3.0),
    ficha("Cuántos conocías", "¿Cuántos conocías?", "Dímelo en los comentarios, *con número*", dur=4.6, x=.30),
    aba([("caja_bt", "Su historia"), ("jiggy", "Jiggies crueles"), ("titulo_ww", "Ranking de mundos")], de="en el canal están su historia",
        a=("Nos vemos en el próximo secreto|fin", .6), marcas=["su historia", "sus Jiggies más crueles#2", "y el ranking"], nombre="videos del canal", x=.70),
] + _avisos()
ROTULOS = [
    dict(texto="50", en="Quedan cincuenta", tam=200, color="amarillo", y=.30, dur=1.6),
    dict(texto="¿ESTÁS CIEGO?", en="estás ciego", tam=130, color="amarillo", y=.86, dur=2.0),
    dict(texto="UN PARPADEO", en="dura un parpadeo", tam=120, color="amarillo", y=.24, dur=1.8),
    dict(texto="SECRET EXIT", en="Secret Exit", tam=120, color="amarillo", y=.80, dur=2.2),
    dict(texto="SOMBRA DE PÁJARO", en="su sombra la delata", tam=110, color="amarillo", y=.24, dur=2.4),
    dict(texto="BIENVENIDO A CASA", en="Bienvenido a casa", tam=110, color="amarillo", y=.24, dur=2.2),
    dict(texto="MINJO DE GIMNASIO", en="Un Minjo de gimnasio", tam=110, color="amarillo", y=.24, dur=2.2),
    dict(texto="¿ACCIDENTE?", en="Juzga tú", tam=140, color="amarillo", y=.22, dur=2.0),
]
SFX = {}
# SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/bt_*.mp3
_ROTA = ["bt_nota", "bt_pluma", "bt_panal", "bt_nota", "bt_correcto", "bt_pluma"]
PISTAS = [dict(sfx="bt_jiggy", en=en, vol=.45) for _, en, _ in SECRETOS] + [
    dict(sfx=_ROTA[i % len(_ROTA)], en=e, vol=.45) for i, e in enumerate([
        "Hay un cartucho", "Un jefe que tenía demasiados", "Ya te contamos su historia", "estás ciego", "huevo culo", "Secret Exit",
        "su hijo Speccy", "Klungo cae del techo", "quién es Jinjo", "con trece", "pone: Eekum Bokum", "Falso", "la Kazooie de siempre",
        "Es Diddy Kong Racing", "Bienvenido a casa", "otra fuerza", "Tuvo que quitarle huesos", "se sortea en cada partida",
        "y esbirro que se replantea", "Falso: funciona", "El récord mundial", "se da en la cabeza", "era solo un chiste",
        "se congela sin avisar", "Juzga tú"])] + [
    dict(sfx="bt_jinjo", en="Estos son los cincuenta secretos", vol=.5),
    dict(sfx="bt_panal_skill", en="Llevamos veinticinco", vol=.45),
    dict(sfx="bt_guhuh", en="Nos vemos en el próximo secreto", vol=.55),
]

# Tira «dónde» al arrancar los secretos que no la llevan arriba (llena el hueco tras el rótulo; regla del 3-nov: sin tramos vacíos).
_DONDE = {
    49: [("chuffy", "TREN", "Chuffy"), ("old_king_coal", "REY", "Old King Coal")],
    44: [("banjo", "SOLO", "Banjo")],
    43: [("bullion_bill", "BAUTIZADO", "Bullion Bill"), ("old_king_coal", "BAUTIZADO", "Old King Coal")],
    37: [("titulo_jrl", "MUNDO", "Jolly Roger's Lagoon"), ("pawno", "USURERO", "Pawno")],
    36: [("tower_tragedy", "CONCURSO", "Tower of Tragedy"), ("xbox360", "VERSIÓN", "Xbox 360")],
    35: [("kirkhope", "MÚSICA", "Grant Kirkhope")],
    34: [("titulo_hfp", "MUNDO", "Hailfire Peaks"), ("sabreman", "EXPLORADOR", "Sabreman")],
    32: [("caja_bt", "SALIDA", "Banjo-Tooie (2000)")],
    31: [("cauldron_keep", "CORTADO", "Cauldron Keep")],
    28: [("kirkhope", "MÚSICA", "Grant Kirkhope"), ("rare_hq", "ESTUDIO", "Rare")],
    27: [("hag1", "JEFE FINAL", "Hag 1"), ("kirkhope", "MÚSICA", "Grant Kirkhope")],
    26: [("jamjars", "SARGENTO", "Jamjars")],
    24: [("titulo_hfp", "MUNDO", "Hailfire Peaks"), ("dragon_kazooie", "FORMA", "Kazooie dragón")],
    23: [("tower_tragedy", "CONCURSO", "Tower of Tragedy"), ("grunty", "PRESENTA", "Gruntilda")],
    22: [("titulo_tdl", "MUNDO", "Terrydactyland"), ("dream", "ORIGEN", "Dream")],
    17: [("titulo_jrl", "MUNDO", "Jolly Roger's Lagoon"), ("lord_woo", "JEFE", "Lord Woo Fak Fak")],
    13: [("caja_bt", "INTRO", "Banjo-Tooie")],
    12: [("klungo", "ESBIRRO", "Klungo")],
    9: [("titulo_jrl", "MUNDO", "Jolly Roger's Lagoon"), ("trotty", "CERDO", "Trotty")],
    8: [("expansion", "ACCESORIO", "Expansion Pak"), ("n64", "CONSOLA", "Nintendo 64")],
    5: [("jamjars", "SARGENTO", "Jamjars"), ("jamjars_silo", "SILO", "Su silo")],
    3: [("n64", "CARTUCHO", "Nintendo 64")],
}
_ANC = {n: en for n, en, _ in SECRETOS}
FX += [donde(_ANC[n], it, dur=3.6) for n, it in _DONDE.items()]

# Huecos > 4 s medidos con fx --seco (3-nov): una pegatina o ficha en cada uno.
FX += [
    cam("Y Japón se lo tomó", "logo_bt_jp", "Japón", x=.14, y=.66, dur=3.6),
    ficha("fue el primer mundo que diseñó", "Steve Malpass", "Venía del departamento de *pruebas*", sub="Su primer mundo", dur=4.6, x=.28),
    cam("Sale muy pocas veces", "jamjars", "Jamjars", x=.14, y=.66, dur=3.8),
    ficha("vista desde arriba", "Vista desde arriba", "Una forma *poco apta* para todo público", sub="Terrydactyland", dur=4.4, x=.28),
    peg("Si te gustó, suscríbete", "banjo", "Suscríbete", dur=4.2, x=.80, y=.60, tam=380),
]
# Segunda pasada de huecos (_huecos.py, regla del 3-nov: ningún tramo > 4 s sin pegatina ni MG).
FX += [
    aba([("breegull_bash", "Breegull Bash"), ("taxi_pack", "Taxi Pack"), ("shack_pack", "Shack Pack")], de="demasiados movimientos",
        a=("alguien nuevo|fin", .8), marcas=["demasiados", "movimientos", "para alguien"], nombre="movimientos", x=.70),
    cam("La entrada principal nunca", "gatehouse", "La entrada", x=.86, y=.66, dur=3.2),
    cam("En casa de Bottles, en Jinjo", "mrs_bottles", "Casa de Bottles", x=.14, y=.66, dur=3.4),
    cam("Klungo cae del techo", "gatehouse", "The Gatehouse", x=.14, y=.66, dur=4.0),
    cam("Una teoría de los fans", "vida_bk3", "Icono de vida", x=.86, y=.66, dur=3.8),
    vs("Te lo enseño encima del mapa", ("o casualidad|fin", .6), ["Te lo enseño", "y tú decides"],
       ("ISLE O' HAGS", "El contorno de la isla", "isla_mapa"), ("BANJO-KAZOOIE", "El icono de vida", "vida_bk3"), titulo="¿Se parecen?", marca=None, y=.44),
    cam("Todo el juego lo diseñaron", "rare_hq", "Rare", x=.86, y=.66, dur=3.6),
    cam(("nunca lo confirmó Treinta y tres", 2.0), "rare_hq", "Rare", x=.86, y=.66, dur=3.2),
    cam("Lo que murmura Mumbo", "mumbo", "Mumbo", x=.14, y=.66, dur=3.4),
    cam("el foso de ácido morado", "cauldron_keep", "Cauldron Keep", x=.14, y=.66, dur=3.2),
    cam("Treinta Jamjars", "jamjars_silo", "Silo de Jamjars", x=.14, y=.66, dur=3.0),
    cam(("Rare enseñó esas imágenes", 3.2), "dream", "Dream", x=.86, y=.66, dur=3.6),
    cam("Bienvenido a casa, Donkey", "dk64", "Donkey Kong 64", x=.86, y=.66, dur=5.0),
    cam("ya bastantes sustos dan", "minjo", "Minjo", x=.14, y=.66, dur=3.2),
    cam("Diecisiete Lord Woo", "woo_fak_fak", "Lord Woo Fak Fak", x=.86, y=.66, dur=3.6),
    aba([("banjo", "Banjo"), ("kazooie", "Kazooie"), ("mumbo", "Mumbo")], de="para presumir cuántos", a=("a la vez|fin", .6),
        marcas=["para presumir", "cuántos", "a la vez"], nombre="la demo"),
]
