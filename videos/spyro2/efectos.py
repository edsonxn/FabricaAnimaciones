# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Spyro 2: su historia y los 30 secretos QUE IGNORASTE» (SECUENCIA YT, Crónicas del gaming, 31-oct-2026).
Kit TRANSLÚCIDO nucleo/mg_spyro.py con la interfaz del propio juego (cuadro de diálogo, gemas que giran, cifras doradas del HUD).
- `secreto` = rótulo con la gema + contador de esquina «N/30» durante todo el secreto (da ritmo en 25 min).
- MG del guion: pilones, mundos, codigo, katakana, anagrama, rueda, vagoneta, renombres, pantallas_negras, discos, trueque, relacion,
  notas, libreta, carteles, gemas, linea_tiempo, nombres.
- PEGATINAS reales (pegatinas/, bajar_pegatinas.py y capturas.py) variadas: silueta, banda, camafeo, abanico, legajo (nucleo/peg_estilos.py).
- MAPA REAL: solo existe la lámina «The World of Avalar» (mapas/avalar.jpg); de niveles no hay mapa en ninguna fuente.
- Citas del juego leídas en pantalla (verificacion_clips.md). SFX DEL JUEGO: sfx/sp_*.mp3. Comentarios: el canal no tiene nuevos (ESTADO.md).
  python fab.py spyro2 fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py spyro2 fx         audio/fx.wav
"""
import os

import mg_mapa as MP
import mg_spyro as S
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .42     # fichas: a la derecha (el rótulo de secreto va arriba)
TEMA = "spyro"

CAMARA = {}
FUNDIDO = {}


def P(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-5.0):
    return dict(tipo="mg", fn=S.pegatina(P(slug), titulo, tam, giro), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620, giro=-3.0):
    return peg(en, slug, titulo, dur=dur, x=.27 if lado == "izq" else .73, y=.52, tam=tam, giro=giro)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=820, encuadre=(0, 1.0)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con el video corriendo detrás."""
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


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


def ficha(en, titulo, texto, tipo=None, dur=6.0, a=None, x=_FX, y=_FY, ancho=820):
    d = dict(tipo="mg", fn=S.ficha(titulo, texto, tipo=tipo, ancho=ancho), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=4.0)


def mapa(puntos, de, a, marcas, titulo="Avalar", sub=None, ventana=False, x=.71, y=.44, **kw):
    """Mapa REAL con ruta (lámina del juego). Mundos: Summer Forest (.21,.26), Autumn Plains (.46,.70), Winter Tundra (.79,.38)."""
    puntos = [p[:4] + (P(p[4]),) if len(p) > 4 else p for p in puntos]
    fn = MP.mapa(os.path.join(_MAP, "avalar.jpg"), puntos, TEMA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa avalar", ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa avalar", ver=4.0)


def secreto(en, num, titulo, hasta):
    """Rótulo del secreto + contador de esquina hasta que empieza el siguiente."""
    return [dict(tipo="mg", fn=S.puesto(num, titulo), en=(en, -.1), dur=3.8, x=.5, y=.14, sale=.45, nombre=f"aviso secreto {num}", ver=1.4),
            dict(tipo="mg", fn=S.hud(31 - num), de=en, a=(hasta, -.45), x=.915, y=.075, sale=.3, nombre=f"aviso hud {num}", ver=1.0)]


_SF, _AP, _WT = (.21, .26), (.46, .70), (.79, .38)

