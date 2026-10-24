# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Zelda: Majora's Mask: su historia y los 12 secretos QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming,
23-oct-2026). Fórmula de zelda_oot con el kit NUEVO `nucleo/mg_majora.py`: todo TRANSLÚCIDO con la interfaz del propio juego
(regla del usuario del 22-oct: nada de carteles opacos que tapen el video):
- PEGATINAS de cada personaje/objeto que nombra la voz (imágenes oficiales de zelda.fandom.com / Wikipedia en pegatinas/,
  fuentes en pegatinas/_fuentes.txt; bajar_pegatinas.py), chicas abajo a la izquierda, en fila cuando la voz enumera, ~1 de cada
  5 GRANDE del lado contrario.
- rótulo `puesto` = el cartel «Amanecer del primer día» (serifa blanca sobre humo) arriba; fichas = el cuadro de diálogo de N64 a
  la derecha, con el texto que se escribe letra a letra, SOLO con datos del guion.
- MG NUEVOS de ESTE guion: `reloj` (el reloj de 3 días del HUD), `ciclo` (Día 1 -> 2 -> 3 -> la luna cae -> Canción del Tiempo),
  `horario` (el cuaderno de los Bombers con Anju y Kafei), `rejilla` (las 24 máscaras -> la Fiera Deidad), `almas` (Darmani y
  Mikau se funden en su máscara).