FX = [
    # ================================================================ GANCHO
    grande("una moneda dorada con la cara", "cap_moneda", "La moneda dorada", lado="der", dur=5.6, tam=640),
    peg("Hay un monje que le pide", "cap_ned", "Brother Ned", x=.27, y=.56, tam=560, dur=5.6, giro=-3),
    aba([("f_catabatus", "Catabatus"), ("f_fistus", "Mister Fistus"), ("f_wuss", "Wuss")],
        ("Hay un libro de monstruos", -.1), ("todos los retos escondidos|fin", .4), ["Hay un libro", "nunca llegaron", "todos los retos"], "abanico faunus"),
    peg("dentro del disco había otro juego", "cap_ctr", "Otro juego en el disco", x=.73, y=.54, tam=600, dur=5.0, giro=4),
    peg("Spyro 2 salió en noviembre de 1999", "caja2", "Spyro 2 (1999)", x=.82, y=.56, tam=480, dur=6.4, giro=4),
    ficha("Y veintisiete años después", "1999", "Veintisiete años después, *el mejor de la saga* para muchos.", tipo="Primera PlayStation", dur=5.4, x=.28),
    mg(S.libreta(["Cómo se *hizo*", "Por qué tiene *tres nombres*", "Los *30 secretos* que ignoraste"], "Hoy, en este video", w=1160),
       ("Hoy te cuento cómo se hizo", -.1), ("seguramente ignoraste|fin", .9), ["cómo se hizo", "tiene tres nombres", "los 30 secretos"], "libreta hoy"),

    # ================================================================ HISTORIA 1: EL ORIGEN
    peg("Un estudio de Burbank", "insomniac", "Insomniac Games", x=.18, y=.60, tam=380, dur=5.4),
    ficha("Un estudio de Burbank", "Insomniac Games", "Burbank, California. Fundador: *Ted Price*.", dur=5.4),
    sil("En 1998 lanzaron Spyro the Dragon", "spyro", "Spyro", "Spyro the Dragon, 1998", dur=6.6, lado="der"),
    ficha("Eso venía de un motor", "El motor de Alex Hastings", "Lo *cercano*, nítido. Lo *lejano*, simplificado sin que lo notaras.",
          tipo="Detalle según la distancia", a=("sin que lo notaras|fin", .6), x=.28),
    ficha("casi todo consistía en recoger cosas", "El problema", "Casi todo era *recoger cosas*.", dur=4.0),
    ficha("Según el documental de Reliable Rhubarb", "Reliable Rhubarb", "El documental de la saga: la secuela empezó *al terminar el primero*.",
          tipo="Fuente de esta parte", dur=6.0),
    peg("Se llamaba, simplemente, Spyro II", "spyro2_logo", "Spyro II", x=.2, y=.58, tam=420, dur=3.6),
    ficha("Y la meta la resumió Ted Price", "Ted Price", "Más *reto*. Más *profundidad*. Más *variedad*.", tipo="La meta de la secuela",
          a=("y más variedad|fin", .8), x=.5, y=.40),
    mg(S.linea_tiempo([("1998", "Spyro the Dragon"), ("Después", "Empieza Spyro II"), ("E3 1999", "Lo enseñan al mundo")], "Así empezó", w=1500),
       ("En el E3 de 1999", -.1), ("gente que le pedía favores|fin", .6), ["En el E3 de 1999", "lo enseñaron", "Ya no era un dragón"], "linea origen", y=.74),

    # ================================================================ HISTORIA 2: AVALAR
    peg("irse de vacaciones a Dragon Shores", "cap_shores", "Dragon Shores", x=.75, y=.56, tam=520, dur=4.2, giro=3),
    peg("no llegan a la playa", "avalar", "Avalar", x=.5, y=.72, tam=520, dur=3.6),
    sil("invadido por un hechicero enano", "ripto", "Ripto", "Hechicero enano", dur=5.2, lado="der"),
    *[peg("Y va acompañado de Crush y Gulp", "crush", "Crush", x=.14, y=.62, tam=330, dur=5.6),
      peg("Crush y Gulp, dos criaturas", "gulp", "Gulp", x=.34, y=.62, tam=330, dur=5.0, giro=4)],
    mapa([(_SF[0], _SF[1], "Summer Forest", "inicio", "cap_summer"), (.33, .47), (_AP[0], _AP[1], "Autumn Plains", "paso", "cap_autumn"), (.64, .60),
          (_WT[0], _WT[1], "Winter Tundra", "meta", "cap_winter")],
         ("Lo que cambió fue todo lo demás", -.1), ("y Winter Tundra|fin", .9), ["tres mundos principales", "Summer Forest", "Autumn Plains", "Winter Tundra"],
         titulo="El mundo de Avalar", sub="Lámina del juego"),
    mg(S.gemas("Por completar", [(64, "Orbes, los retos aparte"), (10000, "Gemas en todo el juego", "10 000")], w=1000),
       ("Cada nivel tiene un talismán", -.1), ("y diez mil gemas|fin", .9), ["Hay sesenta y cuatro orbes", "y diez mil gemas"], "gemas orbes", y=.62),
    ficha("Cada nivel tiene un talismán", "Talismán y orbes", "El talismán es *la historia*. Las orbes, *retos aparte*.", x=.5, y=.30, dur=5.0),
    mg(S.libreta(["*Nadar*", "*Trepar* escaleras", "Dar *cabezazos*"], "Spyro aprendió", w=760), ("Spyro aprendió a nadar", -.1), ("a dar cabezazos|fin", 2.6),
       ["a nadar", "a trepar", "a dar cabezazos"], "libreta habilidades", y=.58, x=.28),
    ficha("Lo de nadar ya estaba planeado", "Spyro the Dragon", "Nadar *ya estaba planeado*: se cayó por falta de tiempo.", a=("falta de tiempo|fin", .8)),
    mg(S.pilones(), ("Y estaban los pilones", -.1), ("o el supervuelo|fin", .9),
       ["Cada enemigo derrotado", "la supercarga", "la supercongelación", "o el supervuelo"], "pilones"),
    ficha("Hay fans con una teoría oscura", "Teoría de fans", "Si orbes y pilones funcionan con *espíritus*, los buenos de Avalar tienen algo que explicar.",
          tipo="No confirmado", a=("bastante que explicar|fin", .6), x=.5, y=.40, ancho=980),
    sil("aparecieron Hunter", "hunter", "Hunter", "Se cree muy listo", dur=4.0, lado="izq"),
    sil("y Elora, una fauna", "elora", "Elora", "Lo es", dur=3.2, lado="der"),
    sil("También Moneybags", "moneybags", "Moneybags", "Te cobra casi por respirar", dur=6.4, lado="der"),
    ficha("La inflación hecha personaje", "Moneybags", "*La inflación* hecha personaje.", dur=2.8, x=.28, y=.36),

    # ================================================================ HISTORIA 3: LA MÚSICA Y LAS ESCENAS
    sil("La compuso Stewart Copeland", "copeland", "Copeland", "Stewart Copeland, The Police", dur=6.0, lado="izq", encuadre=(0, .8)),
    peg("el baterista de The Police", "police", "The Police", x=.76, y=.58, tam=520, dur=4.4, giro=3),
    ficha("Fue uno de los primeros músicos de rock", "Rock en un videojuego", "De los primeros músicos de rock *contratados para un videojuego*.", dur=5.2, x=.28),
    ficha("Le daban trucos para pasearse", "El método de Copeland", "Trucos para recorrer cada nivel, lo jugaba y *componía lo que sentía ahí*.",
          a=("sobre lo que sentía ahí|fin", .7)),
    *[peg("Summer Forest suena a verano", "cap_summer", "Summer Forest", x=.17, y=.60, tam=460, dur=5.6),
      peg("y Scorch suena a desierto", "cap_scorch", "Scorch", x=.83, y=.60, tam=460, dur=4.2, giro=4)],
    ficha("Oliver Wade, por su parte", "Oliver Wade", "Las escenas de entrada y salida de cada nivel, *sin storyboard*.", tipo="Según el documental",
          a=("sin storyboard|fin", .9)),
    ficha("Había otro truco de magia", "Boundary Break", "Shesez sacó la cámara de su sitio: así *disimulan la carga* los portales.",
          tipo="El truco de los portales", a=("la carga de cada nivel|fin", .8)),
    ficha("hubo una cosa que no les dio tiempo", "Sin tiempo", "Nunca probaron los minijuegos *con jugadores de verdad*.", tipo="Según el documental",
          a=("Ya vamos a llegar a eso|fin", .6), x=.5, y=.40),

    # ================================================================ HISTORIA 4: LANZAMIENTO
    mg(S.nombres([("EE. UU.", "Ripto's Rage"), ("Europa", "Gateway to Glimmer"), ("España", "En busca de los talismanes"),
                  ("Japón", "Spyro × Sparx: Tondemo Tours")]),
       ("Spyro 2 salió el 2 de noviembre", -.1), ("Tondemo Tours|fin", 1.0), ["con el nombre de Ripto's Rage", "En Europa se llamó", "En España", "Y en Japón"],
       "nombres", y=.56),
    ficha("¿Por qué tantos nombres?", "¿Por qué?", "*Tres explicaciones*, y no coinciden.", dur=4.4),
    ficha("Una versión europea del 15 de septiembre", "15 de septiembre de 1999", "Versión europea, todavía con el logo *Ripto's Rage*.",
          tipo="El cambio fue tardío", a=("el logo de Ripto's Rage|fin", .8)),
    grande("Con la PocketStation", "pocketstation", "PocketStation", lado="izq", dur=7.6, tam=520),
    ficha("podías desbloquear Sparx Adventure", "Sparx Adventure", "Un minijuego para *criar a tu libélula*.", tipo="Solo en Japón", a=("criar a tu libélula|fin", 1.0)),
    mg(S.notas([("IGN", 8.8, "8,8"), ("GameSpot", 8.6, "8,6"), ("GameRankings", 8.7, "87 %")]),
       ("La crítica lo recibió muy bien", -.1), ("en un 87 por ciento|fin", .9), ["IGN", "GameSpot", "GameRankings"], "notas", y=.56),
    mg(S.gemas("Copias vendidas", [(1000000, "Solo en EE. UU., diciembre de 1999", "1 000 000"), (3400000, "En todo el mundo", "3 400 000")], w=1160),
       ("Para diciembre de 1999", -.1), ("en todo el mundo|fin", .9), ["un millón de copias", "los tres millones"], "gemas ventas", y=.60),
    ficha("Pero lo mejor de este juego no está en las cifras", "Los secretos", "Del *treinta* al *uno*.", tipo="Vamos allá", dur=5.4, x=.5, y=.36),

    # ================================================================ 30 SECRETOS
    *secreto("Número treinta", 30, "Dos niveles, una sola canción", "Número veintinueve"),
    mapa([(_SF[0], _SF[1], "Idol Springs", "inicio", "cap_idol"), (.34, .50), (_AP[0], _AP[1], "Fracture Hills", "meta", "cap_fracture")],
         ("Idol Springs y Fracture Hills", -.1), ("el mismo tema musical|fin", .8), ["Idol Springs", "Fracture Hills"], titulo="Mundos distintos", ventana=True),
    ficha("El remake sí los separó", "Reignited Trilogy", "Sí los separó, con *dos mezclas distintas*.", dur=5.4, x=.28),

    *secreto("Número veintinueve", 29, "El dragón cabezón", "Número veintiocho"),
    mg(S.codigo([("arriba", 4), ("R1", 4), "cir"], "Modo cabezón", "Cabeza gigante"), ("Pausa el juego", -.1), ("Y a Spyro le sale|fin", 2.6),
       ["Pausa el juego", "Y a Spyro le sale"], "codigo cabezon", y=.72),

    *secreto("Número veintiocho", 28, "El truco que ya estaba en el prototipo", "Número veintisiete"),
    mg(S.codigo([("cir", 4), "cua"], "Todas las habilidades", "Todo desbloqueado"), ("Si en la pausa haces círculo", -.1), ("todas las habilidades del juego|fin", .8),
       ["círculo cuatro veces", "obtienes todas"], "codigo habilidades", y=.70),
    mg(S.carteles([("Julio de 1999", "Triángulo ×4 + círculo"), ("Agosto de 1999", "Círculo ×4 + cuadrado")], "El código en los prototipos", w=1200),
       ("Ese mismo código ya estaba", -.1), ("triángulo cuatro veces y círculo|fin", .8), ["en el prototipo de agosto", "En el de julio"], "carteles codigo", y=.68),
    ficha("Ese prototipo incluso tenía un código", "Ver créditos", "El juego *se colgaba*: los créditos aún no existían.", tipo="Prototipo de agosto de 1999",
          a=("todavía no existían|fin", .7)),

    *secreto("Número veintisiete", 27, "Moneybags, traficante de armas", "Número veintiséis"),
    sil("Todos recordamos a Moneybags", "moneybags", "Moneybags", dur=6.0, lado="izq"),
    grande("En Autumn Plains, al abrirte el portal", "cap_autumn", "El portal de Zephyr", lado="der", dur=5.6, tam=640),
    ficha("nunca le pagaron las bombas", "Moneybags", "«Those darn birds in Zephyr never paid me for all the *bombs and TNT barrels*…»",
          tipo="Autumn Plains", dur=6.0, x=.28),
    ficha("el propio Ripto presume", "Ripto", "«I persuaded that fat bear Moneybags to *sell me a few bombs*.»", tipo="Winter Tundra",
          a=("venderle unas bombas|fin", 1.0), x=.28),
    mg(S.libreta(["Un *condominio* en Hurricos", "Una *casa* en Aquaria Towers", "Hamburguesas de *lagarto* en Skelos"], "Los planes de Moneybags", w=1100),
       ("Y lo que gana lo tiene bien planeado", -.1), ("de lagarto en Skelos|fin", 1.0), ["un condominio", "casa en Aquaria", "un puesto de hamburguesas"], "libreta moneybags"),
    ficha("Tampoco es que lo disimule", "Moneybags", "«Say 'hi' to *Ripto* if you see him.»", tipo="Portal de Shady Oasis", a=("salúdame a Ripto si lo ves|fin", 1.0), x=.5, y=.36),

    *secreto("Número veintiséis", 26, "El hockey nació en la oficina", "Número veinticinco"),
    ficha("En Colossus, un monje te reta", "Brother Kipp", "«The first to score *5 goals* wins.»", tipo="Colossus", dur=6.0),
    peg("En Colossus, un monje te reta", "cap_colossus", "Colossus", x=.18, y=.62, tam=440, dur=5.0),
    ficha("Salió de los partidos de hockey", "De la oficina al juego", "Salió de los partidos de hockey *del propio equipo*.", dur=5.2, x=.28),

    *secreto("Número veinticinco", 25, "Elora, la centauro que no cupo", "Número veinticuatro"),
    sil("Según lo que contó Oliver Wade", "elora", "Elora", "Iba a ser centauro", dur=7.0, lado="izq"),
    ficha("Pero un cuerpo de caballo", "Oliver Wade", "Un cuerpo de caballo pedía *demasiados polígonos*.", dur=4.6),
    mg(S.anagrama("CAROLINE", "ELORA", pie="Carolina Trujillo, de Insomniac"), ("Y su nombre salió", -.2), ("del equipo de Insomniac|fin", .9),
       ["Y su nombre salió", "reordenar letras"], "anagrama", y=.60),

    *secreto("Número veinticuatro", 24, "Las alas mal puestas", "Número veintitrés"),
    grande("En el primer juego, las alas", "spyro", "Las alas de Spyro", lado="izq", dur=7.4, tam=640),
    ficha("Craig Stitt, uno de sus artistas", "Craig Stitt", "Corrigió las *alas* para esta secuela.", tipo="Artista", dur=6.0),

    *secreto("Número veintitrés", 23, "Bob Esponja hace de Spyro", "Número veintidós"),
    cam("Sale Carlos Alazraqui", "alazraqui", "Carlos Alazraqui", dur=3.4, x=.14, y=.66, foco=(.5, .3, 1.4)),
    grande("y entra Tom Kenny", "kenny", "Tom Kenny", lado="der", dur=4.6, tam=540),
    mg(S.relacion(("Tom Kenny", P("kenny")), [("Spyro", P("spyro")), ("El Profesor", P("profesor")), ("Electrolls", P("electroll"))], "Una sola voz"),
       ("Y según la wiki de la saga", -.1), ("el parecido es sospechoso|fin", .7), ["según la wiki", "al Profesor", "a los Electrolls"], "relacion kenny"),

    *secreto("Número veintidós", 22, "Un solo actor para los dos bandos", "Número veintiuno"),
    mg(S.relacion(("Gregg Berger", P("berger")), [("Ripto", P("ripto")), ("Hunter", P("hunter"))], "Dos bandos, una voz"),
       ("Según esa misma wiki", -.1), ("hablando consigo mismo|fin", .8), ["Gregg Berger", "la voz de Ripto", "la de Hunter"], "relacion berger"),
    ficha("Una especie de terapia", "Gregg Berger", "Terapia con *presupuesto de Sony*.", dur=3.6, x=.5, y=.40),

    *secreto("Número veintiuno", 21, "El almuerzo de Gulp", "Número veinte"),
    peg("Gulp se traga el cetro", "cap_cetro", "El cetro de Ripto", x=.27, y=.56, tam=580, dur=5.0, giro=-3),
    ficha("Y Ripto le grita", "Ripto", "«You imbecile! *You ate my scepter*.»", tipo="Primera cinemática", a=("te comiste mi cetro|fin", 1.0)),
    sil("en la escena en que le da de comer", "gulp", "Gulp", dur=5.0, lado="der"),
    ficha("Y solo después de vencer a Gulp", "Ripto", "«This is just what I need for a *new scepter*!»", tipo="Tras vencer a Gulp", a=("El juego no se olvidó|fin", .8), x=.28),

    *secreto("Número veinte", 20, "La cantante que Europa nunca oyó", "Número diecinueve"),
    grande("En Ripto's Arena, la versión americana", "cap_arena", "Ripto's Arena", lado="izq", dur=5.6, tam=560),
    mg(S.carteles([("EE. UU.", "Con voz de ópera"), ("Europa", "Sin voz")], "La música de Ripto's Arena", w=1100), ("lleva una voz de ópera", -.2), ("Escucha la diferencia|fin", 1.0),
       ["lleva una voz", "en la versión europea"], "carteles arena", y=.30),
    ficha("Es, según el canal Calcom", "Calcom", "El *único nivel* con música distinta entre regiones.", tipo="Sin explicación oficial", a=("ninguna explicación oficial|fin", .8)),

    *secreto("Número diecinueve", 19, "La música de las demos", "Número dieciocho"),
    *[peg("Sunny Beach y Skelos Badlands", "cap_sunny", "Sunny Beach", x=.17, y=.60, tam=420, dur=5.0),
      peg("Skelos Badlands tienen", "cap_skelos", "Skelos Badlands", x=.83, y=.60, tam=420, dur=4.6, giro=4)],
    ficha("Es un regalo para los oídos", "La demo", "La versión larga sonaba en la demo: *el juego final la recortó*.", dur=5.6),
    mg(S.libreta(["Minijuego de *Skelos Badlands*", "Minijuego de *Sunny Beach*", "Minijuego de *Hurricos*", "*Crystal Glacier*, versión temprana"], "Música en los prototipos", w=1100),
       ("Y los prototipos guardan más", -.1), ("la música de Crystal Glacier|fin", .9), ["para Skelos Badlands", "Sunny Beach y Hurricos", "y Hurricos", "una versión temprana"],
       "libreta prototipos"),

    *secreto("Número dieciocho", 18, "Los jinetes amish de delfines", "Número diecisiete"),
    ficha("Chad Dezern contó en el documental", "Chad Dezern", "Jinetes *amish* montados en *delfines*.", tipo="Según el documental", a=("montados en delfines|fin", .8)),
    peg("Chad Dezern contó en el documental", "cap_aquaria", "Aquaria Towers", x=.18, y=.60, tam=460, dur=5.0),
    ficha("Y la parte de arriba del nivel", "Aquaria Towers", "La parte de arriba venía de un *mundo submarino* del primer Spyro.", a=("todo se reutiliza|fin", .5), x=.28),

    *secreto("Número diecisiete", 17, "El volcán de papel", "Número dieciséis"),
    grande("Magma Cone se presentó en papel", "cap_magma", "Magma Cone", lado="der", dur=5.6, tam=560),
    ficha("Según contó Michael John", "Michael John", "Papel cuadriculado y un *volcán de papel*.", dur=6.2, x=.28),
    ficha("Skelos Badlands, por cierto", "Skelos Badlands", "El *primer nivel* creado para el juego.", tipo="Lo hizo Craig Stitt", dur=5.4),

    *secreto("Número dieciséis", 16, "Los problemas con la vagoneta", "Número quince"),
    mg(S.vagoneta(), ("Breeze Harbor, cincuenta engranajes", -.1), ("que no perdona|fin", 1.0), ["Breeze Harbor", "que no perdona"], "vagoneta", y=.64),
    peg("Y si vuelves a hablarle a Fisher", "cap_fisher", "Fisher", x=.26, y=.58, tam=560, dur=5.6, giro=-3),
    ficha("te suelta", "Fisher", "«*Trouble with the trolley*, eh?»", tipo="Breeze Harbor", a=("Como si no lo supiera|fin", .8)),
    ficha("Según el documental, pudo salir así de cruel", "Sin probar", "Adición *de última hora*, y nunca se probó con usuarios.", tipo="Según el documental",
          a=("nunca se probó con usuarios|fin", .7), x=.5, y=.38),
    peg("Si de niño lloraste aquí", "gear_reto", "Gear Grab", x=.76, y=.56, tam=480, dur=4.8, giro=4),

    *secreto("Número quince", 15, "Los niveles se llamaban de otra forma", "Número catorce"),
    mg(S.renombres([("Sparkle", "Glimmer"), ("Colossus Springs", "Idol Springs"), ("Aquaria Beach", "Sunny Beach"), ("Zephyr Harbor", "Breeze Harbor"),
                    ("Mystic City", "Cloud Temples")]), ("Durante el desarrollo", -.1), ("Y Cloud Temples, Mystic City|fin", 1.0),
       ["Glimmer se llamó", "e Idol Springs", "Sunny Beach era", "Breeze Harbor, Zephyr", "Y Cloud Temples"], "renombres", y=.55),
    mg(S.carteles([("Scorch", "Dunes y Oasis"), ("Metropolis", "Acres y Spires")], "Iban por parejas", w=1000), ("Iban por parejas", -.1), ("Metropolis Spires|fin", 1.4),
       ["Scorch Dunes", "Metropolis Acres"], "carteles parejas", y=.68),

    *secreto("Número catorce", 14, "El nombre que se les olvidó cambiar", "Número trece"),
    ficha("En Zephyr, el soldado Romeo", "Private Romeo", "«Now we can take our honeymoon in *Colossus Springs*…»", tipo="Zephyr", a=("Es el nombre viejo de Idol Springs|fin", .6)),
    peg("Y en Cloud Temples, el mago Murgen", "cap_murgen", "Murgen", x=.26, y=.58, tam=560, dur=5.6, giro=-3),
    ficha("te da un recuerdo de la tienda", "Murgen the Wizard", "«…a souvenir from the *Mystic City gift shop*.»", tipo="Cloud Temples", a=("el nombre viejo de ese nivel|fin", .7)),
    peg("Hasta en Crystal Glacier", "cap_widgie", "Widgie", x=.26, y=.58, tam=560, dur=7.0, giro=-3),
    ficha("dice que su jefe tiene las entradas", "Widgie", "«…tickets to tonight's hockey game in *Colossus Valley*!»", tipo="Crystal Glacier", a=("sin enterarte de nada|fin", .6)),

    *secreto("Número trece", 13, "Lo dejamos listo para noviembre", "Número doce"),
    ficha("Según Hidden Palace", "Prototipo de julio de 1999", "Moneybags: Canyon Speedway sigue en obras, *listo para noviembre*.", tipo="Hidden Palace",
          a=("El oso hablándote|fin", .4)),
    peg("Según Hidden Palace", "cap_canyon", "Canyon Speedway", x=.18, y=.60, tam=440, dur=6.0),
    mapa([(_WT[0], _WT[1], "Winter Tundra", "meta", "cap_winter")], ("En esa versión, varios niveles", -.1), ("usa el menú de pausa si quieres irte|fin", .7),
         ["varios niveles"], titulo="Sin salida", ventana=True),

    *secreto("Número doce", 12, "Las gemas que no daban la cuenta", "Número once"),
    mg(S.gemas("Gemas del juego", [(10000, "Juego final", "10 000"), (9991, "Prototipo de agosto de 1999", "9 991")], w=1080), ("El juego final tiene diez mil", -.1),
       ("nueve mil novecientas noventa y una|fin", 1.0), ["diez mil gemas", "tenía nueve mil"], "gemas prototipo", y=.60),
    *[peg("Zephyr traía una de más", "cap_zephyr", "Zephyr: una de más", x=.17, y=.60, tam=420, dur=5.0),
      peg("a Robotica Farms le faltaban", "cap_robotica", "Robotica Farms: faltaban", x=.83, y=.60, tam=420, dur=4.4, giro=4)],
    ficha("Y había sesenta y cinco orbes", "Orbes", "*65* en lugar de 64.", dur=3.6, x=.5, y=.30),

    *secreto("Número once", 11, "El juego sin final", "Número diez"),
    grande("Ripto's Arena ni siquiera existía", "cap_arena", "Aún no existía", lado="der", dur=5.0, tam=520),
    ficha("A cuatro meses de salir", "Julio de 1999", "A cuatro meses de salir, *sin último nivel*.", dur=5.0, x=.28),
    ficha("el marcador del hockey usaba discos", "Hockey", "Marcador con *discos rojos y azules*, no con las cabezas.", tipo="Prototipo de julio", dur=5.4),
    *[cam("el que te explicaba la cámara era el Profesor", "profesor", "El Profesor", dur=4.6, x=.14, y=.68),
      cam("un trabajo que luego se quedó Hunter", "hunter", "Hunter", dur=3.0, x=.31, y=.68)],

    *secreto("Número diez", 10, "Elora iba a contarlo todo", "Número nueve"),
    sil("En el prototipo de agosto de 1999, las escenas", "elora", "Elora", "Diálogo cortado", dur=7.0, lado="der"),
    ficha("Hurricos, por ejemplo", "Elora, diálogo cortado", "Hurricos: el hogar de los *Electrolls*, que dan energía a Avalar.", tipo="Prototipo", dur=7.0, x=.28),
    peg("Hurricos, por ejemplo", "electroll", "Electrolls", x=.60, y=.62, tam=340, dur=6.4, giro=4),
    ficha("Y los Water Workers", "Elora, diálogo cortado", "Water Workers: vaciaron unas cuevas y levantaron *fábricas sobre el coral*.", a=("encima del coral|fin", .7), x=.28),
    ficha("También te aclaraba", "Elora, diálogo cortado", "«…*scaring the bubbles* out of each other.»", tipo="Caballitos de mar", a=("Un dato vital que nos perdimos|fin", .7)),

    *secreto("Número nueve", 9, "La guerra que empezó Ripto", "Número ocho"),
    mapa([(_AP[0], _AP[1], "Breeze Harbor y Zephyr", "peligro", "cap_breeze")], ("En Breeze Harbor y Zephyr", -.1), ("y los Breeze Builders|fin", .8),
         ["dos pueblos"], titulo="Autumn Plains", ventana=True),
    peg("los Land Blubbers", "landblubber", "Land Blubber", x=.18, y=.62, tam=360, dur=4.6),
    ficha("Pero ese diálogo cortado de Elora", "Elora, diálogo cortado", "«They got along fine *until Ripto arrived*.»", tipo="Prototipo", a=("con menos trabajo|fin", .8)),
    sil("ella sospecha que los enfrentó", "ripto", "Ripto", dur=3.8, lado="izq"),

    *secreto("Número ocho", 8, "Kill the yeti", "Número siete"),
    ban("Brother Ned, te pide", "cap_ned", "Brother Ned", "Colossus", foco=(.5, .42, 1.3), dur=5.0, y=.74),
    mg(S.carteles([("Texto en pantalla", "«…torch that yeti.»"), ("Voz", "«…kill that yeti.»")], "Lo que dice el monje", w=1200),
       ("Si lees el cuadro de texto", -.1), ("Dice kill, mátalo|fin", 1.2), ["Si lees el cuadro", "Dice kill"], "carteles kill", y=.30),
    ficha("Un monje vegetariano", "Brother Ned", "«Even though I'm a *vegetarian*…»", tipo="Censura a medias", a=("una censura a medias|fin", .6)),

    *secreto("Número siete", 7, "El cumpleaños de Hunter", "Número seis"),
    mapa([(_WT[0], _WT[1], "Winter Tundra", "meta", "cap_winter")], ("Antes de la mazmorra de Crush", -.1), ("unas coordenadas|fin", .6), ["el Profesor estaba", "El Profesor estaba"],
         titulo="El superportal", ventana=True),
    peg("El Profesor estaba probando", "profesor", "El Profesor", x=.18, y=.62, tam=380, dur=5.0),
    sil("Y Hunter suelta", "hunter", "Hunter", dur=5.4, lado="izq"),
    mg(S.rueda("22475", "Las coordenadas del portal", "Es su cumpleaños", w=1000), ("Y Hunter suelta", -.1), ("Es mi cumpleaños|fin", 1.4),
       ["veintidós", "Es mi cumpleaños"], "rueda", x=.73, y=.55),
    ficha("Una guerra entera por usar", "Seguridad informática", "Una guerra entera por usar *tu cumpleaños como clave*.", a=("la seguridad informática|fin", .7), x=.5, y=.38),

    *secreto("Número seis", 6, "Ripto sale de Spyro", "Número cinco"),
    mg(S.katakana(), ("El logo japonés del juego", -.1), ("su propio nombre mal leído|fin", .7), ["El logo japonés", "Los artistas lo miraban"], "katakana", y=.54),
    ficha("Lo publicó la revista oficial", "Revista oficial de PlayStation", "Publicado en *1999*.", tipo="La anécdota", dur=4.4),
    leg("ripto", "Ripto", ["Pequeño a propósito", "Contraste con Gnasty Gnorc", "Un solo cuernito"], ("Wade, según el documental", -.1), ("un solo cuernito en la cabeza|fin", .7),
        marcas=["lo dibujó pequeño"], x=.22),
    peg("el enorme Gnasty Gnorc", "gnasty", "Gnasty Gnorc", x=.78, y=.60, tam=420, dur=4.4, giro=4),

    *secreto("Número cinco", 5, "El salto que nadie programó", "Número cuatro"),
    mg(S.codigo(["cru", "cua"], "Doble salto", "Spyro se eleva más"), ("Salta, y justo en lo más alto", -.1), ("todavía más|fin", 1.0), ["Salta", "Si lo haces"], "codigo doble salto", y=.72),
    cam("sin pagarle a Moneybags", "moneybags", "Te ahorras a Moneybags", dur=4.6, x=.14, y=.66),
    ficha("No funciona ni en el primer juego", "Exclusivo", "No funciona *ni en el primero ni en el tercero*.", dur=5.4),

    *secreto("Número cuatro", 4, "Los dos niveles malditos", "Número tres"),
    ficha("La versión europea llevaba", "LibCrypt", "La protección anticopia de la *versión europea*.", dur=5.0),
    mg(S.pantallas_negras([P("cap_colossus"), P("cap_idol")], ["Colossus", "Idol Springs"]), ("Según el documental, con una copia pirata", -.1),
       ("la pantalla se quedaba en negro|fin", 1.2), ["hasta entrar a Colossus", "la pantalla se quedaba"], "pantallas negras", y=.54),
    ficha("En 2007 el juego salió", "PlayStation Network, 2007", "Versión europea: retirada *en menos de una semana*.", a=("en menos de una semana|fin", .9)),
    mapa([(_SF[0], _SF[1], "Colossus e Idol Springs", "peligro", "cap_colossus")], ("Porque había dos niveles que no cargaban", -.1), ("Colossus e Idol Springs|fin", 1.0),
         ["dos niveles"], titulo="Summer Forest", ventana=True),
    ficha("Nadie ha confirmado", "Coincidencia", "*Nadie lo ha confirmado.* En 2012 volvió, con la versión americana.", a=("ya con la versión americana|fin", .8), x=.28),

    *secreto("Número tres", 3, "Crash escondido dentro de Spyro", "Número dos"),
    mg(S.codigo(["L1", "R2", "cua"], "En la pantalla de inicio", "Demo de Crash Team Racing"), ("Cuando sale la pantalla de inicio", -.1), ("Se abre una demo|fin", 2.4),
       ["mantén L1", "Se abre una demo"], "codigo ctr", y=.72),
    mg(S.discos("Spyro 2", "Crash Team Racing", P("juego2"), P("cap_ctr")), ("Y al revés también", -.1), ("dentro del disco de la otra|fin", .8),
       ["Y al revés", "Crash Team Racing esconde", "cada una dentro"], "discos", y=.54),
    ficha("y un aviso", "El aviso", "«*On Shelves November 1999!*»", tipo="Demo de Spyro 2 en CTR", dur=4.4, x=.74, y=.20),

    *secreto("Número dos", 2, "El libro de los monstruos", "Número uno"),
    mg(S.libreta(["Aterrizar en un *ídolo*", "Todos los *molinos* de Hurricos", "Golpear a *Ripto* en Gulp's Overlook"], "Puntos de habilidad: 16", w=1100),
       ("Aterrizar en un ídolo", -.1), ("Golpear a Ripto en Gulp's Overlook|fin", 1.0), ["Aterrizar", "Todos los molinos", "Golpear a Ripto"], "libreta habilidad", y=.46),
    ficha("Si juntas suficientes", "Epílogos", "«Gulp found a new life at the Society for the Protection of *Abused Monsters* petting zoo.»", tipo="Guía del juego",
          a=("zoológico para monstruos maltratados|fin", .8), x=.5, y=.40, ancho=1020),
    grande("llega un libro: Faunus Mortas", "faunus_libro", "Faunus Mortas", lado="der", dur=6.6, tam=640),
    peg("escrito por Basil el Explorador", "basil", "Basil el Explorador", x=.17, y=.62, tam=340, dur=3.6),
    *[peg("Un gato con orejas de murciélago", "f_catabatus", "Catabatus", x=.12, y=.60, tam=320, dur=9.6),
      peg("un robot con pala", "f_farmae", "Farmae Robotum", x=.31, y=.60, tam=320, dur=8.0, giro=4),
      peg("un armadillo azul", "f_armapillow", "Armapillow", x=.50, y=.60, tam=320, dur=6.6),
      peg("un troll con un puño de piedra", "f_fistus", "Mister Fistus", x=.69, y=.60, tam=320, dur=5.2, giro=4),
      peg("y una cosita con orejas grandes", "f_wuss", "Wuss", x=.88, y=.60, tam=320, dur=3.8)],
    ficha("Los dejaron ahí", "Faunus Mortas", "Una *tumba cariñosa* para los diseños que no sobrevivieron.", a=("que no sobrevivieron|fin", 1.0), x=.5, y=.38),

    *secreto("Número uno", 1, "La cara de la moneda", "Spyro 2 sigue vivo"),
    mg(S.trueque([("Huevo", None), ("Semilla", None), ("Patito de goma", None), ("Nabo", None), ("Moneda dorada", P("cap_moneda"))]),
       ("En Mystic Marsh, el Profesor", -.1), ("por una moneda dorada|fin", 1.2),
       ["Un huevo", "por una semilla", "por un patito", "por un nabo", "por una moneda"], "trueque", y=.34),
    grande("Si acercas la cámara a esa moneda", "cap_moneda", "Una cara en relieve", lado="der", dur=6.0, tam=660),
    ficha("Es Dan Johnson, de Insomniac", "Dan Johnson", "De Insomniac Games: sus compañeros lo metieron *como broma interna*.", a=("como una broma interna|fin", .8), x=.28),
    peg("Su cara volvió a aparecer en Spyro 3", "juego3", "Spyro: Year of the Dragon", x=.78, y=.56, tam=460, dur=5.0, giro=4),
    ficha("Dan Johnson murió en diciembre de 2006", "Dan Johnson", "1974 - 2006\nRatchet & Clank: Size Matters *se le dedicó*.", dur=7.4, x=.5, y=.40),
    peg("El remake cambió esa cara", "reignited", "Reignited Trilogy", x=.2, y=.56, tam=460, dur=4.6),

    # ================================================================ CIERRE
    grande("En 2018 volvió con Reignited Trilogy", "reignited", "Reignited Trilogy", lado="der", dur=5.6, tam=560),
    peg("Toys for Bob lo rehízo", "toysforbob", "Toys for Bob", x=.2, y=.60, tam=380, dur=5.6),
    ficha("Tuvieron que crear una herramienta", "Spyro-scope", "Su herramienta para *mirar la geometría* de los juegos de PlayStation.", a=("copiarla con cuidado|fin", .7)),
    grande("Spyro: A Realm Beyond", "realm", "Primavera de 2027", lado="izq", dur=9.0, tam=760, giro=-2),
    mg(S.linea_tiempo([("1999", "Spyro 2"), ("2018", "Reignited Trilogy"), ("2027", "A Realm Beyond")], "Spyro sigue vivo", w=1400), ("Y en junio de este año", -.1),
       ("previsto para la primavera de 2027|fin", .9), ["Y en junio", "Spyro: A Realm Beyond", "previsto para la primavera"], "linea cierre", y=.82),
    cam("Tom Kenny vuelve a ser Spyro", "kenny", "Tom Kenny vuelve", dur=4.4, x=.14, y=.66),
    cam("Pero Stewart Copeland ya confirmó", "copeland", "Copeland no estará", dur=4.4, x=.86, y=.66),
    ficha("Ahora dime tú", "Te leo", "¿Pudiste con la *vagoneta*?", tipo="En los comentarios", a=("nos sirven para mejorar|fin", .8), x=.5, y=.40),
    sil("Y págale a Moneybags", "moneybags", "Moneybags", "Último aviso", dur=5.0, lado="der"),
]
# Tapas: las únicas fuentes de esos datos traen cámara web en la esquina (prototipo y doble salto); la pegatina la cubre.
def _tapa(de, a, slug, titulo, x=.865, y=.84, tam=350):
    return dict(tipo="mg", fn=S.pegatina(P(slug), titulo, tam, 0.0), de=de, a=a, x=x, y=y, sale=.2, nombre="pegatina tapa " + slug, ver=1.0)


FX += [_tapa("scene-115", "scene-119:fin", "elora", "Elora"), _tapa("scene-137", "scene-140:fin", "cap_glimmer", "Glimmer", x=.875, y=.79, tam=430)]
ROTULOS = []
SFX = {}
# SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/sp_*.mp3
_ESTRIBILLO = {"treinta": "sp_tiempo_mas", "veintinueve": "sp_agente0", "veintiocho": "sp_8piezas", "veintisiete": "sp_moneybags", "veintiséis": "sp_puno",
               "veinticinco": "sp_estatua", "veinticuatro": "sp_pterodactilo", "veintitrés": "sp_vasija", "veintidós": "sp_templo", "veintiuno": "sp_gulp_trago",
               "veinte": "sp_portal", "diecinueve": "sp_lava", "dieciocho": "sp_buceo", "diecisiete": "sp_muro", "dieciséis": "sp_vagoneta",
               "quince": "sp_portal_activo", "catorce": "sp_tiempo_fin", "trece": "sp_crush_mazo", "doce": "sp_vasija", "once": "sp_tiempo_fin",
               "diez": "sp_logo", "nueve": "sp_crush", "ocho": "sp_ahogo", "siete": "sp_portal_activo", "seis": "sp_gulp", "cinco": "sp_camello",
               "cuatro": "sp_muro", "tres": "sp_elefante", "dos": "sp_templo", "uno": "sp_estatua"}