- MAPAS REALES con ruta (regla del 23-oct): Termina (mapas/termina_3ds.png, arte oficial de Majora's Mask 3D) con el tema
  «majora» de mg_mapa y la FOTO real de cada región al llegar (regla «fotos en el mapa»): las cuatro regiones (lore) y las cinco
  etapas del duelo (n.º 1).
  python fab.py majora_mask fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py majora_mask fx         audio/fx.wav
"""
import os

import mg_majora as M

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .40     # fichas: a la derecha (el rótulo de puesto va arriba)

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


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=640):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.52, tam=tam)


def fila(en, items, y=.66, tam=330, dur=5.0):
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
    return dict(tipo="mg", fn=M.puesto(num, titulo), en=en, dur=dur, x=.5, y=.17, sale=.45, nombre=f"puesto {num}", ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def mapa(puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, "termina_3ds.png"), puntos, "majora", titulo=titulo, sub=sub,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa termina", ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa termina", ver=4.0)


# Termina (mapas/termina_3ds.png, coordenadas leídas con la rejilla): Ciudad Reloj al centro, pantano al sur, montañas al
# norte, la gran bahía al oeste e Ikana al este.
CIUDAD, PANTANO, MONTANA, BAHIA, IKANA = (.50, .48), (.50, .67), (.47, .19), (.25, .58), (.83, .40)
_P = _img
MASC = [os.path.join(_PEG, "mascaras", f"{i:02d}.png") for i in range(1, 25)]

FX = [
    # ================================================================ GANCHO
    grande("la banda sonora completa de Majora's Mask", "majora", "Majora's Mask (2000)", lado="der", dur=5.2, tam=560),
    ficha("Ciento once pistas", "Nintendo Music", "La banda sonora entera: *111 pistas*, 26 años después.",
          tipo="Octubre de 2026", dur=4.6),
    peg("con una luna que te mira desde el cielo", "luna", "La luna", tam=460, x=.80, y=.30),
    *fila("Un cartero que no puede huir", [
        ("cartero", "El cartero", None),
        ("darmani", "Una máscara con dueño", "unas máscaras que guardan"),
        ("microfono", "Un micrófono olvidado", "y un micrófono")], dur=6.0, tam=300),
    ficha("Así que hoy te cuento", "Majora's Mask", "Su historia, la de Termina y *12 secretos* que seguramente ignoraste.",
          tipo="Nintendo / Nintendo 64 / 2000", a=("que seguramente ignoraste|fin", 1.0)),

    # ================================================================ ORIGEN
    grande("a Eiji Aonuma le tocaba", "aonuma", "Eiji Aonuma", dur=5.0, tam=520),
    ficha("la que se llamaba Ura Zelda", "Ura Zelda", "Las mazmorras de Ocarina, *rehechas* para una expansión.",
          tipo="El encargo", dur=4.4),
    peg("Shigeru Miyamoto le dijo que sí", "miyamoto", "Shigeru Miyamoto", tam=420, x=.80, y=.60),
    ficha("Tenía que estar terminado en un año", "El reto", "Un juego nuevo en *un solo año*, con los modelos de "
          "*Ocarina of Time*.", tipo="La condición de Miyamoto", a=("en tres dimensiones de Ocarina of Time|fin", .6)),
    ficha("con un nombre provisional", "Zelda Gaiden", "*Zelda, la historia paralela*: el nombre provisional.",
          tipo="Febrero de 1999", a=("la historia paralela|fin", .8)),
    peg("La idea del tiempo salió de Yoshiaki Koizumi", "koizumi", "Yoshiaki Koizumi", tam=420),
    ficha("un juego de mesa de policías y ladrones", "Policías y ladrones", "Atrapar a un criminal en *una semana* de juego.",
          tipo="La idea de Koizumi", a=("en una semana de juego|fin", .8)),
    mg(M.ciclo(["Día 1", "Día 2", "Día 3", "La luna cae", "Canción del Tiempo"], "Una semana -> 3 días",
               titulo="El ciclo"),
       ("Al principio el ciclo de Majora's Mask", -.2), ("Así que se quedó en tres días|fin", .8),
       ["Al principio el ciclo", "demasiado largo", "no daba tiempo", "Así que se quedó", "en tres días"], "ciclo", y=.50),
    ficha("Corre, Lola, corre", "Corre, Lola, corre (1998)", "La misma carrera de *20 minutos*, una y otra vez.",
          tipo="Una de las influencias citadas", a=("hasta salvar a su novio|fin", .6)),
    grande("Era obligatorio el Expansion Pak", "expansion_pak", "Expansion Pak", lado="der", dur=5.6, tam=560),
    ficha("doblaba la memoria", "Expansion Pak", "De *4* a *8 megas* de memoria. En Japón, en el mismo paquete.",
          tipo="Obligatorio", a=("se vendía en el mismo paquete|fin", .6), x=.26),
    ficha("Salió en Japón en abril", "Majora's Mask", "Japón: *abril de 2000*. América: *26 de octubre*. Famitsu *37/40*, "
          "Metacritic *95*, más de *3 millones*.", tipo="El lanzamiento", a=("más de tres millones de copias|fin", 1.0)),

    # ================================================================ LORE
    peg("Link se va de Hyrule a caballo", "link_epona", "Link y Epona", tam=460),
    *fila("un Skull Kid con una máscara extraña", [
        ("skull_kid", "Skull Kid", None),
        ("tatl", "Tatl", "dos hadas"),
        ("tael", "Tael", "Tatl y Tael")], dur=5.6, tam=320),
    grande("lo convierte en un Deku", "link_deku", "Link Deku", lado="der", dur=5.0, tam=600),
    peg("Allí conoce al vendedor", "vendedor", "Vendedor de máscaras felices", tam=460),
    grande("la Máscara de Majora, un objeto", "majora", "La Máscara de Majora", lado="der", dur=4.8, tam=520),
    peg("está tirando la luna sobre Ciudad Reloj", "luna", "La luna", tam=480, x=.78, y=.32),
    mg(M.reloj("La luna caerá", [("Día 1", 72, "Amanecer del primer día"), ("Día 2", 48, "Amanecer del segundo día"),
                                 ("Día 3", 24, "Amanecer del último día"), ("Día 3", 6, "Horas finales")]),
       ("que caerá en tres días", -.2), ("Cada tres días, todo vuelve a empezar|fin", .5),
       ["que caerá en tres días", "justo cuando empieza el carnaval", "toca la Canción del Tiempo", "Así empieza el ciclo"],
       "reloj", y=.44),
    mapa([(*CIUDAD, "Ciudad Reloj", "inicio", _P("ciudad_reloj")), (.50, .58), (*PANTANO, "El pantano", "paso", _P("pantano")),
          (.52, .52), (.50, .40), (.48, .30), (*MONTANA, "Las montañas", "paso", _P("snowhead")), (.42, .32), (.36, .45),
          (*BAHIA, "La gran bahía", "paso", _P("bahia")), (.36, .52), (.50, .52), (.66, .48), (.76, .42),
          (*IKANA, "Valle de Ikana", "meta", _P("ikana"))],
         ("Para pararla, tiene que despertar a cuatro gigantes", -.3), ("y el valle de Ikana al este|fin", 1.4),
         ["que duermen en los templos de Termina", "El pantano del sur", "las montañas nevadas del norte",
          "la gran bahía del oeste", "y el valle de Ikana al este"], titulo="Termina", sub="Los cuatro gigantes", ajuste=.8, zoom=1.12),
    grande("Esos gigantes eran los amigos del Skull Kid", "skull_kid", "Skull Kid", lado="der", dur=5.4, tam=600),
    dict(tipo="destello", en="La máscara abandona al Skull Kid", dur=.5, fuerza=.7),
    peg("entra en la luna, y Link la sigue", "majora", "A la luna", tam=380),

    # ================================================================ 12 / EL CARTERO
    puesto("Número doce.", 12, "El hombre que no puede huir"),
    grande("el cartero sigue repartiendo cartas", "cartero", "El cartero", lado="der", dur=5.6, tam=620),
    ficha("Porque su horario no se lo permite", "El cartero", "Su horario manda: reparte *a la hora exacta*, pase lo que "
          "pase.", tipo="Ciudad Reloj", a=("a la hora exacta|fin", .6)),
    peg("Madame Aroma, la alcaldesa", "madame_aroma", "Madame Aroma", tam=440),
    peg("te regala su gorra de cartero", "cartero", "La gorra del cartero", tam=360, x=.80, y=.62),

    # ================================================================ 11 / CANCIONES OCULTAS
    puesto("En el once, las canciones", 11, "Las canciones que no salen en el menú"),
    peg("esconde dos canciones", "link_ocarina", "Ocarina del Tiempo", tam=460),
    ficha("al revés, el reloj se ralentiza", "Canción del Tiempo invertida", "El tiempo pasa a *un tercio* de su "
          "velocidad.", tipo="Nintendo 64", a=("a un tercio de su velocidad|fin", .8)),
    ficha("Y si tocas cada nota dos veces", "Canción del Doble Tiempo", "Salta a la *siguiente mañana* o la *siguiente "
          "noche*.", tipo="Cada nota, dos veces", a=("o la siguiente noche|fin", .8)),
    dict(tipo="destello", en="Un espantapájaros que baila", dur=.4, fuerza=.5),

    # ================================================================ 10 / ELLOS
    puesto("Número diez.", 10, "Lo que viene del cielo"),
    grande("En el rancho vive una niña, Romani", "romani", "Romani", dur=5.4, tam=560),
    ficha("Si te quedas a defender el granero", "El granero", "Aguantar con el arco *hasta el amanecer*. Premio: *una "
          "botella de leche*.", tipo="La primera noche", a=("una botella de leche|fin", .8)),
    dict(tipo="temblor", en="Ellos también se llevan a Romani", amp=8, dur=.8),
    peg("acompañar a su hermana Cremia", "cremia", "Cremia", tam=440),

    # ================================================================ 9 / EL GUARDADO
    puesto("En el nueve, el juego que te castigaba", 9, "El juego que te castigaba por guardar"),
    ficha("tienes que tocar la Canción del Tiempo", "Canción del Tiempo", "Guardas, vuelves al *primer día* y pierdes tus "
          "*rupias* y lo de usar y tirar.", tipo="El único guardado de verdad", a=("de usar y tirar|fin", .8)),
    peg("las estatuas de búho", "buho", "Estatua de búho", tam=380, x=.20, y=.60),
    ficha("Pero ese guardado era temporal", "Estatua de búho", "Guardado *temporal*: lo cargas una vez y *se borra*.",
          tipo="La otra opción", a=("y se borraba|fin", .6)),
    ficha("En la versión de tres de ese", "Majora's Mask 3D (2015)", "Búhos y estatuas que guardan *para siempre*; el "
          "cuaderno de los Bombers *se rellena solo*.", tipo="Nintendo 3DS", a=("se rellena solo|fin", .8)),

    # ================================================================ 8 / ANJU Y KAFEI
    puesto("Número ocho.", 8, "La misión más larga"),
    peg("Anju lleva el hotel", "anju", "Anju", tam=500),
    grande("Pero Kafei ha desaparecido", "kafei", "Kafei", lado="der", dur=4.8, tam=560),
    peg("lo convirtió en niño", "kafei_nino", "Kafei, de niño", tam=440, x=.80, y=.60),
    peg("le robó la Máscara del Sol", "mascara_sol", "Máscara del Sol", tam=380),
    mg(M.horario("Cuaderno de los Bombers", ["Día 1", "Día 2", "Día 3"],
                 [("Anju", [(0, "Espera a Kafei en el hotel"), (2, "Lo espera hasta el final")]),
                  ("Kafei", [(1, "Busca la Máscara del Sol"), (2, "Llega de madrugada")])]),
       ("tienes que seguirlos los tres días enteros", -.2), ("ocupa un ciclo completo|fin", 1.0),
       ["tienes que seguirlos", "a horas exactas", "Es la única misión", "del cuaderno de los Bombers", "un ciclo completo"],
       "bombers", y=.48),
    *fila("te llevas la máscara de Keaton", [
        ("kafei_nino", "Máscara de Keaton", None),
        ("cartero", "Gorra del cartero", "la gorra del cartero"),
        ("mascaras_g/16", "Máscara de los novios", "la máscara de los novios")], dur=5.0, tam=300),
    ficha("Se unen con sus máscaras", "Anju y Kafei", "Se unen en el hotel *a minutos* de que caiga la luna.",
          tipo="Amanecer del último día", a=("deciden recibirlo juntos|fin", 1.0)),

    # ================================================================ 7 / UN VIEJO CONOCIDO
    puesto("En el siete, un viejo conocido.", 7, "Un viejo conocido"),
    peg("el Skull Kid le dice a Link", "skull_kid", "Skull Kid", tam=440),
    ficha("huele igual que el niño hada", "Skull Kid", "Link *huele igual* que el niño hada que le enseñó una canción en "
          "el bosque.", tipo="Al final del juego", a=("una canción en el bosque|fin", .8)),
    grande("En Ocarina of Time, en el Bosque Perdido", "skull_kid_oot", "Skull Kid (Ocarina, 1998)", lado="der", dur=6.0,
           tam=600),
    peg("Ese niño hada era Link", "link", "Link", tam=440),
    ficha("Nintendo nunca lo ha dicho", "Una pista, no un dato", "El juego *deja la pista*; Nintendo nunca lo ha confirmado.",
          tipo="Lo que sabemos", dur=4.6),

    # ================================================================ 6 / LA FIERA DEIDAD
    puesto("Número seis.", 6, "La máscara más poderosa"),
    *fila("cuatro niños que llevan las máscaras", [
        ("nino_odolwa", "Odolwa", None), ("nino_goht", "Goht", "las máscaras de los jefes"),
        ("nino_gyorg", "Gyorg", "Corretean por el prado"), ("nino_twinmold", "Twinmold", "y te piden máscaras")], dur=5.0, tam=280),
    mg(M.rejilla("Las máscaras", 24, remate="20 que no transforman -> la Fiera Deidad",
                 icono=os.path.join(_PEG, "mascaras_g", "24.png"), iconos=MASC),
       ("las veinticuatro máscaras", -.3), ("la Máscara de la Fiera Deidad|fin", .8),
       ["las veinticuatro máscaras", "Necesitas las veinte", "la Máscara de la Fiera Deidad"], "mascaras", y=.48),
    grande("Link se convierte en un guerrero adulto", "link_fiera", "Link Fiera Deidad", lado="der", dur=6.0, tam=680),
    dict(tipo="destello", en="con una espada doble que lanza rayos", dur=.4, fuerza=.6),
    ficha("solo funciona en las peleas contra jefes", "Fiera Deidad", "En Nintendo 64, *solo contra los jefes*.",
          tipo="El truco", a=("no te la puedes poner|fin", .6)),

    # ================================================================ 5 / MÁSCARAS CON DUEÑO
    puesto("Número cinco.", 5, "Las máscaras que guardan a un muerto"),
    grande("Es Darmani, el héroe de los Goron", "darmani", "Darmani", dur=5.4, tam=560),
    mg(M.almas("Una máscara, un alma", [(_P("darmani"), os.path.join(_PEG, "mascaras_g", "12.png"), "Darmani",
                                        "Murió por un alud"),
                                       (_P("mikau"), os.path.join(_PEG, "mascaras_g", "18.png"), "Mikau",
                                        "Murió por los huevos de Lulu")]),
       ("Le tocas la Canción de Curación", -.2), ("Su lápida es su propia guitarra|fin", .6),
       ["Le tocas la Canción de Curación", "En la gran bahía pasa lo mismo"], "almas", y=.50),
    peg("su compañera Lulu", "lulu", "Lulu", tam=420, x=.83, y=.62),
    peg("Su lápida es su propia guitarra", "tumba_mikau", "La tumba de Mikau", tam=420, x=.17, y=.60),
    peg("vas por Termina con la cara de alguien", "link_goron", "Link Goron", tam=460, x=.80, y=.58),

    # ================================================================ 4 / LA MÁSCARA DEKU
    puesto("En el cuatro, ¿de quién era la máscara Deku?", 4, "¿De quién era la máscara Deku?"),
    peg("La primera transformación del juego", "link_deku", "Link Deku", tam=440),
    peg("el mayordomo del rey", "mayordomo", "El mayordomo Deku", tam=460, x=.80, y=.60),
    grande("llora frente a un árbol retorcido", "hijo_mayordomo", "El árbol retorcido", dur=5.4, tam=520),
    ficha("la Elegía del Vacío", "Elegía del Vacío", "Deja *una estatua de ti mismo*: una por cada forma de Link.",
          tipo="Valle de Ikana", a=("Una por cada forma de Link|fin", .6)),
    *fila("La estatua de Darmani", [
        ("darmani", "Darmani", None), ("mikau", "Mikau", "la de Mikau"), ("link", "Link", "la del propio Link"),
        ("hijo_mayordomo", "El hijo del mayordomo", "y la de Link Deku")], dur=5.5, tam=280),
    ficha("Nintendo nunca lo ha confirmado", "La máscara Deku", "Todo apunta a que es *el alma del hijo del mayordomo*.",
          tipo="Sin confirmar", a=("llevas su cara|fin", .8)),

    # ================================================================ 3 / BEN DROWNED
    puesto("Número tres. El cartucho", 3, "El cartucho maldito que nunca existió"),
    ficha("un usuario de 4chan contó", "Ben Drowned", "Un cartucho de una venta de garaje, con una partida a nombre de "
          "*BEN*.", tipo="Septiembre de 2010", a=("a nombre de Ben|fin", .8)),
    *fila("Un cuarto día que no existe", [
        ("ciudad_reloj", "Un cuarto día", None), ("link", "La estatua de Link", "y una estatua de Link")], dur=5.0,
         tam=320),
    ficha("Pero todo era ficción", "Ficción", "Lo escribió *Alex Hall* («Jadusable»): una historia de terror por "
          "capítulos que terminó en *2020*.", tipo="Juego de realidad alternativa", a=("octubre de dos mil veinte|fin", .8)),
    peg("Ningún otro Zelda daba tanto miedo", "majora", "Majora's Mask", tam=420),

    # ================================================================ 2 / EL MICRÓFONO
    puesto("Número dos.", 2, "Un micrófono que nunca usaste"),
    peg("Nintendo vendía un micrófono", "microfono", "El micrófono de N64", tam=420),
    ficha("Se usaba en Hey You", "El micrófono de N64", "Se usaba en *Hey You, Pikachu!* para hablarle a Pikachu.",
          tipo="Solo en Japón", a=("para hablarle a Pikachu|fin", .6)),
    ficha("soporte para ese micrófono", "Escondido en el código", "Sacar *fotos con tu voz* y *despertar a un Deku*.",
          tipo="Todas las versiones", a=("hablándole en japonés|fin", .6)),
    ficha("una variable que nunca toma el valor", "Desactivado", "Una variable que *nunca* toma el valor necesario: "
          "*24 años* escondido.", tipo="Por qué nadie lo usó", a=("sin que nadie lo usara|fin", .6)),
    ficha("En diciembre de dos mil veinticuatro", "Diciembre de 2024", "Un aficionado lo enciende con el *micrófono real*. "
          "Y funciona.", tipo="El hallazgo", a=("que te escuchaban|fin", 1.0)),

    # ================================================================ 1 / LAS CINCO ETAPAS
    puesto("Y llegamos al número uno.", 1, "La teoría que cambió Termina"),
    mapa([(*CIUDAD, "Negación", "inicio", _P("ciudad_reloj")), (.50, .58), (*PANTANO, "Ira", "paso", _P("rey_deku")),
          (.52, .52), (.50, .40), (.48, .30), (*MONTANA, "Negociación", "paso", _P("darmani")), (.42, .32), (.36, .45),
          (*BAHIA, "Depresión", "paso", _P("lulu")), (.36, .52), (.50, .52), (.66, .48), (.76, .42),
          (*IKANA, "Aceptación", "meta", _P("torre_piedra"))],
         ("Ciudad Reloj sería la negación", -.3), ("que ya no luchan contra su destino|fin", 1.2),
         ["Ciudad Reloj sería la negación", "El pantano sería la ira", "Las montañas nevadas serían la negociación",
          "La gran bahía, la depresión", "Y el valle de Ikana, la aceptación"], titulo="Las cinco etapas del duelo",
         sub="Una teoría de los fans", ajuste=.8, zoom=1.12),
    ficha("Ojo, todo esto es una teoría", "Teoría, no dato", "Aonuma solo habló de *tonos emocionales* en algunos "
          "episodios.", tipo="Lo que dijo Aonuma", a=("no que cada zona sea una etapa|fin", .6)),
    peg("Majora's Mask habla de perder a alguien", "skull_kid", "Skull Kid", tam=440),

    # ================================================================ CIERRE
    *fila("Un cartero puntual", [
        ("cartero", "El cartero", None), ("darmani", "Las máscaras", "unas máscaras con dueño"),
        ("microfono", "El micrófono", "un micrófono olvidado"), ("luna", "La luna", "una luna que nunca")], dur=4.2,
         tam=280),
    grande("Y salió de un reto imposible", "link_tatl", "Majora's Mask (2000)", lado="der", dur=5.0, tam=600),
    peg("la Máscara de la Fiera Deidad#2", "link_fiera", "Fiera Deidad", tam=420),
]
ROTULOS = []
# SFX: de la biblioteca (ElevenLabs casi sin saldo el 23-oct); uno distinto por momento (regla: nada de SFX repetidos)
SFX = {   # copiados de la biblioteca (`biblioteca sfx usar`), ninguno oído antes en Crónicas del gaming
    "campana": ("One deep ominous church bell toll with a long reverb tail, dark fantasy", 4),
    "reloj": ("Old mechanical alarm clock ticking in a quiet bedroom at night", 4),
    "fantasma": ("Ghostly whoosh passing by, airy spectral swoosh with a faint moan", 2),
    "ellos": ("Low ominous cinematic sting, deep brass swell with a dark rumble", 3),
    "magia": ("Magical sparkle shimmer swell rising into a warm soft chime", 2),
    "sello": ("Heavy rubber stamp slammed hard on a wooden desk, single thud", 1),
}
PISTAS = [
    dict(sfx="campana", en="que caerá en tres días", vol=.4),
    dict(sfx="ellos", en="llegan Ellos", vol=.4),
    dict(sfx="reloj", en="si te quedaban diez minutos para la luna", vol=.35),
    dict(sfx="magia", en="Link se convierte en un guerrero adulto", vol=.4),
    dict(sfx="fantasma", en="encuentras a un fantasma junto a una tumba", vol=.4),
    dict(sfx="sello", en="Pero todo era ficción", vol=.45),
]