PISTAS = [dict(sfx=v, en="Número " + k, vol=.45) for k, v in _ESTRIBILLO.items()] + [
    dict(sfx="sp_logo", en="Spyro 2 salió en noviembre de 1999", vol=.5),
    dict(sfx="sp_portal", en="Hoy te cuento cómo se hizo", vol=.45),
    dict(sfx="sp_portal_activo", en="Se meten al portal", vol=.5),
    dict(sfx="sp_crush", en="Y va acompañado de Crush", vol=.5),
    dict(sfx="sp_gulp", en="Crush y Gulp, dos criaturas", vol=.45),
    dict(sfx="sp_carga", de="la supercarga", a="o el supervuelo|fin", vol=.22),
    dict(sfx="sp_moneybags", en="También Moneybags", vol=.5),
    dict(sfx="sp_tiempo_mas", en="Cada nivel tiene un talismán", vol=.4),
    dict(sfx="sp_lamparas", en="Y aparecieron Hunter", vol=.3),
    dict(sfx="sp_publico", de="En Colossus, un monje te reta", a="Les gustó tanto que acabó dentro del juego|fin", vol=.22),
    dict(sfx="sp_rocas", en="con un volcán hecho de papel", vol=.35),
    dict(sfx="sp_vagoneta", en="y una vagoneta que no perdona", vol=.55),
    dict(sfx="sp_tiempo_fin", en="La pantalla se quedaba en negro", vol=.5),
    dict(sfx="sp_tiempo_mas", en="Es mi cumpleaños", vol=.5),
    dict(sfx="sp_gulp_trago", en="Gulp se traga el cetro", vol=.6),
    dict(sfx="sp_puno", en="Ripto ya no lleva cetro", vol=.4),
    dict(sfx="sp_8piezas", en="Faunus Mortas", vol=.45),
    dict(sfx="sp_moneybags", en="sin pagarle a Moneybags", vol=.45),
    dict(sfx="sp_agente0", en="Se abre una demo de Crash Team Racing", vol=.5),
]
